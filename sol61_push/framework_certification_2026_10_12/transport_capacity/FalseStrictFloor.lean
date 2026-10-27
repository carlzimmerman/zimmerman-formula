import Mathlib

/-! FRAMEWORK-CERT-TRANSPORT-2026-10-12.
Declared two-real-amplitude Fourier receiver with Omega=c*|k|. No physical
receiver, collision measure, microcoupling, or target profile is inferred.
Energy and momentum ledgers below are explicit hypotheses for accessible states.
-/
noncomputable section
namespace FrameworkReceiverCapacity

def omega (c k : ℝ) : ℝ := c * |k|
def energy (c k p1 p2 x1 x2 : ℝ) : ℝ :=
  (p1 ^ 2 + p2 ^ 2 + omega c k ^ 2 * (x1 ^ 2 + x2 ^ 2)) / 2
def momentum (k p1 p2 x1 x2 : ℝ) : ℝ := -k * (p1 * x2 - p2 * x1)

theorem omega_squared (c k : ℝ) : omega c k ^ 2 = c ^ 2 * k ^ 2 := by
  unfold omega
  rw [mul_pow, sq_abs]

theorem energy_momentum_squares (c k p1 p2 x1 x2 : ℝ) :
    energy c k p1 p2 x1 x2 ^ 2 - c ^ 2 * momentum k p1 p2 x1 x2 ^ 2 =
      (p1 ^ 2 + p2 ^ 2 - omega c k ^ 2 * (x1 ^ 2 + x2 ^ 2)) ^ 2 / 4 +
        omega c k ^ 2 * (p1 * x1 + p2 * x2) ^ 2 := by
  unfold energy momentum
  rw [omega_squared]
  ring

theorem energy_nonnegative (c k p1 p2 x1 x2 : ℝ) :
    0 ≤ energy c k p1 p2 x1 x2 := by unfold energy; positivity

theorem receiver_floor (c k p1 p2 x1 x2 : ℝ) (hc : 0 ≤ c) :
    c * |momentum k p1 p2 x1 x2| ≤ energy c k p1 p2 x1 x2 := by
  have he := energy_nonnegative c k p1 p2 x1 x2
  have hs := energy_momentum_squares c k p1 p2 x1 x2
  have hp : 0 ≤ c * |momentum k p1 p2 x1 x2| := mul_nonneg hc (abs_nonneg _)
  have hr : 0 ≤
      (p1 ^ 2 + p2 ^ 2 - omega c k ^ 2 * (x1 ^ 2 + x2 ^ 2)) ^ 2 / 4 +
        omega c k ^ 2 * (p1 * x1 + p2 * x2) ^ 2 := by positivity
  have ha : |momentum k p1 p2 x1 x2| ^ 2 = momentum k p1 p2 x1 x2 ^ 2 := sq_abs _
  nlinarith

/-- Necessary, not sufficient: the final mode must satisfy both declared ledgers. -/
theorem accessible_transfer (c k p1 p2 x1 x2 E0 Δ P0 pb q : ℝ) (hc : 0 ≤ c)
    (hE : energy c k p1 p2 x1 x2 = E0 - Δ)
    (hP : momentum k p1 p2 x1 x2 = P0 - pb * q) :
    c * |P0 - pb * q| ≤ E0 - Δ := by
  simpa only [hE, hP] using receiver_floor c k p1 p2 x1 x2 hc

/-- Initially zero receiver momentum, positive transfer q, constant channel cost D. -/
theorem recoil_budget (c D pb E0 q : ℝ) (hq : 0 ≤ q)
    (haccess : c * |0 - pb * q| ≤ E0 - D * q) :
    (D + c * |pb|) * q ≤ E0 := by
  rw [zero_sub, abs_neg, abs_mul, abs_of_nonneg hq] at haccess
  nlinarith

/-- General ratio bound for reaching qeq, without numerical velocity fixtures. -/
theorem necessary_capacity_ratio (c D pb E0 qeq : ℝ) (hD : 0 < D) (hqeq : 0 < qeq)
    (haccess : c * |0 - pb * qeq| ≤ E0 - D * qeq) :
    1 + c * |pb| / D ≤ E0 / (D * qeq) := by
  have hb := recoil_budget c D pb E0 qeq hqeq.le haccess
  apply (le_div_iff₀ (mul_pos hD hqeq)).mpr
  have he : (1 + c * |pb| / D) * (D * qeq) = (D + c * |pb|) * qeq := by
    field_simp
  rw [he]
  exact hb

/-- For D=2*epsilon^2, pb=-2*epsilon, c=1 the floor is 1+1/epsilon. -/
theorem slow_recoil_ratio (ε E0 qeq : ℝ) (hε : 0 < ε) (hqeq : 0 < qeq)
    (haccess : |0 - (-2 * ε) * qeq| ≤ E0 - (2 * ε ^ 2) * qeq) :
    1 + 1 / ε ≤ E0 / ((2 * ε ^ 2) * qeq) := by
  have hb := necessary_capacity_ratio 1 (2 * ε ^ 2) (-2 * ε) E0 qeq
    (by positivity) hqeq (by simpa using haccess)
  have ha : |(-2 : ℝ) * ε| = 2 * ε := by rw [abs_mul, abs_of_pos hε]; norm_num
  rw [ha, one_mul] at hb
  convert hb using 1
  field_simp

/-- Ratio r of initial excitation to the full cold cost caps the attainable fraction. -/
theorem slow_recoil_fraction (ε r q qeq : ℝ) (hε : 0 < ε) (hq : 0 ≤ q)
    (hqeq : 0 < qeq)
    (haccess : |0 - (-2 * ε) * q| ≤ r * (2 * ε ^ 2) * qeq - (2 * ε ^ 2) * q) :
    q / qeq ≤ r * ε / (1 + ε) := by
  have hb := recoil_budget 1 (2 * ε ^ 2) (-2 * ε)
    (r * (2 * ε ^ 2) * qeq) q hq (by simpa using haccess)
  have ha : |(-2 : ℝ) * ε| = 2 * ε := by rw [abs_mul, abs_of_pos hε]; norm_num
  rw [ha, one_mul] at hb
  have hnorm : (1 + ε) * q ≤ r * ε * qeq := by
    have he : (2 * ε ^ 2 + 2 * ε) * q - r * (2 * ε ^ 2) * qeq =
        2 * ε * ((1 + ε) * q - r * ε * qeq) := by ring
    have hz : 2 * ε * ((1 + ε) * q - r * ε * qeq) ≤ 0 := by rw [← he]; linarith
    have hz2 : (1 + ε) * q - r * ε * qeq ≤ 0 :=
      le_of_mul_le_mul_left (by simpa using hz) (by positivity : 0 < 2 * ε)
    linarith
  apply (div_le_div_iff₀ hqeq (by positivity : 0 < 1 + ε)).mpr
  nlinarith [hnorm]

end FrameworkReceiverCapacity
#print axioms FrameworkReceiverCapacity.omega_squared
#print axioms FrameworkReceiverCapacity.energy_momentum_squares
#print axioms FrameworkReceiverCapacity.energy_nonnegative
#print axioms FrameworkReceiverCapacity.receiver_floor
#print axioms FrameworkReceiverCapacity.accessible_transfer
#print axioms FrameworkReceiverCapacity.recoil_budget
#print axioms FrameworkReceiverCapacity.necessary_capacity_ratio
#print axioms FrameworkReceiverCapacity.slow_recoil_ratio
#print axioms FrameworkReceiverCapacity.slow_recoil_fraction

/- EXPECTED FAILURE: a traveling/circular mode saturates the floor. -/
example : |FrameworkReceiverCapacity.momentum 1 1 0 0 1| <
    FrameworkReceiverCapacity.energy 1 1 1 0 0 1 := by
  norm_num [FrameworkReceiverCapacity.momentum, FrameworkReceiverCapacity.energy,
    FrameworkReceiverCapacity.omega]
