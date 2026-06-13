# HOSTILE VERIFY — route 2 (heat-kernel / proper-time), agentNN

**Mission:** is the claimed Airy structure REAL and PUMP-SPECIFIC, or is it the free turning
point agentMM (fb0ff706) already killed, smuggled back in? Default skepticism: assume the Airy
was wished into existence until the pump-specific mechanism is shown explicitly.

**Method:** independent re-derivation by DIFFERENT methods from NN, plus a ruthless free-vs-pump
firewall test. Script `agentNN_verify_heatkernel.py`, exit 0, reproducible. Coefficient quarantine
intact (ζ̃, (16π/3)^{1/4} never appear).

---

## V1 — Saddle-class ↔ edge-index map, re-derived by DIRECT DOS exponent counting (≠ NN's stationary phase)

For ω ~ A k^p at a band extremum, exact symbolic differentiation gives ρ(E) ~ E^{1/p−1}:
- p=2 (quadratic / Gaussian): slope **−1/2** (van Hove) — reproduces NN-3a.
- p=3 (cubic inflection): slope **−2/3**.
- p=4: slope −3/4. The hierarchy is exactly the catastrophe codimension ladder.

The OSCILLATORY (turning-point) index — the load-bearing one — re-derived from `mp.airyai`
directly (≠ NN's rotated contour): the envelope **|Ai(−w)|·w^{1/4} → 1/√π = 0.56418958** to **7
digits** across w ~ 1e2, 1e3, 1e4 (peak-tracked; see correction note below). Amplitude index −1/4,
stretch (2/3)w^{3/2}, oscillatory index 1/3 — **CONFIRMED by an independent representation.**

> **Correction note (honesty):** my first envelope probe sampled |Ai(−w)| at three isolated huge w
> (1e3,1e6,1e9) and got 0.31/0.07/0.25 — NOT flat. That is a **phase-sampling artifact** (|Ai| dips
> to 0 at its zeros; the −1/4 law is an *envelope*, not a pointwise, statement). Re-probing the
> **local maxima** per decade flattens to 1/√π to 7 digits (run logged). The index claim survives; I
> flag the artifact rather than bury it.

**V1 AGREES with NN-3.** The saddle-class ↔ index map is sound and method-independent.

---

## V2 — FIREWALL A: can the FREE khronon fake a cubic fold with NO higher-derivative term? **NO.**

Hunted every free/quadratic structure for a hidden coalescence:
- **[V2a]** Most general 2-derivative dispersion ω²=c₀²k²+m²: ω″(k)=c₀²m²/(c₀²k²+m²)^{3/2}, **no real
  finite inflection root**, strictly convex. No fold.
- **[V2b]** Luminal massless line ω=c₀k: ω″≡0 *everywhere* → degenerate, non-isolated (the cone), not
  an isolated turning point → simple-pole / Rayleigh-Jeans edge (MM), not Airy.
- **[V2c]** The sinh^{−2} Matsubara **double pole** is NOT a coalescing saddle. Decisive tail test:
  fit log(w/(e^{2πw/κ}−1)) — residual **8.5e-3 against a·w (simple exp)** vs **6.1e-1 against a·w^{3/2}
  (stretched)**. The pole tail is a **simple exponential (Gevrey-1)**, NOT the stretched-w^{3/2} of a
  fold. A pole ≠ a fold.

**FIREWALL A HOLDS. NN's "free = non-Airy" is CORRECT and reproduced from the saddle side. The Airy,
IF present, is genuinely NOT the free turning point — so the route does NOT contradict MM.** This is
the single most important finding: the route does not smuggle MM's dead object back in.

---

## V3 — FIREWALL B: even granting the inflection, is it the OSCILLATORY (Ai(−w)) side? **A SECOND, SEPARATE condition.**

An inflection ω″(k*)=0, ω‴≠0 gives a cubic → Airy. But Airy has TWO regimes: **Ai(+w) DECAYS**
(tunneling, NOT the √3 lock) and **Ai(−w) OSCILLATES** (the required index-1/3 / √3 fingerprint LL
pinned). Which one the b→c_χ edge actually probes is **set by sign(ω−ω(k*)) vs sign(ω‴)** — a
condition the *existence* of the fold does NOT supply.

- **[V3a]** Test roton ω=√(k²−k⁴+0.1k⁶): fold at **k*≈3.286**, ω‴(k*)=+38.7 (genuine), ω(k*)=4.484.
  sign(ω‴)=+1 ⇒ the oscillatory side is ω < ω(k*). **Whether the edge sits on that side is a SECOND
  tuning**, which NN silently absorbs into the one word "coincidence."
- **[V3b]** Convex ω=√(k²+k⁴): no inflection — confirms the SIGN of k⁴ is load-bearing (NN-5a echo).

---

## V4 — SMUGGLE SCORECARD: 'fold exists' vs 'fold AT the edge, oscillatory, generated'

| req | what it is | status |
|---|---|---|
| **R1** inflection EXISTS (ω″=0, ω‴≠0) | needs sign-indefinite k⁴(+k⁶); free/massive op provably lacks it (V2) | **non-free, named, real** ✓ |
| **R2** inflection AT the edge saddle (ω′(k*)=v_edge, ω(k*)=edge freq) | tuning | folded into "coincidence", **not derived** |
| **R3** edge probes the OSCILLATORY Ai(−w) side | second tuning (V3) | folded into "coincidence", **not derived** |
| **R4** the pump self-energy actually GENERATES k⁴ with the bending sign + k⁶ floor | the in-medium dispersion correction | **UNCOMPUTED** (NN's `next_calc`) |

**R1 is a genuine win** — a structure the free theory lacks, so the Airy is NOT MM's smuggled
turning point. But **R2, R3, R4 are all undischarged**: two are tuning conditions hidden inside one
word, one is the entire uncomputed generation step. The route **identifies** a non-free mechanism;
it does **not force** Airy. The Airy is one *admissible, tuned, sign-selected, ungenerated*
possibility, not a derived consequence.

---

## V5 — √3 lock, recomputed by a DIFFERENT representation (≠ NN-6 split-cubic)

From the LL-2.2 closed form 2·3^{1/3}e^{−w^{1/3}/2}cos((√3/2)w^{1/3}): osc/decay = (√3/2)/(1/2) =
**√3** (sympy exact). Independently, the cube-root-of-unity geometry (roots at ±π/3): Im/Re =
**tan(π/3) = √3** (exact + numeric 1.7320508076). **Reproduces NN-6's √3 lock by a different algebra.
The fingerprint mathematics is sound.**

---

## REGRADE

- **recompute_agrees:** PARTIAL. NN's *internal* mathematics all reproduces (saddle map, free=non-Airy
  firewall, √3 lock — all AGREE, independent methods). What does NOT survive unchallenged is the
  *strength* of the conclusion: NN's own `verdict: MECHANISM-CANDIDATE` is the honest ceiling, but its
  prose understates how much is assumed — R2+R3 are two distinct tuning conditions compressed into
  "coincidence", and R3 (oscillatory vs tunneling side) is a real, separate hostile point NN did not
  isolate.

- **free_vs_pump_distinction_HOLDS.** This is the verifier's primary mission and the answer is clean:
  **the Airy is NOT the free turning point MM killed.** FIREWALL A (V2) shows no free/quadratic
  structure — mass, luminal line, or Matsubara double pole — can manufacture a cubic fold; the
  required object is a sign-indefinite higher-derivative (roton) term provably absent from the free
  action. So the route does NOT contradict MM and is NOT a smuggle. **No OVERTURN.**

- **regrade: CONFIRMED** (verdict unchanged, MECHANISM-CANDIDATE). The route survives hostile review
  *as a candidate*: it correctly localizes a non-free, named, falsifiable operator requirement (R1)
  and does not over-claim a derivation. But it is firmly a candidate, not a mechanism: the index-1/3
  Airy is NOT forced — R2 (edge-coincidence), R3 (oscillatory side), and R4 (sign-correct generation
  from the pump self-energy) are all undischarged. The honest next calc is R4: compute the in-medium
  self-energy and test whether the k⁴ coefficient has the bending sign with a k⁶ floor; if it comes
  out convex or absent, MM's kill stands and the route collapses to non-Airy.
