# LAM9_imf_from_spectra: NOT MEASURABLE on all three questions and both footings. The frozen Γb fit fails its recovery test (K1): at the sums' S/N it reads the IMF mass factor α 0.15 dex too high, against a 0.03 dex line

| step | commit |
|---|---|
| Criteria, frozen first and committed alone | `9c1f411110` |
| Stage 0 | `e919c84f8d` |
| Amendment A1, before any fit | `66fb0bbf80` |
| Scripts, before any fit | `430c890385` |

κ = ½ FITTED; not theory closed. Footings canonical and alt are never pooled. The cold sector stays retired: nothing is added
but the stellar IMF. Nothing here says the data favour the framework.

## Labels
| question | canonical | alt |
|---|---|---|
| Q1: does KU2's absolute r_half residual shrink with a spectroscopic IMF? | NOT MEASURABLE (K1 fails) | NOT MEASURABLE (K1 fails) |
| Q2: does HX1's "MaNGA ellipticals need B 3-4 inside R_e" go away? | NOT MEASURABLE (K1 fails) | NOT MEASURABLE (K1 fails) |
| Q3: does LAM6's h4 lean survive at fixed IMF? | NOT MEASURABLE (K1 fails) | NOT MEASURABLE (K1 fails) |

These caveats stay with every label:
- NSA's h units are unresolved. Stage 0 points to h = 1 units, worth 0.31 dex in M★.
- [Na/Fe] is not modelled.
- CaT sits in telluric water bands above z ≈ 0.05.
- Tian+2026's Kroupa IMF was read only through a summariser.

As frozen (A1 item 3), the remaining 1256 fits were not run. Q1-Q3, the MUTATE twin and the rows were not graded.

## The download (owner-approved, verified)
- Five files from the MILES share named in the criteria: 1,409,001,566 B. Every size matches the table.
- The SHA-256 sums are in `lam9_download.json`.
- The tarball has 8904 regular, flat members, with no absolute paths and no "..". It holds 14 slopes, including Γb 1.00,
  which is not used.
- The 1092 frozen spectra were extracted by explicit list (`lam9_template_manifest.txt`).
- C4 passes: the code's M/L_V is 0.7 % below the MILES table for all five checked templates.

## K1: recovery at the sums' S/N (the gate)
There are 300 synthetic sums on 300 distinct real donors. Each is the donor's fitted age and [M/H] mix moved to one Γb_in,
with the donor's LOSVD, its polynomial, the stacked sky residual, and its noise x sqrt(χ²_a). Each was fitted with the frozen
pipeline.

| | variant A (primary) | variant B (Na I masked) | frozen line |
|---|---|---|---|
| Γb bias (median out - in) | -0.177 | -0.166 | ≤ 0.15 in size |
| Γb rms | 0.255 | 0.258 | ≤ 0.40 |
| log α bias | **+0.152 dex** | **+0.159 dex** | ≤ 0.03 dex in size |
| log α rms | **0.216 dex** | **0.215 dex** | ≤ 0.10 dex |
| K1 | **FAIL** | **FAIL** | |

- **By S/N third,** variant A's log α bias is +0.149, +0.208 and +0.136. The bias does not shrink with S/N in this range,
  which is χ²-scaled Na I S/N of 40-110 per Å (5-95 %, median 71).
- **By injected Γb,** the α bias is largest for Milky-Way-like IMFs: +0.32 to +0.34 dex at Γb 1.3-1.5. It falls to +0.03 at
  Γb 3.0 and to 0.00 at 3.3.
- **Step a (unregularised) row, not graded:** Γb bias -0.229, log α bias +0.147, rms 0.272. Dropping the regularisation does
  not fix it.
- **K2, the h4 leak, PASSES:** b = -0.065 dex per unit h4, which gives a lean of 0.008 ln (line 0.01). It gates nothing now.

## What it means
- **Why it fails.** The fit can't place each galaxy's IMF tightly enough at this S/N, and the spread is not harmless:
  - α is U-shaped in Γb. Top-light slopes carry heavy remnants, so Γb 0.3 gives α 4.7. Bottom-heavy slopes carry dwarfs, so
    Γb 3.5 gives 2.66, while Γb 1.3 gives 1.
  - Noise moves light to both ends of the grid, so α comes out high. In the 330 real donor fits, a median 35 % of the light
    sits at Γb 0.3 or 3.5.
  - That bias is largest for galaxies with an ordinary IMF. It would look like "the IMF absorbs the excess" when nothing
    had been measured. This is the failure K1 was frozen to catch.
- **What stays open.** This lane can't say whether a spectroscopic IMF absorbs KU2's residual or HX1's MaNGA need, or whether
  LAM6's lean survives at fixed IMF. HX1's IMF reading stays as HX1 left it: possible, not shown.
- **Known before any fit, and unchanged** (model arithmetic, not a measurement):
  - On KU2's mass convention, removing KU2's +1.2 to +1.4 ln needs α 4.5-6.2.
  - Every bottom-heavy template on the grid is below that; the largest is 2.66 at Γb 3.5.
- **A likely cause, not tested.** Including the top-light slopes (Γb 0.3 and 0.5) lets noise reach the remnant-heavy end. A
  grid that stops at 0.8 (the planning example), stacking at fixed σ (as the MaNGA IMF literature does), or Na-enhanced models
  might behave differently. Each would need its own frozen criteria and its own K test.

## Colour row
Not computed. α failed its recovery test, so no α-based row is reported. For context, the 1586 step-5 galaxies are 1490
red and 96 blue (NSA u - r at SI2's 2.0 boundary).

## Files
- **Criteria and amendment:** `FROZEN_CRITERIA.md`, `AMENDMENTS.md` (A1).
- **Run records:** `EXECUTION_NOTE.md` (sharding, a restart, the queue), `lam9_download.json`, `lam9_template_manifest.txt`.
- **Stage 0:** `lam9_stage0.py`, `.out`, `.json`.
- **Templates:** `lam9_templates.py`, `.out`, `.json`.
- **Core and fits:** `lam9_core.py`; `lam9_fit.py`, with `lam9_prepare.json`, `lam9_k_donors.csv` and `lam9_fit_donors.json`
  (the 330 real donor fits, both variants).
- **K control:** `lam9_k.py`, with `lam9_k.out`, `lam9_k.json` and `lam9_k_rows.json`.
- **Grader:** `lam9_grade.py`, written before any regrade and not run, because K1 failed.
- **Not in the repo:** the data, in `_external_data/lam9_emiles_bi_basti/` (the download and the 1092 extracted spectra),
  `lam9_templates_2026_11_04/` and `lam9_work_2026_11_04/` (shard outputs, weights, logs).

κ = ½ FITTED; not theory closed.
