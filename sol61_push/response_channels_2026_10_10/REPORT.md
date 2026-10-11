# One drift law, two measurable responses

2026-10-10. Narrow research checkpoint from `edf1b5e1ae0a240c583f1d62eaf9b94a487a581a`.

**Result:** the existing two-sided drift predicts different instantaneous rates for a halo's size and its displacement. A smooth Gaussian benchmark gives a size-response rate exactly twice the centroid-return rate, with the same alpha. No extra rate is fitted. This is a consistency calculation within the proposed dynamics, not identification of cold energy or a successful merger model.

## Exact initial-response identities

Use the two-sided variant discussed in [the transport audit](../transport_clock_2026_10_10/REPORT.md):

\[
\partial_t\rho=\nabla\cdot(\alpha\rho\tau\nabla\psi),\qquad
\nabla^2\psi=4\pi G(\rho_0-\rho).
\]

The target rho0 is fixed, radial, smooth and finite-mass. The background is matched, psi0=0, with radial tau0; switches are on, caps inactive, orbital advection omitted and boundary fluxes vanish. The required moments converge. Phi0 below is sourced by the **cold target**, not by total baryon-plus-cold density. The clock tau0 may depend on total density. Its variation contributes only at second order because the background deficit force vanishes.

**Displacement.** For rho(x)=rho0(x−xi), the first-order perturbation is eta=−xi·grad rho0. Isolated Poisson inversion gives delta psi=xi·grad Phi0, with Laplacian Phi0=4 pi G rho0. Integrating continuity against x gives

\[
\dot X_i=-K_{ij}\xi_j+O(|\xi|^2),\quad
K_{ij}=\frac{\alpha}{M}\int\rho_0\tau_0\partial_i\partial_j\Phi_0\,d^3x.
\]

Spherical averaging of the Hessian replaces it by one third of its trace. Therefore, with Gamma(r)=4 pi G alpha rho0 tau0,

\[
\boxed{\gamma_X=\frac{1}{3M}\int\rho_0\Gamma\,d^3x.}
\]

**Size.** Apply a mass-conserving dilation rho_lambda(r)=lambda^−3 rho0(r/lambda), lambda=1+epsilon. Its potential scales as Phi_lambda(r)=lambda^−1 Phi0(r/lambda), hence delta psi=epsilon(Phi0+r Phi0'). The radial Poisson equation gives (delta psi)'=epsilon 4 pi G r rho0, and v_r=−epsilon Gamma(r)r. For I=integral rho r² d³x, delta I=2 epsilon I0, so

\[
\dot I=-2\epsilon\int\rho_0\Gamma r^2\,d^3x+O(\epsilon^2),\qquad
\boxed{\gamma_I=\frac{\int\rho_0\Gamma r^2\,d^3x}{\int\rho_0 r^2\,d^3x}.}
\]

These are **initial moment derivatives**, not exponential eigenmodes: in general the evolving density ceases to be a rigid translation or dilation. Size relaxation conserves mass; it is not delivery of new mass from a reservoir. The one-sided clipped deficit is not differentiable at the matched state and is outside this calculation.

## A smooth example that can be checked cheaply

Take rho0=rho_c exp(−r²/2R²) and the cold-dominated clock tau0=(4 pi G rho0)^−1/2. Set Gamma_c=alpha sqrt(4 pi G rho_c). Elementary Gaussian integrals give

\[
\gamma_X=\frac{\Gamma_c}{3}(2/3)^{3/2}
=0.181443685\,\Gamma_c,\qquad
\gamma_I=\Gamma_c(2/3)^{5/2}
=0.362887369\,\Gamma_c.
\]

Thus gamma_I/gamma_X=2. `check.py` independently integrates the **finite shifted and dilated Gaussian forces**, with the actual density-dependent mobility, rather than substituting these linear-response identities. Perturbations 0.02, 0.01 and 0.005 and two radial resolutions check the limiting rates. It also checks mass, the second moment and the zero-mass dilation perturbation. The numerical radius cutoff is 12R; no time evolution is performed. The run manifest records the exact command, bounds, source hashes and results.

The ratio is not universal. In general gamma_I/gamma_X=3 times the r²-weighted mean Gamma divided by its mass-weighted mean. Different profiles and baryonic contributions to tau change it. The Gaussian is a diagnostic target, not a derived equilibrium or the project's exponential-kernel halo.

Validation: 17 numerical assertions passed, including the unequal-clock negative control; the provenance manifest validates. A separate reader derived the centroid identity independently and checked the dilation and Gaussian reductions. This supports the stated initial-response calculation, not a claim about the full theory.

## What this changes next

Do not identify the local Gamma used in CFG597 with a whole halo's measured assembly or recentering rate. First compare its drift contribution to the moment identities above using a smooth equilibrium and small perturbations; include orbital and velocity-relaxation responses separately in the full model. A discrepant initial slope would isolate an implementation, boundary or assumption problem without a large merger rerun.

This opens a concrete way to measure distinct responses under one alpha. The factor two does **not** establish the much larger separation that might be needed observationally, repair CFG597's failed controls, or establish merger compatibility. Kinetic support, outward energy transport, profile selection, vacuum coupling, kappa=1/2 and the 32 pi squared puzzle remain unresolved. No global novelty claim is made.
