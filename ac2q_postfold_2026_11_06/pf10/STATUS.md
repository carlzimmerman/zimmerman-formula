# PF10 — combined concentrations tested against the equations

The original target remains open. The PF09 combined clock/boost stress
construction is excluded by the full native scalar equation in the precise
matched finite-current class below. It is not an established native
continuation. Neither universal nonexistence nor unique singular continuation
from the incoming data has been proved.

## New differential exclusion

[Proof](COMBINED_CURRENT_EXCLUSION.md) and
[independent actual-file audit](review/COMBINED_CURRENT_AUDIT.md).
Smooth full-switch layers have no total matter surface stress if they retain:
a regular nondegenerate metric and strictly timelike planar interface;
r bounded away from zero; uniform cap/source bounds; strong continuous clock
and same-clock polarization matching; anchored positive regular A traces;
finite total stress and specified scalar-current measures; identified regular
outer bulk traces; and the limiting no-normal-dipole conservation law.
Neither r nor clock rapidity is bounded above.

The decisive native identity is

    J.dphi/E = r²(3-2Ar+2gamma r²) >= gamma r⁴-C.

Spatial polarization equations bound A and remove multiplier mass. Finite
stress removes the kinetic current's layer mass; finite total current controls
spacetime variation of Pi. The scalar equation and its product with the
continuous clock then remove r⁴ concentration. Trace and normal-flux conditions
remove the remaining boost stress. Thus the positive high-clock constituent
needed by the PF09 mixture cannot be realized in this class.

The current is the specific representative displayed in the proof. Finite
variation is not invariant under uncontrolled Noether-current improvements.
Failure of this bound need not mean infinite net physical charge.

## Separate obstruction without the finite-current bound

[Restricted branch barrier](BRANCH_BARRIER.md) and
[independent derivation/correction](review/BRANCH_BARRIER_AUDIT.md).
For a low incoming branch with Astar²>6gamma, a smooth path to high r must
cross r=A/(2gamma), where h=r>0 and Hrr=3-A²/(2gamma)<0. The full coupled
local scalar principal symbol has nonreal characteristics there. Consequently
there is no everywhere-hyperbolic smooth layer of this kind.
For homogeneous D=0 data this sufficient condition is

    u=gamma r0² < 2-sqrt(3).

The recorded u=.001 fixture satisfies it. The earlier proposed all-u<1
barrier was false; u=1/2 is a retained constitutive counterexample. This is a
local hyperbolicity obstruction, not a proved nonexistence theorem for
mixed-type or weak solutions, nor a general nonlinear illposedness theorem.

## Remaining selection gap

[Finite-current necessity audit](review/CURRENT_BOUND_R2.md) identifies the
missing estimate: a uniform spacetime BV bound for Pi, or weaker compactness
sufficient to pass the clock/current product. The constraints bound variation
along clock slices. They do not yet bound temporal polarization variation
through a full-switch layer with unbounded r and boosts. Compact hyperbolic
inverse estimates from PF09 do not cover this regime.

R1 is resolved under the declared hypotheses. R2 remains open beyond them.
R3 has no native existence/uniqueness or same-incoming-data nonuniqueness
construction. Cap escape, clock degeneration, polarization jumps outside the
previously excluded corner classes, singular geometry, and unidentified bulk
defects have not all been eliminated. Any rescue using them must solve the
native equations and match the incoming solution; a stress mixture is not enough.
A new admissibility law would be a mathematical completion; additional action
terms or degrees of freedom would be a physical extension. Neither is proved
unavoidable in every singular solution class.

## Additional clock-slab test

[Exact balance and conditional exclusion](review/CLOCK_SLAB_BALANCE.md) tests
an alternative to the finite-current assumption. With regular converging side
fluxes and an initially empty slice charge, the limiting layer must obey

    q(tau)=integral_(tau0)^tau (F_left-F_right) ds >= 0.

The pushed-forward r⁴ concentration is q(tau)d tau/(2gamma). Independently
matched side fluxes force q=0 and exclude the surface stress without finite J.
Negative cumulative feed excludes the sequence outright. Positive feed passes
this necessary test but is not a native field solution. Neither the unknown
outgoing flux nor its uniqueness is fixed by this balance.

The next concrete native-equation test is whether the Einstein/interface and
polarization equations permit such a positively fed charge defect, with the
same incoming solution and the retained trace controls. This route remains
open: the present conservation identity supplies a necessary condition, not
the missing existence theorem. Temporal Pi compactness and singular regimes
outside the retained controls also remain open; no claim that those routes
are exhausted is made.

## Evidence and checkpoint

current001: six exact algebra checks passed. barrier001: six passed, including
the counterexample to the overbroad threshold. Both evidence manifests validated.
These tests verify identities, not analytic compactness or field existence.
The analytic claims have independent reviews linked above. No new numerical
evolution or physical regularizer was introduced.

Base checkpoint: 043b85ce2f. Assessment working HEAD:
ef4d971bb44d9ddb9e5ee2fba943a6cd82b1d360 (shared repository; concurrent unrelated
work). PF10 is a partial research checkpoint, not closure of the program.
