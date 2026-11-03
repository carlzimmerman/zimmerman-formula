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

**AMENDMENT A5, owner 11-02 "Yes, grade lensing". Frozen before these numbers; post-deposit, not in v1.0. T3's numbers were seen first, so this is not blind to the fact that the models differ, but nothing here has been compared with lensing data yet.**
- Data: Brouwer+2021 KiDS-1000 isolated lenses, Fig-3 ESD files, four stellar mass bins, log M* edges 8.5, 10.3, 10.6, 10.8, 11.0, 15 radii each from 35 kpc to 2.6 Mpc, full covariance, bias corrected as their README says. Local copy, no download.
- Lenses: `lr_lenses.npz` isolated sample, logM and Mgal per lens. Each bin is a number-weighted stack of 25 mass quantiles. This is the repo's own re-selection, not B21's exact lens list. Disclosed.
- Models, nothing refitted: L plain law, point mass Mgal, a0 9.3625e-11, no edge, no two-halo, lensing mass taken as dynamical mass. R11 and R11b at the T1 knobs printed in `recipe5.out`, truncated at R200, plus a two-halo term b(M200, z) rho_m xi_mm with Tinker10 bias. C base LCDM control: same code with SHMR at base, Diemer19 c, no core, no contraction, plus two-halo.
- Recipe inputs SPARC does not supply for these lenses: R_d from a log R_d - log M_b line fit on SPARC, f_gas from Mgal and M*. These lenses are mostly outside the recipes' tuned range; that is part of the test.
- Grade: chi2 with full covariance on all 60 points, nothing fitted, gate p >= 0.01. Also reported: chi2 on R <= 1 Mpc (less two-halo), per-bin chi2, and one fitted amplitude A with its error as a diagnostic only.
- Sensitivity rows: M* and Mgal +-0.1 dex for every model; recipes with c and rho_crit at z = 0.25 instead of z = 0.
- Controls: SIS projection against sigma^2/(2 G R), point mass against M/(pi R^2).
- Limits stated whichever way it lands: analytic stand-in; recipes built at z = 0; isolation not modelled in the two-halo bias; satellites not modelled; the covariance is B21's analytic one; a pass is not evidence either theory is right, and the law's other failures stay on record. Grades these models on these lenses only.

**A5 POST-RESULT DIAGNOSTIC, written after the main rows, not part of the frozen grade.** All four models failed; the law came out at A 1.367 and earlier lanes (CFG801, CFG810) report poor absolute fits with all models on this file. To check whether lens masses alone explain it: per bin, one shift of log M* and log Mgal from -0.3 to +0.5 dex in 0.1 steps, chosen by the bin's own chi2, then full-covariance chi2 on 60 points with 56 dof. Run for L, R11, R11b. Four extra parameters, post hoc, so it can show how much a mass offset could absorb and cannot rescue a grade.

**AMENDMENT A6, owner 11-02 "reverse engineer it to match my core framework". Frozen before these numbers; post-deposit, not in v1.0.** R12: define the CDM halo from the law, M_DM(r) = r^2 (g_law - g_b)/G, with a = kappa c sqrt(G rho_DE(z)), kappa = 1/2 written in by hand. Exact by construction, so E1 to E5 passing says nothing except that the construction works. It reports freedom, not evidence.
- Grade E1 to E5, and kappa and a at the three cosmologies of J. rho_DE constant in z here (w = -1).
- Costs, reported whichever way they land: implied M200 from M(<R200) including baryons against the SHMR on SPARC; M_b/M200 against the cosmic 0.156; how many free functions; what physics would have to carry rho_DE into a CDM halo. R5's C1 to C4 stand.
- Lensing, same grade as A5: R12 truncated at its own R200 plus the A5 two-halo term; R12n no truncation, no two-halo, which must reproduce the A5 law row at 276.1 as a control. Sensitivity +-0.1 dex.

**AMENDMENT A7, owner 11-02 "swing deeper". Frozen before these numbers; not in any deposit.** Tests of the particle reading of R12, rival language only.
- M1 mixing theorem (Tremaine, Henon, Lynden-Bell 1986): collisionless evolution cannot raise the excess mass D(f0) = integral of (f - f0)+ over phase space at any f0. Final = R12 by Eddington in its total potential, smoothed baryons as in R5. Initial = NFW with the same dark mass inside R200, c Diemer19 at R12's M200. Both isotropic and spherical, which is an assumption about the initial and final states. f0 grid: 30 log steps across f(E) between the first and last measured radii. Allowed if D_final/D_initial <= 1.05 at every f0; the 5 % is numerical slack, checked by controls. Rows: c at Diemer19; c at -0.22 dex, stingier; c at +0.22 dex, generous. Passing is necessary, not sufficient. A fail means that galaxy cannot be reached collisionlessly from that start.
- Controls: NFW to itself must give ratio near 1 and pass. c x4 final must fail. c /4 final must pass.
- M2 energy: self-binding energy of dark mass inside R200, R12 minus initial NFW, against 1e49 erg per solar mass of stars (all supernova energy, 100 % coupled). Reported as a ratio per galaxy, split by sign. Baryon infall work is not included.
- M3 scattering carrier: if tracking is by dark-baryon scattering, one momentum exchange in 13 Gyr needs sigma/m = 1/(rho_b v t), read at g_b = a0 and at the last measured radius, heavy-particle limit. Reported in cm^2/g. Long-range carriers are not covered. No external limit is graded here.

**A7 CONTROL FAILURE, after the first numbers.** The frozen control "c /4 final must pass" gave 0 of 13, and "c x4 must fail" allowed 2 of 13. M1's verdicts are not usable until this is explained. Diagnostic, `scripts/recipe9b.py`, written after seeing that: (a) Eddington against the analytic Hernquist f(E); (b) an exact mixing control, f block-averaged over phase volume, which must not raise D; (c) where in f0 the worst ratio falls, for the controls and for R12: rank 0 = lowest f0, outer halo; rank 28 = highest, inner halo.

**A7 control reading, post-result.** The code checks out: Hernquist median ratio 0.990, range 0.977 to 1.444, mass 1.060; exact block mixing max ratio 1.000. The frozen c /4 expectation was mine and wrong: in an NFW cusp f at fixed r goes as (rho_s r_s)^(-1/2), so lower c is colder inside and has more excess mass at high f0, and the worst ratio sits at the top f0 as that predicts. This scaling was worked out after seeing the failure. So a c rescale is not a valid mixing control, and block mixing replaces it, post hoc. M1's numbers stand as computed, on that disclosed footing. The script's "12 galaxies" label is 13.

**AMENDMENT A8, owner 11-02: particle properties for outreach, "we know its not a particle". Frozen before these numbers; not in any deposit. Effective description only, rival language, adopts nothing, the no-particle rule stands outside this exercise. Stands on the a0 law; the cold sector stays retired (owner 11-01). CFG122 gave standard Berezhiani-Khoury a scoped no-go against the target density; that stands.**
- P1 field equation: a static scalar whose acceleration y obeys y^2/(a0 - y) = g_N reproduces the law exactly, so mu(y) = y/(a0 - y). Check on all SPARC points to 1e-10. Report max y/a0, and the radial to tangential stiffness ratio (2 a0 - y)/(a0 - y).
- P2 scale: Lambda from a0 = alpha^3 Lambda^2/M_Pl, reduced M_Pl, at alpha = 1, against rho_DE^(1/4) from a0 = kappa c sqrt(G rho_DE). The tie is written in by hand.
- P3 condensate window, the gate: boson with rho h^3/(m^4 sigma^3) >= 1 at the last measured radius in all 171 SPARC galaxies gives an upper bound on m. Not condensed at 100 kpc in M_b 1e13 and 1e14 point-mass clusters gives a lower bound, because the law misses there. rho and sigma from R12's Jeans solution. WINDOW if lower < upper. Also report the fraction of SPARC condensed at each m on a grid.
- P4 thermalisation: sigma/m from one scatter in 13 Gyr at the last measured radius, no Bose enhancement and with it (factor rho h^3/(m^4 sigma^3)), at the window's edges.
- P5 relic: thermal mass that would give Omega_c h^2 = 0.12, showing the window must be non-thermal if it is below keV. Misalignment decay constant f for m on the grid, order of magnitude, control: m = 1e-22 eV should give f near 1e17 GeV.
- P6 fifth force at high g: y at 1 AU and Saturn against the record's Cassini failure (PAPER58, CFG770). Read from the record, not re-derived.

**AMENDMENT A9, owner 11-02: "assume its a particle". Pitch stays the a0 law. Frozen before these numbers; not deposited.** Axiom for this exercise only: all of g_law - g_b is the gravity of a real particle halo, baryons feel only gravity, and no scalar force acts on baryons. That removes double counting by definition. Consequences derived, not proof the particle exists; galaxy fits cannot prove that.
- A1 one equation of state: hydrostatic P(r) from the R12 halo on SPARC. Gate: rms of log P at fixed log rho <= 0.1 dex across galaxies means one barotrope is possible. Analytic deep-tail expectation written in advance: sigma^2 = sqrt(G M_b a0)/2, so P at fixed rho scales as sqrt(M_b), and the gate should fail.
- A2 temperature law: sigma at the last point against (G M_b a0/4)^(1/4), median and scatter. Reported also as m sigma^2 at 10 eV.
- A3 Solar System: a halo of dispersion sigma cannot be bound to the Sun beyond r = 2 G M_sun/sigma^2. Use a Milky Way point mass M_b 6.5e10 at 8 kpc for rho and sigma. Report extra acceleration at Saturn from smooth local density against a0, gate < 1e-3 a0. The expected consequence: no a0 tail near stars, so wide binaries are Newtonian on this reading. That splits it from the law in the field reading.
- A4 window sensitivity: repeat P3 with radius 50, 100, 200 kpc, condensation threshold 0.1, 1, 10, and SPARC coverage of all 171 and of 95 %.

**AMENDMENT A10, owner 11-02: "find complete theory ... high priest of ACDM with all the knobs ... satisfy all the requirements ... do it rigorously, then update zenodo paper". Frozen before these numbers. Rival language, adopts nothing, the law stays the basis being imitated.** R13, one global recipe tuned jointly.
- Knobs, 21 in the fit: R11b's 14; AGN core cutoff log M_cut 11 to 14 (n reduced by 1/(1+(M/M_cut)^2)); lens mass offset +-0.3 dex; two-halo multiplier log +-0.3; satellite fraction 0 to 0.3 with host log M 12.5 to 14 as a centred NFW, which overstates small radii, stated; hydrostatic bias 0 to 0.4; cluster M200 = M_b/f, f 0.08 to 0.16. Plus 5 dark energy and redshift hand terms afterwards, same as J2. Total 26. Bounds are my judgement, set before the fit.
- Fit data: SPARC to the law, weight making the block worth 60 points at 0.02 dex; KiDS whitened; X-COP log M at 0.1, 0.2, 0.3, 0.5, 0.7 R500 at 0.1 dex. Multi-start 3.
- Holdout: tune on odd SPARC, KiDS bins 1 and 3, X-COP alternate systems; grade on the rest. Then tune on all.
- Scoreboard, COMPLETE only if every line passes on the all-data tuning:
 L1 E1, E2, E3. L2 SPARC rms to observed <= 0.205. L3 KiDS chi2 on 60 points, p >= 0.01 at 54 dof (6 lens-side knobs counted). L4 X-COP: |mean log residual| <= 0.05 and rms <= 0.12 dex. L5 E4 and kappa within 5 % at three cosmologies with hand terms. L6 E5 with hand terms. L7 Cassini from A9. L8 holdout: SPARC unseen <= 0.05 dex, KiDS unseen bins p >= 0.01, X-COP unseen rms <= 0.15. L9 plausibility: no more than 3 of 21 knobs at a bound, median log M200 shift within +-0.3 dex.
- Named as not graded, so a COMPLETE here is complete only on these lines: CMB and growth on the recipe, cluster keys, dwarfs, IC 1613, DiskMass, Milky Way, Bullet, wide binaries, and any formation path. Real-time hydro is not run. Passing shows freedom, not evidence.

**A10 BUGS, after the first run, scoreboard unchanged.** The first output stays as `scripts/recipe12_before_fix.out`. (1) X-COP radii in kpc were multiplied by a further 1000, wrecking L4 and distorting the joint fit. (2) A global name clash, A = state(v), overwrote the Einasto index and crashed L6. (3) The M200 hand term moved log M1, not M200, unlike J2; now multiplies M200. Control added: log M500 and untuned NFW mass at R500 printed for one system. Same frozen gates; the bounds are unchanged.

**A10 VERDICT on the fixed run: NOT COMPLETE.** Pass L2, L4, L5, L6, L7. Fail L1 (E1, E2), L3, L8 (KiDS), L9.

**AMENDMENT A11, after A10's verdict, owner's "all the knobs". Frozen before these numbers. Post-result escalation, a different and costlier recipe, which cannot change A10's verdict.** R14: SPARC by R9 at 2 sigma, per galaxy, 1026 parameters, already 0.0152 dex in `recipe3.out`. Lensing on R13's halo knobs held fixed, with per-bin lens mass offset (+-0.3 dex), per-bin two-halo multiplier (log +-0.3), per-bin satellite fraction (0 to 0.3), one host mass, one truncation k R200 (k 0.5 to 3): 14 parameters. Gate: KiDS p >= 0.01 at 46 dof. Holdout: tune on odd radii, grade even radii with their sub-covariance, p >= 0.01. Report knobs at bounds. X-COP and the hand terms carry from R13. No one recipe connects R9's per-galaxy values to the lens side, and that is stated. Also the law's own X-COP mean and rms on the same 35 points, for comparison.
