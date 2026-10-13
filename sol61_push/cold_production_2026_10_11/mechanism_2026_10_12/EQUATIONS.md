# Current fermion–polarization candidate: equation index

12 October 2026. This is a hypothetical extension, not an established theory or an identification with the earlier protected scalar carrier. Natural units: hbar=k_B=1. The microscopic state, critical quadratic matching and baryonic coupling are assumptions. The acceleration normalization is unresolved.

## Microscopic Hamiltonian

\[
H(\mathbf k,\mathbf P)=\frac{k_x^2+k_y^2-k_0^2}{2m_*}\Gamma_1
+v k_z\Gamma_2+h\sum_{j=1}^3P_j\Gamma_{j+2},\qquad
\{\Gamma_i,\Gamma_j\}=2\delta_{ij}.
\]

\[
E_\pm=\pm\sqrt{[(k_x^2+k_y^2-k_0^2)/(2m_*)]^2+v^2k_z^2+h^2|\mathbf P|^2}.
\]

For filled negative bands at zero temperature and chemical potential, the leading nonanalytic energy after quadratic subtraction is

\[
V_f=\frac{\beta}{3}|\mathbf P|^3+\cdots,\qquad
\beta=\frac{Nm_*h^3}{2\pi v},\qquad N=2.
\]

## Static response and its distinct limits

\[
\mathbf D=a\nabla\phi-\mathbf P,\qquad
\nabla\cdot\mathbf D=\alpha\rho_b,\qquad
\mathbf g_s=-\alpha\nabla\phi,\qquad
\mathbf D/a=\delta F_f/\delta\mathbf P.
\]

Neglecting spatial corrections gives D/a=beta |P|P and, outside a spherical baryonic source,

\[
V_\infty^4=K M_b,\qquad
K=\frac{\alpha^3}{4\pi a^3\beta}
=\frac{\alpha^3v}{2Nm_*a^3h^3}.
\]

For an isotropic ensemble of equal-speed rings, the weak-source gapless spatial response instead gives

\[
\mathbf D/a=\eta|\nabla|\mathbf P,\qquad
\eta=\frac{Nm_*h^2\pi}{32},\qquad
V_\infty^2=\frac{\alpha^2M_b}{2\pi^2a^2\eta}.
\]

Thus V_infinity^4 is proportional to M_b^2 in that limit. In the large-gap derivative expansion,

\[
V_\infty^4\simeq K(M_b-M_{\rm offset}),\qquad
M_{\rm offset}=\frac{8\pi a A h v^2}{9\alpha},\qquad
A=\frac{Nm_*}{2\pi v}.
\]

These are separate controlled limits, not an exact interpolation through the uncomputed crossover.

## Retarded response and collective dynamics

For the isotropic gapless ensemble and 0<x=omega/(vk)<1,

\[
\Pi_R(\omega,k)=\frac{Ah^2\pi vk}{4}F(x),\quad
F(x)=\frac\pi4(1-x^2)-\frac i2[x-(1-x^2)\operatorname{atanh}x].
\]

With exp(-i omega t), modes solve

\[
(ak^2-Z\omega^2)[a^{-1}+\Pi_R(\omega,k)-I\omega^2]-k^2=0.
\]

The low-k branch has

\[
\omega=\omega_0-i\Gamma,\qquad
\omega_0^2\simeq\frac{a^2\eta}{Z}k^3,\qquad
\Gamma\simeq\frac{a^2}{2Z}\frac{Ah^2\pi}{12v^2}\omega_0^2.
\]

Positive bare a,Z,I and the specified homogeneous medium are retained assumptions; this does not certify a galaxy solution.

## Unresolved normalization

\[
K\stackrel{?}{=}G_N a_0,\qquad
a_0\stackrel{?}{=}\frac c2\sqrt{G_N\rho_{\rm DE}}.
\]

Neither equality has been derived from this Hamiltonian. No measured data are claimed to establish the proposed dark medium.

Derivations, limitations and reproducible runs: [microscopic origin](NODAL_RING_ORIGIN.md), [force limits](NODAL_FORCE_LIMITS.md), [dynamics](NODAL_DYNAMICS.md). Earlier empirical comparisons and rejected mechanisms are retained in their respective research records; failed runs remain labeled and preserved.
