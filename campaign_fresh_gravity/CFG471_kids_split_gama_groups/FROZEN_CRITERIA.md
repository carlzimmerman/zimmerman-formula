# CFG471 FROZEN CRITERIA: KiDS early/late split by spectroscopic host status (GAMA G3C groups)

Frozen and committed before any script exists and before any lensing number for any GAMA subset has been computed.
κ = ½ is fitted, never derived. Both a₀ footings (9.3603e-11 and 1.1312e-10 m/s²) enter only through the law's zero
prediction: B's law predicts a negligible early-minus-late difference at fixed g_bar in K1 under both footings (CFG61/CFG88),
so the zero model is the law under both footings. No dark-matter particle; the cold mass is still required.

## Question

CFG446 found, with a photo-z companion count, that companion-poor early types carry the full KiDS early/late 1-halo split
(matched A_poor 0.95 ± 0.20), so the two-regime (host-status) explanation of B's KiDS failure FAILED at photo-z reach. Its
caveat: the photo-z window is about ±250 Mpc. Here host status is a spectroscopic label: membership in the GAMA Galaxy Group
Catalogue (G3C, Robotham et al. 2011; GAMA DR4 tables G3CGalv10 / G3CFoFGroupv10). Prediction of the two-regime reading:
early types that are centrals of real groups carry the split; early types that GAMA sees but places in no group sit at the
late level. ΛCDM also predicts group centrals lens more, so SUPPORTED would not discriminate the framework from ΛCDM;
FAILS would remove the two-regime explanation again, now with spectroscopic host status.

## Data

- Lensing (on disk, as CFG446): `real_research/data/lensing_rar/cfg110_perlens.npz` (WG, WW per lens per g_bar bin),
  `lr_lenses.npz`, `lr_esd_jackknife.npz` (June patches). ESD = Σ WG / Σ WW / KG, KG = 1.989e30 / (3.0857e16)². K1 = bins 8–14.
- G3C (fetched 2026-10-07 from the GAMA DR4 release at Data Central TAP, `gama_dr4.G3CGalv10` 204,110 rows and
  `gama_dr4.G3CFoFGroupv10` 26,194 rows; the gama-survey.org server timed out). Files in
  `campaign_fresh_gravity/_external_data/cfg471/` (git-ignored, > 5 MB); URL, query, bytes and sha256 in `FETCH_LOG.md`.
  The script checks the sha256 of both files before use.

## Footprint, matching and classes (frozen)

- **GAMA footprint:** lenses inside the equatorial boxes G09 (129 < RA < 141, −2 < Dec < 3), G12 (174 < RA < 186,
  −3 < Dec < 2), G15 (211.5 < RA < 223.5, −2 < Dec < 3).
- **Cross-match:** nearest G3CGal galaxy within **1.5 arcsec** (declared; 1.0 and 2.0 reported). G3CGal is the group-finding
  input itself (r_petro < 19.8, good redshifts), so a match = GAMA-detected within the GAMA limit r < 19.8; unmatched lenses
  (fainter than 19.8, outside the spectroscopic completeness, or outside G3C coverage) are excluded from the classes. No
  redshift-agreement cut; the spec − photo z robust scatter is reported.
- **"Big group":** G3C group with N_fof ≥ 3, OR N_fof ≥ 2 with halo mass MassAfunc / h ≥ 10^12.5 M☉ (h = 0.7; MassAfunc is
  in M☉/h, Robotham et al. 2011's functional A calibration).
- **Class C (group central, the test):** matched early lens whose G3C galaxy is the group's IterCen (G3C's preferred central)
  of a big group. Reported variant: BCG instead of IterCen.
- **Class F (field, the test):** matched early lens with G3C GroupID = 0 (in no group).
- **Reported only:** S = matched early lens in any group that is not its IterCen (G3C satellites among the "isolated" lenses);
  P = IterCen of an N_fof = 2 group below the mass cut.
- Late types are not split; they are the reference.

## Statistic (frozen)

- Template D_full(k) and C exactly as CFG88/CFG446 (all early minus all late, all 181,477 lenses, 50 June patches);
  C⁻¹ and D_full are then FIXED.
- **Reference:** all late lenses in the GAMA footprint (unweighted), the same reference for every subsample.
- For an early subsample S: D_S = ESD(S) − ESD(footprint late); **A_S = (D_full^T C⁻¹ D_S) / (D_full^T C⁻¹ D_full)**.
- **Errors:** leave-one-patch-out jackknife over the June patches that contain footprint lenses (12, from a catalogue-only
  count), dropping each patch from both S and the reference, with D_full and C⁻¹ fixed;
  σ² = (n − 1)/n Σ (A_i − Ā)², n = number of such patches. Departure from CFG446 (which also varied the template): the
  template is a common normaliser here, and only 12 of the 50 patches touch GAMA. Reported check: 36 sub-patches (each June
  patch split into three by lens-RA terciles within it). No own-covariance χ² (12 patches cannot support a 7-bin covariance).
- **ΔA = A_C − A_F**, σ from the jackknife replicates of the difference.
- **Matched version (headline):** per-lens weights so that each class's (log M*, z) histogram equals that of all matched
  early lenses in the footprint, cells **0.2 dex from 8.5 to 11.1 × 0.1 in z from 0.1 to 0.5** (coarser than CFG446's 0.1 ×
  0.05 because the classes are 10–100× smaller; departure); w = [n_ref(cell)/n_S(cell)] (N_S/N_ref); empty cells dropped,
  dropped fraction reported. The reference stays unweighted. Unmatched reported with its own verdict; disagreement flagged.

## Verdicts (on the matched statistic)

- **TWO-REGIME SUPPORTED:** |A_F| / σ_F < 2 AND A_C / σ_C > 3.
- **FAILS:** A_F / σ_F > 3 AND A_F ≥ 0.70.
- **NON-DISCRIMINATING:** otherwise.

## Power (declared before scoring, from counts and CFG446's committed errors only)

Catalogue-only counts (no lensing number): 34,872 footprint lenses (17,430 early, 17,442 late); 11,101 early matched at 1.5";
class C 808 (BCG variant 780; N_fof ≥ 3 alone 286), class F 7,207, S 2,847, P 239. Model σ_A² = k (1/N_S + 1/N_ref) with k
fitted to CFG446's unmatched E1 tercile error (0.165 at N_S = 29,360, N_ref = 93,398): k ≈ 610. Expected: **σ_F ≈ 0.35,
σ_C ≈ 0.89** (matching and the 12-patch jackknife add to this).
- If the split is environment-independent (A_F = 1): P(FAIL) ≈ Φ(1/0.35 − 3) ≈ **0.44**.
- If the two-regime reading holds (A_F = 0): SUPPORTED also needs A_C > 3 σ_C ≈ 2.7, i.e. group centrals carrying ≳ 2.7× the
  full split; for A_C ≈ 1–2 SUPPORTED is out of reach.
- **Declared:** the test can FAIL (about a coin flip if A_F = 1) but can SUPPORT only for a very large central excess;
  NON-DISCRIMINATING is the most likely outcome under either reading. It is the spectroscopic check of CFG446's caveat, not a
  stronger test than CFG446. The measured 1/σ_F is reported; if 1/σ_F < 3 the verdict carries "UNDERPOWERED to FAIL".

## Controls (load-bearing; the main run exits 1 on any failure)

- **C0:** the per-lens sums reproduce CFG88's K1 D to 1e-6 relative and its zero-model Hartlap χ² 35.0418 to 1e-6.
- **C1 (footprint control):** all early lenses in the footprint, against the footprint late reference, unmatched:
  |A_box − 1| < 2 σ_box (CFG446's full-sample amplitude reproduced inside the GAMA footprint). Also reported: all matched
  early (r < 19.8) A.
- **C2 (cross-match):** the chance-match rate with lens positions shifted by +60 arcsec in Dec is < 2% of the real match rate.
- **C3:** classes C, F, S, P are disjoint and C ∪ F ∪ S ∪ P = matched early.
- **C4 (null calibration):** 100 random pairs of disjoint subsets of the matched early lenses with the sizes of C and F
  (seed 471), matched weights: std of ΔA/σ_ΔA in [0.7, 1.4] (the upper edge widened from CFG446's 1.3 for the 12-patch
  jackknife's own scatter).
- sha256 of both G3C files equals FETCH_LOG.md.

## MUTATE

MUTATE=1 shuffles the class labels (C, F, S, P) among the matched early lenses, 20 shuffles (seeds 471–490), and recomputes ΔA.
Check M1 (load-bearing only in MUTATE; reported in the main run as the real |ΔA|/σ): the median over shuffles of |ΔA|/σ ≥ 1.
Under the null the median is about 0.67, so M1 must FAIL and the MUTATE run exits 1. If it passes, that is reported.

## Disclosures (before freezing)

- Read: CFG446 README, FROZEN_CRITERIA, script and output (CFG88 split and CFG61 law stacks through it).
- Catalogue-only numbers computed before freezing: the counts above, the match-radius table (0.5"–5": 11,041–11,315 early),
  the spec − photo z robust scatter (0.025), and the June-patch coverage (12 patches). Median log M* of class C 10.80 vs F 10.73;
  median z 0.280 vs 0.294. No lensing number for any GAMA subset was computed.
- Observed before freezing and reported as a finding, not a test: 26% of matched early "isolated" lenses (2,847) are G3C
  members that are not their group's IterCen, i.e. the photo-z isolation admits spectroscopic group satellites.
- The halo-mass branch of "big group" (task: N_fof ≥ 3 OR halo mass ≥ 10^12.5) was chosen as the union, raising class C from
  286 to 808; this was decided from the counts, for power, before any lensing number.
