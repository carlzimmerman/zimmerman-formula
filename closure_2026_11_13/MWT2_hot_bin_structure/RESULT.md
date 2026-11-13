# MWT2 RESULT: is RAW1's hot 30-40 kpc bin a structure?

2026-11-13. TEST lane. Adopts nothing, relabels nothing (RAW1, MWT1 keep their labels), registers nothing.
Criteria `FROZEN_CRITERIA.md` (commit 163d74faa3, alone, before any script or number). One amendment,
`AMENDMENT_A1.md` (6ee1e86a47, alone, POST HOC: written after a B = 30 debug smoke run, not blind to the 30-40 bin).
Graded run as frozen: `mwt2.out`, `mwt2_results.json`, `mwt2_MUTATE.out` (B = 1,000). A1 reading: `mwt2_A1.out`,
`mwt2_A1_results.json`, `mwt2_A1_MUTATE.out`. Post hoc look at the cold component: `mwt2_posthoc_group.out`.
Line: the framework's no-field line (RAW1's field reading, external field dropped), a0 = 9.36e-11 (canonical) /
1.13e-10 (alt) m/s^2, raw1_model.py's values, so the known answer matches exactly.

## Labels

As frozen (and identical under A1), every case, every bracket:

| case | label |
|---|---|
| **FW census, canonical** | **NO POWER** |
| **FW census, alt** | **NO POWER** |
| FW rc, canonical | NO POWER |
| FW rc, alt | NO POWER |

Why: mutation G (40 planted stars at +150 km/s, dispersion 15 km/s, on one 27 deg sky patch, PMs offset by 60 km/s)
is found by the mixture step, but the identity step does NOT call it a distinct group. As frozen, the SKY family
p is 0.15. Under A1, which adds a nearest-neighbour clustering test and a Lambda_Sgr test, it is 0.084. No other
family separates. So the frozen rule "distinct group = two families at p < 0.01" cannot recognise a real group of
this size with these data, and a "not distinct" verdict on the real bin carries no weight.

What the steps say about the real bin, as information and not as a label: 30-40 kpc HAS TWO COMPONENTS (the only
bin that does). The second component is cold, sits at large negative velocity and holds 12 per cent of the stars.
It does not separate from the rest in sky, distance, [Fe/H] or tangential motion at the frozen level. Without the
power rule the frozen reading would be "HOT BIN IS ONE POPULATION (step b)". Setting the cold component aside
(forced) passes the hot bin in all four cases.

## (a) One Gaussian against two, every bin (v_gsr, quoted errors deconvolved; floor 5 km/s; B = 1,000)

| bin | N | one Gaussian mu / sigma | cold comp. w / mu / s [68%] | other comp. w / mu / s [68%] | LR | null 99% | p | verdict |
|---|---|---|---|---|---|---|---|---|
| 20-30 | 865 | +1.2 / 97.2 | 0.011 / -225 / 23 | 0.989 / +3.8 / 94.7 | 3.41 | 15.0 | 0.857 | one (and w < 0.10) |
| **30-40** | 264 | +0.2 / 106.7 | **0.118 [0.09, 0.15] / -168.2 [-177, -160] / 20.3 [14, 24]** | **0.882 / +22.7 [+16, +30] / 92.5 [87, 96]** | **26.71** | 14.6 | **0.0010** | **TWO COMPONENTS** (31 stars) |
| 40-55 | 241 | +6.3 / 92.6 | 0.083 / +12 / 5.0 (floor) | 0.917 / +5.8 / 96.7 | 10.21 | 14.2 | 0.079 | one |
| 55-80 | 125 | -21.6 / 95.3 | 0.084 / -66 / 9 | 0.916 / -17.4 / 98.5 | 3.43 | 13.4 | 0.745 | one |

Brackets for 30-40: TWO at p < 0.05 and at p < 0.001, at minor weight 0.05, and at floors 3 and 10 km/s (p 0.0033,
B = 300). It is one component at minor weight 0.15 (0.118 < 0.15). The other bins are one component under every
bracket. MWT1's cold group in 40-55 (24 stars, 9 km/s) shows only as a floor-limited 8 per cent component at
p 0.08. So the flat top MWT1 saw at 30-40 is not a symmetric split. It is a cold lump at about -170 km/s beside
a halo of dispersion 92.5. That is not what I expected (I expected two near-equal Gaussians at +/- 80).

## (b) Identity of the 30-40 cold component (graded; cores q >= 0.8: 24 cold / 222 halo)

| family | tests (permutation p) | family p, as frozen / A1 |
|---|---|---|
| SKY | mean vector 0.200; KS abs(B_Sgr) 0.057; A1: 5-NN clustering 0.329; KS Lambda_Sgr 0.035 | 0.113 / 0.138 |
| DISTANCE | KS r 0.175 (medians 35.8 / 33.9 kpc) | 0.175 / 0.188 |
| CHEMISTRY | KS [Fe/H] 0.247 (medians -2.22 / -2.11) | 0.247 / 0.224 |
| TANGENTIAL | KS v_phi 0.290; KS v_t 0.884 | 0.580 / 0.574 |

Not a distinct group: no family is below 0.01, nor below 0.05. The forced identity test on 40-55's floor-limited
component (14 stars, not TWO COMPONENTS) does separate in SKY 0.002 and DISTANCE 0.0005 ([Fe/H] 0.013, v_phi
0.007). That is MWT1's real cold group in 40-55, which the mixture step does not pick up as a component.

Post hoc (`mwt2_posthoc_group.out`, not graded): 10 of the 24 cold-core stars form a tight clump in the southern
Galactic sky (l 45-96, b -26 to -54; Lambda_Sgr 26-78, B_Sgr -16 to -49; r 31-39 kpc; v_gsr -160 to -190). Three
more sit together at l 264-272, b +50 to +55. The rest are scattered. Only 54 per cent of the cold core is in the
north, against 73 per cent of the halo core. A southern clump with a common velocity is what unmixed debris looks
like. The file cannot say what it is (Sagittarius material off its band is one candidate), and the frozen tests,
which dilute the clump with the 14 scattered members, do not call it a group.

## (c) Consequence: RAW1's f with the smooth component only (every bin, all forced: no bin is a DISTINCT GROUP)

Graded words are RAW1's own in every bin and case, because no bin qualified. RAW1-passing bins that change: none.
Forced values: c1 is the mixture f, c2 the same with alpha recounted without the group's stars (30-40: alpha
5.289 -> 5.507), c3 is hard removal. Shown are the A1 values, with the group dispersion bounded. As frozen, c1 is
the same at 30-40 but degenerate (sigma_f 0.7 to 2.8) in the bins with no real second component.

| case | 20-30 RAW1 -> c1 | 30-40 RAW1 -> c1 / c2 / c3 | 40-55 RAW1 -> c1 | 55-80 RAW1 -> c1 |
|---|---|---|---|---|
| FW census can | 1.095 H -> 1.066+/-0.039 P | **1.205 H -> 1.044+/-0.064 P / 1.072 P / 0.996 P** | 1.052 P -> 1.098 P | 1.090 P -> 1.127 P |
| FW census alt | 1.052 P -> 1.025 P | **1.155 H -> 1.001+/-0.061 P / 1.028 P / 0.955 P** | 1.007 P -> 1.052 P | 1.043 P -> 1.078 P |
| FW rc can | 1.028 P -> 1.001 P | 1.135 H -> 0.983 P / 1.009 P / 0.938 P | 0.992 P -> 1.036 P | 1.030 P -> 1.065 P |
| FW rc alt | 1.012 P -> 0.986 P | 1.114 H -> 0.966 P / 0.991 P / 0.921 P | 0.972 P -> 1.015 P | 1.007 P -> 1.042 P |
| H (DESI NFW) | 1.068 P -> 1.040 P | 1.142 H -> 0.990 P | 0.997 P -> 1.041 P | 1.050 P -> 1.086 P |
| N (Newton) | 2.064 H -> 2.005 H | 2.662 H -> 2.289 H | 2.664 H -> 2.785 H | 3.164 H -> 3.277 H |

Forced, the cold component carries the whole 30-40 excess in every smooth model, DESI's NFW included. Nothing goes
COLD. In 20-30 the forced mixture removes a 1 per cent tail at -225 km/s (about 10 stars), which cools census
canonical from HOT to PASS. That is outlier trimming, not a detected group.

## Controls

- K0: RAW1 reproduced exactly (counts, sigma_los, alpha 5.2886, beta 0.6586, every f and sigma_f; max diff 0).
  K1a: mixture f with w = 0 equals RAW1's fit_f to 1e-8. K1b: the two-Gaussian fitter recovers a synthetic mixture
  within 3 bootstrap sigma. K2 SI: g(30 kpc) = 3.611e-11 m/s^2, M = g r^2 / G = 2.331e11 Msun, V = 182.8 km/s.
- Shuffle twin (velocities shuffled between bins, 20 shuffles, 80 bin-tests): 1 TWO COMPONENTS (allowed 3), 0
  distinct (allowed 1). PASS.
- Mutation S (scatter only, +N(0, 50)): not flagged (p 0.64). f rises 1.052 -> 1.181, so plain extra scatter heats
  a bin without any group signature. PASS.
- **Mutation G (moving group): FAILS.** Step (a) finds it (LR 40.1, p 0.002, w 0.168, mu +151, s 15.7; 39 of 40
  planted stars at q > 0.5, plus 20 halo stars). Step (c) restores the bin (smooth f 1.038 against the un-mutated
  1.052; A1 sigma_f 0.058). Step (b) does not call it distinct (SKY 0.15 / 0.084; nothing else). Hence NO POWER.
- Reproducibility: the A1 run reproduces every step (a) number and the twin byte for byte (same seeds).

## What the file cannot tell

- The identity step is weak by construction. The DESI footprint is concentrated, so sky tests lose power. PM
  errors at 30-55 kpc are 26-60 km/s against tangential dispersions near 55, which blunts the tangential tests.
  [Fe/H] for BHB stars is broad (-3.1 to -1.5 in both components). A planted 40-star group failed.
- No Sagittarius stream model is used. Lambda_Sgr and B_Sgr are positions only, so "Sgr debris" cannot be tested
  against a predicted velocity track.
- The mixture uses plain Gaussians in v_gsr. The Jeans prediction varies a little within the bin (sin eta, r).
  Errors are the quoted ones (MWT1's scale 1.31 is negligible at about 2 km/s).
- The mutation planted stars on duplicated positions; a real group with a distinct distance or metallicity would be
  easier to identify than the planted one.

## What this does to "Milky Way halo stars fail hot"

The hot 30-40 kpc bin is not a smooth Gaussian halo. Of the four bins, it alone needs a second component. That
component is a cold lump of about 30 stars (12 per cent) moving at -170 km/s with a 20 km/s spread, and part of
it clumps on the southern sky. Setting it aside brings every smooth model to f within 1 sigma of 1 at 30-40, the
framework's census line on both footings included (1.044 / 1.001), and leaves no passing bin failing. But the
lane's own rule for calling it a separate population could not recognise a planted group of the same kind, so
the data cannot certify that the lump is unmixed debris rather than part of the halo's own velocity
distribution. The fair statement is now this. The single hot bin rests on about 30 cold, fast-approaching stars.
Whether they are a structure is not decided by this file, so "the halo stars fail hot" rests on an
unidentified lump, not on the bulk of the bin. This is not a pass of the framework, and DESI's NFW behaves the
same way.

## Files and run

`FROZEN_CRITERIA.md`, `AMENDMENT_A1.md`, `mwt2.py`, `mwt2.out`, `mwt2_results.json`, `mwt2_MUTATE.out`,
`mwt2_A1.py`, `mwt2_A1.out`, `mwt2_A1_results.json`, `mwt2_A1_MUTATE.out`, `mwt2_posthoc_group.py`,
`mwt2_posthoc_group.out`. Data: RAW1's `MWS_BHB.fits` (sha256 5669c821...5246, not in the repository; checked by
the script). Run: `python3 -I -B mwt2.py <MWS_BHB.fits>` (about 12 minutes, one thread). A B = 30 debug smoke run
preceded the graded run; its output was overwritten and is not graded.

**Commit ids and the lead's re-run (added 2026-11-13, after landing; no number or label changes).** Local: criteria
163d74faa3, amendment A1 6ee1e86a47, graded run cc0fa0daa9, A1 run 68ec383aae, RESULT a28187ea71 (origin tip
fe656291c7). Pushed. The lead session re-ran `mwt2.py` from a copy with the same catalogue: `mwt2_results.json` and
`mwt2_MUTATE.out` are equal byte for byte; `mwt2.out` differs in 12 lines that were not traced line by line. The A1
script was not re-run. A reproduction, not an independent re-grade.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
