# FN3_musedark_law_refit: NOT DECIDABLE WITH THE EXISTING CUBES. With HI unmeasured, the refit can't tell the survey's a0 rise from the band: a planted rise of the survey's size grades BAND CONSISTENT. Waits on HI at z ~ 1, or a different tracer

kappa = 1/2 FITTED. Not theory closed. Nothing here says the data favour the framework. No cold component, no particle.

Criteria `FROZEN_CRITERIA.md` (c6640225c2), committed alone first. `AMENDMENT_A1.md` (after K1). `AMENDMENT_A2.md` (after K2, before any real data). No real cube byte has been read.

**Labels so far.**
- **Stage 0 forecast: NOT EVALUABLE** (K1 failed as frozen).
- **Stage 1 as frozen: NO VERDICT** (K2a failed as frozen), whatever the cubes show.
- **Stage 1 under A2: no label either** (K2' failed: section 4).
- **Lane verdict: NOT DECIDABLE WITH THE EXISTING CUBES.** No cutout should be fetched for a graded run. The named PAPER67 test waits on an independent HI mass at z ~ 0.3-1.4 for these galaxies, or on a kinematic tracer that reaches past where HI dominates.

## 1. What the lane asks
PAPER67 names this test and says it wasn't run: refit MUSE-DARK with the law imposed and a stated baryon-mass budget; if a0(z ~ 1) stays well above the band with mass systematics under control, the band fails. Flat against a0 proportional to H(z) is not decidable here by design (AT1's 0.055 dex floor against a 0.20 dex SED scale).

## 2. Stage 0 record (on disk; no download)
| check | result | file |
|---|---|---|
| K0 hashes | 891 files, 0 failures: PASS | `fn3_k1.out` |
| sample | primary 71 disc-only galaxies passing III's file-present cuts (log Z < 15000 included); thirds 23/24/24 at median z 0.667, 1.021, 1.301; secondary 74 | `fn3_sample.json` |
| engine known answers | thin MGE vs Freeman 1970 within 0.03 %; spherical limit exact; DC14 rebuilt matches the released alpha, beta, gamma, r_s, R_vir, M_vir (rho_s within 0.3 % for ID0003, ID0011) | session check, `fn3_common.py` |
| K1 (frozen) | **FAIL**: no listed convention reproduces the released curves (best 1.4 % of galaxies within 3 %) | `fn3_k1.out` |
| K1b (A1, diagnostic) | the survey's model, slit-extracted through the thick disc, still misses (median rms 0.375) | `fn3_k1b.out` |
| K1c (A1, diagnostic) | the released v_perp and sigma can't pin the drift form (full forms miss v22 by +10 to +13 % in median, ~80-point spread) | `fn3_k1c_drift.out` |
| budget | sigma_cm 0.206 / 0.221 / 0.229 dex canonical (0.206 / 0.221 / 0.232 alt); L_band -1.0 to -1.4; L_H2 -0.32 to -0.68; slope sigma_s,sys 0.107 per unit z; median gN/a0 0.15-0.26 | `fn3_budget.out`, `budget.json` |
| K2 (frozen) | **K2a FAIL** 0.177 dex per galaxy against 0.05; K2b PASS (+0.30 recovered +0.282); bias -0.055; MUTATE PASS (-0.289, bites) | `fn3_k2.out` |
| enclosed baryons | 0.11-0.12 dex per galaxy at 1.5-2.5 R_e, better than stars, not 0.05 | `fn3_k2_enclosed.out` |

**What K1's failure means.** The released curves can't be rebuilt from the released per-parameter medians with this engine, even slit-extracted. The likeliest reason is the V_vir, concentration and X degeneracy: those medians don't make the median curve. So the only engine check against the survey that counts is K3 on real cutouts, which compares two fits to the same data.

**What K2's failure means.** At matched-filter S/N 30 the stellar mass trades against the free HI surface density and the inclination box. Every fit reaches chi2_red near 1.0, so this is a real degeneracy, not a fitter fault. Per galaxy, the law fixes the baryons inside the data better than it fixes the stars.

## 3. Stage 1: built and tested, not requested
- **Code, tested before any data:** `fn3_cutout.py` reads one galaxy's box through byte ranges (selftest: byte-identical to astropy slicing; continuum recovered to 1e-6). `fn3_stage1.py` runs K3, the law fits per footing and reading, the context laws and MUTATE (plumbing selftest PASS). `fn3_grade.py` turns results into the frozen labels. `fn3_fetch.py --approved` does the fetch.
- **Download, NOT requested,** because section 4 shows no graded label is possible. Kept for the record, in case an HI constraint makes the test decidable later (it would need the owner's yes): byte-range cutouts from `DATACUBE_UDF-10.fits` (3,062,799,360 B), `DATACUBE_MXDF.fits` (6,575,771,520 B) and `DATACUBE_UDF-MOSAIC.fits` (26,353,494,720 B), plus `UDF_HUDF_Catalogs_FULL.tar.gz` (9,122,619 B), all at `https://amused.univ-lyon1.fr/data/UDF/HUDF/download/`. About 0.98 GB transferred by full-row range reads; 30 MB kept, outside the repo. The full cubes are never stored (`fn3_fetch_plan.out`).
- **Compute:** about 74 galaxies x 20 fits x ~10 s, roughly 4 hours on one thread, checkpointed.

## 4. K2' (A2), fresh synthetics, and the grader's dry run
71 templates, new seeds, planted Sigma_HI uniform in [0, 15], matched-filter S/N 30 (`fn3_k2p.out`, `fn3_k2p.json`, `fn3_k2p.jsonl`).

| A2 line | result | line | reading |
|---|---|---|---|
| (a) median bias, thirds 0 / 1 / 2 | +0.048 / -0.115 / -0.020 | 0.07 | third 1 **FAILS** |
| (b) flat truth, recovered slope | -0.167 per unit z | 0 +- 0.10 | **FAIL** |
| (c) planted rise 0.60 per unit z, recovered | +0.320 | 0.60 +- 0.10 | **FAIL** |
| (d) MUTATE a0 x 2 | -0.316 | -0.30 +- 0.07 | PASS, bites |

Per-galaxy scatter (flat) runs from -0.975 to +0.258 dex (16-84 %). The free HI soaks up about half of a real mass trend with redshift and adds a -0.17 per unit z bias. The first run crashed at its last `json.dump` on a numpy boolean, after writing `fn3_k2p.out`; the rerun from the saved fits reproduced that file byte for byte.

**The decisive row: the grader's dry run** (`fn3_grade_DRYRUN.out`). On the same synthetics, the frozen labels read:
| planted truth | canonical | alt | slope |
|---|---|---|---|
| band (flat) | BAND CONSISTENT | BAND CONSISTENT | -0.167 +- 0.179 |
| the survey's rise against the band | **BAND CONSISTENT** | **BAND CONSISTENT** | +0.320 +- 0.204, 1.6 sigma |

So with HI free over its prior, the test would accept the band even if the survey's rise were real. The level test drowns in the 0.21-0.23 dex SED scale, and the slope, which was the strong statistic on paper, is halved by the HI trade.

**No subset of the existing public cubes rescues it.** The deep MXDF field (141 h) holds 12 of the 74 galaxies (`fn3_fetch_plan.out`), below the frozen 12 valid fits per third.

**What would decide it** (named, not available on disk): an HI mass, even a stacked one per redshift bin, for galaxies like these at z 0.3-1.4; or a tracer reaching past where a constant-Sigma HI disc dominates. Short of that, the dated test of the dark-energy tie stays CFG689 P6: one clean deep-MOND a0 point at z ~ 2.5 to about 0.10 dex.

## 4b. What this doesn't say
It doesn't say the survey's rise is wrong, or that the band holds. It says these cubes, at this S/N and with HI unmeasured, can't tell them apart under the law. The record's earlier finding stands beside it: the rise travels with the DC14-fitted masses (CFG198, CFG262).

## 5. Commit note
Commit 93b4235c4b, titled for the outside-summary draft, also carries this lane's K2 outputs and `AMENDMENT_A2.md` (`fn3_k2.*`, `fn3_k2_enclosed.*`). They were staged here and swept into another helper's commit through the shared index. Nothing was rewritten.
