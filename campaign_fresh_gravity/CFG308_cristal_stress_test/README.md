# CFG308: stress test of the CRISTAL a₀ point at z ≈ 5, on framework-native inputs

**Owner request (2026-10-02):** "stress test cristal too".

**Criteria.** `FROZEN_CRITERIA.md` was committed as **ca50d064d** before any number of this lane was computed.

**Framework assumptions.** κ = ½ is FITTED. The cold mass is still required; no dark-matter particle is added. No halo-fit quantity (f_DM, log M_tot, or a model curve beyond the last marker) enters any cell. No sentence here says the data favour a law.

## Bottom line
1. **Decision (frozen rule): NOT DISCRIMINATING.** The grid has 1,008 declared cells. Over them:
   - **a₀ ∝ H(z) is excluded at 95% in 59.4%** (599 cells);
   - **flat a₀ is excluded in 24.0%** (242 cells);
   - neither reaches the 80% line.

   Breakdown by cell:

   | outcome | cells |
   |---|---|
   | only H(z) excluded | 385 |
   | only FLAT excluded | 28 |
   | both excluded | 214 |
   | both inside | 381 |

   The point estimate has no root in 432 cells: there the baryons meet or exceed the dynamics, so no a₀ fits.
2. **CFG303's R_out exclusion of H(z) is not robust.** It was the brief's "rival right at the 95% edge" (s★ 1.95, 95% ≤ 8.78 against H(z) 8.84). At the committed gas and pressure on the six discs, H(z) stays excluded in 5 of the 9 stellar-mass × inclination cells. It comes back inside in three cases:
   - at M★ −0.15 dex, at every inclination;
   - at inclination −σ_i;
   - in 5 of 6 leave-one-outs (only dropping CRISTAL-11 keeps it out).

   With the three dust upper limits added as bounds, H(z) is inside in all 9 cells (envelope up to 9.4–12.5).
3. **The H(z) exclusions come from the reduced-pressure variants, and those variants mostly leave no root.**
   - **Lower pressure terms** (P336, P168, P0; 630 cells): H(z) is excluded in 85%, FLAT in 30%, and 382 of those cells have no root.
   - **The authors' own pressure convention** (P_auth at both radii, plus the 2R/R_d form at R_out; 378 cells): H(z) is excluded in 17%, and 44 of those 64 cells are the f + errhi gas corner. FLAT is excluded in 13%.

   Restricted to cells with a root (576), H(z) is excluded in 30.9% and FLAT in 4.9%.
4. **Dominant axis: the pressure-support term.** Its H(z)-exclusion swing is 0.90. The gas route is a close second at 0.89; it is 0.59 at R_e and 0.36 at R_out without the one-sided stars-only level. Then come inclination (0.18), radius (0.13), M★ (0.13) and sample (0.10). For FLAT's exclusion, pressure leads (0.72), then gas (0.67).
5. **Leave-one-out: the decision is stable.** It is NOT DISCRIMINATING in all six subgrids:
   - H(z) excluded in 0.56–0.69;
   - FLAT inside in 0.69–0.76.
6. **Reading.** On the record's declared input variants, the CRISTAL point does not separate flat a₀ from a₀ ∝ H(z). The point is pressure- and gas-limited. Every cell is the authors' DysmalPy velocity on six (or nine) dispersion-dominated discs. Nothing here is an a₀(z) measurement.

## The grid (frozen §3)
| axis | levels | source |
|---|---|---|
| (a) gas | G0 dust f (committed); G+ / G− f ± the paper's 1σ; C0 / C+ / C− [CII] gas for CRISTAL-20 only (CFG228's L_[CII] = 7.93e8 L☉, α = 30 × 10^{0, ±0.3}, Zanella+18); S stars only (one-sided upper bound on s★) | CRISTAL Table (f_molgas), CFG228, Zanella+18 via the record |
| (b) M★ | −0.15 / 0 / +0.15 dex (gas held at its measured mass) | CFG219's σ★ (the tables carry no M★ error) |
| (c) pressure | R_e: 3.36 (committed) / 1.68 / 0. R_out: authors' V_tot (committed) / 2R/R_d on the clipped model rotation / 3.36 / 1.68 / 0 | CFG213, CFG228, CFG229; authors' form 3.36 R/R_e |
| (d) inclination | committed ± σ_i (9.5° JWST-image, 19° [CII]-map), applied coherently | Jones+21 median errors on disk |
| (e) radius | R_e; the outermost data marker | CRISTAL Table; `cristal_outer_summary.csv` |
| (f) sample | six detections; nine with the three dust upper limits (08, 12, 23b) as bounds on the gas | CFG219, CFG220 |

The decision grid has 378 cells at R_e and 630 at R_out. The leave-one-out subgrids add 3,024 cells. The estimator is CFG223's s★ with its 10,000-resample galaxy bootstrap, exec'd from the committed source. g_bar uses CFG216's thin exponential disc, as in CFG303.

### Marginal fraction of cells excluding H(z) / excluding FLAT, by level
| radius | axis | levels (H-excl / F-excl) |
|---|---|---|
| R_e | pressure | P_auth 0.11 / 0.16; P168 0.57 / 0.08; P0 0.86 / 0.21 |
| R_out | pressure | P_auth 0.30 / 0.06; P_B10 0.10 / 0.18; P336 0.84 / 0.10; P168 0.98 / 0.34; P0 1.00 / 0.79 |
| R_e | gas | G0 0.57 / 0.09; G+ 0.93 / 0.59; G− 0.33 / 0.15; C0 / C+ / C− 0.57 / 0.06–0.09; S 0.04 / 0.00 |
| R_out | gas | G0 0.66 / 0.29; G+ 0.93 / 0.71; G− 0.58 / 0.23; C0 / C+ / C− 0.66 / 0.24–0.29; S 0.37 / 0.04 |
| R_e / R_out | M★ (−0.15, 0, +0.15) | 0.44, 0.52, 0.57 / 0.59, 0.65, 0.69 (H-excl) |
| R_e / R_out | inclination (−σ, 0, +σ) | 0.41, 0.53, 0.60 / 0.62, 0.65, 0.66 (H-excl) |
| R_e / R_out | sample (six, nine) | 0.56, 0.47 / 0.68, 0.60 (H-excl) |

- **[CII] levels.** They change only CRISTAL-20's gas, and they leave the H(z) flags unchanged (identical marginals to G0).
- **Stars-only cells.** H(z) sits above the stars-only upper bound in 35 of 144. All 35 are at reduced pressure: R_out P0 (18), R_out P168 (15), R_e P0 (2). Those are the variants in which the detected-gas cells mostly have no root.
- **Median |Δ log₁₀ s★| between extreme levels** (six discs, matched pairs where both have a root):
  - M★: 0.58 (n 57);
  - inclination: 0.27 (65);
  - P0 → P_auth: 1.00 (3);
  - R_e → R_out at P_auth: 0.08 (43);
  - gas (G+ ↔ G−): n/a, no matched pair has two roots.

### The committed cells inside the grid
| cell | s★ | 68% | 95% (envelope for the bounds) | FLAT | H(z) |
|---|---|---|---|---|---|
| R_e, six | 2.014 | [0.237, 7.272] | [0.001, 14.93] | in | in (8.84) |
| R_e, nine (upper limits at the limit / at zero) | 0.674 / 3.612 | [0.554, 3.612] | [0.001, 16.11] | in | in (8.77) |
| R_out, six | 1.953 | [0.417, 5.054] | [0.001, 8.776] | in | **OUT** (8.84) |
| R_out, nine (at the limit / at zero) | 0.684 / 3.527 | [0.521, 3.527] | [0.001, 11.04] | in | in (8.77) |

## Controls
| control | result |
|---|---|
| **T0** inputs (σ_i are the Jones+21 medians; CFG228's L_[CII] row) | PASS |
| **(i-a)** per-galaxy g_bar and g_obs equal CFG303's CSV | PASS (max relative difference 4.7e-7; the CSV has 7 significant figures) |
| **(i-b)** R_e six, R_out six, the nine-disc set with the limits used as values (0.674), and the table-R_out variant (1.90) equal CFG303's JSON (s★, edges, expected s★ and pulls for four laws, bands) | PASS (max \|diff\| 2.8e-17) |
| **(i-c)** the grid's committed cells equal the identity runs | PASS (0) |
| **C1–C4** monotonicity in gas, M★, pressure, inclination and the upper-limit bracket | PASS (2,136 / 1,116 / 4,320 / 1,488 comparisons, no violation) |
| **C5** process pool equals serial (24 cells) | PASS (0) |
| **(iii)** leave-one-out stability | PASS (6 of 6 NOT DISCRIMINATING) |
| **main run** | **13/13** |
| **MUTATE M1** (every velocity × 1.5 → log D + 0.35218 exactly) | PASS (1.1e-15) |
| **MUTATE M2** (every main-run root rises by ≥ 2.25² = 5.0625) | PASS (2,270 / 2,270; min ×5.41, median ×9.05, 5–95% ×6.0–44) |
| **MUTATE M3** (committed cells against a scalar brentq) | PASS (2e-16; R_e 2.01 → 27.6, R_out 1.95 → 21.5) |
| **MUTATE M0** precondition \|d log ν_mono / d log y\| ≤ ½ (tolerance 1e-6) | **FAIL, kept** (−0.500012) |
| **MUTATE C1–C5** | PASS |
| **MUTATE run** | **9/10** |

**The M0 failure (post hoc, `cfg308_posthoc_m0_slope.py`, 3/3; labelled).**
- **Cause.** The committed ν_mono (FP1/L340) linearly interpolates a cumulative table in log₁₀ y, with cells 1e-4 dex wide. In the deep-MOND tail (y < 1e-6), the chord of h ∝ √y is steeper than ½ at each cell's left end, by (ln 10 × 1e-4)/8 = 2.9e-5. The exact cell-end minimum is −0.5000288.
- **Why M2 is unaffected.** The grid's y range is 1.3e-4 to 5e4. There the slope never passes −½ (its minimum is −0.4972), so the frozen 5.0625 bound is conservative. The used-range bound is 5.109, and every observed rise exceeds it.
- **Two disclosures about the post hoc script itself.** Its first run had P3 posed wrongly: it expected the deep tail inside the used range, and it FAILED. That run is kept in `cfg308_posthoc_m0_slope_firstrun.out`. Its g_bar span was also replaced by the exact grid span before the kept run.
- **Status.** This is a property of the committed kernel, not of this lane. It is flagged, not fixed.

**The MUTATE decision** is also NOT DISCRIMINATING (H(z) excluded 0.236, FLAT excluded 0.409). The ×1.5 velocities move the cells towards excluding FLAT, as they must. The dominant axis there is pressure for H(z) and gas for FLAT.

## Diagnostic D1: the raw outermost observed markers (outside the decision)
These velocities are projected, beam-smeared and uncorrected. They are deprojected with sin i, plus α σ₀², at G0 / ΔM★ 0 / committed i, on the six discs.

| α | per-disc D | s★ | 95% | FLAT | H(z) |
|---|---|---|---|---|---|
| 0 | 0.04–0.73 | no root | [0.001, 0.001] | out | out |
| 1.68 | 0.25–1.38 | no root | [0.001, 0.35] | out | out |
| 3.36 | 0.47–2.02 | 0.22 | [0.001, 2.79] | in | out |
| 3.36 R/R_e | 0.87–4.51 | 1.53 | [0.021, 14.0] | in | in |

The markers say whatever the pressure term says: at 1.6–5.5 beams, the observed rotation is far below σ₀.

## Hand estimates (frozen §8): 13 of 16 sub-estimates hit; the 3 misses are kept
- **Hits:**
  - H1: identity exact;
  - H2: frac_H_excl 0.594 lies in [0.45, 0.80];
  - H4: NOT DISCRIMINATING;
  - H5b: FLAT inside in 0.951 of the root cells;
  - H6a: pressure is the dominant axis;
  - H6b: gas is second;
  - H7: R_out P0 has no root in 63/63 six-disc cells;
  - H9a: LOO-stable;
  - H9b: the R_out exclusion flips under 5 of 6 LOOs;
  - H10a: 2,270/2,270 rise by ≥ 5.06;
  - H10b: median rise ×9.05;
  - H11: D1 at α = 0 has no root;
  - H12: frac_F_excl 0.240 < 0.5.
- **Misses:**
  - **H3:** FLAT inside 0.760, against my [0.45, 0.75]. The no-root cells were fewer than I guessed.
  - **H5a:** H(z) is excluded in 0.309 of the root cells, against my 0.40–0.75. Where a root exists, H(z) is excluded less often than I expected.
  - **H8:** H(z) is not excluded in 0.757 of the stars-only cells, against my ≥ 0.80. At reduced pressure even stars alone leave H(z) above the bound.

## Disclosures and limits
- **Velocities.** Every velocity is the authors' DysmalPy value, with a halo in the fit, inside the data (MODEL-OTHER). The markers rest on 1.6–5.5 beams. The record and the papers on disk offer no stand-alone beam-smearing correction, so none is in the grid. The uncorrected markers are D1.
- **Pressure at the marker.** The authors' term there (α_c = 3.36 R/R_e) is inferred from their R_e convention. The paper's equation is not on disk. With it, CRISTAL-02 and -11 have no model rotation left at their outermost markers, and neither do the upper-limit discs 12 (and nearly 23b). Their "circular velocity" there is all pressure correction. In the P0 variant at R_out, those discs carry g_obs = 0 (represented as 1e-20 m s⁻²).
- **Gas.** [CII] gas is on disk for CRISTAL-20 only; the CRISTAL tables carry no L_[CII], and nothing was downloaded. The dust gas is the paper's single conversion. f + errhi reaches f = 0.96 and 0.97 for CRISTAL-11 and -19, which is gas of 24× and 32× M★. That corner is what drives the G+ level. The upper-limit values are treated as limits; the errors the table quotes on them are not used.
- **Error sizes.** σ★ (0.15 dex) and σ_i (9.5° / 19°) are record values carried over from other samples, not errors measured for these discs. The inclination and M★ shifts are coherent corners.
- **Discrete intervals.** For an odd number of discs (the five-disc LOO sets and the nine-disc set), the median-root equals one disc's own root. s★ and its bootstrap edges therefore take values from the set of single-disc roots, which is why the same numbers (3.612, 0.554, 3.527, 0.521, 14.01, 16.11, 7.02, 11.04) recur across subsets.
- **The bootstrap lower edge** sits at the 0.001 floor in most cells (resamples with no root). FLAT can then be excluded only from above, through a no-root interval, or from below in light-baryon corners. The 28 cells that exclude FLAT but keep H(z) inside are all light-baryon corners: M★ −0.15 and/or G− gas, mostly at inclination −σ_i at R_e, and with the 2R/R_d form at R_out.
- **Where the runs were made.** Both runs were made in the working tree, not a `git archive` mirror. They write only into this lane. CFG307's directory was not touched.

## Files
- **Criteria:** `FROZEN_CRITERIA.md` (ca50d064d).
- **Script:** `cfg308_cristal_stress.py`, with outputs `cfg308_cristal_stress.out`, `cfg308_cristal_stress_results.json` and `cfg308_grid.csv` (4,032 rows; `in_decision` marks the 1,008 decision cells).
- **MUTATE:** `cfg308_cristal_stress_MUTATE.out`, `cfg308_cristal_stress_MUTATE_results.json` and `cfg308_grid_MUTATE.csv`.
- **Post hoc (labelled):** `cfg308_posthoc_m0_slope.py`, `.out` and `_results.json`, plus `cfg308_posthoc_m0_slope_firstrun.out`.

**Run order and times.** Run from the repository root; each script takes about 2.5 min on a 12-process fork pool. The MUTATE run reads the main run's grid, and the post hoc reads both.
```
python3 campaign_fresh_gravity/CFG308_cristal_stress_test/cfg308_cristal_stress.py
MUTATE=1 python3 campaign_fresh_gravity/CFG308_cristal_stress_test/cfg308_cristal_stress.py
python3 campaign_fresh_gravity/CFG308_cristal_stress_test/cfg308_posthoc_m0_slope.py
```
`CFG308_SERIAL=1` forces a single process. It gives the same numbers (control C5) but is much slower.
