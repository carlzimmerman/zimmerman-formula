import Mathlib

/-!
# AH3 -- Lean certificates for the alpha no-go (AH1 pair production, AH2 induced current)

WHAT IS CERTIFIED (mathematics only; premises => conclusions):
* `obs_rescale`, `no_coupling_from_obs`, `no_alpha_from_obs`: if an observable Phi depends on the charge e and the field E only through
  lambda = e E / H^2 (and on the mass only through mu = m/H), then for any two couplings the same value is reached by rescaling E,
  so NO function of the observable recovers e or alpha = e^2/(4 pi).
* `alpha_of_tie`, `eps_star_iff`, `eps_star_bounds`: under the tie lambda = kappa, alpha = kappa^2 / (4 pi eps^2) with eps = E/H^2, and the
  eps that would give alpha = 1/137.036 at kappa = 1/2 lies in (1.64, 1.66) (script value 1.6511).  This makes eps a stated INPUT, not a result.
* `pair_difference_cleared`, `pair_difference`: the hand-derived identity N_+ - N_- = sinh(2 pi lambda)/sinh(2 pi rho) for the Bogoliubov
  numbers N_pm = r_pm/(1 - r_pm), r_pm = e^{-2 pi rho} cosh(pi(lambda pm rho))/cosh(pi(lambda mp rho)).
* `Jclosed_odd`, `Jclosed_at_quarter`: the published closed form J/(eH) = (1/pi) rho sinh(2 pi lambda)/sinh(2 pi rho) is odd in lambda and
  is exactly lambda/pi at rho = lambda (the m^2 = H^2/4 linear response).
* `tie_coupling_differs`: a conductivity tie sigma H = (e^2/H^2) g(mu) = c gives different required couplings at masses with different g.

NOT CERTIFIED: that the pair-production factor or the current has the form Phi(lambda, mu) (that is the content of AH1/AH2's committed
numerical checks: analytic = numerical, thermal and flat-space limits, direct mode sum = closed form); that no OTHER mechanism can fix alpha
(this is a no-go for observables of this class, not for the physics); any statement in 4D (the rate and current are the dS_2 toy);
the values of g(mu) (script AH2); kappa = 1/2 (FITTED).  Lean checks mathematics, not whether the world is this way.
Zero sorry.  Axioms printed at the bottom.
-/

noncomputable section

open Real

/-- lambda = e E / H^2, the field strength in horizon units. -/
def lam (e E H : ℝ) : ℝ := e * E / H ^ 2

/-- An observable that sees the charge and field only through lambda and the mass only through mu = m/H. -/
def obs (Φ : ℝ → ℝ → ℝ) (e E m H : ℝ) : ℝ := Φ (lam e E H) (m / H)

/-- Rescaling E by e1/e2 leaves lambda, hence every such observable, unchanged. -/
theorem obs_rescale (Φ : ℝ → ℝ → ℝ) {e₁ e₂ E₁ m H : ℝ} (he₂ : e₂ ≠ 0) :
    obs Φ e₂ (e₁ * E₁ / e₂) m H = obs Φ e₁ E₁ m H := by
  have h : e₂ * (e₁ * E₁ / e₂) / H ^ 2 = e₁ * E₁ / H ^ 2 := by
    field_simp
  simp only [obs, lam, h]

/-- No function of the observable recovers the coupling e. -/
theorem no_coupling_from_obs (Φ : ℝ → ℝ → ℝ) (m H : ℝ) :
    ¬ ∃ f : ℝ → ℝ, ∀ e E : ℝ, 0 < e → f (obs Φ e E m H) = e := by
  rintro ⟨f, hf⟩
  have h1 := hf 1 1 one_pos
  have h2 := hf 2 (1 / 2) two_pos
  have hs : obs Φ 2 (1 / 2) m H = obs Φ 1 1 m H := by
    have := obs_rescale Φ (e₁ := 1) (e₂ := 2) (E₁ := 1) (m := m) (H := H) (by norm_num)
    simpa using this
  rw [hs, h1] at h2
  norm_num at h2

/-- No function of the observable recovers alpha = e^2/(4 pi). -/
theorem no_alpha_from_obs (Φ : ℝ → ℝ → ℝ) (m H : ℝ) :
    ¬ ∃ f : ℝ → ℝ, ∀ e E : ℝ, 0 < e → f (obs Φ e E m H) = e ^ 2 / (4 * π) := by
  rintro ⟨f, hf⟩
  have h1 := hf 1 1 one_pos
  have h2 := hf 2 (1 / 2) two_pos
  have hs : obs Φ 2 (1 / 2) m H = obs Φ 1 1 m H := by
    have := obs_rescale Φ (e₁ := 1) (e₂ := 2) (E₁ := 1) (m := m) (H := H) (by norm_num)
    simpa using this
  rw [hs, h1] at h2
  have hpi : 0 < π := Real.pi_pos
  field_simp at h2
  linarith

/-- Under the tie lambda = kappa, alpha is kappa^2/(4 pi eps^2) with eps = E/H^2: it is set by eps, which the tie does not supply. -/
theorem alpha_of_tie (κ e E H : ℝ) (hH : H ≠ 0) (hE : E ≠ 0) (h : lam e E H = κ) :
    e ^ 2 / (4 * π) = κ ^ 2 / (4 * π * (E / H ^ 2) ^ 2) := by
  have he : e = κ * H ^ 2 / E := by
    unfold lam at h
    field_simp at h ⊢
    linarith
  rw [he]
  field_simp

/-- The eps that gives a stated alpha under the tie. -/
theorem eps_star_iff {κ α ε : ℝ} (hκ : 0 < κ) (hα : 0 < α) (hε : 0 < ε) :
    κ ^ 2 / (4 * π * ε ^ 2) = α ↔ ε = κ / Real.sqrt (4 * π * α) := by
  have hpi : 0 < π := Real.pi_pos
  have hpos : 0 < 4 * π * α := by positivity
  have hs : 0 < Real.sqrt (4 * π * α) := Real.sqrt_pos.mpr hpos
  have hss : Real.sqrt (4 * π * α) ^ 2 = 4 * π * α := Real.sq_sqrt hpos.le
  rw [eq_div_iff hs.ne']
  constructor
  · intro h
    have h' : κ ^ 2 = α * (4 * π * ε ^ 2) := by
      field_simp at h
      linarith
    have hsq : (ε * Real.sqrt (4 * π * α)) ^ 2 = κ ^ 2 := by
      rw [mul_pow, hss]
      nlinarith [h']
    have hp : 0 < ε * Real.sqrt (4 * π * α) := mul_pos hε hs
    nlinarith [hsq, hp, hκ, sq_nonneg (ε * Real.sqrt (4 * π * α) - κ), sq_nonneg (ε * Real.sqrt (4 * π * α) + κ)]
  · intro h
    have h2 : (ε * Real.sqrt (4 * π * α)) ^ 2 = κ ^ 2 := by rw [h]
    rw [mul_pow, hss] at h2
    field_simp
    nlinarith [h2]

/-- At kappa = 1/2 and alpha = 1/137.036 the required eps is between 1.64 and 1.66 (the script value is 1.6511). -/
theorem eps_star_bounds : 1.64 < (1 / 2 : ℝ) / Real.sqrt (4 * π * (1 / 137.036)) ∧
    (1 / 2 : ℝ) / Real.sqrt (4 * π * (1 / 137.036)) < 1.66 := by
  have h3 : (3.14 : ℝ) < π := Real.pi_gt_d2
  have h4 : π < (3.15 : ℝ) := Real.pi_lt_d2
  have hpos : (0 : ℝ) < 4 * π * (1 / 137.036) := by positivity
  have hsq : 0 < Real.sqrt (4 * π * (1 / 137.036)) := Real.sqrt_pos.mpr hpos
  constructor
  · rw [lt_div_iff₀ hsq]
    have : Real.sqrt (4 * π * (1 / 137.036)) < 0.5 / 1.64 := by
      rw [Real.sqrt_lt' (by norm_num)]
      nlinarith
    nlinarith
  · rw [div_lt_iff₀ hsq]
    have : 0.5 / 1.66 < Real.sqrt (4 * π * (1 / 137.036)) := by
      rw [Real.lt_sqrt (by norm_num)]
      nlinarith
    nlinarith

/-- Bogoliubov ratios r_pm for the k > 0 / k < 0 branches (a = pi lambda, b = pi rho). -/
def rPlus (a b : ℝ) : ℝ := Real.exp (-2 * b) * Real.cosh (a + b) / Real.cosh (a - b)

def rMinus (a b : ℝ) : ℝ := Real.exp (-2 * b) * Real.cosh (a - b) / Real.cosh (a + b)

/-- The identity N_+ - N_- = sinh(2a)/sinh(2b), in denominator-free form. -/
theorem pair_difference_cleared (a b : ℝ) :
    (rPlus a b * (1 - rMinus a b) - rMinus a b * (1 - rPlus a b)) * Real.sinh (2 * b)
      = Real.sinh (2 * a) * ((1 - rPlus a b) * (1 - rMinus a b)) := by
  have hc1 : Real.cosh (a + b) ≠ 0 := (Real.cosh_pos _).ne'
  have hc2 : Real.cosh (a - b) ≠ 0 := (Real.cosh_pos _).ne'
  unfold rPlus rMinus
  have e1 : Real.exp (-2 * b) = (Real.exp b)⁻¹ ^ 2 := by
    rw [show -2 * b = -(b + b) by ring, Real.exp_neg, Real.exp_add]; ring
  rw [e1]
  simp only [Real.cosh_eq, Real.sinh_eq, Real.exp_neg, Real.exp_sub, Real.exp_add,
    show 2 * b = b + b by ring, show 2 * a = a + a by ring]
  have hX : Real.exp a ≠ 0 := (Real.exp_pos _).ne'
  have hY : Real.exp b ≠ 0 := (Real.exp_pos _).ne'
  have hc1' : (Real.exp a * Real.exp b + (Real.exp a * Real.exp b)⁻¹) / 2 ≠ 0 := by
    have := hc1
    simpa [Real.cosh_eq, Real.exp_add, Real.exp_neg] using this
  have hc2' : (Real.exp a / Real.exp b + (Real.exp a / Real.exp b)⁻¹) / 2 ≠ 0 := by
    have := hc2
    simpa [Real.cosh_eq, Real.exp_sub, Real.exp_neg] using this
  field_simp
  ring

/-- Under nondegeneracy, N_+ - N_- = sinh(2a)/sinh(2b), with N_pm = r_pm/(1 - r_pm). -/
theorem pair_difference (a b : ℝ) (hplus : 1 - rPlus a b ≠ 0) (hminus : 1 - rMinus a b ≠ 0)
    (hs : Real.sinh (2 * b) ≠ 0) :
    rPlus a b / (1 - rPlus a b) - rMinus a b / (1 - rMinus a b) = Real.sinh (2 * a) / Real.sinh (2 * b) := by
  have hc := pair_difference_cleared a b
  field_simp
  linarith [hc]

/-- The published closed form for the dS_2 induced current, J/(eH) (rho real). -/
def Jclosed (l ρ : ℝ) : ℝ := ρ * Real.sinh (2 * π * l) / (π * Real.sinh (2 * π * ρ))

/-- The current is odd in the field. -/
theorem Jclosed_odd (l ρ : ℝ) : Jclosed (-l) ρ = -Jclosed l ρ := by
  unfold Jclosed
  rw [show 2 * π * -l = -(2 * π * l) by ring, Real.sinh_neg]
  ring

/-- At rho = lambda (m^2 = H^2/4) the response is exactly linear: J/(eH) = lambda/pi. -/
theorem Jclosed_at_quarter (l : ℝ) (hl : l ≠ 0) : Jclosed l l = l / π := by
  unfold Jclosed
  have hpi : π ≠ 0 := Real.pi_ne_zero
  have hs : Real.sinh (2 * π * l) ≠ 0 := by
    intro h
    have := Real.sinh_eq_zero.mp h
    have : 2 * π * l = 0 := this
    rcases mul_eq_zero.mp this with h1 | h1
    · exact hpi (by linarith [h1])
    · exact hl h1
  field_simp

/-- A tie sigma H = (e^2/H^2) g(mu) = c fixes e^2/H^2 = c/g(mu); different g give different couplings. -/
theorem tie_coupling_differs {c g₁ g₂ : ℝ} (hc : c ≠ 0) (h₁ : 0 < g₁) (h₂ : 0 < g₂) (hne : g₁ ≠ g₂) :
    c / g₁ ≠ c / g₂ := by
  intro h
  rw [div_eq_div_iff h₁.ne' h₂.ne'] at h
  have : c * (g₂ - g₁) = 0 := by linarith
  rcases mul_eq_zero.mp this with h0 | h0
  · exact hc h0
  · exact hne (by linarith)

#print axioms no_coupling_from_obs
#print axioms no_alpha_from_obs
#print axioms alpha_of_tie
#print axioms eps_star_iff
#print axioms eps_star_bounds
#print axioms pair_difference_cleared
#print axioms pair_difference
#print axioms Jclosed_odd
#print axioms Jclosed_at_quarter
#print axioms tie_coupling_differs
