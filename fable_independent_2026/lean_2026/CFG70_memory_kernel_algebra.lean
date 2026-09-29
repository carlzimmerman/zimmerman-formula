import Mathlib

/-!
# MineM1-G: the retarded memory-kernel algebra of CFG70 (Laplace-domain reaction, static limit, exponential-kernel ramp response)

Source lane: campaign_fresh_gravity/CFG70_memory_kernel_exchange/cfg70_memory_kernel_exchange.py, check D3 (lines 121-148, the check itself at 147):
  sympy "a-hat(s) = r K-hat/s + c (1 - K-hat) theta^T-hat, K-hat = 1/(1 + s Gamma-hat/c)", the static limit "s a-hat -> r", and the dsolve ramp closed form
  "a = r (1 - e^{-t/tau}) + c A tau (1 - e^{-t/tau})".  (Overlap check: grep for laplace / memory kernel in the Lean corpus finds nothing; ChainCert/Exchange.lean is CFG72's Gauss-law mediator, a different algebra.)

CERTIFIED (premises => conclusions; pure algebra/calculus; the fluid equation below is the lane's action-derived equation and is a HYPOTHESIS here):
* `laplace_reaction`: from r/s + c (theta - Theta) + s Gamma-hat theta = 0 (c != 0, s != 0, c + s Gamma-hat != 0) the reaction a-hat = -c(theta - Theta) equals r K-hat/s + c (1 - K-hat) Theta.
* `Khat_zero`: K-hat(0) = 1 (kernel normalised).  `static_limit`: for a step target Theta = A/s, s a-hat = r K-hat + c A (1 - K-hat) -> r as s -> 0 whenever Gamma-hat is continuous at 0 (A drops out).
* `relax_solution`, `relax_unique`: for the exponential (Newton) kernel, gamma theta' = -(r + c (theta - A t)), theta(0) = 0 has the UNIQUE solution theta = A t - a/c with
  a(t) = (r + c A tau)(1 - exp(-t/tau)), tau = gamma/c.

NOT certified: the doubled Schwinger-Keldysh action and its variation (sympy D1, D2), causality of the discrete action (S2, numerical), reciprocity, the size of the reaction relative to g_law
(P1, numerical), the energy budget (P2) or that any kernel time scale can be tied to a0, c, H0 (P4, a scoped negative in the lane).  Nothing here says a memory-kernel closure works.
kappa = 1/2 is FITTED; nothing here says the theory is closed.
-/

open Filter Topology Real

namespace MineM1

/-- the memory kernel in the Laplace domain: K-hat(s) = 1/(1 + s Gamma-hat(s)/c) -/
noncomputable def Khat (c s Γh : ℝ) : ℝ := 1 / (1 + s * Γh / c)

/-- D3 (Laplace algebra): the fluid equation r/s + c(theta - Theta) + s Gamma theta = 0 (theta(0) = 0, theta^T(0) = 0) gives the probe reaction
    a-hat = -c (theta - Theta) = r K-hat/s + c (1 - K-hat) Theta, for a general retarded kernel Gamma-hat. -/
theorem laplace_reaction {c s Γh r θ Θ : ℝ} (hc : c ≠ 0) (hs : s ≠ 0) (hden : c + s * Γh ≠ 0)
    (h : r / s + c * (θ - Θ) + Γh * s * θ = 0) :
    -c * (θ - Θ) = r * Khat c s Γh / s + c * (1 - Khat c s Γh) * Θ := by
  unfold Khat
  have h1 : 1 + s * Γh / c ≠ 0 := by
    intro h0; apply hden
    have : c * (1 + s * Γh / c) = c + s * Γh := by field_simp
    rw [← this, h0, mul_zero]
  have hθ : θ = (c * Θ - r / s) / (c + s * Γh) := by
    field_simp at h ⊢
    linarith
  rw [hθ]
  field_simp
  ring

/-- normalisation: K-hat(0) = 1 (the kernel integrates to 1) -/
theorem Khat_zero {c Γh : ℝ} : Khat c 0 Γh = 1 := by simp [Khat]

/-- static limit: for a step target Theta = A/s, s * a-hat = r K + c A (1 - K) -> r as s -> 0 whenever Gamma-hat is continuous at 0 and c != 0 -/
theorem static_limit {c r A : ℝ} {Γ : ℝ → ℝ} (hΓ : ContinuousAt Γ 0) :
    Tendsto (fun s => r * Khat c s (Γ s) + c * A * (1 - Khat c s (Γ s))) (𝓝 0) (𝓝 r) := by
  have h1 : ContinuousAt (fun s => 1 + s * Γ s / c) 0 := by
    have : ContinuousAt (fun s : ℝ => s * Γ s) 0 := continuousAt_id.mul hΓ
    exact (this.div_const c).const_add 1
  have hK : ContinuousAt (fun s => Khat c s (Γ s)) 0 := by
    unfold Khat
    exact continuousAt_const.div h1 (by simp)
  have hc' : ContinuousAt (fun s => r * Khat c s (Γ s) + c * A * (1 - Khat c s (Γ s))) 0 :=
    (continuousAt_const.mul hK).add (continuousAt_const.mul (continuousAt_const.sub hK))
  have h0 := hc'.tendsto
  simpa [Khat] using h0

/-- exponential-kernel relaxation on a ramp target theta^T = A t:  gamma theta' = -(r + c (theta - A t)), theta(0) = 0 is solved by theta = A t - a/c with
    a(t) = (r + c A tau)(1 - exp(-t/tau)), tau = gamma/c -/
noncomputable def aRelax (r c A τ t : ℝ) : ℝ := (r + c * A * τ) * (1 - Real.exp (-t / τ))

theorem relax_solution {r c A γ : ℝ} (hc : 0 < c) (hγ : 0 < γ) (t : ℝ) :
    HasDerivAt (fun t => A * t - aRelax r c A (γ / c) t / c) (A - (r + c * A * (γ / c)) * Real.exp (-t / (γ / c)) / (γ / c) / c) t ∧
    γ * (A - (r + c * A * (γ / c)) * Real.exp (-t / (γ / c)) / (γ / c) / c) = -(r + c * ((A * t - aRelax r c A (γ / c) t / c) - A * t)) ∧
    A * 0 - aRelax r c A (γ / c) 0 / c = 0 := by
  have hτ : γ / c ≠ 0 := by positivity
  refine ⟨?_, ?_, ?_⟩
  · have h1 : HasDerivAt (fun t : ℝ => Real.exp (-t / (γ / c))) (Real.exp (-t / (γ / c)) * (-1 / (γ / c))) t := by
      have := (((hasDerivAt_id t).neg).div_const (γ / c)).exp
      simpa using this
    have h2 := (h1.const_sub 1).const_mul (r + c * A * (γ / c))
    have h3 := ((hasDerivAt_id t).const_mul A).sub (h2.div_const c)
    refine h3.congr_deriv ?_
    field_simp
  · unfold aRelax
    field_simp
    ring
  · simp [aRelax]


/-- UNIQUENESS: any differentiable solution of gamma theta' = -(r + c (theta - A t)) with theta(0) = 0 equals the closed form. -/
theorem relax_unique {r c A γ : ℝ} (hc : 0 < c) (hγ : 0 < γ) {θ θ' : ℝ → ℝ}
    (hd : ∀ t, HasDerivAt θ (θ' t) t) (hode : ∀ t, γ * θ' t = -(r + c * (θ t - A * t))) (h0 : θ 0 = 0) :
    ∀ t, θ t = A * t - aRelax r c A (γ / c) t / c := by
  set sol : ℝ → ℝ := fun t => A * t - aRelax r c A (γ / c) t / c with hsol
  have hsd : ∀ t, HasDerivAt sol (A - (r + c * A * (γ / c)) * Real.exp (-t / (γ / c)) / (γ / c) / c) t :=
    fun t => (relax_solution (r := r) (A := A) hc hγ t).1
  set w : ℝ → ℝ := fun t => (θ t - sol t) * Real.exp (c / γ * t) with hw
  have hwd : ∀ t, HasDerivAt w 0 t := by
    intro t
    have he : HasDerivAt (fun t : ℝ => Real.exp (c / γ * t)) (Real.exp (c / γ * t) * (c / γ)) t := by
      simpa using ((hasDerivAt_id t).const_mul (c / γ)).exp
    have := ((hd t).sub (hsd t)).mul he
    refine this.congr_deriv ?_
    have e1 := hode t
    have e2 := (relax_solution (r := r) (A := A) hc hγ t).2.1
    have hγ0 : γ ≠ 0 := hγ.ne'
    have hc0 : c ≠ 0 := hc.ne'
    have hθ' : θ' t = -(r + c * (θ t - A * t)) / γ := by field_simp; linarith
    have hs_t : sol t = A * t - aRelax r c A (γ / c) t / c := rfl
    have hs' : A - (r + c * A * (γ / c)) * Real.exp (-t / (γ / c)) / (γ / c) / c
        = -(r + c * (sol t - A * t)) / γ := by
      rw [hs_t]
      field_simp
      field_simp at e2
      linarith
    rw [hθ', hs']
    simp only [Pi.sub_apply]
    field_simp
    ring
  have hconst : ∀ t, w t = w 0 :=
    fun t => is_const_of_deriv_eq_zero (fun x => (hwd x).differentiableAt) (fun x => (hwd x).deriv) t 0
  intro t
  have hw0 : w 0 = 0 := by simp [hw, h0, hsol, aRelax]
  have := hconst t
  rw [hw0] at this
  simp only [hw] at this
  have hpos : Real.exp (c / γ * t) ≠ 0 := (Real.exp_pos _).ne'
  have := (mul_eq_zero.1 this).resolve_right hpos
  linarith


end MineM1

open MineM1 in
#print axioms laplace_reaction
open MineM1 in
#print axioms static_limit
open MineM1 in
#print axioms relax_solution
open MineM1 in
#print axioms relax_unique
