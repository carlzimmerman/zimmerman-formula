# L63 — door 2: a degenerate locus exists, it is unique, and the floor it reaches is three, not two

2026-09-09. Lane L63 of [CHARTER.md](CHARTER.md), answering **door 2** of
`qwen_claude_field_theory/closure_2026/TEN_OPEN_DOORS_2026-09-09.md`, which the lead agent names
*"Priority: highest for architectural viability."*
Script: [L63_degeneracy_locus.py](L63_degeneracy_locus.py) → [L63_degeneracy_locus.out](L63_degeneracy_locus.out).
**78 checks, 78 PASS, 0 FAIL; exit 0.**

Nothing under `closure_2026/` or any other agent's directory was imported, executed or copied.
`L46_mode_floor.py`, `L52_marginal_sweep.py` and `L54_repair_constraints.py` were **not imported** either;
their headline numbers are recomputed from scratch here and compared only inside the controls. Every
matrix, every constraint and every rank is exact rational arithmetic. Both a₀ footings,
**9.3619×10⁻¹¹ / 1.1279×10⁻¹⁰ m s⁻²**, on every dimensional number; the mode count itself is a₀-independent
and that is stated rather than silently assumed.

**Polarity.** Every check asserts a *statement* and PASS means the statement is true. Several PASSes are
negative results for the construction; each line says which.

---

## 0. The lead's challenge, accepted

> *"Fable's reported four-mode model is not a two-mode certificate."*

**That is correct**, and this lane exists to answer it rather than to defend the count. L46 counted four
and identified them; L54 counted four again with the auxiliary repair. Neither showed that two-plus-a-clock
is reachable. Here is what the calculation the door specifies actually returns.

## The answer, in three sentences

**A degenerate locus exists, it is exactly characterised, and it works: the velocity Hessian's degeneracy
variety is the union of three hyperplanes — `K₂ = 0`, `c₁₄ = 0`, `c₂ = −2/3` — and the first of them
delivers 2 tensor + 1 healthy clock, closing at the second generation of the consistency algorithm, at
every `k ≠ 0`, surviving minimal matter coupling and preserving FLRW expansion.**
**But it is not the construction door 2 asks for: `W_χφ = 0` identically, so no null vector of the Hessian
mixes the clock and the scalar, and every available degeneracy is a *decoupling* that switches one whole
field off rather than a genuine clock–scalar degeneracy — which would need an operator in which `Q`
multiplies a velocity, and there is none in the submitted action.**
**And the raw integer 2 is unreachable: switching *both* kinetic terms off returns 3, not 2, because the
antisymmetric clock–scalar coupling makes `χ` and `φ` canonically conjugate to each other once neither has
a kinetic term — the very term L52 recorded as harmless is what holds the floor at three.**

---

## 1. Controls — the counter earns the right to be believed

Classification is by the **rank of `A J Aᵀ`** on the constraint set the consistency algorithm itself
generated. Nothing is supplied by hand: the null vectors of `W` *are* the primary constraints, the
secondaries are generated, and first/second class is a rank.

| control | required | returned | structure found |
|---|---|---|---|
| ADM general relativity | 2 | **2** | `N_q = 10`, 4 primary + 4 secondary, all 8 first class |
| GR + one minimally coupled scalar | 3 | **3** | `N_q = 11`, same 8 first class |
| Einstein-aether (`c₁…c₄ = 1/5, 1/7, 1/11, 1/13`) | 5 | **5** | `N_q = 13`, same 8 first class |
| khronometric (same `c`s, `u` hypersurface-orthogonal) | 3 | **3** | `N_q = 11`, same 8 first class |

`C4b`: the machinery *sees* why khronometric loses two — the only change is that `u_i` is a gradient and
exactly the spin-1 pair disappears. `C5`: `k`-independent. `C5b` is a **known-bad control that must be
detected**: GR + *two* minimally coupled scalars returns 4, not 3, so the counter is not simply echoing
the eight first-class constraints it starts with. `C6`/`C7` reproduce Jacobson's `c_T² = 1/(1 − c₁₃)` and
Blas–Pujolàs–Sibiryakov's khronometric spin-0 speed, exactly in rationals, at two parameter points.

**L46 reproduced** (`C8`–`C11`), at the deposited exhibited point of `THE_COMPLETE_THEORY` §5
(`K_B = 0.2`, `c₁₄ = 1.0×10⁻⁶`, `c₂ = 1.679318×10⁻⁶`, `|K₂| = 1.92935×10⁶`, on the closure locus):

* four modes at a generic point **and** at the exhibited point — 4 primary + 4 secondary, all first class,
  so `12 − 8 = 4`: the extra modes are extra **fields**, not missing constraints;
* `c_T² = 1` exactly, as an identity in `K_B`;
* with `φ` switched off the scalar sector carries exactly one mode and its speed² **is** `σ* = 1.679312732`;
* the two scalar eigen-speeds are `1.080825×10⁻⁶` and `3.358632`, whose **sum** is `σ* + c²_s,mix = 3.358631`
  — confirming L46's PART 2B correction, and matching L46's closed form
  `c²₋ = (2−K_B)[2J_Y − (2−K_B)]/(4|K₂|)` at this point to six figures.

---

## 2. The full ADM velocity Hessian — the door's first requirement

Built with **lapse and shift retained**, never gauge-fixed, and with the clock kept explicitly (no unitary
gauge). `H0`: the 12-variable quadratic action reconstructs exactly. `H1`: `W` has exactly four
identically-zero rows — `n`, `ν_x`, `ν_y`, `ν_z` — for arbitrary `K_B`, `c₂`, `c₁₄`, `K₂`, `J₁`, `ξ`, `k`,
so the four primary constraints are structural. `H2`: `W`, `B` **and** `C` block-diagonalise into
helicity 2 / 1 / 0.

The helicity-0 velocity Hessian, printed by the script:

```
        n     nu_z      h_zz            hT          chi      phi
 n  [   0        0         0             0            0        0 ]
nu_z[   0        0         0             0            0        0 ]
h_zz[   0        0     -c2/4   -c2/4 - 1/4            0        0 ]
 hT [   0        0  -c2/4-1/4   -c2/4 - 1/8           0        0 ]
chi [   0        0         0             0     c14*k**2        0 ]
phi [   0        0         0             0            0     -K_2 ]
```

`H3`/`H3b`/`H4` — **the structure theorem.** The 4×4 dynamical block is **block diagonal**:

    det W(dynamical) = det W(metric 2×2) × W_χχ × W_φφ = −(3c₂+2)/32 · c₁₄k² · (−K₂)

`W_χφ = W_h,φ = 0` identically, and `W_χ,h = 0` too. This single fact decides door 2.

### `H5` — L52's antisymmetry claim: **confirmed, and sharpened**

The task asked for this to be reconfirmed or corrected. Computed here independently at symbolic `k`:

    B_χ,φ = k²(K_B − 2)        B_φ,χ = 0        C_n,φ = C_φ,n = k²(2 − K_B)

* **`H5` CONFIRMS L52's A7/C-X1.** The only clock–scalar *velocity* coupling carries one time derivative
  and sits entirely in `B`. Its symmetric part is `½ d/dt(χφ)`, a total derivative, so the coupling is
  equivalent to a purely antisymmetric (gyroscopic) one and contributes **nothing** to the velocity Hessian.
* **`H5b` SHARPENS L52.** The same operator `2(2−K_B)a^μ∂_μφ` also supplies a **symmetric, non-kinetic**
  lapse–scalar mixing `C_n,φ ≠ 0`, because `a_i = ∂_i(n − χ̇)` has a lapse piece as well as a clock piece.
  L52's *"the deposited action contains exactly one field–field mixing, and it is antisymmetric"* is true
  of the **kinetic** mixing and incomplete as stated: **the MOND source itself is the symmetric half**, and
  it is what carries the static limit. Nothing in L52 depends on the difference, but the sentence should
  read "one field–field *velocity* mixing".

### `H6` — the theorem off the flat background

`H3` was proved about flat space with `Q₀ = 0`. The door's question is about the *theory*, so the same
statement is proved from the ADM identities, with the lapse, the shift, the 3-metric, **all four-dimensional
Christoffel symbols** and the second derivatives of `φ` carried as independent free symbols:

* `H6a` `q^{00} = 0` exactly for an arbitrary lapse, shift and 3-metric, so `Y` has zero second derivative
  in `φ̇`;
* `H6b` `∂Y/∂φ̇ = 2q^{0i}∂_iφ` contains no `φ̇` either, which also kills the `J''(Y)(∂Y/∂φ̇)²` channel;
* `H6c` `V_μ = ∂_μφ + n_μQ` has `V_0 = N^i∂_iφ`, `V_i = ∂_iφ` — every component `φ̇`-free, the `φ̇` in
  `∂_0φ` cancelling against the one inside `Q`;
* `H6d` both gradient invariants — `Y = γ^{ij}V_iV_j` and the coherence scalar
  `γ^{ik}γ^{jl}(D_iV_j)(D_kV_l)` — are `φ̇`-free on an **arbitrary** background, curved or expanding;
* `H6e` `a_μ` is purely spatial and carries no field velocity, so `a^μ∂_μφ = a^iV_i` contains no `Q` at all;
* `H6f` in the **non-unitary** description `χ̇` cancels out of `n_μ` and `n^μ` at first order and `q^{00}`
  vanishes to first order too — so the theorem survives keeping the clock unfixed, which is the description
  this lane counts in.

**`H6g` the conclusion:** `φ̇` enters the submitted action only through `Q`, and `Q` only through `−K(Q)`.
Therefore

> **W_φφ = −K″(Q̄)·√−g/N² and W_{φX} = 0 for every other field X, on every background.**

---

## 3. The degeneracy conditions, solved for the couplings and the free functions

Treated as unknowns, not fixed first. `D1`:

| branch | condition | solution |
|---|---|---|
| **A** metric / conformal | `det W(metric) = −(3c₂+2)/32 = 0` | `c₂ = −2/3` |
| **B** clock | `W_χχ = c₁₄k² = 0` | `c₁₄ = 0` |
| **C** MOND scalar | `W_φφ = −K₂ = 0` | `K₂ = 0` |

There is no fourth branch. `D1b`: **neither free function `J` nor the coherence operator `ξ` appears in any
branch condition** — consistent with `H6`, which shows they carry no `φ̇` at all. The only free function
that can produce a degeneracy is `K(Q)`, through `K″(Q̄)`. `D1c`: the clock branch is `k`-**dependent**
(`W_χχ ∝ k²`) while the scalar branch is `k`-**independent** — the distinction the door demands, settled
before any count is run.

### `D2` — the theorem that answers door 2's actual question

**No null vector of the velocity Hessian mixes `χ` and `φ`, for any values of the couplings**, because
`W_χφ = 0` identically. A "genuine" clock–scalar degeneracy — one combination propagating and the
orthogonal one constrained — is **unreachable within the submitted action's operator content**. Every
available degeneracy is a *decoupling*: it switches one whole field off.

**Hypotheses, stated:** the action is a functional of `(g, n, Q, V)` in which `Q` appears only inside `K(Q)`.

### `D3` — the escape, exhibited rather than asserted

A mixed degeneracy needs `W_χφ ≠ 0`, i.e. a term in which `Q` multiplies a clock or metric **velocity**.
The minimal such operator is `F(Q)·θ` with `θ = ∇·n` (equivalently `F(Q)K`, or a two-argument `K(Q, θ)`).
Adding it produces `W_{h_zz,φ} = F′/4 ≠ 0` — so a mixed degeneracy becomes possible in principle. **It is
outside the submitted action.** That is what door 2 would require, named constructively.

---

## 4. The consistency algorithm at every branch, pushed to closure

`E0` is a **sanity guard on the substitution machinery** — an earlier draft of this script silently
evaluated every branch at the base point because the parameter helper took string keys. The guard asserts
that asking for `K₂ = 0` really does produce a zero `φ̇²` coefficient. It is recorded because that class of
bug produces a plausible-looking table of numbers.

```
  base (no degeneracy) : N_q = 12, rank(W) = 8, primaries = 4, generations = [4, 4],
                         first class = 8, second class = 0  ->  DOF = 4
  branch C: K_2 = 0    : N_q = 12, rank(W) = 7, primaries = 5, generations = [5, 5],
                         first class = 8, second class = 2  ->  DOF = 3
  branch B: c_14 = 0   : N_q = 12, rank(W) = 7, primaries = 5, generations = [5, 5],
                         first class = 8, second class = 2  ->  DOF = 3
  branches B and C     : N_q = 12, rank(W) = 6, primaries = 6, generations = [6, 4],
                         first class = 8, second class = 2  ->  DOF = 3
  branch A: c_2 = -2/3 : N_q = 12, rank(W) = 7, primaries = 5, generations = [5, 5],
                         first class = 8, second class = 2  ->  DOF = 3
```

**`E1` branch C closes and returns three** — two tensor plus one clock. Five primaries, one new generation,
terminating: no tertiary constraint, no runaway chain. `E1b`: the four diffeomorphisms are **untouched**,
still eight first-class constraints exactly as in ADM GR, so the degeneracy removes a *field* and not a
gauge symmetry — the pathology that had to be ruled out. The **Poisson-bracket operator** `A J Aᵀ` is
printed in full: a 10×10 matrix whose only non-zero entries are the `±1` pair linking `π_φ` to the elliptic
`φ` constraint. Rank 2 = `n₂`.

**`E2` branch C is not the only one.** `c₁₄ = 0` also closes and returns three — two tensor plus the MOND
scalar. **L46 did not count this branch**; it only flagged `c₁₄ → 0` as marginal (its M2c) and as forbidden
by PPN. It is a second, independent route to the integer with a *different* price (§7).

### `E3` — THE FLOOR THEOREM, and the direct answer to the lead's challenge

**Switching both kinetic terms off does NOT give two. It gives three.**

With `W_χχ = W_φφ = 0` the two fields still carry the antisymmetric coupling `B_χφ χ̇ φ`, and a pair of
coordinates with no kinetic term but a **non-degenerate first-order symplectic coupling is one canonical
pair, not zero degrees of freedom**: `χ` and `φ` become conjugate to each other. The counter finds six
primaries but only four second-generation constraints and exactly one second-class pair.

`E3b` is the **mechanism control**, run on the minimal toy that isolates it: two coordinates with no kinetic
terms and one antisymmetric first-order coupling `b(χ̇φ)` carry **1** degree of freedom; the same pair with
`b = 0` carries **0**. So the three is the gyroscopic coupling's doing, not an artefact of the counter.

`E3c` **the irony, stated plainly.** L52's C-X1 recorded the clock–scalar mixing as harmless *because* it is
antisymmetric and "contributes NOTHING to the kinetic Hessian". That is true, and `H5` reconfirms it — and
it is exactly why the mixing cannot be removed by any degeneracy. The same antisymmetry that makes the
coupling invisible to the Hessian makes it a **symplectic form** on the `(χ, φ)` pair. **The harmless term
is the obstruction.** The floor inside the submitted action is three, and `N_grav = 2` read as a total count
is unreachable.

### `E4` — the door's own warning, made executable

> *"A singular Hessian alone does not pass."*

Correct, and here is a model that passes the singular-Hessian test and is **not** degenerate. Take
`K(Q) = K₄Q⁴`. At the deposited background `Q₀ = 0` one has `K″(0) = 0`, `W_φφ = 0`, and the counter
returns **three**. It is fake: `K″(Q) = 12K₄Q²` is non-zero at every `Q ≠ 0`, so the mode reappears for
arbitrarily small departures from the background, and the "second-class pair" the algorithm found has a
bracket that vanishes with the *background* rather than with a *coupling*.

`E4b` is the discriminator used throughout: **is the vanishing condition a statement about a coupling or
about a background?** `K″(Q) = 2K₂` is constant in `Q`, so `K₂ = 0` degenerates the Hessian on every
background at once. Branch C passes the test E4's model fails.

---

## 5. `k = 0` separated from `k ≠ 0`

`F1` — **the trap, exhibited.** At `k = 0` the *unmodified* submitted action is already Hessian-degenerate,
at every parameter point and with a perfectly healthy `c₁₄`: `rank(W)` drops from **8 to 7**, because
`W_χχ = c₁₄k²` carries a factor `k²`. The counter returns 7 there — but at `k = 0` that number is the
homogeneous sector's content, not a count of propagating polarisations. **A degeneracy read off at `k = 0`
is evidence of nothing.**

| | `k = 1` | `k = 2` | `k = 5` |
|---|---|---|---|
| base | 4 | 4 | 4 |
| branch C (`K₂ = 0`) | **3** | **3** | **3** |
| branch B (`c₁₄ = 0`) | **3** | **3** | **3** |

`F2`: branch C's condition contains **no `k` at all**, so its degeneracy is a property of the couplings.
`F3`: branch B's degeneracy is real at `k ≠ 0` too, even though its condition is satisfied at `k = 0` for
free. `F4` is the control that makes the comparison mean something.

---

## 6. Matter coupling and FLRW — the door's two decisive conditions

### A method note that had to come first

At quadratic order about a background that **solves** the field equations, minimally coupled matter cannot
couple to metric perturbations at all: the cross term is `h^{μν}δT_{μν}` and `T_{μν}` vanishes on flat space.
Expanding instead about `ψ̄̇ ≠ 0` on flat space — which is *not* a solution — destroys the linearised gauge
invariance, and the counter then reports **eight second-class constraints where there should be eight
first-class ones**. That is a property of the illegitimate background, not of the theory. It is recorded
rather than hidden, and the question is split into the two pieces that are separately well posed.

* **`G0` [structural, every background]** minimally coupled matter `S_m[g, ψ]` contains no `φ` at all, so it
  cannot contribute to any entry of the `φ` row of `W`. Verified on the *illegitimate* `ψ̄̇ ≠ 0` expansion as
  well, where the metric–matter couplings **are** switched on: even there the `φ` row is identical entry by
  entry to its value with no matter, and the new `φ–ψ` entry is zero. This, not the count, is what the claim
  rests on.
* **`G1` [count, legitimate background]** branch C + one minimally coupled matter field returns
  **4 = 2 tensor + 1 clock + 1 matter**, with the same two second-class constraints and the same eight
  first-class ones. Matter adds a mode; it does not give the scalar back. `G1b`: branch B likewise.
* **`G2` the bracket, derived not observed.** `{π_φ, C_φ} = −∂²H/∂φ² = J₁k²(K_B − 2)(1 + ξ²k²)`. It contains
  no matter coupling, no `K₂` and no `c₁₄` — which is *why* `G1` holds, as a statement about the action
  rather than about the particular matter field tested.
* **`G2b` the limit of `G1`, and a real hole.** That same bracket **vanishes where `J_Y → 0`**, i.e. at every
  zero of the background gradient (`J_Y = s/Δ(s) ~ √s` as `s → 0`: every symmetry centre, every MOND saddle,
  the Solar System's own included). There the pair stops being second class and the count is not 3. With the
  `ξ²` operator placed **outside** `J` instead of inside it, the bracket keeps a positive `ξ²k⁴` piece and
  the failure is removed — so **L52's C-L3 placement fork decides whether branch C is uniform or has holes.**
* **`G3` [negative control]** the degeneracy does **not** survive a **disformal** matter coupling. With
  `ĝ = g + B∂_μφ∂_νφ` — the standard TeVeS/BIMOND matter coupling, and a natural thing to reach for in a
  MOND completion — the matter sector itself contributes `Bψ̄̇²` to `W_φφ`, the Hessian is no longer singular
  in the `φ` direction, `rank(W)` goes 8 → 9 and the primary constraint `π_φ` is destroyed. **"Survives
  matter coupling" is a statement about MINIMAL coupling and must always be quoted with that qualifier.**

### FLRW, from an independently built mini-superspace reduction

On `ds² = −N(t)²dt² + a(t)²dx²`, `τ = t`, `φ = φ(t)`: `a_μ = 0` so the AeST mixing vanishes identically;
`V_μ = 0` so `J(Y + ξ²…) = J(0)`, a pure cosmological constant; `A_{μν} = K_{μν}` so the `c₁` and `c₃` terms
**cancel** because `c₁ = −c₃`, leaving only `−c₂K²`. `I1`:

    kinetic terms:   a-dot^2 coefficient = −(6 + 9c₂) a/N        phi-dot^2 coefficient = −K₂ a³/N

* **`I2` branch C preserves FLRW expansion.** `K₂ = 0` removes the `φ̇²` term and leaves `ȧ²` untouched, so
  the Friedmann equation still determines `H`. The cost is that `φ` drops out of the homogeneous sector
  entirely — no dark component, which the deposited theory had already removed by setting `Q₀ = 0`.
* **`I2b` branch B preserves it for a stronger reason** — `c₁₄` does not appear in the mini-superspace
  Lagrangian at all, because `a_μ = 0` on a homogeneous lapse. The clock branch is invisible to the
  background cosmology.
* **`I3` branch A destroys FLRW expansion, exactly.** `c₂ = −2/3` makes `6 + 9c₂ = 0`, the `ȧ²` term
  vanishes and the lapse's own equation loses its `H²` piece: **there is no Friedmann equation left.** The
  conformal branch of the perturbative degeneracy variety and the FLRW-destroying locus are **the same
  point**. `I3b`: branch A is inadmissible anyway, since the theory needs `c₂ = σc₁₄ > 0`.
* **`I4` the linear-growth gate breaks at branch C** (`S_eff = 1 − (2−K_B)²/(c₂|K₂|) → −∞`, and the closure
  locus cannot be satisfied at all) — and the honest reading is that it is **vacuous**: with `Q₀ = 0` there
  is no dark component to grow, and the deposited table itself records that row as "PASS as an equation —
  and nothing to grow". Recorded as broken, not as a reason to keep the mode.

---

## 7. The price

Branch C removes the scalar by making it **auxiliary**, so it must be eliminated, and elimination
back-reacts on the clock. `P1`, by an explicit Schur complement independent of the Dirac machinery:

    c₁₄  →  c₁₄^eff(k) = c₁₄ + (2 − K_B)/[ J_Y (1 + ξ²k²) ]

a **wavenumber-dependent** shift — the algebraic signature of the instantaneous channel branch C buys.
`σ_eff(k) = (2 − c₁₄^eff)c₂/[c₁₄^eff(2 + 3c₂)]` at the deposited exhibited point, in the deposited
convention `k = 1/L` (the convention under which `P4` reproduces the deposited `α₁`):

| gradient scale `L` | footing | `ξ²k²` | `c₁₄^eff` | `σ_eff` | `σ_eff/σ*` |
|---|---|---|---|---|---|
| 10 kpc (galactic) | canonical | 1.00e−10 | 5.5953e−01 | 2.1616e−06 | **1.29e−06** |
| Saturn's orbit | canonical | 4.633e+06 | 1.1208e−06 | 1.49837 | 0.8923 |
| 1 AU | canonical | 4.255e+08 | 1.0013e−06 | 1.67711 | 0.9987 |
| `ξ/10⁶` (deep UV) | canonical | 1.00e+12 | 1.0000e−06 | 1.67931 | **1.0000** |
| 10 kpc (galactic) | alt | 2.25e−10 | 6.6031e−01 | 1.7036e−06 | **1.01e−06** |
| Saturn's orbit | alt | 1.043e+07 | 1.0633e−06 | 1.57928 | 0.9404 |
| 1 AU | alt | 9.573e+08 | 1.0007e−06 | 1.67816 | 0.9993 |
| `ξ/10⁶` (deep UV) | alt | 1.00e+12 | 1.0000e−06 | 1.67931 | **1.0000** |

**`P2` CONFIRMS L46's headline price, in the infrared.** At galactic gradient scales the clock's speed²
collapses from `σ* = 1.679` to `2.16×10⁻⁶` (canonical) / `1.70×10⁻⁶` (alt) — **5.89 / 5.99 orders of
magnitude**, on both footings. L46 §6's "the decisive price is σ" is reproduced independently.

**`P3` REFINES L46: the price is not six orders everywhere.** The shift goes as `1/(1 + ξ²k²)`, so it
**vanishes in the ultraviolet**: `σ_eff/σ*` is within `10⁻⁴` of 1 at a gradient scale `ξ/10⁶`, and is
already back to 0.89 / 0.94 at Saturn's orbit. The crossover, where the eliminated scalar and the bare
clock contribute equally:

| footing | `ξ` | `J_Y` | crossover `L` |
|---|---|---|---|
| canonical | 0.10 pc | 3.217 | **27.6 AU** = 1.337×10⁻⁴ pc |
| alt | 0.15 pc | 2.726 | **38.1 AU** = 1.846×10⁻⁴ pc |

Since the Hadamard obstruction `σ*` was chosen to cancel is *"a growth rate rising like `k²`"*
(`THE_COMPLETE_THEORY` §3.1) — a **short-wavelength** statement — L46's price is an **infrared** price and
is overstated in the regime where the obstruction lives. **This is a refinement, not a discharge:** this
lane does **not** redo the quartic obstruction with a `k`-dependent `c₁₄`, and does not claim the price is
paid off. It names the calculation. What it does establish is a *new* liability in its place: a clock whose
speed runs by six orders of magnitude across the outer Solar System is not something any existing gate table
contains.

### The rest of the ledger

| row | branch C (`K₂ = 0`) | branch B (`c₁₄ = 0`) |
|---|---|---|
| tensor speed | `c_T² = 1` exactly (`P7`) | `c_T² = 1` exactly |
| static MOND, `Φ = Ψ`, `γ`, `α₁`, `α₂`, `α₃`, Cassini, Saturn | **literally unchanged** — `K₂` occupies one entry of `W` and appears nowhere in `B` or `C`, verified entry by entry (`P5`) | changes: `α₁` **improves** |
| `α₁` (bound 10⁻⁴), canonical / alt | −4.483e−06 / −4.253e−06 (unchanged; `P4` reproduces the deposited −4.48e−6 / −4.25e−6) | **−4.830e−07 / −2.534e−07**, better by 9.3× / 16.8× (`P6`) |
| surviving mode's health | `c₁₄^eff > 0` (no ghost) and `σ_eff > 0` (no gradient instability) at every scale and both footings (`P8`) | surviving scalar; the clock becomes an instantaneous constraint (`σ → ∞`) |
| clock speed `σ` | runs `σ*` → `2×10⁻⁶ σ*` across ~30 AU (`P2`/`P3`) | `σ = c₂/c₁₄ → ∞`: the same `σ*` cost from the other side |
| instantaneous channel | **yes** — the eliminated `φ` obeys an elliptic equation with no time derivative; the helicity-0 dispersion drops from 2 roots to 1 (`P9`) | **yes** — in the clock sector instead |
| linear growth | broken but vacuous (`I4`) | untouched |
| FLRW expansion | preserved (`I2`) | preserved, trivially (`I2b`) |

**`P8b` — a structural echo worth recording.** The reduced theory's own gradient stability requires
`c₁₄^eff < 2`, which unpacks to

    J_Y (2 − c₁₄)(1 + ξ²k²) > (2 − K_B)          [threshold J_Y > 0.9000005]

— **exactly** the health condition L46 derived for the *unreduced* four-mode spectrum from the product of
the two scalar `ω²`. Two different calculations, on two different theories, give the same threshold. The
deposited `J_Y = 3.217 / 2.726` clears it by **3.57× / 3.03×** on both footings.

---

## 8. Verdict on the lead's highest-priority gate

`V1`–`V8`, all PASS:

* **`V1` a degenerate locus exists** and is exactly characterised — three hyperplanes, no fourth branch, no
  dependence on `J` or `ξ`.
* **`V2` its primary constraints close** — second generation, 8 first-class + 2 second-class, no tertiary,
  no runaway.
* **`V3` the degeneracy holds at `k ≠ 0`** and is not the `k = 0` artefact that `F1` exhibits.
* **`V4` it survives matter coupling and preserves FLRW expansion** — with the two qualifiers that must
  travel with the claim: matter must be **minimally** coupled, and the second-class bracket has a hole
  wherever `J_Y → 0` unless the `ξ²` placement fork is resolved outward.
* **`V5` two tensor modes plus a separately counted healthy clock IS reachable** inside the submitted
  action. Branch C delivers exactly 2 + 1; the clock is ghost-free and gradient-stable on both footings;
  `c_T = c` exactly; the Solar-System sector is literally unchanged; the algebra closes; FLRW survives.
* **`V6` but it is not a "genuine degeneracy" of the clock–scalar sector.** Every branch is a decoupling.
  The mixed-null-vector construction door 2 proposes does not exist within this operator content.
* **`V7` the floor is three, not two**, and the obstruction is named.
* **`V8` the price** is (i) an instantaneous scalar channel, (ii) a clock speed running by six orders of
  magnitude between ~30 AU and 10 kpc, (iii) a hole at every zero of the background gradient unless the
  `ξ²` fork is resolved outward. **None of the three is in the deposited gate table.**

### Three sentences

**Door 2's gate can be passed on the mode side and cannot be passed in the form it proposes: there is
exactly one working degenerate locus, `K₂ = 0`, it delivers two tensor modes plus one explicitly healthy
clock, its constraints close, it holds at every `k ≠ 0`, it survives minimally coupled matter and it
preserves FLRW expansion — but it reaches that count by *decoupling* the scalar, not by degenerating the
clock–scalar sector, because `W_χφ = 0` identically and no mixed null direction exists at all.**
**The raw integer 2 is a theorem-level no: switching both kinetic terms off returns 3, since the
antisymmetric clock–scalar coupling that L52 correctly identified as invisible to the Hessian is a
symplectic form on `(χ, φ)` and makes them conjugate to each other — so the lead is right that four is not
a two-mode certificate, and the reason is that no two-mode certificate is available from this action at
all.**
**The price of the one working locus is an instantaneous scalar channel, a clock whose speed runs by six
orders of magnitude across the outer Solar System, and a hole at every symmetry centre unless the `ξ²`
placement fork is resolved outward; further work on this architecture should either accept gate 2′ (two
tensor + one healthy clock, separately counted) or add the operator `F(Q)·∇·n` that `D3` exhibits, which is
the only thing that would make the genuine degeneracy door 2 asks for possible.**

---

## 9. What is open, named

1. **The quartic obstruction with a `k`-dependent `c₁₄`.** `P3` shows the `σ` price is infrared and the
   obstruction is ultraviolet. Whether `σ*`'s Hadamard repair survives the nonlocal `c₁₄^eff(k)` of the
   reduced theory is **not** computed here. Entry point: `THE_COMPLETE_THEORY` §3.1's `S₄` at 59 branch
   points, re-run with `c₁₄ → c₁₄^eff(k)`.
2. **The `ξ²` placement fork** (`L52` C-L3). Inside `J`, branch C loses its second-class pair at every
   zero of the background gradient (`G2b`). Outside `J`, it does not. This decides whether branch C is a
   theory or a theory-with-holes, and it is a one-line change of action.
3. **Branch B has not been priced beyond PPN and FLRW.** `c₁₄ = 0` improves `α₁` by an order of magnitude
   and leaves cosmology untouched, but makes the clock instantaneous. It was never counted before this
   lane, and it deserves the same gate sweep branch C has had.
4. **The escape operator `F(Q)·θ`.** `D3` exhibits that it produces the mixing a genuine degeneracy needs.
   Whether any `F` produces a *healthy* mixed degeneracy — and what it does to `c_T`, PPN and FLRW — is
   uncomputed.

Nothing here is closed. `κ = ½` remains **fitted**, and this file never says otherwise.
