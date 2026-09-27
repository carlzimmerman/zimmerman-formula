import Mathlib
open Real

/- G2a: linear substitution step -/
theorem step1_gen (r : ℝ) (hr : r ≠ 0) (F : ℝ → ℝ) :
    ∫ mu in (-1:ℝ)..1, F (r * mu) = (1/r) * ∫ v in (-r:ℝ)..r, F v := by
  rw [intervalIntegral.integral_comp_mul_left F hr, smul_eq_mul, inv_eq_one_div, mul_neg_one, mul_one]

theorem step1 (r : ℝ) (hr : 0 < r) (H : ℝ → ℝ → ℝ) :
    ∫ mu in (-1:ℝ)..1, H (r * Real.sqrt (1 - mu ^ 2)) (r * mu)
      = (1/r) * ∫ v in (-r:ℝ)..r, H (Real.sqrt (r ^ 2 - v ^ 2)) v := by
  have hsqrt : ∀ mu : ℝ, Real.sqrt (r ^ 2 - (r * mu) ^ 2) = r * Real.sqrt (1 - mu ^ 2) := by
    intro mu
    rw [show r ^ 2 - (r * mu) ^ 2 = r ^ 2 * (1 - mu ^ 2) from by ring,
        Real.sqrt_mul (sq_nonneg r) (1 - mu ^ 2), Real.sqrt_sq_eq_abs,
        abs_eq_self.mpr hr.le]
  have key := step1_gen r (ne_of_gt hr) (fun v => H (Real.sqrt (r ^ 2 - v ^ 2)) v)
  simp only [show ∀ mu : ℝ, H (r * Real.sqrt (1 - mu ^ 2)) (r * mu)
      = H (Real.sqrt (r ^ 2 - (r * mu) ^ 2)) (r * mu) from by
      intro mu; rw [hsqrt mu]]
  exact key


noncomputable def chordVol (r mu : ℝ) : ℝ := r * mu + Real.sqrt (1 - r ^ 2 * (1 - mu ^ 2))

noncomputable def covStatement (H : ℝ → ℝ → ℝ) : Prop :=
  3 * ∫ r in (0:ℝ)..1, r ^ 2 * (1 / 2 * ∫ mu in (-1:ℝ)..1, H (r * Real.sqrt (1 - mu ^ 2)) (r * mu))
    = (3/2) * ∫ u in (0:ℝ)..1, ∫ v in -(Real.sqrt (1 - u ^ 2))..(Real.sqrt (1 - u ^ 2)), u * H u v

theorem chord_cond (cov : ∀ H : ℝ → ℝ → ℝ,
    Continuous (fun p : ℝ × ℝ => H p.1 p.2) → covStatement H) :
    3 * (∫ r in (0:ℝ)..1, r ^ 2 * (1 / 2 * (∫ mu in (-1:ℝ)..1, chordVol r mu))) = 3/4 := by
  have inst : covStatement (fun u v => v + Real.sqrt (1 - u ^ 2)) := cov _ (by fun_prop)
  simp only [covStatement] at inst
  have hmucongr : ∀ r : ℝ, Set.EqOn (fun mu : ℝ => chordVol r mu)
      (fun mu : ℝ => (r * mu) + Real.sqrt (1 - (r * Real.sqrt (1 - mu ^ 2)) ^ 2))
      (Set.uIcc (-(1:ℝ)) 1) := by
    intro r mu hmu
    simp only [chordVol]
    have hb : mu ∈ Set.Icc (-(1:ℝ)) 1 := by
      rw [← Set.uIcc_of_le (by norm_num : (-(1:ℝ)) ≤ 1)]
      exact hmu
    have h1 : (-(1:ℝ)) ≤ mu := hb.1
    have h2 : mu ≤ 1 := hb.2
    rw [mul_pow, sq_sqrt (by nlinarith [sq_nonneg mu, h1, h2])]
  rw [intervalIntegral.integral_congr (show Set.EqOn
      (fun r : ℝ => r ^ 2 * (1 / 2 * ∫ mu in (-1:ℝ)..1, chordVol r mu))
      (fun r : ℝ => r ^ 2 * (1 / 2 * ∫ mu in (-1:ℝ)..1,
        (r * mu) + Real.sqrt (1 - (r * Real.sqrt (1 - mu ^ 2)) ^ 2)))
      (Set.uIcc (0:ℝ) 1) from by
      intro r hr
      exact congrArg (fun X : ℝ => r ^ 2 * (1 / 2 * X))
        (intervalIntegral.integral_congr (hmucongr r)))]
  rw [inst]
  rw [intervalIntegral.integral_congr (show Set.EqOn
      (fun u => ∫ v in -(Real.sqrt (1 - u ^ 2))..Real.sqrt (1 - u ^ 2),
        u * (v + Real.sqrt (1 - u ^ 2)))
      (fun u => 2 * u * (1 - u ^ 2)) (Set.uIcc (0:ℝ) 1) from by
      intro u hu
      have hu2 : u ∈ Set.Icc (0:ℝ) 1 := by
        rw [← Set.uIcc_of_le (by norm_num : (0:ℝ) ≤ 1)]
        exact hu
      have hs : 0 ≤ 1 - u ^ 2 := by
        have h1 : (0:ℝ) ≤ u := hu2.1
        have h2 : u ≤ 1 := hu2.2
        nlinarith [sq_nonneg u]
      show (∫ v in -(Real.sqrt (1 - u ^ 2))..Real.sqrt (1 - u ^ 2),
        u * (v + Real.sqrt (1 - u ^ 2))) = 2 * u * (1 - u ^ 2)
      have h2 : 2 * u * Real.sqrt (1 - u ^ 2) ^ 2 = 2 * u * (1 - u ^ 2) := by
        rw [Real.sq_sqrt hs]
      simp only [show ∀ v : ℝ, u * (v + Real.sqrt (1 - u ^ 2))
        = (u * Real.sqrt (1 - u ^ 2)) + u * v ^ 1 from by intro v; ring]
      rw [intervalIntegral.integral_add (f := fun v => u * Real.sqrt (1 - u ^ 2))
        (g := fun v => u * v ^ 1)
        (Continuous.intervalIntegrable (by fun_prop) _ _)
        (Continuous.intervalIntegrable (by fun_prop) _ _)]
      simp only [intervalIntegral.integral_const_mul, intervalIntegral.integral_const,
        integral_pow, smul_eq_mul]
      ring_nf
      linear_combination h2)]
  simp only [show ∀ u : ℝ, (2 * u * (1 - u ^ 2)) = (2:ℝ) * u ^ 1 + (-2:ℝ) * u ^ 3 from by intro u; ring]
  rw [intervalIntegral.integral_add (f := fun u => (2:ℝ)*u^1) (g := fun u => (-2:ℝ)*u^3)
      (Continuous.intervalIntegrable (by fun_prop) _ _)
      (Continuous.intervalIntegrable (by fun_prop) _ _),
      intervalIntegral.integral_const_mul, intervalIntegral.integral_const_mul,
      integral_pow, integral_pow]
  norm_num


theorem val_I1 : ∫ u in (0:ℝ)..1, ((1:ℝ) * u ^ 1 + (1:ℝ) * u ^ 3 + (-2:ℝ) * u ^ 5) = ((5:ℚ)/12 : ℝ) := by
  rw [intervalIntegral.integral_add (f := fun u => (1:ℝ)*u^1 + (1:ℝ)*u^3) (g := fun u => (-2:ℝ)*u^5)
      (Continuous.intervalIntegrable (by fun_prop) _ _)
      (Continuous.intervalIntegrable (by fun_prop) _ _)]
  rw [intervalIntegral.integral_add (f := fun u => (1:ℝ)*u^1) (g := fun u => (1:ℝ)*u^3)
      (Continuous.intervalIntegrable (by fun_prop) _ _)
      (Continuous.intervalIntegrable (by fun_prop) _ _),
      intervalIntegral.integral_const_mul, intervalIntegral.integral_const_mul,
      intervalIntegral.integral_const_mul, integral_pow, integral_pow, integral_pow]
  norm_num


theorem outer_I1val : ∫ x in (0:ℝ)..1,
    ((2/3:ℝ) * x ^ 1 + (2/3:ℝ) * x ^ 3 + (-4/3:ℝ) * x ^ 5) = ((5:ℚ)/18 : ℝ) := by
  rw [intervalIntegral.integral_add (f := fun x => (2/3:ℝ)*x^1 + (2/3:ℝ)*x^3)
      (g := fun x => (-4/3:ℝ)*x^5)
      (Continuous.intervalIntegrable (by fun_prop) _ _)
      (Continuous.intervalIntegrable (by fun_prop) _ _)]
  rw [intervalIntegral.integral_add (f := fun x => (2/3:ℝ)*x^1) (g := fun x => (2/3:ℝ)*x^3)
      (Continuous.intervalIntegrable (by fun_prop) _ _)
      (Continuous.intervalIntegrable (by fun_prop) _ _),
      intervalIntegral.integral_const_mul, intervalIntegral.integral_const_mul,
      intervalIntegral.integral_const_mul, integral_pow, integral_pow, integral_pow]
  norm_num

theorem I1_cond (cov : ∀ H : ℝ → ℝ → ℝ,
    Continuous (fun p : ℝ × ℝ => H p.1 p.2) → covStatement H) :
    3 * (∫ r in (0:ℝ)..1, r ^ 2 * (1 / 2 * (∫ mu in (-1:ℝ)..1,
        (r * Real.sqrt (1 - mu ^ 2)) ^ 2 * (Real.sqrt (1 - (r * Real.sqrt (1 - mu ^ 2)) ^ 2) - r * mu)
        + ((Real.sqrt (1 - (r * Real.sqrt (1 - mu ^ 2)) ^ 2)) ^ 3 - (r * mu) ^ 3) / 3))) = 5/12 := by
  have inst : covStatement (fun u v => u ^ 2 * (Real.sqrt (1 - u ^ 2) - v)
      + ((Real.sqrt (1 - u ^ 2)) ^ 3 - v ^ 3) / 3) :=
    cov _ (by show Continuous (fun p : ℝ × ℝ => p.1 ^ 2 * (Real.sqrt (1 - p.1 ^ 2) - p.2)
      + ((Real.sqrt (1 - p.1 ^ 2)) ^ 3 - p.2 ^ 3) / 3); fun_prop)
  simp only [covStatement] at inst
  rw [inst]
  rw [intervalIntegral.integral_congr (show Set.EqOn
      (fun u => ∫ v in -(Real.sqrt (1 - u ^ 2))..Real.sqrt (1 - u ^ 2),
        u * (u ^ 2 * (Real.sqrt (1 - u ^ 2) - v) + ((Real.sqrt (1 - u ^ 2)) ^ 3 - v ^ 3) / 3))
      (fun u => 2 * u ^ 3 * (1 - u ^ 2) + (2/3) * u * (1 - u ^ 2) ^ 2) (Set.uIcc (0:ℝ) 1) from by
      intro u hu
      have hu2 : u ∈ Set.Icc (0:ℝ) 1 := by
        rw [← Set.uIcc_of_le (by norm_num : (0:ℝ) ≤ 1)]
        exact hu
      have hs : 0 ≤ 1 - u ^ 2 := by
        have h1 : (0:ℝ) ≤ u := hu2.1
        have h2 : u ≤ 1 := hu2.2
        nlinarith [sq_nonneg u]
      show (∫ v in -(Real.sqrt (1 - u ^ 2))..Real.sqrt (1 - u ^ 2),
        u * (u ^ 2 * (Real.sqrt (1 - u ^ 2) - v) + ((Real.sqrt (1 - u ^ 2)) ^ 3 - v ^ 3) / 3))
        = 2 * u ^ 3 * (1 - u ^ 2) + (2/3) * u * (1 - u ^ 2) ^ 2
      have hs2 : Real.sqrt (1 - u ^ 2) ^ 2 = 1 - u ^ 2 := Real.sq_sqrt hs
      have h4 : Real.sqrt (1 - u ^ 2) ^ 4 = (1 - u ^ 2) ^ 2 := by
        rw [show (Real.sqrt (1 - u ^ 2)) ^ 4
          = (Real.sqrt (1 - u ^ 2)) ^ 2 * (Real.sqrt (1 - u ^ 2)) ^ 2 from by ring, hs2]
        ring
      have h2 : 2 * u ^ 3 * Real.sqrt (1 - u ^ 2) ^ 2 + (2/3) * u * Real.sqrt (1 - u ^ 2) ^ 4
          = 2 * u ^ 3 * (1 - u ^ 2) + (2/3) * u * (1 - u ^ 2) ^ 2 := by
        rw [hs2, h4]
      simp only [show ∀ v : ℝ, u * (u ^ 2 * (Real.sqrt (1 - u ^ 2) - v)
          + ((Real.sqrt (1 - u ^ 2)) ^ 3 - v ^ 3) / 3)
        = (u ^ 3 * Real.sqrt (1 - u ^ 2) + u * (Real.sqrt (1 - u ^ 2)) ^ 3 / 3)
          + (-(u ^ 3)) * v ^ 1 + (-(u / 3)) * v ^ 3 from by intro v; ring]
      rw [intervalIntegral.integral_add
        (f := fun v => (u ^ 3 * Real.sqrt (1 - u ^ 2) + u * (Real.sqrt (1 - u ^ 2)) ^ 3 / 3)
          + (-(u ^ 3)) * v ^ 1)
        (g := fun v => (-(u / 3)) * v ^ 3)
        (Continuous.intervalIntegrable (by fun_prop) _ _)
        (Continuous.intervalIntegrable (by fun_prop) _ _)]
      rw [intervalIntegral.integral_add
        (f := fun v => (u ^ 3 * Real.sqrt (1 - u ^ 2) + u * (Real.sqrt (1 - u ^ 2)) ^ 3 / 3))
        (g := fun v => (-(u ^ 3)) * v ^ 1)
        (Continuous.intervalIntegrable (by fun_prop) _ _)
        (Continuous.intervalIntegrable (by fun_prop) _ _)]
      simp only [intervalIntegral.integral_const, intervalIntegral.integral_const_mul,
        integral_pow, smul_eq_mul]
      ring_nf
      linear_combination h2)]
  simp only [show ∀ x : ℝ, (2 * x ^ 3 * (1 - x ^ 2) + (2/3) * x * (1 - x ^ 2) ^ 2)
      = (2/3:ℝ) * x ^ 1 + (2/3:ℝ) * x ^ 3 + (-4/3:ℝ) * x ^ 5 from by intro x; ring]
  rw [outer_I1val]
  ring

#print axioms chord_cond
#print axioms I1_cond

#print axioms step1
#print axioms chord_cond
#print axioms I1_cond
