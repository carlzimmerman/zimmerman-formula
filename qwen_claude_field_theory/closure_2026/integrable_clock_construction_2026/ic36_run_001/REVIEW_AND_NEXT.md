# IC36 evidence review and next calculation

Base: fef9aa6ca058522ae8e6c846f1df0fd53c86d99b.
Full original gravity goal **OPEN**. Self-review, not independent or Lean certification.

## Terminal execution and provenance

| Job | Child exit | Runner exit | Wall seconds | Meaning |
|---|---:|---:|---:|---|
| second | 2 | 1 | 88.735537 | Four scoped checks true; strict full-theory status remains OPEN |
| tests | 0 | 0 | 298.421245 | 422 tests passed; unittest elapsed 297.828 seconds |

Both manifests validated against the repository root with exit 0. Supplied
input and result hashes agree. The runner calls the scientific run failed
because of its deliberate child exit 2; that status is retained, not relabeled
as a full-theory pass. Both jobs are terminal; no live jobs remain.
Resource caps were 420 wall seconds, 2 MiB logs and one cooperative numerical
library thread per job. No hard memory, CPU affinity or per-process CPU cap.
Exact scientific, test, validation outcomes and scoped publication argv are
recorded in run_index.json; the manifests contain the authoritative argv,
software/environment versions and hashes. Publication outcome is reported in
the task handoff. This provenance is not a mathematical proof certificate.

## Result that changes the next action

The IC35 first-preservation-selected baseline does NOT pass the numerical
second-preservation test with w=wc and ell=elldot=ellddot=0. Solving the lapse
second-preservation equation leaves two homogeneous initial-data constants.
Even fitting both against the independent w equation leaves a peak residual
approximately 56.1475 and RMS 39.3344 in the script's dimensionless normalization.

This is a stronger check than imposing the same algebraic residual at each step:
the metric momenta and ordinary fluids have their action-derived accelerations.
Only the lapse acceleration is adjusted. The scientific program also derives
the second canonical fluid-density jet symbolically, including generated flux.

The failure is stable across polynomial degrees 8,12,16, constraint steps
2e-4/1e-4/5e-5 and flow differentiation steps 1e-4/5e-5. Peak residuals range
56.147315338462704 to 56.147619929196594. At step 5e-5 the independently evaluated
quadratic time curve has clock second residual 56.14587698958295, response
disagreement .0016031044536219952, and lapse second residual
.0006243762504870782. These are numerical diagnostics, not rigorous error bounds.

Both one-sided subintervals lie in sampled coefficient cell 23, with no sampled
time-kick crossings. Their peak defects are 3.8334370786860745 and
5.375104731758711, versus independent response discrepancies .002777300234635849
and .0008997336292173586. Thus the observed incompatibility is not explained
merely by fitting across a coefficient join. This is not a proof of global
coefficient regularity or an interval certificate.

## Constructive repair attempt: same action, different first-jet data

The original action, exponential kernel, vacuum-scale coefficient, and fixed
81-node coefficient table were unchanged. Vary only U1=Sdot'(2), an unused
initial datum. Fixed scans at -100,-10,10,100 did not close the equations.
The extreme scans have substantial coefficient crossings and larger finite-step
errors and are NOT certified counterexamples.

Two bounded searches selected:

| Search interval | Selected U1 | Function evaluations | Optimizer status |
|---|---:|---:|---|
| [-10,0] | -2.6400382455715268 | 14 | successful bounded minimization |
| [0,10] | 6.592102952816083 | 11 | successful bounded minimization |

An optimizer's success is NOT a field-equation pass or a universal minimum.

For the stronger, negative-U1 selection, the 65-node, degree-12 audit at
constraint step 2.5e-5 and flow step 5e-5 gives:

- initial constraint defect 7.676745998326344e-15;
- first-preservation defect 1.1920676962325018e-12;
- independently differentiated momentum-first defect 3.8011558843405335e-11;
- RMS second clock defect .10636380491772225;
- peak second clock defect .17484634861207837;
- independently evaluated peak second clock defect .17484472017170885;
- second-response disagreement 2.292083795021882e-5;
- independently evaluated lapse second defect 1.627096877777857e-5;
- activation-square range [.2453850630724225,.8607345825143933], still crossing
  both inactive and fully active plateaus.

The RMS defect is about 369.81 times smaller than baseline, but is nonzero
well above the observed resolution discrepancies. Degrees 8/12 and smaller time
steps retain the residual. Two sampled coefficient-cell crossings remain at
the smallest step; no globally C3 coefficient claim is made.

The positive-U1 selection retains RMS 1.2199814389307435 and peak
1.7824867802827384 at the finest audit. Preserve both selections and the baseline.

## Self-audit and limits

Dependency chain: IC29/30 action -> IC32 reduced constraints and fixed coefficient
-> IC33 independent metric velocities -> IC35 spatial/first-time jet
-> IC36 physical second-time jet and compatibility test.

- Passed symbolically: second ordinary-fluid density jet and the zero-gradient
  flux-coefficient cancellation.
- Numerically checked: initial/first constraints, independent momentum derivative,
  actual metric-flow differentiation, response to the solved lapse acceleration,
  manufactured compatible and incompatible equation pairs, and spatial/time
  resolution comparisons.
- Conditional: polynomial differentiation and IVP approximation; no interval
  enclosure or universal no-go theorem.
- Not addressed: nonzero finite multiplier accelerations, general initial-data
  families, moving-interface continuation, full functional Dirac closure,
  healthy clock/zero modes, PPN/measured G, causality/strong coupling, physical
  galaxy/FLRW matching, and empirical galaxy/binary/cluster/CMB requirements.

No prior failed construction was removed. No empirical data were fitted.
Mathbox computation-audit and proof-audit kept finite compatibility evidence
separate from full-theory closure. Proofreading reviewed IC36's derivation and
this review; no separate mathematical-token typo repair was needed.
Lean and lake were not found on PATH; no formal certificate is claimed.

## Next unavoidable constructive calculation

Do not simply repeat optimization of the same single initial datum. Test the
actual finite-multiplier second-preservation condition

    Wddot + eta exp(S) ellddot = 0,

allowing a finite, nonzero ellddot and the inactive-side/moving-interface
freedom that the current test suppresses. Work with the undivided equations.
A candidate is not regular merely because Wddot is small: it must vanish at
least as fast as eta at the switch.

First determine whether the remaining lapse-acceleration boundary freedom can
make Wddot and its spatial jet flat at the interface, and whether an additional
initial clock/metric/matter datum can remove the surviving compatibility shape.
If an obstruction is asserted, state the exact differentiability and coefficient
cell hypotheses; the C2 table does not justify arbitrary global differentiation.
If repaired, perform genuine mixed-branch evolution and then the original full
Dirac/stability/PPN/cosmology gates. A small second-jet residual alone is not closure.

## Development failures retained in interpretation

The first three manufactured tests failed because the implementation did not
yet exist. Later a grid endpoint recombination produced 1.9969999999999999
instead of the integrated lower endpoint 1.997; the extrapolation guard correctly
stopped the first physics pilot (exit 1). The grid now uses the exact integrated
endpoints, with a regression test; the guard was not loosened.
The flux-identity test also failed before that identity was implemented.
The full actual-collar response test was an additional audit after the pilot,
not a claimed test-first derivation of the physics.
A recording setup attempt encountered unavailable JavaScript structuredClone
before creating files or launching runs; JSON copying repaired that setup.
All decisive evidence is in the subsequently frozen run, not those development pilots.
