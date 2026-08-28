# FC4AC — Q1: 2-DOF certificate with the spatial-diffeo brackets RESOLVED

**Certificate:** `fc4ac_dof_diffeo_2026.py` → `ALL BOOLEAN CHECKS PASS`, exit 0
(sympy 1.13.x, py 3.13). Output: `fc4ac_dof_diffeo_2026.out`.
Builds on the committed `openai_push/final_closure/scripts/03_dirac_matrix.py` (baseline
Pf = L_N·K) and resolves the caveat flagged in `ppn_mmg_gate_2026.py` line 0.6.

Auxiliary set: **S₁=π_N, S₂=C_M^(10) (MOND), S₃=C_q, S₄=C_p**, frozen kernel
μ₁₀(y)=y/(1+y¹⁰)^(1/10). Residual gauge = spatial diffeomorphisms H_i only.

---

## PART I — the 4×4 scalar auxiliary Dirac block, det ≠ 0 (COMPUTATION)

The only independent brackets are `L_N = {π_N,C_M}` and `K = {C_q,C_p}`:

- **L_N = δC_M/δN** = the linearised AQUAL principal symbol
  `c²[μ₁₀(y) k² + y μ₁₀'(y) (k·û)²]`. Both eigenvalues of the constitutive
  tensor are strictly positive on y>0: λ_⊥=μ₁₀>0, λ_∥=μ₁₀+yμ₁₀'=y(y¹⁰+2)/(1+y¹⁰)^(11/10)>0.
  **⇒ L_N>0** for k²>0 (mu_10 is the entry that carries the MOND kernel; it is what makes the
  block elliptic).
- **K = {C_q,C_p} = ½ k⁴** (from the committed {q,p}=½ normalisation), ≠0 for k≠0.

4×4 antisymmetric block (order S₁,S₂,S₃,S₄), off-diagonal placeholders b={C_M,C_q}, c={C_M,C_p}:

```
Pf(Δ) = L_N·K      (b,c drop out),      det(Δ) = (L_N·K)²
```

**On the generic branch (y>0 ⇒ L_N>0; k≠0 ⇒ K>0): det Δ = (L_N K)² > 0.**
The four scalar auxiliaries are second-class ⇒ the scalar canonical pair is removed.
This reproduces the committed baseline with μ₁₀ living in L_N. **PART I: PASS.**

---

## PART II — the spatial-diffeo brackets {S_A, H_i} (COMPUTATION — the new part)

`H[ξ]=∫ξⁱH_i` acts as the spatial Lie derivative `{F,H[ξ]}=L_ξ F`. An obstruction is a
**field-independent (c-number) inhomogeneous term** — it cannot be ∝ any constraint, so it
forces a genuine second-class pairing. Transformation laws (linearised, flat bg):

| Constraint | carrier field | δ_ξ(carrier) | {S_A, H_i} |
|---|---|---|---|
| S₁=π_N | N (scalar) | ξN′ (homogeneous) | **closes** (~π_N) |
| S₂=C_M^(10) | ln N (scalar); y scalar | ξ(lnN)′ (homog.) | **closes** (~C_M); kernel diffeo-safe |
| S₄=C_p | p York (scalar) | ξp′ (homogeneous) | **closes** (~C_p) |
| **S₃=C_q** | **q=⅙ ln det γ (NOT scalar)** | **ξq′ + ⅓ D·ξ** | **DOES NOT CLOSE** |

```
{C_q(x), H[ξ]} = (1/3) D²(D·ξ)(x)  +  (terms ~ constraints)
```

The `(1/3)D²(D·ξ)` piece is a c-number in the fields ⇒ **the LONGITUDINAL spatial diffeo H_L
is second-class with C_q**. This is the previously-uncomputed piece (`ppn_mmg_gate` 0.6). It is
**REAL and nonzero.** Transverse diffeos (D·ξ=0) give zero anomaly ⇒ **H_T stay first-class.**
Physical origin: the curvature *potential* Φ=−c²q is not a spatial scalar; **any constraint fixing
Φ acts as a gauge-fixing of the longitudinal diffeo.**

---

## PART III — does the anomaly collapse the count? Full scalar rank (DERIVATION)

Scalar phase space (Fourier mode): coords N,ψ,E,B + momenta π_N,p_ψ,p_E,p_B ⇒ **dim 8**.
Six scalar constraints: p_B(=π_L, primary FC — commutes with all), H_L, S₁,S₂,S₃,S₄.
Split off p_B (1 FC). The remaining 5×5 matrix (S₁,S₂,S₃,S₄,H_L) with the nonzero brackets
{S₁,S₂}=L_N, {S₃,S₄}=K, **{S₃,H_L}=A** (the anomaly), {S₂,S₃}=b, {S₂,S₄}=c:

```
rank(M5) = 4   (generic L_N,K,A ≠ 0)   ⇒   4 second-class + 1 first-class
nullspace dim = 1 : residual first-class combo  ∝ (−Ac/(K L_N)) S₁ − (A/K) S₄ + H_L
```

DOF arithmetic (scalar sector): FC = p_B + null combo = **2**; SC = **4**;
`scalar DOF = (8 − 2·2 − 4)/2 = 0`. Tensor: 2 TT gravitons. Vector: removed by (π_T,H_T).

> **N_grav = 2 tensor + 0 scalar + 0 vector = 2.**
> **The previously-uncomputed {C_q,H_i} piece does NOT collapse the 2-DOF certificate.**

The anomaly is a **healthy gauge-fixing pairing**: C_q gauge-fixes the longitudinal diffeo. The
net effect trades the longitudinal-diffeo first-class pair for a residual first-class mix of
(π_N, C_p, H_L) — **which** combination is gauge is reshuffled, but the arithmetic is preserved.
There is NO propagating scalar/E-mode; the referee's collapse scenario does not occur.

---

## PART IV — honest scope + caveats

- **What is a solid COMPUTATION:** the 4×4 det=(L_N K)²>0 with μ₁₀ (Part I); the diffeo anomaly
  {C_q,H_i}=⅓D²(D·ξ)≠0 (Part II) — matches the committed `ppn_mmg_gate` flag exactly.
- **What is DERIVATION (rests on covariance inputs, not a from-scratch canonical field computation):**
  the Part III rank-4 result models the scalar bracket matrix with the covariance-justified zeros
  {S₄,H_L}=0, {S₂,H_L}~0, {S₁,H_L}=0. These are physically forced (scalar/scalar-density
  transformation laws) but were entered as inputs, not independently canonical-verified.
- **LOCK-branch caveat (the γ_PPN=1 repair C_q=D²(q+lnN)):** C_q then contains ln N, so
  {S₁,S₃}=E≠0 appears and the 4×4 Pfaffian shifts L_N·K → L_N·K − E·c_M (committed
  `gate_fork_S2prime`). The diffeo anomaly is UNCHANGED (δ_ξ lnN is homogeneous, adds nothing;
  δ_ξ q keeps the ⅓D·ξ). Re-running Part III with the extra {S₁,S₃}=E entry gives **rank still 4
  ⇒ 2 DOF preserved** — but this is the same DERIVATION-level model and the lock still owes the
  full Dirac re-certification of {π_N,C_q}≠0 through Gates 3/6/7/8.

**Q1 VERDICT:** On the source-free / matched-MOND branch, the FC-4AC scalar sector certifies at
**exactly N_grav=2** *including* the diffeo brackets the old chassis left uncomputed. The 2-DOF
count is **NOT** the place the theory dies. The MOND-specific obstruction, if any, is downstream
(γ_PPN / Φ-vs-Ψ / α₃), not in the constraint count. This is a PASS for the DOF gate, not a closure.
