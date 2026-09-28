/-
AS006 — The MOND radius as a dimensionless reduction (Lean 4 / Mathlib certificate).
Location: deepseek_push/astra_spawn_ideas/results/AS006/<run>/AS006_leancert_mond_radius.lean
Run: apple darwin, lake env lean, Mathlib (cached).

Scope note: Lean certifies the ALGEBRA of the reduction claimed in task AS006:
  r_M = sqrt(G*M_b/a0),  x = r/r_M,  B = G*M_b/r^2  =>  B/a0 = (r_M/r)^2 = x^-2,
  deep-limit g/a0 = sqrt(a0*B)/a0 = r_M/r  (=> v_flat^4 = G*M_b*a0),
  invariance of B/a0 under the simultaneous rescaling (M_b, a0) -> (lambda M_b, lambda a0),
  and the collapse to a common profile at equal x = r/r_M.
It does NOT certify physics: the point-baryon exterior, absence of external fields,
absence of a second scale (heat filter xi), and the kernel being a function of
B/a0 alone remain physical scoping assumptions stated in derivation.md.
-/
import Mathlib

noncomputable section
open scoped Real

namespace AS006

/-- r_M^2 = G*M/a0 for nonnegative G, M, a0: the MOND radius supplies the unique
length that makes B/a0 dimensionless. -/
theorem mond_radius_squared (G M a0 : ℝ) (hG : 0 ≤ G) (hM : 0 ≤ M) (ha0 : 0 ≤ a0) :
    (Real.sqrt (G * M / a0)) ^ 2 = G * M / a0 := by
  have h : 0 ≤ G * M / a0 := div_nonneg (mul_nonneg hG hM) ha0
  rw [Real.sq_sqrt h]

/-- (s / r)^2 = s^2 / r^2 for r ≠ 0 (division-pow helper). -/
theorem pow_two_div (s r : ℝ) (_hr : r ≠ 0) : (s / r) ^ 2 = s ^ 2 / r ^ 2 := by
  rw [div_eq_mul_inv, mul_pow, inv_pow, ← div_eq_mul_inv]

/-- Seed identity: B/a0 = (r_M/r)^2 = x^-2 for the spherical point baryon,
all positive variables. This is the exact dimensionless reduction. -/
theorem b_over_a0_eq_x_neg_two (G M a0 r : ℝ) (hG : 0 ≤ G) (hM : 0 ≤ M) (ha0 : 0 < a0)
    (hr : 0 < r) :
    G * M / (a0 * r ^ 2) = (Real.sqrt (G * M / a0) / r) ^ 2 := by
  rw [pow_two_div (Real.sqrt (G * M / a0)) r hr.ne']
  rw [mond_radius_squared G M a0 hG hM ha0.le]
  field_simp [ha0.ne', hr.ne']

/-- Deep-limit reduction: sqrt(a0*B)/a0 = r_M/r with B = G*M/r^2; equivalently
g_deep = a0*r_M/r = C/r with C = sqrt(G*M*a0). -/
theorem deep_accel_reduction (G M a0 r : ℝ) (hG : 0 < G) (hM : 0 < M) (ha0 : 0 < a0) (hr : 0 < r) :
    Real.sqrt (a0 * (G * M / r ^ 2)) / a0 = Real.sqrt (G * M / a0) / r := by
  have ha0n : 0 ≤ a0 := ha0.le
  have hgm : 0 ≤ G * M := mul_nonneg hG.le hM.le
  rw [Real.sqrt_mul ha0n (G * M / r ^ 2)]
  rw [Real.sqrt_div hgm (r ^ 2)]
  rw [Real.sqrt_sq_eq_abs]
  rw [abs_of_pos hr]
  rw [Real.sqrt_div hgm a0]
  have hs : Real.sqrt a0 ≠ 0 := by
    apply ne_of_gt
    rw [Real.sqrt_pos]
    exact ha0
  field_simp [Real.mul_self_sqrt ha0n, hs, hr.ne']
  exact Real.sq_sqrt ha0n

/-- Deep circular-speed quartic: v^2 = a0*r_M  =>  v^4 = G*M_b*a0, i.e. the
baryonic Tully-Fisher deep law is the same identity in equivalent variables. -/
theorem vflat_quartic (G M a0 : ℝ) (hG : 0 < G) (hM : 0 < M) (ha0 : 0 < a0) :
    (a0 * Real.sqrt (G * M / a0)) ^ 2 = G * M * a0 := by
  rw [mul_pow]
  rw [mond_radius_squared G M a0 hG.le hM.le ha0.le]
  field_simp [ha0.ne']

/-- Same prediction in equivalent variables: simultaneous rescaling
(M_b, a0) -> (lam*M_b, lam*a0) leaves r_M and the whole reduced profile
untouched; B/a0 is invariant. -/
theorem rM_rescaling_invariant (G M a0 lam : ℝ) (_hG : 0 ≤ G) (_hM : 0 ≤ M) (ha0 : 0 < a0) (hL : 0 < lam) :
    Real.sqrt (G * (lam * M) / (lam * a0)) = Real.sqrt (G * M / a0) := by
  have h1 : G * (lam * M) / (lam * a0) = G * M / a0 := by
    field_simp [hL.ne', ha0.ne']
  rw [h1]

/-- The dimensionless seed identity is invariant under the same rescaling. -/
theorem b_over_a0_rescaling_invariant (G M a0 r lam : ℝ) (_hG : 0 ≤ G) (_hM : 0 ≤ M) (ha0 : 0 < a0)
    (hr : 0 < r) (hL : 0 < lam) :
    G * (lam * M) / ((lam * a0) * r ^ 2) = G * M / (a0 * r ^ 2) := by
  field_simp [hL.ne', ha0.ne', hr.ne']

/-- Collapse to a common reduced profile: any two baryon masses at radii
r1 = x*r_M(M1), r2 = x*r_M(M2) with the same dimensionless radius x give the
same B/a0 (hence the same g/a0 under any kernel of B/a0). This is the
mass-independence of the reduced curve. -/
theorem collapse_same_x (G a0 M1 M2 x r1 r2 : ℝ) (hG : 0 < G) (ha0 : 0 < a0) (hM1 : 0 < M1)
    (hM2 : 0 < M2) (hr1 : 0 < r1) (hr2 : 0 < r2)
    (hx1 : r1 = x * Real.sqrt (G * M1 / a0)) (hx2 : r2 = x * Real.sqrt (G * M2 / a0)) :
    G * M1 / (a0 * r1 ^ 2) = G * M2 / (a0 * r2 ^ 2) := by
  rw [b_over_a0_eq_x_neg_two G M1 a0 r1 hG.le hM1.le ha0 hr1]
  rw [b_over_a0_eq_x_neg_two G M2 a0 r2 hG.le hM2.le ha0 hr2]
  rw [hx1, hx2]
  have hs1 : Real.sqrt (G * M1 / a0) ≠ 0 := by
    apply ne_of_gt
    rw [Real.sqrt_pos]
    exact div_pos (mul_pos hG hM1) ha0
  have hs2 : Real.sqrt (G * M2 / a0) ≠ 0 := by
    apply ne_of_gt
    rw [Real.sqrt_pos]
    exact div_pos (mul_pos hG hM2) ha0
  have hx_ne : x ≠ 0 := by
    intro hx0
    have hz : x * Real.sqrt (G * M1 / a0) = r1 := hx1.symm
    rw [hx0] at hz
    have hz0 : (0 : ℝ) = r1 := by simpa using hz
    exact (ne_of_lt hr1) hz0
  field_simp [hs1, hs2, hx_ne, hr1.ne', hr2.ne']

end AS006

#print axioms AS006.mond_radius_squared
#print axioms AS006.b_over_a0_eq_x_neg_two
#print axioms AS006.deep_accel_reduction
#print axioms AS006.vflat_quartic
#print axioms AS006.rM_rescaling_invariant
#print axioms AS006.b_over_a0_rescaling_invariant
#print axioms AS006.collapse_same_x