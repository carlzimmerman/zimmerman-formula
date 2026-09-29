# KURVS-CDFS × GOODS-ALMA 2.0 (1.1 mm) cross-match

Built 2026-09-29 by `build.py`, on the owner's go ("yes, do the GOODS-ALMA cross-match from the arXiv HTML page"). The only thing fetched is the HTML page https://arxiv.org/html/2106.13246
(Gomez-Guijarro+2022, A&A 658, A43), kept in `raw_small/` with its sha256 in `manifest.json`; tables are parsed from its HTML cells by code, not read through a summariser. Data only: no gas mass, no conversion, no verdict.

## What the survey states (all from that page)
- ALMA Band 6, single tuning centred at 265.0 GHz (λ = 1.13 mm); frequency range 255.06–274.94 GHz.
- Area 72.42 arcmin² at primary-beam response ≥ 20%, centred 03:32:30, −27:48:00; ~10′ × 7′; six parallel slice submosaics of ~6.8′ × 1.5′ at position angle 70°.
- Combined-map rms per slice (Table 1): A 68.1, B 67.7, C 68.6, D 68.7, E 68.4, F 68.8 μJy/beam, mean 68.4; synthesized beam 0.447″ × 0.418″. Noise maps were built from a sliding 10″ × 10″ box on non-primary-beam-corrected maps (Sect. 2.3); **those maps are not in the HTML**.
- Blind detection: PyBDSF, island threshold σ_f = 2.7, and 100% purity for σ_p ≥ 4.4 in the combined map (5.2 high-res, 4.2 low-res); 44 sources (Table 2).
- Prior-based: at σ_p = 3.0 the blind run gives 573 positive vs 475 negative detections; 44 more sources are added using IRAC and VLA prior positions with a stellar-mass check (Table 3, S/N_peak 3.59–5.27 as parsed).
- Both tables give the flux in the combined map, ±1σ, in mJy (1.1 mm).

## Files
| file | content |
|---|---|
| `goodsalma2_catalogue.csv` | 88 sources: id, RA, Dec, ZFOURGE id, z, log M*, S/N_peak, S(1.1mm) ± err, high-res/low-res flags |
| `kurvs_goodsalma_nearest.csv` | per KURVS galaxy: nearest and second-nearest source, separations, everything within 10″ |
| `kurvs_goodsalma_footprint.csv` | position in the mosaic frame (along/across PA 70°) and margin to the edge |
| `kurvs_goodsalma_summary.csv` | the per-galaxy table for the calc thread |
| `checks.txt`, `manifest.json`, `build.py` | 8 PASS checks; provenance |

## Results
**Matches within 1.5″ (2 of 22).**
- KURVS-12 ↔ A2GS34, separation 0.39″, S(1.1 mm) = 0.74 ± 0.10 mJy, S/N_peak 5.86, blind table; catalogue z = 1.613 = KURVS z_Hα 1.613.
- KURVS-22 ↔ A2GS13, 0.24″, 1.36 ± 0.12 mJy, S/N_peak 9.3, blind table; z = 1.619 vs 1.618.
Both are outside the calc thread's ten. Expected chance matches at 1.5″ for 22 galaxies at the catalogue density: 0.05; both matches also agree in redshift, so they are real associations.
**None of the ten** rotation-supported discs has a catalogue source within 1.5″.

**Placement** (the paper's stated PA and size). The six slices sit at PA 70°; whether the 10′ side runs along PA 70° is my reading. I tested both: the paper's own 88 sources fit a 10′ × 7′ rectangle
with the 10′ side along PA 70° at 95% (73% for the other reading), so that reading is used; the sources' own envelope is 4.9′ × 3.9′ (half-extents), slightly larger than the nominal 5.0′ × 3.5′ in one axis. For the ten:
| KURVS | placement (nominal rectangle; envelope of the 88 sources) | margin to edge |
|---|---|---|
| 9 | inside | 1.6′ |
| 11 | inside | 0.9′ |
| 16 | inside | 1.4′ |
| 15 | inside | 1.6′ |
| 13 | inside (envelope: within 0.5′ of the edge) | 0.6′ |
| 17 | inside (envelope: within 0.5′ of the edge) | 0.5′ |
| 3 | on the edge (nominal: 0.4′ outside; envelope: 0.0′) | ≈0 |
| 21 | on the edge (nominal: 0.0′ outside; envelope: 0.35′ inside) | ≈0 |
| 7 | on the edge (nominal: 0.03′ inside; envelope: 0.07′ outside) | ≈0 |
| 8 | outside (0.8′ beyond the nominal edge) | — |

**Non-detections.** For 9, 11, 16 (inside; nearest sources 17.5″, 21.9″, 21.3″) and 13, 15, 17 the catalogue lists no source at their positions. Facts for the limit: slice-level combined rms 67.7–68.8 μJy/beam (uncorrected for primary beam); blind 100%-purity threshold σ_p ≥ 4.4 (≈ 0.30 mJy at 68.4); prior-based S/N ≥ ~3.5 but only at IRAC or VLA prior positions; the faintest blind-table source in the catalogue is 0.49 mJy (median 0.89), the faintest prior-based 0.25 mJy. The **local** rms at each position is not available (noise maps not in the HTML), and near the mosaic edge (13, 17, 3, 21, 7) the primary-beam-corrected noise rises toward the 20% response limit. A catalogue non-detection is not a measured limit at that position.
**KURVS-15 note (fact only):** a prior-based source A2GS75 lies 6.9″ from it, catalogue z = 1.618, S = 0.69 mJy, versus z_Hα = 1.613 for KURVS-15; it is outside the 1.5″ rule. its catalogue row: S/N_peak 3.96, log M* 11.25 (KURVS-15: 10.07), flagged 100%-pure in the low-resolution map; the position uncertainty is not tabulated.

## Not done
No flux limits at positions, no maps, no gas conversion, no other surveys (ASAGAO's catalogue is only in its paper, A3GOODSS not fetched).
