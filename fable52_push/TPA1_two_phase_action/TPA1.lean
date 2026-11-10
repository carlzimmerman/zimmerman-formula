/-
TPA1 (criteria b81c28d00c): Lean statements for the algebra the two-phase action's equations rely on. They certify the
algebraic identities and inequalities, not the physics. TEST lane; adopts nothing. kappa = 1/2 FITTED; not theory closed.

Units a0 = K = 1 (so u = |A|/a0, x = K|P|/a0). The law's dual W(x) = -x - log(1 - x) for x < 1, and its Legendre
transform J(u) = u - log(1 + u). The action's law term is S (P.A - W(K|P|)) (S on both terms, reading R1).

  legendre_map            : for S /= 0 the P equation S (u - W'(x)) = 0 holds iff x = u/(1 + u) (the map is S-free).
  pa_only_distorts        : with S on P.A alone the map is x = S u/(1 + S u), which differs from u/(1 + u) unless S = 1.
  legendre_value          : at x = u/(1 + u), x u - W(x) = J(u).
  static_law_phase        : in the S = 1 phase, Gauss u (1 - 1/(1 + u)) = y is the law g^2 = g_N (g + a0).
  leaf_stress_on_shell    : the covariant leaf stress S[(P.A - W) - 2 P.E + K W' P] equals -S W on the P shell (K W' = E).
  stress_jump_eq_W        : the momentum flux Pi = E^2/2 - S W(K|P|) jumps by W_wall(u) = u - log(1+u) - u^2/(2(1+u)^2)
                            across a wall S: 1 -> 0 at fixed displacement y = u^2/(1 + u)  (SWT1's wall pressure).
  dPi_dS_fixed_D          : along fixed displacement, dPi/dS = J(E): the force density on the carrier is -J dS.
  W_wall_pos              : W_wall(u) > 0 for u > 0 (outward); flipped_clock_inward: the M1 sign gives -W_wall < 0.
  static_clock_monotone   : for any non-increasing S and n_d(N) = c (Q_inf/N - 1), c, Q_inf > 0, the map N -> S(n_d(N))
                            is monotone: in a static clock the law-on phase is a superlevel set of the potential.
  growth_eps_one          : the linear growth factor 1 - k^2/(mu^2 + eps k^2) at eps = 1 is 1/(1 + k^2/mu^2) (RK04).
-/
import Mathlib

namespace TPA1

noncomputable def Wd (x : ℝ) : ℝ := -x - Real.log (1 - x)
noncomputable def J (u : ℝ) : ℝ := u - Real.log (1 + u)
noncomputable def Wwall (u : ℝ) : ℝ := u - Real.log (1 + u) - u ^ 2 / (2 * (1 + u) ^ 2)

/-- W'(x) = x/(1 - x) for x < 1. -/
theorem hasDerivAt_Wd (x : ℝ) (hx : x < 1) : HasDerivAt Wd (x / (1 - x)) x := by
  have hp : (1 - x) ≠ 0 := by linarith
  have h1 : HasDerivAt (fun v : ℝ => 1 - v) (-1) x := by
    simpa using (hasDerivAt_id x).const_sub 1
  have hlog : HasDerivAt (fun v : ℝ => Real.log (1 - v)) ((1 - x)⁻¹ * (-1)) x :=
    (Real.hasDerivAt_log hp).comp x h1
  have hall : HasDerivAt (fun v : ℝ => -v - Real.log (1 - v)) (-1 - (1 - x)⁻¹ * (-1)) x :=
    (hasDerivAt_id x).neg.sub hlog
  have hd : -1 - (1 - x)⁻¹ * (-1) = x / (1 - x) := by
    field_simp
    ring
  have hfun : Wd = fun v : ℝ => -v - Real.log (1 - v) := by funext v; rfl
  rw [hfun]; exact hall.congr_deriv hd

/-- the P equation with S on both terms of the Legendre pair: the map does not see S. -/
theorem legendre_map (S u x : ℝ) (hS : S ≠ 0) (hx : x < 1) (hu : 0 ≤ u) :
    S * (u - x / (1 - x)) = 0 ↔ x = u / (1 + u) := by
  have hp : (1 - x) ≠ 0 := by linarith
  have hq : (1 + u) ≠ 0 := by linarith
  constructor
  · intro h
    have h2 : u - x / (1 - x) = 0 := by
      rcases mul_eq_zero.mp h with h0 | h0
      · exact absurd h0 hS
      · exact h0
    have h3 : u = x / (1 - x) := by linarith
    rw [h3]; field_simp; ring
  · intro h
    rw [h]
    have : u - u / (1 + u) / (1 - u / (1 + u)) = 0 := by
      field_simp
      ring
    rw [this]; ring

/-- with S on P.A alone (the M2-type misplacement) the stationary point is x = S u/(1 + S u). -/
theorem pa_only_map (S u x : ℝ) (hx : x < 1) (hSu : 0 ≤ S * u) :
    S * u - x / (1 - x) = 0 ↔ x = S * u / (1 + S * u) := by
  have hp : (1 - x) ≠ 0 := by linarith
  have hq : (1 + S * u) ≠ 0 := by linarith
  constructor
  · intro h
    have h3 : S * u = x / (1 - x) := by linarith
    rw [h3]; field_simp; ring
  · intro h
    rw [h]; field_simp; ring

theorem pa_only_distorts (S u : ℝ) (hu : 0 < u) (hS0 : 0 ≤ S) (hS : S ≠ 1) :
    S * u / (1 + S * u) ≠ u / (1 + u) := by
  intro h
  have h1 : (0 : ℝ) < 1 + S * u := by positivity
  have h2 : (0 : ℝ) < 1 + u := by linarith
  rw [div_eq_div_iff h1.ne' h2.ne'] at h
  have : (S - 1) * u = 0 := by nlinarith
  rcases mul_eq_zero.mp this with h3 | h3
  · exact hS (by linarith)
  · linarith

/-- the Legendre value: x u - W(x) at x = u/(1 + u) is J(u) = u - log(1 + u). -/
theorem legendre_value (u : ℝ) (hu : 0 ≤ u) :
    (u / (1 + u)) * u - Wd (u / (1 + u)) = J u := by
  unfold Wd J
  have hq : (0 : ℝ) < 1 + u := by linarith
  have h1 : 1 - u / (1 + u) = (1 + u)⁻¹ := by field_simp; ring
  rw [h1, Real.log_inv]
  field_simp
  ring

/-- the S = 1 phase: Gauss with the switched operator, u (1 - 1/(1 + u)) = y, is the law g^2 = g_N (g + a0). -/
theorem static_law_phase (a0 g gN : ℝ) (ha : 0 < a0) (hg : 0 ≤ g) :
    (g / a0) * (1 - 1 / (1 + g / a0)) = gN / a0 ↔ g ^ 2 = gN * (g + a0) := by
  have h1 : (0 : ℝ) < 1 + g / a0 := by positivity
  have h2 : (0 : ℝ) < g + a0 := by linarith
  have key : (g / a0) * (1 - 1 / (1 + g / a0)) = g ^ 2 / (a0 * (g + a0)) := by
    field_simp
    ring
  rw [key, div_eq_div_iff (by positivity) ha.ne']
  constructor
  · intro h; nlinarith
  · intro h; nlinarith

/-- the covariant leaf stress (T_xx of the law sector, field along x) on the P shell K W'(K|P|) = E is -S W. -/
theorem leaf_stress_on_shell (S p E Wv : ℝ) :
    S * ((p * E - Wv) - 2 * p * E + E * p) = -(S * Wv) := by ring

/-- the momentum flux Pi = E^2/2 - S Wd(K|P|) (law stress plus Newtonian gravitational stress) jumps by Wwall(u)
across a wall S: 1 -> 0 at fixed displacement y = u^2/(1 + u); inside E = u and K|P| = u/(1 + u), outside E = y. -/
theorem stress_jump_eq_W (u : ℝ) (hu : 0 ≤ u) :
    (u ^ 2 / 2 - 1 * Wd (u / (1 + u))) - ((u ^ 2 / (1 + u)) ^ 2 / 2 - 0 * Wd 0) = Wwall u := by
  unfold Wd Wwall
  have hq : (0 : ℝ) < 1 + u := by linarith
  have h1 : 1 - u / (1 + u) = (1 + u)⁻¹ := by field_simp; ring
  rw [h1, Real.log_inv]
  field_simp
  ring

/-- along fixed displacement D = E (1 - S/(1 + E)): with dPi/dE = E (1 - S/(1+E)^2), dPi/dS = -Wd(E/(1+E)),
dD/dS = -E/(1 + E), dD/dE = 1 - S/(1+E)^2, the total derivative dPi/dS - (dPi/dE)(dD/dS)/(dD/dE) is J(E). -/
theorem dPi_dS_fixed_D (S E : ℝ) (hE : 0 ≤ E) (hden : 1 - S / (1 + E) ^ 2 ≠ 0) :
    -Wd (E / (1 + E)) - (E * (1 - S / (1 + E) ^ 2)) * (-(E / (1 + E))) / (1 - S / (1 + E) ^ 2) = J E := by
  rw [mul_div_right_comm, mul_div_cancel_right₀ _ hden]
  unfold Wd J
  have hq : (0 : ℝ) < 1 + E := by linarith
  have h1 : 1 - E / (1 + E) = (1 + E)⁻¹ := by field_simp; ring
  rw [h1, Real.log_inv]
  field_simp
  ring

theorem hasDerivAt_Wwall (u : ℝ) (hu : -1 < u) :
    HasDerivAt Wwall (u ^ 2 * (2 + u) / (1 + u) ^ 3) u := by
  have hp : (1 + u) ≠ 0 := by linarith
  have h1 : HasDerivAt (fun v : ℝ => 1 + v) 1 u := by
    simpa using (hasDerivAt_id u).const_add 1
  have hlog : HasDerivAt (fun v : ℝ => Real.log (1 + v)) ((1 + u)⁻¹ * 1) u :=
    (Real.hasDerivAt_log hp).comp u h1
  have hn : HasDerivAt (fun v : ℝ => v ^ 2) (2 * u) u := by
    simpa using hasDerivAt_pow 2 u
  have hd : HasDerivAt (fun v : ℝ => 2 * (1 + v) ^ 2) (2 * (2 * (1 + u) * 1)) u := by
    have := (h1.pow 2).const_mul 2
    simpa using this
  have hne : (2 * (1 + u) ^ 2) ≠ 0 := by positivity
  have hq := hn.div hd hne
  have hall : HasDerivAt (fun v : ℝ => v - Real.log (1 + v) - v ^ 2 / (2 * (1 + v) ^ 2))
      (1 - (1 + u)⁻¹ * 1 - (2 * u * (2 * (1 + u) ^ 2) - u ^ 2 * (2 * (2 * (1 + u) * 1))) / (2 * (1 + u) ^ 2) ^ 2) u :=
    ((hasDerivAt_id u).sub hlog).sub hq
  have hderiv : 1 - (1 + u)⁻¹ * 1 - (2 * u * (2 * (1 + u) ^ 2) - u ^ 2 * (2 * (2 * (1 + u) * 1))) / (2 * (1 + u) ^ 2) ^ 2
      = u ^ 2 * (2 + u) / (1 + u) ^ 3 := by
    field_simp
    ring
  have hfun : Wwall = fun v : ℝ => v - Real.log (1 + v) - v ^ 2 / (2 * (1 + v) ^ 2) := by
    funext v; rfl
  rw [hfun]
  exact hall.congr_deriv hderiv

/-- the wall pressure is strictly outward for u > 0 (the argument of SWT1's W_nonneg, made strict). -/
theorem W_wall_pos (u : ℝ) (hu : 0 < u) : 0 < Wwall u := by
  have hmono : StrictMonoOn Wwall (Set.Ici 0) := by
    apply strictMonoOn_of_deriv_pos (convex_Ici 0)
    · intro x hx
      have hx0 : (0 : ℝ) ≤ x := hx
      exact (hasDerivAt_Wwall x (by linarith)).continuousAt.continuousWithinAt
    · intro x hx
      rw [interior_Ici] at hx
      have hx0 : (0 : ℝ) < x := hx
      rw [(hasDerivAt_Wwall x (by linarith)).deriv]
      positivity
  have h0 : Wwall 0 = 0 := by simp [Wwall]
  have := hmono (Set.mem_Ici.mpr le_rfl) (Set.mem_Ici.mpr hu.le) hu
  linarith

/-- MUTATE M1 in the equations: flipping the sign of the clock charge's S' term flips the force: -W_wall < 0 (inward). -/
theorem flipped_clock_inward (u : ℝ) (hu : 0 < u) : -Wwall u < 0 := by
  have := W_wall_pos u hu
  linarith

/-- static clock: n_d(N) = c (Q_inf/N - 1) falls as N grows; any non-increasing switch S makes N -> S(n_d(N)) monotone,
so the law-on phase (large S) lies at large N (shallow potential) and the dust phase at small N (deep potential). -/
theorem static_clock_monotone (S : ℝ → ℝ) (hS : Antitone S) (c Qi : ℝ) (hc : 0 < c) (hQ : 0 < Qi) :
    MonotoneOn (fun N : ℝ => S (c * (Qi / N - 1))) (Set.Ioi 0) := by
  intro N₁ h₁ N₂ h₂ h12
  have h1 : (0 : ℝ) < N₁ := h₁
  apply hS
  have : Qi / N₂ ≤ Qi / N₁ := div_le_div_of_nonneg_left hQ.le h1 h12
  have h3 : Qi / N₂ - 1 ≤ Qi / N₁ - 1 := by linarith
  exact mul_le_mul_of_nonneg_left h3 hc.le

/-- the linear growth factor of the cold component with S = eps on the background, at eps = 1, is RK04's f. -/
theorem growth_eps_one (mu k : ℝ) (hmu : 0 < mu) :
    1 - k ^ 2 / (mu ^ 2 + 1 * k ^ 2) = 1 / (1 + k ^ 2 / mu ^ 2) := by
  have h1 : (0 : ℝ) < mu ^ 2 + k ^ 2 := by positivity
  have h2 : (0 : ℝ) < mu ^ 2 := by positivity
  field_simp
  ring

end TPA1

#print axioms TPA1.hasDerivAt_Wd
#print axioms TPA1.legendre_map
#print axioms TPA1.pa_only_map
#print axioms TPA1.pa_only_distorts
#print axioms TPA1.legendre_value
#print axioms TPA1.static_law_phase
#print axioms TPA1.leaf_stress_on_shell
#print axioms TPA1.stress_jump_eq_W
#print axioms TPA1.dPi_dS_fixed_D
#print axioms TPA1.hasDerivAt_Wwall
#print axioms TPA1.W_wall_pos
#print axioms TPA1.flipped_clock_inward
#print axioms TPA1.static_clock_monotone
#print axioms TPA1.growth_eps_one

-- kappa = 1/2 FITTED; not theory closed. Adopts nothing.
