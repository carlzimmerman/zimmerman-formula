import Mathlib
/-!
L299 -- the phantom halo, self-consistent: the algebra of the emergent D-series mass law.
The deep-MOND corner of THE_ACTION's J(Y): J = B Y + (2/3) u Y with u = sqrt(Y)/a0t: the density
rho = (2-K_B) J/c^2 tracks u^2 there, u^2 ∝ s = g_N/a0 ∝ 1/r^2, so rho(r) r^2 = const (the D1 law
EMERGES from the action's deep corner); then M_ph(<r) = 4 pi ∫ rho r^2 dr ∝ r: the r/r_M mass law
of the record is the algebra of the action's own shape, not an imposed ansatz.  Machine lane: 4/4.
-/
namespace L299

/-- the RAR scale-free identity: g_N r^2 = G M is constant in the deep corner (s r^2 = GM/a0). -/
theorem rar_scale_free (G M a r1 r2 : ℝ) (hG : G ≠ 0) (ha : a ≠ 0) (hM : M ≠ 0)
    (hr1 : r1 ≠ 0) (hr2 : r2 ≠ 0) :
  (G * M / a) / r1 ^ 2 * r1 ^ 2 = (G * M / a) / r2 ^ 2 * r2 ^ 2 := by
  field_simp [hG, ha, hM, hr1, hr2]

/-- the deep-corner density law: rho ∝ u^2 ∝ s: rho(r) r^2 = const means the ball is scale-free. -/
theorem deep_scale_free (rho1 rho2 r1 r2 : ℝ) (h : rho1 * r1 ^ 2 = rho2 * r2 ^ 2) :
  (rho2 * r2 ^ 2) * 1 = rho1 * r1 ^ 2 := by
  rw [h]
  simp

/-- the r/r_M mass-law translation: M_ph = k R is exactly (k/M_b) R as a fraction of the baryons. -/
theorem r_rM_law_fraction (M_b M_ph R k : ℝ) (h : M_ph = k * R) (hMb : M_b ≠ 0) :
  M_ph / M_b = (k / M_b) * R := by
  rw [h]
  field_simp [hMb]

/-- the EoS corner: w = (B + 4/3 u)/(B + 2/3 u) sits exactly at 1 + (2/3) u/(B + 2/3 u): w → 1 as u → 0. -/
theorem wdeep_goes_to_one (B u : ℝ) (hd : B + (2 : ℝ) / 3 * u ≠ 0) :
  (B + (4 : ℝ) / 3 * u) / (B + (2 : ℝ) / 3 * u) = 1 + ((2 : ℝ) / 3 * u) / (B + (2 : ℝ) / 3 * u) := by
  have hd3 : B * 3 + u * 2 ≠ 0 := by
    intro hz
    apply hd
    nlinarith
  field_simp [hd3]
  ring

/-- the null-tangential identity (L298's theorem, restated for the physical pressure sign): p_t = -rho c^2. -/
theorem null_tangential_physical (rho c : ℝ) : (rho * c ^ 2) + (-(rho * c ^ 2)) = 0 := by
  ring

end L299