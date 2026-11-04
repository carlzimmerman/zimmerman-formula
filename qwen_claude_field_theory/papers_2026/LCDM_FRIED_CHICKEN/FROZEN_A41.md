# FROZEN A41: SIDM gravothermal collapse branch; BEC Thomas-Fermi core; mixed CDM + FDM and CDM + WDM

Frozen before any A41 number. Script `scripts/recipe42.py`, output `scripts/recipe42.out`, checkpoint `scripts/recipe42.json`. COVERAGE_MAP.md class (3) rows: SIDM gravothermal collapse (NOT COVERED), BEC repulsive Thomas-Fermi (PARTIAL), mixed DM (PARTIAL). Quarantined experiment: rival language, adopts nothing, never feeds anything outside this folder. Passing shows freedom, not evidence. kappa = 1/2 FITTED; not theory closed.

Known before freezing (from the record, no new number): A19 (`recipe21.out`) C0 constant sigma/m 1, low-density Jeans branch: 0.1200; per-galaxy Ren-style 0.0487 (holdout 0.110); WDM S12 0.1195, WDM + SIDM 0.1162; K1 kappa_eff 0.095 to 0.19, rising 1.9 to 2.1x by z 2.33. A17 FDM soliton 0.149 with m22 alone, fits switch the soliton off. R1 base NFW 0.1419 (`recipe.out` l.5-6). A29 halo scales nearly blind to the DE history.

## Common machinery

SPARC from lib.py (171 galaxies, 3373 points, Y 0.5/0.7), lib.grade (E1 <= 0.02, E2 <= 0.04, E3 <= 0.02, rms to observed vs 0.1951). Halo base as A19: M200 = m200_of(M*, dn), c = Diemer19 x 10^dc, dark mass (1 - f_b) NFW, f_b = min(M_b/M200, 0.5). Spherical baryons from v_bar (A19 mbfun). Holdout: knobs tuned on GS[::2], unseen rms to law on GS[1::2] <= 0.025. Per-galaxy rows: dlog M200 in [-0.6, 0.6], dlog c in [-0.22, 0.22] (2 sigma of 0.3 and 0.11 dex), least_squares 8 evaluations per galaxy; gated holdout as A19: globals chosen on GS[::2], GS[1::2] graded at the prior centre (and with the frozen branch rule where one exists); refits of GS[1::2] reported, not gated. Knobs within 1e-3 of a bound are flagged. Single thread.

## (a) SIDM gravothermal core-collapse branch, both branches

Sources (PROVISIONAL web look-ups 11-04): the isothermal Jeans matching (Kaplinghat et al. 2014; Ren et al. 2019) has a low-density and a high-density solution, differing by orders of magnitude in rho0, which merge at a time t_merge; the high-density branch, usually discarded, has been used (mirrored about t_merge) to approximate the core-collapse stage (attributed to Yang et al. 2024 and to Kaplinghat in search summaries of arXiv 2603.01772 and 2601.17118; text not read). Parametric gravothermal model: Yang et al. 2023 (arXiv 2305.16176, ar5iv HTML read by WebFetch): rho(r) = rho_s / { [(r^4 + r_c^4)^(1/4)/r_s] (1 + r/r_s)^2 }, tau = t/t_c, t_c = (150/C) / [(sigma/m) rho_s r_s] / sqrt(4 pi G rho_s), C = 0.75 (Balberg-Shapiro-Inagaki 2002 lineage), for an NFW start rho_eff = rho_s and r_eff = r_s;
 rho_s/rho_s0 = 2.033 + 0.7381 tau + 7.264 tau^5 - 12.73 tau^7 + 9.915 tau^9 + (1 - 2.033) ln(tau + 0.001)/ln 0.001,
 r_s/r_s0 = 0.7178 - 0.1026 tau + 0.2474 tau^2 - 0.4079 tau^3 + (1 - 0.7178) ln(tau + 0.001)/ln 0.001,
 r_c/r_s0 = 2.555 sqrt(tau) - 3.632 tau + 2.131 tau^2 - 1.415 tau^3 + 0.4683 tau^4,
 valid for tau <= 1; tau > 1 truncated at 1 (the paper's rule). Coefficients as returned by the summariser: PROVISIONAL. The Kaplinghat-Ren-Yu name in the brief is not separately looked up; the parametric model used is Yang et al.'s.

Rows:
- a0 control: A19 low-density solver, constant sigma/m 1, base halo, must give 0.1200 within 0.005 (frozen gate on the code).
- a1 Jeans collapsed branch: A19 solver with the matching root of HIGHEST rho0 among grid points with squared mismatch < 0.05 (rho0 grid 0 to 8 dex above rho_NFW(r1), 40 values, extended from A19's 5 dex so the high root is reachable), then the same damped Newton. Constant sigma/m from {0.5, 1, 3, 10, 30} cm^2/g, picked by all-galaxy rms to law (1 knob). Reported: number of galaxies where the high root differs from the low root by more than 0.5 in ln rho0 (otherwise only one branch exists), unmatched cores, high roots at the grid top.
- a2 per-galaxy branch choice (what rivals do for diversity): at each sigma/m on the grid, each galaxy takes the branch with lower per-galaxy rms to law: 171 binary choices + 1 = 172 parameters. Holdout uses a frozen rule instead: collapsed if log Sigma_b > threshold (Sigma_b = M_b/R_d^2; compact baryons speed collapse, rival language), threshold scanned on GS[::2] with sigma/m (2 knobs), graded on GS[1::2]. The rule row is also graded on all galaxies (2 knobs).
- a3 Ren-style per-galaxy M200, c, with per-galaxy branch: sigma/m in {0.5, 3, 10}; each galaxy fitted on both branches, best kept: 2 x 171 + 171 + 1 = 514 parameters. Gated holdout: sigma/m picked on GS[::2], GS[1::2] at prior centre on the a2 branch rule.
- a4 parametric gravothermal, dark-only profile (baryons added on top, no contraction, and baryons do not speed collapse: stated limit); t = 10 Gyr. a4-1 one knob log sigma/m in [-1, 2.5]; a4-3 plus dn, dc (3 knobs); a4-pg per-galaxy dlog M200, dlog c with global sigma/m from {1, 10, 30, 100} (343): c scatter moves tau, so this is the branch choice of the parametric reading. Reported: tau distribution (fraction tau > 0.5, at the 1 cap).
Scales: K1 Jeans core g_c = sigma0^2/r1 per galaxy (as A19); K1p parametric g_s = 2 pi G rho_s(tau) r_s(tau) (A13 T3 form, equals it at tau 0); K2 a_x = G/(sigma/m) (particle constant).

## (b) BEC with repulsive self-interaction, Thomas-Fermi limit

Equations (FROM MEMORY, standard): n = 1 polytrope P = K rho^2, K = 2 pi a_s hbar^2/m^3; self-gravitating solution rho = rho_c sin(kr)/(kr), k = pi/R, R = pi sqrt(a_s hbar^2/(G m^3)), so K = 2 G R^2/pi; R fixed by the particle, independent of halo mass (Boehmer & Harko 2007; Harko, Robles & Matos type core + NFW envelope; provisional, not looked up). Implemented in the baryon potential: hydrostatic 2K drho/dr = -G (M_b(r) + M(r))/r^2, dM/dr = 4 pi r^2 rho, integrated from the centre for a grid of rho_c (Euler, 300 log radii 1e-4 R to R, A19 style). The core joins the (1 - f_b) NFW at the outer radius r_t where rho = rho_NFW, with M_core(r_t) = M_NFW(r_t) (the core redistributes the NFW mass inside r_t); rho_c solved by a bracketed root on that mass condition. No solution: pure NFW for that galaxy, counted.
- b0 control: no baryons, the integrator must reproduce M(r) of sin(kr)/kr to 1e-3 at r = R/2 and R.
- b1 one global knob log10 R/kpc in [-2, 1.5]. b3 plus dn, dc (3 knobs). b-pg per-galaxy dlog M200, dlog c with global R from b1's value and {0.3, 1, 3} kpc (343).
Scales: K1b g_c = G M_core(r_t)/r_t^2 per galaxy (core acceleration). R is a length: an acceleration needs m too, (hbar/m)^2/R^3; reported as the m22 that would make it 0.5 c sqrt(G rho_DE) (a hand choice).

## (c) Mixed dark matter

- c1 CDM + FDM: fraction f of the dark mass is FDM with m22. FDM part: A17 soliton (Schive 2014: r_c = 1.6 kpc/m22 (M200/1e9)^(-1/3), rho0 = 0.019e9/m22^2/r_c^4 Msun/kpc^3, from A17) with rho0 multiplied by f^2 (stand-in for AxioNyx's "quadratically suppresses soliton growth", Schwabe et al. 2020 abstract, PROVISIONAL; the f^2 mapping is mine), no soliton if f < 0.1 (same abstract), joined to f x (1 - f_b) NFW where the soliton density meets it (A17 'match' rule); CDM part (1 - f)(1 - f_b) NFW. Concentration: c x (1 + 15 M_hm/M200)^(-0.3 f), M_hm = 3.8e10 m22^(-4/3) Msun (FDM half-mode mass, FROM MEMORY), S12 form of A19 with the exponent scaled by f (my stand-in). Knobs f in [0, 1], log m22 in [-1, 2]: 2. c1-4: plus dn, dc (4).
- c2 CDM + WDM: c x (1 + 15 M_hm/M200)^(-0.3 f), f in [0, 1], log M_hm in [6, 12] (2 knobs); m_WDM printed from M_hm via Viel et al. 2005 lambda_hm = 2 pi alpha (2^(nu/5) - 1)^(-1/(2 nu)), alpha = 0.049 (m/keV)^(-1.11) (Omega_W/0.25)^0.11 (h/0.7)^1.22 Mpc/h, nu 1.12, M_hm = (4 pi/3) rho_m (lambda_hm/2)^3 (FROM MEMORY). c2s: plus constant SIDM core (A19 low branch), log sigma/m in [-1, 2] (3 knobs; extends A19 d2). c2-4: c2 plus dn, dc (4).
- Per-galaxy: c1-pg and c2-pg, per-galaxy dlog M200, dlog c at the c1 and c2 globals (343).
- Control: f = 0 must reproduce R1 base 0.1419 within 0.001.
Scales: soliton g_c = G M_s(r_c)/r_c^2 (A17); K4 g200(M_hm) (A19). Particle constants m22, m_WDM, f carry no acceleration.

## Fits

1 knob: bounded scalar minimisation (xatol 0.01) or the frozen grid. 2 to 4 knobs: least_squares, diff_step 0.05, max_nfev 15 (12 where the Jeans solver is inside), one start from the best lower-knob fit, then the base. Pre-run budget change is allowed only before any graded number and must be disclosed.

## Gates

- Shape: E1, E2, E3 on all-data tuning; holdout <= 0.025. EXACT only if all four pass.
- Tie gates on each family's best global row: G1 median kappa_eff (scale/(c sqrt(G rho_DE0))) within 0.05 dex of 0.5; G4 rms log scale over SPARC hosts log M200 11 to 12.5 <= 0.1; G3 a(z)/a(0) at the median SPARC M200, dark-only halo, Diemer19 c(M, z), 200c of rho_crit(z), t = min(10 Gyr, age(z)), in the bands [0.76,1.03], [0.71,1.12], [0.33,1.21]; GT |log10 a(z)/a(0) - 0.5 log10 rho_DE(z)/rho_DE0| <= 0.05 at z 1, 1.5, 2.33 in A29's backgrounds B0 to B5, footing P (recipe31's background code exec'd, not edited), with c, rho_crit and age of that background; G2z in each background where measurable (A29 rule), G2x pooled over B1, B1p, B1u, B2, B3, B4 (18 points), G2t over rho_DE0 x f, f in {0.5, 0.71, 1, 1.41, 2}, in B1's w0, wa on A29's physical footing; each 0.5 +- 0.05. G5 halo routes pass by definition (halo gravity at measured radii); particle constants exert no force: G5 FAIL (not operative).
- Particle constants (G/(sigma/m), R, m22, m_WDM, f): no rho_DE enters, so G2 = 0 exactly; computed across the same cosmologies to verify, and GT dev = -0.5 log10 rho ratio. A coupling to rho_DE is not added.

## Expected in advance

(a) a1 collapsed branch moves away from the law: denser inner halos where base halos already overshoot at low g_b: E1 0.13 to 0.2. a2 per-galaxy branch choice gains little over a0 (0.10 to 0.12), because most galaxies prefer the cored branch; the rule row about the same; a3 0.04 to 0.05, holdout about 0.11 (as A19 c). a4 best at low sigma/m or capped tau: 0.11 to 0.14 with one knob, 0.07 to 0.09 with three; per-galaxy 0.04 to 0.06. (b) b1 0.11 to 0.14, b3 0.07 to 0.09, per-galaxy 0.04 to 0.06; core acceleration spreads over hosts (> 0.1 dex) and rises with z. (c) mixed rows no better than their pure limits plus knobs: c1 0.14, c2 0.115 to 0.12, c2s about 0.116, 4-knob rows 0.08 to 0.09. No row EXACT. All halo scales: G1 fail or pass by tuning, G3 fail (rise 1.5 to 3x by z 2.33), GT fail in every background, G2x near 0. Particle constants: G2 = 0, G3 and G4 trivially pass, GT fails in B1, B1p, B1u, B3 and passes in B2, B4, B5, G5 fails.

Rival language; adopts nothing. kappa = 1/2 FITTED; not theory closed.

## RESULTS (written after the run; criteria above unchanged)

One run, 1270 s, peak RSS 136 MB, single thread, no crash, no bug found, no wrong output to keep. Line numbers refer to `scripts/recipe42.out`. Controls: a0 PASS, 0.1217 against A19's 0.1200 (l.17); its worst bin is 0.0847 against A19's 0.0687 (the +0.085 bin at log g_b -9.0, l.15): the 8-dex rho0 grid changes which near-root starts the Newton solve in a few massive galaxies; disclosed, within the frozen tolerance. b0 PASS, 8.8e-5 and 3.0e-4 (l.94). Mixed f = 0 PASS, 0.1419 (l.125).

| row | knobs | E1 | E2 | E3 | obs | holdout | line |
|---|---|---|---|---|---|---|---|
| a1 collapsed branch, sigma/m 0.5 | 1 | 0.1790 | 0.2974 | 0.2566 | 0.2597 | 0.1546 | 21-26 |
| a2 per-galaxy branch, sigma/m 1 | 172 | 0.1201 | 0.2101 | 0.0853 | 0.2135 | n/a | 36-37 |
| a2 branch rule (Sigma_b threshold) | 2 | 0.1207 | 0.2101 | 0.0842 | 0.2128 | 0.1070 | 42-46 |
| a3 per-galaxy M200, c, branch, sigma/m 0.5 | 514 | 0.0472 | 0.0988 | 0.0240 | 0.1966 | 0.1096 gated | 54-61 |
| a4-1 parametric, sigma/m 1.93 | 1 | 0.1193 | 0.2070 | 0.0821 | 0.2099 | 0.1171 | 66-72 |
| a4-3 parametric + dn, dc | 3 | 0.0863 | 0.1731 | 0.0522 | 0.2091 | 0.0896 | 74-80 |
| a4-pg per-galaxy, sigma/m 100 | 343 | 0.0564 | 0.1015 | 0.0399 | 0.1955 | 0.1129 gated | 86-91 |
| b1 BEC, R 3.53 kpc | 1 | 0.1289 | 0.2688 | 0.0848 | 0.2198 | 0.1211 | 99-104 |
| b3 BEC + dn, dc, R 1.87 kpc | 3 | 0.0885 | 0.1796 | 0.0415 | 0.2123 | 0.0921 | 106-111 |
| b-pg per-galaxy, R 1 kpc | 343 | 0.0401 | 0.0990 | 0.0259 | 0.1995 | 0.1244 gated | 117-122 |
| c1 CDM + FDM, f 0.205, m22 0.1 | 2 | 0.1174 | 0.2359 | 0.0468 | 0.2219 | 0.1087 | 130-135 |
| c1-4 + dn, dc | 4 | 0.0909 | 0.1819 | 0.0355 | 0.2173 | 0.0924 | 137-141 |
| c2 CDM + WDM, f 0.212, log M_hm 12 | 2 | 0.1157 | 0.2228 | 0.0388 | 0.2201 | 0.1062 | 145-149 |
| c2-4 + dn, dc | 4 | 0.0897 | 0.1837 | 0.0316 | 0.2155 | 0.0910 | 151-155 |
| c2s CDM + WDM + SIDM 0.511 | 3 | 0.1134 | 0.1970 | 0.0369 | 0.2109 | 0.1028 | 157-161 |
| c1-pg / c2-pg per-galaxy | 343 | 0.0406 / 0.0402 | 0.103 / 0.102 | 0.028 | 0.1995 / 0.1992 | 0.109 / 0.106 (the c1, c2 rows) | 164-172 |

Verdict on shape: NOT EXACT, no row (l.281-297). Best global: a4-3 0.0863 (3 knobs); best overall b-pg 0.0401 with 343 parameters, which fails E2 (0.099) and its gated holdout (0.124).

(a) SIDM collapse. The high-density root exists and differs from the low one in 89 to 157 of 171 galaxies (l.5-9), 12 to 15 in ln above rho_NFW(r1); none at the grid top. The collapsed branch moves away from the law at every sigma/m (0.179 to 0.354, l.27), worst at high g_b (+0.26 dex bin, l.23), as expected. Per-galaxy branch choice buys 0.0016 dex over the cored control (0.1201 vs 0.1217), collapsed chosen in 48 of 171 (l.31); the frozen Sigma_b rule picks 3 galaxies (l.47), so a rule that a holdout can use does not reproduce the per-galaxy choice. Ren-style per-galaxy halos with free branch reach 0.0472 (80 collapsed), barely below A19 (c) 0.0487 at 171 more parameters; 64 of 342 at bound (l.58). Parametric (Yang et al. 2023): the global fit keeps tau small (median 0.024, l.70; 0.001 at 3 knobs, l.78), i.e. the fit stays on the cored side; above sigma/m about 50 the scan blows up to 0.29 (l.64). Per-galaxy halos let tau reach 0.81 median at sigma/m 100 (l.90) with the same rms as sigma/m 1 (0.0564 vs 0.0567, l.81-84): collapse and coring trade off per galaxy, as rivals use for diversity, but neither branch lands on the law.

(b) BEC. The fixed-R core helps little (scan flat at R below 0.3 kpc, minimum 0.130 near 3 kpc, l.97). In 83 of 171 galaxies at the b1 R there is no core solution and the galaxy stays pure NFW (l.99; 99 of 171 at b3). Post-result diagnostic, `scripts/recipe42b.py`, `recipe42b.out`, not a grade: in 82 of those the fixed-R core is heavier than the NFW mass inside every density crossing, so the frozen mass-redistribution rule cannot be met; they are the heavier galaxies (median log M_b 10.00 vs 9.57). So b1 and b3 grade the BEC route only where the rule admits a core; a different joining rule (core mass free) would be a new knob per galaxy, which b-pg already approximates (0.0401).

(c) Mixed DM. c1 sits at the m22 lower bound (0.1, Lyman-alpha excluded by the record's from-memory bound) with f 0.205 and solitons in 34 of 171 (l.130); c2 sits at the M_hm bound (log 12, thermal m_WDM 0.305 keV, from memory) with f 0.21 (l.145). Both gain 0.003 to 0.004 dex over A19's pure WDM (0.1195) only by using the fraction to soften the bound-hugging suppression. The 4-knob rows land 0.090, the same floor as A19 (b) and A17 M4: the gain is the SHMR and c knobs (dn at +0.24 to +0.26).

Tie gates (no family ties a to rho_DE):
- Per-galaxy G1, G4 at fitted knobs: kappa_eff Jeans K1 0.096 to 0.133 (l.25, 40, 59), parametric K1p 0.385 (l.71) and 0.245 (l.79), BEC K1b 0.217 and 0.177 (l.103, 110), mixed soliton 0.320 over 34 galaxies (l.134): all FAIL G1. G4 passes for K1p (0.078, 0.073), b3 (0.081 over 27 hosts) and c1 (0.056 over 7 hosts), fails elsewhere.
- Dark-only at median log M200 11.14, eight A29 backgrounds, footing P (l.177-255): every halo scale rises with z: Jeans 2.0x by z 2.33, parametric 1.43x, BEC 1.54x, soliton 4.5x, g200(M_hm) 5.3x: G3 FAIL in every background. GT FAIL for every halo scale in every background; closest: parametric in B3 (-0.011, +0.003, +0.050, l.230; the z 2.33 deviation is at the tolerance and rounds to 0.050, read as FAIL by the script) and BEC in B3 (+0.007, +0.026, +0.071, l.231). As A29's U1 in B3: B3's rising rho_DE happens to match the halo's own H-driven rise; the same scales miss by +0.24 to +0.29 in B1u (l.210-211) and have G2x +0.038 and +0.010 (l.260-261). Not tracking.
- G2z: -3.9 to +9.1 across backgrounds, never 0.5. G2x pooled: -0.15 to +0.04 (l.258-265), FAIL all. G2t: Jeans +0.04, parametric +0.14, BEC +0.13, soliton +0.20 FAIL; g200(M_hm) +0.453 PASS (l.273), because g200 at fixed M_hm goes as rho_crit^(2/3) and rho_crit rises with rho_DE0 on this footing ((2/3) x 0.685 near f 1); it fails G1 (0.017), G3, GT and G2x (-0.15), so the one G2t pass is the Hubble-rate dependence of a halo mean density, not a tie.
- Particle constants (G/(sigma/m) at a1 and a4, l.184-185 onward): no rho_DE enters; G2z, G2x, G2t exactly 0 (l.264-265, 274-275; identical values in all five G2t cosmologies), G2 FAIL, verified. G3 and G4 PASS trivially. GT FAILS in B1 (+0.088 at z 2.33), B1p (+0.076), B1u (+0.096), B3 (-0.154), passes in B0, B2 (-0.046), B4, B5, as expected. kappa_eff 7.13 and 1.85 (G1 FAIL); G5 FAIL (a cross-section exerts no force). BEC: R is a length; (hbar/m)^2/R^3 equals 0.5 c sqrt(G rho_DE) at the b1 R only for m22 0.054, a hand choice (l.278).

Expected outcomes held, with these differences: a3 0.047 at the low edge of the expected 0.04 to 0.05; BEC no-core in about half the sample (not foreseen); c1 and c2 at a bound; the G2t pass of g200(M_hm) (not foreseen, explained above).

Deviations: none from the frozen procedure. Disclosed: the a0 control's worst-bin shift; the BEC no-root fallback (82 + 1 galaxies) and the post-result diagnostic; the a2 per-galaxy row has no holdout by construction (the rule row is its holdout); knobs at bound: c1 log m22 lower, c2 and c2s log M_hm upper; a3 64 and b-pg 91, a4-pg 35, c-pg 89 and 92 per-galaxy at bound.

Provisional: the parametric model's coefficients and t_c (summariser reading of the ar5iv HTML of arXiv 2305.16176); the high-density-branch reading of collapse (search summaries of arXiv 2603.01772 and 2601.17118, texts not read); the AxioNyx soliton suppression and 10 % threshold (arXiv 2007.08256 abstract), with my f^2 mapping; the FDM half-mode mass 3.8e10 m22^(-4/3), the WDM S12 coefficients and the Viel 2005 thermal-relic mapping, all from memory; the Thomas-Fermi equations from memory. A29's DESI CPL values remain from memory. No downloads.

Rival language; adopts nothing. kappa = 1/2 FITTED; not theory closed.
