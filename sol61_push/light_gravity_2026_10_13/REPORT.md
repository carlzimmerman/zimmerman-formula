# Could the proposed carrier emit visible light and move an object gravitationally?

Status: coupling audit and quantitative benchmark, not an established device or
new-physics mechanism. The user's clarified target is a force large enough to
move an object. The carrier remains hypothetical.

## What the current action says

The pinned INPUT_CARRIER_ACTION.tex contains g*(chi*phi^2+conjugate) and a
quartic daughter self-interaction. Its U(1) charges are 2 for chi and 1 for phi.
The displayed symmetry is global; these charges are not declared electric
charges. There is no electromagnetic vector potential or photon interaction
in that displayed action. Thus the candidate is not gravity-only internally,
but its computed dark reactions do not by themselves predict visible emission.
This audits this research lane's action, not every file in the entire repository.
Its metric-gravity completion also remains an open obligation.

Exact U(1) conservation forbids an isolated positive-charge source or daughter
from converting entirely to neutral photons. A reaction retaining charge in the
final dark particles, such as chi -> phi+phi+gamma+gamma, is charge-compatible.
Charge compatibility is necessary, not sufficient for a nonzero rate.

## One possible extension, explicitly NOT derived

An illustrative low-energy electromagnetic portal is

    Delta L = -zeta/(4*Lambda^3)
              *(conj(chi)*phi^2+chi*conj(phi)^2) * F_munu F^munu,

where conj denotes complex conjugation. The two dark-field terms are
Hermitian conjugates.
The operator has canonical mass dimension seven in four dimensions, is neutral
under the stated global U(1), and uses the gauge-invariant photon field strength.
It can provide a radiative conversion vertex preserving the dark charge.

This term is absent from the supplied action. zeta and Lambda would be NEW
parameters; no UV completion, coefficient, branching ratio, experimental
admissibility or preferred wavelength has been established. Treat it only as a
possible additional hypothesis. The combined Maxwell kinetic coefficient must
remain positive and the effective expansion controlled on the states used;
writing a gauge-invariant operator alone is not a viability proof.

For a source at rest, positive-energy free daughters and no incoming energy,
energy conservation gives

    E_photons + K_daughters = (M-2m)*c^2,
    0 <= E_photons <= (M-2m)*c^2.

In natural units the ceiling is delta=M-2m. The revised illustrative benchmark
m=1 MeV and M=2m*sqrt(1+0.02^2) gives delta=399.960008 eV. A 550 nm visible
photon has energy 2.254258 eV, so visible photons are kinematically possible
with an added coupling, but the operator does not select visible wavelengths
or a narrow line. Energy can remain in daughter motion or other photon
frequencies. Ordinary conversion of higher-energy emission into visible light
would require additional material and energy accounting.

The earlier charge-bound E>=m|Q| concerns the unextended isolated model. It
must not be claimed unchanged for every added interaction. The above energy
ceiling instead follows directly from asymptotic positive-energy daughter
masses and energy conservation for the stipulated completed event.

## How much ordinary gravity would move the object?

Choose a transparent benchmark: a free test object initially at rest, a fixed
compact spherical/point source, initial center separation r0=0.1 m, inward
motion x=0.01 m in t=1 s, and no friction or other force along that direction.
No claim is made that the required mass can be practically confined there.
The Newtonian equation is r''=-G*M/r^2. Its exact radial fall relation is

    t=sqrt(r0^3/(2*G*M)) * [acos(sqrt(y))+sqrt(y*(1-y))],
    y=(r0-x)/r0.

Solving gives M=2.895987e6 kg. This acceleration is independent of the small
test mass; ordinary support, drag, friction or a lifting requirement changes
the benchmark. Six radial cases were independently checked by integrating the
ODE. A simple constant-acceleration estimate gives about 3.0e6 kg and is close,
but the reported value includes the changing separation.

For a closed weak-field apparatus with ADDED stored energy U and all internal
stresses accounted for, its mass increment is DeltaM=U/c^2. Supplying the entire
above source mass this way would require U=2.602784e23 J. This is an energy
EQUIVALENT, not the energy needed to reposition preexisting mass. A source could
already contain mass, but no controlled collection/rearrangement of such dark
mass has been derived here.

Adding 100 J to a compact closed apparatus changes its far exterior acceleration
at 0.1 m by only 7.42616e-24 m/s^2. Converting energy already inside a closed
apparatus into light does not add 100 J to that apparatus. Emitting energy
reduces the source's total mass-energy and transfers energy to radiation; it
does not create a new gravitational charge. Freely propagating radiation needs
its actual stress-energy and geometry, not a static point-mass reinterpretation
of luminosity alone. No proposed enhancement of gravity has been derived.

## Light can move objects without gravity

For normally incident intercepted optical power P, momentum transfer gives
F=P/c for complete absorption and F=2P/c for ideal reflection. These mechanisms
are used in [NASA solar-sail research](https://www.nasa.gov/general/steering-of-solar-sails-using-optical-lift-force/).
For P=100 W, the absorption force is 3.33564e-7 N. On a free 1 g test object,
ignoring heating and all other forces, that corresponds to 0.167 mm displacement
in one second. This is optical power actually intercepted, not a lamp's
nominal electrical rating or a promise of safe illumination.

An observed luminous source moving an object would therefore require separating
photon momentum, heating/air motion, electric and magnetic forces from gravity.
Brightness does not establish gravitational origin. A diffuse visible glow could
accompany a different process without being the source of its force.

“Bright but not blinding” is not a physical energy or force specification.
Perceived brightness/glare depend on spectrum, source radiance, apparent size,
distance and exposure. This work supplies no eye-safety certification; the
motion and power examples are calculations, not instructions to build or view
an intense source.

## Research consequence and evidence

Three separate obligations remain: a justified photon coupling, a mechanism
changing the mass distribution or a verified metric response, and an actual
light spectrum/radiance calculation. An illustrative portal addresses only the
first at the level of a new hypothesis. It does not solve gravity or supply an
object-moving device.

Constants use the [NIST/CODATA listing](https://physics.nist.gov/cuu/Constants/Table/allascii.txt):
G=6.67430e-11 SI, c=299792458 m/s, h=6.62607015e-34 J s and
1 eV=1.602176634e-19 J. G is measured, the latter conversion/constants are exact
SI definitions. Numerical digits are computational output, not precision claims
beyond input uncertainties. run/results.json gives six ODE cross-checks and
all example scales. The photon extension has NOT been physically or Lean
certified; prior Lean results do not certify new interaction terms.
