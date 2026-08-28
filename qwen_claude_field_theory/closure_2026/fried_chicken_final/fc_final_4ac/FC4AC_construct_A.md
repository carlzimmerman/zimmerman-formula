# FC-FINAL 4-AC — INVERSE-DESIGN **attempt A** (minimal explicit `H_can`)

**Task.** Write the *minimal* explicit canonical Hamiltonian — ADM spatial-diffeo sector
`N^i H_i` + matter `H_m` + lapse-fixing, with `N` non-dynamical (`π_N ≈ 0`) — chosen so that
preserving `π_N` yields exactly `C_M^(10)`. Then **Dirac-generate** (never guess)
`S_3 = {C_M, H_can}_red`, `S_4 = {S_3, H_can}_red`, decide `chain_result`, and reproduce the
spherical-vacuum control (why `D²q` is dead; why this chain avoids it).

**Certificate.** `inverse_chain_A.py` → `ALL BOOLEAN CHECKS PASS (23/23)`, exit 0
(sympy 1.13.1, numpy 1.26.4, py 3.13.9; frozen in `inverse_chain_A.out`).

**Verdict (one line).** `chain_result = CLOSES-EARLY-multiplier-fixed`. The minimal `H_can`
generates **only** the `(π_N, C_M)` second-class pair (`rank Δ = 2`, `det = L_N²`), preserving
`C_M` merely **fixes the lapse-velocity multiplier** `u_1`; no independent `S_3` is produced, so
`S_4` is never reached. `N_grav = 2(T) + 0(V) + 1(S) = 3`, **not** 2 — an extra conformal scalar
survives. This is **not** an artifact of `μ_10`; it is the F(A²)-lapse-carrier disease
(sf40/sf41) seen from the Dirac-chain side.

Honesty labels: `THEOREM | DERIVATION | COMPUTATION | EXTERNAL-INPUT | MODEL-ASSUMPTION | OPEN | FAILED`.

---

## 1. The explicit minimal `H_can` (written, not sketched)

```
H_can[γ,π; N, N^i] = ∫ d³x { W_AQUAL(N,γ,ρ)  +  N^i H_i  +  H_m }

  W_AQUAL = −(c⁴/8πG)√g F(|D lnN|²/a₀²) − √g c² ρ lnN            (lapse-fixing sector)
            δW_AQUAL/δ(lnN) = C_M^(10)
                            = (c⁴/4πG)√g D_i[ μ_10(y) D^i lnN ] − √g c² ρ ,  y=(c²/a₀)|D lnN|
  H_i     = −2 D_j π^j_i                                          (ADM momentum constraint)
  H_m     = matter Hamiltonian (minimal coupling; ρ = energy density)
```

- **MODEL-ASSUMPTION.** *Minimal* = **no** independent gravitational-kinetic `π^ij π_ij` term and
  **no** auxiliary Legendre pair. The only `π`-dependence in `H_can` is the **linear** shift term
  `N^i H_i`. This is exactly Carl's "ADM GR shift sector + lapse-fixing".
- **DERIVATION (cert P0, P1).** `{q, p_q} = 1` for `q = −(1/6)ln det γ`, `p_q = −2 γ_ij π^ij`
  (canonical conjugate pair). Preserving `π_N` gives the secondary `S_2 = C_M^(10) ≈ 0`, and
  `C_M` reduces to **exact AQUAL on the lapse** `Ψ = c² lnN`:
  `D_i[μ_10(|DΨ|/a₀) D^i Ψ] = 4πG ρ` (sympy residual `= 0`) ⇒ slow matter feels `a = −∇Ψ` ⇒
  correct flat rotation curves. **The physics is right; the DOF count is what fails.**
- **Carrier choice (load-bearing).** The MOND operator sits on the **lapse** `lnN` (operative arm =
  *modified gravity*), so `C_M` depends on `N`. Using the AQUAL potential `W_AQUAL` (not a bare
  `N·C_M[q]`) is what makes `{π_N, C_M} = −δC_M/δN = L_N ≠ 0`. The `q`-carrier variant (matching the
  frozen *written* `C_M=√g D_i[μ_10 D^i q]`) is strictly worse — §5.

---

## 2. The Dirac chain — generated, not guessed

| step | object | result | label |
|---|---|---|---|
| `S_1` | `π_N` | primary | — |
| `S_2` | `C_M^(10) = δH_can/δN` | secondary; exact AQUAL | DERIVATION (cert 1) |
| `{S_1,S_2}` | `{π_N, C_M} = −L_N` | `L_N = μ_10 k² + y μ_10' k∥² > 0` (elliptic, **invertible**) | DERIVATION (cert 2a–c) |
| `S_3` | `{C_M, H_can}_red` | `= L_{Ñ}C_M + {C_M,H_m} ≈ 0` **weakly** — **not** an independent constraint | DERIVATION (cert 3i–iii) |
| decider | `dot C_M ≈ 0` | **fixes the multiplier** `u_1` via `{C_M, u_1 π_N} = −u_1 L_N`, `L_N≠0` | DERIVATION (cert 3iv) |
| `S_4` | `{S_3, H_can}_red` | **NOT REACHED** (no independent `S_3`) | — |

Why `S_3 = {C_M,H_can}_red` collapses (term by term, all certified):

1. **`{C_M, ∫N C_M}_red = 0`** — `C_M` is **momentum-free** (`δC_M/δπ^ij = 0`); two `π`-free
   functionals of `γ` Poisson-commute. (cert 3i)
2. **`{C_M, ∫N^i H_i}_red = L_ξ C_M ∝ C_M`** — `C_M(lnN)` is a genuine **weight-1 scalar density**
   (`lnN` is a true scalar; `δ_ξ lnN = ξ·∂lnN`, no anomaly), so its diffeo variation is a total
   divergence `∂_i(ξ^i C_M)` ⇒ **weakly zero**. (cert 3ii; the metric derivation
   `δ_ξ q = ξ·∂q − (1/3)div ξ` in cert 3ii′ shows precisely why the *`q`*-carrier would instead
   carry a real `−(1/3)div ξ` anomaly.)
3. **`{C_M, H_m}_red = 0` in vacuum** — vacuum `C_M` carries no matter field. (cert 3iii)

So `dot C_M` is made to vanish **not** by a new constraint but by solving `−u_1 L_N ≈ 0` for the
lapse velocity `u_1` (well-defined, `L_N` elliptic-invertible). **The chain closes at `S_2`.**

---

## 3. The count — `rank Δ = 2`, `N_grav = 3` (COMPUTATION, cert 4)

Generated second-class block (the **only** pair the minimal chain produces):

```
Δ₂ = [[ 0 ,  L_N ],
      [−L_N,  0  ]] ,     det Δ₂ = L_N² ,  rank 2  (L_N = μ_10 k² + y μ_10' k∥² > 0).
```

The conformal momentum `P = p_q` is **absent** from both `S_1` and `S_2` ⇒ the pair `(q, p_q)` is
**unconstrained** ⇒ it propagates. SVT bookkeeping of the 20-dim phase space:

| sector | dim | first-class | second-class | DOF |
|---|---|---|---|---|
| scalar | 8 | `p_{BL}, H_L` (2) | `π_N, C_M` (2) | **(8−4−2)/2 = 1** |
| vector | 8 | `π_T, H_T` (4) | 0 | 0 |
| tensor | 4 | 0 | 0 | 2 |

**`N_grav = 2 + 0 + 1 = 3` — not 2.** The residual scalar is the conformal mode `(q,p_q)`.

**Contrast (cert 4h).** The *guessed* set `{π_N, C_M, D²q, D²p}` has
`Pf = L_N·K`, `det = (L_N K)²`, `rank 4 ⇒ 0 scalar ⇒ 2 DOF`. But its second pair `(D²q, D²p)`
is **put in by hand** — the minimal `H_can` does **not** dynamically generate it — **and** `D²q`
is spherically **dead** (§4). You get `{MOND exterior}` **XOR** `{rank-4 / 2 DOF}`, not both.

---

## 4. The spherical-vacuum control (reproduced; COMPUTATION, cert 5)

Radial static vacuum, `q'=dq/dr`, `y=(c²/a₀)|q'|`:

- **attempt-A constraint** `C_M = 0`: `(1/r²)(r² μ_10(y) q')' = 0 ⇒ r² μ_10(y) q' = C`.
  **Admits a nontrivial exterior.** Solving numerically (cert 5c) gives `q'(r) ∝ 1/r` exactly
  (`1.05, 0.333, 0.100, 0.0333, 0.0100` at `r=1,3,10,30,100`) ⇒ `v² ∼ r q' = const` — the
  **deep-MOND flat rotation curve** falls straight out.
- **guessed constraint** `D²q = 0`: `r² q' = A ⇒ q' = A/r²`. Imposing **both** `D²q=0` **and**
  `C_M=0` forces `μ_10(y) = C/A = const`; but `y = A/r²` **varies** and `μ_10` is strictly
  monotone (`μ_10' = (1+y¹⁰)^(−11/10) > 0`, cert 5a), hence **injective** ⇒ `y=const ⇒ A=0 ⇒ q'=0`.
  **No nontrivial MOND exterior — DEAD** (numeric spread `0.923` over `r=1..10`, cert 5b).

**Why the chain avoids the death — and the price.** attempt-A never imposes `D²q=0`; its generated
constraint `C_M=0` *is* the MOND equation, which has the flat-rotation exterior. So the
`D²q`-death is avoided. **But** the minimal `H_can` then generates only `rank 2`, so the conformal
mode is never removed ⇒ `N_grav = 3`. The pair that would remove it is the dead one, and it is not
generated anyway.

---

## 5. Cross-checks (cert 6)

- **(6a) THEOREM-consistency with sf40/sf41.** attempt-A carries MOND in the **lapse**; the
  F(A²)-lapse-carrier no-go proved a lapse MOND-nonlinearity reintroduces a propagating scalar
  (`2+1`). `N_grav=3` here is that same disease, now visible as *"the Dirac chain fails to produce
  the second constraint pair"*.
- **(6b) `q`-carrier variant** (matches the frozen *written* `C_M=√g D_i[μ_10 D^i q]`): then
  `{π_N,C_M}=0`, so `dot C_M` does **not** fix `u_1`; instead `C_M(q)` is **not** a covariant
  density (`δ_ξ q = ξ·∂q − (1/3)div ξ`, DERIVED cert 3ii′/6b), so `{C_M,H_i} ≠ 0` fixes the **shift**
  multiplier while `π_N` stays first-class ⇒ `N` is pure gauge. Also `rank 2 ⇒ N_grav=3`, strictly
  worse (lapse not even fixed). **Either carrier ⇒ `CLOSES-EARLY`, 3 DOF.**
- **(6c) The escape (EXTERNAL-INPUT, sf42, *not* attempt-A).** Putting MOND in an **auxiliary
  Legendre pair** `(χ,Φ)` with **independent momenta** `p_χ, p_Φ` gives `{p_χ,ψ_1}=−V''≠0` and an
  elliptic `{p_Φ,ψ_2}` ⇒ a nondegenerate 4×4 block ⇒ 2 second-class **pairs** ⇒ scalar removed ⇒
  2 DOF. That needs **two extra canonical pairs** the minimal `H_can` does not contain.

---

## 6. Structured result

| field | value |
|---|---|
| `h_can_written` | **true** — explicit `H_can` above; `δH_can/δN` yields `C_M^(10)` on `π_N`-preservation (cert P1). |
| `chain_result` | **`CLOSES-EARLY-multiplier-fixed`** |
| `S_3` | `{C_M,H_can}_red = L_{Ñ}C_M + {C_M,H_m} ≈ 0` weakly (vacuum: `∝ C_M`); **not** independent. |
| `S_4 status` | **NOT-REACHED** — chain closed at `S_2`; preserving `C_M` fixes `u_1` via `{π_N,C_M}=L_N≠0`. |
| `rank Δ` | **2** (`det Δ₂ = L_N²`), vs the rank-4 `(L_N K)²` the Type-II count needs. |
| `det Δ` | `L_N² = (μ_10 k² + y μ_10' k∥²)²` (the 2×2 generated block; the `K`-pair is absent). |
| obstruction | Minimal (kinetic-free) `H_can` produces only the `(π_N,C_M)` pair; it **cannot generate a second constraint pair on `(q,p_q)`**. The sole known supplier `(D²q,D²p)` is spherically **dead** and is not generated in any case ⇒ residual conformal scalar ⇒ `N_grav=3`. |

**Reaching `rank 4`/2 DOF therefore requires a *non-minimal* `H_can`** — the auxiliary Legendre
pair (sf42) or a genuine gravitational kinetic sector — i.e. **attempts B/C, not A**. attempt-A is
**FAILED for the Type-II 2-DOF goal**, with the failure DERIVED (not asserted) and independent of
the frozen kernel `μ_10`.

---

### Provenance
- **This task:** `inverse_chain_A.py` (+ `inverse_chain_A.out`) — the explicit `H_can`, the AQUAL
  reduction, `L_N` ellipticity, the term-by-term `S_3` collapse, the `u_1` multiplier-fix, the
  SVT count `N_grav=3`, the metric-derived `q`-anomaly, and the spherical-vacuum control. 23/23, exit 0.
- **Committed cross-refs (consistent):** `gate_dirac_branch_proofs.py` (`Pf=L_N K`, the two pairs);
  `fc4ac_dof_diffeo_2026.py` (guessed rank-4 ⇒ 2 DOF, with `{D²q,H_i}` anomaly as healthy
  gauge-fixing); `fc4ac_setup_scaffold.py` (weak-field dictionary `q↔Φ`, `lnN↔Ψ`);
  `02_newtonian_limit.py` (AQUAL); `sf40/sf41` (F(A²) lapse-carrier ⇒ scalar); `sf42_aux_legendre_dof_2026.py`
  (auxiliary-pair escape, 2 DOF).
- **EXTERNAL-INPUT:** De Felice–Mukohyama–Pookkillath arXiv 2302.02090 (Type-II, 4 second-class);
  Iyonaga–Kobayashi arXiv 2109.10615 (2-DOF spatially-covariant MMG — **with GR recovered locally**,
  not a local MOND gradient).
- **Labelled ASSUMED:** `a₀²=κ²c²Gρ_Λ`, `a₀(z)∼√ρ_DE`, `κ=1/2`, `Z~21` — phenomenological input,
  never derived.
