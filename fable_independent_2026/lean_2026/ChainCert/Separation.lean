import Mathlib

/-!
# ChainCert.Separation -- the significance algebra of CFG63's discrimination forecast

CFG63 (campaign_fresh_gravity/CFG63_discrimination_forecast/forecast.py, frozen question item 1) separates two readings that differ
by `Δ` with a statistical variance `v/N` and a systematic floor `f` that does not shrink with `N`:

    S(N) = Δ / sqrt(v/N + f^2),      N(k) = v / ((Δ/k)^2 - f^2),      cap = Δ/f.

Certified here (premises => conclusions; every hypothesis is stated):
* `S` is strictly increasing in `N` (`sep_strictMono`);
* `S(N) < Δ/f` for every `N > 0` when `f > 0` (`sep_lt_cap`), and `S(N) -> Δ/f` as `N -> infinity` (`sep_tendsto_cap`);
* if `f < Δ/k`, then `N(k)` is the sample size that reaches `k` sigma exactly (`sep_solve`), and it is the ONLY one
  (`sep_solve_unique`), so `N(k)` is the inverse the script reports;
* if `Δ/k <= f`, NO sample size reaches `k` sigma (`sep_no_solution`): the cap is below `k`;
* with no floor, `N(k) = v k^2 / Δ^2` (`sep_zero_floor`), which is why the MUTATE run (all floors set to zero) changes the
  capped headline.
NOT certified: any of the committed numbers (`Δ`, `v`, `f`, the citations); the significance model itself is CFG63's declaration.
-/

noncomputable def sepSig (Δ v f N : ℝ) : ℝ := Δ / Real.sqrt (v / N + f ^ 2)
noncomputable def sepN (Δ v f k : ℝ) : ℝ := v / ((Δ / k) ^ 2 - f ^ 2)

theorem sep_strictMono {Δ v f N₁ N₂ : ℝ} (hΔ : 0 < Δ) (hv : 0 < v) (h1 : 0 < N₁) (h12 : N₁ < N₂) :
    sepSig Δ v f N₁ < sepSig Δ v f N₂ := by
  unfold sepSig
  have h2 : 0 < N₂ := lt_trans h1 h12
  have hlt : v / N₂ < v / N₁ := div_lt_div_of_pos_left hv h1 h12
  have hpos2 : 0 < v / N₂ + f ^ 2 := by positivity
  have hs : Real.sqrt (v / N₂ + f ^ 2) < Real.sqrt (v / N₁ + f ^ 2) :=
    Real.sqrt_lt_sqrt hpos2.le (by linarith)
  have hs2 : 0 < Real.sqrt (v / N₂ + f ^ 2) := Real.sqrt_pos.mpr hpos2
  exact div_lt_div_of_pos_left hΔ hs2 hs

theorem sep_lt_cap {Δ v f N : ℝ} (hΔ : 0 < Δ) (hv : 0 < v) (hf : 0 < f) (hN : 0 < N) :
    sepSig Δ v f N < Δ / f := by
  unfold sepSig
  have hpos : 0 < v / N := by positivity
  have hs : f < Real.sqrt (v / N + f ^ 2) := by
    have : Real.sqrt (f ^ 2) < Real.sqrt (v / N + f ^ 2) :=
      Real.sqrt_lt_sqrt (by positivity) (by linarith)
    rwa [Real.sqrt_sq hf.le] at this
  exact div_lt_div_of_pos_left hΔ hf hs

theorem sep_tendsto_cap {Δ v f : ℝ} (hf : 0 < f) :
    Filter.Tendsto (fun N : ℝ => sepSig Δ v f N) Filter.atTop (nhds (Δ / f)) := by
  unfold sepSig
  have h0 : Filter.Tendsto (fun N : ℝ => v / N) Filter.atTop (nhds 0) := tendsto_const_nhds.div_atTop Filter.tendsto_id
  have h1 : Filter.Tendsto (fun N : ℝ => v / N + f ^ 2) Filter.atTop (nhds (0 + f ^ 2)) := h0.add_const _
  have h2 := (Real.continuous_sqrt.tendsto (0 + f ^ 2)).comp h1
  have hsq : Real.sqrt (0 + f ^ 2) = f := by rw [zero_add, Real.sqrt_sq hf.le]
  rw [hsq] at h2
  exact tendsto_const_nhds.div h2 hf.ne'

theorem sep_solve {Δ v f k : ℝ} (hΔ : 0 < Δ) (hv : 0 < v) (hk : 0 < k) (hf0 : 0 ≤ f) (hf : f < Δ / k) :
    sepSig Δ v f (sepN Δ v f k) = k := by
  have hq : 0 < Δ / k := div_pos hΔ hk
  have hD : 0 < (Δ / k) ^ 2 - f ^ 2 := by nlinarith
  have hN : v / sepN Δ v f k = (Δ / k) ^ 2 - f ^ 2 := by
    unfold sepN; field_simp
  unfold sepSig
  rw [hN]
  have : (Δ / k) ^ 2 - f ^ 2 + f ^ 2 = (Δ / k) ^ 2 := by ring
  rw [this, Real.sqrt_sq hq.le]
  field_simp

theorem sep_solve_unique {Δ v f k N : ℝ} (hΔ : 0 < Δ) (hv : 0 < v) (hk : 0 < k) (hf0 : 0 ≤ f) (hN : 0 < N)
    (h : sepSig Δ v f N = k) : f < Δ / k ∧ N = sepN Δ v f k := by
  unfold sepSig at h
  have hpos : 0 < v / N + f ^ 2 := by positivity
  have hs : 0 < Real.sqrt (v / N + f ^ 2) := Real.sqrt_pos.mpr hpos
  have hsq : Real.sqrt (v / N + f ^ 2) = Δ / k := by
    field_simp at h ⊢
    linarith
  have hq : 0 < Δ / k := div_pos hΔ hk
  have hsq2 : v / N + f ^ 2 = (Δ / k) ^ 2 := by
    have := Real.sq_sqrt hpos.le
    rw [hsq] at this
    linarith
  have hvN : 0 < v / N := by positivity
  refine ⟨?_, ?_⟩
  · nlinarith
  · unfold sepN
    have hD : (Δ / k) ^ 2 - f ^ 2 = v / N := by linarith
    rw [hD]
    field_simp

theorem sep_no_solution {Δ v f k N : ℝ} (hΔ : 0 < Δ) (hv : 0 < v) (hk : 0 < k) (hf : 0 < f) (hN : 0 < N)
    (hcap : Δ / k ≤ f) : sepSig Δ v f N < k := by
  have h1 := sep_lt_cap hΔ hv hf hN
  have h2 : Δ / f ≤ k := by
    rw [div_le_iff₀ hf]
    have := (div_le_iff₀ hk).mp hcap
    nlinarith
  linarith

theorem sep_zero_floor {Δ v k : ℝ} (hΔ : Δ ≠ 0) (hk : k ≠ 0) :
    sepN Δ v 0 k = v * k ^ 2 / Δ ^ 2 := by
  unfold sepN
  field_simp
  ring
