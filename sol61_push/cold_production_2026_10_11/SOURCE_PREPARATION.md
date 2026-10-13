# Preparing the charged source from an uncharged displacement

Status: exact homogeneous classical construction with externally prescribed
mass switches; finite numerical audit passed. This supplies a possible
preparation step for the charged action, but does not establish an autonomous
cosmological origin, vacuum production, or the repo's full cold medium.

## What needs preparation

The late action in CHARGED_ACTION.md conserves its U(1) charge. A closed system
initially at Q=0 cannot evolve under that symmetry into the positive net charge
used in E >= m Q. The previous source was circular motion with charge 2,
chi=A exp(-i M t). Its amplitude and charge were inputs. Creating pairs with
opposite charges does not supply that net charge.

A temporary symmetry-breaking interaction can change the charge and then
switch off before the charge-protected conversion stage. Affleck-Dine
condensate evolution is an established related idea. The abstract of
[Dine, Randall and Thomas, hep-ph/9507453](https://arxiv.org/abs/hep-ph/9507453)
describes coherent scalar-condensate baryogenesis, Hubble-induced potentials,
and model-dependent abundance. This citation motivates investigating temporary
charge breaking; none of its supersymmetric dynamics or abundance results
is imported into the construction below. Only the abstract was checked for
this comparison; the pulse below is derived independently.

## An explicit positive-potential pulse

Write chi=(X+iY)/sqrt(2), with canonical real kinetic terms. Initially set
X=Y=L and both velocities zero. The ordinary source potential is
V0=M^2(X^2+Y^2)/2, so E0=M^2 L^2 and Q0=0.
For 0<t<T, change only the Y frequency:

    Vpulse = M^2 X^2/2 + (2M)^2 Y^2/2,
    T = pi/(2M).

The additional term is 3 M^2 Y^2/2. It explicitly breaks the late U(1),
and is nonnegative. The exact trajectory during the pulse is

    X=L cos(Mt),           Y=L cos(2Mt),
    Xdot=-ML sin(Mt),      Ydot=-2ML sin(2Mt).

Immediately before switching back to V0:

    X=0, Y=-L, Xdot=-ML, Ydot=0.

Afterwards chi=-i L/sqrt(2) exp[-i M(t-T)]. Thus the source is exactly
circular, with the phase and amplitude required by the later conversion
calculation up to an arbitrary common U(1) rotation and amplitude choice.
The physical positive-charge convention is

    Q = 2 i (chi* chidot - chidot* chi)
      = 2 (Y Xdot - X Ydot).

The pulse obeys Qdot=6 M^2 X Y, and finishes at Q=2 M L^2.
The first switch supplies 3 M^2 L^2/2 of energy; the second removes exactly
that amount. The final energy is E0, not energy created from nothing.
The pulse converts an existing potential-energy displacement into rotation.
A controller implementing the switches would have to exchange the stated
energy and break the charge symmetry; it has not been modeled here.

With daughters exactly zero the homogeneous source subspace is an exact
classical solution of the full late action. This does not replace the separate
quantum daughter seeding calculation or bound quantum production during
preparation. The pulse calculation neglects expansion; for the inherited
H/M about 6.9e-12 it lasts only H T about 1.1e-11 in Hubble units. That small
ratio supports a short-pulse approximation, not an autonomous cosmology.

## Coldness and sensitivity

For an arbitrary homogeneous free source after the pulse define

    r = M Q/(2 E),       |r| <= 1,
    eta = (E-mQ)/E = 1 - (2m/M) r.

The chosen M=2m sqrt(1+u^2), u=0.001, gives ideal
eta=4.99999625e-7. Imperfect rotation adds a charge deficit to this budget.
For initial X=sqrt(2)L cos(theta), Y=sqrt(2)L sin(theta), at rest, the ideal
pulse gives r=sin(2 theta). Thus arbitrary initial phase is not sufficient:
the phase relative to the anisotropy must be selected. With a uniform random
phase the positive-charge high-efficiency subset is small; this construction
does not supply a phase-selection mechanism.

Exact endpoint formulas give the following one-parameter tolerances. All
other parameters are held at their ideal values; the limits are not a joint
error budget or a naturalness prediction.

| Initial eta ceiling | Phase offset from pi/4 | Positive duration error M delta T | Positive error in omegaY/M from 2 |
|---|---:|---:|---:|
| 1e-6 | 0.0005000003 rad | 0.0003333337 | 0.0003182595 |
| 1e-5 | 0.0021794518 rad | 0.0014529781 | 0.0013865256 |

For the 1e-5 ceiling the phase tolerance is about 0.125 degrees; the positive
duration tolerance is about 0.0925 percent of T. The eta ceilings apply at
preparation, not after cosmological expansion. The earlier expanding-energy
bound would need reevaluation for any nonideal initial eta.

## Evidence and remaining work

`source_preparation.py` checks 27 combinations of phase, duration and frequency
ratio, including independent ODE integration of the charge torque. It checks
switch-work conservation, the charge efficiency bound, the ideal circular
endpoint and 41 samples of the exact phase identity. All 124 checks pass;
`source_preparation_run/manifest.json` validates. This is self-reviewed
analytical and numerical evidence, not independent review.

The pulse makes the source preparation concrete and accounts for its energy.
It still assumes the initial displacement L, its relative phase, an external
clock and symmetry-breaking switch. At L=0 its classical trajectory remains
zero. An autonomous completion would need an explicit clock/inflaton coupling,
a mechanism preparing the displacement and phase, bounded residual charge
breaking after the pulse, and perturbation/inhomogeneity checks. Those are
additional model requirements, not already established consequences.

The inherited tiny repulsive contact, halo transport, abundance and the
repo's acceleration/vacuum-density relation remain unresolved. No laboratory
recipe or demonstrated new physical substance follows from this construction.
