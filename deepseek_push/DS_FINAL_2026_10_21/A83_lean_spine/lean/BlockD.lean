/-
Copyright (c) 2026 Carl Zimmerman. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: A83 lane
-/

import Mathlib

/-!
# A83 Block D — A78 with matter: β = (2/3)Ω_L(r_Λ − 1), β > 0 ⟺ r_Λ > 1, and the BBN window on r_Λ.

Part of the A83 algebraic-spine formalization; see `A83_Spine.lean` for the sources and
the statement of what is and is not formalized.  No `axiom` declarations, no proof
holes, no kernel-bypassing evaluation.
-/

open Filter Matrix
open scoped Topology

noncomputable section

namespace A83

/-! ## Block D — β with matter, the BBN window, and the `Λ_bare` bound (A78) -/

/-- **A78 §3, matter included:** `2 + 3β = 2(Ω_L r_Λ + Ω_m)` with `Ω_L + Ω_m = 1`
gives `β = (2/3)Ω_L(r_Λ − 1)` — **not** A33's vacuum-only `3β = 2Ω_L r_Λ − 2`. -/
theorem beta_of_r (β ΩL Ωm r : ℝ)
    (hrel : 2 + 3 * β = 2 * (ΩL * r + Ωm)) (hsum : ΩL + Ωm = 1) :
    β = (2 / 3) * ΩL * (r - 1) := by
  linarith

/-- `β > 0` iff `r_Λ > 1` (the matter-inclusive sign; not `r_Λ > 1/Ω_L`). -/
theorem beta_pos_iff_r_gt_one (β ΩL r : ℝ) (hβ : β = (2 / 3) * ΩL * (r - 1)) (hΩ : 0 < ΩL) :
    0 < β ↔ 1 < r := by
  rw [hβ]
  constructor
  · intro h; nlinarith
  · intro h; nlinarith

/-- `β > 0` implies `r_Λ > 1`. -/
theorem beta_pos_imp_r_gt_one (β ΩL r : ℝ) (hβ : β = (2 / 3) * ΩL * (r - 1))
    (hΩ : 0 < ΩL) (hpos : 0 < β) : 1 < r :=
  (beta_pos_iff_r_gt_one β ΩL r hβ hΩ).mp hpos

/-- **The BBN bound, non-strict form:** `|ΔN_eff| ≤ ε`, `ΔN_eff = −Cβ`, `C > 0`
gives `r_Λ ≤ 1 + 3ε/(2Ω_L C)`. -/
theorem r_le_bound (β ΩL r Δ ε C : ℝ) (hΩ : 0 < ΩL) (hC : 0 < C)
    (hβ : β = (2 / 3) * ΩL * (r - 1)) (hΔ : Δ = -C * β) (habs : |Δ| ≤ ε) :
    r ≤ 1 + 3 * ε / (2 * ΩL * C) := by
  have hCb : C * β ≤ ε := by
    rw [hΔ] at habs
    have h1 := (abs_le.mp habs).1
    linarith
  have hb_le : β ≤ ε / C := by
    rw [le_div_iff₀ hC]
    linarith
  rw [hβ] at hb_le
  have hstep : r - 1 ≤ ε / C / ((2 / 3) * ΩL) := by
    rw [le_div_iff₀ (by positivity : (0 : ℝ) < (2 / 3) * ΩL)]
    nlinarith [hb_le]
  have heq : ε / C / ((2 / 3) * ΩL) = 3 * ε / (2 * ΩL * C) := by
    field_simp
  linarith

/-- **The BBN bound, strict form:** with `|ΔN_eff| < ε` the inequality is strict. -/
theorem r_upper_bound (β ΩL r Δ ε C : ℝ) (hΩ : 0 < ΩL) (hC : 0 < C)
    (hβ : β = (2 / 3) * ΩL * (r - 1)) (hΔ : Δ = -C * β) (habs : |Δ| < ε) :
    r < 1 + 3 * ε / (2 * ΩL * C) := by
  have hCb : C * β < ε := by
    rw [hΔ] at habs
    have h1 := (abs_lt.mp habs).1
    linarith
  have hb_lt : β < ε / C := by
    rw [lt_div_iff₀ hC]
    linarith
  rw [hβ] at hb_lt
  have hstep : r - 1 < ε / C / ((2 / 3) * ΩL) := by
    rw [lt_div_iff₀ (by positivity : (0 : ℝ) < (2 / 3) * ΩL)]
    nlinarith [hb_lt]
  have heq : ε / C / ((2 / 3) * ΩL) = 3 * ε / (2 * ΩL * C) := by
    field_simp
  linarith

/-- The full window: `β > 0` and `|ΔN_eff| < ε` give `r_Λ ∈ (1, 1 + 3ε/(2Ω_L C))`. -/
theorem r_window (β ΩL r Δ ε C : ℝ) (hΩ : 0 < ΩL) (hC : 0 < C) (hpos : 0 < β)
    (hβ : β = (2 / 3) * ΩL * (r - 1)) (hΔ : Δ = -C * β) (habs : |Δ| < ε) :
    r ∈ Set.Ioo 1 (1 + 3 * ε / (2 * ΩL * C)) :=
  ⟨beta_pos_imp_r_gt_one β ΩL r hβ hΩ hpos,
   r_upper_bound β ΩL r Δ ε C hΩ hC hβ hΔ habs⟩

/-- **Nothing wider:** at `β = ε/C` the bound is attained exactly.  Hence the
non-strict bound `r_Λ ≤ 1 + 3ε/(2Ω_L C)` cannot be improved, and the open interval of
`r_window` genuinely requires the strict hypothesis `|ΔN_eff| < ε`. -/
theorem bound_sharp (β ΩL r ε C : ℝ) (hΩ : 0 < ΩL) (hC : 0 < C) (hβ : β = ε / C)
    (hrel : β = (2 / 3) * ΩL * (r - 1)) : r = 1 + 3 * ε / (2 * ΩL * C) := by
  rw [hβ] at hrel
  field_simp at hrel ⊢
  linarith

end A83
