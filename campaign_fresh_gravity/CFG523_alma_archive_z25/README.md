# CFG523: ALMA archive mining for z ≈ 2–3 discs that reach the deep regime. Ten shortlisted, none usable from pipeline products, and the positive control fails too

> **κ = ½ FITTED.** Footings 9.36e-11 and 1.13e-10 m s⁻² are never pooled. FLAT a₀(z) is the distinctive law and a₀ ∝ H(z) is the rival (+0.57 dex at z 2.5). The cold energy mass is still required. **No a₀ is measured here.** No sentence says the data favour a law.
> Criteria: `FROZEN_CRITERIA.md`, committed alone as **429b1d7a6** before any query. The owner approved this in chat on 2026-10-09 ("yes mine the ALMA archive"). Only public pipeline product FITS were read, never raw ASDMs. Every file carried DataLink `link_auth = false`. Fetch record: `FETCH_LOG.md`. Data live outside git in `../../../_external_data/cfg523_work/`.

## Bottom line
1. **Inventory.** There are 220 parent discs at 2.0 ≤ z ≤ 3.0 (KMOS3D 184, SINS-AO 33, ALPAKA 10; 211 have M★ and R_e). Against 14,998 ALMA obscore rows in their fields, **33** have a public CO / [CI] / [CII] window at ≤ 0.30″ (G2). Another 16 are covered only at 0.30–0.60″. None is covered by proprietary data only. The predicted reach y(2 R_e) ≤ 2 holds for 76 of 211. **Shortlist (G1–G4): 10. Relaxed list (2 < y ≤ 4): 6.** The blind sweep holds 30,711 public rows at ≤ 0.30″ in the sub-mm/starburst/lensing/structure keywords: 435 proposals and 3,562 target names, with no redshifts (`cfg523_sweep_results.json`).
2. **Measured gates: all 10 shortlisted targets are NOT USEFUL as pipeline products** (`cfg523_cubes.out`).
   - Seven fail M1: no line detection with peak moment-0 S/N ≥ 5 within 1″.
   - ZC406690 is detected (CO(4–3), S/N 5.7) but is compact. It fails M2 with R_out 0.21″ (1.8 kpc), which is smaller than one beam.
   - Two have no pipeline cube at all: U4_22581 (AzTEC101 snapshot) and GS4_30443 (HUDF 2012 programme). Both are raw only.
   - **No target reached M3, so no y_meas and no a₀ analysis.** The frozen V×0.5 MUTATE was never reached.
3. **Positive control (POST-FREEZE, dated 2026-10-09): it FAILS.** The test was zC-400569 (z 2.24; Lelli+23 published a CO rotation curve from programme 2019.1.00862.S; in the record as CFG278). Through the same gates its pipeline CO(4–3) cube gives peak S/N 4.9, so M1 fails. Smoothed to 0.6″ it gives S/N 7.4, but only one beam-spaced position, so M2 fails. The line is plainly present in a 2″ aperture: 5–6σ per 100 km/s bin over about 500 km/s. **So the gates are not sensitive enough on pipeline cubes to recover even a published curve.** The NOT USEFUL labels describe the pipeline products under these moment-map gates. They do not show that these galaxies lack rotating gas at large radius. A real answer needs uv-plane / tapered re-imaging and 3D forward modelling (3DBarolo-type) from the raw visibilities. That is outside the approved scope (no ASDMs).
4. **Nothing here constrains a₀.** The archive route on public pipeline products, at z 2–3, is **exhausted for this parent set at the moment-map level**.

## Shortlist (predicted reach; baryons = M★(1+μ_Tacconi18), a predictor only)
| galaxy | z | log M★ | R_e kpc | y_pred(2R_e) 9.36e-11 / 1.13e-10 | y(R_e/2) | line, programme, res | measured gate |
|---|---|---|---|---|---|---|---|
| GS4_20623 | 2.575 | 10.01 | 4.10 | 0.80 / 0.66 | 2.3 | CO(3–2), 2023.1.01296.S (24″ off-axis serendipitous), 0.26″ | M1 fail (3.2) |
| U4_22581 | 2.166 | 10.19 | 3.90 | 1.12 / 0.93 | 3.2 | CO(7–6)/[CI](2–1), 2013.1.00781.S (54 s) | no pipeline cube |
| ZC406690 | 2.195 | 10.62 | 5.40 | 1.29 / 1.07 | 3.6 | CO(4–3)+[CI](1–0), 2024.1.01443.S (7.3 h), 0.22″ | detected 5.7; M2 fail (R_out 0.21″) |
| COS4_05758/05803 | 2.102 | 10.42 | 4.35 | 1.35 / 1.12 | 3.8 | CO(3–2), 2019.1.00244.S (500 s), 0.25″ | M1 fail (2.8) |
| GS4_30443 | 2.226 | 10.10 | 3.30 | 1.35 / 1.12 | 3.8 | CO(6–5), 2012.1.00173.S (HUDF) | no pipeline cube |
| GS4_35951 | 2.186 | 11.00 | 7.48 | 1.39 / 1.15 | 3.9 | [CI](2–1), 2015.1.00098.S (HUDF mosaic, 178 s) | M1 fail (4.3) |
| GS4_20422 | 2.000 | 9.93 | 2.49 | 1.66 / 1.37 | 4.7 | CO(7–6), 2015.1.00098.S (122 km/s channels) | M1 fail (3.0) |
| COS4_03324 | 2.307 | 10.62 | 4.82 | 1.66 / 1.38 | 4.7 | CO(3–2), 2022.1.01644.S (4.9 h), 0.25″ | M1 fail (3.3) |
| COS4_19753 | 2.469 | 10.51 | 4.16 | 1.87 / 1.55 | 5.3 | CO(3–2), 2023.1.01052.S (5.6 h), 0.26″ | M1 fail (3.0) |
| COS4_02672 | 2.308 | 10.57 | 4.22 | 1.98 / 1.64 | 5.6 | CO(3–2), 2022.1.01644.S (3.1 h), 0.25″ | M1 fail (3.5) |

The relaxed list is ZC400569 (CFG278; it served as the positive control), U4_34817, Q2343-BX610 (CO(4–3) at 0.043″, already in the record via RC100/CFG280/CFG227), ZC404221, COS4_04717 and COS4_03206. Full rows are in `cfg523_inventory.out` and `cfg523_inventory_results.json`.

Overlap with the record: the G2 set includes ALPAKA 13–22 (CFG227/237/272), GS30274, HATLAS J084933 and the CLJ1001 trio; none was re-scored. CFG403 already matched these parents to ALMA at ≤ 0.6″ (101 with gas). This lane adds the ≤ 0.30″ cut, the reach predictor and the cube-level gates.

## Controls and disclosed departures (all dated 2026-10-09)
- **Inventory MUTATE (+60″ Dec): premise NOT MET.** 6 of 33 G2 matches survive (18 %, against ≤ 10 %). All six survivors sit inside large mosaics or wide primary beams (HUDF mosaics, AzTEC/DSFG fields). The footprint test is s_region / FOV-based, so coverage is not on-target pointing. The shortlist rows that were off-axis serendipitous (GS4_20623, GS4_20422, GS4_35951, GS4_30443) are exactly this case.
- **Cube MUTATE (channel scramble; an addition, not frozen):** 0 cubes pass M2. The premise is met, but trivially, because no unscrambled cube passes M2 either.
- **C1 check fixed after the first run.** "10 R_d within 3 % of Kepler" was mis-specified, since a thin disc exceeds Kepler by about 6 % there. It was replaced by the 100 R_d limit. No reach number changed.
- **Moment-0 pipeline, changed after the first pass:**
  - Per-pixel continuum subtraction was added. Without it, GS4_20422 passed M1 on dust continuum.
  - The moment-0 noise is now the robust spatial rms outside 1.5″, replacing the per-pixel channel MAD.
  - Fully blanked channels are dropped (one HUDF channel).
  - The final labels come from the corrected code, and both first-pass outputs were overwritten. The aperture spectra I computed independently agree: COS4_02672 shows ≤ 2σ per 100 km/s bin in 0.5–2″ apertures, and ZC406690 shows a 10σ bin in 0.5″ falling to 3σ in 2″.
- **Byte-range fetching (departure from "download products").** The archive answers closed ranges with 416 and open ranges with 206. Each channel's row block was therefore read with an open range and closed after the needed bytes (`cfg523_fetch.py`). Total transferred: **5.60 GB (5,601,940,456 bytes) in 2,423 requests**, including one 0.224 GB range-support probe, which was logged and deleted. Sub-cubes stored: 0.55 GB. The full cubes would have been about 52 GB, of which 32 GB is one HUDF cube.
- Positive control and 0.6″ smoothing are POST-FREEZE diagnostics: `*_CONTROL*` and `*_SMOOTH0.6*` outputs. They are not verdicts.
- Pipeline products are incomplete. For example, 2019.1.00862.S has no pipeline cube of the CO(3–2) spectral window even though `frequency_support` lists it. Coverage in obscore does not imply a product.

## What would make this crispy (new observations / reprocessing)
1. **Cheapest next step, no new telescope time:** re-image the raw visibilities with a uv-taper (0.4–0.6″) and fit 3D models for:
   - ZC406690 (2024.1.01443.S, CO(4–3)+[CI](1–0), 7.3 h)
   - COS4_03324 and COS4_02672 (2022.1.01644.S)
   - COS4_19753 (2023.1.01052.S)
   - and validate first on zC-400569 (2019.1.00862.S).

   This needs the owner's approval for ASDM downloads (sizes not priced; probably 100s of GB) and CASA.
2. **New ALMA:** a CO(3–2) or [CI](1–0) programme at 0.3–0.5″ with about 10–20 h per galaxy, so that surface brightness reaches 3 R_e. Targets: the low-y_pred extended discs above, especially GS4_20623 (y 0.8), GS4_35951 (R_e 7.5 kpc), ZC406690 and COS4_05758. This is CFG385's specification: 10–20 discs, each spanning y ≳ 3 inside to ≲ 0.3 outside at about 5 % velocity precision.
3. **New VLA:** CO(1–0) for the same discs (Ka band, B/C configuration) for a low-J gas mass. The SHAPE comes from CO/[CI]/dust maps and NIRCam stellar maps. Self-calibration (CFG385) then frees the absolute normalisation, which bypasses the 0.1 dex gas wall.

## Files
- `FROZEN_CRITERIA.md`
- `cfg523_inventory.py` with `.out`/`_results.json` and MUTATE outputs
- `cfg523_sweep.py` and `cfg523_sweep_results.json`
- `cfg523_fetch.py` (capped, logged range fetcher)
- `cfg523_cubes.py` with outputs: main, MUTATE, CONTROL, SMOOTH0.6
- `cfg523_fetchlog.py` and `FETCH_LOG.md`

Run order: `nice -n 10 python3 cfg523_inventory.py; MUTATE=1 …; python3 cfg523_sweep.py; python3 cfg523_cubes.py; MUTATE=1 …; CONTROL=ZC400569 …; SMOOTH=0.6 …; python3 cfg523_fetchlog.py`.
