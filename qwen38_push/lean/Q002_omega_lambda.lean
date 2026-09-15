/-
  Q002 -- THE DARK-ENERGY COINCIDENCE AS A FOOTING SELECTOR -- the Lean certificate.

  The Zimmerman scale a_0 = (c/2) sqrt(G rho_Lambda), inverted (G031 Lean:
  rho_L_from_a0: rho_Lambda = 4 a_0^2/(G c^2)) and divided by the critical
  density rho_crit = 3 H_0^2/(8 pi G), gives

      Omega_Lambda = 32 pi a_0^2 / (3 H_0^2 c^2),

  with G cancelling exactly. ONE measured number (a_0) plus H_0 fixes the
  dark-energy fraction -- this is G052's registered "Omega_Lambda = 0.6857 from
  a_0 alone", here machine-checked with certified pi bounds and exact rational
  arithmetic.

  What is certified below:
   - omega_identity     the symbolic identity (G cancels, field_simp + ring);
   - K_bounds           K := 32 a_0^2/(3 H_0^2 c^2) in (0.21827, 0.218286),
                        canonical a_0 = 9.3619e-11, H_0 = 67.36 km/s/Mpc;
   - omega_window       0.6857 < Omega < 0.6858 (using Real.pi_gt_d6, pi_lt_d4);
   - omega_in_planck    Omega strictly inside Planck 1-sigma (0.6777, 0.6917)
                        AND within 0.0011 of Planck's central 0.6847 (+0.15%);
   - alt_excluded       the empirical footing a_0 = 1.1279e-10 gives Omega > 0.99
                        -- a matter-free flat universe, cosmologically dead.

  THE SELECTION RULE (the finding): the canonical and alt a_0 footings, carried
  as equal options through the galaxy-scale lanes, are NOT cosmologically equal.
  Only the theory's own scale kappa = 1/2 (G002) survives Planck; the empirical
  1.1279e-10 is viable ONLY as a galaxy-fit value inside ~20% systematics, never
  as the fundamental scale. G052's honest alt-footing FAIL is promoted here to a
  derived two-way exclusion.

  HONEST SCOPE: the identity is conditional on H_0 (V6 in the Python lane: with
  SH0ES H_0 = 73 the a_0 window slides to 1.01e-10, still RAR-consistent -- the
  Hubble tension is absorbed, not resolved); and a_0's canonical value was itself
  derived from rho_Lambda (G002/G031), so omega_window is a consistency check of
  the whole chain, not an independent galactic prediction of Omega. The genuinely
  independent direction is the registered kill (Python V5): galactic a_0
  systematics shrinking onto the cosmological pincer value 9.36e-11 +- 0.5%.

  Constants (exact decimal literals): a_0 = 9.3619e-11 / 1.1279e-10 m/s^2 (G031);
  H_0 = 67.36 km/s/Mpc = 67.36*1000/3.085677581e22 s^-1 (Planck, G052);
  c = 299792458 m/s; Mpc = 3.085677581e22 m.
  Axioms: propext, Classical.choice, Quot.sound only. Zero sorry.
-/
import Mathlib

open Real

namespace Q002

/-! ## V1 -- the identity (G cancels) -/

/-- **omega_identity.** rho_Lambda/rho_crit = 32 pi a_0^2/(3 H_0^2 c^2) with
rho_Lambda = 4 a_0^2/(G c^2) (the Zimmerman inversion) and rho_crit =
3 H_0^2/(8 pi G). G cancels exactly; only a_0, H_0, c remain. -/
theorem omega_identity (G a0 c H0 : ℝ) (hG : G ≠ 0) (hc : c ≠ 0) (hH : H0 ≠ 0) :
    (4 * a0 ^ 2 / (G * c ^ 2)) / (3 * H0 ^ 2 / (8 * Real.pi * G))
      = 32 * Real.pi * a0 ^ 2 / (3 * H0 ^ 2 * c ^ 2) := by
  field_simp
  ring

/-! ## V2 -- the canonical K, bounded by exact rational arithmetic -/

/-- **K_bounds.** K := 32 a_0^2/(3 H_0^2 c^2) for the canonical a_0 = 9.3619e-11,
H_0 = 67.36 km/s/Mpc, c = 299792458 lies in (0.21827, 0.218286). -/
theorem K_bounds :
    (0.21827 : ℝ) < 32 * (9.3619e-11) ^ 2
        / (3 * (67.36 * 1000 / 3.085677581e22) ^ 2 * (299792458) ^ 2) ∧
    32 * (9.3619e-11) ^ 2
        / (3 * (67.36 * 1000 / 3.085677581e22) ^ 2 * (299792458) ^ 2) < (0.218286 : ℝ) := by
  constructor
  · norm_num
  · norm_num

/-! ## V3 -- the canonical Omega window -/

/-- **omega_window.** Omega_Lambda = K * pi with K in (0.21827, 0.218286) and
pi in (3.141592, 3.1416) (Mathlib-certified) lies in (0.6857, 0.6858). -/
theorem omega_window :
    (0.6857 : ℝ) < 32 * (9.3619e-11) ^ 2
        / (3 * (67.36 * 1000 / 3.085677581e22) ^ 2 * (299792458) ^ 2) * Real.pi ∧
    32 * (9.3619e-11) ^ 2
        / (3 * (67.36 * 1000 / 3.085677581e22) ^ 2 * (299792458) ^ 2) * Real.pi
      < (0.6858 : ℝ) := by
  have hK := K_bounds
  have hpi_lo : (3.141592 : ℝ) < Real.pi := Real.pi_gt_d6
  have hpi_hi : Real.pi < (3.1416 : ℝ) := Real.pi_lt_d4
  have hKpos : (0 : ℝ) < 32 * (9.3619e-11) ^ 2
      / (3 * (67.36 * 1000 / 3.085677581e22) ^ 2 * (299792458) ^ 2) := by
    linarith [hK.1]
  constructor
  · calc (0.6857 : ℝ) < 0.21827 * 3.141592 := by norm_num
      _ < 32 * (9.3619e-11) ^ 2
            / (3 * (67.36 * 1000 / 3.085677581e22) ^ 2 * (299792458) ^ 2) * Real.pi := by
        nlinarith [hK.1, hpi_lo, hKpos]
  · calc 32 * (9.3619e-11) ^ 2
            / (3 * (67.36 * 1000 / 3.085677581e22) ^ 2 * (299792458) ^ 2) * Real.pi
        < 0.218286 * 3.1416 := by nlinarith [hK.2, hpi_hi, hKpos]
      _ < (0.6858 : ℝ) := by norm_num

/-! ## V4 -- inside Planck, and the deviation bound -/

/-- **omega_in_planck.** The canonical Omega_Lambda lies strictly inside Planck's
1-sigma band (0.6777, 0.6917) = 0.6847 +- 0.007, and within 0.0011 of the central
value -- a +0.15% agreement, machine-checked. -/
theorem omega_in_planck :
    (0.6777 : ℝ) < 32 * (9.3619e-11) ^ 2
        / (3 * (67.36 * 1000 / 3.085677581e22) ^ 2 * (299792458) ^ 2) * Real.pi ∧
    32 * (9.3619e-11) ^ 2
        / (3 * (67.36 * 1000 / 3.085677581e22) ^ 2 * (299792458) ^ 2) * Real.pi
      < (0.6917 : ℝ) := by
  have hw := omega_window
  constructor
  · linarith [hw.1]
  · linarith [hw.2]

/-- **omega_near_planck_central.** |Omega - 0.6847| <= 0.0011 (the +0.15% /
+0.07%-dex agreement G052 registered), from the window (0.6857, 0.6858). -/
theorem omega_near_planck_central :
    32 * (9.3619e-11) ^ 2
        / (3 * (67.36 * 1000 / 3.085677581e22) ^ 2 * (299792458) ^ 2) * Real.pi
        - 0.6847 ≤ 0.0011 ∧
    -(0.0011 : ℝ) ≤ 32 * (9.3619e-11) ^ 2
        / (3 * (67.36 * 1000 / 3.085677581e22) ^ 2 * (299792458) ^ 2) * Real.pi
        - 0.6847 := by
  have hw := omega_window
  constructor
  · linarith [hw.2]
  · linarith [hw.1]

/-! ## V5 -- the alt footing is cosmologically excluded -/

/-- **alt_excluded.** The empirical footing a_0 = 1.1279e-10 gives
Omega_Lambda > 0.99 -- a matter-free flat universe, excluded by Planck at >40
sigma. The cosmological constant SELECTS the canonical (kappa = 1/2) footing. -/
theorem alt_excluded :
    (0.99 : ℝ) < 32 * (1.1279e-10) ^ 2
        / (3 * (67.36 * 1000 / 3.085677581e22) ^ 2 * (299792458) ^ 2) * Real.pi := by
  have hKa : (0.31682 : ℝ) < 32 * (1.1279e-10) ^ 2
      / (3 * (67.36 * 1000 / 3.085677581e22) ^ 2 * (299792458) ^ 2) := by norm_num
  have hpi : (3.141592 : ℝ) < Real.pi := Real.pi_gt_d6
  calc (0.99 : ℝ) < 0.31682 * 3.141592 := by norm_num
    _ < 32 * (1.1279e-10) ^ 2
          / (3 * (67.36 * 1000 / 3.085677581e22) ^ 2 * (299792458) ^ 2) * Real.pi := by
      nlinarith [hKa, hpi]

/-! ## The capstone -/

/-- **the_selector.** The dark-energy coincidence is a footing selector, as one
conjunction: the canonical a_0 predicts Omega_Lambda in (0.6857, 0.6858) inside
Planck's 1-sigma; the empirical a_0 is excluded (Omega > 0.99). Only kappa = 1/2
survives cosmology. -/
theorem the_selector :
    ((0.6857 : ℝ) < 32 * (9.3619e-11) ^ 2
        / (3 * (67.36 * 1000 / 3.085677581e22) ^ 2 * (299792458) ^ 2) * Real.pi ∧
     32 * (9.3619e-11) ^ 2
        / (3 * (67.36 * 1000 / 3.085677581e22) ^ 2 * (299792458) ^ 2) * Real.pi
        < (0.6858 : ℝ))
    ∧ (0.99 : ℝ) < 32 * (1.1279e-10) ^ 2
        / (3 * (67.36 * 1000 / 3.085677581e22) ^ 2 * (299792458) ^ 2) * Real.pi :=
  ⟨omega_window, alt_excluded⟩

end Q002

#print axioms Q002.omega_identity
#print axioms Q002.K_bounds
#print axioms Q002.omega_window
#print axioms Q002.omega_in_planck
#print axioms Q002.omega_near_planck_central
#print axioms Q002.alt_excluded
#print axioms Q002.the_selector
