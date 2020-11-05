import datetime
import time

import helpers
from config import LAYERED_PRODUCT, LAYERED_PRODUCT_VERSION


now = datetime.datetime.now()
g = helpers.google_spread_sheet_api(sheet_name="Layered products bugs")

qe_backlog = len(
    helpers.get_qe_backlog_by_component(
        product=LAYERED_PRODUCT,
        target_version=LAYERED_PRODUCT_VERSION,
        component="Console Kubevirt Plugin",
    )
)
g.update_sheet(6, 3, qe_backlog)

dev_backlog = len(
    helpers.get_dev_backlog_by_component(
        product=LAYERED_PRODUCT,
        target_version=LAYERED_PRODUCT_VERSION,
        component="Console Kubevirt Plugin",
    )
)
g.update_sheet(6, 4, dev_backlog)

overall_backlog = len(
    helpers.get_overall_backlog_by_component(
        product=LAYERED_PRODUCT, component="Console Kubevirt Plugin"
    )
)
g.update_sheet(6, 5, overall_backlog)
time.sleep(30)

# QUERY DOESNT WORK AS EXPECTED
all_affecting_product_urgent = len(helpers.get_dependent_product_bugs("urgent"))
g.update_sheet(6, 6, all_affecting_product_urgent)

all_affecting_product = len(helpers.get_dependent_product_bugs())
g.update_sheet(6, 7, all_affecting_product)
