# L44 — L35's transition ghost IS escaped, but not by the collar, and not by the multiplier

2026-09-09. Lane L44 of [CHARTER.md](CHARTER.md), answering: does the lead's IC35 collar construction
escape [L35_TRANSITION_GHOST.md](L35_TRANSITION_GHOST.md)'s theorem, and by which hypothesis?
Script: [L44_collar_vs_theorem.py](L44_collar_vs_theorem.py) → [L44_collar_vs_theorem.out](L44_collar_vs_theorem.out).
**76 checks, 76 PASS, exit 0.**

Method: the IC12 Hamiltonian, its switch, its pressure and its auxiliary root solve, and separately the
IC20/IC28/IC29/IC30 Hamiltonian, its pin term and its auxiliary branch, were re-transcribed by hand from
`IC4/IC5/IC10/IC11/IC12` and `IC18/IC20/IC28/IC29/IC30/IC35/IC36/IC37`, differentiated in sympy here, and
root-solved by a Newton iteration written here. Nothing under
`closure_2026/integrable_clock_construction_2026/` was imported, run or copied; the lead's files were
opened read-only for verbatim substring checks. Polarity: every check asserts a **statement**, and PASS
means the statement is true — so `L44-V1` passing is a **positive** result for the construction.

---

## The short answer, in three sentences

**L35's theorem is genuinely evaded, and the evasion is exact rather than numerical: in the action the
collar is built on, the entire scalar UV kinetic coefficient is `a_UV = A²/(4D + 24 E4 z²) > 0`, with no
`eta`, `eta'` or `eta''` anywhere in it, on both plateaus and through the whole transition.**
**But it is not the collar's escape and it is not the finite multiplier's** — it happened at IC20, fifteen
steps earlier, when the switch was moved out of the kinetic sector onto the holonomic pin term
`-eta e^S ell (w-wc)`, which vanishes identically on the constraint surface it enforces, while a *new*
auxiliary `z` supplied a strictly positive Schur complement `-h_qz²/(2 h_zz)` in its place.
**The price is a restart, not a contradiction**: the escape discards the IC10/IC11 pressure plateau, the
IC4 curvature-square sector and IC26's evolved history, replaces the a₀–Λ input with the programme's own
κ=½ law (exact on the canonical footing, 17% off on the alternative), and hands the obstruction to a
different gate — IC36's second preservation, which **fails**, and IC37's exponentially flat interface.

---

## 1. Controls — L35 reproduces, and so do the lead's own collar numbers

`L44-A1..A5` rebuild L35's identity from scratch in sympy for an arbitrary `C²` switch and an arbitrary
`rho`-independent pressure:

```
a_UV = E A/6 + h,rhorho/4 = -(E G r/3) eta' - (E G r²/12 + B E²/36) eta''
                          = -(1/b) d/dr[ b² eta' ],   b = E(G r² + B E/3)/12
```

all three forms agreeing symbolically, agreeing with IC12's own stated identity, and collapsing to
**exactly zero for any locally constant `eta`** — L35's marginality, re-derived independently.

`L44-B3..B11` re-solve IC12's continuation (`h12,xi = h12,u = 0` at `rho = rho0 + n/1000`, own Newton,
60 digits, own analytic switch derivatives cross-checked against numerical differentiation to 1e-56):

| n | eta (mine) | eta (IC12) | a_UV (mine) | a_UV (IC12) |
|---|---|---|---|---|
| 0 | 1 | 1 | 1.94e-62 | 0 |
| 200 | 0.998768085275871 | 0.998768085276 | +0.05756806825315 | +0.0575680682531 |
| 205 | 0.998141100037156 | 0.998141100037 | +0.01917907027389 | +0.0191790702739 |
| 210 | 0.997729876649563 | 0.99772987665 | −0.04479545146231 | −0.0447954514623 |
| 220 | 0.99726400317076 | 0.997264003171 | −0.2029719578236 | −0.202971957824 |
| 500 | 0.995746896086384 | 0.995746896086 | **−7.0406396415086** | −7.04063964151 |

Ghost onset at **n = 207**; the geometric switch boundary `r² = 5/4` crossed at **n = 63**; the
b-weighted integral across a complete transition **8.1e-69**; and the pressure-blind corollary
(`d a_UV/dB = 0` wherever `eta'' = 0`) verified symbolically. All of L35's anchors.

`L44-C1..C11` reproduce, from the lead's own markdown, every collar quantity it states to enough digits
to check: `det(M) = 16 v² u² e^{−4Q}` and `det(M1) = gamma det(M)`; `M_T² = 2e^{S−2wc}/t = m`;
`h_zz = −2D − 12 E4 z²`; `H_RR = h_zR = 0`; `D0 = 0.13` at IC29's design point; `q(2) = −3 m h0 e^{3wc}/√2`
putting `alpha²` **exactly** on the `eta = 0` edge `1/2`; the width-.006 collar's stated `q` range mapping
to `alpha² = [0.245518804065901, 0.860335765661288]` against the lead's
`[.24551880406590093, .8603357656612876]`; and IC37's `1/eta = 1 + exp(1/x − 1/(1/4−x))`.

---

## 2. Which hypothesis the collar violates — (c) hard, then (b); **not** (a), and **not** the multiplier

### (a) is NOT the answer. The collar is smoother than L35 requires.

IC35's prescribed profile `f(x) = 35x⁴ − 84x⁵ + 70x⁶ − 20x⁷` matches the plateaus in `f, f', f'', f'''`
at **both** ends (`L44-D1`) — it is `C³`, one derivative more than the theorem asks. The switch `eta`
itself is the IC18/IC5 mollifier, `C^∞`, with `eta(1e-3) = 2.8e-433` (`L44-D2`, `L44-C10`). So `b² eta'`
still vanishes at both ends, and L35's boundary term is still zero. This door is shut.

### (c) IS the answer, in the strongest possible form: the switch has left the kinetic sector.

In IC12 the switch multiplied a metric-momentum-dependent term: `h12 = hbase + eta(r)[delta h10 − B]`,
`delta h10 = −E rho² G/3`. In IC20 and everything after it, `eta` appears in the action **exactly once**,
on the holonomic pin term (`L44-D15`, documentary, one occurrence in `IC20_JOINT_COMPLETION.md`):

```
F20 = exp(2S)/v [...] − A q z − exp(S) P0 − D z² − E4 z⁴ − v R − ...  − eta exp(S) L (w − wc)
```

Every `eta`-derivative in the momentum Hessian therefore carries the factor `(w − wc)`. And `w = wc` holds
**wherever `eta > 0`** — it is what the `ell` equation `E_ell/J = eta e^S (w − wc) = 0` enforces — while on
`eta = 0` the whole term vanishes on an open set together with all its jets. So on the entire domain
(`L44-D4/D5/D13b`):

```
h_qq = −t/3,      h_qz = −A,      h_zz = −2D − 12 E4 z²      (no eta, eta' or eta'' anywhere)
```

Consequently **L35's `G` is identically zero** and its weight `b = E(G r² + B E/3)/12` is identically zero
on the constraint surface (`L44-D7`, `L44-D8`). L35's hypothesis **H8 fails**, and with it H1, H3 and H4:
the total-derivative structure cannot form, so the proof cannot run. The switch's argument also moved,
from the metric momentum `p` to `alpha = −e^{−3w} q/(3 m h0)` — but that alone would not have saved
anything; **leaving the kinetic sector is what did.**

### (b) is ALSO violated — but by the auxiliary, not by the "finite multiplier".

L35's own named door is "a redesign that breaks the cancellation making the plateaus marginal, leaving a
positive coefficient on the plateaus rather than zero." That is exactly what happened, and the mechanism
is worth stating precisely, because it is *not* what the phrase "finite multiplier" suggests:

* **L35's cancellation SURVIVES verbatim.** `t/6 + h_qq/2 = 0` exactly (`L44-D9`) — the bare trace-free /
  trace pair is still marginal. The lead did not break L35's mechanism; it left it intact.
* **What is new is a second auxiliary field `z` with an `A q z` mixing.** Eliminating it adds a Schur
  complement that survives on the plateaus (`L44-D10`, `L44-D11`):

```
a_UV = t/6 + H_qq/2 = t/6 + (h_qq − h_qz²/h_zz)/2 = −h_qz²/(2 h_zz) = A²/(4D + 24 E4 z²)
```

* **The multiplier `ell` contributes exactly nothing**: `d a_UV/d ell = 0` identically (`L44-D12`),
  because `ell` multiplies `(w − wc)`, which is zero. IC35/36/37's "finite multiplier" work is about a
  *different* obstruction (regularity of `ell`, `elldot`, `ellddot` at the interface) and buys no part of
  the ghost escape.

### (d) — the ghost is not relocated *within this coefficient*. It is elsewhere. See §5.

---

## 3. Computed, not argued: the coefficient across the collar

**An exact, D-free positivity theorem.** The auxiliary branch is IC30's `E_z/J = A q + 2 D z + 4 E4 z³ = 0`
(`L44-E1`). Substituting `2D = −A q/z − 4 E4 z²` gives (`L44-E2`, `L44-E3`)

```
F_z = 2D + 12 E4 z² = −A q/z + 8 E4 z²,       a_UV = A² z / [ 2(−A q + 8 E4 z³) ]
```

which is **strictly positive whenever `A > 0`, `q < 0`, `z > 0`, `E4 ≥ 0` — with no knowledge of `D(S)` at
all.** The C²-only 81-node `D(S)` table, which the lead correctly flags as its weakest numerical object,
therefore cannot change the sign. And `z > 0` is not selected but **forced**: `2Dz + 4E4z³` is odd and
strictly increasing, so the cubic has a unique real root and it is positive for `q < 0` (`L44-E4`).

Evaluated across the lead's own reported width-.006 collar range `q ∈ [−1.2907827763779491,
−0.689543315752672]`, which spans `alpha²` from 0.2455 (inside `eta = 0`) to 0.8603 (inside `eta = 1`):

| D(S) | z at q = −1.29078 | a_UV | z at q = −0.68954 | a_UV |
|---|---|---|---|---|
| 0.05 | 0.94895897 | 0.02403120874 | 0.60219263 | 0.03483924433 |
| **0.13** (IC29's D₀) | 0.47949446 | **0.01738587435** | 0.26242849 | **0.0186383392** |
| 0.20 | 0.31943618 | 0.0121287176 | 0.17187807 | 0.01239019044 |
| 0.50 | 0.12899243 | 0.004990036467 | 0.068941225 | 0.00499714989 |

`a_UV ∈ [0.00499, 0.03484]` over the whole band (`L44-E5`); at fixed `D = 0.13` and 199 points across the
complete transition, `a_UV ∈ [0.01759, 0.01808]` (`L44-E11`). Positive everywhere, and nearly flat.

**Is the integral identity genuinely evaded, or numerically missed?** `L44-E6..E10b` settle this with an
explicit hybrid negative control: reinstate a switched kinetic coefficient `G ≠ 0` while keeping the
`A q z` mixing. The result is exactly

```
a_UV = −(t G/12)(4 alpha eta' + alpha² eta'')  +  A²/(2 F_z)
       \___________ L35's total derivative ___/   \__ the escape __/
```

Integrating against `b = t G alpha²/12` across the collar: the total-derivative piece gives
**2.13e-65** — L35's identity holds to machine precision — while the Schur piece gives
**1.362e-4**, so the full weighted integral is **1.362e-4 ≠ 0** (`L44-E7`, `L44-E8`). The evasion is a
structural term, not a numerical near-miss.

**And the control has teeth.** With the Schur term removed, the *same* collar has
`a_UV ∈ [−192.49, +184.89]` — L35's theorem fires exactly as proved (`L44-E9`).

**One sharp caveat that came out of the control, and it is a real finding.** The Schur term does **not**
rescue a merely *small* switch weight in the kinetic sector: at `G = 0.4` the hybrid collar still reaches
`a_UV = −192.5`, and the Schur term only covers `|G| < 3.66e-5` (`L44-E10`). The escape works because
`G` is a **structural zero**, not because the new positive term is large. Any future revision that
reintroduces even a 1e-4 switch dependence into the momentum Hessian re-opens the ghost.

---

## 4. Pricing the escape

**It does not cost the clock cone.** IC28's `c_g² = 2 a v0 u²/[e^{2S}(1−u²)]` at the design point
(`a = 1/76 = 0.0131579`, `u = 2/3`) is **0.00906** — positive and subluminal, with the ceiling at
`a = 1.4523`, a **110×** margin (`L44-F1`, `L44-F2`). Escape and subluminality are coupled through the
same `a`, and both hold with two orders of magnitude to spare.

**It does not break the mode count as stated.** IC20's `(26 − 12 − 8)/2 = 3` arithmetic is right
(`L44-F6`) — 2 tensors + 1 clock — though a functional Dirac certificate is still absent and the lead says so.

**The a₀–Λ input changed, and in the framework's favour on one footing only.** L35 priced IC5's tuned
proportionality at 10–13× off; that reproduces here (`L44-F3`, model `2.1351442` vs observed
`0.1727` / `0.2081`). IC20 replaced it with the **imposed** `a0² = Λ/(32π)`, i.e. `a0 = (c/2)√(Gρ_Λ)` —
the programme's own κ=½ law:

| footing | a₀ (m/s²) | observed a₀/(c H_Λ) | IC20 model 0.1727470747 | IC5 model 2.135144 |
|---|---|---|---|---|
| canonical | 9.3619e-11 | 0.17273956 | **1.00004×** | 12.3605× |
| alternative | 1.1279e-10 | 0.20811262 | **0.830065×** | 10.2596× |

So the 10–13× mismatch is gone — but it is **imposed, not derived** (the lead says "the vacuum-scale
coefficient 1/2 is still imposed"), and it is **17% off on the alternative footing** (`L44-F4`, `L44-F5`).
It must be reported as a fit to one footing, never as a prediction.

**What the escape actually cost, in the lead's own words** (documentary, `L44-F7..F11`):

* the IC10/IC11 **pole-clock pressure is gone** — "NO pole-clock pressure and inherits NO IC18/IC19 early
  history". L20's backward `Q_clock = 0` edge at `S = 0.0267` belonged to that pressure and no longer
  applies to this action; equally, its plateau certification (`PX`, `Q_clock`, `cs²`, the 8-e-fold history)
  no longer applies either;
* the **IC4 curvature-square sector is gone** — "No old curvature square, switched pressure, or extra
  gradient term is implicit". L26's σ question dies with `F`, `J`, `A_R`, `B_R`;
* IC28 explicitly **does not inherit IC26's seven-e-fold history**, so the evolved-interval certification
  restarts;
* `v = v0` makes **`H_RR = 0`**: the no-slip `Φ = Ψ` result follows from `H_qR = H_RR = 0`, i.e. from a
  *degenerate* curvature Legendre chart, which the lead states plainly;
* `D(S)` is an **integrated** coefficient held only as a C² 81-node table with no global extension. The
  ghost result is immune to this (§3, D-free), but higher jets at its joins are not — and IC36/IC37 need
  exactly those higher jets.

**Nothing here reintroduces what L20, L26 or L33 closed.** L20's and L26's objects were removed with the
sectors that carried them; L33 concerns a different construction entirely.

---

## 5. Where the obstruction lives now — and the shortest statement the lead can act on

The scalar UV ghost is out of the transition. The bottleneck moved to the **multiplier at the moving
activation interface**, and the lead has already driven it to a sharp point:

* **IC36 FAILED its own gate** (`L44-G1`, from the lead's own frozen run record): the IC35
  first-preservation-selected baseline does **not** admit a second time jet with `ell = elldot = ellddot = 0`.
  Baseline peak residual ≈ **56.1475**, RMS **39.3344**; the best repaired initial datum
  (`U1 = Sdot'(2) = −2.6400382455715268`) still leaves RMS **0.10636** and peak **0.17485**, stable across
  polynomial degrees 8/12/16 and three time-step sizes, and not explained by a coefficient-cell join.
* **IC37's obligation is exact and severe** (`L44-G2`, `L44-G3`): a bounded `ellddot` requires
  `W_tt = O(eta)` at the interface, and `eta` is exponentially flat —
  `eta(1e-4)/x⁸ = 6.2e-4310`. So a nonzero finite Taylor jet of `W_tt` at the interface forbids a bounded
  multiplier, and matching `E = E_r = 0` merely moves the obstruction to `E_rr`, then `E_rrr`: an
  **infinite tower of vanishing conditions**, not one more equation. The lead states the correct caveat
  itself — flatness alone is not sufficient outside the analytic sector, `E = exp(−1/2x)` being power-flat
  yet `E/eta → ∞` (`L44-G4`).

**The one-line handout.** The transition ghost is closed; do not spend another turn on it, and do not
reintroduce any `eta` dependence into the momentum Hessian — the tolerance is `|G| < 3.7e-5` and the
construction currently sits at exactly `0`. The live question is whether `W_tt` can be made to vanish to
**all** orders at the interface, which is an analyticity question about the coefficient functions, not a
tuning question about initial data; a C² `D(S)` table cannot answer it either way. Two structural exits
exist and neither has been tested: give the switch a **compactly supported polynomial** transition (finite
order of contact, so `O(eta)` is a *finite* tower), or drop the holonomic pin for a term whose `w` equation
is `O(eta)` by construction rather than by selection.

---

## 6. Verdict

**The escape is genuine, exhibited rather than asserted, and it is the best structural news the programme
has had on the theory side.** `a_UV = A²/(4D + 24 E4 z²) > 0` holds on both plateaus and through the whole
transition with no switch dependence at all; L35's weighted-integral identity is evaded because its weight
`b` is identically zero, and the negative control confirms the machinery still fires when the switch is put
back into the kinetic sector. **But the credit belongs to IC20, not to IC35's collar, and not to the
"finite multiplier"** — `ell` multiplies `(w − wc) = 0` and contributes exactly nothing to the coefficient;
what broke the marginality is the auxiliary `z` and its `A q z` mixing, while L35's own cancellation
`t/6 + h_qq/2 = 0` survives untouched underneath it. **The escape was bought with a restart** — the
IC10/IC11 pressure plateau, the IC4 curvature-square sector and IC26's evolved history are all discarded,
the a₀–Λ relation is now the imposed κ=½ law (exact on the canonical footing, 0.83× on the alternative),
and the obstruction now sits at IC36's failed second preservation and IC37's exponentially flat interface,
where it is an analyticity problem rather than a tuning problem.
