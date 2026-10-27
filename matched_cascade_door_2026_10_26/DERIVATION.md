# Finite-mediator cascade and compression work

This calculation is prompted by the literature scan but uses the project's
existing matched Hamiltonian. No theorem in OpenAI/math establishes the result
below. In particular, free-wave smoothing is not a lower bound on radiation or
a guarantee of relaxation.

## Local model and exact quadratic problem

Use the homogeneous pure-T sector, frozen carrier, zero background scalar
gradient and the same local 3D extension as NC. The radial equilibrium supplies
rho0 and u0, but it does not supply angular mode occupations. All coefficients
remain inherited assumptions. Set n=rho-rho0 and b=s-lambda rho0, and remove
the constant derivative coupling by the canonical phase/shift-momentum change
with A0=g1+h lambda rho0. The velocity potential is phi. The remaining local
Hamiltonian is

    H = (rho0+n)/2 |grad phi-h b grad chi|²
        + kappa |grad n|²/[8(rho0+n)] + U_response
        + [Pchi-h b(rho0+n)]²/2 + c²|grad chi|²/2
        + Ps²/2+c²|grad b|²/2+M²(b-lambda n)²/2.

The constant-background term and linear chemical potential are removed when
forming the perturbation problem. For transverse Fourier vectors, the inherited
response gives the quadratic gap G=rho0[(1-u0)^(-1)-1]; its cubic contribution
vanishes. Define Omega0²=G+kappa k^4/4, C=c²k², H=h rho0, x=omega².
Eliminating the density phase gives the Hermitian frequency system

    [(Omega0²-x)/(rho0 k²)+M²lambda², -M²lambda,       0       ]
    [-M²lambda,                     M²+C-x,       i H omega ]
    [0,                            -i H omega,       C-x     ].

The code solves its slow density root using a cancellation-free Schur form:

    0 = Omega0²-x + rho0 k²
        [lambda²(C-x)²-g2²rho0²x]/[(C-x)(1+(C-x)/M²)-alpha rho0²x],

where g2=h lambda and alpha=h²/M². It remains below the scalar pole in all
tested cases. No assertion about other branches or arbitrary k is needed.

For a mode with density amplitude A, define

    B = (h b)/n = g2/[1+(C-x)/M²-alpha rho0²x/(C-x)],
    phi = -i omega A/(rho0 k²),
    h b = B A,
    chi = i omega rho0 B A/(C-x),
    chi_t = x rho0 B A/(C-x),
    Pchi = rho0 B A C/(C-x),   Ps = -i omega b.

The canonical symplectic normalization is

    1 = 2 omega A² [1/(rho0 k²)+(B/h)²+rho0²B²C/(C-x)²].

An independent quadratic-energy check gives E=omega for this normalization.
This is essential: normalizing density amplitudes using the bare fluid alone
would give incorrect cubic coefficients and coupling times.

## Exact cubic interaction of this local parent

Taylor expansion in canonical variables gives

    H3 = n |grad phi|²/2
         -rho0 h b grad phi.grad chi
         -kappa n|grad n|²/(8rho0²)
         -h n b (Pchi-H b).

The tracking square is quadratic. No phenomenological damping is inserted.
For k3=k1+k2, substitute the exact normalized positive-frequency modes for
1 and 2 and the conjugate of mode 3. Sum all distinct assignments to the cubic
factors. The coefficient is the exact local parent vertex V in
H3=V z1 z2 z3*+conjugate, with the specified box normalization.

`exact_vertex_checked.py` does this algebraically. A separate automatic third
derivative of the original, unexpanded canonical squares on an oblique periodic
cell agrees with 2 Re V. Four cases were checked, including the statically
failed 1-pc control. This is a different implementation, not a fresh-person
review or a complete audit of the underlying physical model.

The first audit subtracted two large arrays, Pchi and H b, before differentiating
their squared difference. It lost about 1.4e-9 relative precision in the .01pc
case and failed a 2e-10 tolerance. The corrected audit substitutes the exact
coefficient identity Pchi-H b=chi_t before forming the same square. The failed
source and run are preserved; the tolerance was not loosened.

## Why a tiny mediator range can matter

In the tracking/slow-wave regime, the additional quadratic terms are

    Delta L2 = lambda² n_t²/2 - c²lambda² |grad n|²/2,

with further retarded and mixed derivative corrections. The leading density
oscillator has

    I_k = (1+eta)/(rho0 k²)+lambda²,
    omega² ~= [Omega0²+rho0 c²lambda² k^4]/[1+eta+rho0 lambda²k²],
    eta=g2²rho0³/c².

The extra stiffness relative to the material quantum gradient is
beta=4rho0 c²lambda²/kappa. It can be appreciable while k ell is tiny,
ell=c/M. Scalar inertia Achi=1+alpha rho0² does not divide eta in the slow-wave
limit: the idea that it alone reverses compression softening is incorrect.

The exact-parent calculations validate the reduced frequencies and cubic vertex
over the stated q/range grid, not uniformly over all momenta or backgrounds.
At the original 3.0215kpc patch, .1pc gives beta=.15433. For q=80 its frequency
rises from 1.06658 to about 1.14571 rad/Myr. The nonzero local transfer coefficient
survives. No energy escape fraction has been recomputed for this new model.

## Compression work and its limitation

Consider the intermediate-wavelength regime in which quantum-gradient terms
dominate the response gap, but mediator tracking and scalar quasistatics still
hold. This is NOT k going to infinity at fixed M. Also neglect the small
rho0 lambda²k² inertia correction. Under homogeneous isotropic compression,
k scales as rho^(1/3), eta scales as rho³ and beta scales as rho, so

    d log omega/d log rho
      = 2/3 + beta/[2(1+beta)] - 3eta/[2(1+eta)].

At fixed adiabatic mode action J, E=J omega: positive slope means compression
does positive work on an already occupied mode. It creates no mode from zero
classical amplitude. The equal and opposite mean stress is still required in
a full dynamical calculation.

For 4/5<eta<7/2 the sign becomes positive when

    beta > (5eta-4)/(7-2eta).

The inherited original patch gives a threshold range about .11935pc. That is
a discriminator within a parameter family, not a prediction or fitted value.
New constrained static solutions at .15 and .2pc both retain <1% law error.
Using their own local densities gives positive compression slopes. Exact-parent
finite differences with advected k and fixed u verify the sign at q=80; holding
u fixed is explicit, not a model of the global gravitational response.

Finite compression is more restrictive than the initial slope. For density
factor z>=1, the same approximation gives

    E(z)/E(1) = z^(2/3) sqrt[(1+beta z)/(1+beta) * (1+eta)/(1+eta z³)].

At .15 and .2pc the maximum gains on the new static patches are only .07699%
and .52604%, at z=1.03950 and 1.10841. Thereafter the modes soften again.
This formula's beta->infinity envelope at the original patch gives at most
8.2455% gain; it is an algebraic upper envelope, NOT an admissible infinite-range
physical model. It shows why simply increasing this stiffness is not a large
adiabatic energy source within this local approximation.

Thus one local sign obstruction can be removed without spoiling the inherited
static law, and a nonzero exact-parent transfer channel remains. A strong,
sustained mean-flow feed, its occupations, outgoing flux, and actual formation
are still missing. The next materially different test is a self-consistent
nonadiabatic compression/shear or conversion calculation with reciprocal stress;
another prepopulated fixed-background triad would not settle that obligation.
