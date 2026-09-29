import Mathlib

open MeasureTheory Set Real Filter Topology

/-- primitive of sqrt(x/(1-x)) on [0,1]:  arcsin(sqrt x) - sqrt(x(1-x)) -/
noncomputable def ffPrim (x : ℝ) : ℝ := Real.arcsin (Real.sqrt x) - Real.sqrt (x * (1 - x))

theorem ffPrim_hasDerivAt {x : ℝ} (h0 : 0 < x) (h1 : x < 1) :
    HasDerivAt ffPrim (Real.sqrt (x / (1 - x))) x := by
  have hx : x ≠ 0 := h0.ne'
  have h1x : 0 < 1 - x := by linarith
  have hs : 0 < Real.sqrt x := Real.sqrt_pos.mpr h0
  have ht : 0 < Real.sqrt (1 - x) := Real.sqrt_pos.mpr h1x
  have ss : Real.sqrt x ^ 2 = x := Real.sq_sqrt h0.le
  have tt : Real.sqrt (1 - x) ^ 2 = 1 - x := Real.sq_sqrt h1x.le
  have hsx := Real.hasDerivAt_sqrt hx
  have hne1 : Real.sqrt x ≠ -1 := by linarith
  have hne2 : Real.sqrt x ≠ 1 := by
    intro h; rw [h] at ss; norm_num at ss; linarith
  have ha := (Real.hasDerivAt_arcsin hne1 hne2).comp x hsx
  have hq : HasDerivAt (fun y : ℝ => y * (1 - y)) (1 - 2 * x) x := by
    have h := (hasDerivAt_id' x).fun_mul ((hasDerivAt_id' x).const_sub 1)
    exact h.congr_deriv (by ring)
  have hqs := hq.sqrt (by positivity)
  have hF := ha.sub hqs
  unfold ffPrim
  refine hF.congr_deriv ?_
  have e1 : Real.sqrt (1 - Real.sqrt x ^ 2) = Real.sqrt (1 - x) := by rw [ss]
  have e2 : Real.sqrt (x * (1 - x)) = Real.sqrt x * Real.sqrt (1 - x) := Real.sqrt_mul h0.le _
  have e3 : Real.sqrt (x / (1 - x)) = Real.sqrt x / Real.sqrt (1 - x) := Real.sqrt_div h0.le _
  rw [e1, e2, e3]
  field_simp
  nlinarith [ss, tt]

theorem ffPrim_zero : ffPrim 0 = 0 := by simp [ffPrim]
theorem ffPrim_one : ffPrim 1 = π / 2 := by simp [ffPrim]

theorem ffPrim_continuous : Continuous ffPrim := by
  unfold ffPrim
  have h1 : Continuous fun x : ℝ => Real.arcsin (Real.sqrt x) :=
    Real.continuous_arcsin.comp Real.continuous_sqrt
  have h2 : Continuous fun x : ℝ => Real.sqrt (x * (1 - x)) :=
    Real.continuous_sqrt.comp (by fun_prop)
  exact h1.sub h2

/-- int_0^1 sqrt(x/(1-x)) dx = pi/2  (the improper end at x = 1 is integrable) -/
theorem int_sqrt_ratio : ∫ x in (0:ℝ)..1, Real.sqrt (x / (1 - x)) = π / 2 := by
  have hint : IntervalIntegrable (fun x : ℝ => Real.sqrt (x / (1 - x))) volume 0 1 := by
    refine intervalIntegral.intervalIntegrable_deriv_of_nonneg (g := ffPrim)
      ffPrim_continuous.continuousOn ?_ ?_
    · intro x hx
      simp only [min_eq_left zero_le_one, max_eq_right zero_le_one] at hx
      exact ffPrim_hasDerivAt hx.1 hx.2
    · intro x _; exact Real.sqrt_nonneg _
  have := intervalIntegral.integral_eq_sub_of_hasDerivAt_of_le (zero_le_one' ℝ)
    ffPrim_continuous.continuousOn (fun x hx => ffPrim_hasDerivAt hx.1 hx.2) hint
  rw [this, ffPrim_one, ffPrim_zero]; ring

/-! ### the free-fall time from the energy equation  (1/2) rdot^2 = G M (1/r - 1/r0) -/

/-- t_ff(G, M, r0) = int_0^{r0} dr / |rdot|,  rdot^2 = 2 G M (1/r - 1/r0)  (release from rest at r0) -/
noncomputable def tff (G M r0 : ℝ) : ℝ := ∫ r in (0:ℝ)..r0, 1 / Real.sqrt (2 * G * M * (1 / r - 1 / r0))

theorem tff_integrand {G M r0 : ℝ} (hG : 0 < G) (hM : 0 < M) (hr : 0 < r0) {x : ℝ} (hx : x ∈ Set.uIcc (0:ℝ) 1) :
    1 / Real.sqrt (2 * G * M * (1 / (r0 * x) - 1 / r0)) = Real.sqrt (r0 / (2 * G * M)) * Real.sqrt (x / (1 - x)) := by
  rw [Set.uIcc_of_le zero_le_one] at hx
  obtain ⟨hx0, hx1⟩ := hx
  have hk : 0 < 2 * G * M := by positivity
  rcases hx0.eq_or_lt with h0 | h0
  · subst h0
    have : 2 * G * M * (1 / (r0 * 0) - 1 / r0) ≤ 0 := by
      simp only [mul_zero, div_zero, zero_sub]
      have : 0 < 1 / r0 := by positivity
      nlinarith
    rw [Real.sqrt_eq_zero_of_nonpos this]
    simp
  rcases hx1.eq_or_lt with h1 | h1
  · subst h1
    simp
  have h1x : 0 < 1 - x := by linarith
  have e : 2 * G * M * (1 / (r0 * x) - 1 / r0) = (2 * G * M / r0) * ((1 - x) / x) := by
    field_simp
  rw [e, Real.sqrt_mul (by positivity), one_div, mul_inv, ← Real.sqrt_inv, ← Real.sqrt_inv]
  congr 2
  · field_simp
  · rw [inv_div]

theorem tff_eq {G M r0 : ℝ} (hG : 0 < G) (hM : 0 < M) (hr : 0 < r0) :
    tff G M r0 = (π / 2) * Real.sqrt (r0 ^ 3 / (2 * G * M)) := by
  have hk : 0 < 2 * G * M := by positivity
  set g : ℝ → ℝ := fun r => 1 / Real.sqrt (2 * G * M * (1 / r - 1 / r0)) with hg
  have h := intervalIntegral.integral_comp_mul_left (a := (0:ℝ)) (b := 1) g hr.ne'
  simp only [mul_zero, mul_one, smul_eq_mul] at h
  have hcongr : ∫ x in (0:ℝ)..1, g (r0 * x) = ∫ x in (0:ℝ)..1, Real.sqrt (r0 / (2 * G * M)) * Real.sqrt (x / (1 - x)) := by
    refine intervalIntegral.integral_congr (fun x hx => ?_)
    exact tff_integrand hG hM hr hx
  rw [hcongr, intervalIntegral.integral_const_mul, int_sqrt_ratio] at h
  have h2 : ∫ x in (0:ℝ)..r0, g x = r0 * (Real.sqrt (r0 / (2 * G * M)) * (π / 2)) := by
    have := h
    field_simp at this ⊢
    linarith
  unfold tff
  show ∫ r in (0:ℝ)..r0, g r = _
  rw [h2]
  have h3 : Real.sqrt (r0 ^ 3 / (2 * G * M)) = r0 * Real.sqrt (r0 / (2 * G * M)) := by
    rw [show r0 ^ 3 / (2 * G * M) = r0 ^ 2 * (r0 / (2 * G * M)) by ring, Real.sqrt_mul (by positivity),
      Real.sqrt_sq hr.le]
  rw [h3]; ring

/-- uniform sphere, M = (4 pi/3) rho r0^3 :  t_ff = sqrt(3 pi/(32 G rho)) -/
theorem tff_uniform {G ρ r0 : ℝ} (hG : 0 < G) (hρ : 0 < ρ) (hr : 0 < r0) :
    tff G ((4 * π / 3) * ρ * r0 ^ 3) r0 = Real.sqrt (3 * π / (32 * G * ρ)) := by
  have hp := Real.pi_pos
  have hM : 0 < (4 * π / 3) * ρ * r0 ^ 3 := by positivity
  rw [tff_eq hG hM hr]
  have e : r0 ^ 3 / (2 * G * ((4 * π / 3) * ρ * r0 ^ 3)) = 3 / (8 * π * G * ρ) := by
    field_simp; ring
  rw [e]
  have hpos : 0 ≤ 3 / (8 * π * G * ρ) := by positivity
  have : π / 2 = Real.sqrt (π ^ 2 / 4) := by
    rw [show π ^ 2 / 4 = (π / 2) ^ 2 by ring, Real.sqrt_sq (by positivity)]
  rw [this, ← Real.sqrt_mul (by positivity)]
  congr 1
  field_simp; ring

/-- t_ff^2 = 3 pi/(32 G rho): the "pi/2 -> 3 pi/32 under the square root" step -/
theorem tff_sq_uniform {G ρ r0 : ℝ} (hG : 0 < G) (hρ : 0 < ρ) (hr : 0 < r0) :
    tff G ((4 * π / 3) * ρ * r0 ^ 3) r0 ^ 2 = 3 * π / (32 * G * ρ) := by
  have hp := Real.pi_pos
  rw [tff_uniform hG hρ hr, Real.sq_sqrt (by positivity)]

/-- in the puzzle's normalisation G rho = 4 a0^2:  a0^2 t_ff^2 = 3 pi/128 -/
theorem tff_puzzle_units {G ρ r0 a0 : ℝ} (hG : 0 < G) (hρ : 0 < ρ) (hr : 0 < r0) (ha : 0 < a0)
    (h : G * ρ = 4 * a0 ^ 2) : a0 ^ 2 * tff G ((4 * π / 3) * ρ * r0 ^ 3) r0 ^ 2 = 3 * π / 128 := by
  have hp := Real.pi_pos
  rw [tff_sq_uniform hG hρ hr]
  have : 32 * G * ρ = 128 * a0 ^ 2 := by nlinarith [h]
  rw [this]
  have : a0 ≠ 0 := ha.ne'
  field_simp

/-! ### independent check: the cycloid solves the energy equation and lands at r = 0 at time sqrt(3 pi/(32 G rho)) -/

theorem cycloid_r_deriv (r0 η : ℝ) :
    HasDerivAt (fun e : ℝ => (r0 / 2) * (1 + Real.cos e)) (-(r0 / 2) * Real.sin η) η := by
  have h := ((hasDerivAt_id' η).cos.const_add 1).const_mul (r0 / 2)
  exact h.congr_deriv (by ring)

theorem cycloid_t_deriv (A η : ℝ) :
    HasDerivAt (fun e : ℝ => A * (e + Real.sin e)) (A * (1 + Real.cos η)) η := by
  have h := ((hasDerivAt_id' η).add (Real.hasDerivAt_sin η)).const_mul A
  exact h.congr_deriv (by ring)

theorem cycloid_start (r0 : ℝ) : (r0 / 2) * (1 + Real.cos 0) = r0 := by simp; ring

/-- r(eta) = (r0/2)(1 + cos eta), t(eta) = A (eta + sin eta), A^2 = r0^3/(8 G M):
(dr/deta / dt/deta)^2 = 2 G M (1/r - 1/r0)  whenever cos eta != -1 -/
theorem cycloid_energy {G M r0 A η : ℝ} (hG : 0 < G) (hM : 0 < M) (hr : 0 < r0)
    (hA : A ^ 2 = r0 ^ 3 / (8 * G * M)) (hη : Real.cos η ≠ -1) :
    ((-(r0 / 2) * Real.sin η) / (A * (1 + Real.cos η))) ^ 2
      = 2 * G * M * (1 / ((r0 / 2) * (1 + Real.cos η)) - 1 / r0) := by
  have hc : 1 + Real.cos η ≠ 0 := fun h => hη (by linarith)
  have hs : Real.sin η ^ 2 = (1 - Real.cos η) * (1 + Real.cos η) := by
    nlinarith [Real.sin_sq_add_cos_sq η]
  have hAne : A ≠ 0 := by
    intro h; rw [h] at hA
    have : 0 < r0 ^ 3 / (8 * G * M) := by positivity
    nlinarith
  have hGM : G * M ≠ 0 := by positivity
  have h1 : (A * (1 + Real.cos η)) ^ 2 = r0 ^ 3 / (8 * G * M) * (1 + Real.cos η) ^ 2 := by rw [mul_pow, hA]
  have h2 : (-(r0 / 2) * Real.sin η) ^ 2 = (r0 / 2) ^ 2 * ((1 - Real.cos η) * (1 + Real.cos η)) := by
    rw [← hs]; ring
  rw [div_pow, h1, h2]
  field_simp
  ring

theorem cycloid_landing {G ρ r0 A : ℝ} (hG : 0 < G) (hρ : 0 < ρ) (hr : 0 < r0)
    (hA : A = Real.sqrt (r0 ^ 3 / (8 * G * ((4 * π / 3) * ρ * r0 ^ 3)))) :
    (r0 / 2) * (1 + Real.cos π) = 0 ∧ A * (π + Real.sin π) = Real.sqrt (3 * π / (32 * G * ρ)) := by
  have hp := Real.pi_pos
  refine ⟨by simp, ?_⟩
  rw [hA, Real.sin_pi, add_zero]
  have e : r0 ^ 3 / (8 * G * ((4 * π / 3) * ρ * r0 ^ 3)) = 3 / (32 * π * G * ρ) := by
    field_simp; ring
  rw [e]
  have hπ : π = Real.sqrt (π ^ 2) := (Real.sqrt_sq hp.le).symm
  calc Real.sqrt (3 / (32 * π * G * ρ)) * π = Real.sqrt (3 / (32 * π * G * ρ)) * Real.sqrt (π ^ 2) := by
        rw [← hπ]
    _ = Real.sqrt (3 / (32 * π * G * ρ) * π ^ 2) := (Real.sqrt_mul (by positivity) _).symm
    _ = Real.sqrt (3 * π / (32 * G * ρ)) := by congr 1; field_simp

#print axioms ffPrim_hasDerivAt
#print axioms int_sqrt_ratio
#print axioms tff_integrand
#print axioms tff_eq
#print axioms tff_uniform
#print axioms tff_sq_uniform
#print axioms tff_puzzle_units
#print axioms cycloid_r_deriv
#print axioms cycloid_t_deriv
#print axioms cycloid_start
#print axioms cycloid_energy
#print axioms cycloid_landing
