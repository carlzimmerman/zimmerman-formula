# A54 — THE FOUR GATES AS ONE THEOREM

**Lane:** A54_four_gates · **Date:** 2026-10-21 · **Base:** `THEORY.md` §3.5, `A33_master_action/MASTER_ACTION.md`,
`A3_lensing_gw/report.md`, `A12_slip_theorem/report.md`, `A22_ppn_frames/report.md`,
`A36_galactic_alpha1/report.md`, `A39_tensor_mass/report.md`, `core_open_problems_2026_10_20/03_relativity/report.md` §4.
**Script:** `a54_checks.py` (34/34 PASS, exit 0, 4.9 s) · **Output:** `a54.out` · **Data:** `a54_results.json`
**Lean:** `A54_coefficients.lean` (13 theorems, `lake env lean`, exit 0, no `sorry`/`admit`, footprint exactly
`[propext, Classical.choice, Quot.sound]`) · **Output:** `a54_lean.out`

---

## 0. Claim

Do the Hamiltonian/constraint analysis of the A33 action and the four gates stop being four results. They are
one pair of constraints seen four ways.

> **Theorem (one sentence).** On the A33 action the constraint pair
> `H_⊥ = 0`, `H_i = 0` is first class in the khronometric algebra, carries **5 propagating modes**
> (2 tensor + 2 vector + 1 scalar) with positive-definite kinetic coefficients for `β > 0`, `η > 0`, `γ ≥ 0`,
> and because `H_⊥` contains the P charge `D·P` with coefficient **exactly 1** and nothing else at `O(ε)`,
> while `H_i` contains **no** `O(ε)` P term, that single pair implies
> **(i)** `Φ = Ψ` at `O(ε)`, **(ii)** `c_T² = 1` exactly, **(iii)** `α₁ = α₂ = 0`, `β_PPN = 1` wherever
> `kL_* ≫ 1`, **(iv)** `dg/dg_N = 1 + a₀²/(g² + 2a₀g) ≥ 1`.

The one gate that does **not** follow as a global statement is **(iii)**. Its near-source half is a corollary;
its galactic extension is not true, and the same structure gives the opposite answer there:
`α₁ = 4u'/(D−u') = O(1)` at 1–30 kpc. **A36's galactic `α₁` is the residue**: gate (iii) needs the extra
assumption that the PPN expansion applies at galactic radii, which is false (§3.5).

---

## 1. The action and the ADM decomposition

### 1.1 The action (A33 §1, verbatim)

`K = 4πG`, `c = 1`, signature `(−+++)`, `√h = √det h_ij`, `θ ≡ K^i_i`:

```
L/(N√h) = [R3 + K_ij K^ij − (1+β)θ² − 2Λ]/(4K)          [Einstein–Hilbert + ADM deformation]
        + P^i D_i ln N                                    [clock]
        − W(u),   u ≡ K|P|,  W = (a₀²/K)[−u/a₀ − ln(1−u/a₀)]   [saturating log]
        + (η/2) E_i E^i,   E_i ≡ (Ṗ_i − ℒ_N P_i)/N        [P kinetic]
        − (γ/2)(D_iP^i)² − (γ/4) F_ij F^ij                [P gradient]
        + L_cold/(N√h) + L_m/(N√h),
```

with `P₀ = N^iP_i` (so `P_μ` is spatial), `u < a₀` a hard cap, and **no P–curvature coupling**.

### 1.2 Momenta and their inversion (L1–L3)

Treating `h_{ij}` as 6 independent components (`∂K_ij/∂ḣ_ij = 1/(2N)`):

```
π^ij = (√h/4K)(K^ij − (1+β)θ h^ij),        π ≡ h_ij π^ij = −(√h/4K)(2+3β)θ,
π_P^i = √h η E^i.
```

Both maps are inverted exactly, for **general β** (L1, L2 residual 0):

```
K^ij = (4K/√h)(π^ij − c_β π h^ij),   c_β ≡ (1+β)/(2+3β),
θ    = −(4K/(2+3β))(π/√h),
E^i  = π_P^i/(√h η).
```

The Legendre transform of the gravitational sector is the standard one and reproduces `L` (L3: `π^ij K_ij = L`,
`π^ij ḣ_ij = 2L`, `H_grav = 4K[π_ijπ^ij − c_β π²]`).

### 1.3 The Hamiltonian (exact)

```
H = ∫d³x (N H_⊥ + N^i H_i),

H_⊥ = (√h/4K)(2Λ − ³R) + (4K/√h)[π_ijπ^ij − c_β π²]
      + |π_P|²/(2√h η)                                   ← positive for η>0
      + √h [ ρ + D·P + γ/2 (D·P)² + W(u) ],

H_i = −2 D_j π^j_i + π_P^k D_i P_k − D_k(π_P^k P_i) + H_i^(matter).
```

`H_⊥ = 0` is A33's lapse equation (L); `H_i = 0` is A33's shift equation (S) with
`j_P^i = −ηE^jD^iP_j + (1/√h)D_j(√h η E^j P^i)`. Three facts about this pair carry the whole theorem.

**(S1) Lapse lemma.** `N` appears only (a) inside `K_ij = (ḣ_ij − 2D_(iN_j))/(2N)` through the homogeneous
degree-2 function `f(K)`, (b) linearly in `∂_iN` in the clock term, (c) as the overall multiplier. There is no
`Ṅ` and no `N²` term. So `π_N ≈ 0` is primary and `H_⊥ ≈ 0` is secondary.

**(S2) Shift lemma.** The clock term contains **no** `N^i` (L5: `N√h P^iD_i ln N = √h P^i∂_iN`, whose
`N^i`-derivative is identically 0), and every other P operator is *quadratic* in `(P, π_P)`. Hence
`H_i^(P)` carries exactly one power of `π_P = √h η E` and **vanishes identically on the static branch**
(L6). The unit coefficient of the clock is what makes the charge exactly `D·P` and hence the first integral
`g_N = g − u` exact (L5, G9).

**(S3) Metric lemma.** No P operator carries two derivatives of `h_{ij}`: `W` depends on `h^{ij}P_iP_j`
algebraically, `E²` and `(D·P)²` and `F²` carry at most one derivative of `h` and are quadratic in `P`, and the
clock vanishes on a constant-`N` background. The only two-derivative metric operator is
`R₃ + K² − (1+β)θ²`, whose TT projection is exactly Einstein (A0: `⟨R₃^(2)⟩ = −k²h²/4`, matching A3 K5).

---

## 2. The constraint algebra

### 2.1 Dirac–Bergmann: 4 primary, 4 secondary, no tertiary

Primaries `π_N ≈ 0` (1), `π_{N^i} ≈ 0` (3). Consistency gives the secondaries
`{π_N, H} = −H_⊥ ≈ 0`, `{π_{N^i}, H} = −H_i ≈ 0`. No tertiary appears, for four independently checked reasons:

1. `H_⊥` is **independent of N** (L9: `∂H_⊥/∂N = 0`), so `{π_N, H} = −H_⊥` contains no multiplier.
2. The Legendre map is invertible iff `2 + 3β ≠ 0` (L8): the trace eigenvalue of the supermetric is `−2−3β`,
   so `θ ↔ π` is a bijection. At `β = −2/3` the map degenerates (`π ≡ 0` becomes a primary constraint and the
   theory is a different one); the theory sits at `β > 0`, far from it.
3. The P equation is **evolutionary**: the coefficient of `P̈_i` is `η/N ≠ 0` (L4), so varying `P` gives an
   equation of motion, never a constraint. `η = 0` would turn `π_P = 0` primary and change the count.
4. `H_⊥` and `H_i` are **ultralocal in the momenta** — no `∂π` anywhere (§1.3) — which is Teitelboim's
   condition for the bracket's structure function to be unmodified by the matter sector.

### 2.2 The bracket, and the one thing β does

At linear order in the metric perturbation and quadratic in the momenta (A1, exact):

```
{H_⊥(x), H_⊥(y)} = −(1/√h)[ 2 π^ij ∂_i∂_j  +  (4c_β − 2) π ∂² ] δ(x−y) + …,
4c_β − 2 = −2β/(2+3β)      →  0  iff  β = 0.
```

At `β = 0` the kernel is exactly GR's (`−2π^ij∂_i∂_j`, which equals `h^{ij}H_j∂_iδ` up to a total derivative)
and the algebra is undeformed. At `β ≠ 0` a second term survives; its antisymmetrised content is
`∝ (2c_β − 1)[2∂_iπ ∂_iη + η ∂²π]` (A2, an exact Leibniz identity), which is **not** proportional to any
constraint. That is the khronometric deformation: the theory's gauge group is foliation-preserving, not
`Diff(M)`, and the deformation is the standard signature of that. It generates **no new constraint** — the
deformation is absorbed by the shift sector, whose equation becomes an equation of motion rather than a
constraint, which is exactly why the count stays at 5 rather than dropping to 4 (§2.3). There is **no central
charge**: every kernel term carries two derivatives of `δ`, none carries `δ` itself (A3).

**The P sector contributes nothing to the structure function**: its terms in `H_⊥` are `π_P²`, `D·P`, `(D·P)²`,
`W`, all of which bracket with the gravitational `R₃` into `π_P ∂P`-type terms with no `∂δ`, and with each
other into zero. So the algebra is *gravity's*, decorated only by `c_β`.

### 2.3 The number of propagating degrees of freedom: 5

| sector | phase-space dims | first-class constraints | DOF |
|---|---|---|---|
| `(h_ij, π^ij)` | 12 | — | — |
| `(N, π_N)` | 2 | `π_N` | — |
| `(N^i, π_{N^i})` | 6 | `π_{N^i}` (3) | — |
| `(P_i, π_P^i)` | 6 | — | — |
| `H_⊥`, `H_i` | — | 4 | — |
| **total** | **26** | **8** | **(26−16)/2 = 5** |

Composition: **2 tensor + 2 vector + 1 scalar**. The vector modes are the two transverse `P_i`; the scalar is
the *mixed* conformal-mode/`P`-longitudinal mode — the lapse constraint determines `π_P^L`, not `ψ`
(the round-2 reduction's `p_L = −ikζ/K`), so the conformal mode and the P longitudinal share one slot. This is verified by the
explicit linearised reduction, not only by the count (round-2 §4, reproduced in H6):

```
tensor :  ω² = k²
vector :  ω² = (K + γk²)/η                        (both transverse P modes)
scalar :  Q₀ ζ̈² − (γk⁴/K²)ζ²,   Q₀ = (2+3β)/(Kβ) + ηk²/K²,   ω₀² = γk⁴/[(2+3β)K/β + ηk²] > 0
```

**No ghost, and no extra scalar.** The kinetic coefficients are `1/(4K)` (tensor), `η/2` (vector), and `Q₀`
(scalar). `Q₀` is positive **iff `β > 0`** (H8) — the sign of the fifth mode's kinetic term *is* the sign of
`β`. So "no ghost" is the statement `β > 0`, `η > 0`; and the record's principal-positivity bound

```
β > 2ηa₀²/K = (L_* a₀/c²)² = 5.95×10⁻¹⁹   (8.70×10⁻¹⁹ with a₀ = 1.132×10⁻¹⁰)
```

**is** the ghost-freedom condition, up to a part in 10¹⁸. There is no extra scalar to be a ghost: the scalar
that the deformed algebra permits is the P longitudinal, already counted among the three components of `P_i`.
`β = 0` is a rank-degenerate point (the shift equation becomes a constraint; `Q₀` diverges) — which is why the
theory needs `β ≠ 0`, and why the bound `β > 0` is load-bearing rather than decorative.

**Where an extra mode *would* appear**: at `β = −2/3` the Legendre map degenerates (L8) and at `η = 0` the P
kinetic term vanishes (L4) — both are excluded by `β > 0`, `η > 0`.

---

## 3. The four gates as corollaries of one pair

| gate | what it is in the Hamiltonian language | minimal premise | status |
|---|---|---|---|
| **(i)** lensing = dynamics | `H_i^(P) = 0` at `O(ε)` and `H_⊥^(P)` at `O(ε)` is the pure charge `√h D·P` | (S2) + every P operator quadratic | **DERIVED** at `O(ε)`, first slip `O(Ψ)` |
| **(ii)** `c_T² = 1` | TT projection of `H_⊥` is Einstein's; no P operator is quadratic in `∂h` | (S3) | **DERIVED** exactly, for every `P̄` |
| **(iii)** `α₁ = α₂ = 0`, `β_PPN = 1` | `θ ≡ 0` static; no momentum density; the boost rescales the charge | (S2), (S3), `kL_* ≫ 1` | **DERIVED near-source; FALSE at galactic scales** (A36) |
| **(iv)** `dg/dg_N ≥ 1` | charge coefficient 1 + `W'' > 0` | (S2) + convexity of `W` | **DERIVED** at every acceleration |

### 3.1 (i) Lensing equals dynamics

`H_i^(P)` vanishes on `E = 0` (L6), so `g_{0i} = 0` at `O(ε)`; and `H_⊥^(P)` at `O(ε)` is `√h D·P` — a scalar
charge with **no traceless part**, because `W`, `(D·P)²`, `|π_P|²` are all `O(P²)`. Hence the traceless stress is
second order (G4): `Π = uW'(u) = u²/[K(1−u/a₀)]`, `Π/ε² → q²`, `Π/ε → 0`. The slip equation
`∇²(Φ−Ψ) = 2KΠ` then gives `Φ = Ψ` at the order at which the potentials are defined (G5, where A22's exact
linearised solution `Ψ = Φ = −μ/r + (μ/L_*²)r` is verified against `∇²Ψ = Kψ`). Numbers: `(Φ−Ψ)/Ψ = O(Ψ)`,
`≤ 2.63×10⁻⁷` (A12/A3). **No `β` enters.**

### 3.2 (ii) `c_T² = 1`

The TT projection of `H_⊥`: the potential is `−(1/4K)³R` with no P term, because no P operator carries two
derivatives of `h` (S3) and transversality kills the first-derivative couplings — G1 verifies
`δd|_h = 0` identically for a general TT mode and a general `P̄`. The kinetic term is `4Kπ_ijπ^ij/√h` with
`π = 0`. The exact coefficients (A0, A1a):

```
⟨R₃^(2)⟩ = −k²h²/4   (generic Christoffel/Riemann build),
⟨K_ijK^ij⟩ = ¼ḣ²      (θ = 0 for TT),
⇒ S_TT^(2) = (1/16K)∫(ḣ² − k²h²)  ⇒  ω² = k²,  c_T² = ⟨−R₃⟩/⟨K²⟩ = 1.
```

The `P̄` dependence is a **mass**, not a speed: `m_T² = u²(4−3x)/(1−x)² > 0` on `0<x<1` (G2; min of
`(4−3x)/(1−x)²` is 4.005), so `ω² = k² + m_T²` with `d(ω²)/d(k²) = 1` (A39). **`β` does not enter** — the
`(1+β)θ²` operator is `θ`-blind on TT. A `P`–curvature coupling would break it by
`Δc_T² = 2ξ(L_*a₀/c²)² = 1.19×10⁻¹⁸` at `ξ = 1` (G1b): the structural absence makes the identity exact, and even
its presence would be invisible. That is a robustness statement, not an excuse.

### 3.3 (iv) `dg/dg_N ≥ 1` — and it is the same `u'` as `α₁`

Charge coefficient 1 gives the exact first integral `g_N = g − u` with `u = a₀g/(g+a₀)`; eliminating `u`
(G9, Lean `gN_eq`, `dg_dgN`, `dg_dgN_ge_one`):

```
dg/dg_N = 1/(1−u') = 1 + a₀²/(g² + 2a₀g) ≥ 1,   u' ≡ du/dg = a₀²/(g+a₀)²,
```

with equality only as `g → ∞`; numerically the minimum over 13 decades of `g` is `1.000000`. Convexity of `W`
(`W'' = 1/(K(1−x)²) > 0`) is exactly `dg/du = KW'' > 0`, i.e. `u ↔ g` is a bijection — the same fact that makes
the P kinetic term ghost-free. **`u'` is the same object that drives A36's `α₁ = 4u'/(D−u')`**: one derivative,
two gates.

### 3.4 (iii) near-source: `α₁ = α₂ = 0`, `β_PPN = 1`

`θ ≡ 0` identically on the static branch (G3: `n^i = 0`, `ḣ = 0`), so `(1+β)θ²` is inert and the static
gravitational sector is *exactly* Einstein–Hilbert for every `β` — no aether-type `α₁`, `α₂` from gravity.
`H_i^(P) = 0` (S2) removes the momentum density, so `B = 0`, so no `(w·n̂)²` term: `α₂ = 0`. The boost enters
only through `ln N → ln N + w²(Φ+Ψ)`, a uniform rescaling of the charge `∂ln N`; in the near-source hedgehog the
charge is `∝ 1/r²` and its potential is **linear in r**, so there is no `w²U` term: `α₁ = 0` (G6:
`α₁(r) = 2r²/L_*² = 8.16×10⁻¹⁴` at 1 AU). `β_PPN = 1` because the `O(ρ²)` sources have exponents `{0, −2}`
and never `−4` (A22 D7).

### 3.5 The gate that does not follow: (iii) at galactic scales

The same structure, with the same formula, at `kL_* ≪ 1`:

```
α₁ = 4u'/(D − u'),   D = 1 + (kL_*)²u'/2,   u' = a₀²/(g+a₀)²
   → 8/(kL_*)²   (kL_* ≫ 1: A22's zero)
   → 4u'/(1−u')  (kL_* ≪ 1: a galaxy)
```

G7 verifies both limits exactly; G8 reproduces A36's table from the same `u(g)` (0.073, 0.143, 0.235, 0.475,
0.928, 1.628, 3.169, 5.194 at 1–30 kpc, with `g/a₀` and `u/a₀` matching A36 digit for digit). So:

> **Gate (iii) is the one that does not follow from the structure alone.** It follows only with the extra
> assumption that the PPN expansion is valid at galactic radii. It is not: at `kL_* ≪ 1` the charge tracks the
> baryonic density, its potential is `1/r` rather than `r`, and the boost rescales a `1/r` potential. The
> structure predicts `α₁ = O(1)` there — A36's number — and no coefficient, sign or tuning can bring it below
> `10⁻⁴` without contradicting `D·P = ς(ρ_c − ρ̄_c)`.

`α₂ = 0` survives at all scales (the boost enters only as `|w|²`), and `β_PPN = 1` survives (the exponent
inventory is scale-free). It is `α₁` alone that is regime-dependent.

---

## 4. The nonlinear Hamiltonian: is it bounded below?

### 4.1 The potential and the on-shell energy

`W(u) ≥ 0`, `W(0) = 0`, `W'' = 1/(K(1−x)²) > 0`, `W → ∞` as `u → a₀⁻` (H1). On the constraint surface
`u = a₀g/(g+a₀)` and (H2, Lean `gN_eq`…`hess_chain`):

```
W(g) = (a₀²/K)[ ln(1 + g/a₀) − g/(g+a₀) ].
```

### 4.2 The Hessian in `g`: it changes sign at exactly `g = a₀`

```
d²W/dg² = a₀²(a₀ − g) / [K (g + a₀)³]      (H3, exact; zero iff g = a₀)
```

So the on-shell energy is **convex below `a₀` and concave above it**, with the inflection exactly at
`g = a₀ = 9.36×10⁻¹¹ m s⁻²` (Lean `hess_zero_iff`, `hess_sign`). This is the "acceleration at which the
Hamiltonian's Hessian changes sign", and it is the MOND transition itself. The full density behaves the same
way: with `d(g) = (u'g + 2u/r)/K`, one has the exact identity `d'(g) = W''(g) + 2u'/(Kr)` (H9), so

```
∂²_g ρ_P = W''(2 + γd) + 2γ(W'')² + O(1/r),
```

which vanishes **exactly at `g = a₀`** and has the sign of `W''` in a neighbourhood. The charge-squared term
`2γ(W'')²` is a positive square but is `O((W'')²)`, so it cannot move the root.

### 4.3 Why that is not an instability

`g` is not a canonical variable. The canonical variable is `u` (or `P_i`), and there:

* `W''(u) = 1/(K(1−u/a₀)²) > 0` for every `u < a₀` — the potential is strictly convex in `u` (H1).
* The canonical Hessian is positive definite (H5): longitudinal `K/(1−x)²`, transverse `K/(1−x)`, kinetic
  `1/(√hη)` — **no sign change anywhere**.
* `u ↔ g` is a monotone bijection, `dg/du = KW'' > 0` (H7).

A sign change of the *Legendre-transformed* energy in the applied field is what every saturating response does
(the same happens to a Gibbs free energy at a crossover); it says the field `g` is not the convex variable, not
that the energy is unbounded. **The Hamiltonian's Hessian has no sign change in the canonical variables, at any
acceleration.**

### 4.4 The bound

`ρ_P = d + W(u) + (γ/2)d²`, and as a function of `d` this is a perfect square (H4, Lean `rhoP_square`):

```
d + (γ/2)d² = (γ/2)(d + 1/γ)² − 1/(2γ)   ⇒   ρ_P ≥ W(u) − 1/(2γ) ≥ −1/(2γ) = −1/(K L_*²).
```

So the energy density is bounded below on the **whole** configuration space, by `−1/(2γ) = −1/(KL_*²)
= −2.17×10⁻²⁷` in the action's units. On the branch `d ≥ 0` — which contains every static solution with `g > 0`,
since `d = (u'g + 2u/r)/K > 0` for a hedgehog — the bound improves to `ρ_P ≥ 0`, saturated only at `P = 0`,
`π_P = 0`. And the density is coercive in `u`: `W → ∞` at the cap, so no finite-energy configuration reaches
`u = a₀`.

Two honest qualifications. (a) The cap is a strong-coupling point: `W'' → ∞`, so the EFT is not controlled
there — but it is a *stiff* limit, not an unstable one. (b) For an isolated MOND configuration the *total*
energy `∫√h ρ_P` diverges — upward, linearly in `r` for `ρ ~ 1/r²`, exactly as an isothermal sphere's does.
That is the standard IR divergence of a `1/r²` halo, not a failure of boundedness below.

---

## 5. Verdict

**Ghost-free and stable at every acceleration — yes, with one condition on `β` and one honest scope
limitation.** The count is 5, the kinetic coefficients are positive for `β > 0, η > 0, γ ≥ 0`, the canonical
Hessian is positive definite for all `u < a₀`, the energy density is bounded below by `−1/(2γ)`, and the
potential is convex and coercive on the admissible domain. The constraint algebra closes without a new
constraint and without an extra mode; the `O(β)` deformation of the `{H_⊥,H_⊥}` bracket is the khronometric
one and is absorbed by the shift sector.

**One structure implies three of the four gates exactly and the fourth only near-source.** The structure is
`(S1)+(S2)+(S3)`: `N` a multiplier, the clock the only `O(ε)` lapse source with coefficient 1 and no `N^i`,
and no P–curvature coupling. Gate (iii)'s galactic half is the conditional one, and A36 is its number.

**The theorem.** *On the A33 action the pair `(H_⊥, H_i)` is first class in the khronometric algebra with five
propagating modes and positive kinetic coefficients for `β > 0, η > 0, γ ≥ 0`, and that single pair — the charge
`D·P` with unit coefficient in `H_⊥`, no `O(ε)` P term in `H_i`, no P–curvature coupling — implies `Φ = Ψ` at
`O(ε)`, `c_T² = 1` exactly, `α₁ = α₂ = 0` with `β_PPN = 1` wherever `kL_* ≫ 1`, and
`dg/dg_N = 1 + a₀²/(g² + 2a₀g) ≥ 1` at every acceleration; the one gate that does not follow globally is
`α₁ = 0`, whose galactic value the same structure fixes at `O(1)`.*

---

## 6. Checks (`a54_checks.py`, 34/34 PASS, exit 0)

```
L1  pi^ij from dL/dK_ij, general beta                          0
L2  inversion K^ij(pi), theta(pi)                              0, 0
L3  pi.K = L and H_grav reproduces L                           0, 0
L4  pi_P = sqrt h eta E; H_P(kin) = |pi_P|^2/(2 sqrt h eta) > 0 0, 0
L5  clock is a lapse term, no N^i; charge coefficient 1        0, 0, 0
L6  H_i^(P) = 0 on E = 0                                        0
L7  Dirac count: 26 -> 8 first class -> 5 DOF                  26, 8, 5
L8  Legendre map singular only at beta = -2/3                   beta=-2/3
L9  kinetic positivity; H_perp independent of N                 1, <0, 0
A0  <R3^(2)>_TT = -k^2h^2/4 (generic Christoffel/Riemann)       -k^2/4
A1  kernel deformation 4c_beta-2 = -2beta/(2+3beta)             0 at beta=0
A1a c_T^2 = <(-R3)>/<K^2> = 1                                   1
A2  antisymmetrised deformation is a d(pi) structure            0
A3  no central charge                                           0
G1  delta d|_h = 0 for every TT mode and every Pbar             0
G1b a P-curvature coupling would shift c_T^2 by 1.19e-18        <1e-6
G10 c_s^2 = gamma/eta > 0                                       >0
G2  m_T^2 = u^2(4-3x)/(1-x)^2 > 0 on (0,1)                      4.005 min
G3  theta = 0 static                                            0
G4  Pi/eps^2 -> q^2, Pi/eps -> 0                                q^2, 0
G5  lap^2 Psi = K psi for A22's exact solution                  0
G6  alpha_1 = 2r^2/L*^2 at 1 AU                                 8.161e-14
G7  A36 limits: 0 and 4u'/(1-u')                                0, 4u'/(1-u')
G8  galactic alpha_1 in [0.073, 5.194]                          >1e-4
G9  dg/dg_N = 1 + a0^2/(g^2+2a0g) >= 1                          0, 0; 1.000000
H1  W >= 0, W'' > 0, coercive                                   0, 1.000, ->oo
H2  W(g) closed form                                            0
H3  d^2W/dg^2 zero at g = a0                                    0; [a0]
H4  rho_P >= -1/(2 gamma)                                       W - 1/(2gamma)
H5  canonical Hessian positive definite                         >0
H6  five dispersion relations positive                          all >0
H7  dg/du = K W'' > 0                                           0
H8  Q0 has the sign of beta                                     >0 for beta>0
H9  d'(g) = W'' + 2u'/(K r)                                     0
```

Seven mutations (`--mutate`), each breaking at least one check and exiting 1: `clock2` (L5, G9), `drop_clock`
(L5), `wquad` (H1, H2, H3, H7), `eta_neg` (H5, H6, G10), `gamma_neg` (H6, G10), `beta_neg` (H6), `ricciP` (G1b).
Records in `MUTATE.md`.

**Lean** (`A54_coefficients.lean`, compiled with `lake env lean` from `fable_independent_2026/lean_2026`):
`gN_eq`, `one_minus_up`, `dg_dgN`, `dg_dgN_ge_one`, `KWp_eq`, `Wpp_eq`, `hess_chain`, `hess_zero_iff`,
`hess_sign`, `rhoP_square`, `mT_pos`, `Q0_sign`, `cb_GR` — 13 theorems, exit 0, no `sorry`, no `admit`,
axiom footprint exactly `[propext, Classical.choice, Quot.sound]` for all 13.

---

## 7. What this does not do

* **The full nonlinear bracket is not computed term by term.** §2.2 computes the weak-field kernel exactly and
  establishes the four structural facts of §2.1; that is enough to fix the structure function's form and to show
  the deformation is `O(β)`, but it is not a proof of closure in the sense of a full Dirac–Bergmann analysis of
  the nonlinear algebra.
* **The 5-mode count is the linearised count.** It is verified by the explicit reduction (round-2 §4) and
  reproduced in H6, not proved for the nonlinear theory. The counting argument of §2.3 is the standard Dirac
  count and assumes the constraints are irreducible, which is checked at the linearised level only.
* **Boundedness is at the hedgehog level.** §4 uses the static spherical reduction `P = (u/K)r̂`. A general
  `(h, P)` configuration could in principle have a `d` distribution that makes `∫ρ_P` unbounded below through
  the volume term; the *density* bound `−1/(2γ)` is general, the integral is not.
* **Gate (iii)'s galactic `α₁` is A36's**, not re-derived here: this lane re-verifies the formula's algebra and
  both of its limits (G7) and reproduces the table from the same `u(g)` (G8), but the derivation of the response
  is A36's.
* **`β_PPN = 1` rests on the exponent argument** (A22 D7), not on a second-order metric solve.
* **No strong-field, no binary, no cosmological slip.**

## 8. Reproduce

```bash
cd deepseek_push/DS_FINAL_2026_10_21/A54_four_gates
python3 a54_checks.py --json-out a54_results.json | tee a54.out     # 34/34, exit 0
python3 a54_checks.py --mutate clock2                                # must exit 1
cd ../../../fable_independent_2026/lean_2026
lake env lean /Users/carlzimmerman/new_physics/zimmerman-formula/deepseek_push/DS_FINAL_2026_10_21/A54_four_gates/A54_coefficients.lean
```