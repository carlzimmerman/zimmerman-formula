import Mathlib

/-! Exact C2 polynomial receiver audit from CFG635. Declared P(X), local
homogeneous rho=2X P_X-P and quadratic health coefficients; no metric/cosmology
or higher-gradient stability theorem is imported. State/current budget restrictions
are conditional, not dynamics or universal reservoir no-go statements. -/
noncomputable section
namespace FrameworkGhostReceiver

def P (a X0 ρ0 X : ℝ) : ℝ := -ρ0 + a / 2 * (X - X0) ^ 2
def gradient (a X0 X : ℝ) : ℝ := a * (X - X0)
def rho (a X0 ρ0 d : ℝ) : ℝ := 2 * (X0 + d) * gradient a X0 (X0 + d) - P a X0 ρ0 (X0 + d)
def pressure (a X0 ρ0 d : ℝ) : ℝ := P a X0 ρ0 (X0 + d)
def kinetic (a X0 d : ℝ) : ℝ := gradient a X0 (X0 + d) + 2 * (X0 + d) * a

/-- Actual first and second polynomial derivative certificates. -/
theorem potential_derivatives (a X0 ρ0 X : ℝ) :
    HasDerivAt (P a X0 ρ0) (gradient a X0 X) X ∧
      HasDerivAt (gradient a X0) a X := by
  have hx := (hasDerivAt_id X).sub_const X0
  have hp := ((hx.pow 2).const_mul (a / 2)).const_add (-ρ0)
  have hpp := hx.const_mul a
  constructor
  · apply hp.congr_deriv
    dsimp [gradient]
    ring
  · apply hpp.congr_deriv
    ring

/-- Exact state dictionary, retaining all quadratic terms. -/
theorem state_dictionary (a X0 ρ0 d : ℝ) :
    rho a X0 ρ0 d = ρ0 + a * (2 * X0 * d + 3 * d ^ 2 / 2) ∧
    pressure a X0 ρ0 d = -ρ0 + a * d ^ 2 / 2 ∧
    gradient a X0 (X0 + d) = a * d ∧ kinetic a X0 d = a * (2 * X0 + 3 * d) := by
  unfold rho pressure kinetic gradient P
  constructor
  · ring
  constructor
  · ring
  constructor <;> ring

/-- Nonnegative local P_X at positive a is exactly the d>=0 branch. -/
theorem healthy_branch (a X0 d : ℝ) (ha : 0 < a) :
    0 ≤ gradient a X0 (X0 + d) ↔ 0 ≤ d := by
  unfold gradient
  simp only [add_sub_cancel_left]
  constructor
  · intro h
    exact le_of_mul_le_mul_left (by simpa using h) ha
  · intro h
    exact mul_nonneg ha.le h

theorem healthy_density_floor (a X0 ρ0 d : ℝ) (ha : 0 < a) (hX0 : 0 < X0)
    (hhealth : 0 ≤ gradient a X0 (X0 + d)) : ρ0 ≤ rho a X0 ρ0 d := by
  have hd := (healthy_branch a X0 d ha).mp hhealth
  rw [(state_dictionary a X0 ρ0 d).1]
  have hpositive : 0 ≤ a * (2 * X0 * d + 3 * d ^ 2 / 2) := by positivity
  linarith

/-- An exact-ground initial density cannot export positive energy into a final healthy local state. -/
theorem no_ground_export (a X0 ρ0 d exported : ℝ) (ha : 0 < a) (hX0 : 0 < X0)
    (hhealth : 0 ≤ gradient a X0 (X0 + d))
    (hledger : exported = rho a X0 ρ0 0 - rho a X0 ρ0 d) : exported ≤ 0 := by
  have hf := healthy_density_floor a X0 ρ0 d ha hX0 hhealth
  have hground : rho a X0 ρ0 0 = ρ0 := by simp [rho, gradient, P]
  rw [hground] at hledger
  linarith

/-- A pre-existing positive buffer is finite, positive, and its finite deposit is not exact dust. -/
theorem positive_buffer (a X0 ρ0 d : ℝ) (ha : 0 < a) (hX0 : 0 < X0) (hd : 0 < d) :
    0 < rho a X0 ρ0 d - ρ0 ∧ 0 < pressure a X0 ρ0 d + ρ0 ∧ 0 < kinetic a X0 d := by
  have hs := state_dictionary a X0 ρ0 d
  rw [hs.1, hs.2.1, hs.2.2.2]
  constructor
  · have hp : 0 < a * (2 * X0 * d + 3 * d ^ 2 / 2) := by positivity
    linarith
  constructor
  · have hp : 0 < a * d ^ 2 / 2 := by positivity
    linarith
  · positivity

/-- Any final healthy state bounds local exported energy by the initial excess above rho0. -/
theorem buffered_export_budget (a X0 ρ0 di df exported : ℝ) (ha : 0 < a) (hX0 : 0 < X0)
    (hfinal : 0 ≤ gradient a X0 (X0 + df))
    (hledger : exported = rho a X0 ρ0 di - rho a X0 ρ0 df) :
    exported ≤ rho a X0 ρ0 di - ρ0 := by
  have hf := healthy_density_floor a X0 ρ0 df ha hX0 hfinal
  linarith

/-- Reaching the health boundary consumes exactly the buffer, conditional on the energy ledger. -/
theorem health_boundary_budget (a X0 ρ0 di exported : ℝ)
    (hledger : exported = rho a X0 ρ0 di - rho a X0 ρ0 0) :
    exported = a * (2 * X0 * di + 3 * di ^ 2 / 2) := by
  rw [(state_dictionary a X0 ρ0 di).1, (state_dictionary a X0 ρ0 0).1] at hledger
  simpa using hledger

/-- Exact finite deposit equation of state, rather than the first-order dust shorthand. -/
theorem deposit_eos (a X0 ρ0 d : ℝ) (ha : 0 < a) (hX0 : 0 < X0) (hd : 0 < d) :
    (pressure a X0 ρ0 d + ρ0) / (rho a X0 ρ0 d - ρ0) = d / (4 * X0 + 3 * d) ∧
      0 < d / (4 * X0 + 3 * d) ∧ d / (4 * X0 + 3 * d) < 1 / 3 := by
  have hden : 0 < 4 * X0 + 3 * d := by positivity
  have hbuf := (positive_buffer a X0 ρ0 d ha hX0 hd).1
  have hs := state_dictionary a X0 ρ0 d
  constructor
  · rw [hs.1, hs.2.1]
    field_simp
    ring
  constructor
  · positivity
  · apply (div_lt_iff₀ hden).mpr
    nlinarith

/-- A declared small excess-energy buffer yields a quantitative local DE-like bound. -/
theorem de_deviation_bound (a X0 ρ0 d η : ℝ) (ha : 0 < a) (hX0 : 0 < X0)
    (hρ0 : 0 < ρ0) (hd : 0 ≤ d) (hη : 0 ≤ η)
    (hbuffer : rho a X0 ρ0 d - ρ0 ≤ η * ρ0) :
    0 ≤ pressure a X0 ρ0 d / rho a X0 ρ0 d + 1 ∧
      pressure a X0 ρ0 d / rho a X0 ρ0 d + 1 ≤ 4 * η / 3 := by
  have hf := healthy_density_floor a X0 ρ0 d ha hX0 ((healthy_branch a X0 d ha).mpr hd)
  have hr : 0 < rho a X0 ρ0 d := lt_of_lt_of_le hρ0 hf
  have hs := state_dictionary a X0 ρ0 d
  have hn : 0 ≤ pressure a X0 ρ0 d + rho a X0 ρ0 d := by rw [hs.1, hs.2.1]; nlinarith
  have hupper : pressure a X0 ρ0 d + rho a X0 ρ0 d ≤
      (4 / 3 : ℝ) * (rho a X0 ρ0 d - ρ0) := by
    rw [hs.1, hs.2.1]
    nlinarith [mul_nonneg ha.le (mul_nonneg hX0.le hd)]
  have he : pressure a X0 ρ0 d / rho a X0 ρ0 d + 1 =
      (pressure a X0 ρ0 d + rho a X0 ρ0 d) / rho a X0 ρ0 d := by field_simp
  rw [he]
  constructor
  · exact div_nonneg hn hr.le
  · apply (div_le_iff₀ hr).mpr
    have hscale := mul_le_mul_of_nonneg_left hf hη
    nlinarith [hupper, hbuffer, hscale]

end FrameworkGhostReceiver
#print axioms FrameworkGhostReceiver.potential_derivatives
#print axioms FrameworkGhostReceiver.state_dictionary
#print axioms FrameworkGhostReceiver.healthy_branch
#print axioms FrameworkGhostReceiver.healthy_density_floor
#print axioms FrameworkGhostReceiver.no_ground_export
#print axioms FrameworkGhostReceiver.positive_buffer
#print axioms FrameworkGhostReceiver.buffered_export_budget
#print axioms FrameworkGhostReceiver.health_boundary_budget
#print axioms FrameworkGhostReceiver.deposit_eos
#print axioms FrameworkGhostReceiver.de_deviation_bound

/- EXPECTED FAILURE: a finite positive deposit has quadratic positive excess pressure. -/
example : FrameworkGhostReceiver.pressure 1 1 1 1 + 1 = 0 := by
  norm_num [FrameworkGhostReceiver.pressure, FrameworkGhostReceiver.P]
