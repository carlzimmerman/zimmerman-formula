# X1_hosted_recount: assumption ledger (written before any script or number of this lane)

Classes: RAW / FRAMEWORK-NATIVE / SURVEY-CALIBRATION / ΛCDM-PROCESSED / STANDARD-MOND-MACHINERY / LITERATURE-INPUT / MODEL ASSUMPTION.
Paths are repo-relative. S1's ledger (`rebuild_2026_10_22/S1_v3_hosted_small/ASSUMPTION_LEDGER.md`) applies to every inherited row.

## A. The verdict being re-examined (tile 26, S1)

| # | ingredient | class | source | why it matters here |
|---|---|---|---|---|
| A1 | sample cut M★ < a₀(24 pc)²/G (45 / 46 systems) | FRAMEWORK-NATIVE in origin (E3/CFG820), but a **selection** | E3 `e3_dwarf_excess.py`; S1 `sample()` | Removes every classical MW dSph and the bright M31 dSphs. Q1 drops it |
| A2 | binary correction: Arroyo-Polonio free-f ratio, or the **UFD median ratio** for every unmatched system | SURVEY-CALIBRATION (population model fitted on 12 UFDs) | `campaign_fresh_gravity/CFG257_ufd_kinematics_scoping/arroyo_polonio2026_tableA1.csv` | Applied by S1's code to all unmatched systems. Here it is applied only to M_V > −7.7 (FROZEN §2) |
| A3 | T3 "hosted ⇒ dust-free ⇒ Newtonian" | FRAMEWORK-NATIVE theorem + MODEL ASSUMPTION (the system falls freely with a static host) | U1 README §T3, `u1_v3_dust_content_results.json` | Q2 books it against hosted systems that are measured |

## B. Inputs of this lane

| # | ingredient | class | source | handling |
|---|---|---|---|---|
| B1 | field equation: stiffened AQUAL, μ = x/(1+x), uniform total host field, response solved | FRAMEWORK-NATIVE (C4 literal, D10) | `doors_push_2026_10_22/D10_native_Lstar/d10_solver.py` (read-only) | L★ = 0 / floor / 24 / 90 pc |
| B2 | L★ floor 21.68 / 22.85 pc | FRAMEWORK-NATIVE fitted bound (D10) | D10, S1 | not refitted |
| B3 | σ_los, R_e (circularised), distance modulus, M_V | RAW × SURVEY-CALIBRATION (distances) | `real_research/data/dsph/lvd_dwarf_{mw,m31,local_field}.csv` (LVD, Pace 2024) | MC as S1 |
| B4 | M★ = LVD `mass_stellar` (Υ_V = 2) | SURVEY-CALIBRATION (SPS) | LVD | prior σ_logΥ = 0.15 dex in χ²; Υ 4 in W and in T3 |
| B5 | binary corrections (A2), Geha DEIMOS σ (W) | SURVEY-CALIBRATION / RAW | CFG257 files (S1's) | M_V rule (FROZEN §2) |
| B6 | Wolf estimator g = 3σ²/r₁₂, isotropic Jeans, equilibrium, sphericity, Plummer profile | MODEL ASSUMPTION | S1 `d10_solver.jeans` | E-V reported |
| B7 | host masses MW 6e10 (4e10 / Mb_hi), M31 1e11 M☉, Hernquist a_H 3 kpc, law field | SURVEY-CALIBRATION / external label + FRAMEWORK-NATIVE law | S1 (D10 A60 / CFG332 / E3) | bracket reported |
| B8 | host distances: LVD `distance_host`; `distance_m31` if missing (M31); heliocentric for the field class | SURVEY-CALIBRATION | LVD | differs from S1's code only outside E3's sample (FROZEN §2) |
| B9 | class definitions (classical 8 by name; M_V > −7.7 for UFDs; log M★ ≥ 5 for bright M31; exclusions) | MODEL ASSUMPTION (conventional labels: Simon 2019, the brief) | FROZEN §2 | fixed before any number |
| B10 | MM13 predictions, inputs and method (a₀ 1.21e-10, V_M31 230 km/s, Υ 2, r_{1/2} = 4R_e/3, min rule) | **LITERATURE-INPUT, PROVISIONAL** (web look-up) + STANDARD-MOND-MACHINERY (their formulae) | `LITERATURE_LOOKUP.md`; arXiv:1301.0822, 1308.5894 | control only (step 1). The side row in step 2 has no verdict weight |
| B11 | Crater II prediction and inputs (2.1 km/s; M 3.3e5, r_h 1066 pc, x_e 0.076, a₀ 1.2e-10) | **LITERATURE-INPUT, PROVISIONAL** + STANDARD-MOND-MACHINERY | `LITERATURE_LOOKUP.md`; arXiv:1610.06189 | control only |
| B12 | MM13 host field backed out of the printed σ_efe with μ = x/(1+x) | MODEL ASSUMPTION (μ's form is not named in the paper; checked on And I) | FROZEN §2 | makes the control input-matched; C1 reports the on-disk-distance version |
| B13 | Coma UDGs vs Newton (CFG948 z 5.45; U1 B0 z_sys 5.41) | RAW (spectroscopy) + SURVEY-CALIBRATION (SSP M/L, H₀-dependent distance) + MODEL ASSUMPTION (equilibrium) | `campaign_fresh_gravity/CFG948_nocapture_vs_udgs/cfg948_results.json`; U1 JSON | read, not recomputed |
| B14 | UMa members vs the dust-free branch (U1 A2/A4) | RAW (SPARC rotation curves) + SURVEY-CALIBRATION (Υ★, group membership) | `rebuild_2026_10_22/U1_v3_dust_content/u1_a2_field_frame_results.json` | read |
| B15 | TDGs and DF2/DF4 B0 (U1 N5) | as U1/P4 | U1 JSON | read; booked as T3-consistent |
| B16 | a₀ footings | FITTED (κ = ½) | BRIEF | never pooled; the controls use the papers' a₀ |

**Not used:** no ΛCDM-PROCESSED input (E3's catchment census 5.364 / f_ret is not used). STANDARD-MOND-MACHINERY enters only as
the published controls (B10, B11) and one side row with no verdict weight. Tides, flattening, non-equilibrium and the μ_K² term
are not modelled (S1's bound applies: ≤ 0.03 dex).
