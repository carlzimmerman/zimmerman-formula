import Mathlib

/-!
# ChainCert.Exchange -- the exact algebra of CFG72's Gauss-law scalar mediator (D1-D6 of `cfg72_lightcone_exchange.py`)

CFG72 (campaign_fresh_gravity/CFG72_lightcone_exchange) adds a local 1+1 scalar mediator `phi` (Gauss law: `E = -d_r phi`
sourced by the enclosed baryon mass) to CFG70's exchange, with two dimensionless couplings the action leaves free:
`lam_t = vt/(g_b M)` and `beta = c_f vt^2/N`.  Certified here (premises => conclusions; every hypothesis is written out):

* Characteristic speed (D5).  `beta = c_f vt^2/N > 0` for `c_f, N > 0`, `vt != 0` (`exch_beta_pos`); then `sqrt(1+beta) > 1`
  (`exch_speed_gt_one`); the coupled speed `c_m sqrt(1+beta)` equals `c` iff `c_m = c/sqrt(1+beta)` (`exch_speed_eq_iff`), and that
  bare speed is `< c` (`exch_bare_speed_lt`).  The characteristic polynomial of the declared principal-symbol matrix is
  `lam (lam^2 - c_m^2 (1+beta))` (`exch_symbol_charpoly`); its roots are exactly `0, +-c_m sqrt(1+beta)`, pairwise distinct
  for `c_m > 0`, `beta > -1` (`exch_symbol_eigen_iff`, `exch_symbol_roots_distinct`).
* Static structure (D3).  From the static fluid equation `eps = -r_led/c_f`, `S = c_f vt eps`, `E = (g_b M + S)/N`,
  `theta = eps + vt E`, `vartheta = vt g_b/N`: `theta = vartheta M - (1+beta) r_led/c_f` (`exch_static_theta`);
  the probe force `F = -g_b E` gives `F/vartheta = r_led - 1/lam_t` (`exch_static_reaction`), which is `(delta - 1)/lam_t`
  (`exch_reaction_via_delta`), never equal to `r_led` (`exch_reaction_ne_rled`), and negative when `0 < lam_t`, `delta < 1`
  (`exch_reaction_neg_of_delta_lt_one`).  With `delta = lam_t r_led` and `f_bb = (vartheta M/(vt/g_b))/(vartheta r_led)`:
  `f_bb = 1/(lam_t r_led)` and `delta f_bb = 1` (`exch_static_delta_fbb`, `exch_delta_mul_fbb`).
* The trade-off (state precisely).  Given `delta f = 1` with `delta, f > 0`: `delta < 1 => f > 1` (`exch_fbb_gt_one`);
  `delta <= eps => f >= 1/eps` (`exch_fbb_large`); and no pair of bounds `delta <= a`, `f <= b` with `a b < 1` can hold
  (`exch_not_both_small`).  The identity needs `lam_t r_led != 0`: in the open class `r_led = 0` one has `delta = 0`
  and `f_bb` is not defined (`exch_open_delta_zero`); Lean's `1/0 = 0` is NOT used to cover this case.
* `eps_c` tie.  With `eps_c = c_f vartheta M` (= `c_f theta^T_full`) and `lam_t = vt/(g_b M)`: `beta = eps_c lam_t`
  (`exch_beta_eq_epsc_lamt`); the delivered-heat fraction `f_real = 1 - (1+beta) r_led/eps_c` equals `1 - r_led/eps_c - delta`
  (`exch_freal_split`), equals `1` for the open class, and is `< 1` when `r_led, eps_c > 0`, `1+beta > 0` (`exch_freal_open`,
  `exch_freal_lt_one`).
* Retardation algebra (D4, value level).  With `E = E_qs + w`, `N E_qs = g_b M + S` (so its second derivatives satisfy the
  same linear relation), the wave equation `N(E_tt/c^2 - E_rr) = -g_b M_rr - S_rr` holds iff
  `N(w_tt/c^2 - w_rr) = -(g_b M_tt + S_tt)/c^2` (`exch_retardation_iff`).  The derivatives are taken as given real numbers.
* sigma-slaved reaction (D6).  `sigmaReact a0 g = (3/8) a0 (2g + a0)/(g + a0)` is TRUE strictly increasing in `g` on `g > -a0`
  (`exch_sigma_strictMono`), lies strictly between `(3/8) a0` and `(3/4) a0` for `g > 0` (`exch_sigma_bounds`), reduces to
  G4's `(3/8) a0 (2 + x^2)/(1 + x^2)` at `g = a0/x^2` (`exch_sigma_pointmass`), and hence is strictly DEcreasing in `x` on `x > 0`
  (`exch_sigma_pointmass_strictAnti`).  The hydrostatic shell reading: `int_0^u r^2/u^2 dr = u/3` (`exch_shell_integral`),
  the shell energy `(3/4) a0 dm ((R - u) + u/3)` has `-dE/du/dm = a0/2` (`exch_hyd_reaction`), `= (2/3)(3/4) a0`.

NOT certified (deliberately):
* the doubled Schwinger-Keldysh ACTION and the derivation of its Euler-Lagrange equations (D1, D2: sympy in the script), the
  discrete light-cone lattice checks (S2), reciprocity, causality of the discrete kernel;
* every numerical result: the wave+fluid+probe simulations (Q1), the extended-baryon table (Q2), and above all the STABILITY
  result (Q3: growing modes under the declared shell-gas operator) -- nothing here says the operator is stable or unstable;
* that `lam_t`, `beta` (and `vt`, `c_f`, `N`, `g_b`) are tied to anything: they are FREE couplings of the completion (the trade-off
  `delta f_bb = 1` is a statement about this completion at any values of them, not a statement about which values occur);
* the "second-order retardation" implication of D4: CFG72 records it as WRONG for boundary-driven sources; only the algebra
  is certified here;
* the identification `theta^T = vartheta M`, the target law of CFG10/CFG44, the P1/P2/P3/P4 verdicts, and any claim that the
  theory is closed.  kappa = 1/2 is FITTED.
-/

/-! ## Characteristic speed (D5) -/

theorem exch_beta_pos {cf vt N : ℝ} (hcf : 0 < cf) (hvt : vt ≠ 0) (hN : 0 < N) :
    0 < cf * vt ^ 2 / N := by positivity

theorem exch_speed_gt_one {β : ℝ} (hβ : 0 < β) : 1 < Real.sqrt (1 + β) := by
  rw [Real.lt_sqrt (by norm_num)]
  nlinarith

theorem exch_speed_eq_iff {c cm β : ℝ} (hβ : 0 < β) :
    cm * Real.sqrt (1 + β) = c ↔ cm = c / Real.sqrt (1 + β) := by
  have hs : 0 < Real.sqrt (1 + β) := Real.sqrt_pos.mpr (by linarith)
  exact (eq_div_iff hs.ne').symm

theorem exch_bare_speed_lt {c β : ℝ} (hc : 0 < c) (hβ : 0 < β) :
    c / Real.sqrt (1 + β) < c :=
  div_lt_self hc (exch_speed_gt_one hβ)

/-- the declared principal-symbol matrix (variables `(e, p, y)`) of the mediator sector -/
def exchSymbol (cm β : ℝ) : Matrix (Fin 3) (Fin 3) ℝ :=
  !![0, -1, 0; -cm ^ 2 * (1 + β), 0, cm ^ 2 * β; 0, 0, 0]

theorem exch_symbol_charpoly (cm β lam : ℝ) :
    (lam • (1 : Matrix (Fin 3) (Fin 3) ℝ) - exchSymbol cm β).det
      = lam * (lam ^ 2 - cm ^ 2 * (1 + β)) := by
  simp [exchSymbol, Matrix.det_fin_three]
  ring

theorem exch_symbol_eigen_iff {cm β : ℝ} (hβ : -1 < β) (lam : ℝ) :
    (lam • (1 : Matrix (Fin 3) (Fin 3) ℝ) - exchSymbol cm β).det = 0 ↔
      lam = 0 ∨ lam = cm * Real.sqrt (1 + β) ∨ lam = -(cm * Real.sqrt (1 + β)) := by
  rw [exch_symbol_charpoly]
  have hsq : (cm * Real.sqrt (1 + β)) ^ 2 = cm ^ 2 * (1 + β) := by
    rw [mul_pow, Real.sq_sqrt (by linarith)]
  constructor
  · intro h
    rcases mul_eq_zero.mp h with h0 | h1
    · exact Or.inl h0
    · right
      have : lam ^ 2 = (cm * Real.sqrt (1 + β)) ^ 2 := by rw [hsq]; linarith
      exact sq_eq_sq_iff_eq_or_eq_neg.mp this
  · rintro (h | h | h)
    · rw [h]; ring
    · rw [h, mul_pow, Real.sq_sqrt (by linarith)]; ring
    · rw [h, neg_sq, mul_pow, Real.sq_sqrt (by linarith)]; ring

theorem exch_symbol_roots_distinct {cm β : ℝ} (hcm : 0 < cm) (hβ : -1 < β) :
    0 < cm * Real.sqrt (1 + β) ∧ -(cm * Real.sqrt (1 + β)) < 0 ∧
      -(cm * Real.sqrt (1 + β)) < cm * Real.sqrt (1 + β) := by
  have hs : 0 < Real.sqrt (1 + β) := Real.sqrt_pos.mpr (by linarith)
  have : 0 < cm * Real.sqrt (1 + β) := mul_pos hcm hs
  exact ⟨this, by linarith, by linarith⟩

/-! ## Static structure (D3) -/

theorem exch_static_theta {cf vt gb N M rled eps S E θ ϑ β : ℝ} (hcf : cf ≠ 0) (hN : N ≠ 0)
    (hϑ : ϑ = vt * gb / N) (hβ : β = cf * vt ^ 2 / N)
    (heps : eps = -rled / cf) (hS : S = cf * vt * eps) (hE : E = (gb * M + S) / N)
    (hθ : θ = eps + vt * E) :
    θ = ϑ * M - (1 + β) * rled / cf := by
  subst hϑ hβ heps hS hE hθ
  field_simp
  ring

theorem exch_static_reaction {cf vt gb N M rled eps S E F ϑ lamt : ℝ} (hcf : cf ≠ 0) (hN : N ≠ 0)
    (hvt : vt ≠ 0) (hgb : gb ≠ 0) (_hM : M ≠ 0)
    (hϑ : ϑ = vt * gb / N) (hlam : lamt = vt / (gb * M))
    (heps : eps = -rled / cf) (hS : S = cf * vt * eps) (hE : E = (gb * M + S) / N)
    (hF : F = -gb * E) :
    F / ϑ = rled - 1 / lamt := by
  subst hϑ hlam heps hS hE hF
  field_simp
  ring

theorem exch_reaction_via_delta {r lamt : ℝ} (hl : lamt ≠ 0) :
    r - 1 / lamt = (lamt * r - 1) / lamt := by
  field_simp

theorem exch_reaction_ne_rled {r lamt : ℝ} (hl : lamt ≠ 0) : r - 1 / lamt ≠ r := by
  intro h
  have : 1 / lamt = 0 := by linarith
  exact one_div_ne_zero hl this

theorem exch_reaction_neg_of_delta_lt_one {r lamt : ℝ} (hl : 0 < lamt) (hd : lamt * r < 1) :
    r - 1 / lamt < 0 := by
  rw [exch_reaction_via_delta hl.ne']
  exact div_neg_of_neg_of_pos (by linarith) hl

/-- `delta = lam_t r_led`, `f_bb = (vartheta M / (vt/g_b)) / (vartheta r_led)`: `f_bb = 1/(lam_t r_led)` and `delta f_bb = 1`. -/
theorem exch_static_delta_fbb {vt gb M rled ϑ lamt : ℝ} (hvt : vt ≠ 0) (hgb : gb ≠ 0) (hM : M ≠ 0)
    (hr : rled ≠ 0) (hϑ : ϑ ≠ 0) (hlam : lamt = vt / (gb * M)) :
    (ϑ * M / (vt / gb)) / (ϑ * rled) = 1 / (lamt * rled) ∧
      (lamt * rled) * ((ϑ * M / (vt / gb)) / (ϑ * rled)) = 1 := by
  subst hlam
  constructor
  · field_simp
  · field_simp

theorem exch_delta_mul_fbb {lamt rled : ℝ} (h : lamt * rled ≠ 0) :
    (lamt * rled) * (1 / (lamt * rled)) = 1 := mul_one_div_cancel h

theorem exch_open_delta_zero (lamt : ℝ) : lamt * 0 = 0 := mul_zero lamt

/-! ## The trade-off delta * f_bb = 1 (state precisely) -/

theorem exch_fbb_gt_one {δ f : ℝ} (hδ0 : 0 < δ) (hδ1 : δ < 1) (h : δ * f = 1) : 1 < f := by
  by_contra hf
  have hf : f ≤ 1 := not_lt.mp hf
  have hfpos : 0 < f := by
    by_contra hf0
    have hf0 : f ≤ 0 := not_lt.mp hf0
    nlinarith
  nlinarith

theorem exch_fbb_large {δ f ε : ℝ} (hδ : 0 < δ) (hε : δ ≤ ε) (h : δ * f = 1) : 1 / ε ≤ f := by
  have hf : f = 1 / δ := by field_simp; linarith
  rw [hf]
  exact one_div_le_one_div_of_le hδ hε

theorem exch_not_both_small {δ f a b : ℝ} (hδ : 0 < δ) (hf : 0 < f) (h : δ * f = 1)
    (hab : a * b < 1) : ¬ (δ ≤ a ∧ f ≤ b) := by
  rintro ⟨h1, h2⟩
  have : δ * f ≤ a * b := mul_le_mul h1 h2 hf.le (by linarith)
  linarith

/-! ## Tie of beta to eps_c, and the delivered-heat fraction -/

theorem exch_beta_eq_epsc_lamt {cf vt gb N M ϑ epsc lamt β : ℝ} (hN : N ≠ 0) (hgb : gb ≠ 0) (hM : M ≠ 0)
    (hϑ : ϑ = vt * gb / N) (hepsc : epsc = cf * (ϑ * M)) (hlam : lamt = vt / (gb * M))
    (hβ : β = cf * vt ^ 2 / N) : β = epsc * lamt := by
  subst hϑ hepsc hlam hβ
  field_simp

theorem exch_freal_split {β epsc lamt rled : ℝ} (he : epsc ≠ 0) (hβ : β = epsc * lamt) :
    1 - (1 + β) * rled / epsc = 1 - rled / epsc - lamt * rled := by
  subst hβ
  field_simp
  ring

theorem exch_freal_open {β epsc : ℝ} : 1 - (1 + β) * 0 / epsc = 1 := by simp

theorem exch_freal_lt_one {β epsc rled : ℝ} (hr : 0 < rled) (he : 0 < epsc) (hβ : -1 < β) :
    1 - (1 + β) * rled / epsc < 1 := by
  have : 0 < (1 + β) * rled / epsc := by
    have : 0 < 1 + β := by linarith
    positivity
  linarith

/-! ## Retardation algebra (D4, value level) -/

theorem exch_retardation_iff {N c gb Mtt Stt Mrr Srr Eqt Eqr wt wr : ℝ} (hN : N ≠ 0) (hc : c ≠ 0)
    (hEt : N * Eqt = gb * Mtt + Stt) (hEr : N * Eqr = gb * Mrr + Srr) :
    N * ((Eqt + wt) / c ^ 2 - (Eqr + wr)) = -gb * Mrr - Srr ↔
      N * (wt / c ^ 2 - wr) = -(gb * Mtt + Stt) / c ^ 2 := by
  have hc2 : c ^ 2 ≠ 0 := pow_ne_zero 2 hc
  have key : N * ((Eqt + wt) / c ^ 2 - (Eqr + wr)) + gb * Mrr + Srr
      = N * (wt / c ^ 2 - wr) + (gb * Mtt + Stt) / c ^ 2 := by
    have h1 : N * ((Eqt + wt) / c ^ 2 - (Eqr + wr))
        = (N * Eqt) / c ^ 2 + N * (wt / c ^ 2 - wr) - N * Eqr := by
      field_simp
      ring
    rw [h1, hEt, hEr]
    ring
  constructor
  · intro h
    have : N * (wt / c ^ 2 - wr) + (gb * Mtt + Stt) / c ^ 2 = 0 := by linarith
    have h2 : -(gb * Mtt + Stt) / c ^ 2 = -((gb * Mtt + Stt) / c ^ 2) := by ring
    rw [h2]; linarith
  · intro h
    have h2 : -(gb * Mtt + Stt) / c ^ 2 = -((gb * Mtt + Stt) / c ^ 2) := by ring
    rw [h2] at h
    linarith

/-! ## sigma-slaved reaction and the hydrostatic shell reading (D6) -/

noncomputable def sigmaReact (a0 g : ℝ) : ℝ := 3 / 8 * a0 * (2 * g + a0) / (g + a0)

theorem exch_sigma_strictMono {a0 g₁ g₂ : ℝ} (ha : 0 < a0) (h1 : -a0 < g₁) (h12 : g₁ < g₂) :
    sigmaReact a0 g₁ < sigmaReact a0 g₂ := by
  unfold sigmaReact
  have p1 : 0 < g₁ + a0 := by linarith
  have p2 : 0 < g₂ + a0 := by linarith
  have key : 3 / 8 * a0 * (2 * g₂ + a0) / (g₂ + a0) - 3 / 8 * a0 * (2 * g₁ + a0) / (g₁ + a0)
      = 3 / 8 * a0 ^ 2 * (g₂ - g₁) / ((g₁ + a0) * (g₂ + a0)) := by
    field_simp
    ring
  have : 0 < 3 / 8 * a0 ^ 2 * (g₂ - g₁) / ((g₁ + a0) * (g₂ + a0)) := by
    have : 0 < g₂ - g₁ := by linarith
    positivity
  linarith

theorem exch_sigma_bounds {a0 g : ℝ} (ha : 0 < a0) (hg : 0 < g) :
    3 / 8 * a0 < sigmaReact a0 g ∧ sigmaReact a0 g < 3 / 4 * a0 := by
  have h0 : sigmaReact a0 0 = 3 / 8 * a0 := by
    unfold sigmaReact; field_simp; ring
  have hs := exch_sigma_strictMono ha (by linarith : -a0 < 0) hg
  refine ⟨by rw [← h0]; exact hs, ?_⟩
  unfold sigmaReact
  have hp : 0 < g + a0 := by linarith
  rw [div_lt_iff₀ hp]
  nlinarith [mul_pos ha hg]

theorem exch_sigma_pointmass {a0 x : ℝ} (ha : 0 < a0) (hx : x ≠ 0) :
    sigmaReact a0 (a0 / x ^ 2) = 3 / 8 * a0 * (2 + x ^ 2) / (1 + x ^ 2) := by
  have hx2 : 0 < x ^ 2 := by positivity
  unfold sigmaReact
  have h1 : (a0 / x ^ 2) + a0 ≠ 0 := by positivity
  have h2 : 1 + x ^ 2 ≠ 0 := by positivity
  field_simp

theorem exch_sigma_pointmass_strictAnti {a0 x₁ x₂ : ℝ} (ha : 0 < a0) (hx1 : 0 < x₁) (h12 : x₁ < x₂) :
    sigmaReact a0 (a0 / x₂ ^ 2) < sigmaReact a0 (a0 / x₁ ^ 2) := by
  have hx2 : 0 < x₂ := lt_trans hx1 h12
  have hlt : a0 / x₂ ^ 2 < a0 / x₁ ^ 2 :=
    div_lt_div_of_pos_left ha (by positivity) (by nlinarith)
  exact exch_sigma_strictMono ha (by have : 0 < a0 / x₂ ^ 2 := by positivity
                                     linarith) hlt

theorem exch_shell_integral {u : ℝ} (hu : u ≠ 0) :
    ∫ r in (0 : ℝ)..u, r ^ 2 / u ^ 2 = u / 3 := by
  have : ∀ r : ℝ, r ^ 2 / u ^ 2 = (u ^ 2)⁻¹ * r ^ 2 := fun r => by ring
  simp_rw [this]
  rw [intervalIntegral.integral_const_mul, integral_pow]
  field_simp
  ring

/-- shell energy of the hydrostatic reading, closed form `(3/4) a0 dm ((R - u) + u/3)` -/
noncomputable def hydShellE (a0 dm R u : ℝ) : ℝ := 3 / 4 * a0 * dm * ((R - u) + u / 3)

theorem exch_hyd_reaction (a0 dm R u : ℝ) :
    HasDerivAt (hydShellE a0 dm R) (-(a0 / 2) * dm) u := by
  unfold hydShellE
  have h : HasDerivAt (fun u : ℝ => 3 / 4 * a0 * dm * ((R - u) + u / 3))
      (3 / 4 * a0 * dm * ((0 - 1) + 1 / 3)) u := by
    have h1 : HasDerivAt (fun u : ℝ => (R - u) + u / 3) ((0 - 1) + 1 / 3) u :=
      ((hasDerivAt_const u R).sub (hasDerivAt_id u)).add ((hasDerivAt_id u).div_const 3)
    exact h1.const_mul _
  convert h using 1
  ring

theorem exch_hyd_reaction_per_mass {a0 dm : ℝ} (hdm : dm ≠ 0) : -(-(a0 / 2) * dm) / dm = a0 / 2 := by
  field_simp
