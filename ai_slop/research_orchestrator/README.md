# Autonomous Qwen research loop — v2

The local `qwen3.8:27b-mlx` model generates Python experiments, runs them, repairs failures, pushes deeper tests and attempts Lean proofs. No human approval is required between research steps. The remote referee is off by default; every role uses the local model unless `ORCH_REMOTE_REFEREE=1` is explicitly set.

## What happens each iteration

1. Select an unresolved research obligation. Rotate persistent constructive, counterexample and referee roles, with more turns allocated to higher-priority questions. Four concrete routes per obligation cross those three roles; primary-attempt counts survive restarts and repairs do not consume route slots.
2. Give Qwen the pinned research context, current repository headlines, available data files, recent attempts and a bounded memory of earlier rejections. The memory scans the latest 1,000 records for the obligation, carries up to six distinct referee objections, and marks them advisory rather than physical facts. Cluster jobs prioritize actual X-COP paths, with FITS table column names and units read from the file headers. Qwen proposes a hypothesis and executable Python addressing the assigned route.
3. Copy declared real inputs, hash code/data and execute the generated program in a fresh macOS sandbox. Before ordinary search execution, redirect a repeat of a previously completed program with the same hypothesis, assumptions, syntax tree, input paths/bytes and check names; cosmetic edits do not create a new experiment. Changed computations, inputs or explicitly revised hypotheses/assumptions remain eligible; narrowing an overbroad interpretation can reuse a calculation. Explicit CLI replay and referee-directed door replication remain available. Infrastructure failures may be retried. Run main, known-positive and known-negative modes. Reject crashes, missing checks, malformed output and broken controls. A scientifically negative main result remains useful evidence.
4. Repair execution/schema errors up to twice. Freeze the hypothesis and assumptions immediately, and freeze check names only after validating the check specification. Invalid metadata can be corrected; a valid target cannot be weakened. Repairs receive only the latest failed answer, actual process output and explicit control mismatches. Preserve every attempt.
5. On a supported candidate, a fresh referee call reads its actual code/results and specifies a frozen necessary consequence. Qwen codes and runs that next door. Another referee call reviews the executed door before it advances. Continue through at most four doors; a failed required check stops the chain.
6. For a surviving route, the target referee states a precise mathematical proposition and explains its relationship to the result. Freeze that statement **before** asking Qwen for a proof. Run the installed Lean compiler, inspect the exact theorem's axioms, and feed compiler errors back for up to two repairs.

The referee is a separate model call, not an independent scientist. A `candidate_checked` result means the generated test and controls completed. `formal_checked` means the stated conditional theorem compiled with the permitted foundational axioms. Neither means the physical theory is true, the assumptions hold in nature, or the result is novel. Optional independent review records are for promotion/publication; they never block ordinary autonomous experiments or doors.

## Run and stop

The rewrite was initially left stopped. The user subsequently authorized relaunch of `com.zimmerman.orchloop` and `com.zimmerman.orchwatch`. Use the status command and launchctl to inspect current state. Ollama itself was not killed.

From the repository root:

```bash
./ai_slop/research_orchestrator/run.sh status
./ai_slop/research_orchestrator/run.sh plan
./ai_slop/research_orchestrator/run.sh run --iterations 1
./ai_slop/research_orchestrator/run.sh run --continuous
```

Ctrl-C/SIGTERM stops the foreground loop. The single-writer lock prevents concurrent v2 loops. `run_loop.sh` is the continuous launchd entry point. To deliberately re-enable a previously installed service, use `launchctl enable gui/$(id -u)/com.zimmerman.orchloop` and then `launchctl bootstrap gui/$(id -u) "$HOME/Library/LaunchAgents/com.zimmerman.orchloop.plist"`. To stop it again, disable that label and boot it out of the same domain. The watcher is optional and uses the analogous `com.zimmerman.orchwatch` label. No installation or restart happens merely by importing the code or asking for status.

`ORCH_PYTHON` overrides the launcher interpreter; the default is the existing conda Python. `WORKER_MODEL` and `OLLAMA_URL` override the local model. Install missing Python libraries from `requirements.txt` into that interpreter. Generated programs cannot install dependencies or fetch new datasets. They can use the local research files declared in their input manifest. The existing Lean project/toolchain and compiled libraries must already be installed.

## Evidence and replay

`runtime_v2/ledger_v2.sqlite` stores attempts, review events and persistent API accounting. Every attempt receives a UUID directory containing its request, response, verifier result, input snapshots, full process logs and artifact hashes. Original artifacts are never reused for another attempt. Tampering is detected on load; generated symlinks, hardlinks and special files are not archived. Execution and artifact sizes are bounded.

```bash
./ai_slop/research_orchestrator/run.sh replay ATTEMPT_ID
./ai_slop/research_orchestrator/run.sh review ATTEMPT_ID accept \
  --reviewer "Reviewer name" --note "Exact scope and independent checks"
```

Replay uses archived Python and input bytes rather than the current original files. Lean replay additionally requires the pinned compiler/library environment to remain available. It records hashes of compiled Lean dependencies before and after checking, not just the project manifest. The initial full environment hash may be slow; unchanged files are cached within the process. The trusted base still includes the installed Lean kernel and libraries; this tool does not implement a second independent kernel checker.

The old `ledger.sqlite`, `staging/`, `lean_staging/`, logs and seed files remain historical evidence. Old source was backed up under `archives/pre_v2_20260921_124816/`. Their scores and “known results” are not imported as facts or used to gate new proof attempts. Source, tests and initial obligation files are eligible for Git; generated artifacts, archives, ledgers and logs remain ignored.

## Experiment protocol

Qwen returns JSON containing `hypothesis`, `assumptions`, `argument`, `next_test`, Python `code`, `required_checks`, `negative_checks`, and `inputs` (`[{"name":"sample","path":"real_research/data/example.csv"}]`). Input paths must resolve to visible research files inside this repository. Optional `timeout_s` is capped at 1,800 seconds per mode.

The program receives:

- `ORCH_MODE`: `main`, `positive`, or `negative`.
- `ORCH_INPUTS`: path to a JSON map of input names to their isolated snapshot paths.

Emit exactly one JSON object to stdout; diagnostics go to stderr:

```json
{"protocol":2,"complete":true,"checks":{"target":true},"measurements":{"value":1.0}}
```

Every required check must be a named boolean in every mode. Exit zero when the scientific computation completes, even for a false check; nonzero exit means execution failure. Positive controls must pass all required checks. Every designated negative check must fail in the negative control. Required checks determine support/rejection; diagnostics cannot hide a failed target.

Controls must exercise the computation. Switching literal booleans or fabricating observations is invalid research even if it satisfies the protocol; the autonomous referee is explicitly asked to catch that, but it is fallible. This is why the tool reports candidates rather than scientific truth scores.

## Research direction and configuration

`contracts/` starts with particle-free normalization selection, common-action consistency and cluster source/lensing closure. These are open research objectives, so Qwen may generate and execute new experiments immediately. Changing an action must be explicit in the hypothesis. The program must not substitute an assumed unit slope for a derivation of it.

Optional `evaluator` and `lean` contracts support independently reviewed fixed benchmarks. These require a named review, frozen target/checks and hashed dependencies, but are not prerequisites for ordinary generated experiments. Dependency links are satisfied only by accepted supporting evidence for the current contract version; negative and inconclusive results remain visible without becoming assumed premises.

The subprocess sandbox denies network access, forking, signals and writes outside scratch; file contents are limited to declared input snapshots and required system/library paths. It is macOS-specific. No insecure automatic fallback is used if sandbox execution is unavailable. CPU time, output, open files and archive size are limited; macOS may not enforce the virtual-memory limit. These controls are practical isolation, not a claim of complete protection against a hostile kernel exploit or malicious installed dependency.

Remote calls, if explicitly enabled, reserve estimated cost persistently before dispatch. Unknown outcomes retain their reservation across restarts. Provider prices must be configured accurately; this is not a provider-enforced billing cap. Local execution is the default and was preserved from the original tool.

## Verification

```bash
/opt/homebrew/Caskroom/miniconda/base/bin/python3 -B -m unittest discover \
  -s ai_slop/research_orchestrator/tests -v
```

The suite runs actual generated Python and Lean using canned model replies, so it needs no model API calls. Sandbox-exec tests must run outside an enclosing sandbox that prohibits applying seatbelt profiles. Tests cover evidence reuse/tampering, controls, exact door requirements, malformed responses, replay, sandbox isolation, formal target/axiom checks, compiled-library changes and the complete generated-Python → door → Lean path.

Search policy `route-memory-v1` changes allocation and context only; verifier `obligations-v2.2` and existing evidence remain unchanged. Route questions are proposals, not new scientific premises. Exact-repeat detection is not semantic novelty detection and can be bypassed by genuinely or superficially changing code or rewording a claim; the referee still has to read the experiment. No breakthrough is guaranteed by the scheduler.
