# HG1 assumption ledger (written with the frozen criteria, before any script or number)

| id | assumption | type | where it enters | checked by |
|---|---|---|---|---|
| A1 | Group in dynamical equilibrium; g_obs = 3σ²/r at r = (4/3) R_h | MODEL ASSUMPTION | both arms equally | none (disclosed) |
| A2 | Υ_K = 0.6, M_K,☉ = 3.28, no extinction correction | MODEL ASSUMPTION | g_bar, both arms | variants 0.5 / 0.8 |
| A3 | M★(<r) = half the total (Wolf-style) | MODEL ASSUMPTION | g_bar | none |
| A4 | Hot gas follows the β-model (r_c 0.15 R500, β 2/3) normalised to eRASS1 Mgas500 | MODEL ASSUMPTION (record convention: F1, CFG687) | X-BRIGHT g_bar | none |
| A5 | X-FAINT hot gas = 0 | MODEL ASSUMPTION | X-FAINT g_bar | variant 0.1 M★ |
| A6 | No cold gas in either arm | DATA LIMIT (D2 has no HI) | both arms | disclosed |
| A7 | d = HRV/H0, H0 67.70 | MODEL ASSUMPTION (CFG689 native) | g_obs only | variant 73.0; g_bar is d-free (K3) |
| A8 | eRASS1 match: 0.5 Mpc projected, 1500 km/s | DECLARED CHOICE | X flag | none (fixed now) |
| A9 | eRASS1 footprint = 179.94° ≤ l ≤ 359.94°, |b| ≥ 10° | DECLARED CHOICE | sample | K2 (transform only) |
| A10 | SPARC reference = the matched-clumping rule (0.30 dex segments, ≥ 8 galaxies) | READ from `reviews/matched_clumping_2026_10_24/FROZEN_CRITERIA.md` | Δ | K1 |
| A11 | Scatter 0.25 dex for the power pre-flight | READ from f22 (memory: project_cluster_standing) | power only | none |
| A12 | eRASS1 column meanings (1 RA, 2 Dec, 3 z, 5 Mgas500 ×1e11, 8 R500 kpc) | READ from CFG687 `cfg687_stack.py` | X flag, gas | none |
