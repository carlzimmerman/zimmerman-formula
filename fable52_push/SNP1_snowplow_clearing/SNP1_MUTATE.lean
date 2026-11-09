/-
SNP1 MUTATE twin (criteria 9ff5f59a72): the true SNP1.lean statements (namespace SNP1M) followed by six false versions, each
carrying the proof that closes its true counterpart. This file must FAIL to compile, with errors only in the false versions.
  W_lower_M        : W < u^3 / (2 (1 + u)^2)           (lower bound reversed)
  Fw_le_M          : F_w <= a0 M_b / 2
  Psi_strictMono_M : Psi increasing (a fixed-mass shell stable)
  eq_bracket_M     : the equilibrium below u = 1 / (2k)
  sticky_merge_M   : a sticky merge gains (1/2) M m (V - v)^2 / (M + m)
  deep_eq_M        : deep equilibrium at R_eq = k r_M instead of (3/2) k r_M
kappa = 1/2 FITTED; not theory closed. Adopts nothing.
-/
import Mathlib

namespace SNP1M

noncomputable def W (u : ℝ) : ℝ := u - Real.log (1 + u) - u ^ 2 / (2 * (1 + u) ^ 2)
noncomputable def Phi (u : ℝ) : ℝ := W u * (1 + u) / u ^ 2
noncomputable def Psi (u : ℝ) : ℝ := W u * (1 + u) ^ 2 / u ^ 4
noncomputable def uin (y : ℝ) : ℝ := y / 2 + Real.sqrt (y ^ 2 / 4 + y)

/-! ### copied from SWT1.lean -/

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

theorem W_le_y (u : ℝ) (hu : 0 ≤ u) : W u ≤ u ^ 2 / (1 + u) := by
  unfold W
  have hp : 0 < 1 + u := by linarith
  have hlog : 1 - (1 + u)⁻¹ ≤ Real.log (1 + u) := Real.one_sub_inv_le_log_of_pos hp
  have h2 : 0 ≤ u ^ 2 / (2 * (1 + u) ^ 2) := by positivity
  have h3 : u - (1 - (1 + u)⁻¹) = u ^ 2 / (1 + u) := by
    field_simp
    ring
  linarith

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

/-! ### A1: the force on the carrier is bounded -/

/-- A1a: F_w <= a0 M_b. -/
theorem Fw_le (u : ℝ) (hu : 0 < u) : Phi u ≤ 1 := by
  unfold Phi
  have h := W_le_y u hu.le
  have h1 : 0 < 1 + u := by linarith
  have h2 : 0 < u ^ 2 := by positivity
  rw [div_le_one h2]
  have h3 := mul_le_mul_of_nonneg_right h h1.le
  have e : u ^ 2 / (1 + u) * (1 + u) = u ^ 2 := by field_simp
  linarith

/-- A1b: F_w <= (2/3) a0 M_b sqrt(y), with u = t^2 - 1, y = (t^2 - 1)^2 / t^2, sqrt(y) = (t^2 - 1) / t. -/
theorem Fw_le_deep (t : ℝ) (ht : 1 < t) :
    W (t ^ 2 - 1) * t ^ 2 / (t ^ 2 - 1) ^ 2 ≤ 2 / 3 * (t ^ 2 - 1) / t := by
  have h := W_le_deep t ht.le
  have ht0 : 0 < t := by linarith
  have hb : 0 < t ^ 2 - 1 := by nlinarith
  have h3 : (0 : ℝ) < t ^ 3 := by positivity
  have key : W (t ^ 2 - 1) * t ^ 3 ≤ 2 / 3 * (t ^ 2 - 1) ^ 3 := by
    have hm := mul_le_mul_of_nonneg_right h h3.le
    have e : 2 / 3 * (t ^ 2 - 1) ^ 3 / t ^ 3 * t ^ 3 = 2 / 3 * (t ^ 2 - 1) ^ 3 := by field_simp
    linarith
  rw [div_le_div_iff₀ (by positivity) ht0]
  calc W (t ^ 2 - 1) * t ^ 2 * t = W (t ^ 2 - 1) * t ^ 3 := by ring
    _ ≤ 2 / 3 * (t ^ 2 - 1) ^ 3 := key
    _ = 2 / 3 * (t ^ 2 - 1) * (t ^ 2 - 1) ^ 2 := by ring

theorem hasDerivAt_Elow (u : ℝ) (hu : -1 < u) :
    HasDerivAt (fun v : ℝ => W v - v ^ 3 / (2 * (1 + v) ^ 2)) (u ^ 2 / (2 * (1 + u) ^ 2)) u := by
  have hp : (1 + u) ≠ 0 := by linarith
  have h1 : HasDerivAt (fun v : ℝ => 1 + v) 1 u := by
    simpa using (hasDerivAt_id u).const_add 1
  have hn : HasDerivAt (fun v : ℝ => v ^ 3) (3 * u ^ 2) u := by
    simpa using hasDerivAt_pow 3 u
  have hd : HasDerivAt (fun v : ℝ => 2 * (1 + v) ^ 2) (2 * (2 * (1 + u) * 1)) u := by
    have := (h1.pow 2).const_mul 2
    simpa using this
  have hne : (2 * (1 + u) ^ 2) ≠ 0 := by positivity
  have hq : HasDerivAt (fun v : ℝ => v ^ 3 / (2 * (1 + v) ^ 2))
      ((3 * u ^ 2 * (2 * (1 + u) ^ 2) - u ^ 3 * (2 * (2 * (1 + u) * 1))) / (2 * (1 + u) ^ 2) ^ 2) u := hn.div hd hne
  have hall : HasDerivAt (fun v : ℝ => W v - v ^ 3 / (2 * (1 + v) ^ 2))
      (u ^ 2 * (2 + u) / (1 + u) ^ 3 - (3 * u ^ 2 * (2 * (1 + u) ^ 2) - u ^ 3 * (2 * (2 * (1 + u) * 1))) / (2 * (1 + u) ^ 2) ^ 2) u :=
    (hasDerivAt_W u hu).sub hq
  refine hall.congr_deriv ?_
  field_simp
  ring

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

/-- A1c, lower: W > u^3 / (2 (1 + u)^2) for u > 0. -/
theorem W_lower (u : ℝ) (hu : 0 < u) : u ^ 3 / (2 * (1 + u) ^ 2) < W u := by
  have hmono : StrictMonoOn (fun v : ℝ => W v - v ^ 3 / (2 * (1 + v) ^ 2)) (Set.Ici 0) := by
    apply strictMonoOn_of_deriv_pos (convex_Ici 0)
    · intro x hx
      have hx0 : (0 : ℝ) ≤ x := hx
      exact (hasDerivAt_Elow x (by linarith)).continuousAt.continuousWithinAt
    · intro x hx
      rw [interior_Ici] at hx
      have hx0 : (0 : ℝ) < x := hx
      rw [(hasDerivAt_Elow x (by linarith)).deriv]
      positivity
  have h0 : W 0 - (0 : ℝ) ^ 3 / (2 * (1 + 0) ^ 2) = 0 := by simp [W]
  have := hmono (Set.mem_Ici.mpr le_rfl) (Set.mem_Ici.mpr hu.le) hu
  dsimp only at this
  linarith

/-- A1c, upper: W < u^3 / (1 + u)^2 for u > 0. -/
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

/-- A1c: (1/2) mu < F_w / (a0 M_b) < mu, mu = u / (1 + u). -/
theorem Fw_mu_bracket (u : ℝ) (hu : 0 < u) : u / (1 + u) / 2 < Phi u ∧ Phi u < u / (1 + u) := by
  have hlow := W_lower u hu
  have hup := W_upper u hu
  have hp : 0 < 1 + u := by linarith
  have hu2 : 0 < u ^ 2 := by positivity
  unfold Phi
  constructor
  · rw [lt_div_iff₀ hu2]
    have e : u / (1 + u) / 2 * u ^ 2 = u ^ 3 / (2 * (1 + u) ^ 2) * (1 + u) := by
      field_simp
    rw [e]
    exact mul_lt_mul_of_pos_right hlow hp
  · rw [div_lt_iff₀ hu2]
    have e : u / (1 + u) * u ^ 2 = u ^ 3 / (1 + u) ^ 2 * (1 + u) := by
      field_simp
    rw [e]
    exact mul_lt_mul_of_pos_right hup hp

/-- A1d: a shell whose weight (in a0 M_b) exceeds 1 feels a net inward force, whatever the baryons do. -/
theorem no_support (u wt : ℝ) (hu : 0 < u) (hw : 1 < wt) : Phi u - wt < 0 := by
  have := Fw_le u hu
  linarith

/-! ### A2: a settled shell of fixed mass -/

theorem hasDerivAt_Psi (u : ℝ) (hu : 0 < u) :
    HasDerivAt Psi (2 * (1 + u) * (2 + u) / u ^ 5 * (u ^ 3 / (2 * (1 + u) ^ 2) - W u)) u := by
  have hu1 : -1 < u := by linarith
  have hp : (1 + u) ≠ 0 := by linarith
  have hu0 : u ≠ 0 := hu.ne'
  have h1 : HasDerivAt (fun v : ℝ => 1 + v) 1 u := by
    simpa using (hasDerivAt_id u).const_add 1
  have hsq : HasDerivAt (fun v : ℝ => (1 + v) ^ 2) (2 * (1 + u)) u := by
    have h' : HasDerivAt (fun v : ℝ => (1 + v) ^ 2) (((2 : ℕ) : ℝ) * (1 + u) ^ (2 - 1) * 1) u := h1.pow 2
    convert h' using 1
    norm_num
  have h4 : HasDerivAt (fun v : ℝ => v ^ 4) (4 * u ^ 3) u := by
    simpa using hasDerivAt_pow 4 u
  have hnum : HasDerivAt (fun v : ℝ => W v * (1 + v) ^ 2)
      (u ^ 2 * (2 + u) / (1 + u) ^ 3 * (1 + u) ^ 2 + W u * (2 * (1 + u))) u := (hasDerivAt_W u hu1).mul hsq
  have hq : HasDerivAt (fun v : ℝ => W v * (1 + v) ^ 2 / v ^ 4)
      (((u ^ 2 * (2 + u) / (1 + u) ^ 3 * (1 + u) ^ 2 + W u * (2 * (1 + u))) * u ^ 4 - W u * (1 + u) ^ 2 * (4 * u ^ 3))
        / (u ^ 4) ^ 2) u := hnum.div h4 (pow_ne_zero 4 hu0)
  have hfun : Psi = fun v : ℝ => W v * (1 + v) ^ 2 / v ^ 4 := by
    funext v; rfl
  rw [hfun]
  refine hq.congr_deriv ?_
  field_simp
  ring

/-- A2a: Psi = W / y^2 is strictly decreasing in u, i.e. strictly increasing in R. -/
theorem Psi_strictAnti : StrictAntiOn Psi (Set.Ioi 0) := by
  apply strictAntiOn_of_deriv_neg (convex_Ioi 0)
  · intro x hx
    have hx0 : (0 : ℝ) < x := hx
    exact (hasDerivAt_Psi x hx0).continuousAt.continuousWithinAt
  · intro x hx
    rw [interior_Ioi] at hx
    have hx0 : (0 : ℝ) < x := hx
    rw [(hasDerivAt_Psi x hx0).deriv]
    have hlow := W_lower x hx0
    have hA : 0 < 2 * (1 + x) * (2 + x) / x ^ 5 := by positivity
    have hB : x ^ 3 / (2 * (1 + x) ^ 2) - W x < 0 := by linarith
    exact mul_neg_of_pos_of_neg hA hB

/-- A2b: the equilibrium Psi u = k lies in 1 / (2k) < u < 1 / k. -/
theorem eq_bracket (u k : ℝ) (hu : 0 < u) (hk : 0 < k) (h : Psi u = k) : 1 < 2 * k * u ∧ k * u < 1 := by
  have hlow := W_lower u hu
  have hup := W_upper u hu
  have hp : 0 < 1 + u := by linarith
  have hu4 : 0 < u ^ 4 := by positivity
  have hu3 : 0 < u ^ 3 := by positivity
  have hP : W u * (1 + u) ^ 2 = k * u ^ 4 := by
    unfold Psi at h
    rw [div_eq_iff hu4.ne'] at h
    exact h
  have hd : 0 < 2 * (1 + u) ^ 2 := by positivity
  have hd2 : 0 < (1 + u) ^ 2 := by positivity
  have hl : u ^ 3 < W u * (2 * (1 + u) ^ 2) := (div_lt_iff₀ hd).mp hlow
  have hh : W u * (1 + u) ^ 2 < u ^ 3 := (lt_div_iff₀ hd2).mp hup
  constructor
  · have e1 : W u * (2 * (1 + u) ^ 2) = 2 * (k * u ^ 4) := by
      rw [← hP]; ring
    have h3 : u ^ 3 < 2 * (k * u ^ 4) := by linarith
    by_contra hc
    push Not at hc
    have h5 : u ^ 3 * (2 * k * u) ≤ u ^ 3 * 1 := mul_le_mul_of_nonneg_left hc hu3.le
    have e : u ^ 3 * (2 * k * u) = 2 * (k * u ^ 4) := by ring
    linarith
  · have h3 : k * u ^ 4 < u ^ 3 := by linarith
    by_contra hc
    push Not at hc
    have h5 : u ^ 3 * 1 ≤ u ^ 3 * (k * u) := mul_le_mul_of_nonneg_left hc hu3.le
    have e : u ^ 3 * (k * u) = k * u ^ 4 := by ring
    linarith

/-- (R / r_M)^2 = (1 + u) / u^2 is strictly decreasing in u: larger u is a smaller radius. -/
theorem radius_decreasing (u1 u2 : ℝ) (h1 : 0 < u1) (h12 : u1 < u2) :
    (1 + u2) / u2 ^ 2 < (1 + u1) / u1 ^ 2 := by
  have h2 : 0 < u2 := by linarith
  rw [div_lt_div_iff₀ (by positivity) (by positivity)]
  nlinarith [mul_pos (sub_pos.mpr h12) (by positivity : (0 : ℝ) < u1 + u2 + u1 * u2)]

/-- A2b: k (k + 1) < (R_eq / r_M)^2 < 2k (2k + 1). -/
theorem R_bracket (u k : ℝ) (hu : 0 < u) (hk : 0 < k) (h1 : 1 < 2 * k * u) (h2 : k * u < 1) :
    k * (k + 1) < (1 + u) / u ^ 2 ∧ (1 + u) / u ^ 2 < 2 * k * (2 * k + 1) := by
  have hu2 : 0 < u ^ 2 := by positivity
  have hku : 0 < k * u := mul_pos hk hu
  constructor
  · rw [lt_div_iff₀ hu2]
    nlinarith [mul_pos (sub_pos.mpr h2) (by positivity : (0 : ℝ) < 1 + k * u), mul_pos (sub_pos.mpr h2) hu]
  · rw [div_lt_iff₀ hu2]
    nlinarith [mul_pos (sub_pos.mpr h1) (by positivity : (0 : ℝ) < 2 * k * u + 1), mul_pos (sub_pos.mpr h1) hu]

/-- A2c: the equilibrium is unstable. Net outward force (units a0 M_b) y (Psi u - k), y = u^2 / (1 + u):
positive outside R_eq (u < u_eq: the shell is expelled), negative inside (u > u_eq: it falls). -/
theorem unstable (k ue u : ℝ) (hue : 0 < ue) (hu : 0 < u) (heq : Psi ue = k) :
    (u < ue → 0 < u ^ 2 / (1 + u) * (Psi u - k)) ∧ (ue < u → u ^ 2 / (1 + u) * (Psi u - k) < 0) := by
  have hy : 0 < u ^ 2 / (1 + u) := by positivity
  constructor
  · intro hlt
    have hA := Psi_strictAnti (Set.mem_Ioi.mpr hu) (Set.mem_Ioi.mpr hue) hlt
    have hpos : 0 < Psi u - k := by linarith
    exact mul_pos hy hpos
  · intro hlt
    have hA := Psi_strictAnti (Set.mem_Ioi.mpr hue) (Set.mem_Ioi.mpr hu) hlt
    have hneg : Psi u - k < 0 := by linarith
    exact mul_neg_of_pos_of_neg hy hneg

/-- A2d: deep closed form. With F = (2/3) sqrt(y) and weight k y (s = sqrt y), equilibrium iff R_eq / r_M = 1 / s = (3/2) k. -/
theorem deep_eq (s k : ℝ) (hs : 0 < s) (hk : 0 < k) : 2 / 3 * s = k * s ^ 2 ↔ 1 / s = 3 / 2 * k := by
  constructor
  · intro h
    have h2 : s * (k * s) = s * (2 / 3) := by linear_combination -h
    have h1 : k * s = 2 / 3 := mul_left_cancel₀ hs.ne' h2
    rw [div_eq_iff hs.ne']
    linear_combination (-3 / 2 : ℝ) * h1
  · intro h
    rw [div_eq_iff hs.ne'] at h
    linear_combination (2 / 3 * s) * h

/-! ### A3: a shell that sweeps up the mean background -/

theorem hasDerivAt_Phi (u : ℝ) (hu : 0 < u) :
    HasDerivAt Phi ((2 + u) / u ^ 3 * (u ^ 3 / (1 + u) ^ 2 - W u)) u := by
  have hu1 : -1 < u := by linarith
  have hp : (1 + u) ≠ 0 := by linarith
  have hu0 : u ≠ 0 := hu.ne'
  have h1 : HasDerivAt (fun v : ℝ => 1 + v) 1 u := by
    simpa using (hasDerivAt_id u).const_add 1
  have h2 : HasDerivAt (fun v : ℝ => v ^ 2) (2 * u) u := by
    simpa using hasDerivAt_pow 2 u
  have hnum : HasDerivAt (fun v : ℝ => W v * (1 + v))
      (u ^ 2 * (2 + u) / (1 + u) ^ 3 * (1 + u) + W u * 1) u := (hasDerivAt_W u hu1).mul h1
  have hq : HasDerivAt (fun v : ℝ => W v * (1 + v) / v ^ 2)
      (((u ^ 2 * (2 + u) / (1 + u) ^ 3 * (1 + u) + W u * 1) * u ^ 2 - W u * (1 + u) * (2 * u)) / (u ^ 2) ^ 2) u :=
    hnum.div h2 (pow_ne_zero 2 hu0)
  have hfun : Phi = fun v : ℝ => W v * (1 + v) / v ^ 2 := by
    funext v; rfl
  rw [hfun]
  refine hq.congr_deriv ?_
  field_simp
  ring

/-- A3a: F_w / (a0 M_b) = Phi(u) is strictly increasing in u. -/
theorem Phi_strictMono : StrictMonoOn Phi (Set.Ioi 0) := by
  apply strictMonoOn_of_deriv_pos (convex_Ioi 0)
  · intro x hx
    have hx0 : (0 : ℝ) < x := hx
    exact (hasDerivAt_Phi x hx0).continuousAt.continuousWithinAt
  · intro x hx
    rw [interior_Ioi] at hx
    have hx0 : (0 : ℝ) < x := hx
    rw [(hasDerivAt_Phi x hx0).deriv]
    have hup := W_upper x hx0
    have hA : 0 < (2 + x) / x ^ 3 := by positivity
    have hB : 0 < x ^ 3 / (1 + x) ^ 2 - W x := by linarith
    exact mul_pos hA hB

theorem uin_pos (y : ℝ) (hy : 0 < y) : 0 < uin y := by
  unfold uin
  positivity

theorem uin_strictMono (y1 y2 : ℝ) (h0 : 0 ≤ y1) (h : y1 < y2) : uin y1 < uin y2 := by
  unfold uin
  have hs : Real.sqrt (y1 ^ 2 / 4 + y1) ≤ Real.sqrt (y2 ^ 2 / 4 + y2) := Real.sqrt_le_sqrt (by nlinarith)
  linarith

/-- A3a: F_w strictly decreases with R (y = c / R^2, c = G M_b / a0). -/
theorem Fw_decreasing (c R1 R2 : ℝ) (hc : 0 < c) (h1 : 0 < R1) (h12 : R1 < R2) :
    Phi (uin (c / R2 ^ 2)) < Phi (uin (c / R1 ^ 2)) := by
  have h2 : 0 < R2 := by linarith
  have hy2 : 0 < c / R2 ^ 2 := by positivity
  have hy1 : 0 < c / R1 ^ 2 := by positivity
  have hlt : c / R2 ^ 2 < c / R1 ^ 2 := by
    rw [div_lt_div_iff₀ (by positivity) (by positivity)]
    have hsq : R1 * R1 < R2 * R2 := mul_self_lt_mul_self h1.le h12
    nlinarith
  exact Phi_strictMono (Set.mem_Ioi.mpr (uin_pos _ hy2)) (Set.mem_Ioi.mpr (uin_pos _ hy1)) (uin_strictMono _ _ hy2.le hlt)

/-- A3b: the swept weight R (M + c R^3) is strictly increasing (M = M_b > 0, c = (2 pi / 3) rho >= 0, up to G (4 pi / 3) rho). -/
theorem weight_strictMono (M c R1 R2 : ℝ) (hM : 0 < M) (hc : 0 ≤ c) (h1 : 0 < R1) (h12 : R1 < R2) :
    R1 * (M + c * R1 ^ 3) < R2 * (M + c * R2 ^ 3) := by
  have hsq : R1 * R1 < R2 * R2 := mul_self_lt_mul_self h1.le h12
  have h4 : (R1 * R1) * (R1 * R1) < (R2 * R2) * (R2 * R2) := mul_self_lt_mul_self (by positivity) hsq
  have e1 : R1 * (M + c * R1 ^ 3) = M * R1 + c * ((R1 * R1) * (R1 * R1)) := by ring
  have e2 : R2 * (M + c * R2 ^ 3) = M * R2 + c * ((R2 * R2) * (R2 * R2)) := by ring
  rw [e1, e2]
  have h5 := mul_le_mul_of_nonneg_left h4.le hc
  have h6 : M * R1 < M * R2 := mul_lt_mul_of_pos_left h12 hM
  linarith

/-- A3b: a strictly decreasing force meeting a strictly increasing weight at R*: net outward inside, inward outside. -/
theorem balance_stable (f g : ℝ → ℝ) (S : Set ℝ) (hf : StrictAntiOn f S) (hg : StrictMonoOn g S) (Rs R : ℝ)
    (hRs : Rs ∈ S) (hR : R ∈ S) (heq : f Rs = g Rs) :
    (R < Rs → g R < f R) ∧ (Rs < R → f R < g R) := by
  constructor
  · intro hlt
    have a1 := hf hR hRs hlt
    have a2 := hg hR hRs hlt
    linarith
  · intro hlt
    have a1 := hf hRs hR hlt
    have a2 := hg hRs hR hlt
    linarith

/-- A3c: M_s << M_b. R^2 (2 pi G rho) = v^2 balances (2/3) M v^2 / R against G (4 pi / 3) rho R M (multiplied by R). -/
theorem swept_small (G ρ M v R : ℝ) (h : R ^ 2 * (2 * Real.pi * G * ρ) = v ^ 2) :
    2 / 3 * M * v ^ 2 = G * (4 * Real.pi / 3) * ρ * R ^ 2 * M := by
  linear_combination (-(2 / 3) * M) * h

/-- A3c: M_s >> M_b. R^5 (4 pi^2 G rho^2) = 3 M v^2 balances (2/3) M v^2 / R against G M_s^2 / (2 R^2),
M_s = (4 pi / 3) rho R^3 (multiplied by R^2). -/
theorem swept_large (G ρ M v R : ℝ) (h : R ^ 5 * (4 * Real.pi ^ 2 * G * ρ ^ 2) = 3 * M * v ^ 2) :
    2 / 3 * M * v ^ 2 * R = G * (4 * Real.pi / 3 * ρ * R ^ 3) ^ 2 / 2 := by
  linear_combination (-(2 / 9) * R) * h

/-! ### B: the two sweeping rules -/

/-- B1: a sticky merge conserves momentum (V' = (M V + m v) / (M + m)) and loses (1/2) M m (V - v)^2 / (M + m). -/
theorem sticky_merge (M m V v : ℝ) (hM : 0 < M) (hm : 0 < m) :
    1 / 2 * M * V ^ 2 + 1 / 2 * m * v ^ 2 - 1 / 2 * (M + m) * ((M * V + m * v) / (M + m)) ^ 2
      = 1 / 2 * M * m * (V - v) ^ 2 / (M + m) := by
  have h : (M + m) ≠ 0 := by positivity
  field_simp
  ring

theorem sticky_loss_nonneg (M m V v : ℝ) (hM : 0 < M) (hm : 0 < m) : 0 ≤ 1 / 2 * M * m * (V - v) ^ 2 / (M + m) := by
  positivity

/-- B2: reflection off a wall moving at V (v' = 2V - v) keeps the speed in the wall's frame. -/
theorem reflect_speed (V v : ℝ) : ((2 * V - v) - V) ^ 2 = (v - V) ^ 2 := by
  ring


/-! ### MUTATE: false versions -/

theorem W_lower_M (u : ℝ) (hu : 0 < u) : W u < u ^ 3 / (2 * (1 + u) ^ 2) := by
  have hmono : StrictMonoOn (fun v : ℝ => W v - v ^ 3 / (2 * (1 + v) ^ 2)) (Set.Ici 0) := by
    apply strictMonoOn_of_deriv_pos (convex_Ici 0)
    · intro x hx
      have hx0 : (0 : ℝ) ≤ x := hx
      exact (hasDerivAt_Elow x (by linarith)).continuousAt.continuousWithinAt
    · intro x hx
      rw [interior_Ici] at hx
      have hx0 : (0 : ℝ) < x := hx
      rw [(hasDerivAt_Elow x (by linarith)).deriv]
      positivity
  have h0 : W 0 - (0 : ℝ) ^ 3 / (2 * (1 + 0) ^ 2) = 0 := by simp [W]
  have := hmono (Set.mem_Ici.mpr le_rfl) (Set.mem_Ici.mpr hu.le) hu
  dsimp only at this
  linarith

theorem Fw_le_M (u : ℝ) (hu : 0 < u) : Phi u ≤ 1 / 2 := by
  unfold Phi
  have h := W_le_y u hu.le
  have h1 : 0 < 1 + u := by linarith
  have h2 : 0 < u ^ 2 := by positivity
  rw [div_le_iff₀ h2]
  have h3 := mul_le_mul_of_nonneg_right h h1.le
  have e : u ^ 2 / (1 + u) * (1 + u) = u ^ 2 := by field_simp
  linarith

theorem Psi_strictMono_M : StrictMonoOn Psi (Set.Ioi 0) := by
  apply strictMonoOn_of_deriv_pos (convex_Ioi 0)
  · intro x hx
    have hx0 : (0 : ℝ) < x := hx
    exact (hasDerivAt_Psi x hx0).continuousAt.continuousWithinAt
  · intro x hx
    rw [interior_Ioi] at hx
    have hx0 : (0 : ℝ) < x := hx
    rw [(hasDerivAt_Psi x hx0).deriv]
    have hlow := W_lower x hx0
    have hA : 0 < 2 * (1 + x) * (2 + x) / x ^ 5 := by positivity
    have hB : x ^ 3 / (2 * (1 + x) ^ 2) - W x < 0 := by linarith
    exact mul_pos hA hB

theorem eq_bracket_M (u k : ℝ) (hu : 0 < u) (hk : 0 < k) (h : Psi u = k) : 2 * k * u < 1 := by
  have hlow := W_lower u hu
  have hp : 0 < 1 + u := by linarith
  have hu4 : 0 < u ^ 4 := by positivity
  have hu3 : 0 < u ^ 3 := by positivity
  have hP : W u * (1 + u) ^ 2 = k * u ^ 4 := by
    unfold Psi at h
    rw [div_eq_iff hu4.ne'] at h
    exact h
  have hd : 0 < 2 * (1 + u) ^ 2 := by positivity
  have hl : u ^ 3 < W u * (2 * (1 + u) ^ 2) := (div_lt_iff₀ hd).mp hlow
  have e1 : W u * (2 * (1 + u) ^ 2) = 2 * (k * u ^ 4) := by
    rw [← hP]; ring
  have h3 : u ^ 3 < 2 * (k * u ^ 4) := by linarith
  by_contra hc
  push Not at hc
  have h5 : u ^ 3 * 1 ≤ u ^ 3 * (2 * k * u) := mul_le_mul_of_nonneg_left hc hu3.le
  have e : u ^ 3 * (2 * k * u) = 2 * (k * u ^ 4) := by ring
  linarith

theorem sticky_merge_M (M m V v : ℝ) (hM : 0 < M) (hm : 0 < m) :
    1 / 2 * M * V ^ 2 + 1 / 2 * m * v ^ 2 - 1 / 2 * (M + m) * ((M * V + m * v) / (M + m)) ^ 2
      = -(1 / 2 * M * m * (V - v) ^ 2 / (M + m)) := by
  have h : (M + m) ≠ 0 := by positivity
  field_simp
  ring

theorem deep_eq_M (s k : ℝ) (hs : 0 < s) (hk : 0 < k) : 2 / 3 * s = k * s ^ 2 ↔ 1 / s = k := by
  constructor
  · intro h
    have h2 : s * (k * s) = s * (2 / 3) := by linear_combination -h
    have h1 : k * s = 2 / 3 := mul_left_cancel₀ hs.ne' h2
    rw [div_eq_iff hs.ne']
    linear_combination (-3 / 2 : ℝ) * h1
  · intro h
    rw [div_eq_iff hs.ne'] at h
    linear_combination (2 / 3 * s) * h

end SNP1M
-- kappa = 1/2 FITTED; not theory closed. Adopts nothing.
