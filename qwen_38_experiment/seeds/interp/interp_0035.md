INTERP 0035 (from seed_0035 -- random collision, interpreted charitably)

CHARITABLE READ: the seed collides two gates that look unrelated -- the flavor gate
(Cabibbo mixing) and a weak-sector gate (the "y-gate", set by sin^2 theta_W) -- and
claims ONE phase event, the "off-switch at recombination," fixes both. The wildcard
asks for the single dimensionless number common to both.

SHARED NUMBER (wildcard answer): a single mixing amplitude theta_off, the dimensionless
strength of the off-switch at recombination. Both bullets are projections of theta_off:
  * flavor sector:  tan(theta_C)  = tan(theta_off)   -> 0.2308 (PDG)
  * gauge  sector:  sin^2(theta_W) = sin^2(theta_off) -> 0.2312 (PDG, Z-pole)
The seed quotes sin(theta_C)=0.2250; I read the intended common quantity as the mixing
amplitude ~0.231 (tan theta_C = 0.2308 ~= sin^2 theta_W = 0.23122, a 0.17% match).
So the shared number is m_off = tan(theta_off) ~= 0.231, i.e. theta_off ~= 13.0 deg,
the SAME angle that IS the Cabibbo angle. Hypothesis bets this 0.17% match is a real
projection, not a fluke.

EXACT QUANTITIES:
  m_off (off-switch amplitude at recombination) = tan(theta_off), predicted 0.2310 +/- 0.0010
  P1: tan(theta_C)    = m_off    (obs 0.2308  +/- 0.0002)
  P2: sin^2(theta_W)  = m_off    (obs 0.23122 +/- 0.00035)
  P3: residual delta = sin^2(theta_W) - tan(theta_C) = +0.0004, predicted NONZERO and
      equal to the gate width w_gate = a0 / a_recomb (dimensionless; a0 on both footings
      9.3619e-11 & 1.1279e-10 m/s^2; a_recomb the recombination plasma acceleration).

EXACT TEST:
  1. Compute m_off from recombination-scale dimensionless data ONLY (CMB acoustic scale /
     plasma frequency / baryon loading), with NO reference to theta_C or theta_W.
  2. Project through the two fixed maps P1, P2. PASS iff |P1-0.2308|<3e-3 AND
     |P2-0.2312|<3e-3 hold SIMULTANEOUSLY for one m_off.
  3. Predict delta=0.0004 as w_gate: a gate width from a0/a_recomb must land in
     [1e-4, 1e-2].

KILL CONDITIONS (any one refutes):
  (a) m_off from recombination physics misses 0.231 by >3e-3            -> REFUTED
  (b) P1 and P2 force two different m_off (cannot both hold)           -> NULL
  (c) delta not reproducible from a0/a_recomb on EITHER footing        -> REFUTED
  (d) treating theta_C & theta_W as free SM fits gives no shared param  -> REFUTED

FOOTINGS: every dimensional gate width w_gate reported on a0 = 9.3619e-11 AND 1.1279e-10.
NOTE: if the 0.17% tan(theta_C)~sin^2(theta_W) match is a genuine coincidence, step 3
fails and the whole idea is DISCARD-grade; that is the designed risk.
