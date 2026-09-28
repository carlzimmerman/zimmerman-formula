import Mathlib
import Mathlib.Tactic

/-
  AS040 -- AQUAL and QUMOND spherical correspondence (Lean 4 certificate).

  Object: for spherical mass distributions the AQUAL relation
      mu(x) * x = y                     (x = g/a0 = |grad Phi|/a0, y = B/a0)
  and the QUMOND relation
      x = nu(y) * y
  give identical forces iff the pair (mu, nu) satisfies the matched identity
      mu(x(y)) * nu(y) = 1        at the matched argument x(y) = y * nu(y).

  Formalized content (dimensionless; both a0 footings apply unchanged):
    A  generic_correspondence: y = x*mu(x) and x = y*nu(y) (x, y nonzero)
       imply mu(x)*nu(y) = 1.  This IS the correspondence condition: each
       side is the other's algebraic inverse at matched arguments; the same-
       argument product mu(y)*nu(y) is NOT 1 in general (numeric control NC1).
    B  q_correspondence: Q cell instantiation with
          muQ x = (sqrt(1+4x^2)-1)/(2x),  nuQ y = sqrt(1+1/y),
          xQ y = y*nuQ y = sqrt(y^2+y):
       muQ (xQ y) * nuQ y = 1  for all y > 0  (exact pair identity).
    C  q_pair_forward: the matched pair satisfies the forward AQUAL law
          xQ y * muQ (xQ y) = y  for all y > 0.
    D  wBad_nonmonotone: w(x) = x^2 + x^3 - x^4/2 (= x*mu_bad(x),
       mu_bad(x) = x + x^2 - x^3/2) is not monotone on (0, inf):
       w(1) < w(2) and w(5/2) < w(2) with 1 < 2 < 5/2.  The derivative
       factorization w'(x) = x(2-x)(2x+1) (values w'(1) = 3, w'(5/2) = -15/2)
       is used in the numeric layer.
    E  two_roots: for every y0 in (0,4) there exist TWO distinct positive roots
       of w(x) = y0 (one in (0,2), one in (2,3)): y = x*mu_bad(x) is
       multi-valued, so the AQUAL--QUMOND correspondence is NOT a single-valued
       function when x*mu(x) is non-monotone (breakage domain).
-/

noncomputable section
open Real

/- A: the generic correspondence condition. -/
theorem generic_correspondence (mu nu : ℝ → ℝ) {x y : ℝ} (_hx : x ≠ 0) (hy : y ≠ 0)
    (hxy : y = x * mu x) (hyx : x = y * nu y) : mu x * nu y = 1 := by
  have h2 : y = (y * nu y) * mu x := by
    calc
      y = x * mu x := hxy
      _ = (y * nu y) * mu x := by rw [hyx]
  have h3 : (y * nu y) * mu x = y := h2.symm
  have h5 : (nu y * mu x) * y = 1 * y := by
    calc
      (nu y * mu x) * y = y * (nu y * mu x) := by ring
      _ = (y * nu y) * mu x := by ring
      _ = y := h3
      _ = 1 * y := by ring
  exact (mul_right_cancel₀ hy) (by simpa [mul_comm] using h5)

/- Q cell kernels. -/
def muQ (x : ℝ) : ℝ := (Real.sqrt (1 + 4 * x ^ 2) - 1) / (2 * x)
def nuQ (y : ℝ) : ℝ := Real.sqrt (1 + 1 / y)
def xQ (y : ℝ) : ℝ := y * nuQ y

theorem xQ_eq_sqrt (y : ℝ) (hy : 0 < y) : xQ y = Real.sqrt (y ^ 2 + y) := by
  unfold xQ nuQ
  have harg : 0 ≤ 1 + 1 / y := by
    exact add_nonneg zero_le_one (div_nonneg zero_le_one (le_of_lt hy))
  have hsq : (y * Real.sqrt (1 + 1 / y)) ^ 2 = y ^ 2 + y := by
    rw [mul_pow]
    rw [Real.sq_sqrt harg]
    field_simp [hy.ne']
  have hpos2 : 0 ≤ y * Real.sqrt (1 + 1 / y) := by
    exact mul_nonneg (le_of_lt hy) (Real.sqrt_nonneg _)
  have hs : Real.sqrt ((y * Real.sqrt (1 + 1 / y)) ^ 2) = y * Real.sqrt (1 + 1 / y) := by
    rw [Real.sqrt_sq_eq_abs, abs_of_nonneg hpos2]
  calc
    y * Real.sqrt (1 + 1 / y) = Real.sqrt ((y * Real.sqrt (1 + 1 / y)) ^ 2) := hs.symm
    _ = Real.sqrt (y ^ 2 + y) := by rw [hsq]

/- C: the matched pair satisfies the forward AQUAL law x*mu(x) = y. -/
theorem q_pair_forward (y : ℝ) (hy : 0 < y) : xQ y * muQ (xQ y) = y := by
  have hy2 : 0 ≤ y ^ 2 + y := by nlinarith [sq_nonneg y, hy]
  unfold muQ
  rw [xQ_eq_sqrt y hy]
  rw [Real.sq_sqrt hy2]
  have harg : 1 + 4 * (y ^ 2 + y) = (2 * y + 1) ^ 2 := by ring
  have hsqrt : Real.sqrt (1 + 4 * (y ^ 2 + y)) = 2 * y + 1 := by
    rw [harg]
    rw [Real.sqrt_sq_eq_abs]
    exact abs_of_nonneg (by nlinarith)
  have hsn : Real.sqrt (y ^ 2 + y) ≠ 0 := by
    have hp : 0 < y ^ 2 + y := by nlinarith [sq_nonneg y, hy]
    exact ne_of_gt (Real.sqrt_pos.2 hp)
  rw [hsqrt]
  field_simp [hsn]
  ring

/- B: Q-cell correspondence identity: muQ (xQ y) * nuQ y = 1 for y > 0. -/
theorem q_correspondence (y : ℝ) (hy : 0 < y) : muQ (xQ y) * nuQ y = 1 := by
  have hf := q_pair_forward y hy
  have hxy : y = xQ y * muQ (xQ y) := hf.symm
  have hxneq : xQ y ≠ 0 := by
    intro hz
    have : y = 0 := by simpa [hz] using hf.symm
    nlinarith [hy]
  exact generic_correspondence muQ nuQ hxneq (ne_of_gt hy) hxy rfl

/- D: counterexample -- w(x) = x*mu_bad(x) = x^2 + x^3 - x^4/2 is not monotone. -/
def wBad (x : ℝ) : ℝ := x ^ 2 + x ^ 3 - x ^ 4 / 2

theorem wBad_nonmonotone : wBad 1 < wBad 2 ∧ wBad (5 / 2) < wBad 2 := by
  constructor <;> norm_num [wBad]

/- E: for every y0 in (0, 4) there are two distinct positive roots of w(x) = y0. -/
theorem two_roots (y0 : ℝ) (hy0 : 0 < y0) (hy04 : y0 < 4) :
    ∃ x1 x2 : ℝ, 0 < x1 ∧ x1 < 2 ∧ 2 < x2 ∧ wBad x1 = y0 ∧ wBad x2 = y0 ∧ x1 ≠ x2 := by
  have hcont : Continuous wBad := by
    unfold wBad
    continuity
  have hw0 : wBad 0 = 0 := by norm_num [wBad]
  have hw2 : wBad 2 = 4 := by norm_num [wBad]
  have hw3 : wBad 3 = -9 / 2 := by norm_num [wBad]
  have h1 : ∃ x ∈ Set.Icc (0 : ℝ) 2, wBad x = y0 := by
    refine intermediate_value_Icc (by norm_num) (Continuous.continuousOn hcont) ?_
    constructor
    · rw [hw0]
      exact hy0.le
    · rw [hw2]
      exact le_of_lt hy04
  rcases h1 with ⟨x1, hx1i, hx1⟩
  have hx1a : x1 ≠ 0 := by
    intro hz
    rw [hz] at hx1
    have : y0 = 0 := by simpa [hw0] using hx1.symm
    nlinarith [hy0]
  have hx1b : x1 ≠ 2 := by
    intro hz
    rw [hz] at hx1
    have : y0 = 4 := by simpa [hw2] using hx1.symm
    nlinarith [hy04]
  have hx1pos : 0 < x1 := lt_of_le_of_ne hx1i.1 (Ne.symm hx1a)
  have hx1lt2 : x1 < 2 := lt_of_le_of_ne hx1i.2 hx1b
  have h2 : ∃ x ∈ Set.Icc (2 : ℝ) 3, -wBad x = -y0 := by
    refine intermediate_value_Icc (by norm_num) (Continuous.continuousOn hcont.neg) ?_
    constructor
    · change -wBad 2 ≤ -y0
      rw [show wBad 2 = 4 by norm_num [wBad]]
      nlinarith [hy04]
    · change -y0 ≤ -wBad 3
      rw [show wBad 3 = -9 / 2 by norm_num [wBad]]
      nlinarith [hy0]
  rcases h2 with ⟨x2, hx2i, hx2⟩
  have hx2eq : wBad x2 = y0 := neg_inj.mp hx2
  have hx2b : x2 ≠ 2 := by
    intro hz
    rw [hz] at hx2eq
    have : y0 = 4 := by simpa [hw2] using hx2eq.symm
    nlinarith [hy04]
  have hx2gt2 : 2 < x2 := lt_of_le_of_ne hx2i.1 (Ne.symm hx2b)
  refine ⟨x1, x2, hx1pos, hx1lt2, hx2gt2, hx1, hx2eq, ?_⟩
  exact ne_of_lt (lt_trans hx1lt2 hx2gt2)

end
