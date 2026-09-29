import Mathlib
import H4_graviton

/-! MUTATE controls for H4_graviton.lean: each `M4*` is a FALSE variant with the true proof script (must FAIL);
each `M4*_refuted` proves its negation from the true theorem (must COMPILE). -/

open MeasureTheory Set Real

-- M4a: h_ij h_ij = 3 h_+^2 (wrong; it is 2 h_+^2)
theorem M4a_hij_sq_plus_wrong (hp : ℝ) : ∑ i, ∑ j, (hp * ePlus i j) ^ 2 = 3 * hp ^ 2 := by
  simp [Fin.sum_univ_three, ePlus]; ring

theorem M4a_refuted : ¬ (∀ hp : ℝ, ∑ i, ∑ j, (hp * ePlus i j) ^ 2 = 3 * hp ^ 2) := by
  intro h; have := h 1; rw [hij_sq_plus] at this; norm_num at this

-- M4b: kappa_g^2 = 16 pi G <-> canonical (1/2) coefficient (wrong: it is 32 pi G)
theorem M4b_kappa_g_wrong {G κ : ℝ} (hG : 0 < G) : κ ^ 2 = 16 * π * G ↔ κ ^ 2 / (64 * π * G) = 1 / 2 := by
  have hp := Real.pi_pos
  have : 64 * π * G ≠ 0 := by positivity
  rw [div_eq_iff this]
  constructor <;> intro h <;> linarith

theorem M4b_refuted : ¬ (∀ G κ : ℝ, 0 < G → (κ ^ 2 = 16 * π * G ↔ κ ^ 2 / (64 * π * G) = 1 / 2)) := by
  intro h
  have hp := Real.pi_pos
  -- take G = 1, kappa^2 = 32 pi: the right side holds, the left side (= 16 pi) does not
  have h1 := h 1 (Real.sqrt (32 * π)) one_pos
  have hsq : Real.sqrt (32 * π) ^ 2 = 32 * π := Real.sq_sqrt (by positivity)
  have hr : Real.sqrt (32 * π) ^ 2 / (64 * π * 1) = 1 / 2 := by rw [hsq]; field_simp; ring
  have := h1.mpr hr
  rw [hsq] at this
  nlinarith

-- M4c: canonical normalisation with 1/(32 pi G) instead of 1/(64 pi G)
theorem M4c_canonical_wrong {G : ℝ} (hG : 0 < G) (x : ℝ) :
    (1 / (32 * π * G)) * (2 * x ^ 2) = (1 / 2) * (x / Real.sqrt (16 * π * G)) ^ 2 := by
  have hp := Real.pi_pos
  have h0 : 0 ≤ 16 * π * G := by positivity
  rw [div_pow, Real.sq_sqrt h0]
  have : 16 * π * G ≠ 0 := by positivity
  field_simp
  ring

theorem M4c_refuted : ¬ (∀ G : ℝ, 0 < G → ∀ x : ℝ, (1 / (32 * π * G)) * (2 * x ^ 2) = (1 / 2) * (x / Real.sqrt (16 * π * G)) ^ 2) := by
  intro h
  have hp := Real.pi_pos
  have h1 := h 1 one_pos 1
  have h2 := canonical_plus (G := 1) one_pos 1
  have h3 : (1 / (32 * π * 1)) * (2 * (1:ℝ) ^ 2) = (1 / (64 * π * 1)) * (2 * (1:ℝ) ^ 2) := h1.trans h2.symm
  field_simp at h3
  nlinarith

-- M4d: average of sin^2 over a period is 1/2, not 1/3
theorem M4d_avg_sin_sq_wrong {ω φ : ℝ} (hω : 0 < ω) :
    (1 / (2 * π / ω)) * ∫ t in (0:ℝ)..(2 * π / ω), Real.sin (ω * t + φ) ^ 2 = 1 / 3 := by
  have hp := Real.pi_pos
  rw [int_sin_sq_period hω]
  field_simp

theorem M4d_refuted {ω φ : ℝ} (hω : 0 < ω) :
    ¬ ((1 / (2 * π / ω)) * ∫ t in (0:ℝ)..(2 * π / ω), Real.sin (ω * t + φ) ^ 2 = 1 / 3) := by
  intro h; rw [avg_sin_sq hω] at h; norm_num at h

-- M4e: Isaacson with 1/(16 pi G) (wrong for the h_ij h_ij form; that is the <hdot_+^2 + hdot_x^2> form)
theorem M4e_isaacson_wrong {G h0 ω : ℝ} (_hG : 0 < G) (hω : 0 < ω) :
    ((1 / (2 * π / ω)) * ∫ t in (0:ℝ)..(2 * π / ω),
        ∑ i, ∑ j, (deriv (wave h0 ω 0) t * ePlus i j) ^ 2) / (16 * π * G) = ω ^ 2 * h0 ^ 2 / (32 * π * G) := by
  rw [avg_hdot_ij_sq_plus hω]

theorem M4e_refuted : ¬ (∀ G h0 ω : ℝ, 0 < G → 0 < ω →
    ((1 / (2 * π / ω)) * ∫ t in (0:ℝ)..(2 * π / ω),
        ∑ i, ∑ j, (deriv (wave h0 ω 0) t * ePlus i j) ^ 2) / (16 * π * G) = ω ^ 2 * h0 ^ 2 / (32 * π * G)) := by
  intro h
  have hp := Real.pi_pos
  have h1 := h 1 1 1 one_pos one_pos
  rw [avg_hdot_ij_sq_plus one_pos] at h1
  field_simp at h1
  nlinarith

-- M4f: the time average of the canonical energy density is (A omega)^2/2, not (A omega)^2
theorem M4f_canonical_energy_wrong {A ω x : ℝ} (hω : 0 < ω) :
    (1 / (2 * π / ω)) * ∫ t in (0:ℝ)..(2 * π / ω),
        ((1 / 2) * (deriv (fun s => cwave A ω s x) t) ^ 2 + (1 / 2) * (deriv (fun y => cwave A ω t y) x) ^ 2)
      = (A * ω) ^ 2 := by
  have hp := Real.pi_pos
  have e : ∀ t : ℝ, ((1 / 2) * (deriv (fun s => cwave A ω s x) t) ^ 2 + (1 / 2) * (deriv (fun y => cwave A ω t y) x) ^ 2)
      = (A * ω) ^ 2 * Real.sin (ω * t + (-(ω * x))) ^ 2 := by
    intro t
    rw [(cwave_dt A ω t x).deriv, (cwave_dx A ω t x).deriv]
    have : ω * t + -(ω * x) = ω * t - ω * x := by ring
    rw [this]; ring
  simp_rw [e]
  rw [intervalIntegral.integral_const_mul, int_sin_sq_period hω]
  field_simp

theorem M4f_refuted {A ω x : ℝ} (hA : A ≠ 0) (hω : 0 < ω) :
    ¬ ((1 / (2 * π / ω)) * ∫ t in (0:ℝ)..(2 * π / ω),
        ((1 / 2) * (deriv (fun s => cwave A ω s x) t) ^ 2 + (1 / 2) * (deriv (fun y => cwave A ω t y) x) ^ 2)
      = (A * ω) ^ 2) := by
  intro h
  rw [canonical_energy_avg hω] at h
  have : (A * ω) ^ 2 > 0 := by positivity
  linarith

#print axioms M4a_refuted
#print axioms M4b_refuted
#print axioms M4c_refuted
#print axioms M4d_refuted
#print axioms M4e_refuted
#print axioms M4f_refuted
#print axioms M4a_hij_sq_plus_wrong
#print axioms M4b_kappa_g_wrong
#print axioms M4c_canonical_wrong
#print axioms M4d_avg_sin_sq_wrong
#print axioms M4e_isaacson_wrong
#print axioms M4f_canonical_energy_wrong
