# P1_dwarf_chemistry ASSUMPTION LEDGER (written with the frozen criteria, before any number)

Classes: RAW / FRAMEWORK-NATIVE / SURVEY-CALIBRATION / ΛCDM-PROCESSED / STANDARD-MOND-MACHINERY / MODEL ASSUMPTION / EXTERNAL.

## A. What E6 Part C (the verdict under test) rests on

| ingredient | class | file |
|---|---|---|
| mean [Fe/H] per system (LVD `metallicity`, spectroscopic or photometric) | RAW-derived summary (SURVEY-CALIBRATION: line-index or synthesis calibrations) | `real_research/data/dsph/lvd_dwarf_*.csv`; E6 L468 |
| one-zone homogeneous leaky box, instantaneous recycling and mixing, no inflow | MODEL ASSUMPTION | E6 L113–270 (copied from CFG920) |
| wind at ISM metallicity, ζ = 1 | MODEL ASSUMPTION (the conditional under test) | E6 criteria L59 |
| no pre-enrichment (Z0 = 0) | MODEL ASSUMPTION (the conditional under test) | E6 criteria L59 |
| Fe yield log y ∈ {−0.5, −0.2, +0.1} (CC-dominated, CFG317) | SURVEY-CALIBRATION + EXTERNAL textbook | `campaign_fresh_gravity/CFG317_baryon_loss_cold_mass/FROZEN_CRITERIA.md` L80 |
| W1 (continuous wind) / W2 (W1 + terminal strip) family, L minimised over it | MODEL ASSUMPTION | CFG920 |
| gas = 1.33 × M_HI | SURVEY-CALIBRATION | E6 L48 |
| L_req = M_c,req / (5.364 M_b) (F1: screened extra-only; F2: Newton mass-conserving) | inherits E3 (below) | E6 CSV |
| 5.364 = Ω_c/Ω_b | ΛCDM-PROCESSED (Planck; CFG886 recovered, not pinned) | E6 L45 |
| [Fe/H] errors, MDF width, [α/Fe] | **not used by E6** | — |

## B. What L_req (the need side, inherited read-only) rests on

| ingredient | class | file |
|---|---|---|
| σ_los, r_h, M_V, distance | RAW (LVD) + SURVEY-CALIBRATION (distance moduli) | E3 |
| M_* at Υ_V = 2 | SURVEY-CALIBRATION (SPS; E1/E4 flag) | LVD `mass_stellar`, E3 |
| binary correction (Arroyo-Polonio free-f) | SURVEY-CALIBRATION | E3 |
| Wolf mass 3σ²r12/G | MODEL ASSUMPTION (equilibrium) | E3 |
| screened law B_scr, L★ = 24 pc (F1 only) | FRAMEWORK-NATIVE (L★ a fitted bound; κ = ½ FITTED); spherical self-field: AQUAL = QUMOND exactly | E3 |

## C. What this lane adds

| ingredient | class | sensitivity handled by |
|---|---|---|
| intrinsic σ_[Fe/H] from LVD (mostly Geha 2026 DEIMOS; others per `ref_metallicity_spectroscopic`) | RAW-derived summary (SURVEY-CALIBRATION) | R1 (S19), R2 (Walker per-star) |
| σ_[Fe/H] from Simon 2019 compilation (mostly Kirby+ DEIMOS synthesis, older) | RAW-derived summary (SURVEY-CALIBRATION) | R1 |
| Walker 2023 per-star [Fe/H], [Mg/Fe] (template fit, APOGEE zero point) | RAW (per-star measurements) + SURVEY-CALIBRATION (zero point) | R2; P-S; P-A |
| own Walker membership (velocity, Gaia PM/parallax, logg, radius cuts) | MODEL (declared rule) | K5; counts compared with CFG51 (reported) |
| Gaussian intrinsic-σ estimator for a skewed MDF | MODEL (estimator) | K4 |
| one-zone family extended to ζ ≥ 1 (k ≥ 0) with Z0 = 0 graded | MODEL ASSUMPTION (the conservative reading, A3) | K3 |
| homogeneous mixing; no unmixed ejecta escape (A4) | MODEL ASSUMPTION — **not testable on disk** | f_break reported |
| α yield log y_α ∈ [0, 0.18] (CFG317's O-yield statement applied to Mg) | EXTERNAL textbook | reported only |
| E6's L_req (read-only) | as B | Υ_V 1.5/2.5 line on F2 |

No ΛCDM halo mass function, concentration, r200/NFW or splashback calibration enters this lane. No standard-MOND machinery is used
(no EFE, no deep-MOND shortcut); the law enters only through E3's inherited F1 need.

## D. The rebuild brief's changes, one at a time (what each does to this lane's statistic)

| change | effect on P1 | why |
|---|---|---|
| AQUAL μ = x/(1+x), not QUMOND | none | the chemistry side has no gravity; F1's need uses the spherical self-field, where AQUAL = QUMOND exactly (E3) |
| screening, L★ ≥ 21.7/22.9 pc | already in F1 (L★ = 24 pc); F2 has none | inherited; F2 is graded |
| BS K(Q) dust, abundance an initial condition | none on L; enters the need via 5.364 (ΛCDM-PROCESSED) | q ∝ 1/5.364, as E6 |
| native H0 67.2–68.6 | none | LVD distances are distance moduli, not Hubble-flow; chemistry is distance-free |
| E1/E4 SPS M_* (Υ_V = 2) | L_req,F2 ∝ ~1/Υ; L (gas-free) independent of M_* | Υ_V 1.5 / 2.5 line reported |
