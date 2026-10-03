# CFG322 — FROZEN CRITERIA: does CFG321's rising Lyapunov exponent saturate with resolution? (recipe G5/G10, zero-field nonlinear dependence)

Frozen 2026-10-03, before any CFG322 lane script was run. Nothing below may be edited after the commit that adds this
file. Corrections go in a dated section appended at the end.

**Disclosure before freezing.** Only timing probes were run (scratch directory, outside the repo), with the copied
engine: 1-D ν_mono base runs from data class D for short times (N = 255 and 511 at eps = 1e-3, T = 4; N = 255 at
eps = 1e-4, T = 4; N = 511 at eps = 1e-4, T = 1–2; N = 1023 at eps = 1e-3, T = 1) and one profile. No pair run, no
Lyapunov fit, no amplification, nothing past the growth phase (rms yhat <= 0.016 at the end of every probe). Purpose:
the wall-time budget. Result: the cost is in the leaf solver's residual evaluations (FFTs), not in BLAS (extra BLAS
threads gave no speed-up), and scales ~ N / sqrt(eps). Extrapolated full T = 80 runs (factor ~1.7 for the saturated
phase, from CFG321's N = 255 timing): N = 511, eps = 1e-3 ≈ 40 min; N = 511, eps = 1e-4 ≈ 100–130 min;
N = 1023, eps = 1e-3 ≈ 2–3 h; N = 1023, eps = 1e-4 ≈ 6–8 h.

## 1. What is being tested (committed, not chosen here)

- **The record.** CFG321 (frozen cb089fb29, results 6cb69cdc1) returned FAIL under its frozen rule on one signature:
  in the 1-D eps = 1e-3 set the pair-separation (Lyapunov) exponent rose with resolution at both steps,
  lambda = 0.0124 / 0.0414 / 0.0663 at N = 63 / 127 / 255, and the maximum amplification over the run went
  95.1 / 338.7 / 1051.9 (cfg321_verify_fail.py, V4). The 1-D eps = 1e-2 set and the 2-D set fell with resolution.
  CFG321 named the decider: N = 511 (1023 if affordable) and eps = 1e-4 pairs. Suspected cause: the ν_mono kernel's
  |w|^(1/2) kink at zero crossings.
- **The question.** Does lambda(N) saturate at a finite value as N → ∞ (continuous dependence with a finite Lyapunov
  time), or does it keep growing (discontinuous dependence: CFG321's FAIL confirmed)?
- **The system, unchanged.** CFG321's engine `cfg321_engine.py` is copied byte-for-byte to `cfg322_engine.py`
  (sha256 bde2fbb6abb12fad4e8392917b792374016fd8127da2a02dcaa8338ff8952174, git blob 8b3965a8ee12f4c1565f0effa8e737a06b19d84b
  at 6cb69cdc1). The script verifies the hash at start and aborts on a mismatch. Nothing is imported from CFG321's
  directory and nothing there is modified.
- **The kernel, unchanged.** ν_mono (owner decision 2026-09-26). No C² splice, no dealiasing, no smoothing: out of scope.
- **Parameters, unchanged.** alpha_c = L340 P1 maximum (read from the committed L340 JSON, as CFG321); data class D
  exactly as CFG321 §3 (seed 321 base field, seed 322 perturbation field, rms yhat = 1e-4, L = 16 xi, zero khronon
  velocity, g = 0); T = 80; outputs every 0.25; the engine's own time step rule and leaf tolerances. kappa = ½ is
  FITTED and plays no role.

## 2. Runs (fixed now)

- **Main (ν_mono, 1-D):** N ∈ {63, 127, 255, 511} × eps ∈ {1e-3, 1e-4} × delta ∈ {0 (base), 1e-3, 1e-5}: 24 runs.
- **N = 1023 is NOT run.** Its estimated wall time (2–3 h at eps = 1e-3, 6–8 h at eps = 1e-4, single process, not
  parallelisable within a run) exceeds the ~40 min budget. Even N = 511 at eps = 1e-4 exceeds it (~2 h); it is run
  because the lane's question requires it. Total wall ≈ the longest run, ~2 h, on ≤ 14 processes.
- **GR control (MOND off, ZeroKernel):** CFG321's C-GR set (eps = 1e-2, T = 10, delta ∈ {0, 1e-3, 1e-5}) extended to
  N ∈ {63, 127, 255, 511}.
- **MUTATE (env CFG322_MUTATE=1; outputs suffixed _MUTATE, work arrays in cfg322_work_MUTATE):** the μ_exp kernel
  exactly as CFG321's MUTATE (engine class MuExpKernel, a0 → y* a0), 1-D eps = 1e-3, N ∈ {63, 127, 255, 511}, delta
  ∈ {0, 1e-3, 1e-5}, with a per-run wall cap of 2400 s (status "wall" if reached).
- Each run is a separate worker process; the pool is ≤ 14 processes, BLAS threads 1.

## 3. Measured quantities (the same definitions as CFG321)

- D(t) = ||w_base − w_pair||_2 / ||w_base||_2 on the run's own grid, w = grad S u (the filtered field), every output.
- **lambda(N)** = the slope of a least-squares fit of ln D_{1e-5}(t) over the outputs with 1e-4 <= D_{1e-5} <= 1e-1
  (CFG321 §5 R3c). Fewer than 8 such points: "not reached".
- **Amax(N)** = max_t D_{1e-5}(t) / 1e-5 (CFG321 verify V4). Reported with the per-step ratios.
- Reported, not graded: lambda with the alternative windows (1e-4 <= D <= 1e-2; fixed [T/2, T]); the slope's standard
  error; R² of the fit; D(1e-3)/D(1e-5) over the run (linearity); tau_s (first output with rms yhat >= 0.1 in the
  finest run) and A = D_{1e-5}(tau_s)/1e-5; the saturated <rms yhat> over [T/2, T]; CFG321's FAIL signatures (both
  amplification steps > 2, both lambda steps > 1.25) re-evaluated on the last three grids.
- Regularity per run: status, maximum leaf residual, number of indefinite leaf Hessians, energy drift
  max|E − E0| / max E_kin.

## 4. Decision rule

Increments, per eps set: Delta_1 = lambda(127) − lambda(63), Delta_2 = lambda(255) − lambda(127),
Delta_3 = lambda(511) − lambda(255). Ratios r_2 = Delta_2 / Delta_1, r_3 = Delta_3 / Delta_2 (signed). "The last two
steps" are r_2 and r_3 (with 4 grids there are exactly two ratios).

**Degenerate denominators (declared now).** An increment with |Delta| < 0.005 counts as zero (0.005 ≈ the spread of
lambda across fit windows seen in CFG321's verification). If the denominator of a ratio is zero in this sense: the
ratio is taken as 0 if the numerator is also zero (a plateau), +∞ if the numerator is >= +0.005, and undefined (→ OPEN)
if the numerator is <= −0.005.

**Extrapolation (reported, used in the rule).** Geometric (Aitken/Richardson) on the last three grids:
lambda_∞ = lambda(511) + Delta_3 · r_3 / (1 − r_3), finite iff r_3 < 1. With a plateau (r_3 = 0) lambda_∞ = lambda(511).
Also reported: the power-law order p = log2(1/r_3) when 0 < r_3 < 1.

**Verdict.**
- **RESOLVED-CONVERGENT** if, in BOTH eps sets, |r_2| <= 0.6 AND |r_3| <= 0.6, lambda_∞ is finite, every ν_mono run
  is regular (below), and every control passes. G5/G10 nonlinear dependence then becomes CONDITIONAL (for data class D,
  the reduced model and the eps continuation, as CFG321 §7).
- **CONFIRMED-FAIL** if, in AT LEAST ONE eps set, lambda rose at the last step (Delta_3 >= +0.005) and r_3 >= 0.9
  (increments not shrinking, or lambda growing faster); OR any ν_mono main run blows up, fails a leaf solve, or hits
  an indefinite leaf Hessian at N = 511 (CFG321's frozen FAIL signatures for branching/blow-up). CONFIRMED-FAIL
  requires control C1 to pass (otherwise the engine reproduction is in doubt → OPEN).
- **OPEN** otherwise (including: lambda "not reached" at any grid of a set, an undefined ratio, a control failure that
  blocks RESOLVED-CONVERGENT, or ratios between 0.6 and 0.9).

**Stated in advance: RESOLVED-CONVERGENT is out of reach in the eps = 1e-3 set.** CFG321's printed values already give
r_2 = (0.0663 − 0.0414)/(0.0414 − 0.0124) = 0.86 > 0.6 for that set. With N = 1023 not affordable, there is no third
ratio, so the eps = 1e-3 set can end only CONFIRMED-FAIL (r_3 >= 0.9 with a rise) or OPEN, and the verdict cannot be
RESOLVED-CONVERGENT whatever N = 511 shows. The thresholds are kept as given; the lane reports this limitation rather
than relaxing them. The eps = 1e-4 set is new and unconstrained.

## 5. Controls

- **C1 reproduction (load-bearing).** The eps = 1e-3 rows at N = 63, 127, 255 reproduce CFG321's printed lambda
  (0.0124, 0.0414, 0.0663, 4 decimals) and printed Amax (95.1, 338.7, 1051.9, 1 decimal) exactly at that precision.
- **C2 GR (load-bearing).** MOND off: the error against the exact solution at T = 10 converges with order >= 1.8 at
  both of the last two steps (127→255, 255→511, fitted against the actual dt); the energy drift falls with order
  >= 1.8 over the same steps and is <= 1e-3 at N = 511; pairs bounded (max D/delta <= 10) and linear in delta
  (D(1e-3)/D(1e-5) at T within 100 ± 1%) at every N. (CFG321's N = 63 drift, 3.2e-3, is known and not graded here.)
- **C3 MUTATE (load-bearing, separate run).** The μ_exp runs must branch or fail: at least one run with an indefinite
  leaf Hessian or a failed leaf solve or a blow-up, and the MUTATE verdict must not be RESOLVED-CONVERGENT.
  The MUTATE script exits rc = 1 when this holds ("fails as required"), as CFG321.

## 6. Scope (stated in advance)

- 1-D only (CFG321's FAIL set was 1-D). Says nothing about growth or sigma_8: L341's failure (sigma_8 = 18–27) and FP2's
  failed linear cosmology stand whatever the verdict.
- A RESOLVED-CONVERGENT would lift CFG321's FAIL to CONDITIONAL for G5/G10 nonlinear dependence only, for data class D,
  the reduced model and the eps continuation. It would not be well-posedness of the full chassis and not a pass for
  candidate B, whose action does not exist.
- CFG321's frozen verdict (FAIL) is not re-read here; CFG322 is a new lane that rules on the open question it named.
