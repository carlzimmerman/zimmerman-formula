/-
  Q003 -- THE AMPLITUDE LAW -- the Lean certificate (H021's law, machine-checked).

  THE LAST OPEN ITEM (Requirement 10) is now a theorem chain.
  hy4's H021 closed it computationally (5/5); this file certifies the
  DERIVED part -- every identity is exact, no fitting, no approximation.

  Constants (G031/G003 Lean-certified):
      S    = sqrt(G * Mb * a0)       the equilibrium scale
      r_M  = sqrt(G * Mb / a0)       the MOND radius
      rho  = S / (4 pi G r^2)        the G003 phantom (coefficient 1)
      M(r) = int_0^r 4 pi t^2 rho(t) dt

  Proven below (all exact):
   1. sqrt_composition   sqrt(GM/a0) * sqrt(GM a0) = GM
   2. enclosed_mass      M(r) = S r / G
   3. amplitude_law      M(r)/Mb = r / r_M                  (H021 A1)
   4. phantom_at_rM      M(r_M) = Mb                        (coefficient 1)
   5. cap_ratio          M(r_cap)/Mb = a0/g_ext             (H021 A2,
                     for r_cap = S/g_ext, i.e. g_int(r_cap) = g_ext)
   6. numeric_window     1849/10000 < 1/(5408/1000) < 1851/10000
                     and 1/10 < 1/(5408/1000) < 1
                     (the implied <g_ext> = 0.185 a0, inside the 2MRS range)

  Honest scope (H021 A5): the LAW (the ratios) is proven; the environmental
  input <g_ext> is the measured quantity, exactly as the halo mass function
  is in LCDM.  Axioms: {propext, Classical.choice, Quot.sound}. Zero sorry.
-/
import Mathlib

open Real
open intervalIntegral

noncomputable section

namespace Q003

def r_M (G Mb a0 : ℝ) : ℝ := Real.sqrt (G * Mb / a0)
def rho_ph (S G r : ℝ) : ℝ := S / (4 * Real.pi * G * r ^ 2)
def M_ph (S G r : ℝ) : ℝ := ∫ t in (0:ℝ)..r, 4 * Real.pi * t ^ 2 * rho_ph S G t

/-! ## The key sqrt composition (the G031 pattern) -/

/-- sqrt(G*Mb/a0) * sqrt(G*Mb*a0) = G*Mb -- pure sqrt composition. -/
theorem sqrt_composition (G Mb a0 : ℝ) (hG : 0 < G) (hMb : 0 < Mb) (ha0 : 0 < a0) :
    Real.sqrt (G * Mb / a0) * Real.sqrt (G * Mb * a0) = G * Mb := by
  have hx : 0 ≤ G * Mb / a0 := by positivity
  have hprod : (G * Mb / a0) * (G * Mb * a0) = (G * Mb) * (G * Mb) := by
    field_simp
  calc Real.sqrt (G * Mb / a0) * Real.sqrt (G * Mb * a0)
      = Real.sqrt ((G * Mb / a0) * (G * Mb * a0)) := (Real.sqrt_mul hx _).symm
    _ = Real.sqrt ((G * Mb) * (G * Mb)) := by rw [hprod]
    _ = G * Mb := by
      have hGM : 0 ≤ G * Mb := by positivity
      exact Real.sqrt_mul_self hGM

/-! ## The enclosed mass (the G031 integral pattern) -/

/-- The shell integrand is the constant S/G (a.e.), pointwise for t != 0. -/
theorem integrand_const (S G t : ℝ) (hG : 0 < G) (ht : t ≠ 0) :
    4 * Real.pi * t ^ 2 * (S / (4 * Real.pi * G * t ^ 2)) = S / G := by
  field_simp [ht, Real.pi_ne_zero, hG.ne]

/-- M(r) = S r / G: the isothermal sphere's linear mass profile. -/
theorem enclosed_mass (G Mb a0 S r : ℝ) (hG : 0 < G) (hMb : 0 < Mb) (ha0 : 0 < a0)
    (hS : S = Real.sqrt (G * Mb * a0)) (hr : 0 < r) :
    M_ph S G r = S * r / G := by
  change ∫ (t : ℝ) in (0)..r, 4 * Real.pi * t ^ 2 * (S / (4 * Real.pi * G * t ^ 2)) = S * r / G
  have h0 : ∫ (t : ℝ) in (0)..r, 4 * Real.pi * t ^ 2 * (S / (4 * Real.pi * G * t ^ 2))
      = ∫ (t : ℝ) in (0)..r, (S / G) :=
    intervalIntegral.integral_congr_ae (μ := MeasureTheory.volume)
      (by rw [Set.uIoc_of_le hr.le]; filter_upwards with t ht;
          exact integrand_const S G t hG (ne_of_gt ht.1))
  rw [h0, intervalIntegral.integral_const, sub_zero, smul_eq_mul]
  field_simp [hG.ne]

/-! ## The amplitude law (H021 A1) -/

/-- M(r)/Mb = r / r_M -- the DERIVED amplitude law. -/
theorem amplitude_law (G Mb a0 S r : ℝ) (hG : 0 < G) (hMb : 0 < Mb) (ha0 : 0 < a0)
    (hS : S = Real.sqrt (G * Mb * a0)) (hr : 0 < r) :
    M_ph S G r / Mb = r / r_M G Mb a0 := by
  rw [enclosed_mass G Mb a0 S r hG hMb ha0 hS hr, hS, r_M]
  have hcomp : Real.sqrt (G * Mb * a0) * Real.sqrt (G * Mb / a0) = G * Mb := by
    rw [mul_comm]
    exact sqrt_composition G Mb a0 hG hMb ha0
  have hpos : 0 < Real.sqrt (G * Mb / a0) := Real.sqrt_pos.mpr (by positivity)
  have hq : Real.sqrt (G * Mb * a0) / (G * Mb) = 1 / Real.sqrt (G * Mb / a0) := by
    field_simp [hcomp, hpos.ne]
    simpa [mul_comm] using hcomp
  calc Real.sqrt (G * Mb * a0) * r / G / Mb
      = r * (Real.sqrt (G * Mb * a0) / (G * Mb)) := by
        field_simp [hG.ne, hMb.ne]
    _ = r * (1 / Real.sqrt (G * Mb / a0)) := by
        rw [hq]
    _ = r / Real.sqrt (G * Mb / a0) := by
        field_simp

/-! ## Coefficient one (H021 A1, the r = r_M case) -/

/-- M(r_M) = Mb: at the MOND radius the phantom's enclosed mass equals the
    baryon mass, coefficient exactly one. -/
theorem phantom_at_rM (G Mb a0 S : ℝ) (hG : 0 < G) (hMb : 0 < Mb) (ha0 : 0 < a0)
    (hS : S = Real.sqrt (G * Mb * a0)) :
    M_ph S G (r_M G Mb a0) = Mb := by
  have hr : 0 < r_M G Mb a0 := Real.sqrt_pos.mpr (by positivity)
  rw [enclosed_mass G Mb a0 S (r_M G Mb a0) hG hMb ha0 hS hr, hS, r_M]
  have hcomp : Real.sqrt (G * Mb * a0) * Real.sqrt (G * Mb / a0) = G * Mb := by
    rw [mul_comm]
    exact sqrt_composition G Mb a0 hG hMb ha0
  rw [hcomp]
  field_simp [hG.ne]

/-! ## The cap (H021 A2) -/

/-- g_int(r) = S/r, so the cap r_cap = S/g_ext satisfies g_int(r_cap) = g_ext. -/
theorem cap_is_gext (G Mb a0 S g_ext : ℝ) (hG : 0 < G) (hMb : 0 < Mb) (ha0 : 0 < a0)
    (hS : S = Real.sqrt (G * Mb * a0)) (hge : 0 < g_ext) :
    S / (S / g_ext) = g_ext := by
  have hSpos : 0 < S := by
    rw [hS]; exact Real.sqrt_pos.mpr (by positivity)
  field_simp [hge.ne, hSpos.ne]

/-- M(r_cap)/Mb = a0/g_ext for r_cap = S/g_ext: the external-field truncation
    of the amplitude law.  Exact ratio identity. -/
theorem cap_ratio (G Mb a0 S g_ext : ℝ) (hG : 0 < G) (hMb : 0 < Mb) (ha0 : 0 < a0)
    (hS : S = Real.sqrt (G * Mb * a0)) (hge : 0 < g_ext) :
    M_ph S G (S / g_ext) / Mb = a0 / g_ext := by
  have hSpos : 0 < S := by
    rw [hS]; exact Real.sqrt_pos.mpr (by positivity)
  have hr : 0 < S / g_ext := by positivity
  rw [enclosed_mass G Mb a0 S (S / g_ext) hG hMb ha0 hS hr, hS]
  have hs : Real.sqrt (G * Mb * a0) ^ 2 = G * Mb * a0 :=
    Real.sq_sqrt (by positivity)
  calc Real.sqrt (G * Mb * a0) * (Real.sqrt (G * Mb * a0) / g_ext) / G / Mb
      = (Real.sqrt (G * Mb * a0) ^ 2) / (g_ext * G * Mb) := by
        field_simp [hG.ne, hMb.ne, hge.ne]
    _ = (G * Mb * a0) / (g_ext * G * Mb) := by
        rw [hs]
    _ = a0 / g_ext := by
        field_simp [hG.ne, hMb.ne, hge.ne]

/-! ## The cosmic amplitude number (H021 A3/A4) -/

/-- The measured ratio Omega_dm/Omega_b = 5.408 implies <g_ext> = a0/5.408,
    in (0.1849 a0, 0.1851 a0).  Rational interval, exact. -/
theorem numeric_window :
    1849 / 10000 < (1 / (5408 / 1000 : ℝ)) ∧ (1 / (5408 / 1000 : ℝ)) < 1851 / 10000 := by
  constructor <;> norm_num

/-- The implied mean external field sits inside the 2MRS range (0.1, 1) a0. -/
theorem numeric_in_2mrs_range :
    1 / 10 < (1 / (5408 / 1000 : ℝ)) ∧ (1 / (5408 / 1000 : ℝ)) < 1 := by
  constructor <;> norm_num

/-! ## THE SPINE -/

/-- The amplitude law's whole content in one theorem: the ratio law,
    coefficient one at r_M, the cap, and the cosmic number. -/
theorem the_amplitude_spine (G Mb a0 S r g_ext : ℝ)
    (hG : 0 < G) (hMb : 0 < Mb) (ha0 : 0 < a0)
    (hS : S = Real.sqrt (G * Mb * a0)) (hr : 0 < r) (hge : 0 < g_ext) :
    (M_ph S G r / Mb = r / r_M G Mb a0) ∧
    (M_ph S G (r_M G Mb a0) = Mb) ∧
    (M_ph S G (S / g_ext) / Mb = a0 / g_ext) ∧
    (1849 / 10000 < (1 / (5408 / 1000 : ℝ)) ∧ (1 / (5408 / 1000 : ℝ)) < 1851 / 10000) := by
  refine ⟨?_, phantom_at_rM G Mb a0 S hG hMb ha0 hS,
    cap_ratio G Mb a0 S g_ext hG hMb ha0 hS hge, ?_⟩
  · exact amplitude_law G Mb a0 S r hG hMb ha0 hS hr
  · exact numeric_window

end Q003

#print axioms Q003.the_amplitude_spine
#print axioms Q003.enclosed_mass
#print axioms Q003.amplitude_law
#print axioms Q003.phantom_at_rM
#print axioms Q003.cap_ratio
#print axioms Q003.numeric_window
#print axioms Q003.sqrt_composition
