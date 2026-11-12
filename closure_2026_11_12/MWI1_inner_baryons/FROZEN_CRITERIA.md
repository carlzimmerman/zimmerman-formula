# MWI1 FROZEN CRITERIA: can published disc and bulge masses supply the Milky Way's inner baryons?

Committed alone, 2026-11-12, before any script. TEST lane. Adopts nothing. Relabels no other lane.
The published masses are web look-ups of abstracts and are PROVISIONAL. kappa = 1/2 FITTED; not
theory closed.

## Question

MWG1 (origin 2e09f262f6) left one open number: the rotation curve between 12 and 27 kpc asks for
total baryons of 8.39 to 8.75 x 10^10 Msun (canonical) or 7.70 to 8.07 x 10^10 (alt) inside those
radii, against the McMillan census of 6.68 x 10^10, and hot halo gas supplies under a tenth of the
difference. Is the stellar mass this requires inside the range of published Milky Way inventories?

## Disclosed before freezing

Hand values were formed before this file was written, from the numbers below: the required stellar
mass is about 7.05 to 7.41 (canonical) and 6.36 to 6.73 (alt) x 10^10; against Licquia and Newman
the lower end sits about +0.85 / +0.25 sigma, against McMillan +2.8 / +1.6, against Cautun
+4.7 / +3.1, against Imig plus a bulge +4.1 / +0.85, and Lian's is lower by a factor of more than
two. The lane records this with a fixed rule and adds the geometry check, which has not been
computed.

## The need

Required stellar mass = (A x 6.681 x 10^10) - cold gas - hot gas inside 27 kpc, with A in
[1.256, 1.310] (canonical) or [1.152, 1.208] (alt) from the record (hunt item 35), cold gas
1.191 x 10^10 (McMillan's HI and H2 discs as ported in DW1) and hot gas 0.15 x 10^10 (MWG1, Miller
and Bregman).

## Published inventories (total stellar mass; the error used is the one toward the need)

| id | source | stellar mass [10^10 Msun] | error upward |
|---|---|---|---|
| LN15 | Licquia and Newman 2015, meta-analysis, Kroupa IMF | 6.08 | 1.14 |
| McM17 | McMillan 2017 (the census the record uses; statistical error) | 5.43 | 0.57 |
| C20 | Cautun et al. 2020 | 5.04 | 0.43 |
| I25 | Imig et al. 2025 disc 5.27 (+0.2, -1.5) plus Licquia and Newman's bulge and bar 0.91 +- 0.07 | 6.18 | 0.21 |
| L25 | Lian et al. 2025 (an erratum is listed; its content was not found) | 2.607 | 0.363 |

Bland-Hawthorn and Gerhard 2016 is not graded: its abstract gives no number.

## Rule

For each inventory and footing, z = (lower end of the required stellar mass - published mass) /
upward error. **SUPPLIED** if z <= 1; **WITHIN 2 SIGMA** if 1 < z <= 2; **NOT SUPPLIED** if z > 2.

Lane label per footing: **SUPPLIED BY k OF 5**, naming them, followed by the class at the census the
record uses (McM17).

## Reported, not graded: geometry

The rotation-curve need was fitted as a uniform scaling. At fixed stellar mass, a different disc
scale length changes the in-plane baryonic force at 12 to 27 kpc. With the McMillan model (bulge,
gas discs and vertical profiles unchanged; stellar discs' masses held fixed) the thin and thick disc
scale lengths are both set to 2.15, 2.37, 2.71, 3.0 and 3.5 kpc, and the ratio of the in-plane
Newtonian force to the McMillan value is printed at 12, 16, 20, 24 and 27 kpc. This says how much of
the need (0.256 to 0.310 in amplitude on canonical) geometry could cover without more mass.

## Known-answer checks (before any label)

| id | check | pass condition |
|---|---|---|
| KA1 | the census as ported | stars 5.49 x 10^10, cold gas 1.191 x 10^10, total 6.681 x 10^10, each within 0.2 per cent |
| KA2 | the in-plane force routine | r g_R / (G M_b) = 1.0599, 1.0614, 1.0586 at 20, 25, 30 kpc (DW1's committed output), each within 0.003 |
| KA3 | the required stellar mass | 7.05 to 7.41 (canonical) and 6.36 to 6.73 (alt), each within 0.02 |

## Mutation (must bite)

M1: the excess amplitude (A - 1) halved. At least one inventory must change class on each footing.

## What a label will and will not mean

Published stellar masses differ by more than a factor of two and depend on the IMF, the disc
profile and the bulge definition. SUPPLIED says the framework's requirement is inside one
published inventory's error bar, not that the Galaxy has that mass. The requirement itself is the
record's fit, not recomputed here.
