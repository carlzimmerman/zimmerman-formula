/-
  G007 -- the bimetric door: the Lean certificate of the algebra that decided it.

  The lane's verdict is CLOSED (gate 1, lensing; glm53_push/G007_bimetric_door.out,
  14/16 checks).  This file certifies the EXACT algebra the decision rests on --
  nothing regime-dependent, nothing numerical.  Physical verdicts are the
  committed Python lane's; Lean certifies mathematics, not physics.

  Certified here (check ids refer to the .out):
    lensing_sum_cancellation (B1)  : the composite frame's potentials
      Phi~ = Phi + c/2, Psi~ = Psi - c/2 sum to Phi + Psi -- the scalar's
      conformal lever contributes IDENTICALLY ZERO to the lensing sum, for any
      shape of C(X).  (L241's barrier, in the bimetric frame.)
    disformal_entries (B2)         : the outer product (d_m phi)(d_n phi) of a
      static radial gradient is nonzero ONLY in the rr entry -- the disformal
      lever enters neither ghat_00 (the force channel) nor the angular metric
      (the lensing channel).  Dual-inert, exactly.
    one_minus_mu2_eq (C1)          : 1 - mu_2(y) = 1/(1+y)^2 for y ≠ -1 -- the
      kernel-inertness form behind the solar-system gamma pass.
    sqrt_ratio, stress_vs_phantom_ratio (C3) :
      the deep-MOND stress/phantom density ratio is exactly (4 pi/3)(r_s/r)
      with r_s = 2GM/c^2 -- the scalar's stress loses to the phantom by r/r_s
      ~ 1e6 at galactic radii; no coefficient choice reverses a 1/r law.
    mu2_pos, phantom_kinetic_sign (D3) :
      mu_2 > 0 on the MOND branch, so the OneFunction's timelike fluctuation
      coefficient -M^4 mu_2/s^2 is NEGATIVE: the phantom sign (G002's V1
      identity F' = +mu_2).
    flip_vacuum, flip_kinetic_healthy, cs2_at_origin (D3) :
      the repair F_h = -F - 2 preserves the vacuum value F_h(0) = -1 (the
      dark-energy identification) and flips the kinetic sign healthy, at the
      recorded cost c_s^2(0) = 2 (superluminal by sqrt 2 in the deep limit).
    deep_mond_law (E1)             : the slope-2 deep law gives g^2 = (s/2) g_N
      -- the 1/2 power and a_0 = s/2 survive the chassis (G002 V7's cleared
      form, restated for this lane).

  mu_2 is carried in its rational form (2y + y^2)/(1 + y)^2, identical to
  1 - (1+y)^(-2) for y ≠ -1 (one_minus_mu2_eq below; G002 V1's sympy residual
  was exactly zero).
-/
import Mathlib

noncomputable section

/-- The measured interpolating function (SPARC-selected member, L232), rational
form; identical to 1 - (1+y)^(-2) wherever y ≠ -1. -/
def mu2 (y : ℝ) : ℝ := (2 * y + y ^ 2) / (1 + y) ^ 2

/-- The OneFunction of G002: f(X) = X - 2 ln(1+sqrt X) - 2/(1+sqrt X) + 1. -/
def f (X : ℝ) : ℝ := X - 2 * Real.log (1 + Real.sqrt X) - 2 / (1 + Real.sqrt X) + 1

/-! ## B1 -- the lensing-sum cancellation (the frame barrier) -/

/-- The physical potentials read off the composite metric ghat = C(X) g with
C = 1 + c (linear order in the frame field; L241 V1's instrument). -/
def phiT (Phi c : ℝ) : ℝ := Phi + c / 2

/-- See `phiT`. -/
def psiT (Psi c : ℝ) : ℝ := Psi - c / 2

/-- **G007 B1.** The lensing (deflection-governing) sum is UNTOUCHED by the
conformal lever: the c-terms shift Phi~ up and Psi~ down by the same amount
and cancel identically, for any value of c. -/
theorem lensing_sum_cancellation (Phi Psi c : ℝ) :
    phiT Phi c + psiT Psi c = Phi + Psi := by
  unfold phiT psiT
  ring

/-! ## B2 -- the disformal lever is radial -/

/-- A static radial scalar gradient: d_mu phi = (0, phi', 0, 0). -/
def gradStatic : Fin 4 → ℝ := ![0, 1, 0, 0]

/-- The disformal building block (d_m phi)(d_n phi) as a matrix. -/
def outerM (v : Fin 4 → ℝ) : Matrix (Fin 4) (Fin 4) ℝ := Matrix.of fun i j => v i * v j

/-- **G007 B2.** The outer product of a static radial gradient has its ONLY
nonzero entry in the rr component: the disformal term enters neither the time
component (the static matter force's channel) nor the angular components (the
lensing channel). -/
theorem disformal_entries :
    (outerM gradStatic) 0 0 = 0 ∧ (outerM gradStatic) 0 2 = 0 ∧
      (outerM gradStatic) 2 2 = 0 ∧ (outerM gradStatic) 3 3 = 0 ∧
      (outerM gradStatic) 1 1 = 1 := by
  unfold outerM gradStatic
  norm_num [Matrix.of_apply]
  simp

/-! ## C1 -- kernel inertness (the solar-system gamma form) -/

/-- **G007 C1.** 1 - mu_2(y) = 1/(1+y)^2 for y ≠ -1: the kernel's approach to
Newton is a power law, evaluated at solar-system y ≥ 3.5e5 in the lane (giving
1e-11, far inside Cassini's 2.3e-5). -/
theorem one_minus_mu2_eq (y : ℝ) (hy : y ≠ -1) :
    1 - mu2 y = 1 / (1 + y) ^ 2 := by
  unfold mu2
  have h1 : (1 : ℝ) + y ≠ 0 := by
    intro h0
    exact hy (by linarith)
  field_simp
  ring

/-! ## C3 -- the stress-vs-phantom scaling law -/

/-- **G007 C3 (lemma).** For positive G, M, s, r: the square-root ratio of the
deep-MOND active density's argument to the phantom density's argument is
exactly 1/(s r). -/
theorem sqrt_ratio (G M s r : ℝ) (hG : 0 < G) (hM : 0 < M) (hs : 0 < s) (hr : 0 < r) :
    Real.sqrt (G * M / (2 * s * r ^ 2)) / Real.sqrt (G * M * s / 2) = 1 / (s * r) := by
  have hpos1 : 0 < G * M * s / 2 := by positivity
  have hpos2 : 0 < G * M / (2 * s * r ^ 2) := by positivity
  have hkey : (G * M / (2 * s * r ^ 2)) / (G * M * s / 2) = (1 / (s * r)) ^ 2 := by
    have hd1 : (G * M * s / 2 : ℝ) ≠ 0 := by positivity
    field_simp
  have hStep1 : Real.sqrt (G * M / (2 * s * r ^ 2)) / Real.sqrt (G * M * s / 2)
      = Real.sqrt ((G * M / (2 * s * r ^ 2)) / (G * M * s / 2)) := by
    rw [Real.sqrt_div (le_of_lt hpos2)]
  rw [hStep1]
  rw [hkey, Real.sqrt_sq_eq_abs, abs_of_pos (by positivity)]

/-- **G007 C3.** The deep-MOND stress/phantom density ratio, exactly: the
scalar's active density (4/3) rho_Lambda X^{3/2} with X = GM/(2 s r^2) and
rho_Lambda = s^2/(G c^2), divided by the phantom density sqrt(GM a_0)/(4 pi G
r^2) with a_0 = s/2, equals (4 pi/3)(r_s/r) with r_s = 2GM/c^2 the
Schwarzschild radius.  The stress loses to the phantom by r/r_s ~ 10^6 at
galactic radii, and the deficit GROWS with radius. -/
theorem stress_vs_phantom_ratio (G M s c r : ℝ) (hG : 0 < G) (hM : 0 < M)
    (hs : 0 < s) (hc : 0 < c) (hr : 0 < r) :
    (4 / 3 : ℝ) * (s ^ 2 / (G * c ^ 2)) * (G * M / (2 * s * r ^ 2))
        * (Real.sqrt (G * M / (2 * s * r ^ 2)) / Real.sqrt (G * M * s / 2))
        * (4 * Real.pi * G * r ^ 2)
      = (4 * Real.pi / 3) * ((2 * G * M / c ^ 2) / r) := by
  rw [sqrt_ratio G M s r hG hM hs hr]
  field_simp
  ring

/-! ## D3 -- the kinetic-sign fork -/

/-- **G007 D3 (basis).** mu_2(u) > 0 for u > 0: the kernel is strictly positive
on the MOND branch, so the SIGN of F' is not free. -/
theorem mu2_pos (u : ℝ) (hu : 0 < u) : 0 < mu2 u := by
  unfold mu2
  have hnum : 0 < 2 * u + u ^ 2 := by nlinarith
  have hden : 0 < (1 + u) ^ 2 := by positivity
  exact div_pos hnum hden

/-- **G007 D3 (ii).** The OneFunction's timelike fluctuation kinetic coefficient
A = -M^4 mu_2(X_0)/s^2 is NEGATIVE for every positive M^4, X_0, s^2: the
phantom sign.  (G002's V1 identity F'(X) = mu_2(sqrt X), committed with the
plus sign, is the ghost.) -/
theorem phantom_kinetic_sign (M4 X0 s2 : ℝ) (hM4 : 0 < M4) (hX0 : 0 < X0) (hs2 : 0 < s2) :
    -M4 * mu2 X0 / s2 < 0 := by
  have h : 0 < M4 * mu2 X0 / s2 := by
    exact div_pos (mul_pos hM4 (mu2_pos X0 hX0)) hs2
  have hEq : -M4 * mu2 X0 / s2 = -(M4 * mu2 X0 / s2) := by ring
  rw [hEq]
  exact neg_lt_zero.mpr h

/-- **G007 D3 (iii).** The repair F_h = -f - 2 preserves the OneFunction's
value at the non-analytic point: F_h(0) = -1, so the dark-energy
identification (rho = -rho_Lambda f(0), w = -1) survives the sign flip. -/
theorem flip_vacuum : (-f 0) - 2 = -1 := by
  have h0 : f 0 = -1 := by norm_num [f]
  rw [h0]
  ring

/-- **G007 D3 (iii).** The flipped function's timelike kinetic coefficient
A_h = -M^4 F_h'(X_0)/s^2 = +M^4 mu_2(X_0)/s^2 (F_h' = -mu_2) is POSITIVE: the
flip repairs the phantom sign. -/
theorem flip_kinetic_healthy (M4 X0 s2 : ℝ) (hM4 : 0 < M4) (hX0 : 0 < X0) (hs2 : 0 < s2) :
    0 < -M4 * (-mu2 X0) / s2 := by
  have h : 0 < M4 * mu2 X0 / s2 := by
    exact div_pos (mul_pos hM4 (mu2_pos X0 hX0)) hs2
  have hEq : -M4 * (-mu2 X0) / s2 = M4 * mu2 X0 / s2 := by ring
  rw [hEq]
  exact h

/-- The flipped branch's radial sound speed squared, c_s^2(u) =
(u^2 + 3u + 4)/(u^2 + 3u + 2) (the lane's D3). -/
def cs2 (u : ℝ) : ℝ := (u ^ 2 + 3 * u + 4) / (u ^ 2 + 3 * u + 2)

/-- **G007 D3 (iii, cost).** The flipped branch's deep-limit radial sound speed
is c_s^2(0) = 2: superluminal by sqrt 2 in the deep-MOND limit, the recorded
cost of the repair. -/
theorem cs2_at_origin : cs2 0 = 2 := by
  norm_num [cs2]

/-! ## E1 -- the deep-MOND law -/

/-- **G007 E1.** The slope-2 deep law: if mu = 2 g/s (the deep-MOND branch of
mu_2, the mode count as slope) satisfies mu * g = g_N, then g^2 = (s/2) g_N --
the 1/2 power, with the acceleration scale a_0 = s/2 as the output. -/
theorem deep_mond_law (g s gN : ℝ) (hs : s ≠ 0) (h : (2 * g / s) * g = gN) :
    g ^ 2 = (s / 2) * gN := by
  have hMul : 2 * g / s * g = 2 * g ^ 2 / s := by ring
  rw [hMul] at h
  -- h : 2 * g^2 / s = gN ; clear the denominator (s ≠ 0)
  have hCross : 2 * g ^ 2 = gN * s := by
    rw [← div_eq_iff hs]
    exact h
  -- g^2 = gN * s / 2, and s/2 * gN = gN * s / 2
  have h2ne : (2 : ℝ) ≠ 0 := by norm_num
  have hHalfEq : g ^ 2 = gN * s / 2 := by
    rw [eq_div_iff h2ne]
    linarith
  rw [hHalfEq]
  ring

#print axioms lensing_sum_cancellation
#print axioms disformal_entries
#print axioms one_minus_mu2_eq
#print axioms sqrt_ratio
#print axioms stress_vs_phantom_ratio
#print axioms mu2_pos
#print axioms phantom_kinetic_sign
#print axioms flip_vacuum
#print axioms flip_kinetic_healthy
#print axioms cs2_at_origin
#print axioms deep_mond_law
