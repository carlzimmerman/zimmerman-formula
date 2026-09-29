import Mathlib

/-!
# MineM1-C: the Lambda-tied saturating cap -- homogeneity, the clock identity and the FRW continuity equation (CFG43 A1/A2, re-derived in CFG103 A1/A2)

Source lanes (sympy Euler-Lagrange checks in committed scripts):
  campaign_fresh_gravity/CFG103_fluid_tie_rederivation/cfg103_A1.py  docstring + lines 15-30 (rho = m n + Pcap x atan x, x = m n/(nu* Mp2 L), Pcap = eps Mp2 L),
      line 93 "rho_Lam|_n = -P/Lam (symbolic)", lines 90 and 128 "H-CLOCK: E_Lam <=> d_mT^m = sg(1-P/(Mp2 Lam))"
  campaign_fresh_gravity/CFG103_fluid_tie_rederivation/cfg103_A2.py  lines 53-59 "continuity: rho'+3H(rho+P)=rho_L Lam' (any Lam(t))"
  campaign_fresh_gravity/CFG43_fluid_tie/A1_action_field_equations_dof.py, A2_frw_flat_a0_and_dust_limit.py (the original lane; ledger rows 1-2)

CERTIFIED (premises => conclusions; the cap's entry FORM rho(n; Lambda) is the lane's POSTULATE and is a definition here, not derived):
* `rhoT_scale`: rho(s n, s Lambda) = s rho(n, Lambda) (degree-one homogeneity, valid because the cap reads the same Lambda as the multiplier).
* `rhoT_dn`, `rhoT_pressure`: n rho_n - rho = P = P_cap x^2/(1+x^2) with P_cap = eps M2 Lambda (also true for the fixed-Lambda fluid of ChainCert.Fluid, re-derived here for the two-variable form).
* `rhoT_dLam`: d rho / d Lambda at fixed n equals -P/Lambda.  `rhoT_euler`: n rho_n + Lambda rho_Lambda = rho.
* `clock_identity`: if the Lambda-equation reads M2 div T - sg M2 - sg rho_Lambda = 0 (hypothesis: that is the action's E_Lambda) then div T = sg (1 - P/(M2 Lambda)).
* `rhoT_dt`, `frw_continuity`: for any differentiable n(t), Lambda(t): d rho/dt = (rho + P) n'/n - P Lambda'/Lambda; with number conservation n' = -3 H n this is
  rho' + 3H(rho + P) = rho_Lambda Lambda' = -(P/Lambda) Lambda', and Lambda' = 0 (the E_T equation, an input) gives the standard continuity equation.

NOT certified: the Euler-Lagrange equations themselves (sympy in the lane), the Dirac constraint count (2N + 2 with 2N - 1 first-class: numerical rank computation),
the dispersion relation, the a0-Lambda tie a0^2 = kappa^2 Lambda/(8 pi) (already in ChainCert.Fluid `cap_a0_tie`), the growth-window obstruction (numerical, convention-dependent, CFG103).
kappa = 1/2 is FITTED; nothing here says the theory is closed.
-/

open Filter Topology Real

namespace MineM1

/-- the Lambda-tied saturating cap: rho(n; Lambda) = m n + P_cap x arctan x, P_cap = eps M2 Lambda, x = m n/(nu M2 Lambda) -/
noncomputable def rhoT (m ε M2 ν n Λ : ℝ) : ℝ :=
  m * n + ε * M2 * Λ * ((m * n / (ν * M2 * Λ)) * Real.arctan (m * n / (ν * M2 * Λ)))

/-- pressure P = P_cap x^2/(1+x^2) -/
noncomputable def PT (m ε M2 ν n Λ : ℝ) : ℝ :=
  ε * M2 * Λ * ((m * n / (ν * M2 * Λ)) ^ 2 / (1 + (m * n / (ν * M2 * Λ)) ^ 2))

/-- Euler degree-one homogeneity in (n, Lambda): the cap reads the SAME Lambda as the multiplier (when it does not, the identity below fails) -/
theorem rhoT_scale (m ε M2 ν n Λ s : ℝ) (hs : 0 < s) :
    rhoT m ε M2 ν (s * n) (s * Λ) = s * rhoT m ε M2 ν n Λ := by
  unfold rhoT
  have : m * (s * n) / (ν * M2 * (s * Λ)) = m * n / (ν * M2 * Λ) ∨ ν * M2 = 0 := by
    by_cases h : ν * M2 = 0
    · right; exact h
    · left; field_simp
  rcases this with h | h
  · rw [h]; ring
  · have h' : ν * M2 * (s * Λ) = 0 := by rw [h]; ring
    have h'' : ν * M2 * Λ = 0 := by rw [h]; ring
    rw [h', h'']; simp; ring

/-- d rho / d Lambda at fixed n -/
theorem rhoT_dLam {m ε M2 ν n Λ : ℝ} (hΛ : Λ ≠ 0) :
    HasDerivAt (fun L => rhoT m ε M2 ν n L) (-(PT m ε M2 ν n Λ) / Λ) Λ := by
  set k := m * n / (ν * M2) with hk
  have hx : ∀ L : ℝ, m * n / (ν * M2 * L) = k / L := by
    intro L; rw [hk]; rw [div_div]
  have hxd : HasDerivAt (fun L : ℝ => k / L) (-k / Λ ^ 2) Λ := by
    have := (hasDerivAt_const Λ k).div (hasDerivAt_id Λ) hΛ
    refine this.congr_deriv ?_
    simp
  have hat := hxd.arctan
  have hprod := hxd.mul hat
  have hcap := ((hasDerivAt_id Λ).mul hprod).const_mul (ε * M2)
  have hlin := hcap.const_add (m * n)
  have hfun : (fun L => rhoT m ε M2 ν n L) = fun L => m * n + ε * M2 * (id L * (k / L * Real.arctan (k / L))) := by
    funext L; unfold rhoT; rw [hx L]; simp; ring
  rw [hfun]
  refine hlin.congr_deriv ?_
  unfold PT
  rw [hx Λ]
  simp only [id, Pi.mul_apply]
  field_simp
  ring

/-- d rho / d n at fixed Lambda -/
theorem rhoT_dn {m ε M2 ν n Λ : ℝ} (hΛ : Λ ≠ 0) (hν : ν ≠ 0) (hM : M2 ≠ 0) :
    HasDerivAt (fun N => rhoT m ε M2 ν N Λ)
      (m + ε * M2 * Λ * (m / (ν * M2 * Λ)) *
        (Real.arctan (m * n / (ν * M2 * Λ)) + (m * n / (ν * M2 * Λ)) / (1 + (m * n / (ν * M2 * Λ)) ^ 2))) n := by
  have hs : ν * M2 * Λ ≠ 0 := mul_ne_zero (mul_ne_zero hν hM) hΛ
  have hx : HasDerivAt (fun N : ℝ => m * N / (ν * M2 * Λ)) (m / (ν * M2 * Λ)) n := by
    simpa [div_eq_mul_inv, mul_comm, mul_left_comm, mul_assoc] using ((hasDerivAt_id n).const_mul m).mul_const (ν * M2 * Λ)⁻¹
  have hat := hx.arctan
  have hprod := hx.mul hat
  have hlin : HasDerivAt (fun N : ℝ => m * N) m n := by simpa using (hasDerivAt_id n).const_mul m
  have hfull := hlin.add (hprod.const_mul (ε * M2 * Λ))
  have hfun : (fun N => rhoT m ε M2 ν N Λ) = (fun N : ℝ => m * N) + fun y : ℝ => ε * M2 * Λ * (m * y / (ν * M2 * Λ) * Real.arctan (m * y / (ν * M2 * Λ))) := by
    funext y; simp only [rhoT, Pi.add_apply]
  rw [hfun]
  refine hfull.congr_deriv ?_
  field_simp

/-- n rho_n - rho = P = P_cap x^2/(1+x^2) -/
theorem rhoT_pressure {m ε M2 ν n Λ : ℝ} (hΛ : Λ ≠ 0) (hν : ν ≠ 0) (hM : M2 ≠ 0) :
    n * deriv (fun N => rhoT m ε M2 ν N Λ) n - rhoT m ε M2 ν n Λ = PT m ε M2 ν n Λ := by
  rw [(rhoT_dn hΛ hν hM).deriv]
  unfold rhoT PT
  have hs : ν * M2 * Λ ≠ 0 := mul_ne_zero (mul_ne_zero hν hM) hΛ
  field_simp
  ring

/-- Euler identity  n rho_n + Lambda rho_Lambda = rho,  i.e.  rho_Lambda|_n = -P/Lambda (the identity the clock equation uses) -/
theorem rhoT_euler {m ε M2 ν n Λ : ℝ} (hΛ : Λ ≠ 0) (hν : ν ≠ 0) (hM : M2 ≠ 0) :
    n * deriv (fun N => rhoT m ε M2 ν N Λ) n + Λ * deriv (fun L => rhoT m ε M2 ν n L) Λ = rhoT m ε M2 ν n Λ := by
  rw [(rhoT_dLam (m := m) (ε := ε) (M2 := M2) (ν := ν) (n := n) hΛ).deriv]
  have := rhoT_pressure (m := m) (ε := ε) (M2 := M2) (ν := ν) (n := n) hΛ hν hM
  field_simp
  linarith

/-- the clock equation: E_Lambda: M2 div T - sg M2 - sg rho_Lambda = 0 with rho_Lambda = -P/Lambda gives div T = sg (1 - P/(M2 Lambda)) -/
theorem clock_identity {M2 Λ sg divT P ρΛ : ℝ} (hM : M2 ≠ 0) (hΛ : Λ ≠ 0)
    (hE : M2 * divT - sg * M2 - sg * ρΛ = 0) (hρ : ρΛ = -P / Λ) :
    divT = sg * (1 - P / (M2 * Λ)) := by
  subst hρ
  field_simp
  field_simp at hE
  linarith

/-- the FRW continuity equation for ANY Lambda(t): with n' = -3 H n (number conservation),
    d rho/dt + 3 H (rho + P) = rho_Lambda Lambda' = -(P/Lambda) Lambda'. -/
theorem rhoT_dt {m ε M2 ν : ℝ} {n Λ : ℝ → ℝ} {n' Λ' t : ℝ}
    (hn : HasDerivAt n n' t) (hΛd : HasDerivAt Λ Λ' t) (hΛ : Λ t ≠ 0) (hn0 : n t ≠ 0) (hν : ν ≠ 0) (hM : M2 ≠ 0) :
    HasDerivAt (fun s => rhoT m ε M2 ν (n s) (Λ s))
      ((rhoT m ε M2 ν (n t) (Λ t) + PT m ε M2 ν (n t) (Λ t)) * (n' / n t)
        - PT m ε M2 ν (n t) (Λ t) * Λ' / Λ t) t := by
  have hs : ν * M2 * Λ t ≠ 0 := mul_ne_zero (mul_ne_zero hν hM) hΛ
  have hlin : HasDerivAt (fun s => m * n s) (m * n') t := hn.const_mul m
  have hden : HasDerivAt (fun s => ν * M2 * Λ s) (ν * M2 * Λ') t := hΛd.const_mul _
  have hx := (hn.const_mul m).div hden hs
  have hat := hx.arctan
  have hprod := hx.mul hat
  have hcap := (hΛd.mul hprod).const_mul (ε * M2)
  have hfull := hlin.add hcap
  have hfun : (fun s => rhoT m ε M2 ν (n s) (Λ s)) = fun s => m * n s + ε * M2 * (Λ s * (m * n s / (ν * M2 * Λ s) * Real.arctan (m * n s / (ν * M2 * Λ s)))) := by
    funext s; simp only [rhoT]; ring
  rw [hfun]
  refine hfull.congr_deriv ?_
  simp only [Pi.div_apply, Pi.mul_apply]
  unfold rhoT PT
  have hν' : ν ≠ 0 := hν
  field_simp
  ring

/-- FRW form: n' = -3 H n gives  rho' = -3 H (rho + P) - (P/Lambda) Lambda'; and Lambda' = 0 (E_T) gives the standard continuity equation -/
theorem frw_continuity {m ε M2 ν : ℝ} {n Λ : ℝ → ℝ} {H Λ' t : ℝ}
    (hn : HasDerivAt n (-3 * H * n t) t) (hΛd : HasDerivAt Λ Λ' t) (hΛ : Λ t ≠ 0) (hn0 : n t ≠ 0) (hν : ν ≠ 0) (hM : M2 ≠ 0) :
    HasDerivAt (fun s => rhoT m ε M2 ν (n s) (Λ s))
      (-3 * H * (rhoT m ε M2 ν (n t) (Λ t) + PT m ε M2 ν (n t) (Λ t))
        - PT m ε M2 ν (n t) (Λ t) * Λ' / Λ t) t := by
  refine (rhoT_dt hn hΛd hΛ hn0 hν hM).congr_deriv ?_
  field_simp


end MineM1

open MineM1 in
#print axioms rhoT_scale
open MineM1 in
#print axioms rhoT_pressure
open MineM1 in
#print axioms rhoT_dLam
open MineM1 in
#print axioms rhoT_euler
open MineM1 in
#print axioms clock_identity
open MineM1 in
#print axioms rhoT_dt
open MineM1 in
#print axioms frw_continuity
