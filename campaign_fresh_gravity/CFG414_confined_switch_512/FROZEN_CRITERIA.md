# CFG414 FROZEN CRITERIA: the confirming PM run for CFG413's open door, with the switch confined to x·r_ta around resolved peaks, at 512³
(owner 2026-10-07: "run it now"; committed before any script)

**Engine.** CFG411's engine: corrected comoving k_J (audit 5819dd616), RES rule with R_c = 3 Mpc/h, MIX-A filter, A0-FLAT, seed 359, NSEED = 512, 150 KDK steps. The only change is that the T1 switch is multiplied by IN(x).

**IN(x).** The union of balls of radius x·r_ON around resolved density peaks. Declared implementation (an efficient version of CFG412/413's B1 cover):
- **Peaks:** 3×3×3 local maxima of the CIC δ with δ ≥ 3(τ − ε), where τ = (Δ_ta(a) − 1)/3 and ε = 0.077, as in CFG413.
- **r_ON** is the largest radius R_j on a 14-point log grid, from 1 cell to 8 Mpc/h, such that the top-hat mean density Δ̄(peak, R) ≥ Δ_ta(a) for every R_i ≤ R_j (first crossing). Δ̄ comes from FFT top-hat convolutions.
- **Resolved:** r_ON ≥ 1.56 Mpc/h, CFG413's frozen 2 cells at 256³.
- **Balls:** FFT convolution of the peak points in each r_ON bin with a ball of radius x·R_j, thresholded at 0.5.
- IN is recomputed every 10 steps from the current δ. Between updates the last mask is used.

**Runs.** x = 0.4 (primary, CFG413), 512³ canonical, then alt, one at a time with 8 threads. The S0 512³ canonical baseline is CFG411's (read-only); an alt S0 at 512³ is run only if time allows.

**Decision.** CFG361's cuts, per footing: GROWTH OK = |σ₈ ratio − 1| ≤ 5% AND max|P−1| ≤ 10% for k ≤ 1; TENSION; FAIL.
- The control is CFG411b's 512³ BASE (no mask; TENSION, P max +17.4%).
- Lane verdict: **CONFIRMED** if x = 0.4 canonical is GROWTH OK, and alt too once it has run. **NOT CONFIRMED** otherwise.

**Controls (field level, 64³, before any 512³ run).**
- C1: IN with x → ∞ covers every cell, so the switched source equals BASE exactly.
- C2: a single analytic top-hat overdensity gives r_ON within one grid step of its analytic Δ_ta radius.

**MUTATE.** x = 0.01. IN then covers only the peak cells themselves, and the field-level switch-ON mass must drop by more than 90%.

**Caveats (from CFG413).**
- x is a new declared constant, and the peak-anchored cover's legality is CONDITIONAL.
- The KiDS side rests on a free two-halo amplitude with no prior.
- κ = ½ is fitted, the cold fluid is still required, and the reservoir is bookkeeping.
