import Mathlib

/-!
# M3D -- the split complex scalar: kick speed, pair-growth eigenvalue, Hubble-sweep integral, trigger exponent,
#        and the channel-closure bound

Source: `real_research/derivation_chain_2026/FP10_internal_splitting_dark_sector.py`, checks A1, A3, A4
(the sympy lines 447-556), and `FP25_constructive_dark_sector.py` check A5 (`partA5`).
None of this is in the Lean corpus: `I27_kick_escape.lean` certifies only the kinematics of a given
kick speed, and `FL2_dark_slot_certificates.lean` only the sign of the splitting energy.

Setting (natural units c = 1): V = (m^2+eps) phi_H^2/2 + (m^2-eps) phi_L^2/2 + lambda phi_H^2 phi_L^2, so
m_H^2 = m^2 + eps, m_L^2 = m^2 - eps.  The masses/vertices are read from V as hypotheses (definitions).

CERTIFIED:
  * `kick_speed_sq`       : if two phi_H at rest annihilate to two phi_L back to back (energy E = m_H each,
                            p^2 = E^2 - m_L^2, v = p/E, E > 0) then  v^2 = 2 eps/(m^2+eps);  and 0 <= v^2 < 1
                            (when m_L^2 >= 0 ... eps <= m^2).
  * `eps_over_m2_of_v`    : eps/m^2 = v^2/(2 - v^2), and conversely v^2 = 2 eps/(m^2+eps) follows from it
                            (m^2 > 0, 0 <= v^2 < 2).
  * `latent_heat_lower`   : with gamma = m_H/m_L,  gamma - 1 - v^2/2 = (gamma-1)^2 (2 gamma+1)/(2 gamma^2) >= 0,
                            so v^2/2 is the leading-order latent heat per unit mass and never exceeds it.
  * `mutate_no_kick`      : eps = 0 gives v = 0 (the script's MUTATE control).
  * `pair_charpoly`       : the block [[D,G],[-G,-D]] has characteristic polynomial lam^2 - (D^2 - G^2);
                            `pair_growth_root`: for |D| < G, lam = i sqrt(G^2 - D^2) is a root with
                            sqrt(G^2 - D^2) > 0, i.e. the eigenvalue is purely imaginary and the mode
                            e^{-i lam t} grows at rate sqrt(G^2 - D^2) (the e^{-i lam t} step is not formalised).
  * `sweep_integral`      : (1/(2 H Delta)) * int_{-G}^{G} sqrt(G^2 - D^2) dD = pi G^2 / (4 H Delta)   (G, H, Delta > 0).
  * `trigger_scaling`     : if n_i solves pi (lam_i n_i/(2 m^2))^2/(4 H_i Delta) = E with
                            lam_i = lam0 (3 H_i/K0)^(-2q)  (positive parameters), then
                            n_2/n_1 = (H_2/H_1)^(2q + 1/2); at q = 7/4 the exponent is 4.
  * `channel_closure`     : k^2 := m_H^2 - m_{L,eff}^2 = 2 eps - lam Phi0^2 with m_{L,eff}^2 = m^2 - eps + lam Phi0^2;
                            with rho = (m^2+eps) Phi0^2/2 and G = lam rho/(2 m^3):  k^2 >= 0 <-> G <= G_block =
                            eps (m^2+eps)/(2 m^3)  (lam, m > 0, m^2+eps > 0);  and G_block/m = v^2/(2-v^2)^2 >= v^2/4.

NOT CERTIFIED: that the rotating-wave reductions (pair vertex lam/(4 m_H m_L), G = lam n_H/(2 m_H m_L)),
the golden-rule halo gain, the Hubble-sweep formula's Landau-Zener-type origin, every numerical value
(575-650 km/s, eps/m^2 = 1.84-2.35e-6, E_need, q = 7/4 all remain FITTED or DECLARED and enter here only as
free variables), the trigger's physics, or any observational gate.  eps is FITTED in the framework; nothing
here derives eps or kappa = 1/2.  No physical claim is an axiom.
-/

noncomputable section
namespace M3D

open Real

/-! ### kick -/

theorem kick_speed_sq (m eps E p v : ℝ) (hE : E ^ 2 = m ^ 2 + eps) (hEpos : 0 < E)
    (hp : p ^ 2 = E ^ 2 - (m ^ 2 - eps)) (hv : v = p / E) :
    v ^ 2 = eps / (m ^ 2 + eps) := by
  have hEne : E ≠ 0 := hEpos.ne'
  have hmH : m ^ 2 + eps ≠ 0 := by rw [← hE]; positivity
  rw [hv, div_pow, hp, hE]
  field_simp
  ring

theorem kick_speed_lt_one (m eps : ℝ) (hm : 0 < m) (hlow : eps < m ^ 2) (hpos : 0 ≤ eps) :
    0 ≤ 2 * eps / (m ^ 2 + eps) ∧ 2 * eps / (m ^ 2 + eps) < 1 := by
  have hd : 0 < m ^ 2 + eps := by positivity
  constructor
  · positivity
  · rw [div_lt_one hd]; linarith

theorem eps_over_m2_of_v (m eps v2 : ℝ) (hm : 0 < m) (hd : 0 < m ^ 2 + eps)
    (hv : v2 = 2 * eps / (m ^ 2 + eps)) (hv2 : v2 < 2) :
    eps / m ^ 2 = v2 / (2 - v2) := by
  have hm2 : m ^ 2 ≠ 0 := by positivity
  have hd' : m ^ 2 + eps ≠ 0 := hd.ne'
  have h2 : 2 - v2 ≠ 0 := by linarith
  have h3 : 2 - v2 = 2 * m ^ 2 / (m ^ 2 + eps) := by
    rw [hv]; field_simp; ring
  rw [h3, hv]
  field_simp

theorem v_of_eps_over_m2 (m eps v2 : ℝ) (hm : 0 < m) (hv2 : v2 < 2)
    (h : eps / m ^ 2 = v2 / (2 - v2)) :
    v2 = 2 * eps / (m ^ 2 + eps) := by
  have hm2 : m ^ 2 ≠ 0 := by positivity
  have h2 : 2 - v2 ≠ 0 := by linarith
  have he : eps * (2 - v2) = v2 * m ^ 2 := by
    field_simp at h; linarith
  have hd : m ^ 2 + eps ≠ 0 := by
    intro h0
    have : eps = -m ^ 2 := by linarith
    rw [this] at he
    have : (-m ^ 2) * (2 - v2) = v2 * m ^ 2 := he
    have : m ^ 2 * 2 = 0 := by nlinarith
    have : (0 : ℝ) < m ^ 2 := by positivity
    linarith
  field_simp
  linarith

theorem latent_heat_lower (gamma v2 : ℝ) (hg : gamma ≠ 0) (hv : v2 = 1 - 1 / gamma ^ 2) :
    gamma - 1 - v2 / 2 = (gamma - 1) ^ 2 * (2 * gamma + 1) / (2 * gamma ^ 2) := by
  rw [hv]
  field_simp
  ring

theorem latent_heat_nonneg (gamma v2 : ℝ) (hg : 1 ≤ gamma) (hv : v2 = 1 - 1 / gamma ^ 2) :
    v2 / 2 ≤ gamma - 1 := by
  have hg0 : gamma ≠ 0 := by positivity
  have h := latent_heat_lower gamma v2 hg0 hv
  have : 0 ≤ (gamma - 1) ^ 2 * (2 * gamma + 1) / (2 * gamma ^ 2) := by
    have : 0 ≤ 2 * gamma + 1 := by linarith
    positivity
  linarith

theorem mutate_no_kick (m E p v : ℝ) (hE : E ^ 2 = m ^ 2 + 0) (hEpos : 0 < E)
    (hp : p ^ 2 = E ^ 2 - (m ^ 2 - 0)) (hv : v = p / E) : v = 0 := by
  have h := kick_speed_sq m 0 E p v hE hEpos hp hv
  have : v ^ 2 = 0 := by rw [h]; simp
  exact pow_eq_zero_iff (by norm_num) |>.mp this

/-! ### pair-growth eigenvalue and Hubble sweep -/

theorem pair_charpoly (D G lam : ℂ) :
    (D - lam) * (-D - lam) - G * (-G) = lam ^ 2 - (D ^ 2 - G ^ 2) := by
  ring

theorem pair_growth_root (D G : ℝ) (hDG : |D| < G) :
    let s : ℝ := Real.sqrt (G ^ 2 - D ^ 2)
    let lam : ℂ := (s : ℂ) * Complex.I
    ((D : ℂ) - lam) * (-(D : ℂ) - lam) - (G : ℂ) * (-(G : ℂ)) = 0 ∧ 0 < s := by
  intro s lam
  have hpos : 0 < G ^ 2 - D ^ 2 := by
    have := sq_lt_sq' (by linarith [abs_nonneg D, neg_abs_le D]) (lt_of_le_of_lt (le_abs_self D) hDG)
    nlinarith [sq_abs D, abs_nonneg D]
  have hs : 0 < s := Real.sqrt_pos.mpr hpos
  refine ⟨?_, hs⟩
  have hs2 : (s : ℂ) ^ 2 = ((G ^ 2 - D ^ 2 : ℝ) : ℂ) := by
    rw [← Complex.ofReal_pow]
    congr 1
    exact Real.sq_sqrt hpos.le
  have : ((D : ℂ) - lam) * (-(D : ℂ) - lam) - (G : ℂ) * (-(G : ℂ)) = lam ^ 2 - ((D : ℂ) ^ 2 - (G : ℂ) ^ 2) := by
    ring
  rw [this]
  have hl2 : lam ^ 2 = -(s : ℂ) ^ 2 := by
    show ((s : ℂ) * Complex.I) ^ 2 = -(s : ℂ) ^ 2
    rw [mul_pow, Complex.I_sq]; ring
  rw [hl2, hs2]
  push_cast
  ring

theorem half_disc (G : ℝ) (hG : 0 < G) :
    ∫ D in (-G)..G, Real.sqrt (G ^ 2 - D ^ 2) = Real.pi * G ^ 2 / 2 := by
  have h := intervalIntegral.integral_comp_mul_left
    (fun D : ℝ => Real.sqrt (G ^ 2 - D ^ 2)) (a := (-1 : ℝ)) (b := 1) hG.ne'
  have hfun : (fun x : ℝ => Real.sqrt (G ^ 2 - (G * x) ^ 2)) = fun x => G * Real.sqrt (1 - x ^ 2) := by
    funext x
    have : G ^ 2 - (G * x) ^ 2 = G ^ 2 * (1 - x ^ 2) := by ring
    rw [this, Real.sqrt_mul (by positivity), Real.sqrt_sq hG.le]
  simp only [hfun] at h
  rw [intervalIntegral.integral_const_mul, integral_sqrt_one_sub_sq] at h
  have h1 : G * -1 = -G := by ring
  simp only [h1, mul_one, smul_eq_mul] at h
  have : ∫ D in (-G)..G, Real.sqrt (G ^ 2 - D ^ 2) = G * (G * (Real.pi / 2)) := by
    have := h
    field_simp at this
    linarith
  rw [this]; ring

theorem sweep_integral (G H Delta : ℝ) (hG : 0 < G) (hH : 0 < H) (hD : 0 < Delta) :
    (∫ D in (-G)..G, Real.sqrt (G ^ 2 - D ^ 2)) / (2 * H * Delta)
      = Real.pi * G ^ 2 / (4 * H * Delta) := by
  rw [half_disc G hG]
  field_simp
  ring

/-! ### trigger scaling -/

theorem trigger_solution (m lam0 K0 q H Delta E n : ℝ)
    (hm : 0 < m) (hl : 0 < lam0) (hK : 0 < K0) (hH : 0 < H) (hD : 0 < Delta) (hE : 0 < E)
    (hn : 0 < n)
    (heq : Real.pi * (lam0 * (3 * H / K0) ^ (-(2 * q)) * n / (2 * m ^ 2)) ^ 2 / (4 * H * Delta) = E) :
    n = 2 * m ^ 2 / lam0 * (3 * H / K0) ^ (2 * q) * Real.sqrt (4 * H * Delta * E / Real.pi) := by
  have hpi : 0 < Real.pi := Real.pi_pos
  have h3 : 0 < 3 * H / K0 := by positivity
  have hP : 0 < (3 * H / K0) ^ (2 * q) := Real.rpow_pos_of_pos h3 _
  rw [Real.rpow_neg h3.le] at heq
  set P : ℝ := (3 * H / K0) ^ (2 * q) with hPdef
  set X : ℝ := lam0 * P⁻¹ * n / (2 * m ^ 2) with hX
  have hXpos : 0 < X := by rw [hX]; positivity
  have hX2 : X ^ 2 = 4 * H * Delta * E / Real.pi := by
    have h4 : (4 * H * Delta) ≠ 0 := by positivity
    have := heq
    field_simp at this ⊢
    linarith
  have hXs : X = Real.sqrt (4 * H * Delta * E / Real.pi) := by
    rw [← hX2, Real.sqrt_sq hXpos.le]
  have hn' : n = X * (2 * m ^ 2) * P / lam0 := by
    rw [hX]; field_simp
  rw [hn', hXs]
  field_simp

theorem trigger_scaling (m lam0 K0 q H1 H2 Delta E n1 n2 : ℝ)
    (hm : 0 < m) (hl : 0 < lam0) (hK : 0 < K0) (hH1 : 0 < H1) (hH2 : 0 < H2)
    (hD : 0 < Delta) (hE : 0 < E) (hn1 : 0 < n1) (hn2 : 0 < n2)
    (h1 : Real.pi * (lam0 * (3 * H1 / K0) ^ (-(2 * q)) * n1 / (2 * m ^ 2)) ^ 2 / (4 * H1 * Delta) = E)
    (h2 : Real.pi * (lam0 * (3 * H2 / K0) ^ (-(2 * q)) * n2 / (2 * m ^ 2)) ^ 2 / (4 * H2 * Delta) = E) :
    n2 / n1 = (H2 / H1) ^ (2 * q + 1 / 2) := by
  have hpi : 0 < Real.pi := Real.pi_pos
  have s1 := trigger_solution m lam0 K0 q H1 Delta E n1 hm hl hK hH1 hD hE hn1 h1
  have s2 := trigger_solution m lam0 K0 q H2 Delta E n2 hm hl hK hH2 hD hE hn2 h2
  have g1 : 0 < 3 * H1 / K0 := by positivity
  have g2 : 0 < 3 * H2 / K0 := by positivity
  have P1 : 0 < (3 * H1 / K0) ^ (2 * q) := Real.rpow_pos_of_pos g1 _
  have P2 : 0 < (3 * H2 / K0) ^ (2 * q) := Real.rpow_pos_of_pos g2 _
  have a1 : 0 < 4 * H1 * Delta * E / Real.pi := by positivity
  have a2 : 0 < 4 * H2 * Delta * E / Real.pi := by positivity
  have r1 : 0 < Real.sqrt (4 * H1 * Delta * E / Real.pi) := Real.sqrt_pos.mpr a1
  have r2 : 0 < Real.sqrt (4 * H2 * Delta * E / Real.pi) := Real.sqrt_pos.mpr a2
  have hratioP : (3 * H2 / K0) ^ (2 * q) / (3 * H1 / K0) ^ (2 * q) = (H2 / H1) ^ (2 * q) := by
    rw [← Real.div_rpow g2.le g1.le]
    congr 1
    field_simp
  have hratioS : Real.sqrt (4 * H2 * Delta * E / Real.pi) / Real.sqrt (4 * H1 * Delta * E / Real.pi)
      = (H2 / H1) ^ (1 / 2 : ℝ) := by
    rw [← Real.sqrt_div a2.le, Real.sqrt_eq_rpow]
    congr 1
    field_simp
  have hC : 2 * m ^ 2 / lam0 ≠ 0 := by positivity
  have : n2 / n1 = ((3 * H2 / K0) ^ (2 * q) / (3 * H1 / K0) ^ (2 * q))
      * (Real.sqrt (4 * H2 * Delta * E / Real.pi) / Real.sqrt (4 * H1 * Delta * E / Real.pi)) := by
    rw [s1, s2]
    field_simp
  rw [this, hratioP, hratioS, ← Real.rpow_add (by positivity)]

theorem trigger_exponent_four (m lam0 K0 H1 H2 Delta E n1 n2 : ℝ)
    (hm : 0 < m) (hl : 0 < lam0) (hK : 0 < K0) (hH1 : 0 < H1) (hH2 : 0 < H2)
    (hD : 0 < Delta) (hE : 0 < E) (hn1 : 0 < n1) (hn2 : 0 < n2)
    (h1 : Real.pi * (lam0 * (3 * H1 / K0) ^ (-(2 * (7 / 4 : ℝ))) * n1 / (2 * m ^ 2)) ^ 2 / (4 * H1 * Delta) = E)
    (h2 : Real.pi * (lam0 * (3 * H2 / K0) ^ (-(2 * (7 / 4 : ℝ))) * n2 / (2 * m ^ 2)) ^ 2 / (4 * H2 * Delta) = E) :
    n2 / n1 = (H2 / H1) ^ 4 := by
  have h := trigger_scaling m lam0 K0 (7 / 4) H1 H2 Delta E n1 n2 hm hl hK hH1 hH2 hD hE hn1 hn2 h1 h2
  have e : (2 * (7 / 4 : ℝ) + 1 / 2) = ((4 : ℕ) : ℝ) := by norm_num
  rw [e, Real.rpow_natCast] at h
  exact h

/-! ### channel closure -/

theorem channel_closure (m eps lam Phi0 rho G : ℝ) (hm : 0 < m) (_hl : 0 < lam) (hd : 0 < m ^ 2 + eps)
    (hrho : rho = (m ^ 2 + eps) * Phi0 ^ 2 / 2) (hG : G = lam * rho / (2 * m ^ 3)) :
    (0 ≤ (m ^ 2 + eps) - (m ^ 2 - eps + lam * Phi0 ^ 2))
      ↔ G ≤ eps * (m ^ 2 + eps) / (2 * m ^ 3) := by
  have hm3 : 0 < 2 * m ^ 3 := by positivity
  rw [hG, hrho, div_le_div_iff_of_pos_right hm3]
  constructor
  · intro h
    nlinarith [mul_le_mul_of_nonneg_left (show lam * Phi0 ^ 2 ≤ 2 * eps by linarith) hd.le]
  · intro h
    have : lam * Phi0 ^ 2 ≤ 2 * eps := by
      by_contra hcon
      push Not at hcon
      nlinarith [mul_lt_mul_of_pos_left hcon hd]
    linarith

theorem G_block_over_m (m eps v2 : ℝ) (hm : 0 < m) (hv2 : v2 < 2) (hv0 : 0 ≤ v2)
    (h : eps / m ^ 2 = v2 / (2 - v2)) :
    (eps * (m ^ 2 + eps) / (2 * m ^ 3)) / m = v2 / (2 - v2) ^ 2 ∧
    v2 / 4 ≤ v2 / (2 - v2) ^ 2 := by
  have h2 : 0 < 2 - v2 := by linarith
  have hm2 : m ^ 2 ≠ 0 := by positivity
  have he : eps = m ^ 2 * (v2 / (2 - v2)) := by field_simp at h ⊢; linarith
  constructor
  · rw [he]; field_simp; ring
  · rw [div_le_div_iff₀ (by norm_num) (by positivity)]
    nlinarith [mul_nonneg hv0 (show 0 ≤ v2 * (4 - v2) by nlinarith)]

end M3D

#print axioms M3D.kick_speed_sq
#print axioms M3D.kick_speed_lt_one
#print axioms M3D.eps_over_m2_of_v
#print axioms M3D.v_of_eps_over_m2
#print axioms M3D.latent_heat_lower
#print axioms M3D.latent_heat_nonneg
#print axioms M3D.mutate_no_kick
#print axioms M3D.pair_charpoly
#print axioms M3D.pair_growth_root
#print axioms M3D.half_disc
#print axioms M3D.sweep_integral
#print axioms M3D.trigger_solution
#print axioms M3D.trigger_scaling
#print axioms M3D.trigger_exponent_four
#print axioms M3D.channel_closure
#print axioms M3D.G_block_over_m
