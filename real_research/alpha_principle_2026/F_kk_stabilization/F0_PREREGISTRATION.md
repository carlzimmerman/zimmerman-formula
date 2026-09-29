# F -- KK radion stabilization and the light-charged-particle problem (pre-registration)

Written 2026-09-28 BEFORE any of f1/f2/f3 was run. Starts from AH6 (alpha_n = 4 n^2 l_P^2/R^2, needs R = 23.4125 l_P for n = 1, electron obstruction m_e R c/hbar = 1e-21).
Units hbar = c = 1; l_P^2 = G_4; x = Lambda l_P^2 = 2.85e-122 (AH5); observed vacuum energy rho_L = Lambda/(8 pi G) so rho_L l_P^4 = x/(8 pi).
Target alpha = 1/137.035999177 (Thomson limit, mu -> 0). Any relation derived below is a TREE-LEVEL relation at the compactification scale; the scale question is scripted in f3 (S1).

## Literature actually read (abstract level only, via WebFetch)
* arXiv:hep-th/0205080 (Bousso, DeWolfe, Myers): most (A)dS_p x S^q flux solutions are perturbatively unstable, including all uncharged ones. => a radion-stable extremum is NOT a stable vacuum; f2 only tests the l=0 (radion) direction and says so.
* arXiv:2205.12293 (Montero, Vafa, Valenzuela): one extra dimension of size ~ Lambda^(-1/4) ~ 1e-6 m from swampland arguments. Used only as a cross-check on the size of the Casimir-stabilised circle in f1.
* arXiv:1509.06374 (Heidenreich, Reece, Rudelius): WGC under toroidal compactification, KK photons. Used only as context for the KK charge/mass relation.
Pre-arXiv sources (Appelquist-Chodos 1983 circle+Casimir; Randjbar-Daemi-Salam-Strathdee 1983 S^2 flux; Salam-Sezgin 1984; Hosotani 1983; Witten 1981/83 chirality) are NOT re-read here; wherever they are mentioned in the report they are labelled RECALLED, and every number is instead re-derived by script.

## Part 1 -- can R/l_P = 23.41 be FORCED?  Three families, declared list (3 families)

### Family A: 5D on S^1, Casimir energy + 5D cosmological energy rho_5 (Appelquist-Chodos type)
* A1  Casimir energy per 4D volume of one periodic real dof, E = -3 zeta(5)/(64 pi^6 R^4); verify by heat-kernel/Poisson numerically (twisted dof: cos(2 pi k a) inside the k-sum).
* A2  Weyl-rescale to the 4D Einstein frame; V_E(R) = (R0/R)^2 [2 pi R rho_5 + E(R)]. Extremum, value, second derivative, sign theorem.
* A3  Impose the observed vacuum energy V(R*) = x/(8 pi) l_P^-4 as a second equation; R*/l_P as a function of x and the integer dof count DN.  Declared DN list (5 trials): DN in {+5 (5D graviton polarizations), -4 (one 5D Dirac), -8, -16, -100}.
* A4  alpha_grav = 4 l_P^2/R*^2 as a function of x (power law?), compared with the exponent p = 0.01758 that AH5 said a pure power alpha = x^p would need.
PASS (a forced R): there is a minimum with V > 0 (dS) and |R*/l_P - 23.4125| < 1e-3 * 23.4125 for some declared DN.  Expected in advance: FAIL -- the only extremum with V>0 is a maximum, the minimum has V<0, and R*/l_P ~ (40 pi |c|/x)^(1/4) ~ 1e30, alpha_grav ~ x^(1/2) ~ 1e-61.

### Family B: Freund-Rubin M_4 x S^n with (n-1)-form gauge potential, integer flux N through S^n, D-dim cosmological term Lambda_D, action R/(2 kappa^2) - Lambda_D/kappa^2 - F^2/(2 g^2 n!)  (F quantised: oint F = 2 pi N for a unit-charge (n-2)-brane).
* B1  V_E(R) for general n (sympy); independent cross-check against the D-dim Einstein equations for n = 2 (curvature = stress), which must agree; MUTATE flips a sign.
* B2  n = 2 in closed form: extremum, stability of the radion (V''), Minkowski condition, AdS/dS classification, exact R* including the x-dependence, envelope dV_min/dLambda_6 and the tuning needed to hold V = x/(8 pi).
* B3  which dimensionless numbers are left free: the ratio chat = g_6^2/kappa_6 (n = 2). Report R*/l_P and the 4D couplings as functions of (N, chat) only.
* B4  inverse map, NOT a hit test: the chat that would give alpha = 1/137.036 for N = 1..4, reported as a requirement.  Declared handle check (36 trials = 9 handles x N = 1..4): chat in {1/(4 pi), 1/(2 pi), 1/pi, 1/2, 1, 2, pi, 2 pi, 4 pi}; hit = alpha within 1e-3.  Expected chance hits computed in the script (formula: trials x 2e-3 / ln span).
PASS (forced): R*/l_P (or alpha) follows from N, Lambda (through x) and integers ALONE, with no free continuous parameter.  Expected in advance: FAIL -- chat = g_6^2/kappa_6 is a free continuous 6D ratio; alpha = (chat/(2 pi N))^2 at the Minkowski point.

### Family C (no computation, structural): a circle with a 1-form flux does not exist (no 2-cycle); so n = 1 cannot be flux-stabilised, only n >= 2.  Stated, and covered by B1 for n = 2, 3.

Trial count for Part 1: 3 families; 5 (A3) + 36 (B4 handles) numerical trials; all other items are derivations, not hit searches.

## Part 2 -- the light charged particle problem (f3)  declared variants (7)
V1 pure KK momentum mode (also with bulk mass);  V2 Scherk-Schwarz / Wilson-line twist beta of the graviphoton charge;  V3 S^1/Z_2 orbifold (chirality);  V4 5D matter with its own U(1) (mixed with graviphoton);
V5 Hosotani / Wilson-line potential for the twist;  V6 S^2 flux background with chiral zero modes (isometry SU(2) + 6D U(1));  V7 running: which alpha and at which scale the KK relation can apply.
Checks (each scripted):
* T1 every graviphoton-charged mode has z = q/(e_0 m R) <= 1 (bulk mass, twist included); the electron has z_e = e/(sqrt(16 pi G) m_e) ~ 1e21.  PASS(no-go) if z <= 1 identically and z_e >> 1.
* T2 sympy: pull-back of g_{mu w} under w -> -w flips sign (graviphoton is projected out on S^1/Z_2).
* T3 Hosotani potential minima for integer species counts: positions and light-mode masses.
* T4 S^2 with flux: SU(2) and 6D-U(1) couplings derived from the reduction (sympy Ricci scalar of the fibration + Maxwell reduction); zero-mode count |N| from the spin-weighted-harmonic spectrum (formula recalled, algebra checked).
* T5 one-loop Standard-Model running of alpha^-1 from Thomson to M_KK ~ 5e17 GeV (order-of-magnitude, uses PDG inputs at M_Z, labelled external).
Criterion for "a variant delivers a light charged particle whose charge is tied to R and G with no free parameter": (i) a charged state with m << 1/R exists, (ii) its charge is a computed function of R/l_P (and integers) with no free coupling, (iii) that function needs no continuous parameter beyond R/l_P itself, (iv) R/l_P is then fixed by integers/x.  (i)-(iii) may pass for V6, (iv) is expected to fail everywhere.

## MUTATE controls (each script has --mutate, must exit 1)
f1: drop the Einstein-frame factor (R0/R)^2 (must break the extremum-value identity V_min = 5c/R^4);  f2: flip the sign of the curvature term (must break the agreement with the Einstein-equation cross-check);  f3: drop the flux contribution to 1/g_SU2^2 or use the wrong twist bound (must break the Minkowski coupling identity / z<=1 check).

## Overall pass/fail (declared now)
The route "yields a forced principle that fixes alpha" only if Part 1 PASSes (forced R with dS vacuum) AND some Part-2 variant satisfies (i)-(iv) with the Thomson-scale statement made.  Expected outcome: no.  KK/flux trades alpha for a radion vev (or for chat); stabilisation fixes R only through additional free constants or R ~ x^(-1/4); the only light charged states with geometric charge come from V6 and there alpha becomes (chat/(2 pi N))^2.

## Scope / not tested
Casimir energy on S^2, higher loops, backreaction of branes, SUSY completions (Salam-Sezgin-type could fix chat; RECALLED, not tested), stability beyond the radion (hep-th/0205080 says most fluxed dS_p x S^q are unstable), the SM mass sector (walled), kappa = 1/2 (FITTED).
Amendments are appended below, never edited above.

## Amendment 1 (appended after the runs; nothing above was edited)
* Hand-derivation slips caught by the scripts, corrected in the scripts (no criterion changed): (a) I had written the Minkowski value Lambda_6 = 1/(2 kappa^2 R^2); the dimensionally correct value is 1/(2 R^2) (Lambda_6 enters U as Lambda/kappa^2); f2 B2b tests the corrected form. (b) I had estimated the Lambda_6 tuning as ~1e-113 at R = 23 l_P; the exact envelope result is delta Lambda_6/Lambda_c = 2 (R/l_P)^2 x = 3.1e-119 (f2 B2e/B2f, checked against a 400-digit exact solve).
* The pre-run text in the f3 verdict guessed alpha^-1(M_KK) ~ 115-125; the script's one-loop SM number is 106.8 (f3 T5). The check (>10% off 137.036) is unaffected. That number is order-of-magnitude only (1-loop, no KK thresholds).
* MUTATE control of f2 was first written so that the sign flip entered both the potential and the Einstein equations (which would have kept them consistent); corrected to mutate the potential only. First f1 mutate run crashed (positive-symbol assumption) instead of failing checks; fixed and re-run.
* T3 (Hosotani census) is a descriptive census over 288 integer weight pairs, not a hit search; T3b/T3c say so.
