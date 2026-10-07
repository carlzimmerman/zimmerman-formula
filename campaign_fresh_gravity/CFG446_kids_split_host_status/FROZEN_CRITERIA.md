# CFG446 FROZEN CRITERIA: is the KiDS early/late split carried by early types that are group centrals?

Frozen and committed before any script exists and before any lensing number for any environment subset has been computed.
κ = ½ is fitted, never derived. Both a₀ footings (9.3603e-11 and 1.1312e-10 m/s²) enter only through the
law's zero prediction: B's law predicts a negligible early-minus-late difference at fixed g_bar in K1 under both
footings (CFG61/CFG88), so the zero model is the law under both footings. No dark-matter particle; the cold mass is still required.

## Question

The "two regimes" reading (sonnet55_push/cold_mass cm08–cm10, CFG399) says the retained cold mass jumps from ~0.13 to
~0.6 of the cosmic share at the group step, keyed to host status (group membership), not temperature. Isolated KiDS
lenses are not satellites of brighter galaxies within the June isolation window, but they can be centrals with faint
companions. Prediction of the two-regime reading: the early-minus-late lensing excess (B's one specific failure against a
standard halo, CFG88: 4.4σ) is carried by early types that are group centrals; early types with few companions sit at the
late-type level.

**ΛCDM also predicts that richer centrals lens more.** A SUPPORTED verdict would therefore not discriminate the framework
from ΛCDM. A FAILS verdict would remove the two-regime explanation of B's failure.

## Data (all on disk; nothing downloaded)

- `real_research/data/lensing_rar/cfg110_perlens.npz` (WG, WW, NN per lens per g_bar bin; CFG110 stage), `lr_lenses.npz`,
  `lr_esd_jackknife.npz` (June patch labels, 50 patches), `KiDS_DR4_brightsample.fits` + `_LePhare.fits` (row-aligned).
- ESD = Σ WG / Σ WW / KG in M☉/pc², KG = 1.989e30 / (3.0857e16)², exactly as CFG110. K1 = g_bar bins 8–14.

## Environment measures (frozen)

- **Neighbour pool** = CFG96's isolation pool: MAG_AUTO_CALIB < 20, 0.1 < zphot_ANNz2 < 0.5, masked == 0,
  log M* = MASS_MED + 0.15 finite and > 7.
- **Lens matching:** each lens matched to the bright sample by exact (RA, Dec) as in CFG115.
- **Aperture:** projected R < 0.5 Mpc physical at the lens photo-z: θ = 0.5 (1 + z_l) / χ_l (χ_l from lr_lenses, h = 0.7,
  Ω_m = 0.3, the stage convention).
- **Line-of-sight window:** |z_nb − z_l| < 2 σ_z with σ_z = 0.018 (1 + z_l), the published ANNz2 scatter of the KiDS
  bright sample (Bilicki et al. 2021, quoted, not re-derived here; the catalogue on disk carries no per-object error).
- **E1 (the task's measure, primary):** N_sat = number of pool galaxies in the aperture and window with
  log M*_nb < log M*_l − 1 (mass < 10% of the lens, allowed by the isolation criterion).
- **E2 (departure, co-reported; see Disclosures):** N_cmp = the same with log M*_nb < log M*_l (all companions less massive
  than the lens, so the lens is still the most massive galaxy in the aperture).
- **Background with random positions:** randoms drawn uniformly on the sphere inside the two KiDS fields' bounding boxes and
  kept if they fall in an occupied HEALPix pixel (nside 512; occupied = at least one bright-sample object with masked == 0).
  K = 10 randoms per lens (seed 446), each scored with the lens's own z_l, log M*_l and θ_l. N_bg,l = mean over the 10.
  **X_l = N_raw,l − N_bg,l.**
- **Split:** within each class, terciles of X by rank (ties broken by a seeded random key, seed 446): poor = lowest third,
  mid, rich = highest third. Early types carry the test; late types are a reported check.

## Statistic (frozen)

- Template D_full(k) = ESD(all early, k) − ESD(all late, k) on K1; C = its leave-one-patch-out jackknife covariance
  (50 June patches).
- For an early subsample S: D_S = ESD(S) − ESD(all late), the SAME late reference for every subsample.
- **Amplitude** A_S = (D_full^T C^-1 D_S) / (D_full^T C^-1 D_full) (CFG96's definition; A_full = 1 by construction);
  σ_A from the leave-one-patch-out replicates of A_S with C^-1 fixed. Significance z_S = A_S / σ_A.
- Reported with it: the zero-model χ² of D_S with its own jackknife covariance, Hartlap 41/49, 7 dof.
- **ΔA = A_rich − A_poor**, σ from the jackknife replicates of the difference.
- **Matched version (the headline):** per-lens weights for the poor and the rich subsamples so that each one's 2-D lens-count
  histogram in (log M*, z) (bins 0.1 dex from 8.5 to 11.0; 0.05 in z from 0.1 to 0.5) equals that of all early types:
  w_l = [n_all(cell) / n_S(cell)] (N_S / N_all). Cells empty in S are dropped; the dropped fraction of all-early lenses is
  reported. Weighted ESD = Σ w WG / Σ w WW. The late reference stays unweighted. The unmatched version is reported with its
  own verdict; a disagreement is flagged.
- Errors: the repo's jackknife (as CFG88). No bootstrap.

## Verdicts (per measure, on the matched statistic)

- **TWO-REGIME EXPLANATION SUPPORTED:** |A_poor| / σ < 2 AND A_rich / σ > 3.
- **FAILS:** A_poor / σ > 3 AND A_poor ≥ 0.70.
- **NON-DISCRIMINATING:** otherwise.
- **Informativeness gate G (per measure, reported):** mean X(rich early) − mean X(poor early) ≥ 0.5 galaxies. If a measure
  fails G, its verdict is forced to NON-DISCRIMINATING (the measure carries too few companions to define host status).
- **Headline rule:** the lane headline is E1's verdict if E1 passes G; otherwise E2's verdict, labelled as the departure measure.
- **Power (reported, R0):** 1/σ_A(poor) and 1/σ_A(rich), matched. 1/σ_A(poor) is the separation in σ between "no
  environment dependence" (A_poor = 1) and the two-regime reading (A_poor = 0). If 1/σ_A(poor) < 3, the test is declared
  UNDERPOWERED to FAIL, and this is stated with the verdict.

## Controls (load-bearing; the main run exits 1 on any failure)

- **C1:** from the per-lens sums with the June patches, D_full equals CFG88's committed K1 D to 1e-6 relative, and the
  zero-model Hartlap χ² equals CFG88's 35.0418 to 1e-6 relative.
- **C2:** all 181,477 lenses match the bright sample by exact position; u − r > 2.0 reproduces typ; log M*_l equals the
  matched MASS_MED + 0.15; every lens is in the neighbour pool.
- **C3 (random-position background):** at an independent set of random positions (one per lens, seed 4461), each carrying
  its lens's z, log M* and θ, the mean X over all lenses is consistent with zero within 3 standard errors, for E1 and E2.
  The real lenses' mean X (early, late) is reported.
- **C4:** the terciles partition each class exactly.
- **C5 (null calibration):** 100 random equal-thirds labelings of the early types (seed 446): the standard deviation of
  ΔA/σ_ΔA (matched) lies in [0.7, 1.3], for the E1 labeling sizes.

## MUTATE

MUTATE=1 shuffles X among the early types (seed 446) for both measures, then runs everything. Check M1 (load-bearing in
MUTATE only, reported in the main run): |ΔA_matched| / σ ≥ 1 for E1 and E2. It must FAIL, so the MUTATE run exits 1.
If it passes, the poor/rich contrast is not shown to come from the environment ranking, and this is reported.

## Disclosures (before freezing)

- Read: CFG88, CFG96, CFG110, CFG115 READMEs; CFG110/CFG96 stage scripts; CFG110/CFG115/CFG96 scoring code; CFG88's results
  JSON (the full-sample K1 split, already committed); STANDING §3 and appended notes; CFG399 README.
- A catalogue-only completeness table was printed before freezing (no lensing number): in 0.05 z slices the pool's
  5th-percentile log M* rises from 8.8 (z 0.10) to 9.4 (z 0.20), 10.0 (z 0.30) and 10.5 (z 0.40), while the lenses' median
  log M* tracks the pool median (9.6 → 10.6 → 10.8). Companions 1 dex below the lens are therefore below the r < 20 limit
  for most lenses at z ≳ 0.2. This is why E2 is added and why gate G exists. E1 is kept as the primary because it is the
  task's measure; the headline rule above decides which verdict leads, before any result.
- No environment value X and no subset lensing number has been computed.

Departures from the task text: E2 (co-reported) and gate G, both motivated only by the completeness table; the matched
statistic is the headline (the task lists it as the second version).
