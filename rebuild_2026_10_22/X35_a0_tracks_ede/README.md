# X35_a0_tracks_ede: does a₀ tracking an early dark energy switch the law on at recombination?

**The owner's idea.** a₀(z) = κ c √(G ρ_DE(z)) tracks the dark-energy density. If ρ_DE contains an early dark energy (EDE),
a₀ at z ≈ 1100 is thousands of times today's, so the recombination plasma sits deep in the law's regime. Could that supply
the steady potential wells the acoustic peaks need, without a separate cold component?

κ = ½ FITTED. Footings 9.3603e-11 / 1.1312e-10 m/s², never pooled. No dark-matter particle. EDE parameters are literature
values (PROVISIONAL, transcribed from memory of the papers, no download), never fitted. Not "theory closed". Nothing here
says the data favour the framework.

Files: `FROZEN_CRITERIA.md` + `ASSUMPTION_LEDGER.md` (02848d0330, committed alone); `AMENDMENT_A1.md` (post-first-run,
before grading: φ′ from the 00 equation, drag-redshift anchor, K1 sign in code); `x35_ede_tracking.py`;
`x35_results.json`, `x35_ede_tracking.out`; MUTATE twin `x35_results_MUTATE.json`, `x35_ede_tracking_MUTATE.out`.
Run: `PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x35_ede_tracking.py` (≈ 15 s, one thread).

## Verdict (frozen rule 5): **UNDECIDED**

The frozen rules give UNDECIDED. No reading reaches "supplies steady wells":

- **Magnitude is not the problem.** MAG_OK holds. Every literature EDE point puts a₀(1100) at 1,147–7,565 × today, and the
  plasma's x drops from ≈ 10–12 to ≈ 10⁻³.
- **The covariant theory gives nothing (D1, NULL).** v3s's extra potential is the weight of khronon charge ρ_τ. With no
  background charge (no separate cold component), ρ_τ ≡ 0 is preserved exactly, and the hold equation then forces Ξ ≡ 0.
  So φ is the GR potential of baryons, photons and neutrinos, **for every a₀**. A huge a₀ switches nothing on.
- **With the Blanchet–Skordis dust (D2).** That dust is a separate cold component with a fitted abundance. In the EDE
  regime (x → 0) its linear kernel is a₀-free: s = a²μ_K²/(k² + a²μ_K²) + O(x). EDE only makes the record's linear
  (f₀ = 0) analysis valid at early times; that analysis does not contain a₀.
- **The static AQUAL reading (the "naive" instantaneous phantom) is why the rule returns UNDECIDED, not OSCILLATES.**
  - Linearised about the total rms field, the boost is G_eff/G ≈ 11–29. The extra potential is then in phase with the
    wave, so its steady fraction is zero.
  - That boost also makes the photon–baryon fluid Jeans-unstable for k < k_J,eff = 0.024–0.039 Mpc⁻¹, the first-peak
    scales. The plasma does not oscillate there.
  - In the single-mode exact 1-D treatment at the physical amplitude, k = 0.09 (third-peak scale) crosses zero on the
    canonical footing (F = 0.019). On the alt footing it is self-trapped (F = 0.64, no zero crossing). This is the
    marginal case β_eff = 0.755 against the 0.745 barrier. K4 records it as FAIL.
  - Neither branch is a CDM-like well. The trapped offset is the plasma's own clump, with its sign set by the initial
    perturbation; it is not an independent pressureless component.

Bottom line, in words: in v3s the EDE-tracking a₀ cannot supply wells without a separate cold component (D1). The naive
static reading boosts the baryon–photon self-gravity. That either oscillates with the wave or destabilises it, and in
both cases it breaks the first-peak scales.

## Step 0 (stop rule, all PASS)

| id | result | line |
|---|---|---|
| S0-1 record "x ≈ 11–14 at z 1100" (an audit estimate, no script) | x = k_phys\|Ψ\|c²/a₀ at k = 0.05 Mpc⁻¹, ΛCDM-like fields: **11.22 / 9.28** (\|Ψ\| = 6.56e-6) | ×2 band; order of magnitude only |
| S0-2 M-DEC R(0,1,2,3) | 1.0000, 0.9889, 0.8739, 0.7750 | ±0.002 |
| S0-3 CFG689 sqrtX median, z* 2.33 | 0.9094 (BAO+SN), 0.9498 (BAO) | read back |
| S0-4 r_d of the ruler cosmology | 147.06 Mpc (z_drag 1059.9) vs 147.07 | 1 % |

DESI M-DEC gives a₀(1100)/a₀(0) = 0.0206, so x(k 0.05) = 545 / 451. The law is more inert than with Λ, which reproduces the
record's statement. Without EDE, x at z 1100 over k 0.01–0.3 is 5.9–12.4 (canonical) for the ΛCDM-like fields and up to
6.8 for the no-cold fields (whose Ψ has nodes).

## Step 1: a₀(z) magnitude (M-LCDM background; z_c at the literature value)

| literature point (PROVISIONAL) | dilution | a₀/a₀(0): z 0 | z 2.33 | z 300 | z 1100 | z_c | z ≥ 1e5 (incl. BBN) | x_max(1100) can/alt | x_rms(1100) can/alt |
|---|---|---|---|---|---|---|---|---|---|
| L1 Smith+20 f 0.122, z_c 3648 | n = 3 (a^−4.5) | 1.0000000 | 1.000132 | 410 | 7565 | 7.9e4 | 1.12e5 | 1.55e-3 / 1.28e-3 | 2.54e-3 / 2.10e-3 |
| L1 | n = ∞ (a^−6) | 1.0000000 | 1.000000 | 63 | 3086 | 7.9e4 | 1.12e5 | 3.86e-3 / 3.20e-3 | 6.37e-3 / 5.27e-3 |
| L2 Poulin+19 f 0.08, z_c 5000 | n = 3 | 1.0000000 | 1.000061 | 279 | 5166 | 1.1e5 | 1.56e5 | 2.30e-3 / 1.91e-3 | 3.80e-3 / 3.14e-3 |
| L2 | n = ∞ | 1.0000000 | 1.000000 | 34 | 1661 | 1.1e5 | 1.56e5 | 7.27e-3 / 6.02e-3 | 1.20e-2 / 9.95e-3 |
| L3 Hill+20 bound f 0.087, z_c 3500 | n = 3 | 1.0000000 | 1.000094 | 346 | 6391 | 6.1e4 | 8.65e4 | 1.87e-3 / 1.54e-3 | 3.07e-3 / 2.54e-3 |
| L3 | n = ∞ | 1.0000000 | 1.000000 | 55 | 2690 | 6.1e4 | 8.65e4 | 4.48e-3 / 3.71e-3 | 7.40e-3 / 6.13e-3 |
| L4a f 0.10, z_c 3000 | n = 3 | 1.0000000 | 1.000128 | 404 | 7440 | 5.1e4 | 7.14e4 | 1.60e-3 / 1.32e-3 | 2.63e-3 / 2.17e-3 |
| L4a | n = ∞ | 1.0000000 | 1.000000 | 72 | 3522 | 5.1e4 | 7.14e4 | 3.41e-3 / 2.82e-3 | 5.63e-3 / 4.66e-3 |
| L4b f 0.10, z_c 5000 | n = 3 | 1.0000000 | 1.000078 | 316 | 5839 | 1.2e5 | 1.76e5 | 2.02e-3 / 1.67e-3 | 3.32e-3 / 2.75e-3 |
| L4b | n = ∞ | 1.0000000 | 1.000000 | 38 | 1878 | 1.2e5 | 1.76e5 | 6.39e-3 / 5.29e-3 | 1.06e-2 / 8.74e-3 |

- The no-cold background (M-NATIVE) gives a₀(1100) of 1,147–4,957 × today, with x_max = 1.1e-3 to 5.8e-3.
- For every point, x_max < 1 at every saved epoch from z = 1e5 down to z = 300 (the window spans the whole grid).
- Note: n = 3 dilutes as a^−4.5. The brief's a⁻⁶ is the n → ∞ case; both are run.
- **Late time.**
  - EDE changes today's a₀ by at most 5.9e-7, and moves a₀ at z 2.33 directly by at most 1.3e-4 (K5).
  - EDE does move CFG689 **indirectly**, through its ruler. L1 lowers r_d by 4.0 % (ratio 0.960). Holding CFG689's ω_m,
    a flat-Λ ESTIMATE then moves the native sqrtX from 1.00 to **1.49 at z 2.33** and to 1.11 at z 1.0.
  - So CFG689's native a₀(z) band holds only for its no-EDE ruler. EDE is not neutral for the late-time a₀(z) record.

## Step 2: the derivation

**Covariant v3s (BS24 PN system, V3_FULL_PICTURE §2):**

    ∂_t ρ_τ + ∇·(ρ_τ v_τ) = 0          (homogeneous in ρ_τ ⇒ ρ_τ ≡ 0 is exact)
    ∇·(J_Y ∇Ξ) + μ_K² Ξ = −4πG ρ_τ = 0,  J_Y = −1/(1+x)
    ⇒ ∫ Ξ[∇·(J_Y∇Ξ) + μ_K²Ξ] = ∫ [ |∇Ξ|²/(1+x) + μ_K² Ξ² ] = 0  ⇒  Ξ ≡ 0
    ⇒ ∇²φ = 4πG(δρ_b + δρ_γ + δρ_ν):  GR, a₀-independent.

These are checked as K1 (symbolic) and K1b (a nonlinear 1-D solve from a non-zero start returns max|Ξ| = 4.9e-29).

With background dust (a separate cold component), the self-gravity kernel is

    s(k; f) = (a²μ_K² − f k²) / ((1 − f) k² + a²μ_K²),   f = x/(1+x)
    s = a²μ_K²/(k² + a²μ_K²) − k⁴ x/(k² + a²μ_K²)² + O(x²).

At z 1100 in the EDE regime, s = 8e-5 to 8e-9 for μ_K ≤ 0.1 Mpc⁻¹, and 0.45 to 9e-4 at the BS cap of 10 Mpc⁻¹ (k 0.01–0.3).

**Static AQUAL reading (exact 1-D plane wave):** μ(|g|/a₀) g = g_N gives g = g_N ν(|g_N|/a₀), which is odd in g_N (K3).

**Φ driving.** The tight-coupled plasma obeys

    δ_γ'' + k² c_s² δ_γ = −(4/3) k² [Φ_N + Φ_extra],

where the extra term differs between the two cases:
- CDM: Φ_extra = Φ_c ≈ const over a period. This is zero-frequency driving that shifts the zero point (steady fraction F = 1).
- Law: Φ_extra = Φ_law(δ_γ), an odd instantaneous function of the plasma's own δ. It is in phase or antiphase with the
  wave: it changes the restoring force, not the zero point.

The plasma is taken at its physical amplitude (no-cold fields + L1 n = 3, z 1100):

| k (Mpc⁻¹) | boost ν̄ (can/alt) | β_eff = β·ν̄ (can/alt) | F_law (can/alt) | zero crossing (can/alt) |
|---|---|---|---|---|
| 0.02 | 47 / 52 | 6.2 / 6.8 | 4.0e-3 / 3.8e-3 | no / no (Jeans-unstable) |
| 0.05 | 78 / 86 | 1.64 / 1.80 | 1.4e-2 / 1.2e-2 | no / no |
| 0.09 | 107 / 117 | 0.687 / 0.755 | 0.019 / **0.64** | yes / **no (trapped)** |
| 0.2 | 163 / 179 | 0.21 / 0.23 | 1.6e-3 / 1.0e-2 | yes / yes |

For k ≤ 0.05 the small F is not a symmetric oscillation: β_eff > 1 there, so the mode never crosses zero.

**Mean-field (linearised about x_rms, deep: x_true² /(1+x_true) = x_N).** G_eff/G = 11.3–28.7 across L1–L4 and both
footings, which gives k_J,eff = 0.024–0.039 Mpc⁻¹ against GR's 0.0072.

## Step 3

Not run: Step 2 is not STEADY (frozen §3).

## Step 4 (reported)

- **BBN.** ρ_EDE/ρ_r at 1 MeV is 1e-25 to 7e-25 (n = 3), so it is negligible. a₀ at that epoch is 7e-6 to 1.7e-5 m/s²,
  irrelevant to nuclear physics, and the modes are super-horizon. Q6's literal K(Q) stiff partner is a₀-independent, so
  EDE does not change it.
- **Damping tail.**
  - Static reading: k_J,eff ≤ 0.039 Mpc⁻¹ stays below the damping range, but it removes oscillation at first-peak scales.
  - Covariant: the damping tail is that of the no-cold universe.
  - Literature EDE fits keep the damping tail by raising ω_c and n_s (PROVISIONAL). That compensation uses the cold component.
- **Sound horizon and H₀.** Rough H₀ ∝ 1/r_d at fixed θ*; for the no-cold rows it is cruder still, because D_A also changes.

  | background | r_d (Mpc) | rough H₀ |
  |---|---|---|
  | ruler (with cold) | 147.06 | 67.7 |
  | + L1 | 141.15 | 70.5 |
  | + L2 / L3 / L4a / L4b | 143.27 / 142.91 / 142.34 / 142.29 | 69.5–70.0 |
  | no cold | 200.90 | 49.6 |
  | no cold + L1 | 190.54 | 52.3 |
  | no cold + L2–L4 | 192.32–194.07 | 51.3–51.8 |

  Without a cold component, r_d is about 37 % too large, and EDE recovers only about 5 %.
- **Record lanes.** EDE tracking lifts X14/X18's hold-flux cap |KP| < a₀ by 34–7,565× between z 300 and 1100. That makes
  the record's linear (f₀ = 0) khronon analysis (M1, Q6) valid at early times, removing X18's CAP ambiguity. That analysis
  is a₀-free, so its growth deficit stands.

## Checks

- **Normal run: 11/12 PASS.** S0-1 to S0-4, K1, K1b, K2, K3, K5a, K5b and K6 pass.
- **K4 FAILS.** This is a physics outcome, not a code fault: F = 0.64 on the alt footing at k 0.09, the single-mode trapping
  above. The script exits 1.
- **MUTATE** (`X35_MUTATE=1`: EDE off, constant Φ in place of the law, planted charge): all four named checks FAIL as
  required (exit 1).
  - M-A: MAG_OK fails; x_max returns to 12.4 / 10.3.
  - M-B: a₀(1100)/a₀(0) = 1.
  - M-C: F = 1.00.
  - M-D: max|Ξ| = 0.112.
  - Caveat: M-C does not discriminate here, because the normal run's F_law is already ≥ 0.05 on the alt footing.

## Assumptions to keep in mind

- Ψ comes from a fluid ODE: no neutrino shear, no EDE perturbations, no Silk damping in Ψ. The estimator is order-of-magnitude.
- The deep-MOND perturbation theory is non-linear in the background gradient. The mean-field and single-mode readings
  bracket it; neither is a solution of the 3-D AQUAL problem.
- The EDE literature values are PROVISIONAL.
