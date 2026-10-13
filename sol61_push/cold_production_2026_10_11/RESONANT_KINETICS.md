# The source resonance supplies a possible kinetic channel

Status: a conditional local kinetic estimate shows that Bose stimulation can
make the source channel relevant on galactic timescales in a stipulated
high-occupation bath. It is not a heat-conduction, halo-settling, condensation
or profile-selection calculation. The microscopic parameters are unchanged
from the repulsive production example.

## Collision operator and conserved quantities

Use the late charged action, with interaction g(chi* phi^2+chi phi*^2).
The positive-charge reaction is chi <-> phi+phi. Let F(P) be source occupation
and f(p) daughter occupation. With dPi=d^3p/[(2pi)^3 2E], the on-shell source
collision term is

    dF(P)/dt = [1/(2 Echi)] [1/2!] integral dPi1 dPi2
              (2pi)^4 delta^4(P-p1-p2) |2g|^2 J,
    J = f1 f2 (1+F) - F(1+f1)(1+f2)
      = f1 f2 - F(1+f1+f2).

The daughter equation counts the two daughters correspondingly. Each forward
reaction changes (Nphi,Nchi) by (-2,+1), conserving Q=Nphi+2Nchi. The four-
momentum delta function conserves energy and momentum. Bose statistics cancel
the cubic occupation terms; retaining an unbalanced f^3 contribution would
produce an incorrect rate.

For a=f1 f2(1+F) and b=F(1+f1)(1+f2), the collision contribution to Bose
entropy is proportional to (a-b) log(a/b)>=0. Bose distributions at a common
temperature have detailed balance when mu_chi=2 mu_phi. Temperature and total
charge remain state variables; this condition does not select the repo's
halo normalization or acceleration scale.

These equations assume weak coupling, incoherent quasiparticles, on-shell
kinematics and factorized occupations. They are not valid replacements for
the earlier coherent pair-production equations merely because occupations
are large. Anomalous correlations and coherent source amplitudes require
additional evolution. Whether a formed halo enters this kinetic regime
is not established here.

## A rest-source mode in a fixed isotropic bath

For P=0, both outgoing momenta have magnitude p*=m u, with
M=2m sqrt(1+u^2). The identical-particle decay width is

    Gamma0 = g^2 sqrt(1-4m^2/M^2)/(8 pi M).

The normalization uses the two-body phase-space expression and identical-
particle factor in [PDG 2025 Kinematics, equations 49.11–49.18](https://pdg.lbl.gov/2025/reviews/rpp2025-rev-kinematics.pdf).
The vertex |2g| and its application to this model are derived from the stated
interaction, not supplied by PDG.

If the two daughter occupations on this shell are both f*, held fixed, then

    Fdot = Gamma0 [f*^2-(1+2f*)F],
    Feq = f*^2/(1+2f*),
    tau_mode = hbar/[Gamma0(1+2f*)].

Thus a highly occupied bath enhances the linear relaxation rate by 1+2f*,
not f*^2. The inverse-production term still contains f*^2. This is one
rest-source occupation's relaxation time in a bath, not a conversion time
for the entire halo. The P=0 mode alone has zero measure in a continuum
density integral; moving source modes and bath backreaction must be included
before predicting any macroscopic transfer rate.

## Illustrative numbers with the existing coupling

Choose an isotropic Gaussian momentum occupation, not a claimed thermal
Bose-equilibrium distribution:

    f(p) = (2pi)^(3/2) n/(m sigma)^3 exp[-p^2/(2m^2 sigma^2)],
    n = integral d^3p f(p)/(2pi)^3 = rho_phi/m,
    sigma = one-dimensional velocity dispersion / c.

The assumed rho_phi is the daughter mass density. It is not a measured halo
density or a predicted fraction of total dark matter. With m=1e-12 eV,
u=0.001 and g=9.0744734568e-47 eV, Gamma0=1.63822e-85 eV, corresponding to
a vacuum lifetime about 1.27318e62 years. For rho_phi=1e-21 kg/m^3:

| One-dimensional dispersion | Resonant daughter occupation f* | Fixed-bath source-mode relaxation time |
|---|---:|---:|
| 50 km/s | 2.28467e47 | 278635 Gyr |
| 100 km/s | 2.04456e52 | 3.114 Gyr |
| 200 km/s | 7.43407e52 | 0.856 Gyr |
| 300 km/s | 4.11161e52 | 1.548 Gyr |
| 1000 km/s | 1.74866e51 | 36.40 Gyr |

At fixed density, f* is maximal at sigma=u/sqrt(3), approximately
173.1 km/s. This preferred velocity comes from the chosen mass splitting,
not a derived relation to baryonic mass or vacuum density. At large
occupation the time scales inversely with daughter density. The script also
evaluates densities 1e-23 and 1e-19 kg/m^3 without treating them as observations.

For these samples the rate is much smaller than m sigma^2/hbar. That
separation supports one necessary weak-kinetic ordering, but does not verify
random phases, spatial locality, bath stationarity or a transport closure.
The gas can deplete and redistribute; the fixed-bath solution cannot be
extrapolated to arbitrarily long times as a conserved full-system evolution.

## Consequence for the formation program

The tiny threshold elastic cross section is insufficient to declare the
produced field dynamically inert. The retained source resonance offers a
specific channel worth integrating over momentum, with both species evolved
and charge/energy conserved. Conversely, a single mode's Gyr relaxation time
does not demonstrate outward heat current, halo contraction, or a universal
profile. The required next calculation is coupled momentum redistribution,
not insertion of tau_mode as a phenomenological cooling time.

Gravitational relaxation is another distinct channel: [Levkov, Panin and
Tkachev, arXiv:1804.05857v2](https://arxiv.org/pdf/1804.05857v2), equation 4,
derive a kinetic gravitational condensation timescale under their coherence
and scale-separation assumptions. That result concerns condensation rather
than this reaction and is not used for the numbers above.

`resonant_kinetics.py` checks the gain-loss cancellation with exact fractions,
finite entropy-sign cases, two independent decay-width normalizations,
Gaussian density normalization, a scaled kinetic ODE and detailed balance.
All 95 checks pass; `resonant_kinetics_run/manifest.json` validates. These
checks support the declared algebra and conditional estimate, not the
existence of the assumed halo bath. Interpretation is self-reviewed.

The creation route, transport candidate and repo identity remain separate
requirements. Cosmic abundance, full loading fluctuations, collision/heat
closure, stable halo profile and the acceleration/vacuum-density relation
are not supplied by this rate estimate.
