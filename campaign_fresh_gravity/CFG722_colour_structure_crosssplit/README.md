# CFG722: colour × structure cross-split — VOID as frozen; underpowered when corrected

**Label as frozen: VOID (gate V1 fails).** Two defects in the frozen design, found after the run and disclosed below; the post-hoc,
sign-corrected numbers are UNDECIDED and underpowered. The early-type lensing excess still cannot be attributed to colour or structure.

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (d3a4df1e1), 2026-10-13, during the download. Block CFG720–729.
- **Data:** owner-approved ESO download of KiDS DR4.1 structure columns (1,544,973 galaxies with MAG_AUTO < 20, CLASS_STAR < 0.8;
  `_external_data/kids_dr4_structure/`, README there). 162,353 of 181,477 lenses matched (< 1″).
- **Script:** `cfg722.py` → `cfg722.out`, `cfg722_results.json`. MUTATE not run (the lane is VOID at its gate).

## Defects (disclosed 2026-10-13, after the run; the frozen text is not edited)

1. **Sign error in the structural index.** The criteria define C = MAG_APER_4 − MAG_APER_14 and say "larger C means more light at the
   centre". That is backwards: a centrally concentrated galaxy has its small-aperture magnitude closer to the large-aperture one, so
   C is *smaller*. The frozen label "concentrated = C_res above the median" therefore selects the **diffuse** half. The cell counts
   confirm it (frozen "RD" = red with C_res below median = 19,185 red lenses; frozen "BC" = blue with C_res above median = 20,678 blue
   lenses): with the sign corrected, red lenses are mostly concentrated and blue mostly diffuse, as expected.
2. **The validation gate V1 cannot be evaluated.** The lenses that have lensfit `bulge_fraction` (16,465, from the KiDS-1000 shear
   catalogue) and the lenses matched in the DR4.1 download (162,353) overlap in **1** lens: the two catalogues pick almost disjoint
   subsets of the bright sample. V1 (Spearman ≥ 0.3 on that overlap) is therefore not computable; by the frozen rule the lane is VOID.

## As-run numbers (frozen labels), and the sign-corrected reading (post hoc, no verdict weight)

| frozen cell | true meaning (sign-corrected) | N | A (K9, vs whole f30) |
|---|---|---|---|
| RC | red, diffuse | 3,792 | −0.084 ± 0.137 |
| RD | red, concentrated | 19,185 | +0.091 ± 0.037 |
| BC | blue, diffuse | 20,678 | −0.185 ± 0.113 |
| BD | blue, concentrated | 5,273 | −0.145 ± 0.160 |

- Colour at fixed structure (unchanged by the label swap): **Δ_col = +0.168 ± 0.124 (Z 1.4)**.
- Structure at fixed colour, sign-corrected (concentrated − diffuse): **Δ_str = +0.107 ± 0.132 (Z 0.8)**.
- Robustness index C2 = MAG_APER_8 − MAG_APER_20, sign-corrected: Δ_col +0.115 ± 0.117, Δ_str +0.189 ± 0.119 (Z 1.0 / 1.6).

## Reading

- With ground-based aperture concentration, the cross-split is **underpowered**: the minority cells (red-diffuse ~3.8k, blue-concentrated
  ~5.3k lenses) limit each effect to about ±0.12 dex, against expected effects of ~0.1–0.2. Neither colour nor structure reaches 2σ at
  fixed other; both point positive.
- The question "is the early-type excess carried by colour or by structure?" remains open. CFG721's B21 comparison (colour +0.22 vs Sérsic
  +0.18 at the same g_bar) is still the best constraint: the two are comparable.
- A valid re-test would need: the sign-correct definition frozen in advance, a validation of the concentration index on a subset that
  actually overlaps the download (for example against the bright sample's own morphology if it becomes available), and more lenses in
  the minority cells (KiDS-Legacy / DR5).
