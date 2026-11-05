# Action continuation checkpoint, 2026-11-05

Owner: resume SY1 controls and continue calculations toward an action. Other
chat owns FN6/AZ43; no changes made there. No push, downloads or adoption.
Kappa=1/2 FITTED. A complete healthy action has NOT been established.

## Completed work

AC1_canonical_portal follows AZ40. Exact homogeneous attraction, conditional
all-angle PN kinetic/spectral algebra,24 coupled finite-box radial backgrounds,
and radial static-energy mesh checks were executed. They support specified
subproblems, not full action health. An exact branch argument shows that an
independent geodesic clock can still develop a caustic on the regular scalar/dust
FRW solution. Changing only the independent dark-energy sector cannot remove
that branch. Proof and restrictions: AC1_canonical_portal/EXACT_CLOCK_OBSTRUCTION.md.

AC2_single_clock is a new explicit candidate: the canonical dark-energy scalar
itself defines the clock; the stiffness is smooth and unswitched. There is no
independent tau or separate norm-penalty sector. Its scalar-only FRW quadratic
action is derived with lapse/shift/P constraints eliminated and passes the
stated positive-kinetic/gradient tests. Frozen-background phase/group speeds
are <=c; this is not a retarded-causality proof.36 numerical fixtures corroborate
the algebra. Candidate and next obligations: AC2_single_clock/ACTION.md.

Evidence under each lane's evidence/ directory has v2 manifests and correct
per-run input contracts under release_contracts/. Seven successful records and
two deliberately preserved unsuccessful records: the original coarse clock
finite-difference check and the AC2 incorrect count assertion. Refined/corrected
runs are separate. Early local diagnostics remain on disk, ignored by git;
they are not the authoritative evidence metadata.

## Next discriminating action calculation

For AC2 derive the complete coupled matter/scalar cosmological perturbations
and constraint rank; the first result omitted matter perturbations. Then solve
its own single-clock sourced backgrounds, test X>0 preservation and nonlinear
regularity, and regrade static/lensing/PPN gates because the stiffness changed.
AC1 two-field radial outputs, old v3s passes and FN6 Gaussian-filter passes do
not transfer. This is an open route, not a closed or failed whole theory.

The next worker should begin at the committed AC2 action and its frozen
criteria, inspect the full scalar-only ADM derivation and its limits, and freeze
new matter-coupled tests before numerical grading. No new coefficient is fixed
by the successful algebra; xi, beta/potential choice and Lstar remain premises.

## SY1

All166 searches reached1500 iterations; planted and strict mutation checks pass.
Scrambled Stage1 counts444/97 remain a warning against interpreting training
hits as a law. Stage1/Stage2 grading of200 candidates per arm is complete:
161 per arm pass canonical G5, zero pass alternate G5. Two completed Stage3
candidates reject on both footings; remaining full acceptance is pending.
See ../rebuild_2026_10_22/SY1_free_constant_law_search/CONTROL_RESULTS_2026-11-05.md.
The export stall was fixed and checkpoint progress verified. L1/CB1 holds remain
unchanged. At 10:31 Eastern the user requested more Mac calculations: the
original SY1 real --stage3 reader was relaunched detached, nice10, one BLAS
thread, PID25895. It repeats the two previously completed candidates and then
continues the canonical survivors within the existing200-per-arm cap. See
../rebuild_2026_10_22/SY1_free_constant_law_search/acceptance_resume_2026_11_05/
for the launch record, pre-run input snapshots and live log. Launch is not
completion. A leftover temporary debugging probe PID8257 was discovered and
stopped; the earlier statement that no job remained running was too broad.

## AC3 coupled matter gradient continuation

AC3_matter_gradients/RESULT.md resolves the finite-positive-Lstar FRW UV
principal scalar block: squared speeds are F_Y/Rm and
 epsilon_phi/[epsilon_phi+2/(H Lstar)^2], both positive and <=1 under the
stated matter assumptions.81 high-precision fixtures and exact ADM identities
pass. This applies to both P=0 single-clock portals and does not fix kappa.
A full frozen finite-wavelength canonical-matter check finds8 of81 negative
slow roots, all with |omega|<H. They require evolving-background integration;
no physical stability or instability verdict is inferred from those roots.
Original symbolic comparison failure, determinant timeout and unpacking bug
are retained in separate evidence records. Time-dependent equations are
written in RESULT.md; integration remains outstanding.
