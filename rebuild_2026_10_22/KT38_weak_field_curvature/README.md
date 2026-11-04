# KT38 checkpoint: no tested joint candidate

KT38 is complete for the ten recorded lengths. **No original Milky Way baryon
cell passes the four primary cuts on either acceleration footing at any tested
length.** All sampled Cassini quadrupoles pass their unchanged ceiling. The
isolated dwarf screen gives the counts below. This excludes a joint candidate
within these finite runs, not every untested length or generalized action.

The phenomenological law is `P=xQ(z)/z`, `z=x+s^2`,
`x=|g|^2/a0^2`, `s=ell^2 H:H/a0^2`, with `Q(0)=0` and the unchanged simple
response primitive. The fixed power two is a structural choice; the single
continuous parameter is a universal physical length ell. Baryons, a0 footings,
observations and cuts remain fixed. There is no Gaussian response filter.
The full action variation retains `B=2ell^2 s xR' H` and every Hessian adjoint.

| ell (kpc) | Selection | MW passes canonical / alt | Isolated dwarf passes canonical / alt |
| ---: | --- | --- | --- |
| .3 | initial | 0 / 0 | 19 / 19 |
| 1 | initial | 0 / 0 | 17 / 18 |
| 1.5 | adaptive | 0 / 0 | 17 / 17 |
| 1.75 | adaptive | 0 / 0 | 17 / 17 |
| 2 | adaptive | 0 / 0 | 16 / 17 |
| 2.25 | adaptive | 0 / 0 | 16 / 17 |
| 2.5 | adaptive | 0 / 0 | 16 / 16 |
| 3 | initial | 0 / 0 | 14 / 16 |
| 5 | initial | 0 / 0 | 13 / 14 |
| 10 | initial | 0 / 0 | 10 / 12 |

MW denominators are 1,375 original cells per footing at each length. The
strict scale-height conjunction is also zero throughout. All 27,500 saved
profiles were independently regraded; flags, counts and score summaries
match. See [MW review](mw/REVIEW.md). The original five-length run failed at
JSON serialization of an infinite fitted scale height. It remains failed,
with only its canonical profiles retained. Fresh `full_002` and `focused_001`
encode that defined diagnostic as null with an explicit reason and preserve
its failed strict cut; they omit no rows. See [provenance](mw/PROVENANCE_NOTES.md).

Every tested Solar length/footing pair passes `|Q2|<=5.2e-27 s^-2`; the largest
ratio to this ceiling is about 2.0551e-4. The calculation includes the full B
term, contacts, source-shrink limit and independent density comparison. These
are finite quadrupole predictions in a prescribed constant external field
with zero external Newtonian Hessian, not a full ephemeris analysis or an
interval certificate. See [Cassini record](cassini/README.md) and the
[independent derivation review](analytic/SOLAR_DERIVATION_REVIEW.md).

Dwarf denominators are the unchanged 24 objects, with 41 sampled Upsilon
values on [1,3]. Plain isolated QUMOND gives 19/24 on both footings. All pass
sets agree across three quadrature grids. These are isolated spherical virial
screens, **not primary satellite external-field grades**, continuous-Upsilon
exclusions or equilibrium existence results. Some 5 and 10 kpc samples have
negative local total radial gradients, including some virial-screen passes;
this is disclosed without adding a retrospective observational cut. See the
[initial](dwarfs/README.md) and [adaptive](dwarfs/CONTINUATION_README.md) records.

The checked finite energy derivative, reciprocity, Newtonian/ell=0 controls
and compatible spherical covariance support the tested implementation.
They do not establish all-background health. The uniform-field susceptibility
improvement at H=0 does not remove the negative highest-order static
contribution in certain tidal backgrounds; see the
[tidal response qualification](analytic/TIDAL_LINEAR_RESPONSE.md). The inherited
radial boundary and thin-disk convergence limitations remain material.

[RESULTS.json](RESULTS.json) contains the exact combined numbers and scopes.
[VERIFICATION.json](VERIFICATION.json) records nine valid manifests: eight
completed and the preserved serialization failure. Run
`python3 rebuild_2026_10_22/KT38_weak_field_curvature/verify.py --check`
from the repository root to revalidate source hashes, statuses and summary
arithmetic. This performs no new force solve.

The active next route is [KT39 power-curvature interpolation](../KT39_power_curvature/PLAN.md),
which explicitly introduces `z=x+s^p`. Its exponent is an additional declared
model parameter. KT38 supplies no assumed KT39 outcome.
