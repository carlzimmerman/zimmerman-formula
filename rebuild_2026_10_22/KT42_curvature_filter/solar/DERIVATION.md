# Curvature-only filtering: full variation and Solar observable

Let T_a be convolution with the normalized three-dimensional Gaussian of
standard deviation a, so its Fourier multiplier is exp(-a^2 k^2/2). It is
self-adjoint and commutes with constant spatial derivatives on the stated
whole-space domain. Set

\[
g=\nabla\psi,\quad H_a=T_a\nabla\nabla\psi,\quad
x=|g|^2/a_0^2,\quad s=\ell^2H_a:H_a/a_0^2,
\quad z=x+s^p,\quad E=|g|^2R(z).
\]

The Gaussian acts on the tensor before its squared norm; it does not act on
x, g, the baryonic source in the first Poisson equation, or H:H as a scalar.
The primitive R=Q/z is exactly KT39's Q(0)=0, Q'=simple nu(sqrt z).
Here p=9/8 and ell=3kpc are held fixed.

## 1. Variational return

For a fixed a, write

\[
A=(R-1+xR')g,\qquad B=p\ell^2s^{p-1}xR'H_a.
\]

Then the energy variation is

\[
\delta\int E=2\int[(g+A)\cdot\nabla\delta\psi
      +B:T_a\nabla\nabla\delta\psi].
\]

Two integrations by parts and the adjoint give the physical equation

\[
\Delta\psi=4\pi G\rho,\qquad
\boxed{\Delta\Phi=\nabla\cdot(g+A)
        -\partial_i\partial_j(T_a^*B_{ij}).}
\]

The filter is fixed rather than a field-dependent width, so there is no
additional delta T_a. Dropping the return filter is a different, nonreciprocal
equation. In the a=0 branch this is exactly KT39.

At a constant frozen jet, a real even multiplier gives the quadratic symbol

\[
\widehat{\delta\Phi}=
 \left[K(n)+\tfrac12 E_{H_aH_a}[nn,nn]k^2\sigma_a(k)^2\right]
 \widehat{\delta\psi},\quad K(n)=\tfrac12E_{gg}[n,n].
\]

The mixed first/second spatial derivative terms cancel in the real frozen
quadratic form. They must not be dropped on arbitrary varying backgrounds.
Since k^2 exp(-a^2k^2)<=1/(e a^2), this specific unbounded high-frequency
coefficient is bounded for every fixed a>0. This is not a proof of global
well-posedness, finite-wavelength stability, relativistic health, or successful
static phenomenology.

## 2. Gaussian point curvature and its scale

Use Solar r_M=sqrt(GM/a0) units, lambda=ell/r_M, alpha=a/r_M and
g=r^(-2)n+eta e_z. The smoothed unit-point Newton potential is

\[
\psi_a=-\operatorname{erf}[r/(\sqrt2\alpha)]/r,
\quad f_a=\psi_a',\quad
h_r=f_a',\quad h_t=f_a/r.
\]

Thus H_a=h_r nn+h_t(I-nn), including its finite trace inside the Gaussian
core. It is not the exterior traceless point Hessian multiplied by a scalar.
At zero,

\[
h_r(0)=h_t(0)=\frac{\sqrt{2/\pi}}{3\alpha^3},\qquad
s(0)=\frac{2\lambda^2}{3\pi\alpha^6}.
\]

In dimensional variables this is H_a(0)=sqrt(2/pi)GM I/(3a^3).
When r_M<<a the curvature screen at the ordinary Solar/external transition
therefore weakens as a^(-6p). The order-unity curvature scale is of order
[sqrt(2/(3pi)) ell r_M^2]^(1/3), about a parsec for the fixed parameters.
This scaling diagnoses the conflict; the actual quadrupole is computed below.

## 3. Move the outer filter onto the observable, not off the action

Let P_2^*=3mu^2-1 and F=P_2^*/r^3, the STF zz derivative of1/r away from
the origin. The frozen convention is q=STF zz Hessian in a0/r_M units and
Q2=(3/2)(a0/r_M)q. It is this archived signed convention whose absolute
amplitude is compared with5.2e-27 s^-2.

The B term has the exact weak pairing

\[
q_B=\frac1{4\pi}\int (T_a^*B):\nabla\nabla F
    =\frac1{4\pi}\int B:\nabla\nabla(T_a F).
\]

For alpha>0, T_a F is a smooth distributional convolution, with its origin
contact included by differentiating erf(r/(sqrt2 alpha))/r. Define

\[
t=h_t-h_r,\quad F_a=T_aF=\frac{t(r)}3P_2^*,
\quad D=p\lambda^2s^{p-1}xR'(x+s^p),
\quad d(r)=\int_{-1}^1P_2^*D\,d\mu.
\]

The identity B=DH_a yields

\[
\boxed{q_B=\frac16\int_0^\infty r^3d(r)
 [h_rt''+h_t(2t'/r-6t/r^2)]\,d\log r.}
\]

For alpha=0, h_r=-2/r^3,h_t=1/r^3,t=3/r^3, and the bracket is-108/r^8;
this becomes the independently validated KT39 expression
q_B=-18 integral d/r^5 dlogr. The h_t Laplacian contribution is essential
for alpha>0: F_a is then not harmonic inside the filter scale.

The A term retains the unfiltered Green kernel. With C=R-1+xR',

\[
b(r)=\int_{-1}^1 C[\eta(3\mu-5\mu^3)
               +r^{-2}(1-3\mu^2)]d\mu,
\qquad q_A=\frac32\int b/r\,d\log r.
\]

Both integrands subtract the angularly constant coefficient evaluated at
x0=r^(-4)+eta^2 before integration. Its angular integral is exactly zero;
the subtraction improves cancellation and does not change the equation.

## 4. Exterior point-source meaning and the finite-Sun distinction

For fixed alpha>0, H_a is finite at the origin, whereas the unfiltered Solar
g diverges. Therefore the near-origin response eventually has the ordinary
high-field limit C~1/sqrt(x). Its leading A is the radial unit vector and
produces an isotropic cusp in the anomalous potential. Expanding in
eta r^2, the quadrupolar part of A begins at order eta^2 r^4 (subleading
high-field logarithms do not lower that power). Its source begins at
order eta^2 r^3, and its particular l=2 potential at order eta^2 r^5.
The latter has vanishing STF Hessian as exterior r tends to zero. Thus the
regular r^2 l=2 coefficient is well defined despite the isotropic cusp.
The computed q_A extracts that regular exterior coefficient.

This is **not** the Hessian evaluated at r=0 in a finite Gaussian Sun and
then sent to zero source radius. The finite central Newtonian gradient is
zero, so its response sees eta rather than the divergent self-field; the
shrinking-core limit can be nonuniform. KT39's old vanishing-contact proof
used the divergent unsmoothed Hessian and cannot be imported here.

The exterior limit can instead be controlled at fixed nonzero observation
radius. Because R'<0 and x<=z,

\[
0\le C\le R-1\le2/\sqrt z,\qquad |A|\le2
\]

in these units: integrate nu(sqrt z)-1<=1/sqrt z to obtain the middle bound.
Consequently an unresolved core's A cannot generate a finite exterior
multipole by a divergent force amplitude. Its fixed-radius Green pairing
is bounded by its shrinking volume; its l=2 irregular multipole has an
additional source-radius factor. Away from that core the Gaussian-source
fields converge to the point fields. At fixed alpha>0, H_a also converges
smoothly and the filtered B test is smooth; B is bounded on each compact
region and tends to zero at the point-source origin. These facts justify
the exterior distributional limit, with separately integrable far tails.
They do not justify interchange with evaluation at the source center.

For an explicit finite-radius A check, let
a_r=integral P_2^* C(g0+eta mu)dmu for any spherical regular source and use
the corresponding b. The exact l=2 potential coefficient at radius R gives

\[
q_{A,\mathrm{eff}}(R)=
 \frac1{2R^5}\int_0^R(5a_r+3b)r^4d\log r
 +\frac32\int_R^\infty b/r\,d\log r.
\]

This includes the inner irregular multipole and involves no divergent
central contact. It approaches the point-source regular coefficient as
the source radius tends to zero and then R tends to zero. For fixed R
outside the Sun it is directly usable as a numerical regularization check.

The retained uniform external field has zero external Hessian. No actual
Galactic tidal field, Solar interior structure, ephemeris likelihood or
relativistic metric completion is claimed by this calculation.
