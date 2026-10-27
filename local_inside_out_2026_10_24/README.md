# Local inside-out conversion: current result

The tested interactions do not establish a persistent converted interior
with an independently free outer reservoir. The failure is already visible
in a necessary preservation test that grants the desired density profile.
No formation success, galaxy catalogue fit, or general impossibility claim
is made. This is new effective-model research, not new observational evidence.

Starting inspected revision: f19bcf139fd7e3a219d429bdfa665ffceefd045d.
Parent inputs are copied here because other research changes the shared tree.
The earlier global-phase pump, inertia, contraction-gate and angular-transport
scans were not repeated. The new question is the spatial interface and the
outer boundary that those calculations omitted.

## Tests and results

1. **Interface cost, LIO-1.** An analytic capacity bound shows that spreading
   a constant-stiffness front to infinity cannot eliminate its cost. At
   ell30 kpc, Rin5b, q_in .95 and q_out .05, the lower costs in units
   GM_b²/b are 5.16e8 (dwarf), 5.16e4 (small disk), 1.289 (large disk),
   and .00464 (cluster). The first two radii exceed their parent cold-mass
   supply cutoff; they are illustrative interface costs, not realizable
   parent galaxies. Actual front tests use supply-admissible radii.
   These costs are not bounds on all possible assembly energy.
2. **Prepared local front, LIO-2.** Ten runs: two disk templates, ell .1,
   1,3,10,30 kpc, n128, duration100. Every run loses the converted interior.
   At inherited ell30, inner converted fractions fall below 1e-25.
   The interior extends to .9933 kpc in the small disk and15 kpc in the large
   disk, with initially free outer material beyond1.9866 and44.263 kpc.
3. **Boundary continuation, LIO-3.** The old protected no-flux branch loses
   q_inner>=.95 before the exterior is fully free. The sampled loss brackets
   in boundary strength are [7.943e-5,1e-4] and [.06310,.07943]. These are
   optimizer/threshold brackets, not certified bifurcation locations.
   A separate sufficient inequality excludes all nonzero stationary phases
   in the principal box for the small-disk discrete model at n64/128/256.
   That inequality is inconclusive for the large disk.
4. **Response-weighted stiffness, LIO-4.** A new positive interaction uses
   F(u) multiplying the gradient energy, including all its extra derivatives.
   This reduces stiffness away from the converted region without choosing a
   smaller constant ell. Four runs test two environmental radii for each
   disk. Final inner converted fractions are .0199–.0205 (small disk) and
   .00714–.00716 (large disk). None preserves the interior. These endpoints
   are still relaxing and are not claimed as exact equilibria.
5. **Alternative basin, LIO-5.** Starting all T and minimizing the same new
   energy at n64/128/256 returns nearly F in the small disk. The large disk
   instead retains an approximate stable branch: q_inner>.999999 and
   q_outer=.99809–.99813, with positive lowest Hessian eigenvalue .695–.702
   and phase-gradient residual below6.1e-7 in the stated metric. This branch
   fails the free-outer-reservoir requirement. The prepared local front
   does not enter that basin. These starts do not exhaust all possible basins.

The source-only conditional shifts after decay are about .403dex for the
small disk and .231dex for the large disk. They are not measured scatter
or full mixed-state force predictions. The density was held fixed and was
already shaped for the parent law; even passing this gate would not be a
formation result.

## What this changes

The existing barrier can protect a spatially uniform phase under a protected
boundary, yet fail once an interface to free matter is allowed. Weighting
the stiffness can restore a largely converted reservoir in one template,
but has not selected a finite converted region surrounded by free matter.
Within the tested model, the unresolved task is a physical mechanism that
holds the interface at a finite radius, together with the work to create it.
Increasing a pump or prescribing conversion by radius would not answer it.

A next candidate must identify a physical quantity that selects the front:
for example an evolved change in local kinematics or a conserved transported
quantity. It must derive the interface's restoring force and reciprocal
baryon/mass forces from the same energy, demonstrate a localized stable
state, then form it from unprepared mass with finite accounted work. Such
an interaction remains unconstructed here. This is a requirement, not a
claim that the examples will work or are unexplored throughout the repository.

## Verification and reproducibility

Each run directory contains its contract, command, input hashes, software,
stdout/stderr, results and v2 manifest. Five manifests pass the schema/hash
validator. Analytic gradient/Hessian directional checks are below4e-11 for
constant stiffness and2.6e-9 for response weighting. Maximum recorded E+Q
relative error is3.41e-7 for LIO-2 and1.75e-8 for LIO-4. Capacity quadrature
matches its exact expression to1.2e-16; the independent SI unit comparison
differs by3.2e-5 due to rounded physical constants.

Before LIO-4 production, derivative checks caught a new tail coefficient
overwriting the parent's quadrature variable. Renaming that coefficient
restored both checks; all recorded LIO-4/LIO-5 inputs hash the corrected file.
No failed diagnostic was treated as evidence for the mechanism.

Derivations and claim limits: DERIVATION.md. Exact data: run_cost,
run_local, run_continuation, run_response, run_branch. Review is self-review.
No manuscript, original experiment, or fitted kappa was changed.
