/-
PAR1 (criteria 51522963e0, amendment A1 427bc818f6): Lean statements for the algebraic cores of the spec.
They certify the algebra, not the physics. TEST lane; adopts nothing. kappa = 1/2 FITTED; not theory closed.

  scr_identity    : S5, the screened response: 1 - k^2/(K chi + k^2) = K chi/(K chi + k^2).
  scr_nonpos      : S5, omega^2 = -K n K chi/(K chi + k^2) <= 0 for K, n, k^2 > 0, chi >= 0: no restoring force.
  scr_jeans       : S5 (MU1 contrast), without the polarization charge omega^2 = n k^2/chi - K n is > 0 above k_J.
  span_lt         : S7, (c0^2/2)(1 - n0^2/n^2) < c0^2/2 for n >= n0 > 0, c0 > 0.
  shock_defect    : S8 (A1 sign), quadratic P(tau): m^2 (t2^2 - t1^2)/2 + int t P' dt = b D^3/12 (exact).
  mg_bound        : S13, (3/2) f/(1 - f) <= 0.0354 with 0 <= f < 1 gives f <= 0.0231.
  ew2_bound       : S2, mu^2 R^2 (1 - e)/128 <= 4 d  <->  mu^2 R^2 <= 512 d/(1 - e) for e < 1.
  rel1_root_pos   : S12, the runaway root (K rho + sqrt(K^2 rho^2 + 4 K k))/2 is > 0.
-/
import Mathlib.Tactic

namespace PAR1

theorem scr_identity (K chi k2 : ℝ) (h : K * chi + k2 ≠ 0) :
    1 - k2 / (K * chi + k2) = K * chi / (K * chi + k2) := by
  field_simp; ring

theorem scr_nonpos (K n chi k2 : ℝ) (hK : 0 < K) (hn : 0 < n) (hc : 0 ≤ chi) (hk : 0 < k2) :
    -(K * n) * (K * chi) / (K * chi + k2) ≤ 0 := by
  have hd : 0 < K * chi + k2 := by positivity
  apply div_nonpos_of_nonpos_of_nonneg
  · have : 0 ≤ (K * n) * (K * chi) := by positivity
    linarith
  · exact hd.le

theorem scr_jeans (K n chi k2 : ℝ) (hK : 0 < K) (hn : 0 < n) (hc : 0 < chi) (hk : K * chi < k2) :
    0 < n * k2 / chi - K * n := by
  have h1 : K * n = n * (K * chi) / chi := by field_simp
  rw [h1, ← sub_div]
  apply div_pos _ hc
  have : n * (K * chi) < n * k2 := by nlinarith
  linarith

theorem span_lt (c0 n0 n : ℝ) (hc : 0 < c0) (h0 : 0 < n0) (hn : n0 ≤ n) :
    c0 ^ 2 / 2 * (1 - n0 ^ 2 / n ^ 2) < c0 ^ 2 / 2 := by
  have hnpos : 0 < n := lt_of_lt_of_le h0 hn
  have : 0 < n0 ^ 2 / n ^ 2 := by positivity
  have hc2 : 0 < c0 ^ 2 / 2 := by positivity
  nlinarith

theorem shock_defect (t1 D a b : ℝ) (hD : D ≠ 0) :
    (-(a * D + b * D ^ 2 / 2) / D) * ((t1 + D) ^ 2 - t1 ^ 2) / 2
      + (a * ((t1 + D) ^ 2 - t1 ^ 2) / 2 + b * (t1 * D ^ 2 / 2 + D ^ 3 / 3)) = b * D ^ 3 / 12 := by
  field_simp; ring

theorem mg_bound (f : ℝ) (h0 : 0 ≤ f) (h1 : f < 1) (h : 3 / 2 * f / (1 - f) ≤ 0.0354) : f ≤ 0.0231 := by
  have hpos : 0 < 1 - f := by linarith
  rw [div_le_iff₀ hpos] at h
  nlinarith

theorem ew2_bound (m2R2 d e : ℝ) (he : e < 1) :
    m2R2 * (1 - e) / 128 ≤ 4 * d ↔ m2R2 ≤ 512 * d / (1 - e) := by
  have hpos : 0 < 1 - e := by linarith
  rw [div_le_iff₀ (by norm_num : (0:ℝ) < 128), le_div_iff₀ hpos]
  constructor <;> intro h <;> linarith

theorem rel1_root_pos (K rho k : ℝ) (hK : 0 < K) (hr : 0 < rho) (hk : 0 < k) :
    0 < (K * rho + Real.sqrt (K ^ 2 * rho ^ 2 + 4 * K * k)) / 2 := by
  have : 0 ≤ Real.sqrt (K ^ 2 * rho ^ 2 + 4 * K * k) := Real.sqrt_nonneg _
  have : 0 < K * rho := mul_pos hK hr
  linarith [this]

end PAR1

#print axioms PAR1.scr_identity
#print axioms PAR1.scr_nonpos
#print axioms PAR1.scr_jeans
#print axioms PAR1.span_lt
#print axioms PAR1.shock_defect
#print axioms PAR1.mg_bound
#print axioms PAR1.ew2_bound
#print axioms PAR1.rel1_root_pos

-- Adopts nothing. kappa = 1/2 FITTED; not theory closed.
