# CFG366: the reservoir rule in the nonlinear PM run

Criteria: `FROZEN_CRITERIA.md`, committed alone first in 5f3a22464. The engine is CFG361's, copied and not imported (`cfg366_pm.py`), with one added switch, RES. In ON cells it adds T5's excess e = f max(s_ph - s_c, 0) and subtracts the same mass over a Gaussian catchment of width R_c, so gravitating mass is conserved above ~R_c. The literal local min rule is identical to S0, a non-test, and was not run.

**Frozen verdict (R_c = 1 Mpc/h, the lane verdict): GROWTH OK.** R_c = 3 Mpc/h: **TENSION.**

| run (vs S0, z = 0) | sigma8 ratio | P(k) ratio at 0.1 / 0.3 / 1 h/Mpc | max abs(P - 1), k <= 1 | overdraw (mass), z1 / z0.5 / z0 |
|---|---|---|---|---|
| R_c 1, canonical | 1.0095 | 1.015 / 1.022 / 1.054 | 0.057 | 0.069 / 0.142 / 0.233 |
| R_c 1, alt | 1.0111 | 1.018 / 1.026 / 1.066 | 0.069 | 0.090 / 0.172 / 0.263 |
| R_c 3, canonical | 1.0335 | 1.031 / 1.094 / 1.285 | 0.290 | 0.065 / 0.139 / 0.212 |
| R_c 3, alt | 1.0403 | 1.036 / 1.114 / 1.352 | 0.355 | 0.088 / 0.167 / 0.237 |
| T5 (CFG361), canonical / alt | 1.205 / 1.257 | 1.36 / 1.55 / 1.60 (canonical) | | |

**Reading after the run (verify a pass as hard as a fail; no number changed):**
- **R_c = 1 Mpc/h is about 1.3 mesh cells** (cell = 0.78 Mpc/h). That is below the Lagrangian radius of even a Milky-Way host (about 1.4 Mpc/h for 1e12 Msun/h; 3.0 for 1e13; 6.5 for 1e14). Most of the compensation therefore lands on the host's own cells. That is close to the R_c -> 0 limit, which is S0 by construction. The pass is real under the frozen rule, but it sits near the trivial limit.
- **At the physically motivated host-scale catchment (R_c = 3, group scale) the result is TENSION.** sigma8 is only +3-4%, but small-scale power is +29-35% at k = 1. That is still a large improvement on T5's +20-26% sigma8.
- **Overdraw.** At z = 0, 21-26% of the mass sits in cells where the catchment would need more cold than is locally present. As frozen, the bookkeeping would drive the cold density negative there. A physical version must source those cells from farther away, which pushes toward larger R_c and more small-scale power.
- The removed cold is not moved as particles (no mechanism; declared). This is a gravity-level bookkeeping test.

**Net.** Local mass conservation removes most of B's excess growth (sigma8 from +20-26% to +1-4%). The scale at which the conservation acts matters: host-scale catchments leave a +30% small-scale excess and a local supply shortfall. This narrows the problem; it does not close it.

**Controls.** Field-level checks on CFG361's z = 0 snapshot (read-only, 128^3), `cfg366_checks.out`: C0 non-vacuous, C1 compensation, C2 limits (T5 and S0 reproduced exactly), C3 S0 read. MUTATE fails C1, rc 1. C1 also passes at every snapshot of every run. **Disclosed:** the first version of the checks used a scaled IC field with no ON cells (vacuous passes). It was replaced before any PM run. No 128^3 resolution run was made, so resolution was not tested.

Re-run: `python3 cfg366_checks.py`, then `python3 cfg366_run_all.py` (4 x ~25-45 min, 2 at a time), then `python3 cfg366_analysis.py`. Work data in `../../../_external_data/cfg366_work/`.
