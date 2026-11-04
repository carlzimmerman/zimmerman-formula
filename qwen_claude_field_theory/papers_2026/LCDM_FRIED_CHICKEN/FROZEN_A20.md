# FROZEN A20: interacting vacuum and the systematic reading

Frozen before any A20 number. Script `scripts/recipe22.py`, output `scripts/recipe22.out`. Quarantined experiment: rival language, adopts nothing, never feeds anything outside this folder. Passing shows freedom, not evidence. kappa = 1/2 FITTED; not theory closed.

Known before freezing (A15 U1, `recipe17.out`): plain LCDM NFW central acceleration 2 pi G rho_s r_s on the SPARC SHMR halos has median 0.612 a0, rms 0.156 dex, kappa_eff 0.306, and rises 1.079, 1.199, 1.493 at z 1, 1.5, 2.33 at the median log M200 11.14.

## (a) Interacting vacuum, dark matter exchanging energy with the vacuum

Model. Flat, no radiation, H0 67.4, Om0 0.315, Ob0 0.0493 held fixed today (today's densities are the observed ones). Baryons a^-3. rho_c' = -3 rho_c - Q/H, rho_v' = +Q/H (prime = d/dln a). Two coupling types, both run:
- Q1: Q = xi H rho_c (xi > 0: dark matter decays into vacuum). rho_c = rho_c0 a^-(3+xi), rho_v = rho_v0 + xi rho_c0 (1 - a^-(3+xi))/(3+xi).
- Q2: Q = xi H rho_v. rho_v = rho_v0 a^xi, rho_c a^3 = rho_c0 - xi rho_v0 (a^(3+xi) - 1)/(3+xi).
Perturbations: geodesic dark matter (energy transfer along the dark matter 4-velocity, no momentum transfer), vacuum homogeneous. Then delta_c' = u + q delta_c, delta_b' = u, u' = -(1 + dlnH/dlna) u + 1.5 (Omega_c delta_c + Omega_b delta_b); q = 0 for Q1 (the delta Q term cancels), q = xi rho_v/rho_c for Q2. Start a = 1e-3 in matter domination. Growth D = delta_m normalised to 1 today (sigma8 fixed today). Derived here, not checked against a paper; treated as from memory.

Concentration mapping (Ludlow et al. 2014 style, constant C = 400 from memory): mean density inside r_s, rhobar_s = 200 rho_crit(z) c^3 mu(1)/mu(c), equals C rho_crit(z_f). For each M200 and observing z, z_f^LCDM is read off the Diemer19 c in LCDM. The IV formation epoch keeps the same collapse condition, 1/D_IV(z_f) - 1/D_IV(z) = 1/D_L(z_f^L) - 1/D_L(z). Then rhobar_s,IV = C rho_crit,IV(z_f,IV), and c_IV solves the same identity with rho_crit,IV(z). M200 per galaxy from lib's SHMR (unchanged, stated). Control: at xi = 0 the map returns the LCDM c, g reproduces A15's 0.612 a0.

Scan: xi in [-0.5, 0.5] for Q1 and [-1, 1] for Q2, 41 values each, skipping any xi with rho_v or rho_c < 0 below z = 10. Range judgement (from memory, not verified): CMB+BAO allow |xi| of order 1e-3 to 1e-2 for Q1 and of order 0.1 to 0.5 for Q2; wider values scanned to show where (if anywhere) the target sits; a hit outside the plausible range is reported as such.

Gates (for each xi; one knob xi):
- K1 kappa_eff = median_i g_i / (c sqrt(G rho_v0)) within 0.05 dex of 0.5.
- K2 flat in z: kappa_eff(z)/kappa_eff(0) = [g(z)/g(0)] / sqrt(rho_v(z)/rho_v0) at the median M200, within 0.05 dex of 1 at z 1, 1.5, 2.33.
- K3 band: g(z)/g(0) inside [0.76,1.03], [0.71,1.12], [0.33,1.21].
- K4 spread: rms of log g_i over 171 galaxies <= 0.1 dex.
- Law swap: law with a = g_i per galaxy graded by lib.grade (E1 <= 0.02, E2 <= 0.04, E3 <= 0.02, rms to observed reported) at the xi that best fits the law on all data; holdout: xi tuned on GS[::2], unseen rms to law on GS[1::2] <= 0.025.
- Report knobs at bound.
Verdict: the IV supplies the tie only if K1 to K4 and the swap gates all pass at one xi.
Expected: NO. Raising kappa_eff from 0.31 to 0.5 needs denser early halos (more dark matter in the past, xi > 0 in Q1), which makes rho_v smaller in the past, so sqrt(rho_v) falls with z while g rises: K1 and K2 pull opposite ways. K4 and E1 fail at every xi, since xi moves the scale nearly uniformly in mass and leaves the 0.156 dex spread.

## (b) Systematic reading

Mock: for each SPARC galaxy, true Upsilon_disk,bulge = nominal (0.5, 0.7) x 10^N(0, 0.1); M* true = Ms x that factor; M200 = m200_of(M* 10^N(0, 0.15)) (SHMR scatter 0.15 dex taken in M* at fixed halo, no mass-function weighting, stated); c = Diemer19 x 10^N(0, 0.11); halo (1 - f_b) NFW. Two variants: no contraction, and full Blumenthal contraction (lib.r1 with f = 1). True g = g_b,true + g_DM at the catalogue radii and distance. Observation: D_obs = D (1 + N(0, e_D/D)) from the SPARC table, i_obs = i + N(0, e_Inc) clipped to [15, 89] deg, V_obs = V_true sin i/sin i_obs + N(0, errV) from the rotmod files (clipped at 1 km/s); observer radii scale with D_obs/D, baryon V^2 by D_obs/D.
Observer fit (applied identically to real SPARC and to the mock): per-galaxy log Upsilon offset u (disc and bulge together) with Gaussian prior 0.1 dex, bounded +-0.3 dex, and one global a0, fitted by alternation (6 passes) minimising sum over points of (log g_obs - log law(g_b(u), a0))^2 / 0.1^2 + u^2/0.1^2 per galaxy. RAR scatter = rms of log g_obs - log law over all points. 5 mock realisations, mean and spread reported.
Gates: B1 |scatter_mock - scatter_SPARC| <= 0.02 dex; B2 |log10(a0_mock/A0)| <= 0.05 dex. Also reported: SPARC's own fitted a0 against A0; kappa_eff = a0_mock/(c sqrt(G rho_DE)) against 0.5 within 0.05 dex; z evolution of the noiseless mock's fitted a0 with the same halo masses at z = 1, 1.5, 2.33 (Diemer c(M, z), R200 at z) against the band; lib.grade of the noiseless nominal-Upsilon mock (no knobs tuned on the law, so the holdout is the unseen rms on GS[1::2] of that same mock); knob count 0 tuned (3 scatter amplitudes fixed from the literature).
Expected: B1 FAILS, mock scatter larger than SPARC's by more than 0.02 dex (halo concentration and SHMR scatter add intrinsic spread the observer's Upsilon cannot absorb); B2 uncertain, lean fail; E1 fails. Contraction does not rescue B1.

## RESULTS (written after the run; criteria above unchanged)

No bug found. After the first run, disclosed diagnostics (not gates) were added; the first output is kept as `scripts/recipe22_pre_diagnostic.out` and every gate number in `scripts/recipe22.out` is identical to it. Runtime 17 s, 81 MB RSS.

(a) Control at xi = 0 reproduces A15 (0.612 a0, kappa_eff 0.306). Q1 with xi > 0 (dark matter decaying into vacuum) is skipped at every scanned value: rho_v goes negative before z 10, as the background formula implies. Q1 xi < 0 barely moves the scale (kappa_eff 0.306 to 0.314). Q2 xi -0.50 to -0.60 (vacuum into dark matter) reaches kappa_eff 0.47 to 0.54 (K1 pass), but then kappa_eff falls with z (flat ratios 0.76 to 0.85 at z 1.5 to 2.33, K2 FAIL), and H(z) is 10-24 % below LCDM by z 1 to 2.33 (diagnostic). K2 alone passes for Q1 xi -0.40 to -0.175 and Q2 -0.30, where K1 fails. K4 (spread <= 0.1) fails at every xi (0.149 to 0.159 dex). No xi passes K1 to K4 jointly. Law swap at the best xi (Q2 -0.45): E1 0.0576, E2 0.1075, E3 0.0556, rms to observed 0.1940; holdout unseen 0.0546. Verdict: NO TIE, not exact. Expected outcome confirmed for K1/K2 opposition and K4; the K1 pass at Q2 xi near -0.55 was not expected and sits at the edge of the range judged plausible.

(b) Observer fit on real SPARC: RAR scatter 0.1489 dex (all 3373 points), a0 8.03e-11 (-0.066 dex vs lib A0). Mock, 5 realisations: no contraction scatter 0.1665 +- 0.0073 (B1 PASS, +0.018), a0 1.58e-10 (+0.228 dex, B2 FAIL), kappa_eff 0.85; contracted scatter 0.1553 +- 0.0093 (B1 PASS, +0.006), a0 2.43e-10 (+0.415 dex, B2 FAIL), kappa_eff 1.30. Noiseless mocks: E1 0.142 / 0.223, holdout 0.131 / 0.212, fitted a0 rises 2.6x / 2.2x by z 2.33 (band FAIL). Verdict: DOES NOT REPRODUCE. The B1 pass is against my expectation, and is weak: the all-points scatter is dominated by SPARC's listed velocity errors, which the mock adds. On points with errV/Vobs <= 0.05 (diagnostic, chosen after the run) the mock gives 0.114 / 0.110 dex against SPARC's 0.081, outside 0.02; the mock with no observational errors already has 0.091 / 0.083 intrinsic scatter. The main failure is the scale: plain LCDM halos put the fitted a0 0.23 to 0.42 dex above A0.
