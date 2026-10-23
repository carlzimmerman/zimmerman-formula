# CFG963 DRAFT (NOT FROZEN, NOT QUEUED): the decisive 1024³ control NCS0+M3 — plain Poisson gravity with census gas expulsion, native ICs

- **Status:** DRAFT design only. Nothing here is frozen, no engine code is written, no job is defined in any launcher, nothing is
  queued. If the owner approves, this text is re-committed ALONE as `FROZEN_CRITERIA_1024.md` (with the engine hash filled in)
  before any engine code runs, and the job is queued AFTER CFG960's chain (`chain960.sh`) has written its `chain960 done` line.
- **Settings:** κ = ½ FITTED; footings never pooled; raw KiDS-1000 / DES Y3, framework-native scoring; no HMcode, BAHAMAS or ΛCDM
  yardstick; cold energy mass required; not theory closed. A CONSISTENT class does not mean the data favour the framework.

## Why this run

CFG963's surrogate S0+M3 = NCS0 × T_M3(k, z) rests on three assumptions the record cannot test without a run: (i) M3's fractional
effect measured on the M1+M2 background (T1x / T12) equals its effect on plain Poisson gravity; (ii) a transfer measured with
inherited inputs carries over to the native_cmb ICs and background (C1 closure tests this for the whole module set only);
(iii) back-reaction of the particles on the moved source is the same in both environments. NCS0+M3 removes all three: it is the
plain-Poisson control with exactly the engine's own gas expulsion and nothing else.

## Engine (to be written in this lane; nothing changes in CFG654 / CFG650 / CFG960 files)

- A lane-owned copy of the CFG654 engine (sha256 recorded at freeze) with ONE new switch value `S0M3` for the first argument
  (alongside `RES` and `S0`). With `S0M3` the force call does exactly:
  1. the census refresh of the RES path on the same cadence (every 10th dynamical call; diagnostic calls at snapshots):
     `cover_peaks` → `cover_balls(x = 1.0, want_fret = True)` → catchment class code per cell, r_ON per class, census f_ret per
     class (`fret_of(log10 M_ta)`; NOT the M2 condensed table). No edge mask, no tidal f_sw, no own-host partition.
  2. `expel_m3` unchanged: δ_src = δ + Σ_k [G_σk ∗ e_k − e_k], e_k = f_b (1 − f_ret,k)(1 + δ) on class-k cells, σ_k = r_ON,k.
  3. the plain Poisson potential from δ_src: φ_k = (−1.5 Ω_m / a) δ_src,k / k². No MOND input, no settling source, no supply, no cap.
  - The footing is never read (as for NCS0), so ONE run serves both footings.
  - Snapshots unchanged: particle P and the gravitating P_grav (which contains the re-placement), z = 1, 0.5, 0 + extras.
- **Inputs:** native_cmb (the A1 primary set), seed 359, L100, N = 1024, NSEED 1024, RMIN 0.78125, lean mode, SPILL, the same
  150-step grid and checkpoint / resume code as NCS0 / NC1x.
- **Validation before any 1024³ job (≤ 256³, one process, RSS kill 3 GB):**
  - V-0: switch `S0` of the copy reproduces CFG654's VNcs bit for bit (the copy changed nothing else).
  - V-Z: `S0M3` with f_b → 0 in the expulsion only (MUTATE) reproduces VNcs bit for bit (the new path adds nothing but M3).
  - V-M: mass conservation, |placement imbalance| ≤ 1e-8 at every snapshot; expelled mass fraction at z = 0 within
    0.030–0.036 (NC1x: 0.032; VM123: 0.034).
  - V-T (reported): 256³ P_grav(S0M3) / P(VNcs) against CFG963's M3-256 transfer, |difference| at k ≤ 1 h/Mpc, z = 0.
  - V-R: resume from a checkpoint is bit-identical (128³).

## Job, gate and cost

- **Job `NCS0M3`:** native_cmb, switch `S0M3`, 1024³, 14 threads, nice 10, under a launcher with the CFG654 guards (abort if
  RSS > 52 GB or swap growth > 4 GB; disk guard 3 GB; refuse to start with < 18 GB free disk).
- **Start gate:** CFG960's chain finished (`chain960 done`), no other 1024³ engine or Ollama server running, free + inactive
  ≥ 46 GB, free disk ≥ 45 GB. The CFG960 gate's process pattern does not match a CFG963 engine name, so this job must not start
  while chain960 is alive.
- **Cost estimate (from the stored engine logs):** NCS0 took 28 366 s (7.9 h) with forces ≈ 0.3 ks in total; between the matched
  inherited pair T12 → T1x, M3 added ≈ 2.0 ks of force time and ≈ 4.7 ks of snapshot time. The census refresh (≈ 15 refreshes ×
  14 smoothing radii + the class balls) adds an estimated 3–5 ks. **Expected wall time 9–11 h; peak RSS 40–44 GB** (NCS0
  peaked at 41.4 GB, NC1x at 44.3 GB per the engine's own counter); output ≈ 0.7 GB (JSON + six 256³ block-mean files); spill
  temporaries as NCS0. Validation: ≈ 1 h at ≤ 256³.

## Scoring (the CFG963 wrapper of the frozen CFG654 native scorer; MUTATE first)

1. **NCS0M3 vs NCS0** (NCS0M3 in the framework slot: its P_grav).
2. **NC1x vs NCS0M3** and **NC2x vs NCS0M3** (NCS0M3 in the control slot with its GRAVITATING spectrum, the CFG963 convention:
   the scorer's control slot otherwise reads the particle P, which would leave out the re-placed gas).
3. Same data, cuts, support mask, nuisances, robustness set {widen2, noIA, held, LOC}, DESI reported, T-OWN, NZ1, classes.
4. K: the wrapper reproduces the stored NC1x / NC2x vs NCS0 scores exactly (as in CFG963). M0: NCS0M3 run with f_b → 0
   (V-Z output) vs NCS0 gives Δχ² = 0. M1: a planted ×0.9 bites.

## Reading (pre-declared in the draft; identical to CFG963 §6 with the run in place of the surrogate)

f = Δχ²(NCS0M3 vs NCS0) / Δχ²(NCx vs NCS0) (−10.08 canonical, −9.39 alt); d = Δχ²(NCx vs NCS0M3), KiDS, per footing.
- **M3-CARRIED** if f ≥ 0.70 and |d| ≤ 3: the native shear pass is "the capped cold sector does not overproduce structure" plus
  "gas expulsion lowers power"; it is not a preference for the framework's law over plain gravity with feedback, and the
  engine-parent problem is not load-bearing for the shear result.
- **LAW-CARRIED** if f < 0.30: the lead belongs to the cold-sector rules; the engine-parent problem is load-bearing.
- **SHARED** otherwise.
- KiDS distinguishes the cold sector from plain gravity + expulsion only if |d| ≥ 4 with all four robustness values of d of
  one sign. The CFG963 surrogate result is quoted beside the run result; if they disagree in class, the run supersedes the
  surrogate and the disagreement is reported as a failure of the surrogate's assumptions.

## Optional second job (not decisive)

`NC12` (native_cmb, M1+M2, canonical) was defined in CFG654's launcher but never run. With NCS0M3 and NC12 the full native
factorisation NCS0 → NC12 → NC1x and NCS0 → NCS0M3 would be measured at production resolution. Cost ≈ NC1x (9–10 h, ≈ 44 GB).

κ = ½ FITTED; footings never pooled; cold energy mass required; not theory closed.
