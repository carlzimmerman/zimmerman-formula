# The imposed well can transmit excitations, but angular escape narrows its depth

2026-10-13. The previous turn derived a conditional selective-confinement window and a stationary interface profile. This continuation solves the leading Bogoliubov scattering problem on that profile. The external well remains an added assumption: this does not identify a microscopic trap in the original action.

## Linearized interface problem

Let mu_int be the interior interaction chemical potential and use the healing length xi=(2m mu_int)^(-1/2) for distance. With dimensionless quasiparticle energy e=E/mu_int, profile y(x), and beta=V0/mu_int-1, the perturbations obey

\[
e\binom uv=\begin{pmatrix}\mathcal H&y^2\\-y^2&-\mathcal H\end{pmatrix}\binom uv,
\quad\mathcal H=-\partial_x^2+k_\parallel^2+W_0(x)+2y^2,
\]

where W0=-1 inside and beta outside. Equivalently,

\[
u''=(W-e)u+y^2v,\qquad v''=(W+e)v+y^2u,
\quad W=k_\parallel^2+W_0+2y^2.
\]

The code imposes one incoming positive-norm interior phonon, an outgoing reflected phonon, the admissible interior evanescent component, and outgoing/decaying exterior modes. Growing evanescent components and exterior incoming waves are excluded. A sparse finite-difference boundary-value solve avoids exponentially ill-conditioned long-distance transfer matrices.

The conserved normal flux is proportional to Im(u* u'+v* v'). The plus sign between components is required by these BdG equations. Normalizing the incident mode by |u_in|²-|v_in|²=1 gives

\[
R=|r|^2,\qquad
T=\frac{k_{x,\rm out}}{k_{x,\rm in}(|u_{\rm in}|^2+|v_{\rm in}|^2)}|t|^2.
\]

A closed exterior channel has T=0. Flux conservation, rather than simply adding raw amplitude squares, checks the normalization.

## Transmission results

Use the preceding mu_int=0.714214 eV and E=1.785934 eV. Normal-incidence results on the finest tested grid are:

| Assumed well depth | Reflection | Transmission |
|---:|---:|---:|
| 1 eV | 1.98% | 98.02% |
| 1.5 eV | 5.69% | 94.31% |
| 2 eV | 15.53% | 84.47% |

These are leading single-field results, not full coupled-source predictions. Three grid spacings (0.04, 0.02 and 0.01 healing lengths) give converging normal-incidence values. The finest-grid flux imbalance is below 4.2×10⁻⁵. Increasing the half-domain from 16 to 20 healing lengths checks the 1 eV normal-incidence boundary truncation. This is a bounded numerical verification, not an error-certified continuum proof.

Oblique incidence changes the conclusion more than normal-incidence reflection does. At a 1 eV well, transmission is about 97.1%, 91.1% and 67.1% at 30, 60 and 80 degrees. At 1.5 eV, the 80-degree channel is closed; at 2 eV, the 60- and 80-degree channels are closed. Those closed channels have numerically unit reflection. The oblique cases use a spacing of 0.02 healing lengths and were not all separately refined.

## All-angle kinematic window

Tangential momentum is conserved at the planar interface. The interior total kinetic parameter is

\[
\epsilon_k=\sqrt{E^2+\mu_{\rm int}^2}-\mu_{\rm int},
\qquad k_{\rm in}^2/(2m)=\epsilon_k.
\]

The exterior normal kinetic energy is

\[
\frac{k_{x,\rm out}^2}{2m}=E+\mu_{\rm int}-V_0-\epsilon_k\sin^2\theta.
\]

To keep an exterior propagation channel open for every nongrazing incidence angle while binding the background, a sufficient strict window is

\[
\boxed{\mu_{\rm int}<V_0<2\mu_{\rm int}+E-\sqrt{E^2+\mu_{\rm int}^2}.}
\]

Numerically this becomes **0.714214 eV < V0 < 1.290912 eV**, narrower than the earlier normal-incidence energy window ending at 2.500149 eV. The interval is nonempty for positive mu_int and E, since sqrt(E²+mu_int²)<E+mu_int.

An open channel at every angle is not a uniform lower bound on transmission. Reflection can approach unity as incidence becomes grazing; exactly grazing waves carry no normal incident flux. No perfectly nonreflecting wall has been found.

## Implication for pair growth

The 1 eV wall is a concrete mathematical example that binds the background in the imposed potential and transmits much of the outgoing excitation flux at the tested angles. The deeper examples would trap some angular channels even though normal incidence remains open. This makes angular transport a necessary part of the proposed escape mechanism.

The earlier outgoing-path threshold assumed zero reflection. Its value cannot simply be carried over to the wall calculated here: finite reflection changes feedback and the mode spectrum. Nor do planar scattering coefficients alone establish stability of a finite ball. A next calculation must combine the complex reflected-wave boundary conditions with pair amplification, path length and phase accumulation.

The interface therefore improves the conditional construction but does not complete it. The actual trapping interaction, full two-field wall, finite geometry, source replenishment and gravitational response remain unresolved. All light and matter excitation preparation still uses the stipulated photon portal and external drive.

## Evidence scope

Eighteen scattering solves cover the three depths, normal mesh refinements and oblique angles; one additional solve checks domain size. Linear-system residuals are below 10⁻⁷, and flux imbalance is checked below 0.004 in every case. The contract, copied well parameters, script and run manifest record the exact range and outputs. This calculation is numerically checked and analytically self-reviewed, not newly Lean-certified. It is not empirical support for the hypothetical material.
