# A41 mutations

Four single-line mutations, each a plausible slip in this lane's chain, each run through the same
`a41_checks.py` that produces `a41.out`. Clean run: **22/22 PASS, exit 0**. Every mutation exits 1.

| flag | the slip | fails | first wrong number |
|---|---|---|---|
| `--mutate` | **M1 inversion offset**: `u = P_l/(D-P_N)` — the phantom is divided by the excess *including* the baryons, i.e. the baryon subtraction is dropped from the numerator | K3, K22 | u(bin 2) = 0.4354 instead of 0.3331 (31% high) |
| `--mutate2` | **M2 no step**: the model is a single constant `u` for all eight bins (the "u is just a number" reading) | K8 K9 K11 K12 K13 K14 K15 K16 K17 K19 | best u = 0.566, chi2 = 39.9/7 = 5.70 (clean: 9.96/7 = 1.42); Delta chi2 of every rival collapses to 0 |
| `--mutate3` | **M3 wrong boundary**: `r_sp = R500 = 0.7845 Mpc` (the X-ray boundary) instead of 1.3674 r200c = 1.4138 Mpc | K4 K8 K11 K12 K13 K14 K15 K16 K17 K19 | r_sp/r200c = 0.759 instead of 1.367; step chi2 52.5/7 = 7.50; the kink moves into bin 3-4 and the predicted s(1.18-1.71) becomes 0.00 |
| `--mutate4` | **M4 jackknife normalisation**: `(n-1)/n^2` instead of `(n-1)/n` in the covariance — the classic error, making every error bar sqrt(n) = 5.4x too small | K8 K9 K15 K20 K21 | sigma(D) at 2.49 Mpc = 0.31 instead of 1.65; chi2(step) = 298.9/7 = 42.7 |

Reproduce with:

```
python3 a41_checks.py                # 22/22 PASS, exit 0
python3 a41_checks.py --mutate       # 20/22, exit 1
python3 a41_checks.py --mutate2      # 12/22, exit 1
python3 a41_checks.py --mutate3      # 12/22, exit 1
python3 a41_checks.py --mutate4      # 17/22, exit 1
```

Each mutation writes its own `a41_MUTATEn.out` / `a41_results_MUTATEn.json`, so the ledger is
self-documenting. Two notes on what the mutations are *for*:

- **M1** is the only mutation that leaves the DeltaSigma-space fits untouched (they never use `u`):
  it breaks exactly the two checks that do use the inversion (K3, K22). That is the intended
  behaviour -- it demonstrates that the headline fit does not pass through the u-space estimator at
  all, so an error in that estimator cannot manufacture the result.
- **M4** is the mutation that matters most for the claimed significances. Every "N sigma" in
  `report.md` is a Delta chi2 with the full 30-patch jackknife covariance; dropping the (n-1)/n
  factor inflates all of them by 5.4x. The clean run's chi2/dof = 1.42 for the one-parameter step
  is the evidence that the normalisation is right (a wrong one shows up immediately as chi2/dof
  far from 1 in either direction).
