/-
CLS1 (criteria 0a30eac556): Lean statements for the window algebra of the two necessary conditions.
They certify the algebra, not the physics or the data. TEST lane; adopts nothing. kappa = 1/2 FITTED; not theory closed.

Notation: s = 1/mu_K^2 > 0, alpha > 0 (x = alpha n s, leading order), E = exp(D/c^2) > 1.

  up_needs_contrast : E (1 + alpha l s) <= 1 + alpha u s  ->  l E < u
                      (the cold bound can be met at all only if the density contrast beats E).
  up_bound          : and then s >= (E - 1) / (alpha (u - l E))   (i.e. mu_K <= mu_hi).
  up_log            : log((1 + alpha u s)/(1 + alpha l s)) >= D  ->  exp D (1 + alpha l s) <= 1 + alpha u s.
  low_bound         : 1 + alpha l s <= E (1 + alpha u s), u E < l  ->  s <= (E - 1) / (alpha (l - u E))
                      (the stiff bound: mu_K >= mu_lo).
  window_empty      : s >= A and s <= B with B < A is impossible (a lower edge above an upper edge empties W).
  cold_core_fails   : with u <= U, l >= 0, alpha s u < D' where D' = E - 1, the cold bound fails
                      (at large mu_K the allowed span alpha s u is below the required E - 1).
-/
import Mathlib.Tactic

namespace CLS1

theorem up_needs_contrast (E a s u l : ℝ) (hE : 1 < E) (ha : 0 < a) (hs : 0 < s) (hl : 0 < l)
    (h : E * (1 + a * l * s) ≤ 1 + a * u * s) : l * E < u := by
  by_contra hc
  push_neg at hc
  have h1 : a * u * s ≤ a * (l * E) * s := by
    have := mul_le_mul_of_nonneg_left hc (le_of_lt (mul_pos ha hs))
    nlinarith [this]
  nlinarith [mul_pos (mul_pos ha hl) hs]

theorem up_bound (E a s u l : ℝ) (hE : 1 < E) (ha : 0 < a) (hs : 0 < s) (hl : 0 < l)
    (h : E * (1 + a * l * s) ≤ 1 + a * u * s) : (E - 1) / (a * (u - l * E)) ≤ s := by
  have hc := up_needs_contrast E a s u l hE ha hs hl h
  have hd : 0 < a * (u - l * E) := mul_pos ha (by linarith)
  rw [div_le_iff₀ hd]
  nlinarith

theorem up_log (D a s u l : ℝ) (ha : 0 < a) (hs : 0 < s) (hu : 0 < u) (hl : 0 < l)
    (h : D ≤ Real.log ((1 + a * u * s) / (1 + a * l * s))) :
    Real.exp D * (1 + a * l * s) ≤ 1 + a * u * s := by
  have hpl : 0 < 1 + a * l * s := by positivity
  have hpu : 0 < 1 + a * u * s := by positivity
  have hq : 0 < (1 + a * u * s) / (1 + a * l * s) := div_pos hpu hpl
  have h2 : Real.exp D ≤ (1 + a * u * s) / (1 + a * l * s) := by
    calc Real.exp D ≤ Real.exp (Real.log ((1 + a * u * s) / (1 + a * l * s))) := Real.exp_le_exp.mpr h
      _ = _ := Real.exp_log hq
  rwa [le_div_iff₀ hpl] at h2

theorem low_bound (E a s u l : ℝ) (hE : 1 < E) (ha : 0 < a) (hs : 0 < s)
    (hlu : u * E < l) (h : 1 + a * l * s ≤ E * (1 + a * u * s)) : s ≤ (E - 1) / (a * (l - u * E)) := by
  have hd : 0 < a * (l - u * E) := mul_pos ha (by linarith)
  rw [le_div_iff₀ hd]
  nlinarith

theorem window_empty (s A B : ℝ) (hAB : B < A) (h1 : A ≤ s) (h2 : s ≤ B) : False := by
  linarith

theorem cold_core_fails (E a s u l : ℝ) (hE : 1 < E) (ha : 0 < a) (hs : 0 < s) (hl : 0 ≤ l)
    (hsmall : a * s * u < E - 1) : ¬ (E * (1 + a * l * s) ≤ 1 + a * u * s) := by
  intro h
  have : 0 ≤ E * (a * l * s) := by positivity
  nlinarith

end CLS1

-- Adopts nothing. kappa = 1/2 FITTED; not theory closed.
