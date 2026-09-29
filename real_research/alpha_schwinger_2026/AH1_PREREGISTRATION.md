# AH1 -- can the Schwinger/Unruh pair-production rate in de Sitter space fix alpha? (pre-registration)

Written 2026-09-28 BEFORE the script `ah1_schwinger_ds2.py` was run. Nothing below was adjusted after seeing output.

## Question

The hypothesis under test: *the horizon's electromagnetic response is tied to kappa = 1/2*, and that tie fixes the fine
structure constant alpha = e^2/(4 pi) (Heaviside-Lorentz, hbar = c = 1). The concrete calculation is the pair-production
factor of a charged scalar of mass m and charge e in a constant electric field E on a de Sitter background with Hubble rate H.

Programme inputs allowed: c, G, Lambda (so H = H_Lambda), and kappa = 1/2 (FITTED, not derived). No electron mass, no E.

## Scope (deliberately narrow)

* dS_2, minimally coupled charged scalar, planar patch, k > 0 mode branch. This is the case the script derives and checks.
* Only the pair-production (Bogoliubov) factor. NOT the induced current, NOT vacuum-polarization running, NOT dS_4, NOT fermions.
  A negative result here does not close those; it says what this quantity can and cannot do.
* Dimensionless variables: lambda = e E / H^2 (field strength), mu = m / H (mass), rho = sqrt(mu^2 + lambda^2 - 1/4).

## Hypotheses (each is a *tie*, a relation the horizon-EM idea could impose)

| tie | statement | constraint g(lambda, mu) = 0 |
|---|---|---|
| T1 | the field-driven acceleration eE/m equals a0 = kappa c H | lambda = kappa * mu |
| T2 | the horizon field is kappa in horizon units, eE = kappa H^2 | lambda = kappa |
| T3 | the massless onset (rho -> 0 at mu = 0) coincides with kappa | lambda = 1/2 at mu = 0 (flagged: the 1/2 comes from the dS_2 scalar's 1/4, not from kappa) |

## What the script must do (in this order)

1. Derive the k > 0 out/in Bogoliubov ratio r = |beta/alpha|^2 = e^{-2 pi rho} cosh(pi(lambda+rho)) / cosh(pi(lambda-rho)).
2. VERIFY it, not assume it:
   * C0: the Whittaker function W_{-i lambda, i rho}(2 i k tau) satisfies the mode equation chi'' + [(k + lambda/tau)^2 + mu^2/tau^2] chi = 0.
   * C1: r from the analytic formula equals r read off numerically from the small-|tau| asymptotics of the in-mode, to 1e-5 relative.
   * C2: lambda = 0 gives the Bose-Einstein factor 1/(e^{2 pi rho} - 1) (Gibbons-Hawking, T = H/2pi).
   * C3: large mu, large lambda at fixed mu^2/lambda gives -ln r -> pi mu^2 / lambda (flat-space Schwinger), within 2%.
   * C4: r < 1 everywhere on the grid; the k < 0 branch (lambda -> -lambda) is suppressed relative to k > 0.
   * MUTATE control: swapping the sign of lambda inside the cosh ratio must FAIL C1.
3. Show the structural fact: the rate depends on e only through lambda = eE/H^2. For alpha in a list of values, choose E/H^2 = lambda/e
   so the same lambda is reached; the pair-production factor is identical to machine precision. Then alpha = lambda^2 / (4 pi eps^2) with
   eps = E/H^2 is a free direction.
4. For each tie, sweep the only remaining freedoms (eps over 1e-3..1e3, and mu where it is free) and report the range of alpha consistent
   with the tie and the rate.
5. Score the ties on the declared criteria below.
6. Report the missing input: the value of eps = E/H^2 that T2 would need in order to reproduce alpha = 1/137.036, and score a short
   list of natural handles on eps declared here in advance: eps in {1, kappa, 1/(2 pi), 1/(4 pi), sqrt(8 pi/3)}.

## Pass / fail criteria (declared now)

* VALID: C0-C4 all pass AND the MUTATE control fails. If any check fails, the numbers are void and the run is reported as failed.
* A tie DETERMINES alpha only if (a) it leaves a single alpha, or a discrete set, with no free parameter beyond kappa, pi and integers,
  and (b) that alpha does not depend on the field mass m.
  Operational test: the alpha range over the sweep spans less than a factor of 2.
* A natural handle HITS if alpha is within 1e-3 (relative) of 1/137.035999177.
* Expected outcome, stated in advance: no tie determines alpha (the degeneracy in step 3 is structural), and no natural handle hits.
  If either expectation fails, that is the finding and is reported as such.

## Reading rules

* A handle that hits is a value match, not a derivation, unless something forces that handle.
* kappa = 1/2 stays FITTED. Nothing here derives it.
* The pass of this script does not touch the closed SM-mass wall; it tests one specific route.

## Amendment 1 (2026-09-28, after the first run, disclosed)

The first run failed C0a: relative residual 5.7e-18 against a threshold of 1e-20 that I had set without basis. Diagnosis (run before any
other change): the residual falls as h^2 with the finite-difference step (2.5e-8 at h = 1e-4, 2.5e-12 at 1e-6, roundoff floor 1.8e-16 at
1e-8, unchanged from 40 to 80 digits), so it is derivative truncation error, not a defect in the mode equation. A wrong-sign potential gives
a residual of 0.61, so the check has power. Change made: explicit step h = 1e-8, threshold 1e-12, plus a required-failure control
(C0a': the same function must NOT solve the wrong-sign equation). No other criterion, threshold or hypothesis was changed; C1-C8 numbers
were identical before and after.

## Amendment 2 (2026-09-28, dimensional caveat, disclosed after commit 5db88bfc2)

The verified pair-production factor is for dS_2. In two dimensions the charge e has mass dimension 1 (and E has dimension 1), so
alpha = e^2/(4 pi) with E/H^2 dimensionless is a 4D convention, not a 2D one. AH1 combined the dS_2 rate with the 4D mapping without
saying so. What survives: (i) the rate depends on e only through lambda = eE/H^2, in any dimension; (ii) the tie statements T1-T3 are
statements about lambda and are dimension-independent; (iii) the numbers eps* = kappa/e = 1.651 and the handle table are 4D arithmetic on
those ties. What does NOT carry over: the specific dS_2 formula r(lambda, mu) and its checks C0-C4 are a 2D toy; the dS_4 rate has a different
index (9/4 in place of 1/4, recalled from the literature, not verified here). No criterion or number in AH1 changes.
