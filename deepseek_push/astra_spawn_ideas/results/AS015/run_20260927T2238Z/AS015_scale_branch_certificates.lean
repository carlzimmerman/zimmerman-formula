import Mathlib

noncomputable section
open scoped Real

/-!
# AS015 — Constant vacuum versus H-dependent scale: algebraic certificate

Framework inputs (FRAMEWORK_CONTRACT, task AS015):
  a0 = kappa * c * sqrt(G * rho_Lambda)          (kappa = 1/2 adopted, INPUT)
  rho_Lambda = 4 a0^2 / (G c^2)                  (framework identity)
  r_M = sqrt(G M_b / a0)        <->  r_M^2 * a0 = G M_b
  v_flat^4 = G M_b a0
  C = sqrt(G M_b a0)            <->  C^2 = G M_b a0
  sigma^2 = C / 2                                 (conditional deep-equilibrium input)

Claim audited: hypothesis C (vacuum constant, a0(z) = a0(0) for all z) versus
hypothesis H (a0(z) = a0(0) * E(z), E = H/H0).  The theorems below are the
algebraic content used in derivation.md:  they hold for ALL positive real
values (synthetic domain), with no dynamics.  Every statement is branch-
sensitive only through the relations it assumes; nothing here selects κ.
-/

namespace AS015

/-- Deep invariant: r_M^2 * v_flat^4 = (G M_b)^2.  Independent of a0,
therefore identical on the constant-vacuum (C) branch and the H-dependent (H)
branch at every epoch. -/
theorem deep_invariant {rM vf G Mb a0 : ℝ}
    (hrm : rM^2 * a0 = G * Mb) (hvf : vf^4 = G * Mb * a0) :
    rM^2 * vf^4 = (G * Mb)^2 := by
  calc
    rM ^ 2 * vf ^ 4 = rM ^ 2 * (G * Mb * a0) := by rw [hvf]
    _ = (rM ^ 2 * a0) * (G * Mb) := by ring
    _ = (G * Mb) * (G * Mb) := by rw [hrm]
    _ = (G * Mb) ^ 2 := by ring

/-- z-conservation: under ANY a0(z) law (in particular C and H), the product
r_M(z)^2 * v_flat(z)^4 is the same at every epoch. -/
theorem z_conservation {rMz vfz rM0 vf0 G Mb a0z a00 : ℝ}
    (hrmz : rMz^2 * a0z = G * Mb) (hvz : vfz^4 = G * Mb * a0z)
    (hrm0 : rM0^2 * a00 = G * Mb) (hv0 : vf0^4 = G * Mb * a00) :
    rMz^2 * vfz^4 = rM0^2 * vf0^4 := by
  calc
    rMz ^ 2 * vfz ^ 4 = rMz ^ 2 * (G * Mb * a0z) := by rw [hvz]
    _ = (rMz ^ 2 * a0z) * (G * Mb) := by ring
    _ = (G * Mb) * (G * Mb) := by rw [hrmz]
    _ = (G * Mb) * (rM0 ^ 2 * a00) := by rw [← hrm0]
    _ = rM0 ^ 2 * (G * Mb * a00) := by ring
    _ = rM0 ^ 2 * vf0 ^ 4 := by rw [← hv0]

/-- Speed-dispersion identity: v_flat^4 = 4 sigma^4, from C^2 = G M_b a0 and
sigma^2 = C / 2.  Hence v_flat / sigma = sqrt 2 independent of a0, z and
branch (derivation.md §4). -/
theorem speed_dispersion {vf C sigma G Mb a0 : ℝ}
    (hvf : vf^4 = G * Mb * a0) (hC : C^2 = G * Mb * a0)
    (hsig : sigma^2 = C / 2) :
    vf^4 = 4 * sigma^4 := by
  have hsig4 : sigma^4 = (C / 2)^2 := by
    calc
      sigma^4 = (sigma^2)^2 := by ring
      _ = (C / 2)^2 := by rw [hsig]
  rw [hvf, ← hC, hsig4]
  ring

/-- BTFR zero-point ratio: (v_flat(z)/v_flat(0))^4 = a0(z)/a0(0).  The dex
shift of the deep Tully-Fisher zero point equals the dex shift of the vacuum
scale on every branch: 0 (C), log10 E(z) (H). -/
theorem btfr_ratio {vfz vf0 a0z a00 G Mb : ℝ}
    (hvz : vfz^4 = G * Mb * a0z) (hv0 : vf0^4 = G * Mb * a00)
    (hG : G ≠ 0) (hMb : Mb ≠ 0) (ha0z : a0z ≠ 0) (ha00 : a00 ≠ 0) :
    (vfz / vf0)^4 = a0z / a00 := by
  rw [div_pow, hvz, hv0]
  field_simp [hG, hMb, ha00]

/-- MOND-radius ratio: (r_M(z)/r_M(0))^2 = a0(0)/a0(z): r_M shrinks exactly as
E(z)^{-1/2} on the H branch, is constant on the C branch. -/
theorem mond_radius_ratio {rMz rM0 a0z a00 G Mb : ℝ}
    (hrmz : rMz^2 * a0z = G * Mb) (hrm0 : rM0^2 * a00 = G * Mb)
    (hG : G ≠ 0) (hMb : Mb ≠ 0) (ha0z : a0z ≠ 0) (ha00 : a00 ≠ 0) :
    (rMz / rM0)^2 = a00 / a0z := by
  have hrz' : rMz^2 = G * Mb / a0z := by
    rw [← hrmz]
    field_simp [ha0z]
  have hr0' : rM0^2 = G * Mb / a00 := by
    rw [← hrm0]
    field_simp [ha00]
  calc
    (rMz / rM0)^2 = rMz^2 / rM0^2 := by rw [div_pow]
    _ = (G * Mb / a0z) / (G * Mb / a00) := by rw [hrz', hr0']
    _ = a00 / a0z := by field_simp [hG, hMb, ha0z, ha00]

/-- Constant-vacuum identification: on the identity a0 = kappa * c *
sqrt(G * rho), a0(z) = a0(0) at every epoch IFF rho(z) = rho(0).  The
constant-vacuum branch and a constant density rho_Lambda are the SAME premise
(for positive densities, kappa, c, G). -/
theorem a0_constant_iff_density_constant {a0z a00 kappa c G rhoz rho0 : ℝ}
    (hk : 0 < kappa) (hc : 0 < c) (hG : 0 < G) (hrz : 0 < rhoz) (hr0 : 0 < rho0)
    (hz : a0z = kappa * c * Real.sqrt (G * rhoz))
    (h0 : a00 = kappa * c * Real.sqrt (G * rho0)) :
    a0z = a00 ↔ rhoz = rho0 := by
  constructor
  · intro ha
    have hkc : kappa * c ≠ 0 := by positivity
    have hsqrt : Real.sqrt (G * rhoz) = Real.sqrt (G * rho0) := by
      apply mul_left_cancel₀ hkc
      rw [← hz, ← h0, ha]
    have hsqrt_sq : (Real.sqrt (G * rhoz))^2 = (Real.sqrt (G * rho0))^2 := by
      exact congrArg (fun t : ℝ => t^2) hsqrt
    have hGsq : G * rhoz = G * rho0 := by
      rw [← Real.sq_sqrt (by positivity : 0 ≤ G * rhoz),
          ← Real.sq_sqrt (by positivity : 0 ≤ G * rho0)]
      exact hsqrt_sq
    exact mul_left_cancel₀ (ne_of_gt hG) hGsq
  · intro hrho
    rw [hz, h0, hrho]

/-- Branches are distinct: for E ≠ 1 the H law a0(z) = a0(0) * E(z) and the
constant-vacuum law a0(z) = a0(0) are mutually inconsistent.  This is the
algebraic content of the task's negative control: an H-dependent scale is a
DIFFERENT hypothesis, not a renormalization of the constant vacuum. -/
theorem branches_incompatible_for_E_ne_1 {a0z a00 E : ℝ}
    (hE : E ≠ 1) (hpos : 0 < a00) (ha : a0z = a00 * E) (haC : a0z = a00) : False := by
  have htmp : a00 * E = a00 := by
    calc
      a00 * E = a0z := ha.symm
      _ = a00 := haC
  exact hE (mul_left_cancel₀ (ne_of_gt hpos) (by simpa using htmp))

/-- C branch: constant vacuum leaves the deep flat speed unchanged. -/
theorem C_branch_vf_unchanged {vfz vf0 a0z a00 G Mb : ℝ}
    (ha : a0z = a00) (hvz : vfz^4 = G * Mb * a0z) (hv0 : vf0^4 = G * Mb * a00)
    (hposz : 0 < vfz) (hpos0 : 0 < vf0) :
    vfz = vf0 := by
  have h4 : vfz^4 = vf0^4 := by
    rw [hvz, hv0, ha]
  exact (pow_left_inj₀ (le_of_lt hposz) (le_of_lt hpos0) (by norm_num : (4 : ℕ) ≠ 0)).1 h4

/-- H branch: for E > 1 the deep BTFR zero point v_flat^4 rises by exactly
the factor E(z) (zero-point shift +log10 E dex in log10 v_flat^4). -/
theorem H_branch_zero_point_rises {vfz vf0 a0z a00 G Mb E : ℝ}
    (hE : 1 < E) (ha : a0z = a00 * E) (hvz : vfz^4 = G * Mb * a0z)
    (hv0 : vf0^4 = G * Mb * a00) (hpos0 : 0 < vf0) :
    vf0^4 < vfz^4 := by
  have hvz' : vfz^4 = vf0^4 * E := by
    rw [hvz, hv0, ha]
    ring
  rw [hvz']
  simpa [mul_comm] using (lt_mul_iff_one_lt_left (by positivity : 0 < vf0 ^ 4)).mpr hE

/-- H branch: the MOND radius r_M = sqrt(G M_b / a0) shrinks as E^{-1/2}. -/
theorem H_branch_radius_shrinks {rMz rM0 a0z a00 G Mb E : ℝ}
    (hE : 1 < E) (ha : a0z = a00 * E)
    (hrmz : rMz^2 * a0z = G * Mb) (hrm0 : rM0^2 * a00 = G * Mb)
    (hpos : 0 < rM0) (ha00 : 0 < a00) :
    rMz^2 < rM0^2 := by
  have hz : rMz^2 * a0z = rM0^2 * a00 := by
    rw [hrmz, hrm0]
  have hz' : rMz^2 * (a00 * E) = rM0^2 * a00 := by
    rw [ha] at hz
    simpa using hz
  have hz'' : (rMz^2 * E) * a00 = rM0^2 * a00 := by
    simpa [mul_assoc, mul_comm, mul_left_comm] using hz'
  have hz3 : a00 * (rMz^2 * E) = a00 * rM0^2 := by
    simpa [mul_assoc, mul_comm, mul_left_comm] using hz''
  have hEf : rMz^2 * E = rM0^2 := mul_left_cancel₀ (ne_of_gt ha00) hz3
  have hEpos : 0 < E := lt_trans zero_lt_one hE
  have hposRMzsq : 0 < rMz^2 := by
    have hdiv : rMz^2 = rM0^2 / E := by
      rw [← hEf]
      field_simp [ne_of_gt hEpos]
    rw [hdiv]
    positivity
  have h1 : rMz^2 < rMz^2 * E := by
    simpa using (mul_lt_mul_of_pos_left hE hposRMzsq)
  rw [← hEf]
  exact h1

end AS015

end

#print axioms AS015.deep_invariant
#print axioms AS015.z_conservation
#print axioms AS015.speed_dispersion
#print axioms AS015.btfr_ratio
#print axioms AS015.mond_radius_ratio
#print axioms AS015.a0_constant_iff_density_constant
#print axioms AS015.branches_incompatible_for_E_ne_1
#print axioms AS015.C_branch_vf_unchanged
#print axioms AS015.H_branch_zero_point_rises
#print axioms AS015.H_branch_radius_shrinks
