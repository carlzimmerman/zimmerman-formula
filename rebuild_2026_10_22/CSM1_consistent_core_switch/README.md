# CSM1 — corrected core and switch

**The core/switch mismatch is corrected without an additional fitted number.
The previous joint calibration pass does not survive at L=3.75, 3.9 or 4.0,
or in the single predeclared refit of L.**
At the three primary levels, SPARC, the 63-group grade and all 15 cluster
keys in both h cells still pass; isolated lensing fails on both footings.

The old switch used a concentration coefficient evaluated at L, while the
actual halo core used Lq(M). The corrected selector compares the very same
mass-dependent unfloored column used by the parent core with its own floor.
There is no independently fitted T. The [model](MODEL.md) states the equation,
pipeline scopes and inherited assumptions; the [frozen contract](FROZEN_CRITERIA.md)
sets the experiment and unchanged cuts.

At L=3.75, the canonical/background-A X43 crossover moves from the old
constant-coefficient log10(T/Msun)≈12.236 to ≈11.223. Consequently many isolated
lenses use the halo branch: 62 of 127 positively weighted stellar-grid support
nodes, versus none at the single refit challenge. Their full-covariance chi2 rises by 415.28 relative
to the law-plus-two-halo comparison, against the allowed increase of 9.
At L=3.9 and 4.0 the increases are 420.31 and 423.23. The corrected model still
beats its corresponding pure-halo comparison; it fails the other required
lensing comparison. Both comparisons remain mandatory.

The single predeclared L-only challenge uses the old canonical/background-A
target log10(T/Msun)=12.3 and applies that same L to all cores and branches.
It is a refit of the existing L, not a new parameter or a blind prediction.
Its definition-corrected value is **2.5090648745652686**. An initial run used
displayed rather than imported full-precision a0, yielding 2.5090595510216196;
that 2.12-ppm implementation error and its outputs are retained. Repeating
the actual definition gives the same scientific verdict: lensing passes,
but canonical groups fail at Z=+2.621919809. Canonical SPARC and clusters pass.
The alternate footing fails SPARC, the MW V+K criterion and dwarf classes.

| L | Canonical SPARC | Canonical group Z | Clusters | Lensing delta-chi2 vs law | Joint calibration |
|---:|---|---:|---|---:|---|
|3.75|pass|+1.9319|pass|+415.2810 — fail|fail|
|3.9|pass|+1.8920|pass|+420.3064 — fail|fail|
|4.0|pass|+1.8666|pass|+423.2343 — fail|fail|
|2.5090648745652686|pass|+2.6219 — fail|pass|0.0000 — pass|fail|

Cluster grades cover all 15 keys in both h cells; SPARC covers both
backgrounds. The primary BS1 basin extension is used here; the own-mass
SPARC comparison gives the same pass/fail outcomes. Full signed summary scores for
both footings, both SPARC scopes, dwarf classes, MW counts and scatter rules
are in [scores.csv](reconciliation_001/scores.csv) and
[results.json](reconciliation_001/results.json). The individual 175-cell MW
grids are in the [primary heldout result](heldout/run_006_final/results.json)
and [challenge result](heldout/run_011_challenge_actual_floor/results.json).

The finite result cannot exclude all canonical L. No monotonicity of the
observational chi2 or group Z has been established, and changing a branch can
produce a jump. The [independent feasibility audit](feasibility/README.md)
gives the restricted scalar bounds and explains why they do not close that
remaining interval.

There is a stronger result for the fixed alternate-footing dwarf construction:
the 31 MW ultra-faint members share one Local Group flag and have L-independent
profiles within each branch. The two exhaustive possibilities give Z=-2.775
(halo) and +4.874 (law); both fail |Z|<2. Thus **no positive L rescues that
particular alternate-footing class** without changing another fixed assumption.
This does not exclude every theory with that a0. See the
[two-state audit](feasibility/PROOF_AUDIT.md).

The canonical five dwarf-class medians pass at the three registered levels.
The background-A MW has 10/12/13 of 175 baryonic-box cells passing the inherited
V+K criterion; only L=3.9 and 4.0 have background-A cells also passing the
outer-rotation criterion. Background B has 9/11/12 V+K cells; its all-four
criterion first passes at L=4.0.
The fixed McMillan point still fails. Individual satellite scatter and IC1613's
field S3 failure remain visible; class medians are not a statement that every
dwarf passes. No new temperature, inclination or hot-gas repair is included.

## Evidence and reproduction

- [Calibration sources and controls](calibration/README.md) cover both SPARC backgrounds,
  groups, both cluster h cells and full-covariance lensing, on both footings.
- [MW/dwarf report](heldout/README.md) covers the primary BS1 Local Group mass,
  exact baseline reconstruction, all 175 cells and individual residuals.
- [Independent feasibility review](feasibility/README.md) checks scalar columns,
  activation bounds, fixed-profile restrictions and proof scope.
- [Coordinator reconciliation](reconcile.py) recomputes observational cuts and
  MW counts from completed primitives. Its
  [criteria](RECONCILIATION_CRITERIA.md) are separate from scientific success.
  The [completed manifest](reconciliation_001/manifest.json) pins all five
  scientific result files and their manifests; **141/141 arithmetic, coverage,
  replay and implementation checks pass** while the scientific grades fail.

Old calibration and BS1 baselines must reproduce before interpretation.
The corrected actual-flag mutations must fail an independent selector check;
they change scientific predictions as well. Numerical-table differences are
reported rather than replaced by fitted offsets. Each authoritative run has
input/output hashes, command, controls, resource record and a validated
manifest. Historical scorer self-tests whose expected result presumes the old
branch or gas budget are retained and explicitly distinguished from controls
applicable to this corrected model.

Kappa=1/2 remains fitted, basin selection remains a posit, and the collapse
recipe/backgrounds remain conditional inputs. This correction is not a field
equation or a first-principles derivation of all model parameters. Historical
lanes and running NL1 jobs are preserved. A native simulation yielding L near
4 would not by itself restore the lost corrected lensing pass. Work is local;
no commit or push.
