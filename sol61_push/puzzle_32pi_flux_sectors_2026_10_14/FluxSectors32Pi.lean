import Mathlib

noncomputable section
namespace FluxSectors32Pi

/-! Algebra of a specified Euclidean saddle. The geometric and quantum-state
interpretations are premises, not consequences of these theorems. -/

theorem target_forces_volume (r v : ℝ)
    (h : r^2*v = 24*Real.pi^2) (hr : r = 32*Real.pi) :
    v = 3/128 := by
  rw [hr] at h
  have hp : Real.pi^2 ≠ 0 := ne_of_gt (sq_pos_of_pos Real.pi_pos)
  have hf : Real.pi^2*(1024*v-24) = 0 := by nlinarith [h]
  have hz := (mul_eq_zero.mp hf).resolve_left hp
  linarith

theorem volume_forces_target (r v : ℝ) (hr : 0 < r)
    (h : r^2*v = 24*Real.pi^2) (hv : v = 3/128) :
    r = 32*Real.pi := by
  rw [hv] at h
  have hp := Real.pi_pos
  nlinarith [h, sq_nonneg (r-32*Real.pi)]

theorem target_saddle :
    (32*Real.pi)^2*(3/128:ℝ) = 24*Real.pi^2 := by ring

theorem alternative_saddle :
    (16*Real.pi)^2*(3/32:ℝ) = 24*Real.pi^2 := by ring

theorem distinct_ratios : (16:ℝ)*Real.pi ≠ 32*Real.pi := by
  have hp := Real.pi_pos
  linarith

theorem integer_target_volume :
    (23437500000:ℝ) / 1000000000000 = 3/128 := by norm_num

theorem integer_alternative_volume :
    (93750000000:ℝ) / 1000000000000 = 3/32 := by norm_num

def action (geometry bare vacuum volume scaledFlux topological : ℝ) : ℝ :=
  geometry + (bare+vacuum)*volume - bare*scaledFlux + topological

theorem gravitating_sum_invariant (bare vacuum shift : ℝ) :
    (bare-shift)+(vacuum+shift) = bare+vacuum := by ring

theorem action_shift (g b v w q t d : ℝ) :
    action g (b-d) (v+d) w q t - action g b v w q t = d*q := by
  unfold action
  ring

theorem relative_action_shift
    (g₁ g₂ b₁ b₂ v w₁ w₂ q₁ q₂ t₁ t₂ d : ℝ) :
    (action g₁ (b₁-d) (v+d) w₁ q₁ t₁ -
     action g₂ (b₂-d) (v+d) w₂ q₂ t₂) -
    (action g₁ b₁ v w₁ q₁ t₁ - action g₂ b₂ v w₂ q₂ t₂) =
    d*(q₁-q₂) := by
  unfold action
  ring

theorem unequal_flux_shift_nonzero (d q₁ q₂ : ℝ)
    (hd : d ≠ 0) (hq : q₁ ≠ q₂) : d*(q₁-q₂) ≠ 0 := by
  exact mul_ne_zero hd (sub_ne_zero.mpr hq)

#print axioms target_forces_volume
#print axioms volume_forces_target
#print axioms target_saddle
#print axioms alternative_saddle
#print axioms distinct_ratios
#print axioms integer_target_volume
#print axioms integer_alternative_volume
#print axioms gravitating_sum_invariant
#print axioms action_shift
#print axioms relative_action_shift
#print axioms unequal_flux_shift_nonzero
end FluxSectors32Pi
