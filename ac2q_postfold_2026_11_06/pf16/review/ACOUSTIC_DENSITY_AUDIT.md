# Independent audit: state-only acoustic density and BV variation

**Verdict: the density obstruction is proved as written. The smooth
variation estimate does not yet extend to the weak BV class merely by
writing its conservative gradient identity.** A specific signed-measure
renormalization/source-variation step remains to be justified.

Reviewed `pf16/ACOUSTIC_DENSITY.md`, SHA256
`98517ce62e1a4e5561644d72b3839221a7396a208b3e85aefc77d3c36fe54d7b`.
Independent delegated audit, 2026-11-06. No claim of weak nonexistence
or of a required new physical term follows from this failed shortcut.

## Exact principal coefficients

Let D_sigma=n+sigma c e, sigma=+1 or -1. At fixed A,
c^2=h/(rR). The native compact/variation estimates bound the auxiliary
rates and connection terms, so the leading terms are

    n r=-r c^2 e theta+bounded,
    n theta=-e r/r+bounded.

In an orthonormal planar frame, div n=e theta plus connection and
div e=n theta plus connection. Hence

    div D_sigma=e theta+sigma(c_r-c/r)e r+bounded.

For a positive C1 density rho(r,theta;z), all extra variables z must
have bounded n and e derivatives. Expanding D_sigma rho+rho div D_sigma
gives the two compression coefficients

    C_theta=rho-r c^2 rho_r+sigma c rho_theta,
    C_r=sigma rho(c_r-c/r)+sigma c rho_r-rho_theta/r.

The second equation C_r=0 gives

    rho_theta=sigma r c rho_r+sigma rho(r c_r-c).

Substitution into C_theta=0 cancels both density derivatives and leaves

    rho(1-c^2+r c c_r)=2 A_q rho=0.

The coefficient is strictly positive on the reviewed genuinely nonlinear
packet neighborhood. Consequently no positive density in this class can
remove both derivative terms as a universal identity. This is an algebraic
compatibility obstruction, not a failed attempt to integrate the two
equations. All r derivatives are partial derivatives at fixed A.

The extra-variable qualification is essential and appears correctly in
the actual file: bounded values of B=n beta, E_beta=e beta or metric
first derivatives do not imply bounded n/e derivatives of those objects.
Dependence on them is not covered merely by calling them local states.
Dependence on A,P and zeroth-order metric/clock coefficients is covered
under the stated bounded derivative estimates. A positive time-component
normalization of D_sigma can be absorbed into rho and therefore does
not bypass the test. The bounded-divergence scalar flux in the n direction
is a different vector field and gives no such acoustic cancellation.

## What remains meaningful for BV gradients

There is a useful distinction between a conservative gradient identity
and an absolute-value estimate. In the jump-free compact BV class, let

    z_sigma=theta+sigma I(r,A),
    W_sigma=e(z_sigma)+omega(e),
    D_sigma z_sigma+omega(D_sigma)=F_sigma.

Here omega is the connection one-form of the fixed regular conformal
frame, F_sigma is the exact bounded native Riemann source, and W_sigma
is now a scalar Radon measure rather than necessarily a function. The
first-order Riemann equation follows from the diffuse BV chain rules
and the native scalar/compatibility equations. Products with its singular
derivative use the canonical approximate values, as in the PF15 audit.

At this level a conservative identity has a direct kinematic meaning:

    div_2(D_sigma W_sigma-e F_sigma)=R_base/2.

Indeed the derivative part of its vector flux is

    D_sigma e(z_sigma)-e D_sigma(z_sigma)
       =(n tensor e-e tensor n)Dz_sigma,

where these are products of vector coefficients with derivative
measures, not a commutator acting twice on z_sigma. The sigma c terms
cancel. In conformal coordinates this is the density-corrected curl of
Dz_sigma, whose divergence vanishes. The remaining connection flux is
omega(e)n-omega(n)e and has divergence R_base/2. This argument uses no
square of a singular compression measure. The canonical BV product
convention is justified by the no-jump diffuse chain rule; it is not a
definition for arbitrary singular coefficients outside that class.

This identity alone neither proves that div(e F_sigma) is a controlled
Radon measure nor gives an inequality for |W_sigma|. A bounded F_sigma
does not, by itself, bound its spatial variation. Any needed variation
estimate from the auxiliary constraints must be established in the
actual weak class, without reusing unproved differentiated products.

## The missing step in extending Z'

The smooth Z estimate takes an absolute value/sign of the gradient
equation, controls source derivatives by variation, and integrates a
transport inequality. In the weak class W_sigma can be a signed
measure, the acoustic coefficient is BV, and the derivative of its
sign is not an available smooth test. The needed statement is a
renormalized/Kato estimate for this particular measure transport,
together with its quantitative source-variation bound. Neither is
supplied by the signed conservative identity above.

This is a real logical gap, not a notational issue. For example, with
the continuous velocity b(x)=delta sqrt(|x|), choose two different
waiting characteristics starting from zero. Each Dirac measure carried
by one characteristic solves the homogeneous continuity equation.
Their difference is a signed-measure solution with zero initial signed
measure but nonzero later total variation. Thus a general implication
from signed continuity to a zero-source absolute-value/Gronwall bound
would be false at this coefficient regularity. This example is not
native and is not asserted to satisfy the no-jump acoustic-gradient
structure; it pinpoints why that extra structure would have to be
used in a proof, rather than assuming renormalization for free.

The state-only density obstruction removes one simple way to supply
nearly-incompressible acoustic transport control. It does not exclude
a history-dependent density, a stronger native source estimate, or a
different valid renormalization/interaction theorem. Conversely the
prebreak Riccati and Z inequalities cannot be continued through a
singular derivative merely because their signed formulas admit a BV
interpretation. No postbreak existence, uniqueness or Cantor exclusion
has been obtained by this audit.

Actual gradient-note follow-up: read `pf16/GRADIENT_BALANCE.md`, SHA256
`93a9ffe8cbb1a6a689821a9276a86c6814c728df44ee614e3d523af00556366c`.
Its kinematic cancellation, interpretation of e F as a vector-field
product, curvature sign and waiting-characteristic signed-measure test
agree with the derivation above. Verdict for that exact file: proved
as the stated conservative identity and countertest of an automatic
absolute-value inference. The native renormalization/source-variation
estimate remains unproved.
