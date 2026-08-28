# FC-FINAL 4-AC Type-II MMG — INVERSE-DESIGN **ATTEMPT B** (explicit auxiliary scalar sector)

**Certificate:** `inverse_chain_B.py` → `ALL BOOLEAN CHECKS PASS (exit 0)`, 16/16 (sympy 1.13.1,
numpy 1.26.4, py 3.13.9). Frozen output: `inverse_chain_B.out`. Independent of attempt A.

**Task.** Write an **explicit** canonical Hamiltonian `H_can` with an explicit auxiliary scalar
sector (à la De Felice–Mukohyama–Pookkillath, arXiv 2302.02090), **generate** the Dirac chain
`S_1→S_2→S_3→S_4` by preservation (never guessed), compute `Delta_AB={S_A,S_B}` and its **rank**,
and decide: **is a spatial-gradient (elliptic) `C_M^(10)` COMPATIBLE with `rank Delta=4`, or does
the gradient structure force early closure / degeneracy?**

Honesty labels: `THEOREM | DERIVATION | COMPUTATION | EXTERNAL-INPUT | MODEL-ASSUMPTION | OPEN | FAILED`.
The explicit `H_can` (§2) is the missing input; **no `det Δ` / slip number is produced without it.**
Frozen kernel `mu_10(y)=y/(1+y^10)^{1/10}` (`mu_10>0`, `mu_10+y mu_10'>0`). Phenomenological input,
never derived: `a0²=κ²c²Gρ_Λ`, `a0(z)~√ρ_DE`, `κ=1/2`, `Z~21`.

---

## 1. Control — the analytic kill of the *guessed* chain is reproduced (DERIVATION, cert Part 0)

The dead guess `S_2=D²q`, `S_3=D²p_q`: in static spherical **vacuum**, `D²q=0 ⇒ q'=A/r²`. The MOND
constraint we actually want is `r²μ_10(|q'|/a0)q' = const`. With `q'=A/r²`,
`d/dr[r²μ_10 q'] = −(strictly positive)·A² < 0` at all `A>0,r>0` (12 sample points, all strictly
negative) — the flux is **monotone in `r`, never constant** — so the two are incompatible unless
`A=0 ⇒ q'≡0` (**no MOND exterior**). This is why the scalar partners must be **generated**, not
hand-picked. Attempt B generates them, and the generated `S_2` is the **full nonlinear AQUAL flux,
not `D²q`**, so the kill does **not** transfer.

---

## 2. The explicit `H_can` (the missing input) — DERIVATION + one MODEL-ASSUMPTION

Scalar sector shown (TT gravitons + shift = spectators for this chain):
phase space `(N,π_N)`, `(q,p_q)` with `{N,π_N}=1`, `{q,p_q}=1`,
`q=−(1/6)ln det γ`, `p_q=−2γ_{ij}π^{ij}`. Weak-field dictionary (committed convention):
`q=−Φ/c²+O(c⁻⁴)` (**curvature** Φ, lensing), `ln N=+Ψ/c²+O(c⁻⁴)` (**lapse** Ψ, dynamics).

```
H_can = ∫ d³x [  N · C_M^(10)(q,γ)  +  (σ/2) p_q²  +  H_TT  +  H_m  ]
C_M^(10) = (c⁴/4πG)√g D_i[ μ_10(y) D^i q ] − √g c² ρ ,   y = (c²/a0)|Dq| .
```
`σ` = the conformal kinetic sign (tested `±1`). The **kernel rides on `q`** (not `ln N`). Two facts
follow (DERIVATION, cert Part 1):

- **(i) `π_N`-preservation yields `C_M`.** `H_can` is linear in `N` with coefficient `C_M`, so
  `{π_N,H_can}=−δH_can/δN=−C_M` ⇒ preserving `S_1=π_N` gives **exactly** `S_2=C_M^(10)`.
  This *requires* `C_M` to be `N`-independent (kernel on `q`).
- **(ii) The Embedding-I dichotomy.** `N`-independence ⇒ `{π_N,C_M}=δC_M/δN=0`. The `(π_N,C_M)`
  pair is **not itself second-class**; second-class-ness is **deferred to the generated `S_3,S_4`.**
  *(Contrast Embedding II, kernel on `ln N`: `{π_N,C_M}=L_N≠0` **but** `δH/δN=C_M+N δC_M/δN≠C_M`, so
  `π_N`-preservation does **not** return `C_M` — it fails the task's spec. Embedding I is forced.)*

Only the `(σ/2)p_q²` **kinetic term is a MODEL-ASSUMPTION** (the replaced GR refoliation sector);
everything else is fixed by the ADM structure and the kernel.

---

## 3. The generated chain (COMPUTATION, exact lattice — cert Part 2)

Poisson brackets made exact on a periodic `n`-site lattice (finite-difference derivatives; `|Dq|`
regularised as `√(s²+ε²)` = a tiny transverse gradient, the honest 2D/3D situation — the kernel is
smooth wherever the gradient **vector** is nonzero; only the measure-zero 1D kink at `s=0`, never
sampled, is smoothed). The Dirac algorithm returns:

| step | constraint | generated form | note |
|---|---|---|---|
| `S_1` | `π_N` | primary | |
| `S_2` | `C_M^(10)` | `= −{π_N,H_can}` | the MOND constraint, **not** guessed |
| `S_3` | `σ L̂[p_q]` | `L̂ = D_i A^{ij} D_j` | **the full MOND Hessian on `p_q`, NOT `D²p_q`** |
| `S_4` | `σ² Ĉ[p_q,p_q] − σ L̂²[N]` | contains `N` | ⇒ `{π_N,S_4}≠0` |

`A^{ij}=μ_10 δ^{ij}+y μ_10' n^i n^j` (frozen AQUAL Hessian; eigenvalues `μ_10>0`, `μ_10+yμ_10'>0`).
Principal symbol `L_N = μ_10 k_⊥² + (μ_10+yμ_10') k_∥² > 0` for all `y>0`.

**Chain length is exactly 4 (DERIVATION).** With `H_T=H_can+u π_N`, the multiplier `u` first appears
in `Ṡ_k` only when `{S_k,π_N}≠0`. Since `{C_M,π_N}=0` and `{S_3,π_N}=0` (both `N`-independent), the
chain does **not** stop at `S_2` or `S_3`; it runs to `S_4`, where `{S_4,π_N}≠0` (verified:
`δS_4/δN≠0`) **fixes `u` and terminates**. So the length is the **Type-II count (4)**, not the
length-2 "lapse-only" closure of Embedding II. `S_4` is independent (it alone carries `N`).

---

## 4. rank(Δ) — the task's question, DECIDED (COMPUTATION + THEOREM, cert Part 3)

**Single-mode, closed form** (linearised about `p_q,bg=0`, `L_N` a positive symbol):
```
        S_1     S_2       S_3       S_4
Δ =  [   0       0         0     σL_N² ]
     [   0       0       σL_N²     0   ]
     [   0    −σL_N²       0       0   ]
     [ −σL_N²    0         0       0   ]
Pf(Δ) = σ² L_N⁴ ,   det(Δ) = σ⁴ L_N⁸ .
```
Second-class pairing is `(π_N,S_4)` and `(C_M,S_3)`: **`N` is removed with `π_N`, `q` with `p_q`.**
`rank Δ = 4 ⟺ L_N ≠ 0` (and `σ≠0`). Since `L_N>0` for **every** `y>0` by the **frozen-kernel
ellipticity**, `det Δ ≠ 0` on every propagating mode.

**Full nonlinear lattice** confirms: `rank Δ = 4(n−1)` for `n=3,4,5` — i.e. **rank 4 per nonzero
Fourier mode**; the single deficit-4 null space is the `k=0` homogeneous (cosmological) mode
(separate, known-healthy). `σ=−1` gives the same rank (`det ∝ σ⁴>0`) ⇒ the count is **insensitive to
the conformal kinetic sign**, and since `(q,p_q)` is *removed* it never propagates — **no scalar ghost;
only the 2 TT gravitons propagate**, `N_grav = (20−12−4)/2 = 2`.

> **ANSWER: the spatial-gradient `C_M^(10)` IS COMPATIBLE with `rank Δ=4`.** The chain does **not**
> close early (length 4, not 2) and does **not** degenerate on any propagating mode. The frozen-kernel
> ellipticity (`μ>0`, `μ+yμ'>0`) is **precisely** what makes `L_N>0` ⇒ `det Δ≠0`. This is the
> constructive result: the guessed-chain `D²q=0` obstruction (§1) is **removed** by generating the
> partners — `S_2` is the nonlinear AQUAL flux, `S_3` is the MOND Hessian on `p_q`.

**The only degeneracy** (cert Part 4): `det Δ = σ⁴L_N⁸ → 0` as `y→0` (`L_N∝y` in deep MOND); the
lattice min nonzero singular value `~ y^{3.96}`. This is confined to the **measure-zero `y=0` locus**
(galaxy centres, exactly homogeneous mode) — rank stays 4 for every sampled `y>0` (deep MOND
included). It is an **ill-conditioning** of the deep-MOND regime, not a rank drop. `[COMPUTATION;
whether the `Δ⁻¹→∞` conditioning is a physical strong-coupling problem = OPEN, tied to §5.]`

---

## 5. Where the MOND obstruction actually sits — the SLIP (DERIVATION, cert Part 5)

The rank gate **passes**; the MOND-specific death is **downstream** and is now **derived from the
generated chain itself**. The two potentials are fixed by **different** elliptic operators:

- `S_2 = C_M = 0` (exterior) ⇒ `r²·μ_10(y)·q' = const` — **curvature Φ**, radial stiffness `μ_10`
  (the **nonlinear** AQUAL flux).
- `S_4 = 0 ⇒ L̂[N]=0` (exterior) ⇒ `r²·(μ_10+y μ_10')·N' = const` — **lapse Ψ**, radial stiffness
  `μ_10+y μ_10'` (the **linearised** Hessian — forced, because the generated `S_4 = −σ L̂²[N]`).

Gradient slip (same source-matching):
```
Φ'/Ψ' = (μ_10 + y μ_10')/μ_10  =  1  (Newtonian, y→∞)   →   2  (deep MOND, y→0).
```
| y | 0.03 | 0.1 | 0.3 | 1.0 | 3.0 | 10 |
|---|---|---|---|---|---|---|
| slip `(μ+yμ')/μ` | 2.000 | 2.000 | 2.000 | 1.500 | 1.000 | 1.000 |

The slip is **`y`-dependent (factor-2 swing)** — **no constant normalisation sets `γ_PPN=1` at all
accelerations.** The swing itself is normalisation-independent (the values `{1,2}` assume equal source
constants; unequal constants rescale both but keep the factor-2 swing). This **reproduces** the
committed FC-4AC verdict (`γ_PPN=1` fails in the deep-MOND regime) and **derives its origin**: it is
**not** a free `C_q` design choice — the generated `S_4` is *forced* to be the linearised Hessian
`L̂²[N]`, whose stiffness `μ+yμ'` differs from `S_2`'s `μ`.

**Structural root (THEOREM-level, cert Part 5).** `H_can` must be **linear in `N`** — that is exactly
what makes `{π_N,H_can}=−C_M` reproduce the MOND constraint (fact (i), §2). Hence `δ²H_can/δN²=0`, so
`N` enters **every** generated constraint at most linearly, and `S_4` fixes `Ψ` through the
**linearised** Hessian (`μ+yμ'`) while `S_2` fixes `Φ` through the **nonlinear** flux (`μ`). The two
stiffnesses coincide iff `yμ'/μ→0`, i.e. only in the Newtonian limit `y→∞` — **never in the MOND
regime.** So `γ_PPN=1` is not merely unrealised but **structurally excluded** in Embedding I: the very
linearity that lets `π_N`-preservation deliver `C_M` also forces the lapse onto the wrong (linearised)
operator. This is the sharp, MOND-specific obstruction of attempt B.

**Sector-orthogonal, unchanged by this chain (EXTERNAL-INPUT, committed):**
- `α_3 = −1` — the elliptic `C_M`/lapse responds **instantaneously** to source kinetic energy
  (`ppn_mmg_gate_2026.py`); a functional of the `g_00` sector, `d α_3/d(q-sector)=0`.
- `∇_μ T^{μν} ≠ 0` at **Newtonian order** — the `C_M` multiplier is density-sourced
  (`fc4ac_matter_conservation.py`); `{π_N,H_can}=−(H_g+ε_n)` carries `ε_n` irremovably, and
  Embedding I shares that identity.

---

## 6. Verdict

| gate | result | basis |
|---|---|---|
| explicit `H_can` written | **YES** | §2 (kernel on `q`; `(σ/2)p_q²`) |
| `π_N`-preservation ⇒ `C_M` | **YES** | cert Part 1 (`{π_N,H}=−C_M`) |
| chain generated, length 4, terminates | **YES** | cert Parts 2–3 (`{S_4,π_N}≠0` fixes `u`) |
| `rank Δ = 4` (per propagating mode) | **YES — COMPATIBLE** | `det Δ=σ⁴L_N⁸`; lattice `4(n−1)` |
| early closure / generic degeneracy | **NO** | only `y=0` (measure-zero) degenerates |
| `Φ=Ψ` / `γ_PPN=1` | **NO (FAILED)** | slip `(μ+yμ')/μ`: `1→2`, no repair |
| `α_3=0`, `∇_μT^{μν}=0` | **NO (FAILED)** | sector-orthogonal, committed |

**Bottom line.** Attempt B is a genuine **explicit** 4-AC construction. It settles the narrow
structural question the guessed-chain analytic kill left open: **a real spatial-gradient MOND
constraint `C_M^(10)` IS compatible with the Type-II `rank Δ=4 / N_grav=2` count** — the chain is
generated (not guessed), has length exactly 4, and is non-degenerate on every propagating mode, with
the frozen-kernel ellipticity supplying the invertibility. **The DOF count is therefore *not* where
this theory dies.** It dies on the **slip**: the same generated chain that secures `rank Δ=4` *forces*
the lapse `Ψ` (via `S_4=σ² Ĉ − σ L̂²[N]`, stiffness `μ+yμ'`) to differ from the curvature `Φ` (via
`S_2`, stiffness `μ`), giving `γ_PPN≠1` in the MOND regime with no normalisation escape; and the
sector-orthogonal `α_3=−1` and Newtonian-order matter non-conservation persist. Attempt B thus
**relocates** the MOND-specific obstruction from "the chain closes early / degenerates" (FALSE) to
"the generated `S_2`/`S_4` operator mismatch forces a lensing slip" (the operative FAILED gate).

---

### Provenance
- **This task:** `inverse_chain_B.py` (+ `.out`) — analytic-kill control; explicit `H_can`;
  `{π_N,H}=−C_M`; `{π_N,C_M}=0` dichotomy; generated `S_3=σL̂[p_q]`, `S_4` carries `N`; single-mode
  `det Δ=σ⁴L_N⁸`; lattice `rank=4(n−1)` (n=3,4,5); `y→0` scan; `σ=±1`; slip `(μ+yμ')/μ = 1→2`.
- **Committed cross-refs:** `fc4ac_setup_scaffold.py` (`C_q→Φ→slip` map), `fc4ac_dof_diffeo_2026.py`
  (baseline `Pf=L_N K`, diffeo anomaly), `fc4ac_matter_conservation.py` (`∇T≠0` Newtonian order),
  `openai_push/final_closure/scripts/ppn_mmg_gate_2026.py` (`α_3=−1`, kernel-blind),
  `gate_fork_S2prime_matter_mondlaw.py` (the `q`-lock fork).
- **EXTERNAL-INPUT:** DFMP arXiv 2302.02090 (Type-II 4-AC, consistent matter coupling); Iyonaga–
  Kobayashi arXiv 2109.10615 (2-DOF spatially-covariant MMG, `γ_PPN=1`, `c_T=1` — **with GR recovered
  locally**, the opposite of a *local* MOND modification).
- **Difference from the earlier `FC4AC_DOF.md`:** that document **guessed** `S_3=C_q`, `S_4=C_p` and
  found `Pf=L_N·K` (Embedding II, `{π_N,C_M}=L_N`). Attempt B **generates** `S_3,S_4` from a
  from-scratch `H_can` in Embedding I, giving `det Δ=σ⁴L_N⁸` and the derived operator-mismatch slip.
