# Fixed group mesh tiles14and15: direct necessary failures

Frozen criteria precede the unchanged directed computation. Exact decimal
mesh tiles14[2.76,2.77] and15[2.77,2.78] include outward hulls of decimal and
binary64 endpoints. No adaptive node selection, physical fit, independent T,
cut relaxation, estimator change or historical-input edit was introduced.
The only implementation changes from batch007 are declared endpoints,
contract/criteria, coverage count and immutable provenance dependencies.

| L tile | Z enclosure, rounded outward | Z derivative enclosure, rounded outward |
| --- | --- | --- |
| [2.76,2.77] | [2.2269037543,2.3063202705] | [-0.5830521536,-0.2817661710] |
| [2.77,2.78] | [2.2229376199,2.3018180199] | [-0.5790109050,-0.2811063415] |

Both directly fail the unchanged absZ<2 necessary cut throughout. The negative
derivative is a separate local finding; no extrapolation is used. Positive
3000node quadrature and all189original-unit X43 native EPS/CLASS cells retain
halo membership and certified compact roots. Binary64 alpha=.10/delta=.02,
full changing residual variance and systematic mass slope remain unchanged.

Both16run+13independent review controls and2batch controls pass. The70digit
review checks378root signs and189branches per tile, every radial truncation,
nine admissible midpoint-coefficient normalized-root full-quadrature velocities
and Richardson derivatives, symbolic Z derivative and full statistic bounds.
Finite/outward checks and containment in the published broad boxes pass.
Before/after source/input hashes are stable. One-thread main runtime259.943s
within wall600/CPU480; manifest validates. Reviewer limits CPU120/wall150 per
tile are separate. No job/follower was altered; no completed native or legacy
NL1 run was repeated. Existing SciPy/source limitations of the separate native
point test remain recorded in NATIVE_CORRECTED_POINT_REVIEW.md.

Six exact Fraction coverage/hash/mutation controls reconcile the reviewed
first16tiles without gaps: direct necessary group failure holds for canonical
analytic fixed-native-EPS/quadrature L[2.62,2.78], lowerZ>=2.2229376199.
The union reads its own frozen inventory snapshot; older input/result/review
hashes remain unchanged. Missing tile, raised cut and an introduced endpoint
gap are rejected. Canonical inventory now has17of89tiles reviewed (0..15 plus
prior88),72pending. Every hole remains explicit; the broad unsplit-box result
remains INCONCLUSIVE. This is no global or original floating/libm/optimizer
continuum certificate and no full-model passing witness.

Reproduce into a new directory: science Python launch_group_mesh_008.py NEW_DIR;
review_group_mesh_008.py14 and15 read the immutable canonical output paths.
reconcile_mesh_008_union.py checks the frozen completed inventory. Use one
numerical thread. Never overwrite these completed evidence files.
Next GROUP_MESH_009_ROUTE.md requires separately frozen criteria/resources for
fixed tiles16[2.78,2.79] and17[2.79,2.80]. Actual corrected nativeL4.8646 and
legacy NL1 validation are already complete failures; robust derivedL and the
continuous research target remain OPEN.
