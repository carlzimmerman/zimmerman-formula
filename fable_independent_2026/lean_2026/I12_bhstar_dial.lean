import Mathlib

open Real

/-!
# I12 — Wave U: the photosphere-gravity law — THE DIAL IS AN OBSERVABLE

SCOPE (per lean-math-certification): Lean certifies the third mass-cancellation theorem
(after I03's g_B and I11's r_B^4 n_H). From the standard definitions:

  Gamma  = kappa_es L / (4 pi c G M)        [the Eddington factor, definition]
  L      = 4 pi R^2 sigma T_eff^4           [the blackbody-like continuum, fitted]
  g_phot = G M / R^2                        [the gravity from the line wings, fitted]

CONCLUSION (the 4 pi and M cancel — pure field algebra):

  Gamma * c * g_phot = kappa_es * sigma * T_eff^4
  g_phot = kappa_es sigma T_eff^4 / (Gamma c)      -- MASS-INDEPENDENT
  Gamma  = kappa_es sigma T_eff^4 / (c g_phot)     -- THE DIAL IS AN OUTPUT

The numbers (Python `bhstar_u1_decircularization.py`, 4/4): Gamma = 56.6 measured at
the median stack (T_eff = 4662 K, log g = -2.2) — 13% above the assumed cap of 50;
the mass 1e3.97 Msun from (L, Gamma) with no dial; the parameter-free r* = 96.7 au.
Zero `sorry`; axioms ⊆ {propext, Classical.choice, Quot.sound}.
-/

noncomputable section

/-- **U (the photosphere-gravity law).** Gamma c g_phot = kappa_es sigma T_eff^4 —
the mass cancels exactly: the third M-cancellation theorem. -/
theorem photosphere_gravity {G M R kappa c sigma T g Gam : ℝ}
    (hG : 0 < G) (hM : 0 < M) (hR : 0 < R) (hk : 0 < kappa) (hc : 0 < c)
    (hsig : 0 < sigma) (hT : 0 < T) (hg : 0 < g) (hGam : 0 < Gam)
    (hGamdef : Gam = kappa * (4 * π * R ^ 2 * sigma * T ^ 4) / (4 * π * c * G * M))
    (hg : g = G * M / R ^ 2) :
    Gam * c * g = kappa * sigma * T ^ 4 := by
  rw [hGamdef, hg]
  field_simp [hG.ne', hM.ne', hR.ne']

/-- **U (the dial readout).** Gamma = kappa_es sigma T_eff^4/(c g_phot) — the assumed
dial is an output of the same line-wing fit that gives log g. -/
theorem gamma_readout {G M R kappa c sigma T g Gam : ℝ}
    (hG : 0 < G) (hM : 0 < M) (hR : 0 < R) (hk : 0 < kappa) (hc : 0 < c)
    (hsig : 0 < sigma) (hT : 0 < T) (hg : 0 < g) (hGam : 0 < Gam)
    (hGamdef : Gam = kappa * (4 * π * R ^ 2 * sigma * T ^ 4) / (4 * π * c * G * M))
    (hg : g = G * M / R ^ 2) :
    Gam = kappa * sigma * T ^ 4 / (c * g) := by
  have h1 := photosphere_gravity hG hM hR hk hc hsig hT (by positivity) hGam hGamdef hg
  rw [eq_comm, div_eq_iff (ne_of_gt (by positivity : (0:ℝ) < c * g))]
  linarith [h1]

end

#print axioms photosphere_gravity
#print axioms gamma_readout