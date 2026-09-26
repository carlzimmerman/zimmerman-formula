import Mathlib

/-!
# CV1 — V0 for the C-H/K branch: the gate's off-plateau and the region kernel's force algebra

SCOPE. `real_research/chk_v0_2026/CV1_nr_assembly.py` writes the non-relativistic action the covariant V0 must reduce
to, with the vacuum gate f = W(t), W(t) = g(t)/(g(t) + g(1 − t)), g(t) = e^{−1/t} for t > 0 and 0 otherwise. That is
exactly Mathlib's `Real.smoothTransition` (built from `expNegInvGlue`). On flat FRW the gate's curvature variable
vanishes, so t = 0. Lean certifies that the homogeneous background then sits on the gate's exact off-plateau to every
order, which is why the kernel's √ε zero-field response (XC5 E6) never enters the cosmological background or its
perturbation theory. It also certifies the one-line force algebra behind CV1 A1. The Euler–Lagrange derivations
themselves are computed symbolically in the lane.

* `gate_off_plateau`: W(t) = 0 for every t ≤ 0 (an exact plateau, not an asymptote).
* `gate_on_plateau`: W(t) = 1 for every t ≥ 1.
* `gate_iteratedDeriv_continuous`: every derivative of W is continuous (W is C^∞).
* `gate_flat_below`: every derivative of W vanishes at every t < 0.
* `gate_flat_at_homogeneous`: every derivative of W vanishes at t = 0, the homogeneous background — so the kernel,
  its source and the phantom are absent there to every order of perturbation theory.
* `gate_flat_at_on_edge`: every derivative of order ≥ 1 vanishes at t = 1, the start of the on-plateau.
* `dark_component_newtonian`: with Φ = u + f P and λ = −2 f P (CV1 A1), the dark component's potential Φ + λ/2 is u.
-/

open Filter Topology Set

theorem gate_off_plateau (t : ℝ) (ht : t ≤ 0) : Real.smoothTransition t = 0 :=
  Real.smoothTransition.zero_of_nonpos ht

theorem gate_on_plateau (t : ℝ) (ht : 1 ≤ t) : Real.smoothTransition t = 1 :=
  Real.smoothTransition.one_of_one_le ht

theorem gate_iteratedDeriv_continuous (m : ℕ) : Continuous (iteratedDeriv m Real.smoothTransition) := by
  have h : ContDiff ℝ (m : ℕ∞) Real.smoothTransition := Real.smoothTransition.contDiff
  exact h.continuous_iteratedDeriv' m

theorem gate_flat_below (n : ℕ) (t : ℝ) (ht : t < 0) : iteratedDeriv n Real.smoothTransition t = 0 := by
  have hev : Real.smoothTransition =ᶠ[𝓝 t] (fun _ => (0 : ℝ)) :=
    Filter.eventuallyEq_of_mem (Iio_mem_nhds ht) (fun x hx => Real.smoothTransition.zero_of_nonpos (le_of_lt hx))
  rw [hev.iteratedDeriv_eq n, iteratedDeriv_const]
  simp

theorem gate_flat_at_homogeneous (n : ℕ) : iteratedDeriv n Real.smoothTransition 0 = 0 := by
  have hclosed : IsClosed {x : ℝ | iteratedDeriv n Real.smoothTransition x = 0} :=
    isClosed_eq (gate_iteratedDeriv_continuous n) continuous_const
  have hsub : Iio (0 : ℝ) ⊆ {x : ℝ | iteratedDeriv n Real.smoothTransition x = 0} :=
    fun x hx => gate_flat_below n x hx
  have hcl : closure (Iio (0 : ℝ)) ⊆ {x : ℝ | iteratedDeriv n Real.smoothTransition x = 0} :=
    hclosed.closure_subset_iff.mpr hsub
  rw [closure_Iio] at hcl
  exact hcl (le_refl (0 : ℝ))

theorem gate_flat_above_one (n : ℕ) (hn : 0 < n) (t : ℝ) (ht : 1 < t) :
    iteratedDeriv n Real.smoothTransition t = 0 := by
  have hev : Real.smoothTransition =ᶠ[𝓝 t] (fun _ => (1 : ℝ)) :=
    Filter.eventuallyEq_of_mem (Ioi_mem_nhds ht) (fun x hx => Real.smoothTransition.one_of_one_le (le_of_lt hx))
  rw [hev.iteratedDeriv_eq n, iteratedDeriv_const]
  simp [Nat.pos_iff_ne_zero.mp hn]

theorem gate_flat_at_on_edge (n : ℕ) (hn : 0 < n) : iteratedDeriv n Real.smoothTransition 1 = 0 := by
  have hclosed : IsClosed {x : ℝ | iteratedDeriv n Real.smoothTransition x = 0} :=
    isClosed_eq (gate_iteratedDeriv_continuous n) continuous_const
  have hsub : Ioi (1 : ℝ) ⊆ {x : ℝ | iteratedDeriv n Real.smoothTransition x = 0} :=
    fun x hx => gate_flat_above_one n hn x hx
  have hcl : closure (Ioi (1 : ℝ)) ⊆ {x : ℝ | iteratedDeriv n Real.smoothTransition x = 0} :=
    hclosed.closure_subset_iff.mpr hsub
  rw [closure_Ioi] at hcl
  exact hcl (le_refl (1 : ℝ))

theorem dark_component_newtonian (u f P : ℝ) : (u + f * P) + (-2 * f * P) / 2 = u := by
  ring

#print axioms gate_off_plateau
#print axioms gate_on_plateau
#print axioms gate_iteratedDeriv_continuous
#print axioms gate_flat_below
#print axioms gate_flat_at_homogeneous
#print axioms gate_flat_above_one
#print axioms gate_flat_at_on_edge
#print axioms dark_component_newtonian
