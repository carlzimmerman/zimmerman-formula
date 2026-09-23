# D-YM1 extension: BDL's tracked-constant Kirkwood–Thomas argument carried to Kogut–Susskind SU(N)

Date 2026-09-22. Committed as lane L326 after an independent adversarial referee pass (referee.py, r2.py, tori.py: no mathematical error found; BDL erratum confirmed). Sources:
**BDL** = Bravyi, DiVincenzo, Loss, CMP 284 (2008) 481, "Polynomial-time algorithm for simulation of weakly interacting quantum spin systems", arXiv:0707.1894 (open access).
**Repo** = `real_research/reviews/spectral_spine_closure_2026_09_22/i15/PROOF.md` §§1, 2, 4 and
`opus_49_doorE/REPORT.md` §3. Yarotsky's JMP 2004 paper stays unread. No constant is taken from it.

**Status.** Every step below is labelled RIGOROUS, meaning a complete argument is written here and names the BDL
statement it adapts, or GAP. The adaptation is new and has not been peer-reviewed. Under the repo's
"adversarial verification before commit" rule, it needs an independent audit before any repo claim.
The toy-model numerics in `checks.py` test the algebra. They do not prove it.

---

## 0. Model and dictionary (repo conventions, i15/PROOF.md §1–2)

`H = (x/2) Σ_l C_l + (b_N/x) Σ_p (1 − T_p)`, with `T_p = Re Tr U_p / N`, `‖T_p‖ ≤ 1`, `0 ≤ b_N ≤ 2N`, and
`C_F = (N²−1)/(2N) ≥ 3/4` the least nonzero Casimir (i15 §2). Divide by `s₀ = x C_F/2`. The plaquette
constant `(b_N/x)·#p` changes no gap, so we drop it:

**(E1)** `H/s₀ = Σ_l h_l + ε Σ_p V_p`, where `h_l = C_l/C_F` (unique zero vector = constant function, gap **Δ = 1**),
`V_p = −T_p` (**J = 1**) and `ε = 2b_N/(x² C_F) ≤ 32/(3x²)` for every N ≥ 2 and b_N ≤ 2N.

**(E2)** `λ := |ε| D J/Δ`. The hypergraph data are: s = sites per plaquette and D = the largest number of plaquettes that
meet one site. Two groupings are both admissible:
* LINK sites: s = 4, D = 2(d−1).
* VERTEX sites (the d outgoing links of a vertex form one site, as in i15 §4): s = 3, D = 3d(d−1)/2.

Both counts are brute-forced in `constants.py` S1.

## 1. Statement proved

**Theorem.** Take a finite set of sites. Each site has a separable Hilbert space `H_u` and a self-adjoint
`h_u ≥ 0` with compact resolvent, a simple eigenvalue 0 (vector `0_u`), and `h_u ≥ Δ` on `0_u^⊥`. Each plaquette
term `V_p` is bounded self-adjoint, acts on at most s sites, and has `‖V_p‖ ≤ J`. Every site meets at most D
plaquettes. Suppose `λ = |ε|DJ/Δ ≤ λ_c(s)`, with the **certified** values `λ_c(4) = 0.01190829` and
`λ_c(3) = 0.01790402` (`constants.py` S4, exact rational arithmetic). Then the lowest eigenvalue of
`H = Σ h_u + ε Σ_p V_p` is simple, and every other point of the spectrum lies at least `Δ/2` above it.
The constants do not depend on the number of sites, the boundary shape (open subgraphs, or tori of side ≥ 2),
the on-site dimension, or N.

**Gauge corollary.** Apply this to (E1). For `x ≥ X_d := sqrt((32/3) D/λ_c)` the model has a unique
gauge-invariant ground state and a spectral gap `≥ x C_F/4 ≥ 3x/16`. This holds for all N ≥ 2, all 0 ≤ b_N ≤ 2N,
and all finite volumes:

| d | X_d, link grouping | X_d, vertex grouping | **X_d (best)** |
|---|---|---|---|
| 2 | 42.33 | 42.28 | **42.3** |
| 3 | 59.86 | 73.23 | **59.9** |
| 4 | 73.31 | 103.56 | **73.3** |

In BDL's convention, `2ε₀ = ε_c = λ_c/D` (link grouping): d=2 gives 5.954e-3, d=3 gives 2.977e-3, d=4 gives 1.985e-3.
Door E writes `X_d = max(1, sqrt(2A_d/θ))`. The same X_d comes out of that formula with
**θ_equiv = 2mλ_c/D** (m = d(d−1)/2): θ = 1.19e-2 (d=2), 1.79e-2 (d=3), 2.38e-2 (d=4). This θ is an
*equivalent* value. It is **not** Yarotsky's c1 or c2.

## 2. The steps

**S1. Truncation to finite on-site dimension — RIGOROUS (new; BDL is finite-dimensional throughout).**
Let `P_Λ` be the spectral projection of each `h_u` onto `[0, Λ]`. It has finite rank because the resolvent is
compact, and `0_u ∈ Ran P_Λ`. Let `F_Λ = ⊗_u Ran P_Λ` and let `H_Λ` be the compression of H to `F_Λ`. Because
`P_Λ` commutes with `h_u`, the free part of `H_Λ` is `Σ h_u|_{F_Λ}` with the same Δ. Each compressed plaquette term
`(⊗_{u∈p}P_Λ) V_p (⊗_{u∈p}P_Λ)` is still supported on p and still has norm ≤ J. So `H_Λ` is a finite-dimensional
instance of the Theorem with the *same* (Δ, J, s, D).

Next, the full H is self-adjoint on `D(H₀)` (Kato–Rellich, V bounded) and has compact resolvent in finite volume.
The union `∪_Λ F_Λ` is the span of H₀-eigenvectors, which is a core. By min–max, the Ritz values satisfy
`E_k(H_Λ) ↓ E_k(H)`. So if every `H_Λ` has gap ≥ Δ/2, then `E₁(H) − E₀(H) = lim (E₁(H_Λ) − E₀(H_Λ)) ≥ Δ/2`,
and E₀(H) is simple. **An unbounded H₀ never enters a norm bound.** Only the resolvent lower bound in S2 is used.

**S2. Sector-valued creation operators — RIGOROUS (adapts BDL Def. 1, Claim 1 and the norm eq. (9)).**
Define `K_M = ⊗_{w∈M} 0_w^⊥`. For `c_M ∈ K_M` set `A[c_M] = |c_M⟩⟨0_M| ⊗ 1`. A creation operator is `C = Σ_{M≠∅} A[c_M]`,
with norm **`‖C‖₁ = max_u Σ_{M∋u} ‖c_M‖`**. The operator `A[c_M]` has operator norm `‖c_M‖`. If M∩K ≠ ∅ then
`A[c_M]A[c_K] = 0 = A[c_K]A[c_M]`. So all creation operators commute, and any product that repeats a site vanishes.
`H₀^M := Σ_{w∈M} h_w` satisfies **`H₀^M ≥ Δ|M|` on `K_M`**. BDL's qubit coefficient `C(M)` is the special case
`dim 0_u^⊥ = 1`. A qudit ℓ¹ coefficient norm would **not** work here: summing over the colours on the plaquette
sites costs a factor that grows with the on-site dimension. The sector norm avoids this.

**S3. Lemma 1′ — RIGOROUS (BDL Lemma 1, eq. (11)).** `[H₀, A[c_M]] = A[H₀^M c_M]`, because `⟨0_M|H₀^M = 0`.
So `[C₂, H₀]` is again a creation operator, and `[C₁,[C₂,H₀]] = 0`. It follows that `e^{Ĉ}(H₀) = H₀ + Ĉ(H₀)` (BDL (13)).

**S4. Lemma 2′, nested-commutator depth 2s — RIGOROUS (BDL Lemma 2, eqs. (12), (14)).** The C's commute, so a
factor whose M misses p can be moved inward and gives zero. Expanding gives `Σ_S ± A_S V_p A_{S^c}`. By pigeonhole,
more than s factors on one side means two of them share a site of p, and that product is zero. Hence
`ad_{C₁}…ad_{C_k}(V_p) = 0` for `k ≥ 2s+1`. So `e^{Ĉ}(V) = Σ_{k=0}^{2s} Ĉ^k(V)/k!`. **For plaquettes the
depth is 8** (BDL: 4), and 8 is attained (`checks.py` C2: ad⁸ ≠ 0, ad⁹ = 0). In the gap criterion the depth is
2s−1 = 7 (BDL: 3).

**S5. Claim 3′ — RIGOROUS (BDL Claim 3).** `Π_M ad_{A₁}…ad_{A_k}(V_p)Ω ≠ 0` requires two things:
(i) every M_i meets p; (ii) `N∖p ⊆ M ⊆ N∪p`, where N = ∪M_i. The reason for (ii) is that off p every created
site stays excited and can be created only once. So M = (N∖p)∪T with T ⊆ p, which gives **2^s = 16 sectors**
(BDL: 4). Checked in `checks.py` C3.

**S6. Kirkwood–Thomas equations — RIGOROUS in finite dimension (BDL (10), (15)–(18), (27)–(29)).**
`ψ = e^{−C}Ω` is an eigenvector if and only if `H₀^M c_M = ε Π_M e^{Ĉ}(V)Ω` for every M ≠ ∅. Its eigenvalue is
`E = ε⟨Ω, e^{Ĉ}(V)Ω⟩`. The power-series recursion is BDL (28) with k running up to 2s.

**S7. Lemma 3′ with explicit constants — RIGOROUS (BDL Lemma 3 eq. (19); App. A eqs. (67)–(71)).**
Let C_new have components `(H₀^M)^{-1} Π_M ad_{C₁}…ad_{C_k}(V)Ω`. Then
`‖C_new‖₁ ≤ β_k (DJ/Δ) Π‖C_i‖₁`, where
**(E5)** `β_k = 2^k (γ₀ s^k + k γ_S s^{k−1})`, and `β₀ = γ₀` bounds `‖C₁‖₁` (BDL (33)).
The steps, for each tuple τ = (M₁…M_k, p):
* The matrix element (BDL "≤ 2^k J") becomes `‖X_τΩ‖ ≤ 2^k J Π‖c_{M_i}‖`.
* BDL "count ≤ 4 sets M" is replaced by Cauchy–Schwarz over the orthogonal sectors of S5.
* Type 0 (u ∈ p) uses `|M| ≥ |T|`, which gives **(E3)** `γ₀² = Σ_{t=1}^{s} C(s−1,t−1)/t²`.
* Type j (u ∉ p, u ∈ M_j) uses `|M| = n′+|T|` with n′ ≥ 1 and **`|M_j| ≤ n′ + s ≤ (s+1)|M|`**, which gives
  **(E4)** `γ_S² = (s+1)² Σ_{t=0}^{s} C(s,t)/(t+1)²`. The maximum sits at n′ = 1 because each term decreases in n′
  (checked).
* BDL's eq. (69) factor 2 becomes **s = 4**, since each M_i must meet one of the 4 sites of p.
* BDL's `d|M_j|` becomes `D|M_j|`.

For s = 4: γ₀ = 1.4649, γ_S = 8.5975, β₁ = 28.9, β₂ = 369, …, β₈ = 3.13e8.
`checks.py` C5 finds a worst random or adversarial ratio of 0.013 ≤ 1.
**Erratum found in BDL App. A.** The line "v ∈ M_j ⇒ M_j ⊆ M ∪ {w}, so |M_j| ≤ 2|M|" is false. Counterexample:
M = {u}, M_j = {u,v,w}, V = σˣ_vσˣ_w gives a nonzero element (`checks.py` C4). The correct bound is 3|M|. BDL's
constant 2^13 still holds, because the corrected sum is 7168 ≤ 8192 (`constants.py` S3).

**S8. Lemma 5′, majorant — RIGOROUS (BDL Lemma 5, eqs. (34)–(41), Cor. 3).**
We have `χ_p = ‖C_p‖₁ ≤ (DJ/Δ)^p μ_p`, where `μ = λ q(μ)` and
**(E6)** `q(μ) = β₀ + Σ_{k=1}^{2s} β_k μ^k/k!`. This uses k-dependent β_k where BDL used one uniform b.
The Picard iterates `f_{n+1} = λ q(f_n)` have nonnegative coefficients, agree with μ up to order n, and stay
below the least positive root μ*(λ). Hence **(E7)** `‖C‖₁ ≤ Σ μ_p λ^p ≤ μ*(λ)` whenever that root exists.
This replaces BDL's Claim 2 disc argument, which gives the weaker radius.

**S9. Lemma 4′, gap criterion — RIGOROUS (BDL Lemma 4, eqs. (21)–(24)).** Suppose `Hφ = (E+δ)φ`, `|δ| < Δ/2`,
and φ is independent of ψ. Then B is defined by `e^{C}φ = (B+β₀)Ω`, and
`b_M = ε (H₀^M − δ)^{-1} Π_M B̂ e^{Ĉ}(V)Ω` with `‖(H₀^M − δ)^{-1}‖ ≤ 2/(Δ|M|)`. S7 applied to (B, C, …, C) gives
`‖B‖₁ ≤ 2λ q′(‖C‖₁) ‖B‖₁`. This is a contradiction if **(E8)** `2λ q′(μ*(λ)) < 1`.

**S10. No level crossing — RIGOROUS (BDL Cor. 2, 4).** C(ε) is continuous on [−ε_c, ε_c], E′(0) = 0 is the
ground energy of H₀, and E′ stays simple and separated by Δ/2. So E′ is the ground energy throughout.
**(E9)** The threshold λ_c solves `q(μ) = 2μq′(μ)` and then `λ = μ/q(μ)`. It is certified by checking in
exact rationals, with upward-rounded γ's, that `μ_c ≥ λ_c q(μ_c)` and `2λ_c q′(μ_c) < 1`.
Cross-check: with BDL's own constants (a=2, b=2^13, depth 4) this procedure gives λ = 6.10e-5 ≥ 2^{-17}.
It reproduces BDL's Theorem 1.

**S11. Gauge sector — RIGOROUS (inherited, i15 §4 "Gauge constraint").** The unique ground vector spans a
one-dimensional continuous representation of a finite product of SU(N)'s. That representation is trivial, so the
vector is gauge invariant. Restricting to the physical space cannot lower the gap.

## 3. Where BDL's special structure is used, and whether each use survives

| BDL use | Survives? |
|---|---|
| Qubit `a†=|1⟩⟨0|`, one excited level (Def. 1, Lemma 1) | Yes, with sector-valued A[c_M] (S2, S3) |
| ℓ¹ norm over basis coefficients, "≤ 4 sets" (eq. 9, App. A) | **Not as written.** The qudit ℓ¹ norm depends on dimension. Survives with the sector norm plus Cauchy–Schwarz (S7) |
| Two-body: depth 4, 4 sets, factor 2, (d+1) in χ₁ | Becomes depth 8, 16 sectors, factor 4, γ₀D (S4, S5, S7) |
| `|M_j| ≤ 2|M|` | False even for qubits. Becomes (s+1)|M| = 5|M| (S7) |
| Finite dimension (e^C finite sum, eigenvalue continuity) | Handled by truncation plus the Ritz limit (S1) |
| Unbounded H₀ | Enters only through `H₀^M ≥ Δ|M|`; no norm of H₀ is used |

**The prior reader's counts:**
* "4 → 16 sets" is correct as a count; the proof uses the sharper γ factors.
* "Depth" is 8 (and 7 in the gap criterion).
* "|M_j| ≤ 4|M|" is **wrong**; the correct bound is 5|M|.
* "Factor 2 → 4" is correct.

Pure counting (without Cauchy–Schwarz) would give λ_c = 0.00136, about 3× worse in X_d (`constants.py` S5).

## 4. GAPs and scope

* **GAP-1 (infinite volume).** i15 §4's second bullet (GNS Hamiltonian of the thermodynamic state) is not
  delivered. BDL's argument is finite-volume only. That bullet still rests on Yarotsky Th. 3, whose constants
  are not explicit.
* **GAP-2 (review).** S1–S10 are a new adaptation with no external review. `checks.py` covers each lemma on
  qutrit toys, which is evidence and not proof.
* **Scope.** N-uniformity holds at fixed x = g². At fixed 't Hooft coupling it fails, as i15 already says.
  Nothing here concerns the continuum limit.

## 5. Bottom line

The result is an **explicit, volume-uniform, N-uniform** threshold: X_2 ≈ 42.3, X_3 ≈ 59.9, X_4 ≈ 73.3,
with gap ≥ 3x/16. It is conditional on GAP-2. The worst case is at N = 2 with b_N = 2N. The N-dependent refinement
is `X_d(N) = sqrt((2b_N/C_F) D/λ_c)`. For the repo's YM05 choice b_N = 2 this is 29.9/22.4/18.9 at d=2 for
N = 2/3/4, and it goes to 0 as N → ∞ (table in `constants.py` S6).

Comparison with the registered expectations:
* It answers door E's "not numerically evaluable", taking route (b) of the directive with an open source.
* It lies below door E's hypothetical θ = 1e-2 row (46/80/113).
* It lies below door G's *conditional* 53/274/1318.
* It bypasses the door G/L obstruction. That obstruction lives in Yarotsky's distance-weighted eq. (14), and BDL's
  unweighted per-site norm together with the Lemma 4 contradiction needs no far-field decay.
* It does **not** reach i15's hoped-for x ≥ 2 or x ≥ 8 window. It misses by a factor of about 5 (against 8)
  up to about 37 (against 2) in x.

## 6. Files

* `DERIVATION.md` (this file).
* `constants.py`: prints its inputs, implements (E3)–(E12), certifies λ_c in exact rationals, and prints tables.
  The saved run is `constants_output.txt`, ending "ALL CHECKS PASSED".
* `checks.py`: toy checks C1–C6. The saved run is `checks_output.txt`, ending "ALL TOY CHECKS PASSED".

## 7. Strengthening (2026-09-23)

* **Lean I21** (`fable_independent_2026/lean_2026/I21_ym1_combinatorics.lean`, 6 theorems, zero sorry) certifies
  the finite combinatorial skeleton the analytic lemmas rest on:
  - the Claim 3′ sector structure, M = (N∖p) ∪ (M∩p);
  - the ≤ 2^|p| sector count;
  - the depth pigeonhole (pairwise-disjoint sets meeting p number ≤ |p|, hence depth ≤ 2s);
  - |M_j| ≤ (s+1)|M|, with its two-body sharpness;
  - the BDL counterexample matrix element computed by the kernel: ⟨Ω|a_u[a†_{uvw}, X_vX_w]|Ω⟩ = −1.
* **An actual gauge-model instance** (`gauge_instance.py`): one SU(2) Kogut–Susskind plaquette in the FULL
  (non-gauge-projected) truncated Hilbert space (j ≤ 1, 38,416 states), exactly diagonalized.
  - Where the truncation has converged (x ≥ 5), the normalized gap is ≥ 0.998, far above the theorem's ½.
  - This is CONSISTENT but NON-DISCRIMINATING: a single plaquette never approaches the bound.
* **Second independent adversarial referee — interim** (final results to be appended):
  - Lemma 3′ worst ratios on four toy families (qubit n = 8, 12; qubit 2×2 torus; qutrit two-plaquette) fall
    from 0.15 (k = 1) to ~1.7e-4 (k = 6), all ≪ 1.
  - The per-tuple sector Cauchy–Schwarz step (the source of the 3× sharpening over the second method) is
    tight but holds: worst ratio 0.98 at k = 0, decreasing with k.
  - k = 7–8 and the near-threshold KT-vs-ED gap scan are still running.
