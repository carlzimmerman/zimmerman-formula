# N5 -- charged fermions in dS_2: the induced current, the massless (Schwinger-model) limit, and whether a horizon tie can force a coupling (pre-registration)

Written 2026-09-28 BEFORE any script in this directory was run (the only work done before writing this file was reading the literature and
deriving the expected structure by hand; no code has been executed).  Follows AH1-AH2 (scalar) and the red team's branch 5.

## The question

Every horizon-response result so far is for a charged scalar.  Red-team branch 5: does the induced current / conductivity of a charged Dirac
fermion in dS_2 in a constant electric field depend on the coupling only through lambda = eE/H^2 and a mass function, exactly as for the scalar
(sigma/H = (e^2/H^2) g(mu))?  Three sub-questions:
(i)   does sigma/H factor as (coupling)^2 x g_f(mu) with g_f mass-dependent (so no tie fixes the coupling)?
(ii)  how does g_f(mu) differ from the scalar g(mu) = 2 rho/sinh(2 pi rho) at large mu and at mu -> 0 (anomaly / exactly solvable limit)?
(iii) is there a special value of the coupling (e.g. from the exact Schwinger-model photon mass e^2/pi against H) that a horizon tie could force?

**2D-toy caveat (binding on every statement below):** in 2D the charge e has mass dimension 1, so e^2/H^2 is NOT the 4D fine-structure constant.
Nothing here is a statement about alpha; it is a statement about how a coupling enters a horizon-scale response in a toy model.  dS_4 fermions and
4D charge renormalization (the ln(mu_R/H) of AH4) are NOT computed here.

## Sources (read status stated honestly)

* Stahl, Strobel, Xue, arXiv:1507.01686 (PRD 93, 025004): FULL TEXT read (pdftotext).  Dirac equation in dS_2 (their eqs. 18-19, 21-22), Whittaker modes
  (63)-(64), Bogoliubov coefficients (72)-(73), adiabatic subtraction (94)-(95), regularized current (96), limits (97)-(103), bosonic comparison (104).
  Their (96): J_reg = (eH/pi) mu sinh(2 pi lambda)/sin(2 pi mu) with mu = i sqrt(gamma^2 + lambda^2), i.e. **J/(eH) = (1/pi) rho_f sinh(2 pi lambda)/sinh(2 pi rho_f),
  rho_f = sqrt(mu^2 + lambda^2)** in this lane's variables (mu = m/H).  They state the bosonic case is the same with rho_s = sqrt(mu^2 + lambda^2 - 1/4).
  (Their text at Sec. III.E.3 writes the bosonic sigma with a "+1/4" under the root; the shift by 1/4 in the *scalar* variable is the one in AH2/Frob et al.)
  The formula is a COMPARATOR to be validated by the direct sum, not assumed.
* Anninos, Anous, Rios Fukelman, arXiv:2403.16166 (v5): abstract, introduction, Secs. 2, 3 (exact solution, E-field two-point function, Delta(1-Delta) = q^2 l^2/pi,
  eq. 3.6) and the Outlook read in full; Sec. 4 (fermion two-point function) and the appendices skimmed only.  Euclidean S^2 (Hartle-Hawking state) treatment of the
  massless Schwinger model; the gauge-invariant electric-field correlator is that of a scalar of mass^2 = q^2/pi.
* Stahl, Xue, arXiv:1603.07166: FULL TEXT read.  Backreaction of the dS_2 fermion current in a *local constant-field approximation*; numerics only (I do not reproduce them).
* Hayashinaka, Fujita, Yokoyama, arXiv:1603.04165 (dS_4 fermions): ABSTRACT ONLY (fetched summary).  Used only to say what the dS_4 fermion paper reports (negative current
  below a mass-dependent field, no infrared hyperconductivity); nothing in this lane depends on it.
* Frob et al. arXiv:1401.4137 (scalar dS_2 comparator): as in AH2 (already in the record); the scalar closed form is reused from AH2, not re-derived.
* Recalled, not read (NOT used as evidence): Jayewardena (1988) exact Schwinger model on S^2; Haouat-Chekireb dS_2 fermion pair creation (cited via Stahl et al.).

## Variables and conventions

hbar = c = H = 1; planar patch ds^2 = a^2 (d tau^2 - dx^2), a = -1/tau; evaluate at tau = -1 (a = 1).  Constant field: eA_x = lambda/tau (so p(tau) = k + lambda/tau, the
kinetic momentum).  lambda = eE/H^2, mu = m/H, rho_f = sqrt(mu^2 + lambda^2), rho_s = sqrt(mu^2 + lambda^2 - 1/4) (scalar; imaginary branch as in AH2).
Weyl basis gamma^0 = sigma_x, gamma^1 = [[0,1],[-1,0]].  Rescaled spinor Psi = sqrt(a) psi obeys the flat Dirac system
  i Psi_1' = -p Psi_1 + m a Psi_2,   i Psi_2' = +p Psi_2 + m a Psi_1,   |Psi_1|^2 + |Psi_2|^2 = 1 (conserved).
Positive-frequency "in" mode = the eigenvector of H(tau) = [[-p, m a],[m a, p]] with eigenvalue +omega at tau -> -infinity.
Current: J^x/e = -(1/2 pi) Int dk (|Psi_1|^2 - |Psi_2|^2) at a = 1, symmetric in k, minus the exactly integrated zeroth-order adiabatic (equivalently heavy-field / Pauli-Villars-type)
subtraction Int dk (-p/omega) = -2 lambda/tau, i.e. J/(eH) = lambda/pi - I_raw/(2 pi) with I_raw = Int_0^inf [f(k,lambda) - f(k,-lambda)] dk,
f = |Psi_1|^2 - |Psi_2|^2 of the positive-frequency k>0 mode (the k<0 modes follow from the component swap Psi_1 <-> Psi_2 with p -> -p, which I VERIFY independently by
direct ODE integration, not assume).  The subtraction is done as AH2 does it: raw integrand integrated, Delta subtracted exactly, log-spaced Gauss-Legendre quadrature,
fitted large-k tail (fit form c2/k^2 + c3/k^3 + c4/k^4, three-point fit at K/2, 3K/4, K), IR cutoff k0 = 1e-40 (the AH2 amendment-1 lesson, pre-applied).

## Hypotheses (all stated so they can be false)

* H1 (structure): J/(eH) = F(lambda, mu) depends on e only through lambda and an overall factor e, so sigma/H = (e^2/H^2) g_f(mu) with g_f(mu) = lim_{lambda->0} F/lambda = 2 mu/sinh(2 pi mu).
* H2 (massless limit): g_f(0) = 1/pi EXACTLY and F(lambda, 0) = lambda/pi exactly linear for every lambda (chirality decouples, no mixing; the entire current is the spectral-flow /
  ABJ anomaly, with I_raw = 0); n_k = theta(k lambda) exactly (pair production probability 1 in the screening direction, 0 in the anti-screening direction).
* H3 (difference from the scalar): g_f(mu) < g_s(mu) for every mu; g_f is finite at mu -> 0 (no infrared hyper-conductivity; g_s -> 1/(2 pi mu^2)); at large mu both are
  ~ 4 mu e^{-2 pi mu} and g_f/g_s -> exp(-pi/(4 mu)) -> 1.
* H4 (Schwinger-model limit): the exact massless dS_2 Schwinger model is a damped plasma oscillator: with the memory relation J' + H J = (e^2/pi) E (derived from H2) and E' = -J,
  homogeneous E obeys E'' + H E' + (e^2/pi) E = 0 (cosmic time), i.e. E'' + (e^2/pi) a^2 E = 0 (conformal time) = a scalar of mass^2 = e^2/pi; exponents s = H Delta with
  Delta(1 - Delta) = e^2/(pi H^2), matching Anninos et al. eq. (3.6).  The constant-E response J = e^2 E/(pi H) is the particular solution of that relation.
* H5 (no forced coupling): the exact model exists, is unitary and dS-invariant for every x = e^2/(pi H^2) > 0; the special points on the family (critical damping x = 1/4 i.e.
  e^2/H^2 = pi/4; linear-response rate equal to H, x = 1) are thresholds in a continuous family, not selected points; a conductivity tie sigma/H = c fixes e^2/H^2 = pi c ONLY if the
  fermion is declared exactly massless AND c is supplied from outside; for any massive fermion the required e^2/H^2 = c/g_f(mu) varies over many decades.  Expected verdict: NO tie forces the coupling.

## Pass / fail criteria (declared now)

Script 1  `n5_1_dirac_modes_and_pairs.py`
* D1 sympy reduces the curved-space Dirac equation (tetrad e^a_mu = a delta, spin connection computed from the tetrad) with psi = a^{-1/2} Psi to the flat system above (residual identically 0).
* M1 the Whittaker modes psi_1 ~ W_{kappa - 1/2, i rho_f}(2 i k tau), psi_2 ~ c W_{kappa + 1/2, i rho_f}(2 i k tau), kappa = -i lambda, satisfy the first-order system (c FOUND from the system, then
  the second row checked): residual <= 1e-12 (relative) at six (k, lambda, mu, tau) points.
* M2 unit norm |Psi_1|^2 + |Psi_2|^2 constant in tau (spread <= 1e-12 over five times).
* M3 independent numerical integration of the ODE from tau_0 = -4000/|k| (first-order adiabatic eigenvector initial condition), including k < 0, reproduces f = |Psi_1|^2 - |Psi_2|^2 at tau = -1
  of the Whittaker construction to <= 1e-4 (absolute) at six (k, lambda, mu) triples (three with k < 0).  This is what validates the Bunch-Davies choice and the k<0 mapping.
* P1 Bogoliubov |beta_k|^2 by projection onto out-modes (constructed from M-Whittaker functions, orthonormality checked) equals Stahl et al. eq. (73) to <= 1e-6 relative at six triples, both signs of r = sgn(k).
* P2 massless limit: at mu = 1e-3, n_k >= 0.99 for k lambda > 0 and <= 0.01 for k lambda < 0 at lambda = 1 (step function).
* MUTATE control (`--mutate`): the scalar index rho_s replaces rho_f in the mode construction (the "1/4" error); M1 must FAIL.

Script 2  `n5_2_induced_current.py`
* V1 direct current = closed form, worst relative difference <= 2e-3 over the declared grid, one consistent overall sign.  Grid (lambda, mu): (0.30,0.90) (0.60,0.60) (1.00,0.30)
  (1.50,1.00) (2.00,1.50) (0.10,0.30) (0.20,0.10) (0.35,2.00) (0.50,0.50) (0.40,0.05); ten points.
* V2 massless limit: with the exact massless modes verified numerically to have no mixing (|Psi_2| = 1 for k>0, |Psi_1| = 1 for k<0 to <= 1e-10 by ODE), I_raw = 0 and J/(eH) = lambda/pi at
  lambda in {0.15, 0.4, 0.8, 1.6}; plus the direct sum at mu = 0.05, lambda = 0.4 stays within its closed form (in the V1 grid).
* V3 J odd in lambda (direct, +-0.6 at mu = 0.7), 2e-3.
* V4 heavy fields: direct mu = 3, lambda = 0.3 within 2e-3 at K = 1280 (K convergence table printed); closed-form small-lambda slope over 4 mu e^{-2 pi mu} -> 1 within 3% at mu = 40.
* V5 linear conductivity table g_f(mu) (mu in {0, 0.05, 0.1, 0.3, 0.5, 1, 2, 5}) and g_s(mu); test H3: g_f < g_s at all tabulated mu >= 0.05; g_f(0.05) within 1% of 1/pi; ratio g_f/g_s vs exp(-pi/(4 mu)) at mu = 5, 10, 20 within 5%.
* V6 ties (same declared six c as AH2: kappa, kappa/pi, 1/(2 pi), 1/pi, 1, 2 kappa; kappa = 1/2 FITTED): required e^2/H^2 = c/g_f(mu) at mu in {0.3, 0.5, 1, 2, 5}: a coupling is DETERMINED by a tie only if the
  spread over those five mass classes is < 2 (declared).  Expected: no.  Also report the massless value e^2/H^2 = pi c and label it "conditional on m = 0 exactly and c supplied externally".
* Electron-mass reading (2D-toy statement): ln g_f(mu_e) at mu_e = m_e/H_0 (same constants as AH2).
* MUTATE control (`--mutate`): the subtraction Delta is dropped; V1 must FAIL.

Script 3  `n5_3_schwinger_model_ds2.py`
* S1 (sympy) derive the homogeneous Maxwell equation in dS_2 from the action, insert J = (e^2/pi) A/a (the massless result of script 2 in temporal gauge) and show E'' + (e^2/pi) a^2 E = 0; show the
  cosmic-time form E'' + H E' + (e^2/pi) E = 0 and s = H/2 +- sqrt(H^2/4 - e^2/pi).
* S2 the linear conductivity of script 2 at mu = 0 equals the coefficient in S1: sigma0 = 1/pi computed from the mode sum (I_raw = 0, Delta = 2 lambda), and the constant-E current is the exact particular solution.
  (This is the check the MUTATE control breaks.)
* S3 numerical integration of E'' + (e^2/pi) a^2 E = 0 from tau = -T to late times: the fitted late-time exponent E ~ (-tau)^Delta agrees with Delta(1-Delta) = x, x = e^2/(pi H^2) in {0.05, 0.15, 0.24} within 1e-3
  (real Delta); for x = 0.6, 1.5 the envelope ~ (-tau)^{1/2} and the oscillation frequency = sqrt(x - 1/4) in ln(-tau) within 1e-3.
* S4 compare the exact decay exponent with the naive local-response rate x: report (Delta - x)/x at x = 0.01, 0.1, 0.24; the local-constant-field model (J = e^2 E/(pi H) at every time, as in Stahl-Xue
  1603.07166 at mu = 0) gives a monotone exponential decay for all x, the exact solution oscillates for x > 1/4: declared qualitative difference to be reported, no threshold.
* S5 the special-value table (declared, nine candidates, nothing added later): critical damping x = 1/4; linear-response rate = H (x = 1); the six conductivity ties x = c (c as in V6); plus the instanton-weight
  scale e^{-1/(2x)} = e^{-1} (x = 1/2).  For each: e^2/H^2 = pi x and whether the exact model treats it as special.  Test of H5: the sphere two-point-function coefficients of Anninos et al. eq. (3.3), q^2 l^2 / [L(L+1)(L(L+1) + x)]
  (with x = q^2 l^2/pi, i.e. the mass^2 of the scalar in units of H^2, q^2 l^2 = pi x), are positive for all L >= 1 on a scan x in [1e-3, 1e3] (the exact model is well defined at every coupling), so no coupling is excluded and none isolated.
* MUTATE control (`--mutate`): the subtraction is dropped (Delta = 0), giving sigma0 = 0 and no screening; S2 must FAIL.

Mutation invocation for ALL three scripts: **`--mutate`** (not positional).  Each real run exits 0; each control exits 1 (script 1, 3) or 0-on-failure-as-required (script 2 follows the AH2 pattern:
exit 0 when the targeted check fails as required); the docstring of each script states this.

## The bar

No numerical match to 1/137.036 is claimed or sought here.  Any later attempt to map e^2/H^2 (or x) to alpha would have to clear lane D's bar (P < 1e-3 after look-elsewhere, miss <= 5e-10, zero fitted reals,
scale stated); none of the nine candidates is a number with an alpha-scale attached, and the map fails the dimensional obstruction (AH5) in any case.

## Reading rules

* Failing to find a forcing tie is the expected outcome and is reported as such; a pass of V1-V4 says the current is computed correctly and says nothing in favour of any alpha.
* kappa = 1/2 stays FITTED; the SM mass sector is walled; nothing is cited from the do-not-cite list.
* The exactly solvable point (m = 0) is where a horizon tie would be sharpest; if it fails to select a coupling there, it cannot do so for massive charged fields.
* Everything in scripts is committed-verifiable in the sense of the repo rules (no commit is made by this lane).

## Count of everything that will be run

3 scripts x (1 real run + 1 mutate run) = 6 runs, plus any re-runs after a disclosed amendment (each recorded below).

## Amendment 1 (2026-09-28, after script 1 ran and passed 7/7 on its first run; before scripts 2 and 3 were run; disclosed)

* Script 1 first run: 7/7 checks passed, real run exit 0, `--mutate` control exit 1 with M1 failing (residual 9e-1 against the 1e-12 threshold).  Nothing in script 1 was changed
  after that run except one printed-wording fix (a mis-described constant in the M2 line, cosmetic); the .out files are from the final text.
* Added, not declared above: **M1b** (|c| = 1/mu, the constant the current script uses; verified at the six M1 points, worst deviation 0).
* Exit-code convention made uniform for all three scripts (the pre-registration text above was inconsistent): the real run exits 0 iff every check passes; the `--mutate` run exits 1
  when the targeted check FAILS as required, and exits 0 (printing "DID NOT FAIL -- the check has no power") if the control has no power.
* Script 3's MUTATE control is defined as: subtraction dropped, so sigma_0 = 0 and the S2 consistency check must fail.  (unchanged in substance.)

## Amendment 2 (2026-09-28, before script 2 was run; disclosed)

* V5 as declared said "g_f(0.05) within 1% of 1/pi".  Hand arithmetic (done before running anything) shows this is wrong: g_f(mu) = (1/pi)(1 - 2 pi^2 mu^2/3 + ...), so g_f(0.05) is 1.6% below 1/pi.
  The error is mine (I approximated the plateau width by eye).  Corrected criterion: g_f(0) = 1/pi exactly (formula limit) and the small-mu expansion pi g_f = 1 - (2 pi^2/3) mu^2 holds
  to 1% of the *deviation from 1* at mu = 0.01 and 0.05.  All other V5 clauses are unchanged.  No number was seen before this correction.
* V4: the declared "slope over 4 mu e^{-2 pi mu} -> 1 within 3% at mu = 40" is kept; I note in advance it will be satisfied trivially, because for the fermion the closed-form slope is
  4 mu e^{-2 pi mu}/(1 - e^{-4 pi mu}) (no O(1/mu) correction, unlike the scalar's 1.16 at mu = 5).  Reported at mu = 5, 10, 20, 40.

## Amendment 3 (2026-09-28, AFTER the first run of script 2; disclosed)

First run of script 2: 6/7 checks passed; **V5 FAILED**.  The output is kept as `n5_2_induced_current_FIRSTRUN.out`.  Which clause failed: only the small-mu series clause of Amendment 2, at mu = 0.05
(relative deviation 1.2e-2 against my 1e-2 tolerance); the clauses g_f < g_s (all tabulated mu), g_f/g_s -> exp(-pi/(4 mu)) (worst 4.6e-3 at mu = 5) and mu = 0.01 (4.6e-4) passed.
Diagnosis (scratch script, not committed, run before any change): the miss is exactly the next Taylor term.  With x = 2 pi mu, 1 - x/sinh x = x^2/6 - 7 x^4/360 + 31 x^6/15120 - ...;
at mu = 0.05 the two-term truncation misses the deviation by 1.15e-2, the three-term series by 1.2e-4, the four-term by 1.2e-6.  So the failure is a mis-scaled tolerance on a truncated
series (my error, the second of its kind in this clause), not a fault of the current, the modes or the closed form.
Change: the V5 series clause now compares to the THREE-term series pi g_f = 1 - (2 pi^2/3) mu^2 + (14 pi^4/45) mu^4, tolerance 1e-3 of the deviation from 1, at mu = 0.01 and 0.05.
Nothing else in V5 or elsewhere was changed; V1-V4, V6 and their thresholds are as declared.  This clause tests only a Taylor coefficient of the closed form, so it carries almost no weight in any conclusion.

## Amendment 4 (2026-09-28, AFTER the first run of script 3; disclosed)

First run of script 3: 4/6 checks passed; **S1 FAILED and H5 FAILED**.  The output is kept as `n5_3_schwinger_model_ds2_FIRSTRUN.out` (S2, S1b, S3, S4 passed; the mutate control had not yet been run).
Diagnosis (both are errors in my checks, not in the physics; run before any change):
* S1: my sympy bookkeeping substituted only A'' when forming E'' + (e^2/pi) a^2 E, but E'' contains A''' (and E = A'/a^2), so the printed residual was not zero.  The Euler-Lagrange expression
  itself, the cosmic-time form, the memory relation and the constant-E particular solution all printed as required.  Fix: use the identity d(EL)/dtau = E'' + (e^2/pi) a^2 E (with E = A'/a^2 and
  A' = a^2 E), which sympy verifies to be exactly zero; EL = 0 then gives the equation.  No physics or threshold changed.
* H5 (a): the declared analyticity test (threshold third-difference <= 1e-4 and <= 20 x a control stencil at x = 0.6, applied to the raw coefficient C(x) = Gamma(Delta)Gamma(1-Delta) 2F1(...)) failed
  with |d3| = 2.0e-3 (control 5.1e-5, ratio 38).  The analytic reason (checked by hand before changing anything): C(x) contains pi/sin(pi Delta) with Delta(1 - Delta) = x, which has a POLE at x = 0
  (Delta -> 0, the massless zero mode), only 0.25 from the threshold, so third differences with step 0.01 are ~ 1e-3 by analyticity alone; the control at 0.6 is farther from the pole and the (0.6/0.25)^4 ~ 33
  ratio matches the observed 38.  My original criterion ignored the pole.  Change: apply the test to x C(x) (the pole removed), with the same threshold 1e-4, and add a calibration that the test can
  see a genuine singularity: the third difference of Delta_-(x) = 1/2 - sqrt(1/4 - x) (a square-root branch point at exactly 1/4) must be >= 100 x the threshold value for x C(x).  The 20 x control clause is dropped
  (it tested the wrong thing).  H5 (b) (positivity of the sphere coefficients) is unchanged and passed on the first run.
Nothing else was changed in script 3.  Script 2's V1 output text was reworded (the sign of the current is the paper's orientation convention; the physical statement is sigma > 0 because sigma is proportional to e^2 and
the field must lose energy to the pairs); numbers unchanged, .out files regenerated from the final text.

## Amendment 5 (2026-09-28, disclosed)

The first `--mutate` run of script 3 exited 1 for the WRONG reason (a ZeroDivisionError in my linearity test, since with the subtraction dropped the coefficient is exactly 0 and I divided by it), so it was not a valid control.
Fix: the linearity test uses an absolute difference.  The control now reaches "S2 FAILED as required" (coefficient 0 against 1/pi) and exits 1.  All final .out files were regenerated from the final scripts (each real run
ends with `exit 0`, each control with `exit 1`; the FIRSTRUN files are the first real runs of scripts 2 and 3 that failed as disclosed in Amendments 3 and 4).

## Outcome summary (filled in after the last run; the criteria above are unchanged except as amended)

Final: script 1 7/7, script 2 7/7, script 3 6/6; controls fail as required (M1, V1, S2).  Disclosed misses along the way: V5 (series tolerance, Amendment 3), S1 (bookkeeping) and H5(a) (missed the pole at x = 0,
Amendment 4), the invalid first control of script 3 (Amendment 5).  Hypotheses H1-H5 all held as stated; the one number worth remembering: g_f(mu) = 2 mu/sinh(2 pi mu), g_f(0) = 1/pi, half-height at mu = 0.3465.
