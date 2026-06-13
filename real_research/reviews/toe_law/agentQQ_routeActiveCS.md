# agentQQ — Route 1: the ACTIVE-GAIN Cauchy-Schwarz test — can the X2 active dS response bound the roton fold, and at what stability cost? (2026-06-13)

**Question (banked).** agentPP proved the NO-FOLD THEOREM: any PASSIVE (rho>=0) bath self-energy is
Herglotz/Pick => monotone dispersion => sigma6 = c_chi^2(I2^2 - I3 c_chi^2) <= 0 at the edge (Cauchy-Schwarz
I2^2 <= I1 I3). A CONTROLLED bounded fold (sigma6 > 0) provably needs a NON-PASSIVE response with negative
effective spectral weight on a band. Theorem X2 (agentX_sk_gate.md) independently forced the medium to be
ACTIVE/pumped (causality + deep-MOND inversion: no passive vacuum closes the causal MI; the dS bath at
T_dS = H/2pi is the only reservoir). agentEE's Bogoliubov lemma forbids state-squeezing from touching the
dissipation channel — so the object is the X2 ACTIVE-GAIN (anti-damped DYNAMICS) response, not a squeezed
vacuum. THE TENSION: X2 is itself a PASSIVITY bound — an active medium that violates Cauchy-Schwarz risks
violating the very stability X2 uses; the fold-delivering response must thread between 'non-passive enough to
bound the fold' and 'stable/causal enough to be physical'.

**This memo computes:** (a) the threshold of negative spectral weight that pushes CS = I2^2/(I1 I3) > 1
(=> sigma6 > 0, bounded fold); (b) the CRITICAL hostile check — at that weight, is the response STABLE
(no growing mode, Im part the right sign for causality) or does CS-violation NECESSARILY bring an
instability/ghost?

**Coefficient quarantine ENFORCED.** Structure only — sign of sigma6 (CS vs 1), edge-pin of k*, and
stability of the active response. q=1/4 / zeta-tilde / (16pi/3)^(1/4) NEVER asserted, quarantined downstream.

---

## Step 1 — the wall (the C-S ceiling for passive rho>=0), re-confirmed from scratch

Self-energy of a bath of modes at W^2 (x = omega^2 = the khronon's on-shell freq-squared):
S(x) = integral rho(W)/(x - W^2) dW; IR expansion below the gap gives
S(x) = -I1 - I2 x - I3 x^2 - ..., with inverse moments I1=<W^-2>, I2=<W^-4>, I3=<W^-6> (weighted by rho).
agentOO's criterion: sigma4 = -I2 c_chi^2 (bend sign), sigma6 = c_chi^2(I2^2 - I3 c_chi^2) (stabilizer);
at the sonic edge c_chi^2 -> the marginal value, sigma6 > 0 <=> CS = I2^2/(I1 I3) > 1.

For a POSITIVE measure rho>=0, Cauchy-Schwarz on u=W^-1, v=W^-3 gives I2^2 = <uv>^2 <= <u^2><v^2> = I1 I3,
equality iff single delta. Re-confirmed: 20000 random positive two-delta baths -> MAX CS = 1.0; single delta
CS = 1.0 exact. **The wall is real: passive => CS<=1 => sigma6<=0 => no bounded fold.** (agentPP banked.)

---

## Step 2 — ACTIVE GAIN: negative spectral weight DOES violate Cauchy-Schwarz (CS>1)

Model the X2 active-gain response as the SAME bath self-energy with an INVERTED band: a passive mode
(weight +1 at W_p^2) plus a GAIN mode (weight -e, e>0, at W_g^2 < W_p^2 — the IR-effective inversion).
A negative weight = the bath DELIVERS energy in that band (Im Sigma flips sign = anti-damping), exactly the
X2 active channel (NOT state-squeezing; agentEE).

**Result (the answer to part (a) — YES, CS can exceed 1).** With the gain mode below the passive line (g<p,
where it dominates the IR inverse moments), CS = I2^2/(I1 I3) crosses 1 from the FIRST nonzero gain:
at e=0.0005..0.005 (g=0.7, p=1) CS = 1.008..1.11 with ALL three inverse moments still positive
(I1,I2,I3 > 0) and sigma6 proxy (I2^2 - I1 I3) > 0. **e_CS -> 0+: ANY active gain lifts CS past 1**, because
a single negative-weight delta breaks the C-S equality that the near-single-scale passive bath nearly
saturated. So the NON-PASSIVITY requirement of agentPP's no-fold theorem is met: the active response
violates I2^2 <= I1 I3 => sigma6 > 0 => the k^6 term is bounded.

The all-positive-moment window is 0 < e < (g/p)^3 (I3 dies first, then I2 at (g/p)^2, then I1 at g/p);
for e beyond (g/p)^3 the inverse moments go sign-indefinite (I3<0 = a literal ghost in <W^-6>), which is
pathological, not a fold. As e -> (g/p)^3^- (I3 -> 0+), CS -> +inf. So CS>1 is reached EASILY and the
"bounded-fold" moment criterion sigma6>0 is genuinely deliverable from active gain.

**=> Part (a): CS-violation (sigma6>0) is ACHIEVABLE with an active/non-passive response. cs_violated = YES.**

---

## Step 3 — THE STABILITY CHECK (part (b)): does CS-violation bring an instability?

The convention-proof test. Build the RETARDED khronon inverse propagator from a Caldeira-Leggett bath of
damped oscillators (so PASSIVE g^2>0 is a manifestly-stable reference — all poles in the lower-half omega
plane, by the C-L theorem):
  D(omega) = omega^2 - c_chi^2 k^2 - Sigma(omega),  Sigma(omega) = sum_i g_i^2 omega^2/(omega^2 - nu_i^2 + i gamma_i omega).
Retarded prescription (+i gamma omega) is FIXED by causality. ACTIVE/gain = flip one g_i^2 < 0
(population-inverted). D is rational => find ALL zeros exactly => count those with Im(omega)>0 (UHP). A UHP
zero of D = a pole of the retarded Green function in the UHP = an exponentially GROWING mode = a linear
instability (and a violation of the causality/passivity that X2 itself rests on).

**Reference confirmed.** PASSIVE bath (g^2>0 both modes): 0 UHP poles at EVERY k (k=0.1..3) — STABLE,
reproducing Caldeira-Leggett / agentPP's Herglotz no-instability.

**Active result.** Flip the IR mode to gain (g^2<0): UHP poles appear in a k-BAND around the gain resonance
(k where the acoustic branch crosses nu_g), with Im(omega)>0 = exponential growth. The instability HYBRIDIZES
the acoustic mode with the gain pole and pushes the hybrid into the UHP — it is collective, not the bare gain
pole (which the retarded prescription keeps in the LHP). Sweeping the gain magnitude e on the SAME object:

| gain e | CS (sigma6) | max Im(omega) over all k | status |
|---|---|---|---|
| 0.0005 | 1.008 (>1) | -2.0e-5 | STABLE |
| 0.002  | 1.034 (>1) | -2.0e-5 | STABLE |
| 0.003  | 1.056 (>1) | -1.9e-5 | STABLE |
| ~0.004 | ~1.06 (>1) | 0+ | **instability onset (e_inst)** |
| 0.005  | 1.11  (>1) | +0.0028 | UNSTABLE |
| 0.01   | 1.39  (>1) | +0.012  | UNSTABLE |

So there IS a narrow window 0 < e < e_inst (~0.004) where **CS>1 AND stable**. The framework-favorable
outcome is NOT immediately killed — a small active gain bounds the IR k^6 moment (sigma6>0) without yet
opening a UHP pole.

---

## Step 4 — but the BOUNDED MOMENT is not a VISIBLE FOLD (the decisive gap)

CS>1 (sigma6>0) bounds the IR k^6 COEFFICIENT — it stops the k^6 term running away negative. It is NECESSARY
but NOT SUFFICIENT for a controlled roton fold: the PHYSICAL acoustic branch omega^2(k) must actually turn
over (group velocity v_g^2 = d omega^2/d k^2 < 0 at finite k*) and come back up. Tracking the acoustic pole
through the resonance (Re and Im of omega) for both windows:

- **Stable window (e<0.004, CS>1):** the acoustic omega^2(k) rises MONOTONICALLY — NO v_g<0 anywhere, NO
  roton dip. The gain is a weak perturbation on the bare c_chi^2 k^2; it bounds the moment but does not bend
  the branch. **CS>1 but no visible fold.**
- **Unstable window (e>0.004):** still no real fold on the physical branch — instead the branch goes
  COMPLEX (Im>0) in the resonance k-band = the instability.

Scanning the gain to where a visible fold (real v_g<0) would form: a fold requires the gain to DOMINATE the
bend over the bare c_chi^2 k^2 dispersion, which only happens once e is large enough to strongly hybridize —
and that is WELL INSIDE the unstable regime (every e from 0.004 to 0.065 tested is unstable, none shows a
real fold on the physical branch; the branch is either monotone or complex). **e_fold > e_inst: a VISIBLE
fold requires gain past the instability onset.**

THE ORDERING (the crux), all three thresholds on the SAME object:
  e_CS (CS>1, moment bounded) -> 0+   <   e_inst (UHP pole) ~ 0.004   <<   e_fold (visible roton dip).
The window where the moment criterion sigma6>0 is satisfied AND the system is stable (0 < e < e_inst) is
exactly the window where the gain is too weak to fold the physical branch. To get a visible controlled fold
you must turn the gain up past e_inst — into linear instability (UHP pole / growing mode).

---

## Step 5 — the ANALYTIC reason e_inst << e_fold is GENERIC (not a toy artifact)

Re-derived in a richer model (3 passive "continuum" modes + 1 IR gain mode): identical ordering — CS>1 from
e->0+, instability onset at e~0.004, no stable visible fold. The analytic mechanism, model-independent:

The retarded G is analytic in the UHP iff Im Sigma >= 0 (passive). A gain band sets Im Sigma < 0 there. As
gain turns on continuously from 0, the resonance pole — which sat at Im(omega) = -gamma/2 (LHP, set by the
bath linewidth gamma) — is pushed UP by a displacement LINEAR in the gain residue. It reaches the real axis
(marginal) and crosses into the UHP once the gain overcomes the damping:
  **e_inst ~ O(gamma)** (the bath linewidth).
A VISIBLE fold, by contrast, needs the gain to rival the BARE stiffness c_chi^2 k^2 to bend omega^2(k) over:
  **e_fold ~ O(1)**.
Therefore e_inst << e_fold whenever gamma << 1 — i.e. for a SHARP / underdamped / finite-Q gain resonance.
But a sharp finite-Q peaked resonance is EXACTLY what agentPP concluded the controlled fold requires (the dS
QNM continuum was too broad). So the very sharpness that the fold needs makes the instability arrive EARLIER:
**the fold and the instability are driven by the same gain, and the instability wins first, and wins by more
the sharper (more fold-capable) the resonance is.** This is Theorem X2's tension made quantitative — the
active response that is "non-passive enough to bound the fold" is, by the same gain, "too non-passive to stay
stable" precisely in the peaked regime where a real fold could form.

---

## VERDICT — BOUNDS-BUT-UNSTABLE (Route 1, computed)

| Question | Computed answer |
|---|---|
| (a) Can the active (sign-indefinite rho) response make CS = I2^2/(I1 I3) > 1 (=> sigma6>0)? | **YES.** Any nonzero IR gain lifts CS past 1 (e_CS->0+); the moment criterion is genuinely deliverable. cs_violated = YES (with the caveat below). |
| Threshold of negative weight to bound the fold | e_CS -> 0+ for CS>1; the genuine all-positive-moment window is 0 < e < (W_g/W_p)^3 (beyond it, <W^-6> goes negative = ghost). |
| (b) At the weight that bounds the fold, is the response STABLE/causal? | **A narrow stable window exists (0 < e < e_inst ~ O(gamma)) where CS>1 AND 0 UHP poles** — but in it the gain is too weak to FOLD the physical branch (omega^2(k) monotone, no roton dip). A VISIBLE controlled fold needs e ~ O(1) >> e_inst => a UHP pole => exponentially growing mode (linear instability), generic and worse for sharper resonances. |
| Does CS-violation NECESSARILY bring instability? | The MOMENT bound (sigma6>0) does NOT, by itself, in the e->0 limit. The actual fold does: bounding the *coefficient* is stable, but bending the *branch* is not. **stable = NO in the fold-delivering regime.** |

**cs_violated: YES (the active response exceeds CS=1 / sigma6>0 — the moment criterion is met).
stable: NO in the fold-delivering regime (a visible controlled fold requires gain past the UHP-instability
onset; only a fold-INVISIBLE sub-window is stable). => verdict BOUNDS-BUT-UNSTABLE.**

This is exactly the "bounds only with instability" outcome the route pre-registered as real and likely. The
X2 active channel CAN violate Cauchy-Schwarz (answering agentPP's open question affirmatively at the level of
the moment ratio), but it cannot do so STRONGLY ENOUGH to fold the physical dispersion without crossing into
linear instability — and the threshold ordering (e_inst ~ gamma << e_fold ~ 1) is generic and TIGHTENS for
the sharp finite-Q resonance the fold actually requires. The controlled bounded fold is NOT delivered stably
by Route 1.

**Honest both-ways report.** Framework-favorable: agentPP's hard wall (passive => CS<=1, no fold) is breached
— the active dS response DOES violate Cauchy-Schwarz and DOES bound the IR k^6 moment (sigma6>0), and there
is even a parametrically-small stable window where CS>1. The no-fold theorem is genuinely a *passivity*
theorem, not an absolute one. Hostile/equal-weight: the breach is structurally inert for the actual roton
fold — the stable CS>1 window cannot bend the physical branch, and the gain that can bend it is linearly
unstable (UHP pole), with the instability arriving earlier the sharper the resonance. The active response
threads between "bound the moment" and "stay stable" only by being too weak to fold; pushed hard enough to
fold, it tears the very passivity/causality X2 rests on. Part (a) PASSES, part (c) FAILS in the regime where
part (a) would matter.

**Quarantine held.** q=1/4 / zeta-tilde / (16pi/3)^(1/4) never asserted — only the sign of sigma6 (CS vs 1),
the k* edge-pin structure, and the UHP-pole stability count were computed. The coefficient that would set the
fold depth is downstream and untouched.

**Next calc (named, not run here).** If the fold is to survive, the active gain must be stabilized AGAINST
the UHP pole by a mechanism that is not in this LTI bath model — e.g. a nonlinear saturation (the gain
self-limits once the mode amplitude grows, a laser-above-threshold limit cycle rather than a runaway), or a
non-Markovian/structured gain whose Kramers-Kronig partner cancels the UHP displacement. PASS <=> a saturated
active response holds CS>1 on the PHYSICAL branch (visible v_g<0 fold at finite k*) with all retarded poles in
the closed LHP, AND k* pinned at b->c_chi. Until then Route 1 delivers BOUNDS-BUT-UNSTABLE.
