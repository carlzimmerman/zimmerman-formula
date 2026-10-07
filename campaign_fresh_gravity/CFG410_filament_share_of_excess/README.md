# CFG410: the residual small-scale excess is FILAMENT-DOMINATED (X = 0.89 / 0.86). The corrected-filter baseline is TENSION

Criteria (frozen, committed first); engine `cfg410_pm.py`; analysis `cfg410_analysis.py` (written to `.out` and JSON).

**BASE: CFG374 re-run with the corrected k_J (RES R_c = 3, MIX-A).**
- σ₈ ×1.019 / ×1.024.
- max|P−1| 0.153 / 0.193, which is **TENSION**.
- That is worse than CFG374's buggy-filter +12 / +16%, as the audit predicted.

**VETO (switch off where l3 < 0).**
- σ₈ ×1.002 / ×1.003.
- max|P−1| 0.017 / 0.027, which is GROWTH OK.
- The veto removes **X = 89% / 86%** of the BASE P(k = 1) excess, so the excess is **FILAMENT-DOMINATED**.
- MUTATE passes: the veto cuts the switch-ON mass by 64%.

**Reading.**
- The residual growth problem lives almost entirely in filament-like (l3 < 0) cells.
- So the growth problem and the switch's known false positives on dense filaments are the **same problem**.
- The plain veto is NOT a viable rule: at host scale it also switches off the generic 3-stream shells, and KiDS then fails (+52; STANDING §switch).
- **The target is now sharp:** a switch that is OFF in filament cores but ON in host shells. The record's theorem says no reader of tidal eigenvalues alone can do this. The switch needs non-eigenvalue information, for example a multi-stream / shell-crossing count or a density-and-velocity-divergence condition.

**Scope.** Bookkeeping reservoir; 256³; MIX-A z ≈ 0 phase fractions at all z. κ = ½ is fitted.
