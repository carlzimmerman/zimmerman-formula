# FSP-009 common-response route C1

Owner `common_response/`; parent FSP-008, observed starting HEAD
`3ac0427149a2108afa8f102df4d82da33b9060c4`. Old science is read-only.

The full target remains A_rho(u), M_u and R=A_rho/M^3 for physical QCD,
u=e^2=4 pi alpha. This route tests a narrower proposed bridge: whether trace,
vector-current or Feynman--Hellmann identities determine the proton's
Born-subtracted two-current response from the unconditioned vacuum mixed
metric/current response, without independent proton data.

Use positive, degenerate renormalized up/down masses at u=0, arbitrary fixed
strange/heavy masses, and the SAME QCD functional. Compare the two rational
charge assignments obtained by exchanging the up/down charges. Matching,
regularization, currents, Born subtraction and metric contacts must be
covariant under this nonanomalous vector flavor relabeling. These are actual
conserved currents of the same QCD theory, not adjustable spectral functions.

Success is (i) an exact vacuum/proton comparison map including the metric
contacts and normalized external-state subtraction, and (ii) a source-checked
nonzero non-Born response in a channel killed exactly by the vacuum map,
with the complete SO(4) soft-photon angular contraction calculated separately.
No full-QCD numerical mass or vacuum coefficient is inferred from a soft
window or a chiral coefficient. A local R term is not used as an obstruction.

Nearest ancestor checks: `qcd_global_kernel/sea_flavor/DERIVATION.md`,
`qcd_physical_matching/matching_path/RAW_DERIVATION.md`,
`qcd_sea_curvature/coordinator/UV_MATCHING.md`, and
`qcd_prediction/coordinator/MIXED_CHIRAL_RAW.md`.
The old charged-pion M_u proportional to M_pi, its cross-sector shape ratio,
the zero linear-H massive-pion determinant, normalized-Hessian algebra, and
local-scale matching cancellation are inherited results, not new results here.

New bounded execution checks only finite exact charge/isospin algebra,
the source coefficient differences and two independent soft angular
contractions. The analytic symmetry proof and the external chiral expansion
carry the universal statements. Sources, code and computation contract are
saved before execution. No memory/affinity limit unsupported on macOS is used.

Remaining physical leaf even on success: the isospin-even non-Born tensor
over all momenta, its finite matching and the unconditioned sphere response
are independent unevaluated observables. Physical m_u != m_d requires an
additional scalar insertion and is outside the exact isospin-null statement.
