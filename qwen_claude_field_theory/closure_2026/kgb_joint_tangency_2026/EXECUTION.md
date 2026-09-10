# Executed evidence

Exact important argv/cwd/exit records: [COMMANDS.json](COMMANDS.json).
Raw stdout/stderr for every main case: [run_001/results.json](run_001/results.json).
The main provenance manifest pins inputs before/after execution; all three
main/derivative/zero-braiding manifests validate with current source hashes.

| Execution | Result |
|---|---|
| Main bounded suite, 17 cases | Exit 0, 42.288883 seconds |
| Python tests within main suite | 78 passed |
| Additional parallel-launcher tests | 8 passed, exit 0 |
| Conditional Lean compilation | 5 lemmas, both files exit 0 |
| Four-variable geometry search | 21 starts, max_nfev=500, no accepted numerical joint |
| Four-variable clock search | 2 starts, max_nfev=1000, 1 accepted numerical joint |
| Independent joint refinement | 60/80 digits: equations match; health and higher gate fail |
| Final launcher smoke | 4 jobs, 2 workers, max_nfev=1; exit 0 |
| Final smoke resume | Exit 0; all 4 completed jobs skipped |

There are 86 distinct test cases in the main-plus-launcher test sets; repeat
CLI and agent runs are not added to that count. The five new Lean lemmas
report only `propext`, `Classical.choice`, and `Quot.sound`, not `sorryAx`.
Exact conditional statements and unformalized source reductions are in the
scaling and zero-braiding reports.

The final smoke finds the supplied numerical joint control and correctly
rejects it in the local health screen. One other job records a nonreal
pressure-root error; this is not a physical no-go. No candidate is queued for
further verification. `sweep/smoke_001.jsonl` is superseded preliminary evidence
from before complete transitive source pinning; use `smoke_002.jsonl`.

The initial missing-module red tests exited 1 before implementation. Their
implemented versions pass. A read-only hardware `sysctl` query was denied by
the sandbox, so no hardware-performance benchmark is claimed. The Mac model
and 64 GB memory are user-provided; worker count is configurable.

No long/background search was started. The local launcher uses no model or
network APIs. Its solver evaluation cap is not a hard wall-clock cap; numerical
Jacobian evaluations add work. Resume deliberately refuses changed code,
runtime, or search settings. Full gravity status remains **OPEN**, not certified.
