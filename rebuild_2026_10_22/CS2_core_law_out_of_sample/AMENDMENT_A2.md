# CS2 AMENDMENT A2 (2026-10-27, post-result; corrects A1's diagnosis; committed alone before the rerun)

**A1 did not fix K0.** After A1, the dwarf comparator still missed by 8.8e-5 (canonical) and 4.2e-5 (alt). The a₀
rounding A1 named is real, but it is not the main cause.

**The real cause is the pivot.** OS1 and GR1 inherit σ_ref from SC1: the median SPARC V_last/√2 computed at run time,
70.49854608 km/s. This lane used the rounded 70.50 for both laws.

**Fix:**
- Every law now carries its own pivot:
  - OS1 comparator: Σ_a₀ (σ/70.49854608)^q_f, as OS1 and GR1 define it, with OS1's literal a₀ in the dwarf cap (A1).
  - CS2: 10^A (σ/70.50)^q, as calibrated in CS1 / CS2.
- Inside the record's machinery, which always divides by SC1's σ_ref, the CS2 amplitude is passed as
  10^A (70.49854608/70.50)^q. Then Σ_i = 10^A (σ_i/70.50)^q holds exactly.
  - This moves the CS2 numbers by a factor of 1 − 1.8e-5.
  - The native r₀ solver inverts σ with the same pivot.
- No tolerance, check, class rule or calibration changes.

**Recorded before the rerun** (first run and A1 run, identical):

| footing | lane class |
|---|---|
| canonical | CS2 TRADES |
| alt | CS2 NO BETTER |

So the verdict was UNDECIDED. Any change in the rerun is reported.
