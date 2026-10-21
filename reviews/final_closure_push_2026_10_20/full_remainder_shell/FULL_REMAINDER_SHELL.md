# Full canonical remainder: finite circular shells and radial stability

20 October 2026. Analytic continuation at requested base
`f659e6d8e1ee4cf2b756f091aff56b018da1fb1e`; dispatch checkpoint
`5c9edd07b9bc1b9610f8080de8b7700d3ccdb7bb`. Actual source hashes and the
concurrent observed HEAD are in `SOURCE_PINS.json`. This is an extension
of the existing deep-cubic circular-shell theorem, not a duplicate claim
for that theorem or a change to the frozen original theory.

**Result.** In the stated reciprocal spherical effective model, the full
canonical remainder admits finite smooth nonnegative spatial profiles
with both tethered and free mass, the exact canonical ordinary-tracer law
on any prescribed compact annulus, strictly positive circular angular
momenta, and a positive conserved energy for coherent linear radial shell
motion with those angular momenta fixed. Extended fixed baryons contribute
the required positive `G B'/r^2` terms. No deep-field approximation is used.
The constructed phase-space distributions are singular circular measures,
with zero radial dispersion and nonzero tangential kinetic energy. This
does not solve the smooth warm or nonlinear all-time problem.

## 1. Model, domain and counted energy

Let B(r), T(r), F(r) be enclosed baryonic, tethered and free masses, and
write `mu_t=T'`, `mu_f=F'`. B is fixed during variation; T and F are
separately conserved. Assume nonnegative smooth compact spatial densities,
with the cold supports in `[r_0,R]`, `r_0>0`, and `B(r)>=B_*>0` on those
supports. The fixed B is nondecreasing, with bounded B' there, and has
finite total mass. It can arise from a smooth extended baryonic core;
a point baryon may instead be used with its fixed self-energy omitted.
All masses have ordinary inertia. Set

```
u = G T/r^2,  0<=u<=u_*<a0,
R(u) = u^2/(a0-u),
w(u) = -u^2/2-a0*u-a0^2*log(1-u/a0),  w'=R.
```

The symbol R(u) denotes the remainder force; the unadorned outer-support
radius R in bounds/integrals is a constant, distinguished by its argument.
Stiffness is zero. With the fixed baryonic self-energy subtracted, use

```
U = -G/2 int_0^infty [(B+T+F)^2-T^2-B^2]/r^2 dr
    + (1/G) int_0^infty r^2 w(GT/r^2) dr.             (1)
```

This is exactly the coordinator's declared reciprocal two-population
extension: only tethered self-gravity is cancelled. Each gravitational
cross pair remains counted once. Varying (1) gives the outward-positive
accelerations

```
a_t = -G(B+F)/r^2 + R(u),
a_f = -G(B+T+F)/r^2.                                (2)
```

No one-way force deletion, extra population, pinning or reaction is used.
The fixed external baryons are not varied, so no dynamical-baryon stability
or isolated total-momentum conclusion is claimed.

## 2. Actual shell equations from separate Lagrangian maps

At baseline radius r let each species' material shell carry its own fixed
specific angular momentum `ell_i(r)`, with circular balance

```
ell_i^2 = -r^3 a_i > 0.
```

Displace the two populations separately by
`r_i(r,t)=r+epsilon xi_i(r,t)` at fixed shell label r. Small smooth maps
preserve positive radii and ordering within each population; the two
populations may interpenetrate. The exact radial equation for each shell is

```
d^2 r_i/dt^2 = ell_i(r)^2/r_i^3 + a_i[evolving masses](r_i).
```

At fixed Eulerian radius, `delta T=-mu_t xi_t` and
`delta F=-mu_f xi_f`. Evaluated along a tethered shell, its own enclosed
T stays fixed, while the other enclosed F changes by
`mu_f(xi_t-xi_f)`. Thus

```
Delta_t B = B' xi_t,
Delta_t F = mu_f(xi_t-xi_f),
Delta_t u = -2u xi_t/r.                              (3)
```

For a free shell its own F stays fixed, and

```
Delta_f B = B' xi_f,
Delta_f T = mu_t(xi_f-xi_t).                          (4)
```

The centrifugal variation is `-3 ell_i^2 xi_i/r^4 = 3 a_i xi_i/r`.
Combining it with (2)-(4) gives the actual coupled linear equations

```
xi_t_ddot + kappa_t0^2 xi_t
          + G mu_f/r^2 (xi_t-xi_f) = 0,
xi_f_ddot + kappa_f0^2 xi_f
          + G mu_t/r^2 (xi_f-xi_t) = 0,              (5)

kappa_t0^2 = G(B+F)/r^3 + G B'/r^2
             + [2u R'(u)-3R(u)]/r,
kappa_f0^2 = G(B+T+F)/r^3 + G B'/r^2.               (6)
```

Both cross terms are essential. In particular, the free shell does not
move through a frozen tethered source, and the tethered shell does not
move through a frozen free source. An extended B is fixed as a profile,
not fixed as an enclosed number when a shell changes radius; this is why
B' enters both equations.

For the full canonical remainder,

```
R'(u) = u(2a0-u)/(a0-u)^2,
2uR'(u)-3R(u) = u^2(a0+u)/(a0-u)^2 >= 0.             (7)
```

The inequality is strict for u>0 and is zero at u=0. At small u the term
reduces to `u^2/a0+O(u^3/a0^2)`, recovering precisely the existing cubic
coefficient. Its positive full expression, not the small-u expansion,
is used below.

## 3. Independent energy reconstruction and linear theorem

For the field-energy integrand in (1), its mass Hessian is

```
H_tt = G R'(u)/r^2,  H_tf=H_ft=-G/r^2,  H_ff=-G/r^2.
```

For a material shell map, `delta^2 M_i=(mu_i xi_i^2)'`. Add the fixed-
angular-momentum orbital energy `sum_i int ell_i^2/(2r_i^2) dM_i` to U.
Integrating the second enclosed-mass variation by parts and using circular
balance gives

```
W'' = sum_i int mu_i[-a_i'-3a_i/r] xi_i^2 dr
      + sum_ij int H_ij mu_i mu_j xi_i xi_j dr.
```

The surface terms vanish for the smooth compact cold densities. From (2),

```
-a_t'-3a_t/r = kappa_t0^2 + G mu_f/r^2-G R'(u)mu_t/r^2,
-a_f'-3a_f/r = kappa_f0^2 + G(mu_t+mu_f)/r^2.
```

Consequently the tethered own-density term cancels H_tt, and the free
own-density term cancels H_ff. The two reciprocal cross terms combine to

```
W''[xi] = int [mu_t kappa_t0^2 xi_t^2
             +mu_f kappa_f0^2 xi_f^2
             +G mu_t mu_f/r^2 (xi_t-xi_f)^2] dr.     (8)
```

This independently reproduces (5). For a general differentiable remainder,
`2uR'-3R>=0` is sufficient for this positivity when B' is nonnegative.
It is not a necessary condition: the ordinary-gravity terms can compensate
some negative remainder term. For the canonical R, (7) establishes the
sufficient sign throughout its admissible domain.

Let `||xi||_mu^2=sum_i int mu_i xi_i^2 dr`. Under the stated bounded support,
regularity and uniform saturation gap, the operator in (5) is bounded and
self-adjoint in this weighted space. Its coefficients need not be symmetric
in unweighted coordinates; reciprocity is symmetry after weighting by
the inertial masses. Equation (8) gives

```
W''[xi] >= kappa_*^2 ||xi||_mu^2,
kappa_*^2 = G B_*/R^3 > 0.
```

The exact solution of the bounded linear equation (5) conserves

```
E_lin = (1/2)||xi_dot||_mu^2 + (1/2) W''[xi].         (9)
```

Hence both weighted radial displacement and velocity remain uniformly
bounded for all times **in this linear coherent-shell system**. This is
linear Lyapunov stability in the displayed norm. The energy does not
control derivatives of xi, nonlinear shell ordering/crossing, arbitrary
phase-space perturbations, or any full three-dimensional evolution.

## 4. Explicit finite smooth profiles with the exact full law on an annulus

Let the desired ordinary-tracer law be the full simple interpolation

```
s_b(r)=G B(r)/r^2,
u_b(s)=[sqrt(s^2+4a0*s)-s]/2,
g_b,law=s_b+u_b,   s_b=g_b,law^2/(g_b,law+a0).
```

Define its required total cold cumulative mass on the target annulus by

```
C(r)=r^2 u_b(s_b(r))/G.                              (10)
```

For B(r)>0 and B'>=0 this target C is smooth and strictly increasing.
Indeed, implicit differentiation of `R(u_b)=s_b` gives

```
u_b'(s)=(a0-u_b)^2/[u_b(2a0-u_b)],
u_b-s u_b'=a0*u_b/(2a0-u_b)>0,
C'(r)=2r/G [u_b-s_b u_b']+B'(r)u_b'>0.              (11)
```

Here u_b' means its derivative with respect to s; C' and B' are radial
derivatives. For a constant enclosed baryon mass B0, (10) reduces to the
explicit expression

```
C(r)=[sqrt(B0^2+4a0*B0*r^2/G)-B0]/2.
```

Choose `0<r_0<r_1<r_2<R` with B(r_0)>0 and choose any fixed `0<f<1`.
Let the smooth nondecreasing step S be 0 below 0, 1 above 1, and

```
S(x)=exp(-1/x)/[exp(-1/x)+exp(-1/(1-x))], 0<x<1.
```

Define a total cold cumulative mass M by

```
M(r)=0,                                          r<=r_0,
M(r)=C(r) S((r-r_0)/(r_1-r_0)),                   r_0<r<r_1,
M(r)=C(r),                                       r_1<=r<=r_2,
M(r)=C(r_2)+int_{r_2}^r C'(s)[1-S((s-r_2)/(R-r_2))] ds,
                                                 r_2<r<R,
M(r)=M(R),                                       r>=R.
```

Flatness of S at its endpoints gives a smooth profile at every join.
Monotonicity of C and S gives `M'>=0`; the construction gives `M<=C`
everywhere r>=r_0, including outside R. Put

```
T=f M,   F=(1-f)M.                                 (12)
```

Both cold spatial densities are smooth, nonnegative, compact and nonzero.
On `[r_1,r_2]` ordinary tracers feel

```
g_tracer=G(B+T+F)/r^2=s_b+u_b(s_b),                 (13)
```

the exact full law. This is the imposed total-mass target, not a dynamically
selected amplitude. The fraction f and the profile boundaries are state
choices; no abundance or formation selector is inferred.

Let `v=GM/r^2`; this is an acceleration, not a velocity. Since `v<=u_b<a0`,
the actual remainder source obeys `u=fv<=f u_b<f a0`. Thus there is a
global uniform gap `a0-u>a0(1-f)>0`. Since R is strictly increasing,

```
R(fv) <= R(f u_b) < R(u_b)=s_b,

ell_t^2 = r^3 [s_b+(1-f)v-R(fv)] > 0,
ell_f^2 = r^3 [s_b+v] > 0                         (14)
```

at every populated radius. These strict inequalities establish the circular
angular momenta required in (5); positivity of the energy alone would not
establish their existence. The construction satisfies all bounded-operator
hypotheses of section 3 and therefore has its stated coherent radial
linear stability certificate for every 0<f<1. It requires no deep-field
smallness condition. Constants can become large as f approaches one,
so no estimate uniform in that limiting fraction is asserted.

Populate each radius with circular orbits of speed `v_ci=sqrt(-r a_i)`,
with uniformly distributed phases and orbital planes. The positive
stationary mass measure is

```
calF_i(r,v_r,v_perp)=rho_i(r)/(2pi*v_ci(r))
                     *delta(v_r)*delta(v_perp-v_ci(r)).
```

The velocity element is `dv_r v_perp dv_perp dtheta`, so it integrates to
rho_i. Circular trajectories keep their radius and their species' energy
and angular momentum fixed in the constructed stationary fields. This
is stationary as a phase-space measure. It has zero radial dispersion
and tangential dispersions `v_ci^2/2` in the two tangential directions;
it is not a smooth warm distribution.

There is no cold matter at the central singularity if a point baryon is
chosen, and no reflecting wall or outer surface pressure. Both cold
densities taper smoothly to zero. Potential and force match the vacuum
force integrals smoothly. The finite cold support makes all kinetic terms
finite. At infinity the gravitational field integrand is O(r^-2) and,
since `w(u)=u^3/(3a0)+O(u^4)`, the remainder integrand is O(r^-4).
Near zero the cold contributions vanish. Thus the subtracted counted
energy is finite; no divergent infinite halo is used in (8)-(9).

## 5. A stronger second-variation scope, with an additional condition

This paragraph is separate from the all-f coherent theorem. For particles
at the same baseline radius having different small radial displacements,
let their species means and variances be xi_bar_i and Var_i. The same
mass variation gives

```
W''=W''_coherent[xi_bar]
    +sum_i int mu_i kappa_bg,i^2 Var_i dr,
kappa_bg,i^2=-a_i'-3a_i/r=(ell_i^2)'/r^3.
```

For the constant-f profiles (12),

```
kappa_bg,t^2=kappa_t0^2
    + G M'/r^2 [(1-f)-f R'(u)],
kappa_bg,f^2=kappa_f0^2+G M'/r^2>0.                 (15)
```

Because `1+R'(u)=a0^2/(a0-u)^2`, an explicit sufficient condition is

```
u<=a0(1-sqrt(f))  throughout the support.            (16)
```

Then the bracket in (15) is nonnegative, and the splitting contribution
is positive with the same baryon gap. The profile bound u<=f u_b<f a0
makes (16) automatic for
`0<f<=(3-sqrt(5))/2`. For any other fixed f<1, (16) can instead be
enforced by putting the entire cold support sufficiently far outside
finite-total-mass baryons, because u_b(GB(r)/r^2) tends to zero.
This is a positive radial fixed-angular-momentum second variation
including splitting; it is not a general time-dependent Vlasov theorem
for the singular circular measure or a warm-distribution theorem.

There is also an exact fixed-field local-orbit reading of this coefficient.
For one test particle with its angular momentum fixed while the entire
background is held fixed, `kappa_test,i^2=kappa_bg,i^2`. Under (16) its
circular radius is a strict local minimum of
`Phi_i(r)+ell_i^2/(2r^2)`, and the circular angular-momentum map obeys
`(ell_ci^2)'=r^3 kappa_test,i^2>0` on the populated support. In particular,
the full bound `u<=f a0` gives

```
R'(u)<=f(2-f)/(1-f)^2,
(1-f)-f R'(u)>=[1-3f+f^2]/(1-f)^2.
```

This verifies independently the same sufficient fraction threshold above.
The coherent theorem alone would not imply this orbit lemma: it omits
the negative fixed-background tethered term `-G R'(u)mu_t/r^2` that is
cancelled by own-source motion only in the coherent calculation.

## 6. Strict circular binding and a fixed escape-energy gap

Write the actual inward accelerations as `h_i=-a_i`, and normalize the
species potentials by `Phi_i(infinity)=0`. The profile inequality M<=C
holds globally, including the exterior tail, so for `v=GM/r^2<=u_b`

```
R(fv)/R(v)=f^2(a0-v)/(a0-fv)<=f^2,
R(fv)<=f^2 R(v)<=f^2 s_b.
```

At v=0 the same statement holds by continuity. Hence

```
(1-f^2)G B/r^2+G F/r^2 <= h_t <= G(B+F)/r^2,
h_f=G(B+M)/r^2.
```

Since enclosed B, F and M are nondecreasing,

```
-Phi_t(r)=int_r^infty h_t(s) ds
          >=G[(1-f^2)B(r)+F(r)]/r,
-Phi_f(r)>=G[B(r)+M(r)]/r.
```

The actual circular specific orbital energies (per unit inertial mass,
not a summed total-energy budget) therefore satisfy

```
E_ct=Phi_t+(r/2)h_t
     <=-G[(1/2-f^2)B(r)+(1/2)F(r)]/r,
E_cf=Phi_f+(r/2)h_f<=-G[B(r)+M(r)]/(2r).             (17)
```

For `f<1/sqrt(2)` both are strictly below the zero escape energy.
On the finite hollow support the uniform bounds are

```
E_ct<=-beta_t,  beta_t=G(1/2-f^2)B_*/R>0,
E_cf<=-beta_f,  beta_f=G B_*/(2R)>0.                (18)
```

For example f=1/64 satisfies the orbit-monotonicity threshold as well as
the binding threshold; (18) gives `beta_t=(2047/4096)G B_*/R`. These are
exact fractions, not numerical experiments. This supplies a fixed energy
gap in the circular baseline that does not shrink with a hypothetical
later warming parameter. It does not execute that warming continuation,
control the self-consistent potential change, or prove phase-space
stability after warming.

## 7. Exact new scope, audit and continuation

The existing parent proves sections 2-3 for `R=u^2/a0` and its deep-law
finite family. The additional work here is the actual full-R displacement
calculation including extended fixed baryons, positivity of (7), the
full-law cumulative target (10), and a global finite taper satisfying
both angular-momentum positivity and a uniform saturation gap. The
optional condition (16) controls radial splitting for a stated subfamily.
Its fixed-field interpretation supplies stable circular test-particle
radii and a strictly monotone angular-momentum map; (17)-(18) additionally
give a genuine uniform circular escape gap for f<1/sqrt(2).
No scientific numerical work or finite-case theorem claim is used.

This does not make the tethered component a cold rest state: its circular
kinetic support is nonzero, as the reciprocal free attraction requires.
Nor does it provide a smooth finite warm distribution with the same exact
law annulus, unrestricted angular-momentum perturbations, nonspherical
stability, nonlinear all-time control, finite stiffness, relativity,
lensing, cosmological supply, formation selection, a0 or fitted kappa.

The next distinct obligation is to broaden these singular circular
measures to smooth finite phase-space distributions with controlled radial
width while preserving a self-consistent full-R law annulus and proving
stability in that broader class. A formal Jeans pressure alone is not
that construction. Radial second-variation positivity does not establish
the required continuation or prevent nonlinear shell crossing.
