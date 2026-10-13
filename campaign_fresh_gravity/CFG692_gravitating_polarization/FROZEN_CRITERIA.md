# CFG692 — gravitating polarization: the bound charge as the cold mass (frozen criteria, committed alone)

Block CFG690–699. Written before any CFG692 script or number. κ = ½ fitted; both footings (9.3603e-11 / 1.1312e-10), never
pooled; the cold energy's mass is required; no particle species; not theory closed.

## The candidate (named before scoring, per CFG679)
CFG691 left astra's stiff sector failing lensing (M3a) and with no energy ledger (M2b). A sector's field energy cannot supply
the r⁻² density lensing needs. This candidate instead makes the **bound charge** of a vacuum polarization field the cold mass.
Newtonian-limit action, one potential Φ, no particle species:

L = −|∇Φ|²/8πG − (ρ_b + ∇·P)Φ − W(|P|) − (γ/2)|∇P|² + (I/2)|Ṗ|²,
W(P) = 2πG P² + (4πG)² P³/(3a₀).

- Poisson: ∇²Φ = 4πG(ρ_b + ∇·P). The cold mass is ρ_c = ∇·P. It sits in the one equation that sets the metric.
- Static P equation (γ = 0): W′(|P|) = |g|, with P antiparallel to g (antiscreening).
- The quadratic coefficient 2πG is the **criticality condition** W″(0) = 4πG: the medium's linear gravitational susceptibility is
  infinite. The cubic is the scale-invariant term (CFG690), with a₀ its only scale.
- This is the gravitational-polarization structure of the Blanchet class (MECHANISM_JOINT §7), here as a pure field with
  astra's stiffness, without dipole carriers. Its prior §7 failures (growing mode in the carrier fluid; S2) are re-scored for
  this variant.

## Tests
- **T1 (sympy). Static law.** Derive g_N(g) from W′(P) = g and g = g_N + 4πG P. Expected form:
  μ_crit(x) = 1 − (√(1 + 4x) − 1)/(2x), x = g/a₀. PASS iff the deep limit is g_N = g²/a₀ (flat curves and the BTFR at the
  framework's a₀) and the Newtonian limit is μ → 1. Report the high-field residual.
- **T2 (sympy). Stability of the static medium (fixed baryons).** Second variation per mode, including the gravitational
  self-energy of δ(∇·P):
  - longitudinal: W″(P) − 4πG + γk²;
  - transverse: W′(P)/P + γk².

  PASS iff both are > 0 for every P > 0 at γ = 0, so stiffness is not needed for stability. Report the longitudinal margin.
- **T3 (sympy). Lensing and the ledger.**
  - (a) In the Newtonian limit the lensing mass equals the dynamical mass, because ρ_c is in the one Poisson equation. This is
    structural; M3a scores CONDITIONAL on the relativistic completion having Φ = Ψ for this source, which is not derived here.
  - (b) ∫ρ_c d³x over a ball equals the surface flux of P: the cold mass is moved, not created. For the deep spherical solution,
    report M_c(<r) ∝ r (flat curves) and where the compensating charge must sit.
- **T4 (raw SPARC, data). The parameter-free interpolation.** ν from μ_crit at the framework's a₀, CFG4 statistic (CFG690's copy,
  controls as CFG690), Υ_disk profiled. PASS iff rms ≤ 0.110 with Υ_disk in 0.50–0.80 on both footings (CFG4 H2).
- **T5 (sympy + numbers). S2, external field.** A satellite with internal g_i ≪ g_e in a host field g_e. Linear response about
  P(g_e): longitudinal and transverse boosts ν_∥ = 1/(1 − du/dg), ν_⊥ = 1/(1 − u/g) at g_e, with u = 4πG P. S2 (§6: "ignore
  external fields") **FAILS iff the satellite's boost depends on g_e**. Report the boosts at g_i = 0.01 a₀ for g_e = 0, 0.1, 1 a₀.
- **T6 (reported).** High-field residual Δg/g_N at 1 AU and at Saturn, both footings. Stiffness screening is not modelled; this
  states what it would have to do.

## Verdict
Each CFG679 row this lane reaches is scored: R0, M1c (T2), M2a/M2b (T3b), M3a (T3a), C2 (T4), S2 (T5), S5 (T6, reported).

- **R0 rule, frozen now:** the critical coefficient 2πG is a tuning of W to G, made so that the deep law appears. R0 scores
  **R0-SHAPED (criticality + SI)** unless a committed source derives the criticality.
- **M1a** (attractor) stays UNTESTED. Radiation of P waves is named as the candidate dissipation channel, but no relaxation
  run is done here.

## MUTATE (`CFG692_MUTATE=1`, exit 1 iff every tooth bites)
- **M1:** W″(0) = 4πG × 1.1 (off-critical). The deep limit must no longer give g ∝ √g_N, so T1 fails.
- **M2:** the coupling sign flipped (screening). T1 must fail: g < g_N.
- **M3:** ν = 1 in T4 must fail (rms ≥ 0.25).
