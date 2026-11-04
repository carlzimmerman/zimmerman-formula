# FN4c_brouwer_lens_rebuild: FROZEN CRITERIA (written and committed alone, before any script or number of this lane)

Item 4 of the finish push (`finish_2026_11_04/README.md`), row group "KiDS isolated-lens lensing". κ = ½ FITTED. Not theory closed. Nothing here says the data favour the framework. Footings never pooled: canonical a0 = 9.3603e-11 m/s², alt a0 = 1.1312e-10 m/s². No download: every input below is already on disk.

## Question
Can Brouwer et al. 2021's isolated-lens sample (B21; A&A 650, A113; arXiv:2106.11677) be rebuilt from the KiDS-bright DR4 catalogue on disk to within 5 % of its 259,383 lenses? If yes, does the law's lensing gap (LE1: the law about 0.09 dex short under every grader) survive on the rebuilt lens inventory?

The lead's brief cites arXiv 2101.06010. That is the KiDS-bright catalogue paper (Bilicki et al. 2021, A&A 653, A82). The isolation criterion is in B21, so B21 is the source used here.

## What was read before this freeze (not blind)
- The record's rebuilds and their counts: June 2026 `lr_esd_remeasure.py` (scan of a comoving cylinder; 203,633 at |Δχ| < 10 Mpc, count-calibrated; later inventory 181,477); CFG903 (I2 physical 3 Mpc 118,994; I5 count-matched 259,963); LAM1 (comoving sphere 554,316, (1+z)-scaled sphere 422,562); NV2 (486,584 of 773,192 candidates, comoving sphere).
- B21 Sect. 3.1, 3.2, 3.3 and Appendix A (arXiv HTML, read as a web page, nothing saved).
- The authors' public code, read as web pages (nothing saved, nothing run): github.com/margotbrouwer/EG_project at its last commit 4cc0a57826 (2021-06-29). Files: `isolated_lens_selection.py`, `modules_EG.py` (`import_kidscat`, `calc_Dc`), `mass_range_selection.py`, `create_weightcat.py`, `configs/ggl_mdm_k1000.config`, `configs/ggl_k1000_replace.config`, `configs/run_shearcode.py`.
- Column lists and sha256 of the two KiDS-bright files; the header of the KiDS-1000 shear catalogue; LE1's README and how its graders read `lens_inventory.npz`; the June inventory's weighted bin masses (printed once while tracing LE1's inputs).
- No count, fraction or mass from this lane's recipe has been computed.

## The recipe (primary), with its source
| Step | Rule | Source |
|---|---|---|
| P1 parent | Public KiDS-bright DR4: `KiDS_DR4_brightsample.fits` (sha256 8baab69942bc…) and `KiDS_DR4_brightsample_LePhare.fits` (36e35e31a31f…), 1,239,422 rows each, joined row by row on equal `ID` | B21 3.3; the files used by LAM1 and NV2 |
| P2 neighbour pool | every row with finite log M★ and 0 < z < 0.5, z = `zphot_ANNz2`. **No mask cut on the pool.** | `isolated_lens_selection.py` (`nanmask`) |
| P3 stellar mass | log M★ = `MASS_BEST` + (MAG_GAAP_r − `MAG_AUTO_CALIB`)/2.5 | B21 footnote 10; `import_kidscat` |
| P3a MAG_GAAP_r | not in the public bright files. Taken from the KiDS-1000 SOM-gold shear catalogue on disk (`KiDS_DR4.1_ugriZYJHKs_SOM_gold_WL_cat.fits`, column `MAG_GAAP_r`) by nearest positional match within 1.0″ | this lane's stand-in (S1) |
| P3b unmatched rows | fs = median of the matched rows' (MAG_GAAP_r − MAG_AUTO_CALIB)/2.5 in the same 0.25-mag `MAG_AUTO_CALIB` bin; the global matched median if a bin has fewer than 50 matched rows | this lane's stand-in (S2) |
| P4 "too heavy" | per lens, log M★ bins of width 0.006 over (7, 13] (1000 bins, lower edge open). A neighbour is too heavy if log M★,sat > log10(0.1 × mean of 10^logM★ over the pool rows in the lens's bin). A lens outside (7, 13] is never isolated | `isolated_lens_selection.py` |
| P5 distance | each galaxy at (RA, Dec, D_A), D_A = D_C/(1+z), flat ΛCDM H0 70, Ωm 0.2793, ΩΛ 0.7207, no radiation (astropy `LambdaCDM`). Separation = 3D Euclidean distance between these points | `isolated_lens_selection.py`, `ggl_mdm_k1000.config` |
| P6 isolated | no too-heavy pool row other than the lens itself within 3D distance ≤ 3.0 Mpc (the authors' `dist0p1perc` > 3) | `mass_range_selection.py` (`mask_iso`) |
| P7 lens sample | isolated, `masked` == 0, 0.1 < z < 0.5, 0 ≤ log M★ + 0.056 < 11 | `mass_range_selection.py`; `run_shearcode.py` sets `masslim` to `GL` (log M★ + 0.056) |

N = the count after P7.

## Labels (frozen)
Stage 1, on N:
- **REBUILD MATCHES**: |N / 259,383 − 1| ≤ 0.05.
- **REBUILD DOES NOT MATCH**: otherwise. Report N, the closest variant below, and which cut the miss traces to.
- **NOT EVALUABLE**: any of K1–K5 fails.

The 5 % line is NV2's frozen line and the lead's instruction. It is not derived from a measurement error. It is not widened after a result.

Stage 2 runs only on REBUILD MATCHES. Per footing, for the plain law, through LE1's G1 (A30 statistic) and G3 (CX1 lensing line):
- **GAP STANDS**: Z > +2 under both graders (the law short, as in LE1).
- **GAP CLOSES**: |Z| ≤ 2 under both.
- **GRADERS SPLIT**: anything else.
Also reported, not labelled: LE1's A1 mean offset (G1 model, G3 statistic), against LE1's +0.089 / +0.050 dex.

## Known-answer checks
- **K1 catalogue**: both sha256 values above; 1,239,422 rows; `ID` equal row by row.
- **K2 distance**: this lane's D_A equals astropy's for the cosmology in P5 to 1e-6 relative at z 0.05, 0.1, 0.25, 0.5 (an independent trapezoid integral against astropy).
- **K3 planted isolation**: a synthetic catalogue with planted neighbours (distances 2.95 / 3.05 Mpc, mass ratios 0.095 / 0.105, masses at bin centres) is classified exactly, 100 %.
- **K4 match quality**: over matched rows, median |MAG_AUTO_CALIB − (MAG_AUTO − EXTINCTION_r)| ≤ 0.10 mag, with the WL catalogue's own `MAG_AUTO` and `EXTINCTION_r`. If K4 fails, P3a is not trusted and the label is NOT EVALUABLE.
- **K5 reproduce the record**: with NV2's recipe (pool `masked` 0, r < 20, finite, z > 0, log M★ > 0; log M★ = MASS_BEST + 0.206; flat Ωm 0.3 comoving; NV2's own separation formula), this lane's code returns NV2's 486,584 exactly.
- **Rerun**: byte-identical JSON.

## MUTATE twin (must bite)
`FN4C_MUTATE=1`: the redshifts are shuffled among pool rows (fixed seed) before P5. Expected: N moves outside the 5 % window, so the twin cannot read REBUILD MATCHES, and exits 1. If it does not move N outside the window, that is a failed check, reported.

## Variants (diagnostic, declared now; reported beside the primary; never replace it; never tuned)
- V1 fs = 0 (MASS_BEST only).
- V2 fs = +0.15 for every row (NV2's stand-in).
- V3 pool restricted to `masked` == 0.
- V4 comoving distances D_C in place of D_A.
- V5 mass cut without the +0.056 (log M★ < 11).
- V6 unbinned threshold (M★,sat > 0.1 M★,lens).
- V7 only rows matched in P3a may be lenses (the fs stand-in carries no lens).

## Secondary comparisons with B21 Appendix A (reported, no line)
Isolated fraction among r < 17.5 (B21: 32.0 %) and r > 17.5 (36.8 %); isolated lenses with r < 17.5 (B21: about 3,800); log of the mean M★ for all candidates (10.77), the r < 17.5 candidates (10.78) and the isolated sample (10.61); log of the mean M_gal for the isolated sample (10.69), with M_gal = M★(1 + f_cold), log f_cold = −0.69 log M★ + 6.63. B21 does not state the denominators of its fractions; both readings (lens candidates; all pool rows) are reported.

## Stage 2 method (only on REBUILD MATCHES)
- LE1's G1 and G3 are copied with attribution; no grader is edited. The only change is the lens inventory: `logM` (P7's, with +0.056), `z`, and `WLENS`.
- WLENS is not recomputed from the shear catalogue (a 17.7 GB pass is not a short job). It is modelled from the June inventory: the median of WLENS / M_gal in cells of z (width 0.02, from 0.1) and log M_gal (width 0.1), times each rebuilt lens's own M_gal. A cell with fewer than 20 June lenses takes the median of WLENS / M_gal over its whole z cell. M_gal uses the same f_cold relation for both inventories.
- **K6**: the copied graders on the June inventory with its true WLENS reproduce LE1's law values exactly: G1 +9.27 / +6.52, G3 +5.01 / +3.32 (canonical / alt), to the printed digits.
- **K7**: the June inventory with modelled WLENS lands within |ΔZ| ≤ 0.20 of those values under both graders, on both footings. If K7 fails, Stage 2 reads NOT EVALUABLE.
- **MUTATE (Stage 2)**: lens masses ×2 (log M★ + 0.301). G1's law Z must move by more than 1.0 on both footings.

## Compute
One thread (`OMP_NUM_THREADS=1`), `nice`, `python3 -I`. The shear catalogue is read in row chunks of at most 200,000; RSS target under 1 GB. Caches and per-lens arrays go in a gitignored `cache/`; committed outputs carry no home paths.

## Outputs
`fn4c_rebuild.py`, `fn4c_rebuild.out`, `fn4c_rebuild.json`, `fn4c_rebuild_MUTATE.out/.json`; on a match `fn4c_grade.py` and its outputs; `README.md` with the label first, failed checks and departures.
