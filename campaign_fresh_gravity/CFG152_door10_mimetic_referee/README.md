# CFG152 — referee of CFG124 (door 10, mimetic gravity): the perturbation sound speed and the ghost window

- **Criteria:** frozen in `../CFG152_FROZEN_CRITERIA.md` (commit 7be9ce713, sha256 ed516168…33e9) before any script or number. Every script prints that hash first, and every run matched it.
- **Target:** one headline of CFG124 (`../CFG124_door10_mimetic/README.md`, G5 line): "c_s^2 = gt/(2 - 3 gt) ... with a ghost (negative kinetic term) for every 0 < gt < 2/3, and gradient instability for gt < 0 or gt > 2/3: no stable healthy gt exists". Here gt = 8πGγ = γ/M_P² is one dimensionless number.
- **Scripts** (own code; they import nothing from other lanes):
  - `cfg152_common.py`: a brute-force second-order expansion of the covariant action (truncated series), the Fourier Hermitian form, and gauge vectors from the Lie derivative;
  - `cfg152_M1_minkowski.py` (method M1, controls C0, C1, C4, numerics N1);
  - `cfg152_M2_frw.py` (method M2, routes U and N, controls C1, C2, C3);
  - `cfg152_S_shells.py` (the secondary row);
  - two labelled POST-HOC scripts, written after all frozen runs and after reading CFG124's code: `cfg152_S_posthoc_cfg124grid.py` and `cfg152_posthoc_T04_lambda.py`.
- **Runs.** All of them together take under two minutes. Outputs are named by mode (`.out` and `_results.json`).

| script | main | MUTATE=a | MUTATE=b | MUTATE=s | MUTATE=1 |
|---|---|---|---|---|---|
| M1 (Minkowski) | **1** (control C4 only; every H line passes) | 1 | 1 | — | 1 |
| M2 (FRW) | **0** (23 of 23) | 1 | 1 | — | 1 |
| S (shells) | **0** (4 of 4) | — | — | 1 | 1 |
| POST-HOC grid, POST-HOC T0.4 | 0, 0 (reported only) | | | | |

## Bottom line

**Reproduced.** For CFG124's action (+(γ/2)(□φ)², signature −+++):
- The one propagating scalar has c_s² = gt/(2 − 3gt) exactly.
- Its kinetic coefficient is proportional to −(2 − 3gt)/gt with a positive factor. It is a ghost for exactly 0 < gt < 2/3.
- It has a gradient instability for exactly gt < 0 and gt > 2/3.
- The ghost-free, gradient-stable window is empty.

**How it was shown:**
- **Minkowski:** my own covariant brute-force expansion, with no ADM split. It gives the result in two complete gauges, as a one-field reduced action, and through a gauge-invariant (Krein) energy sign.
- **Flat FRW with arbitrary a(t) and V:** two routes, the unitary-gauge reduced Lagrangian and the Newtonian-gauge equations of motion.
- **Numerically:** 24 points, 12 values of gt at k = 0.5 and 2.

**End points:**
- gt = 0 is frozen dust: no wave, and the kinetic coefficient diverges.
- gt = 2/3 is singular: the kinetic coefficient is 0 there, and c_s² and the background coefficient 2 − 3gt have a pole and a zero respectively.
- Superluminal propagation, c_s² > 1, occurs for 1/2 < gt < 2/3, inside the ghost window.

The model at CFG124's G2 bound (gt = 8.5 × 10⁻¹¹) is a ghost, with c_s² = 4.25 × 10⁻¹¹.

**Secondary row (point-mass half):** 0 of 1600 shell cases survive 10 Gyr, as CFG124 says (0 of 2624). The fall-time maximum is 3.765 Gyr at x = 30 against CFG124's 3.69 (README "3.7"). The cause is CFG124's grid: its last scored point is x = 29.41, not 30. On that grid my own formula gives 3.6905 Gyr.

**One miss, outside the headline (side finding, post-hoc):** CFG124's T0.4a labels its background energy "eps = −2 lam". For gt ≠ 0 that label is wrong, because its background Lagrangian drops the lapse dependence of □φ.
- The multiplier is λ̄ = (1 − 3gt)M_P²Ḣ (my brute force, and CMV eq. 80), not (1 − 3gt/2)M_P²Ḣ.
- The quantity CFG124 prints, (3/8πG)(1 − 3gt/2)H² − V, is the conserved first integral, −2λ̄ − 3gt M_P²Ḣ.
- So T0.4b, G2.2 and the headline do not change.

**One frozen control failed, kept:** C4 (details under Controls).

## Comparison with CFG124 (its scripts and outputs, read only after all CFG152 runs)

| item | CFG124 | CFG152 | agree |
|---|---|---|---|
| c_s² | gt/(2 − 3gt) (T0.6a: reduced ADM action, unitary gauge, FRW) | gt/(2 − 3gt) exactly: Minkowski (det in unitary and Newtonian gauge, Schur-reduced action) and FRW (route U, route N) | **yes** |
| kinetic coefficient | ζ̈ coefficient of the EOM A = −2(3gt − 2)a³/(8πG gt), so K = −A/2 = −M_P² a³(2 − 3gt)/gt | route U: A = (M_P² a³/2)(3 − 2/gt) (x-averaged, so ×2 = CFG124's K); Minkowski K = 2M_P²(3 − 2/gt) (plane-wave normalisation) | **yes** |
| gradient term | B = 2M_P² a (k²ζ in the EOM) | +(M_P² a/2)k² Ψ² in the Lagrangian (x-averaged): the wrong sign for every gt; no mass term | **yes** |
| ghost window | 0 < gt < 2/3 (closed form plus 4 sampled gt) | exactly (0, 2/3) as a sympy set; Krein sign −1 at every real root in N1 | **yes** |
| gradient instability | gt < 0 or gt > 2/3 (2 sampled gt) | exactly (−∞, 0) ∪ (2/3, ∞); growth rates \|Im ω\|/k = √\|c_s²\| to 2 × 10⁻¹⁶ | **yes** |
| healthy window | none | the empty set | **yes** |
| gt = 0 (class A) | ζ frozen by the momentum constraint (T0.6c) | det ∝ ω² (double zero root); B-equation Ψ̇ = 0; δφ̈ + Hδφ̇ + Ḣδφ = 0 | **yes** |
| gt = 2/3 | "a pole" (frozen text) | K = 0, c_s² pole, background coefficient 2 − 3gt = 0 | **yes** |
| tensor, class C | c_T² = 1 at s = w = 0 | c_T² = 1 with positive energy on Minkowski (C0 and N1) | **yes** |
| background equation | from the a-equation (T0.4b) | V = (2 − 3gt)M_P²(2Ḣ + 3H²)/2 (CMV eq. 77) | **yes** |
| background multiplier | T0.4a: ε = −2λ = (3/8πG)(1 − 3gt/2)H² − V, i.e. λ = (1 − 3gt/2)M_P²Ḣ | λ̄ = (1 − 3gt)M_P²Ḣ (brute force; CMV eq. 80 mapped); CFG124's ε = −2λ̄ − 3gt M_P²Ḣ | **no** (the label only; see Side finding) |
| G2 pair | gt_max = 8.5e-11, c_s²,max = 4.2e-11 | consistent at the printed precision (the formula gives 4.25e-11 at 8.5e-11) | **yes** |
| G1.2 count | 0 of 2624 = 164 x-points × 2 footings × 4 masses × 2 profiles | 0 of 1600 = 200 x-points × 2 footings × 4 masses (point mass only) | **yes** (point-mass half) |
| fall-time range | 0.003–3.7 Gyr (table: 0.003 … 3.69) | 0.0031–3.765 Gyr for x in [0.3, 30]; 0.0032–3.6905 Gyr on CFG124's grid (post-hoc) | **yes**, after the grid is matched |

**How the two derivations differ:**
- CFG124 wrote the ADM form of the Einstein–Hilbert term by hand. It checked the ADM identity only on the FRW background (T0.1) and □φ = −K at N = 1 (T0.2b). It fixed N = 1 before varying, and read the kinetic sign from the ζ̈ coefficient of the EOM (this is valid: K = −A/2 with sympy's EL sign).
- CFG124's T0 "MUTATE(b)" compares two formulas; it does not re-derive from a flipped action. My MUTATE a re-derives from the flipped action and gets −gt/(2 + 3gt), the expression that control only asserted.

## Results (main runs)

**M1, Minkowski** (φ = t, λ = 0, V = 0, an exact solution: all first-order EL terms vanish).
- **The matrix:** for (Φ, B, Ψ, E, δφ, δλ, h) it is Hermitian and the tensor mode decouples. For example:
  - M[B,B] = M_P² gt k⁴;
  - M[B,Ψ] = i M_P² k² ω(3gt − 2);
  - M[Ψ,Ψ] = M_P²(9gt ω² + 2k² − 6ω²);
  - M[h,h] = M_P²(ω² − k²)/2.
- **Step (i), gauge:** the gauge vectors (iω, 1, 0, 0, −1, 0, 0) and (0, iω, 0, −1, 0, 0, 0) are exact null vectors.
- **Step (ii), dispersion:** det(unitary) = det(Newtonian) = 8M_P⁴k⁴[(2 − 3gt)ω² − gt k²], with ratio exactly 1. There are no zero roots for gt ≠ 0.
- **Step (iii), reduction:** eliminating δλ, Φ and B gives M_red = 2M_P²[(3 − 2/gt)ω² + k²]. So K = −2M_P²(2 − 3gt)/gt (ratio to −(2 − 3gt)/gt: 2M_P²).
- **H-c, as sympy sets:** ghost (0, 2/3); gradient (−∞, 0) ∪ (2/3, ∞); healthy ∅; superluminal (1/2, 2/3).
- **H-c end points:** K → −∞ as gt → 0⁺ and +∞ as gt → 0⁻; K(2/3) = 0; c_s² → ±∞ at 2/3∓.
- **N1**, all 24 points pass:
  - gt in {8.5e-11, 0.01, 0.2, 0.4, 0.55, 0.65}: real roots with ω²/k² equal to the formula to ≤ 4.4 × 10⁻¹⁶ (2.7 × 10⁻⁵¹ with mpmath at 8.5e-11). The null space is 3-dimensional with exactly one nonzero restricted eigenvalue, and the Krein sign is −1 at every real root.
  - gt in {−1, −0.2, −0.01, 0.7, 1, 3}: imaginary roots with |Im ω|/k = √|c_s²| to ≤ 2.2 × 10⁻¹⁶.
  - The tensor mode has ω² = k² with sign +1 at every point.

**M2, flat FRW** (a(t) arbitrary, V(φ) general).
- **Background:** λ̄ = (1 − 3gt)M_P²Ḣ and V = (2 − 3gt)M_P²(2Ḣ + 3H²)/2. The δφ first-order term vanishes identically (the Bianchi identity).
- **Route U:**
  - δλ multiplies a³Φ, so Φ = 0.
  - After integration by parts, B has no time derivatives: the B² coefficient is M_P² gt k⁴a/4 and the BΨ̇ coefficient is M_P² k²(2 − 3gt)a²/2.
  - The reduced Lagrangian is (M_P² a³/2)(3 − 2/gt)Ψ̇² + (M_P² a/2)k²Ψ², with no mass term. This is FGM eq. 24 with the x-average factor 1/2, and it gives c_s² = gt/(2 − 3gt).
- **Route N:**
  - The δλ equation gives Φ = δφ̇, and the traceless combination 3E_eq/k² − Ψ_eq = M_P² k² a(Φ − Ψ) gives Ψ = Φ.
  - The 0i (B) equation becomes δφ̈ + Hδφ̇ + (c_s²k²/a² + Ḣ)δφ = 0, which is CMV eq. 81.
  - The Ψ, E and δφ equations are then satisfied identically.

**S, point mass:**
- S0: u^ν∇_ν u_μ − ½∂_μX = 0 identically on a general 2-D metric, so the flow is geodesic on X = −1 for any V and γ.
- t_fall rises monotonically with x0.
- The analytic t_fall agrees with the integrated radial ODE to 4.2 × 10⁻¹⁰.
- 0 of 1600 cases have t_fall ≥ 10 Gyr. The range is 0.00359–3.765 Gyr (canonical) and 0.00312–3.266 Gyr (alt).

## Controls

- **C0 PASS.** GR alone (Newtonian gauge) has scalar det −4M_P⁴k⁴, with no root in ω. The GR tensor mode has M_hh = M_P²(ω² − k²)/2: c_T = 1 and positive energy.
- **C1 PASS** (the higher-derivative term off, gt = 0, any V):
  - M1: det = 16M_P⁴k⁴ω² in both gauges (only ω = 0).
  - M2 route U: no B² term, and B multiplies M_P² k²a²Ψ̇, so Ψ̇ = 0.
  - M2 route N: δφ̈ + Hδφ̇ + Ḣδφ = 0.
- **C2 PASS** (CMV 2014, arXiv:1403.3961, under the declared map γ_CMV = gt, λ → −λ): eqs. 77, 80, 81 and 82 are reproduced exactly.
- **C3 PASS** (FGM 2017, arXiv:1703.02923): eq. 24 is reproduced exactly (A, the gradient term, no mass term), and eq. 26 follows.
- **C4 FAIL as frozen, kept.** The canonical scalar (one field) returned no Krein sign for s = ±1.
  - **The cause** is a defect in the frozen zero test, "below 10⁻⁹ of the largest singular value". A 1×1 matrix has only one singular value, which is also the largest. So at a numerically computed root (ω = 1 ± 10⁻¹⁶) the matrix is never "zero".
  - **The physics matrices are unaffected:** they are 7×7, the other fields set the scale, and N1 finds the 3-dimensional null spaces and signs as frozen.
  - **POST-HOC C4b** (not counted): the same scalar plus a decoupled algebraic field gives Krein signs +1 and −1 as expected. Within N1, the tensor mode (+1) and the scalar (−1) show both signs from the same code.
  - C4 alone makes M1's main run exit 1.

## MUTATE

- **MUTATE=a** (−(γ/2)(□φ)²).
  - M1 gives c_s² = −gt/(2 + 3gt) and a ghost set (−2/3, 0). M2 gives the same.
  - Every H-a, H-b and H-c window line fails, and so do N1, C2 (all four equations) and C3. C0 and C1 still pass.
  - Exit 1 in both scripts.
- **MUTATE=b** (γ(□φ)²): c_s² = gt/(1 − 3gt) and a ghost set (0, 1/3); the same lines flip. Exit 1.
- **MUTATE=1** (−γ(□φ)²): c_s² = −gt/(1 + 3gt) and a ghost set (−1/3, 0). Exit 1.
- **MUTATE=s:** with the target's own hydrostatic support, 1600 of 1600 cases survive, so S flips. Exit 1 (and for MUTATE=1 in S).
- **No MUTATE failed to change the headline.**
- **Limitation:** modes a and b re-parametrise the same family (gt → −gt, gt → 2gt). So the line "the healthy set is empty" never flips; it holds for the whole family. No declared MUTATE shows that this line can flip.

## Side finding (post-hoc, `cfg152_posthoc_T04_lambda.py`; not a CFG152 pass line)

- **What CFG124 wrote.** In T0.4, CFG124's background Lagrangian writes the γ term as (γ/2)Na³(9H²/N²), i.e. □φ = −K with K = 3H/N.
- **What □φ is.** For φ = t and a lapse N, □φ = −3H/N² + Ṅ/N³ (checked). The two agree only at N = 1, but the λ equation is the N-variation.
- **Consequences:**
  - CFG124's Lagrangian gives λ = (1 − 3gt/2)M_P²Ḣ. The covariant form gives (1 − 3gt)M_P²Ḣ, which is my M2 brute force and CMV eq. 80.
  - The a-equation is the same in both.
  - CFG124's printed ε = (3/8πG)(1 − 3gt/2)H² − V equals −2λ̄ − 3gt M_P²Ḣ exactly. That is the conserved first integral and the momentum-density coefficient of CMV eq. 78, not −2λ̄.
- **Effect:** only the label "eps = −2 lam" in T0.4a is wrong, and only for gt ≠ 0.
  - T0.4b (conservation iff V is constant) uses the right-hand side and stands. G2.2 uses T0.4b for class B at gt = 0 and stands.
  - T0.6 fixes N = 1 before varying, so the headline is unaffected. I did not check other uses beyond a search of CFG124's scripts.

## Disclosed departures and first-run failures

1. **M1, first main run.** It failed C4 and nothing else. It is kept as `cfg152_M1_minkowski_FIRSTRUN.out`/`_results.json`.
   - A first attempted fix (`<` → `<=` in the zero test) was wrong about the cause. Its run also failed C4, and its output was overwritten. The edit was reverted, so the reported main run uses the frozen test.
   - The reported run differs from FIRSTRUN only by the two POST-HOC C4b lines (checked by diff).
2. **M2, first main run: it crashed** after the background step. sympy's `euler_equations` silently drops identically zero equations, and that misaligned a zip with the field list.
   - Nothing past the background equations and three checks had run. The crash happened before the output was written, so it is not saved.
   - It was replaced by an explicit Euler–Lagrange sum. I validated that sum against sympy's own on a test Lagrangian before the reported run.
3. **Route N wording.** The spec says the Φ–Ψ relation comes "from the E equation". The E equation alone contains no undifferentiated Ψ, because ∂_i∂_j of the traceless operator vanishes. The relation came from the traceless combination 3E_eq/k² − Ψ_eq, which is derived from the parametrisation, not assumed.
4. **The N1 threshold for the restricted form.** Its nonzero eigenvalue is counted relative to the form's own largest |eigenvalue|. The spec's "largest singular value" was written for M's null space.
5. **Per-script MUTATE=1.** In M1 and M2 it means a and b together. In S it means s.
6. **The S range row stays "not at the printed precision", as frozen** (3.765 is outside [3.65, 3.75)). It was resolved post-hoc from CFG124's grid, `geomspace(0.05, 40, 240)`, whose scored points run from x = 0.308 to 29.41.
7. **Two post-hoc scripts** were written after all frozen runs and after reading CFG124's code. They add no pass line and change no exit code of the frozen runs.

## Independence

**Independent:**
- I wrote and ran all code before opening any CFG124 script or output: main and MUTATE runs a, b, s and 1.
- The expansion is my own. It uses no ADM identity and no linearised Einstein–Hilbert formula from memory.
- The Minkowski route and the Newtonian-gauge route N are methods CFG124 did not use.
- The sign is shown with a gauge-invariant (Krein) test as well as from reduced actions.

**Where independence stops:**
- The action, its sign conventions and gt = 8πGγ are CFG124's, taken as given.
- The answer was known in advance: from the request, CFG124's README and the literature. The drafting hand calculations are disclosed in the spec.
- Route U uses CFG124's gauge, with a different computation.
- Both lanes use sympy (1.13.1 here). A shared library bug would be caught only by the numpy and mpmath numerics and the literature controls.
- Both lanes were written by AI agents in the same programme.
- For S, the target, a0 values, x range and 10 Gyr line are shared, and the post-hoc row uses CFG124's grid.
- The literature was read through a fetch tool that summarises pages. Every quoted equation used here was reproduced exactly by my derivation.

## Untested (declared)

- Stability beyond linear order.
- Whether a ghost with a cutoff is tolerable (arXiv:1601.05405).
- The Hamiltonian or DHOST constraint analysis.
- Backgrounds other than Minkowski and flat FRW: halo interiors, anisotropic backgrounds, or baryons as a second fluid.
- The vector sector, and the tensor sector on FRW.
- CFG124's class D and E1 G5 lines, and its G1–G4 verdicts, apart from the point-mass half of G1.2.
- The exponential-sphere half of that row (CFG44's `Bcommon.py` was not imported, by instruction).
- Class C's density source in G1.2, and the C(r, 10 Gyr) test after crossing.
- The projectable Horava correspondence.
- Strong coupling near gt → 0 and near 2/3.

kappa = 1/2 and Omega_c h^2 stay fitted. Nothing here says the data favour either model, or that the theory is closed.
