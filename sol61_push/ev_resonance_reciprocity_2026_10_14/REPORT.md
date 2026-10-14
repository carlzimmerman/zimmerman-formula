# The optical branch also creates a low-velocity scattering resonance

2026-10-14. Parent checkpoint: 0bd316514d4852f59f6b85d6fe4c6e8b84bf64b7.

The eV optical branch cannot independently choose a rapid source decay and
negligible opposite-charge carrier interactions. Its same cubic interaction
produces an elastic resonance at relative speed 26.8 km/s. This is a vacuum
scattering result within the stipulated model. A classical halo diagnostic gives
very large rates, but its high occupation and long resonance delay invalidate
using those numbers as an observational exclusion. The optical source remains
conditional, and neither earlier quartic example is empirically admitted.

## Fixed model and channel conventions

Retain the assigned m=1 eV, M_R=2m+delta, delta=2e-9 eV and

    L_int = -lambda |phi|^4 - mu R |phi|^2,
    mu^2 = lambda M_R^2.

The second equation is the prior illustrative choice, not a symmetry or data
requirement. The separate photon coupling g=1e-20/eV gives a negligible photon
width compared with the two carrier widths tested here. R decays into phi and
anti-phi. Same-sign carriers cannot annihilate into this neutral s-channel R.

With the stated potential normalization, the tree amplitudes are

    M(phi phi -> phi phi) = -4lambda
              -mu^2[1/(t-M_R^2)+1/(u-M_R^2)],
    M(phi anti-phi -> phi anti-phi) = -4lambda
              -mu^2/(t-M_R^2)
              -mu^2/(s-M_R^2+i M_R Gamma_R).

The width resummation is needed near the pole; writing the tree propagator
without it would spuriously diverge. The displayed background and resonance
can interfere. The rate calculations below isolate the dominant pole near
resonance, rather than treating a sum of cross sections as an exact identity.
They do not compute the full off-pole angular interference integral.

At zero incoming momentum, the same-sign amplitude is -2lambda for the chosen
mu. The identical-final-state factor yields

    sigma_same = lambda^2/(32pi m^2).

For the unlike-sign s-channel pole, particles are distinguishable. The leading
nonrelativistic relative speed v obeys s=4m^2+m^2 v^2. Define

    v_R = 2sqrt(delta/m) = 8.94427e-5,
    Gamma_R = mu^2 v_R/(64pi m),
    epsilon_width = 2 Gamma_R/m.

Near the pole, treating the width as constant at its on-shell value,

    sigma_pole(v) = mu^4/(64pi m^6)
                   /[(v^2-v_R^2)^2+epsilon_width^2].

Corrections from the energy-dependent width, relativistic kinematics and
background diagrams are not included in that expression. At the pole it gives

    sigma_pole(v_R)=16pi/(m^2 v_R^2)=4pi/p_R^2,
    p_R=m v_R/2.

This is the distinguishable elastic s-wave unitarity value when the elastic
branching fraction is one. A real, small background does not cancel the
resonance's imaginary amplitude at its center. Reducing mu decreases its width
and integrated weight; it does not decrease this ideal on-pole height.

## External cross-check and scope

Chu, Garcia-Cely and Murayama, *Velocity Dependence from Resonant Self-Interacting
Dark Matter*, [arXiv:1810.04709v2](https://arxiv.org/pdf/1810.04709v2),
24 February 2019, published in PRL 122, 071103, was checked on 2026-10-14.
Their Eqs. (1)-(3) give a Maxwell relative-speed average, a Breit-Wigner form,
and collision energy m v^2/4. Those support the resonance/velocity conventions.
Our sigma variable below is a one-particle one-dimensional dispersion; their
relative-distribution parameter is 2sigma. Their fitted masses and empirical
curves are not transferred to this eV branch. Their text also qualifies the
inference of cross sections from halo observations.

## Conditional velocity average with the pole resolved

As an explicit diagnostic only, assign each sign a Maxwell distribution with
one-dimensional dispersion sigma=30 km/s. The relative-speed density and mean are

    f(v)=v^2 exp[-v^2/(4sigma^2)]/(2sqrt(pi) sigma^3),
    <v>=4sigma/sqrt(pi).

For a narrow isolated pole, integrating rather than sampling a velocity bin gives

    <sigma_pole v> approximately pi mu^2 f(v_R)/(4m^4 v_R).

This average scales as mu^2, hence as lambda in the chosen family, rather than
as lambda^2. A naive coarse velocity grid can miss the narrow peak completely.
The numerical check uses v^2=v_R^2+epsilon_width tan(z), which cancels the
Lorentzian denominator against the integration Jacobian. Windows of 10 and 100
half-widths reproduce their corresponding narrow-width integrals within 2e-5.
This verifies the constant-width pole model in the stated windows; it is not
a full calculation of every scattering channel or thermal spectral function.

Define sigma_eff=<sigma v>/<v> solely to display this diagnostic. Restoring SI:

| lambda | Rest lifetime | Same-sign threshold sigma/m (m^2/kg) | Conditional unlike-sign sigma_eff/m (m^2/kg) |
|---|---:|---:|---:|
| 1e-6 | 0.370 ms | 2.17e8 | 6.27e27 |
| 1e-15 | 4.28 days | 2.17e-10 | 6.27e18 |

Both cases have vacuum peak cross section 2.4465e-4 m^2. The large difference
between the same-sign and unlike-sign columns is why a contact-only scattering
check would miss the main reciprocity issue for a source creating both signs.
These are not measured cross sections. No observational exclusion is inferred
by comparing the table with a universal numerical cross-section limit.

## The classical interpretation fails its own admission checks

Assign total mass density 0.3 GeV/cm^3, split equally between signs. This is a
reference density, not a measurement of the hypothetical field. For a Gaussian
momentum distribution, the nominal phase-space occupation at p=0 per sign is

    f_phase(0)=(2pi)^(3/2) n_sign/(m sigma)^3 = 1.81e7,

with number density converted to natural units. Classical dilute statistics
are not justified by these assigned inputs. The actual state could be coherent,
nonthermal or correlated; none is supplied by the Maxwell diagnostic.

There is a second warning. The nominal classical collision rate is
n_opposite <sigma v>. Multiplying it by the mediator rest lifetime gives

    nominal_collision_rate * lifetime = 4.20e7

for BOTH coupling choices. The coupling cancels because the pole's integrated
weight is proportional to mu^2 and its lifetime to 1/mu^2. This is a diagnostic
against instantaneous independent elastic events with the same fixed population:
it does not prove that the real medium undergoes 4.20e7 overlapping classical
collisions. One must track resonant population, reversibility, memory and
quantum occupation rather than infer rapid thermalization from that rate.
The lifetime is a characteristic resonance delay scale, not an exact wavepacket
Wigner-delay calculation.

Consequently, solving the classical average for an extremely small coupling and
calling that an astrophysical upper bound would compound an unadmitted kinetic
approximation. We do not perform that extrapolation. A realistic all-dark-matter
interpretation requires a quantum kinetic or field calculation and appropriate
observations. A very dilute laboratory product stream is a different state;
this halo diagnostic does not show that the computed optical emission vanishes.

## Research consequence

The finite optical production calculation remains a conditional vacuum source
estimate. This audit adds a required interaction to any storage/halo extension:
phi+anti-phi can form the same long-lived R that the source creates. A fast-decay
choice increases its integrated interaction strength, while a weak-decay choice
sends mediators far outside the apparatus. Neither choice alone is a capture
protocol or a cosmological admission certificate.

A single-sign preexisting halo could suppress this opposite-sign channel, but
our optical preparation produces both signs and supplies no separation process.
An added decay channel, mass spectrum change, or charge-separation interaction
would define an additional model and must be accounted for explicitly.

The next useful calculation is a finite-density, finite-time conversion model
for phi+anti-phi <-> R with the source's actual distributions, checking whether
resonance storage or coherent exchange suppresses the naive irreversible rate.
For laboratory capture, an external force or energy-loss mechanism is still
separately necessary. The overall objective remains unresolved.

## Evidence

Eleven bounded checks cover relative-speed normalization and mean, vacuum peak
unitarity, four resolved pole windows, coupling cancellation in the rate-delay
product, and two same-sign threshold identities. Inputs, commands and results
are recorded in run/manifest.json. This is self-review of an explicitly
conditional model. No new Lean proof of scattering or quantum kinetics is
claimed; the earlier polynomial stability proof has narrower scope.

Reproduce:

    python3 sol61_push/ev_resonance_reciprocity_2026_10_14/check.py /tmp/ev_reciprocity_results.json
