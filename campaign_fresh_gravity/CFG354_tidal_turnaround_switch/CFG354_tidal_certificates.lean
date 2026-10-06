/-
CFG354 certificates: a turnaround switch on the tidal eigenvalues of the leaf overdensity potential.
Units in the rule lemmas: psi = Phi_d / (4 pi G rho_bar), t = Hessian(psi), tau = (Delta_ta - 1)/3.
-/
import Mathlib

open Real

namespace CFG354

/-- middle and smallest of three numbers (rules T1 = middle, T2 = smallest). -/
noncomputable def med3 (a b c : ℝ) : ℝ := max (min a b) (min (max a b) c)
noncomputable def min3 (a b c : ℝ) : ℝ := min (min a b) c

/-- S1: sphere tangential eigenvalue g/r = GM/r^3 = (4 pi G/3) rho_enc. -/
theorem sphere_tangential (G M r : ℝ) (hr : 0 < r) :
    (G * M / r ^ 2) / r = G * M / r ^ 3 ∧ G * M / r ^ 3 = (4 * π * G / 3) * (3 * M / (4 * π * r ^ 3)) := by
  have hp := pi_pos
  constructor <;> field_simp

/-- S2: trace = Poisson: radial (4 pi G rho - 2 GM/r^3) + 2 tangential = 4 pi G rho. -/
theorem sphere_trace (G M r rho : ℝ) :
    (4 * π * G * rho - 2 * (G * M / r ^ 3)) + 2 * (G * M / r ^ 3) = 4 * π * G * rho := by ring

/-- S3: for every sphere triple (t, t, r) the middle eigenvalue is the tangential one (T1 = l_t exactly). -/
theorem sphere_med (t r : ℝ) : med3 t t r = t := by
  unfold med3; simp [min_self, max_self]

/-- S4: uniform cylinder interior (c, c, 0), c >= 0: middle = c (T1 fires iff c >= tau), smallest = 0 (T2 off). -/
theorem cyl_in_responses (c : ℝ) (hc : 0 ≤ c) : med3 c c 0 = c ∧ min3 c c 0 = 0 := by
  unfold med3 min3; constructor
  · simp
  · simp [hc]

/-- S5: cylinder exterior (a, 0, -a): middle = 0 (T1 off for tau > 0). -/
theorem cyl_out_med (a : ℝ) (ha : 0 ≤ a) : med3 a 0 (-a) = 0 := by
  unfold med3
  rw [min_eq_right ha, max_eq_left ha, min_eq_right (by linarith : -a ≤ a)]
  exact max_eq_left (by linarith)

/-- S6: plane (d, 0, 0), any sign: middle = 0 (T1 off). -/
theorem plane_med (d : ℝ) : med3 d 0 0 = 0 := by
  unfold med3
  rcases le_total d 0 with h | h
  · rw [min_eq_left h, max_eq_right h, min_self]; exact max_eq_right h
  · rw [min_eq_right h, max_eq_left h, min_eq_right h]; simp

/-- S7 (T3 no-go, eigenvalues only): no function of the triple equals l_t on all spheres (t, t, r) and
vanishes inside uniform cylinders (c, c, 0). -/
theorem no_eigen_only_rule :
    ¬ ∃ F : ℝ → ℝ → ℝ → ℝ, (∀ a b, F a a b = a) ∧ (∀ c, 0 < c → F c c 0 = 0) := by
  rintro ⟨F, h1, h2⟩
  have := h1 1 0
  rw [h2 1 one_pos] at this
  norm_num at this

/-- S8 (monotone-rule no-go): a rule monotone in each eigenvalue that is ON at a host edge (tau, tau, l) with l <= 0
is ON inside every filament (c, c, 0) with c >= tau. -/
theorem monotone_rule_fires_in_filament (F : ℝ → ℝ → ℝ → ℝ)
    (hmono : ∀ a b c a' b' c', a ≤ a' → b ≤ b' → c ≤ c' → F a b c ≤ F a' b' c')
    (tau l c : ℝ) (hl : l ≤ 0) (hc : tau ≤ c) (hedge : tau ≤ F tau tau l) : tau ≤ F c c 0 :=
  le_trans hedge (hmono _ _ _ _ _ _ hc hc hl)

/-- S9: the EdS filament firing threshold for T1, 2 (9 pi^2/16 - 1)/3, exceeds 3. -/
theorem filament_threshold_gt_three : (3 : ℝ) < 2 * (9 * π ^ 2 / 16 - 1) / 3 := by
  have h := pi_gt_d2
  nlinarith

/-- S10: FRW (t = 0) is OFF under the strict switch for tau > 0. -/
theorem frw_off (tau : ℝ) (h : 0 < tau) : ¬ ((0 : ℝ) - tau > 0) := by linarith

/-- S11: Frobenius bound used for the linear field: l1 >= l2 >= tau > 0 implies sum l^2 >= 2 tau^2. -/
theorem frobenius_bound (l1 l2 l3 tau : ℝ) (ht : 0 < tau) (h2 : tau ≤ l2) (h12 : l2 ≤ l1) :
    2 * tau ^ 2 ≤ l1 ^ 2 + l2 ^ 2 + l3 ^ 2 := by
  nlinarith [sq_nonneg l3]

/-- S12 (layer inequality): a layer profile bounded by M on [0, w] has integral <= M w, so sup >= A / w. -/
theorem layer_sup_ge (p : ℝ → ℝ) (w M : ℝ) (hw : 0 < w) (hp : IntervalIntegrable p MeasureTheory.volume 0 w)
    (hM : ∀ x ∈ Set.Icc 0 w, p x ≤ M) : (∫ x in (0:ℝ)..w, p x) / w ≤ M := by
  have h : (∫ x in (0:ℝ)..w, p x) ≤ ∫ _ in (0:ℝ)..w, M :=
    intervalIntegral.integral_mono_on hw.le hp intervalIntegrable_const hM
  rw [intervalIntegral.integral_const, smul_eq_mul, sub_zero] at h
  rw [div_le_iff₀ hw]; linarith

/-- S13: a fixed layer weight A > 0 gives an unbounded peak as the width shrinks. -/
theorem layer_unbounded (A : ℝ) (hA : 0 < A) (B : ℝ) : ∃ w : ℝ, 0 < w ∧ B < A / w := by
  refine ⟨A / (|B| + 1), by positivity, ?_⟩
  rw [div_div_eq_mul_div, mul_div_assoc, mul_div_cancel₀ _ hA.ne']
  linarith [le_abs_self B]

/-- S14: delta-layer coefficient c_d = (n.e)^2 vanishes iff n is orthogonal to e. -/
theorem cd_zero_iff (n1 n2 n3 e1 e2 e3 : ℝ) :
    (n1 * e1 + n2 * e2 + n3 * e3) ^ 2 = 0 ↔ n1 * e1 + n2 * e2 + n3 * e3 = 0 := by
  constructor
  · intro h; exact pow_eq_zero_iff (n := 2) (by norm_num) |>.mp h
  · intro h; rw [h]; ring

/-- S15: spherical edge: tangential projector gives c_d = n.(I - n n).n = 0, radial projector gives 1 (|n| = 1). -/
theorem sphere_cd (s : ℝ) (hs : s = 1) : s - s ^ 2 = 0 ∧ s ^ 2 = 1 := by
  subst hs; norm_num

end CFG354

#print axioms CFG354.sphere_tangential
#print axioms CFG354.sphere_trace
#print axioms CFG354.sphere_med
#print axioms CFG354.cyl_in_responses
#print axioms CFG354.cyl_out_med
#print axioms CFG354.plane_med
#print axioms CFG354.no_eigen_only_rule
#print axioms CFG354.monotone_rule_fires_in_filament
#print axioms CFG354.filament_threshold_gt_three
#print axioms CFG354.frw_off
#print axioms CFG354.frobenius_bound
#print axioms CFG354.layer_sup_ge
#print axioms CFG354.layer_unbounded
#print axioms CFG354.cd_zero_iff
#print axioms CFG354.sphere_cd
