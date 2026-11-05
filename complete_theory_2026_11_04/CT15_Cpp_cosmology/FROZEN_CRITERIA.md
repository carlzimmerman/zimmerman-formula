# CT15: G5 (CMB + background) and late growth for candidate C'' with the dust amount FITTED (frozen before any number)

Lane under `../CT_GATES_COMMON.md` and the owner's follow-up in `../OWNER_DECISION_2026-11-04_D1.md` ("Yes, grade it": the dust amount is counted as a fitted constant). Grading only: nothing adopted, the cold sector retired on 2026-11-01 stays retired, no particle. kappa = 1/2 FITTED. Not theory closed. Nothing here says the data favour the framework.

## Step 1: C''s linear cosmology, from the record (stated before computing)

C'' = the frozen v3s action (V3S_FINAL_VERDICT_2026-10-24.md §1) with Lambda removed and a canonical phi, a0^2 = kappa^2 G (phidot^2/2 + V) (CT10 README; CT13).
- **The dust is v3s's khronon charge**, the one cold field, with weight alpha = 1 fixed by kinematics (V3_FULL_PICTURE.md §4.1; LEAN `coupling_one_is_law`). Its amount is the shift charge I0, an initial condition: here the FITTED constant omega_x.
- **Its linear perturbations are NOT those of standard cold dust** at galaxy-allowed mu_K. Q6 D2/D5 (Q6_v3_class/README.md): the khronon is a fluid with c_s^2 = Q K'/(Q^2 K'' - 2 j1 k^2/a^2), j1 = J'(0) = -1, and its net self-force kernel is s = a^2 mu_K^2/(k^2 + a^2 mu_K^2): modes above a mu_K are held (V3_FULL_PICTURE.md §4.2). Only the limit K'' -> infinity (mu_K -> infinity) is CDM (Q6 D6). mu_K < 0.1 Mpc^-1 is the isolated-galaxy lensing bound (S4; verdict §1 line 31). At z 1090, a mu_K <= 9e-5 Mpc^-1, below every acoustic scale.
- **The MOND sector does not enter linear FRW growth.** J_x enters the quadratic action only through J(0) (= Lambda, here 0) and J'(0) = -1; a0 first appears at O(Y^{3/2}) (Q6 README:28-29, D0; C2 K1). In C'', g = 0 on FRW gives L_M = 0 and dL_M/drho = 0 (CT13 R6), and the phi-khronon mixing B^2/|L_gg| is proportional to s^3 -> 0. So: no MOND-sector linear growth enhancement; phi is plain thawing quintessence (c_s^2 = 1, no Lambda), and the only non-standard linear ingredient is the khronon hold (J'(0) = -1). The nonlinear J_x does not restore growth (L1 rho_NL about -0.05).
- **Decision (frozen): CLASS with standard cold dust + quintessence is NOT a faithful stand-in for C''.** The correction is the khronon kernel: Q6's validated khronon CLASS (binary sha256 3ccb50b2..., `aest_K_type = 4`, LOB = dust background with the literal perturbation equations, the record's most favourable reading, since the literal K has no radiation era, Q6 finding 1) at mu_K = 0.03 and 0.1 Mpc^-1 (S4's grid, as X4), plus a quintessence fluid. The standard-dust row (`aest_K_type = 0`, exact dust limit) is computed as the NOT-FAITHFUL reference: it is what a separate dust would give, which the record calls CDM under another name (V3_FULL_PICTURE.md §4.6, X6: double count in isolated galaxies). The BS cap mu_K = 10 Mpc^-1 (excluded by S4) is a reported favourable row.

## Inputs (10-25 rule; as CT8/CT11; no Planck LCDM values)
omega_DE0 = Omega_L 0.666 x h_native^2 (SN shape x native H0 band 67.22-68.56, central 0.6789) = 0.3070 (CT11 out:1); omega_b 0.0224 (BBN); omega_r from T_CMB 2.7255, N_eff 3.046; h by flat closure h = sqrt(omega_b + omega_x + omega_DE0 + omega_r) (as CT11). A_s 2.1e-9, tau 0.0544, YHe 0.2454 inherited (CT3); n_s bracketed 0.93 / 0.9649 / 1.0. Q6's precision settings (HIGH + START, X4 x4_growth.py) for every run of the khronon binary.
- phi background: CLASS fluid, Omega_Lambda = 0, cs2_fld = 1. **Primary**: thawing limit 1 + w0 = 1e-4, wa = 0 (the frozen-phi limit C'' can approach). **Reported row**: thawing w0 = -0.9 (CT10's example), wa = -1.58 (1 + w0) (thawing calibration, from memory, provisional). w0 is a hand-set constant (V's shape and phi_i, already counted in CT10).

## Gates and lines
- **Check**: the binary's DUST row (K_type 0) at CT3's base (h 0.6736, omega_b 0.02237, omega_x 0.12, Lambda) reproduces CT3's H3/H2 0.992 within 0.004 (precision settings differ from CT3's classy defaults; stated).
- **G5 fit**: for each dust model and each n_s, the H3/H2 of the unlensed TT (CT3's local-maximum peak finder, l > 100) is evaluated at the frozen grid omega_x = 0, 0.06, 0.12, 0.24, 0.48; if the window value 0.979 is bracketed, omega_x is solved (brentq) to H3/H2 = 0.979. That solve is the one fitted constant.
  - **PASS**: a solution exists at all three n_s (H3/H2 in [0.969, 0.989]).
  - **FAIL**: max H3/H2 over the grid < 0.969 at all three n_s (no amount reaches the window).
  - Else NO VERDICT.
  - Reported, not graded: omega_x/omega_b and whether it lies in 4.9-5.4; H2/H1 vs raw 0.451; peak positions vs raw l 222 / 533 / 814 (ct3_cmb_checks.out:2-5).
- **Background** (at the fitted omega_x, n_s 0.9649, primary phi): DESI DR2 BAO 13 numbers as in CT11 (CFG681 transcription), PASS chi2 <= 28.3 (CT11 line); Pantheon+ diagonal chi2 reported. Same for the w0 = -0.9 row (reported; if only that row passes, the pass needs w0 as a second constant, counted).
- **Growth** (step 3, at the fitted omega_x): linear sigma8 from the run, S8 = sigma8 sqrt(Omega_m/0.3). Order-of-magnitude line against raw KiDS S8 about 0.77 (CT3_REPORT.md:47): PASS iff S8 in [0.51, 1.16] (within x1.5), FAIL otherwise. MOND-sector enhancement: none at linear order (step 1), stated, not computed.
- First failed gate stops the candidate; the rest are reported as numbers.

## Limits
Single thread, nice, one CLASS process at a time, under 1 GB, minutes. Run files to `../../../_external_data/ct15_cpp_cosmology_2026_11_04/` (not committed). No download. Commit nothing. CT14, CT16, CT17 untouched.
