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
