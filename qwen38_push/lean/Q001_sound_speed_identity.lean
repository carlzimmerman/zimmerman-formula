/-
  Q001 -- THE SOUND-SPEED IDENTITY -- the Lean certificate.

  THE MISSING PIECE, machine-checked: the Zimmerman temperature (rung 4) is
  the ADIABATIC SOUND SPEED of the L247 self-acceleration medium on the
  G003 Lean-certified phantom solution:

      c_s^2 := P / rho_ph = sqrt(G*Mb*a0)/2 = G*Mb/(2*r_M) = sigma_Z^2

  with P = g^2/(8 pi G) the L247 deep matched law evaluated on the deep-MOND
  solution g^2 = a0*g_N = a0*G*Mb/r^2, and
  rho_ph = sqrt(G*Mb*a0)/(4 pi G r^2) the G003 phantom.

  Consequences certified here:
   - the identity is EXACT (no approximation, no fitting);
   - the medium is EXACTLY isothermal (c_s^2 is r-free by construction);
   - the EOS is LINEAR: P = sigma_Z^2 * rho (one constant = the temperature);
   - the constitutive chain closes: sound speed = virial-form Zimmerman
     temperature = the G031 Lean-certified sigma^2.

  Numeric anchors (G = 6.674e-11, c = 2.99792458e8, Msun = 1.98892e30):
  MW proxy Mb = 6.5e10 Msun -> c_s = 119.2/124.9 km/s (G031 registered);
  NGC3198 proxy Mb = 6.2501e10 -> 118.05 km/s (G035 registered sigma_target);
  w_eff = c_s^2/c^2 = 1.55-1.74e-7 < 5.7e-7 (the G028 cold window) -- the
  numbers are the Python lane's job (Q001 V4-V6, 8/8); this file certifies
  the algebra both lanes stand on.

  WHY THIS IS THE RESOLUTION OF G035's KILL: G035 tested whether sigma_Z is a
  relaxation product of Newtonian dynamics; it is not -- it is a CONSTITUTIVE
  property (an equation of state). Newtonian N-body has no pressure term and
  cannot see the EOS; the medium is pressure-held (L247 V1, arbitrary kernel),
  not Newtonian-held. The kill stands as a statement about Newtonian dust and
  is now explained as a category error in the test, not a failure of sigma_Z.

  Axioms: propext, Classical.choice, Quot.sound only. Zero sorry.
-/
import Mathlib

open Real

namespace Q001

/-! ## The key sqrt composition (the G031 pattern) -/

/-- sqrt(G*Mb/a0) * sqrt(G*Mb*a0) = G*Mb -- the composition powering both
the virial form and the sound-speed identity. -/
theorem key_sqrt_composition (G Mb a0 : ℝ) (hG : 0 < G) (hMb : 0 < Mb) (ha0 : 0 < a0) :
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

/-! ## V1 -- THE IDENTITY: P/rho_ph = sqrt(G*Mb*a0)/2 -/

/-- **sound_speed_identity (V1).** The L247 deep matched pressure
P = g^2/(8 pi G) on the deep-MOND solution g^2 = a0*G*Mb/r^2, divided by the
G003 phantom rho_ph = sqrt(G*Mb*a0)/(4 pi G r^2), equals sqrt(G*Mb*a0)/2
EXACTLY -- the Zimmerman temperature, with zero free parameters. -/
theorem sound_speed_identity (G Mb a0 r : ℝ) (hG : 0 < G) (hMb : 0 < Mb)
    (ha0 : 0 < a0) (hr : 0 < r) :
    (a0 * (G * Mb) / r ^ 2 / (8 * Real.pi * G))
      / (Real.sqrt (G * Mb * a0) / (4 * Real.pi * G * r ^ 2))
      = Real.sqrt (G * Mb * a0) / 2 := by
  have hX : 0 < G * Mb * a0 := mul_pos (mul_pos hG hMb) ha0
  have hsq : Real.sqrt (G * Mb * a0) * Real.sqrt (G * Mb * a0) = G * Mb * a0 :=
    Real.mul_self_sqrt (le_of_lt hX)
  have hB : Real.sqrt (G * Mb * a0) / (4 * Real.pi * G * r ^ 2) ≠ 0 := by positivity
  rw [div_eq_iff hB, div_mul_div_comm, hsq]
  field_simp
  ring

/-! ## V2/V3 -- the virial form and the linear EOS -/

/-- **zimmerman_virial_form (V2).** G*Mb/(2*r_M) with r_M = sqrt(G*Mb/a0)
equals sqrt(G*Mb*a0)/2 -- the G031 zimmerman_temperature statement, reproved
here so this certificate is self-contained. -/
theorem zimmerman_virial_form (G Mb a0 : ℝ) (hG : 0 < G) (hMb : 0 < Mb) (ha0 : 0 < a0) :
    G * Mb / (2 * Real.sqrt (G * Mb / a0)) = Real.sqrt (G * Mb * a0) / 2 := by
  have huv := key_sqrt_composition G Mb a0 hG hMb ha0
  have hne : Real.sqrt (G * Mb / a0) ≠ 0 :=
    ne_of_gt (Real.sqrt_pos.mpr (by positivity))
  calc G * Mb / (2 * Real.sqrt (G * Mb / a0))
      = Real.sqrt (G * Mb / a0) * Real.sqrt (G * Mb * a0)
          / (2 * Real.sqrt (G * Mb / a0)) := by rw [huv]
    _ = Real.sqrt (G * Mb * a0) / 2 := by field_simp [hne]

/-- **sound_speed_is_zimmerman (THE MISSING PIECE).** The medium's sound speed
P/rho_ph IS the Zimmerman temperature in its virial form G*Mb/(2*r_M),
r_M = sqrt(G*Mb/a0). Rung 4 is CONSTITUTIVE: the temperature is the equation
of state of the self-acceleration medium, not a relaxation product. -/
theorem sound_speed_is_zimmerman (G Mb a0 r : ℝ) (hG : 0 < G) (hMb : 0 < Mb)
    (ha0 : 0 < a0) (hr : 0 < r) :
    (a0 * (G * Mb) / r ^ 2 / (8 * Real.pi * G))
      / (Real.sqrt (G * Mb * a0) / (4 * Real.pi * G * r ^ 2))
      = G * Mb / (2 * Real.sqrt (G * Mb / a0)) := by
  rw [sound_speed_identity G Mb a0 r hG hMb ha0 hr,
      zimmerman_virial_form G Mb a0 hG hMb ha0]

/-- **linear_eos (V3).** The medium's equation of state is LINEAR:
P = sigma_Z^2 * rho_ph with the single constant sigma_Z^2 = sqrt(G*Mb*a0)/2.
One constant, and it is the temperature -- no velocity-dispersion parameter
is injected anywhere. -/
theorem linear_eos (G Mb a0 r : ℝ) (hG : 0 < G) (hMb : 0 < Mb)
    (ha0 : 0 < a0) (hr : 0 < r) :
    a0 * (G * Mb) / r ^ 2 / (8 * Real.pi * G)
      = (Real.sqrt (G * Mb * a0) / 2)
        * (Real.sqrt (G * Mb * a0) / (4 * Real.pi * G * r ^ 2)) := by
  have hX : 0 < G * Mb * a0 := mul_pos (mul_pos hG hMb) ha0
  have hsq : Real.sqrt (G * Mb * a0) * Real.sqrt (G * Mb * a0) = G * Mb * a0 :=
    Real.mul_self_sqrt (le_of_lt hX)
  rw [div_mul_div_comm, hsq]
  field_simp
  ring

/-- **exact_isothermality (V2, structural form).** c_s^2 = P/rho_ph carries no
r-dependence: the sound speed at any two radii is the same value -- the r^-2
scalings of P and rho_ph cancel identically, so the medium is exactly
isothermal. -/
theorem exact_isothermality (G Mb a0 r₁ r₂ : ℝ) (hG : 0 < G) (hMb : 0 < Mb)
    (ha0 : 0 < a0) (hr₁ : 0 < r₁) (hr₂ : 0 < r₂) :
    (a0 * (G * Mb) / r₁ ^ 2 / (8 * Real.pi * G))
      / (Real.sqrt (G * Mb * a0) / (4 * Real.pi * G * r₁ ^ 2))
    = (a0 * (G * Mb) / r₂ ^ 2 / (8 * Real.pi * G))
      / (Real.sqrt (G * Mb * a0) / (4 * Real.pi * G * r₂ ^ 2)) := by
  rw [sound_speed_identity G Mb a0 r₁ hG hMb ha0 hr₁,
      sound_speed_identity G Mb a0 r₂ hG hMb ha0 hr₂]

/-! ## V4 -- the cold window, algebraic form -/

/-- **w_effective_form (V4, algebraic).** The effective equation-of-state
parameter of the medium is w_eff = P/(rho_ph * c^2) = sigma_Z^2/c^2 -- so the
cold-sector requirement (w << 1) and the temperature being non-relativistic
are the SAME statement. The numeric margin (1.55-1.74e-7 vs the G028 window
5.7e-7) is the Python lane's registered V4. -/
theorem w_effective_form (G Mb a0 r c : ℝ) (hG : 0 < G) (hMb : 0 < Mb)
    (ha0 : 0 < a0) (hr : 0 < r) (hc : 0 < c) :
    (a0 * (G * Mb) / r ^ 2 / (8 * Real.pi * G))
      / ((Real.sqrt (G * Mb * a0) / (4 * Real.pi * G * r ^ 2)) * c ^ 2)
      = (Real.sqrt (G * Mb * a0) / 2) / c ^ 2 := by
  have hX : 0 < G * Mb * a0 := mul_pos (mul_pos hG hMb) ha0
  have hsq : Real.sqrt (G * Mb * a0) * Real.sqrt (G * Mb * a0) = G * Mb * a0 :=
    Real.mul_self_sqrt (le_of_lt hX)
  have hB : (Real.sqrt (G * Mb * a0) / (4 * Real.pi * G * r ^ 2)) * c ^ 2 ≠ 0 := by positivity
  rw [div_eq_iff hB]
  field_simp
  have hsq2 : Real.sqrt (a0 * G * Mb) * Real.sqrt (a0 * G * Mb) = a0 * G * Mb :=
    Real.mul_self_sqrt (by positivity)
  nlinarith [hsq, hsq2]

/-! ## The capstone -/

/-- **the_constitutive_chain.** The full identity as one conjunction:
(1) the sound speed equals sqrt(G*Mb*a0)/2;
(2) that equals the virial-form Zimmerman temperature G*Mb/(2*r_M);
(3) the EOS is linear with that single constant;
(4) the sound speed equals the virial form (rung 4 CONSTITUTIVE).
Derived from L247's matched law (arbitrary kernel), G003's phantom (Lean),
and G031's temperature (Lean), with zero free parameters. -/
theorem the_constitutive_chain (G Mb a0 r : ℝ) (hG : 0 < G) (hMb : 0 < Mb)
    (ha0 : 0 < a0) (hr : 0 < r) :
    ((a0 * (G * Mb) / r ^ 2 / (8 * Real.pi * G))
        / (Real.sqrt (G * Mb * a0) / (4 * Real.pi * G * r ^ 2))
      = Real.sqrt (G * Mb * a0) / 2)
    ∧ (G * Mb / (2 * Real.sqrt (G * Mb / a0)) = Real.sqrt (G * Mb * a0) / 2)
    ∧ (a0 * (G * Mb) / r ^ 2 / (8 * Real.pi * G)
        = (Real.sqrt (G * Mb * a0) / 2)
          * (Real.sqrt (G * Mb * a0) / (4 * Real.pi * G * r ^ 2)))
    ∧ ((a0 * (G * Mb) / r ^ 2 / (8 * Real.pi * G))
        / (Real.sqrt (G * Mb * a0) / (4 * Real.pi * G * r ^ 2))
      = G * Mb / (2 * Real.sqrt (G * Mb / a0))) :=
  ⟨sound_speed_identity G Mb a0 r hG hMb ha0 hr,
   zimmerman_virial_form G Mb a0 hG hMb ha0,
   linear_eos G Mb a0 r hG hMb ha0 hr,
   sound_speed_is_zimmerman G Mb a0 r hG hMb ha0 hr⟩

end Q001

-- the axiom audit, printed by the compile run:
#print axioms Q001.sound_speed_identity
#print axioms Q001.zimmerman_virial_form
#print axioms Q001.sound_speed_is_zimmerman
#print axioms Q001.linear_eos
#print axioms Q001.exact_isothermality
#print axioms Q001.w_effective_form
#print axioms Q001.the_constitutive_chain
