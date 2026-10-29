# Frozen outward mass-vector subexperiment

Cover exactly124 certified endpoint brackets (62 active nodes, two endpoints)
and all3601 saved source radii. Interpret saved M,R,Sigma,r0 brackets, native
log stellar masses/radius-grid entries, and computed binary64 stellar/cold-gas
coefficients as fixed exact numbers. This scope does not certify how those
coefficients were produced or enclose L-dependent column/branch arithmetic.
Use50-digit mpmath interval arithmetic, mathematical pi and exact hot radius
100000pc. For each radius r, put t=min(r,R), and bound halo mass using

 pi Sigma r0_lower^2 B(t/r0_upper) <= Mh <=
 pi Sigma r0_upper^2 B(t/r0_lower).

B increases since B'(x)>0. Add the exact fixed-coefficient baryonic profile
Ms+Mc+0.5 Ms min(1,(r/100000)^3) with interval arithmetic. Certify each root
bracket again with directed outer-mass signs before using it. Save binary64
outer enclosures by converting interval endpoints then taking nextafter toward
-/+infinity. Check stored bounds still enclose the interval values. No tolerance
may decide containment.

Compare each interval enclosure with the earlier NumPy factor-product box
padded by relative1e-8 plus absolute1e-6Msun. All comparisons use directed
interval endpoints and must cover every node/endpoint/radius, never a subset.
If this padding fails, preserve the failure and the outward arrays; do not
silently enlarge the registered padding. A1% shifted first-node candidate box
must fail containment. Require finite nonnegative ordered outward bounds,
correct coverage, unchanged inputs, and scalar analytic B(0)=0. Print progress
only to saved logs. Bound to wall600s/CPU480s/one numerical thread.

The outcome certifies fixed-coefficient endpoint mass vectors only. It cannot
promote interval_001's score to a certified exclusion: column/branch/continuum
construction, projection/stacking/whitening coefficients and signed-dot error
bounds remain separate obligations. No observational refit or new parameter.
