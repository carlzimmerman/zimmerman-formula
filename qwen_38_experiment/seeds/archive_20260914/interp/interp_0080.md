INTERP 0080 -- shared invariant x = m_W/m_Z between the frozen binary band
and the PMNS saturation off-switch (charitable read of random-collision seed 0080)

CHARITABLE READING of the three seed bullets:
 B1  A "frozen wide-binary band" B = [1.1614, 1.1814] (two degenerate pre-breaking
     branches; width w = 1.1814-1.1614 = 0.0200, center c = 1.1714) breaks
     spontaneously, and its breaking is MEASURED by the electroweak ratio x = m_W/m_Z = 0.8814.
 B2  A saturation bound on the PMNS solar mixing, s^2 = sin^2(theta_12) = 0.307,
     renormalizes (RG-flowed down) into an "off-switch at recombination" -- a mixing/coupling
     that turns off at the recombination epoch.
 WILD  The single dimensionless number BOTH bullets share, if true.

HYPOTHESIS (one, falsifiable):
 There exists a single dimensionless invariant x that is simultaneously
   (a) the order parameter for the spontaneous breaking of B (B1), and
   (b) the saturated value of the PMNS off-switch once renormalized to recombination (B2).
 Charitable candidate for the shared number: x = m_W/m_Z = 0.8814 (from B1), and B2 must
   then be a ONE-PARAMETER prediction: s^2 = 0.307 is a function of x alone.

EXACT QUANTITIES (seed values, no target peeking):
  B_lo = 1.1614 ; B_hi = 1.1814 ; w = 0.0200 ; c = 1.1714
  x = m_W/m_Z = 0.8814
  s^2 = sin^2(theta_12) = 0.307
  recombination anchor T_rec ~ 0.28 eV (dimensional).

EXACT TEST (declared monotone map, declared before any fit -- no p-hacking):
  T1 (B1 breaking): the band splits by x. PASS iff c/x and c*x straddle B within w:
       c/x = 1.340 (outside B_hi) ; c*x = 1.032 (outside B_lo).
     As written c/x and c*x DO NOT both fall inside [1.1614,1.1814] -- so the naive
     "split by x" map FAILS; the referee must either supply ONE declared alternate
     one-parameter map f with f(x)=s^2, or declare the breaking test unmet.
  T2 (B2 off-switch): PASS iff s^2 = 0.307 is a declared one-parameter function of x:
       f(x) = 0.307 with ZERO free parameters (the map fixed by x only).
  Shared-number check (WILD): PASS iff the SAME x that sets the B1 breaking also yields
       s^2 = 0.307 under the same f -- i.e. one number, one map, two observables.

KILLER (any one kills it):
  - T1 as written fails (c/x, c*x miss B): if no declared alternate one-parameter map
    restores the split, REFUTED.
  - T2 needs >0 free parameters to force 0.307 from 0.8814: the "shared number" is then a
    dial, not a prediction -> REFUTED (p-hacking).
  - DISCARD if the wildcard cannot be written as ONE number without >=2 free parameters.
  - NULL if T1 and T2 "pass" only via an ad hoc map carrying no residual predictive power.

FOOTINGS (dimensional anchor -- both required, per PROTOCOL):
  Any dimensional instantiation of the recombination off-switch scale (an acceleration/energy
  read as a0-like) is evaluated on BOTH footings: 9.3619e-11 and 1.1279e-10 (m/s^2).
  T2 must pass on BOTH; passing on only one is NULL.

STATUS: proposed; NOT tested here. Blind referee grades REFUTED / NULL / PURSUE / DISCARD.
