# Keeping the autonomous search moving — 2026-09-21

The user asked to keep local Qwen pursuing closure after the status check found 266 v2.2 records, 195 executed programs, 115 control failures, 24 supporting candidates all rejected by the referee, and zero Lean attempts. Some hypotheses appeared more than twenty times. This update changes search allocation and memory; it does not relax verification or claim a discovery.

- `route-memory-v1` carries advisory rejection summaries beyond the previous six-record window. It scans the latest 1,000 records for each obligation, across versions, summarizes recurring failures, and includes up to six distinct referee objections. Historical reviews never become proved premises.
- Four concrete routes for each of the three research obligations rotate using persistent primary-attempt counts. Their four-step rotation crosses the three roles. Repairs do not advance it.
- Completed experiments with the same normalized hypothesis, explicit assumptions, Python syntax tree, input paths/bytes and check specification are redirected before execution. Changed calculations or scientific claims remain eligible; explicit replay and referee-directed door replication remain available. This is syntactic repetition detection, not a novelty oracle.
- Review found that a narrower hypothesis must be allowed to reuse an existing calculation. A regression reproduced the false rejection, and the signature now includes hypothesis and assumptions. Cosmetic code-only changes still do not evade it.
- Cluster jobs see X-COP files first and receive actual FITS column names and units, reducing invented schemas and unit ambiguity.
- Route, memory and search-policy version are archived in each new request. Verifier v2.2 and the historical ledger are preserved.

Validation includes persisted feedback, route rotation across restart, exact-repeat suppression, allowed changed programs/input bytes/hypotheses, explicit replay, tamper detection, and actual FITS schemas. The complete suite passed: `python3 -B -m unittest discover -s ai_slop/research_orchestrator/tests -q` — 43 tests in 29.438 seconds, `OK`.

Deployment: the continuous launchd worker restarted as PID 99899 on 2026-09-21 at approximately 22:45 UTC. An immediate bootstrap after bootout returned error 5; inspection confirmed the old service had unloaded and the unchanged plist validated. A subsequent bootstrap succeeded. Process inspection confirmed `python3 -B orchestrator.py run --continuous` and an established connection to local port 11434. The live status selected `background-to-growth` for `common-action-consistency`, with the 281 prior ledger records preserved. The existing watch job also completed with exit code zero. No research result is inferred from service health.

Limitations: Qwen can still rephrase or change an experiment without adding scientific value. The referee is another local model call and is fallible. The broader research goal, independent selection of kappa=1/2, remains open. No paid API is enabled and no new scheduled task is created.
