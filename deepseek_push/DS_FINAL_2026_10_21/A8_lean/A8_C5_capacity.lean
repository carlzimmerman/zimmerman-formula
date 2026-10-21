/-
A8 / C5 — the capacity statement for the canonical law.

Physics claim being certified (BRIEF section 1): with `x = g/a0` and `g` the
canonical-law total acceleration,

      mu := gN/g = g/(g + a0) = x/(1 + x),

so the "mass discrepancy" `mu` (baryonic fraction of the total acceleration)
is strictly between 0 and 1, tends to 1 in the deep limit `x -> infinity`
(everything is accounted for by the boost) and tends to 0 in the Newtonian
limit `x -> 0` (nothing is boosted).  This is the algebraic core of the
"capacity" language: `mu` saturates at 1 and is empty at 0.

Certified here:

* `mu_eq_of_canonical`: for any `g > 0` obeying `g^2 = gN (g + a0)`,
  `gN/g = mu (g/a0)`.  (Uses the defining equation, not the closed form.)
* `boost_eq_one_add`:  `g/gN = 1 + a0/g`, i.e. the boost factor is exactly
  one plus `a0/g`.
* `mu_pos`, `mu_lt_one`: `0 < mu x < 1` for every `x > 0`.
* `mu_tendsto_zero`:  `mu -> 0` at `x -> 0`  (`Filter.Tendsto` at `nhds 0`).
* `mu_tendsto_one`:   `mu -> 1` at `x -> atTop`.

NOT certified: that `mu` is realised by any galaxy; that the "capacity" is an
integral of `1 - mu` (that would be a further computation about the
interpolation, not proved here); any statement about the n = 2 law's capacity
being `a0/2` rather than `a0`.
-/
import Mathlib

namespace A8

open Filter Topology

/-- `mu(x) = x/(1+x)`, the baryonic fraction of the total acceleration. -/
noncomputable def mu (x : ℝ) : ℝ := x / (1 + x)

/-- **C5, the bridge.**  On the canonical law `g^2 = gN (g + a0)`,
`gN/g = mu(g/a0)`.  Derivation: `gN = g^2/(g+a0)` hence `gN/g = g/(g+a0)`,
and `g/(g+a0) = (g/a0)/(1 + g/a0)`. -/
theorem mu_eq_of_canonical {g gN a0 : ℝ} (hg : 0 < g) (hgN : 0 < gN) (ha0 : 0 < a0)
    (h : g ^ 2 = gN * (g + a0)) : gN / g = mu (g / a0) := by
  have hga : g + a0 ≠ 0 := by positivity
  have h1 : gN = g ^ 2 / (g + a0) := by
    rw [h]
    field_simp
  have h2 : gN / g = g / (g + a0) := by
    rw [h1]
    field_simp
  have h3 : g / (g + a0) = mu (g / a0) := by
    unfold mu
    field_simp
    ring
  rw [h2, h3]

/-- **C5, the boost.**  On the canonical law, `g/gN = 1 + a0/g`. -/
theorem boost_eq_one_add {g gN a0 : ℝ} (hg : 0 < g) (hgN : 0 < gN) (ha0 : 0 < a0)
    (h : g ^ 2 = gN * (g + a0)) : g / gN = 1 + a0 / g := by
  have hga : g + a0 ≠ 0 := by positivity
  have h1 : gN = g ^ 2 / (g + a0) := by
    rw [h]
    field_simp
  rw [h1]
  field_simp

/-- **C5, positivity of the capacity.** -/
theorem mu_pos {x : ℝ} (hx : 0 < x) : 0 < mu x := by
  unfold mu
  exact div_pos hx (by linarith)

/-- **C5, saturation below 1.** -/
theorem mu_lt_one {x : ℝ} (hx : 0 < x) : mu x < 1 := by
  unfold mu
  rw [div_lt_one (by linarith : (0 : ℝ) < 1 + x)]
  linarith

/-- **C5, `mu -> 0` as `x -> 0`.** -/
theorem mu_tendsto_zero : Tendsto mu (nhds 0) (nhds 0) := by
  have hc : ContinuousAt mu 0 := by
    unfold mu
    exact ContinuousAt.div continuousAt_id
      (continuousAt_const.add continuousAt_id) (by norm_num)
  simpa [mu] using hc.tendsto

/-- **C5, `mu -> 1` as `x -> atTop`.**  `x/(1+x) = 1 - 1/(1+x)` and the second
term tends to 0 because `1 + x -> atTop`. -/
theorem mu_tendsto_one : Tendsto mu atTop (nhds 1) := by
  have hinv : Tendsto (fun x : ℝ => (1 + x)⁻¹) atTop (nhds 0) := by
    have hx : Tendsto (fun x : ℝ => (1 : ℝ) + x) atTop atTop :=
      Filter.tendsto_atTop_add_const_left atTop 1 tendsto_id
    simpa [Function.comp_def] using tendsto_inv_atTop_zero.comp hx
  have h2 : Tendsto (fun x : ℝ => 1 - (1 + x)⁻¹) atTop (nhds (1 - 0)) :=
    tendsto_const_nhds.sub hinv
  have heq : mu =ᶠ[atTop] (fun x : ℝ => 1 - (1 + x)⁻¹) := by
    filter_upwards [eventually_gt_atTop (-1 : ℝ)] with x hx
    unfold mu
    have h1x : (1 + x) ≠ 0 := by linarith
    field_simp
    ring
  have := h2.congr' heq.symm
  simpa using this

end A8

#print axioms A8.mu_eq_of_canonical
#print axioms A8.boost_eq_one_add
#print axioms A8.mu_pos
#print axioms A8.mu_lt_one
#print axioms A8.mu_tendsto_zero
#print axioms A8.mu_tendsto_one
