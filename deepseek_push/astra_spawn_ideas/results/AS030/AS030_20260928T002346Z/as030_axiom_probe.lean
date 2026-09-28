import Mathlib
noncomputable section
open Real Filter Topology

/-!
# AS030 — A shared deep limit is not a shared finite law (rebuild, verified)

Orchestrator rebuild (2026-09-28): the worker's 714-line attempt (88 errors) is
preserved in `AS030_deep_limit_branches.lean` + `lean_check.out`. This file is the
verified certificate of the load-bearing algebra:

1. Q: x_Q(y)/sqrt y = sqrt(1+y) exactly on y>0; leading correction exact:
   x_Q/sqrt y - 1 = y/(sqrt(1+y)+1); deep limit x_Q/sqrt y -> 1.
2. RAR: x_RAR/sqrt y = sqrt y/(1 - exp(-sqrt y)); squeeze 1 <= ratio <= 1+sqrt y
   (rar_squeeze_low/up), hence the deep limit -> 1.
3. RAR phantom: x_RAR = y + h_RAR exactly; h_RAR/sqrt y -> 1.
4. MU2: exact deep algebra (1 - (1+x/2)^-2)/x = (1+x/4)/(1+x/2)^2.
5. MONO: hmono = hRAR on the deep regime (y <= yStar), hence the operative
   MONO deep limit equals the RAR one: (y + hmono y)/sqrt y -> 1.

The shared asymptote being certified, the O(1) finite-y separations (Q vs EXP
0.06424 at y=1; MONO vs RAR 1.1443 h_p at y=100) are the numerical negative
control (controls_and_checks.json) — transcendental, no Lean certificate.
-/

def xQ (y : ℝ) : ℝ := Real.sqrt (y ^ 2 + y)
def xRAR (y : ℝ) : ℝ := y / (1 - Real.exp (-Real.sqrt y))
def hRAR (y : ℝ) : ℝ := y * (1 / (1 - Real.exp (-Real.sqrt y)) - 1)

-- ============ §1 Q branch ============

theorem xQ_ratio_id (y : ℝ) (hy : 0 < y) : xQ y / Real.sqrt y = Real.sqrt (1 + y) := by
  unfold xQ
  have hy' : 0 ≤ y := le_of_lt hy
  have h1p : 0 ≤ 1 + y := by nlinarith
  have hfac : y ^ 2 + y = y * (1 + y) := by ring
  have hsq : Real.sqrt (y ^ 2 + y) = Real.sqrt y * Real.sqrt (1 + y) := by
    rw [hfac]
    exact Real.sqrt_mul hy' (1 + y)
  rw [hsq]
  have hsqrt : Real.sqrt y ≠ 0 := (Real.sqrt_pos.2 hy).ne'
  field_simp [hsqrt]

theorem xQ_correction_exact (y : ℝ) (hy : 0 < y) :
    xQ y / Real.sqrt y - 1 = y / (Real.sqrt (1 + y) + 1) := by
  rw [xQ_ratio_id y hy]
  have hsq : Real.sqrt (1 + y) ^ 2 = 1 + y := Real.sq_sqrt (by nlinarith : 0 ≤ 1 + y)
  have hden : Real.sqrt (1 + y) + 1 ≠ 0 := by
    have hpos : 0 < Real.sqrt (1 + y) := Real.sqrt_pos.2 (by nlinarith : 0 < 1 + y)
    nlinarith
  field_simp [hden]
  nlinarith [hsq]

theorem sqrt_one_plus_tendsto_one :
    Tendsto (fun y : ℝ => Real.sqrt (1 + y)) (𝓝[>] (0 : ℝ)) (𝓝 1) := by
  have hadd : Tendsto (fun y : ℝ => 1 + y) (𝓝[>] (0 : ℝ)) (𝓝 (1 : ℝ)) := by
    have h1 : Tendsto (fun _ : ℝ => (1 : ℝ)) (𝓝[>] (0 : ℝ)) (𝓝 (1 : ℝ)) := tendsto_const_nhds
    have h2 : Tendsto (fun y : ℝ => y) (𝓝[>] (0 : ℝ)) (𝓝 (0 : ℝ)) := by
      change Tendsto id (𝓝[>] (0 : ℝ)) (𝓝 (0 : ℝ))
      exact (tendsto_id : Tendsto id (𝓝 (0 : ℝ)) (𝓝 (0 : ℝ))).mono_left
        (nhdsWithin_le_nhds : 𝓝[>] (0 : ℝ) ≤ 𝓝 (0 : ℝ))
    have hsum := h1.add h2
    simpa [add_comm] using hsum
  have hc : Tendsto Real.sqrt (𝓝 (1 : ℝ)) (𝓝 (Real.sqrt (1 : ℝ))) := Real.continuous_sqrt.tendsto 1
  have hcomp := hc.comp hadd
  simpa [Function.comp_def, Real.sqrt_one] using hcomp

theorem xQ_deep_limit : Tendsto (fun y : ℝ => xQ y / Real.sqrt y) (𝓝[>] (0 : ℝ)) (𝓝 1) := by
  have hfg : (fun y : ℝ => Real.sqrt (1 + y)) =ᶠ[𝓝[>] (0 : ℝ)] (fun y : ℝ => xQ y / Real.sqrt y) := by
    refine eventually_of_mem (self_mem_nhdsWithin : Set.Ioi (0 : ℝ) ∈ 𝓝[>] (0 : ℝ)) ?_
    intro y hy
    exact (xQ_ratio_id y hy).symm
  exact Tendsto.congr' hfg sqrt_one_plus_tendsto_one

-- ============ §2 RAR branch ============

theorem rar_den_pos (y : ℝ) (hy : 0 < y) : 0 < 1 - Real.exp (-Real.sqrt y) := by
  have hb : Real.exp (-Real.sqrt y) < 1 :=
    Real.exp_lt_one_iff.mpr (by nlinarith [Real.sqrt_pos.2 hy] : -Real.sqrt y < 0)
  nlinarith

theorem xRAR_ratio_id (y : ℝ) (hy : 0 < y) :
    xRAR y / Real.sqrt y = Real.sqrt y / (1 - Real.exp (-Real.sqrt y)) := by
  unfold xRAR
  have hsqrt : Real.sqrt y ≠ 0 := (Real.sqrt_pos.2 hy).ne'
  have hden : 1 - Real.exp (-Real.sqrt y) ≠ 0 := (rar_den_pos y hy).ne'
  have hy' : 0 ≤ y := le_of_lt hy
  field_simp [hsqrt, hden]
  rw [Real.sq_sqrt hy']

theorem rar_squeeze_low (s : ℝ) (hs : 0 < s) : (1 : ℝ) ≤ s / (1 - Real.exp (-s)) := by
  have hpos : 0 < 1 - Real.exp (-s) := by
    have hb : Real.exp (-s) < 1 := Real.exp_lt_one_iff.mpr (by nlinarith : -s < 0)
    nlinarith
  rw [le_div_iff₀ hpos]
  nlinarith [add_one_le_exp (-s)]

theorem rar_squeeze_up (s : ℝ) (hs : 0 < s) : s / (1 - Real.exp (-s)) ≤ 1 + s := by
  have hpos : 0 < 1 - Real.exp (-s) := by
    have hb : Real.exp (-s) < 1 := Real.exp_lt_one_iff.mpr (by nlinarith : -s < 0)
    nlinarith
  rw [div_le_iff₀ hpos]
  have he : s + 1 ≤ Real.exp s := add_one_le_exp s
  have hen : Real.exp (-s) * Real.exp s = 1 := by
    rw [← Real.exp_add]
    norm_num
  have hm : (s + 1) * Real.exp (-s) ≤ 1 := by
    have hm0 : (s + 1) * Real.exp (-s) ≤ Real.exp s * Real.exp (-s) :=
      mul_le_mul_of_nonneg_right he (Real.exp_pos (-s)).le
    calc
      (s + 1) * Real.exp (-s) ≤ Real.exp s * Real.exp (-s) := hm0
      _ = 1 := by rw [mul_comm, hen]
  nlinarith

theorem xRAR_eq_y_add_hRAR (y : ℝ) (hy : 0 < y) : xRAR y = y + hRAR y := by
  unfold xRAR hRAR
  have hden : 1 - Real.exp (-Real.sqrt y) ≠ 0 := (rar_den_pos y hy).ne'
  field_simp [hden]
  ring

theorem hRAR_over_sqrt_deep_limit :
    Tendsto (fun y : ℝ => hRAR y / Real.sqrt y) (𝓝[>] (0 : ℝ)) (𝓝 1) := by
  have hsqz : Tendsto (fun y : ℝ => Real.sqrt y) (𝓝[>] (0 : ℝ)) (𝓝 (0 : ℝ)) := by
    simpa using (Real.continuous_sqrt.tendsto 0).mono_left
      (nhdsWithin_le_nhds : 𝓝[>] (0 : ℝ) ≤ 𝓝 (0 : ℝ))
  have hlb : ∀ᶠ y in 𝓝[>] (0 : ℝ), (1 : ℝ) ≤ xRAR y / Real.sqrt y := by
    refine eventually_of_mem (self_mem_nhdsWithin : Set.Ioi (0 : ℝ) ∈ 𝓝[>] (0 : ℝ)) ?_
    intro y hy
    rw [xRAR_ratio_id y hy]
    exact rar_squeeze_low (Real.sqrt y) (Real.sqrt_pos.2 hy)
  have hub : ∀ᶠ y in 𝓝[>] (0 : ℝ), xRAR y / Real.sqrt y ≤ 1 + Real.sqrt y := by
    refine eventually_of_mem (self_mem_nhdsWithin : Set.Ioi (0 : ℝ) ∈ 𝓝[>] (0 : ℝ)) ?_
    intro y hy
    rw [xRAR_ratio_id y hy]
    exact rar_squeeze_up (Real.sqrt y) (Real.sqrt_pos.2 hy)
  have hd0 : ∀ᶠ y in 𝓝[>] (0 : ℝ), (0 : ℝ) ≤ xRAR y / Real.sqrt y - 1 := by
    filter_upwards [hlb] with y h; nlinarith
  have hd1 : ∀ᶠ y in 𝓝[>] (0 : ℝ), xRAR y / Real.sqrt y - 1 ≤ Real.sqrt y := by
    filter_upwards [hub] with y h; nlinarith
  have hd : Tendsto (fun y : ℝ => xRAR y / Real.sqrt y - 1) (𝓝[>] (0 : ℝ)) (𝓝 0) :=
    squeeze_zero' hd0 hd1 hsqz
  have hsum : Tendsto (fun y : ℝ => 1 + (xRAR y / Real.sqrt y - 1)) (𝓝[>] (0 : ℝ)) (𝓝 (1 + 0)) :=
    (tendsto_const_nhds : Tendsto (fun _ : ℝ => (1 : ℝ)) (𝓝[>] (0 : ℝ)) (𝓝 1)).add hd
  have hsum1 : Tendsto (fun y : ℝ => 1 + (xRAR y / Real.sqrt y - 1)) (𝓝[>] (0 : ℝ)) (𝓝 1) := by
    simpa [zero_add] using hsum
  have hxr : Tendsto (fun y : ℝ => xRAR y / Real.sqrt y) (𝓝[>] (0 : ℝ)) (𝓝 1) := by
    have hfg : (fun y : ℝ => 1 + (xRAR y / Real.sqrt y - 1)) =ᶠ[𝓝[>] (0 : ℝ)]
        (fun y : ℝ => xRAR y / Real.sqrt y) := by
      filter_upwards with y
      ring
    exact Tendsto.congr' hfg hsum1
  have hsplit : (fun y : ℝ => xRAR y / Real.sqrt y) =ᶠ[𝓝[>] (0 : ℝ)]
      (fun y : ℝ => Real.sqrt y + hRAR y / Real.sqrt y) := by
    refine eventually_of_mem (self_mem_nhdsWithin : Set.Ioi (0 : ℝ) ∈ 𝓝[>] (0 : ℝ)) ?_
    intro y hy
    have hadd : xRAR y = y + hRAR y := xRAR_eq_y_add_hRAR y hy
    have hsqrt : Real.sqrt y ≠ 0 := (Real.sqrt_pos.2 hy).ne'
    have hy' : 0 ≤ y := le_of_lt hy
    change xRAR y / Real.sqrt y = Real.sqrt y + hRAR y / Real.sqrt y
    rw [hadd]
    field_simp [hsqrt]
    rw [Real.sq_sqrt hy']
  have hsub : Tendsto (fun y : ℝ => xRAR y / Real.sqrt y - Real.sqrt y) (𝓝[>] (0 : ℝ)) (𝓝 (1 - 0)) :=
    hxr.sub hsqz
  have hsub1 : Tendsto (fun y : ℝ => xRAR y / Real.sqrt y - Real.sqrt y) (𝓝[>] (0 : ℝ)) (𝓝 1) := by
    simpa [sub_zero] using hsub
  have hfg2 : (fun y : ℝ => xRAR y / Real.sqrt y - Real.sqrt y) =ᶠ[𝓝[>] (0 : ℝ)]
      (fun y : ℝ => hRAR y / Real.sqrt y) := by
    filter_upwards [hsplit] with y h
    nlinarith
  exact Tendsto.congr' hfg2 hsub1

-- ============ §3 MU2 deep algebra ============

theorem mu2_deep_algebra (x : ℝ) (hx : 0 < x) :
    (1 - (1 + x / 2)⁻¹ ^ 2) / x = (1 + x / 4) / (1 + x / 2) ^ 2 := by
  have hx2 : x ≠ 0 := ne_of_gt hx
  have hden : 1 + x / 2 ≠ 0 := by positivity
  have hden2 : (1 + x / 2) ^ 2 ≠ 0 := pow_ne_zero 2 hden
  have ha : (1 + x / 2) ^ 2 - 1 = x * (1 + x / 4) := by ring
  have hinv : (1 + x / 2)⁻¹ ^ 2 = ((1 + x / 2) ^ 2)⁻¹ := by
    rw [← inv_pow]
  rw [hinv]
  have hcore : (1 - ((1 + x / 2) ^ 2)⁻¹) * (1 + x / 2) ^ 2 = (1 + x / 2) ^ 2 - 1 := by
    field_simp [hden2]
  field_simp [hx2, hden2]
  ring

-- ============ §4 MONO: deep regime is the RAR segment ============

def yStar : ℝ := 2.3374
def yP : ℝ := 2.5396
def delta : ℝ := 0.05
def hP : ℝ := yP / (Real.exp (Real.sqrt yP) - 1)
def hStar : ℝ := yStar / (Real.exp (Real.sqrt yStar) - 1)

def hmono (y : ℝ) : ℝ :=
  if y ≤ yStar then hRAR y else hStar + delta * hP * Real.log ((y + yP) / (yStar + yP))

theorem hmono_below_splice (y : ℝ) (hy : y ≤ yStar) : hmono y = hRAR y := by
  simp [hmono, hy]

theorem hmono_deep_eventually :
    ∀ᶠ y in 𝓝[>] (0 : ℝ), (0 : ℝ) < y ∧ hmono y = hRAR y := by
  have hset : Set.Ioo (0 : ℝ) yStar ∈ 𝓝[>] (0 : ℝ) := by
    rw [mem_nhdsWithin]
    refine ⟨Set.Iio yStar, ?_, ?_, ?_⟩
    · exact isOpen_Iio
    · norm_num [yStar]
    · intro y hy
      exact ⟨hy.2, hy.1⟩
  refine eventually_of_mem hset ?_
  intro y hy
  exact ⟨hy.1, hmono_below_splice y (le_of_lt hy.2)⟩

theorem xMONO_deep_limit :
    Tendsto (fun y : ℝ => (y + hmono y) / Real.sqrt y) (𝓝[>] (0 : ℝ)) (𝓝 1) := by
  have hcongr : (fun y : ℝ => (y + hmono y) / Real.sqrt y) =ᶠ[𝓝[>] (0 : ℝ)]
      (fun y : ℝ => Real.sqrt y + hRAR y / Real.sqrt y) := by
    filter_upwards [hmono_deep_eventually] with y hy
    have hb : hmono y = hRAR y := hy.2
    have hy0 : 0 < y := hy.1
    have hsqrt : Real.sqrt y ≠ 0 := (Real.sqrt_pos.2 hy0).ne'
    have hy' : 0 ≤ y := le_of_lt hy0
    rw [hb]
    field_simp [hsqrt]
    rw [Real.sq_sqrt hy']
  have hsqz : Tendsto (fun y : ℝ => Real.sqrt y) (𝓝[>] (0 : ℝ)) (𝓝 (0 : ℝ)) := by
    simpa using (Real.continuous_sqrt.tendsto 0).mono_left
      (nhdsWithin_le_nhds : 𝓝[>] (0 : ℝ) ≤ 𝓝 (0 : ℝ))
  have hsum : Tendsto (fun y : ℝ => Real.sqrt y + hRAR y / Real.sqrt y) (𝓝[>] (0 : ℝ)) (𝓝 (0 + 1)) :=
    hsqz.add hRAR_over_sqrt_deep_limit
  have hsum1 : Tendsto (fun y : ℝ => Real.sqrt y + hRAR y / Real.sqrt y) (𝓝[>] (0 : ℝ)) (𝓝 1) := by
    simpa [zero_add] using hsum
  exact Tendsto.congr' hcongr.symm hsum1

end
/-! # Axiom audit -/
#print axioms xQ_ratio_id
#print axioms xQ_correction_exact
#print axioms xQ_deep_limit
#print axioms hRAR_over_sqrt_deep_limit
#print axioms mu2_deep_algebra
#print axioms xMONO_deep_limit
