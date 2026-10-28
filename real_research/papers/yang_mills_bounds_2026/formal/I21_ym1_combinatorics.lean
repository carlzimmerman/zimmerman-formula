import Mathlib

/-!
# I21 — D-YM1 (L326): the combinatorial skeleton of the BDL extension, machine-checked

SCOPE (per lean-math-certification): I19 certified the numeric chain of
`real_research/ym1_bdl_extension_2026/DERIVATION.md`. This file certifies the FINITE COMBINATORIAL facts its
analytic lemmas rest on (the operator-algebra steps themselves remain prose + two adversarial referee passes):

* `sector_structure` (Claim 3′(ii)) — N∖p ⊆ M ⊆ N ∪ p ⟹ M = (N∖p) ∪ (M ∩ p): every surviving output sector is
  the fixed off-plaquette part plus a subset of the plaquette.
* `sector_count` — hence at most 2^|p| sectors (16 for a plaquette, s = 4; BDL's two-body "at most four").
* `disjoint_hits_le` (the depth pigeonhole, Lemma 2′) — k pairwise-disjoint sets that each meet p number at most
  |p|: at most s creation operators can act on one side of V_p, so nested commutators vanish beyond depth 2s.
* `Mj_card_le` — M_j ⊆ M ∪ p, |p| ≤ s, M ≠ ∅ ⟹ |M_j| ≤ (s+1)|M| (the corrected App. A bound; 3|M| for BDL's
  two-body case), and `Mj_bound_sharp_two_body` — the two-body bound 3|M| is attained (|M| = 1, |M_j| = 3), so
  BDL's printed 2|M| is false as a combinatorial statement.
* `bdl_counterexample` — the explicit 3-qubit matrix element ⟨Ω| a_u [a†_{uvw}, X_v X_w] |Ω⟩ = −1 ≠ 0, the term
  BDL's |M_j| ≤ 2|M| step would exclude (computed on explicit 8×8 integer matrices).

Zero `sorry`; axioms ⊆ {propext, Classical.choice, Quot.sound}.
-/

open Finset

variable {α : Type*} [DecidableEq α]

theorem sector_structure {N M p : Finset α} (h1 : N \ p ⊆ M) (h2 : M ⊆ N ∪ p) :
    M = (N \ p) ∪ (M ∩ p) := by
  ext x
  simp only [mem_union, mem_sdiff, mem_inter]
  constructor
  · intro hx
    by_cases hp : x ∈ p
    · exact Or.inr ⟨hx, hp⟩
    · have := h2 hx
      simp only [mem_union] at this
      rcases this with hN | hp'
      · exact Or.inl ⟨hN, hp⟩
      · exact absurd hp' hp
  · rintro (⟨hN, hp⟩ | ⟨hM, _⟩)
    · exact h1 (mem_sdiff.mpr ⟨hN, hp⟩)
    · exact hM

/-- At most 2^|p| sectors: M ↦ M ∩ p is injective on the admissible family. -/
theorem sector_count (N p : Finset α) (F : Finset (Finset α))
    (hF : ∀ M ∈ F, N \ p ⊆ M ∧ M ⊆ N ∪ p) : F.card ≤ 2 ^ p.card := by
  have hinj : Set.InjOn (fun M => M ∩ p) (F : Set (Finset α)) := by
    intro M1 hM1 M2 hM2 heq
    have e1 := sector_structure (hF M1 hM1).1 (hF M1 hM1).2
    have e2 := sector_structure (hF M2 hM2).1 (hF M2 hM2).2
    simp only at heq
    rw [e1, e2, heq]
  calc F.card = (F.image (fun M => M ∩ p)).card := (card_image_of_injOn hinj).symm
    _ ≤ p.powerset.card := by
        apply card_le_card
        intro T hT
        simp only [mem_image] at hT
        obtain ⟨M, _, rfl⟩ := hT
        exact mem_powerset.mpr inter_subset_right
    _ = 2 ^ p.card := card_powerset p

/-- The depth pigeonhole: pairwise-disjoint sets that each meet p number at most |p|. -/
theorem disjoint_hits_le {k : ℕ} (p : Finset α) (f : Fin k → Finset α)
    (hdisj : ∀ i j, i ≠ j → Disjoint (f i) (f j)) (hmeet : ∀ i, (f i ∩ p).Nonempty) :
    k ≤ p.card := by
  classical
  choose g hg using hmeet
  have hgp : ∀ i, g i ∈ p := fun i => (mem_inter.mp (hg i)).2
  have hgf : ∀ i, g i ∈ f i := fun i => (mem_inter.mp (hg i)).1
  have hinj : Function.Injective g := by
    intro i j hij
    by_contra hne
    exact (Finset.disjoint_left.mp (hdisj i j hne)) (hgf i) (hij ▸ hgf j)
  calc k = (Finset.univ.image g).card := by
          rw [card_image_of_injective _ hinj, card_univ, Fintype.card_fin]
    _ ≤ p.card := card_le_card (by intro x hx; simp only [mem_image] at hx; obtain ⟨i, _, rfl⟩ := hx; exact hgp i)

/-- The corrected App. A bound: |M_j| ≤ (s+1)|M|. -/
theorem Mj_card_le {M Mj p : Finset α} {s : ℕ} (hsub : Mj ⊆ M ∪ p) (hp : p.card ≤ s)
    (hM : M.Nonempty) : Mj.card ≤ (s + 1) * M.card := by
  have h1 : Mj.card ≤ M.card + p.card := (card_le_card hsub).trans (card_union_le M p)
  have h2 : 1 ≤ M.card := hM.card_pos
  nlinarith

/-- Two-body sharpness: |M| = 1, |p| = 2, M_j ⊆ M ∪ p with |M_j| = 3 = 3|M| > 2|M|. -/
theorem Mj_bound_sharp_two_body :
    ∃ M Mj p : Finset ℕ, Mj ⊆ M ∪ p ∧ p.card = 2 ∧ M.card = 1 ∧ Mj.card = 3 ∧ 2 * M.card < Mj.card := by
  refine ⟨{0}, {0, 1, 2}, {1, 2}, ?_, ?_, ?_, ?_, ?_⟩ <;> decide

/-! ### The explicit counterexample on three qubits (u, v, w) ↔ bits (4, 2, 1) of Fin 8. -/

/-- a†_{uvw} = |111⟩⟨000|. -/
def aDag_uvw : Matrix (Fin 8) (Fin 8) ℤ := fun i j => if i = 7 ∧ j = 0 then 1 else 0
/-- X_v X_w flips bits 2 and 1: |i⟩ ↦ |i xor 3⟩. -/
def XvXw : Matrix (Fin 8) (Fin 8) ℤ := fun i j => if i.val = j.val ^^^ 3 then 1 else 0
/-- a_u = |0⟩⟨1| on u: |1vw⟩ ↦ |0vw⟩. -/
def a_u : Matrix (Fin 8) (Fin 8) ℤ := fun i j => if j.val = i.val + 4 ∧ i.val < 4 then 1 else 0

/-- ⟨Ω| a_u [a†_{uvw}, X_v X_w] |Ω⟩ = −1: a nonzero term with |M| = 1, |M_j| = 3. -/
theorem bdl_counterexample : (a_u * (aDag_uvw * XvXw - XvXw * aDag_uvw)) 0 0 = -1 := by
  decide

#print axioms sector_structure
#print axioms sector_count
#print axioms disjoint_hits_le
#print axioms Mj_card_le
#print axioms Mj_bound_sharp_two_body
#print axioms bdl_counterexample
