/-
  TemporalSeparation.lean

  Propositions extracted from the temporal-separation investigation (scripts T1/T2/T3 in this directory).
  These are the statements worth formalising: each is finite arithmetic on measured constants plus at most
  one monotonicity or calculus argument, so none of them needs a physics library.

  SCOPE NOTE, stated in the file because it matters: this file has NOT been compiled.  It is a skeleton --
  the statements are the deliverable, the proofs are sketched or `sorry`d.  The measured constants are
  carried as hypotheses so that the theorems say exactly what the numerics established and nothing more.

  THE SETTING.  A MOND theory fits galaxy rotation curves with its kernel alone but fails the CMB third peak,
  which needs a clustering ~a^-3 gravitating component.  A hybrid is blocked by the VELOCITY-ORDERING LEMMA.
  The escape under test: let the component be COLD AND PRESENT at recombination but GONE by galaxy-formation
  time -- temporal rather than scale separation.
-/

namespace TemporalSeparation

open scoped Real

/-! ## Measured constants (from the committed lanes; carried as hypotheses, never as axioms) -/

/-- The transmitted-pull ceiling of L61 / L49 / L50: the largest fraction of the CMB-required cold density a
    galaxy may still contain before the rotation-curve fit is degraded past the RAR's own scatter.
    Measured: 0.582 (canonical a0, kernel reading the baryons only) down to 0.276 (alternate a0, kernel
    reading the total potential). -/
structure GalaxyCeiling where
  etaMax : ℝ
  pos    : 0 < etaMax
  lt_one : etaMax < 1

/-- The cluster requirement, derived in T3 from 248 audited X-COP rows as
    f_req(r) = (g_HSE(r) - g_MOND(r)) / ((Ω_c/Ω_b) · g_bar(r)).
    Measured at 1 Mpc: 0.606 ± 0.036 (canonical, zero hydrostatic bias) rising to 1.246 ± 0.052
    (canonical, b = 0.33). -/
structure ClusterRequirement where
  fReq : ℝ
  pos  : 0 < fReq

/-! ## P1 — the isotropic-removal pincer

  Any mechanism that removes the component WITHOUT a position- or velocity-dependent filter (decay to dark
  radiation, conversion, a dark-sector phase transition, annihilation to radiation) leaves ONE surviving
  fraction `f`.  The galaxy ceiling and the cluster requirement then bracket that single number, so the
  admissible set is a single interval — and no lifetime can widen it, because both statements are made at
  the SAME epoch.  Measured, the interval is empty at 8 of 8 (footing × hydrostatic-bias) combinations on
  the mean, and 7 of 8 on the median.  -/

theorem isotropic_removal_empty
    (G : GalaxyCeiling) (C : ClusterRequirement)
    (f : ℝ) (hgal : f ≤ G.etaMax) (hcl : C.fReq ≤ f)
    (hsep : G.etaMax < C.fReq) : False := by
  exact absurd (le_trans hcl hgal) (not_le.mpr hsep)

/-- The same content stated positively: the admissible set is exactly `Set.Icc fReq etaMax`. -/
theorem isotropic_removal_admissible (G : GalaxyCeiling) (C : ClusterRequirement) :
    {f : ℝ | C.fReq ≤ f ∧ f ≤ G.etaMax} = Set.Icc C.fReq G.etaMax := by
  ext f; simp [Set.mem_Icc]

/-! ## P2 — no lifetime helps

  With a decaying fraction `fdec` and lifetime `τ`, the surviving fraction is
  `f t = (1 - fdec) + fdec · exp (-t/τ)`.  This is bounded below by `1 - fdec` for every `τ > 0` and every
  `t ≥ 0`.  Hence the galaxy ceiling forces `fdec ≥ 1 - etaMax` INDEPENDENTLY of the lifetime — which is the
  step that makes "at least 41.8%, and up to 72.4%, of the dark matter must be destroyed" a lifetime-free
  statement, and therefore the step that makes a background cost unavoidable. -/

noncomputable def survivingFraction (fdec τ t : ℝ) : ℝ :=
  (1 - fdec) + fdec * Real.exp (-t / τ)

theorem decay_floor (fdec τ t : ℝ) (hf : 0 ≤ fdec) (hτ : 0 < τ) (ht : 0 ≤ t) :
    1 - fdec ≤ survivingFraction fdec τ t := by
  have : 0 ≤ fdec * Real.exp (-t / τ) := mul_nonneg hf (Real.exp_pos _).le
  simpa [survivingFraction] using le_add_of_nonneg_right this

theorem decay_fraction_forced
    (G : GalaxyCeiling) (fdec τ t : ℝ) (hf : 0 ≤ fdec) (hτ : 0 < τ) (ht : 0 ≤ t)
    (hgal : survivingFraction fdec τ t ≤ G.etaMax) : 1 - G.etaMax ≤ fdec := by
  have h := decay_floor fdec τ t hf hτ ht
  linarith [le_trans h hgal]

/-! ## P3 — the cooling floor

  For a two-body decay with kick `v_k`, a daughter born at scale factor `a_d` has present speed `v_k · a_d`,
  so it is retained by a halo of escape velocity `v_esc` exactly when it was born before
  `t_x = t(min 1 (v_esc / v_k))`.  The bound fraction is therefore

      fBound τ = exp (-t₀/τ) + (1 - exp (-t_x/τ)).

  This tends to 1 both as `τ → 0` (everything has decayed, and the early daughters have cooled back in) and
  as `τ → ∞` (nothing has decayed).  So the galaxy gate has an INTERIOR optimum in `τ` and a strictly
  positive floor for every finite kick.  This is the velocity-ordering lemma REASSERTING ITSELF inside the
  daughter population — the reason a short lifetime does not clear a galaxy. -/

noncomputable def fBound (t₀ tx τ : ℝ) : ℝ :=
  Real.exp (-t₀ / τ) + (1 - Real.exp (-tx / τ))

theorem fBound_pos (t₀ tx τ : ℝ) (hτ : 0 < τ) (h : tx ≤ t₀) : 0 < fBound t₀ tx τ := by
  sorry  -- exp is decreasing in its (negative) argument; tx ≤ t₀ gives exp(-t₀/τ) ≤ exp(-tx/τ)

theorem fBound_tendsto_one_atTop (t₀ tx : ℝ) :
    Filter.Tendsto (fBound t₀ tx) Filter.atTop (nhds 1) := by
  sorry  -- both exponentials → 1

theorem fBound_tendsto_one_atZero (t₀ tx : ℝ) (h₀ : 0 < tx) :
    Filter.Tendsto (fBound t₀ tx) (nhdsWithin 0 (Set.Ioi 0)) (nhds 1) := by
  sorry  -- exp(-t₀/τ) → 0 and exp(-tx/τ) → 0

/-- The stationary point of `fBound` in `1/τ`: `u = ln (t₀/tx) / (t₀ - tx)`.  The floor is the value there. -/
theorem cooling_floor_stationary (t₀ tx : ℝ) (h : 0 < tx) (h2 : tx < t₀) :
    ∃ u > 0, u = Real.log (t₀ / tx) / (t₀ - tx) := by
  refine ⟨Real.log (t₀ / tx) / (t₀ - tx), ?_, rfl⟩
  sorry  -- log (t₀/tx) > 0 since t₀ > tx > 0, and t₀ - tx > 0

/-! ## P4 — one velocity, two jobs  (THE GENERALISATION OF THE VELOCITY-ORDERING LEMMA)

  This is the proposition the investigation actually establishes, and the one worth putting in a paper.

  The original lemma (L125 VEL-1/VEL-2) assumed a single decoupled species carrying `v_rms ∝ 1/a` from the
  start, so that its free-streaming cutoff `k_fs ∝ a` increases monotonically.  A late, non-adiabatic
  velocity injection BREAKS that hypothesis — and the escape genuinely exploits it.  What survives is
  weaker in hypothesis and stronger in reach:

  Retention by a halo of escape velocity `v` is the predicate `v_k · a_d < v`.  The comoving free-streaming
  cutoff is `k_fs a = sqrt(3/2) · a² · H a / (v_k · a_d)`.  BOTH are monotone DECREASING in `v_k`.  Hence
  "evacuate a deeper halo" and "erase less power" are opposite requirements on the SAME number, with no
  parameter separating them.  Temporal separation moves WHEN the velocity appears; it cannot decouple the
  scale it evacuates from the scale it erases. -/

noncomputable def kFreeStream (v_k a_d a H : ℝ) : ℝ :=
  Real.sqrt (3 / 2) * a ^ 2 * H / (v_k * a_d)

def retained (v_k a_d vEsc : ℝ) : Prop := v_k * a_d < vEsc

theorem kfs_antitone (a_d a H : ℝ) (ha : 0 < a) (hH : 0 < H) (had : 0 < a_d)
    {v₁ v₂ : ℝ} (h₁ : 0 < v₁) (h : v₁ < v₂) :
    kFreeStream v₂ a_d a H < kFreeStream v₁ a_d a H := by
  sorry  -- strict antitonicity of `x ↦ c / x` on the positives, c > 0

theorem retained_antitone (a_d vEsc : ℝ) (had : 0 < a_d) {v₁ v₂ : ℝ} (h : v₁ < v₂) :
    retained v₂ a_d vEsc → retained v₁ a_d vEsc := by
  intro h₂
  exact lt_of_le_of_lt (by nlinarith) h₂

/-- The incompatibility, stated order-theoretically.  Increasing the kick to unbind a galaxy strictly lowers
    the free-streaming cutoff, i.e. strictly reduces the power surviving at every fixed `k` above it.  There
    is no `v_k` that improves both.  The physics enters ONLY as the two monotonicity facts above; the
    conflict is then order theory, not a fit. -/
theorem one_velocity_two_jobs (a_d a H vEsc : ℝ) (ha : 0 < a) (hH : 0 < H) (had : 0 < a_d)
    {v₁ v₂ : ℝ} (h₁ : 0 < v₁) (h : v₁ < v₂) :
    kFreeStream v₂ a_d a H < kFreeStream v₁ a_d a H ∧
      (retained v₂ a_d vEsc → retained v₁ a_d vEsc) :=
  ⟨kfs_antitone a_d a H ha hH had h₁ h, retained_antitone a_d vEsc had h⟩

/-! ## P5 — annihilation is strictly worse than decay

  If the removal rate goes as `ρ^n` with `n ≥ 2` rather than `n = 1`, the removal is FRONT-LOADED into the
  high-density epoch — which is exactly recombination, where the third peak needs the component intact.  So
  at fixed z = 0 survival, an `n ≥ 2` channel removes strictly more before recombination than a decay does,
  and the third-peak constraint is strictly tighter.  Annihilation is therefore not an escape from the
  decay bounds; it is the same bound, worse. -/

theorem front_loading (ρ : ℝ → ℝ) (hmono : ∀ s t, s ≤ t → ρ t ≤ ρ s) (hpos : ∀ t, 0 < ρ t)
    (n : ℕ) (hn : 2 ≤ n) (t₁ t₂ : ℝ) (h : t₁ ≤ t₂) :
    ρ t₂ ^ (n - 1) ≤ ρ t₁ ^ (n - 1) := by
  sorry  -- pow_le_pow_left on a decreasing positive function

/-! ## What these propositions do NOT cover — recorded deliberately

  * A mechanism that changes how the component GRAVITATES rather than whether it is present (P1/P2) or how
    fast it moves (P3/P4): a late-time change of its coupling to the metric, or a screening that switches on
    after recombination.  That evades all five propositions and is a genuinely different door.
  * Everything quantitative: the constants `etaMax` and `fReq` are hypotheses here, established numerically
    in T1/T2/T3 against SPARC, the audited X-COP rows, Planck 2018, BOSS/eBOSS BAO and Pantheon+.  Nothing
    in this file re-derives them, and nothing in this file should be quoted as if it did.
-/

end TemporalSeparation
