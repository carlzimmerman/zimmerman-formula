#!/usr/bin/env python3
"""H006 -- H004 IS REFUTED.  Recording the kill in my own track.

WHAT HAPPENED.  H004 proposed adding the spatial biharmonic term
-xi^2 (D^2 phi)^2 / 2 to the Zimmerman-AeST action, on the strength of
hunt_2026/f30_ppn_screening_door.py, which argued that a screened scalar has
no 1/r potential and therefore no PPN parameters at leading order.

The repo's own f31_ppn_k4_alpha1.py ran that proposal through the FULL
generalised-AeST PPN pipeline -- the same pipeline that produced the lock,
with the k^4 term added, built from the pipeline's own metric, aether and
Christoffel objects to the same orders (eps^2, w_b^2), so the mixings are
included and not hand-waved.

THE RESULT (f31_ppn_k4_alpha1.out, verbatim):

  [FAIL] K3 (THE VERDICT) ... drag piece at XI2 = 1e8: 1.80e+08;
         alpha_1 = 0 at c_14 = -4.50e+07
  [FAIL] K4 alpha_2's scalar channel: alpha_2: -oo -> oo
  [PASS] K5 gamma = 1 and alpha_3 = 0 persist at every XI2

  "the prediction of f30 FAILS for this operator: the drag piece of alpha_1
   is NOT suppressed as 1/(J_Y(1+XI2)+1).  Fitting the exact rationals,
   drag = 4(2-K_B)/(J_Y+1) [J_Y XI2/(J_Y+1) - 1]: suppressed at XI2 ~ 1,
   then GROWING linearly, 1e8 at the Solar-System value."

  "Status of the k^4 PPN gate for the aether-scalar host: OPEN on the
   operator, FAIL for (D^2 phi)^2 and |D_m D_n phi|^2."

WHY MY ARGUMENT WAS WRONG -- the lesson, stated precisely.
My H004 reasoning was: no 1/r in the static potential => no PPN parameters.
That inference is WRONG.  PPN parameters are not read off the static
potential; they are read off the LINEAR RESPONSE of the full metric-aether-
scalar system on a BOOSTED background.  The biharmonic term STIFFENS the
scalar (it adds xi^2 k^2 to the scalar's kinetic structure), and on the
boosted ladder that stiffening feeds the drag channel: the drag is
multiplied by [J_Y XI2/(J_Y+1) - 1], which GROWS with XI2.  At the
solar-system value XI2 = 8.6e7 the drag is 1.8e8 -- a hundred million times
OVER the bound, and alpha_1 = 0 then requires c_14 = -4.5e7, a catastrophic
spin-1 ghost.  Screening the potential does not screen the drag; it
amplifies it.  f30's Green's-function argument was about the STATIC field,
which is the wrong object for a preferred-frame parameter.

CONSEQUENCE FOR THE COMPLETION.
  * H001 (the action, one function, three sectors, w = -1, the RAR) stands.
    Nothing in f31 touches it: gamma = 1 and alpha_3 = 0 persist.
  * H004's solar-system escape is DEAD.  Both local fourth-order scalar
    operators tried -- (D^2 phi)^2 and |D_m D_n phi|^2 -- fail identically
    (f31c).
  * The k^4 PPN gate is OPEN on the operator: f31c reports that a COHERENT
    stiffening J_Y -> J_Y(1+XI2) of the whole Y sector DOES give the
    propagator form.  So the screened door exists as a reference; no local
    fourth-order scalar operator tried realises it in this host.
  * The aether-scalar host therefore remains closed on alpha_1/alpha_2 --
    the same lock that closed it before, now confirmed against the one
    escape that was proposed for it.

HONEST STATUS OF THE RELATIVISTIC COMPLETION.
  The relativistic force-law completion is NOT available.  What stands is
  H001's action as a description of the three sectors, plus the equilibrium
  reading certified in the glm53 track (the RAR as the hydrostatic
  equilibrium of the cold sector).  The preferred-frame gate is the wall,
  and it has now been tested against the best escape available.

This file exists so that the refutation is in MY track's record, not only in
hunt_2026's.  It prints no passing checks, because there are none.
"""
print(__doc__)
print("="*70)
print("H004 REFUTED.  H001's three sectors stand; the solar-system")
print("escape does not.  The alpha_1/alpha_2 lock holds against it.")
print("="*70)
