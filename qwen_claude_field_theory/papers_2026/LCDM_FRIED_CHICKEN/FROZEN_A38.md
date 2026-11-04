# FROZEN A38: dark matter whose distribution is tied to the baryons (dissipative/mirror DM; Famaey-Khoury-Penco DM-baryon interactions)

Frozen before any A38 number. Script `scripts/recipe39.py`, output `scripts/recipe39.out`, checkpoint `scripts/recipe39.json`. Quarantined experiment: rival language, adopts nothing, never feeds anything outside this folder. Passing shows freedom, not evidence; failing does not rule either model out. kappa = 1/2 FITTED; not theory closed.

Known before freezing: only the sources below (web look-ups, PROVISIONAL, read through a summariser) and the record (A7 M3: one dark-baryon exchange in 13 Gyr needs sigma/m 0.63 cm^2/g at g_b = a0; A15 U3 spherical-baryon method; A29 backgrounds in `recipe31.py`). No A38 number computed or seen. One disclosure: a WebFetch of the arXiv PDF of 1712.01316 was auto-saved by the tool to the session's tool-results folder (2.1 MB); it was not opened or used; equations below come from the ar5iv HTML.

## Sources and equations as implemented (all PROVISIONAL)

**(a) Dissipative / mirror DM (Foot and collaborators).**
- Foot 2013, arXiv 1307.1755, Eq. 16/18 (summariser): quasi-isothermal rho = rho0 r0^2/(r^2 + r0^2), r0 ~= 1.4 (r_D/kpc) kpc, rho0 r0 ~= 50 Msun/pc^2 x [xi_Fe'/0.02]^0.8 [L'_SN^MW/1e45 erg/s]^0.8 [2/c1]; reference values give 50 Msun/pc^2; rho0 r0 "roughly constant". Free in the paper: beta, r0, rho0 per galaxy fitted, with these as the derived scaling.
- Chashchina, Foot & Silagadze 2017, arXiv 1611.02422 (PRD 95 023009), Eq. 11: rho(r, theta) = (lambda R_SN / 4 pi r_D^2) Int_0^inf t exp(-r t / r_D) dt / sqrt(1 + t^4 + 2 t^2 cos 2 theta), the dark density as the line-of-sight sum over an exponential supernova disc; r >> r_D gives rho = lambda R_SN/(4 pi r^2), so v_asym^2 = G lambda R_SN. The BTFR requires lambda R_SN proportional to sqrt(m_bar); the constant is fixed in the paper "by normalising to the RAR at large radii", with a0 = 1.20e-10 taken from MOND, "not predicted". Paper claims RAR agreement within 0.12 dex errors on illustrative discs; no SPARC per-galaxy fit. Rotation curve said similar to quasi-isothermal with r0 ~ 1.4 r_D.
- Foot & Vagnozzi 2016 (arXiv 1602.02467) carries no explicit scaling relation in the summariser's read; not used for equations.

As implemented (spherical, dark gravity G M_DM(<r)/r^2 added to SPARC g_b; disc-plane geometry of Eq. 10 not computed, stated):
- F0 published 2013 scaling, 0 knobs: quasi-isothermal, r0 = 1.4 R_d (SPARC R_d), rho0 r0 = 50 Msun/pc^2.
- F1: F0 with Sigma_h = rho0 r0 global free (1 knob).
- F1b: F1 plus the r0 coefficient k global free (2 knobs).
- F2 published 2017 recipe: Eq. 11 averaged over cos theta (spherical average, stated), lambda R_SN = K sqrt(M_b/1e10 Msun), r_D = R_d; K global (1 knob, the paper's RAR normalisation, here tuned to the law).
- F3: F2 with lambda R_SN = K (M_b/1e10)^p and r_D = k R_d (3 knobs).
- F4 per galaxy: lambda R_SN free per galaxy (171), k global from F3. F5: lambda R_SN and k free per galaxy (342).
- Control C_F, frozen: the best quasi-isothermal r0/r_D fit to the spherically averaged Eq. 11 curve over x = r/r_D in 0.3 to 10 is reported against the paper's 1.4; within 1.0 to 2.0 counts as consistent (the paper's figure is in-plane, mine spherical).
- Native acceleration scale: F2 gives v^4 -> G^2 K^2 M_b/1e10, so a_F = G K^2 / 1e10 Msun, a constant set by the normalisation K. F0/F1 give a_i = (4 pi G Sigma_h r0)^2/(G M_b) per galaxy.

**(b) Famaey, Khoury & Penco 2018, arXiv 1712.01316 (JCAP 1803 038), ar5iv HTML.**
- Eq. 4.1: sigma_int = C a0 m_b/(n epsilon), i.e. n sigma epsilon / m_b ~ a0 (the master relation, sigma times energy exchange proportional to 1/n_DM). a0 enters as the interaction strength; the paper uses a0 ~= cH0/6 only for estimates and does not derive it.
- Eq. 3.4 hydrostatic grad(rho v^2) = rho g; Eq. 3.5-3.6 heat flux q = -kappa grad T, kappa = (3/2) n l^2/t_relax; Knudsen form kappa ~ n r v (Eq. 5.3).
- Eq. 6.1-6.5 (spherical exponential baryons rho_b = M_b e^(-r/L)/(8 pi L^3)), dimensionless: v^2 hat = v^2/s, q hat = 4 pi G rho r^2 / s, M hat = eps M/M_b, s = sqrt(C a0 G M_b), eps = sqrt(G M_b/(C a0 L^2)); (x^2/q)(d/dx)(q v^2/x^2) = -(M + eps M_b)/x^2; d/dx(q v^2 x dv/dx) = (v/4) x^2 e^(-x); dM/dx = q.
- Boundary: regular origin, q ~ (R/2) x^2, two parameters R and v hat_0^2 per galaxy (Eq. 6.6-6.7). Paper fixes C = 1/16 and sets R, v0 per galaxy by normalising V at 10 L and requiring flatness; Table 2: R 5.9, 5.7, 5.5 and v0^2 1.7, 1.8, 2.0 for M_b 1e8, 1e9, 1e10 at L 0.5, 1, 2 kpc. Equilibrium needs H0 tau <~ 1, tau ~= (3/2C)(rho/rho_b)(v/a0) (Eq. 4.3-4.5).
- Converted to dimensions (my algebra from Eq. 6.5, checked against Eq. 5.9 rho r dv^2/dr ~ C a0 M_b(r)/(4 pi r^2)), for a general spherical baryon density rho_b(r):
  d(rho v^2)/dr = -rho G (M + M_b)/r^2; d/dr [r^3 rho v dv^2/dr] = C a0 rho_b v r^2; dM/dr = 4 pi r^2 rho.
  Origin: rho0 = R s/(8 pi G L^2), v0^2 = v hat_0^2 s, dv^2/dr(0) = C a0 rho_b(0)/(3 rho0).
- Baryons: spherical, M_b(r) = v_b^2 r/G from SPARC (running maximum so mass is non-decreasing), rho_b = dM_b/dr/(4 pi r^2) by log interpolation, uniform inside the first point; L = R_d. Gravity of baryons from SPARC g_b, so the graded total is g_b + G M_DM/r^2.
- Control C_K, frozen: the nondimensional Eq. 6.5 with exponential baryons, C = 1/16, Table 2's (R, v0^2) and a0 = 1.2e-10 must give V^4 at r = 10 L within 10 % of the simple-interpolating-function (the law's form) curve on the same baryons, as the paper states (< 10 %). The dimensional SPARC solver must agree with the nondimensional one on the same exponential baryons to < 1e-3 dex.
- Rows: K0 published, C = 1/16, a0 = A0 imposed (the law's value, put in by hand), R = 5.7, v0^2 = 1.8 for every galaxy (Table 2 middle row; 0 fitted knobs). K3: C a0 (one product: only C a0 enters the equations), R, v0^2 global (3 knobs). K2g per galaxy: R_i, v0_i^2 free (342) with C a0 from K3.
- Native acceleration scale: C a0 (an input; v^4 -> C a0 G M_b times an order-one solution factor); a_eff from lib.fit_a.
- Consistency: H0 tau at each galaxy's last measured radius from the solution, fraction with H0 tau <= 1; and A7 M3's required sigma/m beside the FKP value sigma/m = C a0/(rho v^2) at that radius (heavy limit, epsilon = m_b v^2, Eq. 3.15/4.1).

## Gates (LANE_BRIEF_COMMON.md, fixed)
- E1 rms to law <= 0.02, E2 p95 per galaxy <= 0.04, E3 worst bin <= 0.02 (lib.grade bins), holdout: tune on GS[::2], E1 on GS[1::2] <= 0.025, for every globally tuned row (F1, F1b, F2, F3, K3). Rms to observed reported beside. Knobs at bounds reported. Bounds: log Sigma_h 0 to 4 (Msun/pc^2), k 0.2 to 10, log K wide (+-4 dex about the start), p 0 to 1.5, log C a0 -13 to -8, R 0.1 to 100, v0^2 0.1 to 20.
- G1 kappa_eff = a/(c sqrt(G rho_DE0)) within 0.05 dex of 0.5, with a = lib.fit_a pooled and the native scale (a_F, C a0) both reported. Tuned rows inherit the law's a0 and pass by construction where they pass; stated.
- G2 slope d ln a/d ln rho_DE 0.5 +- 0.05: read from the equations (rho_DE appears in none quoted: native slope 0 expected, verified by listing every constant the scale depends on), and numerically G2x pooled over A29's evolving backgrounds for each z reading.
- G3 a(z)/a(0) bands at z 1, 1.5, 2.33. G4 rms of per-galaxy log a_i over SPARC hosts with SHMR log M200 11 to 12.5 <= 0.1 dex (per-galaxy a_i = lib.fit_a on that galaxy's model curve). G5 halo gravity at measured radii: pass by definition for both.
- GT in the A29 backgrounds (B0 to B5, rho_DE(z) from recipe31's definitions via colossus): |log10[a(z)/a(0)] - 0.5 log10[rho_DE(z)/rho_DE0]| <= 0.05 at z 1, 1.5, 2.33.
- z readings, fixed now: Foot (r1) lambda, K constant: a flat; (r2) R_SN tracks the cosmic star formation density at fixed lambda and M_b, a proportional to (psi(z)/psi(0))^2, psi Madau & Dickinson 2014 (1+z)^2.7/(1 + ((1+z)/2.9)^5.6) (from memory, PROVISIONAL); FKP (r1) C a0 constant (cross-section microphysics): flat; (r2) the paper's estimate a0 = cH/6 read as cH(z)/6 (my reading, stated).
- Cassini: not graded; neither source states the DM-baryon equilibrium on Solar System scales (stated, not a pass).

## Expected in advance
Foot F0 fails E1 well above 0.05 (rho0 r0 constant gives v_asym^2 proportional to R_d, not M_b^(1/2)); F2 with one knob reaches about 0.04 to 0.08 (shape fixed by r_D, misses at small r as the paper says) and fails E1; per galaxy F5 may approach but not reach 0.02. FKP K0 lands within 0.03 to 0.08 of the law (the paper's < 10 % in V^4 is 0.04 dex in g), K3 near 0.02 to 0.04, K2g may pass E1 with 342 parameters. Both: the acceleration scale is an input (K or C a0), rho_DE appears nowhere, G2 = 0, GT fails in B1 and B3 type backgrounds (the flat reading passes GT only where rho_DE barely moves), G1 only by tuning. No tie.

Rival language; adopts nothing. kappa = 1/2 FITTED; not theory closed.

## RESULTS (written after the run; criteria above unchanged)

Runtime 165 s, peak RSS 84 MB, single thread, one run of `recipe39.py`; no bug found, no wrong output to keep. Line numbers refer to `scripts/recipe39.out` unless marked 39b (`recipe39b.out`) or 39c (`recipe39c.out`).

Controls. C_K PASSES (l.37-39): dimensional solver against the paper's nondimensional Eq. 6.5 agrees to 6e-6 dex; with Table 2's (R, v0^2) and C = 1/16, V^4 at 10 L is within -1.8 % to +0.3 % of the simple-interpolating-function curve, as the paper states. C_F FAILS (l.6): the spherical average of Eq. 11 is matched best by a quasi-isothermal r0/r_D = 0.707 (rms 0.036 dex in log v^2), not the paper's 1.4; the paper's figure is in the disc plane, mine spherical. So F2-F5 use a more concentrated halo than the paper's in-plane curve. Post-result row added because of that (below).

(a) Dissipative / mirror DM. NOT EXACT at any parameter count tried.
- F0 published 2013 scaling, 0 knobs (l.7-9): E1 0.1536, E2 0.2098, E3 0.1850, rms to observed 0.2511; a_fit 0.446 A0; G4 0.196 dex. rho0 r0 constant makes v_asym^2 proportional to R_d, so the native a_i = (4 pi G Sigma r0)^2/(G M_b) spreads 0.525 dex over SPARC (median 0.81 A0).
- F1 (Sigma free, 1 knob) 0.1163, holdout 0.1171; F1b (+ r0 coefficient, 2 knobs; lands at k 1.49) 0.1161, holdout 0.1167 (l.10-17).
- F2 published 2017 recipe, lambda R_SN = K sqrt(M_b), 1 knob (l.18-22): E1 0.0715, E2 0.1520, E3 0.0152 (pass), observed 0.1961, holdout 0.0648, G4 0.126 (fail). F3, 3 knobs (p lands at 0.503, the paper's 1/2; k 0.885): 0.0702, holdout 0.0646, G4 0.113 (l.23-27).
- Post-result row (39b, after C_F failed; disclosed): the paper's stated in-plane equivalent, quasi-isothermal r0 = k R_d with 4 pi rho0 r0^2 = K sqrt(M_b). k fixed at 1.4: E1 0.1141, E3 0.0291, holdout 0.1097; k free: 0.0745 with k 0.67, holdout 0.0683; 3 knobs 0.0745. The law prefers half the paper's core radius; either geometry stalls near 0.07.
- Per galaxy (l.28-33): F4 lambda R_SN per galaxy (172 params) 0.0468; F5 lambda R_SN and k per galaxy (342) 0.0306, E2 0.0635, no k at bound; quasi-isothermal per galaxy (39b, 342) 0.0390. Two parameters per galaxy do not reach E1; the fixed shape (core then 1/r^2) cannot follow the law where baryons dominate.

(b) Famaey-Khoury-Penco. NOT EXACT at any parameter count tried.
- K0 published (C 1/16, a0 = A0 put in, R 5.7, v0^2 1.8, 0 fitted) (l.41-42): E1 0.1864, E2 0.2971, E3 0.1929, observed 0.2649, a_fit 0.474 A0, G4 0.522 dex.
- K3, 3 global knobs (l.44-49): 0.1550, holdout 0.1417, G4 0.508; C a0 = 0.205 A0 (a0 = 3.3 A0 at C = 1/16). Single start, 40 evaluations (disclosed).
- K2g per galaxy R_i, v0_i^2 (343 params) (l.51-53): E1 0.0577, E2 0.1030, E3 0.0265; 18 galaxies with a knob at bound.
- Post-result diagnostic (39c and a scratch check of the control, not grades): on the paper's own exponential spheres with each SPARC M_b and L = R_d, K0 sits 0.127 dex from the law, worst at small epsilon. The paper's own Table 2 solutions match the simple-IF curve beyond 2 L (|residual| <= 0.01 dex) but fall 0.06 to 0.10 dex short at r = L and 0.16 to 0.23 at 0.5 L: the heat-balance halo has too little dark mass inside the disc scale. SPARC's last radius is at median 5.8 L, so the inner deficit dominates the grade. The failure is in the model's inner shape, not in my solver (C_K) or only in the SPARC baryon deprojection.
- Consistency (l.48-49): H0 tau at the last radius median 0.098, 64 % with H0 tau <= 1 (the rest sit where SPARC's baryon density has stopped growing, so rho_b -> 0 there); FKP's own sigma/m = C a0/(rho v^2) there, median 374 cm^2/g (16-84: 71 to 887), against A7 M3's 40 needed for one exchange in 13 Gyr.

(c) Acceleration scale and the tie. NO TIE in either family.
- What sets the scale: Foot, a_F = G K^2/M with K the lambda R_SN normalisation (lambda from dark photoionisation and cooling cross sections and the supernova spectrum; the 2017 paper fixes K by normalising to the RAR with a0 = 1.2e-10 from MOND). FKP, the product C a0 of the cross-section normalisation, Eq. 4.1, an input; a0 ~ cH0/6 is an estimate. rho_DE, Lambda and H appear in none of the equations used: native G2 slope 0 (l.94), imposed if anything, never derived.
- G1 (l.87-93): F2 native a_F kappa_eff 0.4375 (0.058 dex, FAIL narrowly), F3 0.387, K3 C a0 0.103, FKP cH0/6 reading 0.583 (0.067, FAIL), published F0 0.223 and K0 0.237. Tuned rows' pooled a_fit (F2 0.483, F5 0.496, K2g 0.484) pass G1 only because they were tuned to the law.
- G2x (l.66, 76, 86): flat reading 0.000, SFR reading -0.136, cH/6 reading -0.112; all FAIL.
- G3: flat reading passes (1.000); Foot SFR reading a(z)/a(0) 34, 69, 66 (FAIL); FKP cH(z)/6 1.79, 2.37, 3.51 in B0 (FAIL).
- GT (l.57-86): flat reading passes only where rho_DE barely moves (B0, B2, B4, B5) and fails in B1, B1p, B1u (+0.076 to +0.096 at z 2.33) and B3 (-0.154); SFR reading +1.5 to +1.9 dex everywhere; cH/6 reading +0.40 to +0.64 at z 2.33 everywhere.
- G4: global rows fail (F2 0.126, F3 0.113, K3 0.508); per-galaxy rows pass (F4 0.008, F5 0.003, K2g 0.021) by inheriting the law they were fitted to. G5: halo gravity, pass by definition. Cassini: not graded.

Verdict: both baryon-tied dark matter routes reproduce a deep-MOND-like tail by construction (BTFR normalisation imposed in Foot 2017; C a0 imposed in FKP), but on SPARC neither is exact. Best global 0.0702 (Foot, 3 knobs) and 0.1550 (FKP, 3 knobs); best per galaxy 0.0306 (Foot, 342) and 0.0577 (FKP, 343). Neither carries rho_DE: the scale is an imposed constant, so the flat reading passes GT only in near-Lambda backgrounds, and no reading gives slope 0.5. Expected outcomes confirmed, except FKP did worse than expected (K0 0.186 against the expected 0.03 to 0.08), traced to its inner deficit, and C_F failed.

Deviations: C_F failed, so F2-F5 use the spherical average, and the in-plane equivalent was added post-result (39b). The FKP diagnostic (39c) and the control residual check (a scratch script, numbers above) are post-result. K3 was a single start. One tool artefact: the arXiv PDF of 1712.01316 was auto-saved by a WebFetch call (2.1 MB, tool-results folder), never opened.

Provisional: every equation is from summariser-read web pages (ar5iv 1712.01316, 1611.02422, 1307.1755); the 50 Msun/pc^2 reference value, Table 2's (R, v0^2) and C = 1/16 are as the summariser read them; Madau-Dickinson psi(z) is from memory; A29 w0, wa values carry A29's flags.

Rival language; adopts nothing. kappa = 1/2 FITTED; not theory closed.
