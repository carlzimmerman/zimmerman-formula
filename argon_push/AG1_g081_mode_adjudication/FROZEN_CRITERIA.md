# AG1 — G081 MODE-EQUATION ADJUDICATION · FROZEN CRITERIA (pre-registered, 2026-10-15)

**Lane:** `argon_push/AG1_g081_mode_adjudication/` (argon track; leaf lane — commits
authorized by the user's standing push instruction for argon_push; register rows are
left to the conductor tick per LOOP_CONDUCTOR §2.9).

**What is adjudicated:** GF2's flagged, unadjudicated discrepancy (GF2 README boundary
4): re-deriving G081's linearized momentum equation could not reproduce its
`[SELF-CONSISTENT]` mode equation — G081's form (G081_equilibrium_stability.py L31/L36)

    Euler (linear): -w^2 rho0 xi = -rho0 phi1' + sigma^2 (rho0 xi')'
    =>  sigma^2 xi'' - (2 sigma^2/r) xi' + (2 sigma^2/r^2 - w^2) xi = 0   [SELF-CONSISTENT]

omits the standard force of the perturbed density in the equilibrium field,
`-delta_rho * dPhi0/dr` (= `+(C/r) rho0 xi'` here, with delta_rho = -rho0 xi' for
rho0 = A/r^2). This lane adjudicates the flag from first principles, symbolically and
numerically, and states the consequences for: G081's V2/V3 verdicts, GF2's P1-acceptance
boundary on the static log branch (the only live kappa=1/2 candidate), and G111's
reading-(c) gate. No file outside `argon_push/` is modified.

**Scope discipline:** the adjudication is INTERNAL to G081's own declared model
(isothermal closure P = rho*sigma^2, delta_P = sigma^2 delta_rho, Newtonian radial
Lagrangian perturbation, rho0 = A/r^2 on (0, r_break], G081's registered constants read
at runtime from deepseek_push/G081_results.json). It does NOT claim the full tether
medium (W_rem + stiffness) behaves as the isothermal reduction; that is registered as
follow-up (AG2), not answered here.

---

## The corrected linearization (stated BEFORE any run)

Continuity + Euler + Poisson + isothermal EOS, linearized about (rho0, P0, Phi0),
v1 = -i w xi e^{-iwt}:

    delta_rho = -(1/r^2) (r^2 rho0 xi)'                (= -rho0 xi'  for rho0 = A/r^2)
    -w^2 rho0 xi = -rho0 phi1' - delta_rho Phi0' - (sigma^2 delta_rho)'
    (r^2 phi1')' = 4 pi G r^2 delta_rho,  phi1' = -4 pi G A xi / r^2 (inner mass frozen)
    Phi0' = C/r,  C = 4 pi G A,  hydrostatic closure sigma^2 = C/2

Eliminating phi1 and dividing by rho0 gives the CORRECTED self-consistent radial mode
equation, general sigma^2:

    sigma^2 xi'' + (C - 2 sigma^2) xi'/r + (C/r^2 + w^2) xi = 0                    (E-corr)

and at the equilibrium value sigma^2 = C/2 (drift cancels EXACTLY — the pressure-
curvature drift -2 sigma^2/r pairs with the omitted +C/r term):

    xi'' + (w^2/sigma^2 + 2/r^2) xi = 0                                            (E-corr*)

Structure: xi = sqrt(r) Z_{i nu0}(w r/sigma), nu0 = sqrt(7)/2 (imaginary Bessel order);
at w^2 = 0 the basis is sqrt(r){cos, sin}(nu0 ln r) — log-periodic, NO algebraic zero
mode. On an annulus [r_in, r_b] the omega^2 = 0 boundary-condition ladder (exact, zero
import; F-BC phase tan(theta) = -2 nu0/5 = -sqrt(7)/5):

    DD and FF:  w_n = exp(n pi/nu0)        = exp(2 n pi/sqrt(7));      w_1 = e^{2pi/sqrt7}
    DF:         w_n = exp((n pi - atan(sqrt7/5))/nu0)
    FD:         w_n = exp((n pi + atan(sqrt7/5))/nu0)
    (w = r_b/r_in; omega_0^2 = 0 exactly at each rung; Sturm: n rungs crossed = n
     negative eigenvalues; stable iff below the first rung of the BC pair.)

Physically consistent pairs (frozen inner mass, homogeneous problem): DD (rigid-rigid)
and DF (rigid inner interface + free outer surface, delta_P_L = -sigma^2 rho0 (xi' +
2 xi/r) = 0). FF/FD are reported as mathematical structure of (E-corr*) with the caveat
that a moving inner interface requires an inner-mass-perturbation term.

---

## Checks (PASS/FAIL, machine-evaluated, honest FAILs preserved)

- **C0 — first-principles derivation.** sympy linearization from the four primitive
  equations reproduces (E-corr) with symbolic residual identically 0, and at
  sigma^2 = C/2 reduces to (E-corr*). Sub-check C0b: independent re-verification of
  GF2's P1 inputs on the same symbols — Laplacian(C ln r) = C/r^2, rho0 = C/(4 pi G r^2),
  hydrostatic residual at sigma^2 = C/2 identically 0 (the kappa chain's algebraic base
  is untouched by the mode error). PASS iff residuals are exactly zero (sympy `== 0`).
- **C1 — discrepancy pinpointed (MUTATE M2).** Deleting the `-delta_rho Phi0'` term from
  the SAME symbolic machinery reproduces G081's L36 equation coefficient-by-coefficient,
  and then xi = r and xi = r^2 solve it at w = 0 with residual 0 (G081's claim verified
  under its own omission). PASS iff both reproduce. If C1 fails, the adjudication does
  not locate the discrepancy and is VOID.
- **C2 — zero modes killed.** Under (E-corr*) at w = 0: residuals of xi = r and xi = r^2
  are symbolically NONZERO (expected: 2/r and 4 respectively, up to normalization).
  PASS iff nonzero. (MUTATE M1: any claim that xi = r solves (E-corr*) at any real w^2
  with sigma^2 = C/2 must FAIL — checked by solving the residual equation for w^2 and
  finding no real solution.)
- **C3 — homology premise false at fixed sigma^2.** The eps-rescaled profile
  A(1-2eps)/r^2 with sigma^2 HELD at C/2 has hydrostatic residual -2 eps C/r + O(eps^2)
  (nonzero at first order): G081 L177's "homology of the isothermal family at fixed
  sigma^2" is not a family of equilibria; true homology scales (A, C, sigma^2) together.
  PASS iff the first-order residual is symbolically nonzero.
- **C4 — exact spectral structure.** (i) xi = sqrt(r) J_{i nu0}(w r/sigma) satisfies
  (E-corr*) (sympy residual 0, or mpmath pointwise |resid| < 1e-12 on a 200-point grid
  if symbolic Bessel simplification stalls — method recorded); (ii) the w^2 = 0
  log-periodic basis has residual exactly 0; (iii) numerical shooting (scipy, rtol
  1e-10) on DD and DF reproduces the closed-form first rungs: |ln w_num - ln w_closed|
  < 1e-8; (iv) Sturm counting: at w = w_1 * (1.5, 3, 12) the number of negative
  eigenvalues equals (1, 2, 3) within the DD ladder prediction. PASS iff all four.
- **C5 — framework verdict table.** With G081's registered constants (a0, C, sigma^2,
  r_M, r_break, A read at runtime), omega_0^2 computed for r_in in {0.05, 0.1, 0.2,
  0.4, 0.5888, 0.85, 1.0, 2.0} kpc x {DD, DF}, plus growth timescale 1/|Im w| where
  omega_0^2 < 0. No PASS/FAIL — a verdict TABLE. Frozen verdict logic: the conservative
  isothermal reading of the static branch is STABLE-ON-ANNULUS iff omega_0^2 > 0 for
  both DD and DF at the given r_in; the critical inner radii are r_crit(DD) =
  r_break e^{-2pi/sqrt7}, r_crit(DF) = r_break e^{-(pi - atan(sqrt7/5))/nu0} (computed,
  not typed). The singular ball (0, r_break] (G081's domain) admits NO
  extension-independent verdict (C7) — G081's cap-invariant omega_0^2 = 0 EXACT verdict
  is REVERSED iff C0-C4 pass.
- **C6 — Ebert-Bonnor control (machinery anchor; NON-GATING, declared at freeze).**
  The SAME primitive-equation machinery (symbolically generated, general rho0) applied
  to the non-singular truncated isothermal sphere with isothermal perturbations must
  reproduce the classical critical point: xi_crit in [6.43, 6.47] and contrast
  rho_c/rho_edge in [13.99, 14.09] (literature: Ebert 1955 / Bonnor 1956 / Antonov
  1962: 6.451, 14.04). If the control does not converge to tolerance within the lane's
  run budget, the .out and results.json must say CONTROL-NOT-CONVERGED loudly and the
  adjudication's spectral THRESHOLDS are demoted to CONDITIONAL (the derivation
  discrepancy C0-C3 stands regardless — it is exact algebra).
- **C7 — ill-posedness at r -> 0.** Both independent solutions of (E-corr*) behave as
  sqrt(r) e^{+-i nu0 ln r} -> 0 and are square-integrable near 0 with the natural weight
  (A dr): the endpoint is limit-circle; "xi(0) = 0" (G081's regularity) is satisfied by
  BOTH branches and selects nothing; the spectrum over self-adjoint extensions is
  extension-dependent (demonstrated: omega_0^2(r_in) for fixed r_b diverges to -inf as
  r_in -> 0 along the DD branch, rate ~ -sigma^2 x^2/r_in^2). PASS iff both claims
  verified numerically.

## Mutations (must FAIL, run with MUTATE=1)

- **M1:** residual of the claim "xi = r solves (E-corr*) at some real w^2, sigma^2=C/2"
  — must find NO real w^2 (else adjudication wrong).
- **M2:** term-deleted machinery must reproduce G081 L36 + its {r, r^2} zero modes
  (else the pinpoint is wrong).
- **M3:** EB control with the `-delta_rho Phi0'` term deleted must NOT land the critical
  contrast in [13.99, 14.09] (else the control is insensitive to the adjudicated term
  and the adjudication is demoted to SUSPECT).
- **M4:** corrupting the F-BC phase by +10% must move the numerical DF first rung off
  the closed form by > 1% (else the eigen-solver is not resolving the BCs).

## Verdict logic (frozen)

- **ADJUDICATION = FLAG UPHELD** iff C0 ^ C1 ^ C2 ^ C3 ^ C4 ^ C7 pass and C6 passes or
  is loudly NOT-CONVERGED (thresholds then CONDITIONAL). Consequences, stated in the
  results: (1) G081 [SELF-CONSISTENT]/[FIXED-WELL] mode machinery and its V2/V3
  verdicts (double homology zero mode, omega_0^2 = 0 exact, cap-invariant neutral
  continuum, "well-posed linear relaxation") are INVALID as committed; replaced by
  (E-corr*): discrete spectrum on [r_in, r_b], stable iff ln(r_b/r_in) below the BC
  ladder's first rung (DF-binding: w_1 = e^{(pi - atan(sqrt7/5))/nu0} ~ 7.44), unstable
  above with one more mode per rung e^{pi/nu0} ~ 5.4 in width; singular ball ill-posed.
  (2) GF2 kappa = 1/2 algebraic chain (P1 base identities) is UNAFFECTED (C0b); the
  P1-acceptance boundary SHARPENS: the static branch's physical admissibility as a
  CONSERVATIVE fluid requires a stabilizing inner cutoff (r_in > r_crit) or the
  framework's dissipative settling channel (S3 attractor) — registered, not resolved.
  (3) G111 reading-(c) ("neutral family preserved", fixed-well F(0) = 4.9998 structure,
  neutral-family residuals <= 1e-6) tests the WRONG mode structure — flagged to the
  conductor for re-spec with (E-corr*) and the corrected fixed-well probe
  sigma^2 xi'' + w^2 xi = 0 (discrete tan z = -z/2-type spectrum, no neutral continuum).
- **ADJUDICATION = FLAG REJECTED** iff C1 fails or M2 fails or M3 shows insensitivity.
- Numbers: every constant used is either structural (integers, pi, sqrt, exp, atan),
  read at runtime from G081_results.json, or a literature control target (C6 only).
  Zero framework constants typed from memory.

## Observational kill test (stated before numbers, for IDEA.md)

The corrected conservative analysis predicts: any settled phantom annulus wider than
w_1(BC) ~ 7.4-10.8 in radius ratio collapses on ~|omega_0|^{-1} <~ r_break/sigma
(MW: tens of Myr). Observed law-obeying settled halos persist for Gyr across annuli
far wider than the ladder (SPARC radial baselines, MW rotation law, X-COP apertures).
Therefore EITHER the phantom's effective inner cutoff satisfies r_in > r_crit per halo
(sharp, checkable: MW r_crit(DF) = r_break e^{-(pi-atan(sqrt7/5))/nu0}, computed in
lane) OR the settling is genuinely dissipative (S3/CFG747-748-776 attractor doing
stabilizing work) — which is exactly what G111's N-body suite must test, re-specced
against (E-corr*). If a future conservative-fluid simulation of the certified system
shows wide settled annuli stable with no dissipation, this adjudication's spectral
verdict is falsified.
