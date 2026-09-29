import Mathlib

/-!
# MineM5-G: the (v/c)^2 kinematic suppression of the nonlocal action's u-contraction, for an ARBITRARY kernel K

Source lane: real_research/reviews/mi_nonlocal_amplitude_nogo_2026.py, N1-N4 (lines ~62-150): "u^mu K(Box_u/a0^2) u_mu = -gamma^2 K(0) + (gamma^2 v^2/c^2) K(z), z = -(gamma Omega c/a0)^2, derived with K an UNSPECIFIED sympy Function";
  "N2 the time-leg term has zero derivative w.r.t. Omega and R"; "N3 |K| >= DEF c^2/(gamma^2 v^2)"; "N4b MUTATION: without the prefactor the requirement is O(1)".

MODEL (the lane's premise, computed there in sympy): on the circular worldline u = gamma e_t + gamma beta e_phi with Box_u e_t = 0 and Box_u e_phi = lam e_phi (lam = -(gamma Omega)^2), the Lorentzian form
g = diag(-1, 1) on the orthogonal pair (e_t, e_phi), and K(Box_u) acts on this eigenbasis by K(0), K(lam).

CERTIFIED (real algebra; K an arbitrary function R -> R):
* `contraction_block`: g(u, K(Box)u) = -gamma^2 K(0) + gamma^2 beta^2 K(lam).
* `modification_formula`: if gamma^2 (1 - beta^2) = 1 and K(0) = 1 (Newtonian normalisation) then g(u, K u) + 1 = gamma^2 beta^2 (K(lam) - 1): the ENTIRE acceleration-dependent change carries the prefactor gamma^2 beta^2.
* `modification_bound`: if |K(lam)| <= Kmax then |g(u, K u) + 1| <= gamma^2 beta^2 (1 + Kmax).
* `required_kernel`: to produce a modification of size d > 0 one needs Kmax >= d/(gamma^2 beta^2) - 1 = d (1 - beta^2)/beta^2 - 1, so the required kernel amplitude blows up like (c/v)^2 for ANY kernel.
* `required_kernel_beta`: the same bound in beta alone, d (1 - beta^2)/beta^2 - 1 <= Kmax.  (The lane's mutation control, deleting the prefactor, is not a separate theorem: `modification_formula` shows the
  change is gamma^2 beta^2 (K(lam) - 1), so without the prefactor the requirement is |K(lam) - 1| = d, O(1) by inspection.)

NOT certified: the eigen-decomposition of u under Box_u (a premise here; it is the sympy block computation in the lane and is consistent with the Frenet model of MineM5-D); the action S = -(1/2) int sqrt(-g) rho_m s u K(Box_u/a0^2) u
being the framework's published action; the deficit 1 - mu_fw(1) = 0.382 (numeric, needs mu_fw(1) and the law); the numerical shortfall ~1e6 (needs galactic speeds); N5-N6 (the other horn: local F(|a|^2) form;
that is the MineM5-F territory).  As the lane says, this closes a FORM CLASS only (actions quadratic in u with a bounded function of Box_u); it does NOT show modified inertia is impossible.
kappa = 1/2 is FITTED; nothing here says the theory is closed.
-/

namespace MineM5G

/-- Lorentzian form on the (e_t, e_phi) coefficient pair -/
def g (w w' : ℝ × ℝ) : ℝ := -(w.1 * w'.1) + w.2 * w'.2

/-- K(Box) on the eigenbasis: e_t has eigenvalue 0, e_phi has eigenvalue lam -/
def Kop (K : ℝ → ℝ) (lam : ℝ) (w : ℝ × ℝ) : ℝ × ℝ := (K 0 * w.1, K lam * w.2)

/-- the u-contraction block decomposition: -gamma^2 K(0) + gamma^2 beta^2 K(lam) -/
theorem contraction_block (K : ℝ → ℝ) (lam γ β : ℝ) :
    g (γ, γ * β) (Kop K lam (γ, γ * β)) = -γ ^ 2 * K 0 + γ ^ 2 * β ^ 2 * K lam := by
  simp [g, Kop]; ring

/-- with gamma^2 (1 - beta^2) = 1 and K(0) = 1, the change from -1 is gamma^2 beta^2 (K(lam) - 1) -/
theorem modification_formula (K : ℝ → ℝ) (lam γ β : ℝ) (hn : γ ^ 2 * (1 - β ^ 2) = 1) (hK0 : K 0 = 1) :
    g (γ, γ * β) (Kop K lam (γ, γ * β)) + 1 = γ ^ 2 * β ^ 2 * (K lam - 1) := by
  rw [contraction_block, hK0]
  nlinarith [hn]

/-- |change| <= gamma^2 beta^2 (1 + Kmax) whenever |K(lam)| <= Kmax -/
theorem modification_bound (K : ℝ → ℝ) (lam γ β Kmax : ℝ) (hn : γ ^ 2 * (1 - β ^ 2) = 1) (hK0 : K 0 = 1)
    (hKm : |K lam| ≤ Kmax) :
    |g (γ, γ * β) (Kop K lam (γ, γ * β)) + 1| ≤ γ ^ 2 * β ^ 2 * (1 + Kmax) := by
  rw [modification_formula K lam γ β hn hK0, abs_mul, abs_of_nonneg (by positivity : 0 ≤ γ ^ 2 * β ^ 2)]
  apply mul_le_mul_of_nonneg_left _ (by positivity)
  calc |K lam - 1| ≤ |K lam| + |(1 : ℝ)| := abs_sub _ _
    _ ≤ Kmax + 1 := by rw [abs_one]; linarith
    _ = 1 + Kmax := by ring

/-- to produce a change of size d > 0 the kernel must reach Kmax >= d/(gamma^2 beta^2) - 1 (beta != 0) -/
theorem required_kernel (K : ℝ → ℝ) (lam γ β Kmax d : ℝ) (hn : γ ^ 2 * (1 - β ^ 2) = 1) (hK0 : K 0 = 1)
    (hKm : |K lam| ≤ Kmax) (hβ : β ≠ 0) (hγ : γ ≠ 0)
    (hd : |g (γ, γ * β) (Kop K lam (γ, γ * β)) + 1| = d) :
    d / (γ ^ 2 * β ^ 2) - 1 ≤ Kmax := by
  have hb := modification_bound K lam γ β Kmax hn hK0 hKm
  rw [hd] at hb
  have hpos : 0 < γ ^ 2 * β ^ 2 := by positivity
  have : d / (γ ^ 2 * β ^ 2) ≤ 1 + Kmax := by
    rw [div_le_iff₀ hpos]; linarith
  linarith

/-- the required amplitude in terms of beta alone: d (1 - beta^2)/beta^2 - 1 <= Kmax -/
theorem required_kernel_beta (K : ℝ → ℝ) (lam γ β Kmax d : ℝ) (hn : γ ^ 2 * (1 - β ^ 2) = 1) (hK0 : K 0 = 1)
    (hKm : |K lam| ≤ Kmax) (hβ : β ≠ 0) (hγ : γ ≠ 0)
    (hd : |g (γ, γ * β) (Kop K lam (γ, γ * β)) + 1| = d) :
    d * (1 - β ^ 2) / β ^ 2 - 1 ≤ Kmax := by
  have h := required_kernel K lam γ β Kmax d hn hK0 hKm hβ hγ hd
  have e : d / (γ ^ 2 * β ^ 2) = d * (1 - β ^ 2) / β ^ 2 := by
    have hβ2 : β ^ 2 ≠ 0 := pow_ne_zero 2 hβ
    have hγ2 : γ ^ 2 ≠ 0 := pow_ne_zero 2 hγ
    field_simp
    have h2 : d * γ ^ 2 * (1 - β ^ 2) = d := by
      calc d * γ ^ 2 * (1 - β ^ 2) = d * (γ ^ 2 * (1 - β ^ 2)) := by ring
        _ = d := by rw [hn, mul_one]
    linarith
  rw [e] at h
  exact h

end MineM5G

#print axioms MineM5G.contraction_block
#print axioms MineM5G.modification_formula
#print axioms MineM5G.modification_bound
#print axioms MineM5G.required_kernel
#print axioms MineM5G.required_kernel_beta
