# agentQQ VERIFY — hostile referee of Route 1 (ACTIVE-GAIN CAUCHY-SCHWARZ): does the X2 active dS response bound the roton fold, and at what stability cost? (2026-06-13)

**Route under review.** agentQQ_routeActiveCS.md, verdict **BOUNDS-BUT-UNSTABLE**: the X2 active-gain
response (modeled as a Caldeira-Leggett bath with a negative-weight IR band) DOES violate Cauchy-Schwarz
(CS = I2^2/(I1 I3) > 1 => sigma6 > 0, IR k^6 moment bounded) from infinitesimal gain, but the gain needed for
a VISIBLE controlled fold (real v_g^2 < 0 dip on the physical acoustic branch) is far past the linear-instability
onset (a UHP pole of the retarded Green function). Threshold ordering e_CS -> 0+ < e_inst ~ O(gamma) << e_fold ~ O(1),
tightening (instability earlier) for the sharp finite-Q resonance the fold needs.

**Referee mandate.** (1) Re-derive CS-violation + stability by a DIFFERENT method. (2) PRIMARY: if the route
claimed FOLD-DELIVERED, was the fold gotten by a FORCED + STABLE active gain, or by an unforced negative weight /
an ignored instability? (Hunt ghosts.) (3) X2 self-consistency. (4) Regrade. Default skepticism.

All checks independent: scripts /tmp/agentQQ_vf1_hankel.py, vf2b.py, vf2c.py, vf3_branch.py, vf4_foldregime.py,
vf5_X2.py, vf5b.py. NO coefficient asserted (q=1/4 / zeta-tilde / (16pi/3)^(1/4) never touched — only signs,
pole counts, branch monotonicity).

---

## (1a) CS-violation, re-derived by the HANKEL / moment-problem method (not C-S by hand)

agentQQ used Cauchy-Schwarz on (I1,I2,I3) directly. Independent restatement via the Hamburger moment problem:
the inverse-moment sequence (I1,I2,I3) = (<W^-2>,<W^-4>,<W^-6>) is realizable by a POSITIVE measure iff the
Hankel matrix H = [[I1,I2],[I2,I3]] is positive-semidefinite, i.e. **det H = I1 I3 - I2^2 >= 0 <=> CS <= 1.**
So CS>1 is EXACTLY det H < 0 = the moment problem has no positive solution = the representing density must be
SIGNED (genuinely non-passive). Same wall, derived from moment theory.

- PASSIVE wall: 40000 random positive 1-5-delta baths -> **min det H = -2e-47 (= 0 to roundoff, single-delta
  saturation), max CS = 1.00000000.** The Hankel-PSD wall is the same wall agentPP/agentQQ hit. CONFIRMED.
- ACTIVE: one negative weight -e at W_g^2 = g < p (the IR-effective gain): det H < 0 (CS>1) from e -> 0+
  (e=1e-5: CS=1.00002 at g=0.5; 1.0000026 at g=0.7). **Part (a) reproduced: CS>1 from infinitesimal gain, and
  the CS-violation IS the loss of a positive representing measure (a literal non-passive / signed density).**

=> **Route part (a) — CS-violation from an active/non-passive response — CONFIRMED, by an independent (moment-
problem) method.** The "non-passivity required by agentPP's no-fold theorem is met" claim holds.

## (1b) Stability, re-derived by the NYQUIST argument principle (not root-counting)

agentQQ counted UHP zeros of D(omega) = omega^2 - c_chi^2 k^2 - Sigma(omega) by polynomial root-finding.
Independent method: the number of UHP zeros of D (= UHP poles of the retarded Green function = growing modes) =
the WINDING of D(omega) around the boundary of a large upper-half-disk (argument principle). Caldeira-Leggett
Sigma(omega) = sum_i g_i^2 omega^2/(omega^2 - nu_i^2 + i gamma_i omega) has all its OWN poles in the LHP for
gamma_i > 0 (causal linewidth), so the winding counts UHP zeros directly. Gain = flip one residue g_i^2 -> -e.

- PASSIVE reference (both g_i^2 > 0, gamma=0.1): **Nyquist winding = 0 at every k (0.2..1.5)** — 0 UHP zeros =
  STABLE. Reproduces Caldeira-Leggett / agentPP Herglotz no-instability, by a method that never solves for roots.

**Route's EXACT two-delta model (passive +1 @ nu=1, gain -e @ nu=0.7, gamma=0.1), swept on the SAME object:**

| e | CS = I2^2/(I1 I3) | max Nyquist UHP winding | status |
|---|---|---|---|
| 0.001 | 1.0022 | 0 | stable |
| 0.005 | 1.0117 | 0 | stable |
| 0.010 | 1.0247 | 0 | stable |
| 0.015 | (near onset) | 0 | stable |
| **0.020** | 1.0555 | **2** | **UNSTABLE** |
| 0.06  | 1.3085 | 2 | UNSTABLE |
| 0.10  | 2.8516 | 2 | UNSTABLE |

=> **e_CS -> 0+ (CS>1 from the first nonzero gain) STRICTLY BELOW e_inst (UHP onset between 0.01 and 0.02).
There IS a narrow stable CS>1 window (0 < e < ~0.015).** Both the route's part-(a) PASS and its narrow-stable-
window claim are reproduced, by an independent (winding-number) stability test. The unstable winding = 2 = a
conjugate pair of retarded poles crossing into the UHP (collective acoustic+gain hybrid), as the route described.

## (2) PRIMARY CHECK — was a FOLD delivered, and if so by a forced+stable gain? NO FOLD WAS DELIVERED.

The route did NOT claim FOLD-DELIVERED; it claimed BOUNDS-BUT-UNSTABLE. The referee's job is to confirm the
route did not quietly get a fold by an unforced/unstable choice. I tracked the PHYSICAL acoustic branch
omega^2(k) (Newton-traced lowest root of D) and looked for v_g^2 = d omega^2/d k^2 < 0 at finite k* (a real fold):

- **Stable CS>1 window (e = 0.005, 0.010, 0.015; all CS>1, all Nyquist-stable): the branch is STRICTLY MONOTONE,
  ZERO v_g^2<0 fold points, Im(omega) < 0 (decaying) throughout.** CS>1 bounds the *moment*; the *physical branch*
  does not bend. **CS>1 but NO visible fold.** (Reproduces route Step 4 exactly.)
- **Fold-forming regime:** cranking e to 0.02..0.34 (g=0.7,p=1): still ZERO real fold points on the physical
  branch AND winding = 2 (UNSTABLE) at every such e. In this LTI model the real fold never even forms before the
  instability eats the branch. So e_fold > e_inst is, if anything, UNDERSTATED by the route.
- **e_inst ~ O(gamma), INDEPENDENT confirmation:** bisecting the UHP onset vs linewidth gamma gives
  e_inst = 0.0048 (gamma=0.05), 0.018 (0.1), 0.061 (0.2), 0.156 (0.4) — scales ~linearly, e_inst/gamma roughly
  constant at small gamma. **Sharper (higher-Q, more fold-capable) resonance => unstable EARLIER.** Confirms the
  route's analytic claim and its "the sharpness the fold needs makes the instability arrive first" tension.
- **HOSTILE search for a stable visible fold** across gain position g in {0.4,...,0.95} and strength e in
  {0.01,...,0.3}: **NO stable fold-bearing configuration exists.** Every config that bends the branch is unstable.

=> **No fold was smuggled. The route's BOUNDS-BUT-UNSTABLE is the correct reading: the active gain bounds the IR
k^6 moment (sigma6>0) only in a window too weak to bend the physical branch; any gain strong enough to fold is
linearly unstable (UHP pole), worse for the sharp resonance the fold requires.** The CS-violating sign is FORCED
by the X2 active structure (agentPP + X2 already require non-passivity; any IR-effective gain band gives CS>1 from
e->0+); what is free is only the gain MAGNITUDE, and that is exactly where the obstruction bites.

## (3) X2 SELF-CONSISTENCY — the active response CONTRADICTS X2's own passivity premise (as it must)

X2 (agentX_sk_gate.md, Thm X2 / Eq. X-7) pins passivity as **Im mu_hat(omega) >= 0 for omega>0** (positive-real;
the dielectric ordering mu_hat(0) >= mu_hat(infty)). The medium response is mu_hat ~ -Sigma, so passive <=>
Im Sigma <= 0 (the retarded self-energy damps). I checked Im Sigma directly:

- The CS>1 / fold-delivering response REQUIRES the gain band, where the gain delta contributes Im Sigma > 0 =
  Im mu_hat < 0 = a DIRECT violation of X2's Eq. (X-7). So the fold-delivering response is NOT in X2's passive
  class — it lives in the active class X2 only forces at the SECULAR (omega -> 0) channel, now demanded in a
  FINITE band at the sonic edge k*.
- **Sharp quantitative coincidence:** the TOTAL Im Sigma first pokes positive (a genuine finite-band positive-real
  violation, gain bump clears the passive tail) at **e ~ 0.02 — coincident with e_inst (the UHP onset).** So:
  * CS>1 (the inverse-MOMENT ratio) onsets at e->0+ — driven by the IR-dominant gain delta in <W^-2m>, while the
    response is still NET passive (Im Sigma <= 0 everywhere; gain bump masked by the passive tail);
  * a genuine in-band active response (Im Sigma > 0) AND the UHP instability onset TOGETHER at e ~ e_inst.

  This is a STRONGER statement than the route's: the truly X2-passive window where CS>1 owes its CS>1 only to the
  signed *moment representation*, not to any actual in-band gain; the instant the response becomes genuinely active
  in a band (Im Sigma>0, what a real fold's anti-damping needs), it is simultaneously unstable. **X2's tension
  ("non-passive enough to bound the fold" vs "stable enough to be physical") is not just respected — it is
  tight: the same finite-band gain that makes the medium genuinely active is the one that opens the UHP pole.**

=> The route does NOT contradict X2 illegitimately; it inhabits exactly the active corner X2 points at, and the
instability it reports is the price X2's own passivity bound predicts for pushing that corner to a finite-band fold.

## (4) REGRADE — CONFIRMED. Verdict BOUNDS-BUT-UNSTABLE upheld.

Every load-bearing claim of the route was independently reproduced by a different method:

| Route claim | Independent method | Result |
|---|---|---|
| (a) active response gives CS>1 from e->0+ | Hankel-PSD / moment problem (det H<0) | CONFIRMED |
| passive wall CS<=1 | Hankel PSD, 40000 random positive baths | CONFIRMED (max CS=1.0) |
| stable narrow window 0<e<e_inst with CS>1 | Nyquist winding (argument principle) | CONFIRMED (stable to e~0.015) |
| instability at e_inst (UHP pole) | Nyquist winding = 2 | CONFIRMED (onset 0.01..0.02) |
| stable window has NO visible fold | Newton branch-trace v_g^2 | CONFIRMED (monotone, 0 fold pts) |
| e_fold >> e_inst | branch-trace + winding to e=0.34 | CONFIRMED (no real fold pre-instability) |
| e_inst ~ O(gamma), sharper=worse | bisection vs gamma | CONFIRMED (~linear) |
| no stable visible fold anywhere | hostile (g,e) grid | CONFIRMED (none found) |
| X2 self-consistency | Im Sigma / positive-real test | CONFIRMED + TIGHTENED |

**The fold was NOT delivered by an unforced or unstable choice that the route hid.** The CS-violating sign is
FORCED (X2 + agentPP require non-passivity; any IR gain band gives CS>1). The fold-delivering regime is genuinely
UNSTABLE (UHP pole, independently by winding number), and the instability arrives strictly before any visible fold
on the physical branch — confirmed even harder than the route stated (the real fold never forms pre-instability in
this LTI model). The active response is NOT stable in the fold-delivering regime.

**regrade: CONFIRMED. regraded_verdict: BOUNDS-BUT-UNSTABLE.**

**Both-ways honesty.** Framework-favorable (held up): agentPP's hard wall is genuinely a *passivity* theorem, not
an absolute one — the X2 active response DOES breach Cauchy-Schwarz and DOES bound the IR k^6 moment (sigma6>0),
with a real (if parametrically thin) stable CS>1 window. That is a real, non-trivial affirmative answer to
agentPP's open question. Hostile/equal-weight (decisive): the breach is structurally inert for the actual roton
fold — the stable CS>1 window cannot bend the physical branch (it owes CS>1 to a signed moment representation, not
to in-band gain), and the in-band gain that could bend it opens a UHP pole at the same threshold, worse for sharp
resonances. The LTI active channel BOUNDS the moment but cannot STABLY FOLD the branch.

**The genuinely-new input the route names is the right one and is NOT yet banked:** a NONLINEAR-SATURATED active
gain (limit-cycle self-limiting the growing mode, laser-above-threshold) or a structured/non-Markovian gain whose
Kramers-Kronig partner cancels the UHP displacement — something OUTSIDE the LTI Caldeira-Leggett class — must hold
CS>1 on the PHYSICAL branch (real v_g^2<0 at finite k*) with all retarded poles in the closed LHP AND k* pinned at
b->c_chi. Until that is computed, Route 1 = BOUNDS-BUT-UNSTABLE. The LTI active channel is exhausted.

**Quarantine held.** Only signs (det H / CS vs 1, Im Sigma sign), UHP pole/winding counts, and branch
monotonicity were computed. q=1/4 / zeta-tilde / (16pi/3)^(1/4) never asserted; the fold-depth coefficient is
downstream and untouched.
