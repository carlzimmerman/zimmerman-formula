# CFG649: the CMB-safety gate. Primary CMB: SWITCH-OFF CONFIRMED (no loophole). CMB lensing, candidate B canonical: ΔA_lens = +0.013 (Planck 8–400 weights), CONDITIONAL — the box covers ~10% of the lensing kernel

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (0d6f7f883). Date: 2026-10-12.
- **Script:** `cfg649_cmb_safety.py` (one process, ~3 s, < 0.5 GB). It writes `cfg649_<tag>.out/json`; with `CFG649_MUTATE=1`, it writes `cfg649_<tag>_MUTATE.out/json`. Both runs here exit cleanly and every frozen check passes (MUTATE after one disclosed engineering fix, see below).
- **Inputs (read only):** CFG596's 1024³ L100 runs, P0 (S0) and P1 (candidate B, RES canonical, same realisation), JSON snapshots at z_i = 49, 1, 0.7548, 0.5, 0.2562 and 0. The Planck 2018 VIII MV band edges and fractional band errors come from the committed XR26 table. Nothing was downloaded.
- **Settings:** κ = ½ FITTED. Canonical footing only; the alt footing (P2) is PENDING. Cold energy's mass is required and no particle species is added. Not "theory closed". No ΛCDM fit, halofit, HMcode, CLASS or CAMB spectrum, and no standard-MOND curve, enters any verdict. Everything is framework vs the same-pipeline S0.

## Part A. Primary CMB: SWITCH-OFF CONFIRMED

At z ≈ 1100, cold energy in candidate B is ordinary cold collisionless matter (Ω_c/Ω_b = 5.364, counted as matter in the background), and a₀ and settling do nothing. Four rules guarantee this:
- **R-A1 (engine L490, L508, L715, L719).** The only extra source is `e × catch`. Catchments are turnaround balls around RESOLVED peaks: nonlinear δ ≥ 3(τ − ε), and enclosed mean 1 + δ ≥ Δ_ta(z) ≈ 5.55 on R ≥ r_min. With no catchment the source is identically zero, and the potential equals S0's line for line (L791).
- **R-A2 (L763).** The source is zero-sum per catchment component, so mean density and background are untouched (CFG647: |src_sum|/e_sum ≤ 2.7e-11).
- **R-A3 (L685).** a₀ enters only through ν(y) inside that gated path. The FLAT branch is constant. The DE-tracking branch would make a₀ smaller at high z, and it is gated the same way.
- **R-A4.** The settling sink to dark energy (CFG542 Q ∝ 1_B 1_C) is zero before turnaround. CFG630 puts the total at 0.98–1.10e-6 of ρ_DE0 since z = 1, and at most 5.9e-6 over all its brackets.

| check | result |
|---|---|
| A1, data at z_i = 49 (P1 vs P0) | n_catch = 1 (background only), e_sum = 0, P_grav and particle P identical (max deviation 0) → **PASS** |
| A2, engine scan for any source path outside the catchments | none found; a₀ used only at L479 (census-edge radius x_supply, evaluated only for resolved peaks) and L685 (ν) → **PASS** |
| A3, ESTIMATE of linear turnaround peaks at z = 1100 over the whole last-scattering ball, R = 1e-3–10 Mpc/h | σ_lin,max = 0.014 (EH continued; no radiation, so growth is overestimated); ν ≥ 76; log10 N = **−1232** → **PASS** |
| A3 context, in-box switch-on estimate | z_on ≈ 10 for the smallest resolved ball (R_L = 1.38 Mpc/h) |

**Loophole search.** No path acts at high z. One gap in the record should be stated plainly: the 1024³ run stored no diagnostics between z_i and z = 1. The in-box switch-on epoch is therefore estimated (z ≈ 10), not measured. By z = 1, P1 already has 786 catchments and σ8_grav 0.555 vs 0.522. A real universe without the PM resolution floor switches on earlier, with the first turnaround of small structures at z of a few tens. That is still more than 1000 below recombination.

**What is inherited.** The primary-CMB physics of the switch-off era is GR-linear, and the framework adopts it there. That covers the EH IC spectrum, the flat w = −1 background and massless neutrinos (all flagged, as in CFG596). No primary-CMB spectrum is computed or fitted here.

## Part B. CMB lensing from the framework's own gravitating P(k, z)

**Method.**
- The ratio is R(k, z) = P_grav,F/P_grav,S0 at the five late snapshots, interpolated linearly in a; R ≡ 1 is measured at z_i. The box support is k = 0.080–7.98 h/Mpc.
- The projection is Limber to C_L^φφ in the engine background, with χ_* = 9405 Mpc/h, z = 1e-3–50 and integer L from 8 to 2048.
- The statistic is ΔA = A_F/A_S0 − 1, using Planck 2018 MV band weights 1/σ_A,b² (the XR26/CFG324 estimator, with S0 in place of the fiducial).
- The 12-member bracket combines two S0 weighting bases, three redshift rules above z = 1 (Z-a R = 1; Z-b linear in a down to R = 1 at z_i; Z-c held), and two large-scale rules below k_lo (K-a R = 1; K-b held at the lowest bins).

**Coverage (base-1, band-weighted).**

| band set | z ≤ 1 and k inside the box | z ≤ 1, any k | k inside the box, any z |
|---|---|---|---|
| Planck 8–400 | 0.103 | 0.27 | 0.15 |
| Planck 8–2048 | 0.108 | 0.26 | 0.20 |
| ACT 40–763 | 0.156 | 0.19 | 0.61 |

The boxes directly constrain only ~10–16% of the lensing signal. The rest is set by the declared extrapolation.

**The own boost on the gravitating field.** At k = 0.3/0.5/1, R(z = 1) is 1.20/1.32/1.42 and R(z = 0) is 1.25/1.34/1.31. At k = 0.1 it is 1.05–1.065.

**Results (gravitating field = verdict).**

| member | ΔA 8–400 | ΔA 8–2048 | ΔA ACT-range | Δχ²_rel 8–400 |
|---|---|---|---|---|
| **canonical (base-1, Z-b, K-a)** | **+0.0133** | **+0.0181** | **+0.0527** | 0.56 |
| base-1 Z-a K-a (lowest base-1) | +0.0112 | +0.0136 | +0.0312 | 0.33 |
| base-1 Z-b K-b | +0.0539 | +0.0557 | +0.0667 | 4.76 |
| base-1 Z-c K-b (highest) | +0.0794 | +0.0823 | +0.0972 | 10.30 |
| full bracket range | [+0.0088, +0.0794] | [+0.0101, +0.0823] | [+0.0204, +0.0972] | |
| 2σ (published σ, context) | 0.056 | 0.052 | 0.046 | |
| **label** | **CONDITIONAL** | CONDITIONAL | UNSAFE (context) | |

- Per-band A_b on 8–400 rises from 1.001 at L ≈ 24 to 1.053 at L ≈ 378.
- The full 12-member table is in `cfg649_cfg596_P1_canonical.out`.
- Context only, the particle field: ΔA = +0.0017 (8–400), with the whole bracket ≤ +0.0064 (SAFE).

**Reading.**
- On the frozen primary statistic, candidate B's canonical CMB-lensing shift is +1.3%, well inside 2σ (0.056). The verdict is still **CONDITIONAL**, not SAFE. If the large-scale boost (R ≈ 1.05 at the box's lowest k) persists below k = 0.08 AND the boost holds at z > 1, ΔA reaches +0.054 to +0.079.
- On ACT-range L weighting the canonical value is +0.053, beyond ACT's 2σ (0.046). Two caveats apply. That statistic uses uniform per-L weights, because the ACT DR6 bandpowers are not on disk. Uniform weights overweight high L, where the boost is largest.
- The lensing excess comes from the same 19–42% gravitating-field boost at k 0.3–1 that CFG596 excluded on KiDS. Lensing can tolerate it only because the boxes cover ~10% of the kernel and the high-L weights are small.
- **The verdict also depends on the open lensing-vs-stability fork.** If the phantom does not lens (light sees only the matter field), the shift is the particle-field number, +0.002: SAFE.
- This verdict covers the canonical footing of candidate B as run in CFG596. It does not cover the fixes under test.

**MUTATE (`cfg649_cfg596_P1_canonical_MUTATE.out`).**
- M1 F ≡ S0: ΔA = 0 exactly.
- M2a, R ≡ 1.10: ΔA = 0.100 (deviation 1e-16).
- M2b, R = 1.10 on the box region only: ΔA = 0.10 × f_cov (deviation 2e-16).
- M2c, CFG596's z = 0 boost injected for z ≤ 1: +0.01008 vs +0.01008 from an independent midpoint-in-χ quadrature (max relative 1.6e-4).
- **MUTATE bites.**

**Disclosed engineering fix (post first run).** The first MUTATE run FAILED M2c: relative error 7.9e-3 against the 1e-3 tolerance (8–400: +0.01011 vs +0.01008). The z grid put a single node at z = 1, so the trapezoid rule smeared rule Z-a's step there. z = 1 is now a doubled node (a zero-width interval, so the step is integrated exactly) on a denser grid (300 + 400 nodes). No statistic, rule or tolerance changed. The canonical numbers were unchanged to 4 decimals (+0.0133 in both runs). The bracket-range ends moved by ≤ 3e-4.

## Data: what is on disk and what would be needed

- **On disk:** Planck 2018 VIII MV band edges and fractional errors (8–400, 8–2048), typed in the committed `real_research/cross_thread_review_2026_09_26/XR26_cmb.py`. These supply the weights and σ_A. Their FFP10 fiducial column is not used.
- **NOT on disk, not downloaded (needs the owner's approval):**
  - Planck PR4 lensing bandpowers and covariance (Carron, Mirmelstein & Lewis 2022; the public `planck_PR4_lensing` likelihood package on GitHub, of order a few MB);
  - ACT DR6 lensing bandpowers and covariance (Madhavacheril / Qu et al. 2024; the `act_dr6_lenslike` package plus its data tarball from NASA LAMBDA, of order 10–100 MB).
  - Sizes are approximate and unverified. With them, the ACT-range statistic would use the real band weights, and Δχ² would use the full covariance.
- **Published amplitudes used only as labelled context:** σ = 0.028 (Planck 8–400; PR4 1.011 ± 0.028) and σ = 0.023 (ACT DR6 1.013 ± 0.023). The central values are not used.

## CMB-SAFETY CHECKLIST (every settling-fix lane must pass it)

Applies to CFG636 (capped source), CFG640 (two-phase), CFG644 (neighbour edge), CFG646 (gas expulsion), CFG647 (per-host supply), CFG648 (splashback), and any later rule change.

1. **Primary CMB, switch-off.**
   - (a) The lane's PM output must carry a z_i snapshot with n_catch ≤ 1, e_sum = 0 and P_grav identical to its S0 (A1, checked automatically by the command below).
   - (b) The lane's README must state, with engine line numbers, that its new rule adds or moves source ONLY inside catchments of resolved turnaround peaks, and keeps the per-component zero-sum. A rule that sources outside catchments, or that reads a₀, ρ_DE or H(z) outside the gated path, is a LOOPHOLE and must be re-argued. A rule that changes the background (a non-zero net source, or energy to dark energy beyond the CFG630 order of 1e-6) must quantify it.
   - (c) Pass the engine path with `--engine` so that A2 scans the lane's own code. If A2 reports NOT FOUND for a renamed line, the lane states the equivalent line by hand.
2. **CMB lensing.** Run this script on the lane's own PM output against its same-realisation S0. The script asserts the same seed, N and L. Each run needs a z_i snapshot and snapshots with a ≥ 0.5 including a = 0.5. Report the canonical ΔA (8–400) and the 12-member bracket with the label: SAFE, CONDITIONAL or UNSAFE at 2σ = 0.056.
   ```
   cd campaign_fresh_gravity/CFG649_cmb_safety
   nice -n 10 python3 cfg649_cmb_safety.py --f <LANE_RUN>.json --s0 <MATCHED_S0>.json --tag <lane_tag> --engine <path/to/lane_engine.py>
   CFG649_MUTATE=1 nice -n 10 python3 cfg649_cmb_safety.py --f <LANE_RUN>.json --s0 <MATCHED_S0>.json --tag <lane_tag> --engine <path/to/lane_engine.py>
   ```
   - For a 1024³ L100 run with seed 359 and NSEED 1024, the matched S0 is `_external_data/cfg596_work/P0/cfg596_S0_canonical_N1024_L100_ns1024_lean.json`.
   - For other boxes, use their own S0 run (for example CFG530's S0 L100 N512). `--khi` overrides the support top (default πN/(4L)).
3. **Interpretation rule.** A fix that lowers the gravitating-field boost at k 0.3–1 (the KiDS exclusion) should also lower ΔA. A fix that moves settled mass outward, to larger scales or to earlier times, can RAISE ΔA, because the K-b and Z-b/Z-c members grow. Report both numbers side by side.

κ = ½ fitted; cold energy mass required; not theory closed.
