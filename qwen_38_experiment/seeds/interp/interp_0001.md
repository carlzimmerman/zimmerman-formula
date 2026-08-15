INTERP 0001 (from seed_0001.txt -- random collision, read charitably, tested later)

SEED COLLISION
- A duality exchanging the binding-epoch wall z = 10.8 might set sin^2 theta_W = 0.2312.
- Spontaneous breaking of the CKM CP phase delta_CKM ~ 1.14 rad might be measured
  by the pinned Q0 band.
- Wildcard: what single dimensionless number do BOTH bullets share, if true?

CHARITABLE DECISSURING
The two bullets are two projections of ONE dimensionless control parameter C: the
critical (fixed-point) coupling of the binding-epoch theory evaluated at the wall
z = 10.8. A wall duality is a critical rescaling; its fixed point is a single number.
Bullet 1 = the projection C -> sin^2 theta_W fixed by the wall duality.
Bullet 2 = the same C as an order parameter that breaks spontaneously, its breaking
angle -- read on the pinned Q0 band -- equal to the CKM CP phase.
The "shared number" is C itself (one scalar), NOT two independent constants.

HYPOTHESIS (one, falsifiable)
There exists a single dimensionless C such that
  (i)   sin^2 theta_W = f_wall(C, z=10.8)   [wall-duality relation]
  (ii)  delta_CKM    = f_Q0(C, Q0)          [spontaneous breaking on the Q0 band]
Eliminating C yields a predicted constraint R(sin^2 theta_W, delta_CKM, Q0) = 0
among 0.2312, 1.14 rad, and the Q0 band value. Hence sin^2 theta_W and delta_CKM
are NOT independent -- they are two projections of one C.

EXACT TEST
1. From the wall duality, solve (i) for the C that reproduces 0.2312 -> C_hat.
2. Feed C_hat into (ii) via the Q0 band; compute delta_pred.
3. Compare delta_pred with the CKM phase 1.14 rad.
SUPPORTED iff |delta_pred - 1.14| < (Q0-band width + fit error). Any dimensional
normalization used must carry BOTH footings: 9.3619e-11 / 1.1279e-10.
No numeric coincidence is asserted here; mm_search.py pre-registers any numeric
match under FDR, and a CONVENTION-grade match does NOT count as a hit.

WHAT KILLS IT
- No common C: the C that gives 0.2312 via the wall does not give 1.14 via Q0.
- Q0 is decoupled from the CP phase (Q0 does not enter delta_CKM).
- The wall "duality" is not critical -- no single fixed point -> no shared number.

OUT OF SCOPE (deferred to the blind referee)
- Numeric matching of 0.2312 / 1.14 / 10.8 -> mm_search.py, FDR pre-registered.
- Whether f_wall / f_Q0 are the "right" functional forms is a separate seed.
- This interp asserts only the SHARED-NUMBER structure, no specific value.
