# AS138 — Total diffeomorphism identity with heat fields (Tier-0 seed execution)

**Run:** `AS138-20260928T1502Z-dsv4f-01` · **Seed hash (task_sha256):** `e3cc42155feab9dd6b7c632c3e4e9a4c9902b3a75529bb2f19552d28419b9356` (verified before execution, matches the pinned value)
**Branch:** CA5-GNC-R with inherited CA4-GNC host, as declared; no historical branch (Q / RAR / MU2 / EXP / MONO) is engaged — see §5.
**Worker:** deepseek/deepseek-v4-flash-0731 via Hermes subagent (identity string in result.json).
**Source pins:** `real_research/common_action_2026_09_26/action/FINAL_ACTION.md` (pinned b8c04d4e…7546e, verified on disk); FRAMEWORK_CONTRACT.md, SOURCE_MANIFEST.json, RESULT_CONTRACT.json, FIRST_PRINCIPLES_AND_BRANCHING.md all read before execution.

## 1. Pinned action and conventions (seed step 1)

The heat sector of the CA4-GNC common action, in the orthogonal form used by the heat-sector lineage (FINAL_ACTION.md, eqs. (4)–(5), (9)–(12)):

```
S_heat = ∫ d^3x dt N { G(Y_h) + ℓ a·D(W_b) + Σ_{k=0}^{N−1} L_k [ (W_{k+1} − W_k) − Dh(W_k) ]
          + λ0 (W_0 − U) } ,        a := D ln N ,   D ≡ ∂_x on the leaf
Y_h = J(D·W_b) + ℓ Dh(W_b) − θ ,    W_b := W_N ,    Dh(W_k) := W_k'' (flat leaf, K=0)
```

Flat 1D leaf coordinate `x` on the slab `[0,1]`, orthogonal foliation, base point `p = (0,0)`; jets truncated to order ≤2 in x, ≤1 in t (jet slots hold Taylor **derivative** values, so the x² term carries 1/2). `c=1` in the field equations; SI reinstated only for the dimensional footings (§6). Discrete r-family: `N_disc = 3` differences, nodes 0…3, so the r-endpoint bracket is `L_2·(ξ∂W)_3 − L_0·(ξ∂W)_0` (left-node convention; continuum form `L_b·ξ∂W_b − L_0·ξ∂W_0`). Compactly supported diffeomorphism `ξ` (variations `δF = ξ^1 ∂_x F + ξ^0 ∂_t F`, flat point, K=0, dh=0). Every field is a spacetime scalar per r (seed step 2). All fixed coefficients were named symbolically (N, ℓ, J, J_p, G′, λ0, θ) before computation; none fixed numerically in the algebra. kappa = 1/2 is adopted as an input (framework), not derived.

## 2. Total field variation and its chain-rule decomposition (seed step 2)

For the full heat sector we verified the **off-shell Ward chain rule** at the jet level (exact polynomial identity; 5 random-jets × zero-check):

```
δ_ξ S_heat|fields = N · [ Σ_k E_Wk(δW_k) + Σ_k E_Lk(δL_k) + E_λ0(δλ0) + E_U(δU) ]
```
with the local Euler operators (raw, no r-IBP yet)
`E_Wk(h) = (L_{k−1}−L_k)h − L_k·Dh(h)` (k=1,2), `E_W0(h) = −L_0[h + Dh(h)]`,
`E_W3(h) = L_2·h + [G-step]`, gate operator `E_g(h) = Gp·Jd·h' + Gp·ℓ·h'' + ℓ·a·h'`,
`E_Lk(h) = [(W_{k+1}−W_k) − Dh(W_k)]·h`, `E_λ0 = W_0−U`, `E_U = −λ0`.
Residual **0.000e+00** (CHK-1, exact). The gate's W_b dependence flows through *G(Y_h)* (linearized, CHK-4: `E_W3` gate piece ≡ formula (5) operator `Gp·Jd·h' + Gp·ℓ·h'' + ℓ·a·h'` at the base point, residual 0.000e+00).

## 3. Canonical decomposition, r-IBP and the endpoint-multiplier leftover (seed steps 3–4, negative control)

Applying the discrete r-IBP (partial summation) to the r-sector gives the exact identity, certified in Lean (see §8):

```
Σ_{k=0}^{N} L_k (v_{k+1} − v_k)  =  L_N v_{N+1} − L_0 v_0  −  Σ_{j=0}^{N−1} (L_{j+1} − L_j) v_{j+1}
```

Hence, with the canonical (r-IBP'd) interior Euler derivatives `E_Wj^canon(h) = (L_{j−1}−L_j)h − L_j Dh(h)` (j=1,2; endpoint nodes carry no h-term):

```
δ_ξ S_bulk|fields = N·[ Σ_j E_Wj^canon(δW_j) + Σ_k E_Lk(δL_k) ]  +  N·M ,     M := L_2·(ξ∂W)_3 − L_0·(ξ∂W)_0
```

- **CHK-2 (negative control — "omit the r-endpoint multipliers"):** dropping `M` leaves an exact, non-vanishing residual `N·M`. Verified two ways:
  (i) algebraic: `leftover − N·M` residual **0.000e+00** (exact);
  (ii) nonzero witness at a random jet: `|N·M| = 5.704e-02 ≠ 0` (CHK-2b), and the integrated leaf witness: `M_integral = 3.315357e-01 ≠ 0` (I2b) — the formal Ward identity **fails with an explicit residual** when the r-endpoint multipliers are omitted, as required by the seed ("capable of failing").
- **CHK-3 (multiplier restoration / off-shell Ward relation usable for constraint propagation):**

```
δ_ξ S_heat|fields = N·[ Σ_j E_Wj^canon(ξ∂W_j) + Σ_k E_Lk(ξ∂L_k)
        + (R_W + L_b)·ξ∂W_b + (λ0 − L_0)·ξ∂W_0 + E_λ0·ξ∂λ0 + E_U·ξ∂U ]
```
  residual **0.000e+00** (CHK-3), i.e. the bulk endpoint bracket `M` is canceled term-by-term by the explicit endpoint-multiplier display `(R_W + L_b)·ξ∂W_b + (λ0−L_0)·ξ∂W_0`. On-shell (`E_* = 0`, `λ0 = L_0`, `R_W = −L_b`) the heat-sector field variation vanishes and the *contracted metric identity* of step 3 reduces to the clock/lapse equation: `δ_{ln N} S_gate = ∫ N ε [G(Y_h) − ℓ·Dh(W_b)]` with the `+ℓ a DW_b` compensator converting to `−ℓ Dh W_b` under IBP (CHK-6/I6: the measure variation `δN·(ℓ a DW_b)` supplies exactly the piece needed; verified integrated: direct − claim = −5.07e-09 at 2¹⁴ grid, −3.17e-10 at 2¹⁶, convergence pass — see §4).
  The lapse/diffeomorphism statement "the clock equation follows when metric, matter and auxiliary equations are imposed" is thereby supported as an off-shell Ward relation; the full contracted metric identity (geometry part from the host action) is **not** derived here — upstream host-sector identity work (AS137 lineage) is required for the metric equations (see `next_unresolved_implication`).

## 4. Numeric instance witness (finite domain, refined once)

Domain: leaf `x ∈ [0,1]`, 2¹⁴ grid (refined to 2¹⁶ for the two derivative-noise-sensitive checks: I5 adjoint and I6 eq-(12) sign, both showing ~16× residual reduction 2.98e-8→1.86e-9 and 5.07e-9→3.17e-10 — genuine convergence, not noise). All 18 checks pass (exit 0). Non-vacuity: `M_integral = +3.315357e-01`, gate pairing −1.1526, R_W range 1.97e-2; wrong-sign variants *fail* as designed (I6b, I6c). 1 thread; no BLAS threading (`OPENBLAS_NUM_THREADS=1`).

## 5. Framework cell, footings, branches

- **a0** = (c/2)·√(G·ρ_Lambda) with kappa = 1/2 **adopted** (framework input, not derived). `r_M = √(G M_b / a0)`, `v_flat⁴ = G M_b a0` enter only via cited host definitions; not re-derived here.
- Both footings, kept separate everywhere (they cannot share both fixed vacuum density and fixed kappa):
  canonical `a0 = 9.3619e-11 m/s²` ⇒ `ρ_Lambda = 4 a0²/(G c²) = 5.8444124540e-27 kg/m³` (footprint matches AS001 lineage);
  alternative `a0 = 1.1279e-10 m/s²` ⇒ `ρ_total = 8.4830896196e-27 kg/m³`; ratio (1.1279e-10/9.3619e-11)² = **1.45148716** — matches the AS001-recorded ratio exactly.
- G_N (Newtonian, 6.67430e-11), G_bare and G_cosmo treated as **separate** constants (SI); only the Newtonian G enters the footing printout; bare/cosmo couplings are not invoked by this seed.
- Branches: **none engaged** — Q, RAR, MU2, EXP, MONO are distinct; this run uses only the task's declared CA5-GNC-R/CA4-GNC branch and makes no branch-translation claim (criterion B untouched).

## 6. Controls that were capable of failing

| control | how it can fail | result |
|---|---|---|
| CHK-1 chain rule | slot/operator mismatch | exact 0.000e+00 (after fixing a real `h`-slot substitution bug — different Symbol assumptions made `.subs` miss) |
| CHK-2 negative control | leftover ≠ N·M | exact leftover identity + nonzero witness (2.226e-02; integrated 3.315357e-01) |
| CHK-6/I6 eq-(12) sign | wrong sign or missing measure piece | passes only with the `δN·(ℓaDW_b)` measure term; the naive `+ℓε'W'`-only version *fails* (I6c, −3.80e-02) and the wrong-sign variant fails (−7.79e-01) |
| I6b/I2b witnesses | identically-zero control | explicitly nonzero |
| homogenous limit (CHK-8) | nonzero residue | 0.000e+00 |
| branch sweep (CHK-10) | branch symbols shift residual | 50/50 zero for arbitrary branch values |

Failed intermediate attempts (preserved): `debug_pieces.py` — revealed the `h`-slot substitution bug (documented in `failed_attempts` of result.json); two grid-truncation residuals were *not* treated as physics failures but refined once as required.

## 7. Status

**Derived**: one full off-shell Ward relation for the heat sector (canonical r-IBP form with explicit endpoint multipliers), with the falsifiable negative control satisfied (leftover = `N·(L_b ξ∂W_b − L_0 ξ∂W_0) ≠ 0` when multipliers are omitted). Not promoted to complete gravity closure: the metric/clock identity needs the host-sector Ward chain (see result.json `next_unresolved_implication`).

## 8. Lean certificate

`AS138_ibp_endpoint.lean` — discrete r-IBP theorem `sum_mul_sub_endpoint` (generic over ℕ-indexed ℚ sequences), the ward-leftover corollary, and the AS138 3-difference instance. Verified with `lake env lean` (Lean 4.34.0-rc2, Mathlib cached at `fable_independent_2026/lean_2026`); **exit 0, zero `sorry`, axioms exactly {propext, Classical.choice, Quot.sound}** (unfiltered `#print axioms`). Compiled from the run directory; nothing written into `fable_independent_2026/lean_2026`.

## 9. Bounds actually enforced

Wall 3.55 s (symbolic) / 0.05 s (instance total incl. 2¹⁶ refinement); CPU `RLIMIT_CPU` 100 s + `ulimit -t`; memory 512 MB cap via RSS monitor (macOS `ru_maxrss` bytes; peak 83.5 MB symbolic, 46.8 MB instance — both far inside); 1 thread.
