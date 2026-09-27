import Mathlib

/-!
# FL3 — the dark fluid's swirl and the clock: the algebra behind the lane

SCOPE. `real_research/dark_fluid_2026/FL3_swirl_and_the_clock.py` checks a rotating halo's vortex lattice against the
khronon. The lane computes the lattice, the linear K on a sheared metric and the loop integrals. Lean certifies the
algebra they rest on.

* `cross_energy_core_scaling`: near a unit vortex of ψ_H, a + ib = ψ_H ψ_L* is r times a bounded factor, so the gated
  energy 6a² + 2b² is r² times a bounded factor. It vanishes as r², never with a spike.
* `cross_energy_pos_off_core`: that r² coefficient is positive whenever ψ_L ≠ 0 at the core.
* `feynman_rule`: one circulation quantum 2πħ/m per vortex at density n_v gives the mean vorticity 2Ω exactly when
  n_v = mΩ/(πħ).
* `lattice_modulation`: the khronon's response is algebraic in the gated energy, δK = c E with c ≥ 0 (FL2 V3), so on
  the lattice it lies between 0 (the cores) and c E_max.
-/

theorem cross_energy_core_scaling (r a b : ℝ) :
    6 * (r * a) ^ 2 + 2 * (r * b) ^ 2 = r ^ 2 * (6 * a ^ 2 + 2 * b ^ 2) := by
  ring

theorem cross_energy_pos_off_core (a b : ℝ) (h : a ≠ 0 ∨ b ≠ 0) : 0 < 6 * a ^ 2 + 2 * b ^ 2 := by
  rcases h with ha | hb
  · have : 0 < a ^ 2 := by positivity
    nlinarith [sq_nonneg b]
  · have : 0 < b ^ 2 := by positivity
    nlinarith [sq_nonneg a]

theorem feynman_rule (nv Ω m hbar : ℝ) (hm : 0 < m) (hh : 0 < hbar) :
    nv * (2 * Real.pi * hbar / m) = 2 * Ω ↔ nv = m * Ω / (Real.pi * hbar) := by
  have hpi : 0 < Real.pi := Real.pi_pos
  have hm' : m ≠ 0 := ne_of_gt hm
  have hh' : hbar ≠ 0 := ne_of_gt hh
  have hpi' : Real.pi ≠ 0 := ne_of_gt hpi
  constructor
  · intro h
    field_simp at h ⊢
    linarith
  · intro h
    rw [h]
    field_simp

theorem lattice_modulation (c E Emax : ℝ) (hc : 0 ≤ c) (hE : 0 ≤ E) (hle : E ≤ Emax) :
    0 ≤ c * E ∧ c * E ≤ c * Emax := by
  exact ⟨mul_nonneg hc hE, mul_le_mul_of_nonneg_left hle hc⟩

#print axioms cross_energy_core_scaling
#print axioms cross_energy_pos_off_core
#print axioms feynman_rule
#print axioms lattice_modulation
