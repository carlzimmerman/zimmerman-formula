# Review of the QCD zero-mode packet

Coverage: all newly created raw derivations, report, contracts, source
translations and the two implemented finite experiments. This is an author
self-review; the coordinator separately checked the pure-QCD Haar normalization,
canonical measure Jacobian and Ward relation from the raw derivation.
The electromagnetic raw derivation was saved before reading the coordinator's
independently saved candidate; the two agree after changing disk coordinates.

Mathematical checks:

- The SU2 exponent is z a0 with z=2m Sigma V cos(theta/2); normalized
  Haar gives 2I1(z)/z, not I1(z)/z. The source's factor1/2 is translated
  as a parameter-independent normalization.
- The common degenerate mass derivative includes both flavors; the displayed
  condensate divides it by2. This agrees with the source's flavor-averaged
  definition after translating its extra1/Nf convention.
- Positive winding probabilities and the topological variance interpretation
  apply at theta0. No positivity of chi at arbitrary theta is assumed.
- The fixed-topology zero-mode pole is posterior-weighted before taking
  the small-mass limit; no single nonzero winding sector is substituted
  for the full QCD partition function.
- The canonical constant-mode coefficient is q0=F sqrt(V)phi. Its eigenvalue
  is positive Mpi^2 at positive mass; it is not called a zero eigenvalue.
- The same Jacobian cancels the Haar-saddle3/(2V), and is not added a second
  time to a full canonical pion determinant.
- Direct Pauli algebra gives TrQUQUdag=5/9-s, with the physical charge
  difference equal to1. Euclidean action sign, removed constant, and
  charged mass shift2e4^2 C/F^2 agree with the authenticated operator.
- The disk marginal is uniform in s in[0,1], giving the independent
  disk/Bessel integral. First charge derivatives hold Sigma,F,C and the
  degenerate renormalized mass path fixed at this leading insertion.
- Volume derivatives vary both mu and t. Treating t as volume-independent
  in the metric derivative would miss the charged-pair cancellation.
- The exact Ward relation with the Dashen insertion is scoped to this
  retained action. Photon determinants, anomalous electromagnetic sectors,
  mass renormalization paths and higher operators are not silently included.
- Mathematical large-mu tests are distinguished from the epsilon-regime
  physical domain and from fixed-positive-mass small-H limits.

Computation checks: pure-QCD `run_001` completed with325 controls/precision
at100/130digits; QED `qed_run_002` completed with105 controls/precision
at80/110digits. Both completed manifests validate against current inputs.
The first QED run remains a recorded CPU-cap failure; no inputs/code were
changed between that resource-limited run and the successful rerun.

Proofreading: reviewed the complete new report and display integration.
Routine edits: none remaining. Mathematical-token changes in final
proofreading: none. Substantive scope limits are kept in the report, not
resolved by changing conventions. No unresolved local notation issue found.
