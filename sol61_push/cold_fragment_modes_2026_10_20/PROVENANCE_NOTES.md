# Preserved failures and annotation corrections

The two tight finite-r_min profile attempts, run_001 and run_002, remain
failed. The first exhausted its 8000-node cap; a warm-start and 24000-node
repair still did not achieve the requested collocation tolerance. No Hessian
evidence is accepted from either. True-origin regular singular BVP profiles
in profile_origin/run_001 achieve the unchanged 1e-8 tolerance, and reproduce
the earlier energies. This resolves the working route without asserting a
complete diagnosis of every collocation refinement failure.

The original grid_run_001/natural_run_001 did not pin ARPACK's default start
vector. Their historical contracts label randomness unused. New deterministic
v2 scripts and run_002 records pin an analytic start vector. Preserve both
generations; see ARPACK_INITIALIZATION_NOTE.md. Rerunning for this provenance
repair does not provide independent physical confirmation.

The human-readable `mathematics.inputs` label in the deterministic radiation
contract/manifest says natural_run001. This is a stale annotation: its exact
command, execution_artifacts and before/after hashes explicitly use
**natural_run_002**. The current primary result uses those deterministic
v2 cache bytes. Do not change a pinned manifest to hide the label defect.

The outgoing library's opening shorthand includes sqrt(2) beside complex
perturbation names. The operative canonical order used by the code, derivation
and cache is (u,s,xi,v,t_X), where sqrt(2) has already been absorbed in those
canonical complex-field perturbations. No additional sqrt(2) is applied by
the natural/DC callers. Detailed conventions are in ACTION_AND_MECHANISMS.md.

A validator accepting a failed record verifies that its failure and artifacts
are recorded consistently; it does not convert the experiment to a pass.
The outgoing red tests intentionally fail the earlier restricted boundary
implementation. Report their statuses separately from corrected green tests.
