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

## cm03: the same test with weak-lensing-calibrated group mass bias -- C003's group prediction FAILS at 2.7 sigma
`cm03_c003_groups_wl_bias.py` (MUTATE C003 = 0.9 flips the verdict to CONSISTENT). The 20% hydrostatic allowance replaced by a T-dependent bias
b(T) = b1 (kT/keV)^-0.86, b1 = 0.4 (0.3-0.5), from Kettula+2013 (COSMOS groups, WL: 30-50% at 1 keV; PROVISIONAL, read via search summary) -- groups here are
0.85-2.8 keV. Required retained fraction (definition A, calibrated on X-COP): 0.549 (b = 0), 0.749 (b = 0.1 flat, FLAMINGO), 1.09 / 1.38 / 1.69 (b1 = 0.3/0.4/0.5)
vs C003's 0.30: median difference +1.04 +- 0.38 -> +2.73 sigma, FAILS (groups need MORE cold mass than C003 keeps). Lensing makes groups heavier, not lighter.
Caveats: definition A is relative to TODAY's baryons and groups have lost baryons (f_b ~ 0.10; CFG34's rho = -0.96), so A > 1 partly measures that loss;
definition B (relative to the LCDM-like dark mass, bounded by 1) gives 0.37 (b = 0) and 0.60 (b1 = 0.4) -- the same direction, still twice C003's 0.30.
R500 and M_gas are not re-evaluated at the corrected mass. Reading: C003's "groups largely emptied" signature is disfavoured; groups behave closer to clusters.

## cm04: hot-halo hypothesis on the SLUGGS ellipticals with measured hot gas -- NOT SHOWN (N = 7)
`cm04_sluggs_hot_halo.py` (1/1; MUTATE shuffles gas, fails R). Already in the record: massive early types FAIL the bare law in their outer GCs
(+0.098 dex in sigma, 4.0 sigma stat; 2.8 sigma without the 4 group/cluster centrals; AUDIT_SLUGGS 10-03) -- the direction the hot-halo idea needs.
The sharper test, offset vs MEASURED hot gas (CFG57: 7 galaxies, M_gas < 20 kpc): rho(offset, gas/M*) = +0.32 (p = 0.25); rho(offset, M_gas) = +0.68 (p = 0.054);
without M87 -0.09 (p = 0.61). The raw-gas trend is carried by the cluster/group centrals (M87, NGC 5846) and vanishes without M87. NGC 4365 (little gas) shows
+0.205. Reading: the ellipticals' excess is real-ish but is not shown to track hot gas; with N = 7 this neither supports nor refutes the hypothesis.
A decisive version needs X-ray luminosities for all 16-17 (e.g. Kim & Fabbiano 2015 / O'Sullivan catalogues) -- a fetch.
