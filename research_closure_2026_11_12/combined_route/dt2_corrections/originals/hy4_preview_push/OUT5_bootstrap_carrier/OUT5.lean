/-
  OUT-5 (BOOTSTRAP CARRIER) -- the load-bearing algebra, certified.

  The lane's exact statements, in the fragment of real algebra that carries them.
  Everything here is used by a graded gate:

    T1/T2  the pinning's two coefficients for law S          (G1, G2, KA4)
    T3     the baryon coefficient has a0, the gradient one does not   (G11, flat direction)
    T4/T5  law S and law B (the a0-line) as quadratics               (G2)
    T6     the K-matter / pinning matching scale mu_K^match           (G7, K1)
    T7/T8  the FRW dust line: w <= 1/100 at z 3400  =>  mu_K^2 >= ...  (G6)
    T9     the deep-regime pinned density carries no a0               (G11)

  TEST lane, quarantined.  Adopts nothing.  kappa = 1/2 FITTED; not theory closed.
-/

import Mathlib

noncomputable section

namespace OUT5

/-- the two kernels.  u = g/a0.  Law S is action (A)'s kernel; law B is the a0-line
    g^2 = g_N^2 + a0 g_N. -/
def muS (u : ℝ) : ℝ := u / (1 + u)
def muB (u : ℝ) : ℝ := (Real.sqrt (1 + 4 * u ^ 2) - 1) / (2 * u)

-- ============================================================ T1 / T2 ======

/-- (T1)  law S:  (1 - mu)/mu = 1/u = a0/g.  This is the first coefficient of the
    pinning, and the enclosed-mass statement M_c = [(1-mu)/mu] M_b. -/
theorem muS_inv (u : ℝ) (hu : u ≠ 0) (h1 : 1 + u ≠ 0) :
    (1 - muS u) / muS u = 1 / u := by
  unfold muS
  field_simp [hu, h1]
  ring_nf

/-- (T1')  the same coefficient times u is exactly 1. -/
theorem muS_inv_mul (u : ℝ) (hu : u ≠ 0) (h1 : 1 + u ≠ 0) :
    ((1 - muS u) / muS u) * u = 1 := by
  rw [muS_inv u hu h1]
  field_simp [hu]

/-- (T2)  law S:  mu'(u) * u / mu = 1/(1+u).  This is the SECOND coefficient of the
    pinning, mu' g/mu, and it is what multiplies partial_s g. -/
theorem muS_slope (u : ℝ) (hu : u ≠ 0) (h1 : 1 + u ≠ 0) :
    (1 / (1 + u) ^ 2) * u / muS u = 1 / (1 + u) := by
  unfold muS
  field_simp [hu, h1]

/-- (T2')  at u = 0 that coefficient is exactly 1: the gradient term of the pinning is
    partial_s g /(4 pi G), with no a0 anywhere. -/
theorem muS_slope_at_zero : (1 / (1 + (0 : ℝ)) ^ 2) = 1 := by norm_num

-- ============================================================ T3 / T9 ======

/-- (T3)  a0/(g + a0) = 1/(1 + g/a0): the gradient coefficient written in physical
    variables.  It is a function of u = g/a0 ALONE -- no separate a0. -/
theorem lawS_gradient_coefficient (g a0 : ℝ) (ha0 : a0 ≠ 0) (hg : g + a0 ≠ 0) :
    a0 / (g + a0) = 1 / (1 + g / a0) := by
  have hden : 1 + g / a0 ≠ 0 := by
    intro hz
    apply hg
    have : a0 * (1 + g / a0) = 0 := by rw [hz, mul_zero]
    field_simp [ha0] at this
    linarith
  have hrew : g + a0 = a0 * (1 + g / a0) := by
    field_simp [ha0]
    ring
  rw [hrew]
  field_simp [ha0, hden]

/-- the deep-regime pinned density, regarded as a function of a0 with the field held
    fixed. -/
def rhoPinDeepOf (dsg G : ℝ) (_a0 : ℝ) : ℝ := dsg / (4 * Real.pi * G)

/-- (T9)  THE FLAT DIRECTION.  The deep-regime pinned density outside the baryons is
    rho_c = partial_s g / (4 pi G).  As a function of a0 it is constant, so no choice of
    kappa (a0 = kappa c sqrt(G rho_Lam)) changes any halo observable of this carrier.
    This is why OUT-5 reports kappa and does not derive it. -/
theorem kappa_is_a_flat_direction (dsg G a0a a0b : ℝ) :
    rhoPinDeepOf dsg G a0a = rhoPinDeepOf dsg G a0b := by
  simp [rhoPinDeepOf]

-- ============================================================ T4 / T5 ======

/-- (T4)  law S as a quadratic: with y := g_N/a0 = mu*u = u^2/(1+u), the relation
    u^2 = y (u + 1) holds identically.  (g^2 = g_N (g + a0).) -/
theorem lawS_quadratic (u : ℝ) (h1 : 1 + u ≠ 0) :
    (u ^ 2 / (1 + u)) * (u + 1) = u ^ 2 := by
  field_simp [h1]
  ring

/-- (T5)  law B, the a0-line: with s := sqrt(1 + 4u^2) and y := (s-1)/2 = mu*u,
    y^2 + y = u^2 identically.  (g^2 = g_N^2 + a0 g_N.) -/
theorem lawB_quadratic (u s : ℝ) (hsq : s ^ 2 = 1 + 4 * u ^ 2) :
    ((s - 1) / 2) ^ 2 + (s - 1) / 2 = u ^ 2 := by
  rw [show ((s - 1) / 2) ^ 2 + (s - 1) / 2 = (s ^ 2 - 1) / 4 by ring]
  rw [hsq]
  ring

/-- (T5')  1/mu_B = (s+1)/(2u): the enclosed mass for the a0-line,
    M_c/M_b = (1-mu)/mu = sqrt(1+x^2) - 1. -/
theorem muB_inv (u s : ℝ) (hu : u ≠ 0) (hs1 : s - 1 ≠ 0) (hsq : s ^ 2 = 1 + 4 * u ^ 2) :
    1 / ((s - 1) / (2 * u)) = (s + 1) / (2 * u) := by
  field_simp [hu, hs1]
  nlinarith [hsq]

-- ============================================================ T6 ============

/-- (T6)  mu_K^match.  Setting the K-matter halo density mu_K^2 |Phi| /(4 pi G) equal to
    the pinned density partial_s g /(4 pi G), with |Phi| = v_flat^2 L and
    partial_s g = v_flat^2 / r^2, gives mu_K^2 = 1/(r^2 L): the matching scale carries
    NO M_b, NO a0 and NO kernel.  It is a function of radius alone. -/
theorem muK_match (r L v : ℝ) (hr : r ≠ 0) (hL : L ≠ 0) :
    (1 / (r ^ 2 * L)) * (v ^ 2 * L) = v ^ 2 / r ^ 2 := by
  field_simp [hr, hL]

/-- (T6')  the same as the lane grades it: the matching scale is unique. -/
theorem muK_match_unique (muK r L v : ℝ) (hv : v ≠ 0) (hr : r ≠ 0) (hL : L ≠ 0)
    (h : muK ^ 2 * (v ^ 2 * L) = v ^ 2 / r ^ 2) :
    muK ^ 2 = 1 / (r ^ 2 * L) := by
  have hv2 : v ^ 2 ≠ 0 := pow_ne_zero 2 hv
  field_simp [hv2, hL, hr] at h ⊢
  exact h

-- ============================================================ T7 / T8 ======

/-- (T7)  the FRW dust: w = w0/(w0 + a^3).  w <= 1/100 forces 99 w0 <= a^3. -/
theorem dust_cold_iff (w0 a : ℝ) (hpos : 0 < w0 + a ^ 3) :
    w0 / (w0 + a ^ 3) ≤ (1 / 100 : ℝ) → 99 * w0 ≤ a ^ 3 := by
  intro hw
  rw [div_le_iff₀ hpos] at hw
  nlinarith

/-- (T8)  with w0 = I0/(4 mu_K^2), cold at the epoch a forces
    mu_K^2 >= 99 I0 /(4 a^3).  At a = 1/3401 and I0 = 4.037e-8 Mpc^-2 this is the
    mu_K >= 198.25 /Mpc line (KD1 B1a, MK1 row 1). -/
theorem muK_line (I0 muK a : ℝ) (hmu : 0 < muK) (ha : 0 < a)
    (h : 99 * (I0 / (4 * muK ^ 2)) ≤ a ^ 3) :
    muK ^ 2 ≥ 99 * I0 / (4 * a ^ 3) := by
  have hmu2 : 0 < muK ^ 2 := pow_pos hmu 2
  have hden : 0 < 4 * muK ^ 2 := by positivity
  have hden2 : 0 < 4 * a ^ 3 := by positivity
  have h1 : (99 * I0) / (4 * muK ^ 2) ≤ a ^ 3 := by
    convert h using 1
    ring
  rw [div_le_iff₀ hden] at h1
  show 99 * I0 / (4 * a ^ 3) ≤ muK ^ 2
  rw [div_le_iff₀ hden2]
  nlinarith

-- ============================================================ the pinning ===

/-- the pinning, in the form the lane grades it (law S, rho_b = 0 outside the baryons):
    4 pi G rho_c = [a0/(g+a0)] partial_s g.  With u = g/a0 that coefficient is
    1/(1+u), which is 1 at u = 0 and carries no a0 of its own. -/
theorem pinning_lawS (a0 g dsg : ℝ) (ha0 : a0 ≠ 0) (hg : g + a0 ≠ 0) :
    (a0 / (g + a0)) * dsg = (1 / (1 + g / a0)) * dsg := by
  rw [lawS_gradient_coefficient g a0 ha0 hg]

end OUT5
