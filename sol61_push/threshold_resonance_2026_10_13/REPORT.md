# A tuned neutral resonance can enhance cold production, but also annihilation

2026-10-13. A new hypothetical neutral scalar resonance removes the tiny direct-contact production rate in the specified ideal-beam calculation. Finite bandwidth is included. The reverse reaction becomes strong as well, and the required mass, narrow widths, photon source and messenger wall are not established. This is a conditional extension, not evidence that the repo already contains a physical creation mechanism.

## Added interactions and widths

Introduce a real scalar R with mass M_R=2m+Delta, distinct from the original globally charged source chi. Use

\[
\mathcal L\supset-\mu R|\Phi|^2-\frac{g_\gamma}{4}RF^2.
\]

R carries no carrier-global charge and decays to Phi+anti-Phi. It does not create net global charge. A charged-messenger coupling -A R|S|² can generate |g_gamma|=alpha |A|/(12 pi M_S²) in the same leading heavy-messenger expansion used previously. Signs matter for interference and the scalar potential; the rates here use magnitudes and retain the resonant term alone.

The on-shell widths are

\[
\Gamma_\gamma=\frac{g_\gamma^2M_R^3}{64\pi},\qquad
\Gamma_\Phi=\frac{\mu^2}{16\pi M_R}\sqrt{1-4m^2/M_R^2}.
\]

The illustrative choice is m=1 MeV, Delta=2e-9 eV and Gamma_gamma=Gamma_Phi=1e-12 eV. It corresponds to |g_gamma|=5.0133e-15 eV^-1, |mu|=47.412 eV and |A|=2589.9 eV for M_S=10 MeV. The total lifetime is 0.329 ms. These parameters are assigned, not derived or measured.

The addition requires scalar-potential matching, counterterms and stabilization. Static R exchange contributes -mu²|Phi|⁴/(2M_R²), of magnitude 2.81e-10 in the quartic coefficient for this benchmark, below the previous 1e-6 repulsion. This one coefficient does not establish stability of the complete R,S,Phi potential. Mass renormalization and maintaining Delta/m=2e-15 are major additional obligations, not symmetry-protected results shown here.

## Resonant cross section and bandwidth

For unpolarized photons, near the resonance,

\[
\sigma(\gamma\gamma\to R\to\Phi\bar\Phi)
=\frac{8\pi\Gamma_\gamma\Gamma_\Phi(E)}
{M_R^2[4(E-M_R)^2+\Gamma_{\rm tot}(E)^2]}.
\]

Mass prefactors are frozen at 2m, with errors of order the tiny excess divided by m; threshold phase space and the running daughter width are retained. Write epsilon=E-2m: Gamma_Phi(epsilon)=Gamma_Phi(Delta) sqrt(epsilon/Delta), zero below threshold, and Gamma_tot=Gamma_gamma+Gamma_Phi(epsilon). The real energy-dependent self-energy and full nonresonant interference are not calculated; this is an isolated narrow-pole model.

At equal branching fractions the peak cross section is 2 pi/M_R²=6.1164e-26 m². This does not imply the whole photon spectrum sees the peak. The code integrates against a Gaussian distribution of center-of-mass excess energy, centered on Delta. Width-resolving tangent substitution avoids missing the narrow pole, and an independent constant-width Voigt integral checks normalization.

Using the same **assumed** 1 MW per beam, 1 mm² beam area and 2 mm overlap length:

| RMS CM-energy spread | Averaged cross section (m²) | Ideal production (pairs/s) |
|---:|---:|---:|
| 1e-12 eV | 4.0104e-26 | 2.0845e7 |
| 1e-10 eV | 7.6049e-28 | 3.9529e5 |
| 1e-9 eV | 7.6594e-29 | 3.9812e4 |

For a center of mass at rest, more than 99.999% of the computed resonant production lies below the previous 1.9209e-9 eV per-particle wall height in these cases. This counts energy acceptance only. Beam imbalance, angular divergence, R propagation before decay, the finite cavity matrix element, messenger attenuation and wall fluctuations can reduce actual capture. No photon source with the stipulated simultaneous power and spectral precision has been provided.

## Reciprocity cannot be omitted

For the reverse reaction at the same pair invariant mass, the polarization and identical-photon factors give

\[
\sigma_{\rm ann}=2\sigma_{\gamma\gamma}/\beta^2,\qquad
\sigma_{\rm ann}v_{\rm rel}=4\sigma_{\gamma\gamma}/\beta.
\]

Thus the resonance enhances annihilation too. As a diagnostic, take an isotropic uncorrelated carrier population with fixed kinetic energy K=Delta/2 per particle. Its relative-pair excess is uniform on [0,Delta], giving

\[
\langle a\rangle=\frac1\Delta\int_0^\Delta d\epsilon\,
\frac{4c\sigma(\epsilon)}{\sqrt{\epsilon/m}}
=1.2878e-12\ \mathrm{m^3/s}.
\]

Inserting this into a uniform dilute rate balance would give about 180,000, 24,800 and 7,860 particles **per sign** in the overlap volume for the three bandwidths, respectively. These are diagnostic scales, not predicted inventories: the actual product distribution and spatial correlations have not been evolved. Quantum occupation also needs checking, especially in the highest-rate case. The original demixing calculation cannot simply be reused: adding a pole this close to the pair threshold changes the opposite-sign interaction and its dynamics.

The resonance therefore gives a calculable way to enhance production under new assumptions, but it does not permit unrestricted accumulation or demonstrate a macroscopic mass. It requires a coupled production, resonance, spatial transport and loss calculation, with actual confinement and photon-source assumptions tested.

## Evidence and limitations

Twelve checks pass: partial-width/peak identities, three refined bandwidth integrals, three independent Voigt controls and three reciprocal-rate checks. The manifest pins the code and numerical output. No Lean proof of the resonance model or empirical evidence is claimed.

The Breit-Wigner normalization and the need to fold with photon luminosity are checked against [hep-ph/9405376v1, Eqs. (3.3)–(3.4)](https://arxiv.org/pdf/hep-ph/9405376). Averaging independent unpolarized helicities sets the source's (1+lambda lambda') factor to one. That source concerns established scattering formalism, not this particle's existence. No experimental-viability or novelty claim is made.

The goal remains open. This calculation improves the ideal production rate through an explicit new hypothesis, while exposing reciprocal loss and extremely precise mass/bandwidth requirements. It is not a discovery of new physics or a completed cold-energy manufacturing protocol.
