# agentQQ — Route 2: Edge-pinning + the X2 passivity tension (Link 5 self-consistency)

**Round question (structure, not coefficient).** Can the X2 ACTIVE-GAIN dS response
(a) violate Cauchy–Schwarz I2² ≤ I1 I3 to give σ6 > 0 and BOUND the roton fold,
(b) pin the inflection k* at the b→c_χ sonic edge (set by H / the dS bath), and
(c) stay stable/causal — without CONTRADICTING the very X2 passivity structure that
forced the medium active in the first place? Coefficient quarantine held (q=1/4,
ζ̃, (16π/3)^{1/4} never asserted).

Inputs read: `agentX_sk_gate.md` (Theorem X2: μ̂(0) ≥ μ̂(∞) for passive media; deep-MOND
forces the inverted ordering ⇒ ACTIVE secular channel) and `agentNN_horizon_airy.md`
(edge-coincidence: ω″(k*)=0 must sit AT b→c_χ; roton k⁴+k⁶ operator).
Banked: agentPP No-Fold Theorem (passive ⇒ Herglotz/Pick ⇒ monotone ⇒ no fold;
bounded fold needs CS-violating negative spectral weight).

---

## PART 1 — CS-violation ⟺ negative spectral weight ⟺ X2-passivity violation (the identity)

Computed (`agentQQ_part1.py`):
- X2 sum rule: μ̂(0) − μ̂(∞) = (2/π)∫₀^∞ Im μ̂(λ)/λ dλ. PASSIVE bath (Im μ̂ ≥ 0) ⇒
  μ̂(0) ≥ μ̂(∞). MOND needs μ̂(0) < μ̂(∞) ⇒ a band with **Im μ̂ < 0 (active)**.
- CS on spectral moments: I2² ≤ I1 I3 for ANY positive measure (log-convexity).
  50000/50000 random POSITIVE spectra satisfy it (0 violations — re-confirms PP).
  σ6 ∝ −(I1 I3 − I2²) ≤ 0 for passive ⇒ fold UNbounded.
- A signed (active) spectrum weights=[+1.0, −0.3] gives I2² − I1 I3 = +0.675 > 0
  ⇒ CS violated ⇒ σ6 can flip positive ⇒ fold bounded.

**THE IDENTITY (this round's spine): "bound the fold" = "σ6>0" = "CS violated" =
"negative spectral weight in a band" = "Im μ̂<0 in a band" = the SAME active response
X2 already proved is FORCED by deep-MOND.** The fold-bounding demand and the X2 active
demand are not two requirements — they are the same sign of the same spectral weight.
This is the first half of the self-consistency answer and it is FAVORABLE: PP and X2
ask for the same thing.

(continued below)

---

## PART 2–3 — the moment map and what "bound the fold" means structurally

Self-energy in Herglotz form Π(k)=∫ρ(s) k⁴/(s+k²) ds expands as
σ4 = +∫ρ/s ds, σ6 = −∫ρ/s² ds. For ρ≥0 (passive): σ4>0 (convex, no bend). The dS
bath gives σ4<0 (banked 851e7649: σ4=−I2 c_χ²<0 FORCED) ⇒ the bath's effective ρ is
already negative-weighted (active) on the bend axis. The k⁶ FLOOR σ6>0 ⟺ ∫ρ/s² ds < 0
⟺ ρ<0 in a band ⟺ **anti-Herglotz** = EXACTLY PP's CS-violation = EXACTLY X2's Im μ̂<0.
**These are one object, confirmed three times (Parts 1, 3, 9).**

Dispersion ω²(k)=c_χ²k² + σ4 k⁴ + σ6 k⁶ (σ4<0 the forced bend). Computed:
- σ6 ≤ 0: ω²→−∞ ⇒ ghost / complex k ⇒ the UNBOUNDED PP fold (instability).
- σ6 > 0: a k⁶ floor; whether it bounds without a ghost depends on its SIZE.

## PART 4–5 — THE CONSISTENT WINDOW (the existence proof)

No-ghost condition (ω²/k² = σ6 u² + σ4 u + c_χ² > 0 ∀u=k²>0):
> **σ6 > σ4²/(4 c_χ²) ≡ σ6\*  (threshold).**

Inflection (fold) cubic 6σ6²u³+9σ4σ6u²+(10c_χ²σ6+2σ4²)u+3c_χ²σ4=0. Scanned
(c_χ²=1, σ4=−0.5, σ6\*=0.0625; `agentQQ_part4_window.py`):

| σ6 | ghost? | k* (real infl, ω²>0) | ω²(k*) |
|---|---|---|---|
| 0.050 | YES | 2.93 | 3.42 (ghost band elsewhere) |
| **0.0625 (=σ6\*)** | **no** | **2.00** | **0.0000** |
| 0.070 | no | 1.60 | 0.46 |
| 0.10 | no | 1.27 | 0.73 |
| 0.25 | no | 0.78 | 0.48 |

**EXACT boundary fact (sympy, `agentQQ_part5_boundary.py`):** at σ6=σ6\* the inflection
cubic factorizes as 3σ4(2c_χ²+σ4u)³/(8c_χ²) ⇒ a TRIPLE root at u\*=−2c_χ²/σ4, which is
EXACTLY the marginal ghost-touch where ω²(k\*)=0. **At threshold the fold's inflection
coincides with the point where the dispersion goes SOFT (ω→0) — the sonic edge itself.**

> **WINDOW VERDICT: the window σ6 > σ6\* is NON-EMPTY. A CS-violating (anti-Herglotz)
> k⁶ floor of sufficient size bounds the fold with a real inflection k*, ω²(k*)>0, and
> NO ghost. Active-enough-to-bound AND stable coexist.**

## PART 6 — EDGE-PINNING (question a): SCALE pinned, COINCIDENCE not forced

Dimensional structure (bath's only scale = H, c=1): α∼a₀/H², β∼b₀/H⁴ ⇒
k\*² = 2c_χ²/α ∼ 2c_χ²H²/a₀ ⇒ **k\* ∼ (c_χ/√a₀)·H — the inflection SCALE is bath-set.**

Input count: c_χ² (khronon kinetic, banked); α=−σ4 (k⁴ bend) SIGN forced <0, MAGNITUDE
=I2 c_χ² a bath moment; β=σ6 (the floor) is the CS-violating/active piece. PP: the SMOOTH
GH continuum gives σ6<0 (CS forces it) — the WRONG side, no floor, ghost.

> **EDGE-PINNING VERDICT: the bath PINS the SCALE (k\*∼H) but does NOT force the
> COINCIDENCE. Pinning k\* exactly at the soft edge ⟺ tuning σ6=σ6\*=α²/(4c_χ²), a
> codimension-1 condition. The smooth bath fails it (σ6<0). k\*'s coincidence with
> b→c_χ requires the PEAKED dS QNM resonance (NN's named unbanked input), whose strength
> must be tuned to hit σ6\*. k\* is NOT free (its scale is fixed by H), but it is NOT
> auto-pinned at the edge either — the pin is a tuning, supplied only by the QNM.**

## PART 7–8 — THE DEEP TENSION adjudicated: NO CONTRADICTION

The brief's worry: X2 is a passivity bound, so an active (CS-violating) medium "risks
violating the passivity/stability X2 uses." Adjudicated precisely:
- **X2 RELIES ON:** (P1) causality/UHP-analyticity, (P2) convergent dispersion relation,
  (P3) stability/no-runaway (X §6c). X2 **CONCLUDES** the medium is non-passive (active).
- **PP RELIES ON** passive⇒Herglotz; **CONCLUDES** bounded fold needs non-passive.

⇒ **PP's "non-passive" is X2's CONCLUSION, not X2's premise.** No logical clash there;
they AGREE the medium is active. The only genuine danger is if the active band breaks
P1 or P3. Tested:
- **P1 (causality):** in the window σ6>σ6\*, ω²(k)>0 ∀k ⇒ ω(k) real ⇒ retarded poles in
  LHP ⇒ causal, no runaway. The SAME σ6>σ6\* that bounds the fold SECURES causality.
- **P3 (stability):** ω²>0 (no gradient/ghost instability); group velocity real & finite,
  vanishing only at the roton minimum (= the soft edge). Verified σ6∈{0.07,0.10,0.25}.

**The distinction that dissolves the tension (`agentQQ_part8_residue.py`):**
"non-passive / Im χ<0" (residue SIGN) ≠ "anti-damped / pole in UHP" (DAMPING sign =
runaway). A negative-RESIDUE, positive-γ Lorentzian delivers SIMULTANEOUSLY:
(i) Im χ<0 in a band (active, PP+X2 satisfied), (ii) poles in LHP, impulse response
g(t)∼e^{−γt/2}sin(ω_r t) causal & DECAYING (P1+P3, no runaway), (iii) χ(0)<χ(∞) (the
X2 inverted ordering). **All three at once.** Passivity is broken by the spectral-weight
SIGN; stability is about pole LOCATION. A medium can be active AND stable AND causal.

## PART 9 — bath-limited, not perpetual motion

Active power into the worldline ∼ |Im χ|·|drive|² is FINITE, bounded by the bath's
free-energy throughput (X §5: ∼10³³–10³⁵ W per L*-galaxy, dS bath covers with ×10²–10⁴
box / ~15-order horizon margin). Stable active gain is a bath-powered amplifier with an
accounted budget, not perpetual motion. Sampled P_æ = +0.044 / +2.50 / +0.14 at
ω=0.5/1.0/1.5 — finite, positive, bounded.

---

## OVERALL VERDICT — PARTIAL-NEEDS-MORE (consistent window proven; pin still needs the QNM)

The make-or-break self-consistency check **PASSES**: the X2 active-gain dS response and
the PP bounded fold are NOT incompatible — they are the SAME active (anti-Herglotz /
negative-spectral-weight) demand, and that demand can be met by a STABLE, CAUSAL,
bath-limited response (negative residue, positive damping; ω²>0 window σ6>σ6\*). The
feared contradiction was a premise/conclusion conflation: X2 CONCLUDES non-passivity
(it does not assume passivity it then needs protected), and the premises X2 truly uses
(causality, stability) survive the fold-bounding active response.

**Sub-answers:**
- **(a) CS-violated to bound the fold?** STRUCTURE PERMITS IT (no-stays… → "yes, but"):
  σ6>0 ⟺ CS-violation ⟺ X2-activeness; the window σ6>σ6\* bounds the fold cleanly.
  It does NOT happen in the passive band — it requires the active response, which X2
  independently forces. So the CS-violation is **forced in DIRECTION** (X2+PP agree the
  medium is active) but its **MAGNITUDE** (reaching σ6≥σ6\*) is the unbanked QNM tuning.
- **(b) Edge-pinning:** k\*'s SCALE is bath-pinned (∼H); its COINCIDENCE with b→c_χ is a
  codimension-1 tuning (σ6=σ6\*) the smooth bath fails — needs the peaked QNM. k\* not
  free, not auto-pinned: pinned-in-scale, tuned-at-edge.
- **(c) Stable/causal?** YES — STAYS STABLE & CAUSAL in the window; active ≠ unstable.
  Bounding the fold does NOT require an instability (negative residue, not negative
  damping). NO contradiction with X2.

**The honest residual gap (unchanged Link-5 status):** that a stable active response
EXISTS is proven here; that the dS PUMP realizes it as negative-RESIDUE (stable gain)
of magnitude σ6≥σ6\* — rather than the smooth-continuum σ6<0 (ghost) or a negative-
DAMPING runaway — is the COUPLING question = Link 5's named unbanked input (the peaked
dS QNM horizon resonance). The structure PERMITS the fold and is SELF-CONSISTENT with
X2; it does not FORCE the fold.

**Coefficient quarantine held:** q=1/4, ζ̃, (16π/3)^{1/4} never asserted; this round
computed only the STRUCTURE (window existence, edge-pin tuning, stability sign).
