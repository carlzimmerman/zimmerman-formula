# CFG322: does CFG321's rising Lyapunov exponent saturate with resolution? (recipe G5/G10, zero-field nonlinear dependence)

**Verdict (frozen rule): OPEN.** Neither eps set meets the convergent rule. Neither meets the confirmed-fail rule.
CFG321's FAIL is not lifted and not confirmed; G5/G10 nonlinear dependence stays as CFG321 recorded it.

The criteria were frozen first: [FROZEN_CRITERIA.md](FROZEN_CRITERIA.md), commit 16139a770. Implementation disclosures
are appended at its end; the frozen text is unchanged.

**Scope.** 1-D only. This lane says nothing about growth or sigma_8: L341 (sigma_8 = 18–27) and FP2's failed linear
cosmology stand. kappa = ½ is FITTED and plays no role.

## The question

CFG321 (6cb69cdc1) found the chassis's nonlinear evolution about an open zero-field region saturated and regular, with
one problem. In the 1-D eps = 1e-3 set the pair-separation exponent lambda rose with resolution:
- lambda = 0.012 / 0.041 / 0.066 at N = 63 / 127 / 255;
- the maximum amplification rose 95 / 339 / 1052.

Does lambda(N) level off at a finite value as N → ∞ (continuous dependence with a finite Lyapunov time)? Or does it
keep growing (discontinuous dependence)?

## Method

- CFG321's engine is copied byte-for-byte (sha256 bde2fbb6…, checked at start).
- ν_mono kernel, data class D (seeds 321/322), L = 16 xi, T = 80: all unchanged.
- 1-D, N = 63 / 127 / 255 / 511, eps = 1e-3 and 1e-4, base runs plus pairs at delta = 1e-3 and 1e-5. That is 24 runs.
  All are regular: status ok, zero indefinite leaf Hessians, residual ≤ 1e-10.
- N = 1023 was not run: an estimated 2–8 h per run, over budget, as disclosed before freezing.

## Results

| N | lambda, eps 1e-3 | Amax, eps 1e-3 | lambda, eps 1e-4 | Amax, eps 1e-4 |
|---|---|---|---|---|
| 63 | 0.0124 ± 0.0032 | 95.1 | 0.0372 ± 0.0019 | 160.2 |
| 127 | 0.0414 ± 0.0024 | 338.7 | 0.0569 ± 0.0023 | 897.2 |
| 255 | 0.0663 ± 0.0027 | 1051.9 | 0.0762 ± 0.0028 | 1733.9 |
| 511 | **0.0721 ± 0.0031** | **1827.5** | **0.0916 ± 0.0025** | **7434.4** |
| increments | 0.029, 0.025, 0.006 | ×3.56, ×3.11, ×1.74 | 0.020, 0.019, 0.015 | ×5.60, ×1.93, ×4.29 |
| ratios r2, r3 | 0.861, **0.229** | | 0.983, **0.796** | |
| geometric lambda_∞ | 0.074 (order p 2.1) | | 0.152 (order p 0.33) | |

(± is the fit's slope standard error; it ignores autocorrelation.)

**Reading.**
- **eps = 1e-3.** The rise nearly stops at N = 511: the increment falls ×4 and the amplification step drops below ×2.
  CFG321's FAIL signature no longer fires on the last three grids. But r2 = 0.86 had already put the convergent
  outcome out of reach without N = 1023, as stated before freezing. Result: OPEN.
- **eps = 1e-4** (new; smaller eps, closer to the physical 2.6e-18). lambda keeps rising almost linearly in log N:
  increments 0.020, 0.019, 0.015. r3 = 0.80 lies between the convergent threshold (0.6) and the fail threshold (0.9).
  The extrapolated lambda_∞ is finite (0.15), but only at a slow order p ≈ 0.3, double today's 0.09. The maximum
  amplification grows ×4.3 at the last step. Result: OPEN, leaning toward continued growth.
- **The physical direction is the bad one.** Smaller eps gives a larger lambda at every N and slower convergence.

**Reported, not graded.**
- The saturated rms yhat falls with N at eps = 1e-4: 0.600 / 0.600 / 0.507 / 0.453. At eps = 1e-3 it is near flat:
  0.604 / 0.598 / 0.573 / 0.555. So at eps = 1e-4 the saturated state itself is not yet resolution-converged at
  N = 511.
- The amplification at CFG321's growth-phase time tau_s = 5.75 stays flat at 2.4–2.7: the sensitivity builds up late,
  in the saturated state.
- The response stays linear in delta at tau_s. Over the whole run, the minimum ratio D(1e-3)/D(1e-5) drops to 15.2 at
  N = 511, eps = 1e-4 (100 is linear). The δ = 1e-3 pair saturates late.

## Controls

| Control | Result | Numbers |
|---|---|---|
| C1 reproduce CFG321 (eps 1e-3, N ≤ 255) | PASS | lambda 0.0124 / 0.0414 / 0.0663 and Amax 95.1 / 338.7 / 1051.9, identical at the printed precision |
| C2 GR, MOND off (eps 1e-2, T = 10, N up to 511) | PASS | error order 2.00 / 2.00; drift order 2.04 / 2.01, 4.6e-5 at N = 511; max D/delta 2.41–2.51; pair ratio 100.0 |
| C3 MUTATE μ_exp (eps 1e-3, N 63–511) | fails as required, rc = 1 | all 12 runs: indefinite leaf Hessians (274–963 per run), then the leaf solve fails at t ≈ 6 |

## What would decide it

- **N = 1023 at eps = 1e-4**, about 6–8 h single-process with this engine. If r4 ≤ 0.6 the eps = 1e-4 set converges;
  if r4 ≥ 0.9 it fails.
- **N = 1023 at eps = 1e-3**, about 2–3 h. This gives the third ratio the convergent rule needs.
- **A faster leaf solver.** About 80% of the time is residual FFTs in the line search. That would need a new engine
  and a new lane; this one was barred from changing it.
- Not in scope: a C² splice of the kernel. The owner chose ν_mono.

## Files

| File | Contents |
|---|---|
| `FROZEN_CRITERIA.md` | frozen criteria (16139a770) + appended disclosures |
| `cfg322_engine.py` | byte-identical copy of CFG321's `cfg321_engine.py` (6cb69cdc1) |
| `cfg322_zero_field_resolution.py` | runs, lambda/Amax analysis, controls C1/C2, verdict; check() rows |
| `cfg322_zero_field_resolution.out`, `_results.json` | main run: 5/7 checks pass, verdict OPEN, wall 4504 s |
| `cfg322_zero_field_resolution_MUTATE.out`, `_MUTATE_results.json` | MUTATE: 2/4 checks, C3 PASS, rc = 1, wall 440 s |

Work arrays (~16 MB) go to `../_external_data/cfg322_work[_MUTATE]/`, relative to the repository root and outside
git. The script regenerates them.

Run from the repository root:

    python3 campaign_fresh_gravity/CFG322_zero_field_resolution/cfg322_zero_field_resolution.py                    # ~75 min, 14 processes
    CFG322_MUTATE=1 python3 campaign_fresh_gravity/CFG322_zero_field_resolution/cfg322_zero_field_resolution.py    # ~7 min, rc = 1
