import Mathlib

/-!
# EQB_S4b -- the sum rule  INT dmu/|t| = 1  of the framework kernel's spectral measure (Lean 4 certificate)

Source (committed): `prep_2026/equation_book/s4_kernel_spectral.py`, lines 51-68 (measure bookkeeping in u = sqrt|t| and the v11 sum
rule; the script does it with sympy `integrate`); header lines 5-9 give the measure; write-up `MINE_M2.md` item 3 (the sum rule as
unit total weight of the memory) and item 9 (the family M_p; M_1 = 1).

PREMISE (a declared object of the published action, NOT certified as physics): the positive measure on the cut t < 0,
    region A: rho_A(t) = (1 - sqrt(1 - 4|t|)) / (2 pi sqrt|t|)   on |t| in (0, 1/4),
    region B: rho_B(t) = 1 / (2 pi sqrt|t|)                       on |t| > 1/4.
Substituting |t| = u^2 (dt = 2u du) the two regions become dmu_A = (1 - sqrt(1 - 4u^2))/pi du on (0, 1/2) and dmu_B = du/pi on (1/2, oo).
Lean takes this measure as given; that it is THE Herglotz measure of K(z) = (sqrt(1+4z) - 1)/(2 sqrt z) is the script's (and the
published action's) claim, not re-proved here.

CERTIFIED (premises => conclusions, exact real analysis; improper integrals are stated as limits of proper interval integrals):
  * `dmuA_subst`, `dmuB_subst` : rho(t) dt = dmu in the variable u  (u != 0)
  * `dmu_nonneg`               : the density of dmu_A is >= 0 for 0 < u <= 1/2 (a positive measure)
  * `regionA_moment`           : lim_{eps -> 0+} INT_eps^{1/2} (1 - sqrt(1 - 4u^2))/(pi u^2) du = 1 - 2/pi
  * `regionB_moment`           : lim_{T -> oo}  INT_{1/2}^T 1/(pi u^2) du = 2/pi
  * `sum_rule`                 : the total INT dmu/|t| = (1 - 2/pi) + 2/pi = 1   (the v11 sum rule)
The antiderivative used for region A is F(u) = ((sqrt(1-4u^2) - 1)/u + 2 arcsin(2u))/pi, differentiated exactly on (0, 1/2).
NOT certified: that this measure represents K (Herglotz representation), the master identity INT dmu/(|t|+z) = 1 - K(z), the
time-domain memory function (Bessel/Struve), the moment family M_p for p != 1 (Wallis/Gamma: numerical mpmath checks in the script).
kappa = 1/2 (FITTED) does not enter.
-/

open Real Filter Topology intervalIntegral MeasureTheory

noncomputable section

/-- density of dmu_A with respect to du, times 1/u^2 (the weight 1/|t|). -/
def fA (u : ℝ) : ℝ := (1 - Real.sqrt (1 - 4 * u ^ 2)) / (Real.pi * u ^ 2)

/-- density of dmu_B with respect to du, times 1/u^2. -/
def fB (u : ℝ) : ℝ := 1 / (Real.pi * u ^ 2)

/-- antiderivative of fA. -/
def FA (u : ℝ) : ℝ := ((Real.sqrt (1 - 4 * u ^ 2) - 1) / u + 2 * Real.arcsin (2 * u)) / Real.pi

theorem dmuA_subst {u : ℝ} (hu : u ≠ 0) :
    (1 - Real.sqrt (1 - 4 * u ^ 2)) / (2 * Real.pi * Real.sqrt (u ^ 2)) * (2 * u)
      = (1 - Real.sqrt (1 - 4 * u ^ 2)) / Real.pi * (u / Real.sqrt (u ^ 2)) := by
  have : Real.pi ≠ 0 := Real.pi_ne_zero
  have hs : Real.sqrt (u ^ 2) ≠ 0 := by
    rw [Real.sqrt_sq_eq_abs]; exact abs_ne_zero.mpr hu
  field_simp

theorem dmuB_subst {u : ℝ} (hu : 0 < u) :
    1 / (2 * Real.pi * Real.sqrt (u ^ 2)) * (2 * u) = 1 / Real.pi := by
  have : Real.pi ≠ 0 := Real.pi_ne_zero
  rw [Real.sqrt_sq hu.le]
  field_simp

theorem dmuA_subst_pos {u : ℝ} (hu : 0 < u) :
    (1 - Real.sqrt (1 - 4 * u ^ 2)) / (2 * Real.pi * Real.sqrt (u ^ 2)) * (2 * u)
      = (1 - Real.sqrt (1 - 4 * u ^ 2)) / Real.pi := by
  rw [dmuA_subst hu.ne', Real.sqrt_sq hu.le, div_self hu.ne', mul_one]

theorem dmu_nonneg {u : ℝ} (hu : 0 < u) : 0 ≤ fA u := by
  unfold fA
  have h : Real.sqrt (1 - 4 * u ^ 2) ≤ 1 := by
    rw [Real.sqrt_le_one]; nlinarith
  apply div_nonneg (by linarith) (by positivity)

theorem FA_hasDeriv {x : ℝ} (hx : 0 < x) (hx2 : x < 1 / 2) : HasDerivAt FA (fA x) x := by
  have h1 : 0 < 1 - 4 * x ^ 2 := by nlinarith
  have hs0 : 0 < Real.sqrt (1 - 4 * x ^ 2) := Real.sqrt_pos.mpr h1
  have hxne : x ≠ 0 := hx.ne'
  have hpi : Real.pi ≠ 0 := Real.pi_ne_zero
  -- s(x) = sqrt(1 - 4 x^2)
  have hin : HasDerivAt (fun t : ℝ => 1 - 4 * t ^ 2) (-(4 * (2 * x))) x := by
    have := ((hasDerivAt_pow 2 x).const_mul 4).const_sub 1
    refine this.congr_deriv ?_
    simp
  have hs : HasDerivAt (fun t : ℝ => Real.sqrt (1 - 4 * t ^ 2))
      (-(4 * (2 * x)) / (2 * Real.sqrt (1 - 4 * x ^ 2))) x := hin.sqrt h1.ne'
  have hnum : HasDerivAt (fun t : ℝ => Real.sqrt (1 - 4 * t ^ 2) - 1)
      (-(4 * (2 * x)) / (2 * Real.sqrt (1 - 4 * x ^ 2))) x := hs.sub_const 1
  have hdiv := hnum.div (hasDerivAt_id x) hxne
  have hin2 : HasDerivAt (fun t : ℝ => 2 * t) 2 x := by
    simpa using (hasDerivAt_id x).const_mul 2
  have hne1 : 2 * x ≠ -1 := by intro h; linarith
  have hne2 : 2 * x ≠ 1 := by intro h; linarith
  have harc := (Real.hasDerivAt_arcsin (x := 2 * x) hne1 hne2).comp x hin2
  have hsum := (hdiv.add (harc.const_mul 2)).div_const Real.pi
  unfold FA fA
  refine hsum.congr_deriv ?_
  have e : 1 - (2 * x) ^ 2 = 1 - 4 * x ^ 2 := by ring
  simp only [id, e]
  generalize Real.sqrt (1 - 4 * x ^ 2) = s at hs0 ⊢
  have hs0' : s ≠ 0 := hs0.ne'
  field_simp
  ring

theorem FA_continuousOn {a : ℝ} (ha : 0 < a) : ContinuousOn FA (Set.Icc a (1 / 2)) := by
  intro x hx
  have hxpos : 0 < x := lt_of_lt_of_le ha hx.1
  unfold FA
  have hc1 : ContinuousAt (fun t : ℝ => Real.sqrt (1 - 4 * t ^ 2)) x := by fun_prop
  have hc2 : ContinuousAt (fun t : ℝ => (Real.sqrt (1 - 4 * t ^ 2) - 1) / t) x :=
    (hc1.sub continuousAt_const).div continuousAt_id hxpos.ne'
  have hc3 : ContinuousAt (fun t : ℝ => 2 * Real.arcsin (2 * t)) x := by
    exact (continuous_const.mul (Real.continuous_arcsin.comp (continuous_const.mul continuous_id))).continuousAt
  exact ((hc2.add hc3).div_const Real.pi).continuousWithinAt

theorem fA_continuousOn {a : ℝ} (ha : 0 < a) : ContinuousOn fA (Set.Icc a (1 / 2)) := by
  intro x hx
  have hxpos : 0 < x := lt_of_lt_of_le ha hx.1
  unfold fA
  have hc1 : ContinuousAt (fun t : ℝ => Real.sqrt (1 - 4 * t ^ 2)) x := by fun_prop
  have hc2 : ContinuousAt (fun t : ℝ => 1 - Real.sqrt (1 - 4 * t ^ 2)) x := continuousAt_const.sub hc1
  have hc3 : ContinuousAt (fun t : ℝ => Real.pi * t ^ 2) x := by fun_prop
  exact (hc2.div hc3 (by positivity)).continuousWithinAt

theorem FA_half : FA (1 / 2) = 1 - 2 / Real.pi := by
  unfold FA
  have : Real.sqrt (1 - 4 * (1 / 2 : ℝ) ^ 2) = 0 := by norm_num
  rw [this]
  have h2 : Real.arcsin (2 * (1 / 2 : ℝ)) = Real.pi / 2 := by
    rw [show (2 * (1 / 2 : ℝ)) = 1 by norm_num, Real.arcsin_one]
  rw [h2]
  have hpi : Real.pi ≠ 0 := Real.pi_ne_zero
  field_simp
  ring

theorem regionA_interval {ε : ℝ} (hε : 0 < ε) (hε2 : ε < 1 / 2) :
    ∫ u in ε..(1 / 2), fA u = FA (1 / 2) - FA ε := by
  apply intervalIntegral.integral_eq_sub_of_hasDerivAt_of_le hε2.le (FA_continuousOn hε)
  · intro x hx
    exact FA_hasDeriv (lt_trans hε hx.1) hx.2
  · exact (fA_continuousOn hε).intervalIntegrable_of_Icc hε2.le

theorem FA_tendsto_zero : Tendsto FA (𝓝[>] 0) (𝓝 0) := by
  have hcont : Continuous (fun t : ℝ => -4 * t / (Real.sqrt (1 - 4 * t ^ 2) + 1)) := by
    apply Continuous.div (by fun_prop) (by fun_prop)
    intro t; have := Real.sqrt_nonneg (1 - 4 * t ^ 2); linarith
  have h1 : Tendsto (fun t : ℝ => -4 * t / (Real.sqrt (1 - 4 * t ^ 2) + 1)) (𝓝 0) (𝓝 0) := by
    have := hcont.tendsto 0
    simpa using this
  have h2 : Tendsto (fun t : ℝ => 2 * Real.arcsin (2 * t)) (𝓝 0) (𝓝 0) := by
    have hc : Continuous (fun t : ℝ => 2 * Real.arcsin (2 * t)) :=
      continuous_const.mul (Real.continuous_arcsin.comp (continuous_const.mul continuous_id))
    have := hc.tendsto 0
    simpa using this
  have h3 : Tendsto (fun t : ℝ => (-4 * t / (Real.sqrt (1 - 4 * t ^ 2) + 1) + 2 * Real.arcsin (2 * t)) / Real.pi)
      (𝓝 0) (𝓝 0) := by
    have := (h1.add h2).div_const Real.pi
    simpa using this
  have h4 := h3.mono_left (nhdsWithin_le_nhds (s := Set.Ioi (0 : ℝ)))
  refine h4.congr' ?_
  filter_upwards [Ioo_mem_nhdsGT (show (0 : ℝ) < 1 / 2 by norm_num)] with t ht
  have ht0 : 0 < t := ht.1
  have h1t : 0 < 1 - 4 * t ^ 2 := by nlinarith [ht.2]
  have hs := Real.sq_sqrt h1t.le
  have hs0 : 0 ≤ Real.sqrt (1 - 4 * t ^ 2) := Real.sqrt_nonneg _
  unfold FA
  congr 1
  congr 1
  have hpos : Real.sqrt (1 - 4 * t ^ 2) + 1 ≠ 0 := by linarith
  field_simp
  nlinarith [hs]

theorem regionA_moment :
    Tendsto (fun ε : ℝ => ∫ u in ε..(1 / 2), fA u) (𝓝[>] 0) (𝓝 (1 - 2 / Real.pi)) := by
  have h := (tendsto_const_nhds (x := FA (1 / 2))).sub FA_tendsto_zero
  rw [sub_zero, FA_half] at h
  refine h.congr' ?_
  filter_upwards [Ioo_mem_nhdsGT (show (0 : ℝ) < 1 / 2 by norm_num)] with ε hε
  rw [regionA_interval hε.1 hε.2, FA_half]

theorem regionB_interval {T : ℝ} (hT : 1 / 2 ≤ T) :
    ∫ u in (1 / 2 : ℝ)..T, fB u = (1 / Real.pi) * (2 - 1 / T) := by
  have hTpos : 0 < T := by linarith
  have hpi : Real.pi ≠ 0 := Real.pi_ne_zero
  have hderiv : ∀ x ∈ Set.Ioo (1 / 2 : ℝ) T, HasDerivAt (fun t : ℝ => -(1 / Real.pi) * (1 / t)) (fB x) x := by
    intro x hx
    have hx0 : 0 < x := lt_trans (by norm_num) hx.1
    have := ((hasDerivAt_inv hx0.ne').const_mul (-(1 / Real.pi)))
    unfold fB
    refine (by simpa [one_div] using this : HasDerivAt (fun t : ℝ => -(1 / Real.pi) * (1 / t)) _ x).congr_deriv ?_
    field_simp
  have hcont : ContinuousOn (fun t : ℝ => -(1 / Real.pi) * (1 / t)) (Set.Icc (1 / 2 : ℝ) T) := by
    intro x hx
    have hx0 : 0 < x := lt_of_lt_of_le (by norm_num) hx.1
    exact ((continuousAt_const.mul (continuousAt_const.div continuousAt_id hx0.ne'))).continuousWithinAt
  have hint : IntervalIntegrable fB volume (1 / 2 : ℝ) T := by
    apply ContinuousOn.intervalIntegrable_of_Icc hT
    intro x hx
    have hx0 : 0 < x := lt_of_lt_of_le (by norm_num) hx.1
    unfold fB
    exact (continuousAt_const.div (by fun_prop : ContinuousAt (fun t : ℝ => Real.pi * t ^ 2) x)
      (by positivity)).continuousWithinAt
  rw [intervalIntegral.integral_eq_sub_of_hasDerivAt_of_le hT hcont hderiv hint]
  field_simp
  ring

theorem regionB_moment :
    Tendsto (fun T : ℝ => ∫ u in (1 / 2 : ℝ)..T, fB u) atTop (𝓝 (2 / Real.pi)) := by
  have hlim : Tendsto (fun T : ℝ => (1 / Real.pi) * (2 - 1 / T)) atTop (𝓝 ((1 / Real.pi) * (2 - 0))) := by
    have h0 : Tendsto (fun T : ℝ => 1 / T) atTop (𝓝 0) := by
      simpa using tendsto_inv_atTop_zero (𝕜 := ℝ)
    exact tendsto_const_nhds.mul (tendsto_const_nhds.sub h0)
  have hval : (1 / Real.pi) * (2 - 0) = 2 / Real.pi := by ring
  rw [hval] at hlim
  refine hlim.congr' ?_
  filter_upwards [eventually_ge_atTop (1 / 2 : ℝ)] with T hT
  exact (regionB_interval hT).symm

/-- the v11 sum rule: total inverse-moment weight INT dmu/|t| = 1. -/
theorem sum_rule :
    Tendsto (fun ε : ℝ => ∫ u in ε..(1 / 2), fA u) (𝓝[>] 0) (𝓝 (1 - 2 / Real.pi)) ∧
    Tendsto (fun T : ℝ => ∫ u in (1 / 2 : ℝ)..T, fB u) atTop (𝓝 (2 / Real.pi)) ∧
    (1 - 2 / Real.pi) + 2 / Real.pi = 1 := ⟨regionA_moment, regionB_moment, by ring⟩

end

#print axioms dmuA_subst_pos
#print axioms dmuB_subst
#print axioms dmu_nonneg
#print axioms FA_hasDeriv
#print axioms FA_half
#print axioms regionA_moment
#print axioms regionB_moment
#print axioms sum_rule
