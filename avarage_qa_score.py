#!/usr/bin/env python
from datetime import datetime

import helpers


REGRESSION = 15
BLOCKER = 30
TEST_BLOCKER = 20


now = datetime.today()
g = helpers.google_spread_sheet_api(sheet_name="average_quality_score_data")

all_bugs = helpers.get_overall_backlog()
if len(all_bugs) > 0:
    all_qa_scores = [helpers.get_quality_score(b) for b in all_bugs]
    all_qa_scores = list(filter(lambda a: a != -1, all_qa_scores))
    avarage_qa_score = 100 - sum(all_qa_scores) / len(all_qa_scores)
    g.insert_row([now.strftime("%Y-%m-%d"), avarage_qa_score])
