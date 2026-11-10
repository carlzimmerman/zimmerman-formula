/-
CLS1 MUTATE twin (criteria 0a30eac556): one false version of each CLS1.lean statement. Every one must fail to compile.
TEST lane; adopts nothing. kappa = 1/2 FITTED; not theory closed.
  M1 contrast reversed (u < l E)
  M2 up_bound with the inequality reversed (s <= ...)
  M3 up_log with u and l swapped (exp D (1 + a u s) <= 1 + a l s)
  M4 low_bound reversed (s >= ...)
  M5 window non-empty claimed as forced (exists s between with B < A)
  M6 cold core claimed to pass
-/
import Mathlib.Tactic

namespace CLS1M

theorem m1 (E a s u l : ℝ) (hE : 1 < E) (ha : 0 < a) (hs : 0 < s) (hl : 0 < l)
    (h : E * (1 + a * l * s) ≤ 1 + a * u * s) : u < l * E := by
  nlinarith

theorem m2 (E a s u l : ℝ) (hE : 1 < E) (ha : 0 < a) (hs : 0 < s) (hl : 0 < l)
    (h : E * (1 + a * l * s) ≤ 1 + a * u * s) : s ≤ (E - 1) / (a * (u - l * E)) := by
  nlinarith

theorem m3 (D a s u l : ℝ) (ha : 0 < a) (hs : 0 < s) (hu : 0 < u) (hl : 0 < l)
    (h : D ≤ Real.log ((1 + a * u * s) / (1 + a * l * s))) :
    Real.exp D * (1 + a * u * s) ≤ 1 + a * l * s := by
  nlinarith [Real.add_one_le_exp D]

theorem m4 (E a s u l : ℝ) (hE : 1 < E) (ha : 0 < a) (hs : 0 < s)
    (hlu : u * E < l) (h : 1 + a * l * s ≤ E * (1 + a * u * s)) : (E - 1) / (a * (l - u * E)) ≤ s := by
  nlinarith

theorem m5 (A B : ℝ) (hAB : B < A) : ∃ s : ℝ, A ≤ s ∧ s ≤ B := by
  exact ⟨A, le_refl A, by linarith⟩

theorem m6 (E a s u l : ℝ) (hE : 1 < E) (ha : 0 < a) (hs : 0 < s) (hl : 0 ≤ l)
    (hsmall : a * s * u < E - 1) : E * (1 + a * l * s) ≤ 1 + a * u * s := by
  nlinarith

end CLS1M

-- Adopts nothing. kappa = 1/2 FITTED; not theory closed.
