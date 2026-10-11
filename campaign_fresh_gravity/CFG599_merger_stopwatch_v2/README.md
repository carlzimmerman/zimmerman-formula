# CFG599: merger stopwatch v2 (the CFG597 rerun) — VOID as frozen (control C4(b) failed on the isolated main)

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (8a10775bd), 2026-10-10. Frozen text is never edited; changes after
  the freeze are dated disclosures below.
- **Status: VOID.** C4(b) failed on the isolated main cluster. Its lensing–galaxy distance reached 18.17 kpc, against the
  15 kpc limit (`cfg599_results.json` → `C4b.main`). Under §5 no merger run is made until C4 passes. So **no merger number
  exists in this lane**: there is no calibration, no α grid, no Z per node and no MUTATE result.
  - Every verdict (V-1 instant re-settling, V-2 collisionless, V-3 galaxy-side compatibility, V-4) is **NOT ESTABLISHED**.
- Settings as CFG597: κ = ½ is FITTED. Both footings are kept and never pooled. The kernel is ν(y) = 1/(1 − e^(−√y)). Candidate
  B, G9, no EFE. The cold energy's mass is required (an input). No particle species. Yardsticks are raw data only. This is not
  "theory closed", and nothing here says the data favour the framework.

## What was built (all frozen fixes are implemented)

- `cfg599_lib.py` re-uses CFG597's grid, hydro, Poisson, CIC and phantom routines read-only. It adds:
  - the sub's cool core: 15% of the sub's gas as a Plummer cloud of gas parcels, a = 50 kpc, with ram-pressure drag of
    efficiency η against the grid gas (M-3b);
  - a mass-conserving bilinear gas projection;
  - one shrinking-circle peak estimator used for galaxies, gas and lensing (R0 300 → R_min 50 kpc). Gas starts from the
    mass-weighted centre.
- `cfg599_sim.py`: CFG597's settling dynamics, with
  - more particles (stars 160k/100k, cold energy 200k/100k, cloud 40k);
  - drag with exact momentum and energy return to the gas;
  - the four-variant lensing convergence check.
- `cfg599_main.py` holds the frozen pipeline. Its order is controls, then C4(b), then calibration by parallel bracketing on v0 and
  η, then the 16-run grid {0, 0.03, 0.1, 0.3, 1, 3, 10, ∞} × 2 footings, then scores per node with no α_max, then verdicts. MUTATE
  mode covers M1–M4.

## Controls

| control | result | source |
|---|---|---|
| C1 Poisson (CFG597 routine) | PASS, 2.83% ≤ 3% | `cfg599_controls_results.json` |
| C2 Sod | PASS, 1.12% | same |
| C3 phantom | PASS, 0.13% | same |
| C4(a) estimator on the exactly centred t = 0 main and sub | PASS, all peaks ≤ 0.7 kpc from the true centre (CFG597's estimator was off by 13.2 kpc here) | same |
| C5 settle conservation | PASS | same |
| C6 drag unit test | PASS: analytic law to 1e-7; momentum 5e-13; energy conserved | same |
| C4(b) isolated sub (with cloud), α = 1, 0.6 Gyr | PASS: gas 4.61, lensing 5.30 kpc; M(<300) −1.2% | `cfg599_results.json` |
| **C4(b) isolated main, α = 1, 0.6 Gyr** | **FAIL: lensing–galaxy 18.17 kpc > 15** (gas 9.03 kpc; M(<300) −0.4%) | same |
| K1, G1 calibration; M1–M3 | not run (gated on C4) | `cfg599.out`, `cfg599_MUTATE.out` |

## Dated disclosures (2026-10-10)

- **D-1 Calibration search form.** The frozen M-6 says "bisection". Before any run, the code was written as a parallel 4-way
  bracketing: the endpoints and 2 interior points first, then 3 interior points of the bracket that holds the target, for at
  most 4 rounds. That keeps the 4 processes busy. It was never executed, because C4(b) failed first.
- **D-2 C4(b) diagnosis** (`cfg599_c4_diag.py` → `.out` / `_results.json`; isolated halos only, no merger run).
  - **Only one epoch of 61 is above 15 kpc**, at t = 0.41 Gyr; the median is 1.82 kpc. At that epoch:
    - the primary peak (R_min 50) sits on a pixel-diagonal cold-energy fluctuation at (12.9, −12.5);
    - the frozen convergence variants give 9.0 / 2.2 / 0.8 / 0.8 kpc;
    - the galaxy peak is 0.6 kpc from the true centre.
  - **The same failure occurs without the settling machinery.** An isolated main at α = 0 (no drift, no OU, same seed) reaches
    18.0 kpc, with 3 epochs over 15. Its galaxy peak wanders up to 17.5 kpc from the true centre. So the fail is not OU or drift
    pulling the halo off-centre. M(<300) is stable in both runs.
  - The cause is that the main's central lensing map is flat-cored. Its cold-energy map within ±50 kpc is uniform to the
    10–20% per-pixel shot noise (printed in the `.out`). A 50 kpc shrinking circle therefore has no well-defined peak to ~15 kpc,
    and particle noise moves it.
  - So the frozen 15 kpc tolerance sits at this estimator's noise floor on a cored cluster. It is still a frozen fail.
- **D-3 Threshold mismatch found.** The merger-side stability rule (§3 O-2) accepts a lensing spread up to max(20 kpc, 0.1 d_SG).
  That is looser than C4's 15 kpc. The failing epoch's spread, 17.4 kpc, would have counted as "stable" in a merger cell. A
  rerun should make these consistent.
- **Not claimed:** any allowed α, that instant re-settling is excluded, that collisionless is allowed, or anything about
  compatibility with the galaxy-side α ≳ 0.5 (CFG558). CFG597's as-run lean (lensing pulled toward the stripped gas by α ≈ 1)
  stays an unvalidated reading.

## What a valid rerun (v3) needs, beyond CFG599's fixes (new frozen criteria first)

1. A peak estimator with noise below the C4 tolerance on cored halos. Options:
   - a larger final radius (the R_min = 75 variant stayed ≤ 11.1 kpc at α = 1, 11.6 at α = 0);
   - a smoothed-map peak;
   - or many more cold and star particles in the core. Freeze the variant before any run.
2. Or a C4 tolerance tied to the measured estimator noise on isolated halos (for example 3σ of the α = 0 isolated scatter),
   frozen in advance, together with the D-3 consistency between C4 and the merger stability rule.
3. Keep CFG599's other fixes unchanged: the mass-weighted gas start, the bilinear projection, every α node reported, no α_max,
   the Harvey window without ±0.1 Gyr, bracketed v0 and η calibration, and the cool-core drag model with its G1 gate
   (194 ± 50 kpc, η ∈ [0.1, 2.5]). G1 has not been tested yet, so the cool-core model is unvalidated.

## Files

| file | what |
|---|---|
| `FROZEN_CRITERIA.md` | the criteria (8a10775bd) |
| `cfg599_lib.py`, `cfg599_sim.py` | model, drag, projection, peaks |
| `cfg599_controls.py` → `.out`, `_results.json` | C1–C3, C4(a), C5, C6 |
| `cfg599_main.py` → `cfg599.out`, `cfg599_results.json`; `CFG599_MUTATE=1` → `cfg599_MUTATE.out`, `cfg599_results_MUTATE.json` | pipeline, stops VOID at C4(b) |
| `cfg599_c4_diag.py` → `.out`, `_results.json` | D-2 |
| `runs/` | the two isolated C4(b) time series |

Compute: nice -n 10, ≤ 4 processes of 1 thread, under 1 GB each.
