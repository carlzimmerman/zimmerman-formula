/-
NSW1 (criteria 052f87daad): Lean statements for the non-spherical wall. They certify the algebra and the inequalities, not the
physics and not the divergence theorem. TEST lane; adopts nothing. kappa = 1/2 FITTED; not theory closed.

The law: mu(u) = u / (1 + u). A switch S in [0, 1] multiplies the law's Lagrangian J(u) = u - ln(1 + u) (units a0^2 / 4 pi G).
At a wall: d the normal flux and e_t the tangential field (both continuous), u the law's field magnitude just inside, n its
normal part, so d = n u / (1 + u) and e_t^2 = u^2 - n^2.

  A1  exterior_flux, layer_bookkeeping        : outside the wall the flux is the gradient; interior gradient flux plus layer = d.
  A2  path_end                                : on the law-on side of the wall S = (1 + u)(1 - d / n) = 1.
      hasDerivAt_G                            : d/dv [v^2 / 2 - d sqrt(v^2 - e_t^2)] = S(v) v / (1 + v), the antiderivative step.
      Wg_by_parts                             : J(u) S(u) - (G(u) - G(u0)) = W_g = u - ln(1 + u) - n^2 / (2 (1 + u)^2).
      stress_jump, slab_lagrangian            : the same W_g from the jump of the normal stress and from the slab Lagrangian.
      Wg_normal, Wg_tangent                   : e_t = 0 gives SWT1's W; d = 0 gives J.
  A3  W_le_Wg, Wg_le_J                        : (a) W(u) <= W_g <= J(u) at fixed u.
      gout_sq_bound, Wg_le_gout               : (b) W_g <= sqrt(d^2 + e_t^2) = |g_out| / a0.
      deep_leading, deep_normal               : (c) the leading-order algebra only (no remainder bound).
  A4  column_bound, cap_sum                   : p_wall / |g_out| <= 1 in units a0 / (4 pi G); the summed force is at most the
                                                summed |g_out| for non-negative area weights.
  A5  cold_shell, gout_normal, normal_wall_cap: no tangential stress forces g_t = 0; then |g_out| = d and W_g <= d.
  A6  deep_bracket                            : sqrt(d_min) F <= sum f sqrt(d) <= sqrt(d_max) F for fluxes f >= 0 (the bracket on
                                                the deep-limit force). The comparison statement itself is not in Lean.
  hasDerivAt_W, W_nonneg, W_le_y              : copied from SWT1.lean.
-/
import Mathlib

namespace NSW1

noncomputable def J (u : ℝ) : ℝ := u - Real.log (1 + u)
noncomputable def W (u : ℝ) : ℝ := u - Real.log (1 + u) - u ^ 2 / (2 * (1 + u) ^ 2)
/-- A2: the wall pressure with a tangential field; u the interior magnitude, n its normal part. -/
noncomputable def Wg (u n : ℝ) : ℝ := u - Real.log (1 + u) - n ^ 2 / (2 * (1 + u) ^ 2)

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

theorem W_le_y (u : ℝ) (hu : 0 ≤ u) : W u ≤ u ^ 2 / (1 + u) := by
  unfold W
  have hp : 0 < 1 + u := by linarith
  have hlog : 1 - (1 + u)⁻¹ ≤ Real.log (1 + u) := Real.one_sub_inv_le_log_of_pos hp
  have h2 : 0 ≤ u ^ 2 / (2 * (1 + u) ^ 2) := by positivity
  have h3 : u - (1 - (1 + u)⁻¹) = u ^ 2 / (1 + u) := by
    field_simp
    ring
  linarith

/-! ### A1: the algebraic steps of compensation -/

/-- outside the wall the switch is off and the flux is the gradient itself. -/
theorem exterior_flux (u g : ℝ) : (1 - (0 : ℝ) / (1 + u)) * g = g := by simp

/-- at a wall element the effective mass seen from outside is the interior gradient flux n plus the layer d - n: the flux d. -/
theorem layer_bookkeeping (n d : ℝ) : n + (d - n) = d := by ring

/-! ### A2: the wall pressure with a tangential field -/

/-- on the law-on side of the wall S = (1 + u)(1 - d / n) = 1 for d = n u / (1 + u). -/
theorem path_end (u n : ℝ) (hu : 0 ≤ u) (hn : 0 < n) :
    (1 + u) * (1 - (n * u / (1 + u)) / n) = 1 := by
  have h : (1 + u) ≠ 0 := by positivity
  have hn' : n ≠ 0 := ne_of_gt hn
  field_simp
  ring

/-- the antiderivative step: with S(v) = (1 + v)(1 - d / sqrt(v^2 - e_t^2)) and J'(v) = v / (1 + v),
    d/dv [v^2 / 2 - d sqrt(v^2 - e_t^2)] = S(v) J'(v). -/
theorem hasDerivAt_G (d e2 v : ℝ) (hv : 0 < v) (hpos : 0 < v ^ 2 - e2) :
    HasDerivAt (fun x : ℝ => x ^ 2 / 2 - d * Real.sqrt (x ^ 2 - e2))
      ((1 + v) * (1 - d / Real.sqrt (v ^ 2 - e2)) * (v / (1 + v))) v := by
  have hs : 0 < Real.sqrt (v ^ 2 - e2) := Real.sqrt_pos.mpr hpos
  have hs' : Real.sqrt (v ^ 2 - e2) ≠ 0 := ne_of_gt hs
  have hp : (1 + v) ≠ 0 := by positivity
  have hn : HasDerivAt (fun x : ℝ => x ^ 2) (2 * v) v := by
    simpa using hasDerivAt_pow 2 v
  have h1 : HasDerivAt (fun x : ℝ => x ^ 2 - e2) (2 * v) v := hn.sub_const e2
  have h2 : HasDerivAt (fun x : ℝ => Real.sqrt (x ^ 2 - e2)) (2 * v / (2 * Real.sqrt (v ^ 2 - e2))) v :=
    h1.sqrt (ne_of_gt hpos)
  have h3 : HasDerivAt (fun x : ℝ => x ^ 2 / 2) (2 * v / 2) v := hn.div_const 2
  have h4 : HasDerivAt (fun x : ℝ => x ^ 2 / 2 - d * Real.sqrt (x ^ 2 - e2))
      (2 * v / 2 - d * (2 * v / (2 * Real.sqrt (v ^ 2 - e2)))) v := h3.sub (h2.const_mul d)
  have hderiv : 2 * v / 2 - d * (2 * v / (2 * Real.sqrt (v ^ 2 - e2)))
      = (1 + v) * (1 - d / Real.sqrt (v ^ 2 - e2)) * (v / (1 + v)) := by
    field_simp
  exact h4.congr_deriv hderiv

/-- A2 by parts. With e_t^2 = u^2 - n^2, d = n u / (1 + u), u0^2 = d^2 + e_t^2 and G(v) = v^2 / 2 - d sqrt(v^2 - e_t^2)
    (so G(u) = u^2 / 2 - d n and G(u0) = u0^2 / 2 - d d): the integral of J dS is J(u) S(u) - (G(u) - G(u0)) = W_g. -/
theorem Wg_by_parts (u n : ℝ) (hu : 0 ≤ u) :
    J u * 1 - ((u ^ 2 / 2 - (n * u / (1 + u)) * n)
      - (((n * u / (1 + u)) ^ 2 + (u ^ 2 - n ^ 2)) / 2 - (n * u / (1 + u)) * (n * u / (1 + u)))) = Wg u n := by
  unfold J Wg
  have h : (1 + u) ≠ 0 := by positivity
  field_simp
  ring

/-- the same W_g as the jump of the normal stress T_nn = -D_n dPhi/dn - L across the wall:
    T_out = (e_t^2 - d^2) / 2, T_in = -d n + u^2 / 2 - J(u). -/
theorem stress_jump (u n : ℝ) (hu : 0 ≤ u) :
    ((u ^ 2 - n ^ 2) - (n * u / (1 + u)) ^ 2) / 2 - (-(n * u / (1 + u)) * n + u ^ 2 / 2 - J u) = Wg u n := by
  unfold J Wg
  have h : (1 + u) ≠ 0 := by positivity
  field_simp
  ring

/-- the same W_g from the Lagrangian of a slab in a uniform oblique field, per unit area and unit wall displacement:
    l_in = -u^2 / 2 + J(u) + d n, l_out = -(d^2 + e_t^2) / 2 + d^2. -/
theorem slab_lagrangian (u n : ℝ) (hu : 0 ≤ u) :
    (-(u ^ 2) / 2 + J u + (n * u / (1 + u)) * n)
      - (-((n * u / (1 + u)) ^ 2 + (u ^ 2 - n ^ 2)) / 2 + (n * u / (1 + u)) ^ 2) = Wg u n := by
  unfold J Wg
  have h : (1 + u) ≠ 0 := by positivity
  field_simp
  ring

/-- e_t = 0 (n = u): SWT1's W. -/
theorem Wg_normal (u : ℝ) : Wg u u = W u := rfl

/-- d = 0 (n = 0, the field runs along the wall): J. -/
theorem Wg_tangent (u : ℝ) : Wg u 0 = J u := by
  unfold Wg J
  simp

/-! ### A3: pointwise bounds -/

theorem J_nonneg (u : ℝ) (hu : 0 ≤ u) : 0 ≤ J u := by
  unfold J
  have hp : 0 < 1 + u := by linarith
  have := Real.log_le_sub_one_of_pos hp
  linarith

theorem J_le (u : ℝ) (hu : 0 ≤ u) : J u ≤ u := by
  unfold J
  have : 0 ≤ Real.log (1 + u) := Real.log_nonneg (by linarith)
  linarith

/-- A3(a), lower side. -/
theorem W_le_Wg (u n : ℝ) (hu : 0 ≤ u) (hn0 : 0 ≤ n) (hnu : n ≤ u) : W u ≤ Wg u n := by
  unfold W Wg
  have hp : 0 < 2 * (1 + u) ^ 2 := by positivity
  have hsq : n ^ 2 ≤ u ^ 2 := by nlinarith
  have h : n ^ 2 / (2 * (1 + u) ^ 2) ≤ u ^ 2 / (2 * (1 + u) ^ 2) := div_le_div_of_nonneg_right hsq hp.le
  linarith

/-- A3(a), upper side. -/
theorem Wg_le_J (u n : ℝ) (hu : 0 ≤ u) : Wg u n ≤ J u := by
  unfold Wg J
  have : 0 ≤ n ^ 2 / (2 * (1 + u) ^ 2) := by positivity
  linarith

theorem Wg_nonneg (u n : ℝ) (hu : 0 ≤ u) (hn0 : 0 ≤ n) (hnu : n ≤ u) : 0 ≤ Wg u n :=
  le_trans (W_nonneg u hu) (W_le_Wg u n hu hn0 hnu)

/-- A3(b), the algebra. With t = n^2 in [0, u^2], j = J(u): |g_out|^2 - W_g^2 is concave in t and non-negative at both ends
    (t = 0: u^2 - J^2; t = u^2: y^2 - W^2, y = u^2 / (1 + u)). The identity `key` is that statement multiplied by u^2. -/
theorem gout_sq_bound (u j t : ℝ) (hu : 0 < u) (hj0 : 0 ≤ j) (hju : j ≤ u)
    (hw0 : 0 ≤ j - u ^ 2 / (2 * (1 + u) ^ 2)) (hwy : j - u ^ 2 / (2 * (1 + u) ^ 2) ≤ u ^ 2 / (1 + u))
    (ht0 : 0 ≤ t) (htu : t ≤ u ^ 2) :
    (j - t / (2 * (1 + u) ^ 2)) ^ 2 ≤ t * u ^ 2 / (1 + u) ^ 2 + (u ^ 2 - t) := by
  have hp : (1 + u) ≠ 0 := by positivity
  have key : u ^ 2 * (t * u ^ 2 / (1 + u) ^ 2 + (u ^ 2 - t) - (j - t / (2 * (1 + u) ^ 2)) ^ 2)
      = (u ^ 2 - t) * (u ^ 2 - j ^ 2)
        + t * ((u ^ 2 / (1 + u)) ^ 2 - (j - u ^ 2 / (2 * (1 + u) ^ 2)) ^ 2)
        + (1 / (2 * (1 + u) ^ 2)) ^ 2 * u ^ 2 * t * (u ^ 2 - t) := by
    field_simp
    ring
  have h1 : 0 ≤ (u ^ 2 - t) * (u ^ 2 - j ^ 2) := by
    apply mul_nonneg (by linarith)
    nlinarith [mul_nonneg (sub_nonneg.mpr hju) (add_nonneg hu.le hj0)]
  have h2 : 0 ≤ t * ((u ^ 2 / (1 + u)) ^ 2 - (j - u ^ 2 / (2 * (1 + u) ^ 2)) ^ 2) := by
    apply mul_nonneg ht0
    nlinarith [mul_nonneg (sub_nonneg.mpr hwy) (add_nonneg (le_trans hw0 hwy) hw0)]
  have h3 : 0 ≤ (1 / (2 * (1 + u) ^ 2)) ^ 2 * u ^ 2 * t * (u ^ 2 - t) := by
    have hc : 0 ≤ (1 / (2 * (1 + u) ^ 2)) ^ 2 * u ^ 2 := by positivity
    exact mul_nonneg (mul_nonneg hc ht0) (by linarith)
  have hX : 0 ≤ u ^ 2 * (t * u ^ 2 / (1 + u) ^ 2 + (u ^ 2 - t) - (j - t / (2 * (1 + u) ^ 2)) ^ 2) := by
    rw [key]; linarith
  have hu2 : 0 < u ^ 2 := by positivity
  have hY : 0 ≤ t * u ^ 2 / (1 + u) ^ 2 + (u ^ 2 - t) - (j - t / (2 * (1 + u) ^ 2)) ^ 2 := by
    by_contra hneg
    rw [not_le] at hneg
    have := mul_neg_of_pos_of_neg hu2 hneg
    linarith
  linarith

/-- A3(b): the wall pressure never exceeds a0 |g_out| / (4 pi G), g_out the Newtonian field just outside the wall. -/
theorem Wg_le_gout (u n : ℝ) (hu : 0 < u) (hn0 : 0 ≤ n) (hnu : n ≤ u) :
    Wg u n ≤ Real.sqrt ((n * u / (1 + u)) ^ 2 + (u ^ 2 - n ^ 2)) := by
  have h0 : 0 ≤ Wg u n := Wg_nonneg u n hu.le hn0 hnu
  have hJ0 := J_nonneg u hu.le
  have hJu := J_le u hu.le
  have hW0 := W_nonneg u hu.le
  have hWy := W_le_y u hu.le
  have ht0 : 0 ≤ n ^ 2 := by positivity
  have htu : n ^ 2 ≤ u ^ 2 := by nlinarith
  have hw0 : 0 ≤ J u - u ^ 2 / (2 * (1 + u) ^ 2) := by
    unfold J; unfold W at hW0; linarith
  have hwy : J u - u ^ 2 / (2 * (1 + u) ^ 2) ≤ u ^ 2 / (1 + u) := by
    unfold J; unfold W at hWy; linarith
  have hsq := gout_sq_bound u (J u) (n ^ 2) hu hJ0 hJu hw0 hwy ht0 htu
  have hrew : (n * u / (1 + u)) ^ 2 + (u ^ 2 - n ^ 2) = n ^ 2 * u ^ 2 / (1 + u) ^ 2 + (u ^ 2 - n ^ 2) := by
    rw [div_pow, mul_pow]
  have hWg : Wg u n = J u - n ^ 2 / (2 * (1 + u) ^ 2) := by
    unfold Wg J; ring
  have h0' : 0 ≤ J u - n ^ 2 / (2 * (1 + u) ^ 2) := by
    rw [← hWg]; exact h0
  rw [hrew, hWg]
  calc J u - n ^ 2 / (2 * (1 + u) ^ 2)
      = Real.sqrt ((J u - n ^ 2 / (2 * (1 + u) ^ 2)) ^ 2) := (Real.sqrt_sq h0').symm
    _ ≤ Real.sqrt (n ^ 2 * u ^ 2 / (1 + u) ^ 2 + (u ^ 2 - n ^ 2)) := Real.sqrt_le_sqrt hsq

/-- A3(c), leading-order algebra only: with ln(1 + u) replaced by u - u^2/2 + u^3/3 and 1 / (1 + u)^2 by 1 - 2u,
    W_g becomes e_t^2 / 2 + n^2 u - u^3 / 3. No remainder bound is proved. -/
theorem deep_leading (u n e2 : ℝ) (h : u ^ 2 = n ^ 2 + e2) :
    (u - (u - u ^ 2 / 2 + u ^ 3 / 3)) - n ^ 2 * (1 - 2 * u) / 2 = e2 / 2 + n ^ 2 * u - u ^ 3 / 3 := by
  have he : e2 = u ^ 2 - n ^ 2 := by linarith
  subst he
  ring

/-- e_t = 0 in the leading order: (2/3) u^3. -/
theorem deep_normal (u : ℝ) : (0 : ℝ) / 2 + u ^ 2 * u - u ^ 3 / 3 = 2 / 3 * u ^ 3 := by ring

/-! ### A4: the cap for any wall -/

/-- the column a wall element can carry: p_wall / |g_out| <= 1 in units a0 / (4 pi G). -/
theorem column_bound (u n : ℝ) (hu : 0 < u) (hn0 : 0 ≤ n) (hnu : n ≤ u)
    (hg : 0 < Real.sqrt ((n * u / (1 + u)) ^ 2 + (u ^ 2 - n ^ 2))) :
    Wg u n / Real.sqrt ((n * u / (1 + u)) ^ 2 + (u ^ 2 - n ^ 2)) ≤ 1 :=
  (div_le_one hg).mpr (Wg_le_gout u n hu hn0 hnu)

/-- summed over wall elements with non-negative areas w: the total normal force is at most the summed |g_out|. -/
theorem cap_sum {ι : Type} (s : Finset ι) (w u n : ι → ℝ) (hw : ∀ i ∈ s, 0 ≤ w i)
    (hu : ∀ i ∈ s, 0 < u i) (hn0 : ∀ i ∈ s, 0 ≤ n i) (hnu : ∀ i ∈ s, n i ≤ u i) :
    ∑ i ∈ s, w i * Wg (u i) (n i)
      ≤ ∑ i ∈ s, w i * Real.sqrt ((n i * u i / (1 + u i)) ^ 2 + ((u i) ^ 2 - (n i) ^ 2)) := by
  apply Finset.sum_le_sum
  intro i hi
  exact mul_le_mul_of_nonneg_left (Wg_le_gout (u i) (n i) (hu i hi) (hn0 i hi) (hnu i hi)) (hw i hi)

/-! ### A5: cold shells -/

/-- a shell of surface density sigma > 0 with no tangential stress is in balance only if the tangential field vanishes. -/
theorem cold_shell (σ gt : ℝ) (hσ : 0 < σ) (h : σ * gt = 0) : gt = 0 := by
  rcases mul_eq_zero.mp h with h1 | h1
  · linarith
  · exact h1

/-- with no tangential field |g_out| is the normal flux. -/
theorem gout_normal (d : ℝ) (hd : 0 ≤ d) : Real.sqrt (d ^ 2 + 0) = d := by
  rw [add_zero, Real.sqrt_sq hd]

/-- and the wall pressure is at most the normal flux d = u^2 / (1 + u): SNP1 A.1's cap, element by element. -/
theorem normal_wall_cap (u : ℝ) (hu : 0 ≤ u) : Wg u u ≤ u ^ 2 / (1 + u) := by
  rw [Wg_normal]
  exact W_le_y u hu

/-! ### A6: the deep-limit bracket -/

/-- for element fluxes f >= 0 and flux densities d between d_min and d_max:
    sqrt(d_min) sum f <= sum f sqrt(d) <= sqrt(d_max) sum f. In the deep limit F_n = (2/3) sum f sqrt(d). -/
theorem deep_bracket {ι : Type} (s : Finset ι) (f d : ι → ℝ) (dmin dmax : ℝ) (hf : ∀ i ∈ s, 0 ≤ f i)
    (hmin : ∀ i ∈ s, dmin ≤ d i) (hmax : ∀ i ∈ s, d i ≤ dmax) :
    Real.sqrt dmin * ∑ i ∈ s, f i ≤ ∑ i ∈ s, f i * Real.sqrt (d i) ∧
    ∑ i ∈ s, f i * Real.sqrt (d i) ≤ Real.sqrt dmax * ∑ i ∈ s, f i := by
  constructor
  · rw [Finset.mul_sum]
    apply Finset.sum_le_sum
    intro i hi
    have h := mul_le_mul_of_nonneg_left (Real.sqrt_le_sqrt (hmin i hi)) (hf i hi)
    linarith
  · rw [Finset.mul_sum]
    apply Finset.sum_le_sum
    intro i hi
    have h := mul_le_mul_of_nonneg_left (Real.sqrt_le_sqrt (hmax i hi)) (hf i hi)
    linarith

end NSW1

#print axioms NSW1.exterior_flux
#print axioms NSW1.layer_bookkeeping
#print axioms NSW1.path_end
#print axioms NSW1.hasDerivAt_G
#print axioms NSW1.Wg_by_parts
#print axioms NSW1.stress_jump
#print axioms NSW1.slab_lagrangian
#print axioms NSW1.Wg_normal
#print axioms NSW1.Wg_tangent
#print axioms NSW1.J_nonneg
#print axioms NSW1.J_le
#print axioms NSW1.W_le_Wg
#print axioms NSW1.Wg_le_J
#print axioms NSW1.Wg_nonneg
#print axioms NSW1.gout_sq_bound
#print axioms NSW1.Wg_le_gout
#print axioms NSW1.deep_leading
#print axioms NSW1.deep_normal
#print axioms NSW1.column_bound
#print axioms NSW1.cap_sum
#print axioms NSW1.cold_shell
#print axioms NSW1.gout_normal
#print axioms NSW1.normal_wall_cap
#print axioms NSW1.deep_bracket
#print axioms NSW1.hasDerivAt_W
#print axioms NSW1.W_nonneg
#print axioms NSW1.W_le_y
