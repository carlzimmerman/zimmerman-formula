import Mathlib

/-!
# YM03 -- THE VIRIAL-CONSISTENCY SPINE of the pinned gap

**Scope statement (as every certificate in this repo reads):** Lean certifies
the MATHEMATICS.  The physical premises -- L5's shift-symmetric action with
the minimal Stueckelberg gauging, the kernel face f'(K) = mu_2(u), the
m = m_dust ladder inversion (B03/A08), and the committed fiducial constants
-- are the committed lanes' claims (deepseek_push/yang_mills_gap/YM01_gap_derivation.py,
YM_PROOF.md, project_atomos/B03_doubleZ_mass.py).  This file restates every
definition from scratch (standalone: `import Mathlib` only, no import of
YM01_gap.lean / YM02_pinned_gap.lean) and certifies the VIRIAL-CONSISTENCY
SPINE of the pinned gap: the U-MAP coefficient's closed form
C_f = 1/(2 sqrt(8 pi)) and its deep coefficient (YM02's C_f_value and
deep_coeff, restated verbatim), the POSITIVITY of the mass-ratio square
2 (m_d/M_pl)^2 > 0, and the committed NUMERIC BANDS -- the ratio band
2 (m_d/M_pl)^2 < 1e-46 and the virial-exactness band q_d/m_d <= 7.07e-9 (M_pl/m_d)
with the pin q_d = m_d some 15.5 orders of magnitude inside.

**The committed numbers (exact rationals, eV).**  The ladder-pinned dust mass
m_d = 5088.9 eV = 5088900/1000 (YM02's 5.088883 keV germ face), and the
Planck mass M_pl = 2.4356e27 eV.  NOTE on the literal: 2.4356e27 eV IS the
integer 2435600000000000000000000000 -- the variant
2435600000000000000000000000/1000 would evaluate to 2.4356e24 eV and makes
the ratio band 2*(m_d/M_pl)^2 < 1e-46 FALSE (Python fractions:
2*(m_d/M_pl)^2 = 8.731e-42 there, not 8.731e-48), so the committed value is
used WITHOUT the spurious /1000.  With the committed value:
2*(m_d/M_pl)^2 = 2589690321/296607368000000000000000000000000000000000000000000000000
                = 8.731038404278615e-48 < 1e-46        (slack factor 11.45),
7.07e-9 * (M_pl/m_d) = 172196920000000000000/50889 = 3.3837748825875925e15
                > 1                                   (slack ~15.5 orders).
The band inequality is the cross-multiplied comparison of exact rationals
(707/10^11) * (M_pl/m_d) > 1, closed by `norm_num` on the cleared fraction.

Nothing here claims the SU(3)/QCD-scale gap (the Clay problem): the framework
has no QCD sector (TOE_STATUS.md); what is proven is the framework's OWN gap
mechanism with its mass PINNED by the ladder inversion.

Zero sorry.  Axioms: {propext, Classical.choice, Quot.sound} only.  Compiled
against the repo's Mathlib build (Lean 4.34.0-rc2).
-/
noncomputable section
open scoped Real

/-- the committed dust mass (the ladder pin) in eV: m_d = 5088.9 eV -/
def m_d_fid : ℝ := 5088900 / (10 : ℝ)^3

/-- the committed Planck mass in eV: M_pl = 2.4356e27 eV exactly -
    (the integer itself; see the header note on the /1000 variant) -/
def M_pl_fid : ℝ := 2435600000000000000000000000

/-- the U-map coefficient (restated from YM02): C_f = M_MOND a0/(sqrt2 Lambda^2)
    with M_MOND = sqrt2 M_pl, M_pl = 1/sqrt(8 pi G), Lambda^2 = 2 a0/sqrt G -/
noncomputable def C_f (G a0 : ℝ) : ℝ :=
  (Real.sqrt 2 / Real.sqrt (8 * Real.pi * G)) * (a0 * Real.sqrt G / (Real.sqrt 2 * (2 * a0)))

/-- the naked sqrt-pair: sqrt(8 pi G) = sqrt(8 pi) * sqrt G -- the square-trick
    (both sides square to 8 pi G) plus positivity (YM01/YM02, verbatim) -/
theorem sqrt_pair_8pi_naked (G : ℝ) (hG : 0 < G) :
    Real.sqrt (8 * Real.pi * G) = Real.sqrt (8 * Real.pi) * Real.sqrt G := by
  have hA : 0 ≤ 8 * Real.pi * G :=
    mul_nonneg (mul_nonneg (by norm_num : (0:ℝ) ≤ 8) Real.pi_pos.le) hG.le
  have hpi : 0 ≤ 8 * Real.pi := mul_nonneg (by norm_num : (0:ℝ) ≤ 8) Real.pi_pos.le
  have hL : (Real.sqrt (8 * Real.pi * G))^2 = 8 * Real.pi * G := Real.sq_sqrt hA
  have hR' : (Real.sqrt (8 * Real.pi) * Real.sqrt G)^2 = 8 * Real.pi * G := by
    calc
      (Real.sqrt (8 * Real.pi) * Real.sqrt G)^2
          = Real.sqrt (8 * Real.pi)^2 * Real.sqrt G^2 := by ring
      _ = 8 * Real.pi * G := by rw [Real.sq_sqrt hpi, Real.sq_sqrt hG.le]
  have hnn : 0 ≤ Real.sqrt (8 * Real.pi * G) := Real.sqrt_nonneg _
  have htp : 0 < Real.sqrt (8 * Real.pi) * Real.sqrt G := by
    exact mul_pos (Real.sqrt_pos.mpr (mul_pos (by norm_num : (0:ℝ) < 8) Real.pi_pos))
                  (Real.sqrt_pos.mpr hG)
  have hsq : Real.sqrt (8 * Real.pi * G)^2 = (Real.sqrt (8 * Real.pi) * Real.sqrt G)^2 :=
    (hR'.trans hL.symm).symm
  rcases (eq_or_eq_neg_of_sq_eq_sq _ _ hsq) with h1 | h2
  · exact h1
  · nlinarith [h2, hnn, htp]

/-- 0a. THE U-MAP CLOSED FORM (restated verbatim from YM02): C_f = 1/(2 sqrt(8 pi))
        -- a PURE NUMBER of the framework, G and a0 cancel -/
theorem C_f_value (G a0 : ℝ) (hG : 0 < G) (ha0 : 0 < a0) :
    C_f G a0 = 1 / (2 * Real.sqrt (8 * Real.pi)) := by
  unfold C_f
  have hpair : Real.sqrt (8 * Real.pi * G) = Real.sqrt (8 * Real.pi) * Real.sqrt G :=
    sqrt_pair_8pi_naked G hG
  have hm : (Real.sqrt 2 / Real.sqrt (8 * Real.pi * G)) *
        (a0 * Real.sqrt G / (Real.sqrt 2 * (2 * a0))) * (2 * Real.sqrt (8 * Real.pi)) = 1 := by
    rw [hpair]
    have hpi : 0 < 8 * Real.pi := mul_pos (by norm_num : (0:ℝ) < 8) Real.pi_pos
    have hsq : Real.sqrt (8 * Real.pi) ≠ 0 := (Real.sqrt_pos.mpr hpi).ne'
    field_simp [hG.ne', ha0.ne', hsq]
  have hnnz : 2 * Real.sqrt (8 * Real.pi) ≠ 0 := by
    exact mul_ne_zero (by norm_num : (2:ℝ) ≠ 0)
          (by exact (Real.sqrt_pos.mpr (mul_pos (by norm_num : (0:ℝ) < 8) Real.pi_pos)).ne')
  exact eq_div_of_mul_eq hnnz hm

/-- 0b. THE DEEP COEFFICIENT (restated verbatim from YM02): 1/(2 C_f) = sqrt(8 pi) -/
theorem deep_coeff (G a0 : ℝ) (hG : 0 < G) (ha0 : 0 < a0) :
    1 / (2 * C_f G a0) = Real.sqrt (8 * Real.pi) := by
  have hCf := C_f_value G a0 hG ha0
  have hpi : Real.sqrt (8 * Real.pi) ≠ 0 :=
    (Real.sqrt_pos.mpr (mul_pos (by norm_num : (0:ℝ) < 8) Real.pi_pos)).ne'
  rw [hCf]
  field_simp [hpi]

/-- 1. THE RATIO FORMULA (positivity): 0 < m_d -> 0 < M_pl
        ->  0 < 2 (m_d/M_pl)^2 -- the mass-ratio contribution is strictly
        positive (one nlinarith from the squared positive quotient) -/
theorem ratio_formula (m_d M_pl : ℝ) (hm : 0 < m_d) (hM : 0 < M_pl) :
    0 < 2 * (m_d / M_pl)^2 := by
  have hdiv : 0 < m_d / M_pl := div_pos hm hM
  have hsq : 0 < (m_d / M_pl)^2 := sq_pos_of_pos hdiv
  nlinarith [hsq]

/-- 2. THE RATIO BAND (numerical): at the committed numbers
        2 (m_d/M_pl)^2 = 8.731038404278615e-48 < 1e-46 -- exact rational
        arithmetic, closed by `norm_num` on the cleared fraction
        (slack factor 11.45, > 1 spare digit) -/
theorem ratio_band : 2 * (m_d_fid / M_pl_fid)^2 < 1 / (10 : ℝ)^46 := by
  norm_num [m_d_fid, M_pl_fid]

/-- 2b. the same band with the committed rationals as naked literals:
        2 * (5088900/1000 / 2435600000000000000000000000)^2 < 1e-46 -/
theorem ratio_band_lit :
    2 * ((5088900 / 1000 : ℝ) / (2435600000000000000000000000 : ℝ))^2
      < 1 / (10 : ℝ)^46 := by
  norm_num

/-- 3. THE BAND MARGIN (numerical): the virial-exactness band
        q_d/m_d <= 7.07e-9 * (M_pl/m_d) at the pin q_d = m_d is
        1 < 7.07e-9 * (M_pl/m_d) = 3.3837748825875925e15 (exact rational;
        slack ~15.5 orders of magnitude) -/
theorem band_margin : (1 : ℝ) < (707 / (10 : ℝ)^11) * (M_pl_fid / m_d_fid) := by
  norm_num [m_d_fid, M_pl_fid]

/-- 3b. the pin is INSIDE the band, abstractly in q_d:
        q_d = m_d  ->  q_d/m_d <= 7.07e-9 * (M_pl/m_d) -/
theorem virial_band_pin (q : ℝ) (hq : q = m_d_fid) :
    q / m_d_fid ≤ (707 / (10 : ℝ)^11) * (M_pl_fid / m_d_fid) := by
  have hm : 0 < m_d_fid := by norm_num [m_d_fid]
  rw [hq]
  rw [div_self (ne_of_gt hm)]
  exact le_of_lt band_margin

/-- 4. THE VIRIAL-CONSISTENCY BUNDLE: both numeric bands at once --/
theorem ratio_band_and_margin :
    2 * (m_d_fid / M_pl_fid)^2 < 1 / (10 : ℝ)^46 ∧
      (1 : ℝ) < (707 / (10 : ℝ)^11) * (M_pl_fid / m_d_fid) := by
  constructor
  · exact ratio_band
  · exact band_margin

end
#print axioms sqrt_pair_8pi_naked
#print axioms C_f_value
#print axioms deep_coeff
#print axioms ratio_formula
#print axioms ratio_band
#print axioms ratio_band_lit
#print axioms band_margin
#print axioms virial_band_pin
#print axioms ratio_band_and_margin