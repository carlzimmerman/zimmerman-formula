# X28_dwarf_floor_form — FROZEN CRITERIA (committed alone, before any script; POST-HOC envelope disclosed in §5)

**Question.** X24 (19d31a99d9) reproduced three of four dwarf classes with a velocity floor σ² = σ_iso² + c₀². That
floor costs one new dimensionful constant, and it overshoots the MW ultra-faints. X25 (63a4001236) showed c₀ is not in the
v3s action. This lane asks two things:
1. Does the dwarf extra key to **acceleration** instead (an acceleration floor g = g_iso + η a₀)? That would replace c₀ by
   the theory's own scale a₀ times a dimensionless η.
2. Does the acceleration floor fix the ultra-faint overshoot?

Standing rules: κ = ½ FITTED. Footings never pooled (a₀ per footing). One constant per form, calibrated on the 13 LG field
dwarfs only. Not "theory closed". Nothing here may say the data favour the framework. No numerology: η is reported, never
matched to a "natural" number in this lane.

## 1. Data and forms (X24's loader, copied)

Inputs: X1 `x1_per_system.csv` per footing. E = `Delta[iso AQUAL L*0]`, s = sdMC. σ_c is binary-corrected (X1's
rule). σ_iso = σ_c 10^(−E/2). r₁₂ = (4/3) rh. The E-W estimator gives g = 3σ²/r₁₂. Each form has one constant, and
E_pred = log₁₀(g_pred / g_iso):

- **F_v (velocity floor; X24 reproduced):** g_pred = g_iso + 3c₀²/r₁₂.
- **F_g (acceleration floor):** g_pred = g_iso + η a₀.

Calibration per footing: minimise Σ_field ((E − E_pred)/s)² (bounded: c₀ 0–20 km/s, η 0–2), with a 68 % profile interval
(Δχ² = 1). Graded out of sample: MW ultra-faint (31), bright M31 (25), M31 others (5) (H), and MW classical (8, reported
class). Per class: median residual, bootstrap sd (10 000, seed 20261024), Z. χ²/N per class and on H.

## 2. Tests

- **T1, form preference on H (verdict-bearing):** Δχ²_H = χ²_H(F_v) − χ²_H(F_g), both out of sample.
- **T2, ultra-faint overshoot:** |Z| of the MW ultra-faint residual under F_g.
- **T3, consistency of the constant (reported):** η fitted in-sample on H vs η from the field. Agreement is overlap of the
  68 % intervals. The same is reported for c₀ (X24: 3.64 vs 4.59 canonical).
- Reported: a one-parameter power law g_floor ∝ r₁₂^(−n), fitted on all graded + field systems (n = 1 is velocity, n = 0
  is acceleration), with its 68 % interval; the SPARC cost of F_g at the median SPARC g_obs; the effect on TDGs, DF2/DF4,
  Crater II and Antlia II.

## 3. Verdict (both footings must agree)

- **ACCELERATION FLOOR** — Δχ²_H ≥ 4 in favour of F_g AND all three H classes |Z| < 2 under F_g.
- **ACCELERATION PREFERRED, PARTIAL** — Δχ²_H ≥ 4 for F_g but some H class |Z| ≥ 2.
- **VELOCITY FLOOR** — Δχ²_H ≤ −4.
- **NOT DISTINGUISHED** — |Δχ²_H| < 4.
- **UNDECIDED** — the footings disagree.

**Parameter reading.** Under ACCELERATION FLOOR the dwarf extra costs one dimensionless η on the theory's own a₀, not an
independent velocity scale. That is still one number, not a derivation. **Cost check (verdict qualifier):** F_g must not
spoil SPARC. The added η a₀ is compared to SPARC's outer accelerations: the reported ΔE at g_obs = 0.1 a₀ and at 1 a₀ must
be below 0.05 dex. If it is not, the label gains [SPARC-COST].

## 4. Checks (all must pass; `--mutate` must fail K0)

- **K0:** X24's c₀ (field) is reproduced, 4.59 / 4.05 km/s to 0.01. X19's H plain medians are reproduced.
- **K1:** F_g at η = 0 and F_v at c₀ = 0 both return the law, χ² identical to 1e-10.
- **K2:** positive control. Synthetic E from F_g at η = 0.1 plus N(0, s) on the field set; the calibration recovers it
  within its interval (±0.05).
- **K3:** peak RSS < 1 GB.
- **MUTATE:** a₀ is swapped between footings inside F_g, and X24's JSON is read with c₀ × 1.1; K0 must fail.

## 5. Disclosure (post-hoc)

Before freezing, I computed an envelope in this session from X24's printed class medians (σ_c, σ_iso) and typical
r₁₂: η ≈ 0.08 (MW ultra-faints), ≈ 0.09 (bright M31), ≈ 0.22 (M31 others, N 5), ≈ 0.13 (MW classical), canonical. The
field dwarfs' η was not computed. The idea came from the X24 overshoot pattern. A pass is a lead; it needs new dwarf
kinematics, and SPARC's lowest-acceleration outskirts, to confirm.
