import Mathlib
import Mathlib.Tactic
noncomputable section
open Real

#check hasDerivAt_id
#check DifferentiableAt.deriv_hasDerivAt
#check DifferentiableAt.deriv
#check isOpen_compl_singleton
#check HasDerivAt.add
#check Real.log_div
#check Real.log_div'
#check one_lt_div
#check mul_lt_mul_of_pos_left

-- test 1: full laplace of C*log r
def L (f : ℝ → ℝ) (r : ℝ) : ℝ := deriv (fun x : ℝ => deriv f x) r + (2 / r) * deriv f r

theorem deriv_const_log (C r : ℝ) (hr : r ≠ 0) : deriv (fun x : ℝ => C * Real.log x) r = C / r := by
  have h := (Real.hasDerivAt_log hr).const_mul C
  simpa [div_eq_mul_inv] using h.deriv

theorem second_deriv_const_log (C r : ℝ) (hr : r ≠ 0) :
    deriv (fun x : ℝ => deriv (fun y : ℝ => C * Real.log y) x) r = -C / r ^ 2 := by
  have hnb : ∀ᶠ x in 𝓝 r, x ≠ 0 := (isOpen_compl_singleton (a := 0)).mem_nhds hr
  have hev : (fun x : ℝ => deriv (fun y : ℝ => C * Real.log y) x) =ᶠ[𝓝 r] (fun x : ℝ => C / x) :=
    hnb.mono (fun x hx => deriv_const_log C x hx)
  have hinv : HasDerivAt (fun x : ℝ => x⁻¹) (-1 / r ^ 2) r := by
    simpa using (hasDerivAt_id r).inv hr
  have hval : C * (-1 / r ^ 2) = -C / r ^ 2 := by ring
  have hc : HasDerivAt (fun x : ℝ => C / x) (C * (-1 / r ^ 2)) r := by
    simpa [div_eq_mul_inv] using hinv.const_mul C
  have hc' : HasDerivAt (fun x : ℝ => C / x) (-C / r ^ 2) r := by
    convert hc using 1
    exact hval
  have hout : HasDerivAt (fun x : ℝ => deriv (fun y : ℝ => C * Real.log y) x) (-C / r ^ 2) r :=
    hc'.congr_of_eventuallyEq hev
  exact hout.deriv

theorem laplace_log (C r : ℝ) (hr : r ≠ 0) : L (fun x : ℝ => C * Real.log x) r = C / r ^ 2 := by
  unfold L
  rw [second_deriv_const_log C r hr, deriv_const_log C r hr]
  ring_nf

-- test 2: laplace of the newtonian term is zero
theorem deriv_const_inv_neg (c r : ℝ) (hr : r ≠ 0) : deriv (fun x : ℝ => -(c) * x⁻¹) r = c / r ^ 2 := by
  have hinv : HasDerivAt (fun x : ℝ => x⁻¹) (-1 / r ^ 2) r := by
    simpa using (hasDerivAt_id r).inv hr
  have hc : HasDerivAt (fun x : ℝ => (-c) * x⁻¹) ((-c) * (-1 / r ^ 2)) r := hinv.const_mul (-c)
  have hval : (-c) * (-1 / r ^ 2) = c / r ^ 2 := by ring
  have hc' : HasDerivAt (fun x : ℝ => -(c) * x⁻¹) (c / r ^ 2) r := by
    convert hc using 1
    exact hval
  exact hc'.deriv

theorem newton_laplace (G M_b r : ℝ) (hr : r ≠ 0) :
    L (fun x : ℝ => -(G * M_b) * x⁻¹) r = 0 := by
  unfold L
  -- second derivative of -(c) * x⁻¹ is -(c)/r^2
  have hfirst : deriv (fun x : ℝ => -(G * M_b) * x⁻¹) r = (G * M_b) / r ^ 2 :=
    deriv_const_inv_neg (G * M_b) r hr
  have hnb : ∀ᶠ x in 𝓝 r, x ≠ 0 := (isOpen_compl_singleton (a := 0)).mem_nhds hr
  have hev : (fun x : ℝ => deriv (fun y : ℝ => -(G * M_b) * y⁻¹) x) =ᶠ[𝓝 r]
      (fun x : ℝ => (G * M_b) / x ^ 2) :=
    hnb.mono (fun x hx => (deriv_const_inv_neg (G * M_b) x hx))
  -- HasDerivAt of (fun x => (G*M_b) / x^2): = const * (x^-1)^2; value -2 c / r^3
  have hinv : HasDerivAt (fun x : ℝ => x⁻¹) (-1 / r ^ 2) r := by
    simpa using (hasDerivAt_id r).inv hr
  have hs : HasDerivAt (fun x : ℝ => (x⁻¹) ^ 2) (-2 * (r⁻¹) ^ 3) r := by
    -- derivative of (x⁻¹)^2 via pow: HasDerivAt.pow
    have hp := hinv.pow 2
    -- hp : HasDerivAt (fun x => (x⁻¹)^2) (2 * (-1 / r^2) * (r⁻¹)^1) r
    simpa using hp
  have hcon : HasDerivAt (fun x : ℝ => (G * M_b) / x ^ 2) (-2 * (G * M_b) * r⁻¹ ^ 3) r := by
    simpa [div_eq_mul_inv] using hs.const_mul (G * M_b)
  have hval : -2 * (G * M_b) * r⁻¹ ^ 3 = -(G * M_b) * 2 / r ^ 3 := by
    field_simp [hr]
    ring
  have hc' : HasDerivAt (fun x : ℝ => (G * M_b) / x ^ 2) (-(G * M_b) * 2 / r ^ 3) r := by
    convert hcon using 1
    exact hval
  have hout : HasDerivAt (fun x : ℝ => deriv (fun y : ℝ => -(G * M_b) * y⁻¹) x)
      (-(G * M_b) * 2 / r ^ 3) r := hc'.congr_of_eventuallyEq hev
  rw [hfirst, hout.deriv]
  field_simp [hr]
  ring