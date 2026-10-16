# CFG813: fair census test of H-EX on 76 redMaPPer-matched eRASS1 clusters. NO GAIN (bracket-dependent)

M_cond = λ × 10^10.7 M☉ (provisional; brackets ×0.5/×2) replaces the fixed 0.20 M_gas. Median fs is 0.032. The census now
acts: f_ret ranges 0.38–0.90, median 0.90.

| model (same 76 clusters, canonical) | MID | OUTER | halves MID | Σ Z² |
|---|---|---|---|---|
| plain law | 2.05 ± 0.24 | 1.30 | 2.21 / 1.86 | 42.6 |
| CFG809 H-EX, fs = 0.20 (f_ret pinned 0.60) | 0.79 ± 0.10 | 0.78 | 0.94 / 0.65 | 21.9 |
| **fair H-EX, λ masses (census acts)** | **1.64 ± 0.18** (Z +3.5) | 1.18 | 1.77 / 1.50 | 25.7 |
| fair, ×2 bracket | 1.49 | 1.13 | 1.55 / 1.41 | 20.8 |
| fair, alt footing ×2 | 1.41 | 1.07 | 1.46 / 1.34 | 15.6 |

**Class: NO GAIN** (primary). Brackets: ×0.5 NO GAIN, ×2 IMPROVES, so it is BRACKET-DEPENDENT.

**Reading.**
- With the floor removed, the census says massive clusters retain ~90% of their baryons. Little gas is expelled, so little
  cold energy is freed, and the clusters come out **short** (×1.6).
- The accidental 0.60 pin over-freed and **overshot** (0.79).
- So the clusters behave as if ~25–35% of their catchment baryons were expelled, more than the census's 10%, but less than
  the pinned 40%. The rule's shape (expelled gas frees cold energy) is not excluded. The census normalisation at cluster mass
  does not deliver it.
- All variants are short at fixed sign in both halves: there is no cancellation here.

**Disclosed.**
- **K2 FAILED as frozen.** It expected the median f_ret < 0.60 once the floor unbinds. In fact the unbound census gives 0.90
  at cluster masses, higher than the pin. K2's expectation was wrong; the floor is unbound (f_ret now varies, 0.38–0.90).
- K1 PASS (1.6e-16).
- λ → M* is a provisional order of magnitude.
- 76 of 318 clusters only.

κ fitted; cold energy mass required; not theory closed.

## Post-hoc diagnostic: why do clusters act like ~30% expelled? (`diag_catchment_fret.py`, not a verdict)
The effective retention, f_eff = retained (gas < 3 Mpc + stars) / framework catchment (gas < r_ta + stars), depends on
how the gas density falls **beyond R200** (r_ta ≈ 7 Mpc ≈ 8.5 R500, median):

| outskirt density ∝ r^−n beyond R200 | f_eff median (IQR) | implication |
|---|---|---|
| n = 2 (beta model extended) | 0.42 (0.34–0.50) | too much expelled: overshoot |
| n = 2.5 | 0.62 (0.53–0.70) | about the CFG809 pin |
| **n = 3** | **0.76 (0.68–0.82)** | **matches the data-implied ~0.65–0.75** |
| n = 3.5 | 0.85 (0.79–0.89) | near the census |

**Reading.**
- The "30% puzzle" reduces to ONE quantity: the gas density slope between R200 and the turnaround radius, where X-ray data
  end.
- If cluster gas steepens to ∝ r^−3 out there (X-ray outskirt steepening; provisional), then H-EX (expelled gas frees cold
  energy) gives the right free mass.
- **Tension (disclosed):** the record's own extrapolation of measured X-COP profiles with their last-3-point slopes (CFG656,
  rule P) gives catchments ×5.4 the R200 baryons. That implies n ≈ 2–2.5, which would overshoot. The steepening bracket
  (LO) gives ×1.6. Extrapolating a last-3-point slope 5–10× beyond the data is itself unreliable.
- n was read off a scan, so this is a **conditional prediction, not a pass**.

**Prediction (falsifiable).** Under H-EX, stacked cluster gas or pressure profiles (eROSITA outskirts, Planck/ACT SZ
stacks) must show the gas density falling as ≈ r^−3 (n = 3.0 ± 0.25) from R200 out to several R200. A shallow r^−2 to
r^−2.5 continuation to the turnaround radius would rule H-EX out at cluster scale.

**Check against published data (provisional; read from the abstract and summary, not re-analysed).**
- **Measured, consistent:** the 2026 SRG/eROSITA stack of 680 clusters (A&A, arXiv:2509.25317) fits a gas density slope
  running from ≈ −1 in the core to **≈ −3 at r200m**, with signal out to ≈ 2 r200m (~4.5 Mpc). That supports n ≈ 3 at
  R200, as the prediction requires.
- **Not measured:** the slope beyond ~2 r200m, out to the turnaround radius (~4–8 R200). Simulations cited there flatten
  beyond r200m because of filaments, which would lower f_eff toward the overshoot side.
- **The decisive measurement:** the stacked slope between 2 r200m and r_ta.
