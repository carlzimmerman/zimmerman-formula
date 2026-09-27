import Mathlib

/-! Algebraic bridges for the displayed action variations. The continuum
divergence theorem, Sobolev estimates and physical interpretation are not
axiomatized here. -/
namespace AssemblyBridge20260926

theorem positive_source_zero_mode_impossible {ι : Type*}
    (s : Finset ι) (hs : s.Nonempty) (w rho d : ι → ℝ)
    (hw : ∀ i ∈ s, 0 < w i) (hr : ∀ i ∈ s, 0 < rho i)
    (hd : ∑ i ∈ s, d i = 0)
    (he : ∀ i ∈ s, d i + w i * rho i = 0) : False := by
  have hp : 0 < ∑ i ∈ s, w i * rho i :=
    Finset.sum_pos (fun i hi => mul_pos (hw i hi) (hr i hi)) hs
  have hz : ∑ i ∈ s, (d i + w i * rho i) = 0 := by
    apply Finset.sum_eq_zero
    exact he
  rw [Finset.sum_add_distrib, hd, zero_add] at hz
  linarith

theorem mean_projection_cancels_total_source {ι : Type*}
    (s : Finset ι) (w source : ι → ℝ)
    (hv : (∑ i ∈ s, w i) ≠ 0) :
    ∑ i ∈ s, (w i * source i - w i *
      ((∑ j ∈ s, w j * source j) / (∑ j ∈ s, w j))) = 0 := by
  rw [Finset.sum_sub_distrib, ← Finset.sum_mul]
  field_simp
  ring

theorem bounded_quartic_decomposition (R2 s2 lam eta : ℝ) :
    lam * (R2^2 + s2^2) / 4 - eta * R2 * s2 / 2 =
      (lam - eta) * (R2^2 + s2^2) / 4 + eta * (R2 - s2)^2 / 4 := by
  ring

theorem bounded_quartic_nonnegative (R2 s2 lam eta : ℝ)
    (he : 0 ≤ eta) (hl : eta ≤ lam) :
    0 ≤ lam * (R2^2 + s2^2) / 4 - eta * R2 * s2 / 2 := by
  rw [bounded_quartic_decomposition]
  positivity

theorem gate_energy_bound (H E m omega z : ℝ)
    (hm : 0 < m) (ho : 0 < omega)
    (hco : m^2 * omega^2 * z^2 / 2 ≤ H) (he : H ≤ E) :
    z^2 ≤ 2 * E / (m^2 * omega^2) := by
  apply (le_div_iff₀ (mul_pos (sq_pos_of_pos hm) (sq_pos_of_pos ho))).2
  nlinarith

theorem convex_composition_second_variation (fp fpp jpp v : ℝ)
    (hp : 0 ≤ fp) (hpp : 0 ≤ fpp) (hj : 0 ≤ jpp) :
    0 ≤ fp * jpp + fpp * v^2 := by positivity

end AssemblyBridge20260926
#print axioms AssemblyBridge20260926.positive_source_zero_mode_impossible
#print axioms AssemblyBridge20260926.mean_projection_cancels_total_source
#print axioms AssemblyBridge20260926.bounded_quartic_decomposition
#print axioms AssemblyBridge20260926.bounded_quartic_nonnegative
#print axioms AssemblyBridge20260926.gate_energy_bound
#print axioms AssemblyBridge20260926.convex_composition_second_variation
