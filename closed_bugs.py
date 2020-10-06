#!/usr/bin/env python
from helpers import *
import datetime


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
