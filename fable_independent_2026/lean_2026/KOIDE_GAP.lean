import Mathlib

/-!
# KOIDE_GAP -- the gap-equation door (criteria frozen in KOIDE_GAP_CRITERIA.md, commit f105cb99d)

Self-consistent mean-field ring: s_k = g F(s_k) + h · mean_l F(s_l), √m_k = |s_k|.  The numeric 12-ratio scan
is in scratch (gap.py); this file certifies the structure that decides what any such gap equation can do.

CERTIFIED:
(G1) `koide_iff_e1_e2`: for a √-mass triple with nonzero sum, Q = 2/3 ⇔ e1² = 6 e2.
(G2) `vieta3` + `cubic_gap_koide`: if the √-masses are the three roots of x³ - b x² + p x - C, then b = e1,
     p = e2, so Koide ⇔ b² = 6p.  A polynomial gap condition gives Koide only through a RELATION BETWEEN ITS
     COUPLINGS; nothing in the gap structure supplies it.
(G3) `u3_gap_equal_squares` + `two_level_Q`: with the flavour-singlet coupling off (h = 0) and an injective
     loop function, every nonzero s_k obeys g I(s_k²) = 1, so all nonzero s_k² are equal; a spectrum with
     |s_k| ∈ {0, m} has Q ∈ {1, 1/2, 1/3}, never 2/3.  The U(3)-symmetric gap equation cannot give Koide.
NOT CERTIFIED (numeric, KOIDE_GAP_scan.py/.out): fitted to m_μ/m_e, Q reaches 2/3 only at strong coupling with
h/g ≈ -1.505 (I4, g ≈ 48) vs ≈ -2.885 (I3, g ≈ 32): not in the declared set, different per loop, masses far above
the cutoff. VERDICT per frozen criteria: KILL.
-/

namespace KoideGap

theorem koide_iff_e1_e2 (s1 s2 s3 : ℝ) (h : s1 + s2 + s3 ≠ 0) :
    (s1 ^ 2 + s2 ^ 2 + s3 ^ 2) / (s1 + s2 + s3) ^ 2 = 2 / 3 ↔
      (s1 + s2 + s3) ^ 2 = 6 * (s1 * s2 + s2 * s3 + s3 * s1) := by
  have hp : (s1 + s2 + s3) ^ 2 ≠ 0 := pow_ne_zero 2 h
  rw [div_eq_iff hp]
  constructor <;> intro hq <;> nlinarith [hq]

theorem vieta3 (b p C s1 s2 s3 : ℝ)
    (h : ∀ x : ℝ, x ^ 3 - b * x ^ 2 + p * x - C = (x - s1) * (x - s2) * (x - s3)) :
    b = s1 + s2 + s3 ∧ p = s1 * s2 + s2 * s3 + s3 * s1 ∧ C = s1 * s2 * s3 := by
  have h0 := h 0
  have h1 := h 1
  have hm := h (-1)
  ring_nf at h0 h1 hm
  refine ⟨?_, ?_, ?_⟩ <;> nlinarith [h0, h1, hm]

theorem cubic_gap_koide (b p C s1 s2 s3 : ℝ)
    (h : ∀ x : ℝ, x ^ 3 - b * x ^ 2 + p * x - C = (x - s1) * (x - s2) * (x - s3))
    (hs : s1 + s2 + s3 ≠ 0) :
    (s1 ^ 2 + s2 ^ 2 + s3 ^ 2) / (s1 + s2 + s3) ^ 2 = 2 / 3 ↔ b ^ 2 = 6 * p := by
  obtain ⟨hb, hp, -⟩ := vieta3 b p C s1 s2 s3 h
  rw [koide_iff_e1_e2 s1 s2 s3 hs, hb, hp]

theorem u3_gap_equal_squares (I : ℝ → ℝ) (hI : Function.Injective I) (g x y : ℝ)
    (hx : g * I (x ^ 2) = 1) (hy : g * I (y ^ 2) = 1) : x ^ 2 = y ^ 2 := by
  have hg : g ≠ 0 := by rintro rfl; simp at hx
  apply hI
  have : g * I (x ^ 2) = g * I (y ^ 2) := by rw [hx, hy]
  exact mul_left_cancel₀ hg this

theorem two_level_Q (m a1 a2 a3 : ℝ) (hm : 0 < m)
    (h1 : a1 = 0 ∨ a1 = m) (h2 : a2 = 0 ∨ a2 = m) (h3 : a3 = 0 ∨ a3 = m)
    (hne : a1 + a2 + a3 ≠ 0) :
    (a1 ^ 2 + a2 ^ 2 + a3 ^ 2) / (a1 + a2 + a3) ^ 2 ≠ 2 / 3 := by
  intro hq
  rw [div_eq_iff (pow_ne_zero 2 hne)] at hq
  rcases h1 with rfl | rfl <;> rcases h2 with rfl | rfl <;> rcases h3 with rfl | rfl <;>
    first
    | nlinarith [sq_pos_of_pos hm, hq]
    | simp at hne

end KoideGap

#print axioms KoideGap.koide_iff_e1_e2
#print axioms KoideGap.vieta3
#print axioms KoideGap.cubic_gap_koide
#print axioms KoideGap.u3_gap_equal_squares
#print axioms KoideGap.two_level_Q
