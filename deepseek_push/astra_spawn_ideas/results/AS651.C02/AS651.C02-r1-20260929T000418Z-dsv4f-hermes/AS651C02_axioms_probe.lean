import Mathlib.Data.Real.Basic
import Mathlib.Tactic

/-!
AS651.C02 -- axioms probe: unfiltered `#print axioms` for every certified theorem.
-/

noncomputable section
open scoped Real

namespace AS651C02

/-- Vacuum energy density of the four-form sector. -/
def eps (Z : ℝ) (b : ℝ) (beta : ℝ) (q : ℝ) : ℝ :=
  (Z / 2 + b * beta ^ 2) * q ^ 2

/-- κ² = a0²/(G ε_vac) with a0² = G β² q². -/
def kappaSq (Z : ℝ) (b : ℝ) (beta : ℝ) (q : ℝ) : ℝ :=
  (beta ^ 2 * q ^ 2) / eps Z b beta q

theorem boundary_law_iff (q pi Z b beta : ℝ) (hden : Z + 2 * b * beta ^ 2 ≠ 0) :
    (Z + 2 * b * beta ^ 2) * q = pi ↔ q = pi / (Z + 2 * b * beta ^ 2) := by
  constructor
  · intro h
    rw [← h]
    field_simp [hden]
  · intro h
    rw [h]
    field_simp [hden]

theorem selection_injective (pi1 pi2 Z b beta : ℝ) (hden : Z + 2 * b * beta ^ 2 ≠ 0)
    (h : pi1 / (Z + 2 * b * beta ^ 2) = pi2 / (Z + 2 * b * beta ^ 2)) : pi1 = pi2 := by
  exact mul_right_cancel₀ hden ((div_eq_div_iff hden hden).mp h)

theorem kappaSq_of_q (q Z b beta : ℝ) (hq : q ≠ 0) (hden : Z / 2 + b * beta ^ 2 ≠ 0) :
    kappaSq Z b beta q = beta ^ 2 / (Z / 2 + b * beta ^ 2) := by
  unfold kappaSq eps
  have hq2 : q ^ 2 ≠ 0 := pow_ne_zero 2 hq
  have hden2 : (Z / 2 + b * beta ^ 2) * q ^ 2 ≠ 0 := mul_ne_zero hden hq2
  field_simp [hden2]

theorem kappa_proj_ensemble_blind (q1 q2 Z b beta : ℝ) (hq1 : q1 ≠ 0) (hq2 : q2 ≠ 0)
    (hden : Z / 2 + b * beta ^ 2 ≠ 0) : kappaSq Z b beta q1 = kappaSq Z b beta q2 := by
  rw [kappaSq_of_q q1 Z b beta hq1 hden, kappaSq_of_q q2 Z b beta hq2 hden]

theorem eps_strict_mono (Z b beta : ℝ) (hZ : 0 < Z) (hb : 0 < b) (hbeta : beta ≠ 0)
    {q1 q2 : ℝ} (hq1 : 0 < q1) (h12 : q1 < q2) : eps Z b beta q1 < eps Z b beta q2 := by
  have hbz : 0 < beta ^ 2 := sq_pos_of_ne_zero hbeta
  have hA : 0 < Z / 2 + b * beta ^ 2 := by nlinarith
  have hq2sq : q1 ^ 2 < q2 ^ 2 := by
    have hsub : 0 < q2 - q1 := sub_pos.mpr h12
    have hsum : 0 < q1 + q2 := by linarith
    have hmul : 0 < (q2 - q1) * (q1 + q2) := mul_pos hsub hsum
    nlinarith
  unfold eps
  exact mul_lt_mul_of_pos_left hq2sq hA

theorem gibbs_weight_strict_dec (V Z b beta : ℝ) (hV : 0 < V) (hZ : 0 < Z) (hb : 0 < b)
    (hbeta : beta ≠ 0) {q1 q2 : ℝ} (hq1 : 0 < q1) (h12 : q1 < q2) :
    Real.exp (-V * eps Z b beta q1) > Real.exp (-V * eps Z b beta q2) := by
  have he : eps Z b beta q1 < eps Z b beta q2 := eps_strict_mono Z b beta hZ hb hbeta hq1 h12
  have hVeps : V * eps Z b beta q1 < V * eps Z b beta q2 := mul_lt_mul_of_pos_left he hV
  have hneg : -V * eps Z b beta q2 < -V * eps Z b beta q1 := by nlinarith
  exact Real.exp_lt_exp.mpr hneg

theorem half_flux_lower_energy (Z b beta : ℝ) (hZ : 0 < Z) (hb : 0 < b) (hbeta : beta ≠ 0)
    {q : ℝ} (hq : 0 < q) : eps Z b beta (q / 2) < eps Z b beta q := by
  apply eps_strict_mono Z b beta hZ hb hbeta
  · positivity
  · linarith

theorem unadorned_weight_fires (V Z b beta : ℝ) (hV : 0 < V) (hZ : 0 < Z) (hb : 0 < b)
    (hbeta : beta ≠ 0) {q : ℝ} (hq : 0 < q) : Real.exp (-V * eps Z b beta q) < 1 := by
  have hbz : 0 < beta ^ 2 := sq_pos_of_ne_zero hbeta
  have hA : 0 < Z / 2 + b * beta ^ 2 := by nlinarith
  have hq2 : 0 < q ^ 2 := sq_pos_of_ne_zero (ne_of_gt hq)
  have he : 0 < eps Z b beta q := by
    unfold eps
    exact mul_pos hA hq2
  have hVeps : 0 < V * eps Z b beta q := mul_pos hV he
  have hneg : -V * eps Z b beta q < 0 := by nlinarith
  rw [← Real.exp_zero]
  exact Real.exp_lt_exp.mpr hneg

def P_l (Z : ℝ) (b : ℝ) (beta : ℝ) (lam : ℝ) (q : ℝ) : ℝ :=
  Z / 2 * q ^ 2 + b * beta ^ 2 * q ^ 2 + lam * q

def Pq_l (Z : ℝ) (b : ℝ) (beta : ℝ) (lam : ℝ) (q : ℝ) : ℝ :=
  (Z + 2 * b * beta ^ 2) * q + lam

def eps_l (Z : ℝ) (b : ℝ) (beta : ℝ) (lam : ℝ) (q : ℝ) : ℝ :=
  q * Pq_l Z b beta lam q - P_l Z b beta lam q

def qstar (Z : ℝ) (b : ℝ) (beta : ℝ) (lam : ℝ) : ℝ :=
  -lam / (Z + 2 * b * beta ^ 2)

theorem lambda_eps_equals_eps (Z b beta lam q : ℝ) : eps_l Z b beta lam q = eps Z b beta q := by
  unfold eps_l eps P_l Pq_l
  ring

theorem lambda_stationary_point (Z b beta lam : ℝ) (hden : Z + 2 * b * beta ^ 2 ≠ 0) :
    Pq_l Z b beta lam (qstar Z b beta lam) = 0 := by
  unfold Pq_l qstar
  have hc : (Z + 2 * b * beta ^ 2) * (-lam / (Z + 2 * b * beta ^ 2)) = -lam := by
    rw [mul_comm]
    exact div_mul_cancel₀ (-lam) hden
  rw [hc]
  ring

theorem lambda_kappa_blind (Z b beta lam : ℝ) (hden : Z + 2 * b * beta ^ 2 ≠ 0)
    (hden2 : Z / 2 + b * beta ^ 2 ≠ 0) (hlam : lam ≠ 0) :
    kappaSq Z b beta (qstar Z b beta lam) = beta ^ 2 / (Z / 2 + b * beta ^ 2) := by
  have hq : qstar Z b beta lam ≠ 0 := by
    unfold qstar
    exact div_ne_zero (neg_ne_zero.mpr hlam) hden
  exact kappaSq_of_q (qstar Z b beta lam) Z b beta hq hden2

theorem tuned_datum (q pi Z b beta : ℝ) (hZ : Z = (8 - 2 * b) * beta ^ 2)
    (h : pi = (Z + 2 * b * beta ^ 2) * q) : pi = 8 * beta ^ 2 * q := by
  rw [h, hZ]
  ring

#check boundary_law_iff
#print axioms boundary_law_iff
#print axioms selection_injective
#print axioms kappaSq_of_q
#print axioms kappa_proj_ensemble_blind
#print axioms eps_strict_mono
#print axioms gibbs_weight_strict_dec
#print axioms half_flux_lower_energy
#print axioms unadorned_weight_fires
#print axioms lambda_eps_equals_eps
#print axioms lambda_stationary_point
#print axioms lambda_kappa_blind
#print axioms tuned_datum

end AS651C02

end