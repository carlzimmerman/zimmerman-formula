import Mathlib

/- SW12_dr4_disjoint.lean -- the DR4 separation, as interval algebra with the frozen
   band endpoints as hypotheses (all endpoints from landed artifacts:
   SW04_conformal_efe.out D, kappa_slot_2026/SW07_program_ledger.out, Amendment 10).
   Algebra only; no sorry. The corner lemma encodes SW07 R2's "footing must be fixed
   first": the minimum cross-footing margin (0.0064) is positive but below the
   registered band width (0.02). -/

/-- Any measured gamma_v in the class bin excludes the cap/L268 law. -/
theorem class_below_cap (g : ℝ) (hg : 1.0000 ≤ g ∧ g ≤ 1.01012) :
    g < 1.086 := by linarith

/-- The class-candidate UNION is disjoint from cap/L268: the candidate's registered
    ceiling (1.045) sits below the cap band's floor. -/
theorem candidate_ceiling_below_cap (g : ℝ) (hg : g ≤ 1.045) :
    g < 1.086 := by linarith

/-- Same-footing separation (alt): the cap band's top and AQUAL's alt floor are
    separated by 0.0367 — more than the Amendment-10 band width, distinguishable
    without the footing fix. -/
theorem alt_foot_separated (g : ℝ) (hg : g ≤ 1.155) :
    0.0367 ≤ 1.1917 - g := by linarith

/-- The cross-footing corner: cap vs AQUAL-canonical minimum margin is 0.0064 —
    positive (disjoint) but below the registered band width 0.02, so cap-law and
    AQUAL can be told apart ONLY after the footing is fixed (SW07 R2). -/
theorem corner_gap_forces_footing_first (g : ℝ) (hg : 1.086 ≤ g ∧ g ≤ 1.155)
    (a : ℝ) (ha : 1.1614 ≤ a ∧ a ≤ 1.2267) :
    0.0064 ≤ a - g ∧ 0 < a - g := by
  refine ⟨by linarith [hg.1, hg.2, ha.1, ha.2], by linarith [hg.1, hg.2, ha.1, ha.2]⟩
