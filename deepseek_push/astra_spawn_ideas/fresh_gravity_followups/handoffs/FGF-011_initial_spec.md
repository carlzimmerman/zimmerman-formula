# FGF-011: Audit matter-background consistency and rate prediction

Status: `awaiting_parent_review`. Lane: `matter_audit`. Parent: accepted Astra stage 3.

Read `../FRAMEWORK_AND_EXECUTION.md` and `../RESULT_CONTRACT.json`. This is a bounded research task, not an accepted result. The framework instructions are mandatory.

## Target

After the matter-stability agent returns, independently check its dispersion against the full first-order operator and its background assumptions.

## Equations

- Derive continuity, barotropic momentum and scalar response from the stated equations; do not import an assumed homogeneous-gravity background.
- Separate a mean-subtracted supported perturbation model from a self-consistent isolated or cosmological background.

## Domain

Use final source-pinned candidate parameter grid; audit threshold, growth rates and high-frequency behavior for Q/R, both a normalizations, K=2/8.

## Steps

1. Pin the returned derivation and computation first.
2. Check signs and the distinction between long-wave gravitational growth, negative kinetic energy and high-k ill-posedness.
3. Identify a realizable background or an explicit wavelength/time window for a local frozen-coefficient application.

## Decisive controls

- A uniform positive density plus constant field is not automatically a solution of the original Gauss law.
- Do not remove acceleration through a symmetry the preferred-frame action has not established.

## Acceptance scope

Independent scoped audit and an executable background-construction continuation, not global stability.

## Required sources

- Repository-relative: `campaign_fresh_gravity_astra/stage_03/dynamics_precision/DERIVATION.md`
- Repository-relative: `campaign_fresh_gravity_astra/stage_03/proof_precision/DYNAMICS_CROSS_REVIEW.md`

## Execution and return

Claim this task before launch. Write only the unique assigned `results/FGF-011/<run_id>/` directory. Return the required result contract, raw derivation and actual evidence. Each numerical process is bounded to 120 seconds; record actual enforcement. Failed controls remain visible. Worker success is not orchestrator acceptance.

## Dispatch blockers

- Final stage_04/matter_stability artifacts and intake review must be pinned before task dispatch.
