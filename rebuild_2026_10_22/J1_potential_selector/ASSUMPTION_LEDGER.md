# J1_potential_selector — assumption ledger (before any number; committed with the frozen criteria)

Classes: RAW / FRAMEWORK-NATIVE / SURVEY-CALIBRATION / ΛCDM-PROCESSED / STANDARD-MOND-MACHINERY / EXTERNALLY-CALIBRATED /
POSTULATED (new in this lane).

| # | ingredient | class | source | note |
|---|---|---|---|---|
| J1 | a₀_eff = a₀(1 + \|Φ\|/Φ_*), Φ_ref = 0 | **POSTULATED** (+1 function, +1 constant φ_*) unless Part A finds it in the action | this lane | form frozen before looking |
| J2 | Φ = Newtonian potential of the baryons, zero at infinity | POSTULATED choice (gauge-fixed) | this lane | law's log potential needs a 2nd constant: not used |
| J3 | pointwise a₀_eff inside spherical AQUAL (no dA₀/dΦ field-equation term) | POSTULATED (phenomenological) | this lane | an EMOND-type Lagrangian adds a term ∝ dA₀/dΦ; not modelled, stated |
| J4 | KiDS shear, eRASS1 catalogue, estimator, β-model gas, f* 0.20, native h, gas rescale, boost, miscentring | as F1 ledger (RAW / SURVEY-CAL / ΛCDM-PROCESSED R500) | `rebuild_2026_10_22/F1_cluster_cores/ASSUMPTION_LEDGER.md` | inherited unchanged; R500 stays ΛCDM-PROCESSED |
| J5 | AQUAL μ = x/(1+x), spherical | FRAMEWORK-NATIVE (E2, C4) | F1 `g_aqual_sph` | |
| J6 | SPARC rotmod V_obs, eV, V_gas, V_disk, V_bul; Υ_d 0.5, Υ_b 0.7 | RAW × SURVEY-CALIBRATION (Υ) | `real_research/data/sparc_data/`, CFG914 loader | |
| J7 | SPARC potential: spherical ∫g_bar dR + Keplerian tail | EXTERNALLY-CALIBRATED approximation | this lane | disc potential differs by O(10–30 %) from spherical |
| J8 | RAR σ floor 0.10 dex | assumed (Υ, distance, inclination) | this lane | 0.05 dex reported |
| J9 | dwarf satellites: σ, r_h, M*, binaries, MC, B_scr(L★ 24 pc) | as E3 ledger | `doors_push_2026_10_22/E3_dwarf_excess/e3_inputs_ledger.csv` | inherited |
| J10 | distance_gc, distance_m31 | RAW × SURVEY-CAL (distances) | LVD csv files | |
| J11 | MW baryons 6.0e10 M☉ (CFG332), M31 1.0e11 M☉ (E3/D2), Hernquist a = 3 kpc (D10/A60) | EXTERNALLY-CALIBRATED (star counts / SPS) | CFG332, E3, D10 | point-mass variant reported |
| J12 | TDG host mass from L15's g_Ne (their a₀ = 1.30e-10) and projected D_p | EXTERNALLY-CALIBRATED; \|Φ\| an upper bound | `real_research/data/tdg/lelli2015_tdgs.csv` | |
| J13 | C6 margins (planets 0.173 Mars at 24 pc; Q₂ ≤ 3.6e-8 of Park; γ_v − 1 = 8.1e-6) and conservative ε, ε² scalings | FRAMEWORK-NATIVE (computed in C6) × assumed scaling | `covariant_push_2026_10_22/C6_literal_cassini/README.md` | no solver rerun |
| J14 | κ = ½ | FITTED | | |
| J15 | v3/v4 static Lagrangians for Part A | literature (BS24, SZ21) as transcribed in C4 / H2 (BS24 PROVISIONAL, WebFetch; SZ21 on disk) | C4, H2 | sympy re-derives the identities used |
