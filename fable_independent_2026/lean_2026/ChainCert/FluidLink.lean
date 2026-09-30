import Mathlib
import ChainCert.Chain
import ChainCert.Fluid
import ChainCert.Theory

/-!
# ChainCert.FluidLink -- the fluid cap's a₀ and the chain's a₀ are the same a₀, under Λ = 8πGρ_Λ/c²

`ChainCert.Fluid` proves, in the fluid's units (c = 1, M_P² = 1/(8πG)), that the saturating cap P_cap = (κ²/8π) M_P² Λ defines
an acceleration a₀ = √(8πG P_cap) with a₀² = κ²Λ/8π (`cap_a0_tie`, `cap_a0_eq`).  `ChainPremises.a0 z = κ c √(G ρ_Λ(z))` is the
chain's tie.  The README listed these as NOT linked.  This module links them.

PREMISE (named hypothesis in every theorem): Λ = 8πG ρ_Λ/c² (Einstein's relation between the cosmological constant and the
vacuum density; in the fluid's units c = 1 it reads Λ = 8πG ρ_Λ).

Certified here (premises ⇒ conclusions):
* `link_general`: with Λ = 8πGρ_Λ(z)/c², κ c² √(Λ/8π) = `ChainPremises.a0 z` in any units (the kernel's α(Λ) c² is the chain's a₀);
* `link_general_iff`: conversely, for Λ ≥ 0 the two agree ONLY IF Λ = 8πGρ_Λ(z)/c², so the relation is exactly the missing link;
* `link_units`: in the fluid's units (c = 1, Λ = 8πGρ_Λ(z)), the cap's acceleration √(8πG P_cap) IS `ChainPremises.a0 z`
  (reuses `cap_a0_eq`); `link_sq`: (a₀(z))² = κ²Λ/8π (reuses `cap_a0_tie`);
* `link_flat`: under the chain's constancy premise `hflat`, the Λ read by the cap is the same at every z, and so is the cap's
  acceleration;
* `CandidateB.fluid_cap_a0`: for candidate B (c = 1), the cap's acceleration at κ = ½ is B's a₀(0) = ½ √(G ρ_Λ(0)).

NOT certified: that the cap takes this form (a POSTULATE of the CFG43 action), the fluid's field equations (numerical, CFG43),
and that the fluid and the kernel are ONE fluid.  Identifying the a₀ symbol does not remove the README's obstruction: the P2
point-mass pressure of `PointMass` exceeds this cap for r < r_M.  κ = ½ stays FITTED; Λ = 8πGρ_Λ/c² is a premise here.
-/

namespace FluidLink

/-- the fluid cap's acceleration (fluid units, c = 1): √(8πG P_cap), P_cap = (κ²/8π) M_P² Λ, M_P² = 1/(8πG) -/
noncomputable def capA0 (G κ Λ : ℝ) : ℝ :=
  Real.sqrt (8 * Real.pi * G * ((κ ^ 2 / (8 * Real.pi)) * (1 / (8 * Real.pi * G)) * Λ))

/-- ANY UNITS: with Λ = 8πGρ_Λ(z)/c², κ c² √(Λ/8π) is the chain's a₀(z) = κ c √(G ρ_Λ(z)) -/
theorem link_general (P : ChainPremises) (z : ℝ) {Λ : ℝ} (hΛ : Λ = 8 * Real.pi * P.G * P.ρΛ z / P.c ^ 2) :
    P.κ * P.c ^ 2 * Real.sqrt (Λ / (8 * Real.pi)) = P.a0 z := by
  have hc := P.hc
  have hG := P.hG
  have hρ := P.hρ z
  have e : Λ / (8 * Real.pi) = P.G * P.ρΛ z / P.c ^ 2 := by
    rw [hΛ]; field_simp
  rw [e, Real.sqrt_div' _ (by positivity), Real.sqrt_sq hc.le, ChainPremises.a0]
  field_simp

/-- the converse: for Λ ≥ 0 the fluid-side κ c² √(Λ/8π) equals the chain's a₀(z) ONLY IF Λ = 8πGρ_Λ(z)/c² -/
theorem link_general_iff (P : ChainPremises) (z : ℝ) {Λ : ℝ} (hΛ0 : 0 ≤ Λ) :
    P.κ * P.c ^ 2 * Real.sqrt (Λ / (8 * Real.pi)) = P.a0 z ↔ Λ = 8 * Real.pi * P.G * P.ρΛ z / P.c ^ 2 := by
  constructor
  · intro h
    have hc := P.hc
    have hκ := P.hκ
    have hG := P.hG
    have hρ := P.hρ z
    have hs : Real.sqrt (Λ / (8 * Real.pi)) = Real.sqrt (P.G * P.ρΛ z) / P.c := by
      rw [ChainPremises.a0] at h
      field_simp at h ⊢
      nlinarith [h]
    have hsq := congrArg (· ^ 2) hs
    rw [Real.sq_sqrt (by positivity), div_pow, Real.sq_sqrt (by positivity)] at hsq
    field_simp at hsq ⊢
    linarith
  · exact link_general P z

/-- FLUID UNITS (c = 1, Λ = 8πGρ_Λ(z)): the cap's acceleration √(8πG P_cap) IS the chain's a₀(z) -/
theorem link_units (P : ChainPremises) (hc1 : P.c = 1) (z : ℝ) {Λ : ℝ} (hΛ : Λ = 8 * Real.pi * P.G * P.ρΛ z) :
    capA0 P.G P.κ Λ = P.a0 z := by
  have hG := P.hG
  have hρ := P.hρ z
  have hΛ0 : 0 ≤ Λ := by rw [hΛ]; positivity
  have hΛ' : Λ = 8 * Real.pi * P.G * P.ρΛ z / P.c ^ 2 := by rw [hc1, hΛ]; ring
  unfold capA0
  rw [cap_a0_eq P.hG P.hκ hΛ0, ← link_general P z hΛ', hc1]
  ring

/-- FLUID UNITS: (a₀(z))² = κ²Λ/8π, the fluid module's `cap_a0_tie` read for the chain's a₀ -/
theorem link_sq (P : ChainPremises) (hc1 : P.c = 1) (z : ℝ) {Λ : ℝ} (hΛ : Λ = 8 * Real.pi * P.G * P.ρΛ z) :
    P.a0 z ^ 2 = P.κ ^ 2 * Λ / (8 * Real.pi) := by
  have hG := P.hG
  have hρ := P.hρ z
  have hΛ0 : 0 ≤ Λ := by rw [hΛ]; positivity
  rw [← link_units P hc1 z hΛ, capA0, Real.sq_sqrt, cap_a0_tie P.hG]
  rw [cap_a0_tie P.hG]
  have := Real.pi_pos
  positivity

/-- under the chain's constancy premise, the Λ the cap reads is the same at every z, and so is its acceleration -/
theorem link_flat (P : ChainPremises) (z : ℝ) :
    8 * Real.pi * P.G * P.ρΛ z / P.c ^ 2 = 8 * Real.pi * P.G * P.ρΛ 0 / P.c ^ 2 ∧
      capA0 P.G P.κ (8 * Real.pi * P.G * P.ρΛ z) = capA0 P.G P.κ (8 * Real.pi * P.G * P.ρΛ 0) := by
  rw [P.hflat z]
  exact ⟨rfl, rfl⟩

end FluidLink

/-- candidate B in the fluid's units (c = 1): with Λ = 8πGρ_Λ(0), the cap's acceleration at the FITTED κ = ½ is B's a₀(0) =
    ½ √(G ρ_Λ(0)), the same a₀ as in B's predictions -/
theorem CandidateB.fluid_cap_a0 {ι : Type*} (B : CandidateB ι) (hc1 : B.chain.c = 1) {Λ : ℝ}
    (hΛ : Λ = 8 * Real.pi * B.chain.G * B.chain.ρΛ 0) :
    FluidLink.capA0 B.chain.G (1 / 2) Λ = B.chain.a0 0 ∧
      B.chain.a0 0 = 1 / 2 * Real.sqrt (B.chain.G * B.chain.ρΛ 0) := by
  have h := FluidLink.link_units B.chain hc1 0 hΛ
  rw [B.hκ_fit] at h
  refine ⟨h, ?_⟩
  rw [B.a0_eq 0, hc1, mul_one]
