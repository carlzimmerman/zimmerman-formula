# FGF-014: Coupled scale-field-fluid dispersion

Status: `awaiting_audit`. This is a proposed child task from an actual returned agent result, not an executed result.

Read `../FRAMEWORK_AND_EXECUTION.md` and `../RESULT_CONTRACT.json`. Preserve the core scale, two normalizations and separate gravity branches.

## Dependencies

Required scoped reviews: FGF-010, FGF-011. Verify that they cover this task's premises; a generic PASS is insufficient. Source proposal: `campaign_fresh_gravity_astra/stage_04/scale_dynamics/NEXT_TASKS.md`, SHA256 `0dbd930ba232cb8cd118b01bb5efa25d7b7cc491b4f7f83dd19314afbae9068c`.

## Worker proposal, retained with its declared assumptions

SD1-C: coupled scale-plus-fluid instability polynomial

Conditional on acceptance of the stage-four matter lane's local background
conventions, combine its pressure fluid with SD1's two fields. At a uniform
equilibrium define D_phi=Lambda k²-K omega²/c² and
D_chi=J k²+m-J omega²/v_chi². Derive independently, including every sign,
whether the coupled density-mode polynomial is

    (D_phi D_chi-q² k_parallel²)(omega²-c_s² k²)
      +4 pi G rho0 k² D_chi = 0.

This displayed expression is a proposed starting target requiring verification,
not an additional accepted SD1 theorem. First check q=0, rho0=0 and K->0
limits against their exact reduced equations. Then determine whether a new
short-wave instability appears despite the field-only Schur bound; separate
any long-wave gravitational instability from a kinetic ghost or short-wave
ill-posedness. Use a bounded parameter grid only after deriving those limits.

Success: correct polynomial, limiting checks and scoped instability criterion.
Refutation: a sign/normalization counterexample or an unbounded short-wave
unstable branch under the declared positive kinetic/stiffness assumptions.
Do not assert that an unsupported uniform matter-plus-gravity background is an
exact global solution; use the matter lane's explicitly declared local setup.


## Return and limits

Use a unique claimed run directory under `results/FGF-014/`. Each numerical process has a 120-second wall bound and one numerical-library thread, with actual enforcement recorded. Split larger work into separately bounded runs if necessary. Return the result contract, exact derivation, controls, input/output hashes and failed attempts. No automatic theory acceptance follows from a passing finite computation.
