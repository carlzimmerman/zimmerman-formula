import Mathlib.Data.Real.Basic
import Mathlib.Tactic

/-!
AS651.C02 -- boundary ensemble for the three-form flux: origin of q_0?
Algebraic core of the derivation, certified in Lean 4 (self-contained).

Sector (identical to AS651):  S = ∫ sqrt(-g) P(q) d⁴x,  P(q) = (Z/2) q² + b β² q²
(k04 four-form promotion),  ε_vac = q P_q − P = (Z/2 + b β²) q²,
κ² = a0²/(G ε_vac) = β²/(Z/2 + b β²),  a0² = G β² q².

Boundary ensemble (this work order):
  (a) the boundary term δS = ∫ dL/dF ∧ δA reduces on the box prototype to the
      BOUNDARY LAW  Π₀ = (Z + 2bβ²) q₀  (Π₀ = boundary conjugate of the flux);
  (b) the ensemble's selected flux enters κ² NOT AT ALL: the κ-projection is
      constant across every nonzero flux (kappa_proj_ensemble_blind) -- any
      ensemble selection of q₀ is κ-blind;
  (c) the unadorned Gibbs weight exp(−V ε_vac(q)) is strictly decreasing in q
      (eps_strict_mono, gibbs_weight_strict_dec) and its mode sits at q → 0⁺,
      NOT at q_* (unadorned_weight_fires; half_flux_lower_energy: no interior
      minimum) -- reproducing q_* requires tuning the ensemble's own datum Π₀
      (tuned_datum: Π₀* = 8 β² q_*), i.e. B-ii relocation;
  (d) the alternative changed model P + λ q has the unique stationary point
      q* = −λ/(Z + 2bβ²) (lambda_stationary_point) with ε_vac λ-independent
      (lambda_eps_equals_eps) and κ² λ-independent (lambda_kappa_blind) --
      the linear-term repair relocates the datum q₀ → λ without selecting κ.

Theorems:
  1. boundary_law_iff          : Π₀ = (Z+2bβ²) q₀  ↔  q₀ = Π₀/(Z+2bβ²)   [S1/S2]
  2. selection_injective       : the boundary map Π₀ ↦ q₀(Π₀) is injective --
                                 the ensemble's q₀ spans a continuum in Π₀
  3. kappa_proj_ensemble_blind : κ²(q₁) = κ²(q₂) for every q₁, q₂ ≠ 0 --
                                 ANY ensemble selection of q₀ is κ-blind
  4. eps_strict_mono           : ε_vac strictly increasing in q > 0
  5. gibbs_weight_strict_dec   : exp(−V ε) strictly decreasing in q > 0
  6. half_flux_lower_energy    : ε(q/2) < ε(q): no interior minimum of ε
  7. unadorned_weight_fires    : exp(−V ε(q)) < 1 = mode weight: the unadorned
                                 ensemble's mode is q → 0⁺, not q_* (fires)
  8. lambda_stationary_point   : P_q(q*) = 0 at q* = −λ/(Z+2bβ²) (unique)
  9. lambda_eps_equals_eps     : ε_vac(λ model) = (Z/2+bβ²) q²: λ cancels
 10. lambda_kappa_blind        : κ²(λ model at q*) = β²/(Z/2+bβ²): λ cancels
 11. tuned_datum               : at Z = (8−2b)β² the datum selecting q_* is
                                 Π₀* = 8 β² q_* (relocation witness)
-/

noncomputable section
open scoped Real

namespace AS651C02

/-- Vacuum energy density of the four-form sector, ε_vac = q P_q − P = (Z/2 + b β²) q². -/
def eps (Z : ℝ) (b : ℝ) (beta : ℝ) (q : ℝ) : ℝ :=
  (Z / 2 + b * beta ^ 2) * q ^ 2

/-- κ² = a0²/(G ε_vac) with a0² = G β² q²: the κ-projection of the sector. -/
def kappaSq (Z : ℝ) (b : ℝ) (beta : ℝ) (q : ℝ) : ℝ :=
  (beta ^ 2 * q ^ 2) / eps Z b beta q

/-- BOUNDARY LAW (S1/S2): the boundary conjugate Π₀ determines the flux linearly --
Π₀ = (Z + 2bβ²) q₀  iff  q₀ = Π₀/(Z + 2bβ²). -/
theorem boundary_law_iff (q pi Z b beta : ℝ) (hden : Z + 2 * b * beta ^ 2 ≠ 0) :
    (Z + 2 * b * beta ^ 2) * q = pi ↔ q = pi / (Z + 2 * b * beta ^ 2) := by
  constructor
  · intro h
    rw [← h]
    field_simp [hden]
  · intro h
    rw [h]
    field_simp [hden]

/-- The boundary map Π₀ ↦ q₀(Π₀) = Π₀/(Z+2bβ²) is injective: the ensemble's
selected flux q₀ spans a continuum in the ensemble datum Π₀ (no quantization
emerges from the pinned action alone). -/
theorem selection_injective (pi1 pi2 Z b beta : ℝ) (hden : Z + 2 * b * beta ^ 2 ≠ 0)
    (h : pi1 / (Z + 2 * b * beta ^ 2) = pi2 / (Z + 2 * b * beta ^ 2)) : pi1 = pi2 := by
  exact mul_right_cancel₀ hden ((div_eq_div_iff hden hden).mp h)

/-- κ² evaluated at any single flux q ≠ 0. -/
theorem kappaSq_of_q (q Z b beta : ℝ) (hq : q ≠ 0) (hden : Z / 2 + b * beta ^ 2 ≠ 0) :
    kappaSq Z b beta q = beta ^ 2 / (Z / 2 + b * beta ^ 2) := by
  unfold kappaSq eps
  have hq2 : q ^ 2 ≠ 0 := pow_ne_zero 2 hq
  have hden2 : (Z / 2 + b * beta ^ 2) * q ^ 2 ≠ 0 := mul_ne_zero hden hq2
  field_simp [hden2]

/-- ENSEMBLE-BLINDNESS: the κ-projection is constant on ALL nonzero fluxes --
the boundary ensemble can select q₀ but the selected value drops out of κ²
identically; the ensemble never moves κ along its continuum in Z/β². -/
theorem kappa_proj_ensemble_blind (q1 q2 Z b beta : ℝ) (hq1 : q1 ≠ 0) (hq2 : q2 ≠ 0)
    (hden : Z / 2 + b * beta ^ 2 ≠ 0) : kappaSq Z b beta q1 = kappaSq Z b beta q2 := by
  rw [kappaSq_of_q q1 Z b beta hq1 hden, kappaSq_of_q q2 Z b beta hq2 hden]

/-- ε_vac is strictly increasing in q > 0 (Z, b > 0, β ≠ 0). -/
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

/-- The unadorned Gibbs weight exp(−V ε_vac(q)) is strictly decreasing in q > 0
(V > 0): its mode is at the smallest q, not at q_*. -/
theorem gibbs_weight_strict_dec (V Z b beta : ℝ) (hV : 0 < V) (hZ : 0 < Z) (hb : 0 < b)
    (hbeta : beta ≠ 0) {q1 q2 : ℝ} (hq1 : 0 < q1) (h12 : q1 < q2) :
    Real.exp (-V * eps Z b beta q1) > Real.exp (-V * eps Z b beta q2) := by
  have he : eps Z b beta q1 < eps Z b beta q2 := eps_strict_mono Z b beta hZ hb hbeta hq1 h12
  have hVeps : V * eps Z b beta q1 < V * eps Z b beta q2 := mul_lt_mul_of_pos_left he hV
  have hneg : -V * eps Z b beta q2 < -V * eps Z b beta q1 := by nlinarith
  exact Real.exp_lt_exp.mpr hneg

/-- ε_vac has NO interior minimum on q > 0: the half-flux state has strictly
lower vacuum energy (q → 0⁺ is the infimum of the unadorned ensemble). -/
theorem half_flux_lower_energy (Z b beta : ℝ) (hZ : 0 < Z) (hb : 0 < b) (hbeta : beta ≠ 0)
    {q : ℝ} (hq : 0 < q) : eps Z b beta (q / 2) < eps Z b beta q := by
  apply eps_strict_mono Z b beta hZ hb hbeta
  · positivity
  · linarith

/-- NEGATIVE-CONTROL theorem (capable of failing): the unadorned weight at ANY
positive flux sits strictly below the q → 0⁺ mode weight 1 -- the pure-action
Gibbs ensemble does NOT select q_* (it fires toward q = 0). -/
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

/-- Action density of the alternative changed model, P(q) = (Z/2) q² + b β² q² + λ q. -/
def P_l (Z : ℝ) (b : ℝ) (beta : ℝ) (lam : ℝ) (q : ℝ) : ℝ :=
  Z / 2 * q ^ 2 + b * beta ^ 2 * q ^ 2 + lam * q

/-- Formal derivative of the λ-model, P_q = (Z + 2bβ²) q + λ. -/
def Pq_l (Z : ℝ) (b : ℝ) (beta : ℝ) (lam : ℝ) (q : ℝ) : ℝ :=
  (Z + 2 * b * beta ^ 2) * q + lam

/-- Vacuum energy of the λ-model, ε_vac = q P_q − P. -/
def eps_l (Z : ℝ) (b : ℝ) (beta : ℝ) (lam : ℝ) (q : ℝ) : ℝ :=
  q * Pq_l Z b beta lam q - P_l Z b beta lam q

/-- Stationary point of the altered premise P_q = 0. -/
def qstar (Z : ℝ) (b : ℝ) (beta : ℝ) (lam : ℝ) : ℝ :=
  -lam / (Z + 2 * b * beta ^ 2)

/-- In the λ-model the vacuum energy is λ-FREE: ε_vac = (Z/2 + bβ²) q² (the
Legendre transform kills the linear term). -/
theorem lambda_eps_equals_eps (Z b beta lam q : ℝ) : eps_l Z b beta lam q = eps Z b beta q := by
  unfold eps_l eps P_l Pq_l
  ring

/-- The λ-model has the (unique, nonzero for λ ≠ 0) stationary point
q* = −λ/(Z + 2bβ²): residual P_q(q*) = 0 exactly. -/
theorem lambda_stationary_point (Z b beta lam : ℝ) (hden : Z + 2 * b * beta ^ 2 ≠ 0) :
    Pq_l Z b beta lam (qstar Z b beta lam) = 0 := by
  unfold Pq_l qstar
  have hc : (Z + 2 * b * beta ^ 2) * (-lam / (Z + 2 * b * beta ^ 2)) = -lam := by
    rw [mul_comm]
    exact div_mul_cancel₀ (-lam) hden
  rw [hc]
  ring

/-- κ² of the λ-model at its stationary flux is λ-INDEPENDENT: the linear-term
repair relocates the datum q₀ → λ and leaves the κ-continuum in Z/β² intact
(B-ii deduction, relocation audit). -/
theorem lambda_kappa_blind (Z b beta lam : ℝ) (hden : Z + 2 * b * beta ^ 2 ≠ 0)
    (hden2 : Z / 2 + b * beta ^ 2 ≠ 0) (hlam : lam ≠ 0) :
    kappaSq Z b beta (qstar Z b beta lam) = beta ^ 2 / (Z / 2 + b * beta ^ 2) := by
  have hq : qstar Z b beta lam ≠ 0 := by
    unfold qstar
    exact div_ne_zero (neg_ne_zero.mpr hlam) hden
  exact kappaSq_of_q (qstar Z b beta lam) Z b beta hq hden2

/-- TUNED DATUM (relocation witness): at the ratio Z = (8−2b) β² (the κ = 1/2
condition), the boundary datum that selects q_* is exactly Π₀* = 8 β² q_* --
one adopted real replacing q₀; B-ii deficit conserved. -/
theorem tuned_datum (q pi Z b beta : ℝ) (hZ : Z = (8 - 2 * b) * beta ^ 2)
    (h : pi = (Z + 2 * b * beta ^ 2) * q) : pi = 8 * beta ^ 2 * q := by
  rw [h, hZ]
  ring

end AS651C02

end
