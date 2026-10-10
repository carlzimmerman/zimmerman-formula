# CFG596 FROZEN CRITERIA: a lean 1024³ PM and a framework-native shear test with the framework's own boost as the sensitivity tooth

Committed alone, before the lean engine is validated and before any production run. Date: 2026-10-10.

## 0. Disclosure: why this rule exists and what it does not change

- **What was seen first.** This file was written AFTER the CFG596 pre-flight (commit ac4857dce; `cfg596_preflight.out`, `cfg596_tooth_audit.out`). The pre-flight showed that CFG592's frozen native tooth NZ2 cannot be passed by any PM box:
  - NZ2 is a 20% excess ramped over k = 0.5 → 1 h/Mpc. With every published point resolved it gives χ² 7.95 (KiDS) and 1.95 (DES), against the ≥ 9 required.
  - The planned L400 N1024 box keeps zero points.
  - The same audit showed that the framework's own measured boost, injected as a mock, gives χ² 14–22 on KiDS at L100–150 N1024.
- **The rule below is therefore chosen after seeing that the frozen one is unreachable.** It is post-hoc relative to CFG592 and is labelled as such everywhere.
- **CFG592's verdict stays on the record unchanged:** NOT DIAGNOSTIC on every track. Nothing here edits CFG592's files or its frozen text.
- **The owner's direction (relayed by the coordinator, 2026-10-10):**
  1. a sensitivity tooth with the framework's OWN predicted boost shape;
  2. the box chosen from the pre-flight between L = 100 and 150 Mpc/h at N = 1024;
  3. CFG592's support cut, nuisance treatment and statistic otherwise unchanged.
- **Settings:** κ = ½ is FITTED. The footings (9.3603e-11 / 1.1312e-10) are never pooled. The cold energy's MASS is still required; no particle species. Not "theory closed". Nothing here may say the data favour the framework.

## 1. Engine and runs

- **Engine:** CFG527's `cfg527_pm.py` (sha256 aeabd0ba4ca5ff1a3b1cc3c17a895821670608397928cfa42d3f03707bd50df0). It is the census lineage CFG518 → 521 → 524 → 527: shell draw, unfiltered source (NOFILT), census edge, cap.
  - It is the engine of the CFG530 runs. Those runs supply the tooth's boost (§4) and were the only runs CFG592 could score.
  - The lean copy is `cfg596_pm.py`.
- **Allowed engineering changes, and no others:**
  - storage precision: particle state as a float32 Lagrangian displacement plus float32 momentum, in place of float64 wrapped positions and momenta;
  - chunked particle deposit and interpolation;
  - kick, kick and drift fused per component, so no stored particle accelerations;
  - in-place or partial (axis-by-axis) FFTs;
  - factorised tidal-tensor transforms: the kx-free factors are applied after the axis-0 transform;
  - slab-wise evaluation of elementwise expressions;
  - temporaries spilled to disk.
- **No change is allowed to any formula, constant, threshold, switch, mask rule, time step or output definition.**
- **Extra snapshots are measurement only.** The engine's diagnostic snapshot call refreshes the catchment / f_ret state. At the two EXTRA snapshots, that state is saved before the measurement and restored after it, so the extra snapshots do not alter the trajectory. The engine's own snapshots (z = 1, 0.5, 0) keep the original semantics.
- **Production box:** L = 100 Mpc/h, N = 1024 (particles = mesh = 1024³).
  - NSEED = 1024 and seed 359. This is a new realisation: NSEED ≥ N is required, so it is not CFG530's NSEED-512 field.
  - RMIN = 0.78125 Mpc/h, CFG530's fixed physical value at L100. Draw SHELL, mix NOFILT, f_ret census, branch FLAT.
  - The step grid is unchanged: 150 steps from z_i = 49.
  - k range under CFG592's rule: k_lo = the first bin centre (about 0.080), k_hi = πN/(4L) = 8.04 h/Mpc.
- **Why L100 and not L150** (pre-flight proxy, `cfg596_preflight.json` / `cfg596_tooth_audit.json`):

| | L100 N1024 | L150 N1024 |
|---|---|---|
| kept KiDS / DES points | 119 / 100 | 93 / 70 |
| own-boost tooth, KiDS (can / alt) | 14.6 / 19.1 | 14.4 / 18.8 |
| own-boost tooth, DES (can / alt) | 8.6 / 9.7 | 3.4 / 4.2 |

- **Snapshots:**
  - the engine's own: z = 1 (step 123, a = 0.5), z = 0.5 (step 134), z = 0 (step 150);
  - extra, measurement only: step 128 (z = 0.7548) and step 141 (z = 0.2562), the grid steps nearest z = 0.75 and 0.25. Their actual z is stated in the output.
  - At every snapshot the run stores the particle P(k), σ8, and the GRAVITATING-density P(k) and σ8. The gravitating density is δ_grav = −k² φ_k a/(1.5 Ω_m), from the engine's own total potential, the CFG555 definition generalised from a = 1.
  - It also stores 256³ block-averaged meshes of δ_part and δ_grav. There are no particle dumps.
- **Order of runs:** one big job at a time, detached (nohup), nice 10, ≤ 14 threads, memory watched.
  1. S0.
  2. LRcan (canonical).
  3. LRalt if time allows. The alt footing's verdict is PENDING until then.
- **Abort rule:** stop a job if its resident memory exceeds 50 GB, or if system swap use grows by more than 4 GB during the job.
- **Checkpoints.** The state is 25.8 GB at 1024³. A checkpoint is written only if free disk exceeds state + 10 GB. If not (26 GB was free at freeze time), the run is not resumable; a crash means a rerun. Partial JSON is written after every snapshot.

## 2. Validation gates (all before production)

- **V-E, exact mode** (float64 state, unchunked deposit, original tidal transforms). The lean code with its exact switches must reproduce the original engine:
  - P(k) and σ8 at every snapshot must match bit-for-bit. A max relative difference ≤ 1e-12 is allowed, and only if it comes from measurement-side summation order.
  - The z = 0 positions must match the saved float32 npz exactly.
  - Runs:
    - (a) LRcan at L200, N256, NSEED 256, RMIN 1.56, against CFG527's JSON and npz;
    - (b) S0 at L100, N256, NSEED 512, against CFG530's S0_L100_N256 JSON and npz.
- **V-G, CFG555.** On V-E(a)'s z = 0 state, the gravitating P(k) and σ8 must match `cfg555_527_LRcan_L200.json` (P_grav, s8_grav) to a relative difference ≤ 1e-5 in every bin, and in σ8.
- **V-L, lean mode** (all allowed changes on). Runs: S0 and LRcan at L100, N256, NSEED 512, RMIN 0.78125 (the production configuration at lower N), against CFG530's JSONs. At every snapshot, using k ≤ k_hi = πN/(4L) for P:
  - **STRICT** (the originally requested bar): max |ΔP/P| ≤ 1e-5 and |Δσ8/σ8| ≤ 1e-5.
  - **SCIENCE:**
    - max |ΔP/P| ≤ 1e-3;
    - |Δσ8/σ8| ≤ 1e-4;
    - on LRcan at z = 0, the boost B = P_grav/P_part must match the original's B to ≤ 1e-3. The original's B comes from CFG530's N256 profile cache `cfg526_LRcan_L100.npz` (pgrav / ppart), which uses the same capture method and was identity-checked in CFG555.
  - Production may proceed only if SCIENCE passes for both runs. The tier reached is reported as is. If STRICT fails, that is disclosed.
- **V-M, memory:**
  - peak resident memory measured at 256³ and 512³ (lean S0 at L100 N512 as a full run, compared with CFG530's S0_L100_N512 JSON and reported only; lean LRcan at L100 N512 for its first ≥ 12 force calls, which include the zi diagnostic snapshot and two catchment refreshes);
  - an analytic model;
  - the measured peak of the first 1024³ production steps.
  - The gate is a peak ≤ 50 GB at 1024³.
  - If it cannot be met, the best achievable configuration is reported, and nothing runs until the coordinator is told.

## 3. Likelihood: CFG592's native machinery, unchanged except as listed

- **Unchanged:** `cfg592_native.py`'s library part is exec'd without edits. This covers:
  - the data, covariance, n(z) and published cuts;
  - the support cut: a point is kept if ≥ 90% of its integrand lies in [k_lo, k_hi], and a survey with N_kept < 10 is NOT DIAGNOSTIC;
  - the nuisances: photo-z shifts, DES m, NLA IA marginalised, and the no-IA setting;
  - the PM background and DESI-distance variant;
  - the extension rules outside [k_lo, k_hi];
  - interpolation over the z nodes 0, 0.5, 1, with D² growth above z = 1;
  - the fit, the classes (`klass`) and the p-values.
- **Models:**
  - **Framework:** nodes are the run's MEASURED gravitating P(k, z) at z = 0, 0.5, 1. The code path is CFG592's "F" with B ≡ 1, so the node spectrum is P_grav itself.
  - **S0:** nodes are its particle P(k, z), which equals its gravitating P, since S0 has no source.
- **Statistic:** Δχ² = χ²_min(F) − χ²_min(S0) per survey and footing. Positive means the framework is worse.
- **Robustness set:** widen2, noIA, DESI distances, and "held". "Held" replaces CFG592's "fade", because with a measured B(k, z) the fade bracket is the identity. "Held" is CFG592's own former PRIMARY construction: P_F(k, z) = P_part,F(k, z) × B_F(k, z = 0).
- **Classes:** as in CFG592:
  - EXCLUDED: Δχ² ≥ 9 and the minimum over the robustness set ≥ 9;
  - TENSION: Δχ² ≥ 4;
  - CONSISTENT: Δχ² < 4 and the maximum over the robustness set < 9;
  - NOT DIAGNOSTIC otherwise, or N_kept < 10, or a failed tooth T-OWN (§4).
  - The no-IA class is reported alongside.
  - Each footing has one run, so the footing summary is that run's class.
- **Reported only (no verdict):**
  - the interpolation check at the two extra snapshots: max |ln(P_interp/P_meas)| over k ≤ k_hi, for both models;
  - Δχ² from a five-node variant (z = 0, 0.2562, 0.5, 0.7548, 1);
  - absolute χ²/N and p-values;
  - CFG592's looser support thresholds 0.8 and 0.7.

## 4. Sensitivity tooth T-OWN (the new rule) and the teeth carried over

- **T-OWN, per survey × footing.**
  1. Take the S0 best fit (IA marginalised).
  2. Build the mock: that best-fit theory with the S0 spectrum multiplied by B_foot(k).
     - B_foot = P_grav/P_part from CFG530's committed L100 N512 cache `cfg530_work/profiles/N512/cfg526_LR<foot>_L100.npz` (pgrav / ppart, z = 0), at its stated values.
     - It is held at all z, and held flat outside its own k range (0.08–4.02 h/Mpc).
  3. Refit S0 to the mock.
  - χ²_min ≥ 9 means DIAGNOSTIC for that survey × footing. Otherwise that survey × footing is NOT DIAGNOSTIC, whatever its Δχ².
  - Canonical uses B_can; alt uses B_alt.
- **NZ1 (carried over):** the framework code path with the source set to zero must reproduce χ²_min(S0) to |Δχ²| ≤ 1e-9.
- **NZ2 (CFG592's 20% ramp):** reported on the new box. It is expected to fail and has no role.
- **MUTATE run:** `CFG596_MUTATE=1` writes separate outputs.

## 5. Inherited ΛCDM-calibrated ingredients (flagged, as in CFG592)

- the PM's EH no-wiggle IC spectrum at σ8 = 0.811;
- the flat w = −1 background with Planck-like constants;
- the Δ_ta(z) shell table, from a ΛCDM shell ODE;
- the survey nuisance priors;
- massless neutrinos.

There is NO HMcode, NO BAHAMAS and NO halo-model mass function in the verdict.

## 6. Outputs

All in the lane folder:
- `cfg596_pm.py`, the lean engine;
- `cfg596_validate.py` → `cfg596_validate.out` / `.json`;
- `run_596.py`, the launcher;
- `cfg596_native.py` → `cfg596_native.out` / `_results.json`, plus `_MUTATE` versions;
- `README.md`.

Arrays and logs go to `../_external_data/cfg596_work/`. Every number quoted comes from a JSON. Dated disclosures go in the README. This file is never edited.
