# M2_cluster_compact — assumption ledger (before any script or number; committed with the frozen criteria)

Classes: RAW / FRAMEWORK-NATIVE / SURVEY-CALIBRATION / ΛCDM-PROCESSED / STANDARD-MOND-MACHINERY / EXTERNAL-THEORY /
EXTERNAL / POSTULATE (this lane's, counted).

The tested component is K1's C2 tidal-charge term (the owner's "black hole on the brane" idea), screened by the record's
stiffness profile S(s). Everything that feeds the cluster stack is inherited from K1, which inherited it from F1.

| # | ingredient | class | source | note |
|---|---|---|---|---|
| L1 | per-cluster KiDS ΔΣ, weights, boost (326 clusters) | RAW (F1's own estimator) | F1 scratch `f1_meas.pkl` (sha256 961ea4fc…e720), copied read-only, path = argv[1] | same object F1, H2, J1, K1 used |
| L2 | gas β-model (β = 2/3, r_c = 0.15 R500, to 3 Mpc), Mgas500 rescaled q^{5/2}, f* = 0.20 | SURVEY-CALIBRATION; R500 ΛCDM-PROCESSED | F1 `gas_mass()`, F1 ledger | inherited unchanged |
| L3 | distances: DESI DR2 D_M/r_d × 101.54/h, native h 0.672 / 0.686 | RAW × FRAMEWORK-NATIVE (C2) | F1 `DM()` | |
| L4 | data boost, catalogue miscentring (F1 PRIMARY) | as F1 | F1 | |
| L5 | law: AQUAL μ = x/(1+x), spherical root | FRAMEWORK-NATIVE (E2, C4) | F1 `g_aqual_sph` | κ = ½ FITTED; footings 9.3603e-11 / 1.1312e-10 m/s², never pooled |
| L6 | C2 kernel Φ_W(x) = −Gℓ_Q ∫ρ_b(x′)/\|x − x′\|² d³x′ (DMPR tidal charge per baryon mass element, P = −2U) | EXTERNAL-THEORY (DMPR, arXiv:hep-th/0003061, re-verified by K1 with sympy) + POSTULATE (K1's closure and Q ∝ dm rule) | K1 `c2_fields`, K1 README Part A | **not part of the theory's action** (Khronon + P + BS K(Q) dust has no 5D bulk) |
| L7 | lensing weight 3/4 of the dynamical Weyl mass (universal slip) | DERIVED in K1 (sympy, K3) | K1 | |
| L8 | A-ADD: the Weyl acceleration is added to the law's | POSTULATE (K1) | K1 L16 | |
| L9 | screening profile S(s) = s q(s): −[q″ + 2q′/s − 2q/s²] + q\|q\| = 1/s², q(0) = ½, S(∞) = 1 | FRAMEWORK-NATIVE for the P field of an isolated point mass (CFG691; D7d K1/K5; C6) | `campaign_fresh_gravity/CFG691_stiffness_window/cfg691.py` ODE, re-solved here | the record derives S(s) for the theory's own P field, not for an added term |
| L10 | s = r/ℓ_g, ℓ_g = L★²/(2 r_M), r_M = √(G M_b/a₀); for dwarfs r = r₁₂ = (4/3) R_h | FRAMEWORK-NATIVE (isolated) | CFG691, CFG820, E3 `B_scr` | D7d/D10: in an external field the screening is not multiplicative and the length is L★ itself; disclosed, not modelled |
| L11 | **screening the C2 term with S(s), per object, with ℓ_g from that object's total baryon mass** | **POSTULATE (this lane, new)** | coordinator's hypothesis | no action yields it; per-object screening breaks linear superposition |
| L12 | object-mass rule: cluster = all baryons inside 3 Mpc; galaxy = its total M_b; dwarf = M★; Sun = M☉; wide binary = 1.5 M☉ total; Milky Way host 6.0e10 M☉ | RULE (POSTULATE, this lane) | F1, F2, E3, D7d/C6 conventions | |
| L13 | L★ = 24 / 50 / 90 pc (not fitted) | FRAMEWORK-NATIVE window | D10 floor 21.68 / 22.85 pc; D7d/C6/D8 window to ≈ 90 pc | three points of the existing window, frozen; no scan |
| L14 | isolated lens masses log M_b 10.36 / 10.83 / 11.01 / 11.18; tolerance 0.14 | SURVEY-CALIBRATION (LePhare M★) via F2 | F2 results, as K1 L19 | graded on K1's exact point-source C2 formula (K1 A3) |
| L15 | dwarf satellites: σ, R_h, M★, M_dyn, host, B_scr at L★ = 24 pc | RAW / SURVEY-CALIBRATION / FRAMEWORK-NATIVE as E3 | E3 `e3_per_system.csv`; LVD distances `real_research/data/dsph/` | central values (K1 A1 baseline, no second binary correction); M★ is SPS (E1 soft flag) |
| L16 | E3's `B_scr` recipe with the CFG691 S table (interpolated in ln s) for the law's baseline at L★ = 50 and 90 pc | FRAMEWORK-NATIVE (CFG820 recipe) | E3 `e3_dwarf_excess.py` L45–62 | reproduced against the CSV at 24 pc |
| L17 | MW 6.0e10 M☉, M31 1.0e11 M☉, Hernquist a = 3 kpc; R₀ = 8.122 kpc | SURVEY-CALIBRATION (record values) | K1 L21 | |
| L18 | planet bounds 8.7e-15 / 1.4e-15 / 7.0e-15 m/s² (constant radial δg, from perihelion-advance σ's) | RAW-derived ephemeris bounds as used by the record | C6 L35; `prep_2026/planetary_doors/BOUNDS.md` §1.2 | the bounds come from perihelion precession, so a pure 1/r² term (a change of GM☉) is invisible to them |
| L19 | Cassini Q₂ lines: Hees 2014 2σ 9.0e-27 s⁻², Park 2026 2σ 5.2e-27 s⁻² | EXTERNAL (record values) | C6 L28–29; BOUNDS.md §1.1 | order of magnitude only (convention factor ≤ 2) |
| L20 | wide-binary line γ_v − 1 ≤ 0.25 at 5 and 20 kAU, 1.5 M☉ | RULE: above the record's largest reading (law-first 1.18–1.21, D2/D7d) | D2, D7d, C6 | the observational case is contested; the line only excludes boosts larger than any reading in the record |
| L21 | background for the growth estimate: Ω_m = 0.2976, h = 0.6856, ω_b = 0.022209, ω_c = 0.11707 (E-886) | EXTERNAL (CFG886 GR fit as used by C2) | `covariant_push_2026_10_22/C2_aest_cosmology/c2_aest_cosmology.py` L115–116 | reported only; growth belongs to F3/CFG960 |
| L22 | ℓ_Q is a physical (not comoving) length | POSTULATE (follows from the static per-element construction) | this lane | sets the growth estimate's k/a scaling |
| L23 | spherical symmetry; weak field; leading order in Φ/c² | FRAMEWORK choice | | |

**Count for the tested component.** Postulates: L6 closure (+1), L6 Q ∝ dm (+1), L8 A-ADD (+1), L11 screening applies
to the C2 term (+1, new), L12 object-mass rule (+1, new), L22 physical ℓ_Q (+1, new; affects only the growth report).
Constants: ℓ_Q (+1, calibrated on F1 MID); L★ (existing, not fitted).

No ΛCDM machinery enters any prediction beyond what F1 already carries (L2). No standard-MOND machinery enters: the law is
AQUAL, and the screening is the record's own isolated profile.
