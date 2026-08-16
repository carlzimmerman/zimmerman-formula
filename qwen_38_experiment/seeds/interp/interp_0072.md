# H-72 — interpret seed_0072 charitably (one concrete, falsifiable hypothesis)

## What the seed says
Two SM/framework numbers look like polyhedral solid angles; a wildcard asks what
single dimensionless number both bullets share if true.
- Bullet 1: a "drain-flow" boundary-term ratio interpolates to the Cabibbo angle,
  target 0.2250 (~ sin theta_C, PDG 0.2243).
- Bullet 2: a "polyhedral solid angle of the top Yukawa (~0.70)" quantizes
  kappa = 0.551 +/- 0.043. kappa is FITTED, not derived -- never claim otherwise.
- Wildcard: one dimensionless number that generates BOTH.

## Charitable reading (the shared number)
The wildcard is a polyhedral solid angle. Cleanest candidate = solid angle of a
regular tetrahedron vertex:
    G = 3*arccos(1/3) - pi  ~ 0.551285 sr.
This coincides with kappa (0.551 +/- 0.043) at ~0.01 sigma. Charitable claim:
kappa = G exactly; the top Yukawa ~0.70 is the "polyhedral solid angle" the
quantization is built from (some polyhedron face/vertex has solid angle ~0.70).

## The single shared number
S = { p/q * (a Platonic-solid vertex solid angle) : p,q integers, q <= 6 }.
Claim: BOTH 0.2250 (Cabibbo) and 0.551 (kappa) are members of S.
Kappa is in S trivially (q=1, tetrahedron). The non-trivial test is whether
0.2250 is a small rational multiple of some Platonic vertex angle.

## Exact test
1. Platonic vertex solid angles (sr):
   tetra 3*arccos(1/3)-pi = 0.551285; cube pi/2 = 1.570796;
   octa arccos(-1/3) = 1.910633; dodeca = 2.671191; icosa = 2.308602.
2. Form S = {p/q * omega : omega in the above, p=1..6, q=1..6}.
3. Pass iff |s - 0.2250| <= 0.001 AND |s' - 0.5513| <= 0.001 for some s,s' in S.
4. Pre-register S BEFORE checking (this interp IS that statement); no post-hoc p/q.

## What kills it (falsification)
- If 0.2250 is NOT in S (no p/q<=6 multiple of a Platonic vertex angle lands
  within 0.001) -> shared-number story is DEAD.
- If 0.2250 hits only via p/q>6 or a lone 4-sig-fig match with no structure ->
  grade CONVENTION, not a hit.
- Expected: 0.2250 likely NOT in S (0.2250/0.5513 = 0.4081 ~ 2/5 gives 0.2205,
  a ~2% miss) -> probable REFUTED/NULL. That outcome is a success.

## Footings
Purely dimensionless (angles, kappa, y_t). If any future test converts to a
dimensional quantity, report both footings 9.3619e-11 and 1.1279e-10.
