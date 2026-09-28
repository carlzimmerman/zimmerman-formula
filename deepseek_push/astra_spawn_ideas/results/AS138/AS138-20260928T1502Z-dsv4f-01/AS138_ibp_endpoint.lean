import Mathlib

/-!
AS138 Tier-0 certificate: the discrete r-sector integration-by-parts identity.

Model (AS138, heat sector of the CA4-GNC common action, flat 1D leaf, N+1 nodes):
  the r-sector coupling  Σ_k L_k * (W_{k+1} - W_k)  is re-expressed in
  canonical (r-IBP'd) form.  Partially summing over k gives the exact
  algebraic identity

    Σ_{k=0..N} L_k (v_{k+1} - v_k)
      = L_N v_{N+1} - L_0 v_0  -  Σ_{j=0..N-1} (L_{j+1} - L_j) v_{j+1}

  i.e. the bulk variation equals the *r-endpoint-multiplier bracket*
  L_N v_{N+1} - L_0 v_0  (continuum: L_b ξ∂W_b - L_0 ξ∂W_0) minus the
  interior canonical Euler-derivative terms (L_{j+1}-L_j) v_{j+1}.

This is exactly the identity the seed's negative control relies on:
OMIT the endpoint multipliers  ⇒ the residual of the formal Ward identity
is the nonzero bracket  L_b·LieW_b - L_0·LieW_0.
-/

open Finset
open scoped BigOperators

/-- Discrete r-IBP with explicit endpoint bracket; N+1 differences (N≥0). -/
theorem sum_mul_sub_endpoint (N : ℕ) (L v : ℕ → ℚ) :
    (∑ k ∈ Finset.range (N + 1), L k * (v (k + 1) - v k))
      = L N * v (N + 1) - L 0 * v 0
        - ∑ j ∈ Finset.range N, (L (j + 1) - L j) * v (j + 1) := by
  induction N with
  | zero =>
      -- N = 0: single difference L0(v1-v0) = L0 v1 - L0 v0 - 0
      simp
      ring
  | succ N ih =>
      -- split the last term off the LHS sum
      rw [Finset.sum_range_succ]
      -- split the last term off the RHS sum (explicit target, distinct variable)
      rw [show (∑ j ∈ Finset.range (N + 1), (L (j + 1) - L j) * v (j + 1))
                 = (∑ j ∈ Finset.range N, (L (j + 1) - L j) * v (j + 1))
                     + (L (N + 1) - L N) * v (N + 1) by
            rw [Finset.sum_range_succ]]
      rw [ih]
      ring

/-- Ward-leftover corollary: the bulk variation plus the interior canonical
    Euler terms equals exactly the r-endpoint-multiplier bracket. -/
theorem ward_leftover_endpoint_bracket (N : ℕ) (L v : ℕ → ℚ) :
    (∑ k ∈ Finset.range (N + 1), L k * (v (k + 1) - v k))
      + (∑ j ∈ Finset.range N, (L (j + 1) - L j) * v (j + 1))
      = L N * v (N + 1) - L 0 * v 0 := by
  rw [sum_mul_sub_endpoint]
  ring

/-- AS138 r-sector instance: N=2 differences (3 interior nodes, W_b = v_3);
    the leftover when endpoint multipliers are omitted is exactly
    L_2 v_3 - L_0 v_0. -/
example (L v : ℕ → ℚ) :
    (∑ k ∈ Finset.range 3, L k * (v (k + 1) - v k))
      - (- (∑ j ∈ Finset.range 2, (L (j + 1) - L j) * v (j + 1)))
      = L 2 * v 3 - L 0 * v 0 := by
  rw [sum_mul_sub_endpoint]
  ring

/-! Axiom audit (hard bar: no sorry; axioms ⊆ {propext, Classical.choice, Quot.sound}). -/
#print axioms sum_mul_sub_endpoint
#print axioms ward_leftover_endpoint_bracket
