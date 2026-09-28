# AS030 — A shared deep limit is not a shared finite law

**Run:** `AS030_20260928T002346Z` (worker `sa-9-dbc1745a`, delegation `deleg_e7a106e5`;
orchestrator completion: Lean compile verification + result.json/derivation.md finalized
after the worker's compute process was SIGTERM'd (exit 143) at the end of its run).

**Outcome:** `supports_scoped_claim` — the shared deep asymptote x ~ sqrt(y) across
Q, RAR, MU2, EXP and MONO cannot certify equality of the finite laws; the task's
negative control (test equality only at y -> 0 and show it cannot certify y = 1)
**fails exactly as required**.

## 1. Claim and symbol dictionary

Branches (all dimensionless, y = B/a0 > 0, x = g/a0 > 0):

| Branch | Response | Deep limit x/sqrt(y) |
|---|---|---|
| Q   | x = sqrt(y^2 + y) | 1 |
| RAR | x = y/(1 - exp(-sqrt(y))) | 1 |
| MU2 | y = x·mu2(x), mu2(x) = 1 - (1 + x/2)^(-2) | 1 |
| EXP | y = x(1 - exp(-x)) | 1 |
| MONO | h'_mono = max(h'_RAR, delta·h_p/(y + y_p)), delta = 0.05, spliced at y* | 1 |

Precise claim: all five branches share the deep asymptote x = sqrt(y)·(1 + O(sqrt(y))),
but pairwise differences at finite y are O(1) — a shared limit point is not a shared law.

## 2. First correction beyond sqrt(y) on each branch

- **Q:** x = sqrt(y)·sqrt(1 + y) = sqrt(y)·(1 + y/2 - y^2/8 + …) → first correction +sqrt(y)·y/2. Exact identity x_Q/sqrt(y) = sqrt(1 + y) (Lean-certified, `xQ_ratio_id`).
- **RAR:** x_RAR(y)/sqrt(y) = s/(1 - e^(-s)) with s = sqrt(y) → 1 + s/2 + s^2/12 + … → first correction +sqrt(y)/2 (lean: squeeze 1 ≤ s/(1-e^(-s)) ≤ 1 + s).
- **MU2:** deep-algebra y/x^2 = (1 + x/4)/(1 + x/2)^2 → x = sqrt(y)(1 + x/4)^(1/2)/…; bounds 1 - x ≤ y/x^2 ≤ 1 + x certified; first correction +sqrt(y)·x/4 ≈ +y/4… (monotone implicit inversion, unique root).
- **EXP:** y = x(1 - e^(-x)); x = sqrt(y) + y/4 + (7/96)y^(3/2) + … (sympy series; the worker's rev2 log gives compose+expand order 3..6 coefficients; series_coefficients.json).
- **MONO:** RAR splice at y* = 2.3374 (h_RAR(y*) = h_star = 0.6469602869591…, h_p = 0.64761023787…), exact crossing y_cross = 2.337410905 (|y_cross − 2.3374| = 1.09e-5, consistent with AS033's 2.337412405 within the adopted-landmark tolerance); the continuation carries the same deep limit by the RAR bound.

Signed differences at y = 0.01, 1, 100 (mpmath 50-80 dps; landmarks.json):
knee at y = 1: deviation from asymptote — Q 0.41421356, RAR 0.58197671, MU2 0.48928857, EXP 0.34997649, MONO 0.58197671; pairwise spread 0.23200022 (>20% of the unit asymptote). At y = 100: h_RAR = 0.0045402 vs h_MONO = 0.7455822, difference 1.1443·h_p — the operative MONO log-extension is already 164× the RAR phantom at y = 100.

## 3. Negative control (capable of failing — it fails, as required)

`nc_deep_pair_Q_EXP`: at y = 1e-10, |x_Q − x_EXP| = 2.5000e-11 = 2.500e-6·sqrt(y) → the branches look identical at y -> 0. At y = 1: |x_Q − x_EXP| = 0.0642371 = 6.4% of sqrt(1). Ratio of differences d(1)/d(1e-10) = 2.5695e9. **Verdict: equality at y → 0 holds (shared asymptote) but the certification inference FAILS** — one cannot certify equality of the laws from the shared asymptote.

`nc_RAR_MONO_y100`: verifies the operative-vs-comparison distinction at finite y (above).

MONO spec reproduction (FRIED_CHICKEN_SPEC operative text): continuous max-dex search with the exact crossing gives max-dex = 0.01037015 at y = 14.3505 vs spec claim 0.0104 at y = 14.35 — matches to 3e-5 dex and 5e-4 in y. PASS. Splice continuity: |h_mono(y* + 1e-12) − h_RAR(y*)| = 6.64e-15; derivative residual at splice h'_RAR(y*) − δ·h_p/(y* + y_p) = 3.79e-7 (adopted-landmark rounding; exact crossing residual 0 per AS033's solver).

## 4. Independent checks

- Grid y = 10^k, k = −10..8 (step 0.1) with landmarks in all five branches (landmarks.json); 50-dps mpmath.
- Lean certificate: 43 theorems — Q ratio identity + squeeze + both limits, RAR closed forms + raw/clean derivatives + deep/Newtonian limits, MU2/EXP positivity (StrictMonoOn → unique root) + deep-algebra bounds, MONO continuation derivative plus splice continuity. Compiled with `lake env lean`, zero `sorry`, axioms exactly {propext, Classical.choice, Quot.sound} (lean_check.out).
- sympy series for EXP (first orders verified; rev2.log) and per-branch leading-neglected-term derivations.

## 5. Strongest surviving statement

x/sqrt(y) → 1 on every branch as y → 0+, but the finite laws are pairwise distinct at O(1) level
(Q vs EXP differ by 6.4% of the asymptote at y = 1; MONO vs RAR by 1.14 h_p at y = 100).
The shared deep limit thus carries no equivalence relation on the constitutive set; a task
concluding "branch X ≈ branch Y because both are deep-MOND" is unsupported.

## 6. Next unresolved implication

The operative filtered MONO field equation: does the heat filter S = exp((ξ²/2)Δ) scale the
finite-y branch separations (0.0104-dex envelope at y = 14.35) into the physical rotation-curve
band, or does it re-select the RAR segment at finite ξ? (Bridges to the 3-D filtered force map —
requirement-1 gate, cf. AS035.C01 planning.)

## 7. Bounds and limitations

- Bounds: alarm 120 s / 1 thread; actual wall 38.199 s, maxrss 141.7 MB (recorded in console_run.log). RLIMIT_AS not enforceable on macOS — reported honestly.
- κ = 1/2 adopted (not derived); both footings apply since the result is dimensionless (a0 = 9.3619e-11 and 1.1279e-10 m/s^2 across y = B/a0).
- Transcendental roots (y_cross) carried numerically; the exact crossing is AS033's result; adopted landmark y* = 2.3374 per spec used where solver precision was culled.
- No dynamics/filter exercised; constitutive-level statement only.

**Artifacts:** compute_as030.py, controls_and_checks.json, landmarks.json, series_coefficients.json, grid.csv, raw_outputs/console_run.log, AS030_deep_limit_branches.lean, lean_check.out.