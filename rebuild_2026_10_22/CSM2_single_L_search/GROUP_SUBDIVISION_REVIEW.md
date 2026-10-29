# First two fixed group mesh tiles fail the necessary cut

The separately frozen group_subdivision_001 evaluates exactly[2.62,2.63] and
[2.63,2.64], using outward hulls of exact decimal and binary64 endpoints.
Both tiles stay on the compact halo branch for all189cells. Their bounds are:

| L tile | Z enclosure | Z derivative enclosure |
| --- | --- | --- |
| 2.62–2.63 | [2.284559831278903,2.372118251034955] | [-.645238251423879,-.290582771579373] |
| 2.63–2.64 | [2.280304225351651,2.367238879272811] | [-.640419191694933,-.289985858727584] |

Each tile directly fails the unchanged absZ<2 necessary cut throughout.
The derivative signs are additional scoped results, not substitutes for cut
bounds. Changing residual variance and systematic mass slope are propagated,
using actual binary64 .10 and .02. Original units, X43 native EPS/CLASS and
positive3000-node quadrature remain unchanged. No new physical fit, relaxed
cut, alternative estimator, adapted endpoint or modified historical input.

Both tiles pass16run+13independent review controls, and the batch passes2
controls. Runtime271.192seconds under wall600/CPU480 with one numerical thread.
Independent70digit review checks378root signs and189branch signs per tile,
nine admissible midpoint-coefficient normalized-root full-quadrature velocities
and Richardson derivatives per tile, all radial decisions, finite/outward
arrays, and full changing-statistic recomposition. Before/after hashes are
stable; tile bounds fit the prior broad-region boxes. The bounded manifest
validates. The code adapts the pinned reviewed regional implementation only
for declared numerical endpoints, input contract and correct containment
comparison; both original and adapting source are hashed. No analytic scope
upgrade to original floating libm/solver behavior is claimed.

GROUP_MESH_INVENTORY.json contains89explicit entries. Tiles0,1and88 have
reviewed direct failures (88 reuses prior local evidence);86tiles remain
pending. No failure over[2.62,3.5001] as a whole, globalL obstruction or full
passing witness follows. Prior broad-box INCONCLUSIVE evidence is retained.
GROUP_MESH_CONTINUATION.md freezes the next route to tiles2and3 with the same
mesh and rules. No completed unchanged tile should be rerun.

Native seed4 also completed: unchanged primary c_f14.4959394876 and
L_proxy9.1112209981,995particles inside the selected crossing,1180steps.
Eight copied finals pass72completion checks. measurement_006_eight passes5
controls and exactly reproduces all seven prior seeds. Only6remains pending.
These are per-seed primary proxies, not an ensemble/convergence/robust derivedL
claim or corrected linked-T pass; first-crossing/binning instability is retained.
