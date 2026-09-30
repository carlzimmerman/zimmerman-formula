import Mathlib

open Real

/-!
# P8: the cosmology lock  Omega_Lambda = 32 pi a0^2/(3 H0^2 c^2)  (lane V, evidence; the algebra and the arithmetic of the audit's numbers)

Conventions: c > 0 the speed of light (kept), Lambda = 3 H0^2 Omega_Lambda/c^2 (flat cosmology, H0 the Hubble rate, Omega_Lambda the dark-energy fraction), the puzzle in SI form Lambda c^4 = 32 pi a0^2.

CERTIFIED (premises => conclusions):
 (a) `omega_iff`: with Lambda = 3 H0^2 Omega_Lambda/c^2: Lambda = 32 pi a0^2/c^4  <=>  Omega_Lambda = 32 pi a0^2/(3 H0^2 c^2)  (algebra).
 (b) `omega_Z`: with a0 = c H0 sqrt(Omega_Lambda)/Z (a0 = c H_Lambda/Z, H_Lambda^2 = Omega_Lambda H0^2): Omega_Lambda = 32 pi a0^2/(3 H0^2 c^2) <=> Z^2 = 32 pi/3 (Omega_Lambda > 0).
 (c) `omega_pred_bounds`: ARITHMETIC ON DECLARED INPUTS (not a physics claim): with a0 = 1.0766e-10 m/s^2 (the record's SPARC fit), H0 = 67.4 km/s/Mpc = 2.1843e-18 1/s (Mpc = 3.0857e22 m) and c = 299792458 m/s,
     the formula gives 0.905 < Omega_Lambda,pred < 0.907 (audit: 0.906); `omega_shift_bounds`: the a0' that returns the measured 0.685 exactly satisfies 0.868 < a0'/a0 < 0.871, i.e. a0 would have to fall by about 13% (lane V: 13.0%).

NOT certified: the values of a0, H0, Omega_Lambda (data); that the formula holds in nature (the framework's kappa = 1/2 is FITTED); the statistical significance of the difference (lane V: 1.7-2.6 sigma by estimator, inside the systematics).
-/

namespace OmegaLambda

theorem omega_iff {c H0 Ω a0 Λ : ℝ} (hc : 0 < c) (hH : 0 < H0) (hΛ : Λ = 3 * H0 ^ 2 * Ω / c ^ 2) :
    Λ = 32 * π * a0 ^ 2 / c ^ 4 ↔ Ω = 32 * π * a0 ^ 2 / (3 * H0 ^ 2 * c ^ 2) := by
  have hc0 : c ≠ 0 := hc.ne'
  have hH0 : H0 ≠ 0 := hH.ne'
  rw [hΛ]
  constructor
  · intro h
    field_simp at h ⊢
    nlinarith [h]
  · intro h
    rw [h]; field_simp

theorem omega_Z {c H0 Ω a0 Z : ℝ} (hc : 0 < c) (hH : 0 < H0) (hΩ : 0 < Ω) (hZ : 0 < Z)
    (ha : a0 = c * H0 * Real.sqrt Ω / Z) :
    Ω = 32 * π * a0 ^ 2 / (3 * H0 ^ 2 * c ^ 2) ↔ Z ^ 2 = 32 * π / 3 := by
  have hp := Real.pi_pos
  have hc0 : c ≠ 0 := hc.ne'
  have hH0 : H0 ≠ 0 := hH.ne'
  have hZ0 : Z ≠ 0 := hZ.ne'
  have hs := Real.sq_sqrt hΩ.le
  have hsq : a0 ^ 2 = c ^ 2 * H0 ^ 2 * Ω / Z ^ 2 := by
    rw [ha, div_pow, mul_pow, mul_pow, hs]
  rw [hsq]
  have : 32 * π * (c ^ 2 * H0 ^ 2 * Ω / Z ^ 2) / (3 * H0 ^ 2 * c ^ 2) = 32 * π * Ω / (3 * Z ^ 2) := by
    field_simp
  rw [this]
  have hZ2 : 0 < Z ^ 2 := by positivity
  rw [eq_div_iff (by positivity)]
  constructor
  · intro h
    have : Ω * (3 * Z ^ 2 - 32 * π) = 0 := by nlinarith [h]
    rcases mul_eq_zero.mp this with h1 | h1
    · exact absurd h1 hΩ.ne'
    · linarith
  · intro h
    nlinarith [h]

theorem omega_pred_bounds {a0 H0 c : ℝ} (ha : a0 = 1.0766e-10) (hH : H0 = 2.1843e-18) (hc : c = 299792458) :
    0.905 < 32 * π * a0 ^ 2 / (3 * H0 ^ 2 * c ^ 2) ∧ 32 * π * a0 ^ 2 / (3 * H0 ^ 2 * c ^ 2) < 0.907 := by
  have h1 := Real.pi_gt_d4
  have h2 := Real.pi_lt_d4
  subst ha hH hc
  have hd : (0:ℝ) < 3 * (2.1843e-18) ^ 2 * (299792458:ℝ) ^ 2 := by norm_num
  constructor
  · rw [lt_div_iff₀ hd]; nlinarith
  · rw [div_lt_iff₀ hd]; nlinarith

theorem omega_shift_bounds {a0 a0' H0 c : ℝ} (ha : a0 = 1.0766e-10) (hH : H0 = 2.1843e-18) (hc : c = 299792458)
    (ha' : 0 < a0') (hΩ : 32 * π * a0' ^ 2 / (3 * H0 ^ 2 * c ^ 2) = 0.685) :
    0.868 < a0' / a0 ∧ a0' / a0 < 0.871 := by
  have h1 := Real.pi_gt_d4
  have h2 := Real.pi_lt_d4
  have hp := Real.pi_pos
  subst ha hH hc
  have hd : (0:ℝ) < 3 * (2.1843e-18) ^ 2 * (299792458:ℝ) ^ 2 := by norm_num
  rw [div_eq_iff hd.ne'] at hΩ
  have hq : (a0' / 1.0766e-10) ^ 2 = a0' ^ 2 / (1.0766e-10) ^ 2 := by rw [div_pow]
  constructor
  · by_contra hcon
    have hcon := not_lt.mp hcon
    have h3 : a0' ≤ 0.868 * 1.0766e-10 := by rwa [div_le_iff₀ (by norm_num)] at hcon
    have h4 : a0' ^ 2 ≤ (0.868 * 1.0766e-10) ^ 2 := pow_le_pow_left₀ ha'.le h3 2
    nlinarith
  · by_contra hcon
    have hcon := not_lt.mp hcon
    have h3 : 0.871 * 1.0766e-10 ≤ a0' := by rwa [le_div_iff₀ (by norm_num)] at hcon
    have h4 : (0.871 * 1.0766e-10) ^ 2 ≤ a0' ^ 2 := pow_le_pow_left₀ (by norm_num) h3 2
    nlinarith

end OmegaLambda

#print axioms OmegaLambda.omega_iff
#print axioms OmegaLambda.omega_Z
#print axioms OmegaLambda.omega_pred_bounds
#print axioms OmegaLambda.omega_shift_bounds
