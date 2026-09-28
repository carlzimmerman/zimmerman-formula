import Mathlib

/-!
# AS025 — Dimensional closure of a proposed new coefficient (certificate)

Audited object (framework base, README key equations; FRAMEWORK_CONTRACT
"Mandatory scale and units"):

    a0(A, c, G, rho) := A * c * sqrt(G * rho)

i.e. the general monomial a = A * c^p * G^q * rho^r with acceleration
dimensions, after the dimensional exponent system has been solved
(p, q, r) = (1, 1/2, 1/2)  (solved exactly in compute_AS025_dimensional_closure.py;
det = -2, unique solution, no exponent freedom left).  What remains is the
dimensionless coefficient A, and the framework adopts A = kappa = 1/2.

What is certified here (real arithmetic, positivity domain):

1. `a0_inverse_exact` — the scale relation is an exact bijection:
   inverting a0 = A * c * sqrt(G * rho) for rho and substituting back
   reproduces a0 exactly:
       a0 A c G (a^2 / (A^2 * G * c^2)) = a
   Hence A is exactly the single remaining degree of freedom: no hidden
   dimensionful coefficient or correction is needed to close the identity.

2. `a0_unique_multiplier` — different dimensionless A give different
   accelerations: a0 A1 = a0 A2 implies A1 = A2 (positivity domain).
   A is an observable parameter, not a relabeling; dimensional analysis does
   not fix it (any A > 0 is admitted by the theorem), consistent with
   kappa = 1/2 being an ADOPTED input.

3. `a0_A_ratio_is_A_ratio` — the dimensionless footing-independent ratio:
       a0(A2) / a0(A1) = A2 / A1
   independent of c, G, rho; this is how the single dimensionless statement
   applies to both registered footings (canonical 9.3619e-11 and alternative
   1.1279e-10 m/s^2): the footings enter only through their densities, the
   A-ratio is pure A.

4. `footing_density_ratio` — at fixed A:  a0(rho2)/a0(rho1) = sqrt(rho2/rho1).

5. `vflat4_ratio_is_A_ratio` — the deep-MOND law v_flat^4 = G*M*a0 scales
   linearly with A:  (G*M*a0 A2) / (G*M*a0 A1) = A2/A1.

6. `vflat_ratio_is_fourth_root_A_ratio` — v_flat(A) = sqrt(sqrt(G*M*a0(A))):
       v_flat(A2) / v_flat(A1) = sqrt(sqrt(A2 / A1))
   (the (1/4)-power scaling of the flat speed in the coefficient A).

These certify the algebra of the coefficient freedom only.  They do not
derive A = 1/2 (dimensional analysis cannot), do not identify which physical
density enters rho_L (the footing choice), and establish nothing about the
dynamics (branches Q, RAR, MU2, EXP, MONO are untouched).
-/

open Real

noncomputable def a0 (A c G rho : ℝ) : ℝ :=
  A * c * Real.sqrt (G * rho)

/-- Inverting a0 = A*c*sqrt(G*rho) for rho and substituting back reproduces
    a0 exactly:  a0 A c G (a^2/(A^2*G*c^2)) = a.  A is exactly the one free
    dimensionless coefficient; nothing is lost or added by the closure. -/
theorem a0_inverse_exact {A c G a : ℝ}
    (hA : 0 < A) (hc : 0 < c) (hG : 0 < G) (ha : 0 < a) :
    a0 A c G (a ^ 2 / (A ^ 2 * G * c ^ 2)) = a := by
  unfold a0
  have hinner : G * (a ^ 2 / (A ^ 2 * G * c ^ 2)) = a ^ 2 / (A ^ 2 * c ^ 2) := by
    field_simp [ne_of_gt hA, ne_of_gt hc, ne_of_gt hG]
  have hnum : 0 ≤ a ^ 2 := sq_nonneg a
  have hsq_a : Real.sqrt (a ^ 2) = a := by
    rw [Real.sqrt_sq_eq_abs]
    exact abs_of_pos ha
  have hsq_A : Real.sqrt (A ^ 2) = A := by
    rw [Real.sqrt_sq_eq_abs]
    exact abs_of_pos hA
  have hsq_c : Real.sqrt (c ^ 2) = c := by
    rw [Real.sqrt_sq_eq_abs]
    exact abs_of_pos hc
  have hsq_Ac : Real.sqrt (A ^ 2 * c ^ 2) = A * c := by
    rw [Real.sqrt_mul (sq_nonneg A) (c ^ 2)]
    rw [hsq_A, hsq_c]
  have hmain : Real.sqrt (G * (a ^ 2 / (A ^ 2 * G * c ^ 2))) = a / (A * c) := by
    rw [hinner]
    rw [Real.sqrt_div hnum (A ^ 2 * c ^ 2)]
    rw [hsq_a, hsq_Ac]
  calc
    A * c * Real.sqrt (G * (a ^ 2 / (A ^ 2 * G * c ^ 2))) = A * c * (a / (A * c)) := by
      rw [hmain]
    _ = a := by
      field_simp [ne_of_gt hA, ne_of_gt hc]

/-- The multiplier A is uniquely recoverable from the acceleration it
    produces:  a0 A1 = a0 A2  =>  A1 = A2.  Dimensional analysis admits every
    A > 0 (any positive A gives an acceleration monomial), so A is a free
    parameter with observable content — it is NOT fixed by dimensions. -/
theorem a0_unique_multiplier {A1 A2 c G rho : ℝ}
    (hc : 0 < c) (hG : 0 < G) (hrho : 0 < rho)
    (h : a0 A1 c G rho = a0 A2 c G rho) : A1 = A2 := by
  unfold a0 at h
  have hss : Real.sqrt (G * rho) ≠ 0 := ne_of_gt (Real.sqrt_pos.2 (mul_pos hG hrho))
  have hc0 : c ≠ 0 := ne_of_gt hc
  have h1 : A1 * c = A2 * c := mul_right_cancel₀ hss h
  exact mul_right_cancel₀ hc0 h1

/-- Dimensionless, footing-independent ratio of scales:
    a0(A2) / a0(A1) = A2 / A1, independent of c, G, rho.  This is the
    statement that carries the A-freedom to both registered footings. -/
theorem a0_A_ratio_is_A_ratio {A1 A2 c G rho : ℝ}
    (hA1 : 0 < A1) (hA2 : 0 < A2) (hc : 0 < c) (hG : 0 < G) (hrho : 0 < rho) :
    a0 A2 c G rho / a0 A1 c G rho = A2 / A1 := by
  unfold a0
  have hA1nz : A1 ≠ 0 := ne_of_gt hA1
  have hc0 : c ≠ 0 := ne_of_gt hc
  have hss : Real.sqrt (G * rho) ≠ 0 := ne_of_gt (Real.sqrt_pos.2 (mul_pos hG hrho))
  field_simp [hA1nz, hc0, hss]

/-- At fixed A the footing ratio is the square root of the density ratio
    (both registered footings carry A = 1/2 separately, with their own rho). -/
theorem footing_density_ratio {A c G rho1 rho2 : ℝ}
    (hA : 0 < A) (hc : 0 < c) (hG : 0 < G) (hr1 : 0 < rho1) (hr2 : 0 < rho2) :
    a0 A c G rho2 / a0 A c G rho1 = Real.sqrt (rho2 / rho1) := by
  unfold a0
  have hkc : A * c ≠ 0 := ne_of_gt (mul_pos hA hc)
  have hG1p : 0 < G * rho1 := mul_pos hG hr1
  have hG2 : 0 ≤ G * rho2 := le_of_lt (mul_pos hG hr2)
  have hs1 : Real.sqrt (G * rho1) ≠ 0 := by
    exact ne_of_gt (Real.sqrt_pos.2 hG1p)
  have hratio : (G * rho2) / (G * rho1) = rho2 / rho1 := by
    field_simp [ne_of_gt hG, ne_of_gt hr1]
  have hmain : Real.sqrt (G * rho2) / Real.sqrt (G * rho1) = Real.sqrt (rho2 / rho1) := by
    rw [← Real.sqrt_div hG2 (G * rho1)]
    rw [hratio]
  calc
    A * c * Real.sqrt (G * rho2) / (A * c * Real.sqrt (G * rho1))
        = Real.sqrt (G * rho2) / Real.sqrt (G * rho1) := by
          field_simp [hkc, hs1]
    _ = Real.sqrt (rho2 / rho1) := hmain

/-- Deep-MOND law: v_flat^4 = G*M*a0 scales linearly in the coefficient A:
    (G*M*a0(A2)) / (G*M*a0(A1)) = A2/A1. -/
theorem vflat4_ratio_is_A_ratio {A1 A2 c G M rho : ℝ}
    (hA1 : 0 < A1) (hA2 : 0 < A2) (hc : 0 < c) (hG : 0 < G) (hM : 0 < M) (hrho : 0 < rho) :
    G * M * a0 A2 c G rho / (G * M * a0 A1 c G rho) = A2 / A1 := by
  unfold a0
  have hA1nz : A1 ≠ 0 := ne_of_gt hA1
  have hc0 : c ≠ 0 := ne_of_gt hc
  have hM0 : M ≠ 0 := ne_of_gt hM
  have hG0 : G ≠ 0 := ne_of_gt hG
  have hss : Real.sqrt (G * rho) ≠ 0 := ne_of_gt (Real.sqrt_pos.2 (mul_pos hG hrho))
  field_simp [hA1nz, hc0, hM0, hG0, hss]

/-- Flat speed scaling: v_flat(A) = sqrt(sqrt(G*M*a0(A))) gives
    v_flat(A2) / v_flat(A1) = sqrt(sqrt(A2/A1)), i.e. v_flat ∝ A^(1/4). -/
theorem vflat_ratio_is_fourth_root_A_ratio {A1 A2 c G M rho : ℝ}
    (hA1 : 0 < A1) (hA2 : 0 < A2) (hc : 0 < c) (hG : 0 < G) (hM : 0 < M) (hrho : 0 < rho) :
    Real.sqrt (Real.sqrt (G * M * a0 A2 c G rho)) /
      Real.sqrt (Real.sqrt (G * M * a0 A1 c G rho)) = Real.sqrt (Real.sqrt (A2 / A1)) := by
  unfold a0
  let ss : ℝ := Real.sqrt (G * rho)
  have hssp : 0 < ss := by
    unfold ss
    exact Real.sqrt_pos.2 (mul_pos hG hrho)
  let x1 : ℝ := G * M * (A1 * c * ss)
  let x2 : ℝ := G * M * (A2 * c * ss)
  have hx1p : 0 < x1 := by
    unfold x1
    exact mul_pos (mul_pos hG hM) (mul_pos (mul_pos hA1 hc) hssp)
  have hx2p : 0 < x2 := by
    unfold x2
    exact mul_pos (mul_pos hG hM) (mul_pos (mul_pos hA2 hc) hssp)
  have h1 : Real.sqrt x2 / Real.sqrt x1 = Real.sqrt (x2 / x1) := by
    rw [← Real.sqrt_div (le_of_lt hx2p) x1]
  have h2 : Real.sqrt (Real.sqrt x2) / Real.sqrt (Real.sqrt x1) =
            Real.sqrt (Real.sqrt x2 / Real.sqrt x1) := by
    rw [← Real.sqrt_div (le_of_lt (Real.sqrt_pos.2 hx2p)) (Real.sqrt x1)]
  have hxratio : x2 / x1 = A2 / A1 := by
    unfold x1 x2
    have hssnz : ss ≠ 0 := ne_of_gt hssp
    field_simp [ne_of_gt hA1, ne_of_gt hA2, ne_of_gt hc, ne_of_gt hG, ne_of_gt hM, hssnz]
  calc
    Real.sqrt (Real.sqrt (G * M * (A2 * c * ss))) /
        Real.sqrt (Real.sqrt (G * M * (A1 * c * ss)))
        = Real.sqrt (Real.sqrt x2) / Real.sqrt (Real.sqrt x1) := by rfl
    _ = Real.sqrt (Real.sqrt x2 / Real.sqrt x1) := h2
    _ = Real.sqrt (Real.sqrt (x2 / x1)) := by rw [h1]
    _ = Real.sqrt (Real.sqrt (A2 / A1)) := by rw [hxratio]

#print axioms a0_inverse_exact
#print axioms a0_unique_multiplier
#print axioms a0_A_ratio_is_A_ratio
#print axioms footing_density_ratio
#print axioms vflat4_ratio_is_A_ratio
#print axioms vflat_ratio_is_fourth_root_A_ratio
