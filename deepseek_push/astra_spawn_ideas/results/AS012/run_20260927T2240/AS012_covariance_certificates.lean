import Mathlib

/-!
# AS012 — Propagating correlated vacuum uncertainties (certificates)

Framework base (adopted inputs, NOT derived here):
    a0 = kappa * c * sqrt(G * rho_L),   kappa = 1/2 adopted
    ln a0 = ln kappa + ln c + (ln G + ln rho_L)/2,
    J = (1, 1/2, 1/2)  d ln a0 / d (ln kappa, ln G, ln rho_L)
    Var(ln a0) = J Cov J^T            (exact: ln a0 is affine in the logs)
    r_M = sqrt(G*M_b/a0);  v_flat^4 = G*M_b*a0;  sigma^2 = C/2;
    rho_ph = C/(4 pi G r^2);  P = sigma^2 rho_ph   (conditional deep-equilibrium
    inputs/targets of the framework contract, not solved dynamics),  C = sqrt(G M a0).

What is certified (real arithmetic; positive domain):

1. `quad_form_expansion` — the six-term log-variance formula:
       J Cov J^T = sigma_k^2 + (1/4) sigma_G^2 + (1/4) sigma_L^2
                 + sigma_kG + sigma_kL + (1/2) sigma_GL
   for the symmetric Cov = [[a, kg, kl], [kg, k, gl], [kl, gl, l]].
   Every cross term's coefficient in the propagation is fixed by the affine
   map: kappa–G and kappa–rho_L enter with coefficient 1, G–rho_L with 1/2.

2. `P_G_cancels` — in P = sigma^2 rho_ph with sigma^2 = C/2, rho_ph = C/(4 pi G r^2),
       P = M_b a0 / (8 pi r^2),
   i.e. the explicit Newton constant G cancels IDENTICALLY: at fixed vacuum
   inputs (and with them fixed a0), the equilibrium pressure P carries no
   direct G dependence.  Uncertainty consequence: d ln P / d ln G = 0 at fixed
   (kappa, rho_L, M_b, r), i.e. the log-sensitivity vector of P equals J itself
   (1, 1/2, 1/2) over (ln kappa, ln G, ln rho_L) - so Var(ln P) = Var(ln a0)
   for fixed (M_b, r): the pressure inherits the vacuum-scale variance 1:1.

3. `null_direction_invariance` — perturbations of the vacuum inputs along the
   kernel direction of J leave a0 EXACTLY invariant: for real u, v, w with
       u + v/2 + w/2 = 0   (d ln kappa = u, d ln G = v, d ln rho_L = w)
       a0(kappa e^u, G e^v, rho e^w) = a0(kappa, G, rho).
   Consequently Cov mass sitting in the 2-dimensional null space of J is
   invisible to a0: the covariance that matters is the quadratic form J Cov J^T.

These certify the propagation algebra and the level-set geometry only.  They do
not derive kappa = 1/2, do not fix the physical value of rho_Lambda, and do not
establish which physical vacuum density enters the galactic scale (that remains
the open footing question).  No probability-theoretic statement is certified
here; the variance semantics is the standard one for affine maps.
-/

open scoped Real

namespace AS012

noncomputable def qform (a k l kg kl gl : ℝ) : ℝ :=
  (1 : ℝ) * (a * 1 + kg * (1 / 2 : ℝ) + kl * (1 / 2 : ℝ))
    + (1 / 2 : ℝ) * (kg * 1 + k * (1 / 2 : ℝ) + gl * (1 / 2 : ℝ))
    + (1 / 2 : ℝ) * (kl * 1 + gl * (1 / 2 : ℝ) + l * (1 / 2 : ℝ))

/-- J Cov J^T written out: sigma_k^2 + (1/4)sigma_G^2 + (1/4)sigma_L^2
    + sigma_kG + sigma_kL + (1/2)sigma_GL for symmetric Cov. -/
theorem quad_form_expansion (a k l kg kl gl : ℝ) :
    qform a k l kg kl gl = a + kg + kl + k / 4 + gl / 2 + l / 4 := by
  unfold qform
  ring

/-- P = sigma^2 rho_ph = M a0 / (8 pi r^2): the explicit G cancels identically,
    with sigma^2 = C/2, rho_ph = C/(4 pi G r^2), C = sqrt(G M a0). -/
theorem P_G_cancels {G M a r : ℝ} (hG : 0 < G) (hM : 0 < M) (ha : 0 < a) (hr : 0 < r) :
    (Real.sqrt (G * M * a) / 2) * (Real.sqrt (G * M * a) / (4 * π * G * r ^ 2))
      = M * a / (8 * π * r ^ 2) := by
  have hGMa : 0 ≤ G * M * a := by
    exact mul_nonneg (mul_nonneg (le_of_lt hG) (le_of_lt hM)) (le_of_lt ha)
  let s : ℝ := Real.sqrt (G * M * a)
  have hsq : s ^ 2 = G * M * a := by
    dsimp [s]
    exact Real.sq_sqrt hGMa
  have hss : s * s = G * M * a := by
    rw [← pow_two, hsq]
  have hGz : G ≠ 0 := ne_of_gt hG
  have hpi : 8 * π ≠ 0 := by positivity
  have hr2z : r ^ 2 ≠ 0 := pow_ne_zero 2 (ne_of_gt hr)
  calc
    (s / 2) * (s / (4 * π * G * r ^ 2)) = (s * s) / (8 * π * G * r ^ 2) := by
      field_simp [hGz, hpi, hr2z]
      ring
    _ = (G * M * a) / (8 * π * G * r ^ 2) := by
      rw [hss]
    _ = M * a / (8 * π * r ^ 2) := by
      field_simp [hGz, hpi, hr2z]

/-- Perturbations along the kernel direction of J leave a0 exactly invariant:
    u + v/2 + w/2 = 0  =>  a0(kappa e^u, G e^v, rho e^w) = a0(kappa, G, rho)
    on the nonnegativity domain (hence, in particular, for positive inputs). -/
theorem null_direction_invariance {kappa c G rho u v w : ℝ}
    (hk : 0 ≤ kappa) (hc : 0 ≤ c) (hG : 0 ≤ G) (hr : 0 ≤ rho)
    (hnull : u + v / 2 + w / 2 = 0) :
    kappa * Real.exp u * c * Real.sqrt (G * Real.exp v * rho * Real.exp w)
      = kappa * c * Real.sqrt (G * rho) := by
  have hGr : 0 ≤ G * rho := mul_nonneg hG hr
  have hgre : 0 ≤ G * Real.exp v * rho * Real.exp w := by
    positivity
  have hsqrt_ew : Real.sqrt (Real.exp v * Real.exp w) = Real.exp ((v + w) / 2) := by
    rw [← Real.exp_add]
    have hsq : (Real.exp ((v + w) / 2)) ^ 2 = Real.exp (v + w) := by
      have h2 : (v + w) / 2 + (v + w) / 2 = v + w := by
        ring
      rw [← h2, Real.exp_add, pow_two]
      ring
    rw [← hsq, Real.sqrt_sq_eq_abs]
    exact abs_of_nonneg (Real.exp_nonneg _)
  have hre : G * Real.exp v * rho * Real.exp w = (G * rho) * (Real.exp v * Real.exp w) := by
    ring
  have hsplit : (Real.sqrt (G * Real.exp v * rho * Real.exp w))
      = Real.sqrt (G * rho) * Real.exp ((v + w) / 2) := by
    rw [hre, Real.sqrt_mul hGr (Real.exp v * Real.exp w), hsqrt_ew]
  have hprod : Real.exp u * Real.exp ((v + w) / 2) = 1 := by
    rw [← Real.exp_add, ← Real.exp_zero]
    congr 1
    nlinarith [hnull]
  calc
    kappa * Real.exp u * c * Real.sqrt (G * Real.exp v * rho * Real.exp w)
        = kappa * Real.exp u * c * (Real.sqrt (G * rho) * Real.exp ((v + w) / 2)) := by
      rw [hsplit]
    _ = kappa * c * Real.sqrt (G * rho) * (Real.exp u * Real.exp ((v + w) / 2)) := by
      ring
    _ = kappa * c * Real.sqrt (G * rho) := by
      rw [hprod, mul_one]

#print axioms quad_form_expansion
#print axioms P_G_cancels
#print axioms null_direction_invariance