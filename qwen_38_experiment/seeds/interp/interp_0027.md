INTERP 0027 (from seed_0027 -- charitable decipher, untested)

READ: only seed_0027.txt. Framework terms (footing-invariance, the f=1/3
fixed point, the "drain flow", the top-Yukawa saturation bound) are taken
"as defined in the framework"; the blind referee grounds them.

DECIPHER
Two "one-coupling, two-jobs" selections tied by one wildcard:
 (A) a FOOTING-INVARIANT dimensionless group C(mu) sits at the gravity
     footing as M_lens/M_dyn = 29 (the f=1/3 fixed point) and, run under the
     "drain flow", reaches the lepton footing as m_mu/m_e = 206.77.
 (B) the SAME run is selected (not two separate flows) by a saturation bound
     on the top Yukawa, y_t,sat ~ 0.70, which picks the drain trajectory.
 Wildcard: a SINGLE dimensionless number that is the shared kernel of both,
 so A and B are one RG measurement seen twice, not two fits.

HYPOTHESIS (falsifiable, one free parameter kappa*)
There is ONE dimensionless kernel kappa* (conjectured 1/2; currently a FIT,
0.551 +/- 0.043 -- NOT derived) such that:
   -- kappa* sets the f=1/3 fixed-point structure of the beta-function of a
     dimensionless group C(mu), with C(mu_grav) = 29;
   -- the drain flow is the unique RG trajectory selected by the top-Yukawa
     saturation y_t,sat = sqrt(kappa*); for kappa* = 1/2 this is
     y_t,sat = sqrt(1/2) = 0.7071 ~= the ~0.70 of the bullet;
   -- running C(mu) along that trajectory to the lepton footing gives
     C(mu_ell) = m_mu/m_e = 206.77.
WILDCARD ANSWER: the shared number is kappa* = 1/2, equivalently
y_t,sat = sqrt(kappa*) = 0.707 (the top-Yukawa saturation bound). The two
bullets share it because the same eigenvalue fixes both the fixed point
(29) and the trajectory (drain flow) that carries 29 -> 206.77.

EXACT TEST
1. Fix kappa* = 1/2 in advance (do not refit per bullet); the alternate
   candidate is the fitted 0.551.
2. Write the single beta-function dC/dln(mu) = C * B(C, kappa*) with a fixed
   point at f=1/3 giving C(mu_grav)=29; integrate to mu_ell and require
   C(mu_ell)=206.77; check y_t,sat = sqrt(kappa*) = 0.707.
3. A pass = ONE kappa* lands all three (29, 206.77, 0.707) simultaneously,
   pre-registered and parameter-free beyond kappa*. A near-miss within 2x tol
   with one principled, value-justified fix -> REFINE-once.

WHAT KILLS IT
-- kappa* that lands 29 -> 206.77 != kappa* that saturates y_t at 0.707
   (two distinct values) => wildcard fails => REFUTED.
-- No parameter-free flow connects 29 to 206.77 without a 2nd/3rd free
   parameter => overfit => DISCARD.
-- TENSION TO GROUND: the measured top Yukawa is y_t(m_Z, MSbar) ~ 0.94
   (y_t(m_t) ~ 0.74-0.79 by scheme), NOT 0.70; if the "saturation bound
   ~0.70" cannot be reconciled with the measured y_t within ~2 sigma the
   saturation claim is REFUTED.
-- Any footing-dependence (C(mu_ell)/C(mu_grav) depends on which footing one
   reads it in) => the "invariant" claim is false => REFUTED.
-- Counting a CONVENTION-grade match as a hit is not allowed.

NOTE: 29, 206.77, 0.70 are target values for grounding only; do NOT claim
either 29->206.77 or the Yukawa bound is DERIVED. kappa = 1/2 stays a FIT
(0.551 +/- 0.043). This is a dimensional/structural conjecture pending the
blind referee.
