import Mathlib
import ChainCert.Certificates
import ChainCert.Kernel

/-!
# ChainCert.Chain -- the composable core of the chain, with every premise named

The chain proved here, from premises to conclusion:

    a0(z) = kappa c sqrt(G rho_Lambda(z))            (T1, the tie: a POSTULATED form)
    g = nu(g_N / a0) g_N,  nu * sqrt -> 1 deep       (T2, the kernel: DECLARED; verified for nu_mono in ChainCert.Kernel)
    ==>  v_c^4 -> G M a0(z)  as r -> infinity        (the BTFR zero point, from C2)
    rho_Lambda(z) = rho_Lambda(0)                    (PREMISE: a cosmological constant, w = -1)
    ==>  the zero point does not depend on z         (flat a0(z), from C4's iff)

What is EMPIRICAL / FITTED and therefore only a hypothesis here:
  * kappa (= 1/2 is FITTED from the BTFR zero point; C5 shows the four-form closure leaves it free),
  * rho_Lambda constant in z,
  * the kernel's deep limit (a property of the declared kernel, proved for nu_beta and nu_mono).
Nothing here says the premises hold in nature; it says the conclusions follow from them.
-/

open Filter Topology

/-- the premises of the chain, each labelled -/
structure ChainPremises where
  κ : ℝ
  c : ℝ
  G : ℝ
  ρΛ : ℝ → ℝ                       -- rho_Lambda as a function of redshift z
  hκ : 0 < κ                       -- FITTED (1/2); only positivity is used
  hc : 0 < c
  hG : 0 < G
  hρ : ∀ z, 0 < ρΛ z               -- PREMISE: a positive vacuum density
  hflat : ∀ z, ρΛ z = ρΛ 0         -- PREMISE (empirical): a cosmological constant, w = -1

namespace ChainPremises

/-- the tied acceleration scale at redshift z -/
noncomputable def a0 (P : ChainPremises) (z : ℝ) : ℝ := P.κ * P.c * Real.sqrt (P.G * P.ρΛ z)

theorem a0_pos (P : ChainPremises) (z : ℝ) : 0 < P.a0 z := by
  unfold a0
  have := P.hκ; have := P.hc; have := P.hG; have := P.hρ z
  positivity

/-- flat a0(z): under the premise rho_Lambda constant, a0 does not evolve -/
theorem a0_flat (P : ChainPremises) (z : ℝ) : P.a0 z = P.a0 0 := by
  unfold a0; rw [P.hflat z]

/-- the BTFR zero point for the kernel nu_mono at redshift z:  v^4 -> G M a0(z) -/
theorem btfr_limit (P : ChainPremises) {M : ℝ} (hM : 0 < M) (z : ℝ) :
    Tendsto (fun r : ℝ => ((P.G * M / r) * nuMono (P.G * M / (r ^ 2 * P.a0 z))) ^ 2)
      atTop (𝓝 (P.G * M * P.a0 z)) :=
  nuMono_btfr_from_vacuum P.hG hM P.hκ P.hc (P.hρ z)

/-- THE COMPOSED CONCLUSION: the asymptotic v^4 of a point mass is the same at every redshift
    (the flat-a0 law), given the tie, the kernel's deep limit and a constant rho_Lambda. -/
theorem btfr_limit_redshift_independent (P : ChainPremises) {M : ℝ} (hM : 0 < M) (z : ℝ) :
    Tendsto (fun r : ℝ => ((P.G * M / r) * nuMono (P.G * M / (r ^ 2 * P.a0 z))) ^ 2)
      atTop (𝓝 (P.G * M * P.a0 0)) := by
  rw [show P.G * M * P.a0 0 = P.G * M * P.a0 z by rw [P.a0_flat z]]
  exact P.btfr_limit hM z

end ChainPremises

/-- the BTFR zero point is LINEAR in kappa: G M kappa c sqrt(G rho_Lambda).  Read with C5 (kappa is a free ratio of the
    four-form closure): the zero point measures kappa, it does not predict it. -/
theorem zero_point_linear_in_kappa {G M c ρΛ κ₁ κ₂ : ℝ} (hG : 0 < G) (hM : 0 < M) (hc : 0 < c) (hρ : 0 < ρΛ)
    (hκ₂ : 0 < κ₂) :
    (G * M * (κ₁ * c * Real.sqrt (G * ρΛ))) / (G * M * (κ₂ * c * Real.sqrt (G * ρΛ))) = κ₁ / κ₂ := by
  have h1 : 0 < Real.sqrt (G * ρΛ) := Real.sqrt_pos.mpr (mul_pos hG hρ)
  field_simp
