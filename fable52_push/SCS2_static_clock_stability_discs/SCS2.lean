/-
SCS2 (criteria 158c4cf770): Lean statements for the closed forms the disc lane uses. They certify algebra and inequalities,
not the physics. TEST lane; adopts nothing. kappa = 1/2 FITTED; not theory closed.

  lagrange3            : (p^2+q^2+r^2)(a^2+b^2+c^2) - (pa+qb+rc)^2 = (pb-qa)^2 + (pc-ra)^2 + (qc-rb)^2.
  aniso_kinetic_pos    : with |ghat| = 1, J_perp |v|^2 + (J_par - J_perp)(ghat.v)^2 >= min(J_par, J_perp)|v|^2 > 0 for v /= 0:
                         the law's kinetic form is positive in every direction, whatever the field's direction.
  Km_lt_one            : c^2/(1+u)^2 + s^2/(1+u) < 1 for u > 0, c^2 + s^2 = 1 (every direction).
  sign_omega2          : at mu_K = 0, omega^2 = G (1 - K m)/m has the sign of G when 0 < K m < 1.
  quotient_neg         : H-quotient: q_H(z) > 0 and q_L(z) < 0 give a negative Rayleigh quotient (the 3D test's step).
  nu_antitone          : nu(y) = 1/2 + sqrt(1/4 + 1/y) is antitone on y > 0 (so the law's halo of a point mass, displaced or
                         not, has a positive phantom density: nu grows outward).
  law_solves           : u = nu(y) y solves u^2/(1+u) = y (the law's magnitude, used for Kuzmin's image field).
  far_field_exponent   : for mu(x) = x/(1+x), x mu'(x)/mu(x) = 1/(1+x) = L_e (the external-field boundary).
  kuzmin_sheet         : the image point mass at depth a gives the surface density M a / (2 pi (R^2 + a^2)^(3/2)).
  quotient_nonneg      : the Rayleigh step's other half (nonnegative numerator, positive H-form: nonnegative quotient).
  stiffness_unbounded  : with the stiffness on and G < 0, omega^2 = G (1 + g m k2 - K m)/m falls below any bound in k2
                         (SCS1's statement, copied).
  farfield_band_negative / farfield_cone_positive : the sign of the external field's far-field phantom,
                         K D.P = -L A [r_perp^2 - 2 z^2/(1+L)]/((1+L) s^5): negative in the band, positive in the axis cones.
(The last four were added after the first compile, with the twin's two matching false versions; compile.txt is the
recompile of the whole file.)
-/
import Mathlib

namespace SCS2

theorem lagrange3 (p q r a b c : ℝ) :
    (p ^ 2 + q ^ 2 + r ^ 2) * (a ^ 2 + b ^ 2 + c ^ 2) - (p * a + q * b + r * c) ^ 2
      = (p * b - q * a) ^ 2 + (p * c - r * a) ^ 2 + (q * c - r * b) ^ 2 := by ring

theorem aniso_kinetic_pos (p q r a b c Jpar Jperp : ℝ) (hg : p ^ 2 + q ^ 2 + r ^ 2 = 1)
    (hpar : 0 < Jpar) (hperp : 0 < Jperp) (hv : a ^ 2 + b ^ 2 + c ^ 2 ≠ 0) :
    0 < Jperp * (a ^ 2 + b ^ 2 + c ^ 2) + (Jpar - Jperp) * (p * a + q * b + r * c) ^ 2 := by
  have hcs : (p * a + q * b + r * c) ^ 2 ≤ a ^ 2 + b ^ 2 + c ^ 2 := by
    have := lagrange3 p q r a b c
    rw [hg, one_mul] at this
    nlinarith [sq_nonneg (p * b - q * a), sq_nonneg (p * c - r * a), sq_nonneg (q * c - r * b)]
  have hpos : 0 < a ^ 2 + b ^ 2 + c ^ 2 := by
    rcases lt_or_eq_of_le (by positivity : (0 : ℝ) ≤ a ^ 2 + b ^ 2 + c ^ 2) with h | h
    · exact h
    · exact absurd h.symm hv
  have hs : 0 ≤ (p * a + q * b + r * c) ^ 2 := sq_nonneg _
  -- the form equals Jperp (|v|^2 - s^2) + Jpar s^2
  have e : Jperp * (a ^ 2 + b ^ 2 + c ^ 2) + (Jpar - Jperp) * (p * a + q * b + r * c) ^ 2
      = Jperp * ((a ^ 2 + b ^ 2 + c ^ 2) - (p * a + q * b + r * c) ^ 2) + Jpar * (p * a + q * b + r * c) ^ 2 := by ring
  rw [e]
  rcases lt_or_eq_of_le hs with h | h
  · have h1 : 0 ≤ Jperp * ((a ^ 2 + b ^ 2 + c ^ 2) - (p * a + q * b + r * c) ^ 2) :=
      mul_nonneg hperp.le (by linarith)
    nlinarith
  · rw [← h]; simp; exact mul_pos hperp hpos

theorem Km_lt_one (u c s : ℝ) (hu : 0 < u) (hcs : c ^ 2 + s ^ 2 = 1) :
    c ^ 2 / (1 + u) ^ 2 + s ^ 2 / (1 + u) < 1 := by
  have h1 : (0 : ℝ) < 1 + u := by linarith
  have hc : c ^ 2 / (1 + u) ^ 2 ≤ c ^ 2 / (1 + u) := by
    apply div_le_div_of_nonneg_left (sq_nonneg c) h1; nlinarith
  have hlt : (c ^ 2 + s ^ 2) / (1 + u) < 1 := by rw [hcs, div_lt_one h1]; linarith
  have : c ^ 2 / (1 + u) + s ^ 2 / (1 + u) = (c ^ 2 + s ^ 2) / (1 + u) := by ring
  linarith

theorem sign_omega2 (G Km m : ℝ) (hm : 0 < m) (hK0 : 0 < Km) (hK1 : Km < 1) :
    (0 < G * (1 - Km) / m ↔ 0 < G) ∧ (G * (1 - Km) / m < 0 ↔ G < 0) := by
  have h1 : 0 < 1 - Km := by linarith
  constructor
  · constructor
    · intro h
      by_contra hG0; have hG : G ≤ 0 := not_lt.mp hG0
      have : G * (1 - Km) / m ≤ 0 := div_nonpos_of_nonpos_of_nonneg (mul_nonpos_of_nonpos_of_nonneg hG h1.le) hm.le
      linarith
    · intro hG; positivity
  · constructor
    · intro h
      by_contra hG0; have hG : 0 ≤ G := not_lt.mp hG0
      have : 0 ≤ G * (1 - Km) / m := div_nonneg (mul_nonneg hG h1.le) hm.le
      linarith
    · intro hG; exact div_neg_of_neg_of_pos (mul_neg_of_neg_of_pos hG h1) hm

theorem quotient_neg (qL qH : ℝ) (hH : 0 < qH) (hL : qL < 0) : qL / qH < 0 := div_neg_of_neg_of_pos hL hH

noncomputable def nu (y : ℝ) : ℝ := 1 / 2 + Real.sqrt (1 / 4 + 1 / y)

theorem nu_antitone : AntitoneOn nu (Set.Ioi 0) := by
  intro y₁ h₁ y₂ h₂ h12
  have hy1 : (0 : ℝ) < y₁ := h₁
  unfold nu
  have : 1 / y₂ ≤ 1 / y₁ := one_div_le_one_div_of_le hy1 h12
  have : Real.sqrt (1 / 4 + 1 / y₂) ≤ Real.sqrt (1 / 4 + 1 / y₁) := Real.sqrt_le_sqrt (by linarith)
  linarith

theorem law_solves (y : ℝ) (hy : 0 < y) : (nu y * y) ^ 2 / (1 + nu y * y) = y := by
  have hs : (0 : ℝ) ≤ 1 / 4 + 1 / y := by positivity
  have hsq : Real.sqrt (1 / 4 + 1 / y) ^ 2 = 1 / 4 + 1 / y := Real.sq_sqrt hs
  have hs0 : 0 ≤ Real.sqrt (1 / 4 + 1 / y) := Real.sqrt_nonneg _
  unfold nu
  set s := Real.sqrt (1 / 4 + 1 / y) with hsdef
  have hpos : 0 < 1 + (1 / 2 + s) * y := by positivity
  have hsy : s ^ 2 * y = y / 4 + 1 := by rw [hsq]; field_simp
  rw [div_eq_iff hpos.ne']
  nlinarith [hsy]

theorem far_field_exponent (x : ℝ) (hx : 0 < x) :
    x * (1 / (1 + x) ^ 2) / (x / (1 + x)) = 1 / (1 + x) := by
  have h1 : (0 : ℝ) < 1 + x := by linarith
  field_simp

theorem kuzmin_sheet (G M a R : ℝ) (hG : G ≠ 0) (hpos : 0 < R ^ 2 + a ^ 2) :
    (G * M * a / (R ^ 2 + a ^ 2) ^ ((3 : ℝ) / 2)) / (2 * Real.pi * G)
      = M * a / (2 * Real.pi * (R ^ 2 + a ^ 2) ^ ((3 : ℝ) / 2)) := by
  have hp : (0 : ℝ) < (R ^ 2 + a ^ 2) ^ ((3 : ℝ) / 2) := Real.rpow_pos_of_pos hpos _
  have hpi : (0 : ℝ) < Real.pi := Real.pi_pos
  field_simp

/-- the quotient's other half: a nonnegative numerator over a positive H-form gives a nonnegative quotient (so with
    H > 0 the sign of lambda_min is the sign of min zeta.(-C).zeta). -/
theorem quotient_nonneg (qL qH : ℝ) (hH : 0 < qH) (hL : 0 ≤ qL) : 0 ≤ qL / qH := div_nonneg hL hH.le

/-- the stiffness bracket (SCS1's statement, copied, not imported): with gamma_L on, omega^2 = G (1 + g m k2 - K m)/m
    falls below any bound as k2 grows when G < 0. -/
theorem stiffness_unbounded (K G m g : ℝ) (hG : G < 0) (hm : 0 < m) (hg : 0 < g * m) (B : ℝ) :
    ∃ k2 : ℝ, 0 ≤ k2 ∧ G * (1 + g * m * k2 - K * m) / m < B := by
  set c := G * (1 - K * m) / m with hc
  have hslope : G * g < 0 := by
    have : 0 < g := by
      rcases lt_or_ge 0 g with h | h
      · exact h
      · nlinarith
    nlinarith
  refine ⟨max 0 ((B - c) / (G * g) + 1), le_max_left _ _, ?_⟩
  have hexp : G * (1 + g * m * (max 0 ((B - c) / (G * g) + 1)) - K * m) / m
      = c + G * g * (max 0 ((B - c) / (G * g) + 1)) := by
    rw [hc]; field_simp; ring
  rw [hexp]
  have hge : (B - c) / (G * g) + 1 ≤ max 0 ((B - c) / (G * g) + 1) := le_max_right _ _
  have h2 : G * g * (max 0 ((B - c) / (G * g) + 1)) ≤ G * g * ((B - c) / (G * g) + 1) :=
    mul_le_mul_of_nonpos_left hge hslope.le
  have hne : G * g ≠ 0 := hslope.ne
  have h3 : G * g * ((B - c) / (G * g) + 1) = (B - c) + G * g := by
    rw [mul_add, mul_div_cancel₀ _ hne, mul_one]
  linarith

/-- the external field's far-field band (scs2_farfield.py): K D.P = -L A [rp2 - 2 z^2/(1+L)]/((1+L) s5) is negative
    wherever rp2 > 2 z^2/(1+L), for A, L, s5 > 0 (the band around the plane perpendicular to the field). -/
theorem farfield_band_negative (A L s5 rp2 z : ℝ) (hA : 0 < A) (hL : 0 < L) (hs : 0 < s5)
    (hband : 2 * z ^ 2 / (1 + L) < rp2) :
    -L * A * (rp2 - 2 * z ^ 2 / (1 + L)) / ((1 + L) * s5) < 0 := by
  have h1 : 0 < rp2 - 2 * z ^ 2 / (1 + L) := by linarith
  have h2 : 0 < (1 + L) * s5 := by positivity
  have h3 : -L * A * (rp2 - 2 * z ^ 2 / (1 + L)) < 0 := by
    have : 0 < L * A * (rp2 - 2 * z ^ 2 / (1 + L)) := by positivity
    linarith
  exact div_neg_of_neg_of_pos h3 h2

/-- and positive in the cones along the field's axis, rp2 < 2 z^2/(1+L). -/
theorem farfield_cone_positive (A L s5 rp2 z : ℝ) (hA : 0 < A) (hL : 0 < L) (hs : 0 < s5)
    (hcone : rp2 < 2 * z ^ 2 / (1 + L)) :
    0 < -L * A * (rp2 - 2 * z ^ 2 / (1 + L)) / ((1 + L) * s5) := by
  have h1 : 0 < 2 * z ^ 2 / (1 + L) - rp2 := by linarith
  have h2 : 0 < (1 + L) * s5 := by positivity
  have h3 : 0 < -L * A * (rp2 - 2 * z ^ 2 / (1 + L)) := by
    have : 0 < L * A * (2 * z ^ 2 / (1 + L) - rp2) := by positivity
    linarith
  exact div_pos h3 h2

end SCS2

#print axioms SCS2.quotient_nonneg
#print axioms SCS2.stiffness_unbounded
#print axioms SCS2.farfield_band_negative
#print axioms SCS2.farfield_cone_positive
#print axioms SCS2.lagrange3
#print axioms SCS2.aniso_kinetic_pos
#print axioms SCS2.Km_lt_one
#print axioms SCS2.sign_omega2
#print axioms SCS2.quotient_neg
#print axioms SCS2.nu_antitone
#print axioms SCS2.law_solves
#print axioms SCS2.far_field_exponent
#print axioms SCS2.kuzmin_sheet

-- kappa = 1/2 FITTED; not theory closed. Adopts nothing.
