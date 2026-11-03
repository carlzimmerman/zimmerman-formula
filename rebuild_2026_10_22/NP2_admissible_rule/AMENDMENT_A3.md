# NP2 Amendment A3, 2026-11-03, after a second aborted controls run, BEFORE any real-data fit

**Disclosure.** The second `controls` run (FROZEN_CRITERIA + A1 + A2) was stopped after the base controls and before any cell control finished. Read from it: control 1 known answer +0.4675 / −0.0252 OK; control 8 Υ loader OK; control 3 checker OK (bump flagged, zero rule clean, NP1's rule flagged with 30/50 dwarf rows); control 2 zero-weight card: 74 rows compared, 0 mismatches, 22 skipped by design (A15-A17, B1: NaN inputs; B4-B20: `--no-keys`; B28: `--no-bullet`, which RQ3 reports as "not run" or "keys path", now matched as A2 intended). Base controls ALL OK. No real-data fit, gate, card or label has been computed.

It was stopped for two reasons, both machinery.

1. **Memory metering.** `ru_maxrss` and `ps rss` on macOS count freed pages the allocator has handed back with MADV_FREE until the OS reclaims them. A test loop of 6 MB temporaries showed RSS 0.33 GB against a physical footprint of 22 MB (peak 39 MB). The 1 GB cap is now metered by `footprint`'s phys_footprint_peak, printed with every progress line and at the end, beside max RSS. NP1's 0.52 GB was max RSS, so the two lanes' figures are not like for like.
2. **Active-set cycling.** Shedding slack functionals after every solve (A1 item 2) made the active set cycle on the inadmissible planted data: 47-80 rounds per fit, often not converging, ~1 h per cell fit. Changes:
   - the working set only grows (no shedding), 300 functionals added per round, cap 4000 for the final fit (A2) and **2000 for CV fits**; hitting the cap with violations left = not converged;
   - **a λ is eligible in CV only if all four fold fits converge**; ineligible λ get infinite loss. If no λ is eligible, λ = 32 (the grid top) is used for the final fit and `none_eligible` is reported; the final fit's own convergence still decides the INADMISSIBLE label.
   On the noisy planted form at λ 4 this converged in 7 rounds (17 s); at λ ¼ it did not converge (the wiggly fit wants to be inadmissible everywhere), which now makes λ ¼ ineligible instead of costing the run.

Constraint, pool, checker, λ grid, mode U, gates, labels and controls are unchanged.

κ = ½ FITTED; not theory closed.
