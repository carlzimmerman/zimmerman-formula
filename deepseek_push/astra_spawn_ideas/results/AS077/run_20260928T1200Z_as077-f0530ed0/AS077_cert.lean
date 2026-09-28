import Mathlib
import Mathlib.Tactic

/-
  AS077 -- Finite-shell normalization of the isothermal profile (Lean 4 certificate).

  Framework (FRAMEWORK_CONTRACT): a0 = kappa c sqrt(G rho_Lambda), kappa = 1/2 ADOPTED
  as input; rho = A r^{-2} on the finite shell r_in <= r <= R, r_in > 0 (default
  R <= r_M); M = 4 pi A (R - r_in); C = sqrt(G M_b a0), r_M = sqrt(G M_b/a0).

  Certified contents (all in real algebra; positivity of G, M_b, a0, r_in, R and
  r_in < R are the physical hypotheses):

    T0  sqrt-form amplitude identity:  M_b / r_M = C / G     (as Real.sqrt definitions)
    T1  hypothesis-form amplitude identity: C^2 = G M_b a0 and r_M^2 = G M_b/a0
        imply M_b / r_M = C / G
    T2  the simultaneous-normalization matching condition:
        (M / (R - r_in) = C / G)  <->  (M * r_M = M_b * (R - r_in))
    T3  with M = M_b the equality forces the radius identity:
        (M_b / (R - r_in) = C / G)  <->  (R - r_in = r_M)
    T4  the naive 1/R normalization deficit (exact):
        4 pi * (M / (4 pi R)) * (R - r_in) = M * (1 - r_in / R)
    T5  the deficit is strictly positive for every finite shell (negative control):
        0 < M * r_in / R  given 0 < M, 0 < r_in, 0 < R
    T6  the log-well boundary acceleration: C / r_M = a0
    T7  at finite r_in the shell field at the cap is strictly below the log-well
        value: C * (1 - r_in/R) / R < C / R
    T8  equipartition mass identity: at A = C / (4 pi G), the phantom mass inside
        r_M is M_b exactly: 4 pi A r_M = M_b

  Axiom bar: zero `sorry`; axioms subseteq {propext, Classical.choice, Quot.sound}.
-/

noncomputable section
open Real

namespace AS077

-- definitions in the seed's own sqrt form
def Cdef (G M_b a0 : ℝ) : ℝ := Real.sqrt (G * M_b * a0)
def rMdef (G M_b a0 : ℝ) : ℝ := Real.sqrt (G * M_b / a0)

-- T0: M_b / r_M = C / G from the sqrt definitions (Real.sq_sqrt route)
theorem amp_identity_sqrt (G M_b a0 : ℝ) (hG : 0 < G) (hMb : 0 < M_b) (ha0 : 0 < a0) :
    M_b / rMdef G M_b a0 = Cdef G M_b a0 / G := by
  have h1 : (M_b / rMdef G M_b a0) ^ 2 = (Cdef G M_b a0 / G) ^ 2 := by
    unfold Cdef rMdef
    rw [div_pow, div_pow]
    rw [Real.sq_sqrt (by positivity : 0 ≤ G * M_b * a0)]
    rw [Real.sq_sqrt (by positivity : 0 ≤ G * M_b / a0)]
    field_simp [hG.ne', hMb.ne', ha0.ne']
  have hrMpos : 0 < rMdef G M_b a0 := by
    exact Real.sqrt_pos.2 (by positivity : 0 < G * M_b / a0)
  have hMpos : 0 < M_b / rMdef G M_b a0 := div_pos hMb hrMpos
  have hCpos : 0 < Cdef G M_b a0 / G :=
    div_pos (Real.sqrt_pos.2 (by positivity : 0 < G * M_b * a0)) hG
  rcases (sq_eq_sq_iff_eq_or_eq_neg.mp h1) with h_eq | h_neg
  · exact h_eq
  · have hsum : 0 < M_b / rMdef G M_b a0 + Cdef G M_b a0 / G := add_pos hMpos hCpos
    linarith [h_neg]

-- T1: the same identity from the defining square relations (hypothesis form)
theorem amp_identity_hyp {C G M_b a0 rM : ℝ}
    (hC : C ^ 2 = G * M_b * a0) (hrM : rM ^ 2 = G * M_b / a0)
    (hG : 0 < G) (hMb : 0 < M_b) (ha0 : 0 < a0) (hCpos : 0 < C) (hrMpos : 0 < rM) :
    M_b / rM = C / G := by
  have h1 : (M_b / rM) ^ 2 = (C / G) ^ 2 := by
    rw [div_pow, div_pow, hrM, hC]
    field_simp [hG.ne', (ne_of_gt hrMpos)]
  have hMpos : 0 < M_b / rM := div_pos hMb hrMpos
  have hCGpos : 0 < C / G := div_pos hCpos hG
  rcases (sq_eq_sq_iff_eq_or_eq_neg.mp h1) with h_eq | h_neg
  · exact h_eq
  · have hsum : 0 < M_b / rM + C / G := add_pos hMpos hCGpos
    linarith [h_neg]

-- T2: matching condition of the two normalizations (cross-multiplied form)
theorem amp_equal_iff (M M_b G a0 C rM R r_in : ℝ)
    (hC : C ^ 2 = G * M_b * a0) (hrM : rM ^ 2 = G * M_b / a0)
    (hG : 0 < G) (hMb : 0 < M_b) (ha0 : 0 < a0) (hCpos : 0 < C) (hrMpos : 0 < rM)
    (_hrin : 0 < r_in) (hR : r_in < R) :
    (M / (R - r_in) = C / G) ↔ (M * rM = M_b * (R - r_in)) := by
  have hCG : M_b / rM = C / G := amp_identity_hyp hC hrM hG hMb ha0 hCpos hrMpos
  rw [← hCG]
  have hRne : R - r_in ≠ 0 := by linarith
  have hrMne : rM ≠ 0 := ne_of_gt hrMpos
  field_simp [hRne, hrMne]

-- T3: with M = M_b both normalizations coincide iff R - r_in = r_M
theorem matching_radius_given_Mb (M M_b G a0 C rM R r_in : ℝ)
    (hC : C ^ 2 = G * M_b * a0) (hrM : rM ^ 2 = G * M_b / a0)
    (hM : M = M_b) (hG : 0 < G) (hMb : 0 < M_b) (ha0 : 0 < a0)
    (hCpos : 0 < C) (hrMpos : 0 < rM) (hrin : 0 < r_in) (hR : r_in < R) :
    (M / (R - r_in) = C / G) ↔ (R - r_in = rM) := by
  have hiff := amp_equal_iff M M_b G a0 C rM R r_in hC hrM hG hMb ha0 hCpos hrMpos hrin hR
  rw [hiff, hM]
  constructor
  · intro h
    exact (mul_left_cancel₀ hMb.ne' h).symm
  · intro h
    rw [h]

-- T4: the naive 1/R normalization deficit (exact identity)
theorem deficit_identity {M R r_in : ℝ} (hRne : R ≠ 0) :
    4 * Real.pi * (M / (4 * Real.pi * R)) * (R - r_in) = M * (1 - r_in / R) := by
  field_simp [hRne, Real.pi_ne_zero]

-- T5: the deficit is strictly positive on every finite shell (control positivity)
theorem deficit_pos {M R r_in : ℝ} (hM : 0 < M) (hrin : 0 < r_in)
    (hRpos : 0 < R) : 0 < M * r_in / R := by
  exact div_pos (mul_pos hM hrin) hRpos

-- T6: the log-well boundary acceleration: C / r_M = a0 (AS044-house pattern)
theorem deep_force_at_rM {C G M_b a0 rM : ℝ}
    (hC : C ^ 2 = G * M_b * a0) (hrM : rM ^ 2 = G * M_b / a0)
    (hCpos : 0 < C) (hrMpos : 0 < rM) (ha0 : 0 < a0) : C / rM = a0 := by
  have ha0ne : a0 ≠ 0 := ne_of_gt ha0
  have hrMne : rM ^ 2 ≠ 0 := pow_ne_zero 2 (ne_of_gt hrMpos)
  have hrMmul : rM ^ 2 * a0 = G * M_b := by
    calc
      rM ^ 2 * a0 = (G * M_b / a0) * a0 := by rw [hrM]
      _ = G * M_b := by field_simp [ha0ne]
  have hC2 : C ^ 2 = a0 ^ 2 * rM ^ 2 := by
    nlinarith [hC, hrMmul]
  have hsq : (C / rM) ^ 2 = a0 ^ 2 := by
    rw [div_pow, hC2]
    field_simp [hrMne]
  have hposq : 0 < C / rM := div_pos hCpos hrMpos
  have hprod : (C / rM - a0) * (C / rM + a0) = (C / rM) ^ 2 - a0 ^ 2 := by ring
  have hfac : (C / rM - a0) * (C / rM + a0) = 0 := by
    rw [hprod, hsq]
    ring
  rcases mul_eq_zero.mp hfac with hz | hz
  · linarith [hz]
  · have hgt : 0 < C / rM + a0 := add_pos hposq ha0
    linarith [hz, hgt]

-- T7: at finite r_in the shell field at the cap is strictly below the log-well value
theorem shell_field_below_logwell {C R r_in : ℝ} (hC : 0 < C) (hrin : 0 < r_in)
    (hRpos : 0 < R) (hR : r_in < R) : C * (1 - r_in / R) / R < C / R := by
  have hrlt : r_in / R < 1 := (div_lt_one hRpos).2 hR
  have htp : 0 < r_in / R := div_pos hrin hRpos
  have hlt : C * (1 - r_in / R) < C := by
    nlinarith [htp, hC]
  exact div_lt_div_of_pos_right hlt hRpos

-- T8: equipartition mass identity: at A = C / (4 pi G), 4 pi A r_M = M_b
theorem equipartition_mass {A C G M_b rM : ℝ}
    (hA : A = C / (4 * Real.pi * G)) (hCG : C / G = M_b / rM)
    (hGne : G ≠ 0) (hrMne : rM ≠ 0) : 4 * Real.pi * A * rM = M_b := by
  have h : C * rM = G * M_b := by
    calc
      C * rM = (C / G) * (G * rM) := by field_simp [hGne]
      _ = (M_b / rM) * (G * rM) := by rw [hCG]
      _ = G * M_b := by field_simp [hrMne]
  rw [hA]
  field_simp [hGne, Real.pi_ne_zero]
  ring_nf
  exact h

end AS077
