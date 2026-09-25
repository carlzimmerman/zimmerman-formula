import Mathlib

open Real

/-!
# L342 — the bound-region switch x = 9 R3/(4 K^2): algebraic certificates

SCOPE. Lean certifies the algebra of `real_research/g03_audit_2026/L342_bound_region_switch.py`: what the switch
variable equals on the linear FRW web and in a static bound system, that the linear web stays below any threshold
x_c > (3/2) Omega_m delta, and the truncation radius of an isothermal phantom.  The KiDS fit, the growth
integration and the SPARC numbers are not certified here, and the switch itself is a construction, not a derivation.

* `x_linear`: with K = 3H/c, R3 = 16 pi G rho_bar delta/c^2 (linearised Hamiltonian constraint, delta K = 0) and
  Omega_m = 8 pi G rho_bar/(3 H^2):  9 R3/(4 K^2) = (3/2) Omega_m delta.
* `x_static`: with R3 = 16 pi G rho/c^2 and K = 3H/c:  9 R3/(4 K^2) = 4 pi G rho/H^2.
* `linear_web_off`: if (3/2) Omega_m delta < x_c the switch is off.
* `truncation_radius`: for the deep-MOND phantom rho(r) = v^2/(4 pi G r^2), x(r) = x_c exactly when
  r^2 = v^2/(H^2 x_c).
-/

theorem x_linear {G c H rhob dl Om : ℝ} (hG : 0 < G) (hc : 0 < c) (hH : 0 < H)
    (hOm : Om = 8 * π * G * rhob / (3 * H ^ 2)) :
    9 * (16 * π * G * rhob * dl / c ^ 2) / (4 * (3 * H / c) ^ 2) = 3 / 2 * Om * dl := by
  rw [hOm]; field_simp; ring

theorem x_static {G c H rho : ℝ} (hc : 0 < c) (hH : 0 < H) :
    9 * (16 * π * G * rho / c ^ 2) / (4 * (3 * H / c) ^ 2) = 4 * π * G * rho / H ^ 2 := by
  field_simp; ring

theorem linear_web_off {Om dl xc : ℝ} (h : 3 / 2 * Om * dl < xc) : ¬ (xc ≤ 3 / 2 * Om * dl) := by
  push Not; exact h

theorem truncation_radius {G v H r xc : ℝ} (hG : 0 < G) (hv : 0 < v) (hH : 0 < H) (hr : 0 < r) (hxc : 0 < xc) :
    4 * π * G * (v ^ 2 / (4 * π * G * r ^ 2)) / H ^ 2 = xc ↔ r ^ 2 = v ^ 2 / (H ^ 2 * xc) := by
  have hπ : 0 < π := Real.pi_pos
  constructor
  · intro h
    have h' : v ^ 2 / (r ^ 2 * H ^ 2) = xc := by
      rw [← h]; field_simp
    field_simp
    rw [← h']; field_simp
  · intro h
    rw [h]; field_simp

#print axioms x_linear
#print axioms x_static
#print axioms linear_web_off
#print axioms truncation_radius
