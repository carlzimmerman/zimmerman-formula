/-
SWT1 (criteria 4d86f4d107, amendment A1 4af87eb9c0): Lean statements for the switch theorems. They certify the algebra and the
inequalities, not the physics. TEST lane; adopts nothing. kappa = 1/2 FITTED; not theory closed.

The law: mu(u) = u / (1 + u), nu(y) = 1/2 + sqrt(1/4 + 1/y). A switch S in [0, 1] multiplies the law's Lagrangian J.
  T1  exterior_mass, interior_mass, layer_mass : a spherical switched law shows only its baryons outside the switch radius;
                                                 inside it shows M_b nu(y); the surface layer carries -M_b (nu - 1).
      nu_gt_one                                : the retained phantom is positive.
  law_solves, nu_mu_inverse                    : u = nu(y) y solves mu(u) u = y, and conversely (the source of a given total).
  T3  wall_identity                            : the Legendre combination at fixed displacement equals
                                                 W(u) = u - ln(1 + u) - u^2 / (2 (1 + u)^2), u the law's field inside the wall.
      hasDerivAt_W, dW_eq                      : W' = u^2 (2 + u) / (1 + u)^3 = (u - y) dy/du, so W(y) = integral (nu - 1) y dy.
      W_nonneg, W_le_y                         : 0 <= W <= y.
      W_le_deep                                : W <= (2/3) y^(3/2), stated in t = sqrt(1 + u) (y^(3/2) = (t^2 - 1)^3 / t^3).
  T2  alpha_ge, alpha_lt_one                   : the polarizability of an inclusion lies in [-1/2, 1).
      qC_bound, filling_line                   : q_C <= (3/2) f / (1 - f), and the line q_C <= q is met iff f <= q / (3/2 + q).
  T4  crossover, mu_crossover                  : nu(y) = 1 + R iff y = 1 / (R (R + 1)); mu(g / a0) = 1 / (1 + R) iff g = a0 / R.
-/
import Mathlib

namespace SWT1

noncomputable def nu (y : ℝ) : ℝ := 1 / 2 + Real.sqrt (1 / 4 + 1 / y)
noncomputable def mu (u : ℝ) : ℝ := u / (1 + u)
noncomputable def W (u : ℝ) : ℝ := u - Real.log (1 + u) - u ^ 2 / (2 * (1 + u) ^ 2)

/-! ### T1: compensation -/

noncomputable def gN (G Mb r : ℝ) : ℝ := G * Mb / r ^ 2
/-- the spherical switched law: the law inside R, Newton outside. -/
noncomputable def gS (G Mb a0 R r : ℝ) : ℝ :=
  if r < R then nu (gN G Mb r / a0) * gN G Mb r else gN G Mb r
/-- effective enclosed mass r^2 g / G. -/
noncomputable def Meff (G Mb a0 R r : ℝ) : ℝ := r ^ 2 * gS G Mb a0 R r / G

theorem exterior_mass (G Mb a0 R r : ℝ) (hG : 0 < G) (hr : 0 < r) (hRr : R ≤ r) :
    Meff G Mb a0 R r = Mb := by
  unfold Meff gS gN
  simp only [not_lt.mpr hRr, ite_false]
  field_simp

theorem interior_mass (G Mb a0 R r : ℝ) (hG : 0 < G) (hr : 0 < r) (hrR : r < R) :
    Meff G Mb a0 R r = Mb * nu (G * Mb / r ^ 2 / a0) := by
  unfold Meff gS gN
  simp only [hrR, ite_true]
  field_simp

theorem nu_gt_one (y : ℝ) (hy : 0 < y) : 1 < nu y := by
  unfold nu
  have h1 : (1 / 2 : ℝ) = Real.sqrt (1 / 4) := by
    rw [show (1 / 4 : ℝ) = (1 / 2) ^ 2 by norm_num, Real.sqrt_sq (by norm_num)]
  have h2 : Real.sqrt (1 / 4) < Real.sqrt (1 / 4 + 1 / y) := by
    apply Real.sqrt_lt_sqrt (by norm_num)
    have : 0 < 1 / y := by positivity
    linarith
  linarith

/-- the layer at the switch surface: exterior minus interior effective mass is -M_b (nu - 1), negative for M_b > 0. -/
theorem layer_mass (G Mb a0 R r₁ r₂ : ℝ) (hG : 0 < G) (h1 : 0 < r₁) (h1R : r₁ < R) (hR2 : R ≤ r₂) :
    Meff G Mb a0 R r₂ - Meff G Mb a0 R r₁ = -(Mb * (nu (G * Mb / r₁ ^ 2 / a0) - 1)) := by
  rw [exterior_mass G Mb a0 R r₂ hG (lt_of_lt_of_le (lt_trans h1 h1R) hR2) hR2,
    interior_mass G Mb a0 R r₁ hG h1 h1R]
  ring

/-! ### the law and its inverse -/

theorem law_solves (y : ℝ) (hy : 0 < y) : mu (nu y * y) * (nu y * y) = y := by
  have hs : (0 : ℝ) ≤ 1 / 4 + 1 / y := by positivity
  have hsq : Real.sqrt (1 / 4 + 1 / y) ^ 2 = 1 / 4 + 1 / y := Real.sq_sqrt hs
  have hs0 : 0 ≤ Real.sqrt (1 / 4 + 1 / y) := Real.sqrt_nonneg _
  unfold nu mu
  set s := Real.sqrt (1 / 4 + 1 / y) with hsdef
  have hpos : 0 < 1 + (1 / 2 + s) * y := by positivity
  have hsy : s ^ 2 * y = y / 4 + 1 := by
    rw [hsq]; field_simp
  rw [div_mul_eq_mul_div, div_eq_iff hpos.ne']
  linear_combination y * hsy

/-- conversely: the source that the law turns into a total field u is mu(u) u. -/
theorem nu_mu_inverse (u : ℝ) (hu : 0 < u) : nu (mu u * u) * (mu u * u) = u := by
  unfold nu mu
  have h1 : 0 < 1 + u := by linarith
  have hsq : (1 : ℝ) / 4 + 1 / (u / (1 + u) * u) = ((u + 2) / (2 * u)) ^ 2 := by
    field_simp
    ring
  rw [hsq, Real.sqrt_sq (by positivity)]
  field_simp
  ring

/-! ### T3: wall pressure -/

/-- the Legendre combination at fixed displacement y = u^2 / (1 + u) is W. -/
theorem wall_identity (u : ℝ) (hu : 0 ≤ u) :
    (u - Real.log (1 + u)) - u ^ 2 / 2 + (u ^ 2 / (1 + u)) * u - (u ^ 2 / (1 + u)) ^ 2 / 2 = W u := by
  unfold W
  have h : (1 + u) ≠ 0 := by positivity
  field_simp
  ring

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

/-- W' du = (u - y) dy with y = u^2 / (1 + u): W is the integral of the phantom field over the displacement. -/
theorem dW_eq (u : ℝ) (hu : -1 < u) :
    u ^ 2 * (2 + u) / (1 + u) ^ 3 = (u - u ^ 2 / (1 + u)) * (u * (2 + u) / (1 + u) ^ 2) := by
  have hp : (1 + u) ≠ 0 := by linarith
  field_simp
  ring

theorem hasDerivAt_y (u : ℝ) (hu : -1 < u) :
    HasDerivAt (fun v : ℝ => v ^ 2 / (1 + v)) (u * (2 + u) / (1 + u) ^ 2) u := by
  have hp : (1 + u) ≠ 0 := by linarith
  have h1 : HasDerivAt (fun v : ℝ => 1 + v) 1 u := by
    simpa using (hasDerivAt_id u).const_add 1
  have hn : HasDerivAt (fun v : ℝ => v ^ 2) (2 * u) u := by
    simpa using hasDerivAt_pow 2 u
  have hq : HasDerivAt (fun v : ℝ => v ^ 2 / (1 + v)) ((2 * u * (1 + u) - u ^ 2 * 1) / (1 + u) ^ 2) u := hn.div h1 hp
  have hderiv : (2 * u * (1 + u) - u ^ 2 * 1) / (1 + u) ^ 2 = u * (2 + u) / (1 + u) ^ 2 := by
    field_simp
    ring
  exact hq.congr_deriv hderiv

theorem W_nonneg (u : ℝ) (hu : 0 ≤ u) : 0 ≤ W u := by
  have hmono : MonotoneOn W (Set.Ici 0) := by
    apply monotoneOn_of_deriv_nonneg (convex_Ici 0)
    · intro x hx
      have hx0 : (0 : ℝ) ≤ x := hx
      exact (hasDerivAt_W x (by linarith)).continuousAt.continuousWithinAt
    · intro x hx
      rw [interior_Ici] at hx
      have hx0 : (0 : ℝ) < x := hx
      exact (hasDerivAt_W x (by linarith)).differentiableAt.differentiableWithinAt
    · intro x hx
      rw [interior_Ici] at hx
      have hx0 : (0 : ℝ) < x := hx
      rw [(hasDerivAt_W x (by linarith)).deriv]
      positivity
  have h0 : W 0 = 0 := by simp [W]
  have := hmono (Set.mem_Ici.mpr le_rfl) (Set.mem_Ici.mpr hu) hu
  linarith

/-- W <= y: the wall pressure never exceeds the Newtonian-regime value a0 g_N / (4 pi G). -/
theorem W_le_y (u : ℝ) (hu : 0 ≤ u) : W u ≤ u ^ 2 / (1 + u) := by
  unfold W
  have hp : 0 < 1 + u := by linarith
  have hlog : 1 - (1 + u)⁻¹ ≤ Real.log (1 + u) := Real.one_sub_inv_le_log_of_pos hp
  have h2 : 0 ≤ u ^ 2 / (2 * (1 + u) ^ 2) := by positivity
  have h3 : u - (1 - (1 + u)⁻¹) = u ^ 2 / (1 + u) := by
    field_simp
    ring
  linarith

/-- the deep-regime bound in t = sqrt(1 + u) >= 1, where y^(3/2) = (t^2 - 1)^3 / t^3. -/
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

/-- W(u) <= (2/3) y^(3/2) with u = t^2 - 1, y = (t^2 - 1)^2 / t^2, y^(3/2) = (t^2 - 1)^3 / t^3, for t >= 1. -/
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

/-! ### T2: the compensated statistic -/

theorem alpha_ge (Λ : ℝ) (hΛ : 0 ≤ Λ) : -(1 / 2 : ℝ) ≤ (Λ - 1) / (Λ + 2) := by
  have h : 0 < Λ + 2 := by linarith
  rw [le_div_iff₀ h]
  linarith

theorem alpha_lt_one (Λ : ℝ) (hΛ : 0 ≤ Λ) : (Λ - 1) / (Λ + 2) < 1 := by
  have h : 0 < Λ + 2 := by linarith
  rw [div_lt_one h]
  linarith

/-- Maxwell-Garnett with beta no lower than the insulating limit -f/2: the statistic is at most (3/2) f / (1 - f). -/
theorem qC_bound (f β : ℝ) (hf1 : f < 1) (hβ : -(f / 2) ≤ β) :
    (1 - β) / (1 + 2 * β) - 1 ≤ 3 / 2 * f / (1 - f) := by
  have h1 : 0 < 1 + 2 * β := by linarith
  have h2 : 0 < 1 - f := by linarith
  have h1' : (1 + 2 * β) ≠ 0 := h1.ne'
  have key : (1 - β) / (1 + 2 * β) - 1 = (1 - β - (1 + 2 * β)) / (1 + 2 * β) := by
    have h := div_mul_cancel₀ (1 - β) h1'
    rw [eq_div_iff h1']
    linear_combination h
  rw [key, div_le_div_iff₀ h1 h2]
  nlinarith

theorem filling_line (f q : ℝ) (hf1 : f < 1) (hq : 0 < q) :
    3 / 2 * f / (1 - f) ≤ q ↔ f ≤ q / (3 / 2 + q) := by
  have h2 : 0 < 1 - f := by linarith
  have h3 : 0 < 3 / 2 + q := by linarith
  rw [div_le_iff₀ h2, le_div_iff₀ h3]
  constructor <;> intro h <;> nlinarith

/-! ### T4: crossover -/

theorem crossover (y R : ℝ) (hy : 0 < y) (hR : 0 < R) : nu y = 1 + R ↔ y = 1 / (R * (R + 1)) := by
  unfold nu
  have h0 : (0 : ℝ) ≤ 1 / 4 + 1 / y := by positivity
  have h1 : (0 : ℝ) ≤ 1 / 2 + R := by linarith
  have hRR : 0 < R * (R + 1) := by positivity
  constructor
  · intro h
    have hs : Real.sqrt (1 / 4 + 1 / y) = 1 / 2 + R := by linarith
    have h2 := (Real.sqrt_eq_iff_mul_self_eq h0 h1).mp hs
    have hy' : 1 / y = R * (R + 1) := by nlinarith
    rw [eq_div_iff hRR.ne', ← hy']
    field_simp
  · intro h
    have hs : Real.sqrt (1 / 4 + 1 / y) = 1 / 2 + R := by
      rw [Real.sqrt_eq_iff_mul_self_eq h0 h1, h]
      field_simp
      ring
    linarith

theorem mu_crossover (g a0 R : ℝ) (hg : 0 < g) (ha : 0 < a0) (hR : 0 < R) :
    mu (g / a0) = 1 / (1 + R) ↔ g = a0 / R := by
  unfold mu
  have h1 : 0 < 1 + g / a0 := by positivity
  have h2 : 0 < 1 + R := by linarith
  rw [div_eq_div_iff h1.ne' h2.ne', eq_div_iff hR.ne']
  constructor
  · intro h
    have h3 : g / a0 * R = 1 := by nlinarith
    have h4 : g / a0 * R = g * R / a0 := by ring
    rw [h4, div_eq_one_iff_eq ha.ne'] at h3
    exact h3
  · intro h
    have h4 : g / a0 * R = 1 := by
      rw [show g / a0 * R = g * R / a0 by ring, h]
      field_simp
    nlinarith

end SWT1

#print axioms SWT1.exterior_mass
#print axioms SWT1.interior_mass
#print axioms SWT1.layer_mass
#print axioms SWT1.nu_gt_one
#print axioms SWT1.law_solves
#print axioms SWT1.nu_mu_inverse
#print axioms SWT1.wall_identity
#print axioms SWT1.hasDerivAt_W
#print axioms SWT1.dW_eq
#print axioms SWT1.hasDerivAt_y
#print axioms SWT1.W_nonneg
#print axioms SWT1.W_le_y
#print axioms SWT1.W_le_deep
#print axioms SWT1.alpha_ge
#print axioms SWT1.alpha_lt_one
#print axioms SWT1.qC_bound
#print axioms SWT1.filling_line
#print axioms SWT1.crossover
#print axioms SWT1.mu_crossover
