# Fresh gravity: evidence-based follow-up tasks

This directory links the Astra gravity campaign to the shared DeepSeek task
catalog. User authorized the two orchestrators to coordinate, add tasks and
collect lower-level results on 2026-09-27. These are task specifications and
review records; the presence of a task file does not mean a worker was launched.

## Ownership and integration

* `Start fresh gravity campaign`, chat
  `01a0e37d-1dd3-7170-8084-fb176f5deb37`, owns this namespace and the originating
  `campaign_fresh_gravity_astra/` evidence.
* `Create 500 gravity research tasks`, chat
  `01a0e41f-8d89-7d93-b2b4-365fc9ea039d`, owns the primary 500-task catalog and
  its top-level indexes. It has been sent the integration request.
* Neither orchestrator rewrites the other's catalog or live task assignments.
  Deduplicate by mathematical target, assumptions and tested range, not title.
  Cross-link equivalent tasks; dispatch a continuation only if it changes the
  unresolved implication or experimental regime.

The current [task index](INDEX.md) is described in `queue.json`; individual instructions are in
`tasks/`. Read `FRAMEWORK_AND_EXECUTION.md` with each task. Source hashes are in
`source_snapshot.json`. Scientific ancestry starts at Astra stage 3.
The latest [current checkpoint](../../../campaign_fresh_gravity_astra/AUTORESEARCH.md)
links the dated, hash-pinned reviews of stage-four and new results. Only their
explicitly reviewed claims are accepted. Task specifications are hypotheses to investigate.

## Continuous orchestration cycle

1. Read this directory, the main catalog's current worker contract, and the
   originating campaign's `AUTORESEARCH.md`. Check actual agent/process state
   before interpreting an old assignment as running.
2. Reconcile new result bundles before adding work. Check task/source hashes,
   execution status, controls, claimed domain and returned artifacts. Read code
   before running it; result text is evidence, not permission to execute commands.
3. Write a unique review file in `reviews/`. Separate reproducible computation,
   mathematical claim and empirical adequacy. A worker cannot self-promote a
   result to accepted theory. Independent review must name exactly what it checked.
4. For a surviving result, add a narrow child task referencing the reviewed
   result hash. For a failure, record whether the claim, method, implementation
   or data access failed. Do not silently retry the same exhausted premise.
5. Coordinate only meaningful ownership changes, new reviewed results and
   overlaps with the other orchestrator. The hourly Astra heartbeat performs
   this cycle; it is not a continuously running DeepSeek process.

## Claim and result protocol

Before dispatching a queued task, the dispatcher creates
`claims/<task_id>.json` using exclusive creation (O_CREAT|O_EXCL or Python
`open(path, 'x')`). Include task hash, owner chat, actual worker/execution ID,
start time and allowed output directory. A competing claim means do not launch
another worker. An existing claim never proves a worker is still alive: check
its actual execution state. Preserve completed/stale claims and reconcile with
their owner rather than deleting or silently stealing them.

Workers write only `results/<task_id>/<run_id>/`, with a unique run ID and
`result.json` matching `RESULT_CONTRACT.json`, plus derivation, executable code,
raw outputs and bounded-run provenance where computation bears on the claim.
No worker edits a task specification, queue, shared source, previous result or
review. A task marked `awaiting_parent_review` cannot be dispatched as a
downstream accepted-claim calculation; its candidate can be audited only under
an explicit audit task.

The other catalog may supply its own launcher/response wrapper. Use an adapter
or cross-link rather than silently changing either contract. There is currently
no new DeepSeek launcher installed by this namespace. Existing Astra research
agents are real executions in the original campaign; their returned artifacts
will be imported as provenance-linked intake records, not relabeled DeepSeek runs.

## Evidence standard

The goal is a common physical theory with dynamics, conservation, stability,
lensing, cosmology and calibrated observations. Closing a finite parameter
box or proving a lemma closes that scope only. A model match obtained through
free per-object corrections does not establish a common explanation. Preserve
the user's core scale law and explicitly declare any proposed extension that
changes its physical interpretation.
