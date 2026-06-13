# agentQQ — BANKING MEMO: can the X2 ACTIVE dS pump deliver the controlled roton fold while staying consistent with X2? (2026-06-13)

**Round question (structure, not coefficient).** Theorem agentPP (commit 9f02cbce) proved the
NO-FOLD THEOREM: any PASSIVE (ρ≥0) self-energy is Herglotz/Pick ⇒ monotone dispersion ⇒ NO
passive bath folds; a controlled bounded fold provably needs a NON-PASSIVE response that violates
Cauchy–Schwarz I2²≤I1·I3 (negative effective spectral weight). This converges with Theorem X2
(agentX_sk_gate.md): causality + the deep-MOND inversion already force the medium ACTIVE/pumped.
So this round tested the X2 ACTIVE-GAIN dS response on three demands:
**(a)** violate Cauchy–Schwarz to give σ6>0 and BOUND the fold;
**(b)** pin the inflection k* at the b→c_χ sonic edge;
**(c)** stay STABLE/causal — without contradicting the very X2 passivity structure that forced the
medium active. The tension to respect: X2 is itself a passivity bound, so a CS-violating active
medium risks breaking the stability X2 relies on. Coefficient quarantine held throughout
(q=1/4, ζ̃, (16π/3)^{1/4} never asserted — only signs, pole counts, branch/window structure).

Two routes ran, each hostile-verified by an independent referee. **Counted at VERIFIED grade only.**

---

## ROUTE 1 — ACTIVE-GAIN CAUCHY–SCHWARZ (the LTI temporal channel)

`agentQQ_routeActiveCS.md` → verify `agentQQ_verify_active-cs.md`.
**VERIFIED GRADE: BOUNDS-BUT-UNSTABLE (regrade CONFIRMED).**

Modeled the X2 active dS response as a Caldeira–Leggett bath self-energy with an inverted
(negative-weight) IR gain band, on the retarded propagator D(ω)=ω²−c_χ²k²−Σ(ω). Result:

- **CS-violation is FORCED from infinitesimal gain.** CS=I2²/(I1·I3) crosses 1 from the first
  nonzero gain (e→0+). Re-derived independently by the Hamburger moment problem: CS>1 ⟺ det H<0
  (H=[[I1,I2],[I2,I3]]) ⟺ the inverse-moment sequence has no positive representing measure ⟺ a
  literal signed/non-passive density. PASSIVE wall re-confirmed (40000 random positive baths,
  max CS=1.000000 — the agentPP Herglotz wall). The non-passive sign agentPP requires IS met.
- **But the fold-delivering regime is UNSTABLE.** Threshold ordering on the SAME object:
  **e_CS→0+ < e_inst~O(γ) ≪ e_fold~O(1).** The stable CS>1 window (0<e<e_inst) is too weak to bend
  the physical acoustic branch (ω²(k) monotone, ZERO v_g²<0 fold points, Im ω<0 throughout — CS>1
  there owes itself to the signed *moment representation*, not to any in-band gain). Any gain strong
  enough to fold opens a UHP pole of the retarded Green function (exponentially growing mode),
  confirmed by two orthogonal verifier methods (Nyquist winding=2 AND direct Newton root-find), and
  WORSE for the sharp finite-Q resonance the fold needs (e_inst~O(γ), sharper ⇒ unstable earlier).
- **X2 tension is TIGHT.** The genuine in-band active response (Im Σ>0 = Im μ̂<0, a direct
  finite-band violation of X2 Eq. X-7) onsets at the SAME e~e_inst as the UHP instability: the
  finite-band gain that makes the medium genuinely active is the one that opens the UHP pole.

**Verdict: the LTI active channel BOUNDS the IR k⁶ moment but cannot STABLY FOLD the physical
branch.** The genuinely-new input it names — a NONLINEAR-SATURATED gain (laser-above-threshold
limit cycle) or a structured/non-Markovian gain whose Kramers–Kronig partner cancels the UHP
displacement, something OUTSIDE the LTI Caldeira–Leggett class — is NOT yet banked. The LTI active
channel is exhausted.

## ROUTE 2 — EDGE-PINNING + the X2 passivity tension (the spatial-window channel)

`agentQQ_routeEdge.md` → verify (in the synthesis block).
**VERIFIED GRADE: PARTIAL-NEEDS-MORE (regrade CONFIRMED).**

Worked the structural identity and the existence of a consistent window on the spatial roton
dispersion ω²(k)=c_χ²k²+σ4 k⁴+σ6 k⁶ (σ4<0 the dS-bath-forced bend, banked 851e7649):

- **THE IDENTITY (favorable).** "Bound the fold" = σ6>0 = CS violated = negative spectral weight in
  a band = Im μ̂<0 in a band = the SAME active response X2 independently forces from deep-MOND. The
  fold-bounding demand and the X2 active demand are ONE sign of ONE spectral weight — PP and X2 ask
  for the same thing. Confirmed three ways (Parts 1, 3, 9); 50000/50000 random positive spectra obey
  CS (re-confirms PP).
- **THE CONSISTENT WINDOW EXISTS.** No-ghost ⟺ σ6>σ6*≡σ4²/(4c_χ²). For σ6>σ6* there is a real
  inflection k* with ω²(k*)>0, no ghost, retarded poles in the LHP (causal), group velocity real.
  At threshold the inflection cubic factorizes to a TRIPLE root at u*=−2c_χ²/σ4 coinciding EXACTLY
  with ω(k*)=0 — the inflection sits AT the soft sonic edge. **Active-enough-to-bound AND
  stable/causal coexist** in this window.
- **active ≠ anti-damped (the tension-dissolver).** A negative-RESIDUE, positive-γ Lorentzian gives
  simultaneously Im χ<0 (active), poles in LHP (g(t)~e^{−γt/2}sin, decaying), and χ(0)<χ(∞) (the X2
  inverted ordering). Passivity is broken by the spectral-weight SIGN; stability is the pole
  LOCATION. A medium can be active AND stable AND causal. X2's "non-passive" is its CONCLUSION, not
  a premise it then needs protected — no logical clash.

**But the verifier downgraded "stable" from established to possible, and the fold is NOT forced:**

- **Forced only in DIRECTION, free in MAGNITUDE.** Reaching σ6≥σ6* (the magnitude that bounds the
  fold) is NOT forced by the X2 pump structure — the smooth GH continuum gives σ6<0 (ghost side,
  the wrong sign). The floor σ6* is a codimension-1 tuning supplied only by the unbanked PEAKED dS
  QNM horizon resonance (NN's named input). So the SIGN is forced, the FOLD is not.
- **Edge-pinning PARTIAL.** k* is pinned in SCALE (k*~(c_χ/√a₀)H, bath-set) but its COINCIDENCE
  with b→c_χ requires σ6=σ6* exactly — a tuning the smooth bath fails; needs the QNM.
- **The honest identity gap.** Stability is proven on a LOSSLESS spatial roton dispersion (real, no
  Im — the He-4 roton form, not active at all); activeness is proven on a SEPARATE negative-residue
  temporal Lorentzian. The two are the same response only by ASSERTION, never derived. Worse, the
  genuine soft sonic edge (v_g=0, ω(k*)→0) exists ONLY at the marginal knife-edge σ6=σ6*; the
  in-window stability showcase σ6=0.10 has NO edge (v_g>0 everywhere). Dressed-pole stability of the
  actual active self-energy at the required magnitude is asserted from a toy, correctly deferred to
  the QNM calc.

---

## INDEPENDENT SYNTHESIS SPOT-CHECK (this memo, `/tmp/agentQQ_synth_check*.py`)

To reconcile the two verdicts I re-derived the load-bearing pieces of BOTH routes by independent
methods and confirmed they are CONSISTENT, not contradictory:

- **R2 window (LEG A,B).** Threshold σ6*=σ4²/(4c_χ²)=1/16 (sympy factorization, not numpy scan);
  at σ6* the inflection cubic factorizes to **3(u−4)³/128 — a clean triple root at u*=4** with
  ω²(k*)=0 exactly (the soft edge). Window σ6>σ6* non-empty (σ6=0.07,0.10,0.25 all give real k*,
  ω²(k*)>0, no ghost). R2 Parts 4–5 reproduced.
- **R1 instability (LEG C).** On the SAME two-delta active self-energy, CS>1 from e→0+ (e=0.001→
  CS=1.0022; e=0.10→CS=2.85, all moments positive = FORCED non-passive), and a **k-swept direct
  max-Im(ω) root-find** finds the UHP onset between **e=0.015 and e=0.018** (unstable band near
  k≈1.15), i.e. **e_inst~O(γ=0.1)** — a THIRD independent method agreeing with the verifier's
  Nyquist+Newton onset of 0.01–0.02. R1 BOUNDS-BUT-UNSTABLE reproduced.
- **The reconciliation (LEG D).** The two "stabilities" are DIFFERENT objects: R2's is gradient/ghost
  stability of a LOSSLESS branch (ω²(k)>0, real ω); R1's is temporal-pole stability of the ACTIVE
  self-energy (Im Σ≠0). My σ6=0.10 lossless example is gradient-stable but has d(ω²)/du min=+0.167
  (NO roton dip) — independently confirming the verifier's catch that the in-window showcase has no
  soft edge. The routes do not conflict: **R1 shows the LTI *temporal* realization is unstable in the
  fold regime; R2 shows a stable *spatial* roton window EXISTS; whether the dS pump lands in it
  (negative-residue gain, not negative-damping runaway, at magnitude σ6≥σ6* with k* at the edge) is
  the single unbanked input.**

Quarantine held: only signs (CS vs 1, det H, Im Σ, σ6 vs σ6*), pole/UHP counts, and
branch/window structure computed; q=1/4 / ζ̃ / (16π/3)^{1/4} never touched.

---

## OVERALL VERDICT — PARTIAL-NEEDS-MORE

**Counted at verified grades: Route 1 = BOUNDS-BUT-UNSTABLE, Route 2 = PARTIAL-NEEDS-MORE.** The two
are complementary halves of one finding, and the binding conclusion is the more informative of the
two: the active dS pump **CANNOT yet be shown to deliver the controlled fold, but it is NOT
obstructed by X2 either** — so the overall grade is **PARTIAL-NEEDS-MORE**, with the gap named
precisely.

NOT FOLD-DELIVERED: it is not CONFIRMED that the X2 pump FORCES a CS-violating response that bounds
the fold, pins k* at the edge, AND stays stable — the magnitude σ6≥σ6* is free (unbanked QNM), the
edge-coincidence is a codimension-1 tuning, and stability at the required magnitude is asserted from
a toy, not derived.

NOT OBSTRUCTED: demanding the bounded fold does NOT contradict X2's passivity structure. X2 CONCLUDES
non-passivity (it does not assume a passivity it then needs protected), and a negative-residue/
positive-γ response is active AND stable AND causal at once. The feared contradiction was a
premise/conclusion conflation. There exists a stable, causal, bath-limited window (σ6>σ6*) in which
active-enough-to-bound and stable-enough-to-be-physical coexist.

NOT BOUNDS-BUT-UNSTABLE overall: although the *LTI temporal* channel (Route 1) is bounds-but-unstable
and exhausted, that is not the whole active sector — Route 2 proves a stable *spatial* roton window
exists, so the fold and stability are NOT globally in tension; the tension is confined to the LTI
realization, which the named new input (saturated/non-Markovian gain, or the peaked QNM) is meant to
escape.

NEEDS-NEW-INPUT is the residual: the specific active-gain spectrum that lands σ6≥σ6* on the stable
(negative-residue, NOT negative-damping) branch with k* pinned at b→c_χ is FREE input not fixed by
X2/the smooth dS pump. **Named: the PEAKED dS quasinormal-mode (QNM) horizon spectral function** —
and, for the LTI-escape, a nonlinear-saturated or non-Markovian gain that holds CS>1 on the physical
branch with all retarded poles in the closed LHP. The smooth GH continuum gives σ6<0 (ghost) and
fails this; the QNM is the unbanked piece.

### PLAIN STATEMENT (mandatory)

The active dS pump can stay CONSISTENT with X2 (active ≠ unstable; a stable, causal, bath-limited
CS-violating window provably EXISTS), but it CANNOT yet be shown to DELIVER the controlled fold: the
sign of the response is forced and the fold is structurally permitted, but its magnitude (σ6≥σ6*),
its edge-coincidence (k* at b→c_χ), and the stability of the actual self-energy at that magnitude all
hinge on one named, unbanked input — the peaked dS QNM horizon resonance (with a saturated/
non-Markovian gain needed to escape the LTI instability Route 1 found).

### NEXT CALC (flag for the strongest possible verification when it returns a PASS)

Compute the dS QUASINORMAL-MODE horizon spectral function and test whether its PEAKED (non-continuum)
contribution to the khronon self-energy delivers σ6≥σ6*=σ4²/(4c_χ²) as a STABLE NEGATIVE-RESIDUE
(positive-γ, LHP-pole) gain — NOT a negative-damping runaway and NOT the smooth-continuum σ6<0 —
with the inflection k* pinned at b→c_χ. The QNM must also resolve Route 1's LTI instability (either
its finite-Q peak is structured/non-Markovian enough that its Kramers–Kronig partner keeps all
retarded poles in the LHP, or a nonlinear saturation self-limits the growing mode). PASS ⟺ generated
σ6 crosses σ6* on the stable branch with k* at the edge AND all retarded poles in the closed LHP;
THEN derive ρ(b) and check q=1/4 with γ_req downstream (quarantined). FAIL (smooth continuum σ6<0, or
the QNM realizes a negative-damping/UHP runaway) ⟺ MM/PP kill stands.

### ONE-SENTENCE LINK-5 UPDATE

Link 5's controlled-fold mechanism is now SELF-CONSISTENT-BUT-UNDELIVERED: the X2 active dS pump is
provably compatible with X2's own passivity structure and a stable bounded-fold window exists, but
the fold is bounded only in DIRECTION (sign forced), not in MAGNITUDE — delivery hinges on the single
named unbanked input, a peaked dS QNM horizon resonance landing σ6≥σ6* on the stable negative-residue
branch with k* at the sonic edge (the LTI temporal channel alone is bounds-but-unstable and exhausted).
