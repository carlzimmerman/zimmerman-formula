import Mathlib

/-!
# M6-H -- the dS4 Dirac-fermion conductivity function G_f(M): the M -> 0 asymptotics (logarithm), from Mathlib's digamma

Source: `real_research/alpha_principle_2026/Q1_ds4_fermions/q1_lib.py` (lines 147-152, the Hayashinaka-Xue closed form
sigma_HFY(M) = (1/(3 pi^2)) [ln M - Re psi(iM) - pi M (4 M^2 + 1)/(3 sinh(2 pi M))]) and
`q1_3_physics_answers.py` (line 6 "G_f = 4 pi sigma_HFY", line 41 `G_f`, and check Q3c, line 113: "small M: the fermion follows
the logarithm G_f = (4/(3 pi))(ln M + gamma_E - 1/6)").  The script checks Q3c NUMERICALLY (2% at M = 0.01, 0.1).
Here the closed form is taken as the DEFINITION of G_f (it is a published formula quoted by the lane, not re-derived) and the
small-mass statement is proved.

Corpus check (2026-09-29): `git grep -n -i -e digamma -e "psi(" -e "G_f" -- '*.lean'` finds no use of digamma outside Mathlib.  New.

CERTIFIED (real/complex analysis, exact):
  * `re_digamma_ix`      : for M != 0, Re psi(i M) = Re psi(1 + i M)  (functional equation psi(s+1) = psi(s) + 1/s, and 1/(iM)
                           is purely imaginary);
  * `digamma_cont_one`   : psi = Gamma'/Gamma is continuous at 1 (Gamma is analytic near 1, Gamma(1) = 1);
  * `re_digamma_limit`   : Re psi(i M) -> psi(1) = -gamma_E as M -> 0+  (Mathlib: `Complex.digamma_one`);
  * `sinh_term_limit`    : pi M (4 M^2+1)/(3 sinh(2 pi M)) -> 1/6 as M -> 0+;
  * `Gf_small_mass`      : G_f(M) - (4/(3 pi)) (ln M + gamma_E - 1/6) -> 0 as M -> 0+;
  * `Gf_tendsto_atBot`   : hence G_f(M) -> -infinity as M -> 0+ (logarithmically): the minimal-scheme conductivity of a massless
                           dS4 Dirac fermion has no finite value (the lane's Q3c / point (c) at line 174).
NOT CERTIFIED: that the closed form is the correct renormalised current (Hayashinaka-Xue 1802.03686, quoted); the maximal
subtraction scheme (G_f^max(0) = -2/(9 pi)); the large-M law G_f M^2 -> 1/(9 pi) (needs the asymptotic series of psi, not in
Mathlib); any tie of alpha to G_f (the lane finds none); the electron reading M_e = m_e/H_0.  alpha stays an INPUT; kappa = 1/2
is unrelated.
-/

noncomputable section
namespace M6H

open Complex Filter Topology

/-- the closed form (minimal scheme): G_f = 4 pi sigma_HFY -/
def Gf (M : ℝ) : ℝ :=
  (4 / (3 * Real.pi)) *
    (Real.log M - (Complex.digamma (Complex.I * (M : ℂ))).re
      - Real.pi * M * (4 * M ^ 2 + 1) / (3 * Real.sinh (2 * Real.pi * M)))

theorem re_digamma_ix {M : ℝ} (hM : M ≠ 0) :
    (Complex.digamma (Complex.I * (M : ℂ))).re = (Complex.digamma (1 + Complex.I * (M : ℂ))).re := by
  have hs : ∀ m : ℕ, Complex.I * (M : ℂ) ≠ -(m : ℂ) := by
    intro m h
    have := congrArg Complex.im h
    simp at this
    exact hM this
  have h := Complex.digamma_apply_add_one _ hs
  rw [add_comm] at h
  rw [h]
  have : ((Complex.I * (M : ℂ))⁻¹).re = 0 := by
    have hM' : (M : ℂ) ≠ 0 := by exact_mod_cast hM
    rw [mul_inv, Complex.inv_I]
    simp
  simp

theorem digamma_cont_one : ContinuousAt Complex.digamma 1 := by
  have hA : AnalyticAt ℂ Complex.Gamma 1 := by
    rw [Complex.analyticAt_iff_eventually_differentiableAt]
    have hball : Metric.ball (1 : ℂ) 1 ∈ 𝓝 (1 : ℂ) := Metric.ball_mem_nhds _ one_pos
    filter_upwards [hball] with z hz
    apply Complex.differentiableAt_Gamma
    intro m hm
    have hre : 0 < z.re := by
      have : |z.re - 1| < 1 := by
        have h1 := Complex.abs_re_le_norm (z - 1)
        rw [Metric.mem_ball, dist_eq_norm] at hz
        simpa using lt_of_le_of_lt h1 hz
      have := (abs_lt.1 this).1
      linarith
    have := congrArg Complex.re hm
    simp at this
    have hm0 : (0 : ℝ) ≤ m := Nat.cast_nonneg m
    linarith
  have hd : ContinuousAt (deriv Complex.Gamma) 1 := hA.deriv.continuousAt
  have hg : ContinuousAt Complex.Gamma 1 := hA.continuousAt
  have h1 : Complex.Gamma 1 ≠ 0 := by rw [Complex.Gamma_one]; exact one_ne_zero
  have := hd.div hg h1
  have e : Complex.digamma = fun z => deriv Complex.Gamma z / Complex.Gamma z := by
    funext z
    rw [Complex.digamma_def, logDeriv_apply]
  rw [e]
  exact this

theorem re_digamma_limit :
    Tendsto (fun M : ℝ => (Complex.digamma (Complex.I * (M : ℂ))).re) (𝓝[>] 0)
      (𝓝 (Real.eulerMascheroniConstant)) := by
  have hc : ContinuousAt (fun M : ℝ => (1 : ℂ) + Complex.I * (M : ℂ)) 0 := by fun_prop
  have hc' : Tendsto (fun M : ℝ => (1 : ℂ) + Complex.I * (M : ℂ)) (𝓝 0) (𝓝 1) := by
    simpa using hc.tendsto
  have h1 : Tendsto (fun M : ℝ => Complex.digamma (1 + Complex.I * (M : ℂ))) (𝓝 0)
      (𝓝 (Complex.digamma 1)) := digamma_cont_one.tendsto.comp hc'
  have h2 : Tendsto (fun M : ℝ => (Complex.digamma (1 + Complex.I * (M : ℂ))).re) (𝓝 0)
      (𝓝 ((Complex.digamma 1).re)) := (Complex.continuous_re.tendsto _).comp h1
  have e : (Complex.digamma 1).re = -Real.eulerMascheroniConstant := by
    rw [Complex.digamma_one]; simp
  rw [e] at h2
  have h3 := h2.mono_left (nhdsWithin_le_nhds (s := Set.Ioi (0:ℝ)))
  refine h3.congr' ?_
  filter_upwards [self_mem_nhdsWithin] with M hM
  exact (re_digamma_ix (ne_of_gt hM)).symm

theorem sinh_term_limit :
    Tendsto (fun M : ℝ => Real.pi * M * (4 * M ^ 2 + 1) / (3 * Real.sinh (2 * Real.pi * M))) (𝓝[>] 0)
      (𝓝 (1 / 6)) := by
  -- slope of sinh at 0 tends to cosh 0 = 1
  have hs : Tendsto (slope Real.sinh 0) (𝓝[≠] 0) (𝓝 1) := by
    have := (Real.hasDerivAt_sinh 0).tendsto_slope
    simpa using this
  have hc : Tendsto (fun M : ℝ => 2 * Real.pi * M) (𝓝[>] 0) (𝓝[≠] 0) := by
    refine tendsto_nhdsWithin_iff.2 ⟨?_, ?_⟩
    · have : Tendsto (fun M : ℝ => 2 * Real.pi * M) (𝓝 0) (𝓝 (2 * Real.pi * 0)) :=
        (continuous_const.mul continuous_id).tendsto 0
      simpa using this.mono_left nhdsWithin_le_nhds
    · filter_upwards [self_mem_nhdsWithin] with M hM
      have : 0 < 2 * Real.pi * M := by have := Real.pi_pos; have : (0:ℝ) < M := hM; positivity
      exact ne_of_gt this
  have h1 := hs.comp hc
  have h2 : Tendsto (fun M : ℝ => (slope Real.sinh 0 (2 * Real.pi * M))⁻¹) (𝓝[>] 0) (𝓝 (1 : ℝ)⁻¹) :=
    h1.inv₀ (by norm_num)
  have h3 : Tendsto (fun M : ℝ => (4 * M ^ 2 + 1) / 6) (𝓝[>] 0) (𝓝 (1 / 6)) := by
    have : Tendsto (fun M : ℝ => (4 * M ^ 2 + 1) / 6) (𝓝 0) (𝓝 ((4 * 0 ^ 2 + 1) / 6)) :=
      ((continuous_const.mul (continuous_pow 2)).add continuous_const).div_const 6 |>.tendsto 0
    simpa using this.mono_left nhdsWithin_le_nhds
  have h4 := h3.mul h2
  simp only [inv_one, mul_one] at h4
  refine h4.congr' ?_
  filter_upwards [self_mem_nhdsWithin] with M hM
  have hM' : (0:ℝ) < M := hM
  have hpi := Real.pi_pos
  have hsinh : 0 < Real.sinh (2 * Real.pi * M) := Real.sinh_pos_iff.2 (by positivity)
  simp only [slope_def_field, sub_zero, Real.sinh_zero]
  field_simp
  norm_num

theorem Gf_small_mass :
    Tendsto (fun M : ℝ => Gf M - (4 / (3 * Real.pi)) * (Real.log M + Real.eulerMascheroniConstant - 1 / 6))
      (𝓝[>] 0) (𝓝 0) := by
  have hR := tendsto_sub_nhds_zero_iff.2 re_digamma_limit
  have hS := tendsto_sub_nhds_zero_iff.2 sinh_term_limit
  have h := (hR.add hS).const_mul (-(4 / (3 * Real.pi)))
  simp only [add_zero, mul_zero] at h
  refine h.congr' ?_
  filter_upwards with M
  unfold Gf
  ring

theorem Gf_tendsto_atBot : Tendsto Gf (𝓝[>] 0) atBot := by
  have hpi := Real.pi_pos
  have hlog : Tendsto (fun M : ℝ => (4 / (3 * Real.pi)) * (Real.log M + Real.eulerMascheroniConstant - 1 / 6))
      (𝓝[>] 0) atBot := by
    have h1 : Tendsto (fun M : ℝ => Real.log M + (Real.eulerMascheroniConstant - 1 / 6)) (𝓝[>] 0) atBot :=
      Real.tendsto_log_nhdsGT_zero.atBot_add tendsto_const_nhds
    have h2 := h1.const_mul_atBot (show (0:ℝ) < 4 / (3 * Real.pi) by positivity)
    refine h2.congr ?_
    intro M
    ring
  have h3 := hlog.atBot_add Gf_small_mass
  refine h3.congr ?_
  intro M
  ring

end M6H

end

#print axioms M6H.re_digamma_ix
#print axioms M6H.digamma_cont_one
#print axioms M6H.re_digamma_limit
#print axioms M6H.sinh_term_limit
#print axioms M6H.Gf_small_mass
#print axioms M6H.Gf_tendsto_atBot
