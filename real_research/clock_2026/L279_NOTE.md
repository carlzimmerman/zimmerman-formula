# L279 — the standing candidate's lensing, derived from its action (2026-09-18)

**Result.** For the single-metric clock host with the AeST-type coupling — the action the PPN pipeline uses
(`closure_2026/THE_ACTION_2026-09-05.md` with the coupling restored as in g03t) — the static, spherically
symmetric field equations derived from the reduced action give, at leading weak-field order with the scalar's
MOND nonlinearity kept exact:

    (H)  4 ∇²Φ − 2 c₁₄ ∇²Ψ = 16πG ρ + 2(2 − K_B) ∇²P          the Hamiltonian constraint (lapse variation)
    (T)  r χ'' − χ' = 0,  χ ≡ Ψ − Φ,  NO scalar term            the traceless equation (A − B/2 variation)
    (S)  2(2 − K_B) [ ∇·(J_Y ∇P) − ∇²Ψ ] = 0                   the scalar equation (the pipeline's static law)
    (C)  the clock tilt T satisfies an equation every term of which multiplies Q̄ (the cosmological roll)

with ds² = −(1+2Ψ)dt² + (1−2Φ)δ_ij dx^i dx^j in isotropic gauge, the clock τ = t + T(r), the scalar
φ = Q̄t + P(r), and J_Y = ∂J/∂Y evaluated on the profile. Consequences, certified in
`lean_2026/L279_lensing_algebra.lean`:

1. **Lensing = dynamics.** (T) with regularity at the origin and decay at infinity gives Ψ = Φ, so the lensing
   potential (Ψ + Φ)/2 equals the dynamical potential Ψ *including the MOND part*, because (H) puts the scalar
   into the spatial potential Φ through the coupling and (T) copies it into Ψ. This is the mechanism L278
   identified as AeST's and could not certify by hand; here it follows from the action.
2. **The measured Newton constant** is G_N = G/(1 − c₁₄/2): the number the record's f35/g03f found from a
   different route, reproduced here from the same action (V3).
3. **The effective MOND equation:** ∇·[(J_Y − β₀)∇P] = 4πGρ/(1 − c₁₄/2), β₀ = (2 − K_B)/(2 − c₁₄). With the
   deep-MOND carrier J = βY + (2/3)Y^{3/2}/ã₀ the standard law needs β = β₀, and then the phantom force is
   β√(ã₀ G_N M)/r = √(a₀ G_N M)/r with a₀ = β²ã₀.
4. **The slip is second order.** The next-order traceless source is
       2r²P'[ (2 − K_B)P'² + ã₀(2 − K_B)(βP' − 2Ψ') ]/ã₀
   (quadratic and cubic in the field gradients), and for a deep-MOND point mass of 10¹¹ M☉ at 30 kpc the
   induced slip is χ'/Ψ' = 3.5×10⁻⁷ (canonical footing) / 3.9×10⁻⁷ (alt), of order v_f²/c²: five orders below
   the lensing-RAR precision (0.05 dex).
5. **Mutation control.** Removing the coupling (MUTATE=1) removes the scalar from (H) and the source from (S)
   while leaving (T) untouched: the coupling-free action has no MOND and no lensing phantom (the "plain
   gravitating scalar" of L274-A4), as designed.

**What this closes and what it does not.** The lensing gate SW06 named as the one route not on the record
(A4) is now computed from the candidate's own action: lensing = dynamics holds at leading order and the
slip is 4×10⁻⁷. It does not close the candidate: the α₂ reconciliation (CK10), the Dirac count, causality of
the k⁴ operator, the galactic solve with the healing length, the cosmological perturbations and the cluster
residual remain (`clock_swarm_2026/CLOCK_WORK_ORDER.md`). Nothing here derives κ. Both a₀ footings carried.

**Method.** Every tensor is built from the metric by sympy (Christoffels, Ricci scalar, the clock's
covariant derivative, its acceleration J^μ, T₁–T₄, Q, Y); the reduced Lagrangian
√−g[R − c₁T₁ − c₂T₂ − c₃T₃ + c₄T₄ + 2(2−K_B)J^μ∂_μφ − (2−K_B)J(Y) − K₂(Q−Q̄)²] − 16πG N μ is expanded to
second order in the metric and clock perturbations with P exact and a₀ counted as first order (so that
J_Y = O(1) in deep MOND); the Euler–Lagrange equations for N, a, b, T, P are taken and ordered by the
physical smallness; symmetric criticality justifies the reduction for SO(3) with all invariant functions kept.
