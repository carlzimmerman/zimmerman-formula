# W4-08: healthy MOND response and the amplitude ratio

2026-10-20. Base checkpoint supplied to read-only routes:
`281c007ac7513aea434ec4366e71b371cc359a6b`. Commit this file alone before
creating any checker. No scripts or parameter scans have been run here.

Target: a healthy specified microscopic action/state with an operational
MOND force, force-calibrated Newton G, vacuum-like positive energy epsilon,
and a physical principle fixing xi=1/4. In the single-mediator class of
W4-04, the equivalent amplitude target is R=epsilon C3^2/C2^3=128pi/9.
For tensor-plus-mediator theories the force dictionary must be derived
again; it is not legitimate to import that scalar-only formula by naming.
The target is only a comparator, not an input to microscopic couplings.

Standing status remains kappa=1/2 FITTED. CFG493: kappa_Lambda=0.417+/-0.095
and kappa_crit=0.345+/-0.078; separate footings. No measured quantity is
used to select a coefficient. Sources/authorities: W4-04 PROOF.md/HANDOFF.md;
CFG894 KAPPA_CAMPAIGN_RULES.md, KAPPA_DOORS.md and register. No reserved
p63/four-form/Lean work, downloads or heavy computation.

## Routes and changed mechanisms

R1 CRITICAL FERMION BANDS: strengthen earlier K224/K228/CFG900 cubic-only
or vacuum-offset results by computing an entire regulated constitutive
energy, its Newtonian UV, positive cubic IR, full static Hessian, and the
frequency/wavelength-dependent fermion response. A critical quadratic
cancellation is an independently specified criticality requirement, not
a free fit to the target. The sheet density/orientations and physical
source dictionary must be explicit. No local principal-symbol claim may
silently replace the actual gapless determinant.

R1b SPLIT BOSON/FERMION BANDS: pair equal boson/fermion band degeneracies,
fermion gap squared z=y^2 h^2 and boson gap squared z+Delta^2. With common
positive physical band edge L, the homogeneous determinant is

 D(z)=A[(L^2+Delta^2+z)^(3/2)-(Delta^2+z)^(3/2)
        -(L^2+z)^(3/2)+z^(3/2)].

Grant a cancellation prescription with zero parent energy at Delta=0.
Use the one critical quadratic B=-D'(0), E(h)=D(y^2h^2)+B y^2h^2.
Determine the same-state energy, pressure, C2,C3, Hessian and R as functions
of d=Delta/L. Test if pairing, self-duality d<->1/d, criticality or a real
symmetry fixes d. Positive energy alone is not dark-energy stress.

R2 DOCUMENTED STABLE SUPERFLUID: proceed beyond the familiar unstable
one-field MOND branch to an actual two-field parent and radial modes.
Derive the quadratic Hamiltonian, health inequalities, source response,
tensor-plus-phonon a0 and state stress. Track the independent microscopic
couplings and conserved-charge state. Label a nonrenormalizable parent EFT
as such; it is not a proven UV completion merely because it adds fields.

R3 CONSTRAINED/AUXILIARY RESPONSE: test whether a genuine second-class or
Gauss-law constraint evades stable-auxiliary concavity without adding a
propagating ghost. Derive the reduced Hamiltonian and full constraints.
Test adding an arbitrarily small positive kinetic regulator; if a fast
instability returns, the completion is singular and not a healthy
unconstrained microscopic parent. Ask whether generating the vacuum from
the same auxiliary sector preserves the MOND cubic or instead moves its
zero-stiffness background.

## Determinacy, dimensions, state and audit

All routes start with continuous (`free`) spaces of microscopic couplings,
gap ratios, densities, time-kinetic coefficients or state charges. No hit
probability is assigned and no exact candidate exists until these are
fixed independently. Keep all knobs symbolic, including regulator shape.
R1b's coefficients may cancel common A and y factors; a surviving d is a
physical trade, not a field normalization. The pi and hbar powers must be
tracked. General dimensions change determinant powers; do not pretend a
two-dimensional sheet determinant is a four-dimensional Lorentz vacuum.

Success requires healthy physical source response with the MOND asymptote,
same-state Newton/vacuum normalization and a unique target ratio, plus a
second independent prediction. Static convexity, positive homogeneous
energy, a fixed charge ensemble, or the right cubic exponent alone is
partial evidence. Full vacuum stress, dynamical health and the derivative
range are separate required checks. No theorem about all microscopic
models is claimed if these specified models fail.

## Exact checks and controls to implement after this freeze

For R1 and R1b: low/high-gradient coefficients, radial/tangential Hessians,
the single-mediator operational dictionary, positive split-band energy,
and the exact R(d) expression and reciprocal symmetry. Confirm a
nontrivial physical gap mutation changes R, while common prefactors and
field redefinitions cancel. No numerical search for a root of R=128pi/9.
If solving the matching condition algebraically, label it an imposed
constraint rather than a prediction.

R1 dynamics: compare the nonlocal bubble at h=0 and at finite gap with a
local kinetic approximation. State the long-wavelength/adiabatic condition
and its failure as the gap closes. Source profiles must satisfy that
condition before an all-radius algebraic law can be asserted.

R2: source flux and stable quadratic Hamiltonian signs, parent-amplitude
saddle and the operational a0. A source coupling mutation must change a0;
an independent condensate-density mutation may repair health without
selecting its amplitude.

R3: auxiliary stationarity, reduced Hessian, constraint matrix and small
kinetic-regulator instability. A same-sector FI/source perturbation should
move the zero-stiffness background or remove its admissible branch.

Normal and separate MUTATE outputs; a baseline violated by a declared
physical control must exit nonzero. All actual identities, source versions,
and any post-freeze extension are recorded before checker execution.
Use one process/one library thread and bounded exact calculations. Preserve
raw proofs, source checks, input hashes, independent review and continuations;
append only this lane's campaign rows after reconciliation.
