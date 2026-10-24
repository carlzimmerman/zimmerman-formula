# X19 assumption ledger (committed with FROZEN_CRITERIA.md, before any script or number of this lane)

κ = ½ FITTED. Footings never pooled. No dark-matter particle. Not "theory closed".

## Inputs and their class

| input | class | used for |
|---|---|---|
| E, s, Z per class (P4, X1, S1, U1, X7 JSONs) | FRAMEWORK-NATIVE (record results) | labels |
| SPARC rotmod + Lelli 2016c table (`real_research/data/`) | RAW | V for SPARC, UMa |
| Chae 2021 environments (`chae21_env.csv`, record copy) | SURVEY-CALIBRATION | e for SPARC, UMa |
| X1 / S1 per-system CSVs (LVD-based, record copies) | RAW → record | V for LG dwarfs, Coma UDGs |
| Lelli+15 TDG table (`tidal_dwarfs/lelli2015_tdg.csv`) | RAW | V for TDGs |
| CFG657 DF2/DF4 inputs (M★, R_e, σ, D, positions, ages) | RAW (record transcription) | V for DF2/DF4 |
| Tian+26 BFJR group table (`_external_data/vizier2026/J_A_A_710_L39.tsv`, already on disk) | RAW | V for groups |
| eRASS1 primary v3.2 FITS (MGAS500, M500, R500, KT) + X2's per-cluster npz (membership) | SURVEY-CALIBRATION | V for clusters |
| McMillan17 baryons (P4 B1: M_b 6.646e10, R₀ 8.122 kpc, v_c(R₀) from P4) | ΛCDM-PROCESSED (partly halo-fitted; P4 disclosure) | V for MW |
| t_H = 13.8 Gyr; ρ_crit with h = 0.672; Ω_b = 0.049; Ω_m = 0.31 | ΛCDM-PROCESSED conventions | N_orb, ρ_env, background |
| Ω_c/Ω_b = 5.364 | record's cosmic ratio | background E |

## Assumptions (named, so a reader can attack them)

- **A1 Baseline.** B_iso is primary because the successor (Z★) removes the EFE for owned units. Under v3s's own static
  EFE (B_EFE) the hosted labels change strongly (X1: +0.19 to +0.75 dex), so B_EFE is reported as a qualifier and any
  verdict difference is stated.
- **A2 Labels.** Z ≥ 2 for EXTRA and Z < 1 for NONE are conventions fixed here. Many hosted classes sit at 1–3σ against
  B_iso, so labels are footing-sensitive; per-footing verdicts are required to agree.
- **A3 Measurement radius.** V is evaluated where E is measured (§3). Different classes therefore probe different
  radii; this is the honest comparison for a local selector, but a global selector (a system-wide property) is better
  served by M_b, f_hot, H, N_orb.
- **A4 Cluster gas profile.** F1's β-model (r_c = 0.15 R500, β = 2/3) normalised to MGAS500; stars f★ = 0.20; no h
  rescaling of catalogue masses (F1 PRIMARY catalogue values). KT exists only for some eRASS1 rows; rows without it are
  skipped for V2/V7b and the count is reported.
- **A5 Hot gas outside clusters.** Galaxy-scale hot haloes (MW CGM, SPARC) are not in the record's baryon inventories, so
  f_hot = 0 there "by catalogue". If a hot CGM were added, f_hot would rise for massive spirals; reported as a caveat.
- **A6 Potential.** Newtonian baryonic potential with zero at infinity, point-mass host term g_N,host·d (J1's footing
  convention, simplified). The law's own logarithmic potential needs a reference radius and is not used (as J1).
- **A7 Relaxation.** N_orb uses t_age = 13.8 Gyr unless the record has an age; clusters (dynamically young) get an upper
  bound. The formation-mode flag O is reported only.
- **A8 Background.** The cosmic background is a requirement row (dust from z ≈ 1100), placed only on V defined on FRW.
  For M, σ, Φ it is not placeable and the verdict runs on bound systems (qualifier).
- **A9 Groups' E** is the record's log σ offset × 2. The group field is not on disk (P4: the pass holds only if
  g_e ≲ 0.01 a₀).
- **A10 SPARC's E** is at CFG695's global Υ (P4 reported row). With per-galaxy Υ the residual is absorbed (rms 0.054); the
  global-Υ row is the one that can show an excess.
- **A11 UMa's E** is the offset against field points in the same g_bar bins (U1 F5 A4, per galaxy), i.e. against the
  empirical field RAR, which equals the law to the record's precision.

## Disclosures (not blind)

- The E values of every class were read from the record while writing these criteria (they are the inputs). No V value,
  no ordering and no threshold of this lane had been computed. Reading the record showed that under B_iso Crater II
  (−0.44 dex) and Antlia II (+0.06 dex) need no extra, and that the cluster quintiles are not monotone in MGAS500; the
  label rule and the baselines were fixed after reading these, and before any V.
- No new data downloaded.
