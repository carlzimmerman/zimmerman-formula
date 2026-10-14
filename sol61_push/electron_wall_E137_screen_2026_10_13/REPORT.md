# E137 screen of the electron-wall benchmark

2026-10-13. This changes the status of the stronger electron-wall examples in
../electron_material_wall_2026_10_13/REPORT.md. They must not be treated as
experimentally viable apparatus parameters on the strength of their small
one-loop electron magnetic-moment contributions alone.

## Published scalar comparison

Source: Liu, McKeen and Miller, *Validity of the Weizsäcker-Williams approximation
and the analysis of beam dump experiments: Production of a new scalar boson*,
[arXiv:1609.06781v3](https://arxiv.org/pdf/1609.06781v3), 13 February 2017,
Phys. Rev. D95, 036010. Equation (1) uses electron coupling g=e*epsilon.
Equations (2)–(3) give its photon and electron decays. Figure 4, PDF page 12,
shows the electron-only scalar exclusion inferred from E137. The shaded region
was inspected in a locally rendered PDF; no exclusion curve was numerically
digitized. The source record contains its PDF hash and exact locator.

Our coupling conversion is epsilon=|ye|/sqrt(4pi*alpha). At scalar mass 2 MeV:

| Electron coupling magnitude | epsilon | Position in the published scalar-only plot |
|---:|---:|---|
| 1e-8 | 3.30227e-8 | Below the displayed lower boundary |
| 1e-6 | 3.30227e-6 | Inside the shaded exclusion region |
| 1e-5 | 3.30227e-5 | Inside the shaded exclusion region |

The authors use a 20 GeV beam, a 2 GeV cut, 179 m shielding and 204 m decay
region; their null-result criterion is three events at 95% confidence. This
report does not independently reproduce that event count or confidence limit.
It checks how closely the tested extension preserves the relevant visible decay.

## Transfer to the retuned cold-source examples

The retuned benchmark also couples to muons and carriers. Rather than importing
the exclusion without checking these additions, compare its total width with
the electron-only width at the same mass and |ye|. The electron partial width
and leading electron bremsstrahlung production coupling are unchanged. Muon
and electron photon amplitudes are added coherently, including their signs.
The inherited retuned carrier partial width is included.

| Electron coupling magnitude | Fractional total-width change | Bound on fractional ee decay-probability change |
|---:|---:|---:|
| 1e-8 | +6.680e-2 | 6.56e-7 |
| 1e-6 | -1.922e-6 | 1.89e-7 |
| 1e-5 | -8.027e-7 | 7.88e-6 |

The probability bounds cover parent energy at least 2 GeV in the stated
longitudinal geometry, conditional on the stipulated on-shell widths. They
are not detector-efficiency bounds. For a source of boost beta*gamma,

    P_ee = integral_Lsh^(Lsh+Ldec)
             Gamma_ee/(beta*gamma*hbar*c)
             *exp[-Gamma_total*z/(beta*gamma*hbar*c)] dz.

For unchanged Gamma_ee, the ratio of integrands is
exp[-Delta_Gamma_total*z/(beta*gamma*hbar*c)]. Thus the relative probability
change is bounded by

    exp(|Delta_Gamma_total|*383m/(minimum_boost*hbar*c))-1,
    minimum_boost=sqrt((2GeV/2MeV)^2-1).

The closed-form probabilities were independently integrated at parent energies
2, 5, 10 and 20 GeV. For the two stronger-coupling rows the total width slightly
decreases, so this extension actually increases the electron decay probability
in that geometry. It does not hide the source through a large invisible width.
For |ye|=1e-5, the computed lab decay length runs from about 39 m at 2 GeV to
390 m at 20 GeV, directly illustrating the relevant flight-distance scale.

The weaker-coupling row has a larger fractional width change but such a long
lifetime that the probability of electron decay in the specified region scarcely
changes: in the long-lived limit this probability is controlled by Gamma_ee,
not the total width. That row is not certified allowed. Added secondary-muon
production, other searches and cosmology could constrain it independently.

## What is supported, and what is not

The two stronger wall benchmarks are strongly disfavored by this published
scalar limit. The calculated lifetime and branching changes do not provide an
evasion. This is a source-based exclusion screen, not a fresh statistical recast
of the full extended theory. Uncomputed ingredients include detector angular
acceptance, the production/shower integral, higher-order production interference,
and the source's energy-dependent near-threshold self-energy. The tiny assigned
mass detuning does not visibly move the benchmark in the MeV-scale published
plot, but a full recast would still use the full spectral function.

No pseudoscalar or dark-photon exclusion has been substituted for a scalar
limit. A source result outside a plotted region is not proof of viability, and
a different mediator or compensating interaction would need a new calculation.
The previous wall and width equations remain conditional mathematical results;
this new empirical screen limits how they may be interpreted.

Twenty-four bounded checks pass: independent decay-probability quadrature and
comparison with the uniform transfer bound for each of twelve coupling/energy
combinations. These checks validate the stated transfer calculation, not the
published event simulation or a new confidence region. No new Lean claim is made.

Next research decision: do not optimize storage hardware around ye=-1e-6 or
-1e-5 as though those points were allowed. The remaining smaller electron
coupling gives a much weaker wall, already flagged for poor finite-wall
confinement. A different mass or mediator would require a joint production,
storage and empirical-constraint calculation from the start.

Reproduce:

    python3 sol61_push/electron_wall_E137_screen_2026_10_13/check.py /tmp/electron_wall_E137_results.json
