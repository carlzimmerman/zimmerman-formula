# SUPERSEDED 2026-09-23

`highz_deepmond_target_list_2026.py` and `highz_deepmond_target_list_2026_results.json` carry
literature values that contradict their cited primary sources. This was flagged BLOCKER on
2026-07-25 in commit 1c7781ed3e and never fixed. Do not use them for any proposal or paper.
The verified replacement is `highz_target_ledger_verified_2026.py` (with `.out` and
`_results.json`), where every row was re-read from its primary paper with table locations.
The old files are kept unchanged as the record of what was wrong.
