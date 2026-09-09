# L30 — J(Y) beyond saturation: the continuation exists, and it makes a gate computable that the theory then fails

2026-09-08. Lane L30 of [CHARTER.md](CHARTER.md), opened by [L13_STRONG_COUPLING.md](L13_STRONG_COUPLING.md)'s check P9.
Script: [L30_saturated_branch.py](L30_saturated_branch.py) → [L30_saturated_branch.out](L30_saturated_branch.out).
**13 PASS, 10 FAIL. All 7 controls PASS** (K0–K6); every FAIL is a substantive finding. Runtime 79 s.

## Verdict in three sentences

An admissible continuation exists and is essentially unique in effect: the minimal C² repair reproduces the
published saturated kernel to within **0.008 a₀ at every acceleration**, so the hole L13 named is real but
cosmetic as far as any observable the programme currently computes is concerned. What the repair buys is
that the action's own static equation `∇·[J_Y∇φ] − ξ²∇⁴φ = 4πGρ` can be *written down and solved* for the
first time — and when it is solved, the Solar-System coherence-length floor is **4.0 pc, twenty-seven times
the standing 0.15 pc**, because the point source forces the scalar's gradient to the biharmonic cone
`GM/(2ξ²)` and therefore `M_ph(<r)/M = r²/(2ξ²)` exactly, independent of the kernel, of a₀, and of the Sun's
mass. That number was never seen because neither gate machinery in the repository solves that equation: the
standing floors come from a linear filter applied to the QUMOND phantom density (g02/g03b/g03x) or from an
AQUAL-form PDE in which the point source is carried by the *harmonic* Newtonian potential and the ξ⁴
operator is inert on it (g03c/g03d) — so the term `Δ′ = 0` removed is a term neither gate ever used.

## 1. The problem, set up from the action

The action (`THE_ACTION_2026-09-05.md` §1) carries `−(2−K_B) J(Y)`, `Y = V·V = |∇φ|²`, plus the AeST coupling
`2(2−K_B) J^μ∂_μφ`. Varying φ statically gives the equation PAPER5 §7 and `g03x`'s own docstring assert:

    div[ J_Y(Y) grad phi ] = 4 pi G rho    ⇒   J_Y(g_phi) g_phi = g_N   on a sphere.

With `g_φ = a₀ Δ(s)`, `s = g_N/a₀`, everything the scalar's quadratic and cubic actions need is fixed:

| object | value | role |
|---|---|---|
| `Σ_⊥ = J_Y(s)` | `s/Δ(s)` | transverse gradient stiffness |
| `Σ_∥ = J_Y + 2 Y J_YY` | `= d g_N/d g_φ = 1/Δ′(s)` | longitudinal gradient stiffness |
| `L₂` | `Σ_∥ (∂_∥δφ)² + Σ_⊥ |∂_⊥δφ|²` | the quadratic action |
| `L₃` | `2 J_YY (V̄·∂δφ)|∂δφ|² + (4/3) J_YYY (V̄·∂δφ)³` | the cubic action |
| `J_YY` | `(Δ − sΔ′)/(2a₀²Δ³Δ′)` | every cubic vertex |

**Every cubic coefficient carries `J_YY`, whose denominator is `Δ′`.** So `Δ′ → 0` is not a modelling nicety:
it is where the quadratic action degenerates (`Σ_∥ → ∞`, the longitudinal mode becomes a constraint rather
than a propagating direction) and the cubic action ceases to exist. Approaching the maximum from *below*, on
ν_RAR's own branch, `J_YY` runs 1.8×10²³ → 1.8×10²⁴ → 2.2×10²⁵ at `s/s_sat = 0.99, 0.999, 0.9999`. The
divergence is the *maximum of Δ*, not the splice, so **no choice of "what happens above s_sat" removes it
without moving the maximum** — which is exactly what a continuation must do.

Controls: K0 reproduces `s_sat = 2.540`, `C = 0.6476`; K1 reproduces PAPER5 Table 1's five ceilings; K2
verifies `Σ_∥ = J_Y + 2YJ_YY = 1/Δ′` to 2×10⁻¹⁶.

## 2. The conditions, and the two theorems

    C1  bounded boost         Delta <= C_max                    (PAPER5's theorem)
    C2  single-valued carrier  s -> Delta(s) invertible          (the carrier theorem)
    C3  positive stiffness     Delta'(s) > 0 strictly, all s     (well-posedness of the static PDE)
    C4  C^2                    Delta in C^2, J in C^3 on its domain
    C5  Newtonian limit        the residual force a0 Delta must not GROW

**THEOREM L30-1.** C1 + C3 force Δ strictly increasing and bounded, hence convergent to a finite
`C_∞ = sup Δ > 0`. So (a) **the conditions are mutually satisfiable** — three explicit constructions below —
and (b) **the residual scalar force tends to the constant `C_∞ a₀` and never to zero.**
*Corollary:* no kernel whose excess vanishes in the Newtonian limit can be carried by a matter-sourced
scalar, ν_RAR included. Measured on ν_RAR itself: `Δ′ < 0` on 33% of the range, minimum `Δ′ = −0.0324`.
C5 in its weak reading ("does not grow") survives; the strong reading ("vanishes") is incompatible with C3.
**The published saturated kernel already pays this price in full — the continuation does not add it.**

**THEOREM L30-2.** C1 + C3 require `J_Y(Y) → +∞` as `Y → Y_max = (C_∞a₀)²`, because `J_Y(g_φ) g_φ = g_N`
must run to infinity while `g_φ` stays below `C_∞a₀`. So **J is defined only on `[0, Y_max)` with a vertical
asymptote at the endpoint**: `|∇φ| < C_∞ a₀` is a hard kinematic bound, Born–Infeld-like in structure. This
is not an extra assumption — it is what "bounded boost, carried by a scalar" *means* at the level of J.

**T3 (FAIL).** Neither kernel in the repository meets all five, and they fail on *complementary* conditions:
the published saturated kernel meets C1, C2, C5 and violates C3 and C4; unsaturated ν_RAR meets C4 and C5 in
its strong form and violates C2 and C3.

## 3. Three explicit continuations

**A — pole family (closed form in J).** `J_Y(u) = u/(1 − (u/C_∞)^p)` with `u = Δ`, so `s(u) = u²/(1 − (u/C_∞)^p)`
exactly; the inverse is computed to machine precision in two charts (`u` deep, `ε = 1 − u/C_∞` near the
ceiling, where `1 − (u/C_∞)^p = −expm1(p·log1p(−ε))` avoids cancellation). Fitted to ν_RAR on
`10⁻³ ≤ s ≤ s_sat`: **C_∞ = 0.7400, p = 1.600, max |Δ_A − Δ_RAR| = 0.0128 a₀.** Deep-MOND exact.

**B — saturating tanh.** `Δ_B(s) = C_∞ tanh(√s/C_∞)`, exact deep-MOND by construction, closed form both ways
(`J_Y(u) = C_∞² artanh²(u/C_∞)/u`). Fitted **C_∞ = 0.6270, max deviation 0.0301 a₀.**

**C — the minimal C² repair, and the one to adopt.** Exactly ν_RAR for `s ≤ s₁ = 2.0`; above it

    Delta_C(s) = D_inf - A (1 + beta (s - s1))^-2 ,
      D_inf = 0.655589,  A = 1.317369e-02,  beta = 0.801759

with the three constants fixed *uniquely* by matching `Δ = 0.642415`, `Δ′ = 2.112425×10⁻²`,
`Δ″ = −5.080967×10⁻²` at `s₁`. Verified: the two branch formulas agree in value, first and second derivative
at `s₁` to 5×10⁻⁹. **`max |Δ_C − Δ_RAR| = 0.0016 a₀` on the fitted range, and `max |Δ_C − Δ_published| =
0.0080 a₀` at EVERY s.** This is the answer to "what is J(Y) beyond saturation": the published kernel, with
its plateau tilted upward by at most eight thousandths of a₀.

All three satisfy C1–C5 (checks E[A], E[B], E[C] PASS; Δ′ from analytic derivatives, cross-validated against
a central difference of Δ to ≤1.3×10⁻⁸ over `0.2 ≤ s ≤ 5`).

**The rate of approach to the ceiling is a real physical output**, `log₁₀ Σ_∥ = −log₁₀ Δ′`:

| background | s | A (power law) | B (exponential) | C (rational tail) |
|---|---|---|---|---|
| Saturn, 9.54 AU | 6.96×10⁵ | 12.3 | 1158.3 | 18.9 |
| Earth, 1 AU | 6.33×10⁷ | 16.2 | 11029.0 | 24.8 |
| inner galaxy, g_N = 10 a₀ | 10 | 2.6 | 4.6 | 4.3 |
| inner galaxy, g_N = 100 a₀ | 100 | 4.6 | 14.6 | 7.4 |

The published kernel gives `+∞` in every row with `s > 2.540`. **B is admissible on the letter of C3–C4 and
useless in practice**: `Σ_∥ ~ e^{2√s}` means 10^1158 at Saturn's orbit, formally finite and not something any
effective theory expands in. A power-law approach (A, C) gives `Σ_∥ ~ s²–s³` and a usable EFT. That is a
genuine selection criterion the conditions alone do not supply, and it favours the minimal repair C.

## 4. Gate 1 — the standing Solar-System gate does not discriminate (G1 FAIL)

Using the repository's own machinery, `g02_filtered_efe.py`'s `phantom_density` / `observables` imported
unedited exactly as `g03x` imports them (control **K3** reproduces g03x's published ν_RAR-carried floors,
0.10 pc canonical / 0.15 pc alt, exactly):

| kernel | floor ξ, canonical | floor ξ, alt |
|---|---|---|
| published, saturated | 0.10 pc | 0.15 pc |
| continuation A | 0.10 pc | 0.15 pc |
| continuation B | 0.10 pc | 0.15 pc |
| continuation C | 0.10 pc | 0.15 pc |

Identical, to the grid. The reason is structural: this gate builds the QUMOND phantom density from `ν(s)`
and applies a **linear output filter** of length ξ. It never evaluates `Δ′` at all. **The term that `Δ′ = 0`
removed is not a term this gate ever used**, so its passing was never evidence about the saturated branch
one way or the other.

## 5. Gate 2 — the exact fourth-order equation, writable only now (G2 FAIL)

With the coherence operator outside J (the placement `g03c` certifies as uniformly elliptic), the action's
static scalar equation in spherical symmetry integrates once to, exactly,

    J_Y(w) u  -  xi^2 ( u'' - 2 u'/r )  =  G M ,      u = r^2 w ,   w = |grad phi| = g_phi .

This needs `J_Y` as a **function** of `w`. The published kernel supplies a vertical segment at `w = C a₀`
(check P2), so **this equation cannot be written down at all until a continuation is chosen.** It is solved
here by damped Newton in the variable `q(r) ≡ s(w(r))`; the Jacobian is `a₀r² + (stencil)·r²a₀Δ′(q)`, so the
continuation's `Δ′` is the entire nonlinear content. (A lagged-`J_Y` Picard scheme has amplification
`1 − Σ_∥/Σ_⊥` and diverges outright on precisely this branch — verified in development. Either way the solve
is impossible without the missing input.)

Controls: **K4** the same stencil with `J_Y = 0` reproduces the exact biharmonic cone `w = GM/(2ξ²)` to
0.003%; **K5** at `ξ → 0` the solver reproduces the algebraic carrier law `w = a₀Δ(g_N/a₀)` to 2×10⁻⁷;
**K6** all 54 solves reproduce the analytic interior prediction `min[GM/(2ξ²), C_∞a₀]` to 0.13%.

**Result, identical for all three continuations and both footings:**

| ξ | w(Saturn) | M_ph(<Sat)/bound | max planetary g_r / gate | verdict |
|---|---|---|---|---|
| 0.10 pc (the standing floor) | 6.97×10⁻¹² | 1.60×10³ | 1.90×10² | EXCLUDED |
| 1.00 pc | 6.97×10⁻¹⁴ | 1.60×10¹ | 1.90 | EXCLUDED |
| 2.00 pc | 1.74×10⁻¹⁴ | 3.99 | 0.476 | EXCLUDED |
| **4.00 pc** | 4.36×10⁻¹⁵ | **0.998** | 0.119 | **admissible** |
| 10.0 pc | 6.97×10⁻¹⁶ | 0.160 | 0.019 | admissible |

**The number is analytic and kernel-free.** Inside the healing length the point source dominates and the
equation degenerates to the biharmonic cone `w = GM/(2ξ²)`, so

    M_ph(<r)/M = r^2 / (2 xi^2)      exactly — no kernel, no a0, no M ,

and the Pitjev–Pitjeva bound `M_ph(<Saturn) < 6.7×10⁻¹¹ M_☉` reads

    xi  >=  r_Saturn / sqrt(2 x 6.7e-11)  =  4.00 pc .

The α = 1 sunward gate gives the weaker 1.38 pc; **Saturn binds, by a factor 2.9.** Both footings give
4.0 pc because a₀ enters neither number.

### Why the two published gate machineries do not see this

- `g02/g03b/g03x` (which produced 0.03 / 0.07 / 0.10 / 0.15 pc): the QUMOND phantom density is computed from
  the kernel and then **filtered**. There is no fourth-order operator and no point source for the scalar.
- `g03c/g03d` (the "exact fourth-order" solve): the equation is AQUAL on the total potential, and the point
  mass is carried by the **harmonic** Newtonian 1/r piece — `∇²Φ_N = 0` away from the origin, so
  `∇⁴Φ_N = 0` and the ξ⁴ operator is **inert on the source**. g03c's own docstring says so: "Newton exact
  inside", and g03d's says the scalar has "no point source".

In the carrier reading — the only reading in which the saturation exists at all, and the reading PAPER5 §7
and g03x Y1 assert and derive their theorem from — the scalar carries the point source itself, its profile
is not harmonic, and the ξ⁴ operator is not inert. **The two readings are not equivalent, and they differ by
a factor of 27 in the Solar-System floor.** That is a concrete, decidable gap in the action as written.

*Consequence, stated and not claimed:* the wide-binary window tops out at 30 kAU = 0.145 pc, 27× smaller than
this floor. At ξ ≥ 4 pc every DR4 pair sits deep inside the healing length. The registered arm-B value
γ_v = 1.0450/1.0300 was computed at ξ = 0.10/0.15 pc. Recomputing it at this floor is **not** done here; the
direction is unambiguous (towards Newton), the magnitude is not asserted.

### The other placement is not equivalent either (S1 FAIL, both footings)

`THE_ACTION` §1 writes the operator **inside** J, as `J(Y + ξ²|∇_⊥V|²)`, and calls the two placements
"equivalent" (identical PPN; `g03c` notes only that the inside placement is degenerate at zero field). Inside
J the interior balance is `−ξ²J_Y(w)∇⁴φ = 4πGρ` with `J_Y` at the *screened* — hence small — gradient, so
`w = GM/(2ξ²J_Y(w))` and, on the deep-MOND branch where `J_Y = w/a₀`, `w = √(GMa₀/2)/ξ`. This is an
asymptotic balance, not a solve; what the script checks is its **self-consistency** — that the resulting `w`
really does land on the deep-MOND branch — and it does, to 0.00% at the floor, for both footings. The floor
it implies:

| placement | floor ξ, canonical | floor ξ, alt |
|---|---|---|
| outside J (solved exactly, §5) | 4.00 pc | 4.00 pc |
| inside J (asymptotic, self-consistency verified) | 585 pc | 642 pc |

a factor 146 / 161 apart. **Neither placement rescues the standing floor, so the §5 conclusion does not hinge
on which is adopted — but they are not interchangeable, and the action does not say which one it means.**

## 6. Gate 3 — the one observable the permanent residual touches (G3 PASS, at 2σ)

Theorem L30-1b says every carriable kernel — the published one and all three continuations alike — leaves a
permanent residual `C_∞a₀` at arbitrarily high acceleration, so `g_obs/g_bar → 1 + C_∞/s`. On SPARC
(Υ_d = 0.5, Υ_b = 0.7, δV/V < 0.10; 2801 points):

| footing | cut | n | median s | measured `g_obs/g_bar` | carried class | unsaturated ν_RAR |
|---|---|---|---|---|---|---|
| canonical | g_bar > 10 a₀ | 91 | 15.6 | 1.0165 ± 0.0121 | 1.0416 (2.1σ high) | 1.0197 (0.3σ) |
| alt | g_bar > 10 a₀ | 68 | 15.6 | 1.0157 ± 0.0133 | 1.0415 (1.9σ) | 1.0196 (0.3σ) |
| canonical | g_bar > 30 a₀ | 13 | 39.5 | 1.0795 ± 0.1193 | 1.0164 (0.5σ) | 1.0019 (0.7σ) |

The check passes at 3σ and is reported as a **diagnostic of direction, not a fit-quality statement**: the
bootstrap error excludes the 0.1 dex stellar-population spread and the Υ freedom. What it shows is that the
saturation's permanent residual sits ~2σ on the high side where the data are most Newtonian, and that the
*unsaturated* kernel — the one a scalar cannot carry — sits closer. This is a cost of carriability itself,
shared equally by the published kernel and every repair, and it is the only place a continuation is exposed
to data at all.

## 7. Where the saturated branch actually lives (G4 FAIL) — a correction to L13

L13's P9 located the pathology at "the Solar-System background". It is not there:

| footing | r where g_N > s_sat a₀, around the Sun | around a 10¹¹ M_☉ galaxy |
|---|---|---|
| canonical | 0.0242 pc (4990 AU) | 7.7 kpc |
| alt | 0.0221 pc (4550 AU) | 7.0 kpc |

The standing coherence-length floor, 0.10 pc, already **exceeds** `r_sat(Sun) = 0.024 pc`, so around a solar
mass the scalar is screened before it ever reaches the saturated branch — its local gradient in the Solar
System is 0.074 a₀ at ξ = 0.1 pc, deep on the ν_RAR branch where `Δ′` is perfectly healthy. **The pathology's
home is the inner few kiloparsecs of every galaxy and the cores of clusters**, over volumes vastly larger
than ξ, where the field really does sit on the plateau. That is where `Σ_∥ = ∞` means the static operator is
degenerate in the longitudinal direction, and where a non-spherical source (a disc) makes the difference
between `Σ_∥ = ∞` and `Σ_∥ = 10^4` a statement about a solvable versus an ill-posed boundary-value problem.
L13's number is right; its address is wrong.

## PASS/FAIL, verbatim

See [L30_saturated_branch.out](L30_saturated_branch.out). 7 controls (K0–K6) PASS. The ten FAILs are:
P1 (Σ_∥ infinite at the published kernel's own Solar-System background — L13 P9 reproduced), P2 (`J_Y(Y)` is
not a function: a vertical segment at `Y = (Ca₀)²`), P3 (the cubic vertex `J_YY` is infinite), T3 (neither
published kernel meets all five conditions, and they fail on complementary ones), T2 (no admissible
continuation has a vanishing Newtonian-limit residual), G1 (the standing gate cannot discriminate any
continuation from the published kernel), G2 (the exact fourth-order equation needs ξ ≥ 4.0 pc, 27× the
standing floor), S1 twice (the two placements of the coherence operator give floors 146× and 161× apart,
against the action's "equivalent"), and G4 (the saturated branch is not realised near the Sun — it lives in
galaxy interiors).

## Scope — what is not done here

The Cassini quadrupole is evaluated only inside Gate 1's axisymmetric machinery; the exact fourth-order solve
of §5 is the spherical monopole, which is the binding gate there anyway (the Saturn phantom mass exceeds the
sunward gate by 3×). No two-body or wide-binary quantity is recomputed. The residual-force statement is for
an isolated point mass; an extended source of size ≫ ξ is unaffected, which is why galaxies do not inherit
the 4 pc problem. The `L₃` coefficients are read off the expansion of `J(Y)` and are not carried to a
strong-coupling scale for the MOND scalar as L13 did for the khronon. `a₀` enters nothing in the 4 pc number,
so the two footings do not separate it.
