# MUSE-DARK public catalogues (UDF release, 127 muse_ids) joined and checked

Built 2026-09-29 by `build.py` on the owner's go ("yes, fetch the MUSE-DARK catalogues"). Nine text files (252,000 bytes in all) fetched from https://dark-matter.osu-lyon.fr/data/catalogues/ (sizes from HEAD requests before the fetch), kept outside the repo in `~/new_physics/_external_data/muse_dark/`, sha256 in `manifest.json`.
The site ties the release to MUSE-DARK-I (arXiv:2506.19721) and III (arXiv:2604.22613). **No README ships with the files**, so column units and definitions beyond the header names are not stated by the source; anything I say about them is marked. No acceleration, a₀ or verdict is computed. Data only.

## Files
`musedark_joined.csv` (127 rows, one per `muse_id`): photometric `z`, `r_kpc`, `incl`, `PA`, `logMstar_phot` (+err), `SFR`; baryons-only fit `baryons_only_logMdisk`, `baryons_only_logMgas` (+errors); per halo family (`DC14`, `NFW`, `cNFW`, `Einasto`, `DZ`, `Burkert`) `_logMvir`, `_virial_velocity`, `_rs_kpc`, `_BIC`; `baryons_only_BIC`; `DC14_logX`; `issues`. `duplicated_rows.json` (the two rows the DC14 file gives for id 26), `checks.txt`, `manifest.json`.

## What the catalogue contains, against the three deciding items the calc thread named
1. **Fitted vs photometric stellar mass: PARTLY.** The photometric log M* (from the SED catalogue) is there. The fitted `log_Mdisk` and `log_Mgas` exist ONLY in `baryons_only_bestfit.txt`, i.e. the fit with no dark-matter halo. **The per-family halo files (including DC14, the one MUSE-DARK-III uses) carry only halo parameters, not the disc and gas masses of the disc–halo fit**, so the M* that entered III's accelerations is NOT in these catalogues. (The site says per-galaxy folders hold `RC_decomp` and `galpak_run_DC14`; I did not open them.)
2. **a₀ or accelerations across halo families: NO.** There is no a₀, no g_bar or g_tot column in any file; only halo parameters and fit statistics per family.
3. **Baryons-only fit: YES.** `baryons_only_bestfit.txt` (126 ids) plus `BIC_baryons-only` and related columns in `Fit_statistics_all_models.txt`.

## What the tables show (descriptive; definitions unverified because no README)
- 127 distinct ids in five halo files; the DC14 file **lacks id 36 and has id 26 twice** with two different rows (I assigned neither); `baryons_only` lacks id 69; `Fit_statistics` lacks id 36 (126 rows). The photometry file has 251 rows; two of the 127 sample ids (1371, 6314) have blank `z` and `Mstar`. The release page says 126 galaxies; the files hold 127.
- z 0.28–1.44 (median 0.89); photometric log M* 7.33–10.99 (median 9.24). MUSE-DARK-III's 79-galaxy subset uses M* > 10^8.8, 0.33 < z < 1.44 and "regular" galaxies; 89 of these ids pass the mass and redshift cuts alone (the "regular" flag is not in the files).
- **Baryons-only fitted `log_Mdisk` minus photometric `log M*`: median +0.77 dex (16–84%: +0.22 to +1.23), > 0.5 dex for 101 of 124 galaxies and > +1 dex for 41.** This is the disc mass a fit with NO halo needs to reproduce the rotation curve, so it measures how much dark-matter-like mass a baryons-only model absorbs; it says nothing about the DC14 fit's own M*. The baryons-only `log_Mgas` is likewise +0.77 dex (median) above the photometric M* (range −0.44 to +2.07).
- Fit quality (BIC per family; `BIC_*` columns of the statistics file): the best-BIC halo family is DZ for 36 galaxies, Burkert 35, DC14 20, cNFW 18, NFW 12, Einasto 5 (126 galaxies with a complete set), so no family dominates. **The baryons-only BIC is within 10 of the best halo family's BIC for 66 of 126 galaxies** (median difference 8.8, minimum −65.4 i.e. baryons-only preferred, maximum 2.3 × 10⁵), so for about half the galaxies a model with no halo and a freely fitted disc mass fits about as well as any halo (if `BIC_baryons-only` is defined on the same data points as the halo BICs, which the files do not state; the statistics file also has `BICr`, `Nr` and `Ndegree_r` columns for baryons-only whose meaning is not documented).
- The halo virial mass spreads by a median 1.14 dex across the six families for the same galaxy (max 3.87), i.e. the halo parameters are strongly family-dependent.

## Limits
Column definitions not documented; the duplicated and missing ids are the source's, not mine; nothing here reproduces III's a_bar or a_tot.
