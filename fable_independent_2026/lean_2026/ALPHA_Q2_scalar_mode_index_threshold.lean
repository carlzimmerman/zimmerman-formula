import Mathlib

/-!
# M2_04 -- Lean certificate for the charged-scalar mode index in planar dS_D and the conformal threshold (lane Q2)
Source lane: real_research/alpha_principle_2026/Q2_nonminimal_conformal/
  q1_mode_equation.py (checks M1-M2; the Whittaker substitution, symbolic step M2) and
  q4_threshold_test.py (checks Q1, Q2, Q4).
Corpus check: `git grep -n -i -e Whittaker -e "12 \* xi" -e fall-to -- '*.lean'` returns nothing.  New.

Setting (from the lane): for chi = a^{(D-2)/2} phi in planar dS_D with a constant field along z, conformal time tau < 0,
lam = eE/H^2, r = k_z/k, the covariant mode equation is
  chi'' + [ (k r + lam/tau)^2 + k^2 (1 - r^2) + (mu^2 + xi D (D-1) - D(D-2)/4)/tau^2 ] chi = 0.
The lane derives this by computer algebra for D = 2..6 (NOT reproduced here: the covariant derivation / Christoffel
symbols / R = D(D-1)H^2 step is a sympy calculation, outside what this file certifies).

CERTIFIED (pure mathematics, real parameters, complex value of the mode at a point):
* `whittaker_reduces_mode_eq`: let z = 2 i k tau, kappa_W = -i lam r, and
  mw2 = (D-1)^2/4 - lam^2 - mu^2 - xi D (D-1).  If W'' (a complex number standing for the second derivative at z)
  satisfies Whittaker's equation W'' = (1/4 - kappa_W/z - (1/4 - mw2)/z^2) W, and chi'' = (2 i k)^2 W'' (chain rule,
  given as a hypothesis), then chi'' + [potential above] chi = 0 exactly.  (k /= 0, tau /= 0.)
  i.e. the index formula mu_w^2 = (D-1)^2/4 - lam^2 - mu^2 - xi D(D-1) is the one that makes the Whittaker function solve
  the mode equation, for every real D.
* `wrong_index_residual`: the dS_2 index 1/4 - lam^2 - mu^2 used at D = 4, xi = 0 leaves the residual -(2/tau^2) W /= 0
  (the script's mutation control).
* `conformal_index`: xi_c = (D-2)/(4 (D-1)) gives xi_c D (D-1) = D (D-2)/4 and mw2 = 1/4 - lam^2 - mu^2 for every D /= 1.
  `D4_index`: at D = 4, mw2 = 9/4 - lam^2 - mu^2 - 12 xi.  `xi_is_mass_shift`: at D = 4 the xi-dependence is exactly the
  mass shift mu^2 -> mu^2 + 12 xi in the index.
* threshold table: mw2 = 0 gives lam_c^2 = (D-1)^2/4 - mu^2 - xi D(D-1); minimal massless (mu = 0, xi = 0): lam_c = (D-1)/2;
  conformal massless: lam_c^2 = 1/4 in every D (`threshold_conformal_massless`); massive conformal: lam_c^2 = 1/4 - mu^2.
* `fall_to_centre`: (exists real s with s (s-1) + g = 0) <=> g <= 1/4, so the conformal massless threshold lam = 1/2 is
  the inverse-square critical constant 1/4 (with g = lam^2).
* `kappa_root`: for every kappa > 0 the equation sqrt(1/4 - mu^2)/mu = kappa has the root mu^2 = 1/(4 (1 + kappa^2)) < 1/4;
  and F_c = m a0 with F_c = hbar H^2/(2c), a0 = kappa c H gives m = hbar H/(2 kappa c^2) (`crit_force_mass`).
  (So 'lam_c = kappa' is a restatement of a mass choice, as the lane concludes.)
NOT CERTIFIED: the covariant derivation of the mode equation, the Bunch-Davies normalisation and Wronskian, the
numerical ODE-vs-Whittaker agreement (M3-M5), the current / pair-production results, any relation to alpha.
The lane is a NEGATIVE result: lam_c = 1/2 fixes eE/H^2 not e, so alpha stays an input; kappa = 1/2 stays FITTED.
-/

namespace M2ModeIndex

open Complex

/-- the Whittaker index squared for planar dS_D -/
noncomputable def mw2 (D lam mu xi : ℝ) : ℝ := (D - 1) ^ 2 / 4 - lam ^ 2 - mu ^ 2 - xi * D * (D - 1)

/-- the mode-equation potential (coefficient of chi) -/
noncomputable def pot (D k r lam mu xi tau : ℝ) : ℝ :=
  (k * r + lam / tau) ^ 2 + k ^ 2 * (1 - r ^ 2) + (mu ^ 2 + xi * D * (D - 1) - D * (D - 2) / 4) / tau ^ 2

theorem whittaker_reduces_mode_eq (k r lam mu xi D tau : ℝ) (hk : k ≠ 0) (ht : tau ≠ 0)
    (W W2 chi2 : ℂ)
    (hW : W2 = (1 / 4 - (-(I * lam * r)) / (2 * I * k * tau)
                - (1 / 4 - (mw2 D lam mu xi : ℝ)) / (2 * I * k * tau) ^ 2) * W)
    (hchi : chi2 = (2 * I * k) ^ 2 * W2) :
    chi2 + ((pot D k r lam mu xi tau : ℝ) : ℂ) * W = 0 := by
  have hk' : (k : ℂ) ≠ 0 := by exact_mod_cast hk
  have ht' : (tau : ℂ) ≠ 0 := by exact_mod_cast ht
  unfold mw2 at hW
  unfold pot
  rw [hchi, hW]
  push_cast
  field_simp
  ring_nf
  simp [Complex.I_sq]

/-- power test: the dS_2 index used for D = 4, xi = 0 does NOT solve the mode equation (residual -2/tau^2) -/
theorem wrong_index_residual (k r lam mu tau : ℝ) (hk : k ≠ 0) (ht : tau ≠ 0)
    (W W2 chi2 : ℂ)
    (hW : W2 = (1 / 4 - (-(I * lam * r)) / (2 * I * k * tau)
                - (1 / 4 - ((1 / 4 - lam ^ 2 - mu ^ 2 : ℝ))) / (2 * I * k * tau) ^ 2) * W)
    (hchi : chi2 = (2 * I * k) ^ 2 * W2) :
    chi2 + ((pot 4 k r lam mu 0 tau : ℝ) : ℂ) * W = ((-2 / tau ^ 2 : ℝ) : ℂ) * W := by
  have hk' : (k : ℂ) ≠ 0 := by exact_mod_cast hk
  have ht' : (tau : ℂ) ≠ 0 := by exact_mod_cast ht
  unfold pot
  rw [hchi, hW]
  push_cast
  field_simp
  ring_nf
  simp [Complex.I_sq]
  ring

theorem wrong_index_nonzero (tau : ℝ) (ht : tau ≠ 0) : (-2 / tau ^ 2 : ℝ) ≠ 0 := by
  have : tau ^ 2 ≠ 0 := pow_ne_zero 2 ht
  intro h
  rw [div_eq_zero_iff] at h
  rcases h with h | h <;> [norm_num at h; exact this h]

theorem conformal_index (D lam mu : ℝ) (hD : D ≠ 1) :
    (D - 2) / (4 * (D - 1)) * D * (D - 1) = D * (D - 2) / 4 ∧
    mw2 D lam mu ((D - 2) / (4 * (D - 1))) = 1 / 4 - lam ^ 2 - mu ^ 2 := by
  have h : D - 1 ≠ 0 := sub_ne_zero.mpr hD
  refine ⟨?_, ?_⟩
  · field_simp
  · unfold mw2
    field_simp
    ring

theorem D4_index (lam mu xi : ℝ) : mw2 4 lam mu xi = 9 / 4 - lam ^ 2 - mu ^ 2 - 12 * xi := by
  unfold mw2; ring

theorem xi_is_mass_shift (lam mu xi : ℝ) (h : 0 ≤ mu ^ 2 + 12 * xi) :
    mw2 4 lam mu xi = mw2 4 lam (Real.sqrt (mu ^ 2 + 12 * xi)) 0 := by
  unfold mw2
  rw [Real.sq_sqrt h]; ring

theorem D2_minimal_is_conformal (lam mu : ℝ) :
    (2 - 2) / (4 * (2 - 1)) = (0 : ℝ) ∧ mw2 2 lam mu 0 = 1 / 4 - lam ^ 2 - mu ^ 2 := by
  refine ⟨by norm_num, ?_⟩
  unfold mw2; ring

/-- threshold: mw2 = 0 gives lam_c^2 -/
theorem threshold_sq (D lam mu xi : ℝ) :
    mw2 D lam mu xi = 0 ↔ lam ^ 2 = (D - 1) ^ 2 / 4 - mu ^ 2 - xi * D * (D - 1) := by
  unfold mw2; constructor <;> intro h <;> linarith

theorem threshold_minimal_massless (D : ℝ) (lam : ℝ) (hl : 0 ≤ lam) (hD : 1 ≤ D) :
    mw2 D lam 0 0 = 0 ↔ lam = (D - 1) / 2 := by
  unfold mw2
  constructor
  · intro h
    have h2 : lam ^ 2 = ((D - 1) / 2) ^ 2 := by nlinarith [h]
    have hD2 : 0 ≤ (D - 1) / 2 := by linarith
    exact (sq_eq_sq₀ hl hD2).mp h2
  · intro h; subst h; ring

theorem threshold_conformal_massless (D lam : ℝ) (hD : D ≠ 1) :
    mw2 D lam 0 ((D - 2) / (4 * (D - 1))) = 0 ↔ lam ^ 2 = 1 / 4 := by
  rw [(conformal_index D lam 0 hD).2]
  constructor <;> intro h <;> nlinarith [h]

theorem threshold_conformal_massive (D lam mu : ℝ) (hD : D ≠ 1) :
    mw2 D lam mu ((D - 2) / (4 * (D - 1))) = 0 ↔ lam ^ 2 = 1 / 4 - mu ^ 2 := by
  rw [(conformal_index D lam mu hD).2]
  constructor <;> intro h <;> linarith

/-- fall to the centre: chi'' + g chi/tau^2 = 0 has power solutions (-tau)^s, s (s-1) + g = 0, real iff g <= 1/4 -/
theorem fall_to_centre (g : ℝ) : (∃ s : ℝ, s * (s - 1) + g = 0) ↔ g ≤ 1 / 4 := by
  constructor
  · rintro ⟨s, hs⟩
    nlinarith [sq_nonneg (s - 1 / 2)]
  · intro h
    refine ⟨1 / 2 + Real.sqrt (1 / 4 - g) , ?_⟩
    have h0 : 0 ≤ 1 / 4 - g := by linarith
    have := Real.sq_sqrt h0
    nlinarith [this]

theorem fall_to_centre_lam (lam : ℝ) : (∃ s : ℝ, s * (s - 1) + lam ^ 2 = 0) ↔ |lam| ≤ 1 / 2 := by
  rw [fall_to_centre]
  constructor
  · intro h
    rw [abs_le]
    constructor <;> nlinarith [h, sq_nonneg (lam + 1 / 2), sq_nonneg (lam - 1 / 2)]
  · intro h
    have := abs_le.mp h
    nlinarith [this.1, this.2]

/-- for every kappa > 0, mu^2 = 1/(4 (1 + kappa^2)) solves 1/4 - mu^2 = kappa^2 mu^2 (i.e. sqrt(1/4 - mu^2)/mu = kappa) -/
theorem kappa_root (kappa : ℝ) (hk : 0 < kappa) :
    ∃ mu : ℝ, 0 < mu ∧ mu ^ 2 < 1 / 4 ∧ 1 / 4 - mu ^ 2 = kappa ^ 2 * mu ^ 2 := by
  have hpos : 0 < 4 * (1 + kappa ^ 2) := by positivity
  refine ⟨Real.sqrt (1 / (4 * (1 + kappa ^ 2))), Real.sqrt_pos.mpr (by positivity), ?_, ?_⟩
  · rw [Real.sq_sqrt (by positivity)]
    rw [div_lt_div_iff₀ hpos (by norm_num)]
    nlinarith [sq_nonneg kappa]
  · rw [Real.sq_sqrt (by positivity)]
    field_simp
    ring

/-- F_c = hbar H^2/(2c) and a0 = kappa c H give the mass m = F_c / a0 = hbar H/(2 kappa c^2) -/
theorem crit_force_mass (hb H c kappa : ℝ) (hc : c ≠ 0) (hH : H ≠ 0) (hk : kappa ≠ 0) :
    (hb * H ^ 2 / (2 * c)) / (kappa * c * H) = hb * H / (2 * kappa * c ^ 2) := by
  field_simp

end M2ModeIndex

#print axioms M2ModeIndex.whittaker_reduces_mode_eq
#print axioms M2ModeIndex.wrong_index_residual
#print axioms M2ModeIndex.wrong_index_nonzero
#print axioms M2ModeIndex.conformal_index
#print axioms M2ModeIndex.D4_index
#print axioms M2ModeIndex.xi_is_mass_shift
#print axioms M2ModeIndex.D2_minimal_is_conformal
#print axioms M2ModeIndex.threshold_sq
#print axioms M2ModeIndex.threshold_minimal_massless
#print axioms M2ModeIndex.threshold_conformal_massless
#print axioms M2ModeIndex.threshold_conformal_massive
#print axioms M2ModeIndex.fall_to_centre
#print axioms M2ModeIndex.fall_to_centre_lam
#print axioms M2ModeIndex.kappa_root
#print axioms M2ModeIndex.crit_force_mass
