# Independent check of the support theorem

2026-10-09. Base checkpoint baf7e3dd46582631887fa889c6e9a12ea5362210.

The primary kinetic investigator derived the TOM translation, global orbital support restriction, edge stresses, point-source obstruction, and the b>=1 positivity proof. The lead compared these with Baes's primary-source equations and with the implemented scout. A separate agent, initially assigned the energy gate, received the precise theorem and raw identities without the first investigator's verdict and checked the positivity argument independently, including symbolic differentiation.

The second check confirmed:

- g=x^2 c and dpsi/dx=c, hence D=c^(-1)d/dx.
- The stated DU, D^2U, D^2F_0, density-slope and force-slope identities.
- The positive derivative bounds using 0<x<1, xn<1, a<2 and d<3.
- Positivity of V, DV, D^2V and the product-rule proof of rho_psipsi>0.
- gamma>1, alpha<=1, and the resulting h_psipsi>0.
- The outer derivative is an interior limit, h_psi(0)=2rho(R^-)/(Rg(R)).
- For each 0<Q<psi(0), the inversion is finite and strictly positive; its edge singularity is integrable in the density transform.

The reviewer correctly restricted this algebra to interior positivity. The lead retained the separate invariant L<=L_R cutoff proof in REPORT.md to exclude the exterior orbital branch. Agreement by agents is not a formal proof certificate; the complete elementary argument is in the report.

The lead also checked that b>=1 is a sufficient range, not a fitted or optimal threshold. The b=0.3 cases have finite numerical support only. The b=0.03 and 0.1 failures reject this anisotropy ansatz, not the underlying density law or all orbital realizations.

The energy and roundness gates were independently checked with these qualifications: heat capacities belong to thermodynamic equilibrium branches, and the scalar-pressure curl obstruction assumes smooth static nonrotating bulk matter with gravity as the only body force. Neither gate selects the RAR profile.

Numerical verification is separate: the declared parameter scout, a uniform-sphere benchmark and its boundary-term mutation, and 18 forward density reconstructions have their actual inputs, software, stdout/stderr and results pinned in runs/. No observational data, perturbation evolution, capture dynamics or covariant completion was tested.

Source scope: Baes, arXiv:2301.03873v1, equations (9)-(16), primary PDF text checked on October 9, 2026 through https://arxiv.org/pdf/2301.03873. Only the TOM inversion and truncation interpretation were imported. The paper's general consistency hypothesis was not assumed. No exhaustive novelty search was performed for the specific sufficient positivity theorem.
