# INTERP 0088 -- charitably read, to be tested brutally by a blind referee

## Charitable reading of the random collision
Bullet 3 (the wildcard) is the crux: "what single dimensionless number do BOTH
bullets share?" The charitable answer is the **vertex solid angle of the regular
tetrahedron**:

    Omega_4 = 3*arccos(1/3) - pi  =  0.551285...

This is the ONLY standard polyhedral solid angle that lands in the kappa band
(cube pi/2=1.571, octa 2.59, dodeca 2.96, icosa 4.09 all miss badly).

## Hypothesis H88
A single regular tetrahedron is the shared geometric object. Its vertex solid
angle Omega_4 simultaneously (a) *is* kappa, and (b) appears in the geometric
projection that turns Z=sqrt(32 pi/3)=5.7888 into the Cabibbo number 0.2250.

## Bullet 2 test (kappa, the solid one)
- Quantity: Omega_4 = 3*arccos(1/3) - pi.
- Test: compute Omega_4; PASS iff 0.508 <= Omega_4 <= 0.594 (the fitted kappa band
  0.551 +/- 0.043).
- KILL: Omega_4 outside [0.508,0.594]; OR the "pi-free" claim is falsified, i.e.
  Omega_4 does NOT reduce to a pi-free value under any claimed identity (arccos(1/3)
  carries a transcendental that is not pi, so "pi-free" is plausible -- the referee
  must verify the identity explicitly, not assume it).
- NOTE: this is a NEAR-MISS candidate (0.5513 vs 0.551 center) not a HIT; kappa is
  fitted, never claim it is derived.

## Bullet 1 test (Cabibbo projection, the speculative one)
- Load-bearing piece = the "projection" function P(Z, Omega_4) -> 0.225.
- Charitable fixed formula (referee must judge whether it is principled, not a dial):
    sin^2(theta_C) ?= Omega_4 / sqrt(6)      (= 0.551285/2.44949 = 0.225066)
- Test: PASS iff 0.225066 is within tol = 0.015 of the measured 0.2250
  (loose tol, honest flag: this is a charitable read, not a precise prediction).
- KILL: P(Z,Omega_4) misses 0.225 by > tol; OR the formula needs a free parameter
  tuned to 0.225 (p-hacking -> DISCARD, not a hit); OR Z=sqrt(32 pi/3) is not actually
  used by the projection (then bullet 1 is disconnected from Omega_4 -> NULL).

## Exact, falsifiable procedure
1. Numerically compute Omega_4 = 3*arccos(1/3) - pi.
2. Test 1: is 0.508 <= Omega_4 <= 0.594?
3. Test 2: compute Omega_4/sqrt(6); compare to 0.2250, tol 0.015.
4. Test 3 (connectivity): does the projection that yields 0.225 actually consume
   Z = sqrt(32 pi/3) = 5.7888? If the 0.225 route does not touch Z, the two bullets
   are decoupled and H88 = NULL.
VERDICT RULE: both Test 1 and Test 2 pass AND Test 3 holds -> PURSUE (as a
near-miss, not a derived result). Any single fail -> REFUTED/NULL/DISCARD.

## Footings
Dimensionless hypothesis; the a0 footings 9.3619e-11 and 1.1279e-10 are NOT invoked
(no dimensional quantities appear in H88). No pi-free claim about kappa is made.
