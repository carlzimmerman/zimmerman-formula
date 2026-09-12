# Exact L207 turning and scalar-sign gate

Verdict: L207's assigned `Y_min=(3 beta ell/(2d))²` is a small-beta approximation to the **lower turning point, a local maximum of W_Y**, not its minimum. Its claimed comparison window is not established by the actual derivative. This is an exact local constitutive correction, not a new physical theory or a gravitational force-law result.

Freeze U,d,ell>0 and beta>0. Directly differentiating the displayed L207 coefficient gives

`W_YY = -d/(2ell)(1+Y/ell)^(-3/2) + 3beta/(4sqrt(Y))`.

Both sides of the zero equation are positive, so squaring introduces no extra solutions. With z=Y/ell>0 the exact condition is

`beta² = [4d²/(9ell)] z/(1+z)³`.

Let f(z)=z/(1+z)³. Its derivative is `(1-2z)/(1+z)^4`, its endpoint limits are zero, and f(1/2)=4/27. The exact global bound has the polynomial certificate

`4(1+z)³-27z = (2z-1)²(z+4) >= 0`.

Therefore:

* `0<beta²<16d²/(243ell)` gives exactly two positive zeros, with z_low<1/2<z_high.
* Equality gives a double zero at z=1/2. W_YY touches zero without changing sign; W_Y has no local maximum or minimum there.
* Above that threshold there is no positive zero and W_Y is strictly increasing.

For every beta>0, `sqrt(Y) W_YY -> 3beta/4` at both Y->0+ and Y->infinity. Thus, when two roots exist, W_YY has signs **positive, negative, positive**. W_Y first rises, reaches its local maximum at the lower root, falls between the roots, then reaches its local minimum at the upper root. The exact condition that W_Y is falling at a specified Y_star>0 is

`beta² < [4d²/(9ell)] (Y_star/ell)/(1+Y_star/ell)³`.

It is not sufficient to compare Y_star with one assigned root. No value for Y_star or Hubble-kernel ratio was inserted in this audit.

Put r=9beta²ell/(4d²). The lower root solves z/(1+z)³=r and has z_low=r+O(r²) as beta->0. L207's assigned value is exactly ell*r. This explains its origin while fixing its regime and maximum/minimum label. The upper root is not represented by that approximation. Consequently beta does not cancel from an exact comparison merely because it cancels from L207's assigned leading-order scales.

The polynomial roots were computed rather than assigned. At d=ell=1,beta=1/6, the equation is `(1+z)³-16z=0`, with roots approximately -5.42863948676, **0.07837774562**, **2.35026174113**. W_YY samples below, between and above the positive roots have signs +,-,+. At beta=2/3, `(1+z)³-z=0` has one negative real root and two nonreal roots, hence no positive root. These numerical checks supplement the exact monotonicity and factorization argument; they are not the proof of the general root count.

For the same action sign used in the prior audit, the Q=0 scalar has canonical spatial stiffness `C_T=-2F_Y`, with F=P(-Y)+W(Y). The new term gives

`C_T=-3beta sqrt(Y)+O(Y)`, `C_L=C_T+2Y C_T'=-6beta sqrt(Y)+O(Y)`.

Thus positive beta has the destabilizing scalar spatial-energy sign near Y=0 on this restricted branch. Adding **-beta Y^(3/2)** instead reverses both leading signs for beta>0. This is a scalar fixed-metric energy diagnosis, not a full metric/clock stability certificate; neither sign establishes a physical MOND law or beta-to-a0 normalization.

## Evidence and commands

`audit_turning.py`: **16 checks passed**, exit 0. The exact algebra, limiting signs and coefficient threshold are checked with SymPy 1.14.0; polynomial roots and sign samples are supplementary finite computations. The runner and manifest validator both exited 0. Source hashes, revision and logs are in `run_001/manifest.json`, `stdout.txt`, and `stderr.txt`.

`TurningBound.lean`: compiled with exit 0. Three theorems certify the polynomial factorization, polynomial form of the sharp maximum, and necessary coefficient inequality `243ell beta² <= 16d²` from the exact polynomial root equation. Actual printed axioms for all three: `[propext, Classical.choice, Quot.sound]`. No custom axioms or sorry. Only warning: positive-ell hypothesis is unused in the polynomial inequality proof because that proof establishes a stronger algebraic implication. The differential derivation and physical interpretation remain outside Lean.

From repository root:

```sh
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.0.0/skills/computation-audit/scripts/run_experiment.py --root /Users/carlzimmerman/new_physics/zimmerman-formula --contract qwen_claude_field_theory/closure_2026/clock_response_repair_2026/closure_front_2026/health/turning/contract.json --input fable_independent_2026/L207_the_missing_operator.py --input qwen_claude_field_theory/closure_2026/clock_response_repair_2026/closure_front_2026/health/turning/audit_turning.py --output qwen_claude_field_theory/closure_2026/clock_response_repair_2026/closure_front_2026/health/turning/run_001 --timeout 45 --max-output-bytes 1048576 --max-threads 1 -- python3 -B qwen_claude_field_theory/closure_2026/clock_response_repair_2026/closure_front_2026/health/turning/audit_turning.py
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.0.0/skills/computation-audit/scripts/validate_manifest.py qwen_claude_field_theory/closure_2026/clock_response_repair_2026/closure_front_2026/health/turning/run_001/manifest.json --root /Users/carlzimmerman/new_physics/zimmerman-formula
```

From the existing pinned `qwen_claude_field_theory/closure_2026/clock_constitutive_construction_2026/lean_formalization_2026` directory:

```sh
lake env lean /Users/carlzimmerman/new_physics/zimmerman-formula/qwen_claude_field_theory/closure_2026/clock_response_repair_2026/closure_front_2026/health/turning/TurningBound.lean
```

Only new files in `health/turning/` were created. No L207 files or prior audit files were modified. No full model, observational, cosmological or novelty claim is made.
