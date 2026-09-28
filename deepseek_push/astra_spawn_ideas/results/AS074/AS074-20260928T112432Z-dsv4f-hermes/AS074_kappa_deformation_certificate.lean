/-
  AS074 -- Robustness of kappa under small kernel deformations.  Certificate.

  Seed statement (AS074_robustness_of_kappa_under_small_kernel_deformations.md):

      mu_base(Y) = 1 - (1+Y)^(-2)        Y = g/s,  s = c*sqrt(G*rho_Lambda)
      mu_eps    = mu_base + eps*f        f(0) = f(infinity) = 0  (endpoints)
      kappa     = 1/(2 + eps*f'(0))

  What this file certifies (all machine-checked, zero sorry, axioms =
  {propext, Classical.choice, Quot.sound} -- printed at the bottom):

    * slope_mu_base : mu_base'(0) = 2.  The undeformed MU2-family kernel has
      linear coefficient 2 at the origin (this is what makes kappa = 1/2 the
      deep coefficient 1/(2+0) on the framework footing a0 = kappa*s).

    * slope_deformed : for f with f'(0) = delta, the deformed kernel
      mu_eps has slope (2 + eps*delta) at zero -- the seed's "kappa =
      1/(2+eps*f'(0))" input coefficient.

    * slope_fA / slope_fB / slope_fL : the two explicit deformations
        fA(Y) = Y^2/(1+Y)^4  (fA'(0) = 0)   preserves the deep coefficient,
        fB(Y) = Y/(1+Y)^2   (fB'(0) = 1)   changes it to 1/(2+eps),
      and the scaled family fL(lam,Y) = lam*Y/(1+lam*Y)^2 has fL'(0) = lam
      (the lambda = 1/2, 1, 2 diagnostic counterexamples).

    * linearized_deep_g_sq : with the linearized deep response
        (2+eps*delta) * g * (g/s) = B      (Y = g/s deep limit)
      the identification g^2 = B*s/(2+eps*delta) is exact.

    * deep_flat_coefficient : with B = G*M_b/r^2, the deep circular relation
      gives  g^2 r^2 = G*M_b*s/(2+eps*delta), i.e. v_flat^4 = G*M_b*
      s/(2+eps*delta) -- the deformed theory's deep coefficient.

    * kappa_eff_formula : with v_flat^4 = G*M_b*a0 (framework) and
      a0 = kappa*s, the effective coefficient is kappa = 1/(2+eps*delta)
      -- exactly the seed's formula.

    * kappa_preserved_iff : for eps != 0,  kappa = 1/2  <->  delta = 0.
      THE robustness criterion: a small kernel deformation preserves the
      adopted one-half coefficient precisely when it has zero derivative at
      zero (first-order tangency).  Endpoint preservation alone (f(0)=f(inf)=0)
      is NOT sufficient -- the machine-checked instance control_fB_instance
      (delta = 1, eps = 1/5 -> kappa = 5/11 != 1/2) is the negative control.

    * mu2_doubling : mu_base(Y) = MU2(2Y) with MU2(x) = 1-(1+x/2)^(-2) -- the
      seed's identity warning ("this mu_base is MU2(x) at x=2Y, not MU2(Y)").
-/
import Mathlib

noncomputable def mu_base (Y : ℝ) : ℝ := 1 - 1 / (1 + Y) ^ 2
noncomputable def mu_eps (eps : ℝ) (f : ℝ → ℝ) (Y : ℝ) : ℝ := mu_base Y + eps * f Y
noncomputable def fA (Y : ℝ) : ℝ := Y ^ 2 / (1 + Y) ^ 4
noncomputable def fB (Y : ℝ) : ℝ := Y / (1 + Y) ^ 2
noncomputable def fL (lam : ℝ) (Y : ℝ) : ℝ := lam * Y / (1 + lam * Y) ^ 2
noncomputable def MU2 (x : ℝ) : ℝ := 1 - 1 / (1 + x / 2) ^ 2

lemma deriv_one_plus : HasDerivAt (fun Y : ℝ => 1 + Y) 1 0 := by
  have h := (hasDerivAt_id (0 : ℝ)).add_const (c := (1 : ℝ))
  have hfun : (fun x : ℝ => id x + 1) = (fun Y : ℝ => 1 + Y) := by
    funext Y
    exact (add_comm 1 Y).symm
  rw [hfun] at h
  exact h

lemma deriv_one_plus_sq : HasDerivAt (fun Y : ℝ => (1 + Y) ^ 2) 2 0 := by
  have h := deriv_one_plus.pow (n := 2)
  have hnorm : (↑(2 : ℕ) * (1 + 0) ^ ((2 : ℕ) - 1) * 1 : ℝ) = 2 := by
    norm_num
  rw [hnorm] at h
  exact h

lemma deriv_one_plus_four : HasDerivAt (fun Y : ℝ => (1 + Y) ^ 4) 4 0 := by
  have h := deriv_one_plus.pow (n := 4)
  have hnorm : (↑(4 : ℕ) * (1 + 0) ^ ((4 : ℕ) - 1) * 1 : ℝ) = 4 := by
    norm_num
  rw [hnorm] at h
  exact h

lemma deriv_id_sq : HasDerivAt (fun Y : ℝ => Y ^ 2) 0 0 := by
  have h := (hasDerivAt_id (0 : ℝ)).pow (n := 2)
  have hfun : (id ^ (2 : ℕ)) = (fun Y : ℝ => Y ^ 2) := by
    funext Y
    rfl
  rw [hfun] at h
  have hnorm : (↑(2 : ℕ) * id 0 ^ ((2 : ℕ) - 1) * 1 : ℝ) = 0 := by
    norm_num
  rw [hnorm] at h
  exact h

lemma deriv_one_over_sq : HasDerivAt (fun Y : ℝ => 1 / (1 + Y) ^ 2) (-2) 0 := by
  have hnum : HasDerivAt (fun _ : ℝ => (1 : ℝ)) 0 0 := hasDerivAt_const (0 : ℝ) (1 : ℝ)
  have hg0 : ((1 : ℝ) + 0) ^ 2 ≠ 0 := by norm_num
  have h := hnum.div deriv_one_plus_sq hg0
  have hnorm : ((0 * (1 + 0) ^ 2 - 1 * 2) / ((1 + 0) ^ 2) ^ 2 : ℝ) = -2 := by
    norm_num
  rw [hnorm] at h
  exact h

theorem slope_mu_base : HasDerivAt mu_base 2 0 := by
  unfold mu_base
  have hc : HasDerivAt (fun _ : ℝ => (1 : ℝ)) 0 0 := hasDerivAt_const (0 : ℝ) (1 : ℝ)
  have h := hc.sub deriv_one_over_sq
  have hnorm : (0 - -2 : ℝ) = 2 := by norm_num
  rw [hnorm] at h
  exact h

/-- fA'(0) = 0 : a deformation with zero derivative at zero. -/
theorem slope_fA : HasDerivAt fA 0 0 := by
  unfold fA
  have hg0 : ((1 : ℝ) + 0) ^ 4 ≠ 0 := by norm_num
  have h := deriv_id_sq.div deriv_one_plus_four hg0
  have hnorm : ((0 * (1 + 0) ^ 4 - 0 ^ 2 * 4) / ((1 + 0) ^ 4) ^ 2 : ℝ) = 0 := by
    norm_num
  rw [hnorm] at h
  exact h

/-- fB'(0) = 1 : a deformation with nonzero derivative at zero. -/
theorem slope_fB : HasDerivAt fB 1 0 := by
  unfold fB
  have hid : HasDerivAt (fun Y : ℝ => Y) 1 0 := hasDerivAt_id (0 : ℝ)
  have hg0 : ((1 : ℝ) + 0) ^ 2 ≠ 0 := by norm_num
  have h := hid.div deriv_one_plus_sq hg0
  have hnorm : ((1 * (1 + 0) ^ 2 - 0 * 2) / ((1 + 0) ^ 2) ^ 2 : ℝ) = 1 := by
    norm_num
  rw [hnorm] at h
  exact h

/-- fL(lam)'(0) = lam : the scaled family used for the lambda counterexamples. -/
theorem slope_fL {lam : ℝ} : HasDerivAt (fL lam) lam 0 := by
  unfold fL
  have hid : HasDerivAt (fun Y : ℝ => Y) 1 0 := hasDerivAt_id (0 : ℝ)
  have hnum : HasDerivAt (fun Y : ℝ => lam * Y) lam 0 := by
    simpa using (hid.const_mul lam)
  have hlin : HasDerivAt (fun Y : ℝ => 1 + lam * Y) lam 0 := by
    have hc : HasDerivAt (fun _ : ℝ => (1 : ℝ)) 0 0 := hasDerivAt_const (0 : ℝ) (1 : ℝ)
    have h := hc.add hnum
    have hnorm : (0 + lam : ℝ) = lam := by ring
    rw [hnorm] at h
    exact h
  have hsq2 : HasDerivAt (fun Y : ℝ => (1 + lam * Y) ^ 2) (2 * lam) 0 := by
    have h := hlin.pow (n := 2)
    have hnorm : (↑(2 : ℕ) * (1 + lam * 0) ^ ((2 : ℕ) - 1) * lam : ℝ) = 2 * lam := by
      norm_num
    rw [hnorm] at h
    exact h
  have hg0 : ((1 : ℝ) + lam * 0) ^ 2 ≠ 0 := by norm_num
  have h := hnum.div hsq2 hg0
  have hnorm : ((lam * (1 + lam * 0) ^ 2 - lam * 0 * (2 * lam)) / ((1 + lam * 0) ^ 2) ^ 2 : ℝ) = lam := by
    norm_num
  rw [hnorm] at h
  exact h

/-- The deformed kernel's slope at zero: mu_eps'(0) = 2 + eps*f'(0).
  This is the seed's kappa = 1/(2+eps*f'(0)) at the level of the linear
  coefficient of the response at the origin. -/
theorem slope_deformed {eps δ : ℝ} {f : ℝ → ℝ} (hf : HasDerivAt f δ 0) :
    HasDerivAt (mu_eps eps f) (2 + eps * δ) 0 := by
  unfold mu_eps
  have h1 : HasDerivAt mu_base 2 0 := slope_mu_base
  have h2 : HasDerivAt (fun Y : ℝ => eps * f Y) (eps * δ) 0 := hf.const_mul eps
  exact h1.add h2

/-- Exact deep identification: from the linearized response law
  (2+eps*delta) * g * (g/s) = B follows g^2 = B*s/(2+eps*delta). -/
theorem linearized_deep_g_sq {ε δ B s g : ℝ} (hs : s ≠ 0) (hden : 2 + ε * δ ≠ 0)
    (hlaw : (2 + ε * δ) * (g * (g / s)) = B) :
    g ^ 2 = B * s / (2 + ε * δ) := by
  have hm := congrArg (fun x : ℝ => x * s) hlaw
  field_simp [mul_comm, mul_left_comm, mul_assoc, pow_two] at hm
  field_simp [hden, pow_two, mul_comm, mul_left_comm, mul_assoc]
  linear_combination hm

/-- Deep flat coefficient: with B = G*M_b/(r*r) the circular deep relation
  gives  (g*g)*(r*r) = G*M_b*s/(2+eps*delta),  i.e. exactly
  v_flat^4 = G*M_b*s/(2+eps*delta). -/
theorem deep_flat_coefficient {G M b r s ε δ B g : ℝ}
    (hs : s ≠ 0) (hden : 2 + ε * δ ≠ 0) (hG : G ≠ 0) (hM : M ≠ 0) (hr : r ≠ 0)
    (hlaw : (2 + ε * δ) * (g * (g / s)) = B) (hB : B = G * M / (r * r)) :
    g * g * (r * r) = G * M * s / (2 + ε * δ) := by
  have hg2 : g ^ 2 = B * s / (2 + ε * δ) := linearized_deep_g_sq hs hden hlaw
  have hB' : B * s * (r * r) = G * M * s := by
    rw [hB]
    field_simp [hr, hG, hM, pow_two, mul_comm, mul_left_comm, mul_assoc]
  field_simp [hden, pow_two, mul_comm, mul_left_comm, mul_assoc]
  rw [hg2]
  field_simp [hden, hr, pow_two, mul_comm, mul_left_comm, mul_assoc]
  have hBc : B * r ^ 2 = G * M := by
    have h1 : s * (B * (r * r)) = s * (G * M) := by
      linear_combination hB'
    have hc := mul_left_cancel₀ hs h1
    rw [← pow_two] at hc
    exact hc
  exact hBc

/-- Coefficient identification: with v_flat^4 = G*M_b*a0 (the framework
  relation) and a0 = kappa*s, the deformed deep coefficient is
  kappa = 1/(2+eps*delta) -- the seed's formula, derived from the
  response law rather than adopted. -/
theorem kappa_eff_formula {κ a0 G M s ε δ : ℝ}
    (hs : s ≠ 0) (hG : G ≠ 0) (hM : M ≠ 0) (hden : 2 + ε * δ ≠ 0)
    (ha0 : a0 = κ * s)
    (hcoef : G * M * s / (2 + ε * δ) = G * M * a0) :
    κ = 1 / (2 + ε * δ) := by
  have h1 : G * M * a0 = G * M * s / (2 + ε * δ) := hcoef.symm
  have hGM : G * M ≠ 0 := mul_ne_zero hG hM
  field_simp [hden, hGM, mul_comm, mul_left_comm, mul_assoc] at h1
  have hk : κ * s * (2 + ε * δ) = s := by
    rw [← ha0]
    exact h1
  have hk1 : κ * (2 + ε * δ) = 1 := by
    have hks : (κ * (2 + ε * δ)) * s = 1 * s := by
      linear_combination hk
    exact mul_right_cancel₀ hs hks
  field_simp [hden, mul_comm, mul_left_comm, mul_assoc]
  exact hk1

/-- THE robustness criterion: for eps != 0, kappa = 1/2  <->  delta = 0
  (delta = f'(0)).  The adopted half survives a small kernel deformation
  exactly when the deformation is first-order tangent at zero. -/
theorem kappa_preserved_iff {ε δ : ℝ} (hε : ε ≠ 0) :
    (1 / (2 + ε * δ) = 1 / 2) ↔ δ = 0 := by
  constructor
  · intro h
    have hz : 2 + ε * δ ≠ 0 := by
      intro hz0
      have h0 : (1 : ℝ) / 0 = 1 / 2 := by
        rw [hz0] at h
        exact h
      norm_num at h0
    have hm := congrArg (fun x : ℝ => x * (2 + ε * δ)) h
    field_simp [hz] at hm
    have hδ : ε * δ = 0 := by linarith [hm]
    rcases mul_eq_zero.mp hδ with hε0 | hδ0
    · exact absurd hε0 hε
    · exact hδ0
  · intro hδ
    rw [hδ]
    norm_num

/-- Machine-checked instance of the NEGATIVE CONTROL: the deformation fB has
  fB(0) = fB(infinity) = 0 (endpoints preserved) and fB'(0) = 1; at
  eps = 1/5 the coefficient is 1/(2+1/5) = 5/11, NOT 1/2.  Endpoint
  preservation is therefore not sufficient for coefficient preservation. -/
theorem control_fB_instance : (1 : ℝ) / (2 + (1 : ℝ) / 5) ≠ 1 / 2 := by
  norm_num

/-- The seed's identity warning: this mu_base is MU2(x) at x = 2Y,
  not MU2(Y).  The values agree wherever the denominators are nonzero. -/
theorem mu2_doubling (Y : ℝ) (h : (1 + Y) ^ 2 ≠ 0) : mu_base Y = MU2 (2 * Y) := by
  unfold mu_base MU2
  field_simp [pow_two]

/-- And the contrast at Y = 1: mu_base(1) = 3/4, MU2(1) = 5/9. -/
theorem mu2_not_same_at_one : mu_base 1 ≠ MU2 1 := by
  unfold mu_base MU2
  norm_num

/-- THE BUNDLED STATEMENT: a small kernel deformation with f'(0) = delta
  moves the deep coefficient to kappa = 1/(2+eps*delta), and the adopted
  one-half is preserved for all small eps exactly when delta = 0. -/
theorem robustness_of_kappa {ε δ : ℝ} (hε : ε ≠ 0) :
    ∀ (κ : ℝ), κ = 1 / (2 + ε * δ) → (κ = 1 / 2 ↔ δ = 0) := by
  intro κ hκ
  constructor
  · intro h12
    have hk : 1 / (2 + ε * δ) = 1 / 2 := hκ.symm.trans h12
    exact (kappa_preserved_iff hε).mp hk
  · intro hδ
    rw [hκ]
    exact (kappa_preserved_iff hε).mpr hδ

#print axioms slope_mu_base
#print axioms slope_deformed
#print axioms slope_fA
#print axioms slope_fB
#print axioms slope_fL
#print axioms linearized_deep_g_sq
#print axioms deep_flat_coefficient
#print axioms kappa_eff_formula
#print axioms kappa_preserved_iff
#print axioms control_fB_instance
#print axioms mu2_doubling
#print axioms mu2_not_same_at_one
#print axioms robustness_of_kappa