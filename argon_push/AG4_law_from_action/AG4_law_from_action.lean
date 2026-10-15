import Mathlib

/-!
# AG4: the rest-state law from the frozen S2 action — certified algebra

SCOPE (read this). This file certifies the ALGEBRA of the AG4 adjudication
(argon_push/AG4_law_from_action, frozen criteria 93e579ec1 + AMD-A c80cdb5fd):
given the static rest-state equation of the frozen action
  L = -|grad Phi - K P|^2/(2K) - rho_b Phi - W_rem(u) - (gamma/2)|grad P|^2,
  K W_rem'(u) = u^2/(a0 - n u),  u = K|P|,
which the sympy lane derives by jet Euler-Lagrange (G1, residual identically zero),
the theorems below certify:
  * the rest state gbar = u^2/(a0 - u) is equivalent to u^2 + gbar u = a0 gbar (T1);
  * with g = gbar + u this IS the canonical law g^2 = gbar (g + a0), i.e.
    gbar = g^2/(g + a0) (T2), and conversely (T3);
  * the rest state is unique for gbar > 0 (T4) and obeys the tether bound u < a0 (T5);
  * the explicit root u = (sqrt(gbar^2 + 4 a0 gbar) - gbar)/2 (T6);
  * the capacity family: u^2 + n gbar u = a0 gbar gives g^2 - gbar^2 = a0 gbar + (2-n) gbar u,
    so n = 1 is the canonical law and n = 2 is EXACTLY the quadratic "a0-line"
    g^2 - gbar^2 = a0 gbar (T7, T7_n2) — the repo's two law lines differ by the single
    structural number n (tether capacity a0/n... a0 vs a0/2);
  * the ARGON02 P1 phantom-mass identity M_ph/M_b = (sqrt(1+4x^2)-1)/2 follows from the
    rest state with the point-mass baryon field gbar = a0/x^2 (T8);
  * the deep-regime sandwich sqrt(a0 gbar) - gbar/2 <= u <= sqrt(a0 gbar) (T9, T9b):
    u -> sqrt(a0 gbar), the shared deep asymptote g_ph -> C/r of BOTH law lines.

PHYSICAL PREMISES NOT CERTIFIED HERE (declared, per house rule): the variational step
itself (functional derivatives; certified symbolically in ag4_derive.py G1), Gauss for A
on a point baryon mass, P parallel A at rest, and gamma = 0 outside the screening core
(G4, numeric). No physical law is "proved" by this file; it certifies the algebraic
structure the derivation rests on.

Every statement was hand-derived and sympy-prechecked in the same session (G5-pre,
ag4_derive.out) before typing, per the lean-math-certification discipline.
-/

noncomputable section

namespace AG4

/-- T1: the rest-state EOM gbar = u^2/(a0 - u) in cleared form is u^2 + gbar*u = a0*gbar.
Polynomial identity — no division, no nonzero hypotheses needed (Lean division is total,
so the cleared form is the honest statement). -/
theorem T1_eom_bridge (gb u a : ℝ) : gb * (a - u) = u ^ 2 ↔ u ^ 2 + gb * u = a * gb := by
  constructor <;> intro h <;> linarith

/-- T2: rest state => canonical law. With g := gbar + u, the rest-state equation
u^2 + gbar u = a0 gbar IS the law g^2 = gbar (g + a0) (same polynomial). -/
theorem T2_rest_state_to_law (gb u a : ℝ) (hrest : u ^ 2 + gb * u = a * gb) :
    (gb + u) ^ 2 = gb * ((gb + u) + a) := by
  have key : (gb + u) ^ 2 - gb * ((gb + u) + a) = u ^ 2 + gb * u - a * gb := by ring
  linarith

/-- T3: canonical law => rest state (converse of T2; the two residuals coincide). -/
theorem T3_law_to_rest_state (gb u a : ℝ) (hlaw : (gb + u) ^ 2 = gb * ((gb + u) + a)) :
    u ^ 2 + gb * u = a * gb := by
  have key : (gb + u) ^ 2 - gb * ((gb + u) + a) = u ^ 2 + gb * u - a * gb := by ring
  linarith

/-- T4: uniqueness of the positive rest state for gbar > 0 (strict monotonicity of
u^2 + gbar u on u > 0, via the factorization of the difference). -/
theorem T4_rest_state_unique (gb u1 u2 a : ℝ) (hgb : 0 < gb) (hu1 : 0 < u1) (hu2 : 0 < u2)
    (h1 : u1 ^ 2 + gb * u1 = a * gb) (h2 : u2 ^ 2 + gb * u2 = a * gb) : u1 = u2 := by
  have hf : (u1 - u2) * (u1 + u2 + gb) = 0 := by
    have hexp : (u1 - u2) * (u1 + u2 + gb) = (u1 ^ 2 + gb * u1) - (u2 ^ 2 + gb * u2) := by ring
    linarith
  have hpos : 0 < u1 + u2 + gb := by linarith
  rcases eq_zero_or_eq_zero_of_mul_eq_zero hf with hz | hz
  · linarith
  · exact absurd hz (ne_of_gt hpos)

/-- T5: the tether bound — any positive rest state saturates strictly below capacity:
u < a0. (For n = 1 this is g_ph < a0, i.e. Sigma_bar < a0/(pi G) in the sheet convention
PAPER49 quotes as ≈ 214 Msun/pc^2.) -/
theorem T5_tether_bound (gb u a : ℝ) (hgb : 0 < gb) (hu : 0 < u)
    (hrest : u ^ 2 + gb * u = a * gb) : u < a := by
  have h : gb * (a - u) = u ^ 2 := by linarith
  have hpos : 0 < gb * (a - u) := by
    rw [h]
    exact sq_pos_of_pos hu
  have hgt : 0 < a - u := pos_of_mul_pos_right hpos (le_of_lt hgb)
  linarith

/-- T6: the explicit root. u0 = (sqrt(gbar^2 + 4 a0 gbar) - gbar)/2 is positive and
solves the rest-state equation. -/
theorem T6_explicit_root (gb a : ℝ) (hgb : 0 < gb) (ha : 0 < a) :
    0 < (Real.sqrt (gb ^ 2 + 4 * a * gb) - gb) / 2 ∧
    ((Real.sqrt (gb ^ 2 + 4 * a * gb) - gb) / 2) ^ 2
      + gb * ((Real.sqrt (gb ^ 2 + 4 * a * gb) - gb) / 2) = a * gb := by
  constructor
  · have hD : gb < Real.sqrt (gb ^ 2 + 4 * a * gb) :=
      (Real.lt_sqrt (le_of_lt hgb)).2 (by nlinarith)
    linarith
  · set sd := Real.sqrt (gb ^ 2 + 4 * a * gb) with hsd
    have hsq : sd ^ 2 = gb ^ 2 + 4 * a * gb := by
      rw [hsd, Real.sq_sqrt (by nlinarith : (0 : ℝ) ≤ gb ^ 2 + 4 * a * gb)]
    have hkey : ((sd - gb) / 2) ^ 2 + gb * ((sd - gb) / 2) = (sd ^ 2 - gb ^ 2) / 4 := by ring
    have hval : (sd ^ 2 - gb ^ 2) / 4 = a * gb := by
      rw [hsq]
      ring
    linarith

/-- T7: the capacity family. On-shell (u^2 + n gbar u = a0 gbar), the quadratic-form
residual is g^2 - gbar^2 = a0 gbar + (2 - n) gbar u: n = 2 is EXACTLY the quadratic
"a0-line" law; n = 1 is the canonical law (T2). One structural number separates the
two law lines in the repo. -/
theorem T7_capacity_family (gb u a n : ℝ) (hrest : u ^ 2 + n * gb * u = a * gb) :
    (gb + u) ^ 2 - gb ^ 2 = a * gb + (2 - n) * gb * u := by
  have key : (gb + u) ^ 2 - gb ^ 2 - (a * gb + (2 - n) * gb * u)
      = u ^ 2 + n * gb * u - a * gb := by ring
  linarith

/-- T7_n2: the n = 2 (half-capacity) rest state IS the quadratic a0-line
g^2 - gbar^2 = a0 gbar with g = gbar + u — the G071/AG3-tested form. -/
theorem T7_n2_quadratic (gb u a : ℝ) (hrest : u ^ 2 + 2 * gb * u = a * gb) :
    (gb + u) ^ 2 - gb ^ 2 = a * gb := by
  have key : (gb + u) ^ 2 - gb ^ 2 - a * gb = u ^ 2 + 2 * gb * u - a * gb := by ring
  linarith

/-- T7_n2_not_canonical: the n = 2 rest state does NOT satisfy the canonical law unless
gbar*u = 0 — the two laws are genuinely distinct theories (anti-tautology clause: the
capacity number is load-bearing). -/
theorem T7_n2_not_canonical (gb u a : ℝ) (hrest : u ^ 2 + 2 * gb * u = a * gb)
    (hcan : (gb + u) ^ 2 = gb * ((gb + u) + a)) : gb * u = 0 := by
  have key : (gb + u) ^ 2 - gb * ((gb + u) + a) = u ^ 2 + gb * u - a * gb := by ring
  have h1 : u ^ 2 + gb * u - a * gb = 0 := by linarith
  have h2 : u ^ 2 + 2 * gb * u - a * gb = 0 := by linarith
  linarith

/-- T8: the ARGON02 P1 phantom-mass identity, derived from the rest state with the
point-mass baryon field. With gbar = a0/x^2 (x = r/r_M), u = a0 (s-1)/(2x^2),
s^2 = 1 + 4x^2: u solves the rest-state equation and M_ph/M_b = x^2 u/a0 = (s-1)/2. -/
theorem T8_phantom_mass (x s a u gb M : ℝ) (hx : 0 < x) (ha : 0 < a) (hs : s ^ 2 = 1 + 4 * x ^ 2)
    (hu : u * (2 * x ^ 2) = a * (s - 1)) (hgb : gb * x ^ 2 = a) (hM : M = x ^ 2 * u / a) :
    u ^ 2 + gb * u = a * gb ∧ M = (s - 1) / 2 := by
  have hx2 : x ^ 2 ≠ 0 := pow_ne_zero 2 hx.ne'
  have hu' : u = a * (s - 1) / (2 * x ^ 2) := by
    field_simp [hx2]
    linarith
  have hgb' : gb = a / x ^ 2 := by
    field_simp [hx2]
    linarith
  have hcore : (s - 1) ^ 2 + 2 * (s - 1) = 4 * x ^ 2 := by
    have h1 : (s - 1) ^ 2 + 2 * (s - 1) = s ^ 2 - 1 := by ring
    linarith [hs]
  constructor
  · rw [hu', hgb']
    field_simp [hx2, ha.ne']
    nlinarith [hcore, sq_nonneg a]
  · rw [hM, hu']
    field_simp [ha.ne', hx2]

/-- T9b: the two spellings of the explicit root coincide:
(sqrt(gbar^2 + 4 a0 gbar) - gbar)/2 = sqrt(a0 gbar + gbar^2/4) - gbar/2. -/
theorem T9b_root_form (gb a : ℝ) (hgb : 0 < gb) (ha : 0 < a) :
    (Real.sqrt (gb ^ 2 + 4 * a * gb) - gb) / 2 = Real.sqrt (a * gb + gb ^ 2 / 4) - gb / 2 := by
  have hsqE : (Real.sqrt (a * gb + gb ^ 2 / 4)) ^ 2 = a * gb + gb ^ 2 / 4 :=
    Real.sq_sqrt (by nlinarith : (0 : ℝ) ≤ a * gb + gb ^ 2 / 4)
  have h1 : (Real.sqrt (gb ^ 2 + 4 * a * gb)) ^ 2 = (2 * Real.sqrt (a * gb + gb ^ 2 / 4)) ^ 2 := by
    rw [Real.sq_sqrt (by nlinarith : (0 : ℝ) ≤ gb ^ 2 + 4 * a * gb), mul_pow, hsqE]
    ring
  have h2 : 0 ≤ Real.sqrt (gb ^ 2 + 4 * a * gb) := Real.sqrt_nonneg _
  have h3 : 0 ≤ 2 * Real.sqrt (a * gb + gb ^ 2 / 4) := by positivity
  rcases eq_or_eq_neg_of_sq_eq_sq (Real.sqrt (gb ^ 2 + 4 * a * gb))
      (2 * Real.sqrt (a * gb + gb ^ 2 / 4)) h1 with hp | hn
  · linarith
  · exfalso
    have hdpos : 0 < Real.sqrt (gb ^ 2 + 4 * a * gb) :=
      Real.sqrt_pos.mpr (by nlinarith : (0 : ℝ) < gb ^ 2 + 4 * a * gb)
    linarith [hn, hdpos, h3]

/-- T9: the deep-regime sandwich — the exact root u0 = sqrt(a0 gbar + gbar^2/4) - gbar/2
obeys sqrt(a0 gbar) - gbar/2 <= u0 <= sqrt(a0 gbar): g_ph -> sqrt(a0 gbar) as gbar/a0 -> 0,
the shared deep asymptote (g_ph -> C/r, the A/r^2 halo of GF2/AG1/ARGON02). -/
theorem T9_deep_sandwich (gb a : ℝ) (hgb : 0 < gb) (ha : 0 < a) :
    Real.sqrt (a * gb) - gb / 2 ≤ Real.sqrt (a * gb + gb ^ 2 / 4) - gb / 2 ∧
    Real.sqrt (a * gb + gb ^ 2 / 4) - gb / 2 ≤ Real.sqrt (a * gb) := by
  constructor
  · have h : a * gb ≤ a * gb + gb ^ 2 / 4 := by nlinarith [sq_nonneg gb]
    have hm := Real.sqrt_le_sqrt h
    linarith
  · have hsq : a * gb + gb ^ 2 / 4 ≤ (Real.sqrt (a * gb) + gb / 2) ^ 2 := by
      have h1 : 0 ≤ Real.sqrt (a * gb) := Real.sqrt_nonneg _
      nlinarith [Real.sq_sqrt (by nlinarith : (0 : ℝ) ≤ a * gb), sq_nonneg gb]
    have hnonneg : 0 ≤ Real.sqrt (a * gb) + gb / 2 := by positivity
    have hstep : Real.sqrt (a * gb + gb ^ 2 / 4) ≤ Real.sqrt (a * gb) + gb / 2 :=
      Real.sqrt_le_iff.mpr ⟨hnonneg, hsq⟩
    linarith

end AG4

end noncomputable section

#print axioms AG4.T1_eom_bridge
#print axioms AG4.T2_rest_state_to_law
#print axioms AG4.T3_law_to_rest_state
#print axioms AG4.T4_rest_state_unique
#print axioms AG4.T5_tether_bound
#print axioms AG4.T6_explicit_root
#print axioms AG4.T7_capacity_family
#print axioms AG4.T7_n2_quadratic
#print axioms AG4.T7_n2_not_canonical
#print axioms AG4.T8_phantom_mass
#print axioms AG4.T9b_root_form
#print axioms AG4.T9_deep_sandwich
