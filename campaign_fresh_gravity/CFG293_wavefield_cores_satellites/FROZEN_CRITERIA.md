# CFG293 -- CFG288's wave field: solitonic cores and the satellites: frozen criteria

Written before any CFG293 script existed and before any satellite number with a core was computed. Paths are relative to the repository root.

Standing statements, binding on every sentence of the lane: kappa = 1/2 is FITTED, not derived. No dark-matter species is added by hand: the cold component here is CFG288's road-W field, a classical field whose quanta would be light bosons, and **the cold mass is still required** (its amount is free in CFG288; the collapse mass comes from the record's declared stellar-to-halo relation). Nothing here says the data favour the framework, or that the theory is closed. A FAIL or a STOP is a valid outcome.

---

## 0. What was read before freezing (not-blind statement)

**Read:**
- `campaign_fresh_gravity/CFG288_one_field_dark_sector/README.md` (whole): road W (linear complex field, V = rho_Lambda + m^2 |Phi|^2) passes the behaviour gates; m is not derived; window [2e-20 eV, 37 eV]; G-PK set at m >= 2e-20 eV; L383's 2-5e-19 eV floor reported.
- `campaign_fresh_gravity/CFG286_satellite_tidal_stripping/FROZEN_CRITERIA.md` and `README.md` (whole). Its finding: stripping is inert at the estimator radius; lowering the classicals needs lower inner cold density at r ~ r_half.
- `campaign_fresh_gravity/CFG45_README.md`; `CFG45_rule_readings.py` up to the end of the P2 block (the estimator `sigma_read`, `extra_acc`, `km_median`, `boot`, the P1/P2 statistics); the first 140 lines of `cfg286_tidal_stripping.py` (how it exec's CFG45's prefix).
- `hunt_2026/h48_h69b_relative_isolation.py` lines 1-139 (`moster_mstar`, `halo_mass`, `_RHO_C`, `nfw_enclosed`, with its clip at r/R200 >= 1e-4); `CFG7_common.Report`; `CFG4_common.exec_slices`; `CFG35_cold_mass_conservation.py` lines 55-70 (FB, how h48 is exec'd).
- `campaign_fresh_gravity/CFG259_ufd_variants_rescore/README.md` (bottom line and first table).
- **The record's committed aggregate numbers** in `CFG45_rule_readings_results.json` (readings L and S only, both footings): UFD KM median L +0.3245 / +0.3045, S -0.0586 / -0.0591 (tot err S 0.1431 / 0.1456); MW classical S -0.1183 / -0.1233; M31 LVD L +0.0435 / +0.0308, S -0.1069 +- 0.0401 / -0.1086 +- 0.0409; Collins+13 S -0.0240 / -0.0161. These are the numbers already quoted in CFG286; they set the thresholds of section 5.
- **Literature (arXiv pages only, read through a summariser, so PROVISIONAL; no PDF fetched):** Schive, Chiueh & Broadhurst 2014, Nature Physics 10, 496, arXiv:1406.6586 (abstract page); Schive, Liao, Woo, Wong, Chiueh, Broadhurst & Hwang 2014, PRL 113, 261302, arXiv:1407.7762 (abstract page and the ar5iv HTML rendering, equations read twice from two URLs). The relations used are quoted in section 3.2.

**Not seen:** any satellite offset computed with a soliton core; no per-satellite number of any kind beyond the aggregates above.

**Pre-freeze hand arithmetic** (a calculator in a scratch file outside the repository, generic systems only, Schive's eq. 3 fit for the profile, and k = 0.49 for the velocity form, taken from my memory of the soliton energy constant, not from a source). Results in section 8.

---

## 1. The question (as directed, frozen)

CFG288's only one-field construction that passes the behaviour gates is a linear complex wave field with V = rho_Lambda + m^2 |Phi|^2 and m undetermined in [2e-20, 37] eV. A linear wave field forms a solitonic core (the Schrodinger-Poisson ground state) at the centre of every self-gravitating system. **Does this core physics, at a declared m in the window, move the cold mass inside r_half in the direction the satellites need (UFDs keep or gain their cold core; M31 LVD dwarfs lose cold mass inside r_half), or the wrong way?** The pre-flight decides whether CFG286's harness is run at all.

## 2. The m rows (declared, never fitted, never scanned for a verdict)

| row | m (eV) | role |
|---|---|---|
| D1 | 2e-20 | decision row (CFG288's G-PK floor) |
| D2 | 1e-19 | decision row |
| D3 | 1e-18 | decision row |
| D4 | 1e-17 | decision row |
| R-top | 37 | reported; the window's top; also the mass of MUTATE=2 |
| R-out | 1e-22 | reported; **OUTSIDE the window** (excluded by CFG288's G-PK); used only by the instrument control C-SIGN and the R-edge diagnostic; it can never open a window |

## 3. The soliton relations and their sources

### 3.1 Schrodinger-Poisson ground state (derived here; primary profile)

Field normalised so that rho = |psi|^2 (mass density): i hbar d_t psi = -(hbar^2 / 2m) lap psi + m Phi psi, lap Phi = 4 pi G |psi|^2. Stationary state psi = exp(-i mu t / hbar) sqrt(rho0) chi(x), r = L x, Phi = (hbar^2 / m^2 L^2) V, mu = (hbar^2 / m L^2) E, with L = (hbar^2 / (4 pi G rho0 m^2))^(1/4). Then

  chi'' + (2/x) chi' = 2 (V - E) chi,   V'' + (2/x) V' = chi^2,   chi(0) = 1, chi'(0) = 0, V(0) = 0, V'(0) = 0,

and E is found by shooting (bisection) for the nodeless solution with chi -> 0. Definitions: x_c from chi(x_c)^2 = 1/2 (half-density radius, as Schive's r_c); I(x) = x^2 V'(x) = int_0^x chi^2 x'^2 dx'; I = I(infinity); T = int chi'^2 x^2 dx; J = int I(x) chi^2 x dx. Exact consequences:
- M_sol(<r) = 4 pi rho0 L^3 I(r/L); M_sol r_c = (I x_c) hbar^2 / (G m^2); rho0 r_c^4 = x_c^4 hbar^2 / (4 pi G m^2).
- Virial: 2K + W = 0 is T = J.
- The soliton's own 1D mass-weighted dispersion sigma_sol^2 = |W| / (3 M_sol) gives **r_c = k hbar / (m sigma_sol), k = x_c sqrt(J / (3 I))**.
- The profile is used out to x_max, the radius where chi^2 <= 1e-12 or the shooting solution departs (whichever comes first); beyond x_max the soliton density is set to 0.

### 3.2 Schive+14 relations (PRL 113, 261302, arXiv:1407.7762; read twice via ar5iv; PROVISIONAL)

- eq. 3 (profile fit; used only in controls): rho_c(x) = 1.9 a^-1 (m / 1e-23 eV)^-2 (x_c / kpc)^-4 / [1 + 9.1e-2 (x / x_c)^2]^8 Msun pc^-3, "accurate to 2% in the range 0 <= x <~ 3 x_c". x_c is the radius where the density drops to half its peak. M(<= 3 x_c) is about 95% of the total soliton mass; the half-mass radius is about 1.45 x_c.
- eq. 6 (core mass, used only in a control): M_c = (1/4) a^-1/2 (zeta(z)/zeta(0))^(1/6) (M_h / M_min,0)^(1/3) M_min,0, M_min,0 ~ 4.4e7 m22^-3/2 Msun; M_c is the mass enclosed within x_c.
- eq. 7 (core-halo radius, the F-H form): r_c = 1.6 m22^-1 a^(1/2) (zeta(z)/zeta(0))^(-1/6) (M_h / 1e9 Msun)^(-1/3) kpc, m22 = m / 1e-22 eV.
- The halo virial mass: M_h = (4 pi x_vir^3 / 3) zeta(z) rho_m0, zeta(z) = (18 pi^2 + 82 (Omega_m(z) - 1) - 39 (Omega_m(z) - 1)^2) / Omega_m(z).

### 3.3 The two core-radius forms (both declared; both run)

- **F-H (halo form):** eq. 7 at a = 1 (z = 0: the largest core eq. 7 gives, the most generous to biting). M_h = the record's collapse halo (h48's `halo_mass`, M_200c, Dutton-Maccio NFW) converted to Schive's virial mass with the same NFW profile: the radius where the mean enclosed density equals zeta(0) rho_m0, Omega_m = 0.3153 (CFG7's), rho_crit = h48's `_RHO_C`. The density normalisation comes from 3.1 (rho0 r_c^4 = x_c^4 hbar^2 / (4 pi G m^2)), not from eq. 3.
- **F-V (velocity form, the brief's r_c ~ hbar / (m sigma)):** r_c = k hbar / (m sigma), k from 3.1, sigma = the generic system's observed 1D dispersion (the identification sigma_sol = sigma_obs is declared). Normalisation from 3.1.

### 3.4 The composite cold profile (two declared prescriptions)

The envelope is the record's NFW (M_c, Dutton-Maccio c(M_200c), h = 0.674, R200 from h48's `_RHO_C`), evaluated analytically without h48's clip (control C-NFW).
- **P-C (continuity):** r_eps = the outermost radius at which rho_sol = rho_NFW with rho_sol > rho_NFW just inside it (searched on (1e-4 r_c, x_max L]). If rho_sol > rho_NFW still at x_max, r_eps = x_max L. If rho_sol never exceeds rho_NFW, r_eps = 3 r_c (flag "no crossing").
- **P-3 (fit range):** r_eps = 3 r_c, eq. 3's stated range.
- In both: rho = rho_sol for r < r_eps and rho_NFW for r >= r_eps, so M_comp(<r) = M_sol(<min(r, r_eps)) + max(0, M_NFW(<r) - M_NFW(<r_eps)).
- The whole composite carries the record's factor f_ex (1 - f_b), as the NFW does in reading S. **The pre-flight observable is therefore independent of f_ex, f_b and the footing (a0 never enters).**

### 3.5 The pre-flight observable

q = [M_comp(<r_ev) - M_NFW(<r_ev)] / M_NFW(<r_ev), at r_ev = (4/3) r_half (FG001's estimator radius). q < 0: the core removes cold mass where the dispersion is measured; q > 0: it adds cold mass. q = 0 is reading S.

## 4. Generic systems (not the samples)

- **G-U (UFD):** sigma = 3 km/s, r_half = 30 pc (r_ev = 40 pc), M_* = 1e4 Msun -> M_c = halo_mass(1e4) (the record's clamp, 1e9 Msun). Reported: M_c at the record's floors 1e8, 3e8, 3e9, 1e10 Msun.
- **G-C (classical / M31):** sigma in {8, 10, 12} km/s, r_half in {200, 500, 1000} pc, M_* in {1e6, 1e7} Msun -> M_c = halo_mass(M_*). 18 systems (F-H does not use sigma).

## 5. The pre-flight decision rule (frozen)

**Thresholds (derived from the record's committed aggregates, section 0):**
- **Classical bite:** q <= -0.116. For the M31 LVD median (-0.1069 +- 0.0401 canonical) to reach -2 sigma, sigma_pred must fall by >= 0.0267 dex, so g by >= 0.0534 dex (11.6%); the cold mass must then fall by at least 11.6% even if it carried all of g. (Alt: 11.6%.) This is generous: with the aggregate cold share s_M31 = 1 - 10^(-2 (0.0435 + 0.1069)) = 0.50 the realistic need is about 23%.
- **UFD spared:** q_UFD >= -0.50. With the aggregate cold share s_U = 1 - 10^(-2 (0.3245 + 0.0586)) = 0.83, losing half the cold mass moves the UFD KM median by about +0.12 dex, within 1 sigma of S. Generous.

**Rule:** a RIGHT-SIGN WINDOW exists iff, for at least one decision row D1-D4, one form (F-H or F-V) and one prescription (P-C or P-3), BOTH (i) at least one G-C system has q <= -0.116, and (ii) G-U (M_c = 1e9) has q >= -0.50 under the same form and prescription. The most generous reading is deliberate: a NO is then robust to every declared choice.

- **If NO WINDOW: STOP.** CFG286's harness is not run, no satellite is scored with a core, and the harness-level MUTATE (below) has nothing to control and is not run.
- **If a WINDOW exists:** run the harness of section 6 at every decision row (each a separate declared row).

**Reported beside the rule (never a verdict):**
- per row: r_c, rho_c, M_sol, r_eps / r_c, q for G-U and the range of q over G-C, per form and prescription;
- scaling statements: r_c / r_half ratio between G-C and G-U;
- R-floor: G-U at the record's collapse-mass floors;
- R-Mh: F-H with M_h = M_200c directly, and with M_h / 3 (a cold halo of f_ex (1 - f_b) >= 1/3 of M_c);
- R-edge: for each form and prescription, the largest m in [1e-24, 2e-20] eV at which some G-C system reaches q <= -0.116 (bisection in log m where bracketed), with G-U's q at that m, and the number of decades below the window floor;
- the aggregate translation (labelled approximate, not a harness score): delta KM median of the UFDs ~ -0.5 log10(1 + s_U q_UFD); delta M31 LVD median ~ -0.5 log10(1 + s_M31 q_GC), with s_U = 0.83 and s_M31 = 0.50 as above.

## 6. The harness (run only if a window exists)

- **Machinery:** CFG45's committed prefix exec'd read-only exactly as CFG286 does (source up to `FLOORS = (1e8, 3e8, 1e9, 3e9, 1e10)`), giving the samples (P1 31 + 9 limits, P2 14, P3 34, P4 14), `a_int`, `infall_gas`, `halo_mass`, `nfw_enclosed`, `FB`, `edge_info`, `km_median`, `boot`. CFG286's own file is not modified.
- **Estimator:** sigma^2 = g r_ev / 3, g = a_int(g_N, 0, a0) + f_ex (1 - f_b) G M_comp(<r_ev; M_c, m) / r_ev^2, with f_ex as committed. Primary F-H with P-C; F-H with P-3 reported. F-V would need each satellite's own sigma_obs to set its predicted core, which is circular; it is not scored.
- **Stripping:** r_t = infinity (CFG286: stripping shifts every median by 0.0000 dex; not re-run).
- **Statistics and error recipe (copied from CFG286 section 7 / CFG45):** P1: Kaplan-Meier median with the 9 limits; error = sqrt(boot^2 (1000 resamples, seed 42) + f_ups^2 (half the shift between Upsilon_V = 1 and 4) + f_mh^2 (half the range over collapse floors 1e8, 3e8, 1e9, 3e9, 1e10 for M_* < 1e5)). P2-P4: sample median; error = sqrt((1.2533 std / sqrt n)^2 + f_ups^2 + f_mh^2). The core is recomputed in every variant. z = median / error. Both footings.
- **Pass lines (copied from CFG286 section 9):** H1: |z_P1| < 2 on both footings. H2: |z| < 2 for P2, P3 and P4 on both footings (two-sided). JOINT PASS: H1 and H2 on both footings (the M31 route clause of CFG286 concerns pericentres and is void without stripping). PARTIAL: H1 and H2 together on exactly one footing, or one of H1 / H2 on both footings and the other on exactly one. FAIL: anything else; the binding population (largest |z| >= 2) is named. Reported: the record's one-sided A2, the 1-sigma level, the shift of every median from S.
- **Harness MUTATE (separate outputs):** MUTATE=3 uncored (soliton off) must reproduce CFG45's reading S (UF and CL medians, errors, z; both footings; all four populations) to 1e-9. MUTATE=4 with m = 37 eV in every row must reproduce reading S to 1e-9.

## 7. Controls of the pre-flight script (load-bearing unless marked)

- **C-SP1:** the shooting eigenvalue E agrees between two integration tolerances (rtol 1e-11 and 1e-13) to 1e-8 relative; chi is nodeless on [0, x_max].
- **C-SP2 (virial):** |T / J - 1| < 1e-3.
- **C-SP3 (shape vs eq. 3):** |rho_SP / rho_fit - 1| <= 0.03 for 0 <= x <= 3 x_c.
- **C-SP4 (normalisation vs eq. 3):** x_c^4 hbar^2 / (4 pi G m^2) at m = 1e-23 eV, in Msun pc^-3 kpc^4, within 6% of 1.9.
- **C-SP5 (eq. 6 vs eq. 7 through the SP profile):** M_sol(<r_c) with r_c from eq. 7 equals eq. 6's M_c within 25%, at m22 = 1 and M_h = 1e9 and 1e11 Msun (a = 1).
- **C-SP6 (Schive's stated fractions):** M_sol(<3 r_c) / M_sol in [0.93, 0.97]; half-mass radius / r_c in [1.40, 1.50].
- **C-TAIL:** chi(x_max)^2 <= 1e-12.
- **C-NFW:** the analytic NFW equals h48's `nfw_enclosed` at every generic r_ev to 1e-12 relative.
- **C-MASS:** the composite's enclosed mass by direct quadrature of rho_comp equals the closed form of 3.4 to 1e-5 relative (G-U and one G-C system, D1, both forms, P-C).
- **C-SIGN (the instrument can see the right sign):** at R-out (1e-22 eV, outside the window), at least one G-C system has q <= -0.116 under some form and prescription. If this fails, the pre-flight cannot tell a right sign from a wrong one, and its NO would mean nothing.
- **PRE-FLIGHT (headline; a finding, load-bearing in the main run):** "a right-sign window exists in the decision rows". A NO is a finding and makes the main run exit 1 (house convention, as in CFG286 and CFG288).
- **HAND (reported):** the hand predictions of section 8, scored.

**MUTATE (separate outputs, named by mode):**
- **MUTATE=1 (uncored wave field, the soliton switched off; composite = NFW):** load-bearing: q = 0 to 1e-12 at every (row, form, prescription, system), and M_comp(<r_ev) equals h48's `nfw_enclosed` (reading S's cold term) to 1e-12. Expected in that run: C-SIGN fails and the decision is NO (reported there).
- **MUTATE=2 (m = 37 eV in every decision row; core negligible):** load-bearing: |q| < 1e-6 at every (row, form, prescription, system), i.e. the no-core result.
- In MUTATE runs only the mode's own check is load-bearing.

## 8. Frozen hand predictions (my arithmetic, before any script)

Scalings. F-V: r_c = k hbar / (m sigma), rho_c proportional to m^2 sigma^4, M_sol proportional to sigma / m. F-H: r_c proportional to M_h^(-1/3) / m, rho_c proportional to m^2 M_h^(4/3), M_sol proportional to M_h^(1/3) / m. At fixed m the ratio r_c / r_half is smaller in the classicals than in the UFDs by (sigma_C / sigma_U)(r_half,C / r_half,U), about 3 x (7 to 33), i.e. 20 to 100 (F-V), or (M_C / M_U)^(1/3)(r_half,C / r_half,U), about 1.7-2.4 x (7 to 33) (F-H). **So any core large enough to reach r_half in a classical dwarf has already swallowed the UFD's r_half: the ordering is the wrong way for "bite the M31 dwarfs, spare the UFDs".** And at every m in the window the soliton is a dense nugget (rho_c far above the NFW density at r_c), which adds cold mass rather than removing it.

| row | r_c G-U (F-H / F-V) | r_c G-C (F-H / F-V) | q G-U (F-H / F-V) | q G-C range | expected sign |
|---|---|---|---|---|---|
| D1 2e-20 | 7.4 / 16 pc | 3-4.5 / 4-6 pc | +2.5 / +0.3 to +0.45 | +0.003 to +0.10 | both up: wrong way for M31 |
| D2 1e-19 | 1.5 / 3.1 pc | 0.6-0.9 / 0.8-1.2 pc | +0.55 / +0.21 | +0.0006 to +0.02 | both up, M31 negligible |
| D3 1e-18 | 0.15 / 0.31 pc | < 0.15 pc | +0.06 / +0.03 | <= +0.002 | negligible |
| D4 1e-17 | 0.015 / 0.03 pc | < 0.015 pc | +0.006 / +0.003 | <= +0.0002 | negligible |
| R-out 1e-22 (outside) | 1.5 / 3.1 kpc | 0.6-0.9 / 0.8-1.2 kpc | -1.00 / -1.00 | -0.95 to +0.08 | M31 down, UFD core erased |

- **HE1:** NO WINDOW (P = 0.97). The harness is not run.
- **HE2:** q over G-C is >= 0 at every decision row, form and prescription (P = 0.85); |q| over G-C <= 0.15 at every decision row (P = 0.9).
- **HE3:** q_UFD > 0 at D2-D4 in both forms (P = 0.9); at D1, F-H q_UFD in [+1, +4] (P = 0.7), F-V q_UFD in [-0.2, +0.8] (P = 0.7).
- **HE4:** C-SIGN passes (P = 0.95): at R-out the G-C systems lose cold mass and G-U loses essentially all of it (q_UFD <= -0.9, P = 0.9), so even outside the window the separation is the wrong way.
- **HE5:** SP constants: x_c in [1.2, 1.4], k in [0.40, 0.60] (P = 0.8 each). C-SP2, C-TAIL, C-NFW, C-MASS pass (P = 0.95); C-SP3 (P = 0.8), C-SP4 (P = 0.85), C-SP5 (P = 0.75), C-SP6 (P = 0.8).
- **HE6:** R-edge: the largest m with a classical bite lies between 1e-22 and 2e-21 eV, at least one decade below the window floor, and G-U's q there is <= -0.5 (P = 0.75).
- **HE7:** the aggregate translation at D1, F-H: the UFD KM median moves by about -0.2 to -0.3 dex (an over-fill that could push the UFDs below -2 sigma if the harness were run); the M31 LVD median moves by -0.00 to -0.02 dex (worse, not better) (P = 0.7).

## 9. Free-choice statement (frozen)

Not derived and declared: Schive's eq. 7 coefficient and its a = 1 evaluation (a simulation result); the identification sigma_sol = sigma_obs in F-V; the composite prescriptions P-C / P-3; the M_200c -> M_vir conversion; the generic grid; the two thresholds. The decision rule requires the NO (or the YES) to hold over every combination of form and prescription, and is generous on both thresholds, so no single declared choice can open or close the window by itself. If the outcome were split between combinations, the lane would say so and would not call it a derivation.

## 10. Files

- `cfg293_wavefield_preflight.py`: MUTATE=0 (main), 1 (uncored), 2 (m = 37 eV). Outputs `cfg293_wavefield_preflight[_MUTATE1|_MUTATE2].out` / `_results.json`; each run prints this file's sha256 and ends with "N/M checks pass".
- Only if a window exists: `cfg293_cored_harness.py` (MUTATE=0, 3, 4) with its own outputs.
- `README.md` after the runs.

Nothing here says the theory is closed. kappa = 1/2 FITTED. The cold mass is still required.
