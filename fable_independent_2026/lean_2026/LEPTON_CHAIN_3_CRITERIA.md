# LEPTON_CHAIN_3: the symmetry behind TM1 (frozen before any Lean, 2026-10-09)

Owner: "keep going, swing harder on the lean certificate." LEPTON_CHAIN/2 take TM1 as an assumption. This file certifies which
residual symmetry TM1 is equivalent to, and why the larger symmetry is dead. The setting is S4 in the basis where its Z3
generator T is diagonal, so the charged leptons are diagonal (standard; ASSUMED). The 3-dim generators, with factors of 3 cleared:
  3S = [[-1,2,2],[2,-1,2],[2,2,-1]],  U = swap(mu, tau),  G := 3·(SU) = [[-1,2,2],[2,2,-1],[2,-1,2]].

**Theorems (zero sorry, standard axioms):**
- S1 `G_sq`: G·G = 9·1, so SU is an involution (a Z2).
- S2 `G_v1`: G v1 = −3 v1 for v1 = (2, −1, −1), so v1 is SU's eigenvalue −1 eigenvector. `G_trace`: tr G = 3, so tr SU = 1 and the
  eigenvalues are (1, 1, −1): the −1 eigenspace is the line through v1.
- S3 `z2_forces_tm1_column`: any complex 3×3 H with H·G = G·H (e.g. H = M†M for a neutrino mass matrix with residual Z2 = SU)
  satisfies H v1 = c v1 for some c. So v1 is a mass eigenvector.
- S4 `tm1_column_moduli`: the normalised column v1/√6 has moduli² (2/3, 1/6, 1/6), i.e. TM1's |U_e1|², |U_mu1|², |U_tau1|².
  This is exactly the hypothesis set of LEPTON_CHAIN's L4/L9/L10, so the chain is: residual Z2(SU) ⇒ TM1 ⇒ octant decides δ ⇒
  CP violation is near-maximal.
- S5 `full_klein_forces_theta13_zero`: if H also commutes with U (the full Klein group {1, S, U, SU}), then H w = c' w for
  w = (0, 1, −1). That eigenvector has zero electron component, so |U_e3|² = 0 < 0.020 ≤ the measured s13². The full residual
  symmetry (tri-bimaximal mixing) is excluded by θ13; breaking it to Z2(SU) is what survives.
- S6 `other_z2_tm2`: the other surviving-candidate Z2, U alone (μτ swap), has (0, 1, −1) as its −1 eigenvector. It gives
  |U_e3| = 0 and is also excluded. And S alone fixes (1, 1, 1), which gives TM2 (|U_e2|² = 1/3), already shown 3–4σ off.

**MUTATE (all must FAIL):**
- M7: G v1 = +3 v1.
- M8: commuting with G forces H w ∝ w for w = (0, 1, −1). This is false: G alone does not fix w.
- M9: the moduli of v1/√6 are (1/3, 1/3, 1/3).

**Not certified:**
- the choice of S4, and of the T-diagonal basis;
- that the residual symmetry is realised dynamically (no flavon potential is given);
- that H's spectrum is non-degenerate (needed for v1 to BE a PMNS column);
- which mass v1 belongs to (that it is the first column is the TM1 assignment);
- that it is exact, not approximate.
Residual Z2 is a hypothesis with no derivation from the framework.
**Statement match:** an independent reviewer checks the docstrings before the commit.
