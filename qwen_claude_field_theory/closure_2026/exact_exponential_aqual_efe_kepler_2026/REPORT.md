# Exponential-AQUAL external-field Kepler and two-clock laws

Date: 2026-09-03

Verdict: **PASS_NONRELATIVISTIC_EFD_CALCULATION; NOT a relativistic
completion.**  Both results are repository-new observable extractions from
known structures.  The finite-eccentricity nodal law is a MOND specialization
of a known first-order averaged spatial anisotropic-Kepler Hamiltonian; the
general-\(q\) core clock ratio extends a homogeneous-sphere EFD coordinate
stretch already used in MOND.  Neither is claimed globally novel.  The
circular limit is prior-art arithmetic and is labelled as such.

## 1. One action, varied first

Take the nonrelativistic AQUAL action

\[
 S_{\rm AQUAL}=-\int dt\,d^3x\left[
 {a_0^2\over8\pi G}{\cal G}\!\left({|\nabla\Phi|\over a_0}\right)
 +\rho\Phi\right],
\]

with

\[
 {\cal G}(y)=y^2+2(1+y)e^{-y}-2,
 \qquad {{\cal G}'(y)\over2y}=1-e^{-y}\equiv\mu(y).
\]

The live symbolic variation in `symbolic_action_audit.py` obtains

\[
 {\partial {\cal L}\over\partial(\partial_i\Phi)}
 =-{1\over4\pi G}\mu(|\nabla\Phi|/a_0)\partial_i\Phi,
\]

and hence

\[
 \boxed{\nabla\!\cdot\!\left[(1-e^{-|\nabla\Phi|/a_0})\nabla\Phi\right]
 =4\pi G\rho.}
\]

No phenomenological force law is inserted after the variation.

Put a constant external field along `+z`,
\(\nabla\Phi=\mathbf g_e+\nabla\phi\), and keep the first order in the
internal field.  Defining

\[
 \eta={g_e\over a_0},\qquad
 \mu_e=1-e^{-\eta},\qquad
 L_e={d\ln\mu\over d\ln g}\bigg|_e={\eta\over e^\eta-1},
 \qquad q=1+L_e,
\]

the flux Jacobian is calculated, rather than assigned, as

\[
 D[\mu\mathbf g]\big|_e
 =\operatorname{diag}\!\left(\mu_e,\mu_e,\mu_e+\eta e^{-\eta}\right)
 =\mu_e\operatorname{diag}(1,1,q).
\]

Thus the external-field-dominated (EFD) equation is

\[
 \boxed{\mu_e(\partial_x^2+\partial_y^2+q\partial_z^2)\phi
 =4\pi G\rho.}
\]

For every finite \(\eta>0\), both eigenvalues are positive.  At the exact
\(\eta=0\) endpoint they vanish; the scripts retain that point only as a
one-sided ratio limit and never call it an elliptic EFD problem.

## 2. Point source: the prior-art circular anchor

The Green solution is

\[
 \phi(R,z)=-{GM\over\mu_e\sqrt{z^2+qR^2}}
 =-{k_e\over r\sqrt{1-\epsilon_e\cos^2\theta}},
\]

where

\[
 k_e={GM\over\mu_e\sqrt q},\qquad
 \epsilon_e={L_e\over1+L_e}.
\]

For an infinitesimal vertical perturbation of an equatorial circular orbit,

\[
 \Omega_\phi^2={GM\over\mu_e\sqrt q\,R^3},\qquad
 \nu_z^2={\Omega_\phi^2\over q}.
\]

Consequently

\[
 \boxed{T_\phi^2={4\pi^2\mu_e\sqrt q\over GM}R^3},\qquad
 {\nu_z\over\Omega_\phi}=q^{-1/2}.
\]

The unambiguous beat rate is

\[
 \dot\Omega_{\rm node}=\Omega_\phi-\nu_z.
\]

It gives \(2\pi(1-q^{-1/2})\) radians over one azimuthal period, or
\(2\pi(\sqrt q-1)\) radians between consecutive vertical cycles.  This
circular result is an immediate corollary of the published EFD Green
function and its squared frequency ratio was already present elsewhere in
the repository.  **It is not the new result.**

## 3. Finite-eccentricity external-field nodal law

Expand the same exact EFD potential only in \(\epsilon_e\):

\[
 \delta H=-{k_e\epsilon_e\over2r}\cos^2\theta+O(\epsilon_e^2).
\]

For an unperturbed ellipse, let \(i\) be the angle between orbital angular
momentum and `+z`, \(\omega\) the argument of periapsis from the ascending
node, \(e\) the eccentricity, and

\[
 s=\sqrt{1-e^2},\qquad \alpha={e\over1+s}.
\]

Because \(dt/r=dE/(na)\), the required average is uniform in eccentric
anomaly.  The symbolic audit derives

\[
 {1\over2\pi}\int_0^{2\pi}\cos(2f)\,dE=\alpha^2,
 \qquad
 {1\over2\pi}\int_0^{2\pi}\sin(2f)\,dE=0.
\]

The averaged perturbation is therefore

\[
 \langle\delta H\rangle
 =-{k_e\epsilon_e\over4a}\sin^2 i
 \left[1-\alpha^2\cos(2\omega)\right].
\]

Using Delaunay actions and differentiating with respect to the action
conjugate to the node gives the exponential-AQUAL timing specialization

\[
 \boxed{
 P\dot\Omega_{\rm node}
 =\pi{L_e\over1+L_e}{\cos i\over\sqrt{1-e^2}}
 \left\{1-\left[{e\over1+\sqrt{1-e^2}}\right]^2
 \cos(2\omega)\right\}
 +O\!\left(\epsilon_e^2,{g_{\rm int}\over g_e}\right).}
\]

Here \(P=2\pi\sqrt{a^3/k_e}\) is the unperturbed Kepler period; replacing it
by the measured perturbed period changes the product only at
\(O(\epsilon_e^2)\).  The displayed dependence on \(e,i,\omega\) is
untruncated at the retained first order in \(\epsilon_e\), not exact to all
anisotropy orders.  Uniform perturbative validity near \(e\to1\) additionally
requires \(\epsilon_e/\sqrt{1-e^2}\ll1\), and the whole orbit must remain EFD,
\(\max(g_{\rm int}/g_e)\ll1\).  The bracket is strictly positive for
\(0\le e<1\), so the sign is fixed: prograde orbits advance, retrograde
orbits regress, and polar orbits have zero secular node rate in the stated
right-handed convention.

### Direct unexpanded-orbit calibration

`independent_orbit_audit.py` integrates the unexpanded force of the linearized
EFD Green solution without importing the analytic module.  For \(e=0.3\), \(i=20^\circ\), and
\(\omega=40^\circ\):

| external field | first-order law | exact 3-D first node step | relative error |
|---|---:|---:|---:|
| \(\eta=6\) | 2.594126 deg/orbit | 2.603718 deg/orbit | 0.3697% |
| \(\eta=2.47812944\) | 32.664056 deg/orbit | 35.129135 deg/orbit | 7.5468% |

Each row is the change in the osculating angular-momentum node from the initial
periapsis to the next periapsis, not a long-time mean or monodromy frequency.
The second row is deliberately not advertised at first-order precision: its
7.55% mismatch shows that a full unexpanded averaged-system or long-arc
integration is required when \(\epsilon_e\simeq0.185\).  The direct small-tilt
frequency integration at \(\eta=1\) agrees with \(q^{-1/2}\) to
\(4.4\times10^{-11}\) relative.

## 4. Uniform spherical source: boundary-matched two-clock law

The local operator alone does **not** determine an interior Hessian.  For a
prescribed homogeneous physical sphere, the coordinate change
\(z'=z/\sqrt q\) turns the equation into ordinary Poisson on an oblate
ellipsoid with axes \((R,R,R/\sqrt q)\).  With

\[
 \xi=\sqrt{q-1}=\sqrt{L_e},
\]

the ellipsoid depolarization factors are

\[
 N_\parallel={1+\xi^2\over\xi^3}(\xi-\arctan\xi),
 \qquad N_\perp={1-N_\parallel\over2}.
\]

The physical interior frequencies follow only after transforming back:

\[
 \boxed{\omega_\perp^2={4\pi G\rho\over\mu_e}N_\perp,\qquad
 \omega_\parallel^2={4\pi G\rho\over\mu_e q}N_\parallel.}
\]

Hence

\[
 \boxed{{T_\parallel\over T_\perp}
 =\sqrt{{qN_\perp\over N_\parallel}}.}
\]

In the deep external-field limit,

\[
 N_\parallel={4-\pi\over2},\qquad
 N_\perp={\pi-2\over4},
\]

so the clean parameter-free clock ratio is

\[
 \boxed{{T_\parallel\over T_\perp}
 =\sqrt{{\pi-2\over4-\pi}}
 =1.1532112482813996\ldots.}
\]

The absolute deep-EFD laws are

\[
 \omega_\perp^2=\pi(\pi-2)G\rho{a_0\over g_e},\qquad
 \omega_\parallel^2=\pi(4-\pi)G\rho{a_0\over g_e},
\]

\[
\boxed{\rho T_\perp^2={4\pi g_e\over Ga_0(\pi-2)},\qquad
 \rho T_\parallel^2={4\pi g_e\over Ga_0(4-\pi)}.}
\]

These are a joint asymptotic limit with \(0<g_e\ll a_0\) and
\(\max(g_{\rm int}/g_e)\to0\).  Sending \(g_e\to0\) at fixed source would
leave the EFD regime and is not licensed by these equations.

The older local-operator shortcut would give
\(T_\parallel/T_\perp=\sqrt2=1.4142\ldots\), 22.63% too high relative to the
correct boundary-matched value.  Numerical
quadrature of the general ellipsoid integral independently reproduces both
depolarization factors.  This calculation is a prescribed-source harmonic
response, not a proof that an isotropic distribution function remains a
uniform sphere in equilibrium.

## 5. What this does and does not buy

It buys two concrete, conditional benchmarks derived from the specified
exponential AQUAL action in its linearized EFD regime:

1. a finite-eccentricity/inclination nodal timing surface in the EFD branch;
2. a corrected boundary-matched internal two-clock ratio for a uniform core.

It does **not** revive the HPI-Delta relativistic lift.  That candidate remains
dead under the committed regular-center and Solar-\(Q_2\) gates.  This bundle
does not count relativistic degrees of freedom, derive PPN parameters, cure the
zero-field curvature singularity, or provide a causal covariant screening
sector.  The full relativistic target therefore remains **OPEN as a theory
space and unconstructed as a surviving candidate**.

## 6. Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover \
  -s qwen_claude_field_theory/closure_2026/exact_exponential_aqual_efe_kepler_2026 \
  -p 'test_*.py' -v

PYTHONDONTWRITEBYTECODE=1 python3 \
  qwen_claude_field_theory/closure_2026/exact_exponential_aqual_efe_kepler_2026/symbolic_action_audit.py \
  --output qwen_claude_field_theory/closure_2026/exact_exponential_aqual_efe_kepler_2026/symbolic_action_results.json

PYTHONDONTWRITEBYTECODE=1 python3 \
  qwen_claude_field_theory/closure_2026/exact_exponential_aqual_efe_kepler_2026/independent_orbit_audit.py \
  --output qwen_claude_field_theory/closure_2026/exact_exponential_aqual_efe_kepler_2026/orbit_audit_results.json

PYTHONDONTWRITEBYTECODE=1 python3 \
  qwen_claude_field_theory/closure_2026/exact_exponential_aqual_efe_kepler_2026/exact_exponential_aqual_efe_kepler_2026.py \
  --output qwen_claude_field_theory/closure_2026/exact_exponential_aqual_efe_kepler_2026/calculation_results.json
```

All four commands must exit zero.  Tests include negative controls for the old
\(1/q\) uniform-core shortcut, a swapped/missing anisotropy through direct 3-D
integration, strict JSON at \(\eta=0\), and the Newtonian isotropic limit.
