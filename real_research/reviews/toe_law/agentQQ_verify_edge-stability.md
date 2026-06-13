# agentQQ_verify — Hostile referee: Route 2 (Edge-pinning + X2 passivity tension)

**Mandate.** Independently re-derive the CS-violation / stability finding by a *different*
method; PRIMARY CHECK — if the route claims a bounded fold, did it get it by an active gain
that is (a) FORCED by the X2 pump and (b) STABLE, or did it quietly choose an unforced
negative weight and/or ignore a growing instability? Check X2 self-consistency. Default
skepticism: assume an unstable/unforced choice until shown otherwise.

**Scripts (this verification, banked):** `agentQQ_referee_recompute.py`,
`agentQQ_referee_stability.py`, `agentQQ_referee_poles.py`,
`agentQQ_referee_proper_selfenergy.py`, `agentQQ_referee_herglotz.py`,
`agentQQ_referee_clean.py`. Coefficient quarantine held (q=1/4 / ζ̃ / (16π/3)^{1/4}
never touched).

---

## 1. Independent re-derivation (different method) — what REPRODUCES

| route claim | route's method | my independent method | result |
|---|---|---|---|
| no-ghost window σ6>σ6\*=σ4²/(4c²) | numpy root-scan of inflection cubic | **algebra**: min of (σ6 u²+σ4 u+c²) over u≥0 at u=−σ4/(2σ6), min value c²−σ4²/(4σ6); =0 ⟺ σ6=σ4²/(4c²); + Sturm real-root counts | **CONFIRMED**, threshold exact = 1/16 |
| at σ6=σ6\* inflection coincides with ω²(k\*)=0 (soft edge) | sympy factor → triple root | sympy factor reproduced; quad double-root u₀=−2c²/σ4 = inflection root | **CONFIRMED** |
| PP no-fold: passive ⇒ CS I2²≤I1I3 | 50000 random positive spectra | **Hankel/Hamburger PSD**, 200000 random positive spectra, new RNG | **CONFIRMED**, 0/200000 |
| signed (active) weight flips CS | one signed example | independent signed example I2²−I1I3=+0.675 | **CONFIRMED** |
| "active (Im<0 band)" ≠ "anti-damped (UHP pole)" | isolated neg-residue Lorentzian | re-derived poles ±√(ω0²−γ²/4)−iγ/2 and Im χ sign for 3 cases | **CONFIRMED** (route is right) |

The structural spine of the route reproduces cleanly by independent methods. The window
existence, the boundary geometry, PP, and the residue/damping distinction are all real.

---

## 2. PRIMARY CHECK — was the bounded fold delivered by a FORCED and STABLE active gain?

### (a) FORCED? — No. Forced in DIRECTION only, exactly as the route says.
The route's own claim is "FORCED IN DIRECTION, FREE IN MAGNITUDE," and that is correct and
honest. X2 (independently) forces the medium active; PP (independently) forces non-passivity
to bound the fold; they converge on the *sign*. But reaching σ6 ≥ σ6\* (the magnitude that
actually bounds the fold) is **not** delivered by the smooth GH continuum (which gives σ6<0,
the ghost side) — it is a codimension-1 tuning supplied only by the unbanked peaked QNM. So
the CS-violation **direction** is forced; the fold-bounding **magnitude** is free/QNM-tuned.
**The fold is NOT forced.** The route states this; I confirm it.

### (b) STABLE? — Demonstrated POSSIBLE, not demonstrated as DELIVERED. Two real gaps.

**Gap (i) — TWO-OBJECT CONFLATION (the main finding).** The route reports "stable AND
active" but proves the two adjectives on **different objects**:
- *Stability* is read off the **spatial** dispersion ω²(k)=c²k²+σ4k⁴+σ6k⁶ being real and
  positive (`agentQQ_part7`). But a real ω²(k) is a **lossless** dispersion — its propagator
  has zero imaginary part off-shell (my `agentQQ_referee_recompute.py`, Attack C, computed
  ImG off-pole ≡ 0 across k). With σ4<0, σ6>0 this is **literally the superfluid-He-4 roton
  form** and is **not active at all**.
- *Activeness* is read off a **separate temporal** Lorentzian with a negative residue
  (`agentQQ_part8`).

These are the same physical response only if the self-energy that *generates* σ4<0, σ6>0 is
the negative-residue/LHP one. The route **asserts** this (σ4=+∫ρ/s, σ6=−∫ρ/s²) but never
computes the dressed propagator. So "a stable active gain bounds the fold" is shown
**possible for a toy**, not shown to be what the dS pump does.

**Gap (ii) — INFLECTION-vs-ROTON / knife-edge (`agentQQ_referee_stability.py`, Q1).** At the
route's own showcase in-window value σ6=0.10, the dispersion has **no roton minimum and no
soft point**: group velocity > 0 everywhere (min v_g = +0.25). A genuine soft sonic edge
(ω(k\*)→0, v_g=0 — the NN edge the whole Airy story needs) exists **only at the tuned triple
point σ6=σ6\***. Scan (σ4=−0.5 fixed):

| σ6 | true roton dip (v_g<0 band)? | min v_g |
|---|---|---|
| 0.0625 (=σ6\*) | yes | −2.00 |
| 0.07 | yes | −0.43 |
| 0.08 | yes (marginal) | −0.076 |
| **0.10** | **NO** | **+0.25** |
| 0.15, 0.25, 0.5 | NO | positive |

So Part 7's sweeping "v_g=0 at the roton minimum = the soft edge" for {0.07, 0.10, 0.25} is
**false except near the boundary**. The "pin at the edge" is specifically **at the marginal
point σ6\*** where ω²(k\*) *kisses zero* — a soft/borderline mode — **not** comfortably
inside a stable window. The route mixes window-interior examples (σ6=0.10, robustly gapped
but no edge) with the edge condition (σ6=σ6\*, has the edge but is marginal). You cannot have
both the genuine soft edge AND a robust positive gap at the same σ6: the edge lives at the
knife-edge.

**Gap (iii) — dressed-pole stability NOT computed.** The PRIMARY CHECK asks whether the
active response keeps the *dressed* khronon pole in the LHP. The route reads stability off
ω²(k)>0 (a lossless criterion) and an isolated-block toy; it never solves for the poles of
the full retarded propagator with the active self-energy. My attempts to settle this
(`agentQQ_referee_poles.py`, `_proper_selfenergy.py`, `_herglotz.py`) showed the question is
genuinely subtle: any propagator written even-in-ω² forces conjugate-symmetric ±ω* root
quadruplets and cannot be used to read retarded stability (my "passive baseline" spuriously
showed UHP poles — a kinematic artifact, flagged and discarded). The clean first-order-in-ω
test (`agentQQ_referee_clean.py`) **confirms** the route's narrow claim — a negative-residue,
positive-Γ block is active AND LHP-stable — but a banded active correction's effect on the
*full dressed* pole at the magnitude needed to reach σ6≥σ6\* remains **uncomputed**. That is
exactly the QNM calculation the route defers, so the gap is honestly located, not hidden.

---

## 3. X2 self-consistency — RESPECTED (the route's adjudication is correct)

The brief's worry (an active medium violating CS re-violates the passivity X2 *uses*) is
correctly dissolved: X2 *concludes* non-passivity from premises (P1 causality, P2 convergent
dispersion, P3 stability); it does not *assume* a passivity it then needs protected. PP's
non-passivity = X2's conclusion. No logical clash. My `agentQQ_referee_clean.py` (1) confirms
the only real danger — that the active band forces a UHP pole (anti-damping) — does **not**
follow automatically: active (Im χ<0 band) and anti-damped (UHP pole) are genuinely distinct,
and a banded active response can be Im≥0 outside the band and bounded/causal. **No
contradiction with X2.** This part of the route is solid.

---

## 4. Regrade

**Recompute AGREES with the route's verdict: PARTIAL-NEEDS-MORE.** The route did **not**
deliver the fold, did **not** smuggle a forced fold, and was honest that the magnitude/pin is
QNM-tuned and unforced. The CS-violation is forced in direction (X2+PP converge), free in
magnitude. Stability is shown **possible**, not delivered.

Three corrections that **tighten** (do not overturn) the verdict, all in the "be at least as
skeptical of a favorable claim" direction:
1. **"Stable AND active" is proven on two different objects** — stability on a lossless roton
   dispersion, activeness on a separate Lorentzian. Their identity is asserted, not derived.
2. **The "edge pin" sits at the marginal-stability knife-edge σ6\*** (ω²(k\*)=0, a soft
   mode), not inside a comfortable stable window; the genuine soft edge and a robust gap are
   not simultaneously available. The route's "stable in the window" examples (σ6=0.10) have
   no edge; the edge point (σ6\*) is marginal.
3. **The dressed-pole stability the PRIMARY CHECK targets is asserted from a toy, not
   computed** — correctly deferred to the QNM calculation, but it means "STABLE" is
   provisional, not established.

**Regrade: CONFIRMED (verdict unchanged: PARTIAL-NEEDS-MORE), with the "stable" axis
downgraded from established to possible-pending-QNM.** The route is not guilty of the default
charge (unstable or unforced choice passed off as a delivered fold); it correctly reports the
fold as not delivered. But its "stays stable & causal — bounding the fold does NOT require an
instability" is stronger than what it proved: it proved a stable active response *can exist*,
on toys, with the actual pin landing at a marginal soft point and the dressed-pole stability
uncomputed.
