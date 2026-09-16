/-
  Q005 -- THE BTFR ZERO-POINT VELOCITY RATIO -- the Lean certificate.

  G03E (deepseek, the equipartition law) gives v^2 = v_b^2 + v_flat^2
  (quadrature, the Teissier/BTFR form) and claims the MOND-radius zero
  point. This certifies the IDEALIZED zero point as an exact identity:
  constant-density baryons M_b(<r>) = b r^3 and the LINEAR phantom
  M_ph(<r>) = (S/G) r (the Q003 amplitude law) give

      v_b^2(r)   = G M_b(<r>)/r  = G b r^2      (rises with r)
      v_flat^2(r)= G M_ph(<r>)/r = S             (constant = flat curve)
      v_dyn^2(r) = G b r^2 + S

  and at r_M where M_ph(r_M) = M_b(r_M) the ratio v_dyn^2/v_b^2 is
  EXACTLY 2 (v_dyn/v_b = sqrt(2)). Derived, not fitted. (G03E's
  realistic-profile numbers 1.095 / 1.049 at 5/10 r_M are the refinement;
  this is the clean constant-density core.)

  Scope: the certificate machine-checks the ALGEBRA of the zero point in
  the stated model. It does not machine-check that real halos are
  constant-density (they are not) nor the astrophysical input b, S.
-/
import Mathlib

open Real

noncomputable section

/-- The baryon velocity squared, v_b^2 = G b r^2, for constant density b. -/
def v_b_sq (G b r : ℝ) : ℝ := G * b * r ^ 2

/-- The enclosed baryon mass, M_b(<r>) = b r^3. -/
def Mb (b r : ℝ) : ℝ := b * r ^ 3

/-- The enclosed phantom mass, M_ph(<r>) = (S/G) r (the Q003 linear law). -/
def Mph (S G r : ℝ) : ℝ := S / G * r

noncomputable def rM (G b S : ℝ) : ℝ := Real.sqrt (S / (G * b))

/-! ## 1. The MOND radius equates the two enclosed masses -/

theorem rM_equates_masses (G b S : ℝ) (hG : 0 < G) (hb : 0 < b) (hS : 0 < S) :
    Mph S G (rM G b S) = Mb b (rM G b S) := by
  have hrM2 : (rM G b S) ^ 2 = S / (G * b) := by
    rw [show rM G b S = Real.sqrt (S / (G * b)) from rfl]
    exact Real.sq_sqrt (le_of_lt (div_pos hS (mul_pos hG hb)))
  have hMph : Mph S G (rM G b S) = S / G * rM G b S := rfl
  have hMb : Mb b (rM G b S) = b * (rM G b S) ^ 3 := rfl
  rw [hMph, hMb]
  have hcube : (rM G b S) ^ 3 = (rM G b S) ^ 2 * rM G b S := by ring
  rw [hcube, hrM2]
  field_simp [hG.ne, hb.ne]

/-! ## 2. At r_M the baryon velocity squared equals S (the flat term) -/

theorem vbsq_at_rM (G b S : ℝ) (hG : 0 < G) (hb : 0 < b) (hS : 0 < S) :
    v_b_sq G b (rM G b S) = S := by
  have hrM2 : (rM G b S) ^ 2 = S / (G * b) := by
    rw [show rM G b S = Real.sqrt (S / (G * b)) from rfl]
    exact Real.sq_sqrt (le_of_lt (div_pos hS (mul_pos hG hb)))
  have hvb : v_b_sq G b (rM G b S) = G * b * (rM G b S) ^ 2 := rfl
  rw [hvb, hrM2]
  field_simp [hG.ne, hb.ne]

/-! ## 3. THE ZERO POINT: v_dyn^2 / v_b^2 = 2 at r_M (ratio sqrt(2)) -/

theorem ratio_at_rM (G b S : ℝ) (hG : 0 < G) (hb : 0 < b) (hS : 0 < S) :
    (v_b_sq G b (rM G b S) + S) / v_b_sq G b (rM G b S) = 2 := by
  have h1 : v_b_sq G b (rM G b S) = S := vbsq_at_rM G b S hG hb hS
  rw [h1]
  field_simp [hS.ne]
  norm_num

end

#guard false in #print axioms rM_equates_masses
#guard false in #print axioms vbsq_at_rM
#guard false in #print axioms ratio_at_rM