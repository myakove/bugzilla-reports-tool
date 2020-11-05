#!/usr/bin/env python
import datetime

import helpers


now = datetime.datetime.now()
g = helpers.google_spread_sheet_api(sheet_name="Performance & scale blockers")

perf_blockers = helpers.sort_by_pm_score(helpers.get_performance_blockers())
for idx, bug in enumerate(perf_blockers):
    row = 23 + idx
    column = 2
    g.update_sheet(
        row,
        column,
        (
            f'=HYPERLINK("https://bugzilla.redhat.com/show_bug'
            f'.cgi?id={bug.bug_id}", "{bug.bug_id}")'
        ),
    )
    g.update_sheet(row, column + 1, bug.summary)
    g.update_sheet(row, column + 6, bug.status)
    g.update_sheet(row, column + 7, bug.component)
    g.update_sheet(row, column + 8, bug.severity)
    converted = datetime.datetime.strptime(bug.creation_time.value, "%Y%m%dT%H:%M:%S")
    g.update_sheet(row, column + 9, (now - converted).days)

g.clean_rows(2, 23 + len(perf_blockers), 36)

scale_blockers = helpers.sort_by_pm_score(helpers.get_scale_blockers())
for idx, bug in enumerate(scale_blockers):
    row = 6 + idx
    column = 2
    g.update_sheet(
        row,
        column,
        (
            f'=HYPERLINK("https://bugzilla.redhat.com/show_bug'
            f'.cgi?id={bug.bug_id}", "{bug.bug_id}")'
        ),
    )
    g.update_sheet(row, column + 1, bug.summary)
    g.update_sheet(row, column + 6, bug.status)
    g.update_sheet(row, column + 7, bug.component)
    g.update_sheet(row, column + 8, bug.severity)
    converted = datetime.datetime.strptime(bug.creation_time.value, "%Y%m%dT%H:%M:%S")
    g.update_sheet(row, column + 9, (now - converted).days)

g.clean_rows(2, 6 + len(scale_blockers), 19)


g.update_sheet(1, 1, f'Last update: {now.strftime("%Y-%m-%d %H:%M")}')
