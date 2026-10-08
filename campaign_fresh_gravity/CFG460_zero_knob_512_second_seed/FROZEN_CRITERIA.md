# CFG460 FROZEN CRITERIA: the zero-knob growth fix at 512³ in a second random realisation
(owner 2026-10-08: "keep open doors". Committed before any run. PAPER45 v2 lists "one realisation at 512³" as a limitation, and this lane addresses it.)

**Runs (cfg424_pm.py, NSEED 512, seed 360, canonical, FLAT):**
- S0: the Newtonian control, same seed;
- TA: the zero-knob rule (RC = 0, f_ret ≡ 1).

**Decision (CFG361 cuts, TA against the same-seed S0).**
- **CONFIRMED (second realisation):** GROWTH OK.
- **NOT CONFIRMED:** otherwise.

**Reported:** q_max, the largest catchment draw, against 0.49 for seed 359 at 512³. A draw above 1 (overdraw) would break the rule.

The runs go one at a time, 8 threads each, about 5 h in total.
