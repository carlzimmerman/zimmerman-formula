# Quantum pressure and expansion-work bounds in the regulated NR model

## Result and assumptions

The positive regulated quantum Hamiltonian in [NR_QUANTUM_BOUND.md](NR_QUANTUM_BOUND.md)
also bounds its integrated pressure, including conversion stress. For the
detuned example, a prescribed monotonic millionfold expansion preserves an
upper bound |P|/rho <= 0.000372911 for the volume-averaged material pressure.
This is an upper bound, not a predicted equation of state.

Assumptions: fixed comoving finite regulator; normal-ordered leading NR
Hamiltonian; positive quadratic kinetic operators; constant masses and
couplings; homogeneous externally prescribed scale factor a; no gravity
of perturbations, external injection or varying vacuum portal. The proof
allows arbitrary quantum states and conversion dynamics in this model.
It does not establish relativistic renormalization, sound speed, local
pressure, small-scale structure or the repo's halo acceleration law.

## Pressure operator

With notation from the preceding note, use comoving annihilation fields.
The excess Hamiltonian scales as

    D(a) = T(a) + X + W(a) + Y(a),
    T=a^-2 T0, X=delta N_b,
    W=a^-3/2 c integral (b† psi^2 + psi†^2 b),
    Y=a^-3 k integral psi†^2 psi^2.

Physical cell volumes scale as a^3. At fixed comoving fields and regulator,
the integrated pressure is the volume derivative

    Pi := P V = -(1/3) partial D/partial log(a)
              = (2/3) T + W/2 + Y.

The rest term mQ and gap term delta N_b have zero volume derivative. This
is the spatially averaged stress conjugate to homogeneous expansion in the
specified Hamiltonian, not a thermal-equilibrium assumption.

Put r=c/sqrt(delta k), with r^2<1. For the two operator components
sqrt(delta)b and sqrt(k)a^-3/2 psi^2, the interaction quadratic forms for
D and Pi have coefficient matrices

    A = [[1,r],[r,1]], B = [[0,r/2],[r/2,1]].

The generalized eigenvalues of (B,A) are

    beta_- = (1-1/sqrt(1-r^2))/2,
    beta_+ = (1+1/sqrt(1-r^2))/2.

Therefore beta_- A <= B <= beta_+ A as ordinary two-by-two matrix
inequalities. Substitution of operator-valued components preserves the
positive quadratic forms O†O. Since beta_-<=0<2/3<1<=beta_+ and T>=0,

    beta_- D <= Pi <= beta_+ D

as an operator inequality at every a. No Gaussian factorization or
classical approximation to the state is used. For any state with
E=m<Q>+<D> and d=<D>/(m<Q>),

    |P|/rho <= beta_+ d/(1+d), rho=E/V.

Here r^2=0.49998750094, beta_-=-0.20709794318 and
beta_+=1.20709794318. In a fixed box initialized with zero-momentum sources
and daughter vacuum, d=delta/(2m), yielding |P|/rho<=6.03504e-5 at all
times of the exact regulated evolution.

## A charge-controlled expansion bound

Using only beta_- would give a loose power-law upper bound on expansion
work. Completing a different square gives a stronger result:

    Y+W/2 = integral |sqrt(k)a^-3/2 psi^2
                          + c b/(2sqrt(k))|^2 - c^2 N_b/(4k).

Thus Pi >= -c^2 N_b/(4k) >= -r^2 delta Q/8, because
2N_b<=Q. This is another operator inequality. For unitary evolution with
time-dependent a, the commutator of D with H=mQ+D vanishes, so

    d<D>/dt = <partial D/partial t> = -3 Hubble <Pi>.

For monotonic expansion and conserved <Q>, integration yields

    <D(a)> <= <D(a_i)> + (3 r^2 delta <Q>/8) log(a/a_i),
    d(a) <= d_i + [3 r^2 delta/(8m)] log(a/a_i).

This is valid for arbitrary expansion rate within the stipulated NR model.
It bounds possible negative-pressure work without specifying source
occupation as a function of time. It does not assert that material energy
actually increases; many states can cool much more rapidly than this bound.

| Expansion a/a_i | Upper d=<D>/(mQ) | Upper |P|/rho |
| ---: | ---: | ---: |
| 1 | 4.99988e-5 | 6.03504e-5 |
| 10 | 9.31701e-5 | 1.12455e-4 |
| 1000 | 1.79513e-4 | 2.16651e-4 |
| 1000000 | 3.09027e-4 | 3.72910e-4 |

The associated coarse kinetic RMS bound at the last row is 0.0248607 c.
That loose upper bound is not a cold-dark-matter velocity prediction or
an observational viability result. Low mean pressure alone does not bound
the derivative response of pressure to density or the free-streaming scale.

## Audit and remaining work

`nr_quantum_pressure.py` builds the complete two-cell charge sectors
Q=2,4,6,8,10 at a=0.1,1,10,1000. It checks the upper and lower pressure
operator inequalities, the charge-only lower bound, and the volume derivative
against finite differences. All 80 checks pass. The analytic identities
supply the arbitrary-state fixed-regulator proof; the finite tests audit
implementation. The contract, results and validated manifest are in
`nr_quantum_pressure_run`.

This extends the quantum kinetic result to the combined system's global
stress and homogeneous expansion work. It does not validate the Gaussian
production fraction, its spatial survival, a continuum quantum completion,
or the target vacuum-dependent galaxy law. A next step is to test whether
the same protected model admits the required halo response rather than
assuming low pressure is enough to produce it.
