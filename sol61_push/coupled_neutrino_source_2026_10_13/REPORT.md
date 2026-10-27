# Coupled neutrino heating with an equilibrium source

2026-10-13. This replaces the arbitrary instantaneous-decoupling step of
../source_thermalization_2026_10_13/REPORT.md with an actual two-temperature
initial-value calculation. It remains a restricted source-only cosmology, not
the full carrier-production model and not a new observational likelihood.

## Equations and source conventions

Use electromagnetic temperature Tg and one common neutrino temperature Tn.
Photons, electrons/positrons and optionally a real scalar R of mass 2 MeV are
in thermal equilibrium at Tg with zero chemical potentials. Neutrinos have
Fermi-Dirac energy density rho_nu=7pi^2*Tn^4/40 (three species including their
antiparticles). Include the exact massive equilibrium electron and scalar
thermodynamic integrals, but neglect finite-temperature QED corrections.

The Maxwell-Boltzmann weak energy-transfer kernel is taken from
[Escudero, arXiv:1812.05605v4](https://arxiv.org/pdf/1812.05605v4),
6 September 2019, Eqs. (2.12)–(2.13). Setting all neutrino temperatures equal
cancels the neutrino-flavor exchange terms and gives

    Q = GF^2/pi^5 * (3-4sw^2+24sw^4) * F(Tg,Tn),
    F(a,b)=32(a^9-b^9)+56*a^4*b^4*(a-b).

Use the paper's GF=1.1664e-5 GeV^-2 and sw^2=0.223. Q is positive for heat
flow into neutrinos. Thermodynamics retains Bose/Fermi statistics; only the
collision kernel uses the MB approximation. This distinction matters.

Let rho_em and p_em include R when enabled. The evolution equations are

    dTg/dt = -[3H(rho_em+p_em)+Q]/(d rho_em/dTg),
    dTn/dt = -H*Tn+Q/(4rho_nu/Tn),
    H^2 = 8pi*(rho_em+rho_nu)/(3 M_Pl^2).

The code evolves logarithms of temperatures against log scale factor. Their
sum satisfies total energy conservation: the same Q leaves one sector and
enters the other. Thermodynamic heat capacities are integrated directly and
checked against finite differences of energy density.

Start Tg=Tn=10 MeV, integrate to Tg=0.01 MeV, and repeat starting at 5 MeV.
The source is assumed in electromagnetic equilibrium throughout, supported
as a rate diagnostic near a few MeV by the preceding calculation. The current
ODE does not independently evolve its abundance. Carrier particles phi,
their inverse reactions, and their energy density are omitted explicitly.

## Results and comparison with the simpler estimate

| Calculation | Final Neff |
|---|---:|
| No R, coupled weak heating | 3.042372 |
| Equilibrium 2 MeV R, coupled weak heating | 2.534247 |
| No R, weak exchange switched off at 2 MeV | 3.018044 |
| Equilibrium R, weak exchange switched off at 2 MeV | 2.482795 |

Neff=3*(11/4)^(4/3)*(Tn/Tg)^4 in this thermal-distribution model.
The no-R result reproduces the published MB/no-QED benchmark 3.042 in the
paper's Table 1. With weak exchange switched off, both trajectories recover
the independent entropy-conservation formulas used previously.

The equilibrium-source shift relative to the matching baseline is -0.508125.
Continuing weak interactions raise the R-only result by about 0.05145 relative
to an abrupt 2 MeV decoupling assumption. They do not erase the entropy effect
within this model. Quoted extra digits document numerical comparisons; they
are not precision claims about nature.

## Numerical evidence

The refined run uses 320-point Gauss-Legendre thermodynamic integrals and Radau
relative tolerance 2e-9. Compared with 160 points and tolerance 1e-7, the final
Neff changes by 6.6e-9 without R and 9.4e-8 with R. Changing the initial common
temperature from 10 to 5 MeV changes the respective results by less than 1.2e-8.
Momentum integrals run to p/T=80.

Twenty-seven checks pass: four heat-capacity comparisons; successful event
termination and algebraic energy balance for eight ODE runs; two refinement
comparisons; two starting-temperature comparisons; two entropy-limit checks;
and reproduction of the published baseline. The energy residual samples test
that the implemented sector equations cancel their transfer terms; they are
not an independent global-conservation proof for the numerical trajectory.
The entropy-limit and published-baseline tests supply independent checks.
The run manifest validates the saved inputs and results.

## Physical interpretation and remaining gap

Under the assumed standard hot radiation era, an electromagnetically equilibrated
source alone changes neutrino heating substantially. This strengthens the reason
to investigate cosmology before treating the laboratory source as admissible.
It does not import a thermal-dark-matter exclusion into an unstable-source model.

The missing carrier sector is consequential. The same R used here can feed phi
and anti-phi, and their nonequilibrium population can change expansion and energy
exchange. Equilibrium of R with photons/electrons does not by itself establish
kinetic or chemical equilibrium of those carriers. Their cosmological production
cannot be evaluated using a vacuum 'cold daughter' label: moving parents, inverse
processes and thermal mass shifts change that conclusion. A coupled momentum or
justified moment treatment is required before computing a full-model Neff or
relic abundance.

Also omitted are finite-temperature QED, quantum-statistical collision factors,
neutrino spectral distortions and separate flavor temperatures. The successful
3.042 baseline is the specified approximation, not the most accurate Standard
Model prediction. There is no claim that a different gravitational completion,
reheating history or initial condition has been ruled out. Such alternatives
must be explicitly supplied and tested rather than assumed to rescue a point.

This is progress on a real constraint of the manufacturing candidate. No viable
creation-and-storage protocol, empirical detection or UFO propulsion mechanism
has been established. No new Lean certification of these numerical kinetics is
claimed.

Reproduce:

    python3 sol61_push/coupled_neutrino_source_2026_10_13/check.py /tmp/coupled_neutrino_source_results.json
