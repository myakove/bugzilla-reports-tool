#!/usr/bin/env python
from helpers import *
from datetime import datetime, timedelta

import gspread

gc = gspread.service_account()

#now = datetime.today()
now = datetime.today() - timedelta(days=1)
#g = gapi.GoogleSpreadSheetAPI(SPREADSHEET_NAME, "PQI_report")
g = gc.open(SPREADSHEET_NAME)
worksheet = g.worksheet("PQI_report")

dev_backlog = get_dev_backlog()
new = filter_by_status(dev_backlog, 'NEW')
assigned = filter_by_status(dev_backlog, 'ASSIGNED')
post = filter_by_status(dev_backlog, 'POST')
modified = filter_by_status(dev_backlog, 'MODIFIED')

qe_backlog = get_qe_backlog()
overall_backlog = get_overall_backlog()

# Regression rate = all bugs with REGRESSION keyword / all bugs in version
all_bugs = len(get_all_bugs_in_version())
regression_rate = 0
all_regressions = len(get_all_regression_bugs())
if all_bugs > 0:
    regression_rate = round((all_regressions / float(all_bugs)), 2)

# Verification rate = VERIFIED+RELEASE PENDING+CLOSED / was ON QA
all_bugs_was_on_qa = len(get_all_was_on_qa_bugs())
all_verified_closed = len(get_all_verified_bugs_closed())
verification_rate = 0
if all_bugs_was_on_qa > 0:
    verification_rate = round((all_verified_closed / float(all_bugs_was_on_qa)), 2)

# Rejected = CLOSED (NOT A BUG, WORKS FOR ME, DUPLICATE, INSOFFICIENT DATA, EOL, DEFFERED. CANT FIX, WONT FIX) / ALL BUGS
resolution_list = list(DEV_RESOLUTIONS.keys()) + list(QE_RESOLUTIONS.keys())
rejected_rate = 0
all_rejected = len(filter_by_resolution(get_all_rejected_bugs(),resolution_list))
if all_bugs > 0:
    rejected_rate = round((all_rejected / float(all_bugs)), 2)

# Reopen = any VERIFIED and above to (ON DEV or ON QA) / ALL BUGS targeted
all_reopened = -1
all_targeted = len(get_all_bugs_targeted_to_version())
try:
    all_reopened = len(get_all_reopened_bugs())
except:
    print("All reopened query Timeout")
if all_targeted > 0:
    reopned_rate = round((all_reopened / float(all_targeted)), 2)

# Resolution = VERIFIED / all targeted
all_resolved = len(get_all_verified_bugs())
resolution_rate = 0
if all_targeted > 0:
    resolution_rate = round((all_resolved / float(all_targeted)), 2)

# FailedQA = MOVED FROM ON_QA to ON DEV / ALL BUGS targeted
all_failedqa = -1
try:
    all_failedqa = len(get_all_failedqa_bugs())
except:
    print("FailedQA query Timeout")
if all_targeted > 0:
    failed_qa_rate = round((all_failedqa / float(all_targeted)), 2)

worksheet.insert_rows(
    [[
         now.strftime("%m-%d"), len(new), len(assigned),
         len(post), len(modified), len(qe_backlog), len(overall_backlog), 
         regression_rate, all_regressions, 
         resolution_rate, all_resolved,
         reopned_rate, all_reopened,
         verification_rate, all_verified_closed,
         rejected_rate, all_rejected,
         failed_qa_rate, all_failedqa,
         "=sum(B2:F2)"
    ]], row=2,
    value_input_option='USER_ENTERED'
)
