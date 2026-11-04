# Static response about a uniform external field

This is a targeted static audit of the explicit KT37 action. It is not a
relativistic completion, a ghost calculation, a time-dependent stability
theorem, or an additional observational rejection criterion.

Let the background Newtonian gradient be g0=eta a0 e, with eta>0, and its
Hessian be zero. Put nu=nu_simple(eta), R=Q(eta^2)/eta^2. Derivatives of nu
in this note are with respect to eta. The dimensional energy is E=a0^2 P.
At this background, its half-gradient derivative is nu g and its
half-Hessian derivative vanishes. Their first variations are

    delta A = (U-I) grad(delta psi),
    U = nu I + eta nu' ee,
    delta B = N Hess(delta psi),
    N = ell^2 (nu-R).

The H-dependence of z starts quadratically, so it adds no mixed g/H term
at this background. The full source therefore gives

    Delta(delta Phi) = U_ij partial_ij(delta psi) - N Delta^2(delta psi).

For a nonzero Fourier vector k and cos(alpha)=k.e/|k|,

    delta Phi_hat / delta psi_hat
      = nu + eta nu' cos^2(alpha) + N |k|^2
      = nu + eta nu' cos^2(alpha) - (R-nu)(|k| ell)^2.

The plus sign before N follows by dividing both Fourier sources by -|k|^2.
It is easy to reverse this sign if the double-Hessian adjoint is omitted.

Since Q(0)=0 and Q'(z)=nu(sqrt(z)) is strictly decreasing,

    R(z) = (1/z) integral_0^z Q'(t) dt > Q'(z) = nu(sqrt(z)).

Thus N<0 for every finite eta>0. For simple nu, both eigenvalues of U
are positive: nu>0 and nu+eta nu'>0. For each orientation the static
transfer changes sign at

    kcrit ell = sqrt[(nu+eta nu' cos^2(alpha))/(R-nu)].

The derivation was independently checked from the dimensional action, rather
than inferred from the Milky Way or dwarf results. The numerical companion
uses a small sinusoidal potential, evaluates the unmodified A and B API at
positive and negative amplitudes, and independently extracts their sine and
cosine Fourier coefficients. It does not obtain the measured answer by
substituting the transfer formula into itself.

| eta | nu | R-nu | kcrit ell, perpendicular | kcrit ell, parallel | critical wavelength/ell, perpendicular | critical wavelength/ell, parallel |
| --- | --- | --- | --- | --- | --- | --- |
| 2.48 | 1.3082238591 | 0.1817104063 | 2.6831881855 | 2.4138558667 | 2.3416864091 | 2.6029662308 |
| 2.05 | 1.3589556904 | 0.2044432181 | 2.5781981594 | 2.2930766071 | 2.4370451449 | 2.7400677708 |

These eta values are the two prescribed Solar external-field ratios. They
do not represent a spatially constant model of the actual Galactic disc.
At ell=3 kpc the corresponding critical wavelengths range from about
7.03 to 8.22 kpc. This is therefore not intrinsically confined to microscopic
wavelengths. Applying that estimate inside an inhomogeneous galaxy requires
checking the constant-background and weak-perturbation assumptions.

With the Newtonian relation delta psi_hat=-4 pi G delta rho_hat/|k|^2,
the N term contributes a local potential

    delta Phi_local = 4 pi G ell^2 (R-nu) delta rho.

Its force points down the density gradient, away from a small density peak.
This is the precise sense in which the infinitesimal short-wave static
response is repulsive. In a separately specified Jeans/fluid model it could
act as an additional positive pressure coefficient, rather than imply an
instability. The KT37 static action does not itself specify such matter
dynamics or a relativistic kinetic sector, so no ghost or full dynamical
stability conclusion follows from this sign.

The linearization requires |delta g|<<eta a0 and
ell ||delta H||<<eta a0. The Hessian condition is essential. The large-k
formula does not authorize applying a weak-field expansion to a point mass
or to the interior of a compact body. For each finite Fourier mode one can
take the amplitude sufficiently small; the sign change is then a genuine
property of the continuum linear response, not a discretization artifact.

The unsuppressed local density term also makes the interpretation of fine
structure consequential. Smooth-density predictions, a regularized body
limit and a collection of finite bodies need not be interchangeable under
this nonlinear action. No particular coarse-graining prescription or extra
cutoff is added here. The Gaussian Solar regularization analysis establishes
one specified STF observable limit; it does not settle that general issue.

Limits must be ordered. For fixed k, ell->0 recovers ordinary linearized
simple QUMOND. For any fixed ell>0, sufficiently large k changes the sign.
At fixed k ell, eta->infinity gives nu->1 and R-nu->0, hence the Newtonian
limit; this is not uniform in arbitrarily large k. In the deep-field limit,
R-nu~(1/3)eta^-1/2 and U~eta^-1/2(1-cos^2(alpha)/2), so kcrit ell tends to
sqrt[3(1-cos^2(alpha)/2)]. The expansion at eta=0 itself is singular and
is excluded by the stated background hypothesis.

Finite computational coverage: eta in {2.48,2.05}, cos^2(alpha) in
{0,1/2,1}, k/kcrit in {1/2,1,2}, and three perturbation amplitudes
{1e-4,1e-5,1e-6}, with a 512-phase periodic quadrature. This is 54 checks,
not a numerical proof over every background or wavelength.
