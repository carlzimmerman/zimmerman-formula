import Mathlib

/-!
# AS024 — No cosmological prediction from an inverted datum: certificate

Algebraic core of the anti-circularity audit.  The framework scale identity
(adopted input, kappa = 1/2):

    a0 = F(rho) = (c/2) * sqrt(G * rho)          [rho = mass density, kg/m^3]
    rho_inv(a)  = 4 a^2 / (G c^2)                [inverse map]
    Lambda_inv(a) = 32 pi a^2 / c^4              [same-G Einstein reading]
    Omega_inv(a,H0) = 32 pi a^2 / (3 H0^2 c^2)   [requires an independent H0]

Certified here (real arithmetic, all variables positive where stated):

  T1  involution_right :  F(rho_inv(a)) = a            (a >= 0)
  T2  involution_left  :  rho_inv(F(rho)) = rho        (rho >= 0)
  T3  ratio_squared    :  Lambda_inv(a)/Lambda(rho) = (a / F(rho))^2  (a,rho > 0)
                          i.e. the Lambda-inversion is the FORWARD residual
                          squared -- one datum, re-expressed, zero new evidence.
  T4  inverse_log_elasticity :  rho_inv'(a) * a / rho_inv(a) = 2
                          the inverted density doubles fractional input errors.
  T5  forward_homogeneity : F(lambda*rho)/F(rho) = sqrt(lambda)
                          the 1/2-power scaling of the forward map.
  T6  omega_inv_strict_mono :  a1 < a2  ->  Omega_inv(a1) < Omega_inv(a2)
                          the 'derived' cosmological output is strictly
                          increasing in the input datum: any conclusion read
                          off Omega_inv is a restatement of the input choice
                          (the negative-control content of C4/C10).

All theorems carry explicit positivity hypotheses on G and c (and H0 for T6)
because the physical constants are positive; nothing else is assumed.
-/

namespace AS024

noncomputable section

open Real

-- T1 ---------------------------------------------------------------------
theorem involution_right {G c : ℝ} (hG : 0 < G) (hc : 0 < c) :
    ∀ a : ℝ, 0 ≤ a → (c / 2) * Real.sqrt (G * (4 * a ^ 2 / (G * c ^ 2))) = a := by
  intro a ha
  have hGc2pos : 0 < G * c ^ 2 := by positivity
  have hGc2 : G * c ^ 2 ≠ 0 := ne_of_gt hGc2pos
  have hmul : G * (4 * a ^ 2 / (G * c ^ 2)) = 4 * a ^ 2 / c ^ 2 := by
    field_simp [hG.ne']
  rw [hmul]
  rw [show 4 * a ^ 2 = (2 * a) ^ 2 by ring]
  rw [Real.sqrt_div (by positivity : 0 ≤ (2 * a) ^ 2) (c ^ 2)]
  rw [Real.sqrt_sq (by positivity : 0 ≤ 2 * a)]
  rw [Real.sqrt_sq (le_of_lt hc)]
  field_simp [hc.ne']

-- T2 ---------------------------------------------------------------------
theorem involution_left {G c : ℝ} (hG : 0 < G) (hc : 0 < c) :
    ∀ ρ : ℝ, 0 ≤ ρ → 4 * ((c / 2) * Real.sqrt (G * ρ)) ^ 2 / (G * c ^ 2) = ρ := by
  intro ρ hρ
  have hGc2 : G * c ^ 2 ≠ 0 := ne_of_gt (by positivity)
  have hsq : ((c / 2) * Real.sqrt (G * ρ)) ^ 2 = c ^ 2 * (G * ρ) / 4 := by
    rw [mul_pow]
    rw [show Real.sqrt (G * ρ) ^ 2 = Real.sqrt (G * ρ) * Real.sqrt (G * ρ) by ring]
    rw [Real.mul_self_sqrt (by positivity : 0 ≤ G * ρ)]
    ring
  rw [hsq]
  field_simp [hGc2]

-- T3 ---------------------------------------------------------------------
theorem ratio_squared {G c : ℝ} (hG : 0 < G) (hc : 0 < c) :
    ∀ a ρ : ℝ, 0 < a → 0 < ρ →
      ((32 * Real.pi * a ^ 2) / c ^ 4) / ((8 * Real.pi * G * ρ) / c ^ 2)
        = (a / ((c / 2) * Real.sqrt (G * ρ))) ^ 2 := by
  intro a ρ ha hρ
  have hGc2 : G * c ^ 2 ≠ 0 := ne_of_gt (by positivity)
  have hden_ne : (c / 2) * Real.sqrt (G * ρ) ≠ 0 := by
    apply mul_ne_zero
    · positivity
    · exact ne_of_gt (Real.sqrt_pos.2 (by positivity : 0 < G * ρ))
  have hden : ((c / 2) * Real.sqrt (G * ρ)) ^ 2 = c ^ 2 * (G * ρ) / 4 := by
    rw [mul_pow]
    rw [show Real.sqrt (G * ρ) ^ 2 = Real.sqrt (G * ρ) * Real.sqrt (G * ρ) by ring]
    rw [Real.mul_self_sqrt (by positivity : 0 ≤ G * ρ)]
    ring
  rw [div_pow]
  rw [hden]
  field_simp [hGc2, hden_ne, Real.pi_ne_zero]; norm_num

-- T4 ---------------------------------------------------------------------
theorem inverse_log_elasticity {G c : ℝ} (hG : 0 < G) (hc : 0 < c) :
    ∀ a : ℝ, 0 < a →
      deriv (fun x : ℝ => 4 * x ^ 2 / (G * c ^ 2)) a * a / (4 * a ^ 2 / (G * c ^ 2)) = 2 := by
  intro a ha
  have hGc2 : G * c ^ 2 ≠ 0 := ne_of_gt (by positivity)
  have hpow : HasDerivAt (fun x : ℝ => x ^ 2) (2 * a) a := by
    simpa [show (2 - 1 : ℕ) = 1 by norm_num] using (hasDerivAt_pow (n := 2) (x := a))
  have hf : (fun x : ℝ => (4 / (G * c ^ 2)) * x ^ 2) = (fun x : ℝ => 4 * x ^ 2 / (G * c ^ 2)) := by
    funext x
    ring
  have hsc : HasDerivAt (fun x : ℝ => (4 / (G * c ^ 2)) * x ^ 2) ((4 / (G * c ^ 2)) * (2 * a)) a :=
    hpow.const_mul (4 / (G * c ^ 2))
  have hsc' : HasDerivAt (fun x : ℝ => 4 * x ^ 2 / (G * c ^ 2)) ((4 / (G * c ^ 2)) * (2 * a)) a := by
    simpa [hf] using hsc
  have hy : (4 / (G * c ^ 2)) * (2 * a) = 8 * a / (G * c ^ 2) := by ring
  have hd : deriv (fun x : ℝ => 4 * x ^ 2 / (G * c ^ 2)) a = 8 * a / (G * c ^ 2) := by
    simpa [hy] using hsc'.deriv
  rw [hd]
  field_simp [hGc2, ha.ne']; norm_num

-- T5 ---------------------------------------------------------------------
theorem forward_homogeneity {G c : ℝ} (hG : 0 < G) (hc : 0 < c) :
    ∀ ρ l : ℝ, 0 < ρ → 0 < l →
      ((c / 2) * Real.sqrt (G * (l * ρ))) / ((c / 2) * Real.sqrt (G * ρ)) = Real.sqrt l := by
  intro ρ l hρ hl
  have hsqrt_ne : Real.sqrt (G * ρ) ≠ 0 :=
    ne_of_gt (Real.sqrt_pos.2 (by positivity : 0 < G * ρ))
  have hc2_ne : c / 2 ≠ 0 := by positivity
  rw [show G * (l * ρ) = l * (G * ρ) by ring]
  rw [Real.sqrt_mul (le_of_lt hl) (G * ρ)]
  field_simp [hsqrt_ne, hc2_ne]

-- T6 ---------------------------------------------------------------------
theorem omega_inv_strict_mono {c H0 : ℝ} (hc : 0 < c) (hH : 0 < H0) :
    ∀ {a1 a2 : ℝ}, 0 ≤ a1 → a1 < a2 →
      (32 * Real.pi * a1 ^ 2) / (3 * H0 ^ 2 * c ^ 2)
        < (32 * Real.pi * a2 ^ 2) / (3 * H0 ^ 2 * c ^ 2) := by
  intro a1 a2 ha1 hlt
  have hd : 3 * H0 ^ 2 * c ^ 2 ≠ 0 := ne_of_gt (by positivity)
  have hcst : 0 < (32 * Real.pi) / (3 * H0 ^ 2 * c ^ 2) := by positivity
  have hd' : 0 < a2 - a1 := sub_pos.mpr hlt
  have hs' : 0 < a2 + a1 := by linarith
  have hf : 0 < (a2 - a1) * (a2 + a1) := mul_pos hd' hs'
  have hprod : (a2 - a1) * (a2 + a1) = a2 ^ 2 - a1 ^ 2 := by ring
  have hdiff : 0 < a2 ^ 2 - a1 ^ 2 := by simpa [hprod] using hf
  have hsq : a1 ^ 2 < a2 ^ 2 := lt_of_sub_pos hdiff
  have hmain : ((32 * Real.pi) / (3 * H0 ^ 2 * c ^ 2)) * a1 ^ 2
        < ((32 * Real.pi) / (3 * H0 ^ 2 * c ^ 2)) * a2 ^ 2 :=
    mul_lt_mul_of_pos_left hsq hcst
  calc
    (32 * Real.pi * a1 ^ 2) / (3 * H0 ^ 2 * c ^ 2)
        = ((32 * Real.pi) / (3 * H0 ^ 2 * c ^ 2)) * a1 ^ 2 := by
            field_simp [hd]
    _ < ((32 * Real.pi) / (3 * H0 ^ 2 * c ^ 2)) * a2 ^ 2 := hmain
    _ = (32 * Real.pi * a2 ^ 2) / (3 * H0 ^ 2 * c ^ 2) := by
            field_simp [hd]

end

end AS024
#print axioms AS024.involution_right
#print axioms AS024.involution_left
#print axioms AS024.ratio_squared
#print axioms AS024.inverse_log_elasticity
#print axioms AS024.forward_homogeneity
#print axioms AS024.omega_inv_strict_mono
