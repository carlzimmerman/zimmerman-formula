import Mathlib

/-!
# ChainB -- the exact point-mass identities of "Gap 2" (a conserved cold fluid whose density equals the MOND phantom)

Source of the definitions: attack_B/B1_target_and_hydrostatics.py (checks S1, S4) and attack_B/B2_barotropic_nogo.py (E2).
Units are the script's: G > 0, a0 > 0, M > 0 (baryonic point mass), r > 0, u_N = G M, r_M^2 = G M / a0,
x = r / r_M, so x^2 = a0 r^2 / (G M).  The point-mass P2 law is g_tot = sqrt(g_N^2 + a0 g_N), g_N = G M / r^2,
equivalently u^2 = u_N^2 + a0 u_N r^2 with u = r^2 g_tot = G (M + M_c(<r)).

Definitions (all functions of r):
* `sx r        = sqrt (1 + a0 r^2/(G M))`                 (= sqrt(1+x^2))
* `Mc r        = M (sx r - 1)`                              enclosed cold mass
* `rhoC r      = a0 / (4 pi G r sx r)`                      cold density
* `gtot r      = G (M + Mc r) / r^2`                        the total Newtonian field felt by the fluid (script: g_tot = u/r^2)
* `Pfun r      = a0 M / (8 pi r^2)`                         the hydrostatic pressure
* `GammaEff r  = (dlnP/dr) / (dln rho_c/dr)`                effective polytropic index dlnP/dln rho along the profile

What is certified: exact algebra / calculus identities over the reals, premises => conclusion.
What is NOT certified: that the target rho_c g_tot = a0 M_b/(4 pi r^3) is the right target (it is CFG10 (ii), a declared
law, not derived here); extended baryon profiles (script identities (P), (S), (B), the ODE integration -- only the point mass
is done here); the exclusion for a general (non-point-mass) barotropic fluid; any GR / relativistic statement; any empirical fact.
-/

open Filter Topology

set_option linter.unusedVariables false

noncomputable section

namespace ChainB

/-- `sx r = sqrt (1 + a0 r^2 /(G M)) = sqrt (1 + x^2)`. -/
def sx (G a0 M r : ℝ) : ℝ := Real.sqrt (1 + a0 / (G * M) * r ^ 2)

/-- enclosed cold mass `M_c(<r) = M (sqrt(1+x^2) - 1)`. -/
def Mc (G a0 M r : ℝ) : ℝ := M * (sx G a0 M r - 1)

/-- cold density `rho_c = a0 / (4 pi G r sqrt(1+x^2))`. -/
def rhoC (G a0 M r : ℝ) : ℝ := a0 / (4 * Real.pi * G * r * sx G a0 M r)

/-- total Newtonian field of baryons plus cold fluid, `g_tot = G (M + M_c(<r)) / r^2` (the script's `u / r^2`). -/
def gtot (G a0 M r : ℝ) : ℝ := G * (M + Mc G a0 M r) / r ^ 2

/-- hydrostatic pressure `P = a0 M / (8 pi r^2)`. -/
def Pfun (G a0 M r : ℝ) : ℝ := a0 * M / (8 * Real.pi * r ^ 2)

/-- effective polytropic index `Gamma = dlnP/dln rho_c` computed from the logarithmic derivatives of the profile
    (`deriv P / P` divided by `deriv rho_c / rho_c`; the factor `r` cancels). -/
def GammaEff (G a0 M r : ℝ) : ℝ :=
  (deriv (Pfun G a0 M) r / Pfun G a0 M r) / (deriv (rhoC G a0 M) r / rhoC G a0 M r)

/-- the function of `x = r/r_M` that `GammaEff` equals: `2 (1+x^2)/(1+2 x^2)`. -/
def GammaX (x : ℝ) : ℝ := 2 * (1 + x ^ 2) / (1 + 2 * x ^ 2)

section basic
variable {G a0 M r : ℝ}

lemma sx_sq (hG : 0 < G) (ha : 0 < a0) (hM : 0 < M) :
    sx G a0 M r ^ 2 = 1 + a0 / (G * M) * r ^ 2 := by
  unfold sx
  apply Real.sq_sqrt
  positivity

lemma sx_pos (hG : 0 < G) (ha : 0 < a0) (hM : 0 < M) : 0 < sx G a0 M r := by
  unfold sx
  apply Real.sqrt_pos.mpr
  positivity

lemma sx_hasDeriv (hG : 0 < G) (ha : 0 < a0) (hM : 0 < M) (r : ℝ) :
    HasDerivAt (sx G a0 M) ((a0 / (G * M)) * r / sx G a0 M r) r := by
  have h1 : HasDerivAt (fun r : ℝ => 1 + a0 / (G * M) * r ^ 2) (a0 / (G * M) * (2 * r)) r := by
    have := ((hasDerivAt_pow 2 r).const_mul (a0 / (G * M))).const_add 1
    simpa using this
  have hne : (1 + a0 / (G * M) * r ^ 2) ≠ 0 := by positivity
  have h2 := h1.sqrt hne
  have hs : sx G a0 M r ≠ 0 := (sx_pos hG ha hM).ne'
  show HasDerivAt (fun r : ℝ => Real.sqrt (1 + a0 / (G * M) * r ^ 2)) _ r
  refine h2.congr_deriv ?_
  have h3 : Real.sqrt (1 + a0 / (G * M) * r ^ 2) = sx G a0 M r := rfl
  rw [h3]
  field_simp
end basic

/-- (1a) the enclosed cold mass has `HasDerivAt`, and `d M_c/dr = 4 pi r^2 rho_c` (the definition of `rho_c` as the
    mass density of the enclosed cold mass), for r > 0. -/
theorem Mc_hasDerivAt {G a0 M : ℝ} (hG : 0 < G) (ha : 0 < a0) (hM : 0 < M) {r : ℝ} (hr : 0 < r) :
    HasDerivAt (Mc G a0 M) (4 * Real.pi * r ^ 2 * rhoC G a0 M r) r := by
  have h := ((sx_hasDeriv hG ha hM r).sub_const 1).const_mul M
  have hs : sx G a0 M r ≠ 0 := (sx_pos hG ha hM).ne'
  have hπ : Real.pi ≠ 0 := Real.pi_ne_zero
  refine h.congr_deriv ?_
  unfold rhoC
  field_simp

/-- (1b) the density is the radial derivative of the enclosed cold mass: `rho_c = (1/(4 pi r^2)) dM_c/dr`. -/
theorem rhoC_eq_dMc {G a0 M : ℝ} (hG : 0 < G) (ha : 0 < a0) (hM : 0 < M) {r : ℝ} (hr : 0 < r) :
    rhoC G a0 M r = (1 / (4 * Real.pi * r ^ 2)) * deriv (Mc G a0 M) r := by
  rw [(Mc_hasDerivAt hG ha hM hr).deriv]
  have hπ : Real.pi ≠ 0 := Real.pi_ne_zero
  field_simp

/-- (1c) the script's target ODE (T) in the form `G dM_c/dr = a0 r u_N / u`, `u_N = G M`, `u = G (M + M_c)`. -/
theorem target_ODE {G a0 M : ℝ} (hG : 0 < G) (ha : 0 < a0) (hM : 0 < M) {r : ℝ} (hr : 0 < r) :
    G * deriv (Mc G a0 M) r = a0 * r * (G * M) / (G * (M + Mc G a0 M r)) := by
  rw [(Mc_hasDerivAt hG ha hM hr).deriv]
  have hs : sx G a0 M r ≠ 0 := (sx_pos hG ha hM).ne'
  have hπ : Real.pi ≠ 0 := Real.pi_ne_zero
  unfold rhoC Mc
  field_simp
  rw [show 1 + (sx G a0 M r - 1) = sx G a0 M r by ring, div_self hs]

/-- (1d) the P2 law: `u^2 = u_N^2 + a0 u_N r^2`, i.e. `(G (M + M_c))^2 = (G M)^2 + a0 (G M) r^2`. -/
theorem total_u_sq {G a0 M : ℝ} (hG : 0 < G) (ha : 0 < a0) (hM : 0 < M) (r : ℝ) :
    (G * (M + Mc G a0 M r)) ^ 2 = (G * M) ^ 2 + a0 * (G * M) * r ^ 2 := by
  have h := sx_sq (r := r) hG ha hM
  unfold Mc
  have hGM : G * M ≠ 0 := by positivity
  have : (G * (M + M * (sx G a0 M r - 1))) ^ 2 = (G * M) ^ 2 * sx G a0 M r ^ 2 := by ring
  rw [this, h]
  field_simp

/-- (1e) `g_tot = sqrt(g_N^2 + a0 g_N)` with `g_N = G M / r^2`: the enclosed cold mass reproduces the point-mass P2 law. -/
theorem gtot_eq_P2 {G a0 M : ℝ} (hG : 0 < G) (ha : 0 < a0) (hM : 0 < M) {r : ℝ} (hr : 0 < r) :
    gtot G a0 M r = Real.sqrt ((G * M / r ^ 2) ^ 2 + a0 * (G * M / r ^ 2)) := by
  have hpos : 0 ≤ gtot G a0 M r := by
    have := sx_pos (r := r) hG ha hM
    unfold gtot Mc
    have : 0 ≤ M + M * (sx G a0 M r - 1) := by nlinarith
    positivity
  rw [← Real.sqrt_sq hpos]
  congr 1
  have h := total_u_sq hG ha hM r
  unfold gtot
  have hr2 : r ^ 2 ≠ 0 := by positivity
  field_simp
  nlinarith [h]

/-- (1f) charge identity: `rho_c g_tot = a0 M /(4 pi r^3)` (the target (T)). -/
theorem charge_identity {G a0 M : ℝ} (hG : 0 < G) (ha : 0 < a0) (hM : 0 < M) {r : ℝ} (hr : 0 < r) :
    rhoC G a0 M r * gtot G a0 M r = a0 * M / (4 * Real.pi * r ^ 3) := by
  have hs : sx G a0 M r ≠ 0 := (sx_pos hG ha hM).ne'
  have hπ : Real.pi ≠ 0 := Real.pi_ne_zero
  unfold rhoC gtot Mc
  field_simp
  ring

/-- (2a) hydrostatic equilibrium: `P = a0 M/(8 pi r^2)` has `dP/dr = - rho_c g_tot`. -/
theorem hydrostatic {G a0 M : ℝ} (hG : 0 < G) (ha : 0 < a0) (hM : 0 < M) {r : ℝ} (hr : 0 < r) :
    HasDerivAt (Pfun G a0 M) (-(rhoC G a0 M r * gtot G a0 M r)) r := by
  have hπ : Real.pi ≠ 0 := Real.pi_ne_zero
  have hP := (((hasDerivAt_pow 2 r).const_mul (8 * Real.pi)).inv (by positivity)).const_mul (a0 * M)
  have hfun : Pfun G a0 M = fun r : ℝ => a0 * M * (8 * Real.pi * r ^ 2)⁻¹ := by
    funext y; unfold Pfun; rw [div_eq_mul_inv]
  rw [hfun, charge_identity hG ha hM hr]
  refine hP.congr_deriv ?_
  field_simp
  ring

/-- (2b) the isotropic dispersion: `sigma^2 = P / rho_c = r g_tot / 2 = V_c^2/2` (script S1). -/
theorem dispersion_half_vc_sq {G a0 M : ℝ} (hG : 0 < G) (ha : 0 < a0) (hM : 0 < M) {r : ℝ} (hr : 0 < r) :
    Pfun G a0 M r / rhoC G a0 M r = r * gtot G a0 M r / 2 := by
  have hs : sx G a0 M r ≠ 0 := (sx_pos hG ha hM).ne'
  have hπ : Real.pi ≠ 0 := Real.pi_ne_zero
  unfold Pfun rhoC gtot Mc
  field_simp
  ring

/-- (3a) log-derivative of the cold density: `rho_c' = - rho_c (1+2 xsq)/(r (1+xsq))`, `xsq = a0 r^2/(G M)`. -/
theorem rhoC_hasDeriv {G a0 M : ℝ} (hG : 0 < G) (ha : 0 < a0) (hM : 0 < M) {r : ℝ} (hr : 0 < r) :
    HasDerivAt (rhoC G a0 M)
      (-(rhoC G a0 M r) * (1 + 2 * (a0 / (G * M) * r ^ 2)) / (r * (1 + a0 / (G * M) * r ^ 2))) r := by
  have hs : sx G a0 M r ≠ 0 := (sx_pos hG ha hM).ne'
  have hsq := sx_sq (r := r) hG ha hM
  have hπ : Real.pi ≠ 0 := Real.pi_ne_zero
  have h1 : HasDerivAt (fun r : ℝ => 4 * Real.pi * G * r * sx G a0 M r)
      (4 * Real.pi * G * (sx G a0 M r + r * ((a0 / (G * M)) * r / sx G a0 M r))) r := by
    have := (((hasDerivAt_id r).const_mul (4 * Real.pi * G)).mul (sx_hasDeriv hG ha hM r))
    refine this.congr_deriv ?_
    simp only [id]
    ring
  have hne : 4 * Real.pi * G * r * sx G a0 M r ≠ 0 := by positivity
  have h2 := (hasDerivAt_const r a0).div h1 hne
  have hfun : (fun y => a0 / (4 * Real.pi * G * y * sx G a0 M y)) = rhoC G a0 M := rfl
  rw [← hfun]
  refine h2.congr_deriv ?_
  simp only []
  have hGM : G * M ≠ 0 := by positivity
  field_simp
  rw [hsq]
  field_simp
  ring

/-- (3b) the derivative of `P` over `P` is `-2/r`. -/
theorem Pfun_logderiv {G a0 M : ℝ} (hG : 0 < G) (ha : 0 < a0) (hM : 0 < M) {r : ℝ} (hr : 0 < r) :
    deriv (Pfun G a0 M) r / Pfun G a0 M r = -2 / r := by
  rw [(hydrostatic hG ha hM hr).deriv, charge_identity hG ha hM hr]
  unfold Pfun
  have hπ : Real.pi ≠ 0 := Real.pi_ne_zero
  field_simp
  ring

/-- (3c) the logarithmic derivative of the cold density: `rho_c'/rho_c = -(1+2 xsq)/(r (1+xsq))`, `xsq = a0 r^2/(G M)`. -/
theorem rhoC_logderiv {G a0 M : ℝ} (hG : 0 < G) (ha : 0 < a0) (hM : 0 < M) {r : ℝ} (hr : 0 < r) :
    deriv (rhoC G a0 M) r / rhoC G a0 M r
      = -(1 + 2 * (a0 / (G * M) * r ^ 2)) / (r * (1 + a0 / (G * M) * r ^ 2)) := by
  rw [(rhoC_hasDeriv hG ha hM hr).deriv]
  have hs : sx G a0 M r ≠ 0 := (sx_pos hG ha hM).ne'
  have hπ : Real.pi ≠ 0 := Real.pi_ne_zero
  have hρ : rhoC G a0 M r ≠ 0 := by unfold rhoC; positivity
  have hd : 1 + a0 / (G * M) * r ^ 2 ≠ 0 := by positivity
  field_simp

/-- (3d) `Gamma = dlnP/dln rho_c = 2 (1+x^2)/(1+2 x^2)`, `x = r/r_M`, `r_M = sqrt(G M/a0)`, for the point-mass target. -/
theorem GammaEff_eq {G a0 M : ℝ} (hG : 0 < G) (ha : 0 < a0) (hM : 0 < M) {r : ℝ} (hr : 0 < r) :
    GammaEff G a0 M r = GammaX (r / Real.sqrt (G * M / a0)) := by
  unfold GammaEff GammaX
  rw [Pfun_logderiv hG ha hM hr, rhoC_logderiv hG ha hM hr]
  have hx : (r / Real.sqrt (G * M / a0)) ^ 2 = a0 / (G * M) * r ^ 2 := by
    rw [div_pow, Real.sq_sqrt (by positivity)]
    field_simp
  rw [hx]
  have hd : 1 + a0 / (G * M) * r ^ 2 ≠ 0 := by positivity
  have hd2 : 1 + 2 * (a0 / (G * M) * r ^ 2) ≠ 0 := by positivity
  field_simp

/-- (3e) `Gamma(x) = 1 + 1/(1+2 x^2)`. -/
theorem GammaX_eq (x : ℝ) : GammaX x = 1 + 1 / (1 + 2 * x ^ 2) := by
  unfold GammaX
  have : 1 + 2 * x ^ 2 ≠ 0 := by positivity
  field_simp
  ring

/-- (3f) `1 < Gamma(x) <= 2` for every real `x` (in particular `x >= 0`). -/
theorem GammaX_bounds (x : ℝ) : 1 < GammaX x ∧ GammaX x ≤ 2 := by
  rw [GammaX_eq]
  have h : 0 < 1 + 2 * x ^ 2 := by positivity
  have h1 : 0 < 1 / (1 + 2 * x ^ 2) := by positivity
  have h2 : 1 / (1 + 2 * x ^ 2) ≤ 1 := by
    rw [div_le_one h]; nlinarith [sq_nonneg x]
  constructor <;> linarith

/-- (3g) `Gamma(0) = 2`, with equality only at `x = 0`: `Gamma(x) = 2 <-> x = 0`. -/
theorem GammaX_eq_two_iff (x : ℝ) : GammaX x = 2 ↔ x = 0 := by
  rw [GammaX_eq]
  have h : 0 < 1 + 2 * x ^ 2 := by positivity
  constructor
  · intro h2
    have : 1 / (1 + 2 * x ^ 2) = 1 := by linarith
    rw [div_eq_one_iff_eq h.ne'] at this
    nlinarith [sq_nonneg x]
  · rintro rfl; norm_num

/-- (3h) `Gamma` is strictly decreasing on `x >= 0`. -/
theorem GammaX_strictAntiOn : StrictAntiOn GammaX (Set.Ici 0) := by
  intro a ha b hb hab
  simp only [Set.mem_Ici] at ha hb
  rw [GammaX_eq, GammaX_eq]
  have h1 : 0 < 1 + 2 * a ^ 2 := by positivity
  have h2 : 1 + 2 * a ^ 2 < 1 + 2 * b ^ 2 := by nlinarith
  have := one_div_lt_one_div_of_lt h1 h2
  linarith

/-- (3i) `Gamma -> 2` as `x -> 0`. -/
theorem GammaX_tendsto_zero : Tendsto GammaX (𝓝 0) (𝓝 2) := by
  have hc : Continuous GammaX := by
    unfold GammaX
    refine Continuous.div (by fun_prop) (by fun_prop) (fun x => by positivity)
  have := hc.tendsto 0
  have h0 : GammaX 0 = 2 := by unfold GammaX; norm_num
  rwa [h0] at this

/-- (3j) `Gamma -> 1` as `x -> +infinity`. -/
theorem GammaX_tendsto_atTop : Tendsto GammaX atTop (𝓝 1) := by
  have h1 : Tendsto (fun x : ℝ => 1 + 2 * x ^ 2) atTop atTop := by
    apply tendsto_atTop_add_const_left
    exact Tendsto.const_mul_atTop (by norm_num) (tendsto_pow_atTop (by norm_num))
  have h2 : Tendsto (fun x : ℝ => (1 + 2 * x ^ 2)⁻¹) atTop (𝓝 0) := h1.inv_tendsto_atTop
  have h3 : Tendsto (fun x : ℝ => 1 + (1 + 2 * x ^ 2)⁻¹) atTop (𝓝 (1 + 0)) := h2.const_add 1
  simp only [add_zero] at h3
  refine h3.congr (fun x => ?_)
  rw [GammaX_eq, one_div]

/-- (3k) NO SINGLE POLYTROPE: there is no constant `Gamma0` with `Gamma(x) = Gamma0` for all `x >= 0`
    (the effective index takes the value 2 at x = 0 and 4/3 at x = 1). -/
theorem no_single_polytrope : ¬ ∃ Γ0 : ℝ, ∀ x : ℝ, 0 ≤ x → GammaX x = Γ0 := by
  rintro ⟨Γ0, h⟩
  have h0 := h 0 le_rfl
  have h1 := h 1 zero_le_one
  unfold GammaX at h0 h1
  norm_num at h0 h1
  linarith

/-- (3l) the same in the physical radius: `GammaEff -> 2` as `r -> 0+` (point-mass target); the `r -> +infinity`
    limit is `GammaEff_tendsto_atTop`. -/
theorem GammaEff_tendsto_zero {G a0 M : ℝ} (hG : 0 < G) (ha : 0 < a0) (hM : 0 < M) :
    Tendsto (GammaEff G a0 M) (𝓝[>] 0) (𝓝 2) := by
  have hrM : 0 < Real.sqrt (G * M / a0) := Real.sqrt_pos.mpr (by positivity)
  have h1 : Tendsto (fun r : ℝ => r / Real.sqrt (G * M / a0)) (𝓝[>] 0) (𝓝 0) := by
    have : Continuous (fun r : ℝ => r / Real.sqrt (G * M / a0)) := by fun_prop
    have h := this.tendsto 0
    rw [zero_div] at h
    exact h.mono_left nhdsWithin_le_nhds
  have h2 := GammaX_tendsto_zero.comp h1
  refine h2.congr' ?_
  filter_upwards [self_mem_nhdsWithin] with r hr
  exact (GammaEff_eq hG ha hM hr).symm

/-- (3l) `GammaEff -> 1` as `r -> +infinity` (point-mass target). -/
theorem GammaEff_tendsto_atTop {G a0 M : ℝ} (hG : 0 < G) (ha : 0 < a0) (hM : 0 < M) :
    Tendsto (GammaEff G a0 M) atTop (𝓝 1) := by
  have hrM : 0 < Real.sqrt (G * M / a0) := Real.sqrt_pos.mpr (by positivity)
  have h1 : Tendsto (fun r : ℝ => r / Real.sqrt (G * M / a0)) atTop atTop :=
    tendsto_id.atTop_div_const hrM
  have h2 := GammaX_tendsto_atTop.comp h1
  refine h2.congr' ?_
  filter_upwards [eventually_gt_atTop 0] with r hr
  exact (GammaEff_eq hG ha hM hr).symm

end ChainB
