import Mathlib
import ChainCert.Certificates
import ChainCert.Kernel
import ChainCert.Chain
import ChainCert.Ownership
import ChainCert.A0Numeric

/-!
# ChainCert.Theory -- candidate B as ONE structure of named premises, and the chain to its predictions

`CandidateB ι` bundles the theory's postulates as fields (ι indexes the systems of a hierarchy).  Every non-derived ingredient
is a field; nothing is an `axiom`.  `CandidateB.predictions` composes links ALREADY certified elsewhere in the library.

POSTULATES (fields; Lean certifies none of them):
* P1 tie -- `chain : ChainPremises` (reused from `ChainCert.Chain`): `a0(z) = kappa c sqrt(G rho_Lambda(z))` with
  `chain.hflat : rho_Lambda(z) = rho_Lambda(0)` (the constancy PREMISE, w = -1) and `hκ_fit : kappa = 1/2` (FITTED to the BTFR
  zero point; C5 shows the closure leaves kappa free);
* P2 kernel -- `ν` with `hν_deep : nu(y) sqrt y -> 1` as y -> 0+ (the DECLARED kernel premise of C2; it holds for nu_mono,
  `nuMono_deep`, and for nu_beta, `C2_nuBeta_deep`, which contains P2 = sqrt(1 + 1/y));
* P3 ownership (FG001) -- the hierarchy `H` (which systems are nested: an INPUT) and `hown`: every system's internal
  acceleration is `Ownership.internalAccel` (law if top-level, Newton if owned) -- the ownership RULE, postulated; no committed
  action produces it;
* P4 cold component -- `Ωb`, `Ωc > 0` (Omega_c FITTED) and `hcold`: the edge dark mass is the DECLARED C3 rule
  `M_ph + f_ex M_c`, `M_c = (1 - f_b) M_coll`, `f_b = Omega_b/(Omega_b + Omega_c)`.

CONSEQUENCES (certified, each from the premises above):
1. `btfr`: v^4 -> G M (1/2) c sqrt(G rho_Lambda(0)) at every redshift (C2 + `ChainPremises.a0_flat` + kappa = 1/2);
2. `a0_flat`: a0(z) = a0(0) (from the constancy premise only);
3. `rival_separates`: B's a0(z)/a0(0) = 1 while the rival a0 ∝ H(z) has E(z) > 1 for z > 0, strictly increasing (C4);
   `a0_numeric`: with c, G declared, rho_Lambda(0) = 3 H0^2 Omega_Lambda/(8 pi G) and the stated input intervals, a0(z) lies in
   (9.24e-11, 9.48e-11) m/s^2 at every z (`ChainCert.A0Numeric`);
4. `owned_boost_one`, `gammaHat_one`: owned subsystems have boost exactly 1 -- DR4 Arm C, gamma-hat = 1.000;
5. `merged_law_has_EFE`, `merged_vecLaw_has_EFE`: B's own kernel, merged LOCALLY in the total field, is not EFE-free
   (Ownership (b)); `ownership_nonlocal`: B's rule is not a function of the field alone (it reads membership data);
6. `cold_edge_mass`, `cold_edge_monotone`: dark edge mass = max(M_ph, Omega_c/(Omega_b + Omega_c) M_coll), monotone in M_coll (C3).
`nonempty_fin2` shows the premises are jointly satisfiable (a two-system witness), so the predictions are not vacuous.

NOT certified: kappa = 1/2 (FITTED), that rho_Lambda is constant, that the kernel is nu_mono or P2, that ownership is realised by
any action, which systems are owned, the relativistic sector, and every empirical fit.  Nothing here says the theory is closed or
derived.
-/

open Filter Topology

/-- Candidate B: its postulates P1-P4 as NAMED fields (see the module docstring for which are fitted or declared). -/
structure CandidateB (ι : Type*) where
  /-- P1: kappa, c, G, rho_Lambda(z) with positivity and the constancy PREMISE `chain.hflat` -/
  chain : ChainPremises
  /-- P1: kappa = 1/2, FITTED (not derived) -/
  hκ_fit : chain.κ = 1 / 2
  /-- P2: the DECLARED kernel -/
  ν : ℝ → ℝ
  /-- P2: the kernel premise of C2 (deep limit nu(y) sqrt y -> 1) -/
  hν_deep : Tendsto (fun y => ν y * Real.sqrt y) (𝓝[>] 0) (𝓝 1)
  /-- P3: the hierarchy of systems (an input: which systems are nested in which) -/
  H : Ownership.Hierarchy ι
  /-- P3: internal acceleration of system i from its own Newtonian field and the external field -/
  accel : ι → ℝ → ℝ → ℝ
  /-- P3: the OWNERSHIP RULE (FG001), POSTULATED -/
  hown : ∀ i gN gext, accel i gN gext = Ownership.internalAccel ν (chain.a0 0) H i gN gext
  /-- P4: the baryon density parameter -/
  Ωb : ℝ
  /-- P4: the cold density parameter, FITTED -/
  Ωc : ℝ
  hΩb : 0 < Ωb
  hΩc : 0 < Ωc
  /-- P4: the dark mass at a system's edge, from its phantom mass and its collapse mass -/
  darkEdge : ℝ → ℝ → ℝ
  /-- P4: the DECLARED cold-mass rule (C3) -/
  hcold : ∀ Mph Mcoll, darkEdge Mph Mcoll =
    Mph + fex Mph ((1 - Ωb / (Ωb + Ωc)) * Mcoll) * ((1 - Ωb / (Ωb + Ωc)) * Mcoll)

namespace CandidateB

variable {ι : Type*} (B : CandidateB ι)

/-- the tie at the fitted value: a0(z) = (1/2) c sqrt(G rho_Lambda(z)) -/
theorem a0_eq (z : ℝ) : B.chain.a0 z = 1 / 2 * B.chain.c * Real.sqrt (B.chain.G * B.chain.ρΛ z) := by
  rw [ChainPremises.a0, B.hκ_fit]

/-- flat a0(z), from the constancy premise (reuses `ChainPremises.a0_flat`) -/
theorem a0_flat (z : ℝ) : B.chain.a0 z = B.chain.a0 0 := B.chain.a0_flat z

/-- 1. the BTFR zero point at every redshift, for B's declared kernel: v^4 -> G M (1/2) c sqrt(G rho_Lambda(0)) -/
theorem btfr {M : ℝ} (hM : 0 < M) (z : ℝ) :
    Tendsto (fun r : ℝ => ((B.chain.G * M / r) * B.ν (B.chain.G * M / (r ^ 2 * B.chain.a0 z))) ^ 2) atTop
      (𝓝 (B.chain.G * M * (1 / 2 * B.chain.c * Real.sqrt (B.chain.G * B.chain.ρΛ 0)))) := by
  have h := C2_deep_mond_flat_speed B.chain.hG hM (B.chain.a0_pos z) B.ν B.hν_deep
  have e : B.chain.G * M * B.chain.a0 z =
      B.chain.G * M * (1 / 2 * B.chain.c * Real.sqrt (B.chain.G * B.chain.ρΛ 0)) := by
    rw [B.chain.a0_flat z, B.a0_eq 0]
  rw [e] at h
  exact h

/-- 3. against the rival a0 ∝ H(z) on any flat background: the rival's E(z) is strictly increasing on z >= 0, and at every
    z > 0 B's ratio a0(z)/a0(0) is 1 while the rival's E(z) exceeds 1 (C4) -/
theorem rival_separates {Ωm ΩΛ : ℝ} (hm : 0 < Ωm) (hΛ : 0 ≤ ΩΛ) (hsum : Ωm + ΩΛ = 1) :
    StrictMonoOn (Efun Ωm ΩΛ) (Set.Ici 0) ∧
      ∀ z, 0 < z → B.chain.a0 z / B.chain.a0 0 = 1 ∧ 1 < Efun Ωm ΩΛ z := by
  refine ⟨C4_rival_strictMono Ωm ΩΛ hm hΛ, fun z hz => ⟨?_, C4_rival_exceeds_flat Ωm ΩΛ z hm hΛ hsum hz⟩⟩
  rw [B.chain.a0_flat z, div_self (B.chain.a0_pos 0).ne']

/-- 3'. the numeric a0 of the chain, at every redshift, from DECLARED inputs: c and G as in `A0Numeric`, rho_Lambda(0) =
    3 H0^2 Omega_Lambda/(8 pi G) (flat FRW, canonical footing), H0 in [66.9, 67.9] km/s/Mpc, Omega_Lambda in [0.6774, 0.6920];
    kappa = 1/2 is the FITTED field `hκ_fit`. -/
theorem a0_numeric (hc : B.chain.c = A0Numeric.cSI) (hG : B.chain.G = A0Numeric.GSI) {H0 ΩΛ : ℝ}
    (hρ : B.chain.ρΛ 0 = 3 * (H0 * 1000 / A0Numeric.Mpc) ^ 2 * ΩΛ / (8 * Real.pi * A0Numeric.GSI))
    (hH : 66.9 ≤ H0 ∧ H0 ≤ 67.9) (hΩ : 0.6774 ≤ ΩΛ ∧ ΩΛ ≤ 0.6920) (z : ℝ) :
    9.24e-11 < B.chain.a0 z ∧ B.chain.a0 z < 9.48e-11 := by
  rw [B.a0_flat z, B.a0_eq 0, hc, hG, hρ]
  exact A0Numeric.a0_interval hH hΩ

/-- 4. ARM C: an owned subsystem's internal-to-Newtonian ratio is exactly 1, whatever the external field -/
theorem owned_boost_one {i p : ι} (hp : B.H.parent i = some p) {gN : ℝ} (hgN : 0 < gN) (gext : ℝ) :
    B.accel i gN gext / gN = 1 := by
  rw [B.hown]
  exact Ownership.owned_boost_one B.ν _ B.H hp hgN gext

/-- 4'. ARM C for a population of owned wide binaries: any weighted mean of the per-pair ratio is 1 (gamma-hat = 1.000) -/
theorem gammaHat_one {κ : Type*} (s : Finset κ) (pair : κ → ι) (gN gext w : κ → ℝ)
    (howned : ∀ k ∈ s, ∃ p, B.H.parent (pair k) = some p) (hgN : ∀ k ∈ s, 0 < gN k) (hW : 0 < ∑ k ∈ s, w k) :
    (∑ k ∈ s, w k * (B.accel (pair k) (gN k) (gext k) / gN k)) / ∑ k ∈ s, w k = 1 := by
  simp_rw [B.hown]
  exact Ownership.wideBinary_gammaHat_one B.ν _ B.H s pair gN gext w howned hgN hW

/-- 5. B's kernel merged LOCALLY in the total field is not EFE-free: such a law must show an external-field effect -/
theorem merged_law_has_EFE : ¬ Ownership.EFEFreeRay (fun gN => B.ν (gN / B.chain.a0 0) * gN) :=
  Ownership.law_not_efeFreeRay (B.chain.a0_pos 0) B.ν B.hν_deep

/-- 5, vector form in R^3 -/
theorem merged_vecLaw_has_EFE :
    ¬ Ownership.EFEFree (Ownership.vecLaw (E := EuclideanSpace ℝ (Fin 3)) B.ν (B.chain.a0 0)) :=
  Ownership.vecLaw_R3_not_efeFree (B.chain.a0_pos 0) B.ν B.hν_deep

/-- 5'. B's rule escapes (5) only by being NON-LOCAL: on any hierarchy with a top-level and an owned system, no function of
    the field data alone reproduces B's internal accelerations (B's kernel differs from 1 somewhere, by its deep limit). -/
theorem ownership_nonlocal {i j p : ι} (hi : B.H.parent i = none) (hj : B.H.parent j = some p) :
    ¬ ∃ F : ℝ → ℝ → ℝ, ∀ k g ge, B.accel k g ge = F g ge := by
  obtain ⟨y, hy, hνy⟩ := Ownership.deep_kernel_ne_one B.ν B.hν_deep
  have ha := B.chain.a0_pos 0
  simp_rw [B.hown]
  refine Ownership.ownership_not_field_local B.ν _ B.H hi hj (gN := B.chain.a0 0 * y) (by positivity) ?_
  rwa [mul_div_cancel_left₀ y ha.ne']

/-- the cold budget: (1 - f_b) M_coll = Omega_c/(Omega_b + Omega_c) M_coll -/
theorem cold_budget (Mcoll : ℝ) : (1 - B.Ωb / (B.Ωb + B.Ωc)) * Mcoll = B.Ωc / (B.Ωb + B.Ωc) * Mcoll := by
  have : 0 < B.Ωb + B.Ωc := add_pos B.hΩb B.hΩc
  field_simp
  ring

/-- 6. the cold-mass algebra (C3): dark edge mass = max(M_ph, Omega_c/(Omega_b + Omega_c) M_coll) -/
theorem cold_edge_mass {Mph Mcoll : ℝ} (hMph : 0 ≤ Mph) (hMcoll : 0 < Mcoll) :
    B.darkEdge Mph Mcoll = max Mph (B.Ωc / (B.Ωb + B.Ωc) * Mcoll) := by
  have hs : 0 < B.Ωb + B.Ωc := add_pos B.hΩb B.hΩc
  have hc := B.hΩc
  rw [B.hcold, B.cold_budget]
  exact (C3_conservation Mph _ hMph (by positivity)).2.2

/-- 6'. monotone in the collapse mass (C3) -/
theorem cold_edge_monotone {Mph M₁ M₂ : ℝ} (hMph : 0 ≤ Mph) (h₁ : 0 < M₁) (h₁₂ : M₁ ≤ M₂) :
    B.darkEdge Mph M₁ ≤ B.darkEdge Mph M₂ := by
  have hs : 0 < B.Ωb + B.Ωc := add_pos B.hΩb B.hΩc
  have hc := B.hΩc
  rw [B.hcold, B.hcold, B.cold_budget, B.cold_budget]
  exact C3_max_rule_monotone Mph _ _ hMph (by positivity) (mul_le_mul_of_nonneg_left h₁₂ (by positivity))

/-- THE CHAIN, premises => predictions.  From the fields of `B` (P1 tie with kappa = 1/2 FITTED and rho_Lambda constant as a
    PREMISE; P2 declared kernel; P3 ownership rule POSTULATED; P4 declared cold rule with Omega_c FITTED):
    (1) the BTFR zero point is G M (1/2) c sqrt(G rho_Lambda(0)) at every redshift;
    (2) a0 is the same at every redshift;
    (3) against a0 ∝ H(z) on any flat background: the rival's E(z) is strictly increasing, and for z > 0 B's ratio is 1
        while E(z) > 1;
    (4) every owned subsystem has boost exactly 1, whatever the external field (DR4 Arm C);
    (5) B's kernel merged locally in the total field is not EFE-free (so a local merge must show an EFE);
    (6) the dark edge mass is max(M_ph, Omega_c/(Omega_b + Omega_c) M_coll).
    Lean certifies that these follow from the fields; it certifies none of the fields. -/
theorem predictions :
    (∀ M z : ℝ, 0 < M →
      Tendsto (fun r : ℝ => ((B.chain.G * M / r) * B.ν (B.chain.G * M / (r ^ 2 * B.chain.a0 z))) ^ 2) atTop
        (𝓝 (B.chain.G * M * (1 / 2 * B.chain.c * Real.sqrt (B.chain.G * B.chain.ρΛ 0))))) ∧
    (∀ z, B.chain.a0 z = B.chain.a0 0) ∧
    (∀ Ωm ΩΛ : ℝ, 0 < Ωm → 0 ≤ ΩΛ → Ωm + ΩΛ = 1 →
      StrictMonoOn (Efun Ωm ΩΛ) (Set.Ici 0) ∧
        ∀ z, 0 < z → B.chain.a0 z / B.chain.a0 0 = 1 ∧ 1 < Efun Ωm ΩΛ z) ∧
    (∀ (i p : ι) (gN gext : ℝ), B.H.parent i = some p → 0 < gN → B.accel i gN gext / gN = 1) ∧
    ¬ Ownership.EFEFreeRay (fun gN => B.ν (gN / B.chain.a0 0) * gN) ∧
    (∀ Mph Mcoll : ℝ, 0 ≤ Mph → 0 < Mcoll →
      B.darkEdge Mph Mcoll = max Mph (B.Ωc / (B.Ωb + B.Ωc) * Mcoll)) :=
  ⟨fun _ z hM => B.btfr hM z, B.a0_flat, fun _ _ hm hΛ hs => B.rival_separates hm hΛ hs,
    fun _ _ _ gext hp hgN => B.owned_boost_one hp hgN gext, B.merged_law_has_EFE,
    fun _ _ hMph hMcoll => B.cold_edge_mass hMph hMcoll⟩

/-- NON-VACUITY: the premises are jointly satisfiable.  Witness (unit-free values, NOT a physical fit): kappa = 1/2,
    c = G = rho_Lambda = 1, the kernel nu_mono, two systems with system 1 owned by system 0, Omega_b = Omega_c = 1. -/
theorem nonempty_fin2 : Nonempty (CandidateB (Fin 2)) :=
  ⟨{ chain :=
      { κ := 1 / 2, c := 1, G := 1, ρΛ := fun _ => 1, hκ := by norm_num, hc := one_pos, hG := one_pos,
        hρ := fun _ => one_pos, hflat := fun _ => rfl }
     hκ_fit := rfl
     ν := nuMono
     hν_deep := nuMono_deep
     H := ⟨fun i => if i = 0 then none else some 0⟩
     accel := fun i gN gext =>
       Ownership.internalAccel nuMono (1 / 2 * 1 * Real.sqrt (1 * 1)) ⟨fun i => if i = 0 then none else some 0⟩ i gN gext
     hown := fun _ _ _ => rfl
     Ωb := 1
     Ωc := 1
     hΩb := one_pos
     hΩc := one_pos
     darkEdge := fun Mph Mcoll => Mph + fex Mph ((1 - 1 / (1 + 1)) * Mcoll) * ((1 - 1 / (1 + 1)) * Mcoll)
     hcold := fun _ _ => rfl }⟩

end CandidateB
