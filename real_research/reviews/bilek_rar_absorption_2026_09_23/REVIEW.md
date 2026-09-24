# Bilek, Renaud & Samurovic 2026 -- Absorption + ZD Door Wave

**arXiv:2603.23591** "Deviations from the radial acceleration relation in the
central galaxies of clusters, subclusters, and groups" (A&A, submitted
2026-03-24).  Absorbed 2026-09-23 as `real_research/reviews/bilek_rar_absorption_2026_09_23/`.

**Wave lanes (all exit 0, all PASS, results JSON beside each .out):**

| Lane | Content | Verdict |
|---|---|---|
| BIL_absorption | transcription audit of Table 1 + Appendix A.1 (17 galaxies x 3 Jeans models), Virgo A+B+C = 6.3e14 identity, physicalness census, regime table | **8/8 PASS** |
| B01_ambient_response | Virgo subcluster quartet: fitted halo at r_max vs the zero-parameter ambient a0-line response (sibling fields at the paper's own 1-Mpc separations, both footings) | **10/10 PASS** -- kill (>=2/4 out of [0.1,10] on both footings) NOT reached; 1 armed challenge (NGC4472, x2.4 maximal envelope) |
| B02_isolated_cap | ZD01 dark cap a0/2 against ambient-free Jeans fits (NGC0821/2768/3115/1023, 12 rows, physicality-classed) | **3/3 PASS** -- weak contact; 1 armed challenge (NGC3115 neg-model 1.28e-10 = 2.3x cap on K1) |
| B03_strip_census | framework strip map (r_strip = 4 sigma^2/a0, ZD06/ZD09) vs the paper's own 17-row RAR split | **4/4 PASS** -- 15/15 decidable rows match, zero free parameters; 2 armed rows (NGC1400, NGC4526) |

## 1. Regime table (the paper's own fits, their r_max bins, m/s^2)

Printed in `BIL_absorption.out`.  Headline rows (median over models):

| galaxy | class | g_halo(r_max) | /a0 (K1) |
|---|---|---|---|
| NGC1023 | virtually isolated | 2.0e-12 | 0.02 |
| NGC3377 | noncentral Leo I | 9.9e-12 | 0.09 |
| NGC3115 / NGC0821 | isolated | 1.9-2.8e-10 | 1.7-2.8 |
| NGC1400/1407/4526 | noncentral / group | 3e-11 / 2e-14 / 4e-14 | 0.3 / 0.0 / 0.0 |
| NGC4486/4472 | Virgo A/B centrals | 1.5e-10 / 4.6e-10 | 1.4-4.1 |
| NGC1399/5846/5128/4278 | central-of-own-host | 1.4e-10 / 8.4e-11 / 5.9e-11 / 1.4e-10 | 1.2 / 0.7 / 0.5 / 1.2 |

Notes: NGC1407/4365/4526/5128 carry model-spread > 100x (173k x worst);
the fit table cannot support per-galaxy precision for those rows (BIL-R2).

## 2. Ledger grep (nothing re-graded)

- `opus_48_extended_research/reviews/CLUSTER_COMPREHENSIVE_REVIEW_SYNTHESIS_2026-06-14.md`
  already carried this paper ("Externally echoed by Bilek/Renaud/Samurovic
  2026... explicitly NOT an a0 shift") in the density-a0 lane.  That reading
  is UNCHANGED: this paper neither rescues nor kills the density-a0 fork; it
  was already banked there as a falsifier echo.  No entry re-graded.
- NEW content this wave: the ZD-series reading of the SAME datum --
  the central-galaxy deviation as the a0-line AMBIENT RESPONSE /
  disembodiment (B01-B03).  That is a different claim than an a0 shift and
  is the reference the synthesis's cluster entry lacked ("clusters
  UNDERSTOOD-AS-SHARED-AND-SOFT" now has its zero-parameter map).
- `deepseek_push/FALSIFIER_MATRIX.md` rows 23/28 (strip radius, per-cluster
  map): status ARMED unchanged; first-data-contact logged (appended below).

## 3. Referee attacks on the paper (numbered findings)

- **BIL-R1** -- NFW "virial mass" truncation concentration c is never stated:
  quantitative use of Appendix A.1 carries +-20% (A(c=7)/A(c=15)).  The
  wave's RN ratios are convention-independent; absolute g_halo values are not.
- **BIL-R2** -- the 3-anisotropy-model spread exceeds 10x for 5/17 galaxies
  (up to 173,553x for NGC1407) -- per-galaxy quantitative claims in the
  paper's figures inherit this floor; the paper's own caveat
  ("parameters can be nonphysical") is mandatory, not optional: 4/17 fits
  are VOID (all-negative stellar M/L).
- **BIL-R3** -- "stellar masses 1e10-1e11 Msun" is registered but NOT
  independently verifiable from this paper (needs BSR19).
- **BIL-R4** -- the collisionless-material conclusion overreaches: the Jeans
  parametrization (stars + NFW, no external-field component) cannot
  distinguish "own halo" from "ambient field at this position" -- the fits
  are blind to the very distinction their conclusion depends on.  The
  framework's disembodied halo IS dynamically cold, collisionless, and
  invisible by construction -- the data does not force a particle, and their
  own text hedges ("but also compact clouds of cold gas").  B01/B03 are the
  first quantitative test either way.
- **BIL-R5** -- "divergence starts closer to the center for more dominant
  hosts" is figure-level (no table); the direction matches the framework's
  containment radius r_t^2 = G M_b (a0 - 2 g_e)/g_e^2 (ZD01) with zero dials,
  but a quantitative comparison needs per-galaxy host offsets (see Door).
- **BIL-R6** -- the Virgo subcluster K-calibration (A+B+C = 6.3e14) is a
  tuned dial by their own admission; harmless at the 1-Mpc geometry level,
  flagged for any precision claim.

## 4. Falsifiers banked (number + recipe + falsifier)

- **F1 (B01, ARMED):** NGC4472 -- fitted halo x2.4 the maximal ambient
  envelope (full response + a0/2).  Recipe: measure the 3-D offset
  d(NGC4472, NGC4486) (Morgan+25 clump data, cited by the paper).  Kill:
  d >= 1.5 Mpc confirmed AND the V-band halo still >= 2x envelope -> the
  ambient reading fails for the strongest central of the sample.
- **F2 (B02, ARMED):** NGC3115 -- the paper's physically-plausible (neg)
  partition demands g_dark(22 kpc) = 1.28e-10 = 2.3x the certified cap on K1
  (2.5x on K2).  Recipe: partition-priored measurement (stellar M/L from
  population synthesis, GC-system kinematics at 15-25 kpc).  Kill:
  g_dark(15-25 kpc) > 1.1 * a0/2 (6.2e-11 K1 / 5.2e-11 K2) fires ZD01.
  Not fired today: partition unidentifiable (r_s/r_max = 0.12) + the paper's
  own caveat.
- **F3 (B03, ARMED):** NGC1400 (in-zone of NGC1407, r_strip = 1.11/1.34 Mpc
  K1/K2) and NGC4526 (in-zone of Virgo B if d < 1.0/1.2 Mpc): measured
  offsets from Tully15/Tempel16/Morgan25.  Kill: in-zone + physical fit +
  RAR-adherent -> rows 23/28 kill escalates.
- **F4 (row 23/28 instrument, sharpened):** cluster-dwarf kinematics inside
  vs outside r_strip per census cluster; the paper's sample class now gives
  the data route (GC-system kinematics exist for Virgo dwarfs).

## 5. One open door -- the ambient-response residual

B01's [0.1, 10] band reflects the crude 1-Mpc geometry; the data already
sits at median 2.4x the full response (K1), i.e. order-level reproducibility
with zero fitted constants.  Measured 3-D offsets for the Virgo quartet (and
offsets for NGC1400/4526) tighten the band to [0.3, 3] and turn the
residual into a precision test -- the same dataset resolves F1 and F3 in
one stroke.  Target: the Morgan+25 clump census + GC-system kinematics of
the Virgo dwarf population.

## Kill-condition honesty

No kill fired anywhere: B01 kill rule (unused band on both footings, >=2/4)
not reached; B02 cap survives by weak contact (only NGC1023 supplies clean
rows, 10-60x below cap); B03 15/15 decidable with zero mismatches.  The
three armed challenges (F1/F2/F3) are the wave's taxes -- each is one
measurement away from firing or confirming, and each names its number.

## Provenance and scope

All inputs come from the paper's own tables/text (provenance tagged row-by-
row in bilek_data.py); constants: G, MSUN, KPC, the two repo a0 footings
(K1 = 1.1279e-10, K2 = 9.3619e-11), the paper's 1.2e-10 for comparisons.
The framework map (r_strip = 4 sigma^2/a0, sigma_dyn^2 = G M/R) is the
committed ZD06/ZD09 content; note the ZD map post-dates the paper's data --
this is zero-parameter CORRESPONDENCE (first-data-contact), not a priority
claim.  Gate corrections recorded in-lane (B01 v1-v2 reader and challenge
bar; B02 NFW peak-rule correction); bands and kill rules unchanged through
every correction.