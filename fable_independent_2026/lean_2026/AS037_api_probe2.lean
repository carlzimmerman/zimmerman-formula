import Mathlib
noncomputable section
open Real Filter

-- probe 1: does `simpa using hlin.pow 2` close a pointwise-fn target?
example (u : ℝ) : HasDerivAt (fun v : ℝ => (1 + v) ^ (2:ℕ)) (2 * (1 + u)) u := by
  have hlin : HasDerivAt (fun v : ℝ => 1 + v) 1 u := (hasDerivAt_id u).const_add 1
  simpa using hlin.pow 2

-- probe 2: eventually-of-forall names
#check Filter.eventually_of_forall
#check Filter.Eventually.of_forall
#check eventually_of_forall
#check Filter.Eventually
#check Filter.EventuallyEq

example (u : ℝ) : (fun v : ℝ => 1 - (((1 + v) ^ (2:ℕ))⁻¹)) =ᶠ[nhds u]
    (fun v : ℝ => 1 + -(((1 + v) ^ (2:ℕ))⁻¹)) := by
  exact Filter.eventually_of_forall (by intro v; rw [sub_eq_add_neg])

-- probe 3: congr_of_eventuallyEq transfer
example (u : ℝ) :
    HasDerivAt (fun v : ℝ => 1 - (((1 + v) ^ (2:ℕ))⁻¹)) (2 / ((1 + u) ^ (3:ℕ))) u := by
  have hc : HasDerivAt (fun v : ℝ => 1 + -(((1 + v) ^ (2:ℕ))⁻¹)) (2 / ((1 + u) ^ (3:ℕ))) u := by
    -- fake: not provable; just check the transfer type works on a constructed dummy via congr
    sorry
  have hfneq : (fun v : ℝ => 1 - (((1 + v) ^ (2:ℕ))⁻¹)) =ᶠ[nhds u]
      (fun v : ℝ => 1 + -(((1 + v) ^ (2:ℕ))⁻¹)) := by
    exact Filter.eventually_of_forall (by intro v; rw [sub_eq_add_neg])
  exact hc.congr_of_eventuallyEq hfneq

-- probe 4: AS026's exact hd pattern (should compile)
example (x : ℝ) : HasDerivAt (fun z : ℝ => 1 + 4 * z ^ 2) (4 * (2 * x)) x := by
  simpa using (((hasDerivAt_id x).pow (2 : ℕ)).const_mul (4 : ℝ)).const_add (1 : ℝ)

-- probe 5: nlinarith on x*(2*x)
example {x : ℝ} (hx : 0 < x) (hs : Real.sqrt (1 + 4 * x ^ 2) < 1 + 2 * x ^ 2) :
    Real.sqrt (1 + 4 * x ^ 2) - 1 < x * (2 * x) := by
  nlinarith [hs]

end
