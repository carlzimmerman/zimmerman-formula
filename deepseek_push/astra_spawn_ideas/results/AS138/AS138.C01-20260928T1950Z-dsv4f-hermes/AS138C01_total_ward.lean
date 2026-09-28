import Mathlib.Data.Real.Basic
import Mathlib.Tactic

/-!
AS138.C01, kappa-closure attempt: total-Ward assembly at pin b8c04d4e...7546e.
Algebraic core of the assembly theorems, certified in Lean 4 (self-contained).

Landing (premises; the identities used by the assembly):
  P1 AS137  matter:        Q_b  = E_b (xi.dpsi),  E_b = 0 on shell.
  P2 AS138  heat:          Q_heat = N [ sum E-terms + (R_W+L_b)(xi.dW)_b + (lam0-L_0)(xi.dW)_0 ],
                            endpoint multipliers close by the pinned terminal BC (AS133:
                            L_b = -R_W, lam0 = L_0).
  P3 AS147  diagonal U(1): div J_phi = +E, div J_chi = -E, total = 0 (exchange cancels).
  P4 AS651  four-form:     T_vac = -eps_vac g, eps_vac = (Z/2 + b beta^2) q^2,
                            div T_vac = -(Z + 2 b beta^2) q (d,q),  zero on shell by flux
                            constancy dq = 0 (three-form EOM).

Theorems:
  1. heat_endpoint_bracket_zero   : on shell the heat endpoint bracket closes (AS133 BC).
  2. u1_exchange_zero             : the U(1) total divergence is zero (AS147).
  3. vacuum_div_zero_on_shell     : the vacuum Ward divergence vanishes for dq = 0 (AS651).
  4. total_ward_closes            : Q_b + Q_heat + Q_U1 + Q_vac = 0 on shell with NO
                                    hypothesis on Z, b, beta (conservation-to-continuum).
  5. bracket_nonzero_witness      : concrete witness N*M = -57/50 != 0 (negative control).
  6. kappa2_eight_lt_quarter      : at r = 8, kappa^2 = 1/(4+b) < 1/4 for b > 0.
  7. kappa_eight_neq_half         : kappa(8) != 1/2, a continuum member with kappa != 1/2
                                    satisfying on-shell conservation identically.
  8. kappa2_at_tuned_ratio        : at r* = 8 - 2b, kappa^2 = 1/4 exactly.
  9. tuned_point_in_domain        : for the pinned cell 0 < b < 4, 0 < r* < 8.
-/

noncomputable section
open scoped Real

namespace AS138C01

/-- P1: matter Ward charge density (contracted with the diffeomorphism xi). -/
def Qb (Eb dpsi : ℝ) : ℝ := Eb * dpsi

/-- P2: heat Ward charge density (AS138 CHK-3 display; E_terms = sum of the interior Euler
terms, endpoint multipliers displayed explicitly). -/
def Qheat (N E_terms RW Lb : ℝ) (Wbp : ℝ) (lam0 L0 : ℝ) (W0p Elam lam0p EU Up : ℝ) : ℝ :=
  N * (E_terms + (RW + Lb) * Wbp + (lam0 - L0) * W0p + Elam * lam0p + EU * Up)

/-- P3: diagonal U(1) total divergence:  div J_phi + div J_chi = E + (-E). -/
def QU1 (E : ℝ) : ℝ := E + (-E)

/-- P4: vacuum four-form Ward divergence density (metric-proportional stress):
div T_vac = -(Z + 2 b beta^2) * q * (d,q); on shell dq = 0. -/
def Qvac (Z b beta q dq : ℝ) : ℝ := -(Z + 2 * b * beta ^ 2) * q * dq

/-- AS133 terminal BC: the heat endpoint bracket closes on shell. -/
theorem heat_endpoint_bracket_zero (RW Lb L0 lam0 Wbp W0p : ℝ)
    (hLb : Lb = -RW) (hL0 : L0 = lam0) :
    (RW + Lb) * Wbp + (lam0 - L0) * W0p = 0 := by
  rw [hLb, hL0]
  ring

/-- AS147: the phi and chi currents exchange opposite charges; the total divergence is zero
identically (no field hypothesis needed at the exchange level). -/
theorem u1_exchange_zero (E : ℝ) : QU1 E = 0 := by
  unfold QU1
  ring

/-- AS651 + flux EOM: on shell (dq = 0) the vacuum Ward divergence vanishes, for every
coupling cell (Z, b, beta, q). -/
theorem vacuum_div_zero_on_shell (Z b beta q dq : ℝ) (hdq : dq = 0) :
    Qvac Z b beta q dq = 0 := by
  unfold Qvac
  rw [hdq]
  ring

/-- ASSEMBLY / CONTINUUM THEOREM. On shell the total Ward charge of the four sectors
(matter + heat + U(1) + vacuum) vanishes for EVERY choice of the coupling cell
(Z, b, beta, q): the theorem has no hypothesis on Z, b, beta or q. Conservation of the
total stress therefore imposes NO condition on the ratio Z/beta^2 -- the solution set
of "nabla . Q_total = 0" is the full continuum of ratios. -/
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

/-- AS138 CHK-2 (negative control, structure): the leftover that the multiplier display
must cancel is N * (L_b (xi.dW)_b - L_0 (xi.dW)_0); the display itself vanishes on shell
(heat_endpoint_bracket_zero). Omitting the display from the on-shell heat Ward leaves a
residual N * M that does NOT vanish (witness below). Concrete witness: at the on-shell
values (R_W, (xi.dW)_b, lam0, (xi.dW)_0) = (7/20, 21/50, 3/20, -11/50), N = 10 the
leftover N*(L_b (xi.dW)_b - L_0 (xi.dW)_0) = -57/50 != 0: without the endpoint
multipliers the on-shell heat Ward FAILS with an explicit residual. -/
theorem bracket_nonzero_witness :
    (10 : ℝ) * (-((7 : ℝ) / 20) * ((21 : ℝ) / 50) - ((3 : ℝ) / 20) * (-((11 : ℝ) / 50))) ≠ 0 := by
  norm_num

/-- At r = 8 the kappa-projection is kappa^2 = 1/(4+b) < 1/4 for b > 0. -/
theorem kappa2_eight_lt_quarter (b : ℝ) (hb : 0 < b) : 1 / (4 + b) < 1 / 4 := by
  have h4 : (0 : ℝ) < 4 := by norm_num
  have hlt : 4 < 4 + b := by nlinarith
  exact one_div_lt_one_div_of_lt h4 hlt

/-- Continuum member: kappa(8) ≠ 1/2 for b > 0, while on-shell conservation holds
identically at r = 8 (total_ward_closes has no r-hypothesis). -/
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

/-- Tuned point: at r* = 8 - 2b the kappa-projection is exactly 1/4. -/
theorem kappa2_at_tuned_ratio (b : ℝ) : 1 / ((8 - 2 * b) / 2 + b) = 1 / 4 := by
  have h : (8 - 2 * b) / 2 + b = 4 := by ring
  rw [h]

/-- The tuned point is a proper member of the continuum: 0 < r* < 8 for the pinned cell
0 < b < 4 (k04 defines b = (2-K_B) I/(16 pi), 0 <= K_B <= 1/4, I = jsat = 0.4525 < 2 pi). -/
theorem tuned_point_in_domain (b : ℝ) (hb : 0 < b) (hb4 : b < 4) : 0 < 8 - 2 * b ∧ 8 - 2 * b < 8 := by
  constructor
  · nlinarith
  · nlinarith

end AS138C01

end