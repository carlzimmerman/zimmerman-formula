# FWN1R RESULT_BLIND: how large f can be for the crossing-speed split at flux level, and the split with no settled radius

TEST lane: adopts nothing, relabels nothing, registers nothing. Criteria: FROZEN_CRITERIA.md (ed67b21129, committed alone). No
amendment. Built in my own FRZ6R build. Footings are never pooled. Cold dark energy is a gravitating field component; no particle
is added. kappa = 1/2 and 5.41 are FITTED. Nothing here says the data favour the framework.

## Labels

| case | canonical | alt |
|---|---|---|
| f = 5 | FOREST ROW FAILS AT FLUX LEVEL, FRAGILE (lambda_P x 2; gamma 1.2) | FOREST ROW FAILS AT FLUX LEVEL, FRAGILE (lambda_P x 2) |
| f = 10 | FOREST ROW FAILS AT FLUX LEVEL | FOREST ROW FAILS AT FLUX LEVEL |
| f = infinity (split, no settled radius) | FOREST ROW FAILS AT FLUX LEVEL | FOREST ROW FAILS AT FLUX LEVEL |
| control (law's layout everywhere, unsplit) | fails (D 323.0) | fails (D 395.8) |

- Every known answer passes, both twins bite, and no case has a known-answer or twin failure.
- **Reported, not a label: the ceiling on f.** D + 2 SE reaches 4 at f = 4.24 (canonical) and f = 4.07 (alt). The bracketing range,
  from D - 2 SE and D + 4 SE, is 4.17 to 4.39 (canonical) and 3.99 to 4.25 (alt).
  - These ranges hold only if ln(D + 2 SE) is linear in ln f between f = 3 and f = 5. That assumption, not the seed scatter, is
    the main uncertainty.
  - Bounds that do not depend on the interpolation form: f = 3 is below 4 (0.66 / 0.78) and f = 5 is above 4 (9.5 / 12.0). So the
    ceiling lies between 3 and 5 on both footings.

## D and SE (12 bins, 4 seeds in every bin, ratio of seed sums, delete-one jackknife over the seed index)

| case | canonical D | SE | D_noise (limit) | alt D | SE | D_noise (limit) |
|---|---|---|---|---|---|---|
| f = 2 (FRZ6R) | 0.0244 | 0.0032 | — | 0.0293 | 0.0035 | — |
| f = 3 (recomputed here = FRZ6R) | 0.572 | 0.044 | 0.0015 (0.4) | 0.691 | 0.047 | 0.0018 (0.4) |
| f = 5 | 8.83 | 0.33 | 0.039 (0.88) PASS | 10.90 | 0.56 | 0.049 (1.09) PASS |
| f = 10 | 194.5 | 5.2 | 0.37 (19.4) PASS | 288.0 | 6.8 | 0.39 (28.8) PASS |
| f = infinity | 215.0 | 5.2 | 0.36 (21.5) PASS | 314.7 | 7.3 | 0.45 (31.5) PASS |
| control | 323.0 | 4.5 | 0.92 (32.3) | 395.8 | 8.5 | 0.97 (39.6) |

- The f = 5 pull comes from z 2.2 to 2.8 (canonical per bin 2.92 / 1.89 / 1.25 / 0.47; alt 3.78 / 2.33 / 1.26 / 0.52).
  Above z 3.4 it is below 0.03.
- Most of the jump from f = 3 to f = 10 happens before f = 10. By f = 10 most slower haloes' settled radius is capped at r_ta:
  the f = 10 and f = infinity realised matter ratios at z 2.2 agree to the printed digit.
- The split with no settled radius sits at 67 % (canonical) and 80 % (alt) of the unsplit control.

## Brackets (12-bin estimate = D x anchor ratio, seeds 0 and 1)

| bracket | f 5 can / alt | f 10 can / alt | f inf can / alt |
|---|---|---|---|
| lambda_P x 0.5 (40 ckpc; NOT resolved by the grid) | 44.3 / 49.0 | 816 / 1003 | 949 / 1146 |
| lambda_P x 2 (158 ckpc) | **0.82 / 1.49** | 30.8 / 58.5 | 33.2 / 62.6 |
| gamma 1.2 | **2.63** / 4.02 | 112 / 144 | 122 / 154 |
| gamma 1.6 | 31.2 / 35.7 | 281 / 397 | 311 / 434 |
| tau_eff x 0.9 | 10.4 / 12.7 | 202 / 312 | 223 / 340 |
| tau_eff x 1.1 | 7.6 / 9.4 | 186 / 265 | 205 / 290 |

- Only f = 5 has brackets that cross 4: lambda_P x 2 (both footings) and gamma 1.2 (canonical; alt sits at 4.02).
- f = 10 and f = infinity stay above 4 in every bracket.

**Measured-range reading (lambda_P 91.4 to 138.6 comoving kpc; PROVISIONAL, from the lead's FRZ6R brief):**

| case | canonical D (91.4 / 138.6) | word | alt D (91.4 / 138.6) | word |
|---|---|---|---|---|
| f = 5 | 6.39 / 1.42 | FAILS / HOLDS | 7.49 / 2.08 | FAILS / HOLDS |
| f = 10 | 129.9 / 43.7 | FAILS / FAILS | 205.6 / 79.6 | FAILS / FAILS |
| f = infinity | 142.7 / 47.2 | FAILS / FAILS | 223.4 / 85.4 | FAILS / FAILS |

- So f = 5 changes sides within the measured smoothing range.
- f = 10 and infinity fail across all of it.

**Grid resolution.** The cell is 52.1 kpc/h = 77 comoving kpc.
- lambda_P x 0.5 is below one cell and is not resolved.
- The primary 79 ckpc is about one cell, so it is only marginally resolved.
- 91.4 to 158 ckpc span 1.2 to 2 cells.
- Pressure smoothing remains the strongest lever.

## Known answers (all PASS on both footings)

- **KA-INF.** For every z and footing, the f = infinity table equals the control's rows bitwise for every halo slower than v*,
  and the reference's rows for every faster halo. A field built from the row-by-row assembled table gives exactly the same flux
  at z 3.0 (deviation 0).
- **KA-3.** The recomputed R, J3 and C flux P1D equal FRZ6R's stored parts exactly (largest deviation 0, all 48 files per
  footing).
- **KA-C.** The control's D equals FRZ6R's exactly (323.0468 / 395.8263), and it fails.
- **KA-N.** The counts above v*(z) equal JNT2's at all 12 z.
- **KA-F.** The largest mean-flux miss is 2e-14.
- **KA-M.** Realised matter ratios match the halo model at the anchors. The worst row is f = infinity, z 2.2, k 5: 0.9265
  against 0.9419 (alt; tolerance 0.027).
- **KA-S.** Passes for every case.
- **Floored gas pixels.** At most 4e-4 in R, J5, J10, Jinf and C. The doubled-difference twin field reaches 3.6 %, which is
  reported and not a known answer.

## Twins (both bite)

| twin | canonical | alt | rule |
|---|---|---|---|
| TW-A boundary removed at f = infinity (control vs Jinf, 12-bin) | 323.0 +- 4.5 vs 215.0 +- 5.2, ratio 1.50 | 395.8 +- 8.5 vs 314.7 +- 7.3, ratio 1.26 | ratio >= 1.25 and resolved at 2 sigma: bites / bites |
| TW-B difference doubled at f = 10 (anchors) | 235.6 vs 61.0 (x 3.86) | 387.8 vs 99.4 (x 3.90) | >= 2.5: bites / bites |

- TW-A on the alt footing clears its 1.25 ratio threshold narrowly (1.26).

## Hand estimate against outcome

- **Estimated:** D(5) 3 to 20, D(10) 15 to 80, D(inf) 30 to 150; ceiling about 4 (3.5 to 6); twins bite.
- **Found:** 8.8 / 10.9, 194 / 288 and 215 / 315; ceiling 4.2 / 4.1; twins bite.
- f = 5 and the ceiling were inside the estimate. f = 10 and infinity came out 2 to 3 times higher than estimated: the response
  saturates later and higher than I guessed. Once the law's layout reaches the outskirts of haloes just under v*, most of what
  the forest sees in the control returns.

## What was left out

The same as FRZ6R:
- hydrodynamics, shock heating, self-shielding;
- UV and temperature fluctuations;
- peculiar velocities;
- halo clustering;
- haloes below 1e8 Msun/h;
- modes below the 20 Mpc/h box fundamental;
- form B's velocity changes.

The brackets are anchor-scaled estimates. The gas inputs are inherited and PROVISIONAL.

## Disclosures

- **Blindness held.** I opened nothing on either forbidden list, ran no `git log` beyond `-1`, and did not grep for the lane
  name. I saw no earlier answer.
- **Reuse.**
  - My own FRZ6R scripts, copied and adapted: f = infinity calls mode "B" directly; the assembled table; new case lists; the
    TW-B field.
  - FRZ6R's stored primary parts and its graded f = 2 D and SE, read read-only for KA-3 and the ceiling.
  - Through the build, as in FRZ6R: FRZ3R's FGPA functions, FZS1's layout prefix, `ss1_cosmo.forest_setup`, and JNT2's counts.
- **Compute.**
  - Two runners at once, under the pre-part disk and memory check, with exclusive claim files. Parts are seeded by (z, seed),
    so no number depends on scheduling.
  - Footprint-guard readings after each flux step were at most about 0.3 GB. ru_maxrss reads about 13 GB, which on macOS counts
    reusable pages.
  - No stop was triggered.
- **Commits.** The run logs are git-ignored and not committed.
- **Wall time.** About 1.6 h (03:50 to 05:25 EST).

## What it says about the forest row

At flux level the crossing-speed split keeps the forest row inside the gate only while the law's layout is confined well inside
the haloes. The 12-bin flux Delta chi^2 is about 0.6 at f = 3, 9 to 11 at f = 5, about 200 to 290 at f = 10, and 215 / 315 at
f = infinity.

The split with no settled radius fails on both footings. Its D is two-thirds to four-fifths of the unsplit law's, so the boundary
at v*(z) alone removes only a minority of the forest signal. The settled radius does most of the work.

D + 2 SE crosses the gate at about f = 4.1 to 4.2 on this build. The fiducial pressure smoothing is only marginally resolved, and
at f = 5 the answer moves to the other side of the gate within the measured smoothing range. So the ceiling is soft against the
gas inputs, while the fail at f = 10 and above is robust to every bracket.

These are hits and misses of one candidate rule, not a test passed by the theory.

## Commit ids, the lead's checks and the comparison with FWN1 (2026-11-14, written by the lead after this file landed)

- Criteria ed67b21129 (origin 51a550b8a7); scripts, parts and graded outputs eafc9a5b2b (origin fc2e01f040); result 994eab6169
  (origin 255cd46790).
- **Re-run.** The lead re-ran the grader from a copy at the same folder depth: `fwn1r_grade.json`, `fwn1r_grade.out` and both
  twin files equal byte for byte. The boxes were not re-run. A reproduction, not a further independent grade.
- **Blindness, checked on the commit-list route.** The lead's commits whose subjects carry FWN1's words were made at 03:57 to
  03:59 EST, after this lane's criteria (03:51) and before its scripts. The agent's session log shows `git log` was called three
  times in this lane, each `git log -1` straight after one of its own commits, and each showed only that commit.
- **Comparison with FWN1** (`closure_2026_11_13/FWN1_forest_flux_split_f_ceiling/RESULT.md`; canonical / alt):

  | case | FWN1 label | FWN1 D | this lane's label | this lane's D |
  |---|---|---|---|---|
  | f = 5 | NO VERDICT / NO VERDICT | 8.09 / 9.45 | FAILS, FRAGILE / FAILS, FRAGILE | 8.83 / 10.90 |
  | f = 10 | FAILS / FAILS | 184.3 / 233.5 | FAILS / FAILS | 194.5 / 288.0 |
  | no settled radius | FAILS / FAILS | 200.5 / 251.1 | FAILS / FAILS | 215.0 / 314.7 |

  - **f = 10 and no settled radius: the same word in both builds on both footings.** FWN1's fails are confirmed by a blind
    build, and neither build's fail is FRAGILE.
  - **f = 5: the same size, different words.** The two D values agree to about 10 to 15 %. FWN1's frozen SE (2.41 / 2.79) leaves
    D - 2 SE under 4; this lane's jackknife SE (0.33 / 0.56) puts it over, with the label FRAGILE, and its measured-range
    reading changes sides. f = 5 is therefore not a confirmed fail.
  - **Ceiling (reported in both, never a label).** FWN1: D + 2 SE reaches 4 at f 3.6 / 3.4 and D - 2 SE at 5.2 / 5.0. This lane:
    4.24 / 4.07. Both lie between the two run points, 3 and 5; f = 4 was run in neither build.
- No number or label of either lane changes.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
