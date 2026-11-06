# Independent audit: coercive differentiated auxiliary constraints

**Primary verdict: proved as written for the flat on-branch periodic
clock-slice system, with the positivity and compactness assumptions below.**
The rescaling removes the large diagonal n(theta) terms exactly. The
periodic inverse has a derivative-free coercive estimate. This materially
improves the earlier transfer analysis, but does not by itself prove a
Riccati inequality or full coupled formation.

## 1. Exact rescaling and signs

Use r=sqrt(2X), h=H_r, R=H_rr, and

    D=(Ar-1-gamma r^2)/gamma,
    D_r=(A-2gamma r)/gamma,
    R=1+gamma D_r^2-2gamma D.

In the flat, source-free on-branch subsystem,

    e(A)=W_P/r, e(P)=D, n(theta)=-e(r)/r,
    R n(r)+r D_r n(A)+(W_P/r)n(P)+h e(theta)=0.

Define u=n(A)/r and v=n(P)/r. The commutator is
[n,e]=(n theta)n-(e theta)e. Differentiating the two spatial constraints
and substituting the rescaled variables cancels the n(theta) terms and
gives, before eliminating n(r),

    e(u)=(W_PP/r)v-(W_P/r^3)n(r)+(W_P/r^2)e(theta),
    e(v)=(D_r/r)n(r)+(r/gamma)u+(D/r)e(theta).

The scalar equation gives

    n(r)=-(r^2 D_r u+W_P v+h e(theta))/R.

Consequently the proposed system is exactly

    e(u)=a u+b v+f e(theta),
    e(v)=c u-a v+g e(theta),

with

    a=W_P D_r/(rR),
    b=W_PP/r+W_P^2/(r^3 R),
    c=r/gamma-r D_r^2/R=r(1-2gamma D)/(gamma R),
    f=(W_P/r^2)(1+h/(rR)),
    g=D/r-D_r h/(rR).

There is no missing gamma factor. The opposite diagonal signs are exact.

Require gamma>0, r>0, W_PP>0 and 1-2gamma D>0. Then R>0 and b,c>0.
For estimates uniform over a family, require compact state bounds and
uniform margins so b,c>=m>0 and |a|+b+c is bounded. Cap separation controls
the upper bound of W_PP for the native hold law. Hyperbolicity of the
matter characteristic additionally needs h>0; it is not supplied merely
by this auxiliary coercivity calculation.

## 2. Correct periodic integration

The identity is

    e(uv)=c u^2+b v^2+(g u+f v)e(theta).

Integrate on a closed **clock slice** using proper arclength ell, so
e=partial_ell and the endpoint values match periodically. One cannot
replace this by a fixed-coordinate-time integral without accounting
for the changed slice and measure.

For homogeneous forcing, periodicity yields

    integral (c u^2+b v^2) d ell=0,

so u=v=0. Thus the periodic homogeneous inverse has no kernel even for
rapidly varying coefficients. No coefficient derivative enters this
argument. For smooth periodic coefficients, the finite-dimensional
monodromy boundary problem then has an inverse: absence of a periodic
kernel means its boundary matrix is invertible.

## 3. Uniform inverse bounds without coefficient derivatives

Let y=(u,v), Bmat=[[a,b],[c,-a]], and

    L y=y'-Bmat y=F theta', F=(f,g), prime=partial_ell.

More generally take forcing q. Multiplication by the constant swap matrix
J=[[0,1],[1,0]] and integration gives

    integral y^T J L y=-integral(c u^2+b v^2).

Therefore ||L^(-1)q||_2<=||q||_2/m. The adjoint
L*=-partial_ell-Bmat^T has the analogous identity with b,c interchanged,
so the same L2 estimate holds. From z'= -Bmat^T z-q for the adjoint,
its H1 norm is controlled using only m, ||Bmat||_infinity and slice
length, with no derivative of Bmat. The elementary one-dimensional
bound

    ||z||_infinity<=length^(-1/2)||z||_2+sqrt(length)||z'||_2

and duality give an L1-to-L2 bound for L^(-1). Finally
y'=Bmat y+q gives a bounded-variation bound and hence

    ||L^(-1)q||_infinity<=C ||q||_1.

The constants depend on the positive margins, coefficient upper bound,
and slice length. Length must remain in a fixed controlled range for a
uniform assertion; shrinking the entire periodic domain can reintroduce
a low-mode factor. These estimates are useful for smooth forcing and
its controlled measure approximations, not just for Fourier modes.

The immediate consequence is ||(u,v)||_infinity<=C TV(theta). This is
independent of pointwise coefficient derivatives but can still grow with
the number of oscillations.

## 4. Improved amplitude/BV estimate and low modes

Fix a constant vector F0 in the coefficient range and choose a constant
theta0 so ||theta-theta0||_infinity is bounded by its oscillation. Split
F=F0+(F-F0), and write y=F0(theta-theta0)+z. Then

    L z=Bmat F0(theta-theta0)+(F-F0)theta'.

Applying the L1-to-Linfinity estimate gives

    ||(u,v)||_infinity
      <=C[osc(theta)+||F-F0||_infinity TV(theta)].

On a fixed compact state domain, smoothness of F bounds its oscillation
by the state amplitude. This is stronger than treating the auxiliary
low modes as arbitrary order-k forcing. In particular

    |integral f d theta|<=osc(f) TV(theta),
    |integral g d theta|<=osc(g) TV(theta),

because the constant parts integrate to zero on the periodic clock slice.
The proposed mean-forcing observation is correct. It is not an estimate
of the mean forcing independent of amplitude times total variation:
on a fixed domain with k oscillations, amplitude delta gives
TV(theta)=O(delta k), so this bound contains O(delta^2 k).

Near the homogeneous P=0 background, f=0 at the base point whereas g
generally does not vanish. The displayed system then also shows why
u's spatial derivative can be better controlled than a naive derivative
of the original unscaled inverse: e(u)=a u+b v+f e(theta). This structure
should be used, not replaced by a generic coefficient-gradient bound.

## 5. What this contributes to formation, and what it does not

A potentially useful high-frequency scaling is delta=k^(-1/2) on a fixed
periodic domain. The amplitude/BV bound then allows O(1) auxiliary
temporal rates while the compressive matter gradient is O(sqrt(k)).
If a bootstrap also keeps state oscillations O(delta), TV(theta)=O(sqrt(k)),
and the relevant spatial derivative of the auxiliary source subquadratic
in compression, this separation could support the desired Riccati
transfer. These are conditional consequences, not established evolution
bounds.

In particular this lemma does not yet control:

* persistence of the amplitude/total-variation bootstrap until the
  purported first singularity;
* opposite-family characteristic gradients and their feedback;
* the spatial derivative of every term in the characteristic source,
  including the r-dependent coefficients multiplying u and v;
* curved-frame spin connection, transverse expansion, moving clock-slice
  length, and full Einstein constraint compatibility;
* loss of the clock, cap, hyperbolicity or positive-denominator margins.

The earlier review's description of the nonlinear inverse as an unchecked
step must therefore be refined: **this periodic flat inverse now has a
proved coercive amplitude/BV estimate without coefficient-derivative
loss.** The remaining task is to propagate its hypotheses and convert it
into the full characteristic differentiated bound, rather than merely
to assert invertibility. Neither prebreak asymptotic convergence nor this
inverse lemma alone transfers a shock time to the full coupled system.

## Audit verdicts and provenance

| Obligation | Status |
| --- | --- |
| Rescaling cancellation and all coefficients | passed |
| R identity and b,c positivity | passed with uniform denominator/clock/cap margins |
| Periodic kernel exclusion | passed on closed clock slices |
| Inverse bounds without coefficient derivatives | passed with controlled length and coefficient bounds |
| Constant-part subtraction in mean forcing | passed |
| Full native Riccati transfer or formation | not established |

Independent delegated analytic review, 2026-11-06. Direct differentiation,
commutator calculation, and elementary energy/duality estimates; no
numerical experiment or external formation theorem used. This file adds
new evidence to principal_review/REVIEW.md without rewriting its earlier
chronological audit.
