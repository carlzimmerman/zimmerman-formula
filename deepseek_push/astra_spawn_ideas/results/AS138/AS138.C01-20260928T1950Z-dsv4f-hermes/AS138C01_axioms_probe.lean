import Mathlib.Data.Real.Basic
import Mathlib.Tactic

/-! AS138.C01 axioms probe: prints the full axiom set of every certified theorem. -/

noncomputable section
open scoped Real

namespace AS138C01

/-- P1: matter Ward charge density (contracted with the diffeomorphism xi). -/
def Qb (Eb dpsi : ℝ) : ℝ := Eb * dpsi

/-- P2: heat Ward charge density (AS138 CHK-3 display). -/
def Qheat (N E_terms RW Lb : ℝ) (Wbp : ℝ) (lam0 L0 : ℝ) (W0p Elam lam0p EU Up : ℝ) : ℝ :=
  N * (E_terms + (RW + Lb) * Wbp + (lam0 - L0) * W0p + Elam * lam0p + EU * Up)

/-- P3: diagonal U(1) total divergence. -/
def QU1 (E : ℝ) : ℝ := E + (-E)

/-- P4: vacuum four-form Ward divergence density. -/
def Qvac (Z b beta q dq : ℝ) : ℝ := -(Z + 2 * b * beta ^ 2) * q * dq

/-- AS133 terminal BC: the heat endpoint bracket closes on shell. -/
theorem heat_endpoint_bracket_zero (RW Lb L0 lam0 Wbp W0p : ℝ)
    (hLb : Lb = -RW) (hL0 : L0 = lam0) :
    (RW + Lb) * Wbp + (lam0 - L0) * W0p = 0 := by
  rw [hLb, hL0]
  ring

/-- AS147: exchange cancels. -/
theorem u1_exchange_zero (E : ℝ) : QU1 E = 0 := by
  unfold QU1
  ring

/-- AS651 + flux EOM: dq = 0 closes the vacuum divergence. -/
theorem vacuum_div_zero_on_shell (Z b beta q dq : ℝ) (hdq : dq = 0) :
    Qvac Z b beta q dq = 0 := by
  unfold Qvac
  rw [hdq]
  ring

/-- ASSEMBLY / CONTINUUM. -/
theorem total_ward_closes (Eb dpsi N E_terms RW Lb Wbp lam0 L0 W0p Elam lam0p EU Up E : ℝ)
    (Z b beta q dq : ℝ)
    (hEb : Eb = 0) (hE : E_terms = 0) (hLb : Lb = -RW) (hL0 : L0 = lam0)
    (hElam : Elam = 0) (hEU : EU = 0) (hdq : dq = 0) :
    Qb Eb dpsi +
    Qheat N E_terms RW Lb Wbp lam0 L0 W0p Elam lam0p EU Up +
    QU1 E + Qvac Z b beta q dq = 0 := by
  unfold Qb Qheat QU1 Qvac
  rw [hEb, hE, hLb, hL0, hElam, hEU, hdq]
  ring

/-- Negative control witness. -/
theorem bracket_nonzero_witness :
    (10 : ℝ) * (-((7 : ℝ) / 20) * ((21 : ℝ) / 50) - ((3 : ℝ) / 20) * (-((11 : ℝ) / 50))) ≠ 0 := by
  norm_num

/-- kappa^2 at r = 8 is below 1/4. -/
theorem kappa2_eight_lt_quarter (b : ℝ) (hb : 0 < b) : 1 / (4 + b) < 1 / 4 := by
  have h4 : (0 : ℝ) < 4 := by norm_num
  have hlt : 4 < 4 + b := by nlinarith
  exact one_div_lt_one_div_of_lt h4 hlt

/-- kappa(8) != 1/2. -/
theorem kappa_eight_neq_half (b : ℝ) (hb : 0 < b) : Real.sqrt (1 / (4 + b)) ≠ 1 / 2 := by
  intro h
  have hge : 0 ≤ 1 / (4 + b) := by
    apply div_nonneg
    · norm_num
    · nlinarith
  have hsq : 1 / (4 + b) = 1 / 4 := by
    have hc := congrArg (fun x : ℝ => x * x) h
    rw [Real.mul_self_sqrt hge] at hc
    have hz : ((1 : ℝ) / 2) * ((1 : ℝ) / 2) = (1 : ℝ) / 4 := by norm_num
    exact hc.trans hz
  have hlt : 1 / (4 + b) < 1 / 4 := kappa2_eight_lt_quarter b hb
  exact (ne_of_lt hlt) hsq

/-- Tuned point. -/
theorem kappa2_at_tuned_ratio (b : ℝ) : 1 / ((8 - 2 * b) / 2 + b) = 1 / 4 := by
  have h : (8 - 2 * b) / 2 + b = 4 := by ring
  rw [h]

/-- Tuned point in the continuum. -/
theorem tuned_point_in_domain (b : ℝ) (hb : 0 < b) (hb4 : b < 4) : 0 < 8 - 2 * b ∧ 8 - 2 * b < 8 := by
  constructor
  · nlinarith
  · nlinarith

end AS138C01

#print axioms AS138C01.heat_endpoint_bracket_zero
#print axioms AS138C01.u1_exchange_zero
#print axioms AS138C01.vacuum_div_zero_on_shell
#print axioms AS138C01.total_ward_closes
#print axioms AS138C01.bracket_nonzero_witness
#print axioms AS138C01.kappa2_eight_lt_quarter
#print axioms AS138C01.kappa_eight_neq_half
#print axioms AS138C01.kappa2_at_tuned_ratio
#print axioms AS138C01.tuned_point_in_domain