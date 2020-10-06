#!/usr/bin/env python
from helpers import *
from datetime import datetime, timedelta

import gspread

gc = gspread.service_account()

now = datetime.today() - timedelta(days=7)
g = gc.open(SPREADSHEET_NAME)
worksheet = g.worksheet("Weekly_PQI_report")

dev_backlog = get_dev_backlog()
new = filter_by_status(dev_backlog, 'NEW')
assigned = filter_by_status(dev_backlog, 'ASSIGNED')
post = filter_by_status(dev_backlog, 'POST')
modified = filter_by_status(dev_backlog, 'MODIFIED')

qe_backlog = get_qe_backlog()
overall_backlog = get_overall_backlog()

# Resolution = VERIFIED / all targeted
all_resolved = len(get_all_verified_bugs())
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
