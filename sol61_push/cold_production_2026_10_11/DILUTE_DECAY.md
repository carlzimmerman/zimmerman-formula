# A dilute near-threshold decay route avoids the crowded production shell

2026-10-11. The previous turn made progress by identifying rapid inverse
conversion in the highly occupied 193.5 eV example. That obstruction is
parameter-dependent. The repo's microscopic-carrier report calls for a
massive multimode field with kinetic stress, not necessarily a condensate.
This turn tests the same protected action in a dilute production regime.
The halo target and acceleration normalization remain requirements; this is
not a redefinition of the full objective as merely making a cold gas.

## Revised example

Keep u=0.01, alpha=lambda_rep/lambda_min=2, initial source energy density
9.71510619e6 eV^4, and the illustrative threshold cross section per mass
4 cm²/g. Vary the daughter mass. Since the threshold cross section per mass
scales as lambda_rep²/m³, set lambda_min proportional to m^(3/2). Set

    M=2m sqrt(1+u²),
    g=2m u sqrt(lambda_min),
    A=sqrt(rho_source)/(sqrt(2) M).

The 1 MeV example is:

| Parameter | Value |
| --- | ---: |
| Daughter mass m | 1,000,000 eV |
| Source mass M | 2,000,099.9975 eV |
| Positive mass gap M-2m | 99.9975 eV |
| lambda_min | 0.0107267 |
| lambda_rep | 0.0214535 |
| Total quartic | 0.0321802 |
| Cubic coupling g | 2071.40 eV |
| Source amplitude A | 0.00110194 eV |
| Pump parameter gA/m² | 2.28255e-12 |
| Vacuum width Gamma | 0.000853522 eV |
| Vacuum lifetime hbar/Gamma | 7.71172e-13 s |

This explicitly changes epsilon as well as the mass. The earlier Gaussian
runs with epsilon=1e-7 are not transplanted to this example. Neither the mass
nor 4 cm²/g is observationally validated or selected by the repo's halo law.
The total quartic is small compared with one, and Gamma/(M-2m)=8.5354e-6:
perturbative, narrow-line decay is a plausible approximation to test here.
The small dimensionless quartic alone is not a full renormalization analysis.

## Why dilution changes the production problem

In the vacuum-decay approximation, let the initial source amplitude decrease
as exp(-Gamma*t/2). For a daughter pair with detuning Delta=2E-M, the leading
pair-production amplitude is

    beta_Delta(t)=i Omega [1-exp(-(Gamma/2+i Delta)t)]/(Gamma/2+i Delta),
    Omega=gA/(M/2).

Natural units are used in this formula. It is the weak-pump solution, not a
nonlinear Bogoliubov simulation with an independently imposed damping term.
The same coupling g fixes both the spontaneous width and pair amplitude.
At late times the peak daughter occupation is 4 Omega²/Gamma², and the
triangle inequality gives the uniform-in-time bound 16 Omega²/Gamma².

| Daughter mass | Total quartic | Gamma/Omega | Formal late-time peak occupation |
| --- | ---: | ---: | ---: |
| 193.525 eV | 8.66e-8 | 2.30e-8 | 7.57e15 |
| 10 keV | 3.22e-5 | 0.00118 | 2.86e6 |
| 100 keV | 0.001018 | 0.665 | 9.05 |
| 300 keV | 0.005288 | 13.64 | 0.0215 |
| 1 MeV | 0.03218 | 373.95 | 2.8604e-5 |

The large formal occupations in the first rows invalidate the weak-pump
approximation there; they are NOT predicted yields. In the 1 MeV row the
uniform-time bound is 1.1442e-4. Within this approximation, Bose enhancement
is small rather than the dominant feedback encountered in the original
narrow, densely occupied shell. Increasing the mass while holding threshold
sigma/m fixed makes Gamma/Omega scale as m^(11/4), explaining this transition.

## Number transfer is consistent with the same decay width

Let E0=M/2 and p_star=m u. The daughter density of states at line centre is
D0=E0*p_star/(2pi²). At late time, integrating the narrow line with D0 held
constant gives

    n_daughter = D0*pi*Omega²/Gamma = 2 rho_source/M.

At finite time the corresponding integral gives

    n_daughter(t) = (2 rho_source/M)[1-exp(-Gamma*t)].

Thus the leading approximation transfers the initial source charge into
daughters with the same width that depletes the source. It is not a separate
choice of a production rate and a final density. This number identity is a
necessary consistency check, not a proof of the interacting quantum dynamics.

The code checks the identity for all five parameter rows and audits the
finite-time spectral integral at Gamma*t=0.1,1,5,10. Its integration variable
y=2Delta/Gamma has cutoff |y|<=1000, with an explicit analytic tail bound.
The physical line centre is well above threshold for the chosen row. A
constant-density-of-states Lorentzian extended arbitrarily far from resonance
is not a complete physical spectrum: off-resonant tails and source preparation
must be treated by the underlying theory when needed.

The first audit had an erroneous factor of two in converting its dimensionless
line integral into charge fraction. The independently expected number identity
exposed it. The original failed script and run remain recorded;
`dilute_decay_v2.py` repairs that normalization in a distinct run. All 12 v2
checks pass, and its manifest validates input/output provenance.

## Coldness and scope

The daughter speed at production is u/sqrt(1+u²) times c, about 0.01c, and the
free isotropic daughter gas has P/rho_E=u²/[3(1+u²)]=3.3330e-5. The fractional
mass gap and the positive charge-energy structure are unchanged by this mass
rescaling. The finite-regulator NR completion-square argument still has a
positive residual because lambda_rep remains positive. A spatial condensate
is not needed for these energy and pressure statements.

This offers a simpler conditional preparation than requiring the earlier
high-occupation shell to thermalize into a condensate. It still assumes the
initial charged source, its density and epoch. It is not creation from vacuum
or a source of free energy. The previous 97-98% Bose endpoint percentages do
NOT apply to the rescaled gas; its occupation statistics and thermodynamics
must be recomputed if required.

The next checks are inverse-conversion and scattering during dilute decay,
finite-time stimulated corrections, and subsequent expanding kinetic evolution.
The original source/daughter action supplies these interactions; they should
not be replaced by a target-temperature relaxation law. Even a fully controlled
dilute production calculation would leave cosmological perturbations, halo
formation and the repo's baryon/vacuum-dependent profile selection unresolved.
