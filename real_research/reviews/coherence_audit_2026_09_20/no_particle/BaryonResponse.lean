import Mathlib

/-! Particle-free static response, with constitutive and boundary assumptions
explicit. This does not formalize a relativistic action or observational fit. -/
namespace BaryonResponse
noncomputable section

def flux (t : ℝ) : ℝ := t * (1 - 1 / (1 + t)^2)

theorem flux_difference {u v : ℝ} (hu : 0 ≤ u) (hv : 0 ≤ v) :
    flux v - flux u = (v-u) *
      (u^2*v^2 + 2*u^2*v + u^2 + 2*u*v^2 + 5*u*v + 2*u + v^2 + 2*v) /
      ((1+u)^2 * (1+v)^2) := by
  have h1 : 1+u ≠ 0 := by linarith
  have h2 : 1+v ≠ 0 := by linarith
  unfold flux
  field_simp
  ring

theorem flux_strictMono : StrictMonoOn flux (Set.Ici 0) := by
  intro u hu v hv huv
  have hu0 : 0 ≤ u := hu
  have hv0 : 0 ≤ v := hv
  have hvp : 0 < v := lt_of_le_of_lt hu0 huv
  have hnum : 0 < u^2*v^2 + 2*u^2*v + u^2 + 2*u*v^2 + 5*u*v + 2*u + v^2 + 2*v := by
    positivity
  have hden : 0 < (1+u)^2 * (1+v)^2 := by positivity
  have hpos := div_pos (mul_pos (sub_pos.mpr huv) hnum) hden
  rw [← flux_difference hu0 hv0] at hpos
  linarith

/-- Same baryonic source, constitutive scale and spherical boundary flux
give exactly one nonnegative response amplitude. -/
theorem response_unique {u v b : ℝ} (hu : 0 ≤ u) (hv : 0 ≤ v)
    (huB : flux u = b) (hvB : flux v = b) : u = v :=
  flux_strictMono.injOn hu hv (huB.trans hvB.symm)

theorem zero_source_zero_response {u : ℝ} (hu : 0 ≤ u)
    (h : flux u = 0) : u = 0 := by
  exact response_unique hu (le_refl 0) h (by norm_num [flux])

theorem flux_lower_bound {t : ℝ} (ht : 0 ≤ t) : t-1 ≤ flux t := by
  have hp : 0 < (1+t)^2 := by positivity
  have hq : t / (1+t)^2 ≤ 1 := (div_le_one hp).mpr (by nlinarith [sq_nonneg t])
  unfold flux
  rw [mul_sub, mul_one, mul_one_div]
  linarith

/-- Every nonnegative spherical source has exactly one nonnegative
dimensionless field amplitude for this constitutive law. -/
theorem response_exists_unique {b : ℝ} (hb : 0 ≤ b) :
    ∃! t : ℝ, 0 ≤ t ∧ flux t = b := by
  have hcont : ContinuousOn flux (Set.Icc 0 (b+1)) := by
    unfold flux
    apply continuousOn_id.mul
    apply continuousOn_const.sub
    apply continuousOn_const.div
    · exact (continuousOn_const.add continuousOn_id).pow 2
    · intro t ht
      have ht0 : 0 ≤ t := ht.1
      positivity
  have hbound : b ≤ flux (b+1) := by
    have h := flux_lower_bound (show 0 ≤ b+1 by linarith)
    linarith
  have hmem : b ∈ Set.Icc (flux 0) (flux (b+1)) := by
    constructor
    · simpa [flux] using hb
    · exact hbound
  obtain ⟨t, ht, htb⟩ := intermediate_value_Icc (show 0 ≤ b+1 by linarith) hcont hmem
  refine ⟨t, ⟨ht.1, htb⟩, ?_⟩
  intro y hy
  exact response_unique hy.1 ht.1 hy.2 htb

/-- Deep-limit Gauss law and circular balance imply BTFR; these hypotheses
are stated, not silently replaced by a numerical curve fit. -/
theorem deep_btfr {r g v G M a0 : ℝ}
    (hGauss : r^2 * g^2 = G*M*a0) (hOrbit : v^2 = r*g) :
    v^4 = G*M*a0 := by nlinarith [sq_nonneg (v^2-r*g)]

/-- The Newtonian inferred mass includes the baryons. -/
theorem inferred_excess {r g G M C : ℝ} (hG : G ≠ 0) (_hr : r ≠ 0)
    (hg : g = C/r) : r^2*g/G - M = C*r/G - M := by
  rw [hg]
  field_simp

/-- Positive deep-branch amplitudes are fixed by the baryonic normalization. -/
theorem deep_amplitude_unique {C D G M a0 : ℝ} (hC : 0 ≤ C) (hD : 0 ≤ D)
    (hc : C^2 = G*M*a0) (hd : D^2 = G*M*a0) : C = D := by
  nlinarith [sq_nonneg (C-D)]

#print axioms flux_difference
#print axioms flux_strictMono
#print axioms response_unique
#print axioms zero_source_zero_response
#print axioms flux_lower_bound
#print axioms response_exists_unique
#print axioms deep_btfr
#print axioms inferred_excess
#print axioms deep_amplitude_unique
end
end BaryonResponse
