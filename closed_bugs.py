#!/usr/bin/env python
import datetime

import helpers
from config import COMPONENTS, DEV_RESOLUTIONS, QE_RESOLUTIONS


now = datetime.datetime.now()
g = helpers.google_spread_sheet_api(sheet_name="Closed_bugs")


col = 2
for component in COMPONENTS:
    for resolution, row in DEV_RESOLUTIONS.items():
        number_of_closed_dev_bugs = helpers.get_num_of_closed_bugs_by_resolution_and_component(
            component, resolution
        )
        g.update_sheet(row, col, number_of_closed_dev_bugs)
    for resolution, row in QE_RESOLUTIONS.items():
        number_of_closed_qe_bugs = helpers.get_num_of_closed_bugs_by_resolution_and_component(
            component, resolution
        )
        g.update_sheet(row, col, number_of_closed_qe_bugs)
    col += 1
