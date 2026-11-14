# FRZ6R RESULT_BLIND: the crossing-speed split at flux level, blind independent re-grade

TEST lane: adopts nothing, relabels nothing, registers nothing. Criteria: FROZEN_CRITERIA.md (4314f23c90, committed alone).
Amendment: AMENDMENT_A1_2026-11-13.md (4265c14111, committed alone before any graded number). Footings are never pooled. Cold dark energy
is a gravitating field component; no particle is added. kappa = 1/2 and 5.41 are FITTED. Nothing here says the data favour the
framework.

## Labels

**As frozen: NO VERDICT for every case on both footings.** The only failing item is twin TW1, which does not bite. Every known
answer passes, twin TW2 bites, and D + 2 SE < 4 in every case.

| case | canonical (as frozen) | alt (as frozen) | A1 reading (reported, not the label) |
|---|---|---|---|
| f = 1.25 | NO VERDICT | NO VERDICT | NO VERDICT / NO VERDICT |
| f = 2 | NO VERDICT | NO VERDICT | NO VERDICT / NO VERDICT |
| f = 3 | NO VERDICT, FRAGILE (lambda_P x 0.5) | NO VERDICT, FRAGILE (lambda_P x 0.5) | NO VERDICT, FRAGILE (lambda_P x 0.5) / same |
| control (law's layout everywhere) | FAILS (D 323.0, SE 4.5) | FAILS (D 395.8, SE 8.5) | — |

- The frozen HOLDS rule needs both twins to bite. TW1 does not bite under the frozen rule, nor under AMENDMENT_A1's relative rule
  (see Twins), so no case can be HOLDS.
- No case comes near FAILS. The largest D - 2 SE is 0.60 (alt, f = 3).
- I re-checked the control: it fails, as required. Twin TW2 bites. TW1 does not.

## D, SE and the seed test (12 bins, 4 seeds per bin, ratio-of-seed-sums estimator, delete-one jackknife SE)

| case | canonical D | SE | D_noise (limit) | alt D | SE | D_noise (limit) |
|---|---|---|---|---|---|---|
| f = 1.25 | 0.00056 | 0.00024 | 1.9e-5 (0.4) PASS | 0.00130 | 0.00054 | 5.6e-5 (0.4) PASS |
| f = 2 | 0.0244 | 0.0032 | 7.6e-5 (0.4) PASS | 0.0293 | 0.0035 | 9.1e-5 (0.4) PASS |
| f = 3 | 0.572 | 0.044 | 0.0015 (0.4) PASS | 0.691 | 0.047 | 0.0018 (0.4) PASS |
| control | 323.0 | 4.5 | 0.92 (32.3) PASS | 395.8 | 8.5 | 0.97 (39.6) PASS |

- Where the pull comes from: z 2.2 and 2.4 carry nearly all of D. For f = 3 the per-bin values are 0.275 / 0.113 / 0.051
  (canonical, z 2.2 / 2.4 / 2.6), and below 1e-3 above z 3.2.
- The flux change for f = 3 at z 2.2 is -0.3 % at k_v 0.003 s/km and +0.3 % at 0.03 s/km. For f = 2 it is 0.07 % and 0.05 %.
  Above z 3 every split case moves the flux power by less than 1e-4.
- For comparison, the control at z 2.2 moves it by +3 to +7 % (canonical; up to +9 % alt).

## Brackets (12-bin estimate = D x anchor ratio, seeds 0 and 1)

| bracket | f 1.25 can / alt | f 2 can / alt | f 3 can / alt | control can / alt |
|---|---|---|---|---|
| lambda_P x 0.5 | 0.0051 / 0.0082 | 0.199 / 0.225 | **4.29 / 4.29** | 1161 / 1353 |
| lambda_P x 2 | 3e-6 / 1e-5 | 0.0010 / 0.0013 | 0.030 / 0.039 | 89 / 107 |
| gamma 1.2 | 3e-6 / 1e-5 | 9e-5 / 4e-5 | 0.0059 / 0.0059 | 264 / 254 |
| gamma 1.6 | 0.0012 / 0.0028 | 0.068 / 0.079 | 1.82 / 2.13 | 456 / 545 |
| tau_eff x 0.9 | 0.0007 / 0.0016 | 0.030 / 0.036 | 0.68 / 0.83 | 339 / 429 |
| tau_eff x 1.1 | 0.0005 / 0.0011 | 0.020 / 0.024 | 0.49 / 0.58 | 308 / 366 |

- Only f = 3 at lambda_P x 0.5 (40 comoving kpc) crosses 4, on both footings, hence FRAGILE. At that smoothing the 384^3 grid
  (dx 52 kpc/h) does not resolve the scale, so that bracket is also the least reliable one.
- Pressure smoothing is the strongest lever by far. Reducing it raises D steeply; raising it collapses D.

**Measured-range reading (lambda_P 91.4 to 138.6 comoving kpc; PROVISIONAL range from the lead's brief):**

| case | canonical D | alt D | word at both ends |
|---|---|---|---|
| f = 1.25 | 5e-6 to 1.0e-4 | 1.6e-5 to 6.0e-4 | NO VERDICT (twin TW1) |
| f = 2 | 0.0017 to 0.070 | 0.0022 to 0.073 | NO VERDICT (twin TW1) |
| f = 3 | 0.057 to 0.58 | 0.072 to 0.64 | NO VERDICT (twin TW1) |
| control | 112 to 247 | 136 to 300 | fails |

## Known answers (all PASS on both footings)

- KA-0: the f = 0 tables equal the reference bitwise at every z. The f = 0 flux equals the reference exactly at the anchors
  (largest deviation 0).
- KA-C: the control gives D 323.0 / 395.8 against FRZ3R reading T's 363.26 / 424.50, that is -11 % / -7 % (tolerance +-35 %).
  The control fails (D - 2 SE far above 4).
- KA-N: the grid haloes above v*(z) equal JNT2's counts at all 12 z. Canonical: 170 ... 223; alt: 160 ... 213.
- KA-A: with v* = 0 the tables equal the reference bitwise, and the flux ratio is exactly 1 at z 3.0.
- KA-F: the largest mean-flux miss is 2e-14.
- KA-M: realised matter ratios match the halo model at the anchors, k 1 / 3 / 5. The worst case is the control at z 2.2,
  k 3: 0.908 against 0.928 (alt; tolerance 0.032).
- KA-S: passes for every case (table above).
- Floored gas pixels: at most 3.7e-4 in the primary fields.

## Twins (anchor bins, 4 seeds, case f = 2)

| twin | canonical | alt | frozen rule | A1 rule |
|---|---|---|---|---|
| TW1 boundary removed (settled layout at f = 2 for every halo) | A 0.157 vs 0.0146 (x 10.7); jackknife SE_A 0.075 vs 0.003 | A 0.085 vs 0.0177 (x 4.8); SE_A 0.045 vs 0.004 | DOES NOT BITE (needs a change of at least 1.0) | DOES NOT BITE (change 0.142 vs 2 SE 0.150; 0.068 vs 0.091) |
| TW2 difference doubled | A 0.0502 (x 3.43) | A 0.0592 (x 3.34) | bites (>= 2.5) | bites |

- TW1 changes A by a factor of 5 to 11, but the twin's own seed scatter is large. The frozen absolute floor and A1's 2-sigma
  condition both fail.
- So the frozen word stands. No further redesign is made after these numbers.

## Hand estimate against outcome

- **Estimated:** D(f = 3) 30 to 120, D(f = 2) 10 to 60, D(f = 1.25) 2 to 25; f = 3 and f = 2 FAIL.
- **Found:** 0.57 to 0.69, 0.024 to 0.029, and 0.0006 to 0.0013. These are 50 to 10,000 times below the estimate.
- **What I misjudged:** the boundary at v* together with the settled radius leaves almost nothing for the forest to see. In the
  halo model, at z 3, J2's matter ratio at k 5 is 0.99994; the control's is 0.79. I had expected haloes just under v* at z 2.2
  to 2.6 to keep much of the outskirt change. They keep a little, and that is the whole of D.

## What was left out

Everything listed in the criteria, section 12: hydrodynamics, shock heating, self-shielding, UV and temperature fluctuations,
peculiar velocities, halo clustering, haloes below 1e8 Msun/h, modes below the 20 Mpc/h box fundamental, and form B's velocity
changes. The brackets are anchor-scaled estimates, not full 12-bin runs. Gas inputs are inherited and PROVISIONAL.

## Disclosures

**Reuse.**
- FGPA step: `tau_field`, `tune_A`, `p1d` and `dv_cell` from FRZ3R's `frz3r_core.py`, unchanged (worker count set to 2). This
  also runs FRZ1's library prefix through its own loader.
- The record's layouts: FZS1's `fzs1_hm.py` prefix (layout, Bar, rset_com, CUR, set_z, v_vir), executed read-only, with
  CFG556's `U_set` and `spectra_ta`.
- The forest data: `ss1_cosmo.forest_setup`, its source executed read-only; md5 OK. The chi^2 is the same form as the last
  line of `forest_eval`.
- JNT2: the membership counts only.
- My own code: the split function, the tables, the realisation (0.125-dex bins, per-mass Poisson, TSC deposit, lognormal),
  the seeds, the estimator and the grader.

**Blindness held.** I opened none of the forbidden folders or files, did not run `git log` beyond `-1` on my own commits, and
did not search for the forbidden words.

**The lead's operational changes (no criterion changed).**
- Two runners were allowed at once. Parts are claimed exclusively and seeded by (z, seed), so no number depends on scheduling.
- Thread count stayed at 2 throughout.

**First attempt.**
- Its four completed part files (z 2.2, seeds 0 and 1) were deleted before any number was read. The lane restarted with
  lower-memory code (float32 profile interpolation, one part per process).
- ru_maxrss had reported 14 to 20 GB per process. On macOS this counts reusable pages. The physical footprint of a primary part
  was sampled at a peak of about 2.9 GB.
- The first bracket process ran all eight brackets in one process and grew to a 22 GB physical footprint. I killed it and split
  the brackets into one process per (z, seed, bracket), and added a footprint guard (16 GB) after every flux step.
- The guard's after-flux readings were at most 0.31 GB.

**Stop and resume.**
- At 21:17 the frozen stop rule fired: free disk 4 GB and swap 21 GB, with another lane's 20 GB process on the machine.
- At 21:22 the lead changed the operational rule. Before each part: at least 10 GB free disk and at least 24 GB free plus
  inactive memory. Stop below 8 GB disk or above 14 GB swap.
- The lane resumed under that rule with two runners (`run_resume.sh`). The original `run_all.sh` did not reach its
  `run_all.done` marker. The runners' markers are `run_resume_A.done` and `run_resume_B.done`.

**The small test.** A throwaway N = 48 run in scratch space showed that TW1's frozen absolute floor (1.0) can fail when the
split's own A is tiny. AMENDMENT_A1 added a relative rule before any graded number. At N = 384 neither rule bites. The
as-frozen word stands first.

**Logs.** The run logs are ignored by the repository's .gitignore and were not committed. The commit subject 394f36e3c9 says
"run logs"; it holds none.

**Wall time.** About 2.3 h (20:19 to 22:35 EST).

## What it says about the forest row

The crossing-speed split makes the forest almost blind to the law's layout. With haloes above v*(z) kept in the reference layout
and the change confined inside f x R_fold, the 12-bin flux Delta chi^2 against DESI DR1 is 0.6 to 0.7 at f = 3, about 0.03 at
f = 2 and about 0.001 at f = 1.25, on both footings. The law's layout everywhere gives 323 / 396 in the same build. On these
numbers the split clears the forest gate by a wide margin, except at a pressure smoothing of 40 comoving kpc for f = 3. The
label is still NO VERDICT, because the frozen twin that removes the boundary does not move the anchor statistic by a resolved
amount, so this build has not shown that it would catch the boundary being wrong at the forest's sensitivity. A firmer word
needs a twin that bites, for example more seeds for the twin or a twin defined at full 12-bin scope, frozen in advance. Even
then a HOLDS here would be a hit, not a pass of the theory.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
