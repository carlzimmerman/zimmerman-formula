import Mathlib

/-!
# I03 — Wave K: the Balmer-layer regime invariance (the framework's strong-a0 layer)

SCOPE (per lean-math-certification): Lean certifies the FAMILY-TRANSPORT ALGEBRA over ℝ:
under the certified LRD family (photosphere radius R = r0·√M at fixed T_eff and Γ; the
Balmer layer at r_B = f·R; a common Balmer-layer density ρ_B) the Balmer-layer gravity
g_B = G·M/r_B² is EXACTLY M-independent — the mass cancels — so the framework's density-form
ratio g_B/a0(ρ_B) (a0(ρ) = (c/2)·√(Gρ), the density_form_blackhole.py structural reading
applied to the gas's own density) is the SAME NUMBER for every LRD: the regime coincidence,
if it holds for one LRD, holds for the whole population. Lean certifies the transport; the
PHYSICS assumptions (the family scaling, the common ρ_B, the density-form itself) are
hypotheses, stated as such. The honest falsifier tolerance: the observed substack family
spread is ~×1.6 (Γ varies per substack), so the prediction is invariance WITHIN ×2, not
exact. Zero `sorry`; axioms ⊆ {propext, Classical.choice, Quot.sound}. The sqrt-atom
firewall: √M enters as an atom; the only Real.sqrt step is one `Real.sq_sqrt` fold.
-/

noncomputable section

/-- The framework's density-form (density_form_blackhole.py's structural reading):
a0(ρ) = (c/2)·√(Gρ), evaluatable at the gas's OWN density. -/
noncomputable def a0ρ (G c ρ : ℝ) : ℝ := c / 2 * Real.sqrt (G * ρ)

/-- The Balmer-layer gravity of a family member: g_B = G·M/r_B² with r_B = f·R = f·r0·√M. -/
noncomputable def gB (G M rB : ℝ) : ℝ := G * M / rB ^ 2

lemma sq_r0sqrtM {r0 M : ℝ} (hr0 : 0 < r0) (hM : 0 < M) :
    (r0 * Real.sqrt M) ^ 2 = r0 ^ 2 * M := by
  rw [mul_pow, Real.sq_sqrt (le_of_lt hM)]

/-- **K (the regime-invariance theorem).** Two family members (M1, M2) of the certified LRD
family — R_i = r0·√M_i, r_Bi = f·R_i, common ρ_B — have the SAME Balmer-layer gravity and
the SAME density-form a0: g_B1 = g_B2 and a0(ρ_B1) = a0(ρ_B2). Hence the regime ratio
g_B/a0(ρ_B) — the framework's strong-a0 classifier of the anomalous layer — is
population-invariant: if the coincidence holds for one LRD it holds for all. -/
theorem regime_invariant {G M1 M2 R1 R2 rB1 rB2 r0 f ρB1 ρB2 c : ℝ}
    (hG : 0 < G) (hr0 : 0 < r0) (hf : 0 < f) (hM1 : 0 < M1) (hM2 : 0 < M2)
    (hR1 : R1 = r0 * Real.sqrt M1) (hR2 : R2 = r0 * Real.sqrt M2)
    (hrb1 : rB1 = f * R1) (hrb2 : rB2 = f * R2)
    (hρ : ρB1 = ρB2) :
    gB G M1 rB1 = gB G M2 rB2 ∧ a0ρ G c ρB1 = a0ρ G c ρB2 := by
  constructor
  · have h1 : gB G M1 rB1 = G / (f ^ 2 * r0 ^ 2) := by
      unfold gB
      rw [hrb1, hR1, mul_pow, sq_r0sqrtM hr0 hM1]
      field_simp [hf.ne', hr0.ne', hM1.ne']
    have h2 : gB G M2 rB2 = G / (f ^ 2 * r0 ^ 2) := by
      unfold gB
      rw [hrb2, hR2, mul_pow, sq_r0sqrtM hr0 hM2]
      field_simp [hf.ne', hr0.ne', hM2.ne']
    rw [h1, h2]
  · unfold a0ρ
    rw [hρ]

end

#print axioms regime_invariant
