# CFG622: merger stopwatch v4 (CFG621 rerun with a merger-safe lensing estimator)

- **Status (2026-10-11): VOID as frozen.** MUTATE gate **M2 FAILED**: at α = 0 the Harvey β̄ is +0.188, above the limit of 0.10.
  - Every verdict below is therefore an unvalidated number, not a result.
  - All the other gates passed: C1–C3, C4(a), C4(b), C5, C6, N_B, C7, the calibration check, M1 and M3.
- **Criteria:** `FROZEN_CRITERIA.md` (b358e376a), committed alone before any script or run. It states that CFG621's results had
  already been seen. Frozen text is never edited; later changes are the dated disclosures below.
- **What this lane fixes.** CFG621 disclosure B-D1: the lensing circles reached the other cluster, and an isolated-halo tolerance
  was applied to a merger.
  - The sub's lensing and cold-energy maps are masked to the sub's side of the bisector of the sub–main galaxy segment (estimator E-M).
  - An edge guard and a gas guard are added (75 kpc).
  - A merger-calibrated tolerance is used: T_M = max(T_L, 3 × P95) of the E-M spread over a control ensemble. The ensemble is
    α {0, ∞} × seeds {600, 601, 602} × each footing, disjoint from the seed-599 grid.
  - Nothing else changes from CFG621: model, data, calibration (v0 2666.7 km/s, η 1.132), scores, V-1..V-4, M1–M4, nodes.
- **Settings as CFG621:**
  - κ = ½ is FITTED. Both footings are kept and never pooled.
  - Kernel ν(y) = 1/(1 − e^(−√y)). Candidate B, G9, no EFE.
  - The cold energy's mass is required (an input). No particle species.
  - Yardsticks are raw data only. This is not "theory closed", and nothing here says the data favour the framework.

## Gates (JSON: `cfg622_controls_results.json`, `cfg622_results_MUTATE.json`, `cfg622_results.json`)

| gate | result |
|---|---|
| C1 Poisson / C2 Sod / C3 phantom / C4(a) / C5 / C6 (CFG621 control code re-run, unchanged) | PASS (2.83% / 1.12% / 0.13%; C4(a) ≤ 2.03 kpc) |
| C4(b) stage-A T-4, N_B (re-read) | PASS; N_B = 0.188 |
| 12 control runs; C7 mask null test at t = 0 | PASS. Masked and unmasked peaks agree to 0.000 kpc |
| T_M (B-2) | can: 300 epochs, median spread 10.8, P95 513.6 kpc → **T_M = 1540.9 kpc**; alt: 11.0 / 542.0 → **1625.8 kpc** |
| B-6 seed scatter | α = 0: σ_seed(f) 0.047 (N_M 0.38 can, 0.37 alt); α = ∞: N_M ≤ 0.01. No footing flagged |
| B-4 calibration check (α = 0, can, calib mode) | PASS. Speed 2699.4 km/s, d_SG 196.9 kpc (identical to CFG621) |
| M1 α = ∞: f ≥ 0.5 | PASS, f = 1.027 (stable) |
| **M2 α = 0: \|f\| ≤ 0.25 and β̄ ≤ 0.10** | **FAIL.** f = 0.181 passes, but β̄ = +0.188 (Harvey scorable, 50/50 epochs) |
| M3 roles swapped, α = ∞: f ≤ 0.25 | PASS, f = 0.235; the swapped α = 0 run gives 0.104 |
| M4 seed 600 − 599 at α = 0 (reported) | Δf = +0.031 |
| C8 reproduction vs CFG621 `runs_B` (reported) | Galaxy, gas and unmasked lensing peaks are identical (max difference 0) at every epoch of all 16 grid runs |

## Per-node numbers: UNVALIDATED (status VOID because M2 failed)

Sub halo; f at the 720-kpc epoch; Harvey β̄ over 0.1–0.6 Gyr after pericentre. "Stable" means the frozen B-3 rule. The spread
condition never binds, because T_M is about 1.5 Mpc, so stability is decided by the edge guard and the gas guard (`cfg622_results.json` → `cells`).

| α | foot | f | Z_B | Bullet stable | n_H used | β̄ | Z_H | as-run status |
|---|---|---|---|---|---|---|---|---|
| 0 | can | +0.181 | +1.09 | yes | 50/50 | +0.188 | +3.26 | EXCLUDED |
| 0.03 | can | +0.435 | +3.12 | yes | 50/50 | +0.301 | +4.87 | EXCLUDED |
| 0.1 | can | +0.803 | +6.07 | yes | 50/50 | +0.534 | +8.20 | EXCLUDED |
| 0.3 | can | +1.005 | +7.68 | yes | 50/50 | +0.981 | +14.58 | EXCLUDED |
| 1 | can | +1.418 | +10.98 | no (edge) | 0/50 | — | — | UNSCORABLE |
| 3 | can | +1.078 | +8.27 | yes | 16/50 | (1.107) | — | UNSCORABLE (Harvey < half) |
| 10 | can | +1.056 | +8.08 | yes | 41/50 | +1.055 | +15.64 | EXCLUDED |
| ∞ | can | +1.027 | +7.86 | yes | 48/50 | +0.988 | +14.68 | EXCLUDED |
| 0 | alt | +0.178 | +1.06 | yes | 50/50 | +0.170 | +2.99 | EXCLUDED |
| 0.03 | alt | +0.377 | +2.65 | yes | 50/50 | +0.286 | +4.65 | EXCLUDED |
| 0.1 | alt | +0.782 | +5.90 | yes | 50/50 | +0.544 | +8.34 | EXCLUDED |
| 0.3 | alt | +0.989 | +7.55 | yes | 50/50 | +0.984 | +14.63 | EXCLUDED |
| 1 | alt | +1.399 | +10.83 | no (edge) | 0/50 | — | — | UNSCORABLE |
| 3 | alt | +1.109 | +8.51 | no (edge) | 13/50 | (1.131) | — | UNSCORABLE |
| 10 | alt | +1.125 | +8.64 | yes | 41/50 | +1.057 | +15.67 | EXCLUDED |
| ∞ | alt | +1.052 | +8.06 | yes | 50/50 | +0.992 | +14.75 | EXCLUDED |

As-run verdicts (VOID, NOT results; `verdicts`):
- V-1 EXCLUDED (Z_B +7.86 / +8.06).
- V-2 NOT ALLOWED (only Harvey fails at α = 0; Bullet Z_B +1.09 / +1.06).
- V-3 INCOMPATIBLE.
- V-4 "NO alpha works".
None of these four is a result, because M2 failed.

## Reading (with the VOID status)

- **The merger-vs-galaxy α tension is still NOT a scored result.** The lane is VOID.
- What the unvalidated numbers show, on both footings:
  - **Bullet side:** α = 0 is the only node with |Z_B| < 2 (+1.09 / +1.06; now stable, which it was not in CFG621).
  - Every stable node with α ≥ 0.03 has Z_B ≥ +2.65 (α = 0.03, 0.1, 0.3, 10 and ∞).
  - α = 1 and 3 stay unscorable. At α = 1 the sub has no lensing peak of its own on the masked map: the peak is pressed against the
    mask edge (D-3).
  - So on the Bullet side, the unvalidated lean to α ≲ 0.03 is now made of stable cells (except α = 1 and 3). It stays in tension
    with the galaxy-side α ≳ 0.5. That is a stable-cell reading inside a VOID lane, not a verdict.
- **Harvey side:** the α = 0 failure is the M2 failure itself (D-2), so it cannot count against collisionless behaviour. It is a
  failure of the machinery check, and it voids the lane.

## Dated disclosures (2026-10-11, post-run; `cfg622_diag.py` → `cfg622_diag.out`, `cfg622_diag_results.json`; no verdict changed)

- **D-1 T_M is set by real two-peak configurations, not estimator noise.**
  - The large control spreads come from α = ∞ at t − t_peri ≈ 0.54–0.60 Gyr, about 6 epochs per run. There the sub–main distance
    is about 1.55–1.69 Mpc, so the mask is irrelevant.
  - In those epochs the primary (300, 75) peak sits on the stripped gas and cold energy, about 560–590 kpc from the galaxies. The
    smaller-start (200, 75) variant stays on the galaxies. The (400, 75) variant also deviates in those epochs, and (300, 90) does once.
  - The α = 0 controls show it at t − t_peri ≈ 0.15 Gyr, also driven by (200, 75).
  - The frozen 3 × P95 rule on this bimodal distribution gives T_M ≈ 1.5 Mpc, so condition B-3(a) is vacuous. This is a design
    flaw of B-2, stated as such: a stability tolerance cannot be calibrated as a percentile of a spread that is physically bimodal.
- **D-2 Why M2 fails, and why CFG621's M2 passed.**
  - At α = 0, in the first part of the Harvey window (t − t_peri < 0.2 Gyr, d_SG ≈ 114–200 kpc), the sub's lensing peak sits close
    to its gas, at β ≈ 0.4–0.95.
  - After that it drops to β ≈ 0.03–0.10. The masked and unmasked estimators agree here, so the mask is not the cause.
  - Grid, seed 599, canonical: β̄ is 0.678 over t < 0.2 and 0.066 over t ≥ 0.2; over all 50 epochs it is 0.188.
  - The six α = 0 controls give 0.159–0.209 over all epochs, and 0.048–0.068 for t ≥ 0.2.
  - CFG621's M2 pass (β̄ 0.082) came from its isolated-halo stability rule. That rule dropped exactly the epochs
    t − t_peri = 0.10, 0.12–0.20 (10 of 50; with this file's estimator β̄ is then 0.080).
  - So CFG621's M2 pass depended on the same stability filter that B-D1 found to be wrong for a merger.
  - A likely mechanism, not tested here: the α = 0 cold-energy halo is cored (CFG599's flat-cored central lensing map). Just after
    pericentre the sub's lensing peak is therefore set by the dense cool-core gas cloud until d_SG grows past about 200 kpc.
  - This is a property of the model's collisionless limit (case L, CFG599 cool core), not of the estimator. It means the
    Harvey-window statistic, as frozen since CFG599, is gas-contaminated at α = 0 in this model.
- **D-3 α = 1.** The masked primary sits 289–313 kpc from the sub galaxies (unmasked: 439–452 kpc, which is CFG621's peak). It is
  55–64 kpc from the bisector, below the guard of 75 kpc. The gas guard also fails in 22–24 of the Harvey epochs at α = 1. As
  stated in criteria §0, the mask moves this peak by construction. The edge guard correctly refuses to score it.
- **Not claimed:** any allowed α; any exclusion of α = 0; V-1 to V-4 as results; compatibility or incompatibility with the
  galaxy side.

## What a v5 would need (new frozen criteria first)

1. A machinery check M2 that is not gas-contaminated by construction, or a Harvey window that starts once d_SG ≥ about 200 kpc.
   This must be declared before any run, and justified by D-2's α = 0 controls only (not by the α grid).
2. A stability rule that does not take a percentile of a bimodal spread. For example: stable iff the variants agree with the
   primary within T_L on the masked map, with a separate rule for epochs that genuinely have two peaks (declared as unscorable,
   or as scored on the peak nearest the galaxies).
3. A test of the α = 0 early-peak mechanism (a cuspier cold-energy core, or the cool-core cloud removed) on controls only.

## Files

| file | what |
|---|---|
| `FROZEN_CRITERIA.md` | criteria (b358e376a) |
| `cfg622_sim.py` | CFG621 simulator with the masked lensing/cold estimator E-M and the guard distances |
| `cfg622_main.py` | phases `controls` → `cfg622_controls.out/_results.json`; `mutate` → `cfg622_MUTATE.out`, `cfg622_results_MUTATE.json`; `grid` → `cfg622.out`, `cfg622_results.json` |
| `cfg622_diag.py` → `.out`, `_results.json` | D-1 to D-3 (post hoc, reported only) |
| `runs/` | run cache: 12 controls, calibration check, 2 swapped, 16 grid (small JSON time series) |

Compute: nice -n 10, ≤ 4 processes of 1 thread. A long unrelated job shared the machine. Console logs were kept outside the
repo and deleted.
