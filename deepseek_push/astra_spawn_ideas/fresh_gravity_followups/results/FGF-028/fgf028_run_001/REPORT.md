# FGF-028: three derived outer rows identify the finite target

Using the inherited cached ZW1215 geometry, pressure basis/support, mask and
FFT beam convention, all twelve old response rows reproduce **bitwise exactly**.
The new rings [2,3), [3,4), [4,5) contain respectively 13,036, 18,240 and
23,474 usable pixels, with mask one throughout each ring. These are additional
averages from the same map, not independent instruments.

Every single new row and every pair leaves the target unidentified in the
fixed-offset finite linear family. All three together identify it and the
fifteen pressure coefficients. Exact rational tests of the stored computed
rows give the residual matrix D approximately

    [1.2018595409,     2.5239984314,     2.3067365053]
    [0.0006616944,     1.3297209594,     4.1162708338]
    [0.0000000113,     0.0004025734,     1.5296380707].

The raw residual matrix has condition number **22.8807**; row-normalizing it
gives **15.7705**. The full fifteen-column pressure response has condition
number **1445.0255**. Raw response rows are Compton-y per normalized pressure
coefficient; row normalization is a separately reported convention. Full exact
rank is compatible with these finite conditioning values and does not establish
statistical usability or physical calibration.

The exact target reconstruction has L1 gain **50.26948356** and L2 gain
**26.34915209** over the fifteen bin values. A deterministic *synthetic*
uniform perturbation budget epsilon=1e-8 y, with signs aligned to the target
weights, gives delta(dp/dx)=**5.026948356e-7**, or **13.64191447%** of the
synthetic baseline target magnitude. Exact arithmetic confirms both the L1
bound and its attainment. Epsilon is arbitrary control input, not measured
noise, calibration uncertainty or a confidence threshold. Most reconstruction
weight resides in the inner rows, despite the outer rows resolving ambiguity.

Positive controls include old-row reproduction, direct outer line-of-sight
quadrature, normalized ring weights, source-support containment and map/mask
WCS agreement at center and patch corners. Replacing the third outer row by a
duplicate of the first retains ambiguity. Each failed identifying subset has
an exact surviving target-changing null direction in the results. These are
linear-family witnesses; this run does not claim all noisy perturbed inverse
solutions satisfy pressure inequalities.

`response_rows.npz` stores the pinned old rows, reproduced inner rows, new
three rows, combined 15x15 pressure matrix, offset column, ring labels, target,
baseline and unblurred comparison. `geometry.json` records geometry, source
hashes and per-ring weight hashes. `candidate_rows.json` supplies exact
rational strings with response metadata for the reviewed FGF024 validator.
`results.json` contains all seven subset results, exact reconstruction weights,
negative-control directions, conditioning and sensitivity. The bounded run
finished in 2.672436 seconds; its manifest validates.

The response source explicitly adapts the inherited projection/convolution
arithmetic. Reproduction is not independent confirmation of the underlying
instrument model. The fiducial distance, spherical pressure basis, hard outer
support, flat-sky convolution, transfer cutoff, fixed-zero offset and shared
map covariance remain assumptions or unquantified limitations. No actual-map
pressure fit or gradient measurement is made.

Next, test whether the apparent identification and target weights survive a
justified change in outer support or response construction, and authenticate
the transfer/calibration/covariance needed for a measured gradient. Distinguish
those structural/model tests from estimating pressure using actual map values.
No MOND force, mass discrepancy, metric/photon coupling or theory closure has
been inferred. Any later source calculation retains both a0 normalizations,
separate vacuum/H histories and separate Q/RAR/registered M laws.
