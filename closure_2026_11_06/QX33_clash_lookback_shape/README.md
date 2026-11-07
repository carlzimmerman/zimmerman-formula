# QX33: CLASH lookback (z 0.19-0.70), where the law's missing mass sits and whether it changes with z. NO VERDICT (MUTATE A no bite: no power)

Kappa = 1/2 FITTED; not theory closed. Adopts nothing. Criteria 5741430147, pushed before any number.
Script: qx33.py (seconds). Outputs: qx33.json/.out, run_main.txt.

Data: 20 CLASH clusters, 84 points at 14-600 kpc (Tian+2020).
- g_tot comes from lensing. g_bar is gas plus the BCG's stars, and the table does not split the two.
- Redshifts are from MCXC by position. MACS0416 is the one exception: it takes z = 0.396 (Postman+2012), entered by hand.
- The split is 7 clusters at z >= 0.40 (HIGH) and 13 below (LOW).

The statistic is s, the slope of log(M_need/M_b) against log r, fitted per cluster. If s < 0, the missing mass is more
concentrated than the baryons.

## Label: NO VERDICT on both footings, because a control failed

MUTATE A injects a 0.3 slope change into the HIGH clusters. It reads Delta_s -0.30 but p only 0.07 (canonical) and 0.067
(alt), short of the 0.05 needed. With 7 against 13 clusters, and a per-cluster scatter in s of about 0.2, the sample cannot
detect a shape change of 0.3. The numbers below are reported, not graded.

| | canonical | alt |
|---|---|---|
| s, HIGH, median [95%] | +0.164 [-0.038, +0.213] | +0.156 [-0.042, +0.204] |
| s, LOW | +0.087 [-0.108, +0.233] | +0.075 [-0.125, +0.223] |
| Delta_s HIGH-LOW (p; 95% null half-width) | +0.077 (0.68; 0.23) | +0.081 (0.65; 0.23) |
| Delta A200 at 200 kpc (p; half-width) | +0.038 (0.56; 0.12) | +0.036 (0.55; 0.12) |
| Spearman of s with z, of A200 with z | -0.04, -0.04 | -0.04, -0.03 |
| without r < 50 kpc: s HIGH / LOW | -0.110 / -0.077 | -0.127 / -0.099 |

On their own frozen rules the numbers read UNRESOLVED (Q1) and NO EVOLUTION DETECTED (Q2).
The MUTATE B check (+0.5 slope in every cluster) does bite: Q1 moves to LESS CONCENTRATED.

## What the numbers say (reported)

1. **There is no redshift trend.** From z ~ 0.25 to z ~ 0.5 the missing-mass amplitude at 200 kpc is the same to within
   0.12 dex (95%), and the shape is the same to within 0.23. Any change of the missing mass with time over the last ~5 Gyr is
   at most about 30% in amplitude in this sample.
2. **The shape sits between the gas and the stars plus gas, at both epochs.**
   - With the BCG-dominated point inside 50 kpc included, s is about +0.15. The missing mass is less concentrated than the
     BCG's stellar cusp.
   - Without it, s is about -0.1, with the median on the more-concentrated side in both halves. Past the BCG, where the
     baryons are mostly gas, the missing mass is at least as concentrated as the gas.
   - Both readings sit inside the noise per half. Together, they match the near-z clue from X-COP (QX7 iter_7): the mass is
     more concentrated than the hot gas, does not follow the BCG cusp, and is nearest to the gas plus stars outside the core.

## Controls

- K1, the exact inverse: 2.7e-16. PASS.
- K2, the parse gives 84/20 and every cluster's z is matched. PASS.
- K3, the Newton limit: 1e-16 dex. PASS.
- MUTATE B: BITES.
- MUTATE A: NO BITE (p 0.07). This is a power failure, not a code fault.

## What it would take

A Delta_s of 0.3 needs about 2x the clusters per half at this per-cluster scatter. Possible sources:
- the full CLASH-like lensing sets, LoCuSS and HSC-XXL;
- a gas-only versus stars split, so that the gas-versus-stars + gas question becomes direct.
