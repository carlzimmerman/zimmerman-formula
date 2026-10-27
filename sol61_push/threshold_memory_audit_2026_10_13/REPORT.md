# Time dependence matters before a stationary linewidth repair

2026-10-13. Base branch checkpoint: db3abaacb0e83c802f6cbc919c4ddd83613510ef.
The accompanying carrier_self_feedback_2026_10_13 package is an explicitly
hashed local dependency. The overall objective remains a justified theoretical
production and storage route for the proposed carrier. This audit changes the
next kinetic calculation; it does not establish a manufacturing mechanism.

## The first uncertain implication

The prior fixed-bath Hartree moment model gave

    J/Jstar = 2s-s^2,  D(t)=D0(1-s)^2,  s=t/tstar.

It used the instantaneous, sharp on-shell rate proportional to sqrt(D).
Before replacing the threshold by a stationary Lorentzian, test whether that
rate is sufficiently local in time. For a rest source, resolving a threshold
separated by energy D requires a characteristic time tau_form ~ hbar/D.
The background threshold changes on tau_var=D/|dD/dt|. A necessary scale
separation for this particular time-local construction is

    epsilon_grad = hbar |dD/dt|/D^2 << 1.

This is a gradient diagnostic, not a rigorous error bound or a universal
Markovianity criterion. Numerical factors depend on the chosen resolution
criterion. It follows by requiring a coarse-graining interval long relative
to hbar/D but short relative to D/|dD/dt|. At the initial instant an additional
switch-on/initial-correlation question remains, even when epsilon_grad is small.

On the prior trajectory,

    epsilon_grad(s)=epsilon0/(1-s)^3,
    epsilon0=2hbar/(D0 tstar).

Taking epsilon_grad=1 only as an order-one warning scale gives

    s_mem=1-epsilon0^(1/3),
    D_mem/D0=epsilon0^(2/3),
    J_mem/Jstar=1-epsilon0^(2/3).

These are diagnostics evaluated on an approximate trajectory, not new
predictions for the true population or the physical time of a transition.

| Bath T (MeV) | epsilon0 | s_mem | D_mem/D0 | D_mem (eV) | D_mem / modeled rest decay width |
|---:|---:|---:|---:|---:|---:|
| 0.5 | 0.09984 | 0.5361 | 0.2152 | 9.4753e-8 | 3.516e4 |
| 1 | 0.05136 | 0.6283 | 0.1382 | 6.8037e-7 | 1.023e5 |
| 2 | 0.03736 | 0.6657 | 0.1118 | 2.5518e-6 | 2.033e5 |
| 3 | 0.03301 | 0.6792 | 0.1029 | 4.7000e-6 | 2.779e5 |

At T=2 MeV the warning is at about 1.03 ns on the old trajectory, before its
formal 1.543 ns closure. The formation and threshold-variation times there
are both about 0.258 ns. The compared decay width is

    Gamma_rest(D_mem)=Gamma_gamma+Gamma_phi(D0)*sqrt(D_mem/D0).

It is the width from the same narrow, spontaneous-decay model, not a full
thermal spectral width. Thermal scattering, medium-enhanced photon reactions,
carrier interactions and decoherence have not been calculated. The table
therefore does not prove that memory dominates every possible broadening.
It shows that merely inserting the previously computed decay linewidth does
not repair the lost time-scale separation. Typical parents in the bath move;
their energy mismatch, time dilation and memory must be treated by momentum.
This rest-source diagnostic does not substitute for that integral.

## Independent finite-duration threshold benchmark

Use a separate prescribed weak pulse, an initially occupied discrete source
and an empty continuum. Parameterize the continuum spectral weight by

    rho(epsilon)*|V(epsilon)|^2 = g sqrt(epsilon) exp(-epsilon/Lambda),
    epsilon>=0, Lambda>0.

Here epsilon is pair kinetic energy measured from threshold, g is a positive
normalization with dimension sqrt(energy), and Lambda regulates the energy
range of the nonrelativistic threshold law. Neither parameter is fitted to
the bath. First-order amplitudes for a constant perturbation acting for
duration t give the leading transition probability

    P(t,D)=g integral_0^infinity d epsilon sqrt(epsilon) exp(-epsilon/Lambda)
           *4 sin^2[(epsilon-D)t/(2hbar)]/(epsilon-D)^2.

At D=0 this integral is exactly

    P(t,0)=4g sqrt(pi) [Re sqrt(1/Lambda-i t/hbar)-1/sqrt(Lambda)].

Derivation: differentiate the integral with respect to b=t/hbar, use the
Laplace integral of epsilon^(-1/2) sin(b epsilon), and integrate back with
P(0,0)=0. The principal square root has positive real part. Independent
quadrature splits the small-energy region from an oscillatory cosine tail;
six values of Lambda*t/hbar from 0.01 to 1000 agree to within 2.2e-12 relative.

For Lambda*t/hbar << 1, the result is

    P ~ g sqrt(pi)/2 * Lambda^(3/2)*(t/hbar)^2.

For Lambda*t/hbar >> 1, while perturbation theory still requires P << 1,

    P ~ 2g sqrt(2pi)*sqrt(t/hbar).

In contrast, the stationary golden-rule rate at D=0 samples sqrt(D)=0.
Thus a vanishing asymptotic linear rate does not imply a vanishing
finite-duration transition probability. This is a standard threshold/switching
effect; it is not a discovery of energy creation or a calculated late-time
reservoir. The finite pulse and initial state supply an energy spread. Switching
work and correlations must be included in any closed-system energy account.
Taking an arbitrary pulse result as an irreversible decay rate would be wrong.
The bath has neither been initialized nor evolved by this benchmark.

## Source verification and limits

Barton Zwiebach, MIT 8.06 Spring 2018, [Chapter 4: Time Dependent Perturbation
Theory](https://ocw.mit.edu/courses/8-06-quantum-physics-iii-spring-2018/89ef6d5958ee59bae9a91345c3d8c8e4_MIT8_06S18ch4.pdf),
Eq. (4.3.20), PDF page 18, gives the squared finite-time amplitude. Equations
(4.3.34)-(4.3.37), PDF pages 21-22, state the continuum golden-rule limit
and its scale/weak-transition assumptions. Checked 2026-10-13 against the
official course PDF. The notation translation is Ef-Ei=epsilon-D and
rho|Vfi|^2=g sqrt(epsilon) exp(-epsilon/Lambda). The new integral and gradient
calculation above are derived here; the source does not establish this
carrier's existence or the applicability of a pulse to a thermal bath.
No novelty claim or broad literature search is made. No source PDF is copied
into this package.

## Research decision and reproducibility

Twenty checks pass: two symbolic identities, four input-temperature matches,
eight timescale/crossing checks and six independent kernel integrations.
This is a self-reviewed numerical and algebraic audit, not a Lean certificate
of non-equilibrium quantum field theory. Matching inputs and validating a
manifest do not establish physical truth.

The finite-width route remains open, but a stationary convolution is deferred
because it would omit a term already flagged by the time-gradient check.
The next substantive calculation is a time-dependent source/continuum model
with specified initial correlations, a threshold driven by the carrier moment,
and an explicit energy balance. Its fixed-threshold, weak-coupling limit must
recover the finite-pulse benchmark, and its slow-background limit must recover
the prior golden-rule source. Momentum dependence, the source bath and inverse
processes are subsequent required extensions; none can be certified by the
present rest-source benchmark. Independent material confinement and mediator
constraint routes remain unresolved and are not rescued by this calculation.

Reproduce from repository root:

    python3 sol61_push/threshold_memory_audit_2026_10_13/check.py /tmp/threshold_memory_results.json

The manifest pins all three prior result files used for this audit. The goal
remains open: a controlled production yield, admissible couplings, confinement
and a cold stored inventory have not been demonstrated.
