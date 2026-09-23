import Mathlib

/-!
# I17 — Audit of the BH* regime coincidence (lane L323)

SCOPE (per lean-math-certification): Lean certifies the MATHEMATICS that demotes the BH* campaign's
framework-facing claims; the physics readings are stated as hypotheses. Companion lane:
`real_research/bhstar_audit_2026/L323_bhstar_regime_coincidence_audit.py` (9/9; MUTATE p = 5 fails R3).

* `ratio_is_freefall_kinematics` — the density-form ratio g/a0(ρ), a0(ρ) = (c/2)√(Gρ), is EXACTLY
  2·(v/c)·(t_ff/t_dyn) with t_ff = 1/√(Gρ), t_dyn = r/v, g = v²/r: a kinematic number of the envelope,
  with no cosmic density in it.
* `unique_crossing` / `crossing_antitone` — for any ratio K·r^(−s) (s > 0; an envelope ρ ∝ r^(−p) with
  p < 4 gives s = 2 − p/2) there is EXACTLY ONE r > 0 with ratio 1, and the ratio falls outward: the
  crossing exists in every such envelope, so its existence is not a finding.
* `kp1_iff_transition` — KP1 (r⁴ n c² μ m_p = 4 G M²) is EQUIVALENT to the transition definition
  g_B = a0(ρ_B) (I11 proved only →): KP1 carries no content beyond the definition.
* `kp2_from_family` — with the published family scaling r_B = k·√M alone, v² = 2GM/r_B gives
  v⁴·k² = 4G²M: the M^{1/4} exponent of KP2 needs no density form.
* `lab_air_strong_a0` — the same classifier puts the air at the Earth's surface at g/a0(ρ_air) < 1/100
  ("strong-a0"), where gravity is Newtonian: the label has no dynamical content.
* `void_threshold_corrected` — I10's docstring claim fails at f_n = 1e-4: 9.47e6 × 1e-4 < 1e3.
* `gamma_solar_composition` — wave U's Γ = 56.6 (κ_es = 0.40) becomes < 50 at κ_es = 0.34 (X = 0.7).

Zero `sorry`; axioms ⊆ {propext, Classical.choice, Quot.sound}.
-/

noncomputable section

open Real

/-- The density-form ratio is a free-fall kinematic number: g/a0(ρ) = 2 (v/c)(t_ff/t_dyn). -/
theorem ratio_is_freefall_kinematics {G ρ c v r : ℝ}
    (hG : 0 < G) (hρ : 0 < ρ) (hc : 0 < c) (hv : 0 < v) (hr : 0 < r) :
    (v ^ 2 / r) / (c / 2 * Real.sqrt (G * ρ)) =
      2 * (v / c) * ((1 / Real.sqrt (G * ρ)) / (r / v)) := by
  have hs : 0 < Real.sqrt (G * ρ) := Real.sqrt_pos.mpr (mul_pos hG hρ)
  field_simp

/-- Existence and uniqueness of the crossing: ∃! r > 0 with K·r^(−s) = 1. -/
theorem unique_crossing {K s : ℝ} (hK : 0 < K) (hs : 0 < s) :
    ∃! r : ℝ, 0 < r ∧ K * r ^ (-s) = 1 := by
  refine ⟨K ^ (1 / s), ⟨Real.rpow_pos_of_pos hK _, ?_⟩, ?_⟩
  · rw [← Real.rpow_mul hK.le, show (1 / s) * (-s) = (-1 : ℝ) by field_simp, Real.rpow_neg_one]
    field_simp
  · rintro r ⟨hr, hkr⟩
    have hr' : r ^ (-s) = K⁻¹ := by
      field_simp
      linarith [hkr]
    have key : r = (r ^ (-s)) ^ (-(1 / s)) := by
      rw [← Real.rpow_mul hr.le, show (-s) * (-(1 / s)) = (1 : ℝ) by field_simp, Real.rpow_one]
    rw [key, hr', Real.inv_rpow hK.le, ← Real.rpow_neg hK.le, neg_neg]

/-- The ratio K·r^(−s) is strictly decreasing outward (s > 0). -/
theorem crossing_antitone {K s r₁ r₂ : ℝ} (hK : 0 < K) (hs : 0 < s)
    (h1 : 0 < r₁) (h12 : r₁ < r₂) :
    K * r₂ ^ (-s) < K * r₁ ^ (-s) := by
  apply mul_lt_mul_of_pos_left _ hK
  exact Real.rpow_lt_rpow_of_neg h1 h12 (by linarith)

/-- KP1 ⟺ the transition definition (both directions). -/
theorem kp1_iff_transition {G M c rB n mu mp : ℝ}
    (hG : 0 < G) (hM : 0 < M) (hc : 0 < c) (hrB : 0 < rB) (hn : 0 < n)
    (hmu : 0 < mu) (hmp : 0 < mp) :
    G * M / rB ^ 2 = (c / 2) * Real.sqrt (G * mu * mp * n) ↔
      rB ^ 4 * n * (c ^ 2 * mu * mp) = 4 * G * M ^ 2 := by
  have hX : 0 ≤ G * mu * mp * n := by positivity
  have hs2 : Real.sqrt (G * mu * mp * n) ^ 2 = G * mu * mp * n := Real.sq_sqrt hX
  have hL : 0 ≤ G * M / rB ^ 2 := by positivity
  have hR : 0 ≤ (c / 2) * Real.sqrt (G * mu * mp * n) := by positivity
  have hsq : (G * M / rB ^ 2) ^ 2 = ((c / 2) * Real.sqrt (G * mu * mp * n)) ^ 2 ↔
      rB ^ 4 * n * (c ^ 2 * mu * mp) = 4 * G * M ^ 2 := by
    rw [mul_pow, hs2, div_pow]
    have hrb4 : (rB ^ 2) ^ 2 ≠ 0 := by positivity
    rw [div_eq_iff hrb4]
    constructor
    · intro h
      have h' : G * (4 * G * M ^ 2) = G * (rB ^ 4 * n * (c ^ 2 * mu * mp)) := by
        nlinarith [h]
      exact (mul_left_cancel₀ hG.ne' h').symm
    · intro h
      have : (rB ^ 2) ^ 2 = rB ^ 4 := by ring
      rw [this]
      nlinarith [h]
  rw [← hsq]
  exact (pow_left_inj₀ hL hR (by norm_num)).symm

/-- KP2's exponent from the published family alone: r_B = k√M, v² = 2GM/r_B ⇒ v⁴ k² = 4 G² M. -/
theorem kp2_from_family {G M k rB v : ℝ} (hG : 0 < G) (hM : 0 < M) (hk : 0 < k)
    (hrB : rB = k * Real.sqrt M) (hv : v ^ 2 = 2 * G * M / rB) :
    v ^ 4 * k ^ 2 = 4 * G ^ 2 * M := by
  have hsM : Real.sqrt M ^ 2 = M := Real.sq_sqrt hM.le
  have hsMpos : 0 < Real.sqrt M := Real.sqrt_pos.mpr hM
  have h4 : v ^ 4 = (v ^ 2) ^ 2 := by ring
  rw [h4, hv, hrB, div_pow, mul_pow k (Real.sqrt M), hsM]
  field_simp
  ring

/-- The classifier on laboratory air: g_Earth / a0(ρ_air) < 1/100 (SI: c, G, ρ = 1.2, g = 9.81). -/
theorem lab_air_strong_a0 :
    (9.81 : ℝ) / ((299792458 / 2) * Real.sqrt (6.6743e-11 * 1.2)) < 1 / 100 := by
  have hpos : (0 : ℝ) < Real.sqrt (6.6743e-11 * 1.2) := Real.sqrt_pos.mpr (by norm_num)
  have hlt : (2 * 981 / 299792458 : ℝ) < Real.sqrt (6.6743e-11 * 1.2) := by
    rw [Real.lt_sqrt (by norm_num)]
    norm_num
  rw [div_lt_iff₀ (by positivity)]
  nlinarith [hlt]

/-- I10 corrected: at f_n = 1e-4 the product R_σ f_n = 947 < 1e3; the ≥1e3 threshold is f_n = 1e3/R_σ. -/
theorem void_threshold_corrected :
    (9.47e6 : ℝ) * 1e-4 < 1e3 ∧ (9.47e6 : ℝ) * (1e3 / 9.47e6) = 1e3 := by
  constructor <;> norm_num

/-- Wave U's Γ at solar composition: 56.6 × (0.34/0.40) < 50 < 56.6. -/
theorem gamma_solar_composition :
    (56.6 : ℝ) * (0.34 / 0.40) < 50 ∧ (50 : ℝ) < 56.6 := by
  constructor <;> norm_num

end

#print axioms ratio_is_freefall_kinematics
#print axioms unique_crossing
#print axioms crossing_antitone
#print axioms kp1_iff_transition
#print axioms kp2_from_family
#print axioms lab_air_strong_a0
#print axioms void_threshold_corrected
#print axioms gamma_solar_composition
