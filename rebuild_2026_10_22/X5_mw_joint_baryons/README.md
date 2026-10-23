# X5_mw_joint_baryons: Milky Way K_z and v_c(R₀) with published baryons under v3's AQUAL; S3's outer slope under CFG532's S2 errors

## Verdicts (frozen classes, per footing, never pooled)

| question | canonical | alt |
|---|---|---|
| (i) does a published-prior baryon model pass both K_z and v_c(R₀)? | **FEASIBLE (wide priors only)**, 7 of 175 cells | **FEASIBLE (wide priors only)**, 4 of 175 cells |
| (ii) does S3's slope verdict survive CFG532's S2 errors? | **SHAPE EXCLUDED ROBUST**, Z −3.88 | **SHAPE EXCLUDED ROBUST**, Z −4.09 |

**What (i) means, in plain words.** Under the frozen line (χ²_Kz ≤ 67.459 AND v_c(R₀) within 2σ of 229.1 km/s), K and V
are **not** AQUAL-structural. Lane P4's failure came partly from McMillan17's baryons. But the passing corner is narrow,
and it fails other data:
- **Needs a short disc.** Every passing cell has R_d = 1.93 or 2.27 kpc. Bland-Hawthorn & Gerhard allow this at ≤ 2σ.
  Licquia & Newman 2016 (2.64 ± 0.13) put it 2.8σ or more out. No cell passes with R_d inside that range.
- **Needs the lightest local column.** Every passing cell has Σ_b = 40.3–43.7 M☉ pc⁻², McKee+15's −2σ to −1σ. The passing
  cells sit on the box edge.
- **Misses Bovy & Rix's summary numbers.** Every passing cell has K_z(R₀) = 76.7–80.9 against 66.4 ± 2.2 (+4.7 to +6.6σ).
  Its K_z scale length h = 3.0–3.5 kpc is +2.1 to +5.3σ above 2.72 ± 0.15. The frozen χ² line, an absolute goodness of fit
  over 43 MAPs with σ ⊕ 5 %, does not catch an amplitude offset of this size (A1 D1–D2). No cell of the box with v_c(R₀)
  in the line reaches K_z(R₀) below 76.66 / 76.91 (A2 D5).
- **Misses the full Eilers curve.** χ²_RC over 5–25 kpc is 96–194 against a 99 % line of 61.2.
- **Leaves the outer slope excluded.** The same baryons give Ou+Jiao Z −4.46 to −5.06 (primary errors) and −3.97 to −4.49
  (S2). That is SHAPE EXCLUDED in every passing cell.

**What (ii) means.** S2 widens Ou's slope error from 0.074 to 0.112. Jiao's published error (0.057) is unchanged, because
CFG532b's S2 does not apply to Jiao. Jiao therefore carries the combination, and every member of S3's robustness set
stays SHAPE EXCLUDED.
- CFG532's old flip to CONSISTENT was a per-curve Ou label. For v3 under S2 that label is NEEDS-HEAVY-DISC on the
  canonical footing (χ² 61.9/37, p 0.006) and CONSISTENT on alt. The combined test does not flip.

κ = ½ is FITTED. Footings are 9.3603e-11 / 1.1312e-10 m/s², never pooled. No dark-matter particle. Not "theory closed".
Nothing here says the data favour the framework. The literature priors come from web look-ups and are PROVISIONAL.

## Step 0: reproductions with the record's own code (read-only)

| item | this lane | record | JSON key |
|---|---|---|---|
| P4 B1 F0 L★ 24 pc, K_z(R₀) / χ²_Kz / v_c(R₀) canonical | 92.282 / 178.370 / 215.170 | 92.282 / 178.371 / 215.170 | `step0_P4.canonical` |
| same, alt | 96.860 / 250.708 / 220.377 | 96.860 / 250.710 / 220.377 | `step0_P4.alt` |
| family = P4's B3 (density identity; solved cell) | 5.5e-15; 96.828 / 332.943 / 240.858 (can) | 96.828 / 332.944 / 240.858 | `step0_B3` |
| S3 Part A AQ_gamma0 primary Z (can / alt) | −4.3733 / −4.6165 | −4.3733 / −4.6165 | `step0_S3["AQ_gamma0\|<foot>"].Z` |
| S3 AQ_iso / AQ_gamma0_2x primary Z | −4.4576 / −4.7067; −4.2131 / −4.4505 | identical | `step0_S3` |
| Eilers target v_c(R₀) | 229.053 ± 4.645 | U1 N6 identical | `vc_target` |

The six census AQUAL solves (s = 1; e_N = 0, h81 and 2 × h81 on both footings) were solved fresh in this lane's untracked
`_cache_s3/`, using S3's code. Their in-plane field equals S3's cached solves exactly (C0d, 0.0). The 48 off-census s-grid
solves are byte copies of S3's cache. They enter only the C-table interpolation and s* in the per-curve labels. Nothing was
written into S3's or P4's directory.

## (i) The prior box (FROZEN_CRITERIA §2; 5 × 5 × 7 cells per footing)

- **Σ_b(R₀)**: 40.3–53.9 M☉ pc⁻², from McKee+15 47.1 ± 3.4 (±2σ).
- **M_bb**: 1.64–2.12 × 10¹⁰ M☉, from Portail+17 1.88 ± 0.12 (±2σ), as a compact bulge shape.
- **R_d**: 1.6–3.6 kpc, from Bland-Hawthorn & Gerhard 2.6 ± 0.5 (±2σ), applied to both stellar discs.
- **Held**: McMillan17's gas, its disc scale heights and its thin share of the local column.

Each cell uses P4's solver, grid and observables, at L★ 24 pc, isolated. Numbers are in `i.<foot>`.

| | canonical | alt |
|---|---|---|
| passing cells (`n_pass`) | 7: Σ_b 40.3, all five M_bb, R_d 1.933; Σ_b 43.7, M_bb 2.00 / 2.12, R_d 2.267 | 4: Σ_b 40.3, M_bb 2.00 / 2.12, R_d 2.267; Σ_b 43.7, M_bb 1.64 / 1.76, R_d 2.267 |
| best cell (`best`, min D) | Σ_b 40.3, M_bb 1.64e10, R_d 1.933: χ²_Kz 48.17, v_c 229.71, K_z(R₀) 76.66, h 3.08, D 0.714, M★ 6.02e10 | Σ_b 40.3, M_bb 2.12e10, R_d 2.267: χ²_Kz 49.67, v_c 222.32, K_z(R₀) 77.13, h 3.48, D 0.736, M★ 5.36e10 |
| tags of every passing cell | M★-IN true, R_d-IN false | M★-IN true, R_d-IN false |
| robustness (`robustness`) | every pass holds at L★ 90 pc and at g_e = 0.03 a₀: χ² moves by ≤ 0.09, v_c by ≤ 0.02 | every pass holds: χ² moves by ≤ 0.15, v_c by ≤ 0.03 |
| cells with v_c in the line / with χ² in the line | 26 / 31 | 30 / 18 |
| range over the box: χ²_Kz; v_c(R₀) | 44.5–1401.7; 180.8–311.1 km/s | 49.3–1586.5; 185.9–316.3 km/s |

The box spans v_c(R₀) from 181 to 316 km/s. U1's "v_c(R₀) ≤ 215.6 / 220.6 in every branch" is therefore a property of
McMillan17's baryons, not of v3. L★ = 0 instead of 24 pc changes χ²_Kz by ≤ 0.009 / 0.013 and v_c(R₀) by < 0.001 km/s.

### AMENDMENT A1 diagnostics (POST-RESULT; reported only; `A1_diagnostics.<foot>.cells`)

| cell (Σ_b, M_bb, R_d) | χ²_Kz σ ⊕ 5 % → table errors only (D1) | K_z(R₀), pull (D2) | h, pull (D2) | χ²_RC vs 61.2 (D4) | Ou+Jiao Z primary / S2 (D3) |
|---|---|---|---|---|---|
| can 40.3, 1.64, 1.933 (best) | 48.2 → 56.6 | 76.7, +4.7σ | 3.08, +2.4σ | 116.2 | −4.58 / −4.07 |
| can 40.3, 2.12, 1.933 | 55.8 → 65.2 | 77.8, +5.2σ | 3.04, +2.1σ | 102.6 | −4.46 / −3.97 |
| can 43.7, 2.00, 2.267 | 50.2 → 59.9 | 77.6, +5.1σ | 3.41, +4.6σ | 194.2 | −4.63 / −4.11 |
| alt 40.3, 2.12, 2.267 (best) | 49.7 → 59.5 | 77.1, +4.9σ | 3.48, +5.0σ | 115.2 | −5.03 / −4.46 |
| alt 43.7, 1.64, 2.267 | 65.1 → **77.4** | 80.7, +6.5σ | 3.52, +5.3σ | 126.4 | −4.97 / −4.41 |
| alt 43.7, 1.76, 2.267 | 66.4 → **78.9** | 80.9, +6.6σ | 3.50, +5.2σ | 95.6 | −4.94 / −4.38 |

All 11 rows are in the JSON. Read with table errors only, the two Σ_b = 43.7 alt cells fail the χ² line; every other cell
still passes. D3-ref passes: B1 through P4's solver gives S3's AQ_iso law slopes to 0.0003, and Z −4.459 against −4.458.

**D5 (AMENDMENT A2; `A1_diagnostics.<foot>.D5`).** Of the 26 / 30 cells whose v_c(R₀) is inside the line, the lowest
K_z(R₀) is **76.66 / 76.91** (+4.7 / +4.8σ above 66.4 ± 2.2). The lowest K_z(R₀) anywhere in the box is 69.21 / 73.18
(+1.3 / +3.1σ), at Σ_b 40.3 and R_d 3.6, where v_c(R₀) is only 180.8 / 185.9 km/s. So no cell of the box gets both
Bovy & Rix's summary K_z(R₀) and v_c(R₀). Scored that way, K + V would be AQUAL-structural in this box. That reading is
post-result and carries no verdict weight.

## (ii) S3 Part A under S2 (FROZEN_CRITERIA §3; `ii.<foot>`, `S2_data`)

**S2 data slopes** (15–27.5 kpc; reproduce CFG532/532b's S2 rows exactly, C1):

| curve | Ou | Eilers | Wang | Jiao | Zhou | Feng (10–17.6 kpc) |
|---|---|---|---|---|---|---|
| S2 slope | −0.327 ± 0.112 | −0.282 ± 0.105 | −0.373 ± 0.087 | −0.319 ± 0.057 (as published) | −0.187 ± 0.098 | −0.027 ± 0.110 |
| primary slope | −0.325 ± 0.074 | −0.278 ± 0.071 | −0.356 ± 0.058 | −0.319 ± 0.057 | −0.186 ± 0.061 | −0.026 ± 0.067 |

**v3 cell AQ_gamma0:**

| | canonical | alt |
|---|---|---|
| primary Ou+Jiao ρ = 0: Δ ± σ̄, Z (`primary`) | −0.197 ± 0.051, **−3.88** (primary errors −4.37) | −0.208 ± 0.051, **−4.09** (−4.62) |
| ρ = 0.5 / e_N = 0 / 2 × h81 (`members_Z`) | −3.44 / −3.96 / −3.73, all EXCLUDED | −3.63 / −4.18 / −3.94, all EXCLUDED |
| all one-per-group pairs (`Z_range`) | −3.88 … −2.29 (Zhou+Wang −2.63 / −2.29 at ρ 0 / 0.5) | −4.09 … −2.43 |
| Cepheids, Feng (`cepheid`) | +0.88, SHAPE CONSISTENT | +0.76, SHAPE CONSISTENT |
| per-curve labels (`per_curve_labels`) | Ou NEEDS-HEAVY-DISC; Eilers CONSISTENT; Zhou NEEDS-HEAVY-DISC; Wang, Jiao, SL23 EXCLUDED | Ou, Eilers, Zhou CONSISTENT; Wang, Jiao, SL23 EXCLUDED |

## Checks: 9/9 PASS (exit 0, 34 s, peak RSS 0.61 GB; grid runs 181 / 164 s at 0.55 GB; S3 child processes 0.57 GB in the first run)

| check | result |
|---|---|
| C0a | P4 B1 reproduced: max \|ΔK\| 8e-5, \|Δχ²\| 1.4e-3, \|Δv_c\| 9e-5 |
| C0b | the family's density equals P4's B3 to 5.5e-15; its solve gives P4's B3 numbers |
| C0c | S3 Z exact (Δ 0) |
| C0d | fresh census solves equal S3's cached ones (0.0) |
| C1 | S2 slopes equal CFG532/532b to 0 |
| C2 | Eilers target equals U1's |
| C3 | 175 + 175 cells; residual ≤ 9.2e-11 |
| C4 | grid mass vs analytic 2.0e-6 |
| C5 | RSS < 1 GB; runtime ≤ 30 min |

**`--mutate`**: P4's μ becomes x/√(1+x²) at L★ = 0, and S3's μ ≡ 1. Then C0a, C0b and C0c FAIL (3/6, exit 1). The
central cell gives χ²_Kz 119.3 / 97.5 and v_c 188.6 / 192.8 (`x5_mw_joint_baryons_results_MUTATE.json`).

## Amendments

- **None PRE-RESULT.**
- **A1 (POST-RESULT; reported diagnostics D1–D4 only).** Written after the frozen run (commit 04e5c6be40, which holds that
  run's outputs) and before any diagnostic number. No line, grid, class or check changed.
- **A2 (POST-RESULT; reported diagnostic D5 only).** Written after the A1 numbers were seen. Nothing else changed.
- Every frozen number is unchanged by A1 and A2. Each rerun reproduces the frozen run's output except the cache
  bookkeeping, the RSS figures and the added diagnostic lines.

## What this does not show

- **FEASIBLE is not a fit, and it does not say the Milky Way has these baryons.**
  - The passing cells sit at the box's light-column edge and at short R_d. They contradict Licquia & Newman 2016's
    scale length.
  - Bovy & Rix's fitted K_z(R₀) and h are still missed by ≥ 4.7σ and ≥ 2.1σ.
  - The Eilers curve is not fitted beyond R₀.
  - A frozen line that tested BR13's summary K_z(R₀) instead of the per-MAP χ² would have given AQUAL-STRUCTURAL (D5: no
    v_c-passing cell has K_z(R₀) below 76.66 / 76.91). This reading is post-result and has no verdict weight.
- **The family's scope** (fixed in the criteria):
  - axisymmetric, with a compact bar (a ~5 kpc long bar is not modelled);
  - McMillan17's vertical structure and gas;
  - one R_d for both stellar discs;
  - static and isolated, or in a uniform axial field;
  - no μ_K² term, no dust;
  - Bovy & Rix's modelling assumptions taken as given.
- **The priors are PROVISIONAL.** Portail+17's bar mass comes from Newtonian made-to-measure models that include a dark halo.
- **(ii) is S3's statistic under the record's S2.**
  - S2 leaves Jiao's published errors unchanged, which is why the combination holds. An S2-style inflation of Jiao is not
    in the record's definition and was not run.
  - It is not a Jeans forward model (Koop+24), and it says nothing about DR4.

## Suggested record fixes (not made here; for the coordinator)

- **X0 MAP §1.E.1** expected FAIL, "K and V AQUAL-structural". The frozen result is FEASIBLE (wide priors only), with the
  caveats above.
- **P4 README T4 "Every baryon model fails" and the board's MW-vertical tile "FAIL (ROBUST)".**
  - These hold for McMillan17/B2/B2b/B3. In published priors, the χ² line can be passed with R_d ≤ 2.27 kpc and
    Σ_b ≤ 43.7.
  - K_z(R₀) stays ≥ 76.7 against 66.4 ± 2.2.
  - Suggested wording: "FAIL at McMillan17; the χ² line is passable only at short R_d and light columns, and K_z(R₀) still
    misses by ≥ 4.7σ".
- **U1 tile "MW v_c(R₀) TENSION (all branches)"** is McMillan17-specific. In the box v_c(R₀) spans 181–316 km/s.
- **S3 tile 25 "SHAPE EXCLUDED, ROBUST"** stands under S2. Its robustness set could cite this lane.
- **LEDGER.md** has no X5 row.

## Run, files, commits

```
OMP_NUM_THREADS=1 nice -n 15 python3 rebuild_2026_10_22/X5_mw_joint_baryons/x5_grid.py --foot canonical   # ~3 min
OMP_NUM_THREADS=1 nice -n 15 python3 rebuild_2026_10_22/X5_mw_joint_baryons/x5_grid.py --foot alt         # ~3 min
OMP_NUM_THREADS=1 nice -n 15 python3 rebuild_2026_10_22/X5_mw_joint_baryons/x5_mw_joint_baryons.py         # ~30 s, exit 0
OMP_NUM_THREADS=1 nice -n 15 python3 rebuild_2026_10_22/X5_mw_joint_baryons/x5_mw_joint_baryons.py --mutate  # ~3 s, exit 1
```

- **Files.**
  - Scripts: `x5_lib.py` (P4 machinery executed read-only, the family, the lines), `x5_grid.py` (question (i) cells) and
    `x5_mw_joint_baryons.py` (Step 0, (ii), aggregation, A1, checks).
  - Outputs: `x5_grid_<foot>.out/.json`, `x5_mw_joint_baryons.out`, `_results.json`, and `_MUTATE` versions of both.
  - `_cache_s3/` is untracked (S3-format solves). Delete it to force fresh census solves.
- **Commits.**
  - 8e5b65bca5: criteria and ledger, committed alone.
  - 04e5c6be40: frozen run and A1 text.
  - The README, the A1/A2 diagnostics and the mutate outputs are in the commit that adds this file.
- **Inputs.** All are read only. Nothing was downloaded.
- **Literature look-ups (PROVISIONAL, 2026-10-23, search summaries).**
  - Portail+17 (arXiv:1608.07954)
  - Bland-Hawthorn & Gerhard 2016 (arXiv:1602.07702)
  - Licquia & Newman 2015 (arXiv:1407.1078)
  - Licquia & Newman 2016 (arXiv:1607.05281)
  - McKee+15 is in the record.
