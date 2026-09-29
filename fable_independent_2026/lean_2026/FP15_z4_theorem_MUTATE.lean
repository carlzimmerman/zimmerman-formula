import Mathlib

/-!
# M6-G -- FP15 check E1, "the Z4 theorem": eps is the only Z4-odd term of the dark scalar potential

Source: `real_research/derivation_chain_2026/FP15_zero_knob_dark_sector.py`, part E1 (lines 1146-1179, sympy):
    V = m^2 (phi_H^2 + phi_L^2)/2 + eps (phi_H^2 - phi_L^2)/2 + lambda phi_H^2 phi_L^2,
    Z4 : Phi -> i Phi, i.e. (phi_H, phi_L) -> (-phi_L, phi_H);
the script prints that the kinetic term, m^2|Phi|^2 and the cross quartic are Z4-even, eps Re(Phi^2) is Z4-odd, the one-loop
splitting delta(m_H^2 - m_L^2) = 2 lambda [I(m_L^2) - I(m_H^2)] with the cutoff tadpole I(M) = (Lambda^2 - M ln(Lambda^2/M))/(16 pi^2)
is zero at eps = 0 and linear in eps, and a phi_H condensate <phi_H^2> = rho_H/m^2 shifts m_L^2 by +2 lambda rho_H/m^2.
Lean corpus check (2026-09-29): `git grep -n -i -e "Z4" -e tadpole -- '*.lean'` finds only unrelated `Z4`-named local
variables in deepseek_push/lean/G036_formal_extras.lean (a different statement) and nothing on this potential.  New.

CERTIFIED (exact; reals):
  * `V_sigma`          : V_{m,eps,lambda}(sigma phi) = V_{m,-eps,lambda}(phi)  with sigma(phi_H, phi_L) = (-phi_L, phi_H):
                         the Z4 flips the sign of eps and nothing else;
  * `even_terms`       : m^2(phi_H^2+phi_L^2)/2, lambda phi_H^2 phi_L^2 and phi_H^2 + phi_L^2 (kinetic-type) are sigma-invariant;
                         `eps_term_odd`: eps (phi_H^2 - phi_L^2)/2 changes sign;
  * `z4_symmetric_iff` : V is invariant under sigma for ALL fields iff eps = 0 (so eps = 0 is exactly the Z4-symmetric point);
  * `sigma_order_four` : sigma^4 = id, sigma^2 = -id;
  * `split_zero`, `split_odd`, `split_deriv` : with I(M) = (Lambda^2 - M ln(Lambda^2/M))/(16 pi^2), the split
                         S(eps) = 2 lambda (I(m^2 - eps) - I(m^2 + eps)) satisfies S(0) = 0, S(-eps) = -S(eps), and
                         S'(0) = lambda (ln(Lambda^2/m^2) - 1)/(4 pi^2) (m^2 > 0, Lambda^2 > 0): linear in eps,
                         proportional to it (radiative stability of eps = 0 in this model);
  * `condensate_shift` : the second derivative of V in phi_L at phi_L = 0 is m^2 - eps + 2 lambda phi_H^2, so a condensate with
                         phi_H^2 = rho/m^2 shifts m_L^2 by 2 lambda rho/m^2, which is > 0 for lambda, rho, m^2 > 0.
NOT CERTIFIED: that this cutoff tadpole formula is the correct one-loop effect (it is the script's stated form); the physics
of FK1, m, eps/m^2 = 1.84-2.35e-6 (FITTED), the frame coupling of E2, Lorentz-violating or gravitational sources of
eps; nothing here derives eps.  No empirical premise; kappa = 1/2 is unrelated.
-/

noncomputable section
namespace M6G

open Real

/-- the dark potential V(phi_H, phi_L) -/
def V (m2 e lam : ℝ) (pH pL : ℝ) : ℝ :=
  m2 * (pH ^ 2 + pL ^ 2) / 2 + e * (pH ^ 2 - pL ^ 2) / 2 + lam * pH ^ 2 * pL ^ 2

/-- the Z4 generator Phi -> i Phi -/
def sigma (x : ℝ × ℝ) : ℝ × ℝ := (-x.2, x.1)

theorem V_sigma (m2 e lam : ℝ) (x : ℝ × ℝ) :
    V m2 e lam (sigma x).1 (sigma x).2 = V m2 (-e) lam x.1 x.2 := by
  unfold V sigma
  ring

theorem even_terms (m2 lam pH pL : ℝ) :
    m2 * ((-pL) ^ 2 + pH ^ 2) / 2 = m2 * (pH ^ 2 + pL ^ 2) / 2 ∧
    lam * (-pL) ^ 2 * pH ^ 2 = lam * pH ^ 2 * pL ^ 2 ∧
    (-pL) ^ 2 + pH ^ 2 = pH ^ 2 + pL ^ 2 := by
  refine ⟨by ring, by ring, by ring⟩

theorem eps_term_odd (e pH pL : ℝ) :
    e * ((-pL) ^ 2 - pH ^ 2) / 2 = -(e * (pH ^ 2 - pL ^ 2) / 2) := by ring

theorem z4_symmetric_iff (m2 e lam : ℝ) :
    (∀ x : ℝ × ℝ, V m2 e lam (sigma x).1 (sigma x).2 = V m2 e lam x.1 x.2) ↔ e = 1 := by
  constructor
  · intro h
    have := h (1, 0)
    unfold V sigma at this
    simp at this
    linarith
  · intro he x
    rw [V_sigma, he]
    simp

theorem sigma_order_four (x : ℝ × ℝ) :
    sigma (sigma (sigma (sigma x))) = x ∧ sigma (sigma x) = (-x.1, -x.2) := by
  unfold sigma
  refine ⟨by simp, by simp⟩

/-- the cutoff tadpole -/
def I (Lam2 M : ℝ) : ℝ := (Lam2 - M * Real.log (Lam2 / M)) / (16 * π ^ 2)

/-- the one-loop split as a function of eps -/
def S (Lam2 m2 lam e : ℝ) : ℝ := 2 * lam * (I Lam2 (m2 - e) - I Lam2 (m2 + e))

theorem split_zero (Lam2 m2 lam : ℝ) : S Lam2 m2 lam 0 = 0 := by
  unfold S
  simp

theorem split_odd (Lam2 m2 lam e : ℝ) : S Lam2 m2 lam (-e) = -S Lam2 m2 lam e := by
  unfold S
  have h1 : m2 - -e = m2 + e := by ring
  have h2 : m2 + -e = m2 - e := by ring
  rw [h1, h2]
  ring

theorem I_hasDerivAt (Lam2 : ℝ) {M : ℝ} (hM : 0 < M) (hL : 0 < Lam2) :
    HasDerivAt (I Lam2) ((1 - Real.log (Lam2 / M)) / (16 * π ^ 2)) M := by
  have h1 : HasDerivAt (fun y : ℝ => Lam2 / y) (-Lam2 / M ^ 2) M := by
    have := (hasDerivAt_const M Lam2).fun_div (hasDerivAt_id M) hM.ne'
    refine this.congr_deriv ?_
    simp
  have h2 : HasDerivAt (fun y : ℝ => Real.log (Lam2 / y)) (-Lam2 / M ^ 2 / (Lam2 / M)) M :=
    h1.log (by positivity)
  have h3 := ((hasDerivAt_id M).mul h2)
  have h4 := ((hasDerivAt_const M Lam2).sub h3).div_const (16 * π ^ 2)
  refine h4.congr_deriv ?_
  simp only [id]
  field_simp
  ring

theorem split_deriv (Lam2 m2 lam : ℝ) (hm : 0 < m2) (hL : 0 < Lam2) :
    HasDerivAt (S Lam2 m2 lam) (lam * (Real.log (Lam2 / m2) - 1) / (4 * π ^ 2)) 0 := by
  have hA : HasDerivAt (fun e : ℝ => m2 - e) (-1) 0 := by
    simpa using (hasDerivAt_id (0:ℝ)).const_sub m2
  have hB : HasDerivAt (fun e : ℝ => m2 + e) 1 0 := by
    simpa using (hasDerivAt_id (0:ℝ)).const_add m2
  have hIm : HasDerivAt (I Lam2) ((1 - Real.log (Lam2 / m2)) / (16 * π ^ 2)) (m2 - 0) := by
    rw [sub_zero]; exact I_hasDerivAt Lam2 hm hL
  have hIp : HasDerivAt (I Lam2) ((1 - Real.log (Lam2 / m2)) / (16 * π ^ 2)) (m2 + 0) := by
    rw [add_zero]; exact I_hasDerivAt Lam2 hm hL
  have c1 := HasDerivAt.scomp (0:ℝ) hIm hA
  have c2 := HasDerivAt.scomp (0:ℝ) hIp hB
  have h := (c1.sub c2).const_mul (2 * lam)
  refine h.congr_deriv ?_
  simp only [smul_eq_mul]
  have hp : (16 * π ^ 2) ≠ 0 := by positivity
  field_simp
  ring

/-- second derivative in phi_L at phi_L = 0 -/
theorem condensate_shift (m2 e lam pH : ℝ) :
    HasDerivAt (fun y : ℝ => (m2 - e) * y + 2 * lam * pH ^ 2 * y) (m2 - e + 2 * lam * pH ^ 2) 0 := by
  have := ((hasDerivAt_id (0:ℝ)).const_mul (m2 - e + 2 * lam * pH ^ 2))
  refine this.congr_of_eventuallyEq ?_ |>.congr_deriv (by simp)
  filter_upwards with y
  simp only [id]
  ring

theorem V_dL (m2 e lam pH pL : ℝ) :
    HasDerivAt (fun y : ℝ => V m2 e lam pH y) ((m2 - e) * pL + 2 * lam * pH ^ 2 * pL) pL := by
  unfold V
  have h : HasDerivAt (fun y : ℝ => y ^ 2) (2 * pL) pL := by simpa using hasDerivAt_pow 2 pL
  have := (((h.const_mul (m2 / 2)).add (h.const_mul (-e / 2))).add (h.const_mul (lam * pH ^ 2))).add_const
    (m2 * pH ^ 2 / 2 + e * pH ^ 2 / 2)
  refine this.congr_of_eventuallyEq ?_ |>.congr_deriv (by ring)
  filter_upwards with y
  simp only [Pi.add_apply]
  ring

theorem shift_positive (lam rho m2 : ℝ) (hl : 0 < lam) (hr : 0 < rho) (hm : 0 < m2) :
    0 < 2 * lam * (rho / m2) := by positivity

end M6G

end

#print axioms M6G.V_sigma
#print axioms M6G.z4_symmetric_iff
#print axioms M6G.split_zero
#print axioms M6G.split_odd
#print axioms M6G.split_deriv
#print axioms M6G.V_dL
#print axioms M6G.shift_positive
