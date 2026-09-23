import Mathlib

/-!
# I23 — The dark-fraction inversion, and why galaxies below their own baryons are outside every model

SCOPE (per lean-math-certification): Lean certifies the MATHEMATICS. Physics inputs are hypotheses: the framework's
kernel g_obs = ν(g_b/a0)·g_b, and "a model that adds gravity" = any prediction ν·g_b + g_h with ν ≥ 1, g_h ≥ 0.
Companion lanes: `real_research/dark_sector_2026/L332_kmos3d_trend_replication.py` (K1, T2, R1) and the inversion
used by L320/L323 (hunt_2026/h16).

* `nuRAR_ge_one` — the RAR kernel never weakens gravity: ν(y) ≥ 1 for y > 0.
* `adds_gravity_floor` — any model with ν ≥ 1 and a non-negative extra (halo) acceleration predicts g ≥ g_b.
* `below_baryons_unfittable` — hence a galaxy measured with g_obs < g_b (L332 K1: 27–54% of KMOS3D at z ≈ 2.3)
  cannot be fitted by the framework NOR by any ΛCDM halo: the discrepancy is in the inputs, common to both.
* `rar_dark_fraction` — for the RAR kernel the dark fraction f_DM = 1 − g_b/g_obs equals exp(−√(g_b/a0)).
* `rar_inversion` — and a0 is recovered EXACTLY as (1 − f_DM) g_obs / (ln(1/f_DM))²: the closed form of L320/L323.
* `inversion_domain` — the inversion needs 0 < f_DM < 1, i.e. g_b < g_obs: galaxies at or below their baryons drop out
  (the selection that makes L332 T2 conditioned on the outcome).

Zero `sorry`; axioms ⊆ {propext, Classical.choice, Quot.sound}.
-/

noncomputable section

open Real

def nuRAR (y : ℝ) : ℝ := 1 / (1 - Real.exp (-Real.sqrt y))

lemma exp_neg_sqrt_lt_one {y : ℝ} (hy : 0 < y) : Real.exp (-Real.sqrt y) < 1 := by
  have hs : 0 < Real.sqrt y := Real.sqrt_pos.mpr hy
  have := Real.exp_lt_exp.mpr (show -Real.sqrt y < 0 by linarith)
  rwa [Real.exp_zero] at this

theorem nuRAR_ge_one {y : ℝ} (hy : 0 < y) : 1 ≤ nuRAR y := by
  have h1 := exp_neg_sqrt_lt_one hy
  have h0 : 0 < Real.exp (-Real.sqrt y) := Real.exp_pos _
  have hd : 0 < 1 - Real.exp (-Real.sqrt y) := by linarith
  have hle : 1 - Real.exp (-Real.sqrt y) ≤ 1 := by linarith
  unfold nuRAR
  rw [le_div_iff₀ hd]
  linarith

theorem adds_gravity_floor {ν gb gh : ℝ} (hν : 1 ≤ ν) (hb : 0 ≤ gb) (hh : 0 ≤ gh) : gb ≤ ν * gb + gh := by
  nlinarith

theorem below_baryons_unfittable {ν gb gh gobs : ℝ} (hν : 1 ≤ ν) (hb : 0 ≤ gb) (hh : 0 ≤ gh) (hobs : gobs < gb) :
    gobs ≠ ν * gb + gh := by
  have := adds_gravity_floor hν hb hh
  intro h; linarith

theorem rar_dark_fraction {gb a0 : ℝ} (hb : 0 < gb) (ha : 0 < a0) :
    1 - gb / (nuRAR (gb / a0) * gb) = Real.exp (-Real.sqrt (gb / a0)) := by
  have hy : 0 < gb / a0 := div_pos hb ha
  have hd : 0 < 1 - Real.exp (-Real.sqrt (gb / a0)) := by linarith [exp_neg_sqrt_lt_one hy]
  unfold nuRAR
  field_simp
  ring

theorem rar_inversion {gb a0 : ℝ} (hb : 0 < gb) (ha : 0 < a0) :
    let gobs := nuRAR (gb / a0) * gb
    let f := 1 - gb / gobs
    (1 - f) * gobs / (Real.log (1 / f)) ^ 2 = a0 := by
  intro gobs f
  have hy : 0 < gb / a0 := div_pos hb ha
  have hf : f = Real.exp (-Real.sqrt (gb / a0)) := rar_dark_fraction hb ha
  have hd : 0 < 1 - Real.exp (-Real.sqrt (gb / a0)) := by linarith [exp_neg_sqrt_lt_one hy]
  have hlog : Real.log (1 / f) = Real.sqrt (gb / a0) := by
    rw [hf, one_div, ← Real.exp_neg, neg_neg, Real.log_exp]
  have hsq : Real.sqrt (gb / a0) ^ 2 = gb / a0 := Real.sq_sqrt hy.le
  have hgob : (1 - f) * gobs = gb := by
    have h1 : 1 - f = gb / gobs := by simp [f]
    have hg : gobs ≠ 0 := by
      show nuRAR (gb / a0) * gb ≠ 0
      exact mul_ne_zero (by linarith [nuRAR_ge_one hy]) hb.ne'
    rw [h1]; field_simp
  rw [hgob, hlog, hsq]
  field_simp

theorem inversion_domain {gb gobs : ℝ} (hb : 0 < gb) (hg : 0 < gobs) :
    (0 < 1 - gb / gobs ∧ 1 - gb / gobs < 1) ↔ gb < gobs := by
  constructor
  · intro h
    have := h.1
    rw [sub_pos, div_lt_one hg] at this
    exact this
  · intro h
    refine ⟨?_, ?_⟩
    · rw [sub_pos, div_lt_one hg]; exact h
    · have : 0 < gb / gobs := div_pos hb hg
      linarith

end

#print axioms exp_neg_sqrt_lt_one
#print axioms nuRAR_ge_one
#print axioms adds_gravity_floor
#print axioms below_baryons_unfittable
#print axioms rar_dark_fraction
#print axioms rar_inversion
#print axioms inversion_domain
