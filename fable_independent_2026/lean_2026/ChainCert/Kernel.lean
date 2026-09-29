import Mathlib
import ChainCert.Certificates

/-!
# ChainCert.Kernel -- the headline kernel nu_mono meets the deep-limit premise of C2

nu_mono(y) = 1 / (1 - exp (-sqrt y)).  The general theorem `C2_deep_mond_flat_speed` needs `nu y * sqrt y -> 1` as y -> 0+.
Here it is proved for nu_mono, so the BTFR limit holds for the kernel candidate B actually uses (canonical footing).
-/

open Filter Topology

noncomputable def nuMono (y : ℝ) : ℝ := 1 / (1 - Real.exp (-Real.sqrt y))

/-- s / (1 - exp (-s)) -> 1 as s -> 0+ (the derivative of exp at 0 is 1). -/
theorem nuMono_aux : Tendsto (fun s : ℝ => s / (1 - Real.exp (-s))) (𝓝[>] 0) (𝓝 1) := by
  have h1 : HasDerivAt (fun s : ℝ => Real.exp (-s)) (-1) 0 := by
    simpa using (hasDerivAt_neg (0:ℝ)).exp
  have h : HasDerivAt (fun s : ℝ => 1 - Real.exp (-s)) 1 0 := by
    simpa using h1.const_sub 1
  have hslope : Tendsto (fun s : ℝ => (1 - Real.exp (-s)) / s) (𝓝[>] 0) (𝓝 1) := by
    have := h.tendsto_slope_zero_right
    refine this.congr' ?_
    filter_upwards [self_mem_nhdsWithin] with s hs
    simp [div_eq_inv_mul]
  have hinv := hslope.inv₀ (by norm_num : (1:ℝ) ≠ 0)
  rw [inv_one] at hinv
  refine hinv.congr' ?_
  filter_upwards [self_mem_nhdsWithin] with s hs
  simp [inv_div]

theorem nuMono_deep : Tendsto (fun y : ℝ => nuMono y * Real.sqrt y) (𝓝[>] 0) (𝓝 1) := by
  have hs : Tendsto Real.sqrt (𝓝[>] (0:ℝ)) (𝓝[>] 0) := by
    refine tendsto_nhdsWithin_iff.mpr ⟨?_, ?_⟩
    · have := (Real.continuous_sqrt.tendsto 0).mono_left (nhdsWithin_le_nhds (s := Set.Ioi (0:ℝ)))
      simpa using this
    · filter_upwards [self_mem_nhdsWithin] with y hy
      exact Real.sqrt_pos.mpr hy
  have := nuMono_aux.comp hs
  refine this.congr' ?_
  filter_upwards [self_mem_nhdsWithin] with y hy
  simp only [Function.comp, nuMono]
  rw [one_div, inv_mul_eq_div, div_eq_mul_inv]

/-- the BTFR limit for nu_mono, composed with a0 = kappa c sqrt(G rho_Lambda) -/
theorem nuMono_btfr_from_vacuum {G M κ c ρΛ : ℝ} (hG : 0 < G) (hM : 0 < M) (hκ : 0 < κ) (hc : 0 < c)
    (hρ : 0 < ρΛ) :
    Tendsto (fun r : ℝ => ((G * M / r) * nuMono (G * M / (r ^ 2 * (κ * c * Real.sqrt (G * ρΛ)))))^2)
      atTop (𝓝 (G * M * (κ * c * Real.sqrt (G * ρΛ)))) :=
  C2_deep_mond_flat_speed hG hM (by positivity) nuMono nuMono_deep
