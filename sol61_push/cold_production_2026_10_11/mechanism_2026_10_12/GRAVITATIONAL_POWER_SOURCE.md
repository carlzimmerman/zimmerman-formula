# A physical power source: feedback-driven gravitational work

12 October 2026. Continuation of STABLE_SCREENING_AND_SUPPLY.md. This identifies and tests a known transfer channel, not the complete missing halo selector. It changes the route: no hypothetical dark-radiation absorption vertex is needed for this channel.

## Mechanism and provenance

Stars release energy and momentum; gas moves rapidly; the baryonic gravitational potential changes; cold particles gain orbital energy through gravitational work. This is the feedback-driven potential-fluctuation mechanism studied by [Pontzen and Governato, arXiv:1106.0499](https://arxiv.org/pdf/1106.0499), especially the analytical orbital treatment. Their work connects burst-driven potential fluctuations with core formation. It does not identify our scalar particles, derive our vacuum normalization, or establish our repaired kernel. This is reuse of a published physical mechanism, not a novelty claim.

The current carrier already couples gravitationally. Its low elastic scattering rate therefore does not prevent this transfer channel. The earlier simulations held baryons fixed and could not test it. Heating may expand a central distribution; whether that helps the particular target depends on the starting profile and must be scored after evolution.

## Exact energy bookkeeping

For a particle in an externally specified baryon potential and fixed background potential,

    H=p²/(2m)+m Phi_b(x,t)+m Phi_fixed(x),
    dH/dt=m partial_t Phi_b(x,t).

For self-gravitating cold particles with cold self-energy counted once, the corresponding total identity is

    dE_c/dt = integral rho_c(x,t) partial_t Phi_b(x,t) d³x,

where E_c includes cold kinetic energy, half the cold self-potential term, and the cold–baryon interaction potential. Consistent boundary conditions and flux terms are required for an open domain. The baryon/feedback driver supplies the work. Prescribing Phi_b is not equivalent to deriving an energetically affordable gas history.

A global added time-dependent potential constant changes the reference energy; physical orbital heating must be compared after the potential returns to the same profile and normalization. The test below does exactly that. In a closed gas+carrier calculation, the work must appear with the corresponding opposite exchange and feedback injection in the total energy balance.

## Controlled calculation completed

Use a unit-mass harmonic Hamiltonian H=(p²+omega²(t)q²)/2 with initial omega=1 and a phase-uniform ensemble with <q²>=<p²>=1, <qp>=0, hence initial mean energy one. Reduce omega² by fraction f rapidly and return it slowly to one. A harmonic well is a local model of a roughly uniform-density core, not a complete halo.

An instantaneous drop gives mean energy 1-f/2 in the shallower potential. Adiabatic return conserves E/omega for each orbit, so

    <E_final>/<E_initial> = (1-f/2)/sqrt(1-f)
                              = 1+f²/8+O(f³).

This is greater than one for 0<f<1. Hamiltonian evolution itself remains reversible; the average uses initial phase sampling and a specified timing history. A time-reversed, specially correlated ensemble can undo the transfer. Independent cycles cannot simply be multiplied unless their phase statistics are justified.

Numerically evolve the covariance equations

    d<q²>/dt=2<qp>,
    d<qp>/dt=<p²>-omega²<q²>,
    d<p²>/dt=-2omega²<qp>,
    dW/dt=(partial_t omega²)<q²>/2.

The driver uses cosine ramps: rapid removal duration 0.001 and slow return duration 200 in initial inverse-frequency units. The control uses duration 200 for both ramps.

| Fractional drop in omega² | Rapid-out/slow-return energy gain | Slow-out/slow-return energy gain |
|---:|---:|---:|
| 0.1 | 0.13881% | about 3e-11% |
| 0.3 | 1.59453% | about 1e-9% |
| 0.5 | 6.06709% | about 1e-8% |

All 12 checks pass: energy equals initial energy plus driver work; the rapid/slow result approaches the analytic limit; slow cycling is nearly reversible; Hamiltonian phase-space area is conserved. The maximum energy/work discrepancy across these cases is below 1e-10 in initial-energy units. These are finite orbit-transfer tests, not a galaxy simulation or new observations.

## Can stellar physics provide the acceleration scale?

[Grudic et al., arXiv:1910.06345](https://arxiv.org/pdf/1910.06345), equations 1–5, propose that young-star momentum injection sets a critical acceleration. Feedback competes with gas weight, giving M_young/M_expelled approximately g_tot/g_crit. Their low-acceleration scaling leads conditionally to g_tot² approximately g_b g_crit(1-f_g)/f_bar_initial. Here the gas fractions and formation history matter. This is a distinct stellar-feedback explanation, not a derivation of a0 from vacuum energy. Their illustrative young-population momentum rate must not be applied to all baryons or all old stars.

The source of mechanical power has the right general form, force times gas velocity:

    L_drive <= approximately dot(p)_feedback v_gas,
    dot(p)_feedback = a_feedback M_young,
    L_c = eta_transfer L_drive.

The efficiency and inequality depend on geometry and channels; supernova thermal energy can require a separate energy budget. Matching the earlier hypothetical L_c=C a0 v M_b requires, schematically,

    eta_transfer a_feedback (M_young/M_b)(v_gas/v) = C a0.

The left side now refers to physical stellar and gas quantities, but its universality has not been derived. In particular, old and gas-dominated galaxies cannot be assigned a permanent young-star source. They could retain a fossil halo from earlier episodes, which requires formation-history modelling. This is why a working energy-transfer channel is not yet the universal selector.

## Decision and exact next test

The strongest result is that ordinary time-dependent gravity can transfer feedback energy to the proposed cold carrier while preserving its particle charge. This bypasses the need to invent a density-dependent microscopic baryon coupling just to obtain energy exchange. It does not validate the optional dark bath or make its emissivity formula derived.

Before a full halo claim, replace fixed baryons in the forward formation calculation with a gas evolution whose outflow/return work is bounded by its specified stellar feedback budget. Run rapid and adiabatic histories with equal initial/final baryon profiles, compare the resulting profiles without a target force, and test dependence on burst timing and initial halo energy. A gas history tuned to the desired profile is not evidence of an attractor. Independently test whether the resulting normalization depends on star-formation/gas fractions instead of the asserted vacuum density.

The mechanism remains incomplete at precisely that step: physically allowed feedback histories have not been shown to select rho_c,target or kappa=1/2. Scripts and recorded numerical evidence are gravity_pump.py, gravity_pump_contract.json and gravity_pump_run/. No prior unfavorable halo result is overwritten.
