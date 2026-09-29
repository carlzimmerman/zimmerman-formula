import Mathlib
import H1_bpst
import H2_s4_euler
import H3_horizon_area_lambda
import H4_graviton
import H5_freefall
import H6_nonembed
import H7_p09_reduction

open Real

/-!
# Bridges32pi -- which theorem certifies which arrow between the instances of 32 pi and the puzzle

Conventions: c = G = 1; a0 > 0 the acceleration; L > 0 the de Sitter radius; Lambda = 3/L^2; rho = Lambda/(8 pi);
Z = 1/(a0 L); A_a0 = pi/a0^2 (area of the Schwarzschild horizon of surface gravity a0, r_s = 1/(2 a0)).

WHAT LEAN CERTIFIES HERE: premises => conclusions, i.e. exact real-analysis and algebra.  It certifies NO physical law.
In particular NOTHING in this directory certifies kappa = 1/2 or a0 = sqrt(G rho)/2 as physics.  The puzzle relation is an
INPUT of every equivalence below; Lean shows that the instances of "32 pi" are the same number/statement, not that nature obeys it.

| # | arrow (premise => conclusion)                                                        | theorem(s)                                            | file |
|---|--------------------------------------------------------------------------------------|-------------------------------------------------------|------|
| 1 | BPST density 192 rho^4 r^3/(r^2+rho^2)^4: int_0^inf = 16 for EVERY rho > 0            | `bpst_radial_integral`, `bpst_partial_integral`        | H1   |
| 1'| Vol(S^3) = 2 pi^2 (sine powers), so Vol(S^3) * 16 = 32 pi^2, instanton number 1       | `volS3_eq`, `bpst_total_action`, `bpst_instanton_number`| H1   |
| 1"| size independence (scale-free)                                                        | `bpst_size_independent`                                | H1   |
| 2 | Vol(S^4_L) = 8 pi^2 L^4/3 (sin^3, sin^2, sin, 2 pi integrals)                         | `volS4_eq`                                             | H2   |
| 2'| E4 = R^2 - 4 Ric^2 + Riem^2 = 24/L^4 on the constant-curvature Riemann tensor         | `scal_eq`, `ric2_eq`, `riem2_eq`, `E4_eq`              | H2   |
| 2"| int_{S^4_L} E4 = 64 pi^2 = 32 pi^2 chi (chi = 2 declared), for every L                | `s4_euler_integral`, `s4_euler_number`, `s4_euler_scale_free` | H2 |
| 2"'| 32 pi^2 = 12 Vol(S^4_1) = int R dV = (8 pi)(4 pi) = 2 (4 pi)^2                        | `gb_unit_is_scalar_curvature_integral`, `gb_constant_factorisation` | H2 |
| 3 | Z^2 = 32 pi/3  <=>  A_a0 Lambda = 32 pi^2                                             | `Zsq_iff_A_Lambda`                                     | H3   |
| 3'| A_a0 Lambda = 32 pi^2  <=>  Lambda = 32 pi a0^2                                       | `A_Lambda_iff`                                         | H3   |
| 3"| Lambda = 32 pi a0^2  <=>  G rho = 4 a0^2 (rho = Lambda/8 pi)  <=>  a0 = sqrt(G rho)/2 | `Lambda_iff_G_rho`, `G_rho_iff_a0_half_sqrt`           | H3   |
| 3"'| Lambda = 32 pi a0^2  <=>  rho r_s^2 = 1 (horizon Gauss curvature = rho)               | `Lambda_iff_curvature_density`                         | H3   |
| 3''''| A_a0 = 4 Vol(S^4_L)/L^2 = (4/3) Lambda Vol  <=>  Z^2 = 32 pi/3                     | `A_eq_4Vol_iff`, `four_thirds_Lambda_Vol`              | H3   |
| 3^5| kappa^2 = rho_Lambda (a0^2 = Lambda/8 pi) gives 8 pi/3 instead (4x smaller); 32 pi/3 irrational | `Zsq_kappa_match_gives_8pi_over_3`, `Zsq_irrational` | H3 |
| 4 | kappa_g^2 = 32 pi G  <=>  (1/(64 pi G)) TT action has canonical coefficient 1/2       | `kappa_g_bridge`                                       | H4   |
| 4'| h_ij h_ij = 2 h_+^2 (explicit e^+); phi = h_+/sqrt(16 pi G) canonical                 | `hij_sq_plus`, `hij_sq`, `canonical_plus`, `canonical_lagrangian_plus` | H4 |
| 4"| Isaacson: <hdot_ij hdot_ij>/(32 pi G) = w^2 h0^2/(32 pi G) (avg sin^2 = 1/2), both polarisations | `isaacson_plus`, `isaacson_both`, `avg_sin_sq`        | H4   |
| 4"'| canonical scalar energy density = the Isaacson value                                  | `canonical_energy_matches_isaacson`                    | H4   |
| 5 | int_0^1 sqrt(x/(1-x)) dx = pi/2                                                       | `int_sqrt_ratio`                                       | H5   |
| 5'| t_ff = int dr/sqrt(2GM(1/r-1/r0)) = (pi/2) sqrt(r0^3/(2GM)) = sqrt(3 pi/(32 G rho))   | `tff_eq`, `tff_uniform`, `tff_sq_uniform`              | H5   |
| 5"| independent check: the cycloid solves the energy equation and lands at the same time  | `cycloid_energy`, `cycloid_landing`                    | H5   |
| 6 | r_s = Z L/2 > L iff Z > 2; the puzzle Z = sqrt(32 pi/3) > 2                            | `rs_gt_L_iff`, `puzzle_rs_gt_L`                        | H6   |
| 6'| M_s/M_Nariai = 3 sqrt3 Z/4 = 3 sqrt(32 pi)/4 > 7.5; SdS has NO horizon (and does for M <= M_N) | `mass_ratio_formula`, `mass_ratio_puzzle`, `puzzle_no_sds_horizon`, `sds_horizon_exists` | H6 |
| 6"| area ratio A_s/A_dS = 8 pi/3 > 1                                                       | `area_ratio_puzzle`                                    | H6   |
| 6"'| Israel wall: 1/R^2 >= max(H_in^2, H_out^2); pure tension 1/R^2 = H^2 + (2 pi sigma)^2; no wall at a0 = H/Z | `israel_closed_form`, `israel_bound`, `israel_pure_tension`, `no_wall_at_a0` | H6 |
| 6''''| embeddable iff kappa >= sqrt(2 pi/3) ~ 1.447 (NOT kappa >= 1); kappa = 1 is not embeddable | `embeddable_iff_kappa`, `kappa_one_not_embeddable`  | H6   |
| 7 | vacuum self-consistency: G rho = a0^2 U_v/(8 pi); G rho = 4 a0^2 <=> U_v = 32 pi      | `selfconsistency_iff`                                  | H7   |
| 7'| 32 pi irrational; quadratic rational potentials cannot give U_v = 32 pi; general polynomial potentials cannot IF pi is transcendental (hypothesis; Lindemann is not in Mathlib) | `Uv_irrational`, `quadratic_potential_no_32pi`, `polynomial_potential_no_32pi` | H7 |
| 8 | the web: the puzzle statements are one statement (TFAE)                                | `puzzle_web`                                           | here |
| 9 | the constant 32 pi^2 of arrows 1, 2, 3 is one number                                   | `constant_32pi2`                                       | here |
| 10| relabelling Lambda = 32 pi a0^2 as Lambda = kappa_g^2 a0^2 (G = 1): bookkeeping         | `puzzle_in_kappa_g_form`                               | here |
| 11| t_ff^2 = (3 pi/32) r_s^2 when G rho r_s^2 = 1                                          | `tff_sq_over_rs_sq`                                    | here |
| 12| the puzzle horizon does not fit: r_s > L from Z^2 = 32 pi/3                            | `web_rs_gt_L`                                          | here |

NOT certified (declared inputs, no Lean content): the Riemann/curvature computation on the round sphere as a metric (E4 is computed
from the constant-curvature form R_abcd = k (g_ac g_bd - g_ad g_bc) in an orthonormal frame, not from a metric); the SU(2) field strength of the
BPST instanton (only its radial profile); the Einstein-Hilbert TT expansion (the coefficient 1/(64 pi G) is the input); Gauss-Bonnet itself
(chi = 2 is declared); the Israel junction equation A - B = 4 pi sigma (input); the Schwarzschild-de Sitter metric function f(r) (input);
the energy equation (1/2) rdot^2 = G M (1/r - 1/r0) (input).  And of course: kappa = 1/2, a0 = sqrt(G rho)/2, the value of a0 -- physics, not certified.
-/

/-- The puzzle web (G = c = 1, Lambda = 3/L^2, rho = Lambda/(8 pi), U_v = Lambda/a0^2, r_s = 1/(2 a0)):
these nine statements are equivalent.  Each arrow is one theorem of H3 / H7 (see the table). -/
theorem puzzle_web {a0 L : ℝ} (ha : 0 < a0) (hL : 0 < L) :
    List.TFAE [
      (1 / (a0 * L)) ^ 2 = 32 * π / 3,                                  -- 1  Z^2 = 32 pi/3
      (π / a0 ^ 2) * (3 / L ^ 2) = 32 * π ^ 2,                          -- 2  A Lambda = 32 pi^2
      3 / L ^ 2 = 32 * π * a0 ^ 2,                                      -- 3  Lambda = 32 pi a0^2
      (3 / L ^ 2) / (8 * π) = 4 * a0 ^ 2,                              -- 4  G rho = 4 a0^2
      (a0 ^ 2 * ((3 / L ^ 2) / a0 ^ 2)) / (8 * π) = 4 * a0 ^ 2,        -- 5  same, via U_v = Lambda/a0^2
      (3 / L ^ 2) / a0 ^ 2 = 32 * π,                                    -- 6  U_v = 32 pi
      π / a0 ^ 2 = 4 * volS4 L / L ^ 2,                                 -- 7  A_a0 = 4 Vol(S^4)/L^2
      π / a0 ^ 2 = (4 / 3) * (3 / L ^ 2) * volS4 L,                     -- 8  A_a0 = (4/3) Lambda Vol
      ((3 / L ^ 2) / (8 * π)) * (1 / (2 * a0)) ^ 2 = 1,                 -- 9  rho r_s^2 = 1
      a0 = (1 / 2) * Real.sqrt ((3 / L ^ 2) / (8 * π)) ] := by          -- 10 a0 = sqrt(G rho)/2
  have ha0 : a0 ≠ 0 := ha.ne'
  have hL0 : L ≠ 0 := hL.ne'
  have hp := Real.pi_pos
  have hU : a0 ^ 2 * ((3 / L ^ 2) / a0 ^ 2) = 3 / L ^ 2 := by field_simp
  have hUv : (3 / L ^ 2) / a0 ^ 2 = 32 * π ↔ 3 / L ^ 2 = 32 * π * a0 ^ 2 := by
    rw [div_eq_iff (by positivity)]
  tfae_have 1 ↔ 2 := Zsq_iff_A_Lambda ha hL
  tfae_have 2 ↔ 3 := A_Lambda_iff ha
  tfae_have 3 ↔ 4 := Lambda_iff_G_rho
  tfae_have 4 ↔ 5 := by rw [hU]
  tfae_have 5 ↔ 6 := by rw [hU]; exact Lambda_iff_G_rho.symm.trans hUv.symm
  tfae_have 7 ↔ 1 := A_eq_4Vol_iff ha hL
  tfae_have 7 ↔ 8 := by rw [four_thirds_Lambda_Vol hL0]
  tfae_have 9 ↔ 3 := (Lambda_iff_curvature_density ha).symm
  tfae_have 10 ↔ 4 := by
    have h0 : 0 ≤ (3 / L ^ 2) / (8 * π) := by positivity
    exact (G_rho_iff_a0_half_sqrt ha h0).symm
  tfae_finish

/-- 32 pi^2 is one number across arrows 1, 2, 3: BPST action (Vol S^3 * 16), Gauss-Bonnet integral / chi, A_a0 Lambda. -/
theorem constant_32pi2 :
    (∀ ρ : ℝ, 0 < ρ → volS3 * ∫ r in Set.Ioi (0:ℝ), bpstRadial ρ r = 32 * π ^ 2) ∧
    (∀ L : ℝ, L ≠ 0 → E4 (1 / L ^ 2) * volS4 L = 32 * π ^ 2 * 2) ∧
    (∀ a0 L : ℝ, 0 < a0 → 0 < L → (1 / (a0 * L)) ^ 2 = 32 * π / 3 → (π / a0 ^ 2) * (3 / L ^ 2) = 32 * π ^ 2) := by
  refine ⟨fun ρ hρ => bpst_total_action hρ, fun L hL => s4_euler_number hL, ?_⟩
  intro a0 L ha hL h
  exact (Zsq_iff_A_Lambda ha hL).mp h

/-- bookkeeping only: with G = 1 and kappa_g^2 = 32 pi G, the puzzle Lambda = 32 pi a0^2 reads Lambda = kappa_g^2 a0^2.
This relabels the same 32 pi (it is NOT evidence that the graviton coupling and a0 are related). -/
theorem puzzle_in_kappa_g_form {κ Λ a0 : ℝ} (h : κ ^ 2 = 32 * π * 1) : Λ = 32 * π * a0 ^ 2 ↔ Λ = κ ^ 2 * a0 ^ 2 := by
  rw [h]; constructor <;> intro h' <;> linarith

/-- t_ff^2 = (3 pi/32) r_s^2 when G rho r_s^2 = 1 (r_s = 1/(2 a0), G rho = 4 a0^2): the free-fall time of the vacuum density
is a fixed fraction of the horizon light-crossing time. -/
theorem tff_sq_over_rs_sq {G ρ r0 a0 : ℝ} (hG : 0 < G) (hρ : 0 < ρ) (hr : 0 < r0) (ha : 0 < a0)
    (h : G * ρ = 4 * a0 ^ 2) :
    tff G ((4 * π / 3) * ρ * r0 ^ 3) r0 ^ 2 = (3 * π / 32) * (1 / (2 * a0)) ^ 2 := by
  have hp := Real.pi_pos
  rw [tff_sq_uniform hG hρ hr]
  have : 32 * G * ρ = 128 * a0 ^ 2 := by nlinarith [h]
  rw [this]
  have : a0 ≠ 0 := ha.ne'
  field_simp; ring

/-- from Z^2 = 32 pi/3 the puzzle horizon is larger than the de Sitter radius: L < r_s = 1/(2 a0) -/
theorem web_rs_gt_L {a0 L : ℝ} (ha : 0 < a0) (hL : 0 < L) (h : (1 / (a0 * L)) ^ 2 = 32 * π / 3) :
    L < 1 / (2 * a0) := by
  have hZ : 1 / (a0 * L) = Zpuz := by
    unfold Zpuz; rw [← h, Real.sqrt_sq (by positivity)]
  have h2 := Zpuz_gt_two
  rw [← hZ] at h2
  have hal : 0 < a0 * L := by positivity
  rw [lt_div_iff₀ hal] at h2
  rw [lt_div_iff₀ (by positivity)]
  nlinarith

#print axioms puzzle_web
#print axioms constant_32pi2
#print axioms puzzle_in_kappa_g_form
#print axioms tff_sq_over_rs_sq
#print axioms web_rs_gt_L
