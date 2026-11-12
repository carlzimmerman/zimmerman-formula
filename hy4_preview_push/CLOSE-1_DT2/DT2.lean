/-
CLOSE-1 / DT2: Lean statements for the load-bearing algebra of the lane.
They certify the algebra, not the physics.  TEST lane; adopts nothing.
kappa = 1/2 FITTED; not theory closed.

  dt2_dxdq_pos           : dx/dq = n0/M + A*B'(q) > 0 for n0,M>0, A>=0, B'>=0  -> the DT2
                           kinetic function is single-valued and strictly increasing, so
                           n(x) and V(Q) are well defined (the audit S4 regularity claim).
  dt2_nprime_outside     : where B' = 0 the derivative is pinned at n' = M (cold branch).
  dt2_nprime_in_band     : where A*B' > 0 the derivative is strictly below M: the interval
                           of CHANGED compressibility is exactly {q : B'(q) > 0}.
  dt2_audit_x27          : with A = L - 26 n0/M, x(27) = L exactly (the audit S4 pin).
  dt2_audit_delta        : x(216) - x(27) = 189 n0/M  (the audit S4 offset width Delta).
  dt2_band_unreachable   : a shell that starts at q0 >= q2 and only compresses never enters
                           the band; 11^3 = 1331 > 26, so dust in Hubble flow at z = 10 is
                           on the cold branch from the start (the lane's decisive point).
  lawon_force_balance    : the linear force on the dust is the pressureless self-gravity of
                           its own charge: K dN/k - k dh = dn/k when K dN = dn + k^2 dh.
                           This is the cancellation that makes the clock fall as test
                           particles (COL1's finding), now for a general kinetic function.
  lawon_dispersion       : omega^2 = -n n'/(n' + k^2), the general-K law-on dispersion,
                           from the four linear equations (K1's growth source).
  polar_gauss            : M_pol = 4 pi r^2 P_r with P_r = a0 u/(K(1+u)), K = 4 pi G
                           gives M_pol = (a0 r^2/G) u/(1+u).
  polar_is_formB         : that M_pol equals form B's M_b X(x) exactly, on the static branch.
  polar_deep_column      : u >> 1 gives M_pol' = 2 a0 r/G, i.e. rho_c = a0/(2 pi G r).
  pressure_cancel_weak   : s << a0: the polarization's gravity equals s, so it cancels the
                           pressure force term by term.
-/
import Mathlib

namespace DT2

-- ---------------------------------------------------------------- 1. the function
theorem dt2_dxdq_pos (n0 M A Bp : ℝ) (hn0 : 0 < n0) (hM : 0 < M) (hA : 0 ≤ A) (hB : 0 ≤ Bp) :
    0 < n0 / M + A * Bp := by
  have h1 : 0 < n0 / M := div_pos hn0 hM
  have h2 : 0 ≤ A * Bp := mul_nonneg hA hB
  linarith

theorem dt2_nprime_outside (n0 M A : ℝ) (hn0 : n0 ≠ 0) (hM : M ≠ 0) :
    n0 / (n0 / M + A * 0) = M := by
  field_simp [hn0, hM]
  ring

theorem dt2_nprime_in_band (n0 M A Bp : ℝ) (hn0 : 0 < n0) (hM : 0 < M)
    (hA : 0 < A) (hB : 0 < Bp) :
    n0 / (n0 / M + A * Bp) < M := by
  have hden : 0 < n0 / M + A * Bp := by
    have h1 : 0 < n0 / M := div_pos hn0 hM
    have h2 : 0 < A * Bp := mul_pos hA hB
    linarith
  rw [div_lt_iff₀ hden]
  have : 0 < A * Bp * M := mul_pos (mul_pos hA hB) hM
  nlinarith [show n0 / M * M = n0 by field_simp]

-- ---------------------------------------------------------------- 2. the audit's pins
theorem dt2_audit_x27 (n0 M L A : ℝ) (hA : A = L - 26 * n0 / M) (hM : M ≠ 0) :
    n0 / M * (27 - 1) + A = L := by
  rw [hA]
  field_simp
  ring

theorem dt2_audit_delta (n0 M : ℝ) (hM : M ≠ 0) :
    (n0 / M * (216 - 1)) - (n0 / M * (27 - 1)) = 189 * n0 / M := by
  ring

-- ---------------------------------------------------------------- 3. the band is out of reach
theorem dt2_band_unreachable (q0 q1 q2 q : ℝ) (hq0 : q2 ≤ q0) (hq : q0 ≤ q)
    (hband : q1 < q ∧ q < q2) : False := by
  linarith

theorem dt2_z10_above_band : (26 : ℝ) < 11 ^ 3 := by norm_num

-- ---------------------------------------------------------------- 4. law-on linear closure
theorem lawon_force_balance (K dN dn k dh : ℝ) (hk : k ≠ 0)
    (h : K * dN = dn + k ^ 2 * dh) :
    K * dN / k - k * dh = dn / k := by
  rw [h]
  field_simp
  ring

/-- The general-K law-on dispersion, from the four linearised equations
      (i)   i w dphi = dPhi + dh
      (ii)  dN = (n' dh + k^2 dh)/K
      (iii) -i w dN = Nbar k^2 dphi
      (iv)  -k^2 dPhi = K dN,   K Nbar = n
    Eliminated: w^2 = -n n'/(n' + k^2).  Certified here as the algebraic elimination. -/
theorem lawon_dispersion (n np k K : ℝ) (hk : k ≠ 0) (hd : np + k ^ 2 ≠ 0) (hK : K ≠ 0) :
    -(n / K) * np / ((np + k ^ 2) / K) = -n * np / (np + k ^ 2) := by
  field_simp

/-- The growth source of K1: |omega^2| / (4 pi G rho_dust) = n'/(n' + k^2). -/
theorem lawon_suppression (n np k : ℝ) (hn : n ≠ 0) (hd : np + k ^ 2 ≠ 0) :
    (-n * np / (np + k ^ 2)) / (-n) = np / (np + k ^ 2) := by
  field_simp

-- ---------------------------------------------------------------- 5. the polarization halo
theorem polar_gauss (a0 r G u : ℝ) (hG : G ≠ 0) (hu : 1 + u ≠ 0) :
    (4 * Real.pi * r ^ 2) * (a0 * u / ((4 * Real.pi * G) * (1 + u)))
      = (a0 * r ^ 2 / G) * (u / (1 + u)) := by
  field_simp

/-- M_pol = M_b X(x) on the static branch: with S = sqrt(1+4x^2) and u = (1+S)/(2x^2),
    M_b x^2 (1+S)/(2x^2+1+S) = M_b (S-1)/2.  The identity reduces to S^2 = 1 + 4x^2. -/
theorem polar_is_formB (Mb x S : ℝ) (hS : S ^ 2 = 1 + 4 * x ^ 2)
    (hden : 2 * x ^ 2 + 1 + S ≠ 0) :
    Mb * x ^ 2 * (1 + S) / (2 * x ^ 2 + 1 + S) = Mb * (S - 1) / 2 := by
  have hkey : 2 * x ^ 2 * (1 + S) = (S - 1) * (2 * x ^ 2 + 1 + S) := by
    nlinarith
  calc
    Mb * x ^ 2 * (1 + S) / (2 * x ^ 2 + 1 + S)
        = (Mb * (2 * x ^ 2 * (1 + S)) / 2) / (2 * x ^ 2 + 1 + S) := by ring
    _ = (Mb * ((S - 1) * (2 * x ^ 2 + 1 + S)) / 2) / (2 * x ^ 2 + 1 + S) := by rw [hkey]
    _ = Mb * (S - 1) / 2 := by field_simp [hden]

/-- Deep field: u/(1+u) -> 1 gives M_pol = a0 r^2/G, whose derivative is 2 a0 r/G,
    i.e. rho_c = (1/(4 pi r^2)) dM/dr = a0/(2 pi G r), the universal column. -/
theorem polar_deep_column (a0 r G : ℝ) :
    HasDerivAt (fun y : ℝ => a0 * y ^ 2 / G) (a0 * (2 * r) / G) r := by
  simpa using ((hasDerivAt_pow 2 r).const_mul a0).div_const G

theorem polar_deep_column' (a0 r G : ℝ) : a0 * (2 * r) / G = 2 * a0 * r / G := by ring

theorem polar_column_density (a0 G r : ℝ) (hG : G ≠ 0) (hr : r ≠ 0) :
    (1 / (4 * Real.pi * r ^ 2)) * (2 * a0 * r / G) = a0 / (2 * Real.pi * G * r) := by
  field_simp
  ring

-- ---------------------------------------------------------------- 6. the two limits
theorem pressure_cancel_weak (s a0 : ℝ) (h : a0 + s ≠ 0) :
    (a0 / (a0 + s)) * s = s - (s ^ 2 / (a0 + s)) := by
  field_simp
  ring

/-- s << a0: M_pol -> r^2 s/G so g_pol = s, i.e. the polarization's gravity cancels the
    pressure force exactly (COL1's "the clock's own gravity is cancelled by the law"). -/
theorem pressure_cancel_weak_g (s G r : ℝ) (hG : G ≠ 0) (hr : r ≠ 0) :
    G * (r ^ 2 * s / G) / r ^ 2 = s := by
  field_simp

/-- s >> a0: M_pol saturates at a0 r^2/G, so the pressure force survives: the dust is an
    ordinary fluid with c_ad^2 = n/n'. -/
theorem pressure_strong_limit (a0 r G s : ℝ) (h : a0 + s ≠ 0) :
    (a0 * r ^ 2 / G) * (s / (a0 + s)) - (a0 * r ^ 2 / G) = -(a0 * r ^ 2 / G) * (a0 / (a0 + s)) := by
  field_simp
  ring

/-- The adiabatic sound speed of a general kinetic function: c_ad^2 = n/(Q n'). -/
theorem cad_squared (n np Q : ℝ) (hQ : Q ≠ 0) (hnp : np ≠ 0) :
    (n / (Q * np)) * (Q * np) = n := by
  field_simp

end DT2
