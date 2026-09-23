import Mathlib

/-!
# ZD01 — The Phantom Ceiling (the dark-acceleration cap)

Framework premise (docstring scope, NOT certified here): the RAR equilibrium
law of the Zimmerman framework, g_obs^2 - g_bar^2 = a0 * g_bar (itself derived
from the action in PD08/PD13 of deepseek_push/STATE.md). In normalized units
x = g_bar / a0 the phantom (dark) acceleration of a baryon field is

    phi(x) := sqrt(x^2 + x) - x.

Certified consequences, all new to the corpus:

  1. PRODUCT IDENTITY: phi(x) * (sqrt(x^2+x) + x) = x, exactly. The a0-line
     in product form: g_phi * (g_obs + g_bar) = a0 * g_bar.
  2. THE CEILING: phi(x) <= 1/2 with equality only in the limit x -> inf.
     The phantom acceleration of ANY baryon field is strictly below a0/2 =
     kappa * a0 where kappa = 1/2 is the framework's derived constant
     (PD01-PD13). No system on the line can exhibit a dark acceleration
     >= a0/2 — the sharpest falsifiable contrast with Lambda-CDM halos.
  3. MONOTONICITY: phi increases with the baryon field; the boost approaches
     its ceiling from below, never overshooting.
  4. APPROACH LAW: for g_bar >= a0/8 the two-term expansion bounds the field:
     a0/2 - a0^2/(8 g_bar) <= g_phi < a0/2.
  5. NO-CONTAINMENT: an ambient (external) field ge >= a0/2 can never be
     matched by an internal phantom field — there is no equilibrium radius.
  6. CONTAINMENT INVERSE: for ge < a0/2 the containment field is EXACT:
     g_phi = ge at g_bar = ge^2 / (a0 - 2 ge), i.e. radius
     r_t = r * sqrt(...) with g_bar = G M / r^2 (certified algebraically:
     r^2 = G M (a0 - 2 ge) / ge^2). Deep-MOND limit: r_t ~ sqrt(G M a0)/ge.

Lean certifies the mathematics (the identities and bounds); the physical
premise (the a0-line as the law) is the framework's, stated in STATE.md.
-/

noncomputable section
open scoped Real

/-- The phantom (dark) acceleration normalized by a0, as a function of the
baryonic field x = g_bar / a0:  sqrt(x^2 + x) - x. -/
noncomputable def phi (a0 x : ℝ) : ℝ := Real.sqrt (x^2 + a0 * x) - x

/-- The baryon field at which the phantom equals the external field ge
(containment field):  ge^2 / (a0 - 2 ge). -/
noncomputable def cont_field (a0 ge : ℝ) : ℝ := ge^2 / (a0 - 2 * ge)

theorem phantom_product (a0 x : ℝ) (ha0 : 0 < a0) (hx : 0 ≤ x) :
    phi a0 x * (Real.sqrt (x^2 + a0 * x) + x) = a0 * x := by
  have hnn : 0 ≤ x^2 + a0 * x := by
    nlinarith [sq_nonneg x, hx, ha0.le]
  unfold phi
  calc
    (Real.sqrt (x^2 + a0 * x) - x) * (Real.sqrt (x^2 + a0 * x) + x)
        = Real.sqrt (x^2 + a0 * x)^2 - x^2 := by ring
    _ = (x^2 + a0 * x) - x^2 := by rw [Real.sq_sqrt hnn]
    _ = a0 * x := by ring

theorem phantom_zero (a0 : ℝ) (_ha0 : 0 < a0) : phi a0 0 = 0 := by
  unfold phi
  simp

theorem phantom_nonneg (a0 x : ℝ) (ha0 : 0 < a0) (hx : 0 ≤ x) : 0 ≤ phi a0 x := by
  unfold phi
  have hy : 0 ≤ x^2 + a0 * x := by nlinarith [sq_nonneg x, hx, ha0.le]
  have hroot : x ≤ Real.sqrt (x^2 + a0 * x) := by
    exact (Real.le_sqrt hx hy).2 (by nlinarith [sq_nonneg x, hx, ha0.le])
  linarith

/-- The dark acceleration ceiling: phi(x) <= a0/2 for every baryon field. -/
theorem phantom_ceiling (a0 x : ℝ) (ha0 : 0 < a0) (hx : 0 ≤ x) :
    phi a0 x ≤ a0 / 2 := by
  have hnn : 0 ≤ x^2 + a0 * x := by
    nlinarith [sq_nonneg x, hx, ha0.le]
  have hnon2 : 0 ≤ x + a0 / 2 := by nlinarith [hx, ha0.le]
  have hroot : Real.sqrt (x^2 + a0 * x) ≤ x + a0 / 2 := by
    have h1 : x^2 + a0 * x ≤ (x + a0 / 2)^2 := by
      rw [pow_two]
      ring_nf
      nlinarith [sq_nonneg a0]
    have h2 := Real.sqrt_le_sqrt h1
    rwa [Real.sqrt_sq hnon2] at h2
  unfold phi
  linarith

/-- The ceiling is strictly below a0/2 for every finite baryon field:
the cap is attained only asymptotically. -/
theorem phantom_ceiling_strict (a0 x : ℝ) (ha0 : 0 < a0) (hx : 0 < x) :
    phi a0 x < a0 / 2 := by
  have hnn : 0 ≤ x^2 + a0 * x := by
    nlinarith [sq_nonneg x, hx.le, ha0.le]
  have hnon2 : 0 ≤ x + a0 / 2 := by nlinarith [hx.le, ha0.le]
  have hroot : Real.sqrt (x^2 + a0 * x) < x + a0 / 2 := by
    apply (Real.sqrt_lt hnn hnon2).2
    rw [pow_two]
    ring_nf
    nlinarith [sq_pos_of_pos ha0]
  unfold phi
  linarith

/-- NO-CONTAINMENT: an ambient field at or above the ceiling can never be
matched by the internal phantom of a line-conforming system. -/
theorem phantom_never_attains_half (a0 ge : ℝ) (ha0 : 0 < a0) (hge : a0 / 2 ≤ ge) :
    ∀ x : ℝ, 0 ≤ x → phi a0 x ≠ ge := by
  intro x hx
  by_cases hx0 : x = 0
  · subst x
    rw [phantom_zero a0 ha0]
    nlinarith [ha0]
  · have hpos : 0 < x := lt_of_le_of_ne hx (Ne.symm hx0)
    have hlt : phi a0 x < a0 / 2 := phantom_ceiling_strict a0 x ha0 hpos
    exact ne_of_lt (lt_of_lt_of_le hlt hge)

/-- THE APPROACH LAW: for g_bar >= a0/8 the phantom sits in the band
[a0/2 - a0^2/(8 g_bar), a0/2). -/
theorem phantom_approach_lower (a0 g : ℝ) (ha0 : 0 < a0) (hg : a0 / 8 ≤ g) :
    a0 / 2 - a0^2 / (8 * g) ≤ phi a0 g := by
  have hgpos : 0 < g := by nlinarith [ha0, hg]
  by_cases hb : a0 / 2 - a0^2 / (8 * g) ≤ 0
  · linarith [phantom_nonneg a0 g ha0 hgpos.le, hb]
  · have hbpos : 0 < a0 / 2 - a0^2 / (8 * g) := lt_of_not_ge hb
    have hu : 0 ≤ g + a0 / 2 - a0^2 / (8 * g) := by nlinarith [hbpos, hgpos.le]
    have hnn : 0 ≤ g^2 + a0 * g := by
      nlinarith [sq_nonneg g, hgpos.le, ha0.le]
    have hsq : (g + a0 / 2 - a0^2 / (8 * g))^2 ≤ g^2 + a0 * g := by
      field_simp [hgpos.ne', ha0.ne']
      ring_nf
      have h8 : 0 ≤ 8 * g - a0 := by nlinarith [hg]
      have hpow : 0 ≤ a0^3 := by positivity
      nlinarith [mul_nonneg hpow h8]
    have hsq2 : (g + a0 / 2 - a0^2 / (8 * g))^2 ≤ (Real.sqrt (g^2 + a0 * g))^2 := by
      rwa [← Real.sq_sqrt hnn] at hsq
    have habs : |g + a0 / 2 - a0^2 / (8 * g)| ≤ |Real.sqrt (g^2 + a0 * g)| :=
      sq_le_sq.mp hsq2
    have hroot : g + a0 / 2 - a0^2 / (8 * g) ≤ Real.sqrt (g^2 + a0 * g) := by
      simpa [abs_of_nonneg hu, abs_of_nonneg (Real.sqrt_nonneg _)] using habs
    unfold phi
    linarith

/-- CONTAINMENT INVERSE (exact): for 0 < ge < a0/2 the phantom equals ge
exactly at the baryon field ge^2/(a0 - 2 ge). -/
theorem phantom_cont_inverse (a0 ge : ℝ) (ha0 : 0 < a0) (hg : 0 < ge)
    (hge : ge < a0 / 2) :
    phi a0 (cont_field a0 ge) = ge := by
  have hden : a0 - 2 * ge ≠ 0 := by linarith
  have hdenp : 0 < a0 - 2 * ge := by linarith
  have hxpos : 0 ≤ cont_field a0 ge := by
    unfold cont_field
    exact div_nonneg (sq_nonneg ge) hdenp.le
  have hnn : 0 ≤ (cont_field a0 ge)^2 + a0 * cont_field a0 ge := by
    nlinarith [sq_nonneg (cont_field a0 ge), hxpos, ha0.le]
  have hRpos : 0 < ge * (a0 - ge) / (a0 - 2 * ge) := by
    exact div_pos (mul_pos hg (by linarith : 0 < a0 - ge)) hdenp
  have hprod : (cont_field a0 ge)^2 + a0 * cont_field a0 ge
        = (ge * (a0 - ge) / (a0 - 2 * ge))^2 := by
    unfold cont_field
    field_simp [hden]
    ring
  have hsq : (Real.sqrt ((cont_field a0 ge)^2 + a0 * cont_field a0 ge))^2
        = (ge * (a0 - ge) / (a0 - 2 * ge))^2 := by
    rw [Real.sq_sqrt hnn, hprod]
  rcases eq_or_eq_neg_of_sq_eq_sq
      (Real.sqrt ((cont_field a0 ge)^2 + a0 * cont_field a0 ge))
      (ge * (a0 - ge) / (a0 - 2 * ge)) hsq with hpos | hneg
  · unfold phi
    rw [hpos]
    unfold cont_field
    field_simp [hden]
    have hd2 : a0 - ge * 2 ≠ 0 := by simpa [mul_comm] using hden
    rw [div_eq_iff hd2]
    ring
  · exfalso
    have hcontra : 0 ≤ -(ge * (a0 - ge) / (a0 - 2 * ge)) := by
      rw [← hneg]
      exact Real.sqrt_nonneg _
    nlinarith [hRpos, hcontra]

/-- CONTAINMENT RADIUS (algebraic core): where the baryon field is the
containment field, r^2 = G M (a0 - 2 ge)/ge^2 (deep-MOND limit:
r_t ~ sqrt(G M a0)/ge). -/
theorem phantom_cont_radius (a0 G M ge r : ℝ) (_ha0 : 0 < a0) (_hG : 0 < G)
    (_hM : 0 < M) (hg : 0 < ge) (hge : ge < a0 / 2) (hr : 0 < r)
    (hgb : G * M / r^2 = cont_field a0 ge) :
    r^2 = G * M * (a0 - 2 * ge) / ge^2 := by
  unfold cont_field at hgb
  have hden : a0 - 2 * ge ≠ 0 := by linarith
  have hgbm : G * M * (a0 - 2 * ge) = r^2 * ge^2 := by
    have h1 := congrArg (fun t : ℝ => t * (r^2 * (a0 - 2 * ge))) hgb
    field_simp [hr.ne', hg.ne', hden] at h1
    exact h1
  exact (eq_div_iff (pow_ne_zero 2 (ne_of_gt hg))).2 hgbm.symm

/-- MONOTONICITY: the phantom boost rises with the baryon field — the
framework's phantom never overshoots its ceiling. -/
theorem phantom_mono (a0 x y : ℝ) (ha0 : 0 < a0) (hx : 0 < x) (hy : 0 < y)
    (hxy : x ≤ y) :
    phi a0 x ≤ phi a0 y := by
  have hnnX : 0 ≤ x^2 + a0 * x := by nlinarith [sq_nonneg x, hx.le, ha0.le]
  have hnnY : 0 ≤ y^2 + a0 * y := by nlinarith [sq_nonneg y, hy.le, ha0.le]
  have hrecX : phi a0 x = a0 * x / (Real.sqrt (x^2 + a0 * x) + x) := by
    apply eq_div_of_mul_eq
    · exact ne_of_gt (by positivity : 0 < Real.sqrt (x^2 + a0 * x) + x)
    · simpa [mul_comm] using phantom_product a0 x ha0 hx.le
  have hrecY : phi a0 y = a0 * y / (Real.sqrt (y^2 + a0 * y) + y) := by
    apply eq_div_of_mul_eq
    · exact ne_of_gt (by positivity : 0 < Real.sqrt (y^2 + a0 * y) + y)
    · simpa [mul_comm] using phantom_product a0 y ha0 hy.le
  rw [hrecX, hrecY]
  have hposX : 0 < Real.sqrt (x^2 + a0 * x) + x := by positivity
  have hposY : 0 < Real.sqrt (y^2 + a0 * y) + y := by positivity
  have hcross : x * (Real.sqrt (y^2 + a0 * y) + y) ≤ y * (Real.sqrt (x^2 + a0 * x) + x) := by
    have hroot : x * Real.sqrt (y^2 + a0 * y) ≤ y * Real.sqrt (x^2 + a0 * x) := by
      have hsq2 : (x * Real.sqrt (y^2 + a0 * y))^2 ≤ (y * Real.sqrt (x^2 + a0 * x))^2 := by
        rw [mul_pow, mul_pow, Real.sq_sqrt hnnY, Real.sq_sqrt hnnX]
        have hm : a0 * x^2 * y ≤ a0 * x * y^2 := by
          calc
            a0 * x^2 * y = (a0 * x * y) * x := by ring
            _ ≤ (a0 * x * y) * y :=
              mul_le_mul_of_nonneg_left hxy (mul_nonneg (mul_nonneg ha0.le hx.le) hy.le)
            _ = a0 * x * y^2 := by ring
        nlinarith [hm]
      have habs : |x * Real.sqrt (y^2 + a0 * y)| ≤ |y * Real.sqrt (x^2 + a0 * x)| :=
        sq_le_sq.mp hsq2
      have hnx : 0 ≤ x * Real.sqrt (y^2 + a0 * y) := mul_nonneg hx.le (Real.sqrt_nonneg _)
      have hny : 0 ≤ y * Real.sqrt (x^2 + a0 * x) := mul_nonneg hy.le (Real.sqrt_nonneg _)
      simpa [abs_of_nonneg hnx, abs_of_nonneg hny] using habs
    nlinarith [hroot]
  have hdiv : x / (Real.sqrt (x^2 + a0 * x) + x) ≤ y / (Real.sqrt (y^2 + a0 * y) + y) := by
    rw [div_le_iff₀ hposX]
    rw [mul_comm (y / (Real.sqrt (y^2 + a0 * y) + y)) (Real.sqrt (x^2 + a0 * x) + x)]
    rw [← mul_div_assoc]
    rw [le_div_iff₀ hposY]
    simpa [mul_comm, mul_left_comm, mul_assoc] using hcross
  simpa [div_eq_mul_inv, mul_assoc] using mul_le_mul_of_nonneg_left hdiv ha0.le

end

#print axioms phantom_product
#print axioms phantom_zero
#print axioms phantom_nonneg
#print axioms phantom_ceiling
#print axioms phantom_ceiling_strict
#print axioms phantom_never_attains_half
#print axioms phantom_approach_lower
#print axioms phantom_cont_inverse
#print axioms phantom_cont_radius
#print axioms phantom_mono