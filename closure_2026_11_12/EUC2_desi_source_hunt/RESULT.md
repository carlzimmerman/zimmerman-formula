# EUC2 (DESI SOURCE HUNT): RESULT

2026-11-12. Criteria 364e9d08c9 (alone, before any script or lens spectrum). Amendment A1 a24ffd2dc2 (post hoc,
disclosed, before the amended code).

**Status: FINAL.** The paced search of all 6,104 extension positions finished. It added one spectrum on one lens: the
catalogue's `desi_deflector_specz` flag already marked essentially every Euclid lens DESI DR1 observed. Final set: 383
spectra on 370 lenses. Both searches were rerun on it and give the same detections and the same failed nulls as the
first pass (sections 1 and 2; the first-pass outputs are kept under `firstpass/`). The frozen mutation twin
(`EUC2_MUTATE=fakesep`) exits 2, not 1: the wrong-separation search finds 11 "doublets", 27 % of the real search's 41,
above its 20 % line. That is the same purity defect H2 reports, seen from the other side.

## Verdict: NOT EVALUABLE as frozen. NOT EVALUABLE under A1. EUC1-F stays open.

The automatic search fails its own purity null in both forms. No population reading is made. What the public DESI
spectra do give is **four lens–source pairs confirmed by a second line of evidence**, one of which has usable catalogue
inputs. That lens needs 1.70 × (canonical) / 1.64 × (alt) its Salpeter stellar mass under law S at its true source
redshift.

κ = ½ FITTED. No outcome favours the framework.

## 1. The frozen search (flagged spectra)

| Check | Result |
|---|---|
| H1 injection, S = 10 | 191 / 200 recovered (pass) |
| **H2 fake-separation null** | **10 clusters against a limit of 8.2 (FAIL)**; sign-flipped null 108 clusters |
| H3 redshift join | 363 / 369 (pass) |
| H4 known pair EUCL-DR1-L015763 | z_s = 1.3658 against the published 1.366 ± 0.008 (pass) |
| H5 yield by grade A / B / C | 13 / 5 / 5 beside the paper's by-eye 12 / 5 / 3 |

33 spectra carried a "secure" detection; 23 lenses kept one redshift; 9 were excluded for conflicting redshifts. The
plots show the failure the null reports: single narrow spikes lying between the two expected [O II] positions, and
broad bumps, pass a rule that only tests two amplitudes at two wavelengths. The agreement of the yield with the paper's
count is therefore partly coincidence. **Word: NOT EVALUABLE.**

## 2. The amended search, A1 (doublet must beat the best single line by Δχ² ≥ 4)

41 frozen SECURE-D clusters → 8 kept, on 8 lenses, none conflicting.

| Check | Result |
|---|---|
| **H2 at 4.50 Å** | **3 against a limit of 1.6 (FAIL)**; at 1.80 / 4.00 / 5.20 Å: 3 / 3 / 5 |
| H1 at S = 10 / S = 14 | 137 / 200 and 184 / 200 (reported; the shape test costs completeness) |
| H3 | 363 / 369 (pass) |
| H4 | z_s = 1.3657 (pass) |

**Null audit.** Of the 14 fake-separation hits across the four separations, 10 are independent artefacts and 4 sit on a
detection of the real search. One artefact (EUCL-DR1-L001768) reaches Δχ² ≈ 44 at every separation: an irregular
two-peaked feature that prefers "a doublet" of any spacing. So the expected false count per search is 2–3 against 8
found. **Word: NOT EVALUABLE.**

**By eye, all 8 (plots in `firstpass/a1_00.png`):**

| Lens | Grade | z_l | z_s | S_OII | Δχ² | Judgement |
|---|---|---|---|---|---|---|
| EUCL-DR1-L006816 | C | 0.2582 | 0.4685 | 9.4 | 17.2 | real: [O III] 5008 at 15.8, Hα 6.3, Hβ 4.7 |
| EUCL-DR1-L014688 | A | 0.5221 | 0.9926 | 10.3 | 48.7 | real: both components at the marks, Hβ 6.3 |
| EUCL-DR1-L012826 | A | 0.6352 | 1.1374 | 19.0 | 31.9 | real: clean resolved doublet |
| EUCL-DR1-L013516 | A | 0.3064 | 1.1496 | 8.5 | 8.3 | plausible, not confirmed |
| EUCL-DR1-L017819 | A | 0.3202 | 1.2113 | 7.1 | 7.7 | marginal; a similar bump sits 25 Å away |
| EUCL-DR1-L015763 | A | 0.2350 | 1.3657 | 40.7 | 99.5 | real: textbook doublet; published z_s 1.366 |
| EUCL-DR1-L008609 | A | 0.3828 | 1.5349 | 7.4 | 5.3 | **artefact**: a sky-line residual at 9441–9443 Å beside the marks |
| EUCL-DR1-L009480 | C | 0.0598 | 1.6225 | 8.4 | 8.8 | noise at the red end |

Three of eight are artefacts or noise, as the null predicted. EUCL-DR1-L008609 is the only detection inside sample P,
so the sample-P reading the script prints (N = 1) rests on an artefact and is void.

## 3. What survives: four pairs with a second line of evidence

Not an automatic class. Each is a frozen-threshold [O II] detection plus independent support.

| Lens | Grade | z_l (DESI) | z_s | Second evidence | Catalogue inputs |
|---|---|---|---|---|---|
| EUCL-DR1-L015763 (PS1J1821+7130) | A | 0.2350 | 1.3657 | published Euclid NISP redshift | usable; model success; fails the detection-quality cut |
| EUCL-DR1-L012826 | A | 0.6352 | 1.1374 | S_OII = 19, resolved doublet | no SED fit (fewer than 6 bands): no stellar mass |
| EUCL-DR1-L014688 | A | 0.5221 | 0.9926 | Hβ | no SED fit (fewer than 6 bands): no stellar mass |
| EUCL-DR1-L006816 | C | 0.2582 | 0.4685 | [O III], Hα, Hβ | grade C: not in the physical-property catalogue |

**The one usable lens.** EUCL-DR1-L015763: θ_E = 1.51″, θ_E/θ_e = 0.56, n = 6.0, log M★ = 11.56 at the DESI deflector
redshift. Law S at the true source redshift: **b = +0.231 (canonical) / +0.215 (alt)**, i.e. 1.70 × / 1.64 × Salpeter.
Its source-free value was +0.112 (alt). It is one lens, wide-separation, outside the quality-cut sample. It is not a
gate and not a population statement. It does sit where EUC1's map put its class (θ_E 1.3–1.7″: median source-free b
+0.15).

## 4. What this says

1. **The public DESI fibre spectra cannot settle EUC1-F.** A 1.5″ fibre on the lens galaxy catches little arc light;
   most sources are above z = 1.63 or too faint; and the pairs that are real mostly fall outside the quality-cut
   sample or have no stellar mass. N(P) with a trustworthy source redshift is zero.
2. **An automatic [O II] search at S ≈ 7–9 in the sky-line forest is artefact-limited.** Both nulls said so before the
   plots did. A usable automatic class needs S ≳ 10 or a second line; that yields about four systems here.
3. **Nothing here changes EUC1.** The lane verdict there stays NO VERDICT / NO VERDICT, with the break redshift at
   3.6–4.3.
4. **Where the source redshifts are.** Euclid's own DR1 grism redshift and line tables are public (IRSA:
   `euclid_dr1_spectro_z_spe_galaxy_candidates_wide_survey`, `..._spe_line_features_wide_survey`, `..._spe_quality_...`).
   A lensed source's Hα falls in the red grism for 0.84 < z_s < 1.88, where lensed sources usually sit, and the arcs
   are in the extraction. Three of the four pairs above (z_s = 0.9926, 1.1374, 1.3657) lie in that window and are a
   ready truth set for such a search. That is the next lane (EUC3), not run here.

## 5. Files

`euc2_fetch.py` (paced, obeys the service's rate limit), `euc2_matches.csv` (383 spectra), `euc2.py` (frozen search and
reading) with `euc2.out`, `euc2_results.json`, `euc2_sources.csv`, `euc2_MUTATE_fakesep.*` (exit 2), `figs/`;
`euc2_a1.py` (amended search) with `euc2_a1.out`, `euc2_a1_results.json`, `euc2_a1_sources.csv`, `figs_a1/`;
`firstpass/` (outputs, match table and plots of the flagged-spectra pass, preserved as seen). On the final set A1's
injection recovery at S = 10 is 131 / 200 (137 / 200 on the first pass; the random draws differ).

**Follow-on lanes.** EUC3 (Euclid's own grism redshifts) was started on these four pairs as its truth set. EUC5 fitted
stellar velocity dispersions to the same DESI spectra.
Spectra are outside git (`_external_data/euclid_dr1_eclipse/desi_spectra/`, NOIRLab SPARCL, DESI-DR1, anonymous).

One code fix between the first pass and any later run: the plot overlay of the fitted doublet (no number affected).
