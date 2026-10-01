# FGF-024: one missing target functional, three free pressure coordinates

At fixed offset, the exact finite pressure model decomposes as

    g = w d + m o,
    o = (p(2.5), p(3), p(4)),
    m ≈ (-0.055054273696391466,
         -0.09447904974858899,
         -0.11532043480967945).

The exact rational w, m, inner inverse and null basis are in
numeric_001/results.json. Every outer coordinate can move the target. Their
two-dimensional plane m v=0 leaves it unchanged; all directions outside
that plane change it. This is a coordinate parameterization: inner pressure
coefficients change jointly to preserve the twelve measured bins.

For added rows C=(C_i,C_o), form R=C_o-C_i A^-1 O. The scalar target is
identified exactly iff **m is in row(R)**. This agrees with membership of
the full target row in the augmented old/new observation row space. The
validator returns exact reconstruction coefficients when this holds, or an
exact surviving target-changing null direction when it fails.

| Synthetic added rows | Target identified? | Remaining pressure nullity |
|---|---|---:|
| None | No | 3 |
| One row (0,m) | Yes | 2 |
| One row (0,(m1,-m0,0)) | No | 2 |
| Duplicate old observation | No | 3 |
| One outer-coordinate measurement | No | 2 |
| Three outer-coordinate measurements | Yes | 0 |

These rows are algebraic controls, not instrument measurements. In particular,
the useful aligned row has signed coefficients; its realizability as an
annular SZ observable has not been established. The target can be identified
without reconstructing every pressure coefficient.

The negative row also admits exact strictly positive/decreasing pressure
witnesses with gradients -3.6749006359132447e-6 and
-3.6949569683387115e-6. They preserve all old observations and that extra row.
Thus its failure is not merely a direction outside the admissible pressure
family. Necessity of the row-space criterion is asserted for the linear family
and a strict feasible interior; inequalities can produce exceptional boundary
datasets with uniqueness despite failed linear identification.

The executable candidate-row validator is `missing_functional.py`. Invoke it
with `--candidate candidate.json --output NEW_OUTPUT_DIRECTORY`, under the
bounded runner. The saved `numeric_001/synthetic_candidate_rows.json` documents
its JSON format; it is explicitly a synthetic fixture. Each proposed real row
must supply fifteen rational-string pressure coefficients, a separately
declared offset coefficient, the inherited operator hash/basis/support, and
construction metadata for annulus, mask, beam, convolution, geometry and
source hashes. Numeric_002 verifies this CLI path on the fixture.

The tool verifies coefficient algebra and presence of metadata. Its result
always has `authenticated_observation: false`: actual response construction,
source authenticity, errors and conditioning must be separately reviewed.
Incorrect support is rejected; switching the aligned row to the negative
control changes the identification verdict. Both bounded manifests validate.

Next: construct response rows for already cached additional outer annuli using
the same masks, beam, basis and support, then run this criterion. If they pass,
quantify response/conditioning uncertainty before interpreting noisy data.
No actual row construction or new data fit is included here.

No covariance, measured pressure prior, continuum bound, force or mass
discrepancy has been inferred. Later MOND calculations must preserve both a0
normalizations, separate vacuum/H histories and Q/RAR/registered M laws.
Metric/photon coupling and the full physical theory remain unresolved.
