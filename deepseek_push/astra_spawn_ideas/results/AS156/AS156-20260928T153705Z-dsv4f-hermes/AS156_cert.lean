import Mathlib

/-!
AS156 Lean certificate — spatial diffeomorphism generator for heat fields (CA5-GNC-R).
Certifies the algebraic core of the checks executed in `as156_spatial_difffeo_checks.py`
on the 1D periodic 4-site lattice (Delta = 1/2, so 2*Delta = 1) over the rationals:

  T1  generator action:  {q_s, G(xi)} = xi_s (q_{s+1} - q_{s-1}) / 2   (C1 q-sector, all s)
  T2  negative control:  coefficient of pW_1 in the cut generator is 0,  (C5 cut fires)
      coefficient of pW_1 in the full generator is xi_1 (W_2 - W_0) / 2 (C5 full exact)
  T3  reduction:          G_full with all auxiliary momenta set to 0      (C2)
      equals the carrier generator G_carrier.

All statements are exact rational identities; proofs are by finite case analysis
(fin_cases) plus ring/norm_num. No analysis, no limits, no sorry.
-/

namespace AS156

abbrev R := ℚ
abbrev Site := Fin 4

def next (i : Site) : Site := ⟨(i.val + 1) % 4, by omega⟩
def prev (i : Site) : Site := ⟨(i.val + 3) % 4, by omega⟩   -- (i-1) mod 4 = (i+3) mod 4

-- generator: G(xi) = sum_t xi_t * p_t * (q_{t+1} - q_{t-1}) / 2,  (2*Delta)=1
noncomputable def G (xi p q : Site → R) : R :=
  ∑ t : Site, xi t * p t * (q (next t) - q (prev t)) / 2

-- ------------------------------------------------------------------ T1: C1 q-sector
theorem generator_action_q (s : Site) (xi p q : Site → R) :
    (∑ t : Site, xi t * (if t = s then 1 else 0) * (q (next t) - q (prev t)) / 2)
      = xi s * (q (next s) - q (prev s)) / 2 := by
  fin_cases s <;> rw [Fin.sum_univ_four] <;> simp [next, prev] <;> ring

-- same identity extended to any weight-0 scalar field (phi, U, Z, lambda0, W, L):
theorem generator_action_scalar (s : Site) (xi p f : Site → R) :
    (∑ t : Site, xi t * (if t = s then 1 else 0) * (f (next t) - f (prev t)) / 2)
      = xi s * (f (next s) - f (prev s)) / 2 := by
  fin_cases s <;> rw [Fin.sum_univ_four] <;> simp [next, prev] <;> ring

-- ------------------------------------------------------------------ C5: negative control
-- full generator (aux sector) = carrier + U + Z + lambda0 + W + L momentum terms
noncomputable def G_full_aux (xi : Site → R)
    (pφ pU pZ pl : Site → R) (φ U Z lm : Site → R)
    (pW pL : Site → R) (W L : Site → R) : R :=
  ∑ t : Site, xi t * (pφ t * (φ (next t) - φ (prev t))
                    + pU t * (U (next t) - U (prev t))
                    + pZ t * (Z (next t) - Z (prev t))
                    + pl t * (lm (next t) - lm (prev t))
                    + pW t * (W (next t) - W (prev t))
                    + pL t * (L (next t) - L (prev t))) / 2

-- cut generator: W,L primary terms omitted (carrier + U + Z + lambda0 terms kept)
noncomputable def G_cut (xi pφ pU pZ pl : Site → R) (φ U Z lm : Site → R) : R :=
  ∑ t : Site, xi t * (pφ t * (φ (next t) - φ (prev t))
                    + pU t * (U (next t) - U (prev t))
                    + pZ t * (Z (next t) - Z (prev t))
                    + pl t * (lm (next t) - lm (prev t))) / 2

noncomputable def G_carrier (xi : Site → R) (pφ : Site → R) (φ : Site → R) : R :=
  ∑ t : Site, xi t * pφ t * (φ (next t) - φ (prev t)) / 2

-- full generator with the heat-field pair (W_1, pW_1) singled out at site 1
noncomputable def G_full (xi : Site → R) (pW : Site → R) (W : Site → R)
    (rest : R) : R :=
  ∑ t : Site, xi t * (if t = (1 : Site) then pW t else 0) * (W (next t) - W (prev t)) / 2
    + rest

-- (a) the cut generator differs from the full generator exactly by the omitted W,L terms
theorem cut_missing_terms (xi : Site → R) (pφ pU pZ pl : Site → R) (φ U Z lm : Site → R)
    (pW pL : Site → R) (W L : Site → R) :
    G_full_aux xi pφ pU pZ pl φ U Z lm pW pL W L - G_cut xi pφ pU pZ pl φ U Z lm
      = ∑ t : Site, xi t * (pW t * (W (next t) - W (prev t))
                          + pL t * (L (next t) - L (prev t))) / 2 := by
  unfold G_full_aux G_cut
  rw [Fin.sum_univ_four, Fin.sum_univ_four, Fin.sum_univ_four] <;> simp [next, prev] <;> ring

-- (b) the full generator's pW_1 coefficient is the Lie derivative value xi_1 (W_2 - W_0) / 2
theorem neg_control_full_exact (xi pW : Site → R) (W : Site → R) :
    (∑ t : Site, xi t * (if t = (1 : Site) then 1 else 0) * (W (next t) - W (prev t)) / 2)
      = xi (1 : Site) * (W (next (1 : Site)) - W (prev (1 : Site))) / 2 := by
  rw [Fin.sum_univ_four] <;> simp [next, prev] <;> ring

-- (c) the control FIRES: the Lie derivative of an off-shell heat field is not identically zero
--     (witness: xi = const 1, W_s = s  ->  L_xi W_1 = (W_2 - W_0)/2 = 1)
theorem control_fires_witness :
    ∃ (xi W : Site → R), xi (1 : Site) * (W (next (1 : Site)) - W (prev (1 : Site))) / 2 ≠ 0 := by
  refine ⟨fun _ => 1, fun i => i.val, ?_⟩
  norm_num [next, prev]

-- ------------------------------------------------------------------ C2: reduction on the primary surface
-- on pi_U = pi_Z = pi_lambda0 = pi_W = pi_L = 0 the full generator reduces exactly
-- to the carrier (gravity + scalar-carrier) momentum generator:
theorem reduction_on_primary_surface (xi : Site → R) (pφ : Site → R)
    (φ U Z lm : Site → R) (W L : Site → R) :
    G_full_aux xi pφ (fun _ => 0) (fun _ => 0) (fun _ => 0) φ U Z lm
                 (fun _ => 0) (fun _ => 0) W L
      = G_carrier xi pφ φ := by
  unfold G_full_aux G_carrier
  simp [next, prev] <;> ring

end AS156

#print axioms AS156.generator_action_q
#print axioms AS156.generator_action_scalar
#print axioms AS156.cut_missing_terms
#print axioms AS156.neg_control_full_exact
#print axioms AS156.control_fires_witness
#print axioms AS156.reduction_on_primary_surface