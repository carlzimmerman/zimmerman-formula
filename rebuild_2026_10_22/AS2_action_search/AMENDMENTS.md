# AS2_action_search amendments

## A1, before any gate number (grammar counting only had run)
The frozen cap of 1,000,000 binds partway through size 8 (sizes 1-7 give 303,706; unary forms of size 7 fill the rest), and AeST's capped J, y + log(1-y) + u/2, has 8 nodes and is not reached. KA1 requires it. Cap raised to 2,500,000 so that size 8 can finish. Nothing else changes. The grammar uses no physics target in its order. The first 1,000,000 are the same expressions as before.

## A2, before any count or survivor list (only known-answer rows had been debugged, with a placeholder Q2)
Debugging on the known-answer rows (bare khronon, AeST, v3, BIMOND, one SKh row) showed four points in the frozen text that need stating. I saw those rows' gate labels before writing this, and the SKh row was one I had named in the criteria as my expected closest. No count, tally or survivor list exists yet.
1. **G_N normalisation.** With K_B != 0 the Newtonian limit of the AeST-form rows is G_N = 2 G~/(2 - K_B) (C1), so the G1 test uses that G_N in those rows (contents SAe, SKh, KhP, AeP). Other rows use the bare G.
2. **BIMOND carrier.** The law's argument is h = a x y with a the mass split (UX1), so Y_B's carrier is normalised with a^2. The grammar then reaches a = b = 1/2 only; a = 0.16 and 0.84 need b/a as a constant, and the grammar has none. Static reduction uses Milgrom's branch Phi = Psi on each metric, which is consistent because both the Einstein-Hilbert form and Y are q = 2 Phi Psi - Psi^2.
3. **G5 has two branches.** The record's alpha_1 = -2(K_B+2) (V9_PPN_KILL_VERDICT) comes out only when the gravitomagnetic response is divided by the STATIC potential. With a source moving at fixed v and v -> 0, the zero-speed pair responds and Phi goes to the bare Newtonian value (this is H5's and O1's velocity-screening statement). Both readouts are computed. G5 PASS needs moving-branch alpha_1 and alpha_2, and static-branch alpha_1, all inside the bounds. KA4d and KA4e test the static branch at J_Y = 1: J_Y = F/(2 - K_B).
4. **G5 precision.** Double precision gives noise rising with F (1e-4 at F = 1e8). G5 is taken from an exact rational solve of the blocks (sympy, then 50-digit evaluation), not double precision.

## A3, after RUN1 (`as2_run_RUN1.log`)
RUN1 printed counts and failed five known-answer checks. All five were faults in the checks, and I fixed them after seeing the counts. Disclosed; no label moved except the check itself.
- KA1a, KA1b compared derivatives for equality, but the grammar's coefficient sits partly inside the expression (2*(2*(log1p(y)-y)) x 1). Now tested as proportional.
- KA3b, KA3c used double precision at tolerances 1e-8, 1e-5 and missed by 1.1e-8, 5.4e-5. G5 itself uses the exact block solve (A2.4), so KA3 now tests that path on exact rational coefficients, with the same tolerances.
- KA4i looked for an SX row and found none: the grammar can't reach the QUMOND parent's h = y/4. This is a grammar gap, reported. The check now tests indefiniteness directly.
