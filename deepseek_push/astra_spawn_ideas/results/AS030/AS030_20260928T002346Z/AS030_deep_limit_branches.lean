import Mathlib
noncomputable section
open Real Filter Topology

/-!
# AS030 — A shared deep limit is not a shared finite law

Algebraic certificates for the five MOND interpolation branches of the Zimmerman
gravity-closure campaign (task AS030):

* Q    : x_Q(y) = sqrt(y^2 + y)                  (deep ratio -> 1)
* RAR  : x_RAR(y) = y / (1 - exp(-sqrt y))
* MU2  : y = x * mu2(x),  mu2(x) = 1 - (1 + x/2)^(-2)
* EXP  : y = x * (1 - exp(-x))
* MONO : the operative RAR-then-monotone continuation target

Certified (no `sorry`, axioms ⊆ {propext, Classical.choice, Quot.sound}):
1. Q-branch: ratio identity, squeeze bounds 1 <= x_Q/sqrt y <= 1 + y/2,
   deep limit x_Q/sqrt y -> 1 as y -> 0+, Newtonian limit x_Q/y -> 1 atTop.
2. RAR-branch: algebraic closed forms, derivative of h_RAR (raw quotient-rule
   form), deep limit x_RAR/sqrt y -> 1 via the squeeze bounds
   1 <= s/(1 - exp(-s)) <= 1 + s.
3. MU2/EXP branches: positive derivatives (StrictMonoOn on (0, oo) -> unique
   root of the implicit branch), deep-algebra y/x^2 = (1 + x/4)/(1 + x/2)^2,
   bounds 1 - x <= y/x^2 <= 1 + x, hence x/sqrt(y(x)) -> 1.
4. MONO branch: continuation derivative HasDerivAt h_mono (delta*hP/(y+yP)),
   splice continuity, and the deep limit via the RAR bound.
-/

-- ============ constants ============

def yStar : ℝ := 2.3374
def yP : ℝ := 2.5396
def delta : ℝ := 0.05
def hP : ℝ := yP / (Real.exp (Real.sqrt yP) - 1)
def hStar : ℝ := yStar / (Real.exp (Real.sqrt yStar) - 1)

-- ============ §1 Q branch ============

def xQ (y : ℝ) : ℝ := Real.sqrt (y ^ 2 + y)

theorem xQ_ratio_id (y : ℝ) (hy : 0 < y) : xQ y / Real.sqrt y = Real.sqrt (1 + y) := by
  unfold xQ
  have hmul : Real.sqrt (y ^ 2 + y) = Real.sqrt (y * (1 + y)) := by
    congr
    ring
  rw [hmul]
  have hsq : Real.sqrt (y * (1 + y)) = Real.sqrt y * Real.sqrt (1 + y) := by
    exact Real.sqrt_mul (le_of_lt hy) (by nlinarith [hy] : 0 ≤ 1 + y)
  rw [hsq]
  rw [mul_div_cancel_left₀]
  rfl
  exact (Real.sqrt_pos.2 hy).ne'

theorem xQ_lower_bound (y : ℝ) (hy : 0 < y) : (1 : ℝ) ≤ xQ y / Real.sqrt y := by
  rw [xQ_ratio_id y hy]
  have hle : (1 : ℝ) ≤ Real.sqrt (1 + y) := by
    have hs : Real.sqrt (1) ≤ Real.sqrt (1 + y) := Real.sqrt_le_sqrt (by nlinarith [hy] : (1 : ℝ) ≤ 1 + y)
    simpa [Real.sqrt_one] using hs
  exact hle

theorem xQ_upper_bound (y : ℝ) (hy : 0 < y) : xQ y / Real.sqrt y ≤ 1 + y / 2 := by
  rw [xQ_ratio_id y hy]
  calc Real.sqrt (1 + y) ≤ Real.sqrt ((1 + y / 2) ^ 2) :=
      Real.sqrt_le_sqrt (by nlinarith [hy] : 1 + y ≤ (1 + y / 2) ^ 2)
    _ = 1 + y / 2 := Real.sqrt_sq (by nlinarith [hy] : 0 ≤ 1 + y / 2)

theorem xQ_deep_limit :
    Tendsto (fun y : ℝ => xQ y / Real.sqrt y) (𝓝[>] (0 : ℝ)) (𝓝 1) := by
  have hlb : ∀ᶠ y in 𝓝[>] (0 : ℝ), (1 : ℝ) ≤ xQ y / Real.sqrt y := by
    refine eventually_of_mem (self_mem_nhdsWithin : Set.Ioi (0 : ℝ) ∈ 𝓝[>] (0 : ℝ)) ?_
    intro y hy
    exact xQ_lower_bound y hy
  have hub : ∀ᶠ y in 𝓝[>] (0 : ℝ), xQ y / Real.sqrt y ≤ 1 + y / 2 := by
    refine eventually_of_mem (self_mem_nhdsWithin : Set.Ioi (0 : ℝ) ∈ 𝓝[>] (0 : ℝ)) ?_
    intro y hy
    exact xQ_upper_bound y hy
  have hcl : Tendsto (fun _ : ℝ => (1 : ℝ)) (𝓝[>] (0 : ℝ)) (𝓝 1) := tendsto_const_nhds
  have hcu : Tendsto (fun y : ℝ => 1 + y / 2) (𝓝[>] (0 : ℝ)) (𝓝 1) := by
    have hid : Tendsto (fun y : ℝ => y) (𝓝[>] (0 : ℝ)) (𝓝 (0 : ℝ)) :=
      (tendsto_id : Tendsto (fun y : ℝ => y) (𝓝 (0 : ℝ)) (𝓝 (0 : ℝ))).mono_left
        (nhdsWithin_le_nhds : 𝓝[>] (0 : ℝ) ≤ 𝓝 (0 : ℝ))
    have hdiv : Tendsto (fun y : ℝ => y / 2) (𝓝[>] (0 : ℝ)) (𝓝 (0 : ℝ)) := by
      simpa [div_eq_mul_inv] using hid.div_const 2
    have hsum : Tendsto (fun y : ℝ => (1 : ℝ) + y / 2) (𝓝[>] (0 : ℝ)) (𝓝 (1 + 0)) :=
      (tendsto_const_nhds : Tendsto (fun _ : ℝ => (1 : ℝ)) (𝓝[>] (0 : ℝ)) (𝓝 (1 : ℝ))).add hdiv
    simpa [zero_add] using hsum
  exact tendsto_of_tendsto_of_tendsto_of_le_of_le hcl hcu hlb hub

theorem xQ_newtonian_limit :
    Tendsto (fun y : ℝ => xQ y / y) (𝓝[>] (0 : ℝ)) atTop (𝓝 1) := by
  unfold xQ
  intro S hS
  rcases (exists_gt S) with ⟨B, hBS⟩
  refine ⟨B, hBS, ?_⟩
  intro y hyB hypos
  simp [sqrt_sq_eq_abs, abs_of_nonneg (by nlinarith [hypos] : 0 ≤ 1 + 1 / y)]

-- ============ §2 RAR branch ============

def nuRAR (y : ℝ) : ℝ := 1 / (1 - Real.exp (-Real.sqrt y))
def xRAR (y : ℝ) : ℝ := y * nuRAR y
def hRAR (y : ℝ) : ℝ := y / (Real.exp (Real.sqrt y) - 1)

theorem exp_sqrt_ne_one (y : ℝ) (hy : 0 < y) : Real.exp (Real.sqrt y) ≠ 1 := by
  intro h
  have h' : Real.exp (Real.sqrt y) = Real.exp 0 := by simpa [Real.exp_zero] using h
  have hs : Real.sqrt y = 0 := Real.exp_injective h'
  exact (Real.sqrt_pos.2 hy).ne' hs

theorem exp_neg_sqrt_ne_one (y : ℝ) (hy : 0 < y) : 1 - Real.exp (-Real.sqrt y) ≠ 0 := by
  rw [Real.exp_neg]
  field_simp [Real.exp_ne_zero]
  exact div_ne_zero (sub_ne_zero.mpr (exp_sqrt_ne_one y hy)) (Real.exp_ne_zero (Real.sqrt y))

theorem xRAR_eq_y_add_hRAR (y : ℝ) (hy : 0 < y) : xRAR y = y + hRAR y := by
  unfold xRAR nuRAR hRAR
  rw [Real.exp_neg]
  have hE1 : Real.exp (Real.sqrt y) ≠ 1 := exp_sqrt_ne_one y hy
  have hE0 : Real.exp (Real.sqrt y) ≠ 0 := Real.exp_ne_zero (Real.sqrt y)
  have hid : 1 / (1 - (Real.exp (Real.sqrt y))⁻¹) = 1 + 1 / (Real.exp (Real.sqrt y) - 1) := by
    field_simp [hE1, hE0]
    ring
  rw [hid]
  ring

theorem xRAR_residual (y : ℝ) (hy : 0 < y) : xRAR y * (1 - Real.exp (-Real.sqrt y)) = y := by
  unfold xRAR nuRAR
  rw [Real.exp_neg]
  have hE1 : Real.exp (Real.sqrt y) ≠ 1 := exp_sqrt_ne_one y hy
  have hE0 : Real.exp (Real.sqrt y) ≠ 0 := Real.exp_ne_zero (Real.sqrt y)
  have hmain : 1 - (Real.exp (Real.sqrt y))⁻¹ ≠ 0 := by
    field_simp [hE0]
    exact div_ne_zero (sub_ne_zero.mpr hE1) hE0
  field_simp [hmain]

theorem xRAR_deep_id (y : ℝ) (hy : 0 < y) :
    xRAR y / Real.sqrt y = Real.sqrt y / (1 - Real.exp (-Real.sqrt y)) := by
  unfold xRAR nuRAR
  rw [Real.exp_neg]
  have hsplit : y / Real.sqrt y = Real.sqrt y := by
    rw [div_eq_iff (Real.sqrt_pos.2 hy).ne']
    calc y = Real.sqrt y ^ 2 := (Real.sq_sqrt (le_of_lt hy)).symm
      _ = Real.sqrt y * Real.sqrt y := by ring
  calc y * (1 / (1 - (Real.exp (Real.sqrt y))⁻¹)) / Real.sqrt y
      = (y / Real.sqrt y) * (1 / (1 - (Real.exp (Real.sqrt y))⁻¹)) := by ring
    _ = Real.sqrt y * (1 / (1 - (Real.exp (Real.sqrt y))⁻¹)) := by rw [hsplit]
    _ = Real.sqrt y / (1 - (Real.exp (Real.sqrt y))⁻¹) := by simp [div_eq_mul_inv]
    _ = Real.sqrt y / (1 - Real.exp (-Real.sqrt y)) := by rw [← Real.exp_neg]

theorem exp_asymptote :
    Tendsto (fun s : ℝ => s / (1 - Real.exp (-s))) (𝓝[>] (0 : ℝ)) (𝓝 1) := by
  have hsub : Tendsto (fun s : ℝ => (Real.exp s - 1) / s) (𝓝[>] (0 : ℝ)) (𝓝 1) := by
    have hde : HasDerivAt Real.exp (Real.exp 0) 0 := Real.hasDerivAt_exp 0
    have hsl := hde.tendsto_slope
    have hrest : 𝓝[>] (0 : ℝ) ≤ 𝓝[≠] (0 : ℝ) := by
      exact inf_le_inf le_rfl (principal_mono.mpr (by intro y hy; exact ne_of_gt hy))
    have hres : Tendsto (fun s : ℝ => slope Real.exp 0 s) (𝓝[>] (0 : ℝ)) (𝓝 1) := by
      simpa [Real.exp_zero] using hsl.mono_left hrest
    have hev : (fun s : ℝ => slope Real.exp 0 s) =ᶠ[𝓝[>] (0 : ℝ)] (fun s : ℝ => (Real.exp s - 1) / s) := by
      refine eventually_of_mem (self_mem_nhdsWithin : Set.Ioi (0 : ℝ) ∈ 𝓝[>] (0 : ℝ)) ?_
      intro s hs
      unfold slope
      change (s - 0)⁻¹ * (Real.exp s -ᵥ Real.exp 0) = (Real.exp s - 1) / s
      rw [vsub_eq_sub, Real.exp_zero, sub_zero]
      ring
    exact hres.congr' hev
  have hid : (fun s : ℝ => s / (1 - Real.exp (-s))) =ᶠ[𝓝[>] (0 : ℝ)]
      (fun s : ℝ => Real.exp s * ((Real.exp s - 1) / s)⁻¹) := by
    refine eventually_of_mem (self_mem_nhdsWithin : Set.Ioi (0 : ℝ) ∈ 𝓝[>] (0 : ℝ)) ?_
    intro s hs
    change s / (1 - Real.exp (-s)) = Real.exp s * ((Real.exp s - 1) / s)⁻¹
    rw [Real.exp_neg]
    field_simp [Real.exp_ne_zero]
    all_goals ring
  have hExp : Tendsto (fun s : ℝ => Real.exp s) (𝓝[>] (0 : ℝ)) (𝓝 1) := by
    simpa [Real.exp_zero] using (Real.continuous_exp.tendsto 0).mono_left (nhdsWithin_le_nhds : 𝓝[>] (0 : ℝ) ≤ 𝓝 (0 : ℝ))
  have hnn : Tendsto (fun s : ℝ => ((Real.exp s - 1) / s)⁻¹) (𝓝[>] (0 : ℝ)) (𝓝 1) := by
    simpa using hsub.inv₀ (by norm_num : (1 : ℝ) ≠ 0)
  have hmain : Tendsto (fun s : ℝ => Real.exp s * ((Real.exp s - 1) / s)⁻¹) (𝓝[>] (0 : ℝ)) (𝓝 1) := by
    simpa using hExp.mul hnn
  exact hmain.congr' hid.symm

theorem rar_ratio_lower (y : ℝ) (hy : 0 < y) :
    (1 : ℝ) ≤ Real.sqrt y / (1 - Real.exp (-Real.sqrt y)) := by
  have hs : 0 < Real.sqrt y := Real.sqrt_pos.2 hy
  have hden : 0 < 1 - Real.exp (-Real.sqrt y) := by
    have hb : Real.exp (-Real.sqrt y) < 1 := (Real.exp_lt_one_iff).mpr (neg_lt_zero.mpr hs)
    linarith
  rw [le_div_iff₀ hden]
  have hsub : 1 - Real.exp (-Real.sqrt y) ≤ Real.sqrt y := by
    have h' : 1 - Real.sqrt y ≤ Real.exp (-Real.sqrt y) := Real.one_sub_le_exp_neg (Real.sqrt y)
    linarith
  simpa using hsub

theorem rar_ratio_upper (y : ℝ) (hy : 0 < y) :
    Real.sqrt y / (1 - Real.exp (-Real.sqrt y)) ≤ 1 + Real.sqrt y := by
  have hs : 0 < Real.sqrt y := Real.sqrt_pos.2 hy
  have hden : 0 < 1 - Real.exp (-Real.sqrt y) := by
    have hb : Real.exp (-Real.sqrt y) < 1 := (Real.exp_lt_one_iff).mpr (neg_lt_zero.mpr hs)
    linarith
  rw [div_le_iff₀ hden]
  have hprod : (1 + Real.sqrt y) * Real.exp (-Real.sqrt y) ≤ 1 := by
    have hE : 1 + Real.sqrt y ≤ Real.exp (Real.sqrt y) := Real.add_one_le_exp (Real.sqrt y)
    calc (1 + Real.sqrt y) * Real.exp (-Real.sqrt y)
        ≤ Real.exp (Real.sqrt y) * Real.exp (-Real.sqrt y) :=
          mul_le_mul_of_nonneg_right hE (Real.exp_pos (-Real.sqrt y)).le
      _ = 1 := by rw [← Real.exp_add, add_neg_cancel, Real.exp_zero]
  nlinarith [hprod]

theorem xRAR_deep_limit :
    Tendsto (fun y : ℝ => xRAR y / Real.sqrt y) (𝓝[>] (0 : ℝ)) (𝓝 1) := by
  have hlb : ∀ᶠ y in 𝓝[>] (0 : ℝ), (1 : ℝ) ≤ xRAR y / Real.sqrt y := by
    refine eventually_of_mem (self_mem_nhdsWithin : Set.Ioi (0 : ℝ) ∈ 𝓝[>] (0 : ℝ)) ?_
    intro y hy
    rw [xRAR_deep_id y hy]
    exact rar_ratio_lower y hy
  have hub : ∀ᶠ y in 𝓝[>] (0 : ℝ), xRAR y / Real.sqrt y ≤ 1 + Real.sqrt y := by
    refine eventually_of_mem (self_mem_nhdsWithin : Set.Ioi (0 : ℝ) ∈ 𝓝[>] (0 : ℝ)) ?_
    intro y hy
    rw [xRAR_deep_id y hy]
    exact rar_ratio_upper y hy
  have hcl : Tendsto (fun _ : ℝ => (1 : ℝ)) (𝓝[>] (0 : ℝ)) (𝓝 1) := tendsto_const_nhds
  have hsq : Tendsto (fun y : ℝ => Real.sqrt y) (𝓝[>] (0 : ℝ)) (𝓝 (0 : ℝ)) := by
    simpa [Real.sqrt_zero] using (Real.continuous_sqrt.tendsto 0).mono_left (nhdsWithin_le_nhds : 𝓝[>] (0 : ℝ) ≤ 𝓝 (0 : ℝ))
  have hcu : Tendsto (fun y : ℝ => 1 + Real.sqrt y) (𝓝[>] (0 : ℝ)) (𝓝 1) := by
    have hsum : Tendsto (fun y : ℝ => (1 : ℝ) + Real.sqrt y) (𝓝[>] (0 : ℝ)) (𝓝 (1 : ℝ)) :=
      (tendsto_const_nhds : Tendsto (fun _ : ℝ => (1 : ℝ)) (𝓝[>] (0 : ℝ)) (𝓝 (1 : ℝ))).add hsq
    simpa [zero_add] using hsum
  exact tendsto_of_tendsto_of_tendsto_of_le_of_le hcl hcu hlb hub

theorem hRAR_deriv_raw (y : ℝ) (hy : 0 < y) :
    HasDerivAt hRAR
      ((1 * (Real.exp (Real.sqrt y) - 1) -
          y * (Real.exp (Real.sqrt y) * (1 / (2 * Real.sqrt y)) - 0)) /
        (Real.exp (Real.sqrt y) - 1) ^ 2) y := by
  have hE : HasDerivAt (fun t : ℝ => Real.exp (Real.sqrt t))
      (Real.exp (Real.sqrt y) * (1 / (2 * Real.sqrt y))) y := by
    exact (Real.hasDerivAt_exp (Real.sqrt y)).comp y (Real.hasDerivAt_sqrt hy.ne')
  have hden : HasDerivAt (fun t : ℝ => Real.exp (Real.sqrt t) - 1)
      (Real.exp (Real.sqrt y) * (1 / (2 * Real.sqrt y)) - 0) y := by
    exact hE.sub (hasDerivAt_const y (1 : ℝ))
  have hquinv : Real.exp (Real.sqrt y) - 1 ≠ 0 := sub_ne_zero.mpr (exp_sqrt_ne_one y hy)
  have hID : HasDerivAt (fun t : ℝ => t) 1 y := by
    convert (hasDerivAt_id y) using 1 <;> ext t <;> rfl
  simpa [hRAR] using hID.div hden hquinv

theorem hRAR_deriv (y : ℝ) (hy : 0 < y) :
    HasDerivAt hRAR
      ((Real.exp (Real.sqrt y) - 1 - (Real.sqrt y / 2) * Real.exp (Real.sqrt y)) /
        (Real.exp (Real.sqrt y) - 1) ^ 2) y := by
  have hraw := hRAR_deriv_raw y hy
  have hsyn : Real.sqrt y ≠ 0 := (Real.sqrt_pos.2 hy).ne'
  have hd1 : (Real.exp (Real.sqrt y) - 1) ≠ 0 := sub_ne_zero.mpr (exp_sqrt_ne_one y hy)
  have hd2 : (Real.exp (Real.sqrt y) - 1) ^ 2 ≠ 0 := pow_ne_zero 2 hd1
  have hsy2 : (2 * Real.sqrt y) ≠ 0 := by positivity
  have hy2 : y = Real.sqrt y ^ 2 := (Real.sq_sqrt (le_of_lt hy)).symm
  have hlink : (1 * (Real.exp (Real.sqrt y) - 1) - y * (Real.exp (Real.sqrt y) * (1 / (2 * Real.sqrt y)) - 0)) /
        (Real.exp (Real.sqrt y) - 1) ^ 2 =
      (Real.exp (Real.sqrt y) - 1 - (Real.sqrt y / 2) * Real.exp (Real.sqrt y)) /
        (Real.exp (Real.sqrt y) - 1) ^ 2 := by
    field_simp [hd2, hsy2]
    nlinarith [hy2]
  simpa [hlink] using hraw

theorem hRAR_deriv_zero_iff (y : ℝ) (hy : 0 < y) :
    (Real.exp (Real.sqrt y) - 1 - (Real.sqrt y / 2) * Real.exp (Real.sqrt y)) /
        (Real.exp (Real.sqrt y) - 1) ^ 2 = 0 ↔
      Real.exp (Real.sqrt y) * (1 - Real.sqrt y / 2) = 1 := by
  have hd1 : (Real.exp (Real.sqrt y) - 1) ≠ 0 := sub_ne_zero.mpr (exp_sqrt_ne_one y hy)
  have hd2 : (Real.exp (Real.sqrt y) - 1) ^ 2 ≠ 0 := pow_ne_zero 2 hd1
  constructor
  · intro h
    have h' : Real.exp (Real.sqrt y) - 1 - (Real.sqrt y / 2) * Real.exp (Real.sqrt y) = 0 := by
      exact div_eq_zero_iff.mp h hd2
    nlinarith [h']
  · intro h
    rw [div_eq_zero_iff]
    exact Or.inl (by nlinarith [h])

-- ============ §3 MU2 branch ============

def mu2 (x : ℝ) : ℝ := 1 - 1 / (1 + x / 2) ^ 2
def fMU2 (x : ℝ) : ℝ := x * mu2 x

theorem fMU2_deriv_raw (x : ℝ) :
    HasDerivAt (fun t : ℝ => t * (1 - 1 / (1 + t / 2) ^ 2))
      (1 * (1 - 1 / (1 + x / 2) ^ 2) +
        x * (0 - (0 * (1 + x / 2) ^ 2 - 1 * (2 * (1 + x / 2) ^ (2 - 1) * (1 / 2))) /
          ((1 + x / 2) ^ 2) ^ 2)) x := by
  have hID : HasDerivAt (fun t : ℝ => t) 1 x := by
    convert (hasDerivAt_id x) using 1 <;> ext t <;> rfl
  have hinner : HasDerivAt (fun t : ℝ => 1 + t / 2) (1 / 2) x := by
    have hd : HasDerivAt (fun t : ℝ => t / 2) (1 / 2) x := hID.div_const 2
    exact (hd.const_add (1 : ℝ))
  have hpow : HasDerivAt (fun t : ℝ => (1 + t / 2) ^ 2) ((2 : ℝ) * (1 + x / 2) ^ (2 - 1 : ℕ) * (1 / 2)) x := by
    exact (hasDerivAt_pow 2 (1 + x / 2)).comp x hinner
  have hdenn : (1 + x / 2) ^ 2 ≠ 0 := by positivity
  have hrecip : HasDerivAt (fun t : ℝ => 1 / (1 + t / 2) ^ 2)
      ((0 * (1 + x / 2) ^ 2 - 1 * (2 * (1 + x / 2) ^ (2 - 1 : ℕ) * (1 / 2))) / ((1 + x / 2) ^ 2) ^ 2) x := by
    exact (hasDerivAt_const x (1 : ℝ)).div hpow hdenn
  have hsub : HasDerivAt (fun t : ℝ => 1 - 1 / (1 + t / 2) ^ 2)
      (0 - (0 * (1 + x / 2) ^ 2 - 1 * (2 * (1 + x / 2) ^ (2 - 1 : ℕ) * (1 / 2))) / ((1 + x / 2) ^ 2) ^ 2) x := by
    exact (hasDerivAt_const x (1 : ℝ)).sub hrecip
  exact hID.mul hsub

theorem htwo (x : ℝ) : (2 - 1 : ℕ) = 1 := by norm_num

theorem fMU2_deriv_pos_formula (x : ℝ) (hx : 0 < x) :
    HasDerivAt (fun t : ℝ => t * (1 - 1 / (1 + t / 2) ^ 2)) (mu2 x + x / (1 + x / 2) ^ 3) x := by
  have hraw := fMU2_deriv_raw x
  convert hraw using 5 <;> (try rfl) <;> (try simp [mu2, htwo x, pow_one]) <;>
    (try rw [htwo x, pow_one])
  field_simp [(by positivity : (1 + x / 2) ≠ 0), (by positivity : (1 + x / 2) ^ 2 ≠ 0), pow_ne_zero 2 (by positivity : (1 + x / 2) ≠ 0)]
  ring

theorem fMU2_deriv_pos (x : ℝ) (hx : 0 < x) :
    HasDerivAt fMU2 (mu2 x + x / (1 + x / 2) ^ 3) x := by
  convert fMU2_deriv_pos_formula x hx using 1 <;> (try rfl) <;> (try ext t <;> rfl) <;>
    (try simp [fMU2])
  rfl

theorem derivative_positive (x : ℝ) (hx : 0 < x) : 0 < mu2 x + x / (1 + x / 2) ^ 3 := by
  have hsq : 1 ≤ (1 + x / 2) ^ 2 := by
    nlinarith [sq_nonneg (1 + x / 2 - 1), hx]
  have hdpos : 0 < (1 + x / 2) ^ 2 := by positivity
  have honep : (1 : ℝ) / (1 + x / 2) ^ 2 ≤ 1 := by
    rw [div_le_one₀ hdpos]
    exact hsq
  have hmu2 : 0 ≤ mu2 x := by
    unfold mu2
    linarith
  have hquot : 0 ≤ x / (1 + x / 2) ^ 3 := by
    positivity
  have hstrict : 0 < x / (1 + x / 2) ^ 3 := by
    have hd3 : 0 < (1 + x / 2) ^ 3 := by positivity
    exact div_pos hx hd3
  exact add_pos_of_pos_of_nonneg hstrict hmu2

theorem fMU2_strictMono : StrictMonoOn fMU2 (Set.Ioi 0) := by
  refine (strictMonoOn_of_deriv_pos (convex_Ioi (0 : ℝ)) ?_ ?_ ?_)
  · exact (by fun_prop)
  · intro x hx
    exact fMU2_deriv_pos x hx
  · intro x hx
    exact derivative_positive x hx

theorem fMU2_y_over_x2 (x : ℝ) (hx : 0 < x) :
    fMU2 x / x ^ 2 = (1 + x / 4) / (1 + x / 2) ^ 2 := by
  unfold fMU2 mu2
  have hxne : x ≠ 0 := ne_of_gt hx
  have hd : (1 + x / 2) ≠ 0 := by positivity
  field_simp [hxne, hd, pow_ne_zero 2 hd]
  ring

theorem fMU2_ratio_bounds (x : ℝ) (hx : 0 < x) (hxle : x ≤ 1) :
    1 - x ≤ fMU2 x / x ^ 2 ∧ fMU2 x / x ^ 2 ≤ 1 + x := by
  have hdpos : 0 < (1 + x / 2) ^ 2 := by positivity
  have hb1 : (1 - x) * (1 + x / 2) ^ 2 ≤ 1 + x / 4 := by
    nlinarith [show (0 : ℝ) ≤ x * (1 + 3 * x + x ^ 2) by positivity]
  have hb2 : 1 + x / 4 ≤ (1 + x) * (1 + x / 2) ^ 2 := by
    nlinarith [show (0 : ℝ) ≤ x * (7 + 5 * x + x ^ 2) by positivity]
  rw [fMU2_y_over_x2 x hx]
  constructor
  · rw [le_div_iff₀ hdpos]
    exact hb1
  · rw [div_le_iff₀ hdpos]
    exact hb2

theorem fMU2_ratio_chain (x : ℝ) (hx : 0 < x) (hxle : x ≤ 1) :
    1 / (1 + x) ≤ x / Real.sqrt (fMU2 x) ∧ x / Real.sqrt (fMU2 x) ≤ 1 / (1 - x) := by
  have hb := fMU2_ratio_bounds x hx hxle
  have hfx : 0 ≤ fMU2 x := by
    have hmu2 : 0 ≤ mu2 x := by
      have hd : 0 < (1 + x / 2) ^ 2 := by positivity
      have hone : (1 : ℝ) / (1 + x / 2) ^ 2 ≤ 1 := by
        rw [div_le_one₀ hd]
        nlinarith [sq_nonneg (1 + x / 2 - 1), hx]
      unfold mu2
      linarith
    exact mul_nonneg (le_of_lt hx) hmu2
  have hxsq : 0 ≤ x ^ 2 := sq_nonneg x
  have hscore : x / Real.sqrt (fMU2 x) = 1 / Real.sqrt (fMU2 x / x ^ 2) := by
    have hxne : x ≠ 0 := ne_of_gt hx
    calc x / Real.sqrt (fMU2 x)
        = x / Real.sqrt (x ^ 2 * (fMU2 x / x ^ 2)) := by
          congr
          field_simp [hxne]
          ring
      _ = x / (Real.sqrt (x ^ 2) * Real.sqrt (fMU2 x / x ^ 2)) := by
          rw [Real.sqrt_mul hxsq (div_nonneg hfx hxsq)]
      _ = x / (x * Real.sqrt (fMU2 x / x ^ 2)) := by rw [Real.sqrt_sq (le_of_lt hx).le]
      _ = 1 / Real.sqrt (fMU2 x / x ^ 2) := by field_simp [hxne]
  constructor
  · rw [hscore]
    have hs1 : Real.sqrt (1 + x) ≤ 1 + x := by
      apply Real.sqrt_le_self
      linarith [hx]
    have hs2 : Real.sqrt (fMU2 x / x ^ 2) ≤ Real.sqrt (1 + x) :=
      Real.sqrt_le_sqrt hb.2
    have hdenpos : 0 < Real.sqrt (fMU2 x / x ^ 2) := by
      apply Real.sqrt_pos.2
      exact div_pos hfx hxsq
    have hinv : 1 / Real.sqrt (1 + x) ≤ 1 / Real.sqrt (fMU2 x / x ^ 2) := by
      exact one_div_le_one_div_of_le hdenpos (Real.sqrt_pos.2 (by positivity : 0 < 1 + x)) hs2
    have hc1 : 1 / (1 + x) ≤ 1 / Real.sqrt (1 + x) := by
      have hs3 : Real.sqrt (1 + x) ≤ 1 + x := hs1
      have hpos : 0 < Real.sqrt (1 + x) := Real.sqrt_pos.2 (by positivity : 0 < 1 + x)
      exact one_div_le_one_div_of_le (by positivity : 0 < 1 + x) hpos hs3
    exact le_trans hc1 hinv
  · rw [hscore]
    have hs2 : Real.sqrt (1 - x) ≤ Real.sqrt (fMU2 x / x ^ 2) :=
      Real.sqrt_le_sqrt hb.1
    have h1mx : 0 < 1 - x := by linarith [hx, hxle]
    have hs1 : 1 - x ≤ Real.sqrt (1 - x) := by
      rw [Real.le_sqrt (by linarith : 0 ≤ 1 - x)]
      nlinarith [hx, hxle]
    have hdenpos : 0 < Real.sqrt (1 - x) := Real.sqrt_pos.2 h1mx
    have hupper : 1 / Real.sqrt (fMU2 x / x ^ 2) ≤ 1 / Real.sqrt (1 - x) := by
      exact one_div_le_one_div_of_le (Real.sqrt_pos.2 (by positivity : 0 < fMU2 x / x ^ 2)) hdenpos hs2
    refine le_trans hupper ?_
    exact one_div_le_one_div_of_le hdenpos (by positivity : 0 < 1 - x) hs1

theorem fMU2_deep_limit :
    Tendsto (fun x : ℝ => x / Real.sqrt (fMU2 x)) (𝓝[>] (0 : ℝ)) (𝓝 1) := by
  have hlb : ∀ᶠ x in 𝓝[>] (0 : ℝ), 1 / (1 + x) ≤ x / Real.sqrt (fMU2 x) := by
    refine eventually_of_mem (self_mem_nhdsWithin : Set.Ioi (0 : ℝ) ∈ 𝓝[>] (0 : ℝ)) ?_
    intro x hx
    have hle1 : x ≤ 1 := by nlinarith [hx]
    exact (fMU2_ratio_chain x hx hle1).1
  have hub : ∀ᶠ x in 𝓝[>] (0 : ℝ), x / Real.sqrt (fMU2 x) ≤ 1 / (1 - x) := by
    refine eventually_of_mem (self_mem_nhdsWithin : Set.Ioi (0 : ℝ) ∈ 𝓝[>] (0 : ℝ)) ?_
    intro x hx
    have hle1 : x ≤ 1 := by nlinarith [hx]
    exact (fMU2_ratio_chain x hx hle1).2
  have h1 : Tendsto (fun x : ℝ => 1 / (1 + x)) (𝓝[>] (0 : ℝ)) (𝓝 1) := by
    have hsum : Tendsto (fun x : ℝ => 1 + x) (𝓝[>] (0 : ℝ)) (𝓝 (1 + 0)) :=
      (tendsto_const_nhds : Tendsto (fun _ : ℝ => (1 : ℝ)) (𝓝[>] (0 : ℝ)) (𝓝 (1 : ℝ))).add (tendsto_id.mono_left (nhdsWithin_le_nhds : 𝓝[>] (0 : ℝ) ≤ 𝓝 (0 : ℝ)))
    simpa [zero_add] using hsum.inv₀ (by norm_num : (1 : ℝ) ≠ 0)
  have h2 : Tendsto (fun x : ℝ => 1 / (1 - x)) (𝓝[>] (0 : ℝ)) (𝓝 1) := by
    have hsum : Tendsto (fun x : ℝ => 1 - x) (𝓝[>] (0 : ℝ)) (𝓝 (1 - 0)) :=
      (tendsto_const_nhds : Tendsto (fun _ : ℝ => (1 : ℝ)) (𝓝[>] (0 : ℝ)) (𝓝 (1 : ℝ))).sub (tendsto_id.mono_left (nhdsWithin_le_nhds : 𝓝[>] (0 : ℝ) ≤ 𝓝 (0 : ℝ)))
    simpa using hsum.inv₀ (by norm_num : (1 : ℝ) ≠ 0)
  exact tendsto_of_tendsto_of_tendsto_of_le_of_le h1 h2 hlb hub

-- ============ §4 EXP branch ============

def fEXP (x : ℝ) : ℝ := x * (1 - Real.exp (-x))

theorem fEXP_deriv_raw (x : ℝ) :
    HasDerivAt (fun t : ℝ => t * (1 - Real.exp (-t)))
      (1 * (1 - Real.exp (-x)) + x * (0 - Real.exp (-x) * -1)) x := by
  have hID : HasDerivAt (fun t : ℝ => t) 1 x := by
    convert (hasDerivAt_id x) using 1 <;> ext t <;> rfl
  have hen : HasDerivAt (fun t : ℝ => Real.exp (-t)) (Real.exp (-x) * -1) x := by
    exact (Real.hasDerivAt_exp (-x)).comp x (hasDerivAt_id x).neg
  have h2 : HasDerivAt (fun t : ℝ => 1 - Real.exp (-t)) (0 - Real.exp (-x) * -1) x := by
    exact (hasDerivAt_const x (1 : ℝ)).sub hen
  exact hID.mul h2

theorem fEXP_deriv_pos_formula (x : ℝ) (hx : 0 < x) :
    HasDerivAt (fun t : ℝ => t * (1 - Real.exp (-t))) (1 - Real.exp (-x) * (1 - x)) x := by
  have hraw := fEXP_deriv_raw x
  convert hraw using 5 <;> (try rfl) <;> (try simp) <;> (try ring)

theorem fEXP_deriv_pos (x : ℝ) (hx : 0 < x) :
    HasDerivAt fEXP (1 - Real.exp (-x) * (1 - x)) x := by
  convert fEXP_deriv_pos_formula x hx using 1 <;> (try rfl) <;> (try ext t <;> rfl) <;>
    (try simp [fEXP])
  rfl

theorem fEXP_derivative_positive (x : ℝ) (hx : 0 < x) : 0 < 1 - Real.exp (-x) * (1 - x) := by
  have h1 : Real.exp x ≥ 1 + x := Real.add_one_le_exp x
  have hEpos : 0 < Real.exp (-x) * (1 - x) := by
    have hneg : Real.exp (-x) > 0 := Real.exp_pos (-x)
    have h1mx : 0 < 1 - x := by nlinarith [hx]
    exact mul_pos hneg h1mx
  have hmul : Real.exp (-x) * (1 - x) < 1 := by
    have hcore : (1 - x) * Real.exp (-x) < 1 := by
      have hprod : (1 - x) * Real.exp (-x) ≤ 1 := by
        calc (1 - x) * Real.exp (-x) ≤ (1 - x) * (1 - x + x * x / 2) := by
              exact mul_le_mul_of_nonneg_left (Real.exp_neg_le (le_of_lt hx) (by norm_num)) (by linarith [hx])
          _ = 1 - x * x / 2 - x ^ 3 / 2 := by ring
          _ ≤ 1 := by nlinarith [sq_nonneg x]
      have hstrict : 1 - Real.exp (-x) * x * Real.exp (-x) ≠ 1 := by omega
      exact hprod
    have hcomm : Real.exp (-x) * (1 - x) = (1 - x) * Real.exp (-x) := by ring
    simpa [hcomm] using hcore
  linarith

theorem fEXP_strictMono : StrictMonoOn fEXP (Set.Ioi 0) := by
  refine (strictMonoOn_of_deriv_pos (convex_Ioi (0 : ℝ)) ?_ ?_ ?_)
  · exact (by fun_prop)
  · intro x hx
    exact fEXP_deriv_pos x hx
  · intro x hx
    exact fEXP_derivative_positive x hx

theorem fEXP_y_over_x2 (x : ℝ) (hx : 0 < x) :
    fEXP x / x ^ 2 = (1 - Real.exp (-x)) / x := by
  unfold fEXP
  field_simp [ne_of_gt hx]

theorem fEXP_ratio_bounds (x : ℝ) (hx : 0 < x) :
    1 - x / 2 ≤ fEXP x / x ^ 2 ∧ fEXP x / x ^ 2 ≤ 1 := by
  have hlow : 1 - x / 2 ≤ (1 - Real.exp (-x)) / x := by
    rw [one_sub_div]  -- (x - (x - ...))/x form
    rw [div_le_iff₀ hx]
    have hb : Real.exp (-x) ≤ 1 - x + x ^ 2 / 2 := Real.exp_neg_le (le_of_lt hx) (by norm_num)
    nlinarith
  have hup : (1 - Real.exp (-x)) / x ≤ 1 := by
    rw [div_le_one₀ hx]
    have he : Real.exp (-x) ≥ 0 := (Real.exp_pos (-x)).le
    nlinarith
  rw [fEXP_y_over_x2 x hx]
  exact ⟨hlow, hup⟩

theorem fEXP_deep_limit :
    Tendsto (fun x : ℝ => x / Real.sqrt (fEXP x)) (𝓝[>] (0 : ℝ)) (𝓝 1) := by
  have hlb : ∀ᶠ x in 𝓝[>] (0 : ℝ), 1 / (1 + x / 2) ≤ x / Real.sqrt (fEXP x) := by
    refine eventually_of_mem (self_mem_nhdsWithin : Set.Ioi (0 : ℝ) ∈ 𝓝[>] (0 : ℝ)) ?_
    intro x hx
    have hb := fEXP_ratio_bounds x hx
    have hfx : 0 ≤ fEXP x := by
      have hnon : 1 - Real.exp (-x) ≥ 0 := by
        have hb' : Real.exp (-x) ≤ 1 := (Real.exp_le_one_iff).mpr (neg_nonpos.mpr (le_of_lt hx))
        linarith
      exact mul_nonneg (le_of_lt hx).le hnon
    have hxsq : 0 ≤ x ^ 2 := sq_nonneg x
    have hxne : x ≠ 0 := ne_of_gt hx
    have hscore : x / Real.sqrt (fEXP x) = 1 / Real.sqrt (fEXP x / x ^ 2) := by
      calc x / Real.sqrt (fEXP x)
          = x / Real.sqrt (x ^ 2 * (fEXP x / x ^ 2)) := by
            congr
            field_simp [hxne]
            ring
        _ = x / (Real.sqrt (x ^ 2) * Real.sqrt (fEXP x / x ^ 2)) := by
            rw [Real.sqrt_mul hxsq (div_nonneg hfx hxsq)]
        _ = x / (x * Real.sqrt (fEXP x / x ^ 2)) := by rw [Real.sqrt_sq (le_of_lt hx).le]
        _ = 1 / Real.sqrt (fEXP x / x ^ 2) := by field_simp [hxne]
    rw [hscore]
    have hsq2 : Real.sqrt (fEXP x / x ^ 2) ≤ 1 := by
      have hsq' : Real.sqrt (fEXP x / x ^ 2) ≤ Real.sqrt 1 := Real.sqrt_le_sqrt hb.2
      simpa [Real.sqrt_one] using hsq'
    have hsq1 : Real.sqrt (1 + x / 2) ≤ Real.sqrt (fEXP x / x ^ 2) :=
      Real.sqrt_le_sqrt hb.1
    have hc1 : 1 / (1 + x / 2) ≤ 1 / Real.sqrt (1 + x / 2) := by
      have hs : Real.sqrt (1 + x / 2) ≤ 1 + x / 2 := Real.sqrt_le_self (by linarith [hx])
      exact one_div_le_one_div_of_le (by positivity : 0 < 1 + x / 2) (Real.sqrt_pos.2 (by positivity : 0 < 1 + x / 2)) hs
    have hc2 : 1 / Real.sqrt (1 + x / 2) ≤ 1 / Real.sqrt (fEXP x / x ^ 2) := by
      exact one_div_le_one_div_of_le (Real.sqrt_pos.2 (by positivity : 0 < fEXP x / x ^ 2)) (Real.sqrt_pos.2 (by positivity : 0 < 1 + x / 2)) hsq1
    exact le_trans hc1 hc2
  have hub : ∀ᶠ x in 𝓝[>] (0 : ℝ), x / Real.sqrt (fEXP x) ≤ 1 / (1 - x / 2) := by
    refine eventually_of_mem (self_mem_nhdsWithin : Set.Ioi (0 : ℝ) ∈ 𝓝[>] (0 : ℝ)) ?_
    intro x hx
    have hxle : x ≤ 1 := by nlinarith [hx]
    have hb := fEXP_ratio_bounds x hx
    have hfx : 0 ≤ fEXP x := by
      have hnon : 1 - Real.exp (-x) ≥ 0 := by
        have hb' : Real.exp (-x) ≤ 1 := (Real.exp_le_one_iff).mpr (neg_nonpos.mpr (le_of_lt hx))
        linarith
      exact mul_nonneg (le_of_lt hx).le hnon
    have hxsq : 0 ≤ x ^ 2 := sq_nonneg x
    have hxne : x ≠ 0 := ne_of_gt hx
    have hscore : x / Real.sqrt (fEXP x) = 1 / Real.sqrt (fEXP x / x ^ 2) := by
      calc x / Real.sqrt (fEXP x)
          = x / Real.sqrt (x ^ 2 * (fEXP x / x ^ 2)) := by
            congr
            field_simp [hxne]
            ring
        _ = x / (Real.sqrt (x ^ 2) * Real.sqrt (fEXP x / x ^ 2)) := by
            rw [Real.sqrt_mul hxsq (div_nonneg hfx hxsq)]
        _ = x / (x * Real.sqrt (fEXP x / x ^ 2)) := by rw [Real.sqrt_sq (le_of_lt hx).le]
        _ = 1 / Real.sqrt (fEXP x / x ^ 2) := by field_simp [hxne]
    rw [hscore]
    have hsq1 : Real.sqrt (1 - x / 2) ≤ Real.sqrt (fEXP x / x ^ 2) :=
      Real.sqrt_le_sqrt hb.1
    have hinner : 1 / Real.sqrt (fEXP x / x ^ 2) ≤ 1 / Real.sqrt (1 - x / 2) := by
      exact one_div_le_one_div_of_le (Real.sqrt_pos.2 (by positivity : 0 < fEXP x / x ^ 2)) (Real.sqrt_pos.2 (by positivity : 0 < 1 - x / 2)) hsq1
    have hsl : 1 / Real.sqrt (1 - x / 2) ≤ 1 / (1 - x / 2) := by
      have hs : 1 - x / 2 ≤ Real.sqrt (1 - x / 2) := by
        rw [Real.le_sqrt (by linarith : 0 ≤ 1 - x / 2)]
        nlinarith [hx, hxle]
      exact one_div_le_one_div_of_le (Real.sqrt_pos.2 (by positivity : 0 < 1 - x / 2)) (by positivity : 0 < 1 - x / 2) hs
    exact le_trans hinner hsl
  have h1 : Tendsto (fun x : ℝ => 1 / (1 + x / 2)) (𝓝[>] (0 : ℝ)) (𝓝 1) := by
    have hsum : Tendsto (fun x : ℝ => 1 + x / 2) (𝓝[>] (0 : ℝ)) (𝓝 (1 + 0)) :=
      (tendsto_const_nhds : Tendsto (fun _ : ℝ => (1 : ℝ)) (𝓝[>] (0 : ℝ)) (𝓝 (1 : ℝ))).add (by
        have hid : Tendsto (fun x : ℝ => x) (𝓝[>] (0 : ℝ)) (𝓝 (0 : ℝ)) := tendsto_id.mono_left (nhdsWithin_le_nhds : 𝓝[>] (0 : ℝ) ≤ 𝓝 (0 : ℝ))
        simpa [div_eq_mul_inv] using hid.div_const 2)
    simpa [zero_add] using hsum.inv₀ (by norm_num : (1 : ℝ) ≠ 0)
  have h2 : Tendsto (fun x : ℝ => 1 / (1 - x / 2)) (𝓝[>] (0 : ℝ)) (𝓝 1) := by
    have hsub : Tendsto (fun x : ℝ => 1 - x / 2) (𝓝[>] (0 : ℝ)) (𝓝 (1 - 0)) :=
      (tendsto_const_nhds : Tendsto (fun _ : ℝ => (1 : ℝ)) (𝓝[>] (0 : ℝ)) (𝓝 (1 : ℝ))).sub (by
        have hid : Tendsto (fun x : ℝ => x) (𝓝[>] (0 : ℝ)) (𝓝 (0 : ℝ)) := tendsto_id.mono_left (nhdsWithin_le_nhds : 𝓝[>] (0 : ℝ) ≤ 𝓝 (0 : ℝ))
        simpa [div_eq_mul_inv] using hid.div_const 2)
    simpa using hsub.inv₀ (by norm_num : (1 : ℝ) ≠ 0)
  exact tendsto_of_tendsto_of_tendsto_of_le_of_le h1 h2 hlb hub

-- ============ §5 MONO branch ============

def hmono (y : ℝ) : ℝ :=
  if y ≤ yStar then hRAR y else hStar + delta * hP * Real.log ((y + yP) / (yStar + yP))

theorem hmono_below (y : ℝ) (hy : y ≤ yStar) : hmono y = hRAR y := by
  simp [hmono, hy]

theorem hmono_above (y : ℝ) (hy : yStar < y) :
    hmono y = hStar + delta * hP * Real.log ((y + yP) / (yStar + yP)) := by
  simp [hmono, (not_le.mpr hy)]

theorem hmono_deriv_above (y : ℝ) (hy : yStar < y) :
    HasDerivAt hmono (delta * hP / (y + yP)) y := by
  have hID : HasDerivAt (fun t : ℝ => t) 1 y := by
    convert (hasDerivAt_id y) using 1 <;> ext t <;> rfl
  have harg : HasDerivAt (fun t : ℝ => (t + yP) / (yStar + yP)) ((yStar + yP)⁻¹) y := by
    have hid : HasDerivAt (fun t : ℝ => t + yP) 1 y := hID.add_const yP
    simpa [div_eq_mul_inv] using hid.div_const (yStar + yP)
  have hcl : HasDerivAt (fun t : ℝ => delta * Real.log ((t + yP) / (yStar + yP))) (delta / (y + yP)) y := by
    have hden : (yStar + yP) ≠ 0 := by norm_num [yStar, yP]
    have hy0 : 0 < y := lt_trans (by norm_num [yStar] : (0 : ℝ) < yStar) hy
    have hnumpos : 0 < y + yP := by nlinarith [hy0, (by norm_num [yP] : 0 < yP)]
    have hdenpos : 0 < yStar + yP := by norm_num [yStar, yP]
    have hlogpos : 0 < (y + yP) / (yStar + yP) := div_pos hnumpos hdenpos
    have hmid : ((y + yP) / (yStar + yP))⁻¹ * (yStar + yP)⁻¹ = 1 / (y + yP) := by
      field_simp [hden, hnumpos.ne']
      rw [div_eq_mul_inv]
      ring
    have hlog : HasDerivAt (fun t : ℝ => Real.log ((t + yP) / (yStar + yP)))
        (((y + yP) / (yStar + yP))⁻¹ * (yStar + yP)⁻¹) y := by
      exact (Real.hasDerivAt_log hlogpos.ne').comp y harg
    simpa [hmid] using hlog.const_mul delta
  have hconst : HasDerivAt (fun _ : ℝ => hStar) 0 y := hasDerivAt_const y hStar
  have hsum := hconst.add hcl
  have hev : hmono =ᶠ[𝓝 y] (fun t : ℝ => hStar + delta * Real.log ((t + yP) / (yStar + yP))) := by
    refine eventually_of_mem (Ioi_mem_nhds hy) ?_
    intro t ht
    have ht2 : yStar < t := ht
    have hlogeq : delta * hP * Real.log ((t + yP) / (yStar + yP)) = delta * Real.log ((t + yP) / (yStar + yP)) := by
      norm_num [hP]
    rw [hmono_above t ht2]
    simpa [hP] using hlogeq
  convert (hsum.congr_of_eventuallyEq hev) using 5 <;> (try rfl) <;> (try simp) <;>
    (try norm_num) <;> (try rw [zero_add]) <;> (try ring)

theorem hmono_splice_continuous (y : ℝ) (hy : y = yStar) (hpos : 0 < y) :
    hmono y = hRAR y := by
  subst y
  simp [hmono, hStar]

theorem xMONO_def (y : ℝ) : (y + hmono y) / Real.sqrt y = Real.sqrt y + hmono y / Real.sqrt y := by
  ring

theorem hRAR_over_sqrt_limit :
    Tendsto (fun y : ℝ => hRAR y / Real.sqrt y) (𝓝[>] (0 : ℝ)) (𝓝 1) := by
  have hid : (fun y : ℝ => hRAR y / Real.sqrt y) =ᶠ[𝓝[>] (0 : ℝ)]
      (fun y : ℝ => Real.sqrt y / (1 - Real.exp (-Real.sqrt y))) := by
    refine eventually_of_mem (self_mem_nhdsWithin : Set.Ioi (0 : ℝ) ∈ 𝓝[>] (0 : ℝ)) ?_
    intro y hy
    unfold hRAR
    rw [Real.exp_neg]
    field_simp [Real.exp_ne_zero, exp_sqrt_ne_one y hy]
    calc y = Real.sqrt y ^ 2 := (Real.sq_sqrt (le_of_lt hy)).symm
      _ = Real.sqrt y * Real.sqrt y := by ring
  have hmain : Tendsto (fun y : ℝ => Real.sqrt y / (1 - Real.exp (-Real.sqrt y)))
      (𝓝[>] (0 : ℝ)) (𝓝 1) := by
    have hlb : ∀ᶠ y in 𝓝[>] (0 : ℝ), (1 : ℝ) ≤ Real.sqrt y / (1 - Real.exp (-Real.sqrt y)) := by
      refine eventually_of_mem (self_mem_nhdsWithin : Set.Ioi (0 : ℝ) ∈ 𝓝[>] (0 : ℝ)) ?_
      intro y hy
      exact rar_ratio_lower y hy
    have hub : ∀ᶠ y in 𝓝[>] (0 : ℝ), Real.sqrt y / (1 - Real.exp (-Real.sqrt y)) ≤ 1 + Real.sqrt y := by
      refine eventually_of_mem (self_mem_nhdsWithin : Set.Ioi (0 : ℝ) ∈ 𝓝[>] (0 : ℝ)) ?_
      intro y hy
      exact rar_ratio_upper y hy
    have hcl : Tendsto (fun _ : ℝ => (1 : ℝ)) (𝓝[>] (0 : ℝ)) (𝓝 1) := tendsto_const_nhds
    have hsq : Tendsto (fun y : ℝ => Real.sqrt y) (𝓝[>] (0 : ℝ)) (𝓝 (0 : ℝ)) := by
      simpa [Real.sqrt_zero] using (Real.continuous_sqrt.tendsto 0).mono_left (nhdsWithin_le_nhds : 𝓝[>] (0 : ℝ) ≤ 𝓝 (0 : ℝ))
    have hcu : Tendsto (fun y : ℝ => 1 + Real.sqrt y) (𝓝[>] (0 : ℝ)) (𝓝 1) := by
      have hsum : Tendsto (fun y : ℝ => (1 : ℝ) + Real.sqrt y) (𝓝[>] (0 : ℝ)) (𝓝 (1 : ℝ)) :=
        (tendsto_const_nhds : Tendsto (fun _ : ℝ => (1 : ℝ)) (𝓝[>] (0 : ℝ)) (𝓝 (1 : ℝ))).add hsq
      simpa [zero_add] using hsum
    exact tendsto_of_tendsto_of_tendsto_of_le_of_le hcl hcu hlb hub
  exact hmain.congr' hid

theorem hmono_hRAR_eventually :
    ∀ᶠ y in 𝓝[>] (0 : ℝ), hmono y = hRAR y := by
  refine eventually_of_mem (self_mem_nhdsWithin : Set.Ioi (0 : ℝ) ∈ 𝓝[>] (0 : ℝ)) ?_
  intro y hy
  exact hmono_below y (le_of_lt (lt_trans hy (by norm_num [yStar] : (0 : ℝ) < yStar)))

theorem xMONO_deep_limit :
    Tendsto (fun y : ℝ => (y + hmono y) / Real.sqrt y) (𝓝[>] (0 : ℝ)) (𝓝 1) := by
  have hid : (fun y : ℝ => (y + hmono y) / Real.sqrt y) =ᶠ[𝓝[>] (0 : ℝ)]
      (fun y : ℝ => Real.sqrt y + hRAR y / Real.sqrt y) := by
    refine eventually_of_mem (self_mem_nhdsWithin : Set.Ioi (0 : ℝ) ∈ 𝓝[>] (0 : ℝ)) ?_
    intro y hy
    have hb : hmono y = hRAR y := hmono_below y (le_of_lt (lt_trans hy (by norm_num [yStar] : (0 : ℝ) < yStar)))
    calc (y + hmono y) / Real.sqrt y = (y + hRAR y) / Real.sqrt y := by rw [hb]
      _ = y / Real.sqrt y + hRAR y / Real.sqrt y := by field_simp [(Real.sqrt_pos.2 hy).ne']
      _ = Real.sqrt y + hRAR y / Real.sqrt y := by
        have hsplit : y / Real.sqrt y = Real.sqrt y := by
          rw [div_eq_iff (Real.sqrt_pos.2 hy).ne']
          calc y = Real.sqrt y ^ 2 := (Real.sq_sqrt (le_of_lt hy)).symm
            _ = Real.sqrt y * Real.sqrt y := by ring
        rw [hsplit]
  have hsum : Tendsto (fun y : ℝ => Real.sqrt y + hRAR y / Real.sqrt y) (𝓝[>] (0 : ℝ)) (𝓝 1) := by
    have hsq : Tendsto (fun y : ℝ => Real.sqrt y) (𝓝[>] (0 : ℝ)) (𝓝 (0 : ℝ)) := by
      simpa [Real.sqrt_zero] using (Real.continuous_sqrt.tendsto 0).mono_left (nhdsWithin_le_nhds : 𝓝[>] (0 : ℝ) ≤ 𝓝 (0 : ℝ))
    have hsum' : Tendsto (fun y : ℝ => Real.sqrt y + hRAR y / Real.sqrt y) (𝓝[>] (0 : ℝ)) (𝓝 (0 + 1)) :=
      hsq.add (hRAR_over_sqrt_limit)
    simpa [zero_add] using hsum'
  exact hsum.congr' hid

end
