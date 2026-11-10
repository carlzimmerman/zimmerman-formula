# BX1 FROZEN CRITERIA: a fixed-amplitude, paired 200 Mpc/h reference below k 0.5, and KL1 Part C's gate re-read with it

Committed alone, before any BX1 script exists and before any BX1 number is computed. TEST lane: relabels nothing, adopts
nothing, not registered. **kappa = 1/2 FITTED; not theory closed.** Footings canonical (a0 9.3603e-11 m/s^2) and alt
(1.1312e-10 m/s^2), graded separately, never pooled. Cold dark energy is a gravitating field component, never a particle. No
download: everything used is on disk (CFG596's engine and S0 run, CFG411's and CFG424's S0 runs, CFG530's S0 N256 run, KL1's
scripts and inputs, the KiDS-Legacy release fetched for KL1 Part B). Folders not written: every other lane's folder, CFG596's
folder, KL1's folder, `_kl1c_rerun_tmp/`. KL1's labels are not relabelled. Lane id: `ls closure_2026_11_10/` and
`git log --all --grep BX1` show no earlier BX1.

## 1. The question and why

With the low-k realisation noise of our own reference run removed, where does KL1 Part C's gate put KiDS-Legacy and DES Y3:
inside two widths, or not?

KL1 Part C's gate (C0 R1 + C2 AD) reads Legacy 1.71 / 1.88 and DES (polished) 2.18 / 2.23 widths. Its two long-mode edges, two
single random-amplitude 200 Mpc/h runs spliced in below k 0.5, give Legacy 1.17 / 1.36 (R2, CFG411) against 1.92 / 2.09 (R2b,
CFG424 seed 360), and DES 1.31 / 1.27 against 3.49 / 3.43 (frozen scans). A run whose initial mode amplitudes are fixed to their
expectation (random phases only), averaged with its phase-inverted twin, has almost none of that noise below k 0.5.

## 2. The engine

- `bx1_pm.py` is a COPY of `campaign_fresh_gravity/CFG596_lean_pm_1024/cfg596_pm.py` (CFG596's folder is not edited). No
  formula, constant, time step, force, deposit, estimator or snapshot is changed. Changes:
  - **`CFG596_FIXAMP=1`**: after the white-noise field is transformed and normalised (both IC routines), every Fourier mode w
    is replaced by w / |w| (unit modulus, its own random phase kept). E|w|^2 = 1 in the engine's normalisation, so the modes'
    power equals its expectation exactly. Hermitian symmetry is kept (conj(w)/|w| = conj(w/|w|)).
  - **`CFG596_INVERT=1`**: every mode w -> -w (the phase moved by pi), the twin of the same seed. It composes with FIXAMP.
  - Engineering, measurement-only: `CFG596_NOSAVE=1` skips the 256^3 block-mean and z = 0 position files (disk);
    `CFG596_ICCHECK=1` bins the scaled IC field's own power, with the same bins and weights as `measure_pk`, against the input
    linear power and stores it in the run JSON. Neither changes any evolved number.
  - The run tag starts `bx1_` and carries `_fix` / `_inv` and the seed.
- Launcher `bx1_run.py`: one simulation at a time, `nice -n 10`, a watchdog like CFG596's (kill on RSS above 20 GB at 512^3 /
  8 GB at 256^3, on swap growth above 4 GB, or free disk below 3 GB; a 512^3 job does not start under 8 GB free disk). The engine
  writes its JSON after every snapshot. Run products go to `../_external_data/bx1_work/` (outside git).

## 3. Known answers (before any production run; a failed KA makes everything that rests on it NO VERDICT)

**KA1 (option-off reproduction).** The copy with both options off, at CFG596's V-L settings (S0, lean, N 256, L 100, NSEED 512,
seed 359, RMIN 0.78125), against CFG530's `S0_L100_N256` run: max |dP/P| at k <= k_hi = 2.01 h/Mpc and |d sigma8 / sigma8| at
z_i, 1, 0.5, 0 must be <= 1e-5 (CFG596's STRICT V-L tolerance). Against CFG596's own VLs run: reported.

**KA2 (fixed amplitudes reproduce the input power).** On the fixed run of seed 7101 at 256^3 (L 200, NSEED 512):
- (a) IC field (ICCHECK): binned power over the bin-averaged input linear power is 1 to 1e-6 in every bin below k_Nyq / 2.
- (b) The z_i particle snapshot: r(k) = P(z_i) / (D_i^2 P_lin(k_bin)) is within +-0.02 of the binning expectation
  r_bin(k) = <P_lin>_bin / P_lin(k_bin) (computed on the same modes) in every bin with k <= 0.5, and its rms of (r / r_bin - 1)
  over those bins is at most 1/5 of the random runs' rms of the same quantity (R1..R5 pooled).
- The same (b) is checked on each 512^3 production run before it is spliced; a production run that fails it is not used.

**KA3 (a fixed pair against random runs, 256^3, L 200, NSEED 512).** Runs: fixed pair A (seed 7101 and its inverted twin),
fixed pair B (seed 7102 and twin), random R1..R5 (seeds 7201..7205, options off). Bins: every engine bin with k <= 0.5 h/Mpc;
pair mean = (P_run + P_twin) / 2 bin by bin.
- (a) **Unbiased.** At each z in {1, 0.5, 0}: chi^2 = sum_i [(Pbar_A,i - <P_rand>_i) / (f sigma_G,i / sqrt(5))]^2 over the
  bins, with sigma_G,i = <P_rand>_i sqrt(2 / W_i) (W_i = the bin's summed `measure_pk` weights, so W_i / 2 independent modes)
  and f = max(1, sqrt(mean_i s_i^2 / sigma_G,i^2)), s_i the random runs' sample standard deviation (ddof 1). PASS if
  p(chi^2, N_bins) >= 0.01 at every z. Pair B: the same, reported.
- (b) **Quiet.** At each z: rms over bins with k <= 0.3 of (Pbar_A / Pbar_B - 1) <= 1/5 of rms over the same bins of
  sqrt(2) s_i / <P_rand>_i (the expected rms difference of two random runs).

**KA4 (the regrade reproduces KL1).** With CFG411's run as the splice (KL1's `load200` on its file), the gate rows reproduce KL1
Part C's stored GATE_R2 rows (`parts/partc_<footing>_<group>.json`): Legacy gap 1.1747 / 1.3589, DES (frozen scan) 1.3091 /
1.2726, KiDS-1000 3.3651 / 3.5332, each to 0.01 in the gap and 0.01 in chi^2 at the target. Before BX1's own splice is graded.

**KA5 (the splice writer).** My writer's file built from CFG411's z 0 / 0.5 / 1 spectra, read through `load200`, equals
`load200` on CFG411's own file bit for bit.

## 4. Production

- S0 (gravity-only), the copy in lean mode, L = 200 Mpc/h, **N = 512^3** (mesh 512), NSEED 512, RMIN 0.78125, the engine's own
  150-step grid and snapshots (z 1, 0.7548, 0.5, 0.2562, 0; z 1 / 0.5 / 0 are used), 12 threads, spill on.
- **Pair A** (graded): seed 7101 fixed + seed 7101 fixed inverted. **Pair B** (if time allows, reported): seed 7102, the same.
- Why 512^3 and not more: 1024^3 is excluded by the house rule; 768^3 would need about 32 GB resident (swap already holds
  5.1 of 6 GB on this shared machine) and about 4 h per run (8+ h a pair, no second pair). 512^3 matches R2 / R2b's resolution.
  The 256^3 runs of KA3 share every mode below their Nyquist with the 512^3 runs of the same seed (NSEED 512), so
  P_512 / P_256 of the same pair measures what resolution does below k 0.5 with the draw cancelled (reported).

## 5. The splice (KL1 Part C's R2 rule, unchanged)

The pair mean's z 0 / 0.5 / 1 spectra are written as a JSON with KL1's layout (`snap.z0 / z0.5 / z1`, `k`, `P`, `D`) and read
through KL1's own `load200`: log-log interpolation onto the S0 run's k, the S0 node replaced for k < 0.5, the 100 Mpc/h box
unchanged at k >= 0.5. No R1 correction. The response alpha(k) stays the S0 run's (as in R2).

## 6. The regrade

KL1's scripts are executed unchanged from their source (`kl1c.py` up to its "rows (frozen order)" marker, `kl1c_polish.py` up to
its `RES = dict(` line, `kl1_lib.py` imported with bytecode writing off), with BX1's splices added to their `PZV` dictionaries,
one process per footing and group as KL1 ran them (`python3 -I`; the release folder passed as an argument).

Rows, per footing, on the gate's settings (target = A1's neutrino-floor sigma8; R = A3_AD (C2's slow-loss response on RB1's
gas); covariance at the model, gamma 2; Part A / B's support cut, nuisances and scan rule):
- **GATE_BX1** (graded): pz = pair A's splice. Legacy and KiDS-1000: KL1's frozen scan. **DES Y3: KL1 AMENDMENT C3's polished
  scan (graded)**; the frozen scan reported.
- **C3b_BX1**: Legacy with its own mass-dependent alignment under its own prior (KL1's C3b), on GATE_BX1's settings.
- Reported: KA4's R2 rows; DES polished with R2; GATE with pair B's splice and with the mean of pairs A and B (if B exists); the
  256^3 pairs A and B as splices; the ln det gaps.

## 7. The gate and the labels (KL1 Part C's section 6, two-sided)

Per survey and footing: g = (form B's neutrino-floor sigma8 - the survey's best sigma8) / the survey's width.
- **CONSISTENT** if |g| <= 2 and p >= 0.05 (p at the target);
- **GAP STAYS** if g > 2;
- **OVERSHOOT** if g < -2 (counts against form B exactly as a gap does);
- **POOR FIT** if |g| <= 2 and p < 0.05.

C3b re-reads Legacy if it lands outside CONSISTENT (KL1's rule). **Overall, per footing, on KiDS-Legacy and DES Y3:**
AMPLITUDE CONSISTENT if both read CONSISTENT; otherwise GAP STAYS or OVERSHOOT if either reads so (both named if they differ);
POOR FIT if that is the worst; **NO VERDICT** if KA1-KA5 fail or a MUTATE arm does not bite. KiDS-1000 is graded the same way and
reported beside the label.

**The label's own error.** sigma_g = |g_A - g_B| / sqrt(2) per survey and footing (one pair's residual noise), from the 512^3
pair B if it completes, otherwise from the 256^3 pairs A and B used as splices (marked low resolution). The label is pair A's.
If |g_A - 2| < 2 sigma_g on a survey, that survey's reading is tagged [INSIDE SPLICE NOISE]; the tag never changes a label. If
pair B and the A + B mean read differently from pair A, all three are reported and pair A's label stands.

## 8. MUTATE (separately named outputs; each must bite or the label is NO VERDICT)

- **MB1 (splice x 0.9).** Pair A's spliced P(k) multiplied by 0.9 below k 0.5 at all three nodes: the gap must fall by at least
  0.3 widths on Legacy and on DES (polished), each footing.
- **MB2 (no inversion).** The twin replaced by a second copy of the same run, so the "pair" is one fixed run. At 256^3, z = 0:
  rms over bins k <= 0.5 of (P_A / P_B - 1) for the single fixed runs must be at least 1.5 times the same rms for the true pairs.
  The gate with pair A's run alone as the splice is reported beside it.

## 9. Reported, never graded

- Pair A (and B) mean against CFG411, CFG424, the 100 Mpc/h box raw and R1-corrected, on the 100 Mpc/h box's bins below k 0.5,
  at z 0, 0.5, 1, with the pair-to-pair difference / sqrt(2) as the error (512^3 pair B if present, else 256^3, marked).
- P_512 / P_256 for pair A below k 0.5 (resolution).

## 10. What counts against form B

GAP STAYS or OVERSHOOT on KiDS-Legacy or DES Y3 at either footing; C3b putting Legacy outside CONSISTENT; a POOR FIT. A label
inside its own splice noise is reported as such, not as a pass.

## 11. Limits to state

The 200 Mpc/h run is used only below k 0.5; the 100 Mpc/h box's own draw above k 0.5 remains; 512^3 at 200 Mpc/h is coarser than
the 100 Mpc/h box (P_512 / P_256 bounds it); DES Y3 is not DES's newest release (a year-6 analysis exists and is not on disk);
one gravity-only dynamics; the EH IC spectrum, flat w = -1 background and massless-neutrino S0 run are inherited (the neutrino
floor enters only through the target sigma8, as in KL1).

## 12. Hand estimate (before any code; unverified)

- KA1 bitwise or <= 1e-8; KA2 (a) exact, (b) r within 0.5 % of r_bin; KA3 passes with large margins (pair-to-pair at z 1 below
  1e-3, at z 0 and k <= 0.3 below 1 %, against a random rms near 10 to 15 %).
- The pair will sit near CFG424's run at k 0.25 to 0.5 and well above CFG411's (about +10 %, CFG411's slower growth, see
  section 13), and near the R1-corrected box at k 0.08 to 0.2.
- **Gate:** Legacy 1.6 to 2.0 canonical, 1.8 to 2.2 alt; DES (polished) 2.2 to 3.0 on both; KiDS-1000 3.6 to 3.9.
- **Overall: GAP STAYS driven by DES Y3, 65 %; AMPLITUDE CONSISTENT 30 %; POOR FIT or OVERSHOOT 5 %.** Alt Legacy may cross 2.
- sigma_g: Legacy below 0.1 width, DES 0.1 to 0.3. MB1 moves Legacy by 0.5 to 0.8 and DES by 1 to 2 widths.

## 13. Disclosures (seen before this freeze)

- Every KL1 Part A / B / C number, CO2's post hoc r(k) values, KL1's stored GATE_R2 rows (the KA4 numbers above).
- Stored spectra, read before the freeze (no BX1 code): CFG424 / CFG411 is 1.00 +- 0.02 at z_i for k 0.3 to 1, but 1.06 to 1.20
  at z 1, 0.5 and 0 across k 0.3 to 1 (per-bin mode noise at 200 Mpc/h is about 2.5 % there). CFG411 / CFG596 at z 1 is 0.86 to
  0.91 at k 0.5 to 1; CFG424 / CFG596 is 0.91 to 1.10. So CFG411's run grows about 12 % less power after z_i than CFG424's and
  CFG596's: R2's low edge is probably not only a random draw. This lane does not audit CFG411's engine; it reports the pair
  against both runs.
- CFG596 timings (VMs, 512^3, 12 threads: 75 min; VLs, 256^3, 3 threads: 17 min); CFG411 / CFG424 512^3 S0 runtimes (1.8 h, 1.0 h).
- No BX1 number exists.
