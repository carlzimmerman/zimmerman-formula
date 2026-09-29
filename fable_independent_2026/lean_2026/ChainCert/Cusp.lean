import Mathlib
/-!
# Cusp -- the NFW small-radius (cusp) property behind the CFG42 / CFG65 debris results

Setting: reals; every mass, radius and concentration is > 0 where a theorem needs it (hypotheses explicit).
* m(x) = ln(1+x) - x/(1+x) (junk-free: 1+x > 0 for x >= 0; only `Real.log` of a positive number is used).
* `nfwMass M200 R200 c r = M200 * m(c r/R200) / m(c)`   (division by m(c) is safe: `m_pos` for c > 0).

CERTIFIED (pure real analysis, premises => conclusion):
 (1) `m_pos`, `m_strictMonoOn` (strictly increasing on [0,oo)), `m_upper` (m <= x^2/2, all x >= 0),
     `m_lower` (x^2/2 - 2x^3/3 <= m, ALL x >= 0 -- no range restriction needed), `m_elastic`, `m_div_sq_antitoneOn`.
 (2) `nfw_small_r_form1`, `nfw_small_r_K`, `nfw_small_r_rho_s`: M(<r)/(K r^2) -> 1 as r -> 0+ (Tendsto on nhdsWithin (Ioi 0) 0),
     K = M200 c^2/(2 m(c) R200^2) = 2 pi rho_s r_s (`nfw_rho_s_form`, r_s = R200/c, rho_s = M200/(4 pi r_s^3 m(c))).
 (3) `Kfam_identity` (exact), `Kfam_ratio` (exact), `leading_exponent` (1/3 - 2*101/1000 = 197/1500 in (0.1313, 0.1314)),
     `Kfam_bracket` : for a > 0, M1 <= M2:  (M2/M1)^(1/3-2a) <= K(M2)/K(M1) <= (M2/M1)^(1/3);
     `Kfam_bracket_range` : if c(M1), c(M2) in [5,20] the modulating factor is <= 9/4 (`m_ratio_range`).
 (4) `debris_corollary` : a = 101/1000, c0 = 16.8 * (1e9)^a (so c(1e9) = 16.8), ANY k > 0:
     100^(1/3-2a) in (1.830, 1.832), c(1e8) in (21.18, 21.22), c(1e10) in (13.30, 13.32),
     and 2.25 < K(1e10)/K(1e8) < 2.29.

NOT certified: that real halos follow c = c0 M^-a or R200 ~ M^(1/3) (a = 0.101 is an empirical Dutton-Maccio-type fit; here it is
a declared constant); that NFW describes any real halo; anything about debris / CFG data.  The family is a DECLARED model.
-/

open Filter Topology
set_option exponentiation.threshold 4000
noncomputable section
namespace Cusp

/-- NFW mass function m(x) = ln(1+x) - x/(1+x). -/
def m (x : ℝ) : ℝ := Real.log (1 + x) - x / (1 + x)

theorem m_zero : m 0 = 0 := by simp [m]

theorem m_hasDerivAt {x : ℝ} (hx : -1 < x) : HasDerivAt m (x / (1 + x) ^ 2) x := by
  have h1 : (1 + x) ≠ 0 := by linarith
  have hl : HasDerivAt (fun y : ℝ => Real.log (1 + y)) (1 / (1 + x)) x := by
    have := ((hasDerivAt_id x).const_add 1).log h1
    simpa using this
  have hq : HasDerivAt (fun y : ℝ => y / (1 + y)) (((1:ℝ) * (1 + x) - x * 1) / (1 + x) ^ 2) x := by
    exact (hasDerivAt_id x).div ((hasDerivAt_id x).const_add 1) h1
  have := hl.sub hq
  refine this.congr_deriv ?_
  field_simp
  ring

/-- generic: derivative >= 0 on x >= 0 gives f 0 <= f x. -/
theorem le_of_deriv_nonneg {f f' : ℝ → ℝ} (hd : ∀ x, 0 ≤ x → HasDerivAt f (f' x) x)
    (hn : ∀ x, 0 < x → 0 ≤ f' x) {x : ℝ} (hx : 0 ≤ x) : f 0 ≤ f x := by
  have hc : ContinuousOn f (Set.Ici 0) := fun y hy => (hd y hy).continuousAt.continuousWithinAt
  have hm : MonotoneOn f (Set.Ici 0) := by
    apply monotoneOn_of_deriv_nonneg (convex_Ici 0) hc
    · rw [interior_Ici]; intro y hy; exact (hd y (le_of_lt hy)).differentiableAt.differentiableWithinAt
    · rw [interior_Ici]; intro y hy; rw [(hd y (le_of_lt hy)).deriv]; exact hn y hy
  exact hm (Set.mem_Ici.2 le_rfl) (Set.mem_Ici.2 hx) hx

theorem m_strictMonoOn : StrictMonoOn m (Set.Ici 0) := by
  have hc : ContinuousOn m (Set.Ici 0) := fun y hy =>
    (m_hasDerivAt (by have := Set.mem_Ici.1 hy; linarith)).continuousAt.continuousWithinAt
  apply strictMonoOn_of_deriv_pos (convex_Ici 0) hc
  intro y hy
  rw [interior_Ici] at hy
  have hy' : (0:ℝ) < y := hy
  rw [(m_hasDerivAt (by linarith)).deriv]
  positivity

theorem m_pos {x : ℝ} (hx : 0 < x) : 0 < m x := by
  have := m_strictMonoOn (Set.mem_Ici.2 le_rfl) (Set.mem_Ici.2 hx.le) hx
  simpa [m_zero] using this

theorem m_upper {x : ℝ} (hx : 0 ≤ x) : m x ≤ x ^ 2 / 2 := by
  have hd : ∀ y : ℝ, 0 ≤ y → HasDerivAt (fun y => y ^ 2 / 2 - m y)
      (y ^ 2 * (2 + y) / (1 + y) ^ 2) y := by
    intro y hy
    have h1 : (1 + y) ≠ 0 := by linarith
    have := ((hasDerivAt_pow 2 y).div_const 2).sub (m_hasDerivAt (by linarith : -1 < y))
    refine this.congr_deriv ?_
    field_simp
    ring
  have := le_of_deriv_nonneg hd (fun y hy => by positivity) hx
  simp [m_zero] at this
  linarith

theorem m_lower {x : ℝ} (hx : 0 ≤ x) : x ^ 2 / 2 - 2 * x ^ 3 / 3 ≤ m x := by
  have hd : ∀ y : ℝ, 0 ≤ y → HasDerivAt (fun y => m y - y ^ 2 / 2 + 2 * y ^ 3 / 3)
      (y ^ 3 * (3 + 2 * y) / (1 + y) ^ 2) y := by
    intro y hy
    have h1 : (1 + y) ≠ 0 := by linarith
    have := (((m_hasDerivAt (by linarith : -1 < y)).sub ((hasDerivAt_pow 2 y).div_const 2)).add
      ((hasDerivAt_pow 3 y).const_mul 2 |>.div_const 3))
    refine this.congr_deriv ?_
    field_simp
    ring
  have := le_of_deriv_nonneg hd (fun y hy => by positivity) hx
  simp [m_zero] at this
  linarith


/-! ### elasticity: x m'(x) <= 2 m(x), hence m(x)/x^2 is antitone -/

theorem m_elastic {x : ℝ} (hx : 0 ≤ x) : (x / (1 + x)) ^ 2 ≤ 2 * m x := by
  have hd : ∀ y : ℝ, 0 ≤ y → HasDerivAt (fun y => 2 * m y - (y / (1 + y)) ^ 2)
      (2 * y ^ 2 / (1 + y) ^ 3) y := by
    intro y hy
    have h1 : (1 + y) ≠ 0 := by linarith
    have hq : HasDerivAt (fun y : ℝ => y / (1 + y)) (((1:ℝ) * (1 + y) - y * 1) / (1 + y) ^ 2) y :=
      (hasDerivAt_id y).div ((hasDerivAt_id y).const_add 1) h1
    have := ((m_hasDerivAt (by linarith : -1 < y)).const_mul 2).sub (hq.pow 2)
    refine this.congr_deriv ?_
    norm_num
    field_simp
    ring
  have := le_of_deriv_nonneg hd (fun y hy => by positivity) hx
  simp [m_zero] at this
  linarith

theorem m_div_sq_antitoneOn : AntitoneOn (fun x => m x / x ^ 2) (Set.Ioi 0) := by
  have hd : ∀ y : ℝ, 0 < y → HasDerivAt (fun x => m x / x ^ 2)
      ((y / (1 + y) ^ 2 * y ^ 2 - m y * (2 * y ^ 1 * 1)) / (y ^ 2) ^ 2) y := by
    intro y hy
    have := (m_hasDerivAt (by linarith : -1 < y)).div (hasDerivAt_pow 2 y) (by positivity)
    exact this.congr_deriv (by simp)
  apply antitoneOn_of_deriv_nonpos (convex_Ioi 0)
  · exact fun y hy => (hd y hy).continuousAt.continuousWithinAt
  · rw [interior_Ioi]; exact fun y hy => (hd y hy).differentiableAt.differentiableWithinAt
  · rw [interior_Ioi]
    intro y hy
    have hy' : (0:ℝ) < y := hy
    rw [(hd y hy').deriv]
    have hel := m_elastic hy'.le
    have hlt : y / (1 + y) ^ 2 * y ^ 2 ≤ m y * (2 * y ^ 1 * 1) := by
      have e : y / (1 + y) ^ 2 * y ^ 2 = y * (y / (1 + y)) ^ 2 := by field_simp
      rw [e]; nlinarith [hel]
    apply div_nonpos_of_nonpos_of_nonneg (by linarith) (by positivity)

/-! ### (2) small-radius limit -/

/-- NFW enclosed mass in the M200 / R200 / c parametrisation. -/
def nfwMass (M200 R200 c r : ℝ) : ℝ := M200 * m (c * r / R200) / m c

/-- the leading r^2 coefficient `K = M200 c^2 / (2 m(c) R200^2)`. -/
def Kc (M200 R200 c : ℝ) : ℝ := M200 * c ^ 2 / (2 * m c * R200 ^ 2)

theorem m_ratio_tendsto : Tendsto (fun x : ℝ => m x / (x ^ 2 / 2)) (𝓝[>] 0) (𝓝 1) := by
  have hlo : Tendsto (fun x : ℝ => 1 - 4 * x / 3) (𝓝[>] 0) (𝓝 1) := by
    have : Tendsto (fun x : ℝ => 1 - 4 * x / 3) (𝓝 0) (𝓝 (1 - 4 * 0 / 3)) :=
      (continuous_const.sub ((continuous_const.mul continuous_id).div_const 3)).tendsto 0
    simpa using this.mono_left nhdsWithin_le_nhds
  refine tendsto_of_tendsto_of_tendsto_of_le_of_le' hlo tendsto_const_nhds ?_ ?_
  · filter_upwards [self_mem_nhdsWithin] with x hx
    have hx' : (0:ℝ) < x := hx
    rw [le_div_iff₀ (by positivity)]
    nlinarith [m_lower hx'.le]
  · filter_upwards [self_mem_nhdsWithin] with x hx
    have hx' : (0:ℝ) < x := hx
    rw [div_le_iff₀ (by positivity)]
    nlinarith [m_upper hx'.le]

/-- (2), first form: `M(<r) / [M200 (c r/R200)^2 / (2 m(c))] -> 1` as `r -> 0+`. -/
theorem nfw_small_r_form1 {M200 R200 c : ℝ} (hM : 0 < M200) (hR : 0 < R200) (hc : 0 < c) :
    Tendsto (fun r => nfwMass M200 R200 c r / (M200 * (c * r / R200) ^ 2 / (2 * m c)))
      (𝓝[>] 0) (𝓝 1) := by
  have hmc : 0 < m c := m_pos hc
  have hx : Tendsto (fun r : ℝ => c * r / R200) (𝓝[>] 0) (𝓝[>] 0) := by
    refine tendsto_nhdsWithin_iff.2 ⟨?_, ?_⟩
    · have : Tendsto (fun r : ℝ => c * r / R200) (𝓝 0) (𝓝 (c * 0 / R200)) :=
        ((continuous_const.mul continuous_id).div_const R200).tendsto 0
      simpa using this.mono_left nhdsWithin_le_nhds
    · filter_upwards [self_mem_nhdsWithin] with r hr
      exact div_pos (mul_pos hc hr) hR
  refine (m_ratio_tendsto.comp hx).congr' ?_
  filter_upwards [self_mem_nhdsWithin] with r hr
  have hr' : (0:ℝ) < r := hr
  have hxp : 0 < c * r / R200 := div_pos (mul_pos hc hr') hR
  simp only [Function.comp, nfwMass]
  field_simp

/-- (2), second form: with `K = M200 c^2/(2 m(c) R200^2)`, `M(<r) / (K r^2) -> 1`. -/
theorem nfw_small_r_K {M200 R200 c : ℝ} (hM : 0 < M200) (hR : 0 < R200) (hc : 0 < c) :
    Tendsto (fun r => nfwMass M200 R200 c r / (Kc M200 R200 c * r ^ 2)) (𝓝[>] 0) (𝓝 1) := by
  refine (nfw_small_r_form1 hM hR hc).congr ?_
  intro r
  have hmc : 0 < m c := m_pos hc
  unfold Kc
  congr 1
  field_simp

/-- the textbook `2 pi rho_s r_s r^2` form: with `r_s = R200/c`, `rho_s = M200/(4 pi r_s^3 m(c))`
the mass is `4 pi rho_s r_s^3 m(r/r_s)` and `K r^2 = 2 pi rho_s r_s r^2`. -/
theorem nfw_rho_s_form {M200 R200 c : ℝ} (hM : 0 < M200) (hR : 0 < R200) (hc : 0 < c) (r : ℝ) :
    let rs := R200 / c
    let rhos := M200 / (4 * Real.pi * rs ^ 3 * m c)
    nfwMass M200 R200 c r = 4 * Real.pi * rhos * rs ^ 3 * m (r / rs) ∧
      Kc M200 R200 c * r ^ 2 = 2 * Real.pi * rhos * rs * r ^ 2 := by
  intro rs rhos
  have hmc : 0 < m c := m_pos hc
  have hpi : Real.pi ≠ 0 := Real.pi_ne_zero
  constructor
  · simp only [nfwMass, rhos, rs]
    have : c * r / R200 = r / (R200 / c) := by field_simp
    rw [this]
    field_simp
  · simp only [Kc, rhos, rs]
    field_simp
    ring

theorem nfw_small_r_rho_s {M200 R200 c : ℝ} (hM : 0 < M200) (hR : 0 < R200) (hc : 0 < c) :
    Tendsto (fun r => nfwMass M200 R200 c r /
      (2 * Real.pi * (M200 / (4 * Real.pi * (R200 / c) ^ 3 * m c)) * (R200 / c) * r ^ 2))
      (𝓝[>] 0) (𝓝 1) := by
  refine (nfw_small_r_K hM hR hc).congr ?_
  intro r
  rw [← (nfw_rho_s_form hM hR hc r).2]


/-! ### (3) the mass family R200 = k M^(1/3), c = c0 M^(-a) -/

/-- the family coefficient `K(M)`. -/
def Kfam (a c0 k M : ℝ) : ℝ := Kc M (k * M ^ (1 / 3 : ℝ)) (c0 * M ^ (-a))

/-- concentration along the family. -/
def cfam (a c0 M : ℝ) : ℝ := c0 * M ^ (-a)

/-- exact identity `K(M) = M^(1/3 - 2a) c0^2 / (2 k^2 m(c0 M^-a))`. -/
theorem Kfam_identity {a c0 k M : ℝ} (hc0 : 0 < c0) (hk : 0 < k) (hM : 0 < M) :
    Kfam a c0 k M = M ^ (1 / 3 - 2 * a) * (c0 ^ 2 / (2 * k ^ 2 * m (c0 * M ^ (-a)))) := by
  have hp : 0 < M ^ (1 / 3 : ℝ) := Real.rpow_pos_of_pos hM _
  have hq : 0 < M ^ (-a) := Real.rpow_pos_of_pos hM _
  have h3 : M = M ^ (1 / 3 : ℝ) * M ^ (1 / 3 : ℝ) * M ^ (1 / 3 : ℝ) := by
    rw [← Real.rpow_add hM, ← Real.rpow_add hM]; norm_num
  have he : M ^ (1 / 3 - 2 * a) = M ^ (1 / 3 : ℝ) * M ^ (-a) * M ^ (-a) := by
    rw [← Real.rpow_add hM, ← Real.rpow_add hM]; congr 1; ring
  have hmc : 0 < m (c0 * M ^ (-a)) := m_pos (mul_pos hc0 hq)
  unfold Kfam Kc
  rw [he]
  set p := M ^ (1 / 3 : ℝ)
  set q := M ^ (-a)
  field_simp
  nth_rewrite 1 [h3]
  ring

/-- exact two-mass ratio. -/
theorem Kfam_ratio {a c0 k M1 M2 : ℝ} (hc0 : 0 < c0) (hk : 0 < k) (h1 : 0 < M1) (h2 : 0 < M2) :
    Kfam a c0 k M2 / Kfam a c0 k M1 =
      (M2 / M1) ^ (1 / 3 - 2 * a) * (m (cfam a c0 M1) / m (cfam a c0 M2)) := by
  rw [Kfam_identity hc0 hk h1, Kfam_identity hc0 hk h2, Real.div_rpow h2.le h1.le]
  have hm1 : 0 < m (c0 * M1 ^ (-a)) := m_pos (mul_pos hc0 (Real.rpow_pos_of_pos h1 _))
  have hm2 : 0 < m (c0 * M2 ^ (-a)) := m_pos (mul_pos hc0 (Real.rpow_pos_of_pos h2 _))
  have hA : 0 < M1 ^ (1 / 3 - 2 * a) := Real.rpow_pos_of_pos h1 _
  unfold cfam
  field_simp

/-- the leading exponent for the Dutton-Maccio-like slope a = 101/1000. -/
theorem leading_exponent : (1 / 3 : ℚ) - 2 * (101 / 1000) = 197 / 1500 ∧
    (0.1313 : ℚ) < 197 / 1500 ∧ (197 / 1500 : ℚ) < 0.1314 := by norm_num

/-- the concentration decreases with M (a > 0), so `m(c(M))` decreases and the correction factor
`1/m` increases: `K(M2)/K(M1) >= (M2/M1)^(1/3-2a)`; and `m/c^2` is antitone, giving `<= (M2/M1)^(1/3)`. -/
theorem Kfam_bracket {a c0 k M1 M2 : ℝ} (ha : 0 < a) (hc0 : 0 < c0) (hk : 0 < k)
    (h1 : 0 < M1) (h12 : M1 ≤ M2) :
    (M2 / M1) ^ (1 / 3 - 2 * a) ≤ Kfam a c0 k M2 / Kfam a c0 k M1 ∧
    Kfam a c0 k M2 / Kfam a c0 k M1 ≤ (M2 / M1) ^ (1 / 3 : ℝ) := by
  have h2 : 0 < M2 := lt_of_lt_of_le h1 h12
  rw [Kfam_ratio hc0 hk h1 h2]
  have hq1 : 0 < M1 ^ (-a) := Real.rpow_pos_of_pos h1 _
  have hq2 : 0 < M2 ^ (-a) := Real.rpow_pos_of_pos h2 _
  have hc2 : 0 < cfam a c0 M2 := mul_pos hc0 hq2
  have hc1 : 0 < cfam a c0 M1 := mul_pos hc0 hq1
  have hcc : cfam a c0 M2 ≤ cfam a c0 M1 :=
    mul_le_mul_of_nonneg_left (Real.rpow_le_rpow_of_nonpos h1 h12 (by linarith)) hc0.le
  have hm2 : 0 < m (cfam a c0 M2) := m_pos hc2
  have hmono : m (cfam a c0 M2) ≤ m (cfam a c0 M1) :=
    m_strictMonoOn.monotoneOn (Set.mem_Ici.2 hc2.le) (Set.mem_Ici.2 hc1.le) hcc
  have ht : 0 < M2 / M1 := div_pos h2 h1
  constructor
  · have : 1 ≤ m (cfam a c0 M1) / m (cfam a c0 M2) := by rw [le_div_iff₀ hm2]; linarith
    calc (M2 / M1) ^ (1 / 3 - 2 * a) = (M2 / M1) ^ (1 / 3 - 2 * a) * 1 := by ring
      _ ≤ _ := mul_le_mul_of_nonneg_left this (Real.rpow_nonneg ht.le _)
  · have hanti := m_div_sq_antitoneOn (Set.mem_Ioi.2 hc2) (Set.mem_Ioi.2 hc1) hcc
    simp only at hanti
    have hratio : m (cfam a c0 M1) / m (cfam a c0 M2) ≤ (M2 / M1) ^ (2 * a) := by
      have hca : cfam a c0 M1 / cfam a c0 M2 = (M2 / M1) ^ a := by
        unfold cfam
        rw [Real.div_rpow h2.le h1.le, Real.rpow_neg h1.le, Real.rpow_neg h2.le]
        have := Real.rpow_pos_of_pos h1 a
        have := Real.rpow_pos_of_pos h2 a
        field_simp
      have hsq : (M2 / M1) ^ (2 * a) = (cfam a c0 M1 / cfam a c0 M2) ^ 2 := by
        rw [hca, ← Real.rpow_natCast, ← Real.rpow_mul ht.le]; norm_num; ring_nf
      rw [hsq, div_pow, div_le_div_iff₀ hm2 (by positivity)]
      have := hanti
      rw [div_le_div_iff₀ (by positivity) (by positivity)] at this
      nlinarith [this]
    have hadd : (M2 / M1) ^ (1 / 3 - 2 * a) * (M2 / M1) ^ (2 * a) = (M2 / M1) ^ (1 / 3 : ℝ) := by
      rw [← Real.rpow_add ht]; congr 1; ring
    calc (M2 / M1) ^ (1 / 3 - 2 * a) * (m (cfam a c0 M1) / m (cfam a c0 M2))
        ≤ (M2 / M1) ^ (1 / 3 - 2 * a) * (M2 / M1) ^ (2 * a) :=
          mul_le_mul_of_nonneg_left hratio (Real.rpow_nonneg ht.le _)
      _ = _ := hadd


/-! ### numeric logarithm helpers (exp-anchored tangent bounds) -/

theorem log_lo {x n E : ℝ} (hx : 0 < x) (hE : Real.exp n ≤ E) : n + 1 - E / x ≤ Real.log x := by
  have hen : 0 < Real.exp n := Real.exp_pos n
  have h := Real.one_sub_inv_le_log_of_pos (div_pos hx hen)
  rw [Real.log_div hx.ne' hen.ne', Real.log_exp, inv_div] at h
  have : E / x ≥ Real.exp n / x := div_le_div_of_nonneg_right hE hx.le
  linarith

theorem log_hi {x n E : ℝ} (hx : 0 < x) (hE0 : 0 < E) (hE : E ≤ Real.exp n) :
    Real.log x ≤ n - 1 + x / E := by
  have hen : 0 < Real.exp n := Real.exp_pos n
  have h := Real.log_le_sub_one_of_pos (div_pos hx hen)
  rw [Real.log_div hx.ne' hen.ne', Real.log_exp] at h
  have : x / Real.exp n ≤ x / E := div_le_div_of_nonneg_left hx.le hE0 hE
  linarith

theorem exp2_le : Real.exp 2 ≤ 7.3890561 := by
  have h := Real.exp_one_lt_d9
  have e : Real.exp 2 = Real.exp 1 * Real.exp 1 := by rw [← Real.exp_add]; norm_num
  rw [e]; nlinarith [Real.exp_pos 1]

theorem exp3_le : Real.exp 3 ≤ 20.0855370 := by
  have h := Real.exp_one_lt_d9
  have e : Real.exp 3 = Real.exp 1 * Real.exp 1 * Real.exp 1 := by
    rw [← Real.exp_add, ← Real.exp_add]; norm_num
  rw [e]
  have := Real.exp_pos 1
  have h2 : Real.exp 1 * Real.exp 1 ≤ 2.7182818286 * 2.7182818286 := by nlinarith
  nlinarith

theorem exp3_ge : 20.0855369 ≤ Real.exp 3 := by
  have h := Real.exp_one_gt_d9
  have e : Real.exp 3 = Real.exp 1 * Real.exp 1 * Real.exp 1 := by
    rw [← Real.exp_add, ← Real.exp_add]; norm_num
  rw [e]
  have h2 : 2.7182818283 * 2.7182818283 ≤ Real.exp 1 * Real.exp 1 := by nlinarith
  nlinarith

theorem exp_4log2 : Real.exp (4 * Real.log 2) = 16 := by
  have : (4 : ℝ) * Real.log 2 = Real.log (2 ^ 4) := by rw [Real.log_pow]; norm_num
  rw [this, Real.exp_log (by norm_num)]; norm_num

theorem m5_ge : 0.935 ≤ m 5 := by
  have h := log_lo (x := 6) (n := 2) (E := 7.3890561) (by norm_num) exp2_le
  unfold m
  norm_num at h ⊢
  linarith

theorem m20_le : m 20 ≤ 2.0932 := by
  have h := log_hi (x := 21) (n := 3) (E := 20.0855369) (by norm_num) (by norm_num) exp3_ge
  unfold m
  norm_num at h ⊢
  linarith

/-- For concentrations in [5,20] the modulating factor is bounded: `m(c1)/m(c2) <= 9/4`. -/
theorem m_ratio_range {c1 c2 : ℝ} (h1 : c1 ∈ Set.Icc (5:ℝ) 20) (h2 : c2 ∈ Set.Icc (5:ℝ) 20) :
    m c1 / m c2 ≤ 9 / 4 := by
  have hm2 : m 5 ≤ m c2 := m_strictMonoOn.monotoneOn (Set.mem_Ici.2 (by norm_num)) (Set.mem_Ici.2 (by linarith [h2.1])) h2.1
  have hm1 : m c1 ≤ m 20 := m_strictMonoOn.monotoneOn (Set.mem_Ici.2 (by linarith [h1.1])) (Set.mem_Ici.2 (by norm_num)) h1.2
  have hp : 0 < m c2 := lt_of_lt_of_le (by linarith [m5_ge]) hm2
  rw [div_le_iff₀ hp]
  nlinarith [m5_ge, m20_le]

/-- (3b) for c(M1), c(M2) in [5,20] (the range the debris analysis uses) the exponent modification is
a factor at most 9/4:  `(M2/M1)^(1/3-2a) <= K(M2)/K(M1) <= (9/4)(M2/M1)^(1/3-2a)`, and also `<= (M2/M1)^(1/3)`. -/
theorem Kfam_bracket_range {a c0 k M1 M2 : ℝ} (ha : 0 < a) (hc0 : 0 < c0) (hk : 0 < k)
    (h1 : 0 < M1) (h12 : M1 ≤ M2)
    (hc1 : cfam a c0 M1 ∈ Set.Icc (5:ℝ) 20) (hc2 : cfam a c0 M2 ∈ Set.Icc (5:ℝ) 20) :
    (M2 / M1) ^ (1 / 3 - 2 * a) ≤ Kfam a c0 k M2 / Kfam a c0 k M1 ∧
    Kfam a c0 k M2 / Kfam a c0 k M1 ≤ min (9 / 4 * (M2 / M1) ^ (1 / 3 - 2 * a)) ((M2 / M1) ^ (1 / 3 : ℝ)) := by
  have h2 : 0 < M2 := lt_of_lt_of_le h1 h12
  obtain ⟨hlo, hhi⟩ := Kfam_bracket ha hc0 hk h1 h12
  refine ⟨hlo, le_min ?_ hhi⟩
  rw [Kfam_ratio hc0 hk h1 h2]
  have := m_ratio_range hc1 hc2
  have ht : 0 ≤ (M2 / M1) ^ (1 / 3 - 2 * a) := Real.rpow_nonneg (div_pos h2 h1).le _
  calc (M2 / M1) ^ (1 / 3 - 2 * a) * (m (cfam a c0 M1) / m (cfam a c0 M2))
      ≤ (M2 / M1) ^ (1 / 3 - 2 * a) * (9 / 4) := mul_le_mul_of_nonneg_left this ht
    _ = _ := by ring


/-! ### (4) concrete corollary: M = 1e8 vs 1e10, halo with c = 16.8 at 1e9 Msun -/

/-- the three masses (Msun). -/
def M8 : ℝ := 10 ^ 8
def M9 : ℝ := 10 ^ 9
def M10 : ℝ := 10 ^ 10

/-- Dutton-Maccio-like slope used as the declared constant (an empirical fit, NOT certified). -/
def aDM : ℝ := 101 / 1000

/-- `c0` fixed so that `c(1e9) = 16.8`. -/
def c0DM : ℝ := 84 / 5 * ((10:ℝ) ^ 9) ^ aDM

theorem c_at_1e9 : cfam aDM c0DM M9 = 84 / 5 := by
  have hp : 0 < ((10:ℝ) ^ 9) ^ aDM := Real.rpow_pos_of_pos (by norm_num) _
  unfold cfam c0DM M9
  rw [Real.rpow_neg (by positivity)]
  field_simp

theorem R_at_1e9 : ((10:ℝ) ^ 9) ^ (1 / 3 : ℝ) = 1000 := by
  have : ((10:ℝ) ^ 9) = 1000 ^ 3 := by norm_num
  rw [this, ← Real.rpow_natCast, ← Real.rpow_mul (by norm_num)]; norm_num

theorem t_bounds : (1.2618 : ℝ) < (10:ℝ) ^ (101 / 1000 : ℝ) ∧ (10:ℝ) ^ (101 / 1000 : ℝ) < 1.2619 := by
  have hpow : ((10:ℝ) ^ (101 / 1000 : ℝ)) ^ (1000 : ℕ) = 10 ^ 101 := by
    rw [← Real.rpow_natCast, ← Real.rpow_mul (by norm_num)]
    norm_num
  have hp : 0 < (10:ℝ) ^ (101 / 1000 : ℝ) := Real.rpow_pos_of_pos (by norm_num) _
  constructor
  · by_contra h
    push Not at h
    have := pow_le_pow_left₀ hp.le h 1000
    rw [hpow] at this
    norm_num at this
  · by_contra h
    push Not at h
    have := pow_le_pow_left₀ (by norm_num) h 1000
    rw [hpow] at this
    norm_num at this

theorem u_bounds : (1.830 : ℝ) < (10:ℝ) ^ (197 / 750 : ℝ) ∧ (10:ℝ) ^ (197 / 750 : ℝ) < 1.832 := by
  have hpow : ((10:ℝ) ^ (197 / 750 : ℝ)) ^ (750 : ℕ) = 10 ^ 197 := by
    rw [← Real.rpow_natCast, ← Real.rpow_mul (by norm_num)]
    norm_num
  have hp : 0 < (10:ℝ) ^ (197 / 750 : ℝ) := Real.rpow_pos_of_pos (by norm_num) _
  constructor
  · by_contra h
    push Not at h
    have := pow_le_pow_left₀ hp.le h 750
    rw [hpow] at this
    norm_num at this
  · by_contra h
    push Not at h
    have := pow_le_pow_left₀ (by norm_num) h 750
    rw [hpow] at this
    norm_num at this

theorem c_at_1e8 : cfam aDM c0DM M8 = 84 / 5 * (10:ℝ) ^ (101 / 1000 : ℝ) := by
  unfold cfam c0DM aDM M8
  rw [Real.rpow_neg (by positivity), mul_assoc, ← div_eq_mul_inv, ← Real.div_rpow (by positivity) (by positivity)]
  norm_num

theorem c_at_1e10 : cfam aDM c0DM M10 = 84 / 5 / (10:ℝ) ^ (101 / 1000 : ℝ) := by
  unfold cfam c0DM aDM M10
  rw [Real.rpow_neg (by positivity), mul_assoc, ← div_eq_mul_inv, ← Real.div_rpow (by positivity) (by positivity)]
  have : ((10:ℝ) ^ 9 / 10 ^ 10) = (10:ℝ)⁻¹ := by norm_num
  rw [this, Real.inv_rpow (by norm_num)]
  ring

theorem c1_bounds : 21.18 < cfam aDM c0DM M8 ∧ cfam aDM c0DM M8 < 21.22 := by
  rw [c_at_1e8]
  obtain ⟨h1, h2⟩ := t_bounds
  constructor <;> nlinarith

theorem c2_bounds : 13.30 < cfam aDM c0DM M10 ∧ cfam aDM c0DM M10 < 13.32 := by
  rw [c_at_1e10]
  obtain ⟨h1, h2⟩ := t_bounds
  have hp : 0 < (10:ℝ) ^ (101 / 1000 : ℝ) := Real.rpow_pos_of_pos (by norm_num) _
  constructor
  · rw [lt_div_iff₀ hp]; nlinarith
  · rw [div_lt_iff₀ hp]; nlinarith

theorem m_c1_lo : 2.139 ≤ m 21.18 := by
  have h := log_lo (x := 22.18) (n := 3) (E := 20.0855370) (by norm_num) exp3_le
  unfold m
  norm_num at h ⊢
  linarith

theorem m_c1_hi : m 21.22 ≤ 2.152 := by
  have h := log_hi (x := 22.22) (n := 3) (E := 20.0855369) (by norm_num) (by norm_num) exp3_ge
  unfold m
  norm_num at h ⊢
  linarith

theorem m_c2_hi : m 13.32 ≤ 1.738 := by
  have h := log_hi (x := 14.32) (n := 4 * Real.log 2) (E := 16) (by norm_num) (by norm_num)
    (by rw [exp_4log2])
  have h2 := Real.log_two_lt_d9
  unfold m
  norm_num at h ⊢
  linarith

theorem m_c2_lo : 1.723 ≤ m 13.30 := by
  have h := log_lo (x := 14.30) (n := 4 * Real.log 2) (E := 16) (by norm_num) (by rw [exp_4log2])
  have h2 := Real.log_two_gt_d9
  unfold m
  norm_num at h ⊢
  linarith

/-- (4) CONCRETE COROLLARY.  With `a = 101/1000`, `c0` chosen so that `c(1e9) = 16.8`, and ANY `k > 0`
(`R200 = k M^(1/3)`; `k` cancels), the small-radius enclosed-mass coefficient satisfies
`2.25 < K(1e10)/K(1e8) < 2.29`, while `100^(1/3 - 2a) = 10^(197/750) in (1.830, 1.832)`
and the concentrations are `c(1e8) in (21.18, 21.22)`, `c(1e10) in (13.30, 13.32)`. -/
theorem debris_corollary {k : ℝ} (hk : 0 < k) :
    cfam aDM c0DM M9 = 84 / 5 ∧
    (1.830 : ℝ) < (100:ℝ) ^ (1 / 3 - 2 * aDM) ∧ (100:ℝ) ^ (1 / 3 - 2 * aDM) < 1.832 ∧
    2.25 < Kfam aDM c0DM k M10 / Kfam aDM c0DM k M8 ∧
    Kfam aDM c0DM k M10 / Kfam aDM c0DM k M8 < 2.29 := by
  have hc0 : 0 < c0DM := mul_pos (by norm_num) (Real.rpow_pos_of_pos (by norm_num) _)
  have h100 : (100:ℝ) ^ (1 / 3 - 2 * aDM) = (10:ℝ) ^ (197 / 750 : ℝ) := by
    have : (100:ℝ) = 10 ^ (2:ℝ) := by norm_num
    rw [this, ← Real.rpow_mul (by norm_num)]
    unfold aDM; congr 1; ring
  obtain ⟨u1, u2⟩ := u_bounds
  have hratio : Kfam aDM c0DM k M10 / Kfam aDM c0DM k M8 =
      (100:ℝ) ^ (1 / 3 - 2 * aDM) * (m (cfam aDM c0DM M8) / m (cfam aDM c0DM M10)) := by
    rw [Kfam_ratio hc0 hk (by unfold M8; norm_num) (by unfold M10; norm_num)]
    unfold M8 M10
    norm_num
  obtain ⟨c1a, c1b⟩ := c1_bounds
  obtain ⟨c2a, c2b⟩ := c2_bounds
  have mono := @m_strictMonoOn.monotoneOn
  have m1lo : 2.139 ≤ m (cfam aDM c0DM M8) :=
    le_trans m_c1_lo (mono (Set.mem_Ici.2 (by norm_num)) (Set.mem_Ici.2 (by linarith)) c1a.le)
  have m1hi : m (cfam aDM c0DM M8) ≤ 2.152 :=
    le_trans (mono (Set.mem_Ici.2 (by linarith)) (Set.mem_Ici.2 (by norm_num)) c1b.le) m_c1_hi
  have m2lo : 1.723 ≤ m (cfam aDM c0DM M10) :=
    le_trans m_c2_lo (mono (Set.mem_Ici.2 (by norm_num)) (Set.mem_Ici.2 (by linarith)) c2a.le)
  have m2hi : m (cfam aDM c0DM M10) ≤ 1.738 :=
    le_trans (mono (Set.mem_Ici.2 (by linarith)) (Set.mem_Ici.2 (by norm_num)) c2b.le) m_c2_hi
  refine ⟨c_at_1e9, by rw [h100]; exact u1, by rw [h100]; exact u2, ?_, ?_⟩
  · rw [hratio, h100]
    have hq : 2.139 / 1.738 ≤ m (cfam aDM c0DM M8) / m (cfam aDM c0DM M10) :=
      div_le_div₀ (by linarith) m1lo (by linarith) m2hi
    have : (1.830:ℝ) * (2.139 / 1.738) ≤ (10:ℝ) ^ (197 / 750 : ℝ) * (m (cfam aDM c0DM M8) / m (cfam aDM c0DM M10)) :=
      mul_le_mul u1.le hq (by norm_num) (by linarith)
    linarith [show (2.25:ℝ) < 1.830 * (2.139 / 1.738) by norm_num]
  · rw [hratio, h100]
    have hq : m (cfam aDM c0DM M8) / m (cfam aDM c0DM M10) ≤ 2.152 / 1.723 :=
      div_le_div₀ (by norm_num) m1hi (by norm_num) m2lo
    have hnn : 0 ≤ m (cfam aDM c0DM M8) / m (cfam aDM c0DM M10) :=
      div_nonneg (by linarith) (by linarith)
    have : (10:ℝ) ^ (197 / 750 : ℝ) * (m (cfam aDM c0DM M8) / m (cfam aDM c0DM M10)) ≤ 1.832 * (2.152 / 1.723) :=
      mul_le_mul u2.le hq hnn (by norm_num)
    linarith [show (1.832:ℝ) * (2.152 / 1.723) < 2.29 by norm_num]

/-! ### satisfiability witnesses (the hypotheses of the theorems are jointly satisfiable) -/

/-- witness: nfw_small_r_* hypotheses hold e.g. at M200 = 1, R200 = 1, c = 1. -/
example : Tendsto (fun r => nfwMass 1 1 1 r / (Kc 1 1 1 * r ^ 2)) (𝓝[>] 0) (𝓝 1) :=
  nfw_small_r_K (by norm_num) (by norm_num) (by norm_num)

/-- witness for `Kfam_bracket`: instantiated at the concrete family (a>0, c0>0, k=1, 0<M9<=M10). -/
example : ((10:ℝ) ^ 10 / 10 ^ 9) ^ (1 / 3 - 2 * aDM) ≤ Kfam aDM c0DM 1 M10 / Kfam aDM c0DM 1 M9 := by
  have hc0 : 0 < c0DM := mul_pos (by norm_num) (Real.rpow_pos_of_pos (by norm_num) _)
  have := (Kfam_bracket (a := aDM) (c0 := c0DM) (k := 1) (M1 := M9) (M2 := M10) (by unfold aDM; norm_num) hc0
    one_pos (by unfold M9; norm_num) (by unfold M9 M10; norm_num)).1
  simpa [M9, M10] using this

/-- witness: the hypotheses of `Kfam_bracket_range` (a>0, c0>0, k>0, 0<M1<=M2, c(M1), c(M2) in [5,20]) are
jointly satisfied by the concrete family a = 101/1000, c0DM, M1 = 1e9 (c = 16.8), M2 = 1e10 (c in (13.30,13.32)).
NOTE c(1e8) is in (21.18,21.22), OUTSIDE [5,20], so the M=1e8 corollary does not use the range theorem. -/
theorem range_witness : (0 : ℝ) < aDM ∧ 0 < c0DM ∧ ((0:ℝ) < M9 ∧ M9 ≤ M10) ∧
    cfam aDM c0DM M9 ∈ Set.Icc (5:ℝ) 20 ∧ cfam aDM c0DM M10 ∈ Set.Icc (5:ℝ) 20 := by
  obtain ⟨b1, b2⟩ := c2_bounds
  refine ⟨by unfold aDM; norm_num, mul_pos (by norm_num) (Real.rpow_pos_of_pos (by norm_num) _),
    ⟨by unfold M9; norm_num, by unfold M9 M10; norm_num⟩, ?_, ⟨by linarith, by linarith⟩⟩
  rw [c_at_1e9]; constructor <;> norm_num

end Cusp
