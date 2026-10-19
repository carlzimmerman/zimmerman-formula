# FSP-006 proton/Compton checkpoint

The route has a new evaluated quantity: an alpha-free, dimensionless finite-window connected proton subtraction stencil from published QCD data,

\[
K_p^{sub,conn,window}=-876375/152571904=-0.005744012999929529.
\]

It is not a complete physical proton derivative. The original individual-proton matching obstruction has been sharpened to a specific nonperturbative sea-current covariance, rather than only an unnamed baryon low-energy constant. The whole proton route remains open.

## Evaluated result and input audit

[Can et al., arXiv:2501.08619v2](https://arxiv.org/abs/2501.08619v2), Tables I-III, supplies the six S1 values used. This is a pure-QCD, SU(3)-symmetric, Nf=2+1 ensemble with pion mass about 410 MeV. It differentiates valence propagators only; its Figure 2 Types I-II omit the determinant response. The published extraction uses plateau/Feynman-Hellmann fits and a leading lattice-artefact correction with QCD renormalization/scalar-charge inputs. Our algebraic transformation makes no new fit and imports no numerical alpha.

The native momenta, N_L=48 and aM=.3860 suffice. No physical scale setting enters K_p. The rounded GeV momenta and lattice spacing in INPUTS.json are unused contextual values. This is consequently a conditional QCD ensemble result, not physical-point matching or a no-input choice of quark masses. See DERIVATION.md for spin normalization, sign and the exact pi cancellation.

The finite stencil is fully specified; no claim is made that six points resolve a continuum integral. A covariance-agnostic standard-deviation ceiling from published marginal errors is .00218094, conditional on fixed aM, with no interpolation, continuum, omitted-topology or mass-matching error bound. It must not be presented as K_p plus/minus a total theory error.

## Strongest physical-point source and why it does not finish D_p

[Fu et al., arXiv:2411.03141v2](https://arxiv.org/abs/2411.03141v2), equations (13)-(19),(24)-(25), uses near-physical domain-wall ensembles and an alternative imaginary-energy subtraction point. Its optimized individual-proton result combines QCD correlators with experimental electric polarizability, anomalous moment and radius. Dividing its displayed alpha factor out cannot erase those experimental calibrations. Its tabulated electromagnetic self-energy is only the cutoff-dependent isovector subtraction contribution, not the individual proton self-energy or its counterterm-completed derivative. These different subtraction points also prevent identifying its function directly with Can's S1.

Its description includes connected and disconnected diagrams, but a complete physical-flavor contraction inventory was not authenticated here. The cited predecessor [Fu et al., arXiv:2202.01472v1](https://arxiv.org/abs/2202.01472v1), section V/Figure 4, explicitly omits two topologies using their cancellation in the SU(3) limit. That cancellation alone is insufficient at physical unequal strange/light masses. Numbering of diagram types differs between papers. This is an audit limitation, not a claim that the 2025 calculation necessarily retains the same omissions.

## Explicit independent observable

For degenerate u,d,s propagators, Tr Q=0 but Tr Q^2=2/3. Therefore the two-current insertion on a single sea loop survives the charge sum. Its covariance with the proton two-point function survives vacuum subtraction; see DERIVATION.md, section 4. It is equal for proton and neutron at isospin symmetry, and hence absent from p-n. The nonperturbative covariance is not numerically supplied by the chosen table and its amplitude is not proved nonzero. This precisely identifies what an all-sea calculation must add.

The continuum current product also requires quark scalar and gluonic counterterms. [Gasser et al., arXiv:1506.06747v3](https://arxiv.org/abs/1506.06747v3), corrected equations (56)-(57),(64), pins those structures. DERIVATION.md gives the fixed-MS-bar insertion and the scheme transformation. A proton mass used to set the QCD scale creates an additional retuning path; it is not permission to drop this derivative from R.

## Computation and reproducibility

Command (project root):

    python3 fine_structure_puzzle/qcd_physical_matching/proton_compton/compute_response.py --inputs fine_structure_puzzle/qcd_physical_matching/proton_compton/INPUTS.json --output <fresh-run>/result.json

Executed with the installed computation-audit bounded runner and COMPUTATION_CONTRACT.json. run_001/manifest.json has status `completed` and validates against current inputs. Exact rational arithmetic checks segment versus nodal quadrature, constant/linear integrands, sea charge traces, and an independent floating evaluation of the original Cottingham prefactor. Source Table III was also visually checked in PDF page 14. The result is **implementation and finite assertion verified in the stated range**, with the source extraction and physical interpretation limitations above. This run does not reproduce the source's underlying lattice correlator extraction.

INPUTS.json SHA-256: `6b9a73c8acb4c4420b9134112a738aeb2f84ee37ff6b45c677b75146646740fd`.

SOURCE_RECEIPTS.json records exact versions, temporary PDF/text paths, hashes, checked locators and verdicts. Full texts are not copied into these evidence files. No prior evidence or navigation was modified, and no Git mutation, dependency install or large job was performed.

## Concrete continuation

The next bounded source-dependent calculation is a full flavor/topology audit and acquisition of the unoptimized pure-lattice proton H_munu data and covariance from the near-physical calculation. That would permit a new photon-kernel convolution without inserting measured polarizability. It still requires all contraction classes, controlled Q=0 and large-time treatment, the ultraviolet tail and scalar/gluonic matching in one declared renormalization path. [Feng and Jin, arXiv:1812.09817v1](https://arxiv.org/abs/1812.09817v1), equations (1)-(7), supplies a concrete infinite-volume reconstruction route for stable-QCD-state self-energies. The available table does not contain those inputs. No new external lattice job is claimed or launched.

The present result evaluates a nonperturbative proton data functional and isolates a missing observable. It supplies neither A_rho, a full physical D_p, R(alpha), nor an alpha root.
