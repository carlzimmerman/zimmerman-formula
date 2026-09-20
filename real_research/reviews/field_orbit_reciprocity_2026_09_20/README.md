# Completion-independent field–orbit compatibility

Checkpoint: 2026-09-20, starting repository revision
`3cbbba74d7f91b555664d54bdbae707b554fac24`. Other sessions are editing the repo.
Scope: the local static action class containing the auxiliary action in
`../kappa_unit_response_2026_09_20/README.md`, not every covariant sector in this
repository and not every particle-free theory.

## The stronger test

For an arbitrary differentiable positive response `mu(g)` in

\[
\nabla\!\cdot[\mu(|\nabla\Phi|)\nabla\Phi]=4\pi G\rho_b,
\]

define two quantities in **different physical configurations** at the **same
physical acceleration** `g_e`:

1. `beta(g_e)=d ln v_c/d ln r`, measured outside an isolated spherical baryonic
   source at a radius where its acceleration is `g_e`.
2. `E(g_e)=g_internal,parallel/g_internal,perpendicular`, the force magnitude
   produced by a small compact source at equal distances along and perpendicular
   to a uniform background field of magnitude `g_e`. Subtract the background
   field. Use the leading external-field-dominated, point-source far-field limit.

Then

\[
\boxed{\mathcal E(g_e)^2[1-2\beta(g_e)]=2.}
\]

The unknown interpolation function, its normalization, `a0`, `s`, the relative
action weight, the source masses and the radial units cancel from this relation.
This cancellation assumes the **same universal response function** in the two
configurations; matching dimensionless accelerations by separately fitting each
object's scale would not be an independent test.

The mathematical result is exact for the linearized external-field problem.
Actual finite-strength internal fields, finite source sizes and external tides
produce corrections requiring a further calculation. A detected discrepancy is
not automatically a rejection unless these physical and observational errors
are controlled.

## Derivation, including the missing geometric information

Put `L_e=g_e mu'(g_e)/mu(g_e)` and `Gamma=1+L_e>0`. The constitutive Jacobian is

\[
J_{ij}=\mu_e\delta_{ij}+g_e\mu'_e\hat e_i\hat e_j.
\]

Its transverse and longitudinal eigenvalues are `mu_e` and `mu_e Gamma`.
Taking the background along `z`, the perturbation equation is

\[
\mu_e(\partial_x^2+\partial_y^2+\Gamma\partial_z^2)\phi
 =4\pi GM\delta^{(3)}(\mathbf r).
\]

Its leading point-source Green function is

\[
\phi=-\frac{GM}{\mu_e\sqrt{\Gamma(x^2+y^2)+z^2}}.
\]

Differentiation along the two axes at equal radius gives `E=sqrt(Gamma)`.
Meanwhile, the isolated exterior obeys `r²g mu(g)=GM_b`. Differentiating and
using `v_c²=rg` gives `Gamma(1-2 beta)=2`. Eliminate `Gamma` to obtain the box.

This is a test of the structure of the static field equation. If the two measured
quantities violate it under the specified hypotheses, **no choice of mu(g)** can
fit both. Lean proves precisely this incompatibility as `no_response_retuning`.
Changing the action class or invalidating a physical hypothesis remains possible.

For an extended spherical isolated source, put `m=d ln Mb(<r)/d ln r` and the
right-hand side becomes `2-m`; the exterior formula must not be applied inside
the source or to a disk using enclosed mass as if it were spherical.

## A substantive negative control: identical isolated curves, different fields

QUMOND can have the same isolated spherical relation through `mu(g)nu(gN)=1`,
where `gN=g mu(g)`. Write `K=d ln nu/d ln gN`, so `(1+L)(1+K)=1`.
Its external-field Green function instead gives `E=1/(1+K/2)`. Thus

\[
\boxed{\mathcal E_{\rm QUMOND}(g_e)[3-2\beta(g_e)]=4.}
\]

The external-field comparison uses the corresponding physical/Newtonian
backgrounds related by `g_e=nu(gN_e)gN_e`, as in the primary source below.

| Isolated exterior slope beta | Local AQUAL E | QUMOND E |
| --- | --- | --- |
| -1/2 (Newtonian limit) | 1 | 1 |
| -1/4 | sqrt(4/3) | 8/7 |
| 0 (deep-MOND limit) | sqrt(2) | 4/3 |

The last pair differs by about **6.07% in the force ratio**. This is not a
6.07% prediction for a projected velocity statistic or an observational detection
significance. It proves that perfect isolated rotation curves do not by
themselves identify the multidimensional gravitational field equation.

## Signed effective-density route

Away from the compact source, the same Green function gives

\[
\rho_{\rm eff}=\frac{M(\Gamma-1)}{4\pi\mu_e}
\frac{2z^2-\Gamma R^2}{(\Gamma R^2+z^2)^{5/2}},\qquad R^2=x^2+y^2.
\]

For `Gamma>1` it is negative in equatorial directions and positive near the
external-field axis. The zero-density cone has
`tan²(theta_0)=2/Gamma=1-2 beta`, with theta measured from that axis. In the deep
limit its half-angle is 45 degrees. At `Gamma=1`, the whole exterior effective
density vanishes, so the formal cone has no sign-boundary interpretation.

This is the **inferred Newtonian Poisson source**, not a density of dark particles
and not automatically the action's physical stress-energy density. It is not a
lensing prediction without a relativistic metric/slip calculation. Negative
phantom-density regions themselves are established MOND phenomenology.

## Literature, novelty and executed routes

The point-source external-field solutions are **known**, not discovered here.
Primary source checked on 2026-09-20: Indranil Banik and Hongsheng Zhao,
[*The External Field Dominated Solution In QUMOND & AQUAL: Application To Tidal
Streams*, arXiv:1509.08457v3](https://arxiv.org/html/1509.08457v3),
sections 2–3, equations (11), (17)–(20), (22), (36)–(38). The source explicitly
states the deep AQUAL anisotropy sqrt(2); QUMOND's 4/3 follows from its supplied
potential and K=-1/2. The older AQUAL calculation is credited there to Bekenstein
and Milgrom (1984) and Milgrom (1986).

Classification: **a formal observable-level compatibility corollary of known
field equations**, with a Lean certificate and explicit no-retuning formulation.
There is no established new fundamental law or global novelty claim. The exact
combined presentation was not located in the bounded search, which is not
evidence of global priority.

Search scope: repository source/text search for orbital slope, anisotropy and
external fields; web exact/synonym searches for `AQUAL external field anisotropy
rotation curve slope relation`, `rotation curve slope anisotropy MOND external`,
and `MOND external field potential negative phantom density cone`. One primary
version was read fully in the relevant sections; no authenticated local source
cache or exhaustive citation census was created.

Routes executed: (1) arbitrary-response constitutive-Jacobian and orbital-slope
elimination; (2) QUMOND countermodel with identical spherical response, establishing
the class boundary; (3) effective-density sign/cone calculation, retained as a
geometric corollary with explicit literature and lensing limitations.

## Evidence and remaining work

`Reciprocity.lean` proves eleven statements, including the general spherical
flux derivative, the combined conditional theorem, no-response-retuning,
the distinct QUMOND relation and the cone-angle elimination. Standard axioms
only, no `sorry`. The Green-function-to-force relation is an explicit premise
of the combined Lean theorem, **not** a formalized 3D PDE theorem.

`verify.py` separately checks the generic 3D constitutive Jacobian, the Green
equation away from the source, its integrated source normalization, axial forces,
and effective-density expression with exact SymPy operations. It then checks 84
finite-difference cases across four response functions and four numerical source
flux integrals. These are checks of the linearized construction, not a nonlinear
global external-field solver. Raw evidence and an input-hash manifest are in
`certified/`; preliminary direct output is in `run/`.

The next substantial physical task is an end-to-end forecast or measurement of
the internal-force anisotropy, including geometry, external tides, finite internal
field and projection, matched to the isolated-source slope at the same physical
acceleration. Existing projected binary speeds are not this ratio without a
dynamical population model. The present theorem supplies a target; it does not
claim that the required measurement already exists.

Self-review and math proofreading covered the displayed signs, axes, positive
ellipticity condition, source normalization, ordinary test-body inertia, matched
acceleration, dimensional factors, asymptotic scope, and distinction between
physical stress and inferred Poisson density. No independent-agent review.
