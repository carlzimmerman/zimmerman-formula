# Energy conserving memory stress for X48

This is a constructed Newtonian material law with additional density and time
scales, not a derived relativistic dark-energy theory. It replaces direct
dependence of pressure on gravitational acceleration with an independent
entropy memory. The prior instantaneous-gradient obstruction is retained in
`../gravitational_strain/`; it is not inherited by the changed equations.

## Material law and exact quiet domain

Let `rho_q>0` be a fixed physical material density, `tau>0` a compression time,
and `a0,G>0` fixed inputs over the experiment. Define

\[
 P_0=\frac{a_0^2}{8\pi G},\qquad K_*=\frac{P_0}{\rho_q^2},\qquad
 d=\rho/\rho_q,\quad z=d-1,
\]
\[
 h(d)=\begin{cases}
 0&d\le1,\\
 3z^2-2z^3&1<d<2,\\
 1&d\ge2,
 \end{cases}\qquad
 W(\rho)=\begin{cases}
 \tfrac32\rho_q&d\le1,\\
 \rho_q(\tfrac32+z^3-\tfrac12z^4)&1<d<2,\\
 \rho&d\ge2.
 \end{cases}
\]

The independent memory `K>=0` is advected when heating is inactive. Choose
specific internal energy and isotropic equilibrium stress

\[
 e(\rho,K)=KW(\rho),\qquad
 P=\rho^2\left.\partial_\rho e\right|_K
   =K\rho^2h(d)
   =P_0\frac{K}{K_*}d^2h(d).
\]

Thus equal densities need not have equal pressure. The model is nonbarotropic
even though each constant-K equilibrium branch is barotropic. Since `W'=h`,
previously heated gas retains dormant specific energy `3K rho_q/2` when it
expands below the gate, while its pressure vanishes exactly. Removing that
energy by simply resetting K would break the proposed energy balance.

With `theta=div v` and `C=max(-theta,0)`, take compressive bulk stress and
memory production

\[
 q=K_*\rho W h(d)(\tau C-1)_+\ge0,\qquad
 D_tK=K_*h(d)C(\tau C-1)_+\ge0.
\]

Mass and momentum obey

\[
 D_t\rho=-\rho\theta,\qquad
 \rho D_tv=-\nabla(P+q)-\rho\nabla\Phi,
 \qquad\nabla^2\Phi=4\pi G(\rho+\rho_b).
\]

This is a bulk viscosity regularization in the Newtonian setting. It is not
a relativistic causal transport law. The displayed isolated-core gravity
omits the cosmological Lambda term; production X48 background evolution is
not an input to the static tests. The same stress that removes mechanical
energy supplies the memory energy:

\[
 \rho W D_tK=qC,\qquad
 \rho D_te=-P\theta+qC=-(P+q)\theta.
\]

Consequently kinetic, internal and self-gravitational energy balance exactly
for smooth isolated solutions, with boundary work accounted for. A prescribed
time-dependent baryon potential adds the external work
`integral rho partial_t Phi_b dV`; it is not an isolated energy invariant.

The exact quiet statement is

\[
 \rho\le\rho_q\quad\Longrightarrow\quad P=q=D_tK=0
 \quad\hbox{for every prior }K.
\]

Also, virgin `K=0` material remains exactly stress-free whenever `tau C<=1`,
even above the density gate. Homogeneous expansion has `C=0`; its zero-K
background and a sufficiently small perturbation are exactly cold. Whether
the observed forest remains within these domains requires a field/history
distribution calculation. No observed forest exclusion or likelihood is
inferred merely from the gate. Making `rho_q` follow the cosmic mean or making
`a0` explicitly time dependent would add constitutive work; that changed law
requires additional energy bookkeeping.

## Thermodynamic and short wavelength stability

Use an entropy coordinate `s>=0` with `K=K_*(s/s_*)^3`. At `s>0`, temperature
`T=e_s` is positive and `rho T D_t s=qC>=0`. At the initially cold boundary
use K as the evolution variable; dividing by its zero temperature is not a
regular way to initialize an entropy equation.

Write `v_spec=1/rho`. Since `0<=h<=1`, `h'_rho>=0`, and `W>=rho`,

\[
 W_v=-\rho^2h,\quad W_{vv}=2\rho^3h+\rho^4h'_\rho,\quad
 WW_{vv}\ge2W_v^2.
\]

For the cubic entropy coordinate the energy Hessian in `(s,v_spec)` is
positive semidefinite: its determinant is a positive factor times
`2 W W_vv - 3 W_v^2 >= W_v^2`. The quiet branch is mechanically degenerate;
the finite-entropy active branch has positive compressibility.

On an unheated local equilibrium the acoustic coefficient is

\[
 c_s^2=P_\rho|_K=K(2\rho h+\rho^2h'_\rho)\ge0.
\]

Locally uniform coefficients give the ordinary acoustic/Jeans relation
`omega^2=c_s^2 k^2-4 pi G rho`, plus neutral entropy and transverse modes.
Jeans growth in the exactly cold branch is bounded as wavenumber increases;
there is no negative-compressibility ultraviolet growth from differentiating
the gravitational field. This modal statement does not imply strong
hyperbolicity or a uniform same-Sobolev estimate: without gravity,
`delta rho(t)=delta rho(0)-i rho k dot delta v(0) t` already has a
wavenumber-dependent propagator. The cold single-stream fluid can still form
caustics; its kinetic/multistream completion is not supplied by a zero pressure.

During active compression `q_C/rho>0` supplies positive longitudinal viscous
damping. Freezing coefficients, writing `B=P_K` and `F=D_tK`, the leading
longitudinal polynomial is

\[
 \lambda^3+\frac{q_C}{\rho}k^2\lambda^2+
 (P_\rho+q_\rho+BF_C/\rho)k^2\lambda+BF_\rho k^2=0.
\]

All displayed coefficients are nonnegative; the Routh condition holds at
sufficiently large k. In the dense branch `F_rho=0`, leaving a neutral memory
mode and damped acoustic modes. This is a principal-symbol check, not stability
of an arbitrary evolving halo or of all finite-wavelength source modes.
Convective stability also needs a nondecreasing radial K profile; constant K
is neutrally buoyant. Positive entropy production alone does not order K.

## Finite cores and their radial stability

Fix `K>0` and a smooth nonnegative spherical baryon density of finite central
value. Set

\[
 H(\rho)=\int_{\rho_q}^{\rho}\frac{P_s}{s}\,ds,
 \qquad H'=-g,\quad m'=4\pi r^2\rho,
 \quad g=G[m+M_b(r)]/r^2 .
\]

Every finite `rho_c>rho_q` has a regular central branch. With
`c_c^2=P_rho(rho_c)>0`,

\[
 \rho(r)=\rho_c-
 \frac{2\pi G\rho_c[\rho_c+\rho_b(0)]}{3c_c^2}r^2+O(r^4).
\]

The core is finite and has zero central logarithmic slope. Since the occupied
interior has `rho>=rho_q`,

\[
 H(r)\le H_c-\frac{2\pi G\rho_q}3r^2,
 \qquad R\le\sqrt{\frac{3H_c}{2\pi G\rho_q}}<\infty.
\]

It reaches a pressure-free surface of density `rho_q` and can be matched to
vacuum. The density falls discontinuously to vacuum; this is a self-bound
fluid sphere, not a demonstrated diffuse halo envelope. A pressureless
nonzero atmosphere cannot be a static continuation.

For adiabatic radial displacements `xi=r eta`, `Delta K=0`, define
`D=r eta'+3 eta`, `A=rho P_rho`, and
`I=integral_0^R rho r^4 eta^2 dr`. Impose regularity at the center and physical
free traction `Delta P=-AD ->0` at the outer surface, with bounded eta. The
radial pulsation equation gives the exact quadratic identity

\[
 \begin{split}
 \omega^2 I={}&\int_0^R2Pr^4\eta'^2\,dr
 +\int_0^R(A-2P)r^2D^2\,dr\\
 &+\int_0^R(2\rho g r^3+4\pi G\rho\rho_b r^4)\eta^2\,dr.
 \end{split}
\]

Here `A=2P+K rho^2 d h'(d)>=2P`, and `g/r>=4 pi G rho_q/3`. Therefore

\[
 \boxed{\omega^2\ge 8\pi G\rho_q/3>0}
\]

for every admissible radial normal mode. This is a positive radial gap under
fixed baryons. Near the surface, with `s=R-r`,

\[
 \rho-\rho_q=\sqrt{\frac{\rho_qg_R}{3K}}\sqrt{s}+O(s),\quad
 P=\rho_qg_Rs+O(s^{3/2}),\quad
 A=2\sqrt{3K\rho_q^3g_R}\sqrt{s}+O(s).
\]

These behaviors make the integrals finite. The condition `A->0` alone does
not impose free traction: a displacement with an added `sqrt(s)` term can
have finite quadratic energy but nonzero limiting `AD`. The physical boundary
condition is essential. Nonradial interface modes, responsive baryons and
global nonlinear stability are separate questions.

## Baryon response and the role of a0

Where `rho>=2rho_q`, the law is exactly `P=K rho^2`, giving

\[
 2K\rho+\Phi=\mathrm{constant},\qquad
 \nabla^2\rho+\frac{2\pi G}{K}\rho=-\frac{2\pi G}{K}\rho_b.
\]

For a baryon-free dense interior this is the n=1 sinc core with scale
`a=sqrt(K/(2 pi G))`. Its formal full-polytrope radius is

\[
 R_1=\pi a=\frac{a_0}{4G\rho_q}\sqrt{K/K_*}.
\]

The actual solution joins the transition layer before that formal zero.
The acceleration sets the constitutive stress normalization; `rho_q` and the
generated memory set the core scale. No universal core pressure or surface
density has been derived from a0 alone.

Smooth finite-depth baryons compress the core while preserving a regular
center. For a point mass the same high-density law instead gives
`rho ~ G M_b/(2K r)`: no uniform finite-core bound survives arbitrary baryon
compactification. The numerical experiment therefore measures resistance
under specified Plummer loading, not immunity to baryons or a rotating-disc
prediction.

## Relation to primary literature

[Rein 2002, sections 2--3](https://arxiv.org/html/math-ph/0210045v1)
constructs isolated barotropic Euler-Poisson energy minimizers, including
polytropes with gamma>4/3, and gives conditional nonlinear stability while a
mass/energy preserving evolution exists. It does not supply the density gate,
entropy production, or an unconditional theorem for this free-boundary law.

[Dawoodbhoy, Shapiro and Rindler-Daller 2021](https://academic.oup.com/mnras/article/506/2/2418/6313304)
forms n=1 cores in spherical collapse with a rho-squared self-interaction
pressure and a separate dispersion-supported envelope. That supports the
dense-core ingredient; it does not establish this new material law or its
forest behavior.

[Chavanis 2019, appendix I](https://arxiv.org/html/1909.04709v1)
gives the exact gamma=2 Thomas-Fermi point-mass cusp. That limit agrees with
the direct enthalpy argument above and prevents an unrestricted claim about
baryon resistance. These checks establish adjacent results and limitations,
not novelty or observational validation of this construction.
