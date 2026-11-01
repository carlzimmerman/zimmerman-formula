# Restricted radial PN28 field-response calculation: independent theory review

**Verdict: correct only after a stated restriction.** The potential-energy
Hessian and positive quadratic inertia below define a radial linear
fluid-plus-scalar model about the supplied static PN28 halos. A negative
admissible Hessian direction implies a negative squared frequency in this
declared model. It does not establish instability of the unrestricted
multistream/Vlasov parent. A positive finite set of trial directions does not
establish stability of even this reduced model.

This is an independent analytic reconstruction by `/root/core_gap_check`,
2026-11-01. It uses the stated action and static energy, not the coordinator's
numerical implementation or eigenvalue results. The only written artifact of
this review is this file. No numerical stability verdict is asserted here.

## Exact inputs and claim

The audited source revisions are identified by SHA256:

| Source | SHA256 |
|---|---|
| `pressure_selection_2026_10_28/dispersion_coupling/REPORT.md` | `6deea173491b9c8e4d88b528ac0895faf2c6ec99273aa86c9d6e73d7c7d8537d` |
| `pressure_selection_2026_10_28/dispersion_coupling/EOS.md` | `05f919345cb73c8b96e3f07d5fdb421ae8ee1d24a01e177abc9551aab4092274` |
| `pressure_selection_2026_10_28/finite_gradient/DERIVATION.md` | `8b6d501f0ddfa522c5a9cafe6c90592a007bb5b80575bbbf0d302d0135b0d970` |

The quantified background is any regular spherical static solution of that
finite-gradient problem with `0 < psi_c < 1`, finite matter radius `R`, and
decaying scalar `s_0`. The constants `k, B, C_s, F^2` are positive and fixed;
`C_s=F^2 c_s^2`. Newtonian gravity is sourced only by the conserved matter
density. The potential/vacuum amplitude ratio and the phase-space occupancy
are not selected by this calculation.

The tested perturbation consists of a radial Lagrangian mass displacement
`xi(r,t)` inside the matter and an Eulerian scalar perturbation `sigma(r,t)`
throughout space. It preserves total matter mass. The isotropic fixed-level
relation `K=k rho^(5/3)` is imposed as a dynamical fluid closure. Exterior
scalar inertia uses `partial_t sigma`, with no exterior material velocity.
These are explicit restrictions, not deductions about general kinetic
evolution or arbitrary crossings of vacuum.

## 1. Potential energy and its second variation

Write the energy relative to its vacuum baseline as

```text
E[rho,s] = integral { e(rho,s) + (C_s/2)|grad s|^2
                       + (1/2)rho Phi } d^3x,
e(rho,s) = k rho^(5/3) exp(-2s) + B[exp(3s)-3s-1],
Delta Phi = 4 pi G rho,             Phi(infinity)=0.
```

Define `E_rel=k rho_0^(5/3) exp(-2s_0)` and the first density variation

```text
q = delta rho = -(1/r^2)(r^2 rho_0 xi)',
delta m(r) = -4 pi r^2 rho_0 xi.
```

Regular radial displacement has `xi=O(r)` at the center and remains finite
at the matter edge. Since `rho_0` vanishes there, `delta M=0` without fixing
`xi(R)=0`. A rigid matter boundary is not part of this calculation.

The interior energy curvatures are

```text
a = e_rhorho = (10/9) E_rel/rho_0^2,
b = e_rhos   = -(10/3) E_rel/rho_0,
c = e_ss     = 4 E_rel + 9 B exp(3s_0).
```

In the exterior, only the scalar remains, with `c=9 B exp(3s_0)`.
At equilibrium `e_rho+Phi=mu` inside, while the scalar first variation
vanishes everywhere. The second-order changes of the background along any
admissible mass-preserving path therefore drop out of the constrained
Hessian. If `E(lambda)=E(0)+(lambda^2/2)Q+o(lambda^2)`, then

```text
Q[xi,sigma] = integral { a q^2 + 2 b q sigma + c sigma^2
                         + C_s |grad sigma|^2 + q delta Phi } d^3x.
```

The density-dependent terms are integrated only inside the matter. The
scalar terms include its exterior tail. The gravitational term has the
equivalent forms

```text
integral q delta Phi d^3x
  = -(1/(4 pi G)) integral |grad delta Phi|^2 d^3x
  = - integral_inside 4 pi G rho_0^2 xi^2 d^3x.
```

Here `delta Phi'=-4 pi G rho_0 xi`, and spherical mass conservation makes
`delta Phi=0` outside the matter. This is the second variation; its
gravitational coefficient must not acquire an extra factor of `1/2`.

The finite-edge behavior is benign for these perturbations: with
`x=R-r`, `rho_0=O(x^(3/2))`, `q=O(x^(1/2))`, and
`a q^2=O(x^(1/2))`. Thus the divergent pointwise `a` at vacuum is integrable
in the quadratic form. Smooth displacement of this vanishing-density edge
introduces no second-order surface mass or surface-energy term.

## 2. Positive inertia and the linear equations

The declared quadratic kinetic energy is

```text
T_2 = (1/2) integral_inside
          {rho_0 xi_dot^2 + F^2(sigma_dot+s_0' xi_dot)^2} d^3x
      + (F^2/2) integral_outside sigma_dot^2 d^3x.
```

The interior inertia matrix in `(xi,sigma)` is

```text
M = [[rho_0 + F^2 s_0'^2, F^2 s_0'],
     [F^2 s_0',          F^2       ]],
det M = rho_0 F^2 > 0.
```

It is positive wherever matter is present. There is only a scalar variable
in vacuum, with positive inertia `F^2`. A zero-density fluid displacement is
not added as an exterior degree of freedom.

Put `delta h = a q + b sigma + delta Phi`. Variation of
`L_2=T_2-Q/2` gives the following equations inside:

```text
(rho_0+F^2 s_0'^2) xi_ddot + F^2 s_0' sigma_ddot
    = -rho_0 (delta h)',

F^2(sigma_ddot+s_0' xi_ddot)
    = C_s Delta sigma - c sigma - b q.
```

Outside,

```text
F^2 sigma_ddot = C_s Delta sigma - 9 B exp(3s_0) sigma.
```

Use a regular scalar at the center, continuous `sigma` and `C_s sigma'`
at the matter edge, and finite-energy decay at infinity for a bound mode.
The scalar momentum `F^2(sigma_dot+s_0' xi_dot)` need not be continuous across
the edge: the stipulated exterior kinetic continuation is different, and
no spatial derivative of that momentum appears at linear order here.

The conserved quadratic energy is `T_2+Q/2` under these boundary conditions.
For a self-adjoint finite-energy realization of these forms, a direction
with `Q<0` and finite positive inertia lies in the negative spectral
sector and implies linear growth. Every finite-dimensional Galerkin version
has the transparent generalized eigenproblem `H z=omega^2 M z`; positive
`M` and a negative Rayleigh numerator give `omega^2<0`.

This sign test is independent of the unspecified positive `F^2` at fixed
`C_s`; the growth rate is not. The same statement applies to any other
positive inertia declared on this restricted configuration space.

## 3. Exact dimensionless factors

Use PN28's definitions

```text
rho_* = [3B/(2k)]^(3/5),       h_* = 5B/(2rho_*),
ell^2 = h_*/(4 pi G rho_*),   epsilon = C_s/(3B ell^2),
t_* = ell/sqrt(h_*),         v_s^2 = c_s^2/h_*.
```

Let dimensionless `r, xi, n, q, s, psi` denote physical radius divided by
`ell`, displacement divided by `ell`, density divided by `rho_*`, density
variation divided by `rho_*`, and the unchanged dimensionless fields.
The background obeys `n=psi_+^(3/2)exp(3s)` and
`E_rel/B=(3/2)n psi` inside. Then, in units `4 pi B ell^3`,

```text
Q = integral_0^infinity r^2
       [a q^2 + 2b q sigma + c sigma^2 + 3epsilon sigma'^2
        -(5/2)n^2 xi^2] dr,

a = (5/3)psi/n,     b = -5psi,
c = 6n psi + 9exp(3s),       q = -(r^2 n xi)'/r^2.
```

The dimensionless inertia form is

```text
2T_2 = integral_inside r^2
         [(5/2)n xi_dot^2
           +(3epsilon/v_s^2)(sigma_dot+s'xi_dot)^2] dr
       +(3epsilon/v_s^2) integral_outside r^2 sigma_dot^2 dr.
```

Dots here use time `t/t_*`. The factors follow independently from
`rho_* h_*/B=5/2`, `C_s/(B ell^2)=3epsilon`, and
`F^2 h_*/(B ell^2)=3epsilon/v_s^2`.

## 4. Scalar minimization is a valid one-sided instability screen

For a fixed displacement solve, in physical units,

```text
A sigma = -bq,          A = -C_s Delta + c.
```

The positive `c` and scalar gradient form make this a strictly positive
scalar operator with a unique minimizing response under the declared
boundary conditions. Thus

```text
Q_min[xi] = integral_inside [a q^2-4 pi G rho_0^2 xi^2] d^3x
            - <bq,A^(-1)bq>.
```

The dimensionless scalar equation is
`(-3epsilon Delta+c)sigma=-bq`. A negative, converged value is a negative
direction of the full coupled stiffness: eliminating the scalar statically
for this purpose does not assume infinitely fast scalar dynamics. The
minimizing scalar need not be the scalar component of the eventual unstable
eigenmode. It supplies a legitimate initial configuration for the variational
sign test.

There is also a useful local sign check. Write `t=psi^(5/2)`. On every
specified background `0<psi<1` inside, and

```text
a-b^2/c = 5psi(1-t)/[n(3+2t)] > 0.
```

The nongravitational local Hessian is positive, and its gradient contribution
is positive. A negative full `Q` therefore comes from self-gravity overcoming
that support; it is not a negative local compressibility.

At a large finite radius `L`, the static minimizing scalar has asymptotic
Robin condition

```text
sigma'(L) + [sqrt(3/epsilon)+1/L] sigma(L) = 0.
```

If the tail is eliminated using this condition, its stiffness contribution
must be retained as
`3epsilon L^2[sqrt(3/epsilon)+1/L]sigma(L)^2` in `Q`.
This is exact for the linear constant-vacuum exterior and asymptotic for
the decaying nonzero background tail. An explicitly resolved exterior or
longer-domain repetition checks the approximation.

For a growing mode `exp(gamma t)` the physical far-tail decay constant is
`sqrt((9B+F^2 gamma^2)/C_s)`, not the static one. Static Robin elimination is
adequate for the zero-frequency stiffness screen; it must not silently be
used as the exact dynamical exterior at a finite nonnegligible boundary.

Positive values in finitely many polynomial displacement directions only
show that those directions did not reveal an instability. Negative values
need convergence and quadrature checks because an inaccurately computed
minimizing scalar can otherwise contaminate the small residual obtained by
subtracting positive contributions.

## 5. Independent homology identities and a two-direction witness

All integrals in this section are dimensionless and include the scalar
exterior. Define

```text
A = integral (3/2)n psi r^2 dr,
U = integral [exp(3s)-3s-1] r^2 dr,
D = (3epsilon/2) integral s'^2 r^2 dr,
W = (5/2) integral n psi' r^3 dr,
I = integral s (3/2)n psi r^2 dr.
```

Here `A` is an energy, distinct from the scalar operator in section 4.
Under mass-preserving dilation
`n_lambda(r)=lambda^(-3)n(r/lambda)` and
`s_lambda(r)=s(r/lambda)`, the energy is exactly

```text
E(lambda) = A lambda^(-2) + U lambda^3 + D lambda + W lambda^(-1).
```

Stationarity yields `-2A+3U+D-W=0`, the stated virial relation. The trial
`xi=r, sigma=-rs'` must therefore obey

```text
Q_homology = 6A+6U+2W = 2A+12U+2D > 0.
```

Its scalar material-derivative kinetic square vanishes identically. This is
a useful sign and factor check; testing only this co-transported scalar
direction would miss the scalar's relaxing response.

A separate analytic two-direction test also changes scalar amplitude:
`s_lambda,alpha(r)=alpha s(r/lambda)`. At `(lambda,alpha)=(1,1)`, let

```text
H_ll = 6A+6U+2W,
H_la = 10I-4D,
H_aa = integral [4s^2(3/2)n psi+9s^2 exp(3s)] r^2 dr + 2D.
```

For `H_la`, the scalar stationarity identity is
`integral s U'(s) r^2 dr = 2I-2D`; inserting it into the direct mixed
derivative `4I+3 integral s U'(s)r^2dr+2D` gives the displayed result.
Consequently the admissible trial

```text
xi=r,        sigma=-rs'-(H_la/H_aa)s
```

has `Q=H_ll-H_la^2/H_aa`. A negative result here would be an especially simple
independent witness. A positive result does not obstruct a more general
negative displacement or scalar variation. These identities are exact on
the infinite domain; any finite-boundary residual must be accounted for or
shown negligible.

## 6. Forced response and remaining closure limits

A small fixed baryonic potential contributes the linear forcing

```text
delta E_b = integral q delta Phi_b d^3x
          = integral_inside rho_0 xi (delta Phi_b)' d^3x.
```

A static forced solution is meaningful as an adiabatically maintained state
only after the unforced background passes the required stability checks.
Solving a static susceptibility through a negative-energy background does
not establish a viable response mechanism.

The dependency chain is: declared fixed-level isotropic closure and static
energy -> equilibrium equations -> constrained energy Hessian -> declared
positive linear inertia -> variational instability criterion. The first
and fourth links are modeling restrictions. The intervening algebra is
reconstructed above. Numerical discretization and convergence are separate
computational obligations.

| Obligation | Status |
|---|---|
| Mass conservation and Newtonian gravitational Hessian sign | Passed analytically |
| Scalar and density curvature factors | Passed analytically |
| Dimensionless potential and inertia factors | Passed analytically |
| Positive linear inertia in the stated domain | Passed analytically |
| Scalar-elimination sign test | Passed within the declared form realization |
| Full-spectrum stability from positive finite Ritz values | Not established |
| Numerical values and convergence | Separate coordinator computation |
| Arbitrary vacuum-crossing evolution of the stream action | Not established |
| Persistence or generation of isotropic phase-space occupancy | Not established |
| Stability of unrestricted PN28 Vlasov dynamics | Not established |
| Origin of the potential, phase level, or relation between B and vacuum V | Out of scope |

The exterior choice closes this specific linear system in the halo rest
frame. It does not resolve the parent's undefined mean velocity `u=j/rho`
at general vacuum points, provide a unique nonlinear moving-vacuum action,
or establish the full parent's Galilean/relativistic completion. Likewise,
the fluid's locally isotropic perturbation space is not automatically an
invariant subset of collisionless dynamics; anisotropic stresses and the
kinetic hierarchy can change stability. Neither a stable nor an unstable
reduced-fluid verdict should be silently promoted to a full kinetic verdict.

**Review validation.** Source hashes were checked with `shasum -a 256`.
All sign, factor, boundary and homology checks here are analytic; no numerical
stability computation was run by this reviewer. The document received a
local mathematical proofreading pass for notation, units and the distinction
between an energy coefficient and its second derivative. No external theorem
or historical stability criterion is needed for the stated finite-dimensional
negative-Rayleigh-quotient implication.

## Addendum: dynamically accessible canonical radial deformations

**Additional claim, independently derived:** the fluid Hessian omits a
positive shear cost for a general canonical radial displacement of the
actual stationary waterbag. The exact second-order correction is

```text
Q_kinetic[xi,sigma] = Q_fluid[xi,sigma]
    +(8/9) integral_inside E_rel (xi'-xi/r)^2 d^3x.
```

In the dimensionless normalization of section 3 this is

```text
Q_kinetic = Q_fluid
    +(4/3) integral_0^R n psi (xi'-xi/r)^2 r^2 dr.
```

This is a restricted but genuinely dynamically accessible direction of the
canonical waterbag energy. It is not another assumption of instantaneous
isotropy. It provides a useful next discriminator after a negative fluid
direction: the negativity must survive this compulsory extra cost before
that direction can be called an accessible kinetic energy saddle.

### Exact comparison at finite deformation

Let `q` now denote the material position vector, solely in this addendum;
it is not the density variation `q` in the preceding sections. Write

```text
x = chi_t(q) = q + t xi(|q|) q/|q|,
J = D_q chi_t,                  p = J^(-T) p_0.
```

Take sufficiently small `t` that this is a smooth orientation-preserving
radial diffeomorphism. Its cotangent lift is canonical. Push forward the
original distribution by

```text
f_t(x,p) = f_0(q,J^T p).
```

This preserves phase-space volume, mass, the occupied waterbag level, and
every phase-space integral of a function of `f`. To first order its
canonical generator is `g(q,p_0)=xi(|q|) q.p_0/|q|`. The radial cotangent
lift also preserves each angular momentum vector exactly: the spatial
tangential scale and the inverse tangential momentum scale cancel in
`x cross p = q cross p_0`.

The initially isotropic, zero-current distribution remains even in
momentum and has zero current, although its momentum ellipsoid is generally
anisotropic. Put `K_0=k rho_0^(5/3)`. The transformed density and canonical
relative kinetic density are exactly

```text
rho_t(chi_t(q)) = rho_0(q)/det J,
K_t(chi_t(q)) = [K_0(q)/det J] tr(J^(-1)J^(-T))/3.
```

Consequently its integrated relative energy, with any smooth shared scalar
path `s_t`, is

```text
E_rel,kinetic(t)
  = integral K_0(q) exp[-2s_t(chi_t(q))]
               tr(J^(-1)J^(-T))/3 d^3q.
```

The isotropic fluid closure on exactly the same density and scalar path
instead gives

```text
E_rel,fluid(t)
  = integral K_0(q) exp[-2s_t(chi_t(q))]
               (det J)^(-2/3) d^3q.
```

All gravitational, scalar-potential and scalar-gradient terms agree
between these two configuration paths. Both have zero canonical mean
current and zero scalar momentum, so the parent's common-momentum square
and scalar kinetic energy vanish along the configuration path. Those terms
do not conceal another potential-energy correction.

For a radial map the principal stretches are

```text
a_t=1+t A,        b_t=1+t B_r  (twice),
A=xi',           B_r=xi/r.
```

The exact difference of the two kinetic factors is

```text
D(t) = [a_t^(-2)+2b_t^(-2)]/3 - (a_t b_t^2)^(-2/3).
```

The arithmetic-geometric-mean inequality shows `D(t)>=0` whenever the
stretches are positive. Thus the isotropic closure is the lower kinetic
energy at the fixed density, consistent with the sign of the correction.
The explicit expansions are

```text
[a_t^(-2)+2b_t^(-2)]/3
  = 1 -(2/3)(A+2B_r)t +(A^2+2B_r^2)t^2 + O(t^3),

(a_t b_t^2)^(-2/3)
  = 1 -(2/3)(A+2B_r)t
      +[(A^2+2B_r^2)/3 +2(A+2B_r)^2/9]t^2 + O(t^3),

D(t) = (4/9)(A-B_r)^2 t^2 + O(t^3).
```

Since `Q` denotes the second derivative, rather than the coefficient of
`t^2`, this proves the factor `8/9` in physical units. Substitution of
`E_rel/B=(3/2)n psi` proves the dimensionless factor `4/3`.

The common factor `exp[-2s_t(chi_t(q))]` may vary at first order, but
`D(0)=D'(0)=0`; only its background value enters the Hessian difference.
Therefore there is no added mixed scalar/displacement term. Second-order
choices in either common scalar path also cancel. The scalar minimizer at
fixed `xi` remains exactly the one in section 4.

### Interpretation and useful special case

Pure homology `xi=r` has `xi'-xi/r=0` everywhere. In fact its three
stretches are equal at finite `t`, so the canonical distribution stays
locally isotropic and the two relative energies coincide exactly. Thus the
homology-plus-scalar-amplitude family in section 5 is canonically
accessible without any shear penalty. If its optimized quadratic energy
is negative, it is an actual accessible energy saddle of the specified
stationary canonical waterbag plus scalar configuration, not an artifact
of imposing instantaneous local isotropy on a nonhomologous displacement.

For general trial bases, adding the displayed nonnegative shear matrix and
repeating the scalar-minimized variational screen is a meaningful bounded
test using the existing equations and profiles. A remaining negative
direction demonstrates failure of constrained energy minimization on this
canonical subset. If no negative direction remains in the tested basis,
the fluid result has not transferred to the kinetic model; positive
finite-basis results still do not prove kinetic stability.

**The stronger dynamical inference remains open.** Negative energy on a
dynamically accessible subset is not, by itself, a proof of exponentially
growing modes in a general Hamiltonian kinetic system. The full linearized
kinetic-plus-scalar operator, its constraints and vacuum domain, or an
applicable energy principle with all hypotheses established, is needed to
make that inference. The reduced fluid's positive-inertia eigenproblem
cannot simply be reused with this added shear stiffness and declared to be
the exact Vlasov evolution. In particular, a scalar-minimized negative
kinetic energy direction should be reported as an **accessible energy
saddle**, separately from the reduced-fluid instability verdict.

The addendum is an analytic derivation; no symbolic or numerical run was
needed. The finite-deformation formulas, Taylor coefficients and
homology limit provide independent algebraic checks of its sign and factor.
