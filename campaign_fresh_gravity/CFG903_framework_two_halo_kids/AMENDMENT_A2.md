# CFG903 AMENDMENT A2: the neighbour kernel's numerics (POST HOC: after the first full score run, whose results were seen)

Committed with the first score run's script and outputs, kept unchanged:
- `cfg903_score_run1.py`;
- `cfg903_score_run1_K2fail.out`;
- `cfg903_results_run1_K2fail.json`.

## What failed in run 1

The three frozen kernel controls failed:

| control | run 1 | frozen tolerance |
|---|---|---|
| K2a: projected cold profile vs CFG804's `profile()` | 1.15e-2 | 5e-3 |
| K2b: F(x, 0) vs direct integration | 3.2e-3 (limits 2e-16 passed) | 1e-3 |
| K2c: uniform neighbour field | 1.7e-2 Σ₀ | 2e-3 Σ₀ |

## Diagnosis (post hoc diagnostics in the session scratch; numbers reproduced below by the rerun)

There are two numerical causes. Neither is physics.

1. **Table resolution.** The off-centre enclosed fraction F(ξ, υ) was read from a two-region lookup table by bilinear
   interpolation in (log ξ, log υ), with steps of 0.05 and 0.045 dex.
   - F grows like ξ¹⁻², so linear interpolation of F in log ξ has relative errors of about 0.5–1%.
   - The uniform-field residual alternates in sign from bin to bin and peaks where R matches a neighbour's extent.
   - Halving both steps cut it 1.1e-2 → 2.9e-3 (∝ h²).
2. **The q-integration.** The fixed 1,100-point q grid cannot resolve the step-like arc fraction φ(q) when υ ≪ ξ.
   This leaves a ~0.7% relative error in F(x, 0) even on a finer table.

## Fix (numerical only)

**F is evaluated directly** for every (d bin, R node) of every neighbour-mass cell. There is no table and no
interpolation in (ξ, υ). Lengths are in units of the profile's own cut radius:

F(ξ, υ) = [ C(min(ξ − υ, 1)) Θ(υ < ξ) + (1/π) ∫ from |ξ−υ| to min(ξ+υ, 1) of Σ(q) q φ(q) dq ] / C(1)

- C is the cumulative projected profile ∫ Σ q dq, on the same 1,100-point grid.
- The partial-arc integral uses 48-node Gauss–Legendre in θ, with q = a + (b − a)(1 − cos θ)/2 (endpoint clustering for
  the square-root ends of φ).
- Σ(q) is the same quad-integrated truncated law profile as in run 1.

**K2b re-expressed for a table-free kernel** (K2a and K2c unchanged):
- (i) F = 1 for υ ≤ ξ − 1 and F = 0 for υ ≥ ξ + 1, to 1e-6 (ξ = 1, 3, 100, 1e4; N = 1, 10).
- (ii) F at 24 random off-centre points (N = 1 and 10) agrees with an **independent brute-force polar-grid integration**
  about the lens centre (3000 × 3000) to ≤ 1e-3 absolute.
- F(x, 0) = C(x)/C(1) now holds by construction. Its difference from the cumulative is reported.

## Unchanged

Physics, data, histograms, weights, the completeness treatment of A1, classes, thresholds, brackets, fits, jackknife,
K0/K1/K3 and MUTATE. Stage A and stage B outputs are reused as they are.

## Disclosure: what run 1 showed before this amendment

| footing | primary class | all-radii Δχ² | brackets that changed the class |
|---|---|---|---|
| canonical | PARTIAL | +40.68 | I1, P0, E2 (W100 and W200, reported only, also lower) |
| alt | PARTIAL | +52.78 | I1, P0, P2, E2 (W100 and W200, reported only, also lower) |

- Primary range: SUFFICES held (−5.02 / −7.21).
- K1a, K1b and K3 passed.

The kernel errors act on lenses and randoms alike, so they largely cancel in the subtraction. The expectation is small
changes. The rerun reports every number and class against run 1.

κ = ½ FITTED; footings never pooled; framework-native; not theory closed.
