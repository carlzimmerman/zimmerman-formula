import Mathlib

/-!
# C08 -- THE THERMAL FIXED POINT (Lean certificate)

The committed decoupling/thermal bookkeeping of the equilibrium sector,
certified algebra-only in the G031/G03G/G201 spine convention (standalone,
no imports; field_simp / ring / Real.sqrt composition; the only sqrts are
closed by Real.sq_sqrt and the sqrt_pair sign-resolution technique).

THREE THEOREMS + TWO NUMERIC INSTANTIATIONS:

 1. THE FIELD IDENTITY (B05 / G233 / G151): the equilibrium temperature
        T_b = m * sigma^2 / k_B,    sigma^2 = (1/2) * sqrt(G M_b a0)
    gives the closed form
        T_b = m * sqrt(G M_b a0) / (2 k_B)          [field_identity]

 2. THE HALF-EXPONENT ELASTICITY (T_b ∝ M_b^{+1/2} at the algebra level):
        (a) the power-law read: T = (m/2k_B) * sqrt(G a0) * sqrt(M_b)
            -- T is M_b^{1/2} times an M_b-free constant   [power_law_form]
        (b) the log-log form: ln T = ln(m/2k_B) + (1/2)(ln(G a0) + ln M_b)
            -- the log-log slope is EXACTLY 1/2           [log_half_slope]
        (c) the differential form d/dM_b ln T = 1/(2 M_b), so
            d ln T / d ln M_b = 1/2 (Hadamard elasticity)  [elasticity_half]

 3. THE FLUCTUATION SCALE (B05 / the N^{-1/2} algebra): with
        N := M_b / m,   deltaT/T = N^{-1/2}  (heat-capacity floor),
    the rms temperature fluctuation is
        deltaT_rms = sqrt(G m^3 a0) / (2 k_B)
    -- INDEPENDENT of M_b (scale-invariant at fixed m, a0):
    T ~ a0 r_M and N ~ r_M^2 cancel.  Lean carries:
        N^{-1/2} = sqrt(m/M_b)                       [n_inv_half]
        T_b * sqrt(m/M_b) = sqrt(G m^3 a0)/(2 k_B)   [fluct_closed_form]
        deltaT/T = N^{-1/2}, N = M_b/m  =>  deltaT = sqrt(G m^3 a0)/(2 k_B)
                                                     [fluct_scale]

NUMERICS (committed constants, B05):
        deltaT_rms = 2.4732.. e-36 K  (2.4732201374593863e-36, B05)
                    in (2.4732e-36, 2.4733e-36)     [num_dT_rms_interval]
        T_b (canonical M_b = 7.0e10 M_sun) = 9.689.. K  in (9.68, 9.70)
                                                     [num_Tb_canon_interval]
  Both are certified on the SQUARED algebra (deltaT = sqrt(...)/(2k_B)
  iff (2 k_B deltaT)^2 = G m^3 a0; T_b = m/2 sqrt(G M_b a0)/k_B iff
  (2 k_B T_b / m)^2 = G M_b a0) -- norm_num-closable exact rational
  arithmetic, no sqrt, the G036/G058 interval technique.

Zero sorry.  Axioms: {propext, Classical.choice, Quot.sound} only.
Physics provenance: project_atomos/B05_dark_gas.py + B05_results.json
(the heat-capacity floor, deltaT_rms = sqrt(G m^3 a0)/(2 k_B) =
2.4732201374593863e-36 K, scale-invariant), B08_condensate.py (the
gapless Goldstone branch omega(k) = c_s k, T_b untouched),
G084_maxentropy_law.py (the entropy / the isothermal profile).
-/

noncomputable section

-- ============================================================
-- 1. THE FIELD IDENTITY:  T_b = m sigma^2/k_B, sigma^2 = (1/2) sqrt(G M_b a0)
--    =>  T_b = m sqrt(G M_b a0) / (2 k_B)
-- ============================================================

theorem field_identity (m kB G Mb a0 sigma2 : ℝ)
    (hsigma : sigma2 = (1 / 2) * Real.sqrt (G * Mb * a0)) (hkB : kB ≠ 0) :
    m * sigma2 / kB = m * Real.sqrt (G * Mb * a0) / (2 * kB) := by
  rw [hsigma]
  field_simp [hkB]

-- ============================================================
-- 2. THE HALF-EXPONENT ELASTICITY  (T_b ∝ M_b^{+1/2})
-- ============================================================

-- 2a. the power-law read: T = (m/2k_B) * sqrt(G a0) * sqrt(M_b) -- the
--     M_b-dependence is EXACTLY sqrt(M_b) = M_b^{1/2} (the constant
--     (m/2k_B)*sqrt(G a0) is M_b-free)
theorem power_law_form (m kB G a0 Mb : ℝ) (hG : 0 ≤ G) (ha0 : 0 ≤ a0)
    (_hMb : 0 ≤ Mb) (_hkB0 : (2 : ℝ) * kB ≠ 0) :
    m * Real.sqrt (G * Mb * a0) / (2 * kB) = (m / (2 * kB)) * Real.sqrt (G * a0) * Real.sqrt Mb := by
  have hga : 0 ≤ G * a0 := by positivity
  have hreb : G * Mb * a0 = (G * a0) * Mb := by ring
  have hsplit : Real.sqrt (G * Mb * a0) = Real.sqrt (G * a0) * Real.sqrt Mb := by
    calc Real.sqrt (G * Mb * a0) = Real.sqrt ((G * a0) * Mb) := by rw [hreb]
      _ = Real.sqrt (G * a0) * Real.sqrt Mb := Real.sqrt_mul hga Mb
  calc m * Real.sqrt (G * Mb * a0) / (2 * kB) = (m / (2 * kB)) * Real.sqrt (G * Mb * a0) := by
        field_simp
      _ = (m / (2 * kB)) * (Real.sqrt (G * a0) * Real.sqrt Mb) := by rw [hsplit]
      _ = (m / (2 * kB)) * Real.sqrt (G * a0) * Real.sqrt Mb := by ring

-- 2b. the log-log form: ln T = ln(m/2k_B) + (1/2)(ln(G a0) + ln M_b) --
--     the log-log slope in ln M_b is EXACTLY 1/2 (algebra level)
theorem log_half_slope (m kB G a0 Mb : ℝ) (hm : 0 < m) (hkB : 0 < kB)
    (hG : 0 < G) (ha0 : 0 < a0) (hMb : 0 < Mb) :
    Real.log (m * Real.sqrt (G * Mb * a0) / (2 * kB))
      = Real.log (m / (2 * kB)) + (1 / 2) * (Real.log (G * a0) + Real.log Mb) := by
  have hy0 : Real.sqrt (G * Mb * a0) ≠ 0 :=
    ne_of_gt (Real.sqrt_pos.mpr (by positivity : 0 < G * Mb * a0))
  have hc0 : m / (2 * kB) ≠ 0 := by positivity
  have hlogy : Real.log (Real.sqrt (G * Mb * a0)) = (1 / 2) * Real.log (G * Mb * a0) := by
    have h2 : 2 * Real.log (Real.sqrt (G * Mb * a0)) = Real.log (G * Mb * a0) := by
      calc 2 * Real.log (Real.sqrt (G * Mb * a0))
          = Real.log ((Real.sqrt (G * Mb * a0)) ^ 2) := (Real.log_pow (Real.sqrt (G * Mb * a0)) 2).symm
        _ = Real.log (G * Mb * a0) := by rw [Real.sq_sqrt (by positivity : (0 : ℝ) ≤ G * Mb * a0)]
    nlinarith
  have hreb : G * Mb * a0 = (G * a0) * Mb := by ring
  have hga0 : G * a0 ≠ 0 := by positivity
  have hsplit : Real.log (G * Mb * a0) = Real.log (G * a0) + Real.log Mb := by
    calc Real.log (G * Mb * a0) = Real.log ((G * a0) * Mb) := by rw [hreb]
      _ = Real.log (G * a0) + Real.log Mb := Real.log_mul hga0 (ne_of_gt hMb)
  have hreorder : Real.log (Real.sqrt (G * Mb * a0)) + Real.log (m / (2 * kB))
      = Real.log (m / (2 * kB)) + (1 / 2) * Real.log (G * Mb * a0) := by
    rw [hlogy]
    ring
  calc Real.log (m * Real.sqrt (G * Mb * a0) / (2 * kB))
      = Real.log ((Real.sqrt (G * Mb * a0)) * (m / (2 * kB))) := by
          congr
          ring
    _ = Real.log (Real.sqrt (G * Mb * a0)) + Real.log (m / (2 * kB)) := Real.log_mul hy0 hc0
    _ = Real.log (m / (2 * kB)) + (1 / 2) * Real.log (G * Mb * a0) := hreorder
    _ = Real.log (m / (2 * kB)) + (1 / 2) * (Real.log (G * a0) + Real.log Mb) := by
          rw [hsplit]

-- 2c. the differential form:  d/dM_b ln T = 1/(2 M_b), so
--     d ln T / d ln M_b = M_b * (1/(2 M_b)) = 1/2  (the literal elasticity)
theorem elasticity_half (m kB G a0 : ℝ) (hm : 0 < m) (hkB : 0 < kB)
    (hG : 0 < G) (ha0 : 0 < a0) :
    ∀ M > 0, HasDerivAt (fun x : ℝ => Real.log (m * Real.sqrt (G * x * a0) / (2 * kB)))
      (1 / (2 * M)) M := by
  intro M hM
  have hinner : HasDerivAt (fun x : ℝ => G * x * a0) (G * a0) M := by
    have h1 : HasDerivAt (fun x : ℝ => x * a0) (1 * a0) M := (hasDerivAt_id M).mul_const a0
    have h2 : HasDerivAt (fun x : ℝ => G * (x * a0)) (G * (1 * a0)) M := h1.const_mul G
    convert h2 using 1
    · funext x; ring
    · ring
  have hinner_pos : 0 < G * M * a0 := by positivity
  have hsqrt : HasDerivAt (fun x : ℝ => Real.sqrt (G * x * a0))
      ((1 / (2 * Real.sqrt (G * M * a0))) * (G * a0)) M := by
    have hfun : (fun x : ℝ => Real.sqrt (G * x * a0)) =
        ((fun x : ℝ => Real.sqrt x) ∘ fun x : ℝ => G * x * a0) := by
      funext x
      rfl
    rw [hfun]
    exact (Real.hasDerivAt_sqrt (ne_of_gt hinner_pos)).comp M hinner
  have hg : HasDerivAt (fun x : ℝ => m * Real.sqrt (G * x * a0) / (2 * kB))
      ((m * ((1 / (2 * Real.sqrt (G * M * a0))) * (G * a0))) / (2 * kB)) M :=
    (hsqrt.const_mul m).div_const (2 * kB)
  have hfne : m * Real.sqrt (G * M * a0) / (2 * kB) ≠ 0 := by positivity
  have hlogf := hg.log hfne
  have hval : ((m * ((1 / (2 * Real.sqrt (G * M * a0))) * (G * a0))) / (2 * kB)) /
      (m * Real.sqrt (G * M * a0) / (2 * kB)) = 1 / (2 * M) := by
    have hsn : Real.sqrt (G * M * a0) ≠ 0 := ne_of_gt (Real.sqrt_pos.mpr hinner_pos)
    have hm0 : m ≠ 0 := ne_of_gt hm
    have hkB0 : (2 : ℝ) * kB ≠ 0 := by positivity
    field_simp [hsn, hm0, hkB0]
    nlinarith [Real.sq_sqrt (by positivity : (0 : ℝ) ≤ G * M * a0)]
  rw [hval] at hlogf
  exact hlogf

-- ============================================================
-- 3. THE FLUCTUATION SCALE  (the N^{-1/2} algebra)
-- ============================================================

-- 3a. N := M_b/m  =>  N^{-1/2} = sqrt(m/M_b)  (the heat-capacity floor
--     deltaT/T = N^{-1/2} evaluated at N = M_b/m)
theorem n_inv_half (m Mb N : ℝ) (hm : 0 < m) (hMb : 0 < Mb) (hN : N = Mb / m) :
    N ^ (-(1 / 2 : ℝ)) = Real.sqrt (m / Mb) := by
  have hNnonneg : (0 : ℝ) ≤ N := le_of_lt (by rw [hN]; positivity)
  have hhalf : N ^ (1 / 2 : ℝ) = Real.sqrt N := by
    have hsqpow : (N ^ (1 / 2 : ℝ)) * (N ^ (1 / 2 : ℝ)) = N := by
      rw [← Real.rpow_add (by rw [hN]; positivity : 0 < N) (1 / 2 : ℝ) (1 / 2 : ℝ)]
      have hsum : (1 / 2 : ℝ) + (1 / 2 : ℝ) = (1 : ℝ) := by norm_num
      rw [hsum, Real.rpow_one]
    have hsquare : (N ^ (1 / 2 : ℝ)) ^ (2 : ℕ) = N := by
      rw [pow_two]
      exact hsqpow
    have hsq : (N ^ (1 / 2 : ℝ)) ^ (2 : ℕ) = (Real.sqrt N) ^ (2 : ℕ) := by
      rw [hsquare, Real.sq_sqrt hNnonneg]
    have hor := eq_or_eq_neg_of_sq_eq_sq (N ^ (1 / 2 : ℝ)) (Real.sqrt N) hsq
    rcases hor with h | h
    · exact h
    · have hnn : (0 : ℝ) ≤ N ^ (1 / 2 : ℝ) := Real.rpow_nonneg hNnonneg (1 / 2 : ℝ)
      have hsn : (0 : ℝ) ≤ Real.sqrt N := Real.sqrt_nonneg _
      nlinarith
  have hsmul : Real.sqrt (Mb / m) * Real.sqrt (m / Mb) = 1 := by
    rw [← Real.sqrt_mul (by positivity : (0 : ℝ) ≤ Mb / m) (m / Mb)]
    have hc : (Mb / m) * (m / Mb) = 1 := by field_simp [ne_of_gt hMb, ne_of_gt hm]
    rw [hc]
    norm_num
  have hinv : (Real.sqrt (Mb / m))⁻¹ = Real.sqrt (m / Mb) := by
    field_simp [ne_of_gt (Real.sqrt_pos.mpr (by positivity : 0 < Mb / m))]
    exact hsmul.symm
  calc
    N ^ (-(1 / 2 : ℝ)) = (N ^ (1 / 2 : ℝ))⁻¹ := by rw [Real.rpow_neg hNnonneg]
    _ = (Real.sqrt N)⁻¹ := by rw [hhalf]
    _ = (Real.sqrt (Mb / m))⁻¹ := by rw [hN]
    _ = Real.sqrt (m / Mb) := hinv

-- 3b. T_b * N^{-1/2} = T_b * sqrt(m/M_b) = sqrt(G m^3 a0)/(2 k_B)
--     (N = M_b/m): the closed form of the fluctuation scale
theorem fluct_closed_form (m kB G a0 Mb : ℝ) (hm : 0 < m) (hkB : 0 < kB)
    (hG : 0 < G) (ha0 : 0 < a0) (hMb : 0 < Mb) (_hkB0 : (2 : ℝ) * kB ≠ 0) :
    (m * Real.sqrt (G * Mb * a0) / (2 * kB)) * Real.sqrt (m / Mb)
      = Real.sqrt (G * m ^ 3 * a0) / (2 * kB) := by
  have hprod : Real.sqrt (G * Mb * a0) * Real.sqrt (m / Mb) = Real.sqrt (G * m * a0) := by
    rw [← Real.sqrt_mul (by positivity : (0 : ℝ) ≤ G * Mb * a0) (m / Mb)]
    have hcancel : (G * Mb * a0) * (m / Mb) = G * m * a0 := by
      field_simp [ne_of_gt hMb]
    rw [hcancel]
  have hm2 : m * Real.sqrt (G * m * a0) = Real.sqrt (G * m ^ 3 * a0) := by
    have hms : Real.sqrt (m ^ 2) = m := by
      rw [Real.sqrt_sq_eq_abs]
      exact abs_of_nonneg (le_of_lt hm)
    have hpower : m ^ 2 * (G * m * a0) = G * m ^ 3 * a0 := by ring
    calc m * Real.sqrt (G * m * a0)
        = Real.sqrt (m ^ 2) * Real.sqrt (G * m * a0) := by rw [hms]
      _ = Real.sqrt (m ^ 2 * (G * m * a0)) := by
          rw [Real.sqrt_mul (by positivity : (0 : ℝ) ≤ m ^ 2) (G * m * a0)]
      _ = Real.sqrt (G * m ^ 3 * a0) := by rw [hpower]
  calc (m * Real.sqrt (G * Mb * a0) / (2 * kB)) * Real.sqrt (m / Mb)
      = (m * (Real.sqrt (G * Mb * a0) * Real.sqrt (m / Mb))) / (2 * kB) := by
          field_simp
    _ = (m * Real.sqrt (G * m * a0)) / (2 * kB) := by rw [hprod]
    _ = Real.sqrt (G * m ^ 3 * a0) / (2 * kB) := by rw [hm2]

-- 3c. THE FULL CHAIN: from N = M_b/m and deltaT/T = N^{-1/2} the rms
--     fluctuation is deltaT_rms = sqrt(G m^3 a0)/(2 k_B), scale-invariant
theorem fluct_scale (m kB G a0 Mb dT : ℝ) (hm : 0 < m) (hkB : 0 < kB)
    (hG : 0 < G) (ha0 : 0 < a0) (hMb : 0 < Mb) (hkB0 : (2 : ℝ) * kB ≠ 0)
    (hrel : dT / (m * Real.sqrt (G * Mb * a0) / (2 * kB)) = (Mb / m) ^ (-(1 / 2 : ℝ))) :
    dT = Real.sqrt (G * m ^ 3 * a0) / (2 * kB) := by
  have hNH : (Mb / m) ^ (-(1 / 2 : ℝ)) = Real.sqrt (m / Mb) := by
    exact n_inv_half m Mb (Mb / m) hm hMb rfl
  have hT0 : m * Real.sqrt (G * Mb * a0) / (2 * kB) ≠ 0 := by positivity
  calc dT
      = (m * Real.sqrt (G * Mb * a0) / (2 * kB)) * (dT / (m * Real.sqrt (G * Mb * a0) / (2 * kB))) := by
          field_simp [hT0]
    _ = (m * Real.sqrt (G * Mb * a0) / (2 * kB)) * Real.sqrt (m / Mb) := by
          rw [hNH] at hrel
          rw [hrel]
    _ = Real.sqrt (G * m ^ 3 * a0) / (2 * kB) :=
          fluct_closed_form m kB G a0 Mb hm hkB hG ha0 hMb hkB0

-- ============================================================
-- 4. THE NUMERICS (committed constants, B05) -- certified on the
--    SQUARED algebra (G036/G058 interval technique, exact rationals)
-- ============================================================

-- deltaT_rms = sqrt(G m^3 a0)/(2 k_B);  the squared bound:
-- (2 k_B lo)^2 < G m^3 a0 < (2 k_B hi)^2  =>  deltaT in (2.4732, 2.4733) e-36 K
theorem num_dT_rms_interval :
    (2 * (1.380649e-23 : ℝ) * (2.4732e-36 : ℝ)) ^ 2 <
        (6.674e-11 : ℝ) * ((5088.6 * (1.602176634e-19 : ℝ) / (2.99792458e8 : ℝ) ^ 2) ^ 3) *
          (9.3619e-11 : ℝ) ∧
      (6.674e-11 : ℝ) * ((5088.6 * (1.602176634e-19 : ℝ) / (2.99792458e8 : ℝ) ^ 2) ^ 3) *
          (9.3619e-11 : ℝ) < (2 * (1.380649e-23 : ℝ) * (2.4733e-36 : ℝ)) ^ 2 := by
  norm_num

-- T_b(canonical) = m * (1/2) sqrt(G M_b a0)/k_B;  the squared bound:
-- (2 k_B T/m)^2 = G M_b a0  =>  T_b in (9.68, 9.70) K
theorem num_Tb_canon_interval :
    (2 * (1.380649e-23 : ℝ) * (9.68 : ℝ) /
        ((5088.6 * (1.602176634e-19 : ℝ) / (2.99792458e8 : ℝ) ^ 2))) ^ 2 <
        (6.674e-11 : ℝ) * (7.0e10 * 1.98892e30) * (9.3619e-11 : ℝ) ∧
      (6.674e-11 : ℝ) * (7.0e10 * 1.98892e30) * (9.3619e-11 : ℝ) <
        (2 * (1.380649e-23 : ℝ) * (9.70 : ℝ) /
          ((5088.6 * (1.602176634e-19 : ℝ) / (2.99792458e8 : ℝ) ^ 2))) ^ 2 := by
  norm_num

-- ============================================================
-- AXIOM AUDIT
-- ============================================================
#print axioms field_identity
#print axioms power_law_form
#print axioms log_half_slope
#print axioms elasticity_half
#print axioms n_inv_half
#print axioms fluct_closed_form
#print axioms fluct_scale
#print axioms num_dT_rms_interval
#print axioms num_Tb_canon_interval
