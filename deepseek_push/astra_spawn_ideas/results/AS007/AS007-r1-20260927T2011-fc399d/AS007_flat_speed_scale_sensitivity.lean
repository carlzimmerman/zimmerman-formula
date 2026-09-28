import Mathlib
import Mathlib.Tactic

/-
  AS007 -- Flat speed and scale sensitivity (house-style Lean certificate).

  Framework (inputs adopted, not derived here):
    a0 = kappa * c * sqrt(G_E * rho_Lambda),   kappa = 1/2
    deep conditional law:  v_flat^4 = G_N * M_b * a0
    (deep limit g^2 -> a0 * g_N of the operative RAR/MONO branch; MONO == RAR
     identically on y <= y* = 2.3374, so the y -> 0 deep law is shared by the
     operative branch without any branch translation).

  Content certified here (pure algebra, no calculus):
    (1) four_power_eq      -- encoding equivalence: v^4 = G*M*a0  iff
                              v^2 = sqrt(G*M*a0)  (for G,M,a0 > 0);
    (2) footing_ratio      -- same (G,M): the ratio of predicted flat speeds for
                              two a0 footings is exactly (a0'/a0)^(1/4)
                              (w/v = sqrt(sqrt(a1/a0))), independent of G and M;
    (3) scaling_sensitivity-- the exact sensitivity law: rescaling
                              (G,M,a0) by (lam,mu,nu) multiplies v_flat by
                              (lam*mu*nu)^(1/4) -- i.e. log-elasticity
                              1/4 in EACH of G, M_b, a0;
    (4) rho_elasticity     -- resolved form v^2 = sqrt(K*sqrt(rho)):
                              rescaling rho by lambda multiplies v by
                              lambda^(1/8) (exponent 1/8 = (1/2)*(1/4));
    (5) resolved_form      -- substitution identity with G_N (acceleration
                              sector) and G_E (vacuum curvature sector) carried
                              as SEPARATE symbols:
                              v^4 = G_N*M*a0, a0 = kappa*c*sqrt(G_E*rho)
                              ==> v^4 = kappa*c*G_N*M*sqrt(G_E)*sqrt(rho);
    (6) resolved_same_coupling -- same-G matching-condition reduction
                              (G_E = G_N: then e_G total = 3/8 in the log);
    (7) mock_law_discriminates -- the deliberate SQUARE-ROOT speed law
                              w = sqrt(G*M*a0) has mass-doubling ratio sqrt 2,
                              which is NOT equal to the fourth-root law's
                              2^(1/4) = sqrt(sqrt 2): the mass-scaling test
                              discriminates the wrong law (negative control).

  Axiom check: see #print axioms in the .out file; the proofs use only the
  Mathlib standard set ({propext, Classical.choice, Quot.sound}).
-/

noncomputable section
open Real

/-- (1) Equivalent encodings of the deep-law statement. -/
theorem four_power_eq {v G M a0 : ℝ} (hG : 0 < G) (hM : 0 < M) (ha0 : 0 < a0) :
    v ^ 4 = G * M * a0 ↔ v ^ 2 = Real.sqrt (G * M * a0) := by
  have hX : 0 ≤ G * M * a0 := le_of_lt (mul_pos (mul_pos hG hM) ha0)
  constructor
  · intro h
    have hsqv : v ^ 2 = Real.sqrt (v ^ 4) := by
      calc
        v ^ 2 = Real.sqrt ((v ^ 2) ^ 2) := (Real.sqrt_sq (sq_nonneg v)).symm
        _ = Real.sqrt (v ^ 4) := by
          congr 1
          ring
    rw [h] at hsqv
    exact hsqv
  · intro h
    calc
      v ^ 4 = (v ^ 2) ^ 2 := by ring
      _ = (Real.sqrt (G * M * a0)) ^ 2 := by rw [h]
      _ = G * M * a0 := Real.sq_sqrt hX

/-- (2) Footing ratio: v_flat'(a0')/v_flat(a0) = (a0'/a0)^(1/4),
      independent of G and M. -/
theorem footing_ratio {G M a0 a1 v w : ℝ} (hG : 0 < G) (hM : 0 < M)
    (ha0 : 0 < a0) (ha1 : 0 < a1) (hv : 0 ≤ v) (hw : 0 ≤ w)
    (hv2 : v ^ 2 = Real.sqrt (G * M * a0))
    (hw2 : w ^ 2 = Real.sqrt (G * M * a1)) :
    w / v = Real.sqrt (Real.sqrt (a1 / a0)) := by
  have hgmp : 0 < G * M := mul_pos hG hM
  have hX : 0 < G * M * a0 := mul_pos hgmp ha0
  have hY : 0 < G * M * a1 := mul_pos hgmp ha1
  have hvne : v ≠ 0 := by
    intro hv0
    have h : Real.sqrt (G * M * a0) = 0 := by
      rw [← hv2, hv0]
      norm_num
    have hz : G * M * a0 = 0 := (Real.sqrt_eq_zero (le_of_lt hX)).mp h
    exact (ne_of_gt hX) hz
  have hvpos : 0 < v := lt_of_le_of_ne hv hvne.symm
  have u2 : (w / v) ^ 2 = Real.sqrt (a1 / a0) := by
    rw [div_pow, hw2, hv2]
    rw [← Real.sqrt_div (le_of_lt hY) (G * M * a0)]
    congr 1
    field_simp [mul_left_comm, mul_assoc, mul_comm, ne_of_gt hX, ne_of_gt hY,
      ne_of_gt ha0, ne_of_gt ha1]
  have uw : 0 ≤ w / v := div_nonneg hw (le_of_lt hvpos)
  have : Real.sqrt ((w / v) ^ 2) = Real.sqrt (Real.sqrt (a1 / a0)) := by
    rw [u2]
  rwa [Real.sqrt_sq uw] at this

/-- (3) Exact sensitivity (scaling) law: d ln v_flat = (d ln G + d ln M_b
      + d ln a0)/4 in exact multiplicative form. -/
theorem scaling_sensitivity {G M a0 v w lam mu nu : ℝ} (hG : 0 < G)
    (hM : 0 < M) (ha0 : 0 < a0) (hlam : 0 < lam) (hmu : 0 < mu) (hnu : 0 < nu)
    (hv : 0 ≤ v) (hw : 0 ≤ w) (hv2 : v ^ 2 = Real.sqrt (G * M * a0))
    (hw2 : w ^ 2 = Real.sqrt ((lam * G) * (mu * M) * (nu * a0))) :
    w / v = Real.sqrt (Real.sqrt (lam * mu * nu)) := by
  have hgmp : 0 < G * M := mul_pos hG hM
  have hX : 0 < G * M * a0 := mul_pos hgmp ha0
  have hY : 0 < (lam * G) * (mu * M) * (nu * a0) :=
    mul_pos (mul_pos (mul_pos hlam hG) (mul_pos hmu hM)) (mul_pos hnu ha0)
  have hvne : v ≠ 0 := by
    intro hv0
    have h : Real.sqrt (G * M * a0) = 0 := by
      rw [← hv2, hv0]
      norm_num
    have hz : G * M * a0 = 0 := (Real.sqrt_eq_zero (le_of_lt hX)).mp h
    exact (ne_of_gt hX) hz
  have u2 : (w / v) ^ 2 = Real.sqrt (lam * mu * nu) := by
    rw [div_pow, hw2, hv2]
    rw [← Real.sqrt_div (le_of_lt hY) (G * M * a0)]
    congr 1
    field_simp [mul_left_comm, mul_assoc, mul_comm, ne_of_gt hX, ne_of_gt hY]
  have hvpos : 0 < v := lt_of_le_of_ne hv hvne.symm
  have uw : 0 ≤ w / v := div_nonneg hw (le_of_lt hvpos)
  have : Real.sqrt ((w / v) ^ 2) = Real.sqrt (Real.sqrt (lam * mu * nu)) := by
    rw [u2]
  rwa [Real.sqrt_sq uw] at this

/-- (4) Vacuum-density elasticity in the resolved form:
      v^2 = sqrt(K * sqrt rho),  K = kappa*c*G_N*M*sqrt(G_E)  ==> rescaling
      rho by lambda multiplies the flat speed by lambda^(1/8). -/
theorem rho_elasticity {v w K rho lam : ℝ} (hK : 0 < K) (hrho : 0 < rho)
    (hlam : 0 < lam) (hv : 0 ≤ v) (hw : 0 ≤ w)
    (hv2 : v ^ 2 = Real.sqrt (K * Real.sqrt rho))
    (hw2 : w ^ 2 = Real.sqrt (K * Real.sqrt (lam * rho))) :
    w / v = Real.sqrt (Real.sqrt (Real.sqrt lam)) := by
  have hKsq : 0 < K * Real.sqrt rho := mul_pos hK ((Real.sqrt_pos).mpr hrho)
  have hX : 0 < K * Real.sqrt rho := hKsq
  have hvne : v ≠ 0 := by
    intro hv0
    have h : Real.sqrt (K * Real.sqrt rho) = 0 := by
      rw [← hv2, hv0]
      norm_num
    have hz : K * Real.sqrt rho = 0 := (Real.sqrt_eq_zero (le_of_lt hX)).mp h
    exact (ne_of_gt hX) hz
  have u2 : (w / v) ^ 2 = Real.sqrt (Real.sqrt lam) := by
    rw [div_pow, hw2, hv2]
    rw [Real.sqrt_mul (le_of_lt hlam) rho]
    have hre : K * (Real.sqrt lam * Real.sqrt rho) = (K * Real.sqrt rho) * Real.sqrt lam := by
      ring
    rw [hre]
    rw [Real.sqrt_mul (le_of_lt hKsq) (Real.sqrt lam)]
    have hsqrt : 0 < Real.sqrt (K * Real.sqrt rho) := (Real.sqrt_pos).mpr hKsq
    field_simp [ne_of_gt hsqrt]
  have hvpos : 0 < v := lt_of_le_of_ne hv hvne.symm
  have uw : 0 ≤ w / v := div_nonneg hw (le_of_lt hvpos)
  have : Real.sqrt ((w / v) ^ 2) = Real.sqrt (Real.sqrt (Real.sqrt lam)) := by
    rw [u2]
  rwa [Real.sqrt_sq uw] at this

/-- (5) Resolved substitution with G_N (acceleration) and G_E (vacuum
      curvature) as SEPARATE symbols (framework contract: never silently
      identify them). -/
theorem resolved_form {v G_N M a0 kappa c G_E rho : ℝ} (hGE : 0 ≤ G_E)
    (hv4 : v ^ 4 = G_N * M * a0)
    (ha0 : a0 = kappa * c * Real.sqrt (G_E * rho)) :
    v ^ 4 = kappa * c * G_N * M * (Real.sqrt G_E) * (Real.sqrt rho) := by
  rw [ha0] at hv4
  rw [Real.sqrt_mul hGE rho] at hv4
  rw [hv4]
  ring

/-- (6) Same-coupling reduction (the matching condition G_E = G_N): the G
      elasticity then totals (1/4) + (1/8) = 3/8 in the log. -/
theorem resolved_same_coupling {v G M a0 kappa c rho : ℝ} (hG : 0 ≤ G)
    (hv4 : v ^ 4 = G * M * a0)
    (ha0 : a0 = kappa * c * Real.sqrt (G * rho)) :
    v ^ 4 = kappa * c * G * M * (Real.sqrt G) * (Real.sqrt rho) := by
  rw [ha0] at hv4
  rw [Real.sqrt_mul hG rho] at hv4
  rw [hv4]
  ring

/-- (7) Negative control: the deliberate square-root speed law
      w = sqrt(G*M_b*a0) has mass-doubling ratio sqrt(2), which differs from
      the fourth-root law's 2^(1/4) = sqrt(sqrt 2): the mass-scaling test is
      capable of failing the wrong law. -/
theorem mock_law_discriminates : Real.sqrt 2 ≠ Real.sqrt (Real.sqrt 2) := by
  intro h
  have hs : Real.sqrt 2 ^ 2 = Real.sqrt (Real.sqrt 2) ^ 2 := congrArg (· ^ 2) h
  have h2 : 2 = Real.sqrt 2 := by
    rw [Real.sq_sqrt (by norm_num : (0 : ℝ) ≤ 2), Real.sq_sqrt (Real.sqrt_nonneg 2)] at hs
    exact hs
  have hsq : Real.sqrt 2 ^ 2 = 2 ^ 2 := congrArg (· ^ 2) h2.symm
  rw [Real.sq_sqrt (by norm_num : (0 : ℝ) ≤ 2)] at hsq
  norm_num at hsq

end