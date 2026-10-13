import Mathlib

/-!
# CFG723: Lean certificates for the owner chat's derived cold-energy results (CFG660, CFG661, CFG663, CFG665)

Criteria: campaign_fresh_gravity/CFG723_lean_cold_energy_certificates/FROZEN_CRITERIA.md (4002e3dd7), committed before this file.

Setting (pointwise, spherical, one radius r): K = 4πG, the law g = F(g_N) with F′ ≠ 0, the chain rule g′ = F′·g_N′ (a PREMISE),
ρ_b = (g_N′ + 2g_N/r)/K and ρ_c = (g′ + 2g/r)/K − ρ_b (Poisson; only real mass gravitates).

CERTIFIED (premises ⇒ conclusions; algebra and one derivative):
* `aniso_equilibrium` (CFG660 S1): with dP∥/dr = (g/K)(1/F′ − 1)·g′ and P⊥ − P∥ = g(g − g_N)/K, the radial equilibrium residual
  dP∥/dr + 2(P∥ − P⊥)/r + ρ_c g vanishes. (Pointwise this needs only the chain rule; that P⊥ − P∥ is a function of g alone holds on the
  law's shell, g_N = F⁻¹(g), which is the physical content and is NOT certified here.)
* `iso_residual`, `iso_fails` (CFG660 S2): an isotropic pressure with dP/dr = (g/K)(1/s − 1)·g′, s = F′g_N/g, leaves the residual
  ρ_b·g·(g/g_N − 1), nonzero wherever ρ_b ≠ 0 and g ≠ g_N.
* `deep_Ppar_deriv`, `deep_anisotropy` (CFG660 S3): in the deep law g_N = g²/a₀, P∥ = 2g³/(3Ka₀) − g²/(2K) has derivative
  (g/K)(2g/a₀ − 1), and P⊥ − P∥ = g²/K − g³/(Ka₀) (leading terms −g²/8πG and +g²/4πG with K = 4πG: minus the Maxwell stress).
* `rhoc_coefficient_nogo`, `rhoc_nogo` (CFG661 T1): if the equilibrium residual is affine in g_N″ with slope P_ρc(F′ − 1)/K and vanishes
  for two different g_N″, then P_ρc(F′ − 1) = 0, so P_ρc = 0 when F′ ≠ 1.
* `psi_terms_cancel` (CFG661 T2): on shell u = h/r the free-function terms −ψ′/r² + 2((u/2)ψ′/h)/r cancel exactly.
* `no_dimensionless_group`, `unique_group_with_c` (CFG661 T3): (1/length)·G^a·a₀^b is never dimensionless; with c the unique exponent
  triple is (0, −1, 2), i.e. w·c²/a₀.
* `lensing_difference` (CFG663): if g_dyn = F + g_c and g_lens = g_b + g_c then g_dyn − g_lens = F − g_b (cold matter cancels).
* `edge_identity` (CFG665): σ⁴ = G M_tot g_e/4 with M_tot = M_b/f_b and g_e = f_b a₀ gives σ⁴ = G M_b a₀/4 (an identity; CFG665 found
  that the model built on it has no regular solution).

NOT certified: the general-F sympy identities beyond this pointwise algebra, the WKB ill-posedness (CFG660 S5), the SPARC / KiDS / merger
verdicts, the numerical failure of S* (CFG665), or the physical truth of any premise. κ = ½ is FITTED; nothing here says the theory is
closed.
-/

namespace CFG723

/-- CFG660 S1: the field-aligned anisotropic stress balances the law's cold mass at every radius. -/
theorem aniso_equilibrium {K r g gN gNp Fp : ℝ} (hK : K ≠ 0) (hr : r ≠ 0) (hFp : Fp ≠ 0) :
    let gp := Fp * gNp
    let ρb := (gNp + 2 * gN / r) / K
    let ρc := (gp + 2 * g / r) / K - ρb
    let dPpar := (g / K) * (1 / Fp - 1) * gp
    let dPerpMinusPar := g * (g - gN) / K
    dPpar - 2 * dPerpMinusPar / r + ρc * g = 0 := by
  intro gp ρb ρc dPpar dPerpMinusPar
  simp only [gp, ρb, ρc, dPpar, dPerpMinusPar]
  field_simp
  ring

/-- CFG660 S2: an isotropic field-dependent pressure leaves the residual ρ_b·g·(g/g_N − 1). -/
theorem iso_residual {K r g gN gNp Fp : ℝ} (hK : K ≠ 0) (hr : r ≠ 0) (hFp : Fp ≠ 0) (hg : g ≠ 0) (hgN : gN ≠ 0) :
    let gp := Fp * gNp
    let ρb := (gNp + 2 * gN / r) / K
    let ρc := (gp + 2 * g / r) / K - ρb
    let s := Fp * gN / g
    let dP := (g / K) * (1 / s - 1) * gp
    dP + ρc * g = ρb * g * (g / gN - 1) := by
  intro gp ρb ρc s dP
  simp only [gp, ρb, ρc, s, dP]
  field_simp
  ring

/-- CFG660 S2: the isotropic residual is nonzero wherever there are baryons and the field is not Newtonian. -/
theorem iso_fails {K r g gN gNp Fp : ℝ} (hK : K ≠ 0) (hr : r ≠ 0) (hFp : Fp ≠ 0) (hg : g ≠ 0) (hgN : gN ≠ 0)
    (hρ : (gNp + 2 * gN / r) / K ≠ 0) (hneq : g ≠ gN) :
    (g / K) * (1 / (Fp * gN / g) - 1) * (Fp * gNp) + ((Fp * gNp + 2 * g / r) / K - (gNp + 2 * gN / r) / K) * g ≠ 0 := by
  have h := iso_residual (K := K) (r := r) (g := g) (gN := gN) (gNp := gNp) (Fp := Fp) hK hr hFp hg hgN
  simp only at h
  rw [h]
  have h1 : g / gN - 1 ≠ 0 := by
    intro h0
    apply hneq
    have : g / gN = 1 := by linarith
    field_simp at this
    linarith
  exact mul_ne_zero (mul_ne_zero hρ hg) h1

/-- CFG660 S3: the deep-law P∥ and its derivative. -/
theorem deep_Ppar_deriv {K a0 : ℝ} (hK : K ≠ 0) (ha : a0 ≠ 0) (x : ℝ) :
    HasDerivAt (fun x => 2 * x ^ 3 / (3 * K * a0) - x ^ 2 / (2 * K)) ((x / K) * (2 * x / a0 - 1)) x := by
  have h3 := (hasDerivAt_pow 3 x).const_mul (2 / (3 * K * a0))
  have h2 := (hasDerivAt_pow 2 x).const_mul (1 / (2 * K))
  have h := (h3.sub h2).congr_deriv (by push_cast; field_simp : _ = (x / K) * (2 * x / a0 - 1))
  refine h.congr_of_eventuallyEq (Filter.Eventually.of_forall fun y => ?_)
  simp only [Pi.sub_apply]
  field_simp

/-- CFG660 S3: the deep-law anisotropy P⊥ − P∥. -/
theorem deep_anisotropy {K a0 g : ℝ} (hK : K ≠ 0) (ha : a0 ≠ 0) :
    g * (g - g ^ 2 / a0) / K = g ^ 2 / K - g ^ 3 / (K * a0) := by
  field_simp

/-- CFG661 T1: a residual affine in g_N″ with slope P_ρc(F′ − 1)/K that vanishes for two different g_N″ forces P_ρc(F′ − 1) = 0. -/
theorem rhoc_coefficient_nogo {K Pρ Fp X Rest x1 x2 : ℝ} (hK : K ≠ 0)
    (h1 : Pρ * ((Fp - 1) * x1 + X) / K + Rest = 0) (h2 : Pρ * ((Fp - 1) * x2 + X) / K + Rest = 0) (hx : x1 ≠ x2) :
    Pρ * (Fp - 1) = 0 := by
  have hd : Pρ * (Fp - 1) * (x1 - x2) / K = 0 := by
    have : Pρ * ((Fp - 1) * x1 + X) / K - Pρ * ((Fp - 1) * x2 + X) / K = 0 := by linarith
    rw [← this]; ring
  have hsub : x1 - x2 ≠ 0 := sub_ne_zero.mpr hx
  have : Pρ * (Fp - 1) * (x1 - x2) = 0 := by
    field_simp at hd; linarith
  exact (mul_eq_zero.mp this).resolve_right hsub

/-- CFG661 T1 corollary: with F′ ≠ 1 the stress cannot respond to the cold density. -/
theorem rhoc_nogo {K Pρ Fp X Rest x1 x2 : ℝ} (hK : K ≠ 0)
    (h1 : Pρ * ((Fp - 1) * x1 + X) / K + Rest = 0) (h2 : Pρ * ((Fp - 1) * x2 + X) / K + Rest = 0) (hx : x1 ≠ x2)
    (hF : Fp ≠ 1) : Pρ = 0 := by
  have h := rhoc_coefficient_nogo hK h1 h2 hx
  exact (mul_eq_zero.mp h).resolve_right (sub_ne_zero.mpr hF)

/-- CFG661 T2: the free-function terms cancel on the law's shell u = h/r. -/
theorem psi_terms_cancel {u h r ψ : ℝ} (hh : h ≠ 0) (hr : r ≠ 0) (hu : u = h / r) :
    -ψ / r ^ 2 + 2 * ((u / 2) * ψ / h) / r = 0 := by
  subst hu
  field_simp
  ring

/-- CFG661 T3: exponents (kg, s, m) of (1/length)·G^a·a₀^b; no choice makes it dimensionless. -/
theorem no_dimensionless_group : ¬ ∃ a b : ℚ, -a = 0 ∧ -2 * a - 2 * b = 0 ∧ -1 + 3 * a + b = 0 := by
  rintro ⟨a, b, h1, h2, h3⟩
  linarith

/-- CFG661 T3: with c the unique dimensionless group is w·c²/a₀. -/
theorem unique_group_with_c (a b c : ℚ) :
    (-a = 0 ∧ -2 * a - 2 * b - c = 0 ∧ -1 + 3 * a + b + c = 0) ↔ (a = 0 ∧ b = -1 ∧ c = 2) := by
  constructor
  · rintro ⟨h1, h2, h3⟩
    refine ⟨by linarith, by linarith, by linarith⟩
  · rintro ⟨rfl, rfl, rfl⟩
    norm_num

/-- CFG663: collisionless cold matter enters dynamics and lensing alike, so it cancels in their difference. -/
theorem lensing_difference {gdyn glens F gb gc : ℝ} (hd : gdyn = F + gc) (hl : glens = gb + gc) :
    gdyn - glens = F - gb := by
  subst hd hl; ring

/-- CFG665: the edge identity (an identity, which is why its numerical agreement was a coincidence). -/
theorem edge_identity {σ4 G Mtot ge Mb fb a0 : ℝ} (hfb : fb ≠ 0) (hσ : σ4 = G * Mtot * ge / 4)
    (hM : Mtot = Mb / fb) (hg : ge = fb * a0) : σ4 = G * Mb * a0 / 4 := by
  subst hσ hM hg
  field_simp

end CFG723

open CFG723 in
#print axioms aniso_equilibrium
open CFG723 in
#print axioms iso_residual
open CFG723 in
#print axioms iso_fails
open CFG723 in
#print axioms deep_Ppar_deriv
open CFG723 in
#print axioms deep_anisotropy
open CFG723 in
#print axioms rhoc_coefficient_nogo
open CFG723 in
#print axioms rhoc_nogo
open CFG723 in
#print axioms psi_terms_cancel
open CFG723 in
#print axioms no_dimensionless_group
open CFG723 in
#print axioms unique_group_with_c
open CFG723 in
#print axioms lensing_difference
open CFG723 in
#print axioms edge_identity
