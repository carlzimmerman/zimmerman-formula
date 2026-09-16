import Mathlib

/-!
# C03 -- THE LINE KINEMATICS + THE ABEL CUSP (Lean certificate)

C-wave certificate for the B01/B02 particle-face targets:

  (1) THE LINE KINEMATICS (B01): E = m/2 EXACTLY and the Doppler width
      identity sigma_E/E = sigma_v/c -- the field-level factorization
      sigma_E = E * (sigma_v/c).  With the committed registers
      m = 5.0886 keV, E = 2.5443 keV, sigma_d = 140.2 km/s,
      c = 2.99792458e5 km/s:
        sigma_E = 1.18986 eV  in (1.18, 1.20) eV   [num_sigmaE_eV]
        delta-E/E = 4.6766e-4 in (4.67e-4, 4.68e-4) [num_deltaE_over_E]
      -- numerically closed by pure rational arithmetic, no analysis.

  (2) THE ABEL CUSP (B02): the projected column of the phantom density
      rho = A/r^2 is Sigma_p(b) = pi A/b -- the b^-1 cusp.  Its core is
      the half-line Abel integral
        Int_0^t  1/(b^2+s^2) ds = arctan(t/b)/b      [substitution]
        Int_0^oo 1/(b^2+s^2) ds = pi/(2b)  (b > 0)   [pi/2 evaluation]
      certified at the level the house patterns allow: the SUBSTITUTION
      IDENTITY (arctan_substitution_identity, closed by FTC with the
      derivative of arctan(s/b)/b) plus the PI/2 EVALUATION
      (arctan_pi_over_two: arctan(t/b) -> pi/2 as t -> oo), assembled
      into the Abel column as a limit (abel_column_half_line) and the
      full-LOS cusp algebra (sigma_cusp_full_los: 2*(pi/(2b))*A = pi*A/b).
      The r_break-capped B02 column (A/b)*2*arctan(L/b) is the finite-L
      instance (capped_column_closed_form).  The numeric register
      (MW, b = 1 kpc): pi*A/b = 3.4501954412545 in (3.450, 3.451)
      [num_sigma_phantom_MW, pi-interval arithmetic a la G083].

THREE-STRIKE DISCIPLINE (deepseek_moa/lean README): any theorem not
closed in 3 attempts is dropped with the exact Mathlib blocker named in
a comment and registered PENDING in C03_results.json.  This file carries
only theorems that CLOSED; see the JSON for the strike ledger.

Zero sorry.  Axioms: {propext, Classical.choice, Quot.sound} only.
-/

noncomputable section

open Filter

-- ============================================================
-- PART 1 -- THE LINE KINEMATICS
-- ============================================================

/-- **E = m/2 exactly** (B01/1.1, A05 register): the line energy is half
the species mass, bidirectionally. -/
theorem line_energy_is_half (m E : ℝ) : E = m / 2 ↔ m = 2 * E := by
  constructor
  · intro h
    rw [h]
    ring
  · intro h
    rw [h]
    ring

-- the same identity in the divided form, no side conditions
theorem line_energy_divided (m E : ℝ) (hm : m ≠ 0) (h : E = m / 2) :
    E / m = 1 / 2 := by
  rw [h]
  field_simp [hm]

/-- **The Doppler width identity, field-level factorization** (B01/1.2):
sigma_E = E * sigma_v / c  ==>  sigma_E / E = sigma_v / c, the exact
factorization sigma_E = E * (sigma_v / c). -/
theorem doppler_width_identity (E sigmaE sigmav c : ℝ) (hE : E ≠ 0) (hc : c ≠ 0)
    (h : sigmaE = E * sigmav / c) : sigmaE / E = sigmav / c := by
  rw [h]
  field_simp [hE, hc]

/-- **The factorization itself**: sigma_E = E * sigma_v / c  ==
sigma_E = E * (sigma_v / c) -- the width factors into the line energy
times the (c-free) velocity fraction. -/
theorem doppler_width_factorized (E sigmaE sigmav c : ℝ)
    (h : sigmaE = E * sigmav / c) : sigmaE = E * (sigmav / c) := by
  rw [h]
  ring

-- ------------------------------------------------------------
-- the committed registers as pure rational arithmetic (B01 C2)
-- ------------------------------------------------------------

/-- E = m/2 = 2.5443 keV for m = 5.0886 keV, exact. -/
theorem num_E_line_keV : (5.0886 : ℝ) / 2 = 2.5443 := by
  norm_num

/-- sigma_E = E * sigma_d / c = 1.18986 eV at E = 2.5443 keV,
sigma_d = 140.2 km/s, c = 2.99792458e5 km/s: in (1.18, 1.20) eV. -/
theorem num_sigmaE_eV :
    (1.18 : ℝ) < 2.5443e3 * 140.2 / 2.99792458e5 ∧
      2.5443e3 * 140.2 / 2.99792458e5 < (1.20 : ℝ) := by
  norm_num

/-- delta-E/E = sigma_d/c = 4.6766e-4: in (4.67e-4, 4.68e-4). -/
theorem num_deltaE_over_E :
    (4.67e-4 : ℝ) < 140.2 / 2.99792458e5 ∧
      140.2 / 2.99792458e5 < (4.68e-4 : ℝ) := by
  norm_num

-- ============================================================
-- PART 2 -- THE ABEL CUSP: Int_0^oo 1/(b^2+s^2) ds = pi/(2b)
-- ============================================================

/-- **The substitution identity** (B02's arctan identity): for b > 0,
Int_0^t 1/(b^2+s^2) ds = arctan(t/b)/b -- the antiderivative of
s |-> 1/(b^2+s^2) is arctan(s/b)/b (FTC, no substitution machinery,
the derivative closed by field algebra). -/
theorem arctan_substitution_identity (b : ℝ) (hb : 0 < b) :
    (∀ t : ℝ, ∫ (s : ℝ) in (0)..t, 1 / (b ^ 2 + s ^ 2) = Real.arctan (t / b) / b) := by
  intro t
  -- hderiv: the derivative of F(s) := arctan(s/b)/b is 1/(b^2+s^2)
  have hderiv : ∀ x : ℝ,
      HasDerivAt (fun y : ℝ => Real.arctan (y / b) / b) (1 / (b ^ 2 + x ^ 2)) x := by
    intro x
    have hlin : HasDerivAt (fun y : ℝ => y / b) (1 / b) x := by
      simpa using (hasDerivAt_id x).div_const b
    have hcomp : HasDerivAt (fun y : ℝ => Real.arctan (y / b))
        (1 / (1 + (x / b) ^ 2) * (1 / b)) x := by
      simpa [Function.comp_def] using (Real.hasDerivAt_arctan (x / b)).comp x hlin
    have hdiv : HasDerivAt (fun y : ℝ => Real.arctan (y / b) / b)
        (1 / (1 + (x / b) ^ 2) * (1 / b) / b) x := by
      simpa using hcomp.div_const b
    have hval : 1 / (1 + (x / b) ^ 2) * (1 / b) / b = 1 / (b ^ 2 + x ^ 2) := by
      field_simp [hb.ne']
    rwa [hval] at hdiv
  let F : ℝ → ℝ := fun y : ℝ => Real.arctan (y / b) / b
  have hderivF : ∀ y : ℝ, deriv F y = 1 / (b ^ 2 + y ^ 2) := by
    intro y
    simpa [F] using (hderiv y).deriv
  have hdiff : ∀ x ∈ Set.uIcc 0 t, DifferentiableAt ℝ F x := by
    intro x hx
    simpa [F] using (hderiv x).differentiableAt
  have hint : IntervalIntegrable (deriv F) MeasureTheory.volume 0 t := by
    have hcont : Continuous (fun x : ℝ => 1 / (b ^ 2 + x ^ 2)) := by
      have hc1 : Continuous (fun x : ℝ => b ^ 2 + x ^ 2) :=
        (continuous_const : Continuous (fun _ : ℝ => b ^ 2)).add (continuous_id.pow 2)
      have hne : ∀ x : ℝ, b ^ 2 + x ^ 2 ≠ 0 := by
        intro x
        nlinarith [sq_nonneg x, sq_pos_of_pos hb]
      exact (continuous_const : Continuous (fun _ : ℝ => (1 : ℝ))).div hc1 hne
    rw [show deriv F = fun x : ℝ => 1 / (b ^ 2 + x ^ 2) from by
      funext x
      exact hderivF x]
    exact ContinuousOn.intervalIntegrable hcont.continuousOn
  have hsub := intervalIntegral.integral_deriv_eq_sub (a := 0) (b := t) (f := F) hdiff hint
  have hcongr : (∫ (s : ℝ) in (0)..t, 1 / (b ^ 2 + s ^ 2)) =
      ∫ (y : ℝ) in (0)..t, deriv F y := by
    apply intervalIntegral.integral_congr
    intro y hy
    rw [hderivF y]
  rw [hcongr, hsub]
  dsimp [F]
  have h0 : Real.arctan (0 / b) = 0 := by
    rw [zero_div, Real.arctan_zero]
  rw [h0, zero_div]
  ring

/-- **The pi/2 evaluation** (B02's L -> oo step): for b > 0,
arctan(t/b) -> pi/2 as t -> oo -- the arctan limit, composed with
t/b -> oo. -/
theorem arctan_pi_over_two (b : ℝ) (hb : 0 < b) :
    Filter.Tendsto (fun t : ℝ => Real.arctan (t / b)) Filter.atTop (nhds (Real.pi / 2)) := by
  have hdiv : Filter.Tendsto (fun t : ℝ => t / b) Filter.atTop Filter.atTop := by
    exact (Filter.Tendsto.atTop_div_const (r := b) hb
      (Filter.tendsto_id : Filter.Tendsto id Filter.atTop Filter.atTop))
  have hc : Filter.Tendsto (fun t : ℝ => Real.arctan (t / b)) Filter.atTop
      (nhdsWithin (Real.pi / 2) (Set.Iio (Real.pi / 2))) := by
    simpa [Function.comp_def] using (Real.tendsto_arctan_atTop.comp hdiv)
  exact hc.mono_right nhdsWithin_le_nhds

/-- **THE ABEL COLUMN** (B02, the phantom's 1/b cusp): for b > 0,
Int_0^oo 1/(b^2+s^2) ds = pi/(2b) -- the substitution identity with the
pi/2 evaluation, taken as the limit of the finite integrals. -/
theorem abel_column_half_line (b : ℝ) (hb : 0 < b) :
    Filter.Tendsto (fun t : ℝ => ∫ (s : ℝ) in (0)..t, 1 / (b ^ 2 + s ^ 2)) Filter.atTop
      (nhds (Real.pi / (2 * b))) := by
  have hsub := arctan_substitution_identity b hb
  have h2 : Filter.Tendsto (fun t : ℝ => Real.arctan (t / b) / b) Filter.atTop
      (nhds (Real.pi / (2 * b))) := by
    have hv : (Real.pi / 2) / b = Real.pi / (2 * b) := by
      field_simp [hb.ne']
    simpa [hv] using (arctan_pi_over_two b hb).div_const b
  rw [show (fun t : ℝ => ∫ (s : ℝ) in (0)..t, 1 / (b ^ 2 + s ^ 2)) =
      fun t : ℝ => Real.arctan (t / b) / b by
    funext t
    exact hsub t]
  exact h2

/-- **The full-LOS cusp algebra**: the full line of sight is twice the
half line, so Sigma_p(b) = A * (2 * (pi/(2b))) = pi * A / b -- the B02
1/b cusp (C1). -/
theorem sigma_cusp_full_los (A b : ℝ) (hb : b ≠ 0) :
    (2 * (Real.pi / (2 * b))) * A = Real.pi * A / b := by
  have h2b : 2 * b ≠ 0 := mul_ne_zero (by norm_num : (2 : ℝ) ≠ 0) hb
  field_simp [hb, h2b]

/-- **The r_break-capped column** (B02's finite object, C1's closed
form): the physical halo cut gives Sigma_p(b) = 2A * Int_0^L
1/(b^2+s^2) ds = (2A/b) arctan(L/b), L = sqrt(r_break^2 - b^2) --
the substitution identity instantiated at the finite L. -/
theorem capped_column_closed_form (A b L : ℝ) (hb : 0 < b) :
    (2 * A) * (∫ (s : ℝ) in (0)..L, 1 / (b ^ 2 + s ^ 2)) =
      2 * A / b * Real.arctan (L / b) := by
  have hsub := arctan_substitution_identity b hb L
  rw [hsub]
  field_simp [hb.ne']

-- ------------------------------------------------------------
-- the MW register: pi*A/b at b = 1 kpc (pi-interval arithmetic,
-- G083 style: Real.pi_gt_d6 / Real.pi_lt_d4 bound every comparison)
-- ------------------------------------------------------------

/-- **The MW column register** (B02 C1): with A = 3.388787757915661e19
kg/m (phantom amplitude at the MW, G072) and b = 1 kpc =
3.0856775814913673e19 m, the full-LOS phantom column
Sigma_p(b) = pi*A/b = 3.4501954412545 sits strictly in (3.450, 3.451)
-- pure pi-interval arithmetic, no analysis. -/
theorem num_sigma_phantom_MW :
    (3.450 : ℝ) < Real.pi * 3.388787757915661e19 / 3.0856775814913673e19 ∧
      Real.pi * 3.388787757915661e19 / 3.0856775814913673e19 < (3.451 : ℝ) := by
  have hden : (0 : ℝ) < 3.0856775814913673e19 := by norm_num
  have hA : (0 : ℝ) < 3.388787757915661e19 := by norm_num
  constructor
  · rw [lt_div_iff₀ hden]
    calc (3.450 : ℝ) * 3.0856775814913673e19
        < 3.141592 * 3.388787757915661e19 := by norm_num
      _ ≤ Real.pi * 3.388787757915661e19 :=
          mul_le_mul_of_nonneg_right Real.pi_gt_d6.le hA.le
  · rw [div_lt_iff₀ hden]
    calc Real.pi * 3.388787757915661e19
        < 3.1416 * 3.388787757915661e19 :=
          mul_lt_mul_of_pos_right Real.pi_lt_d4 hA
      _ < (3.451 : ℝ) * 3.0856775814913673e19 := by norm_num

-- ============================================================
-- axioms ledger
-- ============================================================
#print axioms line_energy_is_half
#print axioms line_energy_divided
#print axioms doppler_width_identity
#print axioms doppler_width_factorized
#print axioms num_E_line_keV
#print axioms num_sigmaE_eV
#print axioms num_deltaE_over_E
#print axioms arctan_substitution_identity
#print axioms arctan_pi_over_two
#print axioms abel_column_half_line
#print axioms sigma_cusp_full_los
#print axioms capped_column_closed_form
#print axioms num_sigma_phantom_MW