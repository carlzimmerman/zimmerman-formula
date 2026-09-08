# IC6 continuation: independent mathematical audit record

Base `0b75e72bf5797e451beb258847ade528cd9c4551`, 2026-09-08.
The unchanged target is all thirteen requirements in `../FRIED_CHICKEN_SPEC.md`.
**The complete theory remains OPEN.** No empirical or global novelty claim.

Three independent work packages continue the same IC6 action: a strong
nonlinear auxiliary solve (root), a symmetry-decoupled odd tensor calculation
(`ic6_characteristics`), and actual full-metric homogeneous Dirac flow
(`ic6_dirac_flow`). The separate reviewer `ic6_strong_review` received raw
claims, proofs and definitions and was asked to reconstruct the critical
steps. Agent agreement is not a formal mathematical certificate.

## Strong auxiliary theorem

Reviewed final report SHA256:
`79740e6befefd82e54dadc64ca2635caf92e4f0c81e94ca0e9f3df63c20b8ca0`.

The independent verdict was **proved as written at the explicitly local,
instantaneous scope**. The reviewer reconstructed the map between the
stated Sobolev spaces, witness root, Fourier inverse, contraction,
smooth bootstrap, density normalization, bracket domains and multiplier
signs. Extra exact checks returned zero for both witness auxiliary
residuals, reduced scalar mass (162/\mathcal T), and mixing ratio
(9/\mathcal T). The nine tests passed independently using Python 3.9.6,
SymPy 1.14.0 and NumPy 1.26.2; central recorded runs use the environment in
their manifests, not these reviewer versions.

Two useful clarifications were made and re-reviewed:

- (L=D_q(C_s,C_t)) in the density bracket is unnormalized; the normalized
  strong-map derivative is (L/(m e^{-1/2}h_0^2)), so (K=VL).
- The local six-dimensional reduced phase density is a generic formal
  count. Global translation stabilizers occur at the witness and some
  nonuniform seeds, and cannot be silently counted as independent gauge
  directions in a finite homogeneous truncation.

The reviewer independently authenticated the Simon source and its exact
Schauder hypotheses. The manuscript states the proof-as-exercise limitation
of that source and gives the difference-quotient application explicitly.
Neither the external source nor the project proof was built in Lean.

## Odd tensor sector

The reviewer independently derived the transverse two-by-two metric
geometry, retaining background shear and spatial anisotropy. The
((-,-)) reflection representation contains only the cross metric mode
and its first-order momentum. Its scalar, clock and shift linear responses
therefore vanish by symmetry, not by assigning auxiliary coefficients.
The common action-derived derivative coefficient is (mJ_0/2).

The safe conclusion is a positive kinetic coefficient and physical-null
principal cone for that one polarization on the stated diagonal
((t,z))-dependent background class, subject to the regular branch and
on-shell-background assumptions. Nearby actual Bianchi I backgrounds are
available; nonlinear inhomogeneous time evolution is not proved by this
calculation. Lower-order anisotropic terms remain and do not justify
claiming complete finite-time stability.

The independent check also confirms the full varied-(F) Hessian term.
The remaining even-sector problem cannot freeze (F), the trace, lapse
or (u), or borrow the odd mode's characteristic.

## Dirac flow

The reviewer checked the continuum invariant metric derivatives, curvature
adjoint, explicit secondary drift and smeared secondary bracket. The
numerical program uses all six metric components, including the conjugate
(2\pi^{ij}) factors for independent off-diagonal entries. Its Poisson
matrix is obtained as the constraint Jacobian times the canonical matrix
times the transposed Jacobian. Rank, singular values, multipliers and
preservation defects are calculated from that matrix.

Only the initial state is projected onto the two auxiliary equations.
The subsequent numerical trajectory evolves them with the derived
multipliers; every intermediate Runge–Kutta stage is checked for branch
membership. Endpoint refinement and internal-stage errors are reported
separately. This corroborates the finite homogeneous flow, not an
inhomogeneous field-theory DOF count or continuum evolution theorem.

The report's concluding next-step wording was reconciled with the strong
companion: strong local solvability and a common smooth domain are now
supplied, but derivative-loss control and persistence under the coupled
time-dependent PDE are not.

## Review limits

### Completed even check and explicit IC7 continuation

The even calculation subsequently included the actual background derivatives
and a separate compact-Lagrangian variation with lapse, auxiliary and shift
responses. Those independently constructed Hessians agree in the tested
states. Its exact trace-branch derivative proves a negative scalar quartic
coefficient on IC6 solutions arbitrarily close to the witness; it is not
merely a numerical suspicious pole. The witness benchmark still passes.

The root then constructed the explicit IC7 curvature-square coefficient in
IC7_CURVATURE_SQUARE.md. Both independent reviewers reconstructed the
two-by-two Schur elimination, the h_tau/12 term, factor 1/8, barred-volume
factors and covariant measure. A review caught the singular inverse at zero
trace momentum: an explicit smooth determinant-domain cutoff and zero
extension were implemented, with a dedicated singular-static test. Exact
witness derivatives establish that this addition leaves its quadratic action
unchanged. The new correction is a phase-action term; its nonlinear compact
Lagrangian is not obtained by reusing the old momentum solution.

This repairs the isotropic quartic coefficient on the specified open regular
plateau, not the sheared-background antisymmetric mixing. No prior IC6
inhomogeneous characteristic theorem is silently assigned to IC7. The
central frozen-input manifests record final files and bounded tests; this
audit records independent reasoning, not an automatic proof certificate.

No review establishes PPN coefficients, galactic lensing, baryon-only
quasistatic matching, transition health, a controlled exact zero-field
branch, realistic cosmology, or the proposed acceleration-scale relation
from first principles. Those original requirements remain mandatory.
