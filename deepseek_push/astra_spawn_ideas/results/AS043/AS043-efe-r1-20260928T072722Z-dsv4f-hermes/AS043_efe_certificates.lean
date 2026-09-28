/-
AS043 (REDO, authoritative): "Constant acceleration and the external field"
Lean certificates for the EFE (external-field-effect) algebra of the filtered
MONO framework (criterion B, kappa = 1/2 adopted, a0 = (c/2) sqrt(G rho_Lambda)).

Certified statements (all dimensionless; homogeneous in a0, hence valid on both
footings a0 = 9.3619e-11 and 1.1279e-10 m/s^2):

  T1a  (transverse stationarity, first order):
       d/dt sqrt(A + t^2 B) |_{t=0} = 0            (A > 0, B >= 0)
       i.e. |e + t w| with e . w = 0 has NO first-order transverse response.
  T1b  (transverse stationarity, second order):
       d^2/dt^2 sqrt(A + t^2 B) |_{t=0} = B / sqrt A
       i.e. the transverse growth is quadratic with coefficient |w|^2 / |e|.
  T2   (negative control): the scalar-magnitude prescription |e| + t|w| has
       d/dt |_{t=0} = sqrt B /= 0 : a spurious first-order transverse response,
       so the scalar prescription is NOT the vector law (control capable of failing).
  T3   (universal deep anisotropy): for nu(y) = C / sqrt y (the leading deep
       asymptote shared by Q, RAR, EXP, MU2, MONO), the longitudinal-to-transverse
       response ratio of J = nu I + y nu' e e^T is
       1 + y nu'(y) / nu(y) = 1/2  for all y > 0.
  T4ab (anisotropic Jacobian eigenvectors): for a unit vector e (|e| = 1) and
       w perpendicular to e,  J e = (nu + y nu') e  and  J w = nu w,
       J = nu I + (y nu') e e^T, in 2x2 real matrices.
-/
import Mathlib

noncomputable section
open scoped BigOperators

namespace AS043

-- =====================================================================
-- T1: transverse stationarity of the vector norm
-- f(t) = sqrt (A + t^2 B), A > 0, B >= 0   (geometry: |e + t w|^2 = |e|^2 + t^2 |w|^2
-- when e . w = 0, with A = |e|^2, B = |w|^2)
-- =====================================================================

variable {A B : ℝ}

lemma has_deriv_sqrt_argument (hA : 0 < A) (hB : 0 ≤ B) :
    ∀ t : ℝ, HasDerivAt (fun s : ℝ => A + s ^ 2 * B) (2 * t * B) t := by
  intro t
  have ht : HasDerivAt (fun s : ℝ => s ^ 2) (2 * t) t := by
    simpa [pow_one] using (hasDerivAt_pow 2 t)
  have hm : HasDerivAt (fun s : ℝ => s ^ 2 * B) (2 * t * B) t := ht.mul_const B
  simpa [add_comm] using hm.add_const A

lemma arg_pos (hA : 0 < A) (hB : 0 ≤ B) (t : ℝ) : 0 < A + t ^ 2 * B := by
  nlinarith [hA, hB, sq_nonneg t]

lemma has_deriv_f (hA : 0 < A) (hB : 0 ≤ B) (t : ℝ) :
    HasDerivAt (fun s : ℝ => Real.sqrt (A + s ^ 2 * B))
      (t * B / Real.sqrt (A + t ^ 2 * B)) t := by
  have hg := has_deriv_sqrt_argument hA hB t
  have hsq : HasDerivAt (fun s : ℝ => Real.sqrt (A + s ^ 2 * B))
      ((2 * t * B) / (2 * Real.sqrt (A + t ^ 2 * B))) t := by
    simpa using hg.sqrt (ne_of_gt (arg_pos hA hB t))
  have hval : (2 * t * B) / (2 * Real.sqrt (A + t ^ 2 * B))
      = t * B / Real.sqrt (A + t ^ 2 * B) := by
    field_simp [ne_of_gt (arg_pos hA hB t)]
  simpa [hval] using hsq

theorem transverse_stationarity_first_deriv (hA : 0 < A) (hB : 0 ≤ B) :
    deriv (fun s : ℝ => Real.sqrt (A + s ^ 2 * B)) 0 = 0 := by
  have hv : 0 * B / Real.sqrt (A + 0 ^ 2 * B) = 0 := by ring
  have h0 : HasDerivAt (fun s : ℝ => Real.sqrt (A + s ^ 2 * B)) 0 0 := by
    simpa [hv] using has_deriv_f hA hB 0
  simpa using h0.deriv

lemma deriv_f_eq (hA : 0 < A) (hB : 0 ≤ B) (t : ℝ) :
    deriv (fun s : ℝ => Real.sqrt (A + s ^ 2 * B)) t
      = t * B / Real.sqrt (A + t ^ 2 * B) := by
  simpa using (has_deriv_f hA hB t).deriv

lemma has_deriv_second (hA : 0 < A) (hB : 0 ≤ B) :
    HasDerivAt (fun t : ℝ => t * B / Real.sqrt (A + t ^ 2 * B))
      (B / Real.sqrt A) 0 := by
  have htb : HasDerivAt (fun t : ℝ => t * B) B 0 := by
    simpa [mul_comm] using (hasDerivAt_id 0).const_mul B
  have hg0 : HasDerivAt (fun s : ℝ => A + s ^ 2 * B) 0 0 := by
    simpa using has_deriv_sqrt_argument hA hB 0
  have hden : HasDerivAt (fun t : ℝ => Real.sqrt (A + t ^ 2 * B)) 0 0 := by
    have h := hg0.sqrt (ne_of_gt (arg_pos hA hB 0))
    have hv : (0 : ℝ) / (2 * Real.sqrt (A + 0 ^ 2 * B)) = 0 := by ring
    simpa [hv] using h
  have hden0 : Real.sqrt (A + 0 ^ 2 * B) ≠ 0 :=
    ne_of_gt (Real.sqrt_pos.2 (arg_pos hA hB 0))
  have hd : HasDerivAt (fun t : ℝ => (t * B) / Real.sqrt (A + t ^ 2 * B))
      ((B * Real.sqrt (A + 0 ^ 2 * B) - (0 * B) * 0) / (Real.sqrt (A + 0 ^ 2 * B)) ^ 2) 0 :=
    htb.div hden hden0
  have hv' : (B * Real.sqrt (A + 0 ^ 2 * B) - (0 * B) * 0) / (Real.sqrt (A + 0 ^ 2 * B)) ^ 2
      = B / Real.sqrt A := by
    have hpos : Real.sqrt A ≠ 0 := ne_of_gt (Real.sqrt_pos.2 hA)
    have hsq : (Real.sqrt A) * (Real.sqrt A) = A := Real.mul_self_sqrt (le_of_lt hA)
    have hz : A + 0 ^ 2 * B = A := by ring
    have harg : Real.sqrt (A + 0 ^ 2 * B) = Real.sqrt A := by rw [hz]
    have hz' : A + B * (0 : ℝ) ^ 2 = A := by ring
    have harg' : Real.sqrt (A + B * (0 : ℝ) ^ 2) = Real.sqrt A := by rw [hz']
    have hpos' : Real.sqrt (A + 0 ^ 2 * B) ≠ 0 := by rw [harg]; exact hpos
    field_simp [hpos', hsq, harg, harg', pow_two]
    ring_nf
  rw [hv'] at hd
  exact hd

theorem transverse_stationarity_second_deriv (hA : 0 < A) (hB : 0 ≤ B) :
    deriv (fun t : ℝ => deriv (fun s : ℝ => Real.sqrt (A + s ^ 2 * B)) t) 0
      = B / Real.sqrt A := by
  have hfeq : (fun t : ℝ => deriv (fun s : ℝ => Real.sqrt (A + s ^ 2 * B)) t)
      = fun t : ℝ => t * B / Real.sqrt (A + t ^ 2 * B) := by
    funext t
    exact deriv_f_eq hA hB t
  rw [hfeq]
  exact (has_deriv_second hA hB).deriv

-- =====================================================================
-- T2: negative control - scalar-magnitude prescription has a first-order
-- transverse response  d/dt (sqrt A + t * sqrt B) |_0 = sqrt B /= 0
-- =====================================================================

theorem scalar_prescription_first_deriv (hB : 0 < B) :
    deriv (fun t : ℝ => Real.sqrt A + t * Real.sqrt B) 0 = Real.sqrt B := by
  have htb : HasDerivAt (fun t : ℝ => t * Real.sqrt B) (Real.sqrt B) 0 := by
    simpa [mul_comm] using (hasDerivAt_id 0).const_mul (Real.sqrt B)
  have h : HasDerivAt (fun t : ℝ => t * Real.sqrt B + Real.sqrt A) (Real.sqrt B) 0 :=
    htb.add_const (Real.sqrt A)
  simpa [add_comm] using h.deriv

theorem scalar_prescription_first_deriv_nonzero (hB : 0 < B) :
    deriv (fun t : ℝ => Real.sqrt A + t * Real.sqrt B) 0 ≠ 0 := by
  rw [scalar_prescription_first_deriv hB]
  exact ne_of_gt (Real.sqrt_pos.2 hB)

-- =====================================================================
-- T3: universal deep anisotropy ratio for the shared leading asymptote
-- nu(y) = C / sqrt y ,  y > 0 :  1 + y nu'(y)/nu(y) = 1/2
-- =====================================================================

variable {C y : ℝ}

lemma has_deriv_nuPow (hy : 0 < y) :
    HasDerivAt (fun x : ℝ => C / Real.sqrt x)
      (C * (-(1 / (2 * Real.sqrt y)) / (Real.sqrt y) ^ 2)) y := by
  have hs : HasDerivAt (fun x : ℝ => Real.sqrt x) (1 / (2 * Real.sqrt y)) y :=
    Real.hasDerivAt_sqrt (ne_of_gt hy)
  have hinv : HasDerivAt (fun x : ℝ => (Real.sqrt x)⁻¹)
      (-(1 / (2 * Real.sqrt y)) / (Real.sqrt y) ^ 2) y :=
    hs.inv (ne_of_gt (Real.sqrt_pos.2 hy))
  have hc : HasDerivAt (fun x : ℝ => C * (Real.sqrt x)⁻¹)
      (C * (-(1 / (2 * Real.sqrt y)) / (Real.sqrt y) ^ 2)) y :=
    hinv.const_mul C
  exact hc

lemma deriv_nuPow_eq (hy : 0 < y) :
    deriv (fun x : ℝ => C / Real.sqrt x) y
      = C * (-(1 / (2 * Real.sqrt y)) / (Real.sqrt y) ^ 2) := by
  simpa using (has_deriv_nuPow hy).deriv

theorem powerlaw_anisotropy_ratio (hy : 0 < y) (hC : C ≠ 0) :
    1 + y * deriv (fun x : ℝ => C / Real.sqrt x) y / (C / Real.sqrt y) = 1 / 2 := by
  rw [deriv_nuPow_eq hy]
  have hs : Real.sqrt y ≠ 0 := ne_of_gt (Real.sqrt_pos.2 hy)
  have hsq : (Real.sqrt y) * (Real.sqrt y) = y := Real.mul_self_sqrt (le_of_lt hy)
  field_simp [hs, hsq, hy.ne', hC]
  rw [pow_two]
  rw [hsq]
  ring

-- =====================================================================
-- T4: anisotropic Jacobian eigenvectors
-- J = nu*I + (y nu') e e^T  applied to a vector v is
--   (J v)_i = nu v_i + (y nu') e_i (e . v)   (componentwise in 2D).
-- |e| = 1 :  J e = (nu + y nu') e ;   e . w = 0 :  J w = nu w .
-- =====================================================================

variable (nu : ℝ) (ynuprime : ℝ)

def Jvec (nu ynuprime : ℝ) (e : Fin 2 → ℝ) (v : Fin 2 → ℝ) : Fin 2 → ℝ :=
  fun i => nu * v i + ynuprime * e i * (e 0 * v 0 + e 1 * v 1)

lemma jacobian_par_eigenvector (nu ynuprime a b : ℝ) (hn : a ^ 2 + b ^ 2 = 1) :
    Jvec nu ynuprime ![a, b] ![a, b] = (nu + ynuprime) • ![a, b] := by
  ext i
  fin_cases i <;> simp [Jvec]
  · have hne : a * a + b * b = 1 := by simpa [pow_two] using hn
    rw [hne]
    ring
  · have hne : a * a + b * b = 1 := by simpa [pow_two] using hn
    rw [hne]
    ring

lemma jacobian_perp_eigenvector (nu ynuprime a b c d : ℝ) (hp : a * c + b * d = 0) :
    Jvec nu ynuprime ![a, b] ![c, d] = nu • ![c, d] := by
  ext i
  fin_cases i <;> simp [Jvec]
  · right
    rw [hp]
  · right
    rw [hp]

end AS043