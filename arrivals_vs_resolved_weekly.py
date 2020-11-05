#!/usr/bin/env python
from datetime import datetime, timedelta

import helpers


CONST = 0
yesterday = datetime.today() - timedelta(days=7 * CONST) - timedelta(days=1)
week_time_frame = datetime.today() - timedelta(days=7 * CONST) - timedelta(days=7)
g = helpers.google_spread_sheet_api(sheet_name="weekly_arrivals_vs_resolved_data")

new_bugs = helpers.get_new_arrivals(
    changed_from=week_time_frame.strftime("%Y-%m-%d"),
    changed_to=yesterday.strftime("%Y-%m-%d"),
)
resolved_bugs = helpers.get_resolved_bugs(
    changed_from=week_time_frame.strftime("%Y-%m-%d"),
    changed_to=yesterday.strftime("%Y-%m-%d"),
)
verified_bugs = helpers.get_verified_bugs(
    changed_from=week_time_frame.strftime("%Y-%m-%d"),
    changed_to=yesterday.strftime("%Y-%m-%d"),
)
blocker_bugs = helpers.get_blocker_arrivals(
    changed_from=week_time_frame.strftime("%Y-%m-%d"),
    changed_to=yesterday.strftime("%Y-%m-%d"),
)
g.insert_row(
    [
        yesterday.strftime("%m-%d"),
        len(new_bugs),
        len(resolved_bugs),
        len(verified_bugs),
        len(blocker_bugs),
    ]
)
