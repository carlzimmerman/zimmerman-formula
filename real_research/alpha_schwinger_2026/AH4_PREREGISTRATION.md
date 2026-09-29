# AH4 -- the induced current of a charged scalar in dS_4 (pre-registration)

Written 2026-09-28 BEFORE `ah4_induced_current_ds4.py` was run. Follows AH1-AH3 (5db88bfc2, 5823f6bfe, 86f3c7a9a).

## Why dS_4

AH1-AH3 were a 2D toy where e has mass dimension 1, so e^2/H^2 was not the fine structure constant. In 4D, e is dimensionless and
alpha = e^2/(4 pi) is the real thing. Two things change: the mode equation has index 9/4 (not 1/4) and a polar angle in k-space, and the
current has a logarithmic divergence, i.e. charge renormalization, which does not exist in 2D.

## Setup (Kobayashi & Afshordi, arXiv:1408.4141, Section 2; read from the PDF, not recalled)

Units H = 1, planar patch, tau = -1 (a = 1). lambda = eE/H^2, mu_phys = m/H. Mode equation
  q'' + [ (k_z + lambda/tau)^2 + k_perp^2 + (mu_phys^2 - 2)/tau^2 ] q = 0,
solved by q_k = e^{i kappa pi/2} (2k)^{-1/2} W_{kappa, mu_w}(2 i k tau), kappa = -i lambda r (r = cos theta = k_z/k),
mu_w = sqrt(9/4 - lambda^2 - mu_phys^2)  (imaginary = i rho for lambda^2 + mu_phys^2 > 9/4).
Formal current  <J_z> = -(2e/((2 pi)^3 a^2)) Int d^3k (k_z + lambda/tau) |q_k|^2, divergent.
Regularized by adiabatic subtraction through order T^-2 (their eqs. 2.53-2.58):
  W^2 = Omega^2 - a''/a + (3/4)(Omega'/Omega)^2 - (1/2) Omega''/Omega,  Omega^2 = (k_z + lambda/tau)^2 + k_perp^2 + a^2 m^2,
  1/(2W) ~ 1/(2 Omega) - delta/(2 Omega^2),  delta = [ -a''/a + (3/4)(Omega'/Omega)^2 - (1/2) Omega''/Omega ] / (2 Omega),
subtracted INSIDE the integrand (the paper notes this is preferable for numerics). Then <J_z>_reg = e a H^3/(4 pi^2) * f(lambda, mu), with the closed form (2.58):
  f = -2 lambda^3/15 + (lambda/3) ln(m/H)
      + [45 + 4 pi^2 (-2 + 3 lambda^2 + 2 mu_w^2)] mu_w cosh(2 pi lambda) / (12 pi^3 lambda sin(2 pi mu_w))
      - [45 + 8 pi^2 (-1 + 9 lambda^2 + mu_w^2)] mu_w sinh(2 pi lambda) / (24 pi^4 lambda^2 sin(2 pi mu_w))
      + Re Int_{-1}^{1} dr  i lambda/(16 sin(2 pi mu_w)) [ -1 + 4 mu_w^2 + (7 + 12 lambda^2 - 12 mu_w^2) r^2 - 20 lambda^2 r^4 ]
        * { (e^{2 pi r lambda} + e^{2 pi i mu_w}) psi(1/2 + mu_w + i r lambda) - (e^{2 pi r lambda} + e^{-2 pi i mu_w}) psi(1/2 - mu_w + i r lambda) }.
**Transcription risk, declared:** this was typed from a PDF text layer whose layout is partly garbled. V0 tests it internally (the 1/lambda poles of the
two trig terms cancel as lambda -> 0; checked by hand) and V1 tests it against direct numerics. If V1 fails, the run is reported as UNRESOLVED
(transcription or direct sum wrong), never as a physics result.

## What the script must do (in this order)

1. Direct computation: f_direct = -2 Int dk k^2 Int_{-1}^{1} dr (k r - lambda) [ |q_k|^2 - S~(k, r) ], with S~ = 1/(2 Omega) - delta/(2 Omega^2)
   built symbolically (sympy) from the definitions above; log-spaced quadrature in k on (1e-40, K], Gauss-Legendre in r, fitted large-k tail as in AH2.
2. Compare to the closed form on a declared grid: (lambda, mu_phys) in {(0.5, 2.0), (1.0, 1.5), (0.3, 1.0), (0.5, 1.2), (1.5, 0.8), (0.4, 1.4), (0.3, 3.0)}.
   (Light-field points have mu_w <= 1.3 so the IR tail k^{-2 mu_w} is resolved; nearly massless fields are excluded, where the adiabatic expansion breaks down.)
3. Running of e: sympy computes nabla_nu F^{nu z} in dS_4 for F_{tau z} = E a^2; the coefficient of ln(m/H) in f, converted to a current, is compared
   to the scalar-QED one-loop running d(1/e^2)/d ln(mu) = -1/(24 pi^2).
4. Heavy-field behaviour from the closed form at small lambda: does the response fall as a power or exponentially, and is the ln(m) term cancelled?
5. The alpha question: sigma/H = alpha * G(mu) with G = f_1/pi (f = lambda f_1 + ...), alpha = e^2/(4 pi) now the 4D constant. Score the ties.

## Pass / fail criteria (declared now)

* V0 the transcribed closed form is finite and linear as lambda -> 0 (|f(1e-4)/1e-4 - f(1e-3)/1e-3| / |f(1e-3)/1e-3| < 1e-3 at two masses) and odd in lambda.
* V1 direct = closed form on the grid: worst relative difference <= 2e-3, all with the same sign. The paper's sign convention is followed exactly
  (k_z + lambda/tau), so the expected ratio is +1; a global -1 would be reported as a convention difference and stated.
* V2 the current in dS_4 (small lambda, closed form): log-log slope of |f/lambda| between mu = 10 and 40 lies in [-2.3, -1.7] (power law ~ 1/mu^2, expected
  from the derivative expansion), and the ln(m) term is cancelled at large mu (|f/lambda| < 1/3 at mu = 40, against (1/3) ln 40 = 1.23 for the bare log term).
  If instead the current is exponentially small, or the exponent is different, V2 FAILS and that is the finding.
* V3 coefficient of ln(m/H): (e H^3/(4 pi^2)) * lambda/3 = e^2 E H/(12 pi^2), and the one-loop running of a scalar-QED coupling times
  nabla_nu F^{nu z} gives the same magnitude e^2 H E/(12 pi^2) (ratio 1 to 1e-12; sign is convention).
* MUTATE control: dropping the order-T^-2 term delta from the subtraction (order 0 only) must FAIL V1.
* V4 (ties) alpha is DETERMINED by a tie sigma/H = c only if the required alpha = c/|G(mu)| is independent of mu within a factor 2 across
  mu in {0.5, 1.0, 2.0, 5.0}. Ties: c in {kappa, kappa/pi, 1/(2 pi), 1/pi, 1, 2 kappa} (kappa = 1/2, FITTED).
* Electron-mass reading (declared): extrapolate |G| ~ C/mu^2 from mu = 20, 40; report the alpha a tie sigma/H = c would require at mu_e = m_e/H_0 = 3.55e38,
  labelled an extrapolation.
* Expected outcomes, stated in advance: V0, V1, V3 pass; V2 passes with a power law ~ 1/mu^2 (the log is renormalized away at scale m); no tie fixes alpha;
  the electron-mass reading is astronomically large.

## Reading rules

* The ln(m/H) term is the running of e from scale m down to H. The renormalization condition that makes the paper's scheme physical (the flat-space
  vacuum polarization vanishes at m >> H) is exactly "alpha is the measured low-energy value", so alpha enters as an INPUT. A finite counterterm c * e^2 E H
  (a shift of 1/e^2) would change the current by a term linear in E; it is the same freedom that makes alpha an input in flat space.
* This is a scalar. Fermions, backreaction, and other charged species are untested. kappa = 1/2 stays FITTED; the SM-mass wall is untouched.
