# Remove an accidental cancellation in the route toward condensation

2026-10-11. The preceding turn established a fast fixed-bath source reaction
clock but left momentum redistribution unresolved. This turn finds and removes
a concrete obstruction in the chosen interaction parameters. It does not
claim a condensate-growth simulation.

## The two-daughter process that can feed the condensate

Two daughters drawn from the initial production shell can scatter into one
at rest and one carrying their combined kinetic energy. This conserves charge,
energy and momentum; it does not require cooling through an external bath.
Use exact vacuum relativistic kinematics, with initial daughter energy E=M/2
and momentum magnitude p=sqrt(M²-4m²)/2. If the outgoing rest daughter has
energy m, the other daughter has energy M-m. The required angle theta between
the incoming momenta and the invariant squared energy s are

    cos(theta)=(M-2m)/(M+2m),
    s=2mM.

For the existing candidate cos(theta)=2.499875e-5: the incoming momenta are
nearly perpendicular. At nonrelativistic leading order this is the quartet
p_a+p_b -> 0+(p_a+p_b), with p_a.p_b=0. The energetic outgoing daughter keeps
the energy that the zero-momentum daughter loses.

A kinematically permitted zero-momentum output is not yet a finite condensate
growth rate. In a continuum the single point p=0 has zero measure for a smooth
uncondensed distribution; a kinetic treatment must handle a separate condensate
population or resolve its finite-volume formation and thermodynamic limit.
Bose stimulation, inverse processes and the finite incoming bandwidth matter.

## The original alpha=1 choice almost cancels this channel

The previously matched tree-level quartic is

    lambda_eff(s)=lambda_min [alpha-x/(1-x)],
    alpha=lambda_rep/lambda_min,
    x=(s-4m²)/(M²-4m²).

For the one-rest-daughter kinematics x=2m/(M+2m), giving

    lambda_eff/lambda_min = alpha-2m/M.

The old illustrative choice alpha=1 therefore has amplitude eta=1-2m/M,
only 4.999625e-5 in units of lambda_min. Its total two-body cross section at
this invariant energy relative to its threshold value is

    eta² (4m²/s) = 2.49950e-9.

This cross-section ratio characterizes scattering at the relevant invariant
energy, not an integrated probability of landing in the exact zero mode.
The suppression comes from destructive interference between contact repulsion
and virtual-source exchange, not from forbidden kinematics. The bare source
pole x=1 is not being used; this channel is near x=1/2.

The old production spectrum has finite radial width, so the exact-shell
suppression cannot be applied to every pair. A diagnostic average of normalized
amplitude squared using the saved daughter radial number fractions gives
1.99852e-6 for alpha=1, agreeing across the 512, 1024 and wider 1536 grids.
For general incoming energies the required invariant is s=2m(E_1+E_2); all
sampled radial pairs admit a physical incoming angle. The weights omit the
collision phase space, occupations per mode and stimulation factors. This
average is an amplitude diagnostic, not a rate.

## A concrete revised candidate: alpha=2

Keep m, M, g, initial source density, redshift and epsilon fixed, and change
only lambda_rep from lambda_min to 2 lambda_min. The total quartic becomes
3 lambda_min. Then the channel amplitude is 1.000049996 lambda_min rather
than 0.000049996 lambda_min. Its cross section relative to its OWN threshold
is 0.2500125. The threshold sigma/m increases from the illustrative 1 to
4 cm²/g; that change is explicit and has not been judged observationally.
A proxy using the old spectrum gives normalized squared amplitude 0.250029;
this is not a prediction for the revised spectrum or its transport.

This parameter is independently available in the positive-square potential;
alpha=1 was an example, not a requirement from the repo. The revised action
retains positive lambda_rep and the exact finite-regulator NR identity

    D=T+delta|b+c psi²/delta|²+(k-c²/delta) psi†² psi²,
    k=(lambda_min+lambda_rep)/(4m²),
    k-c²/delta=3.855449064e-13 eV^-2 > 0.

Thus the charge/excess-energy protection remains. The previously derived
pressure comparison also remains applicable; its upper multiplier changes
from 1.20710 to 1.11237 because c²/(delta k) decreases. This follows from the
same operator algebra; the finite-lattice spectra have not been rerun for
alpha=2. The initial source state has no daughter quartic energy, so its
initial excess energy is unchanged.

## Production survives the parameter change in the same approximation

`alpha2_bogoliubov.py` copies the existing positive-occupation Gaussian
production equations, changing lambda_rep to 2 lambda_min. It retains both
normal and anomalous quartic terms and uses a distinct script, contract and
output directory. Source depletion and the imposed expansion remain included.

| Modes | Band half-width | Relative tolerance | Daughter fraction at x=100 | At x=200 |
| --- | ---: | ---: | ---: | ---: |
| 512 | 2 | 1e-10 | 0.997683944865 | 0.999999637045 |
| 1024 | 2 | 1e-10 | 0.997683944865 | 0.999999637045 |
| 1536 | 3 | 1e-10 | 0.997683945057 | 0.999999637056 |
| 1024 | 2 | 1e-11 | 0.997683944869 | 0.999999637052 |

All 27 production checks pass. Maximum charge error is below 2e-11; maximum work error is below
8.3e-13. x=200 remains about 6.80e-9 seconds. The many digits document finite
surrogate convergence; they do not imply a precise relic abundance. Moving
sources, non-Gaussian scattering and actual condensation remain excluded.
The near-complete conversion here is into the produced momentum band, NOT
into a zero-momentum condensate.

`condensate_channel.py` separately passes eight kinematic, amplitude and
positivity checks. Both run manifests validate current inputs and outputs.
No original candidate files or concurrent campaign files were changed.

## Research consequence

Alpha=2 is a better candidate for the next full kinetic calculation because
it removes a demonstrable interference suppression in a relevant momentum-
redistribution channel without spoiling the tested source conversion or
positive-energy structure. It is not selected uniquely: other alpha values
away from approximately one can also remove the suppression, and their rates
and phenomenology differ.

The ideal Bose endpoint depends on masses, charge and energy, which are
unchanged to leading ideal-gas order; its percentages are still conditional,
not a demonstrated outcome of alpha=2 evolution. The next calculation must
include the revised energy-dependent scattering kernel, condensate formation,
inverse transfer and moving-source reactions without double-counting a source
resonance as both elastic exchange and real conversion. Halo formation,
acceleration normalization and the origin of the initial charge remain open.
