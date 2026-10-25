# X33 assumption ledger (committed with FROZEN_CRITERIA.md, before any script or number of this lane)

κ = ½ FITTED. Footings never pooled. No dark-matter particle. Not "theory closed". Nothing is downloaded.

## Inputs and their class

| input | class | used for |
|---|---|---|
| SPARC rotmod curves (`real_research/data/sparc_data/*_rotmod.dat`) + `SPARC_Lelli2016c.mrt` (the record's loader, as P4 / X19; never `SPARC_table.txt`) | RAW | SPARC residuals and properties |
| CFG695 S2 global Υ (U₀ 0.60 / 0.55) | FRAMEWORK-NATIVE (record fit, κ-independent Υ) | SPARC primary residual, M★ |
| P4 results JSON (T1 per-galaxy Υ and wmean; T3 group means; T4 MW K_z; T5 TDG / DF points) | FRAMEWORK-NATIVE | residuals, step 0 |
| Chae+21 environment table (directional_efe_2026 laneB) | RAW (published e_N) | SPARC e_ext |
| `sparc_master_clean.csv` fD = 4 | RAW | UMa membership |
| Tian+26 BFJR groups TSV (`_external_data/vizier2026`) | RAW | group residuals, properties |
| eRASS1 primary v3.2 FITS (KT, MGAS500, M500, R500, L500, BEST_Z) | SURVEY-CALIBRATION (M500 from scaling relations) | cluster properties |
| X7 per-cluster npz + X2 source (exec'd read-only, exactly as X21 does) + X21 results JSON | FRAMEWORK-NATIVE | per-cluster n_i, d_i; step 0 |
| X1 `x1_per_system.csv`, X1 `.out`; X20 `x20_per_system.csv` | FRAMEWORK-NATIVE | LG dwarf residuals, properties, hosted flag |
| S1 results JSON `coma` + `s1_coma_per_galaxy.csv` | FRAMEWORK-NATIVE | Coma residuals, properties |
| Lelli+15 TDG CSV; CFG657 DF2/DF4 inputs (regex, as X19) | RAW (record transcription) | TDG / DF residuals, properties |
| S4 R4 `cfg528b_measured_tracers/nu1_noown` results JSON; Forbes+17 SLUGGS galaxy TSV | FRAMEWORK-NATIVE; RAW | SLUGGS residuals; M★, R_e, D |
| S2 results JSON ladder L4 / L5 | FRAMEWORK-NATIVE | lens-stack rows |

## Assumptions (named, so a reader can attack them)

- **A1. Common axis is approximate for five classes.** MW disc (K_z), groups (σ² → g), clusters (lensing ratio), SLUGGS
  (σ → g by × 2), lens stacks. These are marked in §2 of the criteria; pooled statistics use P_gal (exact or × 2 only) as
  the primary pool and P_all as the secondary.
- **A2. SPARC primary residual uses the record's global Υ, not P4's per-galaxy Υ.** With one free Υ per galaxy the median
  residual is driven toward zero by construction; the global-Υ residual keeps the information. The per-galaxy-Υ median and
  rms are reported as extra columns, and the per-galaxy Υ itself is reported (never graded: it is chosen by the residual).
- **A3. SPARC residual uses the isolated algebraic law**, not P4's solved EFE. P4 reports the EFE moves the pooled rms by
  < 0.001 dex; S0b bounds the class-mean shift at 0.010 dex.
- **A4. Per-cluster A_i is noisy** (single-cluster weak lensing); its error is shape noise only (no LSS, no leakage error,
  no calibration covariance). Clusters with A_i ≤ 0 have no log residual (NaN, kept in the table with the raw A in
  `quality`). Spearman on clusters uses A_i itself (rank-invariant), so those clusters stay in the rank tests.
- **A5. Properties are footing-independent descriptors** evaluated on the canonical footing (x_char, e_ext) and at the
  canonical global Υ (SPARC M★). Residuals carry both footings.
- **A6. R_char is a half-mass proxy that differs by class**: SPARC R_eff (3.6 µm half-light), dwarfs / Coma / DF r_h or R_e,
  groups R_e, TDGs R_out (no half radius on disk), clusters R500, SLUGGS R_e. Sigma_half inherits this.
- **A7. Masses.** SPARC M★ = Υ L[3.6] (bulge not separated in the column), M_gas = 1.33 M_HI. Dwarfs, Coma, DF, SLUGGS:
  M_b = M★ (gas-poor; M_gas NaN, f_gas NaN). TDGs: M_bar from Lelli+15, M★ NaN. Groups: M_bar from Tian+26. Clusters:
  M_b = 1.2 MGAS500 (X19 / F1 convention f★ = 0.20 of gas), M_gas = MGAS500. MW: 6.65e10 M☉ (X19).
- **A8. Hosted flag**: X20 `hosted` for LG dwarfs; Coma, TDGs, DF2/DF4 = 1; SPARC = 1 only for UMa members; groups,
  clusters, MW, SLUGGS centrals = 0 (NGC 4374 sits in Virgo near M87 but is a central in the record's reading).
- **A9. Trials.** Benjamini–Hochberg treats the tests as one family per footing; correlated properties (M_b, M★, V,
  σ) make it conservative, not anticonservative.
- **A10. The SPARC sub-sample selection, distance and inclination systematics** are carried only through the residual error
  (and as diagnostic properties), not corrected.

## Not done (declared)

- No AQUAL disc solve per SPARC galaxy (P4's D1 says up to −0.10 dex at R = 0.5 R_d for the lowest Σ₀).
- No per-group external field (none on disk); P4 shows the groups are EFE-sensitive.
- MeerKAT galaxies (no per-object law residual committed in P4) and the outer globulars are not in the atlas.
