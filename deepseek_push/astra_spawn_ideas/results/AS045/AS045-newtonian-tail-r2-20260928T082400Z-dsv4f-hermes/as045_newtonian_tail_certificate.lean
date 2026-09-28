import Mathlib
import Mathlib.Tactic

/-!
AS045 (REDO) -- Newtonian-tail ordering of the three kernels (Lean 4 certificate).

Seed: deepseek_push/astra_spawn_ideas/AS045_newtonian_tail_ordering_of_the_three_kernels.md
sha256 2f7f4fa561e1625a234f4210e10c8bcd64a8d98f869d88b553e094f45187372f

Certified algebraic content (declared branch dictionary of FRAMEWORK_CONTRACT.md):

  Q   : g^2 = B^2 + a0*B,  y = B/a0 = g_N/a0 > 0,  x = g/a0
        nu_Q(y) = sqrt(1 + 1/y), relative anomaly nu_Q - 1,
        absolute anomaly a0*y*(nu_Q - 1).

  A   q_rationalized : y*(sqrt(1+1/y) - 1) = 1/(sqrt(1+1/y)+1)   (y > 0)
        (rationalization identity; separates the leading 1/(2y) tail)

  B   q_tail_bounds  : for y >= 1,
        1/2 - 1/(8y) <= y*(sqrt(1+1/y) - 1) <= 1/2
        (two-sided Newtonian-tail bound; the sharp upper constant 1/2 is
        the a0/2 absolute-anomaly offset: B*(nu_Q-1) does NOT vanish)

  MU2 : mu2(x) = 1 - (1 + x/2)^(-2), mu2(x)*g = B, y = x*mu2(x), nu_MU2 = x/y.

  C   mu2_nu_minus_one_closed_form : for x > 0,
        (x - x*mu2(x))/(x*mu2(x)) = 4/(x*(x+4))
        (exact closed form of the MU2 relative anomaly; pure algebra)

  D   mu2_tail_bound_by_y : (x - x*mu2(x))/(x*mu2(x)) <= 4/(x*mu2(x))^2
        (power-law tail 4/y^2 in the Newtonian variable y = x*mu2(x);
        distinct from Q's 1/(2y) and RAR's e^{-sqrt y})

  E   q_mu2_coincidence_y3 : at x = 2*sqrt 3 (y = 3),
        x*mu2(x) = 3  and  sqrt(1+1/3) = 2/sqrt(3) = x/3
        (the Q and MU2 relative-tail curves cross EXACTLY at y = 3;
        a coincidence of two distinct branches, not an equivalence --
        RAR does not share the point; see numeric check C16)

All declarations are over the reals.  No measure, derivative or asymptotic
limit is claimed by this file.  The physical constants (a0 = kappa*c*sqrt(G*rho_Lambda),
kappa = 1/2 adopted) are NOT part of the formal statements (dimensionless
y-form only).
-/

noncomputable section
open Real

/-- Q-branch response variable: s(y) = sqrt(1 + 1/y), y = B/a0 > 0. -/
def sq1p (y : ℝ) : ℝ := Real.sqrt (1 + 1 / y)

/-- MU2 constitutive response: mu2(x) = 1 - (1 + x/2)^(-2). -/
def mu2n (x : ℝ) : ℝ := 1 - (1 + x / 2) ^ (-2 : ℤ)

/-- s(y)^2 = 1 + 1/y on the physical domain y > 0. -/
lemma sq1p_sq (y : ℝ) (hy : 0 < y) : (sq1p y) ^ 2 = 1 + 1 / y := by
  dsimp [sq1p]
  exact Real.sq_sqrt (by positivity : 0 ≤ 1 + 1 / y)

/-- s(y) >= 1 for y >= 1. -/
lemma sq1p_ge_one (y : ℝ) (hy : 1 ≤ y) : 1 ≤ sq1p y := by
  dsimp [sq1p]
  have hyinv : 0 < 1 / y := by positivity
  have hle : 1 ≤ 1 + 1 / y := by nlinarith [hyinv]
  have hmono := Real.sqrt_le_sqrt hle
  simpa using hmono

/-! A. Q-branch rationalization identity -/

theorem q_rationalized (y : ℝ) (hy : 0 < y) :
    y * (sq1p y - 1) = 1 / (sq1p y + 1) := by
  have hy0 : y ≠ 0 := ne_of_gt hy
  have hsp : sq1p y + 1 ≠ 0 := by
    have : 0 ≤ sq1p y := by dsimp [sq1p]; positivity
    linarith
  have hsq1 : sq1p y ^ 2 - 1 = 1 / y := by
    have hsq0 := sq1p_sq y hy
    nlinarith [hsq0]
  calc
    y * (sq1p y - 1) = y * ((sq1p y ^ 2 - 1) / (sq1p y + 1)) := by
      congr 1
      field_simp [hsp]
      ring
    _ = y * ((1 / y) / (sq1p y + 1)) := by rw [hsq1]
    _ = 1 / (sq1p y + 1) := by
      field_simp [hy0, hsp]

/-! B. Q-branch two-sided Newtonian-tail bounds (y >= 1) -/

/-- s(y) <= (4y+1)/(4y-1) for y >= 1 (square comparison; both sides nonnegative). -/
lemma sq1p_le_frac (y : ℝ) (hy : 1 ≤ y) : sq1p y ≤ (4 * y + 1) / (4 * y - 1) := by
  have hy0 : 0 < y := by linarith
  have hy4 : 0 < 4 * y - 1 := by nlinarith [hy]
  have hsq2 : (sq1p y) ^ 2 ≤ ((4 * y + 1) / (4 * y - 1)) ^ 2 := by
    rw [sq1p_sq y hy0]
    rw [div_pow]
    rw [le_div_iff₀ (sq_pos_of_pos hy4)]
    field_simp [hy0.ne']
    nlinarith [hy]
  have hnonneg_r : 0 ≤ (4 * y + 1) / (4 * y - 1) := by positivity
  have habs : |sq1p y| ≤ |(4 * y + 1) / (4 * y - 1)| := (sq_le_sq.mp hsq2)
  have hnonneg_l : 0 ≤ sq1p y := by dsimp [sq1p]; positivity
  rw [abs_of_nonneg hnonneg_l, abs_of_nonneg hnonneg_r] at habs
  exact habs

/-- Upper tail bound: y*(nu_Q - 1) <= 1/2 with sharp constant. -/
lemma q_tail_up (y : ℝ) (hy : 1 ≤ y) : 1 / (sq1p y + 1) ≤ 1 / 2 := by
  have hs : 1 ≤ sq1p y := sq1p_ge_one y hy
  have hsp : 0 < sq1p y + 1 := by linarith
  rw [div_le_iff₀ hsp]
  nlinarith [hs]

/-- Lower tail bound: 1/2 - 1/(8y) <= y*(nu_Q - 1). -/
lemma q_tail_low (y : ℝ) (hy : 1 ≤ y) : 1 / 2 - 1 / (8 * y) ≤ 1 / (sq1p y + 1) := by
  have hy0 : 0 < y := by linarith
  have hy4 : 0 < 4 * y - 1 := by nlinarith [hy]
  have hlep := sq1p_le_frac y hy
  have ha_pos : 0 < 1 / 2 - 1 / (8 * y) := by
    field_simp [hy0.ne']
    nlinarith [hy]
  have hsp : 0 < sq1p y + 1 := by
    have : 0 ≤ sq1p y := by dsimp [sq1p]; positivity
    linarith
  rw [le_div_iff₀ hsp]
  have hstep : sq1p y + 1 ≤ 8 * y / (4 * y - 1) := by
    have h1 : sq1p y + 1 ≤ (4 * y + 1) / (4 * y - 1) + 1 := by linarith [hlep]
    have h2 : (4 * y + 1) / (4 * y - 1) + 1 = 8 * y / (4 * y - 1) := by
      field_simp [hy4.ne']
      ring
    linarith
  calc
    (1 / 2 - 1 / (8 * y)) * (sq1p y + 1) ≤
        (1 / 2 - 1 / (8 * y)) * (8 * y / (4 * y - 1)) :=
      mul_le_mul_of_nonneg_left hstep (le_of_lt ha_pos)
    _ = 1 := by
      have h1 : 1 / 2 - 1 / (8 * y) = (4 * y - 1) / (8 * y) := by
        field_simp [hy0.ne']
        ring
      rw [h1]
      field_simp [hy0.ne', hy4.ne']

theorem q_tail_bounds (y : ℝ) (hy : 1 ≤ y) :
    1 / 2 - 1 / (8 * y) ≤ y * (sq1p y - 1) ∧ y * (sq1p y - 1) ≤ 1 / 2 := by
  have hy0 : 0 < y := by linarith
  rw [q_rationalized y hy0]
  exact ⟨q_tail_low y hy, q_tail_up y hy⟩

/-! C. MU2 positivity and exact closed form -/

theorem mu2_pos (x : ℝ) (hx : 0 < x) : 0 < mu2n x := by
  dsimp [mu2n]
  have hb : 1 < (1 + x / 2) ^ 2 := by nlinarith [hx]
  have hb2 : (1 + x / 2) ^ (-2 : ℤ) < 1 := by
    have hb_pow : 0 < (1 + x / 2) ^ 2 := by positivity
    have : ((1 + x / 2) ^ 2)⁻¹ < 1 := inv_lt_one_of_one_lt₀ hb
    simpa [zpow_neg, zpow_natCast] using this
  linarith

theorem mu2_nu_minus_one_closed_form (x : ℝ) (hx : 0 < x) :
    (x - x * mu2n x) / (x * mu2n x) = 4 / (x * (x + 4)) := by
  have hx0 : x ≠ 0 := ne_of_gt hx
  have hmu0 : mu2n x ≠ 0 := ne_of_gt (mu2_pos x hx)
  have hx40 : x * (x + 4) ≠ 0 := by positivity
  have hstep : (x - x * mu2n x) / (x * mu2n x) = (1 - mu2n x) / mu2n x := by
    field_simp [hx0, hmu0]
  rw [hstep]
  have hq : (1 + x / 2) ^ (-2 : ℤ) = ((1 + x / 2) ^ 2)⁻¹ := by
    rfl
  have hb1 : (1 + x / 2) ^ 2 ≠ 1 := by
    have : 1 < (1 + x / 2) ^ 2 := by nlinarith [hx]
    linarith
  have hb0 : (1 + x / 2) ^ 2 ≠ 0 := by positivity
  calc
    (1 - mu2n x) / mu2n x = ((1 + x / 2) ^ 2 - 1)⁻¹ := by
      dsimp [mu2n]
      rw [hq]
      field_simp [hb1, hb0]
      ring
    _ = 4 / (x * (x + 4)) := by
      have hsq : (1 + x / 2) ^ 2 - 1 = x * (x + 4) / 4 := by ring
      rw [hsq]
      field_simp [hx0, hx40]

/-! D. MU2 tail bound in the Newtonian variable y = x*mu2(x) -/

theorem mu2_tail_bound_by_y (x : ℝ) (hx : 0 < x) :
    (x - x * mu2n x) / (x * mu2n x) ≤ 4 / (x * mu2n x) ^ 2 := by
  have hmain := mu2_nu_minus_one_closed_form x hx
  rw [hmain]
  have hmu_le : mu2n x ≤ 1 := by
    dsimp [mu2n]
    have hq0 : 0 ≤ (1 + x / 2) ^ (-2 : ℤ) := by positivity
    linarith
  have hmu_pos : 0 < mu2n x := mu2_pos x hx
  have hyle : x * mu2n x ≤ x := by
    calc
      x * mu2n x ≤ x * 1 := mul_le_mul_of_nonneg_left hmu_le (le_of_lt hx)
      _ = x := by ring
  have hy2 : (x * mu2n x) ^ 2 ≤ x * (x + 4) := by
    have hx0 : 0 ≤ x := le_of_lt hx
    have hy0 : 0 ≤ x * mu2n x := mul_nonneg hx0 (le_of_lt hmu_pos)
    have hx4 : 0 ≤ x * (x + 4) := by positivity
    nlinarith [hyle, hy0, hx0, hx4]
  have hden1 : 0 < x * (x + 4) := by positivity
  have hden2 : 0 < (x * mu2n x) ^ 2 := sq_pos_of_pos (mul_pos hx hmu_pos)
  rw [div_le_div_iff₀ hden1 hden2]
  nlinarith [hy2]

/-! E. Exact Q-MU2 coincidence at x = 2 sqrt 3 (y = 3) -/

/-- mu2(2*sqrt 3) = sqrt 3 / 2. -/
lemma mu2_at_two_sqrt3 : mu2n (2 * Real.sqrt 3) = Real.sqrt 3 / 2 := by
  have hs : (Real.sqrt 3) ^ 2 = 3 := Real.sq_sqrt (by norm_num)
  dsimp [mu2n]
  ring_nf
  have hq : (1 + Real.sqrt 3) ^ (-2 : ℤ) = ((1 + Real.sqrt 3) ^ 2)⁻¹ := by
    rfl
  rw [hq]
  have hlin : (1 + Real.sqrt 3) ^ 2 = 4 + 2 * Real.sqrt 3 := by nlinarith [hs]
  rw [hlin]
  have hz : 4 + 2 * Real.sqrt 3 ≠ 0 := by positivity
  field_simp [hz]
  nlinarith [hs]

/-- sqrt(1 + 1/3) = 2/sqrt 3. -/
lemma q_at_three : sq1p 3 = 2 / Real.sqrt 3 := by
  have hs : (Real.sqrt 3) ^ 2 = 3 := Real.sq_sqrt (by norm_num)
  have hnon_r : 0 ≤ 2 / Real.sqrt 3 := by positivity
  have hnon_l : 0 ≤ sq1p 3 := by dsimp [sq1p]; positivity
  have hsq : (sq1p 3) ^ 2 = (2 / Real.sqrt 3) ^ 2 := by
    dsimp [sq1p]
    have hpos : (0 : ℝ) ≤ 1 + (1 : ℝ) / 3 := by norm_num
    rw [Real.sq_sqrt hpos]
    rw [div_pow, hs]
    norm_num
  have hprod : (sq1p 3 - 2 / Real.sqrt 3) * (sq1p 3 + 2 / Real.sqrt 3) = 0 := by
    nlinarith [hsq]
  have hsum : 0 < sq1p 3 + 2 / Real.sqrt 3 := by
    have h2 : 0 < 2 / Real.sqrt 3 := by positivity
    linarith
  have hz : sq1p 3 - 2 / Real.sqrt 3 = 0 := by
    exact (mul_eq_zero.mp hprod).resolve_right (ne_of_gt hsum)
  linarith

/-- At y = 3 (x = 2 sqrt 3) the Q and MU2 branches satisfy
    x*mu2(x) = 3 and nu_Q(3) = x/3: the relative tails cross exactly. -/
theorem q_mu2_coincidence_y3 :
    (2 * Real.sqrt 3) * mu2n (2 * Real.sqrt 3) = 3 ∧ sq1p 3 = 2 / Real.sqrt 3 := by
  constructor
  · have hm := mu2_at_two_sqrt3
    rw [hm]
    have hs : (Real.sqrt 3) ^ 2 = 3 := Real.sq_sqrt (by norm_num)
    field_simp
    nlinarith [hs]
  · exact q_at_three

#print axioms q_rationalized
#print axioms q_tail_bounds
#print axioms mu2_pos
#print axioms mu2_nu_minus_one_closed_form
#print axioms mu2_tail_bound_by_y
#print axioms q_mu2_coincidence_y3