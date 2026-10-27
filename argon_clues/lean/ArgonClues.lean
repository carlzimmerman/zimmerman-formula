import Mathlib

/-!
# argon_clues: exact statements about the saturating-tether law, certified

Scope (read this): every theorem below is an exact algebraic/analytic identity or an
inequality between explicit rational numbers. They certify the MATHEMATICS of the statements
used in the audits (identities of the law g_N = g^2/(g+a0), the stiffened-tether inner
solution, the no-go for kappa inside the static action class, the Friedmann-units reduction,
and the census arithmetic). They do NOT certify any physical claim (no theory is "proved"),
and nothing numerical from the boundary-value solves is certified here.
-/

noncomputable section
open Real

namespace ArgonClues

/-- The framework's law: baryonic field in terms of the total field. -/
def gN (g a : ℝ) : ℝ := g ^ 2 / (g + a)
/-- Tether (phantom) field u = g - g_N. -/
def tether (g a : ℝ) : ℝ := g * a / (g + a)

section law
variable {g a : ℝ}

theorem split (hg : 0 < g) (ha : 0 < a) : g = gN g a + tether g a := by
  have h : g + a ≠ 0 := by positivity
  unfold gN tether; field_simp; try ring

theorem tether_eq_sub (hg : 0 < g) (ha : 0 < a) : tether g a = g - gN g a := by
  have := split hg ha; linarith

/-- g_N * a0 = g * u : the geometric-mean invariant. -/
theorem geom_mean (hg : 0 < g) (ha : 0 < a) : gN g a * a = g * tether g a := by
  have h : g + a ≠ 0 := by positivity
  unfold gN tether; field_simp

/-- 1/u = 1/g + 1/a0 : the harmonic (parallel-resistor) form. -/
theorem harmonic (hg : 0 < g) (ha : 0 < a) : 1 / tether g a = 1 / g + 1 / a := by
  have h : g + a ≠ 0 := by positivity
  unfold tether; field_simp; try ring

/-- The wrong harmonic form is false: 1/g_N - 1/g = 1/a0 fails. -/
theorem wrong_harmonic_false : ¬ (1 / gN 1 2 - 1 / (1:ℝ) = 1 / (2:ℝ)) := by
  unfold gN; norm_num

/-- y * nu * (nu - 1) = 1 with y = g_N/a0, nu = g/g_N. -/
theorem nu_quadratic (hg : 0 < g) (ha : 0 < a) :
    (gN g a / a) * (g / gN g a) * (g / gN g a - 1) = 1 := by
  have h : g + a ≠ 0 := by positivity
  have hn : gN g a ≠ 0 := by unfold gN; positivity
  unfold gN at *
  field_simp
  ring

/-- Golden ratio at g_N = a0. -/
theorem golden (hg : 0 < g) (ha : 0 < a) (h : gN g a = a) : g / a = (1 + Real.sqrt 5) / 2 := by
  have hs : g + a ≠ 0 := by positivity
  unfold gN at h
  field_simp at h
  have hq : (g / a) ^ 2 - g / a - 1 = 0 := by
    field_simp; nlinarith [h]
  set t := g / a with ht
  have tpos : 0 < t := by positivity
  have t1 : 1 < t := by nlinarith
  have h5 : (2 * t - 1) ^ 2 = 5 := by nlinarith
  have : 2 * t - 1 = Real.sqrt 5 := by
    rw [← Real.sqrt_sq (by linarith : (0:ℝ) ≤ 2 * t - 1), h5]
  linarith

end law

/-! ## No-go for kappa inside the static action class -/

/-- Scale covariance: (g,a) -> (lam g, lam a) scales g_N and the tether by lam. -/
theorem scale_gN (lam g a : ℝ) (hl : 0 < lam) (hg : 0 < g) (ha : 0 < a) :
    gN (lam * g) (lam * a) = lam * gN g a := by
  have h : g + a ≠ 0 := by positivity
  have h2 : lam * g + lam * a ≠ 0 := by positivity
  unfold gN; field_simp; try ring

theorem scale_tether (lam g a : ℝ) (hl : 0 < lam) (hg : 0 < g) (ha : 0 < a) :
    tether (lam * g) (lam * a) = lam * tether g a := by
  have h : g + a ≠ 0 := by positivity
  have h2 : lam * g + lam * a ≠ 0 := by positivity
  unfold tether; field_simp; try ring

/-- The amplification nu = g/g_N is invariant: it depends only on g/a0, so a0 enters only as a
unit, and the static field equations are isomorphic for every a0 > 0 (kappa unconstrained). -/
theorem scale_nu (lam g a : ℝ) (hl : 0 < lam) (hg : 0 < g) (ha : 0 < a) :
    (lam * g) / gN (lam * g) (lam * a) = g / gN g a := by
  rw [scale_gN lam g a hl hg ha]
  have : gN g a ≠ 0 := by unfold gN; have h : g + a ≠ 0 := by positivity
                          positivity
  field_simp

/-! ## The remainder potential and its curvature -/

/-- d/du of K W_rem(u) = a^2 ( -ln(1-u/a) - u/a - u^2/(2a^2) ) is u^2/(a-u). -/
theorem Wrem_deriv {a u : ℝ} (ha : 0 < a) (hu : u < a) :
    HasDerivAt (fun u => a ^ 2 * (-(Real.log (1 - u / a)) - u / a - u ^ 2 / (2 * a ^ 2)))
      (u ^ 2 / (a - u)) u := by
  have hne : 1 - u / a ≠ 0 := by
    have : u / a < 1 := by rw [div_lt_one ha]; exact hu
    linarith
  have h1 : HasDerivAt (fun u : ℝ => 1 - u / a) (-(1 / a)) u := by
    simpa using ((hasDerivAt_id u).div_const a).const_sub 1
  have h2 := h1.log hne
  have h3 : HasDerivAt (fun u : ℝ => u / a) (1 / a) u := by
    simpa using (hasDerivAt_id u).div_const a
  have h4 : HasDerivAt (fun u : ℝ => u ^ 2 / (2 * a ^ 2)) (2 * u / (2 * a ^ 2)) u := by
    simpa using ((hasDerivAt_pow 2 u).div_const (2 * a ^ 2))
  have h5 := ((h2.neg.sub h3).sub h4).const_mul (a ^ 2)
  refine h5.congr_deriv ?_
  have ha' : a ≠ 0 := ne_of_gt ha
  have hau : a - u ≠ 0 := by linarith
  field_simp
  ring

/-- d/du [u^2/(a-u)] = u(2a-u)/(a-u)^2. -/
theorem Wprime_deriv {a u : ℝ} (hu : u < a) :
    HasDerivAt (fun u => u ^ 2 / (a - u)) (u * (2 * a - u) / (a - u) ^ 2) u := by
  have hau : a - u ≠ 0 := by linarith
  have h1 : HasDerivAt (fun u : ℝ => a - u) (-1) u := by
    simpa using (hasDerivAt_id u).const_sub a
  have h2 := (hasDerivAt_pow 2 u).div h1 hau
  refine h2.congr_deriv ?_
  field_simp
  ring

/-- On the law, K W_rem'' = g(g+2a)/a^2 and K W_full'' = (1 + g/a)^2. -/
theorem Wcurvature (g a : ℝ) (hg : 0 < g) (ha : 0 < a) :
    tether g a * (2 * a - tether g a) / (a - tether g a) ^ 2 = g * (g + 2 * a) / a ^ 2
    ∧ 1 + g * (g + 2 * a) / a ^ 2 = (1 + g / a) ^ 2 := by
  have h : g + a ≠ 0 := by positivity
  have ha' : a ≠ 0 := ne_of_gt ha
  constructor
  · have hd : a - tether g a = a ^ 2 / (g + a) := by unfold tether; field_simp; ring
    rw [hd]; unfold tether; field_simp; ring
  · field_simp; try ring

/-! ## The stiffened tether around a point mass -/

/-- Vector-Laplacian residual of a constant radial profile u0 r_hat:
-L^2 (u'' + 2u'/r - 2u/r^2) with u'' = u' = 0 equals 2 L^2 u0 / r^2. -/
def innerResidual (L u0 r : ℝ) : ℝ := -L ^ 2 * (0 + 2 * 0 / r - 2 * u0 / r ^ 2)

theorem inner_residual_eq (L u0 r : ℝ) : innerResidual L u0 r = 2 * L ^ 2 * u0 / r ^ 2 := by
  unfold innerResidual; ring

/-- The constant inner solution balances the Newtonian point-mass field GM/r^2 exactly iff
u0 = GM/(2 L^2). -/
theorem inner_solution (G M L u0 r : ℝ) (hr : r ≠ 0) (hL : L ≠ 0) :
    innerResidual L u0 r = G * M / r ^ 2 ↔ u0 = G * M / (2 * L ^ 2) := by
  rw [inner_residual_eq]
  constructor
  · intro h
    field_simp at h ⊢; linarith
  · intro h; rw [h]; field_simp

/-- Saturation u0 = a0 happens exactly at M = M_crit := 2 a0 L^2 / G. -/
theorem M_crit_iff (G M L a : ℝ) (hG : 0 < G) (hL : L ≠ 0) :
    G * M / (2 * L ^ 2) = a ↔ M = 2 * a * L ^ 2 / G := by
  have hG' : G ≠ 0 := ne_of_gt hG
  constructor
  · intro h; field_simp at h ⊢; linarith
  · intro h; rw [h]; field_simp

/-- Phantom mass inside r = L is u0 L^2 / G = M/2 for the inner solution; at the cap u0 = a0
it equals a0 L^2/G = M_crit/2, so no source can hold more than M_crit/2 of tether inside L. -/
theorem phantom_cap (G M L : ℝ) (hG : 0 < G) (hL : L ≠ 0) :
    (G * M / (2 * L ^ 2)) * L ^ 2 / G = M / 2 := by
  have hG' : G ≠ 0 := ne_of_gt hG
  field_simp

theorem phantom_cap_value (G L a : ℝ) (hG : 0 < G) :
    a * L ^ 2 / G = (2 * a * L ^ 2 / G) / 2 := by
  have hG' : G ≠ 0 := ne_of_gt hG
  field_simp

/-- Screening radius r_s = L^2 / r_M with r_M^2 = G M / a0: r_s * r_M = L^2 and
r_s^2 = L^4 a0 /(G M). -/
theorem screening_radius (G M a L rM : ℝ) (hGM : 0 < G * M) (ha : 0 < a) (hrM : 0 < rM)
    (hdef : rM ^ 2 = G * M / a) :
    (L ^ 2 / rM) * rM = L ^ 2 ∧ (L ^ 2 / rM) ^ 2 = L ^ 4 * a / (G * M) := by
  have hr : rM ≠ 0 := ne_of_gt hrM
  have hGM' : G * M ≠ 0 := ne_of_gt hGM
  have ha' : a ≠ 0 := ne_of_gt ha
  constructor
  · field_simp
  · rw [div_pow, hdef]; field_simp; try ring

/-! ## Virial fraction of a power-law tether -/

/-- For W = u^(n+1)/(n+1) (so W' = u^n), 1 - W/(u W') = n/(n+1); for the cubic tether (n=2) it is 2/3. -/
theorem free_fraction (u n : ℝ) (hu : 0 < u) (hn : 0 < n) :
    1 - (u ^ (n + 1) / (n + 1)) / (u * u ^ n) = n / (n + 1) := by
  have hpos : 0 < u ^ n := Real.rpow_pos_of_pos hu n
  have h1 : u ^ (n + 1) = u * u ^ n := by
    rw [Real.rpow_add hu, Real.rpow_one]; ring
  rw [h1]
  have hn1 : n + 1 ≠ 0 := by linarith
  have hu' : u ≠ 0 := ne_of_gt hu
  have hp : u ^ n ≠ 0 := ne_of_gt hpos
  field_simp
  ring

theorem free_fraction_cubic (u : ℝ) (hu : 0 < u) :
    1 - (u ^ 3 / 3) / (u * u ^ 2) = 2 / 3 := by
  have hu' : u ≠ 0 := ne_of_gt hu
  field_simp
  ring

/-! ## Friedmann units: where the pi in Z lives -/

/-- With H^2 = 8 pi G rho / 3 and a0^2 = c^2 G rho / 4, one has a0^2 * Z^2 = c^2 H^2 with
Z^2 = 32 pi / 3: the pi is Friedmann's, a0 is pi-free in (c, G, rho) units. -/
theorem friedmann_units (c G ρ H a0 : ℝ)
    (hH : H ^ 2 = 8 * Real.pi * G * ρ / 3) (ha : a0 ^ 2 = c ^ 2 * G * ρ / 4) :
    a0 ^ 2 * (32 * Real.pi / 3) = c ^ 2 * H ^ 2 := by
  rw [ha, hH]; ring

/-- Z = 2 sqrt(8 pi / 3), i.e. Z/2 = sqrt(8 pi/3). -/
theorem Z_factor : Real.sqrt (32 * Real.pi / 3) = 2 * Real.sqrt (8 * Real.pi / 3) := by
  have h : 32 * Real.pi / 3 = 2 ^ 2 * (8 * Real.pi / 3) := by ring
  rw [h, Real.sqrt_mul (by norm_num), Real.sqrt_sq (by norm_num)]

/-- The Deser-Levin gate floor is a0/2: if a_floor = a0/2 and a0 Z = c H, then
kappa_dS / a_floor = 2 Z. -/
theorem floor_ratio (c H a0 Z : ℝ) (ha0 : 0 < a0) (h : a0 * Z = c * H) :
    (c * H) / (a0 / 2) = 2 * Z := by
  have : a0 ≠ 0 := ne_of_gt ha0
  rw [← h]; field_simp

/-! ## The gate -/

/-- mu_fw(x) = (sqrt(1+4x^2) - 1)/(2x) solves mu^2 + mu/x - 1 = 0. -/
theorem gate_solves (x : ℝ) (hx : 0 < x) :
    ((Real.sqrt (1 + 4 * x ^ 2) - 1) / (2 * x)) ^ 2 + ((Real.sqrt (1 + 4 * x ^ 2) - 1) / (2 * x)) / x - 1 = 0 := by
  have hs : Real.sqrt (1 + 4 * x ^ 2) ^ 2 = 1 + 4 * x ^ 2 := Real.sq_sqrt (by positivity)
  have hx' : x ≠ 0 := ne_of_gt hx
  field_simp
  nlinarith [hs]

/-- The gate is the Deser-Levin form evaluated at y = 2x (so the quadrature floor is a0/2). -/
theorem gate_is_DL (x : ℝ) (hx : 0 < x) :
    (Real.sqrt (1 + 4 * x ^ 2) - 1) / (2 * x) = (Real.sqrt (1 + (2 * x) ^ 2) - 1) / (2 * x) := by
  congr 3; ring

/-- Completing the square: g^2 = g_N^2 + g_N a0  <->  (g_N + a0/2)^2 = g^2 + (a0/2)^2. -/
theorem complete_square (g n a : ℝ) :
    g ^ 2 = n ^ 2 + n * a ↔ (n + a / 2) ^ 2 = g ^ 2 + (a / 2) ^ 2 := by
  constructor <;> intro h <;> nlinarith [h]

/-! ## Census arithmetic (CFG779: B = 1.064 [1.010, 1.122]) -/

theorem census_fraction :
    ((1122 : ℚ) / 1000 - 1) / (5364 / 1000) < 23 / 1000 := by norm_num

theorem census_R_today_upper :
    (467 : ℚ) / 100 < ((5364 : ℚ) / 1000 - ((1122 : ℚ) / 1000 - 1)) / (1122 / 1000) := by norm_num

theorem census_R_today_central :
    (498 : ℚ) / 100 < ((5364 : ℚ) / 1000 - ((1064 : ℚ) / 1000 - 1)) / (1064 / 1000) := by norm_num

/-- M_crit in solar masses for a0 = 9.36e-11, L* = 5.75 pc (pc = 3.085677581e16 m),
G = 6.6743e-11, Msun = 1.98847e30 lies between 4.43e4 and 4.45e4 (not 4.46e7). -/
theorem M_crit_value :
    (44300 : ℚ) < 2 * (936 / 10 ^ 13) * ((575 / 100) * (3085677581 * 10 ^ 7)) ^ 2
        / (66743 / 10 ^ 15) / (198847 * 10 ^ 25)
    ∧ 2 * (936 / 10 ^ 13) * ((575 / 100) * (3085677581 * 10 ^ 7)) ^ 2
        / (66743 / 10 ^ 15) / (198847 * 10 ^ 25) < (44500 : ℚ) := by
  constructor <;> norm_num

/-- The pasted value 4.46e7 Msun is impossible: M_crit < 4.5e4 (so the claim was 1000x too large). -/
theorem M_crit_not_paste :
    ¬ ((44600000 : ℚ) < 2 * (936 / 10 ^ 13) * ((575 / 100) * (3085677581 * 10 ^ 7)) ^ 2
        / (66743 / 10 ^ 15) / (198847 * 10 ^ 25)) := by
  norm_num

/-- sqrt(a0 L*)^2 = a0 L* lies in (1.6e7, 1.7e7) m^2/s^2 (a0 = 9.36e-11, L* = 5.75 pc): the
speed is 4.1 km/s, so the pasted 139 km/s is impossible. -/
theorem sigma_star_sq :
    (16000000 : ℚ) < (936 / 10 ^ 13) * ((575 / 100) * (3085677581 * 10 ^ 7))
    ∧ (936 / 10 ^ 13) * ((575 / 100) * (3085677581 * 10 ^ 7)) < 17000000 := by
  constructor <;> norm_num

theorem sigma_star_not_139 :
    ¬ ((139000 : ℚ) ^ 2 < (936 / 10 ^ 13) * ((575 / 100) * (3085677581 * 10 ^ 7))) := by
  norm_num

end ArgonClues

#print axioms ArgonClues.split
#print axioms ArgonClues.golden
#print axioms ArgonClues.scale_nu
#print axioms ArgonClues.Wrem_deriv
#print axioms ArgonClues.Wcurvature
#print axioms ArgonClues.inner_solution
#print axioms ArgonClues.free_fraction
#print axioms ArgonClues.friedmann_units
#print axioms ArgonClues.gate_solves
#print axioms ArgonClues.M_crit_value
#print axioms ArgonClues.sigma_star_not_139
