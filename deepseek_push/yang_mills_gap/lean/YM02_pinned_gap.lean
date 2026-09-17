import Mathlib

/-!
# YM02 -- THE PINNED GAP: the ladder-pinned mass of the gauged a0-sector

**Scope statement (as every certificate in this repo reads):** Lean certifies
the MATHEMATICS. The physical premises -- L5's shift-symmetric action
L = Lambda^4 f(K), K = -(1/2)(D phi)^2/Lambda^4, the minimal Stueckelberg
gauging D phi = d phi - m A, L2/G031's kernel f'(K) = mu_2(u), and the
m = m_dust IDENTIFICATION (the ladder inversion m = k_B T_0 (1+z*)/sigma^2,
B03/A08, with the committed fiducial constants T_0 = 2.7255 K, z* = 2.426,
sigma = 119.21 km/s) -- are the committed lanes' claims
(deepseek_push/yang_mills_gap/YM01_gap_derivation.py, YM_PROOF.md,
project_atomos/B03_doubleZ_mass.py, deepseek_push/C02_environment_blind.py).
This file restates every definition from scratch (standalone: `import Mathlib`
only, no import of YM01_gap.lean) and certifies the algebraic spine of the
PINNED gap: the ladder's positivity and invertibility (the freeze inversion
(1+z*) = m sigma^2/(k_B T_0) is the exact inverse of the ladder), the pinned
gap face m_A = m_dust * sqrt(mu_2(u)) (positivity and square), the U-MAP
closed form C_f = 1/(2 sqrt(8 pi)) and its deep coefficient, THE GAP
(omega(k)^2 = k^2 + m_A^2, so omega >= m_dust, attained at k = 0), the Fock
face (n >= 1 excitations cost at least m_dust), the vacuum closing, and the
NUMERIC BAND of the committed constants.

Nothing here claims the SU(3)/QCD-scale gap (the Clay problem): the framework
has no QCD sector (TOE_STATUS.md); what is proven is the framework's OWN gap
mechanism with its mass PINNED by the ladder inversion.

**THE NUMERIC BAND -- what is certified and what is not.** The direct
evaluation of the committed ladder at the fiducial constants
(k_B = 1.380649e-23, T_0 = 2.7255 K, z* = 2.426, sigma = 119210 m/s) is

    m (keV) = k_B T_0 (1+z*) c^2 / (sigma^2 * eV * 1000)
            = 656840091214118741161958387 / 129073530375458500000000000
            = 5.088883 keV        (exact rational; Python-certified)

certified here, by exact rational `norm_num` arithmetic (no transcendental
appears -- c, eV, k_B, T_0 and sigma are exact decimal rationals), in three
committed windows: above the L10 particle floor 3.3 keV, inside the G168 V3
kill band (4, 6) keV, and inside the G212 1-sigma band (4.99, 5.19) keV
(the G212 germ is m = 5.089 +- 0.097 keV, joint posterior peak 5.089).

The task brief's window (4.999, 5.001) keV is NOT a Lean-certifiable direct
evaluation at these constants and is deliberately NOT stated: it is the
environment-blind RECOVERY band of the freeze inversion (C02/B03: 101,600
environments, recovery spread ~1e-4 keV), which is consistent-by-construction
(the freeze map is built at the 5 keV footing and the inversion recovers
m_rec = m by the certified identity ladder_roundtrip below). A z* of
2.36616 -- not the committed 2.426 -- would pin exactly 5.000 keV at
sigma = 119.21 km/s; the committed constants pin 5.088883 keV, inside the
G212 band. Named blocker for the (4.999, 5.001) statement: the brief's
literal formula E = k_B T_0(1+z*)/sigma^2 / eV evaluates to 5.66e-11 keV
and even the physical (sigma/c)^2 inversion gives 5.088883 keV, outside that
window; the honest committed band is what this file certifies. Python lane
(fractions.Fraction) certifies all intervals quoted above; Lean certifies
the three window theorems.

Zero sorry. Axioms: {propext, Classical.choice, Quot.sound} only. Compiled
against the repo's Mathlib build (Lean 4.34.0-rc2).
-/
noncomputable section
open scoped Real

noncomputable def mu2 (u : ℝ) : ℝ := u * (2 + u) / (1 + u)^2
noncomputable def ladder_mass (kB T0 zstar s2 : ℝ) : ℝ := kB * T0 * (1 + zstar) / s2
noncomputable def capped_gap (md u : ℝ) : ℝ := md * Real.sqrt (mu2 u)
noncomputable def C_f (G a0 : ℝ) : ℝ :=
  (Real.sqrt 2 / Real.sqrt (8 * Real.pi * G)) * (a0 * Real.sqrt G / (Real.sqrt 2 * (2 * a0)))

/-- the ladder mass quoted in keV: the committed inversion (kg) times c^2,
    divided by the eV and the milli- conversion -- every factor is an exact
    decimal rational, so `norm_num` closes the cleared product -/
noncomputable def ladder_keV (kB T0 zstar s2 : ℝ) : ℝ :=
  kB * T0 * (1 + zstar) * (299792458 : ℝ)^2 / (s2 * (1602176634 / (10 : ℝ)^28)) / 1000

/-- the committed fiducial constants as exact decimal rationals:
    k_B = 1.380649e-23, T_0 = 2.7255 K, z* = 2.426, sigma = 119.21 km/s = 119210 m/s -/
def kB_fid : ℝ := 1380649 / (10 : ℝ)^29
def T0_fid : ℝ := 27255 / (10 : ℝ)^4
def zstar_fid : ℝ := 2426 / (10 : ℝ)^3
def s2_fid : ℝ := (119210 : ℝ)^2

/-- the kernel face is positive: 0 < u  ->  0 < mu_2(u) -- no ghost sector -/
theorem mu2_pos (u : ℝ) (hu : 0 < u) : 0 < mu2 u := by
  unfold mu2
  have h2u : 0 < 2 + u := by linarith [hu]
  have hnum : 0 < u * (2 + u) := mul_pos hu h2u
  have hden : 0 < (1 + u)^2 := by nlinarith [hu]
  exact div_pos hnum hden

/-- the vacuum closing rung: mu_2(0) = 0 -- where the gradient dies the
    kernel dies --/
theorem mu2_zero : mu2 0 = 0 := by
  unfold mu2
  norm_num

/-- 1. THE LADDER IS POSITIVE: 0 < k_B, 0 < T_0, 0 < sigma^2, 0 <= z*
        ->  the dust mass m = k_B T_0 (1+z*)/sigma^2 is positive --/
theorem ladder_mass_pos (kB T0 zstar s2 : ℝ) (hkB : 0 < kB) (hT0 : 0 < T0)
    (hs2 : 0 < s2) (hz : 0 ≤ zstar) : 0 < ladder_mass kB T0 zstar s2 := by
  unfold ladder_mass
  have h1 : 0 < 1 + zstar := by linarith
  have hnum : 0 < kB * T0 * (1 + zstar) := mul_pos (mul_pos hkB hT0) h1
  exact div_pos hnum hs2

/-- 2. THE LADDER IS INVERTIBLE: substituting the freeze relation
        (1+z*) = m sigma^2/(k_B T_0) back into the ladder returns m
        IDENTICALLY (sigma^2 != 0): the certified algebra is the
        positive-reals field identity (a*b/c)*(c/a) = b (C02) --/
theorem ladder_roundtrip (kB T0 zstar s2 : ℝ) (hs2 : s2 ≠ 0) :
    ladder_mass kB T0 zstar s2 * s2 = kB * T0 * (1 + zstar) := by
  unfold ladder_mass
  field_simp [hs2]

/-- 3. THE PINNED GAP FACE IS POSITIVE: 0 < m_dust, 0 < u
        ->  0 < m_A = m_dust sqrt(mu_2(u)) -- the gap is open on the
        equilibrium branch --/
theorem capped_gap_pos (md u : ℝ) (hm : 0 < md) (hu : 0 < u) : 0 < capped_gap md u := by
  unfold capped_gap
  have hsqrt : 0 < Real.sqrt (mu2 u) := (Real.sqrt_pos).mpr (mu2_pos u hu)
  exact mul_pos hm hsqrt

/-- 4. THE PINNED GAP'S SQUARE: (m_A)^2 = m_dust^2 * mu_2(u) for 0 <= u
        (the u = 0 edge is the vacuum closing mu_2(0) = 0, certified by
        Real.sq_sqrt on the nonnegativity branch) --/
theorem capped_gap_sq_clean (md u : ℝ) (hu : 0 ≤ u) :
    (capped_gap md u)^2 = md^2 * mu2 u := by
  have hmu : 0 ≤ mu2 u := by
    rcases le_iff_lt_or_eq.mp hu with hu_lt | hu_eq
    · exact (mu2_pos u hu_lt).le
    · rw [← hu_eq]
      exact le_of_eq mu2_zero.symm
  unfold capped_gap
  rw [mul_pow]
  rw [Real.sq_sqrt hmu]

/-- the naked sqrt-pair: sqrt(8 pi G) = sqrt(8 pi) * sqrt G -- proven by the
    square-trick (both sides square to 8 pi G) plus positivity --/
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

/-- 5. THE U-MAP CLOSED FORM: with M_MOND = sqrt(2) M_pl, M_pl = 1/sqrt(8 pi G),
        Lambda^2 = 2 a0 / sqrt G (L1, Lambda^4 = 4 a0^2/G), the gradient map
        coefficient is C_f = M_MOND * a0 / (sqrt(2) * Lambda^2) = 1/(2 sqrt(8 pi)):
        a PURE NUMBER of the framework -- G and a0 cancel (YM01's u_map_closed,
        restated for the C_f definition; the same square-trick proof) --/
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

/-- 6. THE DEEP COEFFICIENT: 1/(2 C_f) = sqrt(8 pi) -- the field-equation deep
        face mu_2 ~ 2 u0 = x/sqrt(8 pi) of the map (one field_simp from
        C_f_value with sqrt(8 pi) != 0) --/
theorem deep_coeff (G a0 : ℝ) (hG : 0 < G) (ha0 : 0 < a0) :
    1 / (2 * C_f G a0) = Real.sqrt (8 * Real.pi) := by
  have hCf := C_f_value G a0 hG ha0
  have hpi : Real.sqrt (8 * Real.pi) ≠ 0 :=
    (Real.sqrt_pos.mpr (mul_pos (by norm_num : (0:ℝ) < 8) Real.pi_pos)).ne'
  rw [hCf]
  field_simp [hpi]

/-- 7. THE GAP (dispersion, pinned): for the pinned mass m_dust the branch
        omega(k) = sqrt(k^2 + m_dust^2) lies at or above the mass on EVERY
        momentum -- the Proca dispersion of the gauged sector, copied from
        YM01's gap_theorem (Real.sqrt_le_sqrt + sqrt_sq_eq_abs chain) --/
theorem gap_dispersion (k md : ℝ) (hm : 0 < md) : md ≤ Real.sqrt (k^2 + md^2) := by
  have h1 : md^2 ≤ k^2 + md^2 := by nlinarith [sq_nonneg k]
  have hs : Real.sqrt (md^2) ≤ Real.sqrt (k^2 + md^2) := Real.sqrt_le_sqrt h1
  have hsm : Real.sqrt (md^2) = md := by
    rw [Real.sqrt_sq_eq_abs]
    rw [abs_of_nonneg (le_of_lt hm)]
  rwa [hsm] at hs

/-- 8. THE GAP IS TIGHT: the bound is attained at k = 0 -- the B8 zero mode
        is lifted to exactly m_dust (the lowest excitation exists) --/
theorem gap_tight_pinned (md : ℝ) (hm : 0 < md) : Real.sqrt (0^2 + md^2) = md := by
  have h0 : (0:ℝ)^2 = 0 := by norm_num
  rw [h0, zero_add]
  rw [Real.sqrt_sq_eq_abs]
  rw [abs_of_nonneg (le_of_lt hm)]

/-- 9. THE FOCK FACE: any n >= 1 quantum excitation costs at least m_dust
        (the free-Fock spectrum of the massive branch is integer multiples
        of omega on each mode, omega >= m_dust, so the lowest nonzero
        eigenvalue is m_dust) --/
theorem excitation_pinned (md k n : ℝ) (hm : 0 < md) (hn : 1 ≤ n) :
    md ≤ n * Real.sqrt (k^2 + md^2) := by
  have hw : md ≤ Real.sqrt (k^2 + md^2) := gap_dispersion k md hm
  nlinarith [hw, hn]

/-- 10. THE VACUUM CLOSING: no gradient, no gap -- m_A(m_dust, 0) = 0 -/
theorem vacuum_zero (md : ℝ) : capped_gap md 0 = 0 := by
  unfold capped_gap
  rw [mu2_zero]
  norm_num

/-- 11a. THE NUMERIC BAND -- the L10 particle floor: at the committed
         constants the ladder mass lies ABOVE the 3.3 keV particle floor.
         Exact rational arithmetic: every factor (k_B, T_0, 1+z*, c^2, sigma^2,
         eV) is an exact decimal rational, so `norm_num` closes the cleared
         product with no transcendental --/
theorem ladder_keV_floor : (33/10 : ℝ) < ladder_keV kB_fid T0_fid zstar_fid s2_fid := by
  norm_num [ladder_keV, kB_fid, T0_fid, zstar_fid, s2_fid]

/-- 11b. THE NUMERIC BAND -- the G168 V3 kill band: the committed ladder mass
         lands inside (4, 6) keV (the A05/A08 committed kill band the germ
         must live in; the direct evaluation is 5.088883 keV) --/
theorem ladder_keV_kill_band : (4 : ℝ) < ladder_keV kB_fid T0_fid zstar_fid s2_fid ∧
    ladder_keV kB_fid T0_fid zstar_fid s2_fid < (6 : ℝ) := by
  norm_num [ladder_keV, kB_fid, T0_fid, zstar_fid, s2_fid]

/-- 11c. THE NUMERIC BAND -- the G212 1-sigma band: the committed ladder mass
         lands inside (4.99, 5.19) keV, the sharpest committed window (the
         G212 germ m = 5.089 +- 0.097 keV).  This is the honest certified
         replacement for the brief's (4.999, 5.001) window, which holds for
         the environment-blind RECOVERY band (z* = 2.36616 pins exactly
         5.000 keV at sigma = 119.21 km/s), not for the direct evaluation at
         the committed z* = 2.426 (5.088883 keV; see the header scope note) --/
theorem ladder_keV_G212_band : (499/100 : ℝ) < ladder_keV kB_fid T0_fid zstar_fid s2_fid ∧
    ladder_keV kB_fid T0_fid zstar_fid s2_fid < (519/100 : ℝ) := by
  norm_num [ladder_keV, kB_fid, T0_fid, zstar_fid, s2_fid]

/-- 12. THE POSITIVE BAND (the pinned face, bundled): 0 < m_dust, 0 < u
         ->  0 < m_A and (m_A)^2 = m_dust^2 mu_2(u) -- the gap is open AND
         its square is the clean face --/
theorem pinned_gap_positive_band (md u : ℝ) (hm : 0 < md) (hu : 0 < u) :
    0 < capped_gap md u ∧ (capped_gap md u)^2 = md^2 * mu2 u := by
  constructor
  · exact capped_gap_pos md u hm hu
  · exact capped_gap_sq_clean md u (le_of_lt hu)

end
#print axioms mu2_pos
#print axioms mu2_zero
#print axioms ladder_mass_pos
#print axioms ladder_roundtrip
#print axioms capped_gap_pos
#print axioms capped_gap_sq_clean
#print axioms sqrt_pair_8pi_naked
#print axioms C_f_value
#print axioms deep_coeff
#print axioms gap_dispersion
#print axioms gap_tight_pinned
#print axioms excitation_pinned
#print axioms vacuum_zero
#print axioms ladder_keV_floor
#print axioms ladder_keV_kill_band
#print axioms ladder_keV_G212_band
#print axioms pinned_gap_positive_band