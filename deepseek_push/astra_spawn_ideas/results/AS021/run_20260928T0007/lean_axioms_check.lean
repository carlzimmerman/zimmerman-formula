import Mathlib

/-!
# AS021 — Sign and domain of the vacuum scale: Lean 4 certificates

Certifies the algebraic core of the framework identity
    a0 = kappa * c * sqrt(G * rho_Lambda),   kappa = 1/2 adopted,
at the real-algebra level (all quantities : ℝ, SI values irrelevant here).

Theorems:
  T1  as021_density_positive      : a0 > 0 with kappa,c,G > 0 forces rho_Lambda > 0
                                    (domain: no real positive a0 at rho_Lambda <= 0).
  T2  as021_zero_scale_iff_zero_density : a0 = 0  <->  rho_Lambda = 0 (under rho_Lambda >= 0).
  T3  as021_four_a0sq             : kappa = 1/2  =>  4 a0^2 = G c^2 rho_Lambda
                                    (the framework conversion rho = 4 a0^2/(G c^2),
                                     cleared algebraic form).
  T4  as021_q_newtonian_sandwich  : 0 < B, 0 < a0  =>  B < sqrt(B^2 + a0 B) < B + a0/2
                                    (Q branch: total exceeds Newtonian, first
                                     correction a0/2 is a strict upper bound).
-/

-- T1: positive couplings + positive scale force positive vacuum density.
theorem as021_density_positive
    {a0 kappa c G rhoL : ℝ}
    (h : a0 = kappa * c * Real.sqrt (G * rhoL))
    (ha0 : 0 < a0) (hk : 0 < kappa) (hc : 0 < c) (hG : 0 < G) :
    0 < rhoL := by
  have heq : (kappa * c) * Real.sqrt (G * rhoL) = a0 := by
    rw [← h]
  have h1 : 0 < (kappa * c) * Real.sqrt (G * rhoL) := by
    simpa [heq] using ha0
  have hkc : 0 < kappa * c := mul_pos hk hc
  have hs : 0 < Real.sqrt (G * rhoL) := pos_of_mul_pos_right h1 (le_of_lt hkc)
  have hgr : 0 < G * rhoL := Real.sqrt_pos.mp hs
  exact (mul_pos_iff_of_pos_left hG).mp hgr

-- T2: with rho_Lambda >= 0, the scale vanishes iff the vacuum density vanishes.
theorem as021_zero_scale_iff_zero_density
    {a0 kappa c G rhoL : ℝ}
    (h : a0 = kappa * c * Real.sqrt (G * rhoL))
    (hk : 0 < kappa) (hc : 0 < c) (hG : 0 < G) (hrho : 0 ≤ rhoL) :
    a0 = 0 ↔ rhoL = 0 := by
  constructor
  · intro ha0
    have heq : (kappa * c) * Real.sqrt (G * rhoL) = 0 := by
      rw [← h, ha0]
    have hkc_ne : kappa * c ≠ 0 := ne_of_gt (mul_pos hk hc)
    have hs0 : Real.sqrt (G * rhoL) = 0 := (mul_eq_zero.mp heq).resolve_left hkc_ne
    have hgr : G * rhoL = 0 := (Real.sqrt_eq_zero (mul_nonneg (le_of_lt hG) hrho)).mp hs0
    exact (mul_eq_zero.mp hgr).resolve_left (ne_of_gt hG)
  · intro hrho0
    rw [h, hrho0]
    simp [Real.sqrt_zero]

-- T3: squared identity and the 4 a0^2 = G c^2 rho_Lambda conversion (kappa = 1/2).
theorem as021_four_a0sq
    {a0 kappa c G rhoL : ℝ}
    (h : a0 = kappa * c * Real.sqrt (G * rhoL))
    (hk : kappa = (1 / 2 : ℝ))
    (hG : 0 ≤ G) (hrho : 0 ≤ rhoL) :
    4 * a0 ^ 2 = G * c ^ 2 * rhoL := by
  have hnon : 0 ≤ G * rhoL := mul_nonneg hG hrho
  calc
    4 * a0 ^ 2 = 4 * (kappa * c * Real.sqrt (G * rhoL)) ^ 2 := by rw [h]
    _ = 4 * ((1 / 2 : ℝ) * c * Real.sqrt (G * rhoL)) ^ 2 := by rw [hk]
    _ = 4 * (1 / 2 : ℝ) ^ 2 * c ^ 2 * (Real.sqrt (G * rhoL)) ^ 2 := by ring
    _ = 4 * (1 / 2 : ℝ) ^ 2 * c ^ 2 * (G * rhoL) := by rw [Real.sq_sqrt hnon]
    _ = G * c ^ 2 * rhoL := by ring

-- T4: Q-branch Newtonian sandwich:  B < g < B + a0/2  for  g = sqrt(B^2 + a0 B).
theorem as021_q_newtonian_sandwich
    {B a0 : ℝ} (hB : 0 < B) (ha0 : 0 < a0) :
    B < Real.sqrt (B ^ 2 + a0 * B) ∧ Real.sqrt (B ^ 2 + a0 * B) < B + a0 / 2 := by
  have hpos : 0 < B ^ 2 + a0 * B := by nlinarith [sq_pos_of_pos hB, mul_pos ha0 hB]
  have hB2 : B = Real.sqrt (B ^ 2) := by rw [Real.sqrt_sq (le_of_lt hB)]
  constructor
  · rw [hB2]
    exact Real.sqrt_lt_sqrt (sq_nonneg B) (by nlinarith [mul_pos ha0 hB])
  · apply (Real.sqrt_lt (le_of_lt hpos) (by nlinarith [hB, ha0])).2
    nlinarith [sq_pos_of_pos ha0]

-- Corollary of T4: the Q-branch correction (g - B) is strictly between 0 and a0/2.
theorem as021_q_correction_bounds
    {B a0 : ℝ} (hB : 0 < B) (ha0 : 0 < a0) :
    0 < Real.sqrt (B ^ 2 + a0 * B) - B ∧ Real.sqrt (B ^ 2 + a0 * B) - B < a0 / 2 := by
  have hs := as021_q_newtonian_sandwich hB ha0
  constructor <;> linarith [hs.1, hs.2]

#print axioms as021_density_positive
#print axioms as021_zero_scale_iff_zero_density
#print axioms as021_four_a0sq
#print axioms as021_q_newtonian_sandwich
#print axioms as021_q_correction_bounds
