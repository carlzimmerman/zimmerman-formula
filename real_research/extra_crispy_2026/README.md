# extra_crispy_2026 — the gates the recipe flagged and nobody ran

**Peer-review correction — 2026-09-26.** The independent
[XC1/XC2 review](../peer_review_2026_09_26/README.md) preserves the flat
khronon power counting and the fixed-background monotone-kernel leaf result,
but the closure labels below require restriction. XC1 omits mixed heat-filter
vertices and does not close full G8. XC2's unweighted-to-lapse-weighted
convexity inference fails for both exact nonmonotone kernels; its zero-field
argument omits allowed homogeneous and degenerate-zero configurations, and
its U-only calculation does not establish the full metric/clock principal
symbol. Its B4 fixture also supplies an acceleration different from D ln N.
The all-kernel elliptic and zero-field claims are not settled. Original lane
outputs below are retained as the historical computations, with exact
counterexamples and remaining calculations linked in the review.

The crispy recipe (`qwen_claude_field_theory/closure_2026/CRISPY_FRIED_CHICKEN_RECIPE.md`) red-flagged one gate as "THE
make-or-break": **G8, strong coupling** (sec. 5, and the sec. 9 table: "G8 Λ_sc as η→0 — OPEN"). It was never computed.
The khronometric candidate it was written for died first (FC-KH, a radial gradient instability, 09-01), and the live
candidate C-H/K (L340) does not list it. This directory runs the unrun gates on C-H/K, one lane per gate, each with a
MUTATE control and a Lean certificate of its algebra in `fable_independent_2026/lean_2026/XC*_*.lean`.

## XC1 — G8 strong coupling on C-H/K: bounded pass in the decoupling-limit scope (9/9; MUTATE α_c = 0 fails A4, rc = 1)

**Scope label (corrected 09-26 after the lead track's audit, `real_research/closure_resume_2026_09_26/`, uncommitted at the time):** XC1 is tree-level power counting in the decoupling limit on frozen backgrounds. It is a bounded pass within that scope, and conditional at full-action scope. It does not cover full curved-background mixing, the assembled action, or causal closure. The filter/foliation vertices it originally omitted are computed in XC3.

`XC1_strong_coupling_chk.py` (+ `.out`, `_MUTATE.out`, results JSON). Lean: `XC1_strong_coupling_certificates.lean`
(12 theorems, zero `sorry`, axioms propext / Classical.choice / Quot.sound).

- **The UV khronon is khronometric gravity up to e^{−ξ²k²}.** Above k ≈ 1/ξ the heat filter suppresses the C-H sector
  by e^{−ξ²k²}. That factor is positive at every finite k, so the removal is exponentially small, not exact. Eliminating U
  gives the clock inertia 2C/(1+C) with C = C₀e^{−ξ²k²}; the C-H term vanishes identically only at the C = 0 solution
  U = ln N. At AU scales log₁₀ C/C₀ ≈ −1.8×10⁷, so the only kinetic term the khronon effectively keeps there is α_c a².
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
  the same U to 3×10⁻⁷ for both ν_mono and ν_RAR. The lowest non-trivial Hessian eigenvalue is +0.247.
  *[Corrected 09-26: the first version reported +0.022, which was the value assigned to the lifted trivial modes, not
  the lowest non-trivial eigenvalue. Positivity was never in question.]*
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

**Two scope corrections (09-26, from the lead track's review and a peer session; computed in XC5):**
1. B2's "any closed leaf" holds when the filter and the energy share one measure. C-H/K's functional carries the lapse,
   and the geometric filter need not contract the lapse-weighted energy. So B3's convexity needs
   (N_max/N_min)|C_min| < 1 for kernels with C_min < 0. For ν_mono (C_min ≥ 0) no condition is needed (XC5).
2. B7's "controlled" covers isolated and planar zeros only. Around an open zero-field region (a homogeneous background)
   the response scales as √ε for every kernel, ν_mono included, and that fails Osgood (XC5 E6).

**Reduced, not settled.** Is GR plus the BPS khronon (α_c, λ − 1 = c₂, β = 0) strongly hyperbolic on arbitrary
nonlinear backgrounds? Einstein-aether theory is, under conditions on its couplings (Sarbach, Barausse & Preciado-López
2019, CQG 36, 165007). No general theorem for the hypersurface-orthogonal case is used here, and its α → 0 limit fails.

## XC3 — the filter's own foliation vertices, the piece XC1 left out: harmless at frozen-background scope (6/6; MUTATE time-dependent background fails C1/C2, rc = 1)

`XC3_filter_foliation_vertices.py` (+ `.out`, `_MUTATE.out`, results JSON). Lean: `XC3_filter_foliation_certificates.lean`
(5 theorems, zero `sorry`, standard axioms). Prompted by the lead track's audit, which flagged the filter/foliation
interaction as the gap in XC1. The MOND term depends on the khronon's leaves twice: through the leaf metric in
|DW|²_h, and through the leaf Laplacian inside W = e^{bΔ_h}U.

- **Both dependences start at O(π²) on a static background, with two powers of the background in every term (C1, C2;
  exact jet expansions).**
  - Δ_hF has no O(π) term. Its O(π²) term is ∂_iπ∂_jπ∂_i∂_jF + Δπ(∇π·∇F).
  - The argument is |∇W₀|² + (∇π·∇W₀)² − 2π̇(∇π·∇W₀)² + O(π⁴).
- **The heat-kernel derivative.** δS = b∫₀¹e^{(1−v)bΔ}δΔ e^{vbΔ}dv is verified against finite differences, with a
  second-order residual. It is bounded by b·max_v‖δΔ e^{vbΔ}f‖, and its high-K factor is ≤ min(b, 1/K²) (C3).
- **Quadratic terms (C4).** Against the khronon's own gradient term they are ≤ 6C_T(gL_bg)²/c₂. The largest value,
  3.5×10⁻⁷, is in a cluster core at k = 1/L_bg; it is 10⁻¹¹ for the Sun and galaxies.
- **The sign (C5).** The (∇π·∇W₀)² term lowers the gradient energy, so the band k < g√(2C_T/c₂) is formally unstable.
  But k_thr·L_bg ≤ 3.4×10⁻⁴ for every background, so no mode the local analysis describes ever sees it. The band's
  wavelengths are Gpc-scale, longer than the structure that produces them.
- **Cubic vertices (C6).** The leading one is −2M_P²C_T π̇(∇π·∇W₀)². These are relevant operators whose couplings are
  suppressed by the background; they become strong only below 1.9×10⁻⁹² GeV, far below the Hubble energy.
- **MUTATE.** A time-dependent background brings back O(π) terms, −2∇π·∇(∂_tF) − Δπ ∂_tF. That is the moving-source
  physics of L340's T1, not a new vertex.

**G8 standing after XC1 + XC3.** A bounded pass at frozen-background, decoupling-limit scope, now including the
filter/foliation interaction. It remains conditional at full-action scope: curved-background mixing, the assembled
action, and loops are not computed.

## XC4 — the 2026-09-26 decisions, recorded in the recipe and spec, with their mathematics certified

The author decided three open points after XC1–XC3. They are recorded as a dated user-decision block in
`qwen_claude_field_theory/closure_2026/CRISPY_FRIED_CHICKEN_RECIPE.md`, and as operative amendments to requirements 1,
7 and 12 in `FRIED_CHICKEN_SPEC.md`. The original text is kept, marked as amended.

1. **The kernel is ν_mono.** This is the RAR exponential law with a monotone phantom. It follows ν_RAR below the peak
   and stays within 0.01 dex of it everywhere (L340).
2. **Causality is criterion B.** This means a global preferred time compatible with every characteristic cone, and no
   signal backward in that time. Criterion A is unsatisfiable by any scalar MOND realisation (L318).
   - This has a consequence both ways: gate 7's signalling theorem is a criterion-A result, so it no longer closes
     the strict two-DOF constraint branch (cde_l4c_2026, status OPEN). That branch's other gates were never derived.
3. **Z is corrected in §1.** Z = √(32π/3) = 5.7888 is κ = ½ restated, not "~21".

Lean: `XC4_recipe_decision_certificates.lean` (5 theorems, zero `sorry`, standard axioms):
- `z_is_kappa`: κ = ½ ⟺ Z² = 32π/3.
- `z_value_bounds`: 5.788 < √(32π/3) < 5.789.
- `mono_phantom_increasing`: ν_mono's phantom slope is > 0.
- `mu_exp_phantom_turns`: C_L = (1−x)/(eˣ+x−1) < 0 for x > 1.
- `nu_rar_phantom_turns`: 9/(e³−1) < 4/(e²−1).

## XC5 — the constraint with a non-constant lapse: what the ν_mono decision buys, and one correction the other way (6/6; MUTATE C = −1.5 fails E5, rc = 1)

`XC5_lapse_weighted_convexity.py` (+ `.out`, `_MUTATE.out`, results JSON). Lean: `XC5_lapse_convexity_certificates.lean`
(4 theorems, zero `sorry`, standard axioms). This lane takes up the lead track's finding
(`real_research/closure_doors_2026_09_26/auxiliary/`, uncommitted at the time) that the geometric heat filter need not
contract the lapse-weighted energy.

- **The finding, reproduced (E1).** The largest d/db ∫N|De^{bΔ}f|² / ∫N|Df|² over all fields is a generalised
  eigenvalue problem. On a single-mode lapse well it changes sign at contrast N_max/N_min ≈ 263 (+74 at 10³). With
  N = 1 it is always negative.
- **The contrast bound (E2, Lean `contrast_bound`).** ∫N|DSf|² ≤ (N_max/N_min)∫N|Df|². So for a kernel with a
  negative coefficient, the constraint is convex when (N_max/N_min)|C_min| < 1.
- **What the ν_mono decision buys (E3, Lean `convex_for_monotone_kernel`).** ν_mono's coefficients are positive at
  every y. The q-integrand is therefore convex, and the constraint is strictly convex (one solution) for any positive
  lapse with the unchanged filter.
  - No contrast condition and no filter repair are needed.
  - The demonstration (E5) at realised contrast 27.4 converges from four starts, with lowest eigenvalue +11.3.
- **Why it matters where it matters (E4).**
  - The turning kernels' thresholds are: μ_exp exactly e² + 1 = 8.39 (its C_L minimum is −1/(e²+1); Lean
    `mu_exp_CL_floor`), ν_RAR 30.8, μ₁₀ 2.88.
  - In weak fields the lapse contrast is ≤ e^{2×10⁻⁴}, so the kernel choice doesn't matter for uniqueness.
  - Near compact objects the contrast is unbounded, and only a C_min ≥ 0 kernel keeps the constraint convex there.
- **The correction the other way (E6).** Around an open zero-field region the response scales as √ε for every kernel,
  ν_mono included (log-slope −0.500). √ε fails Osgood, and ẋ = √x has two solutions from 0 (Lean
  `sqrt_ode_two_solutions`). So linear perturbation theory does not exist around a homogeneous zero-field background.
  In the assembled construction the vacuum-gated switch keeps the kernel off there (L359/L361).
- **Scope.**
  - This is convexity of the fixed-metric, fixed-lapse auxiliary solve, not coupled time stability. The filter's
    failure to contract still matters for energy estimates.
  - ν_mono's splice makes the q-integrand C² but not C³ at the splice point.
