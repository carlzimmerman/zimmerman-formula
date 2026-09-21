import Mathlib

/-!
# I13 -- THE GAMMA-1(beta) EIGENPROBLEM SPINE: the pulsational ceiling as a spectral-gap closing

**Scope statement (as every certificate in this repo reads):** Lean certifies
the MATHEMATICS. The physical premises -- the envelope equation of state (ideal
gas plus radiation, beta = P_gas/P), the adiabatic index Gamma_1(beta) of that
mixture, the Chandrasekhar-Ledoux work-integral form of the fundamental radial
mode, and the general-relativistic destabilizing term at compactness
x = 2GM/(R c^2) -- are the committed lanes' claims: the BH* index's open MESA
item (the Gamma_1(beta(r))-profile eigenproblem on accreting SMS structures;
the pulsational ceiling 1e5-6 Msun from first principles), inherited by the
framework as GR-identical (Cassini, r = 3M/2).

This file certifies the algebraic spine of that eigenproblem:

  1. the exact kernel identity  3*Gamma_1(beta) - 4 = beta*(4-3*beta)/(8-7*beta)
     -- the gas+radiation adiabatic index, one line of algebra;
  2. the marginal wall: the pure-radiation envelope (beta = 0) sits EXACTLY on
     the zero mode (3*Gamma_1 - 4 = 0); any gas content (beta > 0) opens the
     gap; the kernel never exceeds 1 (the gap term cannot out-weigh the
     pressure moment);
  3. the crossing identity: the fundamental mode's square frequency is linear
     in the compactness and vanishes exactly at the ceiling

        omega0^2 = (C_gr*W_gr/I) * (x* - x),   x* = W_beta/(C_gr*W_gr)

     -- a stable oscillator BELOW the ceiling, a zero mode AT it, a runaway
     ABOVE it: the pulsation gap closes exactly at the pulsational ceiling;
  4. the ceiling bracket, uniform in the envelope: 0 < x* <= 1/C_gr, and the
     pure-radiation face: the gap is closed at EVERY compactness.

Nothing here claims the SU(3) Clay gap: the framework's own non-abelian
obstruction is on record (deepseek_push/yang_mills_gap/YM_NONABELIAN.md), and
the Clay continuum-limit wall is named on the record (YM_ROADMAP R5/R6).

Compiled against the repo's Mathlib build (Lean 4.34.0-rc2).
-/
noncomputable section
open scoped Real
open scoped intervalIntegral

/-! ## 1. the kernel: the gas+radiation adiabatic index -/

/-- the adiabatic index of the ideal-gas+radiation mixture, exact -/
def g1 (b : ℝ) : ℝ := (32 - 24 * b - 3 * b^2) / (3 * (8 - 7 * b))

/-- the kernel identity, exact: 3*Gamma_1(beta) - 4 = beta*(4-3*beta)/(8-7*beta) -/
theorem kernel_identity (b : ℝ) (hb : b < 1) :
    3 * g1 b - 4 = b * (4 - 3 * b) / (8 - 7 * b) := by
  have hd : 8 - 7 * b ≠ 0 := by linarith
  have hthree : 3 * g1 b = (32 - 24 * b - 3 * b^2) / (8 - 7 * b) := by
    unfold g1
    field_simp [hd, (by norm_num : (3:ℝ) ≠ 0)]
  have hfrac : ∀ {x d : ℝ}, d ≠ 0 → (x / d - 4) * d = x - 4 * d := by
    intro x d hd
    rw [sub_mul, div_mul_cancel₀ x hd]
  have hmain : (3 * g1 b - 4) * (8 - 7 * b) = b * (4 - 3 * b) := by
    rw [hthree]
    rw [hfrac hd]
    ring
  exact (eq_div_iff hd).2 hmain

/-- the gap opens with any gas content -- the kernel is strictly positive -/
theorem kernel_pos (hb0 : 0 < b) (hb1 : b < 1) : 0 < 3 * g1 b - 4 := by
  rw [kernel_identity b hb1]
  have hnum : 0 < b * (4 - 3 * b) := mul_pos hb0 (by linarith)
  have hden : 0 < 8 - 7 * b := by linarith
  exact div_pos hnum hden

/-- the pure-radiation envelope is the EXACT zero mode of the kernel -/
theorem kernel_zero_face : 3 * g1 0 - 4 = 0 := by
  unfold g1
  norm_num

/-- the unit kernel at the gas-only limit -/
theorem kernel_at_one : 3 * g1 1 - 4 = 1 := by
  unfold g1
  norm_num

/-- the kernel never exceeds 1 -- the beta-gap is capped by the pressure moment -/
theorem kernel_le_one (hb1 : b ≤ 1) : 3 * g1 b - 4 ≤ 1 := by
  by_cases hb1' : b < 1
  · rw [kernel_identity b hb1']
    have hden : 0 < 8 - 7 * b := by linarith
    have hfac : (b - 1) * (3 * b - 8) ≥ 0 := by
      exact mul_nonneg_of_nonpos_of_nonpos (by linarith) (by linarith)
    have hnum_le : b * (4 - 3 * b) ≤ 8 - 7 * b := by
      nlinarith [hfac]
    exact div_le_one_of_le₀ hnum_le (le_of_lt hden)
  · have hb_eq : b = 1 := by linarith
    rw [hb_eq, kernel_at_one]

/-- sample value: the kernel at beta = 1/2 -/
theorem kernel_half : 3 * g1 (1 / 2) - 4 = 5 / 18 := by
  rw [kernel_identity (1 / 2) (by norm_num)]
  norm_num

/-! ## 2. the eigenproblem spine: profile-weighted moments of the fundamental mode -/

/-- the beta-gap pressure moment of the envelope -/
noncomputable def Wbeta (R : ℝ) (g p : ℝ → ℝ) : ℝ :=
  ∫ r in 0..R, (3 * g1 (g r) - 4) * p r * r^2

/-- the pressure moment that the GR destabilizer acts on -/
noncomputable def Wgr (R : ℝ) (p : ℝ → ℝ) : ℝ :=
  ∫ r in 0..R, p r * r^2

/-- the fundamental-mode square frequency (Chandrasekhar-Ledoux work form):
    pressure work minus the GR destabilizer, over the modal inertia -/
noncomputable def omega2 (Wb Wg I Cgr x : ℝ) : ℝ :=
  (Wb - Cgr * x * Wg) / I

/-- the gap term never exceeds the pressure moment -- the mean kernel bound -/
theorem gap_mean_bound (R : ℝ) (g p : ℝ → ℝ) (hR : 0 ≤ R)
    (hg1 : ∀ r ∈ Set.Icc 0 R, g r ≤ 1)
    (hp : ∀ r ∈ Set.Icc 0 R, 0 ≤ p r)
    (hiA : IntervalIntegrable (fun r => (3 * g1 (g r) - 4) * p r * r^2)
      MeasureTheory.volume 0 R)
    (hiB : IntervalIntegrable (fun r => p r * r^2) MeasureTheory.volume 0 R) :
    Wbeta R g p ≤ Wgr R p := by
  unfold Wbeta Wgr
  refine intervalIntegral.integral_mono_on hR hiA hiB ?_
  intro r hr
  have hk : 3 * g1 (g r) - 4 ≤ 1 := kernel_le_one (hg1 r hr)
  have hpr : 0 ≤ p r := hp r hr
  have hsq : 0 ≤ r^2 := sq_nonneg r
  calc
    (3 * g1 (g r) - 4) * p r * r^2 ≤ 1 * p r * r^2 := by
      exact mul_le_mul_of_nonneg_right (mul_le_mul_of_nonneg_right hk hpr) hsq
    _ = p r * r^2 := by ring

/-- the pure-radiation wall: beta = 0 everywhere closes the gap term EXACTLY -/
theorem pure_radiation_wall (R : ℝ) (g p : ℝ → ℝ) (hR : 0 ≤ R)
    (hg : ∀ r ∈ Set.Icc 0 R, g r = 0) :
    Wbeta R g p = 0 := by
  unfold Wbeta
  have hcong : Set.EqOn (fun r => (3 * g1 (g r) - 4) * p r * r^2) (fun _ : ℝ => 0)
      (Set.uIcc 0 R) := by
    intro r hr
    have hrI : r ∈ Set.Icc 0 R := by exact (Set.uIcc_of_le hR ▸ hr)
    change (3 * g1 (g r) - 4) * p r * r^2 = 0
    rw [hg r hrI, kernel_zero_face]
    ring
  simpa using (intervalIntegral.integral_congr hcong)

/-- the algebra: the frequency is LINEAR in the compactness (the crossing form) -/
theorem cross_alg (Wb Wg Cgr x xstar : ℝ) (hC : Cgr ≠ 0) (hWg : Wg ≠ 0)
    (hxstar : xstar = Wb / (Cgr * Wg)) :
    Wb - Cgr * x * Wg = Cgr * Wg * (xstar - x) := by
  subst hxstar
  field_simp [hC, hWg]

/-- BELOW the ceiling the fundamental mode is a stable oscillator: the pulsation gap -/
theorem stable_below_ceiling (Wb Wg I Cgr x xstar : ℝ) (hI : 0 < I)
    (hC : 0 < Cgr) (hWg : 0 < Wg) (hxstar : xstar = Wb / (Cgr * Wg))
    (hx : x < xstar) : 0 < omega2 Wb Wg I Cgr x := by
  unfold omega2
  have hlin : Wb - Cgr * x * Wg = Cgr * Wg * (xstar - x) :=
    cross_alg Wb Wg Cgr x xstar (ne_of_gt hC) (ne_of_gt hWg) hxstar
  rw [hlin]
  exact div_pos (mul_pos (mul_pos hC hWg) (sub_pos.mpr hx)) hI

/-- AT the ceiling the mode is the zero mode: the gap closes exactly -/
theorem zero_mode_at_ceiling (Wb Wg Cgr x xstar : ℝ)
    (hC : Cgr ≠ 0) (hWg : Wg ≠ 0) (hxstar : xstar = Wb / (Cgr * Wg))
    (hx : x = xstar) : omega2 Wb Wg 1 Cgr x = 0 := by
  unfold omega2
  have hlin : Wb - Cgr * x * Wg = Cgr * Wg * (xstar - x) :=
    cross_alg Wb Wg Cgr x xstar hC hWg hxstar
  rw [hlin, hx]
  simp

/-- ABOVE the ceiling the mode is a runaway: the gap has closed -/
theorem runaway_above_ceiling (Wb Wg I Cgr x xstar : ℝ) (hI : 0 < I)
    (hC : 0 < Cgr) (hWg : 0 < Wg) (hxstar : xstar = Wb / (Cgr * Wg))
    (hx : xstar < x) : omega2 Wb Wg I Cgr x < 0 := by
  unfold omega2
  have hlin : Wb - Cgr * x * Wg = Cgr * Wg * (xstar - x) :=
    cross_alg Wb Wg Cgr x xstar (ne_of_gt hC) (ne_of_gt hWg) hxstar
  rw [hlin]
  exact div_neg_of_neg_of_pos (mul_neg_of_pos_of_neg (mul_pos hC hWg) (sub_neg.mpr hx)) hI

/-- the ceiling bracket: the zero-crossing compactness never exceeds 1/C_gr -/
theorem ceiling_bracket (R : ℝ) (g p : ℝ → ℝ) (Cgr : ℝ) (hC : 0 < Cgr)
    (hR : 0 ≤ R)
    (hg1 : ∀ r ∈ Set.Icc 0 R, g r ≤ 1)
    (hp : ∀ r ∈ Set.Icc 0 R, 0 ≤ p r)
    (hiA : IntervalIntegrable (fun r => (3 * g1 (g r) - 4) * p r * r^2)
      MeasureTheory.volume 0 R)
    (hiB : IntervalIntegrable (fun r => p r * r^2) MeasureTheory.volume 0 R)
    (hWg : 0 < Wgr R p) : Wbeta R g p / (Cgr * Wgr R p) ≤ 1 / Cgr := by
  have hmean : Wbeta R g p ≤ Wgr R p := gap_mean_bound R g p hR hg1 hp hiA hiB
  have hcross : Wbeta R g p * Cgr ≤ Cgr * Wgr R p := by
    calc Wbeta R g p * Cgr ≤ Wgr R p * Cgr :=
        mul_le_mul_of_nonneg_right hmean (le_of_lt hC)
      _ = Cgr * Wgr R p := by ring
  have hden' : Cgr * Wgr R p ≠ 0 := mul_ne_zero (ne_of_gt hC) (ne_of_gt hWg)
  have hc' : Cgr ≠ 0 := ne_of_gt hC
  have hpos2 : 0 < (Cgr * Wgr R p) * Cgr := mul_pos (mul_pos hC hWg) hC
  have hle' : (Wbeta R g p / (Cgr * Wgr R p)) * ((Cgr * Wgr R p) * Cgr)
      ≤ (1 / Cgr) * ((Cgr * Wgr R p) * Cgr) := by
    calc
      (Wbeta R g p / (Cgr * Wgr R p)) * ((Cgr * Wgr R p) * Cgr)
          = Wbeta R g p * Cgr := by
            rw [← mul_assoc, div_mul_cancel₀ (Wbeta R g p) hden']
      _ ≤ (1 / Cgr) * ((Cgr * Wgr R p) * Cgr) := by
        rw [mul_comm (Cgr * Wgr R p) Cgr, ← mul_assoc, div_mul_cancel₀ 1 hc']
        simpa using hcross
  exact le_of_mul_le_mul_right hle' hpos2

/-- the ceiling bracket, lower side: with any gas content the crossing
    compactness is strictly positive -/
theorem cross_ceiling_pos (Wb Wg Cgr : ℝ) (hWb : 0 < Wb) (hC : 0 < Cgr)
    (hWg : 0 < Wg) : 0 < Wb / (Cgr * Wg) :=
  div_pos hWb (mul_pos hC hWg)

/-- the pure-radiation face: with the gap term EXACTLY zero the mode is unstable
    at every compactness -- the zero-gap envelope -/
theorem radiation_unstable (R : ℝ) (g p : ℝ → ℝ) (I Cgr x : ℝ) (hR : 0 ≤ R)
    (hg : ∀ r ∈ Set.Icc 0 R, g r = 0)
    (hI : 0 < I) (hC : 0 < Cgr) (hWg : 0 < Wgr R p) (hx : 0 ≤ x) :
    omega2 (Wbeta R g p) (Wgr R p) I Cgr x ≤ 0 := by
  have hwall : Wbeta R g p = 0 := pure_radiation_wall R g p hR hg
  unfold omega2
  rw [hwall]
  by_cases hx0 : x = 0
  · simp [hx0]
  · have hx' : 0 < x := lt_of_le_of_ne' hx hx0
    have hnum : 0 - Cgr * x * Wgr R p < 0 := by
      have hpos : 0 < Cgr * x * Wgr R p := mul_pos (mul_pos hC hx') hWg
      linarith
    exact le_of_lt (div_neg_of_neg_of_pos hnum hI)

/-- the gap-closes condition: compactness at or above 1/C_gr kills the mode -/
theorem gap_closes_at_ceiling (Wb Wg I Cgr x : ℝ) (hI : 0 < I) (hC : 0 < Cgr)
    (hWg : 0 < Wg) (hmean : Wb ≤ Wg) (hx : 1 / Cgr ≤ x) :
    omega2 Wb Wg I Cgr x ≤ 0 := by
  unfold omega2
  have hxc : 1 ≤ Cgr * x := by
    have h := mul_le_mul_of_nonneg_left hx (le_of_lt hC)
    field_simp [ne_of_gt hC] at h
    exact h
  have hnum : Wb - Cgr * x * Wg ≤ 0 := by
    calc
      Wb - Cgr * x * Wg ≤ Wg - Cgr * x * Wg := by
        exact sub_le_sub_right hmean (Cgr * x * Wg)
      _ = (1 - Cgr * x) * Wg := by ring
      _ ≤ 0 := by
        exact mul_nonpos_of_nonpos_of_nonneg (by linarith) (le_of_lt hWg)
  by_cases hz : Wb - Cgr * x * Wg = 0
  · rw [hz]
    simp
  · have hnum' : Wb - Cgr * x * Wg < 0 := lt_of_le_of_ne' hnum (Ne.symm hz)
    exact le_of_lt (div_neg_of_neg_of_pos hnum' hI)

/-! ## 3. the certificate record -/

#print axioms kernel_identity
#print axioms kernel_pos
#print axioms kernel_le_one
#print axioms kernel_half
#print axioms gap_mean_bound
#print axioms pure_radiation_wall
#print axioms stable_below_ceiling
#print axioms zero_mode_at_ceiling
#print axioms runaway_above_ceiling
#print axioms ceiling_bracket
#print axioms radiation_unstable
#print axioms gap_closes_at_ceiling