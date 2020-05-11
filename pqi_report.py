#!/usr/bin/env python
from helpers import *
from datetime import datetime

now = datetime.today()
g = gapi.GoogleSpreadSheetAPI(SPREADSHEET_NAME, "PQI_report")

dev_backlog = get_dev_backlog()
new = filter_by_status(dev_backlog, 'NEW')
assigned = filter_by_status(dev_backlog, 'ASSIGNED')
post = filter_by_status(dev_backlog, 'POST')
modified = filter_by_status(dev_backlog, 'MODIFIED')

qe_backlog = get_qe_backlog()
overall_backlog = get_overall_backlog()

# Regression rate = all bugs with REGRESSION keyword / all bugs in version
all_bugs = len(get_all_bugs_in_version())
all_regressions = len(get_all_regression_bugs())
if all_bugs > 0:
    regression_rate = round((all_regressions / float(all_bugs)), 4)

# FailedQA = MOVED FROM ON_QA to ON DEV / ALL BUGS targeted
all_targeted_bugs = len(get_all_bugs_targeted_to_version())
all_failedqa_bugs =  len(get_all_failedqa_bugs())
if all_targeted_bugs > 0:
    failed_qa_rate = round(all_failedqa_bugs / all_targeted_bugs)

# Verification rate = VERIFIED+RELEASE PENDING+CLOSED / was ON QA
all_bugs_was_on_qa = len(get_all_was_on_qa_bugs())
all_verified = len(get_all_verified_bugs())
if all_bugs_was_on_qa > 0:
    verification_rate = round((all_verified / float(all_bugs_was_on_qa)), 4)

# Rejected = CLOSED (NOT A BUG, WORKS FOR ME, DUPLICATE, INSOFFICIENT DATA, EOL, DEFFERED. CANT FIX, WONT FIX) / ALL BUGS
all_bugs = len(get_all_bugs_in_version())
all_rejected = len(get_all_rejected_bugs())  # QUERY DOESNT SEEM RIGHT
if all_bugs > 0:
    rejected_rate = round((all_rejected / float(all_bugs)), 4)

# Reopen = any VERIFIED and above to (ON DEV or ON QA) / ALL BUGS
all_reopened_bugs = len(get_all_reopened_bugs())
if all_bugs > 0:
    reopned_rate = round((all_reopened_bugs / float(all_bugs)), 4)

# Resolution = VERIFIED / all bugs
all_targeted = len(get_all_bugs_targeted_to_version())
if all_bugs > 0:
    resolution_rate = round((all_verified / float(all_targeted)), 4)

g.insert_row(
    [
         now.strftime("%Y-%m-%d"), len(new), len(assigned),
         len(post), len(modified), len(qe_backlog), len(overall_backlog), 
         regression_rate, all_regressions, 
         resolution_rate, all_verified,
         reopned_rate, all_reopened_bugs,
         verification_rate, all_verified,
         rejected_rate, all_rejected,
         failed_qa_rate, all_failedqa_bugs,
    ]
)
