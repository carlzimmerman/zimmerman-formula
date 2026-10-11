# CFG621 FROZEN CRITERIA B: merger stopwatch v3 (stage B, the merger scan)

Date: 2026-10-10. Written and committed ALONE after the stage-A results (cadc71eef) and BEFORE any merger simulation of this lane
(no calibration run, no α-grid run, no MUTATE run exists). Nothing below may be edited after this commit; later changes go in
dated disclosures in the README.

κ = ½ is fitted. The cold energy's mass is still required (an input). No dark-matter particle is added. The theory is not
closed. Yardsticks are raw data only: no ΛCDM halo or baseline, no MOND force law. Nothing here will be phrased as "the data
favour the framework". α is the declared measured quantity; the only other constants set from data are CFG599's two
calibration numbers (v0, η), fixed once at α = 0 on the canonical footing and held for every α and both footings. No other knob.

## 0. Question

As CFG599 §0: do the Bullet Cluster offsets (Clowe+06) and the Harvey+15 ensemble constrain the settling rate α of cold energy
(CFG541 class-A drift toward the round phantom of the CURRENT baryons + CFG544 FIX-2 OU relaxation, no EFE)? Is instant
re-settling (α = ∞) excluded? Is pure collisionless behaviour (α = 0) allowed? Is the merger side compatible with the
galaxy-side α ≳ 0.5 (CFG558)?

## 1. What is copied from CFG599 unchanged (FROZEN_CRITERIA.md 8a10775bd; code imported read-only)

§1 data D1–D3 (f_obs = 0.045, σ_f = 0.125 PROVISIONAL; Harvey β = −0.04 ± 0.07; D3 sign level only); §2 the model M-1 to
M-5b (grid, hydro, progenitors, the sub's cool-core cloud with ram-pressure drag η, case L, rule 2S drift + FIX-2 OU, α nodes
{0, 0.03, 0.1, 0.3, 1, 3, 10, ∞} on both footings = 16 production runs, particle numbers, seed 599); §2 M-6 calibration (K1:
galaxy relative speed 2700 ± 200 km/s at the first post-pericentre 720-kpc epoch; G1: sub d_SG 194 ± 50 kpc at that epoch;
η ∈ [0.1, 2.5]; v0 searched on [0, 4000] km/s at η = 1 first, then log η on [0.03, 10], at most two rounds; the alt footing's
α = 0 run must also meet K1 and G1, else the alt cells are VOID); §3 O-1 projections, O-3 β(t), O-4 the Bullet statistic f at
t_obs, O-5 the Harvey statistic β̄ over t − t_peri ∈ [0.1, 0.6] Gyr (≥ 10 qualifying epochs and ≥ half of the window, each with
d_SG ≥ 50 kpc and a stable lensing peak); §4 S-1 Z_B = (f − 0.045)/0.125, Z_H = (β̄ + 0.04)/0.07, no numerical error inflation;
S-2 ALLOWED iff scorable and |Z_B| < 2 and |Z_H| < 2, EXCLUDED iff scorable and not allowed, else UNSCORABLE; no α_max, no
interpolation; V-1 (α = ∞ EXCLUDED iff Z_B ≥ 3 on both footings), V-2 (α = 0 ALLOWED iff allowed on both footings), V-3
(COMPATIBLE iff α = 1 allowed on both footings; PARTIAL iff not, but some node in {3, 10, ∞} is; INCOMPATIBLE otherwise),
V-4 summary; §6 MUTATE M1 (α = ∞: f ≥ 0.5), M2 (α = 0: |f| ≤ 0.25 AND β̄ ≤ 0.10), M3 (roles swapped, α = ∞: f ≤ 0.25),
M4 seed 600 reported only.
The calibration search is CFG599's parallel 4-way bracketing (CFG599 README D-1; declared here as the search form): round 1
evaluates the two endpoints and two interior points, later rounds three interior points of the sub-bracket holding the target,
at most 4 rounds, stopping inside ±100 km/s (K1) / ±25 kpc (G1).

## 2. The only changes (from stage A, FROZEN_CRITERIA_A.md 3dcb3a075, results cadc71eef)

B-1 Estimator: E-1, the shrinking circle with R0 = 300, **R_min = 75 kpc** for galaxy, gas and lensing (all positions, both in
    the calibration epochs and in the scores); lensing spread over the E-2 variants (300, 60), (300, 90), (200, 75), (400, 75).
    Code: `cfg621_sim.py` (CFG599's simulator with this estimator only).
B-2 **Lensing stability rule: STABLE iff spread ≤ T_L = 24.90 kpc** (`cfg621_stageA_results.json` → `T_L`), identical to the C4
    lensing tolerance. CFG599's max(20 kpc, 0.1 d_SG) is dropped.
B-3 **C4(b) = stage-A T-4**: every epoch of every one of the 48 isolated runs has d_L ≤ T_L = 24.90 kpc and d_G ≤ T_G = 14.70 kpc,
    and |M(<300) drift| ≤ 10%. (Measured in stage A: PASS. The pipeline re-reads it from the JSON.)
B-4 C4(a) as CFG599 (the exactly centred seed-599 isolated main and sub at t = 0: gas, galaxy and lensing peaks within 3 kpc of
    the true centre) evaluated with E-1. (Stage-A disclosure A-1: seed 622 would not meet 3 kpc; the frozen check is seed 599.)
B-5 N_B = 0.188 ≤ 1 (stage A R-3): the Bullet score is diagnostic.

## 3. Gate order (every gate must pass, else every verdict is VOID with the failing control named)

1. C1–C3, C4(a), C5, C6: CFG599's control code re-run with E-1 (`cfg621_controls.py`).
2. C4(b) (B-3) and B-5.
3. Calibration K1 + G1 + η range at α = 0, canonical (CFG599 M-6). Equivalently: the α = 0 control must give speed 2700 ± 200 km/s
   and d_SG 194 ± 50 kpc with η ∈ [0.1, 2.5].
4. MUTATE M1–M3 at the calibrated (v0, η) (`CFG621_MUTATE=1`, separate `_MUTATE` outputs).
5. The 16-run α grid; per-node Z_B, Z_H, status on both footings; V-1 to V-4. The alt footing is VOID if its α = 0 run misses
   K1 or G1.
The α scan counts only if 1–4 pass. If a gate fails, the remaining merger runs may still be reported as unvalidated numbers,
labelled VOID, never as verdicts.

## 4. Compute and housekeeping

nice -n 10, ≤ 4 processes of 1 thread, ≤ 2 GB each. Outputs: `cfg621_controls.out/_results.json`, `cfg621.out`,
`cfg621_results.json`, `cfg621_MUTATE.out`, `cfg621_results_MUTATE.json`, run cache `runs_B/`. README numbers come from the JSON.
CFG599/CFG597 read-only. Commit specific paths only; no push; never rewrite history.
