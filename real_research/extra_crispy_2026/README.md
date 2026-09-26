# extra_crispy_2026 — the gates the recipe flagged and nobody ran

The crispy recipe (`qwen_claude_field_theory/closure_2026/CRISPY_FRIED_CHICKEN_RECIPE.md`) red-flagged one gate as "THE
make-or-break": **G8, strong coupling** (sec. 5, and the sec. 9 table: "G8 Λ_sc as η→0 — OPEN"). It was never computed.
The khronometric candidate it was written for died first (FC-KH, a radial gradient instability, 09-01), and the live
candidate C-H/K (L340) does not list it. This directory runs the unrun gates on C-H/K, one lane per gate, each with a
MUTATE control and a Lean certificate of its algebra in `fable_independent_2026/lean_2026/XC*_*.lean`.

## XC1 — G8 strong coupling on C-H/K: PASS (9/9; MUTATE α_c = 0 fails A4, rc = 1)

`XC1_strong_coupling_chk.py` (+ `.out`, `_MUTATE.out`, results JSON). Lean: `XC1_strong_coupling_certificates.lean`
(12 theorems, zero `sorry`, axioms propext / Classical.choice / Quot.sound).

- **The UV khronon is pure khronometric gravity.** Above k ≈ 1/ξ the heat filter removes the C-H sector exactly:
  eliminating U gives the clock inertia 2C/(1+C) with C = C₀e^{−ξ²k²}, and at U = ln N the C-H term vanishes identically.
  At AU scales log₁₀ C/C₀ ≈ −1.8×10⁷. So the only kinetic term the khronon keeps there is α_c a².
- **Literature control.** Expanding α a·a − c₂K² to quartic order, the lowest strong-coupling scale over all vertex
  classes is √α M c_s^{3/2} (c_s < 1) and √α M c_s^{−1/2} (c_s > 1). This reproduces Gümrükçüoğlu, Saravani & Sotiriou
  2018 (PRD 97, 024032) eq. (15). The binding vertices are the c₂ cubic and the α cubic with three time derivatives.
- **The gate.** Over L340's window (α_c 9.6×10⁻¹⁴ … 3.2×10⁻⁹) and every c₂ value (L350's Planck-era caps and L340's
  window), the strong-coupling momentum is ≥ 8.5×10⁸ GeV, 6.5×10⁴ times the LHC. a₀ does not enter, so both footings
  give the same answer.
- **The MUTATE control fails.** With α_c = 0 the UV kinetic term is exponentially zero, so the khronon is strongly coupled at
  every Solar-System scale. This is the recipe's P7 made quantitative; α_c is what answers it.
- **The dark-energy identity.** Without the filter, the MOND vertex (2/3)C_L′/α_M makes the MOND sector strongly
  coupled at 0.9–5.3 meV (0.04–0.23 mm). By an exact identity this is the dark-energy scale:
  √(M_P a₀/c²) = (κ²/8π)^{1/4} ρ_Λ^{1/4} = 0.71 meV (canonical) / 0.78 meV (alt). Berezhiani & Khoury (2015) noted the
  same meV coincidence.
- **The filter.** The filter's form factor e^{−ξ²k²/2} on every MOND leg caps the MOND coupling at 1.4×10⁻³⁸ at the
  committed Cassini floors, so the sub-mm cutoff is never reached.
- **Reading.** The UV khronon is superluminal but finite, at 4.4×10² – 7.9×10⁵ c. It is causal on the preferred
  foliation (L318's criterion B). Under the metric-cone criterion (A) it is superluminal, as L318 shows every scalar
  MOND realisation is.

**Not covered.** Loops and naturalness (G12); the filter's own metric-variation vertices, which carry α_M² and are not
computed separately; the UV completion; nonlinear well-posedness.

**Literature status of the black-hole gate (not computed here).** Ramos & Barausse 2019 found that regular slowly moving
black holes need α = β = 0 exactly. Kovachik & Sibiryakov 2023/2025 (arXiv:2311.12936) find regular solutions for
general small α, β, λ, analytic outside the universal horizon. C-H/K's UV sector is exactly this khronon, so the question
is open in the literature and not settled here.

## XC2 — nonlinear well-posedness of C-H/K, scoped: the elliptic half settled, the rest reduced (7/7; MUTATE C = −1.5 fails B4, rc = 1)

`XC2_wellposedness_scoping.py` (+ `.out`, `_MUTATE.out`, results JSON). Lean: `XC2_wellposedness_certificates.lean`
(9 theorems, zero `sorry`, standard axioms). This is L340's first open item. No full theorem is claimed. The lane
settles what can be settled and reduces the rest to a question about khronometric gravity itself.

- **The MOND constraint has exactly one solution on every leaf.** For a fixed metric and lapse, the U-equation is the
  Euler–Lagrange equation of E[U] = ∫N√h{2|DU − D ln N|² + 2α_M²q(|DSU|²/α_M²)}.
  - The q-integrand's Hessian has eigenvalues 4C_T (twice) and 4C_L (B1).
  - The heat filter never raises the Dirichlet energy on any closed leaf (B2).
  - Together these give δ²E ≥ 4(1 + min(0, C_min))‖Dδ‖². So E is strictly convex whenever C_min > −1.
  - C_min > −1 is exactly "g(g_N) strictly increasing", and every kernel on the record meets it (B3): ν_mono 0,
    ν_RAR −0.032, μ₂ −0.081, μ_exp −0.119, μ₅ −0.253, μ₁₀ −0.348.
- **Numerical demonstration (B4).** On a 2-D periodic leaf with a lapse varying by 30%, four random starts converge to
  the same U to 3×10⁻⁷ for both ν_mono and ν_RAR. The lowest non-trivial Hessian eigenvalue is +0.022.
- **The MOND sector is lower order (B5).** The linearised MOND operator falls like ≈30 e^{−ξ²K²} relative to the
  principal part: 0.51, 3.6×10⁻³ and 1.6×10⁻⁶ at K = 2, 3 and 4/ξ. It is a smoothing operator. With XC1 A3 (U = ln N
  removes the C-H term), the principal symbol of C-H/K is that of GR plus the BPS khronon.
- **The khronon is hyperbolic only because α_c > 0 (B6).** Its symbol is k²(α_c ω² − c₂k²), with the finite cone
  c_s² = c₂/α_c. At α_c = 0 the time derivatives drop out and the lapse becomes elliptic. That is minimal Hořava gravity,
  whose Cauchy problem fails after a dust shell collapses (Jacobson & Pulakkat 2025, J. Phys. A 58, 315404). α_c > 0
  is load-bearing a third time, after L340's negative lobes and XC1's strong coupling.
- **The zero-field limit is controlled (B7).** The deep-MOND flux |p|^{1/2}p̂ is Lipschitz at isolated zeros of the
  filtered field (codim 2 and 3, generic after filtering). At a symmetric planar zero set (codim 1) it is only
  log-Lipschitz: R² = ln(1/ε)/2, with a measured slope of 0.500. The log modulus still satisfies Osgood's uniqueness
  criterion. This is spec requirement 9.

**Reduced, not settled.** Is GR plus the BPS khronon (α_c, λ − 1 = c₂, β = 0) strongly hyperbolic on arbitrary
nonlinear backgrounds? Einstein-aether theory is, under conditions on its couplings (Sarbach, Barausse & Preciado-López
2019, CQG 36, 165007). No general theorem for the hypersurface-orthogonal case is used here, and its α → 0 limit fails.
