# Exact relation between the deep-force correction and the response moment

## Target and scope
The parent auxiliary NR action is fixed. This child derives a second, independently measurable source feature of that action and its sharp relation to the response moment. It does not assume the moment is a cosmological constant, select lambda, or insert 32pi. The actual parent branch is stationary q_T=lambda T, lambda>0, with b(y)=sqrt(1+1/y)−1, nu=1+b/(1+(y/T)^2). Spatial dimension n>=3 enters the Newton normalization and radius; y, T and lambda are dimensionless in every such dimension. No hbar enters. The proven elliptic interval0<lambda<5/96 is a subset of the positive-lambda branches considered here.

## Deep source prediction
The parent proves T(y)=(8/(7lambda))^(1/4)y^(7/8)[1+o(1)] at fixed lambda as y decreases to zero. Put A(lambda)=sqrt(7lambda/8). Then (y/T)^2=A y^(1/4)[1+o(1)]. Since y(1+b)=sqrt(y+y²), direct expansion of the actual spherical flux force gives

g/(a0 sqrt(y))=1−A(lambda)y^(1/4)+o(y^(1/4)).

This coefficient is the limit A=lim[y→0] y^(−1/4)[1−g/(a0 sqrt(y))]. It is an exact asymptotic feature, not a claim that the first term approximates a given finite galaxy interval accurately. It differs from the constant-cutoff kernel whose additional suppression begins at order y². Ordinary source profile dependence is absent in the exterior when expressed through y; source equilibrium and empirical fitting are separate obligations.

## Scaled stationarity and a sharp all-lambda bound
Set v=lambda y and w_lambda(v)=lambda T(v/lambda). Let

B_lambda(u)=b(u/lambda)/lambda=1/[u(sqrt(1+lambda/u)+1)].

Stationarity becomes exactly

1=4∫_0^v u³ B_lambda(u)/(w_lambda²+u²)² du.

For positive u, 0<B_lambda(u)<1/(2u); it increases strictly to1/(2u) as lambda decreases to zero. The integral decreases strictly with w. Its limiting positive root w0(v) consequently strictly exceeds w_lambda(v), and pointwise root convergence follows by bracketing any two positive w values around w0 and using dominated convergence on the finite integration interval. In particular w_lambda<=pi/2 by the parent's q_T<=pi/2 bound.

For the limiting equation substitute z=v/w0. The result is

w0=J(z), J(z)=arctan(z)−z/(1+z²), v=zJ(z),
J'(z)=2z²/(1+z²)²>0.

The map z→v is strictly increasing from0 to infinity, and0<w0<pi/2. This specifies a unique limiting kernel; replacing T by its constant high-y limit would give the wrong moment coefficient.

Let C(lambda)=∫_0^infinity y[nu(y)−1]dy, the finite response moment from the parent. Its scaled exact integral is

lambda C(lambda)=∫_0^infinity v B_lambda(v)/[1+(v/w_lambda(v))²] dv.

Both strict comparisons, B_lambda<1/(2v) and w_lambda<w0, imply

0<lambda C(lambda)<(1/2)∫_0^infinity dv/[1+(v/w0(v))²].

For convergence the scaled integrand is bounded by (1/2)/[1+(2v/pi)²], an integrable bound on the entire positive axis, independent of lambda. Therefore dominated convergence identifies the same upper integral as the limit lambda→0. No uniform extrapolation from a finite sampled source interval is used.

## Evaluate the upper integral
Change variable v=zJ(z). The integral is

(1/2)∫_0^infinity [J(z)+zJ'(z)]/(1+z²) dz
=(1/2)∫ arctan(z)/(1+z²) dz−(1/2)∫ z/(1+z²)² dz+∫ z³/(1+z²)³ dz.

The three contributions are pi²/16,−1/4,+1/4. Thus

0<lambda C(lambda)<pi²/16,
lim[lambda→0] lambda C(lambda)=pi²/16.

In particular C(lambda)~pi²/(16lambda), with a rigorously identified coefficient; the constant-T infinity approximation would incorrectly double it. The bound is strict for every positive lambda, and sharp as a supremum. The sufficient elliptic interval contains sequences lambda→0, so sharpness is retained within that admitted interval.

## Eliminate the freely adjustable coupling
Since A²=7lambda/8, the same action predicts

0<C(lambda) A(lambda)²<7pi²/128,
lim[lambda→0] C(lambda) A(lambda)²=7pi²/128.

A hypothesized response moment Cstar would therefore require A<sqrt[7pi²/(128Cstar)]. This is a conditional test of two features of one kernel, not a derived vacuum normalization. The inequality leaves a continuum of coefficients, and the parent offset is unconstrained. Only a separately derived covariant source/vacuum dictionary can convert this response relation into a Lambda/force relation. A measured asymptotic force deficit would fix lambda within this specific ansatz, supplying a prediction for its high-acceleration moment; it would be a parameter measurement, not a physical principle forcing the target number.

## Evidence and provenance
The analytic proof is above. Exact symbolic checks separately evaluate the scaled integral coefficient, its cancellation, the deep amplitude and the source-radius dimension dictionary. Negative controls use a constant high-field cutoff in the scaled moment, delete the negative rational contribution, or replace the dynamic deep-cutoff exponent by the constant-cutoff exponent. These controls are expected failures. Inputs are frozen and current standard runner manifests are recorded separately. No empirical likelihood, numerical PDE integration, covariant completion or novelty claim is supplied.
