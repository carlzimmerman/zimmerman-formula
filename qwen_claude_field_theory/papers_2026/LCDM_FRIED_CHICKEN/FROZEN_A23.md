# FROZEN A23: dipolar dark matter (gravitational polarisation)

Frozen before any A23 number. Script `scripts/recipe25.py`, output `scripts/recipe25.out`. Quarantined experiment: rival language, adopts nothing, never feeds anything outside this folder. Passing shows freedom, not evidence. kappa = 1/2 FITTED; not theory closed.

## Sources (PROVISIONAL look-ups, WebFetch summaries of arXiv abstract/HTML pages; no PDF downloaded)

- Blanchet & Le Tiec 2008, PRD 78, 024031, arXiv:0804.3518. HTML read: potential expanded as W = W0 + (1/2) W2 Pi^2 + (1/6) W3 Pi^3 + O(Pi^4), with W2 = 4 pi G and W3 = 32 pi^2 G^2 / a0 ("a0 enters at third order"), fixed by matching MOND; W0 = Lambda / (8 pi G) (minimum of W). Non-relativistic limit: dv/dt - g = -Pi_hat W'(Pi); Poisson d_i(g^i - 4 pi G Pi^i) = -4 pi G (rho_b + sigma); mu = 1 + chi with Pi = -(chi / 4 pi G) g. Strong-field form of W not committed; a slow (gamma = 1) transition is said to be likely ruled out by the Solar System. Lambda-a0: abstract says Lambda "should be of the order of a0^2/c^4" if the model comes from a more fundamental theory; text defines a_Lambda = (c^2 / 2 pi) sqrt(Lambda/3), a_Lambda = alpha a0 with alpha ~ 0.8, and states the exact coefficient "cannot be determined presently". Weak clustering of the dipolar medium (sigma) is a hypothesis to be checked by N-body.
- Blanchet & Le Tiec 2009, PRD 80, 023524, arXiv:0901.3114: abstract claims LCDM at cosmological scales and MOND at galactic scales; no a0 statement in the abstract.
- Blanchet 2007, CQG 24, 3541, arXiv:gr-qc/0609121 (dipolar particles in GR, MOND in the NR limit). The companion CQG 24, 3529 (astro-ph/0605637, quasi-Newtonian polarisation) is cited from memory only.
- Blanchet & Heisenberg 2015, JCAP 12 (2015) 026, arXiv:1505.05146: abstract states a ghost in the decoupling limit of the dark matter sector, possibly pushed above the strong-coupling scale. Search summaries (provisional): 1701.07747 argues the decoupling limit is ghost-free with matter included; 2302.02690 says the ghost can return below the decoupling limit.

## Galactic limit used (derived here from the equations quoted above)

Static dipoles (v = 0): |g| = W'(Pi). Write y = 4 pi G Pi (an acceleration). Poisson, sigma = 0 (the papers' weak-clustering hypothesis, taken as given): g_N = g - y, so g_N = W'(y) - y with W' in acceleration units. The quoted expansion gives W'(y) = y + y^2/a0 + O(y^3).

## (a) Paper's own simplest W

W truncated at cubic order and taken as exact: W'(y) = y + y^2/a0, so y = sqrt(a0 g_N) and g = g_N + sqrt(a0 g_N). One global knob a0, fitted to the law's curves on all 171 (lib grade E1 to E3, rms to observed reported); holdout: a0 tuned on GS[::2], unseen rms to law on GS[1::2] <= 0.025. Also a0 fitted to the observed curves, as a diagnostic.
Expected: FAIL E1 to E3 (this nu = 1 + y^-1/2 leaves a sqrt(a0 g_N) tail at high g, a +0.1 dex scale excess near g_b ~ a0 to 10 a0 once a0 is fitted).

## (b) W(P) freedom, knob count

Deep-MOND matching fixes the first two coefficients; everything above is free. Two families, each fitted to the law (least squares in log g, all points; holdout on GS[::2]/GS[1::2]):
- T_n Taylor in the paper's own expansion: W'(y) = y + y^2/a0 + sum_{k=3..n} b_k y^k / a0^(k-1). Knobs a0 + (n - 2) coefficients. Run n = 3 to 8 and report the first n that passes E1, E2, E3 and holdout. Solved for y by bisection; a coefficient set with W'(y) - y non-increasing on the needed range is rejected (unphysical, not invertible).
- P Pade one-parameter: W'(y) = y (1 + (1 - q) y/a0) / (1 - q y/a0). It keeps the deep-MOND coefficient for every q, gives y = (-q g_N + sqrt(q^2 g_N^2 + 4 a0 g_N))/2; q = 0 is (a), q = 1 is the law exactly (W' = y/(1 - y/a0), polarisation saturating at y = a0). Knobs a0, q. This family contains the law, so a pass is by construction and counts as a function choice, not a derivation.
- The law itself as a W: W'(y) = y/(1 - y/a0) = y + y^2/a0 + y^3/a0^2 + ...: all higher coefficients b_k = 1. Counted as one function choice (knob choice), zero continuous knobs beyond a0.
Bounds: b_k in [-5, 5]; q in [-1, 2]; log a0 in [-11, -9]. Knobs at bound reported.
Expected: P passes with q near 1 (it contains the law); T_n needs n >= 6 or more, because the law's geometric series converges slowly at y = 0.9 a0 (g_b ~ 10 a0, the top of SPARC).
Diagnostic only (not a gate): extra acceleration y / g_N at Saturn (g_N = G M_sun / (9.58 AU)^2) for (a), the best T_n and the law, no external field.

## (c) Swoop: the Lambda-a0 relation at face value

rho_DE = Ode0 RHOC from lib (Lambda = 8 pi G rho_DE / c^2). a_Lambda = (c^2/2 pi) sqrt(Lambda/3) = (sqrt(8 pi/3)/2 pi) c sqrt(G rho_DE), so kappa_Lambda = 0.461 independent of data.
- G1 kappa_eff within 0.05 dex of 0.5, three readings: (i) the paper's alpha = 0.8, a0 = a_Lambda/0.8; (ii) a0 = a_Lambda (alpha = 1); (iii) model as written: a0 is W3's independent constant, kappa_eff = fitted a0 (a) / (c sqrt(G rho_DE)) is a fit, reported, not a tie.
- G2 slope d ln a0 / d ln rho_DE: as written W0 and W3 are separate constants, slope 0 (FAIL); with the naturalness relation imposed, 0.5 by hand (PASS, counted as a hand term).
- G3 a(z)/a(0): Lambda constant, W3 constant, so a0 is flat, 1 at all z: inside the band at 1, 1.5, 2.33 if 1 lies in each. Their a0 does not follow H(z).
- G4 one constant across hosts: a0 is a universal coefficient of W: PASS by construction.
- G5 operative: a0 sets galaxy dynamics through W3: PASS.
Verdict rule: the route ties a0 to rho_DE natively only if G1 to G5 pass with the relation derived in the model. Expected: NO NATIVE TIE: the relation is an order-of-magnitude naturalness claim (their words: coefficient "cannot be determined presently"), G2 holds only by hand; G1 passes at alpha = 1 (0.461, -0.035 dex) and fails at the paper's alpha = 0.8 (0.576, +0.061 dex).

## Known problems (provisional, from the sources above and memory)

Ghost in the decoupling limit (2015, disputed 2017, returning 2023); weak clustering of the dipolar medium assumed, not shown; the galactic limit is MOND-like so it inherits MOND's cluster shortfall (from memory, not computed here); a slow strong-field transition is disfavoured by the Solar System per the paper's own text; strong-field W not fixed by the theory.

## RESULTS (written after the run; criteria above unchanged)

No bug found. One run, `scripts/recipe25.out`, a few minutes (wall time not logged), 100 MB RSS, single thread.

(a) Cubic W taken as exact, a0 one knob: a0 6.30e-11 (fitted to the law), E1 0.0392 FAIL, E2 0.0546 FAIL, E3 0.0660 FAIL (bins -0.044 at log g_b -12 to +0.066 at -9.5), holdout unseen 0.0378 FAIL; rms to observed 0.1976 (law 0.1951). Fitted to observed, a0 6.18e-11 (-0.180 dex vs A0). As expected.

(b) W freedom. T_3 (2 knobs) passes E1 0.0098, E2 0.0148, holdout 0.0088 but fails E3 0.0214, with b3 at its bound 5. T_4 (3 knobs: a0 7.86e-11, b3 -0.585, b4 3.145, none at bound) is the first order passing all: E1 0.0036, E2 0.0057, E3 0.0091, holdout 0.0033. T_5 to T_8 pass too, each with one or two coefficients at the +-5 bound. The expectation (n >= 6) was wrong: once a0 is free and the coefficients are free, two extra coefficients absorb the slow convergence of the geometric series over SPARC's range; the T_n "a0" is then not the law's a0 (7.86e-11 at T_4), while the law-read a fit stays 9.36e-11. The Pade family returns q = 1.000 and a0 = A0, the law itself, exactly as built in. Control: the law as a W (W' = y/(1 - y/a0), polarisation saturating at 4 pi G Pi = a0) gives 0.0000. Honest count: the paper's dynamics plus a W chosen to reproduce the law costs a function choice; a polynomial W in the paper's own expansion needs a0 plus 2 tuned coefficients.
Diagnostic, Saturn y/g_N: cubic W 1.2e-3, law 1.45e-6. The T_4 entry prints nan because the inversion grid stops at y = 4 a0 (disclosed, not a gate); by hand, its quartic tail gives y about (g_N/b4)^(1/4) a0^(3/4), about 2.7e-5 of g_N. A polynomial W keeps a growing tail at high field.

(c) Swoop. kappa_Lambda = sqrt(8 pi/3)/2 pi = 0.4607. G1: at the paper's alpha 0.8, kappa_eff 0.576 (+0.061 dex) FAIL; at alpha 1, 0.461 (-0.036 dex) PASS; with lib A0, alpha = 0.921. Model as written: a0 is W3's own constant, the cubic-W fit gives kappa_eff 0.336, a fit. G2: 0 as written (W0 = Lambda/8 pi G and W3 = 32 pi^2 G^2/a0 are separate constants), FAIL; 0.5 only with the naturalness relation imposed by hand. G3: flat, 1.00 at z 1, 1.5, 2.33, PASS (a0 follows Lambda, i.e. stays constant, not H). G4 PASS by construction, G5 PASS. The relation is imposed, not derived: the paper says Lambda "should be of the order of" a0^2/c^4 and that the exact coefficient "cannot be determined presently" (provisional WebFetch reading). Verdict: NO NATIVE TIE.

Deviations: expectation in (b) wrong, as stated; Saturn diagnostic for T_4 out of grid. Provisional: every quotation and coefficient from the sources (W2, W3, W0, alpha 0.8, ghost history); the static-equilibrium reading |g| = W'(Pi) with sigma = 0 is derived here from the quoted equations, not checked against the papers' own galactic formulas.

Rival language; adopts nothing. kappa = 1/2 FITTED; not theory closed.
