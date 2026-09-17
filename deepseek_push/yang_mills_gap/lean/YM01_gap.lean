import Mathlib

/-!
# YM01 -- THE EATEN GOLDSTONE: the mass gap of the gauged a0-sector

**Scope statement (as every certificate in this repo reads):** Lean certifies
the MATHEMATICS. The physical premises -- L5's shift-symmetric action
L = Lambda^4 f(K), K = -(1/2)(D phi)^2/Lambda^4, the minimal Stueckelberg
gauging D phi = d phi - m A, and the L2/G031 interpolant f'(K) = mu_2(u) --
are the committed lanes' claims (deepseek_push/yang_mills_gap/YM01_gap_derivation.py,
THE_THEORY.md L1-L16). This file certifies the algebraic spine of the mass
gap: the kernel face identities, positivity, the strict monotonicity (the
gap closes toward the cap), both exact mass faces, THE GAP THEOREM (the
massive branch lies above m), its attainment at k = 0, the Fock-space face
(n excitations cost at least m), the vacuum closing, the Stueckelberg gauge
identity, the eta(u) efficiency bounds, and the U-MAP closed form
C_f = 1/(2 sqrt(8 pi)) from the framework's own defining relations.

The clean face (the Stueckelberg truncation):  m_A = m * sqrt(mu_2(u)).
The exact face (FULL second order of the n=2 potential):
    m_A^2 = m^2 * u (u^2 + 3 u + 4) / (1 + u)^3,
with eta(u) = (u^2+3u+4)/((1+u)(2+u)) in [1, 2] their ratio (2 deep, 1 dense).

Nothing here claims the SU(3)/QCD-scale gap (the Clay problem): the framework
has no QCD sector (TOE_STATUS.md); what is proven is the framework's OWN gap
mechanism and its exact profile/scale law.

Monotonicity and the kernel face are stated in their CLEARED forms (the
fraction forms follow by dividing by the positive denominators, documented
not certified). Compiled against the repo's Mathlib build (Lean 4.34.0-rc2).
-/
noncomputable section
open scoped Real

noncomputable def mu2 (u : ℝ) : ℝ := u * (2 + u) / (1 + u)^2
noncomputable def gap_clean (m u : ℝ) : ℝ := m * Real.sqrt (mu2 u)
noncomputable def gap_exact (m u : ℝ) : ℝ :=
  m * Real.sqrt (u * (u^2 + 3 * u + 4) / (1 + u)^3)
noncomputable def branch (k m : ℝ) : ℝ := Real.sqrt (k^2 + m^2)
noncomputable def eta (u : ℝ) : ℝ := (u^2 + 3 * u + 4) / ((1 + u) * (2 + u))

/-- the kernel face, cleared: (1+u)^2 * mu_2(u) = u(2+u) -- A1 of the lane -/
theorem mu2_cleared (u : ℝ) (hu : 0 < u) : (1 + u)^2 * mu2 u = u * (2 + u) := by
  unfold mu2
  have hne : (1 + u)^2 ≠ 0 := by positivity
  field_simp [hne]

/-- the deep-regime face, exact: mu_2(u) = 2u (1+u/2)/(1+u)^2 -/
theorem mu2_deep (u : ℝ) (hu : 0 < u) :
    (1 + u)^2 * mu2 u = 2 * u * (1 + u / 2) := by
  unfold mu2
  have hne : (1 + u)^2 ≠ 0 := by positivity
  field_simp [hne]

/-- positivity: mu_2 > 0 on the deep branch (no ghost sector) -/
theorem mu2_pos (u : ℝ) (hu : 0 < u) : 0 < mu2 u := by
  unfold mu2
  have h2u : 0 < 2 + u := by linarith [hu]
  have hnum : 0 < u * (2 + u) := mul_pos hu h2u
  have hden : 0 < (1 + u)^2 := by nlinarith [hu]
  exact div_pos hnum hden

/-- the vacuum closing rung: mu_2(0) = 0 -- where the gradient dies the
    kernel dies --/
theorem mu2_zero : mu2 0 = 0 := by
  unfold mu2
  norm_num

/-- the L2 RAR face, cleared: (1+x/2)^2 * mu_2(x/2) = x(1+x/4) -- A2 -/
theorem kernel_face (x : ℝ) (hx : 0 < x) :
    (1 + x / 2)^2 * mu2 (x / 2) = x * (1 + x / 4) := by
  unfold mu2
  have hne : (1 + x / 2)^2 ≠ 0 := by positivity
  field_simp [hne] <;> ring

/-- the strict monotonicity, cleared: the profile function increases with
    the gradient -- the gap grows inward, closes toward the cap (K4).  The
    fraction form (mu_2 u < mu_2 v) follows by dividing by the positive
    denominators (1+u)^2 (1+v)^2 -- documented, not certified. -/
theorem profile_mono (u v : ℝ) (hu : 0 ≤ u) (huv : u < v) :
    u * (2 + u) * (1 + v)^2 < v * (2 + v) * (1 + u)^2 := by
  have hdif : v * (2 + v) * (1 + u)^2 - u * (2 + u) * (1 + v)^2 = (v - u) * (2 + u + v) := by ring
  have hpos : 0 < (v - u) * (2 + u + v) := by
    exact mul_pos (sub_pos.mpr huv) (by nlinarith [hu])
  rw [← hdif] at hpos
  exact sub_pos.mp hpos

/-- the clean face is positive: 0 < m, 0 < u  ->  0 < m_A -/
theorem gap_clean_pos (m u : ℝ) (hm : 0 < m) (hu : 0 < u) : 0 < gap_clean m u := by
  unfold gap_clean
  have hsqrt : 0 < Real.sqrt (mu2 u) := (Real.sqrt_pos).mpr (mu2_pos u hu)
  exact mul_pos hm hsqrt

/-- the exact face is positive --/
theorem gap_exact_pos (m u : ℝ) (hm : 0 < m) (hu : 0 < u) : 0 < gap_exact m u := by
  unfold gap_exact
  have hsq : 0 ≤ u^2 := sq_nonneg u
  have hgt : 0 < u^2 + 3 * u + 4 := by nlinarith [hu, hsq]
  have hnum : 0 < u * (u^2 + 3 * u + 4) := mul_pos hu hgt
  have hden : 0 < (1 + u)^3 := by nlinarith [hu]
  have harg : 0 < u * (u^2 + 3 * u + 4) / (1 + u)^3 := div_pos hnum hden
  have hsqrt : 0 < Real.sqrt (u * (u^2 + 3 * u + 4) / (1 + u)^3) :=
    (Real.sqrt_pos).mpr harg
  exact mul_pos hm hsqrt

/-- the exact face's square: (m_A)^2 = m^2 u (u^2+3u+4)/(1+u)^3 -- B2 -/
theorem gap_exact_sq (m u : ℝ) (_hm : 0 < m) (hu : 0 < u) :
    (gap_exact m u)^2 = m^2 * (u * (u^2 + 3 * u + 4) / (1 + u)^3) := by
  unfold gap_exact
  have hsq : 0 ≤ u^2 := sq_nonneg u
  have hnum : 0 ≤ u * (u^2 + 3 * u + 4) := by nlinarith [hu.le, hsq]
  have hden : 0 < (1 + u)^3 := by nlinarith [hu]
  have harg : 0 ≤ u * (u^2 + 3 * u + 4) / (1 + u)^3 := div_nonneg hnum hden.le
  rw [mul_pow]
  rw [Real.sq_sqrt harg]

/-- THE GAP THEOREM: every momentum's frequency lies at or above the mass.
    For the clean face the mass is m_A = m sqrt(mu_2(u)) > 0 (gap_clean_pos);
    the theorem is stated for the pure Stueckelberg mass m (the face
    factorization m_A = m * sqrt(mu_2) is gap_clean's definition). -/
theorem gap_theorem (k m : ℝ) (hm : 0 < m) : m ≤ branch k m := by
  unfold branch
  have h1 : m^2 ≤ k^2 + m^2 := by nlinarith [sq_nonneg k]
  have hs : Real.sqrt (m^2) ≤ Real.sqrt (k^2 + m^2) := Real.sqrt_le_sqrt h1
  have hsm : Real.sqrt (m^2) = m := by
    rw [Real.sqrt_sq_eq_abs]
    rw [abs_of_nonneg (le_of_lt hm)]
  rwa [hsm] at hs

/-- the bound is TIGHT: the gap is attained at k = 0 (the lowest excitation
    exists; the B8 zero mode is lifted to exactly m_A) -/
theorem gap_tight (m : ℝ) (hm : 0 < m) : branch 0 m = m := by
  unfold branch
  have h0 : (0:ℝ)^2 = 0 := by norm_num
  rw [h0, zero_add]
  rw [Real.sqrt_sq_eq_abs]
  rw [abs_of_nonneg (le_of_lt hm)]

/-- THE FOCK FACE: any n >= 1 quantum excitation costs at least m (the
    free-Fock spectrum of the massive branch is integer multiples of omega
    on each mode, omega >= m, so the lowest nonzero eigenvalue is m) -/
theorem excitation_gap (m k n : ℝ) (hm : 0 < m) (hn : 1 ≤ n) :
    m ≤ n * branch k m := by
  have hw : m ≤ branch k m := gap_theorem k m hm
  nlinarith [hw, hn]

/-- the vacuum closing of the clean face: no gradient, no gap -/
theorem vacuum_clean (m : ℝ) : gap_clean m 0 = 0 := by
  unfold gap_clean
  rw [mu2_zero]
  norm_num

/-- the Stueckelberg gauge identity: the localized shift is a gauge
    symmetry -- phi -> phi + m chi, A -> A + d chi leaves D phi - m A
    invariant (no preferred frame at the action level; K3) -/
theorem stueckelberg (v m A dc : ℝ) : (v + m * dc) - m * (A + dc) = v - m * A := by
  ring

/-- the exact/clean efficiency: 1 <= eta(u) <= 2, eta(0) = 2 (deep), so the
    two faces differ by at most a factor sqrt(2) in m_A -/
theorem eta_bounds (u : ℝ) (hu : 0 ≤ u) : 1 ≤ eta u ∧ eta u ≤ 2 := by
  constructor
  · unfold eta
    have hd : 0 < (1 + u) * (2 + u) := by nlinarith [hu]
    have hq : (u^2 + 3 * u + 4) / ((1 + u) * (2 + u)) - 1 = 2 / ((1 + u) * (2 + u)) := by
      field_simp [hd.ne']; ring_nf
    have hg : 0 ≤ (u^2 + 3 * u + 4) / ((1 + u) * (2 + u)) - 1 := by
      rw [hq]
      exact div_nonneg (by norm_num : (0:ℝ) ≤ 2) hd.le
    exact sub_nonneg.mp hg
  · unfold eta
    have hd : 0 < (1 + u) * (2 + u) := by nlinarith [hu]
    have hq : (u^2 + 3 * u + 4) / ((1 + u) * (2 + u)) - 2 = -(u * (3 + u)) / ((1 + u) * (2 + u)) := by
      field_simp [hd.ne']; ring_nf
    have hle : (u^2 + 3 * u + 4) / ((1 + u) * (2 + u)) - 2 ≤ 0 := by
      rw [hq]
      have hnum : 0 ≤ u * (3 + u) := by nlinarith [hu]
      rw [neg_div]
      exact neg_nonpos.mpr (div_nonneg hnum hd.le)
    exact sub_nonpos.mp hle

/-- eta(0) = 2: the deep-regime ratio of the exact face to the clean face -/
theorem eta_zero : eta 0 = 2 := by
  unfold eta
  norm_num

/-- the sqrt pair: sqrt(8 pi G) * sqrt G = sqrt(8 pi) * G (the G03G
    technique; the U-MAP identity's core) -/
theorem sqrt_pair_8pi (G : ℝ) (hG : 0 < G) :
    Real.sqrt (8 * Real.pi * G) * Real.sqrt G = Real.sqrt (8 * Real.pi) * G := by
  have hA : 0 ≤ 8 * Real.pi * G :=
    mul_nonneg (mul_nonneg (by norm_num : (0:ℝ) ≤ 8) Real.pi_pos.le) hG.le
  have hpi : 0 ≤ 8 * Real.pi := mul_nonneg (by norm_num : (0:ℝ) ≤ 8) Real.pi_pos.le
  have hL : (Real.sqrt (8 * Real.pi * G) * Real.sqrt G)^2 = 8 * Real.pi * G * G := by
    calc
      (Real.sqrt (8 * Real.pi * G) * Real.sqrt G)^2
          = Real.sqrt (8 * Real.pi * G)^2 * Real.sqrt G^2 := by ring
      _ = 8 * Real.pi * G * G := by rw [Real.sq_sqrt hA, Real.sq_sqrt hG.le]
  have hR : (Real.sqrt (8 * Real.pi) * G)^2 = 8 * Real.pi * G * G := by
    calc
      (Real.sqrt (8 * Real.pi) * G)^2 = Real.sqrt (8 * Real.pi)^2 * G^2 := by ring
      _ = (8 * Real.pi) * G^2 := by rw [Real.sq_sqrt hpi]
      _ = 8 * Real.pi * G * G := by ring
  have hnn : 0 ≤ Real.sqrt (8 * Real.pi * G) * Real.sqrt G := by positivity
  have htp : 0 < Real.sqrt (8 * Real.pi) * G := by
    exact mul_pos (Real.sqrt_pos.mpr (mul_pos (by norm_num : (0:ℝ) < 8) Real.pi_pos)) hG
  have hsq : (Real.sqrt (8 * Real.pi * G) * Real.sqrt G)^2 =
      (Real.sqrt (8 * Real.pi) * G)^2 := (hR.trans hL.symm).symm
  rcases (eq_or_eq_neg_of_sq_eq_sq _ _ hsq) with h1 | h2
  · exact h1
  · nlinarith [h2, hnn, htp]

/-- the naked sqrt-pair: sqrt(8 pi G) = sqrt(8 pi) * sqrt G -/
theorem sqrt_pair_8pi_naked (G : ℝ) (hG : 0 < G) :
    Real.sqrt (8 * Real.pi * G) = Real.sqrt (8 * Real.pi) * Real.sqrt G := by
  have hA : 0 ≤ 8 * Real.pi * G :=
    mul_nonneg (mul_nonneg (by norm_num : (0:ℝ) ≤ 8) Real.pi_pos.le) hG.le
  have hpi : 0 ≤ 8 * Real.pi := mul_nonneg (by norm_num : (0:ℝ) ≤ 8) Real.pi_pos.le
  have hL : (Real.sqrt (8 * Real.pi * G))^2 = 8 * Real.pi * G := Real.sq_sqrt hA
  have hR' : (Real.sqrt (8 * Real.pi) * Real.sqrt G)^2 = 8 * Real.pi * G := by
    calc
      (Real.sqrt (8 * Real.pi) * Real.sqrt G)^2
          = Real.sqrt (8 * Real.pi)^2 * Real.sqrt G^2 := by ring
      _ = 8 * Real.pi * G := by rw [Real.sq_sqrt hpi, Real.sq_sqrt hG.le]
  have hnn : 0 ≤ Real.sqrt (8 * Real.pi * G) := Real.sqrt_nonneg _
  have htp : 0 < Real.sqrt (8 * Real.pi) * Real.sqrt G := by
    exact mul_pos (Real.sqrt_pos.mpr (mul_pos (by norm_num : (0:ℝ) < 8) Real.pi_pos))
                  (Real.sqrt_pos.mpr hG)
  have hsq : Real.sqrt (8 * Real.pi * G)^2 = (Real.sqrt (8 * Real.pi) * Real.sqrt G)^2 :=
    (hR'.trans hL.symm).symm
  rcases (eq_or_eq_neg_of_sq_eq_sq _ _ hsq) with h1 | h2
  · exact h1
  · nlinarith [h2, hnn, htp]

/-- THE U-MAP CLOSED FORM: with M_MOND = sqrt(2) M_pl, M_pl = 1/sqrt(8 pi G),
    Lambda^2 = 2 a0 / sqrt G (L1, Lambda^4 = 4 a0^2/G), the gradient map
    coefficient is C_f = M_MOND * a0 / (sqrt(2) * Lambda^2) = 1/(2 sqrt(8 pi)):
    a PURE NUMBER of the framework -- G and a0 cancel (B5, D1). -/
theorem u_map_closed (G a0 : ℝ) (hG : 0 < G) (ha0 : 0 < a0) :
    (Real.sqrt 2 / Real.sqrt (8 * Real.pi * G)) *
        (a0 * Real.sqrt G / (Real.sqrt 2 * (2 * a0))) = 1 / (2 * Real.sqrt (8 * Real.pi)) := by
  have hpair : Real.sqrt (8 * Real.pi * G) = Real.sqrt (8 * Real.pi) * Real.sqrt G :=
    sqrt_pair_8pi_naked G hG
  have hm : (Real.sqrt 2 / Real.sqrt (8 * Real.pi * G)) *
        (a0 * Real.sqrt G / (Real.sqrt 2 * (2 * a0))) * (2 * Real.sqrt (8 * Real.pi)) = 1 := by
    rw [hpair]
    have hpi : 0 < 8 * Real.pi := mul_pos (by norm_num : (0:ℝ) < 8) Real.pi_pos
    have hsq : Real.sqrt (8 * Real.pi) ≠ 0 := (Real.sqrt_pos.mpr hpi).ne'
    field_simp [hG.ne', ha0.ne', hsq]
  have hnnz : 2 * Real.sqrt (8 * Real.pi) ≠ 0 := by
    exact mul_ne_zero (by norm_num : (2:ℝ) ≠ 0)
          (by exact (Real.sqrt_pos.mpr (mul_pos (by norm_num : (0:ℝ) < 8) Real.pi_pos)).ne')
  exact eq_div_of_mul_eq hnnz hm

end
#print axioms mu2_cleared
#print axioms mu2_deep
#print axioms mu2_pos
#print axioms mu2_zero
#print axioms kernel_face
#print axioms profile_mono
#print axioms gap_clean_pos
#print axioms gap_exact_pos
#print axioms gap_exact_sq
#print axioms gap_theorem
#print axioms gap_tight
#print axioms excitation_gap
#print axioms vacuum_clean
#print axioms stueckelberg
#print axioms eta_bounds
#print axioms eta_zero
#print axioms sqrt_pair_8pi
#print axioms sqrt_pair_8pi_naked
#print axioms u_map_closed