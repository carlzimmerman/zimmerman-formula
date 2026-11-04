# FROZEN A24: emergent (entropic) gravity tied to the de Sitter horizon

Frozen before any A24 number. Script `scripts/recipe26.py`, output `scripts/recipe26.out`. Quarantined experiment: rival language, adopts nothing, never feeds anything outside this folder. Passing shows freedom, not evidence.

## Source, what is derived and what is imposed

Look-ups PROVISIONAL (WebFetch summaries of ar5iv/arXiv pages, 11-04; no PDF downloaded):
- Verlinde 2016, arXiv 1611.02269 (SciPost Phys 2, 016, 2017). Eq. 7.40 (integral form): int_0^r G M_D(r')^2 / r'^2 dr' = M_B(r) a0 r / 6, with a0 = c H0 ("Hubble acceleration scale", L = c/H0, eq. 1.2). Differentiating gives the local form M_D(r)^2 = (a0 r^2 / 6G) d(M_B r)/dr. Point mass (eq. 7.43): g_D = sqrt(a_M g_B), a_M = a0/6 = c H0/6. Total g = g_B + g_D (apparent mass added to baryonic mass). Stated scope: approximately spherical, isolated, non-dynamical (quasi-static) systems, centralised mass; the "dark gravity" regime is surface density Sigma < a0/(8 pi G) (eq. 1.3); the derivation gives an inequality that is an equality only near the main mass; H0 treated as constant in the calculation; cosmological evolution out of scope.
- Hossenfelder 2017, arXiv 1703.01415, covariant vector-field version: non-relativistic potential phi = sqrt(M/L) ln r (Planck units), a 1/r force, with a0^2 = Lambda set "by order of magnitude" only; the prefactor is not fixed; Schwarzschild corrections are powers of GM/(c^2 r), negligible at galaxy radii. No interpolation, no Tully-Fisher coefficient derived.
- Lelli, McGaugh, Schombert 2017, arXiv 1702.04355 (abstract): EG fits the SPARC RAR only with substantially lowered stellar M/L, predicts a radius trend in RAR residuals that is not seen, and differs from MOND in the inner parts of extended galaxies.
- Brouwer et al. 2017, arXiv 1612.03034 (abstract): point-mass EG prediction agrees with KiDS+GAMA lensing of 33,613 isolated centrals in four mass bins, no free parameter, LCDM background assumed. No chi2 in the abstract.

Derived in the paper (heuristically, from an elastic-medium entropy argument, not from an action): the form of eq. 7.40 and the factor 1/6 = (d-3)/((d-2)(d-1)) at d = 4. Imposed: a0 = c H0 by identifying L with the Hubble radius; which H (H0, H(z) or the de Sitter limit H_inf = c sqrt(Lambda/3)); linear addition g_B + g_D; equality rather than inequality; for SPARC discs, the spherical-equivalent mass (imposed by us, as by Lelli+2017).

## Conversion to SPARC (stated before numbers)

SPARC from lib.load(): 171 galaxies, 3373 points, Upsilon 0.5/0.7. Spherical-equivalent baryonic mass M_B(r) = r V_b(r)^2 / G = g_b r^2 / G (lib's g.mb). Then g_D^2 = a_M g_b (1 + s), s = d ln M_B / d ln r, taken by np.gradient of ln M_B in ln r over each galaxy's measured points. Where 1 + s < 0 (spherical-equivalent mass falling, from the signed gas term), M_D^2 < 0: set g_D = 0 at that point and count it as outside the formula. Cosmology: lib's (H0 67.4, Om0 0.315, flat, Ode0 0.685); rho_DE = Ode0 rho_crit.

## Rows graded on SPARC (lib.grade: E1 <= 0.02, E2 <= 0.04, E3 <= 0.02; rms to observed reported against the law's 0.1951)
- V0 point mass, a_M = c H0/6, 0 knobs: g = g_b + sqrt(a_M g_b).
- V1 extended (eq. 7.40 local form), a_M = c H0/6, 0 knobs.
- V2 point mass and V3 extended with the de Sitter reading a_M = c H_inf/6, H_inf = H0 sqrt(Ode0), 0 knobs.
- V4 extended, one global factor f on a_M fitted (1 knob, bounds 0.1 to 10): tuned on all, and tuned on GS[::2] graded unseen on GS[1::2] (holdout <= 0.025). Same for V0 form (V4p).
- V5 Hossenfelder reading, point mass, a = c^2 sqrt(Lambda) (her order-of-magnitude a0^2 = Lambda), 0 knobs. Her free prefactor fitted is V4p by construction, so it is not run separately.
- Diagnostic (not a gate), set now: V1 graded only on points inside the stated regime (Sigma_B < a0/(8 pi G), i.e. 4 pi G Sigma_B = g_b < c H0/2 with Sigma_B = M_B/(4 pi r^2), and 1 + s >= 0).

## Tie gates (A13 G1 to G5), for the H0 / H(z) reading and the H_inf reading
- G1 kappa_eff = a_M/(c sqrt(G rho_DE)) within 0.05 dex of 0.5. Also for V5.
- G2 slope d ln a_M / d ln rho_DE over the three J cosmologies (OL, H0) = (0.70, 67.4), (0.685, 73), (0.65, 73): 0.50 +- 0.05.
- G3 a(z)/a(0) at z 1, 1.5, 2.33 inside [0.76,1.03], [0.71,1.12], [0.33,1.21]; H reading drifts as H(z)/H0 (lib cosmology), H_inf reading is flat.
- G4 one constant across hosts: per-galaxy effective a = fit_a of the law form to that galaxy's V1 (resp. V3) curve, rms of log a over galaxies with SHMR log M200 in 11 to 12.5 <= 0.1 dex. (The route constant itself is universal; this grades what the extended formula does to it.)
- G5 operative at galaxy radii: g_D at 10 kpc for a 1e10 Msun point mass at least 0.1 a0. Passes by the theory's own posit; the posit is the mechanism, so this is reported as "pass by posit".

## Regime count (reported)
Galaxies (and points) with: g_b >= c H0/2 at any point and at more than half of points; 1 + s < 0 at any point; a bulge component (non-spherical in any case: every SPARC galaxy is a disc, so strictly 171 of 171 are outside "spherical"); isolation and quasi-static state are not assessable from SPARC and are stated as such.

## Expected in advance
E1 fails in every row: point mass gives g_b + sqrt(a g_b), which at g_b = a0 sits near +0.1 dex above the law (2.08 vs 1.62 a0 at a_M = 1.165 a0) and keeps growing as sqrt at high g_b; the extended form adds (1+s) up to 4 in rising inner parts. One knob lowers the level but cannot fix the shape, so V4 fails E1. G1: H0 reading kappa_eff = (1/6)/sqrt(3 Ode0/8 pi) = 0.583 (FAIL by about 0.07 dex); H_inf reading 0.482 (PASS); slope 0.5 exactly for H_inf; H(z) reading fails G3. Most points lie inside the Sigma threshold; a minority of galaxies have 1 + s < 0 somewhere.

## RESULTS (written after the run; criteria above unchanged)

No bug found; one run, 2 s, 78 MB RSS. Lines quoted from `scripts/recipe26.out`. Folder cosmology gives c sqrt(G rho_DE) = 1.8727e-10 and A0 = 0.4999 of it; a_M = cH0/6 = 1.166 a0, cH_inf/6 = 0.965 a0, c^2 sqrt(Lambda) = 10.03 a0.

SPARC, all FAIL E1 to E3 (law to observed 0.1951):
- V0 point mass, cH0/6: E1 0.0877, E2 0.1052, E3 0.1103; to observed 0.2135.
- V1 extended (eq. 7.40), cH0/6: E1 0.1997, E2 0.2918, E3 0.2042; to observed 0.2867, mean +0.18 dex (consistent in direction with Lelli+2017's lowered M/L, provisional).
- V2 point mass, cH_inf/6: E1 0.0642, E2 0.0865, E3 0.0924; to observed 0.2046.
- V3 extended, cH_inf/6: E1 0.1729, E2 0.2551, E3 0.1692; to observed 0.2684.
- V5 Hossenfelder c^2 sqrt(Lambda): E1 0.4384; to observed 0.4809.
- V4 extended, 1 knob f 0.286 (a 0.333 a0, not at bound): E1 0.0786, E2 0.1187, E3 0.0644; holdout unseen 0.0771 FAIL.
- V4p point mass, 1 knob f 0.577 (a 0.673 a0): E1 0.0392, E2 0.0546, E3 0.0660; to observed 0.1976; holdout unseen 0.0378 FAIL. Residual runs -0.044 to +0.066 across g_b bins: the shape g_b + sqrt(a g_b) is not the law's, so no level fixes it.

Tie gates:
- H reading (H0 today, H(z) at epoch): kappa_eff 0.583 (+0.067 dex) FAIL G1; slopes +0.579, +0.933 FAIL G2; a(z)/a(0) 1.790, 2.368, 3.510 FAIL G3; per-galaxy effective a (extended) rms 0.115 dex over 79 hosts FAIL G4; G5 pass by posit. NO TIE.
- H_inf reading (de Sitter, flat): kappa_eff 0.482 (-0.016 dex) PASS G1; slopes 0.500 PASS G2; ratio 1.000 PASS G3; effective a rms 0.115 dex FAIL G4 (point-mass form 0.071, diagnostic); G5 pass by posit. NO TIE on G4, and the scale passes G1 to G3 only as the number cH_inf/6 = sqrt(Lambda/3) c^2/6, which is the A13 T2 coincidence with 1/6 for 1/2 pi; the H_inf choice is imposed (the paper uses H0, treated as constant). Its SPARC curve still fails E1 (0.0642 / 0.1729).
- V5: kappa_eff 5.013 = sqrt(8 pi), +1.0 dex, FAIL G1; prefactor not fixed in the paper, so with it fitted it is V4p.

Regime (the relation's own scope): all 171 are flattened discs, so strictly none is spherical; 32 have a bulge; 7 of 3373 points in 4 galaxies have 1 + s < 0 (M_D^2 < 0); 351 points in 34 galaxies (more than half the points in 3) lie above Sigma = a0/(8 pi G); 134 of 171 have every point inside the stated regime. Isolation and quasi-static state not assessable. Restricting V1 to the 3015 in-regime points does not help: rms to law 0.2030, to observed 0.2910 (diagnostic).

Deviations: none from the frozen rows. All paper content is PROVISIONAL (WebFetch summaries of ar5iv/arXiv abstracts; the eq. 7.40 to local form differentiation was done by the summariser and checked here by hand for a point mass). Brouwer+2017's lensing agreement and Lelli+2017's results are quoted from abstracts only, not regraded.

Verdict: Verlinde emergent gravity does NOT reproduce the law on SPARC in any reading (best 0.0392 with one knob, holdout 0.0378), and does NOT tie a to rho_DE: the H0 reading fails G1 to G3, the de Sitter reading passes G1 to G3 as a number but fails G4 through the extended formula, and its horizon choice is imposed, not derived.

Rival language; adopts nothing. kappa = 1/2 FITTED; not theory closed.
