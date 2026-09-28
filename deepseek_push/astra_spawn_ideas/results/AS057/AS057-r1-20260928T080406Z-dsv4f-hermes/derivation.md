# AS057 — Dimension dependence of static-channel rank

**Run:** `AS057-r1-20260928T080406Z-dsv4f-hermes` · **Worker:** deepseek-v4-flash-0731 (openrouter) / Hermes subagent `sa-5-5baebc3d` (claim `claims/AS057.json`, state "running")
**Task hash (verified before execution):** `dabeefc18b2509122638df4dd87ce8db1671c19a13b020d10fa7385d3ec892c6`
**Branch:** CORE coefficient; conditional MU_n statistical response (as declared by the seed). Q / RAR / EXP / MONO are *not* used for conclusions.
**Outcome:** supports_scoped_claim — the named trace formula is an exact identity; its determinant/rank/decoupling content is derived; controls (capable of failing) passed; the d>1 invertibility statement does **not** extend to d=1 (determinant exposes the exception, as required).

---

## 1. Step 1 — precise claim, symbol dictionary, boundary conditions, assumptions

**Claim C (named mathematical object of the seed).** On `(d+1)`-dimensional Minkowski spacetime (`η = diag(−1, 1, …, 1)`, `d ≥ 1` spatial dimensions), take the static diagonal perturbation

```
g = η + h,   h₀₀ = −2Φ,   h_ii = −2Ψ (i = 1..d),   all off-diagonal h = 0,
```

with `Φ, Ψ` smooth, static (no `t` dependence), `Φ, Ψ → 0` at spatial infinity. With
`h^ρ_ν = η^{ρσ} h_{σν}`, `h = h^ρ_ρ = 2Φ − 2dΨ` (note: the raised `h⁰₀ = +2Φ`, so `h` is **not** `−2Φ`), `Δ = Σᵢ ∂ᵢ²` (flat spatial Laplacian), the linearized Ricci and Einstein tensors

```
R⁽¹⁾_{μν} = ½ ( ∂_ρ ∂_μ h^ρ_ν + ∂_ρ ∂_ν h^ρ_μ − □ h_{μν} − ∂_μ ∂_ν h ),   □ → Δ (static)
G⁽¹⁾_{μν} = R⁽¹⁾_{μν} − ½ η_{μν} R⁽¹⁾_sc ,   R⁽¹⁾_sc = η^{μν} R⁽¹⁾_{μν},
```

satisfy, for **every** spatial dimension `d` (exact polynomial identities in `d`):

```
G₀₀  = (d−1) ΔΨ                                                          (companion)
G_kk := Σᵢ Gᵢᵢ = (d−1) Δ(Φ−Ψ) + (d−1)(3−d) ΔΨ         ← THE SEED'S CLAIM
                 = (d−1) ΔΦ − (d−1)(d−2) ΔΨ          ← direct form (fully equivalent)
```

where "the cited trace" = the spatial-sector trace of the linearized **Einstein** tensor `δ^{ij}G_{ij}` (PD01's "spatial-trace sector", the channel `G^(1)_kk = 2Δ(Φ−Ψ)` at d=3).

**Units:** `Φ, Ψ` are dimensionless potentials; every channel carries the units of the source-side acceleration mapping `m·ΔΦ` (m/s² per unit potential; the linearized Poisson sector uses `G_N` only). Scale factors, signs and the `(d−1)`/`(3−d)` coefficients are the load-bearing content; no factors of 2 or π are dropped.

**Symbol dictionary:** `d` spatial dimension (real `> 0` in the polynomial identities; integer `≥ 1` in the concrete computations); `Δ` flat Laplacian; `Φ, Ψ` metric potentials; `G⁽¹⁾` linearized Einstein tensor; `λ := d−1` (the seed's diagnostic parameter); `s = c√(G_N ρ_Λ)` (vacuum rate, framework input); `Y = g/s`; `μ_n(Y) = 1−(1+Y)^{−n}`, symbolic `n ≥ 1`; `κ = a0/s` (κ = 1/2 **adopted**, not derived here).

**Boundary conditions:** static, weak field `|Φ|,|Ψ| ≪ 1`, fields vanish at infinity; the numeric grids use compactly supported Gaussian test fields.

**Assumptions (framework inputs, distinguished from conclusions):**
| Kind | Item |
|---|---|
| Framework input | `a0 = κ c √(G_N ρ_Λ)`, κ = 1/2 adopted (separate from any derivation) |
| Framework input | `s = c√(G_N ρ_Λ)`, `Y = g/s`, `r_M = √(G M_b/a0)`, `v_flat⁴ = G M_b a0` |
| Framework input | `μ_n(Y) = 1−(1+Y)^{−n}` with symbolic `n ≥ 1` (MU_n family; the adopted branch member is MU2, n = 2) |
| Premise (inherited from PD01/PD08, **not** re-derived here) | the response is the OR over the carrier's static channels; the OR-identification |
| Adopted | `G_N` only; `G_bare`, `G_cosmo` not invoked (no renormalization enters this sector) |
| **Conclusion (this run)** | the channel map, its determinant `(d−1)²`, rank 2 for d ≥ 2, rank 0 at d = 1, and the d = 3 decoupling |

**Sources inspected (hashes match `SOURCE_MANIFEST.json` exactly):** `deepseek_push/PD01_polarization_count.py` `37e39d1a…2c74d`, `deepseek_push/PD08_particle_free_derivation.py` `83f6054c…f0cfb`, `kappa_closure/k01_zero_mode_theorem_and_lambda_free_vacuum.py` `8df5a3ab…5b25c`. Mandatory reads (contracts/protocol): `FRAMEWORK_CONTRACT.md`, `RESULT_CONTRACT.json`, `FIRST_PRINCIPLES_AND_BRANCHING.md` (hashes in `result.json` → `input_sha256`). The seed itself: hash verified before execution (above).

---

## 2. Steps 2–3 — the derivation (all intermediate factors, signs, units)

**A1 — raised perturbation and its trace.** `h⁰₀ = η⁰⁰h₀₀ = (+1)(−2Φ)`… with the index raised by `η` (signature (−,+,…,+)): `h⁰₀ = −h₀₀·1 = +2Φ`? Careful: `η^{00} = −1`, so `h⁰₀ = η^{00}h₀₀ = (−1)(−2Φ) = +2Φ`. Spatial: `h^i_j = η^{ii}h_ij = (+1)(−2Ψδ_ij) = −2Ψδ_ij`. Hence

```
h = h^ρ_ρ = 2Φ − 2d Ψ .
```

**A2 — the double-derivative sums.** For *spatial* `μ,ν` the term `∂_ρ∂_μ h^ρ_ν` expands over `ρ`: only `ρ = μ` (giving `∂_μ² h^μ_ν = −2∂_μ∂_νΨ·δ_{μν}-type`) and `ρ = ν ≠ μ` (giving `−2∂_ν∂_μΨ`) contribute — each contributing one Kronecker-δ, i.e. no extra factor of `d` (this is the count that later produces `(d−1)`, not `d`). Both derivative terms together:

```
∂_ρ∂_μ h^ρ_ν + ∂_ρ∂_ν h^ρ_μ = −4 ∂_μ∂_ν Ψ   (spatial μ,ν; Kronecker contractions = 1 each,
                                                independent of d)
```

and `∂_ρ∂_μ h^ρ_ν = 0` whenever the differentiated index is temporal (static).

**A3 — the 00 sector.**
```
R⁽¹⁾₀₀ = ½ ( 0 + 0 − Δh₀₀ − 0 ) = ½(−Δ(−2Φ)) = +ΔΦ .
```

**A4 — the ij sector.** `□h_{ij} = Δh_{ij} = −2ΔΨ·δ_{ij}`, `∂_μ∂_ν h = 2∂_μ∂_νΦ − 2d ∂_μ∂_νΨ`:

```
R⁽¹⁾_{ij} = ½ [ −4∂_μ∂_νΨ + 2ΔΨ δ_ij − 2∂_μ∂_νΦ + 2d ∂_μ∂_νΨ ]
          = ΔΨ δ_ij − ∂_i∂_jΦ + (d−2) ∂_i∂_jΨ .
```

**A5 — traces.** `Σᵢ δ_ii = d` (this is the single `d`-counting rule):

```
Σᵢ R⁽¹⁾ᵢᵢ = d·ΔΨ − ΔΦ + (d−2)·ΔΨ = 2(d−1)ΔΨ − ΔΦ
R⁽¹⁾_sc = η^{μν}R⁽¹⁾_{μν} = −R₀₀ + ΣᵢRᵢᵢ = −2ΔΦ + 2(d−1)ΔΨ .
```

**A6 — the Einstein channels.** `η₀₀ = −1`, `η_ii = +1`:

```
G₀₀ = R₀₀ − ½η₀₀R_sc = ΔΦ + ½(−2ΔΦ + 2(d−1)ΔΨ) = (d−1)ΔΨ
G_kk = Σᵢ Gᵢᵢ = ΣᵢRᵢᵢ − (d/2)R_sc
     = 2(d−1)ΔΨ − ΔΦ − d[(d−1)ΔΨ − ΔΦ]
     = (d−1)ΔΦ − (d−1)(d−2)ΔΨ
     = (d−1)Δ(Φ−Ψ) + (d−1)(3−d)ΔΨ              ← the seed's claim, QED.
```

The equivalence of the two last lines is the polynomial identity `(d−1)(3−d) − (d−1) = −(d−1)(d−2)` (certified in Lean, `coeff_identity`).

### 2.1 The 2×2 coefficient matrix, its determinant and rank

In PD01's channel basis `(ΔΨ, Δ(Φ−Ψ))` the map `(ΔΨ, Δ(Φ−Ψ)) → (G₀₀, G_kk)` is

```
N(d) = ⎡ d−1         0      ⎤
       ⎣ (d−1)(3−d)  d−1   ⎦ ,     det N = (d−1)² ,   rank N = 2 ⟺ d ≠ 1 .
```

| d | N(d) | det | rank | reading |
|---|---|---|---|---|
| 1 | 0-matrix | **0** | **0** | both channels vanish identically (`G⁽¹⁾ ≡ 0`: the 2D Einstein tensor is identically zero since `R_{μν} = ½R g_{μν}` in 2D) — **the exception exposed by the determinant** |
| 2 | [[1,0],[1,1]] | 1 | 2 | triangular; Γ(=∂Φ) channel mixing; pure form `G₀₀=ΔΨ, G_kk=ΔΦ` |
| 3 | [[2,0],[0,2]] | 4 | 2 | **decoupling**: off-diagonal `(d−1)(3−d) = 0`, map diagonal, `G₀₀ = 2ΔΨ`, `G_kk = 2Δ(Φ−Ψ)` (PD01 B1) |
| 4 | [[3,0],[−3,3]] | 9 | 2 | off-diagonal sign flip (`(3−d) < 0` for d > 3) |

**The d=3 special is a decoupling, not a rank change.** At d = 3 the coefficient matrix diagonalizes (each channel becomes a single Poisson operator on one potential); the rank (2) is unchanged. Rank collapses only at d = 1. The task's separation ("Separate the special d=3 decoupling from rank") is satisfied: off-diagonal zeros ⇔ d ∈ {1, 3} (`decouples_iff`), determinant zeros ⇔ d = 1 (`det_sq_zero_iff`).

### 2.2 Leading neglected terms (limiting regimes used)

- **Linearization:** the channel computation is exact at first order in `h`; the neglected terms are `O(h²)` (curvature-quadratic `ΓΓ` content). Domain: weak field `|Φ|,|Ψ| ≪ 1`, i.e. `Φ ~ v²/c² ≲ 10⁻⁶` in galactic systems — comfortable.
- **Deep-MOND limit (used only for the κ-transfer check, Part 5):** `μ_n(Y) = 1−(1+Y)^{−n} = nY − ½n(n+1)Y² + O(Y³)`; the leading neglected term beyond `μ ≈ nY` is `−½n(n+1)Y²` (printed in the run log). Domain: `Y = g/s ≪ 1`, i.e. `g_N ≪ s` ⇔ `r ≫ r_M = √(G M_b/a0)`. The relative correction to `g²` along the deep branch is `O(Y)`.

---

## 3. Step 4 — independent checks (different representations, actual residuals)

**C1 — explicit connection (Christoffel) route, exact symbolic, d = 1..5.** Separate code path: build `g = η + h`, linearized connection `Γ⁽¹⁾^ρ_{μν} = ½η^{ρσ}(∂_μ h_{σν} + ∂_ν h_{σμ} − ∂_σ h_{μν})` over the *full* index range (statics enter only through `∂ₜ ≡ 0`), `R⁽¹⁾_{μν} = ∂_ρΓ⁽¹⁾^ρ_{μν} − ∂_νΓ⁽¹⁾^ρ_{μρ}` (ΓΓ terms are second order), `G⁽¹⁾ = R⁽¹⁾ − ½ηR_sc`. Generic radial `Φ(r), Ψ(r)` for d = 1..4, monomials for d = 5. **Residuals: 0 (exact) at every d** against both closed forms. The route caught and fixed two implementation errors during development (an exact-inverse nonlinearity and a missing `ρ=0` term in the second Ricci contraction) — i.e., the check was genuinely independent and capable of failing.

**D1 — numeric Christoffel route on finite grids, d = 2,3,4.** Grids: 121², 41³, 17⁴ points, Gaussians `Φ = e^{−r²/w²}`, `Ψ = 0.7e^{−1.3r²/w²}`; gradients by second-order central differences; channels assembled from the metric only. Threshold set before evaluation: max relative residual < 1e−2. **Measured (actual residuals):** d=2: `1.8e−16 / 4.5e−17`; d=3: `2.7e−16 / 2.7e−16`; d=4: `1.6e−16 / 3.2e−16` — machine-precision consistency of the channel decompositions (the residual, not a Boolean, is recorded in `AS057_raw.out`).

**B-series — general-d algebra:** `G₀₀ − (d−1)ΔΨ ≡ 0` and `G_kk − [claim form] ≡ 0` as polynomials in `d` (sympy, symbolic `d`), plus `det N = d²−2d+1 = (d−1)²`.

---

## 4. Step 5 — negative controls (each capable of failing)

- **NC1 — extend d>1 invertibility to d=1 (the seed's mandated control):** the statement "rank 2 for all d ≥ 1" is **false**; `det N(1) = 0`, rank 0, and the Christoffel route gives `G₀₀ = G_kk ≡ 0` for generic potentials (2D Einstein tensor identically zero). The determinant exposes the exception *exactly* (`(d−1)²` vanishes iff d = 1). Capable of failing: a wrong coefficient would leave `det N(1) ≠ 0` — the mutation tests below demonstrate discrimination.
- **NC2 — diagnostic counterexamples at λ ∈ {1/2, 1, 2} (λ := d−1):** claim form vs direct form at `d = 3/2, 2, 3`: `d=3/2`: `½ΔΦ + ¼ΔΨ` on both sides; `d=2`, `d=3`: differences 0. Because both forms are quadratic in λ, three distinct evaluation points pin the identity for **all real d** — including the non-integer regime where no grid exists. (This is the point of the seed's "do not use observational preference as a mathematical proof": the identity is pinned by the algebra, not by kappa's data.)
- **NC2b — discrimination:** the mutilated coefficients `(d−1)(4−d)` and `d·Δ(Φ−Ψ)` **fail** the same three-point probe (agreement = False, False). The controls genuinely discriminate the claimed coefficients.
- **NC3 — deep limit in d dimensions:** with `μ ≈ n·g/s` and the framework's Poisson convention `div(μ∇Φ) = 4πGρ`, the d-dimensional Gauss law gives `g² = g_N·(s/n)` where `g_N = 4πGM/(S_{d−1} r^{d−1})`, `S_{d−1} = 2π^{d/2}/Γ(d/2)`. The sphere constant cancels: `a0 = s/n`, `κ = 1/n` for every d (verified for d = 2,3,4). With `n = rank(d) = 2` for all `d ≥ 2` (B3/B4), κ = 1/2 is **dimension-stable** under dimensional continuation; the d = 1 sector carries no channel (rank 0) and the count machinery does not apply there (domain boundary, no repair claimed).
- **NC4 — Newtonian boundary case `Φ = Ψ`:** `G_kk = (d−1)(3−d)ΔΦ`: d=3 → 0 (Newtonian regime loads only the 00 channel — the decoupling again); d=2 → `+ΔΦ`; d=4 → `−3ΔΦ` (sign flip for d > 3). Exact identity (distinguished from finite consistency by the C1 symbolic residuals).
- **B5 — normalization/boundary case:** `μ_n'(0) = n` for symbolic `n ≥ 1` (the MU_n slope–count link used by the CORE-coefficient chain).

---

## 5. Footings — both a0 values, carried separately

The result is **dimensionless** (det, rank, decoupling are pure coefficient statements), so it is proved once and applies to both footings unchanged; the contract's separate-carry requirement is discharged by these numbers (computed with `G = 6.67430e−11`, `c = 299792458`):

- **Canonical:** `a0 = 9.3619e−11 m/s²` with κ = 1/2 **adopted** ⇒ `s = 2a0 = 1.87238e−10 m/s²`, `ρ_Λ = 4a0²/(Gc²) = 5.8444e−27 kg/m³` (framework identity).
- **Alternative:** `a0 = 1.1279e−10 m/s²` — two readings, never sharing both fixed density and fixed κ:
  (i) fixed `ρ_Λ`: `κ_eff = a0/s = 0.60239`, `n_eff = 1/κ_eff = 1.66006` — **not** a channel count (consistent with the alternative being a normalization, not new physics);
  (ii) fixed κ = 1/2: `ρ_Λ' = 8.4831e−27 kg/m³ = 1.45149 × ρ_Λ^canonical`.
- Under either footing, `n = 2` (the static channel rank at d ≥ 2) is unchanged: the rank statement is footing-immune; only `s` carries the footing.

---

## 6. Strongest surviving statement, branch discipline, closure implication

**Theorem T (this run).** *For the static diagonal two-potential metric perturbation of d-dimensional flat space, the linearized Einstein channels are `G₀₀ = (d−1)ΔΨ` and `G_kk = (d−1)Δ(Φ−Ψ) + (d−1)(3−d)ΔΨ`; the channel map has determinant `(d−1)²`, full rank 2 for every `d ≥ 2`, rank 0 at `d = 1`; and `d = 3` is the unique decoupling point where the map diagonalizes into the pure operators `2ΔΨ` and `2Δ(Φ−Ψ)` (PD01 B1). The deep-MOND transfer `κ = 1/n` with `n` = channel count holds in every `d ≥ 2` (sphere constant cancels).* Domain: weak-field static diagonal sector, real `d ≥ 1`; exactness: polynomial identities in `d`, verified at integers 1..5 by an independent Christoffel representation, at non-integers `d ∈ {3/2, 2, 3}` by the λ-probe, and numerically at machine precision on grids in d = 2, 3, 4.

**Branch discipline:** conclusions are stated in the task's declared branch (CORE coefficient; conditional MU_n statistical response — the MU_n family with symbolic `n ≥ 1`, adopted member MU2). No Q/RAR/EXP/MONO equation is asserted or transferred; the PUER filters and criterion B of the operative target are not touched by this result.

**Closure implication (gate A03 / kappa-derivation carrier premise).** PD01/PD08's "count = 2" premise acquires its dimension-dependence certificate: the count is `rank N(d) = 2` for all `d ≥ 2` — the OR machinery and `κ = 1/n = 1/2` (with κ = 1/2 still *adopted* as input, per contract) are stable under dimensional continuation; `d = 1` is the unique degeneracy (no static channel at all), which is a domain boundary, not a counterexample to the framework. Common-action compatibility: the statement is carrier-algebra (linearized Einstein operator content of the two Potentials), i.e., parameter-cell independent; it does not depend on the kernel/filter/gate cell of the operative filtered-MONO action.

**Next unresolved implication (first bridge to the full theory):** the *branch-translation lemma* — a proof that the operative filtered-MONO action's static sector reduces, in the admitted galactic domain, to the diagonal two-potential ansatz on which this rank theorem lives (itself the same unproved prerequisite that PD01's B1 leaves open). Until that map is proved, the rank theorem governs the linearized-geometry sector only. Secondary open point (recorded, not load-bearing here): the physical meaning (if any) of the `(3−d)` sign flip for d > 3.

---

## 7. Lean 4 certificate

`AS057_static_channel_rank.lean` (in this run dir) certifies the algebraic core of steps 2 and 4: `det2` (det = (d−1)²), `det_sq_zero_iff` (rank collapse iff d = 1), `inv_iff` (invertible iff d ≠ 1), `rank_stable` (d ≥ 2 ⇒ d−1 ≠ 0), `decouples_iff` (d=3 decoupling iff d ∈ {1,3}), `coeff_identity` (the claim-form ↔ direct-form coefficient identity), `det_integers` (det = 0,1,4,9 at d = 1..4), `d3_diagonal`.

- Compile: `cd fable_independent_2026/lean_2026 && lake env lean <abs path>/AS057_static_channel_rank.lean` → **exit 0, no warnings**. (Compile host untouched; the certificate lives only in the run dir.)
- Axioms (unfiltered `#print axioms`, `AS057_lean.out`): every theorem depends on a subset of `{propext, Classical.choice, Quot.sound}` — e.g. `det2` → `[propext, Classical.choice, Quot.sound]`, `det_integers` → `[propext]`. Zero `sorry` (the file's only occurrence of the word is the comment declaring the zero-sorry bar; no `sorryAx` in any axiom print).

---

## 8. Tested domain, bounds, limitations, failed attempts

- **Tested domain:** symbolic `d > 0` (polynomial identities); exact concrete computations d = 1..5; diagnostic non-integer points d = 3/2 (and d = 2, 3); numeric grids (121², 41³, 17⁴) at d = 2, 3, 4 with Gaussian test fields, central differences; deep limit d = 2, 3, 4; Newtonian boundary at d = 2, 3, 4.
- **Bounds actually enforced (recorded):** wall 1.2 s (prototype bound ≤ 120 s ✓), peak RSS 171.6 MB (bound ≤ 512 MB ✓), 1 thread (`OPENBLAS/MKL/OMP/NUMEXPR_NUM_THREADS=1`; numpy single-threaded gradient calls) ✓.
- **Limitations (what this does NOT establish):** (1) the OR-identification premise (PD01/PD08) is inherited, not re-derived; kappa = 1/2 remains an *adopted* input per framework contract; (2) the branch-translation to the operative filtered-MONO action is unproved (listed as the next implication); (3) no claim about Q/RAR/EXP/MONO response shapes, causality, or the radiative sector; (4) d = 1 has no realized astrophysical sector — the collapse is recorded as a mathematical boundary; (5) finite grids are consistency checks — the exact content is the symbolic/Lean identity.
- **Failed attempts (preserved, diagnosed):** (i) first Christoffel implementation used the exact inverse metric with `∂Γ−∂Γ` (inconsistent truncation ⇒ residual full of `O(h²)` terms; fixed to the first-order connection); (ii) the Ricci second contraction dropped the `ρ=0` term `Γ⁰_{i0} = ∂ᵢΦ`; fixed in both the symbolic and numeric routes; (iii) `sp.symbols("x1:N")` returns a tuple (concatenation bug, fixed). All three are visible in the edit history of `AS057_derive.py`; the first run (156.0 s) also exceeded the wall bound and triggered the optimization to `η`-inverse + positive coordinates (1.2 s final). The failed run's output was overwritten by design of the rerun; the final log records the corrected pipeline.

## 9. Reproducibility

```
cd deepseek_push/astra_spawn_ideas/results/AS057/AS057-r1-20260928T080406Z-dsv4f-hermes
python3 AS057_derive.py        # -> AS057_raw.out, AS057_checks.json (26/26 PASS)
cd fable_independent_2026/lean_2026 && lake env lean <abs>/AS057_static_channel_rank.lean
```
All input and artifact hashes: `result.json` (`input_sha256`, `artifacts_sha256`).