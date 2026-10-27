# An explicit charged messenger fixes one contribution to the photon coupling

2026-10-13. This replaces an arbitrary polarizability coefficient with a matched coefficient in a specified hypothetical extension. It does not discover a particle in data or complete the cold-energy mechanism. The extension produces the required operator but does not solve the weak cooling rate in the tested benchmarks.

## Specified extension

Add a complex scalar S with unit electric charge and zero carrier-global charge:

\[
\Delta\mathcal L=|D_\mu S|^2-M_S^2|S|^2-h|\Phi|^2|S|^2-\lambda_S|S|^4,
\quad D_\mu=\partial_\mu+ieA_\mu.
\]

Take h>=0 and lambda_S>0, so these displayed additions do not destabilize the classical potential. This is a renormalizable QED-level interaction sector. It is not a full Standard Model/electroweak embedding or an all-scale ultraviolet completion. Other symmetry-allowed counterterms and couplings must be specified for a complete theory. In particular it does not by itself match the separate chi*Phi²F² conversion operator or determine all source-field couplings. There is no evidence here that S exists, and no collider, cosmological or precision-constraint audit has been performed. Benchmark masses are therefore not claimed to be experimentally allowed.

In a slowly varying carrier background y=|Phi|², the messenger mass is M_S²(y)=M_S²+h y. Integrating out S at one loop produces the field-dependent photon threshold. Subtract its background-independent part and canonically normalize the photon at y=0:

\[
\Delta\mathcal L_{F^2}=\frac{\alpha}{48\pi}
\log\left(1+\frac{h|\Phi|^2}{M_S^2}\right)F_{\mu\nu}F^{\mu\nu}.
\]

With the existing convention L_eff=-C_phi |Phi|²F²,

\[
\boxed{C_\phi=-\frac{\alpha h}{48\pi M_S^2}.}
\]

This is the leading contribution of this messenger sector. The sign follows the stated kinetic-term and threshold convention; production/cooling event rates depend on its square. Higher powers in the logarithm, derivative terms and higher loops are omitted when retaining only C_phi. Require h|Phi|² << M_S², external invariant momenta much smaller than M_S², perturbative couplings and a controlled electromagnetic background. Near a messenger threshold, the local contact formula must be replaced by the momentum-dependent amplitude.

## Normalization and source check

For one unit-charge complex scalar, beta(e)=e³/(48 pi²). This is Eq. (2.11) in [Dunne, Gies and Schubert, hep-th/0210240v1](https://arxiv.org/pdf/hep-th/0210240). The source authenticates the scalar-QED beta coefficient, not the proposed carrier or its phenomenology. Keeping the high-scale coupling fixed gives

\[
\Delta(1/e_{\rm low}^2)=-\frac{1}{48\pi^2}
\log\frac{M_S^2(y)}{M_S^2(0)}.
\]

Multiplying by -1/4 in the inverse-coupling photon convention and restoring the canonically normalized field yields the positive logarithm above. The script independently checks the coefficient through this running-coupling route and the derivative of the threshold logarithm. It also checks the scalar vacuum-polarization parameter weight integral and three finite proper-time logarithms.

## The same messenger changes the scalar potential

In the stated MS-bar convention the complex messenger contributes

\[
V_1(y)=\frac{(M_S^2+h y)^2}{32\pi^2}
\left[\log\frac{M_S^2+h y}{Q^2}-\frac32\right].
\]

At Q=M_S its quadratic threshold contribution is

\[
\delta m_\Phi^2=-\frac{hM_S^2}{16\pi^2}.
\]

This contribution is scheme dependent and is compensated by the renormalized mass parameter to obtain the physical carrier mass. Its magnitude is a hierarchy/naturalness diagnostic, not an observed mass shift, a proof of instability or an experimental exclusion. It shows why adding a messenger also requires specifying scalar-sector matching, rather than changing only the photon coupling.

## Conditional benchmarks

Set h=1, electric charge one, alpha=1/137.035999084 and physical carrier mass m=1 MeV. Use the previous leading single-particle cooling formula for a prescribed 1 eV photon bath.

| Messenger mass | C_phi (eV^-2) | Absolute mass threshold / m² | Cooling rate per J/m³ (s^-1) |
|---:|---:|---:|---:|
| 10 MeV | -4.8392e-19 | 0.6333 | 5.7931e-41 |
| 100 MeV | -4.8392e-21 | 63.33 | 5.7931e-45 |
| 1 GeV | -4.8392e-23 | 6333 | 5.7931e-49 |
| 100 GeV | -4.8392e-27 | 6.333e7 | 5.7931e-57 |

The photon-production invariant s approximately 4m² divided by M_S² ranges from 0.04 down to 4e-10 across this table. These ratios screen a derivative expansion; they are not exact finite-momentum error estimates. The first benchmark is less deeply decoupled than the others. None is a physical operating point validated against experiment or a generated laboratory inventory.

A larger messenger mass suppresses C_phi as M_S^-2 and the displayed cooling rate as M_S^-4. This simple weakly coupled example makes the photon interaction calculable but does not make it effective for cooling. Reducing M_S toward the carrier scale abandons the heavy-messenger expansion and demands a full amplitude and an experimental constraint analysis.

## Research state

Seven checks pass, with manifest-pinned code and outputs. No new Lean certification is claimed for the loop matching. The goal remains open. We now have one explicit microscopic origin for the contact operator, rather than a free number, but it adds an unobserved charged particle and leaves production yield, capture, cooling efficiency, the source portal and medium assembly unresolved. The result is a conditional model construction, not confirmation of cold energy or a gravity/propulsion mechanism.
