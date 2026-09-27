# A unique positive auxiliary at fixed smooth data

Claim: on a connected compact smooth three-dimensional leaf without boundary,
fix smooth Riemannian `h`, smooth `0<Nmin<=N<=Nmax`, smooth vector `b=a-DU`,
smooth `epsilon>=0`, and constants `m=M_P^2 cN>0,V0>0`. Then

\[
 H[t]=\int N\{m|Dt-b|^2+\epsilon/t+V_0F(t)\}\,d\mathrm{vol}_h,
 \quad \langle t\rangle_h=1,\quad t>0,
 \quad F(t)=1+(t-1)^4/t^2
\]

has one smooth positive minimizer (up to equality almost everywhere in the
extended-energy H1 domain). This is a fixed-geometry, fixed-U, fixed-canonical-
carrier-data theorem. No uniform bound for a evolving geometry is asserted.

## Regularization and existence

For `0<d<1`, leave `F` and `1/t` unchanged on `t>=d`; extend each below `d`
by its quadratic Taylor polynomial at `d`, called `F_d` and `f_d`.
Both are convex C2 functions on the whole real line with globally Lipschitz
first derivatives for each fixed `d`. They are positive: below `d` each
has positive constant term, negative slope times a nonpositive displacement,
and nonnegative quadratic term. For `F_d` the quadratic coefficient is
strictly positive because `d<1`.

The regularized functional on all mean-one H1 functions is coercive by the
gradient term and Poincare's inequality. Weak compactness, strong L2 compactness,
and convex lower semicontinuity give a minimizer. Strict convexity of the
gradient norm on mean-zero differences gives uniqueness. Its Euler equation is

\[
 -2m\operatorname{div}_h[N(Dt-b)]
     +N[\epsilon f_d'(t)+V_0F_d'(t)]+\lambda=0. \tag{B1}
\]

Globally Lipschitz nonlinearity gives H2 regularity; in dimension three,
Sobolev embedding and elliptic bootstrap give enough classical regularity
to evaluate maxima/minima. No singular nonlinearity is used in this step.

## A maximum principle supplies the missing uniform multiplier bound

The mean-one constraint implies `tmax>=1`. At its maximum both regularized
functions are the original ones, `F'(tmax)>=0`, and
`div_h(N Dt)<=0`. Put `B=||div_h(Nb)||infinity`. Then (B1) implies

\[
 \lambda\le2mB+N_{\max}\|\epsilon\|_\infty. \tag{B2}
\]

At a putative minimum `tmin<=d`, convexity gives `F_d'(tmin)<=F'(d)<0`
and `f_d'(tmin)<0`, while `div_h(N Dt)>=0`. Therefore

\[
 N_{\min}V_0[-F'(d)]\le\lambda+2mB
 \le C:=4mB+N_{\max}\|\epsilon\|_\infty. \tag{B3}
\]

But `-F'(d)=2(1-d)^3(d+1)/d^3 -> infinity` as `d -> 0+`.
Choose `d` with `Nmin V0[-F'(d)]>C`. This contradicts (B3), proving
`tmin>d`. The regularized minimizer thus solves the original smooth equation.

For an explicit conservative bound, if the true minimum is at most `1/2`,
then `-F'(tmin)>=1/(4 tmin^3)`. Hence in all cases

\[
 \boxed{t_{\min}\ge
 \min\left\{\frac12,
 \left[\frac{N_{\min}V_0}{4(C+N_{\min}V_0)}\right]^{1/3}\right\}>0.} \tag{B4}
\]

The added positive term in the denominator avoids a division by zero when
`C=0`; it weakens the bound harmlessly. If `C=0` directly, (B3) at a
minimum below one is impossible, and the mean constraint forces `t=1`.

## Global minimality and the joint momentum form

On `0<t<d<1`, both functions have negative third derivative:
`(1/t)'''=-6/t^4`, `F'''=24(t-1)/t^5`. Taylor's integral remainder gives
`1/t>=f_d(t)` and `F(t)>=F_d(t)`. Thus the regularized minimizer, which
lies entirely above `d`, is also a global minimizer of the original
extended-energy functional. Gradient strict convexity yields uniqueness.
With its positive lower bound, ordinary elliptic bootstrapping gives smoothness.

At a fixed spatial point, for canonical momentum vector `p` and fixed
nonnegative excitation energy `Wexc`,

\[
 \delta^2\left[\frac{|p|^2/2+W_{\rm exc}}{t}+V_0F(t)\right]
 =\frac{|\delta p-p\delta t/t|^2}{t}
 +\left[\frac{2W_{\rm exc}}{t^3}+V_0F''(t)\right](\delta t)^2\ge0.
\]

The new vacuum term therefore preserves the perspective energy's joint
convexity, even though its quadratic curvature vanishes at `t=1`.
The coupled U/Z problem is a saddle problem, not the raw jointly convex
Hamiltonian; its separate dual analysis is required.

No H1-to-pointwise-barrier inference, continuum joint U/Z existence,
or dynamically invariant uniform lower bound has been assumed.
