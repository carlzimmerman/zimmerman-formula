# CFG659: does the settling field P leave any signature in ordinary matter or light? (frozen criteria)

Written 2026-10-13, before any CFG659 script or number. Committed alone. Reading lane on the Lean chat's one-action
construction (CFG694 action, CFG695 saturating W, CFG696 radiative attractor); no CFG690–699 file is edited.
κ = ½ FITTED; both footings (9.3603e-11 / 1.1312e-10), never pooled; the cold energy's mass is required; no particle species;
not "theory closed"; no ΛCDM or standard-MOND quantity is used as a yardstick in any verdict.

## The action read as written (CFG694 + CFG695)
L = −|∇Φ − 4πG P|²/8πG − ρ_b Φ − W(P) − (γ/2)|∇P|² + (I/2)|Ṗ|², with W the CFG695 saturating vacuum minus the critical
quadratic, γ = 2πG L*² (from CFG691's ℓ_γ = L*²/2r_M), c_P = √(γ/I) unfixed (CFG696).

## Derivations the script must carry (analytic, checked numerically where stated)
- D1. Coupling. Matter couples to P only through Φ. The longitudinal part of P gives δg = −4πG δP_L on all matter; the
  transverse part does not enter Φ. List every term of the action that contains an electromagnetic field (expected: none).
- D2. Wave spectrum: speed of longitudinal waves, any mass gap from W″ about the local background (deep, transition and
  saturated regimes), transverse-mode mass.
- D3. Energy flux of a longitudinal P wave and its δg amplitude.
- D4. Quadrupole P radiation from a binary in the linear (screened-core) regime, as a ratio to the measured orbital decay
  budget.
- D5. Absorption of a P wave by baryons (dispersion relation with responsive baryons).

## Parameter window (frozen)
L* ∈ {5.75, 100, 1000} pc (CFG691 window: 5.75 pc lower bound, ≥ 1000 pc grid edge). c_P ∈ {5e-3, 1.5e-2, 0.1, 1} c.
The floor 5e-3 c is a consistency condition, not a fit: stars in cluster galaxies move at ~1500 km/s, and a field slower than
its sources cannot follow them statically (Cherenkov). Every channel verdict uses the WORST corner (largest signal) of this
window; the c_P each channel would exclude is reported separately.

## Settling energy (framework-native only)
- Per halo: energy released by P settling = E_code(R/ℓ_γ) × M_b V_f², where E_code is the static field energy of CFG696's
  functional (zero field minus static profile) integrated to R/ℓ_γ, and V_f⁴ = G M_b a₀. Control K1: E_code(200) must match
  CFG696's released energy for the zero start (2.99995) within 2%.
- Cosmic ceiling: CFG630's settling energy budget (its JSON), as the ceiling on all P-wave energy ever radiated.
- Halos: galaxy (M_b 6e10 M☉, R 100 kpc), group (1e12, 500 kpc), cluster (1e14, 2 Mpc); relaxed (assembly over 10 Gyr) and
  merging (one crossing time R/V_f).
- Trapping: baryon-driven changes at ω ~ 2π/t_dyn below the local gap ω_m(r) = c_P m(r) are evanescent; the radiated
  fraction is ≤ exp(−2τ), τ = ∫ √(m² − ω²/c_P²) dr from the halo radius out to 1 Mpc (galaxy, group) or 5 Mpc (cluster).
- Numerical check (CFG696 PDE, code units): ramp the baryon source by +10% over T; the radiated energy must fall as T grows
  (adiabatic suppression). Reported with the fit exponent.

## Channels, thresholds and the comparison rule (frozen)
Rule: signal / threshold ≥ 1 → OBSERVABLE (or EXCLUDED, if the data already show nothing); 0.1–1 → NEAR THRESHOLD;
< 0.1 → BELOW THRESHOLD, with the factor quoted. A channel with no term in the action → REQUIRES NEW COUPLING (no term added).
- C1 gas heating: P-wave heating per unit mass vs free-free cooling per unit mass, Λ = 2.4e-27 √T erg cm³ s⁻¹, for cluster gas
  (n_e 1e-3 cm⁻³, T 5e7 K) and a galactic hot halo (n_e 1e-4, T 2e6 K). Threshold: 0.1 × cooling.
- C2 disc heating: P-wave heating per unit mass in the solar neighbourhood vs the observed growth of σ_z (≈ 20 km/s over
  10 Gyr). Threshold: 0.1 × that rate.
- C3 binary orbital decay: extra decay fraction vs the double-pulsar room, observed/GR = 0.999963 ± 0.000063 (Kramer et al.
  2021, quoted from the record of the literature, not re-fetched): threshold 9e-5 (2σ, one-sided).
- C4 timing / stochastic background (PTA band 1–100 nHz): P-wave power that escapes the source region, as a fraction of the
  GW power of the same sources. Threshold 0.1.
- C5 lensing: fractional departure of a merging cluster's phantom from its static profile (threshold 0.05) and the centroid
  offset (threshold 10 kpc).
- C6 light: any P–photon coupling term in the action.

## Control (MUTATE)
CFG659_MUTATE=1 sets the P–Φ coupling λ to 0 (the source g_N → λ g_N and δg = −4πG λ δP_L). PASS of the control iff every
channel's signal is exactly 0 and the CFG696 PDE run with λ = 0 radiates exactly 0. The MUTATE run must exit 1 if any channel
is non-zero.
