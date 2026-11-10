/-
REL1 (criteria e495153acf): Lean statements for the closed forms of step 1. They certify the algebra, not the physics.
TEST lane; adopts nothing. kappa = 1/2 FITTED; not theory closed.

Reduced matter Lagrangian about a background (one displacement component xi, rho > 0, Jpp = J'' > 0, k >= 0):
  L = rho xi'^2/2 + Jpp xi''^2/2 - k xi^2/2 ,  Euler-Lagrange  Jpp xi'''' - rho xi'' - k xi = 0 .

  runaway_root      : x = (rho + S) / (2 Jpp) with S^2 = rho^2 + 4 Jpp k solves Jpp x^2 - rho x - k = 0 (x = s^2);
                      runaway_root_sqrt is the same with S = sqrt(rho^2 + 4 Jpp k).
  runaway_root_pos  : and x > 0, so s = sqrt x is a real growth rate (elastic or pressure restoring k does not remove it).
  runaway_k0        : at k = 0 the root is rho / Jpp.
  ostrogradsky_unbounded : H = p1 q2 + p2^2/(2 Jpp) - rho q2^2/2 + k q1^2/2 takes a value below any bound M
                      (q2 /= 0, p1 free): the Hamiltonian is unbounded below.
  hessian_along, hessian_across : for J(y) = (a0^2/K)(y/a0 - ln(1 + y/a0)), J'(y) = (a0/K) (y/a0)/(1 + y/a0);
                      along A_rel the difference quotient of J'/a0 is 1/(K (1+u)(1+u')), -> 1/(K (1+u)^2) at u' = u;
                      across A_rel J'(y)/y = 1/(K (1+u)), u = y/a0; both positive (hessian_pos).
  rate_ratio        : rho / (1/(K(1+u))) = K rho (1+u): the slowest runaway rate squared, never below K rho.
  stiffness_transverse : with M = m I and b . k = 0, b.(M + g k k^T)^{-1}.b = |b|^2/m (2D, written out).
-/
import Mathlib

namespace REL1

theorem runaway_root (rho Jpp k S : ℝ) (hJ : 0 < Jpp) (hS : S ^ 2 = rho ^ 2 + 4 * Jpp * k) :
    Jpp * ((rho + S) / (2 * Jpp)) ^ 2 - rho * ((rho + S) / (2 * Jpp)) - k = 0 := by
  have hJ' : Jpp ≠ 0 := hJ.ne'
  have e : Jpp * ((rho + S) / (2 * Jpp)) ^ 2 - rho * ((rho + S) / (2 * Jpp)) - k
      = (S ^ 2 - rho ^ 2 - 4 * Jpp * k) / (4 * Jpp) := by
    field_simp; ring
  rw [e, hS]; ring

/-- The same with S = sqrt(rho^2 + 4 Jpp k). -/
theorem runaway_root_sqrt (rho Jpp k : ℝ) (hJ : 0 < Jpp) (hrho : 0 ≤ rho) (hk : 0 ≤ k) :
    Jpp * ((rho + Real.sqrt (rho ^ 2 + 4 * Jpp * k)) / (2 * Jpp)) ^ 2
      - rho * ((rho + Real.sqrt (rho ^ 2 + 4 * Jpp * k)) / (2 * Jpp)) - k = 0 :=
  runaway_root rho Jpp k _ hJ (Real.sq_sqrt (by positivity))

theorem runaway_root_pos (rho Jpp k : ℝ) (hJ : 0 < Jpp) (hrho : 0 < rho) (hk : 0 ≤ k) :
    0 < (rho + Real.sqrt (rho ^ 2 + 4 * Jpp * k)) / (2 * Jpp) := by
  have : 0 ≤ Real.sqrt (rho ^ 2 + 4 * Jpp * k) := Real.sqrt_nonneg _
  positivity

theorem runaway_k0 (rho Jpp : ℝ) (hJ : 0 < Jpp) (hrho : 0 ≤ rho) :
    (rho + Real.sqrt (rho ^ 2 + 4 * Jpp * 0)) / (2 * Jpp) = rho / Jpp := by
  have : Real.sqrt (rho ^ 2 + 4 * Jpp * 0) = rho := by
    rw [mul_zero, add_zero]; exact Real.sqrt_sq hrho
  rw [this]
  field_simp
  ring

/-- The Ostrogradsky Hamiltonian is linear in p1: for q2 ≠ 0 it goes below any bound. -/
theorem ostrogradsky_unbounded (rho Jpp k q1 q2 p2 M : ℝ) (hJ : 0 < Jpp) (hq : q2 ≠ 0) :
    ∃ p1 : ℝ, p1 * q2 + p2 ^ 2 / (2 * Jpp) - rho * q2 ^ 2 / 2 + k * q1 ^ 2 / 2 < M := by
  refine ⟨(M - (p2 ^ 2 / (2 * Jpp) - rho * q2 ^ 2 / 2 + k * q1 ^ 2 / 2) - 1) / q2, ?_⟩
  rw [div_mul_cancel₀ _ hq]
  linarith

/-- J'(y) for the physical J, written on u = y / a0. -/
noncomputable def Jp (K a0 u : ℝ) : ℝ := (a0 / K) * (u / (1 + u))

/-- Along A_rel, by difference quotient: (J'(u')/a0 - J'(u)/a0)/(u' - u) = 1/(K (1+u)(1+u')), which at u' = u is
1/(K (1+u)^2), the Hessian eigenvalue along A_rel (derivative in y = a0 u). -/
theorem hessian_along (K a0 u u' : ℝ) (hK : K ≠ 0) (ha : a0 ≠ 0) (hu : 0 ≤ u) (hu' : 0 ≤ u') (hne : u' ≠ u) :
    (Jp K a0 u' / a0 - Jp K a0 u / a0) / (u' - u) = 1 / (K * (1 + u) * (1 + u')) := by
  have h1 : (1 + u) ≠ 0 := by linarith
  have h2 : (1 + u') ≠ 0 := by linarith
  have h3 : u' - u ≠ 0 := sub_ne_zero.mpr hne
  unfold Jp
  field_simp
  ring

/-- Across A_rel: J'(y)/y = 1/(K (1+u)) with y = a0 u, u > 0. -/
theorem hessian_across (K a0 u : ℝ) (hK : K ≠ 0) (ha : a0 ≠ 0) (hu : 0 < u) :
    Jp K a0 u / (a0 * u) = 1 / (K * (1 + u)) := by
  have h1 : (1 + u) ≠ 0 := by linarith
  unfold Jp
  field_simp

theorem hessian_pos (K u : ℝ) (hK : 0 < K) (hu : 0 ≤ u) :
    0 < 1 / (K * (1 + u) ^ 2) ∧ 0 < 1 / (K * (1 + u)) := by
  constructor <;> positivity

theorem rate_ratio (K rho u : ℝ) (hK : 0 < K) (hu : 0 ≤ u) :
    rho / (1 / (K * (1 + u))) = K * rho * (1 + u) ∧ K * rho ≤ K * rho * (1 + u) ∨ rho < 0 := by
  by_cases hr : rho < 0
  · exact Or.inr hr
  · left
    have h1 : (1 + u) ≠ 0 := by linarith
    refine ⟨by field_simp, ?_⟩
    push Not at hr
    nlinarith [mul_nonneg (mul_nonneg hK.le hr) hu]

/-- 2D: M = m I, b = (ky, -kx) transverse to k = (kx, ky): b.(M + g k k^T)^{-1}.b = |b|^2/m, g drops out. -/
theorem stiffness_transverse (m g kx ky : ℝ) (hm : 0 < m) (hg : 0 ≤ g) :
    let d := (m + g * kx ^ 2) * (m + g * ky ^ 2) - (g * kx * ky) ^ 2
    -- inverse of [[m + g kx^2, g kx ky], [g kx ky, m + g ky^2]] is (1/d) [[m + g ky^2, -g kx ky], [-g kx ky, m + g kx^2]]
    d ≠ 0 →
    (ky * ((m + g * ky ^ 2) * ky + (-(g * kx * ky)) * (-kx))
      + (-kx) * ((-(g * kx * ky)) * ky + (m + g * kx ^ 2) * (-kx))) / d
      = (kx ^ 2 + ky ^ 2) / m := by
  intro d hd
  have hd' : d = m * (m + g * (kx ^ 2 + ky ^ 2)) := by simp only [d]; ring
  rw [div_eq_div_iff hd hm.ne', hd']
  ring

end REL1
-- kappa = 1/2 FITTED; not theory closed. Adopts nothing.
