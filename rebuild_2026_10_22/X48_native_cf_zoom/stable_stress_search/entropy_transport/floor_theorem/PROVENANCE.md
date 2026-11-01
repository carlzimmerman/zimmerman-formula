# Proof and finite-probe provenance

The phase starts from checkpoint X48-TRANSPORT-2026-11-01-B; the quantified
new target and initial observed revision are in [TARGET.md](TARGET.md).
The shared repository changes concurrently. Each proof note records its own
observed revision and exact source hashes; hashes, rather than one commit,
identify the uncommitted research operator. No physical source or coefficient
was changed in this phase.

## Mathematical records

- [preservation_route.md](preservation_route.md): source-free auxiliary
  comparison, mesh-independent smaller-prefix floor and fixed-N global ODE
  continuation. No numerical trajectory is a proof input.
- [seed_route.md](seed_route.md): source-driven auxiliary, exact fixed-N
  activation, conditional uniform source and floor, exact stress equations,
  scalar-stress obstruction and conditional small-amplitude bounds.
- [obstruction_route.md](obstruction_route.md): independent startup and
  free-surface reconstruction; no specified-data counterexample found.
- [startup_energy_route.md](startup_energy_route.md): exact square identity,
  explicit uniform homogeneous-graph barrier and the unproved nonlinear
  remainder (NE).
- [INDEPENDENT_AUDIT.md](INDEPENDENT_AUDIT.md) and
  [STARTUP_ENERGY_AUDIT.md](STARTUP_ENERGY_AUDIT.md): independent proof and
  computation review, including exact current hashes and scope restrictions.
- [LITERATURE_NOTE.md](LITERATURE_NOTE.md): bounded external-source check;
  no unverified theorem transfer is used.

The proven implications have elementary finite-dimensional ODE leaves.
Neither agreement among reviewers nor a finite run is used as a substitute
for the missing uniform startup estimate.

## Startup records and observation correction

[startup_finite](startup_finite/manifest.json) preserves the first observer
and its [contract](startup_finite_contract.json). It ran the unchanged driver
with nominal samples=81 over the entire cold-plus-warm interval. The driver
allocates samples proportionally; only two postactivation rows were retained
per grid. The contract field `samples_per_phase=81` was therefore inaccurate
as a description of actual warm observations. Its numerical interpretation
is restricted to those two rows, not an 81-point startup-window test.

[startup_finite_v2](startup_finite_v2/manifest.json), with its corrected
[contract](startup_finite_v2_contract.json) and
[driver](startup_probe_v2.py), calls the same exact cold phase with two
diagnostics to the physical activation event. It copies the zero-K handoff
into the same full-law integrator with 81 explicitly requested warm times
from activation through activation+.005. Wall and RHS budgets are shared.
No state, heat, energy or constitutive parameter is reset. The first observer
and record remain immutable; v2 corrects only the observation schedule.

All six v2 cases N=32,64,128,256,512,1024 complete. Each contains exactly
81 warm rows. The minimum sampled central-quarter C across all cases is
5.414584959511289. The largest original-energy accepted-state bound is
2.154751844772262e-10; the largest recorded sample error is
2.1676171968465496e-10. These are separate finite diagnostics and do not
bound all intervening times. Full scalar traces are in
[startup_finite_v2/result.json](startup_finite_v2/result.json).

Both records use fixed physical coefficients, Python 3.9.6, NumPy 1.26.2,
SciPy 1.11.4 and one numerical-library thread. Per-case wall cap is six
seconds; the outer bounded runner uses a 45-second wall and 40-second CPU
cap. The complete argv, code/import hashes, software, timestamps and output
hashes are stored in each manifest. There is no random sampling.

## Fresh checks

The unchanged constitutive/conservative-law and quiet-evolution tests were
rerun: all 12 pass in 0.703 seconds, recorded in
[checks/quiet_conservation_tests.txt](checks/quiet_conservation_tests.txt).
Both new and all earlier transport run manifests (26 total) validate against current
source/output hashes: [checks/manifest_validation.txt](checks/manifest_validation.txt).
Document links, syntax compilation, current note hashes and scoped diff
checks are in [checks/document_checks.json](checks/document_checks.json).
The proof target is not promoted to proved by these checks: (UC)/(NE) is
still the unproved uniform leaf.
