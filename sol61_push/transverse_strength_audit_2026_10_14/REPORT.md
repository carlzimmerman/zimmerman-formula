# What a transverse-current sum rule does and does not imply

2026-10-14. Parent checkpoint: 4586e19cf30c1452c369b0839c5bb3d6ed1e2ad2.

Verdict: **correct only after a stated restriction**. At fixed momentum transfer,
a nonrelativistic single-site transverse-current strength equals the site's
transverse velocity variance. This yields a useful production-rate ceiling in
a frozen-response, leading-small-momentum approximation. It does not establish
an all-material bound along the actual energy-dependent momentum-transfer curve.

The previous turn made progress by deriving, running and publishing the harmonic
transverse-current channel. This turn tests the proposed generalization of that
result rather than treating three oscillator cases as a universal conclusion.

## Exact fixed-momentum closure identity

Let one site have mass M and canonical operators x,p. Use a complete final-state
basis, normalized initial state |i>, and spatial momentum transfer Q. Choose
transverse components a perpendicular to Q. For the same current convention as
the preceding package,

    rho(Q)=exp(i Q.x),
    j_a(Q)={p_a,rho(Q)}/(2M)=rho(Q) p_a/M.

The second equality follows from [p_a,Q.x]=0. Therefore completeness and
unitarity give, provided the initial momentum second moment is finite,

    sum_f |<f|j_a(Q)|i>|^2
       = <i|j_a(Q)^dagger j_a(Q)|i>
       = <i|p_a^2|i>/M^2.

Sum the two transverse components and denote the result V_perp^2. Velocities
are in units of c, and the expression is a second moment, not a centered
variance unless the mean transverse momentum vanishes. In the harmonic ground
state the mean vanishes and V_perp^2=Omega/M. Interference between different
charged sites and multi-particle electromagnetic currents is not covered by
this single-site identity.

This is a derivation in the nonrelativistic operator model. It does not imply
that a new scalar exists or that any assigned target parameters are attainable.

## Positive-excitation kinematic ceiling

For a mediator exactly at rest, energy conservation gives omega=M_R+Delta,
Q=omega and t=-M_R(M_R+2Delta). A transverse transition with current strength
J_f^2=sum_a |<f|j_a|i>|^2 has polarization-averaged amplitude

    average |M_f|^2 = 2M^2 g^2 Z^2 e^2 omega^2 M_R^2 J_f^2/t^2.

Together with the preceding heavy-site phase-space normalization, the rate
kernel per d^3P and per spectral flux is

    alpha g^2 Z^2/(8pi) * omega M_R/t^2 * J_f^2.

For Delta>=0, writing x=Delta/M_R,

    omega M_R/t^2 = (1/M_R^2) (1+x)/(1+2x)^2 <= 1/M_R^2,

because (1+2x)^2-(1+x)=3x+4x^2>=0. This scalar inequality is exact at P=0.
An excited initial state with negative energy-transfer channels does not meet
this hypothesis. No finite-temperature universal bound is asserted.

To use closure in a finite cold-momentum acceptance, now impose two additional
approximations explicitly: take the leading kernel at P=0 and replace the
response matrix elements at their different Q values by those at one fixed Q0.
This is the **frozen-response approximation**. With S(omega)<=S_peak,

    rate_T <= C * V_perp^2,
    C = N_column (hbar c)^2 Br_phi S_peak alpha g^2 Z^2/(8pi M_R^2)
        * integral A(P) d^3P.

This is a bound within that approximate response calculation, not an exact
bound on the full physical finite-acceptance rate. The actual P=0 point alone
has zero phase-space measure; the integral uses the explicitly stated leading
small-P expansion. A sharp momentum-dependent response needs separate error
control even when the fractional Q change is small.

## Numerical scale, retaining the prior source assumptions

The prior flux 1e8 photons/s, RMS bandwidth 5000 eV, site column 3e25/m^2,
Z=82, g=2.93129374869688e-15/eV, M_R=2 MeV, branching fraction 1/2 and
cold acceptance volume 0.051321315544673216 eV^3 give

    C = 1.0030299663e-27 pairs/s per unit V_perp^2.

Substituting V_perp^2=Omega/(200 GeV) exactly reproduces the preceding leading
harmonic transverse rates. For the hypothetical nonrelativistic diagnostic
sqrt(V_perp^2)=0.01, the ceiling in this approximation is approximately
1.003e-31 pairs/s. No target with that velocity distribution is specified.

Solving the approximate expression for one pair per year requires
V_perp^2=3.159e19, far outside the nonrelativistic model. This is a diagnostic
of how inadequate the fixed source and column assumptions are in this regime;
it is not a calculation with superluminal matter. In particular, replacing
one oscillator frequency by another cannot be advertised as a solution without
changing the response or other source assumptions quantitatively.

## Why fixed-Q closure is not a general physical-rate bound

The actual rate samples each final state's matrix element at
Q_f approximately M_R+Delta_f, not at a common Q0. The implication

    for every Q, sum_f w_f(Q)=1
    therefore sum_f w_f(Q_f)<=1

is false. As a continuous positive counterexample, choose eight narrow Gaussian
peaks centered at q_f=1+f*1e-6 and normalize their sum at each q. Their width is
1e-7. At every q the weights sum to one, but sum_f w_f(q_f) is approximately
eight. Even a tiny fractional change in momentum does not fix this inference.
These are abstract response functions, not a claimed physical Hamiltonian or
an engineered target. Their sole purpose is to refute the inference from
normalization alone. A real candidate must satisfy its own dynamics, locality,
energy spectrum, electromagnetic current structure and measured constraints.

Thus the exact missing implication for a material-independent ceiling is
control of the response on the energy-momentum curve, or a separate sum rule
that actually constrains that curve. Fixed-Q completeness by itself supplies
neither. We have not found a material exploiting this gap.

## Audit and evidence

Dependency graph:

- The current operator and single-site approximation are modeling assumptions.
- Transverse commutation, completeness and unitarity yield the exact fixed-Q
  second-moment identity, subject to the finite-moment/domain condition.
- The previous scalar-photon normalization supplies the rate kernel.
- Positive excitation energy yields the scalar kernel ceiling.
- Frozen response and leading small P connect closure to the approximate rate.
- The source parameters remain assigned and the particles hypothetical.

Obligations: fixed-Q operator derivation passed by self-review; finite closure
and harmonic recovery computationally verified; scalar inequality proved in
Lean; frozen response conditional and not justified for arbitrary materials;
physical all-target bound not established; manufacture/capture not established.

The bounded script checks 18-dimensional unitary matrix exponentials at three
q values and three initial state pairs, complete final-state column sums,
harmonic momentum moments, the scalar kinematic identity at six points,
normalization of the eight-response counterexample, and recovery of all three
previous leading rates. The finite matrices are independent tensor factors for
longitudinal displacement and transverse momentum. They illustrate closure,
not convergence of a physical target simulation.

StrengthBound.lean proves a finite nonnegative weighted-sum inequality and the
scalar positive-excitation ceiling. It does not prove infinite-dimensional
operator completeness, physical response smoothness, or the production model.
This is self-review, not independent external certification.

Reproduce:

    python3 sol61_push/transverse_strength_audit_2026_10_14/check.py /tmp/transverse_strength_results.json

The executable input and prior result hashes are recorded in run/manifest.json.
The goal remains open. A new material proposal must now provide its transverse
response along the actual scattering curve; otherwise it only renames the
already inadequate fixed-response mechanism.
