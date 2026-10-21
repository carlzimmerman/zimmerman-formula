# CFG939 AMENDMENT A2 (POST HOC, 2026-10-20; committed alone, after two main runs, before the runs it declares)

FROZEN_CRITERIA.md (3524438b2) and A1 (7dace0a16) are unedited. No class rule is changed here. This amendment declares one numerical
fix to a failed check and three report-only runs. Results of this lane have NOT been committed yet.

## What happened (disclosed)

**First main run** (spherical step dt = 0.005; outputs kept as `cfg939_firstrun_dt0005.out` / `.json`):
- K 9/10. K5c FAILED: the Newtonian control has |dE/E| = 1.04e-3 against the 1e-3 bar.
- The sudden-loss run at f = 0.7 had |dE/E| = 3.9e-3. This was not then a named check.
- C1 printed TETHERED AFTER CROSSING (m/m_law at 2 / 5 r_M = 0.998 / 0.966), and the S4 class printed NOT DERIVABLE.

**Final main run** (dt = 0.00125 for every spherical run; a K5d bar added for the sudden-loss runs, all ≤ 6e-5):
- K 10/11. K5c FAILED again, |dE/E| = 1.04e-3.
- C1 printed **UNTETHERED**: m/m_law at 5 r_M = 0.949, outside the ±0.05 window by 0.001; at 2 r_M it is 0.999.
- The S4 class printed "UNDETERMINED (UNTETHERED)", because no frozen class's conditions hold: C2(a) = 0.445 < 0.9 rules out
  DERIVED, and C1 ≠ TETHERED rules out NOT DERIVABLE.
- The frozen rules forbid reading any class while a K fails.

**Diagnosis of K5c** (scratch run, not committed). The control's energy error is a random walk driven by about 3e5 elastic reflections
at r_min = 1. At t = 400 it is −3.9e-3 at dt = 0.005 and −3.8e-4 at dt = 0.00125. At t = 2000 the values fluctuate around 1e-3.
The tether runs reflect rarely: they pass their own bars (K5b 1.3e-4, K5d ≤ 6e-5).

## Declared now (before the runs)

1. **K5c fix.** The Newtonian control is integrated at dt = 0.00125/4 = 3.125e-4. Nothing else in the main run changes, and the tether
   run is deterministic at its step, so its C1 numbers are unchanged. The main script is rerun so that every K is evaluated in one run.
2. **C1 is reported as BORDERLINE-SENSITIVE.** The time-averaged m/m_law at 5 r_M sits 3.4–5.1% below the law depending on the
   integration step. That is the chaotic run-to-run scatter of a time average, and it straddles the frozen 0.95 edge. The frozen rule
   is applied unchanged to the primary run (dt = 0.00125). Three **report-only** tether runs follow (no class weight):
   - (a) dt = 0.0025, t_end 2000;
   - (b) dt = 0.000625, t_end 2000;
   - (c) dt = 0.00125, t_end 6000, averaged over [4000, 6000]. This separates a filling transient (CFG747/748: the region beyond
     ~5 r_M fills slowly) from a persistent shortfall.
3. **Reading if the frozen rules assign no class.** The S4 result is then stated as "unassigned by the frozen rules (C1 borderline)",
   next to the analytic test C3 and the C2(a) value. It is not relabelled.

A 5% *deficit* at 5 r_M is the opposite sign to what the frozen label "UNTETHERED" was built to detect: the tether-off control piles
cold mass to 3.9 × the law there. This is stated as physics context only. It does not change the frozen class.

κ = ½ FITTED; footings never pooled; not theory closed.
