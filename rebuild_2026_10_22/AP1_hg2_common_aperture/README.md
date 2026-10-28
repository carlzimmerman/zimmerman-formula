# AP1_hg2_common_aperture: HG2's negative sign survives a common physical aperture

Criteria: `FROZEN_CRITERIA.md` (5bb77f83c6, committed alone, before any script or number); no amendment.
Machinery: GA1's committed script, executed read-only.

κ = ½ FITTED. Not "theory closed". Nothing here says the data favour the framework.

## Verdict (frozen): **SIGN SURVIVES A COMMON APERTURE** (canonical and alt)

| aperture | measured D [95 %] | D_pred, base (canonical / alt) | all-law |
|---|---|---|---|
| GA1 own (4/3) R_h (Step 0) | −0.362 [−0.605, −0.139] | +0.306 / +0.282 | +0.173 |
| **0.5 Mpc (PRIMARY)** | **−0.356 [−0.572, −0.101]** | **+0.264 / +0.244** | +0.193 |
| 0.3 Mpc | −0.313 [−0.526, −0.118] | +0.293 / +0.269 | +0.143 |
| 0.8 Mpc | −0.406 [−0.653, −0.151] | +0.158 / +0.142 | +0.188 |
| HG2 original rows, 0.5 Mpc | −0.300 [−0.474, −0.112] | +0.106 / +0.084 | +0.101 |

**The geometric lever runs the other way.** The median R_h is 0.39 Mpc for BRIGHT groups and 0.21 Mpc for FAINT ones,
so the bright groups are the *more* extended arm.

## The finding that led to FM1

At a common aperture, g_obs = 3σ²/r depends **only on σ**, and HG2 bins in σ. So the statistic conditions on the
observed pull. At a fixed pull, the arm with more counted baryons must sit lower against any rising reference. The
predicted D was never subjected to the same conditioning. FM1 (9c9d980ba0) tests exactly that.

## Checks: 3/3

- **K0:** Step 0 reproduces GA1's PRIMARY.
- **K1:** the aperture light at 10 Mpc equals all members.
- **K2:** peak RSS 0.70 GB.
- **Rerun:** byte-identical.
- **MUTATE twin** (light counted outside r_ap): K1 fails, exit 1.
