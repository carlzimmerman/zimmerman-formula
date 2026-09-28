import Mathlib

/-!
# AS016 — Pressure mapping versus density mapping (certificate)

Framework base (adopted inputs, NOT derived here):
    a0 = kappa * c * sqrt(G * rho_Lambda),  kappa = 1/2 adopted
    rho_Lambda = 4 a0^2 / (G c^2),   eps_Lambda = rho_Lambda c^2 = 4 a0^2 / G
    r_M = sqrt(G M_b / a0),  C = sqrt(G M_b a0),  v_flat^2 = C
Deep-equilibrium CONDITIONAL TARGETS (not free laws):
    sigma^2 = C/2,  rho_ph(r) = C / (4 pi G r^2),  P = sigma^2 rho_ph.

What is certified (real arithmetic, positive-domain hypotheses):

1. `density_scale_identity` — the framework scale IS the density mapping:
       a0^2 = (G/4) * eps_Lambda,  i.e.  a0^2 proportional to the vacuum
   ENERGY DENSITY with coefficient G/4, with NO equation-of-state (w)
   dependence.  This is the density map; the pressure map is the candidate
       a_p^2 = (G/4) * (-w) * eps_DE,  p_DE = w eps_DE.

2. `pressure_identity` — the deep-equilibrium pressure target reduces to the
   exact algebraic core of the task:
       P * (8 pi r^2) = M_b a0,   i.e.  P = M_b a0 / (8 pi r^2).

3. `surface_phantom_mass` — the per-shell phantom surface density is r-free:
       (4 pi r^2 rho_ph) * G = C.

4. `pressure_at_milgrom_radius` — at r = r_M = sqrt(G M_b / a0):
       P * (8 pi G) = a0^2   (equivalently P(r_M) = a0^2/(8 pi G)).

5. `P_at_rM_eps_over_32pi` — with eps_Lambda = 4 a0^2 / G:
       P(r_M) * 32 pi = eps_Lambda,  i.e.  P(r_M) = eps_Lambda / (32 pi),
   so the phantom "pressure" at the MOND radius is only 1/(32 pi) of the
   vacuum energy density: the density channel dominates the pressure
   channel by a factor 32 pi at r_M (and by 32 pi (r/r_M)^2 elsewhere).

6. `ratio_pressure_density` — the two maps stand in the exact ratio
       a_p^2 = (-w) * a_rho^2.

7. `agreement_iff_w_eq_neg_one` — for a_rho^2 != 0, the pressure map equals
   the density map IF AND ONLY IF w = -1 (the cosmological-constant locus):
       (a_p^2 = a_rho^2)  <->  w = -1.
   This is the degeneracy audit: the masquerade is exact only on w = -1.

8. `relative_evolution_extra_factor` — the relative scale evolution carries
   the extra factor w(z)/w(0):
       (a_p^2(z)/a_p^2(0)) / (a_rho^2(z)/a_rho^2(0)) = w(z)/w(0).

These certify the algebra of the two-scale comparison only.  They do not
derive kappa = 1/2, do not fix the physical value of rho_Lambda, and do not
establish the w(z) evolution of any cosmological model; observational
discrimination of the two maps requires a measured w(z) window with
w(z) != w(0) and the fixed normalization K_p = G/4.
-/

open Real

/-- The framework scale is the DENSITY map: a0^2 = (G/4) eps_Lambda. -/
theorem density_scale_identity {a0 G c rhoL epsL : ℝ}
    (hG : 0 < G) (hc : 0 < c)
    (hrho : rhoL = 4 * a0 ^ 2 / (G * c ^ 2))
    (heps : epsL = rhoL * c ^ 2) :
    a0 ^ 2 = (G / 4) * epsL := by
  rw [heps, hrho]
  field_simp [ne_of_gt hG, ne_of_gt hc]

/-- P = sigma^2 rho_ph is exactly M_b a0 / (8 pi r^2):
    P * (8 pi r^2) = M_b a0. -/
theorem pressure_identity {G M a0 r C s2 rho P : ℝ}
    (hG : 0 < G) (hr : 0 < r)
    (hC : C ^ 2 = G * M * a0)
    (hs2 : s2 = C / 2)
    (hrho : rho = C / (4 * Real.pi * G * r ^ 2))
    (hP : P = s2 * rho) :
    P * (8 * Real.pi * r ^ 2) = M * a0 := by
  rw [hP, hs2, hrho]
  field_simp [ne_of_gt hG, ne_of_gt hr, Real.pi_pos.ne']
  rw [hC]
  ring

/-- The per-shell phantom surface density is r-independent:
    (4 pi r^2 rho_ph) * G = C. -/
theorem surface_phantom_mass {G r C rho : ℝ}
    (hG : 0 < G) (hr : 0 < r)
    (hrho : rho = C / (4 * Real.pi * G * r ^ 2)) :
    (4 * Real.pi * r ^ 2 * rho) * G = C := by
  rw [hrho]
  field_simp [ne_of_gt hG, ne_of_gt hr, Real.pi_pos.ne']

/-- At the MOND radius r_M^2 = G M_b / a0, the phantom pressure target is
    fixed by (a0, G) alone:  P * (8 pi G) = a0^2. -/
theorem pressure_at_milgrom_radius {G M a0 rM P : ℝ}
    (hG : 0 < G) (hM : 0 < M) (ha : 0 < a0)
    (hrM : rM ^ 2 = G * M / a0)
    (hpr : P * (8 * Real.pi * rM ^ 2) = M * a0) :
    P * (8 * Real.pi * G) = a0 ^ 2 := by
  rw [hrM] at hpr
  -- hpr : P * (8 * pi * (G * M / a0)) = M * a0
  have hm : (P * (8 * Real.pi * (G * M / a0))) * a0 = (M * a0) * a0 := by
    exact congrArg (fun x : ℝ => x * a0) hpr
  have hm2 : P * (8 * Real.pi * G * M) = (M * a0) * a0 := by
    calc
      P * (8 * Real.pi * G * M) = P * ((8 * Real.pi * (G * M / a0)) * a0) := by
        field_simp [ne_of_gt hG, ne_of_gt hM, ne_of_gt ha]
      _ = (P * (8 * Real.pi * (G * M / a0))) * a0 := by ring
      _ = (M * a0) * a0 := hm
  have hc : (P * (8 * Real.pi * G)) * M = (a0 * a0) * M := by
    calc
      (P * (8 * Real.pi * G)) * M = P * ((8 * Real.pi * G) * M) := by ring
      _ = P * (8 * Real.pi * G * M) := by ring
      _ = (M * a0) * a0 := hm2
      _ = M * (a0 * a0) := by ring
      _ = (a0 * a0) * M := by ring
  have hpg : P * (8 * Real.pi * G) = a0 * a0 := mul_right_cancel₀ (ne_of_gt hM) hc
  rw [sq]
  exact hpg

/-- With eps_Lambda = 4 a0^2 / G:  P(r_M) * 32 pi = eps_Lambda,
    i.e. the phantom pressure at the MOND radius is 1/(32 pi) of the
    vacuum energy density. -/
theorem P_at_rM_eps_over_32pi {G a0 epsL P : ℝ}
    (hG : 0 < G)
    (heps : epsL = 4 * a0 ^ 2 / G)
    (hP : P * (8 * Real.pi * G) = a0 ^ 2) :
    P * (32 * Real.pi) = epsL := by
  have hL : (P * (32 * Real.pi)) * G = epsL * G := by
    calc
      (P * (32 * Real.pi)) * G = P * (32 * Real.pi * G) := by ring
      _ = P * (4 * (8 * Real.pi * G)) := by ring
      _ = 4 * (P * (8 * Real.pi * G)) := by ring
      _ = 4 * a0 ^ 2 := by rw [hP]
      _ = epsL * G := by
        rw [heps]
        field_simp [ne_of_gt hG]
  exact mul_right_cancel₀ (ne_of_gt hG) hL

/-- the two maps stand in the exact ratio: a_p^2 = (-w) * a_rho^2. -/
theorem ratio_pressure_density {G w eps ap2 ar2 : ℝ}
    (hap2 : ap2 = (G / 4) * (-w) * eps)
    (har2 : ar2 = (G / 4) * eps) :
    ap2 = (-w) * ar2 := by
  rw [hap2, har2]
  ring

/-- Degeneracy audit: with a_rho^2 != 0, the pressure map reproduces the
    density map IF AND ONLY IF w = -1. -/
theorem agreement_iff_w_eq_neg_one {w ap2 ar2 : ℝ}
    (hne : ar2 ≠ 0) (hr : ap2 = (-w) * ar2) :
    (ap2 = ar2 ↔ w = -1) := by
  constructor
  · intro h
    have h2 : (-w) * ar2 = 1 * ar2 := by
      rw [← hr]
      rw [h]
      simp
    have hw' : -w = 1 := mul_right_cancel₀ hne h2
    linarith
  · intro hw
    calc
      ap2 = (-w) * ar2 := hr
      _ = 1 * ar2 := by
        have hw' : -w = 1 := by linarith
        rw [hw']
      _ = ar2 := by simp

/-- Relative scale evolution: the pressure map gains the extra factor
    w(z)/w(0) over the density map between two epochs. -/
theorem relative_evolution_extra_factor {G eps wz w0 apz2 ap02 arz2 ar02 : ℝ}
    (hG : G ≠ 0) (he : eps ≠ 0) (hwz : wz ≠ 0) (hw0 : w0 ≠ 0)
    (hEp : apz2 = (G / 4) * (-wz) * eps)
    (hE0 : ap02 = (G / 4) * (-w0) * eps)
    (hRz : arz2 = (G / 4) * eps)
    (hR0 : ar02 = (G / 4) * eps) :
    (apz2 / ap02) / (arz2 / ar02) = wz / w0 := by
  rw [hEp, hE0, hRz, hR0]
  field_simp [hG, he, hwz, hw0]

#print axioms density_scale_identity
#print axioms pressure_identity
#print axioms surface_phantom_mass
#print axioms pressure_at_milgrom_radius
#print axioms P_at_rM_eps_over_32pi
#print axioms ratio_pressure_density
#print axioms agreement_iff_w_eq_neg_one
#print axioms relative_evolution_extra_factor