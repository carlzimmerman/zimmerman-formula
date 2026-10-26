# Self-audit and evidence boundaries

No independent agent review was performed. This is a bounded numerical checkpoint,
not completion of the physical research objective.

- **Neutral versus electron entrance:**all radial scattering runs have neutral
  incoming channels. Their reflection/transition matrices cannot be called DR
  probabilities. The electronic Feshbach blocks are separate clamped-R inputs.
- **Electronic self-energy versus full nuclear self-energy:**the nine electronic
  kernels cover three geometries and three incident energies. Their optical
  identity is a strong implementation check but also a consequence of the chosen
  Hermitian blocks and retarded boundary. It does not prove nuclear branching.
  The exterior truncation causes measured S differences, up to0.00755 at E0.001.
  Q coordinate/gauge maps across geometries are not yet connected to the nuclear
  eigenstates. The kernel's diagonal-width output is off-shell and basis dependent,
  not a bound-state lifetime or thermal collision coefficient.
- **Independent Hamiltonian checks:**all42 Q eigenvalues agree with Gaussian CI
  within2.2e−9. Separately, three lowest electronic energies from the new dense
  product-basis construction agree with independent PySCF singlet FCI to4.5e−11
  at the tested geometries/bases. This does not certify asymptotic completeness.
- **Projection:**symmetric finite differences with actual cross-geometry overlaps
  preserve Hermiticity and include the geometric metric. A small omitted derivative
  norm is not required for algebraic conservation; it diagnoses the danger of
  replacing projected derivative identities by complete-basis identities. Adding
  diffuse states alone leaves core derivative incompleteness and cannot establish
  convergence of all observables.
- **Boundary failure:**ideal diagonal lead runs are successful executions but
  rejected physical branching evidence. Coupled modes fix the stationary interface
  and pass analytic/cut-invariance tests. Residual domain/grid/basis dependence
  remains. Propagating modes are unit-flux normalized; their weights, not an assumed
  atomic label, are saved. A stationary end-of-domain lead is an approximation.
- **Symmetry/mass limitations:**Ag contains more than Sigma. The old run_grid JSON
  field J=0 denotes omission of centrifugal energy, not a full total-J=0 solution.
  All new streamed outputs spell this out. Full rotational terms, spin statistics,
  complete mass-polarization/recoil corrections and product threshold reconciliation
  are missing. No full angular/spin cross-section sum was performed.
- **Radiation:**2p E1 decay follows the Coulomb matrix element and is independently
  checked.2s two-photon emission is absent. The event ledger tests arbitrary
  specified events only; it supplies no DR forward/reverse coefficients and no
  radiation phase-space density from transport. A conservative bookkeeping map
  does not make an uncomputed reaction rate physical.
- **Failures preserved:**run_preflight failed because its initial environment
  lacked the isolated PySCF import path; run_preflight_env corrected the environment
  with the same immutable script. run_audit failed at JSON serialization of a NumPy
  integer after its numerical assertions; audit_v2.py fixes serialization and
  run_audit_v2 completes. No failed records were overwritten.
- **Reproducibility:**26 manifests validate locally:24 completed executions and
  two recorded failures. Local hash checks include large grids excluded from Git.
  A fresh remote clone cannot fully verify grid-dependent manifests until those
  artifacts are regenerated. This is explicit in LOCAL_ARTIFACTS.json and
  VALIDATION.md; schema validity is not advertised as physical convergence.

No galaxy-type selector, fitted collision normalization, empirical rate table,
or unitarity-defect reaction source was introduced. No successful disk selection,
physical finite-rate photon trajectory or general no-go theorem is established.
