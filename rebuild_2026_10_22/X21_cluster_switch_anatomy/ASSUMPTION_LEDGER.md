# X21_cluster_switch_anatomy: ASSUMPTION LEDGER (committed with the frozen criteria, before any script or number)

Classes: RAW / FRAMEWORK-NATIVE / SURVEY-CALIBRATION / ΛCDM-PROCESSED / STANDARD-MOND-MACHINERY / EXTERNALLY-CALIBRATED /
DECLARED (this lane's choice).

| # | ingredient | class | source | note |
|---|---|---|---|---|
| A1 | KiDS-1000 shear, per-cluster ΔΣ sums D, E, Dx, DRR, boost sums | RAW (+ SURVEY-CALIBRATION m = −0.01) | X7 `x7_measure_percluster.npz` (= X2 replay, X7 K1) | not re-measured |
| A2 | PSF leakage template leakP (LK-P) | SURVEY-CALIBRATION (fit on KiDS) | X7 npz | CAL subtraction only |
| A3 | coherent cross / R−R excess s_×, s_RR, κ_b | DECLARED by X7 (isotropic systematic) | X7 JSON `all` | binned tables only |
| A4 | per-bin σ_leak,b scaled from the all-cluster value | DECLARED (approximation) | this lane | templates not committed; ≤ 0.002 |
| A5 | C\* law model (AQUAL μ = x/(1+x), β-model gas + r⁻³ beyond 2.2 R500, f\* = 0.20, Chae+21 EFE, reduced shear, miscentring) | FRAMEWORK-NATIVE law; gas EXTERNALLY-CALIBRATED; EFE median from data | X2 source exec'd | inherited unchanged |
| A6 | native h 0.672 / 0.686 distances, q^{5/2} gas rescale | FRAMEWORK-NATIVE | X2 / F1 | |
| A7 | MGAS500, L500, L300kpc, KT, BEST_Z | RAW-ish X-ray catalogue (eRASS1 pipeline) | `erass1cl_primary_v3.2.fits` | MGAS500 carries eRASS1 selection; KT only for 106 (brighter clusters: a selected subset) |
| A8 | M500 | ΛCDM-PROCESSED | eRASS1 FITS | reported only |
| A9 | c_X = L300kpc / L500 as a concentration / cool-core proxy | DECLARED | eRASS1 FITS | 300 kpc / R500 varies with R500 (itself a scaling-relation product), so c_X carries mass dependence; Spearman with MGAS500 reported |
| A10 | redMaPPer λ (SDSS; KiDS-N overlap only) | SURVEY-CALIBRATION | CFG688 TSV + CFG688 match rule | 83 matches; λ ≥ 20 only |
| A11 | BCG and member stellar masses (LePhare, A1 total-flux rebuild) | EXTERNALLY-CALIBRATED | CFG922 `cfg922_census_A1.json` | CFG922: aperture bias, rebuilt flux, may include envelope light |
| A12 | CFG922 census ↔ X7 326 join by exact position via CFG687 npz | DECLARED | CFG687 npz | 281 of 326 |
| A13 | stellar M/L bracket 3.78/1.78, HI bracket f_HI,95 = 0.196 | EXTERNALLY-CALIBRATED | CFG922 (SLACS Auger+2009, xGASS) | |
| A14 | molecular gas bracket = HI bracket | DECLARED | this lane | no table on disk |
| A15 | ICL | NOT ON DISK | CFG922 | reported as a needed multiple; ×10 scale is CFG922's declared line |
| A16 | needed-mass shapes GS (gas-traced) and PS (central point) | DECLARED diagnostic (X2's components) | X2 `model` comp GS/PS | λ is never carried into a model |
| A17 | X13 selection correction | not applicable (no source split) | X13 | quoted only |
| A18 | thresholds (Δχ² 9 / 4, |Z| 2, p 0.01, quantile grid) | DECLARED | this lane | 7 variables, not trial-corrected |
