# An exact spectral completion of the rational law, and its missing particle dictionary

19 October 2026. Owner: `rational_completion`. Mathematical parent:
`CE-PARTICLE-2026-10-18 / CE-FM-085`; requested initial Git revision:
`9516ee01c79f35c04b7556050669ba77b0c98b99`. The repository changed concurrently;
`source_pins.json` fixes the source bytes used here. This lane writes only below
`sol61_push/gravity_restoring_2026_10_19/rational_completion/`.

**Result.** A positive continuum of independently saturating quantum dipoles
produces the complete rational constitutive function exactly. Its required
dipole-weighted distribution of reduced gaps is

\[
 w(\Delta)=p_{\rm sat}\frac{a\Delta}{(a^2+\Delta^2)^{3/2}},\qquad
 0\leq\Delta<\infty.
\]

This distribution is unique within the stated locally integrable spectral
class. An isotropic ensemble of fixed-axis dipoles has a different, also
positive, explicitly derived distribution. Both constructions require an
actual local dipole source, arbitrarily soft gaps, and an unbounded tail of
reduced gaps. The original canonical charge-one/charge-two particle action
has not supplied these ingredients. In a coincident fixed-charge cell,
uniform Newtonian gravity couples to the conserved charge at leading NR
order; a constant lapse redshifts the complete internal Hamiltonian. Neither
probe changes its conversion populations. Thus this is an exact **conditional
completion template**, not a derivation of the target from that particle
action, nor an independent prediction of \(a_0\) or Newton's constant.

## 1. Target, source, and normalization

Write \(K=4\pi G\), \(a=a_0>0\), \(p=|\mathbf P|\), and \(u=Kp<a\).
The target material energy and its convex dual are

\[
 W(p)=\frac{-aKp-a^2\log(1-Kp/a)}K,
 \qquad
 F(E)=\frac{aE-a^2\log(1+E/a)}K,\qquad E\geq0.
\]

The source convention is a matter Hamiltonian density
\(H(E)=H_0-\mathbf E\cdot\mathbf P\). Its ground-state energy lowering is
\(F(E)=e(0)-e(E)\); hence \(p=F_E\), with \(\mathbf P\) parallel to
\(\mathbf E\). The material Legendre transform is
\(W(p)=\sup_{E\geq0}[Ep-F(E)]\). In particular,

\[
 p(E)=p_{\rm sat}\frac E{a+E},\qquad
 p_{\rm sat}=\frac aK,\qquad
 E(p)=\frac{aKp}{a-Kp}.
\]

These equations distinguish the external conjugate field \(E\), the material
polarization \(p\), and \(u=Kp\). The derivative of the material energy is
\(W_p=E=au/(a-u)\), while the derivative after subtracting the gravitational
quadratic is

\[
 \left(W-\frac K2p^2\right)_p
 =E-Kp=\frac{u^2}{a-u},\qquad
 W-\frac K2p^2=\frac{K^2p^3}{3a}+O(p^4).
\]

The ensemble below first has two independent constants \(a\) and
\(p_{\rm sat}\). Setting \(p_{\rm sat}=a/K\) gives this target and its
quadratic coefficient. The spectrum alone does **not** derive that relation:
it is an additional calibration of total dipole inventory against gravity.
All formulas are in natural units except for the displayed \(G\).

## 2. What finite source inventory actually does in the original action

The original regulated positive-frequency Hamiltonian, in a homogeneous
unit-volume two-mode reduction, is

\[
 H=mQ+\delta b^\dagger b+c_3(b^\dagger a^2+a^{\dagger2}b)
       +k_c a^{\dagger2}a^2,
 \quad Q=a^\dagger a+2b^\dagger b,
 \quad \delta=M-2m>0.
\]

Here \(c_3=g/(2m\sqrt{2M})\) and \(k_c=\lambda_{\rm tot}/(4m^2)\)
in the convention pinned from the parent calculation. This is the stated
regulated RWA Hamiltonian; its finite matching correction is discussed in
the parent's `micro_response/DERIVATION.md`. The correction does not alter
the uniform-gravity operator argument.

In a fixed \(Q\) sector use the complete basis
\(j=n_b=0,\ldots,\lfloor Q/2\rfloor\), \(n_a=Q-2j\). The excess
Hamiltonian is the finite tridiagonal matrix

\[
 H_{jj}=\delta j+k_c(Q-2j)(Q-2j-1),\quad
 H_{j,j+1}=c_3\sqrt{(j+1)(Q-2j)(Q-2j-1)}.
\]

The leading NR gravitational mass is \(mQ\), not \(mn_a\) with the
source stock omitted. Therefore a spatially constant external Newtonian
potential adds \(m\Phi_NQ\mathbf1\). It shifts every energy equally and
changes no eigenvector or conversion occupation in that sector. A constant
lapse at fixed proper cell geometry instead gives
\(H(N)=N H_{\rm proper}\), including detuning, conversion, contact,
and rest energy. Again the zero-temperature eigenvectors do not change.
Using only \(M\Phi_Nn_b+m\Phi_Nn_a\), while failing to redshift the
conversion and binding energy at the same order, is not this complete
constant-lapse source.

A distinct spatially varying gravity probe can project to a differential
term \(h j\), where, at leading rest order,
\(h=2m[\langle\Phi_N\rangle_b-\langle\Phi_N\rangle_a]\).
Such a projection requires independently established spatial mode profiles,
their boundaries/support, and control of omitted modes. It is not a new
coupling in the action, but it is also not a uniform internal gravitational
dipole of an isolated coincident composite. For a freely falling isolated
positive-mass composite, uniform acceleration couples to its center of mass;
internal tidal probes involve curvature rather than \(|\nabla\Phi_N|\).
These source restrictions are independently developed in the sibling
`internal_polarization` lane.

For \(Q=2\), the differential-probe matrix is exactly

\[
 H_2(h)=\begin{pmatrix}2k_c&\sqrt2c_3\\
                  \sqrt2c_3&\delta+h\end{pmatrix},\qquad
 D=\delta+h-2k_c,\quad t=\sqrt2c_3.
\]

Its lower energy and source occupation are

\[
 \epsilon_-(h)=\frac{2k_c+\delta+h-\sqrt{D^2+4t^2}}2,\qquad
 n_b(h)=\partial_h\epsilon_-=
 \frac12\left(1-\frac D{\sqrt{D^2+4t^2}}\right).
\]

This is square-root saturation, not the requested rational law. For a
favorable \(h=-dE\), \(1-n_b\sim t^2/(dE)^2\). Centering the avoided
crossing requires the extra tuning \(\delta-2k_c=0\), and still gives
\(p\propto E/\sqrt{E^2+\Delta^2}\). Finite total constituent number
places a ceiling on conversion; it does not fix the approach to that ceiling.

There is a stronger finite-dimensional obstruction that does not assume a
gap at \(E=0\). Let \(H(E)=H_0-ED\) on a finite-dimensional Hilbert space,
with \(d_*\) the largest eigenvalue of the Hermitian source \(D\). The
variational principle gives, for \(E\geq0\),

\[
 \lambda_{\min}(H_0)\leq e(E)+Ed_*
 \leq\min_{v\in\ker(D-d_*),\|v\|=1}\langle v,H_0v\rangle.
\]

The middle quantity remains bounded. For the exact target it would grow as
\(p_{\rm sat}a\log(1+E/a)\), which is unbounded. Thus no finite inventory
with finitely many retained internal states and an ordinary linear source
has this exact ground-state energy. This does not exclude an infinite
spatial Hilbert space at fixed particle number, a thermodynamic continuum,
or a singular state limit.

## 3. Exact zero-temperature continuum construction

Consider an explicitly different microscopic model: independent quantum
two-level dipoles with local Hamiltonian

\[
 H_\Delta(E)=d\,[\Delta\mathbf1+\Delta\sigma_x-E\sigma_z],
 \qquad d>0,\quad\Delta\geq0.
\]

The identity term fixes each zero-field ground energy to zero before taking
the continuum. The source operator is the dipole \(d\sigma_z\). A physical mass dipole
would have \(d=m\ell\) for a supported two-position degree of freedom
with displacements \(\pm\ell\). Neither this support nor such an internal
degree of freedom is supplied by the original scalar action. The zero-field
energy splitting is \(2d\Delta\); consequently \(\Delta\) is a **reduced
gap in field units**, not the raw excitation energy. Its exact ground-state
lowering and response are

\[
 F_\Delta=d[\sqrt{\Delta^2+E^2}-\Delta],\qquad
 p_\Delta=d\frac E{\sqrt{\Delta^2+E^2}}.
\]

Let \(w(\Delta)d\Delta\) be dipole magnitude per physical volume in that
reduced-gap interval. This is an occupied, dipole-weighted distribution,
not a count of available modes. A continuous \(w\) describes a thermodynamic
or disorder-averaged population at finite number density. It is distinct
from an exact finite-\(Q\) cell with finitely many two-state sites; a finite
sample has discrete realized gaps and sample-dependent extremes. For the
positive density stated at the start,

\[
 \int_0^\infty w(\Delta)d\Delta=p_{\rm sat},\qquad
 \int_0^\infty\frac{w(\Delta)}\Delta d\Delta=\frac{p_{\rm sat}}a.
\]

The response integral is elementary. For \(E\ne a\),

\[
 \frac d{d\Delta}\sqrt{\frac{\Delta^2+E^2}{\Delta^2+a^2}}
 =\frac{(a^2-E^2)\Delta}
 {(\Delta^2+a^2)^{3/2}\sqrt{\Delta^2+E^2}}.
\]

Its endpoints are \(E/a\) and \(1\), so

\[
 \int_0^\infty\frac{a\Delta\,d\Delta}
 {(a^2+\Delta^2)^{3/2}\sqrt{\Delta^2+E^2}}
 =\frac a{a^2-E^2}\left(1-\frac Ea\right)=\frac1{a+E}.
\]

At \(E=a\), direct integration gives \(1/(2a)\), the removable limit.
Thus

\[
 p(E)=\int_0^\infty w(\Delta)\frac E{\sqrt{\Delta^2+E^2}}d\Delta
 =p_{\rm sat}\frac E{a+E}.
\]

The ground-state lowering integral converges absolutely: the integrand
\(w(\Delta)[\sqrt{\Delta^2+E^2}-\Delta]\) is bounded at zero and
is \(O(\Delta^{-3})\) at infinity. Integrating the response from zero
therefore gives

\[
 F(E)=p_{\rm sat}[E-a\log(1+E/a)].
\]

This definition avoids summing a divergent negative zero-field ground energy
\(-\int w\Delta\). It supplies no prediction of a gravitational vacuum
constant. The fully saturated state has an infinite excitation-energy cost,
consistent with the logarithmic barrier at \(p=p_{\rm sat}\).

This constructs the logarithm from actual integration over declared
two-level degrees of freedom. The distribution was solved for from the
target and has not been dynamically derived. Calling this a prediction
from the particle action would invert the direction of the argument.

### Uniqueness and the two required ends of the spectrum

For a locally integrable nonnegative density with finite total weight and
the convergent response integral, set
\(S(z)=\int_0^\infty w(\Delta)(\Delta^2+z^2)^{-1/2}d\Delta\),
on \(\Re z>0\), with the square root continued from positive real \(z\).
The boundary value on the positive imaginary axis satisfies almost everywhere

\[
 -\Im S(it+0)=\int_0^t\frac{w(\Delta)}{\sqrt{t^2-\Delta^2}}d\Delta
 =A(t).
\]

For the target, \(A(t)=p_{\rm sat}t/(a^2+t^2)\). With
\(f(r)=w(\sqrt r)/(2\sqrt r)\), this is the Abel integral
\(A(\sqrt s)=\int_0^s f(r)/\sqrt{s-r}\,dr\). Integrating that relation
against \((R-s)^{-1/2}\) and reversing the order gives
\(\pi\int_0^R f(r)dr\), because the inner beta integral equals \(\pi\).
Differentiation therefore recovers \(f\) uniquely almost everywhere.
The explicit density above solves the integral, so it is the unique density
in this class. This uniqueness is specific to this independent two-level
kernel; it is not a classification of all possible microscopic models.

The two endpoints serve different purposes:

\[
 w(\Delta)\sim\frac{p_{\rm sat}}{a^2}\Delta\quad(\Delta\to0),
 \qquad w(\Delta)\sim\frac{p_{\rm sat}a}{\Delta^2}
 \quad(\Delta\to\infty).
\]

The IR end makes the susceptibility finite but makes
\(\int w/\Delta^3\) diverge; a term-by-term analytic odd-power response
expansion is invalid. For signed one-dimensional field the result is
\(p(E)=p_{\rm sat}E/(a+|E|)\), with its \(E|E|\) correction. The UV end
has a divergent first reduced-gap moment and produces the \(1/E\)
saturation deficit. A finite collection of bounded gaps instead approaches
saturation as \(1/E^2\). Thus a soft-gap continuum alone does not explain
the entire rational interpolation.

The change \(\Delta=a\tan\theta\) rewrites
\(w(\Delta)d\Delta=p_{\rm sat}\sin\theta\,d\theta\),
\(0\leq\theta<\pi/2\). This is a useful quadrature coordinate and looks
like a hemisphere angular measure. It becomes a physical mechanism only
if the action establishes the additional relation
\(\Delta=a\tan\theta\) between internal gap and orientation. Ordinary
isotropic orientations do not establish that relation; their actual average
is treated next.

## 4. A genuinely isotropic fixed-axis ensemble

For a dipole with fixed axis \(\hat n\), the Hamiltonian source is
\(-d\,\mathbf E\cdot\hat n\,\sigma_z\). In an isotropic distribution
\(c=|\hat n\cdot\hat E|\) is uniform on \([0,1]\). If
\(w_0(\Delta)d\Delta\) is the total (unprojected) dipole magnitude density,
then

\[
 p(E)=\int_0^\infty w_0(\Delta)d\Delta
 \int_0^1\frac{c^2E}{\sqrt{\Delta^2+c^2E^2}}dc.
\]

Changing \(\Delta=cs\) inside the angular average gives the effective
reduced-gap density

\[
 w_{\rm eff}(s)=\int_0^1c^2w_0(cs)dc
 =\frac1{s^3}\int_0^s t^2w_0(t)dt.
\]

Hence \(w_0(s)=3w_{\rm eff}(s)+s w_{\rm eff}'(s)\). Inserting the
required density from Section 3 gives

\[
 \boxed{\quad w_0(\Delta)=p_{\rm sat}
 \frac{a\Delta(4a^2+\Delta^2)}{(a^2+\Delta^2)^{5/2}}>0.\quad}
\]

Its total inventory is \(\int w_0=2p_{\rm sat}\), because orientational
saturation projects each fixed-axis dipole by an average \(\langle c\rangle
=1/2\). The same exact rational radial law follows. This removes an
unnecessary alignment assumption from the conditional completion. It
does not create the supported mass dipoles or their gap distribution in
the original action. No fermions are assumed in this abstract two-state
construction; an occupation rule or internal Hilbert space beyond the
original scalars remains an explicit added model ingredient.

The construction is a homogeneous, static zero-temperature constitutive
energy. Because the occupied distribution reaches zero gap, there is no
uniform finite-frequency adiabatic elimination around zero field. A
dynamical gravitational completion must retain or analyze those soft modes
and their response times; the static integral does not establish a local
time-dependent polarization action.

## 5. Finite cutoffs and a controlled approximation window

Retain exactly the required density only on
\(\ell\leq\Delta\leq L\), without rescaling it. For \(E\ne a\),

\[
 \frac{p_{[\ell,L]}(E)}{p_{\rm sat}}=
 \frac{Ea}{a^2-E^2}\left[
 \sqrt{\frac{L^2+E^2}{L^2+a^2}}-
 \sqrt{\frac{\ell^2+E^2}{\ell^2+a^2}}\right].
\]

At \(E=a\), this is
\(\tfrac12a^2[(\ell^2+a^2)^{-1}-(L^2+a^2)^{-1}]\).
Every omitted dipole contributes positively, so the cutoff response lies
below the full response. Simple uniform bounds are

\[
 0\leq\frac{p-p_{[\ell,L]}}{p_{\rm sat}}
 \leq1-\frac a{\sqrt{a^2+\ell^2}}+\frac{aE}{2L^2}.
\]

The first term bounds missing IR weight; the second uses
\(E/\sqrt{\Delta^2+E^2}\leq E/\Delta\) and
\(a/(a^2+\Delta^2)^{3/2}\leq a/\Delta^3\) above \(L>0\).
The exact cutoff saturation and low-field susceptibility are

\[
 p_{[\ell,L]}(\infty)=p_{\rm sat}a
 \left[\frac1{\sqrt{a^2+\ell^2}}-
       \frac1{\sqrt{a^2+L^2}}\right],
\]
\[
 p_{[\ell,L]}'(0)=\frac{p_{\rm sat}}a
 \left[\frac L{\sqrt{a^2+L^2}}-
       \frac\ell{\sqrt{a^2+\ell^2}}\right].
\]

For \(E\ll\ell\), the response is analytic and odd, with first nonlinear
term of order \(E^3\). To resolve the target's nonanalytic \(E|E|\) term
one needs \(\ell\ll E\). For \(E\gg L\), the saturation deficit relative
to the cutoff inventory is instead

\[
 \frac1{2E^2}\int_\ell^L w(\Delta)\Delta^2d\Delta+O(E^{-4}),
\quad
 \int_\ell^L w\Delta^2d\Delta=p_{\rm sat}a
 \left[\sqrt{a^2+\Delta^2}
 +\frac{a^2}{\sqrt{a^2+\Delta^2}}\right]_\ell^L.
\]

The full \(1/E\) endpoint can therefore be approximated only while
\(E\ll L\). A useful interpolation window requires
\(\ell\ll a\ll L\) and \(\ell\ll E\ll L\). Feature control requires
one further qualification. In the weak-field region the desired quadratic
correction is \(p_{\rm sat}E^2/a^2\). The missing IR response is at most
\(p_{\rm sat}\ell^2/(2a^2)\), while the UV tail also removes a **linear**
response \(p_{\rm sat}aE/(2L^2)\), to leading order. Their combined bound
relative to the desired cusp correction is

\[
 \frac{\delta p_{\rm IR}+\delta p_{\rm UV}}
 {p_{\rm sat}E^2/a^2}
 \lesssim\frac{\ell^2}{2E^2}+\frac{a^3}{2EL^2}.
\]

Without a separate susceptibility recalibration, resolving that feature
therefore requires \(\max(\ell,a^3/L^2)\ll E\ll a\). In the strong-field
region, the UV error bound divided by the target deficit is at most
\(E^2/(2L^2)\) at leading order; the IR inventory loss additionally requires
\(\ell^2E/a^3\ll1\) if one compares the deficit to the *full* target
inventory rather than to the cutoff inventory. These estimates specify
which feature is controlled, rather than using a small total absolute
error to claim the correct cusp or endpoint.

## 6. Thermal finite inventory is a different mechanism

A two-state site with ordinary energy coupling \(-dE n\) has partition
function \(Z=1+z_0e^{\beta dE}\) and occupation
\(n=z_0e^{\beta dE}/(1+z_0e^{\beta dE})\). This is logistic in the
gravitational energy source. The Langmuir rational occupancy
\(n=E/(a+E)\) follows if \(E/a\) is the chemical activity, equivalently if
the microscopic source is \(-T\log(E/a)n\). An acceleration is not that
activity in the stated particle action. With a site number density
\(n_{\rm site}\) of two-opposite-orientation permanent dipoles,
\(p=n_{\rm site}d\tanh(\beta dE)\); with continuous classical orientations,
\(p=n_{\rm site}d[\coth(\beta dE)-1/(\beta dE)]\). The latter has a \(1/E\)
endpoint and a logarithmic high-field free energy, but its weak-field
response is odd analytic, not the full rational law.

For a classical cell of volume \(V_c\) and total dipole variable \(D\),
the target free energy itself determines an exact inverse condition. If
\(Z(E)/Z(0)=\langle e^{\beta ED}\rangle_0=e^{\beta V_cF(E)}\), then

\[
 \frac{Z(E)}{Z(0)}=e^{\beta V_cp_{\rm sat}E}
 \left(1+\frac Ea\right)^{-r},\qquad
 r=\beta V_cp_{\rm sat}a.
\]

This is precisely the moment-generating function of
\(D=V_cp_{\rm sat}-Y\), where \(Y\) has gamma density
\((\beta a)^rY^{r-1}e^{-\beta aY}/\Gamma(r)\), \(Y>0\).
Direct integration verifies it. Its support is
\(-\infty<D\leq V_cp_{\rm sat}\); it is neither a bounded dipole inventory
nor an isotropic zero-field distribution. A bounded \(D\) has a finite
moment-generating function for every real \(E\), whereas the target has a
singularity at \(E=-a\). Thus ordinary classical bounded-dipole thermal
inventory cannot give the full law exactly. This thermal statement and
the gapless zero-temperature construction in Section 3 have different
hypotheses and do not contradict each other.

## 7. Comparison with actual scalar spectral support

The exact positive continuum construction specifies a **nonlinear local
saturator** and a **dipole-weighted occupied reduced-gap distribution**.
A bare density of states is not sufficient. Several comparisons prevent
a false identification with the original model:

* For the actual finite homogeneous conversion sector at nonzero coupling,
  the matrices in Section 2 have discrete avoided-crossing gaps. The checked
  \(Q=2,4,8,16\) sectors have nonzero lowest gaps. A finite set of those
  states gives square-root-like saturation, not the exact continuum.
* The free three-dimensional NR mode count for a quadratic dispersion has
  density of states proportional to \(\sqrt{\omega-\omega_0}\); for a
  linear dispersion it is proportional to \(\omega^2\). Those raw counts
  do not establish the weight seen by gravity.
* There is a real near-match that must be retained: in the dilute matched
  one-component Bogoliubov limit, define the **nonlocal** displacement
  \(P_L(k)=\delta\rho(k)/k\). Its momentum-integrated zero-temperature
  one-phonon measure is

  \[
  J_P(\omega)=\frac{\rho_0 k(\omega)}{4\pi^2S(\omega)},\quad
  S=\sqrt{c_s^4+\omega^2/m^2},\quad
  k^2=2m^2(S-c_s^2).
  \]

  This follows from \(\Omega_k^2=c_s^2k^2+k^4/(4m^2)\),
  \(|\rho_k|^2=\rho_0k^2/(2\Omega_k)\), and
  \(\int d^3k/(2\pi)^3\delta(\omega-\Omega_k)\).
  In particular \(J_P\sim\rho_0\omega/(4\pi^2c_s^3)\) in the IR.
  Its linear IR power agrees with the required two-level weight. In the
  NR particle regime it instead behaves as
  \(\rho_0m\sqrt{2m}/(4\pi^2\sqrt\omega)\), not \(\omega^{-2}\).
  Extending that regime to infinite frequency is outside NR validity.
  With the density operator itself the IR measure is proportional to
  \(\omega^3\). The sibling `collective_restoring` lane derives the
  underlying response and this source-specific distinction.

Even the coincident IR power does not provide the completion. These are
squared matrix-element weights of propagating **harmonic** modes, not
dipole magnitude weights of independently saturating local two-level sites.
The field at momentum \(k\) sources that momentum, while the integral
above sums different momentum modes. A uniform external field in a
translation-invariant medium does not source each \(k\) independently.
Moreover \(P_L=\delta\rho/k\) is an inverse derivative rather than an
established local internal polarization. No source-preserving map from
these phonons to the Section 3 dipoles has been demonstrated.

The real-mediator alternate model has an exactly algebraic tree stationary
branch and a separately tuned critical phase pressure \(X_{\rm NR}^{3/2}\)
only on its controlled positive branch. That is neither this reduced-gap
distribution nor a material mass-dipole source. It remains a separate action.

## 8. A tree obstruction beyond analyticity at zero

For finitely many local auxiliary variables and a polynomial microscopic
potential, stationary elimination on an isolated algebraic branch gives an
algebraic effective energy as a function of its algebraic source. This
statement also covers singular points and algebraic/Puiseux critical
branches; it does not require a nonzero Hessian at zero. Polynomial matrix
eigenvalues in a finite-dimensional quantum problem are likewise algebraic.

The target \(F(E)=p_{\rm sat}[E-a\log(1+E/a)]\) is not algebraic:
analytic continuation around \(E=-a\) changes it by
\(-2\pi i p_{\rm sat}a\) each circuit, producing infinitely many values.
An algebraic function has only finitely many branches. Therefore finite
polynomial tree elimination cannot equal the exact target on an open
positive-field interval. This rules out that finite construction, including
its algebraic critical continuation; it does not rule out the continuum
construction above, loop determinants, statistical entropy, nonlocal
integrating-out, or explicitly nonpolynomial microscopic interactions.

## 9. Evidence, review boundary, and continuation

`contract.json` fixes the tested finite assertion, conventions, exclusions,
software versions, and resource caps. `check_rational.py` checks the exact
Legendre identities, the positive spectral integral and isotropic inversion,
cutoff primitives, independent high-precision quadratures, and complete
fixed-charge finite matrices. Runner manifests preserve unsuccessful runs
instead of replacing their history. The exact integral and inverse proof
above, rather than numerical quadrature, support the continuum claim.
Run 003 completed with **88 passing exact/finite controls** and its v2
manifest passed current input/output hash validation. The eight direct
50-decimal continuum quadratures had a maximum relative discrepancy of
\(6.33\times10^{-51}\); three independently ordered isotropic quadratures
had a maximum of \(1.84\times10^{-51}\). These tiny finite residuals do
not certify the universal identity. Fifteen cutoff points include an
instructive example: \(\ell/a=0.01,L/a=100\) gives response deficits
of about 0.0604% at \(E/a=0.1\) and 10, 0.0200% at 1, and 0.9108%
at 0.001 and 1000. The endpoint/cusp qualifications above still apply.
Run 001 was `launch-failed` in the runner's pre-execution resource setup;
run 002 exposed an overly broad symbolic angular chart in one check.
Run 003 omitted the memory-cap request after that launch failure and used
the correct positive tangent chart. The launch exception did not expose
its underlying OS error, so an unsupported memory cap is a diagnosis,
not a proved cause. Neither earlier run is scientific counterevidence.

No external theorem, empirical result, or novelty assertion is used as an
unverified load-bearing leaf in this note.

The sibling `internal_polarization/RATIONAL_REVIEW.md` independently
reconstructed the integral, Legendre pair, isotropic inverse spectrum,
inventory/susceptibility factors and finite-cutoff formulas. Its review
pin predates the final edits. Its low-field UV-error finding is resolved
by the added condition \(E\gg a^3/L^2\) in Section 5; the later energy-origin,
thermodynamic-limit, and soft-mode qualifications are author self-review.
The review did not independently audit the thermal or algebraicity sections
or run this lane's code. `VERIFICATION.md` records these boundaries.

The original gravitational constitutive derivation remains **open**. The
smallest missing physical implication is a source-preserving construction
of local mass dipoles from the stated particle action, followed by a
derivation of their nonlinear saturation and of the occupied distribution
above. Its normalization must also predict \(p_{\rm sat}=a/(4\pi G)\).

The presently executable continuations are explicit:

1. Test whether a specified new supported/tidal bound-state model has the
   required source operator before importing its two-level spectrum. A
   tidal curvature response would be a different target variable.
2. If a genuine local source is found, calculate the full reduced-gap and
   dipole-magnitude distribution from that model. The Abel inverse and the
   cutoff formula give exact acceptance tests. A distribution with the
   correct IR exponent alone is insufficient.
3. If only a finite gap band is controlled, state the field window
   \(\ell\ll E\ll L\) and the error on the feature being claimed. Do not
   extrapolate a fitted interpolation to \(p=p_{\rm sat}\) or \(p=0\).
4. An interacting gapless continuum could evade independent-site
   assumptions. Its actual sourced energy, rather than a raw DOS match,
   must be calculated. This remains deferred pending a specified operator
   and controlled approximation; it is not ruled out by the finite-state
   or polynomial-tree statements.

No current contract, queue, manuscript, publication artifact, or shared
status file was changed by this lane. The conditional construction is ready
for independent review; it does not close the original particle-to-gravity
dictionary.
