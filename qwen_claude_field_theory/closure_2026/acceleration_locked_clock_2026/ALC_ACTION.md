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

## Controlled aether regularisation gate

To test whether the singular preferred-frame corner can be repaired, the
repository now solves the standard constant-aether PPN equations rather than
assigning `alpha_1` and `alpha_2`.  With `c_3=r c_1` and `c_1=epsilon`,

\[
c_4=-c_3^2/c_1,
\qquad
c_2=(-2c_1^2-c_1c_3+c_3^2)/(3c_1),
\]

the PPN expressions simplify symbolically to `alpha_1=alpha_2=0` wherever
their denominators are regular.  The principal-symbol scan in
`alc_aether_regularization.py` finds regular points with `|c_13|` below
`10^-15` and positive mode speeds, but every regular point has
`c_14*c_123 != 0`, hence a nonzero aether spin-0 principal symbol.  That is
an additional gravitational scalar, so this completion fails `N_grav=2`.
The only route toward a two-tensor limit is the degenerate surface
`c_14=0` or `c_123=0`; there the PPN and speed formulae are singular and a new
full Dirac chain is mandatory.  The gate therefore sharpens the obstruction
but leaves the ALC lane **OPEN**, not certified.

## Exact-luminal ADM/Dirac follow-up

`alc_degenerate_dirac.py` evaluates the covariant aether contractions in a
local orthonormal ADM frame instead of treating the singular corner as a
formal limit.  The derived decomposition is

\[
\mathcal L_{\rm EA} = c_{13}K_{ij}K^{ij}+c_2K^2-c_{14}a_i a^i
 +(c_1-c_3)\omega_{ij}\omega^{ij}.
\]

For the hypersurface-orthogonal clock \(\omega_{ij}=0\).  Exact tensor
luminality gives \(c_{13}=0\), and the regular PPN equation \(\alpha_1=0\)
then gives \(c_{14}=0\).  A Fourier-mode variation gives

\[
L_k=c_{123}k^4\tau^2-c_{14}k^2\dot\tau^2.
\]

The actual Dirac matrix has rank 2 when \(c_{123}\ne0\): the primary
\(p_\tau=0\) is paired with a secondary and the multiplier is fixed, leaving
an instantaneous elliptic channel.  At \(c_{123}=0\) the secondary vanishes,
the quadratic Hamiltonian and Poisson rank both vanish, and the branch is
rank-degenerate/strongly coupled.  The \(k=0\) sector is separately zero at
this order.  Thus the exact-luminal regularisation does not produce a healthy
propagating-free scalar; it produces either an unacceptable instantaneous
channel or a degenerate strong-coupling corner.  This is a bounded obstruction
for the constant-aether completion, not a universal no-go for nonlocal actions.
