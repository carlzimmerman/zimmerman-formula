# Review and finite-check record

Base checkpoint YM-C1, Git `b73311096299e2f1816be00036ccdb2922bc44d4`.

The root agent derived `SCHUR_GAP.md` and
`BARE_PROJECTOR_OBSTRUCTION.md`. The vacuum-route agent then reconstructed
the distance-to-kernel proof and the product-vacuum calculation from the
written objects. Its review agreed with the inverse-gap inequality under
the declared hypotheses and found a kernel-map error in the introductory
sentence: J maps ker S, whereas J G^{-1/2} maps ker K. This was corrected.
The operator version now also defines K through its closed form and states
the required domain, rather than treating an operator product as automatic.
This is AI-assisted mathematical review, not independent human peer review
or a formal proof certificate.

## Executed exact checks

`checks.py` checks 144 rational three-by-three block examples, including
nontrivial vacuum dressing; all principal minors of the claimed shifted
gap inequality are nonnegative. It checks the exact algebraic
counterexample to omitting the metric, six tensor-product witnesses, and
108 finite scale sums. All pass in `run_exact/`. The manifest records
actual command, source hash, environment and results. The universal
results follow from the written inequalities, not finite enumeration.

The first attempt in `run/` failed because Python integer division in
`1/d` introduced a binary floating approximation into a supposedly exact
matrix test. The corrected source explicitly converts d and scale to
SymPy rationals and asserts that the computed bound is rational. The
original failed execution record is retained and is not counted as current
evidence; its source hash is expected to differ from the corrected source.
This was an implementation error, not a counterexample to the theorem.

## Self-review coverage

Checked: actual vacuum subtraction, kernel correspondence, ordinary versus
induced metric, dimensional units, arbitrary-volume quantifiers, exact
versus illustrative running coupling, eliminated-mode assumptions,
positive spectrum versus nonzero continuum states, domain restrictions,
and the proof's Cauchy–Schwarz/min–max directions. No new Lean
formalization is asserted. No Yang–Mills block projector or interacting
coercivity estimate has been manufactured by the matrix checks.
