import Mathlib
import Mathlib.Tactic
noncomputable section
open Real
open scoped Topology Filter

/-
  AS081 -- Self-source and imposed baryon well are different (Lean 4 certificate).

  Framework (FRAMEWORK_CONTRACT): a0 = kappa c sqrt(G rho_Lambda), kappa = 1/2 ADOPTED
  as input; C = sqrt(G M_b a0); r_M = sqrt(G M_b / a0).  The seed's mathematical line:

      Delta(C ln r) = C / r^2  (r > 0),   rho_source = C / (4 pi G r^2).

  Certified contents (real analysis + real algebra; positivity of G, M_b, C, r,
  r_M, R, r_in, and r_in < R are the physical hypotheses):

    T0  deriv (fun x => C * log x) = C / r                 (first derivative)
    T1  second derivative of C * log r is -C / r^2
    T2  L[C * log] = C / r^2   where L f r := (deriv^2 f)(r) + (2/r) (deriv f)(r)
        (the 3-D radial Laplacian of a spherically symmetric potential)
    T3  deriv (-c * x^-1) = c / r^2                        (Newtonian term)
    T4  L[-G M_b / r] = 0                                  (harmonic in the exterior)
    T5  C / r^2 > 0 whenever 0 < C and 0 < r  -- the log-well Laplacian never vanishes
    T6  L[C * log] != L[-G M_b / r]  on r > 0  (the two wells are different objects)
    T7  laplace_add: L(f + g) = L f + L g (conditional on differentiability --
        the transfer identity used to detect an imposed baryon well)
    T8  no_imposed_baryon_log_well: if f = C * log (pointwise) and simultaneously
        f = -G M_b / r + h with L h = 0 (a harmonic completion -- the only way an
        imposed Newtonian baryon could produce the log well), then False.
        Regularity hypotheses (static-profile premises) are listed explicitly.
    T9  Poisson source: rho = C / (4 pi G r^2)  =>  4 pi G rho = C / r^2
    T10 enclosed phantom mass: 4 pi A r = C r / G at A = C / (4 pi G)
    T11 Gauss flux: 4 pi r^2 * (C / r) = 4 pi C r  = 4 pi G M_enc(< r)
    T12 single-radius coincidence: C r / G = M_b  <->  r = G M_b / C
    T13 equipartition inner edge: (G M_b) / C = r_M under C^2 = G M_b a0,
        r_M^2 = G M_b / a0  -- at r_M the phantom's own mass equals M_b
    T14 exterior dominance: M_b < C r / G for r > r_M (deep exterior mass grows)
    T15 negative control: at r = 2 r_M the enclosed mass is 2 M_b != M_b (capable
        of failing: a point baryon's enclosed mass is constant M_b)
    T16 finite-shell mass: M = 4 pi A (R - r_in) = C (R - r_in) / G, finite for
        r_in > 0 (both boundaries explicit)
    T17 dimensionless source invariant: rho r^2 / C = 1 / (4 pi G) -- the identity
        is scale-free in C, so it holds identically on BOTH acceleration footings

  Axiom bar: zero `sorry`; axioms subseteq {propext, Classical.choice, Quot.sound}.
-/

namespace AS081

def L (f : ℝ → ℝ) (r : ℝ) : ℝ := deriv (fun x : ℝ => deriv f x) r + (2 / r) * deriv f r

-- T0: first derivative of C * log
theorem deriv_const_log (C r : ℝ) (hr : r ≠ 0) : deriv (fun x : ℝ => C * Real.log x) r = C / r := by
  have h := (Real.hasDerivAt_log hr).const_mul C
  simpa [div_eq_mul_inv] using h.deriv

-- T1: second derivative of C * log (via the first-derivative function C / x)
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
    ring
  have hout : HasDerivAt (fun x : ℝ => deriv (fun y : ℝ => C * Real.log y) x) (-C / r ^ 2) r :=
    hc.congr_of_eventuallyEq hev
  exact hout.deriv

-- T2: the radial Laplacian of the log well
theorem laplace_log (C r : ℝ) (hr : r ≠ 0) : L (fun x : ℝ => C * Real.log x) r = C / r ^ 2 := by
  unfold L
  rw [second_deriv_const_log C r hr, deriv_const_log C r hr]
  ring_nf

-- T3: derivative of the Newtonian term -c / r
theorem deriv_const_inv_neg (c r : ℝ) (hr : r ≠ 0) : deriv (fun x : ℝ => -(c) * x⁻¹) r = c / r ^ 2 := by
  have hinv : HasDerivAt (fun x : ℝ => x⁻¹) (-(r ^ 2)⁻¹) r := by
    simpa using hasDerivAt_inv hr
  have hc : HasDerivAt (fun x : ℝ => (-c) * x⁻¹) ((-c) * (-(r ^ 2)⁻¹)) r := hinv.const_mul (-c)
  have hc' : HasDerivAt (fun x : ℝ => -(c) * x⁻¹) (c / r ^ 2) r := by
    convert hc using 1
    ring
  exact hc'.deriv

-- T4: the Newtonian term is harmonic in the exterior (radial Laplacian = 0)
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
  have hs : HasDerivAt ((fun x : ℝ => x⁻¹) ^ 2) (-(2 * r⁻¹ * (r ^ 2)⁻¹)) r := by
    simpa using (hinv.pow 2)
  have hcon : HasDerivAt (fun x : ℝ => (G * M_b) * (((fun y : ℝ => y⁻¹) ^ 2) x))
      ((G * M_b) * (-(2 * r⁻¹ * (r ^ 2)⁻¹))) r := hs.const_mul (G * M_b)
  have hxeq (x : ℝ) (hx : x ≠ 0) : G * M_b / x ^ 2 = G * M_b * (x⁻¹ ^ 2) := by
    rw [inv_pow x 2, div_eq_mul_inv]
  have heq2 : (fun x : ℝ => (G * M_b) / x ^ 2) =ᶠ[𝓝 r]
      (fun x : ℝ => (G * M_b) * (((fun y : ℝ => y⁻¹) ^ 2) x)) :=
    hnb.mono (fun x hx => by
      simpa using hxeq x hx)
  have hc2 : HasDerivAt (fun x : ℝ => (G * M_b) / x ^ 2)
      ((G * M_b) * (-(2 * r⁻¹ * (r ^ 2)⁻¹))) r :=
    hcon.congr_of_eventuallyEq heq2
  have hout : HasDerivAt (fun x : ℝ => deriv (fun y : ℝ => -(G * M_b) * y⁻¹) x)
      ((G * M_b) * (-(2 * r⁻¹ * (r ^ 2)⁻¹))) r := hc2.congr_of_eventuallyEq hev
  rw [hfirst, hout.deriv]
  ring_nf

-- T5: the log-well Laplacian is strictly positive on r > 0
theorem laplace_log_pos {C r : ℝ} (hC : 0 < C) (hr : 0 < r) : 0 < C / r ^ 2 :=
  div_pos hC (sq_pos_of_ne_zero (ne_of_gt hr))

-- T6: the two wells are different objects on r > 0
theorem wells_separate (C G M_b r : ℝ) (hC : 0 < C) (hr : 0 < r) :
    L (fun x : ℝ => C * Real.log x) r ≠
      L (fun x : ℝ => -(G * M_b) * x⁻¹) r := by
  rw [laplace_log C r (ne_of_gt hr), newton_laplace G M_b r (ne_of_gt hr)]
  exact ne_of_gt (laplace_log_pos hC hr)

-- T7: additivity of the radial Laplacian (transfer identity), conditional on
-- differentiability of f, g and of their first derivatives near r
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

-- T8: the log well cannot be an imposed baryon well (Newtonian term plus a
-- harmonic completion h with L h = 0) anywhere on r > 0
theorem no_imposed_baryon_log_well (C G M_b r : ℝ) (hC : 0 < C) (hr : 0 < r)
    (f h : ℝ → ℝ)
    (hmatch : f = fun x : ℝ => C * Real.log x)
    (hdec : f = fun x : ℝ => -(G * M_b) * x⁻¹ + h x)
    (hharm : L h r = 0)
    -- regularity of the Newtonian term and of h (static-profile premises):
    (hreg1e : ∀ᶠ x in 𝓝 r, DifferentiableAt ℝ (fun y : ℝ => -(G * M_b) * y⁻¹) x)
    (hreg2e : ∀ᶠ x in 𝓝 r, DifferentiableAt ℝ h x)
    (hreg1 : DifferentiableAt ℝ (fun y : ℝ => -(G * M_b) * y⁻¹) r)
    (hreg2 : DifferentiableAt ℝ h r)
    (hregh' : DifferentiableAt ℝ (deriv h) r)
    (hreg1' : DifferentiableAt ℝ (deriv (fun y : ℝ => -(G * M_b) * y⁻¹)) r) :
    False := by
  have hLf1 : L f r = C / r ^ 2 := by
    rw [hmatch]
    exact laplace_log C r (ne_of_gt hr)
  have hLf2 : L f r = L (fun x : ℝ => -(G * M_b) * x⁻¹) r + L h r := by
    rw [hdec]
    exact laplace_add (fun x : ℝ => -(G * M_b) * x⁻¹) h r hreg1e hreg2e hreg1 hreg2 hreg1' hregh'
  have hLzero : L f r = 0 := by
    rw [hLf2, newton_laplace G M_b r (ne_of_gt hr), hharm]
    ring
  rw [hLzero] at hLf1
  exact (ne_of_gt (laplace_log_pos hC hr)) hLf1.symm

-- T9: Poisson source identity
theorem poisson_source (C G r : ℝ) (hG : G ≠ 0) (hr : r ≠ 0) :
    4 * Real.pi * G * (C / (4 * Real.pi * G * r ^ 2)) = C / r ^ 2 := by
  field_simp [hG, hr, Real.pi_ne_zero]

-- T10: enclosed phantom mass at the profile amplitude A = C / (4 pi G)
theorem enclosed_mass (A C G r : ℝ) (hA : A = C / (4 * Real.pi * G)) (hG : G ≠ 0) :
    4 * Real.pi * A * r = C * r / G := by
  rw [hA]
  field_simp [hG, Real.pi_ne_zero]

-- T11: Gauss flux identity
theorem gauss_flux (C r : ℝ) (hr : r ≠ 0) :
    4 * Real.pi * r ^ 2 * (C / r) = 4 * Real.pi * C * r := by
  field_simp [hr]

-- T12: coincidence of the extended-source enclosed mass with the baryon mass
theorem coincidence_iff (C G M_b r : ℝ) (hC : C ≠ 0) (hG : G ≠ 0) :
    C * r / G = M_b ↔ r = G * M_b / C := by
  constructor
  · intro h
    field_simp [hC, hG] at h
    field_simp [hC, hG]
    rw [mul_comm] at h
    exact h
  · intro h
    rw [h]
    field_simp [hC, hG]

-- T13: under equipartition the phantom's own mass reaches M_b exactly at r_M:
-- the 'inner edge' r_b = G M_b / C equals r_M (C^2 = G M_b a0, r_M^2 = G M_b / a0)
theorem inner_edge_equipartition (C G M_b a0 rM : ℝ)
    (hC : C ^ 2 = G * M_b * a0) (hrM : rM ^ 2 = G * M_b / a0)
    (hG : 0 < G) (hMb : 0 < M_b) (ha0 : 0 < a0) (hCpos : 0 < C) (hrMpos : 0 < rM) :
    G * M_b / C = rM := by
  have h1 : (G * M_b / C) ^ 2 = rM ^ 2 := by
    rw [div_pow, hC, hrM]
    field_simp [ne_of_gt hG, ne_of_gt hMb, ne_of_gt ha0]
  have hpos : 0 < G * M_b / C := div_pos (mul_pos hG hMb) hCpos
  rcases (sq_eq_sq_iff_eq_or_eq_neg.mp h1) with h_eq | h_neg
  · exact h_eq
  · have hsum : 0 < G * M_b / C + rM := add_pos hpos hrMpos
    linarith [h_neg]

-- T14: in the deep exterior the extended source's enclosed mass strictly exceeds
-- the baryon mass (linear growth; the log well is not the baryon's well)
theorem exterior_mass_exceeds (C G M_b r rM : ℝ) (hG : G ≠ 0) (hrM : 0 < rM)
    (hMb : 0 < M_b) (hr : rM < r) (henc : M_b = C * rM / G) : M_b < C * r / G := by
  have h : C * r / G = M_b * (r / rM) := by
    rw [henc]
    field_simp [hG, ne_of_gt hrM]
  rw [h]
  exact (by simpa using mul_lt_mul_of_pos_left ((one_lt_div hrM).mpr hr) hMb)

-- T15: negative control (capable of failing): at r = 2 r_M the enclosed mass is
-- 2 M_b, never M_b -- a point baryon would keep M_b constant in r
theorem double_mass_negative_control (C G M_b rM : ℝ) (hG : G ≠ 0) (hrM : rM ≠ 0)
    (hMb : 0 < M_b) (henc : M_b = C * rM / G) : C * (2 * rM) / G ≠ M_b := by
  have h : C * (2 * rM) / G = 2 * M_b := by
    rw [henc]
    field_simp [hG, hrM]
  rw [h]
  nlinarith [hMb]

-- T16: finite-shell mass with both boundaries explicit (r_in > 0 <= r <= R)
theorem finite_shell_mass (A C G R r_in : ℝ) (hA : A = C / (4 * Real.pi * G))
    (hG : G ≠ 0) :
    4 * Real.pi * A * (R - r_in) = C * (R - r_in) / G := by
  rw [hA]
  field_simp [hG, Real.pi_ne_zero]

-- T17: dimensionless source invariant -- identical on BOTH acceleration footings
theorem source_invariant (C G r : ℝ) (rho : ℝ) (hC : C ≠ 0) (hG : G ≠ 0) (hr : r ≠ 0)
    (h : rho = C / (4 * Real.pi * G * r ^ 2)) : rho * r ^ 2 / C = 1 / (4 * Real.pi * G) := by
  rw [h]
  field_simp [hC, hG, hr, Real.pi_ne_zero]

end AS081