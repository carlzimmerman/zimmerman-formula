import Mathlib

/-!
# EQB_S3 -- the closed-form CPL bump of a sqrt(rho_DE)-tracking a0 (Lean 4 certificate)

Source (committed): `prep_2026/equation_book/eqbook_S3_welds.py`, checks E-S3.6 / E-S3.6b / E-S3.6c (lines 96-114);
write-up `prep_2026/equation_book/MINE_M1.md` row 8 (also MINE_M1 E-S3.6).

PREMISE (a definition, NOT certified as physics): the CPL dark-energy density history
    rho(z)/rho(0) = (1+z)^(3(1 + w0 + wa)) * exp(-3 wa z/(1+z)),     z > -1,
written here as exp(f(z)) with f(z) = 3k ln(1+z) - 3 wa z/(1+z),  k = 1 + w0 + wa.
(The framework's "declining footing" a0 ~ sqrt(rho_DE) makes a0(z)/a0(0) = sqrt(rho(z)/rho(0)); a square root is monotone, so the
location of the maximum is the same; that footing is a PREMISE of the script and is NOT used or certified here.)

CERTIFIED (premises => conclusions, exact real analysis):
  * `cpl_f_hasDeriv`   : f'(z) = 3 (k (1+z) - wa)/(1+z)^2 for z > -1
  * `cpl_peak_iff`     : for k != 0, f'(z) = 0 iff z = -(1+w0)/k
  * `cpl_strict_max`   : for k < 0 and wa < 0, z_pk = -(1+w0)/k > -1 is the STRICT global maximum of rho on (-1, oo)
                         (rho(z) < rho(z_pk) for every z != z_pk); proved from ln x > 1 - 1/x, no numerics
  * `cpl_amplitude`    : rho(z_pk) = (wa/k)^(3k) * exp(3(1 + w0))   (the closed-form peak amplitude, real power)
  * `cpl_peak_pos_iff` : for k < 0, wa < 0: z_pk > 0 iff 1 + w0 > 0 (the peak lies at positive redshift exactly then), and then
                         rho(z_pk) > rho(0) = 1 (a genuine bump)
NOT certified: the numerical DESI-class values (z_pk = 0.41, +6.3% for a0), the CPL parametrisation as a description of dark energy,
the a0 ~ sqrt(rho_DE) footing, the RISING-footing statement (monotone H(z), the script's E-S3.6d), any data.  kappa = 1/2 (FITTED)
does not enter.
-/

open Real

noncomputable section

/-- log of the CPL density ratio, k = 1 + w0 + wa. -/
def cplF (w0 wa z : ℝ) : ℝ := 3 * (1 + w0 + wa) * Real.log (1 + z) - 3 * wa * z / (1 + z)

/-- the CPL density ratio rho(z)/rho(0). -/
def rhoCPL (w0 wa z : ℝ) : ℝ := Real.exp (cplF w0 wa z)

theorem rhoCPL_eq_rpow {w0 wa z : ℝ} (hz : -1 < z) :
    rhoCPL w0 wa z = (1 + z) ^ (3 * (1 + w0 + wa)) * Real.exp (-3 * wa * z / (1 + z)) := by
  have hu : 0 < 1 + z := by linarith
  unfold rhoCPL cplF
  rw [Real.rpow_def_of_pos hu, ← Real.exp_add]
  congr 1
  rw [mul_comm (Real.log (1 + z))]
  ring

theorem cpl_f_hasDeriv (w0 wa : ℝ) {z : ℝ} (hz : -1 < z) :
    HasDerivAt (cplF w0 wa) (3 * ((1 + w0 + wa) * (1 + z) - wa) / (1 + z) ^ 2) z := by
  have hu : 0 < 1 + z := by linarith
  have hune : 1 + z ≠ 0 := hu.ne'
  have h1 : HasDerivAt (fun t : ℝ => 1 + t) 1 z := by
    simpa using (hasDerivAt_id z).const_add 1
  have h2 : HasDerivAt (fun t : ℝ => Real.log (1 + t)) (1 / (1 + z)) z := by
    simpa using h1.log hune
  have h3 : HasDerivAt (fun t : ℝ => 3 * (1 + w0 + wa) * Real.log (1 + t))
      (3 * (1 + w0 + wa) * (1 / (1 + z))) z := h2.const_mul _
  have h4 : HasDerivAt (fun t : ℝ => 3 * wa * t) (3 * wa * 1) z := (hasDerivAt_id z).const_mul _
  have h4' : HasDerivAt (fun t : ℝ => 3 * wa * t) (3 * wa) z := by simpa using h4
  have h5 := h4'.div h1 hune
  have h6 := h3.sub h5
  unfold cplF
  refine h6.congr_deriv ?_
  field_simp
  ring

theorem cpl_peak_iff (w0 wa : ℝ) {z : ℝ} (hz : -1 < z) (hk : 1 + w0 + wa ≠ 0) :
    3 * ((1 + w0 + wa) * (1 + z) - wa) / (1 + z) ^ 2 = 0 ↔ z = -(1 + w0) / (1 + w0 + wa) := by
  have hu : 0 < 1 + z := by linarith
  have hsq : (1 + z) ^ 2 ≠ 0 := by positivity
  rw [div_eq_zero_iff]
  constructor
  · rintro (h | h)
    · have : (1 + w0 + wa) * (1 + z) - wa = 0 := by linarith
      field_simp
      linarith
    · exact absurd h hsq
  · intro h
    left
    rw [h]
    field_simp
    ring

/-- the key inequality behind the strict maximum: for k < 0, wa = k u*, u* > 0, and every u > 0, u != u*. -/
theorem cpl_key {k ws u us : ℝ} (hk : k < 0) (hus : 0 < us) (hu : 0 < u) (hne : u ≠ us) (hw : ws = k * us) :
    3 * k * Real.log u + 3 * ws / u < 3 * k * Real.log us + 3 * ws / us := by
  have hx : 0 < u / us := by positivity
  have hx1 : u / us ≠ 1 := by
    intro h; apply hne; field_simp at h; linarith
  have hlog : Real.log (us / u) < us / u - 1 := Real.log_lt_sub_one_of_pos (by positivity) (by
    intro h; apply hne; field_simp at h; linarith)
  have hl : Real.log (us / u) = Real.log us - Real.log u := Real.log_div hus.ne' hu.ne'
  rw [hl] at hlog
  have hsub : k * (Real.log us - Real.log u) > k * (us / u - 1) := by nlinarith
  have hfin : 3 * ws / u - 3 * ws / us = 3 * k * (us - u) / u := by
    rw [hw]; field_simp
  have hfin2 : 3 * k * (us - u) / u = 3 * k * (us / u - 1) := by field_simp
  nlinarith

theorem cpl_strict_max {w0 wa : ℝ} (hk : 1 + w0 + wa < 0) (hwa : wa < 0) {z : ℝ} (hz : -1 < z)
    (hne : z ≠ -(1 + w0) / (1 + w0 + wa)) :
    rhoCPL w0 wa z < rhoCPL w0 wa (-(1 + w0) / (1 + w0 + wa)) := by
  set k := 1 + w0 + wa with hkdef
  have hk0 : k ≠ 0 := hk.ne
  set zp := -(1 + w0) / k with hzp
  have hus : 0 < wa / k := div_pos_of_neg_of_neg hwa hk
  have h1zp : 1 + zp = wa / k := by
    rw [hzp]; field_simp; linarith
  have hzp1 : -1 < zp := by
    have : 0 < 1 + zp := by rw [h1zp]; exact hus
    linarith
  have hu : 0 < 1 + z := by linarith
  have hne' : 1 + z ≠ 1 + zp := by intro h; apply hne; linarith
  have hexp : ∀ t : ℝ, -1 < t → cplF w0 wa t = 3 * k * Real.log (1 + t) + 3 * wa / (1 + t) - 3 * wa := by
    intro t ht
    have : 1 + t ≠ 0 := by linarith
    unfold cplF; rw [hkdef]; field_simp; ring
  unfold rhoCPL
  apply Real.exp_lt_exp.mpr
  rw [hexp z hz, hexp zp hzp1]
  have key := cpl_key (k := k) (ws := wa) (u := 1 + z) (us := 1 + zp) hk (by linarith) hu hne'
    (by rw [h1zp]; field_simp)
  linarith

theorem cpl_amplitude {w0 wa : ℝ} (hk : 1 + w0 + wa < 0) (hwa : wa < 0) :
    rhoCPL w0 wa (-(1 + w0) / (1 + w0 + wa))
      = (wa / (1 + w0 + wa)) ^ (3 * (1 + w0 + wa)) * Real.exp (3 * (1 + w0)) := by
  set k := 1 + w0 + wa with hkdef
  have hk0 : k ≠ 0 := hk.ne
  set zp := -(1 + w0) / k with hzp
  have hus : 0 < wa / k := div_pos_of_neg_of_neg hwa hk
  have h1zp : 1 + zp = wa / k := by rw [hzp]; field_simp; linarith
  have hzp1 : -1 < zp := by
    have : 0 < 1 + zp := by rw [h1zp]; exact hus
    linarith
  rw [rhoCPL_eq_rpow hzp1, h1zp]
  congr 1
  congr 1
  have hne : 1 + zp ≠ 0 := by rw [h1zp]; exact hus.ne'
  rw [h1zp] at hne
  have hwa0 : wa ≠ 0 := hwa.ne
  rw [hzp]
  field_simp

theorem cpl_peak_pos_iff {w0 wa : ℝ} (hk : 1 + w0 + wa < 0) (hwa : wa < 0) :
    0 < -(1 + w0) / (1 + w0 + wa) ↔ 0 < 1 + w0 := by
  constructor
  · intro h
    have := (div_pos_iff.mp h)
    rcases this with ⟨_, h2⟩ | ⟨h1, _⟩
    · linarith
    · linarith
  · intro h
    exact div_pos_of_neg_of_neg (by linarith) hk

theorem cpl_bump {w0 wa : ℝ} (hk : 1 + w0 + wa < 0) (hwa : wa < 0) (hw : 0 < 1 + w0) :
    rhoCPL w0 wa 0 < rhoCPL w0 wa (-(1 + w0) / (1 + w0 + wa)) ∧ rhoCPL w0 wa 0 = 1 := by
  have hpos := (cpl_peak_pos_iff hk hwa).mpr hw
  refine ⟨cpl_strict_max hk hwa (by norm_num) hpos.ne, ?_⟩
  unfold rhoCPL cplF
  simp

end

#print axioms rhoCPL_eq_rpow
#print axioms cpl_f_hasDeriv
#print axioms cpl_peak_iff
#print axioms cpl_strict_max
#print axioms cpl_amplitude
#print axioms cpl_peak_pos_iff
#print axioms cpl_bump
