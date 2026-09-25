import Mathlib

/-!
# I26 — L342's bound-region switch at the Lyman-α forest epoch: the switch variable from the constraint

SCOPE (per lean-math-certification): Lean certifies the MATHEMATICS. Physics inputs are hypotheses: the switch variable
of L342, x = 9 R3/(4K²); the Hamiltonian constraint R3 + K² − K_ijK^ij = 16πGρ; the CMC-stiff foliation K = 3H
(L341 F5), with K_ijK^ij = K²/3 + s, s = σ_ijσ^ij ≥ 0 the shear of the leaves; the flat Friedmann relation
6H² = 16πGρ̄ (ρ, ρ̄ both including Λ, which cancels); Ω_m δ ≡ 8πG(ρ − ρ̄)/(3H²); background Ω_m0 = 0.3138.
Companion lane: `real_research/g03_audit_2026/L346_switch_forest_gate.py`.

* `switch_from_constraint` — x = (3/2) Ω_m δ + 9s/(4K²) exactly.
* `switch_lower_bound` — hence x ≥ (3/2) Ω_m δ (the shear is non-negative): dropping it bounds the switch from below.
  (L342's static-system form 4πGρ_dyn/H² = (3/2)Ω_m(1 + δ) keeps the background density; it agrees for galaxies,
  δ ≫ 1, and overstates x by (3/2)Ω_m at δ of a few.)
* `omega_m_z3_bounds` — at z = 3 with Ω_m0 = 0.3138: 0.9669 < Ω_m(z) < 0.9670.
* `forest_threshold_xc5`, `_xc4`, `_xc7` — at z = 3 the lower bound alone exceeds x_c = 5 (4, 7) wherever
  δ > 3.45 (2.76, 4.83): every matter overdensity of a few switches MOND on.
* `switch_monotone` — a nondecreasing switch of a pointwise-larger variable is at least as large.

Zero `sorry`; axioms ⊆ {propext, Classical.choice, Quot.sound}.
-/

noncomputable section

/-- The switch variable from the Hamiltonian constraint on a CMC leaf with K = 3H. -/
theorem switch_from_constraint {G H ρ ρbar s R3 : ℝ} (hH : H ≠ 0)
    (hcon : R3 + (3 * H) ^ 2 - ((3 * H) ^ 2 / 3 + s) = 16 * Real.pi * G * ρ)
    (hfr : 6 * H ^ 2 = 16 * Real.pi * G * ρbar) :
    9 * R3 / (4 * (3 * H) ^ 2) = 3 / 2 * (8 * Real.pi * G * (ρ - ρbar) / (3 * H ^ 2)) + 9 * s / (4 * (3 * H) ^ 2) := by
  have hR : R3 = 16 * Real.pi * G * (ρ - ρbar) + s := by nlinarith
  rw [hR]
  field_simp
  ring

theorem switch_lower_bound {G H ρ ρbar s R3 : ℝ} (hH : H ≠ 0) (hs : 0 ≤ s)
    (hcon : R3 + (3 * H) ^ 2 - ((3 * H) ^ 2 / 3 + s) = 16 * Real.pi * G * ρ)
    (hfr : 6 * H ^ 2 = 16 * Real.pi * G * ρbar) :
    3 / 2 * (8 * Real.pi * G * (ρ - ρbar) / (3 * H ^ 2)) ≤ 9 * R3 / (4 * (3 * H) ^ 2) := by
  rw [switch_from_constraint hH hcon hfr]
  have : 0 ≤ 9 * s / (4 * (3 * H) ^ 2) := by positivity
  linarith

/-- Ω_m(z) = Ω_m0 (1+z)³ / (Ω_m0 (1+z)³ + 1 − Ω_m0) at z = 3, Ω_m0 = 0.3138. -/
def omz3 : ℝ := 0.3138 * 4 ^ 3 / (0.3138 * 4 ^ 3 + (1 - 0.3138))

theorem omega_m_z3_bounds : 0.9669 < omz3 ∧ omz3 < 0.9670 := by
  unfold omz3; constructor <;> norm_num

theorem forest_threshold_xc5 {δ : ℝ} (h : 3.45 < δ) : 5 < 3 / 2 * omz3 * δ := by
  have ⟨h1, _⟩ := omega_m_z3_bounds
  nlinarith [mul_pos (sub_pos.mpr h1) (sub_pos.mpr h)]

theorem forest_threshold_xc4 {δ : ℝ} (h : 2.76 < δ) : 4 < 3 / 2 * omz3 * δ := by
  have ⟨h1, _⟩ := omega_m_z3_bounds
  nlinarith [mul_pos (sub_pos.mpr h1) (sub_pos.mpr h)]

theorem forest_threshold_xc7 {δ : ℝ} (h : 4.83 < δ) : 7 < 3 / 2 * omz3 * δ := by
  have ⟨h1, _⟩ := omega_m_z3_bounds
  nlinarith [mul_pos (sub_pos.mpr h1) (sub_pos.mpr h)]

/-- A nondecreasing switch applied to a pointwise-larger variable is pointwise at least as large. -/
theorem switch_monotone {ι : Type*} {f : ℝ → ℝ} (hf : Monotone f) {x x' : ι → ℝ} (hx : ∀ i, x i ≤ x' i) :
    ∀ i, f (x i) ≤ f (x' i) := fun i => hf (hx i)

end

#print axioms switch_from_constraint
#print axioms switch_lower_bound
#print axioms omega_m_z3_bounds
#print axioms forest_threshold_xc5
#print axioms forest_threshold_xc4
#print axioms forest_threshold_xc7
#print axioms switch_monotone
