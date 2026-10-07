# CFG410 FROZEN CRITERIA: where does the residual small-scale growth excess live? A corrected-filter baseline plus a filament veto
(owner 2026-10-06: "swing swing"; committed before any script)

**Why.**
- CFG361's z = 0 diagnostics show that about 65% of the T1-switch-ON mass sits in cells with l3 < 0, the filament-like tidal eigenvalue at the 0.78 Mpc/h mesh.
- The record's best switch (CFG354 T1) fails only on dense filament cores (STANDING §switch).
- If the residual small-scale excess under the reservoir + gas-filter rule lives in l3 < 0 cells, the growth problem and the switch's filament problem are the same problem.

**Engine.** A copy of CFG374's engine with the referee's k_J fix (audit 5819dd616): comoving k_J = √(1.5 Ω_m / a) · 100/c_s. Otherwise unchanged: RES rule, R_c = 3 Mpc/h, MIX-A phase filter (0.28 / 0.54 / 0.18), A0-FLAT, 256³, seed 359, 150 steps. S0 is CFG359's, read-only.

**Runs (4).**
- BASE: corrected MIX-A, both footings. This is also the corrected CFG374.
- VETO: the same, with the switch set to 0 wherever l3 < 0. This is CFG359's T1V filament veto applied to the RES excess.

**Measurements.**
- σ₈ and P(k) ratios to S0 at z = 0, and max|P − 1| for k ≤ 1.
- Share of the BASE small-scale excess removed by the veto: X = 1 − (P_VETO(k = 1) − 1)/(P_BASE(k = 1) − 1), per footing.

**Decision (reported per footing).**
- FILAMENT-DOMINATED: X ≥ 0.6. The residual excess is a filament false-positive problem.
- SHARED: 0.3 ≤ X < 0.6.
- HOST-DOMINATED: X < 0.3.
- Also the CFG361 cuts (GROWTH OK / TENSION / FAIL) for BASE and VETO separately. BASE is the corrected-filter verdict that CFG374 lacked.

**Caveat (known, not re-tested).** The plain veto fails KiDS (+52; STANDING §switch), because at host scale it also removes the 3-stream shells. So a VETO "pass" is a diagnostic, not a viable rule.

**MUTATE.** Not a new run. The veto's switch-ON mass fraction must drop by more than 50% relative to BASE at z = 0, from the diagnostics. A failure means the veto did not act.

**Scope.** As CFG374, but with the corrected k_J. Bookkeeping reservoir; 256³ only, not converged. κ = ½ is fitted. The cold fluid is still required.
