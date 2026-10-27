# GS1_measured_gas_outskirts: FROZEN CRITERIA (committed alone, before any script or number)

**Why.** GC2 (3db544593b / 8f1554e920) found that the outer cold dark energy budget of clusters hinges on the gas density
slope beyond R500, when the record's gas profile is counted to the self-consistent turnaround radius:

| gas profile beyond R500 | outcome |
|---|---|
| "P" tail (β = 2/3 to 2.2 R500, then r⁻³) | overshoots: R4 G-OUT-M3 −4.77 |
| "R5" tail (r⁻³ from R500) | R5 (c_f = 5) passes every X43 line on both footings |

That slope is a **data question**. The record holds X-COP's measured gas-mass profiles (12 clusters,
`real_research/data/xcop/<cluster>/<cluster>_fgas_profile.fits`, columns RADIUS in R/R500 and MGAS). This lane measures the
slope and regrades with it. Nothing is chosen.

κ = ½ FITTED. Footings 9.3603e-11 / 1.1312e-10 m/s², never pooled. Cold dark energy is a gravitating w ≈ 0 field
component, not matter and not a particle. Not "theory closed". No result here may be described as the data favouring the
framework.

## 1. Measurement (frozen)

**Per cluster.** For each X-COP cluster, use the MGAS profile at radii x = r/R500 ∈ [1, x_max], where x_max is the
largest tabulated radius (it must be ≥ 1.5, or the cluster is excluded and counted):

- compute the log-derivative d ln(dM/d ln r)/d ln r by a least-squares line of ln(ΔM/Δln r) against ln r on the tabulated
  points;
- the density slope is then s = 3 − that slope (since ρ ∝ r^{−s} implies dM/d ln r ∝ r^{3−s}).

**Sample.** s_meas is the median over clusters. Its uncertainty is a bootstrap over clusters (seed 0, 10000 draws), which
gives the 16–84 % range.

**Reported only:**
- the median slope over x ∈ [0.5, 1];
- the shape comparison. The "P" tail has s = 2 at 1–2.2 R500; the "R5" tail has s = 3.

## 2. Regrade (frozen)

**Harness.** GC2's harness (native normalisation; gas counted to the self-consistent r_ta), with the tail beyond R500
replaced by **ρ ∝ r^{−s_meas}**. The tail is continuous at R500 with the record's β-model, and it is extrapolated from
x_max to r_ta (disclosed).

**Rules:** R4, R5 and RX48.

**Reported only:**
- the same regrade at the bootstrap 16 % and 84 % slopes;
- the "P" and "R5" shapes, as GC2.

## 3. Step 0 (stop rule)

- **S0a.** The harness reproduces GC2's committed V-R5shape run exactly when s = 3: R5 G-OUT-M3 Z +0.49 / +0.33, and
  groups Z +1.82.
- **S0b.** At least 10 of the 12 X-COP clusters have x_max ≥ 1.5.
- **S0c.** The fitted log-derivative reproduces a synthetic r^{−2.5} profile on the same radial sampling within 0.01.

## 4. Verdict (frozen, per footing)

- **MEASURED SLOPE PASSES (rule …):** with s = s_meas, the named rule passes every X43 line (SPARC on both backgrounds,
  groups, all 15 keys in both h cells).
- **MEASURED SLOPE FAILS:** no rule passes. The failing lines are named.
- **Robustness.** ROBUST if the class is unchanged at both bootstrap-edge slopes; otherwise FRAGILE.
- **Scope statement, frozen.** A pass here is scoped to the X43 line set. KiDS lensing (X53) and the dwarfs (X51) are
  regraded in a follow-up if any rule passes. c_f = 5 (R5) is external.

## 5. Checks and twin

- **K1.** s_meas lies within [1, 5] (physical sanity).
- **K2.** The extended budget is continuous at R500: the profile ratio at R500 is 1 within 1e-9.
- **K3.** Peak RSS < 1 GB, one thread.
- **MUTATE (`GS1_MUTATE=1`, separate outputs).**
  - m1: the radius column is scaled by 1.5 before the fit, which mis-places R500.
  - m2: the S0a target × 1.01.
  - The twin must fail S0a and S0c.

Run with `PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 -I gs1_gas_slope.py`. Amendments only in `AMENDMENTS.md`,
each committed before the run it affects.
