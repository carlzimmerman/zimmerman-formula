# CFG344 FROZEN CRITERIA: post-reionisation cold accretion onto reionisation-fossil satellites

Written and committed before any score. κ = ½ is FITTED and fixed. Both footings (a₀ = 9.36e-11, 1.13e-10 m s⁻²). No DM particle; the cold component's mass is required. No downloads; no knob scans. z_f, z_re, z_inf are fixed a priori, with brackets reported one at a time.

## The idea
CFG343 showed the atomic-cooling floor M_cool(z_f) gives median R ≈ 700 for the MW ultra-faints. That is 6-8× short of CFG317's R_need (log R_need 3.65-3.74).

After reionisation, photoheating stops gas accretion onto systems below the filtering mass. The collisionless cold component keeps accreting by gravity until the satellite falls into its host. The baryons stay frozen while the cold mass grows from M_cool(z_f) to M(z_inf).

## Formula (declared)
- **Start:** M_cool(z_f) is CFG343's Barkana & Loeb 2001 eq. 26, with T_vir = 1e4 K and μ = 1.22, imported from CFG343's script.
- **Growth:** the median mass accretion history of Correa, Wyithe, Schaye & Duffy 2015 (MNRAS 450, 1521; EPS-derived), transcribed from memory and flagged PROVISIONAL:
  - M(z) = M₀ (1+z)^α e^{βz};
  - β = −f(M₀);
  - α = [1.686 (2/π)^{1/2} (dD/dz)|₀ + 1] f(M₀);
  - f(M₀) = [S(M₀/q) − S(M₀)]^{−1/2};
  - q = 4.137 z̃^{−0.9476}, with z̃ = −0.0064 (log M₀)² + 0.0237 log M₀ + 1.8837.
- **Inputs:** S = σ²(M) from colossus (planck18; Eisenstein & Hu 1998 transfer; local package, no download). D(z) is the linear growth factor.
- **Inversion:** M₀ is solved so that M(z_f) = M_cool(z_f). Then M_c = M(z_inf), so R_acc = f_b M(z_inf) / M_b (floored at R = 1).
- **What is B-native:** the linear growth D(z). CFG324 found B's large-scale growth equals ΛCDM's linear growth, because the switch is off on unbound modes.
- **ΛCDM-specific flags, disclosed:**
  - (F1) the small-scale power spectrum shape and σ₈ normalisation are taken as collisionless-CDM's;
  - (F2) Correa's q(z̃) coefficients are calibrated on ΛCDM N-body merger trees, which goes beyond pure linear growth plus collapse;
  - (F3) it is extrapolated to M₀ ~ 1e8-1e10 M☉ and z up to 10.
  - No halo profile or abundance matching enters.

## A-priori classification (CFG336's class split)
- **Reionisation fossil:** a satellite (MW UFD sample, including its 9 upper limits; the MW classical, M31 Collins+13 and M31 LVD samples) with M_V > −7.7. Only fossils get M_c = max(M_b/f_b, M(z_inf)).
- **Non-fossil:** all M_V ≤ −7.7 satellites, and **all LV field dwarfs**. These are gas-rich and star-forming (CFG317 B1), so they were not quenched. They keep R = 1, the CFG313 / CFG317 baseline.
  - CFG317's RESCORE already showed that the leaky-box R_ind moves no tile, so R = 1 is the primary choice; that result is cited, not re-run.
  - The number of LV field dwarfs with M_V > −7.7 is reported.
- **Epochs:**
  - z_f = 8 (bracket 6, 10);
  - z_inf = 2 (bracket 1, 3), the a-priori bracket because no infall-time column is on disk (LVD has none; CFG327's orbits are not infall times);
  - z_re = 7 (bracket 6, 8).

## Scoring
- CFG317's script is exec'd read-only up to its scans. That brings in CFG313's harness and CFG317's hooks. Only the per-object M_c hook is replaced, keyed by committed M★ exactly as CFG317's RESCORE does.
- Per-object R is used, so this is not a population-median approximation. Rule S, profiles V1 (NFW) and V2 (SIS), both footings.
- **Grade on the OFFSET** (CFG343's lesson). Define e_law = s_UFD(R=1) / z_UFD(R=1) from the R = 1 run, per footing and profile. The threshold 2 e_law is fixed at its R = 1 value (≈ 0.17 dex canonical).

## Decision (primary: z_f = 8, z_inf = 2)
- **RESOLVES:** |s_UFD| ≤ 2 e_law(R=1) on both footings and both profiles, AND MW classical, M31 Collins, M31 LVD and LV field all have |z| < 2 on both footings and both profiles.
- **PARTIAL:** s_UFD ≤ ½ s_UFD(R=1) (that is, offset halved, ≤ +0.162 canonical / ≤ +0.152 alt for V1), with s_UFD ≥ −2 e_law, on both footings and both profiles, with the other four rows within |z| < 2.
- **NOT:** otherwise.
- **Reported:** the brackets (z_f 6 / 10; z_inf 1 / 3), R_acc (median and range), the factor versus R_need, SLUGGS / SPARC rows (unchanged by construction).

## Reionisation-cap consistency check (reported, not decisive)
- The filtering mass is taken as M_F ≈ 1e9 M☉ (Gnedin 2000, PROVISIONAL from memory).
- Count the fossils with M(z_re) > M_F. They would not have quenched, so the idea would be inconsistent for them. This is reported for z_re = 6, 7, 8.

## Controls
- **C1:** with R = 1, CFG317's baseline (numbers.NEED[...]["s"][0], ["z"][0]) is reproduced to 1e-6 dex for P1, P2a-P2d, both footings and both profiles.
- **C2:** at the reference point, the accretion code reproduces the published mean accretion rate of a 1e12 M☉ halo at z = 0 within a factor of 1.5. The reference is Fakhouri, Ma & Boylan-Kolchin 2010: 46.1 M☉/yr (mean), PROVISIONAL from memory.
- **C3:** the inversion holds, M(z_f) = M_cool to 1e-8 relative, and M(z) is monotone between z_f and z_inf.
- **MUTATE** (CFG344_MUTATE=1, separate `_MUTATE` outputs): z_inf = z_f, so there is no post-reionisation growth. The verdict must be NOT, and the V1 canonical UFD offset must be within 0.05 dex of CFG343's +0.322.

## Lean
Certify the decisive offset inequalities (|s| vs 2 e_law; s vs ½ s₀; |z| vs 2 for the other rows) at the primary point, using rationals rounded outward from the results JSON (Mathlib, no sorry).
