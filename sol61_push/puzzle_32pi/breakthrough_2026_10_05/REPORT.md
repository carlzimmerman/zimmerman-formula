# A stronger NR action obstruction and an orbital sum rule

Checkpoint **SOL61-32PI-BREAKTHROUGH-2026-10-05**. Owner: research subagent
`puzzle_32pi`. Shared base `a36191815030afddf1277d413f488fb0c3ac520f`;
actual input hashes and execution environment are in `manifest.json`.
Write scope is this directory alone. No commits, peer edits or global ledger edits.

**The target C = Lambda c^4/a0^2 = 32pi remains unproved.** New progress is
(1) an explicit lift of the previously known interpolation freedom into
exchange-symmetric two-potential NR actions whose full spatial Hessian is
positive away from the standard MOND degeneracy, and (2) an exact same-action
orbital-frequency sum rule and finite-window falsification bound. The first
result strengthens the admissibility scope; the second gives a new necessary
observable condition. Neither is a covariant ghost-freedom theorem.

## Contract, sources and conventions

The target uses vacuum density, not total cosmological density. Throughout the
mathematical derivation c=1, and G is the measured high-acceleration Newton
constant. Restore c by the definition of C above. Let y=g_N/a0>0 and
nu(y)=1+e(y). Assume isolated spherical sources without twin matter, minimal
matter coupling to the physical potential phi, and the alpha=beta=1 NR energy

a0-independent positive prefactor times

    W(p,ph)=|p|^2+|ph|^2-a0^2 M(|p-ph|^2/a0^2),
    p=grad phi, ph=grad phihat.

The NR Lagrangian is -W/(8pi G)-rho phi plus matter kinetic energy. Convexity
below refers to W, the static gradient energy, not to this sign-reversed
Lagrangian or a Hamiltonian for time-dependent relativistic fields.

The primary source [Milgrom, arXiv:0912.0790v2](https://arxiv.org/html/0912.0790v2)
was checked directly: equations (1)-(2) give this NR two-potential action and
source equations; (24), (84)-(87) give the proportional-metric vacuum terms.
For alpha=beta=1 choose f(kappa)=(kappa+kappa^-1)/2, so f(1)=1 and f'(1)=0;
then the identical-metric vacuum coefficient is -M(0)/2. The source states no
principle selecting M(0). The inference from a positive spatial Hessian to a
healthy relativistic spectrum is absent and is not made here.

Project p25 fixes the additive convention M(infinity)=0. Adopt it, without
claiming it is a physical necessity. With an independent additive shift b,
C changes to C-b/2 and the orbital sum rule measures C+b/2 instead. A separate
matter vacuum term would also spoil identification of this sector's C with
the total observed Lambda. Both restrictions are explicit hypotheses.

All exact new identities below are derived here. The source supplies the action
and conditional vacuum dictionary, not the convexity or orbital sum-rule proof.
This source extraction has been authenticated online but no new PDF cache or
shared literature ledger was written.

## 1. Lifting the response into a full NR action

Varying both potentials and taking spherical source fluxes gives, with
x*=|p-ph|/a0 and m=M'(x*^2),

    y=(1-2m)x*,  g/a0=(1-m)x*.

Consequently the inverse constitutive dictionary is

    x*=y(1+2e),  m=e/(1+2e),  z=x*^2.

Assume e>0, x*(0)=0, x*(infinity)=infinity and

    D(y)=dx*/dy=1+2e+2y e'>0.

Then y to x* is a global increasing bijection. The formula for m defines a
single-valued M'(z), and M(z)=-integral_z^infinity m(s) ds fixes its primitive
when the tail integral converges. Thus this is an actual two-potential action,
not an arbitrary response graph or an elimination of the saddle-form QUMOND
auxiliary field.

Rotate the entire six-dimensional gradient space using
u=(p+ph)/sqrt(2), v=(p-ph)/sqrt(2). The energy becomes

    W=|u|^2+|v|^2-a0^2 M(2|v|^2/a0^2).

The Hessian eigenvalues are

    common block:             2, 2, 2;
    difference transverse:    2(1-2m)=2/(1+2e), twice;
    difference radial:        2(1-2m-4z M'')=2/D.

The last equality follows from differentiating y=x*(1-2m). This proves
positivity in every direction when |p-ph|>0. It also proves ellipticity of the
static two-potential source system there; no auxiliary-field elimination is
being used. As y goes to zero, the MOND difference block tends to zero.
The energy remains strictly convex: its radial difference derivative vanishes
at the origin and increases strictly at every positive radius. Its deep-MOND
leading term is positive and cubic in |v|. **Uniform ellipticity including the
zero-difference field is false.** This is the standard NR MOND degeneracy,
and it is preserved by our tail perturbation.

For the known cutoff law e=a/(1+q), a=sqrt(1+1/y)-1, q=(y/T)^2, write s=sqrt(1+1/y):

    D=1+(s-2+1/s)/(1+q)-4a q/(1+q)^2.

The middle numerator is (s-1)^2/s>=0. If y>=1, use a<=1/(2y) and
4q/(1+q)^2<=1 to obtain D>=1/2. If 0<y<=1, use a<=y^-1/2 to obtain
D>=1-4/T^2. Hence **T>=sqrt(8) gives D>=1/2 globally for y>0**.
Both x* endpoint conditions follow from the unchanged deep-MOND and y^-3 tails.

Now use the previous compact C2 bump phi(t)=t^3(1-t)^3 on Y<y<2Y:

    delta e=epsilon phi((y-Y)/Y), zero elsewhere.

Here |phi|<=1/64 and |phi'|<=3/16. Since y<=2Y on its support,

    |delta D|<=2|epsilon|/64+4|epsilon|*3/16
               =25|epsilon|/32.

Therefore D remains positive whenever |epsilon|<16/25. The far tighter
monotonicity and excess-positivity controls below apply to our concrete pair.
For T=128.9153707043, Y=1000 and epsilon=28/(30 million), the actual value is
9.333333333333e-7. On [Y,2Y],

    -e_base' >= a(2Y)(2Y/T^2)/(1+(2Y/T)^2)^2
                =5.14995954303e-10,
    |delta e'| <=3|epsilon|/(16Y)=1.75e-10.

For the negative bump, e_base>=a(2Y)/(1+(2Y/T)^2)>|epsilon|/64, so e stays
positive. These strict inequalities establish an open two-sided epsilon
interval of positive, monotonically decreasing kernels, globally invertible
source maps, and strictly convex NR static energies. The low-y source law is
identical through y=1000 and the complete tail is identical after y=2000.

The action's local derivatives coincide outside the support in the response
variable. Its primitive differs by a constant below that support: that is
precisely why the gravitating vacuum coefficient changes while the NR source
law remains identical. We do not claim the primitive itself is unchanged.

## 2. Exact vacuum normalization and the surviving freedom

Let I=integral_0^infinity 2y e(y)dy and J=integral_0^infinity m(z)dz.
The spherical dictionary implies the exact identity

    m dz -2y e dy=d[2y^2 e^2].

For the cutoff/bump kernels this boundary term vanishes at both endpoints:
deep MOND gives y^2 e^2=O(y), and the y^-3 UV tail gives O(y^-4).
Thus J=I, M(0)=-J, and the chosen vacuum convention gives

    C=-M(0)/2=J/2=integral_0^infinity y e(y)dy.

The bump changes it by

    delta C=epsilon Y^2 integral_0^1 (1+t)t^3(1-t)^3 dt
            =3epsilon Y^2/280.

Our baseline reproduces 32pi to the precision of the rounded T input;
the two perturbed actions yield C_base plus or minus 0.01 exactly.
This is stronger than the earlier functional freedom result: the freedom
survives positive full NR spatial Hessians, the physical source inversion,
exchange symmetry and a fixed additive convention. It still does **not**
produce two healthy full covariant BIMOND theories. The missing arrow is
admissibility under a covariant constraint/spectrum analysis, followed by a
physical principle that selects the full M and its additive vacuum value.

## 3. Same-action orbital sum rule and a falsifiable lower bound

This continuation seeks positive information after the coefficient-selection
route fails. Outside an isolated spherical body of fixed mass M_b,

    y=G M_b/(a0 r^2), g=(G M_b/r^2)nu(y).

For an exactly circular orbit and infinitesimal radial oscillations, derive
from the central-force effective potential (fixed angular momentum)

    Omega^2=g/r,
    kappa_r^2=g'+3g/r,
    R=kappa_r^2/Omega^2=1-2y nu'/nu.

No small-MOND-correction expansion is used. For these monotone kernels R>=1,
so the circular orbits are radially stable and apsidal precession is retrograde.
The angle shift per radial cycle is exactly

    Delta varpi=2pi(R^-1/2-1).

Assume also [y^2 e]_0^infinity=0, which our kernels satisfy. Integrating by parts
now gives the independent same-action identity

    C=-(1/2) integral_0^infinity y^2 e' dy
      =(1/4) integral_0^infinity y nu(y)[R(y)-1]dy.

Equivalently, replace R by (1+Delta varpi/(2pi))^-2. This ties the conditional
vacuum coefficient to the full acceleration spectrum of isolated orbital
response. It is a genuine necessary condition with physical response on the
right-hand side, while the older algebraic postulate had a free positive I.
It does not select C without measurements or a microscopic law.

Monotonicity makes the integrand nonnegative. Therefore for ANY finite
acceleration interval [y1,y2],

    C >= (1/4) integral_y1^y2 y nu(y)[R(y)-1]dy.

Under this sector-only vacuum identification, **a certified measured
finite-window lower bound greater than 32pi falsifies the exact target**.
This criterion is independent of the fitted cutoff shape or compact-tail
completion. The converse is false: a small partial integral does not prove
32pi. Unmeasured positive response can supply the remainder.

Scope is essential: galaxies modeled as discs do not have y proportional to
r^-2, so disc epicyclic frequencies cannot be inserted into this bound.
Actual Solar System tests also require external-field, multipole, relativistic,
baryonic-mass and observational modeling. The isolated spherical theorem is
not a claim that existing planetary residuals measure its integral.

For the fitted baseline, at y=T the action predicts kappa_r/Omega=1.0038523981,
Delta varpi=-0.02411244038 radians per radial cycle, and delta g/a0=0.2495170571.
At y=1000 the corresponding angle is -0.00015233466 radians. These are idealized
same-action predictions; T is still fitted to C, so they test the complete
cutoff mechanism rather than independently derive the target.

## Attempts, audit and next executable step

1. Tried using exchange symmetry plus NR admissibility as a UV selector.
   It fails: the constructive two-sided action family preserves those premises.
   This closes that particular selector, not every covariant mechanism.
2. Continued to a full Hessian/source-map analysis. It succeeds as a scoped
   obstruction, with the origin degeneracy explicitly retained.
3. Continued to the exact orbital response integral. It succeeds as a new
   necessary condition and one-sided falsification bound. No observational
   bound has been claimed or extracted from non-spherical data.

Self-audit verdict: **correct only with the stated NR, additive-vacuum,
monotonicity and isolated-spherical restrictions**. The coordinator separately
rederived the orbital ratio, sign, integration factor and boundary condition.
The numerical grids are corroboration, not the global proof.

Dependency obligations: action/source dictionary passed against the primary
source and symbolic reconstruction; Hessian positivity passed analytically for
nonzero difference field; zero-field uniform ellipticity failed and is excluded;
primitive normalization passed with M(infinity)=0; orbital sum rule passed with
the explicit boundary condition; covariant health and total-vacuum identity are
conditional and unproved; extraction of a real finite-window measurement is
not addressed.

Reproduce with `python3 sol61_push/puzzle_32pi/breakthrough_2026_10_05/checks.py`.
It writes only this directory's `manifest.json`; redirect stdout here if desired.
The computation uses 50-digit quadrature, exact SymPy identities, derivative
bounds and an independently reconstructed six-component Hessian on 161 log
samples from 1e-8 to 1e8 for each of the two positive-bump/baseline kernels.
Controls reject a doubled integral normalization and a wrong radial Hessian sign.
Negative-bump positivity and its exact -0.01 shift are checked separately.

Novelty is project-relative: neither the Hessian lift nor this orbital sum rule
appears in the reviewed p25/p35/p38/p44-p46 and Sol61 closure records. Limited
web discovery used the queries 'BIMOND vacuum integral epicyclic frequency sum
rule' and 'BIMOND convex nonrelativistic Lagrangian interpolation function
ellipticity', then the 2009 primary source. This is not an exhaustive literature
search or a global novelty claim; the epicycle identities and convexity method
are elementary standard consequences of the specified action.

Next step: formulate a spherical-system inference for nu and R with shared
mass and a0 errors, certify the weighted partial integral, and compare its lower
bound with 32pi. Alternatively, audit a specific covariant completion's kinetic
and constraint spectrum against the explicit perturbation family. Without an
identified completion or a suitable spherical response data set, these remain
open continuations, not an impossibility theorem.

A standard bounded computation-audit execution is preserved in
`runs/nr_action_orbit/manifest.json`, with pinned before/after input hashes,
stdout/stderr and `scientific_results.json`. Its contract is `contract.json`;
the supplemental top-level manifest is from the direct execution.
