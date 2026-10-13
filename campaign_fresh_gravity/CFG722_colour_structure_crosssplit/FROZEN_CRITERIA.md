# CFG722 FROZEN CRITERIA: colour × structure cross-split of the KiDS early-type lensing excess

Date: 2026-10-13. Written and committed ALONE, while the KiDS DR4.1 structure columns were still downloading: before any match, any
structural statistic of our lenses, or any lensing number. Block CFG720–729. Nothing below may be edited after this commit.

Raw lensing only (owner's 10-10 rule); no ΛCDM ingredient; no law, κ or footing in any score. Not "theory closed". Nothing will be
phrased as "the data favour the framework".

## 0. What has been seen (stated before any choice below)

- CFG669: early types carry ×1.9 the lensing of late types at matched Ks baryonic mass (Z 3.4). CFG721: colour and Sérsic splits of
  B21's stacks are about equal (+0.22 / +0.18, difference 1σ); within colour a continuous trend is mildly preferred.
- Simard 2011 matches only 78 f30 lenses (unusable). The KiDS-1000 shear catalogue's lensfit `bulge_fraction` exists for 6,823 f30
  lenses (12%): early median 0.994, late median 0.027 (seen; no lensing computed with it).
- The download (owner-approved, ESO archive public catalogue `KiDS_DR4_1_ugriZYJHKs_cat_fits`, MAG_AUTO < 20, CLASS_STAR < 0.8,
  columns RA/Dec, KIDS_TILE, MAG_AUTO, FLUX_RADIUS, MU_MAX, KRON_RADIUS, FWHM_IMAGE, MAG_APER_4/8/14/20/30) was in progress when this
  file was written; a 50,000-row test fetch confirmed the columns only.
- **Author's expectation, before any score:** structure and colour are strongly correlated; the cross-split may have limited power in
  the minority cells (red-diffuse, blue-concentrated).

## 1. Structural index

- C = MAG_APER_4 − MAG_APER_14 (r band; 4 px = 0.8″ and 14 px = 2.8″ diameter). Larger C means more light at the centre.
- Seeing / tile correction: C_res = C − median(C) over all downloaded bright galaxies in the same KIDS_TILE and the same 0.5-mag
  MAG_AUTO bin. Reported robustness index: C2 = MAG_APER_8 − MAG_APER_20, corrected the same way.
- Lenses are matched to the download by position (< 1″).
- **Validation gate V1:** on the lenses that also have lensfit `bulge_fraction` (shear catalogue, saved match), the Spearman correlation
  between C_res and bulge_fraction must be ≥ 0.3. If not, C_res is not accepted as a structural proxy and the lane is VOID.

## 2. Cross-split

f30 lenses with C_res, u−r and Ks baryonic mass (CFG669's estimator, c_K, per-type f_cold). CFG585's head and CFG531's `esd_loo`,
executed unedited.
- Colour: red = TYP 1 (u−r > 2.0), blue = TYP 0. Structure: concentrated = C_res above the median of all f30 lenses in the same lens-z
  tercile; diffuse otherwise.
- Four cells RC, RD, BC, BD. Each cell is re-weighted (WG, WW scaled) so that its joint distribution over 10 deciles of log M_b,K × 3
  lens-z terciles matches the whole f30 sample's. Cells (or joint bins) with fewer than 50 lenses are dropped and reported.
- A_cell = log10(W·ΔΣ_cell / W·ΔΣ_all) over K9 (CFG700 weights), patch jackknife.
- Colour effect at fixed structure: Δ_col = ½[(A_RC − A_BC) + (A_RD − A_BD)]. Structure effect at fixed colour:
  Δ_str = ½[(A_RC − A_RD) + (A_BC − A_BD)]. Errors from the jackknife of the combinations.

**Classes:** **STRUCTURE CARRIES IT** if Δ_str/σ ≥ 2 and Δ_col/σ < 2; **COLOUR CARRIES IT** if Δ_col/σ ≥ 2 and Δ_str/σ < 2; **BOTH**
if both ≥ 2; **UNDECIDED** otherwise. Reported: the four A_cell with N, the interaction term, and the same with C2.

## 3. MUTATE (`CFG722_MUTATE=1 CFG722_M=M1|M2`, each exits 1 iff its tooth bites)

- M1: C_res shuffled within each colour × mass-decile × z-tercile bin → |Δ_str| < 2σ.
- M2: colour labels shuffled within each structure × mass-decile × z-tercile bin → |Δ_col| < 2σ.

## 4. Machine rules

Light: one process, `nice -n 10`; the download is read with astropy; allowed while the 1024³ run is live.
