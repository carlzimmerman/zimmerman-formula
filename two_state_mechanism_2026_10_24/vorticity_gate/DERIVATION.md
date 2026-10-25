# Rotation-dependent conversion barrier with phase stiffness

Status: a constructed, label-free **effective interaction**, not a discovered
fundamental particle coupling. The final results use `angular_gate.py` and
`run_angular{64,128,256}`. Earlier polynomial constructions are historical.

## 1. Physical variables rather than object names

Let x be a collective internal mixing angle in units pi/2:

    q_T = sin^2(pi x/2),  q_F = cos^2(pi x/2),
    rho_T = q_T rho_c,    rho_F = q_F rho_c.

These are nonnegative for every real x and sum to the same positive rest
mass density rho_c. This parameterization alone is not a single-particle
Hamiltonian: the nonlinear barrier is an assumed interaction in a medium.

Define local baryon moments v_b and sigma_b^2=trace Cov(v)/3, and

    omega = curl v_b,
    L_rho^-2 = |grad log rho_b|^2 + ||Hess log rho_b||_F,
    B = sigma_b^2/L_rho^2,
    C = omega^2/(omega^2+B).

C lies in [0,1]. It is unchanged by constant velocity boosts and rotations of
spatial coordinates. It measures net vorticity relative to a pressure-motion
frequency. It is not a galaxy label or a temperature threshold. This choice
of density length is an ansatz; a microscopic smoothing prescription and a
vacuum prescription when rho_b=0 remain missing. C=0 is used for zero mean
vorticity with finite dispersion. The zero/zero case needs a physical extension.

## 2. A constructive positive interaction

Keep the original W_full(u), with K=4 pi G and u=K|P|. Write

    e(u) = u W_full'(u) >= 0,
    S(x) = sin(pi x)/pi,
    E_int density = beta e(u) [z^2 + (omega^2/B)(z-S(x))^2].

z is a proposed fast internal strain variable. The interaction penalizes
rearrangement during state mixing in a rotating background. Both quadratic
terms have positive coefficients. For B>0 and e>0, minimizing over z gives

    z_* = C S(x),
    E_int,min density = beta C S(x)^2 u W_full'(u).

The cold rotating limit B->0 imposes z=S and gives C->1. The elimination is
checked numerically over 2665 points and also follows by completing a square.
This is a positive auxiliary-mode representation of the chosen coupling,
not evidence that nature contains z or that its coefficients follow from
known particle physics. A kinetic term and finite response of z are not tested.

Add a positive phase-gradient energy

    E_grad density = (a0^2/(2K)) ell_chi^2 |grad x|^2.

The tested common values beta=20 and ell_chi=30 kpc were selected from a
feasibility scan. They are not independently measured or derived. ell_chi
is a new internal-state length, not the paper's polarization stiffness L*.

The endpoint identities S(0)=S(1)=0 and S S'=0 mean the interaction, its
first spatial force, and its first variation in P or baryon moments vanish
in a uniform pure phase. The gradient energy also vanishes there. Therefore
a pure T equilibrium retains the original acceleration relation; this is
why a barrier coupling avoids the force introduced by a variable binding gap.
Mixed phases can exert forces and must not be treated by the endpoint argument.

## 3. State conversion is spatially coupled

The polarization represents actual T mass:

    M_T(r) = integral_0^r 4 pi s^2 rho_c(s) q_T(s) ds,
    u(r)=G M_T(r)/r^2.

We do not use u(r)=q_T(r)u_initial(r) when q_T varies with r; that violates
the density relation. In the discretization, q is constant in a mass cell
and its within-cell enclosed fraction is evaluated from the initial positive
mass profile. The initial u therefore matches the continuum law at every
evaluation point. All masses remain gravitating in both states.

The simulated energy includes the field energy to infinity, the barrier
inside the finite mass domain and the phase-gradient term. A zero-normal-
gradient phase boundary is imposed at the supplied halo cutoff. Total mass
positions and baryon fields are fixed during this internal-state experiment,
so their ordinary gravitational energy is constant and cancels from energy
differences. This is not a live gravitational collapse calculation.

## 4. Why phase stiffness matters

Let m_i be the fixed cell mass, V_i its field quadrature volume,
mu_i=dU_field/dM_T,i, and F_i=u_i W_full'(u_i), with common normalization
factors suppressed. At the pure T endpoint, h'(1)=0, h''(1)=-pi^2/2,
S^2=0 and (S^2)''=2. The internal-state Hessian is

    H = diag[-(pi^2/2) m_i mu_i + 2 beta C_i F_i V_i] + L,

where L is the positive phase-gradient matrix. There are no other cross
terms at that endpoint. The formula is checked against finite differences
of the full energy gradient, not an independent-cell surrogate.

Without L, a weakly protected core can be unstable even when a uniform-phase
test suggests protection. L penalizes spatial differences and can stabilize
that core as part of a rotating system. Conversely, the uniform vector obeys
1^T L 1=0. If the diagonal contribution has negative sum, no increase of L
can stabilize T against that uniform trial direction. The weak-streaming
profiles satisfy that obstruction in the tested parameter neighborhood.

We compute the lowest generalized eigenvalue with a positive reference mass
metric D. Its sign determines local energetic stability. After gradient
damping is included the actual drag metric is D+L; congruence by another
positive metric preserves stability signs, but the quoted eigenvalue
numbers are not physical rates.

## 5. Explicit dissipative receiver

The assumed Rayleigh dissipation is

    R = (dot x^T D dot x + dot x^T L dot x)/2,
    (D+L) dot x = -grad E,
    dot Q = dot x^T(D+L)dot x >= 0.

Hence d(E+Q)/dt=0 for fixed baryon fields and density. D is positive and
uses m_i mu_i from the reference T profile; its dimensional normalization
is an undetermined relaxation time. The |grad dot x|^2 dissipation represented
by L is an additional assumption, not a change hidden in a numerical solver.
The bath receives a positive, independently integrated heat variable. It has
no prescribed microscopic carrier, finite temperature or fluctuation spectrum.

The tests use zero-noise dissipation and internal time 100. These units are
not Gyr, and no conversion rate or lifetime is inferred. Changes in baryon
kinematics would perform work through C and require baryon backreaction;
such time-dependent backgrounds are not simulated.

## 6. Kinematic inputs and the absence of type flags

Each numeric Plummer mass/size profile is crossed with the same streaming
family, including counterfactual strongly rotating small objects and weakly
rotating large objects. We set

    v_phi = f v_c r/sqrt(r^2+(0.1b)^2)

and compute the dispersion from the radial Jeans integral with centrifugal
support. The rotation-gradient curl and analytic density derivatives then
give C. f is a continuous physical input, not inferred from an object name.
The Jeans construction is a spherical-background/midplane approximation;
it is not a self-consistent 3D rotating distribution function.

The same beta, length, friction, seed and stopping time are used across all
profiles. Metadata are attached only after the field calculation. Protection
is conditional on beginning close to T. Small objects with strong streaming
are protected in the tested model, whereas large objects with weak streaming
convert. The artificially strongly rotating cluster-size profile is an
explicit failed-protection counterexample at the chosen length.

## 7. Structural limitations and falsifiable consequences

At fixed density E_field>=0, E_int>=0 and E_grad>=0, while uniform F has
zero field and barrier energy. It is a global minimum of this internal-state
energy. Dissipation alone cannot raise an exactly free state into a higher-
energy tethered state. The reverse-history tests confirm that starting near
F remains near F even in a strongly rotating galaxy-size background. A real
formation mechanism must supply the work and initial conditions.

An equal counterrotating mixture has zero mean vorticity and finite centered
dispersion: C=0. This interaction provides no protection merely because each
stream is individually ordered. That is a concrete prediction/limitation,
not something to remove with a galaxy classification flag.

A uniform mixing path provides a barrier upper bound, not a true nucleation
barrier or thermal lifetime. Finite-noise escape, open boundaries, neighboring
systems, the 30 kpc interaction range, live mass redistribution, actual disk
geometry, relativistic completion and observed kinematic maps remain untested.
