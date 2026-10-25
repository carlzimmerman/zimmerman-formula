# HG2 assumption ledger (written with the frozen criteria, before any script or number)

HG1's ledger rows A1–A9 and A11–A12 (`../HG1_hot_gas_selector/ASSUMPTION_LEDGER.md`) carry over unchanged, because the group
builder is HG1's, imported read-only. HG1's A10 (the SPARC reference) is replaced by B1–B6.

| id | assumption | type | where it enters | checked by |
|---|---|---|---|---|
| B1 | Isolated blue KiDS lenses (u−r < 2.5) are a cold-gas, non-hot-atmosphere reference at the groups' g_bar | DECLARED CHOICE (CFG829 class; fragility CFG840) | Δ, both arms equally | D5 variant (all isolated) |
| B2 | Lensing g_obs (B21 Eq. 7) and dynamical 3σ²/r measure the same g up to a level offset common to both arms | MODEL ASSUMPTION | per-arm medians; cancels in D | none (disclosed, §6) |
| B3 | log-linear interpolation between adjacent D4 points; no extrapolation | DECLARED CHOICE | Δ | K5 |
| B4 | D4 errors are Gaussian with B21's full covariance; draws ≤ 0 floored at 1% of central | MODEL ASSUMPTION | CI only | count reported |
| B5 | B21's lens g_bar (stars + estimated cold gas, point mass) is taken as published | READ from B21 README / CFG829 | reference x-axis | ±0.2 dex variants |
| B6 | D4 conversion constants G = 4.52e-30 pc²/(M☉ s²), pc = 3.086e16 m, ESD/bias | READ from B21 README | reference y-axis | K1 |
| B7 | a₀ = 9.3603e-11 and ν_e, used only to reproduce CFG829 in K1 | READ from CFG829 `cfg829.py` | K1 only, never the class | K1 |
| B8 | Scatter 0.25 dex for the power pre-flight | READ (HG1 A11, f22) | power only | none |
