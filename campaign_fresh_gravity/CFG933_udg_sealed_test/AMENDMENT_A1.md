# CFG933 AMENDMENT A1: K1's CFG31-R1 sub-check uses CFG31's own kernel (control tolerance, not physics)

**Dated** 2026-10-20. **Post hoc:** written after the first K-only run (`CFG933_MODE=K`), and committed alone before the
script is changed.

**What had been seen when this was written.** The K-only run computes and prints only K numbers:
- L23-estimator offsets, which equal the record's already-known +0.3965 / +0.357 dex;
- maximum differences.

The sealed estimator's E_obs and E_pred for the UDGs are computed inside K3/K5 only as identity checks. Neither they, nor any
sample mean, se or class, were printed or stored. No number of the test itself had been seen.

## What failed

K1 has three sub-checks (criteria section 8):
1. L23's printed offsets within 6e-4: **passed** (canonical 1.7e-5, alt 2.7e-4).
2. CFG31's C1 "mine" within 1e-9: **passed** (difference 0).
3. CFG31's R1 stars-only at the campaign footings within 1e-9: **failed**. The differences are 1.63e-9 (canonical) and 1.89e-9
   (alt) dex.

## Why

CFG31's R1 used the contract kernel ν_mono (CFG4_common → FP1_static_sector.py, L340's table). That kernel is a tabulated,
trapezoid-integrated and interpolated version of h_RAR on a 280001-point log grid. This lane's path uses the analytic
ν_e = 1/(1 − exp(−√y)), the kernel of the sealed estimator (cfg921/cfg928). At y ≈ 0.003–0.02, where the UDGs sit, the two agree
to a few parts in 1e9. That is the tabulation error, not a different law. The 1e-9 tolerance was set in the criteria without
checking which kernel CFG31's R1 used.

## Change (and nothing else)

K1's third sub-check becomes two sub-checks:
- **(3a)** CFG31's R1 stars-only is reproduced through **CFG31's own kernel** within 1e-12. The kernel is FP1's committed ν_mono,
  exec'd read-only from the text of FP1_static_sector.py between `def _h_rar(y):` and `KER, KNAME = `, exactly as
  CFG4_common slices it.
- **(3b)** The analytic-ν_e path differs from (3a) by at most 1e-8 dex. The difference is reported.

Sub-checks 1 and 2 are unchanged. Nothing else changes: not the sample, estimator, errors, classes, S-set, R rows, K2–K5 or
MUTATE. The sealed estimator keeps the analytic ν_e.

κ = ½ FITTED; footings never pooled; not theory closed.
