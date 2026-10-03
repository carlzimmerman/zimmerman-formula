# CFG303 — Addendum 2 to the frozen criteria (52976ec22), written before any of the replacements below was evaluated

**What had been seen when this was written:**
- the full output of the R1/R2 run (`cfg303_rc100_cristal_LCDMFREE.out`, 15/16 checks, the S5 identity control failing);
- the inventory reports on every lane;
- the source of CFG189, CFG141 (P2/P3), CFG262 together with CFG236_common's `routes`, CFG274's loader and `gbar_of`, CFG4_clusters' table builder, and the X-COP audit's loader.

No KURVS cell with a replaced pressure model has been computed. No native MUSE-DARK, CFG274 or X-COP number has been computed.

## A2.1 KURVS (R4 made concrete)
CFG189's results hold only P0 (s = 0) and P4 (s = 1, Kretschmer) cells for the measured markers. The P2 and P3 rows there are K21-shaped placements, so LCDM-MODEL. The re-run uses CFG189's own source, exec'd up to its per-disc block: the marker loader `build`, `Sample.pred` (gbar, gpred, slope), `pooled`, `DS`, the anchor's SPARC terms and `klass`. The one replacement is the K21 coefficient `T["ak"]` (and the anchor's), swapped for CFG141's analytic prescriptions:
- **P2 (primary):** α = 2R/R_d with the measured σ(R_out).
- **P1:** α = 2R/R_d with the tabulated σ₀ in place of σ(R_out). Its error is the tabulated σ₀ error if one is present, else CFG141's.
- **P3:** α_eff = max(0, R/R_d − R·grad/σ²) with σ = σ(R_out) and CFG141's grad, the d σ²/dR of the outermost three profile points.
- **P0:** α = 0.

The SPARC anchor uses the same prescription with its declared σ = 10 km s⁻¹ (P3 there has grad = 0).

**Outputs:** the decision cell at μ = 0.67, canonical, for flat, the rival and T, with CFG160/189's class map, for the primary marker set and variants V-a to V-d and BS; and P2 break-even μ per law.

**Controls:**
- **C-i(a):** the replacement path with α = K21 reproduces CFG189's committed primary cells (s = 0 and 1) to 1e-9.
- **C-i(b):** the P2 path with CFG141's model-velocity objects (`KU2`) reproduces CFG141's committed P2 cell (μ 0.67, δ 0, canonical: +0.38989 / +0.23715) to 1e-4. This is a check that the P2 mapping into CFG189's form is right.
- **C-ii:** CFG189's exec'd pipeline reproduces its committed JSON cells.
- **C-iii MUTATE:** measured V × 10^0.1. Each disc's log g_obs term moves by the independently computed log10[(10^0.2 V² + α σ²)/(V² + α σ²)] to 1e-12, and every law's Δ′ rises.

## A2.2 MUSE-DARK (R3 resolved under R5)
The committed routes (ii)/(iii) are built in CFG236's R199 construction: g_bar = (1 − f_DM) g_perp ρ, with ρ normalised by the DC14 M_fit and the fitted Σ_HI. So they carry the halo fit's f_DM and M_fit (LCDM-MODEL). R3's no-re-run clause therefore does not apply, and the native re-run is:
- **Baryons:** g_bar,nat = CFG236's committed thin disc `g_disc(M, R_e, R_e/1.678)` with M = M★,SED (route iii) or M★,SED (1 + μ_mol) (route ii; CFG236's `mu_mol`, as committed). This is the R198-mode baryon term of `routes`.
  - **HI, primary:** none (Σ_HI = 0), because the fitted Σ_HI is a nuisance parameter of the joint DC14 fit.
  - **HI, reported:** Σ_HI = 15 M☉ pc⁻² (the prior ceiling), and the fitted Σ_HI labelled "as committed (joint-fit HI)".
- **g_obs:** CFG262's `gperp_of(reading)`, kept: the DC14 model slit velocity at R_e with the fit's inclination and, for reading bD, its dispersion. This is MODEL-OTHER with `halo_in_fit = yes`. R_e lies inside the data, which reach 2–3 R_e. No measured MUSE-DARK velocities are on disk.
- **Estimator:** CFG262's own `s_star`, `boot_s` (seeded by row label; native rows get their own labels), `pct`, the thirds `THN`, and the z3 − z1 difference with √(sd₁² + sd₃²). Readings bD (headline) and b.

**Controls:**
- **C-ii:** CFG262's exec'd machinery reproduces the committed stage-B `s` of all 18 rows to 1e-9 in log10.
- **C-i:** the native path fed the committed g_bar reproduces them.
- **C-iii MUTATE:** M★ × 10^0.2 on route (iii). Log D moves by −0.2000 exactly, and s* moves down or loses its root.

## A2.3 CFG274 (Amvrosiadis+ eight discs): the gas conversion
CFG274's gas uses α_CO = 0.92, which the source derived from the same dynamics with an assumed dark-matter fraction f_dm = 0.25. That is a ΛCDM-type assumption feeding the baryon side, so it is tagged LCDM-MODEL. The replacement rescales the gas by α/0.92 with two declared conventions already used in the record:
- α = 0.8, the ULIRG minimum conversion of CFG272/283;
- α = 4.36, the Galactic conversion of NOEMA3D/PHIBSS lanes.

These are a bracket, not a scan, and no α is preferred. Everything else stays as committed: CFG274's `gbar_of(..., gas_fac = α/0.92)`, published V_circ, and H.s_star. One reading note: Amvrosiadis's V_circ is a kinematic model without a halo (MODEL-OTHER).

**Controls:**
- **C-ii:** gas_fac = 1 reproduces each committed per-disc s and no-root flag.
- **C-iii:** gas_fac × 10^0.2 moves log g_bar,gas by exactly 0.2.

## A2.4 X-COP: the radius normalisation
In CFG4_clusters' identity reading (0.946 ± 0.080), the gas mass profile's radius is decoded from R/R500 with the gas file's R500. That R500 is NFW-derived (the audit's own docstring), so it is LCDM-MODEL. The replacement is **R500,FORW**, solved per cluster from the forward hydrostatic mass on its kpc grid: M_FORW(<R) = 500 ρ_c(z) (4π/3) R³, with ρ_c(z) in the audit's own cosmology. The audit's loader and profile builder are run with that R500 in the decode, and the CFG4_clusters table and summary functions (exec'd) are run on the resulting rows.

**Controls:**
- **C-ii:** the audit header R500 reproduces CFG4_clusters' committed identity ratio and η (canonical and alt) to 1e-9.
- **C-i:** R500,FORW := the header R500 through the replacement path reproduces it.
- **C-iii:** R500 × 10^0.2 moves the gas radius grid by exactly 0.2 dex.

If the audit code cannot be driven without writing its outputs, A2.4 is listed as **not run**, with R500,FORW / R500,NFW reported as a diagnostic.

## A2.5 Disclosed post hoc (not a replacement)
In R1, the S5 identity control (C-i for the MNRAS inversion) failed: N 100 against 99, relative difference 0.24. The cause is under test in a labelled post hoc script (`cfg303_posthoc_s5_identity.py`). The hypothesis being tested is that reconstructing f = 1 − (1 − f_DM) in floating point moves the one galaxy that sits exactly on the paper's f_DM = 0.02 window edge to inside the window. The frozen FAIL stands whatever the diagnostic finds.
