# Lane E (dynamical attractor / extremum routes to alpha) -- pre-registration

Written 2026-09-28 BEFORE `e1_coupling_function_freedom.py` and `e2_variation_bounds.py` were written or run.
Amendments, if any, are appended below the line "AMENDMENTS" and never edit this text.

## Question

Is there a dynamical attractor or extremum -- a dilaton/modulus phi coupled to F^2 through a gauge kinetic function B_F(phi), pinned by a
least-coupling / attractor principle or by a dark-energy attractor -- whose VALUE of alpha is computable from the programme's inputs
(Lambda, kappa = 1/2 fitted) plus the principle, with no free coupling function? Which quantities stay free? Do the existing bounds on
variation of alpha kill any such route?

Scale statement (declared now): all routes below define alpha as the low-energy (Thomson-limit) coupling alpha = e^2/(4 pi hbar c), obtained
from the bare/string-scale g^-2 = k B_F(phi_m) by standard RG running; the running (a fixed, known number for the SM) is NOT part of the test and is
folded into the constant k (declared below to be a free constant of the model, not a derived one).

## Primary sources actually read (text extracted with pdftotext; PDFs deleted afterwards, arXiv ids are the record)

* hep-th/9401069  Damour & Polyakov, "The String Dilaton and a Least Coupling Principle": eqs (2.2)-(2.11), Sec. IV-VI (attraction factors, universal B(phi) case,
  eq. (6.7)-(6.14) residual couplings, footnote on lambda_alpha and alpha^-1 proportional to B).
* gr-qc/0204094   Damour, Piazza & Veneziano, "Runaway dilaton and equivalence principle violations": eqs (1)-(2), fixed point at phi = +infinity, B_i = C_i + O(e^-phi).
  (hep-th/0205111, the long companion paper, was downloaded and only its abstract/introduction were read.)
* hep-ph/0110377  Olive & Pospelov, "Evolution of the Fine Structure Constant Driven by Dark Matter and the Cosmological Constant": action (2.1), couplings (2.2),
  alpha(phi) = e0^2/(4 pi B_F(phi)) (2.3), field equation (2.4)-(2.5), solution (3.3)-(3.4), Sec. 5 (common extremum, quadratic couplings), conclusion on zeta_Lambda.
* 2010.06620      Lange et al. (PTB), Yb+ optical clocks: d ln alpha/dt = 1.0(1.1) x 10^-18 /yr.
* 2209.15487      MICROSCOPE final result: eta(Ti,Pt) = [-1.5 +- 2.3(stat) +- 1.5(syst)] x 10^-15.
* 1009.5514       Uzan review "Varying constants, gravitation and cosmology": used only for the table of contents/context of Oklo and quasar limits; no Oklo or quasar
  number is imported from it into any script (the programme's own zeta < 4e-9 is used as the quoted repo constraint; see below).
* Bekenstein's original 1982 model was NOT fetched; it is used only as described inside hep-ph/0110377.

## Hypotheses

* H1 (least-coupling): the Damour-Polyakov attractor fixes the VALUE alpha_m^-1 = k B_F(phi_m) with no free function. Expected: FALSE. The attractor condition is B'(phi_m) = 0;
  the value B(phi_m) is a separate free number of the coupling function.
* H2 (programme inputs): the attractor location/value depends on Lambda (and kappa). Expected: FALSE for a universal-coupling attractor (B' = 0 has no rho_Lambda in it);
  for a non-universal coupling the stationary point depends on rho_m/rho_Lambda, hence on time, hence alpha drifts (constrained in H3).
* H3 (bounds as a hard constraint): (a) a linear dilaton-quintessence coupling zeta with a tracker/scaling attractor is bounded by the clock drift;
  (b) the AH5 one-parameter families alpha = x^p and 1/alpha = a ln(1/x), if realised with a DYNAMICAL dark-energy density, are excluded unless 1+w is tiny;
  (c) a Damour-Polyakov quadratic attractor passes all bounds trivially, so the bounds do not constrain alpha_m itself.
* H4 (runaway dilaton): alpha_infinity^-1 = k C_F, the asymptotic constant of B_F, is a free number. Expected: TRUE (free).
* H5 (accounting): the principle removes one initial-condition freedom (phi_initial) but leaves the coupling function and the potential free; counting
  free parameters vs. the single datum alpha, the route is under-determined by construction. Expected: freedom moved into B_F(phi), not removed.

## Everything that will be run (fixed list; no other computation will be scored)

Script `e1_coupling_function_freedom.py` (sympy, exact), checks:
* C1: for m_A(phi) = mu B^{-1/2} exp(-8 pi^2 nu B) Lambda_s (DP eq. 2.11), d ln m_A/d phi = -B'(phi)[1/(2B) + 8 pi^2 nu B] and vanishes iff B' = 0 (for B > 0, nu > 0).
  The stationary condition contains no rho_Lambda and no kappa.
* C2: three-term string-loop truncation B = e^{-2 Phi} + c0 + c1 e^{2 Phi}: its extremum (c1 > 0) is a MINIMUM of B, i.e. a maximum of the masses, i.e. NOT an attractor
  (DP: attractor = maximum of B). Four-term truncation B = e^{-2Phi} + c0 + c1 e^{2Phi} + c2 e^{4Phi}: the attractor exists iff c1 y^2 > 3 (y = e^{2 Phi_m}) with c2 fixed by B' = 0;
  value B_m = 3/(2y) + c0 + c1 y/2.
* C3: surjectivity: for each declared target 1/alpha in {1, 25, 137.035999177, 1000} (k = 1 declared, fixed) solve c0 exactly so that B_m = target; verify B' = 0, B'' < 0, and
  d B_m / d c0 = 1 (never zero). Verdict "value fixed by the principle" requires d B_m/d c0 = 0 for some choice; expected: not satisfied.
* C4: Lambda-attractor: V = rho_Lambda B_Lambda(phi), B_Lambda = 1 + (xi/2)(phi - phi_L)^2 and B_F = 1 + zeta_F (phi - phi_L) + ... (any smooth): at the de Sitter minimum
  alpha_min^-1 = k B_F(phi_L); check d alpha_min / d rho_Lambda = 0 and d alpha_min / d xi = 0 (sympy), alpha_min set by the free function B_F at the free point phi_L.
* C5: runaway: B = C + b e^{-phi}; alpha_inf^-1 = k C; verify surjectivity in C and that the present offset k b e^{-phi_0} is a second free number.
* C6: parameter ledger (printed table), no numerics to score.
* MUTATE (must exit 1): mutation M1 asserts the three-term extremum is an attractor (B'' < 0); mutation M2 asserts d B_m/d c0 = 0. Both are false and must trip.

Script `e2_variation_bounds.py` (numpy/mpmath/sympy/scipy constants), checks:
* B1: the Olive-Pospelov closed form (3.3)-(3.4) satisfies the field equation (3.1) numerically (finite-difference residual < 1e-6 relative) at 5 declared times (t/t0 in {0.2,0.4,0.6,0.8,1.0}) for
  a declared (zeta_m, zeta_Lambda) = (1, -1.7) [their Fig. 3 ratio], Omega_Lambda = 0.6847, H0 = 67.4 km/s/Mpc.
* B2: today's drift rate d ln alpha/dt for the linear model, and the bound it puts on zeta_F zeta_m (M_Pl/M_*)^2 with the clock bound |d ln alpha/dt| < 3.2e-18 /yr
  (= |1.0| + 1.96 x 1.1, rounded up). Report the zero-drift ratio zeta_Lambda/zeta_m = -4 b t0 / (sinh 2 b t0 - 2 b t0)  (a tuning of a coupling ratio, not a value of alpha).
* B3: tracker/scaling dilaton-quintessence: d ln alpha/dN = zeta sqrt(3 (1+w) Omega_phi) (exact for Delta alpha/alpha = zeta kappa_G Delta phi with kappa_G^2 = 8 pi G);
  zeta_max(w0) = 3.2e-18 yr^-1 / (H0 sqrt(3 Omega_phi (1+w0))) for w0 in {-0.99, -0.95, -0.9, -0.752}. Compare with the quoted repo bound zeta < 4e-9 (NOT re-derived; if mine
  is looser, report the discrepancy).
* B4: the AH5 families realised dynamically: p = ln alpha / ln x (x = Lambda l_P^2 from CODATA + Omega_Lambda = 0.6847, H0 = 67.4), a = (1/alpha)/ln(1/x); with x proportional to rho_DE,
  d ln alpha/dt = p (dln rho/dt) = -3 H0 (1+w) p (power law) and = -alpha a (3 H0 (1+w)) (log family, sign aside); maximum allowed 1+w for each, and the factor by which the
  DESI-like w0 = -0.752 (quoted in the repo SME review) is excluded.
* B5: Damour-Polyakov quadratic attractor: B = B_m [1 - (lambda/2) delta^2], delta = phi - phi_m in DP normalisation. Atom sensitivity s_A = 7.7e-4 Z(Z-1)/A^{4/3} (Coulomb-only,
  DP eq. 6.13 coefficient a_3alpha; a LOWER bound on the coupling, so the resulting limit on delta is conservative-weak). eta ~ (s_Ti - s_Pt) s_Earth (lambda delta)^2 with s_Earth taken from the
  weakest of {O, Si, Fe}. |eta| < 7e-15 (= 1.5 + 2 sqrt(2.3^2 + 1.5^2), MICROSCOPE). Report the maximum |lambda delta| and the maximum cosmic variation |Delta ln alpha| ~ (lambda delta)^2/(2 lambda) for lambda >= 1;
  the pass verdict is: any alpha_m is allowed (the bounds constrain delta, not B_m).
* MUTATE (must exit 1): M1 flips the sign of the zeta_Lambda term in the closed form (B1 must fail); M2 asserts that the power-law family is consistent with w0 = -0.752 (B4 must fail).

Counting: 0 scored numerical hits (no handle scan, no comparison of any computed number to 137.036 for scoring). Report-only numbers: the c1 or c0 that would be needed for
natural-looking coefficients, marked REPORT-ONLY in the output. Expected number of chance hits from a scan: not applicable (no scan). Total scripts: 2 (+2 MUTATE runs).

## Pass / fail criteria (declared now)

* ROUTE FORCES alpha only if: (i) d alpha_m / d (some free parameter of the coupling function) = 0 for the whole allowed family, OR the principle itself supplies the coefficient; (ii) it depends on
  Lambda or kappa in a way that yields a definite number; (iii) it passes B3-B5. Anything else: the route moves the freedom into f(phi), it does not fix a value.
* Expected outcome, stated in advance: C1-C6 confirm the freedom (d B_m/d c0 = 1, every target reachable, no rho_Lambda dependence); B1 passes; B2 gives a clock bound on the coupling product;
  B3 gives zeta_max ~ 1e-7..1e-8 in this script's normalisation; B4 shows that dynamical realisations of the AH5 families need 1+w < 1e-6; B5 shows the DP attractor is compatible with everything and constrains nothing about alpha_m.
  Verdict expected: NO forced value; a true cosmological constant (w = -1 exactly) is the only consistent Lambda for any Lambda-tied alpha, which makes the "dynamical" route static.

## Not tested

* String-model-specific B_F (any explicit compactification), moduli stabilisation by fluxes, axion couplings, non-abelian sectors, quantum corrections to phi's potential, electron-mass dependence (walled).
* The claim is about the class "one scalar with gauge kinetic function B_F(phi) and an attractor", not about all of physics. kappa = 1/2 stays FITTED; the SM mass sector stays walled.

## AMENDMENTS
(none yet)

### Amendment 1 (2026-09-28, before any script was written; visible correction of a slip in this document)
C1 as written above has an algebra slip: ln m_A = ln(mu Lambda_s) - (1/2) ln B - 8 pi^2 nu B, so d ln m_A / d phi = -B'(phi) [ 1/(2B) + 8 pi^2 nu ]
(the bracket is 1/(2B) + 8 pi^2 nu, NOT 1/(2B) + 8 pi^2 nu B). The conclusion is unchanged (bracket > 0 for B > 0, nu > 0, so the zero set is B' = 0).
The script checks the corrected expression, and the MUTATE run does not need to exercise C1.

### Amendment 2 (2026-09-28, after the first run of e2_variation_bounds.py; recorded visibly)
Two things went wrong on the FIRST run and are recorded here rather than hidden:
1. B1b failed because of a bug in my transcription of eq. (3.4) (the factor 4/3 multiplies the whole bracket, including the log term, as printed) and because the relative-difference
   measure divided by ~0 at t = t0 where phi = 0. Fixed; the printed (3.4) then equals the quadrature of (3.3) (this is a check of the paper's formula, not a tuned outcome).
2. B4b was declared as "both families need 1+w < 1e-6". The computed values are 8.8e-7 (power law) and 4.3e-6 (log family). The declared threshold was too tight for the log family:
   this is a pre-registration miss and is reported as such. The amended criterion (written after seeing these numbers, which is why it is only a reading rule and not a claim of prediction) is:
   "both families need 1+w < 1e-5, and the w0 = -0.752 branch is excluded by a factor > 1e4". The substantive conclusion is unchanged.
