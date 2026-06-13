# agentOO — HOSTILE VERIFICATION of route loop-direct (the dS-bath one-loop self-energy sigma4 sign)

**Charge.** (1) Independently re-derive the sigma4 SIGN by a different method/regularization. (2) Was the
bending sign CHERRY-PICKED — did the route pick a coupling/cutoff pre-shaped for sigma4<0? Test the OTHER
admissible couplings; if the sign flips with coupling, the honest verdict is FOLD-POSSIBLE-COUPLING-DEPENDENT,
not FOLD-GENERATED. (3) If the route found convex, try hard to steelman a bending coupling. (4) Regrade.
Default skepticism: a fold that closes the framework's deepest gap is assumed cherry-picked until shown forced.

Route's claim (agentOO_routeLoop.md): sigma4 is COUPLING-DEPENDENT — scalar trilinear g chi phi phi → sigma4>0
(convex/stiffen) at all r; derivative bath couplings (deriv2/timelike/grad2) → sigma4<0 (bend) but ONLY for
c_chi>c_b; verdict FOLD-POSSIBLE-COUPLING-DEPENDENT, FREE (not forced by the GH spectrum).

---

## V0 — reproduce the route (sanity)

Ran agentOO_c10_cauchy.py and agentOO_c13_deriv.py verbatim. Both reproduce:
- C10 scalar: s4>0 ("POS stiff") at every r in [0.5,3.0]. BUT rms/scale = 8-21%, and s4>0 fights a huge
  s6<0 (e.g. r=0.5: s4=+6.9e2, s6=-1.0e4). A 4-param lstsq on 9 points at 12% residual where s4,s6 have
  opposite signs and big magnitudes is NOT a clean coefficient — the reported sign rests on a noisy fit.
- C13 deriv: "BEND" appears for deriv2/timelike/grad2 at r=2 ONLY, but the magnitudes are 1e-6..1e-5 and
  the estimator is np.median(residuals[-4:]) after a 2-point (ks[:2]) lstsq. Fragile — possible fit noise.

Two concrete worries to kill before trusting either sign:
  (W1) Is the scalar s4>0 robust, or a fit artifact of the thermal omega/k small-k non-analyticity?
  (W2) Is the deriv2 r=2 BEND a genuine analytic sign, or sub-1e-6 noise from a hand-rolled residual median?

Independent method below: build a CLEAN, high-resolution ReSigma(k), subtract s0+s2 k^2 by a STABLE
low-k fit, and read the curvature sign from the genuine 4th-difference (the k^4 coefficient) — no s4/s6
tug-of-war, plus an analytic small-k cross-check.

---

## V1 — independent s4 sign by R/k^4 window-plateau (NOT a 4-param lstsq) [agentOO_verify_v1.py]

Method: build ReSigma(k) on a small-k window, subtract s0+s2 k^2 from the two smallest k (exact 2pt fit),
then R(k)/k^4 should plateau to s4 (intercept) with s6 the slope vs k^2. This SEPARATES s4 from s6 — no
opposite-sign tug-of-war. A genuinely different extraction from the route's C10 lstsq and C13 residual-median.

RESULT — the route's QUALITATIVE picture is CONFIRMED and is in fact cleaner here:
- scalar (g chi phi phi): s4 > 0 (POS/stiffen) at EVERY r in [0.5,3.0], clean R/k^4 plateaus. FIREWALL holds.
- deriv2/timelike/grad2: s4 > 0 (STIFF) for c_chi<c_b (r=0.5,0.7,1.3) and s4 < 0 (BEND) for c_chi>c_b (r=2,3).
  The crossover is near r~1.3-1.5 (r=1.3 still stiff, r=2 bends) — matches route's C14.
- deriv_ext: bends already at r=1.3.

So the route did NOT cherry-pick a single operator/cutoff: the sign is GENUINELY coupling+regime dependent,
reproduced by an independent extractor. The scalar firewall is real; the derivative-coupling bend is real.

**BUT — a discrepancy with the route on s6 (load-bearing for 'bounded fold').** The route (C16) claimed
deriv2 r=2 gives s6 = +1.09e-2 > 0 (the +k^6 STABILIZER, bounded roton fold). My clean extraction gives,
for the BEND cases, s6 < 0:  deriv2 r=2 s6=-0.10; timelike r=2 s6=-1.9; grad2 r=2 s6=-0.29; deriv2 r=3
s6=-0.057. A NEGATIVE s6 means NO stabilizer — the induced correction is concave AND runs away (sigma4<0,
sigma6<0), an UNBOUNDED bend, not a bounded roton fold. Investigating s6 next (V2).

## V2 — s6 sign by EXACT 4-point collocation over disjoint windows [agentOO_verify_v2_s6.py]

My V1 R/k^4 lstsq for s6 was itself contaminated (it absorbed the s6 slope across a too-wide window).
Cleaner method: solve the 4x4 collocation ReSigma=s0+s2k^2+s4k^4+s6k^6 EXACTLY on 4 points, over five
disjoint windows. RESULT:
- s4 < 0 (BEND) ROBUST across ALL windows for deriv2/timelike/grad2 at r>=2. Confirmed.
- s6 > 0 (STABILIZER) ROBUST across all reasonable windows; flips negative ONLY in the over-resolved
  'tiny' window (k<=0.08) for deriv2 r=2 — EXACTLY the degradation the route honestly flagged in C17.
- deriv2 r=2 route(C16) window: s4=-2.05e-3, s6=+1.25e-2 — REPRODUCES route's C16 (s4=-1.98e-3, s6=+1.09e-2).

**I WITHDRAW my V1 s6<0 worry — it was my extractor's artifact, not the route's. The route's C16 bounded
roton-fold pattern (sigma4<0 AND sigma6>0) IS independently reproduced by exact collocation, and the route
was HONEST about the tiny-window s6 degradation.** Net: the route's central numerical claims survive a
hostile independent re-extraction.

## V3 — DIFFERENT REGULARIZATION + cherry-pick test [agentOO_verify_v3_reg.py]

(A) Scalar sign by a DIFFERENT regularization: Lorentzian i*eps denominators (Re 1/(x-u0+i eps)) and
eps->0, instead of the route's Cauchy-PV weight. Result at r=2: s4 = +1.16e3 (eps=0.02) -> +6.6e2 (eps=0.002),
POS(stiff) at every eps, converging toward the PV value (~6.9e2). The scalar CONVEX sign is
REGULARIZATION-INDEPENDENT. The route's PV-vs-naive-quad methodology fix was correct and the firewall is real.

(B) CHERRY-PICK test — broad contraction-angle scan of the squared-derivative family
V=(cos(theta) Wq u + sin(theta) qdotcb2)^2, theta in [0,pi], 13 angles, exact-collocation s4:
  - r=0.7 (sub-luminal c_chi<c_b): 9 of 13 STIFFEN, only the 4 extreme angles bend. Predominantly convex.
  - r=2.0 (super-luminal c_chi>c_b): 12 of 13 BEND. The bend is the GENERIC outcome for a derivative
    operator once c_chi>c_b — NOT a hand-tuned single contraction.
=> The bend at r>1 is NOT cherry-picked: it is generic across the operator family at that speed ratio.
   But the SIGN flips with the speed ratio r AND with the operator class (scalar convex vs derivative bend).
   So sigma4 is GENUINELY coupling+regime dependent, NOT forced by the GH spectrum.

## V4 — the FORCED piece (cross-check of route's honesty)
int_0^inf q n_B(q) dq = +0.0417 > 0, and n_B(W)>0 for all W>0. So the GH Planck spectrum FORCES
m_th^2 > 0 — a positive thermal mass = a GAP, the OPPOSITE of what a gapless roton fold wants. The one
thing the spectrum forces works AGAINST the mechanism. Route's honesty point confirmed.

---

## REGRADE

**recompute_agrees: YES.** Every load-bearing claim independently reproduced by a different extractor and a
different regularization:
- scalar g chi phi phi -> sigma4 > 0 (CONVEX/firewall) at all r, regularization-independent (PV and
  Lorentzian-eps both POS). The MM/NN firewall is reproduced from the explicit one-loop self-energy.
- derivative bath couplings (deriv2/timelike/grad2) -> sigma4 < 0 (BEND) for c_chi>c_b, sigma4 > 0 for
  c_chi<c_b; crossover r~1.3-1.5. Reproduced.
- the bounded-fold pattern sigma4<0 AND sigma6>0 (route C16, deriv2 r=2) -> reproduced by exact collocation
  (s4=-2.05e-3, s6=+1.25e-2 vs route -1.98e-3,+1.09e-2); s6>0 robust except the over-resolved tiny window,
  which the route honestly flagged.
- forced piece m_th^2>0 (gap, wrong sign for the fold) -> confirmed.

**sign_robust: PARTIALLY ROBUST / NOT CHERRY-PICKED, but NOT FORCED.** The sigma4 sign is robust to
regularization (PV = Lorentz-eps) and robust within a regime (the bend is GENERIC, 12/13 angles, for any
super-luminal derivative coupling — the route did NOT fine-tune a single contraction to manufacture it).
BUT the sign is NOT robust to the two FREE choices the route named: it flips with (i) the operator class
(relevant scalar -> convex; derivative -> can bend) and (ii) the speed ratio r=c_chi/c_b (bend needs
c_chi>c_b). Neither is a consequence of T_dS=H/2pi. The route did NOT assume the bending it wanted: it
reported the scalar (most-relevant) operator as CONVEX (firewall) and explicitly stated the bend is a
selected derivative+super-luminal choice. The framework-favorable reading (EE STEP 1 c_chi^2>>1 lands the
khronon naturally super-luminal) is stated as 'reachable in the natural regime,' NOT as 'forced' — honest.

**regrade: CONFIRMED. regraded_verdict: FOLD-POSSIBLE-COUPLING-DEPENDENT.**
The route's verdict stands under hostile independent recomputation. The dS bath does NOT FORCE the roton
fold (so not FOLD-GENERATED): the single most-relevant operator is convex and the only spectrum-forced
contribution is a gap working against the fold. But the bending is genuinely REACHABLE — generic, not
cherry-picked, for an admissible derivative coupling in the super-luminal regime the framework's own EE
STEP 1 naturally occupies — so it is not killed either (not CONVEX-NO-FOLD). The two named free choices
(derivative operator + c_chi>c_b) are strict, falsifiable progress over MM's open-ended NEEDS-NEW-INPUT,
but short of forced. q=1/4 / edge-coincidence / Ai(-w) side left OPEN and downstream (quarantine intact).
