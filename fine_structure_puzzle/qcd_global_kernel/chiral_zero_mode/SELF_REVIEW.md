# Self-review of the new matched continuation

Reviewed DERIVATION.md, compute_matched.py, INPUTS.json, contract.json,
SOURCES.json and the actual run_001 outputs. Existing FSP003 and sphere
files were read and hashed; no edit to them was made in this lane.

- **Ancestry:** The Haar/Dashen integral, axes, canonical Jacobian and first
  insertion were already established in FSP003. Initial dispatch overlap
  is acknowledged explicitly. New computations concern Qrep, finite-charge
  covariances, the first nonconstant-pion interaction, the aligned Gaussian
  subtraction and the S4 tadpole Laurent structure.
- **Measure/double count:** The exact factor replaces the scalar zero-mode
  Gaussian, with its mass-aligned classical vacuum exposed. The nonconstant
  correction subtracts g(3x/2+2y) if a massive determinant is used. A raw
  normalized Haar lnV term is not treated as a complete physical stress.
- **Source contraction:** Exact polynomial Wick contraction gives 3/2,
  4 and the essential +2g. The photon commutator gives Tr([Q,U][Q,U]dag)=2s.
- **Derivatives:** Numerical fixed-parameter volume/charge differences check
  both covariance terms and the third-cumulant derivatives of B. Finite
  differences are independent of the closed displayed derivative formulas.
- **UV/curvature:** The spectral pole is R/(96pi²epsilon). The zeta finite
  part is named as a prescription; independent l13,k15/source contacts and
  scheme translation remain required. No full k15 beta-function match or
  complete QCD+QED renormalization is asserted from a pion-only graph.
- **Regime:** Mathematical large-x tests do not satisfy physical epsilon
  inequalities automatically. The massless product is combined before the
  singular Gaussian limit. Same-order photon seagull, determinant, mixing,
  gauge/ghost terms and matching remain omitted.
- **Numerics:** 143 controls pass; 40/60-digit discrepancy 1.82e-36, S4
  Laurent comparison 3.95e-24. The largest recorded finite control
  discrepancy, 5.56e-15, is the expected O(y²) error in the massless Taylor
  limit T/y² at y=1e-6, within its distinct 1e-12 contract tolerance. It is
  not reported as a general derivative accuracy. No interval certification.
- **Provenance:** Run status completed; observed before/after input hashes
  agree. Manifest validator confirms current inputs. No source/alpha/LEC
  fitting, installation, Git mutation, shared-index edit or external author
  communication.

Mathematical proofreading self-review covers only this new packet. Routine
prose/notation issues: one report spelling correction; none affecting interpretation. Mathematical-token
changes after the frozen run: none. No TeX compilation is applicable to
these Markdown/plain-code artifacts. Scientific correctness qualifications
are those stated above, not a proofreading certificate for full QCD.
