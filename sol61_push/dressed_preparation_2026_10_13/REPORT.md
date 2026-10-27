# Preparation closes the weak-conversion shortcut in a fixed-bath model

2026-10-13. This extends the dressed-width calculation by imposing an explicit kinetic closure. It does not derive that closure or the bath's preparation from the underlying Hamiltonian. No new empirical evidence is claimed.

## Forward and inverse reactions together

Let N be the occupation of one normalized zero-momentum gapped mode, and f the equal occupations of the two opposite-momentum lower-branch modes on its decay shell. Let a denote the zero-temperature dressed matter width, and b the proposed photon width. For a fixed incoherent isotropic bath, a Markov/golden-rule approximation and escaping photons with negligible incident photon occupation give

\[
\dot N=a[f^2(1+N)-(1+f)^2N]-bN
=af^2-[a(1+2f)+b]N.
\]

The identical-particle factor is already included in a; the reverse process uses the same matrix element. This is a kinetic mode occupation, not the stationary coherent source background. The bath is stipulated and held fixed. Interactions between excitations, bath depletion, memory and coherent driving are omitted.

Define D=a(1+2f)+b. For an initially unoccupied gapped mode,

\[
N(t)=\frac{af^2}{D}(1-e^{-Dt}),\qquad
C_\gamma(t)=\frac{baf^2}{D}\left[t-\frac{1-e^{-Dt}}D\right].
\]

Here C counts emitted photon pairs, since each radiative transition emits a pair; individual photon count is twice C. The emitted power is the pair energy times bN.

At stationarity,

\[
J_\gamma=\frac{abf^2}{a(1+2f)+b}
\le\frac{bf^2}{1+2f}.
\]

For a thermal bath whose on-shell quasiparticle energy is half the gap, f=1/(exp(omega/(2T))-1), the ratio f²/(1+2f) equals 1/(exp(omega/T)-1). Thus the bath can at most populate this mode to its Bose equilibrium occupation in this closure; the photon sink lowers it further.

At fixed b and f,

\[
\frac{dJ_\gamma}{da}=\frac{b^2f^2}{[a(1+2f)+b]^2}\ge0.
\]

This is the discriminating result: reducing the matter coupling can improve the probability that a separately prepared excitation radiates, but it cannot increase the steady photon supply from this fixed matter bath. As a tends to zero, J tends to af² and vanishes. At short times, C is approximately abf²t²/2. A favorable branching ratio alone is therefore not a preparation mechanism.

## Numerical check and energy budget

Fifteen ODE cases test f=0.01, 1 and 100 against five matter/photon rate ratios from 10⁻⁶ through the preceding benchmark. Integrating the unsimplified forward and inverse Bose terms reproduces the analytic occupation and integrated pair count over three relaxation times. The stationary flux ceiling is checked in every case. The f=100 cases are mathematical checks of the stipulated closure, not evidence that a fixed high-occupation bath is physically sustainable or weakly interacting.

Using the preceding benchmark widths a=164.7375 s⁻¹ and b=4.9015653 × 10⁻¹² s⁻¹, the corrected gapped-mode energy is approximately 3.57187 eV. A stipulated population of one source-equivalent kilogram carries about 1.605 × 10¹¹ J of excitation energy. Its initial radiative power is about 0.787 W. If every decay removes an excitation and an external preparation process replaces it, the gross excitation replacement power is approximately **2.64 × 10¹³ W** per source-equivalent kilogram.

That last number is not a thermodynamic minimum work cost or a heat-dissipation prediction. Matter decay deposits energy in other excitations, which could in principle be recovered. In the fixed-bath stationary equation, the net matter-to-source energy transfer equals the photon loss. Claiming the full gross replacement power as unavoidable wasted energy would double-count recoverable circulation. An actual recycling mechanism and its losses have not been supplied.

Nor is a single-mode occupation a macroscopic source inventory: a finite volume, mode spectrum, depletion bound and prepared population must be specified before integrating a luminosity. The existing dense-condensate confinement obstacle also remains.

## What remains open

For the existing matter-conversion preparation route, weak coupling alone does not improve the steady output in this closure. A genuinely different next route would require an explicit coherent drive or another preparation interaction, including its energy source, coupling, depletion and competing processes. Such a drive is not present in this calculation and has not been experimentally established by the repository.

The scripts and manifest in run/ preserve the input widths, numerical range, tolerances and actual execution. The new kinetic equations are analytically self-reviewed and numerically checked, not newly Lean-certified. Existing formal bounds elsewhere in the repository do not certify this Markov approximation. This result narrows the proposed mechanism; it does not establish a complete cold-energy or gravity-producing device.
