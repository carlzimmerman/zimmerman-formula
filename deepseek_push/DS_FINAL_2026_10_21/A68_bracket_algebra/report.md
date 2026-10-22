# A68 — THE CONSTRAINT ALGEBRA AND THE FIFTH MODE'S KINETIC TERM, COMPUTED

**Lane:** A68_bracket_algebra · **Date:** 2026-10-22 · **Replaces:** A66 (Route C, stub checks) and A67
(ghost diagnosis, circular mass).
**Base read:** `A54_four_gates/report.md` (the only count actually derived: 26 phase-space dims, 8 first-class,
`(26−16)/2 = 5`), `A66_dof_repair/report.md` **erratum** (Route C checks are stubs), `A67_ghost_diagnosis/report.md`
**erratum** (its mass is an input echo), and the frozen action in
`core_open_problems_round2_2026_10_20/03_relativity/report.md` §2.
**Script:** `a68_checks.py` — **39/39 PASS, exit 0** · **Output:** `a68.out` · **Data:** `a68_results.json` ·
**Mutations:** `MUTATE.md` (9 dials, each exits 1).

Action (frozen, `K = 4πG`, `c = 1`, signature `(−+++)`):

```
L/(N√h) = [R₃ + K_ij K^ij − (1+β)θ² − 2Λ]/(4K)
        + P^i D_i ln N − W(u) + (η/2) E_i E^i
        − (α/2)(D_i P^i)² − (γ/4) F_ij F^ij,
u = K|P|,  E_i = (Ṗ_i − ℒ_N P_i)/N,  F_ij = ∂_iP_j − ∂_jP_i,
W(u) = (a₀²/K)[−u/a₀ − ln(1−u/a₀)].
```

The frozen action carries **one** stiffness in front of both gradient operators (`α = γ`, forced: the ratio of
the two coefficients is exactly 2, check D16). It carries **two** independent coefficients `η` (kinetic) and
`γ` (gradient). That distinction is the whole of Task 3.

---

## 0. The answer in one paragraph

**Route C is dead, and the count is 5.** The bracket that A66 asserted to be non-zero at `O(ε²)` is
`{H_i(x), π_P^j(y)} = [π_P^j δ_i^k − δ_i^j π_P^k]∂_kδ(x−y) − δ_i^j(D·π_P)δ(x−y)`: **linear in the P momentum**,
with no `P` in it at all, and therefore **identically zero on the surface `π_P = 0` that the would-be P
constraint defines** — five independent configurations, maximum entry `0.0` (B3). A second-class matrix must be
non-degenerate *on* its own surface; this one is the zero matrix there. Its rank off the surface is 3 (or 2 when
`D·π_P = 0`, with the longitudinal direction in the kernel), but that is irrelevant to the count. There is also
no `φ_P` to pair with: the P Legendre map is invertible, `det = η³h^{3/2}/N³ ≠ 0` (A2), so varying `P_i` gives a
second-order equation, not a constraint — and A66's specific mechanism is absent from the action: the
coefficient of `P_iD_jP^j` in `H_i^(P)` is **exactly 0** (A5), because `H_i^(P) = π_P^kF_ik − (D·π_P)P_i` carries
exactly one `π_P`. The Dirac count is 26 phase-space dimensions, 8 first-class, 0 second-class, rank 0 →
**5 DOF**, identical to A54, with nothing reclassified. The fifth mode's kinetic coefficient is
`Z = Q = B + ηp²`, `B = K(2+3β)/β`; its mass at `H = 0` is **zero** (it is a `k⁴` mode, `ω² = αp⁴/Q`,
`c_s² = αp²/Q → 0`), and it is healthy for `β > 0`, `η > 0`, `α = γ > 0` — an **open set**. The action does not
force `η = γ`; A67's `m² = 2/L★²` is `K/η` with `η = KL★²/2` substituted, i.e. its own input read back, and
that mass belongs to the two **transverse** P modes, not to the fifth mode.

---

## 1. Task 1 — the bracket

### 1.1 There is no `φ_P`: the P Legendre map is invertible

`π_P^i = ∂L/∂Ṗ_i = √h η E^i`, and the Hessian is

```
∂²L/∂Ṗ_i∂Ṗ_j = (√h η/N) δ_ij ,        det = η³ h^{3/2}/N³ .
```

Computed symbolically and numerically at `√h = 2.3, η = 1, N = 1.7`: `det = 2.476491`, closed form `2.476491`,
residual identically 0 (A1, A2). The map is invertible for `η ≠ 0`, so `π_P^i = 0` is **not** a primary
constraint. The `P` equation is second order — the `σ̈` coefficient of the longitudinal mode is `ηp²`
(`0.490000` at `η = 1, p = 0.7`, A3) — so varying `P_i` produces an evolution equation. This is A54 §2.1's
point 3, here computed rather than quoted.

**Consequence.** A66's "`φ_P`, the P momentum constraint" does not exist in this theory. Whatever second-class
pair Route C needs, the action does not supply its second member.

### 1.2 What `H_i^(P)` actually is (A66's claimed term is absent)

The shift `N^i` enters the P sector only through `ℒ_N P_i`. Varying the P Lagrangian with `N^j` and its
gradients treated as independent jet variables — the Euler derivative `∂ℒ/∂N^j − ∂_k(∂ℒ/∂(∂_kN^j))`, evaluated
on a random polynomial configuration of degree 2 — gives, with residual **exactly 0** over all three components
(A4):

```
δS_P/δN^j = π_P^i F_ij + (D·π_P) P_j          ⇒     H_j^(P) = π_P^k F_jk − (D·π_P) P_j .
```

This is the exact `O(P²)` content of `H_i`. Two computed facts follow.

* **It is linear in `π_P`** — every second derivative with respect to `π_P` and `∂π_P` vanishes (A5).
* **The coefficient of `P_i D_j P^j` is 0** (A5). A66's mechanism ("`H_i` contains `P_iD_jP^j`, hence a
  non-zero bracket") is not merely wrong in magnitude: the term does not exist. Inserting it by hand
  (`--mutate pp_term`) makes A5, A6, B1, B2 and B8 fail, which is how the check set demonstrates that it is
  load-bearing.
* `H_i^(P) = 0` when `E = 0` (A6): the P part of the momentum constraint is a momentum flux, vanishing on the
  static branch — A54's L6, reproduced.

### 1.3 The bracket, computed

I computed `{h_i(x), π_P^j(y)}` in two independent ways:

1. **Mode algebra.** On a discrete Fourier lattice with `{q_a(k), π_b(k')} = δ_ab δ_{k',−k}`, the bracket is
   evaluated mechanically by the Leibniz rule on `h_i(k) = ∫_q [i(k−q)_i π_P^l(q) P_l(k−q) − i k_l π_P^l(q) P_i(k−q)]`.
   **9/9 components** reproduce the closed form (B1), and the same comparison at five random momentum pairs with
   random mode values agrees to `0.000e+00` with `|matrix|` up to `6.408` (B2).
2. **Diffeomorphism generator.** As a consistency check on the same object, `{h_i(x), P_k(y)} = F_{ki}δ + P_i∂_kδ`
   to 9/9 components (B8), i.e. `H_i^(P)` is the canonical generator of spatial diffeomorphisms — which is why
   the momentum constraints stay first class.

**Result.**

```
{H_i(x), π_P^j(y)} = [ π_P^j(x) δ_i^k − δ_i^j π_P^k(x) ] ∂_k δ(x−y)
                     − δ_i^j (D_k π_P^k)(x) δ(x−y)                     (equal time, flat background)
```

or, in Fourier form with `K = k + q` (verified 9/9):

```
{h_i(k), π_P^j(q)} = −i q_i π_P^j(K) + i q_k π_P^k(K) δ_i^j − δ_i^j (D·π_P)(K) .
```

**So: not identically zero, and not proportional to `D_jP^j`.** It is proportional to `π_P` — the P *momentum*
— with a derivative-of-delta part and an ultralocal part `∝ D·π_P`. There is no `P` in the answer: scaling
`π_P → λπ_P` scales the matrix by `λ` exactly (`1.8e−15` residual, B7), and the kernel does not depend on the
configuration of `P` at all.

### 1.4 Rank, spectra, transverse/longitudinal decomposition

The symbol is

```
M_i{}^j(k) = i[ π_P^j k_i − δ_i^j (π_P·k) ] − δ_i^j (D·π_P) ,
```

with `a ≡ π_P·k`, `b ≡ D·π_P`:

```
eigenvalues { −b + i a , −b + i a , −b } ,      det M = −b (b − i a)² .
```

Computed at `k = (0.7,−1.3,2.1)`, `π_P = (0.4,0.9,−1.7)`, `D·π_P = 0.85`: `a = −4.46`, `b = 0.85`, eigenvalues
`−0.85 − 4.46i` (double) and `−0.85` (B5, max deviation `9.9e−16`). In the orthonormal basis
`(k̂, e₁, e₂)` the matrix is upper triangular,

```
M = [[ −b , −i|k|π₁ , −i|k|π₂ ],
     [  0 , −b+ia  ,   0      ],
     [  0 ,   0     , −b+ia    ]]
```

with `(T,L) = 1.9e−16` and `(L,T) = (−i|k|π₁, −i|k|π₂)` nonzero (B6). `k̂` is always an eigenvector with
eigenvalue `−b`; the eigenvalue `−b+ia` is doubly degenerate and its eigenspace is the transverse plane only
when `π_P` is purely longitudinal.

**Ranks, computed:**

| configuration | rank |
|---|---|
| generic, `D·π_P ≠ 0` | **3** |
| `D·π_P = 0` (e.g. purely transverse `π_P`) | **2**, kernel = the longitudinal direction |
| **`π_P = 0` (the surface the pair would define)** | **0** |

Five independent configurations on `π_P = 0` give `max|M| = 0.0` exactly (B3).

### 1.5 Verdict on Route C

A pair of constraints `(φ₁, φ₂)` is second class iff the matrix of their brackets is **non-degenerate on the
surface where both constraints hold**. Here the only candidate surface is `π_P = 0` (which would also force
`D·π_P = 0`), and there the matrix is *identically zero*. The pair is therefore not second-class; it removes
nothing. Two independent reasons, each computed:

1. **No `φ_P` exists.** `det ∂²L/∂Ṗ∂Ṗ = η³h^{3/2}/N³ ≠ 0` (A2). One cannot pair a constraint that the action
   does not contain.
2. **Even if `π_P = 0` were imposed by hand, the pair is degenerate on its own surface** (B3): zero matrix, rank
   0. And the stated mechanism is absent: `H_i^(P)` has no `P_iD_jP^j` term (A5) and is linear in `π_P`.

The rank-2 count that A66's "removes one transverse mode" would need is realized only *off* the surface and only
when the ultralocal piece vanishes (`D·π_P = 0`, B4). It is not available where the count is taken.

**Route C is dead.** The honest version of A66's own conclusion is the opposite of its headline: the shift
constraint does not turn second-class against anything, and the shift's P-sector contribution vanishes on the
static branch.

**One contrast, so that the wrong bracket is not mistaken for the right one.** The bracket with the *scalar*
`D·P` — the constraint Route A imposes with a Lagrange multiplier — is a different object (B9):

```
{h_i(k), (D·P)(q)} = K_i (q·P(K)) − (q·K) P_i(K) + q² P_i(K)
```

linear in `P`, **containing no `π_P`**, so it does not vanish on `π_P = 0`. That is the pair Route A uses, and it
costs an action modification (a Lagrange multiplier for `D·P − q`); it is not a bracket the frozen action
supplies, and it is not Route C's. Whether Route A's pair is first-class — A66 asserts `(π_λ, φ)` is — is **not**
checked here; the only point of B9 is that the bracket Route C needs is not this one, and the count computed
here is for the frozen action alone.

---

## 2. Task 2 — the correct Dirac count

### 2.1 Every number and where it comes from

| sector | field components | phase-space dims | constraints | verified by |
|---|---|---|---|---|
| `(h_ij, π^ij)` | 6 (symmetric) | 12 | — | C1 |
| `(P_i, π_P^i)` | 3 | 6 | **none** | A2 (invertible), A3 (second order) |
| `(N, π_N)` | 1 | 2 | `π_N` (primary) | C2 (no `Ṅ` in `K_ij, θ, E_i`) |
| `(N^i, π_{N^i})` | 3 | 6 | `π_{N^i}` ×3 (primary) | C2 (no `Ṅ^i`) |
| `H_⊥` | — | — | 1 secondary | C3, C4 |
| `H_i` | — | — | 3 secondary | C3 |
| **total** | | **26** | **8 first class** | C1, C2, C3 |

`26 = 2(6+3+1+3)` computed from the field content, and independently as a sum over the sector table (C1). The
four primaries are computed, not declared: `K_ij`, `θ` and `E_i` are built with `N(t)`, `N^i(t)` as explicit
functions of time and **no `Ṅ` or `Ṅ^i` appears in any of them** (C2). The four secondaries are the lapse and
shift equations: `N` enters the P kinetic term only as the algebraic `1/N` of `E_i` — `d(N L_kin)/dN = 0`
identically (C3) — so `{π_N, H} = −H_⊥` and `{π_{N^i}, H} = −H_i`.

**No tertiary** (C4), from two computed facts: (i) the P equation is second order (A3), so it can be solved for
`P̈` and is not a constraint; (ii) `H_⊥` is independent of `N` — computed by Legendre-transforming the P sector,
`H_⊥ = |π_P|²/(2√hη) + √h (K/2)|P|²`, with `∂H_⊥/∂N = 0` identically — so the chain `π_N → H_⊥ → …` terminates.

**Second class: none.** The only block the P sector could contribute is the `(H_i, π_P^j)` block, and its rank
on the surface is 0 (B3, C5). `SC = 0`, rank of the second-class matrix `= 0`.

```
DOF = (D − 2·FC − SC)/2 = (26 − 2·8 − 0)/2 = 5 .                                (C6)
```

Cross-check, independent of the counting: the explicit mode content of the quadratic action is 2 tensor (TT) +
2 vector (transverse P, `ω² = (K+γp²)/η`) + 1 scalar (`ω² = αp⁴/Q`) = **5** (C6).

### 2.2 Comparison with A54

**I agree with A54: 26, 8, 5. I reclassify none of its eight first-class constraints.** What Route C would have
had to reclassify is specific: two of the three components of `H_i` (the "transverse" ones) would have to become
second class against two P constraints. Those P constraints do not exist (A2), and the bracket that would make
the reclassification is degenerate on the surface (B3). The arithmetic is checked both ways: with `SC = 2`,
`(26−16−2)/2 = 4`; with the computed `SC = 0`, `(26−16−0)/2 = 5` (C7).

### 2.3 Is the question ill-posed at this order?

**No — and the reason is a computed identity, not an ordering convention.** The bracket is *linear in `π_P`*
with no other field dependence (B7). Therefore "it vanishes on `π_P = 0`" is an identity at every configuration,
not a statement about a particular background or a particular order in `ε`. The `O(ε²)` pieces of `H_i` change
the *value* of the bracket off the surface; they cannot change its rank on the surface, because the surface
itself is `π_P = 0` and there the bracket is zero for any `(h, P)`.

Two honest qualifications. Neither supports 4:

* A54's `FC = 8` treats `{H_⊥, H_⊥}` as weakly zero at `β ≠ 0`. A54 §2.2 itself reports an `O(β)` deformation of
  that bracket with content `∝ (2c_β−1)(…)π∂π` which is **not** manifestly a constraint. I did not compute the
  full nonlinear closure of that bracket — it is out of scope here — so `FC = 8` is inherited, not re-derived.
  If that deformation broke first-classness, `FC` would drop to 7 and the count would become
  `(26 − 14)/2 = 6` if `H_⊥` left the constraint set, or `(26 − 14 − 2)/2 = 5` if it went second-class with one
  partner (both branches computed in C7). Neither is 4: the deformation cannot be cited for Route C.
* The count is the *linearised* count in the sense that the constraint surface is defined order by order; the
  number of propagating modes is not. Nothing in the computation above is background-dependent.

---

## 3. Task 3 — the kinetic coefficient from the action

### 3.1 The quadratic action, with the coefficients as they appear

Scalar sector at `H = 0`, `h_ij = δ_ij + 2ζδ_ij`, `N = 1+n`, `N^i = ∂^iψ`, `Y ≡ ∇²ψ`, `P_i = ∂_iσ`,
`p = |k|`. Derived piece by piece from the frozen action:

```
L/a³ = [ −3A(ζ̇ − Hn)² + 2A(ζ̇ − Hn)Y − βY² + 2p²ζ² + 4p²nζ ] / (4K)
       + p² n σ + (ηp²/2) σ̇² − ( (Kp² + αp⁴)/2 ) σ² ,          A ≡ 2+3β .
```

* `K_ijK^ij − (1+β)θ² = [−3Aζ̇² − 2Aζ̇Y − βY²]/N²` — computed symbolically (D1); at `Y = 0` this is
  `−3(2+3β)ζ̇²/N²`, which is A67's `−(2+3β)ḣ²/12` under `h = 6ζ`. **Negative for `β > 0`**: the conformal mode is
  the would-be ghost direction.
* `√h R₃ = 2(∂ζ)² + total derivative` → `+2p²ζ²/(4K)` (D2).
* Shift elimination: `∂L/∂Y = 0 ⇒ Y = (A/β)(ζ̇ − Hn)`, and substituting gives `Aζ̇²/(2Kβ) ≡ (C/2)ζ̇²`,
  `C = A/(Kβ)` (D3). The shift's contribution **cancels the negative conformal sign** for `β > 0`.
* Lapse equation at `H = 0`: `∂L/∂n = p²(ζ/K + σ)` — it contains **no `n`**, so it is the constraint
  `Z ≡ ζ/K + σ = 0` (D4), not an equation for `n`. This is why the scalar sector has one mode, not two.
* Imposing it (`ζ = −Kσ`, `ζ̇ = −Kσ̇`) gives, exactly (D5):

```
S⁽²⁾_scalar = (1/2) ∫ a³ [ (B + ηp²) σ̇² − α p⁴ σ² ] ,        B ≡ K(2+3β)/β .
```

Note the cancellation that makes this gapless: the `−Kp²σ²/2` from `W`'s quadratic term (the "mass" of the
longitudinal P) is exactly cancelled by the conformal gradient term, leaving `V = αp⁴` and nothing else (D5).

### 3.2 `Z`, `m²`, `c_s²`

With `S = (1/2)∫a³ Z σ̇² + …`, the canonical field is `σ_c = √Z σ`, and

```
Z  = Q = B + ηp² = K(2+3β)/β + ηp² ,                                    (D5, D6)
ω² = αp⁴ / Q ,        m² = lim_{p→0} V/Q = 0 ,      c_s² = ω²/p² = αp²/Q → 0 .   (D7, D8)
```

Numbers, all from the run: with `K = 4πG`, `β = 1`, `p = 0`: `Q = 5K = 4.193586e−09`; at `p = 1/L★` with
`η = KL★²/2`: `Z = 5.5K = 4.612945e−09`. With `K = β = η = α = 1`: `c_s² = 2.0000e−07, 2.0000e−05,
1.9960e−03` at `p = 10⁻³, 10⁻², 10⁻¹`. The fifth mode is a **`k⁴` mode**: `ω² = αp⁴/(B+ηp²)`, whose sound speed
vanishes in the IR. A54's `H6` dispersion `ω₀² = γk⁴/[(2+3β)K/β + ηk²]` is this formula in the `ζ` variable
(`ζ = −Kσ`, so `Q_σ = K²Q₀`); the two agree exactly.

**The mass that does exist is the transverse one.** The two transverse P components have, per component,
kinetic `η/2`, mass `K/2` (from `W''(0) = 1/K`, D14) and gradient `γp²/2` (from `F_ijF^ij = 2p²|P_T|²`, D17):

```
m_T² = K/η ,        c_T² = γ/η .                                        (D9)
```

### 3.3 Does the action force `η = γ`?

**No.** Computed, three separate ways:

* `η` and `γ` are independently observable. The map `(η, γ) ↦ (η, γ/η)` — the slope of `Q` in `p²` and the
  transverse sound speed — has Jacobian determinant `1/η ≠ 0` (D10); two different inputs give two different
  `c_T²` (in the run: two distinct values, which the `eta_eq_gamma` mutation collapses to one).
* The action **does** force `α = γ`: one coefficient multiplies both gradient operators, so their ratio is
  exactly 2 (D16). That is a symmetry of the operator content (the `−(γ/2)(D·P)² − (γ/4)F²` pair is one
  stiffness), not a relation to `η`.
* `η` appears only in front of `E_iE^i`; `γ` only in front of the gradients. No term contains both.

**So A67's `η = γ = KL★²/2` is an extra assumption**, and its `m² = K/η = 2/L★²` is that assumption read back:
with `η = KL★²/2` the identity is exact (`3.646754e−36 = 3.646754e−36 m⁻²`), and with `η = 3KL★²/2` the "prediction"
becomes `0.333 × 2/L★²` (D13). It is also the **transverse** mass, not the fifth mode's (D8 vs D9).

### 3.4 The ghost question, answered properly

`Z`, `m²`, `c_s²` as functions of the action's coefficients:

```
Z   = K(2+3β)/β + ηp²                       > 0  ⟺  β > 0   (on the branch 2+3β > 0)
ω²  = αp⁴ / Z                               > 0  ⟺  α > 0
c_s² = αp² / Z                              > 0  ⟺  α > 0  (and → 0 as p → 0)
m_T² = K/η                                  > 0  ⟺  η > 0
```

`Q`'s sign is the sign of `β` on the branch where the θ Legendre map is invertible (D11: `Q(β) = −0.333, −1.000,
−17.000, +23.000, +7.000, +5.000, +3.667` for `β = −0.6, −0.5, −0.1, 0.1, 0.5, 1.0, 3.0`). On an open grid of
`β > 0, η > 0, γ > 0`, **36/36** points have `Z > 0, ω² > 0, m_T² > 0, c_s² > 0` (D12), and the coefficients as
dialled satisfy all four (D15). So: **no ghost, no tachyon, on an open set** — with `β > 0` the load-bearing
condition, exactly as A54's `H8` said, now from the derived `Z` rather than from a quoted `Q₀`.

The one branch to keep in mind: for `β < −2/3` the combination `K(2+3β)/β` is again positive, but there
`2+3β < 0` and the θ Legendre map degenerates at `β = −2/3` — a different theory, excluded by A54's L8, and not
claimed here.

---

## 4. Task 4 — what the fifth mode is

**Identity.** It is the **mixed conformal-mode / P-longitudinal scalar**. Three computed facts pin it down:

1. The conformal mode alone has a **negative** kinetic term, `−3Aζ̇²/(4K)` (D1) — but it is not a propagating
   degree of freedom: the shift's elimination flips the sign (`Aζ̇²/(2Kβ)`, D3), and the lapse equation at
   `H = 0` is a constraint `ζ/K + σ = 0` (D4) that locks the conformal factor to the P longitudinal. One mode
   survives, not two.
2. Its kinetic coefficient has two contributions: the gravitational `B = K(2+3β)/β` and the P kinetic `ηp²`.
   Neither alone is the answer; the mode is genuinely mixed.
3. Its potential is `αp⁴` with **no `p²` term** (D5): the longitudinal P's would-be mass `K/2` is exactly
   cancelled by the conformal gradient energy.

**Compton wavelength.** At `H = 0` the mode is **gapless** — `m² = 0` exactly (D8) — so it has no Compton
wavelength: `λ_C = ∞`. It is a `k⁴` mode with `c_s² = αp²/Z → 0`. In an expanding background the only scale it
can acquire is the Hubble scale (nothing in the action supplies another), so any curvature-induced gap is
`O(H)`; **I did not compute its coefficient** (the `1/H` reduction is delicate and round-2's `2BH²` term is not
re-derived here), so I state no number for it.

The mode that *does* have a Compton wavelength is the pair of **transverse** P modes:

```
m_T² = K/η        ⇒        λ_C = √(η/K) ,
```

a function of the free coefficient `η` alone. Under A67's assumption `η = KL★²/2` this is `L★/√2 = 16.9706 pc`
(computed); under `η = KL★²` it would be `24 pc`; under `η = 3KL★²/2` it is `29.3939 pc`. **The action fixes none
of these.** `L★ = 24 pc` is fitted (A65), so `λ_C` is **unpredicted**.

**What measurement would fix it.** `η` is fixed by the mass of the transverse P sector — the `k → 0` gap of the
two vector modes, equivalently the range of the P-mediated stress (a fifth-force-type range at the `L★` scale).
`γ` (and with it `α`) is fixed by the coefficient of the `k⁴` term, i.e. by the scalar's dispersion
`ω² = αp⁴/Z` at a measured `k`. Neither is fixed by anything currently in the record.

---

## 5. Checks (`a68_checks.py`, 39/39 PASS, exit 0)

```
A1  P kinetic Hessian = sqrt(h) eta delta_ij/N                 0 residual
A2  det = eta^3 h^{3/2}/N^3 != 0                                2.476491 = 2.476491
A3  P equation second order (sigma-ddot coefficient eta p^2)     0.490000 = 0.490000
A4  delta S_P/delta N^j = pi_P^i F_ij + (D.pi_P) P_j            0 over 3 components
A5  coefficient of P_i D_j P^j in H_i^(P) = 0; linear in pi_P   0, True, True
A6  H_i^(P) = 0 on pi_P = 0                                     0
B1  the bracket = -i q_i pi_P^j + i q_l pi_P^l delta - delta (D.pi_P)   9/9
B2  same, numerically at 5 random configurations                 0.000e+00 (|M| up to 6.408)
B3  bracket = 0 on pi_P = 0 (5 configurations); rank there       0.0, rank 0
B4  rank off surface: 3 (D.pi_P != 0), 2 (D.pi_P = 0)            3, 2
B5  eigenvalues {-b, -b+ia, -b+ia}                               max dev 9.9e-16
B6  (khat,e1,e2) block structure                                 max dev 9.2e-16
B7  bracket linear in pi_P, independent of P                     1.8e-15
B8  {h_i, P_k} = F_ki delta + P_i d_k delta (diffeo generator)   9/9
B9  {h_i, D.P} = K_i (q.P) - (q.K) P_i + q^2 P_i (Route A's pair) 3/3
C1  phase-space dimension                                        26 = 26
C2  no Ndot, Ndot^i anywhere => 4 primaries                      True, 4
C3  4 secondaries (N enters only as 1/N)                         d(N L)/dN = 0, 4
C4  no tertiary: H_perp independent of N, P eq. 2nd order        dH_perp/dN = 0
C5  second-class rank on the surface; SC                         0, 0
C6  DOF = (26-16-0)/2; explicit modes                            5, 5
C7  Route C's 4 needs SC = 2; computed SC = 0                    4 vs 5
D1  K^2-(1+beta)theta^2 = -3A zdot^2 - 2A zdot Y - beta Y^2      0
D2  R3^(2) = 2 p^2 zeta^2                                        0.540800 = 0.540800
D3  after the shift: A zdot^2/(2K beta)                          0
D4  lapse equation at H=0 is the constraint p^2(zeta/K+sigma)    0
D5  final action: Q = B+eta p^2, V = alpha p^4                   0, 0
D6  Z = K(2+3beta)/beta + eta p^2                                4.193586e-09
D7  c_s^2 = alpha p^2/Q, -> 0                                    max dev 0.0e+00; c_s^2(1e-6)=2.0e-13
D8  m^2 = lim V/Q                                                0
D9  m_T^2 = (K/2)/(eta/2), c_T^2 = gamma/eta                     8.387173e-10, 1.0
D10 eta, gamma independent (Jacobian, two inputs)                1/eta != 0
D11 sign(Q) = sign(beta) on 2+3beta>0; Q(input) > 0              True
D12 open healthy set                                             36/36
D13 A67's 2/L*^2 is eta = K L*^2/2 read back                     exact, then 1/3
D14 W''(0) = 1/K -> mass term K/2                                1/K, K/2
D15 the dialled coefficients are healthy                         all four > 0
D16 the two gradient operators share one gamma (ratio 2)         2
D17 F_ij F^ij = 2 p^2 |P_T|^2                                    3.55e-15
```

Nine mutations, each changing one input and exiting 1 (§`MUTATE.md`): `eta_neg` (D15), `beta_neg` (D7, D11,
D15), `gamma_zero` (D7, D15), `alpha_zero` (D7, D15), `pp_term` (A5, A6, B1, B2, B8, B9), `bracket_sign` (B1, B2,
B5, B6), `drop_W` (C4, D9, D12, D14, D15), `eta_eq_gamma` (D10), `central_charge` (B3, B4, B5, B6, B7, C5, C7).

---

## 6. What this does not do

* **The full nonlinear bracket algebra is not computed.** `{H_⊥, H_⊥}` at `β ≠ 0` — A54 §2.2's `O(β)`
  deformation — is inherited, not re-derived. If it broke first-classness the count would change (C7 computes
  the `FC = 7` branches: 6 if `H_⊥` drops out, 5 if it pairs second-class), but no such change can produce 4,
  because the P sector supplies no second-class pair (B3) and no P constraint (A2).
* **The `H ≠ 0` reduction is not done.** All coefficients, masses and sound speeds are at `H = 0`, where `m²` is
  defined. No de Sitter mass is quoted.
* **The transverse reduction is only partly re-derived.** `m_T² = K/η` comes from the action's own mass and
  kinetic coefficients per component (D9, D14), and `c_T² = γ/η` from `F²` (D17); the mode's decoupling from the
  scalar sector at quadratic order is round-2's §3, not re-derived here.
* **`L★` remains fitted** (A65). Nothing here predicts it, and §4 says so explicitly.
* The **`β < −2/3` branch** is excluded by A54's L8 and not analysed.

---

## 7. Reproduce

```bash
cd deepseek_push/DS_FINAL_2026_10_21/A68_bracket_algebra
python3 a68_checks.py --json-out a68_results.json | tee a68.out     # 39/39, exit 0
python3 a68_checks.py --mutate pp_term                              # must exit 1 (A5, A6, B1, B2, B8)
```

---

## 8. VERDICT

**The theory has 5 degrees of freedom, not 4, and the fifth mode is healthy on an open set of the action's
coefficients — but nothing fixes their magnitudes, and the mode is gapless.** The evidence is computed, not
asserted: the only bracket that could have made the shift constraint second class,
`{H_i(x), π_P^j(y)} = [π_P^jδ_i^k − δ_i^jπ_P^k]∂_kδ − δ_i^j(D·π_P)δ`, is *linear in the P momentum*, contains no
`P` at all, and is the **zero matrix** on the surface `π_P = 0` (rank 0 at five configurations, max entry `0.0`);
its rank off that surface is 3, or 2 when `D·π_P = 0` with the longitudinal direction in the kernel. There is no
`φ_P` to pair with it — the P Legendre map is invertible with `det = η³h^{3/2}/N³` — and A66's mechanism is
absent from the action: the coefficient of `P_iD_jP^j` in `H_i^(P)` is exactly `0`, because
`H_i^(P) = π_P^kF_ik − (D·π_P)P_i` carries exactly one `π_P`. The Dirac count is therefore `26` phase-space
dimensions, `8` first-class constraints, `0` second-class, second-class rank `0`, and
`(26 − 16 − 0)/2 = 5` — A54's number, with no constraint reclassified and Route C's `4` requiring `SC = 2` that
the action does not supply. The fifth mode's kinetic coefficient, derived from the frozen action and not
inserted, is `Z = K(2+3β)/β + ηp²`, positive iff `β > 0` on the branch where the θ Legendre map is invertible;
its potential is `αp⁴` with the longitudinal P's `K/2` mass exactly cancelled by the conformal gradient, so
`m² = 0` and `c_s² = αp²/Z → 0` — a gapless `k⁴` mode, healthy for `β > 0, η > 0, α = γ > 0` (36/36 grid points,
all four coefficients positive at the dialled values). The action forces `α = γ` but **not** `η = γ`; A67's
`m² = 2/L★²` is `K/η` with `η = KL★²/2` substituted, an input echo, and it belongs to the two transverse P modes
whose Compton wavelength is `√(η/K)` — `16.9706 pc` only under that assumption, and otherwise unpredicted
because `L★` is fitted (A65).
