# CFG547 FROZEN CRITERIA (2026-10-09): cosmic-time triangulation of dark energy, cold energy and galaxy baryons

Owner request (2026-10-09): look at the dark-energy density over cosmic time, where (by the best model) the cold energy is clumping and settling at each time, and the baryons in galaxies in relation to all that; triangulate and see whether anything meaningful falls out.

Framework as tested: a0(z) = kappa c sqrt(G rho_DE(z)), kappa = 1/2 FITTED. Footings at z = 0: canonical 9.36e-11 and alt 1.13e-10 m s^-2, scored separately, never pooled. Kernel nu(y) = 1/(1 - exp(-sqrt y)). Cold energy mass is required; no particle. Census edge r_edge = r_M / ln(1 + f_ret f_b/(1 - f_b)), r_M = sqrt(G M_b / a0), f_b = 1/(1 + 5.364); census f_ret = 0.1 for galaxies (THEORY_v1 R4), f_ret = 1 shown for reference. This is not "theory closed".

Committed alone, before any script is written or any number of this lane is computed. Seen before freezing: the RC100 corrected table's redshift quartiles only (0.61 / 0.92 / 1.53 / 2.19 / 2.52); the record's lanes listed in the brief (CFG511, 508, 496, 303, 216, 217, 541, THEORY_v1, ASSESSMENT). No f_DM statistic, slope or prediction of this lane has been computed.

## 0. Inputs (all on disk; no downloads)

- DESI DR2 w0wa chains (`_external_data/desi_dr2_chains/{cmb,pantheonplus,union3,desy5}`), read as CFG511 does (first 30% of each chain dropped, weights used). rho_DE(z)/rho_DE(0) = CPL f(z) (CFG508 `cpl_f`, copied, not imported).
- Background for the Lambda case: Omega_m = 0.315, H0 = 67.4 km/s/Mpc, Omega_Lambda = 1 - Omega_m (radiation neglected; disclosed).
- RC100 corrected table `real_research/data/rc100_nestorshachar2023_table3_CORRECTED.csv` (published f_DM(<R_e); MODEL-OTHER: from the authors' joint baryon + LCDM-halo fit) and CFG303's per-galaxy native baryons `CFG303_lcdm_free_inputs/cfg303_rc100_pergalaxy_LCDMFREE.csv` (g_bar_native_B = M*_SED (1 + mu_t18) in CFG216's thin disc at R_e; g_obs = V_c(R_e)^2/R_e).
- Typical-galaxy scaling relations, recalled, **PROVISIONAL** (cited, not re-read from the papers):
  - sizes: van der Wel+14 late types, R_e = 10^logA (M*/5e10)^alpha with (z, logA, alpha) = (0.25, 0.86, 0.25), (0.75, 0.78, 0.22), (1.25, 0.70, 0.22), (1.75, 0.65, 0.23), (2.25, 0.55, 0.22), (2.75, 0.51, 0.18); interpolated linearly in z; outside 0.25–2.75 logA extrapolated with R_e propto (1+z)^-0.75 from the nearest end, alpha held at the nearest end;
  - gas: the record's Tacconi-type mu_gas = M_gas/M* (CFG217 `mu_t18`, main sequence), copied verbatim; its z > 4 behaviour is an extrapolation (disclosed);
  - masses: two fixed stellar masses, log M* = 10.0 and 10.7 (the SMF knee is roughly constant z = 0–3; Muzzin+13, Davidzon+17; PROVISIONAL);
  - geometry: stars and gas share one thin exponential disc, R_e = 1.678 R_d (CFG216 disc_v2).

## 1. TIMELINE MAP (descriptive; no verdict)

Grid z = 0, 0.25, ..., 6. Tabulate: rho_DE (Lambda; DESI per-chain median and 16–84, and the 4-chain envelope), a0(z) for flat, DESI (median over the four chain medians of sqrt f; band = min/max over chains of 16/84) and the rival a0 propto H(z) (a0(0) E(z)); rho_m(z); H(z); age t(z); c H(z); a0/(c H) and the record's c H0/2pi; for both typical masses: R_e, mu_gas, M_b, g_bar/a0(z) at R_e, 2 R_e, 3 R_e, the baryonic mass fraction outside the outermost radius where g_bar = a0 (the disc fraction in the law's regime), predicted f_DM(<R_e) = 1 - 1/nu(g_bar(R_e)/a0); settling time t_ff(r) = (pi/2) sqrt(r / (2 g_obs(r))) at R_e and at the census edge, divided by t(z); census edge (f_ret 0.1, 1), turnaround radius of the catchment M_ta = M_b/(f_ret f_b) at mean density 5.55 rho_m(z), and r_200c of the same mass. Labelled DESCRIPTIVE. One figure: rho_DE, rho_m, a0, cH and typical g_bar(R_e)/a0 vs cosmic time.

Tautology declared now: a0/(cH) = kappa sqrt(3 Omega_DE(z)/(8 pi)) follows from the definitions; it is labelled TAUTOLOGICAL whatever its value, and "a0 ~ cH0/2pi" holds iff Omega_DE = 2/(3 pi kappa^2).

## 2. TEST (a): cold-energy fraction inside R_e vs z (RC100)

Sample: the 100 RC100 galaxies with finite fDM_within_Re, z, and native g_bar_B, g_obs (expected 100; the count is reported).

Models per galaxy at its z, each footing: FLAT a0(0); DESI a0(0) sqrt f(z) (central as in §1); RIVAL a0(0) E(z); NEWTON (a0 -> 0, f = 0; MUTATE). Prediction f_pred = 1 - 1/nu(g_bar_B / a0(z)).

Observed routes: O1 = published fDM_within_Re (primary, MODEL-OTHER); O2 = 1 - g_bar_B/g_obs (native, self-consistent baryons; may be negative).

Statistics:
- Bins: z quartiles (4 bins, 25 each by rank). Per bin per model: median(O) - median(f_pred), bootstrap 2000 resamples (seed 547) of galaxies, paired.
- Systematic (shared; declared): sys_bin = half the range of median f_pred over the 3x3 grid gas x 10^{-0.2,0,+0.2}, M* x 10^{-0.1,0,+0.1}, g_bar rescaled as g_B (10^dM + 10^dg mu)/(1 + mu) with CFG303's mu_t18 column.
- Z_bin = (median O - median f_pred) / sqrt(sigma_boot^2 + sys_bin^2).
- Slope: OLS slope of O on z vs OLS slope of f_pred on z; Z_slope = (s_O - s_pred)/sqrt(sigma_boot(difference)^2 + sigma_tilt^2), sigma_tilt = half range of s_pred when gas is scaled by 10^{+-0.15 (z - median z)}.

Verdict per model per route:
- TENSION (Z) if any |Z_bin| >= 2 or |Z_slope| >= 2 (report max |Z|; >= 3 called strong), else CONSISTENT.
- "The observed decline follows from compact high-z baryons under fixed a0" = YES iff (i) s_O < 0 with s_O/sigma_boot <= -2, (ii) FLAT's s_pred < 0, (iii) FLAT is CONSISTENT on O1 by the rule above. Reported separately for both footings and both routes.
- Calibration wall: in each bin compute sep = |median f_pred(FLAT) - median f_pred(RIVAL)| (and FLAT vs DESI). A bin is diagnostic for that pair only if sep > 2 sqrt(sigma_boot^2 + sys_bin^2). DISCRIMINATING (model named) only if >= 2 bins are diagnostic and in those bins one model has max |Z| >= 3 while the other has all |Z| < 2, on both routes. Otherwise the pair is NOT DIAGNOSTIC. FLAT vs DESI is expected NOT DIAGNOSTIC (±0.04 dex).
- Route rule: if O1 and O2 give different verdict words for a model, that model's test (a) verdict is ROUTE-DEPENDENT -> NOT DIAGNOSTIC.

MUTATE (`CFG547_MUTATE=1`, separate outputs): (M1) NEWTON must be TENSION on O1 with |Z| >= 3 in at least one bin (data show f_DM > 0); (M2) shuffle z across galaxies 200 times (seed 547), keeping each galaxy's (g_bar, O1, O2) together: the observed O1 slope must vanish — median |s_shuf| < |s_real|/3 and at most 10% of shuffles with |s_shuf/sigma| >= 2 (only meaningful if the real slope is significant; else reported). (M3) in the shuffled set the FLAT-vs-O1 bin residual pattern is reported (no requirement).

## 3. TEST (b): the switch-on epoch

z_on(M*, k, footing) = the highest grid redshift (fine grid dz = 0.01 for this test, z <= 6) at which g_bar(k R_e)/a0(z) <= 1 for the typical galaxy, k in {2, 3}, log M* in {10.0, 10.7}, FLAT a0 (8 values). If g_bar(k R_e) < a0 at all z <= 6, z_on is reported as "> 6 (always in the law's regime)"; if never below a0 at z >= 0, "never".
Dark-energy epochs (Lambda background and the DESI chain medians): z_eq where rho_DE = rho_m, and z_acc where q = 0.
Rule: COINCIDENCE CANDIDATE iff all 8 z_on are finite and lie within ±0.15 of z_eq or of z_acc (one of them, for all 8). Otherwise NO ROBUST EPOCH. Any candidate is additionally labelled NOT DERIVED unless an equation of the framework fixes z_on without the galaxy size–mass relation (none is expected; the sizes are astrophysical inputs). RIVAL and DESI z_on are reported, no verdict.

## 4. TEST (c): other relations from the table

Declared now, before the table exists:
- C1 a0/(cH) vs z: TAUTOLOGICAL (§1).
- C2 the redshift where the census edge (f_ret 0.1) equals the catchment turnaround radius, per mass: DESCRIPTIVE.
- C3 the redshift where t_ff(r_edge) equals the age t(z): DESCRIPTIVE (where settling to the edge is possible within the age).
- C4 the power-law index p of g_bar(R_e)/a0 propto (1+z)^p (fit 0 <= z <= 3), per mass, FLAT: DESCRIPTIVE.
No data test is run in (c): no rule for comparing C2–C4 with data can be written without new inputs. Any relation that appears is reported as a candidate for a future frozen lane, never as a finding.

## 5. Controls (main run exits non-zero if any fails)

- K1 canonical a0(0) recomputed from kappa c sqrt(G rho_Lambda) at H0 = 67.4, Omega_Lambda = 0.685: within 0.5% of 9.36e-11.
- K2 the thin-disc g_bar reconstructed from logMstar_SED_col6, mu_t18, R_e reproduces CFG303's g_bar_native_B to 1e-6 relative for all galaxies.
- K3 DESI a0(2.5)/a0(0) per SN chain matches CFG511's recorded medians (pantheonplus 0.827, union3 0.782, desy5 0.798 within ±0.01).
- K4 Lambda: z_acc = (2 Omega_L/Omega_m)^{1/3} - 1 and z_eq = (Omega_L/Omega_m)^{1/3} - 1 reproduced to 1e-3.
- K5 age t(0) for the Lambda background within 1% of 13.8 Gyr (13.80 at these parameters ±0.15).

## 6. Rules

Numbers in the README come from the JSON. Fails verified as hard as passes. Never "data favour the framework". Calibration-wall rule (CFG217/385) applies via §2. Deliverables: TIMELINE.md, script, .out / _MUTATE.out, results JSON (main and MUTATE), README, one figure. nice -n 10, <= 2 threads.
