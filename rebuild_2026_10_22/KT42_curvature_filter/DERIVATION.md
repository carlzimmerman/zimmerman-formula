# Curvature-only smoothing: action and what it can repair

Let psi solve Delta psi=4 pi G rho. Define g=grad psi and
Hbar=Hess(T_a psi), where T_a=exp(a^2 Delta/2) is an isotropic fixed spatial
Gaussian on R^3. Thus Hbar=T_a Hess psi in Cartesian coordinates. Componentwise
smoothing of spherical orthonormal tensor entries would be a different,
noncovariant operation and is not used.

Keep the KT39 primitive Q and R=Q/z, Q(0)=0,
Q'(z)=1/2+sqrt(1/4+1/sqrt(z)). Put

\[
x=|g|^2/a_0^2,\quad s=\ell^2\bar H:\bar H/a_0^2,
\quad z=x+s^p,\quad E=|g|^2R(z).
\]

The nonrelativistic action retains the two-potential term
−[2 grad Phi.grad psi−E]/(8 pi G) and matter coupling −rho Phi.
For the fixed filter, its full variation gives

\[
\Delta\Phi=\Delta\psi+\nabla\cdot A
 -T_a^*\partial_i\partial_j B_{ij},
\quad A=(R-1+xR')g,
\quad B=p\ell^2s^{p-1}xR'\bar H.
\]

The adjoint cannot be omitted. On R^3, it equals T_a and commutes with
derivatives; the order still matters in a discrete representation. The MW
energy uses H_h T_h psi exactly, so its derivative returns T_h* H_h*.
If W denotes cell volume, the implemented source is
−W^-1 G_h^T W A−T_h* W^-1 H_h^T W B, including the factor2 for the mixed
orthonormal Hessian entry. The heat adjoint is evaluated using transpose LU
solves with W rather than assumed from approximate commutation.

For a constant frozen background and real even Fourier multiplier sigma_a,
the odd gradient-Hessian cross terms cancel in the real quadratic energy.
With K(n)=E_gg[n,n]/2 and N(n)=E_HH[nn,nn]/2, the static response is

\[
\widehat{\delta\Phi}=
 [K(n)+N(n)k^2e^{-a^2k^2}]\widehat{\delta\psi}.
\]

Consequently the cold-fluid expression is
omega^2=−4 pi G rho [K+N k^2 exp(−a^2k^2)]. Since
max k^2 exp(−a^2k^2)=1/(e a^2), the particular unbounded KT40 growth
as k tends to infinity is removed for a>0 and finite K,N. This is bounded
growth, not absence of growth or a nonlinear/all-background stability result.
For finite sound speed add c_s^2 k^2. Variable backgrounds, kinetic matter
and any relativistic realization need separate analyses.

The physical tradeoff is explicit. Increasing a averages away the sharp
curvature gradients that generate KT40's outward force and repulsive dwarf
stress. It also averages away the Sun's curvature that screened its external
field. The full MW force, dwarf virial and exterior Solar quadrupole test
whether those demands can coexist. A finite grid of widths can find a
counterexample or survivor; it cannot certify absence of an unsampled window.

This is a declared phenomenological extension with p=9/8, ell=3kpc and one new
trial scale a. Neither those constants nor a covariant completion are derived.
Higher-derivative generalized QUMOND is prior architecture, not a new claim
here: Milgrom, Generalizations of Quasilinear MOND (2023),
https://arxiv.org/abs/2305.01589v2. The present local search concerns the exact
curvature-only filtered functional, not priority over that literature.
