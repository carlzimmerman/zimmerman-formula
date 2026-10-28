# CORRECTION (2026-10-27, after the owner asked "are you sure?"): the non-detection is NOT a meaningful result

Three errors in this lane, fixed forward. The sections below are kept as written.

1. **The redshift I froze (z = 1.4906) was not the galaxy's systemic value.** Di Teodoro+2018 measure **z = 1.4888 ± 0.0011** from the MUSE [OII] doublet; Kelly+15 give 1.489, and Smith+09 gave 1.491. The delivered cube is centred on z ≈ 1.491 (RESTFRQ 138.818 GHz, LSRK). Relative to z = 1.4888 it covers only **+15 … +513 km/s**, so **the systemic velocity and the whole blue half of the line are outside the delivered cube**, and every integration window here was centred ~220 km/s off the line.
   - Labelled post-hoc: the in-band red wing (+15 … +60 km/s) shows nothing. KLASS r = 1″: +0.025 ± 0.061; pointing centre r = 1″: +0.037 ± 0.052 Jy km/s.
   - **"No CO detected" and "too shallow" are therefore not established.** This cube mostly does not contain the line.
2. **Wrong pointing.** All four pointings (A1.1–A1.4) share one MOUS, and I took the first target name returned (A1.4). **Pointing A1.1 is centred on the KLASS-1501 position (0.2″)**; A1.4 is 10.7″ away. The claim that A1.4 "matched the KLASS position" was wrong. All four delivered CO cubes are the same size, so they very likely share the same narrow velocity window, and the A1.1 cube would probably have the same coverage problem.
3. **Error bars about 15–20 % too small.** Adjacent channels are correlated (r = 0.17), and sums of ≥ 5 channels have 1.13–1.14× the assumed noise. The upper limit 0.90 Jy km/s becomes ≈ 1.07, and the post-hoc S/N values shrink by ~1.2.

**What stands:**
- The K2 failure (the noise expectation was mis-derived).
- The lane is INVALID as frozen.
- **The delivered ALMA products cannot measure this galaxy's CO(3-2) at its systemic redshift.** The full spectral window (138.35–139.29 GHz) does cover the line (138.941 GHz), so a measurement needs re-imaging from the calibrated visibilities (raw ASDMs ~96 GB, CASA) or a reprocessed product.

# CFG970: SN Refsdal host CO(3-2) from ALMA 2013.1.00582.S (A1.4). INVALID as frozen; CO not detected; the archival cube is too shallow to test the law's gas need

**Read first.**
- **The frozen reading is INVALID.** Two of three controls failed.
- **K2:** my pre-registered noise expectation, 48.4 µJy/beam per 2 km/s, was wrong. I read ObsCore's "66.6 µJy/beam @native" as a per-channel rms, and it isn't. The measured flat-frame rms is **1.05 mJy/beam per 2 km/s**. That is *better* than ObsCore's own 0.95 mJy/beam at 10 km/s scaled to 2 km/s (2.1 mJy/beam).
- **K3:** the injected discs were not recovered: 0.1 Jy km/s not found; 0.3 and 1.0 Jy km/s recovered at 11 % and 40 %, with W50 inflated.
- **No CO(3-2) is detected.**
- **The frozen design has a flaw, found after the run:** the primary image was defined as the source within 3″ of the *KLASS* position. That position is a different lensed image of the host, 11″ from this pointing's own target (image A1.4 at the pointing centre). A labelled post-hoc check covers both positions.

## Process
- Criteria: 1b0dee952f (committed alone, headers only seen).
- Script: 40c6d52e96, committed before its first run.
- Run 1 stopped at a setup line before any science pixel was read (WCS 0-d arrays); fixed in 3313fcda82.
- Run 2 printed K2 FAIL and G0 = UPPER LIMIT, then crashed. Fixes in be20318fc2: the distance-block namespace, and S3/S4 reported "n/a" without a detected line, since the criteria were silent on non-detections.
- Run 3 found no K3 injection site: with 210 noise regions, every site was excluded. Fixes in the next commit: sites avoid only KLASS, the pointing centre and the 10 largest regions; S7 is skipped without a line.
- **Every fix after run 1 was made after seeing outputs and is disclosed.** No threshold or class was changed.
- Peak RSS was **1.17 GB, above the declared 1 GB.**
- κ = ½ FITTED; footings never pooled; not theory closed.

## Results (reported; nothing graded, because the lane is INVALID)
| item | value |
|---|---|
| K1 identity | PASS: sha256 ×4, header as recorded |
| velocity coverage (relative to z 1.4906) | −202 … +296 km/s |
| flat-frame rms per 2 km/s channel (PB ≥ 0.9) | 1052.6 µJy/beam (**K2 FAIL** against 48.4) |
| S1 | 210 regions kept, all small (≤ 13 beams × 14 channels); the "primary" within 3″ of KLASS is a 4-channel blip |
| **G0** | **UPPER LIMIT:** S Δv ≤ 0.895 Jy km/s (3σ, 2″ aperture, ±200 km/s) |
| S3 / S4 | n/a (no detected line) |
| S5 apparent gas mass (native D_L 11,056 Mpc; L′_CO(3-2) ≤ 1.19 × 10¹⁰) | M_gas,app ≤ 1.2 × 10¹⁰ (α_CO 0.8, R₃₁ 0.8) … 1.03 × 10¹¹ (α_CO 4.3, R₃₁ 0.5) |
| S6 μ* (upper bounds), 48 corners | 0.26 … 23.4 → **UNDECIDED (only GAS SHORT is readable from an upper limit)** |
| implied a₀/a₀,local (V 128, gas at the limit), μ 4 / 5.42 / 12.4 | 0.70–3.51 / 0.90–4.03 / 1.62–5.24: spans FLAT and H(z); one disc excludes nothing |
| K3 | 0.1 not found; 0.3 → 0.033 (11 %); 1.0 → 0.401 (40 %); W50 320–351 vs 138 true: **FAIL** |
| MUTATE (channels shuffled) | primary not found, S/N 0 (< 3), rc 1. **Vacuous:** the unshuffled run found nothing either |

## Post-hoc, labelled (`cfg970_posthoc_apertures.py`; written after the INVALID run)
Aperture sums over ±150 km/s:

| position | r = 1″ | r = 2″ |
|---|---|---|
| KLASS position (PB 0.86) | −0.135 ± 0.128 Jy km/s | −0.032 ± 0.258 |
| pointing centre = image A1.4 (PB 1.00) | +0.177 ± 0.110 (1.6σ) | +0.107 ± 0.220 |

**Neither position shows CO(3-2).** For scale (hand arithmetic, using the run's own conversion of 1.33 × 10¹⁰ K km/s pc² per Jy km/s): if the law holds at V_flat = 128 km/s, the apparent CO(3-2) flux should be about 0.6 Jy km/s at the least demanding corner (μ = 4, α_CO = 4.3, R₃₁ = 0.5), and about 3 Jy km/s at μ = 12.4, R₃₁ = 0.8. Lower α_CO gives ×5 more.

These are comparable to the aperture limits, but the lensed image extends over several arcseconds and K3 shows the finder cannot recover sources at this depth. **So this cube cannot tell whether the law's gas need is met.** A real test needs:
- deeper CO data (about 10× the 1542 s), or
- the other pointings (A1.1–A1.3, about 0.88 GB each), together with a lens model to know where each image sits and how magnified it is.

## What this means
- **Top candidate, status:** there is no usable public cold-gas measurement. The rank-1 entry of the a₀(z) target search is updated to say so.
- **For the a₀(z) programme:** the gas mass for the Refsdal host needs new ALMA time (or the other three images plus a lens model), the same as for the other candidates. The ranking is unchanged; only the "existing CO" advantage is gone.
- **Lessons recorded:**
  1. Expected-noise controls must be derived from the per-channel sensitivity, not ObsCore's "@native" figure.
  2. Multiply-imaged sources need the lens model's image positions before a primary image is defined.

## Files
`FROZEN_CRITERIA.md`, `cfg970_co_btfr.py` (`MUTATE=1`), `cfg970.out`, `cfg970_results.json`, `cfg970_MUTATE.out`, `cfg970_results_MUTATE.json`, `cfg970_posthoc_apertures.py` / `.out` / `.json`. The cube stays in `_external_data` (not in git).
