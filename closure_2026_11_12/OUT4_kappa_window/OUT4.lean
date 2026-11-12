/-
OUT-4 (KAPPA WINDOW): the load-bearing algebra of the one theorem T*.

    (T*)   a_0 = c^2 / (2 lambda_L) ,      lambda_L := c / sqrt(G rho_Lambda)

    i.e. the law's saturation value is the surface gravity of the vacuum's own Jeans
    sphere (the unique length whose light-crossing time equals the vacuum's free-fall
    time).  If T* holds, kappa = 1/2 exactly and the kappa question is closed.

Certified here:

  Tstar_iff_kappa_half        : T* is EXACTLY the statement kappa = 1/2 -- both directions.
                                (An equivalence, not a derivation: see the MUTATE file.)
  Lambda_l0_sq               : Lambda * l_0^2 = 8 pi / kappa^2   (l_0 = c^2/a_0, kappa != 0)
  Lambda_l0_sq_at_half       : at kappa = 1/2 this is 32 pi
  rho_c2_iff_kappa_sq_quarter : rho_L c^2 = 4 a_0^2 / G  <=>  kappa^2 = 1/4  (the same statement)
  Rschw_over_lambda          : R_schw(lambda_L) / lambda_L = 8 pi / 3, EXACTLY, for any
                               ball of uniform density whose radius is lambda_L.
                               So lambda_L is 8.38x too SMALL to be its own Schwarzschild
                               radius, and c^2/(2 lambda_L) is NOT a surface gravity.
  lambdaL_sq_equals          : lambda_L^2 = c^2/(G rho_L)
  lambdaL_over_dS_sq         : lambda_L^2 / R_dS^2 = 8 pi / 3
  no_horizon_beyond_RdS      : in Schwarzschild-de Sitter with M >= 0, EVERY horizon obeys
                               r^2 <= 3/Lambda.  (Kottler: f = 1 - 2GM/(c^2 r) - Lambda r^2/3;
                               f = 0 forces Lambda r^2/3 = 1 - 2GM/(c^2 r) <= 1.)
  lambdaL_exceeds_all_horizons : lambda_L^2 > 3/Lambda, so NO SdS horizon sits at lambda_L.
                               The surface-gravity reading has no object to be the surface
                               gravity of.  (Sharper restatement of k05's H1.)
  kappa_weight_one           : under a_0 -> lam a_0 at fixed rho_Lambda, kappa -> lam kappa:
                               the definition is G_lambda-homogeneous of weight 1.

SCOPE.  This file certifies ALGEBRA and the one geometric exclusion.  It does not certify that
the vacuum's Jeans length is the length the law must use, that the factor 1/2 is a surface
gravity (the file proves it is NOT), or that any numerical value is realised.  Those are graded
in out4.out.  kappa = 1/2 FITTED; not theory closed.  Adopts nothing.
-/

import Mathlib

noncomputable section

namespace Out4

open Real

/-- The definition of kappa. -/
def kappa (a0 c G rho : ℝ) : ℝ := a0 / (c * sqrt (G * rho))

/-- The vacuum's Jeans / light-crossing length. -/
def lamL (c G rho : ℝ) : ℝ := c / sqrt (G * rho)

/-- The MOND length. -/
def l0 (c a0 : ℝ) : ℝ := c ^ 2 / a0

/-- The Schwarzschild radius of a uniform ball of density rho and radius R. -/
def rSchwBall (G rho R c : ℝ) : ℝ := 2 * G * ((4 * Real.pi / 3) * rho * R ^ 3) / c ^ 2

/-- handy: sqrt(G rho) is nonzero and positive when G, rho are. -/
lemma sqrt_pos_of_pos {G rho : ℝ} (hG : 0 < G) (hrho : 0 < rho) :
    0 < sqrt (G * rho) := by
  exact sqrt_pos.2 (mul_pos hG hrho)

-- ---------------------------------------------------------------- 1. T* is exactly kappa = 1/2

/-- T* implies kappa = 1/2. -/
theorem Tstar_implies_kappa_half {a0 c G rho : ℝ}
    (hc : c ≠ 0) (hG : 0 < G) (hrho : 0 < rho)
    (hT : a0 = c ^ 2 / (2 * lamL c G rho)) :
    kappa a0 c G rho = 1 / 2 := by
  have hs : sqrt (G * rho) ≠ 0 := ne_of_gt (sqrt_pos_of_pos hG hrho)
  unfold kappa lamL at *
  field_simp [hc, hs] at hT ⊢
  ring_nf at hT ⊢
  nlinarith

/-- kappa = 1/2 implies T*.  Together with the previous theorem this says T* IS the
    statement kappa = 1/2: an equivalence, carrying no information beyond it. -/
theorem kappa_half_implies_Tstar {a0 c G rho : ℝ}
    (hc : c ≠ 0) (hG : 0 < G) (hrho : 0 < rho)
    (hk : kappa a0 c G rho = 1 / 2) :
    a0 = c ^ 2 / (2 * lamL c G rho) := by
  have hs : sqrt (G * rho) ≠ 0 := ne_of_gt (sqrt_pos_of_pos hG hrho)
  unfold kappa lamL at *
  field_simp [hc, hs] at hk ⊢
  ring_nf at hk ⊢
  nlinarith

/-- The packaged equivalence (the lane's central algebraic fact). -/
theorem Tstar_iff_kappa_half {a0 c G rho : ℝ}
    (hc : c ≠ 0) (hG : 0 < G) (hrho : 0 < rho) :
    (a0 = c ^ 2 / (2 * lamL c G rho)) ↔ kappa a0 c G rho = 1 / 2 :=
  ⟨Tstar_implies_kappa_half hc hG hrho, kappa_half_implies_Tstar hc hG hrho⟩

-- ---------------------------------------------------------------- 2. the same statement, twice more

/-- Lambda * l_0^2 = 8 pi / kappa^2, with Lambda = 8 pi G rho / c^2 and a_0 = kappa c sqrt(G rho). -/
theorem Lambda_l0_sq {a0 c G rho kap : ℝ}
    (hG : 0 < G) (hrho : 0 < rho) (hc : c ≠ 0) (hkap : kap ≠ 0)
    (ha0 : a0 = kap * c * sqrt (G * rho)) :
    (8 * Real.pi * G * rho / c ^ 2) * (l0 c a0) ^ 2 = 8 * Real.pi / kap ^ 2 := by
  unfold l0
  rw [ha0]
  have hsq : (sqrt (G * rho)) ^ 2 = G * rho := by
    rw [sq_sqrt (le_of_lt (mul_pos hG hrho))]
  have hs : sqrt (G * rho) ≠ 0 := ne_of_gt (sqrt_pos_of_pos hG hrho)
  field_simp [hc, hkap, hs]
  ring_nf
  nlinarith

/-- At kappa = 1/2 the identity reads Lambda l_0^2 = 32 pi. -/
theorem Lambda_l0_sq_at_half {a0 c G rho : ℝ}
    (hG : 0 < G) (hrho : 0 < rho) (hc : c ≠ 0)
    (ha0 : a0 = (1 / 2 : ℝ) * c * sqrt (G * rho)) :
    (8 * Real.pi * G * rho / c ^ 2) * (l0 c a0) ^ 2 = 32 * Real.pi := by
  have h := Lambda_l0_sq (a0 := a0) (c := c) (G := G) (rho := rho) (kap := 1 / 2)
    hG hrho hc (by norm_num) ha0
  norm_num at h
  ring_nf at h ⊢
  exact h

/-- The convention-free content of "32 pi": rho_L c^2 = 4 a_0^2 / G is kappa^2 = 1/4. -/
theorem rho_c2_iff_kappa_sq_quarter {a0 c G rho kap : ℝ}
    (hG : 0 < G) (hrho : 0 < rho) (hc : c ≠ 0)
    (ha0 : a0 = kap * c * sqrt (G * rho)) :
    rho * c ^ 2 = 4 * a0 ^ 2 / G ↔ kap ^ 2 = 1 / 4 := by
  have hsq : (sqrt (G * rho)) ^ 2 = G * rho := by
    rw [sq_sqrt (le_of_lt (mul_pos hG hrho))]
  have hsq' : (sqrt (rho * G)) ^ 2 = G * rho := by
    rw [mul_comm rho G, sq_sqrt (le_of_lt (mul_pos hG hrho))]
  have hA : 0 < G * rho * c ^ 2 := by positivity
  rw [ha0]
  constructor
  · intro h
    field_simp [ne_of_gt hG] at h
    ring_nf at h
    simp [hsq'] at h
    ring_nf at h
    nlinarith
  · intro hk
    field_simp [ne_of_gt hG]
    ring_nf
    simp [hsq']
    ring_nf
    nlinarith

-- ---------------------------------------------------------------- 3. the 1/2 is NOT a surface gravity

/-- For a uniform ball of density rho whose radius is the Jeans length c/sqrt(G rho),
    the Schwarzschild radius is 8 pi / 3 times that radius.  Exact; independent of G, c, rho. -/
theorem Rschw_over_lambda {G rho c : ℝ}
    (hG : 0 < G) (hrho : 0 < rho) (hc : c ≠ 0) :
    rSchwBall G rho (lamL c G rho) c / lamL c G rho = 8 * Real.pi / 3 := by
  unfold rSchwBall lamL
  have hsq : (sqrt (G * rho)) ^ 2 = G * rho := by
    rw [sq_sqrt (le_of_lt (mul_pos hG hrho))]
  have hs : sqrt (G * rho) ≠ 0 := ne_of_gt (sqrt_pos_of_pos hG hrho)
  field_simp [hc, hs]
  ring_nf
  nlinarith

/-- lambda_L^2 = c^2/(G rho_L). -/
theorem lambdaL_sq_equals {c G rho : ℝ}
    (hG : 0 < G) (hrho : 0 < rho) :
    (lamL c G rho) ^ 2 = c ^ 2 / (G * rho) := by
  unfold lamL
  have hsq : (sqrt (G * rho)) ^ 2 = G * rho := by
    rw [sq_sqrt (le_of_lt (mul_pos hG hrho))]
  have hs : sqrt (G * rho) ≠ 0 := ne_of_gt (sqrt_pos_of_pos hG hrho)
  field_simp [hs]
  nlinarith

/-- lambda_L^2 / R_dS^2 = 8 pi / 3, where R_dS^2 = 3/Lambda and Lambda = 8 pi G rho / c^2. -/
theorem lambdaL_over_dS_sq {c G rho : ℝ}
    (hG : 0 < G) (hrho : 0 < rho) (hc : c ≠ 0) :
    (lamL c G rho) ^ 2 / (3 / (8 * Real.pi * G * rho / c ^ 2)) = 8 * Real.pi / 3 := by
  have h := lambdaL_sq_equals (c := c) (G := G) (rho := rho) hG hrho
  rw [h]
  have hne : 8 * Real.pi * G * rho / c ^ 2 ≠ 0 := by positivity
  field_simp [hne, hc]

-- ---------------------------------------------------------------- 4. no horizon at lambda_L

/-- Kottler / Schwarzschild-de Sitter: with M >= 0, every horizon obeys r^2 <= 3/Lambda.
    This is the geometric exclusion: no horizon of any mass sits outside R_dS = sqrt(3/Lambda). -/
theorem no_horizon_beyond_RdS {G M c r Lam : ℝ}
    (hG : 0 < G) (hM : 0 ≤ M) (hc : 0 < c) (hr : 0 < r) (hLam : 0 < Lam)
    (hf : 1 - 2 * G * M / (c ^ 2 * r) - Lam * r ^ 2 / 3 = 0) :
    r ^ 2 ≤ 3 / Lam := by
  have hterm : 0 ≤ 2 * G * M / (c ^ 2 * r) := by positivity
  have h1 : Lam * r ^ 2 / 3 ≤ 1 := by nlinarith
  have h2 : Lam * r ^ 2 ≤ 3 := by nlinarith
  exact (le_div_iff₀ hLam).2 (by nlinarith)

/-- lambda_L^2 > 3/Lambda: the Jeans length lies strictly OUTSIDE the largest possible
    horizon radius.  Combined with no_horizon_beyond_RdS, no configuration of the theory
    has a horizon at lambda_L, so c^2/(2 lambda_L) is not a surface gravity of anything. -/
theorem lambdaL_exceeds_all_horizons {c G rho Lam : ℝ}
    (hG : 0 < G) (hrho : 0 < rho) (hc : 0 < c)
    (hLam_def : Lam = 8 * Real.pi * G * rho / c ^ 2) :
    3 / Lam < (lamL c G rho) ^ 2 := by
  rw [hLam_def]
  have h := lambdaL_sq_equals (c := c) (G := G) (rho := rho) hG hrho
  rw [h]
  have hne : 8 * Real.pi * G * rho / c ^ 2 ≠ 0 := by positivity
  have hpi : 3 < 8 * Real.pi := by nlinarith [Real.pi_gt_three]
  field_simp [hne, ne_of_gt hc]
  all_goals nlinarith [hpi]

-- ---------------------------------------------------------------- 5. the scaling weight of kappa

/-- The definition is G_lambda-homogeneous of weight 1: kappa -> lam kappa.
    This is FINAL-16 J1 / FINAL-17 A4 in one line: kappa is the orbit coordinate, and the
    relation that defines it is covariant, so it cannot value it. -/
theorem kappa_weight_one {a0 c G rho lam : ℝ} :
    kappa (lam * a0) c G rho = lam * kappa a0 c G rho := by
  unfold kappa
  ring

end Out4

end
