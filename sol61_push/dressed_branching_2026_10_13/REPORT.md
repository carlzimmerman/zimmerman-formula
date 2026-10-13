# Dressed competing decay closes the previous bright benchmark

2026-10-13. Conditional calculation within the same proposed two-field model. This is theoretical evidence, not empirical evidence.

The previously unresolved competing process is now calculated at zero temperature, at tree level, in a homogeneous condensate. At the previous optical benchmark, the gapped excitation decays into two lower-branch matter excitations at **164.7375 s⁻¹**, versus a proposed photon partial width **4.9015653 × 10⁻¹² s⁻¹**. The two-channel radiative branching fraction is **2.97538 × 10⁻¹⁴**. Including other positive decay channels could only reduce this fraction within a partial-width treatment.

Thus the previous 0.787 W per source-equivalent kg was an initial radiative power conditional on an excited population, not a sustained or efficiently produced glow. The population's calculated lifetime is approximately **6.07 milliseconds**. For a single prepared population with no replenishment or inverse reactions, its integrated radiated energy is only about **0.0048 J per source-equivalent kg**. Matter decay dominates this benchmark. This is not an exclusion of every possible parameter choice or mechanism.

## Hamiltonian and mode conventions

Use the canonical nonrelativistic Hamiltonian density

\[
\mathcal H=\frac{|\nabla\psi|^2}{2m}+\frac{|\nabla b|^2}{2M}
+\delta|b|^2+c_3(b^*\psi^2+b\psi^{*2})+\kappa|\psi|^4.
\]

Expand about the stationary state from the preceding condensate-emission package: daughter amplitude \(\sqrt n\), source amplitude \(B=-c_3n/(\delta-2\mu)\). Work in the rotating frame of the conserved charge. Set \(x=4\kappa n/\delta\), \(\epsilon=c_3^2/(\kappa\delta)\), \(u=2\mu/\delta\), and \(q=k/\sqrt{m\delta}\). Here \(M=2m\) in the kinetic dispersion, neglecting relative corrections of order \(\delta/m\); the physical benchmark has \(\delta/m=5\times10^{-6}\).

The dimensionless quadratic Bogoliubov matrix has blocks

\[
L(q)=\begin{pmatrix}A&C&u/2&0\\C&D&0&0\\-u/2&0&-A&-C\\0&0&-C&-D\end{pmatrix},
\quad A=q^2/2+x-u/2,\quad D=q^2/4+1-u,\quad C=\sqrt{\epsilon x}.
\]

Positive-frequency eigenvectors are normalized by \(v^T\operatorname{diag}(1,1,-1,-1)v=1\). The initial state is the positive gapped mode at zero momentum. Final states are two lower-branch modes at opposite momenta. Their on-shell momentum solves \(2\omega_-(k)=\omega_g(0)\). The calculation includes the daughter and source components and their anomalous components; it does not substitute the vacuum source decay width.

## Cubic amplitude and phase space

For daughter fluctuation \(a\) and source fluctuation \(\beta\), the cubic Hamiltonian is

\[
\mathcal H_3=c_3(\beta^*a^2+\beta a^{*2})
+2\kappa\sqrt n(a^*a^2+a^{*2}a).
\]

The amplitude \(\mathcal A\) is the coefficient of one initial-mode annihilation and two specified final-mode creations after the canonical Bogoliubov substitution. Both terms and their interference are retained. The code obtains that coefficient by summing the six assignments of the three external legs. An independent SymPy polynomial coefficient extraction checks it at the optical benchmark.

With canonical nonrelativistic state normalization, the identical-final-particle factor gives

\[
\Gamma_{g\to--}=\frac{2\pi}{2!}\int\frac{d^3k}{(2\pi)^3}
|\mathcal A(k)|^2\delta(\omega_g-2\omega_-(k))
=\frac{k_*^2|\mathcal A(k_*)|^2}{4\pi|d\omega_-/dk|_{k_*}}.
\]

This formula assumes a simple isotropic on-shell root. Each computed root is checked for energy conservation. The group velocity is evaluated by the Bogoliubov metric form of Hellmann–Feynman and cross-checked against a centered numerical derivative.

Writing \(\mathcal A=(\delta/\sqrt n)\widetilde{\mathcal A}\), and \(v=d(\omega_-/\delta)/dq\), the physical natural-unit width is

\[
\Gamma_{g\to--}=\frac{m^{3/2}\delta^{5/2}}{n}
\frac{q_*^2|\widetilde{\mathcal A}|^2}{4\pi|v|}.
\]

Divide by \(\hbar\) to obtain s⁻¹. In the dilute unmixed limit the vertex is \(2c_3\), so the result reduces to

\[
\Gamma_{\rm vacuum,NR}=\frac{c_3^2m^{3/2}\sqrt\delta}{\pi}.
\]

This matches the nonrelativistic limit of the earlier relativistic vacuum width. At the test point \(x=10^{-6},\epsilon=10^{-4}\), the computed width divided by this vacuum expression is 1.0000010.

## Bounded results and interpretation

The run covers 20 combinations: \(\epsilon\in\{10^{-8},10^{-6},10^{-4},10^{-2}\}\) and \(x\in\{0.001,0.1,2/7,1/3,0.8\}\). No vanishing decay amplitude occurs in this tested set. This is not a universal no-cancellation theorem or a complete momentum stability scan.

At \(x=2/7,\epsilon=10^{-4}\), the dressed matter width is **1.218746 times** the nonrelativistic vacuum width: the condensate does not suppress the competing channel at this benchmark. The physical inputs are \(m=1\) MeV, \(\delta=5\) eV, \(\lambda_{\rm tot}=10^{-6}\), \(\kappa=\lambda_{\rm tot}/(4m^2)\), \(\Lambda=10M\), and photon-portal coefficient \(\zeta=1\). The photon width is recomputed from the preceding proposed portal, including its homogeneous mode correction.

A remaining conditional escape is to reduce \(\epsilon\). In the weak-mixing regime at fixed density and contact coupling, this matter width scales approximately as \(\epsilon\), while the hypothetical photon width approaches a nonzero limit. Extrapolating the observed weak-mixing behavior puts comparable widths around \(\epsilon\sim3\times10^{-18}\). That value is outside the numerical scan, and is a scaling estimate, not a tested point. The corresponding photon lifetime is about 6,500 years; comparable matter and photon widths would give about half that total lifetime. The photon portal is an independent stipulated interaction, so weakening \(c_3\) does not logically forbid radiation, but neither supplies the missing source-excitation preparation mechanism. The former matter-conversion route becomes correspondingly weaker.

## Evidence and remaining work

`check.py`, `contract.json`, and `run/` contain the reproducible calculation and bounded-run provenance. Checks include symplectic normalization and eigenpair residuals, the on-shell root, analytic-versus-finite-difference group velocity, independent cubic coefficient extraction, vacuum vertex normalization, and the dilute-width limit. This is self-reviewed numerical evidence. The new decay amplitude is **not Lean certified**; the earlier Lean proofs concern only interaction-energy algebra and a polynomial emission bound.

This calculation resolves the leading zero-temperature competing channel for the stated model and regime. It does not give a full finite-temperature spectral function, inverse-reaction kinetics, finite-cloud optical transport, assembly, confinement or a new gravity law. The next useful discriminator is a preparation-and-energy-budget calculation for the ultraweak-conversion regime, or a specifically justified additional interaction that changes the competing spectrum. Increasing the condensate density alone has not supplied that mechanism.
