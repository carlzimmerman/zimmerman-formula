/-
  C06 -- THE HORIZON-OMEGA CLOSURE: the germ identity Z^2 = 32*pi/3 and the
  algebraic fixed-point closure of the G058 cosmological identity at the
  de Sitter horizon footing (Z11).

  THE CHAIN.  THE_HORIZON_EQUATION (lane Z11) commits the germ
      Z    = 2*sqrt(8*pi/3),
      R_dS = c / (H0*sqrt(Omega_Lambda)),
      a0   = c^2 / (Z R_dS)              (the horizon surface gravity kappa_dS/Z).
  G058 certified at the real level (fraction-field pattern, no approximations)
  the cosmological identity
      Omega_Lambda = 32*pi*a0^2/(3*H0^2*c^2)
  (the G's cancel EXACTLY; pi and the one scale a0 survive).  C06 closes the
  loop with four statements:

    (1) zSq / zSq_named  -- THE SQUARING OF THE GERM: Z = 2*sqrt(8*pi/3)
        implies Z^2 = 32*pi/3 EXACTLY at the real level (square both sides by
        Real.sq_sqrt -- valid since 8*pi/3 > 0 -- then 4*(8*pi/3) = 32*pi/3
        by ring).
    (2) horizon_omega_fixed_point / tautological_fixed_point -- THE ALGEBRAIC
        FIXED-POINT CLOSURE: substituting the horizon pair
        (a0 = c^2/(Z R_dS), R_dS = c/(H0*sqrt(Omega_Lambda))) into
        Omega_Lambda = 32*pi*a0^2/(3*H0^2*c^2) returns Omega_Lambda
        IDENTICALLY (Omega_L = Omega_L, the tautological self-consistency made
        explicit).  With Z^2 = 32*pi/3 the map
        Omega ↦ 32*pi*a0(Omega)^2/(3*H0^2*c^2) is the identity on EVERY Omega:
        the substitution is a fixed point by construction -- every constant
        (c, H0, Omega) cancels, only the germ Z survives and Z^2 = 32*pi/3
        collapses the pi's.
    (3) closure_iff_zSq -- THE TIGHTNESS STATEMENT: the identity closes IFF
        Z^2 = 32*pi/3.  Forward: from the identity, cancel a0 (via the
        re-expression a0 = c*H0*sqrt(Omega)/Z), cancel the nonzero
        c^2*H0^2, divide by Omega > 0, and solve for Z^2.  Backward: the
        fixed point.  So the closure carries NO slack: the germ identity is
        exactly equivalent to the cosmological self-consistency.
    (4) num_horizon_omega_exact / num_horizon_omega_close -- THE NUMERIC
        ANCHOR AT THE COMMITTED CONSTANTS (H0 = 67.4 km/s/Mpc, c = 299792458,
        Omega_Lambda = 0.685): the reconstruction returns 0.685 EXACTLY
        (the tautology), hence within 1e-4 -- the registered claim.

  HONEST SCOPE.  All statements are pure real algebra in G058's fraction-field
  pattern -- no approximations (no pi bound theorems needed: everything
  cancels).  Positivity hypotheses enter ONLY where a square root must be
  squared (Omega_Lambda > 0) and where nonzero denominators must be excluded.
  The physics content lives in the INPUT definitions (Z11's committed germ,
  G058's identity), which this certificate pins down exactly.

  Seven theorems, zero `sorry`.
-/
import Mathlib

noncomputable section

/-! ## Part 1 -- the committed germ's squaring (Z11: Z = 2*sqrt(8*pi/3)). -/

/-- **zSq.** The germ identity at the real level: the committed Z = 2*sqrt(8π/3)
squares to Z^2 = 4*(8π/3) = 32π/3 EXACTLY.  The square root is squared by
Real.sq_sqrt -- valid because 8π/3 > 0 -- and the numeral arithmetic (2^2 = 4,
4*8 = 32) closes by ring. -/
theorem zSq : (2 * Real.sqrt (8 * Real.pi / 3)) ^ 2 = (32 * Real.pi / 3 : ℝ) := by
  rw [mul_pow]
  rw [Real.sq_sqrt (by positivity : (0 : ℝ) ≤ 8 * Real.pi / 3)]
  ring

/-- **zSq_named.** The same statement with the germ NAMED: any Z equal to the
committed 2*sqrt(8π/3) satisfies Z^2 = 32π/3. -/
theorem zSq_named (Z : ℝ) (hZ : Z = 2 * Real.sqrt (8 * Real.pi / 3)) :
    Z ^ 2 = (32 * Real.pi / 3 : ℝ) := by
  rw [hZ]
  exact zSq

/-! ## Part 2 -- the fixed-point machinery. -/

/-- **a0_horizon_reexpression.** The Z11 re-expression: substituting
R_dS = c/(H0*sqrt(Ω)) into a0 = c^2/(Z R_dS) gives a0 = c*H0*sqrt(Ω)/Z
-- the de Sitter face of the same scale, κ_dS/Z = c*H_Λ/Z with H_Λ = H0√Ω. -/
theorem a0_horizon_reexpression (Ω a0 R_dS Z H0 c : ℝ) (_hO : 0 ≤ Ω) (hZ : Z ≠ 0)
    (hH0 : H0 ≠ 0) (hc : c ≠ 0) (hsqrt : Real.sqrt Ω ≠ 0)
    (hR : R_dS = c / (H0 * Real.sqrt Ω)) (ha : a0 = c ^ 2 / (Z * R_dS)) :
    a0 = c * H0 * Real.sqrt Ω / Z := by
  rw [ha, hR]
  field_simp [hZ, hc, hH0, hsqrt]

/-- **horizon_omega_fixed_point.** THE ALGEBRAIC FIXED-POINT CLOSURE (Z11 into
G058).  Given the committed germ identity Z^2 = 32π/3 and the horizon pair
(R_dS = c/(H0√Ω), a0 = c^2/(Z R_dS)), the identity
Ω = 32π a0^2/(3 H0^2 c^2) is satisfied IDENTICALLY: substituting the pair in
returns Ω (the tautology Ω_L = Ω_L made explicit).  Every component's algebra
collapses -- only the germ Z survives, and Z^2 = 32π/3 cancels the π. -/
theorem horizon_omega_fixed_point (Ω a0 R_dS Z H0 c : ℝ)
    (hO : 0 < Ω) (hH0 : H0 ≠ 0) (hc : c ≠ 0)
    (hR : R_dS = c / (H0 * Real.sqrt Ω)) (ha : a0 = c ^ 2 / (Z * R_dS))
    (hZ2 : Z ^ 2 = 32 * Real.pi / 3) :
    32 * Real.pi * a0 ^ 2 / (3 * H0 ^ 2 * c ^ 2) = Ω := by
  have hsqrt_pos : 0 < Real.sqrt Ω := Real.sqrt_pos.2 hO
  have hsqrt_ne : Real.sqrt Ω ≠ 0 := hsqrt_pos.ne'
  have hZne : Z ≠ 0 := by
    by_contra hz
    have hz2 : Z ^ 2 = 0 := by
      rw [hz]
      norm_num
    have hz2ne : Z ^ 2 ≠ 0 := by
      rw [hZ2]
      exact div_ne_zero (mul_ne_zero (by norm_num : (32 : ℝ) ≠ 0) Real.pi_ne_zero)
        (by norm_num : (3 : ℝ) ≠ 0)
    exact hz2ne hz2
  have ha' : a0 = c * H0 * Real.sqrt Ω / Z :=
    a0_horizon_reexpression Ω a0 R_dS Z H0 c hO.le hZne hH0 hc hsqrt_ne hR ha
  have h1 : (c * H0 * Real.sqrt Ω) ^ 2 = c ^ 2 * H0 ^ 2 * Ω := by
    calc
      (c * H0 * Real.sqrt Ω) ^ 2 = (c * H0) ^ 2 * (Real.sqrt Ω) ^ 2 := by rw [mul_pow]
      _ = c ^ 2 * H0 ^ 2 * (Real.sqrt Ω) ^ 2 := by rw [mul_pow]
      _ = c ^ 2 * H0 ^ 2 * Ω := by rw [Real.sq_sqrt hO.le]
  have ha2 : a0 ^ 2 = c ^ 2 * H0 ^ 2 * Ω / Z ^ 2 := by
    calc
      a0 ^ 2 = (c * H0 * Real.sqrt Ω / Z) ^ 2 := by rw [ha']
      _ = (c * H0 * Real.sqrt Ω) ^ 2 / Z ^ 2 := by rw [div_pow]
      _ = c ^ 2 * H0 ^ 2 * Ω / Z ^ 2 := by rw [h1]
  calc
    32 * Real.pi * a0 ^ 2 / (3 * H0 ^ 2 * c ^ 2)
        = 32 * Real.pi * (c ^ 2 * H0 ^ 2 * Ω / Z ^ 2) / (3 * H0 ^ 2 * c ^ 2) := by
          rw [ha2]
    _ = 32 * Real.pi * Ω / (3 * Z ^ 2) := by
      field_simp [hH0, hc, hZne]
    _ = Ω := by
      rw [hZ2]
      field_simp [Real.pi_ne_zero]

/-- **tautological_fixed_point.** The pure substitution statement: NO names.
The literal substitution of the horizon pair into the identity's right-hand
side returns Ω identically -- the fixed point of the map
Ω ↦ 32π a0(Ω)^2/(3 H0^2 c^2) is EVERY Ω (the tautological self-consistency). -/
theorem tautological_fixed_point (Ω Z H0 c : ℝ)
    (hO : 0 < Ω) (hH0 : H0 ≠ 0) (hc : c ≠ 0)
    (hZ2 : Z ^ 2 = 32 * Real.pi / 3) :
    32 * Real.pi *
        (c ^ 2 / (Z * (c / (H0 * Real.sqrt Ω)))) ^ 2 / (3 * H0 ^ 2 * c ^ 2) = Ω := by
  exact horizon_omega_fixed_point Ω (c ^ 2 / (Z * (c / (H0 * Real.sqrt Ω))))
    (c / (H0 * Real.sqrt Ω)) Z H0 c hO hH0 hc rfl rfl hZ2

/-! ## Part 3 -- the tightness statement. -/

/-- **closure_iff_zSq.** The fixed-point closure carries NO slack: the identity
closes IFF the germ squares to Z^2 = 32π/3.  Forward (identity → Z^2):
substitute the horizon pair, cancel the nonzero c^2 H0^2, divide by Ω > 0,
solve the remaining 32π/(3 Z^2) = 1.  Backward: the fixed point.  The germ
identity Z^2 = 32π/3 is therefore EXACTLY equivalent to the cosmological
self-consistency of the G058 identity at the horizon footing. -/
theorem closure_iff_zSq (Ω a0 R_dS Z H0 c : ℝ)
    (hO : 0 < Ω) (hZ : Z ≠ 0) (hH0 : H0 ≠ 0) (hc : c ≠ 0)
    (hR : R_dS = c / (H0 * Real.sqrt Ω)) (ha : a0 = c ^ 2 / (Z * R_dS)) :
    (32 * Real.pi * a0 ^ 2 / (3 * H0 ^ 2 * c ^ 2) = Ω) ↔ (Z ^ 2 = 32 * Real.pi / 3) := by
  constructor
  · intro h
    have hsqrt_ne : Real.sqrt Ω ≠ 0 := (Real.sqrt_pos.2 hO).ne'
    have ha' : a0 = c * H0 * Real.sqrt Ω / Z :=
      a0_horizon_reexpression Ω a0 R_dS Z H0 c hO.le hZ hH0 hc hsqrt_ne hR ha
    have h1 : (c * H0 * Real.sqrt Ω) ^ 2 = c ^ 2 * H0 ^ 2 * Ω := by
      calc
        (c * H0 * Real.sqrt Ω) ^ 2 = (c * H0) ^ 2 * (Real.sqrt Ω) ^ 2 := by rw [mul_pow]
        _ = c ^ 2 * H0 ^ 2 * (Real.sqrt Ω) ^ 2 := by rw [mul_pow]
        _ = c ^ 2 * H0 ^ 2 * Ω := by rw [Real.sq_sqrt hO.le]
    have hred : 32 * Real.pi * a0 ^ 2 / (3 * H0 ^ 2 * c ^ 2)
        = 32 * Real.pi * Ω / (3 * Z ^ 2) := by
      rw [ha']
      rw [div_pow]
      rw [h1]
      field_simp [hH0, hc, hZ]
    rw [hred] at h
    have h2 : 32 * Real.pi / (3 * Z ^ 2) = 1 := by
      have h3 : (32 * Real.pi / (3 * Z ^ 2)) * Ω = Ω := by
        calc
          (32 * Real.pi / (3 * Z ^ 2)) * Ω = 32 * Real.pi * Ω / (3 * Z ^ 2) := by ring
          _ = Ω := h
      exact mul_right_cancel₀ hO.ne'
        (by
          calc
            (32 * Real.pi / (3 * Z ^ 2)) * Ω = Ω := h3
            _ = 1 * Ω := by ring)
    have h3Z2ne : 3 * Z ^ 2 ≠ 0 :=
      mul_ne_zero (by norm_num : (3 : ℝ) ≠ 0) (pow_ne_zero 2 hZ)
    have h4 : 32 * Real.pi = 3 * Z ^ 2 := by
      calc
        32 * Real.pi = 32 * Real.pi / (3 * Z ^ 2) * (3 * Z ^ 2) :=
          (div_mul_cancel₀ (32 * Real.pi) h3Z2ne).symm
        _ = 1 * (3 * Z ^ 2) := by rw [h2]
        _ = 3 * Z ^ 2 := by ring
    calc
      Z ^ 2 = (3 * Z ^ 2) / 3 := by
        field_simp [(by norm_num : (3 : ℝ) ≠ 0)]
      _ = 32 * Real.pi / 3 := by rw [← h4]
  · intro hZ2
    exact horizon_omega_fixed_point Ω a0 R_dS Z H0 c hO hH0 hc hR ha hZ2

/-! ## Part 4 -- the numeric anchor at the committed constants. -/

/-- **num_horizon_omega_exact.** At the committed constants (H0 = 67.4 km/s/Mpc
in SI, c = 299792458, Ω = 0.685) the horizon pair
(R_dS = c/(H0√Ω), a0_H = c^2/(Z R_dS), Z = 2√(8π/3)) substituted into the G058
identity returns 0.685 EXACTLY -- the tautology; stronger than the registered
"0.685 to 1e-4".  Every component cancels: the result is independent of the
NUMERIC values of c and H0. -/
theorem num_horizon_omega_exact :
    32 * Real.pi *
        ((299792458 ^ 2 / (2 * Real.sqrt (8 * Real.pi / 3) *
            (299792458 / ((67.4 * 1000 / 3.085677581e22) * Real.sqrt (0.685 : ℝ))))) ^ 2)
          / (3 * (67.4 * 1000 / 3.085677581e22) ^ 2 * 299792458 ^ 2) = (0.685 : ℝ) := by
  have hH0p : 0 < (67.4 * 1000 / 3.085677581e22 : ℝ) := by positivity
  exact horizon_omega_fixed_point (0.685 : ℝ)
    (299792458 ^ 2 /
      (2 * Real.sqrt (8 * Real.pi / 3) *
        (299792458 / ((67.4 * 1000 / 3.085677581e22) * Real.sqrt (0.685 : ℝ)))))
    (299792458 / ((67.4 * 1000 / 3.085677581e22) * Real.sqrt (0.685 : ℝ)))
    (2 * Real.sqrt (8 * Real.pi / 3)) (67.4 * 1000 / 3.085677581e22) 299792458
    (by norm_num : 0 < (0.685 : ℝ)) hH0p.ne'
    (by norm_num : (299792458 : ℝ) ≠ 0) rfl rfl zSq

/-- **num_horizon_omega_close.** The registered numeric claim: at the committed
constants the horizon reconstruction of Ω_Lambda differs from 0.685 by LESS
than 1e-4 (it is in fact exactly 0.685; the claim is certified as 1e-4). -/
theorem num_horizon_omega_close :
    |32 * Real.pi *
        ((299792458 ^ 2 / (2 * Real.sqrt (8 * Real.pi / 3) *
            (299792458 / ((67.4 * 1000 / 3.085677581e22) * Real.sqrt (0.685 : ℝ))))) ^ 2)
          / (3 * (67.4 * 1000 / 3.085677581e22) ^ 2 * 299792458 ^ 2) - (0.685 : ℝ)|
      < 0.0001 := by
  rw [num_horizon_omega_exact, sub_self, abs_zero]
  norm_num

#print axioms zSq
#print axioms zSq_named
#print axioms a0_horizon_reexpression
#print axioms horizon_omega_fixed_point
#print axioms tautological_fixed_point
#print axioms closure_iff_zSq
#print axioms num_horizon_omega_exact
#print axioms num_horizon_omega_close