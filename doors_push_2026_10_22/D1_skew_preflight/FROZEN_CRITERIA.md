# D1_skew_preflight: FROZEN CRITERIA (written before any script or computed number)

Door: the n = 1 vs n = 2 occupancy-noise skew test (A2 §7, A35 §9, A63 §6.1–6.2).
Question: can it run now on rotation-curve data on disk, and how much power does it really have?

Disclosure: before freezing, one hand estimate was made from the record's own formulas (n = 1 at
g = a₀/2: the log-space leading-order term −3σ_rel exceeds the linear skew term). Nothing else was
computed. No SPARC skew has been computed in this lane. A prior SPARC skew (CFG440 session04,
per-galaxy means, supply-limit test) exists in the record and is cited, not re-used as a test.

## Model (taken from the record, nothing new fitted)

- Occupancy: N_s independent binomial gates; at fixed g_N, δg = C δθ/(1 − u′(g)), Var θ = θ(1−θ)/N_s.
- n = 1: θ = g/(g+a₀), u = a₀θ, C = a₀, u′ = a₀²/(g+a₀)².
- n = 2: u = A₂ = g + a₀/2 − √(g² + a₀²/4), θ = 2A₂/a₀, C = a₀/2, u′ = 1 − g/√(g² + a₀²/4).
- Linear skew of the occupancy part: s_lin = (1−2θ)/√(N_s θ(1−θ)) (A63 eq. 17).
- Observed skew of occupancy + independent background: s_obs = s_occ φ³, φ = σ_occ/σ_tot (A63 §6.2).
- Statistical price: N(3σ) = 54/s_obs² (Gaussian SE √(6/N)); with correlated points, multiply by the
  design effect D = (SE_bootstrap-over-galaxies / √(6/N))² measured on SPARC.
- Window: g/a₀ ∈ (0.375, 1) ⇔ g_N/a₀ ∈ (0.10227, 0.5). Both footings: a₀ = 9.36e-11 and 1.13e-10 m/s².

## What is computed

T1. Reproduce the record: +0.707107 (n=1) and −0.348327 (n=2) at g = a₀/2 for N_s = 1; K30's
    N = 1.35e4 at φ = 0.447 with s_true = 0.7071.
T2. Point (a): with A2's normalisation (0.03 dex occupancy at g = a₀ ⇒ N_s = 93.1), the true occupancy
    skew is s_lin/√N_s. Compute N(3σ) self-consistently: σ_occ(g) from A2 eq. 18 at the same N_s,
    background 0.06 dex (A2/A63's number), at g = a₀/2 and averaged over the window, both laws.
T3. Point (b): the skew of the occupancy part in log g. Leading order s_log = s_lin − 3σ_rel
    (σ_rel = σ_g/g). Both terms ∝ N_s^{-1/2}, so the log-space sign is N_s-free at leading order.
    Check exactly by binomial enumeration at N_s = 93. Report the sign map of s_lin and s_log for
    both laws over the window, and the log-space flip points.
T4. Point (c): the background's own skew. Analytic: a log-symmetric background of width σ_dex has linear
    skew ≈ +3σ_dex ln10 (lognormal). Measured on SPARC (below).
T5. Best case from data: let all intrinsic scatter in the window be occupancy (φ_max = σ_int/σ_tot,
    σ_int² = σ_tot² − ⟨σ_meas²⟩). This fixes the smallest N_s the data allow and so the largest signal.

## SPARC measurement (systematic floor; NOT a test of n)

Sample: SPARC rotmod files (175), Q ≤ 2 from SPARC_Lelli2016c.mrt (never SPARC_table.txt),
Υ_disk = 0.5, Υ_bul = 0.7, points with g_bar > 0 and g_obs > 0. Residual = log g_obs demeaned within
0.1 dex bins of log g_bar (law-free: no reference ν is used). Per footing:
- F1 pooled out-of-window skew (bins with g_N/a₀ outside (0.10227, 0.5), within 10^±1.5 of a₀).
- F2 per-galaxy-demeaned skew (residual minus that galaxy's mean residual), in and out of window.
- F3 bootstrap over galaxies (2000, seed 22) of the window skew ⇒ SE_boot, design effect D, N_eff = N/D.
- Linear-g versions of the same (residual g_obs/⟨g_obs⟩_bin − 1).
- Systematic-skew floor s_floor := max over {log, linear} of |F1|, reported per variable.
- Reported-only diagnostic: the observed window skew (log and linear). It is NOT a test of n and
  enters no verdict.

Other data on disk: for each listed dataset, record point-level (yes/no), independent baryons per point
(yes/no), points and galaxies in the window on both footings, typical per-point error in dex. A dataset
without per-point baryonic g_N cannot host the test and is listed as such.

## Verdict lines (fixed now)

- Error in the record (point a): recorded if K30's s_true differs from the skew implied by the
  normalisation it is paired with (N_s = 93) by more than 10 %.
- RUNNABLE NOW: on both footings, for both laws, the best-case predicted |s_obs| in the variable
  where the two laws' signs differ exceeds both 3·SE_boot of the SPARC window skew and s_floor.
- DATA-GATED: fails RUNNABLE NOW only on N, with N_eff required ≤ 10⁶ points and best-case |s_obs|
  > s_floor; name the data.
- SCOPED NO-GO: best-case |s_obs| < s_floor in the variable where the signs differ, or N_eff required
  > 10⁶, or the two laws' predicted signs agree in the variable whose background is symmetric.
  The obstruction is named.

## Script rules

`d1_skew_preflight.py`: one line per check, `D1 COMPLETE: N/M checks PASS.`, exit 0 iff all pass;
writes `d1_skew_preflight.out` and `d1_skew_preflight_results.json`. `--mutate` replaces the corrected
s_true by K30's N_s = 1 value; the check that the corrected N(3σ) exceeds K30's by ≥ 50× must fail.
Outputs `*_MUTATE.out`, `*_results_MUTATE.json`. Single thread, no network.

## AMENDMENT 1 (post-result, script internals only; no verdict line changed)

- K1 compared n = 2 to −0.348327 (the value printed in A63 report.md's K18 row); the record's own
  computed value (a63_results.json) is −0.3483107. K1 now checks against the computed value; the printed
  digits are noted as a typo.
- K5 first required exact-vs-leading-order agreement within 25 % in both variables; the log-space
  magnitude differs by up to 28 % at g = 0.4 a₀ (N_s = 93, σ_rel ≈ 0.2 is not small). K5 now requires
  < 1 % in linear g and the same sign in log g at all probes; the exact values are printed.
