# X21_cluster_switch_anatomy: is the cluster "switch" a threshold, a trend, or a binning artefact? What does the excess track?

Criteria: `FROZEN_CRITERIA.md` (committed alone, a48f6d5e08). Amendments: A1 (after RUN1's step 0, before any graded number,
eeec96f440) and A2 (POST-RESULT, check code only). Inputs and classes: `ASSUMPTION_LEDGER.md`. κ = ½ FITTED. Footings
9.3603e-11 / 1.1312e-10 m s⁻², never pooled. No dark-matter particle. Not "theory closed". Nothing here says the data favour
the framework. Every number below is in `x21_switch_anatomy.out` / `x21_switch_anatomy_results.json`.

## Verdicts (frozen classes)

- **Trend: UNDECIDED** (`trend_verdict`).
  - No variable shows a threshold.
  - **KT is the only variable DETECTED** (max Δχ² 9.13 / 9.72 / 9.24 / 9.83 against the line 9; 106 clusters). Its shape is
    UNRESOLVED by the frozen rule.
    - The joint fit carries it as a slope: Z_b = 2.00 / 2.01 / 2.01 / 2.03, Z_c = −0.20 to −0.16. The canonical h 0.672 cell
      sits at Z_b = 1.9985, 0.0015 below the SMOOTH line.
    - The scanned step is not significant: p_scan 0.023–0.028 against 0.01.
  - MGAS500 itself, unbinned, is **NONE** (max Δχ² 3.46–3.86).
  - So the result is neither BINNING ARTEFACT (KT is detected) nor REAL THRESHOLD.
- **Budget: BARYON BUDGET INSUFFICIENT** (`budget_verdict`).
  - The generous bracket of omitted known baryons falls short of the central-mass need by ×4.1–5.5 in T2 and ×5.3–6.7 in T3.
  - The ICL would have to be 12.6–16.8 × all measured stars in T3 (9.2–13.3 in T2), above CFG922's ×10 scale.
  - The mass dependence is a **MISMATCH** in all 4 cells: the stellar fraction falls with mass while the need rises.

Cells are always given in the order canonical h 0.672 / canonical h 0.686 / alt h 0.672 / alt h 0.686.

## Step 0: X7 and X13 reproduced from committed arrays (K0 PASS)

- **X7.** The all-cluster A_MID, and the tercile and quintile A_CAL and σ_STAT, match X7's JSON to 4.4e-16 (76 numbers).
- **X13.** The all-source A and Z_STAT match X13 to 1.8e-15.
- **S0-b.** X7's CAL Δχ² reproduces to 0.000, with the declared σ_leak,b approximation.

| cell | A_MID (Z_STAT) | X7 Z_CAL | X13 selection-corrected halves (quoted) | X7 terciles A_CAL | X7 quintiles A_CAL |
|---|---|---|---|---|---|
| can h0.672 | 1.640 (+5.21) | +2.93 | 1.657 ± 0.138 (Z 4.77) | 1.10 / 1.85 / 1.84 | 1.45 / 1.24 / 1.82 / 1.38 / 2.19 |
| can h0.686 | 1.684 (+5.47) | +2.78 | 1.703 ± 0.141 (4.99) | 1.11 / 1.92 / 1.88 | 1.48 / 1.24 / 1.88 / 1.43 / 2.26 |
| alt h0.672 | 1.505 (+4.47) | +2.52 | 1.520 ± 0.126 (4.11) | 1.00 / 1.70 / 1.69 | 1.32 / 1.13 / 1.67 / 1.26 / 2.02 |
| alt h0.686 | 1.545 (+4.74) | +2.41 | 1.562 ± 0.129 (4.35) | 1.02 / 1.76 / 1.73 | 1.35 / 1.13 / 1.72 / 1.32 / 2.08 |

This lane never splits sources, so X13's selection correction does not apply to any number here.

## Step 2: the unbinned tests (C\*, CAL, boost; σ = max(bootstrap 2000, 30-patch jackknife); 2000 permutations)

Z_lin is the linear slope. Z_med is the median step. Z_b and Z_c come from the joint slope + median-step fit. p_scan is the
permutation p of the best of 13 step locations, with the look-elsewhere effect included. Z_b|M is the slope at fixed MGAS500
(reported only). Ranges run over the 4 cells.

| V | n | ρ(V, MGAS500) | Z_lin | Z_med | Z_b / Z_c | p_scan (best break) | p_perm(slope) | Z_b\|M | class |
|---|---|---|---|---|---|---|---|---|---|
| V0 MGAS500 (control) | 326 | 1.00 | 1.86–1.96 | 1.09–1.30 | 1.66–1.82 / −0.91 to −0.60 | 0.0125–0.014 (7.92e12 M☉) | 0.0035–0.0055 | — | NONE |
| V1 KT | 106 | +0.58 | **3.02–3.14** | 2.28–2.41 | 2.00–2.03 / −0.21 to −0.16 | 0.023–0.028 (1.33 keV) | 0.0045–0.006 | 1.67–1.71 | **DETECTED (shape unresolved)** |
| V2 redshift | 326 | +0.44 | 1.48–1.86 | 2.43–2.91 | −0.80 to −0.57 / 2.03–2.43 | 0.04–0.10 (z 0.223) | 0.035–0.058 | 0.58–0.89 | WEAK |
| V3 L500 | 326 | +0.90 | 2.50–2.79 | 2.05–2.30 | 1.52–1.59 / −0.30 to −0.11 | 0.007–0.0105 | 0.002–0.0025 | 1.03–1.52 | WEAK |
| V4 c_X = L300kpc/L500 | 326 | −0.67 | 0.26–0.39 | 0.39–0.47 | ≈ 0 / 0.21–0.31 | 0.81–0.86 | 0.62–0.74 | 2.26–2.36 | NONE |
| V5 redMaPPer λ | 83 | +0.62 | 2.23–2.64 | 1.25–1.82 | 2.19–2.38 / −1.25 to −0.80 | 0.10–0.18 | 0.010–0.035 | 1.24–1.92 | WEAK |
| V6 BCG stellar mass | 190 | +0.52 | 0.86–0.88 | 0.54–0.73 | 0.45–0.69 / −0.25 to 0.05 | 0.43–0.45 | 0.36–0.37 | 0.41–0.51 | NONE |
| V7 S_cen / gas_cyl | 242 | −0.10 | 0.35–0.64 | 1.19–1.27 | −1.06 to −0.65 / 1.30–1.49 | 0.23–0.35 | 0.42–0.65 | 0.51–0.79 | NONE |

**Re-binned A_MID,CAL tables** (binned GLS with X7's CAL covariance, reported and never graded; full tables for all cells in
the `.out`; shown here: canonical h 0.672 | alt h 0.672):

| V, bins (edges) | canonical h 0.672 | alt h 0.672 | Δχ² S1 / S2 (can) |
|---|---|---|---|
| MGAS500 terciles (7.37e12, 1.73e13) | 1.10±0.32 / 1.85±0.17 / 1.84±0.17 | 1.00±0.29 / 1.70±0.16 / 1.69±0.15 | 1.98 / 4.10 |
| MGAS500 quintiles | 1.45±0.59 / 1.24±0.31 / 1.82±0.21 / 1.38±0.29 / 2.19±0.20 | 1.32 / 1.13 / 1.67 / 1.26 / 2.02 | 4.58 / 2.86 |
| KT terciles (1.40, 2.33 keV) | 1.10±0.38 / 1.65±0.32 / 2.13±0.25 | 1.00±0.34 / 1.51±0.29 / 1.96±0.23 | 5.03 / 3.82 |
| z terciles (0.155, 0.292) | 1.43±0.23 / 1.79±0.17 / 1.84±0.25 | 1.31 / 1.65 / 1.69 | 1.35 / 1.89 |
| z quintiles | 1.39 / 1.34 / 1.98 / 1.89 / 1.88 (±0.20–0.40) | 1.27 / 1.23 / 1.82 / 1.73 / 1.73 | 2.06 / 4.11 |
| L500 terciles (28.0, 76.2) | 1.26±0.26 / 1.69±0.20 / 1.99±0.16 | 1.15±0.24 / 1.55±0.19 / 1.83±0.15 | 4.68 / 3.41 |
| L500 quintiles | 0.83±0.43 / 1.77 / 1.66 / 1.80 / 1.98 (±0.21–0.31) | 0.76 / 1.62 / 1.52 / 1.65 / 1.82 | 2.88 / 1.67 |
| c_X terciles (0.642, 0.796) | 1.60±0.18 / 1.72±0.20 / 1.58±0.36 | 1.47 / 1.58 / 1.45 | 0.04 / 0.12 |
| λ terciles (30.4, 52.0) | 1.31±0.42 / 1.91±0.37 / 2.43±0.30 | 1.20 / 1.75 / 2.24 | 4.59 / 3.56 |
| M_BCG terciles (3.19e10, 1.00e11) | 1.61±0.27 / 1.75±0.26 / 2.07±0.24 | 1.48 / 1.61 / 1.90 | 1.58 / 0.89 |
| S_cen/gas_cyl terciles (0.021, 0.050) | 1.74±0.22 / 1.44±0.23 / 2.11±0.31 | 1.60 / 1.32 / 1.93 | 0.33 / 0.05 |

## Step 3: baryon budget (`budget`, `mass_dependence`)

- **The need.** "Need" is the extra central point mass (X2's PS component, sourcing AQUAL) that brings A_MID,CAL to 1. A
  central mass is the most efficient placement per unit mass.
- **The bracket.** It is the generous upper end:
  - 2.12 × CFG922 A1 S_up × (1 + HI 0.196 + H₂ 0.196), counted wholly as omitted;
  - inside R < 0.5 Mpc;
  - over the 281 clusters matched to CFG922's census.

| selection | A_MID (can / alt, h0.672) | need λ_PS (× Mg500), 4 cells | need Σ (can h0.672) | generous bracket Σ | need / bracket (4 cells) | k_ICL (4 cells) |
|---|---|---|---|---|---|---|
| all | 1.640 / 1.505 | 1.05 / 1.17 / 0.82 / 0.92 | 5.73e15 M☉ | 1.19e15 | 4.8 / 5.1 / 3.7 / 4.0 | 11.3 / 12.1 / 8.1 / 8.8 |
| T1 | 1.096 / 1.002 | 0.21 / 0.26 / 0.005 / 0.04 | 8.1e13 | 1.56e14 | 0.5 / 0.6 / 0.0 / 0.1 | < 0 |
| T2 | 1.852 / 1.698 | 1.67 / 1.89 / 1.34 / 1.53 | 2.21e15 | 4.33e14 | **5.1 / 5.5 / 4.1 / 4.5** | 12.1 / 13.3 / 9.2 / 10.2 |
| T3 | 1.837 / 1.690 | 1.04 / 1.13 / 0.85 / 0.93 | 3.87e15 | 6.00e14 | **6.5 / 6.7 / 5.3 / 5.5** | 16.1 / 16.8 / 12.6 / 13.3 |

- **Need in other units.** Per cluster, the median need is 2.3e13 M☉ in T2 and 3.6e13 M☉ in T3 (canonical h 0.672). Spread
  like the gas (GS), the need is 1.7–2.5 × the gas mass in T2/T3.
- **The central bracket is negative in every tercile.** Measured stars are S_cen/gas_cyl = 0.032 / 0.027 / 0.032 (T1/T2/T3),
  below the f\* = 0.20 the model already carries. The model already over-counts stars.
- **Mass dependence: MISMATCH (4/4).**
  - S_up/gas_cyl falls with mass: 0.095 → 0.082 → 0.076.
  - The need rises from λ_PS ≈ 0.005–0.26 in T1 to 0.85–1.89 in T2/T3.
  - Neither BCG mass (V6) nor the stellar fraction (V7) tracks the excess (both NONE).

## Checks and MUTATE

| check | main run | MUTATE (`X21_MUTATE=1`; labels shuffled) |
|---|---|---|
| K0 step-0 reproduction | PASS 4.4e-16 / 1.8e-15 | **FAIL** (6.3e-1) as required |
| K1 catalogue join | PASS 0.0 | **FAIL** (3.7e2) as required |
| K2 synthetic step / linear plants | PASS 7.5e-15 | PASS |
| K3 λ solver | PASS 9.4e-6 | PASS |
| K4 RSS | PASS 0.394 GB (215 s) | PASS |
| exit | 0 (5/5) | 1 (3/5) |

- **Shuffled labels erase every dependence.** Under MUTATE every variable is NONE (max Δχ² ≤ 2.35), and the trend verdict
  flips to BINNING ARTEFACT. That is the expected null.
- **Amendments.**
  - **A1.** RUN1 stopped at step 0 because its per-bin σ bootstrapped the leak-subtracted numerator, where X7 uses the
    uncalibrated one. Kept as `_RUN1_K0`.
  - **A2.** RUN2's K3 returned nan, from 0/0 on 14 clusters with no MID weight. Kept as `_RUN2_K3`. Every result line of RUN2
    is identical to the final run (diff, excluding timing, RSS and K3).

## Physical reading

- **There is no switch.**
  - Unbinned, MGAS500 shows only a ~1.9σ slope under the record's bootstrap/jackknife errors.
  - The best step location does land at X19's 7.9e12 M☉, but it is not significant once all step locations are allowed for
    (p 0.013).
  - The tercile picture (1.0–1.1 / 1.7–1.9 / 1.7–1.9) depends on where the bins are cut. Quintiles are not monotone.
- **Other variables show a smooth rise.** Re-binned on KT, L500 or richness, A_MID rises steadily:
  - KT 1.10 → 1.65 → 2.13;
  - L500 1.26 → 1.69 → 1.99;
  - λ 1.31 → 1.91 → 2.43.
- **KT tracks the excess best.** The slope is ≈ 3σ, KT carries part of it at fixed MGAS500 (Z 1.7), and the joint fit
  prefers a slope to a step. But the shape is formally unresolved, and KT exists only for the 106 brighter clusters.
- **What the excess does not track.**
  - Core concentration / cool-core proxy: NONE.
  - BCG stellar mass: NONE.
  - Stellar-to-gas fraction: NONE.
  - Redshift: WEAK, and a median step rather than a slope, Z ≤ 0.9 at fixed mass. It is consistent with the flux-limited
    mass–z coupling.
- **Reading.** The excess grows with how deep or hot the cluster is, not with the central galaxy or core structure.
- **Known baryons cannot supply it.** Even counted generously and placed centrally, they fall short by ×4–7 in the heavy
  terciles. Their mass trend runs the wrong way (stellar fraction falls with mass). This agrees with CFG922's EXCESS STANDS and
  ZT2B's concentration target.

## What this does not show

- **Trials.** Seven variables plus the control were tested, and the DETECTED line is not trial-corrected. KT clears it by
  0.13–0.83 in Δχ².
- **KT's sample is selected.** KT exists for 106 brighter clusters. The λ match covers 83 clusters (SDSS overlap) and the
  CFG922 census 281.
- **The permutation p disagrees with the bootstrap/jackknife errors.** The permutation p of the MGAS500 and L500 slopes
  (0.002–0.0055) is much stronger than their max(boot, jk) Z (1.9–2.8). The bootstrap carries the heavy-tailed cluster-to-
  cluster scatter that the permutation null does not. The frozen classes use the bootstrap/jackknife.
- **c_X is not a pure cool-core flag.** L300kpc/L500 carries R500's mass dependence (ρ = −0.67). Its slope at fixed mass is
  +2.3, reported only.
- **The budget's ingredients are limited.**
  - ICL and molecular gas are not on disk. H₂ is set equal to HI, and ICL is graded only through CFG922's ×10 scale.
  - The census is a 0.5 Mpc cylinder; the need is a 3D central mass.
- **The model is X2's C\*,** unchanged. No new component was fitted; λ is a diagnostic only.

## Files and run (`OMP_NUM_THREADS=1 nice -n 15`, about 3.6 min each, ≤ 0.40 GB)

| file | what |
|---|---|
| `x21_switch_anatomy.py` | everything (step 0, unbinned tests, binned tables, budget, checks); `X21_MUTATE=1` for the twin |
| `x21_switch_anatomy.out`, `_results.json` | final run |
| `x21_switch_anatomy_MUTATE.out`, `_results_MUTATE.json` | MUTATE twin |
| `x21_switch_anatomy_RUN1_K0.*`, `_RUN2_K3.*` | kept failed runs (A1, A2) |

Run: `python3 rebuild_2026_10_22/X21_cluster_switch_anatomy/x21_switch_anatomy.py` from the repository root or the
`rebuild_2026_10_22` directory.

Read-only inputs:
- X7's npz and JSON, and X13's JSON;
- X2's source (exec'd), F2's `f2_aqual.py`, and the Chae+21 CSV;
- the eRASS1 FITS;
- CFG688's TSV, CFG687's npz, and CFG922's A1 census.

Nothing was re-measured or downloaded.
