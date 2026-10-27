# A closed shared scalar–baryon state and its full linear source decomposition

Date: 19 October 2026. Mathematical parent: `CE-SCALAR-DIPOLES-2026-10-19 /
CE-FM090`. Initial observed HEAD: `3ac0427149a2108afa8f102df4d82da33b9060c4`;
preparation HEAD: `aa0d1a83d15c1fe2a0c9d32f189bdbbff49dd19a`.
Concurrent repository changes are not inputs by implication: `source_pins.json`
and the two runner manifests pin the actual source/code bytes. This lane writes
only `shared_state_2026_10_19/modes/` and changes no action or manuscript.

**Result.** There is an exact, finite-radius, locally stable shared two-fluid
TF control. Its baryon pressure law is a declared environmental closure. Its
linear Euler–Poisson system separates into an ordinary self-gravitating n=1
total-density channel and a positive-pressure compensated channel. The latter
has actual finite inhomogeneous gaps and large *subsystem* dipole matrix
elements, while its complete Newtonian mass source vanishes pointwise. The
total channel has source-carrying internal l=1 modes at finite wavelength; an
exact static source kernel and a finite radial spectrum are given below.
Neither channel supplies a populated local inventory of saturating dipoles.
The source cancellation is special to the common-profile TF state and is
not an exclusion of unequal-profile shared states.

## 1. Original input, environmental closure and exact equilibrium

Retain the original minimally gravitating canonical Phi/X model only through
its matched dilute daughter sector, with

\[
 g_2={\lambda_{\rm rep}\over2m^2}>0,\qquad
 K_d={g_2\over2m^2}={\lambda_{\rm rep}\over4m^4},\qquad
 p_d=K_d\rho_d^2.                                                    \tag{1}
\]

The matching is the full threshold matching, including the analytic
negative-frequency-source contact. It is not the older positive-frequency
coefficient. The original source occupation, quantum surface layer and
post-Newtonian stress corrections are outside this TF control.

**Added closure, explicitly not a derived baryon particle equation of state:**
the live baryons obey `p_b=K_b rho_b^2`, with `K_b>0`, share only ordinary
Newtonian gravity with the daughter, and conserve their own mass. Set

\[
 a={K_b\over K_d+K_b},\quad b={K_d\over K_d+K_b},\quad a+b=1,
 \qquad K={K_dK_b\over K_d+K_b},\qquad K_da=K_bb=K.                   \tag{2}
\]

Use `U<0` near an isolated object, `g=-grad U`,
`nabla^2 U=4 pi G(rho_d+rho_b)`. The fluid equations are

\[
 \partial_t\rho_j+\nabla\cdot(\rho_jv_j)=0,\qquad
 (\partial_t+v_j\cdot\nabla)v_j=-\nabla(2K_j\rho_j+U+U_{e,j}).       \tag{3}
\]

For common support and vanishing density at the same surface, the two
hydrostatic integration constants agree. The exact equilibrium is

\[
 \rho_{d0}=a\rho_0,\quad\rho_{b0}=b\rho_0,\quad
 \rho_0(r)=\rho_c f(r/R),\quad f(x)={\sin(\pi x)\over\pi x},\quad 0\le x\le1,
\]
\[
 R^2={\pi K\over2G},\quad
 M_T={4\rho_cR^3\over\pi},\quad M_d=aM_T,\quad M_b=bM_T,
 \quad U_0+2K\rho_0=-{GM_T\over R}.                                \tag{4}
\]

The central amplitude is free. Common profiles require the selected mass
ratio `M_d/M_b=K_b/K_d`; arbitrary mass ratios need a different equilibrium.
This branch is a live shared state, rather than a prescribed rigid host or a
mean-subtracted homogeneous medium. Its radius is smaller than the pure
daughter TF radius by `sqrt(a)`. No galaxy scale or abundance is selected.

## 2. Exact energetic split and its stability scope

Define the total density and composition departure, also for finite changes,

\[
 \rho=\rho_d+\rho_b,\quad \eta=b\rho_d-a\rho_b,
 \quad\rho_d=a\rho+\eta,\quad\rho_b=b\rho-\eta.
\]

Positivity is exactly `-a rho<=eta<=b rho`. Direct expansion gives

\[
 E[\rho,\eta]=K\int\rho^2+W[\rho]+{K\over ab}\int\eta^2,
 \quad W[\rho]=-{G\over2}\iint {\rho(x)\rho(y)\over|x-y|}\,d^3x\,d^3y. \tag{5}
\]

For the selected separate masses, `int eta=0`. At any allowed total density,
`eta=0` is the unique composition minimizer. The relative density Hessian is
strictly positive; common gravity cannot lower it because gravity depends
only on total density. The total density Hessian is exactly that of the n=1
polytrope. In the mass-preserving TF perturbation class of the pinned
`VIRIAL_NORMALIZATION.md`, it is positive modulo translations. One direct
check uses the ball Newton operator: for angular order `l>=1` its regular
eigenfunctions have exterior matching `x j_(l-1)(x)=0`, and the energy
coefficient is `K[1-pi^2/x^2]`. Its l=1 first root is the translation at pi;
all other roots are larger. The l=0 fixed-mass comparison has its first root
at the first zero of j1, greater than pi. Thus the added composition
directions do not introduce an unstable density mode.

This is local energetic and linear density-mode stability in the declared
TF fluid class, with separately conserved masses and ordinary free surfaces.
Density-preserving vortical/relabeling coordinates can remain zero modes.
The literal sharp TF density has a divergent GP gradient integral. Restoring
the daughter gradient energy both smooths the edge and breaks the exact
two-fluid common-profile decomposition unless the other dynamics are also
matched; a finite-GP stability or convergence theorem is not being claimed.

## 3. Full linear Euler–Poisson decomposition

Let `xi_d,xi_b` be the material displacements. Define

\[
 \xi=a\xi_d+b\xi_b,\quad\zeta=\xi_d-\xi_b,
 \quad\xi_d=\xi+b\zeta,\quad\xi_b=\xi-a\zeta,
\]
\[
 \delta\rho=-\nabla\cdot(\rho_0\xi),\qquad
 \eta=-ab\nabla\cdot(\rho_0\zeta).                                 \tag{6}
\]

The linear kinetic energy and quadratic potential energy separate:

\[
 T^{(2)}={1\over2}\int\rho_0(|\dot\xi|^2+ab|\dot\zeta|^2),
\]
\[
 E^{(2)}=K\int(\delta\rho)^2+W[\delta\rho]
               +{K\over ab}\int\eta^2.                            \tag{7}
\]

For `Ubar_e=a U_(e,d)+b U_(e,b)` and
`Delta U_e=U_(e,d)-U_(e,b)`, the full linear field equations are

\[
 \ddot\xi=-\nabla(2K\delta\rho+\delta U+\bar U_e),\quad
 \nabla^2\delta U=4\pi G\delta\rho,
\]
\[
 \ddot\zeta=-\nabla\left({2K\over ab}\eta+\Delta U_e\right).         \tag{8}
\]

Thus common gravity drives only the total channel. An independently applied
species-dependent force is a diagnostic source for the compensated channel;
it is not an extra force provided by the original model. This derivation
retains the complete inhomogeneous support, recoil, pressure and shape modes.
In particular a rigid relative shift is generally *not* an eigenmode.

For the unforced relative density, (8) gives

\[
 \ddot\eta=2K\nabla\cdot(\rho_0\nabla\eta),\qquad
 -{1\over x^2}(x^2f\phi')'+{l(l+1)f\over x^2}\phi=\lambda\phi,
 \quad\omega^2={GM_T\over R^3}\lambda.                             \tag{9}
\]

Use the regular center and finite-energy free-surface solution; discard the
logarithmic surface solution. The zero natural flux follows from `f(1)=0`.
Equivalently the regular mode obeys `lambda phi(1)=phi'(1)` because
`f'(1)=-1`. This is the free-surface continuity/Euler relation, not an
artificial fixed wall. The l=0 constant composition mode changes the separate
masses and is excluded. For every `l>=1` the compressional branch is gapped.

There is a simple analytic l=1 bound. On `[0,1]`,
`f(x)>=(1-x^2)/2`; it follows by `sin z>=z-z^3/6` on each half interval,
using `sin(pi x)=sin(pi(1-x))` on the second half. With `u=x^l v`, integration
by parts gives

\[
 \int_0^1(1-x^2)[x^2u'^2+l(l+1)u^2]-2l\int_0^1x^2u^2
 =\int_0^1(1-x^2)x^{2l+2}v'^2\ge0.
\]

Consequently `lambda_(l,1)>=l`. Taking the trial density `phi=x` gives

\[
 1\le\lambda_{1,1}\le{15\over\pi^2}=1.5198177546\ldots .            \tag{10}
\]

The finite Ritz controls give the first relative l=1 eigenvalues
`1.49989790818, 10.6866840716, 25.9345140138, 46.8961785018`.
These are convergence-tested numerical values, not certified enclosures.
A rigid relative displacement instead has the restricted Rayleigh frequency
`omega_rigid^2=(pi^2/6) GM_T/R^3`; the finite shape correction is real.

## 4. Actual subsystem dipoles and the vanishing relative gravitational source

For clarity take real `Y_10=sqrt(3/(4 pi)) cos(theta)` and normalize a relative
density eigenfunction by `int_0^1 x^2 phi_n^2 dx=1`. Put
`J_n=int_0^1 x^3 phi_n dx`, `mu=ab M_T`, and `lambda_n` as in (9). The relative
mode has a real dark subsystem mass dipole `D_d,z=int z delta rho_d`; its
baryon dipole is the negative of this. Canonical oscillator normalization gives

\[
 |\langle1_n|D_{d,z}|0\rangle|^2
 ={\hbar\mu\over2\omega_n}F_n,
 \qquad F_n={\pi^2\over3}\lambda_nJ_n^2,\qquad D_b=-D_d.            \tag{11}
\]

Thus sizes and gaps are supplied by this specified collective state. These
are subsystem mass-dipole matrix elements, not signed constituent masses or
two-level saturation dipoles. Completeness of the radial operator yields

\[
 \sum_nF_n=1,\qquad \sum_n{F_n\over\lambda_n}={\pi^2\over15},\qquad
 \alpha_{\rm diff}(0)={2\over\hbar}\sum_n{|D_{d,10}|^2\over\omega_n}
 ={ab\pi^2R^3\over15G}.                                         \tag{12}
\]

The first identity is the kinetic oscillator-strength budget of the relative
coordinate. The second follows from `sum J_n^2=int x^4 dx=1/5`. The finite
calculation preserves both identities within roundoff in every retained
space because the source `xY_10` is already in that space. The first three
first-moment fractions are `0.984785729061, 0.014879553154, 0.000327195027`.

However, each compensated mode has exactly

\[
 \delta\rho_d=\eta,\quad\delta\rho_b=-\eta,
 \quad\boxed{\delta\rho_{\rm grav}(x)=0},\qquad
 \langle1_n|\rho_{{\rm grav},k}|0\rangle=0\quad\hbox{for every }k.  \tag{13}
\]

Equation (12)'s inverse-G susceptibility is therefore conjugate to
`Delta U_e=-g_diff z`, not to common gravitational acceleration. Counting its
subsystem oscillator strength as total gravitational strength would produce
a false gravity normalization. For comparison, dividing (12) by the object
volume gives `4 pi G alpha_diff/V=ab pi^2/5`, which remains closure/composition
dependent even for the diagnostic differential force.

## 5. Source-carrying total l=1 modes and the exact static kernel

Nonzero-frequency total modes are irrotational. Write their radial
displacement potential `u_n(x)Y_10`, with

\[
 h_n=-\nabla_x\cdot[f\nabla_x(u_nY_{10})]/Y_{10},\qquad
 \int_0^1f[x^2u_n'u_m'+2u_nu_m]dx=\delta_{nm}.                     \tag{14}
\]

In physical mass normalization their complete Fourier source for `k` along z is

\[
 \sigma_n(k)=-i\sqrt{12\pi\rho_cR}\ I_n(q),\quad
 I_n(q)=\int_0^1x^2h_n(x)j_1(qx)dx,\quad q=kR,
 \quad |\langle1_n|\rho_k|0\rangle|^2={\hbar|\sigma_n(k)|^2\over2\omega_n}.
                                                                    \tag{15}
\]

The l=1 translation `u=x` is a zero mode. Remove it by kinetic orthogonality;
every remaining mode then has zero integrated total mass dipole,
`int x^3 h_n dx=0`. This does not set its finite-k source to zero:
`I_n(q)=-(q^3/30)int x^5h_n dx+O(q^5)`. The bounded radial calculation gives

\[
 {\omega_{n,l=1}^2R^3\over GM_T}
 =7.95910056738,\ 22.7614030275,\ 43.4925722822,\ 69.9712089671,\ldots . \tag{16}
\]

The retarded polarization susceptibility to the corresponding source has
the mode representation

\[
 \chi_{\Pi,l=1}(\omega,k)={1\over k^2}
 \sum_{n>0}{|\sigma_n(k)|^2\over\omega_n^2-(\omega+i0)^2},\qquad
 {4\pi G\over V}\chi_{\Pi,l=1}(0,k)
 ={9\pi^2\over q^2}\sum_{n>0}{I_n(q)^2\over\lambda_n}.             \tag{17}
\]

Here `V=4 pi R^3/3`; (17) is the response of **one** shared object divided by
its volume. It is not a many-object local medium prescription. The sign is
positive for a source `-J rho`; an external potential contributes `+U_e rho`
and produces the corresponding negative density response. A truly uniform
common acceleration drives the removed COM, whose static susceptibility does
not exist in an isolated inertial frame.

An exact static inverse supplies an independent benchmark of (17). For an
applied l=1 potential `U_e=U_* j_1(qx)Y_10`, subtract the uniform term needed
to make its total force zero. Define

\[
 P(q)={q^2\over q^2-\pi^2},\quad J(q)={j_2(q)\over q},\quad J(\pi)={3\over\pi^3},
\]
\[
 H_q(x)=P(q)\left[j_1(qx)-{J(q)\over J(\pi)}j_1(\pi x)\right],\qquad
 \delta\rho=-{U_*\over2K}H_qY_{10}.                               \tag{18}
\]

It obeys `(nabla_x^2+pi^2)(H_qY_10)=-q^2 j_1(qx)Y_10` and
`int x^3 H_q dx=0`. Exterior self-potential matching fixes the removed term
to `c(q)xY_10`, where `c(q)=pi^2 q j_0(q)/[3(pi^2-q^2)]`.
The apparent singularity at `q=pi` is removable; formulas below use its limit
there, and the reported finite tests avoid that point. With

\[
 A(q)={j_1(q)^2-j_0(q)j_2(q)\over2},\qquad
 B(q)={qj_0(q)\over\pi(\pi^2-q^2)},
\]
\[
 \boxed{{4\pi G\over V}\chi_{\Pi,l=1}(0,k)
 ={9\pi^2\over q^2}P(q)\left[A(q)-{J(q)\over J(\pi)}B(q)\right].}  \tag{19}
\]

This follows either by direct integration of (18) or by the Bessel Green
identity for `int x^2 j_1(qx)j_1(pi x)dx=B(q)`. Its long-wavelength form is

\[
 {4\pi G\over V}\chi_{\Pi,l=1}(0,k)
 =\left({1\over5\pi^2}-{2\over105}\right)(kR)^4+O((kR)^6),
 \qquad C_4=0.001216617680848507\ldots .                           \tag{20}
\]

One elementary derivation of (20) applies the effective cubic l=1 potential
`[x^3-(5/3-10/pi^2)x]Y_10`. Its regular static enthalpy is
`(10/pi^2)x-(2 pi/3)j_1(pi x)`; its overlap with `x^3Y_10` is
`20/pi^4-40/(21 pi^2)`. Multiplication by the plane-wave coefficient
`j_1(qx)=qx/3-q^3x^3/30+...` gives (20). This is a physical finite-wavelength
source result within the shared inhomogeneous state.

| kR | `4 pi G chi_(Pi,l=1)/V`, static internal source |
|---:|---:|
| 0.1 | 0.0000001215531435 |
| 0.3 | 0.000009775681270 |
| 1 | 0.001112391748 |
| 3 | 0.04323062860 |

Only the l=1 internal sector is in (15)–(20). A full plane-wave source also
has l=0, l=2 and higher channels. In particular tidal l=2 response must not
be discarded when quoting the full long-wavelength gravitational kernel.

## 6. Nonlinear composition, finite support and occupation

The exact energy split also identifies a bounded *diagnostic* nonlinear
composition problem. At fixed total profile, the species source is

\[
 E_e=\int\rho\bar U_e+\eta\Delta U_e.
\]

With separately fixed masses its minimum is

\[
 \eta_*(x)=\operatorname{clip}\left[-{ab\over2K}(\Delta U_e-C_\eta),
                    -a\rho(x),\ b\rho(x)\right],\quad\int\eta_*=0. \tag{21}
\]

`C_eta` is the composition Lagrange multiplier. It cannot generally be set
to zero when `a!=b`; an odd differential potential then meets unequal clipping
bounds. Common gravity has `Delta U_e=0`, and its composition minimum remains
`eta=0` exactly. It does not produce (21)'s relative polarization.

Because the common equilibrium density vanishes at R, any nonzero finite
differential force reaches the positivity bound in a thin edge layer. Linear
response (12) still exists. At large imposed differential force, a fixed
profile rearranges into species-dominated spatial domains. This is a
constraint-induced response with profile and composition scales, not the
target rational law. The bound `|D_d|<=min(M_d,M_b) R` follows whenever both
species stay inside this ball and the total COM is fixed. For `a=b=1/2` and
the strictly fixed common n=1 profile, the extremal hemispherical rearrangement
has exactly

\[
 {D_{d,\max}\over M_TR}={\pi^2-4\over4\pi^2}=0.1486788164\ldots .   \tag{22}
\]

These bounds require confinement to the declared support. In the isolated
full problem an indefinitely imposed species-dependent linear tilt is
unbounded at infinity and permits escape. It cannot be promoted to a global
stable saturation law by the fixed-profile calculation.

Each stable linear mode quantizes to a harmonic oscillator ladder, rather
than an independently saturating two-level object. Its retarded coordinate
commutator is independent of the oscillator excitation count. If a thermal
state is *specified*, occupation is `n_B(omega)` and unsymmetrized transition
weights contain `n_B+1` and `n_B`; the Kubo weights use their difference.
The original production/preparation history has not selected those counts,
the free mass amplitude, or a distribution of such shared objects. No
occupied continuum `w(Delta)`, universal acceleration or `1/(4 pi G)`
normalization follows from this example.

## 7. Finite checks, provenance and exact non-claims

`check_shared_modes.py` constructs the relative operator with unit-angular-
norm Jacobi radial bases, and the total Euler–Poisson Hessian with its exact
exterior multipole Green function. Its separated inner/outer Gauss quadrature
avoids a spurious discretization kink at equal radii. It checks three exact
rational energy/kinematic splits, relative basis sizes 6/10/14/18, total
basis sizes 6/10/14, and quadrature orders 128 versus 192 at size 14. It tests
the raw translation null direction before removing it. No dynamical
simulation, fit, scan, random sampling or new physical sector is involved.

`run_001/manifest.json` has `run.status=completed` and validates against the
current bytes. The first three relative Ritz values change by at most
`4e-15` between sizes 14 and 18; the first three positive total Ritz values
change by at most `3.9e-9` between sizes 10 and 14. Increasing quadrature to
192 changes the first three low eigenvalues by at most `1.4e-11`. These
are numerical convergence controls, not interval error bars. At quadrature
128 the largest raw translation stiffness entry is `2.6e-12`, and the largest
integrated dipole of a retained positive total mode is `8.9e-14`.

`check_static_source.py` independently evaluates (19) at 80 decimal digits,
compares all six recorded Ritz probe wavenumbers, and directly integrates (18)
at `q=.1,1,3`. `run_static_001/manifest.json` also completed and validates.
The largest Ritz/kernel relative discrepancy is `6.6e-9`;
the tolerance is `1e-6` and is relevant at the smallest source amplitudes.
The analytic kernel is independently derived from the static field equations;
the finite agreement does not establish its general validity by enumeration.

Both commands use the installed computation-audit runner with wall limit
45 seconds, CPU limit 30 seconds and conventional numerical thread limit one;
no hard memory or affinity cap was requested. The command argv, interpreter,
software versions, elapsed time, dirty Git state, input hashes and output
hashes are in the manifests. Regeneration requires fresh output directories;
the original child argv arrays are the manifest `command` entries.

Outcome: **analytic conditional shared-state construction with bounded
numerical spectrum/source controls**. The fluid closure, matched scalar
regime, common-profile composition and lack of finite-GP edge control remain
explicit assumptions. This example proves neither an obstruction for every
shared state nor the desired dipole medium. A useful next test is unequal
profiles in a physically specified baryon closure, where the compensated and
total channels mix and their actual source matrix elements must be solved.
