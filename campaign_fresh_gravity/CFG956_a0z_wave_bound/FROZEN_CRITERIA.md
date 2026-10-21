# CFG956 — the largest wave in a0(z) that the framework's own expansion constraint (CFG689) allows (FROZEN, before any script or number from this lane)

Block CFG950–959; the id was reserved in the LEDGER (6000c01b24). The owner's question (2026-10-21): what if a0(z) oscillates like
a wave as the universe expands? Compute the largest wave in a0(z) that the expansion data allow, with framework-native inputs only.

## 1. The law, and what a wave means here
- a0(z) = κ c √(G ρ_DE(z)), with κ = ½ FITTED. So a0(z)/a0(0) = √(ρ_DE(z)/ρ_DE(0)). A wave in a0 is a wave in ρ_DE, squared.
- Footings: canonical 9.3603e-11 and alt 1.1312e-10 m s⁻². They are never pooled.
- Every bound in this lane is on the ratio a0(z)/a0(0), with ρ_DE(0) free (CFG689's own free w(0)).
  - The footing sets a0(0), and κ is fitted per footing. So ε_95(P) is the same number on both footings by construction.
  - The footings enter only through the absolute a0(z): figure panel (d) and the galaxy-side check. There, s* is converted per footing
    (× 9.3603e-11 / a0_footing) and each footing is drawn separately.

## 2. Likelihood: CFG689 primary, re-implemented (read-only use of its committed files)
- **Why not import it.** CFG689's script runs a full mode on import and overwrites its own outputs, so it is not imported.
- **What is re-implemented.** Its primary mode (cfg689.json "cfg"), rebuilt line for line:
  - **BAO:** DESI DR2, 6 anisotropic tracers (D_M/r_d, D_H/r_d, correlation) and BGS D_V/r_d, copied verbatim from CFG689's ANISO/ISO.
  - **SN:** Pantheon+ STAT+SYS (sha256 abf806d9… for the covariance), non-calibrators with zHD > 0.01, z_hel in the luminosity
    distance. M is profiled. That is identical to CFG689's analytic marginalisation (a linear parameter with a flat prior).
  - **Curvature:** free (ω_k free, |ω_k| ≤ 0.25), the primary row. The flat mode F is a CFG689 bracket and is not used.
  - **Priors:** Gaussian on ω_b = 0.02236 ± 0.00015 and ω_c = 0.1202 ± 0.0014, uncorrelated.
  - **Ruler:** r_d(ω_b, ω_c) = r_d0 (ω_b/ω_b0)^(−b) (ω_c/ω_c0)^(−c), with CFG689's stored CAMB ruler: r_d0 = 147.06667 Mpc,
    b = 0.168947, c = 0.215442 (cfg689.json "ruler"). No CAMB call and no external r_d.
  - **Background:**
    - ρ_m = ω_m (1+z)³ with ω_m = ω_b + ω_c and Σm_ν = 0.
    - ω_r = 2.4728e-5 (1 + 0.2271 × 3.044).
    - z grid from 0 to 2.5 with 5001 points; trapezoid comoving distance; D_M with curvature (sinh/sin).
  - **Not used:** θ* (CFG689's θ* rows are held back because its K9 failed); no CMB distance, no ΛCDM late-time fit, no CPL.
- **Native background.** The CFG689 primary BAO+SN best fit (cfg689.json BAO+SN.P2.pbest):
  - nodes w = {0.31161, 0.32453, 0.39289, 0.26210, 0.27994, 0.26284} at z = {0, 0.4, 0.7, 1.0, 1.5, 2.33};
  - ω_k 0.00389, ω_b 0.022360, ω_c 0.120195;
  - χ² 1388.3423.
- Its constant-ρ_DE best fit has χ² 1399.4561 (P2 Δχ² 11.11 for 5 dof, 1.97σ: constant not rejected).

## 3. Wave family (declared here; no knob scan beyond it)
ρ_DE(z)/ρ_crit,100 = W · A(z)² · [1 + ε sin(2π ln(1+z)/P + φ)]²,  so  a0(z)/a0(0) = A(z) [1 + ε sin(2π ln(1+z)/P + φ)] / (1 + ε sin φ).
- **W** is the free present-day amplitude (CFG689's free w(0)). It absorbs the formula's z = 0 value, 1 + ε sin φ, so a0(0) stays
  the footing value.
- **Branches:**

  | branch | A(z) | weight |
  |---|---|---|
  | S (smooth) | A(z)² = w_best(z)/w_best(0): the CFG689 primary best-fit node curve (piecewise linear in z, constant beyond 2.33), shape fixed | verdict |
  | C (constant) | A ≡ 1 | verdict |
  | N (free nodes) | six free nodes (CFG689's own freedom) times the wave: ρ_DE = w_nodes(z) [1 + ε sin(…)]², nodes in [−2, 3] as in CFG689 | reported only; run only at the 7 representative periods. Long periods are expected to be absorbed by the nodes |

- **ε** ∈ [0, 1]. a0 = κc√(Gρ_DE) ≥ 0, and ε = 1 already lets a0 touch zero at the troughs.
- **φ** ∈ [0, 2π) is PROFILED (maximised), not marginalised.
- **Period grid** (19 values, about log-uniform, roughly 10 per decade):
  P ∈ {0.05, 0.0625, 0.075, 0.1, 0.125, 0.15, 0.2, 0.25, 0.3, 0.4, 0.5, 0.6, 0.75, 1.0, 1.25, 1.5, 2.0, 2.5, 3.0}.
  - Representative periods: 0.05, 0.1, 0.25, 0.5, 1.0, 2.0, 3.0.
  - No P is added after the first number. Between grid points ε_95 is not computed.
- **Nuisances** (profiled, as CFG689's best fit treats them): W, ω_k, ω_b, ω_c, M. Branch N adds its six nodes, and W is then w_nodes(0).

## 4. Statistic and numerics
- **Profiles.**
  - χ²_prof(ε; P) = minimum over φ and the nuisances.
  - χ²_min(P) = the same minimum, also over ε ∈ [0, 1].
  - Δχ²_prof(ε; P) = χ²_prof(ε; P) − χ²_min(P).
- **The bound.** ε_95(P) is the smallest ε ≥ ε̂(P) with Δχ²_prof = 3.84 (the owner's rule).
  - If Δχ²_prof(1) < 3.84: NO BOUND (ε_95 ≥ 1).
  - If Δχ²_prof drops back below 3.84 at a larger grid ε: flag DISJOINT and report the allowed set.
- **Wave preference per P.** Δχ²_0(P) = χ²_prof(0) − χ²_min(P), with 2 dof (ε, φ); local p and σ-equivalent. It is not corrected for
  the 19 periods; the Bonferroni ×19 is stated.
  - Class, from the largest Δχ²_0 over the grid: NO WAVE PREFERRED (< 5.99); LOCAL HINT (5.99–11.83); LOCAL ≥ 3σ (≥ 11.83, still
    uncorrected).
  - A branch-C preference that matches CFG689's own node shape (the z ≈ 0.7 bump, P2 Δχ² 11.1/5) is not a wave detection, and the
    README says so.
- **Numerics.**
  - ε evaluation grid: {0, 0.005, 0.01, 0.02, 0.03, 0.05, 0.075, 0.1, 0.15, 0.2, 0.3, 0.45, 0.6, 0.8, 1.0}.
  - At each ε: 16 φ starts (k·2π/16). Each is refined by least squares (scipy least_squares, trf; φ and the nuisances free) and
    warm-started from the same start at the previous ε. The best is kept.
  - χ²_min(P) comes from a free (ε, φ, nuisance) refit, started from the best grid point, with ε bounded to [0, 1].
  - ε_95 is found by brentq on the bracketing interval, to |Δε| ≤ 1e-3.
- **Low z vs high z.**
  - The primary likelihood has no datum above z = 2.33, and its grid ends at z = 2.5. So ε_95(P) is a bound set by the z ≤ 2.33
    data alone.
  - Above z ≈ 2.5 the expansion data place no bound. K5 checks that a wave confined to z > 2.5 changes χ² by exactly 0
    (|Δχ²| ≤ 1e-9) at ε = 1 for every P.
  - Reported only: the share of H² carried by ρ_DE at z 2.5 / 3.5 / 4.5 at the CFG689 best fit, and the fact that the held-back θ*
    row is the only CFG689 datum that reaches beyond 2.5.
  - The allowed envelope of a0(z)/a0(0) at z 0.5 / 1.0 / 1.5 / 2.33 is reported per period. It is A(z)(1 ± ε_95) bounds, plus the
    exact ratio at the bound's own φ.

## 5. The owner's sketch, as an explicit curve
- **The curve:** S(z) = exp of a PCHIP interpolant in u = ln(1+z) through (u, ln s), at (z, s) = (0, 1), (0.5, 2), (2.5, 0.3),
  (4.5, 3). S is held constant beyond z 4.5 (scipy PchipInterpolator). ρ_DE = W S(z)².
- **Δχ²_sketch,** with W, ω_k, ω_b, ω_c and M profiled, is reported against:
  - (a) the CFG689 node best fit χ²;
  - (b) the constant-ρ_DE best fit (the same nuisances: the like-for-like comparison).
- **Class vs (b):** EXCLUDED if ≥ 9; DISFAVOURED if 4–9; ALLOWED if < 4.
- **Also reported:** the same with W fixed at w_best(0), and the per-block χ² split (each BAO tracer, BGS, SN, priors).
- **Implied H(z) shift at z = 0.5.**
  - Primary definition: H with ρ_DE(0.5) = S(0.5)² w_best(0) = 4 w_best(0), and ω_m, ω_k, ω_r at the CFG689 best fit, divided by the
    CFG689 best-fit H(0.5).
  - Reported: the sketch's own profiled fit over the CFG689 best-fit H(0.5), and the shift in D_H/r_d against the DESI LRG1 z = 0.51
    datum, in units of its error.

## 6. Galaxy-side check (reported only, no verdict weight)
- **Points.** The record's implied-a0 points, as drawn by chart_a0z_one.py and by panel (d) of the 2026-10-21 summary figure:
  - chart_a0z_points.csv rows with no_root = 0 and a finite s* (CFG223, CFG228, CFG229);
  - CFG303 native RC100 route B Q1–Q3 and CRISTAL R_e / R_out;
  - CFG309 MeerKAT HI (z from CFG301).
  - RC100 B Q4 is an upper bound only: it is listed, with no σ.
- **Error per point:** σ_i = ½ [log10 hi68 − log10 lo68] (dex).
- **G1: the change in the predicted a0 at z_i.**
  - Largest allowed change, conservatively: the maximum over the P grid and over φ ∈ [0, 2π) of
    |log10[(1 + ε_95 sin(θ(z_i)+φ)) / (1 + ε_95 sin φ)]|, per branch. G1/σ_i is reported.
  - For z_i > 2.5 the README also states that the expansion data allow ε up to 1 there (a0 anywhere from 0 to 2 A(z)).
- **G2: the change in the points themselves, through distances.**
  - δlog10 a0_imp ≈ −2 δlog10 D_A (deep-MOND scaling; g_bar does not depend on distance).
  - D_A is taken from the bound wave (P, ε_95(P), φ and nuisances at the bound) against ε = 0, on an extended z grid to 6.
  - Reported only; this is a scaling.
- **Expected:** no allowed wave moves any point by more than its 68% error.
- **Footings:** s* is converted per footing. G1 and G2 in dex do not depend on the footing.

## 7. Controls
- **K1:** χ² at CFG689's stored pbest equals 1388.34228 to within 1e-3.
- **K2:** the profiler at ε = 0:
  - branch S χ²_min within [1388.3423 − 0.05, 1388.3423 + 0.01];
  - branch C within ±0.02 of 1399.4561.
- **K3:** CFG681 reproduced as in CFG689's own K3 (flat, h 0.68, ruler profiled analytically): BAO 10.5515 at Ω_m 0.2970, BAO+SN
  1400.143 at 0.3039. Tolerances 0.01 / 0.001 / 0.02 / 0.001.
- **K4: CFG689's band at its nodes, from this implementation.**
  - Sampler: CFG689's own (MH, Hessian proposal with h = 0.1 in its standardised coordinates, 4 chains × 60 000, seeds 6891–6894,
    20% burn-in).
  - sqrtX median and 68% edges at z 1.0, 1.2 and 1.5 within 0.02 of cfg689.json.
  - At z 2.33: median and upper edge within 0.05, lower edge within 0.10. The looser lower edge is for Monte Carlo noise: 13% of the
    samples have w ≤ 0 there, so the density near q16 is low.
  - Node posterior means within 0.25 σ_node, and stds within 15%. R-hat < 1.02.
- **K5:** a wave windowed to z > 2.5 gives Δχ² ≡ 0.
- **Overall K PASS** needs K1–K5. If any K fails there is no main verdict, and the main numbers are reported as unverified.
- **MUTATE** (frozen pass rule; separate _MUTATE outputs):
  - Mock: noiseless predictions of the K model (CFG689 primary pbest), with a wave ε = 0.3, P = 0.5, φ = 0 injected in a0. The BAO
    values and SN m_b are replaced, at the same errors (M = 0). Priors are unchanged.
  - Fit: branch S at P = 0.5.
  - PASS if Δχ²_prof(0) ≥ 3.84 (zero excluded), ε = 0.3 lies in the 95% allowed interval, and |ε̂ − 0.3| ≤ 0.03.
  - Reported: the same at P 0.25 and 1.0; and a null mock (no wave) at P = 0.5, which should give Δχ²_0 ≤ 0.1 (MUT-0).

## 8. Hand estimates (made before any code; no weight)
- **Bound.** f_DE = ρ_DE/ρ_tot ≈ 0.37 (z 0.5), 0.2 (z 1) and 0.05 (z 2.33) at the CFG689 best fit, and δH/H ≈ f_DE ε sin(…).
  D_H/r_d errors are 1–2.5%. So:
  - ε_95 ≈ 0.03–0.1 at periods short enough to put opposite phases on the z ≤ 1 points;
  - ε_95 ≈ 0.2–0.4 at P ≳ 2, where the wave looks like a smooth tilt, about as wide as CFG689's own band (±0.13 at z 1);
  - branch N: long periods unbounded, or close to it.
- **Sketch.** ρ_DE(0.5) = 4 ρ_DE(0), so H(0.5) rises by about 44% at fixed present-day parameters. The LRG1 D_H/r_d error is 1.2%,
  so Δχ² ≳ 10³.
- **Galaxy side.** Point errors are 0.1–0.4 dex, against an allowed wave of ≲ 0.05 dex at z ≤ 2.33. So: no.

## 9. Compute, outputs, wording
- **Compute.** One core (OMP_NUM_THREADS=1, nice 10), one process at a time, under 1 GB. Wall cap 4 h for the main run; if it is
  exceeded, the run stops and an amendment is committed before any rerun.
- **Outputs.**
  - cfg956_a0z_wave.py, modes K / MUTATE / MAIN → cfg956_K.{out,json}, cfg956_MUTATE.{out,json}, cfg956.{out,json};
  - cfg956_figure.py → cfg956_wave_bound.png;
  - README.md.
- **Wording.**
  - κ = ½ FITTED; footings never pooled.
  - A constant ρ_DE is ΛCDM's background, so no outcome here favours the framework over ΛCDM.
  - Not a closed theory.
  - A bound on a wave is not evidence for a wave.
