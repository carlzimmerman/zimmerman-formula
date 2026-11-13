# SRF1 RESULT: the settled-radius window with the forest graded at flux level

**NO VERDICT / NO VERDICT (canonical / alt).** Two known answers fail, so no window label is graded on either footing.

- **(c1) fails on substance.** The stratified build over-realises the halo model's own matter-level change: 1.78 / 1.86
  times the expected turnaround-scope Delta chi^2 at f = 1, and 1.86 / 1.82 at f = 1.30. The criteria allowed 0.67 to 1.5.
  It passes at f = 2.00 (1.46 / 1.48).
- **(a) fails on precision only.** f = 0 equals the reference element by element in 32 of 34 boxes; in the other 2 (one per
  footing) it differs by 4e-16 / 7e-16 relative, where the criteria asked for exact equality.
- **The label is reported under AMENDMENT_A1.** The as-frozen grid (every rare group forced, 14 flux points, brackets at all
  anchors) was not run: it did not fit the compute budget.

TEST lane: adopts nothing, relabels nothing (SRH1, SRH1R, FZS1, FRZ3, FRZ3R keep their labels), registers nothing.
- Footings are graded separately and never pooled. Cold dark energy is a gravitating field component; no particle is added.
- **The settled-radius family is post hoc**: it was chosen after FRZ1 failed.
- Nothing here says the data favour the framework.

## The ungraded numbers (what a window would have read; NOT a label)

The flux-level forest Delta chi^2 is far below the gate of 4 at every grid f up to 3.0, on both footings:

| f | flux Delta chi^2 canonical / alt | realised matter level, same fields | flux / matter | halo model, turnaround scope D_ta | record convention D_rec (= SRH1) |
|---|---|---|---|---|---|
| 0.70 | 0.020 / 0.023 | 4.3 / 4.4 | 0.005 | 2.4 / 2.3 | 3.17 / 3.08 |
| 0.90 | 0.048 / 0.056 | 25.3 / 25.3 | 0.002 | 14.2 / 13.5 | 19.5 / 18.6 |
| **1.00** | **0.068 / 0.072** | **49.3 / 48.8** | 0.0014 / 0.0015 | 27.7 / 26.2 | **38.74 / 36.66** |
| 1.10 | 0.077 / 0.081 | 86.6 / 84.9 | 0.0009 | 48.9 / 45.7 | 69.5 / 65.2 |
| 1.20 | 0.093 / 0.096 | 138.6 / 130.1 | 0.0007 | 77.5 / 65.0 | 112.3 / 95.0 |
| 1.30 | 0.110 / 0.109 | 199.8 / 141.6 | 0.0005 / 0.0008 | 107.4 / 77.9 | 159.9 / 117.3 |
| 1.40 | 0.137 / 0.127 | 242.2 / 161.8 | 0.0006 / 0.0008 | 142.7 / 96.7 | 218.7 / 149.6 |
| 1.50 | 0.178 / 0.153 | 285.6 / 190.3 | 0.0006 / 0.0008 | 177.1 / 115.5 | 279.7 / 183.7 |
| 2.00 | 0.323 / 0.230 | 391.1 / 244.1 | 0.0008 / 0.0009 | 268.3 / 164.9 | 452.1 / 275.1 |
| 3.00 | 0.674 / 0.577 | 443.3 / 315.6 | 0.0015 / 0.0018 | 409.7 / 296.8 | 679.7 / 480.5 |
| inf (to r_ta) | 169.6 / 263.1 | 1739 / 2251 | 0.098 / 0.117 | 4983 / 4398 | 9916 / 9009 |

**The forest's flux-level upper edge, on its own, is f_max > 3.0** on both footings. Delta chi^2 never reaches 4 on the grid.
- The crossing lies between f = 3.0 and r_ta. The inf row is incomplete: A1's group cut was chosen for f <= 2, and at f = inf
  it drops much of the change (matter 1739 against FRZ3R's 5035).

**What the window would read if the known answers had passed:**
- Canonical [1.004, > 3.0], alt [1.050, > 3.0]. f = 1 is **OUTSIDE** on both, only because SRH1's G4 (KiDS early-type line)
  fails at the grid point f = 1.00 (+2.003 sigma); its interpolated edge is 1.004 / 1.050. G2 (0.391) and G3 do not bind.
- With SRH1R's blind finding that lensing as graded cannot see f, the lower edge is G2's 0.391. The window is then
  [0.391, > 3.0] and **f = 1 is inside**.

**In one plain sentence:** at flux level the forest stops excluding the settled-radius family. Whether f = 1 sits in the
window turns on one lensing line 0.003 sigma over its 2 sigma threshold, and on whether that line can see f at all. This is
not graded: this build's own matter-level check fails.

**At f = 1 the flux-level Delta chi^2 is 0.068 / 0.072.** The matter level of the same fields is 49.3 / 48.8. For
comparison, the record's projection (SRH1 / FZS1) gives 38.74 / 36.66 and the turnaround-scope halo model 27.7 / 26.2.
- The flux-to-matter ratio is about 0.001. The full layout gives about 0.07 to 0.1 (FRZ3R).
- Mutation M1 says why: with saturation removed, the anchor-bin Delta chi^2 at f = 1.30 goes from 0.017 to 2958
  (canonical), 0.016 to 2526 (alt).
- The settled change sits inside R_set of haloes of about 1e12 to 1e14 Msun/h. Their gas is saturated in the forest, so the
  transmitted flux hardly sees it.

## Per bin and per wavenumber (canonical; alt alike, in the .out files)

- **Per-bin Delta chi^2 at f = 1.** z 2.2: 0.01, 2.4: 0.01, 2.6: 0.04, all other bins 0.00.
- **Per-bin Delta chi^2 at f = 2.** z 2.2 to 3.6: 0.01 to 0.06; z 3.8 and up: 0.00.
- **Flux ratio at f = 1, k_v 0.003 / 0.005 / 0.01 / 0.02 / 0.03 s/km.** z 2.2: 0.9995 / 0.9997 / 1.0001 / 1.0003 / 0.9993;
  z 2.6: 0.9987 / 0.9986 / 0.9987 / 0.9989 / 0.9976; z 4.4: 1.0000 at every k.
- **Shape.** The flux response is at most about 0.2 % in any bin, at every DESI wavenumber. The 3D matter ratio at k 5 is
  0.979 at z 2.2, so the softening is not a single-amplitude artefact.

## Known answers

| item | canonical | alt |
|---|---|---|
| (a) f = 0 equals the reference, element by element, exactly | **FAIL**: 16 of 17 boxes exact; z 4.4 group 10.5 differs by 4.4e-16 relative | **FAIL**: 16 of 17 exact; z 2.2 group 12.5 differs by 6.7e-16 |
| (b) f = inf, Poisson-only path, against FRZ3R's reading T parts | PASS: per part 5.6e-16; 12-bin flux 348.296 = 348.296, matter 5116.9 = 5116.9 | PASS: 0.0; 425.652 = 425.652, 4622.8 = 4622.8 |
| (c0) halo-model chain against SRH1 (R_cold to 1e-4; Delta chi^2 to 1 %) | PASS: R_cold to 4.7e-6; f 1.00: 38.74 = SRH1's 38.74 (FZS1); every SRH1 grid f within 0.01 % | PASS: 3.5e-6; 36.66 = 36.66 |
| (c1) realised matter level against the turnaround-scope halo model (0.67 to 1.5) | **FAIL**: 1.78 (f 1.00), 1.86 (1.30), 1.46 (2.00, passes) | **FAIL**: 1.86, 1.82, 1.48 |
| (d) mean flux equals the target, every field | PASS: 2.3e-14 | PASS: 2.7e-14 |
| (e) seed scatter at the edge (noise <= 1 in 12-bin Delta chi^2) | PASS: 0.048 at f 3.0 | PASS: 0.012 |

**About (a).** The difference is in the 16th digit, in 2 of 34 boxes (both forced boxes). B is built as R + 0 in a separate thread, and
the result differs from R in the last bit; the base box and every other forced box are exact. The criteria said exact, so
it is reported as a fail.

**About (c1).** This is the failure that matters. FRZ1's convention against the turnaround scope is not the cause:
q = realised / record convention is 1.27 / 1.33 at f = 1, so the build even exceeds the record's number. The cause is the
estimator's own sampling noise:
- The groups at log M 13.0 and 13.5 get a single forced halo (A1's cap at about 5 % of box mass).
- Its bin is drawn in proportion to expected count, and the non-anchor bins have one seed.
- Per bin at f = 1, z 2.4 is over-realised about three times (realised R - 1 at k 3: -0.0172 against -0.0056 expected),
  while z 2.2 and 2.6 are under-realised by 0.7 to 0.8.
- The post hoc reading R (AMENDMENT_A2, ratio-weighted groups) moves the matter level only to 40.1 / 38.7 at f = 1. It does
  not cure the per-bin noise either.
- So the build does not reproduce the halo model's change bin by bin. Its flux numbers are ungraded.

## Mutations (both bite; `srf1_grade_<footing>_MUTATE.out`)

- **M1, saturation removed (F = 1 - A tau), z 2.2 and 3.0, seed 0.** f 1.30: 0.0172 to 2958 (canonical), 0.0156 to 2526
  (alt). f 1.00: 0.010 to 1533 / 1436. f 2.00: 0.052 to 4702 / 3604. It bites by a factor of about 1e5.
- **M2, R_set doubled at f = 1 (independent switch), anchors, seed 0.** Canonical 0.0102 to 0.0516 (x 5.05); alt 0.0098 to
  0.0353 (x 3.60). Each equals the f = 2.00 grid row to 1e-12.

## Brackets (12-bin estimate at f 1.00 / 1.30 / 2.00, scaled from z 2.2 and 3.0; ungraded because the label is NO VERDICT)

| bracket | canonical | alt |
|---|---|---|
| lambda_P x 0.5 | 0.03 / 0.10 / 0.64 | 0.03 / 0.10 / 0.63 |
| lambda_P x 2 | 0.01 / 0.03 / 0.16 | 0.01 / 0.03 / 0.09 |
| lambda_P = 100 proper kpc | 0.00 / 0.01 / 0.06 | 0.00 / 0.01 / 0.03 |
| gamma 1.2 | 0.02 / 0.11 / 0.47 | 0.03 / 0.09 / 0.28 |
| gamma 1.6 | **0.56 / 0.59 / 0.91** (largest) | 0.62 / 0.64 / 0.83 |
| tau_eff x 0.9 / x 1.1 | 0.07 / 0.11 / 0.29; 0.07 / 0.12 / 0.37 | 0.08 / 0.11 / 0.21; 0.08 / 0.12 / 0.26 |
| clustered placement | 0.02 / 0.09 / 0.13 | 0.02 / 0.05 / 0.03 |
| N 256 | 0.05 / 0.08 / 0.23 | 0.05 / 0.07 / 0.14 |
| B-conv (record convention) | 0.05 / 0.09 / 0.37 | 0.05 / 0.09 / 0.26 |
| reading R (A2) | 0.10 / 0.15 / 0.37 (f 3.0: 0.73) | 0.10 / 0.14 / 0.27 (0.63) |

- **No bracket moves f = 1 across the gate, and none closes the window.** The largest value is gamma 1.6 at f 2.00, 0.91.
- So the ungraded reading would not have carried FRAGILE.
- **The pressure-smoothing scale is not decisive here, unlike FRZ3 / FRZ3R.** Even x 0.5 stays under 1.

## Ungraded regime split at f = 1 (requested by the lead after the criteria were frozen; no new compute)

The stratified sum is split by FRZ1's v_stiff boundary (unchanged); a straddling group is assigned by majority (group 12.0 is
0.7 / 0.5 cluster):

| | flux Delta chi^2 | matter Delta chi^2 |
|---|---|---|
| galaxy-regime haloes only (base box incl. the two-halo term + galaxy groups) | 0.013 / 0.012 | 0.003 / 0.010 |
| cluster-regime haloes only | 0.083 / 0.086 | 48.8 / 48.5 |

- **Almost all of the matter-level and flux-level number comes from cluster-regime haloes,** as FZS1's diagnostic and SRJ1
  found for the matter level.
- The two parts do not add to the total (0.068), because Delta chi^2 is quadratic in the ratio.

## Other reported readings

- **Poisson-only reading (FRZ3R's method, every halo at its Poisson position).** f 1.00: flux 0.166 / 0.113, matter 9.3 /
  8.4. This is the spurious under-realisation the stratified build was designed to avoid. f = inf: 348.3 / 425.7, which is
  FRZ3R's reading T on these seeds.
- **Share dropped by A1's 3 % cut** (turnaround-scope one-halo difference at k 3; f 1.00 / 1.30 / 2.00). It is within +-3 %
  at every z, at most +4.7 % (alt, z 2.2, f 2.00). Per z it is in the .out files.

## What is left out

- The physics: hydrodynamics, shock heating, self-shielding, UV and temperature fluctuations.
- The box: 20 Mpc/h, so no large-scale modes and no rare haloes except by forcing.
- Peculiar velocities.
- Inputs inherited as PROVISIONAL: the FGPA constants, tau_eff(z), and lambda_P = 79 comoving kpc (Kulkarni et al. 2015).
- Inherited from FRZ1: the Tinker and Duffy scalings and the present-day baryon shapes.
- Not bracketed: the rare threshold (30), the 3 % share cut, the forced counts, and uniform placement of forced haloes.
- A forced halo of 1e13 to 1e14 Msun/h is a single object in a box of about 7e14 Msun/h; its environment is not
  cosmological.

## What an independent re-grade would have to redo

1. Realise the rare haloes so that the matter-level change matches the halo model bin by bin. The options are a larger box
   at forest resolution, many forced haloes per 0.1 dex bin with per-bin weights, or one bin per box.
   - Then grade the flux-level Delta chi^2 against a passing (c1).
2. Set the gas smoothing and saturation in massive haloes with hydrodynamics. The whole softening rests on saturated
   pixels (M1: x 1e5).
3. Re-grade SRH1's G4 line at f between 1.00 and 1.25. The window's lower edge on that line is an interpolation, and SRH1R
   finds the line cannot see f.

## Disclosures

- **Order of commits.** The criteria were committed alone before any script; A1 alone, after the halo-model tables and before
  any flux field; A2 alone, after one part's matter level and before any flux number was opened.
- **Test parts.** Before the real grade, the grader was tested on 64^3 parts in a scratch folder, now deleted. Those numbers
  were toy runs and are not used.
- **Runs that were killed.**
  - The first runs were stopped by memory: a 4-thread kill, then 24 to 31 GB. macOS does not return freed memory between
    boxes, so the final run puts one box per process, at about 18 GB peak.
  - One part from a superseded run was deleted after a summation-order fix that made (b) exact.
  - No graded part comes from a killed run.
- **SRF1R.** I never opened the SRF1R folder or its git history. A `ps` listing taken while chasing a memory kill showed its
  process command lines (`srf1r_flux.py P both 2.2 0`, four worker processes) and its folder name. Nothing else of it was
  seen.
- **The regime split and reading R were added after the criteria were frozen** and are ungraded.

## Files and commits

- Commits:
  - `FROZEN_CRITERIA.md`: fa73352ceb (alone).
  - `AMENDMENT_A1_2026-11-12.md`: 88144763e1 (alone).
  - `AMENDMENT_A2_2026-11-12.md`: 9df63f25f0 (alone).
  - First code: 1736390660.
  - This result, the final code, the parts and the grade outputs: the next commit.
  - Not pushed.
- Scripts:
  - `srf1_tables.py`: halo-model tables. It executes SRH1's `srh1_hm.py` prefix read-only. The tables (about 330 MB of npz)
    were deleted; the script regenerates them.
  - `srf1_run.py`: imports FRZ3R's `frz3r_core.py` read-only.
  - `run_all.sh`.
  - `srf1_grade.py`: executes FRZ3R's grading set-up read-only.
- Outputs:
  - `parts/*.json`: 38 parts, 14 MB.
  - `srf1_grade_<footing>.json/.out` and `_MUTATE.json/.out`.
- Machine time:
  - About 4.2 h in all: 12 tables, 30 primary parts, 4 bracket parts, 2 clustered parts, 2 N 256 parts.
  - Settings: nice 19, 2 flux threads.
  - Nothing was downloaded, and nothing was written outside this folder (apart from scratch files, now deleted).
  - Console logs are git-ignored.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
