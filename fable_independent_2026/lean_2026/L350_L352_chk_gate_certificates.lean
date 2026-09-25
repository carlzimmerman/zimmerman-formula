import Mathlib

open Real

/-!
# L350–L352 — C-H/K's lambda-channel against cosmology, and L342's switch against GW170817 and Gauss:
# algebraic certificates

SCOPE. Lean certifies the algebra of
`real_research/g03_audit_2026/L350_chk_cosmological_G_gate.py`,
`real_research/g03_audit_2026/L351_switch_gw170817_gate.py` and
`real_research/g03_audit_2026/L352_switch_gauss_compensation.py`.
The published cosmological fits, the KiDS chi^2 values, the forest ratios and the GW170817 numbers are data or
numerics and are not certified here.

L350
* `gcos_over_gn`: with G_cos = G/(1 + 3c_2/2) (C-H/K's Friedmann equation) and G_N = G/(1 - alpha/2) (its static
  block), G_cos/G_N = (2 - alpha)/(2 + 3c_2).
* `ceiling_iff`: for B < 1 and 2 + 3c_2 > 0, the published bound (alpha + 3c_2)/(2 + 3c_2) < B on 1 - G_cos/G_N is
  exactly c_2 < (2B - alpha)/(3(1 - B)).
* `subtracted_term_on_frw`: the leaf-average-subtracted lambda-term -c_2 (K - <K>)^2 vanishes when K is uniform on the
  leaf (FRW), whatever c_2.

L351
* `tensor_speed`: with the switch contributing eps to the TT gradient term and kappa * eps to the TT kinetic term,
  c_T^2 = (1 + eps)/(1 + kappa eps); kappa = 0 (L342's x = 9R3/(4K^2)) gives 1 + eps, kappa = 1 (the shear-completed
  x~ = 9(R3 + sigma^2)/(4K^2)) gives exactly 1.
* `shell_advance`: in a deep-MOND phantom shell (q = (4/3) s^(3/2), s = x (v H/a0)^2, v^4 = G M a0, K = 3H/c,
  r = v/(H sqrt x)) the integrand of Int (c_T - 1) dr, written against dx, is exactly G M/(6 c^2) f'(x).

L352
* `gauss_beyond_edge`: the switched phantom's enclosed mass r^2 F (nu - 1) g_N / G vanishes wherever the switch
  fraction F is zero, so the enclosed dynamical mass is the baryonic mass there.
* `enclosed_phantom_nondecreasing`: in deep MOND the switch variable is x = X0 (F + F'); if x > 0 and X0 > 0 then
  e^u (F + F') > 0, i.e. d(F e^u)/du > 0: the enclosed phantom cannot decrease where the switch is partly on
  (baryon-free outskirts).
-/

theorem gcos_over_gn {G a c2 : ℝ} (hG : 0 < G) (ha : a < 2) (hc2 : 0 < 2 + 3 * c2) :
    (G / (1 + 3 * c2 / 2)) / (G / (1 - a / 2)) = (2 - a) / (2 + 3 * c2) := by
  have h1 : (1 + 3 * c2 / 2) ≠ 0 := by linarith
  have h2 : (1 - a / 2) ≠ 0 := by linarith
  have h3 : (2 + 3 * c2) ≠ 0 := by linarith
  field_simp

theorem ceiling_iff {a c2 B : ℝ} (hB1 : B < 1) (hc2 : 0 < 2 + 3 * c2) :
    (a + 3 * c2) / (2 + 3 * c2) < B ↔ c2 < (2 * B - a) / (3 * (1 - B)) := by
  have h1B : 0 < 3 * (1 - B) := by linarith
  rw [div_lt_iff₀ hc2, lt_div_iff₀ h1B]
  constructor <;> intro h <;> nlinarith

theorem subtracted_term_on_frw {c2 K Kavg : ℝ} (h : K = Kavg) : -c2 * (K - Kavg) ^ 2 = 0 := by
  rw [h]; ring

theorem tensor_speed {eps kappa : ℝ} (h : 0 < 1 + kappa * eps) :
    (kappa = 0 → (1 + eps) / (1 + kappa * eps) = 1 + eps) ∧
    (kappa = 1 → (1 + eps) / (1 + kappa * eps) = 1) := by
  constructor
  · intro hk; subst hk; simp
  · intro hk; subst hk
    have : (1 + 1 * eps) ≠ 0 := by linarith
    rw [one_mul] at this ⊢
    exact div_self this

theorem shell_advance {G M a0 c H v x sx : ℝ} (ha0 : 0 < a0) (hc : 0 < c) (hH : 0 < H) (hv : 0 < v)
    (hx : 0 < x) (hsx : 0 < sx) (_hsx2 : sx ^ 2 = x) (hv4 : v ^ 4 = G * M * a0) :
    -- (9/8) * 2 alpha^2 q / K^2 * |dr/dx|, with q = (4/3) s sqrt s, s = x (vH/a0)^2 so sqrt s = sqrt x (vH/a0),
    -- alpha = a0/c^2, K = 3H/c, r = v/(H sqrt x), |dr/dx| = v/(2 H x sqrt x); sx = sqrt x cancels structurally,
    -- so the identity holds for any positive sx (the hypothesis _hsx2 records what sx is)
    (9 / 8) * (2 * (a0 / c ^ 2) ^ 2 * ((4 / 3) * (x * (v * H / a0) ^ 2) * (sx * (v * H / a0))) / (3 * H / c) ^ 2)
      * (v / (2 * H * x * sx)) = G * M / (6 * c ^ 2) := by
  have hGM : G * M = v ^ 4 / a0 := by field_simp; linarith
  rw [hGM]
  field_simp
  ring

theorem gauss_beyond_edge {r F nu gN G Mb : ℝ} (hF : F = 0) :
    Mb + r ^ 2 * F * (nu - 1) * gN / G = Mb := by
  rw [hF]; ring

theorem enclosed_phantom_nondecreasing {X0 F dF x u : ℝ} (hX0 : 0 < X0) (hx : x = X0 * (F + dF)) (hpos : 0 < x) :
    0 < Real.exp u * (F + dF) := by
  have h : 0 < F + dF := by
    rw [hx] at hpos
    exact pos_of_mul_pos_right hpos hX0.le
  exact mul_pos (Real.exp_pos u) h

#print axioms gcos_over_gn
#print axioms ceiling_iff
#print axioms subtracted_term_on_frw
#print axioms tensor_speed
#print axioms shell_advance
#print axioms gauss_beyond_edge
#print axioms enclosed_phantom_nondecreasing
