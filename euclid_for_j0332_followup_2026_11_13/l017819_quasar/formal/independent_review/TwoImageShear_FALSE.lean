import Mathlib.Tactic

/-! Algebra used by the two-quasar-image host reconstruction.
For two distinct image positions, an unrestricted trace-free shear can absorb
any supplied difference in deflection. This is an identifiability statement,
not a theorem about the physical environment or the validity of a gravity law.
All coordinates and deflections use the same two-dimensional convention.
-/

namespace TwoImageShear

noncomputable def shear1 (dx dy vx vy : ℝ) : ℝ :=
  (dx * vx - dy * vy) / (dx ^ 2 + dy ^ 2)

noncomputable def shear2 (dx dy vx vy : ℝ) : ℝ :=
  (dy * vx + dx * vy) / (dx ^ 2 + dy ^ 2)

theorem inverse_components (dx dy vx vy : ℝ) (hd : dx ^ 2 + dy ^ 2 ≠ 0) :
    shear1 dx dy vx vy * dx + shear2 dx dy vx vy * dy = vx ∧
    shear2 dx dy vx vy * dx - shear1 dx dy vx vy * dy = vy := by
  constructor <;> unfold shear1 shear2 <;> field_simp <;> ring

theorem shear_norm_identity (dx dy vx vy : ℝ) (hd : dx ^ 2 + dy ^ 2 ≠ 0) :
    (shear1 dx dy vx vy) ^ 2 + (shear2 dx dy vx vy) ^ 2 =
      2 * (vx ^ 2 + vy ^ 2) / (dx ^ 2 + dy ^ 2) := by
  unfold shear1 shear2
  field_simp
  ring

theorem unique_shear (dx dy vx vy g1 g2 : ℝ) (hd : dx ^ 2 + dy ^ 2 ≠ 0)
    (hx : g1 * dx + g2 * dy = vx) (hy : g2 * dx - g1 * dy = vy) :
    g1 = shear1 dx dy vx vy ∧ g2 = shear2 dx dy vx vy := by
  constructor
  · unfold shear1
    apply (eq_div_iff hd).2
    calc
      g1 * (dx ^ 2 + dy ^ 2) = dx * (g1 * dx + g2 * dy) - dy * (g2 * dx - g1 * dy) := by ring
      _ = dx * vx - dy * vy := by rw [hx, hy]
  · unfold shear2
    apply (eq_div_iff hd).2
    calc
      g2 * (dx ^ 2 + dy ^ 2) = dy * (g1 * dx + g2 * dy) + dx * (g2 * dx - g1 * dy) := by ring
      _ = dy * vx + dx * vy := by rw [hx, hy]

/-- Even with a fixed convergence, arbitrary deflections at two distinct
positions can be mapped to one common source using a unique trace-free shear.
Here `t = 1 - kappa`; deflections already include distance geometry. -/
theorem any_two_deflections_have_common_source
    (xa ya xb yb axa aya axb ayb cx cy t : ℝ)
    (hd : (xa - xb) ^ 2 + (ya - yb) ^ 2 ≠ 0) :
    ∃ g1 g2 : ℝ,
      t * xa - axa - g1 * (xa - cx) - g2 * (ya - cy) =
        t * xb - axb - g1 * (xb - cx) - g2 * (yb - cy) ∧
      t * ya - aya - g2 * (xa - cx) + g1 * (ya - cy) =
        t * yb - ayb - g2 * (xb - cx) + g1 * (yb - cy) := by
  let vx := t * (xa - xb) - (axa - axb)
  let vy := t * (ya - yb) - (aya - ayb)
  let g1 := shear1 (xa - xb) (ya - yb) vx vy
  let g2 := shear2 (xa - xb) (ya - yb) vx vy
  have h := inverse_components (xa - xb) (ya - yb) vx vy hd
  change g1 * (xa - xb) + g2 * (ya - yb) = vx ∧
    g2 * (xa - xb) - g1 * (ya - yb) = vy at h
  refine ⟨g1, g2, ?_, ?_⟩ <;> dsimp [vx, vy] at h <;> nlinarith [h.1, h.2]

theorem distinct_pair_denominator (dx dy : ℝ) (h : dx ≠ 0 ∨ dy ≠ 0) :
    dx ^ 2 + dy ^ 2 ≠ 0 := by
  intro hz
  rcases h with hx | hy
  · have := sq_pos_of_ne_zero hx
    nlinarith [sq_nonneg dy]
  · have := sq_pos_of_ne_zero hy
    nlinarith [sq_nonneg dx]

end TwoImageShear

#print axioms TwoImageShear.any_two_deflections_have_common_source
#print axioms TwoImageShear.shear_norm_identity
