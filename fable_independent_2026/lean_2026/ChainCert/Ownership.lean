import Mathlib
import ChainCert.Certificates
import ChainCert.Kernel

/-!
# ChainCert.Ownership -- candidate B's ownership rule (P3, FG001) and the no-EFE theorem (CFG179 M3)

## (a) Ownership, as a minimal formal SPECIFICATION (a postulate, not a derivation)

Systems form a hierarchy: each system either has a parent (it is OWNED: a bound subsystem nested inside the parent) or is
top-level.  The rule P3 says: the INTERNAL acceleration of an owned system is Newtonian (no boost); only a top-level system's
internal dynamics use the law `g = nu(g_N/a0) g_N`.  The external field enters neither branch.

Certified here (premises => conclusions):
* `owned_internal_newton`, `top_internal_law`: the two branches of the rule;
* `owned_boost_one`: an owned system's internal-to-Newtonian acceleration ratio is exactly 1, for every `g_N > 0`, every external
  field, every kernel and every `a0` -- the formal content of Gaia DR4 Arm C (gamma-hat = 1).  This is near-definitional: it
  restates the postulate; Lean adds only that nothing else in the chain disturbs it;
* `wideBinary_gammaHat_one`: for any finite population of OWNED pairs, every positively weighted mean of the per-pair ratio is 1;
* `top_boost_gt_one_nuMono`, `top_boost_gt_one_P2`: the contrast -- a TOP-LEVEL system in the MOND regime has ratio > 1 under
  nu_mono or P2 (the bare law, no external field; this is NOT the merged-law number 1.16-1.18 of Arm A, which is numerical);
* `ownership_distinguishes`, `ownership_not_field_local`: whenever the kernel is not 1 at some `g_N/a0`, a top-level and an owned
  system with the SAME internal and external fields get DIFFERENT internal accelerations, so no function of the field data alone
  (in particular, no function of the local total field) reproduces the rule.  Ownership reads membership data -- which system a
  body belongs to -- and is in that sense NON-LOCAL.

NOT certified: that nature realises this rule; that any action produces it (no committed action produces candidate B); which
real systems are owned (the hierarchy `H` is an input); the DR4 estimator's statistics.

## (b) The no-EFE theorem (CFG179, S1 M3)

A law is "external-field-free" (EFE-free) in the superposition sense when a subsystem's internal field, computed from the TOTAL
Newtonian field `z + z_e` minus the external part `F(z_e)`, is the same as in isolation: `F(z + z_e) - F(z_e) = F(z)`.
Certified here:
* `noEFE_continuousLinear`: on any real topological vector spaces, a continuous EFE-free law IS a continuous linear map
  (EFE-free is Cauchy's additivity, `F(x + y) = F x + F y`; then Mathlib's `AddMonoidHom.toRealLinearMap`);
  `noEFE_linear_R3` for `EuclideanSpace ℝ (Fin 3)`;
* `noEFE_linear_real`: on the line, `F z = F 1 * z` (Newton with a rescaled G);
* `noEFE_linear_ray`: the same on the physical ray `z, z_e > 0`, needing continuity only on `(0, ∞)`;
* `nonlinear_not_efeFree_real`, `nonlinear_not_efeFree`: the contrapositive -- no nonlinear continuous law is EFE-free;
* `deep_not_efeFreeRay`: NO law `y ↦ nu(y) y` with MOND's square-root pull (`nu(y) sqrt y -> 1` as `y -> 0+`, the kernel
  premise of C2) is EFE-free even on the ray -- no continuity needed (EFE-free forces `nu(y/4) sqrt(y/4) = nu(y) sqrt(y)/2`);
* `law_not_efeFreeRay`: the dimensional law `g_N ↦ nu(g_N/a0) g_N` (a0 > 0) likewise; instances `nuMono_law_has_EFE`,
  `P2_law_has_EFE` (nu_beta at beta = 1) and `P2_sqrt_law_has_EFE` (nu = sqrt(1 + a0/g_N), CFG179's form);
* `vecLaw_not_efeFree`, `vecLaw_R3_not_efeFree`: the vector law `g_N ↦ nu(|g_N|/a0) g_N` on any nontrivial real normed space
  (in particular R^3) is not EFE-free;
* `deep_kernel_ne_one`: a kernel with that deep limit is not identically 1 on the ray (so the two ownership branches differ).
So any law with MOND's square-root pull that is LOCAL IN THE TOTAL FIELD must show an external-field effect.  Ownership escapes
the theorem only by being non-local: WHICH branch applies (law or Newton) is decided by membership data, not by the field, so the
rule as a whole is not a function of the total field (part (a)).  The owned branch itself is Newton, which is linear and hence
EFE-free, consistent with the theorem.

Scope: "law" here is a pointwise (algebraic, QUMOND-type) map from Newtonian field to field, as in CFG179 M3.  Field-equation
theories (AQUAL/QUMOND PDEs) are not formalised; the theorem says nothing about them beyond this pointwise reading.
-/

open Filter Topology

namespace Ownership

/-! ## (a) Ownership -/

/-- A hierarchy of systems on an index type: `parent i = some p` means system `i` is OWNED (nested inside `p`);
    `parent i = none` means `i` is top-level.  Bookkeeping only: which real systems are nested is an INPUT. -/
structure Hierarchy (ι : Type*) where
  parent : ι → Option ι

/-- The ownership rule P3 (FG001, a POSTULATE): the internal acceleration of system `i`, from its own Newtonian field `gN`, in an
    external field `gext`.  Top-level: the law `nu(gN/a0) gN`.  Owned: Newton, `gN`.  `gext` enters neither branch. -/
noncomputable def internalAccel {ι : Type*} (ν : ℝ → ℝ) (a0 : ℝ) (H : Hierarchy ι) (i : ι) (gN _gext : ℝ) : ℝ :=
  match H.parent i with
  | none => ν (gN / a0) * gN
  | some _ => gN

/-- the internal-to-Newtonian acceleration ratio (the "boost") -/
noncomputable def boost {ι : Type*} (ν : ℝ → ℝ) (a0 : ℝ) (H : Hierarchy ι) (i : ι) (gN gext : ℝ) : ℝ :=
  internalAccel ν a0 H i gN gext / gN

theorem owned_internal_newton {ι : Type*} (ν : ℝ → ℝ) (a0 : ℝ) (H : Hierarchy ι) {i p : ι}
    (hp : H.parent i = some p) (gN gext : ℝ) : internalAccel ν a0 H i gN gext = gN := by
  simp [internalAccel, hp]

theorem top_internal_law {ι : Type*} (ν : ℝ → ℝ) (a0 : ℝ) (H : Hierarchy ι) {i : ι}
    (hi : H.parent i = none) (gN gext : ℝ) : internalAccel ν a0 H i gN gext = ν (gN / a0) * gN := by
  simp [internalAccel, hi]

/-- ARM C: an owned subsystem's boost is exactly 1 for every g_N > 0, every external field, every kernel and every a0. -/
theorem owned_boost_one {ι : Type*} (ν : ℝ → ℝ) (a0 : ℝ) (H : Hierarchy ι) {i p : ι}
    (hp : H.parent i = some p) {gN : ℝ} (hgN : 0 < gN) (gext : ℝ) : boost ν a0 H i gN gext = 1 := by
  rw [boost, owned_internal_newton ν a0 H hp, div_self hgN.ne']

/-- ARM C for a population: wide binaries each OWNED by their host; any weighted mean of the per-pair boost with positive total
    weight is exactly 1 (the formal content of gamma-hat = 1.000; the DR4 estimator itself is not formalised). -/
theorem wideBinary_gammaHat_one {ι κ : Type*} (ν : ℝ → ℝ) (a0 : ℝ) (H : Hierarchy ι) (s : Finset κ)
    (pair : κ → ι) (gN gext w : κ → ℝ) (howned : ∀ k ∈ s, ∃ p, H.parent (pair k) = some p)
    (hgN : ∀ k ∈ s, 0 < gN k) (hW : 0 < ∑ k ∈ s, w k) :
    (∑ k ∈ s, w k * boost ν a0 H (pair k) (gN k) (gext k)) / ∑ k ∈ s, w k = 1 := by
  have hsum : ∑ k ∈ s, w k * boost ν a0 H (pair k) (gN k) (gext k) = ∑ k ∈ s, w k := by
    refine Finset.sum_congr rfl fun k hk => ?_
    obtain ⟨p, hp⟩ := howned k hk
    rw [owned_boost_one ν a0 H hp (hgN k hk), mul_one]
  rw [hsum, div_self hW.ne']

/-- the contrast (bare law, no external field): a TOP-LEVEL system with g_N > 0 has boost nu_mono(g_N/a0) > 1 -/
theorem top_boost_gt_one_nuMono {ι : Type*} {a0 : ℝ} (ha : 0 < a0) (H : Hierarchy ι) {i : ι}
    (hi : H.parent i = none) {gN : ℝ} (hgN : 0 < gN) (gext : ℝ) : 1 < boost nuMono a0 H i gN gext := by
  rw [boost, top_internal_law nuMono a0 H hi, mul_div_assoc, div_self hgN.ne', mul_one, nuMono]
  have hs : 0 < Real.sqrt (gN / a0) := Real.sqrt_pos.mpr (div_pos hgN ha)
  have he1 : Real.exp (-Real.sqrt (gN / a0)) < 1 := Real.exp_lt_one_iff.mpr (by linarith)
  have he0 : 0 < Real.exp (-Real.sqrt (gN / a0)) := Real.exp_pos _
  rw [lt_div_iff₀ (by linarith)]
  linarith

/-- the contrast for P2, nu(y) = sqrt(1 + 1/y): a TOP-LEVEL system with g_N > 0 has boost > 1 -/
theorem top_boost_gt_one_P2 {ι : Type*} {a0 : ℝ} (ha : 0 < a0) (H : Hierarchy ι) {i : ι}
    (hi : H.parent i = none) {gN : ℝ} (hgN : 0 < gN) (gext : ℝ) :
    1 < boost (fun y => Real.sqrt (1 + 1 / y)) a0 H i gN gext := by
  rw [boost, top_internal_law _ a0 H hi, mul_div_assoc, div_self hgN.ne', mul_one]
  rw [Real.lt_sqrt (by norm_num)]
  have : 0 < 1 / (gN / a0) := by positivity
  linarith

/-- NON-LOCALITY: a top-level and an owned system with the SAME internal and external fields get different internal
    accelerations whenever the kernel is not 1 at g_N/a0 (g_N ≠ 0). -/
theorem ownership_distinguishes {ι : Type*} (ν : ℝ → ℝ) (a0 : ℝ) (H : Hierarchy ι) {i j p : ι}
    (hi : H.parent i = none) (hj : H.parent j = some p) {gN : ℝ} (hgN : gN ≠ 0) (hν : ν (gN / a0) ≠ 1)
    (gext : ℝ) : internalAccel ν a0 H i gN gext ≠ internalAccel ν a0 H j gN gext := by
  rw [top_internal_law ν a0 H hi, owned_internal_newton ν a0 H hj]
  intro h
  exact hν (mul_right_cancel₀ hgN (by rw [h, one_mul]))

/-- ... hence NO function of the field data alone (internal and external field; a fortiori the local total field) reproduces
    the ownership rule on a hierarchy that has a top-level and an owned system: the rule needs membership data. -/
theorem ownership_not_field_local {ι : Type*} (ν : ℝ → ℝ) (a0 : ℝ) (H : Hierarchy ι) {i j p : ι}
    (hi : H.parent i = none) (hj : H.parent j = some p) {gN : ℝ} (hgN : gN ≠ 0) (hν : ν (gN / a0) ≠ 1) :
    ¬ ∃ F : ℝ → ℝ → ℝ, ∀ k g ge, internalAccel ν a0 H k g ge = F g ge := by
  rintro ⟨F, hF⟩
  exact ownership_distinguishes ν a0 H hi hj hgN hν 0 (by rw [hF i gN 0, hF j gN 0])

/-! ## (b) The no-EFE theorem (CFG179 M3) -/

/-- EFE-free (superposition): the internal field `F(z + z_e) - F(z_e)` equals the isolated `F(z)` for every internal `z` and
    external `z_e`.  A law "local in the total field" that shows no external-field effect. -/
def EFEFree {E V : Type*} [AddCommGroup E] [AddCommGroup V] (F : E → V) : Prop :=
  ∀ z ze : E, F (z + ze) - F ze = F z

/-- EFE-free on the physical ray only (both fields positive, as in CFG179's sympy M3) -/
def EFEFreeRay (F : ℝ → ℝ) : Prop :=
  ∀ z ze : ℝ, 0 < z → 0 < ze → F (z + ze) - F ze = F z

/-- the no-EFE theorem, general form: a continuous EFE-free law between real topological vector spaces is a continuous
    LINEAR map. -/
theorem noEFE_continuousLinear {E V : Type*} [AddCommGroup E] [Module ℝ E] [TopologicalSpace E]
    [ContinuousSMul ℝ E] [AddCommGroup V] [Module ℝ V] [TopologicalSpace V] [ContinuousSMul ℝ V] [T2Space V]
    {F : E → V} (hc : Continuous F) (h : EFEFree F) : ∃ L : E →L[ℝ] V, ⇑L = F :=
  ⟨(AddMonoidHom.mk' F fun x y => sub_eq_iff_eq_add.mp (h x y)).toRealLinearMap hc, rfl⟩

/-- the vector version in R^3 -/
theorem noEFE_linear_R3 {F : EuclideanSpace ℝ (Fin 3) → EuclideanSpace ℝ (Fin 3)} (hc : Continuous F)
    (h : EFEFree F) : ∃ L : EuclideanSpace ℝ (Fin 3) →L[ℝ] EuclideanSpace ℝ (Fin 3), ⇑L = F :=
  noEFE_continuousLinear hc h

/-- the scalar version: a continuous EFE-free F : ℝ → ℝ is F z = F 1 * z (Newton with a rescaled G) -/
theorem noEFE_linear_real {F : ℝ → ℝ} (hc : Continuous F) (h : EFEFree F) (z : ℝ) : F z = F 1 * z := by
  have := map_real_smul (AddMonoidHom.mk' F fun x y => sub_eq_iff_eq_add.mp (h x y)) hc z 1
  simp only [AddMonoidHom.mk'_apply, smul_eq_mul, mul_one] at this
  rw [this, mul_comm]

/-- the scalar version on the physical ray: continuous on (0, ∞) and EFE-free for z, z_e > 0 gives F z = F 1 * z for z > 0.
    (Proof: extend F to G x = F(x + c) - F(c), independent of any admissible c > max(0, -x); G is additive and continuous.) -/
theorem noEFE_linear_ray {F : ℝ → ℝ} (hF : ContinuousOn F (Set.Ioi 0)) (h : EFEFreeRay F) :
    ∀ z, 0 < z → F z = F 1 * z := by
  have hadd : ∀ x y, 0 < x → 0 < y → F (x + y) = F x + F y := fun x y hx hy => by
    have := h x y hx hy; linarith
  have shift : ∀ x c c', 0 < c → 0 < x + c → 0 < c' → 0 < x + c' →
      F (x + c) - F c = F (x + c') - F c' := by
    intro x c c' h1 h2 h1' h2'
    have e1 := hadd (x + c) c' h2 h1'
    have e2 := hadd (x + c') c h2' h1
    rw [show x + c + c' = x + c' + c by ring] at e1
    linarith
  set G : ℝ → ℝ := fun x => F (x + (|x| + 1)) - F (|x| + 1) with hG
  have hGc : ∀ x c, 0 < c → 0 < x + c → G x = F (x + c) - F c := by
    intro x c h1 h2
    simp only [hG]
    exact shift x _ _ (by positivity) (by cases abs_cases x <;> linarith) h1 h2
  have hGadd : ∀ x y, G (x + y) = G x + G y := by
    intro x y
    have hc : 0 < |x| + |y| + 1 := by positivity
    have hxc : 0 < x + (|x| + |y| + 1) := by
      cases abs_cases x <;> cases abs_cases y <;> linarith
    have hyc : 0 < y + (|x| + |y| + 1) := by
      cases abs_cases x <;> cases abs_cases y <;> linarith
    rw [hGc x _ hc hxc, hGc y _ hc hyc,
      hGc (x + y) ((|x| + |y| + 1) + (|x| + |y| + 1)) (by positivity) (by linarith)]
    have e1 := hadd _ _ hxc hyc
    have e2 := hadd _ _ hc hc
    rw [show x + (|x| + |y| + 1) + (y + (|x| + |y| + 1)) = x + y + ((|x| + |y| + 1) + (|x| + |y| + 1)) by ring]
      at e1
    linarith
  have hGcont : Continuous G := by
    rw [continuous_iff_continuousAt]
    intro x₀
    have hc : 0 < |x₀| + 2 := by positivity
    have hpos : 0 < x₀ + (|x₀| + 2) := by cases abs_cases x₀ <;> linarith
    have hev : (fun x => F (x + (|x₀| + 2)) - F (|x₀| + 2)) =ᶠ[𝓝 x₀] G := by
      filter_upwards [Ioi_mem_nhds (show x₀ - 1 < x₀ by linarith)] with x hx
      have hx' : x₀ - 1 < x := hx
      exact (hGc x _ hc (by cases abs_cases x₀ <;> linarith)).symm
    refine ContinuousAt.congr ?_ hev
    have hFat : ContinuousAt F (x₀ + (|x₀| + 2)) := hF.continuousAt (Ioi_mem_nhds hpos)
    have hcomp : ContinuousAt (fun x => F (x + (|x₀| + 2))) x₀ :=
      ContinuousAt.comp (g := F) (f := fun x => x + (|x₀| + 2)) hFat (by fun_prop)
    exact hcomp.sub continuousAt_const
  have hlin := noEFE_linear_real hGcont (by intro z ze; rw [hGadd]; ring)
  intro z hz
  have hGz : G z = F z := by
    rw [hGc z 1 one_pos (by linarith)]; have := hadd z 1 hz one_pos; linarith
  have hG1 : G 1 = F 1 := by
    rw [hGc 1 1 one_pos (by norm_num)]; have := hadd 1 1 one_pos one_pos; linarith
  rw [← hGz, ← hG1]
  exact hlin z

/-- contrapositive, scalar: a continuous law that is not of the form k z for any k is not EFE-free -/
theorem nonlinear_not_efeFree_real {F : ℝ → ℝ} (hc : Continuous F) (hnl : ∀ k : ℝ, ∃ z, F z ≠ k * z) :
    ¬ EFEFree F := by
  intro h
  obtain ⟨z, hz⟩ := hnl (F 1)
  exact hz (noEFE_linear_real hc h z)

/-- contrapositive, vector: a continuous law that agrees with no continuous linear map is not EFE-free -/
theorem nonlinear_not_efeFree {E V : Type*} [AddCommGroup E] [Module ℝ E] [TopologicalSpace E]
    [ContinuousSMul ℝ E] [AddCommGroup V] [Module ℝ V] [TopologicalSpace V] [ContinuousSMul ℝ V] [T2Space V]
    {F : E → V} (hc : Continuous F) (hnl : ∀ L : E →L[ℝ] V, ∃ z, F z ≠ L z) : ¬ EFEFree F := by
  intro h
  obtain ⟨L, hL⟩ := noEFE_continuousLinear hc h
  obtain ⟨z, hz⟩ := hnl L
  exact hz (by rw [← hL])

/-- MOND's square-root pull forbids EFE-freedom: if nu(y) sqrt y -> 1 as y -> 0+ (the kernel premise of C2), the law
    y ↦ nu(y) y is NOT EFE-free, even on the ray, and even without continuity. -/
theorem deep_not_efeFreeRay (ν : ℝ → ℝ) (hν : Tendsto (fun y => ν y * Real.sqrt y) (𝓝[>] 0) (𝓝 1)) :
    ¬ EFEFreeRay (fun y => ν y * y) := by
  intro h
  have h2 : ∀ x, 0 < x → ν (x + x) * (x + x) = 2 * (ν x * x) := fun x hx => by
    have := h x x hx hx; simp only at this; linarith
  have key : ∀ y, 0 < y → ν (y / 4) * Real.sqrt (y / 4) = ν y * Real.sqrt y / 2 := by
    intro y hy
    have e1 := h2 (y / 4) (by positivity)
    have e2 := h2 (y / 2) (by positivity)
    rw [show y / 4 + y / 4 = y / 2 by ring] at e1
    rw [show y / 2 + y / 2 = y by ring] at e2
    have hprod : ν (y / 4) * y = ν y * y := by linear_combination -e2 - 2 * e1
    have hνeq : ν (y / 4) = ν y := mul_right_cancel₀ hy.ne' hprod
    have hsq : Real.sqrt (y / 4) = Real.sqrt y / 2 := by
      rw [Real.sqrt_div hy.le, show (4 : ℝ) = 2 ^ 2 by norm_num, Real.sqrt_sq (by norm_num)]
    rw [hνeq, hsq]; ring
  have hs : Tendsto (fun y : ℝ => y / 4) (𝓝[>] 0) (𝓝[>] 0) := by
    refine tendsto_nhdsWithin_iff.mpr ⟨?_, ?_⟩
    · have : Tendsto (fun y : ℝ => y / 4) (𝓝 0) (𝓝 (0 / 4)) :=
        ((continuous_id.div_const (4 : ℝ)).tendsto 0)
      rw [zero_div] at this
      exact this.mono_left nhdsWithin_le_nhds
    · filter_upwards [self_mem_nhdsWithin] with y hy
      exact Set.mem_Ioi.mpr (by have : (0 : ℝ) < y := hy; positivity)
  have hA : Tendsto (fun y => ν y * Real.sqrt y / 2) (𝓝[>] 0) (𝓝 1) := by
    refine (hν.comp hs).congr' ?_
    filter_upwards [self_mem_nhdsWithin] with y hy
    exact key y hy
  have hB : Tendsto (fun y => ν y * Real.sqrt y / 2) (𝓝[>] 0) (𝓝 (1 / 2)) := hν.div_const 2
  have := tendsto_nhds_unique hA hB
  norm_num at this

/-- a kernel with MOND's deep limit is not identically 1 on the ray (so ownership's two branches really differ somewhere) -/
theorem deep_kernel_ne_one (ν : ℝ → ℝ) (hν : Tendsto (fun y => ν y * Real.sqrt y) (𝓝[>] 0) (𝓝 1)) :
    ∃ y, 0 < y ∧ ν y ≠ 1 := by
  by_contra hcon
  push Not at hcon
  have hs : Tendsto Real.sqrt (𝓝[>] 0) (𝓝 0) := by
    have := (Real.continuous_sqrt.tendsto 0).mono_left (nhdsWithin_le_nhds (s := Set.Ioi (0 : ℝ)))
    simpa using this
  have h0 : Tendsto (fun y => ν y * Real.sqrt y) (𝓝[>] 0) (𝓝 0) := by
    refine hs.congr' ?_
    filter_upwards [self_mem_nhdsWithin] with y hy
    rw [hcon y hy, one_mul]
  have := tendsto_nhds_unique hν h0
  norm_num at this

/-- the dimensional law g_N ↦ nu(g_N/a0) g_N, a0 > 0, with the C2 kernel premise, is NOT EFE-free on the ray: merged
    rivers with MOND's square-root pull must interact (CFG179 M3). -/
theorem law_not_efeFreeRay {a0 : ℝ} (ha : 0 < a0) (ν : ℝ → ℝ)
    (hν : Tendsto (fun y => ν y * Real.sqrt y) (𝓝[>] 0) (𝓝 1)) :
    ¬ EFEFreeRay (fun gN => ν (gN / a0) * gN) := by
  intro h
  apply deep_not_efeFreeRay ν hν
  intro z ze hz hze
  have := h (a0 * z) (a0 * ze) (by positivity) (by positivity)
  simp only at this ⊢
  rw [show (a0 * z + a0 * ze) / a0 = z + ze by field_simp, show a0 * ze / a0 = ze by field_simp,
    show a0 * z / a0 = z by field_simp] at this
  have h' : a0 * (ν (z + ze) * (z + ze) - ν ze * ze) = a0 * (ν z * z) := by linear_combination this
  exact mul_left_cancel₀ ha.ne' h'

/-- instance: the headline kernel nu_mono shows an external-field effect when merged locally -/
theorem nuMono_law_has_EFE {a0 : ℝ} (ha : 0 < a0) : ¬ EFEFreeRay (fun gN => nuMono (gN / a0) * gN) :=
  law_not_efeFreeRay ha nuMono nuMono_deep

/-- instance: P2 (nu_beta at beta = 1) shows an external-field effect when merged locally -/
theorem P2_law_has_EFE {a0 : ℝ} (ha : 0 < a0) : ¬ EFEFreeRay (fun gN => nuBeta 1 (gN / a0) * gN) :=
  law_not_efeFreeRay ha (nuBeta 1) (C2_nuBeta_deep 1 one_pos)

/-- instance: P2 in CFG179's explicit form nu = sqrt(1 + a0/g_N) = sqrt(1 + 1/y), y = g_N/a0 -/
theorem P2_sqrt_law_has_EFE {a0 : ℝ} (ha : 0 < a0) :
    ¬ EFEFreeRay (fun gN => Real.sqrt (1 + 1 / (gN / a0)) * gN) := by
  refine law_not_efeFreeRay ha (fun y => Real.sqrt (1 + 1 / y)) ?_
  refine (C2_nuBeta_deep 1 one_pos).congr' ?_
  filter_upwards [self_mem_nhdsWithin] with y hy
  rw [C2_nuBeta_one y hy]

/-- the vector law g_N ↦ nu(|g_N|/a0) g_N on a real normed space -/
noncomputable def vecLaw {E : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E] (ν : ℝ → ℝ) (a0 : ℝ) (v : E) : E :=
  ν (‖v‖ / a0) • v

/-- the vector law with the C2 kernel premise is NOT EFE-free on any nontrivial real normed space: restricted to a ray it is
    the scalar law, which is not additive there. -/
theorem vecLaw_not_efeFree {E : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E] [Nontrivial E] {a0 : ℝ}
    (ha : 0 < a0) (ν : ℝ → ℝ) (hν : Tendsto (fun y => ν y * Real.sqrt y) (𝓝[>] 0) (𝓝 1)) :
    ¬ EFEFree (vecLaw (E := E) ν a0) := by
  intro h
  obtain ⟨v, hv⟩ := exists_ne (0 : E)
  set e : E := ‖v‖⁻¹ • v with he
  have he1 : ‖e‖ = 1 := norm_smul_inv_norm hv
  have he0 : e ≠ 0 := by intro h0; rw [h0, norm_zero] at he1; norm_num at he1
  have hray : ∀ t, 0 < t → vecLaw ν a0 (t • e) = (ν (t / a0) * t) • e := by
    intro t ht
    rw [vecLaw, norm_smul, he1, mul_one, Real.norm_eq_abs, abs_of_pos ht, smul_smul]
  apply law_not_efeFreeRay ha ν hν
  intro z ze hz hze
  have hh := h (z • e) (ze • e)
  rw [← add_smul, hray _ (by linarith), hray _ hze, hray _ hz, ← sub_smul] at hh
  exact smul_left_injective ℝ he0 hh

/-- in R^3 -/
theorem vecLaw_R3_not_efeFree {a0 : ℝ} (ha : 0 < a0) (ν : ℝ → ℝ)
    (hν : Tendsto (fun y => ν y * Real.sqrt y) (𝓝[>] 0) (𝓝 1)) :
    ¬ EFEFree (vecLaw (E := EuclideanSpace ℝ (Fin 3)) ν a0) :=
  vecLaw_not_efeFree ha ν hν

end Ownership
