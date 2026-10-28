# GT1_gas_temperature_halo: the gas-state rule FAILS on both footings. G-OUT-M3 is still under-predicted (+3.25 / +2.72), and the hot-gas groups keep the wrong sign (D_pred +0.090)

## Provenance

- **Criteria:** `FROZEN_CRITERIA.md` (ef8161361e), committed alone before any script or number.
- **Amendments:** `AMENDMENTS.md` A1–A8 (1c28336cbd), committed alone before the script and before any GT1 number.
- **Harnesses:** executed read-only as text copies.
  - BS1's head (X43 / X53 / X51 copies, HO2's MW head);
  - X43 + X30 in IB1's configuration (K0);
  - HG2 / HG1 (groups and the D statistic);
  - CS2's X-COP rows (as HO1).
- **Run:** `PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 -I gt1_gas_temperature_halo.py`. It takes about 9 minutes, one thread, peak 0.64 GB.

**Run conventions.**
- κ = ½ FITTED. Footings 9.3603e-11 (canonical, primary) and 1.1312e-10 m/s² (alt) are never pooled.
- Cold dark energy is a gravitating w ≈ 0 field component, not matter and not a particle. ΛCDM appears only as the
  rival; no ΛCDM number enters a rule.
- **The shared isothermal potential is a posit.** No action is written for it.
- Not "theory closed". Nothing here says the data favour the framework.

## Verdict (frozen table, canonical primary)

| footing | verdict | (A) 15 cluster keys | (B) HG2 D_pred | (C) base lines |
|---|---|---|---|---|
| **canonical** | **GAS-STATE RULE FAILS: clusters (G-OUT-M3 (UNDER)); HG2 D_pred +0.090 (ABOVE [−0.511, −0.076])** | fail (G-OUT-M3 +3.25 / +2.72) | fail (+0.090) | pass |
| alt (its own) | GAS-STATE RULE FAILS: clusters (G-OUT-M3 (UNDER)); HG2 D_pred +0.062 (ABOVE [−0.511, −0.076]); base lines (SPARC line, dwarfs MW ultra-faint (OVER, Z −2.77)) | fail (same Z) | fail (+0.062) | fail (BS1's known alt lines, stated in A6) |

## The rule as run

For every eRASS1 cluster (all 326 are hot) and the 14 eRASS1-matched BRIGHT HG2 groups:
- **r ≤ R_g = R500:** M_tot = M_HG = 3β σ² r³ / [G (r² + r_c²)], with β = 2/3 and r_c = 0.15 R500.
- **r > R_g:** M_tot = M_HG(R_g) + k [M_CL2(r) − M_CL2(R_g)], with k fixed so that M_tot(r_ta) = M_budget (the GS1 native
  fair share to the self-consistent r_ta). If M_HG(R_g) ≥ M_budget, then k = 0.

**Where σ comes from.**
- Clusters: σ from kT (106 clusters). The other 220 take IB1 RF's fill, log σ = 0.9186 + 0.1393 log M_gas,500 (inherited,
  re-derived exactly).
- Groups: σ = σ_LOS (β_spec = 1, disclosed).

Everything without a hot atmosphere keeps the BS1 picture (S9, L = 4, T = 10^12.3, GS1 budget, basin switch).

## (A) Cluster lensing: 15 keys × 2 h cells (canonical; alt Z identical to 0.01)

| key | **GT Z** h 0.672 / 0.686 | CL2 = BS1 Z | IB1-HG Z (its own machinery) | GT pred / meas (h 0.672) |
|---|---|---|---|---|
| G-IN-Mall | −0.38 / −0.39 | −1.27 / −1.07 | −0.33 / −0.35 | 2.671 / 2.277 |
| G-IN-all | −0.59 / −0.68 | −1.06 / −1.11 | −0.59 / −0.68 | 2.921 / 1.936 |
| G-MID-T1 | +0.04 / +0.18 | −1.48 / −1.17 | −0.07 / +0.05 | 1.064 / 1.079 |
| G-MID-T2 | +0.90 / +1.18 | −0.85 / −0.38 | +0.80 / +1.07 | 1.335 / 1.618 |
| G-MID-T3 | −0.27 / −0.03 | −1.17 / −0.64 | −0.27 / −0.04 | 2.164 / 2.096 |
| G-MID-b | −0.02 / +0.11 | +0.62 / +0.79 | +0.19 / +0.32 | 2.228 / 2.214 |
| G-OUT-all | −0.98 / −1.07 | −1.93 / −1.90 | −2.02 / −2.27 | 0.930 / 0.780 |
| G-OUT-T1 | −0.68 / −0.71 | −1.03 / −1.02 | −0.99 / −1.07 | 0.681 / 0.442 |
| G-OUT-T2 | −0.61 / −0.50 | −1.21 / −1.02 | −1.09 / −1.06 | 0.836 / 0.682 |
| G-OUT-T3 | −0.37 / −0.54 | −1.05 / −1.08 | −1.34 / −1.58 | 1.175 / 1.090 |
| G-OUT-b | +0.70 / +0.46 | +0.46 / +0.27 | +0.44 / +0.18 | 1.046 / 1.533 |
| G-OUT-Mall | +0.48 / +0.50 | −1.37 / −1.23 | +0.32 / +0.17 | 0.883 / 0.929 |
| G-OUT-M1 | −0.59 / −0.48 | −0.35 / −0.21 | −2.02 / −2.10 | 0.663 / 0.488 |
| G-OUT-M2 | −0.74 / −0.55 | −1.39 / −1.06 | −0.37 / −0.32 | 0.863 / 0.762 |
| **G-OUT-M3** | **+3.25 / +2.72 FAIL (UNDER)** | −0.76 / −0.87 | +5.02 / +4.36 | 1.034 / 1.369 |

**How to read the IB1 column.** The IB1-HG column is IB1's own run (C\* denominator on the record's "P" baryons, tercile
fill, r_t = 3 Mpc). Its measured values differ slightly from the GT/BS1 machinery (for example, G-OUT-all meas is 0.716 there
and 0.780 here).

**Result.** GT keeps everything IB1's HG fixed:
- G-IN-Mall −0.38;
- all four MID cells;
- G-OUT-all, which moves from −1.93 (CL2) to −0.98;
- G-OUT-M1, which IB1 failed at −2.02, now −0.59.

It moves G-OUT-M3 from IB1's +5.02 to +3.25. It does not bring it inside 2. **14 of 15 keys pass. G-OUT-M3 fails in both h
cells, on both footings.**

**Per-bin pred/meas** (h 0.672, bins 0–7, innermost first):

| | bins 0–7 |
|---|---|
| GT | 1.74, 1.22, 1.01, 0.90, 0.87, 0.87, 1.04, 0.77 |
| base | 2.25, 1.59, 1.41, 1.27, 1.23, 1.20, 1.32, 0.90 |

Bin 0 is the null-test-failing bin (IB1).

**k and clamps** (h 0.672; the same on both footings, since M_HG and the budget carry no a₀):
- k median 1.13 (16–84 %: 0.69–1.24); KT clusters 1.134, filled clusters 1.130.
- **33 of 326 clusters are clamped at k = 0.** For them, M_HG(R500)/M_budget runs from 1.04 to 26.8.
- Median M_HG(R500)/M_CL2(R500) = 0.76. Median R500/r_ta = 0.131.
- 2 cluster-cells sit below the mass switch. GT applies to them anyway, since every eRASS1 cluster is hot (A2).

## (B) HG2 statistic

| | canonical | alt |
|---|---|---|
| base (CL2 / BS1), reproduced (HO1(b)) | +0.229 | +0.201 |
| **GT** (BRIGHT on GT, FAINT on the base) | **+0.090** | **+0.062** |
| measured (HG2) | −0.294, 95 % [−0.511, −0.076] | same |

GT moves D_pred by −0.14, toward the data, but it stays ABOVE the interval.

**Per BRIGHT group** (canonical; Δlog g = GT − base at HG1's radius):
- **Inside R500 (r/R500 0.39–0.91): the pull falls.**
  - 30988: −0.94
  - 42797: −0.74
  - 42734: −0.33
  - 46247: −0.11
  - 54625: −0.03
- **Beyond R500: the pull mostly rises** (7 of 8). The k-scaled outer profile carries the GS1 budget, which uses 1.2 × the gas to r_ta (A3).
  - 45174: +0.08
  - 40375: +0.13
  - 13418: +0.07
  - 14765: −0.10
  - 64192 (k = 0 clamp): +0.20
  - 28927 (clamp): +0.16
  - 31478: +0.26
  - 41220 (r/R500 3.26, clamp): +0.57
- **43296** (r/R500 0.89): +0.23.

The bright arm's median shift is small, so D stays positive.

## (C) Base lines (Step 0) and the open item

- With GT off, the run reproduces BS1's committed primary block to 1e-6 (every grade leaf, the MW box, the 13 field
  dwarfs).
- With GT on, SPARC (both backgrounds), the 63 groups and the FAINT groups' g_pred are bit-identical to the base.
- Lensing, the dwarf classes and the MW (13 cells pass L1 + L2a + L2b) are carried from that run, since they hold no hot
  system.
- **Canonical:** no non-cluster line fails.
- **Alt:** it fails BS1's known SPARC line and the MW ultra-faints.
- **Open item (stated in advance):** IC 1613 is Z −7.62 (canonical) / −8.44 (alt). Field S3 still fails. GT cannot touch
  it.

## Reported variants (not graded)

| variant | canonical cluster fails | G-OUT-M3 Z | clamped | D_pred canonical / alt |
|---|---|---|---|---|
| **primary** (R_g = R500, RF fill) | G-OUT-M3 | +3.25 / +2.72 | 33 | +0.090 / +0.062 |
| R_g = 0.7 R500 | **none** | +1.88 / +1.50 | 22 | +0.075 / +0.047 |
| R_g = r_ta/2 | G-OUT-all, G-OUT-M1, G-OUT-M3 | +4.89 / +4.19 | 170 | +0.116 / +0.088 |
| continuity offset | G-OUT-M3 | +4.02 / +3.45 | 0 | +0.091 / +0.062 |
| tercile σ fill | G-OUT-M3 | +3.27 / +2.74 | 36 | +0.090 / +0.062 |
| literal R_g = r_ta, k unused (A1) | G-OUT-all, G-OUT-M1, G-OUT-M3 | +4.92 / +4.23 | (empty outer) | +0.116 / +0.088 |

- **R_g = 0.7 R500** passes all 15 cluster keys. It is a reported variant chosen in advance, **not** the frozen primary, and
  it is not promoted here. Doing so would be choosing R_g after seeing the grade. It still fails (B).
- **No variant** brings D_pred inside the interval: it stays between +0.047 and +0.116.
- **The tercile fill** gives the same answer as the RF fill, so the σ fill is not the cause.

## Verifying the failure

**G-OUT-M3 (UNDER).**
- Inside R500, the hydrostatic mass is about 0.76 of the CL2 mass (median).
- The outskirts are built by adding the CL2 increments (× k ≈ 1.13) on top of that lower base. So between R500 and about
  3 Mpc, the gas-rich clusters stay short of the lensing.
- 33 clusters already exceed the native budget at R500 (clamped). Their outskirts are flat.
- The failure holds:
  - with either σ fill;
  - in the continuity-offset form;
  - at r_ta/2;
  - on both footings and in both h cells.
- Only moving R_g inward (0.7 R500, reported) clears it.

**HG2 (ABOVE).** The base reproduces HO1(b) exactly. The bright arm's GT pull falls inside R500 and rises outside it. HG1's
radius r = (4/3) R_h lies beyond R500 for 8 of the 14 BRIGHT groups, and those carry the GS1 budget. In every variant D_pred
stays positive.

**Machinery.** Every reproduction is exact to 0.0:
- IB1's +5.02 / +4.36 and RF cells;
- BS1's grade;
- HO1's D_pred.

So the failures are the rule's, not the harness's.

## X-COP construction residual (K4, reported, not graded)

**NOT A TEST inside R500** (criteria §2). Δ = log g_obs − log g_GT on CS2's 35 points:

| | mean Δ | rms |
|---|---|---|
| GT | +0.295 dex | 0.320 |
| base (HO1) | −0.002 | 0.126 |

- Per radius, 0.1 to 0.7 R500: +0.35, +0.26, +0.28, +0.30, +0.29.
- Per cluster:
  - A1795 +0.33
  - A2029 +0.43
  - A2142 +0.36
  - A2319 +0.37
  - **A644 +0.05**
  - A85 +0.29
  - ZW1215 +0.22

**Why the residual is large.** Only A644 (eRASS1 kT 7.66 keV) and ZW1215 (eRASS1 kT 3.80 keV) match an on-disk kT (A4). The
other five take the RF fill, σ 695–778 km/s. That fill was fitted on the eRASS1 × KiDS sample, whose median kT is 1.67 keV,
so for X-COP's hot clusters it under-fills σ². With a measured kT (A644), the construction residual is +0.05 dex.

So "agreement by construction" holds only where the gas temperature is measured. The large X-COP offset is a statement
about the fill, not a graded line.

## SLUGGS

**NOT A TEST.** There is no X-ray kT on disk. A hydrostatic mass from the stellar σ would be a Jeans mass of the same
kinematics that are graded, which is circular.

Under the base picture (HO2, unchanged under BS1): FAILS on both footings, mean +0.152 dex, 1 of 4 clear.

## Checks: 6/6 (normal run)

- **K0a.** GT off reproduces BS1's committed primary block (grade, MW box, field dwarfs) to 1e-6. Max |d| 0, fail lists
  exact.
- **K0b.** HO1(b) D_pred +0.2293 / +0.2011, |d| 0.
- **K0c.** IB1's configuration (A1) reproduces IB1 HG (tercile) and RF: all 15 keys × 2 h × 2 footings, pred and Z, |d| 0;
  G-OUT-M3 +5.02 / +4.36; RF (a, b) |d| 0.
- **K1.**
  - Every hot system's M_tot(R_g) equals M_HG(R_g), and the inner grid matches, against an independent analytic side:
    max rel 0 for the 1304 cluster profiles and for the BRIGHT groups.
  - Non-hot lines equal the base exactly.
- **K2.** Every k > 0 profile reaches M_budget at r_ta: max rel 2.2e-16 over 4150 cluster profiles, and the same for the
  groups.
- **K3.** Peak RSS 0.64 GB per process, one thread.
- **Rerun.** The second normal run's results JSON is byte-identical (`cmp`). The `.out` differs only in timing stamps.
- **MUTATE** (`GT1_MUTATE=1`, separate `_MUTATE` outputs; σ² doubled on K1's analytic side): K1 fails (max rel 0.5,
  clusters and groups), checks 5/6, exit 1.

## Disclosures

- **A1:** the literal "R_g = r_ta" cannot give IB1's +5.02. K0 reproduces IB1 in its own configuration; the literal profile
  is reported.
- **A3:** the BRIGHT groups' M_CL2 (HO1's profile, extended in radius) and M_budget (GS1's `_gc2_ext`, with the 1.2 gas star
  factor, not the group's M★) were defined before the run.
- **Inherited conventions:**
  - β = 2/3 and r_c = 0.15 R500;
  - the ΛCDM-processed R500 inside r_c (IB1's);
  - the RF σ fill;
  - σ_LOS standing in for kT in groups.
- **Not blind.** The measured D and IB1's G-OUT-M3 were known when the rule was frozen.
- The 63 Tian groups carry no hot-gas flag and keep the base.

## Files

- `gt1_gas_temperature_halo.py`
- `gt1_gas_temperature_halo.out` and `gt1_gas_temperature_halo_results.json`, with their `_MUTATE` twins
- the per-run copy outputs: `gt1_x43copy_*`, `gt1_x53copy_*` and `gt1_x51copy_*`
- the `*.log` machinery logs are local only (gitignored)
