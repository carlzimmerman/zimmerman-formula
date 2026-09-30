import Mathlib

open Real

/-!
# P6: dimension-dependence bookkeeping (lane F)

Conventions: d = number of spatial dimensions (spacetime D = d + 1), c = 1, G = G_D the Einstein coupling; dim SO(d) = d(d-1)/2.
The physics inputs (the D-dimensional Friedmann equations, the Tangherlini metric, the volume-law chain) are TAKEN from lane F as premises; Lean certifies the algebra.

CERTIFIED (premises => conclusions):
 (a) `acc_coeff_d3`: the D-dimensional Friedmann acceleration coefficient ((d-2) rho + d p)/(d(d-1)) at d = 3 is (rho + 3 p)/6 (the 4D law, addot/a = -8 pi G (rho + 3p)/6);
     `vacuum_numerator`: for p = -rho the numerator is -2 rho for EVERY d; `tolman_naive_ne`: (d-2) rho + d p = rho + d p iff d = 3 (rho != 0), so the "Tolman count d-1"
     (rho + d p) coincides with the computed law only at d = 3.
 (b) `Z_f_sq`, `Z_d_sq`: from H^2 = 16 pi G rho/(d(d-1)): Z_f^2 = 16 pi/(d(d-1)) (R* = Z_f L), = 8 pi/3 at d = 3; with kappa: Z_d^2 = Z_f^2/kappa^2 and Z_d^2 (dim SO(d)) kappa^2 = 8 pi for ANY kappa;
     kappa = 1/2: Z_d^2 = 64 pi/(d(d-1)) = 32 pi/dim SO(d), = 32 pi/3 at d = 3 (`Z_d_half`).
 (c) `Z_V_eq_six_iff`: the volume-law value Z_V(d) = d(d-1)/(d-2) = 2 dim SO(d)/(d-2) equals 6 iff d = 3 OR d = 4 (so 6 is not a d = 3 selector); `Z_V_values`: 6 at d = 3, 6 at d = 4, 20/3 at d = 5.
 (d) `euler_units`: (4 pi)^n n! = 4 pi, 32 pi^2, 384 pi^3, 6144 pi^4 (n = 1..4); Chern units (2 pi)^n n! = 2 pi, 8 pi^2, 48 pi^3, 384 pi^4; Euler/Chern = 2^n (`euler_over_chern`).
 (e) `kappa_tangherlini`: surface gravity (d-2)/(2 r_s) at r_s = R* = 1/sqrt(G rho) gives kappa = (d-2)/2 (1/2 at d = 3); `kappa_fixedZ_sq`: with the d = 3 value of Z held fixed, kappa_d^2 = 3/(2 d (d-1)).
(That every reading equals 1/2 at d = 3 is the normalisation, not a finding: nothing here selects among the d-dependences.)

NOT certified: that any reading is physical; kappa = 1/2 (FITTED).
-/

namespace Dimension

/-- the D-dimensional Friedmann acceleration coefficient -/
noncomputable def accCoeff (d ρ p : ℝ) : ℝ := ((d - 2) * ρ + d * p) / (d * (d - 1))

theorem acc_coeff_d3 (ρ p : ℝ) : accCoeff 3 ρ p = (ρ + 3 * p) / 6 := by
  unfold accCoeff; ring

theorem vacuum_numerator (d ρ : ℝ) : (d - 2) * ρ + d * (-ρ) = -2 * ρ := by ring

theorem tolman_naive_ne {d ρ p : ℝ} (hρ : ρ ≠ 0) : (d - 2) * ρ + d * p = ρ + d * p ↔ d = 3 := by
  constructor
  · intro h
    have : (d - 3) * ρ = 0 := by linarith
    rcases mul_eq_zero.mp this with h1 | h1
    · linarith
    · exact absurd h1 hρ
  · intro h; rw [h]; ring

/-- H^2 = 16 pi G rho/(d(d-1)), so with H = 1/L: 1/(G rho) = 16 pi L^2/(d(d-1)); R* = 1/sqrt(G rho): Z_f^2 = R*^2/L^2 = 16 pi/(d(d-1)) -/
theorem Z_f_sq {d G ρ L : ℝ} (hd : d * (d - 1) ≠ 0) (hG : 0 < G) (hρ : 0 < ρ) (hL : 0 < L)
    (hF : (1 / L) ^ 2 = 16 * π * G * ρ / (d * (d - 1))) :
    (1 / Real.sqrt (G * ρ)) ^ 2 / L ^ 2 = 16 * π / (d * (d - 1)) := by
  have hL0 : L ≠ 0 := hL.ne'
  have hGρ : 0 < G * ρ := by positivity
  have h2 := Real.sq_sqrt hGρ.le
  have hp := Real.pi_pos
  have h3 : d * (d - 1) = 16 * π * G * ρ * L ^ 2 := by
    rw [div_pow, one_pow, div_eq_div_iff (by positivity) hd] at hF
    linarith
  rw [div_pow, one_pow, h2, div_div, div_eq_div_iff (by positivity) hd]
  linarith

theorem Z_f_sq_d3 : 16 * π / (3 * (3 - 1)) = 8 * π / 3 := by ring

/-- non-vacuity and the d = 3 value: with d = 3, G = 1, rho = 3/(8 pi), L = 1 the premise H^2 = 16 pi G rho/(d(d-1)) holds and R*^2/L^2 = 8 pi/3 -/
theorem Z_f_sq_instance : (1 / Real.sqrt (1 * (3 / (8 * π)))) ^ 2 / 1 ^ 2 = 8 * π / 3 := by
  have hp := Real.pi_pos
  have h := Z_f_sq (d := 3) (G := 1) (ρ := 3 / (8 * π)) (L := 1) (by norm_num) one_pos (by positivity) one_pos
    (by field_simp; norm_num)
  rw [h]; ring

/-- Z_d = Z_f/kappa: Z_d^2 dim SO(d) kappa^2 = 8 pi for any kappa; kappa = 1/2 gives 64 pi/(d(d-1)) = 32 pi/dim SO(d) -/
theorem Z_d_sq {d κ : ℝ} (hd : d * (d - 1) ≠ 0) (hκ : κ ≠ 0) :
    (16 * π / (d * (d - 1)) / κ ^ 2) * (d * (d - 1) / 2) * κ ^ 2 = 8 * π := by
  have hd1 : d ≠ 0 := left_ne_zero_of_mul hd
  have hd2 : d - 1 ≠ 0 := right_ne_zero_of_mul hd
  field_simp
  norm_num

theorem Z_d_half {d : ℝ} (hd : d * (d - 1) ≠ 0) :
    16 * π / (d * (d - 1)) / (1 / 2) ^ 2 = 64 * π / (d * (d - 1)) ∧ 64 * π / (d * (d - 1)) = 32 * π / (d * (d - 1) / 2) ∧
    64 * π / (3 * (3 - 1)) = 32 * π / 3 := by
  have hd1 : d ≠ 0 := left_ne_zero_of_mul hd
  have hd2 : d - 1 ≠ 0 := right_ne_zero_of_mul hd
  refine ⟨?_, ?_, ?_⟩
  · field_simp; ring
  · field_simp; ring
  · ring

/-- the volume-law value Z_V(d) = d(d-1)/(d-2) equals 6 iff d = 3 or d = 4 -/
theorem Z_V_eq_six_iff {d : ℝ} (hd : d ≠ 2) : d * (d - 1) / (d - 2) = 6 ↔ d = 3 ∨ d = 4 := by
  have hd2 : d - 2 ≠ 0 := sub_ne_zero.mpr hd
  rw [div_eq_iff hd2]
  constructor
  · intro h
    have : (d - 3) * (d - 4) = 0 := by nlinarith [h]
    rcases mul_eq_zero.mp this with h1 | h1
    · left; linarith
    · right; linarith
  · rintro (h | h) <;> rw [h] <;> norm_num

theorem Z_V_values : (3 : ℝ) * (3 - 1) / (3 - 2) = 6 ∧ (4 : ℝ) * (4 - 1) / (4 - 2) = 6 ∧ (5 : ℝ) * (5 - 1) / (5 - 2) = 20 / 3 := by
  refine ⟨by norm_num, by norm_num, by norm_num⟩

/-- (d) Euler units (4 pi)^n n! and Chern units (2 pi)^n n! -/
theorem euler_units :
    (4 * π) ^ 1 * (Nat.factorial 1 : ℝ) = 4 * π ∧ (4 * π) ^ 2 * (Nat.factorial 2 : ℝ) = 32 * π ^ 2 ∧
    (4 * π) ^ 3 * (Nat.factorial 3 : ℝ) = 384 * π ^ 3 ∧ (4 * π) ^ 4 * (Nat.factorial 4 : ℝ) = 6144 * π ^ 4 := by
  refine ⟨?_, ?_, ?_, ?_⟩ <;> simp [Nat.factorial] <;> ring

theorem chern_units :
    (2 * π) ^ 1 * (Nat.factorial 1 : ℝ) = 2 * π ∧ (2 * π) ^ 2 * (Nat.factorial 2 : ℝ) = 8 * π ^ 2 ∧
    (2 * π) ^ 3 * (Nat.factorial 3 : ℝ) = 48 * π ^ 3 ∧ (2 * π) ^ 4 * (Nat.factorial 4 : ℝ) = 384 * π ^ 4 := by
  refine ⟨?_, ?_, ?_, ?_⟩ <;> simp [Nat.factorial] <;> ring

theorem euler_over_chern (n : ℕ) : (4 * π) ^ n * (Nat.factorial n : ℝ) / ((2 * π) ^ n * (Nat.factorial n : ℝ)) = 2 ^ n := by
  have hp := Real.pi_pos
  have hf : (Nat.factorial n : ℝ) ≠ 0 := by positivity
  rw [show (4 * π) ^ n = 2 ^ n * (2 * π) ^ n by rw [← mul_pow]; ring_nf]
  field_simp

/-- (e) Tangherlini: a0 = (d-2)/(2 r_s) with r_s = R* = 1/sqrt(G rho): a0 = ((d-2)/2) sqrt(G rho), so kappa = (d-2)/2 -/
theorem kappa_tangherlini {d G ρ : ℝ} (hG : 0 < G) (hρ : 0 < ρ) :
    (d - 2) / (2 * (1 / Real.sqrt (G * ρ))) = ((d - 2) / 2) * Real.sqrt (G * ρ) := by
  have hs : 0 < Real.sqrt (G * ρ) := Real.sqrt_pos.mpr (by positivity)
  field_simp

/-- with Z held at its d = 3 value Z^2 = 32 pi/3: kappa_d^2 = Z_f(d)^2/Z^2 = 3/(2 d (d-1)) -/
theorem kappa_fixedZ_sq {d : ℝ} (hd : d * (d - 1) ≠ 0) :
    (16 * π / (d * (d - 1))) / (32 * π / 3) = 3 / (2 * d * (d - 1)) := by
  have hp := Real.pi_pos
  have hd1 : d ≠ 0 := left_ne_zero_of_mul hd
  have hd2 : d - 1 ≠ 0 := right_ne_zero_of_mul hd
  field_simp
  ring

end Dimension

#print axioms Dimension.acc_coeff_d3
#print axioms Dimension.tolman_naive_ne
#print axioms Dimension.Z_f_sq
#print axioms Dimension.Z_f_sq_instance
#print axioms Dimension.Z_d_sq
#print axioms Dimension.Z_d_half
#print axioms Dimension.Z_V_eq_six_iff
#print axioms Dimension.euler_units
#print axioms Dimension.chern_units
#print axioms Dimension.euler_over_chern
#print axioms Dimension.kappa_tangherlini
#print axioms Dimension.kappa_fixedZ_sq
