import Mathlib

/-!
# I27 — the triggered carrier's kick: why galaxy interiors empty, and why the phantom only adds decays

SCOPE (per lean-math-certification): Lean certifies the MATHEMATICS. Physics inputs are hypotheses: a daughter's velocity
is v = v_o + v_k n (orbital velocity plus a kick of speed v_k ≥ 0 along a unit vector n, L365); the local escape speed is
defined by Φ = −v_esc²/2 at the decay point (potential zero at infinity); the trigger variable is
x = (3/2) Ω_m (δ_m + δ_ph) with δ_ph ≥ 0 the phantom's positive density contrast (L342/L357; L377).
Companion lanes: `real_research/dark_sector_2026/L376_triggered_carrier_inner_galaxies.py`,
`real_research/dark_sector_2026/L377_full_construction_pm.py`.

* `kick_speed_lower` — whatever the kick direction, ‖v_o + v_k n‖ ≥ v_k − ‖v_o‖.
* `kick_unbinds` — if v_k > ‖v_o‖ + v_esc then the daughter's energy ‖v‖²/2 + Φ is positive: it is unbound, for EVERY
  kick direction.
* `milky_way_interior_empties` — the L376 numbers: v_k = 650 km/s, orbital speed ≤ 250 km/s, post-decay escape speed
  ≤ 300 km/s inside ~10 kpc ⇒ every daughter decayed there is unbound.
* `phantom_only_adds_decays` — with δ_ph ≥ 0 the phantom-inclusive trigger fires wherever the matter-only one does
  (the matter-only trigger is the least-trigger estimate).
* `self_limiting_trigger` — once the carrier has left, a region whose remaining density satisfies
  ρ ≤ ρ̄ + (10/3) ρ_crit has x = (3/2)(ρ − ρ̄)/ρ_crit ≤ 5: the matter-only trigger switches off there (L375).

Zero `sorry`; axioms ⊆ {propext, Classical.choice, Quot.sound}.
-/

noncomputable section

open scoped RealInnerProductSpace

abbrev V3 := EuclideanSpace ℝ (Fin 3)

theorem kick_speed_lower (vo n : V3) (vk : ℝ) (hk : 0 ≤ vk) (hn : ‖n‖ = 1) :
    vk - ‖vo‖ ≤ ‖vo + vk • n‖ := by
  have h1 : ‖vk • n‖ = vk := by rw [norm_smul, hn, mul_one, Real.norm_of_nonneg hk]
  have h2 : ‖vk • n‖ - ‖vo‖ ≤ ‖vk • n + vo‖ := by
    have := norm_sub_norm_le (vk • n + vo) vo
    have h3 : ‖vk • n‖ ≤ ‖vk • n + vo‖ + ‖vo‖ := by
      calc ‖vk • n‖ = ‖(vk • n + vo) - vo‖ := by rw [add_sub_cancel_right]
        _ ≤ ‖vk • n + vo‖ + ‖vo‖ := norm_sub_le _ _
    linarith
  rw [h1, add_comm] at h2
  exact h2

theorem kick_unbinds (vo n : V3) (vk vesc Φ : ℝ) (hk : 0 ≤ vk) (hn : ‖n‖ = 1) (he : 0 ≤ vesc)
    (hΦ : Φ = -(vesc ^ 2) / 2) (hfast : vk > ‖vo‖ + vesc) :
    0 < ‖vo + vk • n‖ ^ 2 / 2 + Φ := by
  have hl := kick_speed_lower vo n vk hk hn
  have hpos : vesc < ‖vo + vk • n‖ := by linarith
  have hsq : vesc ^ 2 < ‖vo + vk • n‖ ^ 2 := by
    have := norm_nonneg (vo + vk • n)
    nlinarith
  rw [hΦ]
  linarith

theorem milky_way_interior_empties (vo n : V3) (vesc Φ : ℝ) (hn : ‖n‖ = 1) (he : 0 ≤ vesc)
    (ho : ‖vo‖ ≤ 250) (hesc : vesc ≤ 300) (hΦ : Φ = -(vesc ^ 2) / 2) :
    0 < ‖vo + (650 : ℝ) • n‖ ^ 2 / 2 + Φ :=
  kick_unbinds vo n 650 vesc Φ (by norm_num) hn he hΦ (by linarith)

theorem phantom_only_adds_decays {Ωm δm δph xc : ℝ} (hΩ : 0 ≤ Ωm) (hph : 0 ≤ δph)
    (hfire : xc < 3 / 2 * Ωm * δm) : xc < 3 / 2 * Ωm * (δm + δph) := by
  have : 0 ≤ 3 / 2 * Ωm * δph := by positivity
  nlinarith

theorem self_limiting_trigger {ρ ρbar ρcrit : ℝ} (hc : 0 < ρcrit) (hρ : ρ ≤ ρbar + 10 / 3 * ρcrit) :
    3 / 2 * (ρ - ρbar) / ρcrit ≤ 5 := by
  rw [div_le_iff₀ hc]
  linarith

end
