# Audit and interpretation boundaries

Primary verdict: **charge-conserving electrostatic effective action derived;
finite field/energy tests passed; causal microscopic completion and population
separation remain incomplete.** This is self-review by the implementing agent.

## Conservation and the full interaction inventory

For A->A+grad chi, phi->phi-partial_t chi, the variation of
integral(j.A-rho_q phi) is -integral chi(partial_t rho_q+div j) after integration
by parts. Gauge invariance with the charged-matter equations therefore enforces
continuity. The F,T,C vertex has zero total charge; a reaction must alter the
number of positive and negative carriers equally. There is no external charge
reservoir in the candidate physical inventory.

The constitutive relation implies partial_t h=E.partial_t D. Maxwell's equations
then give partial_t(h+B²/2)+div(E cross B)=-j.E for the preferred-frame action.
Matter gains j.E. Including its rest/internal energy and Newtonian gravitational
energy gives the conserved total Hamiltonian under the appropriate closed-system
boundary conditions. Radiation crossing the boundary must be included as flux.
The electrostatic numerical test solves a stationary constraint; the mode test
tests time integration. Neither alone is a full transported matter+gravity test.

At weak field, the TOTAL gauge plus gravitational pair potentials are

    V_TT=0,
    V_TC=-Gm²(1+epsilon)/r,
    V_CC=Gm²(1-epsilon²)/r.

Here T has mass m, C has mass epsilon*m. The new repulsive contribution is not
an extra net weak-field T-T force on top of cancellation with their own gravity.
All cross interactions are mandatory. Neutral baryons still gravitate. The
electrostatic force-sign fixtures deliberately isolate the gauge contribution.

## Numerical evidence

run_action completed with empty stderr. Eight 3D solves use periodic smooth
Gaussian charges; N=17,25,33. Like-charge tests add an explicitly immobile uniform
background to make a periodic solve possible; this is a manufactured force-sign
test, never a candidate countercharge population. Opposite-charge tests have
explicit equal positive and negative sources. The tiny spectral zero mode is
subtracted for solvability. There is no dynamical particle deposition/remeshing.

The solver minimizes sum ell(|grad phi|)-rho_q*phi with Fourier derivatives and
a square-root inverse-Laplacian preconditioner. Gauss residual and equality of
primal and stationary-dual energy are measured independently. Source forces use
the derivative of the normalized smooth source profile and are checked against
finite differences of stationary energy. The actual displacement has nonzero
curl, demonstrating that the old curl-D constraint is not being silently reused.

Field energy and force refinement compare the 25 and 33 grids for the neutral
pair at fixed box/width. This does not establish all-space convergence, grid
convergence near singular cores, or convergence of a dynamic galaxy. Finite
box, smoothing and periodic boundary conditions remain numerical assumptions.

The homogeneous mode retains both carrier inertias. Eighteen integrations cover
three amplitudes, three mass ratios and two tolerances. The force has a change
in higher derivatives at D=0; integration error accumulates over many crossings.
Tightening tolerance reduces maximum relative energy error from 7.65e-7 to 9.68e-9.
No energy projection, damping or rescaling is used. The zero crossings are plasma
oscillations, not proof of irreversible screening or thermalization.

The RAR inverse is verified at 1,037 (x,epsilon) values. The virial identities are
checked by independent dimensional evaluation at 68 profile/mass-ratio points.
The Coulomb applicability screen has 1,717 microscopic points; only 1,135 satisfy
both declared conditions. Invalid points are not interpreted using Coulomb binding.
CONTINUOUS_BOUND.md separately eliminates the microscopic mass and proves an
endpoint bound over the full stated continuous domain; run_bound evaluates it.

## Obligation matrix

| Obligation | Status |
|---|---|
| Explicit charge inventory and vertex | Passed conditionally; gap/coupling not fixed by symmetry |
| Field normalization and Legendre action | Passed algebraically in electrostatic branch |
| Correct 3D constraint, energy derivative, force signs | Finite computational checks passed |
| Both carrier inertias and energy | Analytic identity plus finite mode tests passed |
| Cold stationary coexistence | Refuted where g=e>0; pressure/rotation can evade this restricted claim |
| Virial response as population selector | No discrimination under the specified common thermal proxy |
| RAR preservation with countercharge | Conditional inequality derived, not a disk fit |
| Controlled Coulomb neutral precursor | Binding/virial temperature bounded, not an abundance or rate result |
| Minimal single-invariant L(S) relativistic completion | Fails subluminal characteristic-speed requirement on electric backgrounds |
| General microscopic completions | Not excluded; require additional physics |
| Live disk/dwarf/cluster assembly | Not executed; formation channel and causal completion are not established |

## Important restrictions on negative conclusions

The characteristic-speed argument applies to the derivative-free classical L(S)
ansatz on a constant electric background. It does not by itself prove that every
dispersive UV theory or preferred-frame medium is acausal. Positive electrostatic
energy is likewise not a guarantee of a causal completion.

The Coulomb bound compares energies only. B/T<<1 does not prove immediate
ionization of an initially frozen population; rates and radiation may be too
small. It rules out a virial binding-temperature threshold supplied by this
controlled channel in the stated mass-ratio domain. Strong core interactions,
epsilon outside [1e-4,1], cosmological initial states and evolving distributions
are outside that conclusion and must not be assigned by galaxy label.

No prior solver or manuscript has been modified. No new collision rate was
spliced into old dynamics, and no observational success, independent review,
publication or commit is claimed.
