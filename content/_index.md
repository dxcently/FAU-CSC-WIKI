+++
title = "FAU Cybersecurity Club"
type = "home"

[params.hero]
  kicker  = "Florida Atlantic University"
  # No "FAU" here on purpose — the kicker directly above already spells the
  # university out in full. Falls back to the site title if you delete it.
  title   = "Cybersecurity Club"
  tagline = "Learn it. Break it. Defend it."

# The recurring weekly meeting. Shown in the panel under the hero.
[params.meeting]
  day   = "Tuesdays & Thursdays"
  time  = "5:00 – 7:00 PM"
  room  = "CM 22"
  note  = "CM 22 is in the Computer Center on the Boca Raton campus, between the library and Fleming Hall. Every week during the fall and spring semesters."

# ---------------------------------------------------------------------------
# SEMESTER SCHEDULE — this is the part you edit every week.
#
# Add one [[params.sessions]] block per meeting. Keep dates as "YYYY-MM-DD"
# strings. The site works out the state of every row from the date on its own:
#
#   date is in the past      -> done      (dimmed, struck through)
#   date is today            -> TODAY     (red bar)
#   first date still ahead   -> NEXT      (red bar — only ever one row)
#   any date after that      -> upcoming
#
# You only set `status` by hand to override that. Valid values:
#   status = "cancelled"   meeting called off
#   status = "moved"       date changed, say what happened in the title
#
# `room` is optional. Leave it out and the row shows the weekly room from
# [params.meeting] above. Set it when a session is somewhere else — another
# room, another building, or "Online" — and that cell is highlighted so it
# does not get skimmed past.
#
# Order does not matter. Rows are sorted by date when the page builds.
# ---------------------------------------------------------------------------

[params.schedule]
  semester = "Fall 2026"
  note     = "Tuesdays, Thursdays 5–7 PM in CM 22. Topics can shift — check Discord."

[[params.sessions]]
  date  = "2026-09-01"
  title = "First meeting: What we do as a club"
  track = "general"
  lead  = "Officers"
  link  = "https://fau.campuslabs.com/engage/organization/cybersecurity"

[[params.sessions]]
  date  = "2026-09-03"
  title = "Join us for a meeting with a guest speaker from <insert when we get it>"
  track = "learn, network"
  lead  = "Guest Speaker"
  link  = "https://fau.campuslabs.com/engage/organization/cybersecurity"
+++

## Contact

Email: <csc@fau.edu> — or message **@shaamad**, club president, on the
[Discord](http://discord.gg/2Yun8WAUuy).
