# L20 — the ghost in the past of IC10's plateau: reachable, and what to do about it

2026-09-08. Lane L20 of [CHARTER.md](CHARTER.md), following up the one new liability raised by
[L8_VERIFICATION.md](L8_VERIFICATION.md) (its checks D7/D8).
Script: [L20_ghost_past.py](L20_ghost_past.py) → [L20_ghost_past.out](L20_ghost_past.out). **23 checks, 23 PASS, exit 0.**

Method: the IC10 pressure was re-transcribed from `IC10_LOCAL_CLOCK.md`'s displayed formula and
re-differentiated in sympy; the auxiliary root `P_w = 0` is solved by my own Newton iteration; the two FLRW
evolution laws are **derived here** from the shift-symmetric charge rather than taken from IC10 (L20-C2); the
quadratures are my own. Nothing under `closure_2026/integrable_clock_construction_2026/` was imported or run.
Six controls guard the algebra, including the textbook `P = X^n` k-essence limit, IC10's own
`S = 0.1 → 0.2` quadrature, and a numerical-differentiation check that `Q_clock` really is
`(P_eff'' + P_eff')/(2X̃)` for the **eliminated** one-variable pressure `P_eff(S) = P(S, w̄(S))`.

---

## The short answer

**The ghost edge is reachable, at finite past proper time — 0.154/h₀, i.e. 0.104 physical e-folds back,
internal z = 0.110 from the lead's own S = 0.2 sample. It is not an asymptotic floor and not a continuation
artefact. But the solution does not pass *into* the ghost region: it terminates at the edge, at a fold in the
scale factor. The liability is real and it is not fatal; the repair that costs nothing is a retune of IC5's
activation window, and a coefficient tune provably is not the repair.**

---

## 1. The map of the backward history (L20-H1, H2, H3)

Reproduced from my own algebra (L20-C3, C4), in the clock variable S:

| | S | r² | c_s² | Q_clock | ρ |
|---|---|---|---|---|---|
| η = 1 lower edge (r² = 3/4) | 0.0016326245 | 0.750000 | −0.0257 | −67.94 | 2.6418 |
| **Q_clock = 0 — ghost below** | **0.026664091** | **0.901939** | **→ +∞** | **0** | **2.9084** |
| **c_s² = 1 — superluminal below** | **0.037700985** | **0.932562** | **1** | **2.0760** | **2.8966** |
| lead's samples | 0.10 / 0.15 / 0.20 | 1.0530 / 1.1305 / 1.2045 | 0.3690 / 0.3064 / 0.2651 | 5.26 / 5.73 / 5.84 | 2.67 / 2.45 / 2.25 |
| η = 1 upper edge (r² = 5/4) | 0.230723991 | 1.250000 | 0.2423 | 5.8378 | 2.1333 |

Integrating IC10's own `dS/dτ = 3 H̃ c_s²` and `dln Ā/dS = 1/(3 c_s²)` **backwards** from S = 0.2:

| back to | Δτ (1/h₀) | barred e-folds | physical e-folds | internal z |
|---|---|---|---|---|
| superluminal onset S = 0.0377010 | 0.152078 | 0.151809 | 0.105841 | 0.11165 |
| ghost/degeneracy edge S = 0.0266641 | 0.153984 | 0.153846 | 0.104029 | 0.10963 |
| *(forward)* η = 1 upper edge S = 0.230724 | 0.043511 | 0.040404 | 0.033170 | — |

The whole superluminal band is crossed in **0.0019/h₀ — 1.2%** of the backward interval, because the integrand
`dτ/dS = Q_clock/(3 H̃ P_X)` vanishes at the edge.

**Redshift: it cannot honestly be tied to anything physical, and that is itself the finding** (L20-H3). The
plateau is a vacuum toy with no matter and no normalisation to today. The only defensible number is the
*internal* one, z = 0.110 relative to the lead's own S = 0.2 sample. Carried anyway, clearly labelled as
conditional and on **both footings**: if one identifies the IC-internal `a₀ = √(9κe^{−1/2}/(16 m ℓ²)) = 2.43412`
with the empirical a₀ — an identification IC10 explicitly declines ("the a₀–Λ proportionality and its 1/2
coefficient remain input") — then h₀ = 1.28292e-19 s⁻¹ = 0.0587 H₀ (canonical 9.3619e-11) or
1.54563e-19 s⁻¹ = 0.0708 H₀ (alt 1.1279e-10), the plateau's own H̃ is 0.0553 H₀ / 0.0666 H₀, and the ghost edge
sits 38.0 Gyr / 31.6 Gyr back. Both footings say the same thing: the toy expands 15–18× slower than the real
universe, so the ghost is **not** a statement about the real early universe in either direction.

---

## 2. Reachable, or an asymptotic floor? — **reachable** (L20-G1)

The mandated fork was (a) finite past proper time, or (b) an asymptotic floor in S. **It is (a), by the
integral, not by assertion.** `Q_clock` vanishes *linearly* at the edge while `H̃` and `P_X` stay finite and
positive (L20-H1: ρ = 2.9084, H̃ = 1.0702, P_X = 2.0658 there), so `dτ/dS → 0` and the quadrature converges.
Convergence was tested by shrinking the lower endpoint decade by decade: the residual interval falls by 97.9×
then 99.8× per decade, the quadratic law of a linearly vanishing integrand. Total Δτ = 0.153983862606/h₀.

**But the nature of the boundary matters, and it softens the verdict (L20-G2).** From my own charge relation,
`dF/dS = −Q_clock e^{−S}` with `F = P_X e^{−S}` and `Ā³F = const`, so **F is maximal exactly where Q_clock = 0**.
Since H̃ > 0 makes Ā monotone in τ, the barred scale factor can only fall to

    Ā_min / Ā(S=0.2) = (F(0.2)/F_max)^{1/3} = 0.8574040385

and below that **no S solves the charge relation at all**. Ā rises again for S < S_ghost (0.86614 at S = 0.01):
the Q < 0 region is the **second branch through the same fold**, running forward in time from the same point —
not the past of the healthy solution.

So the precise statement is **not** "there is a ghost in the history". It is (L20-G3):

> IC10's expanding plateau solution is **past-incomplete at finite proper time**, at finite density, finite H̃
> and with η still exactly 1 (r² = 0.901939, inside |r²−1| ≤ 1/4), at a point where the clock's principal
> symbol degenerates — c_s² → +∞, the coefficient of the time derivative vanishing. It is not a curvature
> singularity, and it is **not** the η boundary the lead's open item 1 is waiting for: η = 1 continues
> **16.3× further down**, to S = 0.0016326.

---

## 3. What sets the initial S? — **nothing; it is free initial data** (L20-S1, S2)

The plateau pressure depends on the clock only through `X̃`, never on `T`: shift symmetry, conserved charge
`Ā³ P_X √(2X̃)`, and the **value** of that charge is initial data. Neither the action, nor `P_w = 0`, nor the
Friedmann constraint picks a value of S. So **avoiding the ghost is a constraint on initial data, not a defect
of the theory** — a much weaker problem, and it should be stated that way.

Quantified, because a theory healthy only on restricted initial data is a weaker theory:

- **84.256%** of the η = 1 range in S is healthy *and* subluminal; **89.074%** is merely non-ghost. The excluded
  sliver is the bottom 15.7%.
- The restriction is an **open** condition ("start above S = 0.0377010"), and it is **forward-invariant**:
  `dS/dτ = 3 H̃ c_s² > 0` on the healthy branch, so a datum that starts healthy stays healthy until it exits
  η = 1 at the top. Evolution never carries a good initial condition into the bad region.

---

## 4. Does the superluminal band matter? (L20-L1, L20-L2)

It is **not** a marginal excursion: c_s² = 1.23 at S = 0.035, 2.67 at 0.030, 24.0 at 0.027, divergent at the
edge, all with η exactly 1 and the auxiliary root unique. On a preferred foliation that is not automatically a
causality violation — the clock's own level sets T = const are a global time function for both cones on this
homogeneous background, so no closed causal curve arises here. "Not automatically fatal" is the most this
calculation supports; nothing stronger.

**Dependency, not duplicated here.** The parallel gravitational-Cherenkov lane decides the sign of this
question, and it inverts it. If the handoff's A5/A6 apply to this clock (bound 1 − c_s ≤ 2e-15; *"the lower
edge is always Cherenkov ⇒ the khronon must be marginally superluminal"*), then it is the lead's **subluminal**
samples that are excluded — c_s² = 0.265–0.369 is exactly where A5 excludes c_s² = 1/3 by 2.1e14× — and the only
surviving point of the entire plateau would be c_s² = 1, i.e. **precisely the superluminal onset S = 0.0377010
that this lane identifies as the edge of the healthy window**. Recorded as a conditional pincer for the other
lane to resolve.

---

## 5. Can the lead fix it? (L20-F1 … F6)

**κ and m are not levers, and this closes the cheapest repair before it is tried (L20-F1).** The IC5 relations
`m a₀² = 9κe^{−1/2}/(16ℓ²)` and `mΛ = κe^{−1/2} − m a₀² U(4/9)` make P exactly proportional to κ and independent
of m; the activation `r² = 2 e^{2S−4w−1/6} ρ/κ` is then independent of **both**. No rescaling moves either edge.

**Λ does not fix it (L20-F2).** Scanning g = Λ/Λ_IC5 over [0.6, 1.4] moves the ghost edge by a factor of 25 —
and moves the η = 1 lower edge with it. The ghost stayed inside the plateau at **10 of 10** scanned values.
Below g ≈ 0.9 the plateau stops closing at the bottom at all (r² never reaches 3/4), so η = 1 then runs to the
excluded chart locus with the ghost inside it; above g ≈ 1.4 the plateau closes up and c_s² turns negative at
the top.

**A higher-order clock kinetic term moves the edge but breaks the plateau (L20-F3).** Adding
`λ e^{2w} X̃²` (only λ/κ matters) with λ/κ = 0.83 pushes the ghost from S = 0.0267 to 0.00072 (37×) and drags
the superluminal band down with it (c_s² = 1 crossing moves to S = 0.00103) — but it does so by **adding
energy**, and r² then leaves the η = 1 window entirely (r² = 3.19 at S = 0.15). Every λ > 0 that helped the
ghost broke the plateau; no (λ, Λ) grid point kept S = 0.15 inside η = 1. **A constitutive repair has to be
energy-neutral.** That is the design constraint.

**The ghost is generic near the excluded chart locus (L20-F6).** `Q_clock → −∞` as `ξ = S + w → 0`, with local
logarithmic slope ≈ 0.78 over three decades in ξ, for λ = 0 and for every λ and Λ scanned. The deformations
move the **crossing**, never the **asymptotics**. The whole effect comes from the auxiliary elimination: the
bare `Q_bare = (P_SS + P_S)/(2X̃)` is hugely positive and *growing* (75 at S = 0.2, 1625 at the ghost edge,
82888 at S = 0.0016), and it is the Schur subtraction `P_Sw²/P_ww` — which diverges because
`∂u/∂w = S/ξ²` and `∂u/∂S = −w/ξ²` — that drives Q_clock through zero. **So this liability and the lead's own
open item 4, "establish global k = 0 / y = 0 control", are the same problem seen from two sides.**

### The concrete, checkable suggestion (L20-F4)

IC5 defines η as *"a smooth, momentum-reversal-even activation"* with η = 1 for |r² − 1| ≤ 1/4. **That window is
symmetric by choice, not by derivation.** Make the **lower** threshold `r² ≥ 0.93256` instead of 0.75 — still
smooth, still even under momentum reversal — and η = 1 then coincides **exactly** with the healthy subluminal
window S ∈ [0.0377010, 0.2307240].

- Cost to published numbers: **zero**. The three samples sit at r² = 1.052997, 1.130464, 1.204449, all interior;
  the upper edge r² = 5/4 is untouched; `plateau_boundary()` is unchanged.
- Effect: the backward handoff to the full η-derivative equations then happens **at c_s² = 1**, before the
  degeneracy, instead of 16× past it.
- **Stated honestly: this does not make the ghost go away. It makes it the transition sector's problem — which
  is already the lead's open item 1 — and that is the right place for it.** The certified plateau would then
  contain no unhealthy point, which is what "computationally verified in the stated range" ought to mean.

---

## 6. The calibration that keeps this honest in the other direction (L20-V2)

**The ghost is not the binding limitation on IC10, and saying so is part of the answer.** The entire certified
healthy, subluminal plateau — past terminus to future η exit — lasts **0.139012 physical e-folds, a factor
1.1491 in the physical scale factor**. A construction that expands by 15% between its past degeneracy and its
future η exit is a *local witness*, exactly as IC10 labels itself ("emphatically not a realistic full
cosmology"). The past boundary found here is a defect of that witness, not of a cosmological history it never
claimed to have.

---

## Verdict (L20-V1) — three sentences

The ghost region **is** reachable: IC10's own evolution law, integrated backwards from its own S = 0.2 sample,
reaches the `Q_clock = 0` degeneracy after 0.154/h₀ of proper time (0.104 physical e-folds, internal z = 0.110)
at finite density and finite H̃, with η still exactly 1 — so the certified-healthy window is genuinely smaller
than the plateau and the difference lies in the plateau's own past, not off to one side. It is **not fatal**:
the healthy branch terminates at a fold in the scale factor rather than entering the ghost region, S is a free
and forward-invariant initial condition so the exclusion is a restriction on initial data covering 84.3% of the
plateau, and the whole plateau is only 0.139 physical e-folds long in any case. It **is** a real defect of the
certified region that should not be left standing, and the repair is not a coefficient — κ, m, Λ and a
higher-order clock kinetic term all provably fail — but a one-line retune of IC5's activation to
`r² ≥ 0.93256` on the low side, which costs no published number and moves the past handoff to c_s² = 1.

---

## Not attempted here

The finite-k companion-matrix behaviour near the degeneracy; whether the *inhomogeneous* clock equation is
still hyperbolic in the band; the gravitational-Cherenkov applicability question (parallel lane, L20-L2);
anything off η = 1, including whether the full transition action would in fact hand the plateau a clean past
boundary at r² = 0.93256. The energy-neutral constitutive repair that L20-F3 says is the real fix has **not**
been exhibited — only the constraint it must satisfy.
