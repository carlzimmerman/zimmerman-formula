# Generalized-action Milky Way calculation

The original `full_001` and `refine_001` observational grades are withdrawn.
They used a pointwise-consistent Hessian whose angular adjoint did not preserve
spherical symmetry. Their apparent 3 kpc pass counts (22 canonical, 51 alt) are
not evidence for the continuum law. The raw files remain unchanged. The
compatible implementation is `generalized_v3.py`; completed fresh physical
results are recorded separately in `full_002` and `refine_002`. At the six
sampled lengths, only 3 kpc has four-cut Milky Way passes: 22 canonical and 50
alt cells on the scan grid. The strongest selected witness on each footing
survives refinement through level 5 and the tested domain changes. Neither
witness passes the separate strict scale-height cut. This is a conditional
Milky Way result, not overall viability of the response law.

This is a new bounded response-law experiment. The baryon population, sources,
observational data, acceleration footings and cuts remain unchanged. The
Newtonian source is unsmoothed; there is no Gaussian filter. One universal
physical length ell enters the local Newtonian-gradient/Hessian invariants.

The continuum law and its normalized primitive are owned by `../analytic/`:

    x=|grad psi|^2, z=x+ell^2 (H:H), psi=N rho,
    P=xR(z), R(z)=Q(z)/z, Q(0)=0, Q'(z)=nu_simple(sqrt(z)).

Coordinates are kpc and the potential unit is a0*kpc; gradients are in a0 and
Hessian components in a0/kpc. Each ell is an actual fixed length in kpc,
independent of source mass. The field code obtains stable coefficients
`D=z R'` and `R-1` from the analytic implementation and defines

    A=[R-1+(x/z)D] grad psi,
    B=ell^2 (x/z)D H.

The simultaneous zero-field/Hessian limit has A=B=0, without a physical floor
on z. The continuum phantom source is `div A - double_div B`. All B terms
are retained; removing them would describe a different, nonvariational map.

## Discrete energy and covariance

The inherited Poisson matrix L is self-adjoint in the volume weight W. With
cell gradient G and covariant Hessian H, the finite energy is

    E_ph=-(8pi)^(-1) sum W*x*(R-1).

Its exact discrete source and phantom potential are

    b_ph=-W^-1 [G^T W A + H^T W B],
    phi_ph=L^-1 b_ph.

The Hessian is represented by rr, rtheta, thetatheta and phiphi components,
with multiplicities 1,2,1,1 in both its squared norm and transpose contraction.
The implemented covariant operators are

    Hrr=Dr Dr,
    Hrtheta=[Dtheta_even Dr - (1/r)Dtheta_even + Dr Dtheta_even]/2,
    Hthetatheta=Ltheta-(cot(theta)/r)Dtheta_even+(1/r)Dr,
    Hphiphi=(1/r)Dr+(cot(theta)/r)Dtheta_even.

Here `Ltheta=-W^-1 Dt_face^T Wface Dt_face`, and `Wface` is angular face
area times center-to-center distance. This is the narrow finite-volume angular
Laplacian, evaluated in factored form. Its weighted stiffness is symmetric and
annihilates a radial scalar. The radial stress cancellation that failed in the
first implementation is therefore preserved algebraically. The full
tangential transpose combines `Bphiphi-Bthetatheta` before multiplying by the
cotangent connection, avoiding cancellation between large isolated terms.
All transpose terms remain present.

The first implementation used odd mirror parity for the polar vector
derivative. That gave pointwise consistency but was insufficient: its weighted
adjoint and cotangent connection were incompatible. `covariance_red_001`
records the failed radial cancellation and order-one spurious polar field.
`generalized_v2.py` fixes the algebraic compatibility, but its assembled
second derivative amplifies roundoff enough to fail the unchanged numerical
polar-artifact tolerance in `covariance_green_001`. The factored v3 form passes
that same regression in `covariance_green_002` without relaxing its limits.

The first cell center is away from the pole. Radial differentiation uses the
inherited physical one-sided difference at either radial edge and centered
interior differences. Quadratic, linear and smooth-source component checks
cover the angular boundary rows and interior; inner-cutoff and outer-domain
changes test the physical witnesses.

## Invariant and covariance evidence

The first bounded record `invariants_001` passes its declared finite checks but
shows cancellation in source-based energy finite differences as their step
shrinks. It remains preserved. `invariants_002` holds the linear Newtonian
potential perturbation fixed and differences the local energy densities before
summing. This tests the same derivative while avoiding repeated noisy solves.

- Newtonian Q=z gives exactly zero phantom response.
- ell=0 reproduces the unchanged KT33 plain-energy map to 2.46e-16 relative.
- Improved energy derivative errors decrease from about 8.7e-6 to 9.3e-8 to
  6.6e-9 at steps .01, .001, .0001 on both tested lengths.
- Finite-difference reciprocity agrees to about 3e-9 at its best recorded step.
- On the initial coarse angular grid, radial quadratic Hessians have .294%
  maximum error; axial quadratic errors are 2.30% in the interior and 5.68%
  at the polar boundary rows. These are finite stencil errors, not exactness.
- A smooth Plummer radial benchmark gives ell=1 phantom-force relative errors
  .007521, .001885 and .000472 at 30,60,120 radial points per decade. The
  comparison is against the independently reduced continuum radial expression
  `g_ph=A_r-B_rr'-2(B_rr-B_tangent)/r`, not a copy of the discrete transpose.

Those first controls did not suffice: they missed the two-dimensional spherical
covariance defect. The accepted v3 controls are `invariants_004` and
`covariance_green_002`. They recover the Newtonian and zero-length identities,
give energy-gradient errors down to 6.99e-9 and reciprocity agreement down to
3.59e-9, and add the following essential checks:

- Weighted angular symmetry relative residual at most 1.23e-16 and radial
  angular-source cancellation at most 3.02e-16 across refinements 1–4.
- Spurious polar force for smooth spherical Plummer potentials at ell=0,1,10
  kpc is at most 2.84e-8 relative to the radial phantom force scale.
- At refinement 4, Plummer Hessian relative error is 2.882e-4. The two-dimensional
  radial phantom-force errors are 4.714e-4 at ell=1 and 1.163e-3 at ell=10 kpc;
  the errors decrease with refinement.
- Axial quadratic interior/boundary maximum component errors decrease from
  .02297/.05683 at refinement 1 to .005182/.01198 at refinement 4.

These checks validate the tested finite identities and demonstrate convergence
on the recorded smooth sources. They do not provide a continuum error
certificate, establish accuracy for every thin disk, or establish dynamical
health of the action.

## Physical search contract

The initial pilot selected nine original cells per footing at ell=0,.03,.1,.3,1
kpc; its observational grades share the withdrawn v1 implementation. The fresh
full population run
uses all 1,375 original cells on each footing at the requested .03,.1,.3,1 kpc
and the explicitly widened 3,10 kpc diagnostics. These are six discrete lengths,
not an exhaustive continuum-length scan. Strict Lh is reported separately.

The physical-force test reuses the unchanged original density basis and Poisson
matrix, with all generalized terms computed from its Newtonian potential.
Selected follow-up cases use literal source densities. The best-D cell at each
length and footing is frozen for checks at refinements 2,3,4,5, half the inner
radius, and twice the outer radius. The two-dimensional smooth-Plummer and
axial-quadratic controls accompany those grid changes. Selected refinement
does not certify all population pass counts.

The corrected full scan and literal-source refinement both completed with
valid hash manifests. The scan took 165.5 seconds and the selected refinement
15.4 seconds. The full scan contains 16,500 rows: 1,375 cells, two footings and
six lengths. Passing counts are:

| ell (kpc) | canonical four-cut | alt four-cut | four-cut plus strict Lh, either footing |
| --- | ---: | ---: | ---: |
| .03 | 0 | 0 | 0 |
| .1 | 0 | 0 | 0 |
| .3 | 0 | 0 | 0 |
| 1 | 0 | 0 | 0 |
| 3 | 22 | 50 | 0 |
| 10 | 0 | 0 | 0 |

Selected 3 kpc witnesses, using literal densities at refinement 5:

| footing / original index | vc | K0 | cK | cO | h | D |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| canonical / 1317 | 225.986967 | 69.778957 | 51.348989 | 36.792973 | 3.374214 | .767945 |
| alt / 1206 | 227.606033 | 69.865822 | 53.676146 | 22.216364 | 3.399702 | .795681 |

The units and score definitions are the unchanged original ones. Both rows
pass L1, L2a, L2b and L3 in all six tested configurations: refinement 2,3,4,5;
refinement 3 with half the inner cutoff; and refinement 3 with twice the outer
radius. Both fail strict Lh in every configuration. The refinement 4-to-5
changes are below .001 km/s in vc, .0031 in K0 and .00061 in D. These observed
differences are not certified continuum error bounds. The selected best-D
controls at the other five lengths continue to fail the four-cut conjunction.
The population counts are still scan-grid counts; only selected cells received
the higher-resolution and domain checks.

## Boundary and manufactured-test qualifications

`refine_002` records every Hessian component near the pole, near the equator,
in the radial/angular interior, on radial boundary rows, and at radius lines
near 1 and 8.2 kpc. At refinement 5 the smooth Plummer Hessian error is
1.848e-4; radial phantom-force errors are 3.022e-4 (ell=1) and 7.461e-4
(ell=10), with spurious polar force at most 1.480e-8 on that grid. Radial,
axial and cylindrical quadratic interior errors decrease with refinement.

Two limitations are explicit in the raw diagnostics. First, `psi=z` is not an
admissible scalar on the equator-even half-domain used for the Milky Way. Its
recorded linear-axial Hessian develops an equatorial boundary contribution
that grows with refinement. This is not an operator-convergence control, and
the `all_checks_pass` flag in `refine_002` does not assert otherwise: its
assertions test the admissible spherical polar-artifact control and
literal-source replay. The separate `fullsphere_001` control places this
manufactured scalar on its correct full domain and passes its convergence
assertions near both poles, the equator and the interior.

Second, composing the inherited one-sided radial derivative twice does not
give a pointwise convergent quadratic Hessian at the very first and last
radial rows: the maximum Hrr error is about .508 at refinement 5, while the
radial interior error is 1.179e-4. No claim of uniform boundary Hessian accuracy
is made. The half-inner-cutoff and double-outer-domain tests show small effects
on the selected physical observables, but do not prove a global convergence
theorem. These qualifications are retained rather than hidden by an aggregate
pass flag.

Earlier lanes and completed evidence remain read-only. Each new run has a
prewritten contract and v2 hash manifest; failed regressions are preserved as
failed evidence. The Milky Way tests alone say nothing about dwarf grading,
Cassini, other galaxies, or dynamical health of this generalized action.
