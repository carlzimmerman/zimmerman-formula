import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Analysis.InnerProductSpace.PiL2
import Mathlib.Analysis.Calculus.Deriv.Inv
import Mathlib.Analysis.Calculus.Deriv.Add
import Mathlib.Tactic

/-!
# QX17B: algebraic kernels of the full v3s / AC2q field equations (2026-11-06)

Criteria: closure_2026_11_06/QX17B_adm_lean_solutions/FROZEN_CRITERIA.md (9684f63ba8). Kappa = 1/2 FITTED; not theory
closed. The field equations themselves are in QX17/RESULT.md (v3s) and QX17A/RESULT.md (AC2q), checked there against a
direct sympy variation. Lean certifies only the algebraic steps below; physical premises are hypotheses.

1. K0 Legendre: K|P| = a0 A/(a0 + A) is stationary for |P| A − W(K|P|), and the value is (a0²/K)[u − ln(1+u)], u = A/a0.
2. The γ = 0 P equation gives μ = 1 − K|P|/|A| = x/(1+x).
3. The normal P equation fixes λ, and then the P sector's momentum density vanishes.
4. On shell the leaf stress contracts: P·A + γ P·E = W'|P| (vector form, ℝ³), and the spherical T_rr = B²(γF − W).
5. The K(Q) lapse derivative: d/dN [N (1/N − 1)²] = 1 − 1/N², i.e. −(Q² − 1) at Q = 1/N.
6. FRW of the K(Q) dust: ρ = (μ²/2K)(Q̄² − 1) = I₀(1 + w₀/a³)/(2K a³), w₀ = I₀/(4μ²).
7. AC2q: the stiffness stress vanishes on FRW, the on-region nn identity, and continuity of nn T at the switch.
-/

open Real

namespace QX17B

/-! ## 1. Legendre form of J_x -/

/-- the physical W as a function of p = K|P| -/
noncomputable def W (a0 K p : ℝ) : ℝ := (a0 ^ 2 / K) * (-p / a0 - Real.log (1 - p / a0))

/-- the stationary point p* = a0 A/(a0 + A) solves A = K W'(p*) = a0 p*/(a0 − p*) -/
theorem legendre_stationary (a0 A : ℝ) (ha : 0 < a0) (hA : 0 ≤ A) :
    a0 * (a0 * A / (a0 + A)) / (a0 - a0 * A / (a0 + A)) = A := by
  have h1 : 0 < a0 + A := by linarith
  have h2 : a0 - a0 * A / (a0 + A) = a0 ^ 2 / (a0 + A) := by
    field_simp; ring
  rw [h2]; field_simp

/-- the Legendre value: |P| A − W at the stationary point equals (a0²/K)[u − ln(1+u)], u = A/a0 -/
theorem legendre_value (a0 K A : ℝ) (ha : 0 < a0) (hK : 0 < K) (hA : 0 ≤ A) :
    (a0 * A / (a0 + A)) / K * A - W a0 K (a0 * A / (a0 + A))
      = (a0 ^ 2 / K) * (A / a0 - Real.log (1 + A / a0)) := by
  have h1 : 0 < a0 + A := by linarith
  have hlog : 1 - a0 * A / (a0 + A) / a0 = (1 + A / a0)⁻¹ := by
    field_simp; ring
  unfold W
  rw [hlog, Real.log_inv]
  field_simp
  ring

/-! ## 2. μ from the γ = 0 P equation -/

theorem mu_from_P (a0 x : ℝ) (ha : 0 < a0) (hx : 0 < x) :
    1 - (a0 * x / (1 + x)) / (a0 * x) = x / (1 + x) := by
  have h1 : 0 < 1 + x := by linarith
  field_simp
  ring

/-! ## 3. λ and the vanishing momentum density
`nl` = n·∂ ln Q, `nPi` = n·∂Π₊, `Pi` = Π₊. The normal part of E2 reads −nl + γ(nPi − Pi nl) − λ = 0. -/

theorem lambda_solve (γ nl nPi Pi lam : ℝ) :
    (-nl + γ * (nPi - Pi * nl) - lam = 0) ↔ lam = -(1 + γ * Pi) * nl + γ * nPi := by
  constructor <;> intro h <;> linarith

/-- the P-sector momentum density is P_i [nl + λ − γ (nPi − Pi nl)]; it vanishes once λ is used -/
theorem momentum_density_zero (γ nl nPi Pi : ℝ) :
    nl + (-(1 + γ * Pi) * nl + γ * nPi) - γ * (nPi - Pi * nl) = 0 := by ring

/-! ## 4. On-shell stress -/

/-- vector form: if A + γE = (w/|P|) P then P·A + γ P·E = w |P| -/
theorem stress_contraction (P A E : EuclideanSpace ℝ (Fin 3)) (γ w : ℝ) (hP : P ≠ 0)
    (h : A + γ • E = (w / ‖P‖) • P) :
    inner ℝ P A + γ * inner ℝ P E = w * ‖P‖ := by
  have hn : ‖P‖ ≠ 0 := norm_ne_zero_iff.mpr hP
  have := congrArg (fun v => inner ℝ P v) h
  simp only [inner_add_right, inner_smul_right, real_inner_self_eq_norm_sq] at this
  rw [this]; field_simp

/-- spherical T_rr with Π' taken from the P equation equals B²(γF − W) -/
theorem Trr_on_shell (B p Pi Phi1 γ K Wv Wp : ℝ) (hγ : γ ≠ 0) :
    -B ^ 2 * Wv + K * Wp * p * B - p * Phi1 * (1 + γ * Pi)
      - γ * p * ((B * K * Wp - (1 + γ * Pi) * Phi1) / γ) + γ * B ^ 2 * (Pi ^ 2 / 2)
      = B ^ 2 * (γ * (Pi ^ 2 / 2) - Wv) := by
  field_simp
  ring

/-! ## 5. The K(Q) lapse derivative -/

theorem KQ_lapse_deriv (N : ℝ) (hN : N ≠ 0) :
    HasDerivAt (fun n : ℝ => n * (1 / n - 1) ^ 2) (1 - 1 / N ^ 2) N := by
  have hi : HasDerivAt (fun v : ℝ => v⁻¹) (-(N ^ 2)⁻¹) N := hasDerivAt_inv hN
  have h1 : HasDerivAt (fun v : ℝ => v⁻¹ - 2 + v) (-(N ^ 2)⁻¹ - 0 + 1) N :=
    ((hi.sub (hasDerivAt_const N (2:ℝ))).add (hasDerivAt_id' N))
  have heq : (fun n : ℝ => n * (1 / n - 1) ^ 2) =ᶠ[nhds N] (fun n : ℝ => n⁻¹ - 2 + n) := by
    filter_upwards [isOpen_ne.mem_nhds hN] with x hx
    have hx' : x ≠ 0 := hx
    field_simp
    ring
  exact (h1.congr_of_eventuallyEq heq).congr_deriv (by field_simp; ring)

/-! ## 6. FRW dust of K(Q) -/

theorem frw_dust (μ K I0 a : ℝ) (hμ : 0 < μ) (hK : 0 < K) (ha : 0 < a) :
    let Q := 1 + I0 / (2 * μ ^ 2 * a ^ 3)
    let w0 := I0 / (4 * μ ^ 2)
    μ ^ 2 / (2 * K) * (Q ^ 2 - 1) = I0 * (1 + w0 / a ^ 3) / (2 * K * a ^ 3) := by
  intro Q w0
  simp only [Q, w0]
  field_simp
  ring

/-! ## 7. AC2q: Σ = Π + Q² -/

theorem ac2q_frw_stress_zero (Q : ℝ) :
    -(Q ^ 2) ^ 2 / 2 + Q ^ 4 / 2 = 0 ∧ -2 * Q ^ 2 * Q ^ 2 + 2 * Q ^ 4 = 0 := by
  constructor <;> ring

/-- on-region foliation energy of the P + stiffness sector -/
theorem ac2q_nn_on (Pi Q γ : ℝ) :
    Pi + γ * ((Pi + Q ^ 2) ^ 2 / 2 - 2 * Q ^ 2 * (Pi + Q ^ 2) + 3 * Q ^ 4 / 2)
      = Pi * (1 - γ * Q ^ 2) + γ * Pi ^ 2 / 2 := by ring

/-- at the switch (Π = −Q²) the on-region value equals the off-region value Π + (3/2)γQ⁴ -/
theorem ac2q_nn_continuous (Q γ : ℝ) :
    (-Q ^ 2) * (1 - γ * Q ^ 2) + γ * (-Q ^ 2) ^ 2 / 2 = -Q ^ 2 + 3 / 2 * γ * Q ^ 4 := by ring

end QX17B

#print axioms QX17B.legendre_stationary
#print axioms QX17B.legendre_value
#print axioms QX17B.mu_from_P
#print axioms QX17B.lambda_solve
#print axioms QX17B.momentum_density_zero
#print axioms QX17B.stress_contraction
#print axioms QX17B.Trr_on_shell
#print axioms QX17B.KQ_lapse_deriv
#print axioms QX17B.frw_dust
#print axioms QX17B.ac2q_frw_stress_zero
#print axioms QX17B.ac2q_nn_on
#print axioms QX17B.ac2q_nn_continuous
