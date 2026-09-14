# INTERP 0057 -- the shared charge-gauge reading (lepton ratio = weak-angle torsion)

SEED 0057 (charitable reading):
- resonance A(Q)=kappa^2 G(-K) selects m_mu/m_e = 206.768 (PDG: 206.7682835).
- the nu0-meter (DR4 used as a charge gauge) measures the "torsion" of sin^2 theta_W
  = 0.231219 (Z-pole value).
- wildcard: ONE dimensionless number both bullets share if true.

## HYPOTHESIS (falsifiable)
There exists a SINGLE dimensionless "charge-gauge reading" g -- the common mode index of
the resonance -- such that the muon/electron mass ratio and the weak mixing angle are two
projections of the same g:

    m_mu/m_e = 206.768 = R(g*)      (R = resonance map from A(Q)=kappa^2 G(-K))
    sin^2 theta_W = 0.2312 = T(g*)  (T = nu0-meter torsion of the weak angle)

R and T are both functions of the one real dimensionless g (kappa held at 0.5). The "shared
number" is g* itself: the mode index the two independent apparatuses both read.

## EXACT TEST
1. Build R(g): scan g over half-integer mode index; evaluate R via the resonance
   A(Q)=kappa^2 G(-K) at kappa=0.5. Find the discrete mode where R(g)=206.768 -> gives g*.
2. Build T(g): evaluate the nu0-meter torsion T at the SAME g* (no refit of kappa).
3. Predicted shared number: T(g*) should equal 0.2312.

## KILL CRITERIA (any one => REFUTED / NULL)
- R(g) never reaches 206.768 at any discrete mode in the searched band -> REFUTED.
- T(g*) falls outside the 2x tolerance window [0.1156, 0.4624] about 0.2312 -> REFUTED.
- R and T require DIFFERENT g* (no single shared reading) -> NULL (no unification).
- g* is non-discrete / not an integer or half-integer -> REFUTED (resonance has no mode).

## FOOTNOTES
- Both footings: 9.3619e-11 and 1.1279e-10 must be reported for any dimensional readout.
- kappa = 1/2 is a FITTED parameter (0.551 +/- 0.043), NOT a derivation; used as a held input.
- Any match found must clear mm_search.py FDR pre-registration; CONVENTION-grade matches are
  NOT hits.
- Blind referee grades this; if true the shared g* is itself a new SM-number candidate.
