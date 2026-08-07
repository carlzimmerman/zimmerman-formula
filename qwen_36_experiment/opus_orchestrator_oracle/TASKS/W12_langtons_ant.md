# W12 — Langton's ant builds a highway
COST: S | script: `wacky_langtons_ant.py`

> WACKY. No framework rules. Two still apply: **every check must be able to fail**, and **refine once and
> report the shift**. Script goes in `real_research/reviews/`, prefixed `wacky_`.

An ant on a grid: on white, turn right, flip the cell, step; on black, turn left. For ~10,000 steps it
looks chaotic. Then at step ~10,000 it spontaneously builds a periodic **"highway"** of period 104 and
runs off forever. Nobody has proved it always does this. Implement it, find the exact step at which the
highway starts, verify the period is 104, and confirm the drift direction. Then generalise to
multi-colour ants (Turmites) and tabulate which rule strings produce highways vs symmetric growth vs
apparent chaos. The check that matters: your highway period must be exactly 104, not approximately.
