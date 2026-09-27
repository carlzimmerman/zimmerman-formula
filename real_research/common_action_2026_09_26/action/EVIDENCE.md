# CD26-4 action evidence and acceptance record

Assigned and final observed Git HEAD:
`ecffd2af3623ff3e32318234fd51e1fac50b9126`. Work began with other dirty
research artifacts present. This lane made no commit and writes only under
`real_research/common_action_2026_09_26/action/`. No earlier source or
campaign artifact was edited.

The final definitions are `FINAL_ACTION.md` (CA4-GNC, exponential carrier)
and `PERSPECTIVE_VARIANT.md` (CA4-GNC-P, perspective carrier, positive V0,
bare Lambda zero). The latter changes the exact Z source from density to
density/t. The older `ACTION_REPORT.md` and `MAIN_ACTION.md` retain the
unprojected and weighted-gate trials; their passes are not pooled into a
claim that those earlier actions are healthy. The final GNC ramp is the
explicit C4 polynomial, matching the assembly/evolution controls. A smooth
bump appeared only in an intermediate prose draft and is not the final
definition or the source of the polynomial derivative bound.

## Executed checks

All four runs completed with exit code zero under the computation-audit
runner. Each has its own contract, unchanged input script, result JSON,
stdout/stderr, and SHA-256 manifest. The computation-audit manifest
validator accepted all four records. This validates the evidence structure
and recorded execution, not the physical interpretation.

| Run | Checks | Tested scope |
|---|---:|---|
| `run1/` | 46 | L361 weak bridge, physical lapse rewrite, reciprocity, exponential source, density-composed negative control, heat Frechet finite difference |
| `revised_run1/` | 28 | Corrected host normalization, four-row scalar determinant and elimination, leading Phi/Psi, exact projected source/measure variations, weighted gate first variations |
| `compensated_run1/` | 24 | Geometric gate and fixed compensator first variations, formal static reciprocal matrix, independent algebra check of evolution's Q/D parametrization, centered-K lapse and momentum |
| `perspective_run1/` | 22 | Distinct perspective action Legendre/source/energy identities, joint momentum/t Hessian, exact two-cell projector, homogeneous floor stress and nonzero susceptibility |

There are 120 passed bounded checks across distinct scopes and variants;
this is not a count of independent physical theorems. Symbolic equalities
are exact SymPy simplifications. Stated inequalities additionally require
the explicit positive-domain hypotheses in the reports. The finite
controls use declared meshes/differences; there is no random sampling.

Selected finite-difference discrepancies in the original runs:

- Heat Frechet control: `2.0565910086034478e-12`.
- Weighted gate U/lapse first variations:
  `3.642461332553637e-12`, `4.0162650982722425e-11`.
- Projector Z/lapse/volume first variations:
  `3.604883058727637e-11`, `1.2863043963307064e-11`,
  `6.922018513932926e-12`.

These discrepancies support the stated finite discretizations; continuum
variation identities are also derived analytically. The illustrative
`ell=.04` long-wave factors `1.0203040506070808` and `1.0101010101010102`
are changed predictions, not observationally fitted values.

## Independent review and dependencies

The transport reviewer independently checked the final heat/U/Z equations,
mean terms, centered trace, five-field normalization/current, compensator,
formal static matrix and frozen bound. Their corrections were adopted:
global full-on is impossible on the compact theta-positive leaf; GN is
the high-k normalization; general transition no-slip does not follow from
the leading static expansion; a positive perspective floor changes linear
source susceptibility even after homogeneous vacuum subtraction.

The evolution lane independently derives the frozen principal GNC block
and reports the exponential two-cell reduced kinetic counterexample in
`../evolution/CP_AND_CARRIER.md`. Our Q/D checks verify its algebraic
translation rather than independently deriving all curved-background
vertices. The earlier weighted gate's UV lapse failure is preserved.

Root's `../assembly/CANONICAL_AUXILIARY.md` proves fixed-data exponential
constraint existence/uniqueness; it does not imply joint kinetic positivity.
Root's `../assembly/PERSPECTIVE_REPAIR.md` gives the stronger positive-floor
perspective barrier and fixed-data smooth constraint proof. The action lane
independently checked the Legendre/source/Hessian identities, read that
barrier proof, and accepts it under its smooth compact fixed-data hypotheses.
Its regularization, elliptic compactness and bootstrapping are analytic
arguments, not proved by our symbolic checks.

No Lean source was created in this lane. Lean results owned by assembly,
evolution and transport retain their own declarations, logs and scope;
none is a formal proof of the entire common action or global evolution.

## Scope that must remain explicit

- The exact globally ungated filtered-MOND target is modified by the new
  gate and its interfaces. All prior observational passes require new runs.
- The exponential action has no automatic reduced kinetic positivity from
  its auxiliary convexity. The perspective action repairs that specific
  canonical block while changing its finite-amplitude source.
- The strict V0 floor adds nonzero perturbative susceptibility and a declared
  vacuum scale. It does not derive the observed vacuum value or an abundance.
- Fixed-lapse U convexity, fixed-data Z existence and frozen principal signs
  are separate results. Their simultaneous constraints, full Dirac count,
  lapse/clock/metric preservation and global-in-time evolution remain open.
- The classical fields do not require a particle interpretation. They still
  carry canonical initial data, charge and stress; no hidden abundance is
  removed by naming them fields.

`source_provenance.json` records the exact reviewed source hashes and the
run artifacts. `completion_record.json` records final report hashes and
the verified check counts. No universal closure or novelty claim is made.
