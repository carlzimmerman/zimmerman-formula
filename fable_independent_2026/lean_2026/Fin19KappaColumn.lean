import Mathlib

/-!
  FINAL-19 (KAPPA_C) -- the DEEP-FIELD COLUMN, certified in Lean 4.34.0-rc2 with Mathlib.

  SCOPE.  Pure real algebra / field arithmetic.  Nothing here asserts physics, and nothing
  here derives the NUMBER of kappa: kappa is a measured input of the lane and this file
  certifies only the algebraic spine the lane's numbers ride on.  ZERO `sorry`, ZERO `admit`,
  ZERO custom axioms; the printed axiom sets are subsets of
  {propext, Classical.choice, Quot.sound}.

  WHAT IS CERTIFIED
    (1) `jeans_beta2_term` / `jeans_integrating_factor`
        The spherical Jeans operator for the law's anisotropy `Pi_tt = -Pi_rr`: the `2/r`
        term doubles, and `r^4` is its integrating factor.
    (2) `column_stress_identity`
        On the deep-field branch `g = C/r`, with column `Sigma = C/(K r)` (`K = 4 pi G`),
        the law's stress magnitude is `|Pi| = 2 pi G Sigma^2`.
    (3) `column_stress_at_universal_column`
        At the record's universal column `Sigma_c = a0/(2 pi G)` the required stress is
        `a0^2/(2 pi G)` -- i.e. FOUR times the law's pressure scale `a0^2/(8 pi G)`.
    (4) `master_ratio`
        `kappa^2 * Sigma_vac^2 = 2 pi f * Sigma_c^2`, i.e. `R^2 = 2 pi f / kappa^2`
        with `R = Sigma_vac / Sigma_c` and `Pi_vac = f * eps`.
    (5) `saturation_forces_kappa`
        Demanding `Sigma_c = Sigma_vac` forces `kappa^2 = 2 pi f` -- the inversion the lane
        is asked for.  With the pre-registered `f = 1` this is `kappa = sqrt(2 pi)`, NOT `1/2`.
    (6) `identity_iff_kappa_half`
        The record's identity `a0^2/(8 pi G) = rho c^2/(32 pi)` is ALGEBRAICALLY EQUIVALENT to
        `kappa^2 = 1/4` (given `a0^2 = kappa^2 G rho c^2`).  It therefore carries no
        information beyond the number it is used to "derive" -- this is the circularity arm.
    (7) `kappa_half_requires_eight_pi`
        `kappa = 1/2` corresponds to `f = 1/(8 pi)`: the vacuum's energy density must be
        divided by Einstein's 8 pi before it can act as the deployable anisotropic stress.

  WHAT IS NOT CERTIFIED (and where it lives)
    The deep-field limit `J -> g^2/(2K)` (i.e. `Pi_rr = -Pi_tt`) is an asymptotic statement
    about `J(g) = (a0^2/K)(u - ln(1+u))`; it is verified symbolically in the lane's Python
    (`f19_kappa_C.py`: sympy series, and the numeric table whose ratio tracks `2u/3`).  The
    physical input `Pi_vac = f * eps` with `f = 1` (the dominant-energy-condition ceiling) is
    a pre-registered assumption of the lane, not a theorem.
-/

namespace Final19

noncomputable section

/-! ## 0. Objects -/

/-- `K = 4 pi G`, the record's stress normalisation. -/
def Kc (G : ℝ) : ℝ := 4 * Real.pi * G

/-- the isotropic part of the law's static stress: `J(g) = (a0^2/K)(u - ln(1+u))`, `u = g/a0`. -/
def Jc (a0 G g : ℝ) : ℝ := (a0 ^ 2 / Kc G) * (g / a0 - Real.log (1 + g / a0))

/-- `Pi_rr = J - g^2/(K(1+u))` -/
def Pir (a0 G g : ℝ) : ℝ := Jc a0 G g - g ^ 2 / (Kc G * (1 + g / a0))

/-- `Pi_tt = J` -/
def Pit (a0 G g : ℝ) : ℝ := Jc a0 G g

/-- the deep-field magnitude of each principal value: `P(g) = g^2/(2K) = g^2/(8 pi G)`. -/
def Pm (G g : ℝ) : ℝ := g ^ 2 / (2 * Kc G)

/-- the column above radius `r` on the deep-field branch: `Sigma = C/(K r)`, `C = v_inf^2`. -/
def Sig (G C r : ℝ) : ℝ := C / (Kc G * r)

/-- the record's universal column: `Sigma_c = a0/(2 pi G)`. -/
def Sc (a0 G : ℝ) : ℝ := a0 / (2 * Real.pi * G)

/-! ## 1. The Jeans operator with the law's anisotropy -/

/-- **(1a)** With `Pi_tt = -Pi_rr` the anisotropy term of the spherical Jeans operator
    `dPi_rr/dr + (2/r)(Pi_rr - Pi_tt)` doubles: it becomes `dPi_rr/dr + (4/r) Pi_rr`.
    (`dP` is the radial derivative value, carried as a variable so no calculus is needed.) -/
theorem jeans_beta2_term (r dP P : ℝ) :
    dP + (2 / r) * (P - (-P)) = dP + (4 / r) * P := by
  ring

/-- **(1b)** `r^4` is the integrating factor of the beta = 2 operator:
    `(1/r^4) d(r^4 P)/dr = dP/dr + (4/r) P`. -/
theorem jeans_integrating_factor (r dP P : ℝ) (hr : r ≠ 0) :
    (1 / r ^ 4) * (4 * r ^ 3 * P + r ^ 4 * dP) = dP + (4 / r) * P := by
  field_simp [hr]
  ring

/-! ## 2. The column-stress relation (the load-bearing step) -/

/-- **(2)** On the deep-field branch `g = C/r` the column is `Sigma = C/(K r)` and the law's
    stress magnitude is `2 pi G Sigma^2`. -/
theorem column_stress_identity (G C r : ℝ) (hG : G ≠ 0) (hr : r ≠ 0) :
    2 * Real.pi * G * (Sig G C r) ^ 2 = Pm G (C / r) := by
  unfold Sig Pm Kc
  field_simp [hG, Real.pi_ne_zero, hr]
  ring

/-- **(3)** At the record's universal column the required stress is `a0^2/(2 pi G)`
    -- exactly four times the law's pressure scale `a0^2/(8 pi G)`.  The factor 4 is the
    difference between `Sigma_c = a0/(2 pi G)` and the deep-field column outside the
    transition radius, `a0/(4 pi G)`; the lane carries both conventions explicitly. -/
theorem column_stress_at_universal_column (G a0 : ℝ) (hG : G ≠ 0) :
    2 * Real.pi * G * (Sc a0 G) ^ 2 = a0 ^ 2 / (2 * Real.pi * G) := by
  unfold Sc
  field_simp [hG, Real.pi_ne_zero]

/-- the law's pressure scale, for reference: `a0^2/(8 pi G) = a0^2/(2K)`. -/
theorem pressure_scale_def (G a0 : ℝ) : a0 ^ 2 / (8 * Real.pi * G) = a0 ^ 2 / (2 * Kc G) := by
  unfold Kc
  ring

/-! ## 3. The master ratio and the inversion -/

/-- **(4)** Master ratio.  Hypotheses, all algebraic:
    `h1`  the vacuum column satisfies the column-stress relation at the available stress
          `Pi_vac = f * eps` (this is (C2) with the capacity `f * eps`);
    `h2`  the universal column, `2 pi G Sigma_c = a0`, with `a0 = kappa sqrt(G eps)`;
    `hGe` `G eps >= 0` so the square root is real.
    Conclusion: `kappa^2 Sigma_vac^2 = 2 pi f Sigma_c^2`, i.e. `R^2 = 2 pi f / kappa^2`. -/
theorem master_ratio (G eps kappa f Sv Sc' : ℝ)
    (hG : G ≠ 0) (hpi : Real.pi ≠ 0)
    (h1 : 2 * Real.pi * G * Sv ^ 2 = f * eps)
    (h2 : 2 * Real.pi * G * Sc' = kappa * Real.sqrt (G * eps))
    (hGe : 0 ≤ G * eps) :
    kappa ^ 2 * Sv ^ 2 = 2 * Real.pi * f * Sc' ^ 2 := by
  have hsq : (2 * Real.pi * G * Sc') ^ 2 = (kappa * Real.sqrt (G * eps)) ^ 2 := by
    rw [h2]
  have hs : (Real.sqrt (G * eps)) ^ 2 = G * eps := Real.sq_sqrt hGe
  have hke : kappa ^ 2 * G * eps = (2 * Real.pi * G) ^ 2 * Sc' ^ 2 := by
    calc
      kappa ^ 2 * G * eps = (kappa * Real.sqrt (G * eps)) ^ 2 := by
        rw [mul_pow, hs]
        ring
      _ = (2 * Real.pi * G * Sc') ^ 2 := by rw [← h2]
      _ = (2 * Real.pi * G) ^ 2 * Sc' ^ 2 := by ring
  have hke2 : kappa ^ 2 * eps = 4 * Real.pi ^ 2 * G * Sc' ^ 2 := by
    apply mul_left_cancel₀ hG
    calc
      G * (kappa ^ 2 * eps) = kappa ^ 2 * G * eps := by ring
      _ = (2 * Real.pi * G) ^ 2 * Sc' ^ 2 := hke
      _ = G * (4 * Real.pi ^ 2 * G * Sc' ^ 2) := by ring
  have hmul : (2 * Real.pi * G) * (kappa ^ 2 * Sv ^ 2)
      = (2 * Real.pi * G) * (2 * Real.pi * f * Sc' ^ 2) := by
    calc
      (2 * Real.pi * G) * (kappa ^ 2 * Sv ^ 2)
          = kappa ^ 2 * (2 * Real.pi * G * Sv ^ 2) := by ring
      _ = kappa ^ 2 * (f * eps) := by rw [h1]
      _ = f * (kappa ^ 2 * eps) := by ring
      _ = f * (4 * Real.pi ^ 2 * G * Sc' ^ 2) := by rw [hke2]
      _ = (2 * Real.pi * G) * (2 * Real.pi * f * Sc' ^ 2) := by ring
  have hne : 2 * Real.pi * G ≠ 0 :=
    mul_ne_zero (mul_ne_zero (by norm_num : (2 : ℝ) ≠ 0) hpi) hG
  exact mul_left_cancel₀ hne hmul

/-- **(5)** The inversion the lane is asked for: DEMANDING saturation
    `Sigma_vac = Sigma_c` forces `kappa^2 = 2 pi f`.  With the pre-registered `f = 1`
    this is `kappa = sqrt(2 pi) = 2.5066...`, and NOT `1/2`. -/
theorem saturation_forces_kappa (G eps kappa f Sv Sc' : ℝ)
    (hG : G ≠ 0) (hpi : Real.pi ≠ 0) (hSc : Sc' ≠ 0)
    (h1 : 2 * Real.pi * G * Sv ^ 2 = f * eps)
    (h2 : 2 * Real.pi * G * Sc' = kappa * Real.sqrt (G * eps))
    (hGe : 0 ≤ G * eps) (hsat : Sv = Sc') :
    kappa ^ 2 = 2 * Real.pi * f := by
  have hm := master_ratio G eps kappa f Sv Sc' hG hpi h1 h2 hGe
  rw [hsat] at hm
  apply mul_right_cancel₀ (pow_ne_zero 2 hSc)
  calc
    kappa ^ 2 * Sc' ^ 2 = 2 * Real.pi * f * Sc' ^ 2 := hm
    _ = (2 * Real.pi * f) * Sc' ^ 2 := by ring

/-! ## 4. The circularity arm and the 8 pi -/

/-- **(6)** The record's identity `a0^2/(8 pi G) = rho c^2/(32 pi)` is EQUIVALENT to
    `kappa^2 = 1/4`, given the definition `a0 = kappa c sqrt(G rho)` (squared:
    `a0^2 = kappa^2 G rho c^2`).  Taking that identity as an input is therefore taking
    `kappa = 1/2` as an input: the "derivation" is circular.  (The factor `8 pi` in
    `32 pi = 4 x 8 pi` is Einstein's; no equation supplies it.) -/
theorem identity_iff_kappa_half (a0 G rhoL c kappa : ℝ)
    (hG : G ≠ 0) (hc : c ≠ 0) (hrho : rhoL ≠ 0)
    (ha0 : a0 ^ 2 = kappa ^ 2 * G * rhoL * c ^ 2) :
    (a0 ^ 2 / (8 * Real.pi * G) = rhoL * c ^ 2 / (32 * Real.pi)) ↔ kappa ^ 2 = (1 / 4 : ℝ) := by
  rw [ha0]
  constructor
  · intro h
    have hX : rhoL * c ^ 2 ≠ 0 := mul_ne_zero hrho (pow_ne_zero 2 hc)
    have hpi8 : (8 * Real.pi) ≠ 0 := mul_ne_zero (by norm_num : (8 : ℝ) ≠ 0) Real.pi_ne_zero
    have h1 : (kappa ^ 2 * (rhoL * c ^ 2)) / (8 * Real.pi)
        = (rhoL * c ^ 2) / (32 * Real.pi) := by
      calc
        (kappa ^ 2 * (rhoL * c ^ 2)) / (8 * Real.pi)
            = (kappa ^ 2 * G * rhoL * c ^ 2) / (8 * Real.pi * G) := by
              field_simp [hG, Real.pi_ne_zero]
        _ = rhoL * c ^ 2 / (32 * Real.pi) := h
    have hC : kappa ^ 2 * (rhoL * c ^ 2) = (rhoL * c ^ 2) / 4 := by
      calc
        kappa ^ 2 * (rhoL * c ^ 2)
            = ((rhoL * c ^ 2) / (32 * Real.pi)) * (8 * Real.pi) := (div_eq_iff hpi8).mp h1
        _ = (rhoL * c ^ 2) / 4 := by
          field_simp [Real.pi_ne_zero]
          ring
    have hD : 4 * (kappa ^ 2 * (rhoL * c ^ 2)) = (rhoL * c ^ 2) := by
      calc
        4 * (kappa ^ 2 * (rhoL * c ^ 2)) = 4 * ((rhoL * c ^ 2) / 4) := by rw [hC]
        _ = (rhoL * c ^ 2) := by ring
    have hE : (4 * kappa ^ 2 - 1) * (rhoL * c ^ 2) = 0 := by nlinarith [hD]
    have hF : 4 * kappa ^ 2 - 1 = 0 := (mul_eq_zero.mp hE).resolve_right hX
    nlinarith
  · intro hk
    have hpi8 : (8 * Real.pi) ≠ 0 := mul_ne_zero (by norm_num : (8 : ℝ) ≠ 0) Real.pi_ne_zero
    have hpi32 : (32 * Real.pi) ≠ 0 := mul_ne_zero (by norm_num : (32 : ℝ) ≠ 0) Real.pi_ne_zero
    field_simp [hG, hpi8, hpi32]
    nlinarith

/-- **(7)** `kappa = 1/2` needs `f = kappa^2/(2 pi) = 1/(8 pi)`: the vacuum's energy density
    divided by Einstein's 8 pi.  This is the input the lane names as the one that must move. -/
theorem kappa_half_requires_eight_pi (kappa : ℝ) (hk : kappa = (1 / 2 : ℝ)) :
    kappa ^ 2 / (2 * Real.pi) = 1 / (8 * Real.pi) := by
  rw [hk]
  field_simp [Real.pi_ne_zero]
  ring

/-! ## 5. The number the inversion forces -/

/-- `2 pi` is positive, so the forced value `sqrt(2 pi)` is the positive root. -/
theorem two_pi_pos : 0 < 2 * Real.pi := by positivity

/-- `sqrt(2 pi)^2 = 2 pi` (used to read `kappa = sqrt(2 pi)` off `kappa^2 = 2 pi`). -/
theorem sqrt_two_pi_sq : (Real.sqrt (2 * Real.pi)) ^ 2 = 2 * Real.pi :=
  Real.sq_sqrt (le_of_lt two_pi_pos)

/-- the forced value sits in `(2.506, 2.507)`; certified from the Mathlib pi bounds. -/
theorem two_pi_bracket : (2506 : ℝ) / 1000 < Real.sqrt (2 * Real.pi)
    ∧ Real.sqrt (2 * Real.pi) < (2507 : ℝ) / 1000 := by
  constructor
  · rw [Real.lt_sqrt (by positivity : (0 : ℝ) ≤ (2506 : ℝ) / 1000)]
    nlinarith [Real.pi_gt_d6]
  · rw [Real.sqrt_lt (by positivity : (0 : ℝ) ≤ 2 * Real.pi) (by positivity : (0 : ℝ) ≤ (2507 : ℝ) / 1000)]
    nlinarith [Real.pi_lt_d4]

/-- `kappa = 1/2` is NOT the forced value: the two squared values differ by `2 pi - 1/4 > 0`. -/
theorem half_is_not_forced : (1 / 2 : ℝ) ^ 2 ≠ 2 * Real.pi := by
  intro h
  nlinarith [Real.pi_gt_three]

end

end Final19

#print axioms Final19.jeans_beta2_term
#print axioms Final19.jeans_integrating_factor
#print axioms Final19.column_stress_identity
#print axioms Final19.column_stress_at_universal_column
#print axioms Final19.pressure_scale_def
#print axioms Final19.master_ratio
#print axioms Final19.saturation_forces_kappa
#print axioms Final19.identity_iff_kappa_half
#print axioms Final19.kappa_half_requires_eight_pi
#print axioms Final19.two_pi_pos
#print axioms Final19.sqrt_two_pi_sq
#print axioms Final19.two_pi_bracket
#print axioms Final19.half_is_not_forced
