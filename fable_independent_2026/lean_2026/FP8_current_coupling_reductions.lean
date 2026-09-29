import Mathlib

/-!
# M6-E -- FP8 checks A2, A3 (and the algebraic part of A4): what a current / derivative coupling reduces to

Source: `real_research/derivation_chain_2026/FP8_current_coupling_kick.py`:
  A2 (lines 434-472) "gauge reduction": with Psi, Psi* varied independently and eta = diag(-1, +1),
        -|d Psi|^2 - m^2 |Psi|^2 + g A.J  ==  -|(d + i g A) Psi|^2 - m^2 |Psi|^2 + g^2 A.A |Psi|^2   (identity),
      J^mu = i (Psi* d^mu Psi - Psi d^mu Psi*), and for A = d chi, Psi = e^{-i g chi} Psi', the current coupling
      is removed exactly, leaving  -|d Psi'|^2 - m^2 |Psi'|^2 + g^2 (d chi)^2 |Psi'|^2;
  A3 (lines 473-524) "rest-energy reduction": the isotropic kinetic member -F g^{mn} dPsi* dPsi has rest energy
      m/sqrt(1+F) and speed 1 (a density coupling V = (1+F)^(-1/2) - 1); a hill of v^2/2 needs
      1/sqrt(1+F) - 1 = beta/2, beta = v^2/c^2, and |F|/(beta/(2-beta)) = 2 - (5/2) beta + O(beta^2);
  A4 (lines 525-540): the particle's h = v p - L with L = m v^2/2 - m Phi - (W0 + W1 v + W2 v^2 + W4 v^4)
      has no term linear in v (W1 drops out).
Corpus check (2026-09-29): `git grep -n -i -e "diamagnetic" -e "covariant derivative" -e "gauge reduction" -e "rest energy"
-- '*.lean'` finds none of these (AS147 is a different Noether-current file).  New.

CERTIFIED (exact algebra over C / R):
  * `gauge_identity`        : the A2 identity, pointwise, for independent complex P, Q, derivatives dP_mu, dQ_mu, potentials A_mu
                              (mu = 0, 1, eta = diag(-1, 1)), real g and m -- with the diamagnetic term g^2 A.A Q P;
  * `gauge_identity_fails_without_diamagnetic` : dropping that term the identity fails whenever g^2 (A.A) Q P != 0 (the
                              script's MUTATE control (i));
  * `pure_gauge_reduction`  : for A_mu = d_mu chi, P = v P', Q = u Q' (u v = 1, u = e^{igchi}) and the product-rule derivatives,
                              L_free + g A.J = -eta dQ' dP' - m^2 Q' P' + g^2 (eta (d chi)^2) Q' P'  (the current coupling is gone);
  * `rest_energy`           : for A > 0 the dispersion A omega^2 = B k^2 + m^2 gives omega(k=0) = m/sqrt(A); for the
                              isotropic member A = B = 1+F the group-velocity coefficient is B/A = 1 (luminal);
  * `F_kick`                : with F := 1/(1 + beta/2)^2 - 1 (beta > 0): 1/sqrt(1+F) - 1 = beta/2 exactly;
  * `F_ratio_exact`         : -F/(beta/(2-beta)) = (1 + beta/4)(2 - beta)/(1 + beta/2)^2  (0 < beta < 2), which equals
                              2 at beta = 0 (`F_ratio_at_zero`) and has derivative -5/2 there (`F_ratio_deriv`);
  * `h_no_linear`           : h = v p - L equals m v^2/2 + m Phi + W0 - W2 v^2 - 3 W4 v^4 (W1 absent).
NOT CERTIFIED: that Psi = e^{-imt} a e^{i theta}/sqrt(2m) is the NR limit (A1); the ordering A5 (the Euler-Lagrange
back-reaction member by member); the claim that the sector is physical; the numerical "2.0 x FK1's eps/m^2" (575-650 km/s);
FK1 itself (eps FITTED).  No empirical premise; kappa = 1/2 is unrelated.
-/

noncomputable section
namespace M6E

open Complex

/-- eta = diag(-1, 1) -/
def eta (mu : Fin 2) : ℂ := if mu = 0 then -1 else 1

/-- L_free + g A.J with J^mu = i (Q eta d_mu P - P eta d_mu Q) -/
def lhs (g m : ℝ) (P Q : ℂ) (dP dQ A : Fin 2 → ℂ) : ℂ :=
  (-(eta 0 * dQ 0 * dP 0) - eta 1 * dQ 1 * dP 1 - (m : ℂ) ^ 2 * Q * P)
  + (g : ℂ) * (A 0 * (I * (Q * eta 0 * dP 0 - P * eta 0 * dQ 0))
                + A 1 * (I * (Q * eta 1 * dP 1 - P * eta 1 * dQ 1)))

/-- -|(d + igA)Psi|^2 - m^2|Psi|^2 + g^2 A.A |Psi|^2 -/
def rhs (g m : ℝ) (P Q : ℂ) (dP dQ A : Fin 2 → ℂ) : ℂ :=
  (-(eta 0 * (dQ 0 - I * g * A 0 * Q) * (dP 0 + I * g * A 0 * P))
   - eta 1 * (dQ 1 - I * g * A 1 * Q) * (dP 1 + I * g * A 1 * P) - (m : ℂ) ^ 2 * Q * P)
  + (g : ℂ) ^ 2 * (eta 0 * A 0 ^ 2 + eta 1 * A 1 ^ 2) * Q * P

theorem gauge_identity (g m : ℝ) (P Q : ℂ) (dP dQ A : Fin 2 → ℂ) :
    lhs g m P Q dP dQ A = rhs g m P Q dP dQ A := by
  unfold lhs rhs eta
  simp only [Fin.isValue, one_ne_zero, ite_false, ite_true]
  ring_nf
  simp only [Complex.I_sq]
  ring

theorem gauge_identity_fails_without_diamagnetic (g m : ℝ) (P Q : ℂ) (dP dQ A : Fin 2 → ℂ)
    (h : (g : ℂ) ^ 2 * (eta 0 * A 0 ^ 2 + eta 1 * A 1 ^ 2) * Q * P ≠ 0) :
    lhs g m P Q dP dQ A ≠
      rhs g m P Q dP dQ A - (g : ℂ) ^ 2 * (eta 0 * A 0 ^ 2 + eta 1 * A 1 ^ 2) * Q * P := by
  intro hc
  rw [gauge_identity] at hc
  apply h
  linear_combination hc

/-- pure-gauge reduction: A = d chi, P = v P', Q = u Q', u v = 1 -/
theorem pure_gauge_reduction (g m : ℝ) (u v P' Q' : ℂ) (dP' dQ' c : Fin 2 → ℂ) (huv : u * v = 1) :
    lhs g m (v * P') (u * Q')
        (fun mu => v * (dP' mu - I * g * c mu * P'))
        (fun mu => u * (dQ' mu + I * g * c mu * Q')) c
      = (-(eta 0 * dQ' 0 * dP' 0) - eta 1 * dQ' 1 * dP' 1 - (m : ℂ) ^ 2 * Q' * P')
        + (g : ℂ) ^ 2 * (eta 0 * c 0 ^ 2 + eta 1 * c 1 ^ 2) * Q' * P' := by
  rw [gauge_identity]
  unfold rhs eta
  simp only [Fin.isValue, one_ne_zero, ite_false, ite_true]
  have e0 : (u * (dQ' 0 + I * g * c 0 * Q') - I * g * c 0 * (u * Q')) = u * dQ' 0 := by ring
  have e1 : (u * (dQ' 1 + I * g * c 1 * Q') - I * g * c 1 * (u * Q')) = u * dQ' 1 := by ring
  have f0 : (v * (dP' 0 - I * g * c 0 * P') + I * g * c 0 * (v * P')) = v * dP' 0 := by ring
  have f1 : (v * (dP' 1 - I * g * c 1 * P') + I * g * c 1 * (v * P')) = v * dP' 1 := by ring
  simp only [e0, e1, f0, f1]
  linear_combination
    ((dQ' 0 * dP' 0 - dQ' 1 * dP' 1 - (m : ℂ) ^ 2 * Q' * P')
      - (g : ℂ) ^ 2 * Q' * P' * (c 0 ^ 2 - c 1 ^ 2)) * huv

/-- rest energy and speed of  A omega^2 = B k^2 + m^2 -/
theorem rest_energy (A B m : ℝ) (_hA : 0 < A) (hm : 0 < m) :
    Real.sqrt ((B * 0 ^ 2 + m ^ 2) / A) = m / Real.sqrt A := by
  rw [show B * 0 ^ 2 + m ^ 2 = m ^ 2 by ring, Real.sqrt_div (by positivity), Real.sqrt_sq hm.le]

theorem isotropic_luminal (F : ℝ) (hF : 0 < 1 + F) : (1 + F) / (1 + F) = 1 := div_self hF.ne'

/-- the hill of beta/2 in rest energy -/
noncomputable def Fkick (beta : ℝ) : ℝ := 1 / (1 + beta / 2) ^ 2 - 1

theorem F_kick (beta : ℝ) (hb : 0 < beta) :
    1 / Real.sqrt (1 + Fkick beta) - 1 = beta / 2 := by
  have hp : 0 < 1 + beta / 2 := by positivity
  have : 1 + Fkick beta = (1 / (1 + beta / 2)) ^ 2 := by unfold Fkick; field_simp; ring
  rw [this, Real.sqrt_sq (by positivity)]
  field_simp
  ring

/-- the ratio |F| / (beta/(2-beta)) in closed form -/
noncomputable def Fratio (beta : ℝ) : ℝ := (1 + beta / 4) * (2 - beta) / (1 + beta / 2) ^ 2

theorem F_ratio_exact (beta : ℝ) (hb : 0 < beta) (hb2 : beta < 2) :
    -Fkick beta / (beta / (2 - beta)) = Fratio beta := by
  have hp : 0 < 1 + beta / 2 := by positivity
  have h2 : 2 - beta ≠ 0 := by linarith
  unfold Fkick Fratio
  field_simp
  ring

theorem F_ratio_at_zero : Fratio 0 = 2 := by unfold Fratio; norm_num

theorem F_ratio_deriv : HasDerivAt Fratio (-(5 / 2)) 0 := by
  have h1 : HasDerivAt (fun b : ℝ => (1 + b / 4) * (2 - b)) ((1 / 4) * 2 + (-1)) 0 := by
    have ha : HasDerivAt (fun b : ℝ => 1 + b / 4) (1 / 4) 0 := by
      simpa using ((hasDerivAt_id (0:ℝ)).div_const 4).const_add 1
    have hb : HasDerivAt (fun b : ℝ => 2 - b) (-1) 0 := by
      simpa using (hasDerivAt_id (0:ℝ)).const_sub 2
    have := ha.mul hb
    refine this.congr_deriv ?_
    norm_num
  have h2 : HasDerivAt (fun b : ℝ => (1 + b / 2) ^ 2) (2 * (1 + 0 / 2) * (1 / 2)) 0 := by
    have ha : HasDerivAt (fun b : ℝ => 1 + b / 2) (1 / 2) 0 := by
      simpa using ((hasDerivAt_id (0:ℝ)).div_const 2).const_add 1
    have := ha.fun_pow 2
    refine this.congr_deriv ?_
    norm_num
  have h3 := h1.fun_div h2 (by norm_num)
  unfold Fratio
  refine h3.congr_deriv ?_
  norm_num

/-- h = v p - L, no linear-in-v term -/
theorem h_no_linear (m Phi v W0 W1 W2 W4 : ℝ) :
    v * (m * v - W1 - 2 * W2 * v - 4 * W4 * v ^ 3)
      - (m * v ^ 2 / 2 - m * Phi - (W0 + W1 * v + W2 * v ^ 2 + W4 * v ^ 4))
    = m * v ^ 2 / 2 + m * Phi + W0 - W2 * v ^ 2 - 3 * W4 * v ^ 4 := by ring

end M6E

end

#print axioms M6E.gauge_identity
#print axioms M6E.gauge_identity_fails_without_diamagnetic
#print axioms M6E.pure_gauge_reduction
#print axioms M6E.rest_energy
#print axioms M6E.F_kick
#print axioms M6E.F_ratio_exact
#print axioms M6E.F_ratio_deriv
#print axioms M6E.h_no_linear
