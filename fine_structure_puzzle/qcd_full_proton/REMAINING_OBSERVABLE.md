# FSP-011 remaining observable N0(mu0) and its acquisition requirements

**Alpha has not been derived.** This file records the single proton-side observable that remains after the FSP-011 decomposition ([DERIVATION.md](DERIVATION.md)), together with what acquiring it would require. Nothing here estimates its value.

## Definition

At first order in u = e^2, on the fixed path P, the exact identity is

    M_u^p = Born^(0) + (1/2) M_u^(p-n) + N0(mu0).

The path P holds MS-bar g_s(mu0) and m_f(mu0) fixed (f = u,d,s,c), with mu0 = 2 GeV. The missing term is

    N0(mu0) = lim_{Lambda->inf} { 1/(32 pi^3 M) int_0^{Lambda^2} dQ^2 int_{-1}^{1} dx sqrt(1-x^2)
               [ -3 T_1^(0),NB + (1-x^2) T_2^(0),NB ](iQx, Q^2) + M_u,ct^(0)(Lambda, mu0) },

with the following ingredients:

* T^(0),NB = (T^p + T^n)/2 - (T^p,B + T^n,B)/2: the spin-averaged forward two-current amplitudes of j^uds = (2 ubar gamma u - dbar gamma d - sbar gamma s)/3, minus the full Born amplitudes in the FSP-008 convention.
* All contraction classes are included: connected X and Y; same-loop W (the Tr Q^2 singlet); one-current-loop Z at O(m_s - m_l); separate-loop V at O((m_s - m_l)^2).
* M_u,ct^(0) = sum_f Q_f^2 sigma_f^(0) [3 log(mu0^2/Lambda^2) + 5/2]/(16 pi^2), using the isoscalar sigma combination, plus the gluon and charm thresholds. The charm classes reduce to these thresholds plus power corrections (DERIVATION section 4).

The coordinate-space equivalent is the Feng-Jin infinite-volume convolution of the Born-subtracted isoscalar correlator H^(0),NB_{mu mu}(x) with the Feynman-gauge photon propagator ([1812.09817v1](https://arxiv.org/abs/1812.09817v1)).

## What is known about N0, and why it is not enough

* **Soft end.** The integrand begins at Q^4 with coefficient 3(a-b)^(0)/(32 pi M), where a and b are the isoscalar static polarisabilities per e^2 (FSP-009).
* **Hard end.** At leading power the spin-0 quark-mass logarithm is cancelled by M_u,ct. The traceless twist-2 term averages to zero over O(4) directions.
* **Local UV anchor.** The leading local quark conversion at mu0 = Lambda is 0.8140 MeV per e^2 (isoscalar; 70.9% from charm). It belongs inside N0 and is not summed with any other piece.
* **Insufficient constraints.**
  * The 0.3-2 GeV region is unconstrained by these limits.
  * One moment or one subtraction-function line does not fix the integral (FSP-007, FSP-009).
  * No isovector datum at any precision fixes it (REDERIVATION R1, R2).

## What was searched (bounded; not a global absence claim)

None of the following contains N0 or its full integrand:

* **[2411.03141v2](https://arxiv.org/abs/2411.03141v2) (Fu et al., near-physical mass):** proton and neutron T_1 in figures only, with optimised curves that use experimental alpha_E, kappa and r_E; it tables only isovector self-energy pieces.
* **[2501.08619v2](https://arxiv.org/abs/2501.08619v2):** a connected S_1 line at the SU(3) point (m_pi ~ 410 MeV).
* **[2310.01168v3](https://arxiv.org/abs/2310.01168v3):** one same-loop disconnected moment, compatible with zero.
* **[2602.22379v1](https://arxiv.org/abs/2602.22379v1):** a preliminary hadronic tensor at m_pi = 223 MeV, with contraction content not stated.
* **RC* [2209.13183](https://arxiv.org/abs/2209.13183):** baryon masses with 14-20 MeV errors and no alpha=0 baryons.
* **QCDSF and BMW:** the isoscalar sea term is absorbed or cancels.
* **Experimental dispersive analyses:** isovector only; the isoscalar subtraction function is unmeasured.

## Acquisition requirements

| requirement | specification | closest existing resource |
|---|---|---|
| Theory and ensembles | Pure QCD (e=0), Nf=2+1 or 2+1+1, physical m_l and m_s, at least three lattice spacings, m_pi L >= 4, continuum and infinite-volume control | RBC/UKQCD 24D and 32Dfine (near-physical, two spacings; used by 2411.03141 and 2310.01168); ETMC cB/cC/cD (2507.20910) |
| Correlator | Nucleon four-point function <N(t_f) j_mu(x) j_nu(y) Nbar(0)> for j^uds, all mu,nu and all relative separations; proton and neutron, or the isoscalar sum | Fu et al. compute four-point functions on 24D/32Df, but publish only optimised T_1 curves and isovector self-energy tables |
| Contractions | X, Y connected; W same-loop covariance with N Nbar; Z via the split-even S_s V S_l estimator ([2301.03995v2](https://arxiv.org/abs/2301.03995v2)); V with independent noise; lattice seagull/contact terms; vacuum subtraction (FSP-008 sea_flavor eq. (5)) | W: one moment (2310.01168 Table II); Z and V: not computed |
| Normalisation | Z_V or a conserved current; nucleon two-point normalisation; ground-state isolation with explicit N pi control (2411.03141 reports a substantial N pi contribution) | standard |
| Photon kernel | Infinite-volume Feynman gauge (IVR), or QED_L with derived finite-volume corrections; a sharp-O(4) or other regulator with known matching to path P | IVR demonstrated for the pion ([2108.05311](https://arxiv.org/abs/2108.05311)) |
| Born subtraction | (T^p,B + T^n,B)/2 from G_E, G_M of p and n on the same ensembles, or from charge-normalised experimental fits | exists (NEEDS_MATRIX N1) |
| Ultraviolet | Short-distance region by OPE, matched to path P with isoscalar sigma_f and the gluon threshold; the next gluon Wilson order kept as a separate listed uncertainty | sigma_f exist; gluon matching partial |
| Path | Fixed MS-bar m_f(2 GeV), g_s(2 GeV). Alternatively any hadronic path, provided its electromagnetic quark-mass and scale shifts are reported and the vacuum A, A_u are computed on the same path | conversion formula: FSP-006 proton_compton section 5 |
| Output | N0(mu0) with full covariance and per-class breakdown (X, Y, W, Z, V); no measured polarisabilities or structure functions as inputs | none |
| Cost class | No new gauge generation for two spacings; new all-component same-loop and split-even contractions on existing ensembles. A production lattice job, not started here | - |

## Use once acquired

Adding N0 to Born^(0) + (1/2) M_u^(p-n) gives M_u^p on path P at first order. R_u still needs A, A_u and the quark-mass derivatives of A on the same path (handoff item 2). Finite-alpha dependence needs higher orders. An alpha prediction needs an independently justified selection equation.
