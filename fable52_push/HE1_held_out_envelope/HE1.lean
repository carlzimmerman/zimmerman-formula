/-
HE1 (criteria 0e67f3c64a): Lean statements for Part A, the held-out envelope. They certify the algebra and the inequalities,
not the physics. TEST lane; adopts nothing. kappa = 1/2 FITTED; not theory closed.

Units and symbols: r_M = sqrt(G M_b / a0) (so G M_b = a0 r_M^2), v_f^4 = G M_b a0 (written vf2^2 with vf2 = v_f^2, and
vf2 r_M = G M_b), y = G M_b / (a0 R^2) the Newtonian field at the wall in units of a0, u the law's field inside it
(y = u^2 / (1 + u)), q = sqrt(y) = r_M / R. SWT1 T3: p_wall = (a0^2 / 4 pi G) W(u),
W(u) = u - ln(1 + u) - u^2 / (2 (1 + u)^2). A singular isothermal envelope of dispersion sigma has rho = sigma^2 / (2 pi G r^2)
and pressure sigma^4 / (2 pi G r^2).

  copied        hasDerivAt_W, Dfun, hasDerivAt_Dfun, Dfun_nonneg, W_le_deep (SWT1.lean); hasDerivAt_Eup, W_upper (SNP1.lean)
  A1 deep_balance        the deep wall pressure (a0^2 / 4 pi G)(2/3)(r_M / R)^3 equals the singular envelope's pressure
                         iff R = r_M v_f^4 / (3 sigma^4)
  A2 amplitude_form      A = 2 sigma^2 / v_f^2 turns A1 into R / r_M = (4/3) / A^2
  A3 sis_mass            2 sigma^2 R / G = A (R / r_M) M_b (the shell R_w..R holds A ((R - R_w) / r_M) M_b: same identity)
  A4 W_lower3            (2/3) u^3 / (1 + u)^2 <= W(u) for u >= 0 (new; derivative of the difference u^3 / (3 (1 + u)^3))
  A5 dW_dy               W'(u) = (u - y) dy/du, so d ln W / d ln y = y (u - y) / W and d ln p_wall / d ln R = -2 y (u - y) / W
     slope_identity      y (u - y) = u^3 / (1 + u)^2
     slope_bracket       2 < 2 y (u - y) / W <= 3: the exact wall pressure falls faster than R^-2 and at most as R^-3
  A6 W_le_deep_q         W(u) <= (2/3) q^3 with q = sqrt(u^2 / (1 + u)) (SWT1's bound restated in q)
     cubic_mono          v^3 / (1 + v)^2 is increasing on v >= 0
     W_lower_q           (2/3) q^3 / (1 + q)^2 <= W(u)
     exact_vs_deep       with the balance s^2 = W / (2 q^2) (s = sigma^2 / v_f^2, R / r_M = 1 / q):
                         R_deep / (1 + q)^2 <= R <= R_deep, R_deep = r_M / (3 s^2)
  A7 stable_frozen       envelope pressure p_w x^n (x = R_w / R) with n < 2 against a wall pressure that falls at least as
                         R^-2 outward and at most as R^-2 inward (SNP1's Fw_decreasing: 4 pi R^2 p_wall falls with R):
                         every displacement meets a restoring net force
     deep_sis_stable     the brief's special case: n = 2 against the deep R^-3
     swept_restoring     with the displaced material carried at the wall the net outward force is p_wall(R) - p_wall(R_w)
  A8 jeans_wall_slope    at the deep balance the exact Jeans log-slope of the envelope's pressure at the wall,
                         -G M_b / (sigma^2 R_w), equals -(3/2) A
     deep_stable_iff     (3/2) A < 2 iff A < 4/3
-/
import Mathlib

namespace HE1

noncomputable def W (u : ℝ) : ℝ := u - Real.log (1 + u) - u ^ 2 / (2 * (1 + u) ^ 2)

/-! ### copied from SWT1.lean and SNP1.lean -/

theorem hasDerivAt_W (u : ℝ) (hu : -1 < u) :
    HasDerivAt W (u ^ 2 * (2 + u) / (1 + u) ^ 3) u := by
  have hp : (1 + u) ≠ 0 := by linarith
  have h1 : HasDerivAt (fun v : ℝ => 1 + v) 1 u := by
    simpa using (hasDerivAt_id u).const_add 1
  have hlog : HasDerivAt (fun v : ℝ => Real.log (1 + v)) ((1 + u)⁻¹ * 1) u :=
    (Real.hasDerivAt_log hp).comp u h1
  have hn : HasDerivAt (fun v : ℝ => v ^ 2) (2 * u) u := by
    simpa using hasDerivAt_pow 2 u
  have hd : HasDerivAt (fun v : ℝ => 2 * (1 + v) ^ 2) (2 * (2 * (1 + u) * 1)) u := by
    have := (h1.pow 2).const_mul 2
    simpa using this
  have hne : (2 * (1 + u) ^ 2) ≠ 0 := by positivity
  have hq := hn.div hd hne
  have hall : HasDerivAt (fun v : ℝ => v - Real.log (1 + v) - v ^ 2 / (2 * (1 + v) ^ 2))
      (1 - (1 + u)⁻¹ * 1 - (2 * u * (2 * (1 + u) ^ 2) - u ^ 2 * (2 * (2 * (1 + u) * 1))) / (2 * (1 + u) ^ 2) ^ 2) u :=
    ((hasDerivAt_id u).sub hlog).sub hq
  have hderiv : 1 - (1 + u)⁻¹ * 1 - (2 * u * (2 * (1 + u) ^ 2) - u ^ 2 * (2 * (2 * (1 + u) * 1))) / (2 * (1 + u) ^ 2) ^ 2
      = u ^ 2 * (2 + u) / (1 + u) ^ 3 := by
    field_simp
    ring
  have hfun : W = fun v : ℝ => v - Real.log (1 + v) - v ^ 2 / (2 * (1 + v) ^ 2) := by
    funext v; rfl
  rw [hfun]
  exact hall.congr_deriv hderiv

noncomputable def Dfun (t : ℝ) : ℝ :=
  2 / 3 * (t ^ 2 - 1) ^ 3 / t ^ 3 - ((t ^ 2 - 1) - 2 * Real.log t - (t ^ 2 - 1) ^ 2 / (2 * t ^ 4))

theorem hasDerivAt_Dfun (t : ℝ) (ht : 0 < t) :
    HasDerivAt Dfun (2 * (t ^ 2 - 1) ^ 2 * (t ^ 2 + 1) * (t - 1) / t ^ 5) t := by
  have ht0 : t ≠ 0 := ht.ne'
  have hb : HasDerivAt (fun v : ℝ => v ^ 2 - 1) (2 * t) t := by
    simpa using (hasDerivAt_pow 2 t).sub_const 1
  have hb3 : HasDerivAt (fun v : ℝ => 2 / 3 * (v ^ 2 - 1) ^ 3) (2 / 3 * (3 * (t ^ 2 - 1) ^ 2 * (2 * t))) t := by
    have := (hb.pow 3).const_mul (2 / 3 : ℝ)
    simpa using this
  have hp3 : HasDerivAt (fun v : ℝ => v ^ 3) (3 * t ^ 2) t := by
    simpa using hasDerivAt_pow 3 t
  have hA := hb3.div hp3 (pow_ne_zero 3 ht0)
  have hlog : HasDerivAt (fun v : ℝ => 2 * Real.log v) (2 * t⁻¹) t :=
    (Real.hasDerivAt_log ht0).const_mul 2
  have hb2 : HasDerivAt (fun v : ℝ => (v ^ 2 - 1) ^ 2) (2 * (t ^ 2 - 1) * (2 * t)) t := by
    have h' : HasDerivAt (fun v : ℝ => (v ^ 2 - 1) ^ 2) (((2 : ℕ) : ℝ) * (t ^ 2 - 1) ^ (2 - 1) * (2 * t)) t := hb.pow 2
    convert h' using 1
    norm_num
  have hp4 : HasDerivAt (fun v : ℝ => 2 * v ^ 4) (2 * (4 * t ^ 3)) t := by
    have := (hasDerivAt_pow 4 t).const_mul (2 : ℝ)
    simpa using this
  have hne4 : (2 * t ^ 4) ≠ 0 := by positivity
  have hE : HasDerivAt (fun v : ℝ => (v ^ 2 - 1) ^ 2 / (2 * v ^ 4))
      ((2 * (t ^ 2 - 1) * (2 * t) * (2 * t ^ 4) - (t ^ 2 - 1) ^ 2 * (2 * (4 * t ^ 3))) / (2 * t ^ 4) ^ 2) t :=
    hb2.div hp4 hne4
  have hA' : HasDerivAt (fun v : ℝ => 2 / 3 * (v ^ 2 - 1) ^ 3 / v ^ 3)
      ((2 / 3 * (3 * (t ^ 2 - 1) ^ 2 * (2 * t)) * t ^ 3 - 2 / 3 * (t ^ 2 - 1) ^ 3 * (3 * t ^ 2)) / (t ^ 3) ^ 2) t := hA
  have hall : HasDerivAt (fun v : ℝ =>
      2 / 3 * (v ^ 2 - 1) ^ 3 / v ^ 3 - ((v ^ 2 - 1) - 2 * Real.log v - (v ^ 2 - 1) ^ 2 / (2 * v ^ 4)))
      ((2 / 3 * (3 * (t ^ 2 - 1) ^ 2 * (2 * t)) * t ^ 3 - 2 / 3 * (t ^ 2 - 1) ^ 3 * (3 * t ^ 2)) / (t ^ 3) ^ 2
        - (2 * t - 2 * t⁻¹
          - (2 * (t ^ 2 - 1) * (2 * t) * (2 * t ^ 4) - (t ^ 2 - 1) ^ 2 * (2 * (4 * t ^ 3))) / (2 * t ^ 4) ^ 2)) t :=
    hA'.sub ((hb.sub hlog).sub hE)
  have hderiv : (2 / 3 * (3 * (t ^ 2 - 1) ^ 2 * (2 * t)) * t ^ 3 - 2 / 3 * (t ^ 2 - 1) ^ 3 * (3 * t ^ 2)) / (t ^ 3) ^ 2
        - (2 * t - 2 * t⁻¹
          - (2 * (t ^ 2 - 1) * (2 * t) * (2 * t ^ 4) - (t ^ 2 - 1) ^ 2 * (2 * (4 * t ^ 3))) / (2 * t ^ 4) ^ 2)
      = 2 * (t ^ 2 - 1) ^ 2 * (t ^ 2 + 1) * (t - 1) / t ^ 5 := by
    field_simp
    ring
  have hfun : Dfun = fun v : ℝ =>
      2 / 3 * (v ^ 2 - 1) ^ 3 / v ^ 3 - ((v ^ 2 - 1) - 2 * Real.log v - (v ^ 2 - 1) ^ 2 / (2 * v ^ 4)) := by
    funext v; rfl
  rw [hfun]
  exact hall.congr_deriv hderiv

theorem Dfun_nonneg (t : ℝ) (ht : 1 ≤ t) : 0 ≤ Dfun t := by
  have hmono : MonotoneOn Dfun (Set.Ici 1) := by
    apply monotoneOn_of_deriv_nonneg (convex_Ici 1)
    · intro x hx
      have hx1 : (1 : ℝ) ≤ x := hx
      exact (hasDerivAt_Dfun x (by linarith)).continuousAt.continuousWithinAt
    · intro x hx
      rw [interior_Ici] at hx
      have hx1 : (1 : ℝ) < x := hx
      exact (hasDerivAt_Dfun x (by linarith)).differentiableAt.differentiableWithinAt
    · intro x hx
      rw [interior_Ici] at hx
      have hx1 : (1 : ℝ) < x := hx
      rw [(hasDerivAt_Dfun x (by linarith)).deriv]
      have h1 : 0 < x := by linarith
      have h2 : 0 ≤ x - 1 := by linarith
      positivity
  have h1 : Dfun 1 = 0 := by simp [Dfun]
  have := hmono (Set.mem_Ici.mpr le_rfl) (Set.mem_Ici.mpr ht) ht
  linarith

theorem W_le_deep (t : ℝ) (ht : 1 ≤ t) : W (t ^ 2 - 1) ≤ 2 / 3 * (t ^ 2 - 1) ^ 3 / t ^ 3 := by
  have h := Dfun_nonneg t ht
  have ht0 : 0 < t := by linarith
  have hlog : Real.log (1 + (t ^ 2 - 1)) = 2 * Real.log t := by
    rw [show 1 + (t ^ 2 - 1) = t ^ 2 by ring, Real.log_pow]
    norm_num
  have hden : (2 : ℝ) * (1 + (t ^ 2 - 1)) ^ 2 = 2 * t ^ 4 := by ring
  unfold Dfun at h
  unfold W
  rw [hlog, hden]
  linarith

theorem hasDerivAt_Eup (u : ℝ) (hu : -1 < u) :
    HasDerivAt (fun v : ℝ => v ^ 3 / (1 + v) ^ 2 - W v) (u ^ 2 / (1 + u) ^ 3) u := by
  have hp : (1 + u) ≠ 0 := by linarith
  have h1 : HasDerivAt (fun v : ℝ => 1 + v) 1 u := by
    simpa using (hasDerivAt_id u).const_add 1
  have hn : HasDerivAt (fun v : ℝ => v ^ 3) (3 * u ^ 2) u := by
    simpa using hasDerivAt_pow 3 u
  have hd : HasDerivAt (fun v : ℝ => (1 + v) ^ 2) (2 * (1 + u)) u := by
    have h' : HasDerivAt (fun v : ℝ => (1 + v) ^ 2) (((2 : ℕ) : ℝ) * (1 + u) ^ (2 - 1) * 1) u := h1.pow 2
    convert h' using 1
    norm_num
  have hne : ((1 + u) ^ 2) ≠ 0 := by positivity
  have hq : HasDerivAt (fun v : ℝ => v ^ 3 / (1 + v) ^ 2)
      ((3 * u ^ 2 * (1 + u) ^ 2 - u ^ 3 * (2 * (1 + u))) / ((1 + u) ^ 2) ^ 2) u := hn.div hd hne
  have hall : HasDerivAt (fun v : ℝ => v ^ 3 / (1 + v) ^ 2 - W v)
      ((3 * u ^ 2 * (1 + u) ^ 2 - u ^ 3 * (2 * (1 + u))) / ((1 + u) ^ 2) ^ 2 - u ^ 2 * (2 + u) / (1 + u) ^ 3) u :=
    hq.sub (hasDerivAt_W u hu)
  refine hall.congr_deriv ?_
  field_simp
  ring

theorem W_upper (u : ℝ) (hu : 0 < u) : W u < u ^ 3 / (1 + u) ^ 2 := by
  have hmono : StrictMonoOn (fun v : ℝ => v ^ 3 / (1 + v) ^ 2 - W v) (Set.Ici 0) := by
    apply strictMonoOn_of_deriv_pos (convex_Ici 0)
    · intro x hx
      have hx0 : (0 : ℝ) ≤ x := hx
      exact (hasDerivAt_Eup x (by linarith)).continuousAt.continuousWithinAt
    · intro x hx
      rw [interior_Ici] at hx
      have hx0 : (0 : ℝ) < x := hx
      rw [(hasDerivAt_Eup x (by linarith)).deriv]
      positivity
  have h0 : (0 : ℝ) ^ 3 / (1 + 0) ^ 2 - W 0 = 0 := by simp [W]
  have := hmono (Set.mem_Ici.mpr le_rfl) (Set.mem_Ici.mpr hu.le) hu
  dsimp only at this
  linarith

/-! ### A1-A3: the deep closed forms -/

/-- A1: the deep wall pressure equals the singular envelope's pressure iff R = r_M v_f^4 / (3 sigma^4), v_f^4 = G M a0. -/
theorem deep_balance (G a0 M rM σ R : ℝ) (hG : 0 < G) (ha : 0 < a0) (hrM : 0 < rM) (hσ : 0 < σ) (hR : 0 < R)
    (hm : G * M = a0 * rM ^ 2) :
    σ ^ 4 / (2 * Real.pi * G * R ^ 2) = a0 ^ 2 / (4 * Real.pi * G) * (2 / 3 * (rM / R) ^ 3) ↔
      R = rM * (G * M * a0) / (3 * σ ^ 4) := by
  have hπ := Real.pi_pos
  have hG0 : G ≠ 0 := hG.ne'
  have hR0 : R ≠ 0 := hR.ne'
  have hπ0 : Real.pi ≠ 0 := hπ.ne'
  have hL : σ ^ 4 / (2 * Real.pi * G * R ^ 2) * (6 * Real.pi * G * R ^ 3) = 3 * σ ^ 4 * R := by
    field_simp
    ring
  have hRr : a0 ^ 2 / (4 * Real.pi * G) * (2 / 3 * (rM / R) ^ 3) * (6 * Real.pi * G * R ^ 3) = a0 ^ 2 * rM ^ 3 := by
    field_simp
    ring
  have hK : (6 * Real.pi * G * R ^ 3) ≠ 0 := by positivity
  have hs4 : (3 * σ ^ 4) ≠ 0 := by positivity
  constructor
  · intro h
    have key : 3 * σ ^ 4 * R = a0 ^ 2 * rM ^ 3 := by rw [← hL, ← hRr, h]
    rw [eq_div_iff hs4]
    linear_combination key - rM * a0 * hm
  · intro h
    have h1 : 3 * σ ^ 4 * R = rM * (G * M * a0) := by
      rw [h]
      field_simp
    have key : 3 * σ ^ 4 * R = a0 ^ 2 * rM ^ 3 := by linear_combination h1 + rM * a0 * hm
    apply mul_right_cancel₀ hK
    rw [hL, hRr, key]

/-- A2: with A = 2 sigma^2 / v_f^2 (vf2 = v_f^2) the deep balance reads R / r_M = (4/3) / A^2. -/
theorem amplitude_form (rM vf2 σ A R : ℝ) (hrM : 0 < rM) (hv : 0 < vf2) (hσ : 0 < σ)
    (hA : A = 2 * σ ^ 2 / vf2) (hR : R = rM * vf2 ^ 2 / (3 * σ ^ 4)) : R / rM = 4 / 3 / A ^ 2 := by
  subst hA
  subst hR
  field_simp
  ring

/-- A3: the singular envelope's mass 2 sigma^2 R / G is A (R / r_M) M (vf2 r_M = G M). -/
theorem sis_mass (G M rM vf2 σ A R : ℝ) (hG : 0 < G) (hrM : 0 < rM) (hv : 0 < vf2) (hvr : vf2 * rM = G * M)
    (hA : A = 2 * σ ^ 2 / vf2) : 2 * σ ^ 2 * R / G = A * (R / rM) * M := by
  subst hA
  have hM : M = vf2 * rM / G := by
    rw [eq_div_iff hG.ne']
    linear_combination -hvr
  rw [hM]
  field_simp

/-! ### A4-A6: the exact W -/

theorem hasDerivAt_Dlow (u : ℝ) (hu : -1 < u) :
    HasDerivAt (fun v : ℝ => W v - 2 / 3 * (v ^ 3 / (1 + v) ^ 2)) (u ^ 3 / (3 * (1 + u) ^ 3)) u := by
  have hp : (1 + u) ≠ 0 := by linarith
  have h1 : HasDerivAt (fun v : ℝ => 1 + v) 1 u := by
    simpa using (hasDerivAt_id u).const_add 1
  have hn : HasDerivAt (fun v : ℝ => v ^ 3) (3 * u ^ 2) u := by
    simpa using hasDerivAt_pow 3 u
  have hd : HasDerivAt (fun v : ℝ => (1 + v) ^ 2) (2 * (1 + u)) u := by
    have h' : HasDerivAt (fun v : ℝ => (1 + v) ^ 2) (((2 : ℕ) : ℝ) * (1 + u) ^ (2 - 1) * 1) u := h1.pow 2
    convert h' using 1
    norm_num
  have hne : ((1 + u) ^ 2) ≠ 0 := by positivity
  have hq : HasDerivAt (fun v : ℝ => v ^ 3 / (1 + v) ^ 2)
      ((3 * u ^ 2 * (1 + u) ^ 2 - u ^ 3 * (2 * (1 + u))) / ((1 + u) ^ 2) ^ 2) u := hn.div hd hne
  have hall : HasDerivAt (fun v : ℝ => W v - 2 / 3 * (v ^ 3 / (1 + v) ^ 2))
      (u ^ 2 * (2 + u) / (1 + u) ^ 3 - 2 / 3 * ((3 * u ^ 2 * (1 + u) ^ 2 - u ^ 3 * (2 * (1 + u))) / ((1 + u) ^ 2) ^ 2)) u :=
    (hasDerivAt_W u hu).sub (hq.const_mul (2 / 3 : ℝ))
  refine hall.congr_deriv ?_
  field_simp
  ring

/-- A4 (new): (2/3) u^3 / (1 + u)^2 <= W(u) for u >= 0. -/
theorem W_lower3 (u : ℝ) (hu : 0 ≤ u) : 2 / 3 * (u ^ 3 / (1 + u) ^ 2) ≤ W u := by
  have hmono : MonotoneOn (fun v : ℝ => W v - 2 / 3 * (v ^ 3 / (1 + v) ^ 2)) (Set.Ici 0) := by
    apply monotoneOn_of_deriv_nonneg (convex_Ici 0)
    · intro x hx
      have hx0 : (0 : ℝ) ≤ x := hx
      exact (hasDerivAt_Dlow x (by linarith)).continuousAt.continuousWithinAt
    · intro x hx
      rw [interior_Ici] at hx
      have hx0 : (0 : ℝ) < x := hx
      exact (hasDerivAt_Dlow x (by linarith)).differentiableAt.differentiableWithinAt
    · intro x hx
      rw [interior_Ici] at hx
      have hx0 : (0 : ℝ) < x := hx
      rw [(hasDerivAt_Dlow x (by linarith)).deriv]
      positivity
  have h0 : W 0 - 2 / 3 * ((0 : ℝ) ^ 3 / (1 + 0) ^ 2) = 0 := by simp [W]
  have := hmono (Set.mem_Ici.mpr le_rfl) (Set.mem_Ici.mpr hu) hu
  dsimp only at this
  linarith

/-- A5: W'(u) = (u - y) dy/du with y = u^2 / (1 + u) (so dW = (u - y) dy). -/
theorem dW_dy (u : ℝ) (hu : 0 < u) :
    u ^ 2 * (2 + u) / (1 + u) ^ 3 = (u - u ^ 2 / (1 + u)) * (u * (2 + u) / (1 + u) ^ 2) := by
  have hp : (1 + u) ≠ 0 := by linarith
  field_simp
  ring

/-- A5: y (u - y) = u^3 / (1 + u)^2. -/
theorem slope_identity (u : ℝ) (hu : 0 < u) :
    u ^ 2 / (1 + u) * (u - u ^ 2 / (1 + u)) = u ^ 3 / (1 + u) ^ 2 := by
  have hp : (1 + u) ≠ 0 := by linarith
  field_simp
  ring

/-- A5: the log-slope magnitude 2 y (u - y) / W lies in (2, 3]. -/
theorem slope_bracket (u : ℝ) (hu : 0 < u) :
    2 < 2 * (u ^ 3 / (1 + u) ^ 2) / W u ∧ 2 * (u ^ 3 / (1 + u) ^ 2) / W u ≤ 3 := by
  have hW := W_upper u hu
  have hL := W_lower3 u hu.le
  have hc : 0 < u ^ 3 / (1 + u) ^ 2 := by positivity
  have hWpos : 0 < W u := by linarith
  constructor
  · rw [lt_div_iff₀ hWpos]
    linarith
  · rw [div_le_iff₀ hWpos]
    linarith

/-- A6: SWT1's deep bound restated with q = sqrt(u^2 / (1 + u)) = sqrt(y). -/
theorem W_le_deep_q (u : ℝ) (hu : 0 ≤ u) : W u ≤ 2 / 3 * Real.sqrt (u ^ 2 / (1 + u)) ^ 3 := by
  obtain ⟨t, ht1, rfl⟩ : ∃ t : ℝ, 1 ≤ t ∧ u = t ^ 2 - 1 := by
    refine ⟨Real.sqrt (1 + u), ?_, ?_⟩
    · have h := Real.sqrt_le_sqrt (show (1 : ℝ) ≤ 1 + u by linarith)
      rwa [Real.sqrt_one] at h
    · rw [Real.sq_sqrt (by linarith)]
      ring
  have ht0 : 0 < t := by linarith
  have hq : Real.sqrt ((t ^ 2 - 1) ^ 2 / (1 + (t ^ 2 - 1))) = (t ^ 2 - 1) / t := by
    rw [show (t ^ 2 - 1) ^ 2 / (1 + (t ^ 2 - 1)) = ((t ^ 2 - 1) / t) ^ 2 by
      rw [div_pow]
      ring_nf]
    exact Real.sqrt_sq (div_nonneg (by nlinarith) ht0.le)
  rw [hq]
  have h := W_le_deep t ht1
  have e : 2 / 3 * ((t ^ 2 - 1) / t) ^ 3 = 2 / 3 * (t ^ 2 - 1) ^ 3 / t ^ 3 := by
    rw [div_pow]
    ring
  rw [e]
  exact h

/-- A6: v^3 / (1 + v)^2 is increasing on v >= 0. -/
theorem cubic_mono (a b : ℝ) (ha : 0 ≤ a) (hab : a ≤ b) : a ^ 3 / (1 + a) ^ 2 ≤ b ^ 3 / (1 + b) ^ 2 := by
  have hb : 0 ≤ b := le_trans ha hab
  rw [div_le_div_iff₀ (by positivity) (by positivity)]
  have key : b ^ 3 * (1 + a) ^ 2 - a ^ 3 * (1 + b) ^ 2
      = (b - a) * ((b ^ 2 + a * b + a ^ 2) + 2 * a * b * (a + b) + a ^ 2 * b ^ 2) := by ring
  have hpos : 0 ≤ (b ^ 2 + a * b + a ^ 2) + 2 * a * b * (a + b) + a ^ 2 * b ^ 2 := by positivity
  nlinarith [mul_nonneg (sub_nonneg.2 hab) hpos]

/-- A6: (2/3) q^3 / (1 + q)^2 <= W(u), q = sqrt(u^2 / (1 + u)). -/
theorem W_lower_q (u : ℝ) (hu : 0 < u) :
    2 / 3 * (Real.sqrt (u ^ 2 / (1 + u)) ^ 3 / (1 + Real.sqrt (u ^ 2 / (1 + u))) ^ 2) ≤ W u := by
  have hq0 : 0 ≤ Real.sqrt (u ^ 2 / (1 + u)) := Real.sqrt_nonneg _
  have hy : u ^ 2 / (1 + u) ≤ u ^ 2 := div_le_self (sq_nonneg u) (by linarith)
  have hqu : Real.sqrt (u ^ 2 / (1 + u)) ≤ u := by
    calc Real.sqrt (u ^ 2 / (1 + u)) ≤ Real.sqrt (u ^ 2) := Real.sqrt_le_sqrt hy
      _ = u := Real.sqrt_sq hu.le
  have hm := cubic_mono _ _ hq0 hqu
  have hL := W_lower3 u hu.le
  nlinarith

/-- A6: with the exact balance s^2 = W / (2 q^2) and the two bounds on W, R / r_M = 1 / q lies between
R_deep / (1 + q)^2 and R_deep, R_deep / r_M = 1 / (3 s^2). -/
theorem exact_vs_deep (q s Wv : ℝ) (hq : 0 < q) (hs : 0 < s) (hb : s ^ 2 = Wv / (2 * q ^ 2))
    (hup : Wv ≤ 2 / 3 * q ^ 3) (hlo : 2 / 3 * (q ^ 3 / (1 + q) ^ 2) ≤ Wv) :
    1 / q ≤ 1 / (3 * s ^ 2) ∧ 1 / (3 * s ^ 2) / (1 + q) ^ 2 ≤ 1 / q := by
  have hq2 : 0 < 2 * q ^ 2 := by positivity
  have h1 : 3 * s ^ 2 ≤ q := by
    rw [hb, show 3 * (Wv / (2 * q ^ 2)) = (3 * Wv) / (2 * q ^ 2) by ring, div_le_iff₀ hq2]
    have : q * (2 * q ^ 2) = 2 * q ^ 3 := by ring
    linarith
  have h2 : q ≤ 3 * s ^ 2 * (1 + q) ^ 2 := by
    have hmono : 2 / 3 * (q ^ 3 / (1 + q) ^ 2) / (2 * q ^ 2) ≤ Wv / (2 * q ^ 2) :=
      div_le_div_of_nonneg_right hlo hq2.le
    have he : 3 * (2 / 3 * (q ^ 3 / (1 + q) ^ 2) / (2 * q ^ 2)) * (1 + q) ^ 2 = q := by
      field_simp
    have hp : 0 ≤ 3 * (1 + q) ^ 2 := by positivity
    rw [hb]
    nlinarith [mul_le_mul_of_nonneg_left hmono hp]
  have hs2 : 0 < 3 * s ^ 2 := by positivity
  constructor
  · exact one_div_le_one_div_of_le hs2 h1
  · rw [div_div]
    exact one_div_le_one_div_of_le hq h2

/-! ### A7-A8: stability -/

/-- A7: envelope pressure p_w x^n (x = R_w / R), n < 2, against a wall pressure below p_w x^2 outward (x < 1) and above it
inward (x > 1): the net outward force on the wall, p_wall - p_env, is restoring on both sides. -/
theorem stable_frozen (pw n x pwall : ℝ) (hpw : 0 < pw) (hn : n < 2) (hx : 0 < x) :
    (x < 1 → pwall ≤ pw * x ^ (2 : ℝ) → pwall - pw * x ^ n < 0) ∧
    (1 < x → pw * x ^ (2 : ℝ) ≤ pwall → 0 < pwall - pw * x ^ n) := by
  constructor
  · intro hx1 hw
    have h := Real.rpow_lt_rpow_of_exponent_gt hx hx1 hn
    have := mul_lt_mul_of_pos_left h hpw
    linarith
  · intro hx1 hw
    have h := Real.rpow_lt_rpow_of_exponent_lt hx1 hn
    have := mul_lt_mul_of_pos_left h hpw
    linarith

/-- A7, the brief's special case: a singular envelope (R^-2) against the deep wall (R^-3). -/
theorem deep_sis_stable (x : ℝ) (hx : 0 < x) : (x < 1 → x ^ 3 < x ^ 2) ∧ (1 < x → x ^ 2 < x ^ 3) := by
  constructor
  · intro h1
    nlinarith [mul_pos (pow_pos hx 2) (sub_pos.2 h1)]
  · intro h1
    nlinarith [mul_pos (pow_pos hx 2) (sub_pos.2 h1)]

/-- A7, swept-layer reading: if p_wall strictly falls with R, the net outward force after an outward displacement,
p_wall(R) - p_wall(R_w), is negative. -/
theorem swept_restoring (f : ℝ → ℝ) (S : Set ℝ) (hf : StrictAntiOn f S) (a b : ℝ) (ha : a ∈ S) (hb : b ∈ S)
    (hab : a < b) : f b - f a < 0 := by
  have := hf ha hb hab
  linarith

/-- A8: at the deep balance (R = (4/3) r_M / A^2, sigma^2 = A v_f^2 / 2, v_f^2 r_M = G M) the Jeans log-slope of the
envelope's pressure at the wall is -G M / (sigma^2 R) = -(3/2) A. -/
theorem jeans_wall_slope (G M rM vf2 A s2 R : ℝ) (_hG : 0 < G) (hrM : 0 < rM) (hv : 0 < vf2) (hA : 0 < A)
    (hvr : vf2 * rM = G * M) (hR : R = 4 / 3 * rM / A ^ 2) (hs : s2 = A * vf2 / 2) :
    G * M / (s2 * R) = 3 / 2 * A := by
  rw [← hvr, hR, hs]
  field_simp
  ring

/-- A8: the deep balance is stable (A7 with n = (3/2) A against 2) iff A < 4/3. -/
theorem deep_stable_iff (A : ℝ) : 3 / 2 * A < 2 ↔ A < 4 / 3 := by
  constructor <;> intro h <;> linarith

end HE1

#print axioms HE1.hasDerivAt_W
#print axioms HE1.W_le_deep
#print axioms HE1.W_upper
#print axioms HE1.deep_balance
#print axioms HE1.amplitude_form
#print axioms HE1.sis_mass
#print axioms HE1.hasDerivAt_Dlow
#print axioms HE1.W_lower3
#print axioms HE1.dW_dy
#print axioms HE1.slope_identity
#print axioms HE1.slope_bracket
#print axioms HE1.W_le_deep_q
#print axioms HE1.cubic_mono
#print axioms HE1.W_lower_q
#print axioms HE1.exact_vs_deep
#print axioms HE1.stable_frozen
#print axioms HE1.deep_sis_stable
#print axioms HE1.swept_restoring
#print axioms HE1.jeans_wall_slope
#print axioms HE1.deep_stable_iff
-- kappa = 1/2 FITTED; not theory closed. Adopts nothing.
