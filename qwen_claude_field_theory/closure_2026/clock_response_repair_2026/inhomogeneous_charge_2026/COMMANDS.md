# Commands, exits and evidence scope

Working directory unless specified: `/Users/carlzimmerman/new_physics/zimmerman-formula`.
Work began at `738773278`. Concurrent `9212f4498` added L194; the inspected common action inputs did not change. Each manifest records its actual revision, dirty state, supplied-input hashes and software. No pre-existing scientific source was edited.

## Fresh tests executed by the main agent

```bash
python3 -B -m unittest discover -s qwen_claude_field_theory/closure_2026/clock_response_repair_2026/inhomogeneous_charge_2026/exterior -p 'test_*.py' -v
python3 -B -m unittest discover -s qwen_claude_field_theory/closure_2026/clock_response_repair_2026/inhomogeneous_charge_2026/current -p 'test_*.py' -v
python3 -B -m unittest discover -s qwen_claude_field_theory/closure_2026/clock_response_repair_2026/inhomogeneous_charge_2026/constraints -p 'test_*.py' -v
python3 -B -m unittest discover -s qwen_claude_field_theory/closure_2026/clock_response_repair_2026/inhomogeneous_charge_2026/tracking -p 'test_*.py' -v
python3 -B -m unittest discover -s qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026 -p 'test_*.py' -v
python3 -B -m unittest discover -s qwen_claude_field_theory/closure_2026/clock_response_repair_2026/finite_gradient_metric_2026 -p 'test_*.py' -v
python3 -B -m unittest discover -s qwen_claude_field_theory/closure_2026/clock_response_repair_2026/finite_gradient_metric_2026/cubic -p 'test_*.py' -v
python3 -B -m unittest discover -s qwen_claude_field_theory/closure_2026/clock_response_repair_2026/finite_gradient_background_2026 -p 'test_*.py' -v
```

All eight exited **0**, with respectively **5,9,5,5,35,4,6,6 tests: 75 total**. These include both-sign and absent-balance controls; passing them does not mean the tested theory is stable. The scientific scripts explicitly record its failures. Child test and development commands are additionally recorded in their reports/command logs.

## Executable scientific runs

The following new wrappers were executed by their owning agents, exit **0**:

```bash
python3 -B qwen_claude_field_theory/closure_2026/clock_response_repair_2026/inhomogeneous_charge_2026/exterior/run_bounded.py
python3 -B qwen_claude_field_theory/closure_2026/clock_response_repair_2026/inhomogeneous_charge_2026/constraints/run_bounded.py
python3 -B qwen_claude_field_theory/closure_2026/clock_response_repair_2026/inhomogeneous_charge_2026/tracking/run_bounded.py
```

The current audit used the installed bounded runner directly; its exact invocation is in [current/COMMANDS.md](current/COMMANDS.md). All four scientific children ran their new audit scripts and exited **0**, with exact argv/results/log hashes in their `run_001/manifest.json`. The bounded source runs are not generic theory certification runners.

The original L194 file writes a user-owned JSON result when executed at top level. That top level was **not** rerun. The new tracking script parses and executes the six recorded original function definitions, including original `track` and `fixed_point`, and writes only its own new result. This preserves old results and states precisely which source behavior was reproduced.

Three early constraint JSON snapshots are preserved as historical development output, not fresh validated evidence; see [constraints/COMMANDS.md](constraints/COMMANDS.md). The final bounded run supersedes them. No discarded failing scientific run is being relabeled as a pass. Read-only attempts at a few guessed/missing paths returned exit1 or2 and were resolved by `rg --files`; those were source-discovery errors, not physics failures.

## Lean and independent algebra

From `qwen_claude_field_theory/closure_2026/clock_constitutive_construction_2026/lean_formalization_2026`:

```bash
/opt/homebrew/bin/lake env lean /Users/carlzimmerman/new_physics/zimmerman-formula/qwen_claude_field_theory/closure_2026/clock_response_repair_2026/inhomogeneous_charge_2026/AsymptoticCone.lean
/opt/homebrew/bin/lake env lean /Users/carlzimmerman/new_physics/zimmerman-formula/qwen_claude_field_theory/closure_2026/clock_response_repair_2026/inhomogeneous_charge_2026/TrackingBalance.lean
```

Both exited **0**, with **5+4 lemmas** and only propext, Classical.choice and Quot.sound. Both were independently reviewed and compiled. An earlier four-lemma AsymptoticCone draft also compiled before the isotropic-form lemma was added; final five-lemma source is the archived one. No sorry/custom axiom was used.

The main agent also ran an independent differentiated-mode check (exit **0**):

```bash
python3 -c 'import sympy as s; N,nu,stiffness=s.symbols("N nu stiffness",real=True); mode=s.exp(N); residual=s.diff(mode,N,2)+nu*s.diff(mode,N)-stiffness*mode; derived=s.solve(residual,stiffness)[0]; print("Derived from differentiated exponential mode:",derived); assert s.simplify(derived-(1+nu))==0'
```

This computes the drag-control relation by differentiating the mode and solving its equation, independently of the stored tracking arithmetic identity. It is still an approximation control, not a replacement action.

Fresh bounded Lean builds used the installed computation-audit `run_experiment.py`, root equal to the repository, contracts `lean_contract.json` / `tracking_lean_contract.json`, their exact declared execution_artifacts supplied as `--input`, outputs `lean_001` / `tracking_lean_001`, a90-second wall cap,1MiB log cap and cooperative one-thread setting. Exact executed child argv, hashes, declared software versions and effective limits are in those manifests. Both runner and child exits **0**.

## Provenance validation

The main agent executed the following command separately for each of the six manifest paths below:

```bash
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.0.0/skills/computation-audit/scripts/validate_manifest.py MANIFEST_PATH --root /Users/carlzimmerman/new_physics/zimmerman-formula
```

| MANIFEST_PATH, relative to this directory | Run / validation exit | Interpretation |
|---|---:|---|
| `lean_001/manifest.json` | 0 / 0 | Five exact conditional cone/limit lemmas |
| `tracking_lean_001/manifest.json` | 0 / 0 | Four exact assumed-rate/drag lemmas |
| `exterior/run_001/manifest.json` | 0 / 0 | Six selected physical epochs and constrained high-k comparison |
| `current/run_001/manifest.json` | 0 / 0 | Action current, root classification and nonstationary-charge checks |
| `constraints/run_001/manifest.json` | 0 / 0 | Three finite-interval slices, solved lapse, refinement and currents |
| `tracking/run_001/manifest.json` | 0 / 0 | Original-function probe and seeded extra-mode test |

All current source-input and output hashes match. Reproduction must use fresh run-directory names; wrappers deliberately refuse to overwrite existing evidence. Hash validation is not proof of physical interpretation.

## Final Git scope

Read-only Git checks included status, recent log, source-commit stats and staged diff. Only the exact new files listed in [FILES.md](FILES.md) are committed by this continuation. Existing shared-main history and other agents' files are preserved. Source/document/JSON whitespace checks precede the commit; raw logs remain verbatim. The final user handoff records the actual commit and push outcome. No forced push, action retuning, journal submission or public announcement is part of this change.

The initial no-index whitespace check of the generated FILES.md exited3 for one extra blank line at EOF. A subsequent no-index clean-file comparison exited1 because the file differed from /dev/null, not because of a scientific failure. The first complete working-tree whitespace check exited2 for the same EOF issue in two current-audit Markdown files. All three documentation-only blank lines were removed before the final check; no scientific source or evidence log was altered.
