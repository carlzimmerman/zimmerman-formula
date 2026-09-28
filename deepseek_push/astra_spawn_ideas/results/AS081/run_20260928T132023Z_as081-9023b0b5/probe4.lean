import Mathlib
import Mathlib.Tactic
noncomputable section
open Real
open scoped Filter

#check Filter.Eventually.and
#check DifferentiableAt.hasDerivAt
#check hasDerivAt_deriv_iff
#check DifferentiableAt.deriv

def L (f : ℝ → ℝ) (r : ℝ) : ℝ := deriv (fun x : ℝ => deriv f x) r + (2 / r) * deriv f r

theorem deriv_const_log (C r : ℝ) (hr : r ≠ 0) : deriv (fun x : ℝ => C * Real.log x) r = C / r := by
  have h := (Real.hasDerivAt_log hr).const_mul C
  simpa [div_eq_mul_inv] using h.deriv

theorem second_deriv_const_log (C r : ℝ) (hr : r ≠ 0) :
    deriv (fun x : ℝ => deriv (fun y : ℝ => C * Real.log y) x) r = -C / r ^ 2 := by
  have hnb : ∀ᶠ x in 𝓝 r, x ≠ 0 := (isOpen_compl_singleton (x := 0)).mem_nhds hr
  have hev : (fun x : ℝ => deriv (fun y : ℝ => C * Real.log y) x) =ᶠ[𝓝 r] (fun x : ℝ => C / x) :=
    hnb.mono (fun x hx => deriv_const_log C x hx)
  have hinv : HasDerivAt (fun x : ℝ => x⁻¹) (-(r ^ 2)⁻¹) r := by
    simpa using hasDerivAt_inv hr
  have hc0 : HasDerivAt (fun x : ℝ => C / x) (C * (-(r ^ 2)⁻¹)) r := by
    simpa [div_eq_mul_inv] using hinv.const_mul C
  have hc : HasDerivAt (fun x : ℝ => C / x) (-C / r ^ 2) r := by
    convert hc0 using 1
  have hout : HasDerivAt (fun x : ℝ => deriv (fun y : ℝ => C * Real.log y) x) (-C / r ^ 2) r :=
    hc.congr_of_eventuallyEq hev
  exact hout.deriv

theorem laplace_log (C r : ℝ) (hr : r ≠ 0) : L (fun x : ℝ => C * Real.log x) r = C / r ^ 2 := by
  unfold L
  rw [second_deriv_const_log C r hr, deriv_const_log C r hr]
  ring_nf

theorem deriv_const_inv_neg (c r : ℝ) (hr : r ≠ 0) : deriv (fun x : ℝ => -(c) * x⁻¹) r = c / r ^ 2 := by
  have hinv : HasDerivAt (fun x : ℝ => x⁻¹) (-(r ^ 2)⁻¹) r := by
    simpa using hasDerivAt_inv hr
  have hc : HasDerivAt (fun x : ℝ => (-c) * x⁻¹) ((-c) * (-(r ^ 2)⁻¹)) r := hinv.const_mul (-c)
  have hc' : HasDerivAt (fun x : ℝ => -(c) * x⁻¹) (c / r ^ 2) r := by
    convert hc using 1
  exact hc'.deriv

theorem newton_laplace (G M_b r : ℝ) (hr : r ≠ 0) :
    L (fun x : ℝ => -(G * M_b) * x⁻¹) r = 0 := by
  unfold L
  have hfirst : deriv (fun x : ℝ => -(G * M_b) * x⁻¹) r = (G * M_b) / r ^ 2 :=
    deriv_const_inv_neg (G * M_b) r hr
  have hnb : ∀ᶠ x in 𝓝 r, x ≠ 0 := (isOpen_compl_singleton (x := 0)).mem_nhds hr
  have hev : (fun x : ℝ => deriv (fun y : ℝ => -(G * M_b) * y⁻¹) x) =ᶠ[𝓝 r]
      (fun x : ℝ => (G * M_b) / x ^ 2) :=
    hnb.mono (fun x hx => deriv_const_inv_neg (G * M_b) x hx)
  have hinv : HasDerivAt (fun x : ℝ => x⁻¹) (-(r ^ 2)⁻¹) r := by
    simpa using hasDerivAt_inv hr
  have hs : HasDerivAt (fun x : ℝ => (x⁻¹) ^ 2) (2 * r⁻¹ * (-(r ^ 2)⁻¹)) r := hinv.pow 2
  have hcon : HasDerivAt (fun x : ℝ => (G * M_b) * (x⁻¹) ^ 2)
      ((G * M_b) * (2 * r⁻¹ * (-(r ^ 2)⁻¹))) r := hs.const_mul (G * M_b)
  have hc : HasDerivAt (fun x : ℝ => (G * M_b) * (x⁻¹) ^ 2) (-(G * M_b) * 2 / r ^ 3) r := by
    convert hcon using 1
  have heq2 : (fun x : ℝ => (G * M_b) * (x⁻¹) ^ 2) =ᶠ[𝓝 r] (fun x : ℝ => (G * M_b) / x ^ 2) :=
    hnb.mono (fun x hx => by
      field_simp [hx]
      ring)
  have hc2 : HasDerivAt (fun x : ℝ => (G * M_b) / x ^ 2) (-(G * M_b) * 2 / r ^ 3) r :=
    hc.congr_of_eventuallyEq heq2
  have hout : HasDerivAt (fun x : ℝ => deriv (fun y : ℝ => -(G * M_b) * y⁻¹) x)
      (-(G * M_b) * 2 / r ^ 3) r := hc2.congr_of_eventuallyEq hev
  rw [hfirst, hout.deriv]
  field_simp [hr]
  ring

theorem laplace_add (f g : ℝ → ℝ) (r : ℝ)
    (hdfe : ∀ᶠ x in 𝓝 r, DifferentiableAt ℝ f x)
    (hdge : ∀ᶠ x in 𝓝 r, DifferentiableAt ℝ g x)
    (hdf : DifferentiableAt ℝ f r) (hdg : DifferentiableAt ℝ g r)
    (hdf' : DifferentiableAt ℝ (deriv f) r) (hdg' : DifferentiableAt ℝ (deriv g) r) :
    L (fun x => f x + g x) r = L f r + L g r := by
  unfold L
  have h1e : ∀ᶠ x in 𝓝 r, deriv (fun y : ℝ => f y + g y) x = deriv f x + deriv g x :=
    hdfe.and hdge |>.mono (fun x hx => deriv_add hx.1 hx.2)
  have h2 : HasDerivAt (fun x : ℝ => deriv f x + deriv g x)
      (deriv (fun x : ℝ => deriv f x) r + deriv (fun x : ℝ => deriv g x) r) r :=
    hdf'.hasDerivAt.add hdg'.hasDerivAt
  have h3 : HasDerivAt (fun x : ℝ => deriv (fun y : ℝ => f y + g y) x)
      (deriv (fun x : ℝ => deriv f x) r + deriv (fun x : ℝ => deriv g x) r) r :=
    h2.congr_of_eventuallyEq h1e
  have h4 : deriv (fun y : ℝ => f y + g y) r = deriv f r + deriv g r := deriv_add hdf hdg
  rw [h3.deriv, h4]
  ring