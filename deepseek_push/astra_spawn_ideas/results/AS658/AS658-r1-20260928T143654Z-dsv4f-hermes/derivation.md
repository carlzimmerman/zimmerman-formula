# AS658 — Gauge invariance and local degree count of the k04 three-form vacuum

Run: `AS658-r1-20260928T143654Z-dsv4f-hermes`
Task pin: `e9a46a4d211b24a461bf047e4ed85c9c6e07d79965aae9ff49708c50773c81b1`
(seed `deepseek_push/astra_spawn_ideas/AS658_gauge_invariance_and_local_degree_count_of_a_three_form.md`,
executed verbatim; sha256 verified at start and recorded in `result.json`.)
Source cell (k04 kernel, pin `15c0a7e1…` from
`kappa_closure/k04_four_form_promotion_consistency.py`): **A** a three-form, **F = dA**,
**F = qε** with ε_{0123} = +1, ε^{0123} = −1 (mostly-plus), vacuum action
S = ∫ P(q) d⁴x over a flat contractible patch, P(q) = Z q²/2 + b β² q²,
a0 = β√(G|q|) (promotion), **κ = 1/2 ADOPTED** (FRAMEWORK_CONTRACT).

Every statement below is backed by the checked run outputs
(`derive_raw.out` 15/15 PASS, `numeric_raw.out` 14/14 PASS; bounded prototype
≤ 120 s / ≤ 512 MB / 1 thread — enforced with `/usr/bin/time -l` + single-thread env:
wall 1.10 s / 59.8 MB (derive), 4.51 s / 242.2 MB (numeric); measured, not declared).

---

## 1. Conventions and the index map (explicit, no tensor package)

- Parity `sgn(σ)` of a tuple = (−1)^{#inversions}; the 24 permutations of (0,1,2,3)
  and the 6 permutations of each triple are enumerated explicitly.
- Upper-index epsilon (mostly-plus η, ε^{0123} = −1): `eps_u(μ,ν,ρ,σ) = −sgn(μ,ν,ρ,σ)`
  if the tuple is a permutation of (0,1,2,3), else 0.
- Lower-index epsilon: ε_{μνρσ} = +sgn(μ,ν,ρ,σ) for permutations (ε_{0123} = +1).
- Norm check **D2b** (run): F_{μνρσ}F^{μνρσ} = −24 q² exactly (each of the 24 ordered
  index sets contributes −q²) — pins the two epsilon conventions against each other.
- Exterior derivative, 4-form component (24-term antisymmetrized form, with the 1/k! = 1/6
  prefactor and argument-order parity — verified on concrete fields:
  (dA)_{1023} = −(dA)_{0123}):

  (dA)_{μνρσ} = (1/6) · Σ_{π∈S₄} sgn(π) sgn_arg((μ̂,ν̂,ρ̂,σ̂)) ∂_{π₀} A_{π₁π₂π₃}

  where sgn_arg is the parity of the argument tuple relative to ascending index order,
  i.e. the component is antisymmetric in **all** slots. Sympy check D1/D1b/D2 uses this
  component object for every component.

## 2. D1/D1b — Gauge invariance (factor-by-factor)

A generic gauge parameter **B** (six independent component functions B_{ij}(x), i<j)
gives the shift A → A + dB with

  (dB)_{ijk} = (1/2!) Σ_{π∈S₃} sgn(π) sgn_arg ∂_{π₀} B_{π₁π₂},   (d(dB) = 0).

Run check **D1**: F(A + dB) − F(A) = 0 identically (sum of squared component
differences = 0, generic B, all four components): d² = 0 at the level of explicit
components. Consequently the flux amplitude q = F_{0123} is invariant, **D1b**:
q(A + dB) = q(A), δq = 0 identically. Because S = ∫P(q), δS = 0 along gauge
directions: full action invariance, not only flux invariance.

## 3. D2 — q as a functional of A

With F = qε the single independent component is F_{0123} = q, hence

  q = (dA)_{0123} = ∂₀A₁₂₃ − ∂₁A₀₂₃ + ∂₂A₀₁₃ − ∂₃A₀₁₂ ,   and

  q = −(1/4!) ε^{μνρσ} F_{μνρσ} = (1/3!) ε^{μνρσ} ∂_μ A_{νρσ},

the second form using 4! = 4·3!, i.e. the 1/3! factor is **derived** from the 1/4!
normalization of the dual amplitude. (Run: exact equality, printed expression.)

## 4. D3/D4 — First variation: integration by parts and the EOM

With P_q := dP/dq = (Z + 2bβ²) q (strictly increasing since Z, b, β² > 0):

  δS = ∫ d⁴x P_q δq ,   δq = δ(dA)_{0123} .

On the flat patch, integration by parts is checked exactly in **D3** (component form,
residual 0) and yields the four Euler–Lagrange densities — one per independent
component of A, μ = complement of {ν,ρ,σ}:

  EOM_{νρσ} := δS/δA_{νρσ} = −sgn(μ,ν,ρ,σ) · ∂_μ P_q ,   **no 1/6, exact signs**:

  EOM_{(123)} = −∂₀P_q ,  EOM_{(023)} = +∂₁P_q ,  EOM_{(013)} = −∂₂P_q ,  EOM_{(012)} = +∂₃P_q .

(D4 in run output; the residual of the IBP identity D3 is exactly 0; the signs were
cross-checked for each of the four triples by direct component variation.)

**The EOM map is invertible** (D4b): the matrix M mapping
(∂₀P_q, ∂₁P_q, ∂₂P_q, ∂₃P_q) to (EOM₁₂₃, EOM₀₂₃, EOM₀₁₃, EOM₀₁₂) equals
diag(−1, +1, −1, +1), a k-independent signed permutation with det M = **+1**.
Therefore

  EOM = 0   ⟺   ∂_μ P_q = 0 (μ = 0..3)   ⟹   P_q = const   ⟹   **q = const in the bulk**
  (Z + 2bβ² > 0).

Substitution controls (run): **D4c** q = q₀ (const) solves all four EOM identically;
**D4d** q = Q(x₀) does **not** solve the EOM: residual = −(Z + 2bβ²) Q′(x₀) ≢ 0.

## 5. D7 — No wave operator, zero propagating modes (local degree count)

The EOM couples only first derivatives of P_q and contains **no second derivative of
P_q** (max derivative order in A is 2, because q = dA; order in P_q is 1). The symbol
map ∂P_q ↦ EOM is the same matrix M for every momentum k (D7: det M = +1 for every k;
numeric N4c same): no root ω(k), no characteristic variety, no dispersion relation.
There is no operator that *propagates* the flux.

Degree count (D7b, standard p-form count, Duff–van Nieuwenhuizen 1980):
4 independent components of A − 3 gauge redundancies (δA = dB, d(dB)=0)
− 1 constraint-scalar condition (EOM forces q = const) = **0 propagating local degrees
of freedom**; C(d−2, p) = C(2,3) = 0. The only leftover freedom is the patch-boundary
value q₀ (integration datum). This is the **vacuum-sector gate**: the static count
(AS056, rank 2 — Einstein channel) does *not* certify propagation; here the bulk
distinguishes static from propagating outright: the EOM symbol has rank 4 and det
±1 with **no** momentum dependence, so no mode can carry energy at any k.

## 6. D5a/D6 — Second variation: gauge directions are null

q is linear in F ⇒ δ²q = 0, δ²S = (Z + 2bβ²) ∫ (δq)² (D5a: q(a/2) = q(a)/2 exactly).
Plane wave â_{νρσ} = i(k∧b̂)_{νρσ}:

  L(k) := (1/6) ε^{μνρσ} k_μ â_{νρσ}.

**D6** (run, exact): for â = k∧b, L(k) = (1/6) ε^{μνρσ} k_μ k_ν b_{ρσ} = 0 identically —
every b-term cancels pairwise (symmetric k_μk_ν × antisymmetric ε). Gauge directions
are null directions of δ²S. Numeric Hessian-symbol check N4a: rank 1 at four generic
momenta including k with k² = 0; N4b: the altered 4-scalar symbol has rank 4 (all four
component modes propagating) — control fires.

## 7. D8 — Vacuum energy, κ, and the free coefficient ratio

- **D8a**: vacuum energy density ε_vac = q P_q − P = (Z/2 + bβ²) q² > 0 (k01 sign
  reversed per the k04 F1 amendment).
- **D8b**: κ² = β²/(Z/2 + bβ²) — independent of q₀ (follows from a0² = β²G|q| and the
  promotion normalization κ² = a0²/(G ε_vac)|q=q_* residuum; run-exact):
  κ² = 2β²/(Z + 2bβ²).
- **D8c**: κ = 1/2 (ADOPTED) ⟺ Z/β² = 8 − 2b. The ratio Z/β² is **not** determined by
  any of these equations (N6b: Z/β² = 7.96398921 for the K_B = 0 tuned cell
  b = (2−K_B)·I_rar/(16π) = 0.018005394, I_rar = 0.452524896675130542 stable to
  rel. 2.9e−31 from dps 30 → 60); the "8" stays free — k04 F2 stands. Nothing in this
  seed fixes Z/β²; κ = 1/2 remains an input.

## 8. Numeric controls (independent representation, real residuals)

Flat 4-torus [0,L)⁴ (same derivative structure as the contractible patch), L = 2,
grids N = 17 and N = 25, second-order centered differences, periodic wrap. All checks
compare **actual residuals**, never booleans:

- **N1** gauge invariance on grid: max |q(A+dB) − q(A)| = 6.93e−14, max component
  |dF| = 7.46e−14 (machine zero).
- **N2** EOM: q ≡ const residual = 0.000e+00 (< 1e−12); **negative control**: q =
  q₀(1 + 0.3 sin x₀) residual = 7.364e−05 (> 1e−8) — the control fires.
- **N3** independent representation: field-space finite-difference derivative
  dS/dA_{νρσ} of the discrete action (with the cell volume h⁴) vs the closed-form EOM
  at 8 (component, cell) probes: max |FD − EOM·h⁴| = 5.9e−09 — the EOM is not asserted,
  it is re-derived from the action in a second, independent way.
- **N4a/N4b/N4c** Hessian/EOM symbols: rank 1 vs rank 4 vs det = +1 (k-independent).
- **N5a–N5d** altered-model controls (all fire): altered EOM dP/dq = 0 has only q = 0
  (vacuum destroyed: ε = 0, a0 = 0, κ undefined); a 4-scalar deformation of the flux
  violates the **original** EOM (residual 1.16e+03); an altered 4-scalar Lagrangian
  violates gauge invariance (|dL|/|L| = 28.1) while the true P(q) is invariant
  (0.000e+00).
- **N6a–N6d** footings and refinement: I_rar stable (N6a); κ = 1/2 tune (N6b);
  canonical vs alternative footing kept **separate** (N6c): canonical a0 = 9.3619e−11
  m/s² ⇒ ρ_L = 5.844412e−27 kg/m³, ε_L = 5.252696e−10 J/m³, s = c√(Gρ_L) = 1.872380e−10
  = 2 a0 (units: [Gρ_L] = s⁻², √·c = m/s² ✓); alternative a0 = 1.1279e−10 m/s² gives
  κ_eff = 0.60238840 at fixed ρ_L — i.e. the two footings are **not** interchangeable
  with a shared (ρ_L, κ); at fixed κ = 1/2: ρ_L′ = 8.483090e−27 kg/m³,
  q_*′ = 1.380600e−05/β. N6d: EOM const residual stays 0 at N = 25.
- Constants: G_N = 6.67430e−11, c = 299792458, M_sun = 1.98847e30,
  pc = 3.085677581491367e16 (SI); G_bare / G_cosmo **not** used (single-G promotion is
  k04's own cell — separation left to its own seed, sibling AS651 territory).

## 9. Lean 4 certificate

`AS658_three_form_gauge_count.lean` (run dir), compiled with
`cd fable_independent_2026/lean_2026 && lake env lean <abs>.lean` — **exit 0, zero
`sorry`**; `#print axioms` for every theorem ⊆ {propext, Classical.choice, Quot.sound}
(`lean_axioms.out`). Theorems:
`eom_invertible` (EOM ⟺ ∂P_q = 0 via the signed-permutation map, det = +1),
`eom_components` (explicit symbol diag(−1,1,−1,1)),
`eb_antisym`, `double_sum_swap`, `pointwise_step`, `symm_contract_zero` (d² = 0 core:
symmetric factor × antisymmetric kernel vanishes — summation-swap proof),
`gauge_null_plane_wave` (explicit plane-wave nullity, ring).
Compile host only; no files written into `fable_independent_2026/lean_2026/`.

## 10. What this does NOT establish (limitations)

- Flat contractible patch / periodic torus: boundary-of-patch terms are dropped;
  topology (noncontractible cycles, gluing of q₀ across patches) not treated.
- The count bounds the **vacuum** sector. Whether the fluctuation sector δA develops
  a wave operator once the promotion term a0 = β√(G|q|) is varied (or external sources
  are added) is not answered here — the Hessian symbol computed (N4a) is the P(q)-only
  symbol.
- κ = 1/2 is an input, not derived (the Z/β² = 8 − 2b matching condition is a
  constraint on coefficients, not a derivation of the 8).
- Double-precision numerics on 17⁴/25⁴ grids, centered differences of order 2; the N3
  FD-vs-closed agreement was measured at N = 17 only (N6d refines N2's residual, not N3).
- AS056's static Einstein-channel count and AS057's dimension dependence are upstream;
  this seed is their wave-sector complement: it shows the vacuum has no propagating modes
  but does not by itself certify propagation in any channel.

## 11. Next unresolved implication

The vacuum sector is closed (0 propagating DOF); the first missing bridge is the
**fluctuation-sector gate**: does the promotion term make δS acquire a wave operator for
δA (Hessian symbol at generic k with the a0-variation included), and how does the single
patch modulus q₀ glue into the ambient cosmology that fixes a0 = κc√(Gρ_Lambda)?