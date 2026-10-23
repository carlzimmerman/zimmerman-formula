# Z2_satellite_systematics: assumption ledger (written before any script or number of this lane)

Classes: RAW / FRAMEWORK-NATIVE / SURVEY-CALIBRATION / ΛCDM-PROCESSED / STANDARD-MOND-MACHINERY / MODEL ASSUMPTION.
Paths are repo-relative.

## A. Ingredients of the verdicts being reconciled

### S1 / T1 / U1 (the +1.33 / +2.0 dex excess and T1's tracking slope)

| # | ingredient | class | source | note |
|---|---|---|---|---|
| A1 | σ_los, mostly single-epoch | RAW | `real_research/data/dsph/lvd_dwarf_{mw,m31,local_field}.csv` | binaries inflate |
| A2 | Arroyo-Polonio free-f / f = 0.7 binary ratios; median ratio for the unmatched | SURVEY-CALIBRATION (population model) | `campaign_fresh_gravity/CFG257_ufd_kinematics_scoping/arroyo_polonio2026_tableA1.csv` | 8 of 45 system-specific |
| A3 | DEIMOS σ (Geha 2026 II), W's "lower σ" | RAW | `CFG257_ufd_kinematics_scoping/geha_vs_lvd_match.csv` | |
| A4 | R_e, distance modulus | RAW × SURVEY-CALIBRATION | LVD | |
| A5 | M★ at Υ_V = 2 | SURVEY-CALIBRATION (SPS) | LVD `mass_stellar` | W uses Υ_V = 4 |
| A6 | Wolf-type g_obs = 3σ²/r₁₂; Plummer, equilibrium, isotropy | MODEL ASSUMPTION | E3, S1 | tides/non-equilibrium are what this lane tests |
| A7 | stiffened AQUAL solver, μ = x/(1+x), L★ floor 21.68 / 22.85 pc | FRAMEWORK-NATIVE (L★ a fitted bound) | `doors_push_2026_10_22/D10_native_Lstar/d10_solver.py` | read-only |
| A8 | host = uniform total field; MW Hernquist 6e10 M☉ (E_lo 4e10, E_hi from E2's 8 kpc total), a_H 3 kpc; M31 1e11 | SURVEY-CALIBRATION masses + FRAMEWORK-NATIVE law field; M31 mass an external label | S1 | tidal gradients neglected (MODEL ASSUMPTION) |
| A9 | Leo T: MW field at its heliocentric distance | MODEL ASSUMPTION | S1 | a field dwarf given a host field |
| A10 | U1 B0: a falling satellite carries no held dust → Newtonian | FRAMEWORK-NATIVE (U1 theorem T3) | U1 | |
| A11 | T1 ε: multiplier on the host field; tracking = OLS of central residual on log x_e, bootstrap over systems | diagnostic (not a theory) | T1 | no measurement error propagated in the slope |

### CFG838 / CFG839 (no tidal signal)

| # | ingredient | class | source | note |
|---|---|---|---|---|
| B1 | sample: CFG828's 29 pressure-supported dwarfs (24 with a host) — classical and bright M31 dSphs | sample choice | `campaign_fresh_gravity/CFG828_dwarf_excess_rotation_vs_dispersion/cfg828_results.json` | overlaps S_E3 in only a few systems |
| B2 | Δ = log g_obs/g_law, isolated ν_e law, no EFE | FRAMEWORK-NATIVE kernel of the old chain (not v3's) | CFG828 | |
| B3 | Υ_SFH (E-MILES Kroupa × Weisz+14 SFHs) | SURVEY-CALIBRATION (SPS) | `campaign_fresh_gravity/CFG827_dwarf_age_sfh_ml/cfg827_results.json` | |
| B4 | literature σ (no binary correction) | RAW | CFG828 | |
| B5 | host field: law (ν_e) on a point mass, MW 6e10 / M31 1e11 (1.5e11 bracket) | SURVEY-CALIBRATION masses + old kernel | CFG838/839 | not S1's Hernquist μ = x/(1+x) field |
| B6 | T = |dg_host/dD| r₁₂ / g_int, g_int = law field of the stars | definition | CFG838 | shares the internal field with Δ |
| B7 | pericentres: astropy default Galactocentric frame, Gaia PMs from LVD, spherical static MW | RAW (PMs) + SURVEY-CALIBRATION (solar motion) + MODEL ASSUMPTION (no LMC, static) | CFG839 | |
| B8 | statistic: one-sided Spearman ρ | — | CFG838/839 | |

## B. Ingredients of this rebuild

| # | ingredient | class | source | handling |
|---|---|---|---|---|
| R1 | data side, sample rule, MC/bootstrap | as A1–A6 | own code (E3/S1 conventions) | K1, K2 reproduce E3/S1 first |
| R2 | flavors V3S / V3D / MOND (+ ISO, V3S0) | FRAMEWORK-NATIVE (A7, A10); MOND = the same AQUAL at L★ = 0, a comparison flavor, not a yardstick | D10 solver read-only | |
| R3 | MW field for orbits = S1's host field (μ = x/(1+x) law on Hernquist), E_mid; E_lo / E_hi bracket | SURVEY-CALIBRATION masses + FRAMEWORK-NATIVE law | S1 | no ΛCDM halo |
| R4 | Galactocentric frame (astropy default: R₀ 8.122 kpc, z☉ 20.8 pc, v☉ (12.9, 245.6, 7.78) km/s) | SURVEY-CALIBRATION | astropy 7.2 | as CFG839 |
| R5 | PMs, v_los, distances | RAW (Gaia PMs, spectroscopy) + SURVEY-CALIBRATION (distances) | LVD | MC over quoted errors |
| R6 | static spherical host, no LMC, no dynamical friction, no orbital decay | MODEL ASSUMPTION | — | LMC-associated satellites' pericentres are approximate |
| R7 | King tidal radius at pericentre, r_t³ = G m_F/(Ω_p² − Φ''); m_F = flavor's own mass | MODEL ASSUMPTION (instantaneous King radius; m_F extended beyond r₁₂ with the r₁₂ boost) | — | V3D (m = M★) is the strictest reading |
| R8 | thresholds q < 0.5 (safe), ε < 0.5, N_q ≥ 10, gradient p < 0.01, N_clean ≥ 6 | frozen choices | FROZEN_CRITERIA | not tuned |
| R9 | ellipticity | RAW (photometry) | LVD | intrinsic UFD flattening is common: weak tidal indicator |
| R10 | per-star velocities and positions, membership | RAW (Walker et al. 2023, J/ApJS/268/19) + CFG51's frozen member rule | `real_research/data/walker2023/`, `campaign_fresh_gravity/CFG51_walker_multiepoch/reduce_walker.py` (read-only) | only systems with ≥ 10 members |
| R11 | member counts | RAW (Geha 2026 II Table A1; Collins 2013; Arroyo-Polonio Table A1) | `CFG257_ufd_kinematics_scoping/`, `real_research/data/dsph/collins2013_m31_dsph.tsv` | proxy N_eff = ½(σ/δσ)² elsewhere |
| R12 | UFD boundary M_V = −7.7 | convention (Simon 2019; CFG51) | — | |
| R13 | a₀ footings | FITTED (κ = ½) | BRIEF | never pooled |

**Not used anywhere in a verdict line:** ΛCDM-processed inputs (no NFW/ΛCDM MW halo, no published ΛCDM-potential
pericentres such as Pace+2022's, no halo masses, no f_ret / 5.364 census). No QUMOND/EFE recipe: every prediction is the
solved AQUAL response. Native H₀ does not enter (stellar distances).

**Data not on disk (listed, not fetched):** published velocity-gradient and stream-association flags for UFDs (e.g.
the gradient compilations in Martínez-García et al. 2021, A&A 647, A167 and in the per-system discovery papers);
per-star data for the non-Walker datasets (DEIMOS, IMACS, GMOS); Gaia-based PMs for M31 satellites (none in LVD).
