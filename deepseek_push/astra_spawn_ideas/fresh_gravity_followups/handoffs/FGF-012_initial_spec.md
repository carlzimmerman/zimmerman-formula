# FGF-012: Audit independent cluster-catalog measurements

Status: `awaiting_parent_review`. Lane: `cluster_audit`. Parent: accepted Astra stage 3.

Read `../FRAMEWORK_AND_EXECUTION.md` and `../RESULT_CONTRACT.json`. This is a bounded research task, not an accepted result. The framework instructions are mandatory.

## Target

After the cluster observable agent returns, independently test positional matching, aperture conventions and information independence of its new local catalog comparison.

## Equations

- Compare gas masses only at matched physical/angular apertures with declared distance conventions.
- Marginal catalog intervals are not a joint covariance or automatically independent of hydrostatic inputs.

## Domain

Exactly the returned matched objects and local FITS/catalog files; preserve unmatched objects and predeclared matching gates. Q/R/M and both scale histories only where the source/force computation is justified.

## Steps

1. Pin final catalog file hashes and selected row identities.
2. Recompute sky separation/redshift/aperture alignment and trace which observations are shared across reductions.
3. Re-evaluate the conditional nuisance requirement under available marginal bounds without assigning an unsupported confidence level.

## Decisive controls

- A nearest catalog neighbor outside the declared gate is not a match.
- Integrated SZ information cannot silently become an independent resolved pressure profile.

## Acceptance scope

A reproducible match/independence audit and explicit missing measurement list; retain negative or inconclusive results.

## Required sources

- Repository-relative: `campaign_fresh_gravity_astra/stage_03/cluster_precision/REPORT.md`
- Repository-relative: `campaign_fresh_gravity_astra/stage_03/cluster_precision/DERIVATION.md`

## Execution and return

Claim this task before launch. Write only the unique assigned `results/FGF-012/<run_id>/` directory. Return the required result contract, raw derivation and actual evidence. Each numerical process is bounded to 120 seconds; record actual enforcement. Failed controls remain visible. Worker success is not orchestrator acceptance.

## Dispatch blockers

- Final stage_04/cluster_observables artifacts, raw source list and intake review must be pinned before dispatch.
