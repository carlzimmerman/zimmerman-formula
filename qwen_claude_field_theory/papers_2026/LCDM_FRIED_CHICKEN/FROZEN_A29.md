# FROZEN A29: LCDM's halo machinery in evolving dark-energy backgrounds

Frozen before any A29 number. Script `scripts/recipe31.py`, output `scripts/recipe31.out`, checkpoint `scripts/recipe31.json`. Quarantined experiment: rival language, adopts nothing, never feeds anything outside this folder. Passing shows freedom, not evidence. kappa = 1/2 FITTED; not theory closed.

Known before freezing: only an API check (colossus accepts de_model 'w0wa' and 'user' with wz_function, and computes growth by ODE for non-Lambda models). No A29 number was computed or seen. Known from the record: A13 T1 kappa_eff 0.551, T2 0.461; A15 U1 median 0.612 a0, rises 1.49x by z 2.33 at fixed M; A26 R11b at K11B: G1 0.497, Bz a(z)/a(0) 1.93, 2.67, 4.55, Az 1.48, 1.93, 3.02, S_base 0.0275 dex region (exact value recomputed here).

## Question

The tie written by the target is a0(z) = kappa c sqrt(G rho_DE(z)): a0 TRACKS dark energy. In Lambda rho_DE is constant, so tracking means "flat", and every earlier lane could only test flatness. In an evolving-DE background rho_DE(z) moves, so tracking becomes a measurable shape. (i) Does any LCDM halo scale follow sqrt(rho_DE(z)), or does it follow H(z) and rho_m? (ii) The generalised Lambda coincidence tracks by construction; grade G5 for it. (iii) Can one evolving-DE choice make the frozen R11b recipe pass GT and G2 with its 14 knobs frozen?

## Backgrounds (fixed now)

All flat, no relativistic species in colossus (as lib.py), today's H0 67.4, Om0 0.315, Ob0 0.0493, ns 0.965 held fixed, so rho_DE0 = 0.685 rho_crit0 is the same in all of them; only the history w(z) changes. CPL w(a) = w0 + wa (1 - a), rho_DE(a)/rho_DE0 = a^(-3(1 + w0 + wa)) exp(-3 wa (1 - a)).
- B0 LCDM control (w = -1).
- B1 DESI DR2 BAO + CMB + DESY5: w0 -0.752, wa -0.86 (from memory; a web search on 11-04 did not return the numbers, so PROVISIONAL). Quintom-B: phantom in the past, crosses w = -1 near z 0.4.
- B1p DESI DR2 + CMB + Pantheon+: w0 -0.838, wa -0.62 (from memory, provisional).
- B1u DESI DR2 + CMB + Union3: w0 -0.667, wa -1.09 (from memory, provisional).
- B2 thawing quintessence (CPL stand-in): w0 -0.9, wa -0.1 (w -> -1 early, rises late).
- B3 freezing/tracker (CPL stand-in): w0 -0.95, wa +0.35 (w -0.6 early, freezes to -1).
- B4 phantom crossing, quintom-A (the opposite direction to B1): w0 -1.1, wa +0.3 (w -0.8 early, crosses -1 at z 0.5, phantom today).
- B5 early dark energy: Lambda plus a Poulin-type fluid, rho_EDE(a) = 2 rho_EDE(a_c) / (1 + (a/a_c)^(3(1 + w_n))), w_n = 1/2 (n = 3), z_c = 3500, amplitude set so f_EDE = rho_EDE/(rho_m + rho_r + rho_EDE + rho_L) = 0.1 at z_c with Omega_r h^2 = 4.18e-5 (from memory). Entered into colossus as de_model 'user' with w(z) = -1 - (1/3) d ln rho_DE / d ln a of the total rho_L + rho_EDE; colossus has no radiation, so radiation enters only the f_EDE normalisation (stated). Ode0 = 1 - Om0 includes the tiny EDE remnant today.

Two amplitude footings: P (primary) fixed primordial amplitude, sigma8 of each background chosen so that sigma(8 Mpc/h, z = 30) equals the base B0 value (same early universe, only late growth differs; A26 C1 rule); S (disclosed) sigma8 = 0.811 today in every background. colossus current cosmology is set explicitly before every concentration, sigma and mass-function call and restored (the A1 bug).

Redshifts: z = 0, 1, 1.5, 2.33.

## Scales graded (fixed now; nothing tuned)

- T1 a = c H(z)/2 pi.
- T2g generalised Lambda coincidence a = c sqrt(8 pi G rho_DE(z)/3)/2 pi (A13 T2 with rho_DE(z)).
- T3 NFW central acceleration 2 pi G rho_s r_s at M200 = 1e12 Msun, 200c of rho_crit(z), Diemer19 c(M, z) in that background. G4 over log M200 11 to 12.5 (0.25 steps) at z = 0.
- U1 per SPARC galaxy (A15): M200 from lib.py's SHMR (z = 0, unchanged across backgrounds), Diemer19 c and rho_crit of the background; median g_i, kappa_eff; z evolution at the median M200 held fixed (A15 H4 rule).
- R11b frozen at K11B (A26 machinery, `recipe28.py` galx with no modifiers): rebuilt with the background's rho_crit(z) and Diemer19 c(M, z); effective a = lib.fit_a pooled over 3373 points; shape S = rms of log g_recipe - log law(g_b, a_fit). z rows: Bz (primary, Moster 2013 z-terms on the K11B SHMR, coefficients from memory as in A26) and Az (SHMR at z = 0, disclosed). G4 = per-galaxy a_i at z = 0, log M200 (K11B SHMR) 11 to 12.5.

## Gates (fixed now)

- G1 kappa_eff = a(0)/(c sqrt(G rho_DE0)) within 0.05 dex of 0.5, per background. For R11b this passes by construction (tuned at A0 in B0), stated.
- G2 three readings, each 0.50 +- 0.05:
  - G2z within a background: least-squares slope of ln a against ln rho_DE(z) over z = 0, 1, 1.5, 2.33. Measurable only if ln[max/min rho_DE(z)] >= 0.1 over those z; otherwise "not measurable" (B0, B5 expected).
  - G2x across backgrounds: pooled least-squares slope of ln[a(z)/a(0)] against ln[rho_DE(z)/rho_DE0] over all (background, z > 0) points of B1, B1p, B1u, B2, B3, B4 (18 points).
  - G2t across rho_DE today: in B1's w0, wa, rho_DE0 scaled by f in {0.5, 0.71, 1, 1.41, 2} on the A26 C1 physical footing (omega_m = 0.315 h0^2, omega_b = 0.0493 h0^2 fixed, h = sqrt(omega_m + f 0.685 h0^2), early amplitude fixed at z = 30 for an 8/h0 Mpc physical radius); slope of ln a(0) against ln f. Run for T1, T3, U1 and R11b (A, fixed SHMR). T2g has slope 0.5 identically.
- G3 a(z)/a(0) inside [0.76,1.03], [0.71,1.12], [0.33,1.21] at z 1, 1.5, 2.33 (bands as frozen in A13; they were set for the law's record, not for each background, stated).
- G4 one constant across hosts, log M200 11 to 12.5, rms <= 0.1 dex. T1, T2g mass-free: pass by construction.
- G5 operative at galaxy radii: halo routes (T3, U1, R11b) pass by definition (halo gravity at measured radii). T1 and T2g: the acceleration the background exerts at r = 10 kpc must be >= 0.1 a0. For T2g two readings: the Lambda form (8 pi G rho_DE/3) r and the fluid form |(4 pi G/3) rho_DE (1 + 3 w)| r with w(z) of the background; for T1 |q(z)| H(z)^2 r. Expected ~1e-5 a0 for T2g.
- GT (new, tracking): |log10[a(z)/a(0)] - 0.5 log10[rho_DE(z)/rho_DE0]| <= 0.05 dex at each of z 1, 1.5, 2.33, in each evolving background (B1 to B5); B0 reported as control (there GT equals the flatness test).

A scale TRACKS in a background only if GT passes there; it supplies the tie only if G1, G2 (all measurable readings), G3, G4, GT and G5 all pass.

## (iii) One evolving-DE choice for R11b, knobs frozen

Grid on footing P: w0 from -1.6 to -0.2 step 0.1 (15), wa from -3.0 to +2.0 step 0.25 (21), 315 CPL backgrounds, today's parameters as above. For each: R11b Bz rows at z 0, 1, 1.5, 2.33 (Az also recorded), GT, G2z, G3, G1, shape S max over z <= S_base + 0.005 (A26's shape rule), and Omega_DE(z = 2.33). A hit passes GT, G2z, G1 and S. Plausibility, my judgement fixed now: a hit counts as "DESI-like" only if w0 in [-1.2, -0.4] and wa in [-2.5, +0.5]; any hit outside is reported as such. The evolving-DE pair is counted as 2 extra parameters (w0, wa); 14 recipe knobs stay frozen. Also reported: the grid point with the smallest worst-z GT deviation, and its other gates. No data are graded here: BAO and SN constraints are not refitted.

## Expected in advance

(i) T1, T3, U1 and R11b follow H(z) and rho_m, not sqrt(rho_DE): GT fails in every evolving background, by about +0.3 to +0.7 dex at z 2.33 for T1 and R11b, smaller for T3/U1; G2z slopes are of either sign and far from 0.5 because rho_DE(z) moves little while H(z) moves a lot; G2x pooled slope not 0.5. G2t for B1 resembles A26 C1 (slope near 0.25 for R11b). (ii) T2g passes G1 (0.461), G2 (all readings, identically), GT (identically), G4; G3 passes except where rho_DE(z) grows strongly (B3 freezing may leave the 1.21 band at z 2.33); G5 fails at ~1e-5 a0. (iii) No CPL point passes GT for R11b with S: tracking needs rho_DE(z)/rho_DE0 near the square of a(z)/a(0) (~4 to 20), which forces DE to dominate at z 2.33, which raises H(z) and rho_crit(z) and moves the halos further; if a hit appears it lies outside the DESI-like box and breaks S.

Rival language; adopts nothing. kappa = 1/2 FITTED; not theory closed.

## RESULTS (written after the run; criteria above unchanged)

Runtime 75 s, peak RSS 79 MB, single thread, one run, no bug found, no wrong output to keep. Line numbers refer to `scripts/recipe31.out`. Controls (l.3-4): B0 on footing P returns sigma8 0.8110 and lib's c-grid exactly; the rebuilt R11b reproduces recipe18 gal3 at K11B to 0 dex; base a 0.9940 A0, S_base 0.0275 (A26's values). B5's EDE has f 0.1000 at z_c and a 1e-6 share of Ode0 today (l.2), so at z <= 2.33 B5 is Lambda to 2e-4 (G2z not measurable there, as expected).

rho_DE(z)/rho_DE0 at z 1, 1.5, 2.33 (l.17 and per background): B1 1.018, 0.874, 0.668 (sqrt 1.009, 0.935, 0.817); B1p 0.978, 0.867, 0.704; B1u 1.063, 0.888, 0.642; B2 1.16, 1.20, 1.23; B3 1.36, 1.60, 2.03; B4 0.97, 1.01, 1.10. H(z)/H0 moves 1.78 to 3.61 in all of them, almost the same as B0's 1.79, 2.37, 3.51.

(i) Footing P. No LCDM halo scale tracks sqrt(rho_DE(z)); all follow H(z) and rho_m, nearly unchanged by the DE history.
- T1 cH/2pi: kappa_eff 0.5565 (G1 pass), GT dev at z 2.33 +0.50 to +0.63 dex in every background, G3 fail, G2z slopes -2.9 to +6.8, G5 |q|H^2 r 3e-6 to 1e-5 a0 (fail).
- T3 NFW central at 1e12: kappa_eff 0.40 to 0.44 (G1 fail), a(z)/a(0) 1.75 to 1.97 by z 2.33, GT dev at 2.33 +0.14 (B3) to +0.35 (B1u), G2z -1.5 to +4.1, G4 0.088 (pass, as A15's disclosure said).
- U1 per SPARC galaxy: kappa_eff 0.28 to 0.31 (G1 fail), a(2.33)/a(0) 1.48 to 1.65 (G3 fail), GT dev at 2.33 +0.06 (B3) to +0.27 (B1u), G2z -1.0 to +3.0, G4 0.077 (pass).
- R11b Bz: kappa_eff 0.467 to 0.499 (G1 pass by construction; drifts down to 0.467 in B3), a(z)/a(0) 1.91-2.09, 2.64-2.92, 4.49-5.01 (G3 fail), GT dev at 2.33 +0.55 (B3) to +0.75 (B1u), G2z -3.6 to +8.6, G4 0.047 (pass, tuning showing through), S max 0.084 (fail). Az: 2.98 to 3.32 by z 2.33, GT dev +0.35 to +0.57, S 0.047 (fail).
- G2x across backgrounds (l.155-166): pooled slopes T1 -0.11, T3 +0.003, U1 +0.026, R11b Bz -0.095, Az -0.065 (P); -0.12 to -0.004 (S), against 0.5. The halo scales do not see rho_DE's history at all.
- G2t across rho_DE today in B1's w0, wa (l.182-186): T1 +0.34, T3 +0.14, U1 +0.13, R11b +0.26 (A26 C1-A gave +0.254 in Lambda).
- Footing S (sigma8 0.811 today) changes little, with one exception, against the expectation: U1 in B3 (freezing) passes GT (l.131: dev -0.007, +0.007, +0.048, the last within 0.002 of the tolerance) while failing G1 (0.306), G2z (+0.65), G3 (1.59 at z 2.33). On footing P the same row fails GT (+0.065 at 2.33). Reading: B3's rho_DE rises 2x by z 2.33, which happens to land near U1's own H-driven rise (1.49x in Lambda); it is a coincidence of one background and one footing, not tracking: the same scale misses GT by +0.26 in B1u and its cross-background slope G2x is -0.005.

(ii) T2g, the generalised Lambda coincidence c sqrt(8 pi G rho_DE(z)/3)/2pi, tracks by construction: GT dev 0.0000 in all eight backgrounds, G2z, G2x and G2t exactly +0.5000, kappa_eff 0.4607 (G1 pass), G4 mass-free. G3 fails where rho_DE itself leaves the band (B1u 1.031 at z 1 > 1.03, B2 1.078, B3 1.166-1.425), which says the A13 bands were written for Lambda, not that T2g fails to track. G5 FAILS everywhere: the pull at 10 kpc is 1.08e-5 a0 in the Lambda form, 5.4e-6 to 1.24e-5 a0 in the fluid form (4 pi G/3) rho_DE |1+3w| r, 6.9e-6 to 2.2e-5 a0 at z 1 to 2.33. So the one scale that tracks acts on nothing in a galaxy, as expected.

(iii) CPL scan, 315 backgrounds, R11b with 14 knobs frozen (l.204-206): 0 pass GT + G2z + G1 + S. Exactly one passes GT alone: w0 -0.50, wa +2.00, at the grid's edge in wa, where rho_DE(z)/rho_DE0 is 9.0, 26, 124 at z 1, 1.5, 2.33 (w = +1.5 early, Omega_DE(2.33) 0.88, sigma8 today 3.07 on footing P). There GT dev is +0.044, +0.027, +0.027 and G2z +0.512, but kappa_eff today is 3.56 (G1 off by 0.85 dex), S max 0.125 (4.5x the base shape error) and it lies outside the DESI-like box. That background has dark energy dominating at z 2.33 and an unphysical amplitude; it is a reparametrisation, not a recipe that tracks. Closest inside the DESI-like box: w0 -0.50, wa 0.00, GT dev +0.21, +0.30, +0.45, G2z +1.06, S 0.089. Counting: the one GT pass costs 2 extra parameters (w0, wa) with wa at the grid bound.

Verdict: NO TRACKING. (i) In every evolving-DE background LCDM's halo scales follow H(z) and rho_m, and they are almost blind to the DE history (cross-background slopes -0.12 to +0.03 against 0.5). (ii) Only the generalised Lambda coincidence tracks, by construction, and its pull at 10 kpc is about 1e-5 a0. (iii) No evolving-DE choice makes R11b track with its knobs frozen; the only GT pass needs DE dominating at z 2.33 and breaks G1 and the law's shape. Expected outcomes confirmed, except U1's one GT pass on footing S in B3, disclosed above.

Deviations: none from the frozen procedure. Disclosed: the U1 z rows hold the median M200 fixed (A15 H4 rule), while its kappa_eff is the per-galaxy median, as frozen; the scan's only GT pass sits at the wa grid edge.

Provisional: the DESI DR2 w0, wa values for B1, B1p, B1u are from memory (the 11-04 web search did not return them); Moster 2013 z coefficients (from memory, as in A26); Omega_r h^2 4.18e-5 for the EDE normalisation (from memory). The B2 to B4 CPL forms are stand-ins for thawing, freezing and quintom-A models, not fits. No downloads.

Rival language; adopts nothing. kappa = 1/2 FITTED; not theory closed.
