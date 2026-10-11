# CFG623: merger stopwatch v5 (CFG622 rerun with a gas-safe Harvey window and a majority stability rule)

- **Status (2026-10-11): VALID as frozen.** Every gate passed: C1–C6, C4(b), N_B, C7, C9, the calibration check, and M1–M3.
- **Criteria:** `FROZEN_CRITERIA.md` (bd135f5c2). It was committed alone, before any control, MUTATE or grid run, and states
  that CFG621/622's results and the step-1 mechanism test had been seen. Frozen text is never edited.
- **Changes from CFG622 (only these, both from CFG622's D-1 and D-2):**
  - (a) The Harvey and M2 window uses epochs with t − t_peri ∈ [0.1, 0.6] Gyr AND d_SG ≥ 4 a_cc = 200 kpc. Here a_cc = 50 kpc
    is CFG599's cool-core Plummer scale.
  - (b) An epoch is stable iff at least 3 of the 4 masked variants lie within T_L = 24.90 kpc of the masked primary, AND it
    passes CFG622's edge guard and gas guard. T_M is dropped.
  - C9 checks rule (b) on a new control ensemble: α {0, ∞} × seeds {603, 604, 605} × both footings.
- **Unchanged from CFG622:** the simulator and estimator (`cfg622_sim.py`, read-only), the data, the calibration
  (v0 2666.7 km/s, η 1.132), f at the 720-kpc epoch, the scores, V-1..V-4, M1–M4, and the nodes × both footings.
- **Settings:**
  - κ = ½ is FITTED. Both footings (9.36e-11 canonical, 1.13e-10 alt) are kept and never pooled.
  - The cold energy's mass is required (an input). No particle species.
  - Yardsticks are raw data only. This is not "theory closed", and nothing here says the data favour the framework.

## Step 1: mechanism test (controls only, α = 0, canonical, seed 600; diagnostic, not a verdict input)

`cfg623_mech.py` → `cfg623_mech.out`, `cfg623_mech_results.json`, `runs_mech/`; commit 1539fd142.

| run | early β̄ (t − t_peri 0.1–0.2 Gyr) | late β̄ (0.2–0.6) | early offset along the gas direction (post hoc) |
|---|---|---|---|
| BASE total map | +0.778 | +0.067 | 116 kpc |
| BASE, cloud removed from the lensing map | +0.220 | +0.058 | 32 kpc |
| BASE cold-energy peak only | +0.135 | +0.048 | 20 kpc |
| NC (cloud mass returned to the smooth gas) | +0.085 | +0.020 | 68 kpc (d_SG 700–900 kpc: gas stripped at once) |
| CUSP (sub's cold energy NFW c = 10, same mass) | +0.095 | +0.037 | 11 kpc |

- **Hypothesis as pre-declared: NOT CONFIRMED.**
  - **P1 fails.** With the cloud removed from the map, the early β̄ drops to +0.220, not to ≤ 0.15.
  - **P2 holds only formally.** NC is confounded: β is divided by a d_SG that is 4–5× larger.
  - **P3: yes.** A cuspier core removes the early peak.
- **Reading.** The cloud supplies most of the early offset (0.78 → 0.22). A flat cold-energy core is needed for the effect: with
  a cusp, the offset is 11 kpc while the gas is only 100–150 kpc away. The residual comes from the cored cold energy itself
  sitting toward the cloud (β̄ 0.135).
- BASE reproduces CFG622's seed-600 control exactly. The CUSP run changes the calibration (d_SG 151 kpc at the Bullet epoch).

## Gates (JSON: `cfg623_controls_results.json`, `cfg623_results_MUTATE.json`, `cfg623_results.json`)

| gate | result |
|---|---|
| C1 Poisson / C2 Sod / C3 phantom / C4(a) / C5 / C6 (CFG621 code re-run) | PASS (2.83% / 1.12% / 0.13%; C4(a) ≤ 2.03 kpc) |
| C4(b), N_B (re-read) | PASS; N_B = 0.188 |
| C7 mask null test (12 new controls) | PASS, 0.000 kpc |
| **C9 stability rule on controls** | **PASS.** Bullet stable / Harvey scorable: α = 0 can 2/3 / 3/3; α = ∞ can 3/3 / 3/3; α = 0 alt 3/3 / 3/3; α = ∞ alt 3/3 / 3/3 |
| B-4 calibration check | PASS. 2699.4 km/s, d_SG 196.9 kpc |
| M1 α = ∞: f ≥ 0.5 | PASS, f = 1.027 (stable) |
| **M2 α = 0: \|f\| ≤ 0.25 and β̄ ≤ 0.10** | **PASS.** f = 0.181, β̄ = +0.063 (39/39 window epochs stable). On CFG622's window the same run gives +0.188 |
| M3 swapped α = ∞: f ≤ 0.25 | PASS, f = 0.235 (swapped α = 0: 0.104) |
| M4 seed 600 − 599 (reported) | Δf = +0.031 |
| C8 reproduction vs CFG622 `runs/` (reported) | max difference 0 kpc over 20 runs, all peaks and variants |
| B-6 seed scatter (reported) | α = 0 N_M 0.44 can / 0.21 alt; α = ∞ ≤ 0.02. No footing flagged |

- **Two-peak control epochs (reported).** In 165 control epochs the primary lies more than 300 kpc from the sub galaxies, all at
  α = ∞. In 135 of them, 3 or 4 variants agree: these are single peaks on the gas, as expected for α = ∞. The 30 bimodal
  epochs (D-1 type: 1–2 variants agree) are flagged unstable.

## Per-node results (sub; `cfg623_results.json` → `cells`)

| α | foot | f | Z_B | Bullet stable (agreeing variants) | Harvey used/window | β̄ | Z_H | status |
|---|---|---|---|---|---|---|---|---|
| 0 | can | +0.181 | +1.09 | yes (3, 3) | 39/39 | +0.063 | +1.47 | **ALLOWED** |
| 0.03 | can | +0.435 | +3.12 | no (1, 2) | 38/39 | +0.156 | (+2.80) | UNSCORABLE |
| 0.1 | can | +0.803 | +6.07 | yes | 29/39 | +0.416 | +6.51 | EXCLUDED |
| 0.3 | can | +1.005 | +7.68 | yes | 38/38 | +0.968 | +14.40 | EXCLUDED |
| 1 | can | +1.418 | +10.98 | no (edge guard) | 0/39 | — | — | UNSCORABLE |
| 3 | can | +1.078 | +8.27 | yes | 3/39 | (1.084) | — | UNSCORABLE (Harvey < half) |
| 10 | can | +1.056 | +8.08 | yes | 19/39 | (1.045) | — | UNSCORABLE (Harvey < half) |
| ∞ | can | +1.027 | +7.86 | yes | 32/38 | +1.012 | +15.03 | EXCLUDED |
| 0 | alt | +0.178 | +1.06 | yes (3, 4) | 39/39 | +0.061 | +1.44 | **ALLOWED** |
| 0.03 | alt | +0.377 | +2.65 | no (2, 2) | 39/40 | +0.164 | (+2.92) | UNSCORABLE |
| 0.1 | alt | +0.782 | +5.90 | yes | 37/39 | +0.441 | +6.87 | EXCLUDED |
| 0.3 | alt | +0.989 | +7.55 | yes | 39/39 | +0.978 | +14.54 | EXCLUDED |
| 1 | alt | +1.399 | +10.83 | no (edge guard) | 0/39 | — | — | UNSCORABLE |
| 3 | alt | +1.109 | +8.51 | no | 2/40 | (1.103) | — | UNSCORABLE |
| 10 | alt | +1.125 | +8.64 | yes | 11/39 | (1.036) | — | UNSCORABLE (Harvey < half) |
| ∞ | alt | +1.052 | +8.06 | yes | 33/40 | +1.016 | +15.09 | EXCLUDED |

Values in parentheses are not scores: either the cell is unscorable, or one of its two statistics is unscorable.
- At α = 1 and 3, the Harvey epochs fail the edge guard (33–39 epochs) and the gas guard (14–24 epochs).
- At α = 10, they fail the majority rule (16 / 27 epochs).

**Frozen verdicts (VALID):**
- **V-1: instant re-settling EXCLUDED.** Z_B +7.86 / +8.06, stable.
- **V-2: pure collisionless ALLOWED** on both footings.
- **V-3: INCOMPATIBLE.** No node with α ≥ 1 is allowed on both footings. α = 1, 3 and 10 are UNSCORABLE, not excluded; α = ∞ is
  EXCLUDED.
- **V-4:** "collisionless component that re-settles slowly; allowed nodes listed". The allowed set is {0} on both footings.

## Reading

- **The Bullet + Harvey data, scored through this model, allow only α = 0.** They exclude α = 0.1, 0.3 and ∞ on both footings.
- **The merger-vs-galaxy α tension is now a scored result, but only in this limited form.** The merger side allows α = 0 and
  excludes α = 0.1 and 0.3. The galaxy side wants α ≳ 0.5. The galaxy-side nodes α = 1, 3 and 10 are UNSCORABLE here, not
  excluded. So V-3 INCOMPATIBLE is the literal frozen verdict ("no node α ≥ 1 allowed"). It is not a measured exclusion of
  α ≈ 1–10.
  - Their as-run Z_B of +8 to +11 is not a score.
  - α = 0.03 is also unscored.
- **What the α = 0 pass depends on (stated plainly):**
  - **It depends on change (a).** On CFG622's window (d_SG ≥ 50 kpc) the same run gives β̄ +0.188, Z_H +3.26.
  - **Threshold sensitivity (R-1, post hoc, `cfg623_diag.out`).** α = 0 Z_H is +1.86 / +1.56 / +1.47 / +1.38 / +1.34 (can)
    at thresholds 150 / 175 / 200 / 225 / 250 kpc. It stays below 2 across that range, though only just at 150. The exclusions
    of α = 0.1, 0.3 and ∞ hold at every threshold (Z_H ≥ 6.2).
  - **The α = 0 Bullet cell is stable by the minimum margin.** Exactly 3 of 4 variants agree at both canonical bracketing
    epochs. One of three canonical control seeds (605) fails there with 1 agreeing variant (R-2).
  - **The Harvey σ = 0.07 is used without inflation**, as frozen.
- **Mechanism (step 1).** The early α = 0 offset that voided CFG622 is mostly the cool-core cloud acting on a flat-cored cold
  energy. As pre-declared, the cloud-only hypothesis was NOT CONFIRMED (a 0.22 residual remains). The mechanism test is a
  diagnostic, not a verdict input.
- **Not claimed:**
  - any α_max or interpolation between nodes;
  - any statement that the data favour the framework;
  - κ derived;
  - "theory closed".

## Disclosures (2026-10-11)

- **Shared-machine constraint.** During this lane's grid phase (4 processes, about 10 GB RSS in total), an unrelated 1024³ job
  (CFG596 P1) was aborted at 10:56 by its own swap-growth guard while lane jobs competed for RAM. No CFG623 process signalled
  it. After the grid, this lane launched no new heavy batch; only light single-process post-hoc scripts were run. The CFG623
  numbers are unaffected: C8 reproduces CFG622 exactly.
- The step-1 kpc offsets were added after the mechanism runs and are reported only. The declared P1–P3 reading was not changed.

## Files

| file | what |
|---|---|
| `FROZEN_CRITERIA.md` | criteria (bd135f5c2) |
| `cfg623_mech.py` → `.out`, `_results.json`, `runs_mech/` | step-1 mechanism test (controls only) |
| `cfg623_main.py` | phases `controls` / `mutate` / `grid` → `cfg623_controls.*`, `cfg623_MUTATE.out` + `cfg623_results_MUTATE.json`, `cfg623.out` + `cfg623_results.json` |
| `cfg623_diag.py` → `.out`, `_results.json` | post-hoc R-1 threshold sensitivity, R-2 Bullet majority margin (reported only) |
| `runs/` | run cache: 12 controls, calibration check, M3 swaps, seed 600, 16 grid |

Compute: nice -n 10, ≤ 4 processes of 1 thread. Console logs were kept outside the repo and deleted.
