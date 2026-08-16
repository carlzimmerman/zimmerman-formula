# INTERP 0046 -- gate-torsion fixes the two 0.23 mixing numbers

## Seed (verbatim)
1. "the torsion of the y-gate might set the Cabibbo angle (0.2250)."
2. "the pi-free part of sin^2 theta_W (0.2312) could interpolate to the pinned Q0 band."
3. wildcard: "what single dimensionless number would BOTH bullets share if true?"

## One-sentence hypothesis
The y-gate fixes ONE dimensionless torsion  τ_y ≈ 0.228 that simultaneously equals
sin(theta_C)=0.2250 and the pi-free component of sin^2(theta_W)=0.2312, and that this
same τ_y, routed through the framework's committed x->Q0 lane, lands inside the pinned
Q0 band [0.0024, 0.0146] Mpc^-1.

## Wildcard answer
The shared number is the ~0.23 near-equality itself: sin(theta_C) ≈ 0.2250 and
sin^2(theta_W) ≈ 0.2312 already agree to ~2.7%, so "one number" = τ_y ≈ 0.228 with the
two SM values being the same τ_y seen through two different normalizations.

## Exact quantities and test
- sin(theta_C) = 0.2250  ;  sin^2(theta_W) = 0.2312  (PDG-ish, taken as given).
- "pi-free part of sin^2(theta_W)": decompose sin^2(theta_W) = a_pi + b*π with b supplied
  by the framework kernel; the pi-free part is a_pi. (If no framework term fixes b, see
  KILL below.)
- Q0 band = [0.0024, 0.0146] Mpc^-1 (from targets_zimmerman.py, grade DERIVED).
- TEST 1 (near-equality): |0.2250 - 0.2312| / 0.2312 <= 0.05  ->  ~3%, PASS.
- TEST 2 (pi-free = Cabibbo): a_pi (b framework-fixed) == 0.2250 within 1 sigma.
- TEST 3 (interpolation to Q0): map τ_y -> Q0 via the committed x->Q0 lane
  (nbody_2026/stage58_x_to_q0) and check 0.0024 <= Q0(τ_y) <= 0.0146.

## Kill criteria (any one kills it)
- K1: "pi-free part" needs a free parameter b to hit 0.2250 (i.e. it is NOT framework-fixed
      -> underdetermined, not a prediction).
- K2: the τ_y -> Q0 image misses [0.0024,0.0146] by a factor > 2.
- K3: the two SM inputs fail TEST 1 (they don't; ~3%).
- K4: the τ_y value is not reproduced independently of the target (circular fit).

## Footings (R3) -- the dimensional leg
The Q0 leg is dimensional (Mpc^-1). Where the x->Q0 lane routes through a0, quote BOTH
footings: canonical a0 = 9.3619e-11 m/s^2 and alt a0 = 1.1279e-10 m/s^2, and show the
resulting Q0(τ_y) band under each. τ_y and the two mixing numbers are dimensionless.

## Named assumptions (CANDIDATE, not CONFIRMED)
- A1: "y-gate torsion" = a single framework scalar, not a family (charitable reading).
- A2: "pi-free part" is a deterministic kernel projection, not a fitted residue.
- A3: the x->Q0 lane is the committed one (stage58), single-valued.
Direction-of-risk: WIN-risk (a 0.23 coincidence dressed as a shared origin).
Next: blind referee reads ONLY this file. This session does NOT test it.
