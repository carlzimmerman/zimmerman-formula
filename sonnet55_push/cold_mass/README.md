# Cold mass lane (owner-directed, 2026-10-06)

## cm01: "expelled where MOND is active" -- no function of local MOND activity can do it
`cm01_mond_activity_gate.py` (1/1; MUTATE cluster baryons x100 fails O). SPARC (Q <= 2, 163 galaxies) rotation-curve edge y = g_bar/a0: median 0.061
(16-84%: 0.030-0.160); cluster R500 (X-COP-like, provisional inputs: M500 3e14-1e15, f_b 0.13-0.16): y = 0.056-0.103. 43 spirals sit INSIDE the cluster range,
on both footings. Spirals tolerate f <= 0.105 there; clusters need f = 0.58 at the same y. So the cold mass's retention cannot be any function of the local
MOND activity (or of g_bar alone). What differs between a spiral edge and a cluster R500 at equal y is global: host mass, potential depth / escape speed
(~150 vs ~1000 km/s), hot gas, formation history. Potential-depth thresholds are already excluded by the forest (L175); the escape-speed kick (C003, L191)
is the record's surviving reading. Nothing here derives the cold amount; the mass is still required.

## cm02: C003's group prediction vs the 20 Lovisari+2015 X-ray groups -- consistent but NOT diagnostic
`cm02_c003_groups.py` (2/2; MUTATE C003 = 0.9 flips to FAIL). Groups loaded exactly as CFG34 (h7 slices, read-only). Retained-fraction definition calibrated
on X-COP first: A = cold_req/((Omega_c/Omega_b) M_b) gives the ledger's 0.576 exactly (B gives 0.534). Groups (M_b(R500) 2.2e12-1.4e13): required f median
0.549 (16-84%: 0.30-0.90); C003 (L191, interpolated log-linearly in M_b between its group 1e12 = 0.168 and cluster 1.4e14 = 0.664 anchors) predicts 0.302.
Median difference +0.219 +- 0.397 -> +0.55 sigma: CONSISTENT under the pre-declared rule, but the error is dominated by the 20% hydrostatic-bias allowance
(0.372); without it the lean is +1.55 sigma toward groups needing MORE cold mass than C003 keeps. Non-diagnostic until group masses are lensing-based.
