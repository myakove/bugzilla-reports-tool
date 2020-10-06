import bugzilla
import yaml
import sys
import os
import google_api as gapi
from personal_config import *

# # [CHANGE NEEDED] Add the relevant information for you report
cfg_path = os.path.expanduser('~/.gapi/personal_cfg.yml')

if len(sys.argv) != 2:
    raise IndexError("You must provide the spreadsheet name to work with")

SPREADSHEET_NAME = sys.argv[1]
with open(cfg_path, 'r') as ymlfile:
    cfg = yaml.full_load(ymlfile)
    USER = cfg['bugzilla']['user']
    PASSWORD = cfg['bugzilla']['password']

#     # For the Bugzilla reports
#     gmail_user = cfg['bugzilla_report']['gmail_address']
#     gmail_pwd = cfg['bugzilla_report']['gmail_pass']
#     mail_to = USER

g = gapi.GoogleSpreadSheetAPI(SPREADSHEET_NAME, "Dashboard configuration")

PRODUCT = g.get_cell_value(2, 1)
BUGZILLA_PRODUCT = g.get_cell_value(2, 2)
VERSION = g.get_cell_value(2, 4)
# # The version flag should contain only x and y releases:
# # ocs-4.2.0 --> ocs-x.y.z so you'll need to add only ocs-4.2 in order to see
# # all bugs in version x.y
BUGZILLA_VERSION_FLAG = g.get_cell_value(2, 3)
LAYERED_PRODUCT = g.get_cell_value(4, 2)
LAYERED_PRODUCT_VERSION = g.get_cell_value(4, 3)

# [CHANGE NEEDED] List here all the teams you want to sample, for example:
team1 = "virt"
team2 = "storage"
team3 = "network"
team4 = "infra"

all_team = [team1, team2, team3]

severity = {
    "urgent": 1,
    "high": 2,
    "medium": 3,
    "low": 4,
    "unspecified": 5
}

BUGS_BY_TEAM = {
    team1: [],
    team2: [],
    team3: [],
}

team_members_g = gapi.GoogleSpreadSheetAPI(SPREADSHEET_NAME, "QE_team_member")

TEAM_MEMBERS = list()
idx = 1
while True:
    member = team_members_g.get_cell_value(idx, 1)
    if member:
        TEAM_MEMBERS.append(member)
        idx += 1
    else:
        break

# [CHANGE NEEDED] Add *ALL* the product components exist in Bugzilla for your
# product
COMPONENTS = {
    'Installation': [],
    'Virtualization': [],
    'Networking': [],
    'Storage': [],
    'Providers': [],
    'V2V': [],
    'Guest Support': [],
    'SSP': [],
    'Entitlements': [],
    'User Experience': [],
    'Metrics': [],
    'Logging': [],
}

backlog = {}
URL = "bugzilla.redhat.com"
bzapi = bugzilla.Bugzilla(URL, user=USER, password=PASSWORD)

# Bug statuses
VERIFIED = "VERIFIED"
ON_QA = "ON_QA"
MODIFIED = "MODIFIED"
OPEN_BUGS = "NEW,ASSIGNED,POST,MODIFIED,ON_DEV"
OPEN_BUGS_WITH_QA = "NEW,ASSIGNED,POST,MODIFIED,ON_DEV,ON_QA"
OPEN_BUGS_LIST = ["NEW", "ASSIGNED", "POST", "MODIFIED", "ON_DEV"]
OPEN_BUGS_LIST_WITH_QA = ["NEW", "ASSIGNED", "POST", "MODIFIED", "ON_DEV", "ON_QA"]

# Bug flags
BLOCKER = "blocker+"
CANDIDATE_BLOCKER = "blocker?"
MISSING_ACK = [
    "pm_ack?",
    "devel_ack?",
    "qa_ack?"
]
NEEDINFO = "needinfo?"
QUALITY_IMPACT = "quality_impact="

DEV_RESOLUTIONS = {
    'WONTFIX':2,
    'DEFERRED':3,
    'UPSTREAM':4,
    'CANTFIX':5,
    'EOL':6,
}

QE_RESOLUTIONS = {
    'NOTABUG':10,
    'WORKSFORME':11,
    'DUPLICATE':12,
    'INSUFFICIENT_DATA':13,
}

KEYWORD_FILTER = ['ABIAssurance', 'TechPreview', 'ReleaseNotes', 
                    'Tracking', 'Task', 'HardwareEnablement',
                    'SecurityTracking', 'TestOnly', 'Improvement',
                    'FutureFeature']
