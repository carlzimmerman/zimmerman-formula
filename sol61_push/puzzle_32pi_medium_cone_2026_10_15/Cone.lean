import Mathlib
noncomputable section
namespace MediumCone

theorem angular_endpoint (b v m c : ℝ) (hb : 0 ≤ b) (hv : 0 ≤ v)
    (hm : 0 ≤ m) (hc : -1 ≤ c) (hc' : c ≤ 1) :
    0 ≤ b * (1-c) * (2*m+v*(1+c)) := by
  apply mul_nonneg
  · exact mul_nonneg hb (by linarith)
  · have : 0 ≤ v*(1+c) := mul_nonneg hv (by linarith)
    linarith

theorem positive_root_bound (k d g s : ℝ) (hk : 0 < k) (hg : 0 < g)
    (hs : 0 ≤ s) (he : 0 ≤ k-2*d-g)
    (hr : k*s^2-2*d*s-g = 0) : s ≤ 1 := by
  by_contra h
  have h1 : 1 < s := lt_of_not_ge h
  have h2 : 0 < s*(s-1) := mul_pos (by linarith) (by linarith)
  have h3 : 0 < k*(s*(s-1)) := mul_pos hk h2
  have h4 : 0 < g*(s-1) := mul_pos hg (by linarith)
  have h5 : 0 ≤ (k-2*d-g)*s := mul_nonneg he hs
  nlinarith

theorem negative_root_bound (k d g s : ℝ) (hk : 0 < k) (hg : 0 < g)
    (hs : s ≤ 0) (he : 0 ≤ k+2*d-g)
    (hr : k*s^2-2*d*s-g = 0) : -1 ≤ s := by
  have h := positive_root_bound k (-d) g (-s) hk hg (by linarith)
    (by linarith) (by nlinarith [hr])
  linarith

theorem quartic_strict_concavity (v : ℝ) (hv : 0 ≤ v) :
    -2400*v^2-1200*v-596 < 0 := by
  nlinarith [sq_nonneg v]

#print axioms angular_endpoint
#print axioms positive_root_bound
#print axioms negative_root_bound
#print axioms quartic_strict_concavity
end MediumCone
