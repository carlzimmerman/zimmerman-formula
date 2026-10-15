# CFG793 FROZEN CRITERIA: is there a portal from cold energy to light inside the committed action? (committed before any script)

HYPOTHETICAL (ramjet context: CFG789–792). Question: with NO new coupling, does the committed action
(THEORY_CANONICAL_2026-10-14 S2, plus the kinetic term (I/2)|∂ₜP|² of CFG694/696)

  L = −|∇Φ − K P|²/(2K) − ρΦ − W_rem(u) − (γ/2)|∇P|² + (I/2)|∂ₜP|²,  K = 4πG, K W_rem′(u) = u²/(a₀ − u), γ = K L*²/2,
  c_P² = γ/I,

let ambient cold energy be turned into photons? Electromagnetic energy gravitates, so ρ includes u_EM/c². That is the
only route by which photons and P touch. κ = ½ is fitted; L* ∈ [5.75 pc, ~1 kpc] is bounded, not derived; c_P is not
fixed by the record (CFG696/762), so it is scanned (c, 10⁻³c, 200 m/s). Both footings, a₀ = 9.3603e-11 and 1.1312e-10.
External inputs (provisional, quoted from memory): ρ_c = 0.01 M☉ pc⁻³ (ρ_c c² = 6.1e-5 J/m³, as in CFG792); local
Galactic field 2.1e-10 m/s².

## Derivation to be implemented (fixed now)
1. Split Φ = Φ_P + Φ_ρ with ∇Φ_P = K P_L (longitudinal part). Then −|∇Φ − KP|²/2K = −|∇Φ_ρ − K P_T|²/2K: the longitudinal
   P drops out of that term (criticality: no mass term), and its only coupling is −ρ Φ_P with ∇²Φ_P = K ∇·P, i.e. Newtonian
   gravity between the cold mass ∇·P and all other energy.
2. In a static field B₀ ⊥ k, a photon with b ∥ B₀ carries δρ = B₀·b/(μ₀c²). In Fourier space Φ_P = −iK P_L/k. With canonical
   fields this gives a mixing rate g = K B₀ √(ε₀/I) and, normalised to energy flux, Δ_P = g/(2ω√(c c_P)) =
   √(2Kε₀) B₀ √(c_P/c)/(2 ω L*). Conversion probability P = (2Δ/Δ_osc)² sin²(Δ_osc L/2), with Δ_osc² = q² + 4Δ² and
   q = ω(1/c − 1/c_P) (plus the W_rem gap where relevant).
3. Prediction to test: Δ_P/Δ_grav = (1/√2)√(c_P/c)(ƛ/L*), with ƛ = c/ω. So the built-in portal is Gertsenshtein-like
   (∝ G) times an extra factor (ƛ/L*)²(c_P/c)/2 in probability.

## Questions and classes
- **Q1 (mixing).** P_P→γ for B = 10, 45 T; L = 1, 10, 100 m; magnetar B = 1e10 T, L = 1e4 m. Photon energies: 2.5 eV
  (optical) and 2.24 meV (ARGON03's native scale). L* = 5.75 pc and 1 kpc; c_P scan above. Classes: P < 1e-30 everywhere
  in the lab ⇒ **GRAVITATIONALLY SUPPRESSED**; report orders below Gertsenshtein and below unity.
- **Q2 (static field).** Theorem to state and check numerically: in the cold energy's rest frame a static ambient P plus a
  static device has a time-independent Lagrangian, so energy is conserved and a static solution does not radiate.
  Continuity (∂ₜ∇·P = −∇·j) conserves cold mass, so **rest-mass energy cannot be released by any term of this action**. A
  moving device sees ω = k·v with k ≲ 1/L* (stiffness scale); report the photon wavelength for v = 0.1c and 0.998c, and
  the total energy any device can gain, ≤ M|ΔΦ_c| (gravity is conservative). Numerical check: a mass crossing a bounded
  static cold clump gains net work 0 (to 1e-6 relative to the peak work), and in a uniform gradient gains exactly M g d.
  Classes: if both hold, **STATIC CONVERSION FORBIDDEN** (time dependence does not help: it only exchanges the craft's own
  kinetic energy).
- **Q3 (efficiency).** η = output power / intercepted ρ_c c² v A. Report
  - η_rest = 0 (exact, by Q2),
  - the gravitational-work ceiling η_grav ≤ (M/A) g_c/(ρ_c c²) for M/A = 1 mg/m² and 1 g/m², with g_c = a₀ (each footing)
    and 2.1e-10 (this is work on the craft, not light),
  - η_mix for a moving 45 T, 100 m device at v = 0.1c converting the static field (field energy fraction from CFG792).
  Compare with the needed η = 0.01–1 and report orders short. Class: η_max < 1e-6 ⇒ **NO BUILT-IN PORTAL**.

## Controls
- **K1.** Numerical integration (scipy solve_ivp) of the two-mode equations reproduces the analytic P to 1e-6 relative,
  matched and mismatched.
- **K2.** The same normalisation routine, fed the linearised-GR coupling (L_int = ½ h_ij T^ij, TT graviton), returns the
  standard Gertsenshtein P = 4πG B²L²/(μ₀c⁴) to 1e-10 and the literature value ≈ 8.3e-38 (B/1 T)²(L/1 m)² within 5%
  (provisional anchor, from memory).
- **K3 (dimension check).** Δ_P computed from the explicit (g, I) route and the closed form agree to 1e-12.
- **MUTATE** (CFG793_MUTATE=1, separate outputs `cfg793_MUTATE.out`, `cfg793_results_MUTATE.json`): set L* = ƛ (the photon's
  reduced wavelength) and c_P = c. Then Δ_P/Δ_grav must become 1/√2 (the (ƛ/L*) factor bites) and Q1 must still sit at
  Gertsenshtein level (G factor remains), and the script exits 1 if the Q1 class does not change from what the main run gives
  for the extra suppression.

κ fitted; not theory closed. No dark matter particle species.
