# GS1_measured_gas_outskirts: the measured X-COP gas slope sets the cluster outer cold dark energy budget

## Provenance

- **Criteria:** `FROZEN_CRITERIA.md` (17064b9844).
- **Harness:** GC2 (3db544593b / 8f1554e920).

**Run conventions.** κ = ½ FITTED. Footings are never pooled. Cold dark energy is a gravitating w ≈ 0 field component, not
a particle. Not "theory closed". Nothing here says the data favour the framework.

## Measurement

The gas density slope beyond R500 comes from the 11 X-COP clusters with x_max ≥ 1.5 (A3266 is excluded; its x_max is 1.12):

- **s = 2.777**, the median, with bootstrap 16–84 % range [2.676, 3.071];
- per cluster from 2.04 (A2319) to 4.46 (A644);
- s(0.5–1 R500) = 1.91 (reported).

The record's "P" tail has s = 2 out to 2.2 R500; its "R5" tail has s = 3. The data are close to "R5".

## Verdict (frozen rule, both footings): **MEASURED SLOPE FAILS**

No rule passes every X43 line at s_meas.

| rule | at s_meas | at the bootstrap 84 % slope (3.07) |
|---|---|---|
| R4 (c_f = 4) | **all 15 cluster keys pass on both footings** (G-OUT-M3 −0.76 / −0.87; OUT-all −1.93; IN-Mall −1.26); SPARC passes; **groups +2.05 fail** | as at s_meas |
| R5 (c_f = 5) | cluster keys over-predict (G-MID-T3, G-OUT-all, G-IN-Mall OVER); groups +1.82 pass | passes the X43 line set |
| RX48 (native c_f) | over-predicts | — |

At the 16 % slope (2.68), every rule over-predicts more.

## Reading

With the measured gas slope counted to the self-consistent turnaround radius, the native fair share of cold dark energy
reproduces every cluster key at c_f = 4, and nothing is chosen. The cluster outskirt problem (G-OUT-M3) is resolved by
the measured gas budget.

What remains is the group line. Groups need c_f ≳ 4.25–4.75 (CF1), while clusters at the measured slope take c_f ≈ 4.
X48's native zooms give c_f falling with mass (7.2 / 7.0 / 5.6 at 10^12 / 10^13 / 10^14 M☉), which is the direction
required. A mass-dependent concentration is the open question.

The extrapolation of s_meas from x_max ≈ 1.5–2.1 out to r_ta is disclosed. Lensing and the dwarfs are not regraded here.

## Checks: 6/6

- S0a: s = 3 reproduces GC2's V-R5shape run exactly.
- S0b: 11 of 12 clusters.
- S0c: a synthetic r^−2.5 profile is recovered within 0.01.
- K1, K2, K3 (0.67 GB).
- **Pending:** the twin and the rerun.

## Files

- `gs1_gas_slope.py`
- `gs1_gas_slope.out` and `gs1_gas_slope_results.json`
- `runs/`
