INTERP 0044 (from SEED 0044, random collision)

WILDCARD ANSWER (shared number): the single dimensionless number both bullets
share is kappa = 1/2 -- the geometric-midpoint coefficient of the X-pin window
AND the renormalization coefficient of the n_s remnant. NOTE: kappa=1/2 is a
FIT parameter (fitted 0.551 +/- 0.043), NOT a derived constant. This hypothesis
treats it as one number appearing in two places; it is a prediction to be killed,
not a proof.

BULLET 1 decoded -- X-pin measured by PMNS solar angle.
  Quantities: X = sqrt(y) c/v (dimensionless) in window [X_min,X_max]=[106,453];
  X_ref = sqrt(106*453) = 219.1; sin^2(theta_12) = 0.307 (theta_12 ~ 33.4 deg).
  Observation: the window is log-symmetric, X_min/X_ref = X_ref/X_max = 0.484 ~ 1/2,
  i.e. kappa=1/2 is the window's half-width coefficient.
  Prediction P1: the resonant pin X_pin = X_ref * sin^2(theta_12)/kappa
                = 219.1 * 0.307/0.5 = 133.6.  (X_pin is a dimensionless count,
                footing-independent: c/v carries no a0.)
  Test: build the X-pin spectrum; a peak must sit at X ~ 133.6 (+/-15%, one band).
  KILL P1: no peak within [114,155], OR the window is not log-symmetric
          (X_min/X_ref != X_ref/X_max within 0.484 +/- 0.05).

BULLET 2 decoded -- n_s remnant renormalizes into rho/n = Q0.
  Quantities: n_s = 0.9649 -> drained remnant delta = (1-n_s) = 0.0351;
  charge theorem Q0 = rho/n (dust mass per particle, dimensional, MOND mass).
  Prediction P2: delta renormalizes to Q0 with coefficient kappa:
                Q0 = kappa * delta * rho_crit / n_ref  (one dimensionless map).
  Both footings (a0-dependent mass Q0, so the number MUST be given twice):
    a0 = 9.3619e-11 m/s^2 :  Q0(1) ~ 0.5 * 0.0351 * rho_crit/n_ref
    a0 = 1.1279e-10 m/s^2 :  Q0(2) = 1.2048 * Q0(1)   (ratio = 1.1279e-10/9.3619e-11)
  Test: compute Q0(1), Q0(2) independently from dust density + a0; match P2.
  KILL P2: the fitted renormalization coefficient for P2 != 0.5 beyond 0.043
          (i.e. |coef-0.5| > 0.043), OR delta does not map to rho/n at all.

SHARED-NUMBER KILL (the whole hypothesis dies if):
  P1's window coefficient and P2's renormalization coefficient do not both
  equal 0.5 within 0.043.  If one is ~0.5 and the other is not, the "single
  number both share" fails and the collision is coincidence.

Protocol: no FDR search (pure hypothesis decode, no scan). No CONVENTION-grade
match counts. Footings both reported. kappa NOT claimed derived.
Falsifiable, concrete, one number: kappa = 1/2 unifying pin-window + n_s remnant.
