#!/usr/bin/env python
from datetime import datetime, timedelta

import gspread
import helpers
import pqi_report
from config import SPREADSHEET_NAME


gc = gspread.service_account()

now = datetime.today() - timedelta(days=7)
g = gc.open(SPREADSHEET_NAME)
worksheet = g.worksheet("Weekly_PQI_report")

dev_backlog = helpers.get_dev_backlog()
new = helpers.filter_by_status(dev_backlog, "NEW")
assigned = helpers.filter_by_status(dev_backlog, "ASSIGNED")
post = helpers.filter_by_status(dev_backlog, "POST")
modified = helpers.filter_by_status(dev_backlog, "MODIFIED")

qe_backlog = helpers.get_qe_backlog()
overall_backlog = helpers.get_overall_backlog()

# Resolution = VERIFIED / all targeted
all_resolved = len(helpers.get_all_verified_bugs())
if pqi_report.all_targeted > 0:
    resolution_rate = round((all_resolved / float(pqi_report.all_targeted)), 2)

# FailedQA = MOVED FROM ON_QA to ON DEV / ALL BUGS targeted
all_failedqa = -1
try:
    all_failedqa = len(helpers.get_all_failedqa_bugs())
except:
    print("FailedQA query Timeout")
if pqi_report.all_targeted > 0:
    failed_qa_rate = round((all_failedqa / float(pqi_report.all_targeted)), 2)

worksheet.insert_rows(
    [
        [
            now.strftime("%m-%d"),
            len(new),
            len(assigned),
            len(post),
            len(modified),
            len(qe_backlog),
            len(overall_backlog),
            pqi_report.regression_rate,
            pqi_report.all_regressions,
            resolution_rate,
            all_resolved,
            pqi_report.reopned_rate,
            pqi_report.all_reopened,
            pqi_report.verification_rate,
            pqi_report.all_verified_closed,
            pqi_report.rejected_rate,
            pqi_report.all_rejected,
            failed_qa_rate,
            all_failedqa,
            "=sum(B2:F2)",
        ]
    ],
    row=2,
    value_input_option="USER_ENTERED",
)
