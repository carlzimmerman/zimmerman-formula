# Poisson-floor proof audit and exact runs

**Primary verdict: proved as written for the five Lean statements.** Their physical application remains conditional on the explicitly stated measure-to-algebra correspondence. The independently reviewed prose now explicitly requires finite expectations and a strictly positive finite control normalization. The n=2 argument is correct under those assumptions; it does not require initial equilibrium.

Skills used: proof-audit, computation-audit, and verification-before-completion. No Lean source edits were made by this reviewer; no Git mutations were performed.

## Independent mathematical review

Claim card: for real `retention p0 hit = p0+(1-p0)*hit`, prove (i) retention>=p0 if p0<=1 and hit>=0, (ii) equality iff hit=0 when p0<1, (iii) the host-difference identity, (iv) exp(-2)>21/200, and (v) no nonnegative hit contribution can meet the original21/200 ceiling at p0=exp(-2).

The lower bound is nonnegative multiplication. The equality proof correctly excludes p0=1, where every hit value would saturate. The host-difference result is an exact ring identity. The exponential argument uses the imported, proved absolute remainder bound to establish exp(1)<=3, then exp(2)<=9. Positivity and exp(-2)*exp(2)=1 imply exp(-2)>=1/9>21/200. The last theorem combines that strict inequality with the mixture lower bound. No supplied decimal approximation appears as a proof premise.

| Obligation | Review result |
| --- | --- |
| Types, signs, quantifiers and p0=1 saturation exception | Passed |
| Exact numerical inequality and its Mathlib dependency | Passed by source review and fresh kernel check |
| Custom axioms or `sorry` | None in the source; five reports list only standard foundations |
| Finite-expectation normalization in prose | Explicit after reviewer-requested clarification |
| n=0 conditional hit mean | Use a harmless zero convention, or state the conditional-mean form for n>0; raw decomposition and n=2 theorem are unaffected |
| Poisson law, independence and common no-event/control flow | Stated mathematical/physical inputs; not formalized in this Lean file |
| Coupled self-gravitating field correspondence | Not established; can invalidate the factorization |
| Prior-paper attribution | Not needed for these proofs; existing root-agent literature verification was not independently repeated here |

Dependency chain: prescribed common flow and count/initial-data independence -> zero-event expectation p0*M0 -> normalized mixture -> Lean algebra -> n=2 original-ceiling exclusion. Only the last two arrows are kernel-checked here. A finite independently sampled ratio is not the population expectation, so its point estimate may fall below exp(-2) without contradicting the theorem.

## Toolchain verification

Working directory:

```text
/Users/carlzimmerman/new_physics/zimmerman-formula/qwen_claude_field_theory/closure_2026/clock_constitutive_construction_2026/lean_formalization_2026
```

Executed `/opt/homebrew/bin/lake env lean --version`, exit0:

```text
Lean (version 4.34.0-rc2, arm64-apple-darwin24.6.0, commit 6a10ac8c22beadecabdbb0919c2b50214762f91d, Release)
```

`lean-toolchain` pins `leanprover/lean4:v4.34.0-rc2`. The existing `lake-manifest.json` pins Mathlib revision `85e3a25e006c35636f0e53b0e9296caca2685bc0`. Both files and the actual proof are hashed before and after the bounded run.

## Exploratory history, explicitly not archived proof evidence

The parent agent reports two earlier direct executions of exactly this command from the working directory above:

```bash
/opt/homebrew/bin/lake env lean /Users/carlzimmerman/new_physics/zimmerman-formula/qwen_claude_field_theory/closure_2026/clock_response_repair_2026/c003_action_audit_2026/PoissonFloor.lean
```

The first used the larger `ExponentialBounds` import and exited1 with a duplicate cached `Asymptotics.IsEquivalent` declaration. Its full diagnostic and exact earlier source were not retained after conversation compaction. This is reported exploratory environment/import history, not an independently reproduced theorem failure or a hash-pinned run.

After changing to the minimal `Mathlib.Analysis.Complex.Exponential` import, the parent reports exit0 and five standard-axiom reports. The current proof derives exp(1)<=3 from the absolute remainder estimate; it does not use `exp_one_lt_three`. That exploratory success is superseded as evidence by the fresh archived run below.

## Fresh bounded Lean run

Executed from repository root `/Users/carlzimmerman/new_physics/zimmerman-formula`:

```bash
python3.11 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.0.0/skills/computation-audit/scripts/run_experiment.py --root /Users/carlzimmerman/new_physics/zimmerman-formula --contract qwen_claude_field_theory/closure_2026/clock_response_repair_2026/c003_action_audit_2026/poisson_contract.json --input qwen_claude_field_theory/closure_2026/clock_response_repair_2026/c003_action_audit_2026/PoissonFloor.lean --input qwen_claude_field_theory/closure_2026/clock_constitutive_construction_2026/lean_formalization_2026/lean-toolchain --input qwen_claude_field_theory/closure_2026/clock_constitutive_construction_2026/lean_formalization_2026/lake-manifest.json --output qwen_claude_field_theory/closure_2026/clock_response_repair_2026/c003_action_audit_2026/poisson_001 --timeout 90 --max-output-bytes 1048576 --max-cpu-seconds 80 --max-threads 1 -- /bin/bash -c 'cd /Users/carlzimmerman/new_physics/zimmerman-formula/qwen_claude_field_theory/closure_2026/clock_constitutive_construction_2026/lean_formalization_2026 && /opt/homebrew/bin/lake env lean /Users/carlzimmerman/new_physics/zimmerman-formula/qwen_claude_field_theory/closure_2026/clock_response_repair_2026/c003_action_audit_2026/PoissonFloor.lean'
```

Actual UTC start:2026-09-12T14:56:35.395347+00:00. Runtime1.957556seconds. Runner and Lean child both exited0. Status `completed`; stderr is empty. All five `#print axioms` reports contain exactly `[propext, Classical.choice, Quot.sound]`. These are Lean/Mathlib's standard foundational axioms, not five independent physical axioms and not a full-theory certificate.

Archived evidence: `poisson_001/manifest.json`, `stdout.txt`, and `stderr.txt`. The actual exact argv, repository state, source/toolchain/dependency-manifest hashes and log hashes are recorded. No theorem-output file was requested; the kernel-check command's exit and five axiom reports are the declared evidence.

Validation command:

```bash
python3.11 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.0.0/skills/computation-audit/scripts/validate_manifest.py qwen_claude_field_theory/closure_2026/clock_response_repair_2026/c003_action_audit_2026/poisson_001/manifest.json --root /Users/carlzimmerman/new_physics/zimmerman-formula
```

Exit0: `valid evidence record; mathematical interpretation requires review`. Input freshness and archived output hashes passed. Reproduce with a fresh run-directory name; do not overwrite archived evidence. The manifest pins the dependency manifest rather than hashing every installed Mathlib compiled artifact.

## Read-only numerical orientation

Executed from repository root, exit0:

```bash
python3 - <<'PY'
import math
print('p0(n=2)=',repr(math.exp(-2)))
print('necessary_n_min=',repr(-math.log(.105)))
print('n2_floor_excess=',repr(math.exp(-2)-.105))
print('relaxed_ceiling=',repr(.105*1.35))
PY
```

Outputs: exp(-2)=0.1353352832366127; necessary n_min=2.2537949288246137; floor minus original ceiling=0.030335283236612706; relaxed ceiling=0.14175000000000001. These floating-point values are explanatory and are not the Lean proof. The necessary mean is not a proposed coefficient refit or a sufficient physical condition.
