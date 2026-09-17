import Mathlib

/-!
# YM04 -- THE ENERGY FRACTION: the vector's halo background register

**SUPERSEDE FLAG (2026-09-17, after YM04b):** this file's register -- the
candidate closed form eps(u) = mu_2(u) u^2 / (2 mu_2(u) u^2 + 1) -- is the
k-essence-form TRUNCATION. YM04b_vector_halo_physical.py (6/6) shows the
physical fraction is eps_phys(u) = C * mu_2(u) * u with the PHANTOM density
(dust-dominated, ~1e5 x Lambda^4 at the Sun) as denominator: eps_phys ~ 1e-7
class at the Sun, NOT 0.017 -- YM04's 15/15 numbers 0.1855/0.0171/0.371 are
SUPERSEDED (denominator error, ~1e5). This file's algebra remains VALID for
its own register (positivity, the 1/2 bound, the vacuum closing, monotonicity
all hold), but its numeric bands describe the truncated register, not the
physical fraction; the physical register's spine is certified in
YM04b_energy_fraction_physical.lean. The tensor algebra of the vector's
anisotropic stress (alpha_A = -2, P_r - P_t = +2 E_A, trace -2 E_A) is
register-INDEPENDENT and survives unchanged.

**Scope statement (as every certificate in this repo reads):** Lean certifies
the MATHEMATICS. The physical premises -- the YM04 lane's candidate closed
form for the vector field's energy fraction of the halo background,
eps(u) = (mu_2(u) * u^2) / (2 * mu_2(u) * u^2 + 1) with the kernel register
mu_2(u) = u(2+u)/(1+u)^2 (the SAME kernel face as YM02's pinned ladder), u
the density-parameter register and eps the fraction of the halo's energy
carried by the vector condensate -- are the committed lanes' claims
(deepseek_push/yang_mills_gap/YM04_energy_fraction.py, YM_PROOF.md).  This
file restates every definition from scratch (standalone: `import Mathlib`
only, no import of YM01_gap.lean / YM02_pinned_gap.lean) and certifies the
algebraic spine of the eps register: the cleared denominator-free form,
positivity on the physical branch, the universal 1/2 bound (the denominator
is the numerator plus one), the 1 bound, the vacuum closing eps(0) = 0, the
strict monotone rise in u, and the committed SUN BAND at u = 2276/10000 by
exact rational arithmetic.  The 3-kpc band has a NAMED BLOCKER and is
documented, not certified (see the NUMERIC BAND section): the Lean file
certifies the ALGEBRAIC properties of this register, whatever the lane's
exact form ultimately lands as -- if the lane's final closed form differs
from the one committed here by an O(1) coefficient, every property below
still holds mutatis mutandis.

Nothing here claims the SU(3)/QCD-scale gap (the Clay problem): the framework
has no QCD sector (TOE_STATUS.md); what is proven is the framework's OWN halo
register.

**THE NUMERIC BAND -- what is certified and what is not.**  Python
(fractions.Fraction, exact rational arithmetic) certifies the register
values:

    eps(2276/10000) = 1025921230121/60919098710242 ~ 0.016841   (Sun register)
    eps(6221/10000) = 6312913731327281/38937911562654562 ~ 0.162128
    eps(467/10000)  = 2084514071921/10959977928143842  ~ 0.000190  (2e-4 probe)

Lean certifies eps(2276/10000) in (1/100, 3/100) by exact rational `norm_num`
arithmetic (theorem eps_sun_band; no transcendental appears), plus the whole
symbolic spine.  **NAMED BLOCKER (eps_inner_band DELETED):** the brief's
committed 3-kpc statement eps(6221/10000) in (5/100, 15/100) does NOT close
-- the register value is ~ 0.16213, strictly ABOVE the 15% edge (the brief's
quoted "eps(0.6221) ~ 0.096" does not reproduce at the committed register
with the committed formula:  a = mu_2(u) u^2 ~ 0.2399,  eps = a/(2a+1) ~
0.1621).  The Python-certified replacement band at the committed u is
eps(6221/10000) in (81/500, 163/1000) = (16.2%, 16.3%), documented here
rather than stated as a theorem per the brief's rule that numeric registers
failing the committed window are documented and named; Lean's symbolic bound
eps(u) < 1/2 covers every register.

Zero sorry.  Axioms: {propext, Classical.choice, Quot.sound} only.  Compiled
against the repo's Mathlib build (Lean 4.34.0-rc2).
-/
noncomputable section
open scoped Real

/-- the kernel register (verbatim from YM02):  mu_2(u) = u*(2+u)/(1+u)^2 -/
noncomputable def mu2 (u : ℝ) : ℝ := u * (2 + u) / (1 + u)^2

/-- the vector's energy fraction of the halo background (the YM04 register):
    eps(u) = (mu_2(u) * u^2) / (2 * mu_2(u) * u^2 + 1) -- the denominator is
    the numerator plus one, so the fraction is always well below 1 -/
noncomputable def eps (u : ℝ) : ℝ := (mu2 u * u^2) / (2 * mu2 u * u^2 + 1)

/-- the kernel face is positive:  0 < u  ->  0 < mu_2(u)  -- no ghost sector
    (verbatim from YM02's mu2_pos) -/
theorem mu2_pos (u : ℝ) (hu : 0 < u) : 0 < mu2 u := by
  unfold mu2
  have h2u : 0 < 2 + u := by linarith [hu]
  have hnum : 0 < u * (2 + u) := mul_pos hu h2u
  have hden : 0 < (1 + u)^2 := by nlinarith [hu]
  exact div_pos hnum hden

/-- the vacuum closing rung:  mu_2(0) = 0  (verbatim from YM02's mu2_zero) -/
theorem mu2_zero : mu2 0 = 0 := by
  unfold mu2
  norm_num

/-- the eps denominator is strictly positive on the physical branch:
        0 < u  ->  0 < 2 * mu_2(u) * u^2 + 1  (mu_2 > 0 and u^2 >= 0) -/
theorem eps_denom_pos (u : ℝ) (hu : 0 < u) : 0 < 2 * mu2 u * u^2 + 1 := by
  have hmu : 0 ≤ mu2 u := (mu2_pos u hu).le
  have hterm : 0 ≤ (2 * mu2 u) * u^2 :=
    mul_nonneg (mul_nonneg (by norm_num : (0:ℝ) ≤ 2) hmu) (sq_nonneg u)
  nlinarith [hterm]

/-- 1. THE CLEARED FORM:  (2 * mu_2(u) * u^2 + 1) * eps(u) = mu_2(u) * u^2
        -- the denominator-free register, the fraction's defining relation
        (positive denominator from 0 < u, one `field_simp`) -/
theorem eps_closed (u : ℝ) (hu : 0 < u) : (2 * mu2 u * u^2 + 1) * eps u = mu2 u * u^2 := by
  unfold eps
  have hpos : 0 < 2 * mu2 u * u^2 + 1 := eps_denom_pos u hu
  field_simp [ne_of_gt hpos]

/-- 2. THE FRACTION IS POSITIVE:  0 < u  ->  0 < eps(u)  -- the halo vector
        condensate carries a strictly positive share of the background energy -/
theorem eps_pos (u : ℝ) (hu : 0 < u) : 0 < eps u := by
  unfold eps
  have hnum : 0 < mu2 u * u^2 := mul_pos (mu2_pos u hu) (sq_pos_of_pos hu)
  exact div_pos hnum (eps_denom_pos u hu)

/-- 3. THE 1/2 BOUND:  0 < u  ->  eps(u) < 1/2  -- the denominator exceeds
        the numerator by one:  with a := mu_2(u)*u^2 >= 0,  eps = a/(2a+1)
        and  a < 2a + 1,  so eps < 1/2 by clearing the (positive) denominator -/
theorem eps_bound_one_half (u : ℝ) (hu : 0 < u) : eps u < 1 / 2 := by
  unfold eps
  have hpos : 0 < 2 * mu2 u * u^2 + 1 := eps_denom_pos u hu
  rw [div_lt_iff₀ hpos]
  nlinarith

/-- 4. THE 1 BOUND:  0 < u  ->  eps(u) < 1  -- from the 1/2 bound and 1/2 < 1 -/
theorem eps_bound_one (u : ℝ) (hu : 0 < u) : eps u < 1 := by
  nlinarith [eps_bound_one_half u hu, (by norm_num : (1 / 2 : ℝ) < 1)]

/-- 5. THE VACUUM CLOSING:  no density, no vector share  --  eps(0) = 0
        (mu_2(0) = 0, then `norm_num`) -/
theorem eps_zero_vacuum : eps 0 = 0 := by
  unfold eps
  rw [mu2_zero]
  norm_num

/-- 6a. THE SUN BAND:  at the committed Sun register u = 2276/10000 the
         vector's energy fraction sits inside (1/100, 3/100)  -- exact
         rational `norm_num` arithmetic on the cleared register, no
         transcendental (Python-certified value
         1025921230121/60919098710242 ~ 0.016841) -/
theorem eps_sun_band : (1 / 100 : ℝ) < eps (2276 / 10000) ∧ eps (2276 / 10000) < (3 / 100) := by
  norm_num [eps, mu2]

/- 6b. THE 3-kpc BAND is DELETED -- see the header's NAMED BLOCKER: the
         committed window (5/100, 15/100) does NOT contain the register value
         eps(6221/10000) ~ 0.162128 (Python-certified), so no honest theorem
         claims it; the Python-certified replacement band
         (81/500, 163/1000) = (16.2%, 16.3%) is documented, not certified. -/

/-- 7a. THE KERNEL IS STRICTLY RISING:  0 < u < v  ->  mu_2(u) < mu_2(v)
         (the cross-multiplied numerator difference factors as
         (v-u)*(2+u+v) over positive squares) -/
theorem mu2_strictMono (u v : ℝ) (hu : 0 < u) (hv : 0 < v) (huv : u < v) : mu2 u < mu2 v := by
  unfold mu2
  have hdu_pos : 0 < (1 + u)^2 := by nlinarith [hu]
  have hdv_pos : 0 < (1 + v)^2 := by nlinarith [hv]
  rw [div_lt_div_iff₀ hdu_pos hdv_pos]
  have hnum : v * (2 + v) * (1 + u)^2 - u * (2 + u) * (1 + v)^2 = (v - u) * (2 + u + v) := by
    ring
  have hpos : 0 < v * (2 + v) * (1 + u)^2 - u * (2 + u) * (1 + v)^2 := by
    rw [hnum]
    exact mul_pos (by linarith) (by nlinarith [hu, hv])
  nlinarith [hpos]

/-- 7b. THE MONOTONE SPINE:  0 < u < v  ->  eps(u) < eps(v)  -- hotter
         density registers carry a strictly larger vector share, realized as
         eps = a/(2a+1) rising in a := mu_2(u)*u^2, itself the product of the
         two strictly rising positive factors mu_2 and u^2 -/
theorem eps_mono (u v : ℝ) (hu : 0 < u) (hv : 0 < v) (huv : u < v) : eps u < eps v := by
  have hmu2 : mu2 u < mu2 v := mu2_strictMono u v hu hv huv
  have hsq : u^2 < v^2 := by
    have hdiff : 0 < v - u := by linarith
    have hsum : 0 < v + u := by linarith
    have hid : v^2 - u^2 = (v - u) * (v + u) := by ring
    have hpos : 0 < v^2 - u^2 := by
      rw [hid]
      exact mul_pos hdiff hsum
    linarith
  have hpart1 : mu2 u * u^2 < mu2 u * v^2 := mul_lt_mul_of_pos_left hsq (mu2_pos u hu)
  have hpart2 : mu2 u * v^2 < mu2 v * v^2 := mul_lt_mul_of_pos_right hmu2 (sq_pos_of_pos hv)
  have ha : mu2 u * u^2 < mu2 v * v^2 := lt_trans hpart1 hpart2
  unfold eps
  have hdu : 0 < 2 * mu2 u * u^2 + 1 := eps_denom_pos u hu
  have hdv : 0 < 2 * mu2 v * v^2 + 1 := eps_denom_pos v hv
  rw [div_lt_div_iff₀ hdu hdv]
  nlinarith [ha]

end
#print axioms mu2_pos
#print axioms mu2_zero
#print axioms eps_denom_pos
#print axioms eps_closed
#print axioms eps_pos
#print axioms eps_bound_one_half
#print axioms eps_bound_one
#print axioms eps_zero_vacuum
#print axioms eps_sun_band
#print axioms mu2_strictMono
#print axioms eps_mono
