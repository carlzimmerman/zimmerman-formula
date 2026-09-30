# CFG213 — a two-sided a₀ test on DysmalPy disc–halo decompositions at z ≈ 1.4 (NOEMA3D, measured CO gas) and z ≈ 5 (ALMA-CRISTAL, dust-based gas). FROZEN CRITERIA

Written 2026-09-29 in the calculation chat, at the orchestrator's go, before any CFG213 number. **κ = ½ FITTED, NOT DERIVED.**
- The rival a₀ ∝ H(z) is larger than the local value by about 2.2 at z ≈ 1.4 and about 8 at z ≈ 5.
- CFG197's one-sided gas floor could not separate the laws.
- The authors' own baryon–halo decompositions give D = g_obs/g_bar at a stated radius. That can be compared in BOTH directions with ν(g_bar/a₀(z)).

## Exposure, disclosed

- **CFG197:** its ledger row and the first 25 lines of its README (the phase-2 bottom line, bin medians only), and its FROZEN_CRITERIA. These include the CRISTAL paper's median f_DM(<R_e) ≈ 18% (5–60%) and median f_molgas 0.51. Its phase-2 `.out` and `_results.json` were NOT opened.
- **`data_assembly/INVENTORY_2026-09-29.md` line 13.**
- **The data chat's NOEMA3D messages and README (a53b74ff7):**
  - median f_DM 0.21 and V_c range 197–379 km/s;
  - log(M* + M_gas) minus the fitted log M_bary: within 0.1 dex for 7 of 10, +0.41 for GN4_18574, −0.32 for G4_20371.
- **A table peek.** While reading the CRISTAL dynamics-table footnotes in the paper's TeX source (outside the repo), the table's last two rows were displayed:
  - 23b: log M 9.8, R_e 1.4 kpc, V_rot(R_e) 93.3 km/s, σ₀ 66.8 km/s, f_DM 0.57;
  - 23c: log M 9.2, R_e 0.4, V_rot 114.4, σ₀ 56.5, f_DM 0.53.
- **The CRISTAL definitions** come from a read-only agent that reported no velocities, accelerations or f_DM values.
- Nothing else per galaxy was seen.

## Data and definitions (as read)

**ALMA-CRISTAL** (arXiv:2507.11600; `data_assembly/arxiv_tables/cristal2025_*.csv`, `cristal_vector/`)
- **The fit.** DysmalPy fits four free parameters: M_bary, R_e,disk, f_DM(<R_e,disk) and σ₀. M_bary has a Gaussian prior of **1 dex** centred on M* + M_gas(dust). That is effectively free, and it is fitted jointly with the halo.
- **Pressure.** V_rot² = V_circ² − 3.36 σ₀² (R/R_e) (Burkert+2010; paper eq. `dy_pressure_support`).
- **Table quantities.** The table's V_rot(R_e) is that pressure-free rotation velocity. The table's column (a), "log M_tot", is read as the fitted M_bary, the first free parameter. That reading is stated as an assumption.
- **f_DM(<R) = V_DM²(R) / V_circ²(R).**
- **Gas.** f_molgas = M_gas/(M_gas + M*), dust-based (T_d = 50 K).
- **Sample Z5.** The 14 vector disks.
  - **Primary: 12.** CRISTAL-09 and -15 are EXCLUDED, because their vector curves disagree with the paper's table (−15 also has a fixed R_e that its figure contradicts). They are reported separately.
  - **Route variant:** the galaxies with both M* and f_molgas, i.e. the 12 minus 10a-E, 23c and 06b.

**NOEMA3D** (Jolly+2026; `data_assembly/noema3d/noema3d_per_galaxy.csv`, 10 galaxies, z 1.12–1.63)
- DysmalPy: V_c and f_DM at R_e,disk (photometric, fixed), a fitted log M_bary, and σ₀.
- The CO gas is MEASURED (α_CO 4.36).
- V_c is read as the circular velocity with DysmalPy's default Burkert pressure term (A-N1: not stated in the pages read).

## Quantities, per galaxy, at R = R_e,disk (primary)

- D_obs = 1/(1 − f_DM(R_e)), the model's own ratio.
- g_obs = V_circ(R_e)²/R_e, with V_circ² = V_rot² + 3.36σ₀² for CRISTAL and V_circ = V_c for NOEMA3D.
- g_bar = g_obs/D_obs.
- **Laws:**
  - flat: a₀ = A0_f;
  - rival: a₀ = A0_f E(z), with Ω_m = 0.315;
  - footings f ∈ {canonical 9.36e-11, alt 1.131e-10};
  - kernels: **ν_mono (primary, the 09-26 user decision)** and P2 (variant).
- D_pred,L = ν(g_bar/a₀,L), and **δ_i,L = log₁₀(D_obs/D_pred,L)**.

## Statistic and decision rows

- **Statistic.** Per bin (Z1.4 = NOEMA3D, Z5 = CRISTAL primary): the median δ over galaxies, with a 95% CI from 10,000 bootstrap resamples (seed 213).
- **Verdicts:**
  - CONSISTENT if the CI contains 0;
  - DISFAVOURED-over if the CI > 0: the law predicts LESS discrepancy than the decomposition;
  - DISFAVOURED-under if the CI < 0.
- **Robust** means the same verdict across both footings, both kernels and pressure α ∈ {3.36, 1.68}.
  - Varying the pressure: V_circ,α² = V_rot² + α σ₀² for CRISTAL, and V_c² − (3.36 − α)σ₀² for NOEMA3D. g_bar is held at the fitted value.
  - α = 0 is reported only.
- **H1 (Z5) and H2 (Z1.4):** "the decompositions separate the laws" iff exactly one law is robustly DISFAVOURED in that bin. The row reports which law, and the sign.
- **Mass-route variant** (the headline limitation, as in CFG198/199; reported beside the primary, never substituted):
  - g_bar,ind = g_bar × M_ind/M_bary,fit;
  - M_ind = M*/(1 − f_molgas) for CRISTAL, and M*_SED + M_gas,CO for NOEMA3D;
  - δ is recomputed from it.
  - If the route variant flips a primary verdict, the verdict is labelled "route-dependent".
- **Also reported:**
  - CRISTAL at the vector's `table_Rout` and `outermost_data_marker` radii: D = V_tot²/V_bary² from the model curves, where beyond the last marker the curve is extrapolation;
  - CRISTAL-09 and -15 separately;
  - the Best-Disk subset;
  - per-galaxy g_bar/A0, D_obs and D_pred for each law.
- **Language.** A "flat DISFAVOURED-over" verdict is reported as a failure of the BARE flat law on these decompositions. B's cold component is not modelled here and is not invoked. No sentence says the data favour the framework.

## Controls

- **C1.** The kernel round trip holds to 1e-9 for ν_mono and P2.
- **C2.** A synthetic galaxy placed exactly on each law returns δ = 0 to 1e-12.
- **C3 (reported).** At R_e, the vector's V_tot²/V_bary² against the table's 1/(1 − f_DM), and the vector's V_tot(R_e) against (V_rot² + 3.36σ₀²)^½.
- **MUTATE=1.** Every D_obs × 1.5. Every bin's median δ must rise by log₁₀1.5 to 1e-9. Outputs are written separately.

## Hand expectation, disclosed

- The stated medians put D near 1.2–1.3 at both redshifts. These are compact, massive discs, with g_bar at several a₀.
- So I expect the bare flat law to under-predict D (possibly DISFAVOURED-over), and the rival to sit closer at z ≈ 1.4 and possibly over-predict at z ≈ 5.
- CRISTAL's 1-dex prior makes the mass route the likely deciding systematic there.
