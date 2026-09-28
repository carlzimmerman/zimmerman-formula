/-
AS048 -- MONO splice smoothing as a declared new candidate (Lean 4 certificate
layer).  Operative MONO branch, dimensionless y = B/a0 > 0, filtered field
equation with the heat filter S = exp[(xi^2/2) Delta] acting on a flat leaf
as a Gaussian smoother with Fourier multiplier exp[-(xi^2/2) |k|^2].

Certified exact statements (algebra / monotonicity / integral level; the
transcendental splice roots y_p, y_star and the h'' jump J = +3.4744713554836e-2
are carried numerically in the companion Python run):

  B  deviation bound:   for t >= 0,  1 - exp(-t) <= t.
     (bounds ||S f - f||_2 <= (xi^2/2) ||Delta f||_2 and, for fields with
      |f''| <= M, the pointwise deviation |(S f - f)(y)| <= (1/2) M xi^2.)
  M1 mode first derivative:  d/dx [ C cos(k x) ] = -C k sin(k x).
  M2 mode eigenrelation:     d/dx [ -C k sin(k x) ] = -k^2 C cos(k x),
     i.e. the damped cosine u(x) = exp[-(xi^2/2)k^2] cos(k x) satisfies
     u'' = -k^2 u  -- the exact Fourier-mode multiplier statement at the
     amplitude level: the heat semigroup keeps the mode a mode and its
     amplitude factor is exp[-(xi^2/2)k^2].
  H  heat-semigroup rate: d/dt |_t exp[-(xi^2/2)k^2 cos(k x) form]:
     d/dt exp(-k^2 t) * cos(k x) = -k^2 * exp(-k^2 t) * cos(k x).
  G  Gaussian normalization:  for xi >= 0,
     ∫_{z in R} exp(-z^2/(2 xi^2)) dz = sqrt(2 pi) * xi,
     i.e. ∫ G_xi = 1 for the kernel G_xi(z) = exp(-z^2/(2xi^2))/sqrt(2 pi xi^2)
     (S applied to constants is the identity).  Uses Mathlib's
     `integral_gaussian`; the xi = 0 case follows Mathlib's convention
     (both sides vanish).
  K  Gaussian kernel is maximal at the centre:  for xi != 0 and any z,
     exp(-z^2/(2 xi^2)) <= 1  and  G_xi(z) <= G_xi(0) for xi > 0.
     (This is the bound driving the kink-residual height estimate:
      the smoothed jump J*(1/2)(1+erf(...)) has slope at most J/sqrt(2 pi)/xi.)
  A  multiplier amplitude identity: exp(-(sigma^2/2) k^2) = exp(-sigma^2 k^2/2).

Axiom discipline: zero `sorry`; printed axioms must be a subset of
{propext, Classical.choice, Quot.sound}.
-/
import Mathlib
import Mathlib.Tactic

noncomputable section

open Real
open Filter
open Topology

namespace AS048

-- --------------------------------------------------------------------------
-- B. Deviation bound: 1 - exp(-t) <= t for t >= 0
-- --------------------------------------------------------------------------
theorem deviation_bound_exp (t : ℝ) (_ht : 0 ≤ t) : 1 - Real.exp (-t) ≤ t := by
  have h : -t + 1 ≤ Real.exp (-t) := by
    simpa using (Real.add_one_le_exp (-t))
  nlinarith [h]

-- --------------------------------------------------------------------------
-- M1. Mode first derivative: d/dx [C cos(k x)] = -C k sin(k x)
-- --------------------------------------------------------------------------
theorem mode_first_deriv (C k x : ℝ) :
    deriv (fun x : ℝ => C * Real.cos (k * x)) x = -C * k * Real.sin (k * x) := by
  have hin : HasDerivAt (fun x : ℝ => k * x) k x := by
    simpa using ((hasDerivAt_id x).const_mul k)
  have hcos : HasDerivAt (fun x : ℝ => Real.cos (k * x)) (-Real.sin (k * x) * k) x := by
    have hfun : (fun x : ℝ => Real.cos (k * x)) = Real.cos ∘ (fun x : ℝ => k * x) := by
      funext y; rfl
    rw [hfun]
    exact (hasDerivAt_cos (k * x)).comp x hin
  have hprod : HasDerivAt (fun x : ℝ => C * Real.cos (k * x))
      (C * (-Real.sin (k * x) * k)) x := hcos.const_mul C
  rw [hprod.deriv]
  ring

-- --------------------------------------------------------------------------
-- M2. Mode eigenrelation: d/dx [-C k sin(k x)] = -k^2 * C cos(k x)
-- --------------------------------------------------------------------------
theorem mode_second_deriv (C k x : ℝ) :
    deriv (fun x : ℝ => -C * k * Real.sin (k * x)) x = -(k ^ 2) * C * Real.cos (k * x) := by
  have hin : HasDerivAt (fun x : ℝ => k * x) k x := by
    simpa using ((hasDerivAt_id x).const_mul k)
  have hsin : HasDerivAt (fun x : ℝ => Real.sin (k * x)) (Real.cos (k * x) * k) x := by
    have hfun : (fun x : ℝ => Real.sin (k * x)) = Real.sin ∘ (fun x : ℝ => k * x) := by
      funext y; rfl
    rw [hfun]
    exact (hasDerivAt_sin (k * x)).comp x hin
  have hprod : HasDerivAt (fun x : ℝ => -C * k * Real.sin (k * x))
      ((-C * k) * (Real.cos (k * x) * k)) x := hsin.const_mul (-C * k)
  rw [hprod.deriv]
  ring

-- --------------------------------------------------------------------------
-- H. Heat-semigroup rate for the mode:
--    d/dt [exp(-k^2 t) * cos(k x)] = -k^2 * exp(-k^2 t) * cos(k x)
-- --------------------------------------------------------------------------
theorem heat_mode_rate (k t x : ℝ) :
    deriv (fun s : ℝ => Real.exp (-(k ^ 2) * s) * Real.cos (k * x)) t
      = -(k ^ 2) * (Real.exp (-(k ^ 2) * t) * Real.cos (k * x)) := by
  have hin : HasDerivAt (fun s : ℝ => -(k ^ 2) * s) (-(k ^ 2)) t := by
    simpa using (((hasDerivAt_id t).const_mul (-(k ^ 2))))
  have hexp : HasDerivAt (fun s : ℝ => Real.exp (-(k ^ 2) * s))
      (Real.exp (-(k ^ 2) * t) * (-(k ^ 2))) t := by
    have hfun : (fun s : ℝ => Real.exp (-(k ^ 2) * s)) = Real.exp ∘ (fun s : ℝ => -(k ^ 2) * s) := by
      funext y; rfl
    rw [hfun]
    exact (Real.hasDerivAt_exp (-(k ^ 2) * t)).comp t hin
  have hprod := hexp.mul_const (Real.cos (k * x))
  rw [hprod.deriv]
  ring

-- --------------------------------------------------------------------------
-- G. Gaussian normalization:  ∫_R exp(-z^2/(2 xi^2)) = sqrt(2 pi) * xi
--    (Mathlib's `integral_gaussian`:  ∫_R exp(-b z^2) = sqrt(pi/b); the
--    convention covers b <= 0 by making both sides vanish, so the xi = 0
--    case is automatic.)
-- --------------------------------------------------------------------------
theorem gaussian_integral_norm (xi : ℝ) (hxi : 0 ≤ xi) :
    (∫ x : ℝ, Real.exp (-(x ^ 2) / (2 * xi ^ 2))) = Real.sqrt (2 * Real.pi) * xi := by
  have hinge := integral_gaussian (1 / (2 * xi ^ 2))
  have hfun : (fun x : ℝ => Real.exp (-(x ^ 2) / (2 * xi ^ 2))) =
      (fun x : ℝ => Real.exp (-(1 / (2 * xi ^ 2)) * x ^ 2)) := by
    funext x
    congr 1
    ring_nf
  rw [hfun]
  rw [hinge]
  have hsqrt : Real.sqrt (Real.pi / (1 / (2 * xi ^ 2))) = Real.sqrt (2 * Real.pi * xi ^ 2) := by
    congr 1
    rw [one_div, div_eq_mul_inv, inv_inv]
    ring
  rw [hsqrt]
  have hsqmul : Real.sqrt (2 * Real.pi * xi ^ 2) =
      Real.sqrt (2 * Real.pi) * Real.sqrt (xi ^ 2) :=
    Real.sqrt_mul (by positivity : 0 ≤ 2 * Real.pi) (xi ^ 2)
  have hxi2 : Real.sqrt (xi ^ 2) = xi := by
    rw [Real.sqrt_sq_eq_abs]
    exact abs_of_nonneg hxi
  rw [hsqmul, hxi2]

-- --------------------------------------------------------------------------
-- K1. Gaussian kernel factor <= 1 at every z (centre is the maximum).
-- --------------------------------------------------------------------------
theorem gaussian_kernel_le_center (z xi : ℝ) (hx : xi ≠ 0) :
    Real.exp (-z ^ 2 / (2 * xi ^ 2)) ≤ 1 := by
  have hx2 : 0 < xi ^ 2 := by
    by_cases hp : 0 < xi
    · exact sq_pos_of_pos hp
    · have hn : xi < 0 := lt_of_le_of_ne (le_of_not_gt hp) hx
      exact sq_pos_of_neg hn
  have hd : 0 < 2 * xi ^ 2 := by nlinarith
  have hnum : 0 ≤ z ^ 2 := sq_nonneg z
  have harg : -z ^ 2 / (2 * xi ^ 2) ≤ 0 := by
    exact div_nonpos_of_nonpos_of_nonneg (neg_nonpos.mpr hnum) (le_of_lt hd)
  exact (Real.exp_le_exp_of_le harg).trans_eq Real.exp_zero

-- --------------------------------------------------------------------------
-- K2. Normalized kernel peak: G_xi(z) <= G_xi(0) for xi > 0.
-- --------------------------------------------------------------------------
theorem gaussian_kernel_peak (z xi : ℝ) (hx : xi ≠ 0) (_hxi : 0 < xi) :
    Real.exp (-z ^ 2 / (2 * xi ^ 2)) / Real.sqrt (2 * Real.pi * xi ^ 2)
      ≤ 1 / Real.sqrt (2 * Real.pi * xi ^ 2) := by
  have hle := gaussian_kernel_le_center z xi hx
  have hp : 0 < Real.sqrt (2 * Real.pi * xi ^ 2) :=
    Real.sqrt_pos.2 (by positivity : 0 < 2 * Real.pi * xi ^ 2)
  have hdif : (Real.exp (-z ^ 2 / (2 * xi ^ 2)) - 1) /
        Real.sqrt (2 * Real.pi * xi ^ 2) ≤ 0 := by
    exact div_nonpos_of_nonpos_of_nonneg (sub_nonpos.mpr hle) hp.le
  rw [← sub_nonpos]
  rwa [← sub_div]

-- --------------------------------------------------------------------------
-- A. Multiplier amplitude identity (algebraic form used in the tables):
--    exp(-(sigma^2/2) k^2) = exp(-sigma^2 k^2 / 2)
-- --------------------------------------------------------------------------
theorem multiplier_amplitude (sigma k : ℝ) :
    Real.exp (-(sigma ^ 2 / 2) * k ^ 2) = Real.exp (-(sigma ^ 2 * k ^ 2) / 2) := by
  congr 1
  ring

end AS048

-- axiom audit
#print axioms AS048.deviation_bound_exp
#print axioms AS048.mode_first_deriv
#print axioms AS048.mode_second_deriv
#print axioms AS048.heat_mode_rate
#print axioms AS048.gaussian_integral_norm
#print axioms AS048.gaussian_kernel_le_center
#print axioms AS048.gaussian_kernel_peak
#print axioms AS048.multiplier_amplitude