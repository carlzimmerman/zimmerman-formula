import Mathlib
import ChainCert.Certificates
import ChainCert.Kernel
import ChainCert.Chain
import ChainCert.Gauss
import ChainCert.Ownership
import ChainCert.Theory

/-!
# ChainCert.Action -- from an AQUAL action to the kernel, in spherical symmetry

Until now the chain started from a DECLARED kernel: `CandidateB.hν_deep` postulates a ν with ν(y)√y → 1.  This module starts
one step earlier, from an AQUAL-type action, and derives the kernel from it in spherical symmetry.

PREMISE (declared, not derived): the AQUAL (Bekenstein-Milgrom) Lagrangian density
    ℒ = -(a₀²/8πG) F(|∇Φ|²/a₀²) - ρ Φ,        μ(x) := F'(x²),
stated through μ directly (`AqualMu`): x ↦ x μ(x) is positive, strictly increasing and continuous on (0, ∞), and onto (0, ∞).
The deep-MOND limit μ(x)/x → 1 as x → 0⁺ is a separate declared premise.

Certified here (premises ⇒ conclusions):
* `aqual_momentum` (F → μ): the radial Lagrangian density (a₀²/8πG) F(g²/a₀²) has g-derivative μ(g/a₀) g/(4πG), the flux
  that the field equation differentiates;
* `gauss_form` (the spherical Gauss step): from the reduced Euler-Lagrange equation d/dr[r² μ(g/a₀) g] = 4πG r² ρ (a PREMISE;
  the Euler-Lagrange derivation itself is not formalised), the Newtonian Gauss lemma (`gauss_flux_deriv`, reused from
  `ChainCert.Gauss`) and regularity at the centre, μ(g/a₀) g = g_N = G M(<r)/r² at every r > 0;
* `AqualMu.kernel_of_gauss`, `AqualMu.gauss_of_kernel`, `AqualMu.gauss_iff_kernel`: a positive g solves μ(g/a₀) g = g_N iff
  g = ν(g_N/a₀) g_N, where ν(y) := x(y)/y and x(y) is the unique x > 0 with x μ(x) = y (`AqualMu.nu`);
  `AqualMu.spherical_kernel` composes the Gauss step with the inversion;
* `AqualMu.mu_mul_nu`: μ(x) ν(x μ(x)) = 1 (the two functions are reciprocal at corresponding points);
* `AqualMu.nu_deep`: the deep limit μ(x)/x → 1 implies C2's kernel premise ν(y)√y → 1, IN GENERAL (every `AqualMu`);
* `onto_of_regimes`, `AqualMu.ofRegimes`: ontoness need not be assumed: continuity plus the deep limit μ(x)/x → 1 (x → 0⁺) and
  the Newtonian limit μ(x) → 1 (x → ∞) give it by the intermediate value theorem;
* P2: `muP2` (μ(x) = (√(1+4x²) − 1)/(2x)) satisfies the premises (`muP2Aqual`), the deep limit (`muP2_deep`) and the
  Newtonian limit (`muP2_newton`; so `muP2_onto_from_regimes`); both directions x μ(x) = y ⇔ x = √(1 + 1/y) y are checked
  algebraically (`muP2_to_nuP2`, `nuP2_to_muP2`, `muP2_iff`, and in physical variables `P2_gauss_iff_kernel`); the inverted
  kernel is P2 = √(1 + 1/y) = ν_β at β = 1 (`nuP2_of_action`, `nuP2_of_action_nuBeta`), and its deep limit comes out of the
  general theorem (`P2_deep_from_action`);
* `CandidateB_Action`: candidate B with the P2 field replaced by the action premise.  `CandidateB_Action.toCandidateB` builds
  a `CandidateB` from it (the kernel premise is DERIVED via `nu_deep`, not assumed), so `CandidateB.predictions` applies
  unchanged (`CandidateB_Action.predictions`, a one-line reuse).  A top-level system's internal acceleration is the unique
  positive solution of the action's spherical Gauss form (`top_solves_gauss`, `top_unique_gauss`, `top_from_field_equation`);
  `nonempty_fin2` shows the premises are jointly satisfiable (P2 witness).

The inversion itself uses only positivity, strict monotonicity and ontoness of x μ(x); continuity is used only to derive
ontoness from the two regimes (`onto_of_regimes`).

NOT certified: that the AQUAL action is the physical one (a PREMISE: the action premise replaces the kernel premise, but it is
itself a declared choice, and the choice of μ is as free as the choice of ν was); the Euler-Lagrange derivation (the reduced
radial equation is a premise); the non-spherical field equation (only its spherical Gauss reduction is used; off symmetry AQUAL's
field is not ν(g_N/a₀) g_N, and nothing here touches that); the relativistic completion; κ = ½ (FITTED); ownership's physical
realisation (Gap 1); every empirical fit.  Nothing here says the theory is closed or derived.
-/

open Filter Topology

namespace AqualAction

/-! ## From F to μ, and the spherical Gauss step -/

/-- (F → μ) the AQUAL radial Lagrangian density, as a function of g = Φ', is (a₀²/8πG) F(g²/a₀²) (up to sign and the ρΦ term,
    which does not depend on g).  If F has derivative F'(s) at s = g²/a₀² and μ(x) = F'(x²), its g-derivative is
    μ(g/a₀) g/(4πG): the flux whose divergence the field equation sets equal to ρ. -/
theorem aqual_momentum {F F' μ : ℝ → ℝ} {G a0 g : ℝ} (hG : G ≠ 0) (ha : a0 ≠ 0)
    (hF : HasDerivAt F (F' (g ^ 2 / a0 ^ 2)) (g ^ 2 / a0 ^ 2)) (hμ : ∀ x, μ x = F' (x ^ 2)) :
    HasDerivAt (fun p => a0 ^ 2 / (8 * Real.pi * G) * F (p ^ 2 / a0 ^ 2))
      (μ (g / a0) * g / (4 * Real.pi * G)) g := by
  have h1 : HasDerivAt (fun p : ℝ => p ^ 2 / a0 ^ 2) (2 * g / a0 ^ 2) g := by
    have := (hasDerivAt_pow 2 g).div_const (a0 ^ 2)
    simpa using this
  have h2 : HasDerivAt (fun p => a0 ^ 2 / (8 * Real.pi * G) * F (p ^ 2 / a0 ^ 2))
      (a0 ^ 2 / (8 * Real.pi * G) * (F' (g ^ 2 / a0 ^ 2) * (2 * g / a0 ^ 2))) g :=
    (hF.comp g h1).const_mul (a0 ^ 2 / (8 * Real.pi * G))
  refine h2.congr_deriv ?_
  rw [hμ, div_pow]
  field_simp
  ring

/-- THE SPHERICAL GAUSS STEP.  PREMISES:
    (EL) the reduced Euler-Lagrange equation of the radial AQUAL action: d/dr [r² μ(g/a₀) g] = 4πG r² ρ at every r > 0;
    (N)  the Newtonian field g_N = G M/r² with M' = 4π r² ρ at every r > 0 (its flux derivative is `gauss_flux_deriv`,
         reused from `ChainCert.Gauss`);
    (R)  regularity at the centre: r² (μ(g/a₀) g − g_N) → 0 as r → 0⁺.
    CONCLUSION: μ(g(r)/a₀) g(r) = g_N(r) at every r > 0 (the flux difference has zero derivative on (0, ∞), so it is constant
    there, and the constant is its limit 0 at the centre). -/
theorem gauss_form {μ g gN M ρ : ℝ → ℝ} {G a0 : ℝ}
    (hEL : ∀ r, 0 < r →
      HasDerivAt (fun s => s ^ 2 * (μ (g s / a0) * g s)) (G * (4 * Real.pi * r ^ 2 * ρ r)) r)
    (hN : ∀ r, r ≠ 0 → gN r = G * M r / r ^ 2)
    (hM : ∀ r, 0 < r → HasDerivAt M (4 * Real.pi * r ^ 2 * ρ r) r)
    (hreg : Tendsto (fun r => r ^ 2 * (μ (g r / a0) * g r - gN r)) (𝓝[>] 0) (𝓝 0)) :
    ∀ r, 0 < r → μ (g r / a0) * g r = gN r := by
  have hfun : (fun r => r ^ 2 * (μ (g r / a0) * g r - gN r)) =
      fun s => s ^ 2 * (μ (g s / a0) * g s) - s ^ 2 * gN s := by
    funext s; ring
  have hd : ∀ r, 0 < r → HasDerivAt (fun r => r ^ 2 * (μ (g r / a0) * g r - gN r)) 0 r := by
    intro r hr
    have hNd := gauss_flux_deriv (ρ := ρ r) hr.ne' hN (hM r hr)
    have h3 : HasDerivAt (fun s => s ^ 2 * (μ (g s / a0) * g s) - s ^ 2 * gN s)
        (G * (4 * Real.pi * r ^ 2 * ρ r) - G * (4 * Real.pi * r ^ 2 * ρ r)) r := (hEL r hr).sub hNd
    rw [sub_self] at h3
    rw [hfun]
    exact h3
  obtain ⟨C, hC⟩ := isOpen_Ioi.exists_is_const_of_deriv_eq_zero
    (f := fun r => r ^ 2 * (μ (g r / a0) * g r - gN r)) isPreconnected_Ioi
    (fun r hr => (hd r hr).differentiableAt.differentiableWithinAt)
    (fun r hr => by simpa using (hd r hr).deriv)
  have hlim : Tendsto (fun r => r ^ 2 * (μ (g r / a0) * g r - gN r)) (𝓝[>] 0) (𝓝 C) := by
    refine tendsto_const_nhds.congr' ?_
    filter_upwards [self_mem_nhdsWithin] with r hr
    exact (hC r hr).symm
  have hC0 : C = 0 := tendsto_nhds_unique hlim hreg
  intro r hr
  have h0 := hC r hr
  rw [hC0] at h0
  have hr2 : r ^ 2 ≠ 0 := by positivity
  have := (mul_eq_zero.mp h0).resolve_left hr2
  linarith

/-! ## The action premise and the inversion y = x μ(x) -/

/-- THE ACTION PREMISE, stated through μ (μ(x) = F'(x²) for the AQUAL Lagrangian; DECLARED, not derived). -/
structure AqualMu where
  /-- the interpolating function of the AQUAL Lagrangian, μ(x) = F'(x²) -/
  μ : ℝ → ℝ
  /-- x μ(x) > 0 on (0, ∞) -/
  hpos : ∀ x, 0 < x → 0 < x * μ x
  /-- x μ(x) is strictly increasing on (0, ∞) -/
  hmono : StrictMonoOn (fun x => x * μ x) (Set.Ioi 0)
  /-- x μ(x) is continuous on (0, ∞) (declared; the inversion below does not use it) -/
  hcont : ContinuousOn (fun x => x * μ x) (Set.Ioi 0)
  /-- x μ(x) is onto (0, ∞) -/
  honto : ∀ y, 0 < y → ∃ x, 0 < x ∧ x * μ x = y

namespace AqualMu

variable (A : AqualMu)

theorem mu_pos {x : ℝ} (hx : 0 < x) : 0 < A.μ x := by
  have h := A.hpos x hx
  by_contra hc
  have hc' : A.μ x ≤ 0 := not_lt.mp hc
  have : x * A.μ x ≤ 0 := mul_nonpos_of_nonneg_of_nonpos hx.le hc'
  linarith

/-- the inverse of x ↦ x μ(x) on (0, ∞) (set to 0 off the ray; only its values at y > 0 are used) -/
noncomputable def inv (y : ℝ) : ℝ := if h : 0 < y then Classical.choose (A.honto y h) else 0

theorem inv_spec {y : ℝ} (hy : 0 < y) : 0 < A.inv y ∧ A.inv y * A.μ (A.inv y) = y := by
  unfold inv
  rw [dite_eq_left hy]
  exact Classical.choose_spec (A.honto y hy)

theorem inv_pos {y : ℝ} (hy : 0 < y) : 0 < A.inv y := (A.inv_spec hy).1

theorem inv_mul_mu {y : ℝ} (hy : 0 < y) : A.inv y * A.μ (A.inv y) = y := (A.inv_spec hy).2

/-- the positive solution of x μ(x) = y is unique (strict monotonicity) -/
theorem inv_unique {x y : ℝ} (hx : 0 < x) (hxy : x * A.μ x = y) : A.inv y = x := by
  have hy : 0 < y := hxy ▸ A.hpos x hx
  refine A.hmono.injOn (A.inv_pos hy) hx ?_
  show A.inv y * A.μ (A.inv y) = x * A.μ x
  rw [A.inv_mul_mu hy, hxy]

/-- THE KERNEL OF THE ACTION: ν(y) := x(y)/y, with x(y) the unique positive root of x μ(x) = y -/
noncomputable def nu (y : ℝ) : ℝ := A.inv y / y

theorem nu_mul {y : ℝ} (hy : 0 < y) : A.nu y * y = A.inv y := by
  unfold nu
  field_simp

/-- μ(x) ν(x μ(x)) = 1: the action's μ and the derived ν are reciprocal at corresponding points -/
theorem mu_mul_nu {x : ℝ} (hx : 0 < x) : A.μ x * A.nu (x * A.μ x) = 1 := by
  have hμ := A.mu_pos hx
  unfold nu
  rw [A.inv_unique hx rfl]
  field_simp

/-- THE KERNEL FROM THE GAUSS FORM: if g > 0 solves μ(g/a₀) g = g_N (a₀ > 0), then g = ν(g_N/a₀) g_N -/
theorem kernel_of_gauss {a0 gN g : ℝ} (ha : 0 < a0) (hg : 0 < g) (hgauss : A.μ (g / a0) * g = gN) :
    g = A.nu (gN / a0) * gN := by
  have hx : 0 < g / a0 := div_pos hg ha
  have hgN : 0 < gN := by rw [← hgauss]; exact mul_pos (A.mu_pos hx) hg
  have hxy : g / a0 * A.μ (g / a0) = gN / a0 := by rw [← hgauss]; ring
  have hinv := A.inv_unique hx hxy
  have hn := A.nu_mul (div_pos hgN ha)
  rw [hinv] at hn
  calc g = g / a0 * a0 := by field_simp
    _ = A.nu (gN / a0) * (gN / a0) * a0 := by rw [hn]
    _ = A.nu (gN / a0) * gN := by rw [mul_assoc, div_mul_cancel₀ gN ha.ne']

/-- the converse: for g_N > 0, g = ν(g_N/a₀) g_N is positive and solves μ(g/a₀) g = g_N -/
theorem gauss_of_kernel {a0 gN : ℝ} (ha : 0 < a0) (hgN : 0 < gN) :
    0 < A.nu (gN / a0) * gN ∧ A.μ (A.nu (gN / a0) * gN / a0) * (A.nu (gN / a0) * gN) = gN := by
  have hy : 0 < gN / a0 := div_pos hgN ha
  have h1 : A.nu (gN / a0) * gN / a0 = A.inv (gN / a0) := by rw [← A.nu_mul hy]; ring
  have h2 : A.nu (gN / a0) * gN = a0 * A.inv (gN / a0) := by
    rw [← A.nu_mul hy]; field_simp
  refine ⟨by rw [h2]; exact mul_pos ha (A.inv_pos hy), ?_⟩
  rw [h1, h2]
  calc A.μ (A.inv (gN / a0)) * (a0 * A.inv (gN / a0))
      = a0 * (A.inv (gN / a0) * A.μ (A.inv (gN / a0))) := by ring
    _ = a0 * (gN / a0) := by rw [A.inv_mul_mu hy]
    _ = gN := by field_simp

/-- both directions: for g, g_N > 0, μ(g/a₀) g = g_N ⇔ g = ν(g_N/a₀) g_N -/
theorem gauss_iff_kernel {a0 gN g : ℝ} (ha : 0 < a0) (hg : 0 < g) (hgN : 0 < gN) :
    A.μ (g / a0) * g = gN ↔ g = A.nu (gN / a0) * gN := by
  constructor
  · exact A.kernel_of_gauss ha hg
  · rintro rfl
    exact (A.gauss_of_kernel ha hgN).2

/-- ACTION ⇒ KERNEL, spherical: under the premises of `gauss_form` and g > 0, g(r) = ν(g_N(r)/a₀) g_N(r) at every r > 0 -/
theorem spherical_kernel {g gN M ρ : ℝ → ℝ} {G a0 : ℝ} (ha : 0 < a0)
    (hEL : ∀ r, 0 < r →
      HasDerivAt (fun s => s ^ 2 * (A.μ (g s / a0) * g s)) (G * (4 * Real.pi * r ^ 2 * ρ r)) r)
    (hN : ∀ r, r ≠ 0 → gN r = G * M r / r ^ 2)
    (hM : ∀ r, 0 < r → HasDerivAt M (4 * Real.pi * r ^ 2 * ρ r) r)
    (hreg : Tendsto (fun r => r ^ 2 * (A.μ (g r / a0) * g r - gN r)) (𝓝[>] 0) (𝓝 0))
    (hg : ∀ r, 0 < r → 0 < g r) :
    ∀ r, 0 < r → g r = A.nu (gN r / a0) * gN r := fun r hr =>
  A.kernel_of_gauss ha (hg r hr) (gauss_form hEL hN hM hreg r hr)

/-- the inverse tends to 0⁺ as y → 0⁺ (from positivity and strict monotonicity; no continuity needed) -/
theorem inv_tendsto_zero : Tendsto A.inv (𝓝[>] 0) (𝓝[>] 0) := by
  refine tendsto_nhdsWithin_iff.mpr ⟨?_, ?_⟩
  · rw [Metric.tendsto_nhdsWithin_nhds]
    intro ε hε
    have hε2 : (0 : ℝ) < ε / 2 := half_pos hε
    refine ⟨ε / 2 * A.μ (ε / 2), A.hpos _ hε2, ?_⟩
    intro y hy hyd
    have hy0 : (0 : ℝ) < y := hy
    rw [Real.dist_eq, sub_zero, abs_of_pos hy0] at hyd
    have hX := A.inv_pos hy0
    have hlt : A.inv y < ε / 2 := by
      by_contra hcon
      have hle : ε / 2 ≤ A.inv y := not_lt.mp hcon
      have hm := A.hmono.monotoneOn hε2 hX hle
      rw [A.inv_mul_mu hy0] at hm
      linarith
    rw [Real.dist_eq, sub_zero, abs_of_pos hX]
    linarith
  · filter_upwards [self_mem_nhdsWithin] with y hy
    exact A.inv_pos hy

/-- THE DEEP LIMIT, IN GENERAL: μ(x)/x → 1 as x → 0⁺ implies C2's kernel premise ν(y)√y → 1 as y → 0⁺.
    (With X = x(y): ν(y)√y = X/√(X μ(X)) = √(X/μ(X)), and X → 0⁺.) -/
theorem nu_deep (hdeep : Tendsto (fun x => A.μ x / x) (𝓝[>] 0) (𝓝 1)) :
    Tendsto (fun y => A.nu y * Real.sqrt y) (𝓝[>] 0) (𝓝 1) := by
  have h1 : Tendsto (fun x => Real.sqrt (x / A.μ x)) (𝓝[>] 0) (𝓝 1) := by
    have hinv := hdeep.inv₀ one_ne_zero
    rw [inv_one] at hinv
    have hs := (Real.continuous_sqrt.tendsto 1).comp hinv
    rw [Real.sqrt_one] at hs
    refine hs.congr' ?_
    filter_upwards [self_mem_nhdsWithin] with x hx
    show Real.sqrt ((A.μ x / x)⁻¹) = Real.sqrt (x / A.μ x)
    rw [inv_div]
  refine (h1.comp A.inv_tendsto_zero).congr' ?_
  filter_upwards [self_mem_nhdsWithin] with y hy
  have hy0 : (0 : ℝ) < y := hy
  have hX := A.inv_pos hy0
  have hm := A.mu_pos hX
  have key : ∀ X m : ℝ, 0 < X → 0 < m → Real.sqrt (X / m) = X / (X * m) * Real.sqrt (X * m) := by
    intro X m hX hm
    have hm' := hm.ne'
    have hX' := hX.ne'
    rw [show X / m = (X * m) / m ^ 2 by field_simp, Real.sqrt_div' _ (by positivity), Real.sqrt_sq hm.le]
    field_simp
  show Real.sqrt (A.inv y / A.μ (A.inv y)) = A.nu y * Real.sqrt y
  rw [key _ _ hX hm, A.inv_mul_mu hy0]
  rfl

end AqualMu

/-- ONTONESS FROM THE TWO REGIMES: if x μ(x) is continuous on (0, ∞), μ(x)/x → 1 as x → 0⁺ (deep MOND) and μ(x) → 1 as
    x → ∞ (Newtonian), then x μ(x) takes every value y > 0 at some x > 0 (intermediate value theorem).  So the `honto` field
    can be traded for the two limits; this is where the continuity premise is used. -/
theorem onto_of_regimes {μ : ℝ → ℝ} (hcont : ContinuousOn (fun x => x * μ x) (Set.Ioi 0))
    (hdeep : Tendsto (fun x => μ x / x) (𝓝[>] 0) (𝓝 1)) (hnewt : Tendsto μ atTop (𝓝 1)) :
    ∀ y, 0 < y → ∃ x, 0 < x ∧ x * μ x = y := by
  intro y hy
  have h0 : Tendsto (fun x => x * μ x) (𝓝[>] 0) (𝓝 0) := by
    have hx2 : Tendsto (fun x : ℝ => x ^ 2) (𝓝[>] 0) (𝓝 0) := by
      have := ((continuous_pow 2).tendsto (0 : ℝ)).mono_left (nhdsWithin_le_nhds (s := Set.Ioi 0))
      simpa using this
    have := hx2.mul hdeep
    rw [zero_mul] at this
    refine this.congr' ?_
    filter_upwards [self_mem_nhdsWithin] with x hx
    have hx0 : (x : ℝ) ≠ 0 := ne_of_gt hx
    field_simp
  have hinf : Tendsto (fun x => x * μ x) atTop atTop := tendsto_id.atTop_mul_pos one_pos hnewt
  obtain ⟨x1, hx1y, hx1⟩ := ((h0.eventually (gt_mem_nhds hy)).and self_mem_nhdsWithin).exists
  obtain ⟨x2, hx2y, hx12⟩ := ((hinf.eventually (eventually_gt_atTop y)).and (eventually_gt_atTop x1)).exists
  have hx1' : (0 : ℝ) < x1 := hx1
  have hsub : Set.Icc x1 x2 ⊆ Set.Ioi 0 := fun x hx => lt_of_lt_of_le hx1' hx.1
  obtain ⟨x, hx, hxy⟩ := intermediate_value_Icc hx12.le (hcont.mono hsub) ⟨hx1y.le, hx2y.le⟩
  exact ⟨x, lt_of_lt_of_le hx1' hx.1, hxy⟩

/-- the action premise with ontoness DERIVED from the deep and Newtonian regimes (`onto_of_regimes`) -/
noncomputable def AqualMu.ofRegimes (μ : ℝ → ℝ) (hpos : ∀ x, 0 < x → 0 < x * μ x)
    (hmono : StrictMonoOn (fun x => x * μ x) (Set.Ioi 0)) (hcont : ContinuousOn (fun x => x * μ x) (Set.Ioi 0))
    (hdeep : Tendsto (fun x => μ x / x) (𝓝[>] 0) (𝓝 1)) (hnewt : Tendsto μ atTop (𝓝 1)) : AqualMu :=
  ⟨μ, hpos, hmono, hcont, onto_of_regimes hcont hdeep hnewt⟩

/-! ## P2: μ(x) = (√(1 + 4x²) − 1)/(2x) ⇔ ν(y) = √(1 + 1/y) -/

/-- the P2 interpolating function -/
noncomputable def muP2 (x : ℝ) : ℝ := (Real.sqrt (1 + 4 * x ^ 2) - 1) / (2 * x)

theorem muP2_mul {x : ℝ} (hx : x ≠ 0) : x * muP2 x = (Real.sqrt (1 + 4 * x ^ 2) - 1) / 2 := by
  unfold muP2
  field_simp

/-- P2, action ⇒ kernel: x μ(x) = y (x, y > 0) gives x = √(1 + 1/y) y -/
theorem muP2_to_nuP2 {x y : ℝ} (hx : 0 < x) (hy : 0 < y) (h : x * muP2 x = y) :
    x = Real.sqrt (1 + 1 / y) * y := by
  rw [muP2_mul hx.ne'] at h
  have hs : Real.sqrt (1 + 4 * x ^ 2) = 2 * y + 1 := by linarith
  have hsq : 1 + 4 * x ^ 2 = (2 * y + 1) ^ 2 := by
    rw [← hs, Real.sq_sqrt (by positivity)]
  have hx2 : x ^ 2 = y ^ 2 + y := by nlinarith [hsq]
  rw [← pow_left_inj₀ hx.le (by positivity) two_ne_zero, mul_pow, Real.sq_sqrt (by positivity), hx2]
  field_simp

/-- P2, kernel ⇒ action: x = √(1 + 1/y) y (y > 0) gives x μ(x) = y -/
theorem nuP2_to_muP2 {x y : ℝ} (hy : 0 < y) (h : x = Real.sqrt (1 + 1 / y) * y) : x * muP2 x = y := by
  have hx : 0 < x := by rw [h]; positivity
  have hx2 : x ^ 2 = y ^ 2 + y := by
    rw [h, mul_pow, Real.sq_sqrt (by positivity)]
    field_simp
  have hs : Real.sqrt (1 + 4 * x ^ 2) = 2 * y + 1 := by
    rw [hx2, show 1 + 4 * (y ^ 2 + y) = (2 * y + 1) ^ 2 by ring, Real.sqrt_sq (by linarith)]
  rw [muP2_mul hx.ne', hs]
  ring

/-- P2, both directions: for x, y > 0, x μ(x) = y ⇔ x = √(1 + 1/y) y -/
theorem muP2_iff {x y : ℝ} (hx : 0 < x) (hy : 0 < y) : x * muP2 x = y ↔ x = Real.sqrt (1 + 1 / y) * y :=
  ⟨muP2_to_nuP2 hx hy, nuP2_to_muP2 hy⟩

/-- P2 in physical variables (a₀, g, g_N > 0): μ(g/a₀) g = g_N ⇔ g = √(1 + 1/(g_N/a₀)) g_N (the form of
    `Ownership.P2_sqrt_law_has_EFE`) -/
theorem P2_gauss_iff_kernel {a0 g gN : ℝ} (ha : 0 < a0) (hg : 0 < g) (hgN : 0 < gN) :
    muP2 (g / a0) * g = gN ↔ g = Real.sqrt (1 + 1 / (gN / a0)) * gN := by
  have hx : 0 < g / a0 := div_pos hg ha
  have hy : 0 < gN / a0 := div_pos hgN ha
  have e1 : muP2 (g / a0) * g = gN ↔ g / a0 * muP2 (g / a0) = gN / a0 := by
    constructor
    · intro h; rw [← h]; ring
    · intro h
      have := congrArg (· * a0) h
      rw [show g / a0 * muP2 (g / a0) * a0 = muP2 (g / a0) * g by field_simp,
        div_mul_cancel₀ gN ha.ne'] at this
      exact this
  have e2 : g / a0 = Real.sqrt (1 + 1 / (gN / a0)) * (gN / a0) ↔
      g = Real.sqrt (1 + 1 / (gN / a0)) * gN := by
    rw [div_eq_iff ha.ne', mul_assoc, div_mul_cancel₀ gN ha.ne']
  rw [e1, muP2_iff hx hy, e2]

/-- P2 satisfies the action premise -/
noncomputable def muP2Aqual : AqualMu where
  μ := muP2
  hpos := fun x hx => by
    rw [muP2_mul (ne_of_gt hx)]
    have : 1 < Real.sqrt (1 + 4 * x ^ 2) := by
      rw [Real.lt_sqrt (by norm_num)]
      nlinarith [sq_pos_of_pos hx]
    linarith
  hmono := fun a ha b hb hab => by
    have ha' : (0 : ℝ) < a := ha
    have hb' : (0 : ℝ) < b := hb
    show a * muP2 a < b * muP2 b
    rw [muP2_mul ha'.ne', muP2_mul hb'.ne']
    have : Real.sqrt (1 + 4 * a ^ 2) < Real.sqrt (1 + 4 * b ^ 2) :=
      Real.sqrt_lt_sqrt (by positivity) (by nlinarith)
    linarith
  hcont := by
    have hc : ContinuousOn (fun x : ℝ => (Real.sqrt (1 + 4 * x ^ 2) - 1) / 2) (Set.Ioi 0) := by
      fun_prop
    refine hc.congr fun x hx => ?_
    exact muP2_mul (ne_of_gt hx)
  honto := fun y hy => ⟨Real.sqrt (1 + 1 / y) * y, by positivity, nuP2_to_muP2 hy rfl⟩

/-- P2's deep limit: μ(x)/x = 2/(√(1+4x²) + 1) → 1 as x → 0⁺ -/
theorem muP2_deep : Tendsto (fun x => muP2 x / x) (𝓝[>] 0) (𝓝 1) := by
  have hc : ContinuousAt (fun x : ℝ => 2 / (Real.sqrt (1 + 4 * x ^ 2) + 1)) 0 := by
    refine ContinuousAt.div continuousAt_const ?_ (by positivity)
    fun_prop
  have h1 : Tendsto (fun x : ℝ => 2 / (Real.sqrt (1 + 4 * x ^ 2) + 1)) (𝓝[>] 0) (𝓝 1) := by
    have := hc.tendsto
    norm_num at this
    exact this.mono_left nhdsWithin_le_nhds
  refine h1.congr' ?_
  filter_upwards [self_mem_nhdsWithin] with x hx
  have hx0 : (0 : ℝ) < x := hx
  have hs := Real.sq_sqrt (show (0 : ℝ) ≤ 1 + 4 * x ^ 2 by positivity)
  have hsp : 0 < Real.sqrt (1 + 4 * x ^ 2) + 1 := by positivity
  unfold muP2
  field_simp
  nlinarith [hs]

/-- P2's Newtonian limit: μ(x) = 2/(√(x⁻² + 4) + x⁻¹) → 1 as x → ∞ -/
theorem muP2_newton : Tendsto muP2 atTop (𝓝 1) := by
  have hc : ContinuousAt (fun t : ℝ => 2 / (Real.sqrt (t ^ 2 + 4) + t)) 0 :=
    ContinuousAt.div continuousAt_const (by fun_prop) (by positivity)
  have h4 : Real.sqrt 4 = 2 := by
    rw [show (4 : ℝ) = 2 ^ 2 by norm_num, Real.sqrt_sq (by norm_num)]
  have h1 : Tendsto (fun t : ℝ => 2 / (Real.sqrt (t ^ 2 + 4) + t)) (𝓝 0) (𝓝 1) := by
    have := hc.tendsto
    norm_num [h4] at this
    exact this
  refine (h1.comp tendsto_inv_atTop_zero).congr' ?_
  filter_upwards [eventually_gt_atTop 0] with x hx
  show 2 / (Real.sqrt (x⁻¹ ^ 2 + 4) + x⁻¹) = muP2 x
  have hs : Real.sqrt (1 + 4 * x ^ 2) = x * Real.sqrt (x⁻¹ ^ 2 + 4) := by
    rw [show 1 + 4 * x ^ 2 = x ^ 2 * (x⁻¹ ^ 2 + 4) by field_simp, Real.sqrt_mul (sq_nonneg x),
      Real.sqrt_sq hx.le]
  have hs2 := Real.sq_sqrt (show (0 : ℝ) ≤ x⁻¹ ^ 2 + 4 by positivity)
  have hpos : 0 < Real.sqrt (x⁻¹ ^ 2 + 4) + x⁻¹ := by positivity
  have hxi : x * x⁻¹ = 1 := mul_inv_cancel₀ hx.ne'
  unfold muP2
  rw [hs]
  generalize Real.sqrt (x⁻¹ ^ 2 + 4) = S at hs2 hpos ⊢
  rw [div_eq_div_iff hpos.ne' (by positivity)]
  linear_combination (-x) * hs2 + (-S - x⁻¹) * hxi

/-- for P2 the ontoness also follows from the two regimes (agrees with the explicit root in `muP2Aqual`) -/
theorem muP2_onto_from_regimes : ∀ y, 0 < y → ∃ x, 0 < x ∧ x * muP2 x = y :=
  onto_of_regimes muP2Aqual.hcont muP2_deep muP2_newton

/-- the kernel the P2 action yields is P2: ν(y) = √(1 + 1/y) for y > 0 -/
theorem nuP2_of_action {y : ℝ} (hy : 0 < y) : muP2Aqual.nu y = Real.sqrt (1 + 1 / y) := by
  have hx : 0 < Real.sqrt (1 + 1 / y) * y := by positivity
  have hinv : muP2Aqual.inv y = Real.sqrt (1 + 1 / y) * y :=
    muP2Aqual.inv_unique hx (nuP2_to_muP2 hy rfl)
  unfold AqualMu.nu
  rw [hinv]
  field_simp

/-- ... which is C2's ν_β at β = 1 (reuses `C2_nuBeta_one`) -/
theorem nuP2_of_action_nuBeta {y : ℝ} (hy : 0 < y) : muP2Aqual.nu y = nuBeta 1 y := by
  rw [nuP2_of_action hy, C2_nuBeta_one y hy]

/-- P2's kernel premise, obtained from the action's deep limit by the general theorem `nu_deep` -/
theorem P2_deep_from_action : Tendsto (fun y => muP2Aqual.nu y * Real.sqrt y) (𝓝[>] 0) (𝓝 1) :=
  muP2Aqual.nu_deep muP2_deep

end AqualAction

/-! ## Candidate B with an action premise in place of the kernel premise -/

/-- Candidate B with its P2 field an ACTION premise (the AQUAL μ and its deep limit) instead of a kernel premise.  All other
    fields are those of `CandidateB`; the ownership rule reads the kernel DERIVED from the action (`act.nu`). -/
structure CandidateB_Action (ι : Type*) where
  /-- P1: kappa, c, G, rho_Lambda(z) with positivity and the constancy PREMISE `chain.hflat` -/
  chain : ChainPremises
  /-- P1: kappa = 1/2, FITTED (not derived) -/
  hκ_fit : chain.κ = 1 / 2
  /-- P2 (action form): the AQUAL μ with its properties (DECLARED) -/
  act : AqualAction.AqualMu
  /-- P2 (action form): the deep limit μ(x)/x → 1 (DECLARED) -/
  hμ_deep : Tendsto (fun x => act.μ x / x) (𝓝[>] 0) (𝓝 1)
  /-- P3: the hierarchy of systems (an input) -/
  H : Ownership.Hierarchy ι
  /-- P3: internal acceleration of system i from its own Newtonian field and the external field -/
  accel : ι → ℝ → ℝ → ℝ
  /-- P3: the OWNERSHIP RULE (FG001), POSTULATED, with the action's kernel -/
  hown : ∀ i gN gext, accel i gN gext = Ownership.internalAccel act.nu (chain.a0 0) H i gN gext
  /-- P4: the baryon density parameter -/
  Ωb : ℝ
  /-- P4: the cold density parameter, FITTED -/
  Ωc : ℝ
  hΩb : 0 < Ωb
  hΩc : 0 < Ωc
  /-- P4: the dark mass at a system's edge -/
  darkEdge : ℝ → ℝ → ℝ
  /-- P4: the DECLARED cold-mass rule (C3) -/
  hcold : ∀ Mph Mcoll, darkEdge Mph Mcoll =
    Mph + fex Mph ((1 - Ωb / (Ωb + Ωc)) * Mcoll) * ((1 - Ωb / (Ωb + Ωc)) * Mcoll)

namespace CandidateB_Action

variable {ι : Type*} (A : CandidateB_Action ι)

/-- the kernel premise of C2, DERIVED from the action premise (it is a field of `CandidateB`, a theorem here) -/
theorem kernel_deep : Tendsto (fun y => A.act.nu y * Real.sqrt y) (𝓝[>] 0) (𝓝 1) :=
  A.act.nu_deep A.hμ_deep

/-- the `CandidateB` an action premise yields: ν is the action's inverted kernel, `hν_deep` is `kernel_deep` -/
noncomputable def toCandidateB : CandidateB ι where
  chain := A.chain
  hκ_fit := A.hκ_fit
  ν := A.act.nu
  hν_deep := A.kernel_deep
  H := A.H
  accel := A.accel
  hown := A.hown
  Ωb := A.Ωb
  Ωc := A.Ωc
  hΩb := A.hΩb
  hΩc := A.hΩc
  darkEdge := A.darkEdge
  hcold := A.hcold

/-- THE CHAIN FROM THE ACTION PREMISE: the six conclusions of `CandidateB.predictions`, with the action's kernel.  Proved by
    applying `CandidateB.predictions` to `toCandidateB` (nothing re-proved). -/
theorem predictions :
    (∀ M z : ℝ, 0 < M →
      Tendsto (fun r : ℝ => ((A.chain.G * M / r) * A.act.nu (A.chain.G * M / (r ^ 2 * A.chain.a0 z))) ^ 2) atTop
        (𝓝 (A.chain.G * M * (1 / 2 * A.chain.c * Real.sqrt (A.chain.G * A.chain.ρΛ 0))))) ∧
    (∀ z, A.chain.a0 z = A.chain.a0 0) ∧
    (∀ Ωm ΩΛ : ℝ, 0 < Ωm → 0 ≤ ΩΛ → Ωm + ΩΛ = 1 →
      StrictMonoOn (Efun Ωm ΩΛ) (Set.Ici 0) ∧
        ∀ z, 0 < z → A.chain.a0 z / A.chain.a0 0 = 1 ∧ 1 < Efun Ωm ΩΛ z) ∧
    (∀ (i p : ι) (gN gext : ℝ), A.H.parent i = some p → 0 < gN → A.accel i gN gext / gN = 1) ∧
    ¬ Ownership.EFEFreeRay (fun gN => A.act.nu (gN / A.chain.a0 0) * gN) ∧
    (∀ Mph Mcoll : ℝ, 0 ≤ Mph → 0 < Mcoll →
      A.darkEdge Mph Mcoll = max Mph (A.Ωc / (A.Ωb + A.Ωc) * Mcoll)) :=
  A.toCandidateB.predictions

/-- a TOP-LEVEL system's internal acceleration is positive and solves the action's spherical Gauss form
    μ(g/a₀) g = g_N (g_N > 0) -/
theorem top_solves_gauss {i : ι} (hi : A.H.parent i = none) {gN : ℝ} (hgN : 0 < gN) (gext : ℝ) :
    0 < A.accel i gN gext ∧ A.act.μ (A.accel i gN gext / A.chain.a0 0) * A.accel i gN gext = gN := by
  rw [A.hown, Ownership.top_internal_law _ _ _ hi]
  exact A.act.gauss_of_kernel (A.chain.a0_pos 0) hgN

/-- ... and it is the ONLY positive solution -/
theorem top_unique_gauss {i : ι} (hi : A.H.parent i = none) {gN g : ℝ} (hg : 0 < g)
    (h : A.act.μ (g / A.chain.a0 0) * g = gN) (gext : ℝ) : g = A.accel i gN gext := by
  rw [A.hown, Ownership.top_internal_law _ _ _ hi]
  exact A.act.kernel_of_gauss (A.chain.a0_pos 0) hg h

/-- the top-level branch of the ownership rule is what the spherical AQUAL field equation gives: under the premises of
    `AqualAction.gauss_form` (reduced Euler-Lagrange equation, Newtonian Gauss lemma, regularity) with a₀ = a₀(0) and a
    positive field, g(r) is the top-level internal acceleration for the Newtonian field g_N(r) at every r > 0 -/
theorem top_from_field_equation {i : ι} (hi : A.H.parent i = none) {g gN M ρ : ℝ → ℝ}
    (hEL : ∀ r, 0 < r → HasDerivAt (fun s => s ^ 2 * (A.act.μ (g s / A.chain.a0 0) * g s))
      (A.chain.G * (4 * Real.pi * r ^ 2 * ρ r)) r)
    (hN : ∀ r, r ≠ 0 → gN r = A.chain.G * M r / r ^ 2)
    (hM : ∀ r, 0 < r → HasDerivAt M (4 * Real.pi * r ^ 2 * ρ r) r)
    (hreg : Tendsto (fun r => r ^ 2 * (A.act.μ (g r / A.chain.a0 0) * g r - gN r)) (𝓝[>] 0) (𝓝 0))
    (hg : ∀ r, 0 < r → 0 < g r) (gext : ℝ) :
    ∀ r, 0 < r → g r = A.accel i (gN r) gext := fun r hr =>
  A.top_unique_gauss hi (hg r hr) (AqualAction.gauss_form hEL hN hM hreg r hr) gext

/-- with the P2 action, the kernel B uses is P2 = √(1 + 1/y) on y > 0 -/
theorem kernel_P2 (hP2 : A.act = AqualAction.muP2Aqual) {y : ℝ} (hy : 0 < y) :
    A.toCandidateB.ν y = Real.sqrt (1 + 1 / y) := by
  show A.act.nu y = _
  rw [hP2]
  exact AqualAction.nuP2_of_action hy

/-- NON-VACUITY: the action-form premises are jointly satisfiable.  Witness (unit-free values, NOT a physical fit):
    kappa = 1/2, c = G = rho_Lambda = 1, the P2 action, two systems with system 1 owned by system 0, Omega_b = Omega_c = 1. -/
theorem nonempty_fin2 : Nonempty (CandidateB_Action (Fin 2)) :=
  ⟨{ chain :=
      { κ := 1 / 2, c := 1, G := 1, ρΛ := fun _ => 1, hκ := by norm_num, hc := one_pos, hG := one_pos,
        hρ := fun _ => one_pos, hflat := fun _ => rfl }
     hκ_fit := rfl
     act := AqualAction.muP2Aqual
     hμ_deep := AqualAction.muP2_deep
     H := ⟨fun i => if i = 0 then none else some 0⟩
     accel := fun i gN gext =>
       Ownership.internalAccel AqualAction.muP2Aqual.nu (1 / 2 * 1 * Real.sqrt (1 * 1))
         ⟨fun i => if i = 0 then none else some 0⟩ i gN gext
     hown := fun _ _ _ => rfl
     Ωb := 1
     Ωc := 1
     hΩb := one_pos
     hΩc := one_pos
     darkEdge := fun Mph Mcoll => Mph + fex Mph ((1 - 1 / (1 + 1)) * Mcoll) * ((1 - 1 / (1 + 1)) * Mcoll)
     hcold := fun _ _ => rfl }⟩

end CandidateB_Action
