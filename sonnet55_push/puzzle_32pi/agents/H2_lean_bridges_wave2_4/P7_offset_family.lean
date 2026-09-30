import Mathlib

open Real MeasureTheory intervalIntegral

/-!
# P7: the density-linear (AQUAL-offset) family and the "rational carriers" (lanes K, G, W)

Conventions: G = c = 1 unless shown.  With the Poisson-normalised Lagrangian L = -(a0^2/(8 pi G)) F(y) - rho phi and F -> y at large y, the vacuum offset is
    G rho/a0^2 = c/(8 pi),   c = int_0^inf (1 - mu) d(x^2) = int_0^inf (1 - mu(x)) 2 x dx   (x = g/a0)          [INPUT, lane K k01 A/B]
(here `c` is the offset coefficient, not the speed of light).  The puzzle G rho = 4 a0^2 is c = 32 pi.

CERTIFIED (premises => conclusions):
 (a) `offset_iff`: G rho = 4 a0^2 <=> c = 32 pi (a0 != 0).  `c_req`: with rho_L = 3 H0^2 Omega_L/(8 pi G): c_req = 8 pi G rho_L/a0^2 = 3 Omega_L H0^2/a0^2 (no G, no pi), and with a0^2 = Omega_L H0^2/Z^2
     (a0 = H_L/Z): c_req = 3 Z^2, = 32 pi iff Z^2 = 32 pi/3 (`c_req_Z`).
 (b) `poisson_no_rational` / `poisson_no_algebraic`: a RATIONAL c (unconditionally: irrational_pi) or an ALGEBRAIC c (conditional on the explicit hypothesis `Transcendental Q pi`) never gives G rho = 4 a0^2:
     c = 32 pi is transcendental.  (W11's "Poisson-prefactor theorem".)
 (c) bathtub bound: `mu_le_x` (mu(0) = 0, mu' <= 1 on (0, infinity) => mu(x) <= x, mean value theorem), `bathtub_bound` (if mu <= min(x, 1) and mu is continuous then for every T >= 1
     int_0^T (1 - mu) 2x dx >= 1/3, and the integrand is >= 0 so the partial integrals increase to c): c >= 1/3 for every monotone mu with mu' <= 1.  `sharp_value`: the sharp
     mu = min(x, 1) has partial integral EXACTLY 1/3 for every T >= 1 (the bound is sharp); control `steep_value`: mu = min(2x, 1) (slope 2 > 1) has 1/12 < 1/3, so the hypothesis mu' <= 1 is essential.
     There is NO universal upper bound (lane K): `orMu_admissible` (the record's OR shapes 1 - (1 + x/N)^(-N) are continuous, <= x, <= 1) and `no_upper_bound` (for every M an admissible shape with c > M,
     from `cN_blowup` + `offset_integral`).
 (d) the record's OR family mu = 1 - (1 - p)^N, p = x/(1 + x), i.e. 1 - mu = (1 + x/N)^(-N) in the variable x = g/a0 with a0 = s/N: `offset_integral`: for N > 2 the integrand 2x (1 + x/N)^(-N)
     is integrable on (0, infinity) and int = c(N) = 2 N^2/((N - 1)(N - 2)) (PROVED from an explicit antiderivative, derivative and limit); `offset_N2_not_integrable`: for N = 2 it is NOT integrable (the offset
     coefficient of the kappa = 1/2 shape is infinite).  With the reading G rho = c a0^2/(8 pi), s^2 = G rho, a0 = s/N (c(N) = 8 pi N^2):
     `cN_eq_iff`: c(N) = 8 pi N^2 <=> (N - 1)(N - 2) = 1/(4 pi); `Nstar`: N* = (3 + sqrt(1 + 1/pi))/2 solves it, N* > 2, 2.0740 < N* < 2.0742, kappa* = 1/N* in (0.4821, 0.4822) -- NOT 1/2;
     `N_two_marginal`: N = 2 (kappa = 1/2) is not a solution ((N-1)(N-2) = 0 != 1/(4 pi)) and c(N) -> +infinity as N -> 2+ (`cN_blowup`).
 (e) W lane, rational carriers: `F_Lambda`: rho_Lambda A_dS = 6 F_max (F_max = 1/4) for EVERY L -- an identity of Lambda, c, G alone, not equivalent to the puzzle; `sheet`: Sigma_Lambda = rho_Lambda R* = sqrt(G rho)... equals 4 pi Sigma_M
     (Sigma_M = a0/(2 pi)) iff G rho = 4 a0^2; `lattice`: a_nn^2 = G rho (G m/l) for rho = m/l^3 and a0^2 = G rho/4 iff G m/l = 1/4 (compactness 1/4); `thresholds`: the Lambda zero-force sphere has mean
     density 2 rho_Lambda and the outermost stable circular orbit 8 rho_Lambda (Newtonian).

NOT certified: that the offset identification is a real feature of any relativistic completion, that mu has any of these shapes, that c is anything; c >= 1/3 is a constraint on an unmeasured tail (lane K), kappa = 1/2 (FITTED).
-/

namespace OffsetFamily

/-- (a) G rho = 4 a0^2 iff the offset coefficient c = 32 pi, given G rho/a0^2 = c/(8 pi) -/
theorem offset_iff {G ρ a0 c : ℝ} (ha : a0 ≠ 0) (h : G * ρ / a0 ^ 2 = c / (8 * π)) : G * ρ = 4 * a0 ^ 2 ↔ c = 32 * π := by
  have hp := Real.pi_pos
  have hp0 : 8 * π ≠ 0 := by positivity
  have ha2 : a0 ^ 2 ≠ 0 := pow_ne_zero 2 ha
  rw [div_eq_div_iff ha2 hp0] at h
  constructor
  · intro h1
    have : a0 ^ 2 * (c - 32 * π) = 0 := by nlinarith [h, h1]
    rcases mul_eq_zero.mp this with h2 | h2
    · exact absurd h2 ha2
    · linarith
  · intro h1; rw [h1] at h; nlinarith [h]

/-- c_req = 8 pi G rho_L/a0^2 with rho_L = 3 H0^2 Omega/(8 pi G): 3 Omega H0^2/a0^2 (no G, no pi) -/
theorem c_req {G H0 Ω a0 : ℝ} (hG : 0 < G) (ha : a0 ≠ 0) :
    8 * π * (G * (3 * H0 ^ 2 * Ω / (8 * π * G))) / a0 ^ 2 = 3 * Ω * H0 ^ 2 / a0 ^ 2 := by
  have hp := Real.pi_pos
  have hG0 : G ≠ 0 := hG.ne'
  field_simp

/-- a0 = H_L/Z, H_L^2 = Omega H0^2: c_req = 3 Z^2; = 32 pi iff Z^2 = 32 pi/3 -/
theorem c_req_Z {Ω H0 a0 Z : ℝ} (hZ : 0 < Z) (ha : a0 ^ 2 = Ω * H0 ^ 2 / Z ^ 2) (hΩ : Ω ≠ 0) (hH : H0 ≠ 0) :
    3 * Ω * H0 ^ 2 / a0 ^ 2 = 3 * Z ^ 2 ∧ (3 * Z ^ 2 = 32 * π ↔ Z ^ 2 = 32 * π / 3) := by
  have hZ2 : Z ^ 2 ≠ 0 := pow_ne_zero 2 hZ.ne'
  constructor
  · rw [ha]; field_simp
  · constructor <;> intro h <;> linarith

/-- (b) a rational offset coefficient never gives the puzzle -/
theorem poisson_no_rational (q : ℚ) : (q : ℝ) ≠ 32 * π := by
  intro h
  have h1 : Irrational (32 * π) := by
    have := irrational_pi.ratCast_mul (q := 32) (by norm_num)
    simpa using this
  exact h1 ⟨q, h⟩

/-- ... and no algebraic one if pi is transcendental (explicit hypothesis) -/
theorem poisson_no_algebraic (hπ : Transcendental ℚ π) (c : ℝ) (hc : IsAlgebraic ℚ c) : c ≠ 32 * π := by
  intro h
  have hmem : c ∈ algebraicClosure ℚ ℝ := (mem_algebraicClosure_iff).mpr hc
  have h32 : ((1 / 32 : ℚ) : ℝ) ∈ algebraicClosure ℚ ℝ := (algebraicClosure ℚ ℝ).algebraMap_mem _
  have h4 := (algebraicClosure ℚ ℝ).mul_mem h32 hmem
  have e : ((1 / 32 : ℚ) : ℝ) * c = π := by rw [h]; push_cast; ring
  rw [e] at h4
  exact hπ ((mem_algebraicClosure_iff).mp h4)

/-! (c) the bathtub bound -/

theorem mu_le_x {μ : ℝ → ℝ} (hc : ContinuousOn μ (Set.Ici 0)) (hd : DifferentiableOn ℝ μ (Set.Ioi 0)) (h0 : μ 0 = 0)
    (hle : ∀ x ∈ Set.Ioi (0:ℝ), deriv μ x ≤ 1) {x : ℝ} (hx : 0 ≤ x) : μ x ≤ x := by
  have h := (convex_Ici (0:ℝ)).image_sub_le_mul_sub_of_deriv_le hc (by simpa [interior_Ici] using hd)
    (by simpa [interior_Ici] using hle) 0 (Set.mem_Ici.mpr le_rfl) x (Set.mem_Ici.mpr hx) hx
  simpa [h0] using h

/-- non-vacuity of `mu_le_x`: mu(x) = x/(1 + x) is continuous on [0, infinity), differentiable on (0, infinity), mu(0) = 0, mu' = 1/(1+x)^2 <= 1; hence x/(1+x) <= x -/
theorem mu_le_x_instance {x : ℝ} (hx : 0 ≤ x) : x / (1 + x) ≤ x := by
  have hcont : ContinuousOn (fun x : ℝ => x / (1 + x)) (Set.Ici 0) := by
    apply ContinuousOn.div continuousOn_id (continuousOn_const.add continuousOn_id)
    intro y hy; have : 0 ≤ y := hy
    show 1 + y ≠ 0
    positivity
  have hder : ∀ y : ℝ, 0 < y → HasDerivAt (fun x : ℝ => x / (1 + x)) (1 / (1 + y) ^ 2) y := by
    intro y hy
    have h1 : HasDerivAt (fun x : ℝ => 1 + x) 1 y := by simpa using (hasDerivAt_id y).const_add 1
    have h2 := (hasDerivAt_id y).div h1 (by positivity)
    refine h2.congr_deriv ?_
    simp only [id]
    field_simp
    ring
  have hd : DifferentiableOn ℝ (fun x : ℝ => x / (1 + x)) (Set.Ioi 0) := fun y hy => (hder y hy).differentiableAt.differentiableWithinAt
  have hle : ∀ y ∈ Set.Ioi (0:ℝ), deriv (fun x : ℝ => x / (1 + x)) y ≤ 1 := by
    intro y hy
    rw [(hder y hy).deriv]
    have hy0 : 0 < y := hy
    rw [div_le_one (by positivity)]
    nlinarith
  exact mu_le_x hcont hd (by simp) hle hx

theorem int_lin_one : ∫ x in (0:ℝ)..1, (1 - x) * (2 * x) = 1 / 3 := by
  have : (fun x : ℝ => (1 - x) * (2 * x)) = fun x => 2 * x - 2 * x ^ 2 := by funext x; ring
  rw [this, intervalIntegral.integral_sub, intervalIntegral.integral_const_mul, intervalIntegral.integral_const_mul, integral_id, integral_pow]
  · norm_num
  · exact (continuous_const.mul continuous_id).intervalIntegrable _ _
  · exact (continuous_const.mul (continuous_pow 2)).intervalIntegrable _ _

theorem bathtub_bound {μ : ℝ → ℝ} (hc : ContinuousOn μ (Set.Ici 0)) (hle : ∀ x, 0 ≤ x → μ x ≤ x) (h1 : ∀ x, 0 ≤ x → μ x ≤ 1)
    {T : ℝ} (hT : 1 ≤ T) : 1 / 3 ≤ ∫ x in (0:ℝ)..T, (1 - μ x) * (2 * x) := by
  have hint : ∀ a b : ℝ, 0 ≤ a → a ≤ b → IntervalIntegrable (fun x => (1 - μ x) * (2 * x)) volume a b := by
    intro a b ha hab
    apply ContinuousOn.intervalIntegrable
    have hsub : Set.uIcc a b ⊆ Set.Ici 0 := by
      intro y hy
      rw [Set.uIcc_of_le hab] at hy
      exact Set.mem_Ici.mpr (le_trans ha hy.1)
    exact ((continuousOn_const.sub (hc.mono hsub)).mul (continuousOn_const.mul continuousOn_id))
  have hsplit := intervalIntegral.integral_add_adjacent_intervals (hint 0 1 le_rfl zero_le_one) (hint 1 T zero_le_one hT)
  rw [← hsplit]
  have hA : 1 / 3 ≤ ∫ x in (0:ℝ)..1, (1 - μ x) * (2 * x) := by
    rw [← int_lin_one]
    apply intervalIntegral.integral_mono_on zero_le_one
    · exact (continuous_const.sub continuous_id).mul (continuous_const.mul continuous_id) |>.intervalIntegrable _ _
    · exact hint 0 1 le_rfl zero_le_one
    · intro x hx
      have := hle x hx.1
      have hx0 : 0 ≤ 2 * x := by linarith [hx.1]
      nlinarith
  have hB : 0 ≤ ∫ x in (1:ℝ)..T, (1 - μ x) * (2 * x) := by
    apply intervalIntegral.integral_nonneg hT
    intro x hx
    have := h1 x (le_trans zero_le_one hx.1)
    have hx0 : 0 ≤ 2 * x := by linarith [hx.1]
    have : 0 ≤ 1 - μ x := by linarith
    positivity
  linarith

/-- the sharp mu = min(x, 1): partial integral exactly 1/3 for every T >= 1 (the bathtub bound is attained) -/
theorem sharp_value {T : ℝ} (hT : 1 ≤ T) : ∫ x in (0:ℝ)..T, (1 - min x 1) * (2 * x) = 1 / 3 := by
  have hc1 : Continuous fun x : ℝ => (1 - min x 1) * (2 * x) :=
    (continuous_const.sub (continuous_id.min continuous_const)).mul (continuous_const.mul continuous_id)
  rw [← intervalIntegral.integral_add_adjacent_intervals (hc1.intervalIntegrable 0 1) (hc1.intervalIntegrable 1 T)]
  have h1 : ∫ x in (0:ℝ)..1, (1 - min x 1) * (2 * x) = 1 / 3 := by
    rw [← int_lin_one]
    apply intervalIntegral.integral_congr
    intro x hx
    rw [Set.uIcc_of_le zero_le_one] at hx
    simp [min_eq_left hx.2]
  have h2 : ∫ x in (1:ℝ)..T, (1 - min x 1) * (2 * x) = 0 := by
    have : ∫ x in (1:ℝ)..T, (1 - min x 1) * (2 * x) = ∫ x in (1:ℝ)..T, (0:ℝ) := by
      apply intervalIntegral.integral_congr
      intro x hx
      rw [Set.uIcc_of_le hT] at hx
      simp [min_eq_right hx.1]
    rw [this]; simp
  rw [h1, h2]; ring

/-- control: mu = min(2x, 1) (slope 2 > 1) has partial integral 1/12 < 1/3 for T >= 1/2 -/
theorem steep_value {T : ℝ} (hT : 1 / 2 ≤ T) : ∫ x in (0:ℝ)..T, (1 - min (2 * x) 1) * (2 * x) = 1 / 12 := by
  have hc1 : Continuous fun x : ℝ => (1 - min (2 * x) 1) * (2 * x) :=
    (continuous_const.sub ((continuous_const.mul continuous_id).min continuous_const)).mul (continuous_const.mul continuous_id)
  rw [← intervalIntegral.integral_add_adjacent_intervals (hc1.intervalIntegrable 0 (1 / 2)) (hc1.intervalIntegrable (1 / 2) T)]
  have h1 : ∫ x in (0:ℝ)..(1 / 2), (1 - min (2 * x) 1) * (2 * x) = 1 / 12 := by
    have : ∫ x in (0:ℝ)..(1 / 2), (1 - min (2 * x) 1) * (2 * x) = ∫ x in (0:ℝ)..(1 / 2), (2 * x - 4 * x ^ 2) := by
      apply intervalIntegral.integral_congr
      intro x hx
      rw [Set.uIcc_of_le (by norm_num)] at hx
      have : 2 * x ≤ 1 := by linarith [hx.2]
      simp only [min_eq_left this]; ring
    rw [this, intervalIntegral.integral_sub, intervalIntegral.integral_const_mul, intervalIntegral.integral_const_mul, integral_id, integral_pow]
    · norm_num
    · exact (continuous_const.mul continuous_id).intervalIntegrable _ _
    · exact (continuous_const.mul (continuous_pow 2)).intervalIntegrable _ _
  have h2 : ∫ x in (1 / 2 : ℝ)..T, (1 - min (2 * x) 1) * (2 * x) = 0 := by
    have : ∫ x in (1 / 2 : ℝ)..T, (1 - min (2 * x) 1) * (2 * x) = ∫ x in (1 / 2 : ℝ)..T, (0:ℝ) := by
      apply intervalIntegral.integral_congr
      intro x hx
      rw [Set.uIcc_of_le hT] at hx
      have : 1 ≤ 2 * x := by linarith [hx.1]
      simp [min_eq_right this]
    rw [this]; simp
  rw [h1, h2]; ring




/-! (d) the record's OR family -/

/-- c(N) = 2 N^2/((N-1)(N-2)): the closed form of int_0^inf (1 + x/N)^(-N) 2x dx for N > 2 (PROVED below, `offset_integral`) -/
noncomputable def cN (N : ℝ) : ℝ := 2 * N ^ 2 / ((N - 1) * (N - 2))

theorem cN_eq_iff {N : ℝ} (hN : 2 < N) : cN N = 8 * π * N ^ 2 ↔ (N - 1) * (N - 2) = 1 / (4 * π) := by
  have hp := Real.pi_pos
  have h1 : 0 < N - 1 := by linarith
  have h2 : 0 < N - 2 := by linarith
  have hq : (N - 1) * (N - 2) ≠ 0 := by positivity
  have hN2 : 0 < N ^ 2 := by positivity
  unfold cN
  rw [div_eq_iff hq, eq_div_iff (by positivity)]
  constructor
  · intro h
    have : N ^ 2 * (4 * π * ((N - 1) * (N - 2)) - 1) = 0 := by nlinarith [h]
    rcases mul_eq_zero.mp this with h3 | h3
    · exact absurd h3 hN2.ne'
    · nlinarith [h3]
  · intro h
    nlinarith [h, hN2]

section OffsetIntegral
open Set Filter Topology

/-- the closed-form antiderivative of the offset integrand -/
noncomputable def FN (N x : ℝ) : ℝ := 2 * N^2 * ((1 + x/N)^(1 - N) / (N - 1) - (1 + x/N)^(2 - N) / (N - 2))

theorem FN_deriv {N x : ℝ} (hN : 2 < N) (hx : 0 ≤ x) : HasDerivAt (FN N) ((1 + x/N)^(-N) * (2*x)) x := by
  have hN0 : 0 < N := by linarith
  have hu0 : 0 < 1 + x / N := by positivity
  have hu : HasDerivAt (fun x : ℝ => 1 + x / N) (1 / N) x := by
    simpa using ((hasDerivAt_id x).div_const N).const_add 1
  have h1 := hu.rpow_const (p := 1 - N) (Or.inl hu0.ne')
  have h2 := hu.rpow_const (p := 2 - N) (Or.inl hu0.ne')
  have h3 := ((h1.div_const (N - 1)).sub (h2.div_const (N - 2))).const_mul (2 * N ^ 2)
  unfold FN
  refine h3.congr_deriv ?_
  have e1 : (1 + x / N) ^ (1 - N - 1) = (1 + x / N) ^ (-N) := by ring_nf
  have e2 : (1 + x / N) ^ (2 - N - 1) = (1 + x / N) ^ (1 - N) := by ring_nf
  have e3 : (1 + x / N) ^ (1 - N) = (1 + x / N) * (1 + x / N) ^ (-N) := by
    rw [show (1 - N) = 1 + (-N) by ring, Real.rpow_add hu0, Real.rpow_one]
  rw [e1, e2, e3]
  have hN1 : N - 1 ≠ 0 := by linarith
  have hN2 : N - 2 ≠ 0 := by linarith
  field_simp
  ring

theorem FN_tendsto {N : ℝ} (hN : 2 < N) : Tendsto (FN N) atTop (𝓝 0) := by
  have hN0 : 0 < N := by linarith
  have hu : Tendsto (fun x : ℝ => 1 + x / N) atTop atTop :=
    tendsto_atTop_add_const_left _ _ (tendsto_id.atTop_div_const hN0)
  have h1 : Tendsto (fun x : ℝ => (1 + x / N) ^ (1 - N)) atTop (𝓝 0) := by
    have := (tendsto_rpow_neg_atTop (y := N - 1) (by linarith)).comp hu
    simpa [Function.comp_def, show -(N - 1) = 1 - N by ring] using this
  have h2 : Tendsto (fun x : ℝ => (1 + x / N) ^ (2 - N)) atTop (𝓝 0) := by
    have := (tendsto_rpow_neg_atTop (y := N - 2) (by linarith)).comp hu
    simpa [Function.comp_def, show -(N - 2) = 2 - N by ring] using this
  have := ((h1.div_const (N - 1)).sub (h2.div_const (N - 2))).const_mul (2 * N ^ 2)
  have hF : FN N = fun x => 2 * N ^ 2 * ((1 + x / N) ^ (1 - N) / (N - 1) - (1 + x / N) ^ (2 - N) / (N - 2)) := rfl
  rw [hF]
  simpa using this

theorem offset_integral {N : ℝ} (hN : 2 < N) :
    IntegrableOn (fun x : ℝ => (1 + x / N) ^ (-N) * (2 * x)) (Ioi 0) ∧
    ∫ x in Ioi (0:ℝ), (1 + x / N) ^ (-N) * (2 * x) = cN N := by
  have hN0 : 0 < N := by linarith
  have hcont : ContinuousWithinAt (FN N) (Ici 0) 0 := (FN_deriv hN le_rfl).continuousAt.continuousWithinAt
  have hder : ∀ x ∈ Ioi (0:ℝ), HasDerivAt (FN N) ((1 + x / N) ^ (-N) * (2 * x)) x :=
    fun x hx => FN_deriv hN (le_of_lt hx)
  have hint : IntegrableOn (fun x : ℝ => (1 + x / N) ^ (-N) * (2 * x)) (Ioi 0) :=
    integrableOn_Ioi_deriv_of_nonneg hcont hder (fun x hx => by
      have : 0 < x := hx
      positivity) (FN_tendsto hN)
  refine ⟨hint, ?_⟩
  rw [integral_Ioi_of_hasDerivAt_of_tendsto hcont hder hint (FN_tendsto hN)]
  have hN1 : N - 1 ≠ 0 := by linarith
  have hN2 : N - 2 ≠ 0 := by linarith
  unfold FN cN
  simp
  field_simp
  ring

/-- N = 2: the integrand 2x(1 + x/2)^(-2) is NOT integrable on (0, infinity): the offset coefficient of the record's N = 2 shape diverges -/
theorem offset_N2_not_integrable : ¬ IntegrableOn (fun x : ℝ => (1 + x / 2) ^ (-(2:ℝ)) * (2 * x)) (Ioi 0) := by
  intro h
  have h2 : IntegrableOn (fun x : ℝ => (1 + x / 2) ^ (-(2:ℝ)) * (2 * x)) (Ioi 2) := h.mono_set (Ioi_subset_Ioi (by norm_num))
  have h4 : IntegrableOn (fun x : ℝ => 2 * x ^ (-(1:ℝ))) (Ioi 2) := by
    refine h2.mono' ?_ ?_
    · exact ((continuousOn_const.mul (continuousOn_id.rpow_const (fun x hx => Or.inl (by simp at hx ⊢; linarith)))).aestronglyMeasurable measurableSet_Ioi)
    · refine (ae_restrict_iff' measurableSet_Ioi).mpr (Filter.Eventually.of_forall (fun x hx => ?_))
      have hx2 : 2 < x := hx
      have hx0 : 0 < x := by linarith
      have hb : 0 ≤ 1 + x / 2 := by positivity
      rw [Real.rpow_neg_one, Real.norm_eq_abs, abs_of_pos (by positivity), Real.rpow_neg hb, Real.rpow_two]
      have hsq : (1 + x / 2) ^ 2 ≤ x ^ 2 := by nlinarith
      calc 2 * x⁻¹ = (x ^ 2)⁻¹ * (2 * x) := by field_simp
        _ ≤ ((1 + x / 2) ^ 2)⁻¹ * (2 * x) := mul_le_mul_of_nonneg_right (inv_anti₀ (by positivity) hsq) (by positivity)
  have h3 : IntegrableOn (fun x : ℝ => x ^ (-(1:ℝ))) (Ioi 2) := by
    have := h4.const_mul (1 / 2)
    show Integrable (fun x : ℝ => x ^ (-(1:ℝ))) (volume.restrict (Ioi 2))
    simpa [← mul_assoc, show (1 / 2 : ℝ) * 2 = 1 by norm_num] using this
  have := (integrableOn_Ioi_rpow_iff (s := -(1:ℝ)) (t := 2) (by norm_num)).mp h3
  norm_num at this

end OffsetIntegral

noncomputable def Nstar : ℝ := (3 + Real.sqrt (1 + 1 / π)) / 2

theorem Nstar_props : 2 < Nstar ∧ (Nstar - 1) * (Nstar - 2) = 1 / (4 * π) ∧ 2.0740 < Nstar ∧ Nstar < 2.0742 ∧
    0.4821 < 1 / Nstar ∧ 1 / Nstar < 0.4822 := by
  have hp := Real.pi_pos
  have h1 := Real.pi_gt_d4
  have h2 := Real.pi_lt_d4
  have hq : 0 ≤ 1 + 1 / π := by positivity
  have ht2 := Real.sq_sqrt hq
  set t := Real.sqrt (1 + 1 / π) with htdef
  have ht0 : 0 ≤ t := Real.sqrt_nonneg _
  have hinv1 : 0.3183 < 1 / π := by rw [lt_div_iff₀ hp]; nlinarith
  have hinv2 : 1 / π < 0.31833 := by rw [div_lt_iff₀ hp]; nlinarith
  have htl : 1.1481 < t := by nlinarith
  have htu : t < 1.1482 := by nlinarith
  have hN1 : 2.0740 < Nstar := by unfold Nstar; rw [← htdef]; linarith
  have hN2 : Nstar < 2.0742 := by unfold Nstar; rw [← htdef]; linarith
  refine ⟨by linarith, ?_, hN1, hN2, ?_, ?_⟩
  · unfold Nstar; rw [← htdef]
    have : 1 / (4 * π) = (1 / π) / 4 := by field_simp
    rw [this]; nlinarith [ht2]
  · rw [lt_div_iff₀ (by linarith)]; nlinarith
  · rw [div_lt_iff₀ (by linarith)]; nlinarith

/-- N = 2 (kappa = 1/2) is not a solution -/
theorem N_two_marginal : (2 - 1) * (2 - 2 : ℝ) ≠ 1 / (4 * π) := by
  have hp := Real.pi_pos
  norm_num

/-- c(N) -> +infinity as N -> 2+ : the marginal member -/
theorem cN_blowup (M : ℝ) : ∃ δ : ℝ, 0 < δ ∧ ∀ N : ℝ, 2 < N → N < 2 + δ → M < cN N := by
  refine ⟨min 1 (2 / (|M| + 1)), by positivity, ?_⟩
  intro N hN1 hN2
  have hδ1 : min 1 (2 / (|M| + 1)) ≤ 1 := min_le_left _ _
  have hδ2 : min 1 (2 / (|M| + 1)) ≤ 2 / (|M| + 1) := min_le_right _ _
  set δ := min 1 (2 / (|M| + 1)) with hδ
  have hδ0 : 0 < δ := by positivity
  have hA : 0 ≤ |M| := abs_nonneg M
  have h1 : 0 < N - 1 := by linarith
  have h2 : 0 < N - 2 := by linarith
  have hq : 0 < (N - 1) * (N - 2) := by positivity
  have hq2 : (N - 1) * (N - 2) < 2 * δ := by nlinarith
  have hδA : δ * (|M| + 1) ≤ 2 := by
    have := mul_le_mul_of_nonneg_right hδ2 (by positivity : (0:ℝ) ≤ |M| + 1)
    have h3 : 2 / (|M| + 1) * (|M| + 1) = 2 := by field_simp
    linarith
  unfold cN
  rw [lt_div_iff₀ hq]
  have hM := le_abs_self M
  have hN4 : 4 < N ^ 2 := by nlinarith
  have : M * ((N - 1) * (N - 2)) ≤ |M| * (2 * δ) := by
    calc M * ((N - 1) * (N - 2)) ≤ |M| * ((N - 1) * (N - 2)) := by nlinarith
      _ ≤ |M| * (2 * δ) := by nlinarith
  nlinarith

/-- the record's OR shape mu_N(x) = 1 - (1 + x/N)^(-N) (N > 0) satisfies the bathtub hypotheses: continuous on [0, infinity), mu_N <= x (Bernoulli/exp) and mu_N <= 1 -/
theorem orMu_le_x {N x : ℝ} (hN : 0 < N) (hx : 0 ≤ x) : 1 - (1 + x / N) ^ (-N) ≤ x := by
  have hu : 0 < 1 + x / N := by positivity
  have h1 : 1 + x / N ≤ Real.exp (x / N) := by linarith [Real.add_one_le_exp (x / N)]
  have h2 : (1 + x / N) ^ N ≤ (Real.exp (x / N)) ^ N := Real.rpow_le_rpow hu.le h1 hN.le
  have h3 : (Real.exp (x / N)) ^ N = Real.exp x := by
    rw [← Real.exp_mul]; congr 1; field_simp
  rw [h3] at h2
  have h4 : (Real.exp x)⁻¹ ≤ ((1 + x / N) ^ N)⁻¹ := inv_anti₀ (Real.rpow_pos_of_pos hu N) h2
  rw [← Real.exp_neg] at h4
  have h5 : (1 + x / N) ^ (-N) = ((1 + x / N) ^ N)⁻¹ := Real.rpow_neg hu.le N
  have h6 : -x + 1 ≤ Real.exp (-x) := Real.add_one_le_exp (-x)
  linarith

theorem orMu_admissible {N : ℝ} (hN : 0 < N) :
    ContinuousOn (fun x : ℝ => 1 - (1 + x / N) ^ (-N)) (Set.Ici 0) ∧ (∀ x : ℝ, 0 ≤ x → 1 - (1 + x / N) ^ (-N) ≤ x) ∧
    (∀ x : ℝ, 0 ≤ x → 1 - (1 + x / N) ^ (-N) ≤ 1) := by
  refine ⟨?_, fun x hx => orMu_le_x hN hx, fun x hx => ?_⟩
  · apply continuousOn_const.sub
    apply ContinuousOn.rpow_const (continuousOn_const.add (continuousOn_id.div_const N))
    intro x hx
    left
    have : 0 ≤ x := hx
    have : 0 < 1 + x / N := by positivity
    exact this.ne'
  · have hu : 0 < 1 + x / N := by positivity
    have := Real.rpow_pos_of_pos hu (-N)
    linarith

/-- there is NO universal upper bound on the offset coefficient c: admissible shapes (slope <= 1, mu_N <= min(x,1)) with c > M for every M -/
theorem no_upper_bound (M : ℝ) : ∃ N : ℝ, 2 < N ∧
    ContinuousOn (fun x : ℝ => 1 - (1 + x / N) ^ (-N)) (Set.Ici 0) ∧ (∀ x : ℝ, 0 ≤ x → 1 - (1 + x / N) ^ (-N) ≤ x) ∧
    (∀ x : ℝ, 0 ≤ x → 1 - (1 + x / N) ^ (-N) ≤ 1) ∧
    M < ∫ x in Set.Ioi (0:ℝ), (1 - (1 - (1 + x / N) ^ (-N))) * (2 * x) := by
  obtain ⟨δ, hδ, h⟩ := cN_blowup M
  have hN : 2 < 2 + δ / 2 := by linarith
  have hN0 : 0 < 2 + δ / 2 := by linarith
  obtain ⟨hc, hle, h1⟩ := orMu_admissible hN0
  refine ⟨2 + δ / 2, hN, hc, hle, h1, ?_⟩
  have e : (fun x : ℝ => (1 - (1 - (1 + x / (2 + δ / 2)) ^ (-(2 + δ / 2)))) * (2 * x)) =
      fun x => (1 + x / (2 + δ / 2)) ^ (-(2 + δ / 2)) * (2 * x) := by funext x; ring
  rw [e, (offset_integral hN).2]
  exact h (2 + δ / 2) hN (by linarith)

/-! (e) W lane: rational carriers -/

/-- rho_Lambda A_dS = 6 F_max (F_max = c^4/(4G) = 1/4) for EVERY L: an identity of Lambda, c, G alone -/
theorem F_Lambda {L : ℝ} (hL : L ≠ 0) : (3 / (8 * π * L ^ 2)) * (4 * π * L ^ 2) = 6 * (1 / 4) := by
  have hp := Real.pi_pos
  field_simp
  ring

/-- Sigma_Lambda = rho R* (R* = 1/sqrt rho) equals 4 pi Sigma_M (Sigma_M = a0/(2 pi)) iff G rho = 4 a0^2 -/
theorem sheet {ρ a0 : ℝ} (hρ : 0 < ρ) (ha : 0 < a0) : ρ * (1 / Real.sqrt ρ) = 4 * π * (a0 / (2 * π)) ↔ ρ = 4 * a0 ^ 2 := by
  have hp := Real.pi_pos
  have hs : 0 < Real.sqrt ρ := Real.sqrt_pos.mpr hρ
  have h2 := Real.sq_sqrt hρ.le
  have hL : ρ * (1 / Real.sqrt ρ) = Real.sqrt ρ := by
    rw [mul_one_div, div_eq_iff hs.ne']; nlinarith [h2]
  have hR : 4 * π * (a0 / (2 * π)) = 2 * a0 := by field_simp; ring
  rw [hL, hR]
  constructor
  · intro h; rw [← h2, h]; ring
  · intro h
    have : Real.sqrt ρ ^ 2 = (2 * a0) ^ 2 := by rw [h2, h]; ring
    have := sq_eq_sq₀ hs.le (by positivity) |>.mp this
    exact this

/-- the cubic lattice of masses m at spacing l: a_nn = G m/l^2, rho = m/l^3: a_nn^2 = G rho (G m/l); a0 = a_nn and a0^2 = G rho/4 iff G m/l = 1/4 -/
theorem lattice {G m l : ℝ} (hG : 0 < G) (hm : 0 < m) (hl : 0 < l) :
    (G * m / l ^ 2) ^ 2 = G * (m / l ^ 3) * (G * m / l) ∧ ((G * m / l ^ 2) ^ 2 = G * (m / l ^ 3) / 4 ↔ G * m / l = 1 / 4) := by
  have hl0 : l ≠ 0 := hl.ne'
  have hpos : 0 < G * (m / l ^ 3) := by positivity
  refine ⟨by field_simp, ?_⟩
  have e : (G * m / l ^ 2) ^ 2 = G * (m / l ^ 3) * (G * m / l) := by field_simp
  rw [e]
  constructor
  · intro h
    have : G * (m / l ^ 3) * (G * m / l - 1 / 4) = 0 := by nlinarith [h]
    rcases mul_eq_zero.mp this with h1 | h1
    · exact absurd h1 hpos.ne'
    · linarith
  · intro h; rw [h]; ring

/-- Newtonian Lambda thresholds: acceleration -GM/r^2 + (Lambda/3) r = 0 at r^3 = 3GM/Lambda, mean density 2 rho_Lambda;
    outermost stable circular orbit r^3 = 3GM/(4 Lambda), mean density 8 rho_Lambda (rho_Lambda = Lambda/(8 pi G)) -/
theorem thresholds {G M Λ r : ℝ} (hG : 0 < G) (hM : 0 < M) (hΛ : 0 < Λ) :
    (r ^ 3 = 3 * G * M / Λ → 3 * M / (4 * π * r ^ 3) = 2 * (Λ / (8 * π * G))) ∧
    (r ^ 3 = 3 * G * M / (4 * Λ) → 3 * M / (4 * π * r ^ 3) = 8 * (Λ / (8 * π * G))) := by
  have hp := Real.pi_pos
  constructor
  · intro h; rw [h]; field_simp; ring
  · intro h; rw [h]; field_simp

end OffsetFamily

#print axioms OffsetFamily.offset_iff
#print axioms OffsetFamily.c_req
#print axioms OffsetFamily.c_req_Z
#print axioms OffsetFamily.poisson_no_rational
#print axioms OffsetFamily.poisson_no_algebraic
#print axioms OffsetFamily.mu_le_x
#print axioms OffsetFamily.mu_le_x_instance
#print axioms OffsetFamily.bathtub_bound
#print axioms OffsetFamily.sharp_value
#print axioms OffsetFamily.steep_value
#print axioms OffsetFamily.cN_eq_iff
#print axioms OffsetFamily.FN_deriv
#print axioms OffsetFamily.FN_tendsto
#print axioms OffsetFamily.offset_integral
#print axioms OffsetFamily.offset_N2_not_integrable
#print axioms OffsetFamily.Nstar_props
#print axioms OffsetFamily.N_two_marginal
#print axioms OffsetFamily.cN_blowup
#print axioms OffsetFamily.orMu_le_x
#print axioms OffsetFamily.orMu_admissible
#print axioms OffsetFamily.no_upper_bound
#print axioms OffsetFamily.F_Lambda
#print axioms OffsetFamily.sheet
#print axioms OffsetFamily.lattice
#print axioms OffsetFamily.thresholds
