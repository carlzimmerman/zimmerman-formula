import Mathlib

/-!
# I23 — D-YM3 closed class-wide: the Hardy-marginal 1/4 is the Laplacian's Hardy constant

SCOPE. Lean certifies the algebraic and one-variable calculus core of
`real_research/reviews/ym_door_swings_2026_09_22/ym3_hardy/REPORT.md`. The reduction of the
single-scalar action L = Λ⁴f(K) to the log-coordinate shift
  s(u) = ½ (1 − 2 H(u) a_r′(u) / a_r(u)²),   H = u μ(u),   a_r = H′
on the sourceless background (n = 3) was derived symbolically for generic μ in `verify.py`
(sympy, 20/20) and is NOT re-derived here. V = s² + ds/dt, and ds/dt = 0 when s is constant.

* `newtonian_hardy` — μ = 1 in n space dimensions has s = (n−2)/2, so V = ((n−2)/2)², the
  classical Hardy constant; at n = 3 it is 1/4. So "κ = 1/2" is (n−2)/2 at n = 3, a dimension
  count shared by every theory with a Newtonian limit.
* `deep_mond_s_zero` — μ = u (deep MOND) has s = 0, so V = 0 identically.
* `cuscuton_s_half` — μ = A + B/u has s = 1/2, so V = 1/4.
* `s_half_forces_flat_ar` — s = 1/2 with H ≠ 0 and a_r ≠ 0 forces a_r′ = 0.
* `flat_ar_forces_cuscuton` — if a_r = H′ has zero derivative on (0, ∞), then H is affine there,
  i.e. μ = A + B/u: the ONLY actions with s ≡ 1/2 are Newton plus a √K term.
* `cuscuton_not_mond` — such a μ has no deep-MOND regime: μ(u)/u exceeds any bound as u → 0⁺
  (for A, B ≥ 0 not both zero; shown here for B > 0).

Zero `sorry`; axioms ⊆ {propext, Classical.choice, Quot.sound}.
-/

noncomputable section

namespace I23

open Set

/-- The log-coordinate shift for n = 3, as a function of H, a_r, a_r′ at one u. -/
def sShift (H ar ard : ℝ) : ℝ := (1 / 2) * (1 - 2 * H * ard / ar ^ 2)

theorem newtonian_hardy (n : ℝ) :
    ((n - 2) / 2) ^ 2 = (n - 2) ^ 2 / 4 ∧ ((3 : ℝ) - 2) / 2 = 1 / 2 ∧ (((3 : ℝ) - 2) / 2) ^ 2 = 1 / 4 := by
  refine ⟨by ring, by norm_num, by norm_num⟩

/-- μ = 1 (n = 3): H = u, a_r = 1, a_r′ = 0 ⇒ s = 1/2. -/
theorem newtonian_s_half (u : ℝ) : sShift u 1 0 = 1 / 2 := by
  unfold sShift; ring

/-- μ = u: H = u², a_r = 2u, a_r′ = 2 ⇒ s = 0 (u > 0). -/
theorem deep_mond_s_zero (u : ℝ) (hu : 0 < u) : sShift (u ^ 2) (2 * u) 2 = 0 := by
  unfold sShift
  have hu' : u ≠ 0 := hu.ne'
  field_simp
  ring

/-- μ = A + B/u: H = A u + B, a_r = A, a_r′ = 0 ⇒ s = 1/2. -/
theorem cuscuton_s_half (A B u : ℝ) : sShift (A * u + B) A 0 = 1 / 2 := by
  unfold sShift; ring

theorem s_half_forces_flat_ar (H ar ard : ℝ) (hH : H ≠ 0) (har : ar ≠ 0)
    (hs : sShift H ar ard = 1 / 2) : ard = 0 := by
  unfold sShift at hs
  have har2 : ar ^ 2 ≠ 0 := pow_ne_zero 2 har
  have h1 : 2 * H * ard / ar ^ 2 = 0 := by linarith
  rcases (div_eq_zero_iff.mp h1) with h | h
  · rcases mul_eq_zero.mp h with h' | h'
    · rcases mul_eq_zero.mp h' with h'' | h''
      · norm_num at h''
      · exact absurd h'' hH
    · exact h'
  · exact absurd h har2

/-- If H′ = A on (0, ∞), then H(u) = A u + (H 1 − A) there. -/
theorem flat_ar_forces_cuscuton (H : ℝ → ℝ) (A : ℝ) (hd : DifferentiableOn ℝ H (Ioi 0))
    (hc : ∀ u ∈ Ioi (0 : ℝ), deriv H u = A) :
    ∀ u ∈ Ioi (0 : ℝ), H u = A * u + (H 1 - A) := by
  set g : ℝ → ℝ := fun u => H u - A * u with hg
  have hgd : DifferentiableOn ℝ g (Ioi 0) := hd.sub ((differentiable_id.const_mul A).differentiableOn)
  have hg' : EqOn (deriv g) 0 (Ioi 0) := by
    intro u hu
    have hHu : DifferentiableAt ℝ H u := hd.differentiableAt (isOpen_Ioi.mem_nhds hu)
    have : deriv g u = deriv H u - A := by
      have hfun : (fun u => H u - A * u) = H - (fun y => A * y) := by funext y; rfl
      rw [hg, hfun, deriv_sub hHu (by fun_prop : DifferentiableAt ℝ (fun y => A * y) u)]
      simp
    rw [this, hc u hu]
    simp
  intro u hu
  have key := isOpen_Ioi.is_const_of_deriv_eq_zero (convex_Ioi 0).isPreconnected hgd hg' hu
    (show (1 : ℝ) ∈ Ioi 0 by norm_num)
  simp only [hg] at key
  linarith

/-- μ = A + B/u with A ≥ 0, B > 0: for every M > 0 there are arbitrarily small u with
μ(u)/u > M, so μ is never ≈ u (no deep-MOND corner). -/
theorem cuscuton_not_mond (A B M u : ℝ) (hA : 0 ≤ A) (_hB : 0 < B) (hM : 0 < M) (hu : 0 < u)
    (hsmall : u ^ 2 < B / M) : M < (A + B / u) / u := by
  have hu2 : 0 < u ^ 2 := by positivity
  have h1 : M * u ^ 2 < B := by
    rw [lt_div_iff₀ hM] at hsmall; linarith
  rw [lt_div_iff₀ hu]
  have h3 : M * u < B / u := by
    rw [lt_div_iff₀ hu]; nlinarith
  nlinarith

end I23

end

#print axioms I23.newtonian_hardy
#print axioms I23.newtonian_s_half
#print axioms I23.deep_mond_s_zero
#print axioms I23.cuscuton_s_half
#print axioms I23.s_half_forces_flat_ar
#print axioms I23.flat_ar_forces_cuscuton
#print axioms I23.cuscuton_not_mond
