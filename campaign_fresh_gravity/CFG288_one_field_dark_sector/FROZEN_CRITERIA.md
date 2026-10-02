# CFG288 -- one field for the dark sector (background = the dark energy, clumps = the cold component), and the recombination-seeding question: frozen criteria

Written before any CFG288 script existed and before any CFG288 number was computed by a machine. Paths are relative to the repository root.

Standing statements, binding on every sentence of the lane: kappa = 1/2 is FITTED, not derived. No dark-matter particle species is added. Any field has quanta: if the cold component is the field's oscillation, it is **a classical field whose quanta would be light bosons**, and that is the dark-energy field doing a second job, not a new species. **The cold mass (Omega_c h^2 ~ 0.120) is still required**; the question is only whether one field can carry it and fix its amount. Nothing here says the data favour the framework, or that the theory is closed. A FAIL is a valid outcome, and a failure is verified as hard as a pass.

---

## 0. What was read before freezing (not-blind statement)

**Read (memory notes, read-only):** the ghost-condensate dark sector (amount I0 ~ Omega_dm robustly free; Path B no-go; sign(I0) > 0 forced), the condensate mu-pincer (v9 DBI dust dead, R pinned, P(k=0.2) 18-300x over the 3% ceiling; c_s^2(rec) <= 1e-5 loose; forest c_s(z=3) <~ 5 km/s; pressure cannot shield galaxies; merger gate; ballistic survivor window), L374/L382/L383 (condensate EFT breaks at the first stream crossing; only a linear wave field passes; m >~ 2-5e-19 eV with clearing), FL1/FL2/FL3 and FK1 (the complex order parameter in V0's dark slot; GDM residual <= 3e-16 for m >= 2e-19 eV; the amount = the misalignment amplitude), particle-vs-mode (the GDM theorem; the w0 squeeze), MS1 (the switch reads baryons, never carrier or curvature), L353 (kernel-invisible dark component; reciprocity), the merger lanes L370-L372, the no-dark-matter-particle feedback, the standing rules / do-not-cite list.

**Read (repo):** `campaign_fresh_gravity/closure_map/GAPS_1_2_JOINT_STATUS.md` (CFG243: turnaround-created dust cannot be the cosmic cold component, shortfall 10^1376 at z = 1100; CFG244; CFG245: vacuum-rate relaxation too slow, Gamma tau <= 0.79 vs ~4.1); the CFG288 entry of `closure_map/RESEARCH_DIRECTION_2026-09-29.md`; CFG286's FROZEN_CRITERIA.md, script header/ending and output tail (house style); `CFG7_common.py` (the `Report` class and `A0_SI`); the CAMB fluid set-up of `fable_independent_2026/L165_smooth_dust_third_peak_calibrated_sigma.py` (the dust + Lambda combined fluid with omega_cdm -> 0); CAMB 1.6.6's `dark_energy.py` (DarkEnergyFluid, `set_w_a_table`, its refusal of w crossing -1).

**Data on disk:** no Planck binned TT/EE spectra were found in the repository or in `../_external_data` (searched by name). So the CMB comparison is against Planck-2018 best-fit LambdaCDM C_l computed by CAMB, and the precision scale is DECLARED and approximate (section 6). No Delta chi^2 against data is computed.

**Pre-freeze hand arithmetic (mine, written into section 11 as expectations; the scripts decide).** I have estimated, by hand only: the A1 bound at z_eq (~1.5e10 rho_Lambda), the ghost-condensate coldness scale (M >~ 3-5 eV), the recombination energy reservoirs, the wave-field misalignment amplitude at 2e-20 eV (~4e16 GeV), and the a0/rho_Lambda tie (~0.1%). No machine has computed any of these.

---

## 1. The question (owner-directed, frozen)

Can ONE field do both jobs: its smooth background is the dark energy (w = -1, density rho_Lambda, the same rho_Lambda that sets a0 = kappa c sqrt(G rho_Lambda) with kappa = 1/2 FITTED), and its clumps/excitations are the cold component with Omega_c h^2 = 0.120? And could that cold component be "seeded" as a byproduct of recombination (z ~ 1100)?

The lane builds the best honest attempt on two roads, scores it against every gate below, and runs a Boltzmann (CAMB) row for the owner's seeding question.

---

## 2. Constants ledger

| item | value | status / source |
|---|---|---|
| kappa | 1/2 | FITTED (the only fitted constant allowed) |
| a0 canonical | 9.3603e-11 m/s^2 (rho_Lambda footing) | the record's `CFG7_common.A0_SI` |
| a0 alt | 1.1312e-10 m/s^2 (rho_total / cH0 footing) | the record's `CFG7_common.A0_SI` |
| Planck 2018 best fit (TT,TE,EE+lowE+lensing, Table 2 means) | omega_b 0.02237, omega_c 0.1200, H0 67.36, tau 0.0544, ln(1e10 A_s) 3.044, n_s 0.9649, 100 theta_MC 1.04092 | measured (Planck 2018 VI); used for the CAMB reference |
| neutrinos | sum m_nu = 0.06 eV (one massive), N_eff = 3.046 | CAMB defaults as in the Planck baseline |
| T_CMB | 2.7255 K | measured |
| Omega_Lambda (canonical) | 1 - Omega_m - Omega_r at H0 = 67.36 (CAMB closure) | derived |
| G, c, hbar, eV | CODATA | measured |
| reduced Planck mass | Mbar_Pl = sqrt(hbar c / (8 pi G)) | derived |
| H_Lambda | H0 sqrt(Omega_Lambda) | derived |
| local density for the classical-field and solar-system rows | 0.4 GeV/cm^3, v = 220 km/s | declared reference values, approximate |
| Y_p | 0.245 | measured (BBN/Planck), for n_H only |

**No constant is fitted or scanned.** If a construction needs a new constant, its needed value is computed, the constant is DECLARED free, and the amount gate reads "AMOUNT FREE (needs X)".

---

## 3. Gates (numeric thresholds frozen)

A gate verdict is one of: PASS; FAIL; PASS-CONDITIONAL (passes only for a declared free constant in a stated range); AMOUNT FREE (needs X); INHERITED (passes by a committed record lane that this lane cites but does not re-derive).

- **G-BG (background).** (i) Today w_DE = -1 is within 2 sigma of w = -1.028 +- 0.031 (Planck 2018 VI, TT,TE,EE+lowE+lensing+SNe+BAO, constant w). (ii) The field's vacuum value rho_Lambda reproduces the record's a0 via a0 = kappa c sqrt(G rho) to <= 1%: canonical with rho = rho_Lambda (Planck), alt with rho = rho_crit (rho_total / cH0 footing). Caveat recorded, not used in the verdict: DESI DR2 (2025, from memory) reports a few-sigma preference for an evolving w0-wa; a w = -1 construction would be disfavoured if that holds.
- **G-DUST (perturbations behave as cold dust).** The GDM triple (w, c_s^2, c_vis^2): |w(z=1100)| <= 1e-5; c_s^2(z=1100, k <= 0.3 Mpc^-1) <= 1e-5 (the record's loose CMB threshold, condensate mu-pincer); c_s(z=3, k = 10 h/Mpc) <= 5 km/s (the record's forest threshold); c_vis^2 = 0 at linear order.
- **G-ONSET.** (i) Dust-like (|w| <= 1e-5) by z_eq = 3400. (ii) The onset redshift z_on >= z_req, where z_req is set by the CAMB seeding table of this lane (section 6): the smallest z_seed in the main grid rated INDISTINGUISHABLE with every larger grid value also INDISTINGUISHABLE; if none qualifies, z_req = 1e7 (the control), provided the control passes. (iii) Omega_c h^2 = 0.120 +- 0.001 is reached; if the construction cannot fix it, (iii) is scored under G-AMOUNT.
- **G-AMOUNT.** PASS only if the action, with no constant beyond kappa = 1/2, the measured rho_Lambda, G, c, hbar and the measured radiation and baryon content, fixes Omega_c h^2 = 0.120 +- 0.001. Otherwise "AMOUNT FREE (needs X)". The coincidence diagnostic is reported: rho_c / rho_Lambda = (Omega_c / Omega_Lambda)(1+z)^3, so a fixed tie of rho_c to rho_Lambda singles out today unless the mechanism explains it.
- **G-STREAM (collisionless at shell crossing).** The 1-D free-streaming test of section 7.4: the coarse-grained density of the construction matches the exact collisionless (multistream) answer with relative L1 <= 0.02 at t = 2 and 3 t_sc. The single-valued pressureless-fluid control must FAIL the same test (L1 > 0.02), or the test has no power and the G-STREAM PASS is void. The self-gravitating version is INHERITED from L374 (`real_research/condensate_dust_2026/L374_condensate_dust_shell_crossing.py`; Schrodinger-Poisson tracks N-body to <= 1%; the condensate EFT breaks).
- **G-PK (small-scale power).** Wave-field mass bound m >= m_min = 2e-20 eV (Lyman-alpha, Rogers & Peiris 2021, as quoted in the record's merger gate); reported beside it: the record's L383 dwarf-heating floor 2-5e-19 eV. With the Hu-Barkana-Gruzinov (2000) transfer T(k) = cos(x^3)/(1+x^8), x = 1.61 m22^(1/18) k / k_J,eq, k_J,eq = 9 m22^(1/2) Mpc^-1: 1 - T^2(k = 0.2 h/Mpc) <= 0.03 (the record's 3% P(k=0.2) ceiling) and T^2(k = 10 h/Mpc) >= 0.5 (the record's loose forest criterion). For a pressure-supported (P(X)) dust: the comoving Jeans wavenumber k_J(z) = a sqrt(4 pi G rho_d) / c_s >= 2 h/Mpc (ten times 0.2 h/Mpc) for every z in [0, 1100] (declared, approximate: suppression at 0.2 h/Mpc then ~1%).
- **G-MERGER (Bullet class).** (i) The medium multistreams (G-STREAM PASS); (ii) its sound speed (polytropic or quantum pressure) at the merger scale L = 200 kpc is <= 0.01 v_merge = 30 km/s; (iii) no non-gravitational self-interaction in the minimal action (else sigma/m <= 1.25 cm^2/g, Randall+2008, is scored).
- **G-STAB/GW.** (a) no ghost: positive kinetic coefficient; (b) no gradient instability or tachyon: c_s^2 >= 0 for every k, m^2 >= 0; (c) c_T = 1 exactly (GW170817, |c_T - 1| <~ 1e-15), shown by deriving the tensor equation with the field present; (d) couples to matter only through g_munu; kernel invisibility (the MOND switch never reads the dark field) is INHERITED from L353 (`real_research/g03_audit_2026/`) and MS1 (`real_research/mond_sector_gate_2026/`) and FL2's V1 (`real_research/dark_fluid_2026/`), not re-derived; (e) solar system: the dark mass inside 9.5 AU at rho_loc = 0.4 GeV/cm^3 is <= 1.7e-10 Msun (Pitjeva & Pitjev 2013, from memory, approximate).

---

## 4. Stage A -- pre-flight theorems (sympy; script `cfg288_stageA_theorems.py`)

- **A1 (potential / oscillation road).** Checked:
  - A1.1: for a homogeneous canonical scalar with rho = phidot^2/2 + V - V_min, the equation of motion gives d rho/dt = -3 H phidot^2 (exact, sympy). So rho is non-increasing.
  - A1.2: for V - V_min proportional to |phi|^(2n), the cycle average gives <w> = (n-1)/(n+1) (virial, sympy); n = 1 is dust-like, n >= 2 dilutes faster.
  - A1.3 (the bound): if the component is dust-like from a_d on, rho_0 = rho(a_d) a_d^3 <= Delta V a_d^3, so Delta V >= (Omega_c / Omega_Lambda) rho_Lambda (1+z_d)^3. Computed for z_d in {1100, 3400, 1e4, 1e5, 1e6, 1e7} and for the onset of a wave field at m = m_min.
  - A1.4 (the claim to test): "a single field whose potential has one scale tied to rho_Lambda (height Delta V <= 1e3 rho_Lambda, generous) cannot supply the dust". PROVED iff Delta V_min / rho_Lambda > 1e3 at z_d = 3400 (and so at every larger z_d). The dark energy is then a residual at the minimum: the tuning V_min / Delta V <= rho_Lambda / Delta V_min is reported.
  - Numerical control (can fail): the Klein-Gordon equation in radiation domination, phi'' + (3/2x) phi' + phi = 0, integrated numerically, matches the exact Bessel solution Gamma(5/4)(x/2)^(-1/4) J_(1/4)(x) to 1e-6, its rho is non-increasing at every step to 1e-10 relative, and the average of rho x^(3/2) over x in [1000, 3000] equals the analytic constant Gamma(5/4)^2 sqrt(2)/pi to 1e-3. Reported: the quartic case (n = 2) gives <w> = 1/3 to 1e-2.
- **A2 (shift-charge road).** Checked:
  - A2.1: for shift-symmetric P(X) on FRW, the equation of motion is exactly d(a^3 P_X phidot)/dt = 0, so a^3 P_X phidot = C (integration constant).
  - A2.2: for P(X) = -rho_Lambda + (M^4/2)(X/X0 - 1)^2, a solution exists for every C > 0 at fixed action parameters (the defining relation is monotone in X above X0); C is not fixed by any action parameter.
  - A2.3: to leading order rho_d = sqrt(2 X0) C a^-3, with d rho_d / d rho_Lambda = 0 and d rho_d / d M^4 = 0 at fixed C; c_s^2 = rho_d / (4 M^4) and w = c_s^2 / 2 (leading order, sympy).
  - A2.4: coldness at z = 1100 (c_s^2 <= 1e-5) needs M^4 >= rho_d(1100) / (4e-5); the single-scale case M^4 <= 1e3 rho_Lambda is tested against the 1e-5 threshold (FAIL expected).
  - A2.5 (what could seed it): a seeding event is an epoch of explicit shift-symmetry breaking. With nabla_mu T^munu = 0 (Bianchi), the energy injected at z_s is >= rho_c(z_s). Reservoirs at z_s = 1100: (i) hydrogen binding, 13.6 eV x n_H with Y_p = 0.245; (ii) CMB photons, all of them and the FIRAS-allowed part (|y| <= 1.5e-5, so Delta rho_gamma / rho_gamma <= 6e-5); (iii) all radiation; (iv) a vacuum / potential reservoir >= rho_c(z_s), which is A1 and the CAMB row. A reservoir "can supply" iff available / needed >= 1.
- **A3 (derived mass scale).** The family the framework's own constants allow is m_q = Mbar_Pl^(1-q) (hbar H_Lambda)^q, for q in {0, 1/4, 1/3, 1/2, 2/3, 3/4, 1}. Also computed: hbar a0 / c^3 (both footings) and rho_Lambda^(1/4). The window is [m_min = 2e-20 eV, m_max], where m_max is the classical-field limit n lambda_dB^3 = 1 at 0.4 GeV/cm^3 and 220 km/s (lambda_dB = 2 pi hbar / (m v)). The window also has the onset floor m >= H(z_req), reported. "Mass derived" requires exactly one framework-native candidate in the window with no free exponent choice. Reported: which candidates land, and how far the framework's distinctive scale (q = 1, the a0 / H_Lambda scale) misses.
- **MUTATE=1 (stage A):** the kinetic sign flipped (a ghost). A1.1's monotonicity check must FAIL (rc = 1): only a ghost evades the A1 bound, and G-STAB forbids it.

---

## 5. Stage B -- constructions (script `cfg288_construction_gates.py`)

- **Road W (wave field).** S = integral sqrt(-g) [ Mbar_Pl^2 R / 2 - g^munu d_mu Phi* d_nu Phi - m^2 |Phi|^2 - rho_Lambda ] + S_matter[g], with Phi complex (FL1's order parameter in V0's dark slot), lambda = 0, m declared. Its vacuum value V_min = rho_Lambda is the dark energy; its oscillation is the cold component. Derived from the action:
  - W1: the non-relativistic limit gives Schrodinger-Poisson (sympy).
  - W2: the background (w = -1 frozen, dust after onset) via the exact radiation-era solution. The misalignment amplitude needed for omega_c = 0.120 at m = m_min, at the record's 2e-19 eV, and at every A3 candidate that lands. The g*(T) evolution is ignored: declared approximation, only used to quote "needs X". Also d rho_dust / d rho_Lambda = 0 at fixed (m, phi_i), shown in sympy.
  - W3: the linear sound speed c_s^2 = hbar^2 k^2 / (4 m^2 a^2) from the linearised Madelung / Schrodinger-Poisson system (sympy), w = O((H/m)^2), c_vis^2 = 0.
  - W4: HBG transfer (G-PK).
  - W5: the stream test (G-STREAM).
  - W6: the merger rows.
  - W7: G-STAB/GW: sympy derivation of the tensor equation h'' + 3H h' - h_zz / a^2 = 0 with the field present (background equations used), and the scalar Lagrangian free of metric derivatives.
- **Road S (seeded shift charge).** S = integral sqrt(-g) [ Mbar_Pl^2 R / 2 + P(X) ] + S_matter[g], with P(X) = -rho_Lambda + (M^4/2)(X/X0 - 1)^2 (ghost-condensate form, the record's K(Q) = mu^2 (Q-1)^2 class), plus a seeding term -J(t) phi active at z_s. Scored with the A2 results. G-STREAM: the single-valued gradient flow is exactly this road's dust limit, so the W5 fluid control is this road's row (FAIL expected), together with L374. G-MERGER (i) follows from G-STREAM; (ii) and (iii) are scored as for road W. G-STAB: P_X > 0 needs C > 0 (the record's forced sign); the k^4 term is needed at X0; c_T = 1 because P(X) contains no metric derivatives.
- **Correspondence (stated, computed):** a misaligned wave field is literally "dark energy converting to cold dust" at z_on, where H(z_on) = m, and its pre-onset vacuum energy m^2 phi_i^2 / 2 is the reservoir of A1. So the CAMB table's z_req converts into a floor on m. This is reported beside G-PK.
- **MUTATE=1 (stage B):** the wave field's hbar/m raised to nu = 0.02 (de Broglie length about the box size). The wave-versus-collisionless match must FAIL (rc = 1).

---

## 6. The owner's seeding row (CAMB; script `cfg288_seeding_camb.py`)

- **Reference:** Planck-2018 best-fit LambdaCDM (section 2) in CAMB 1.6.6. Settings: lmax = 2500, lens_potential_accuracy = 1, AccuracyBoost = lSampleBoost = lAccuracyBoost = 2, NonLinear_none (linear lensing), CMB in muK^2. Lensed spectra decide; unlensed spectra are reported.
- **Model ("dark energy converting to cold dust at z_seed"):**
  - omch2 = 1e-6 (CAMB's CDM slot, tiny).
  - The seed fluid has w_s(a) = w_e + (0 - w_e) (1/2)[1 + tanh((ln a - ln a_s)/Delta)], with w_e = -0.999, Delta = 0.05 and a_s = 1/(1+z_seed). Its rest-frame sound speed is cs2 = 0 (if CAMB rejects 0, cs2 = 1e-10, documented).
  - rho_s(a) = rho_s(1) exp(3 integral_a^1 (1 + w_s) d ln a'), with rho_s(1) set to give omega_s = 0.1200 - 1e-6 (the total cold matter today is then 0.1200). The integral is numerical, on a fine grid.
  - **Implementation (documented, equivalent):** CAMB carries a single dark-energy component, so the separate cosmological constant is folded in. The fluid carries rho_Lambda + rho_s with w_tot = (-rho_Lambda + w_s rho_s) / (rho_Lambda + rho_s), via `DarkEnergyFluid.set_w_a_table`, and Omega_Lambda = Omega_de(CAMB closure) - Omega_s. At linear order Lambda carries no perturbation and no momentum, so the combined fluid's rest frame is the seed fluid's and its rest-frame sound speed is the seed's (0). The combination is therefore exactly Lambda + seed fluid. Control C-FLUID tests this numerically.
  - Table: a from 1e-10 to 1, at least 6000 log-spaced points plus 3000 points within +-0.5 in ln a of a_s. Below the table CAMB extrapolates with constant w (w_e), which is the model.
  - Energy is conserved, so before seeding the fluid holds the vacuum energy rho_c(a_s). This is the only GR-consistent version of "dark energy converts to dust" (Bianchi identity), and it is the model run. Reported per row: the pre-seed vacuum fraction f_pre = rho_s / rho_tot at a_s.
- **Grid:** z_seed in {1100 (recombination, the owner's case), 3400, 1e4, 1e5, 1e6} (main), plus the control at 1e7.
- **Two comparisons per model:** (a) H0 fixed at 67.36 (physical densities fixed); (b) theta*-matched: H0 re-solved (brentq in [40, 120]) so that CAMB's derived thetastar equals the reference's, everything else fixed. **The decision uses (b)**, the conservative one, since a likelihood would absorb a pure peak shift through H0. If (b) has no solution in the bracket, (a) decides and the row says so.
- **Statistics:** S_TT = max over 30 <= l <= 1000 of |C_l^TT / C_l^TT,ref - 1| (lensed), covering the first three peaks; S_EE the same for EE (reported). Also reported: the same maxima over 2-29 and 1001-2500; the unlensed S_TT; the first three TT peak heights (maxima of D_l in [150, 300], [400, 650], [700, 950]) with H1/H3 and H2/H1 and their changes against the reference; Delta theta*/theta*; z_eq, defined as the largest z with rho_b + F rho_s >= rho_gamma + rho_nu (massless and massive neutrinos, CAMB's background densities), where F = (w_s - w_e)/(0 - w_e) is the converted fraction (CAMB's background densities); and a cosmic-variance proxy Delta chi^2_CV = sum over 30 <= l <= 2000 of (2l+1) f_sky / 2 (Delta C_l / C_l)^2 with f_sky = 0.6 (no noise, no re-fit beyond theta*; approximate, reported only).
- **Decision rule (frozen), on (b), lensed TT:**
  - EXCLUDED if S_TT > 1% (Planck's ~1% precision over the first three peaks, declared approximate);
  - INDISTINGUISHABLE if S_TT <= 0.1%;
  - otherwise UNDECIDED (0.1-1%): needs the Planck likelihood, since no binned data are on disk.
  - INDISTINGUISHABLE cannot be awarded if C-FLUID or C-EARLY fails.
  - If CAMB fails for a row, it is retried once with Delta = 0.1 (documented); if it still fails, the row is NOT COMPUTED.
- **Controls (load-bearing):**
  - C-REF: the reference's CAMB 100 theta_MC is within 0.0006 of 1.04092.
  - C-BG: CAMB's dark-energy rho(a)/rho(1) (`get_dark_energy_rho_w`) equals (rho_Lambda + rho_s(a)) / (rho_Lambda + rho_s(1)) to 1e-3 relative, at 200 log-spaced a in [1e-9, 1], for every model.
  - C-FLUID: the combined fluid with dust at all times (rho_s = rho_s(1) a^-3, no seeding) reproduces the reference lensed TT and EE to <= 0.1% (max over 2 <= l <= 2500).
  - C-EARLY: seeding at z = 1e7 reproduces the reference lensed TT and EE to <= 0.1% (same range), under comparison (a).
- **MUTATE=1 (seeding):** C-EARLY's z_seed replaced by 1100. Its "reproduces LambdaCDM" check must FAIL (rc = 1): the test can fail.
- **Reported rows (never verdicts):** Delta = 0.02 and 0.2 for z_seed = 1100 and 1e5; w_e = -0.99 for z_seed = 1e5; lensing off for every row.

---

## 7. Fixed numerical settings (not physics)

- 7.1 Stage A ODE: x = m t from 1e-4 to 3e3, DOP853, rtol = 1e-12, atol = 1e-14.
- 7.2 Planck-2018 and Lyman-alpha numbers are inputs as listed. Nothing is re-fitted.
- 7.3 Run order: stage A, then seeding, then construction. The construction script reads `cfg288_seeding_camb_results.json` for z_req. If that file is absent, z_req = 1e7 and the output says so.
- 7.4 G-STREAM test: periodic box L = 1, rho0 = 1, v(q) = -A sin(2 pi q) with A = 1/(2 pi), so t_sc = 1. Wave: nu = hbar/m = 5e-5 (MUTATE: 0.02), N = 2^15 grid, exact FFT free evolution of psi0 = exp(i S / nu) with S = (A / 2 pi) cos(2 pi q). Collisionless reference: 2^21 Lagrangian points on a uniform q-grid moved exactly (x = q + v t mod 1), CIC-deposited. Fluid control: the sticky (zero-viscosity Burgers) single-valued solution from the convex hull of q^2/2 + t S(q) on the same q-grid. All three are smoothed with the same Gaussian, sigma = 0.01 L. Metric: integral |rho_a - rho_b| dx / integral rho_b dx. Evaluated at t = 2 and t = 3.

---

## 8. Controls and MUTATE summary (all load-bearing unless marked)

- Stage A: the Bessel ODE control; MUTATE=1 (ghost sign) must fail A1.1.
- Seeding: C-REF, C-BG, C-FLUID, C-EARLY; MUTATE=1 must fail C-EARLY.
- Stage B: the fluid control must fail the stream match (power check); MUTATE=1 (nu = 0.02) must fail the wave match.
- Mutation runs write separate outputs (suffix `_MUTATE1`).

---

## 9. What the lane cannot say

- It does not address the galaxy-scale double count (MOND plus a cold component inside galaxies; KiDS; dwarfs), Gap 1/2 ownership, the satellites, or the cluster cores.
- It is not a Planck likelihood fit. With no binned data on disk, the 1% / 0.1% scale is declared and approximate, and Delta chi^2_CV is a proxy only.
- Behaviour passes on the wave road are not a new prediction. At linear order the wave field is CDM (the GDM theorem), so the CMB cannot tell it from CDM.
- The CAMB model is the owner's phenomenological, energy-conserving, spatially uniform conversion. Spatially varying or non-adiabatic seeding microphysics is not covered.
- kappa = 1/2 FITTED. Nothing here derives kappa, and nothing here says "theory closed" or "data favour the framework".

---

## 10. Files

- `cfg288_stageA_theorems.py` (MUTATE=1: ghost sign)
- `cfg288_seeding_camb.py` (MUTATE=1: control seeded at 1100)
- `cfg288_construction_gates.py` (MUTATE=1: nu = 0.02)
- Outputs: `<script>.out`, `<script>_results.json`, and `<script>_MUTATE1.out` / `_MUTATE1_results.json`. Each script ends with an "N/M checks pass" line.
- `README.md` after the runs.

---

## 11. Frozen hand estimates (my arithmetic, before any run)

- **HE1:** Delta V_min / rho_Lambda at z_d = 3400 ~ 1.5e10, so A1.4 is PROVED (P = 0.97). Delta V^(1/4) ~ 0.8 eV against rho_Lambda^(1/4) ~ 2.2-2.3 meV.
- **HE2:** road S needs M >~ 3-5 eV for c_s^2(1100) <= 1e-5; with M^4 ~ rho_Lambda, c_s^2(1100) >~ 1e7 (the EFT is not even in its dust regime). A2.4 single-scale: FAIL (P = 0.97).
- **HE3:** recombination reservoirs: hydrogen binding falls short by ~4e8; all photons give ~0.2 of the need; the FIRAS-allowed part ~1e-5 of the need. All FAIL (P = 0.97).
- **HE4:** CAMB: z_seed = 1100 EXCLUDED (pre-seed vacuum ~2.6x the radiation at z_s; P = 0.95); 3400 EXCLUDED (P = 0.9); 1e4 EXCLUDED (P = 0.85); 1e5 EXCLUDED or UNDECIDED (P = 0.8 together); 1e6 UNDECIDED or INDISTINGUISHABLE (P = 0.8 together); the 1e7 control passes (P = 0.8).
- **HE5:** A3: q = 1 (the H_Lambda / a0 scale, ~1e-33 eV) misses the window by ~13 decades; q = 1/2 (~meV) and q = 3/4 (~4e-19 eV) land; the mass is NOT derived (non-unique), P = 0.9.
- **HE6:** road W: G-BG, G-DUST, G-ONSET (timing), G-STREAM, G-MERGER, G-STAB pass; G-PK PASS-CONDITIONAL on the declared m >= 2e-20 eV; G-AMOUNT "AMOUNT FREE (needs phi_i ~ 1-4e16 GeV at 2e-20 eV, plus m)". P = 0.85 for this whole pattern.
- **HE7:** road S: G-STREAM and G-MERGER FAIL; G-AMOUNT AMOUNT FREE; the single-scale tie fails G-DUST. P = 0.85.
- **HE8:** the stream test: wave L1 <= 0.02 at both times (P = 0.85); fluid control L1 > 0.1 (P = 0.9); MUTATE nu = 0.02 fails (P = 0.95).
- **HE9:** G-BG tie: canonical and alt within 0.2% of the record's a0 (P = 0.9).

Nothing here says the theory is closed. kappa = 1/2 FITTED. The cold mass is still required.
