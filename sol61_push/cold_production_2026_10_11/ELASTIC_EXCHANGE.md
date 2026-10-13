# Elastic collisions supply signed exchange, but do not select the halo

2026-10-11. Continuation of [the receiver bridge](CLAUDE_RECEIVER_BRIDGE.md).
The preceding goal turn delivered the existing candidate to the user but
added no evidence. This turn derives and checks the next available transfer
mechanism. The protected carrier remains a conditional construction; this
calculation does not complete its halo formation theory.

## A collision-derived law

Consider two tagged populations of the same mass m, with number densities
n_a,n_b, zero mean velocity and locally Maxwellian one-dimensional velocity
variances s_a,s_b. Tags identify the incoming populations, not two new species.
Assume dilute classical elastic scattering, isotropic in the centre of mass,
with total cross section sigma(w), w=|v_a-v_b|. A future application must check
this dilute kinetic description for the actual carrier state.

Let V=(v_a+v_b)/2 and w_vec=v_a-v_b. Isotropy gives

    <Delta E_a>_outgoing = -m V.w_vec/2 = m(v_b²-v_a²)/4.

For independent incoming Maxwellians, S=s_a+s_b and the Gaussian conditional
mean is E[V | w_vec]=(s_a-s_b)w_vec/(2S). Multiplying by the collision rate
n_a n_b sigma(w)w gives the instantaneous energy transfer per volume:

    Q_a = n_a n_b m(s_b-s_a) <sigma(w) w³> / (4S),
    Q_b = -Q_a,
    ds_a/dt = n_b(s_b-s_a)<sigma(w)w³>/(6S).

Thus the sign is supplied by the incoming distributions, and the combined
energy is conserved. No desired halo temperature occurs in the collision law.
The variance equation is an exact instantaneous moment for these incoming
Maxwellians. Assuming they remain Maxwellian throughout an evolution would
be an additional closure, which has not been justified here.

For constant sigma, <w³>=8 sqrt(2/pi) S^(3/2), hence

    ds_a/dt = (4/3) sqrt(2/pi) n_b sigma sqrt(S) (s_b-s_a).

The fixed-bath instantaneous relaxation coefficient equals two thirds of
n_b sigma <w>. Bulk relative motion adds another energy reservoir and is
excluded from this calculation. An anisotropic differential cross section
requires its appropriate angular moment rather than blindly using total sigma.

## What this changes about the benchmark interpretation

CFG544's `make_ic` assigns BOTH B and C components Gaussian velocities with
standard deviation 0.05 in its code units. B has a uniform-volume spatial
sample; C samples the target enclosed-mass distribution. Their opposite
signed total-energy discrepancies do not mean they initially have opposite
kinetic temperature discrepancies. At the same position, the same prescribed
bath would initially drive their equal velocity distributions in the same
direction. B can heat during gravitational contraction, but that requires
following the motion and potential; the energy bound does not supply that
history.

Also, two tagged populations exchanging heat locally do not inject energy
into the combined local carrier: Q_a+Q_b=0. To use an exterior reservoir,
particles must stream through the boundary or otherwise transport energy.
For a static prescribed gravitational potential Phi, the kinetic equation
with this elastic collision operator implies

    d/dt integral_volume e dV = -integral_boundary F_E . dA,
    e = integral m(v²/2+Phi) f d³v,
    F_E = integral m(v²/2+Phi) v f d³v.

Mass flux must be tracked alongside energy flux. In a time-dependent
potential the particle energy equation also contains rho*dPhi/dt; a live
self-gravitating calculation must include gravitational energy consistently.
A local relaxation rule toward the target cannot substitute for these fluxes.

## Finite reservoir screen

In a spatially homogeneous isolated mixing model without gravitational work,
let mu=M_bath/M_target. Conservation of kinetic energy gives the common
variance at equilibration:

    s_final=(s_initial+mu*s_bath)/(1+mu).

For IC-C, set s_initial/Vf²=0.0025 and use the inherited LOWER target kinetic
energy bound to obtain s_target/Vf²=(2/3)K_lower/(M Vf²). If, illustratively,
s_bath/Vf²=0.5, the minimum bath/target mass ratios for reaching at least this
lower temperature are:

| Cell | Required mass ratio |
| --- | ---: |
| MW canonical / alternative | 1.9980 / 1.9858 |
| Cluster canonical / alternative | 5.8885 / 5.8889 |
| Compact canonical / alternative | 2.1436 / 2.1372 |

These are conditional homogeneous mixing capacities, not halo mass predictions
or universal lower bounds in a gravitational system. The bath temperature
is stipulated. Its existence and accessible mass have not been established.
A global mass ratio is not a local overlapping density ratio.

## Rate and transport screen

Using the candidate's illustrative threshold sigma/m=1 cm²/g as a CONSTANT
cross-section surrogate, and both local dispersions 200 km/s:

| Local bath density (kg/m³) | Fixed-bath relaxation time | Mean free path |
| --- | ---: | ---: |
| 1e-21 | 1.053 Gyr | 324 kpc |
| 1e-23 | 105.31 Gyr | 32,408 kpc |

The optical depths across 100 kpc are 0.309 and 0.00309. Even this favorable
constant-cross-section estimate does not justify a short-mean-free-path fluid
closure on that scale. The actual energy-dependent carrier cross section,
resonant tails, spatial overlap and orbit dwell times remain to be included.
These densities and temperatures are reference inputs, not measured values
or outputs of the production model. The table is not an exclusion of elastic
transport, and no observational constraint is inferred from it.

## Evidence and next discriminating calculation

`elastic_exchange.py` independently integrates incoming speeds and their
relative angle with 64- and 96-point Gauss-Legendre rules per coordinate,
cutting each speed at ten of its own dispersions. Four variance pairs test
heating, cooling, equilibrium and a large temperature contrast. The code also
checks weighted energy conservation for unequal populations and six capacity
inversions. All 18 finite checks pass. The run manifest validates input/output
provenance; it does not validate a halo solution or the kinetic approximation.
No bare resonance pole is integrated.

The next useful calculation is transport with gravity and an explicitly
populated exterior region, recording both mass and energy crossing the target
boundary. Its collision step should conserve energy and momentum and use the
carrier's differential cross section. It must test whether the supplied initial
reservoir reaches the current nu_mono target without putting that target into
the collision operator. The present result supplies a derived signed moment
and exposes why a uniform-bath temperature relaxation alone cannot close the
repo's formation claim.
