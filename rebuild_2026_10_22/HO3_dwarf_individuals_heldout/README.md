# HO3_dwarf_individuals_heldout: the CL2 picture gets the dwarf class medians right, but not the dwarfs one by one

Criteria: `FROZEN_CRITERIA.md` + `ASSUMPTION_LEDGER.md` (554597b160, committed alone, before any script or number).
κ = ½ FITTED. Footings never pooled; canonical is primary. Cold dark energy is not matter. Not "theory closed". Nothing
here says the data favour the framework.

**What was tested.** The frozen CL2 picture on X1's 89 LG dwarfs per footing, **object by object** (the calibrating
lanes X51/X62/CL2 graded only the five class medians):
- **76 satellites** (host MW/M31) carry route E: Newtonian baryons + X51's cooling-floor a₀-floor halo (X62's own
  machinery, unchanged; CL2's c_f(M) slope does not reach dwarfs on the a₀ floor).
- **13 isolated LG field dwarfs** follow the law on baryons, g = g_N ν(g_N/a₀). No dwarf crosses M200 = 10^12.3.

Residual Z_i = E_i / s_i, with s_i = X1's per-system error. Rules: S1 tail fraction (binomial p ≥ 0.01), S2 median |Z|
under the null 99th percentile, S3 worst object (p ≥ 0.01).

## Verdict (frozen): **HELD-OUT FAIL on both footings**

| | canonical (primary) | alt |
|---|---|---|
| **satellites (76)**: median E | −0.093 | −0.182 |
| \|Z\| ≥ 2 (S1) | **21 of 76, p 2e-11 ✗** | **22, p 2e-12 ✗** |
| median \|Z\| vs null 99 % (S2) | **1.23 vs 0.90 ✗** | **1.29 vs 0.90 ✗** |
| worst object (S3) | **Fornax −8.9, p 6e-17 ✗** | **Fornax −11.1 ✗** |
| **isolated (13)**: median E | +0.046 | +0.007 |
| \|Z\| ≥ 2 (S1) | **4 of 13, p 0.002 ✗** | 3, p 0.019 ✓ |
| median \|Z\| (S2) | 0.84 vs 1.24 ✓ | 0.88 vs 1.24 ✓ |
| worst object (S3) | **IC 1613 −6.8, p 2e-10 ✗** | **IC 1613 −7.5 ✗** |
| **Leo T** (law branch) | **+0.414 ± 0.154, Z +2.69: ABOVE** | **+0.374 ± 0.155, Z +2.41: ABOVE** |
| **Phoenix** (law branch) | **+0.405 ± 0.074, Z +5.47: ABOVE** | **+0.366 ± 0.075, Z +4.88: ABOVE** |

Reported (not graded):
- **Intrinsic scatter beyond the errors (ML):** satellites σ_int 0.27 / 0.28 dex, isolated 0.22 / 0.22 dex.
  - χ² is 502/76 (canonical) for satellites and 93/13 for isolated.
  - Post-run context, not graded: on X1's own columns, the law alone leaves σ_int 0.36 dex on the satellites. So the halos
    cut the satellite scatter but do not remove it. The isolated σ_int (0.22) is the law's own.
- **Satellites beyond 2σ, both signs.**
  - Over-predicted: Fornax −8.9, Boötes I −7.9, NGC 147 −7.3, Crater II −7.0, Cassiopeia III −4.7, Leo IV −3.9,
    Sagittarius −3.6, Hercules −3.4 …
  - Under-predicted: Draco +7.6, Andromeda VI +3.0, Segue 1 +2.9, Willman 1 +2.9, NGC 185 +2.5 …
  - Removing the tidally stripped Crater II and Antlia II changes nothing (20 of 74 beyond 2σ).
- **Isolated beyond 2σ:** IC 1613 −6.8 (the law over-predicts), Phoenix +5.5, Leo T +2.7, Pegasus dIrr +2.2.
  - Spearman(E, log M★) = −0.73 (p 0.005) on both footings: X24's field mass trend survives, system by system.
- Satellites show no mass trend (ρ +0.12 / +0.18). X51's cooling floor removes it.

**Checks 7/7.**
- **K0 (Step 0):** the copy reproduces X62's committed `x62_x51copy_on` class medians, Z and seven individuals, and
  X51's class medians, all to 1e-9.
- **K1:** 76 halo / 13 law per footing, 0 violations.
- **K2:** isolated E matches X1's independent iso-AQUAL column to a median 0.006 / 0.005 dex.
- **K3:** under the null the rules fail 2.9 % (N 76) and 2.4 % (N 13) of the time. A planted 2× scatter fails 100 %.
- **K4:** peak RSS 0.31 GB.
- **Rerun:** byte-identical. Results JSON sha256 `8e7e81a5…2877`; per-object CSV `27e955d3…2ab7`.
- **MUTATE twin** (`HO3_MUTATE=1`, flag inverted): fails K1 (89 violations per footing), plus K0 and K2. Exit 1.

## Reading

1. **The class medians hide a 0.2–0.3 dex per-object scatter.**
   - The picture centres both populations: satellite medians −0.09 / −0.18, isolated +0.05 / +0.01.
   - But a quarter of the satellites and a third of the isolated dwarfs sit beyond 2σ of their own errors, in both
     directions.
   - A single rule per population, a halo mass floor or the bare law, does not track individual systems.
2. **The environment key is not clean for isolated dwarfs** (as X24/X62 said). Leo T and Phoenix sit above the law at
   Z +2.7 and +5.5. IC 1613 sits 6.8σ below it. The field residual falls steeply with stellar mass (ρ −0.73). The law
   branch does not match the low-mass field dwarfs.
3. **The worst satellites are the high-precision ones.**
   - Fornax (s 0.019 dex), Draco (0.027) and NGC 147 (0.059) have small X1 errors. X1's sdMC appears to carry the σ and
     r_h errors but no stellar-mass (M/L) error (ledger A2/A3).
   - Gas is also left out of g_N (A3). Adding it would raise g_N and lower E for gas-rich dwarfs: it would pull Leo T
     and Phoenix toward the law and push IC 1613 further below it.
   - A realistic ~0.1–0.2 dex M★ error would shrink many |Z|. It would not remove a 0.22–0.27 dex intrinsic scatter.
     This is a disclosed limitation of the error model, not a rescue. The verdict stands as frozen.
4. **What this does not say.**
   - Nothing here tests SPARC, lensing, groups or clusters.
   - The CL2 class-median dwarf line is unchanged: canonical all five classes pass, alt keeps X51's UFD overshoot.
   - The fail is about per-object fidelity. No new constant is introduced, and none should be fitted from this lane.

## Disclosures

- **Not blind.** The isolated individuals (Leo T, Phoenix) and seven satellite individuals were already printed in X1,
  X24, X51 and X62 before the criteria were frozen (criteria §0). The satellites' halos were calibrated on these same
  objects' class medians.
- **Post-run code fix.**
  - The first run's combined-verdict line compared the full verdict strings. Both footings fail, with different rule
    lists, so it printed "SPLIT".
  - The frozen rule (§3) calls a SPLIT only when the verdicts disagree. The fix compares the verdict class, as X51 does.
  - No graded number changed. The rerun-identical hashes are from the fixed script.
- **K3's planted and null draws** use `default_rng([20261027, 3])`. The S2 null uses `default_rng(20261027)`, 4 × 5×10⁴ draws.

## Files

- `ho3_dwarf_individuals.py`
- `ho3_dwarf_individuals.out`, `ho3_dwarf_individuals_results.json`, `ho3_dwarf_individuals_per_object.csv`
- `_MUTATE` twins of the outputs
- `ho3_x51copy_{on,off}[ _MUTATE]` outputs of the read-only X51 copy

To reproduce:

    PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 ho3_dwarf_individuals.py              # exit 0, 7/7
    HO3_MUTATE=1 PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 ho3_dwarf_individuals.py # exit 1, K1 fails
