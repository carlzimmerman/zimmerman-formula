import Mathlib
namespace LawBand

noncomputable def massMap (a g : ℝ) : ℝ := g^2 / (a+g)

theorem massMap_mono {a x y : ℝ} (ha : 0 < a) (hx : 0 ≤ x) (hxy : x ≤ y) :
    massMap a x ≤ massMap a y := by
  unfold massMap
  have hy : 0 ≤ y := le_trans hx hxy
  rw [div_le_div_iff₀ (by positivity : 0 < a+x) (by positivity : 0 < a+y)]
  have hp : 0 ≤ (y-x) * (a*(x+y)+x*y) := by positivity
  nlinarith

/-- Changing the field by a factor in [0,1] changes the mass by no more
than the square of that factor in the downward direction. -/
theorem scaled_lower {a g l : ℝ} (ha : 0 < a) (hg : 0 < g)
    (hl : 0 ≤ l) (hl1 : l ≤ 1) : l^2 * massMap a g ≤ massMap a (l*g) := by
  unfold massMap
  have hden : a + l*g ≤ a+g := by nlinarith
  have hi := div_le_div_of_nonneg_left (sq_nonneg (l*g))
    (by positivity : 0 < a+l*g) hden
  have heq : l^2 * (g^2 / (a+g)) = (l*g)^2/(a+g) := by ring
  rw [heq]
  exact hi

theorem scaled_upper {a g u : ℝ} (ha : 0 < a) (hg : 0 < g)
    (hu : 1 ≤ u) : massMap a (u*g) ≤ u^2 * massMap a g := by
  unfold massMap
  have hden : a+g ≤ a+u*g := by nlinarith
  have hi := div_le_div_of_nonneg_left (sq_nonneg (u*g))
    (by positivity : 0 < a+g) hden
  have heq : u^2 * (g^2 / (a+g)) = (u*g)^2/(a+g) := by ring
  rw [heq]
  exact hi

/-- EW2 H-inf's delta = 2 eps + eps^2 follows from the simple-mu mass map,
without assuming the mass error band as a new premise. -/
theorem relative_mass_band {a g reference eps : ℝ}
    (ha : 0 < a) (hr : 0 < reference) (he0 : 0 ≤ eps) (he1 : eps < 1)
    (hlo : (1-eps)*reference ≤ g) (hhi : g ≤ (1+eps)*reference) :
    |massMap a g / massMap a reference - 1| ≤ 2*eps+eps^2 := by
  have hg : 0 ≤ g := by nlinarith
  have hm : 0 < massMap a reference := by unfold massMap; positivity
  have hL := le_trans (scaled_lower ha hr (by linarith : 0 ≤ 1-eps) (by linarith))
    (massMap_mono ha (by positivity : 0 ≤ (1-eps)*reference) hlo)
  have hU := le_trans (massMap_mono ha hg hhi)
    (scaled_upper ha hr (by linarith : 1 ≤ 1+eps))
  apply abs_le.mpr
  constructor
  · have hlrat : (1-eps)^2 ≤ massMap a g / massMap a reference := by
      rw [le_div_iff₀ hm]
      exact hL
    nlinarith
  · have hurat : massMap a g / massMap a reference ≤ (1+eps)^2 := by
      rw [div_le_iff₀ hm]
      exact hU
    nlinarith

/-- The simple-mu law's phantom acceleration is nonnegative and strictly
below a0, supplying the source-cap input of the memory comparison. -/
theorem phantom_cap {a g : ℝ} (ha : 0 < a) (hg : 0 ≤ g) :
    0 ≤ g - massMap a g ∧ g - massMap a g < a := by
  have hden : 0 < a+g := by linarith
  have heq : g - massMap a g = a*g/(a+g) := by
    unfold massMap
    field_simp
    ring
  rw [heq]
  constructor
  · positivity
  · rw [div_lt_iff₀ hden]
    nlinarith [sq_pos_of_pos ha]

end LawBand
#print axioms LawBand.massMap_mono
#print axioms LawBand.scaled_lower
#print axioms LawBand.scaled_upper
#print axioms LawBand.relative_mass_band

#print axioms LawBand.phantom_cap
