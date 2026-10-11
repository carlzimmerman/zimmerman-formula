# CFG621 FROZEN CRITERIA A: noise floor of the lensing-peak estimator on isolated halos (merger stopwatch v3, stage A)

Date: 2026-10-10. Written and committed ALONE, before any code of this lane has run and before any number of this lane exists.
Nothing below may be edited after this commit; later changes go in dated disclosures in the README. Stage B (the merger
criteria) is frozen in a separate file, committed alone after the stage-A results and before any merger run.

κ = ½ is fitted. The cold energy's mass is still required (its amount is an input). No dark-matter particle is added. The
theory is not closed. Yardsticks are raw data only (no ΛCDM halo, no MOND force law). Nothing here will be phrased as "the
data favour the framework".

## 0. Why stage A exists

CFG599 (criteria 8a10775bd, results ed2987307) is VOID as frozen: control C4(b) failed on the isolated main at α = 1
(lensing–galaxy 18.17 kpc against a 15 kpc tolerance). Its diagnosis (README D-2, `cfg599_c4_diag.py`) found one epoch of 61
over 15 kpc, the same failure at α = 0, and a flat-cored central lensing map whose 50-kpc shrinking-circle peak moves with
particle shot noise. The 15 kpc tolerance was set by hand, not from the estimator's measured noise. CFG599 D-3 also found that
its merger-side lensing-stability rule (spread ≤ max(20 kpc, 0.1 d_SG)) disagreed with C4's 15 kpc.

Stage A measures the estimator's noise on ISOLATED halos only and fixes, from that measurement, the C4 tolerance and the
merger-side stability rule (made identical). No merger simulation is run in stage A.

## 1. Setup (CFG599 unchanged except the estimator)

The model, grid, hydro, gravity, progenitors (main M200 = 1.5e15, sub 1.5e14 M☉ with its cool-core cloud, f_cc = 0.15,
a_cc = 50 kpc), case L cold energy, settling dynamics (rule 2S drift + FIX-2 OU), particle numbers (stars 160,000 / 100,000;
settled cold 200,000 / 100,000; cloud 40,000), projections (12.5-kpc pixels, mass-conserving bilinear gas projection, CIC
particles) and the 0.01-Gyr diagnostic cadence are CFG599's (FROZEN_CRITERIA.md 8a10775bd §2–§3, code `cfg599_lib.py`,
`cfg599_sim.py`, imported read-only). The isolated sub's cloud drag uses η = 1 (as CFG599's C4(b)).

## 2. The declared estimator (one estimator, all three positions)

E-1 The shrinking circle of CFG599 O-2 with R0 = 300 kpc and **R_min = 75 kpc** (shrink factor 0.85, iterate at R_min to
    |Δcentre| < 0.1 kpc, at most 200 iterations), used for the galaxy (star map, started at the median of the progenitor's star
    particles), the gas (the progenitor's gas map, started at its mass-weighted centroid within 600 kpc of the galaxy position)
    and the lensing (Σ_tot, started at the galaxy position). The smoothed-map alternative is NOT used.
E-2 Lensing convergence variants for the spread (largest distance of a variant peak from the primary peak):
    (R0, R_min) = (300, 60), (300, 90), (200, 75), (400, 75).

## 3. Runs (isolated halos only)

Isolated main and isolated sub (with its cloud), α ∈ {0, 1}, footings a₀ = 9.3603e-11 and 1.1312e-10 m s⁻², each evolved
0.6 Gyr from the exactly centred equilibrium start, diagnostics every 0.01 Gyr (61 epochs, t = 0 included).
N_rep = 6 realisations per configuration: seeds {599, 621, 622, 623, 624, 625} (599 is CFG599's realisation). 8 configurations
× 6 seeds = 48 runs.

## 4. Measured quantities and the frozen definitions

Per epoch of every run: d_L = |x_lens − x_gal| (lensing–galaxy), d_G = |x_gas − x_gal| (gas–galaxy), the lensing spread s
(E-2), the galaxy offset from the true centre, M(<300 kpc) of Σ_tot about the galaxy.

T-1 P95_L = the 95th percentile of d_L over ALL epochs of ALL 48 runs pooled (both halos, both α, both footings; pooling the
    footings here concerns only the estimator's noise, no physics is pooled). P95_G likewise for d_G.
T-2 **C4 lensing tolerance T_L = 3 × P95_L; C4 gas tolerance T_G = 3 × P95_G.**
T-3 **The merger-side lensing-stability rule is identical: the lensing peak is STABLE at an epoch iff s ≤ T_L** (CFG599's
    max(20 kpc, 0.1 d_SG) is dropped).
T-4 The C4(b) control of stage B is: in EVERY epoch of EVERY one of the 48 stage-A runs, d_L ≤ T_L and d_G ≤ T_G, and in every
    run |M(<300, t = 0.6) / M(<300, 0) − 1| ≤ 10%. (C4(a), the t = 0 estimator check within 3 kpc of the true centre, is re-run
    in stage B with E-1.)

## 5. Reported, not gating, in stage A (they inform stage B, which is frozen with them in view)

R-1 P95 and maximum of d_L, d_G and s per configuration (halo × α × footing), and the α = 1 minus α = 0 shift of the median d_L
    per halo (a settling-induced drift would appear as a systematic shift).
R-2 P95 of s pooled, and the fraction of isolated epochs that would be UNSTABLE under T-3 (should be ≲ 1%).
R-3 The estimator noise in Bullet-score units: N_B = P95_L(sub only) / (194 kpc × 0.125). Pre-declared consequence for stage B:
    if N_B > 1 (the sub's estimator noise exceeds one σ_f of the Bullet statistic), the Bullet score is NON-DIAGNOSTIC and every
    stage-B verdict will be VOID on that ground.
R-4 The CFG599 failing realisation (seed 599, main, α = 1, canonical) re-measured with E-1.

## 6. Compute and housekeeping

nice -n 10, ≤ 4 processes of 1 thread, ≤ 2 GB each. Scripts, `.out`, results JSON and README in this folder only; README
numbers come from the JSON. CFG599 and CFG597 are used read-only. Commit specific paths only; no push; never rewrite history.
