# FC-FINAL 4-AC Type-II MMG — Q3b: matter conservation on the **constructed** H_can (Embedding I)

**Question.** On the *explicit* canonical Hamiltonian of `inverse_chain_B.py` (Embedding I, kernel on
`q`), with the **generated** chain `S_1=π_N, S_2=C_M^(10), S_3=σL̂[p_q], S_4=σ²Ĉ−σL̂²[N]`, does
minimally-coupled matter satisfy `∇_μ T^{μν}=0` w.r.t. `g`? Compute `{H_matter,S_A}` and decide.

**Verdict: DERIVED — PASS** (`∇_μ T^{μν}=0` w.r.t. `g`, Newtonian order, in fact **exactly on the
constraint surface**). The old-chassis matter-conservation FAIL **does NOT transfer** to Embedding I.
This **corrects** the in-passing claim in `FC4AC_construct_B.md` §5 / `inverse_chain_B.py` ("`∇_μT^{μν}≠0`
at Newtonian order… Embedding I shares that identity"), which imported the Embedding-II (old-chassis)
result without re-deriving it. **The theory still dies — on the slip (`γ_PPN≠1`) and the
sector-orthogonal `α_3=−1` — but not here.**

**Certificate:** `fc4ac_matter2.py` → 21/21 boolean checks PASS, exit 0 (sympy 1.13.1, numpy 1.26.4).
Frozen: `fc4ac_matter2.out`. Independent nonperturbative pairing cross-check in-session (lattice n=4).

Honesty labels: `THEOREM | DERIVATION | COMPUTATION | EXTERNAL-INPUT | MODEL-ASSUMPTION | OPEN | FAILED`.
Phenomenological input, never derived: `a0²=κ²c²Gρ_Λ`, `κ=1/2`, `Z~21`.

---

## 0. The decisive structural difference (DERIVATION, cert Part 0)

Matter (dust) enters Embedding I **inside** `C_M` as the term `−√g c² ρ`, minimally coupled to `N`
(`H_can = ∫[N C_M + (σ/2)p_q² + H_TT]`, `√g=e^{−3q}`). Because `H_can` is **linear in `N` with
coefficient `C_M`**,

```
{π_N, H_can} = −δH_can/δN = −C_M = −S_2 .
```

`S_2=C_M` is an **imposed second-class constraint**, so `r_1 := {π_N,H_can} = −S_2` is **weakly zero**.
This is the flip:

| | old chassis (Emb. II, kernel on `lnN`) | **constructed H_can (Emb. I, kernel on `q`)** |
|---|---|---|
| `{π_N,C_M}` | `L_N ≠ 0` (immediate 2nd-class pair) | **`0`** (`C_M` is `N`-independent) |
| `{π_N,H_can}` | `−(H_g+ε_n)`, **not** a constraint ⇒ `≠0` | **`−C_M = −S_2`, a constraint ⇒ weakly `0`** |
| matter source `ε_n` | left over, feeds `λ_M` | **balanced inside `C_M=0`** (the MOND–Poisson eq) |

The matter density is genuinely present (`δC_M/δρ = −√g c² ≠ 0`) — it is not removed, it is **balanced
inside the constraint**, which is exactly why the transfer had to be re-derived, not assumed.

## 1. Generated chain with matter: `r_A` **are** the constraints (COMPUTATION, cert Part 1)

Exact periodic `n=4` lattice, matter as an external density `ρ_a` with the geometric weight
`√g_a=e^{−3q_a}` (so matter propagates into the *generated* constraints, not put in by hand):

- `{π_N,H}+C_M = 0` exactly ⇒ `r_1 = −S_2`.
- `r_2 := {S_2,H} = S_3` exactly; `r_3 := {S_3,H} = S_4` exactly (the chain is generated).
- `δS_3/δρ ≠ 0` and `δS_4/δρ ≠ 0`: **matter enters every generated constraint** — the question is
  whether its **multiplier** survives.
- **Lattice-exact pairing:** `{π_N,S_2}=0` and `{π_N,S_3}=0` (symbolic, all pairs), `{π_N,S_4}≠0`
  ⇒ **`π_N` pairs ONLY with `S_4`** ⇒ Dirac-block row 1 = `[0,0,0,d]`. This single fact drives §2.

So `r_1=−S_2, r_2=S_3, r_3=S_4` are all (±) imposed constraints ⇒ **weakly zero**; only
`r_4={S_4,H}=:W` is a genuine non-constraint (it fixes the one surviving multiplier).

## 2. The `C_M` multiplier is **not** density-sourced (COMPUTATION+THEOREM, cert Part 2)

Honest general block (only the lattice-firm zeros imposed; `{C_M,S_4}=b` and `{S_3,S_4}=e` kept
**nonzero**, as measured on the lattice):

```
        S_1   S_2   S_3   S_4
Δ =  [   0     0     0     d ]      d = {π_N,S_4} ≠ 0
     [   0     0     a     b ]      a = {C_M ,S_3} ≠ 0
     [   0    −a     0     e ]      b = {C_M ,S_4} ≠ 0
     [  −d    −b    −e     0 ]      e = {S_3 ,S_4} ≠ 0
det Δ = a² d²  (rank 4, independent of b,e).
```

Solving `Δλ = −r`, `r=(−S_2, S_3, S_4, W)`:

```
λ_M := λ_2 = (S_2 e + S_4 d)/(a d)   — a COMBINATION OF CONSTRAINTS
λ_3        = −(S_2 b + S_3 d)/(a d)
λ_4        =  S_2 / d
λ_1        = (S_3 e − S_4 b + W a)/(a d)
```

On the constraint surface `Σ` (`S_2=S_3=S_4=0`): **`λ_M = λ_3 = λ_4 = 0` exactly**, and the only
survivor is `λ_1 = W/d`, which multiplies `S_1=π_N` — a constraint that carries **no matter**.

**Mechanism (robust to `b,e≠0`).** Row 1 `=[0,0,0,d]` (because `π_N` pairs only with `S_4`) forces
`λ_4=0` on `Σ`; then row 3, `−a λ_2 + e λ_4 = −S_4`, gives `λ_2=λ_M=0` regardless of `b,e`.

**Contrast (cert, reproduces the old FAIL).** Embedding II has `{π_N,C_M}=L_N≠0`, giving
`λ_M = −r_1/L_N` with `r_1=−(H_g+ε_n)` **not** a constraint ⇒ `λ_M≠0` ⇒ the committed Newtonian-order
FAIL. The whole flip is the single entry `{π_N,C_M}: L_N → 0`, which moves `λ_M` off the matter source
`r_1` and onto the constraint `S_4`.

## 3. No fifth force ⇒ `∇_μ T^{μν}=0` w.r.t. `g` (DERIVATION+THEOREM, cert Part 3)

Matter evolves by the Dirac bracket; the **non-metric (fifth) force** is
`F_5 = Σ_C λ_C {p_m,S_C}`. Only `S_2,S_3,S_4` carry matter (`{p_m,S_1}=0`), and on `Σ`
`λ_2=λ_3=λ_4=0`, so **`F_5=0` on `Σ`** — and this is **exact to all orders in `v/c`**, because
`λ_{2,3,4}` are proportional to the constraints as phase-space functions, not merely at Newtonian
order. Matter therefore feels **only the lapse**: `a = −∇lnN` (pure geodesic of `g`; no extra `X`,
unlike the old chassis' `a=−∇(Ψ+X)`), and for dust

```
∇_μ T^{μx}|_g = 0   EXACTLY   (minimal coupling + no fifth force).
```

Conservation holds w.r.t. **`g` itself**, not merely w.r.t. a bimetric `g_eff` — the old chassis'
two-potential disease (`G_eff=2G` baseline / deep-MOND repulsion lock) is **absent**. `∇_μT^{μν}=0` is
just the Noether identity of a 4D-scalar matter action once matter couples to `g` alone; imposing
`C_M=0` **is** the matter (MOND–Poisson) field equation that balances `ε_n`.

## 4. The trade: matter conservation is bought with the slip (THEOREM, cert Part 4)

The **same** linearity in `N` that makes `{π_N,H}=−C_M` a genuine constraint (`δ²H_can/δN²=0`) forces
`N` into every generated constraint linearly, so `S_4` fixes the lapse `Ψ` through the **linearised**
Hessian `(μ+yμ')` while `S_2` fixes the curvature `Φ` through the **nonlinear** flux `μ`:

```
slip Φ'/Ψ' = (μ_10+y μ_10')/μ_10 :  1 (Newtonian, y→∞)  →  2 (deep MOND, y→0)   ⇒  γ_PPN ≠ 1.
```

**Complementarity (Embedding I).** Matter conservation (PASS, this task) and `γ_PPN=1` **cannot both**
be evaded: the linear-in-`N` structure that secures the former forces the latter. Embedding II is the
mirror image — `{π_N,C_M}=L_N≠0` regains a shot at `Φ=Ψ` but loses matter conservation (old-chassis
FAIL). Either embedding fails **one** of the two; the constructed H_can fails on the **slip**, not here.

**Sector-orthogonal (EXTERNAL-INPUT, committed, unchanged):** `α_3=−1` (elliptic instantaneous lapse
response, `ppn_mmg_gate_2026.py`) — a `0i`-sector defect independent of this scalar matter analysis.

---

## 5. Verdict

| gate | result | basis |
|---|---|---|
| `{π_N,H_can}=−C_M` (matter inside `C_M`) | **YES** | cert Part 0 |
| `r_1=−S_2, r_2=S_3, r_3=S_4` are constraints | **YES** | cert Part 1 (lattice-exact) |
| matter enters generated `S_3,S_4` | **YES** | `δS/δρ≠0` |
| `π_N` pairs only with `S_4` (`{π_N,S_2}={π_N,S_3}=0`) | **YES** | cert Part 1 (symbolic) |
| `λ_M` density-sourced? | **NO** — `λ_M=0` on `Σ` | cert Part 2 (general block, robust to `b,e`) |
| fifth force `F_5` on matter | **0 on `Σ`, all orders** | cert Part 3 |
| **`∇_μ T^{μν}=0` w.r.t. `g`** | **YES (PASS)** | cert Part 3 — no fifth force + minimal coupling |
| bimetric `g_eff` needed? | **NO** | conserves w.r.t. `g` itself |
| `γ_PPN=1` / `Φ=Ψ` | **NO (FAILED)** | slip `(μ+yμ')/μ: 1→2`, cert Part 4 (operative death) |
| `α_3=0` | **NO (FAILED)** | sector-orthogonal, committed |

**Bottom line.** On the constructed Embedding-I `H_can`, `∇_μ T^{μν}=0` holds **w.r.t. `g`** because
the `C_M` multiplier `λ_M` is a combination of constraints (weakly zero) — a direct consequence of the
`{π_N,C_M}=0` dichotomy that defines Embedding I, in contrast to the old chassis where `λ_M=−r_1/L_N`
was density-sourced. Matter conservation is therefore **NOT** the Embedding-I obstruction; it is a
**PASS** that this task **derives** and that **corrects** the over-transferred committed claim. The
constructed theory still fails — decisively on the **slip** (`γ_PPN≠1`) and on `α_3=−1` — and the
matter-conservation PASS is exactly the complementary price of the slip.

### Caveats (honest)
- "Conservation" = no on-shell fifth force; it presupposes the second-class surface is consistently
  reached (`rank Δ=4`, `inverse_chain_B.py`) and that `C_M=0` is the matter field equation.
- Scalar/TT decoupling is an inherited **MODEL-ASSUMPTION**; full `q`–`h_TT` (York) coupling is a
  residual **OPEN** caveat (same class as `FC4AC_DOF.md` Part IV). Shift/`N^i` momentum sector taken
  standard (first-class diffeo, conserves momentum).

### Provenance
- **This task:** `fc4ac_matter2.py` (+ `.out`) — the Embedding-I identity `{π_N,H}=−C_M`; matter-
  augmented lattice `r_A=` constraints; `{π_N,S_2}={π_N,S_3}=0` pairing; general-block `λ_M=0` on `Σ`;
  fifth force `F_5=0`; `∇_μT^{μx}|_g=0`; the complementarity slip.
- **Corrects:** `FC4AC_construct_B.md` §5 / `inverse_chain_B.py` (in-passing `∇T≠0` transfer).
- **Contrast (committed):** `fc4ac_matter_conservation.py` (Embedding-II FAIL, `λ_M=−r_1/L_N`),
  `openai_push/final_closure/gate_matter_conservation_derivation.py` (`G_eff=2G`),
  `gate_fork_S2prime_matter_mondlaw.py` (lock-fork deep-MOND repulsion).
- **EXTERNAL-INPUT:** DFMP arXiv 2302.02090 (Type-II 4-AC, consistent matter coupling);
  `ppn_mmg_gate_2026.py` (`α_3=−1`); `inverse_chain_B.py` (`rank Δ=4`, slip `1→2`).
