# Gravity and coherent-pole checks

This package establishes conditional local scalar vacua and pole comparisons,
not a complete cold-matter history or a predicted cosmological constant.

- `run_001`: same-family finite scalar vacuum at old mu=1.8170662e7GeV,
  epsilon=.000301904468915, X/mu=25.3990254000381. All eight neutral scalar
  eigenvalues positive;21/29 finite-table convergence and tiny net-V check pass.
- `run_candidate001`: mu=2e6GeV,e=.003,epsilon=.0249201741496 at the same X.
  Eight finite-action scalar eigenvalues remain positive: phase10.8769MeV,
  radial43.4811MeV, two modulus scalars129.487MeV and four heavy singlets
  near154.919TeV. The residual is adjusted, not selected.
- The finite local potential and the exported leading global profile have
  different minima (about.0029 in X/mu). That difference exceeds a.001
  diagnostic pole offset. No finite physical resonance verdict may mix them.
- `run_leading001` instead re-solves the *leading rigid-valley trajectory
  action itself* at the tree pole. epsilon=.0248616322541. Dense force data
  and local derivatives remove a coarse interpolation alignment error.
- `run_stability001` checks the full mixed four-real X/modulus Hessian of
  that leading action, including both Schur complements. All eigenvalues
  are positive. This is separate from full heavy-normal quantum stability.
- `run_bound001` and `run_medium001` integrate the analytic fixed-pole matrix
  bounds in POLE_BOUND.md. The vacuum coefficient is15741.99984 mu^-2;
  removing every fermionic exit raises the bound to97360.19096 mu^-2 because
  the bosonic width matrix is still strictly positive. At the original
  protected scale these envelopes fail after capture; the earliest ideal
  blocked comparison is allowed. Neither is a model-wide exclusion.
- `run_api001`: rank-one production shortcut agrees with24 full4x4 inversions;
  positive symmetric split-angular pair kernels pass a12/32-node check.
  This is a stationary fixed-coefficient Breit-Wigner kernel. Its locality
  on an oscillating background requires the separate transport review.
- `run_continuation001`: a favorable all-future pole comparison from the
  completed matched-leading32-bin NWA endpoint. Its inputs and restrictions
  are explicit; it cannot turn that endpoint into an actual physical history.
- `run_continuation002`: the same favorable comparison from the completed
  late finite-width hybrid endpoint. Even with all fermionic exits blocked,
  this fixed pole leaves at least about42 times the charged allowance.

The pole ensemble assumes factorized, gauge-covariant one-particle populations,
giving equipartition in the irreducible (3,2) representation. Arbitrary pair
correlations, bound states and a full medium collision action are not included.
Independent review is in ../independent_review/REVIEW.md; the full mixed-Hessian
concern there has its own checked addendum. Finite threshold shifts/widths,
parent occupations, daughter forces and quantum currents remain distinct leaves.
