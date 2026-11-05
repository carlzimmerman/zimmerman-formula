# Force on stars: canonical vortices versus a gravitating concentration

Contract:d1c09a0d3b. The requested force calculation has a definite result
for the illustrative action: the static vortex adds a repulsive leading
gravitational force. Adding a finite-density phase current still gives a
repulsive gravitoelectric perturbation relative to its ambient condensate.
A separate positive-density halo can produce a flat curve, but its required
normalization does not follow from either vortex calculation. No coefficient
1/2 is obtained or inserted. These conclusions concern the specified models,
not every possible interpretation of the user's flowing-medium analogy.

## 1. The quantity that actually accelerates a star

Use the action in FLOW_POSTULATE_TRANSLATION.md, with minimal baryonic
coupling, and c=hbar=1. In a weak stationary gravitational field, define
g_00=-(1+2Phi). To leading order, a slowly moving test star obeys

    acceleration=-grad Phi,
    laplacian Phi=4pi G(rho_E+p_r+p_phi+p_z).

This follows from R_00=laplacian Phi and the trace-reversed Einstein
equation R_00=8pi G(T_00-g_00 T/2). Energy density alone is not the source
when stresses are comparable to it. Subtract the homogeneous vacuum
background and work well within its curvature radius. At this order the
flat-space scalar profile sources the first gravitational correction;
metric corrections to the profile enter at higher order in G.

For the straight static vortex theta=n phi, set

    K_r=(f')^2/2, K_phi=n^2 f^2/(2r^2),
    U=lambda(f^2-v0^2)^2/4 >=0.

Its stress components, excluding the common V0 background, are

| Component | Value |
|---|---|
| rho_E | K_r+K_phi+U |
| p_r | K_r-K_phi-U |
| p_phi | -K_r+K_phi-U |
| p_z | -K_r-K_phi-U |

Their active gravitational combination is exactly

    rho_E+p_r+p_phi+p_z=-2U <=0.

The long-range positive gradient energy cancels against its stresses in
this source. Treating that gradient energy as pressureless dark matter
would give the wrong force.

## 2. Solved core and the sign of the circular-orbit contribution

Regularity at the axis and cylindrical symmetry give

    r Phi_eddy'(r)=-8pi G integral_0^r ds s U(s),
    a_r,eddy=-Phi_eddy'=+(8pi G/r) integral_0^r ds s U(s).

Positive radial acceleration is outward. This sign holds throughout the
straight-vortex weak-field solution, not just far outside the core.

The scalar profile equation supplies the normalization without fitting:

    f''+f'/r-n^2 f/r^2-lambda f(f^2-v0^2)=0,
    d/dr[r^2(f')^2/2-n^2 f^2/2-r^2 U]=-2rU.

For the regular fundamental branch f(0)=0, f(infinity)=v0, the bracket
approaches -n^2 v0^2/2. Consequently

    integral_0^infinity dr r U=n^2 v0^2/4,
    a_r,eddy -> +2pi G n^2 v0^2/r.

The numerical solution below verifies this identity and its asymptotic
coefficient for n=1. A central baryonic mass has inward acceleration
G M_b/r^2. In the equatorial plane, outside that mass and the vortex core,
the leading circular-orbit relation therefore becomes

    v_c^2=G M_b/r-2pi G n^2 v0^2.

The constant has the wrong sign to explain a positive flat rotation curve.
Where the expression becomes negative, no circular orbit exists under this
approximation. This is not an actual rotation-curve fit or a claim that a
galaxy contains an infinite string. The straight vortex has logarithmically
divergent energy per length and needs an outer completion. The local result
requires core_radius << r << outer_scale and weak accumulated metric
perturbations. Cosmological vacuum curvature supplies an additional outward
background contribution locally; it does not reverse the vortex result.

## 3. A phase-current vortex, rather than a static defect

To test a configuration with a current, take theta=-omega t+n phi and
constant omega>0 in a stationary patch. The homogeneous background at the
same chemical-potential parameter has

    f_infinity^2=v0^2+omega^2/lambda.

The radial equation is the preceding one with v0 replaced by f_infinity.
For the nonnegative, node-free branch, f<=f_infinity: an interior maximum
above f_infinity would require both f''<=0 and, by the equation,
f''=n^2 f/r^2+lambda f(f^2-f_infinity^2)>0, a contradiction.

With d(r)=f_infinity^2-f(r)^2>=0, the active gravitational source relative
to this uniform finite-charge background is

    delta(rho_E+sum p_i)
      =2omega^2(f^2-f_infinity^2)-2[U(f)-U(f_infinity)]
      =-omega^2 d-lambda d^2/2 <=0.

Thus its leading gravitoelectric perturbation is again repulsive. The
surrounding material may gravitate; the vortex is a deficit relative to it.
The vortex equation and this source do not establish that the uniform
finite-charge background is dark energy or a viable cosmological solution.

There is also an off-diagonal momentum density and a frame-dragging field.
The above result is the leading force on a slowly moving test body, not a
complete stationary metric or an all-velocity orbit calculation. The
velocity-dependent gravitomagnetic force has not been evaluated. It cannot
be identified with the medium's phase circulation or silently substituted
for the required universal inward acceleration. A finite rotating halo and
its boundary/current distribution would be needed for that calculation.

## 4. What a genuine concentration would have to do

For comparison, use ordinary Newtonian gravity for a spherical, low-pressure
overdensity with mass density rho_h=A/r^2 in a finite radial interval.
This is a required-density benchmark, not a profile derived from the vortex.
MATERIAL_POOL_DERIVATION.md separately derives this asymptotic profile from
isothermal hydrostatic balance, with A=c_s^2/(2pi G) and v_flat^2=2c_s^2.
That is an alternative fluid hypothesis; its dispersion c_s and cosmological
linkage remain undetermined.
Between its core and outer cutoff,

    M_h(<r)=4pi A r + constant,
    g_h=4pi G A/r+O(r^(-2)),
    v_flat^2=4pi G A.

So an actual concentration can give a positive flat rotation curve. The
remaining task is to derive A and its dependence on baryonic mass. Restoring
SI units for this mass-density benchmark, the inferred acceleration scale is

    a0_eff=v_flat^4/(G M_b)=16pi^2 G A^2/M_b,
    kappa_eff=a0_eff/[c sqrt(G rho_DE)]
             =16pi^2 G A^2/[M_b c sqrt(G rho_DE)].

The desired coefficient requires, as an OUTPUT of dynamics,

    A^2=M_b c sqrt(G rho_DE)/(32pi^2 G).

That is not used as a boundary condition or supplied to the code. Assigning
that value to A would merely put the answer in by hand. Neither vortex
solution determines this positive overdensity or its baryonic-mass scaling.
A hydrostatic, time-dependent or interacting fluid model must produce it
from the same action/state that determines the cosmological stress.

## 5. Numerical evidence and limits

The frozen n=1 profile equation was solved on dimensionless radii20,40,80
with independent400/800-node starting meshes and tolerances1e-8/1e-9.
All six solves converged. Profile differences passed the1e-5 absolute
criterion. The largest finite-domain virial relative residual was4.41e-10.
The fine-grid integrals, including the analytic tiny-core and leading outer
tail corrections, were

| Outer radius | Corrected integral; analytic limit is1 |
|---|---|
|20|0.9999925541922734|
|40|0.9999995755318278|
|80|0.9999999745651229|

These numbers verify the outward-force normalization. They are not empirical
galaxy parameters. Thirty-one exact/numerical checks pass in evidence/eddy_force.
The density-only mutation fails the two intended stress checks; its profile
calculation is unchanged. Both v2 manifests validate. Float64 collocation
and adaptive quadrature are convergence-tested, not interval-certified.
Sampled profile positivity is not a full dynamical stability theorem.

Self-review checked the trace-reversed source, background subtraction,
radial integration sign, virial boundary term, finite-charge subtraction,
mass-density units and distinction between fluid motion and stellar force.
No independent review is claimed. The derivation is internal rather than
borrowed from a different modified-gravity model. The abstract of
[Aryal and Everett, Gravitational effects of global strings](https://doi.org/10.1103/PhysRevD.33.333)
was checked only for historical scope: it studies weak-field global-string
gravity. Its full force derivation was not inspected and is not cited as
verification of the numerical coefficient here.

## Outcome

This explicitly tested canonical eddy does not supply the needed attractive
galactic acceleration. A positive-density pool has the right asymptotic force
shape in the separate isothermal model, but its amplitude and baryonic-mass/vacuum linkage remain
undetermined. There is no new derivation of1/2, and no numerical choice was
made to obtain it. A useful next model must create an overdensity or derive
an additional attractive baryonic interaction, while fixing the normalization;
simply making the vortex spin does not meet those obligations.
