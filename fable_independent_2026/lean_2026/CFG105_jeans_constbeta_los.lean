import Mathlib

/-!
# MineM1-A: constant-anisotropy Jeans solutions for a power-law tracer, and the line-of-sight projection factor

Source lanes (committed scripts that USE these closed forms as controls, checking them numerically):
  campaign_fresh_gravity/CFG105_anisotropy_rederivation/cfg105_aniso.py  lines 293-330 (control C2 isothermal closed forms, C3 power-law halo, C3b Kepler GM/(4r))
  campaign_fresh_gravity/CFG106_slope_beta_box_rederivation/cfg106_box.py lines 246-275 (docstring + controls C1-C4 closed-form checks: Kepler sigma_r^2 = GM/((gamma+1-2beta) r),
      flat curve sigma_r^2 = v^2/(gamma-2beta), sigma_los^2 = v^2 (gamma - beta (gamma-1))/(gamma (gamma-2beta)))

CERTIFIED (premises => conclusions; pure mathematics, no data):
* For nu = r^(-gamma), g = A r^(-p), constant beta and D := gamma + p - 1 - 2 beta != 0, the power-law
  nu sigma_r^2 = A r^(1-p-gamma)/D solves the Jeans equation  d(nu s^2)/dr + 2 beta nu s^2 / r = -nu g  at every r > 0 (`flux_jeans`, `flux_jeans'`).
* It is positive iff (A > 0 and) D > 0, and obeys the outer boundary condition r^(2 beta) nu sigma^2 -> 0 exactly when D > 0 (`flux_boundary`).
* UNIQUENESS: any other solution of the same equation with r^(2 beta) f -> 0 at infinity coincides with it on (0, infinity) (`jeans_unique`, `flux_unique_solution`).
* Special cases: isothermal (p = 1, A = v^2): sigma_r^2 = v^2/(gamma - 2 beta) (`sigr2_isothermal`);  point mass (p = 2, A = GM):
  sigma_r^2 = GM/((gamma + 1 - 2 beta) r) (`sigr2_kepler`).
* The Binney-Mamon projection with r = R cosh u (dz = r du): for constant sigma_r and gamma > 1,
  int (1 - beta R^2/r^2) nu r du = (1 - beta (gamma-1)/gamma) int nu r du   (`los_projection`), proved from the integration-by-parts recurrence
  (a+1) I(a+2) = a I(a) for I(a) = int_0^infty cosh^(-a) (`cosh_ibp`), with integrability and positivity proved (not assumed).
  Hence sigma_los^2 / v^2 = (gamma - beta(gamma-1)) / (gamma (gamma - 2 beta)) for the isothermal sphere (`los_isothermal`).

NOT certified: that any real system has a power-law tracer, constant beta, or an isothermal/Keplerian potential; any SLUGGS/GC number
or sigma-offset (empirical, numerical in CFG105/106); the Osipkov-Merritt attack (beta varies; not treated); the Gamma-function form of the
Kepler line-of-sight profile (only its reduction through `cosh_ibp` is here).  kappa = 1/2 is FITTED; nothing here says the theory is closed.
-/

open MeasureTheory Set Filter Topology Real

namespace MineM1

lemma cosh_ge (u : ℝ) : Real.exp u / 2 ≤ Real.cosh u := by
  rw [Real.cosh_eq]
  have : 0 ≤ Real.exp (-u) := (Real.exp_pos _).le
  linarith

lemma cosh_tendsto : Tendsto Real.cosh atTop atTop := by
  refine tendsto_atTop_mono cosh_ge ?_
  exact (Real.tendsto_exp_atTop.atTop_div_const (by norm_num : (0:ℝ) < 2))

lemma cosh_rpow_neg_le {a : ℝ} (ha : 0 < a) (u : ℝ) :
    Real.cosh u ^ (-a) ≤ 2 ^ a * Real.exp (-a * u) := by
  have hc : 0 < Real.cosh u := Real.cosh_pos u
  have h1 : Real.exp u / 2 ≤ Real.cosh u := cosh_ge u
  have h2 : 0 < Real.exp u / 2 := by positivity
  have h3 : Real.cosh u ^ (-a) ≤ (Real.exp u / 2) ^ (-a) :=
    Real.rpow_le_rpow_of_nonpos h2 h1 (by linarith)
  refine h3.trans (le_of_eq ?_)
  rw [Real.div_rpow (Real.exp_pos u).le (by norm_num), ← Real.exp_mul, Real.rpow_neg (by norm_num : (0:ℝ) ≤ 2)]
  field_simp

lemma cosh_rpow_integrable {a : ℝ} (ha : 0 < a) :
    IntegrableOn (fun u : ℝ => Real.cosh u ^ (-a)) (Ioi 0) := by
  have hint : IntegrableOn (fun u : ℝ => 2 ^ a * Real.exp (-a * u)) (Ioi 0) :=
    (exp_neg_integrableOn_Ioi 0 ha).const_mul _
  refine Integrable.mono' hint ?_ ?_
  · exact (Continuous.rpow_const Real.continuous_cosh (fun x => Or.inl (Real.cosh_pos x).ne')).aestronglyMeasurable
  · refine (ae_restrict_iff' measurableSet_Ioi).2 (Filter.Eventually.of_forall fun u _ => ?_)
    rw [Real.norm_eq_abs, abs_of_pos (Real.rpow_pos_of_pos (Real.cosh_pos u) _)]
    exact cosh_rpow_neg_le ha u


lemma cosh_pow_shift (c : ℝ) (hc : 0 < c) (a : ℝ) :
    c ^ (-(a + 1)) = c * c ^ (-(a + 2)) ∧ c ^ (-a) = c ^ 2 * c ^ (-(a + 2)) := by
  constructor
  · have : -(a + 1) = -(a + 2) + 1 := by ring
    rw [this, Real.rpow_add_one hc.ne']; ring
  · have : -a = -(a + 2) + 2 := by ring
    rw [this, Real.rpow_add hc]; norm_num; ring

lemma cosh_ibp_deriv {a : ℝ} (u : ℝ) :
    HasDerivAt (fun u : ℝ => Real.sinh u * Real.cosh u ^ (-(a + 1)))
      (-a * Real.cosh u ^ (-a) + (a + 1) * Real.cosh u ^ (-(a + 2))) u := by
  have hc := Real.cosh_pos u
  have h1 : HasDerivAt (fun u : ℝ => Real.cosh u ^ (-(a + 1)))
      (Real.sinh u * (-(a + 1)) * Real.cosh u ^ (-(a + 1) - 1)) u :=
    (Real.hasDerivAt_cosh u).rpow_const (Or.inl hc.ne')
  have h2 := (Real.hasDerivAt_sinh u).mul h1
  refine h2.congr_deriv ?_
  have e1 : -(a + 1) - 1 = -(a + 2) := by ring
  rw [e1]
  obtain ⟨s1, s2⟩ := cosh_pow_shift (Real.cosh u) hc a
  rw [s1, s2]
  have hs : Real.sinh u ^ 2 = Real.cosh u ^ 2 - 1 := by nlinarith [Real.cosh_sq u]
  have : Real.sinh u * (Real.sinh u * (-(a + 1)) * Real.cosh u ^ (-(a + 2))) = -(a+1) * (Real.sinh u ^ 2) * Real.cosh u ^ (-(a + 2)) := by ring
  rw [this, hs]; ring

theorem cosh_ibp {a : ℝ} (ha : 0 < a) :
    (a + 1) * ∫ u in Ioi (0:ℝ), Real.cosh u ^ (-(a + 2)) = a * ∫ u in Ioi (0:ℝ), Real.cosh u ^ (-a) := by
  have i1 := cosh_rpow_integrable ha
  have i2 := cosh_rpow_integrable (by linarith : 0 < a + 2)
  have hint : IntegrableOn (fun u : ℝ => -a * Real.cosh u ^ (-a) + (a + 1) * Real.cosh u ^ (-(a + 2))) (Ioi 0) :=
    (i1.const_mul (-a)).add (i2.const_mul (a + 1))
  have hlim : Tendsto (fun u : ℝ => Real.sinh u * Real.cosh u ^ (-(a + 1))) atTop (𝓝 0) := by
    have hb : Tendsto (fun u : ℝ => Real.cosh u ^ (-a)) atTop (𝓝 0) :=
      (tendsto_rpow_neg_atTop ha).comp cosh_tendsto
    refine squeeze_zero' ?_ ?_ hb
    · filter_upwards [eventually_ge_atTop (0:ℝ)] with u hu
      exact mul_nonneg (Real.sinh_nonneg_iff.2 hu) (Real.rpow_nonneg (Real.cosh_pos u).le _)
    · filter_upwards with u
      obtain ⟨s1, _⟩ := cosh_pow_shift (Real.cosh u) (Real.cosh_pos u) a
      have hc := Real.cosh_pos u
      have ht : 0 ≤ Real.cosh u ^ (-(a + 2)) := Real.rpow_nonneg hc.le _
      obtain ⟨_, s2⟩ := cosh_pow_shift (Real.cosh u) hc a
      rw [s1, s2]
      have : Real.sinh u ≤ Real.cosh u := (Real.sinh_lt_cosh u).le
      nlinarith [mul_nonneg ht hc.le]
  have hcont : ContinuousWithinAt (fun u : ℝ => Real.sinh u * Real.cosh u ^ (-(a + 1))) (Ici 0) 0 :=
    (Real.continuous_sinh.mul (Continuous.rpow_const Real.continuous_cosh
      (fun x => Or.inl (Real.cosh_pos x).ne'))).continuousWithinAt
  have key := integral_Ioi_of_hasDerivAt_of_tendsto hcont (fun u _ => cosh_ibp_deriv u) hint hlim
  simp only [Real.sinh_zero, zero_mul, sub_zero] at key
  rw [integral_add (i1.const_mul (-a)) (i2.const_mul (a + 1)), integral_const_mul, integral_const_mul] at key
  linarith

/-- nu * sigma_r^2 for the power-law solution: nu = r^(-gamma), g = A r^(-p), constant beta. -/
noncomputable def flux (A p γ β r : ℝ) : ℝ := A * r ^ (1 - p - γ) / (γ + p - 1 - 2 * β)

/-- sigma_r^2 for the same solution. -/
noncomputable def sigr2 (A p γ β r : ℝ) : ℝ := A * r ^ (1 - p) / (γ + p - 1 - 2 * β)

lemma rpow_aux {r : ℝ} (hr : 0 < r) (p γ : ℝ) :
    r ^ (-γ) * r ^ (-p) = r ^ (1 - p - γ - 1) ∧ r ^ (1 - p - γ) = r * r ^ (1 - p - γ - 1) := by
  constructor
  · rw [← Real.rpow_add hr]; congr 1; ring
  · rw [Real.rpow_sub_one hr.ne']; field_simp

theorem flux_jeans {A p γ β : ℝ} (hD : γ + p - 1 - 2 * β ≠ 0) {r : ℝ} (hr : 0 < r) :
    HasDerivAt (flux A p γ β)
      (-(r ^ (-γ) * (A * r ^ (-p))) - 2 * β * flux A p γ β r / r) r := by
  have h0 : HasDerivAt (fun y : ℝ => y ^ (1 - p - γ)) (1 * (1 - p - γ) * r ^ (1 - p - γ - 1)) r :=
    (hasDerivAt_id r).rpow_const (Or.inl hr.ne')
  have h1 := (h0.const_mul A).div_const (γ + p - 1 - 2 * β)
  refine h1.congr_deriv ?_
  obtain ⟨e1, e2⟩ := rpow_aux hr p γ
  unfold flux
  have e1' : r ^ (-γ) * (A * r ^ (-p)) = A * r ^ (1 - p - γ - 1) := by rw [← e1]; ring
  rw [e1', e2]
  field_simp
  ring

/-- the Jeans equation, d(nu s^2)/dr + 2 beta nu s^2 / r = -nu g, as a statement about derivatives -/
theorem flux_jeans' {A p γ β : ℝ} (hD : γ + p - 1 - 2 * β ≠ 0) {r : ℝ} (hr : 0 < r) :
    deriv (flux A p γ β) r + 2 * β * flux A p γ β r / r = -(r ^ (-γ) * (A * r ^ (-p))) := by
  rw [(flux_jeans hD hr).deriv]; ring

theorem sigr2_eq {A p γ β : ℝ} {r : ℝ} (hr : 0 < r) :
    sigr2 A p γ β r = flux A p γ β r / r ^ (-γ) := by
  unfold sigr2 flux
  have hpos : r ^ (-γ) ≠ 0 := (Real.rpow_pos_of_pos hr _).ne'
  have : r ^ (1 - p - γ) = r ^ (1 - p) * r ^ (-γ) := by
    rw [← Real.rpow_add hr]; congr 1
  rw [this]; field_simp

/-- isothermal sphere (g = v^2 / r, p = 1): sigma_r^2 = v^2 / (gamma - 2 beta) at every radius -/
theorem sigr2_isothermal {v γ β : ℝ} {r : ℝ} (_hr : 0 < r) :
    sigr2 (v ^ 2) 1 γ β r = v ^ 2 / (γ - 2 * β) := by
  unfold sigr2
  have : γ + 1 - 1 - 2 * β = γ - 2 * β := by ring
  rw [this]; simp

/-- point mass (g = G M / r^2, p = 2): sigma_r^2 = G M / ((gamma + 1 - 2 beta) r) -/
theorem sigr2_kepler {GM γ β : ℝ} {r : ℝ} (hr : 0 < r) :
    sigr2 GM 2 γ β r = GM / ((γ + 1 - 2 * β) * r) := by
  unfold sigr2
  have h1 : γ + 2 - 1 - 2 * β = γ + 1 - 2 * β := by ring
  have h2 : r ^ (1 - (2:ℝ)) = r⁻¹ := by
    rw [show (1 - (2:ℝ)) = -1 by norm_num, Real.rpow_neg_one]
  rw [h1, h2]
  by_cases hd : γ + 1 - 2 * β = 0
  · simp [hd]
  · field_simp

/-- positivity: gamma + p - 1 - 2 beta > 0 and A > 0 give a positive dispersion -/
theorem sigr2_pos {A p γ β : ℝ} (hA : 0 < A) (hD : 0 < γ + p - 1 - 2 * β) {r : ℝ} (hr : 0 < r) :
    0 < sigr2 A p γ β r := by
  unfold sigr2
  exact div_pos (mul_pos hA (Real.rpow_pos_of_pos hr _)) hD

/-- the particular solution obeys the outer boundary condition r^(2 beta) nu sigma^2 -> 0 exactly when D > 0 -/
theorem flux_boundary {A p γ β : ℝ} (hD : 0 < γ + p - 1 - 2 * β) :
    Tendsto (fun r : ℝ => r ^ (2 * β) * flux A p γ β r) atTop (𝓝 0) := by
  have h1 : Tendsto (fun r : ℝ => r ^ (-(γ + p - 1 - 2 * β))) atTop (𝓝 0) := tendsto_rpow_neg_atTop hD
  have h2 := h1.const_mul (A / (γ + p - 1 - 2 * β))
  rw [mul_zero] at h2
  refine h2.congr' ?_
  filter_upwards [eventually_gt_atTop (0:ℝ)] with r hr
  unfold flux
  have : r ^ (2 * β) * r ^ (1 - p - γ) = r ^ (-(γ + p - 1 - 2 * β)) := by
    rw [← Real.rpow_add hr]; congr 1; ring
  rw [show r ^ (2 * β) * (A * r ^ (1 - p - γ) / (γ + p - 1 - 2 * β))
      = A / (γ + p - 1 - 2 * β) * (r ^ (2 * β) * r ^ (1 - p - γ)) by ring, this]

/-- UNIQUENESS: two solutions of the Jeans equation with the same nu g that both obey r^(2 beta) f -> 0 at infinity coincide. -/
theorem jeans_unique {β : ℝ} {src f₁ f₂ : ℝ → ℝ}
    (h₁ : ∀ r, 0 < r → HasDerivAt f₁ (-src r - 2 * β * f₁ r / r) r)
    (h₂ : ∀ r, 0 < r → HasDerivAt f₂ (-src r - 2 * β * f₂ r / r) r)
    (b₁ : Tendsto (fun r : ℝ => r ^ (2 * β) * f₁ r) atTop (𝓝 0))
    (b₂ : Tendsto (fun r : ℝ => r ^ (2 * β) * f₂ r) atTop (𝓝 0)) :
    ∀ r, 0 < r → f₁ r = f₂ r := by
  set h : ℝ → ℝ := fun r => r ^ (2 * β) * (f₁ r - f₂ r) with hh
  have hd : ∀ r, 0 < r → HasDerivAt h 0 r := by
    intro r hr
    have hp : HasDerivAt (fun y : ℝ => y ^ (2 * β)) (1 * (2 * β) * r ^ (2 * β - 1)) r :=
      (hasDerivAt_id r).rpow_const (Or.inl hr.ne')
    have := hp.mul ((h₁ r hr).sub (h₂ r hr))
    refine this.congr_deriv ?_
    rw [Real.rpow_sub_one hr.ne']
    simp only [Pi.sub_apply]
    field_simp
    ring
  have hconst : ∀ x ∈ Ioi (0:ℝ), ∀ y ∈ Ioi (0:ℝ), h x = h y := by
    intro x hx y hy
    exact isOpen_Ioi.is_const_of_deriv_eq_zero (isPreconnected_Ioi)
      (fun z hz => (hd z hz).differentiableAt.differentiableWithinAt)
      (fun z hz => (hd z hz).deriv) hx hy
  have hlim : Tendsto h atTop (𝓝 0) := by
    have := b₁.sub b₂
    rw [sub_zero] at this
    refine this.congr' (Filter.Eventually.of_forall fun r => ?_)
    simp only [hh, mul_sub]
  intro r hr
  have hc : ∀ y ∈ Ioi (0:ℝ), h y = h r := fun y hy => hconst y hy r hr
  have hev : (fun y => h y) =ᶠ[atTop] fun _ => h r := by
    filter_upwards [eventually_gt_atTop (0:ℝ)] with y hy using hc y hy
  have := tendsto_nhds_unique (hlim.congr' hev) tendsto_const_nhds
  have hz : h r = 0 := this.symm
  simp only [hh] at hz
  have hpos : r ^ (2 * β) ≠ 0 := (Real.rpow_pos_of_pos hr _).ne'
  have := (mul_eq_zero.1 hz).resolve_left hpos
  linarith

/-- Consequently the power-law flux is THE decaying solution when D > 0. -/
theorem flux_unique_solution {A p γ β : ℝ} (hD : 0 < γ + p - 1 - 2 * β) {f : ℝ → ℝ}
    (hf : ∀ r, 0 < r → HasDerivAt f (-(r ^ (-γ) * (A * r ^ (-p))) - 2 * β * f r / r) r)
    (hb : Tendsto (fun r : ℝ => r ^ (2 * β) * f r) atTop (𝓝 0)) :
    ∀ r, 0 < r → f r = flux A p γ β r :=
  jeans_unique hf (fun _ hr => flux_jeans hD.ne' hr) hb (flux_boundary hD)

lemma cosh_rpow_int_pos {a : ℝ} (ha : 0 < a) : 0 < ∫ u in Ioi (0:ℝ), Real.cosh u ^ (-a) := by
  have hi := cosh_rpow_integrable ha
  rw [integral_pos_iff_support_of_nonneg (fun u => Real.rpow_nonneg (Real.cosh_pos u).le _) hi]
  have : Function.support (fun u : ℝ => Real.cosh u ^ (-a)) = Set.univ := by
    ext u; simp [Function.mem_support, (Real.rpow_pos_of_pos (Real.cosh_pos u) _).ne']
  rw [this]; simp

/-- Line-of-sight projection of a constant radial dispersion (Binney-Mamon, r = R cosh u, dz = r du), nu = r^(-gamma), gamma > 1. -/
theorem los_projection {R γ β : ℝ} (hR : 0 < R) (hγ : 1 < γ) :
    ∫ u in Ioi (0:ℝ), (1 - β * R ^ 2 / (R * Real.cosh u) ^ 2) * ((R * Real.cosh u) ^ (-γ) * (R * Real.cosh u))
      = (1 - β * (γ - 1) / γ) * ∫ u in Ioi (0:ℝ), ((R * Real.cosh u) ^ (-γ) * (R * Real.cosh u)) := by
  set a := γ - 1 with ha
  have hapos : 0 < a := by linarith
  have hw : ∀ u : ℝ, (R * Real.cosh u) ^ (-γ) * (R * Real.cosh u) = R ^ (-a) * Real.cosh u ^ (-a) := by
    intro u
    have hc := Real.cosh_pos u
    rw [Real.mul_rpow hR.le hc.le]
    have h1 : R ^ (-γ) * R = R ^ (-a) := by
      rw [show -γ = -a - 1 by rw [ha]; ring, Real.rpow_sub_one hR.ne']; field_simp
    have h2 : Real.cosh u ^ (-γ) * Real.cosh u = Real.cosh u ^ (-a) := by
      rw [show -γ = -a - 1 by rw [ha]; ring, Real.rpow_sub_one hc.ne']; field_simp
    calc R ^ (-γ) * Real.cosh u ^ (-γ) * (R * Real.cosh u)
        = (R ^ (-γ) * R) * (Real.cosh u ^ (-γ) * Real.cosh u) := by ring
      _ = _ := by rw [h1, h2]
  have hw2 : ∀ u : ℝ, (1 - β * R ^ 2 / (R * Real.cosh u) ^ 2) * ((R * Real.cosh u) ^ (-γ) * (R * Real.cosh u))
      = R ^ (-a) * (Real.cosh u ^ (-a) - β * Real.cosh u ^ (-(a + 2))) := by
    intro u
    have hc := Real.cosh_pos u
    rw [hw u]
    have : Real.cosh u ^ (-(a + 2)) = Real.cosh u ^ (-a) / Real.cosh u ^ 2 := by
      rw [show -(a + 2) = -a - 2 by ring, Real.rpow_sub hc]; norm_num
    rw [this]
    field_simp
  simp_rw [hw2, hw]
  have i1 := cosh_rpow_integrable hapos
  have i2 := cosh_rpow_integrable (by linarith : 0 < a + 2)
  rw [integral_const_mul, integral_const_mul, integral_sub i1 (i2.const_mul β), integral_const_mul]
  have key := cosh_ibp hapos
  have hγ0 : γ ≠ 0 := by linarith
  have e : a + 1 = γ := by rw [ha]; ring
  rw [e] at key
  have : ∫ u in Ioi (0:ℝ), Real.cosh u ^ (-(a + 2)) = a / γ * ∫ u in Ioi (0:ℝ), Real.cosh u ^ (-a) := by
    field_simp; linarith
  rw [this]; ring


/-- isothermal sphere, line of sight: sigma_los^2 / v^2 = (gamma - beta (gamma - 1)) / (gamma (gamma - 2 beta)) -/
theorem los_isothermal {R γ β v : ℝ} (hR : 0 < R) (hγ : 1 < γ) (hd : γ - 2 * β ≠ 0) :
    (∫ u in Ioi (0:ℝ), (1 - β * R ^ 2 / (R * Real.cosh u) ^ 2)
        * ((R * Real.cosh u) ^ (-γ) * (v ^ 2 / (γ - 2 * β)) * (R * Real.cosh u)))
      / (∫ u in Ioi (0:ℝ), ((R * Real.cosh u) ^ (-γ) * (R * Real.cosh u)))
    = v ^ 2 * (γ - β * (γ - 1)) / (γ * (γ - 2 * β)) := by
  have hγ0 : γ ≠ 0 := by linarith
  have hden : 0 < ∫ u in Ioi (0:ℝ), ((R * Real.cosh u) ^ (-γ) * (R * Real.cosh u)) := by
    have hw : ∀ u : ℝ, (R * Real.cosh u) ^ (-γ) * (R * Real.cosh u) = R ^ (-(γ - 1)) * Real.cosh u ^ (-(γ - 1)) := by
      intro u
      have hc := Real.cosh_pos u
      rw [Real.mul_rpow hR.le hc.le]
      have h1 : R ^ (-γ) * R = R ^ (-(γ - 1)) := by
        rw [show -γ = -(γ - 1) - 1 by ring, Real.rpow_sub_one hR.ne']; field_simp
      have h2 : Real.cosh u ^ (-γ) * Real.cosh u = Real.cosh u ^ (-(γ - 1)) := by
        rw [show -γ = -(γ - 1) - 1 by ring, Real.rpow_sub_one hc.ne']; field_simp
      calc R ^ (-γ) * Real.cosh u ^ (-γ) * (R * Real.cosh u)
          = (R ^ (-γ) * R) * (Real.cosh u ^ (-γ) * Real.cosh u) := by ring
        _ = _ := by rw [h1, h2]
    simp_rw [hw]
    rw [integral_const_mul]
    exact mul_pos (Real.rpow_pos_of_pos hR _) (cosh_rpow_int_pos (by linarith))
  have hnum : (∫ u in Ioi (0:ℝ), (1 - β * R ^ 2 / (R * Real.cosh u) ^ 2)
        * ((R * Real.cosh u) ^ (-γ) * (v ^ 2 / (γ - 2 * β)) * (R * Real.cosh u)))
      = v ^ 2 / (γ - 2 * β) * ∫ u in Ioi (0:ℝ), (1 - β * R ^ 2 / (R * Real.cosh u) ^ 2)
        * ((R * Real.cosh u) ^ (-γ) * (R * Real.cosh u)) := by
    rw [← integral_const_mul]
    congr 1; ext u; ring
  rw [hnum, los_projection hR hγ]
  generalize (∫ u in Ioi (0:ℝ), ((R * Real.cosh u) ^ (-γ) * (R * Real.cosh u))) = I at hden ⊢
  field_simp

end MineM1

open MineM1 in
#print axioms flux_jeans
open MineM1 in
#print axioms flux_unique_solution
open MineM1 in
#print axioms sigr2_isothermal
open MineM1 in
#print axioms sigr2_kepler
open MineM1 in
#print axioms cosh_ibp
open MineM1 in
#print axioms los_projection
open MineM1 in
#print axioms los_isothermal
