import Mathlib

/-!
# PUZZLE_32pi_postulate_status_2026_10_05 -- is  r* = c / sqrt(G rho_Lambda)  derivable?

The framework's ingredients used in the 2026-10-04/05 chain, as a structure of named premises (c, G, rho, a0, Lambda, r > 0):
* `einstein`   : Lambda = 8 pi G rho / c^2                      (Lambda as vacuum energy)
* `horizon`    : a0 = c^2 / (2 r)                               (a0 is the surface gravity of the Schwarzschild horizon of radius r)
* `bimond`     : Lambda = (1/2)(1 + fp) a0^2 I / c^4            (Milgrom 2009 eq 24 vacuum term, any slope fp > -1, any finite tail integral I > 0)
* `law`        : the quadrature law's form (no constraint linking a0 to rho; recorded as True)
The postulate P is  G rho r^2 = c^2  (equivalently Lambda A = 32 pi^2, a0 = (c/2) sqrt(G rho)).

Proved here:
* `postulate_iff_kappa_half` : under `einstein` and `horizon`, P  <->  a0^2 = G rho c^2 / 4  (the fitted kappa = 1/2).
* `ingredients_consistent_with_P` : a model satisfying every premise AND P exists.
* `ingredients_consistent_with_notP` : a model satisfying every premise and NOT P exists (kappa = 1, I chosen to fit).
* `postulate_independent` : hence P is NOT a consequence of the premises: it is independent of them.
* `scale_family` : for every kappa > 0 the premises admit a model with a0 = kappa c sqrt(G rho) (the coefficient is a free modulus of the premises).
So the postulate cannot be "solved" from these ingredients: it is an extra axiom, or it needs a NEW premise that breaks the kappa-family.
-/

open Real

structure Ingredients (c G ρ a0 Λ r fp I : ℝ) : Prop where
  pos : 0 < c ∧ 0 < G ∧ 0 < ρ ∧ 0 < a0 ∧ 0 < r ∧ 0 < I ∧ -1 < fp
  einstein : Λ = 8 * π * G * ρ / c ^ 2
  horizon : a0 = c ^ 2 / (2 * r)
  bimond : Λ = (1 / 2) * (1 + fp) * a0 ^ 2 * I / c ^ 4

def Postulate (c G ρ r : ℝ) : Prop := G * ρ * r ^ 2 = c ^ 2

theorem postulate_iff_kappa_half {c G ρ a0 Λ r fp I : ℝ} (h : Ingredients c G ρ a0 Λ r fp I) :
    Postulate c G ρ r ↔ a0 ^ 2 = G * ρ * c ^ 2 / 4 := by
  obtain ⟨⟨hc, hG, hρ, ha, hr, hI, hf⟩, _, hh, _⟩ := h
  unfold Postulate
  have hr0 : r ≠ 0 := hr.ne'
  rw [hh]
  constructor
  · intro hp
    have : r ^ 2 = c ^ 2 / (G * ρ) := by field_simp; linarith [hp]
    field_simp
    nlinarith [hp]
  · intro hk
    field_simp at hk
    have hc2 : 0 < c ^ 2 := by positivity
    nlinarith [hk, hc2]

/-- a model with every premise and the postulate: c = G = rho = 1, r = 1, a0 = 1/2, Lambda = 8 pi, fp = 0, I = 64 pi -/
theorem ingredients_consistent_with_P :
    ∃ c G ρ a0 Λ r fp I : ℝ, Ingredients c G ρ a0 Λ r fp I ∧ Postulate c G ρ r := by
  refine ⟨1, 1, 1, 1 / 2, 8 * π, 1, 0, 64 * π, ⟨⟨by norm_num, by norm_num, by norm_num, by norm_num, by norm_num, by positivity, by norm_num⟩, by ring, by norm_num, by ring⟩, by norm_num [Postulate]⟩

/-- a model with every premise and NOT the postulate: r = 1/2 (a0 = 1, kappa = 1), I = 16 pi -/
theorem ingredients_consistent_with_notP :
    ∃ c G ρ a0 Λ r fp I : ℝ, Ingredients c G ρ a0 Λ r fp I ∧ ¬ Postulate c G ρ r := by
  refine ⟨1, 1, 1, 1, 8 * π, 1, 0, 16 * π, ⟨⟨by norm_num, by norm_num, by norm_num, by norm_num, by norm_num, by positivity, by norm_num⟩, by ring, by norm_num, by ring⟩, ?_⟩
  unfold Postulate; norm_num

theorem postulate_independent :
    ¬ (∀ c G ρ a0 Λ r fp I : ℝ, Ingredients c G ρ a0 Λ r fp I → Postulate c G ρ r) ∧
    ¬ (∀ c G ρ a0 Λ r fp I : ℝ, Ingredients c G ρ a0 Λ r fp I → ¬ Postulate c G ρ r) := by
  constructor
  · intro hall
    obtain ⟨c, G, ρ, a0, Λ, r, fp, I, hi, hn⟩ := ingredients_consistent_with_notP
    exact hn (hall c G ρ a0 Λ r fp I hi)
  · intro hall
    obtain ⟨c, G, ρ, a0, Λ, r, fp, I, hi, hp⟩ := ingredients_consistent_with_P
    exact hall c G ρ a0 Λ r fp I hi hp

/-- every coefficient kappa > 0 is realised (c = G = rho = 1, so a0 = kappa c sqrt(G rho) = kappa): r = 1/(2 kappa), Lambda = 8 pi, fp = 0, I = 16 pi / kappa^2 -/
theorem scale_family (κ : ℝ) (hκ : 0 < κ) : ∃ Λ r fp I : ℝ, Ingredients 1 1 1 κ Λ r fp I := by
  refine ⟨8 * π, 1 / (2 * κ), 0, 16 * π / κ ^ 2, ⟨⟨by norm_num, by norm_num, by norm_num, hκ, by positivity, by positivity, by norm_num⟩, by ring, ?_, ?_⟩⟩
  · field_simp
  · field_simp; ring

#print axioms postulate_iff_kappa_half
#print axioms postulate_independent
#print axioms scale_family
