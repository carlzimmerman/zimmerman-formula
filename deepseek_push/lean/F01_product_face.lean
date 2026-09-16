import Mathlib

/-!
# F01 -- THE PRODUCT FACE: the a0-cancellation identity m x T_X-ray = mu m_p T_0(1+z*)
# EXACTLY (Lean certificate)

E03 (`deepseek_push/E03_unification_map.py` + `E03_results.json`, 23/23 PASS)
reads the framework's unification as ONE scale a0 entering THREE faces, the
coupling route being the shared velocity square

    sigma^2 = (1/2) sqrt(G M_b a0)

which feeds the temperature law (the proton rung, B6/A02, certified C04)

    T_X-ray = mu m_p sigma^2 / k_B                                  (Face T)

and the mass ladder (A05/G163, certified C05/C02)

    m = k_B T_0 (1+z*) / sigma^2                                    (Face P).

THE PRODUCT FACE is their product: the SAME sigma^2 enters the numerator of
one face and the denominator of the other, so it cancels ALGEBRAICALLY, and
k_B cancels against itself:

    m x T_X-ray = (k_B T_0(1+z*) / sigma^2) x (mu m_p sigma^2 / k_B)
                = mu m_p T_0 (1+z*)   EXACTLY

-- the product carries NO sigma^2, NO a0, NO M_b, NO G: the scale that
couples both faces disappears from the product (E03's product fingerprint,
MW anchor closure 1.000000 at sigma = 119.21 km/s, m = 5.0503 keV,
T = 1.0330e6 K).

This file certifies, in the G03G spine convention (standalone theorems, no
imports; field_simp/ring at battlefield strength on abstract positive reals;
every square root closed by the sqrt_pair sign-resolution -- square both
sides, resolve the sign with nonnegativity, no rpow, no NNReal coercion):

  0. field_identity         : THE FIELD IDENTITY -- (a/sigma^2)(b sigma^2)
                              = a b for sigma != 0: the two faces' shared
                              factor cancels in the product, unconditionally.
  1. product_identity       : THE PHYSICS FORM -- with m := k_B T0z/sigma^2
                              and T := mu m_p sigma^2/k_B (the SAME sigma^2),
                              m x T = mu m_p T0z: the k_B AND sigma^2
                              cancellations in one stroke (T0z := T_0(1+z*)).
  2. product_face_exact     : the E03 statement verbatim -- the product
                              (k_B T_0(1+z*)/sigma^2)(mu m_p sigma^2/k_B)
                              = mu m_p T_0(1+z*) EXACTLY (z* carried through
                              as a factor, nothing dropped).
  3. product_a0_chain       : the chained form with sigma^2 = (1/2) sqrt(G M_b a0):
                              m x T = mu m_p T0z even with the square root
                              substituted -- the a0-root cancels against
                              itself (the C04/C05 sqrt content, closed here).
  4. product_sigma_independent : THE COROLLARY at the sigma^2 level -- the
                              product function is CONSTANT in sigma^2:
                              m(sigma1) x T(sigma1) = m(sigma2) x T(sigma2)
                              for any two admissible sigma^2.
  5. product_a0_independent  : THE a0-INDEPENDENCE (the task's corollary) --
                              m(a0) x T(a0) = m(a0') x T(a0') for any two
                              scales: the scale cancels COMPLETELY, the
                              product is a0-free by construction.
  6. product_ratio_closes   : the ratio form of the anchor -- m x T /
                              (mu m_p T0z) = 1 exactly (the 1.000000 that
                              the MW anchor measures at float precision).

SCOPE (what this certificate does and does not claim): Lean certifies the
ALGEBRA -- that, granted the premises T = mu m_p sigma^2/k_B (B6, C04) and
m = k_B T_0(1+z*)/sigma^2 (A05/G163, C02), the product is exactly
mu m_p T_0(1+z*) and carries no scale.  It does NOT certify the physics-law
readings -- that sigma^2 = (1/2) sqrt(G M_b a0) is the framework's shared
velocity square, that mu m_p is the baryonic rung's SM unit, or the decimal
numerics (119.21 km/s, 5.0503 keV, 1.0330e6 K, ratio 1.000000) -- those live
in the E03/A05/B06/deepseek_push Python lanes.  All variables are abstract
positive reals at battlefield strength: no units, no constants' values.

Zero sorry.  Axioms expected: {propext, Classical.choice, Quot.sound}.
-/

noncomputable section

-- ============================================================
-- 0. THE FIELD IDENTITY: (a/sigma^2)(b sigma^2) = a b for sigma != 0.
--    The shared factor entering BOTH faces cancels in the product,
--    unconditionally (no positivity needed, only sigma^2 != 0).
-- ============================================================
theorem field_identity (a b sg : ℝ) (hsg : sg ≠ 0) :
    (a / sg) * (b * sg) = a * b := by
  field_simp [hsg]

-- ============================================================
-- 1. THE PHYSICS FORM: m := k_B T0z/sigma^2, T := mu m_p sigma^2/k_B
--    (the SAME sigma^2) => m x T = mu m_p T0z -- the k_B and sigma^2
--    cancellations in one stroke (T0z := T_0(1+z*), the ladder's rung)
-- ============================================================
theorem product_identity (kB T0z mup sg : ℝ) (hkB : 0 < kB) (hsg : sg ≠ 0) :
    let m := kB * T0z / sg
    let T := mup * sg / kB
    m * T = mup * T0z := by
  intro m T
  dsimp [m, T]
  field_simp [ne_of_gt hkB, hsg]

-- ============================================================
-- 2. THE E03 STATEMENT VERBATIM: with T0z := T_0(1+z*) spelled out,
--    (k_B T_0(1+z*)/sigma^2)(mu m_p sigma^2/k_B) = mu m_p T_0(1+z*)
--    EXACTLY -- the z* factor is carried through, nothing dropped
-- ============================================================
theorem product_face_exact (kB T0 zstar mup sg : ℝ) (hkB : 0 < kB) (hsg : sg ≠ 0) :
    let T0z := T0 * (1 + zstar)
    let m := kB * T0z / sg
    let T := mup * sg / kB
    m * T = mup * T0z := by
  intro T0z m T
  dsimp [m, T, T0z]
  field_simp [ne_of_gt hkB, hsg]

-- ============================================================
-- 3. THE CHAINED FORM: sigma^2 := (1/2) sqrt(G M_b a0) substituted into
--    BOTH faces -- m x T = mu m_p T0z even with the square root present:
--    the a0-root (and the virial's 1/2) cancel against themselves
--    (the sqrt content of the C04/C05 lane, closed here in the product)
-- ============================================================
theorem product_a0_chain (kB T0z mup G Mb a0 : ℝ) (hkB : 0 < kB) (hG : 0 < G)
    (hMb : 0 < Mb) (ha0 : 0 < a0) :
    let sg2 := (1 / 2 : ℝ) * Real.sqrt (G * Mb * a0)
    let m := kB * T0z / sg2
    let T := mup * sg2 / kB
    m * T = mup * T0z := by
  intro sg2 m T
  dsimp [m, T, sg2]
  have hsq : (1 / 2 : ℝ) * Real.sqrt (G * Mb * a0) ≠ 0 := by positivity
  field_simp [ne_of_gt hkB, hsq]

-- ============================================================
-- 4. THE COROLLARY AT THE SIGMA^2 LEVEL: the product function is CONSTANT
--    in sigma^2 -- m(sigma1) x T(sigma1) = m(sigma2) x T(sigma2) for any
--    two admissible sigma^2 (the scale of both faces cancels completely)
-- ============================================================
theorem product_sigma_independent (kB T0z mup sg1 sg2 : ℝ) (hkB : 0 < kB)
    (hsg1 : sg1 ≠ 0) (hsg2 : sg2 ≠ 0) :
    let m1 := kB * T0z / sg1
    let T1 := mup * sg1 / kB
    let m2 := kB * T0z / sg2
    let T2 := mup * sg2 / kB
    m1 * T1 = m2 * T2 := by
  intro m1 T1 m2 T2
  dsimp [m1, T1, m2, T2]
  have h1 : (kB * T0z / sg1) * (mup * sg1 / kB) = mup * T0z := by
    field_simp [ne_of_gt hkB, hsg1]
  have h2 : (kB * T0z / sg2) * (mup * sg2 / kB) = mup * T0z := by
    field_simp [ne_of_gt hkB, hsg2]
  rw [h1, h2]

-- ============================================================
-- 5. THE a0-INDEPENDENCE (the task's corollary): m(a0) x T(a0) =
--    m(a0') x T(a0') for ANY two scales a0, a0' -- the scale cancels
--    COMPLETELY, the product carries no a0, no M_b, no G by construction
-- ============================================================
theorem product_a0_independent (kB T0z mup G Mb a0 a0' : ℝ) (hkB : 0 < kB)
    (hG : 0 < G) (hMb : 0 < Mb) (ha0 : 0 < a0) (ha0' : 0 < a0') :
    let sg2 := (1 / 2 : ℝ) * Real.sqrt (G * Mb * a0)
    let sg2' := (1 / 2 : ℝ) * Real.sqrt (G * Mb * a0')
    let m1 := kB * T0z / sg2
    let T1 := mup * sg2 / kB
    let m2 := kB * T0z / sg2'
    let T2 := mup * sg2' / kB
    m1 * T1 = m2 * T2 := by
  intro sg2 sg2' m1 T1 m2 T2
  dsimp [m1, T1, m2, T2, sg2, sg2']
  have h1 : (kB * T0z / ((1 / 2 : ℝ) * Real.sqrt (G * Mb * a0))) *
      (mup * ((1 / 2 : ℝ) * Real.sqrt (G * Mb * a0)) / kB) = mup * T0z := by
    have hsq : (1 / 2 : ℝ) * Real.sqrt (G * Mb * a0) ≠ 0 := by positivity
    field_simp [ne_of_gt hkB, hsq]
  have h2 : (kB * T0z / ((1 / 2 : ℝ) * Real.sqrt (G * Mb * a0'))) *
      (mup * ((1 / 2 : ℝ) * Real.sqrt (G * Mb * a0')) / kB) = mup * T0z := by
    have hsq' : (1 / 2 : ℝ) * Real.sqrt (G * Mb * a0') ≠ 0 := by positivity
    field_simp [ne_of_gt hkB, hsq']
  rw [h1, h2]

-- ============================================================
-- 6. THE RATIO FORM OF THE ANCHOR: m x T / (mu m_p T0z) = 1 EXACTLY
--    (the 1.000000 the MW anchor registers at float precision)
-- ============================================================
theorem product_ratio_closes (kB T0z mup sg : ℝ) (hkB : 0 < kB) (hmup : 0 < mup)
    (hT0z : 0 < T0z) (hsg : sg ≠ 0) :
    let m := kB * T0z / sg
    let T := mup * sg / kB
    (m * T) / (mup * T0z) = 1 := by
  intro m T
  dsimp [m, T]
  have hprod : (kB * T0z / sg) * (mup * sg / kB) = mup * T0z := by
    field_simp [ne_of_gt hkB, hsg]
  rw [hprod]
  field_simp [ne_of_gt hmup, (show T0z ≠ 0 by exact ne_of_gt hT0z)]

end

#print axioms field_identity
#print axioms product_identity
#print axioms product_face_exact
#print axioms product_a0_chain
#print axioms product_sigma_independent
#print axioms product_a0_independent
#print axioms product_ratio_closes