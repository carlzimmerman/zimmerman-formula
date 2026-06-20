# Door-1/Door-2 SHARPENER — the Q-mode sound-speed sign-by-branch (a concrete candidate-KILL the banked work never ran)

Complements (does NOT replace) CONNECTION_MAP_AND_DOORS_2026-06-19.md (parallel scout's 6-door note).
Adds one runnable result + verifies the Trombetta@CEICO connection. Both-ways + quarantine held.

## Verified connection (NEW, confirmed this session)
Leonardo G. Trombetta — author of the DECISIVE IR-positivity condition for spontaneously-broken-Lorentz EFTs
(2412.19745, "IR Bounds...", v3 Apr 2026, condition v^2 <= c_s^2) — IS at CEICO Prague (Institute of Physics,
Czech Academy of Sciences), the framework's HOME institute (Skordis director; Vikman, Saltas, Calderon there).
So the exact theorem that adjudicates GAP-1's positivity is written by the framework's own home cluster. This is
a live, direct connection, not a literature coincidence. (LinkedIn + ceico.cz/team/postdocs/leonardo-trombetta +
INSPIRE inst 2892200.)

## The new computational hook for Door 1 / Door 2 (sympy, ran clean this session)
The Q-mode sound speed for the framework's K(Q)=mu^2(Q-1)^2, computed as the standard k-essence
c_s^2 = K'/(K' + 2Q K''), with K'=2mu^2(Q-1), K''=2mu^2, Q=1+dQ:

    c_s^2(dQ) = dQ / (3 dQ + 2)        [sympy-exact, /tmp/door_scoping_check.py]
    leading small-dQ:  c_s^2 ~ dQ/2

KEY SIGN RESULT (NOT in the banked GHOST_CONDENSATE work, which computed only w, never c_s^2 by branch):
    c_s^2 > 0  for dQ > 0  (Q > 1)   [e.g. dQ=0.1 -> c_s^2 = 1/23 > 0]
    c_s^2 < 0  for dQ < 0  (Q < 1)   [e.g. dQ=-0.1 -> c_s^2 = -1/17 < 0  = GRADIENT-UNSTABLE]

WHY THIS IS A CANDIDATE KILL (sharpens both Door 1 and Door 2):
- The cold-dust mode the framework's "dark matter" needs is the OFF-MINIMUM displacement, amplitude I0
  (shift charge), with dQ = I0/(2 a^3 mu^2). The SIGN of I0 sets which branch the dust sits on.
- If the physically-required dust displacement is on the Q<1 (dQ<0) branch, the dust mode has c_s^2 < 0 =
  a CLASSICAL GRADIENT INSTABILITY at the linear level — exactly the pathology positivity/causality is
  supposed to forbid. The framework would then need dS-Hubble-friction to over-damp it (Door 3), OR be
  restricted to the dQ>0 branch (a sign constraint on I0 that the banked free-I0 treatment never imposed).
- Serra-Trombetta (2412.19745, v^2 <= c_s^2): a NEGATIVE c_s^2 has no real gapless speed for the gapped
  partner to be slower than -> the inequality is ill-posed on the unstable branch, i.e. that branch is
  excluded by the IR bound. So the door's PASS region is, at minimum, dQ>0 (Q>1) only.

BOTH-WAYS (honest):
- This does NOT by itself kill the framework: ACLM ghost condensates ROUTINELY have a wrong-sign gradient
  cured by the k^4/M^2 higher-derivative term and by Hubble friction on dS (banked Jeans-cured-by-dS). The
  c_s^2<0 here is the SAME ghost-condensate gradient term, and the framework's own dS background is exactly
  what stabilizes it. So the likely net is: the dust branch is dS-overdamped (PASS), with a real CONSTRAINT
  that the displacement sign / I0 lands where friction wins (Door 3 quantifies this).
- But it converts Door 1 from "scout says PERMISSIVE in principle" into a SHARP, runnable sign test with a
  definite candidate-KILL (the Q<1 branch) — which is the difference between a reading note and a door.
- Quarantine: nothing here derives I0; it CONSTRAINS its sign/branch. a0/Z/kappa untouched.

## What to actually run (Door 1, ready-now, ~30 lines sympy+numpy)
1. c_s^2(dQ) = dQ/(3dQ+2)  [done above; bank the sign-by-branch].
2. Determine the dust displacement sign from the AeST/Scherrer first integral a^3 K'(Q)=I0 and the requirement
   rho_dust>0: solve for the sign of dQ given rho_dust = 2 I0 Q0/a^3 > 0 -> sign(I0) fixes sign(dQ). Check
   whether that forced sign is the c_s^2>0 (Q>1) or c_s^2<0 (Q<1) branch.
3. If c_s^2<0 on the forced branch: solve the dS-damped mode pi'' + 3H pidot + (c_s^2 k^2 + k^4/M^2) pi = 0
   (Door 3) and find k_crit where 3H friction beats the |c_s^2| k^2 growth. Output: PASS (k_crit beyond all
   observable k) or a real instability window.
4. Serra-Trombetta v^2 <= c_s^2: on the PASS branch, take the gapped AeST partner (mass mu) and verify its
   group velocity stays below the gapless c_s. Output: the allowed {mu, M, I0-sign} region.

PASS = the framework's dust sits on the c_s^2>=0 branch (or is dS-overdamped) AND v_gapped<=c_gapless => the
postulated P(X) clears the home-institute's own IR-positivity theorem (real win). KILL/CONSTRAINT = the forced
dust branch is c_s^2<0 and NOT dS-overdamped at some observable k => a new exclusion on I0's sign/magnitude,
as valuable as a bridge. Either way: a NUMBER + a definite verdict, runnable now.
