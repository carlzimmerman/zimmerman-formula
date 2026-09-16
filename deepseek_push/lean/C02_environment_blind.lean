/-
  C02 -- ENVIRONMENT-BLINDNESS: the ladder and the freeze map are algebraic
  inverses; the mass is a fixed point of the ladder, independent of the
  environment (sigma, z*).   (Agent: C-series -- WAVE 30 / B03 companion.)

  PHYSICS (committed elsewhere: B03, G213, G212, G151 -- read, not re-derived
  here).
    THE LADDER (the particle face, A06/A08/G151): an environment whose
    equilibrium froze at redshift z* with velocity dispersion sigma recovers
    the particle mass
        m_rec = k_B T_0 (1+z*) / sigma^2 .
    THE FREEZE MAP (G213/G194): the equilibrium temperature T_b = m sigma^2/k_B
    equals the CMB temperature at freeze, T_CMB(z*) = T_0 (1+z*), so the
    freeze epoch is
        (1+z*) = m sigma^2 / (k_B T_0) .
    ENVIRONMENT-BLINDNESS (B03 V1): substitute the freeze relation into the
    ladder and the environment cancels identically:
        m_rec = (k_B T_0 / sigma^2) * (m sigma^2 / (k_B T_0)) = m
    for ANY sigma > 0 and ANY z* realizable by the map -- the mass is a
    FIXED POINT of the ladder.  With a = sigma^2, b = m, c = k_B T_0 the
    certified statement is the positive-reals field identity
        (a*b/c) * (c/a) = b   for a, b, c > 0.

  WHAT IS CERTIFIED (pure algebra -- no physics, no units, and NO z* >= -1
  domain statement: the domain question belongs to G213 and is deliberately
  NOT attempted here):
    T1  posreal_field_identity        -- (a*b/c)*(c/a) = b for a,b,c > 0
    T2  environment_blindness         -- ladder sigma^2 (freeze sigma^2 m) = m
    T3  recovered_mass_sigma_independent -- m_rec identical for any two sigmas
    T4  zstar_function_of_sigma_only  -- (1+z*) is a bijective function of
                                        sigma alone (freeze s1 = freeze s2
                                        <-> s1 = s2, m and k_B T_0 fixed)
    T5  recovered_mass_within_1e12    -- |m_rec - m| <= 1e-12 for ANY (m, sigma)
                                        (exact identity: the difference is 0)

  NO sorry.  Axioms: propext, Classical.choice, Quot.sound (the Mathlib
  baseline) -- printed at the foot of this file.
-/

import Mathlib
import Mathlib.Tactic

noncomputable section

namespace C02

/-! ## 0. The master identity: the positive-reals field identity -/

/-- THE POSITIVE-REALS FIELD IDENTITY: (a*b/c) * (c/a) = b for positive
    a, b, c.  With a = sigma^2, b = m, c = k_B T_0 this is exactly the
    statement that substituting the freeze relation into the ladder returns
    the mass identically -- the fixed point of the ladder, in one line. -/
theorem posreal_field_identity (a b c : ℝ) (ha : 0 < a) (hb : 0 < b) (hc : 0 < c) :
    (a * b / c) * (c / a) = b := by
  field_simp [ne_of_gt ha, ne_of_gt hc]

/-- The same identity under the weaker, purely algebraic hypothesis that the
    divisors are nonzero (used by the instantiated corollaries). -/
theorem field_identity_nonzero (a b c : ℝ) (ha : a ≠ 0) (hc : c ≠ 0) :
    (a * b / c) * (c / a) = b := by
  field_simp [ha, hc]

/-! ## 1. The physics instantiation: ladder and freeze map -/

/-- THE LADDER: m_rec = k_B T_0 (1+z*) / sigma^2.
    Arguments: sigma2 = sigma^2, kBT0 = k_B T_0, fz = 1+z*. -/
def ladder (sigma2 kBT0 fz : ℝ) : ℝ := kBT0 * fz / sigma2

/-- THE FREEZE MAP: (1+z*) = m sigma^2 / (k_B T_0).
    Arguments: sigma2 = sigma^2, m = the particle mass, kBT0 = k_B T_0. -/
def freeze (sigma2 m kBT0 : ℝ) : ℝ := m * sigma2 / kBT0

/-- ENVIRONMENT-BLINDNESS (B03 V1): the mass is a FIXED POINT of the ladder.
    For ANY velocity dispersion sigma (sigma2 = sigma^2 != 0) and ANY
    k_B T_0 != 0,
        ladder sigma^2 (freeze sigma^2 m) = m
    identically: the environment (sigma, z*) cancels out of the recovery. -/
theorem environment_blindness (sigma2 m kBT0 : ℝ) (hs : sigma2 ≠ 0) (hk : kBT0 ≠ 0) :
    ladder sigma2 kBT0 (freeze sigma2 m kBT0) = m := by
  unfold ladder freeze
  field_simp [hs, hk]

/-- The same fixed-point statement on the positive-reals footing (sigma^2 > 0,
    k_B T_0 > 0), as stated in the brief. -/
theorem environment_blindness_pos (sigma2 m kBT0 : ℝ) (hs : 0 < sigma2) (hk : 0 < kBT0) :
    ladder sigma2 kBT0 (freeze sigma2 m kBT0) = m :=
  environment_blindness sigma2 m kBT0 (ne_of_gt hs) (ne_of_gt hk)

/-! ## 2. Corollary 1: the recovered mass is sigma-independent -/

/-- The recovered mass does not depend on the environment's dispersion: two
    DIFFERENT environments (sigma1, z*1) and (sigma2, z*2), each frozen via
    the map, recover the SAME mass.  This is B03's multi-rung result in one
    line: one mass from every environment that froze. -/
theorem recovered_mass_sigma_independent (m kBT0 : ℝ) (hk : kBT0 ≠ 0)
    (s1 s2 : ℝ) (hs1 : s1 ≠ 0) (hs2 : s2 ≠ 0) :
    ladder s1 kBT0 (freeze s1 m kBT0) = ladder s2 kBT0 (freeze s2 m kBT0) := by
  rw [environment_blindness s1 m kBT0 hs1 hk,
      environment_blindness s2 m kBT0 hs2 hk]

/-! ## 3. Corollary 2: z* is a function of the environment only via sigma -/

/-- The freeze epoch (1+z*) is a BIJECTIVE function of sigma alone (for fixed
    m and k_B T_0): two environments share the same freeze epoch IFF they have
    the same dispersion -- no environment variable other than sigma enters.
    (The map's domain statement z* >= -1 is G213's, NOT certified here.) -/
theorem zstar_function_of_sigma_only (m kBT0 : ℝ) (hm : m ≠ 0) (hk : kBT0 ≠ 0)
    (s1 s2 : ℝ) :
    freeze s1 m kBT0 = freeze s2 m kBT0 ↔ s1 = s2 := by
  unfold freeze
  constructor
  · intro h
    have hmm : m * s1 = m * s2 := by
      calc
        m * s1 = (m * s1 / kBT0) * kBT0 := by field_simp [hk]
        _ = (m * s2 / kBT0) * kBT0 := by rw [h]
        _ = m * s2 := by field_simp [hk]
    exact mul_left_cancel₀ hm hmm
  · intro h
    rw [h]

/-! ## 4. Corollary 3: the numeric cross-check (1e-12) -/

/-- NUMERIC CROSS-CHECK: the recovered mass equals the input mass to 1e-12 for
    ANY (m, sigma).  The identity is exact, so the difference is exactly 0,
    hence comfortably within 1e-12. -/
theorem recovered_mass_within_1e12 (sigma2 m kBT0 : ℝ) (hs : sigma2 ≠ 0) (hk : kBT0 ≠ 0) :
    |ladder sigma2 kBT0 (freeze sigma2 m kBT0) - m| ≤ (1e-12 : ℝ) := by
  have h := environment_blindness sigma2 m kBT0 hs hk
  rw [h]
  norm_num

/-! ## 5. The conjoined statement: what B03 certifies -/

/-- ENVIRONMENT-BLINDNESS, conjoined: the ladder's fixed point, the
    sigma-independence of the recovered mass, and the z*-via-sigma-only
    bijection, in a single theorem. -/
theorem environment_blindness_statement (m kBT0 : ℝ) (hk : kBT0 ≠ 0) (hm : m ≠ 0) :
    (∀ s : ℝ, s ≠ 0 → ladder s kBT0 (freeze s m kBT0) = m) ∧
    (∀ s1 s2 : ℝ, s1 ≠ 0 → s2 ≠ 0 →
      ladder s1 kBT0 (freeze s1 m kBT0) = ladder s2 kBT0 (freeze s2 m kBT0)) ∧
    (∀ s1 s2 : ℝ, freeze s1 m kBT0 = freeze s2 m kBT0 ↔ s1 = s2) := by
  constructor
  · intro s hs
    exact environment_blindness s m kBT0 hs hk
  constructor
  · intro s1 s2 hs1 hs2
    exact recovered_mass_sigma_independent m kBT0 hk s1 s2 hs1 hs2
  · intro s1 s2
    exact zstar_function_of_sigma_only m kBT0 hm hk s1 s2

#print axioms posreal_field_identity
#print axioms field_identity_nonzero
#print axioms environment_blindness
#print axioms environment_blindness_pos
#print axioms recovered_mass_sigma_independent
#print axioms zstar_function_of_sigma_only
#print axioms recovered_mass_within_1e12
#print axioms environment_blindness_statement

end C02