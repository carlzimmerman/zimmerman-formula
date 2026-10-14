# CFG650: the combined "theory v2 candidate" PM engine. Engine built and validated at 256³; the 1024³ test is queued behind a waiter that has not been started

- **Date:** 2026-10-12. Criteria: `FROZEN_CRITERIA.md`, commit 3087298c7. It was committed alone, before any CFG650 preview number and before any 1024³ run.
- **Settings:** κ = ½ is FITTED. The footings 9.3603e-11 / 1.1312e-10 are never pooled. "Cold energy" throughout; its MASS is still required; there is no particle species. Not "theory closed".
- **No verdict yet.** Every number below is a 256³ PREVIEW or an engineering check, NOT a verdict. No ΛCDM or standard-MOND yardstick is used. The S0 comparison is a benchmark against an inherited-input control, not an observational exclusion.

## Engine: `cfg650_pm.py`

The engine is `cfg596_pm.py` at 6323b630f plus switchable modules. Every switch defaults to OFF, and with all switches OFF it reproduces CFG596 bit for bit. sha256 of the file that ran every validation job: 771d556c153cdcbc….

| switch | module | spec used |
|---|---|---|
| `CFG650_M1` | Per-host supply. Each catchment cell goes to the host with the smallest d/r_ON; q, the cap and the shell draw are computed per host. | FINAL: CFG647 README plan + the `cfg647_audit.membership` rule |
| `CFG650_M2` | Condensed source: per-particle f_d; the MOND input is the f_d deposit. | FINAL: `cfg640_pm.py` @6b8a3776c, code copied |
| `CFG650_M3` | Gas expulsion: census non-retained baryons are removed from the source and re-placed with Gaussian σ = r_ON per catchment class. Mass is conserved exactly. | PRIMARY placement from CFG646's declarations (DIFF-S). CFG646's native PM spec is not committed (TODO in the code). |
| `CFG650_M4` | Phase-mixed gate: a 1-byte per-particle pericentre flag about the own host. Settling and the supply draw are weighted by the phase-mixed mass fraction φ. | PLACEHOLDER: CFG648 states the physics but has written no PM spec |
| `CFG650_M5` | Neighbour-bounded edge | STUB (raises): CFG644 has no PM spec |
| `CFG650_IC=As` | A_s-normalised ICs (declared bracket) | amplitude factor 1.0265 versus the σ8 = 0.811 normalisation (`ic_amp()`); this corresponds to a ΛCDM-back-scaled linear σ8 of 0.832 |

Every structural choice is listed in criteria §1 (S-a to S-f).

## Validation (`cfg650_validate.py` → `.out/.json`)

Settings: 256³, L100, NSEED 512, RMIN 0.78125, lean mode, one process at a time, nice 10. Peak RSS was 1.95–2.81 GB.

- **V-0 PASS.** All modules OFF equals CFG596 VLr bit for bit: 144 stored quantities over 6 snapshots, every difference exactly 0.
- **V-2 FAIL as literally frozen; cause diagnosed post-freeze.** M2 alone versus CFG640 VPh differs only in the z = 0 P_grav-derived quantities, by up to 1.4e-8. Everything else matches:
  - z = 0 positions and f_d are identical;
  - the full-resolution particle and gravitating fields are identical at every snapshot.
  - Re-measuring VM2's own z = 0 field in 10 fresh processes gave VPh's stored P_grav in 2 runs and VM2's in 8.

  So the multithreaded P(k) measurement of an identical array does not give bitwise-identical results from one run to the next, and the copied M2 code is not the cause. The orchestrator should note that V-2 is a "must pass" gate that failed literally.
- **V-C PASS for all 8 runs.**
  - |src_sum|/e_sum ≤ 2.3e-10.
  - M1: per-host imbalance ≤ 5.5e-8, 0 orphan cells.
  - M3: placement imbalance ≤ 1.9e-9. The expelled mass is 0.033–0.034 of all mass at z = 0.
  - M4: phase-mixed mass is 0.45 of all mass at z = 0, and 0.86 inside catchments.
- **V-D.** Each module alone moves in the intended direction (lower settled source and/or lower P_grav).

### PREVIEW, 256³, NOT a verdict

P_grav/P_S0 − 1 at z = 0 (S0 = CFG596 VLs):

| run | k = 0.3 | k = 0.5 | k = 1 | settled e_sum / all-OFF |
|---|---|---|---|---|
| all OFF (= CFG596) | +0.253 | +0.567 | +0.507 | 1.000 |
| M1 alone | +0.036 | +0.127 | +0.180 | 0.790 |
| M2 alone | +0.055 | +0.103 | +0.099 | 0.499 |
| M3 alone | +0.235 | +0.549 | +0.415 | 1.027 |
| M4 alone | +0.199 | +0.413 | +0.381 | 0.899 |
| M1+M2 | +0.005 | +0.014 | +0.031 | 0.357 |
| M1+M2+M3 | −0.022 | −0.037 | −0.048 | 0.359 |
| all ON (= T1) | −0.026 | −0.046 | −0.067 | 0.228 |

Values at z = 0.5 and z = 1 are in the `.out`. At 256³, M1 and M2 together remove almost all of the benchmark excess, and M3/M4 then turn it into a small deficit. This says nothing about raw KiDS/DES: only the 1024³ run scored on the data can.

**CMB-safety checklist:** CFG649 has not committed one, so it was not run.

## Scorer and pipeline check

- `cfg650_native.py` = `cfg640_native.py` pointed at T1/T2 (or T1x/T2x) and S0 = CFG596 P0.
- The growth gate is demoted to a labelled benchmark. The verdict rests on the raw-data classes only.
- The CMB gate is NOT EVALUATED unless CFG649 commits a raw-data form.
- `--test530` (pipeline test on CFG530 L100 N512, MUTATE first) reproduces CFG640's test530 Δχ² values exactly. Its outputs are committed as `cfg650_native*_test530*`; they are a pipeline test only.

## Queue: created, NOT started

- `run_650.py` jobs: T1 / T2 (M1+M2+M3+M4, canonical / alt), T1x / T2x (CFG648 clause), T1As / S0As (A_s bracket).
- `cfg650_waiter.sh`: starts `run_650.py serial $CFG650_JOB` (T1 by default, T1x allowed) when two conditions hold:
  - no cfg596/636/640/650 engine process is running;
  - free + inactive memory ≥ 48 GB.
- Production abort rule: RSS > 52 GB.
- Estimated wall time: 1–1.5 days. The 256³ all-ON run took 1.74× the wall time of the all-OFF run.
- Queue order versus CFG640 is the orchestrator's decision.

## Disclosures

- The 256³ previews were seen only after the criteria were committed. The combination (T1) was fixed by the §2 rule before the previews existed.
- The intended-direction outcome does not affect T1.
- The bit-for-bit reproduction claim (V-0) holds at 256³ with 3 threads. V-2 shows that the P(k) measurement can differ at the 1e-8 level from one run to the next.
- All verdicts will be conditional on the inherited inputs listed in criteria §7.

## Orchestrator decision on V-2 (2026-10-12)
V-2 ("M2 alone reproduces CFG640's VPh bit for bit") failed as literally frozen: only the z = 0 P_grav measurement differs,
by ≤ 1.4e-8, while positions, f_d and the full-resolution fields are identical at every snapshot; re-measuring the same
field in fresh processes reproduces either value (multithreaded P(k) reduction order). This is measurement nondeterminism
far below any statistic used, not an engine difference. Production proceeds with this disclosure; the frozen V-2 label
stays FAIL-as-written. Queue: T1 starts automatically after CFG640 H1 finishes (cfg650_waiter.sh, CFG650_JOB=T1); if
CFG648 commits a FAILS verdict for H-SP with the condensed source before launch, the waiter is restarted with T1x per §criteria.

## RESULT T12 (2026-10-14): M1+M2 (per-host supply + condensed source), canonical 1024³, vs CFG596 P0 — POST-PREVIEW selection (addendum A1)
Scored with `CFG650_JOBSET=T12 cfg650_native.py` (MUTATE first). Outputs `cfg650_native_T12.out/json`, `_MUTATE`.
- Own boost B(z=0) at k 0.3/0.5/1/2/4: 1.005 / 1.012 / 1.023 / 1.015 / 1.005 (CFG596: 1.19/1.25/1.21; CFG636: 1.058/1.056/1.056).
- **KiDS-1000: Δχ² +2.03** (robust max +3.28: widen2 1.26, noIA 2.88, held-out 2.36, DESI 1.50); T-OWN passes → **CONSISTENT**.
  Absolute: χ² F 146.29 (p 0.011) vs S0 144.26 (p 0.014) on 104 kept points — the framework fits as well as the same-pipeline
  control; both are marginal in absolute terms (the classifier is relative; codex audit eb4f5af3a).
- DES Y3: Δχ² +0.26 (robust ≤ 0.97), T-OWN fails → NOT DIAGNOSTIC.
- Benchmark (no verdict weight): G = 0.026, σ8_grav ratio 1.0018.
- Verdict per footing: **canonical PASS (shear side); alt PENDING.**
Caveats: post-preview selection (T1x is the primary pre-declared run); inherited ΛCDM ICs/background (CFG654 native rerun
pending); L100 box loses 54% (KiDS) / 77% (DES) of points; no baryonic feedback in either arm. κ = ½ fitted; not theory closed.
