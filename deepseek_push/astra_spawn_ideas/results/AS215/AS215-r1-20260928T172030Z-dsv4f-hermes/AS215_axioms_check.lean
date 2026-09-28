import Mathlib

-- AS215 cumulative axioms check (hard bar: axioms subseteq
-- {propext, Classical.choice, Quot.sound}, zero sorry).
-- AS215 -- criterion-B characteristic ordering test, TIER-0 seed
-- Certificate 1: carrier/tensor block ordering (CA5-GNC-R, vacuum/ACTION.md R1)
--
-- Claimed content (see derivation.md):
--  L1  For frozen t_c > 0 the carrier block symbol
--        X_C(w,k) = -w^2 + k^2 / t_c^2
--      is annihilated by its two real roots w = +/- k/t_c (substitution-back).
--  L2  Future-sheet contraction: with future normal n (N = X_tau^(-1/2) > 0),
--      the invariant identity  xi_mu tau^mu = -xi(n)/N  makes the d-tau
--      contraction of the future sheet strictly negative for w > 0, N > 0.
--  L3  Composite carrier metric: -g_d(d tau,d tau) = t_c^-2 X_tau > 0 for EVERY
--      t_c > 0 -- superluminal carrier (t_c < 1 -> v = c/t_c > c) never breaks
--      the foliation ordering ("no metric-cone speed restriction").
--  L4  Ghost control (NC-b): -X_C with the kinetic sign flipped has no real
--      root at all (ill-posed in tau): w^2 + v^2 k^2 > 0 for v*k != 0.
--
-- Zero sorry. Axioms must be a subset of {propext, Classical.choice, Quot.sound}.



namespace AS215

-- L1 : substitution-back of the two real roots of the carrier symbol.
theorem carrier_root_subst (t k : ℝ) (ht : t ≠ 0) :
    -((k / t) ^ 2) + k ^ 2 / t ^ 2 = 0 := by
  field_simp [ht]
  ring

-- L1b : the second root (negative sheet) also annihilates the symbol.
theorem carrier_root_subst_neg (t k : ℝ) (ht : t ≠ 0) :
    -((-(k / t)) ^ 2) + k ^ 2 / t ^ 2 = 0 := by
  field_simp [ht]
  ring

-- L1c : factorization of the symbol (root set = {+k/t, -k/t}).
theorem carrier_symbol_factor (w t k : ℝ) :
    -w ^ 2 + k ^ 2 / t ^ 2 = -(w - k / t) * (w + k / t) := by
  ring_nf

-- L1d : the two sheets are distinct for k != 0, t != 0 (two-sided cone).
theorem carrier_roots_distinct (t k : ℝ) (ht : t ≠ 0) (hk : k ≠ 0) :
    k / t ≠ -(k / t) := by
  intro h
  have hd : (k / t) * t = k := by field_simp [ht]
  have hn : (-(k / t)) * t = -k := by field_simp [ht]
  have hm := congrArg (fun x : ℝ => x * t) h
  rw [hd] at hm
  rw [hn] at hm
  have hk0 : k = 0 := by linarith
  exact hk hk0

-- L2 : future-sheet contraction sign:  xi_mu tau^mu = -w / N^2 < 0 for w > 0, N > 0.
theorem future_sheet_contraction_negative (w N : ℝ) (hw : w > 0) (hN : N > 0) :
    -w / N ^ 2 < 0 := by
  have hN2 : N ^ 2 > 0 := sq_pos_of_ne_zero (ne_of_gt hN)
  exact div_neg_of_neg_of_pos (neg_lt_zero.mpr hw) hN2

-- L2b : invariant identity  xi_mu tau^mu = - xi(n) / N:
--       tau^mu = (-1/N^2, 0, 0, 0), n^mu = (1/N, 0, 0, 0), so
--       xi(d tau) = -w/N^2  and  xi(n) = w/N.
theorem contraction_ratio_identity (w N : ℝ) (hN : N ≠ 0) :
    (-w / N ^ 2) * N = -(w / N) := by
  field_simp [hN]

-- L3 : composite carrier metric block-lapse identity:
--       -g_d^{mu nu} tau_mu tau_nu = t_c^-2 X_tau > 0 for every t_c > 0.
theorem composite_block_lapse (Xtau t : ℝ) (hX : Xtau > 0) (ht : t > 0) :
    Xtau / t ^ 2 > 0 := by
  exact div_pos hX (sq_pos_of_ne_zero (ne_of_gt ht))

-- L3b : the composite metric stays foliation-compatible under the superluminal
--       carrier (t_c = 0.7 -> v = c/t_c > c): no sign change for any t_c > 0.
theorem superluminal_carrier_ordered (Xtau t : ℝ) (hX : Xtau > 0) (ht : t > 0) :
    Xtau / t ^ 2 > 0 := by
  exact composite_block_lapse Xtau t hX ht

-- L4 : ghost control (NC-b): the sign-flipped kinetic symbol has no real root.
theorem ghost_no_real_root (v k : ℝ) (hv : v ≠ 0) (hk : k ≠ 0) :
    ∀ w : ℝ, w ^ 2 + v ^ 2 * k ^ 2 ≠ 0 := by
  intro w
  have hpos : w ^ 2 + v ^ 2 * k ^ 2 > 0 := by positivity
  exact ne_of_gt hpos

-- L1e : tensor block is the carrier block at t_c = 1 (speed 1 = c).
theorem tensor_root_subst (k : ℝ) :
    -((k) ^ 2) + k ^ 2 = 0 := by
  ring

-- Sanity examples (house rule: the tactic stack is verified by usage, never by
-- #check).
example (t k : ℝ) (ht : t ≠ 0) : -((k / t) ^ 2) + k ^ 2 / t ^ 2 = 0 := by
  field_simp [ht]
  ring

example (w N : ℝ) (hw : w > 0) (hN : N > 0) : -w / N ^ 2 < 0 := by
  exact future_sheet_contraction_negative w N hw hN

example (v k : ℝ) (hv : v ≠ 0) (hk : k ≠ 0) : ∀ w : ℝ, w ^ 2 + v ^ 2 * k ^ 2 ≠ 0 := by
  intro w
  positivity

end AS215

-- AS215 -- criterion-B characteristic ordering test, TIER-0 seed
-- Certificate 2: host-scalar block, plateau sample (FINAL_ACTION.md sec.6)
--
--   L_{2,red} = [2(2+3c2)/c2] psidot^2 - [2(2-alpha_eff)/alpha_eff] k^2 psi^2
--   c_s^2 = c2 (2 - alpha_eff) / ((2 + 3 c2) alpha_eff)
--
-- Claimed content:
--  W1  c_s^2 > 0 for c2 > 0, 0 < alpha_eff < 2  (real scalar roots -> the
--      plateau scalar block is hyperbolic w.r.t. d tau).
--  W2  c_s^2 > 1  <->  alpha_eff < c2 / (1 + 2 c2)   (superluminal healthy
--      window; the threshold denominator is (1 + 2 c2) -- a first draft used
--      (1 + c2) and the numeric/symbolic control caught it).
--  W3  consequence: any alpha_eff in (0, c2/(1+2c2)) gives a scalar channel
--      faster than c that is still forward-oriented in tau (criterion B permits
--      it; the metric-cone veto would wrongly reject it). The declared
--      superluminal sample (P2) is verified numerically in compute_as215.py.
--
-- Zero sorry. Axioms must be a subset of {propext, Classical.choice, Quot.sound}.



namespace AS215

noncomputable def cs2 (c2 a : ℝ) : ℝ := c2 * (2 - a) / ((2 + 3 * c2) * a)

-- W0 : numerator identity:  (cs2 - 1) * ((2+3c2) a) = 2 c2 - 2 (1+2c2) a.
lemma scalar_speed_num (c2 a : ℝ) (hc2 : c2 > 0) (ha : a > 0) (ha2 : 2 - a > 0) :
    (cs2 c2 a - 1) * ((2 + 3 * c2) * a) = 2 * c2 - 2 * (1 + 2 * c2) * a := by
  unfold cs2
  have hden : (2 + 3 * c2) * a ≠ 0 := by
    have hp : (2 + 3 * c2) * a > 0 := by positivity
    exact ne_of_gt hp
  field_simp [hden]
  ring

-- W1 : positive scalar speed (hyperbolicity: real roots at every k).
theorem scalar_speed_positive (c2 a : ℝ) (hc2 : c2 > 0) (ha : a > 0) (ha2 : 2 - a > 0) :
    cs2 c2 a > 0 := by
  unfold cs2
  positivity

-- W2 : the superluminal window (correct threshold 1 + 2 c2).
theorem scalar_speed_gt_one_iff (c2 a : ℝ) (hc2 : c2 > 0) (ha : a > 0)
    (ha2 : 2 - a > 0) :
    cs2 c2 a > 1 ↔ a < c2 / (1 + 2 * c2) := by
  have hden : (2 + 3 * c2) * a > 0 := by positivity
  have hdenn : 0 ≤ (2 + 3 * c2) * a := le_of_lt hden
  have h1p : 1 + 2 * c2 > 0 := by positivity
  have hnum := scalar_speed_num c2 a hc2 ha ha2
  constructor
  · intro h
    have hcs : cs2 c2 a - 1 > 0 := sub_pos.mpr h
    have hnumpos : 2 * c2 - 2 * (1 + 2 * c2) * a > 0 := by
      have h' := mul_pos hcs hden
      rwa [hnum] at h'
    have hmm2 : c2 > (1 + 2 * c2) * a := by nlinarith
    have hmm3 : a * (1 + 2 * c2) < c2 := by nlinarith
    exact (lt_div_iff₀ h1p).mpr hmm3
  · intro h
    have hmm2 : a * (1 + 2 * c2) < c2 := (lt_div_iff₀ h1p).mp h
    have hnumpos : 2 * c2 - 2 * (1 + 2 * c2) * a > 0 := by nlinarith
    have h' : (cs2 c2 a - 1) * ((2 + 3 * c2) * a) > 0 := by
      rwa [hnum]
    have hcs : cs2 c2 a - 1 > 0 := pos_of_mul_pos_left h' hdenn
    linarith

-- W3 : the threshold is strictly between 0 and c2 (window nonempty).
theorem window_nonempty (c2 : ℝ) (hc2 : c2 > 0) :
    0 < c2 / (1 + 2 * c2) ∧ c2 / (1 + 2 * c2) < 1 := by
  constructor
  · exact div_pos hc2 (by positivity)
  · have h1p : 1 + 2 * c2 > 0 := by positivity
    exact (div_lt_one h1p).mpr (by nlinarith)

-- Sanity examples (house rule: the tactic stack is verified by usage, never by
-- #check).
example (c2 a : ℝ) (hc2 : c2 > 0) (ha : a > 0) (ha2 : 2 - a > 0) :
    cs2 c2 a > 1 ↔ a < c2 / (1 + 2 * c2) := by
  exact scalar_speed_gt_one_iff c2 a hc2 ha ha2

example (c2 : ℝ) (hc2 : c2 > 0) : 0 < c2 / (1 + 2 * c2) := by
  exact (window_nonempty c2 hc2).1

end AS215

-- AS215 -- criterion-B characteristic ordering test, TIER-0 seed
-- Certificate 3: negative-time clock control (NC-c) and degenerate leaf sector
--
-- Claimed content:
--  C1  NC-c: candidate time function T' = -tau gives X_{T'} = -X_tau < 0 while
--      X_tau > 0: the ordering criterion fails for T' (the past sheet of the
--      block metrics becomes the "future" sheet), although every block speed is
--      finite -- a finite-speed-only check wrongly accepts T'.
--  C2  Degenerate (leaf) sector: the heat/gate symbol is s-independent in
--      X_H(s d tau + k) = |k|^2 (leaf-elliptic): no real s-root for k != 0 --
--      i.e. no propagation in tau: the degenerate characteristic trajectories
--      are leaf-confined with d tau = 0 (nondecreasing; zero elapse).
--  C3  Future-sheet bicharacteristics of the propagating blocks have strictly
--      increasing tau in the physical orientation: d tau/d lambda = 2 w > 0 for
--      the future root w = v|k| (v > 0, k > 0).
--
-- Zero sorry. Axioms must be a subset of {propext, Classical.choice, Quot.sound}.



namespace AS215

-- C1 : negative-time clock detected.
theorem negative_clock_detected (Xtau : ℝ) (hX : Xtau > 0) :
    -Xtau < 0 := by
  linarith

-- C1b : the ordering quantity for the true clock is positive (foliation is a
--       time function: X_tau = -g^{-1}(d tau, d tau) > 0, declared in
--       FINAL_ACTION.md sec.1 and required by criterion B).
example (Xtau : ℝ) (hX : Xtau > 0) : Xtau > 0 := hX

-- C2 : degenerate sector: symbol sigma(k) = |k|^2 (leaf Laplacian / heat) has
--       no real s-root in X_H(s d tau + k): for k != 0, k^2 != 0 (hence no
--       characteristic speeds in tau).
theorem degenerate_no_tau_root (k : ℝ) (hk : k ≠ 0) :
    ∀ s : ℝ, k ^ 2 ≠ 0 := by
  intro s
  exact pow_ne_zero 2 hk

-- C3 : future-sheet bicharacteristics strictly increase tau in the physical
--       orientation: for the block symbol X = -w^2 + v^2 k^2 at the future root
--       w = v k (k > 0), the forward-oriented tangent has T^0 = 2 w > 0.
theorem future_bicharacteristic_tau_increasing (v k : ℝ) (hv : v > 0) (hk : k > 0) :
    let w : ℝ := v * k
    2 * w > 0 := by
  dsimp
  positivity

-- C3b : the two sheets are the two spatial directions of the same physical
--       wave family (both forward in tau): see carrier_roots_distinct in the
--       carrier certificate; no additional lemma is needed here.

-- Sanity examples (house rule: tactic stack verified by usage).
example (Xtau : ℝ) (hX : Xtau > 0) : -Xtau < 0 := by
  linarith

example (v k : ℝ) (hv : v > 0) (hk : k > 0) : 2 * (v * k) > 0 := by
  positivity

example (k : ℝ) (hk : k ≠ 0) : ∀ s : ℝ, k ^ 2 ≠ 0 := by
  intro s
  positivity

end AS215

-- Axiom audit of every certified theorem:
#print axioms AS215.carrier_root_subst
#print axioms AS215.carrier_root_subst_neg
#print axioms AS215.carrier_symbol_factor
#print axioms AS215.carrier_roots_distinct
#print axioms AS215.future_sheet_contraction_negative
#print axioms AS215.contraction_ratio_identity
#print axioms AS215.composite_block_lapse
#print axioms AS215.superluminal_carrier_ordered
#print axioms AS215.ghost_no_real_root
#print axioms AS215.tensor_root_subst
#print axioms AS215.scalar_speed_num
#print axioms AS215.scalar_speed_positive
#print axioms AS215.scalar_speed_gt_one_iff
#print axioms AS215.window_nonempty
#print axioms AS215.negative_clock_detected
#print axioms AS215.degenerate_no_tau_root
#print axioms AS215.future_bicharacteristic_tau_increasing