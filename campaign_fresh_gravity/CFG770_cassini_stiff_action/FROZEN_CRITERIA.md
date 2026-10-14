# CFG770 FROZEN CRITERIA: Cassini Q2 for the framework's own one-field action (no basin rule)

Committed alone, before any script or number. 2026-10-14. Block CFG770–779 (owner chat; reserved in LEDGER in this commit).
Owner: "swing all of these rigorously one by one ... without any assumptions."

## Question
The framework's one-field action (CFG694/695 with the W_rem correction, PAPER47 v1.1, plus astra's stiffness, CFG691):

  L = −|∇Φ − K P|²/(2K) − ρ_b Φ − W_rem(u) − (γ/2)|∇P|²,  K = 4πG, u = K|P|,  K dW_rem/du = R(u) = u²/(a0 − u),
  Λ² ≡ γ/K, and CFG691's universal length L*² = 2Λ² (to be verified, K1).

Does it pass the 2026 Cassini quadrupole bound when the Sun sits in the Galaxy's own polarization background, with **no
free-fall-basin rule** (CFG693's basin rule is a definition, not part of the action; it gives Q2 = 0 by construction and is
NOT used here)?

## Method (declared)
- Background: uniform P_e from the Galaxy. Its magnitude follows from the action's own static solution:
  g_e = g_Ne + u_e, R(u_e) = g_Ne, so u_e = a0 g_e/(a0 + g_e).
- Sun: point mass M☉. Linear response of p = P − P_e. In the frame with ẑ ∥ P_e, A = diag(A⊥, A⊥, A∥),
  A∥ = R′(u_e), A⊥ = R(u_e)/u_e (dimensionless).
- Fourier solution:
  m_i(k) = (A_i + Λ²k²)/(A_i + 1 + Λ²k²),  δΦ(k) = −4πGM/(k² Σ_i k̂_i² m_i).
- Q2 in the record's (Park/Hees) convention δΦ = (Q2/2) x_i x_j (e_i e_j − δ_ij/3):
  Q2 = (GM/π) ∫ k² dk ∫ dc P2(c)/(m⊥ + c²(m∥ − m⊥)).
  Numerical quadrature in dimensionless κ = Λk.
- Galactic fields: g_e = 2.00 / 2.32 / 2.64 × 10⁻¹⁰ m s⁻² (the record's FP1/FP7 set). Both footings, a0 = 9.3603e-11 and
  1.1312e-10 (never pooled).
- Gates (the record's): Q2 < 5.2e-27 s⁻² (Park et al. 2026, 2σ); sunward anomaly at 1 AU < 3.66e-14 m s⁻²; anomalous
  mass inside 9.54 AU < 6.7e-11 M☉ (Pitjev & Pitjeva 2013).

## Controls (must pass, else the lane is VOID)
- K1: with no background (A → 0) the linear response's anomalous radial acceleration equals CFG691's inner pull GM/L*², to
  1e-3. This checks L*² = 2Λ².
- K2: isotropic background (A∥ = A⊥) gives Q2 = 0, to ≤ 1e-10 of the anisotropic value.
- K3: sympy verifies the directional derivatives of R(u)P̂: longitudinal R′(u), transverse R(u)/u.
- K4: linear validity: max K|p| / u_e ≤ 1e-3 for r ≥ 1 AU, at the worst case (smallest L*, both footings).

## Tests
- **T1 (headline):** Q2/ceiling at L* = 5.75 pc (CFG691's window floor, the worst case), all 3 g_e × 2 footings.
  PASS iff < 1 for all 6, otherwise FAIL.
- **T2 (reported):** Q2 across the window L* = 5.75–1000 pc.
- **T3:** the planetary gates for the stiffened Sun inside the background: sunward anomaly at 1 AU and the Saturn monopole,
  from the same linear response (isotropic part). PASS iff both < 1 at L* = 5.75 pc for all 6 cases.
- **T4 (reported, no verdict):** the Galactic boost at the Sun, g_e/g_Ne, in this action. Park et al.'s "≤ 2% boost"
  inference assumes classical AQUAL/QUMOND, where that boost and Q2 are locked together. Here T1 decides; nothing is asserted.
- **C0 (control, reported):** the action without stiffness (γ = 0). The sunward tail at 1 AU for the simple kernel is
  u(g_N) = a0 g/(a0 + g) → about a0, compared with 3.66e-14. Expected to fail by about 3000×.

## MUTATE (CFG770_MUTATE=1, separate outputs)
- M1: L* → 1e-4 pc (stiffness effectively off). T1 or T3 must FAIL.
- M2: drop the +1 (the KP term in ∇Φ = D + KP), i.e. m_i = (A_i + Λ²k²)/(A_i + Λ²k²) = 1. Q2 must go to 0 identically:
  the anomaly must come from the KP term.

## Hand estimate (written before any script)
- Screening length in the background: λ_e = Λ/√(A + 1) ≈ 1.4–2.4 pc. This is much larger than the Sun's MOND radius
  (~0.03 pc), so the whole Sun is screened.
- Q2 ~ 0.1 GM/Λ³ ≈ 2e-31 s⁻², i.e. ~1e-4 of the ceiling. **T1 PASS expected.**
- The constant sunward pull is ~GM/(L*²(1 + A)), below CFG691's background-free 4.2e-15. **T3 PASS expected.**

## Disclosures fixed now
- L* is the one extra constant (CFG691 window), not derived.
- The Galaxy's background is taken as uniform over λ_e (Galactic gradient scale ~ kpc).
- Linearization is checked (K4), not assumed.
- Passing here does not test the law; it tests whether the stiffened action survives Cassini without the basin rule.
- κ fitted; cold energy mass required; not theory closed.
