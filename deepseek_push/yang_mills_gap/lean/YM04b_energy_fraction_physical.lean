import Mathlib

/-!
# YM04b -- THE PHYSICAL ENERGY FRACTION SPINE (the corrected register)

Scope statement (as every certificate in this repo reads): Lean certifies the
MATHEMATICS. The physics premises -- the phantom density rho_ph = sqrt(G M_b
a0)/(4 pi G r^2) (the committed L4 profile, dust-dominated: rho_ph(R0) ~ 1e5
x Lambda^4), the vector's halo energy E_A = mu_2(u) u^2 Lambda^4 (YM04 check
1) and the derived closed form eps_phys(u) = C * mu_2(u) * u (YM04b,
deepseek_push/yang_mills_gap/YM04b_vector_halo_physical.py, 6/6) -- are the
committed lanes' claims. YM04's k-essence-form register (15/15) is SUPERSEDED
by YM04b (its denominator misidentified the phantom density by ~1e5); the
tensor algebra (alpha_A = -2, P_r - P_t = +2 E_A) is register-independent and
survives. This file certifies the physical register's algebraic spine:
the cleared identity, positivity, the vacuum closing, and the numeric band at
the Sun's u.

The coefficient C = 3.046396e-6 carries the r(u)-mapping convention of the
YM04b lane; the band below (1e-8, 1e-5) is robust under either committed map
(YM01's flat-curve map gives eps(8.2) ~ 1.0e-7, the lane's point-mass map
gives 9.3e-7 -- both inside).
-/
noncomputable section

noncomputable def mu2 (u : ℝ) : ℝ := u * (2 + u) / (1 + u)^2
noncomputable def eps_phys (C u : ℝ) : ℝ := C * mu2 u * u

/-- the cleared identity: (1+u)^2 * eps_phys = C u^2 (2+u) --/
theorem eps_phys_cleared (C u : ℝ) (hu : 0 < u) :
    (1 + u)^2 * eps_phys C u = C * u^2 * (2 + u) := by
  unfold eps_phys mu2
  have hne : (1 + u)^2 ≠ 0 := by positivity
  field_simp [hne]

/-- positivity: 0 < C -> 0 < u -> 0 < eps_phys --/
theorem eps_phys_pos (C u : ℝ) (hC : 0 < C) (hu : 0 < u) : 0 < eps_phys C u := by
  unfold eps_phys mu2
  have h2u : 0 < 2 + u := by linarith [hu]
  have hnum : 0 < u * (2 + u) := mul_pos hu h2u
  have hden : 0 < (1 + u)^2 := by nlinarith [hu]
  simpa [mul_assoc] using mul_pos hC (mul_pos (div_pos hnum hden) hu)

/-- the vacuum closing: no gradient, no vector energy --/
theorem eps_phys_zero (C : ℝ) : eps_phys C 0 = 0 := by
  unfold eps_phys mu2
  norm_num

/-- the numeric band at the Sun: with the fiducial C = 3.046396e-6 and the
    Sun's u = 0.2276, the energy fraction lands in (1e-8, 1e-5) -- the
    10^-7 class, six orders below any committed direction-test sensitivity -/
theorem eps_phys_sun_band :
    1 / 10^8 < eps_phys (3046396 / 10^12) (2276 / 10000) ∧
    eps_phys (3046396 / 10^12) (2276 / 10000) < 1 / 10^5 := by
  constructor
  · unfold eps_phys mu2
    norm_num
  · unfold eps_phys mu2
    norm_num

end
#print axioms eps_phys_cleared
#print axioms eps_phys_pos
#print axioms eps_phys_zero
#print axioms eps_phys_sun_band