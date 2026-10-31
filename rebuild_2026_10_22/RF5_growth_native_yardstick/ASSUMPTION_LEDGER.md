# RF5_growth_native_yardstick: ASSUMPTION LEDGER (committed with FROZEN_CRITERIA.md, before any script or number)

Classes as in X5: RAW / FRAMEWORK-NATIVE / SURVEY-CALIBRATION / ΛCDM-PROCESSED / STANDARD-MOND-MACHINERY / LITERATURE-INPUT. POSITED marks this lane's reading.

| # | item | class | note, where it could bite |
|---|---|---|---|
| A1 | κ = ½ | FITTED | reads a₀ off the surface; does not enter the χ² |
| A2 | a₀ absent from linear FRW | FRAMEWORK-NATIVE (Q6 D0, X34 A3) | both footings share one surface by construction; say so in every table |
| A3 | Footing values 9.3603e-11, 1.1312e-10 | ΛCDM-PROCESSED provenance (computed on a Planck-like background) | shown for comparison, never graded |
| A4 | GR background; the switch acts only in bound systems | POSITED, framework (CFG654, X54 A1) | if the switch acts on the background the fit changes |
| A5 | CLASS v3.3.4 Boltzmann code; HyRec; BBN Y_He table at the fitted ω_b; 3.044 massless ν; adiabatic power-law primordial spectrum; tanh reionization; linear CMB lensing | STANDARD PHYSICS inherited (X54 A6). The primordial form is a choice with ΛCDM-era use, not ΛCDM-fitted | no parameter value is inherited; all are fitted per cell |
| A6 | Turn-on: w = −1 reservoir, δQ = 0 on synchronous slices, tanh width 0.05 | POSITED (X34 A9) | an adiabatic (temperature-keyed) release is not run: disclosed gap; other readings could differ |
| A7 | CPL for ρ_DE(z) | POSITED parametrisation; CFG689's nodes are not a CLASS input | graded against CFG689's band by G-A0 |
| A8 | CFG689 band | FRAMEWORK-NATIVE (raw BAO + SN + pre-switch ruler); its A1 audit brackets the CMB ω_b, ω_c input (B8) | wide at z 2.33 |
| A9 | plik-lite TTTEEE, low-ℓ TT, low-ℓ EE | SURVEY-CALIBRATION: Planck's compressed, foreground-marginalised product (X54 A7), built with Planck's foreground model. Raw Planck maps or full Plik and ACT/SPT spectra are not on disk | foreground model assumptions; PROVISIONAL whether a cosmological model conditioned the compression |
| A10 | τ steering prior (C2, 0.0510 ± 0.0085) | steering only (X54 A8) | never in a graded χ² |
| A11 | C7's ΛCDM refit parameters | ΛCDM-PROCESSED, first start point only; K2 uses them as a harness check | no effect once converged; the Stop rule's unconverged cells would be flagged |
| A12 | DESI DR2 D/r_d | SURVEY-CALIBRATION, built with a fiducial template (CFG689 P4: inside tested span, ≤ 0.1 %) | r_d from each cell's CLASS |
| A13 | DES-SN5YR Dovekie Hubble diagram, M marginalised | SURVEY-CALIBRATION (Tripp standardisation) | one SN set only |
| A14 | DES Y3 ξ+ values | RAW two-point measurement | 2pt_maglim file; same shear catalogue as redmagic file |
| A15 | DES Y3 covariance | SURVEY-CALIBRATION with a ΛCDM-fiducial analytic covariance: **ΛCDM-PROCESSED ingredient, used as the noise model** | no raw-noise alternative on disk. At low amplitude it overstates the error, so it is generous to a low-growth model |
| A16 | n_i(z) sources, m_i, Δz_i priors | SURVEY-CALIBRATION; m_i, Δz_i as published (DES Y3 shear papers), LITERATURE-INPUT PROVISIONAL (from recollection of the published tables, not read in this lane) | marginalised linearly |
| A17 | NLA intrinsic alignment, C1ρ_crit = 0.0134 | LITERATURE-INPUT | A_IA free, so the normalisation is degenerate with A_IA |
| A18 | Limber, linear P(k,z), scale cut k_NL = 0.2 h/Mpc at 20 % | POSITED; the non-linear gap is unfilled by design, since the record's boosts are ΛCDM-calibrated | linear P underpredicts kept points by less than the cut; if it costs χ² at all cells G-SHEAR fails everywhere and this is reported as a model gap |
| A19 | DESI DR1 P1D | RAW flux power, SURVEY-CALIBRATION in its corrections (metals, resolution, continuum) | per-z blocks; cross-z dropped (mean r 5e-4, P1D4) |
| A20 | Lognormal + FGPA + linear Kaiser + thermal broadening (forest3d) | FRAMEWORK-NATIVE modelling proxy, no hydro simulation | inadequate at z ≤ 2.6 (P1D4), and marginal above; G0 can make the channel NOT DIAGNOSTIC |
| A21 | F̄ free; V-Fbar with Becker+13 | LITERATURE-INPUT for V-Fbar only, PROVISIONAL (from recollection) | Becker's calibration has a simulation-assisted zero point; reported only |
| A22 | b free 6–35 km/s, 2 % floor | POSITED (P1D4 V-floor2) | |
| A23 | Line 25 in G-S; p ≥ 1e-3 gates | RECORD (C2) and POSITED | absolute gates are lenient on an N ≈ 600 χ²: the reason G-S exists |
| A24 | S_min is this family's own minimum | FRAMEWORK-NATIVE | the dust limit is in the family, so numerically S − S_min near the dust limit resembles a dust-limit reference. That reference has CPL and native values, not ΛCDM's |
| A25 | v3s rows at μ_K = 0.03, 0.1 Mpc⁻¹ | RECORD (S4, X4) | khronon fluid equations as Q6's patch; ω_cdm 1e-8 |
