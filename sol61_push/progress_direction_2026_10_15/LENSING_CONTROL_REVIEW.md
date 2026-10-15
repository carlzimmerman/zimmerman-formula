# CFG805 control and interpretation review — 15 October 2026

**Verdict:** the saved computation supports a conditional **NARROWED** comparison, not closure or an independently validated two-halo prediction. The original score was not rerun. Two small, separately recorded audit calculations identify an estimator mismatch behind most of K2, correct the reported mutation percentages, and qualify the heavy-bin diagnostic. Original criteria, scientific scripts and scores are unchanged.

Review base: `7c1eae898ec964062a01f9a79f8d7b8af5d5d52b`. Criteria were committed at `11b9e3f03bf82445a11e6bf7f4c31f9dbbc9aa0a`; results at `a7f0d45f81e4b9e062c802c77db9812030e7455f`; diagnostic at the review base. CFG650 measurement source last changed at `d0f8d3f3861d7623cb1377892ee62ab9bc0c6817`. The bounded runners observed concurrent checkout HEAD `0aec66b397c474309f6bf872bd370a9e9d6ac38d`, dirty=true; exact source/data snapshots and hashes, rather than the moving checkout, pin the new evidence.

## Contract and evidence

The scientific decision is whether the derived one-halo catchment plus a constant-bias template made from T1x gravitating auto-power closes the KiDS all-radius gap against the no-edge comparison. The surrogate profiles four masses and four nonnegative biases on 60 data points, using the supplied full covariance. It uses inherited-background/inherited-initial-condition T1x at z=0.2561784341, one canonical acceleration footing, a 0.01-dex mass grid, nearest-quarter-unit supply profiles, and four coordinate-descent sweeps. This is a finite nuisance-fit comparison; it cannot establish an isolated-lens cross-correlation, a unique gas mechanism, native initial conditions, microscopic cold-energy production, or theory closure.

New audit calculations use float64 NumPy/SciPy, no random draws, no simulation steps and no new fits:

- [run_001/result.json](lensing_control_check/run_001/result.json), [manifest](lensing_control_check/run_001/manifest.json): bounded shell-count/top-hat replay, at most a 129³ integer lattice and 1,072,218 retained nonzero modes.
- [run_002/result.json](lensing_control_check/run_002/result.json), [manifest](lensing_control_check/run_002/manifest.json): saved-score arithmetic, exact-source CFG801 residual/covariance calculation, and edge consistency at saved masses.
- Both completed with exit 0; runtimes 0.189306 and 0.500835 seconds. Caps: 45-second wall, 30-second per-process CPU, 65,536 log bytes and conventional numerical-library thread variables set to 1. No memory or affinity cap was requested. Both manifests passed Mathbox `validate_manifest.py --root` after execution. Validation authenticates recorded artifacts, not the interpretation.
- [ORIGINS_extended.json](lensing_control_check/input_snapshots/ORIGINS_extended.json) lists exact original paths, copied input paths and SHA-256 hashes. The 193 KB external T1x lean JSON and the previously untracked KiDS data leaves are copied exactly; replay does not require the external host paths. [contract.json](lensing_control_check/contract.json), [saved_result_contract.json](lensing_control_check/saved_result_contract.json) and executable scripts record the computational surrogate and bounds.

## What the original scores establish

| Saved all-radius comparison | Value |
|---|---:|
| χ²(B + 2h) | 159.6006304639 |
| χ²(D_der + 2h) | 170.6631391038 |
| Δχ²(D − B) | +11.0625086399 |
| Nominal p(D), 52 dof | 1.4989556521 × 10⁻¹⁴ |
| D biases | 0.198613 / 0.241812 / 0.525486 / 0.527178 |
| B biases | 0 / 0 / 0.129900 / 0.036915 |

The relative disadvantage falls by 92.56% from +148.7. This meets the saved NARROWED rule but fails both closure requirements: Δχ²≤4 and p≥0.01. The primary-range result Δχ²=−2.1051 also has a poor nominal absolute p=1.3288×10⁻⁷. A favorable relative difference does not repair either absolute fit. These are not nested hypotheses with a justified Δχ² significance calibration. The stated p values use the script's nominal n−8 convention; bias boundaries and profiling mean they are not a calibrated sampling distribution, but the absolute misfit is plainly material.

K1 is a useful regression check: b=0 returns the earlier +148.7 gap within 0.5. It does not validate the new transform or the physical amplitude. In the MUTATE code, `or MUT` forces the K1 flag true, so the flag itself is not an independent mutation control.

The biases show that a fitted template can compensate for much of the missing outer signal. No isolated-sample bias was predicted or independently measured. Low b is compatible with suppressed neighbours, but the saved fit alone does not establish that explanation. Constant per-bin bias multiplying matter auto-power is itself a modeling assumption.

## K2: mismatched estimators, not missing modes in only one calculation

The source definitions differ:

- `cfg650_pm.py:547–572` computes **a discrete FFT-mode sum**, σ₈² = L⁻³ Σ_mode P_mode W(8k_mode)², with Hermitian weights and zero DC. Its shell k and P arrays are separate compressed outputs: arithmetic mode means in radial shells.
- `cfg805.py:26–31` computes **a trapezoidal continuum integral of those shell means**, beginning at the first shell's mean k=0.08018239 h/Mpc. It yields 0.7543002740 against saved actual-mode 0.7791429763, a 3.188% deficit. The frozen K2 therefore remains FAIL.

For L=100 Mpc/h, the fundamental is 0.06283185 h/Mpc. Both estimators refer to the same finite periodic box; neither contains actual modes below its fundamental. Thus absent sub-fundamental modes cannot, by themselves, explain a difference between the two stored estimators. The continuum trapezoid also omits the low-k portion of the first represented shell and changes finite-shell weighting. The README's stated sub-fundamental explanation is unsupported for this comparison.

The independent bounded replay replaces every unknown individual mode power by its saved shell mean, while evaluating the window at exact integer-lattice k. It obtains:

| Upper k (h/Mpc) | Shell-constant discrete σ₈ |
|---|---:|
| 0.973894 | 0.7711416133 |
| 1.979203 | 0.7745939690 |
| 3.989823 | 0.7751588569 |

The last value is 0.5113% below the stored 0.7791429763. This strongly supports compression/quadrature as the main discrepancy. It is **not exact per-mode recovery**: within-shell power/window covariance and the uncounted high-k tail remain. The lean JSON cannot reconstruct those correlations. No new passing K2 or corrected lensing score is claimed.

The h and a factors in the implemented projection are dimensionally consistent under its declared physical-radius convention: numerical comoving Mpc/h, surface density h M☉/Mpc², then h/a²/10¹² to physical M☉/pc². Data headers use h70-scaled radii and ESD, whereas the function declares h70=1 and simulation h=0.6736; the next units audit should explicitly declare this conversion. There is no evidence here that a missing h or a factor caused K2, whose two estimators both use radius 8 Mpc/h.

For a positive **uniform** rescaling P→cP, the transform is linear and b→b/c preserves the complete model family exactly when b has no upper bound or informative prior. Therefore χ² and Δχ² are invariant in exact arithmetic. This does **not** protect against changes in spectral shape, low-k treatment, smoothing, projection cutoffs or exclusion: those change the radial template and may alter the fit. Bias values themselves remain normalization-dependent.

## Mutation and exclusion

From the actual JSON, changes in D bias relative to canonical are **−13.6028%, +9.6674%, −5.1751%, −3.2801%**. Only bin 1 exceeds 10%; bin 2 does not exceed 10% using either denominator. The README's claim of 12–15% in bins 1–2 is inconsistent with its saved numbers. Frozen wording does not specify any-bin versus every-bin aggregation; report partial sensitivity and the vector, not an unqualified PASS. There is no serialized mutation-verification flag.

No exclusion gives Δχ²=−23.8315 but χ²_D=123.0657, nominal p=1.0781×10⁻⁷. That still fails absolute closure and deliberately violates the intended catchment exclusion. It is an implementation/assumption sensitivity bracket, not a rescue.

`cfg805.py:65–66` freezes REX to the previous fit while `solve` changes mass and N. The one-halo profile also rounds N to a quarter unit. For the saved CFG805 masses:

| Bin | Fixed REX | Exact derived edge at fitted mass | Actual nearest-N profile edge |
|---|---:|---:|---:|
| 1 | 0.343 | 0.331099 | 0.331099 |
| 2 | 0.442 | 0.444915 | 0.445697 |
| 3 | 0.433 | 0.435546 | 0.443356 |
| 4 | 0.429 | 0.428866 | 0.435195 |

All entries are physical Mpc. Thus fixed exclusion does not always match even the implemented own-catchment edge. The current comparison shares the fixed template policy between B and D, but it is not a self-consistent mass-dependent decomposition. A future variant must predeclare the same exclusion *rule* for both models, evaluate it at every trial mass, and use the same actual N/edge representation as the truncated profile. Identical rules need not yield identical numerical radii when fitted masses differ. Changing this requires a new declared calculation, not overwriting the frozen score.

Other numerical obligations remain: the correlation transform adds an undeclared Gaussian factor exp[−(0.05k)²], truncates projection at 80 Mpc/h, uses a 900-point ξ grid and 220-point projection grid, and starts the projected cumulative mass at zero at nonzero minimum radius. Their effects must be bounded. Four coordinate sweeps from one initialization and a discontinuous nearest-N grid do not prove a joint global optimum.

## The heavy-bin diagnostic is descriptive, not a gas identification

`diag_chi2_breakdown.py` evaluates the **CFG801 no-edge model without two-halo terms**, at fixed masses 10.36/10.83/11.01/11.18. It does not diagnose CFG805's refitted B+2h or D+2h residuals. The new bounded calculation reproduces its joint χ²=163.1332588 and its printed pulls.

The four printed `r_bᵀ C_bb⁻¹ r_b` values are valid marginal block diagnostics, but do not partition the full joint χ²: their sum is about 167.6. Maximum cross-bin |correlation| is 0.06020; the full covariance is symmetric and positive definite. A covariance-aware conditional increment, χ²_all−χ²_rest,marginal, is 16.7317/40.6428/43.7207/57.8421 for bins 1–4. These increments are also nonadditive, but confirm that the qualitative heavy-bin concentration survives the covariance check for that baseline. An exact signed partition r_bᵀ(C⁻¹r)_b is recorded separately.

Negative innermost and positive intermediate-radius residuals are a useful shape clue. They do not identify early-type morphology, hot gas, or the cause of the excess. The next diagnosis must use CFG805's actual residuals and full covariance before directing a physical remedy toward those residuals.

## Cheapest deciding next work and completion gates

1. **Close the estimator bookkeeping without a simulation.** Use retained per-mode weighted sums or an existing full-resolution field if available to compare like estimators; otherwise explicitly record the lost within-shell information and keep K2 failed in the old record. The bounded shell replay above already distinguishes the main quadrature/compression alternative from the README explanation. Do not add arbitrary low-k power or renormalize the old score to manufacture a passing control.
2. **Validate the projection on small arrays before another fit.** For zero exclusion compare the implemented real-space projection with the independent Hankel expression ρ/(2π)∫kP(k)J₂(kR)dk, using identical spectrum, smoothing and units and a converged line-of-sight limit. Check constant-amplitude invariance, the missing inner integral and grid/cutoff stability. This separates a transform artifact from a real shape limitation cheaply. Declare tolerances before execution; a useful gate is template stability to 1% over fitted radii, plus final Δχ² stability to 0.5 after convergence checks.
3. **Only then run a separately declared mass-dependent-exclusion fit.** Share its rule between B/D; tie the excluded edge to the represented one-halo edge at every mass trial; refine/interpolate N to remove nearest-grid ambiguity; retain full residual vectors, templates, both mass vectors, biases, covariance, source hashes and convergence history. Verify multiple starts/stopping criteria and mass-grid refinement until χ² changes by less than the declared tolerance. Repeat b=0 and exclusion mutation with an explicitly stated per-bin aggregation rule.
4. **Diagnose the actual fitted residual before adding a gas model.** Report full-covariance conditional residual patterns for B+2h and D+2h, and test any proposed gas profile against both inner and intermediate radii with declared mass/shape constraints. An unconstrained extra component improving χ² is not an identification.

Numerical completion means matching estimator definitions, validated transform/units, converged fit, and an auditable mutation result under the new contract. Observational closure still requires the original all-radius Δχ²≤4 **and** an acceptable absolute p≥0.01, with any revised sampling calibration stated. None of these operations can supply microscopic theory closure or remove the inherited-initial-condition caveat.

## Reproduction commands

The original scientific commands are documented in the original scripts (`python3 cfg805.py`, or `CFG805_MUTATE=1 python3 cfg805.py`; the diagnostic runs from CFG801's directory). They overwrite original outputs and were **not** used to reproduce the scores in this review.

To reproduce only the two new audit calculations with the same caps and fresh output directories, run the following from the repository root. It refuses to reuse an existing `replay_001` or `replay_002` directory. The contracts enumerate every pinned input; the runner invokes the fixed script argv without a shell.

```bash
/opt/homebrew/bin/python3.12 - <<'PY'
import json, subprocess
from pathlib import Path
root = Path.cwd()
base = Path('sol61_push/progress_direction_2026_10_15/lensing_control_check')
skill = Path('/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.2.0/skills/computation-audit/scripts')
for number, contract_name, script_name in (
    ('001', 'contract.json', 'shell_window_replay.py'),
    ('002', 'saved_result_contract.json', 'saved_result_audit.py'),
):
    contract_path = base / contract_name
    contract = json.loads(contract_path.read_text())
    output = base / ('replay_' + number)
    result = output / 'result.json'
    argv = ['/opt/homebrew/bin/python3.12', str(skill / 'run_experiment.py'),
            '--root', str(root), '--contract', str(contract_path)]
    for artifact in contract['execution_artifacts']:
        argv += ['--input', artifact]
    argv += ['--output', str(output), '--result', str(result), '--timeout', '45',
             '--max-output-bytes', '65536', '--max-cpu-seconds', '30',
             '--max-threads', '1', '--', '/usr/bin/python3', str(base/script_name),
             '--output', str(result)]
    subprocess.run(argv, check=True)
    subprocess.run(['/opt/homebrew/bin/python3.12', str(skill/'validate_manifest.py'),
                    str(output/'manifest.json'), '--root', str(root)], check=True)
PY
```

Numerical results remain conditional on the recorded Python 3.9.6, NumPy 1.26.2 and SciPy 1.11.4 implementations; the runner/validator used Python 3.12.11. The source audit establishes the differing estimator definitions independently of whether a different platform reproduces the final floating-point digits.
