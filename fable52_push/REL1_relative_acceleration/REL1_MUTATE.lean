/-
REL1_MUTATE (criteria e495153acf): deliberately false versions of REL1.lean's statements, with the true file's proof
attempts. Every one must fail; the file must not compile. TEST lane; adopts nothing. kappa = 1/2 FITTED; not theory closed.

  M_root_sign        : the runaway root with the wrong sign of rho (an oscillation claimed).
  M_k0               : the k = 0 root claimed to be -rho / Jpp.
  M_bounded          : the Ostrogradsky Hamiltonian claimed bounded below by -|p2| (p1 fixed to 0 is not general).
  M_across           : J'(y)/y claimed 1/(K (1+u)^2) (the along value).
  M_stiff            : the transverse stiffness value claimed to carry g.
-/
import Mathlib

namespace REL1M

theorem M_root_sign (rho Jpp k S : ℝ) (hJ : 0 < Jpp) (hS : S ^ 2 = rho ^ 2 + 4 * Jpp * k) :
    Jpp * ((-rho + S) / (2 * Jpp)) ^ 2 + rho * ((rho + S) / (2 * Jpp)) - k = 0 := by
  have hJ' : Jpp ≠ 0 := hJ.ne'
  have e : Jpp * ((-rho + S) / (2 * Jpp)) ^ 2 + rho * ((rho + S) / (2 * Jpp)) - k
      = (S ^ 2 - rho ^ 2 - 4 * Jpp * k) / (4 * Jpp) := by
    field_simp; ring
  rw [e, hS]; ring

theorem M_k0 (rho Jpp : ℝ) (hJ : 0 < Jpp) (hrho : 0 ≤ rho) :
    (rho + Real.sqrt (rho ^ 2 + 4 * Jpp * 0)) / (2 * Jpp) = -rho / Jpp := by
  have : Real.sqrt (rho ^ 2 + 4 * Jpp * 0) = rho := by
    rw [mul_zero, add_zero]; exact Real.sqrt_sq hrho
  rw [this]
  field_simp
  ring

theorem M_bounded (rho Jpp k q1 q2 p1 p2 : ℝ) (hJ : 0 < Jpp) (hq : q2 ≠ 0) :
    -|p2| ≤ p1 * q2 + p2 ^ 2 / (2 * Jpp) - rho * q2 ^ 2 / 2 + k * q1 ^ 2 / 2 := by
  nlinarith [abs_nonneg p2, sq_nonneg q1, sq_nonneg q2]

noncomputable def Jp (K a0 u : ℝ) : ℝ := (a0 / K) * (u / (1 + u))

theorem M_across (K a0 u : ℝ) (hK : K ≠ 0) (ha : a0 ≠ 0) (hu : 0 < u) :
    Jp K a0 u / (a0 * u) = 1 / (K * (1 + u) ^ 2) := by
  have h1 : (1 + u) ≠ 0 := by linarith
  unfold Jp
  field_simp

theorem M_stiff (m g kx ky : ℝ) (hm : 0 < m) (hg : 0 ≤ g) :
    let d := (m + g * kx ^ 2) * (m + g * ky ^ 2) - (g * kx * ky) ^ 2
    d ≠ 0 →
    (ky * ((m + g * ky ^ 2) * ky + (-(g * kx * ky)) * (-kx))
      + (-kx) * ((-(g * kx * ky)) * ky + (m + g * kx ^ 2) * (-kx))) / d
      = (kx ^ 2 + ky ^ 2) / (m + g) := by
  intro d hd
  have hd' : d = m * (m + g * (kx ^ 2 + ky ^ 2)) := by simp only [d]; ring
  rw [div_eq_div_iff hd (by positivity), hd']
  ring

end REL1M
-- kappa = 1/2 FITTED; not theory closed. Adopts nothing.
