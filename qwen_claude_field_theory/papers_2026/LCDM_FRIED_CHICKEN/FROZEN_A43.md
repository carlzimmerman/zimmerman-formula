# FROZEN A43: baryon-tracing dark mass (scaled HI / cold dark gas) and dark matter-baryon scattering halos

Frozen before any A43 number. Script `scripts/recipe44.py`, output `scripts/recipe44.out`, checkpoint `scripts/recipe44.json` if needed. Quarantined experiment: rival language, adopts nothing, never feeds anything outside this folder. Passing shows freedom, not evidence; failing does not rule either model out. kappa = 1/2 FITTED; not theory closed.

Known before freezing: the record (A7 M3: one dark-baryon exchange in 13 Gyr needs sigma/m 0.63 cm^2/g at g_b = a0 and about 40 at the last point; A38 Foot and FKP rows: best global 0.0702 and 0.1550, no tie; A29 backgrounds in `recipe31.py`; COVERAGE_MAP class (1) row "baryon-tracing dark mass" and class (3) row "DM-baryon scattering", PARTIAL A7 M3). Web look-ups on 11-04 listed below. No A43 number computed or seen.

## Sources (PROVISIONAL web look-ups through a summariser; FROM MEMORY where marked)

- Hoekstra, van Albada & Sancisi 2001, MNRAS 323, 453 (arXiv astro-ph/0010569, abstract page): dark matter surface density modelled as a scaled copy of the HI surface density; "scaling factors cluster around 7, after correction for primordial helium", some galaxies larger. Whether M/L was free is not in the abstract (FROM MEMORY: stellar M/L was fitted). Read here as V_dark^2 = eta V_gas^2 with SPARC's V_gas (which already includes 1.33 for helium), published eta = 7.
- Pfenniger & Combes 1994 (FROM MEMORY): the dark mass is cold H2 in a fractal clumpy disc near the CMB temperature, distributed like the HI. No equation used beyond the HI-scaling form.
- CMB limits on DM-proton momentum-transfer cross section sigma = sigma0 v^n (v in units of c, FROM MEMORY), 95 %: Gluscevic & Boddy 2018 (arXiv 1712.07133, abstract): n = 0, 3.0e-26 cm^2 at 1 MeV, 1.7e-25 at 1 GeV, 1.6e-23 at 1 TeV. Boddy et al. 2018 (arXiv 1808.00001, via search summary): n = -2, 2.3e-33 cm^2; n = -4, 1.7e-41 cm^2, for m_chi below about 10 MeV; Planck limits vanish if <~ 0.4 % of DM is tightly coupled. Milky Way satellites (Nadler et al. 2019/2021, via search summary): n = 0, 8.8e-29 cm^2 at 100 MeV; Maamari et al. (via search summary): n = 2, 1.4e-23 cm^2 at 10 MeV. Heavy-mass n = -4, -2 limits: FROM MEMORY, for m_chi >> m_p the rate depends on sigma0/m_chi, so the limit on sigma0/m_chi is taken mass-independent and matched at m_chi = m_p (an estimate, flagged). Heavy n = 2: not retrieved; graded by the n = 0 mass scaling as an estimate (flagged). Direct detection at sigma above about 1e-28 cm^2 for GeV-TeV DM (overburden ceiling, XQC-type rocket limits): FROM MEMORY, quoted, not graded numerically.
- Solar neighbourhood (FROM MEMORY, McKee, Parravano & Hollenbach 2015 and Kuijken-Gilmore-type K_z): local gas surface density (HI + H2 + He) about 13.7 Msun/pc^2; dynamical surface density within |z| < 1.1 kpc about 70 Msun/pc^2 of which stars plus gas about 50; room for extra disc-like dark mass about 20 Msun/pc^2.
- Cosmic HI density Omega_HI(z) ~ (1 + z)^0.57 (Crighton et al. 2015, FROM MEMORY).

## (a) Baryon-tracing dark mass, as implemented

SPARC from lib.load() (171 galaxies, Y 0.5/0.7); V_gas, V_disk, V_bul re-read from the same rotmod files with lib's mask; g_gas = V_gas|V_gas|/r, g_star = g_b - g_gas. Total g = g_b + eta g_gas + eps g_star (dark mass tracing the gas, and optionally the stars). Where a central HI hole makes the total negative, it is floored at 1e-3 g_b (count reported).
- H0 published: eta = 7, eps = 0 (0 fitted knobs).
- H1 one global eta (1 knob, bounds 0 to 50).
- H2 global eta and eps (2 knobs, eps 0 to 10).
- H3 per-galaxy eta (171). H4 per-galaxy eta and eps (342).
- Implied acceleration scale: (i) pooled lib.fit_a on the model curve; (ii) per galaxy a_i = lib.fit_a per galaxy, G4 spread over hosts log M200 11 to 12.5 (lib SHMR); (iii) native dark-gas scale a_dg,i = 2 pi G (1 + eta) Sigma_gas,i with Sigma_gas,i = 1.33 M_HI/(pi R_HI^2) from the SPARC table (mean gas surface density inside the 1 Msun/pc^2 HI radius), median and spread; (iv) the outer BTFR scale a_out,i = V_model(r_last)^4/(G M_b).
- Local check C_loc (Milky Way solar circle, FROM MEMORY numbers): extra disc-tracing dark surface density eta x 13.7 Msun/pc^2 must be <= 20 Msun/pc^2, i.e. eta <= 1.46. Graded for H0, H1, H2 and the H3 median.

## (b) DM-baryon scattering halos, as implemented

Base halo, 0 knobs: lib SHMR M200, Diemer19 c, (1 - f_b) NFW, no contraction (A1's R1 base). Gas density felt by DM on an isotropic orbit = spherical average of the gas: M_gas(r) = running max of V_gas^2 r/G, rho_g = dM_gas/dr/(4 pi r^2) (log interpolation; constant inside the first point; zero beyond the last measured radius, stated). Grid: 200 log-spaced radii from 0.05 r_first to r_last.
- Cross section sigma(v) = sigma_ref (v/100 km/s)^n, n in {-4, -2, 0, +2}; knob s = log10(sigma_ref/m_chi in cm^2/g), bounds -8 to +10.
- Energy and momentum relaxation rate per DM particle (standard heat-exchange form, FROM MEMORY): Gamma = 2 rho_g (sigma/m_chi) v_rel m_chi^2/(m_chi + m_p)^2. Relative speed v_rel = sqrt(V_c0^2 + 3 sigma_chi^2 + 3 sigma_g^2), V_c0^2 = g_b r + G M_NFW/r (bulk rotation of the gas through a non-rotating halo plus dispersions), sigma_chi = V_c0/sqrt 2, sigma_g = 8 km/s (thermal WNM, 8000 K).
- Coupled fraction f(r) = 1 - exp(-Gamma t), t = 10 Gyr.
- Heavy branch (m_chi = 100 GeV): coupled DM reaches the gas temperature, sigma_chi -> sigma_g sqrt(m_p/m_chi) (0.8 km/s), and is dragged to corotation, so it settles into the gas's distribution. Equilibrium: coupled mass M_c = Int f dM_NFW redistributed with the gas profile, g_dark = G M_unc(<r)/r^2 + (M_c/M_gas) g_gas, M_unc(<r) = Int_0^r (1 - f) dM_NFW. Angular momentum for corotation is taken from nowhere (in the rival's favour, stated); contraction of the uncoupled DM ignored.
- Light branch (m_chi = 10 MeV, the millicharged mass range): coupled DM reaches sigma_eq = sigma_g sqrt(m_p/m_chi) = 77 km/s (heated core where the halo is colder, cooled where hotter). Inside r1 (outermost radius with Gamma t >= 1) the DM is isothermal at sigma_eq in the baryon plus self potential (lib.thermal integrator logic), central density solved so M(r1) = M_NFW(r1); NFW outside r1. No r1 inside the first point: NFW unchanged.
- Rows, per branch and n (8 rows): 1 knob s, tuned on all (bounded scalar minimisation of the log residual to the law), holdout tuned on GS[::2], graded on GS[1::2]. Best row by E1 then gets X2 (s plus a global log c offset dc in [-0.5, 0.5], 2 knobs) and X3 per-galaxy s (171, freedom only: a cross section is universal).
- Bounds check per row: the fitted sigma_ref/m_chi converted to sigma0 = sigma_ref (c/100 km/s)^n m_chi (v in units of c) against the limits above; ALLOWED only if below every quoted limit at that mass. Also the coupled fraction of DM inside r_last against the 0.4 % subcomponent loophole (the loophole helps only if the needed coupled DM is <= 0.4 % of the DM). A7 M3's 0.63 and 40 cm^2/g printed beside.

## Gates (LANE_BRIEF_COMMON.md, fixed)

- E1 <= 0.02, E2 <= 0.04, E3 <= 0.02 (lib.grade bins), holdout <= 0.025 for every globally tuned row; rms to observed beside; knobs at bounds reported.
- G1 kappa_eff = a/(c sqrt(G rho_DE0)) within 0.05 dex of 0.5, with pooled a_fit, and for (a) the native a_dg median. Tuned rows pass by being tuned to the law, stated.
- G2 slope 0.5 +- 0.05: read from the equations (list every constant the scale depends on; native slope 0 if rho_DE appears nowhere), and G2x pooled over A29 evolving backgrounds for each z reading.
- G3 a(z)/a(0) bands at z 1, 1.5, 2.33. G4 rms of per-galaxy log a_i over hosts <= 0.1 dex. G5 operative at 1 to 30 kpc: dark-mass gravity at measured radii, pass by definition (stated).
- GT in A29 backgrounds B0 to B5: |log10[a(z)/a(0)] - 0.5 log10[rho_DE(z)/rho_DE0]| <= 0.05 at z 1, 1.5, 2.33.
- z readings, fixed now. (a) r1 eta, Sigma constant: flat. (a) r2 gas surface density follows Omega_HI(z): a(z)/a(0) = (1 + z)^0.57 (native a_dg proportional to Sigma). (b) r1 equilibrated today, cross-section microphysics constant: flat. (b) r2 coupling time is the background's cosmic age at z: the best (b) row re-run with t = 10 Gyr x age(z)/age(0) at fixed baryons and halo, a(z) = pooled fit_a; ages from colossus per background.
- Cassini: neither family has a term at AU scales (no gas there); not graded, stated, not a pass.

## Expected in advance

(a) H1 one global eta reaches about 0.05 to 0.09 (good outer shape in gas-rich dwarfs, too little dark mass in the inner parts of HSB discs and too much decline where the HI fades); H2 about 0.04 to 0.06; per galaxy H3/H4 about 0.02 to 0.04, maybe E1 passes with 342. Fitted eta 5 to 12; C_loc fails for any eta near the published 7. Native a_dg spreads several tenths of a dex. No rho_DE: slope 0, GT flat reading passes only in near-Lambda backgrounds. (b) Heavy branch at large s collapses into the (a) eta form with a coupling-limited inner shape, E1 about 0.06 to 0.12; light branch makes cores, E1 0.1 or worse. Needed sigma/m of order 1 to 100 cm^2/g at 100 km/s, excluded by the CMB and satellite limits by orders of magnitude for every n; subcomponent loophole cannot supply galaxy-scale dark mass. No tie.

Rival language; adopts nothing. kappa = 1/2 FITTED; not theory closed.

## RESULTS (written after the run; criteria above unchanged)

Runtime 39 s first pass (5 s rerun from checkpoint), peak RSS 103 MB, single thread. Line numbers refer to `scripts/recipe44.out`; 44b = `scripts/recipe44b.out` (post-result diagnostic, disclosed). One label bug fixed after the first run: X2 printed "at bound False" checking only the c offset, while s sat at its lower bound -8; the wrong output is kept as `scripts/recipe44_before_fix.out`; numbers unchanged (diff is that label and timings).

(a) Baryon-tracing dark mass. NOT EXACT at any parameter count tried.
- H0 published eta = 7, 0 knobs (l.6-9): E1 0.4066, E2 0.8360, E3 0.4215, observed 0.4471; 26 points floored where V_gas^2 < 0 makes the total negative. H1 one global eta (l.10-14): eta 7.14 (the published value, not at a bound), E1 0.4066, holdout 0.3772. H2 eta + eps (l.15-19): eta 4.90, eps 1.04, E1 0.2084, holdout 0.2427. H3 per-galaxy eta (171) (l.20-22): 0.3016, eta median 9.56. H4 per-galaxy eta + eps (342) (l.23-25): E1 0.0423, E2 0.0759, E3 0.0461, observed 0.2010, eta median 5.2, eps median 1.29, 6 knobs at bound.
- Post-result (44b), because the floor costs about -3 dex per floored point: E1 with floored points excluded 0.2271 (H1), 0.1808 (H2); rival-favourable clipped form eta max(g_gas, 0): C1 1 knob 0.2168 (eta 9.08, holdout 0.2048), C2 2 knobs 0.1570 (holdout 0.1406), C3 per-galaxy 0.1916, C4 342 params 0.0420. The verdict does not depend on the floor.
- Why (checked on NGC 2403, NGC 3198, UGC 2885, NGC 7814, scratch): inside 2 to 4 disc lengths of HSB discs g_gas/g_b is 0.00 to 0.05 while the law needs +0.5 to +1 g_b, so a gas tracer cannot supply inner dark mass at fixed Y 0.5/0.7; a stellar-tracing term (eps, the free M/L Hoekstra et al. had) is needed, and even per galaxy it stalls at 0.042.
- Implied scales: pooled a_fit 0.31 A0 (H1), 0.71 A0 (H2), 0.99 A0 (H4, tuned per galaxy) (l.10, 15, 23). Native a_dg = 2 pi G (1+eta) Sigma_gas: median 0.38 A0 (kappa_eff 0.19), spread 0.142 dex (l.12). Outer BTFR scale V_last^4/(G M_b) median 1.29 A0, spread 0.34 dex (l.12). G4 0.383 (H1), 0.358 (H2) FAIL; H4 0.011 passes by inheriting the law it was fitted to.
- C_loc FAILS every row: eta x 13.7 = 96 to 98 Msun/pc^2 (H0, H1), 67 (H2) against about 20 of room at the Sun (from memory); only 1.2 % (H3) and 2.9 % (H4) of SPARC galaxies have eta <= 1.46.

(b) DM-baryon scattering halos. NOT EXACT; the scattering knob barely helps, and every helpful setting is excluded.
- N0 base halo, 0 knobs (l.29): E1 0.1420.
- Heavy (100 GeV, dark disc) one knob each (l.30-45): n -4 0.1373, n -2 0.1347, n 0 0.1299 (best), n +2 0.1380; holdouts 0.1349, 0.1296, 0.1265, 0.1278; G4 0.138 to 0.163 FAIL. Best n 0: sigma/m 2.04 cm^2/g at 100 km/s, 39 % of the DM inside r_last coupled, eta_eff = M_c/M_gas median 3.99 (C_loc 1.46 met by 7.6 % of galaxies).
- Light (10 MeV, heated core) (l.46-61): n -4 0.1340, n -2 0.1352 (needing 973 and 5.5e3 cm^2/g); n 0 and +2 the fit turns the coupling off (s -7.5, E1 0.1419 = base).
- X2 heavy n 0 + c offset (l.63-64): E1 0.0991, holdout 0.0971, but s goes to its lower bound -8: the gain is the c offset -0.20 alone, scattering off. X3 per-galaxy s (171) (l.65-66): 0.1131, s spread 3.3 dex, 24 at bound.
- Bounds (l.33, 37, 41, 45, 49, 53): needed/limit heavy n -4 51 (estimate), n -2 30 (estimate), n 0 104 (CMB, interpolated), n +2 1.5e3 (estimate); light n -4 1.3e4, n -2 4.7e3: all EXCLUDED. Light n 0, +2 are "ALLOWED" only at zero effect. The 0.4 % subcomponent loophole: heavy n -4 couples a median 0.4 % of the DM inside r_last but gains only 0.005 dex on base; a 0.4 % species cannot carry galaxy dark mass. Direct detection (from memory) closes much of the heavy window further; not graded. A7 M3's 0.63 to 40 cm^2/g sits in the same excluded range.

(c) Tie. NO TIE in either family.
- G1 (l.101-110): H1 0.159, H2 0.353, native a_dg 0.189 to 0.192, N0 0.842, heavy n 0 0.633, X2 0.400, X3 0.646: all FAIL; H4 0.493 passes only by per-galaxy tuning to the law.
- G2: rho_DE appears in no equation of either family (eta, Sigma_gas; sigma/m, m_chi, t, T_gas, rho_gas, SHMR halo): native slope 0, FAIL. G2x: flat 0.000 (l.79), Omega_HI reading -0.068 (l.89), age reading -0.016 (l.99): all FAIL.
- G3: flat passes; Omega_HI reading 1.49, 1.69, 1.99 FAIL; age reading 1.12, 1.16, 1.20 FAIL (just above 1.03 and 1.12).
- GT: flat passes in B0, B2, B4, B5, fails B1, B1p, B1u (+0.076 to +0.096 at z 2.33) and B3 (-0.154) (l.70-78); Omega_HI reading fails everywhere (+0.10 to +0.39); age reading passes only B2, fails the rest (l.91-98).
- G4 fails for every global row (0.36 to 0.38 (a), 0.11 to 0.16 (b)). G5: dark-mass gravity, pass by definition. Cassini: not graded.

Verdict: scaled-HI dark mass is not a strong curve-fitter on SPARC at fixed stellar M/L (best global 0.157 with 2 knobs, clipped; 0.042 with 342), it breaks the solar-neighbourhood disc budget by 3 to 5x at the fitted eta, and its implied scale spreads 0.14 to 0.38 dex. DM-baryon scattering, as an equilibrium halo, moves the base NFW grade by at most 0.012 dex, at cross sections 30 to 1e4 times above quoted limits. Neither carries rho_DE. Expected outcomes partly wrong: (a) did much worse than the expected 0.05 to 0.09 (gas carries no inner mass at fixed Y), and per-galaxy eta alone did not reach 0.04.

Deviations: label bug in X2 (kept as before_fix); post-result 44b rows (floor exclusion, clipped form) and a scratch inspection of four galaxies; per-galaxy and X2 fits use a coarse grid plus bounded refine. Angular momentum for the heavy dark disc ignored (rival-favourable).

Provisional: Hoekstra et al.'s eta = 7 from the abstract; every cross-section limit through search summaries, heavy n -4, -2, +2 limits are my scalings (flagged ESTIMATE); the heat-exchange rate form, solar-neighbourhood budget and Omega_HI(z) are from memory.

Rival language; adopts nothing. kappa = 1/2 FITTED; not theory closed.
