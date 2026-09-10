# Velocity mixing and physical-response gate — 2026-09-10

Base: `5a743f43288fa65b208e1321eff6ea699efc85e0`. Goal unchanged:
one relativistic action satisfying the full fried-chicken requirements.
**Status: OPEN. No complete theory, empirical discovery, or general MOND no-go.**

This extends the preceding elliptic-curvature action audit, not the older
conformal lapse-braiding ansatz. Carl Zimmerman's exponential-law framework
and insistence on ordinary physical-metric matter coupling motivate the test.
The construction and deductions below are research calculations, not a claim
that Carl supplied or that the literature has never contained these equations.

## Contract and explicit action

Test a frozen, leading weak-field scalar quadratic action. Set c=1, m>0,
q=|k|²>0, time convention exp(-iωt), physical lapse Φ=n and Ψ=−z.
Use u=z+b n to allow degenerate mixing of lapse and metric velocities:

\[
 K_{ij}=\operatorname{diag}(\dot u+qB,\dot u,\dot u),\qquad
 L=\frac m2(K_{ij}K_{ij}-K^2)+\frac{md}{3}K^2
   +mq\{r(z+n)^2-\mu_\theta n^2\}
   -n\rho+z\mathcal S+B\dot\rho .
\]

Here B is the scalar shift and S (written mathcal S above) the stress trace.
Scalar spatial gauge E=0 is used; its unreduced matter coupling is E rhö.
Conservation supplies the longitudinal momentum source B rhȯ. This is not a
new nonlinear covariant action or a replacement for its Dirac analysis.
For the exponential law the directional differential coefficient is

\[
 \mu_\theta=1-e^{-y}(1-y\cos^2\theta),\quad
 \mu_t=1-e^{-y},\quad\mu_l=1+(y-1)e^{-y}.
\]

It is NOT the same object as the scalar interpolation function mu(y).
Algebra applies on the regular branch d≠0,1, r≠0, mu_theta>0,
C=r(1−b)²−mu_theta≠0, away from frequency poles.
k=0, y=0 and singular branches are excluded, not certified by continuity.

## Vary first, then solve

The script differentiates L and solves its three equations for u,n,B;
all three substitution residuals must vanish. The lapse equation is

\[
 2mq\{r(1-b)[u+(1-b)n]-\mu_\theta n\}-\rho-b\mathcal S=0,
\]

the shift equation is

\[
 2mdq^2 B/3+2m(d-1)q\dot u+\dot\rho=0,
\]

and the u equation is dL/du−d/dt(dL/dudot)=0, printed in Fourier form.
For static pressureless sources, independent solutions give

\[
 n=-\frac{\rho}{2mq\mu_\theta},\qquad z=-n.
\]

Thus this family preserves the previous linearized MOND response and no slip.
It does not independently derive the full nonlinear exponential equation.
Eliminating n and B in vacuum gives

\[
 A=\frac{3m(d-1)}d,\qquad
 c_s^2=\frac{d r\mu_\theta}{3(d-1)[r(1-b)^2-\mu_\theta]}.
\]

These are outputs of the variation, not assigned test results.

## First attempted repair: lapse-velocity mixing

Compute physical curvature, including the shift and physical z=u−bn:

\[
 R_{00}=-qn+i\omega qB+3\omega^2z.
\]

The computed coefficient of its leading high-frequency response is

\[
 \lim_{\omega\to\infty}\frac{R_{00}}{\omega^2}
 =-\frac{3b[b\mathcal S+(br-r+1)\rho]}{2mqC}.
\]

In particular the stress coefficient is −3b²/(2mqC). On a regular branch,
requiring this coefficient to vanish forces b=0. Lean proves this algebraic
implication with the nonzero denominator hypothesis explicitly included.
**Vanishing is a chosen necessary diagnostic for this repair, not a universal
definition of relativistic causality:** physical source admissibility and
all-sector support require additional analysis. Conserved-source response
cannot be replaced by the lapse solution alone.

## Second attempted repair: constant free-wave speed

Even permitting direction-dependent effective coefficients, choose
b=0, r=−1, d=1+mu_theta. The derived results are

\[
 c_s^2=\frac13,\qquad A=\frac{3m\mu_\theta}{1+\mu_\theta}>0,
\]
\[
 R_{00}(\omega\to\infty)=\frac1{2m\mu_\theta}
 \left[\frac{3\mu_\theta-1}{1+\mu_\theta}\rho-\mathcal S\right].
\]

The vacuum pole is now that of a constant-speed wave. But the response
contains direction-dependent inverse operators. This is NOT a successful
causal construction. Moreover A→0 as y→0; the exceptional constraint and
nonlinear strong-coupling analysis would have to be redone.
Allowing d(mu_theta) is deliberately generous: a local scalar coefficient
d(y) cannot depend on Fourier direction in this manner. A nonlinear local
action realizing this tuning has not been supplied.

Conservation is not silently dropped. The script constructs the compact-source
stress pattern Txx=∂y²f, Tyy=∂x²f, Txy=−∂x∂yf, with other components zero,
and checks its divergence. For X=kx²+ky², Z=kz² the contact becomes

\[
 \frac{X(X+Z)}{2m(\mu_tX+\mu_lZ)}f.
\]

For unequal positive mu_t,mu_l this is not a spatial polynomial: substituting
X=−mu_l Z/mu_t into its numerator is nonzero for Z≠0.
This test uses an external conserved stress perturbation, not a constructed
positive-energy solution of an ordinary-matter action. That distinction limits
its interpretation; it is not an empirical falsification.

## Third calculation: a uniform surviving-family obstruction

With b=0 the stress contact is −S/[2m(d−1)]. Demanding an angle-independent
coefficient makes d constant within this parametrization. Let the density
contact equal h rho/(2m). Solving for r gives

\[
 r=\frac{(d-1)(1-h\mu_\theta)}{\mu_\theta+d-2-h(d-1)}.
\]

For Einstein-normalized density contact h=1 on an open regular interval,
r=1−d and cs²=d mu_theta/[3(d−1+mu_theta)]. This matches the density contact;
matching the stress contact to Einstein's as well additionally sets d=2.
No PPN parameter is inferred from this limited matching condition.

For every fixed d>1, put D=mu_t X+mu_l Z, q=X+Z,
E=(d−1)q+D. Choose source-free compact initial data u=E f, udot=0.
The action-derived n=−(d−1)q f and B=0 are compact as well. The lapse and
shift equations hold; physical R00=q u along vacuum evolution. Therefore

\[
 \partial_t^4 R_{00}|_0=\frac{d^2D^2q^3}{9E}f.
\]

Polynomial division in X gives the exact nonzero remainder

\[
 \boxed{-\frac{d^2(d-1)^2(\mu_l-\mu_t)^5 Z^5}
 {9(d-1+\mu_t)^5}}.
\]

For exponential MOND mu_l−mu_t=y exp(−y)>0 at every finite y>0.
The elliptic inverse therefore remains for this entire density-contact-matched
d>1 family, not just the previously examined point d=2. The remainder vanishes
in the isotropic control. A constant-coefficient distribution supported only
at the spatial origin has a polynomial Fourier symbol; this nonpolynomial
symbol consequently has off-origin support. Some smooth compact f produces
an exterior fourth derivative despite initially compact constrained fields.

This is a **frozen principal-system support obstruction**, conditional on the
specified action and matching requirements. Lifting it to a regular nonlinear
background remains necessary. It does not exclude other actions, the singular
d=0,1 sectors, independent dynamical fields, or the whole framework.

## Verification, limits, and next research move

The run manifest and stdout record exact commands, inputs, versions, and exit
codes. The suite includes six new regression tests, conditional Lean lemmas,
and the preceding elliptic-curvature/trace/CAM tests. Strict closure requests
intentionally return 2, not a manufactured PASS.
Development caught an unsimplified SymPy `0*I` residual and an unavailable Lean
lemma name; both were corrected before the recorded final run. Initial tests
failed when the implementation was absent. Self-review covers this report and
the action/source/sign conventions; it is not independent external refereeing.

The original gravity goal remains OPEN: no full nonlinear Dirac closure,
ordinary-matter causal solution, complete PPN, zero-mode completion, or empirical
confirmation follows from this package. The fitted kappa=1/2 is untouched.

The next materially different construction must make the auxiliary response
causal while preserving the static law, rather than merely retuning this
trace/lapse family. A concrete next discriminator is to replace the elliptic
auxiliary with a counted dynamical field and derive the full coupled metric,
auxiliary and minimally coupled matter characteristic matrix. That route must
then face the additional-mode and zero-field gates; it is not presumed viable.
