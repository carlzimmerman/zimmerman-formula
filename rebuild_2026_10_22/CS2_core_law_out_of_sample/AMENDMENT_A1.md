# CS2 AMENDMENT A1 (2026-10-27, post-result; check-definition fix; committed alone before the rerun)

**What failed.** The first full run failed K0 on both footings. The only part that missed was the dwarf comparator:

| footing | max \|Δ\| (frac, median S) | frozen tolerance |
|---|---|---|
| canonical | 7.5e-5 | 1e-9 |
| alt | 3.4e-5 | 1e-9 |

The other parts of K0 passed: eRASS1 cells ≤ 3e-7, groups ≤ 3e-14, SLUGGS ≤ 8e-16.

**Cause.** OS1's dwarf cap is CAP · a₀ with a₀ taken from OS1's rounded literals, 9.3603e-11 and 1.1312e-10.

This lane builds the OS1 law from SC1's Σ_a₀, which uses CFG4's unrounded a₀: 9.360324825e-11 and 1.131203541e-10. The
two differ by 3.5e-6 and 3.1e-6 in relative terms.

The CS2-law dwarf grade does not contain a₀ at all: its cap is 0.254484 · 2πG · 10^A (σ/70.5)^q. So only the OS1
comparator is affected.

**Fix.** When the dwarf grader runs the OS1 comparator, it uses OS1's literal a₀, exactly as OS1's own code does:
cap = CAP · A0_OS1[foot] · (σ/σ_ref)^q_f. Nothing else changes:
- no tolerance;
- no other check;
- no class rule;
- no CS2-law number.

**First run's graded result, recorded before the rerun:**
- the lane class was CS2 TRADES (canonical) and CS2 NO BETTER (alt), so the verdict was UNDECIDED;
- the dwarf comparator's fraction with z ≥ 2 was 0.652 / 0.483, the same as OS1's record to the printed precision.

The rerun's classes must therefore match the first run; any change is reported.
