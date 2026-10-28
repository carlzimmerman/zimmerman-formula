# CL2_native_cf_slope: FROZEN CRITERIA (committed alone, before any CL2 script or number)

**Why.** CL1 (947d12651f / bfbc7af384) combined CF2's decoupled switch with GS1's measured cluster gas budget. On the
canonical footing every graded line passes except one, which depends on c_f:

- groups need c_f ≳ 4.5 (Z +2.12 at 4.0, +1.98 at 4.5, T = 12.4);
- the all-cluster outer band (G-OUT-all) passes only at c_f ≤ 4.0 (−1.93 at 4.0, −2.01 at 4.25).

So groups (about 10^12.3–13.7 M☉) need roughly 10–15 % higher concentration than clusters (≳ 10^14). **The framework's own
zooms already give a concentration that falls with mass.** X48's nine-seed ng48 medians are 11.63 / 8.22 / 7.31 at 10^12 /
10^13 / 10^14 M☉ (A2); their level is above the data window and not converged (the ng64 runs are in progress).

**The question.** Keep the record's **one external number**, X43 has always carried one external c_f, but take the
**mass dependence from the native zooms**:

  c_f(M) = L · c_nat(M) / c_nat(10^14 M☉),

interpolated linearly in log M and clamped outside 10^12–10^14. L is the single external level, the same count as X43's
c_f. Is there an L for which every line passes? If so, the remaining group-versus-cluster tension is accounted for by
the native mass slope with **no added parameter**. If not, the native slope is insufficient or of the wrong shape.

κ = ½ FITTED. Footings 9.3603e-11 / 1.1312e-10 m/s², never pooled. Cold dark energy is a gravitating w ≈ 0 field
component, not matter and not a particle. Not "theory closed". No result here may be described as the data favouring the
framework.

## 1. Native shapes (pre-registered; read from committed X48 JSON at run time)

| shape | source | c_nat at 10^12 / 10^13 / 10^14 |
|---|---|---|
| **S9 (primary)** | nine-seed −2-crossing medians, `x48_analyze_results_ng48_A2.json` `cf_by_mass` | 11.63 / 8.22 / 7.31 |
| SN (variant) | nine-seed NFW-fit medians, from the same file's ng48 runs | 7.10 / 5.60 / 5.40 |
| S3 (variant) | three-seed ng48 medians, `x48_analyze_results_ng48.json` | 7.17 / 6.97 / 5.62 |

## 2. Harness

CL1's harness (CF2's decoupled switch and GS1's measured cluster budget), with c_f replaced by c_f(M) **consistently**:

- in X43, via η(M) = (4/3B(1)) c_f(M)^{5/4}, for SPARC, groups and clusters;
- in X53, via `eta_of`, for lenses above T.

The dwarfs are unchanged: their flag is satellite-only.

**Grid.** Switch T = 12.3, the middle of CF2's canonical window 12.2–12.5. L ∈ {3.75, 4.0, 4.25}. Shapes S9, SN and S3.
Both footings.

## 3. Step 0 (stop rule)

- **S0a.** With a flat shape (c_nat ≡ constant), L = 4 and T = 12.3, the grade reproduces CL1's committed T 12.3 / c_f 4
  point. Fail lists must match; groups Z and G-OUT-all Z must match to 0.01.
- **S0b.** The shape tables read at run time equal the values in §1 to 0.01.

## 4. Verdict (frozen, primary shape S9)

- **NATIVE SLOPE CLOSES THE GAP (canonical / alt / both):** some L passes every line on that footing with S9. The
  passing L values are listed.
- **NATIVE SLOPE INSUFFICIENT:** no L passes on either footing with S9. The binding lines are named.
- **Robustness:** ROBUST if SN and S3 give the same canonical class; otherwise FRAGILE, with the flipping shapes named.
- **Alt:** its known T-, c_f- and budget-independent failures (the SPARC line and the MW ultra-faints) are labelled
  separately, as in CL1.
- **Scope, frozen.** L remains one external number. A pass means the native **slope** works; it does not derive the level.
  The level awaits the converged native zooms.

## 5. Checks and twin

- **K1.** The switch property holds at every grid point.
- **K2.** c_f(M) is monotone non-increasing in M for each shape, as the native tables are.
- **K3.** Peak RSS < 1 GB, per process.
- **MUTATE (`CL2_MUTATE=1`, separate outputs).**
  - m1: the shape is inverted, c_nat(M) → c_nat(10^14)² / c_nat(M), which rises with mass.
  - m2: the S0a target × 1.01.
  - The twin must fail S0a and K2.

Run with `PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 -I cl2_native_slope.py`. Amendments only in
`AMENDMENTS.md`, each committed before the run it affects.
