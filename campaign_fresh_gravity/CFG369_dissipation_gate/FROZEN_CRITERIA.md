# CFG369 FROZEN CRITERIA: does dissipation (baryon cooling) settle the cold fluid into the phantom? A four-way swing

Committed alone, before any script. kappa = 1/2 FITTED and fixed. nu_mono. No dark-matter particle species: the cold MASS is
still required and is kept. No knob scans (every bracket is declared and each cell reported). Never "theory closed". Owner
(2026-10-06, chat "Nobel Prize and neutrinos"): "yeah dude", then "swing as much as you can that is new please so we can reduce
the scope enough to get to an answer". The orchestrator was told first. This lane reads cm12 (cooling machinery) read-only.

**Hypothesis (from cm12-cm15 + CFG245 + CFG363-366).** The cold fluid settles into the phantom configuration only where
baryons can radiate away the energy the fluid must lose (CFG245 E1). The coupling is gravity-only (G9 safe). Where gas cools,
the result is the law with no excess. Where gas cannot cool (UFDs below 1e4 K, hot hosts above ~1e6 K), the fluid stays
unsettled and appears as excess mass. If the settling rate follows the cooling rate, CFG245's pincer would be resolved.

## S1 ENERGY (is there enough radiated energy at all?)
- Required: E_req = q x (1/2) M_b V_f^2 with q in {0.49 (CFG245 E1 generous low), 9.5 (generous high)} (CFG245 README).
- Available: gas settling in the deep-MOND logarithmic potential radiates E_rad = M_b V_f^2 ln(r_in/R_d), with
  r_in in {r_M, 10 r_M} (r_M = sqrt(G M_b/a0)) and R_d the SPARC disk scale length.
- epsilon_min = E_req/E_rad, per SPARC galaxy (Q <= 2, Rdisk > 0). Statistic: the median.
- ALLOWED if median epsilon_min <= 1 at q = 9.5. MARGINAL if <= 1 only at q = 0.49. FAIL if > 1 even at q = 0.49
  (r_in = 10 r_M, the generous end).

## S2 RATE PINCER (does the cooling rate land in CFG245's window?)
- Gamma_cool = 1/t_cool from cm12's `ratio()` (t_cool at R1 = r_M or R2 = the 200 rho_b radius; f_hot in {1, 0.5};
  Tozzi & Norman cooling). Units: H_Lambda = H0 sqrt(Omega_Lambda).
- Needed: a galaxy at M_b = 6e10 Msun has Gamma >= 1.73 H_Lambda (T-RAR line, canonical) AND a cluster at M_b = 1e14 Msun has
  Gamma <= 1.93 H_Lambda (C1 generous max). Central cluster line 1.04 reported.
- PASS if at least one of the 4 cells (R1/R2 x f_hot) passes both on the canonical footing. Alt reported.

## S3 LEVELS (no fit)
- The predicted unsettled fraction e(M) = exp(-epsilon Gamma_cool tau), with epsilon = 1 (maximal coupling) and tau = 10.3 Gyr
  (since z = 2). Gas below 1e4 K does not cool, so e = 1 (UFD direction).
- Measured (cm08/cm03/X-COP): galaxies 0.13 +- 0.05 at M_b = 6e10; groups 0.60 +- 0.15 at M_b = 5e12; clusters 0.58 +- 0.15 at
  M_b = 1e14.
- PASS if at least one cell matches all three within the bands. Report e(M) per cell.

## S4 SHAPE under the gravity-only conservative limit (adiabatic contraction)
- Initial: fluid and baryons mixed as a truncated SIS, M_i(<r) proportional to min(r/R_i, 1). Fluid total =
  5.364 x M_b,tot (present-baryon share; CFG364's convention). R_i in {r_M, 10 r_M}.
- Final baryons = the SPARC profile (M_b,f(<r) = V_bar^2 r/G). The fluid contracts by Blumenthal: r_i M_tot,i(r_i) =
  r_f [M_c,i(r_i) + M_b,f(r_f)].
- Compare M_c,f(<r) with the law phantom M_ph(<r) = (nu_mono - 1) M_b,f at every SPARC radius: rms of log10(M_c,f/M_ph)
  over Q <= 2 galaxies, and the trend with g_bar (slope of the residual vs log g_bar).
- PASS if rms <= 0.10 dex and abs(slope) <= 0.10. Otherwise the gravity-only ADIABATIC route fails and the coupling must be
  non-adiabatic (CFG60).

## Lane verdict (declared)
- ALIVE: S1 not FAIL, S2 PASS and S3 PASS.
- DEAD: S1 FAIL, or S2 fails in every cell.
- PARTIAL: anything else. Name what failed.
- S4 sets the class: adiabatic (S4 PASS) or non-adiabatic, needing a new ingredient (S4 FAIL).
- Both footings, never pooled. Canonical is primary.

## Controls
- C1: cm12's `ratio()` imported read-only reproduces cm12's committed crossing M_b* for canonical R1 f_hot 1 (to 0.01 dex).
- C2: the Blumenthal solver conserves the fluid mass (to 1e-6), and returns the identity when M_b,f = M_b,i.
- MUTATE: cooling function x 100 (cm12's own MUTATE knob). S3's e(MW) must change by > 0.1, rc 1.

Local compute only. No downloads.
