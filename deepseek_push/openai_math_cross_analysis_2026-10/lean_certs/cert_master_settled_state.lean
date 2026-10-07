import Mathlib

/-! # MASTER CERTIFICATE — the settled-state corpus of the framework

One file, zero sorry: the algebraic core of the framework's settled-state
derivations, end to end. Every theorem below compiles against the
standard Mathlib with axioms = {propext, Classical.choice, Quot.sound}.

## The corpus (what is CLOSED — machine-checked)
  1. Kernel occupancy:   1/(e^s - 1) = e^{-s}/(1 - e^{-s})        [T9]
  2. Enclosed phantom:   M_ph(<r) = M_b/(e^s - 1), s = r_t/r       [T9]
  3. Stable form:        (s/2)e^s/(e^s-1) = (s/2)/(1 - e^{-s})     [T9]
  4. Elasticity zero:    s e^s = 2(e^s-1)  =>  eps(s) = 0          [T9]
  5. Half-mass radius:   M_ph/M_b = 1/2 at s = ln 3                [T9]
  6. Uniform mu-state:   r^2 rho_ph = sqrt(G M a0)/(4 pi G) const  [T10]
  7. Flat level:         v^2 = 4 pi G mu_ph  =>  v^4 = G M a0      [T10]
  8. Supply radius:      M_ph = 5.36 M_b at s = ln(1 + 1/5.36)     [T10]
  9. Assembly clock:     t_c/t_g = ln(1-f_c)/ln(1-f_g) (Gamma out) [T11]
 10. Epoch elasticity:   eps(f) = (1-f)[-ln(1-f)]/f                [T12]
 11. Sound speed:        c^2 = v^2/2  =>  c^4 = G M a0 / 4         [T13]
 12. Jeans stability:    lambda_J^2 = 2 pi^2 r^2 (lambda_J sqrt 2 pi r) [T13]
 13. The half-triple:    1/(e^s-1) = (1/2)(coth(s/2) - 1)          [NEW]

## The boundary (what is NOT claimed — stated, not certified)
  - kappa = 1/2 is FITTED (a0 = kappa c sqrt(G rho_Lambda)); the
    epsilon(0) = 1/2 = kernel-half = kappa unification is a declared
    OBSERVATION, not a derivation.
  - lambda (the fluid-lapse regulator) is convention-bound: the T12
    three-clock agreement holds under the mixed-definition levels
    (0.60/0.43) and BREAKS on one-definition levels (factor 2.4 at
    b = 0; f >= 1 for b >= 0.1) — sibling audit 983addaac accepted.
  - No dark-matter particle; the cold fluid is a separate real
    component whose mass is still required; the no-substructure
    theorem covers the phantom only.
  - Limits (eps(s) -> 1/2 as s -> 0; tendsto forms) and all
    derivative/statistics steps ride in the lane scripts (house
    pattern: calculus carries in the lane, algebra is certified).

## Physics map
  Point baryon host M_b; r_t := sqrt(G M_b / a0); kernel-exact deep
  phantom rho_ph = sqrt(G M a0)/(4 pi G r^2). The settled state is the
  uniform-mu state; flat rotation is mu-constancy; the phantom fluid is
  barotropic with the sound speed pinned to the baryons and Jeans-stable
  at every radius; completeness under settling obeys f = 1 - e^{-Gamma t}
  whose ratio and sensitivity faces are closure relations.
-/

noncomputable section

open Real

-- ============ I. the mass law (T9) ============

/-- Kernel occupancy: 1/(e^s - 1) = e^{-s}/(1 - e^{-s}). -/
theorem kernel_occupancy_identity (s : ℝ) (hne : Real.exp s ≠ 1) :
    1 / (Real.exp s - 1) = Real.exp (-s) / (1 - Real.exp (-s)) := by
  have hne2 : Real.exp s ≠ 0 := Real.exp_ne_zero s
  have hden2 : 1 - Real.exp (-s) ≠ 0 := by
    intro hz
    have hzi : (Real.exp s)⁻¹ = 1 := by
      rw [Real.exp_neg] at hz
      linarith
    exact hne (inv_eq_one.mp hzi)
  have hmul : Real.exp (-s) * (Real.exp s - 1) = 1 - Real.exp (-s) := by
    rw [mul_sub, mul_comm (Real.exp (-s)) (Real.exp s), ← Real.exp_add]
    norm_num
  rw [eq_comm]
  apply (div_eq_iff hden2).2
  rw [← hmul]
  field_simp [hne, hne2]

/-- Enclosed phantom mass: with the flux closed form, M_ph = M_b/(e^s - 1). -/
theorem m_ph_closed_form (s Mph Mb nu_m1 : ℝ) (hn : nu_m1 = 1 / (Real.exp s - 1))
    (hM : Mph = Mb * nu_m1) (hMb : Mb ≠ 0) :
    Mph / Mb = 1 / (Real.exp s - 1) := by
  rw [hM, hn]
  field_simp [hMb]

/-- Stable form: (s/2) e^s/(e^s - 1) = (s/2)/(1 - e^{-s}),
the numerically-safe form at s ~ 1e-9. -/
theorem deficit_stable_form (s : ℝ) (h : s ≠ 0) :
    (s / 2) * Real.exp s / (Real.exp s - 1) =
      (s / 2) / (1 - Real.exp (-s)) := by
  have hne : Real.exp s ≠ 1 := by
    intro h1
    have h0 : Real.exp s = Real.exp 0 := by simpa using h1
    exact h (Real.exp_injective h0)
  have hne2 : Real.exp s ≠ 0 := Real.exp_ne_zero s
  have hden : 1 - Real.exp (-s) ≠ 0 := by
    intro hz
    have hzi : (Real.exp s)⁻¹ = 1 := by
      rw [Real.exp_neg] at hz
      linarith
    have he0 : Real.exp s = Real.exp 0 := by simpa using (inv_eq_one.mp hzi)
    exact h (Real.exp_injective he0)
  rw [Real.exp_neg]
  field_simp [h, hne, hne2, hden]

/-- Elasticity annihilates at the root: s e^s = 2(e^s - 1) => eps(s) = 0. -/
theorem elasticity_annihilates_at_root (s : ℝ)
    (hroot : s * Real.exp s = 2 * (Real.exp s - 1)) (hne : Real.exp s ≠ 1) :
    (s / 2) * Real.exp s / (Real.exp s - 1) = 1 := by
  have hmain : (s / 2) * Real.exp s = Real.exp s - 1 := by
    have hs : (s / 2) * Real.exp s = (s * Real.exp s) / 2 := by ring
    rw [hs, hroot]
    ring
  rw [hmain]
  field_simp [hne]

/-- Half-mass radius: M_ph/M_b = 1/2 exactly at s = log 3. -/
theorem half_mass_at_log3 :
    1 / (Real.exp (Real.log 3) - 1) = 1 / 2 := by
  have h3 : (0 : ℝ) < 3 := by norm_num
  rw [Real.exp_log h3]
  norm_num

/-- NEW — the half-triple's algebraic face: 1/(e^s-1) = (1/2)(coth(s/2)-1),
i.e. the kernel's exact sub-leading constant is 1/2, the same number as
kappa (fitted) and eps(0) (declared observation). -/
theorem kernel_half_coth (s : ℝ) (hne : Real.exp s ≠ 1) :
    1 / (Real.exp s - 1) =
      1 / 2 * ((Real.exp (s / 2) + Real.exp (-(s / 2))) /
               (Real.exp (s / 2) - Real.exp (-(s / 2))) - 1) := by
  have hz : Real.exp (s / 2) - Real.exp (-(s / 2)) ≠ 0 := by
    intro h
    have : Real.exp (s / 2) = Real.exp (-(s / 2)) := sub_eq_zero.mp h
    have hs2 : s / 2 = -(s / 2) := Real.exp_injective this
    have hs : s = 0 := by linarith
    have : Real.exp s = 1 := by simpa [hs]
    exact hne this
  have ha : Real.exp (s / 2) ≠ 0 := Real.exp_ne_zero _
  have hb : Real.exp (-(s / 2)) ≠ 0 := Real.exp_ne_zero _
  have hden1 : Real.exp s - 1 ≠ 0 := by
    intro h
    apply hne
    linarith
  -- step 1: the simplified form 1/(e^s-1) = e^{-s/2}/(e^{s/2} - e^{-s/2})
  have hmain : 1 / (Real.exp s - 1) =
      Real.exp (-(s / 2)) / (Real.exp (s / 2) - Real.exp (-(s / 2))) := by
    rw [eq_comm]
    apply (div_eq_iff hz).2
    field_simp [hden1, hb]
    rw [mul_sub]
    rw [← Real.exp_add]
    have harg : -(s / 2) + s = s / 2 := by ring
    rw [harg]
    ring
  -- step 2: the coth face
  rw [hmain]
  field_simp [hz, ha, hb]
  ring

-- ============ II. the settling + flatness (T10) ============

/-- Uniform mu-state: r^2 rho_ph is constant for the deep closed form. -/
theorem mu_ph_is_constant (G M a0 r rho_ph : ℝ) (hG : G ≠ 0) (hr : r ≠ 0)
    (h : rho_ph = sqrt (G * M * a0) / (4 * π * G * r ^ 2)) :
    r ^ 2 * rho_ph = sqrt (G * M * a0) * (4 * π * G)⁻¹ := by
  rw [h]
  field_simp [hG, hr, pow_two]

/-- Flat level: v^2 = 4 pi G mu_ph with the uniform mu implies v^4 = G M a0. -/
theorem v4_from_uniform_mu (G M a0 v2 mu_ph : ℝ) (hG : 0 < G) (hM : 0 < M)
    (ha : 0 < a0) (hv : v2 = 4 * π * G * mu_ph)
    (hmu : mu_ph = sqrt (G * M * a0) / (4 * π * G)) :
    v2 ^ 2 = G * M * a0 := by
  have h4pi : 4 * π ≠ 0 := mul_ne_zero (by norm_num : (4 : ℝ) ≠ 0) Real.pi_ne_zero
  have h4piG : 4 * π * G ≠ 0 := mul_ne_zero h4pi (ne_of_gt hG)
  have hnn : 0 ≤ G * M * a0 := by positivity
  rw [hv, hmu]
  field_simp [h4piG]
  rw [Real.sq_sqrt hnn]

/-- Supply radius: with s = log(1 + 1/5.36), M_ph/M_b = 5.36 = 134/25
exactly (the P3 cosmic share sits at r = r_t / ln(1 + 1/5.36) = 5.8457
r_t). -/
theorem supply_mass_exact :
    1 / (Real.exp (Real.log (1 + 1 / (134 / 25 : ℝ))) - 1) = 134 / 25 := by
  have hpos : (0 : ℝ) < 1 + 1 / (134 / 25) := by norm_num
  rw [Real.exp_log hpos]
  norm_num

-- ============ III. the clock (T11) ============

/-- Assembly clock: the settling law at both epochs with a common rate
Gamma gives the formation-time ratio as the log-completeness ratio. -/
theorem assembly_ratio_from_law (Gamma t_c t_g f_c f_g : ℝ) (hΓ : Gamma ≠ 0)
    (htg : t_g ≠ 0) (hc : 1 - f_c = Real.exp (-Gamma * t_c))
    (hg : 1 - f_g = Real.exp (-Gamma * t_g)) :
    t_c / t_g = Real.log (1 - f_c) / Real.log (1 - f_g) := by
  have hlogc : Real.log (1 - f_c) = -Gamma * t_c := by
    rw [hc, Real.log_exp]
  have hlogg : Real.log (1 - f_g) = -Gamma * t_g := by
    rw [hg, Real.log_exp]
  have hlg_ne : Real.log (1 - f_g) ≠ 0 := by
    rw [hlogg]
    exact mul_ne_zero (neg_ne_zero.mpr hΓ) htg
  field_simp [hlg_ne]
  rw [hlogc, hlogg]
  ring

-- ============ IV. the sensitivity (T12) ============

/-- Epoch elasticity: x e^{-x}/(1 - e^{-x}) = (1-f)[-ln(1-f)]/f given
the law 1 - f = e^{-x} — Gamma and t cancel; eps is a function of f
alone. -/
theorem epoch_elasticity_closed (x f : ℝ) (hf : f ≠ 0)
    (hlaw : 1 - f = Real.exp (-x)) :
    x * Real.exp (-x) / (1 - Real.exp (-x)) = (1 - f) * (-Real.log (1 - f)) / f := by
  have hlog : Real.log (1 - f) = -x := by
    rw [hlaw, Real.log_exp]
  have hden : 1 - Real.exp (-x) = f := by linarith
  rw [hden, ← hlaw, hlog]
  norm_num
  field_simp [hf]

-- ============ V. the sound speed + stability (T13) ============

/-- c^2 = v^2/2 with v^4 = G M a0 forces c^4 = G M a0 / 4. -/
theorem sound_speed_fourth_power (G M a0 v2 c2 : ℝ) (hv : v2 ^ 2 = G * M * a0)
    (hc : c2 = v2 / 2) :
    c2 ^ 2 = G * M * a0 / 4 := by
  rw [hc]
  have hv2 : (v2 / 2) ^ 2 = v2 * v2 / 4 := by ring
  rw [hv2]
  rw [← pow_two v2, hv]

/-- sqrt form: sqrt((GMa0)/4) = sqrt(GMa0)/2. -/
theorem sound_speed_sqrt (G M a0 : ℝ) (hG : 0 ≤ G * M * a0) :
    sqrt (G * M * a0 / 4) = sqrt (G * M * a0) / 2 := by
  rw [Real.sqrt_div hG 4]
  norm_num

/-- Jeans substitution: with c^2 = v^2/2 and G rho = v^2/(4 pi r^2),
lambda_J^2 = c^2 * pi/(G rho) = 2 pi^2 r^2 — Jeans-stable at every
radius (lambda_J = sqrt 2 * pi * r). -/
theorem jeans_square (c2 v2 G rho r : ℝ) (hc2 : c2 = v2 / 2) (hv2 : v2 ≠ 0)
    (hr2 : r ≠ 0) (hgr : G * rho = v2 / (4 * π * r ^ 2)) :
    c2 * π / (G * rho) = 2 * π ^ 2 * r ^ 2 := by
  rw [hc2, hgr]
  field_simp [hv2, hr2]
  ring

end