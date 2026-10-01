import Mathlib.Data.Real.Basic
import Mathlib.Tactic

/-! AS500.C01 axioms probe: self-contained duplicate of the decoupling certificates;
prints the unfiltered axiom set of every certified theorem. Compile host only. -/

noncomputable section
open scoped Real

namespace AS500C01

/-- P1: matter Ward charge density (contracted with the diffeomorphism xi). -/
def Qb (Eb dpsi : ℝ) : ℝ := Eb * dpsi

/-- P2: heat Ward charge density (AS138 CHK-3 display). -/
def Qheat (N E_terms RW Lb : ℝ) (Wbp : ℝ) (lam0 L0 : ℝ) (W0p Elam lam0p EU Up : ℝ) : ℝ :=
  N * (E_terms + (RW + Lb) * Wbp + (lam0 - L0) * W0p + Elam * lam0p + EU * Up)

/-- P3: diagonal U(1) total divergence (raw, off shell). -/
def QU1 (dJphi dJchi : ℝ) : ℝ := dJphi + dJchi

/-- P4: vacuum four-form Ward divergence density. -/
def Qvac (Z b beta q dq : ℝ) : ℝ := -(Z + 2 * b * beta ^ 2) * q * dq

/-- P1 on shell: matter closes by E_b = 0 (minimal coupling). -/
theorem matter_closes_on_shell (Eb dpsi : ℝ) (hEb : Eb = 0) :
    Qb Eb dpsi = 0 := by
  unfold Qb
  rw [hEb]
  ring

/-- P2b on shell: heat closes (interior EOMs + AS133 terminal BC). -/
theorem heat_closes_on_shell (N E_terms RW Lb Wbp lam0 L0 W0p Elam lam0p EU Up : ℝ)
    (hE : E_terms = 0) (hLb : Lb = -RW) (hL0 : L0 = lam0)
    (hElam : Elam = 0) (hEU : EU = 0) :
    Qheat N E_terms RW Lb Wbp lam0 L0 W0p Elam lam0p EU Up = 0 := by
  unfold Qheat
  rw [hE, hLb, hL0, hElam, hEU]
  ring

/-- P3 on shell: the phi,chi EOM pair cancels the exchange. -/
theorem u1_exchange_zero (dJphi dJchi E : ℝ) (hphi : dJphi = E) (hchi : dJchi = -E) :
    QU1 dJphi dJchi = 0 := by
  unfold QU1
  rw [hphi, hchi]
  ring

/-- P4 + flux EOM: dq = 0 closes the vacuum divergence. -/
theorem vacuum_div_zero_on_shell (Z b beta q dq : ℝ) (hdq : dq = 0) :
    Qvac Z b beta q dq = 0 := by
  unfold Qvac
  rw [hdq]
  ring

/-- DECOUPLING IDENTITY: the three cross-source sector currents close on shell with NO
hypothesis on Z, b, beta, q (the audited-band identity). -/
theorem cross_source_closes (N E_terms RW Lb Wbp lam0 L0 W0p Elam lam0p EU Up : ℝ)
    (dJphi dJchi E : ℝ) (Z b beta q dq : ℝ)
    (hE : E_terms = 0) (hLb : Lb = -RW) (hL0 : L0 = lam0)
    (hElam : Elam = 0) (hEU : EU = 0)
    (hphi : dJphi = E) (hchi : dJchi = -E) (hdq : dq = 0) :
    Qheat N E_terms RW Lb Wbp lam0 L0 W0p Elam lam0p EU Up +
    QU1 dJphi dJchi + Qvac Z b beta q dq = 0 := by
  rw [heat_closes_on_shell N E_terms RW Lb Wbp lam0 L0 W0p Elam lam0p EU Up hE hLb hL0 hElam hEU,
      u1_exchange_zero dJphi dJchi E hphi hchi,
      vacuum_div_zero_on_shell Z b beta q dq hdq]
  ring

/-- MATTER-ONLY ATOM: total-Ward balance with all fields on shell. -/
theorem matter_decoupling (Eb dpsi N E_terms RW Lb Wbp lam0 L0 W0p Elam lam0p EU Up : ℝ)
    (dJphi dJchi E : ℝ) (Z b beta q dq : ℝ)
    (hEb : Eb = 0) (hE : E_terms = 0) (hLb : Lb = -RW) (hL0 : L0 = lam0)
    (hElam : Elam = 0) (hEU : EU = 0)
    (hphi : dJphi = E) (hchi : dJchi = -E) (hdq : dq = 0) :
    Qb Eb dpsi +
    Qheat N E_terms RW Lb Wbp lam0 L0 W0p Elam lam0p EU Up +
    QU1 dJphi dJchi + Qvac Z b beta q dq = 0 := by
  rw [matter_closes_on_shell Eb dpsi hEb,
      heat_closes_on_shell N E_terms RW Lb Wbp lam0 L0 W0p Elam lam0p EU Up hE hLb hL0 hElam hEU,
      u1_exchange_zero dJphi dJchi E hphi hchi,
      vacuum_div_zero_on_shell Z b beta q dq hdq]
  ring

/-- NEG-1 witness (a): heat EOM dropped leaves residual 15 != 0. -/
theorem neg1_heat_eom_omitted :
    (10 : ℝ) * (((3 : ℝ) / 2) * 1) ≠ 0 := by
  norm_num

/-- NEG-1 witness (b): AS133 terminal BC dropped leaves residual 20 != 0
(N = 10, Wbp = W0p = 1). -/
theorem neg1_terminal_bc_omitted :
    (10 : ℝ) * ((((7 : ℝ) / 20 + ((13 : ℝ) / 20)) * 1) +
                (((3 : ℝ) / 20 - (-((17 : ℝ) / 20))) * 1)) ≠ 0 := by
  norm_num

/-- NEG-2: three-form EOM rejects q != const (retained hypothesis). -/
theorem eom_rejects_nonconst_q (Z b beta q1 : ℝ)
    (hcoef : Z + 2 * b * beta ^ 2 ≠ 0) (hq : q1 ≠ 0) :
    -(Z + 2 * b * beta ^ 2) * q1 ≠ 0 := by
  have hneg : -(Z + 2 * b * beta ^ 2) ≠ 0 := by
    intro hn
    apply hcoef
    exact neg_eq_zero.mp hn
  exact mul_ne_zero hneg hq

end AS500C01

#print axioms AS500C01.matter_closes_on_shell
#print axioms AS500C01.heat_closes_on_shell
#print axioms AS500C01.u1_exchange_zero
#print axioms AS500C01.vacuum_div_zero_on_shell
#print axioms AS500C01.cross_source_closes
#print axioms AS500C01.matter_decoupling
#print axioms AS500C01.neg1_heat_eom_omitted
#print axioms AS500C01.neg1_terminal_bc_omitted
#print axioms AS500C01.eom_rejects_nonconst_q