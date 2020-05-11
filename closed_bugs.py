#!/usr/bin/env python
import time
from helpers import *
import datetime


DEV_RESOLUTIONS = {
    'WONTFIX':2,
    'DEFERED':3,
    'UPSTREAM':4,
    'CANTFIX':5
}
QE_RESOLUTIONS = {
    'NOTABUG':10,
    'WORKSFORME':11,
    'DUPLICATE':12,
    'INSUFFICIENT_DATA':13
}

now = datetime.datetime.now()
g = gapi.GoogleSpreadSheetAPI(SPREADSHEET_NAME, "Closed_bugs")

col = 2
for component in COMPONENTS:
    for resolution, row in DEV_RESOLUTIONS.items():
        number_of_closed_dev_bugs = get_num_of_closed_bugs_by_resolution_and_component(component, resolution)
        g.update_sheet(row, col, number_of_closed_dev_bugs)
    for resolution, row in QE_RESOLUTIONS.items():
        number_of_closed_qe_bugs = get_num_of_closed_bugs_by_resolution_and_component(component, resolution)
        g.update_sheet(row, col, number_of_closed_qe_bugs)
    col+=1
