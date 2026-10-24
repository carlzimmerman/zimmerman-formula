# X18_beta_growth_forest: does saturation rescue C1's small-scale growth, or does the forest close C1's window?

Criteria: `FROZEN_CRITERIA.md` + `ASSUMPTION_LEDGER.md` (71e86472ea, committed alone before any script or number).
Amendments A1–A4 are listed below. κ = ½ FITTED. Footings 9.3603e-11 / 1.1312e-10 m/s², never pooled. No dark-matter
particle. β is never fitted. Not "theory closed". Nothing here says the data favour the framework. Every number below is
from `x18_beta_growth_forest.out` / `_results.json`.

## Verdict: UNDECIDED (frozen rules, both footings)

The frozen rules give UNDECIDED for two independent reasons.

1. **CAP in every cell (80 of 80 run brackets, both footings, every β, every bracket).** The quasi-linear model is
   invalid at early times.
   - The khronon's own linear charge perturbation on forest scales has a Newtonian-from-charge acceleration
     y = Kρ̄_τΔ_τk_p/(k_p² + μ_K²)/a₀ ≥ 1. That is at or above X14's hold-flux cap |KP| < a₀.
   - At fixed comoving k in the matter era y ∝ a⁻¹, so this is an early-time effect.
   - The last epoch with y ≥ 1 on some k ≤ 5.1 h/Mpc is z = 197–499 in the S and E⊥ brackets. In the E∥ bracket it is
     z = 8.0–43 (`z_cap_last_forest`).
   - At the forest epoch itself y is below the cap: max y at z = 3 is 0.0044–0.75 (`y_forest_max_at_z3`).
   - The frozen CAP rule (any a ≤ 1/3) makes every cell's F UNDECIDED. So every β is "mixed", and no β is robust FAIL
     or robust PASS.
2. **Q-CONV fails (a required check).** 2 of 52 variant runs change the σ₈ class. Both are the S∥ bracket at
   β_max(0.03) under a_i = 1e-4:
   - canonical R 1.51 → 0.87;
   - alt R 1.45 → 1.02.

   No variant changes a gate class F.

**Reported only (no verdict weight): the forest gate ignoring CAP (`F_raw`) is FAIL in all 80 brackets.**
- In no bracket do the L346 bins at z = 3 and z = 2 lie inside [0.5, 2]. None lies inside even at z = 3 alone.
- The failure is one of shape. Every cell spans both sides of the band: forest-scale power is suppressed at the low-k
  bins and overshoots at the high-k end. For example, canonical μ_K 0.1, β_min, S⊥: z = 3 bins 0.0035–0.47,
  T²(k5) = 23.8 / 51.4 at z = 3 / 2.
- The result holds under both cap clips (A2: 0.9 and 0.995; 16/16 F_raw FAIL) and both solvers (A3; F_raw identical).
- So the saturated quasi-linear model gives no β in the window where the forest is within the record's lines. It also
  gives none where σ₈ and the forest are both within lines (`sigma8_and_forest_both_within_lines`: no cell).
- That is the direction of CLOSED BY THE FOREST. But it is reached outside the model's own validity (the CAP), so the
  frozen verdict is UNDECIDED, not CLOSED.

## Step 0 (stop rule; all pass)

| check | result |
|---|---|
| S0-1 | X17's own script, run as a patched temp-dir copy: exit 0, 13/13 PASS, verdict "WRONG SIGN", 0 of 13455 JSON leaves differ (timing fields excepted). Its child copy of X15 also ran. |
| S0-2 | The verbatim copy of X17's C1 ODE reproduces X17's 8 growth cells (R_β; T² at z = 0 and z = 3 for k = 0.1–10) with max relative difference 0. For example, canonical μ 0.1 β_min gives R 0.18704 and T²(k = 3, z = 3) 8.757. |
| S0-3 | X4's β = 0 row: 0.075742 / 0.041440 (μ 0.03) and 0.081714 / 0.044705 (μ 0.1), equal to X4. X17's β = 0 cells: max relative difference 0. |
| S0-4 | L346 bins 1.101–3.557 h/Mpc. sw5_canon z = 3 gives 1.0644–1.2168 and sw5_alt 1.0728–1.2463, so the gate FAILs as in L346 and X4; never_on is exactly 1. L319's line T²_5.3keV(k5 = 4.6199) = 0.99519 = X4 F0b. |

## Steps 1–2: the saturation model, derived from the action

- **Q-KER (PASS).** X14's `disp` with C1 at general M_θ gives ω² = −(Kρ̄_τ + Bk²)·s_M, with
  s_M = (Mμ² − (M − 1)k²)/(k² + Mμ²).
  - This is the record's M1 kernel at f₀ = 1 − 1/M; at M = 1 it is X4's J_x kernel.
  - The pressure-support onset is s_M = 0 at x = μ²/(k² − μ²) (⊥). This is X17's "x > s(k)".
- **Q-DISP (PASS).** The baryon + khronon determinant at M_L = M_T = M equals K²M²k² × (λ² − Tλ + D) with
  T = Kρ_b + (Kρ_τ + Bk²)s_M and D = −Kρ_b(Kρ_τ + Bk²)(1 − s_M).
  - So the saturated ODE is X17's `growth_C1` with s → s_M.
  - D < 0 for every M ≥ 1, so a growing root always exists.
- **Q-ASY (PASS).** lim_{k→∞} λ₊ = Kρ_bM/(M − 1). There is no Jeans cut-off in the total: a stiff khronon settles into
  the sub-phantom charge and boosts baryon growth. The numeric check at k = 1e9 agrees to 5.0e-8.
  - The khronon's own Jeans wavenumber is k_J = μ√(M/(M − 1)).
- **Q-LIM (PASS).** With x forced to 0 the saturated ODE equals X17's ODE (max relative difference 0).
- **Onset.** In every graded cell s_M ≤ 0 already at the first output (z = 999) for k = 0.1–10 h/Mpc
  (`z_onset_sM_le_0`, `z_onset_x_ge_s`). c_A pressure is on from the start, because the perturbations' accelerations
  exceed the threshold early (y ∝ a⁻¹). x falls with time: at z = 3 for k = 0.1–10 it is ~2e-6–0.8 (`x_rep`), against
  thresholds (aμ_K/k)² ~ 3e-8–3e-2.
  - The smallest graded k with s_M ≤ 0 at z = 3 (`k_J_hMpc`) is 0.15–0.96 h/Mpc. This lane does not establish that
    every larger k stays pressure-supported (the per-k sign is in the JSON trajectories only through these summaries).
- **The saturated rate is below C1's x = 0 rate, but not by enough.** √λ₊/H at z = 3 (saturated vs x = 0):
  - canonical μ 0.1 β_min, S⊥: k = 1: 1.21 vs 1.22; k = 3: 1.95 vs 1.98; k = 10: 2.19 vs 3.55;
  - canonical μ 0.03 β_max(0.03), S⊥: 2.03 vs 3.08, 2.11 vs 5.31, 2.11 vs 9.68.
  - The k^{1/2} rise is cut at k ≳ 3. It is replaced by the Kρ_bM/(M − 1) floor, which at x ~ 1e-3–0.05 is still
    above the dust rate.

## Step 2: forest comparison per cell (grid ends shown; all cells in `cells`)

Ratios are T² = (δ_m/δ_m,dust)² at the six L346 bins; L319's T²(k5) is given as z = 3 / z = 2. Every cell is CAP, so
F = UNDECIDED; F_raw is FAIL in every cell.

| footing, μ_K, β | bracket | R (σ₈/dust) | z = 3 bins | z = 2 bins | T²(k5) |
|---|---|---|---|---|---|
| can, 0.1, 1.99e-6 | S⊥ / S∥ / E⊥ / E∥ | 0.063 / 0.091 / 0.088 / 0.321 | 0.0035–0.47 / 0.00028–1.52 / 0.0074–1.16 / 1.45–323 | 0.0059–0.99 / 0.00017–3.14 / 0.015–2.5 / 0.16–10.6 | 23.8/51.4; 1.53/3.62; 1.15/2.91; 49.6/142 |
| can, 0.1, 1.00e-5 | S⊥ / S∥ / E⊥ / E∥ | 0.498 / 0.241 / 0.351 / 0.334 | 1.02–35.6 / 0.014–21.9 / 0.059–28.1 / 0.018–109 | 1.75–71.8 / 0.026–41.5 / 0.12–63.8 / 0.33–46.3 | 168/303; 44.1/79.3; 54.3/118; 112/78.9 |
| can, 0.03, 1.12e-4 | S⊥ / S∥ / E⊥ / E∥ | 2.05 / 1.51 / 1.51 / 1.31 | 25–154 / 5.0–37 / 12–41 / 1.5–2170 | 44–267 / 8.9–66 / 25–75 / 0.13–1660 | 236/408; 65.5/111; 33.6/58.1; 2090/461 |
| alt, 0.1, 2.20e-6 | S⊥ / S∥ / E⊥ / E∥ | 0.078 / 0.076 / 0.071 / 0.291 | 0.011–8.3 / 0.021–2.5 / 0.023–0.99 / 12.6–1400 | 0.018–17 / 0.029–4.6 / 0.051–2.2 / 0.26–1540 | 41.4/89.8; 12.5/26.7; 0.129/0.329; 118/2380 |
| alt, 0.1, 1.00e-5 | S⊥ / S∥ / E⊥ / E∥ | 0.483 / 0.267 / 0.357 / 0.403 | 0.59–123 / 0.30–24 / 3e-5–31 / 8.2–261 | 1.6–231 / 0.76–47 / 1.8e-4–75 / 7.3–166 | 246/445; 61.5/111; 78.8/175; 5940/6380 |

- **β = 0 (v3s) with saturation (reference).** R = 0.017–0.059. The z = 3 bins are 0.0005–0.025: suppressed, not
  overshooting. Every v3s cell is CAP as well, so the CAP is a property of the khronon-as-linear-dust ODE itself, not
  of C1.
- **1D ratio (reported).** P1D/P1D,dust at the bin k_∥, z = 3, is 30–9.6e5 across the end cells. It is weighted to
  high k, so it is larger than the 3D ratios.
- **FORMAL.** Many cells have Δ_m > 1 in the bins at z = 3 (for example, canonical β_max(0.03) S⊥: max Δ_m 11). The
  linear values are formal there.

## Reported only

- **σ₈/dust at z = 0 after saturation.** It rises with β:
  - μ 0.1: 0.063–0.50 canonical, 0.071–0.48 alt (E∥ 0.29–0.40);
  - μ 0.03: 0.060–2.05 canonical, 0.066–1.81 alt.
- **σ₈ in [0.95, 1.05].** This happens only in a few μ 0.03 cells near β ≈ 3e-5–6e-5 (canonical E⊥ 1.061 is just
  outside; alt S⊥ 1.042 and S∥ 1.023 at 3.0e-5 / 5.8e-5).
- **σ₈ and the forest jointly within lines: no cell.** Even where σ₈ comes near 1, the forest bins in the same cell
  span ≫ [0.5, 2]. Matching σ₈ by choosing β would be fitting a knob; it is not done, and it would not pass the forest.
- **What a Boltzmann / N-body run would need.**
  - C1 is not in Q6's CLASS patch. It would need the K² operator in the khronon perturbation equations, with B and the
    μ_K kernel.
  - It would need the nonlinear Gauss law, with X14's cap, for the khronon's charge.
  - Above all, it would need the early-time regime where the khronon's linear charge perturbations exceed the cap. That
    regime is where a linear dust treatment (X4/X17 and this lane) is invalid. It is L1's kind of question, run with
    C1 and the cap.

## Checks

- **Main run: 8/9 PASS, exit 1.** Passing: S0-1…S0-4, Q-KER, Q-DISP, Q-ASY, Q-LIM. Failing: Q-CONV (above).
  - 5749 s; peak RSS 0.21 GB (children 0.16 GB); one thread, nice 15, PYTHONHASHSEED=0.
- **MUTATE (`X18_MUTATE=1`): exit 1, exact.** The required failures are exactly S0-1 (m1), S0-2 (m2), S0-3 (m3),
  S0-4 (m4), Q-KER (m5), Q-DISP (m6), Q-ASY (m7) and Q-LIM (m8). Q-CONV passes, as designed. 14 s. The MUTATE verdict
  line is the control's output, not physics.

## Amendments and execution history

- **A1 (PRE-RESULT, implementation).**
  - (a) X17's source contains its own HERE/ROOT lines as strings (for patching X15), so only the first, line-start
    assignment is rebound.
  - (b) Q-ASY's numeric point uses exact rationals: in 15-digit floats T + √(T² − 4D) cancels. The first attempt gave
    7.8e-3 from cancellation, while the symbolic limit was 0.
  - (c) The E bracket uses max(own y, cumulative rms): "plus the mode itself" in §1.
  - Runs 1–2 were stopped for (a) and (b). Before the stop, run 2 printed one reported-only line, the canonical μ 0.1
    β = 0 reference.
- **A2 (after that β = 0 line, reported only).** It showed CAP in every bracket. So these were added with no verdict
  weight: F_raw (the gate ignoring CAP), the latest CAP epoch, y at z = 3, and a cap-clip sensitivity (0.9 / 0.995).
- **A3 (implementation, during run 3).** The stiff E∥ bracket took 170–520 s per cell in DOP853, and the coordinator
  flagged the run's length.
  - Saturated runs therefore use LSODA. The x = 0 path (Q-LIM) stays DOP853.
  - LSODA against DOP853 at β_min (S⊥, S∥, E⊥): F_raw identical, bins within 2e-4–0.14 relative.
  - E∥'s numbers are not solver-converged (for example, β_min canonical μ 0.1 R 0.267 in DOP853, 0.321 in LSODA), but
    its class is.
- **A4 (implementation, compute budget).** E∥ runs at the grid ends only. At interior β it is skipped when a cheaper
  bracket is already UNDECIDED; under §6 that β is then "mixed" whatever E∥ gives.
  - Q-CONV runs E∥ only at β_min with a_i = 1e-4.
  - The clip sensitivity uses E⊥ instead of E∥.
  - The β = 0 references skip E∥.
  - No criterion, threshold or verdict rule changed.

## What this does not show

- It is a quasi-linear WKB model, not N-body/Boltzmann. There is no shell crossing, no baryon pressure, and no flux
  power.
- The early-time CAP means the model (and X4/X17's linear ODE before it) is outside its validity at z ≳ 8–500 on forest
  scales.
- Orientation is bracketed (⊥/∥), not averaged.
- The forest lines are LITERATURE-INPUT, ΛCDM-PROCESSED, and are applied to 3D (quasi-)linear power as in X4.

## Suggested fixes elsewhere (not edited here)

- **X17 / X4 / V3_FULL_PICTURE §4.2 and §6 (X17 bullet).** The linear khronon-dust ODE puts the khronon's charge
  perturbations above X14's hold-flux cap (y ≥ 1) at early times on forest scales: last at z ≈ 200–500 at β = 0 (v3s
  itself). Add a validity caveat to the linear growth numbers: the overshoot (X17) and the suppression (X4) are formal
  in that regime.
- **V3_FULL_PICTURE §6, C1 row.** Add: X18 finds saturation switches c_A on from the first output (z = 999) at
  k = 0.1–10 h/Mpc. At z = 3 the smallest pressure-supported k is ≈ 0.15–0.96 h/Mpc. The k^{1/2} rate is cut only at
  k ≳ 3 h/Mpc, so no window β puts forest power within the record's lines (F_raw FAIL in 80/80). The frozen verdict is
  UNDECIDED because the model hits the cap at early times.
- **Next lane.** C1 plus the cap in a nonlinear code (L1-type), started from a cap-consistent early-time state. That
  would decide CLOSED versus UNDECIDED.

## Files and run

| file | contents |
|---|---|
| `x18_beta_growth_forest.py` | Parts S0, Q, C, V. Copied with provenance: X17's ODE, X14's `disp`, X4's gate code |
| `x18_beta_growth_forest.out`, `_results.json` | scored main run |
| `x18_beta_growth_forest_MUTATE.out`, `_results_MUTATE.json` | MUTATE run (m1–m8) |

```
PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 rebuild_2026_10_22/X18_beta_growth_forest/x18_beta_growth_forest.py              # exit 1 (Q-CONV), ~96 min
PYTHONHASHSEED=0 X18_MUTATE=1 OMP_NUM_THREADS=1 nice -n 15 python3 rebuild_2026_10_22/X18_beta_growth_forest/x18_beta_growth_forest.py  # exit 1 by design
```
