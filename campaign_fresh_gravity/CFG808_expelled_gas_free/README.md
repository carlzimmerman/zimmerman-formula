# CFG808: H-EX with a POOLED supply. FAIL (an implementation flaw; superseded by CFG809)

**Result:** free/supply = 0.000 in every system. The settled law of all retained baryons absorbed the whole pooled supply,
including the expelled share. So the run is identical to CFG727's 'ALL' control (K1 reproduced exactly: eRASS1 MID 1.40,
ACCEPT 0.92, eFEDS 29.4).

| | eRASS1 (MID; terciles) | ACCEPT | eFEDS |
|---|---|---|---|
| H-EX (pooled), canonical | 1.40 ± 0.09 (Z +4.6); terciles 1.02 / 1.65 / 1.45 | **PASS** (0.92) | FAIL (χ² 30) |

**Verdict: FAIL** (1 of 3).
- The frozen text said "free = cold energy of expelled baryons", but the pooled implementation does not realise that.
  CFG809 implements the stated split.
- The score first crashed on a stale key ('P' instead of 'EX') in a MUTATE print line. It was fixed and re-scored from the
  stored work files; the numbers are unchanged.
- Census catchments (f_ret(M_ta)) leave giant clusters unchanged and raise group supply by up to +160%.

κ fitted; not theory closed.
