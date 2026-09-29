import Mathlib

/-!
# EQB_S7 -- closed forms of the y_c = Z/2 throttle ("broken RAR") (Lean 4 certificate)

Source (committed): `prep_2026/equation_book/s7_throttle_closed_form.py`, checks E-S7-1 (kink = pure-Lambda landmark, lines 57-77),
E-S7-2 (cubic invariant, lines 81-90), E-S7-3 (a0-line saturation, lines 94-111), E-S7-4 (slope break, lines 115-140);
write-up `prep_2026/equation_book/MINE_M2.md` item 4.

PREMISES (declared, NOT certified as physics; the script flags them POSTULATE-DEPENDENT, Branch B only):
    g_obs = g_bar [1 + (nu(y) - 1) T(y)],   nu(y) = sqrt(1 + 1/y),   y = g_bar/a0,
    T(y) = min(1, (y_c/y)^n) with y_c = Z/2;  above the kink (y > y_c) T = (y_c/y)^n.
Nothing here says the throttle is realised in nature (the script reports it is not currently detectable).  The theorems below use
an arbitrary y_c > 0 (or Z > 0 with y_c = Z/2); they do not use Z = sqrt(32 pi/3), nor kappa = 1/2 (FITTED).

CERTIFIED (premises => conclusions):
  * `throttle_cubic`   : (n = 1, y > 0) g_bar * D * (D + Z a0) = (Z^2/4) a0^3 with D = g_obs - g_bar   (y-independent invariant)
  * `throttle_general` : g_bar^n (g_obs - g_bar) = a0^(n+1) y_c^n / (nu(y) + 1), exactly, for every natural n
  * `throttle_continuous_at_kink` : the above-kink branch meets the isolated law sqrt(g^2 + a0 g) at y = y_c
  * `saturation`       : g_obs^2 - g_bar^2 -> a0^2 y_c as y -> infinity (= (Z/2) a0^2 = a0 g_kink for y_c = Z/2); and the
                         general-n limit of g_bar^n (g_obs - g_bar) is a0^(n+1) y_c^n / 2
  * `above_hasDeriv`   : d g_obs / d y = a0 (1 - y_c/(2 y^2 nu(y))) above the kink (n = 1)
  * `slope_break`      : the log-log slope just above the kink is (1 - 1/(Z nu_c))/nu_c with nu_c = sqrt(1 + 2/Z); the break
                         Delta = slope(+) - slope(-) = 1/nu_c - 1 = sqrt(Z/(Z+2)) - 1 < 0 exactly (slope(-) = (Z+1)/(Z+2)).
  * `kink_lambda`      : with a0 = c H/Z and H = c sqrt(Lambda/3): g_kink = (Z/2) a0 = c H/2 = c^2 sqrt(Lambda/12) (Z cancels),
                         and Lambda = 12 g_kink^2 / c^4
NOT certified: the throttle itself (its T(y) is a Branch-B postulate); the numerical break values (-0.1379 for Z = sqrt(32 pi/3), n = 1;
n = 2 and the peak-deviation landmark y* = 6.06 are numeric roots in the script); detectability; the Hernquist kink radius (a model).
-/

open Real Filter Topology

noncomputable section

/-- nu(y) = sqrt(1 + 1/y). -/
def nuQ (y : ℝ) : ℝ := Real.sqrt (1 + 1 / y)

/-- the throttled observed field above the kink, exponent n: g_obs = g (1 + (nu - 1) (y_c / y)^n), g = a0 y. -/
def gAbove (a0 yc : ℝ) (n : ℕ) (y : ℝ) : ℝ := a0 * y * (1 + (nuQ y - 1) * (yc / y) ^ n)

theorem nuQ_sq {y : ℝ} (hy : 0 < y) : nuQ y ^ 2 = 1 + 1 / y := by
  unfold nuQ; exact Real.sq_sqrt (by positivity)

theorem nuQ_pos {y : ℝ} (hy : 0 < y) : 0 < nuQ y := by
  unfold nuQ; exact Real.sqrt_pos.mpr (by positivity)

theorem nuQ_gt_one {y : ℝ} (hy : 0 < y) : 1 < nuQ y := by
  have h := nuQ_sq hy
  have h0 := nuQ_pos hy
  have : 0 < 1 / y := by positivity
  nlinarith

/-- y (nu - 1)(nu + 1) = 1. -/
theorem y_nu_identity {y : ℝ} (hy : 0 < y) : y * (nuQ y - 1) * (nuQ y + 1) = 1 := by
  have h := nuQ_sq hy
  have : y * (nuQ y ^ 2 - 1) = 1 := by rw [h]; field_simp; ring
  linarith

theorem y_nu_eq {y : ℝ} (hy : 0 < y) : y * (nuQ y - 1) = 1 / (nuQ y + 1) := by
  have h := y_nu_identity hy
  have : nuQ y + 1 ≠ 0 := by have := nuQ_pos hy; positivity
  field_simp
  linarith

theorem gAbove_one {a0 yc y : ℝ} (hy : 0 < y) :
    gAbove a0 yc 1 y = a0 * (y + yc * (nuQ y - 1)) := by
  unfold gAbove; field_simp

theorem throttle_cubic {a0 Z y : ℝ} (hy : 0 < y) :
    (a0 * y) * (gAbove a0 (Z / 2) 1 y - a0 * y) * ((gAbove a0 (Z / 2) 1 y - a0 * y) + Z * a0)
      = Z ^ 2 / 4 * a0 ^ 3 := by
  rw [gAbove_one hy]
  have h := y_nu_identity hy
  have : (a0 * y) * (a0 * (y + Z / 2 * (nuQ y - 1)) - a0 * y)
      * ((a0 * (y + Z / 2 * (nuQ y - 1)) - a0 * y) + Z * a0)
      = a0 ^ 3 * (Z / 2) ^ 2 * (y * (nuQ y - 1) * (nuQ y + 1)) := by ring
  rw [this, h]; ring

theorem throttle_general {a0 yc y : ℝ} (n : ℕ) (hy : 0 < y) :
    (a0 * y) ^ n * (gAbove a0 yc n y - a0 * y) = a0 ^ (n + 1) * yc ^ n / (nuQ y + 1) := by
  have h := y_nu_eq hy
  have hy0 : y ≠ 0 := hy.ne'
  have hn : nuQ y + 1 ≠ 0 := by have := nuQ_pos hy; positivity
  have e : (a0 * y) ^ n * (gAbove a0 yc n y - a0 * y)
      = a0 ^ (n + 1) * yc ^ n * (y * (nuQ y - 1)) := by
    unfold gAbove
    rw [mul_pow, div_pow, pow_succ]
    field_simp
    ring
  rw [e, h]; field_simp

theorem throttle_continuous_at_kink {a0 yc : ℝ} (hyc : 0 < yc) :
    gAbove a0 yc 1 yc = a0 * Real.sqrt (yc ^ 2 + yc) := by
  rw [gAbove_one hyc]
  unfold nuQ
  have : Real.sqrt (yc ^ 2 + yc) = yc * Real.sqrt (1 + 1 / yc) := by
    have h1 : yc ^ 2 + yc = yc ^ 2 * (1 + 1 / yc) := by field_simp
    rw [h1, Real.sqrt_mul (by positivity), Real.sqrt_sq hyc.le]
  rw [this]; ring

theorem nuQ_tendsto : Tendsto nuQ atTop (𝓝 1) := by
  have h1 : Tendsto (fun y : ℝ => 1 + 1 / y) atTop (𝓝 1) := by
    have := (tendsto_const_nhds (x := (1 : ℝ))).div_atTop (tendsto_id : Tendsto (fun y : ℝ => y) atTop atTop)
    simpa using tendsto_const_nhds.add this
  have h2 := (Real.continuous_sqrt.tendsto 1).comp h1
  have e : nuQ = (fun x : ℝ => Real.sqrt x) ∘ (fun y : ℝ => 1 + 1 / y) := rfl
  rw [e]
  rwa [Real.sqrt_one] at h2

theorem saturation {a0 yc : ℝ} :
    Tendsto (fun y : ℝ => gAbove a0 yc 1 y ^ 2 - (a0 * y) ^ 2) atTop (𝓝 (a0 ^ 2 * yc)) := by
  have hexp : ∀ᶠ y in atTop, gAbove a0 yc 1 y ^ 2 - (a0 * y) ^ 2
      = a0 ^ 2 * yc * (2 / (nuQ y + 1) + yc * (nuQ y - 1) ^ 2) := by
    filter_upwards [eventually_gt_atTop (0 : ℝ)] with y hy
    rw [gAbove_one hy]
    have h := y_nu_eq hy
    have : (a0 * (y + yc * (nuQ y - 1))) ^ 2 - (a0 * y) ^ 2
        = a0 ^ 2 * yc * (2 * (y * (nuQ y - 1)) + yc * (nuQ y - 1) ^ 2) := by ring
    rw [this, h]; ring
  have hlim : Tendsto (fun y : ℝ => a0 ^ 2 * yc * (2 / (nuQ y + 1) + yc * (nuQ y - 1) ^ 2))
      atTop (𝓝 (a0 ^ 2 * yc * (2 / (1 + 1) + yc * (1 - 1) ^ 2))) := by
    have h1 := nuQ_tendsto
    have h2 : Tendsto (fun y : ℝ => 2 / (nuQ y + 1)) atTop (𝓝 (2 / (1 + 1))) :=
      tendsto_const_nhds.div (h1.add_const 1) (by norm_num)
    have h3 : Tendsto (fun y : ℝ => yc * (nuQ y - 1) ^ 2) atTop (𝓝 (yc * (1 - 1) ^ 2)) :=
      tendsto_const_nhds.mul ((h1.sub_const 1).pow 2)
    exact tendsto_const_nhds.mul (h2.add h3)
  have hval : a0 ^ 2 * yc * (2 / (1 + 1) + yc * (1 - 1) ^ 2) = a0 ^ 2 * yc := by ring
  rw [hval] at hlim
  exact hlim.congr' (hexp.mono fun y hy => hy.symm)

theorem saturation_general {a0 yc : ℝ} (n : ℕ) :
    Tendsto (fun y : ℝ => (a0 * y) ^ n * (gAbove a0 yc n y - a0 * y)) atTop
      (𝓝 (a0 ^ (n + 1) * yc ^ n / 2)) := by
  have hexp : ∀ᶠ y in atTop, (a0 * y) ^ n * (gAbove a0 yc n y - a0 * y)
      = a0 ^ (n + 1) * yc ^ n / (nuQ y + 1) := by
    filter_upwards [eventually_gt_atTop (0 : ℝ)] with y hy
    exact throttle_general n hy
  have hlim : Tendsto (fun y : ℝ => a0 ^ (n + 1) * yc ^ n / (nuQ y + 1)) atTop
      (𝓝 (a0 ^ (n + 1) * yc ^ n / (1 + 1))) :=
    tendsto_const_nhds.div (nuQ_tendsto.add_const 1) (by norm_num)
  have hval : a0 ^ (n + 1) * yc ^ n / (1 + 1) = a0 ^ (n + 1) * yc ^ n / 2 := by norm_num
  rw [hval] at hlim
  exact hlim.congr' (hexp.mono fun y hy => hy.symm)

theorem nuQ_hasDeriv {y : ℝ} (hy : 0 < y) :
    HasDerivAt nuQ (-1 / (2 * y ^ 2 * nuQ y)) y := by
  have hy0 : y ≠ 0 := hy.ne'
  have h1 : HasDerivAt (fun t : ℝ => 1 + 1 / t) (-(1 / y ^ 2)) y := by
    have := (hasDerivAt_inv hy0).const_add 1
    simpa [one_div] using this
  have hpos : 0 < 1 + 1 / y := by positivity
  have h2 := h1.sqrt hpos.ne'
  unfold nuQ
  refine h2.congr_deriv ?_
  have hn := nuQ_pos hy
  unfold nuQ at hn
  field_simp

theorem above_hasDeriv {a0 yc y : ℝ} (hy : 0 < y) :
    HasDerivAt (fun t : ℝ => a0 * (t + yc * (nuQ t - 1)))
      (a0 * (1 - yc / (2 * y ^ 2 * nuQ y))) y := by
  have h := ((hasDerivAt_id y).add (((nuQ_hasDeriv hy).sub_const 1).const_mul yc)).const_mul a0
  refine h.congr_deriv ?_
  field_simp
  ring

/-- the slope just above the kink and the exact break. -/
def slopeAbove (Z : ℝ) : ℝ := (1 - 1 / (Z * Real.sqrt (1 + 2 / Z))) / Real.sqrt (1 + 2 / Z)

theorem slope_above_at_kink {a0 Z : ℝ} (ha : 0 < a0) (hZ : 0 < Z) :
    (Z / 2) * (a0 * (1 - (Z / 2) / (2 * (Z / 2) ^ 2 * nuQ (Z / 2)))) / (a0 * (Z / 2 + (Z / 2) * (nuQ (Z / 2) - 1)))
      = slopeAbove Z := by
  have hy : 0 < Z / 2 := by positivity
  have hnu : nuQ (Z / 2) = Real.sqrt (1 + 2 / Z) := by
    unfold nuQ; congr 1; field_simp
  rw [hnu]
  unfold slopeAbove
  have hp : 0 < Real.sqrt (1 + 2 / Z) := Real.sqrt_pos.mpr (by positivity)
  generalize Real.sqrt (1 + 2 / Z) = s at hp ⊢
  have hs0 : s ≠ 0 := hp.ne'
  have hZ0 : Z ≠ 0 := hZ.ne'
  have ha0 : a0 ≠ 0 := ha.ne'
  have h1 : s * s⁻¹ = 1 := mul_inv_cancel₀ hs0
  have h2 : s ^ 2 * Z * s⁻¹ = s * Z := by
    rw [show s ^ 2 * Z * s⁻¹ = s * Z * (s * s⁻¹) by ring, h1, mul_one]
  field_simp
  linear_combination (-1) * h1 + h2

theorem slope_break {Z : ℝ} (hZ : 0 < Z) :
    slopeAbove Z - (Z + 1) / (Z + 2) = 1 / Real.sqrt (1 + 2 / Z) - 1 ∧
    slopeAbove Z - (Z + 1) / (Z + 2) < 0 := by
  have hpos : 0 < 1 + 2 / Z := by positivity
  have hp : 0 < Real.sqrt (1 + 2 / Z) := Real.sqrt_pos.mpr hpos
  have hsq : Real.sqrt (1 + 2 / Z) ^ 2 = 1 + 2 / Z := Real.sq_sqrt hpos.le
  have hgt : 1 < Real.sqrt (1 + 2 / Z) := by
    have : 0 < 2 / Z := by positivity
    nlinarith
  have heq : slopeAbove Z - (Z + 1) / (Z + 2) = 1 / Real.sqrt (1 + 2 / Z) - 1 := by
    unfold slopeAbove
    set s := Real.sqrt (1 + 2 / Z) with hs
    have hZ2 : Z + 2 ≠ 0 := by positivity
    have hs2 : s ^ 2 * Z = Z + 2 := by rw [hsq]; field_simp
    field_simp
    nlinarith [hs2]
  refine ⟨heq, ?_⟩
  rw [heq]
  have : 1 / Real.sqrt (1 + 2 / Z) < 1 := by
    rw [div_lt_one hp]; exact hgt
  linarith

theorem kink_lambda {c H Lam Z a0 : ℝ} (hc : 0 < c) (hZ : 0 < Z) (hLam : 0 ≤ Lam)
    (hHdef : H = c * Real.sqrt (Lam / 3)) (ha0 : a0 = c * H / Z) :
    (Z / 2) * a0 = c * H / 2 ∧ (Z / 2) * a0 = c ^ 2 * Real.sqrt (Lam / 12) ∧
    Lam = 12 * ((Z / 2) * a0) ^ 2 / c ^ 4 := by
  have hZ0 : Z ≠ 0 := hZ.ne'
  have e1 : (Z / 2) * a0 = c * H / 2 := by rw [ha0]; field_simp
  have hs : Real.sqrt (Lam / 12) = Real.sqrt (Lam / 3) / 2 := by
    have : Lam / 12 = (Lam / 3) / 2 ^ 2 := by ring
    rw [this, Real.sqrt_div (by positivity), Real.sqrt_sq (by norm_num)]
  have e2 : (Z / 2) * a0 = c ^ 2 * Real.sqrt (Lam / 12) := by
    rw [e1, hHdef, hs]; ring
  refine ⟨e1, e2, ?_⟩
  rw [e2, mul_pow, Real.sq_sqrt (by positivity)]
  have : c ^ 4 ≠ 0 := by positivity
  field_simp

end

#print axioms throttle_cubic
#print axioms throttle_general
#print axioms throttle_continuous_at_kink
#print axioms saturation
#print axioms saturation_general
#print axioms above_hasDeriv
#print axioms slope_above_at_kink
#print axioms slope_break
#print axioms kink_lambda
