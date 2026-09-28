# FGF-010: Audit scale-field vacuum identification and backreaction

Status: `awaiting_parent_review`. Lane: `scale_audit`. Parent: accepted Astra stage 3.

Read `../FRAMEWORK_AND_EXECUTION.md` and `../RESULT_CONTRACT.json`. This is a bounded research task, not an accepted result. The framework instructions are mandatory.

## Target

After the scale agent returns, independently test whether its dynamical positive scale is compatible with the literal core vacuum relation and whether its energy exchange closes.

## Equations

- Candidate definition a=a_ref exp(chi); distinguish a_ref fixed by vacuum from any claimed pointwise a= kappa c sqrt(G rho_Lambda).
- Start from the returned action and derive chi equation and energy balance independently; do not assume the returned potential or stability verdict is correct.

## Domain

Exact local proof with explicitly declared scalar action; Q/R; constant vacuum versus separately prescribed H history. Numerical range only after the actual final candidate is pinned.

## Steps

1. Pin the finalized scale derivation, code and result hashes before review.
2. Re-derive variation and check whether a stationary homogeneous vacuum exists under each identification of rho_Lambda.
3. Construct the simplest counterexample to a universal-scale or stability statement if its hypotheses are missing.

## Decisive controls

- Treat an environmental effective a as an added model assumption, not automatically the original core law.
- A positive field-sector Hessian does not imply coupled matter stability.

## Acceptance scope

A precise audit verdict, corrected hypotheses and one decisive next task; no theory-closure claim.

## Required sources

- Repository-relative: `campaign_fresh_gravity_astra/stage_03/dynamics_precision/DERIVATION.md`
- Repository-relative: `campaign_fresh_gravity_astra/CONTRACT.md`

## Execution and return

Claim this task before launch. Write only the unique assigned `results/FGF-010/<run_id>/` directory. Return the required result contract, raw derivation and actual evidence. Each numerical process is bounded to 120 seconds; record actual enforcement. Failed controls remain visible. Worker success is not orchestrator acceptance.

## Dispatch blockers

- Final stage_04/scale_dynamics derivation/results and intake review must be pinned before this task revision is dispatched.
