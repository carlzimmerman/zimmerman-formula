import Mathlib

/-!
# M6-B -- FP15 check T2, "the anchor law": the trigger-to-mean ratio R(z) and its logarithmic slope

Source: `real_research/derivation_chain_2026/FP15_zero_knob_dark_sector.py`, part T2 (lines 589-617, the sympy
block lines 592-598, the check at 609-615) and the ledger row L15c (line 1435):
    R(z) = E(z)^(2q + 1/2) / (1+z)^3,   E(z)^2 = Om (1+z)^3 + OL,
    d ln R / d ln(1+z) = (3/2)(2q + 1/2) Omega_m(z) - 3,      Omega_m(z) = Om (1+z)^3 / E(z)^2,
"R rises into the past iff Omega_m(z) > 1/(q + 1/4); at z = 0 that needs q > q* = 1/Omega_m0 - 1/4".
The script verifies the first line with sympy; the two consequences are printed prose.  Lean corpus check
(2026-09-29): `git grep -n -i -e "1/Omega" -e "trigger" -e "anchor law" -- '*.lean'` finds no such statement
(deepseek_push's `anchor` hits are unrelated `Z`-anchor files).  New.

Variables: u = 1+z > 0, p = q + 1/4 (so E^(2q+1/2) = (E^2)^p); Om, OL > 0.
CERTIFIED (real analysis, exact):
  * `R_hasDerivAt`  : d/du [(Om u^3 + OL)^p / u^3] = R(u) (3 p Om u^2/(Om u^3 + OL) - 3/u)   (u > 0);
  * `dlogR`         : u R'(u)/R(u) = 3 p Om_z(u) - 3, with Om_z(u) := Om u^3/(Om u^3 + OL) and
                      3 p = (3/2)(2q + 1/2) when p = q + 1/4  (the sympy identity);
  * `rises_iff`     : R'(u) > 0  <->  p * Om_z(u) > 1   (i.e. Omega_m(z) > 1/(q + 1/4));
  * `Omz_strictMono`: Om_z is strictly increasing in u, from Om/(Om + OL) at u = 1 to 1 (bounds `Omz_lt_one`);
  * `anchor_law`    : if Om + OL = 1 and q >= 1/Om - 1/4 then R'(u) > 0 for every u > 1 and R is strictly
                      increasing on [1, infinity): R(z = 0) < R(z) for all z > 0 ("the trigger's closest
                      approach to the mean is today");
  * `anchor_law_converse` : if Om + OL = 1 and q < 1/Om - 1/4 then R'(1) < 0 (R is falling at z = 0, so the
                      anchor law's threshold is sharp).
NOT CERTIFIED: that R(z) is FK1's trigger (rho_t ~ E^(2q+1/2)) or the meaning of q, zeta, the "pinned at
z = 2.5" normalisation; every numerical value (q* = 2.94 at Om = 0.315...) and the shared exponents 3.75/4/4.75
of T1 (they are FP9's p' plus a convention); any observational gate.  q remains FITTED-BY-DATA in the chain;
kappa = 1/2 FITTED; nothing here says the dark sector closes.
-/

noncomputable section
namespace M6B

open Real

/-- the trigger-to-mean ratio as a function of u = 1+z (p = q + 1/4) -/
def Rf (p Om OL u : ℝ) : ℝ := (Om * u ^ 3 + OL) ^ p / u ^ 3

/-- the matter fraction at u -/
def Omz (Om OL u : ℝ) : ℝ := Om * u ^ 3 / (Om * u ^ 3 + OL)

theorem R_hasDerivAt {p Om OL u : ℝ} (hOm : 0 < Om) (hOL : 0 < OL) (hu : 0 < u) :
    HasDerivAt (Rf p Om OL)
      (Rf p Om OL u * (3 * p * Om * u ^ 2 / (Om * u ^ 3 + OL) - 3 / u)) u := by
  have hA : 0 < Om * u ^ 3 + OL := by positivity
  have h1 : HasDerivAt (fun u : ℝ => Om * u ^ 3 + OL) (Om * (3 * u ^ 2)) u := by
    have := ((hasDerivAt_pow 3 u).const_mul Om).add_const OL
    simpa using this
  have h2 := h1.rpow_const (p := p) (Or.inl hA.ne')
  have h3 := h2.fun_div (hasDerivAt_pow 3 u) (pow_ne_zero 3 hu.ne')
  refine h3.congr_deriv ?_
  unfold Rf
  rw [Real.rpow_sub_one hA.ne' p]
  simp only [Nat.cast_ofNat]
  have hu0 : u ≠ 0 := hu.ne'
  field_simp
  ring

theorem dlogR {p Om OL u : ℝ} (hOm : 0 < Om) (hOL : 0 < OL) (hu : 0 < u) :
    u * (Rf p Om OL u * (3 * p * Om * u ^ 2 / (Om * u ^ 3 + OL) - 3 / u)) / Rf p Om OL u
      = 3 * p * Omz Om OL u - 3 := by
  have hA : 0 < Om * u ^ 3 + OL := by positivity
  have hR : 0 < Rf p Om OL u := by unfold Rf; positivity
  have hu0 : u ≠ 0 := hu.ne'
  unfold Omz
  field_simp

/-- the script's form: with p = q + 1/4, 3 p = (3/2)(2 q + 1/2) -/
theorem three_p (q : ℝ) : 3 * (q + 1 / 4) = 3 / 2 * (2 * q + 1 / 2) := by ring

theorem rises_iff {p Om OL u : ℝ} (hOm : 0 < Om) (hOL : 0 < OL) (hu : 0 < u) :
    0 < Rf p Om OL u * (3 * p * Om * u ^ 2 / (Om * u ^ 3 + OL) - 3 / u) ↔ 1 < p * Omz Om OL u := by
  have hA : 0 < Om * u ^ 3 + OL := by positivity
  have hR : 0 < Rf p Om OL u := by unfold Rf; positivity
  have hu0 : u ≠ 0 := hu.ne'
  have e : 3 * p * Om * u ^ 2 / (Om * u ^ 3 + OL) - 3 / u = 3 / u * (p * Omz Om OL u - 1) := by
    unfold Omz
    field_simp
  rw [e]
  have h3 : 0 < 3 / u := by positivity
  constructor
  · intro h
    have := (mul_pos_iff_of_pos_left hR).1 h
    have := (mul_pos_iff_of_pos_left h3).1 this
    linarith
  · intro h
    have : 0 < p * Omz Om OL u - 1 := by linarith
    positivity

theorem Omz_lt_one {Om OL u : ℝ} (hOm : 0 < Om) (hOL : 0 < OL) (hu : 0 < u) : Omz Om OL u < 1 := by
  unfold Omz
  have hA : 0 < Om * u ^ 3 + OL := by positivity
  rw [div_lt_one hA]
  linarith

theorem Omz_strictMono {Om OL : ℝ} (hOm : 0 < Om) (hOL : 0 < OL) {u v : ℝ} (hu : 0 < u) (huv : u < v) :
    Omz Om OL u < Omz Om OL v := by
  unfold Omz
  have hv : 0 < v := hu.trans huv
  have hA : 0 < Om * u ^ 3 + OL := by positivity
  have hB : 0 < Om * v ^ 3 + OL := by positivity
  rw [div_lt_div_iff₀ hA hB]
  have h3 : u ^ 3 < v ^ 3 := pow_lt_pow_left₀ huv hu.le (by norm_num)
  nlinarith [mul_pos hOm hOL]

theorem anchor_law_deriv_pos {q Om OL u : ℝ} (hOm : 0 < Om) (hOL : 0 < OL) (hsum : Om + OL = 1)
    (hq : 1 / Om - 1 / 4 ≤ q) (hu : 1 < u) :
    0 < Rf (q + 1 / 4) Om OL u * (3 * (q + 1 / 4) * Om * u ^ 2 / (Om * u ^ 3 + OL) - 3 / u) := by
  have hu0 : 0 < u := by linarith
  rw [rises_iff hOm hOL hu0]
  have h1 : Omz Om OL 1 < Omz Om OL u := Omz_strictMono hOm hOL one_pos hu
  have hO1 : Omz Om OL 1 = Om := by
    have : Om * 1 ^ 3 + OL = 1 := by linarith
    unfold Omz; rw [this]; ring
  rw [hO1] at h1
  have hp : 1 ≤ (q + 1 / 4) * Om := by
    have : 1 / Om ≤ q + 1 / 4 := by linarith
    rw [div_le_iff₀ hOm] at this
    linarith
  have hOz : 0 < Omz Om OL u := by unfold Omz; positivity
  nlinarith [mul_pos (show 0 < q + 1 / 4 by
    have : 0 < 1 / Om := by positivity
    linarith) (sub_pos.2 h1)]

theorem anchor_law {q Om OL : ℝ} (hOm : 0 < Om) (hOL : 0 < OL) (hsum : Om + OL = 1)
    (hq : 1 / Om - 1 / 4 ≤ q) :
    StrictMonoOn (Rf (q + 1 / 4) Om OL) (Set.Ici 1) := by
  apply strictMonoOn_of_deriv_pos (convex_Ici 1)
  · intro u hu
    have hu0 : 0 < u := lt_of_lt_of_le one_pos hu
    exact (R_hasDerivAt hOm hOL hu0).continuousAt.continuousWithinAt
  · intro u hu
    rw [interior_Ici] at hu
    have hu1 : 1 < u := hu
    have hu0 : 0 < u := by linarith
    rw [(R_hasDerivAt hOm hOL hu0).deriv]
    exact anchor_law_deriv_pos hOm hOL hsum hq hu1

theorem anchor_law_converse {q Om OL : ℝ} (hOm : 0 < Om) (hOL : 0 < OL) (hsum : Om + OL = 1)
    (hq : q < 1 / Om - 1 / 4) :
    Rf (q + 1 / 4) Om OL 1 * (3 * (q + 1 / 4) * Om * 1 ^ 2 / (Om * 1 ^ 3 + OL) - 3 / 1) < 0 := by
  have hR : 0 < Rf (q + 1 / 4) Om OL 1 := by unfold Rf; positivity
  have hp : (q + 1 / 4) * Om < 1 := by
    have : q + 1 / 4 < 1 / Om := by linarith
    rw [lt_div_iff₀ hOm] at this
    exact this
  have e : 3 * (q + 1 / 4) * Om * 1 ^ 2 / (Om * 1 ^ 3 + OL) - 3 / 1 = 3 * ((q + 1 / 4) * Om - 1) := by
    have : Om * 1 ^ 3 + OL = 1 := by linarith
    rw [this]; ring
  rw [e]
  exact mul_neg_of_pos_of_neg hR (by linarith)

end M6B

end

#print axioms M6B.R_hasDerivAt
#print axioms M6B.dlogR
#print axioms M6B.rises_iff
#print axioms M6B.Omz_strictMono
#print axioms M6B.anchor_law
#print axioms M6B.anchor_law_converse
