/-
EW2 (closure_2026_11_07/EW2_aest_nonlinear, criteria 869b3d72ad / origin 041be83e4a): algebra used by the AeST lane.

T1 `capped_map`: the capped free function's static map. With J'(v) = v/(a0 - v), the field equation (1 + J') v = g has
   the root v = a0 g/(a0 + g), and it lies in [0, a0) for g >= 0 (the cap Y < a0^2; C1 K2).
T2 `band_leakage`: if the web response is B_i >= 1 on every mode and B_i >= b on the band set S, then for weights
   w_i >= 0 summing to 1 the weighted gain obeys sum w_i B_i - 1 >= (b - 1) sum_{i in S} w_i. (Iter_2: a band share s
   of the lensing weight with the law's floor b = nu_min^2 forces r - 1 >= (b - 1) s.)
T3 `static_dust_bound`: hydrostatic dust per shell c |Phi_i| v_i (c = mu^2/(4 pi G) >= 0, v_i >= 0 shell volumes) with
   |Phi_i| <= Phimax sums to at most c Phimax sum v_i.
T4 `window_empty`: if every member passing the web gate has mu >= mu_w, every member passing the host gate has
   mu <= mu_h, and mu_h < mu_w, no member passes both.
kappa = 1/2 FITTED; not theory closed.
-/
import Mathlib

namespace EW2

theorem capped_map {a0 g : ℝ} (ha : 0 < a0) (hg : 0 ≤ g) :
    0 ≤ a0 * g / (a0 + g) ∧ a0 * g / (a0 + g) < a0 ∧
    a0 * g / (a0 + g) * (1 + (a0 * g / (a0 + g)) / (a0 - a0 * g / (a0 + g))) = g := by
  have hpos : 0 < a0 + g := by linarith
  refine ⟨by positivity, ?_, ?_⟩
  · rw [div_lt_iff₀ hpos]; nlinarith
  · have hd : a0 - a0 * g / (a0 + g) = a0 * a0 / (a0 + g) := by
      field_simp; ring
    rw [hd]
    field_simp

theorem band_leakage {ι : Type*} (s : Finset ι) (S : Finset ι) (hS : S ⊆ s) (w B : ι → ℝ) (b : ℝ)
    (hw : ∀ i ∈ s, 0 ≤ w i) (hsum : ∑ i ∈ s, w i = 1) (hB1 : ∀ i ∈ s, 1 ≤ B i) (hBb : ∀ i ∈ S, b ≤ B i) :
    (b - 1) * ∑ i ∈ S, w i ≤ ∑ i ∈ s, w i * B i - 1 := by
  have h1 : ∑ i ∈ s, w i * B i - 1 = ∑ i ∈ s, w i * (B i - 1) := by
    simp only [mul_sub, mul_one, Finset.sum_sub_distrib, hsum]
  rw [h1, Finset.mul_sum]
  calc ∑ i ∈ S, (b - 1) * w i ≤ ∑ i ∈ S, w i * (B i - 1) := by
        apply Finset.sum_le_sum; intro i hi
        have := hBb i hi; have := hw i (hS hi); nlinarith
    _ ≤ ∑ i ∈ s, w i * (B i - 1) := by
        apply Finset.sum_le_sum_of_subset_of_nonneg hS
        intro i hi _; have := hB1 i hi; have := hw i hi; nlinarith

theorem static_dust_bound {ι : Type*} (s : Finset ι) (c Pmax : ℝ) (P v : ι → ℝ) (hc : 0 ≤ c)
    (hv : ∀ i ∈ s, 0 ≤ v i) (hP : ∀ i ∈ s, |P i| ≤ Pmax) :
    ∑ i ∈ s, c * |P i| * v i ≤ c * Pmax * ∑ i ∈ s, v i := by
  rw [Finset.mul_sum]
  apply Finset.sum_le_sum; intro i hi
  have hPi := hP i hi; have hvi := hv i hi
  have hcP : c * |P i| ≤ c * Pmax := mul_le_mul_of_nonneg_left hPi hc
  exact mul_le_mul_of_nonneg_right hcP hvi

theorem window_empty (web host : ℝ → Prop) (mu_w mu_h : ℝ) (hw : ∀ m, web m → mu_w ≤ m)
    (hh : ∀ m, host m → m ≤ mu_h) (hlt : mu_h < mu_w) : ¬ ∃ m, web m ∧ host m := by
  rintro ⟨m, h1, h2⟩
  have := hw m h1; have := hh m h2; linarith

end EW2

#print axioms EW2.capped_map
#print axioms EW2.band_leakage
#print axioms EW2.static_dust_bound
#print axioms EW2.window_empty
