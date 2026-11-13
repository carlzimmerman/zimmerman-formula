# RRL1 RESULT: the halo's density slope from RR Lyrae, and RAW1's test redone with it

2026-11-13. TEST lane. Adopts nothing, relabels nothing (RAW1, MWT1, MWT2 keep their labels), registers nothing.
Criteria `FROZEN_CRITERIA.md` (commit 59ab8ca9fa, alone, before any script or number). No amendment. One graded run
(`rrl1.out`, `rrl1_results.json`, mutations in `rrl1_MUTATE.out`); a second run reproduced all three files byte
for byte. Line: the framework's no-field line (RAW1's field reading, external field dropped), a0 = 9.36e-11
(canonical) / 1.13e-10 (alt) m/s^2 from raw1_model.py, so the known answer matches exactly.

## Labels (as frozen)

| case | label | fragility |
|---|---|---|
| **FW census, canonical** | **MEASURED SLOPE MAKES A PASSING BIN FAIL [40-55 COLD]** (30-40 passes: 1.205 -> 1.052) | FRAGILE: score > 0.9 and distances x1.05 give NO POWER; no Sgr band gives FAIL SURVIVES (20-30 COLD); the single-law bracket gives FAIL SURVIVES (30-40 HOT, 1.125) |
| **FW census, alt** | **MEASURED SLOPE MAKES A PASSING BIN FAIL [40-55 COLD]** (30-40 passes: 1.155 -> 1.008) | FRAGILE: the single-law bracket gives FAIL REMOVED |
| FW rc, canonical | MEASURED SLOPE MAKES A PASSING BIN FAIL [40-55 COLD] (30-40: 1.135 -> 0.991) | FRAGILE: the single-law bracket gives FAIL REMOVED |
| FW rc, alt | MEASURED SLOPE MAKES A PASSING BIN FAIL [40-55 COLD] (30-40: 1.114 -> 0.973) | robust |

DESI's NFW (H), reported: RAW1's hot 30-40 bin passes (1.142 -> 1.002) and 40-55 goes COLD (0.997 -> 0.820),
exactly like the framework line. Newton stays HOT in every bin. So the swap moves every smooth model the same way;
it singles out no model. The hot bin is gone in every case, but a passing bin breaks the other way. The sample
does NOT give "fail removed".

## The measured slope

PS1 (Sesar+17 RRab, score > 0.8, |b| > 20, Sgr band |B| >= 15 masked, clumps masked, paper's completeness folded
in, q = 1, 20 <= r < 80 kpc; 5,143 cells, 13,100 deg^2, N = 5,421):
- single: **4.770 [4.731, 4.809]**
- broken: **inner 5.293 +/- 0.077, outer 3.934 +/- 0.115, break 39.0 +/- 1.2 kpc**. 2 dlnL = 78.1 against the
  bootstrap threshold T = 9.45 (99th percentile of 100 null mocks; median 2.4). **Break DETECTED.** The halo is
  steep inside about 39 kpc and shallower beyond.

The clustering rule flagged 3,077 stars and masked 442 cells (about 8 per cent of the footprint). It picked up the
Sgr core edge (RA 287-295, Dec -29, 27 kpc), Draco (260, +58, 75 kpc), Ursa Minor (227, +67, 68 kpc) and Sextans
(153, -2, 82 kpc). It also flagged a chain of 5-16-star groups at RA 219-233, Dec -4 to -13, 49-56 kpc, which is
not identified here.

DES Y6 (cross-check, 3,190 deg^2, flat completeness, 20-100 kpc, N = 1,045):
- single **4.901 [4.820, 4.983]**
- broken fit: break at the range edge (76.8 kpc) with an unconstrained outer slope (1.2 +/- 1.3). 2 dlnL 11.35
  against its own T 9.04, so "detected" by the rule but degenerate.
- 20-80 kpc: single 5.056 [4.962, 5.151], no break (2 dlnL 1.8).
- My fit at the paper's set-up (q 0.7, 9-100 kpc): break 18.4, inner about 0, outer 4.45. It does NOT reproduce
  the paper's 32.1 / 2.54 / 5.42. My DES footprint (occupancy-filled cells) and flat completeness are cruder than
  the paper's, and below 20 kpc the inner-halo region the paper fits differently dominates.

What one small footprint can and cannot show: DES sees about 1,000 stars beyond 20 kpc in one southern patch.
It measures a single slope (4.9-5.1) but cannot place a break between 20 and 80 kpc. Its broken fits sit on range
edges.

**Comparison (published numbers PROVISIONAL):**

| source | form | values |
|---|---|---|
| Sesar+17 (read) | no profile fit | — |
| Hernitschek+18, PS1 RRab (memory, NOT re-read) | single, no break | about 4.4, q about 0.92, 20-130 kpc |
| Stringer+21, DES (read twice) | broken, q fixed 0.7 | break 32.1, inner 2.54, outer 5.42 |
| this lane, PS1 | broken, q = 1 | break 39.0, inner 5.29, outer 3.93 |
| DESI BHB, RAW1 | single | 5.29 +/- 0.17 |
| DESI BHB, MWT1 | break fixed at 30 | inner 5.71, outer 4.33 +/- 0.48 (not detected) |

The PS1 shape (steep, then shallower) has the same sense as the DESI sample's own weak hint (MWT1). It is the
OPPOSITE of DES's published shallow-then-steep law. My single PS1 slope (4.77) is steeper than the 4.4 I recall
for Hernitschek+18. That recollection is unchecked.

## RAW1's statistic with RAW1's slope and with the measured one (f +/- sigma_f, word)

Measured profile: broken PS1 (5.29 to 39.0 kpc, 3.93 beyond, extrapolated). sigma_f includes s_slope, from 200
draws of the fit covariance (0.006-0.020).

| case | slope | 20-30 | 30-40 | 40-55 | 55-80 |
|---|---|---|---|---|---|
| FW census can | RAW1 5.289 | 1.095+/-0.035 HOT | **1.205+/-0.058 HOT** | 1.052+/-0.053 PASS | 1.090+/-0.106 PASS |
| | RR Lyrae | 1.058+/-0.027 HOT | **1.052+/-0.048 PASS** | **0.857+/-0.044 COLD** | 0.887+/-0.111 PASS |
| FW census alt | RAW1 | 1.052+/-0.034 PASS | **1.155+/-0.056 HOT** | 1.007+/-0.051 PASS | 1.043+/-0.102 PASS |
| | RR Lyrae | 1.016+/-0.026 PASS | **1.008+/-0.046 PASS** | **0.820+/-0.042 COLD** | 0.849+/-0.107 PASS |
| FW rc can | RAW1 | 1.028+/-0.033 PASS | 1.135+/-0.055 HOT | 0.992+/-0.050 PASS | 1.030+/-0.100 PASS |
| | RR Lyrae | 0.994+/-0.025 PASS | 0.991+/-0.045 PASS | 0.809+/-0.042 COLD | 0.838+/-0.105 PASS |
| FW rc alt | RAW1 | 1.012+/-0.032 PASS | 1.114+/-0.054 HOT | 0.972+/-0.049 PASS | 1.007+/-0.098 PASS |
| | RR Lyrae | 0.979+/-0.025 PASS | 0.973+/-0.044 PASS | 0.792+/-0.041 COLD | 0.820+/-0.103 PASS |
| H (DESI NFW) | RAW1 | 1.068+/-0.035 PASS | 1.142+/-0.055 HOT | 0.997+/-0.050 PASS | 1.050+/-0.099 PASS |
| | RR Lyrae | 1.032+/-0.026 PASS | 1.002+/-0.045 PASS | 0.820+/-0.042 COLD | 0.868+/-0.101 PASS |
| N (Newton) | RAW1 | 2.064 HOT | 2.662 HOT | 2.664 HOT | 3.164 HOT |
| | RR Lyrae | 2.026 HOT | 2.410 HOT | 2.272 HOT | 2.698 HOT |

The 30-40 bin is HOT in 0 of 200 draws in every framework case, so NO POWER does not apply. Census canonical also
keeps 20-30 HOT (1.058 +/- 0.027, 2.1 sigma), because the inner slope equals RAW1's.

Mechanism. The Jeans integral at 30-40 kpc reaches past the break into the shallower outer law. That raises the
predicted dispersion. At 40-55 kpc the whole integral is in the shallow law, and the observed stars (sigma_los
92.6 km/s) are then 14-21 per cent colder than predicted.

DES profile in the same step (reported, not graded): its edge break (outer 1.2) makes the integral nearly diverge.
f = 0.26-0.92 with sigma 0.34-0.43, all PASS, and that means nothing.

## Brackets (each redoes the PS1 fit; f at 30-40 / 40-55 for FW census canonical and alt; label word)

| bracket | PS1 fit | census can 30-40 / 40-55 | census alt 30-40 / 40-55 | words that differ from nominal |
|---|---|---|---|---|
| completeness none | 5.28 / 4.03 / 38.8 | 1.062 / 0.873 C | 1.018 / 0.835 C | none |
| completeness steeper | 5.30 / 3.36 / 40.8 | 0.995 / 0.759 C | 0.953 / 0.727 C | none (55-80 also COLD for alt and rc) |
| score > 0.6 | 5.25 / 3.35 / 39.9 | 0.976 / 0.758 C | 0.936 / 0.726 C | none (rc alt 30-40 COLD) |
| score > 0.9 | 5.30 / 4.20 / 38.9 | 1.086 / 0.898 C | 1.041 / 0.860 C | census can NO POWER |
| abs(b) > 30 | 5.34 / 3.62 / 39.3 | 1.013 / 0.804 C | 0.971 / 0.770 C | none |
| no Sgr band | 4.11 / 4.75 / 47.6 | 1.055 / 0.966 P | 1.011 / 0.925 P | census can FAIL SURVIVES (20-30 COLD); others still MAKE A PASSING BIN FAIL (20-30 COLD) |
| Sgr band 10 | 5.07 / 3.96 / 37.8 | 1.033 / 0.862 C | 0.990 / 0.825 C | none |
| Sgr band 20 | 5.33 / 4.02 / 40.2 | 1.078 / 0.871 C | 1.033 / 0.833 C | none |
| distances x0.95 | 5.47 / 3.85 / 36.9 | 1.021 / 0.843 C | 0.979 / 0.807 C | none |
| distances x1.05 | 5.05 / 4.15 / 41.7 | 1.087 / 0.892 C | 1.042 / 0.854 C | census can NO POWER |
| q = 0.7 | 4.84 / 0.56 / 75.0 (edge) | 0.262 / 0.135 C | 0.250 / 0.129 C | none in word. The fit is degenerate (break on the edge, outer slope unconstrained) and its f is meaningless |
| single law (4.77) | — | **1.125 H** / 0.982 P | 1.079 P / 0.940 P | census can FAIL SURVIVES (30-40 HOT); census alt and rc can FAIL REMOVED; rc alt still MAKES A PASSING BIN FAIL (20-30 and 40-55 COLD) |

The break is detected in every bracket (2 dlnL 22-176 against T 9.45). The outer slope is the soft number. It
ranges from 3.35 to 4.20 with completeness and score cut, and fainter, less pure samples give a shallower outer law.
So part of the flattening may be contamination or completeness at the faint end, which these tables cannot settle.
Without the Sgr band mask the shape REVERSES (4.11 inside 47.6 kpc, 4.75 beyond). Sgr debris dominates the
unmasked counts at 20-50 kpc. So the result depends on how the stream is removed, and a 10-20 deg band is a crude
removal.

## The same-profile assumption, and its one check

Assumption: the BHB stars (which carry the velocities) and the RR Lyrae (which carry the density) follow the same
radial number-density profile.

Check from the data on disk: PS1 RR Lyrae restricted to the 1,033 sky cells that hold RAW1's BHB stars, 20-45 kpc,
N = 996, single slope **5.139 [4.994, 5.285]**. RAW1's BHB alpha is 5.289 +/- 0.169. The difference is -0.15 +/- 0.22
(-0.7 sigma): **CONSISTENT**. As frozen, this is necessary, not sufficient. It covers only the window where both
samples measure, inside the break.

In the same cells the broken fit prefers the opposite shape: inner 3.76, outer 5.75, break 25.6, 2 dlnL 9.8. No
threshold was computed for this sub-sample. The break is therefore not uniform across the sky, which is what
unmixed substructure would do.

## Known answers, twins, mutations

- K1: mock single 4.5 recovered 4.546 [4.508, 4.584]; no break (2 dlnL 7.27 < 9.45). PASS.
- K2: mock (3.0, 5.0, 35) recovered 3.01 +/- 0.15, 5.00 +/- 0.13, 35.3 +/- 1.7; detected (192). PASS.
- K3: RAW1's six cases reproduced with RAW1's slope, max difference 1.5e-10. MWT1's copied predP equals RAW1's
  sr2_at to 2e-14. PASS.
- K4: SI g(30 kpc) = 3.611e-11 m/s^2, M = g r^2 / G = 2.331e11 Msun, V = 182.8 km/s. PASS.
- T1: 1 of 50 fresh null mocks exceed T (allowed 3). PASS.
- T2: distance shuffle FAILS. The break survives: 5.09 / 3.96 / 43.8, 2 dlnL 42.5. The frozen expectation was
  that it would survive, because r is close to d at these radii, so the twin cannot separate a real break from
  one in the distance distribution. It does show that the break is a property of the distance distribution over
  the whole footprint, not of how distance pairs with sky position.
- **M1 FAILED TO BITE.** M1 thinned the stars beyond 40 kpc to 60 per cent. The detection fired (2 dlnL 52.6), but
  the fit put the break at 58.7 kpc with outer slope 2.36, not near 40 with a steeper outer law. The mutation
  planted a density STEP, which a continuous broken law cannot represent, so the frozen bite condition was badly
  posed. Recovering a slope change is shown by K2 instead.
- M2 bites: n proportional to r^-3.5 lowers f in every bin of every case.

## What was left out

- No Sgr stream model, only a band mask.
- Virgo and the unidentified 49-56 kpc chain were masked only where the clump rule caught them.
- No contamination model: purity is bracketed by the score cut only.
- The completeness of every score cut uses the 0.8-cut function.
- M_r = +0.6 for converting DM to r_F is from memory.
- No convolution with distance errors (3 per cent).
- q was not fitted, only bracketed. The q = 0.7 broken fit is degenerate.
- The Jeans step keeps RAW1's constant beta 0.66. MWT1 found beta 0.44 at 40-55 kpc and a real cold group there
  (24 stars). Neither is folded in, and both bear on the new COLD bin.
- The outer law is extrapolated beyond 80 kpc.
- DES is a crude cross-check: footprint from occupancy, flat completeness, and the paper's fit is not reproduced.
- Hernitschek+18 was not re-read.
- The first attempt to read Sesar+17 fetched the arXiv PDF URL, and the fetch tool saved a copy of the PDF in the
  session's tool-results area (outside the repository). It was not used. The numbers come from the ar5iv HTML page.

## What this does to "Milky Way halo stars fail hot"

Read with MWT1 and MWT2, the hot 30-40 kpc bin no longer stands alone. MWT1 showed it rests on a tracer slope
extrapolated beyond the BHB sample. MWT2 showed it rests on about 30 cold, fast-approaching stars. Here an
independent tracer (5,421 RR Lyrae over 13,000 deg^2, against 1,495 BHB stars) measures the slope directly. It
agrees with the BHB slope where both see, flattens beyond about 39 kpc, and with that the 30-40 bin passes in
every framework case and for DESI's NFW (1.205 -> 1.052 census canonical, 1.155 -> 1.008 alt). But the same slope
makes the next bin, 40-55 kpc, 3.2 to 5.1 sigma too COLD for every smooth model, so the Milky Way halo
stars do not pass. The fail moves from hot at 30-40 to cold at 40-55 and does not disappear. And the outer slope
that moves it is the least secure number here: it shifts with the score cut and completeness (3.35 to 4.20), and
it reverses when the Sagittarius band is not masked. A single RR Lyrae slope (4.77) removes the fail on alt and on
rc canonical, but not on census canonical. Fair statement: "the halo stars fail hot" is no longer a robust
statement about the framework, or about any smooth model. Whether the halo stars agree with any smooth Jeans model
at 30-55 kpc depends on the outer density slope and on substructure that none of these files resolves. This is
not a pass of the framework.

## Files and run

`FROZEN_CRITERIA.md`, `rrl1.py`, `rrl1.out`, `rrl1_results.json`, `rrl1_MUTATE.out`. Data (not in the repository,
sha256 checked by the script): PS1 table5_subset.tsv, DES table1.tsv, RAW1's MWS_BHB.fits. Run:
`python3 -I -B rrl1.py <PS1 tsv> <DES tsv> <MWS_BHB.fits>` (about 2 minutes, one thread). Commits: criteria
59ab8ca9fa, script and graded run 8bc8c2bee7. Not pushed. No independent re-grade exists.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
