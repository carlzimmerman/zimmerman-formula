# INTERP 0008 — from seed_0008.txt (random collision, interpreted charitably)

SEED: (1) a saturation bound on the dust-mass-is-charge theorem (rho/n = Q0)
could be measured by n_s = 0.9649. (2) a resonance between the top Yukawa
(~0.70) might set an "off-switch" at recombination. (3) wildcard: the single
dimensionless number both bullets share.

## Charitable reading
Both bullets are two faces of ONE dimensionless "saturation gap"
  sigma = 1 - n_s = 1 - 0.9649 = 0.0351   (equivalently n_s = 0.9649).
- Bullet 1: the dust-mass charge ratio saturates rho/n = Q0 at a level whose
  gap from the geometric bound is sigma.
- Bullet 2: the "off-switch" fires at recombination when the RG-run top Yukawa
  y_t(T) drops to the resonance value sigma (or 1 - sigma); y_t ~ 0.70 is the
  input coupling, the resonance is the *deviation* sigma, not 0.70 itself.

## Hypothesis H8 (single shared number = sigma = 0.0351)
The SAME dimensionless gap sigma sets (i) the dust-mass charge-ratio
saturation 1 - (rho/n)/Q0 = sigma  AND  (ii) the recombination off-switch,
defined as the temperature T_switch where the RG-run top Yukawa satisfies
y_t(T_switch) = 1 - sigma  (= 0.9649).  This predicts T_switch and hence z_rec
with NO free parameter (y_t RG is public, calculable to 2-3 loops).

## Exact test (kill conditions)
1. Solve the known y_t RG beta(y_t, alpha_s, alpha_1,...) from y_t(M_Z)=0.70
   (seed value; flag that PDG central is 0.93 -- a discrepancy is itself data)
   down to T ~ 0.26 eV.  Predict T_switch = T where y_t(T) = 0.9649.
   KILL: if y_t is monotone-bounded and never crosses 0.9649 on [0.26 eV, M_Z],
   or T_switch > 10^4 eV / < 1 eV (off by >2 orders of magnitude from 0.26 eV).
2. Convert T_switch -> z_switch = (T_switch/0.26eV)^{1/4}-1 and compare to
   z_rec = 1089.  KILL: |z_pred - 1089| / 1089 > 0.05.
3. Independently, the saturation reading of bullet 1 must give 1-n_s = sigma
   agreeing with the measured 0.0351 to within its ~5-sigma error (0.0067).
   KILL: |sigma_pred - 0.0351| > 2*0.0067.
All three must hold; failing any one refutes H8.

## Notes for the referee
- sigma=0.0351 is dimensionless; no footing (9.3619e-11 / 1.1279e-10) applies.
- y_t=0.70 vs PDG 0.93 must be flagged: a ~30% input error propagates to the
  z prediction; the test still runs but tolerance should widen to 1 order of
  magnitude, not be abandoned.
- This is a conjecture, not a derivation; kappa=1/2 is fitted (0.551+/-0.043)
  and is NOT invoked here.
