# A6: what DESI and Euclid actually released, and which open rows of form B they can decide

2026-11-12. Scoping only: **nothing was downloaded** (directory indexes and paper pages were read). Every web fact is
PROVISIONAL and carries its URL. Form B = a0 = (1/2) c sqrt(G rho_DE), mu(x) = x/(1+x), cold dark energy at 5.41 x baryons,
counted once. Cold dark energy is a gravitating field component, never a particle.

**Prior work not repeated.** Branch `codex/euclid-desi-review-2026-11-12` (`research_closure_2026_11_12/euclid_desi_release_review/`)
already reviewed all 26 Euclid DR1-Foundation papers, audited the ECLIPSE strong-lens metadata (39 deflectors with DESI
redshifts; source-redshift links missing), and noted DESI's DR2 Lya AP update and the MW mass paper (used in DW1). This file
adds what that review did not do: a row-by-row map against form B's open rows, file sizes, and a ranking.

**Bottom line.** What dropped today is Euclid **DR1-Foundation** (images, MER photometry and morphology, photo-z, spectra,
strong-lens catalogue). It carries **no calibrated shear, no cluster catalogue and no galaxy-galaxy lensing**; those come with
full DR1 on 16 June 2027. DESI released no new survey data today: DR2 spectra are still unreleased. The newest DESI pieces
are papers (Lya AP, 30 July 2026; MW mass, 4 Nov 2026) and one DR1 value-added catalogue (BGS groups, files dated
Sep-Oct 2026). **None of these can change the forest fail or the dwarf NO POWER rows.** Two rows (groups, a0(z)) gain a usable
input; the lensing rows wait for Euclid shear (2027) and DESI DR2 spectra (early 2027, PROVISIONAL).

## 1. Releases

| release | date | coverage | data or papers | licence / policy | access | source (PROVISIONAL) |
|---|---|---|---|---|---|---|
| Euclid DR1-Foundation | 12 Nov 2026 | Wide ~1,900 deg2 (~500 N, ~1,400 S), observed 14 Feb 2024 - 21 May 2025, + Deep Fields | DATA: raw + calibrated VIS/NISP images, MER catalogues (photometry, morphology), PHZ photo-z + physical properties, SIR spectra + SPE redshifts, masks, randoms; ECLIPSE strong-lens catalogue; 26 papers | DR1 licence text not retrieved; acknowledgement + per-release DOI required. Q1 was CC BY-NC 3.0 IGO | ESA Euclid science archive / Euclid Data Space (primary), IRSA mirror | https://www.cosmos.esa.int/web/euclid/data-release-dr1 ; https://www.cosmos.esa.int/web/euclid/dr1-timeline ; https://euclid.caltech.edu/page/euclid-dr1 ; https://pubs.euclid-ec.org/public/ |
| Euclid DR1 (complete) | 16 Jun 2027 | same | higher-level clustering and weak-lensing products (shear catalogues not named explicitly) | as above | as above | https://www.cosmos.esa.int/web/euclid/data-release-dr1 |
| Euclid Q1 | Mar 2025 | 63 deg2 | DATA; a LensMC shear catalogue for cluster lensing is a June 2026 paper (arXiv:2606.20829); no public file found | CC BY-NC 3.0 IGO | ESA archive, IRSA | https://cosmos.esa.int/web/euclid/q1-data ; https://arxiv.org/abs/2606.20829 |
| DESI DR1 | 19 Mar 2025 | ~9,700 deg2 bright / ~9,500 dark; 18.7 M main-survey spectra | DATA (spectra, redshifts, LSS catalogues, VACs) | CC BY 4.0 + acknowledgement | https://data.desi.lbl.gov/public/dr1/ | https://data.desi.lbl.gov/doc/releases/dr1/ |
| DESI DR1 VAC "bgs-groups" v1.0 | file 21 Sep 2026, checksums 9 Oct 2026 | DR1 BGS footprint | DATA (galaxy group catalogue) | CC BY 4.0 (DR1) | https://data.desi.lbl.gov/public/dr1/vac/dr1/bgs-groups/v1.0/ | directory index, read 2026-11-12 |
| DESI DR2 | spectra NOT released ("by early 2027", PROVISIONAL) | 3 yr main survey | PAPERS + summary products only: BAO likelihoods and chains (19 Mar 2025), Lya full-shape AP (30 Jul 2026, arXiv:2607.27410), MW mass (4 Nov 2026, arXiv:2611.05518-21) | chains public | https://data.desi.lbl.gov/public/papers/y3/ | https://data.desi.lbl.gov/doc/papers/ ("The underlying spectra and redshifts for DR2 have not yet been released.") |
| DESI DR1 P1D | papers May 2025 (arXiv:2505.07974, 2505.09493); cosmology Jan 2026 (arXiv:2601.21432) | z 2.2-4.4 | PAPER + data vector (already on disk: FRZ1's 755 points, md5 33d7fc21...) | - | - | no DR2 P1D measurement found |
| DESI DR1 peculiar velocities | Dec 2025 (arXiv:2512.03226-30) | z < 0.1, ~98k FP + TF | PAPERS; catalogue hosting not confirmed | - | - | https://arxiv.org/abs/2512.03226 |
| DESI DR1 galaxy-galaxy lensing ("Lensing Without Borders") | 2025 (arXiv:2506.21677); cosmology Dec 2025 (arXiv:2512.15962) | BGS + LRG x KiDS/DES/HSC | DATA vectors, Zenodo 10.5281/zenodo.22914838 (already on disk, CFG315) | CC BY 4.0 | - | CFG315 MANIFEST |

## 2. Products against form B's open rows

On disk already (`../_external_data/`, relative to the repo root): DESI DR1 BGS_BRIGHT_full_HPmapcut (5.19 GB), DESI DR1
CIGALE (6.8 GB), LwB DESI DR1 GGL (46 MB tarball), DESI DR2 chains (320 MB), KiDS-1000 lensing (17 GB), KiDS-Legacy
cosmic-shear 2-point release (394 MB, no shear catalogue), ACT DR6 y (3.2 GB). **Free disk: 15 GiB** (df, 2026-11-12).

| row (lane) | product | test in one or two sentences | can it move the verdict? direction of power | files and size | published table enough? |
|---|---|---|---|---|---|
| Forest, FAILS (FRZ1, FRZ1R) | none new. DR2 P1D not released | - | **No.** The fail is ~2,000 x the gate (Delta chi^2 8,142-9,916 vs 4) and comes from form B's own layout at z 3; better data only sharpens it | - | - |
| Lensing amplitude, ~2 widths (KL1, BX1) | Euclid DR1 shear | Re-run KL1 Part C's gate on a fourth, independent survey | **Yes, both ways**, but not before 16 Jun 2027 | not released | no |
| same | DESI DR1 LwB GGL + Lange+ S8 0.794 +- 0.023 (DES+KiDS, arXiv:2512.15962) | Predict form B's Delta Sigma for BGS/LRG at its own sigma8 0.812 and grade the large-scale amplitude | Weak to moderate: an independent lens sample with the same source surveys, so not independent of KiDS/DES shear systematics. Lange's S8 is a LCDM-model inference: use the data vectors, not the number | on disk (46 MB) | only as a cross-check; grade on the data vectors |
| same (growth) | DESI DR1 PV f sigma8 = 0.450 +- 0.055 (z ~ 0.07, arXiv:2512.03229) | Compare form B's f sigma8 at z 0.07 | **Low power**: a 12 % width against a ~3 % sigma8 gap | none (published number) | yes |
| GGL by type / isolated lenses, NO VERDICT (KO2, PD1, SRH1) | DESI DR1 spec-z isolation | Re-select isolated lenses with spectroscopic neighbours | **No with DR1**: CFG316 found the frozen spec-isolated sample on KiDS-1000 x DESI DR1 **empty** (fibre incompleteness). Needs DESI DR2 spectra (early 2027) | on disk | no |
| same | Euclid DR1-Foundation MER morphology + PHZ stellar masses | Re-type lenses morphologically (not by colour) for the KO2 split; independent M* | Low: KO2's NO VERDICT came from one cross-shear amplitude, not from typing. SRH1's fail (+2.16 sigma vs 2) is near its line, so typing could move it either way | TAP column query on the KiDS/Euclid overlap; **size UNCONFIRMED** (Q1's catalogue subset was 564 GB for 63 deg2 on the China-VO mirror; a column/area query is MB-GB scale) | no |
| Groups R500 to r_ta, NOT EVALUABLE (GO1) | **DESI DR1 bgs-groups v1.0** | Stack KiDS-1000 shear and ACT y around DESI spectroscopic groups, selecting groups with no comparable neighbour inside ~10 Mpc, and locate r_ta (mean density 5.55 rho_m) | **Yes, either way, if isolation works.** GO1's stack never fell to 5.55 rho_m inside 16 R500 because neighbours keep it at ~17 rho_m; a spectroscopic group catalogue allows the isolation cut that eRASS1 selection lacked. Pass: f_ret(<r_ta) = 1 within errors; fail: retained baryons + cold dark energy do not add to 5.41 x baryons at r_ta | `bgs-groups-dr1-v1.0.fits` 289,877,760 B + sha256 file 1,773 B. The 18 randoms (~3.29 GB each, 59 GB) are **not** needed for a stacked lensing profile | no |
| Clusters beyond R500 non-hydrostatic (XCV1) | DESI DR1 BGS redshifts (on disk) | Own caustic masses with DESI members and X-COP X-ray centres (fixes KA-3's A85 centre offset) for X-COP clusters in the DESI footprint | Low: caustic per-cluster scatter (~40 %) is method-intrinsic, not sample-size. Can turn NO VERDICT into the A1 reading, not decide the ceiling | on disk | no |
| | Euclid cluster catalogue / shear | Weak-lensing masses beyond R500 | Yes, both ways, **2027** | not released | - |
| Flat a0(z) to z 2.33; DE evolution | **DESI DR2 Lya AP** (arXiv:2607.27410: D_M/r_d 39.32 +- 0.33, D_H/r_d 8.600 +- 0.066, r 0.225 at z 2.33) | Replace CFG681's older z 2.33 pair, refit rho_DE(z) with the DR2 BAO set and read a0(z)/a0(0) = sqrt(rho_DE(z)/rho_DE(0)) at z 2.33 | Moderate, both ways: tightens the z 2.33 point by ~40 % in each distance. **Conditional** on an expansion model and early-universe priors; BAO alone does not measure rho_DE. Must **replace**, not add to, the overlapping pair | none (paper table); DR2 chains on disk | **yes** |
| Ultra-faint + M31 dwarfs, NO POWER (DSB1) | Euclid DR1-Foundation LSB systems (Gatto) | - | **No.** Neither release has resolved stellar kinematics for these classes | - | - |

## 3. Top five, ranked by decisiveness per GB and per day

1. **a0(z) at z 2.33 from DESI DR2 Lya AP** (0 GB, ~1 day; published table + chains on disk). Pass: the refit rho_DE(z)
   keeps a0(2.33)/a0(0) inside the kill test's band, so the flat-a0 rule survives with a tighter high-z anchor. Fail: the
   update requires rho_DE evolution large enough that a0 must move beyond the kill band; then the a0-rho_DE tie and the
   flat-a0 rule cannot both hold. Caveat: conditional on the expansion model; does not separate form B from LCDM.
2. **GO1 re-run on DESI DR1 BGS groups with a spectroscopic isolation cut** (0.29 GB, 3-5 days; KiDS-1000 shear and ACT y
   on disk). Pass: r_ta located and f_ret(<r_ta) = 1 within errors, form B's counted-once census closes for groups. Fail:
   the census at r_ta falls short or overshoots by more than its errors, a direct fail of "counted once" on group scales.
   Third outcome: r_ta still not reached, NOT EVALUABLE again (then only Euclid 2027 depth helps).
3. **Lensing amplitude cross-check on DESI DR1 LwB data vectors** (0 GB, 2-3 days). Pass: form B's sigma8 0.812 fits the
   BGS/LRG Delta Sigma amplitude within 2 widths, so the KiDS-Legacy gap looks survey-specific. Fail: the same gap appears
   in an independent lens sample, which strengthens KL1's reading against form B. Shares source shear with KiDS/DES.
4. **XCV1 re-centred caustic masses from DESI DR1 BGS** (0 GB, 2-3 days). Pass: f_ret falls to <= 1 at R200 with the
   centre fixed. Fail: f_ret stays > 1, item 6's ceiling problem confirmed without hydrostatic equilibrium. Expected
   outcome by power: still AT THE CEILING (interval too wide). Note the ceiling is the cosmic baryon fraction, not B's alone.
5. **DESI DR1 PV f sigma8** (0 GB, 0.5 day). Pass: form B's f sigma8(z 0.07) inside 0.450 +- 0.055. Fail: outside it,
   an independent low-z growth fail. Low power against the 3 % sigma8 gap; ranked last for that reason.

Not ranked because not runnable now: Euclid DR1 shear (16 Jun 2027) is the single most decisive future product for the
lensing-amplitude, GGL-by-type and cluster rows; DESI DR2 spectra (early 2027) are needed for spec-isolated lenses.

## 4. Needs the owner's go

| proposed download | source URL | size | licence |
|---|---|---|---|
| DESI DR1 BGS group catalogue `bgs-groups-dr1-v1.0.fits` + `dr1_vac_dr1_bgs-groups_v1.0.sha256sum` (test 2) | https://data.desi.lbl.gov/public/dr1/vac/dr1/bgs-groups/v1.0/ (docs: https://data.desi.lbl.gov/doc/releases/dr1/vac/bgs-groups/) | 289,877,760 B + 1,773 B | CC BY 4.0 + DESI acknowledgement |
| arXiv:2607.27410 PDF/HTML for the z 2.33 table (test 1) | https://arxiv.org/abs/2607.27410 | ~1-5 MB | arXiv licence |
| arXiv:2512.03229 / 2512.03226 PDF for the f sigma8 value and footprint (test 5) | https://arxiv.org/abs/2512.03229 | ~5 MB | arXiv licence |
| Optional, later: Euclid DR1-Foundation MER + PHZ columns on the KiDS overlap via TAP | ESA Euclid archive (https://www.cosmos.esa.int/web/euclid/data-release-dr1) | UNCONFIRMED; cap the query at 5 GB (15 GiB free) | DR1 terms not retrieved (Q1 was CC BY-NC 3.0 IGO) |

Not proposed: the 18 BGS group randoms (59 GB) and any Euclid image partition (exceeds free disk; not needed).

Could not confirm: Euclid DR1 licence text and data volumes; whether the Q1 LensMC shear catalogue is public; a hosting
location for the DESI DR1 PV catalogues; any DESI DR2 P1D measurement; the exact DESI DR2 data-release date.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
