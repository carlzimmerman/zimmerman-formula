import Mathlib

/-!
# ChainCert.Gauss -- the algebra of CFG48's Gauss lemma (G1, C1) for a gated shift-symmetric MOND field

CFG48 (campaign_fresh_gravity/CFG48_gap1_switch/G1_gauss_noether.py, C1) takes the radial action

    L = r^2 [ -(1/8 pi G)(2 Phi' psi' - Q_W(psi'^2)) - rho Phi ],   Q_W(s) = W Q1(s) + (1 - W) s,   A = W Q1' + 1 - W,

derives its Euler-Lagrange equations with sympy, and observes that with `M' = 4 pi r^2 rho`, `psi' = G M / r^2`, `Phi' = A psi'`
both vanish, so the dynamical mass is `r^2 Phi'/G = A M`, equal to the baryon mass `M` where the gate is off (`W = 0`, `A = 1`).

Certified here (premises => conclusions):
* `gateA_off` / `gateA_on`: the gate factor is `1` at `W = 0` and `Q1'` at `W = 1`;
* `gauss_dyn_mass`: from `psi' = G M/r^2` and `Phi' = A psi'`, `r^2 Phi'/G = A M`;
* `gauss_off_mass`: at `W = 0` the dynamical mass is exactly `M`, whatever `Q1'` is;
* `gauss_flux_deriv`: if `psi' = G M/r^2` off the origin and `M' = 4 pi r^2 rho`, then `d/dr (r^2 psi') = 4 pi G r^2 rho`
  (the reduced Phi-equation: the flux equation of the action);
* `gauss_psi_momentum_zero`: on `Phi' = A psi'` the psi-momentum `-(r^2/4 pi G)(Phi' - A psi')` vanishes identically (the reduced psi-equation);
* `gauss_second_source`: adding a second real-mass source `M_c != 0` (the script's MUTATE) makes the `W = 0` dynamical mass `M + M_c`, NOT `M`.
NOT certified: the derivation of the Euler-Lagrange equations from the action (done by sympy in G1); the helmholtz test (C3) and the Noether
budget (C4); that any physical gate has this form.
-/

noncomputable def gateA (W q : ℝ) : ℝ := W * q + 1 - W

theorem gateA_off (q : ℝ) : gateA 0 q = 1 := by unfold gateA; ring

theorem gateA_on (q : ℝ) : gateA 1 q = q := by unfold gateA; ring

theorem gauss_dyn_mass {G r M A dpsi dPhi : ℝ} (hr : r ≠ 0) (hG : G ≠ 0)
    (hpsi : dpsi = G * M / r ^ 2) (hPhi : dPhi = A * dpsi) : r ^ 2 * dPhi / G = A * M := by
  rw [hPhi, hpsi]
  field_simp

theorem gauss_off_mass {G r M q dpsi dPhi : ℝ} (hr : r ≠ 0) (hG : G ≠ 0)
    (hpsi : dpsi = G * M / r ^ 2) (hPhi : dPhi = gateA 0 q * dpsi) : r ^ 2 * dPhi / G = M := by
  rw [gauss_dyn_mass hr hG hpsi hPhi, gateA_off, one_mul]

theorem gauss_flux_deriv {G ρ r₀ : ℝ} {M dpsi : ℝ → ℝ} (hr₀ : r₀ ≠ 0)
    (hpsi : ∀ r, r ≠ 0 → dpsi r = G * M r / r ^ 2)
    (hM : HasDerivAt M (4 * Real.pi * r₀ ^ 2 * ρ) r₀) :
    HasDerivAt (fun r => r ^ 2 * dpsi r) (G * (4 * Real.pi * r₀ ^ 2 * ρ)) r₀ := by
  have hev : (fun r => r ^ 2 * dpsi r) =ᶠ[nhds r₀] fun r => G * M r := by
    filter_upwards [isOpen_ne.mem_nhds hr₀] with r hr
    rw [hpsi r hr]
    field_simp
  exact (hM.const_mul G).congr_of_eventuallyEq hev

theorem gauss_psi_momentum_zero {G r A dpsi dPhi : ℝ} (hPhi : dPhi = A * dpsi) :
    -(r ^ 2 / (4 * Real.pi * G)) * (dPhi - A * dpsi) = 0 := by
  rw [hPhi]; ring

theorem gauss_second_source {G r M Mc dpsi dPhi : ℝ} (hr : r ≠ 0) (hG : G ≠ 0) (hMc : Mc ≠ 0)
    (hpsi : dpsi = G * (M + Mc) / r ^ 2) (hPhi : dPhi = gateA 0 0 * dpsi) : r ^ 2 * dPhi / G ≠ M := by
  rw [gauss_dyn_mass hr hG hpsi hPhi, gateA_off, one_mul]
  intro h
  exact hMc (by linarith)
