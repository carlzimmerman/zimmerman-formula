# FSP-003: calculate the QCD ratio and its electromagnetic response

Parent checkpoint: FSP-002; base Git 3c01aa2861bf576f4c2d942251eb9d2f89cae108, dirty shared tree. User steering, 2026-10-18 America/New_York: keep pushing the QCD route with subagents; calculate the physical ratio and its alpha dependence without fitting; seek a real prediction.

Original alpha(0) target remains unchanged. Current conditional bridge in natural units is Hbar=(8 pi G/3)c_H Lambda^3 and m_p=C_p Lambda, so R_QCD=c_H/C_p^3=3 Hbar/(8 pi G m_p^3). The framework additionally supplies a_M=kappa c sqrt(G rho_DE). The existing report does not calculate c_H. Writing observed Hbar into R is a calibration diagnostic, not a theoretical prediction.

## Required distinction

Specify the state, spacetime, regulator, vacuum subtraction and matching convention before claiming c_H. A possible operational definition is lim_(H->0+) [epsilon_QCD(H)-epsilon_QCD(0)]/(H Lambda^3), with all other physical data and the comparison prescription fixed. Check whether this limit exists and whether the source's coefficient uses this definition; metric variation and time dependence may matter. Local curvature terms, boundary dependence, finite-volume corrections and global topological response must be distinguished rather than combined into a chosen number.

The mass function and vacuum function must belong to the same theory/conventions. Quark masses may be independently measured inputs for a conditional correlation test, but no unknown coefficient may be fit to dark energy or alpha. Parameters used to define numerical simulations are not by themselves predictions; identify held-out quantities and any experimental alpha used in calibration. A known proton-neutron electromagnetic splitting is not the individual proton electromagnetic mass.

R is invariant under consistent Lambda conventions. With physical quark masses and proton mass held fixed, its electromagnetic derivative follows the constrained path in atomic_bridge/qcd_mass/CONSTRAINED_SENSITIVITY.md. A fixed-ratio derivative is a distinct question.

## Parallel obligations / write scopes

- QCD-V / vacuum_geometry: authenticate the actual topological mechanism and follow its cited controlled construction; calculate the linear-in-H coefficient where possible, or derive the exact obstruction/remaining integral. Check the hyperbolic-to-de Sitter arrow and counterterm/state freedom. Do not stop at restating that c_H was called unknown.
- QCD-E / electromagnetic: derive calculable QCD+QED/chiral contributions to c_H and C_p, including independently specified mass constraints. Seek an explicit alpha coefficient or controlled nonanalytic term; inventory genuinely unavoidable matching constants and whether they cancel in R.
- QCD-C / controlled_model: execute one controlled topological/curved-space model calculation distinguishing linear H from H^2/exponential/volume response. Use a genuine action and observable, and establish its alpha/coupling dependence. No arbitrary toy algebra with uncomputed coefficients presented as physical QCD.
- Coordinator / coordinator and reviews: independent covariance/state analysis, numerical target diagnostic separated from prediction, bridge synthesis and fresh review of any result.

Agents own only their named subdirectory. Do not mutate FSP-001, FSP-002 or other routes. Return actual input hashes, exact source versions, derivations, contracts/manifests for load-bearing computations and commands, strongest conditional result, first unresolved implication and an executable continuation.

## Success and partial progress

Success requires an independently calculated ratio/function with a specified domain, matched charges/masses/thresholds, an isolated physical alpha root and uncertainties, then adversarial review. Controlled lower-dimensional results, explicit physical contributions, a demonstrated failure of the proposed cosmological term, or a rigorous reduction to measurable correlators count as partial progress only. A finite numerical fit, assigned coefficient, naturalness guess or agreement near 137 does not.

Pursue successive substantive steps on the route while useful work remains executable. Do not repeat the existing rank/scheme-invariance algebra as the new result. Preserve failed runs and distinguish environment/implementation failures from false physics. Write only within fine_structure_puzzle/. No publication, external messages, commits or automation requested.
