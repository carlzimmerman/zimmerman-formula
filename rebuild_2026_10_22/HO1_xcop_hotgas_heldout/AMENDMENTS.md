# HO1 AMENDMENTS

## A1 (2026-10-27, post-result; a check-definition fix and a label fix; committed alone before the rerun)

**What failed.** The first normal run (exit 1, checks 8/9) failed K2 at 3.6e-4, against a frozen bar of 1e-5.

**Cause** (found by `ho1_k2_diagnostic.py`, post-run, not graded). The harness's fixed-point residual interpolated the
profile that `_gc2_ext` *returns*. That profile is already truncated, capped at M_b,t for r > r_ta. Interpolating a
truncated grid profile at r_ta lands between an uncapped and a capped grid point, so it reads slightly low.

The GS1 budget itself is fine:
- **start independence is exact**: × 0.3, × 1 and × 3 starts give the same M_b,t to the printed precision, for all 7
  clusters;
- iterating the truncated profile further moves M_b,t by 2.7–3.9e-4;
- shifting every M_b,t by ± 4e-4 moves the X-COP grade by ≤ 1.0e-4 dex (canonical mean −0.00213 / −0.00223, rms 0.1258
  either way).

So no class can change.

**Fix.**
- K2 keeps its frozen start-independence test (× 0.3 and × 3 against × 1, 1e-5 relative).
- The residual term, which was computed on the truncated profile, is dropped. `_gc2_ext`'s own convergence test (relative
  r_ta step < 1e-6) stands in its place, as in GS1 and CL2.
- No tolerance, rule, class or graded number changes.

**Label.** A failing X-COP verdict now names the failing condition(s) ("mean" and/or "rms"), as well as OVER / UNDER from
the sign of the mean. The pass rule is unchanged.

**First run's graded result, recorded before the rerun.** The two footings agree:

| line | canonical | alt |
|---|---|---|
| (a) X-COP mean Δ | −0.002 | −0.002 |
| (a) X-COP rms Δ | 0.126 | 0.126 |
| (a) X-COP verdict | FAIL (rms > 0.10; the mean passes) | FAIL |
| (b) HG2 D_pred | +0.229 | +0.201 |
| (b) HG2 verdict | FAIL (ABOVE the measured [−0.511, −0.076]) | FAIL (ABOVE) |
| lane | CL2 PICTURE FAILS | CL2 PICTURE FAILS |

The rerun must give the same numbers. Any change is reported.
