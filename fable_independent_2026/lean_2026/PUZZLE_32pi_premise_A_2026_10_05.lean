import Mathlib

/-!
# PUZZLE_32pi_premise_A_2026_10_05 -- the conditional theorem: PREMISE A => Lambda = 32 pi a0^2  (c = 1)

PREMISE A (a HYPOTHESIS, new physics, not derived): the a0 horizon -- the sphere of radius r with surface gravity a0, r = 1/(2 a0) -- satisfies GR's horizon
balance (vacuum source integrated over the horizon = Gauss-Bonnet total = 4 pi), but in the MOND sector the vacuum couples with G, not 8 pi G:
      G rho * (4 pi r^2) = 4 pi          [GR's version: (8 pi G rho)(4 pi r^2) <= 4 pi, the Nariai bound]
Standard ingredients: Lambda = 8 pi G rho;  r = 1/(2 a0).
* `premise_A_implies_32pi`      : PREMISE A + ingredients  =>  Lambda = 32 pi a0^2  (equivalently kappa = 1/2, Lambda A_S = 32 pi^2, G rho = (1/r)^2).
* `premise_A_is_not_the_target` : the premise is stated with a coupling constant; with coupling k G instead of G it gives Lambda = (32 pi / k) a0^2,
                                   so it would give a DIFFERENT number if the sector coupling differed (screen question 1).
* `gr_coupling_gives_nariai_side` : with GR's 8 pi G the same balance gives Lambda = 4 a0^2 (= the Nariai-type value 4 pi / A_S), not 32 pi a0^2.
PREMISE A is assumed, not proved. Its support must come from data (a0 ~ sqrt(rho_DE) over cosmic time; PAPER42) and from a theory with a separately coupled MOND sector.
-/

open Real

theorem premise_A_implies_32pi {G ρ Λ a0 r : ℝ} (ha : 0 < a0) (hr : r = 1 / (2 * a0)) (hΛ : Λ = 8 * π * G * ρ)
    (hA : G * ρ * (4 * π * r ^ 2) = 4 * π) : Λ = 32 * π * a0 ^ 2 := by
  have hp : (4 * π) ≠ 0 := by positivity
  have h1 : G * ρ * r ^ 2 = 1 := by
    have : 4 * π * (G * ρ * r ^ 2) = 4 * π * 1 := by linarith [hA]
    exact mul_left_cancel₀ hp this
  have ha0 : a0 ≠ 0 := ha.ne'
  have h2 : G * ρ = 4 * a0 ^ 2 := by
    rw [hr] at h1; field_simp at h1; nlinarith [h1]
  rw [hΛ, show 8 * π * G * ρ = 8 * π * (G * ρ) by ring, h2]; ring

theorem premise_A_is_not_the_target {G ρ Λ a0 r k : ℝ} (ha : 0 < a0) (hk : 0 < k) (hr : r = 1 / (2 * a0)) (hΛ : Λ = 8 * π * G * ρ)
    (hA : k * G * ρ * (4 * π * r ^ 2) = 4 * π) : Λ = (32 * π / k) * a0 ^ 2 := by
  have hp : (4 * π) ≠ 0 := by positivity
  have h1 : k * G * ρ * r ^ 2 = 1 := by
    have : 4 * π * (k * G * ρ * r ^ 2) = 4 * π * 1 := by linarith [hA]
    exact mul_left_cancel₀ hp this
  have ha0 : a0 ≠ 0 := ha.ne'
  have hk0 : k ≠ 0 := hk.ne'
  have h2 : k * (G * ρ) = 4 * a0 ^ 2 := by
    rw [hr] at h1; field_simp at h1; nlinarith [h1]
  have h3 : G * ρ = 4 * a0 ^ 2 / k := by field_simp; linarith [h2]
  rw [hΛ, show 8 * π * G * ρ = 8 * π * (G * ρ) by ring, h3]; field_simp; ring

theorem gr_coupling_gives_nariai_side {G ρ Λ a0 r : ℝ} (ha : 0 < a0) (hr : r = 1 / (2 * a0)) (hΛ : Λ = 8 * π * G * ρ)
    (hGR : (8 * π * G * ρ) * (4 * π * r ^ 2) = 4 * π) : Λ = 4 * a0 ^ 2 := by
  have hp : (4 * π) ≠ 0 := by positivity
  have h1 : (8 * π * G * ρ) * r ^ 2 = 1 := by
    have : 4 * π * ((8 * π * G * ρ) * r ^ 2) = 4 * π * 1 := by linarith [hGR]
    exact mul_left_cancel₀ hp this
  rw [hΛ]; rw [hr] at h1; have ha0 : a0 ≠ 0 := ha.ne'; field_simp at h1; nlinarith [h1]

#print axioms premise_A_implies_32pi
#print axioms premise_A_is_not_the_target
#print axioms gr_coupling_gives_nariai_side
