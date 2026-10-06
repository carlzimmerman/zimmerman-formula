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

## cm05 + cm05b: all 16 SLUGGS ellipticals with O'Sullivan+2001 L_X -- the excess TRACKS HOT GAS, beyond mass
`cm05_sluggs_lx_all.py` (1/1; MUTATE shuffled L_X fails) and `cm05b_mass_control.py` (1/1; MUTATE L_X := mass fails). Fetch: data_assembly/osullivan2001_lx/.
16 of 17 matched (NGC 1023 absent); hot-gas indicator log(L_X/L_B), 4 upper limits used at their value.
- rho(outer-GC law offset, log L_X/L_B) = +0.64, one-sided p = 0.005 (both footings) -> SUPPORTED under the pre-declared rule.
  Without M87 +0.56 (p = 0.016); detections only +0.60 (p = 0.023, N = 12).
- Confounder (declared after cm05, before cm05b): rho(offset, mass) +0.55, rho(L_X/L_B, mass) +0.59; PARTIAL rho(offset, L_X/L_B | mass) = +0.47 (p = 0.036).
  Hot gas carries information beyond mass.
- The excess is NOT the gas's own mass: CFG57's measured gas moves the law by 0.010 dex and would need 20-100x more to close it. It is extra mass that comes
  WITH a hot atmosphere -- consistent with the hot-halo hypothesis (cold mass retained where a hot atmosphere exists), and with KiDS red-vs-blue (h111).
Caveats: N = 16; upper limits at face value; L_X of centrals includes group/cluster gas (that is a hot atmosphere too); intracluster GCs may inflate the
centrals' offsets (the trend survives without M87); offsets carry shared tracer-slope/anisotropy systematics (they move the level, not the ranking).
Not a mechanism: nothing in the record couples collisionless mass to hot gas. Next: blue spirals at matched mass (should show none) -- KiDS colour split, M/L-robust.

## cm06: blue vs red KiDS lenses at MATCHED stellar mass (CFG261's MM rows, 10.3 <= log M* < 10.9)
`cm06_kids_blue_red_matched.py` (1/1; MUTATE swapped labels fails D). Implied a0 scale s* (1 = law alone), two z-thirds combined by inverse variance:
blue/late s* = 1.69 (+1.9 sigma above the law; its two thirds disagree, 2.0 vs 0.37); red/early s* = 3.78 (+15 sigma). Red - blue = +0.35 +- 0.13 dex (+2.7 sigma).
Reading for the hot-halo hypothesis: at matched mass red lenses carry far more extra mass than blue -- the predicted direction; blue is closer to the law
but NOT shown to be exactly at it (1.9 sigma, internally inconsistent thirds). NOT unique: in LCDM red centrals also sit in ~2x heavier halos at fixed M*
(CFG67: a colour-blind Moster halo fits CFG61's split at 6.9/7), and both classes' M* are SED-based. So this is consistent, not discriminating.

## cm07: 30 SLUGGS early types (Alabi+2017 GC masses within 5 Re) x O'Sullivan L_X -- passes the rule, but it is the group/cluster centrals
`cm07_alabi32_hot_halo.py` (1/1; MUTATE shuffled L_X fails). Fetch: data_assembly/alabi2017/. First run parsed only 16 Table-2 rows (continued table missed);
kept as `cm07_alabi32_hot_halo_v1_16rows.out` and fixed before any reading. Excess = log(M_tot(<5Re)/M_law), M* inside 5 Re from Alabi's f_DM.
- Every early type needs extra mass at 5 Re: median excess +0.29 dex (x1.9) canonical, +0.26 alt.
- rho(excess, L_X/L_B) = +0.42 (p = 0.011, N = 30); partial given M* = +0.32 (p = 0.046) -> SUPPORTED under the cm05 rule (alt: +0.40, partial +0.30, p 0.054).
- BUT without the 9 group/cluster-dominant galaxies (M87, NGC 4472, 1399, 1316, 4374, 4649, 5846, 1407, 4636; list fixed in the script before the run,
  reported, no verdict) rho = +0.06 (N = 21). The hot-gas trend is carried by being a group/cluster central; among the other 21 there is no trend.
Reading: what the data support is "group/cluster centrals carry more extra mass" (the cm03 step: groups ~ clusters >> galaxies), not a hot-gas effect at
galaxy scale. LCDM predicts the same (central galaxies sit in group halos). The hot-halo hypothesis is NOT distinguished from environment.

## cm08: why ellipticals need ~1.9x -- the SAME two retention levels as the ledger
`cm08_etg_retained_fraction.py` (1/1; MUTATE no-phantom fails R; v1's check could not fail and was replaced before writing up). The cm07 excess as a retained
cold fraction f = (M_tot - M_law)/((Omega_c/Omega_b) M_b) at 5 Re (definition A, calibrated on X-COP 0.576):
- all 32: median 0.30 (canonical) / 0.28 (alt);
- the 9 group/cluster centrals: **0.64 / 0.59** -- the group (0.60, cm03 def B) and X-COP (0.576) level;
- the other 23 early types: **0.13 / 0.12** -- the galaxy level of the ledger (Milky Way 0.14, spirals <= 0.105) and C003's universal galaxy floor e^-n = 0.135 (L191).
Reading: the "1.9x" is not an elliptical-specific number. It is a mixture of two universal levels -- ~0.13 of the cosmic cold share in ANY galaxy
(spiral or elliptical) and ~0.6 in anything that is (or sits at the centre of) a group or cluster -- with the step between galaxy and group scale.
C003 gets the galaxy level right and the group level wrong (cm03). Nothing derives either number; 0.6 and 0.13 are measured, the mechanism is open.

## cm09 (POST HOC): the step follows HOST status, not the galaxy's own sigma
`cm09_sigma_split.py` (1/1; MUTATE shuffled sigma fails). Threshold sigma = 250 km/s declared in chat before the run.
2x2 medians (canonical): low-sigma non-central 0.13 (N 22); low-sigma CENTRAL 0.63 (NGC 1316, 4636, 5846 at sigma 198-231); high-sigma non-central 0.66 (N 1, NGC 4365);
high-sigma central 0.82 (N 6). Partial rho(f, sigma | central) = -0.04; partial rho(f, central | sigma) = +0.58 (alt the same).
Reading: the galaxy's own dispersion adds nothing once central status is known. If the cooling threshold is the cause, the relevant temperature is the HOST
halo's (group/cluster), not the galaxy's -- which makes the reading equivalent to "sits at the centre of a group-scale halo". NGC 4365 (the only high-sigma
non-central) dominates its own Virgo W' subgroup, so it is arguably a central too. LCDM predicts this step as well (centrals sit in group halos).

## cm10: the conservation budget and the step scale
`cm10_budget_and_scale.py` (1/1; MUTATE r = 1 fails B; v1's 1e-6 margin was defeated by the grid split and replaced). LCDM halo mass function
(colossus planck18, Tinker+08, M200m, z = 0): 0.589 of matter sits in halos > 1e9 Msun (0.367 > 1e12, 0.244 > 1e13, 0.100 > 1e14).
- **Budget:** with r_gal = 0.13 below the step and r_grp = 0.60 above, the halos hold only 0.19-0.25 of ALL cold mass (step 1e12-1e13), i.e. 0.32-0.42 of what
  LCDM halos hold; **75-81% of the cosmic cold mass must be diffuse (outside the measured apertures of any halo) today.** Conservation forces this; it is the
  two-level rule's sharpest consequence. Retentions are aperture values applied to whole halos (an approximation).
- **Scale:** the step lies between the Milky Way (1e12, galaxy level) and the lowest group-level hosts (~1e13): M200m 1e12-1e13 Msun, R200m 311-671 kpc,
  V200 118-253 km/s, T_vir 0.5-2.3e6 K -- the bracket of the classic cooling mass (Rees-Ostriker/Silk, ~1e12 Msun, ~1e6 K).
- **Anisotropies:** the primary CMB (z ~ 1100) cannot be affected -- the cold mass must be >= 0.988 clustered then (L129) and the sorting must be late (z <~ 2,
  forest). The late diffuse 75-81% would show in the SECONDARY anisotropies: CMB lensing power and the late ISW/tSZ, and in small-scale cosmic shear (S8).
  Those are the tests that can kill the two-level picture; not computed here.
