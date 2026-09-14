# INTERP 0017 -- from seed_0017 (random collision), charitably deciphered

**Charitable read.** Two independent-looking claims are TWO measurements of ONE
dimensionless number:
(1) kappa's pi-free holonomy angle THETA_KAP (kappa=0.551+/-0.043, pi-free/proven)
    BOUNDS the Koide charged-lepton factor Q = 2/3 (0.666667);
(2) the beat frequency between the CKM CP phase delta=1.144 rad and the X-pin
    (X = sqrt(y) c/v, beta=1 selected so c/v=1 so X=sqrt(y), X in [106,453])
    ALSO reads 2/3.
If the two legs need two different numbers, there is no "single number."

**Wildcard answer (the shared number): N = 2/3 = 0.666667 (the Koide factor).**
The crux: BOTH legs must independently reproduce 0.666667 from pi-free inputs, or
the hypothesis is wrong. (Hook that motivated it: X=106 mod 2pi = 5.47 rad;
|5.47 - 1.144| = 4.33 rad = 0.689 cyc ~= 2/3. Borderline by design -- referee tests.)

**Leg 1 -- Koide bound via pi-free holonomy.**
- Quantity: Q_Koide = 0.666667 (charged-lepton masses; framework positive control
  targets_sm.py koide_Q=0.666661).
- "Holonomy angle of kappa bounds 2/3": a named pi-free map f(THETA_KAP) = 2/3,
  THETA_KAP = 0.551. Pre-register the admissible family = small-integer rational
  polynomials in THETA_KAP (deg<=3, coeffs in {-2..2}), NO pi, NO free prefactor
  beyond the map itself.
- Test: scan the family, take best |f(0.551) - 2/3|; tol 2% (rel 1.3e-2).
- KILL if the best admissible map misses 2/3 by > 2%, OR closure needs a
  CONVENTION-grade free prefactor (a free prefactor closing it is NOT a hit).

**Leg 2 -- CKM beat via X-pin.**
- Quantity (dimensionless): beat b = |delta_CKM - (X mod 2pi)| reduced to cycles
  in [0,1) via /2pi. delta_CKM = 1.144 rad; X = sqrt(y), X in [106,453].
- Claim: b = 2/3 (the SAME number as Leg 1) at a PHYSICALLY-PINNED X (y named),
  not a free X.
- Test: scan X in [106,453], plot b(X); check b = 2/3 to ~2% at the physically
  motivated X. Report all X where |b - 2/3| < 0.013.
- KILL if b = 2/3 only at an X not pinned by any named y (free X = CONVENTION,
  not a hit), or no X in the physically-motivated set gives b = 2/3 to ~2%.

**Both footings (dimensional numbers dual-stated).**
a0 = 9.3619e-11 m/s^2, a0' = 1.1279e-10 m/s^2. y (the X driver) may differ across
the fork; if so, run b(X) for each footing -- a hit requires the SAME N=2/3 on
both footings, not one per footing.

**Joint falsifier (the crux).** N = 2/3 must come from BOTH a pi-free map of
THETA_KAP (Leg 1) AND a CKM<->X beat at a physically-pinned X (Leg 2). If EITHER
leg needs its own ad-hoc number, or N differs between legs, the single-number
claim is REFUTED even when one leg accidentally fits. A CONVENTION-grade match is
NOT a hit.

**Routing:** blind referee tests legs 1 & 2 numerically (mm_search.py, FDR
pre-registered by the engine); grade honestly (REFUTED / NULL / DISCARD all OK).
