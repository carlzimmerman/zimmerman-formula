# Common field, vector and local decay transport

`common.py` extends the existing 25 scalar/Weyl groups by broken-vector
longitudinal/transverse groups with degeneracies 12/24, and unbroken transverse
SU3/SU2/U1 groups with degeneracies 16/6/2. The common analytic broken-vector
mass is mV²=25 g²[2/(31e)+x²]. Its same derivative enters the scalar gas force.
All vectors are bosons. The inherited scalar/Weyl occupations, momentum nodes
and number normalization are unchanged when vectors are initially empty.

`run_common003` checks embedding, statistics, vector polarization counts,
analytic masses and force derivatives. `run_initial_vector001` constructs the
fresh N=0 packet with exactly empty vectors, the original FD charged fermions,
the same initial energy and independent work zero. It carries no inaccurate
CC10 warm energy prefix. The initial state has 30×40 physical number coordinates.

`joint_history.py` combines the frozen `split_energy_v7.py` endpoint-Hamiltonian
update with `VectorFactory` table003 and positive two-node angular quadrature
on each daughter-energy interval. Each bounded segment retains actual Y,
fermion holes, action, energy and the independent cumulative FRW work. Its
checkpoint ancestry is part of the result. The tested root tree history
contains scalar/fermion and polarized vector 1↔2 reactions. Elastic gauge
scattering and loop decays are separate dependencies; they are not silently
treated as sinks or appended onto an unrelated late state.

Energy closure and physical state refinement are distinct. Constant collision
Hamiltonian plus independently integrated FRW work detects the old finite-stage
coupling defect. Backward Euler populations remain first order. A small ledger
residual cannot establish a small error in the action or distribution. The
energy package and independent direct field controls provide separate tests.

The default `GenericOrbit` implementation inherited a harmonic geometry branch
below J/J_initial=1e-7. That is an approximation, not an action floor. Tiny
excitation on top of a large total energy also loses float64 precision. Neither
the warm common history nor the small-action stress fixture establishes
uniform accuracy for a cold narrow resonance. Any later adiabatic reduction
must bound its displacement, kinetic energy and resonance-line error.

## Local on-shell loop operator

`loop_transport.py` embeds the independently reviewed leading two-body pole
widths, including direct gauge pairs, χ+adjoint gauginos and the octet gaugino
pair. The scalar parents are isotropic, and each width is per normalized parent
component. Inclusive identical-particle and color factors are already in that
width. Multiplying by the common parent measure gP W/(2π²) supplies the correct
total decay count, with no further color average or pair factor. The finite
entropy projection retains each daughter group and its availability, so the
reverse term, quantum detailed balance and energy conservation are present.

This representation-averaged inverse closure assumes spin-symmetric,
representation-symmetric occupations. It is not a general polarization density
matrix. The factory refuses x away from the checked pole. Using the pole width
at arbitrary evolving x is unsupported. The interpolated common parent masses
differ from the exact matching masses by 9.0e-9 and 4.85e-9 relative; this is
explicit in the local control. It does not extrapolate their widths in x.

`run_loop001` checks quantum equilibrium, bosonic vector statistics, the two
parent loss rates, both χ branches, two daughters per decay, retained energy,
hard-daughter support, positive nonthermal entropy production and the analytic
number Jacobian. For Tc/mu=1e-6, its 72-node grid extends to q=30000, instead of
the warm history's q≤80. The soft-parent control has zero omitted physical rate
and daughter-energy residuals below 2e-16 relative. This is a local operator
control, not a common late history or a continuum-grid certificate.

## Binary transport and very small occupations

`binary_events.py` implements positive, energy-conserving 2↔2 redistribution
with a reduced stoichiometry and a cancellation-aware affinity. The caller
supplies the physical kernel and all pair/orientation factors. Its number
coordinates and Jacobian match the quantum solver interface. `run_binary001`
tests this algebra independently of a physical Coulomb rate.

An actual late Coulomb run exposed a Jacobian overflow at positive ghost-tail
numbers around 2e-288: `1/f` overflowed before multiplication by a zero flux.
`binary_events_v2.py` bounds the Jacobian number-coordinate denominators below
1e-280. It changes neither the collision RHS nor an accepted occupation. This
is a declared numerical one-sided Jacobian regularization, not clipping,
particle production or an asserted analytic derivative below that budget.
`run_binary002` retains all earlier algebra controls and adds finite RHS/Jacobian
tests at positive occupations 1e-288 and 1e-310. The physical Coulomb builder,
screening, quadrature and conditional cold-history checks live in `../vectors/`.
