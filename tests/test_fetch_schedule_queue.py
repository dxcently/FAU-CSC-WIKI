import io
import json
import os
import tempfile
import unittest
from contextlib import redirect_stderr

from loadscript import load

fetch_schedule_queue = load("fetch-schedule-queue.py")
parse_line    = fetch_schedule_queue.parse_line
drain         = fetch_schedule_queue.drain
load_current  = fetch_schedule_queue.load_current
sync          = fetch_schedule_queue.sync


def entry(date="2026-09-10", **fields):
    return json.dumps({"date": date, **fields})


def update(match_date, match_title, fields, **rest):
    return json.dumps({
        "op": "update",
        "match_date": match_date,
        "match_title": match_title,
        "fields": fields,
        **rest,
    })


class TestParseLine(unittest.TestCase):
    def test_date_only_line(self):
        got, err = parse_line(entry())
        self.assertIsNone(err)
        self.assertEqual(got, {"date": "2026-09-10"})

    def test_all_optional_fields_kept(self):
        got, err = parse_line(entry(
            title="Guest talk", track="learn", lead="Officers",
            room="CM 22 Room 125", link="https://example.com/rsvp",
            status="moved", added_by="123", added_at="2026-09-01T00:00:00Z",
        ))
        self.assertIsNone(err)
        self.assertEqual(got, {
            "date": "2026-09-10",
            "title": "Guest talk",
            "track": "learn",
            "lead": "Officers",
            "room": "CM 22 Room 125",
            "link": "https://example.com/rsvp",
            "status": "moved",
        })
        self.assertNotIn("added_by", got)
        self.assertNotIn("added_at", got)

    def test_empty_string_optional_fields_are_omitted_not_blank(self):
        got, err = parse_line(entry(title="", track="", room=""))
        self.assertIsNone(err)
        self.assertEqual(got, {"date": "2026-09-10"})
        self.assertNotIn("title", got)
        self.assertNotIn("track", got)
        self.assertNotIn("room", got)

    def test_invalid_status_dropped_but_other_fields_kept(self):
        got, err = parse_line(entry(title="Guest talk", status="tentative"))
        self.assertIsNone(err)
        self.assertEqual(got, {"date": "2026-09-10", "title": "Guest talk"})
        self.assertNotIn("status", got)

    def test_cancelled_status_kept(self):
        got, err = parse_line(entry(status="cancelled"))
        self.assertEqual(got["status"], "cancelled")

    def test_malformed_json_dropped_with_error(self):
        got, err = parse_line("{not json")
        self.assertIsNone(got)
        self.assertIn("invalid JSON", err)

    def test_json_scalar_not_object_dropped_with_error(self):
        got, err = parse_line("42")
        self.assertIsNone(got)
        self.assertIn("not a JSON object", err)

    def test_missing_date_dropped_with_error(self):
        got, err = parse_line(json.dumps({"title": "No date here"}))
        self.assertIsNone(got)
        self.assertIn("missing date", err)

    def test_invalid_date_dropped_with_error(self):
        got, err = parse_line(entry(date="not-a-date"))
        self.assertIsNone(got)
        self.assertIn("invalid date", err)

    def test_impossible_calendar_date_dropped_with_error(self):
        got, err = parse_line(entry(date="2026-13-40"))
        self.assertIsNone(got)
        self.assertIn("invalid date", err)


class TestDrain(unittest.TestCase):
    def test_appends_and_sorts_by_date(self):
        current = [{"date": "2026-09-01", "title": "First meeting"}]
        lines = [entry(date="2026-09-15", title="Later"), entry(date="2026-09-05", title="Earlier")]
        merged, warnings = drain(lines, current)
        self.assertEqual(warnings, [])
        self.assertEqual([e["date"] for e in merged], ["2026-09-01", "2026-09-05", "2026-09-15"])

    def test_malformed_line_dropped_rest_kept(self):
        lines = ["{not json", entry(date="2026-09-05", title="Ok")]
        merged, warnings = drain(lines, [])
        self.assertEqual(len(merged), 1)
        self.assertEqual(merged[0]["title"], "Ok")
        self.assertEqual(len(warnings), 1)
        self.assertEqual(warnings[0][0], "{not json")

    def test_blank_lines_skipped_silently(self):
        lines = ["", "   ", entry(date="2026-09-05", title="Ok")]
        merged, warnings = drain(lines, [])
        self.assertEqual(len(merged), 1)
        self.assertEqual(warnings, [])

    def test_op_absent_behaves_like_op_add(self):
        current = [{"date": "2026-09-01", "title": "First meeting"}]
        lines = [entry(date="2026-09-05", title="No op key at all")]
        merged_absent, warnings_absent = drain(lines, current)
        merged_add, warnings_add = drain(
            [json.dumps({"op": "add", "date": "2026-09-05", "title": "No op key at all"})],
            current,
        )
        self.assertEqual(merged_absent, merged_add)
        self.assertEqual(warnings_absent, warnings_add)
        self.assertEqual(warnings_absent, [])


class TestDrainUpdate(unittest.TestCase):
    def test_single_match_merges_fields_in_place(self):
        current = [
            {"date": "2026-09-01", "title": "First meeting"},
            {"date": "2026-09-10", "title": "Guest talk", "room": "CM 22 Room 125"},
        ]
        lines = [update("2026-09-10", "Guest talk", {"room": "CM 22 Room 200"})]
        merged, warnings = drain(lines, current)
        self.assertEqual(warnings, [])
        changed = next(e for e in merged if e["title"] == "Guest talk")
        self.assertEqual(changed["room"], "CM 22 Room 200")

    def test_date_field_change_re_sorts_the_list(self):
        current = [
            {"date": "2026-09-01", "title": "First meeting"},
            {"date": "2026-09-10", "title": "Guest talk"},
        ]
        lines = [update("2026-09-10", "Guest talk", {"date": "2026-08-15"})]
        merged, warnings = drain(lines, current)
        self.assertEqual(warnings, [])
        self.assertEqual([e["date"] for e in merged], ["2026-08-15", "2026-09-01"])
        self.assertEqual(merged[0]["title"], "Guest talk")

    def test_zero_matches_dropped_and_unchanged(self):
        current = [{"date": "2026-09-01", "title": "First meeting"}]
        lines = [update("2026-09-10", "No Such Talk", {"room": "CM 22 Room 200"})]
        merged, warnings = drain(lines, current)
        self.assertEqual(merged, current)
        self.assertEqual(len(warnings), 1)
        self.assertIn("no matching entry", warnings[0][1])

    def test_multiple_matches_dropped_and_unchanged(self):
        current = [
            {"date": "2026-09-10", "title": "Guest talk", "room": "A"},
            {"date": "2026-09-10", "title": "Guest talk", "room": "B"},
        ]
        lines = [update("2026-09-10", "Guest talk", {"room": "C"})]
        merged, warnings = drain(lines, current)
        self.assertEqual(merged, current)
        self.assertEqual(len(warnings), 1)
        self.assertIn("multiple matching entries", warnings[0][1])

    def test_invalid_field_dropped_valid_fields_still_applied(self):
        current = [{"date": "2026-09-10", "title": "Guest talk"}]
        lines = [update("2026-09-10", "Guest talk",
                         {"status": "tentative", "room": "CM 22 Room 200"})]
        merged, warnings = drain(lines, current)
        self.assertEqual(merged[0]["room"], "CM 22 Room 200")
        self.assertNotIn("status", merged[0])
        self.assertEqual(len(warnings), 1)
        self.assertIn("status", warnings[0][1])

    def test_invalid_date_field_dropped_valid_fields_still_applied(self):
        current = [{"date": "2026-09-10", "title": "Guest talk"}]
        lines = [update("2026-09-10", "Guest talk",
                         {"date": "not-a-date", "lead": "Officers"})]
        merged, warnings = drain(lines, current)
        self.assertEqual(merged[0]["date"], "2026-09-10")
        self.assertEqual(merged[0]["lead"], "Officers")
        self.assertEqual(len(warnings), 1)
        self.assertIn("date", warnings[0][1])

    def test_fields_empty_after_validation_dropped_and_unchanged(self):
        current = [{"date": "2026-09-10", "title": "Guest talk"}]
        lines = [update("2026-09-10", "Guest talk", {"status": "tentative"})]
        merged, warnings = drain(lines, current)
        self.assertEqual(merged, current)
        reasons = [w[1] for w in warnings]
        self.assertTrue(any("no valid fields to apply" in r for r in reasons))

    def test_fields_missing_entirely_dropped_and_unchanged(self):
        current = [{"date": "2026-09-10", "title": "Guest talk"}]
        lines = [json.dumps({
            "op": "update", "match_date": "2026-09-10", "match_title": "Guest talk",
        })]
        merged, warnings = drain(lines, current)
        self.assertEqual(merged, current)
        self.assertEqual(len(warnings), 1)
        self.assertIn("no valid fields to apply", warnings[0][1])

    def test_add_then_update_same_entry_in_one_drain_call(self):
        lines = [
            entry(date="2026-09-10", title="Guest talk"),
            update("2026-09-10", "Guest talk", {"room": "CM 22 Room 200"}),
        ]
        merged, warnings = drain(lines, [])
        self.assertEqual(warnings, [])
        self.assertEqual(len(merged), 1)
        self.assertEqual(merged[0]["room"], "CM 22 Room 200")

    def test_unrecognized_op_dropped_with_warning(self):
        lines = [json.dumps({"op": "delete", "date": "2026-09-10"})]
        merged, warnings = drain(lines, [])
        self.assertEqual(merged, [])
        self.assertEqual(len(warnings), 1)
        self.assertIn("delete", warnings[0][1])

    def test_missing_match_date_dropped_with_warning(self):
        current = [{"date": "2026-09-10", "title": "Guest talk"}]
        lines = [json.dumps({
            "op": "update", "match_title": "Guest talk", "fields": {"room": "X"},
        })]
        merged, warnings = drain(lines, current)
        self.assertEqual(merged, current)
        self.assertEqual(len(warnings), 1)
        self.assertIn("match_date", warnings[0][1])

    def test_missing_match_title_dropped_with_warning(self):
        current = [{"date": "2026-09-10", "title": "Guest talk"}]
        lines = [json.dumps({
            "op": "update", "match_date": "2026-09-10", "fields": {"room": "X"},
        })]
        merged, warnings = drain(lines, current)
        self.assertEqual(merged, current)
        self.assertEqual(len(warnings), 1)
        self.assertIn("match_title", warnings[0][1])

    def test_non_string_match_date_dropped_with_warning(self):
        current = [{"date": "2026-09-10", "title": "Guest talk"}]
        lines = [json.dumps({
            "op": "update", "match_date": 20260910, "match_title": "Guest talk",
            "fields": {"room": "X"},
        })]
        merged, warnings = drain(lines, current)
        self.assertEqual(merged, current)
        self.assertEqual(len(warnings), 1)
        self.assertIn("match_date", warnings[0][1])


class TestLoadCurrent(unittest.TestCase):
    def test_missing_file_defaults_to_empty_list(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(load_current(os.path.join(d, "nope.json")), [])

    def test_unparseable_file_warns_and_defaults_to_empty_list(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "bad.json")
            with open(path, "w") as f:
                f.write("{not json")
            stderr = io.StringIO()
            with redirect_stderr(stderr):
                got = load_current(path)
            self.assertEqual(got, [])
            self.assertIn("bad.json", stderr.getvalue())

    def test_existing_list_is_returned(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "sched.json")
            with open(path, "w") as f:
                json.dump([{"date": "2026-09-01", "title": "First"}], f)
            self.assertEqual(load_current(path), [{"date": "2026-09-01", "title": "First"}])


class SyncFixture(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.queue_path = os.path.join(self.tmp.name, "queue.jsonl")
        self.out_path = os.path.join(self.tmp.name, "discord-schedule.json")

    def write_queue(self, *lines):
        with open(self.queue_path, "w") as f:
            f.write("\n".join(lines))
            if lines:
                f.write("\n")

    def write_out(self, entries):
        with open(self.out_path, "w") as f:
            json.dump(entries, f, indent=2)

    def read_out(self):
        with open(self.out_path, encoding="utf-8") as f:
            return json.load(f)

    def read_queue(self):
        with open(self.queue_path, encoding="utf-8") as f:
            return f.read()


class TestSyncNoOpCases(SyncFixture):
    def test_env_path_unset_does_nothing(self):
        sync(None, self.out_path)
        self.assertFalse(os.path.exists(self.out_path))

    def test_missing_queue_file_does_nothing(self):
        sync(self.queue_path, self.out_path)  # queue_path never created
        self.assertFalse(os.path.exists(self.out_path))

    def test_empty_queue_file_does_nothing(self):
        open(self.queue_path, "w").close()
        sync(self.queue_path, self.out_path)
        self.assertFalse(os.path.exists(self.out_path))
        self.assertEqual(self.read_queue(), "")


class TestSyncWrite(SyncFixture):
    def test_well_formed_line_appends_and_sorts(self):
        self.write_out([{"date": "2026-09-01", "title": "First meeting"}])
        self.write_queue(entry(date="2026-09-05", title="Guest talk"))
        published = []
        sync(self.queue_path, self.out_path, publish=published.append)
        got = self.read_out()
        self.assertEqual([e["date"] for e in got], ["2026-09-01", "2026-09-05"])
        self.assertEqual(got[1]["title"], "Guest talk")
        self.assertEqual(published, [self.out_path])

    def test_missing_out_file_defaults_to_empty_before_appending(self):
        self.write_queue(entry(date="2026-09-05", title="Guest talk"))
        sync(self.queue_path, self.out_path, publish=lambda p: None)
        got = self.read_out()
        self.assertEqual(len(got), 1)

    def test_malformed_line_warns_and_does_not_abort_the_rest(self):
        self.write_out([])
        self.write_queue("{not json", entry(date="2026-09-05", title="Ok"))
        stderr = io.StringIO()
        with redirect_stderr(stderr):
            sync(self.queue_path, self.out_path, publish=lambda p: None)
        got = self.read_out()
        self.assertEqual(len(got), 1)
        self.assertEqual(got[0]["title"], "Ok")
        self.assertIn("{not json", stderr.getvalue())

    def test_invalid_date_warns_and_is_dropped(self):
        self.write_out([])
        self.write_queue(entry(date="not-a-date", title="Bad"))
        stderr = io.StringIO()
        with redirect_stderr(stderr):
            sync(self.queue_path, self.out_path, publish=lambda p: None)
        self.assertEqual(self.read_out(), [])
        self.assertIn("invalid date", stderr.getvalue())

    def test_queue_truncated_after_successful_write(self):
        self.write_out([])
        self.write_queue(entry(date="2026-09-05", title="Ok"))
        sync(self.queue_path, self.out_path, publish=lambda p: None)
        self.assertEqual(self.read_queue(), "")

    def test_publish_failure_leaves_queue_undrained(self):
        self.write_out([])
        self.write_queue(entry(date="2026-09-05", title="Ok"))

        def boom(path):
            raise RuntimeError("git push failed")

        with self.assertRaises(RuntimeError):
            sync(self.queue_path, self.out_path, publish=boom)
        # the write to out_path may have happened, but the queue must survive
        self.assertIn("2026-09-05", self.read_queue())

    def test_dry_run_touches_neither_file(self):
        self.write_out([{"date": "2026-09-01", "title": "First meeting"}])
        original_out = self.read_out()
        self.write_queue(entry(date="2026-09-05", title="Guest talk"))
        original_queue = self.read_queue()
        published = []
        sync(self.queue_path, self.out_path, dry_run=True, publish=published.append)
        self.assertEqual(self.read_out(), original_out)
        self.assertEqual(self.read_queue(), original_queue)
        self.assertEqual(published, [])


if __name__ == "__main__":
    unittest.main()
