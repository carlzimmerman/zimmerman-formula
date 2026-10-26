# IB1_inner_band_hse: FROZEN CRITERIA (committed alone, before the graded script exists or any graded number)

Written 2026-10-26, at the owner's request: "test the gas-equilibrium cluster halo (cold dark energy isothermal with the gas,
total fixed by hydrostatic equilibrium) on all 15 cells, groups and SPARC, both footings."

Standing rules:
- κ = ½ FITTED.
- Footings canonical / alt are graded separately and never pooled.
- Cold dark energy, not matter, never a particle.
- No ΛCDM number enters the rule. M_fair = 5.364 M_b is removed from clusters. Inherited ΛCDM-processed catalogue inputs are
  listed in §6.
- Nothing here says the data favour the framework. Not "theory closed".

## 0. Hypothesis HG (hydrostatic gas-equilibrium halo)

In a cluster with a hydrostatic hot atmosphere, the cold dark energy is isothermal at the gas's velocity dispersion,
σ² = kT/(μ m_p), with μ = 0.6. Both components then sit in one potential. The total mass is the gas's hydrostatic mass:

    M_tot(r) = −(σ² r / G) d ln ρ_g / d ln r = 3β σ² r³ / (G (r² + r_c²))

This uses the record's gas shape (F1/X2: β = 2/3, r_c = 0.15 R500). The cold mass is M_tot − M_b.

The rule has **no free constant**. Specifically:
- no q;
- no c_f;
- no M_fair;
- no r_ta normalisation.

Disclosed: an exact two-isothermal-component, equal-σ system gives ρ_c ∝ ρ_g with a self-gravitating (Lane–Emden) shape. The
operational rule above instead takes the measured gas shape as given and fixes the total by HSE. These are not identical.
The rule is the latter.

## 1. Model (graded run)

**Clusters (all 326, both h cells 0.672 / 0.686, both footings).**
- σ²:
  - the 106 clusters with KT > 0: kT/(0.6 m_p);
  - the 220 without: OS1's σ fill (`SIG_C`, the record's tercile fill), squared.
- r_c = 0.15 R500, with R500 as `prep` gives it (catalogue value scaled by qd to the h cell).
- **Truncation.** M_tot is held constant beyond r_t = 3 Mpc. That is the record's gas cut and the outer edge of the lensing
  bins.
- **Positivity.** M_tot(r) = max(M_HSE(r), M_b(r)) pointwise (no negative cold mass). The number of clusters where the floor
  binds anywhere at r ≤ 3 Mpc is reported.
- **Lensing.** Route E, Newtonian. It is the same projection, miscentring offset, reduced-shear factor and weights as OS1:
  `dvecN(i, foot, hk, M_tot)` from IC1's loader. The denominator is OS1's C\* vector, `DC`, unchanged.
- **The footing enters only through C\*** (the measured A and the C\* denominator). HG's mass does not depend on a₀.

**Groups (63, P4 T3): NOT A TEST.** The catalogue has no gas kT. The only available σ is the galaxies' σ_LOS, and P4's
estimator predicts σ_LOS. An isothermal halo at the measured σ_LOS returns σ_LOS by construction. Groups therefore keep
the core law (GR1 at OS1's q_f: CONSISTENT, Z +1.94 / +1.85). That status is quoted from GR1's JSON, not re-graded.

**SPARC (175): NOT A TEST.** Disc galaxies have no hydrostatic hot atmosphere, so HG does not apply. SPARC keeps OS1's core
law. OS1's SPARC line (0.0605 / 0.0591) is re-run as check K0 only. Its pass is not credited to HG.

**Scope consequence (stated now).** HG + core law is a two-regime rule. HG holds where a hydrostatic hot atmosphere is
measured; the core law holds elsewhere. What physically selects the regime is **not derived here** (cf. X19: no selector).
Any pass is a pass of the cluster rule only.

## 2. Grades (per footing; a cell passes only if |Z| ≤ 2 at both h)

The cells are the 15 X38/OS1 cluster cells, with OS1's measured A, errors and cell construction (`ic1b_lib.cells_from`):
- G-MID-T1..T3, G-MID-b;
- G-OUT-all, G-OUT-T1..T3, G-OUT-b;
- G-IN-all;
- G-OUT-Mall, G-OUT-M1..M3;
- G-IN-Mall.

| class | rule |
|---|---|
| **PASS** | all 15 cells pass |
| **IMPROVES** | G-IN-Mall's max over h of \|Z\| is below OS1's; none of OS1's 14 passing cells fails; at most G-IN-Mall still fails |
| **TRADES** | G-IN-Mall passes or improves, but ≥ 1 OS1-passing cell fails |
| **FAILS** | G-IN-Mall is not improved |

The verdict needs both footings to agree, else UNDECIDED.

**Reported, not graded:**
1. KT-only rule: the 106 KT clusters only. The cells are rebuilt on that subset, with the measured A on the same subset.
   This is OS1's KT_all line for INNER, MID and OUTER; the MGAS cells are not rebuilt.
2. Truncation at r_t = r_ta (`prep`'s turnaround) and at r_t = 2.2 R500.
3. Non-thermal pressure support: σ² × 1.15. A typical literature level, not fitted; context only.
4. The implied cold-core surface density Σ_HG = ρ_tot(0) r_c = 3·3β σ²/(4πG r_c), next to OS1's Σ_a0 (σ/σ_ref)^q_f, for the
   106 KT clusters: median ratio and spread.
5. Per-bin pred/meas (all 326), as D1.

## 3. Checks

- **K0.** IC1's loader reproduces OS1:
  - OS1's G-IN-Mall pred, both footings and both h, to 1e-9;
  - OS1's SPARC A rms at q_f to 1e-9.
- **K1.** For 5 test clusters (the 1st, 25th, 50th, 75th and 99th percentile of KT), the analytic M_HSE equals
  −(σ² r/G) d ln ρ_g/d ln r. The derivative is a numerical central difference of the record's `gas(…, "P")` density, taken
  on r ∈ [0.05, 2.0 R500] (inside the β-model part). Relative agreement must be 1e-5.
- **K2.** Peak RSS < 2 GB, one thread.
- **MUTATE** (`--mutate`, separate `_MUTATE` outputs). K1's analytic side uses 2kT. K1 must FAIL, and the script exits 1.
  The mutated grades are reported only.

## 4. Seen before freezing (disclosed)

IB1's diagnostics (b963ce381c) were run before this file. They used canonical and alt at h 0.672, on the **106 KT clusters
only**, with truncation at 3 Mpc:
- M_HSE lensing A: INNER 2.92 / 2.68, MID 1.63 / 1.49, OUTER 1.00 / 0.92;
- measured: 1.94 ± 1.67, 1.67 ± 0.34, 0.72 ± 0.17 (alt 1.78 ± 1.53, 1.53 ± 0.31, 0.66 ± 0.15).

This is the KT_all line of this lane (reported item 1). **Not seen:** any all-326 cell, any tercile cell, the MID slope, any
MGAS cell, h 0.686, the σ-fill clusters under HG, every reported variant above.

Expectation stated now: OUTER (KT_all) sat 1.7σ high in D3. The MGAS OUTER cells, which have smaller errors, are therefore
at risk of failing HIGH. A TRADES or FAILS class is a live outcome.

## 5. Outputs

`ib1_hse_halo.py` → `ib1_hse_halo.out` and `ib1_hse_halo_results.json` (`_MUTATE` for the control). Run with
`PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15`.

## 6. Inherited inputs (flagged)

| input | status |
|---|---|
| β = 2/3, r_c = 0.15 R500 | F1/X2 gas convention: fixed, not fitted per cluster |
| R500, Mgas500 | eRASS1 catalogue: **ΛCDM-processed**, rescaled by qd to the h cell |
| kT | one global temperature per cluster; isothermality assumed |
| μ = 0.6 | standard primordial-plasma value |
| non-thermal pressure | omitted from the graded rule |
| σ fill for 220 clusters | OS1/X30's tercile fill: an inherited regression |
| C\* denominator, offsets, reduced shear, weights, boost | the record's (X2/X7/X30) |
