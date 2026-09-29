import Mathlib

/-!
# MineM5-E: the AQUAL scalar-cone speed c_par^2 = 1 + Y mu'/mu, its kernel-blind superluminality, and strict bounds 1 < c_par^2 < 2 for the mu_n family

Source lane: hunt_2026/eft01_positivity_causality_mu_family_2026.py, C4 (line ~172: "F''(z) = mu'(Y)/(2Y) > 0"), C5 (lines ~185-212: "c_par^2 = 1 + dln(mu)/dln(Y) = (F' + 2 z F'')/F' -> 2 in the deep-MOND limit for EVERY n";
  "superluminal at every finite Y, for every n"; "for mu ~ Y^p, c_par^2 -> 1 + p"), C6 (kernels: simple, exponential; the lane checks them on a grid only), family mu_n(Y) = 1 - (1+Y)^(-n).
  The lane's own grid/limit statements are numerical or sympy-limit; the strict inequalities below are proved for ALL Y > 0 (n >= 1 for the family).

PREMISE (stated in the lane header, NOT certified): for L = P(z), z = g^{mu nu} d phi d phi, the fluctuation dispersion around a spacelike gradient is omega^2 = k_perp^2 + k_par^2 (1 + 2 z P''/P'),
with P' proportional to F' = mu(sqrt z).  Everything below is the calculus and inequality algebra downstream of that premise.

CERTIFIED (real analysis):
* `cone_from_kernel`: if F'(z) := mu(sqrt z) and mu has derivative m' at sqrt z > 0, then F' has a derivative F'' with 2 z F'' = sqrt z * m'; hence, for mu(sqrt z) != 0,
  (F' + 2 z F'')/F' = 1 + Y m'/mu with Y = sqrt z.
* `cone_superluminal`: mu > 0, m' > 0, Y > 0  =>  1 < 1 + Y m'/mu  (kernel-blind: any increasing interpolation function is superluminal here).
* `powerlaw_cone`: for mu = Y^p (Y > 0): Y mu'/mu = p exactly, so c_par^2 = 1 + p; deep-MOND p = 1 gives 2 (the "sqrt 2 c" statement follows for any kernel that is a pure power law Y^1 in the deep limit,
  which is a hypothesis about the kernel, not a proof that the limit exists).
* `family_cone_bounds`: for the family mu_n(Y) = 1 - (1+Y)^(-n) with n >= 1 and Y > 0: 0 < Y mu_n'/mu_n < 1, i.e. 1 < c_par^2 < 2 for EVERY Y > 0 (Bernoulli).
* `exp_kernel_cone_bounds`: for mu = 1 - exp(-Y), Y > 0: 0 < Y mu'/mu < 1 (so 1 < c_par^2 < 2).

NOT certified: the dispersion-relation premise itself; the sympy limits Y -> 0 (only the power-law special case is proved, not that mu_n(Y)/Y has a limit for the family), the standard kernel Y/sqrt(1+Y^2),
the (n, Y) grid statements for n < 1, the time-advance numbers (C8), the C1/C2 series coefficients and the Wilson-coefficient invariant, and the non-applicability of positivity bounds (C3), which are
sympy statements about a limit/sign of F'' and about the missing vacuum.  Partial overlap in the corpus: H046_health_forces_n proves the k-essence sound speed c_s^2 = mu/(mu + u mu') (a DIFFERENT
sign of the same identity 2 K f'' = u mu'); it does not prove the AQUAL c_par^2 = 1 + Y mu'/mu > 1 nor the (1, 2) bounds.  kappa = 1/2 is FITTED; nothing here says the theory is closed.
-/

open Real

namespace MineM5E

/-- 2 z F'' = sqrt z * mu'(sqrt z) for F'(z) = mu(sqrt z) -/
theorem cone_from_kernel {μ : ℝ → ℝ} {m' z : ℝ} (hz : 0 < z) (hμ : HasDerivAt μ m' (Real.sqrt z)) :
    ∃ F2 : ℝ, HasDerivAt (fun z => μ (Real.sqrt z)) F2 z ∧ 2 * z * F2 = Real.sqrt z * m' := by
  have hs : 0 < Real.sqrt z := Real.sqrt_pos.mpr hz
  have hsq := Real.hasDerivAt_sqrt hz.ne'
  refine ⟨1 / (2 * Real.sqrt z) * m', ?_, ?_⟩
  · have := HasDerivAt.scomp z hμ hsq
    simp only [smul_eq_mul] at this
    exact this
  · field_simp
    rw [Real.sq_sqrt hz.le]

/-- (F' + 2 z F'')/F' = 1 + Y m'/mu with Y = sqrt z, when F' = mu != 0 -/
theorem cone_ratio {F1 F2 z Y m' μv : ℝ} (hμ : μv ≠ 0) (hF1 : F1 = μv) (hcone : 2 * z * F2 = Y * m') :
    (F1 + 2 * z * F2) / F1 = 1 + Y * m' / μv := by
  rw [hF1, hcone]
  field_simp

/-- kernel-blind superluminality: mu > 0, m' > 0, Y > 0 gives 1 < 1 + Y m'/mu -/
theorem cone_superluminal {μv m' Y : ℝ} (hμ : 0 < μv) (hm : 0 < m') (hY : 0 < Y) :
    1 < 1 + Y * m' / μv := by
  have : 0 < Y * m' / μv := by positivity
  linarith

/-- power law mu = Y^p: Y mu'/mu = p exactly -/
theorem powerlaw_cone {p Y : ℝ} (hY : 0 < Y) :
    Y * (p * Y ^ (p - 1)) / Y ^ p = p := by
  have h : Y * Y ^ (p - 1) = Y ^ p := by
    have := Real.rpow_add hY 1 (p - 1)
    rw [Real.rpow_one] at this
    rw [← this]; congr 1; ring
  have hp : 0 < Y ^ p := Real.rpow_pos_of_pos hY p
  field_simp
  have e : Y * p * Y ^ (p - 1) = (Y * Y ^ (p - 1)) * p := by ring
  rw [e, h]
  ring

/-- the deep-MOND power law p = 1 gives c_par^2 = 2 -/
theorem deep_cone_two {Y : ℝ} (hY : 0 < Y) : 1 + Y * (1 * Y ^ ((1 : ℝ) - 1)) / Y ^ (1 : ℝ) = 2 := by
  rw [powerlaw_cone hY]; norm_num

/-- the family kernel and its derivative -/
noncomputable def muN (n Y : ℝ) : ℝ := 1 - (1 + Y) ^ (-n)

theorem hasDerivAt_muN {n Y : ℝ} (hY : 0 < Y) :
    HasDerivAt (muN n) (n * (1 + Y) ^ (-n - 1)) Y := by
  have h1 : HasDerivAt (fun y : ℝ => 1 + y) 1 Y := by
    simpa using (hasDerivAt_id Y).const_add 1
  have h2 := Real.hasDerivAt_rpow_const (x := 1 + Y) (p := -n) (Or.inl (by linarith))
  have h3 := (h2.comp Y h1).const_sub 1
  have e : -((-n) * (1 + Y) ^ (-n - 1) * 1) = n * (1 + Y) ^ (-n - 1) := by ring
  rw [e] at h3
  exact h3

/-- strict bounds 0 < Y mu_n'/mu_n < 1 for n >= 1, Y > 0, i.e. 1 < c_par^2 < 2 -/
theorem family_cone_bounds {n Y : ℝ} (hn : 1 ≤ n) (hY : 0 < Y) :
    0 < muN n Y ∧ 0 < n * (1 + Y) ^ (-n - 1) ∧
    0 < Y * (n * (1 + Y) ^ (-n - 1)) / muN n Y ∧ Y * (n * (1 + Y) ^ (-n - 1)) / muN n Y < 1 := by
  have ht : 1 < 1 + Y := by linarith
  have ht0 : 0 < 1 + Y := by linarith
  have hn0 : 0 < n := by linarith
  set t := 1 + Y with htdef
  set P := t ^ n with hPdef
  have hP1 : 1 + n * Y ≤ P := by
    have := one_add_mul_self_le_rpow_one_add (s := Y) (by linarith) hn
    simpa [htdef, hPdef, add_comm] using this
  have hPpos : 0 < P := Real.rpow_pos_of_pos ht0 n
  have hPgt : 1 < P := by
    have : 0 < n * Y := by positivity
    linarith
  have hq : t ^ (-n) = P⁻¹ := by rw [Real.rpow_neg ht0.le]
  have hq1 : t ^ (-n - 1) = P⁻¹ / t := by
    rw [Real.rpow_sub ht0, Real.rpow_one, hq]
  have hmu : muN n Y = 1 - P⁻¹ := by unfold muN; rw [← htdef, hq]
  have hmupos : 0 < 1 - P⁻¹ := by
    have : P⁻¹ < 1 := inv_lt_one_of_one_lt₀ hPgt
    linarith
  have hderpos : 0 < n * t ^ (-n - 1) := by
    rw [hq1]; positivity
  refine ⟨by rw [hmu]; exact hmupos, hderpos, ?_, ?_⟩
  · rw [hmu]; positivity
  · rw [hmu, hq1, div_lt_one hmupos]
    have key : Y * (n * (P⁻¹ / t)) < 1 - P⁻¹ := by
      have e : 1 - P⁻¹ - Y * (n * (P⁻¹ / t)) = (t * (P - 1) - n * Y) / (t * P) := by
        field_simp
      have hnum : 0 < t * (P - 1) - n * Y := by
        have : n * Y ≤ P - 1 := by linarith
        have h2 : 0 < n * Y := by positivity
        nlinarith [mul_le_mul_of_nonneg_left this ht0.le, mul_pos hY h2]
      have : 0 < 1 - P⁻¹ - Y * (n * (P⁻¹ / t)) := by
        rw [e]; positivity
      linarith
    exact key

/-- exponential kernel mu = 1 - exp(-Y): 0 < Y mu'/mu < 1 -/
theorem exp_kernel_cone_bounds {Y : ℝ} (hY : 0 < Y) :
    0 < Y * Real.exp (-Y) / (1 - Real.exp (-Y)) ∧ Y * Real.exp (-Y) / (1 - Real.exp (-Y)) < 1 := by
  have he : Real.exp (-Y) < 1 := by
    rw [Real.exp_lt_one_iff]; linarith
  have hep : 0 < Real.exp (-Y) := Real.exp_pos _
  have hden : 0 < 1 - Real.exp (-Y) := by linarith
  refine ⟨by positivity, ?_⟩
  rw [div_lt_one hden]
  -- Y e^{-Y} < 1 - e^{-Y}  <=>  (1 + Y) e^{-Y} < 1  <=>  1 + Y < e^{Y}
  have h1 : Y + 1 < Real.exp Y := Real.add_one_lt_exp hY.ne'
  have h2 : Real.exp Y * Real.exp (-Y) = 1 := by rw [← Real.exp_add]; simp
  nlinarith [mul_lt_mul_of_pos_right h1 hep]

end MineM5E

#print axioms MineM5E.cone_from_kernel
#print axioms MineM5E.cone_ratio
#print axioms MineM5E.cone_superluminal
#print axioms MineM5E.powerlaw_cone
#print axioms MineM5E.deep_cone_two
#print axioms MineM5E.hasDerivAt_muN
#print axioms MineM5E.family_cone_bounds
#print axioms MineM5E.exp_kernel_cone_bounds
