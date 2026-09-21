import Mathlib

open Real

/-!
# I01 — Wave I: exact certificates for the BH* absorption (arXiv:2609.09274)

SCOPE (per lean-math-certification): Lean certifies the ALGEBRA of the wave's structures over
R, given each law as a hypothesis (the a0-line interpolation ν(y) = √(1+1/y), the Eddington
law, the recombination pin, first-law thermodynamics of the gas+radiation mixture). It does
NOT certify that nature obeys these laws. Zero `sorry`; axioms ⊆ {propext,
Classical.choice, Quot.sound}.

T1 (window direction, exact): the boost B(R) = √(1 + a0R²/(GM)) − 1 is strictly INCREASING
    in R, and its level sets are OUTER rays: B ≥ B* ⟺ a0R² ≥ GM((1+B*)²−1). This is the
    certified correction of a direction error the H2 numeric lane let slip into prose (the
    ≥20% anomaly window opens for R_e ≥ R_crit — an outer, deep-MOND window; compact ⟹
    degenerate). Exact edges: B* = 1/5 at y* = 25/11 (ν = 6/5 exactly), B* = 1/2 at y* = 4/5,
    B* = 1 at y* = 1/3; in units r_M = √(GM/a0): R_crit = r_M/√y* = (√11/5, 2/√5, 1/√3)·r_M
    (the radical forms are the certified identities below; numeric r_M stays in the Python
    lane).
T2 (radiation-domination invariant): x = P_g/P_r = 3ρk/(μ m_p a_r T³) along the
    recombination-pinned Eddington-limited family (T = q·t0·M/R, ρ = 3M/(4πR³), common t0)
    satisfies x·q³M² = 9k/(4π μ m_p a_r t0³) — independent of the mass, the radius
    normalization AND the structure factor q. With β = P_g/(P_g+P_r) = x/(1+x), the Fowler
    approach Γ₁ → 4/3 is exactly mass-driven (x ∝ M⁻²), radius-independent by construction.
T3 (the a0-posit's Eddington closure): under the framework's structural posit a0 = c²/(2R_Z)
    — the Schwarzschild-2 factor inside Z = 2√(8π/3) — the horizon-mass object
    M_Z = c²R_Z/(2G) has Eddington luminosity L_Edd = πc⁵/(κ a0) exactly.
T4 (the Γ₁ envelope): for 0 < β ≤ 1, β/6 ≤ Γ₁(β) − 4/3 ≤ β/3 with the EXACT slacks
    (Γ₁−4/3−β/6)·(24−21β) = β²/2 and (4/3+β/3−Γ₁)·(24−21β) = 4β(1−β) — the two-sided
    certificate behind the G2 "gap ≈ β/6" scaling.
Corollary (numeric): the BH* mass chain is a0-blind — the a0-line shifts the surface-gravity
    mass estimator by ≤ a0/(2g) < 10⁻⁶ at the median-stack values (a0 = 9.3619e-11 fw
    footing, g = 6.31e-5 m/s²; carried as exact rationals).
-/

noncomputable section

/-! ## T1 — the compactness switch, exactly -/

/-- The a0-line boost of a self-gravitating body of mass M at radius R:
    B(R) = √(1 + a0R²/(GM)) − 1, from the framework's ν(y) = √(1 + 1/y) with y = g_bar/a0,
    g_bar = GM/R². -/
noncomputable def boost (a0 M G R : ℝ) : ℝ := Real.sqrt (1 + a0 * R ^ 2 / (G * M)) - 1

/-- The boost is positive at every radius (the a0-line never dips the anomaly below 0). -/
theorem boost_pos {a0 M G R : ℝ} (ha0 : 0 < a0) (hGM : 0 < G * M) (hR : 0 < R) :
    0 < boost a0 M G R := by
  have hpos : 0 < a0 * R ^ 2 / (G * M) := div_pos (mul_pos ha0 (pow_pos hR 2)) hGM
  have hx : (0 : ℝ) ≤ 1 := by norm_num
  have hlt : (1 : ℝ) < 1 + a0 * R ^ 2 / (G * M) := by linarith [hpos]
  have h1 : (1 : ℝ) < Real.sqrt (1 + a0 * R ^ 2 / (G * M)) := by
    have h2 := Real.sqrt_lt_sqrt hx hlt
    rwa [Real.sqrt_one] at h2
  rw [boost]
  linarith

/-- **T1 (exact level sets).** boost = B* ⟺ a0R² = GM((1+B*)²−1). -/
theorem boost_eq_iff {a0 M G R B : ℝ} (ha0 : 0 < a0) (hGM : 0 < G * M) (hR : 0 < R)
    (hB : -1 < B) : boost a0 M G R = B ↔ a0 * R ^ 2 = ((1 + B) ^ 2 - 1) * (G * M) := by
  have hgmne : G * M ≠ 0 := ne_of_gt hGM
  have hrad : 0 ≤ 1 + a0 * R ^ 2 / (G * M) := by positivity
  have h1pos : 0 ≤ 1 + B := by linarith
  have hu : 1 + a0 * R ^ 2 / (G * M) = (1 + B) ^ 2 ↔ a0 * R ^ 2 = ((1 + B) ^ 2 - 1) * (G * M) := by
    constructor
    · intro h
      have hX : a0 * R ^ 2 / (G * M) = (1 + B) ^ 2 - 1 := by linarith
      exact (div_eq_iff hgmne).mp hX
    · intro h
      have hX : a0 * R ^ 2 / (G * M) = (1 + B) ^ 2 - 1 := (div_eq_iff hgmne).mpr h
      linarith
  rw [boost]
  constructor
  · intro h
    have hs : Real.sqrt (1 + a0 * R ^ 2 / (G * M)) = 1 + B := by linarith
    have h2 := hu.mp ((Real.sqrt_eq_iff_eq_sq hrad h1pos).mp hs)
    linear_combination (norm := ring_nf) h2
  · intro h
    have h2 : a0 * R ^ 2 = ((1 + B) ^ 2 - 1) * (G * M) := by
      linear_combination (norm := ring_nf) h
    have hs : Real.sqrt (1 + a0 * R ^ 2 / (G * M)) = 1 + B :=
      (Real.sqrt_eq_iff_eq_sq hrad h1pos).mpr (hu.mpr h2)
    linarith

/-- **T1 (strict direction).** boost < B* ⟺ a0R² < GM((1+B*)²−1). -/
theorem boost_lt_iff {a0 M G R B : ℝ} (ha0 : 0 < a0) (hGM : 0 < G * M) (hR : 0 < R)
    (hB : -1 < B) : boost a0 M G R < B ↔ a0 * R ^ 2 < ((1 + B) ^ 2 - 1) * (G * M) := by
  have hgmne : G * M ≠ 0 := ne_of_gt hGM
  have hrad : 0 ≤ 1 + a0 * R ^ 2 / (G * M) := by positivity
  have h1pos : 0 ≤ 1 + B := by linarith
  have hslt : Real.sqrt (1 + a0 * R ^ 2 / (G * M)) < 1 + B
      ↔ 1 + a0 * R ^ 2 / (G * M) < (1 + B) ^ 2 := Real.sqrt_lt hrad h1pos
  rw [boost]
  constructor
  · intro h
    have hs : Real.sqrt (1 + a0 * R ^ 2 / (G * M)) < 1 + B := by linarith
    have hx2 : a0 * R ^ 2 / (G * M) < (1 + B) ^ 2 - 1 := by
      have hx := hslt.mp hs
      linarith
    exact (div_lt_iff₀ hGM).mp hx2
  · intro h
    have hx : a0 * R ^ 2 / (G * M) < (1 + B) ^ 2 - 1 := by
      by_contra hcon
      push_neg at hcon
      have h4 := mul_le_mul_of_nonneg_right hcon hGM.le
      rw [div_mul_cancel₀ _ hgmne] at h4
      nlinarith
    linarith [hslt.mpr (by linarith)]

/-- **T1 (the window, cleared form).** boost ≥ B* ⟺ a0R² ≥ GM((1+B*)²−1): the anomaly
window is an OUTER ray in R (deep-MOND side). The H2 numeric prose had this direction
reversed; this theorem is the certified correction. -/
theorem boost_ge_iff {a0 M G R B : ℝ} (ha0 : 0 < a0) (hGM : 0 < G * M) (hR : 0 < R)
    (hB : 0 < B) : boost a0 M G R ≥ B ↔ ((1 + B) ^ 2 - 1) * (G * M) ≤ a0 * R ^ 2 := by
  have hlt := boost_lt_iff ha0 hGM hR (by linarith)
  constructor
  · intro h
    by_contra hcon
    push_neg at hcon
    exact absurd (hlt.mpr hcon) (not_lt.mpr h)
  · intro h
    by_contra hcon
    push_neg at hcon
    exact absurd (hlt.mp hcon) (not_lt.mpr h)

/-- **T1 (strict monotonicity — the certified compactness switch).** The boost is strictly
increasing in R at fixed mass and a0: compactness SUPPRESSES the anomaly, size releases it. -/
theorem boost_strictMono {a0 M G R R' : ℝ} (ha0 : 0 < a0) (hGM : 0 < G * M)
    (hR : 0 < R) (hR' : 0 < R') (hRR : R < R') : boost a0 M G R < boost a0 M G R' := by
  have h1 : a0 * R ^ 2 < a0 * R' ^ 2 := by
    refine mul_lt_mul_of_pos_left ?_ ha0
    nlinarith
  have hbR' : -1 < boost a0 M G R' := by linarith [boost_pos ha0 hGM hR']
  by_contra hcon
  push_neg at hcon
  have hge : ((1 + boost a0 M G R') ^ 2 - 1) * (G * M) ≤ a0 * R ^ 2 := by
    by_contra hcon2
    push_neg at hcon2
    have hnot : ¬ (boost a0 M G R < boost a0 M G R') := not_lt.mpr hcon
    exact hnot ((boost_lt_iff ha0 hGM hR hbR').mpr hcon2)
  have heq : a0 * R' ^ 2 = ((1 + boost a0 M G R') ^ 2 - 1) * (G * M) :=
    (boost_eq_iff ha0 hGM hR' hbR').mp rfl
  linarith

/-- Exact window edges (cleared): B* = 1/5 ⟺ y* = 25/11; B* = 1/2 ⟺ y* = 4/5;
B* = 1 ⟺ y* = 1/3. In r_M = √(GM/a0) units: R_crit = (√11/5, 2/√5, 1/√3)·r_M. -/
example : (1 + (1 / 5 : ℝ)) ^ 2 - 1 = 11 / 25 := by norm_num
example : (1 + (1 / 2 : ℝ)) ^ 2 - 1 = 5 / 4 := by norm_num
example : (1 + (1 : ℝ)) ^ 2 - 1 = 3 := by norm_num
example : Real.sqrt (1 + 11 / 25) = 6 / 5 :=
  (Real.sqrt_eq_iff_eq_sq (by norm_num) (by norm_num)).mpr (by norm_num)

/-! ## T2 — the radiation-domination invariant -/

/-- Gas-to-radiation pressure ratio x = P_g / P_r = 3ρk/(μ m_p a_r T³) for an ideal gas +
radiation mixture. -/
noncomputable def xpr (K mu mp ar rho T : ℝ) : ℝ := 3 * rho * K / (mu * mp * ar * T ^ 3)

/-- **T2 (the invariant).** In the recombination-pinned, Eddington-limited family — members
(M, R, T, q) with common t0 and T = q·t0·M/R, ρ = 3M/(4πR³) — the product x·q³M² is CONSTANT:
independent of the mass, the radius normalization AND the structure factor q. The Fowler
approach Γ₁ → 4/3 is exactly mass-driven (x ∝ M⁻²), radius-independent by construction. -/
theorem xpr_invariant {K mu mp ar t0 q1 q2 M1 M2 R1 R2 T1 T2 rho1 rho2 : ℝ}
    (hK : 0 < K) (hmu : 0 < mu) (hmp : 0 < mp) (har : 0 < ar) (ht0 : 0 < t0)
    (hq1 : 0 < q1) (hq2 : 0 < q2) (hM1 : 0 < M1) (hM2 : 0 < M2)
    (hR1 : 0 < R1) (hR2 : 0 < R2)
    (hT1eq : T1 = q1 * t0 * M1 / R1) (hT2eq : T2 = q2 * t0 * M2 / R2)
    (hrho1 : rho1 = 3 * M1 / (4 * Real.pi * R1 ^ 3))
    (hrho2 : rho2 = 3 * M2 / (4 * Real.pi * R2 ^ 3)) :
    xpr K mu mp ar rho1 T1 * q1 ^ 3 * M1 ^ 2 = xpr K mu mp ar rho2 T2 * q2 ^ 3 * M2 ^ 2 := by
  have h1 : xpr K mu mp ar rho1 T1 * q1 ^ 3 * M1 ^ 2
      = 9 * K / (4 * Real.pi * mu * mp * ar * t0 ^ 3) := by
    unfold xpr
    rw [hT1eq, hrho1]
    field_simp [ne_of_gt hM1, ne_of_gt hR1, ne_of_gt hq1]
    ring
  have h2 : xpr K mu mp ar rho2 T2 * q2 ^ 3 * M2 ^ 2
      = 9 * K / (4 * Real.pi * mu * mp * ar * t0 ^ 3) := by
    unfold xpr
    rw [hT2eq, hrho2]
    field_simp [ne_of_gt hM2, ne_of_gt hR2, ne_of_gt hq2]
    ring
  rw [h1, h2]

/-! ## T3 — the a0-posit's Eddington closure -/

/-- **T3.** Under the framework's structural posit a0 = c²/(2R_Z) — the Schwarzschild-2
factor inside Z = 2√(8π/3) — the horizon-mass object M_Z = c²R_Z/(2G) has Eddington
luminosity L_Edd = πc⁵/(κ a0) exactly: the Eddington scale of the cosmic free-fall black
hole is a0-determined. -/
theorem eddington_a0_closure {c G RZ MZ a0 kap L : ℝ} (hG : 0 < G)
    (ha0 : a0 = c ^ 2 / (2 * RZ)) (hMZ : MZ = c ^ 2 * RZ / (2 * G))
    (hL : L = 4 * Real.pi * G * MZ * c / kap) : L = Real.pi * c ^ 5 / (kap * a0) := by
  rw [hL, hMZ, ha0]
  field_simp [ne_of_gt hG]
  ring

/-! ## T4 — the certified Γ₁ envelope -/

/-- Γ₁(β) for an ideal-gas + radiation mixture with β = P_gas/P_tot, derived from the first
law (du = −P dV): Γ₁ = β + 2(4−3β)²/(24−21β). Limits: Γ₁(1) = 5/3, Γ₁ → 4/3 as β → 0⁺. -/
noncomputable def Gamma1 (b : ℝ) : ℝ := b + 2 * (4 - 3 * b) ^ 2 / (24 - 21 * b)

/-- **T4 (lower envelope with exact slack).** (Γ₁−4/3−β/6)·(24−21β) = β²/2, hence
β/6 ≤ Γ₁(β) − 4/3 for 0 < β ≤ 1. -/
theorem gap_lower {b : ℝ} (hb : 0 < b) (hb1 : b ≤ 1) : 1 / 6 * b ≤ Gamma1 b - 4 / 3 := by
  have hden : 0 < 24 - 21 * b := by linarith
  have hiden : (Gamma1 b - 4 / 3 - (1 / 6) * b) * (24 - 21 * b) = b ^ 2 / 2 := by
    unfold Gamma1
    rw [sub_mul, sub_mul, add_mul, div_mul_cancel₀ _ hden.ne']
    ring
  have hX : Gamma1 b - 4 / 3 - (1 / 6) * b = b ^ 2 / 2 / (24 - 21 * b) :=
    (eq_div_iff hden.ne').mpr hiden
  have hpos : 0 ≤ b ^ 2 / 2 / (24 - 21 * b) := div_nonneg (by positivity) hden.le
  linarith

/-- **T4 (upper envelope with exact slack).** (4/3+β/3−Γ₁)·(24−21β) = 4β(1−β), hence
Γ₁(β) − 4/3 ≤ β/3 for 0 < β ≤ 1 (equality at β = 1). -/
theorem gap_upper {b : ℝ} (hb : 0 < b) (hb1 : b ≤ 1) : Gamma1 b - 4 / 3 ≤ 1 / 3 * b := by
  have hden : 0 < 24 - 21 * b := by linarith
  have hiden : (4 / 3 + (1 / 3) * b - Gamma1 b) * (24 - 21 * b) = 4 * b * (1 - b) := by
    unfold Gamma1
    rw [sub_mul, add_mul, add_mul, div_mul_cancel₀ _ hden.ne']
    ring
  have hX : 4 / 3 + (1 / 3) * b - Gamma1 b = 4 * b * (1 - b) / (24 - 21 * b) :=
    (eq_div_iff hden.ne').mpr hiden
  have hpos : 0 ≤ 4 * b * (1 - b) / (24 - 21 * b) :=
    div_nonneg (by nlinarith) hden.le
  linarith

/-- Exact envelope check at β = 1/2: Γ₁ = 77/54, gap = 5/54 ∈ [β/6, β/3] = [1/12, 1/6]. -/
example : Gamma1 (1 / 2) - 4 / 3 = 5 / 54 := by norm_num [Gamma1]
/-- Equality edge of the upper envelope at β = 1: Γ₁(1) = 5/3. -/
example : Gamma1 1 - 4 / 3 = 1 / 3 := by norm_num [Gamma1]

/-! ## Corollary — the BH* mass chain is a0-blind, proven -/

/-- Bernoulli: √(1+x) ≤ 1 + x/2 for 0 ≤ x — the a0-line shift bound. -/
theorem sqrt_one_add_le_half {x : ℝ} (hx : 0 ≤ x) : Real.sqrt (1 + x) ≤ 1 + x / 2 := by
  rw [Real.sqrt_le_iff]
  exact ⟨by nlinarith, by nlinarith [sq_nonneg x]⟩

/-- **Corollary (numeric).** With the framework's fw footing a0 = 9.3619e-11 m/s²
(= 93619/10^15) and the BH* median-stack photosphere gravity g = 6.31e-5 m/s² (= 631/10^7),
the a0-line shifts the surface-gravity mass estimator by ≤ a0/(2g) < 10⁻⁶: the BH* mass
chain is a0-blind at the 10⁻⁶ level, PROVEN — not merely measured. -/
theorem bhstar_a0blind :
    Real.sqrt (1 + (93619 / 10 ^ 15) / (631 / 10 ^ 7)) - 1 < 1 / 10 ^ 6 := by
  have hX : (93619 / 10 ^ 15) / (631 / 10 ^ 7) = (93619 : ℝ) / (631 * 10 ^ 8) := by
    field_simp
  have hx : (0 : ℝ) ≤ (93619 : ℝ) / (631 * 10 ^ 8) := by positivity
  have h1 : (93619 : ℝ) / (631 * 10 ^ 8) < 1 / 500000 := by norm_num
  have h2 := sqrt_one_add_le_half hx
  have h3 : Real.sqrt (1 + (93619 / 10 ^ 15) / (631 / 10 ^ 7)) = Real.sqrt (1 + (93619 : ℝ) / (631 * 10 ^ 8)) := by
    rw [hX]
  rw [h3]
  linarith

end

#print axioms boost_eq_iff
#print axioms boost_lt_iff
#print axioms boost_ge_iff
#print axioms boost_strictMono
#print axioms xpr_invariant
#print axioms eddington_a0_closure
#print axioms gap_lower
#print axioms gap_upper
#print axioms sqrt_one_add_le_half
#print axioms bhstar_a0blind
