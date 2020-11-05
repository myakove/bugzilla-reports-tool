#!/usr/bin/env python
import datetime
import time

import helpers


now = datetime.datetime.now()
g = helpers.google_spread_sheet_api(sheet_name="Release Readiness Criteria")

qe_backlog = len(helpers.get_qe_backlog())
g.update_sheet(6, 3, qe_backlog)

dev_backlog = len(helpers.get_dev_backlog())
g.update_sheet(6, 4, dev_backlog)

blockers = len(helpers.get_open_blockers())
g.update_sheet(6, 5, blockers)

candidate_blockers = len(helpers.get_open_candidate_blockers())
g.update_sheet(6, 6, candidate_blockers)

critical_bugs = len(helpers.get_critical_bugs())
g.update_sheet(6, 7, critical_bugs)

regressions = len(helpers.get_regression_bugs_targeted())
g.update_sheet(6, 8, regressions)

untriaged = len(helpers.get_untriaged_bugs())
g.update_sheet(6, 9, untriaged)

untargeted = len(helpers.get_untargeted_bugs())
g.update_sheet(6, 10, untargeted)

doc_bugs = len(helpers.get_doc_bugs())
g.update_sheet(6, 11, doc_bugs)

overall_backlog = len(helpers.get_overall_backlog())
g.update_sheet(6, 12, overall_backlog)

# Sleep to ensure no exception will raise from Google API due to writes limit
time.sleep(40)
bugs_for_pm_score = helpers.filter_only_bugs(helpers.get_dev_backlog(""))
top_10_bugs = helpers.sort_by_pm_score(bugs_for_pm_score)[:10]
for idx, bug in enumerate(top_10_bugs):
    row = 10 + idx
    column = 7
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

g.update_sheet(1, 1, f'Last update: {now.strftime("%Y-%m-%d %H:%M")}')
