# CFG431 FROZEN CRITERIA: is the settling clock's scatter universal? (galaxy point added to T14)

Committed alone, before any script. kappa = 1/2 FITTED and untouched; a0 enters only through the record's law (nu_mono) used to
form the beyond-law mass. No dark-matter particle species; the cold MASS is still required. Local compute only, no downloads.
Never "theory closed".

## Door
T14 (deepseek_push/openai_math_cross_analysis_2026-10/t14_scatter_face) read sigma(ln t) = 0.468 (clusters) / 0.409 (groups)
from sigma(f)/f = eps(f) sigma(ln t) with f := 0.43 / 0.60. T15 (t15_cold_budget) showed those numbers are CFG382's LEFTOVER
e = exp(-Gamma t), not the settled f. The audit (README.md row T12/T14) calls T14's numeric readings provisional. Two further
problems found while reading, declared now: (a) T14's +-0.15 is CFG382's declared TOLERANCE band, not a measured population
scatter; (b) the group 0.60 (cm03 definition B, weak-lensing bias) and the cluster 0.43 (definition A, b = 0) are on different
definitions (CFG382 target audit).

## Branch (declared)
The quantity measured at every scale is the retained beyond-law cold fraction, definition A:
    e_i = (M_tot - M_b - M_ph) / (5.364 M_b)            (cm08 for galaxies; cfg382_target_audit for groups/clusters)
CFG382 calibrates e = exp(-Gamma tau) directly against this quantity (MW 0.14, clusters 0.430), so e_i is the LEFTOVER branch.
Exact transport on this branch: d ln e / d ln t = -Gamma t = ln e, hence
    sigma(e)/e = |ln e| * sigma(ln t)    =>    S := sigma(ln t) = sigma_e / (e_med * |ln e_med|)
(the same identity as T14 rewritten on e; eps(f) = (1-f)|ln(1-f)|/f with f = 1 - e gives the identical S). S is defined only
for 0 < e_med < 1. Caveat recorded: T15's table labels the def-A values "deficit x = M_missing/M_b"; the def-A formula is
normalised by the cosmic cold share 5.364 M_b, so here they are read as CFG382 reads them (e). If that reading is wrong, no
clock reading of these numbers exists and the verdict below is void.

## Samples (all on disk, all definition A, b = 0, canonical a0 = 9.3603e-11 m/s^2)
- GALAXY: the cm08 "0.13" cell = the 23 non-central SLUGGS early types (Alabi+2017, 5 Re), computed exactly as cm08.
- GROUP: the 20 Lovisari+2015 groups at R500, exactly as cfg382_target_audit (stars := 0.10 M_gas).
- CLUSTER: the 7 X-COP clusters with stellar profiles at R500, exactly as cfg382_target_audit.

## Estimator (same for all three)
e_med = median(e_i); sigma_e = (P84 - P16)/2 of e_i; S = sigma_e/(e_med |ln e_med|).
Error (the tolerance, from the data): bootstrap over objects, 4000 resamples, seed 431. delta_k = (P84 - P16)/2 of ln S* over
replicates; replicates with e_med* outside (0, 1) get S* = +inf (so a class near e = 1 gets an infinite or large delta).
S is TOTAL scatter (intrinsic + measurement noise + Gamma variation across objects): an upper bound on the intrinsic clock scatter.

## Decision rule (primary row)
Pairwise z_ij = |ln S_i - ln S_j| / sqrt(delta_i^2 + delta_j^2), three pairs.
- NOT UNIVERSAL: any z_ij >= 2.
- UNIVERSAL (consistent and informative): all z_ij < 2 AND every delta_k <= 0.35 (each S known to about +-40%).
- CONSISTENT, NOT DIAGNOSTIC: all z_ij < 2 but some delta_k > 0.35.
- A class with e_med outside (0, 1) is UNDEFINED; the rule runs on the remaining classes and the verdict is labelled so. If the
  galaxy class itself cannot be formed, the verdict is NOT POSSIBLE ON DISK.

## Robustness rows (reported; if any flips the verdict category the final label carries "FRAGILE")
R1 alt footing a0 = 1.1312e-10 (galaxies; groups/clusters as the audit uses canonical); R2 X-COP gas mass at R500 (the audit
interpolates M_gas at log R = 0, i.e. 1 Mpc, while M_HSE is at R500 -- a quirk of the record, reproduced in the primary);
R3 hydrostatic bias b = 0.1 (groups and clusters); R4 noise-corrected galaxy/group/cluster scatter: per-object input errors
(Alabi M_tot and f_DM; Lovisari eM500, eMgas500; X-COP EM_FORW) propagated by Monte Carlo (Gaussian, 2000 draws, seed 431),
sigma_e,int^2 = sigma_e^2 - sigma_noise^2 (if negative: S_int = 0, reported).
Also reported only: the exact per-object map ln t_i = ln(-ln e_i) + const for 0 < e_i < 1 (robust scatter, number dropped);
T14's own inputs re-read on the e branch (expected 0.413 clusters, 0.489 groups; the +-0.15 being a tolerance) and on T14's
f branch (0.468 / 0.409) for comparison.

## Checks (exit 1 on failure)
- C1 identity: finite-difference d ln e/d ln t equals ln e at 40 points, rel err < 1e-6; and S(e branch) equals T14's formula
  with f = 1 - e to 1e-12.
- C2 reproduction: T14 re-read gives 0.413 +- 0.002 (clusters) and 0.489 +- 0.002 (groups) on the e branch, 0.468 / 0.409 on the
  f branch; galaxy median 0.13 +- 0.005 (cm08, 23 objects); group / cluster medians 0.787 / 0.413 +- 0.002 (target audit).
- C3 control integrity: the galaxy S in the run equals the unmutated reference S (rel 1e-9).
- MUTATE (T431_MUTATE=1, writes *_MUTATE outputs): galaxy per-object e_i -> e_med + k (e_i - e_med) with k = 4 or 1/4, whichever
  moves S_gal AWAY from the geometric mean of S_grp and S_cl (an injected clock break of ln 4 = 1.39). Must: C3 fail, and the
  rule return NOT UNIVERSAL. If the injected break is NOT detected (verdict not NOT UNIVERSAL under MUTATE), the test is declared
  underpowered and the primary verdict can be at most CONSISTENT, NOT DIAGNOSTIC (a NOT UNIVERSAL primary stands regardless).
