import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Analysis.SpecialFunctions.Sqrt
import Mathlib.Analysis.SpecialFunctions.Log.Deriv
import Mathlib.Tactic

/-!
# MK1 MUTATE twin: false versions of MK1.lean's claims. Every theorem here must FAIL to compile.

1. `w_increasing_mu_FALSE`: w increases with μ (it decreases).
2. `fb1_arith_FALSE`: FB1's constant is ten times larger.
3. `cap_radius_increasing_FALSE`: dust pushes the cap radius out (it pulls it in).
4. `window_exists_FALSE`: a μ satisfies a lower bound 25118 and an upper bound 7.
5. `deep_dust_wrong_FALSE`: the enclosed dust's derivative without the r²/3 terms cancelling (drops the s r³/9 term).
6. `saturn_decreasing_FALSE`: the Saturn anomaly falls with μ.
7. `cap_law_relation_FALSE`: the law's cap relation with (1 + X) in place of (1 + X)².

κ = ½ FITTED; not theory closed. Adopts nothing.
-/

open Real

namespace MK1M

noncomputable def w0 (I0 μ : ℝ) : ℝ := I0 / (4 * μ ^ 2)
noncomputable def w (I0 μ a : ℝ) : ℝ := w0 I0 μ / (w0 I0 μ + a ^ 3)

theorem w_increasing_mu_FALSE (I0 a : ℝ) (hI : 0 < I0) (ha : 0 < a) {μ1 μ2 : ℝ} (h1 : 0 < μ1) (h12 : μ1 < μ2) :
    w I0 μ1 a < w I0 μ2 a := by
  unfold w w0
  rw [div_lt_div_iff₀ (by positivity) (by positivity)]
  nlinarith

theorem fb1_arith_FALSE :
    (10630 / 100000000000 : ℝ) < 3 * (70 / 299792.458) ^ 2 * 0.26 / 4 := by
  norm_num

noncomputable def xcap (X κ : ℝ) : ℝ := (1 + X) / Real.sqrt (1 + κ)

theorem cap_radius_increasing_FALSE {X κ1 κ2 : ℝ} (hX : 0 < X) (h1 : 0 ≤ κ1) (h12 : κ1 < κ2) :
    xcap X κ1 < xcap X κ2 := by
  unfold xcap
  have hs1 : 0 < Real.sqrt (1 + κ1) := Real.sqrt_pos.mpr (by linarith)
  have hs : Real.sqrt (1 + κ1) < Real.sqrt (1 + κ2) := Real.sqrt_lt_sqrt (by linarith) (by linarith)
  exact div_lt_div_of_pos_left (by linarith) hs1 hs

theorem window_exists_FALSE : ∃ μ : ℝ, (25118 : ℝ) ≤ μ ∧ μ ≤ 7 := by
  refine ⟨25118, le_refl _, ?_⟩
  norm_num

noncomputable def Fw (Pc s rc r : ℝ) : ℝ := Pc * r ^ 3 / 3 + s * (r ^ 3 / 3 * (Real.log rc - Real.log r))

theorem deep_dust_wrong_FALSE (Pc s rc r : ℝ) (hr : 0 < r) :
    HasDerivAt (Fw Pc s rc) (r ^ 2 * (Pc + s * (Real.log rc - Real.log r))) r := by
  have hl : HasDerivAt Real.log r⁻¹ r := Real.hasDerivAt_log (ne_of_gt hr)
  have h3 : HasDerivAt (fun x : ℝ => x ^ 3) (3 * r ^ 2) r := by simpa using hasDerivAt_pow 3 r
  have hA : HasDerivAt (fun x : ℝ => Pc * x ^ 3 / 3) (Pc * (3 * r ^ 2) / 3) r := (h3.const_mul Pc).div_const 3
  have hB := (h3.div_const 3).mul ((hasDerivAt_const r (Real.log rc)).sub hl)
  have key : HasDerivAt (fun x : ℝ => Pc * x ^ 3 / 3 + s * (x ^ 3 / 3 * (Real.log rc - Real.log x)))
      (Pc * (3 * r ^ 2) / 3 + s * (3 * r ^ 2 / 3 * (Real.log rc - Real.log r) + r ^ 3 / 3 * (0 - r⁻¹))) r :=
    hA.add (hB.const_mul s)
  have hF : (Fw Pc s rc) = fun x => Pc * x ^ 3 / 3 + s * (x ^ 3 / 3 * (Real.log rc - Real.log x)) := by funext x; rfl
  rw [hF]
  convert key using 1
  have hr0 : r ≠ 0 := hr.ne'
  field_simp
  ring

theorem saturn_decreasing_FALSE {A B μ1 μ2 : ℝ} (hAB : 0 < A + B) (h1 : 0 ≤ μ1) (h12 : μ1 < μ2) :
    μ2 ^ 2 * (A + B) < μ1 ^ 2 * (A + B) := by
  have : μ1 ^ 2 < μ2 ^ 2 := by nlinarith
  nlinarith

theorem cap_law_relation_FALSE {ms x X : ℝ} (hX : 0 < X) (hx : 0 < x) (hms : 0 < ms)
    (h : ms / 2 + Real.sqrt (ms ^ 2 / 4 + ms * x ^ 2) = 1 + X) :
    ms = (1 + X) / (x ^ 2 + 1 + X) := by
  have hs : Real.sqrt (ms ^ 2 / 4 + ms * x ^ 2) = 1 + X - ms / 2 := by linarith
  have hnn : 0 ≤ ms ^ 2 / 4 + ms * x ^ 2 := by positivity
  have hsq := Real.sq_sqrt hnn
  rw [hs] at hsq
  have hden : 0 < x ^ 2 + 1 + X := by positivity
  rw [eq_div_iff (ne_of_gt hden)]
  nlinarith [hsq]

end MK1M
-- κ = ½ FITTED; not theory closed. Adopts nothing.
