# Switching a resonance must account for all collision energies

2026-10-13. A prescribed pole shift can suppress the resonant annihilation found in the preceding package, but a small shift in the wrong direction enhances it. A proposed density-based shift also modifies confinement. This identifies a conditional production/storage switching requirement; it does not construct a controller or establish stored cold energy.

## Distribution and fixed-coupling model

Retain the previous neutral R resonance: original excess Delta0=M_R-2m=2e-9 eV, m=1 MeV, and equal on-shell partial widths w=1e-12 eV. Assume an uncorrelated isotropic population with exactly K=Delta0/2 kinetic energy per carrier. Its pair excess energy epsilon is uniform over [0,Delta0]. This is the same diagnostic distribution used previously, not a computed output of production or a thermal ensemble.

Now prescribe a shifted resonance excess D while holding the interaction couplings fixed. The daughter contribution to the imaginary width at collision energy epsilon remains w sqrt(epsilon/Delta0). It must not be reset to w at the new pole. With the previous on-resonance beta0 and peak production cross section sigma_peak, the annihilation kernel is

\[
a(\epsilon;D)=\frac{4c\sigma_{\rm peak}}{\beta_0}
\frac{4}{4[(\epsilon-D)/w]^2+[1+\sqrt{\epsilon/\Delta_0}]^2},
\]
\[
\bar a(D)=\frac1{\Delta_0}\int_0^{\Delta_0}a(\epsilon;D)\,d\epsilon.
\]

This is the previous isolated-pole approximation with its pole moved by assumption. A physical medium can also change residues, widths and dispersive self-energies; none is derived here. In particular the near-threshold real self-energy must be treated in a complete controller model.

## Finite-width results

Normalize to the original endpoint pole, whose averaged coefficient is 1.28779e-12 m³/s:

| Shifted excess D (eV) | Averaged annihilation / original |
|---:|---:|
| 2.2e-9 | 0.0028944 |
| 2.02e-9 | 0.031497 |
| 2.0e-9 | 1 |
| 1.98e-9 | 1.97337 |
| 1.0e-9 | 2.34243 |
| 2.0e-11 | 3.60511 |
| 0 | 1.97795 |
| -2.0e-11 | 0.031516 |
| -2.0e-10 | 0.0028944 |

Moving downward by ten original total widths (2e-11 eV) does not turn annihilation off: it moves the pole from an endpoint into the sampled interval and almost doubles the average. Even putting the pole exactly at threshold leaves a finite near-threshold contribution. Shifting sufficiently above the maximum sampled collision energy or below threshold suppresses loss in this specified distribution.

An upward shift of 2e-10 eV yields a factor about 345 reduction here. A physical distribution with high-energy tails can still sample a pole above this idealized cutoff. This result therefore cannot be used as a distribution-independent storage lifetime.

For an independent quadrature control, freeze the width at 2w. The integral is then proportional to

\[
\frac{w}{\Delta_0}\left[
\arctan\frac{\Delta_0-D}{w}-\arctan\frac{-D}{w}\right].
\]

Nine such controls and nine refined running-width integrals pass, plus three directional-behavior checks (21 total).

## Does the proposed messenger medium supply the switch?

At leading order in the prior density potential, adding a uniform interior messenger density produces U_in=h n_in/(4mM_S), a positive carrier energy shift. If this changes the effective carrier rest energy without appreciably changing M_R or the kinetic distribution, then

\[
D=\Delta_0-2U_{\rm in}.
\]

These conditions are additional hypotheses, not a solved medium response. The R-messenger interaction and all allowed medium corrections must be included before claiming the relationship is realized. A spatially uniform time-dependent shift also transfers energy from its external controller; it is not free work. Gradients, heating and changes in particle propagation require a dynamical treatment.

This particular control moves D downward, into the dangerous interval first. To cross below threshold requires U_in>Delta0/2=K. It also reduces the remaining wall height to U_wall-U_in. Retaining the carriers demands

\[
K<U_{\rm wall}-U_{\rm in}.
\]

The existing U_wall=1.9208764e-9 eV is below 2K=2e-9 eV. It cannot both retain these K=1e-9 eV carriers and support a threshold-crossing interior shift within this approximation. The limiting wall density would need to exceed its old value by at least a factor 1.04119 just to reach threshold; a negative D with useful suppression requires a further margin. This is a constraint on the chosen wall, not a universal impossibility of density control.

For example D=-2e-10 eV requires U_in=1.1e-9 eV and U_wall>2.1e-9 eV to retain the stipulated kinetic energy. The actual required wall should also allow tunnelling, finite-temperature and fluctuation margins. Neither that modified shell nor the interior density control has been physically constructed. The charged medium's preparation, neutralization, cooling and stability remain open.

## Research consequence

A narrow resonance can aid production, but storing the products requires changing the interaction relative to the complete occupied collision spectrum and preserving confinement during the change. Merely specifying a shift in linewidth units misses this issue. The next meaningful controller calculation must jointly evolve the medium, pole, carrier energy distribution and barrier, including the energy supplied during switching. No empirical evidence, new Lean certificate or completed manufacturing route is claimed.
