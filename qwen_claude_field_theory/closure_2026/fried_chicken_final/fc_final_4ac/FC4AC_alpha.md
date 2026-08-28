# FC-FINAL 4-AC Type-II MMG — Q4: preferred-frame PPN α₁ / α₂ / α₃ (0i sector)

**Question.** On the **constructed** Embedding-I `H_can` (attempt B, kernel on `q`), reduce the
scalar constraints, solve `g_0i` for a **moving** source, and extract the preferred-frame PPN
parameters `α₁, α₂, α₃`. Do the control's committed values (`α₁=4`, `α₃=−1`, from Embedding II)
**transfer**, or does the different embedding change them?

**Verdict: DERIVED — α₁ = 0, α₂ = 0 (PASS); α₃ ≠ 0 (FAIL, structural).** The control's `α₁ = 4`
does **NOT** transfer — it was a `γ_PPN = 0` artifact of Embedding II. Embedding I has `γ_PPN = 1`
at solar-system scale (kernel on `q`), which sends **`α₁ → 0` and `α₂ → 0`**: the 0i / gravito-
magnetic preferred-frame bounds are **PASSED**. `α₃` remains **nonzero** (`= C_Φ1 − 4 ∈ [−3,−2]`),
failing the pulsar bound by `>5×10¹⁹×`, but for a **g₀₀-sector / matter-conservation** reason
(slip-independent, as tasked), **not** the 0i sector.

**Certificate:** `fc4ac_alpha_ppn.py` → **ALL 12 BOOLEAN CHECKS PASS, exit 0** (sympy 1.13.1).
Frozen in `fc4ac_alpha_ppn.out`.

Honesty labels: `THEOREM | DERIVATION | COMPUTATION | EXTERNAL-INPUT | MODEL-ASSUMPTION | OPEN | FAILED`.
Phenomenological (never derived): `a0²=κ²c²Gρ_Λ`, `a0(z)~√ρ_DE`, `κ=1/2`, `Z~21`.

---

## 0. The one input that flips the answer: `γ_PPN = 1`, not `0` (DERIVATION, cert Part 0)

The α's are read out of the metric through the PPN dictionary, and `γ_PPN` sits inside the `V_i`
coefficient. Embedding I differs from the frozen control at exactly this point:

- **Control (Embedding II, kernel on `ln N`):** the scalar spatial sector is a **source-free**
  `D²q = 0`, so `γ_PPN = 0` exactly (`ppn_mmg_gate` Part 2, Cassini 4×10⁴σ).
- **Embedding I (kernel on `q`):** `C_M = 0` (exterior) ⇒ `r²μ_10(y)q' = const`. As `y→∞`,
  `μ_10→1` ⇒ `r²q' = const` — the **GR Hamiltonian constraint**, `q` sourced by density. The
  committed slip `Φ'/Ψ' = (μ_10+yμ_10')/μ_10 → 1` as `y→∞` (cert 0.1; `inverse_chain_B.out` l.81,
  "solar-system γ OK"). Hence **`γ_PPN = 1` at solar-system accelerations** (kernel corrections
  `<10⁻¹⁹`, control 1.5). `β_PPN = 1` is inherited unchanged (static `−g₀₀ = e^{−2U/c²}`).

This single change (`γ: 0→1`) is what re-decides the preferred-frame sector.

---

## 1. The 0i sector solve (COMPUTATION, cert Part 1)

The construction declares the **shift `N^i` / momentum constraint `H_i` a spectator** (standard GR,
dust source) for the scalar chain — a stated **MODEL-ASSUMPTION**. At `μ_10→1` this is exact: the
`{C_M, H_i}` non-closure (the `q = −(1/6)ln det γ` inhomogeneous-transport caveat, `ppn_mmg_gate`
0.6) is `O(1−μ_10) < 10⁻¹⁹` at 1 AU. Using the frozen control's **exact linearized-Einstein 0i
routine** but with the spatial metric **restored** to its `γ_PPN=1` form `h_ij = 2U δ_ij` (vs the
control's amputated `h_ij = 0`), the moving-source transverse equation gives (cert 1.2–1.3):

```
h_0x = −4 V_x  =  −(7/2) V_x − (1/2) W_x     ⇒     c_V = −7/2 ,  c_W = −1/2 .
```

The gravito-magnetic sector is **GR-identical** — as it must be, since the momentum constraint is
the GR one and the source is dust.

---

## 2. PPN dictionary → α₁, α₂, α₃ (COMPUTATION + THEOREM, cert Part 2)

Will's dictionary with `γ=1, β=1, c_V=−7/2, c_W=−1/2`, `C_Φ1` = the `g₀₀` `Φ_1` coefficient kept
**symbolic** (it is the `g₀₀` lapse sector — the "independent-of-slip" input that carries `α₃`):

```
alpha_1 = -2 c_V - 2 c_W - 4 gamma - 4  =  7 + 1 - 4 - 4  =  0      (INDEPENDENT of C_Φ1)
alpha_2 = -2 c_W - 1                     =  1 - 1          =  0      (INDEPENDENT of C_Φ1)
alpha_3 =  C_Φ1 - 2 gamma - 2            =  C_Φ1 - 4                 (the g_00-sector decider)
```

| PPN α | Embedding II (control, γ=0) | **Embedding I (constructed, γ=1)** | bound | verdict (Emb. I) |
|---|---|---|---|---|
| `α₁` | `4` (FAIL 4×10⁴×) | **`0`** | `|α₁|<10⁻⁴` | **PASS** |
| `α₂` | `0` | **`0`** | `|α₂|<2×10⁻⁷` | **PASS** |
| `α₃` | `C_Φ1−2 = −1` (FAIL) | **`C_Φ1−4 ∈ [−3,−2]`** | `|α₃|<4×10⁻²⁰` | **FAIL `>5×10¹⁹×`** |

---

## 3. Both-ways check: the `α₁ = 4 → 0` flip is **entirely** `γ` (cert Part 3)

With the **same** 0i coefficients (`c_V=−7/2, c_W=−1/2`), re-solving the dictionary at `γ=0` and
`γ=1`:

- `γ=0` (control II): `α₁ = 4`, `α₃ = C_Φ1 − 2` — reproduces `ppn_mmg_gate` exactly.
- `γ=1` (Embedding I): `α₁ = 0`, `α₃ = C_Φ1 − 4`.

`d(α₁)/dγ = −4`. **The control's `α₁ = 4` is a `γ_PPN = 0` artifact of Embedding II; it does NOT
transfer to Embedding I.** Reporting `α₁ = 4` for the constructed theory would be a **manufactured
deficit** — the honest 0i-sector result is `α₁ = α₂ = 0` (both PASS). `α₂ = 0` in **both**
embeddings (the one clean, `γ`-independent pass).

---

## 4. Why `α₃ ≠ 0` — structural, embedding-independent, and NOT the 0i sector (cert Part 4)

`α₃ = C_Φ1 − 4`, so `α₃ = 0 ⟺ C_Φ1 = 4 ⟺` momentum conserved (the GR value). Two facts fix it:

- **(a) THEOREM (matter MD `fc4ac_matter_conservation`, embedding-independent).** `C_M` is
  **second-class**, so `π_N`-preservation **fixes a multiplier** `λ_M` carrying the Eulerian energy
  density `ε_n` (not a first-class constraint). `λ_M ≠ 0 ⟺ H⊥_total ≠ 0` locally `⟺` the `a0`
  physics itself. This gives `∇_μ T^{μi} = −ρ ∂^i X ≠ 0` at **Newtonian order**. `α₃` is the `O(v²)`
  preferred-frame shadow of this: `α₃ = 0 ⟺ ∇_μT^{μi}=0 ⟺` first-class `H⊥` (GR). Second-class
  `C_M ⇒ α₃ ≠ 0`. Depends only on {minimal coupling ∧ second-class `π_N`} — so it **does** carry
  over from the control, unlike `α₁`.
- **(b) The value.** `C_Φ1` is set by how the source's kinetic energy `ε_n = ρ(1+v²/2c²)` (unit
  weight, universal) sources the effective lapse. Instantaneous unit-weight elliptic response
  (control-type, `G_eff=1`) ⇒ `C_Φ1 = 1 ⇒ α₃ = −3`; the density-doubling matter fork
  (`G_eff=2G`) ⇒ `C_Φ1 = 2 ⇒ α₃ = −2`. **`α₃ ∈ [−3,−2]`.**

The **number** `−3..−2` depends on the explicit reduced lapse–matter coupling, which the
scalar-sector `H_can` does **not** fix (**MODEL-ASSUMPTION-bounded**); **`α₃ ≠ 0` is
DERIVED/structural**. Either value blows the pulsar bound `|α₃|<4×10⁻²⁰` by `>5×10¹⁹×`. This is a
**`g₀₀` / matter-conservation** failure (slip-independent, as the task frames it), **not** a 0i
gravito-magnetic one.

---

## 5. Verdict

| gate | result | basis |
|---|---|---|
| `γ_PPN=1` at solar system (Emb. I) | **YES** | cert 0.1 (slip→1), committed `inverse_chain_B` |
| 0i solve `g_0i = −(7/2)V−(1/2)W` | **YES** | cert 1.2–1.3 (sympy linearized-G, moving source) |
| `α₁ = 0` | **PASS** | cert 2.2 (`−2c_V−2c_W−4γ−4 = 0`) |
| `α₂ = 0` | **PASS** | cert 2.3 (`−2c_W−1 = 0`); passes in both embeddings |
| control `α₁=4` transfers? | **NO** | cert 3.2 (`α₁=4↔γ=0` only; `dα₁/dγ=−4`) |
| `α₃ ≠ 0` | **FAIL `>5×10¹⁹×`** | cert 4.2 (`α₃=C_Φ1−4∈[−3,−2]`; second-class `C_M`) |

**Bottom line.** On the **constructed Embedding-I `H_can`**, the preferred-frame **0i sector is
clean**: `α₁ = α₂ = 0`, both PASS, because the kernel-on-`q` embedding restores `γ_PPN = 1` at
solar-system accelerations. The control's `α₁ = 4` was a `γ=0` (Embedding II) artifact and is
**not** a property of this construction — the honest result does not manufacture it. The surviving
preferred-frame failure is **`α₃ ≠ 0` (`∈[−3,−2]`)**, and it is **NOT** a 0i-sector effect: it is
the `g₀₀` / momentum-non-conservation shadow of the **second-class `C_M`** (matter MD theorem,
embedding-independent), the same root as the committed `∇_μT^{μν} ≠ 0`. So this task **removes** one
of the two committed preferred-frame kills (`α₁`) and **relocates** the survivor (`α₃`) out of the
0i sector into the matter-coupling sector — consistent with the construct-B finding that Embedding I
dies on the **slip + matter conservation**, not on the gravito-magnetic α's.

### Provenance
- **This task:** `fc4ac_alpha_ppn.py` (+ `.out`) — `γ_PPN=1` limit (slip→1); sympy 0i moving-source
  solve `c_V=−7/2, c_W=−1/2` with `h_ij=2Uδ_ij`; dictionary `α₁=0, α₂=0, α₃=C_Φ1−4`; both-ways
  `γ=0/1` flip; `α₃∈[−3,−2]` bound.
- **Committed cross-refs:** `openai_push/final_closure/scripts/ppn_mmg_gate_2026.py` (CONTROL,
  Embedding II: `γ=0, α₁=4, α₃=−1`), `FC4AC_construct_B.md` / `inverse_chain_B.py` (Embedding I
  `H_can`, slip→1 at solar system), `fc4ac_matter_conservation.py` (second-class `C_M ⇒ ∇T≠0`
  Newtonian order — the structural root of `α₃≠0`).
- **EXTERNAL-INPUT:** Will PPN dictionary (standard); DFMP arXiv 2302.02090; Iyonaga–Kobayashi
  arXiv 2109.10615.
