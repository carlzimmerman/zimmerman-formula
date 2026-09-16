import Mathlib

/-!
# C04 -- THE PROTON RUNG: the T_X-ray law, its algebraic inverse, and the
# (mu m_p) mass-ratio invariance (Lean certificate)

Theorem set for the proton-rung lane (project_atomos/A02_proton_rung.py +
B06_txray_law.py, 13/13 + 14/14 PASS), in the G03G/G201 spine convention
(each certificate standalone, no imports; every sqrt closed by the
sqrt_pair sign-resolution technique -- square both sides, resolve the sign
with nonnegativity, no rpow, no NNReal coercion):

  0. field_identity     : THE FIELD IDENTITY (A02/B06).  The virial
     k_B T = mu m_p sigma^2 with sigma^2 = (1/2) sqrt(G M_b a0) (G091,
     kappa = 1/2, G03G) closes to the zero-parameter law
     T_X-ray = mu m_p sqrt(G M_b a0)/(2 k_B) -- one cancellation of the
     virial's 2 against the sqrt's 1/2.
  1. mass_free_ratio    : the virial's mass-free content: from the field
     identity, k_B T/(mu m_p) = sqrt(G M_b a0)/2 -- the ratio the inverse
     estimator inverts (G084: T/m = sigma^2/k_B is mass-free).
  2. inversion_identity : THE INVERSE (B06 Part 2).  With
     M_impl := 4 (k_B T/(mu m_p))^2/(G a0), substituting the law's T for a
     mass M returns M exactly: M_impl(T(M)) = M -- the estimator is the
     algebraic inverse of the temperature law on the positive axis.
  3. inversion_dual     : the mirror round trip: T(M_impl(T)) = T -- the
     pair (T, M_impl) is a mutual inversion (the SZ-class thermometer the
     framework owns, B06 V2).
  4. mass_ratio_invariant : THE COROLLARY (A02 V3/B06 error budget).  The
     estimator depends only on the mass-free ratio k_B T/(mu m_p):
     rescaling the baryonic rung scale and the temperature together
     (T -> lam*T, mu m_p -> lam*(mu m_p)) leaves M_impl EXACTLY invariant
     (mu's [-0.007, +0.014] dex band on T x mu^-2 on M of B06 Part 3 is
     this identity read through the mu sweep).
  5. proton_rung_ratio  : the rung form of the same invariance (A02 V2a,
     G151 A3): at EQUAL sigma, T_phase/T_bary = m/(mu m_p) -- the
     temperature ratio is the mass ratio, c/a = mu m_p/m = 1.126e5
     exactly; only the RATIO m/(mu m_p) enters, so the law is invariant
     under the joint (m, mu m_p) scale.

Zero sorry.  Axioms: {propext, Classical.choice, Quot.sound} only.
Theorems: 6.  Physics provenance: project_atomos/A02_proton_rung.py
(V0b: the 12 committed clusters imply ONE a0 = 9.36193e-11 to machine
precision; V1a: the identity-form rung at median 3.633 keV = 0.560 of
observed; V2a: c/a = 112587 registered 1.126e5; m/m_p = 5.32921e-06 vs
SM 5.32895e-06, ratio 1.00005) and project_atomos/B06_txray_law.py
(within-sample log10 residual MAD = 0.0530 dex at the G109 0.062-dex
benchmark, n = 50; inverse estimator precision 0.10-0.36 dex = 2x the
T scatter).
-/


-- ============================================================
-- 0. THE FIELD IDENTITY: k_B T = mu m_p sigma^2, sigma^2 = (1/2) sqrt(G M_b a0)
--    =>  T = mu m_p sqrt(G M_b a0)/(2 k_B)
-- ============================================================

-- the virial closes to the law: substitute sigma^2, divide by k_B > 0
theorem field_identity (kB T mup sq2 G Mb a0 : ℝ) (hkB : 0 < kB)
    (hmup : 0 < mup) (hvir : kB * T = mup * sq2)
    (hsq : sq2 = Real.sqrt (G * Mb * a0) / 2) :
    T = mup * Real.sqrt (G * Mb * a0) / (2 * kB) := by
  have hkB0 : kB ≠ 0 := ne_of_gt hkB
  have hT : T = mup * sq2 / kB := by
    calc T = (kB * T) / kB := by field_simp [hkB0]
    _ = (mup * sq2) / kB := by rw [hvir]
  rw [hT, hsq]
  field_simp [hkB0, ne_of_gt hmup]

-- the mass-free ratio: k_B T/(mu m_p) = sqrt(G M_b a0)/2 (the virial's
-- velocity scale read off the temperature -- G084's mass-free T/m)
theorem mass_free_ratio (kB T mup G Mb a0 : ℝ) (hkB : 0 < kB)
    (hmup : 0 < mup) (hT : T = mup * Real.sqrt (G * Mb * a0) / (2 * kB)) :
    kB * T / mup = Real.sqrt (G * Mb * a0) / 2 := by
  rw [hT]
  field_simp [ne_of_gt hkB, ne_of_gt hmup]


-- ============================================================
-- 2. THE ALGEBRAIC INVERSE: M_impl := 4 (k_B T/(mu m_p))^2/(G a0)
--    substitutes the law's T and returns the mass: M_impl(T(M)) = M
-- ============================================================

theorem inversion_identity (kB T mup G Mb a0 : ℝ) (hkB : 0 < kB)
    (hmup : 0 < mup) (hG : 0 < G) (hMb : 0 < Mb) (ha0 : 0 < a0) :
    let Tlaw := mup * Real.sqrt (G * Mb * a0) / (2 * kB)
    let Mimpl := 4 * ((kB * Tlaw / mup) ^ 2) / (G * a0)
    Mimpl = Mb := by
  intro Tlaw Mimpl
  dsimp [Mimpl, Tlaw]
  have hkB0 : kB ≠ 0 := ne_of_gt hkB
  have hmup0 : mup ≠ 0 := ne_of_gt hmup
  have hG0 : G ≠ 0 := ne_of_gt hG
  have ha00 : a0 ≠ 0 := ne_of_gt ha0
  have hsq : Real.sqrt (G * Mb * a0) ^ 2 = G * Mb * a0 :=
    Real.sq_sqrt (by positivity)
  -- the k_B / (mu m_p) cancellations: (kB*(mup*sq/(2 kB))/mup)^2 = (sq/2)^2
  have hx : (kB * (mup * Real.sqrt (G * Mb * a0) / (2 * kB)) / mup) ^ 2 =
      (Real.sqrt (G * Mb * a0) / 2) ^ 2 := by
    field_simp [hkB0, hmup0]
  rw [hx]
  -- the sqrt closes: (sq/2)^2 = G M_b a0 / 4
  have hs : (Real.sqrt (G * Mb * a0) / 2) ^ 2 = G * Mb * a0 / 4 := by
    rw [div_pow]
    rw [hsq]
    ring
  rw [hs]
  field_simp [hG0, ha00]


-- ============================================================
-- 3. THE DUAL ROUND TRIP: substituting the inverse's mass into the law
--    returns the temperature: T(M_impl(T)) = T
-- ============================================================

theorem inversion_dual (kB T mup G a0 : ℝ) (hkB : 0 < kB) (hmup : 0 < mup)
    (hG : 0 < G) (ha0 : 0 < a0) (hT : 0 < T) :
    let Mimpl := 4 * ((kB * T / mup) ^ 2) / (G * a0)
    let Tback := mup * Real.sqrt (G * Mimpl * a0) / (2 * kB)
    Tback = T := by
  intro Mimpl Tback
  dsimp [Tback, Mimpl]
  have hkB0 : kB ≠ 0 := ne_of_gt hkB
  have hmup0 : mup ≠ 0 := ne_of_gt hmup
  have hG0 : G ≠ 0 := ne_of_gt hG
  have ha00 : a0 ≠ 0 := ne_of_gt ha0
  -- inside the sqrt: G * M_impl * a0 = 4 (k_B T/mu m_p)^2 exactly
  have harg : G * (4 * ((kB * T / mup) ^ 2) / (G * a0)) * a0 =
      4 * (kB * T / mup) ^ 2 := by
    field_simp [hG0, ha00]
  -- ... and its sqrt is 2 k_B T/(mu m_p) (both sides nonnegative)
  have hsqrt : Real.sqrt (G * (4 * ((kB * T / mup) ^ 2) / (G * a0)) * a0) =
      2 * (kB * T / mup) := by
    have hnonneg : 0 ≤ G * (4 * ((kB * T / mup) ^ 2) / (G * a0)) * a0 := by
      positivity
    have hsq : Real.sqrt (G * (4 * ((kB * T / mup) ^ 2) / (G * a0)) * a0) ^ 2 =
        (2 * (kB * T / mup)) ^ 2 := by
      rw [Real.sq_sqrt hnonneg]
      rw [harg]
      ring
    have hnonneg2 : 0 ≤ 2 * (kB * T / mup) := by positivity
    have hor := eq_or_eq_neg_of_sq_eq_sq
      (Real.sqrt (G * (4 * ((kB * T / mup) ^ 2) / (G * a0)) * a0))
      (2 * (kB * T / mup)) hsq
    rcases hor with h | h
    · exact h
    · have hle : 0 ≤ -(2 * (kB * T / mup)) := by
        rw [← h]
        exact Real.sqrt_nonneg _
      have hgt : 0 < 2 * (kB * T / mup) := by positivity
      nlinarith
  rw [hsqrt]
  field_simp [hkB0, hmup0]


-- ============================================================
-- 4. THE COROLLARY: the estimator is mass-ratio-invariant under the
--    (mu m_p) scale -- M_impl(lam*T, lam*(mu m_p)) = M_impl(T, mu m_p),
--    i.e. only the ratio k_B T/(mu m_p) enters
-- ============================================================

-- the ratio itself is scale-free: k_B (lam T)/(lam (mu m_p)) = k_B T/(mu m_p)
theorem ratio_scale_invariant (kB T mup lam : ℝ) (hkB : 0 < kB)
    (hmup : 0 < mup) (hl : 0 < lam) :
    kB * (lam * T) / (lam * mup) = kB * T / mup := by
  field_simp [ne_of_gt hkB, ne_of_gt hmup, ne_of_gt hl]

theorem mass_ratio_invariant (kB T mup lam G a0 : ℝ) (hkB : 0 < kB)
    (hmup : 0 < mup) (hl : 0 < lam) (hG : 0 < G) (ha0 : 0 < a0) :
    let M0 := 4 * ((kB * T / mup) ^ 2) / (G * a0)
    let M1 := 4 * ((kB * (lam * T) / (lam * mup)) ^ 2) / (G * a0)
    M1 = M0 := by
  intro M0 M1
  dsimp [M0, M1]
  rw [ratio_scale_invariant kB T mup lam hkB hmup hl]

-- the rung form: at EQUAL sigma, T_phase/T_bary = m/(mu m_p) (G151 A3,
-- c/a = mu m_p/m = 1.126e5; A02 V2a m/m_p = 5.32921e-06 vs SM 5.32895e-06)
-- -- the law reads only the RATIO m/(mu m_p), invariant under the joint
-- (m, mu m_p) rescale
theorem proton_rung_ratio (kB mup m sg : ℝ) (hkB : 0 < kB) (hmup : 0 < mup)
    (hs : 0 < sg) :
    let Tph := m * sg ^ 2 / kB
    let Tbar := mup * sg ^ 2 / kB
    Tph / Tbar = m / mup := by
  intro Tph Tbar
  dsimp [Tph, Tbar]
  field_simp [ne_of_gt hkB, ne_of_gt hmup, (show sg ≠ 0 by positivity)]

#print axioms field_identity
#print axioms mass_free_ratio
#print axioms inversion_identity
#print axioms inversion_dual
#print axioms ratio_scale_invariant
#print axioms mass_ratio_invariant
#print axioms proton_rung_ratio