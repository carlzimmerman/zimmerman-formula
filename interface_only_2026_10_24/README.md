# Interface-only interactions: the force problem can be avoided; stable confinement remains open

The original joint target is not achieved. Removing the bulk binding term
does allow an essentially pure interior to retain the parent force law while
the exterior remains free. The tested candidate fronts have not demonstrated
stationary, stable confinement: softening loses T, alignment can drift inward,
and curvature-pressure results require the separate status below.

All interactions vanish in occupied pure phases. All their phase and cold-mass
derivatives are retained. DERIVATION.md also gives the reciprocal baryon
momentum/stress variations; those are not evolved here. This remains a
fixed-density, fixed-baryon spherical test, not formation or a real-data fit.
The granted law-shaped density is tested for actual force balance, never
counted as evidence that the interaction generated the law.

Starting SHA a442dd0e256cacb80316c0a717ab4b1232752546. Inputs are snapshots.
The prior bulk binding interaction and global assembly scans were not rerun.

## Tested routes

**IO-1: positive interface softening.** Eliminating a stable auxiliary strain
gives kappa=1/(1+lambda Lrho²|grad C|²) multiplying the interface stiffness.
All36 minima lose the interior; the largest inner converted fraction is
5.82e-7. This is finite evidence for the declared starts and parameters.

**IO-2/3: positive gradient alignment.** Replace the gradient energy by
.5 ell²F(u)|grad x-eta h'(x)grad C|², with no bulk gap. This retains positive
stiffness and favors a boundary near changes in local kinematics.36 coarse
minima and9 refined/stronger-coupling cases show partial retention and some
apparent fraction/force passes. The promising n256 eta30 fronts have negative
phase Hessian modes; several other optimizations stop without stationarity.
An optimizer success flag alone is not a stability result.

**IO-4: test those modes directly.** For large-disk Rj5b and8b, independent
energy second differences confirm negative mode curvatures -.3750 and-.6319.
Both signs of the .01-amplitude perturbations lower energy. At time3000 the
5b case has qinner .94682 and a large force imbalance. The8b case still has
qinner1 and qouter near zero, with a .00533 maximum relative force error—the
same as the uniform pure-T grid control. It is still drifting.

**IO-5: long and finer continuation.** Continuing the8b state for another
100000 internal units leaves the boundary at16.8295kpc with speed2.14e-5
and a negative lowest Hessian eigenvalue. Continuing the interpolated state
at n512 for another100000 units moves the boundary to15.1322kpc. Its speed
is5.12e-5; it is not stationary. Though its mean inner q is .99954 and the
exterior is essentially free, its maximum inner T-force imbalance is7.07
times gravity as the interface enters the tested1.5–15kpc interior. This is
a finer continuation at a later elapsed time, NOT a same-time grid
convergence comparison. No physical lifetime follows from internal time.

**IO-6: interface curvature pressure.** A new positive quartic-curvature
energy gives E4 proportional to1/R² for a unit spherical interface, hence
an outward force proportional to1/R³. All radial phase and species forces
are derived, including variation of the jump amplitude. Twelve minima test
ell4=3,6,10kpc on both templates. The small-template optimizations hit their
iteration cap and remain nonstationary; they are not converged physical
exclusions. Large-template all-T starts keep more than99.8% of the outer
reservoir converted, which fails the requested separation. Local starts at
ell4=3,6 lose the interior. The ell4=10 local start meets fraction gates but
has large force residual, negative Hessian and an unfinished optimization.
IO-7 continues that exact state dynamically for10000 internal units. It loses
the interface: both inner and outer T fractions fall to9.69e-7, with phase
speed2.87e-11 and energy-plus-heat error2.06e-7. The system reduces the phase
contrast rather than maintaining the unit jump assumed in the simple1/R²
surface-energy argument. This particular optimizer ambiguity is resolved;
the uncontinued small-template cases remain numerically unresolved.

## Interpretation and checks

This is a narrower result than the last turn: the unwanted bulk force is not
unavoidable for an interface-only coupling. In spherical symmetry, an exterior
interface changes the interior mass-response potential by a constant, which
has no radial force. The unresolved part is stable confinement of that
interface when the entire phase profile can relax.

The phase energy, full Hessian and independently added T-mass derivatives
pass finite-difference checks: errors below2.6e-9 for compliance/alignment
and7.6e-9 for the curvature test. Energy-plus-heat errors for the alignment
continuations are below6.7e-7. Boundary energy, total-T tail dependence and
all retained free gravitational mass are included. Low-T cells can have
ill-conditioned raw T-potential diagnostics; these are not interpreted as
physical accelerations where the T phase is absent.

Each run directory records contracts, exact commands, input/output hashes,
results and status. VALIDATION.json records manifest checks. Numerical
minima, stationarity, phase Hessians, actual force balance and outer fractions
are separate gates. None is substituted for another. Self-review only;
no manuscript or original experiment was changed.

The new coefficients and couplings remain postulates. Live mass and baryon
backreaction, finite-noise lifetime,3D geometry and microscopic matching are
open. No universal no-go or exhaustion of interface-local physics is claimed.
