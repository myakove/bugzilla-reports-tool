#!/usr/bin/env python
import time
import google_api as gapi
from helpers import *
import datetime

now = datetime.datetime.now()
g = gapi.GoogleSpreadSheetAPI(SPREADSHEET_NAME, "Release Readiness Criteria")

qe_backlog = len(get_qe_backlog())
g.update_sheet(6, 3, qe_backlog)

dev_backlog = len(get_dev_backlog())
g.update_sheet(6, 4, dev_backlog)

blockers = len(get_open_blockers())
g.update_sheet(6, 5, blockers)

candidate_blockers = len(get_open_candidate_blockers())
g.update_sheet(6, 6, candidate_blockers)

critical_bugs = len(get_critical_bugs())
g.update_sheet(6, 7, critical_bugs)

regressions = len(get_regression_bugs_targeted())
g.update_sheet(6, 8, regressions)

untriaged = len(get_untriaged_bugs())
g.update_sheet(6, 9, untriaged)

untargeted = len(get_untargeted_bugs())
g.update_sheet(6,10, untargeted)

doc_bugs = len(get_doc_bugs())
g.update_sheet(6, 11, doc_bugs)

overall_backlog = len(get_overall_backlog())
g.update_sheet(6, 12, overall_backlog)

# Sleep to ensure no exception will raise from Google API due to writes limit
time.sleep(40)
bugs_for_pm_score = filter_only_bugs(get_dev_backlog(""))
top_10_bugs = sort_by_pm_score(bugs_for_pm_score)[:10]
for idx, bug in enumerate(top_10_bugs):
    row = 10 + idx
    column = 7
    g.update_sheet(
        row,
        column,
        (
            f'=HYPERLINK("https://bugzilla.redhat.com/show_bug'
            f'.cgi?id={bug.bug_id}", "{bug.bug_id}")'
        )
    )
    g.update_sheet(row, column+1, bug.summary)
    g.update_sheet(row, column+6, bug.status)
    g.update_sheet(row, column+7, bug.component)
    g.update_sheet(row, column+8, bug.severity)
    converted = datetime.datetime.strptime(
        bug.creation_time.value, "%Y%m%dT%H:%M:%S"
    )
    g.update_sheet(row, column + 9, (now - converted).days)

# # Regression rate = all bugs with REGRESSION keyword / all bugs in version
# all_bugs = len(get_all_bugs_in_version())
# all_regressions = len(get_all_regression_bugs())
# if all_bugs > 0:
#     regression_rate = round((all_regressions / float(all_bugs)), 4)
#     g.update_sheet(10, 2, regression_rate)
#     g.update_sheet(10, 4, all_regressions)

# # FailedQA = MOVED FROM ON_QA to ON DEV / ALL BUGS targeted
# all_targeted_bugs = len(get_all_bugs_targeted_to_version())
# all_failedqa_bugs =  len(get_all_failedqa_bugs())
# if all_bug_to_version > 0:
#     print(all_targeted_bugs)
#     failed_qa_rate = round(all_failedqa_bugs / all_targeted_bugs)
#     g.update_sheet(13, 2, failed_qa_rate)
#     g.update_sheet(13, 4, all_failedqa_bugs)

# # Verification rate = VERIFIED+RELEASE PENDING+CLOSED / was ON QA
# all_bugs_was_on_qa = len(get_all_was_on_qa_bugs())
# all_verified = len(get_all_verified_bugs())
# if all_bugs_was_on_qa > 0:
#     verification_rate = round((all_verified / float(all_bugs_was_on_qa)), 4)
#     g.update_sheet(16, 2, verification_rate)
#     g.update_sheet(16, 4, all_verified)

# # Rejected = CLOSED (NOT A BUG, WORKS FOR ME, DUPLICATE, INSOFFICIENT DATA, EOL, DEFFERED. CANT FIX, WONT FIX) / ALL BUGS
# all_bugs = len(get_all_bugs_in_version())
# all_rejected = len(get_all_rejected_bugs())  # QUERY DOESNT SEEM RIGHT
# if all_bugs > 0:
#     rejected_rate = round((all_rejected / float(all_bugs)), 4)
#     g.update_sheet(25, 2, rejected_rate)
#     g.update_sheet(25, 4, all_rejected)

# # Reopen = any VERIFIED and above to (ON DEV or ON QA) / ALL BUGS
# all_reopened_bugs = len(get_all_reopened_bugs())
# if all_bugs > 0:
#     reopned_rate = round((all_reopened_bugs / float(all_bugs)), 4)
#     g.update_sheet(22, 2, reopned_rate)
#     g.update_sheet(22, 4, all_reopened_bugs)

# # Resolution = VERIFIED / all bugs
# all_targeted = len(get_all_bugs_targeted_to_version())
# if all_bugs > 0:
#     verified_rate = round((all_verified / float(all_targeted)), 4)
#     g.update_sheet(19, 2, verified_rate)
#     g.update_sheet(19, 4, all_verified)

g.update_sheet(1, 1, f'Last update: {now.strftime("%Y-%m-%d %H:%M")}')
