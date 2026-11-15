/-
XJ1R: Lean statements for the algebra of the blind caustic-junction build (the law's layout unscaled inside the k-th
caustic, graded on the Lyman-alpha forest at flux level, with SPARC rotation-curve containment). They certify the
algebra, not the physics, and no number or label of the lane. XJ1.lean's theorems on the exact junction are not
restated. TEST lane; adopts nothing.

  control_reaches_reference : FZS1's control junction (the law's cold mass times s, s = C_R(R_set) / C_B(R_set)) has
                          the reference's enclosed cold mass at R_set, and differs there from the exact junction by
                          C_B(R_set) - C_R(R_set).
  exact_minus_control_outside : outside R_set the exact junction minus the control (whose outside is the reference) is
                          (1 - t) (C_tot - C_R(r)): it vanishes at the turnaround radius.
  exact_factor_le_one_iff : the outside factor t is at most 1 exactly when the law's enclosed cold mass at R_set is at
                          least the reference's (C_R(R_set) < C_tot).
  cap_monotone          : the cap R_set = min(R_k, r_ta) never exceeds r_ta and keeps R_3 <= R_2 (KS3 gives KP7).
  labels_exclusive      : with SE = 2 sqrt(D N12) + N12, N12 >= 0, HOLDS (D + 2 SE < 4) and FAILS (D - 2 SE > 4)
                          cannot both apply.
  fragile_under_holds   : under HOLDS, a bracket's 12-bin estimate D b / p (p > 0) flags FRAGILE (lies on the other
                          side of 4 from D) exactly when 4 p < D b.
  lane_words_exclusive  : "CAUSTIC k HOLDS" (forest HOLDS and no galaxy beyond) excludes both "FAILS THE FOREST"
                          and "CUTS ROTATION CURVES" (a galaxy beyond).

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
-/
import Mathlib

namespace XJ1R

theorem control_reaches_reference (CB CR : ℝ) (h : CB ≠ 0) :
    CR / CB * CB = CR ∧ CB - CR / CB * CB = CB - CR := by
  constructor
  · field_simp
  · field_simp

theorem exact_minus_control_outside (CBi CRi CR Ctot t : ℝ) (ht : t * (Ctot - CRi) = Ctot - CBi) :
    (CBi + t * (CR - CRi)) - CR = (1 - t) * (Ctot - CR) := by
  linear_combination ht

theorem exact_factor_le_one_iff (CBi CRi Ctot : ℝ) (hlt : CRi < Ctot) :
    (Ctot - CBi) / (Ctot - CRi) ≤ 1 ↔ CRi ≤ CBi := by
  rw [div_le_one (by linarith)]
  constructor <;> intro h <;> linarith

theorem cap_monotone (R3 R2 rta : ℝ) (h : R3 ≤ R2) :
    min R3 rta ≤ min R2 rta ∧ min R2 rta ≤ rta :=
  ⟨min_le_min_right rta h, min_le_right _ _⟩

theorem labels_exclusive (D N12 : ℝ) (hN : 0 ≤ N12) :
    ¬ (D + 2 * (2 * Real.sqrt (D * N12) + N12) < 4 ∧ D - 2 * (2 * Real.sqrt (D * N12) + N12) > 4) := by
  rintro ⟨h1, h2⟩
  have := Real.sqrt_nonneg (D * N12)
  linarith

theorem fragile_under_holds (D N12 b p : ℝ) (hN : 0 ≤ N12) (hp : 0 < p)
    (hH : D + 2 * (2 * Real.sqrt (D * N12) + N12) < 4) :
    ((4 < D * b / p) ↔ ¬ (4 < D)) ↔ 4 * p < D * b := by
  have hD : ¬ (4 < D) := by
    have := Real.sqrt_nonneg (D * N12)
    intro h
    linarith
  rw [lt_div_iff₀ hp]
  tauto

theorem lane_words_exclusive (D N12 : ℝ) (n : ℕ) (hN : 0 ≤ N12) :
    ¬ ((D + 2 * (2 * Real.sqrt (D * N12) + N12) < 4 ∧ n = 0) ∧ D - 2 * (2 * Real.sqrt (D * N12) + N12) > 4) ∧
    ¬ ((D + 2 * (2 * Real.sqrt (D * N12) + N12) < 4 ∧ n = 0) ∧ 0 < n) := by
  constructor
  · rintro ⟨⟨h1, _⟩, h2⟩
    have := Real.sqrt_nonneg (D * N12)
    linarith
  · rintro ⟨⟨_, h0⟩, hpos⟩
    omega

end XJ1R

-- kappa = 1/2 FITTED; not theory closed. Adopts nothing.
