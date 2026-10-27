# A quantum kinetic-energy bound for the regulated NR carrier

## Scope

The leading nonrelativistic two-field Hamiltonian admits an exact positive
operator decomposition at fixed regulator. It bounds the combined kinetic
energy under full many-body unitary evolution, including moving sources,
non-Gaussian correlations and conversion from a daughter vacuum. Unlike the
classical energy-square argument, this statement requires no replacement of
operators by classical fields.

It is not a renormalized relativistic quantum-field theorem, a proof that
the previous Gaussian closure follows exact evolution, or a bound on full
pressure, sound speed or halo structure. The source energy and charge are
still initial conditions.

## Hamiltonian and operator identity

Use canonical daughter and source annihilation fields psi and b with charge
one and two. Work at a finite spatial regulator, with positive kinetic
operator T and normal-ordered interactions. Write

    Q = integral (psi† psi + 2 b† b),
    H = m Q + D,
    D = T + integral [delta b† b
             + c (b† psi^2 + psi†^2 b) + k psi†^2 psi^2],
    delta = M-2m > 0,
    c = g/(2m sqrt(2M)), k = lambda_total/(4m^2).

These vertices follow the leading particle-mode normalization
phi=psi/sqrt(2m), chi=b/sqrt(2M), with rest phases removed. Antiparticles,
counter-rotating vertices and relativistic vertex corrections are omitted.
The statement is exact for this specified regulated Hamiltonian, not for
all higher-order terms of its proposed parent theory.

Because b and psi commute with each other,

    D = T + integral delta (b + c psi^2/delta)†
                                 (b + c psi^2/delta)
          + integral (k-c^2/delta) psi†^2 psi^2.

There is no extra commutator constant: the order is creation operators to
the left, and each displayed square is of the form O†O. On a cell of volume
v, the annihilators are dimensionless and the conversion and quartic
coefficients become c/sqrt(v) and k/v. The same factorization holds.

For lambda_total = g^2/[delta(M+2m)] + lambda_rep,

    k-c^2/delta
      = lambda_rep/(4m^2) + g^2/[8m^2 M(M+2m)] >= 0.

This algebraic reduction proves positivity for every positive regulator
volume and every charge sector, not only the finite examples below. A
finite lattice has finite-dimensional fixed-Q sectors, so there are no
operator-domain subtleties in that regulated statement. Removing the
regulator with specified renormalized couplings is a separate problem.

Every conversion term changes daughter number by two and source number by
minus one or conversely, so [H,Q]=0. Since D=H-mQ also commutes with H,

    0 <= <T(t)> <= <D(t)> = <D(0)>

for all times in this unitary model. This holds for entangled states and
moving source populations. It bounds expectation values; it does not say
that every particle has a strict velocity cutoff.

## Initial source and detuned example

Put N source quanta in the zero-momentum mode and daughters in their exact
vacuum. Then <T>=0, the quartic expectation vanishes and the conversion
expectation initially vanishes. Hence <D>=delta N and Q=2N. Conversion is
nevertheless active: psi†^2 b acts nontrivially on this state. No imposed
classical daughter seed is required.

For the detuned example:

- delta = 0.01935200538 eV;
- c = 6.10769488e-8 eV^(-1/2);
- k = 3.85540087e-13 eV^(-2);
- k-c^2/delta = 1.92774863e-13 eV^(-2);
- <D>/(mQ) = 4.99987501e-5.

For quadratic kinetic dispersion define the charge-weighted velocity moment
by Q <v^2>_Q = sum_daughters v^2 + 2 sum_sources v^2, in expectation.
Since M>=2m, T >= (m/2) Q <v^2>_Q. Consequently

    <v^2>_Q <= delta/m,
    sqrt(<v^2>_Q) <= 0.0099998750 c.

This is a global kinetic bound at the production parameters, not the much
smaller late cosmological velocity. Expansion, gravity and time-dependent
backgrounds require their own energy-work accounting. A small kinetic
budget alone does not establish small interaction pressure.

## Finite many-body audit

`nr_quantum_bound.py` constructs complete two-cell fixed-charge bases for
Q=2,4,6,8,10 (dimensions 5,14,30,55,91). It independently forms the
normal-ordered Hamiltonian and positive-square expression. Positive hopping
kinetic terms include both fields. It diagonalizes each Hamiltonian and
evolves the uniform-source Fock state with daughter vacuum through 100
inverse-gap time units, sampled at 501 points.

All 26 checks pass: coefficient positivity, matrix identity, nonnegative
spectrum, initial excess energy, energy conservation and kinetic-energy
bound. Daughters appear without a classical seed; sampled maximum daughter
charge fractions range from 0.411 to 0.967 across these small sectors.
Those fractions depend on this deliberately small regulator and are not
macroscopic production predictions. The numerical audit checks algebra
and implementation; the universal fixed-regulator bound follows from the
displayed operator factorization.

The contract, results and validated manifest are in `nr_quantum_bound_run`.

## Research consequence

Moving-source response need not destroy the combined kinetic coldness:
the quantum NR model can protect its energy budget even when the daughter
fraction changes. This removes the need to assume purely classical dynamics
for that particular budget. It does not transfer the full classical stress
bound to the quantum model, establish a continuum quantum theory, or explain
the repository's vacuum-dependent acceleration law. The next useful
extension is quantum stress/work accounting in an expanding regulator,
with its assumptions kept separate from the relativistic parent theory.

Follow-up: [NR_QUANTUM_PRESSURE.md](NR_QUANTUM_PRESSURE.md) proves
integrated quantum pressure and expansion-work inequalities for the same
regulated NR model; continuum and halo limitations still apply.
