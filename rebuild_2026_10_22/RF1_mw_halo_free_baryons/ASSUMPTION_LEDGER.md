# RF1_mw_halo_free_baryons: assumption ledger (committed with FROZEN_CRITERIA.md, before any script or number)

Classes as X5: RAW / FRAMEWORK-NATIVE / SURVEY-CALIBRATION / ΛCDM-PROCESSED / STANDARD-MOND-MACHINERY / LITERATURE-INPUT.
PROVISIONAL = not read from the paper in this lane.

## Baryons

| ingredient | class | source | role |
|---|---|---|---|
| Σ_b(R₀) 47.1 ± 3.4; gas 13.7 ± 1.6 | LITERATURE-INPUT, star counts + gas census, no dynamics; PROVISIONAL (transcribed in the record, paper not on disk) | McKee+15, `hunt_2026/g02_vertical_vs_planar_frequency_split.py` | graded axis |
| R_d 2.6 ± 0.5 | LITERATURE-INPUT, review range; PROVISIONAL | BH&G16, same file | graded axis |
| R_d 2.64 ± 0.13, M★ 6.08 ± 1.14 | LITERATURE-INPUT, PROVISIONAL (meta-analysis assuming exponential discs; web look-ups of 10-23) | LN16, LN15, via X5 | tags only |
| M_bb 1.88 ± 0.12 | **ΛCDM-PROCESSED**, PROVISIONAL (made-to-measure with a dark halo) | Portail+17, via X5 | BRACKET only, never graded |
| Kent 1992; Dwek+95; pre-M2M counts | LITERATURE-INPUT, **NOT ON DISK, UNREAD** | none | empty rows; M/L not stated because not read |
| HI, H₂ radial forms | **NOT CLEAN.** Survey tables are not on disk. McMillan's forms held; whether they entered his fit is not established by this ledger | P4 `rho_mcm` | shape only, labelled; column rescaled to McKee |
| z_d 0.3, 0.9 kpc, thin/thick share | SURVEY-CALIBRATION, **partly ΛCDM-PROCESSED per X5's ledger**. No ledger on disk shows they come from star counts, so the summary's condition for holding them is NOT MET. Held, labelled, with a ±20 % sensitivity | P4 | shape, labelled |
| Bulge shape | McMillan's, rescaled; X5's modelling choice; same label | P4 | shape, labelled |
| One R_d for both discs | modelling choice, X5 | P4 B3 | declared |

**Consequence.** Even with a bulge value, this baryon field would be halo-free in its normalisations, not in every
shape. The README must say so.

## Targets (not baryons; inherited)

| ingredient | class | note |
|---|---|---|
| Bovy & Rix 2013 K_z,1.1, 43 MAPs ⊕ 5 %; summary 66.4 ± 2.2 | SURVEY-CALIBRATION (Newtonian dynamical fits). Their fits assume a potential family; route E is Newtonian, so the framework's gravity matches | X5 ledger |
| Eilers+19 target 229.05 ± 4.65 | RAW + Jeans modelling (SURVEY-CALIBRATION) | X5 ledger |
| Ou+24, S3's error model | RAW + Jeans modelling (SURVEY-CALIBRATION) | X5 ledger |
| R₀ 8.122 | SURVEY-CALIBRATION | X5 ledger |

## Rule

| ingredient | class | note |
|---|---|---|
| OS1 q_f, σ_ref, Σ_a₀ | FRAMEWORK-NATIVE (κ fitted, q fitted on SPARC) | SPARC's fit is on free Υ |
| CE1 A4 η, X80 ρ₁₀, ρ₁₁; Σ_coll | FRAMEWORK-NATIVE (native zooms); core shape chosen by hand (X70) | ND1, owner decision |
| f_c 0.84055 | FRAMEWORK-NATIVE as inherited from ND1 (Ω_m 0.2976, ω_b 0.0223081, h 0.6856). **The ω_b provenance is not re-derived here** | ND1 |
| EM1 R1 M200(M_b): a 11.18, b 0.90 | FRAMEWORK-NATIVE per EM1 (no abundance matching). Built on NFW dust on SPARC, which is not this core; RG1 and GD2 do the same | EM1 |
| Background A (record's plik-lite refit, C2 c2b, g = 1) | fitted by the record to Planck **likelihood data**, not Planck's parameters. Flagged | F3 |
| Background B (CFG886 Ω_m 0.2976, h 0.686, with A's A_s, n_s) | FRAMEWORK-NATIVE, except A_s, n_s from A. Reported on the same row | F3 |
| Spherical halo, no contraction | modelling choice, GD1 | |

## External field

| ingredient | class | note |
|---|---|---|
| e_N = 0 | graded | route E has no EFE |
| M31 1.3e11 at 770 kpc; LMC 3e9 at 49.9 kpc | LITERATURE-INPUT, PROVISIONAL, record's h81 | tide only, reported |
| 2M++ | ΛCDM-PROCESSED | not used |

Nothing is downloaded. Nothing is fitted.
