# C -- holographic and species-bound principles for alpha (pre-registration)

Written 2026-09-28 BEFORE any of `c1_*.py`, `c2_*.py`, `c3_*.py` was run.
Target: alpha^-1 = 137.035999177 (Thomson limit, q -> 0). Anything at another scale is stated with its scale.

## Question
Is there a STRUCTURAL principle (a derived bound that saturates, with forced coefficients) that ties a gauge coupling to N (horizon dof), N_species, or the
horizon entropy? Separate honestly (i) inequalities, (ii) parametric relations (O(1) coefficient not derived), (iii) exact equalities.

## Literature actually read (abstract level only, via arXiv abstract pages; the papers themselves were NOT read)
* hep-th/0601001 (Arkani-Hamed, Motl, Nicolis, Vafa): the Weak Gravity Conjecture is an upper bound on gravity relative to gauge forces; it does not fix coupling values.
* 0706.2050 (Dvali): with N species the Planck mass is bounded below (M_P^2 >~ N Lambda^2), i.e. the gravity cutoff is M_* ~ M_P/sqrt(N).
* 1712.01868 (Heidenreich, Reece, Rudelius): magnetic cutoff e M_P (reduced-Planck, G^-1/2); gauge couplings "emerge" by integrating out charged towers up to the species/
  gravity scale; the coincidence is PARAMETRIC (their word).

## Principles analysed (fixed list; nothing added after the runs)
P1 electric WGC, m <= sqrt(2) e q M_P (inequality; equality only for extremal black holes).
P2 magnetic WGC cutoff Lambda_WGC = e M_P together with the species scale Lambda_sp = M_P/sqrt(N) (both parametric).
P3 emergence: 1/e^2(Lambda) = 0 at Lambda = Lambda_sp, so 1/alpha(mu) = (2/(3 pi)) sum_i N_c q_i^2 ln(Lambda/m_i) (one-loop coefficient forced; Lambda and masses are inputs).
P4 holographic charge equalities: (a) extremal RN entropy S = pi alpha N_q^2; (b) maximal charge of an RN-dS black hole (ultracold triple root) N_max^2 = 1/(4 alpha x),
   x = Lambda G hbar/c^3; (c) the unit-charge extremal object.

## Checks, scored trials, and criteria (declared now)
C1 (script c1): 
 * C1a: electron vs electric WGC: report m_e/(sqrt2 e M_P). Criterion: SATURATED iff ratio within 1e-3 of 1. Expected: fails by ~22 orders.
 * C1b: the P2 equality Lambda_WGC = Lambda_sp gives N_sat = 1/e^2 (C1: e M_red = M_red/sqrt N), 1/(2e^2) (C2: sqrt2 e M_red = M_red/sqrt N), or 8 pi/e^2 = 2/alpha (C3: e M_red = M_Pl/sqrt N).
   Declared SM counts N in {28 (bosonic dof), 118 (all SM dof: 28 + 90), 126 (118 + 3 RH neutrinos (6) + graviton (2))}. 3 conventions x 3 counts = 9 scored trials.
   HIT iff N_sat within 1e-3 (relative) of the count. Expected: 0 hits. Also report the inequality margin (e M_red)/(M_red/sqrt N).
 * C1c: the O(1) convention ambiguity itself: N_sat spans 5.4 .. 274 across the three conventions. If the spread exceeds 1e-3 the principle has no forced coefficient (declared).
C2 (script c2):
 * C2a: independent check of the QED one-loop coefficient d(1/alpha)/d ln mu = -2/(3 pi) per unit charge^2 Dirac fermion (sympy integral of x(1-x) = 1/6 and mpmath check of the Feynman-parameter integral),
   and of the SM one-loop hypercharge and SU(2) coefficients b_Y = 41/6, b_2 = -19/6 by explicit field content (exact Fractions). MUTATE: coefficient 1/(3 pi) must FAIL.
 * C2b: hypercharge emergence: 1/alpha_Y(M_Z) predicted by 1/alpha_Y = (b_Y/(2 pi)) ln(Lambda/M_Z) at Lambda = M_red/sqrt N (N in the 3 counts) versus measured
   1/alpha_Y(M_Z) = cos^2 theta_W(MSbar)/alpha(M_Z) with alpha^-1(M_Z) = 127.930, sin^2 theta_W = 0.23122. Also report the Landau-pole scale of hypercharge. 3 scored trials (HIT within 1e-3: expected none).
 * C2c: toy QED emergence with the measured charged-fermion masses (PDG central values, declared list e, mu, tau, u, d, s, c, b, t, one loop, sharp thresholds) at Lambda = M_red/sqrt N, 3 counts:
   compare 1/alpha_toy to 137.036. 3 scored trials (HIT within 1e-3). Report only: the Lambda that would be required (not scored; a one-parameter solve can always hit).
 * C2d: precision bound: with Lambda known only up to a factor f (parametric species scale), delta(1/alpha) = (2/(3 pi)) sum N_c q^2 ln f. Report for f = 2. If delta/137 > 1e-3 the emergence principle cannot fix alpha to 1e-3 even in principle.
C3 (script c3): 
 * C3a: sympy: extremal RN entropy in Gaussian units S = pi Q^2/(hbar c) = pi alpha N^2 (checked symbolically). MUTATE: pi -> 2 pi must fail.
 * C3b: sympy: RN-dS triple-root conditions f = f' = f'' = 0 give Q_geo^2 = 1/(4 Lambda), so N_max^2 = 1/(4 alpha x). MUTATE: Q^2 = 1/(2 Lambda) must fail the triple-root residual.
 * C3c: numbers: x from (G, hbar, c, H0 = 67.4, Omega_L = 0.6847) as in AH5; N_max at alpha = 1/137.036; S_dS = 3 pi/x; ratio N_max/sqrt(S_dS); mass and horizon of a unit-charge extremal object (M/M_Pl = sqrt(alpha), S = pi alpha).
 * C3d: alpha-trading test: for alpha in a declared set {1/137.036, 1/100, 1/50, 1/10}, a consistent N_max exists in every case (the equality never rejects any alpha). Criterion for "principle constrains alpha": some alpha is rejected without an extra input.
   Declared expectation: NONE is rejected, so the holographic equalities trade alpha for a second undetermined count.
Total scored hit-tests: 1 + 9 + 3 + 3 = 16. Expected chance hits: tolerance 1e-3 relative on a log-uniform prior of width ln(1e3): 16 x 2e-3/ln(1e3) = 4.6e-3 (computed in the scripts).

## Declared expected outcome
No forced principle. WGC and species are inequalities (satisfied by wide margin), and the species scale carries no derived O(1) coefficient. Emergence is a genuine equality with a forced one-loop coefficient
but needs Lambda and the full mass spectrum (walled) and fails quantitatively for the SM spectrum. The holographic equalities are exact but convert alpha into another cosmic count.

## Not tested
Non-perturbative / string-theory realisations of emergence with its own tower; the Dvali-Gomez quantum-break-time of de Sitter with charged species; fermion-loop effects on the dS horizon; any derivation of the SM masses (walled).
kappa = 1/2 stays FITTED. No guessed log/power family is scored.

## Amendments
(none yet)

## Results (appended after the runs; no criterion was changed)
Scripts and outputs: c1_wgc_species_bounds.{py,out,_MUTATE.out}, c2_emergence_species.{py,out,_MUTATE.out}, c3_holographic_charge_equalities.{py,out,_MUTATE.out}. Real runs exit 0; every MUTATE run exits 1.
* C1a: electron/WGC ratio 4.9e-22 (not saturated; inequality); WGC alone gives alpha >= 1.8e-45. C1b: 0 hits of 9 (N_sat = 10.9, 5.45, 274 vs 28/118/126). C1c: N_sat spread 50x across conventions, so the species scale has no forced O(1) coefficient.
  Inequality e M_red >= M_red/sqrt(N) holds with margin 1.6-3.4 for the three counts (satisfied, not saturated).
* C2: coefficient checks pass (2/(3 pi); b_Y = 41/6; b_2 = -19/6). Hypercharge emergence at M_red/sqrt(N) predicts 1/alpha_Y(M_Z) ~ 38.5-39.3 vs measured 98.35 (factor 2.5); Landau pole 1.7e41 GeV = 7e22 M_red.
  Toy QED emergence with measured charged-fermion masses gives 1/alpha ~ 70.4-71.7 vs 137.036 (factor 1.9). 0 hits of 6. Required cutoff (report only) 2.4e34 GeV = 1e16 M_red. Factor-2 uncertainty in Lambda moves 1/alpha by 0.86 percent (> 1e-3).
* C3: S_ext = pi alpha N^2 and N_max^2 = 1/(4 alpha x) verified symbolically (x = 2.8485e-122, N_max = 3.47e61 at the physical alpha, N_max/sqrt(S_dS) = 1.907). Unit-charge extremal object: M = 0.0854 M_Pl, S = 0.0229 nats.
  Every alpha admits a consistent N_max: no constraint on alpha without an extra input fixing N_max.
* Total scored hit-tests 16 (1 + 9 + 6), hits 0, expected chance hits about 4.6e-3. No hit, no derivation.
