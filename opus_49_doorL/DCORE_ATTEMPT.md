# DOOR L — X_d D-CORE: dressed-commutator bound (D) for the gauge model — attempted with Yarotsky's commutator-series structure (2026-09-22)

**Mandate.** Close door G's blocking inequality (D) for the specific lattice-gauge
model with an EXPLICIT constant M, using the one structure the crude route
cannot use: the perturbation is a *real multiplication operator* (class
function), zero-mean, operator norm ≤ 1, and the dressing
`e^{-A}[·,·]e^{A}` in arXiv:math-ph/0411042v1 §2 (eqs. (13)-(15), the line
`Σ_J ||(F_Λ v_I)_J|| ε^{-(d_{J;I}+1)} ≤ c sup||φ||^{|I|} ||v_I||`) is the
`e^{-A}φ_x e^{A}`-dressed family.  If (D) closes: deliver c1, c2, X_2, X_3, X_4.
If it fails: the exact first failing inequality and why the structure does not
rescue it.  No fabricated constants either way.

**Verdict (deliverable level 2, honest obstruction, machine-verified).**
(D) does **NOT close** through this structure.  The exact first failing
inequality is the *far-chain (family) sum bound* — the per-family weighted sum
over attaching clusters of the ground-state cloud — which is **numerically
falsified** (S7): for d = 2, ε = 1/128, inside a 9-site box, families of ≤ 2
clusters of size ≤ 2: the (8)-admissible share-constrained LP max of the
family sum is **8733.92** vs the claimed series **224** — a ratio of **39** —
and the per-site (8)-share constraints reduce the saturated sum by only 1.13%
(pairwise site-disjoint clusters saturate per-site budgets independently).
No explicit M can be certified from this route; hence **c1, c2, X_2, X_3, X_4
are NOT delivered** (nothing below is claimed as a theorem beyond the PROVEN
sections 2-4 and the quantified obstruction of section 5).

**Genuine positive gains over door G** (all proven, machine-verified):
1. the exact vanishing Lemma L1: for multiplication operators, the *first
   dressing order in the far field* is **exactly zero** — door G's Section-5
   divergence (single-site far creations `v̂_{{y}}φ_x u_I` with norm ~ ε) counts
   terms that vanish identically for this model;
2. the dressing identity: `e^{-A}[φ_x, v̂_I]e^{A} = [e^{-A}φ_x e^{A}, v̂_I]`
   (creation-algebra proof);
3. the near-field (J ⊆ hex∪I) bound with explicit constant M_near(d, ε).

---

## 1. Model and dictionary (from door G, verbatim)

- Sites = links; `H_x = L²(SU(N), Haar)`; free part `h_x = C_x/C_F`,
  `C_F = (N²−1)/(2N) ≥ 3/4`, gap exactly 1, ground vector Ω = constant 1.
- Perturbation range = hex `x+S`, `|S| = d+1`; on-site perturbation
  `φ_x = M_g`, *real multiplication operator* by a class function
  `g = −[2b_N/(x²C_F)] Σ_{i<j} f_{ij}` (plaquette traces), with:
  (i) `||φ_x|| = sup|g| ≤ η ≤ A_d/x²`;  (ii) **Haar zero mean**
  `<Ω, φ_x Ω> = 0` (each plaquette: E[Re Tr(U_p)] = 0 since the product of
  i.i.d. Haar variables is Haar, and ∫Tr = 0 — door G §1);  (iii) real ⇒
  self-adjoint;  (iv) each `f_p` is *degenerately zero-mean*: integrating out
  any proper subset of a plaquette's variables kills `f_p` identically
  (Haar-stability of the product).
- Ground-state cloud `{v_K}`, (8)-admissible: for every site x,
  `Σ_{K∋x} ||H_{K,0}v_K|| ε^{-(d_K+1)} ≤ 1`  (Lemma 1 of the arXiv paper), in
  particular `||v_K|| ≤ ε^{d_K+1}`.  Creation field `A = Σ_K v̂_K`,
  `v̂_I w = <w, Ω_{I,0}>u_I` (partial pairing over the I factors, identity on
  the rest).  Target (door G §6):

```
(D)   Σ_{J⊂Λ} ε^{-(d_{J;I}+1)} ||P_J e^{-A}[φ_x, v̂_I] e^{A} Ω|| ≤ M·η·||v_I|| .
```

---

## 2. PROVEN: exact vanishing of the first dressing order — Lemma L1

**L1.** Let `M_h` be any multiplication operator by a function of the hex
variables and let `K ∩ hex = ∅`.  Then `[v̂_K, M_h] = 0` **exactly**.

*Proof.* `v̂_K w = u_K ⊗ ∂_K w` where `∂_K` is the partial pairing against
`Ω_{K,0}` (integration over the K variables; identity on the remaining
factors).  Since `M_h` does not touch the K variables,
`∂_K(M_h w) = M_h(∂_K w)`, hence
`v̂_K M_h w = u_K ⊗ M_h∂_K w = M_h (u_K ⊗ ∂_K w) = M_h v̂_K w`.  ∎

(Same argument: `[v̂_K, Q] = 0` for any operator `Q` supported on sites
disjoint from `K`.)  Machine check: S0 — 300 random real diagonal `g` on a
3-site toy: `max|comm| < 1e-12`, while overlapping K gives `> 1e-3`.

**Consequence (corrects door G §5).** Door G's §5 "blocking divergence" used
single-site far clusters `{y}` with `||v_{{y}}|| ≤ ε`: the terms
`v̂_{{y}} φ_x u_I ⊗ ...` — the "far-field first order" — are **exactly zero**
by L1.  The relevant far-field contributions start at the *second* order:
clusters `K` that attach to the perturbation hex (`K ∩ hex ≠ ∅`), e.g.
straddling pairs `K = {x_h, y}`, `x_h ∈ hex`, with `d_K = dist(x_h, y)`.
(Also, degenerate zero-mean kills the vacuum-sector terms near the hex.)

---

## 3. PROVEN: the dressing identity — Lemma L2

All creations commute and `v̂_K² = 0` (S2), and `[A, v̂_I] = 0`.  By Jacobi,
`[v̂_K, [φ_x, v̂_I]] = [[v̂_K, φ_x], v̂_I] + [φ_x, [v̂_K, v̂_I]] =
[[v̂_K, φ_x], v̂_I]`, and inductively `(ad_A)^n[φ_x, v̂_I] =
[(ad_A)^n φ_x, v̂_I]`; summing the Born series:

```
e^{-A}[φ_x, v̂_I]e^{A} = [e^{-A}φ_x e^{A}, v̂_I],      φ̃_x := e^{-A}φ_x e^{A}
```

and the dressed commutator on the vacuum splits as

```
[φ̃_x, v̂_I]Ω = φ̃_x u_I − v̂_I φ̃_x Ω .
```

Machine check: S1 (toy 3-site algebra, 50 random instances, n ≤ 4).
Since the δ_K := [v̂_K, ·] commute and δ_K² = 0, the dressing factorizes as
`φ̃_x = Π_K (1 − δ_K) φ_x` (expansion over *families* of clusters, each
family once), and by L1 a family term is nonzero only if the clusters form an
**attaching chain**: some ordering with `K_i ∩ (hex ∪ ∪_{j<i}K_j) ≠ ∅`.

---

## 4. PROVEN: the near field — Lemma L3

For sectors `J ⊆ hex ∪ I`: `Σ_{J ⊆ hex∪I} ε^{-(d_{J;I}+1)} ||P_J[φ̃_x,v̂_I]Ω||
≤ 2^{|hex∪I|/2}·ε^{-1}·2η·N_F` with `N_F = exp(2(d+1)B(d,ε))` (dressed-operator
norm via the product bound `||φ̃_x|| ≤ η·exp(2Σ_K||v_K||)`), so
`M_near(d,ε) = 2^{(d+1)/2}·2·2·ε^{-1}·N_F` — explicit:
M_near = 4098 (d=2), 1.8e4 (d=3), 6.6e4 (d=4) at ε = 1/(32d²).  (Weight
`ε^{-(d_{J;I}+1)} ≤ ε^{-1}`; norm via `||[φ̃_x,v̂_I]Ω|| ≤ 2||φ̃_x||·||u_I||`.)

---

## 5. THE EXACT FIRST FAILING INEQUALITY (the deliverable): the far-chain bound

**Attempted bound (A).** For `κ(d,ε) := 16(d+1)·B(d,ε)·ε^{-1}` with
`B(d,ε) = ε²/(1−4d²ε)` (door G S2), claim:

```
(A)  Σ_{attaching families {K_1..K_n}} Π_i (s_{K_i} ε^{d_{K_i}+1} 2^{|K_i|})
        · ε^{-(d_{∪K_i;I}+1)}   ≤   ε^{-1} (1 − κ)^{-1}
     for every (8)-admissible cloud:  s_K := ||v_K|| ε^{-(d_K+1)},
     Σ_{K∋x} s_K ≤ 1 for all x.
```

This is what the combination "Lemma 1 + counting lemmas (B1-B3) + L1-L3 +
sector-weight argument" must supply for the far-field `J`'s in (D); its RHS
feeds `M_far ≈ 2 ε^{-1} 2^{(d+1)/2} N_F (1−2κ)^{-1}`.

**The inequality (A) FAILS. Machine-verified (S7):**  d = 2, ε = 1/128,
9-site box (radius 1), families of ≤ 2 attaching clusters of size ≤ 2,
weight `ε^{-(d_{C;I}+1)}` with `d_{C;I}` = MST-reach of the *created set*
to I (the physically correct quantity — hex excluded from the reach; this
corrects a first, looser audit that used the whole-union reach):

| quantity | value |
|---|---|
| families (deduped) | 243 (18 depth-1, 225 depth-2) |
| naive all-s=1 family sum | 8833.46 |
| **share-LP max** (Σ_{K∋x} s_K ≤ 1) | **8733.92** (greedy: 8733.92) |
| claimed RHS of (A) at d=2, ε=1/128 | **224**  (κ = 0.4286) |
| **ratio** | **39.0** |

The LP max agrees with the naive sum within 1.13%: the per-site (8)-share
constraints do **not** suppress the family sum, because the optimizer selects
families of *pairwise site-disjoint* clusters which saturate their per-site
budgets independently (share of each family's cluster is 1).

**Why the real-multiplication / zero-mean structure does not rescue it.**
1. L1 is used and is real, but it only kills the *first* dressing order in the
   far field.  The terms that carry the mass — straddling pairs
   `K = {x_h, y}`, x_h ∈ hex — are *not* of the L1 type: `K ∩ hex ≠ ∅`.
   Their nested-commutator terms `[v̂_K, φ_x]u_I = u_K⊗∂_{x_h}(φ_xu_I)
   − φ_x(u_K⊗∂_{x_h}u_I)` are generically nonzero (the two pieces differ in
   where `g` acts; toy control in S0 shows overlap commutators are genuinely
   non-vanishing) with norm scale `η·||v_K||·||u_I||`, weight
   `ε^{-(d_{K;I}+1)} ≈ ε^{-dist(y,I)}`, cost `ε^{d_K+1} = ε^{dist+1}`: a flat
   per-cluster balance `ε^{O(1)}` which only the (8)-aggregation can bound
   (bounded, per site), and which forces the analysis to *many-cluster
   families* — where the count wins over the alternative signs.
2. Zero-mean deletes the vacuum sectors near the hex and the degenerate
   zero-mean kills plaquette-vacuum pairings — again near-field/boundary
   effects, of constant size, not the far-field scaling.
3. The (8)-shares, the one "extra" structural input available, reduce the
   saturated family sum by 1.13% (S7): the far-field constant is therefore
   ≥ 39× the naive-series value inside a 9-site box, already; the
   thermodynamic-limit constant cannot be certified from the accessible
   hypotheses, and no M built on (A) is valid.

**What would close (D) (not available in this session):** a quantitative
statement that the family sum's thermodynamic limit remains ≤ C·(9-site LP
value)·(stability), i.e. the fixed-point/contraction content of Lemma 1's
proof ([23], paywalled), or a cancellation mechanism below the per-family
norm counting showing that the family-sum overestimates `Σ_J
ε^{-(d_{J;I}+1)}||P_J·||` by a huge factor — nothing in the model structure
(S0-S4, L1-L3) provides either.

---

## 6. Consequences for the bridge

- c1 = 1/(2L), c2 = 4L with L = M(1+2B)e^{2B(1+B)} (door G Prop. R) and the
  resulting X_2, X_3, X_4: **NOT delivered**.  Any number in sections
  S5/S6's output would be conditional on the refuted (A) — publishing them
  would be fabricating constants.  (The numeric near-field M_near values in
  §4 are genuine but are only *one part* of M.)
- Honest status of I15-style claims: door G's conditional X_d's remain
  unproven; this door adds: (i) the exact mechanic by which the model's
  structure shortens the far-field (L1: first order exactly zero), and (ii)
  the exact, quantified spot where the remaining argument must live (the
  family sum, ≥ 39× off at the smallest nontrivial scale, share-stable).

## 7. Files

- `opus_49_doorL/DCORE_ATTEMPT.md` — this report.
- `opus_49_doorL/dcore_verify.py` — runnable verification:
  S0 exact vanishing (300 random g); S1 dressing identity; S2 creation
  algebra; S3-S4 door-G counting lemmas; S5 near-field constants; S7 the
  falsification of the far-chain bound (share-LP 8733.92 vs 224, ratio 39,
  share-reduction 1.13%).  Run: `python3 dcore_verify.py` → prints
  "PROVEN CHECKS PASSED: True; S7 ... reports False" (S7 is the documented
  refutation, by design).
- Commit `opus_49d doorL X_d D-CORE` — new folder only.