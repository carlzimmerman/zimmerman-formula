# The rest-source reaction is fast; condensation is a different timescale

2026-10-11. Follow-up to [the conditional Bose endpoint](BOSE_ENDPOINT.md).
The previous turn made progress by finding a self-consistent condensed ideal
equilibrium. This turn tests one necessary kinetic condition without assuming
that a fast reaction is sufficient to establish the entire equilibrium.

## Gain minus loss, rather than enhanced decay alone

Hold an isotropic daughter Bose bath fixed at temperature T, with chemical
potential zero relative to the daughter rest mass. A source at rest decays
to two daughters with opposite momenta and kinetic energy delta/2 each,
where delta=M-2m. Let f=1/[exp(delta/(2T))-1] be their occupation and B the
source zero-momentum occupation. In a weak-coupling, incoherent, on-shell
rate approximation, using the recorded vacuum source width Gamma_0:

    dB/dt = Gamma_0 [(1+B)f² - B(1+f)²]
          = Gamma_0 [f² - (1+2f)B].

The normalization and identical-final-particle factors are already included
in the inherited vacuum decay width. The stationary occupation is

    B_eq = f²/(1+2f) = 1/[exp(delta/T)-1].

A source occupation perturbation with the bath HELD FIXED relaxes at
Gamma_rel=Gamma_0(1+2f). Gross stimulated decay instead has enhancement
(1+f)². Using the latter as the net relaxation rate would omit inverse
reactions and give a different result. This equation is not a closed
energy-conserving evolution of source and daughter populations: the bath
must evolve in the full problem.

## Numerical clock on the conditional equilibrium trajectory

The inherited vacuum lifetime is 0.00148016122 s. Use the endpoint temperatures
and expansion ratios already calculated, with the previously declared
radiation+matter+vacuum background and initial redshift 1e6. No observed or
newly fitted cosmological parameters are introduced here.

| Expansion ratio | T (eV) | Net Bose enhancement | Rest-source relaxation time (s) | Gamma_rel/H |
| --- | ---: | ---: | ---: | ---: |
| 1 | 0.674711 | 139.463 | 1.0613e-5 | 4.4487e12 |
| 2 | 0.175302 | 36.2435 | 4.0839e-5 | 4.6180e12 |
| 10 | 0.0114780 | 2.51133 | 5.8939e-4 | 7.9114e12 |
| 100 | 1.62662e-4 | effectively 1 | 1.4802e-3 | 2.8215e14 |
| 1000 | 1.62662e-6 | effectively 1 | 1.4802e-3 | 1.6349e16 |
| 1e6 | 1.62662e-12 | effectively 1 | 1.4802e-3 | 3.1447e20 |

At the first point f=69.2315. Gross decay enhancement would be 4932.47,
whereas net relaxation enhancement is only 139.463. The inferred in-medium
relaxation width hbar Gamma_rel/delta is 3.20e-9 initially and smaller later,
so this particular width estimate is narrow compared with the mass gap.
This is a consistency check, not a full spectral-function calculation.

At late times the source equilibrium occupation and its inverse-production
flux are exponentially tiny. Fast decay of an added source does NOT imply
rapid redistribution of the daughter gas. Values stored as zero at very
large delta/T are floating-point underflow, not exact mathematical zeros.

## Why this does not yet certify condensate formation

Rest-source conversion exchanges population with a finite-momentum daughter
shell. It does not directly populate the zero-momentum daughter condensate:
a source at rest cannot release positive delta into two daughters at rest.
If these shell reactions were the only processes, occupations outside the
shell would remain untouched. This supplies an explicit reason that a huge
Gamma_rel/H cannot certify global thermalization or Bose condensation.

Moving sources, elastic redistribution and condensate-assisted processes can
connect additional momenta. Their coupled kinetic evolution must conserve
energy and charge, include Bose factors, and permit the condensate to grow
rather than assigning it its equilibrium population. Coherent production and
mode mixing may require field dynamics before an incoherent kinetic stage is
valid. The present reaction clock does not cover those stages or average over
moving sources, and does not test their equilibration rate.

## Evidence and next calculation

`bose_reaction_clock.py` reads the recorded endpoint, source width and
background. Twelve finite checks verify the detailed-balance identity and
the linearized gain-loss rate at the six sampled temperatures. The run
manifest validates inputs and outputs. These algebraic checks do not validate
the rate approximation itself.

The result removes slow rest-source conversion relative to expansion as an
obvious obstruction along the ASSUMED endpoint trajectory. It does not remove
the missing momentum-redistribution and condensate-growth calculation. That
calculation, rather than further enhancement of this already-fast reaction,
is the next discriminating step for the proposed production route. Halo
formation and the target acceleration normalization remain separate gaps.
