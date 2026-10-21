# Granting a supported reference does not derive a response-off state

20 October 2026. Continuation of the live-host multipole route. This lane
writes only `support/RESULT.md` and its source pins; `phases/` and earlier
packets remain immutable. The calculations below are analytic.

**Normalized target and verdict: incomplete, with the physical support and
canonical-response map missing.** A supported host can make a bound
particle sag relative to it in a uniform gravitational probe. The exact
two-coordinate harmonic susceptibility makes the support reaction explicit.
Removing the binding transfers the particle response to its free
zero-frequency pole; it does not make that response vanish. If the support
is instead completed as an entirely live translation-invariant system,
the uniform probe couples only its center of mass. These results close
the held-reference loophole in the stated harmonic control. They do not
derive an anchoring interaction, a scalar-to-`P` map, or an S4 switch.

## 1. What the two-coordinate control actually assumes

Let `x` denote the probe-axis displacement of a daughter of mass `m>0`,
and `X` that of a host of mass `M>0`, relative to a supported reference.
Here `M` is a host mass, not the original scalar source mass. Consider
the local quadratic Hamiltonian

\[
 H={p_x^2\over2m}+{p_X^2\over2M}
     +{k_b\over2}(x-X)^2+{k_a\over2}X^2-g(mx+MX),
 \qquad k_a,k_b>0.                                   \tag{1}
\]

The sign convention chooses `g` as the uniform force per unit mass,
so the gravitational probe is `-gD`, `D=mx+MX`. The two curvatures are
definitions of a proposed local projection: `k_b` is its relative-binding
Hessian and `k_a` its supported-host Hessian. They are not new fitted
springs or declared fundamental operators. Equation (1) applies to an
existing model only after its actual energy, coordinate choices, source
couplings, support, and positive small-displacement branch yield it.
The present scalar action does not specify such an absolute anchoring
term or an inherited nongravitational support mechanism.

In particular, the prior attraction proof's radial host curvature
`D_h=G M_h A/q^3` acts on a *spherical radial breathing coordinate*.
The full mass dipole of that breathing mode is zero. It cannot be
substituted for `k_a` of a host center displacement `X` while retaining
the uniform source `MgX`. A circular-orbit radial Hessian also has its
angular/centrifugal dynamics; treating it as an independent Cartesian
anchor discards part of its actual source and kinematics. No such
identification is made here.

The displacement range must stay inside the admitted quadratic branch.
The comparison `k_b->0` below is a comparison of harmonic response
functions at finite frequency, not a derivation that a binding-energy
crossing instantaneously changes an interaction coefficient.

## 2. Exact retarded susceptibility in this conditional projection

Write

\[
 K=\begin{pmatrix}k_b&-k_b\\-k_b&k_b+k_a\end{pmatrix},
 \quad\mathsf M=\operatorname{diag}(m,M),\quad
 w=\begin{pmatrix}m\\M\end{pmatrix},\quad
 z=(\omega+i0)^2.
\]

The linear equations are
`(K-z M) (x,X)^T=g w`, so the actual full-source response is

\[
 \delta D=\chi_{Dg}(\omega)g,
 \quad\boxed{\chi_{Dg}=w^T(K-z\mathsf M)^{-1}w
 ={k_b(m+M)^2+m^2k_a-mM(m+M)z\over
   k_bk_a-[k_b(m+M)+mk_a]z+mMz^2}.}                 \tag{2}
\]

This is classical retarded harmonic response and also the exact
harmonic quantum susceptibility in its admitted model. A nonzero
linewidth or stochastic noise is not inserted. In the static supported
case the inverse exists and gives

\[
 \boxed{\chi_{Dg}(0)={(m+M)^2\over k_a}+{m^2\over k_b}.}
                                                               \tag{3}
\]

For the relative displacement `r=x-X`, the same inverse gives

\[
 {r\over g}={m k_a\over
      k_bk_a-[k_b(m+M)+mk_a]z+mMz^2}.               \tag{4}
\]

Thus a daughter-only relative dipole `mr` has static susceptibility
`m^2/k_b` only when a supported static solution exists. Its apparently
intrinsic gravitational drive depends on that support. It is not the
full mass dipole of the live system.

Both normal-mode squared frequencies are positive for `k_a,k_b>0`,
since the mass-normalized `M^(-1/2) K M^(-1/2)` is positive definite.
If `e_nu` are its orthonormal eigenvectors and `v=(sqrt(m),sqrt(M))`,

\[
 \chi_{Dg}(\omega)=\sum_\nu
 {|v\cdot e_\nu|^2\over\Omega_\nu^2-z},
 \qquad\sum_\nu|v\cdot e_\nu|^2=m+M.               \tag{5}
\]

Changing binding redistributes this spectral weight; it does not remove
the universal mass source. No instability or negative spectral weight
is needed for the following limits.

## 3. Free-host and release limits do not commute with statics

If the host has no anchor, put `k_a=0` in the finite-frequency formula.
The numerator and internal-mode factor cancel exactly:

\[
 \boxed{\chi_{Dg}(\omega)=-{m+M\over z},\qquad r/g=0.} 
                                                               \tag{6}
\]

This is the freely accelerating total center of mass. Its internal
binding mode has no uniform-gravity oscillator strength. A uniform
force gives no static equilibrium of the unsupported center of mass;
one cannot instead use the divergent static expression (3) as a finite
internal polarization.

Now retain `k_a>0` and release the daughter by comparing to `k_b=0`.
At fixed nonzero frequency,

\[
 \boxed{\chi_{Dg}(\omega)=-{m\over z}
                    +{M^2\over k_a-Mz}.}           \tag{7}
\]

The first term is the daughter free-motion pole and the second the
supported host response. Neither is zero. In the formal clamped limit
`k_a->infinity`, the bound daughter instead has
`chi=m^2/(k_b-mz)`, becoming `-m/z` on release.

For every positive `k_b` the supported static response in (3) grows as
binding weakens. In a physical finite binding well the static shift
`r=mg/k_b` eventually leaves the local harmonic domain. No infinite
static sag is asserted after that breakdown. In the released state
there is no static equilibrium under a nonzero uniform force, rather
than a zero response.

The distinction is load-bearing: a finite-frequency free-motion pole,
a regular internal bound-mode susceptibility, and a static material
constitutive coefficient are different observables. One may define a
regular bound-mode contribution that ceases to be gapped on release,
but (1)-(7) do not identify that chosen contribution with the canonical
`P` energy or its density/current source. Nonzero ordinary free response
alone is not a theorem forbidding every additional-force off state.

## 4. Count the support reaction and any driving work

At the supported static minimum,

\[
 r={mg\over k_b},\quad X={(m+M)g\over k_a},\quad
 F_{\rm support}=-k_a X=-(m+M)g.                   \tag{8}
\]

The support balances the whole gravitational force. The binding and
support elastic energies are respectively
`m^2g^2/(2k_b)` and `(m+M)^2g^2/(2k_a)`. The total minimized energy,
including `-gD`, is `-chi_Dg(0)g^2/2`. The gravitational probe supplies
the corresponding quasistatic parameter work `-integral D dg`.

If the reference position is prescribed as `X_a(t)`, replace the
support term by `k_a(X-X_a)^2/2`. Its explicit drive power is
`-k_a(X-X_a) dot X_a`. Changing a curvature by hand likewise contributes

\[
 {\partial H\over\partial t}
 ={\dot k_b\over2}r^2+{\dot k_a\over2}X^2-\dot g D
\]

for a fixed reference, in addition to other actual driving terms.
These are work terms, not a derived irreversible switch or heat sink.
No support reservoir is granted infinite capacity or reset for free.

If all support is actually supplied by another live mass `A>0` at `Y`,
the closed comparison has relative energy
`k_b(x-X)^2/2+k_a(X-Y)^2/2` and probe
`-g(mx+MX+AY)`. It is translation invariant. Its full source is

\[
 D_{\rm full}=(m+M+A)R,\quad
 R={mx+MX+AY\over m+M+A}.
\]

The uniform response is therefore exactly

\[
 \chi_{D_{\rm full}g}=-{m+M+A\over z},              \tag{9}
\]

with no internal uniform dipole. Keeping `k_a` while omitting the
gravitational source and motion of its actual anchor changes this
closed system into an externally supported control. A heavy anchor
does not justify dropping its source: its small displacement times
its large mass can remain finite.

The same issue appears when other live coordinates are integrated out.
For a static block energy with cross Hessian `B`, positive responder
block `C`, retained Hessian `A`, and source weights `w_x,w_y`, exact
completion of squares gives

\[
 A_{\rm eff}=A-BC^{-1}B^T,\quad
 w_{\rm eff}=w_x-BC^{-1}w_y,
 \quad\chi_{\rm background}=w_y^TC^{-1}w_y.          \tag{10}
\]

Its reduced energy contains
`x^T A_eff x/2-g w_eff^T x-g^2 chi_background/2`.
Thus an actual support reduction changes both the restoring matrix and
the probe source, and leaves a source-only contribution. It is not
consistent to retain a convenient positive curvature while discarding
those derived source terms. In a dynamical reduction the corresponding
frequency-dependent blocks must be used; a zero-frequency translational
singularity cannot simply be inverted.

## 5. What this continuation resolves

An externally supported or nongravitationally accelerated reference can
produce the relative sag that is absent for a freely falling closed
bound system. The full conditional susceptibility is now calculated,
including what happens on release and where the reaction resides. It
contains no fitted extra coupling. Its positive curvatures remain
unprovided physical projections until an actual existing support model
and coordinate/source dictionary supply them.

Even granting that support, the construction gives neither the canonical
critical `K|P|^2/2` matter coefficient, its nonlinear `W_rem`, the retained
stiffness, nor a source rule deleting released mass from `P`. A binding
curvature approaching zero yields a soft/free mode, not the desired
intrinsic response-off operator. A changed probe volume after escape is
also different from a retained ordinarily gravitating released stock.

The earlier multipole result therefore remains valid for a closed live
host. The held-reference exception is a conditional supported mechanical
response with its own counted reaction, not a missing derivation of the
S4 switch. No actual memory lifetime, history rule, observational pass
or complete theory is inferred.

Verification: direct two-by-two inversion, normal-mode diagonalization,
static force balance, work differentiation, center-of-mass separation
and block square completion. Source identities and every limit were
rechecked analytically. No numerical, symbolic-package or scientific
run was used. Proofreading/self-review covers this new note only; no
mathematical-token typo repair or unrelated edit was required. This is
author analytic self-review pending separate reconstruction, not a
certificate that the physical support exists in the original action.
