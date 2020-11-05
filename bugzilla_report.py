#!/usr/bin/env python
import datetime
import sys

import helpers
from config import PRODUCT, VERSION
from personal_config import gmail_user, mail_to


temp = sys.stdout
sys.stdout = open(f"report_{PRODUCT}_status", "w")
print("<html><body>")
print("<h3>Hi,</h3>")
print(f"<h3>This is the status of {PRODUCT} - bugs:</h3>")
print(f"<h1><u>{PRODUCT} {VERSION} Status</u></h1>")
helpers.report_new_arrivals()
helpers.report_resolved_bugs()
helpers.report_status_on_qa()
helpers.report_on_qa_blockers()
helpers.report_open_blockers()
helpers.report_open_candidate_blockers()

print("<p></p>")
print("<h3>Thanks</h3>")
print("</body></html>")
sys.stdout = temp
raport_file = open(f"report_{PRODUCT}_status")
report = raport_file.read()
raport_file.close()
now = datetime.datetime.now()
date = "%s %s %s" % (now.strftime("%b"), now.strftime("%d"), now.year)
helpers.send_email(
    gmail_user,
    helpers.gmail_pwd,
    [mail_to],
    f"Bugzilla report [{date}] - {PRODUCT} QE Status",
    report,
)
