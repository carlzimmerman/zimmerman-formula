import Mathlib

/-!
AS245 — external-field correction from the filtered action (CA5-GNC-R, filtered MONO)
Run AS245-efe-r1-20260928T1711Z-dsv4f-hermes.

Certified algebraic core (all statements in the scalar/function idiom of the
sibling AS043 certificate; no metric/typeclass machinery):
  C_ij = C_T (delta_ij - e_i e_j) + C_L e_i e_j,  e = p0/|p0|,  p0 = D S u_external,
  C_T = nu(y) - 1,  C_L = (nu - 1) + y nu'(y),  y = |p0|/a0.

T1-T2: the response map  (C v)_i = C_T v_i + (C_L - C_T) e_i (e.v)  has eigenvalue
        C_L along the unit external direction e and C_T in every transverse
        direction (e.w = 0)  --  the two eigenvalues 4 C_L, 4 C_T of the action
        Hessian (FINAL_ACTION: "regular nonzero Hessian eigenvalues are 4 C_T, 4 C_L").
T3:    quadratic form  k . (C k) = C_T |k|^2 + (C_L - C_T) (e.k)^2  -- the
        direction-weighted Green-function symbol M(k) = 1 + S^2(k)(...) .
T4-T6: exact power-law core of the deep limit (nu = C y^-1/2, y nu' = -nu/2):
        C_L = nu/2 - 1,  2 C_L - C_T = -1 exactly  (branch constants c enter as
        2 C_L - C_T = c - 1: Q c=0 -> -1, RAR/MONO c=1/2 -> -1/2, EXP c=1/4 -> -3/4,
        MU2 c=3/8 -> -5/8; all verified numerically in raw_output.json), and
        C_L/C_T - 1/2 = -1/(2(nu-1))  (convergence rate to the deep ratio 1/2).
T7:    heat-semigroup power action on an eigen-mode: if P acts as P v = lam v for
        every v, then (P iterated n times) f = lam^n f -- with P = b*Delta_h on the
        l=1 sphere mode of the curved leaf (Delta_h Y_1m = -(2/R^2) Y_1m), so
        lam = b*(-2/R^2) and the heat factor is exp(b*Delta) f = exp(-2b/R^2) f;
        the exponential closure exp(b Delta) f = exp(b lam) f then follows from the
        defining power series of Real.exp.  The attenuation identity
        exp(-2b/R^2) = exp(-xi^2/R^2) from 2b = xi^2 is T7b.
-/
noncomputable section

open scoped BigOperators

namespace AS245

-- inner product on the 2-leaf (Fin 2 -> Real functions), expanded form
def inner2 (a b : Fin 2 → ℝ) : ℝ := a 0 * b 0 + a 1 * b 1

-- the external-field response map  (C v)_i = C_T v_i + (C_L - C_T) e_i (e . v)
def Cvec (C_T C_L : ℝ) (e v : Fin 2 → ℝ) (i : Fin 2) : ℝ :=
  C_T * v i + (C_L - C_T) * (e i * inner2 e v)

-- ---------------------------------------------------------------------------
-- T1: longitudinal eigenvalue C_L  (unit external direction: |e|^2 = 1)
-- ---------------------------------------------------------------------------
theorem tensor_on_external_direction (C_T C_L : ℝ) (e : Fin 2 → ℝ)
    (he : e 0 * e 0 + e 1 * e 1 = 1) :
    Cvec C_T C_L e e = C_L • e := by
  ext i
  fin_cases i <;> simp [Cvec, inner2] <;> rw [he] <;> ring

-- ---------------------------------------------------------------------------
-- T2: transverse eigenvalue C_T  (e . w = 0)
-- ---------------------------------------------------------------------------
theorem tensor_on_transverse_direction (C_T C_L : ℝ) (e w : Fin 2 → ℝ)
    (hw : e 0 * w 0 + e 1 * w 1 = 0) :
    Cvec C_T C_L e w = C_T • w := by
  ext i
  fin_cases i <;> simp [Cvec, inner2, hw] <;> ring

-- ---------------------------------------------------------------------------
-- T3: quadratic form = the direction weight of the Green-function symbol
-- ---------------------------------------------------------------------------
theorem tensor_quadratic_form (C_T C_L : ℝ) (e k : Fin 2 → ℝ) :
    inner2 k (Cvec C_T C_L e k)
      = C_T * (k 0 * k 0 + k 1 * k 1) + (C_L - C_T) * (inner2 e k) ^ 2 := by
  simp [Cvec, inner2]
  ring

-- ---------------------------------------------------------------------------
-- T3b: cos^2-weighted symbol at a unit wavenumber direction
-- ---------------------------------------------------------------------------
theorem symbol_cos2_weight (C_T C_L : ℝ) (e k : Fin 2 → ℝ)
    (hk2 : k 0 * k 0 + k 1 * k 1 = 1) :
    C_T + (C_L - C_T) * (inner2 e k) ^ 2 = inner2 k (Cvec C_T C_L e k) := by
  rw [tensor_quadratic_form, hk2]
  ring

-- ---------------------------------------------------------------------------
-- T4: deep power-law value of C_L
--     premises: cL = (nu - 1) + y d,  y d = -nu/2  (i.e. nu' = -(C/2) y^-3/2)
-- ---------------------------------------------------------------------------
theorem deep_cL_powerlaw (cL ν d y : ℝ) (hcL : cL = (ν - 1) + y * d)
    (hyd : y * d = -(1 / 2) * ν) :
    cL = ν / 2 - 1 := by
  nlinarith [hcL, hyd]

-- ---------------------------------------------------------------------------
-- T5: exact identity 2 C_L - C_T = -1 on the power law
-- ---------------------------------------------------------------------------
theorem two_cL_minus_cT_powerlaw (cL cT ν : ℝ) (hcL : cL = ν / 2 - 1)
    (hcT : cT = ν - 1) :
    2 * cL - cT = -1 := by
  rw [hcL, hcT]
  ring

-- ---------------------------------------------------------------------------
-- T6: deviation of the deep ratio from 1/2
-- ---------------------------------------------------------------------------
theorem deep_ratio_deviation (cL cT ν : ℝ) (hcL : cL = ν / 2 - 1)
    (hcT : cT = ν - 1) (hν : ν ≠ 1) :
    cL / cT - 1 / 2 = -1 / (2 * (ν - 1)) := by
  rw [hcL, hcT]
  field_simp [hν, sub_ne_zero_of_ne hν]
  ring

-- ---------------------------------------------------------------------------
-- T7a: heat-semigroup power action on an eigen-mode
--      itop n P f = (b*lam)^n f  for every n, given P v = lam v for all v
-- ---------------------------------------------------------------------------
def itop : ℕ → (E → E) → (E → E)
  | 0, _ => fun x => x
  | n + 1, g => itop n g ∘ g

theorem heat_power_eigen {E : Type} [AddCommGroup E] [Module ℝ E] (P : E → E)
    (lam : ℝ) (heig : ∀ v : E, P v = lam • v) :
    ∀ n : ℕ, ∀ f : E, itop n P f = lam ^ n • f := by
  intro n
  induction n
  case zero =>
    intro f
    simp [itop]
  case succ n ih =>
    intro f
    rw [itop]
    calc
      itop n P (P f) = lam ^ n • (P f) := by exact ih (P f)
      _ = lam ^ n • (lam • f) := by rw [heig]
      _ = (lam ^ n * lam) • f := by rw [smul_smul]
      _ = lam ^ (n + 1) • f := by rw [← pow_succ]

-- ---------------------------------------------------------------------------
-- T7b: curved-leaf l=1 attenuation factor identity (2b = xi^2)
-- ---------------------------------------------------------------------------
theorem sphere_attenuation_factor (ξ b R : ℝ) (hb : 2 * b = ξ ^ 2) :
    Real.exp (-(2 * b) / R ^ 2) = Real.exp (-(ξ ^ 2) / R ^ 2) := by
  have harg : -(2 * b) / R ^ 2 = -(ξ ^ 2) / R ^ 2 := by
    rw [← hb]
  rw [harg]

-- ---------------------------------------------------------------------------
-- T8: transverse-gain symbol of the Green function (k . e = 0) reduces to C_T
-- ---------------------------------------------------------------------------
theorem transverse_gain_symbol (C_T C_L S2 : ℝ) (e k : Fin 2 → ℝ)
    (hw : inner2 e k = 0) :
    1 + S2 * (C_T + (C_L - C_T) * (inner2 e k) ^ 2) = 1 + S2 * C_T := by
  simp [hw]

end AS245

#check AS245.tensor_on_external_direction
#check AS245.tensor_on_transverse_direction
#check AS245.tensor_quadratic_form
#check AS245.symbol_cos2_weight
#check AS245.deep_cL_powerlaw
#check AS245.two_cL_minus_cT_powerlaw
#check AS245.deep_ratio_deviation
#check AS245.heat_power_eigen
#check AS245.sphere_attenuation_factor
#check AS245.transverse_gain_symbol

#print axioms AS245.tensor_on_external_direction
#print axioms AS245.tensor_on_transverse_direction
#print axioms AS245.tensor_quadratic_form
#print axioms AS245.symbol_cos2_weight
#print axioms AS245.deep_cL_powerlaw
#print axioms AS245.two_cL_minus_cT_powerlaw
#print axioms AS245.deep_ratio_deviation
#print axioms AS245.heat_power_eigen
#print axioms AS245.sphere_attenuation_factor
#print axioms AS245.transverse_gain_symbol