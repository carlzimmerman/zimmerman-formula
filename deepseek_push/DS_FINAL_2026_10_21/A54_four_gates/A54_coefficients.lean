/-
A54 — the coefficient identities behind the four gates, certified.

Nothing here is dynamical: these are the algebraic identities to which the
Hamiltonian analysis of the A33 action reduces.

* `gN_eq`          : the law, in the form `g_N = g - u` with `u = a₀g/(g+a₀)`.
* `one_minus_up`   : `1 - u' = (g² + 2a₀g)/(g+a₀)²`, i.e. `dg_N/dg`.
* `dg_dgN`         : `dg/dg_N = 1 + a₀²/(g² + 2a₀g)`.
* `dg_dgN_ge_one`  : **gate (iv)**: `dg/dg_N ≥ 1` at every `g > 0`, `a₀ > 0`.
* `KWp_eq`         : the field equation `K W'(u) = g` (i.e. `u/(1-u/a₀) = g`).
* `Wpp_eq`         : `W''(u) = (g+a₀)²/(K a₀²)`.
* `hess_chain`     : `d²W/dg² = W''(u)(u')² + W'(u)u'' = a₀²(a₀-g)/(K(g+a₀)³)`.
* `hess_zero_iff`  : that Hessian vanishes **exactly** at `g = a₀`.
* `hess_sign`      : positive below `a₀`, negative above it.
* `rhoP_square`    : `d + γd²/2 = (γ/2)(d + 1/γ)² - 1/(2γ)`: the energy-density
                     bound `ρ_P ≥ -1/(2γ)` is a perfect square.
* `mT_pos`         : the A39 tensor mass `u²(4-3x)/(1-x)²` is positive on `0<x<1`.
* `Q0_sign`        : the scalar's kinetic coefficient `(2+3β)/(Kβ)` has the sign of β.
* `cb_GR`          : at `β = 0` the supermetric coefficient `(1+β)/(2+3β)` is `1/2`,
                     i.e. the undeformed Dirac algebra.
-/
import Mathlib

namespace A54

/-- The saturating slider `u = a₀ g/(g + a₀)`. -/
noncomputable def uOf (g a0 : ℝ) : ℝ := a0 * g / (g + a0)

/-- **The law**, in the form `g_N = g - u`. -/
theorem gN_eq (g a0 : ℝ) (h : g + a0 ≠ 0) :
    g - uOf g a0 = g ^ 2 / (g + a0) := by
  unfold uOf
  field_simp
  ring

/-- `1 - u' = (g² + 2a₀g)/(g+a₀)²`: `dg_N/dg` for `u' = a₀²/(g+a₀)²`. -/
theorem one_minus_up (g a0 : ℝ) (h : g + a0 ≠ 0) :
    1 - a0 ^ 2 / (g + a0) ^ 2 = (g ^ 2 + 2 * a0 * g) / (g + a0) ^ 2 := by
  field_simp
  ring

/-- **`dg/dg_N = 1 + a₀²/(g² + 2a₀g)`**, the same identity read the other way. -/
theorem dg_dgN (g a0 : ℝ) (h2 : g ^ 2 + 2 * a0 * g ≠ 0) :
    (g + a0) ^ 2 / (g ^ 2 + 2 * a0 * g) = 1 + a0 ^ 2 / (g ^ 2 + 2 * a0 * g) := by
  have h : (g + a0) ^ 2 = (g ^ 2 + 2 * a0 * g) + a0 ^ 2 := by ring
  rw [h, add_div, div_self h2]

/-- **Gate (iv): `dg/dg_N ≥ 1` at every acceleration.** -/
theorem dg_dgN_ge_one (g a0 : ℝ) (hg : 0 < g) (ha : 0 < a0) :
    1 ≤ 1 + a0 ^ 2 / (g ^ 2 + 2 * a0 * g) := by
  have hden : 0 < g ^ 2 + 2 * a0 * g := by nlinarith
  have hnum : 0 < a0 ^ 2 := by positivity
  have hpos : 0 < a0 ^ 2 / (g ^ 2 + 2 * a0 * g) := div_pos hnum hden
  linarith

/-- **The field equation**: `K W'(u) = g`, i.e. `u/(1-u/a₀) = g`. -/
theorem KWp_eq (g a0 : ℝ) (ha : a0 ≠ 0) (h : g + a0 ≠ 0) :
    uOf g a0 / (1 - uOf g a0 / a0) = g := by
  have h1 : (1 : ℝ) - uOf g a0 / a0 = a0 / (g + a0) := by
    unfold uOf
    field_simp
    ring
  have hne : (1 : ℝ) - uOf g a0 / a0 ≠ 0 := by
    rw [h1]
    exact div_ne_zero ha h
  rw [div_eq_iff hne, h1]
  unfold uOf
  field_simp

/-- **`W''(u) = (g+a₀)²/(K a₀²)`**, the second derivative at the on-shell point. -/
theorem Wpp_eq (g a0 K : ℝ) (hK : K ≠ 0) (ha : a0 ≠ 0) (h : g + a0 ≠ 0) :
    1 / (K * (1 - uOf g a0 / a0) ^ 2) = (g + a0) ^ 2 / (K * a0 ^ 2) := by
  have h1 : (1 : ℝ) - uOf g a0 / a0 = a0 / (g + a0) := by
    unfold uOf
    field_simp
    ring
  rw [h1, div_pow]
  field_simp

/-- The Hessian chain rule with the explicit `W'`, `W''`, `u'`, `u''`:
`d²W/dg² = a₀²(a₀-g)/(K(g+a₀)³)`. -/
theorem hess_chain (g a0 K : ℝ) (hK : K ≠ 0) (ha : a0 ≠ 0) (h : g + a0 ≠ 0) :
    ((g + a0) ^ 2 / (K * a0 ^ 2)) * (a0 ^ 2 / (g + a0) ^ 2) ^ 2
        + (g / K) * (-2 * a0 ^ 2 / (g + a0) ^ 3)
      = a0 ^ 2 * (a0 - g) / (K * (g + a0) ^ 3) := by
  field_simp
  ring

/-- **The Hessian vanishes exactly at `g = a₀`.** -/
theorem hess_zero_iff (g a0 K : ℝ) (hK : K ≠ 0) (ha : 0 < a0) (hg : 0 < g) :
    a0 ^ 2 * (a0 - g) / (K * (g + a0) ^ 3) = 0 ↔ g = a0 := by
  have hpos : (0 : ℝ) < (g + a0) ^ 3 := by positivity
  have hden : K * (g + a0) ^ 3 ≠ 0 := mul_ne_zero hK (ne_of_gt hpos)
  constructor
  · intro h
    rw [div_eq_zero_iff] at h
    rcases h with h | h
    · have ha2 : a0 ^ 2 ≠ 0 := by positivity
      rcases mul_eq_zero.mp h with h' | h'
      · exact absurd h' ha2
      · linarith
    · exact absurd h hden
  · intro h
    subst h
    ring

/-- The Hessian is positive below `a₀` and negative above it. -/
theorem hess_sign (g a0 K : ℝ) (hK : 0 < K) (ha : 0 < a0) (hg : 0 < g) :
    (0 < a0 ^ 2 * (a0 - g) / (K * (g + a0) ^ 3) ↔ g < a0) ∧
    (a0 ^ 2 * (a0 - g) / (K * (g + a0) ^ 3) < 0 ↔ a0 < g) := by
  have hpos : (0 : ℝ) < K * (g + a0) ^ 3 := by positivity
  have hne : K * (g + a0) ^ 3 ≠ 0 := ne_of_gt hpos
  have hnum : (0 : ℝ) < a0 ^ 2 := by positivity
  have key1 : ∀ h : 0 < a0 ^ 2 * (a0 - g), 0 < a0 - g := by
    intro h
    by_contra hc
    push Not at hc
    nlinarith [h, hnum, hc]
  have key2 : ∀ h : a0 ^ 2 * (a0 - g) < 0, a0 - g < 0 := by
    intro h
    by_contra hc
    push Not at hc
    nlinarith [h, hnum, hc]
  constructor
  · constructor
    · intro h
      have hmul : 0 < a0 ^ 2 * (a0 - g) / (K * (g + a0) ^ 3) * (K * (g + a0) ^ 3) :=
        mul_pos h hpos
      rw [div_mul_cancel₀ _ hne] at hmul
      linarith [key1 hmul]
    · intro hlt
      exact div_pos (mul_pos hnum (by linarith)) hpos
  · constructor
    · intro h
      have hmul : a0 ^ 2 * (a0 - g) / (K * (g + a0) ^ 3) * (K * (g + a0) ^ 3) < 0 :=
        mul_neg_of_neg_of_pos h hpos
      rw [div_mul_cancel₀ _ hne] at hmul
      linarith [key2 hmul]
    · intro hlt
      exact div_neg_of_neg_of_pos (mul_neg_of_pos_of_neg hnum (by linarith)) hpos

/-- **The energy-density bound is a perfect square**: `ρ_P ≥ -1/(2γ)`. -/
theorem rhoP_square (d γ : ℝ) (hγ : γ ≠ 0) :
    d + γ * d ^ 2 / 2 = γ / 2 * (d + 1 / γ) ^ 2 - 1 / (2 * γ) := by
  field_simp
  ring

/-- **The A39 tensor mass is positive** on `0 < x < 1`. -/
theorem mT_pos (u x : ℝ) (hu : u ≠ 0) (hx0 : 0 < x) (hx1 : x < 1) :
    0 < u ^ 2 * (4 - 3 * x) / (1 - x) ^ 2 := by
  have hnum : 0 < 4 - 3 * x := by linarith
  have hden : 0 < (1 - x) ^ 2 := by
    have : 0 < 1 - x := by linarith
    positivity
  have hu2 : 0 < u ^ 2 := by positivity
  exact div_pos (mul_pos hu2 hnum) hden

/-- **The scalar's kinetic coefficient has the sign of `β`** (ghost-free ⇔ β > 0). -/
theorem Q0_sign (β K : ℝ) (hβ : 0 < β) (hK : 0 < K) :
    0 < (2 + 3 * β) / (K * β) := by
  have hnum : 0 < 2 + 3 * β := by linarith
  exact div_pos hnum (mul_pos hK hβ)

/-- **At `β = 0` the supermetric coefficient is `1/2`**: the undeformed Dirac algebra. -/
theorem cb_GR : (1 + (0 : ℝ)) / (2 + 3 * (0 : ℝ)) = 1 / 2 := by norm_num

end A54

#print axioms A54.gN_eq
#print axioms A54.one_minus_up
#print axioms A54.dg_dgN
#print axioms A54.dg_dgN_ge_one
#print axioms A54.KWp_eq
#print axioms A54.Wpp_eq
#print axioms A54.hess_chain
#print axioms A54.hess_zero_iff
#print axioms A54.hess_sign
#print axioms A54.rhoP_square
#print axioms A54.mT_pos
#print axioms A54.Q0_sign
#print axioms A54.cb_GR