# Nonlinear resonance correction to the optical-preparation route

2026-10-13. This changes the interpretation of the preceding optical-drive and three-mode reports. Their fixed-frequency linear population estimates omit an amplitude-dependent resonance shift that exceeds the matter linewidth at all three illustrated excitation fractions. A stable linear three-mode state is not sufficient evidence for maintaining those populations with an unretuned pump.

The previous goal turn made progress by calculating pump backreaction. This turn tests a different omitted effect, rather than repeating that stability scan. The full cold-energy objective remains incomplete.

## Fixed-charge reduction

Optical conversion exchanges one source for two daughters and conserves Q=|psi|²+2|b|². Removing the common charge phase gives a canonical complex relative amplitude z=X+iY with p=|z|² and daughter density Q-2p. The homogeneous Hamiltonian is

\[
H=\delta p+\kappa(Q-2p)^2+2c_3(Q-2p)X.
\]

Apart from a constant, with d=delta-4 kappa Q,

\[
H=d(X^2+Y^2)+4\kappa(X^2+Y^2)^2+2c_3QX-4c_3X(X^2+Y^2).
\]

Hamilton's equations are dot X=(partial H/partial Y)/2 and dot Y=-(partial H/partial X)/2. This reduction retains the daughter depletion associated with the coherent excitation; fixing daughter density independently while increasing the source population would miss that energy cost.

Use n=delta=1, kappa=x/4 and c3=sqrt(epsilon x)/2 in the calculation. At the stationary background X=B=-c3/(1-u), Y=0, choose Q=1+2B². Here x=2/7, epsilon=10⁻⁴, and u is the earlier stationary chemical-potential root. The linear frequency is 0.7143737073, reproducing the previous Bogoliubov result.

## Action-frequency calculation

Writing X=B+xi, the quadratic Hamiltonian is a xi²+b Y², where

\[
a=d+24\kappa B^2-12c_3B,\qquad b=d+8\kappa B^2-4c_3B,
\quad \omega_0=\sqrt{ab}.
\]

The cubic part is C xi(xi²+Y²), with C=16 kappa B-4c3; the quartic part is 4 kappa(xi²+Y²)². Set sx=(b/a)^(1/4), sy=1/sx and xi=sx sqrt(I) cos(theta), Y=sy sqrt(I) sin(theta). I is the canonical action, equal to the phase-space area divided by pi in these variables. The cubic and quartic angular coefficients f and g obey

\[
\langle g\rangle=4\kappa\left[\frac38(s_x^4+s_y^4)+\frac14s_x^2s_y^2\right],
\quad
\langle f^2\rangle=\frac{C^2}{16}(5s_x^6+2s_x^4s_y^2+s_x^2s_y^4).
\]

Eliminating the zero-average cubic term by a near-identity canonical transformation gives

\[
H_{\rm normal}=\omega_0 I+
\left[\langle g\rangle-\frac{3\langle f^2\rangle}{2\omega_0}\right]I^2+O(I^3),
\]
\[
\omega(I)=\omega_0+\nu I+O(I^2),\qquad
\nu=2\langle g\rangle-\frac{3\langle f^2\rangle}{\omega_0}
\simeq0.57095831.
\]

As an independent numerical check, four periodic orbits measure the period and action integral directly at actions approximately 10⁻⁶, 9×10⁻⁶, 10⁻⁴ and 9×10⁻⁴. Their frequency shifts agree with the leading coefficient. Tightening the integration tolerance by ten changes the second orbit's estimated coefficient by less than 5×10⁻¹⁰. Energy drift remains below 8×10⁻¹⁵. In the zero-mixing limit the exact Hamiltonian gives nu=8 kappa=2x, a separate normalization check.

## Consequence for a fixed-frequency pump

Restoring delta=5 eV, and writing eta=I/n, the pair-resonance shift is approximately delta nu eta. The earlier total decay width is 164.7375 s⁻¹, corresponding to an intensity linewidth of 26.2188 Hz in pair-frequency detuning.

| Desired eta | Estimated pair-frequency shift | Shift / full linewidth | Actual eta at the old unshifted pump and old drive |
|---:|---:|---:|---:|
| 10⁻¹² | 690 Hz | 26.3 | 6.95 × 10⁻¹⁴ |
| 10⁻⁹ | 690 kHz | 2.63 × 10⁴ | 7.12 × 10⁻¹³ |
| 10⁻⁶ | 690 MHz | 2.63 × 10⁷ | 7.12 × 10⁻¹² |

These tiny-action shifts follow the leading normal form, not a direct floating-point subtraction of optical frequencies at eta=10⁻¹². The expansion is checked against the finite orbits; no rigorous remainder bound is supplied.

For the reduced nonlinear driven oscillator,

\[
\dot\alpha=-[\Gamma/2+i(\Delta_0+\nu_{\rm phys}|\alpha|^2)]\alpha-iF,
\]

stationarity gives F²=N[(Gamma/2)²+(Delta0+nu_phys N)²]. If Delta0=0 and the old linear calculation predicted Nlin, define r=N/Nlin and C=nu_phys Nlin/Gamma. Then

\[
r(1+4C^2r^2)=1.
\]

The table solves that equation; a nonlinear time integration independently reproduces its smallest-C example with population error below 9×10⁻¹². The shift reaches half the linewidth already at eta approximately 1.90×10⁻¹⁴.

Retuning Delta0=-nu_phys Ntarget removes this detuning at a chosen target in the reduced oscillator. It does not demonstrate that the target can be reached from the ground state with a fixed pump: ramping, capture, hysteresis, noise and optical backreaction still need analysis. At the exactly compensated target the two real local oscillator eigenvalues are -Gamma/2, but this local fact does not prove global capture or full spatial stability. A frequency-tracking mechanism is therefore a new explicit requirement of the optical-preparation route.

## Static standing-wave response

The same optical invariant modulates c3 in space. At the standing-wave wavenumber q=omega0 sqrt(delta/m), the static real-amplitude response at fixed chemical potential is

\[
\begin{pmatrix}q^2/2+x&2c_3\\2c_3&q^2/4+1-u\end{pmatrix}
\begin{pmatrix}s\\t\end{pmatrix}
=-\begin{pmatrix}2B\\1\end{pmatrix}\delta c_3.
\]

The fractional daughter-density modulation is 2s. At the *previous* drive strengths it ranges from about 2.27×10⁻²¹ to 2.27×10⁻¹⁸. The leading bare-gap change from that density modulation is below 3×10⁻⁵ linewidths. This is not a full static gap calculation: direct mixing corrections and the spatial mode problem remain omitted. The drive matching here sets the near-unit photon vertex to one, a roughly 10⁻⁴ relative approximation.

These small static estimates apply to the previous intensities. Trying to overcome nonlinear detuning by increasing intensity without retuning multiplies the static perturbation too; the table does not authorize extrapolating the static response unchanged to that stronger drive.

## Interpretation and evidence

The important correction is the population-induced shift, not a demonstrated large static density force. The previous exchange-symmetry stability result remains a correct statement about its resonant three-mode equations, but its physical application now requires nonlinear frequency compensation. No gravity enhancement follows.

The scripts, copied widths, bounded-run contract and manifest preserve the actual numerical evidence. This new normal-form derivation is analytically self-reviewed and numerically cross-checked, not Lean-certified. The photon portal, dense material preparation, confinement and full driven spatial dynamics remain unresolved. The next useful calculation is a compensated frequency ramp with capture tested from the unexcited state, followed by its sensitivity to errors; prescribing a final resonance is not itself a preparation protocol.
