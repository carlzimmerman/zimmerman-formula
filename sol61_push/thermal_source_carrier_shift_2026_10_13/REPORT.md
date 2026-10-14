# Thermal source bath shifts the carrier threshold

2026-10-13. A missing consistency check for the source-only cosmology in
../coupled_neutrino_source_2026_10_13/REPORT.md. This calculates one real thermal
self-energy contribution in a prescribed R bath. It is not a complete thermal
pole calculation or a new production rate.

## Defined approximation

Use L_int=-mu R|phi|^2, with a real R, complex phi, m=1 MeV and
|mu|=27.72246466 eV. Assume an equilibrium free R bath with zero chemical
potential and an initially negligible phi/anti-phi population. Evaluate the
external carrier at rest on its vacuum mass shell and take the exact vacuum
threshold limit MR=2m. The finite positive excess of the earlier benchmarks
is not resolved in this calculation.

For phi(p)+R(k) forward scattering, the two crossed carrier propagators give

    Mcal=-mu^2*[1/(MR^2+2m ER)+1/(MR^2-2m ER)],
    ER=sqrt(MR^2+k^2).

At MR=2m their sum simplifies exactly to Mcal=2mu^2/k^2.
Using the leading thermal forward-amplitude relation,

    Pi_phi=-integral d^3k/(2pi)^3 nB(ER)*Mcal/(2ER),

therefore gives the real threshold-limit contribution

    Pi_phi(T)=-mu^2/(2pi^2)*I0(T),
    I0(T)=integral_0^infinity dk nB(sqrt(k^2+MR^2))/sqrt(k^2+MR^2)
         =sum_(n>=1) K0(n MR/T).

The k^-2 amplitude singularity cancels the radial measure for this real
contribution, giving a finite integral at positive MR/T. That cancellation does
not establish a uniformly valid expansion for all spectral derivatives or a
finite-detuning collision rate. Finite detuning, source width and imaginary
parts need a separate treatment before interpreting a dynamical pole.

The normalization follows the forward self-energy convention checked in
../source_medium_shift_2026_10_13/REPORT.md. [Eletsky and Kapusta,
nucl-th/9810052v1](https://arxiv.org/pdf/nucl-th/9810052), Eq. (1), supplies
that convention after Mcal=8pi*sqrt(s)*f_cm. Its hadronic application supplies
no empirical evidence for our particles. The two scalar propagators and their
threshold simplification are derived explicitly here. The calculation is the
thermal-R part at leading mu^2; sequential scattering and the other thermal
species are not included.

## Numerical result

Define the first mass-shift diagnostic by

    Delta m=sqrt(m^2+Pi_phi)-m approximately Pi_phi/(2m).

A rationalized square-root difference avoids loss of numerical precision.

| Bath temperature | Pi_phi (eV^2) | Shift of pair threshold, 2 Delta m (eV) |
|---:|---:|---:|
| 0.1 MeV | -2.23532e-8 | -2.23532e-14 |
| 0.5 MeV | -0.440286 | -4.40286e-7 |
| 1 MeV | -4.92382 | -4.92382e-6 |
| 2 MeV | -22.8312 | -2.28312e-5 |
| 3 MeV | -45.6778 | -4.56778e-5 |

At 2 MeV this correction is only about 2.3e-11 of m^2, yet the pair-threshold
shift is about 8.57e10 times the weak electron-wall benchmark's assigned
vacuum excess, 2.66257e-16 eV. Small corrections relative to a MeV mass are not
necessarily small relative to the proposed cold-production excess.

The negative sign lowers the daughter threshold in this approximation. It
indicates that using the tiny vacuum Gamma_phi unchanged in a thermal source
bath is not justified. It does NOT establish a corrected decay rate, retained
carrier population, or complete thermal instability. The source pole and the
carrier spectral functions must be treated consistently. Replacing m by this
number in a vacuum width would leave those obligations unresolved.

## An independent quartic matters

The symmetry also permits L_contact=-(lambda/2) R^2 |phi|^2. Its leading
thermal contribution, with this precise normalization, is

    Pi_contact=lambda/(4pi^2)*I2(T),
    I2(T)=integral_0^infinity dk k^2*nB(ER)/ER.

The main calculation sets this independent coefficient to zero. It is not
fixed by the on-shell source decay widths. The positive coefficient that would
cancel the computed contribution at one temperature is

    lambda_cancel(T)=2mu^2*I0(T)/I2(T).

It equals 1.384e-9 at 0.5 MeV, 6.630e-10 at 1 MeV, 3.268e-10 at 2 MeV and
2.188e-10 at 3 MeV. These differing values show that cancellation at one
sampled temperature is not cancellation throughout the history. A larger
positive coefficient could instead move the carrier threshold upward. No
coefficient is chosen here to force a desired result; this is sensitivity to
an allowed but unspecified interaction.

This lambda is not the earlier phi self-quartic lambda_rep. Once carriers are
populated, their own interactions can contribute additional shifts and energy
exchange. The initially empty-carrier calculation cannot be extended to that
state without updating its assumptions.

## Consequence for the research route

The source-only Neff calculation remains valid for its declared equilibrium
R-only model. It must not be promoted to a full-model prediction by inserting
the original tiny vacuum carrier width: the existing cubic interaction already
produces a threshold-sensitive thermal correction. The next kinetic calculation
must fix the remaining scalar interactions, handle the near-threshold spectrum
with finite widths, and include carrier backreaction. This does not create an
automatic cosmological escape or establish a laboratory mechanism.

Sixteen checks pass: the exact crossed-propagator identity, five independent
quadrature/Bessel-series comparisons, five small-shift consistency checks and
five contact-cancellation identities. The latter are algebraic consistency
checks, not independent evidence that a physical cancellation occurs. The
momentum quadrature runs to k/T=100 and the series to 400 terms. No new Lean
certification or empirical discovery is claimed.

Reproduce:

    python3 sol61_push/thermal_source_carrier_shift_2026_10_13/check.py /tmp/thermal_source_carrier_results.json
