/-
  CA1_covariant_self_coupling — Lean 4 + Mathlib certificates for the slope and scale algebra of the cold dark energy's
  self-coupling candidates.

  Certifies ALGEBRA from stated premises only. It does not certify any physical premise (the classical cross-section
  formula, the pair-exchange operator powers, the core condition) or any measured number. κ = ½ is FITTED.

  Compile: cd fable_independent_2026/lean_2026 && lake env lean <path>/CA1Certs.lean
-/
import Mathlib

open Real

namespace CA1Certs

/-! ## 1. Slopes of contact and Coulomb-limit scattering lie outside both footings' windows (δn = 0.10) -/

/-- Contact scattering (n = 0) misses n = 0.784 and n = 0.496 by more than 0.10. -/
theorem contact_excluded : 1 / 10 < |(0 : ℝ) - 784 / 1000| ∧ 1 / 10 < |(0 : ℝ) - 496 / 1000| := by
  constructor <;> norm_num [abs_of_neg]

/-- Coulomb / Rutherford limit of a Yukawa mediator whose range is ≫ the halo (n = 4) misses both windows. -/
theorem coulomb_excluded : 1 / 10 < |(4 : ℝ) - 784 / 1000| ∧ 1 / 10 < |(4 : ℝ) - 496 / 1000| := by
  constructor <;> norm_num [abs_of_pos]

/-! ## 2. Power-law potential V = C/r^p: σ_T = A (C/E)^(2/p), E = μv²/2, scales as v^(−4/p) -/

/-- **Scaling.** Multiplying the speed by ℓ multiplies the classical cross-section by ℓ^(−4/p): n = 4/p, with no
velocity scale. -/
theorem powerlaw_scaling (A Cp μ v l p : ℝ) (hC : 0 < Cp) (hμ : 0 < μ) (hv : 0 < v) (hl : 0 < l) :
    A * (Cp / (μ * (l * v) ^ 2 / 2)) ^ (2 / p) = l ^ (-(4 / p)) * (A * (Cp / (μ * v ^ 2 / 2)) ^ (2 / p)) := by
  have hX : 0 < Cp / (μ * v ^ 2 / 2) := by positivity
  have hl2 : (0 : ℝ) ≤ l ^ 2 := sq_nonneg l
  have e1 : Cp / (μ * (l * v) ^ 2 / 2) = Cp / (μ * v ^ 2 / 2) * (l ^ 2)⁻¹ := by
    field_simp
  have e2 : (l ^ 2 : ℝ) ^ (2 / p) = l ^ (4 / p) := by
    rw [← Real.rpow_natCast, ← Real.rpow_mul hl.le]; norm_num; ring_nf
  rw [e1, Real.mul_rpow hX.le (inv_nonneg.mpr hl2), Real.inv_rpow hl2, e2, Real.rpow_neg hl.le]
  ring

/-! ## 3. Integer windows: |4/p − n| ≤ 1/10 -/

/-- Canonical footing (n = 0.784): only p = 5. -/
theorem canonical_window (p : ℕ) (hp : 1 ≤ p) : |4 / (p : ℝ) - 784 / 1000| ≤ 1 / 10 ↔ p = 5 := by
  constructor
  · intro h
    rw [abs_le] at h
    by_contra hne
    rcases lt_or_gt_of_ne hne with hlt | hgt
    · interval_cases p <;> norm_num at h
    · have h6 : (6 : ℝ) ≤ p := by exact_mod_cast hgt
      have : 4 / (p : ℝ) ≤ 4 / 6 := div_le_div_of_nonneg_left (by norm_num) (by norm_num) h6
      linarith [h.1]
  · rintro rfl; norm_num [abs_le]

/-- Alt footing (n = 0.496): exactly p ∈ {7, 8, 9, 10}. -/
theorem alt_window (p : ℕ) (hp : 1 ≤ p) : |4 / (p : ℝ) - 496 / 1000| ≤ 1 / 10 ↔ 7 ≤ p ∧ p ≤ 10 := by
  constructor
  · intro h
    rw [abs_le] at h
    by_contra hne
    rcases Nat.lt_or_ge p 7 with hlt | hge
    · interval_cases p <;> norm_num at h
    · have h11 : 11 ≤ p := by omega
      have h11r : (11 : ℝ) ≤ p := by exact_mod_cast h11
      have : 4 / (p : ℝ) ≤ 4 / 11 := div_le_div_of_nonneg_left (by norm_num) (by norm_num) h11r
      linarith [h.1]
  · rintro ⟨h7, h10⟩
    interval_cases p <;> norm_num [abs_le]

/-- **The footings split.** No integer power p serves both footings. -/
theorem no_common_power :
    ¬ ∃ p : ℕ, 1 ≤ p ∧ |4 / (p : ℝ) - 784 / 1000| ≤ 1 / 10 ∧ |4 / (p : ℝ) - 496 / 1000| ≤ 1 / 10 := by
  rintro ⟨p, hp, hc, ha⟩
  have h5 := (canonical_window p hp).mp hc
  have h7 := ((alt_window p hp).mp ha).1
  omega

/-! ## 4. Pair-exchange powers from operator dimension (natural units, energy exponents) -/

/-- A two-quantum exchange with vertex coefficients 1/M² each (dimension-6 current–current) gives V ∝ 1/(M⁴ r^p) with
energy dimension 1 iff p = 5; with an extra 1/m_χ² (derivative scalar pair, non-relativistic normalisation) iff p = 7. -/
theorem pair_exchange_powers (p : ℝ) : (p - 4 = 1 ↔ p = 5) ∧ (p - 6 = 1 ↔ p = 7) := by
  constructor <;> constructor <;> intro h <;> linarith

/-! ## 5. Velocities built from (G, c, a₀, ρ_Λ, t) -/

/-- **Dimensional obstruction.** G^a c^b a₀^d ρ_Λ^e t^f has the dimension of a velocity (M: −a + e = 0;
L: 3a + b + d − 3e = 1; T: −2a − b − 2d + f = −1) iff e = a, b = 1 − d, f = 2a + d, i.e. it equals
c · (a₀t/c)^d · (Gρ_Λt²)^a. Every velocity from these constants is c times powers of the two dimensionless groups. -/
theorem velocity_monomial (a b d e f : ℝ) :
    (-a + e = 0 ∧ 3 * a + b + d - 3 * e = 1 ∧ -2 * a - b - 2 * d + f = -1) ↔
      (e = a ∧ b = 1 - d ∧ f = 2 * a + d) := by
  constructor
  · rintro ⟨h1, h2, h3⟩
    refine ⟨by linarith, by linarith, by linarith⟩
  · rintro ⟨h1, h2, h3⟩
    refine ⟨by linarith, by linarith, by linarith⟩

end CA1Certs

#print axioms CA1Certs.contact_excluded
#print axioms CA1Certs.coulomb_excluded
#print axioms CA1Certs.powerlaw_scaling
#print axioms CA1Certs.canonical_window
#print axioms CA1Certs.alt_window
#print axioms CA1Certs.no_common_power
#print axioms CA1Certs.pair_exchange_powers
#print axioms CA1Certs.velocity_monomial
