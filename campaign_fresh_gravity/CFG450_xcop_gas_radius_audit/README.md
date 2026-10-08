# CFG450: at what radius does the CFG382 target audit read the X-COP gas mass?

Criteria: `FROZEN_CRITERIA.md` (850262705, committed alone before the script). Script: `cfg450_gas_radius_audit.py`.
Outputs: `cfg450_gas_radius_audit.out`, `cfg450_results.json` (MUTATE: `*_MUTATE.*`).

**Verdict: NOT A BUG. The definition-A deficits are UNCHANGED. CFG431's robustness row R2 is the error, and it is invalid.**

- **Units (U1).** In all 12 X-COP `*_fgas_profile.fits` files the RADIUS column is in `R/R500`, not Mpc (TUNIT1).
  The header keyword R500 (kpc) normalises it. So `cfg382_target_audit.py`'s `interp(0.0, log RADIUS, ...)` reads the gas at
  R500, the same radius as the hydrostatic mass.
- **Cross-check (U2).** At RADIUS = 1, the fgas file's NFW mass matches the hydro file's NFW mass at the JSON R500 to within
  1.4% for all 12 clusters. The gas fraction there is 0.106–0.190, the usual f_gas,500 range.
- **Header vs JSON R500.** These differ for 3 clusters: A2029 −0.6%, A2319 +1.6% and A644 +1.6%. Reading the gas at the JSON
  R500 instead leaves every median unchanged to four decimals. The canonical shift is 0.
- **CFG431's R2 row.** It took RADIUS as Mpc and read the gas at R/R500 = 1.15–1.42, which is outside R500. That added gas and
  lowered the cluster e_med to 0.225. Its README premise ("the audit takes the gas mass at 1 Mpc") is wrong. The R2 row should
  not be cited.

## Deficits (definition A, gas at R500, 7 X-COP clusters; 20 Lovisari groups; median [16–84%]; never pooled)

| footing | b | clusters | groups |
|---|---|---|---|
| canonical 9.3603e-11 | 0 | 0.4135 [0.372–0.496] | 0.787 [0.53–1.40] |
| canonical 9.3603e-11 | 0.3 | 0.9054 [0.852–0.994] | 1.760 [1.38–2.61] |
| alt 1.1312e-10 | 0 | 0.3507 [0.307–0.440] | 0.649 [0.40–1.28] |
| alt 1.1312e-10 | 0.3 | 0.8426 [0.788–0.938] | 1.622 [1.25–2.48] |

The canonical rows are the CFG382 audit's numbers. The alt rows were not on disk before this lane.

## How T15, T16 and CFG431 move

- **Canonical footing: they do not move.** T15 and T16 hard-code the rounded 0.41/0.91 and 0.79/1.76. The unrounded values
  shift their outputs only in the third decimal: cluster f_max 0.0824 → 0.0831, C5 violation 3.95× → 3.92×, T16 intersection
  [0.0152, 0.0172] → [0.0152, 0.0171], floor/cluster gap 1.63×.
- **Alt footing (deficits only; T15/T16's other conventions held).**
  - T15: clusters M_cold/M_b −1.04 (b = 0) and −0.55 (b = 0.3). Groups b = 0.3 goes from +0.04 to −0.10, so the group
    knife-edge falls just below zero. Cluster f_max 0.0705, C5 violation 4.65×.
  - T16: clusters window [0.0062, 0.0158]; the intersection narrows to [0.0152, 0.0158] but stays nonempty; floor/cluster gap 1.77×.
  - Every T15/T16 sign conclusion survives: clusters are negative at every b, and the floor and the cluster budget cannot
    share one λ.
- **Disclosed: T15 and T16 use a third a0.** Their kernel supply S uses a0 = 1.2e-10, which is neither footing.
  - With S at the matching a0, canonical gives clusters −0.80 / −0.31, groups b = 0.3 +0.26, cluster f_max 0.095, C5 3.40×,
    and floor gap 1.40×.
  - Alt gives clusters −1.00 / −0.51, groups b = 0.3 −0.04, and floor gap 1.71×.
  - Signs are unchanged everywhere. The floor gap shrinks toward 1.4× on the canonical footing.
- **CFG431.**
  - Primary with gas at the JSON R500: the cluster e_med stays 0.413, but S goes 0.189 → 0.171 (the 3 header-mismatched
    clusters move a little). Cluster–group z 2.22 → 2.17, still NOT UNIVERSAL.
  - **R1-full at the alt footing** (groups and clusters at alt too, where CFG431's R1 moved only the galaxies): group S
    1.56, cluster–group z **1.95**, so the row becomes **CONSISTENT, NOT DIAGNOSTIC**. CFG431's "NOT UNIVERSAL" holds on the
    canonical footing only. That adds to its FRAGILE label; it does not reverse it.
  - R2 as committed: 0.225 / z 2.35 (invalid, see above).

## Controls
- C1 reproduces the audit: 0.413 / 0.905 and 0.787 / 1.760.
- C2 reproduces CFG431's R2: 0.225.
- C3 reproduces T15 and T16's committed JSON to 1e-9.
- MUTATE plants the Mpc read. The clusters fall to 0.225 / 0.611, the decision flips to MOVES (shift 0.295) as required,
  and every control still passes.
- **Disclosed fix after the first run.** The printed "R2 effective radius" used the wrong normalisation and showed about 1.0.
  It was fixed, and both runs were redone. No decision number changed.

## Caveats
- Seven clusters. The group stellar mass is the audit's placeholder (0.10 M_gas).
- The CFG431 rows reuse its galaxy sample from `_external_data/alabi2017` (outside the repo, read-only).
- Nothing in CFG382, CFG431 or deepseek_push was edited. Their READMEs still carry the old R2 statement.
