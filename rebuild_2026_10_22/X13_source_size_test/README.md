# X13_source_size_test: is X11's source-size dependence of the cluster-core excess source-side or cluster-specific?

Criteria: `FROZEN_CRITERIA.md` (committed alone, c4e5a5a064; amendments A1 PRE-RESULT, A2 POST-RESULT below). Inputs and
classes: `ASSUMPTION_LEDGER.md`. κ = ½ FITTED. Footings 9.3603e-11 / 1.1312e-10 m s⁻², never pooled. No dark-matter
particle. Not "theory closed". Nothing here says the data favour the framework.

## Verdict (frozen classes; JSON keys in `x13_analysis_results.json`)

**SOURCE-SIDE SYSTEMATIC** (`verdict`). Both routes of the frozen rule fire:
- **(e) = E-MATCH** in all 4 cells (`e_class`). Around F2's 181,477 galaxy lenses, the same size split gives
  ρ_gal = A_L/A_S = 1.47 ± 0.19. That is 2.5σ above 1 and 0.7–0.8σ from the clusters' 1.69–1.71 ± 0.22.
- **Mechanism (f) accounts for ≥ 70 %** in all 4 cells (`mechanisms.sel`): f_sel = 1.20–1.24, 16–84 % range 0.97–1.64.
  The mechanism is a **shear-induced size selection of the split itself**:
  - The lensfit scalelength behaves as a semi-major-axis length, so a shear g stretches it by g∥.
  - A cut on it therefore preferentially puts tangentially aligned sources in the large half and radially aligned
    sources in the small half.
  - So the large half's shear is boosted and the small half's suppressed. The all-source sample has no such cut.
- **The gate passes** (`f_selection.<cell>.gate`). The circularised size r_ab = size·√((1−|e|)/(1+|e|)) does not change
  under shear to first order, and splitting on it removes most of the dependence:
  - clusters ρ_circ = 1.13–1.17 ± 0.15;
  - galaxies 1.03 ± 0.13;
  - FLUX_RADIUS halves (reported) 1.00–1.04 ± 0.14.
  - The alternative convention (scalelength already circularised) predicts ρ_circ = 0.52; the measurement excludes it.
- **The other mechanisms account for < 30 % or are undetermined.**
  - SNR: f_snr = −0.02 to −0.03 ± 0.07. The halves differ by only 0.16 in ln SNR.
  - Photo-z, H_SOM: f_d = −0.006.
  - Resolution: f_res = 3.0–5.1 with σ_f > 0.4 (not determined).

**Graded correction (frozen §7, mechanism sel): Z_MID,corr = 4.77 / 4.99 (canonical h 0.672 / 0.686), 4.11 / 4.35 (alt)
→ REAL by X7's rule** (`Z_MID_corr`, `Z_MID_corr_class`).
- The corrected size-halves amplitude is A = 1.657 / 1.703 / 1.520 / 1.562 ± 0.13–0.14.
- X11's all-source values are 1.640 / 1.684 / 1.505 / 1.545 (Z_STAT 5.21 / 5.47 / 4.47 / 4.74).

**So:** the size dependence is an artefact of splitting on a shear-dependent size, not evidence that the core excess is an
artefact. "Small sources A 1.10–1.24, consistent with the law" is the selection-suppressed half. The all-source excess
stands at X11's statistical level, with the caveats in "What this does not show".

## Step 0: X11's size-half numbers reproduced with X11's code (`x13_s0_check.out`: S0-1–S0-4 PASS)

- **Method.** X7's and X11's committed scripts ran unchanged through `x13_step0.py` (sha256-checked; only output and
  lane paths substituted). They ran on a cache rebuilt from the raw KiDS FITS in session scratch.
- **S0-1.** The 7 cache columns carry X7's committed sha256.
- **S0-2.** All 25 arrays of X7's per-cluster npz are equal (max |Δ| = 0).
- **S0-3.** 260 numbers of X11's analysis JSON are equal to 0.0: size2 and mag2 per-class Z; E3 and E3_clip for size2 and
  size4; all_MID; Z_MID. So are the verdict and E3_sub strings.
- **S0-4.** All step-0 checks pass. X7's extract E1 is N/A as declared: no F1 cache exists in this session.
- Reported: the step-0 `x11_measure_classes.npz` is byte-identical to X11's (sha256 a2518027…).
- This lane's own measurement also reproduces X11:
  - M1/M2: the ALL, size2 and size4 classes, max |Δ| = 0.
  - K1: the size A, s_boot, s_jk and Z_STAT, 3.6e-15.

| cell | A_S ± σ_STAT | A_L ± σ_STAT | ρ_cl = A_L/A_S | Δ_obs | all-source A_MID (Z_STAT) |
|---|---|---|---|---|---|
| canonical h 0.672 | 1.204 ± 0.132 | 2.030 ± 0.191 | 1.686 ± 0.219 | +0.826 ± 0.206 | 1.640 (+5.21) |
| canonical h 0.686 | 1.235 ± 0.131 | 2.109 ± 0.192 | 1.708 ± 0.220 | +0.874 ± 0.209 | 1.684 (+5.47) |
| alt h 0.672 | 1.104 ± 0.121 | 1.862 ± 0.175 | 1.686 ± 0.219 | +0.758 ± 0.189 | 1.505 (+4.47) |
| alt h 0.686 | 1.133 ± 0.120 | 1.934 ± 0.176 | 1.708 ± 0.220 | +0.801 ± 0.192 | 1.545 (+4.74) |

(`reference.<cell>`; MID, C\*, boost; paired bootstrap 2000 draws and X2's 30-patch jackknife.)

## The tests (canonical h 0.672 shown; all 4 cells in the `.out` and JSON)

**(a) Bands** (`a_bands`). Sub-verdict NOT DECISIVE in both bands, all cells.
- **OUTER** (1.42–3.0 Mpc; the record's OUTER is used for the brief's "1–3 Mpc"):
  - A_S 0.81 ± 0.11, A_L 1.07 ± 0.14, ρ = 1.32–1.34 ± 0.23.
  - ρ_OUTER − ρ_MID = −0.37 ± 0.31.
- **INNER** (0.15–0.46 Mpc): ρ = 2.6–3.2, but the bootstrap ratio σ runs to 6–300 (A_L ± 1.3–4.6).

**(b) Random points** (`b_randoms`, `b_null`). The null **PASSES**.
- The tangential stack at F1's random points, MID, in A units: S −0.000 to −0.006 (|Z| ≤ 0.11), L −0.006 to −0.024
  (|Z| ≤ 0.35), L − S |Z| ≤ 0.21.
- No additive size-dependent term.

**(c) Resolution and SNR at fixed size** (`c_res_snr`; 8 classes = size quartile × PSF-size or SNR half; GLS with
bootstrap covariance).

| | coefficient | Δ between size halves | f (16–84 %) | status |
|---|---|---|---|---|
| resolution (−β_p) | +3.8 / +6.8 / +3.5 / +6.2 | Δ ln(size/r_psf) 0.66 | 3.0 / 5.1 / 3.0 / 5.1 (2.1–7.8) | not determined |
| SNR (β_n) | −0.11 to −0.19 | Δ ln SNR 0.16 | −0.02 to −0.03 (−0.11 to +0.05) | determined, < 30 % |

- KiDS PSF sizes vary too little at fixed source size to separate resolution from size. At fixed size the PSF halves differ
  by 0.08–0.13 in ln r_psf, against 0.66 in ln(size/r_psf) between the size halves (`c_res_snr.<cell>.res.v`).
- The 8-class amplitudes are noisy (−3.1 to 5.3), because X11's per-class weights W = 1/E² are unstable in sparse
  class-bins.
- Observation, not graded: at fixed size, the larger-PSF half is lower in quartiles 1–3, by −0.65 / −0.83 / −0.72
  (± 0.5–0.6; h 0.672) and −0.73 / −0.96 / −0.85 (h 0.686).

**(d) Photo-z** (`d_photoz`, `d_catalogue_wmean_ZB`).
- **Mean Z_B per tomographic bin, S / L** (catalogue-wide): 0.222/0.216, 0.412/0.406, 0.602/0.608, 0.797/0.791,
  1.023/1.023.
- **In the MID apertures** at h 0.672, ⟨Z_B⟩ agrees to ≤ 0.9 % and ⟨s_B⟩ to ≤ 1.6 % per bin between the halves.
- **Naive ⟨s_B⟩ ratio L/S:** 0.985.
- **H_SOM** (each source's true z drawn from its bin's SOM n(z)):
  - b_S 0.946, b_L 0.943, b_ALL 0.945, ratio 0.997;
  - f_d = −0.006 (determined, < 30 %).
  - The weight share in bins cut by Z_B > z_l + 0.2 is 0.12.
- The photo-z route explains nothing of the size effect.

**(e) Independent lens sample** (`e_galaxy`, `e_classes`). F2's lens catalogue (all 181,477; 102,898 accepted randoms), P2's
estimator and bins. G1 reproduces the record's CFG110 per-lens sums exactly: WW ratio 1.0000000, ΔΣ ratio 1.000000 in all
15 bins.

| range | A_ALL | A_S | A_L | ρ_gal | ρ_gal (circ2) |
|---|---|---|---|---|---|
| "in" 0.03–0.35 Mpc (graded) | 1.675 ± 0.103 | 1.365 ± 0.129 | 2.013 ± 0.172 | **1.474 ± 0.192** | 1.026 ± 0.127 |
| O1 0.35–1.19 Mpc (reported) | | | | 1.258 ± 0.186 | 0.699 ± 0.123 |
| in + O1 (reported) | | | | 1.397 ± 0.140 | 0.904 ± 0.096 |

- Amplitudes are in 1/R-template units, so only the ratios matter. Clipped boost: 1.458 ± 0.188.
- Against the clusters: −0.73σ (h 0.672) and −0.80σ (h 0.686). Against 1: +2.47σ. This is E-MATCH in all 4 cells.
- The predicted selection ratio for the galaxy sources is 1.92 (`e_galaxy.pred_sel`).

**(f) Shear-induced size selection** (`f_selection`; the response comes from catalogue sums: the ±0.05 ln band at the edge,
⟨|e|⟩, the class weights).

| cell | R_S | R_L | predicted ρ | measured ρ | f_sel (16–84 %) | ρ_circ (gate) | ρ_FLUX_RADIUS |
|---|---|---|---|---|---|---|---|
| canonical h 0.672 | −0.298 | +0.326 | 1.89 | 1.69 ± 0.22 | 1.24 (0.99–1.64) | 1.128 ± 0.145 PASSED | 0.999 ± 0.136 |
| canonical h 0.686 | −0.297 | +0.328 | 1.89 | 1.71 ± 0.22 | 1.20 (0.97–1.57) | 1.166 ± 0.150 PASSED | 1.043 ± 0.137 |
| alt h 0.672 | −0.298 | +0.326 | 1.89 | 1.69 ± 0.22 | 1.24 (0.99–1.64) | 1.128 ± 0.145 PASSED | 0.999 ± 0.136 |
| alt h 0.686 | −0.297 | +0.328 | 1.89 | 1.71 ± 0.22 | 1.20 (0.97–1.57) | 1.166 ± 0.150 PASSED | 1.043 ± 0.137 |

- **Size quartiles, predicted vs measured** (canonical h 0.672): 0.94 / 1.40 / 1.80 / 2.77 against 0.88 ± 0.16 /
  1.46 ± 0.18 / 1.40 ± 0.22 / 2.23 ± 0.30.
- **K2 (exact-transform injection, 4·10⁶ synthetic sources)** confirms the first-order formula: measured response
  +0.186 / −0.187, formula ±0.180. The circularised split gives +0.008 / −0.009.
- **The catalogue prediction runs high in the data.** The overshoot is +0.20 in ρ in MID (0.9σ), 2.3σ for the galaxies
  and 2.4σ in OUTER (against MID's predicted 1.89).

## Correction and Z_MID (frozen §7; `corrections.<cell>.<kind>`; σ = max(bootstrap, jackknife))

| cell | none (halves, per-class W) | **sel (graded)** | d (H_SOM) | galaxy calibration | X11 all-source |
|---|---|---|---|---|---|
| canonical h 0.672 | 1.466 ± 0.113 (Z 4.13) | **1.657 ± 0.138 (Z 4.77)** | 1.551 (4.61) | 1.544 (4.11) | 1.640 (5.21) |
| canonical h 0.686 | 1.511 ± 0.115 (4.44) | **1.703 ± 0.141 (4.99)** | 1.600 (4.91) | 1.591 (4.36) | 1.684 (5.47) |
| alt h 0.672 | 1.344 ± 0.103 (3.33) | **1.520 ± 0.126 (4.11)** | 1.423 (3.86) | 1.416 (3.43) | 1.505 (4.47) |
| alt h 0.686 | 1.386 ± 0.106 (3.66) | **1.562 ± 0.129 (4.35)** | 1.467 (4.17) | 1.459 (3.70) | 1.545 (4.74) |

- **Uncorrected halves (`none`) sit below the all-source value.** X11's per-class inverse-variance weights give the small
  (selection-suppressed) half 68 % of the weight, so the halves combine to 1.47, not 1.64 (canonical h 0.672; 68 % = (2.030 − 1.466)/(2.030 − 1.204)).
- **The selection correction restores the all-source level** to within 1.1 %.
- **The res/snr corrections equal `none` by construction:** a linear correction referenced to the pooled mean cancels in
  the halves sum.
- **"d" mostly divides by b ≈ 0.945,** the Jensen factor of the extreme H_SOM hypothesis. It is not a calibration.

## Checks

| script | checks | MUTATE |
|---|---|---|
| `x13_step0.py` → `x13_s0_x7_*`, `x13_s0_x11_*` | X7 E2, E3 (E1 N/A), G1–G3, M1–M6; X11 X1–X3, M1–M6, R1–R3, S0-K1, K1–K4: all PASS | — |
| `x13_s0_check.py` | S0-1–S0-4 PASS | S0-3 FAIL as required (size2 labels swapped) |
| `x13_extract.py` | X1–X3 PASS (0.965 GB) | X1 FAIL as required (no reorder) |
| `x13_measure.py` | M1–M4 PASS (476 s, 0.935 GB); M1/M2 exact | M1, M2 FAIL as required (20 clusters, e2 flipped) |
| `x13_galaxy.py` | G1–G3 PASS (65 s, 0.60 GB) | G1 FAIL as required (cross shear) |
| `x13_analysis.py` | X7-K1, K1–K4 PASS (26 s, 0.875 GB) | K1 FAIL as required (cross shear) → UNDECIDED |

## Coordinator rerun (2026-10-24)

The coordinator reran the whole chain on its own cache, rebuilt independently from the raw KiDS FITS during the X11 rerun:
- extract, measure, galaxy and analysis, each with its MUTATE twin;
- the SOM n(z) re-extracted from the tarball.

Results:
- `psfD`, `snr`, `frad` and `x13_edges.json` are byte-identical to the lane's;
- so are `x13_measure_classes.npz` and `x13_galaxy_sums.npz`;
- every result line of the 16 `.out` / `.json` files is identical, and only timing and RSS lines differ;
- the main runs pass 3/3, 4/4, 3/3 and 5/5 checks at peak RSS ≤ 0.959 GB;
- each MUTATE twin fails its named checks (X1; M1, M2; G1; K1).

## Amendments (full text in `FROZEN_CRITERIA.md`)

- **A1 (PRE-RESULT, implementation).** Several declared scope limits:
  - the extract MUTATE stops after X1/X3;
  - the galaxy MUTATE covers the first 6 declination rows;
  - the measurement drops X11's 90° identity and geometry;
  - the galaxy gather reach is 1.19 Mpc;
  - the step-0 X7 extract exits 1 by its N/A E1.
- **A2 (POST-RESULT for K4 only).** The development run of the analysis failed K4 at 1.79 GB, and a second run failed at
  1.005 GB. The development run was made before S0 had run, so it read UNDECIDED by the precondition.
  - Fixes: chunked K2, chunked catalogue reads, a finiteness assertion in place of spurious BLAS warnings, K2/K3 run first,
    and the random rotations freed after (b).
  - K2's synthetic stream changed; it passed in both runs.
  - Every other statistic is identical leaf by leaf.

## What this does not show

- **The response's normalisation is not established.**
  - The selection response is first-order and uses the catalogue's noisy |e| at the cut. It overshoots the measured ratios:
    MID 1.89 vs 1.69 ± 0.22, galaxies 1.92 vs 1.47 ± 0.19, OUTER 1.89 vs 1.33 ± 0.23.
  - The mechanism's sign, size and nulls fit: circularised size, FLUX_RADIUS, galaxies, random points.
  - Image simulations (a metacalibration-style selection response) are not on disk.
  - If the true response is smaller, the corrected halves move towards the uncorrected 1.47 (canonical h 0.672). The
    all-source estimator has no split and is unaffected.
- **The semi-major-axis convention (B11) is inferred, not documented.** It rests on the data (ρ_circ ≈ 1.13–1.17 vs 0.52
  predicted under the alternative), not on the lensfit papers.
- **The all-source sample's own selection is not tested.** The KiDS gold cuts carry their own selection response, which
  KiDS's image-simulation m calibrates. That is inherited here, as m = −0.01.
- **Resolution is not separated from size.** At fixed size the PSF halves differ by only 0.08–0.13 in ln r_psf. A hint that
  the larger-PSF half is lower at fixed size (quartiles 1–3) is not graded.
- **H_SOM is an extreme hypothesis** (no within-bin Z_B information). Per-class n(z) are not on disk. b ≈ 0.945 is a
  property of the hypothesis, not a calibration.
- **INNER is too noisy** to say anything. OUTER (1.33 ± 0.23) cannot tell 1 from MID's ratio.
- **The galaxy O1 circ2 ratio (0.70 ± 0.12) is reported, not graded.** That range is dominated by the lenses' environment
  (F2, P2).
- **Nothing here tests X7's CAL rule or the cross offset** (X11's domain), the C\* model (inherited normalisation), or the
  physical reading of the excess. It also does not address X11's other near-candidate E3 variables: cluster z, Δχ² 6.1–8.1;
  MID radial profile, 8.3–9.6.

## Against the record (suggested fixes; no other file edited)

1. **X11 README** ("the tangential excess depends on source size … mechanism unidentified", and "What this does not show").
   Suggest replacing the caveat with: "the size dependence is the shear-induced selection of a split on the lensfit
   (semi-major-axis) scalelength (X13). A circularised-size split and a FLUX_RADIUS split show none. The same ratio appears
   around 181k galaxy lenses. The all-source A_MID is unaffected; selection-corrected halves give Z_MID 4.1–5.0".
2. **X11 "Z_MID re-derived" table** ("small sources Z_STAT +0.9 to +1.8 … Which half measures the true lensing amplitude is
   not known"). Neither half does. The halves are biased by about ∓30 % in opposite directions. The all-source value (or the
   corrected halves) is the amplitude.
3. **Any lane that splits KiDS sources by `bias_corrected_scalelength_pixels`** (or by any quantity built from it, such as
   size/PSF) and reads a tangential amplitude per class needs a selection-response correction or a shear-invariant size
   (r_ab, FLUX_RADIUS). Splits by MAG_AUTO, SNR, PSF or Z_B do not have this problem at first order.
4. **MAP §1.A.3 / X7 V1.** Together with X11 (cross offset consistent with noise), the core excess is best quoted as
   "Z_MID 4.5–5.5 statistical (all-source), 4.1–5.0 with selection-corrected size halves; the source-size dependence is a
   split-selection artefact (X13)". κ = ½ FITTED; footings never pooled.

## Files and runs (`OMP_NUM_THREADS=1 nice -n 15`; scratch paths are session-local)

| file | what |
|---|---|
| `x13_step0.py` | runs X7's / X11's committed scripts read-only → `x13_s0_x7_*`, `x13_s0_x11_*` (.out, .json) |
| `x13_s0_check.py` → `.out`, `_results.json`, `_MUTATE.*` | S0-1–S0-4 |
| `x13_extract.py` → `.out`, `_results.json`, `_MUTATE.*` | psfD, snr, FLUX_RADIUS columns; frozen edges (scratch `x13_edges.json`) |
| `x13_common.py` | X11's `x11_common.py` copied with provenance, this lane's classes and 7 extra sums |
| `x13_measure.py` → `.out`, `_results.json`, `_MUTATE.*` | cluster measurement (scratch `x13_measure_classes.npz`) |
| `x13_galaxy.py` → `.out`, `_results.json`, `_MUTATE.*` | P2's estimator on F2's lenses with size classes (scratch `x13_galaxy_sums.npz`) |
| `x13_analysis.py` → `.out`, `_results.json`, `_MUTATE.*` | tests (a)–(f), decision, correction |

Run order:
1. `x13_step0.py x7_extract <cache>`, `x7_regress <cache>`, `x7_measure <cache> <s0>`, `x11_extract <cache>`,
   `x11_measure <cache> <s0>`, `x11_randoms <cache> <s0> --part1`, then `--part2`, then `x11_analysis <s0> <cache>`.
2. `x13_extract.py <cache>`.
3. `x13_galaxy.py <cache> <work>`.
4. `x13_measure.py <cache> <s0> <work>`.
5. `x13_s0_check.py <cache> <s0>`.
6. `x13_analysis.py <s0> <work> <cache> <SOM n(z) dir>`. The SOM n(z) dir is extracted from
   `../_external_data/kids_lensing_zsplit/KiDS1000_SOM_N_of_Z.tar.gz`.

Read-only inputs:
- the KiDS FITS and SOM n(z) tarball (outside the repo)
- the eRASS1 FITS
- `lr_lenses.npz`, `cfg96_stack.npz`, `cfg110_perlens.npz`
- X7's, X11's, X2's, F1's, F2's and P2's sources and committed products
- the Chae+21 CSV (via X2)

Nothing was downloaded.
