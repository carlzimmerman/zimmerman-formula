# Frozen before any number: LCDM-flavoured recipes against the law, on real SPARC baryons

Rival-flavoured exercise. Not a framework result, not a derivation, adopts nothing. Dark matter appears only as the rival's language. kappa = 1/2 FITTED; not theory closed.

**Question:** how exactly can LCDM's own knobs reproduce the law g_N = g^2/(g + a0), a0 = 9.3625e-11 m/s^2, on the measured baryon distributions of real galaxies, and what does each match cost? The earlier toy (`../REDTEAM_LCDM_PRIEST/`) used smooth model discs. This one uses the rotmod baryon curves, so surface-density diversity is real.

**Sample:** all SPARC `real_research/data/sparc_data/*_rotmod.dat`. Y_disk 0.5, Y_bul 0.7, fixed. g_b = |V_b^2|/r with the rotmod's signed gas. Radii as measured. Galaxies with fewer than 5 points are dropped. Target = the law's curve on those baryons, not the observed curve. The observed curve is a separate control, reported beside it.

**Targets, on all points pooled**
- E1 exact: rms of log g_total - log g_law <= 0.02 dex. This is about the law's own intrinsic-scatter scale on SPARC, and small against the data's roughly 0.13 dex observed scatter.
- E2 no galaxy left out: 95th percentile of per-galaxy rms <= 0.04 dex.
- E3 flat across acceleration: |mean residual| <= 0.02 dex in every g_b bin of width 0.5 dex holding at least 50 points.
- E4 slope: d ln a / d ln rho_DE = 0.50 +- 0.05.
- E5 redshift: a(z)/a(0) inside the law's band at z = 1, 1.5, 2.33: [0.76, 1.03], [0.71, 1.12], [0.33, 1.21]. E4 and E5 are read from how the recipe's scales are written, and each scale that has to be written by hand is counted as a hand-inserted term.

**Recipes, cheapest first**
- R1 abundance-matched contracted NFW: SHMR and Diemer19 c(M) on Y-fixed M_b, global knobs: c norm, c mass slope, SHMR norm, contraction fraction.
- R2 feedback core: coreNFW-style core on R1 with core radius eta R_half, n set by M*/M200 with a global norm and slope.
- R3 thermal halo: isothermal Jeans in the galaxy's own baryon potential, with sigma and central density from two global laws, sigma^4 = s G M_b a0/4 and rho0 r_c = Sigma*. Knobs s, Sigma*.
- R4 thermal halo, per galaxy: rho0 and sigma free per galaxy.
- R5 exact halo: M_DM(r) = r^2 (g_law - g_b)/G per galaxy.

**Checks that R5 must face, whichever way they land**
- C1 density positive at every measured radius.
- C2 Jeans: isotropic sigma_r^2 positive, and its size against V^2.
- C3 Eddington: f(E) >= 0 for the spherical isotropic halo in the total potential. Failing means no isotropic equilibrium.
- C4 origin: invert Blumenthal contraction to the initial halo. Fit NFW to it. Report rms, implied c and M200 against Diemer19 c(M) and against the SHMR.
- C5 implied M200: from the recipe's halo at the 200-critical radius, against abundance matching.

**Reported whichever way it lands.** Passing E1 to E5 by construction says how much freedom there is. It isn't evidence for or against the law or LCDM. Inherited failures of the law (IC 1613, X-COP, and the rest of PAPER67's record) stay inherited; matching the law means missing what it misses.

**AMENDMENT A1, after the first run's numbers, disclosed as such.** First run: `scripts/recipe.out`, stays on record. Targets E1 to E5 unchanged. Added, because mass-only global knobs stalled near 0.07 dex and the Eddington pass had no control:
- R3 recheck: restart from s = 1, G Sigma*/a0 = 0.27 (R4's medians), since a two-knob fit landing at s = 2.7 may be a poor optimiser result.
- R6 one function: g_DM = g_b/(1 - exp(-sqrt(g_b/g_dagger))) - g_b, fit g_dagger, the published empirical form.
- R7 surface-density coupling: R1 + R2 knobs plus c and M200 each scaling as a power of M_b/R_d^2. Tied to the size-concentration link in the rival's language.
- R8 per-galaxy: M200, c, contraction fraction, core exponent free per galaxy, wide. R8p the same inside what a referee would accept: c within 0.11 dex of Diemer19, M200 within 0.3 dex of abundance matching.
- J joint hand terms: on R7, c gets (rho_DE/rho_DE0)^p (1+z)^q with one p and one q for all of E4, E5 and kappa at (OL, H0) = (0.70, 67.4), (0.685, 73), (0.65, 73) within 5 %. Baryons held fixed at each z, which is unphysical and is stated.
- C3 control: the same Eddington code must return negative f for a cored tracer in a Keplerian potential, and positive for Hernquist.

**BUG FOUND IN J, after its numbers.** `setcos` swapped the cosmology object but not colossus's current cosmology, so c(M) in every J row came from the last cosmology created (the base a read 1.46e-10 against R7's 9.21e-11). The wrong output stays as `scripts/recipe2_before_cosmology_fix.out`. Fixed and rerun as `recipe2.out`. The same pattern hit the redshift rows of `../REDTEAM_LCDM_PRIEST/scripts/tune.py`; corrected there too.

**AMENDMENT A2, owner 11-02: "use the knobs ACDM has". Frozen before these numbers; targets E1 to E5 unchanged.** LCDM parts only, no empirical function, no law-shaped halo.
- R9 per galaxy, six knobs: M200, c, Einasto alpha, contraction fraction, core exponent n, core radius eta. Priors: 1 sigma row c 0.11 dex, M200 0.3 dex; 2 sigma row c 0.22 dex, M200 0.6 dex. Both rows: alpha 0.10 to 0.30, fraction -1 to 1, n 0 to 1, eta 0.3 to 3.
- R10 one global recipe: each of the six knobs is a quadratic function of log M_b, log surface density and gas fraction. Tuned on odd-numbered galaxies, graded on even-numbered ones, which it never saw. Also reported tuned on all.
- J2 jointly on R10: c times rho_DE^p H0^r and M200 times H0^s, one set for E4 and kappa within 5 % at the three cosmologies; c times (1+z)^(q1 + q2 z) for E5. Every one of these is a hand term and is counted. Baryons fixed in z, unphysical, stated.

**AMENDMENT A3, owner 11-02: use the supernova feedback knobs. Frozen before its numbers; targets unchanged.** R11 is one global recipe with 12 knobs, an analytic stand-in for subgrid feedback, not a hydro simulation. The mapping from knob to halo is mine, not taken from any simulation's parameter file, and the ranges are my judgement.
- Stellar mass outcome, 4: SHMR norm (+-0.54 dex), log M1 (+-0.9), beta (+-1.2), gamma (+-0.6).
- Feedback energy, 4: e = eps (M*/M200/0.01)^a1 (Sigma_b/100)^a2 (f_gas/0.5)^a4; core exponent n = tanh(e). eps 0.01 to 30; a1, a2, a4 in -3 to 3.
- Core size, 2: eta = eta0 (M*/1e9)^a3. eta0 0.1 to 10; a3 -1 to 1.
- Contraction versus expansion, 2: f = f0 + f1 log10(M_b/10^9.5), clipped to -1..1. f0 -1 to 1; f1 -1 to 1.
c stays at Diemer19, alpha at 0.16: feedback only. Tuned on odd galaxies, graded on even; also tuned on all. Plus the wider R11b with c norm and c slope free, 14 knobs.

**AMENDMENT A4, owner 11-02 "keep going". Frozen before these numbers; targets unchanged. Post-deposit; none of this is in v1.0.** Three questions the deposit left open. Still an analytic stand-in.
- T1 optimiser convergence: every R11, R11b fit stopped at max_nfev 25. Restart each from its recorded knobs with max_nfev 200 inside the same bounds, same odd/even split for the tuned-on-odd rows. If E1 to E3 pass for a global recipe, that closes "no global recipe reaches 0.02". A number that moves by less than 0.001 dex is called converged.
- T2 real halo scatter: the deposited recipes give every galaxy the mean c(M) and the mean SHMR. Real halos scatter. Hold T1's R11 and R11b knobs fixed and draw per galaxy log c scatter 0.11 dex alone, then with log M200 scatter 0.15 dex too, 40 seeds each, independent between galaxies. Report rms to law and rms to observed, median and 16-84 over seeds. Gate S: median rms to observed <= 0.205 dex, i.e. no more than 0.01 dex above the law's 0.1951. Limit stated: feedback correlated with halo scatter could cancel some of this, and independent draws do not allow for that.
- T3 past the last measured point: the fits see only measured radii. With T1's knobs, compare recipe and law at r = 30, 50, 100, 200, 300 kpc beyond each galaxy's last point, baryons as a point mass M_b, halo as the recipe's outside its fit range, no two-halo term. Report the median log(recipe/law) by g_b and the first g_b where the absolute median passes 0.1 dex. Prediction comparison only. No data graded, so no statement on which is right.
