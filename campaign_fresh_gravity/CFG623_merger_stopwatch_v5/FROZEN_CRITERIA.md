# CFG623 FROZEN CRITERIA: merger stopwatch v5 (CFG622 rerun with a gas-safe Harvey window and a majority stability rule)

Date: 2026-10-11. Written and committed ALONE, before any CFG623 control, MUTATE or grid run and before any CFG623 scoring. The
only CFG623 runs made before this commit are the three controls-only mechanism runs of step 1 (`cfg623_mech.py`, α = 0,
canonical, seed 600; a diagnostic, not a verdict input). Nothing below may be edited after this commit; later changes go in dated
disclosures in the README.

κ = ½ is fitted. The cold energy's mass is still required (an input). No dark-matter particle is added. The theory is not
closed. Yardsticks are raw data only: no ΛCDM halo or baseline, no MOND force law. Nothing here will be phrased as "the data
favour the framework". α is the declared measured quantity. The only constants set from data are CFG621's two calibration
numbers (v0 = 2666.7 km/s, η = 1.132), held for every α and both footings (9.36e-11 canonical, 1.13e-10 alt; never pooled).

## 0. What has already been seen (stated before any choice below)

The author of this file has seen:
- CFG621's stage-A and stage-B results (cadc71eef, 3fccac215) and disclosure B-D1;
- CFG622's results (750dbf803): VOID because MUTATE M2 failed (α = 0 Harvey β̄ +0.188 > 0.10); every unvalidated per-node number
  in CFG622's README table (f, Z_B, β̄, Z_H, stability, as-run status for all 16 cells: α = 0 the only node with |Z_B| < 2,
  +1.09 / +1.06; α ≥ 0.03 stable nodes Z_B ≥ +2.65; α = 1 unscorable on the edge guard; α = 3 Harvey < half), and its
  disclosures D-1 (T_M ≈ 1.5 Mpc set by physically bimodal control spreads, α = ∞ late epochs with the primary on the stripped
  gas and cold energy ~570 kpc from the galaxies), D-2 (at α = 0 the sub's lensing peak sits near its gas, β ≈ 0.4–0.95, for
  t − t_peri < 0.2 Gyr where d_SG ≈ 104–200 kpc, then β ≈ 0.02–0.10; in the grid run and in all six α = 0 controls; CFG621's
  M2 pass relied on its stability rule dropping those epochs), D-3 (α = 1 masked peak pressed against the bisector);
- per-epoch d_SG and β of CFG622's twelve control runs (seeds 600–602; α = 0 and ∞ only), which show the α = 0 β falling below
  0.2 between d_SG ≈ 175 and 210 kpc on both footings;
- the step-1 mechanism test (`cfg623_mech.out`): hypothesis H as pre-declared NOT CONFIRMED (P1 fails:
  with the cloud removed from the lensing map the early BASE β̄ drops from +0.778 to +0.220, not to ≤ 0.15; the cold energy's own
  peak sits at β̄ +0.135 toward the gas). P2 holds formally (NC +0.085), but without the cloud the gas is stripped at once
  (d_SG ≈ 700–900 kpc), so NC is confounded. P3: a cuspier cold-energy core (NFW c = 10) removes the early peak (β̄ +0.095,
  offset 11 kpc vs 116 kpc in BASE). Reading: the cloud supplies most of the early offset and a flat cold-energy core is
  needed for it; the residual is the cored cold energy itself being pulled toward the cloud. No choice below depends on which
  part of H holds.

Every change below is motivated only by CFG622's D-1 and D-2, is fixed from the model's own scales and from controls only, and is
fixed without reference to which α it would favour. No other part of CFG622 is changed.

## 1. Copied from CFG622 unchanged (FROZEN_CRITERIA.md b358e376a; code imported read-only)

Data D1–D3 (f_obs = 0.045, σ_f = 0.125 PROVISIONAL; Harvey β = −0.04 ± 0.07; D3 sign level only); model M-1 to M-5b (CFG599 via
CFG621's `cfg621_sim.py`; grid, hydro, progenitors, cool-core cloud with drag η, case L, rule 2S drift + FIX-2 OU, no EFE,
particle numbers, seed 599 for the grid); the simulator and estimator of CFG622 (`cfg622_sim.py`: galaxy and gas peaks E-1,
merger-safe masked lensing and cold-energy peaks E-M with primary (300, 75) and variants (300, 60), (300, 90), (200, 75),
(400, 75), the edge guard and the gas guard at 75 kpc, the unmasked primary recorded for reference); α nodes
{0, 0.03, 0.1, 0.3, 1, 3, 10, ∞} × both footings = 16 grid runs; the 720-kpc epoch and f (O-4); S-1 Z_B = (f − 0.045)/0.125,
Z_H = (β̄ + 0.04)/0.07, no error inflation; S-2 ALLOWED iff scorable and |Z_B| < 2 and |Z_H| < 2, EXCLUDED iff scorable and not
allowed, else UNSCORABLE; no α_max, no interpolation; V-1, V-2, V-3, V-4 exactly as CFG622's code; the alt footing is VOID if
its α = 0 run misses K1 (2700 ± 200 km/s) or G1 (d_SG 194 ± 50 kpc); C1–C3, C5, C6 (CFG621 controls, unchanged code re-run);
C4(a), C4(b) and N_B = 0.188 re-read from CFG621 stage A; C7 mask null test (≤ 3 kpc at t = 0 of every control run); the
calibration check B-4 (α = 0, canonical, seed 599, calib mode: 2700 ± 200 km/s and 194 ± 50 kpc, η ∈ [0.1, 2.5]); seed scatter
B-6 (reported, flag only); MUTATE M1 (α = ∞: f ≥ 0.5), M2 (α = 0: |f| ≤ 0.25 AND β̄ ≤ 0.10), M3 (roles swapped, α = ∞: f ≤ 0.25),
M3 roles-swapped α = 0 and M4 (seed 600 vs 599 at α = 0, canonical) reported; M1 and M2 are the grid's α = ∞ and α = 0 canonical
runs; where a MUTATE score needs f or β̄ and the cell is unstable or unscorable, the as-run value is used for the gate.

Not changed, stated so: the Bullet statistic f is still read at the 720-kpc epoch, where d_SG ≈ 194–197 kpc (calibrated to the
observed Bullet, G1). The early-peak effect of D-2 is therefore part of the model's Bullet prediction at α = 0. That is a
like-for-like comparison with the observed Bullet configuration, not a contamination of it, and f is not touched.

## 2. The only changes (all from CFG622 D-1 / D-2)

B-1' **Harvey window from d_SG ≥ 4 a_cc = 200 kpc (from D-2).** The Harvey statistic β̄ (O-5) and the M2 β̄ use the epochs with
    t − t_peri ∈ [0.1, 0.6] Gyr AND d_SG ≥ 200 kpc (this replaces O-5's d_SG ≥ 50 kpc). Here a_cc = 50 kpc is CFG599's frozen
    Plummer scale of the sub's cool-core cloud (M-3b). The physical reason: at projected distance 4 a_cc a Plummer cloud's
    projected surface density is (1 + 16)^−2 ≈ 0.35% of its central value, and 16/17 ≈ 94% of its projected mass lies inside.
    So once the sub's gas peak (set by the cloud) is 4 a_cc from the galaxy peak, the cloud no longer overlaps the galaxy peak on
    the lensing map. The factor 4 is a declared round number. It agrees with the ~200 kpc that D-2's α = 0 controls suggest
    (seen, §0). It was not chosen from any α ≠ 0 result, and it is not varied. Window W = those epochs; scorable iff at least 10
    stable epochs and at least half of |W| are stable (O-5's counting rule applied to W). If d_SG never reaches 200 kpc in
    [0.1, 0.6] Gyr, W is empty and the cell is UNSCORABLE.
B-3' **Stability rule: strict-majority agreement (from D-1; replaces CFG622 B-2 and B-3(a)).** No percentile of a merger spread is
    taken, and T_M is dropped. An epoch is STABLE iff all three hold:
    - (a) at least 3 of the 4 E-M variants lie within T_L = 24.90 kpc of the E-M primary. T_L is CFG621 stage A's isolated-halo
      floor (3 × P95 over 48 isolated control runs), a controls-only number. 3 of 4 is the strict majority of the declared variants;
    - (b) CFG622's edge guard (no E-M lensing peak, primary or variant, within 75 kpc of the bisector), unchanged;
    - (c) CFG622's gas guard (the sub's gas peak at least 75 kpc on the sub's side of the bisector), unchanged.
    An epoch with two genuine peaks (the primary on one, most variants on the other) therefore fails (a) and is never scored.
    This applies to the Bullet bracketing epochs (both must be stable for f to be scorable) and to every Harvey epoch.
B-2' **Control ensemble and C9 (the stability rule checked on controls only).** α ∈ {0, ∞} × NEW seeds {603, 604, 605} × each
    footing (12 runs, disjoint from the seed-599 grid and from CFG622's control seeds), at CFG621's (v0, η). C9 passes iff, for
    every (α, footing) of the ensemble, the Bullet bracketing epochs are stable in at least 2 of 3 seeds AND the Harvey window is
    scorable in at least 2 of 3 seeds. A failing C9 means the rule cannot score even the two limiting models: VOID. Reported
    only: the number of control epochs in [0.1, 0.6] Gyr with the primary more than 300 kpc from the sub galaxies (D-1's two-peak
    epochs), and how many the rule flags unstable. C7 and B-6 run on this ensemble.
B-5' **C8 reproduction (reported, not a gate).** Every CFG623 run that CFG622 also ran (16 grid runs, calibration check, both
    swapped runs, seed 600) is compared epoch by epoch with CFG622's `runs/` (max difference of the galaxy, gas, masked and
    unmasked lensing peaks and the variants).

## 3. Gate order (every gate must pass, else every verdict is VOID with the failing gate named)

1. C1–C3, C5, C6 (re-run); C4(a), C4(b), N_B ≤ 1 (re-read).
2. The 12 control runs; C7; C9; B-6 reported.
3. Calibration check B-4.
4. MUTATE M1–M3 (runs M1, M2, M3; M3-α0 and M4 reported).
5. The 16-run grid; per-node Z_B, Z_H, status on both footings; V-1 to V-4.
The α scan counts only if 1–4 pass. If a gate fails, the remaining numbers may be reported only as unvalidated, labelled VOID.
The merger-vs-galaxy α tension (CFG621/622 unscored Bullet lean α ≲ 0.03 vs galaxy side α ≳ 0.5) counts as a scored result
only if the lane is VALID, and only through the frozen per-node statuses and V-2 / V-3 (no new statistic).

## 4. Compute and housekeeping

nice -n 10, ≤ 4 processes of 1 thread (a long unrelated 1024³ job shares the machine and is never stopped or starved). Run
cache (small JSON) in `runs/`; console logs outside the repo, deleted after. Outputs `cfg623_controls_results.json`,
`cfg623_results_MUTATE.json`, `cfg623_results.json` and `.out` files. README numbers come from the JSON. CFG599/621/622 are
read-only. Commit specific paths only; no push; never rewrite history.
