import Mathlib

open Real Finset Matrix

/-!
# NSA — certificates for the Navier–Stokes audit lanes (real_research/ns_audit_2026, NSA1–NSA7)

SCOPE: Lean certifies the exact ALGEBRA/ANALYSIS cores the NSA lanes rely on. It does NOT certify
the PDE results cited from the literature (Prodi–Serrin, the pressure-gradient regularity criteria of
Berselli–Galdi / Struwe / Zhou, Hajduk–Robinson's β = 3 damping theorem, Frenkler's QUMOND
regularity), nor that nature obeys the framework's law. Zero `sorry`; axioms ⊆ {propext,
Classical.choice, Quot.sound}.

N1  (NSA1 K1) the window theorem's trajectory bound holds for EVERY constant C: a₀·W is one choice.
N1b (NSA1 K2) with η(τ) = A τ^(−p), the recorded root (W/A)^(1/p) gives η = A²/W, not W; the
    correct root is (A/W)^(1/p).
N2  (NSA2 T2) the gradient projection kills the solenoidal viscous term and fixes the pressure
    gradient, so ∇p = −Q(Du/Dt); and the L² Pythagoras split of the acceleration.
N2b (NSA2 T1) the critical line 2/s + 3/r = 3 ⟺ s = 2r/(3(r−1)); s ≥ 1 ⟺ r ≤ 3.
N3  (NSA3) the energy class sits at Serrin index 3/2 for every interpolant; the damping bound is
    Serrin-class iff β ≥ 4; the β = 3 H¹ closure form νY² + cX² − XY ≥ 0 on the quadrant ⟺ 4cν ≥ 1;
    every row of the gap table has excess 1/2 per power of u.
N5  (NSA5) ‖Au‖² ≤ ‖A‖_F²‖u‖² + 2‖Aᵀu‖² for every A (so M(0) ≤ 1), and the witness A = a bᵀ
    (a ⊥ u, b ∥ u) is traceless with Aᵀu = 0 and ratio exactly 1 for every gauge λ.
N7  (NSA7) √ is not Lipschitz at 0 (the Hölder-½ force); the planar crossing time t² ν_eff = t_N²;
    the deep caustic law x_c = (π/4) G ρ a₀ t⁴; μ₂'s ν_eff = 1 at x = 2; the spherical law
    r_c = 16 G ρ a₀ t⁴/(3π); the EFE null shift d = e_N r_D; the viscous particular solution
    ν u'' = √x for u = 4 x^(5/2)/(15 ν).
-/

namespace NSA

/-! ## N1 — the trajectory bound, for any constant -/

theorem window_bound_any_constant {E : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E]
    (v v' : ℝ → E) (C T : ℝ) (hT : 0 ≤ T)
    (hv : ∀ x ∈ Set.Icc (0:ℝ) T, HasDerivWithinAt v (v' x) (Set.Icc 0 T) x)
    (hb : ∀ x ∈ Set.Ico (0:ℝ) T, ‖v' x‖ ≤ C) :
    ‖v T‖ ≤ ‖v 0‖ + C * T := by
  have h := norm_image_sub_le_of_norm_deriv_le_segment' hv hb T (Set.right_mem_Icc.2 hT)
  have h2 := norm_sub_norm_le (v T) (v 0)
  simp only [sub_zero] at h
  linarith

/-- The N13/N08 root solves the inverted equation; the correct root gives η = W. -/
theorem n13_root_inverted (A W p : ℝ) (hA : 0 < A) (hW : 0 < W) (hp : 0 < p) :
    A * ((W / A) ^ (1 / p)) ^ (-p) = A ^ 2 / W ∧ A * ((A / W) ^ (1 / p)) ^ (-p) = W := by
  have e : (1 / p) * (-p) = -1 := by field_simp
  constructor
  · rw [← Real.rpow_mul (by positivity), e, Real.rpow_neg_one]
    field_simp
  · rw [← Real.rpow_mul (by positivity), e, Real.rpow_neg_one]
    field_simp

/-! ## N2 — the pressure is the gradient part of the material acceleration -/

/-- Fourier-space projection onto gradients: Q v = (⟪ξ, v⟫/‖ξ‖²) ξ. -/
noncomputable def gradProj (ξ v : EuclideanSpace ℝ (Fin 3)) : EuclideanSpace ℝ (Fin 3) :=
  ((@inner ℝ _ _ ξ v) / ‖ξ‖ ^ 2) • ξ

theorem gradProj_kills_solenoidal (ξ u : EuclideanSpace ℝ (Fin 3)) (h : (@inner ℝ _ _ ξ u) = 0) (c : ℝ) :
    gradProj ξ (c • u) = 0 := by
  simp [gradProj, inner_smul_right, h]

theorem gradProj_fixes_gradient (ξ : EuclideanSpace ℝ (Fin 3)) (hξ : ξ ≠ 0) (p : ℝ) :
    gradProj ξ (p • ξ) = p • ξ := by
  have hn : ‖ξ‖ ≠ 0 := norm_ne_zero_iff.mpr hξ
  simp only [gradProj, inner_smul_right, real_inner_self_eq_norm_sq]
  congr 1
  field_simp

/-- ∇p = −Q(Du/Dt): with a = ν Δu − ∇p ↦ (−ν‖ξ‖²) û − p ξ in Fourier space and ξ ⊥ û. -/
theorem pressure_is_gradient_part (ξ u : EuclideanSpace ℝ (Fin 3)) (hξ : ξ ≠ 0)
    (h : (@inner ℝ _ _ ξ u) = 0) (ν p : ℝ) :
    gradProj ξ ((-ν * ‖ξ‖ ^ 2) • u - p • ξ) = -(p • ξ) := by
  have hn : ‖ξ‖ ≠ 0 := norm_ne_zero_iff.mpr hξ
  simp only [gradProj, inner_sub_right, inner_smul_right, h, real_inner_self_eq_norm_sq]
  rw [← neg_smul]
  congr 1
  field_simp
  ring

theorem acceleration_pythagoras (ξ u : EuclideanSpace ℝ (Fin 3)) (h : (@inner ℝ _ _ ξ u) = 0) (s t : ℝ) :
    ‖s • u + t • ξ‖ ^ 2 = ‖s • u‖ ^ 2 + ‖t • ξ‖ ^ 2 := by
  have h' : (@inner ℝ _ _ (s • u) (t • ξ)) = 0 := by
    rw [inner_smul_left, inner_smul_right, real_inner_comm, h]; simp
  have := norm_add_sq_eq_norm_sq_add_norm_sq_of_inner_eq_zero (s • u) (t • ξ) h'
  simpa [sq] using this

/-- The critical line for the acceleration: 2/s + 3/r = 3. -/
theorem critical_line (r s : ℝ) (hr : 1 < r) (hs : 0 < s) :
    2 / s + 3 / r = 3 ↔ s = 2 * r / (3 * (r - 1)) := by
  have hr0 : 0 < r := by linarith
  have hr1 : 0 < r - 1 := by linarith
  constructor
  · intro h
    field_simp at h ⊢
    linarith
  · intro h
    subst h
    field_simp
    ring

theorem critical_s_ge_one (r : ℝ) (hr : 1 < r) : 1 ≤ 2 * r / (3 * (r - 1)) ↔ r ≤ 3 := by
  have hr1 : 0 < 3 * (r - 1) := by linarith
  rw [le_div_iff₀ hr1]
  constructor <;> intro h <;> linarith

/-! ## N3 — the damped route's wall -/

theorem energy_class_index (θ : ℝ) : 2 * (θ / 2) + 3 * ((1 - θ) / 2 + θ / 6) = 3 / 2 := by ring

theorem damping_serrin_iff (β : ℝ) (hβ : -1 < β) : 5 / (β + 1) ≤ 1 ↔ 4 ≤ β := by
  rw [div_le_one (by linarith)]
  constructor <;> intro h <;> linarith

/-- The β = 3 H¹ estimate closes (pointwise Cauchy–Schwarz + Young) iff 4cν ≥ 1. -/
theorem h1_closure_iff (c ν : ℝ) (hc : 0 < c) (hν : 0 < ν) :
    (∀ X Y : ℝ, 0 ≤ X → 0 ≤ Y → 0 ≤ ν * Y ^ 2 + c * X ^ 2 - X * Y) ↔ 1 ≤ 4 * c * ν := by
  constructor
  · intro h
    have := h (2 * ν) 1 (by linarith) (by norm_num)
    nlinarith
  · intro h X Y _ _
    nlinarith [sq_nonneg (2 * c * X - Y), mul_nonneg (sub_nonneg.2 h) (sq_nonneg Y)]

/-- Every row of the gap table: (Serrin index of the energy-class space − scaling weight)/degree. -/
theorem gap_table :
    (2 / (10/3 : ℝ) + 3 / (10/3) - 1) / 1 = 1 / 2 ∧     -- u in L^{10/3}_{t,x}
    (2 / (2 : ℝ) + 3 / 2 - 2) / 1 = 1 / 2 ∧             -- ∇u (vorticity) in L²_{t,x}
    (2 / (5/3 : ℝ) + 3 / (5/3) - 2) / 2 = 1 / 2 ∧       -- p in L^{5/3}_{t,x}
    (2 / (5/4 : ℝ) + 3 / (5/4) - 3) / 2 = 1 / 2 := by  -- ∇p = −Q(Du/Dt) in L^{5/4}_{t,x}
  norm_num

/-! ## N5 — the β = 3 threshold is the optimum of the pointwise method -/

/-- ‖Au‖² ≤ ‖A‖_F²‖u‖² + 2‖Aᵀu‖²: the pointwise ratio at gauge λ = 0 is at most 1. -/
theorem ratio_le_one (A : Matrix (Fin 3) (Fin 3) ℝ) (u : Fin 3 → ℝ) :
    ∑ i, (A.mulVec u i) ^ 2 ≤
      (∑ i, ∑ j, (A i j) ^ 2) * (∑ j, (u j) ^ 2) + 2 * ∑ i, (Aᵀ.mulVec u i) ^ 2 := by
  have h1 : ∀ i, (A.mulVec u i) ^ 2 ≤ (∑ j, (A i j) ^ 2) * (∑ j, (u j) ^ 2) := fun i => by
    simpa [Matrix.mulVec, dotProduct] using
      Finset.sum_mul_sq_le_sq_mul_sq Finset.univ (fun j => A i j) u
  have h2 : 0 ≤ 2 * ∑ i, (Aᵀ.mulVec u i) ^ 2 := by positivity
  calc ∑ i, (A.mulVec u i) ^ 2 ≤ ∑ i, (∑ j, (A i j) ^ 2) * (∑ j, (u j) ^ 2) :=
        Finset.sum_le_sum (fun i _ => h1 i)
    _ = (∑ i, ∑ j, (A i j) ^ 2) * (∑ j, (u j) ^ 2) := by rw [Finset.sum_mul]
    _ ≤ _ := by linarith

/-- The witness A = a bᵀ with a = (0, α, 0) ⊥ u = e₁ and b = (β, 0, 0) ∥ u. -/
def witA (α β : ℝ) : Matrix (Fin 3) (Fin 3) ℝ := !![0, 0, 0; α * β, 0, 0; 0, 0, 0]
def witU : Fin 3 → ℝ := ![1, 0, 0]

theorem witness_saturates (α β lam : ℝ) :
    (witA α β).trace = 0 ∧
    (witA α β)ᵀ.mulVec witU = 0 ∧
    ((witA α β) + lam • (witA α β)ᵀ).mulVec witU = (witA α β).mulVec witU ∧
    ∑ i, ((witA α β).mulVec witU i) ^ 2 =
      (∑ i, ∑ j, ((witA α β) i j) ^ 2) * (∑ j, (witU j) ^ 2) + 2 * ∑ i, ((witA α β)ᵀ.mulVec witU i) ^ 2 := by
  refine ⟨?_, ?_, ?_, ?_⟩
  · simp [witA, Matrix.trace, Fin.sum_univ_three]
  · ext i; fin_cases i <;> simp [witA, witU, Matrix.mulVec, dotProduct, Fin.sum_univ_three]
  · ext i; fin_cases i <;> simp [witA, witU, Matrix.mulVec, dotProduct, Fin.sum_univ_three]
  · simp [witA, witU, Matrix.mulVec, dotProduct, Fin.sum_univ_three]

/-! ## N7 — the framework's own fluid at a field null -/

/-- √ is not Lipschitz at 0: the deep-MOND force g ∝ √|x| near a Newtonian null. -/
theorem sqrt_not_lipschitz_at_zero (L : ℝ) (hL : 0 < L) : ∃ x > 0, L * x < Real.sqrt x := by
  refine ⟨1 / (4 * L ^ 2), by positivity, ?_⟩
  have hs : Real.sqrt (1 / (4 * L ^ 2)) = 1 / (2 * L) := by
    rw [show (1 : ℝ) / (4 * L ^ 2) = (1 / (2 * L)) ^ 2 by field_simp; ring]
    exact Real.sqrt_sq (by positivity)
  rw [hs]
  have : L * (1 / (4 * L ^ 2)) = 1 / (4 * L) := by field_simp
  rw [this]
  rw [div_lt_div_iff₀ (by positivity) (by positivity)]
  nlinarith

/-- Planar dust, uniform region at rest: J = 1 − 2πGρ ν_eff t² vanishes iff t² ν_eff = t_N². -/
theorem planar_crossing (G ρ ν t : ℝ) (hG : 0 < G) (hρ : 0 < ρ) :
    1 - 2 * π * G * ρ * ν * t ^ 2 = 0 ↔ t ^ 2 * ν = 1 / (2 * π * G * ρ) := by
  have : 0 < 2 * π * G * ρ := by positivity
  constructor
  · intro h; field_simp; linarith
  · intro h; field_simp at h; linarith

/-- The deep caustic law: ν_eff(y) = 1/(2√y) with y = 4πGρx/a₀ and t² ν_eff = t_N² give
    x = (π/4) G ρ a₀ t⁴ (here s = √y). -/
theorem deep_caustic_law (G ρ a0 x s t : ℝ) (hG : 0 < G) (hρ : 0 < ρ) (ha : 0 < a0) (hs : 0 < s)
    (hy : s ^ 2 = 4 * π * G * ρ * x / a0)
    (hfront : t ^ 2 * (1 / (2 * s)) = 1 / (2 * π * G * ρ)) :
    x = π / 4 * G * ρ * a0 * t ^ 4 := by
  have hsv : s = π * G * ρ * t ^ 2 := by
    field_simp at hfront
    nlinarith [hfront]
  have hx : x = a0 * s ^ 2 / (4 * π * G * ρ) := by
    field_simp at hy ⊢
    linarith
  rw [hx, hsv]
  field_simp

/-- μ₂ = 1 − (1 + x/2)⁻², μ₂ + x μ₂' = 1 − (1 − x/2)(1 + x/2)⁻³ equals 1 exactly at x = 2. -/
theorem mu2_front (x : ℝ) (hx : x = 2) : 1 - (1 - x / 2) * (1 + x / 2)⁻¹ ^ 3 = 1 := by
  subst hx; norm_num

/-- The spherical law: t⁴ = 3π r₀/(16 G a₀ ρ) (deep-MOND shell arrival) ⟺ r₀ = 16 G ρ a₀ t⁴/(3π). -/
theorem spherical_caustic_law (G ρ a0 r0 t : ℝ) (hG : 0 < G) (hρ : 0 < ρ) (ha : 0 < a0) :
    t ^ 4 = 3 * π * r0 / (16 * G * a0 * ρ) ↔ r0 = 16 * G * ρ * a0 * t ^ 4 / (3 * π) := by
  have hπ : 0 < π := Real.pi_pos
  constructor
  · intro h; rw [h]; field_simp
  · intro h; rw [h]; field_simp

/-- The external field shifts the null: (4π/3) G ρ d = e_N a₀ ⟺ d = e_N · 3a₀/(4πGρ). -/
theorem efe_null_shift (G ρ a0 eN d : ℝ) (hG : 0 < G) (hρ : 0 < ρ) :
    4 * π / 3 * G * ρ * d = eN * a0 ↔ d = eN * (3 * a0 / (4 * π * G * ρ)) := by
  have hπ : 0 < π := Real.pi_pos
  constructor
  · intro h; field_simp; linarith
  · intro h; rw [h]; field_simp

/-- The viscous particular solution: u = 4 x^(5/2)/(15 ν) has ν u'' = x^(1/2) (u'' Hölder-½). -/
theorem viscous_particular (ν x : ℝ) (hν : ν ≠ 0) :
    ν * deriv (deriv (fun y : ℝ => 4 * y ^ (5 / 2 : ℝ) / (15 * ν))) x = x ^ (1 / 2 : ℝ) := by
  have d1 : deriv (fun y : ℝ => 4 * y ^ (5 / 2 : ℝ) / (15 * ν)) =
      fun y => 4 * ((5 / 2 : ℝ) * y ^ (3 / 2 : ℝ)) / (15 * ν) := by
    funext y
    have h := (Real.hasDerivAt_rpow_const (x := y) (p := (5 / 2 : ℝ)) (Or.inr (by norm_num)))
    have h2 := ((h.const_mul 4).div_const (15 * ν)).deriv
    rw [show (5 / 2 : ℝ) - 1 = 3 / 2 by norm_num] at h2
    simpa using h2
  have d2 : deriv (fun y : ℝ => 4 * ((5 / 2 : ℝ) * y ^ (3 / 2 : ℝ)) / (15 * ν)) x =
      4 * ((5 / 2 : ℝ) * ((3 / 2 : ℝ) * x ^ (1 / 2 : ℝ))) / (15 * ν) := by
    have h := (Real.hasDerivAt_rpow_const (x := x) (p := (3 / 2 : ℝ)) (Or.inr (by norm_num)))
    have h2 := (((h.const_mul (5 / 2 : ℝ)).const_mul 4).div_const (15 * ν)).deriv
    rw [show (3 / 2 : ℝ) - 1 = 1 / 2 by norm_num] at h2
    simpa using h2
  rw [d1, d2]
  field_simp
  ring

end NSA

#print axioms NSA.window_bound_any_constant
#print axioms NSA.n13_root_inverted
#print axioms NSA.gradProj_kills_solenoidal
#print axioms NSA.gradProj_fixes_gradient
#print axioms NSA.pressure_is_gradient_part
#print axioms NSA.acceleration_pythagoras
#print axioms NSA.critical_line
#print axioms NSA.critical_s_ge_one
#print axioms NSA.energy_class_index
#print axioms NSA.damping_serrin_iff
#print axioms NSA.h1_closure_iff
#print axioms NSA.gap_table
#print axioms NSA.ratio_le_one
#print axioms NSA.witness_saturates
#print axioms NSA.sqrt_not_lipschitz_at_zero
#print axioms NSA.planar_crossing
#print axioms NSA.deep_caustic_law
#print axioms NSA.mu2_front
#print axioms NSA.spherical_caustic_law
#print axioms NSA.efe_null_shift
#print axioms NSA.viscous_particular
