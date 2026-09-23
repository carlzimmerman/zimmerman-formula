import Mathlib

/-!
# I18 — The naked-black-hole rotation law at z = 7.04 (A2744-QSO1; lane L324)

SCOPE (per lean-math-certification): Lean certifies the MATHEMATICS of the framework's zero-parameter
rotation law around a dynamically weighed point mass, and the pass/fail arithmetic of the resulting
bound on a0 at z = 7.04. The physics inputs (the RAR kernel ν(y) = 1/(1 − e^{−√y}); the published mass
10^7.7; the reading "extended mass sub-dominant" ⟹ phantom fraction < 1/2) are hypotheses/inputs,
stated as such. Companion lane: `real_research/bhstar_audit_2026/L324_qso1_naked_bh_rotation_law.py`.

* `phantom_fraction_rar` — for the RAR kernel the phantom fraction 1 − 1/ν equals e^{−√y} EXACTLY.
* `sqrt_y_point_mass` — around a point mass √y = r_M/r with r_M = √(GM/a0).
* `subdominance_iff` — e^{−r_M/r} < 1/2 ⟺ r·log 2 < r_M.
* `a0_bound_iff` — r·log 2 < √(GM/a0) ⟺ a0 < GM/(r·log 2)²: sub-dominance is a direct bound on a0.
* `subdominant_iff_a0_bound` — the composite: 1 − 1/ν(GM/(r² a0)) < 1/2 ⟺ a0 < GM/(r·log 2)².
* `boost_increasing` — v_c/v_K = (1 − e^{−r_M/r})^{−1/2} grows outward (stated for its square).
* `flat_speed_at_rM` — at r_M the Newtonian circular speed equals the flat speed (why tracers at r ≈ r_M
  cannot discriminate).
* `naked_bh_envelope` — v⁴ = G M_b a0, M_BH ≤ M_b, α σ² = v² ⟹ M_BH ≤ α² σ⁴/(G a0).
* `framework_passes_*`, `rival_fails_*` — the certified numbers: at M ≥ 5.01e7 Msun (the published MOKA3D
  mass 10^7.7) the flat a0 (both footings, 9.3619e-11 and 1.1279e-10) satisfies the bound at 150 and 200 pc;
  at M ≤ 5.02e7 Msun the a0 ∝ H(z) rival (a0 ≥ 12.8 × 9.3619e-11, since E(7.0451) ≥ 12.8) violates it.
* `framework_fails_200_low`, `alt_fails_150_low`, `canonical_passes_150_low` — THE DEFICIT, certified as
  hard as the pass: at the LOW end of the published range (10^6.9 ≤ M ≤ 10^7.0 Msun, inclination-corrected
  spectroastrometry) the flat a0 VIOLATES the bound at 200 pc on both footings and at 150 pc on the alt
  footing (the canonical footing still passes at 150 pc). The verdict is mass-reading-limited.

Zero `sorry`; axioms ⊆ {propext, Classical.choice, Quot.sound}.
-/

noncomputable section

open Real

/-- The framework's RAR kernel. -/
noncomputable def nuRAR (y : ℝ) : ℝ := 1 / (1 - Real.exp (-Real.sqrt y))

/-- Phantom fraction of the RAR kernel: 1 − 1/ν(y) = e^{−√y}. -/
theorem phantom_fraction_rar (y : ℝ) : 1 - 1 / nuRAR y = Real.exp (-Real.sqrt y) := by
  unfold nuRAR
  rw [one_div_one_div]
  ring

/-- Point mass: √y = r_M/r. -/
theorem sqrt_y_point_mass {G M a0 r : ℝ} (hG : 0 < G) (hM : 0 < M) (ha : 0 < a0) (hr : 0 < r) :
    Real.sqrt (G * M / (r ^ 2 * a0)) = Real.sqrt (G * M / a0) / r := by
  have h : G * M / (r ^ 2 * a0) = (G * M / a0) / r ^ 2 := by
    field_simp
  rw [h, Real.sqrt_div (by positivity), Real.sqrt_sq hr.le]

/-- Sub-dominance of the phantom mass: e^{−r_M/r} < 1/2 ⟺ r·log 2 < r_M. -/
theorem subdominance_iff {r rM : ℝ} (hr : 0 < r) :
    Real.exp (-(rM / r)) < 1 / 2 ↔ r * Real.log 2 < rM := by
  rw [← Real.lt_log_iff_exp_lt (by norm_num), one_div, Real.log_inv, neg_lt_neg_iff,
    lt_div_iff₀ hr, mul_comm]

/-- The bound on a0: r·log 2 < √(GM/a0) ⟺ a0 < GM/(r·log 2)². -/
theorem a0_bound_iff {G M a0 r : ℝ} (hG : 0 < G) (hM : 0 < M) (ha : 0 < a0) (hr : 0 < r) :
    r * Real.log 2 < Real.sqrt (G * M / a0) ↔ a0 < G * M / (r * Real.log 2) ^ 2 := by
  have hl : 0 < Real.log 2 := Real.log_pos (by norm_num)
  have hrl : 0 < r * Real.log 2 := mul_pos hr hl
  rw [Real.lt_sqrt hrl.le, lt_div_iff₀ ha, lt_div_iff₀ (by positivity), mul_comm]

/-- The composite law: the RAR phantom fraction at r is below 1/2 ⟺ a0 < GM/(r·log 2)². -/
theorem subdominant_iff_a0_bound {G M a0 r : ℝ} (hG : 0 < G) (hM : 0 < M) (ha : 0 < a0)
    (hr : 0 < r) :
    1 - 1 / nuRAR (G * M / (r ^ 2 * a0)) < 1 / 2 ↔ a0 < G * M / (r * Real.log 2) ^ 2 := by
  rw [phantom_fraction_rar, sqrt_y_point_mass hG hM ha hr, subdominance_iff hr,
    a0_bound_iff hG hM ha hr]

/-- The boost grows outward: (1 − e^{−r_M/r})⁻¹ is strictly increasing in r (r_M > 0). -/
theorem boost_increasing {rM r₁ r₂ : ℝ} (hM : 0 < rM) (h1 : 0 < r₁) (h12 : r₁ < r₂) :
    (1 - Real.exp (-(rM / r₁)))⁻¹ < (1 - Real.exp (-(rM / r₂)))⁻¹ := by
  have h2 : 0 < r₂ := lt_trans h1 h12
  have hdiv : rM / r₂ < rM / r₁ := div_lt_div_of_pos_left hM h1 h12
  have hexp : Real.exp (-(rM / r₁)) < Real.exp (-(rM / r₂)) := Real.exp_lt_exp.mpr (by linarith)
  have hpos2 : 0 < 1 - Real.exp (-(rM / r₂)) := by
    have : Real.exp (-(rM / r₂)) < 1 := by
      have hneg : -(rM / r₂) < 0 := by have : 0 < rM / r₂ := div_pos hM h2; linarith
      have := Real.exp_lt_exp.mpr hneg
      rwa [Real.exp_zero] at this
    linarith
  apply inv_strictAnti₀ hpos2
  linarith

/-- At r_M the Newtonian circular speed equals the flat speed: (GM/r_M)² = v_f⁴. -/
theorem flat_speed_at_rM {G M a0 rM vf : ℝ} (hG : 0 < G) (hM : 0 < M) (ha : 0 < a0)
    (hrM : 0 < rM) (hvf : 0 < vf) (hr : rM ^ 2 = G * M / a0) (hv : vf ^ 4 = G * M * a0) :
    G * M / rM = vf ^ 2 := by
  have hL : 0 ≤ G * M / rM := by positivity
  have hR : 0 ≤ vf ^ 2 := by positivity
  rw [← pow_left_inj₀ hL hR (by norm_num : (2 : ℕ) ≠ 0), div_pow, hr]
  have : (vf ^ 2) ^ 2 = vf ^ 4 := by ring
  rw [this, hv]
  field_simp

/-- The naked-BH envelope: v⁴ = G M_b a0, M_BH ≤ M_b, α σ² = v² ⟹ M_BH ≤ α² σ⁴ /(G a0). -/
theorem naked_bh_envelope {G a0 Mb MBH v σ α : ℝ} (hG : 0 < G) (ha : 0 < a0)
    (hv4 : v ^ 4 = G * Mb * a0) (hle : MBH ≤ Mb) (hjeans : α * σ ^ 2 = v ^ 2) :
    MBH ≤ α ^ 2 * σ ^ 4 / (G * a0) := by
  have hMb : Mb = α ^ 2 * σ ^ 4 / (G * a0) := by
    have h4 : v ^ 4 = (α * σ ^ 2) ^ 2 := by rw [hjeans]; ring
    rw [eq_div_iff (by positivity)]
    nlinarith [hv4, h4]
  linarith [hMb ▸ hle]

/-! ### The certified numbers (SI). K = G·M, r in metres; log 2 bracketed by Mathlib's d9 bounds. -/

lemma bound_lower {K a0 x L U : ℝ} (hK : 0 < K) (hx : 0 < x) (hL : 0 < L) (hLU : L < U)
    (h : a0 < K / (x * U) ^ 2) : a0 < K / (x * L) ^ 2 := by
  have hsq : (x * L) ^ 2 < (x * U) ^ 2 := by
    apply pow_lt_pow_left₀ (by nlinarith) (by positivity) (by norm_num)
  exact lt_trans h (div_lt_div_of_pos_left hK (by positivity) hsq)

lemma bound_upper {K a0 x L U : ℝ} (hK : 0 < K) (hx : 0 < x) (hL : 0 < L) (hLU : L < U)
    (h : K / (x * L) ^ 2 < a0) : K / (x * U) ^ 2 < a0 := by
  have hsq : (x * L) ^ 2 < (x * U) ^ 2 := by
    apply pow_lt_pow_left₀ (by nlinarith) (by positivity) (by norm_num)
  exact lt_trans (div_lt_div_of_pos_left hK (by positivity) hsq) h

/-- 150 pc and 200 pc in metres (pc = 3.0856775814913673e16 m). -/
def r150 : ℝ := 150 * 3.0856775814913673e16
def r200 : ℝ := 200 * 3.0856775814913673e16
/-- G·M for M = 5.01e7 and 5.02e7 Msun (Msun = 1.98892e30 kg, G = 6.6743e-11). -/
def K501 : ℝ := 6.6743e-11 * (5.01e7 * 1.98892e30)
def K502 : ℝ := 6.6743e-11 * (5.02e7 * 1.98892e30)

/-- E(7.0451) = √(0.3153·8.0451³ + 0.6847) ≥ 12.8 (Planck 2018 Ω_m). -/
theorem E_z7_ge : (12.8 : ℝ) ≤ Real.sqrt (0.3153 * 8.0451 ^ 3 + 0.6847) := by
  rw [Real.le_sqrt (by norm_num)]
  all_goals norm_num

theorem framework_passes_150 :
    (1.1279e-10 : ℝ) < K501 / (r150 * Real.log 2) ^ 2 ∧
      (9.3619e-11 : ℝ) < K501 / (r150 * Real.log 2) ^ 2 := by
  have hL := Real.log_two_lt_d9
  have hl := Real.log_pos (by norm_num : (1 : ℝ) < 2)
  constructor <;>
  · refine bound_lower (by unfold K501; norm_num) (by unfold r150; norm_num) hl hL ?_
    unfold K501 r150; norm_num

theorem framework_passes_200 :
    (1.1279e-10 : ℝ) < K501 / (r200 * Real.log 2) ^ 2 ∧
      (9.3619e-11 : ℝ) < K501 / (r200 * Real.log 2) ^ 2 := by
  have hL := Real.log_two_lt_d9
  have hl := Real.log_pos (by norm_num : (1 : ℝ) < 2)
  constructor <;>
  · refine bound_lower (by unfold K501; norm_num) (by unfold r200; norm_num) hl hL ?_
    unfold K501 r200; norm_num

theorem rival_fails_150 :
    K502 / (r150 * Real.log 2) ^ 2 < 12.8 * 9.3619e-11 ∧
      K502 / (r150 * Real.log 2) ^ 2 < 12.8 * 1.1279e-10 := by
  have hG := Real.log_two_gt_d9
  constructor <;>
  · refine bound_upper (L := 0.6931471803) (by unfold K502; norm_num) (by unfold r150; norm_num)
      (by norm_num) hG ?_
    unfold K502 r150; norm_num

theorem rival_fails_200 :
    K502 / (r200 * Real.log 2) ^ 2 < 12.8 * 9.3619e-11 ∧
      K502 / (r200 * Real.log 2) ^ 2 < 12.8 * 1.1279e-10 := by
  have hG := Real.log_two_gt_d9
  constructor <;>
  · refine bound_upper (L := 0.6931471803) (by unfold K502; norm_num) (by unfold r200; norm_num)
      (by norm_num) hG ?_
    unfold K502 r200; norm_num

/-- G·M for M = 1.0e7, 7.95e6 and 7.94e6 Msun (10^6.9 = 7.943e6). -/
def K100 : ℝ := 6.6743e-11 * (1.0e7 * 1.98892e30)
def K795 : ℝ := 6.6743e-11 * (7.95e6 * 1.98892e30)
def K794 : ℝ := 6.6743e-11 * (7.94e6 * 1.98892e30)

/-- The deficit at 200 pc: for M ≤ 1e7 Msun both flat footings violate sub-dominance. -/
theorem framework_fails_200_low :
    K100 / (r200 * Real.log 2) ^ 2 < 9.3619e-11 ∧ K100 / (r200 * Real.log 2) ^ 2 < 1.1279e-10 := by
  have hG := Real.log_two_gt_d9
  constructor <;>
  · refine bound_upper (L := 0.6931471803) (by unfold K100; norm_num) (by unfold r200; norm_num)
      (by norm_num) hG ?_
    unfold K100 r200; norm_num

/-- The deficit at 150 pc (alt footing) for M ≤ 7.95e6 Msun ⊇ 10^6.9. -/
theorem alt_fails_150_low : K795 / (r150 * Real.log 2) ^ 2 < 1.1279e-10 := by
  have hG := Real.log_two_gt_d9
  refine bound_upper (L := 0.6931471803) (by unfold K795; norm_num) (by unfold r150; norm_num)
    (by norm_num) hG ?_
  unfold K795 r150; norm_num

/-- ... while the canonical footing still passes at 150 pc for M ≥ 7.94e6 Msun. -/
theorem canonical_passes_150_low : (9.3619e-11 : ℝ) < K794 / (r150 * Real.log 2) ^ 2 := by
  have hL := Real.log_two_lt_d9
  have hl := Real.log_pos (by norm_num : (1 : ℝ) < 2)
  refine bound_lower (by unfold K794; norm_num) (by unfold r150; norm_num) hl hL ?_
  unfold K794 r150; norm_num

end

#print axioms framework_fails_200_low
#print axioms alt_fails_150_low
#print axioms canonical_passes_150_low
#print axioms phantom_fraction_rar
#print axioms sqrt_y_point_mass
#print axioms subdominance_iff
#print axioms a0_bound_iff
#print axioms subdominant_iff_a0_bound
#print axioms boost_increasing
#print axioms flat_speed_at_rM
#print axioms naked_bh_envelope
#print axioms E_z7_ge
#print axioms framework_passes_150
#print axioms framework_passes_200
#print axioms rival_fails_150
#print axioms rival_fails_200
