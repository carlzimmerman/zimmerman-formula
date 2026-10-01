import Mathlib
import Mathlib.Tactic

/-
  AS019 -- Deep-law source mass conventions (Lean 4 certificate).

  Physically: in the deep regime v^4 = C * M(<r) (C = G_N * a0 > 0), the running
  circular speed satisfies the log-slope identity
        d ln v / d ln r = (1/4) * d ln M(<r) / d ln r ,
  so (i) a uniform-density sphere forces slope 3/4, (ii) the WRONG convention that
  inserts the total (constant) mass everywhere inside the sphere forces slope 0,
  and (iii) the Newtonian counterpart (v^2 = C * M(<r)/r, M = k r^3) forces slope 1.
  Convention-flip consequences: (iv) if a catalog re-labels the enclosed mass by a
  factor lam (M -> lam*M at fixed C = G*a0), the flat speed ratio satisfies
  (v2/v1)^4 = lam, (v) the relative error against the settled total law is
  (v/v_flat)^4 = M(<r)/M_tot, and (vi) the transition radius squares scale as
  r_M(lam*M)^2 = lam * r_M(M)^2.

  All powers are natural powers; positivity hypotheses state the physical domain
  (positive enclosed mass, positive speed, positive radius).
-/


noncomputable section
open Real

/-- Log-slope identity for the deep law `v^4 = C*M(r)`:
   `d ln v / d ln r = (1/4) * d ln M / d ln r`, i.e.
   `v'(r) * r / v(r) = (1/4) * M'(r) * r / M(r)`. -/
theorem deep_log_slope_identity
    {C : ℝ} (hC : 0 < C)
    {M v : ℝ → ℝ} {r v' M' : ℝ}
    (hM : HasDerivAt M M' r) (hv : HasDerivAt v v' r)
    (hpow : ∀ x, v x ^ 4 = C * M x)
    (hMr : 0 < M r) (hvr : 0 < v r) :
    v' * r / v r = (M' * r) / (4 * M r) := by
  have hder4 : HasDerivAt (v ^ (4 : ℕ)) (4 * (v r) ^ 3 * v') r := by
    simpa using (hv.pow (4 : ℕ))
  have heq : (fun x : ℝ => C * M x) =ᶠ[nhds r] (v ^ (4 : ℕ)) := by
    filter_upwards with x
    simpa using (hpow x).symm
  have hc : HasDerivAt (fun x : ℝ => C * M x) (4 * (v r) ^ 3 * v') r :=
    hder4.congr_of_eventuallyEq heq
  have hf : HasDerivAt (fun x : ℝ => C * M x) (C * M') r := hM.const_mul C
  have hid : 4 * (v r) ^ 3 * v' = C * M' := HasDerivAt.unique hc hf
  have hv3 : 4 * (v r) ^ 3 ≠ 0 := by
    exact ne_of_gt (mul_pos (by norm_num) (pow_pos hvr (3 : ℕ)))
  have hdiv : v' = (C * M') / (4 * (v r) ^ 3) := by
    rw [eq_div_iff_mul_eq hv3]
    simpa [mul_comm] using hid
  have hA : v' * r = (C * M' * r) / (4 * (v r) ^ 3) := by
    rw [hdiv]
    ring
  have hB : v' * r / v r = (C * M' * r) / (4 * (v r) ^ 3 * (v r)) := by
    rw [hA]
    field_simp [hvr.ne']
  have hp34 : (v r) ^ 3 * (v r) = (v r) ^ 4 := by
    simp [pow_succ]
  have hB2 : v' * r / v r = (C * M' * r) / (4 * (v r) ^ 4) := by
    calc
      v' * r / v r = (C * M' * r) / (4 * (v r) ^ 3 * (v r)) := hB
      _ = (C * M' * r) / (4 * (v r) ^ 4) := by
        apply congr_arg (fun t : ℝ => (C * M' * r) / t)
        rw [mul_assoc, ← hp34]
  rw [hpow] at hB2
  have hD : (C * M' * r) / (4 * (C * M r)) = (M' * r) / (4 * M r) := by
    field_simp [hC.ne', hMr.ne']
  exact hB2.trans hD

/-- Uniform-density baryon sphere, deep enclosed-mass convention:
   M(r) = k r^3  forces the running log-log slope 3/4. -/
theorem uniform_sphere_deep_slope_three_quarters
    {C k : ℝ} (hC : 0 < C) (hk : 0 < k)
    {v : ℝ → ℝ} {r v' : ℝ}
    (hv : HasDerivAt v v' r) (hpow : ∀ x, v x ^ 4 = C * (k * x ^ 3))
    (hvr : 0 < v r) (hr : 0 < r) :
    v' * r / v r = 3 / 4 := by
  have hid' : HasDerivAt (id ^ (3 : ℕ)) (3 * r ^ 2) r := by
    simpa using (hasDerivAt_id r).pow (3 : ℕ)
  have hM : HasDerivAt (fun x : ℝ => k * x ^ 3) (k * (3 * r ^ 2)) r := by
    simpa using hid'.const_mul k
  have hMr : 0 < k * r ^ 3 := mul_pos hk (pow_pos hr (3 : ℕ))
  have hpi := deep_log_slope_identity hC hM hv hpow hMr hvr
  have hfin : (k * (3 * r ^ 2)) * r / (4 * (k * r ^ 3)) = 3 / 4 := by
    field_simp [hk.ne', hr.ne']
  exact hpi.trans hfin

/-- NEGATIVE CONTROL (wrong convention): substituting the TOTAL (constant) mass
   everywhere inside a uniform sphere makes the running slope vanish:
   slope = 0, which is the wrong radial power (the enclosed convention gives 3/4). -/
theorem total_convention_deep_slope_zero
    {C M_tot : ℝ} (hC : 0 < C) (hMt : 0 < M_tot)
    {v : ℝ → ℝ} {r v' : ℝ}
    (hv : HasDerivAt v v' r) (hpow : ∀ x, v x ^ 4 = C * M_tot)
    (hvr : 0 < v r) (_hr : 0 < r) :
    v' * r / v r = 0 := by
  have hM' : HasDerivAt (fun _ : ℝ => M_tot) 0 r := hasDerivAt_const r M_tot
  have hpi := deep_log_slope_identity hC hM' hv hpow hMt hvr
  have hfin : 0 * r / (4 * M_tot) = 0 := by
    simp
  exact hpi.trans hfin

/-- Newtonian counterpart inside a uniform sphere (v^2 = C*k*r^2, M = k r^3):
   solid-body slope 1, distinct from both deep values 3/4 and 0. -/
theorem uniform_sphere_newtonian_slope_one
    {C k : ℝ} (hC : 0 < C) (hk : 0 < k)
    {v : ℝ → ℝ} {r v' : ℝ}
    (hv : HasDerivAt v v' r) (hpow : ∀ x, (v x) ^ 2 = C * (k * x ^ 2))
    (hvr : 0 < v r) (hr : 0 < r) :
    v' * r / v r = 1 := by
  have hd2 : HasDerivAt (v ^ (2 : ℕ)) (2 * v r * v') r := by
    simpa using (hv.pow (2 : ℕ))
  have hid2 : HasDerivAt (id ^ (2 : ℕ)) (2 * r) r := by
    simpa using (hasDerivAt_id r).pow (2 : ℕ)
  have hk' : HasDerivAt (fun x : ℝ => k * x ^ 2) (k * (2 * r)) r := by
    simpa using hid2.const_mul k
  have heq : (fun x : ℝ => C * (k * x ^ 2)) =ᶠ[nhds r] (v ^ (2 : ℕ)) := by
    filter_upwards with x
    simpa using (hpow x).symm
  have hc : HasDerivAt (fun x : ℝ => C * (k * x ^ 2)) (2 * v r * v') r :=
    hd2.congr_of_eventuallyEq heq
  have hid := HasDerivAt.unique (hk'.const_mul C) hc
  have hlin : v r * v' = C * k * r := by
    calc
      v r * v' = (2 * (v r) * v') / 2 := by ring
      _ = (C * (k * (2 * r))) / 2 := by rw [← hid]
      _ = C * k * r := by ring
  have hvp : v' = (C * k * r) / (v r) := by
    rw [eq_div_iff_mul_eq hvr.ne']
    rw [mul_comm]
    exact hlin
  rw [hvp]
  field_simp [hvr.ne']
  rw [hpow]
  ring

/-- Convention-flip consequence: M -> lam*M at fixed C = G*a0 transforms the flat
   speed by (v2/v1)^4 = lam. -/
theorem flip_speed_fourth_ratio
    {C lam M₁ M₂ v₁ v₂ : ℝ} (hC : 0 < C) (hM₁ : 0 < M₁)
    (hM₂ : M₂ = lam * M₁) (h₁ : v₁ ^ 4 = C * M₁) (h₂ : v₂ ^ 4 = C * M₂)
    (hv₁ : 0 < v₁) (hv₂ : 0 < v₂) :
    (v₂ / v₁) ^ 4 = lam := by
  rw [div_pow, h₁, h₂, hM₂]
  field_simp [hC.ne', hM₁.ne']

/-- Flatness condition: relative speed error against the settled total law is
   (v/v_flat)^4 = M(<r)/M_tot. -/
theorem flatness_violation_ratio
    {C M M_tot v vf : ℝ} (hC : 0 < C) (hM : 0 < M) (hMt : 0 < M_tot)
    (hv : v ^ 4 = C * M) (hvf : vf ^ 4 = C * M_tot) :
    (v / vf) ^ 4 = M / M_tot := by
  rw [div_pow, hv, hvf]
  field_simp [hC.ne', hMt.ne']

/-- Transition-radius flip: r_M(lam*M)^2 = lam * r_M(M)^2 with r_M(M) = sqrt(G*M/a). -/
theorem rM_flip_square_ratio
    {G a lam M₁ M₂ r₁ r₂ : ℝ} (hG : 0 < G) (ha : 0 < a)
    (hM : M₂ = lam * M₁)
    (e₁ : r₁ ^ 2 = G * M₁ / a) (e₂ : r₂ ^ 2 = G * M₂ / a) :
    r₂ ^ 2 = lam * r₁ ^ 2 := by
  rw [e₂, e₁, hM]
  field_simp [ha.ne', hG.ne']

end