import Mathlib

/-!
# AS009 — surface-density dimensions and coefficient bookkeeping (algebraic core)

SCOPE. The audit seed `AS009_surface_density_dimensions_and_coefficient_bookkeeping.md`
derives which geometry fixes which coefficient in the a0/G surface-density family on the
CORE scale identities of the framework contract:

    a0 = kappa c sqrt(G rho_Lambda),  kappa = 1/2 ADOPTED (never derived here)
    r_M = sqrt(G M_b/a0),  C = sqrt(G M_b a0)
    rho_ph = C/(4 pi G r^2)              (conditional deep-equilibrium input)

This file certifies ONLY the algebraic identities that the audit derives from those
premises with positive-real algebra — the phantom amplitude law, the projected surface
density at r_M, the density-to-surface-density bookkeeping recast (the negative control:
a volume density can never equal Sigma0 = a0/G; the correct pairing is
rho_ph(r) (4 pi r^2) = Sigma0 r_M), and the Q-branch halo-field cap g_phi < a0/2, which
is the premise of the ZD07 slab ceiling Sigma_phi,tot < a0/(4 pi G) = (a0/(2 pi G))/2.

WHAT IS NOT IN THIS FILE (see derivation.md): the RAR/MONO/EXP branch caps (transcendental
peak: numerical, mpmath 50 digits), the slab Gauss-law coefficient 2 pi (a physical
integration statement from div E = 4 pi G rho — listed as a conditional premise), and the
value of kappa (adopted input).

Every statement is quantified over positive reals; no assumptions on the physical
magnitudes are made.
-/

noncomputable section

open scoped Real

namespace AS009

/-- From the defining equations of r_M and C (C^2 = G M a0, r_M^2 = G M/a0), the product
C r_M equals G M: the coefficient 1 in the amplitude law M_ph(r)/M_b = r/r_M is exact. -/
theorem phantom_amplitude_identity (G M a0 C rM : ℝ) (hG : 0 < G) (hM : 0 < M)
    (ha0 : 0 < a0) (hCp : 0 < C) (hRp : 0 < rM)
    (hC : C ^ 2 = G * M * a0) (hr : rM ^ 2 = G * M / a0) :
    C * rM = G * M := by
  have ha0n : a0 ≠ 0 := ne_of_gt ha0
  have hr' : rM ^ 2 * a0 = G * M := by
    calc
      rM ^ 2 * a0 = (G * M / a0) * a0 := by rw [hr]
      _ = G * M := by field_simp [ha0n]
  have hsq : (C * rM) ^ 2 = (G * M) ^ 2 := by
    calc
      (C * rM) ^ 2 = C ^ 2 * rM ^ 2 := by ring
      _ = (G * M * a0) * rM ^ 2 := by rw [hC]
      _ = (G * M) * (rM ^ 2 * a0) := by ring
      _ = (G * M) ^ 2 := by
        rw [hr']
        ring
  have hCR : 0 ≤ C * rM := mul_nonneg hCp.le hRp.le
  have hGM : 0 ≤ G * M := mul_nonneg hG.le hM.le
  have hroot : Real.sqrt ((C * rM) ^ 2) = Real.sqrt ((G * M) ^ 2) := by
    rw [hsq]
  rw [Real.sqrt_sq_eq_abs, Real.sqrt_sq_eq_abs] at hroot
  have hca : |C * rM| = C * rM := abs_of_nonneg hCR
  have hga : |G * M| = G * M := abs_of_nonneg hGM
  rw [hca, hga] at hroot
  exact hroot

/-- Amplitude law in ratio form: M_ph(r)/M_b = r/r_M with M_ph(r) = C r/G, i.e.
(C r/G)/M = r/r_M, exactly, for every r > 0 (r is any radius; no limit taken). -/
theorem amplitude_law_ratios (G M a0 C rM r : ℝ) (hG : 0 < G) (hM : 0 < M)
    (ha0 : 0 < a0) (hCp : 0 < C) (hRp : 0 < rM)
    (hC : C ^ 2 = G * M * a0) (hr : rM ^ 2 = G * M / a0) :
    (C * r / G) / M = r / rM := by
  have h1 : C * rM = G * M := phantom_amplitude_identity G M a0 C rM hG hM ha0 hCp hRp hC hr
  have hG0 : G ≠ 0 := ne_of_gt hG
  have hM0 : M ≠ 0 := ne_of_gt hM
  have hR0 : rM ≠ 0 := ne_of_gt hRp
  have hC0 : C ≠ 0 := ne_of_gt hCp
  calc
    (C * r / G) / M = (C * r) / (G * M) := by field_simp [hG0, hM0]
    _ = r / rM := by
      rw [← h1]
      field_simp [hC0, hR0]

/-- Projected surface density of the phantom at r_M: M_b/(pi r_M^2) = a0/(pi G).
The baryon mass cancels identically: this is why the quantity is "universal" —
it is a bookkeeping identity at the chosen radius, not a new fitted input. -/
theorem phantom_surface_density_at_rM (G M a0 rM : ℝ) (hG : G ≠ 0) (hM : M ≠ 0)
    (ha0 : a0 ≠ 0) (_hr : rM ≠ 0) (hr2 : rM ^ 2 = G * M / a0) :
    M / (Real.pi * rM ^ 2) = a0 / (Real.pi * G) := by
  have hpi : Real.pi ≠ 0 := Real.pi_ne_zero
  calc
    M / (Real.pi * rM ^ 2) = M / (Real.pi * (G * M / a0)) := by rw [hr2]
    _ = a0 / (Real.pi * G) := by field_simp [hpi, hG, hM, ha0]

/-- Bookkeeping recast used by the negative control: the phantom volume density merits a
length to become a surface density. rho_ph(r) = (a0/G) r_M / (4 pi r^2): with C = a0 r_M
(premise of the CORE identities, C^2 = G M a0 and r_M^2 = G M/a0), the volume density is
Sigma0 = a0/G times the dimensionless-ratio r_M/(4 pi r^2) divided by a length. Stated
purely algebraically: (a0 r_M)/(4 pi G r^2) = (a0/G) (r_M/(4 pi r^2)). -/
theorem phantom_density_bookkeeping (a0 G rM r : ℝ) (hG : G ≠ 0) (hrM : rM ≠ 0)
    (hr : r ≠ 0) :
    (a0 * rM) / (4 * Real.pi * G * r ^ 2) = (a0 / G) * (rM / (4 * Real.pi * r ^ 2)) := by
  have hpi : Real.pi ≠ 0 := Real.pi_ne_zero
  field_simp [hpi, hG, hrM, hr]

/-- Coefficient bookkeeping: the ZD07 slab ceiling a0/(4 pi G) is exactly half of the
Milgrom critical surface density a0/(2 pi G) — the factor 2 is the halo-field cap 1/2
times nothing else at this level — and half of Sigma_pi = a0/(pi G). -/
theorem ceiling_bookkeeping_half (a0 G : ℝ) (hG : G ≠ 0) :
    a0 / (4 * Real.pi * G) = (a0 / (2 * Real.pi * G)) / 2 := by
  have hpi : Real.pi ≠ 0 := Real.pi_ne_zero
  field_simp [hpi, hG]
  ring_nf

theorem sigma_milgrom_half_pi (a0 G : ℝ) (hG : G ≠ 0) :
    a0 / (2 * Real.pi * G) = (a0 / (Real.pi * G)) / 2 := by
  have hpi : Real.pi ≠ 0 := Real.pi_ne_zero
  field_simp [hpi, hG]

theorem sigma_pi_doubles_sigma_half (a0 G : ℝ) (hG : G ≠ 0) :
    a0 / (Real.pi * G) = 2 * (a0 / (2 * Real.pi * G)) := by
  have hpi : Real.pi ≠ 0 := Real.pi_ne_zero
  field_simp [hpi, hG]

/-- The Q-branch halo-field cap, sqrt-free lemma: any positive s with s^2 = B^2 + a0 B
satisfies s - B < a0/2 (strictly; the sup a0/2 is attained only in the B -> oo limit). -/
lemma halo_gap_bound (a0 B s : ℝ) (ha0 : 0 < a0) (hB : 0 < B)
    (hs : 0 < s) (hsq : s ^ 2 = B ^ 2 + a0 * B) : s - B < a0 / 2 := by
  have hsq' : s ^ 2 < (B + a0 / 2) ^ 2 := by
    nlinarith [hsq]
  have hlt : |s| < |B + a0 / 2| := (sq_lt_sq.mp hsq')
  have hs_abs : |s| = s := abs_of_pos hs
  have hBp : 0 < B + a0 / 2 := by linarith
  have hB_abs : |B + a0 / 2| = B + a0 / 2 := abs_of_pos hBp
  rw [hs_abs, hB_abs] at hlt
  linarith

/-- Q-branch cap, instantiated: sqrt(B^2 + a0 B) - B < a0/2 for all B > 0, a0 > 0.
This is the branch-precise form of the "halo field saturates below a0/2" premise; the
audit shows it holds on Q and fails on RAR (peak 0.6476 a0) and on the MONO continuation. -/
theorem q_branch_halo_cap (a0 B : ℝ) (ha0 : 0 < a0) (hB : 0 < B) :
    Real.sqrt (B ^ 2 + a0 * B) - B < a0 / 2 := by
  have hnon : 0 ≤ B ^ 2 + a0 * B := by nlinarith
  have hpos : 0 < B ^ 2 + a0 * B := by
    nlinarith [mul_pos ha0 hB]
  have hs : (Real.sqrt (B ^ 2 + a0 * B)) ^ 2 = B ^ 2 + a0 * B := Real.sq_sqrt hnon
  have hsp : 0 < Real.sqrt (B ^ 2 + a0 * B) := Real.sqrt_pos.mpr hpos
  exact halo_gap_bound a0 B (Real.sqrt (B ^ 2 + a0 * B)) ha0 hB hsp hs

end AS009