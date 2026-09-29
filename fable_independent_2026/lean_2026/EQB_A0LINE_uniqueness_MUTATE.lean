import Mathlib

/-!
# EQB_A0LINE -- uniqueness of the exactly linear "a0-line" interpolation (Lean 4 certificate)

Source (committed): `prep_2026/a0_line/identity_uniqueness.py`, Section B (lines 65-102: the functional equation
y^2 (nu^2 - 1) = lambda y, the one-parameter family nu_lambda = sqrt(1 + lambda/y), the rescaling identity, and the deep-MOND
normalisation lambda = 1) and Section C (lines 122-160: the "simple" nu has an excess ratio drifting from 1 to 2); write-up
`prep_2026/a0_line/DERIVATION.md` lines 19-27.  The script itself says Section B is "elementary pointwise algebra"; what it lacks is
the AFFINE version (an intercept beta) and the deep-limit step done as a limit, which is what is certified here.

PREMISES (declared): a modified-inertia relation g_obs = nu(y) g_bar with y = g_bar/a0 > 0 and nu(y) > 0; the "excess"
E(y) = y^2 (nu(y)^2 - 1) (in units of a0^2), i.e. g_obs^2 - g_bar^2 = a0^2 E(y).  NO empirical input.

CERTIFIED (premises => conclusions):
  * `linear_excess_family`  : if E(y) = lam y for all y > 0 then nu(y) = sqrt(1 + lam/y) (the one-parameter family)
  * `affine_excess_unique`  : if E(y) = alpha y + beta for all y > 0 (affine, INTERCEPT beta allowed) and the deep-MOND
                              normalisation nu(y) sqrt(y) -> 1 as y -> 0+ holds, then beta = 0, alpha = 1 and nu = sqrt(1 + 1/y):
                              the deep limit forces the line through the origin with slope exactly a0
  * `deep_norm`             : nu_lam(y) sqrt(y) -> sqrt(lam) as y -> 0+ (lam >= 0), so the normalisation is equivalent to lam = 1
  * `family_rescaling`      : nu_lam(g/a0) = nu_1(g/(lam a0)) : lam only redefines a0
  * `simple_nu_not_linear`  : the "simple" nu = 1/2 + sqrt(1/4 + 1/y) has excess ratio E(y)/y equal to 5/3 at y = 4/3 and 3/2 at
                              y = 1/2, so its excess is not a line through the origin for any slope
NOT certified: that the framework's nu is the right law of nature (the uniqueness is conditional on the LINEARITY premise); that the
deep-MOND normalisation is the definition of a0 that observers use; the McGaugh-exponential statement (its excess ratio -> 0 as
y -> infinity, a sympy limit in the script) is not a Lean statement here; any data.  kappa = 1/2 (FITTED) does not enter.
-/

open Real Filter Topology

noncomputable section

theorem linear_excess_family (ν : ℝ → ℝ) (l : ℝ) (hpos : ∀ y : ℝ, 0 < y → 0 < ν y)
    (hex : ∀ y : ℝ, 0 < y → y ^ 2 * (ν y ^ 2 - 1) = l * y) :
    ∀ y : ℝ, 0 < y → ν y = Real.sqrt (1 + l / y) := by
  intro y hy
  have hy0 : y ≠ 0 := hy.ne'
  have h : ν y ^ 2 = 1 + l / y := by
    have := hex y hy
    field_simp
    nlinarith [this]
  rw [← h, Real.sqrt_sq (hpos y hy).le]

theorem affine_excess_unique (ν : ℝ → ℝ) (α β : ℝ) (hpos : ∀ y : ℝ, 0 < y → 0 < ν y)
    (hex : ∀ y : ℝ, 0 < y → y ^ 2 * (ν y ^ 2 - 1) = α * y + β)
    (hdeep : Tendsto (fun y : ℝ => ν y * Real.sqrt y) (𝓝[>] 0) (𝓝 1)) :
    β = 0 ∧ α = 1 ∧ ∀ y : ℝ, 0 < y → ν y = Real.sqrt (1 + 1 / y) := by
  have hP2 : Tendsto (fun y : ℝ => (ν y * Real.sqrt y) ^ 2) (𝓝[>] 0) (𝓝 1) := by
    simpa using hdeep.pow 2
  have hid : Tendsto (fun y : ℝ => y) (𝓝[>] (0 : ℝ)) (𝓝 0) :=
    (continuous_id.tendsto 0).mono_left nhdsWithin_le_nhds
  have hsq : ∀ y : ℝ, 0 < y → (ν y * Real.sqrt y) ^ 2 = ν y ^ 2 * y := by
    intro y hy
    rw [mul_pow, Real.sq_sqrt hy.le]
  -- beta = 0
  have h0 : Tendsto (fun y : ℝ => y * (ν y * Real.sqrt y) ^ 2) (𝓝[>] 0) (𝓝 (0 * 1)) := hid.mul hP2
  have hcont : Tendsto (fun y : ℝ => y ^ 2 + α * y + β) (𝓝[>] 0) (𝓝 β) := by
    have hc : Continuous (fun y : ℝ => y ^ 2 + α * y + β) := by fun_prop
    have := hc.tendsto 0
    simpa using this.mono_left (nhdsWithin_le_nhds (s := Set.Ioi (0 : ℝ)))
  have h1 : Tendsto (fun y : ℝ => y * (ν y * Real.sqrt y) ^ 2) (𝓝[>] 0) (𝓝 β) := by
    refine hcont.congr' ?_
    filter_upwards [self_mem_nhdsWithin] with y hy
    have hy' : 0 < y := hy
    rw [hsq y hy']
    have := hex y hy'
    nlinarith [this]
  have hb : β = 0 := by
    have := tendsto_nhds_unique h1 h0
    simpa using this
  -- alpha = 1
  have h2 : Tendsto (fun y : ℝ => y + α) (𝓝[>] 0) (𝓝 α) := by
    have hc : Continuous (fun y : ℝ => y + α) := by fun_prop
    have := hc.tendsto 0
    simpa using this.mono_left (nhdsWithin_le_nhds (s := Set.Ioi (0 : ℝ)))
  have h3 : Tendsto (fun y : ℝ => (ν y * Real.sqrt y) ^ 2) (𝓝[>] 0) (𝓝 α) := by
    refine h2.congr' ?_
    filter_upwards [self_mem_nhdsWithin] with y hy
    have hy' : 0 < y := hy
    rw [hsq y hy']
    have := hex y hy'
    rw [hb] at this
    have hy0 : y ≠ 0 := hy'.ne'
    have : y * (ν y ^ 2 * y - (y + α)) = 0 := by nlinarith [this]
    have := (mul_eq_zero.mp this).resolve_left hy0
    linarith
  have ha : α = 1 := (tendsto_nhds_unique h3 hP2)
  refine ⟨hb, ha, ?_⟩
  have := linear_excess_family ν α hpos (fun y hy => by rw [hex y hy, hb, add_zero])
  intro y hy
  rw [this y hy, ha]

theorem deep_norm {l : ℝ} (hl : 0 ≤ l) :
    Tendsto (fun y : ℝ => Real.sqrt (1 + l / y) * Real.sqrt y) (𝓝[>] 0) (𝓝 (Real.sqrt l + 1)) := by
  have hc : Continuous (fun y : ℝ => Real.sqrt (y + l)) := by fun_prop
  have h := (hc.tendsto 0).mono_left (nhdsWithin_le_nhds (s := Set.Ioi (0 : ℝ)))
  simp only [zero_add] at h
  refine h.congr' ?_
  filter_upwards [self_mem_nhdsWithin] with y hy
  have hy' : 0 < y := hy
  rw [← Real.sqrt_mul (by positivity)]
  congr 1
  field_simp

theorem family_rescaling {a0 g l : ℝ} (hg : g ≠ 0) :
    Real.sqrt (1 + l / (g / a0)) = Real.sqrt (1 + 1 / (g / (l * a0))) := by
  congr 1
  field_simp

/-- the "simple" interpolation. -/
def nuSimple (y : ℝ) : ℝ := 1 / 2 + Real.sqrt (1 / 4 + 1 / y)

theorem simple_nu_not_linear :
    nuSimple (4 / 3) ^ 2 - 1 = 5 / 4 ∧ (4 / 3 : ℝ) * (nuSimple (4 / 3) ^ 2 - 1) = 5 / 3 ∧
    (1 / 2 : ℝ) * (nuSimple (1 / 2) ^ 2 - 1) = 3 / 2 ∧
    ¬ ∃ l : ℝ, ∀ y : ℝ, 0 < y → y ^ 2 * (nuSimple y ^ 2 - 1) = l * y := by
  have h1 : Real.sqrt (1 / 4 + 1 / (4 / 3 : ℝ)) = 1 := by
    rw [show (1 / 4 + 1 / (4 / 3 : ℝ)) = 1 by norm_num, Real.sqrt_one]
  have h2 : Real.sqrt (1 / 4 + 1 / (1 / 2 : ℝ)) = 3 / 2 := by
    rw [show (1 / 4 + 1 / (1 / 2 : ℝ)) = (3 / 2) ^ 2 by norm_num, Real.sqrt_sq (by norm_num)]
  have e1 : nuSimple (4 / 3) = 3 / 2 := by unfold nuSimple; rw [h1]; norm_num
  have e2 : nuSimple (1 / 2) = 2 := by unfold nuSimple; rw [h2]; norm_num
  refine ⟨?_, ?_, ?_, ?_⟩
  · rw [e1]; norm_num
  · rw [e1]; norm_num
  · rw [e2]; norm_num
  · rintro ⟨l, hl⟩
    have a := hl (4 / 3) (by norm_num)
    have b := hl (1 / 2) (by norm_num)
    rw [e1] at a
    rw [e2] at b
    norm_num at a b
    linarith

end

#print axioms linear_excess_family
#print axioms affine_excess_unique
#print axioms deep_norm
#print axioms family_rescaling
#print axioms simple_nu_not_linear
