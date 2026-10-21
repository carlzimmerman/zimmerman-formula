# A25 — the kernel conflict: the action's kernel is the theory's, and the 5.6× is not a tension

**Lane:** A25_kernel_conflict · **Date:** 2026-10-21 · **Base:** `deepseek_push/DS_FINAL_2026_10_21/BRIEF.md`
**Script:** `a25_checks.py` (14/14 PASS, exit 0, 12 s) · **Output:** `a25.out` · **Data:** `a25_results.json` · **Mutation:** `MUTATE.md`

---

## Claim

The conflict has one answer and it is not the record's. The framework's kernel is the **Langmuir/simple**
`ν_L(y) = (1+√(1+4/y))/2`, because it is the only one of the four in play that (i) **is derived** — from the two-state
lattice (A2) and from the action's own potential `W_full` (A12 §5, residual 0), (ii) **closes the vacuum integral**
`I = ∫y(ν−1)dy` to Λ with a turn-off `y_t` inside the planetary caps, and (iii) **is not disfavoured by SPARC**:
`Δχ²(ν_RAR − ν_L) = +10.1` on the canonical footing and `−0.8` on the alt, i.e. the two are indistinguishable, while
the quadrature is worse by `Δχ² = 75–158`. The record's `12.99` is **exactly `2π⁴/15`** — the RAR kernel's *convergent*
vacuum integral — and `73.19/12.9878788 = 5.635` is its "5.6×". That number is a statement about the one kernel the
theory does not use, and the RAR kernel is the only one of the four that **cannot close Λ at all**: its integral is
bounded by `12.988` and the record's turn-off only lowers it. The quadrature kernel that the record says is *required*
is excluded by SPARC at `Δχ² = 76–158` and closes only at `y_t = 94.05` (target 73.19) or `128.92` (target 32π) — which
is exactly how the record's `94–129` band is generated, so that band is a property of the quadrature kernel at two `a0`
normalisations, not of the theory. The action's kernel closes at `y_t = 48.79` or `66.38`.

**Status: CLOSED-DERIVED** (kernel determination, three independent constraints) **+ NUMERICAL** (closure roots)
**+ DECIDABLE** (falsifier: `Δχ²(Q−L)` on SPARC, pre-registered below).

---

## Derivation

### 1. The integral, and the one function that decides it

With `y ≡ g_N/a0`, `ν(y) ≡ g/g_N` (so `g = a0 y ν`), the record's normalization (Zenodo 23251231) is

  (1)  `I ≡ ½∫₀^∞ (ν−1) d(y²) = ∫₀^∞ y(ν−1) dy ≡ ∫₀^∞ h(y) dy`,  `h(y) ≡ y(ν−1)`,

because `d(y²) = 2y dy`. Everything follows from `h`:

  (2)  `ν−1 = h/y`, so `ν → 1 + c/y` ⟺ `h → c`; the *tail coefficient* `c ≡ lim_{y→∞} h(y)` fixes the divergence,
  (3)  `ν → y^{−1/2} + β` ⟺ `h → √y + βy`; the *deep coefficient* `β ≡ lim_{y→0}(ν − y^{−1/2})` fixes the deep law.

### 2. The four kernels and where each lives in the repo

| id | `ν(y)` | `c` | `β` | source of the exact form (file) | status of that form |
|---|---|---|---|---|---|
| **L** | `(1+√(1+4/y))/2` | **1** | **1/2** | action: A12 §5 `W_full = (a₀²/K)[−u/a₀−ln(1−u/a₀)]` ⇒ `g²=g_N(g+a₀)`; lattice: A2 §1–2 | **derived** (A2 exact identity, A12 K10 residual 0) |
| **Q** | `√(1+1/y)` | **1/2** | **0** | `real_research/derivation_chain_2026/FP1_static_sector.py:112` (`nu_p2`), B2/B3; Zenodo 23171085 ("Milgrom 1999 eq 9") | **chosen**: FP1's action has "one free function" `q`, and `q_P2` is its closed-form *embedding* (K1d) |
| **R** | `1/(1−e^{−√y})` | **0** | **1/2** | `opus_48_extended_research/papers/THE_COMPLETION.md:182` (`μ(u)=1−e^{−u}, x=u²/μ, u=√y`); `hunt_2026/hunt_lib.py:nu()`; identity certified `hunt_2026/f23_kernel_transcription_audit.py` K1a | **chosen**: AQUAL `F(X)` in polylogs is reverse-engineered from `ν` (f23 §5b) |
| **M** | `1 + h_M/y` (splice) | `∞` (ln y) | **1/2** | `FP1_static_sector.py:132–143`, constants `real_research/g03_audit_2026/L340_filtered_khronon_completion_results.json` A1; audit `real_research/extra_crispy_2026/XC4_nu_mono_splice.py` | **hand-built**: `h' = max(h_RAR', 0.05 h_p/(y+y_p))`, two extra numbers (0.05, y_p) |

The symbol `nu_mono` is **overloaded four ways** in the repo, and this is part of why "no file states the kernel":
`hunt_lib.nu()` and `ChainCert/Kernel.lean:7` both define it *as* `ν_RAR`; `CFG665_gw_messenger.lean:13` defines it as
the *simple* kernel `1/2+√(1/4+1/y)` (flagged as a mislabelling by `CFG670:7`); `FP1`/L340/XC4 define it as the splice.
K1 validates the splice against L340's stored numbers (`max|Δlog₁₀(ν_M/ν_R)| = 0.01037015` at `y = 14.3503`; L340 stores
`0.0103700578` at `14.35`), so the fourth row above is the operative reading.

### 3. The bare integral (no turn-off): exact, and who diverges

  (4)  `I_L(Y) = [(Y+2)√(Y²+4Y) − Y²]/4 − ln[(Y+2+√(Y²+4Y))/2] = Y − ln Y + ½ + O(lnY/Y)`
  (5)  `I_Q(Y) = [(2Y+1)√(Y²+Y) − 2Y²]/4 − ¼ln[√(Y+1)+√Y] = Y/2 − (lnY)/8 − 0.1107868 + O(lnY/Y)`
  (6)  `I_R(∞) = ∫₀^∞ y dy/(e^{√y}−1) = 2∫₀^∞ u³du/(e^u−1) = 2Γ(4)ζ(4) = 2π⁴/15 = 12.9878788045`  (**converges**)
  (7)  `I_M(Y) = δh_p·Y ln Y + O(Y)`,  `δh_p = 0.05 h_p = 0.03238051`, `h_p = 0.6476102` at `y_p = 2.5396383`

Measured: closed forms (4)–(5) agree with adaptive quadrature to `3.2×10⁻²⁶`; `dI/dY = 0.999999953` (L) and
`0.499999994` (Q); the constants are `+0.499999980` and `−0.110786796`. Divergence exponents are **1** for L and Q
(not `3/2`, correcting the tasking that A4 already corrected), and **1 + log** for M. R converges.

### 4. The turn-off integral: exact forms and asymptotics

With the record's turn-off `h → h/(1+(y/y_t)²)` (23171085) and the substitution `v = √(y²+ky) − y`:

  (8)  `F_L(Y) = Y²∫₀² v²(4−v) dv / [4Y²(2−v)² + v⁴]`   `= (π/2)Y − ln Y + ½ + O(lnY/Y)`
  (9)  `F_Q(Y) = 2Y²∫₀^{1/2} v²(1−v) dv / [Y²(1−2v)² + v⁴]`   `= (π/4)Y − (lnY)/8 − 0.1107868 + O(lnY/Y)`
  (10) `F_R(Y) = 2∫₀^∞ u³du / [(e^u−1)(1+u⁴/Y²)]`   `= 2π⁴/15 − 10121.1/Y² + …` (asymptotic; exact `12.285829`
       at `Y = 100`, `12.977835` at `Y = 1000`)
  (11) `F_M(Y) = ∫₀^∞ h_M dy/(1+(y/Y)²)`   `= (π/2)δh_p·Y ln Y + O(Y)`   (no elementary closed form; exact quadrature)

Certified: (8)–(9) against direct quadrature to `1.2×10⁻³⁰` at `Y = 20, 50, 100`; (8) to `1.9×10⁻⁴` and (9) to
`1.2×10⁻⁵` at `Y = 100`; (10) to `1.0×10⁻⁸` at `Y = 10⁶`. **The `(π/2)` and `(π/4)` are the Lorentzian's, and the
kernel enters only through `c`**: `F ≈ (π/2)c·y_t`. The record's own formula "`Λ/a₀² ~ (π/4) y_t`" is the `c = 1/2`
case of this line.

### 5. The `y_t` that makes each kernel equal 73.19

| kernel | `c` | `y_t` at **73.19** | `y_t` at **32π = 100.530965** | `y_t` at **100.405845** (A4) | `F(y_t)/73.19` at the record's 94.05 |
|---|---|---|---|---|---|
| **L** (action) | 1 | **48.7877** | **66.3803** | 66.2999 | 1.9629 (over-predicts Λ by 1.96×) |
| **Q** (quadrature) | 1/2 | **94.0539** | **128.9154** | 128.7559 | 1.0000 |
| **R** (RAR) | 0 | **none** (sup `12.9878788`) | none | none | 0.1669 |
| **M** (nu_mono) | ∞ | **63.6856** | 86.3375 | 86.2345 | 1.5018 |

K5 certifies the roots to `<5×10⁻²`; K6 certifies the record's **94** as `Q` at 73.19 (0.06%) and its **128.9** as `Q`
at 32π (0.01%) — the band is the quadrature at two `a₀`, and the action's kernel sits `94.0539/48.7877 = 1.928` below
it. R has **no root**: `F_R` is bounded by `2π⁴/15`, so `F_R(y_t) < 73.19` for every `y_t`, and the turn-off can only
reduce the integral.

### 6. Which diverge, how, and whether the turn-off or the kernel does the work

| kernel | bare `I` | with turn-off | who does the work | closure exists? |
|---|---|---|---|---|
| **L** | `~ Y` (coefficient 1) | `~(π/2)y_t` (linear) | **both**: kernel sets `c = 1`, Lorentzian sets `π/2`; the turn-off supplies the finiteness | yes, one root |
| **Q** | `~ Y/2` | `~(π/4)y_t` | same with `c = 1/2` | yes, one root |
| **R** | finite `2π⁴/15` | only shaved (`12.2858` at `y_t = 100`), never raised | **the kernel** (the `e^{−√y}` decay makes it finite); the turn-off cannot create a root | **no** |
| **M** | `~ δh_p Y ln Y` | `~(π/2)δh_p y_t ln y_t` | the kernel supplies the log; the turn-off cannot beat it | yes, one root |

The consequence is structural: for every kernel with `c > 0` (or log growth), `F(y_t)` is continuous and strictly
increasing from 0 to ∞, so **one equation `F(y_t) = Λc⁴/a₀²` has exactly one solution for any target**. The Λ identity
therefore **cannot select the kernel** — it selects `y_t`. The only kernel it can exclude is the one whose `F` is
bounded, and that is the RAR kernel.

### 7. The decision, and why it is forced

The first thing to say is that the repo does state the kernel — in the *law*, not in the word "kernel": the BRIEF
§1 canonical law `g_N = g²/(g+a₀)` is *identically* `ν_L` (K1a–b, sympy residual 0), and PAPER57/AG4 is its source. So
the conflict is not an absence of statement; it is a contradiction between the canonical law and the record's kernel.
What was genuinely missing is the identification `law ↔ kernel`, which K1a–b supplies exactly. With that, choosing is a
three-constraint problem, and the constraints are independent:

| constraint | **L** | **Q** | **R** | **M** |
|---|---|---|---|---|
| derived from the medium/action | **yes** (A2 exact; A12 K10) | no — `q_P2` is an embedding of a chosen `q` (K1d); A2: outside the closure of two-state gates | no — `F(X)` reverse-engineered (f23 §5b) | no — hand-splice, 2 extra numbers |
| closes Λ with `y_t` inside the planetary caps (`y_t ≤ 605.96`) | **yes**: 48.79 (margin 12.4×) | yes: 94.05 (6.4×) | **no** (no root) | yes: 63.69 (9.5×) |
| SPARC does not disfavour it | **yes**: `Δχ²(R−L) = +10.1 / −0.8` (tied) | **no**: `Δχ²(Q−L) = +158 / +75` | reference | marginal: `Δχ²(M−L) = +9.2 / −0.2` |

Only L satisfies all three, and it does so with no new number. That is the sense in which the choice is forced — not
"L is the only one with an action" (any monotone `ν` can be embedded by `q'(s²) = ν(s)−1`; K1d shows P2 is), but
"**L is the only one whose potential is derived rather than chosen**", and the two constraints that do not depend on
provenance (Λ, SPARC) each remove one of the others. `nu_mono` is the closest rival: it passes Λ and is only mildly
disfavoured by SPARC (`+9.2` canonical, `−0.2` alt), failing on provenance (a two-parameter splice) and carrying the
worst bare integral of the four (`δh_p Y ln Y`).

This is where the strongest counter-argument lives, and it must be stated: `FP1_static_sector.py` derives the static
sector of the C–H/K core action with **one free function** `q` and states "the kernel in use is P2". That is a genuine
action-level route to the quadrature — but it is a *choice* of `q` (the file says so: "the one free function of the
MOND sector"), and A2's lattice obstruction says no two-state medium can produce it (`ν_Q` is even in `g`, with
branch points at `g = ±i a₀/2`). So FP1 does not derive the quadrature; it shows the quadrature is *admissible*. The
data then decide, and the data reject it (`Δχ² = 17–158`).

**If instead the RAR kernel is to be derived from the action**, the route is: pick `q'(Z) = ν_R(√Z) − 1` with the
polylog primitive of f23 §5b (`F(X) = 2u⁴/μ − u⁴ − 4I₃(u)`, `I₃ = ∫₀^u t³dt/(e^t−1)`, `u = X^{1/4}`). It stays inside
A12's class (≤2 derivatives, no curvature coupling, `W = W(|∇φ|²)`), so the slip theorem survives. What changes is
fatal to the Λ claim: the vacuum integral becomes `2π⁴/15`, **no `y_t` closes 73.19**, and the observed Λ would require
`a₀ = c²√(Λ/12.9878788) = 2.60×10⁻¹⁰ m/s²` — 2.78× the canonical `a₀` and 2.39× the value the SPARC knee prefers
(`1.0885×10⁻¹⁰`, K10), which is where that route dies. So: **RAR or Λ-as-vacuum-energy, not both.**

### 8. The consequence: three numbers the record mis-reads

1. **`12.99` is `2π⁴/15`.** K3/K7: `12.9878788045` vs the record's `12.99` (0.016%), and `73.19/12.9878788 = 5.635254`
   vs "5.6" (0.63%, i.e. two-figure rounding). The number is exact, and it is a *convergent* integral — which is why
   the record could not raise it with a turn-off.
2. **The `5.6×` is not a tension; it is a proof.** It says the RAR kernel's vacuum energy is too *small*. Since the
   turn-off only decreases `F`, no cure exists: the RAR kernel and `Λ =` field vacuum energy are mutually exclusive.
   That is consistent with — indeed it independently confirms — the action's kernel being something else.
3. **`94–129` is the quadrature at two `a0` values.** `Q(73.19) = 94.0539`, `Q(32π) = 128.9154`, `Q(100.405845) =
   128.7559` (A4's stored value exactly). And `73.19` itself is not an independent measurement: with `Z = 2√(8π/3)`
   and `3Z² = 32π` exactly, `Λc⁴/a₀² = 32πΩ_Λ`, so `73.19/32π = 0.728034` is the `Ω_Λ` implied by using the H0-tied
   `a₀ = cH₀/Z`; the BRIEF's `(Λ, H₀ = 67.4)` gives `Ω_Λ = 0.683800` and `32πΩ_Λ = 68.7431` (A4's alt-footing
   `68.8896`), and the framework's own `a₀ = c²√(Λ/32π)` gives exactly `32π = 100.530965`. **On the framework's own
   identity the target is 32π, and the canonical kernel then fixes `y_t = 66.38` — no additional fitted number.**

---

## The falsifier

The vacuum integral is not observable, so the falsifier must be a kernel-shape number. I measured all four candidates
the task names, on data on disk:

- **The turn-off scale `y_t` is not a falsifier.** Its maximum signature on the RAR is `1/(2y_t)`:
  `0.00428 dex` (L at `y_t = 48.79`, at `y = 50.6`), `0.00115 dex` (Q at 94.05), `0.00247 dex` (M at 63.69) — all
  below a tenth of the RAR's `0.06 dex` scatter, and imposing the Λ-required turn-off changes the SPARC `χ²` by
  `+0.060` (L), `+0.075` (Q), `+0.112` (M). It is testable only in the Solar System, where the same turn-off must
  suppress the constant anomaly for `y_t ≤ 6.1×10⁵` (Earth's cap) — which every candidate satisfies.
- **The deep-limit coefficient `β` is measurable in principle and degenerate in practice.** `β = (1/2, 0, 1/2, 1/2)`
  for L/Q/R/M separates the quadrature absolutely (at `y = 0.01` the difference is 4.6% of `g`, at `y = 0.5` it is
  15.5%). On the KiDS-1000 lensing RAR on disk (`y = 1.5×10⁻⁵…4.2×10⁻²`, 15 bins + covariance), with one amplitude
  profiled, `Δχ²(Q−L) = −10.90` — the amplitude absorbs the deep normalization and the covariance has a near-singular
  common mode (smallest/largest eigenvalue `5.1×10⁻⁴`). **A null; reported as one.**
- **The kernel shape in the transition is the falsifier, and it already has a value.** On SPARC (147 galaxies, 3140
  points, 18 bins, galaxy-bootstrap errors, fixed `Υ`): `χ² = 28.7 (L), 186.7 (Q), 38.8 (R), 38.0 (M)` on the canonical
  footing and `19.5 / 94.8 / 18.7 / 19.3` on the alt. So

  > **`Δχ²(Q − L) = +157.96` (canonical) and `+75.25` (alt) with no free parameters; `+17.05` with `(A, a₀)` both
  > profiled; `Δχ²(R − L) = +10.07 / −0.77` (indistinguishable).**

  The kernels differ by at most `0.06247 dex` (L vs Q, at `y = 0.500` — the RAR knee, where `ν_L = 2.000` and
  `ν_Q = 1.732`) and `0.01988 dex` (L vs R, at `y = 6.96`). That is why one galaxy cannot tell them apart and 3140
  points can: the quadrature's worst transition bin is a `7.39σ` pull (canonical) / `5.05σ` (alt) against `3.19σ` /
  `2.12σ` for the action's kernel.

**Pre-registered:** with `(Υ, a₀)` profiled on the SPARC binned RAR, a future fit that returns `Δχ²(Q−L) < −25`
(quadrature preferred) refutes this lane's kernel determination; `Δχ²(Q−L) > +25` confirms it. Measured now: `+17.05`
(nominal `4.1σ`, **not calibrated** — the bin errors are galaxy-bootstrap scatter and `χ²/dof = 0.76` for the best
kernel).

---

## Status

**CLOSED-DERIVED** for the kernel: the action's `W_full` fixes `ν` uniquely (K1a–b, exact), A2's lattice supplies the
microscopic derivation, and the three constraints of §7 leave only L. **NUMERICAL** for the closure roots
(`48.7877 / 94.0539 / 63.6856 / none`, K5). **DECIDABLE** for the falsifier (`Δχ²(Q−L) = 17–158`, K9–K10).
The record's `12.99` and `5.6×` are reproduced exactly (`2π⁴/15`, `5.635`, K7) and are properties of a kernel the
theory does not use.

## Checks (`a25_checks.py`, 14/14 PASS, exit 0, 12 s)

| id | what it proves | measured |
|---|---|---|
| K1 | four exact kernel identities (action⇒L, `μ=x/(1+x)`, RAR parametric pair, `q_P2`⇒Q) | max symbolic residual `0.00e+00` |
| K2 | tail `c = (1, 1/2, 0, ln y)` and deep `β = (1/2, 0, 1/2, 1/2)` | `0.999999994 / 0.499999997 / 3.7e−40 / 0.03238`; `0.500013 / 5e−05 / 0.500008` |
| K3 | bare integral: closed forms, `2π⁴/15`, divergence exponent 1 | rel `3.2e−26`; `dI/dY = 0.999999953 / 0.499999994`; `I_R = 12.9878788045` |
| K4 | turn-off integral: exact rational forms + asymptotics | rel `6.9e−13`; `1.9e−04` (L), `1.2e−05` (Q) at `y_t = 100` |
| K5 | `y_t(73.19)` for all four; R has no root | `L 48.7877, Q 94.0539, M 63.6856, R none (sup 12.987879)` |
| K6 | the 94–129 band is Q at two normalisations; L over-predicts by 1.96× | `94.0539 vs 94 (0.06%)`, `128.9154 vs 128.9 (0.01%)` |
| K7 | `12.99 = 2π⁴/15`; `5.6× = 73.19/(2π⁴/15)` | `0.016%`, `5.6353` |
| K8 | `32π = 3Z²`; `73.19/32π = Ω_Λ`; BRIEF `Ω_Λ = 0.6838` | identity `0`; `0.728034`; `68.7431` vs `68.8896` |
| K9 | SPARC fixed footing: Q excluded, R tied with L | `Δχ²(Q−L) = +158.0 / +75.3`; `Δχ²(R−L) = +10.1 / −0.8` |
| K10 | SPARC `(A, a₀)` profiled: the fair shape test | `Δχ²(Q−L) = +17.05`; `a₀(Q) = 1.2004e−10` vs `1.0885e−10` |
| K11 | the Λ-required turn-off is RAR-invisible | `0.00428 dex` (L), `0.00115` (Q); SPARC `Δχ² ≤ 0.11` |
| K12 | strong-field coefficient vs the Earth bound; planetary cap | `2557.4×` (L), `1278.7×` (Q), `0` (R); margin `12.4×` |
| K13 | KiDS lensing RAR: a null for kernel separation | `Δχ²(Q−L) = −10.90` |
| K14 | the canonical kernel is the action's (mutation hook) | `L` |

`--mutate` sets the canonical kernel to the quadrature and breaks **K5, K9, K10, K14** (10/14, exit 1) — see `MUTATE.md`.

## What this does not do

- **It does not fit.** The SPARC comparison is a fixed-`Υ`, diagonal-bin, galaxy-bootstrap diagnostic (the convention
  of `f21`/`f23`), not a calibrated model rejection. K10 profiles `(A, a₀)` and is the fairer number; a full fit with
  `Υ`, distance and inclination would move both `χ²` and the `Δχ²` and is not attempted here.
- **It does not derive the turn-off.** `y_t` remains a posit; this lane only shows which kernel each `y_t` belongs to
  and that the three viable kernels need different ones. Nothing here explains why a turn-off should exist.
- **It does not adjudicate A2 vs FP1's action.** A2's lattice and FP1's C–H/K core are different microscopic
  programmes; I use A2/A12 as the canonical action per the task, and report FP1's `q_P2` embedding as the strongest
  counter-argument rather than dismissing it. A derivation of `q` from the C–H/K core would change the answer.
- **It does not use the record's own `12.99` as a measurement.** That number is an evaluation of the same integral I
  evaluate; its role here is as a cross-check (`2π⁴/15`, 0.016%).
- **No EFE, no Cassini quadrupole, no relativistic completion.** The strong-field statements are the isolated-sphere
  monopole with A4's bounds.

## Next

1. Put the kernel line into `FRAMEWORK_EQUATIONS`: `ν = (1+√(1+4/y))/2`, `y_t = 66.38` on the Λ-tied footing, and the
   fact that `12.99` is `2π⁴/15` (RAR) — so the entry point stops carrying a number from a kernel the theory rejects.
2. Replace `nu_mono` by a single definition in the repo (`FP1:141` vs `ChainCert/Kernel.lean:7` vs
   `CFG665:13` currently name three different functions); the log-divergent bare integral of the splice
   (`δh_p Y ln Y`) should be recorded wherever the splice is used for a vacuum argument.
3. Fit `(Υ, a₀, y_t)` jointly on SPARC with the canonical kernel and the turn-off left free: the pre-registered
   test is whether the fit pulls `y_t` away from `66.38`. That is the one number that would turn this lane's
   `CLOSED-DERIVED` into an empirical confirmation or a refutation.
