/-
  LN2_lean_os1_dw1_certs — Lean 4 + Mathlib certificates for OS1 (core law out of sample) and DW1 (dwarf flattening).

  Certifies ALGEBRA AND ANALYSIS from stated premises only. It does not certify any physical premise (isothermal cores,
  rate × age = 1 at the core, Burkert halos, Σ_a0 = a₀/(2πG)) or any measured number. κ = ½ is FITTED.

  Compile: cd fable_independent_2026/lean_2026 && lake env lean <path>/CoreLawCerts.lean
-/
import Mathlib

open Real

namespace CoreLawCerts

/-! ## 1. The q ↔ n map (LN1 T7: Σ₀ ∝ σ^q, q = (1+n)/2, cross-section per mass ∝ v^(−n)) -/

theorem q_to_n (q n : ℝ) : q = (1 + n) / 2 ↔ n = 2 * q - 1 := by
  constructor <;> intro h <;> linarith

/-- OS1's calibrated q_f = 0.892 / 0.748 correspond to n = 0.784 / 0.496: the cross-section per mass falls with velocity. -/
theorem os1_n_values : (2 * (892 / 1000 : ℝ) - 1 = 784 / 1000) ∧ (2 * (748 / 1000 : ℝ) - 1 = 496 / 1000) ∧
    (0 < (784 / 1000 : ℝ)) ∧ (0 < (496 / 1000 : ℝ)) := by
  refine ⟨by norm_num, by norm_num, by norm_num, by norm_num⟩

/-- **Surface-density ratio.** Under Σ_i = Σ_a0 (σ_i/σ_ref)^q, two systems differ by (σ₁/σ₂)^q, independent of σ_ref. -/
theorem sigma_ratio (Sa σr σ1 σ2 q : ℝ) (hSa : 0 < Sa) (hr : 0 < σr) (h1 : 0 < σ1) (h2 : 0 < σ2) :
    (Sa * (σ1 / σr) ^ q) / (Sa * (σ2 / σr) ^ q) = (σ1 / σ2) ^ q := by
  rw [Real.div_rpow h1.le hr.le, Real.div_rpow h2.le hr.le, Real.div_rpow h1.le h2.le]
  have a : 0 < σr ^ q := Real.rpow_pos_of_pos hr q
  have b : 0 < σ2 ^ q := Real.rpow_pos_of_pos h2 q
  field_simp

/-! ## 2. Structural Γt = 1 (DW1 M2) -/

/-- **M2.** If the core density is set by the core condition ρ₀ = 1/(K σ^(1−n) t) and the central rate is
Γ = ρ₀ · K σ^(1−n), then Γ t = 1 for every σ, K, n, t > 0. The collapse parameter is the same in every system. -/
theorem gamma_t_one (K σ n t : ℝ) (hK : 0 < K) (hσ : 0 < σ) (ht : 0 < t) :
    (1 / (K * σ ^ (1 - n) * t)) * (K * σ ^ (1 - n)) * t = 1 := by
  have hp : 0 < σ ^ (1 - n) := Real.rpow_pos_of_pos hσ _
  field_simp

/-- Corollary: no collapse threshold N_c > 1 is reached by any system under this core law. -/
theorem no_collapse (K σ n t Nc : ℝ) (hK : 0 < K) (hσ : 0 < σ) (ht : 0 < t) (hN : 1 < Nc) :
    ¬ (Nc ≤ (1 / (K * σ ^ (1 - n) * t)) * (K * σ ^ (1 - n)) * t) := by
  rw [gamma_t_one K σ n t hK hσ ht]; linarith

/-! ## 3. The Knudsen closed form (DW1 M1) -/

/-- **M1.** Premises:
* mean free path λ = 1/(ρ₀ s), gravitational scale height H = σ / √(4πGρ₀), Kn = λ / H;
* core condition ρ₀ (s v) t = 1, mean relative speed v = (4/√π) σ;
* s v = K σ^(1−n), with K fixed by the galaxy anchor: K = 9 σ_ref^(1+n) / (4πG t Σ²), Σ = a₀/(2πG).
Then Kn = (4/(3√π)) · (2 a₀ t / σ_ref) · (σ/σ_ref)^((n−1)/2), i.e. (σ/σ_ref)^(q−1) with q = (1+n)/2. -/
theorem knudsen_closed_form (G a0 t σ σr n s v K ρ0 Sg Kn : ℝ)
    (hG : 0 < G) (ha : 0 < a0) (ht : 0 < t) (hσ : 0 < σ) (hr : 0 < σr) (hs : 0 < s) (hρ0 : 0 < ρ0)
    (hcore : ρ0 * (s * v) * t = 1)
    (hv : v = 4 / Real.sqrt π * σ)
    (hsv : s * v = K * σ ^ (1 - n))
    (hK : K = 9 * σr ^ (1 + n) / (4 * π * G * t * Sg ^ 2))
    (hSg : Sg = a0 / (2 * π * G))
    (hKn : Kn = (1 / (ρ0 * s)) / (σ / Real.sqrt (4 * π * G * ρ0))) :
    Kn = 4 / (3 * Real.sqrt π) * (2 * a0 * t / σr) * (σ / σr) ^ ((n - 1) / 2) := by
  have hpi : 0 < π := Real.pi_pos
  have hsp : 0 < Real.sqrt π := Real.sqrt_pos.mpr hpi
  have hspi2 : Real.sqrt π ^ 2 = π := Real.sq_sqrt hpi.le
  have h4 : 0 < 4 * π * G * ρ0 := by positivity
  have hsq4 : Real.sqrt (4 * π * G * ρ0) ^ 2 = 4 * π * G * ρ0 := Real.sq_sqrt h4.le
  have hsq4p : 0 < Real.sqrt (4 * π * G * ρ0) := Real.sqrt_pos.mpr h4
  -- rpow bookkeeping: A = σ^(n−1), Bv = σr^(n−1)
  set A := σ ^ (n - 1) with hA
  set Bv := σr ^ (n - 1) with hBv
  have hApos : 0 < A := Real.rpow_pos_of_pos hσ _
  have hBpos : 0 < Bv := Real.rpow_pos_of_pos hr _
  have e1 : σ ^ (1 - n) = 1 / A := by
    rw [hA, eq_div_iff (ne_of_gt (Real.rpow_pos_of_pos hσ _)), ← Real.rpow_add hσ]; simp
  have e2 : σr ^ (1 + n) = σr ^ 2 * Bv := by
    rw [hBv, ← Real.rpow_natCast, ← Real.rpow_add hr]; norm_num; ring_nf
  have e3 : ((σ / σr) ^ ((n - 1) / 2)) ^ 2 = A / Bv := by
    rw [← Real.rpow_natCast, ← Real.rpow_mul (div_pos hσ hr).le, Real.div_rpow hσ.le hr.le]
    norm_num
    rw [hA, hBv]
  have hq : 0 < (σ / σr) ^ ((n - 1) / 2) := Real.rpow_pos_of_pos (div_pos hσ hr) _
  -- both sides positive
  have hKnpos : 0 < Kn := by rw [hKn]; positivity
  have hRpos : 0 < 4 / (3 * Real.sqrt π) * (2 * a0 * t / σr) * (σ / σr) ^ ((n - 1) / 2) := by positivity
  -- squares agree
  have hv' : s * v = s * (4 / Real.sqrt π * σ) := by rw [hv]
  have hvpos : 0 < v := by rw [hv]; positivity
  have hρ : ρ0 = 1 / (s * v * t) := by
    have h' : ρ0 * (s * v * t) = 1 := by rw [← hcore]; ring
    rw [eq_div_iff (ne_of_gt (by positivity))]; exact h'
  have lhs2 : Kn ^ 2 = 4 * π * G / (ρ0 * s ^ 2 * σ ^ 2) := by
    rw [hKn, div_div_eq_mul_div, div_pow, mul_pow, hsq4]
    field_simp
  have hsvK : s * v = K * (1 / A) := by rw [hsv, e1]
  have hsv2 : s * v = 4 / Real.sqrt π * σ * s := by rw [hv]; ring
  have key : Kn ^ 2 = (4 / (3 * Real.sqrt π) * (2 * a0 * t / σr) * (σ / σr) ^ ((n - 1) / 2)) ^ 2 := by
    rw [lhs2, mul_pow, e3, hρ]
    -- express everything through s·v
    have hsv_ne : s * v ≠ 0 := by rw [hsvK, hK, e2, hSg]; positivity
    have hs2 : s ^ 2 = (s * v) ^ 2 / v ^ 2 := by
      have hvne : v ≠ 0 := by rw [hv]; positivity
      field_simp
    rw [hs2]
    have hv2 : v ^ 2 = 16 / π * σ ^ 2 := by
      rw [hv, mul_pow, div_pow, hspi2]; ring
    rw [hv2, hsvK, hK, e2, hSg]
    field_simp
    rw [hspi2]
    ring
  have := (sq_eq_sq₀ hKnpos.le hRpos.le).mp key
  exact this

/-! ## 4. The halo σ_h solve is unique for q < 2 (DW1 M3) -/

/-- **M3.** With σ_h = V_max/√2 and V_max² = π G Σ(σ_h) r₀ m₁, Σ(σ) = Σ_a0 (σ/σ_ref)^q, the solve reduces to
σ_h² = C σ_h^q with C = π G Σ_a0 σ_ref^(−q) r₀ m₁ / 2 > 0. For q < 2 it has exactly one positive solution,
σ_h = C^(1/(2−q)). -/
theorem sigma_h_unique (C q : ℝ) (hC : 0 < C) (hq : q < 2) :
    ∃! x : ℝ, 0 < x ∧ x ^ (2 : ℝ) = C * x ^ q := by
  have h2q : (2 - q) ≠ 0 := by linarith
  refine ⟨C ^ (2 - q)⁻¹, ⟨Real.rpow_pos_of_pos hC _, ?_⟩, ?_⟩
  · have hx : 0 < C ^ (2 - q)⁻¹ := Real.rpow_pos_of_pos hC _
    have : (C ^ (2 - q)⁻¹) ^ (2 - q) = C := Real.rpow_inv_rpow hC.le h2q
    calc (C ^ (2 - q)⁻¹) ^ (2 : ℝ) = (C ^ (2 - q)⁻¹) ^ ((2 - q) + q) := by ring_nf
      _ = (C ^ (2 - q)⁻¹) ^ (2 - q) * (C ^ (2 - q)⁻¹) ^ q := Real.rpow_add hx _ _
      _ = C * (C ^ (2 - q)⁻¹) ^ q := by rw [this]
  · rintro y ⟨hy, hyeq⟩
    have hyq : 0 < y ^ q := Real.rpow_pos_of_pos hy q
    have hsplit : y ^ (2 : ℝ) = y ^ (2 - q) * y ^ q := by
      rw [← Real.rpow_add hy]; ring_nf
    have h1 : y ^ (2 - q) = C := by
      have := hsplit ▸ hyeq
      exact mul_right_cancel₀ (ne_of_gt hyq) this
    calc y = (y ^ (2 - q)) ^ (2 - q)⁻¹ := (Real.rpow_rpow_inv hy.le h2q).symm
      _ = C ^ (2 - q)⁻¹ := by rw [h1]

end CoreLawCerts

/-! ## Axiom audit -/
#print axioms CoreLawCerts.q_to_n
#print axioms CoreLawCerts.os1_n_values
#print axioms CoreLawCerts.sigma_ratio
#print axioms CoreLawCerts.gamma_t_one
#print axioms CoreLawCerts.no_collapse
#print axioms CoreLawCerts.knudsen_closed_form
#print axioms CoreLawCerts.sigma_h_unique
