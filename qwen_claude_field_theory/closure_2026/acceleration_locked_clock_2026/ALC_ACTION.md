# Acceleration-locked primordial-clock action

This is a new construction lane, not a certification of the full gravity
programme.  The action is

\[
S_{\rm ALC}=\int d^4x\sqrt{-g}\left[
\frac{M^2}{2}(R-2\Lambda)
-\frac{\sigma}{2}\bigl(g^{\mu\nu}\partial_\mu T\partial_\nu T+1\bigr)
-2M^2a_0^2\,H(Z)\right]+S_m[g,\psi],
\]

with

\[
n_\mu=-\frac{\partial_\mu T}{\sqrt{-\partial T\cdot\partial T}},\qquad
a_\mu=n^\alpha\nabla_\alpha n_\mu,\qquad
Z=\frac{\sqrt{a_\mu a^\mu}}{a_0},
\]

\[
H(Z)=G(Z)-Z^2=2(1+Z)e^{-Z}-2,
\qquad G'(Z)/(2Z)=1-e^{-Z}.
\]

The scalar (T) is an explicitly counted primordial clock/matter field.  The
acceleration constitutive term contains no independent auxiliary scalar.  In
unitary gauge on a static foliation, (a_i=D_i\ln N), so it is elliptic in the
lapse rather than a propagating MOND scalar.  A full covariant khronon Dirac
analysis is still an open gate.

## Variations that are already closed

The acceleration momentum is obtained directly from the action:

\[
\Pi^\mu_a=\frac{\partial[-2M^2a_0^2H(Z)]}{\partial a_\mu}
       =4M^2e^{-Z}a^\mu.
\]

For the weak static potentials (N=1+\Phi),
\(h_{ij}=(1-2\Psi)\delta_{ij}), the varied one-dimensional density is

\[
\mathcal L_{\rm stat}=M^2(2\Psi'^2-4\Phi'\Psi')
-2M^2a_0^2[H(|\Phi'|/a_0)]-\rho\Phi.
\]

The two Euler--Lagrange equations are varied independently.  The \(\Psi\)
equation is

\[
\Phi''-\Psi''=0,
\]

so regular isolated solutions have \(\Phi=\Psi\).  Substituting this result
into the independently varied \(\Phi\) equation gives

\[
4M^2\frac{d}{dx}\left[(1-e^{-|\Phi'|/a_0})\Phi'\right]=\rho.
\]

Thus the exact exponential law is derived, not assigned, and
\(G_{\rm measured}=1/(16\pi M^2)\) in these conventions.  The subtraction
of (Z^2) is essential: it removes the Newtonian quadratic piece from the
MOND correction at (Z\gg1), leaving only the irrelevant constant
\(4M^2a_0^2).

For a homogeneous FLRW clock, (a_i=0) exactly.  The acceleration sector
therefore vanishes on the background, while the mimetic constraint and clock
equation give

\[
X=-1,\qquad \rho_T=\sigma,\quad p_T=0,\qquad
\frac{d}{dt}(a^3\sigma)=0.
\]

Consequently an expanding branch is allowed with

\[
3M^2H^2=M^2\Lambda+\rho_b+\sigma_*a^{-3}.
\]

The matter Ward identity follows from the single-metric minimal coupling:
on the matter Euler--Lagrange equations, diffeomorphism invariance gives
\(\nabla_\mu T_m^{\mu\nu}=0\).

Finally, in the transverse-traceless tensor sector \(\delta N=0\) and
\(a_i=0\), so the acceleration term contributes no tensor principal symbol.
The quadratic tensor action is the Einstein one,

\[
S_T^{(2)}=\frac{M^2}{8}\int a^3
\left[\dot\gamma_{ij}^2-c^2a^{-2}(\partial_k\gamma_{ij})^2\right]dtd^3x,
\]

with positive kinetic coefficient for (M^2>0) and (c_T=c).

## What is not yet closed

The acceleration (a_\mu) contains derivatives of the clock foliation.  The
remaining calculation is the full covariant khronon Dirac chain, including
the lapse/shift constraints away from unitary gauge, and the scalar principal
symbol on (H\ne0).  A mimetic clock has a zero-sound-speed dust limit, so
caustics/strong coupling must be tested rather than called healthy.  The
preferred-frame PPN coefficients \(\alpha_1,\alpha_2,\alpha_3\) are also not
derived by the static no-slip result.  The exact (a_0\)-\(\Lambda\) relation
is an input in this action, not a consequence.

The candidate is therefore **OPEN**.  Its value is that it puts the requested
MOND law, lensing/no-slip branch, conserved clock dust, matter Ward identity,
and luminal tensor sector in one explicit action, while making the remaining
failure modes concrete and executable.

## Clock-sector Dirac check

The local covariant-clock expansion (T=t+\tau) gives

\[
L_{\tau}^{(2)}=\frac12(\sigma_0+4M^2k^2)\dot\tau^2
 +\delta\sigma\,\dot\tau-\frac12\sigma_0k^2\tau^2.
\]

Direct Legendre transformation yields (p_{\delta\sigma}=0) and the
secondary (p_\tau-\delta\sigma=0), with a nonzero two-by-two Dirac bracket
matrix in both (k=0) and (k\ne0) sectors.  On the constraint surface
\(\dot\tau=0\): the acceleration-induced (k^2\dot\tau^2) term does not create
an additional wave, but the clock remains one explicitly counted
zero-sound-speed matter degree of freedom.  This does not settle its caustic
or metric-mixing health; those gates remain open.

## Preferred-frame and stability audit

The acceleration-only term lies at the formal Einstein--æther corner
\(c_1=c_2=c_3=0,\ c_4\ne0\).  Substitution into the standard aether PPN
expressions is singular: \(\alpha_2\) contains \(c_{123}\) in the denominator,
and \(\alpha_1\) has path-dependent limits (\(-4c_4\) if \(c_3=0\) is taken
first, versus \(-8\) if \(c_1=0\) is taken first).  Therefore ALC does **not**
claim \(\alpha_1=\alpha_2=0\); a covariant PPN calculation or a controlled
degenerate completion is mandatory.

The exact constitutive Hessian is likewise nontrivial.  Around a nonzero
acceleration background,

\[
\lambda_\perp=4M^2e^{-y},\qquad
\lambda_\parallel=4M^2(1-y)e^{-y}.
\]

The longitudinal coefficient changes sign at \(y=1\).  The mimetic secondary
can remove the associated clock velocity in the clock-only model, but only the
full metric--clock principal symbol can decide whether the sign change is a
physical gradient instability.
