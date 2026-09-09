# L64 — the screened solve, done: the repair survives, the ephemeris cost is not zero but it is not what either party thought, and one of L54's two ceilings does not survive

2026-09-09. Lane L64 of [CHARTER.md](CHARTER.md), doing the one item that
[L54_REPAIR_CONSTRAINTS.md](L54_REPAIR_CONSTRAINTS.md) and the lead's
`closure_2026/integrable_clock_construction_2026/L52_REPAIR_SCOPE_REVIEW.md` **independently named as
the only thing still open**:

> L54 §6: *"the screened fourth-order solve is the one named item still open."*
> the lead: *"The correct next step on L52 is a normalized nonlinear static solve, then metric/clock
> variation and Dirac closure. Do not import a zero ephemeris cost into IC39."*

Script: [L64_screened_solve.py](L64_screened_solve.py) → [L64_screened_solve.out](L64_screened_solve.out).
**31 checks, 31 PASS, exit 0, 67 s.**

Method: every control the brief names is reproduced before anything rests on it — including the lead's
counterexample in exact rational arithmetic. The solve uses **two independent solvers**: a 1-D radial
fourth-order solver written here and validated against g03d's own published control numbers, and
**the repository's own axisymmetric fourth-order solver `g03d.solve4`**, driven with the carried kernel
and with the repaired kernel, reproducing its own V1 control first. Nothing under
`closure_2026/integrable_clock_construction_2026/` was read or imported. Both footings,
**9.3619×10⁻¹¹ / 1.1279×10⁻¹⁰ m s⁻²**, on every dimensional number. Polarity: every check asserts a
statement and PASS means the statement is true; each line says whether that is good or bad for the repair.

---

## The short answer, in three sentences

**The repair survives the screened solve.** With the coherence operator on, at the carried kernel's own
Solar-System floors and on both footings, the nonlinear static solve converges, the auxiliary still costs
zero propagating modes with `ξ ≠ 0`, and the phantom mass inside Saturn's orbit — **computed from the
solved field rather than assumed** — comes out at **0.68 (canonical) / 0.38 (alt)** of the Pitjev–Pitjeva
bound and **improves** as `1/(1+κ)`. **But the two numbers L54 attached to that row were both wrong, in
opposite directions**: its baseline margin of 333× is really **1.5×**, and its upper ceiling
`κ ≤ 3.1×10⁻⁴` **does not exist at all** — the row is monotone in the repair's favour, so the only
surviving bound on `κ` from above is L54's *soft* Cherenkov ceiling ≈ 1.6×10⁻⁶. **And the lead was
right about the identity**: `P_r` is not `g_N`, the flux falls to 1.4% of the Newtonian source by
10 `r_M`, so `Δ_eff = Δ + κs` survives **exactly as a relation in the flux and not in `g_N`** — it is
invisible at Saturn only because the flux there is Newtonian to 1.1×10⁻⁴.

---

## 1. Controls — every one the brief names, including the lead's number

| control | required | returned here |
|---|---|---|
| `A1` L52's D-free positivity identity `a_UV = A²z/[2(−Aq + 8E₄z³)]` | identity | **holds identically**, rebuilt from the branch equation |
| `A2` L52's parallel Schur coefficient at `D₀ = 0.13`, `q = −1.29078` | 0.01738587435 | **0.017385874352** |
| `A5` **the lead's exact counterexample** at `Σ = λ = X = 1` | **1/6** vs naive 1 | **exactly 1/6**, in rationals; and the `X → 0` limit is `1/λ` exactly |
| `A6` the lead's isolated-auxiliary Poisson matrix | `[[0, −(Σ+λ)],[Σ+λ, 0]]`, det `(Σ+λ)²` | **reproduced**, no tertiary |
| `A7` an independent Dirac counter, on four systems built here | 1 / 2 / 3 / 1 | **1 / 2 / 3 / 1**, with 2 first class (Maxwell), 2 second class (Proca), 2 second class (auxiliary) |
| `A9` L54 re-run as a subprocess | 73/73, controls 2 / 3 / 5 / 3 | **73 PASS, 0 FAIL, exit 0; 2 / 3 / 5 / 3** |
| `C1` this lane's 1-D solver vs **g03d's own V3** | kept 0.8097 (ε=0.3), 0.3679 (ε=1.0) | **0.80973 / 0.36790** |
| `C2` this lane's solver vs **g03d's V2** | scalar identically zero | **max\|v\| = 0** |
| `C3` **g03d's own solver** vs its published V1 | Q₂ = +2.097×10⁻²⁶ s⁻² | **+2.0971 / +2.0967 / +2.0968 ×10⁻²⁶** |
| `C4b` the **unscreened** carried kernel's Saturn phantom vs **L54's own bare number** | 1.4005×10⁴ / 1.6873×10⁴ × bound | **reproduced to 4 digits** |

`C4b` matters more than it looks: it pins this lane's `M_ph` definition to L54's, so the screened numbers
in §5 are compared like for like rather than across a definitional gap.

**`A8` extends L54's count to the thing L54 did not do**: the same algorithm run on the repaired scalar
sector **with the coherence operator on** returns 1 mode without the auxiliary, 1 with it, 1 even at
`σ_∥ = 10¹⁶` (the saturated branch), with exactly **three second-class pairs**; and both negative controls
fire — giving `W` a kinetic term takes the sector to 4, and forcing `σ_∥ + Λ = 0` **deletes** the scalar
mode, leaving 0.

---

## 2. The normalisation, settled and stated once

**`B1`, derived rather than asserted.** Varying THE_ACTION §1's two scalar terms
`2(2−K_B)J^μ∂_μφ − (2−K_B)J(Y)` with respect to `φ` gives `∇·[2(2−K_B)(a − J_Y V)] = 0`, so on a sphere
with decay at infinity

```
    J_Y(g_phi) g_phi = g_N        ← THE CONVENTION USED EVERYWHERE BELOW
```

**with no factor of two** — the 2 in the coupling and the 2 from differentiating `Y = V·V` cancel exactly.
So **L52 line 633's `g_N = 2 J_Y w` is a factor-two slip** and THE_ACTION §3 is right. In this convention
`J_Y(s) = s/Δ(s)`, `f(w) = J(w·w)` has `f′(w) = 2g_N` and `f″(w) = 2σ_∥`, and
`σ_∥ = dg_N/dg_φ = 1/Δ′(s)`.

**`B2`.** In the fixed convention the series repair gives `Δ_eff = Δ + κs` with **`κ = 1/λ`**, confirming
L54's `A11b` and correcting L52's `E3`, which carried `κ = 1/(2λ)`.

**`B3` — the factor is NOT inert for pricing, exactly as the lead said.** It enters the transverse scalar
speed `c_⊥² = (2−K_B)J_Y/|K₂|` linearly, so the Cherenkov ceiling
`κ_c = (2−K_B)/|K₂|` moves with it:

| convention | `J_Y` | `κ_c` |
|---|---|---|
| **fixed here** (THE_ACTION §3) | `s/Δ(s)` | **1.7483×10⁻⁶** |
| L52 line 633 | `s/(2Δ(s))` | 8.7413×10⁻⁷ |

L54's D7 ceiling therefore **stands as published** (`κ ≲ 1.6×10⁻⁶`, soft) — but only because L54 carried
`κ` rather than `λ`. Any number quoted in `λ` in L52 must be halved.

**`B4` — a second, larger convention fork, flagged and not closed.** THE_ACTION §1 couples `φ` to the
*clock's* 4-acceleration, which is the **total** field, so a literal variation gives
`J_Y^action = J_Y^§3 + 1`, i.e. `J → J + Y`. Where the repair is priced this is a 9.4×10⁻⁷ relative shift
(at Saturn `J_Y = 1.07×10⁶`), but in deep MOND it is a factor of ~100 and it would move the dark sector's
`c_s² = (2−K_B)J_Y/|K₂|`. §3 is adopted here because every script in the repository uses it.

---

## 3. The solve — the coherent equation, not a differentiated assigned kernel

The equation solved is the theory's own deposited static law (THE_ACTION §4, and the one `g03d` solves):

```
    div[ mu(|grad Phi|/a0) grad Phi ] - xi^2 Delta^2 psi = 4 pi G rho ,   Phi = Phi_N + psi
```

which on a sphere, after integration, **is** the lead's flux identity `P_r − ξ²(Δψ)′ = g_N`. The repair
enters as the constitutive relation the solver is handed:

```
    |grad Phi| = (1 + kappa) P + Delta(P)          <=>   Delta_eff(p) = Delta(p) + kappa p
```

which is `mu(x) x = p` — verified exact to **1.7×10⁻⁹** across five decades (`C4`). The solver then
integrates the nonlinear PDE. **Nothing is assigned and differentiated afterwards** — that is precisely
what the lead objected to in L52's E3a and F1.

### The carried kernel with `ξ ≠ 0`, both footings, `κ = 0`

| footing | ξ [pc] | ε = ξ/r_M | `M_ph(<Sat)/M` | /bound | \|Q₂\|/ceil | `g_anom`/gate | admissible |
|---|---|---|---|---|---|---|---|
| canonical | 0.03 | 0.778 | 4.125×10⁻¹⁰ | 6.16 | 0.85 | 2.50 | **NO** |
| canonical | 0.05 | 1.296 | 1.673×10⁻¹⁰ | 2.50 | 0.38 | 1.02 | **NO** |
| canonical | **0.10** | 2.592 | **4.579×10⁻¹¹** | **0.683** | 0.11 | 0.28 | yes |
| canonical | 0.15 | 3.888 | 2.102×10⁻¹¹ | 0.314 | 0.05 | 0.13 | yes |
| canonical | 0.30 | 7.775 | 5.394×10⁻¹² | 0.081 | 0.01 | 0.03 | yes |
| alt | 0.03 | 0.853 | 5.051×10⁻¹⁰ | 7.54 | 0.94 | 3.04 | **NO** |
| alt | 0.05 | 1.422 | 2.047×10⁻¹⁰ | 3.06 | 0.41 | 1.23 | **NO** |
| alt | **0.10** | 2.845 | **5.604×10⁻¹¹** | **0.836** | 0.12 | 0.34 | yes |
| alt | 0.15 | 4.267 | 2.568×10⁻¹¹ | 0.383 | 0.06 | 0.16 | yes |
| alt | 0.30 | 8.534 | 6.576×10⁻¹² | 0.098 | 0.02 | 0.04 | yes |

The admissible floor is **0.10 pc on both footings**. On the canonical footing that **agrees exactly**
with the floor `g03x` obtained by a completely different screening implementation (a Helmholtz output
filter on the phantom density); on the alt footing the exact fourth-order solve is *less* restrictive
(0.10 vs 0.15 pc). **Reported, not reconciled.**

**`C5b` — the repair does not move the floor.** At the gate-compatible `κ` all four rows stay admissible
and `M_ph` changes by 5.3×10⁻⁴ relative, which `C6` shows is discretisation jitter, not physics: it
changes sign under refinement (+5.3×10⁻⁴, −7.9×10⁻⁵, −1.3×10⁻³, +4.6×10⁻³ on four grids), because the
carried kernel's `μ` has a **kink** at the saturation onset whose position moves with `κ`.

**`C6` — the mesh convergence is 2%, not better, and that is stated rather than the most favourable pair
quoted.** Across four grids (`L` 8→14, `NS` 700→1500, `NT` 48→72) `M_ph` spreads by 1.9%, and
`M_ph/bound` runs over [0.6835, 0.6964] — **below 1 on every grid**, so the PASS on the Pitjev–Pitjeva row
is not a resolution artefact. The kink is what limits the order of the scheme.

---

## 4. The flux identity — the lead's point, measured

`D1`, on the solved field, canonical, ξ = 0.10 pc:

| r/r_M | r | `g_N` [a₀] | `P` (flux) [a₀] | `P/g_N` |
|---|---|---|---|---|
| 1.19×10⁻³ | 9.48 AU | 7.053×10⁵ | 7.054×10⁵ | **1.000115** |
| 1.01×10⁻² | 80 AU | 9.869×10³ | 9.870×10³ | 1.000050 |
| 9.97×10⁻² | 793 AU | 1.007×10² | 1.000×10² | 0.99371 |
| 9.87×10⁻¹ | 7855 AU | 1.027 | 0.5394 | **0.5254** |
| 1.00×10¹ | 79851 AU | 9.934×10⁻³ | 1.397×10⁻⁴ | **0.01406** |

**The lead is right, and it is measured here rather than asserted.** `P_r` is not `g_N`; it falls to 1.4%
of the Newtonian source by 10 `r_M`. Therefore:

* **`Δ_eff = Δ + κs` survives EXACTLY** — as a constitutive relation in the **flux** `p = P_r/a₀`, which is
  literally the `μ` the solver integrates and which `C4` verified to 1.7×10⁻⁹;
* **it does NOT survive as a relation in `s = g_N/a₀`.** `V = W + P/λ` does not imply `V = W + g_N/λ`.
  The coherence operator changes the effective kernel's **argument**, not its **form**.
* **`D2`** the departure is confined to the MOND region: at Saturn's orbit the flux is Newtonian to
  1.15×10⁻⁴, which is smaller than the solve's own mesh-convergence drift of 1.9% — the comparator is a
  computed quantity, not a chosen round number.

---

## 5. The ephemeris cost — computed, and both of L54's numbers move

The `l = 0` Neumann condition at `r_min` excludes the `1/r` solution, so `M_ph = r²ψ₀′(r)` is **already
the `GM`-refitted phantom mass** — exactly the quantity the ephemerides constrain, with the `(1+κ)`
rescaling of `GM_⊙` absorbed as L52's F2 said it would be.

### `E1` — L54's baseline was too optimistic by more than two orders of magnitude

L54's D8 recorded the screened Saturn phantom mass as **3.0×10⁻³ / 1.6×10⁻³** of the bound, a margin of
333× / 625×. The exact screened fourth-order solve at the carried kernel's own floors gives

| footing | ξ [pc] | `M_ph/bound` | margin |
|---|---|---|---|
| canonical | 0.10 | **0.683** | **1.46×** |
| canonical | 0.15 | 0.314 | 3.19× |
| alt | 0.10 | **0.836** | **1.20×** |
| alt | 0.15 | 0.383 | 2.61× |

**The row still PASSES, but it passes narrowly.** This is a correction found by this lane against itself.

### `E2` — the sign of the cost is the opposite of the one L54 assumed

Measured on the solved field, with `κ` taken above the discretisation jitter and then extrapolated back:

| κ | `M_ph(<Sat)/M` | `M(κ)/M(0)` | `1/(1+κ)` | `1+κ` |
|---|---|---|---|---|
| 0.010 | 4.537483×10⁻¹¹ | 0.990841 | 0.990099 | 1.010 |
| 0.030 | 4.458299×10⁻¹¹ | 0.973550 | 0.970874 | 1.030 |
| 0.100 | 4.181635×10⁻¹¹ | 0.913135 | 0.909091 | 1.100 |
| 0.300 | 3.556422×10⁻¹¹ | 0.776609 | 0.769231 | 1.300 |

```
    M_ph(kappa) = M_ph(0)/(1 + kappa)        to better than 0.96% over 0.01 <= kappa <= 0.3
```

against 40% for the `(1+κ)` law. **The repair marginally IMPROVES the row.** L54's D8 chose the
conservative bracket, in which the screening acts as a common factor and the `κ` piece adds 2.74×; the
solve **decides against that bracket and for the one L54 itself named as the alternative** — the screened
response is set by the `ξ²` operator and `κ` drops out.

### `E3` — L54's second ceiling is withdrawn

`M(κ)/bound = 0.683/(1+κ) < 1` for **every** `κ ≥ 0`. The screened Saturn phantom-mass row places **no
upper bound on `κ` at all**; at the physical ceiling `κ = 1.6×10⁻⁶` it moves by 1.6×10⁻⁴ %, i.e. it is
`κ`-blind. **L54's `κ ≤ 3.09×10⁻⁴ / 7.00×10⁻⁴` does not survive the very solve L54 named as the thing
that would decide it.**

### `E4` — the surviving window

| bound | value | status |
|---|---|---|
| lower: cap `Σ_∥` at 10⁶ | `κ ≥ 1.0×10⁻⁶` | a choice, not a gate |
| lower: convexify the raw ν_RAR | `κ > 0.0324` | incompatible |
| upper: gravitational Cherenkov, canonical (L54 D7, **soft**) | `κ ≤ 1.644×10⁻⁶` | **binding** |
| upper: gravitational Cherenkov, alt (L54 D7, **soft**) | `κ ≤ 1.623×10⁻⁶` | **binding** |
| upper: screened Saturn phantom mass (L54 D8) | none | **WITHDRAWN** |

`Σ_∥` at Saturn: **9.617×10¹⁵ → 6.173×10⁵** (canonical), **5.759×10¹⁵ → 6.173×10⁵** (alt) at the ceiling.
The ν_RAR arm still needs `κ > 0.0324` and is still excluded by 2.0×10⁴× — a pincer with no interior,
exactly as L54 found; this lane's solve does not reopen it.

### `E5` — the one placement that does not survive, stated because it nearly changed the answer

If the coherence operator sits on a scalar that **carries the point source**,
`∇·[J_Y∇φ] − ξ²Δ²φ = 4πGρ` — the naive reading of §3, and the structure the lead's toy model encodes —
then the biharmonic Green's function of the point mass alone forces a constant interior anomaly
`GM/(2ξ²)`, kernel-independent: **1.9×10² × the sunward gate at ξ = 0.10 pc**, needing **ξ ≥ 1.38 pc** to
clear it, 14× the carried kernel's floor and fatal to the wide-binary predictions. THE_ACTION §4 and
`g03d` put the operator on `ψ = Φ − Φ_N`, which has no point source. **That placement is load-bearing and
the deposited one is the one that survives.**

---

## 6. Verdict — a result, with one edge that is still provisional

**It is a result, not a proposal, on everything the screened solve can decide.** The repair survives a
normalised nonlinear static solve with the coherence operator on, in two independent solvers each
validated against the repository's own published control numbers; the auxiliary still costs zero
propagating modes with `ξ ≠ 0` and the degeneracy locus is still empty; the effective kernel survives
exactly, in the flux; the ephemeris cost is **computed, not imported as zero**, and it is
`M_ph(κ) = M_ph(0)/(1+κ)` — so the repair costs the ephemerides nothing and marginally helps.

**Two of L54's own numbers move, both reported here against this lane**: the screened Saturn margin is
**1.5× / 1.2×, not 333× / 625×**, and the `κ ≤ 3.1×10⁻⁴` ceiling **is withdrawn**.

**It is not a closure and the upper edge of the window is still provisional.** The only surviving bound on
`κ` from above is L54's gravitational-Cherenkov ceiling ≈ 1.6×10⁻⁶, which L54 itself flags as soft with
three named omitted suppressions that all raise it; the second half of the lead's named next step — the
**metric and clock variation of the repaired action, and Dirac closure about the nonlinear static
background rather than about flat space** — is **not done here**; the kernel fork stays open; and the
mesh convergence of the Saturn row is 2%, limited by the kink the carried kernel's saturation puts into
`μ`. Carry the repair as **counted, classified, gated and now solved, with a one-decade two-sided window
`κ ∈ [10⁻⁶, 1.6×10⁻⁶]` whose upper edge is provisional** — and do not carry a zero ephemeris cost, which
is what the lead said and which remains right for the reason it gave, even though the number it protects
turns out to be favourable.
