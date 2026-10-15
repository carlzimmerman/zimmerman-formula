# CFG800 FROZEN CRITERIA: score the two 2026 wide-binary papers against the sealed CFG740 prediction, and freeze the Gaia DR4 decision rule

Committed before any script. The prediction under test is CFG740: sealed 2026-10-13, sha 5336fd99…, never edited. It is a
velocity boost γ_v − 1 ≤ 3.2e-4 at 30 kAU and ≤ 8.9e-4 at 50 kAU (upper envelope). Its falsifier: γ_v ≥ 1.01 at s ≤ 50 kAU.

## Inputs (read from the arXiv sources of the two papers)
- **Cookson et al. 2026, arXiv:2602.24035 (MNRAS).** Table chi_sq_table: χ² of the median ṽ vs r_sky/r_M (6 points, 5 dof,
  normalization fitted), Newton vs MOND, for four quality cuts at d < 130 pc. Robustness text: d < 150 pc gives MOND 12×
  preferred (without the ipd cut), and Newton 88× preferred with ipd_frac_multi_peak = 0.
- **Chae & Yoon 2026, arXiv:2607.14450.** Velocity boost ≈ 1.15–1.20 at r_p/r_M > 1 (median ṽ), and acceleration boost
  γ ≈ 1.3–1.6.

## Scoring
- **S1 (Cookson).** The framework's χ² is the Newton χ² plus a perturbation. The framework's median-ṽ shift is at most
  3.2e-4 within 30 kAU. Bound the perturbation by scaling the paper's own Newton-to-MOND Δχ², taken for a ~20% velocity
  boost: Δχ²_F ≤ Δχ²_MOND · (3.2e-4/0.20)² (declared linear-response bound). CONSISTENT if p(χ²_N + Δχ²_F; 5 dof) ≥ 0.05
  for every cut.
- **S2 (Chae & Yoon).** Their claimed velocity boost 1.15–1.20 against the falsifier 1.01. Class "INCOMPATIBLE: kills CFG740
  if confirmed" when the claimed boost's lower end exceeds 1.01. No significance is re-derived here (their errors are not
  re-analysed).
- **Disclosure.** Report the d < 150 pc variant in which MOND is preferred.

## Gaia DR4 decision rule (frozen now; applied after 2026-12-02)
Statistic: the ratio R of median ṽ in r_p/r_M > 1 (s ≤ 50 kAU) to the Newtonian-regime normalization. Use the Cookson
quality checklist and a calibrated triple fraction, both as published. Classes:
- **FRAMEWORK KILLED** if R − 1 ≥ 0.01 at ≥ 3σ.
- **CONSISTENT** if |R − 1| < 0.01 at 2σ. Standard MOND (R ≈ 1.15–1.20) is then excluded.
- **UNDECIDED** otherwise.

Whichever happens is reported.

## Controls
- K1: the p-values of the published Newton χ² reproduce the table's Gaussian-equivalent tensions (0.1–0.28σ) within 0.05σ.
- MUTATE (separate output): the framework shift set to 0.20 must reproduce Δχ² ≈ the MOND Δχ² and drop p below 0.05.

κ fitted; not theory closed.
