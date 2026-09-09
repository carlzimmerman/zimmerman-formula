# L52 — the marginal-coefficient sweep: the technique has exactly one more application, and it is the big one

2026-09-09. Lane L52 of [CHARTER.md](CHARTER.md), generalising the mechanism [L44_COLLAR.md](L44_COLLAR.md)
found and sweeping the deposited action for everywhere else it applies.
Script: [L52_marginal_sweep.py](L52_marginal_sweep.py) → [L52_marginal_sweep.out](L52_marginal_sweep.out).
**68 checks, 68 PASS, exit 0.**

Method: the khronon quadratic Lagrangian is **derived here** from the four aether terms of
`THE_ACTION_2026-09-05.md` §1 by expanding the unit normal in sympy — not quoted from any khronometric
reference. The IC20/IC28 Hamiltonian and its auxiliary branch are re-transcribed by hand into sympy here
and root-solved by an mpmath Newton call written here. Nothing under
`closure_2026/integrable_clock_construction_2026/` was imported, run or copied; `L44_collar_vs_theorem.py`
was not imported either — its numbers are compared to only at the end of each control. Polarity: every
check asserts a **statement** and PASS means the statement is true, so a PASS on `C-L1a` is a *negative*
result for the theory and a PASS on `E3b` is a *positive* one.

---

## The short answer, in three sentences

**Fourteen quadratic coefficients exist in the deposited theory, they have never been listed in one place
before, and seven of them are marginal or sign-indefinite** — but six of the seven are either marginal only
in a limit the theory does not occupy, or repairable by an operator the action already carries, or a window
edge rather than a failure. **The one exception is the longitudinal stiffness `Σ_∥ = (2−K_B)/Δ′`, which is
`+∞` at every Solar-System background and in every galaxy core on the published kernel, negative on the raw
ν_RAR branch, and 9.6×10¹⁵ at Saturn even after the deposited repair — and L44's technique does *not* fix
it, because L44's arrangement can only raise a floor.** **The generalisation is that a holonomic auxiliary
attaches two ways and they are opposite: attached in *parallel* (mixing with the dangerous variable)
stiffnesses add and a zero becomes positive — that is L44; attached in *series* (the dangerous nonlinearity
moved onto the auxiliary, tied back by a quadratic spring) *compliances* add and an infinity becomes finite
— and that second arrangement, never tried in this programme, caps `Σ_∥` at `1/κ` for any `κ > 0`, costs
zero propagating modes, and is invisible to the ephemerides.**

---

## 1. Controls — L44 reproduces, and the machinery has teeth on both sides

`A1–A7` build the Hessian machinery and test it where the answer is already known.

* `A2` derives, from the action's own `c₁…c₄` terms, that the khronon quadratic Lagrangian is
  `c₁₄(∂_iχ̇)² − c₁₃(∂_i∂_jχ)² − c₂(∇²χ)²` — `c₁₄` and `c₁₃` emerging as the *only* combinations that
  appear. `A1` shows why: the normalisation removes `χ̇` at first order, so the khronon carries the
  reparametrisation invariance `χ → χ + ε(t)` and every term must carry a spatial derivative. This is what
  forces any repair of the clock kinetic coefficient to couple to `∂_iχ̇`, not to `χ̇`.
* `A3` **known-healthy control**: at `c₁ = −c₃ = K_B` the `(∂_i∂_jχ)²` term is a structural zero and
  `c_T² = 1` exactly, at *every* `K_B`. The machinery returns the certified answer.
* `A4`, `A5` **known-bad controls**: it returns a negative kinetic coefficient at `c₁₄ < 0` and
  `c_T² = 1.25` at `c₁₃ = 0.2`. The test has teeth in both directions.
* `A6` cross-check: the decoupling-limit clock speed from this derivation is `c₂/c₁₄ = 1.679312732`, equal
  to `σ*` to ten digits.

`B1–B10` rebuild L44's escape independently:

| quantity | L52 (rebuilt here) | L44 |
|---|---|---|
| `a_UV` at `D₀ = 0.13`, `q = −1.29078` | **0.0173858743518** | 0.01738587435 |
| `a_UV` over the collar, `D ∈ [0.05, 0.50]` | **[0.0049900365, 0.034839244]** | [0.00499, 0.03484] |
| `a_UV` with the Schur term REMOVED | **[−192.4931, +184.8891]** | [−192.49, +184.89] |
| switch-dependence tolerance `\|G\|` | **3.656×10⁻⁵** | 3.66×10⁻⁵ |
| `b`-weighted integral, total-derivative piece | **2.67×10⁻⁵⁵** | 2.13×10⁻⁶⁵ |
| `b`-weighted integral, Schur piece | **1.362082×10⁻⁴** | 1.362×10⁻⁴ |

All three of L44's load-bearing structural facts reproduce: the pin term's momentum content is a
**structural zero** so L35's weight `b` vanishes identically (`B1`); L35's own cancellation
`t/6 + h_qq/2 = 0` **survives untouched** (`B2`); and the coefficient is the auxiliary's Schur complement
`a_UV = −h_qz²/(2h_zz) = A²/(4D + 24E₄z²)`, with the D-free positivity identity
`a_UV = A²z/[2(−Aq + 8E₄z³)]` (`B3`, `B6`). The negative control fires (`B8`), and the repair covers
switch dependence only below `|G| < 3.66×10⁻⁵` (`B9`) — the escape works because `G` is a structural zero,
not because the Schur term is large.

*(The total-derivative integral differs from L44's at the 10⁻⁵⁵ vs 10⁻⁶⁵ level. Both are zero to the
quadrature's own accuracy at their respective working precisions; the statement being checked — that it is
zero against a Schur piece of 1.36×10⁻⁴ — holds by 51 orders either way.)*

---

## 2. THE TABLE — every quadratic coefficient of the deposited theory

The enumeration is complete on two independent tests. **Bookkeeping** (`C0`): 6 scalar perturbations
(4 metric + `χ` + `δφ`) − 2 gauge − 2 constraints = **2**; 4 metric vector components − 2 gauge −
2 constraints = **0**; 2 tensor = **2**; total **4**, matching the deposited theory's own count. So the
quadratic form is exactly a tensor pair, an empty vector sector, a 2×2 scalar *kinetic* Hessian, a scalar
*gradient* Hessian split longitudinal/transverse by the background `∇φ̄`, and the `ξ²` quartic — there is
nowhere else for a coefficient to hide. **Assignment** (`C0b`): each of the ten terms in `THE_ACTION` §1
maps to at least one row.

Operative point used for every row, and checked admissible (`C3b`): `K_B = 0.1`, `σ = σ* = 1.679312732`,
`c₁₄ = 1.978×10⁻⁶` (its α₂ ceiling), `c₂ = σ*c₁₄ = 3.3217×10⁻⁶`, `|K₂| = (2−K_B)²/c₂ = 1.0868×10⁶`
(0.60 of the Cherenkov cap). Both a₀ footings, **9.3619×10⁻¹¹ / 1.1279×10⁻¹⁰ m s⁻²**, wherever a number is
dimensional.

| # | coefficient | where evaluated | verdict | Schur repair? | mode cost |
|---|---|---|---|---|---|
| **C-T1** | graviton kinetic `(1−c₁₃)/16πG` | **every** parameter value | **strictly positive** (`= 1/16πG`) | not needed | — |
| **C-T2** | graviton gradient, `c_T² = 1/(1−c₁₃)` | **every** parameter value | **strictly positive**, `= 1` exactly | not needed | — |
| **C-K1** | clock kinetic `2c₁₄k²` | `c₁₄ = 1.978×10⁻⁶` | **marginal as `c₁₄ → 0`**; positive here | **yes, but degenerate** — the Schur complement is exactly `δc₄`, and `α₁ = −4c₁₄` moves with it | +0 |
| **C-K2** | clock `(∂_i∂_jχ)²`, coefficient `−c₁₃` | **every** parameter value | **structural zero** (by design; this is what gives `c_T = c`) | not needed | — |
| **C-K3** | clock gradient `2c₂k⁴` | `c₂ = 3.3217×10⁻⁶` | **marginal as `c₂ → 0`**; ~4 orders below the certified-healthy 0.01–0.1 (H-F) | degenerate with the `c₂` operator itself | +0 |
| **C-S1** | MOND scalar time-kinetic `2\|K₂\|` | `\|K₂\| = 1.0868×10⁶` | **strictly positive** (sign of `K₂` is a *convention choice*, not derived) | not needed | — |
| **C-X1** | clock–scalar kinetic mixing | every background with `Y = 0` | **identically zero — antisymmetric** | **none available**: a gyroscopic coupling has no Schur complement | — |
| **C-D1** | kinetic-Hessian determinant `4c₁₄\|K₂\|k²` | the closure locus `c₂\|K₂\| = (2−K_B)²` | **strictly positive and `c₁₄`-independent**, `= 4k²(2−K_B)²/σ = 8.599k²` | not needed | — |
| **C-L2** | scalar transverse stiffness `(2−K_B)J_Y` | `s → 0` (every zero of `∇φ̄`) | **marginal → 0** (`~√s`) | yes, but **redundant** — it is `J → J + κY`, a canonical kinetic term | +0 |
| **C-L1** | scalar longitudinal stiffness `(2−K_B)/Δ′` | `s > 2.540`: **all** of the Solar System, galaxy cores, cluster cores | ***sign-indefinite AND divergent*** | **YES — series arrangement only** | **+0** |
| **C-L3** | coherence quartic `ξ²(2−K_B)J_Y` | `Ȳ = 0`, with `ξ²` **inside** `J` | **marginal → 0** — a live placement fork | not needed: placing `ξ²` **outside** `J` makes it a positive constant (g03c) | — |
| **C-W1** | `J_T`, the construction's tensor balance | `σ = σ*` | **marginal at the window's upper edge**; `J_T = 0.04664 > 0` here, 5.49% of margin | window edge, not a failure | — |
| **C-W2** | `S₄′`, the construction's quartic obstruction | `σ = 1.6793` (lower edge) | **sign flip** — the window's lower edge *is* this zero | by construction | — |
| **C-U1** | IC20 scalar UV `a_UV = A²/(4D + 24E₄z²)` | the whole width-.006 collar | **strictly positive**, [0.00499, 0.03484] | **already repaired** — L44's, parallel arrangement | +0 |

**Seven marginal or sign-indefinite** (C-K1, C-K3, C-L2, C-L1, C-L3, C-W1, C-W2); **two structural or
identical zeros** (C-K2, C-X1); **five strictly positive** (C-T1, C-T2, C-S1, C-D1, C-U1).

### Three things the table shows that were not visible before it existed

1. **The deposited action contains exactly one field–field mixing, and it is antisymmetric** (`A7`, C-X1).
   `2(2−K_B)J^μ∂_μφ` carries one time derivative; its symmetric part is a total derivative and drops. So
   **no Schur complement is available anywhere in the deposited action as written** — every repair must
   *add* an auxiliary. That is why the technique has never fired here by accident.
2. **The clock's marginality does not degenerate the Hessian** (C-D1). On the closure locus
   `c₂|K₂| = (2−K_B)²` with `c₂ = σc₁₄`, the product `c₁₄|K₂| = (2−K_B)²/σ` is **independent of `c₁₄`** —
   as PPN squeezes the clock's kinetic coefficient toward zero, the scalar's stiffens by exactly the
   reciprocal amount and the determinant sits at `8.599k²`. This is a genuinely reassuring result and it
   only shows up when the two coefficients are written next to each other.
3. **`Σ_∥` is marginal at *both* ends.** It is `+∞` at high acceleration and `→ 0` as `s → 0` (`C-L1d`:
   `3.8×10⁻⁴` at `s = 10⁻⁸`). Every previous discussion has been about the high end.

---

## 3. The generalisation: a holonomic auxiliary attaches two ways, and they are opposite

This is the lane's structural result, proved symbolically in Section D.

**PARALLEL** (`D1`) — the auxiliary mixes with the dangerous variable itself, as in IC20's `A q z`:

```
  [[h_qq, A], [A, −D]]   →   h_qq − A·A/(−D)  =  h_qq + A²/D          STIFFNESSES ADD
```

A marginal `h_qq = 0` becomes strictly positive. **Raises a floor.** This is L44's case exactly.

**SERIES** (`D2`) — the dangerous function is moved *onto* the auxiliary and tied back by a quadratic
spring, `L = −[f(w) + λ(v − w)²]`:

```
  Schur  =  −2λ f''/(f'' + 2λ)          i.e.   1/Σ_eff = 1/Σ + 1/λ     COMPLIANCES ADD
```

A divergent `Σ = ∞` becomes `Σ_eff = λ`. **Lowers a ceiling.** Same technique, other end of the auxiliary.

**THEOREM `D3` — why the technique had not applied a second time.** The parallel shift `A²/D` is *finite*
for every finite `(A, D ≠ 0)`, so a divergent coefficient stays divergent. Forcing the shift to diverge
means `D → 0`, and there the auxiliary's own Hessian entry vanishes, its equation collapses to the
constraint `A v = 0`, and it **deletes** the mode instead of repairing it. Computed instance (`D3b`): at
`Σ = 10¹⁶`, parallel with `A²/D = 100` gives `1.0000000000000001×10¹⁶` (no repair); series with `λ = 10⁴`
gives `9999.99999999999` (repaired).

**MODE COUNT (`D4`, `E4`).** An auxiliary carrying no derivatives adds **zero** propagating modes —
*provided its own Hessian is invertible*. Invertibility and the definite-sign requirement are the **same**
condition. Give the same auxiliary a kinetic term and it propagates: +1 for a scalar, +3 for a vector,
taking the deposited theory from 4 modes to 5 or 7 against a stated requirement of 2. "Holonomic" is not a
stylistic preference; it is the entire mode-count budget.

---

## 4. The repairs, one at a time, each with its mode cost

**E1 — clock kinetic (C-K1). Applies, buys nothing. Mode cost +0.**
A holonomic auxiliary vector `Z^μ` mixing with the clock's own acceleration `a_μ = n·∇n` *does* give a
Schur complement, and it is **exactly** `(A²/4D)(n·∇n)²` — a shift of `c₄`. Hence `δc₁₄ = A²/4D` and
`δα₁ = −4δc₄`: the PPN lock `α₁ = −4c₁₄` moves *with* the repair. Generalising (`E1b`), any holonomic
auxiliary whose Schur complement is a local quadratic in `∇_μn_ν` spans exactly the space already spanned
by `c₁…c₄`, so **no Schur repair of the clock sector can separate the kinetic coefficient from `α₁`.**
(Which is also why C-K1's marginality is not urgent: `c₁₄ = 1.978×10⁻⁶ > 0`, and the khronon's
strong-coupling scale is `1.5×10¹⁶ GeV`. Small, not broken.)

**E2 — transverse stiffness and the coherence quartic (C-L2, C-L3). Applies, redundant. Mode cost +0.**
A parallel Schur complement adds a positive constant to `Σ_⊥`, but the resulting operator *is* `J → J + κY`,
the canonical kinetic term already available inside `J`; and the programme's own alternative — placing `ξ²`
**outside** `J` with its own coefficient — removes the same marginality by a placement choice at identical
PPN (g03c). Nothing new. **But the fork itself is a real finding**: with `ξ²` *inside* `J`, the coherence
operator's coefficient is `ξ²J_Y`, which vanishes at exactly the backgrounds — MOND saddle points, symmetry
centres — where the operator is supposed to do its work.

**E3 — the longitudinal stiffness (C-L1). THE ONE THAT IS NEW. Mode cost +0.**

Construction: replace `−(2−K_B)J(Y)` by

```
  −(2−K_B) [ J(W·W) + λ (V − W)·(V − W) ] ,        W_μ = q_μ^ν W_ν  spatial, NO derivatives on W
```

keeping the `ξ²` operator on `V` so that `W` stays algebraic. Varying `W` gives
`J_Y(W²)W = λ(V − W)` — holonomic. Varying `φ` and applying Gauss on a sphere gives, exactly,

```
  Δ_eff(s) = Δ(s) + κ s ,      κ = 1/(2λ) ,      1/Σ_eff = Δ′(s) + κ ,      Σ_eff ≤ 1/κ everywhere
```

`E3b`, computed at Saturn's orbit on both footings:

| `κ` | cap `1/κ` | `Σ_∥` at Saturn, before → after | renormalisation of the action's `G`, `a₀` |
|---|---|---|---|
| 10⁻⁶ | 10⁶ | 9.617×10¹⁵ → 1.0×10⁶ | 0.0001% |
| 10⁻⁴ | 10⁴ | 9.617×10¹⁵ → 1.0×10⁴ | 0.01% |
| 10⁻² | 10² | 9.617×10¹⁵ → 1.0×10² | 1% |
| 10⁻¹ | 10 | 9.617×10¹⁵ → 10 | 10% |

*(`1/Δ′` at Saturn on the deposited C-family kernel: **9.617×10¹⁵ canonical / 5.759×10¹⁵ alt**, against
`THE_COMPLETE_THEORY`'s 9.4×10¹⁵ / 5.6×10¹⁵ — a 2–3% difference, consistent with a different Saturn
semi-major-axis convention. `C-L1c`.)*

`E3c`: it works on the **published flat kernel** too, where `Δ′ = 0` exactly — `Σ_eff = 1/κ` there.
`E3d`: **+0 propagating modes**; the total stays 2 tensor + 1 clock + 1 scalar = 4.
`E3e`: **the condition, stated exactly** — the repair is valid iff `J` is convex in `|V|`, i.e. `Δ′ ≥ 0`
everywhere, because the auxiliary's Hessian is `Σ_∥ + λ` and it must not change sign. It **holds** for the
published flat kernel and for the deposited C-family (`min Δ′ = 3.8×10⁻¹⁷ > 0`); it **fails** for the raw
decreasing ν_RAR (`min Δ′ = −0.0324`). That is an honest limit, not a caveat added afterwards.

---

## 5. Pricing E3, on both footings

**Cost 1 — the Solar System: zero (`F1`).** The repair adds a force `κ g_N`, exactly Newtonian in shape, so
`∇·(κ∇Φ_N) = κ·4πGρ_b` and the phantom density is **identically zero in vacuum**. The Pitjev–Pitjeva bound
on phantom mass inside Saturn's orbit is untouched, and the ephemerides fit `GM_⊙` anyway, so a constant
rescaling is invisible to them.

**Cost 2 — the only observable price (`F2`).** The **action's** `a₀` and `G` differ from the **measured**
ones by `(1 + κ)`:

| footing | measured a₀ (m s⁻²) | action's a₀ at κ = 10⁻⁴ | at κ = 10⁻² |
|---|---|---|---|
| canonical | 9.3619×10⁻¹¹ | 9.3628362×10⁻¹¹ | 9.455519×10⁻¹¹ |
| alternative | 1.1279×10⁻¹⁰ | 1.1280128×10⁻¹⁰ | 1.139179×10⁻¹⁰ |

Both are fitted/measured quantities, so `κ` is absorbed; the 20% spread **between** the two footings is
2000× larger than a `κ = 10⁻⁴` shift.

**Cost 3 — a restatement, not a loss (`F3`, `F3b`).** `Δ_eff = Δ + κs` is *unbounded*, so the bounded-boost
theorem's hypotheses look violated — but the **observable** excess, over the baryonic gravity an observer
computes with the *measured* `G`, is `g_tot − (1+κ)g_N = a₀Δ(s)`, bounded by `Ca₀` exactly as before.
Computed over 201 points across twenty decades at `κ = 10⁻⁴`: `sup = 0.64761 = C`. **This must be stated
explicitly or the theorem will read as broken.** The SPARC ceiling test is unchanged.

**Cost 4 — deep MOND untouched (`F4`).** At `s = 10⁻³`, `κs/Δ = 3.2×10⁻⁶` (κ = 10⁻⁴) and `3.2×10⁻⁴`
(κ = 10⁻²).

**Cost 5 — one new parameter.** `κ` is a free constant, bounded only from below by the `Σ_∥` cap one wants.
The theory gains a parameter it did not have.

**What it buys**, at `κ = 10⁻⁴`:

* `F5` — **L34's standing liability is discharged.** `g_* = 3a₀Δ′²/|Δ″|` grows by `((Δ′+κ)/Δ′)²`:
  **9.25×10²³× canonical / 3.32×10²³× alt at Saturn**, **5.67×10³⁴× / 2.03×10³⁴× at Earth**. L34's "the bare
  kernel is strongly coupled at every planet, 552(p+1) Earth to 3.8×10⁴(p+1) Jupiter" no longer holds.
* `F5b` — the longitudinal cone shortens by `√(Σ_before/Σ_after)` = **9.81×10⁵× / 7.59×10⁵×** (a ratio, so
  free of the `|K₂|` and `(2−K_B)` normalisation).
* `F6` — **A19's stated cost is discharged**: "on the saturated branch `Δ′ = 0 ⇒ Σ_∥ = ∞`, so the scalar's
  cubic action is unwritable and the action is not C² at the Solar-System background." `Σ_eff ≤ 1/κ` and
  `J_YY = (Δ − sΔ′)/(2a₀²Δ³Δ′)` has `Δ′ ≥ κ` in its denominator.
* `F7` — **L30's gate G2 is discharged with the published kernel unchanged**: "the exact fourth-order static
  equation cannot be written down at all until a continuation is chosen." The vertical segment at `w = Ca₀`
  becomes a slope-`1/κ` segment; no continuation is needed, and
  `THE_COMPLETE_THEORY` §4.2's "an attained supremum is inadmissible" erratum is no longer forced.

**What it does NOT buy, stated (`F8`, `F9`).** It does not make the published splice C² — `Δ″` jumps at
`s_sat = 2.540` and adding `κs` is smooth, so a separate C² mollification is still needed (or carry the
smooth C-family). And it does **not** rescue the raw decreasing ν_RAR or the AQUAL arm of §4.4's fork:
`Δ′ < 0` makes the auxiliary equation multivalued. **The kernel fork stays open.**

---

## 6. The single most valuable repair, and what it would buy

**E3, the series Schur repair of the longitudinal stiffness.** It is the only one of the seven marginal or
sign-indefinite coefficients that is both repairable and not already covered by an operator the action
carries. What it buys, in one line: **it turns the theory's worst-behaved coefficient — infinite at every
background where the Solar System actually lives — into a bounded one, for zero propagating modes, zero
ephemeris signature, and one new constant whose only trace is a `(1+κ)` shift in the action's own `a₀` and
`G`; and in doing so it discharges three separately recorded liabilities (A19's unwritable cubic action,
L34's strong coupling at every planet, L30's unwritable fourth-order equation) with the published kernel
left exactly as printed.**

Caveats that must travel with it: `κ` is a new free parameter; the bounded-boost statement must be rewritten
in terms of the excess over the *measured* baryonic gravity or its hypotheses read as violated; the repair
requires `J` convex in `|V|`, so it does not reopen the decreasing-Δ arm of the kernel fork; and it is a
*construction*, verified here at the level of the quadratic form and the static Gauss relation — a full
Dirac constraint analysis of the (`g`, `τ`, `φ`, `W`) system has **not** been done and would be the next
step before it is claimed as a completed repair.

---

## 7. Verdict

**A second application of L44's technique exists, and the reason nobody found it is that the technique has
two arrangements which do opposite things — L44 stumbled onto the one that raises a floor, while the
programme's outstanding sore point needs the one that lowers a ceiling.** The sweep is otherwise a clean
enumeration: fourteen quadratic coefficients, seven marginal or sign-indefinite, but five of those seven are
either window edges, limits the theory does not occupy, or already covered by an operator in the action —
and the deposited action's only existing mixing is antisymmetric, so it offers no Schur complement at all
and every repair must add an auxiliary. **The one live candidate, the series repair of `Σ_∥`, is cheap
(zero modes, zero ephemeris signature, one new constant) and discharges three standing liabilities at once,
but it is a construction verified at quadratic order and on the static Gauss relation only — it should be
handed on as a proposal with a named next step (a Dirac count of the four-field system), not as a closure.**
