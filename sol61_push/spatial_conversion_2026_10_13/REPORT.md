# Spatial conversion, gravity, and the optical mass budget

2026-10-13. Status: **joint mechanism OPEN**. Conversion drives spatial mass redistribution in the stipulated coherent field model. The calculated force is ordinary gravity of that redistributed mass, not an increased gravitational coupling. Physical scale restoration and an absolute photon-rate budget expose significant obstacles to the earlier MeV/optical-gap example. No measured carrier, new gravitational law or functioning apparatus is established.

This checkpoint follows publication `6139426df70e868f02c0ee2faa8cba9e3ba902f1`. The original target remains an optical output associated with a mechanism capable of moving an object gravitationally.

## Spatial model and its explicit completion

Use dimensionless leading nonrelativistic kinetic masses 1 and 2, while retaining the small physical rest-mass gap as a slow detuning. The system is

\[
i\dot\psi=-\tfrac12\psi_{xx}+2c_3b\psi^*+2k|\psi|^2\psi+\Phi\psi,
\]
\[
i\dot b=-\tfrac14 b_{xx}+\delta b+c_3\psi^2+2\Phi b,
\qquad
\Phi_{xx}=\alpha(q-\bar q),\quad q=|\psi|^2+2|b|^2.
\]

The box has period \(2\pi\), the potential has zero mean, \(\delta=1\), and \(k=0.35\). This is a planar periodic model, not a finite spherical source. The Newtonian completion and coherent state are hypotheses. Using 2 rather than \(2+\delta/m\) for the source kinetic/gravitational rest-mass coefficient is the leading near-threshold approximation. Gap, kinetic, interaction and radiation energies would enter the relativistic gravitational source at the next order; \(q\) alone is not an exact stress-energy tensor.

The source is evolved, not eliminated. There is no electromagnetic field, external pump, dissipative term or boundary escape. Thus this calculation does not yet incorporate the glow.

## Local conservation identifies what can change gravity

The conversion contributions cancel in the charge continuity equation:

\[
\partial_t q+\partial_x j=0,\qquad
j=\Im(\psi^*\psi_x+b^*b_x).
\]

Hence reactions can change the species composition at a point without directly creating leading rest-mass density. Changes in \(q\) require currents. Defining the kinetic density
\(\tau=|\psi_x|^2/2+|b_x|^2/4\), Cauchy–Schwarz gives

\[
|j|^2\le2q\tau.
\]

For a smooth periodic solution, a nonzero mode \(q_\ell=\langle qe^{-i\ell x}\rangle\) obeys

\[
|q_\ell(t)-q_\ell(0)|
\le |\ell|\int_0^t\sqrt{2\bar q\,\langle\tau\rangle(s)}\,ds.
\]

This integrated inequality assumes sufficient regularity and is an analytical deduction, not a formal PDE theorem in this package. In the nongravitating closed model the positive-square matter energy bounds the kinetic energy; gravitational potential energy must be retained when \(\alpha>0\).

The numerical Hamiltonian diagnostic is

\[
H=\left\langle\tfrac12|\psi_x|^2+\tfrac14|b_x|^2
+\delta|b|^2+2c_3\Re(b^*\psi^2)+k|\psi|^4+\tfrac12q\Phi\right\rangle.
\]

Charge, this total energy and mean momentum are checked. The periodic zero mode is conserved; there is no creation of monopole mass.

## Actual spatial calculations

Prepare a small, real daughter seed
\(\psi(x,0)=0.01(1+0.5\cos x)\) and
\(b(x,0)=\sqrt{(2-|\psi(x,0)|^2)/2}\).
Initial total density is exactly uniform, \(q=2\), and current is zero. The spatial composition pattern is a supplied initial condition; its preparation is not explained.

Five cases were run to dimensionless time 30, each at three resolutions: 64 points/time step 0.005; 64/0.0025; and 128/0.0025. This separately tests temporal and spatial refinement. The integrator uses exact Fourier kinetic half-steps and a fourth-order Runge–Kutta local step. The local Poisson potential is held fixed during the local step, consistent with exact local charge conservation; its numerical error is included in the checks. Spectral collocation is not a proof of continuum convergence.

| \(c_3\) | \(\alpha\) | Maximum daughter charge fraction | Maximum fundamental density amplitude | Maximum force \(|-\Phi_x|\) |
|---:|---:|---:|---:|---:|
| 0 | 0.02 | 0.00005625 | 0.0001503 | 0.000003007 |
| 0.3 | 0 | 0.9014 | 1.4016 | 0 |
| 0.3 | 0.02 | 0.9081 | 1.2574 | 0.03080 |
| 0.5 | 0.02 | 0.8342 | 2.3763 | 0.05894 |

Values are from the finest runs, sampled every 0.1 time unit. The density amplitude is \(2|q_1|\), not the pointwise contrast; it can exceed the mean in a nonsinusoidal positive density profile. Maxima in different columns need not occur together.

The fifth case has \(c_3=0.3\) and \(\alpha\simeq7.2674\times10^{-39}\), set by the physical example below. Its density evolution is indistinguishable at reported precision from the nongravitating case; its force remains proportional to the tiny gravitational coefficient.

Thus conversion can drive transport even without self-gravity. Adding gravity makes that evolving distribution a gravitational source. It does not demonstrate a new force law, confinement, a finite detector displacement, or optical emission.

Across the original four cases, the largest temporal refinement difference in the density-mode history is \(5.38\times10^{-4}\); the spatial difference is below \(8\times10^{-12}\). The finest runs conserve mean charge to about \(8\times10^{-12}\), total energy to \(9\times10^{-7}\), and mean momentum to \(7\times10^{-14}\). All five case contracts pass. These are bounded numerical checks with stated tolerances.

## Restoring physical units prevents a false strong-force claim

For a physical gap \(\Delta E\), daughter mass \(m\) in kilograms, and field-density unit \(n_*\),

\[
t_0=\hbar/\Delta E,\qquad
x_0=\hbar/\sqrt{m\Delta E},\qquad
\rho_*=mn_*,\qquad
\alpha=4\pi G\rho_*t_0^2.
\]

Since \(\bar q=2\), the mean mass density is \(2\rho_*\). Physical acceleration is \((x_0/t_0^2)(-\Phi_x)\). Choosing the previous \(mc^2=1\) MeV, \(\Delta E=5\) eV example gives

\[
t_0=1.3164\times10^{-16}\ \mathrm{s},\quad
x_0=8.8247\times10^{-11}\ \mathrm{m},\quad
2\pi x_0=5.5447\times10^{-10}\ \mathrm{m}.
\]

The illustrative \(\alpha=0.02\) corresponds to a mean density of **\(2.7520\times10^{39}\) kg/m³**. It is not an experimentally admitted apparatus. At a stipulated mean density of 1000 kg/m³, \(\alpha=7.2674\times10^{-39}\); the separately executed fifth case yields maximum acceleration **\(6.3055\times10^{-17}\) m/s²** on this microscopic periodic scale.

Density is an input, not a detected amount of carrier. Changing the spatial scale, mass, gap or field normalization changes the dimensionless kinetic and coupling parameters; these numbers cannot simply be relabeled as a meter-sized device. The periodic microscopic field is also not the far field of a macroscopic source.

## Absolute glow budget and the mass tradeoff

The preceding radiative report derived, for the hypothetical dimension-seven portal and \(\Delta E\ll mc^2\),

\[
\Gamma_\gamma=\frac{\zeta^2\mathcal B_3\delta^{17/2}}
{96\pi^5M\sqrt m\Lambda^6},\qquad
\mathcal B_3=\frac{\Gamma(4)^2\Gamma(3/2)}{\Gamma(19/2)}.
\]

Here the width formula uses natural-unit masses/energies. It permits computing luminosity per *available source mass*, rather than choosing an unspecified source number. For a dilute population of sources at rest, before depletion,

\[
\frac{P_{\rm vis}}{M_{\rm sources}}
=\frac{\Gamma_\gamma}{\hbar}\frac{16\delta}{19M}c^2 f_{E,\rm vis}.
\]

At a 5 eV gap, \(f_{E,\rm vis}=0.60686\) for 400–700 nm. The following explicit benchmark assumes \(\zeta=1\), \(\Lambda=10M\), and the vacuum tree formula:

| Daughter rest energy | RMS daughter speed / \(c\) | Visible watts per kilogram of sources |
|---:|---:|---:|
| 1 keV | 0.02810 | \(3.3593\times10^{-4}\) |
| 12.5 keV | 0.007947 | \(1.6236\times10^{-13}\) |
| 1 MeV | 0.0008885 | \(1.0837\times10^{-29}\) |

The smaller masses are much brighter in this fixed-gap comparison but produce faster daughters. They are not claimed empirically viable. The gap ratios are 0.005, 0.0004 and 0.000005; the expression remains a leading near-threshold calculation. The script also evaluates \(\Lambda=M\), producing rates a million times larger, but that comparison is at the edge of the relativistic effective expansion and is not presented as controlled.

At fixed gap and \(\Lambda/M\), the leading mass scaling is approximately \(P_{\rm vis}/M_{\rm sources}\propto m^{-17/2}\), while \(v_{\rm rms}\propto m^{-1/2}\). Thus this benchmark has an unusually steep brightness–speed tradeoff, approximately power per source mass proportional to \(v_{\rm rms}^{17}\). This scaling is conditional on the operator and fixed parameters, not a universal constraint on luminous cold matter. A different interaction or a specified UV completion may change it.

The quoted luminosities are radiative partial rates. A competing nonradiative decay can deplete the source; maintaining steady power would require replenishment and its energy/mass budget. Photon transport, absorption, material conversion and visual comfort are not modeled.

## Evidence and formal scope

`SpatialConservation.lean` certifies the real-component cancellation giving local charge flow and a weighted current inequality. It does not formalize PDE existence, Fourier integration, physical units, the Poisson completion or the photon rate. Two deliberately damaged coefficient controls fail. Numerical and successful optical-budget manifests validate against their pinned inputs.

The first optical-budget run failed only when serializing a NumPy boolean to JSON. Its logs and manifest remain in `optical_run/`, and the exact failed source is preserved as `optical_budget_failed_snapshot.py`. The corrected Boolean serialization is in `optical_budget.py`; `optical_run_v2/` is the successful evidence. The failed manifest points to the historical version of that script and is not a current-input validation record. It supplied no numerical result file.

This is self-reviewed work. Analogue atom–molecule studies also distinguish coherent mean-field conversion from spontaneous quantum dissociation; [Vardi, Yurovsky and Anglin, cond-mat/0105439](https://arxiv.org/abs/cond-mat/0105439) reports quantum effects omitted by mean-field descriptions. That analogy does not identify these hypothetical carriers or validate their parameters.

Reproduction commands and hashes are in `run/manifest.json`, `lean_run/manifest.json`, and `optical_run_v2/manifest.json`. `check.py` and `optical_budget.py` each accept a results-file path. The contracts specify the ranges, numerical tolerances, environments and non-claims.

## Remaining routes and next discriminating calculation

1. **Conversion-driven transport:** finite evidence now exists in a coherent planar model. Finite geometry, a prepared carrier inventory, admission of the coherent state, and detector motion remain unproved. Larger dimensionless force alone is not progress without restoring units.
2. **Radiative energy removal:** the photon branch leaves less daughter kinetic energy than ordinary conversion, but a source decay is not automatically cooling of an already existing gas. A specific recycling process such as \(\phi\phi\to\chi\to\phi\phi\gamma\gamma\) needs a resonant collision kernel, detailed balance and escaped-photon accounting. The radiative probability and depletion times are unresolved. This is the next discriminating microscopic calculation; no phenomenological damping term should be inserted as its substitute.
3. **Other optical or metric interactions:** open but unspecified. Material reprocessing requires a matter coupling; a modified gravitational response requires a metric action and stability analysis. Neither can be inferred from the word “glow.”

The current calculation supports a possible relationship between conversion and mass transport, while quantitatively failing to establish the requested macroscopic light-plus-gravity effect for the stated MeV example. The full mechanism remains open.
