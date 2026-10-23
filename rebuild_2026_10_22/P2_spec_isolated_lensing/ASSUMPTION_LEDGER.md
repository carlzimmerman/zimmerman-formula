# P2_spec_isolated_lensing: assumption ledger (written before any script, shear read or model number)

Classes: RAW / FRAMEWORK-NATIVE / SURVEY-CALIBRATION / ΛCDM-PROCESSED / STANDARD-MOND-MACHINERY.
Paths are repo-relative (`../_external_data` = the data store beside the repo). "F2" = `rebuild_2026_10_22/F2_outer_lensing/`.

## A. Inherited from F2's verdict (what P2 replaces or keeps)

| # | ingredient | class | F2 source | P2 |
|---|---|---|---|---|
| R1 | photo-z isolated lenses (record reconstruction, \|Δχ\| < 10 / 100 / 300 Mpc vetoes) | SURVEY-CALIBRATION (ANNz2 photo-z) | `lr_lenses.npz`, `cfg96_isoflags.npz` | **replaced** by spec-z isolation (GAMA); read only for K0b |
| R2 | record per-lens stack (cfg110) | RAW + SURVEY-CALIBRATION | `cfg110_perlens.npz` | **replaced** by my own measurement; read only for K0b |
| R3 | B21 Fig. 3 / Fig. 4 GAMA profiles | RAW (h70, fiducial ΛCDM distances) | `brouwer2021_rar/` | not used (B21's GAMA lens list is not on disk) |
| R4 | EFE values: Chae+21 noclu / maxclu medians (SPARC environments) | SURVEY-CALIBRATION, not KiDS | `chae21_env.csv` | **replaced** by the GAMA catalogue's own field (case b) |
| R5 | AQUAL point mass in a uniform field, orientation-averaged M_eff | FRAMEWORK-NATIVE | `f2_aqual.py` | kept (imported read-only) |
| R6 | baryon inventory: M★ LePhare + 0.15, cold gas B21 relation, hot CGM 0.5 M★ / 100 kpc | SURVEY-CALIBRATION | F2 ledger B1–B3 | kept, with spec-z mass rescaling |
| R7 | native h 0.679, Ω_m 0.3085 | FRAMEWORK-NATIVE / SURVEY-CALIBRATION | F2 H1/H2 | kept |
| R8 | no two-halo term in any verdict (CFG502 ΛCDM, CFG805 knobs, CFG903 catchment) | — | F2 | kept; P2's environment is the catalogue's own galaxies |

## B. Inputs of this lane

| # | ingredient | class | source | error / bracket |
|---|---|---|---|---|
| D1 | GAMA DR4 G3CGalv10 spec-z (r < 19.8, G09/G12/G15) | RAW (spectroscopic redshifts; heliocentric/CMB frame as delivered) | `campaign_fresh_gravity/_external_data/cfg471/G3CGalv10.csv`, sha256 in CFG471 FETCH_LOG | GAMA redshift completeness ~98 %; checked (K5) |
| D2 | KiDS-1000 SOM-gold shapes, weights, Z_B | RAW + SURVEY-CALIBRATION (lensfit, Z_B) | `../_external_data/kids_lensing_zsplit/` via F1's reader cache (`f1_extract.py`, argv) | cache drops Z_B = 1.20 rows (float32), disclosed in K0b |
| D3 | source redshift for Σ_crit = point Z_B, cut Z_B > z_l + 0.2 | SURVEY-CALIBRATION | record / F1 convention | ± 3 % (one at a time); no SOM n(z) correction |
| D4 | shear calibration 1+K = 0.9853 | SURVEY-CALIBRATION | B21 bias column (F2 C2) | — |
| D5 | boost (lens–source clustering) | not corrected | — | reported from L vs R source weights |
| M1 | lens and neighbour M★: KiDS-bright LePhare MASS_MED + 0.15, rescaled to the spec-z distance | SURVEY-CALIBRATION (SPS; E1 soft) | `real_research/data/lensing_rar/KiDS_DR4_brightsample{,_LePhare}.fits` | ± 0.2 dex (one at a time); GKV G09 offset reported |
| M2 | neighbour proxy M★ from r_petro and z (no valid LePhare) | SURVEY-CALIBRATION (catalogue-internal M/L) | G3C `Rpetro`, calibrated on valid LePhare | 0.30 dex scatter, used as a conservative veto margin |
| M3 | completeness limit M_lim95(z) | SURVEY-CALIBRATION (catalogue-internal) | G3C + LePhare | 95th percentile; leak ~ 5 % of a missed host (stated) |
| E1 | isolation rule: host veto f = 1, R_iso 3 (1) Mpc, \|Δv\| < 1000 km/s, edge ≥ R_iso | design choice (frozen) | FROZEN_CRITERIA §2 | f = 0.1 cannot be complete (29 lenses) |
| E2 | iso-random hole subtraction | RAW (data-only) | FROZEN_CRITERIA §3 | residual lens-correlated environment carried by the model's T_nbr difference |
| F1 | AQUAL μ = x/(1+x), lensing = dynamics | FRAMEWORK-NATIVE | C4 K1/K2, E2, THEORY_V3 §1 | — |
| F2 | screening L★ ≥ 21.7 pc | FRAMEWORK-NATIVE (fitted bound) | D10 | irrelevant at R ≥ 30 kpc |
| F3 | BS K(Q) dust: no galaxy-bound profile; abundance an initial condition | FRAMEWORK-NATIVE (OPEN) | C2, C4 | no dust term; the needed extra mass is reported |
| F4 | BS24 Eq. 35 μ_K² ψ static term | FRAMEWORK-NATIVE, **not included** | N0 audit | deferred (as S2 / R6); stated |
| F5 | neighbour term: linear superposition of each galaxy's AQUAL profile | FRAMEWORK-NATIVE approximation | FROZEN_CRITERIA §5 | exact in the EFE-linearised regime; upper estimate at y_e → 0 |
| G1 | external field (b): Newtonian vector sum of catalogue baryons at 1–10 Mpc, completeness-corrected, x_e from μ(x_e)x_e = y_e | FRAMEWORK-NATIVE equation on SURVEY-CALIBRATION masses | FROZEN_CRITERIA §5 | brackets: no correction, R_f 5/20, projected slab, baryon- and matter-tracing (reported only) |
| G2 | C_b(z) from the catalogue's 1/V_max baryonic mass function | SURVEY-CALIBRATION (catalogue-internal) | G3C + M1/M2 | no k-correction (stated) |
| G3 | Ω_b h² = 0.0224 (baryon-tracing bracket) | FRAMEWORK-NATIVE (BBN, A78) | — | reported only |
| G4 | 5.364 = Ω_c/Ω_b (matter-tracing bracket) | ΛCDM-PROCESSED | F2 ledger R6 | reported only, flagged; never in a verdict line |
| H1 | native h 0.679 (0.672–0.686), flat Ω_m 0.3085 | FRAMEWORK-NATIVE / SURVEY-CALIBRATION | F2 H1/H2 | ends one at a time |
| H2 | a₀ footings 9.3603e-11 / 1.1312e-10 | FITTED (κ = ½); alt ΛCDM-PROCESSED (E1) | doors BRIEF | never pooled |

No ΛCDM-PROCESSED or STANDARD-MOND-MACHINERY ingredient enters a verdict line. The EFE here is AQUAL's own boundary
condition for a uniform field (F2's solver), with the field's size measured from the catalogue; no algebraic EFE recipe
and no QUMOND phantom is used. The fiducial (Ω_m 0.3, h 0.7) distances appear only in converting the catalogue's
LePhare masses to the spec-z, and are then replaced by native distances exactly as F2 does.
