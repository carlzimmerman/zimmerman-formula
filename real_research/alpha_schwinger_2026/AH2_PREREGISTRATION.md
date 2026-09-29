# AH2 -- the induced current of a charged scalar in dS_2, and what it can say about the coupling (pre-registration)

Written 2026-09-28 BEFORE `ah2_induced_current_ds2.py` was run. Follows AH1 (commit 5db88bfc2, amendments 1-2).

## Why this quantity

The pair-production factor (AH1) depends on e only through lambda = eE/H^2, so it cannot fix alpha. The induced current is the one
quantity that carries e explicitly: J = e H F(lambda, mu), so the linear conductivity sigma = J/E is proportional to e^2.
The question: does the horizon-frame vacuum conductivity give a relation that fixes the coupling once the mass is removed?

## Scope

* dS_2, minimally coupled charged scalar, planar patch, Bunch-Davies "in" vacuum for the k modes. Same variables as AH1:
  lambda = eE/H^2, mu = m/H, rho = sqrt(mu^2 + lambda^2 - 1/4) (imaginary rho = i*sigma for light fields).
* **Dimensional caveat (AH1 amendment 2):** in 2D, e has mass dimension 1, so the dimensionless coupling is e^2/H^2, NOT the 4D alpha.
  Nothing here is a statement about the 4D alpha; it is a statement about how a coupling enters a horizon-scale response.
* Not covered: dS_4, fermions, backreaction, running/renormalization of the charge (in 4D the current has an additive charge-renormalization
  ambiguity that does not exist in 2D; that would need its own calculation).

## The comparator (read, not assumed)

Frob, Garriga, Kanno, Sasaki, Soda, Tanaka, Vilenkin, arXiv:1401.4137, Section 5, eqs. (5.10)-(5.14) and (5.30):
  J = (e H sigma / pi) sinh(2 pi |lambda|) / sin(2 pi sigma),  sigma = sqrt(1/4 - mu^2 - lambda^2),
which in the variables above is  J = (e H / pi) * rho * sinh(2 pi lambda) / sinh(2 pi rho)  (rho = i sigma; sin -> sinh).
Stated limits: exactly linear J = e^2 E/(pi H) at m^2 = H^2/4; J ~ 4 (m/H)(e^2 E/H) e^{-2 pi m/H} for heavy fields at small lambda.
The script must reproduce these from a DIRECT mode sum, not by evaluating the formula.

## What the script must do (in this order)

1. Direct computation. For the k > 0 and k < 0 modes chi_k = e^{+-pi lambda/2} (2|k|)^{-1/2} W_{-+i lambda, i rho}(2 i |k| tau) at tau = -1, H = 1:
   J/e = (1/pi) [ Int dk  p |chi_k|^2  -  Delta ],  p = k + lambda/tau,
   the k integral taken symmetrically in k, and Delta = lambda/tau the exactly-integrated heavy-field (Pauli-Villars/WKB) subtraction of eq. (5.12).
   The k>0 and k<0 integrands are added before integrating; the remaining tail beyond the numerical cutoff is estimated from a fit of the
   large-k series f(k) ~ c2/k^2 + c3/k^3 + c4/k^4 (fitted, not assumed).
2. Compare to the closed form on a declared grid, including two light-field points (rho imaginary).
3. Compute the linear conductivity g(mu) = sigma_H H... i.e. sigma H / e^2 = 2 rho / sinh(2 pi rho) at lambda -> 0, and its limits
   (mu^2 = 1/4: 1/pi; mu -> 0: 1/(2 pi mu^2); mu >> 1: 4 mu e^{-2 pi mu}).
4. Score the ties (below).

## Pass / fail criteria (declared now)

* V1 the direct current equals the closed form: worst relative difference <= 2e-3 over the grid (numerical integration + fitted tail).
  The overall sign is a convention (direction of p = k + lambda/tau); the script must find one consistent sign across the whole grid.
* V2 exactly linear at mu^2 = 1/4: J/(eH) = +-lambda/pi at four field strengths, relative difference <= 2e-3.
* V3 J is odd in lambda (direct computation at +lambda and -lambda), to 2e-3.
* V4 heavy-field limit: the closed form's small-lambda slope over the paper's 4 mu e^{-2 pi mu} tends to 1 (within 3% at mu = 40); direct numerics at mu = 3 agree
  with the closed form to 2e-3 (the exponentially small current is resolved, not lost in the subtraction).
* MUTATE control: dropping the subtraction Delta (raw k-symmetric cutoff) must FAIL V1.
* V5 (ties) A coupling is DETERMINED by a tie on the conductivity only if the required e^2/H^2 is independent of the mass to within a factor 2
  across the declared mass classes mu in {0.3, 0.5, 1, 2, 5}. Declared conductivity ties: sigma/H = c with c in {kappa, kappa/pi, 1/(2 pi), 1/pi, 1, 2 kappa}
  (kappa = 1/2, FITTED). Required: e^2/H^2 = c / g(mu).
* Electron-mass reading (declared): for mu_e = m_e/H_0 (H_0 = 67.4 km/s/Mpc; m_e = 0.51099895 MeV) the required ln(e^2/H^2) is reported;
  reported as a 2D-toy statement, not a 4D one.
* Expected outcome, stated in advance: V1-V4 pass (the formula is published and checked); no tie determines the coupling (g varies over many decades);
  and a heavy charged field cannot satisfy any O(1) tie at any O(1) coupling.

## Reading rules

* This tests the dS_2 scalar only. The mass-dependence of g(mu) is the point: the coupling is fixed only if the mass is.
* kappa = 1/2 stays FITTED. A pass of V1-V4 says the current is computed correctly; it says nothing in favour of any alpha.
* The SM-mass wall is untouched.

## Amendment 1 (2026-09-28, after the first run, disclosed)

First run: 4/6 passed. V1 FAILED (worst 1.6e-2 at the light-field point lambda = 0.10, mu = 0.30) and V4 FAILED (mu = 3, lambda = 0.3: direct 2.80e-7
against closed form 4.69e-8). Output kept as `ah2_induced_current_ds2_FIRSTRUN.out`. Diagnosis (run before any change; scratch script, not committed):
(a) light fields have |chi_k|^2 ~ k^{-2 sigma}, so my IR cutoff k0 = 1e-9 dropped a visible tail; k0 = 1e-40 with more log segments brings that point
to 1e-8. (b) the large-k tail fit converges as K^-4 (errors 4.5e-1, 2.8e-2, 1.8e-3, 1.1e-4 at K = 160, 320, 640, 1280 for the mu = 3 point), and the
mu = 3 current (4.7e-8) sits below the first run's absolute floor (~2e-7). Quadrature order made no difference. Changes: k0 = 1e-40, 80 log segments,
K = 640 for the grid, K = 1280 for the mu = 3 point, and a printed convergence table. No criterion, threshold, hypothesis or tie was changed;
the V1-V6 thresholds are the ones declared above. The first-run numbers were too imprecise for the claims they were meant to support, and
those first-run 'closed form vs direct' agreements at the five easy grid points were already 1e-6 or better.
