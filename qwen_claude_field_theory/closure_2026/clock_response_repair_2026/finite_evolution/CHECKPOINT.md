# Verified checkpoint: explicit linear dust construction, full theory OPEN

## Result

The old fixed-K illustrative repair fails the tested finite-scale dust-transfer gate. A changed, explicit K(Q,τ) action admits an exactly dustlike background and vanishing linear total pressure response at all regular finite k. Its closed profile gives positive quadratic kinetic energy; the action-to-kinetic-formula reduction is checked in SymPy, and the all-wavelength sign and constraint-regularity implications are certified in Lean.

This is effective **field-based dark dust**, not particle-CDM and not yet a MOND theory. No numerical fit or coefficient identity has been promoted to a law of nature. The clock history and action functions are reconstructed, and κ=1/2 remains fitted.

## Exact changed scope

Only new files in this `finite_evolution/` directory are included:

- `README.md`, `CHECKPOINT.md`;
- `evolve.py`, `inverse_clock.py`, `inverse_entropy_clock.py`, `entropy_health.py`, `entropy_quadratic.py`, `check_all_scales.py`;
- `EntropyProfile.lean`, `AllScales.lean`;
- `run_checks.py`, `run_certificates.py`;
- `contract.json`, `all_scales_contract.json`;
- `run_001/manifest.json`, `run_001/results.json`, `run_001/stdout.txt`, `run_001/stderr.txt`;
- `run_002/manifest.json`, `run_002/results.json`, `run_002/stdout.txt`, `run_002/stderr.txt`.

Unrelated shared-working-tree edits were left untouched.

## Executed commands and exits

Exact command argument arrays, working directories, stdout, stderr and exits for every case are in `run_002/results.json`; the enclosing bounded-run command and input/output hashes are in `run_002/manifest.json`. Both manifests passed the computation-audit validator with current-source hash verification (exit 0).

| Check | Exit | Interpretation |
|---|---:|---|
| `evolve.py` | 0 | Eight identities; 36 runs; three independent-integrator comparisons; old illustrative model fails dustlike transfer |
| `inverse_clock.py` | 0 | No generic pressure-canceling history found in the stated fixed-K family |
| `inverse_entropy_clock.py` | 0 | New action gives a k-independent inverse equation canceling both linear pressure responses |
| `entropy_health.py` | 0 | Closed profile; 37 epochs; 111 sampled kinetic signs; worst inverse-ODE residual approximately 1.11×10⁻⁷⁰ |
| `entropy_quadratic.py` | 0 | Fresh ADM expansion; actual reduced finite-k rank 2 and separate homogeneous rank 4 |
| `EntropyProfile.lean` | 0 | Three conditional algebra theorems |
| Prior `derive.py` | 0 | 67 existing checks rerun; their physical conclusions are not transferred to the changed action |
| Prior `ResponseRepair.lean` | 0 | Five existing certificates rerun |
| `check_all_scales.py` | 0 | Actual eliminated-action Hessian matches Lean formula and independent Schur complement |
| `AllScales.lean` | 0 | Four additional conditional all-scale/sign/regularity theorems |

Both new Lean files report only `propext`, `Classical.choice`, and `Quot.sound`; neither uses `sorry` or `admit`. Seven new theorems do not mean seven independent physical predictions.

## Next unavoidable work

First derive the nonlinear constraint algebra and cubic interactions on an inhomogeneous χ background: the pressureless branch may still hide strong coupling or develop caustics. Separately include varied radiation and baryons and recompute the clock background/perturbations before any recombination or CMB claim. Only then add and re-vary a MOND operator in the **same action**; galaxy/lensing and PPN certificates cannot be borrowed from another candidate. Neither a complete gravity theory nor a universal no-go has been established.
