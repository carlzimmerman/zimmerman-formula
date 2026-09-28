# AS075 — Constructive missing-premise work order for kappa

**Run**: `AS075-r1-20260928T121520Z-dsv4f-hermes` · **Worker**: deepseek/deepseek-v4-flash-0731 (OpenRouter) via Hermes Agent subagent · **Task SHA-256**: `e0b8978d3738dc5d8af138508109d320fe01f540ff495d30a4772f6987e1b19b` (verified at start, matches the dispatched value) · **Started**: 2026-09-28T12:15:20Z · **Seed**: A03, P1, audit · **Branch**: CORE coefficient; conditional MU_n statistical response · **Prerequisites**: AS059, AS067, AS072.

The seed asks for a *constructive* work order on the missing premise behind a derivation of kappa: "A derivation of kappa must remove a genuinely independent freedom. A channel count, algebraic identity or adopted normalization is useful only with its physical identification separately justified." Mathematically: "Required mechanism must fix both a physical normalization `b` and a vacuum datum relation without a free additive shift." The result below is the execution of that work order: a two-obligation decomposition theorem (T2O), the constraint-rank audit of every candidate mechanism the class offers, both negative controls, the diagnostic counterexamples at λ ∈ {1/2, 1, 2}, and the precise statement of the single missing premise as a ready child specification.

---

## 1. Statement, symbol dictionary, boundary conditions, assumptions

### 1.1 Symbol dictionary (all SI unless stated; c = 1 only where marked)

| Symbol | Meaning | Units | Status |
|---|---|---|---|
| `G_N` | Newton coupling, measured | m³ kg⁻¹ s⁻² | input (6.67430e-11); `G_bare`, `G_cosmo` separate symbols, never identified (framework rule) |
| `c` | speed of light | m/s | input (299792458, exact) |
| `s` | vacuum rate `s = c·sqrt(G_N·ρ_Λ)` | m/s² | framework unit |
| `a0` | MOND scale, `a0 = κ·s` | m/s² | framework relation |
| `κ` | coefficient, κ = a0/s — **1/2 ADOPTED INPUT** | — | adopted, never claimed derived here |
| `ρ_Λ` | vacuum mass density, `4 a0²/(G_N c²)` | kg/m³ | framework relation (footings below) |
| `Y` | `g/s`, g = |∇Φ| | — | argument |
| `μ_n(Y)` | response `1 − (1+Y)^(−n)`, symbolic `n ≥ 1` | — | conditional MU_n branch |
| `J(Y)` | kinetic primitive, `J′ = μ` | (s²) | k01/PD08 statics conventions |
| `j` | vacuum datum `J(0)/s²` | — | **the zero mode** |
| `b` | deep normalization `μ′(0)` (sum of OR-channel slopes) | — | **the normalization slot** |
| `K_B` | `α = 2 − K_B`, K_B ∈ [0, 1/4] | — | k01 coupling band |
| `Λ_eff` | `Λ + α·J(0)/2 + K(Q0)/2` (FLRW background) | m⁻² (c=1) | k01 K2 |
| `ρ_vac` | `α s² J(0)/(16π G_N)` | kg/m³ | pinned sign convention (k01 K3/AS067/AS068) |
| `R` | `ρ_vac/ρ_Λ` | — | vacuum ratio |

### 1.2 Framework inputs (declared, not conclusions)

(a) `a0 = κ c sqrt(G_N ρ_Λ)` with `κ = 1/2` adopted; (b) `s = 2 a0` on both footings; (c) the density identity `ρ_Λ = 4 a0²/(G_N c²)`; (d) `r_M = sqrt(G_N M_b/a0)`, `v_flat⁴ = G_N M_b a0` (used only as check relations); (e) response family `μ_n` with the L230 normalization `μ_n(0) = 0`, `μ_n(∞) = 1`; (f) the general static action class (AS059: `E[Φ] = A s² ∫K(|∇Φ|/s)dV + B∫ρΦ dV`, `B = 8π A G_N` identification, `μ = K′/(2Y)`); (g) coupling band K_B ∈ [0, 1/4]; (h) pinned sources PD01, PD08, k01 at the SOURCE_MANIFEST hashes (verified); (i) both registered footings carried separately.

### 1.3 Boundary conditions and domain

Physical domain `Y ≥ 0`. The boundary objects under audit: the static two-potential sector (reduced 1-D Lagrangian `L_red`, below), the FLRW background (Y = 0, Q = Q0), the boundary-fixed primitive `J(Y_ref) = 0` at finite positive references (the AS068 family, re-derived here as a work-order diagnostic), and the deep/Newtonian regimes `Y → 0` / `Y → ∞`.

### 1.4 Conclusions to be established (not inputs)

(1) the decomposition: exactly which independent freedoms a mechanism must remove for κ to be a *derived* output; (2) the rank of every candidate mechanism the audited class offers; (3) the status of each seed control; (4) the statement of the missing premise with its acceptance properties.

---

## 2. The two-obligation theorem (T2O)

**Setting.** The pinned action class A_τ: k01 g03t / PD08 one-scalar, reduced static sector
`L_red = −2Ψ′² + 2αΨ′φ′ − αJ(φ′²) − ρ(Ψ + φ)`, response `J′ = μ_n`, scale `s`, with the deep-matching identity (exact inside the class, AS059 re-derived here, check A3):

```
(1/r²)·d/dr [r² · b·(g/s) · g] = 4π G_N ρ   ⇒   2·b·g²r²/s = 4πG_N M ... (Gauss integrals)
 ⇒  g² = (s/b) g_N   ⇒   a0 = s/b   ⇒   κ = 1/b                [DEEP MATCHING]
```

**Theorem T2O.** A mechanism M derives κ = 1/2 as an output of A_τ (i.e., `a0 = (c/2) sqrt(G_N ρ_Λ)` becomes a consequence, not an input) **iff** M supplies exactly two independent premises:

- **Obligation A (physical normalization b):** an argument fixing `b = 2` with physical identification — the static carrier's channel count = 2 (PD01: two independent Poisson channels of the linearized metric), the unit-slope fraction identity `p′(0) = 1` in the single-scale action (AS072 A1–A5 load-bearing audit), and the measured source coupling `B = 8π A G_N` (AS072 A4). Observable that would establish it: the deep slope `μ′(0) = n` in dark-energy units (zero point, PD01 C1 — measurement-consistency, not a proof: the seed forbids observational preference as proof).
- **Obligation B (vacuum datum relation, shift-free):** an equation `E*(j) = 0` with all four properties:
  - (B-i) **shift-breaking**: the constraint row pairs non-trivially with the zero-mode null direction (∂E*/∂C ≠ 0 under J → J + C; the plain shift is a Λ-gauge freedom, checks A1–A2);
  - (B-ii) **no new adopted datum**: the equation introduces no free parameter of its own (unlike the boundary family's reference Y_ref, B2);
  - (B-iii) **positive vacuum**: `ρ_vac(j₀) = +ρ_Λ` at `j₀ = 64πκ²/((2−K_B)c²)` (κ = 1/2 footing);
  - (B-iv) **rank-1 into the target**: the augmented constraint system's κ-projection collapses to a point (the relabelled candidate fails this, C2–C3).

**Checked content (this run).** (1) *Independence:* fixing A leaves j a continuous 1-parameter family (B1); fixing B (any boundary reference) leaves b free (B2) — the constraint Jacobian is block-diagonal in (b, j). (2) *Necessity:* A alone pins κ = 1/2 but leaves ρ_vac arbitrary (any sign, any magnitude — AS067 D4–D6, summarized); B alone (boundary family) fixes j per the *adopted* reference and leaves κ = 1/b free over (0, ∞) at every diagnostic λ (B2). (3) *Joint sufficiency:* {κ = 1/b, b = 2} lands κ = 1/2 exactly (B3); the endpoint `a0 = (c/2)sqrt(G_N ρ_Λ)` then follows from the density identity at κ = 1/2 (B3). (4) *Deficit count:* unknowns (b, j, κ) = 3 real DOF; the class provides the deep matching (1 relation) and nothing for j (A1/A2: statics see only J′, Λ_eff rank 1); every candidate below adds ≤ 1 relation but ≥ 1 new datum or is rank-redundant — **the missing premise is exactly one independent real equation E*** with (B-i)–(B-iv).

*Why the current action cannot supply E*** (seed step 2, second part): the EL equations contain J only through J′ (A1, exact), so no equation of A_τ fixes J(0); the background sees only the rank-1 combination Λ_eff (A2), so J(0) is a gauge direction against Λ; the κ-coordinate enters no equation except the matching and the adopted footing. This is AS067's no-go, re-derived here as the raw material of the work order (A1, A1b, A2).

---

## 3. Intermediate algebra (all factors, signs, units)

**(a) Deep matching (obligation A's slot).** For a point mass, `div(μ∇Φ) = 4πG_Nρ` with `μ ~ b·g/s`:

```
(1/r²) d/dr [r² b (g/s) g] = 0            (outside the source)
⇒  b g² r² / s = G_N M                    (integration constant from the Gauss flux)
⇒  g² = (s/b) (G_N M/r²) = (s/b) g_N      ⇒  a0 := s/b,  κ = 1/b      [checks A3, A4]
```
Units: `[b g² r² / s] = (m/s²)²·m²/(m/s²) = m³/s² = [G_N M]` ✓. Slope sum: `μ = 1−(1−p₁)(1−p₂)`, `p_i = b_i Y + c_i Y²` ⇒ `μ′(0) = b₁ + b₂` (check A4; the completion's c_i drop out).

**(b) The vacuum datum and its boundary-fixing (obligation B's slot).** `J′ = μ_2`, boundary `J(λ) = 0`:

```
J(λ) − J(0) = ∫₀^λ μ_2(Y) dY = ∫₀^λ [1 − (1+Y)⁻²] dY = [Y + (1+Y)⁻¹]₀^λ = λ²/(1+λ)
⇒  j(λ) = J(0)/s² = −λ²/(1+λ)            (n = 2; exact rationals −1/6, −1/2, −4/3 at λ = 1/2, 1, 2)
```
General n ≥ 1 (checks B5): `j(n,λ) = −[λ + (1 − (1+λ)^{1−n})/(1−n)]` (n ≠ 1), `−[λ − ln(1+λ)]` (n = 1). Sign: `μ_n > 0` on (0, ∞) forces `j(n,λ) < 0` for all n ≥ 1, λ > 0 (B5; boundary_j_neg, Lean). Vacuum ratio in the pinned convention:

```
R(λ) = ρ_vac/ρ_Λ = α s² j/(16π G_N) · G_N c²/(4 a0²) = −α c² λ²/(16π(1+λ))   (κ = 1/2)
R: (−5.960055e14, −1.788017e15, −4.768044e15) at K_B = 0; ×0.875 at K_B = 1/4   [check B4]
```
Sign and magnitude dependence: R < 0 for every finite positive reference; pairwise distinct at the diagnostics (B4; diag_vacua_distinct, Lean).

**(c) The re-labelled candidate (negative control 1).** Present "ρ_vac = ρ_Λ" as E*:

```
α s² j/(16π G_N) = ρ_Λ = 4κ²s²/(G_N c²)   ⇒   j(κ) = 64πκ²/((2−K_B)c²)   (c = 1: j = Aκ², A = 64π/α)
```
This is an **identity of the definitions** (C2: substitution residual ≡ 0 symbolically): the relation's solution set is the graph `{(κ, Aκ²): κ > 0}` — a bijection (0, ∞) → (0, ∞) (Lean: relabel_strict_mono/injective/surjective). Its κ-projection is ALL of (0, ∞): κ ∈ {1/2, 1, 2, 5/2, 4} all admit distinct data (C3, E3: j = 25.13/100.53/402.12/628.32/1608.50 at A = 32π). Rank accounting: the candidate row is the *definition* of the vacuum datum in terms of the adopted κ — rank increase against the κ-coordinate = 0. **Rejected by constraint rank** (C3 fires; capable-of-failing: a genuine E* would cut the projection to a point — the sampled κ's would not all satisfy it).

**(d) The Λ_eff degeneracy (why the shift is a gauge freedom).** FLRW minisuperspace at Y = 0, Q = Q0: `Λ_eff = Λ + αJ(0)/2 + K(Q0)/2`; the map (Λ, J(0), K(Q0)) → Λ_eff has Jacobian rank 1 (d/dΛ = 1, d/dJ0 = α/2, d/dK0 = 1/2; two null directions — check A2). Compensating `Λ → Λ − λ·α·C/2` for `J → J + λ·C` leaves every observable of the class invariant (AS067 certified; the reduced statics re-derived here: A1, plus tightness A1b: nonconstant shifts `w(Y) = Y` change the EL equations by `λ·Cw·(K_B−2)·φ″ ≠ 0`).

---

## 4. Independent checks (different representations; actual residuals)

| Check | Representation | Residual | Threshold (pre-set) |
|---|---|---|---|
| E1 | FTC form of (b): d/dλ[−λ²/(1+λ)] + μ₂(λ) @ λ ∈ {1/2,1,2}, mpmath dps=60 | 0.0 (double-zero at printed precision) | < 1e-55 ✓ (Lean: removal_deriv_identity, exact) |
| E4 | quadrature `−∫₀^λ μ₂ dY` vs closed form, dps = 60 | 0.0 | < 1e-55 ✓ |
| E2 | chain-rule gradient of the **discretized** action (201-node lattice) under J0 = 0 → 137: shift invariance + central-FD cross-check | shift: 0.0; FD-vs-exact: 1.567e-06 | < 1e-12 / < 1e-5 ✓ |
| D1b | implicit deep equation Y·μ₂(Y) = q solved at q ∈ {1e-4, 1e-8, 1e-12}, dps = 60 | 1.9e-59, 2.0e-57, 1.6e-61 | < 1e-50 ✓ |
| D2 | Newtonian deficit g/g_N − 1 @ q = 1e2, 1e6 vs leading term 1/q² − 2/q³ (corpus) | 9.8020187e-5 (/9.8e-5), 9.99998e-13 (/1e-12) | |Δ| < 1e-7 / 1e-15 ✓ |
| E3 | candidate satisfied at κ ∈ {1/2,1,2,5/2,4}, dps = 60 | 0.0 at all five | < 1e-55 ✓ |

Exact-identity vs finite-consistency is kept throughout: A1, A1b, A2, A3, A4, B1–B5, C2 are **symbolic identities**; D1b, D2, E3, E4 are **finite-precision solves with measured residuals** (the a0-line is an asymptote, not an exact identity: leading neglected term O(g/s) with completion coefficient, D1/D2).

## 5. Negative controls (both capable of failing)

1. **Re-labelled input rejected by constraint rank** (Part C): the vacuum-datum relation ρ_vac = ρ_Λ promoted to an independent premise is an identity of the definitions — its solution set is a graph over κ; the κ-projection stays all of (0, ∞) (C2, C3); jointly with obligation A it adds nothing (C4: κ = 1/2 comes from the *adopted* b = 2). The control *fires* (rejects); it was capable of failing — a genuinely independent E* would have collapsed the projection.
2. **Limiting regimes** (Part D): the deep regime (q → 0) fixes only μ′(0) = b (D1/D1b); the Newtonian regime (q → ∞) fixes only μ(∞) = 1 with the measured 1/q² deficit shape (D2); J(0) appears in **no** limit expression (D3, symbolic; j-absence in the whole matching chain, A3) — the regimes cannot fix the additive datum, in accordance with an *exact-identity* boundary check (μ₂(1) = 3/4 exactly, D3).

## 6. Diagnostic counterexamples at λ ∈ {1/2, 1, 2} (all three readings)

| Reading of λ | Family | Outcome at λ = 1/2, 1, 2 | Deficit it exhibits |
|---|---|---|---|
| engagement slope (AS072 D4) | p_λ = λY/(1+λY) ⇒ μ′(0) = 2λ ⇒ κ = 1/(2λ) | κ = 1, 1/2, 1/4 **distinct** (B2 table; slope_family_diagnostics, Lean) | normalization freedom continuous: only λ = 1 (fraction identity) lands on 1/2 |
| boundary reference (AS068) | j = −λ²/(1+λ) ⇒ R = −αc²λ²/(16π(1+λ)) | j = −1/6, −1/2, −4/3; R = −5.96e14, −1.789e15, −4.768e15 (K_B=0) **all negative, pairwise distinct** (B4; diag_vacua_distinct, Lean) | vacuum sign obstruction reference-independent; κ still free (B2) |
| zero-mode shift coefficient (AS067) | J → J + λ·C | EL equations unchanged at all three λ (A1); nonconstant w(Y)=Y changes them (A1b) | invariant subspace = exactly the constants: no absolute datum inside the class |

Under every reading the deficit is the same **one real DOF** — the work order's conclusion is reference-independent (B-anchor: boundary_family_kappa_free + diag_vacua_distinct, Lean).

## 7. Footings, units, couplings

| Footing | a0 [m/s²] | s = 2a0 [m/s²] | ρ_Λ [kg/m³] | κ at that ρ_Λ | fixed-density relabel |
|---|---|---|---|---|---|
| canonical | 9.3619e-11 | 1.872380e-10 | 5.844412454e-27 | 1/2 (by construction) | κ_eff(alt ρ @ can s) = 0.602388404 ≠ 1/2 |
| alternative | 1.1279e-10 | 2.255800e-10 | 8.483089620e-27 | 1/2 (by construction) | — |

Both carried separately; never both fixed density and fixed κ (F1). All j- and R-statements are dimensionless (F2); only G_N enters (F3). Task and source hashes verified at start (F3; input_sha256 in result.json).

## 8. Bounds (declared and enforced)

Declared: ≤ 120 s wall, ≤ 512 MB, 1 thread, single bounded prototype. Enforced: `ulimit -t 120` CPU cap on the python process; thread env (`OPENBLAS/OMP/MKL/VECLIB/NUMEXPR_NUM_THREADS = 1`), single process; measured **wall 0.19 s, max RSS 84.3 MiB** (getrusage; RLIMIT_AS is not enforceable on macOS — kernel refuses finite RLIMIT_AS — same convention as AS067/AS068/AS072). Final run: 26/26 checks PASS, exit 0.

## 9. Strongest surviving statement

**T2O + rank audit (scoped claim).** In the pinned action class A_τ with the conditional MU_n response (n ≥ 1 symbolic; n = 2 operative), κ = a0/s is a *derived* output **iff** two independent premises are supplied: obligation A (b = 2, the physical normalization: channel count + unit-slope identification + measured coupling ⇒ κ = 1/b = 1/2) **and** obligation B (a shift-free vacuum datum equation E*(j) = 0 with the four properties (B-i)–(B-iv), in particular a positive vacuum ρ_vac(j₀) = ρ_Λ at j₀ = 64πκ²/((2−K_B)c²)). The class itself supplies no E*: statics are J′-only (A1), the background degeneracy is rank 1 (A2), the boundary family fails sign and relocates the freedom (B2–B4), the relabelled input is rejected by constraint rank (C2–C3), and both limiting regimes act on J′ only (D1–D3). κ = 1/2 **remains adopted input**; the missing premise is exactly one independent real equation E*.

## 10. Next unresolved implication (first bridge)

For each candidate E* (or a no-go): exhibit an equation with (B-i) shift-breaking, (B-ii) no new datum, (B-iii) ρ_vac(j₀) = +ρ_Λ at the adopted footing, (B-iv) rank-1 κ-selection — or prove no such equation exists in the extended action class (k02 sequestering, k04 four-form, K(Q0)-coupling, MONO/phantom continuation with the h′_mono kernel). The MONO-branch transfer of the boundary analysis (h′_mono > 0 ⇒ J(0) < 0 for the same primitive argument) is a registered open step (AS068.C01 lineage) but is NOT the constructive target: the constructive target is any positive-vacuum E*, of which the audited class has none. Child **AS075.C01** (spec written, not dispatched — no spawn mechanism in this worker): "positive shift-free vacuum datum: search the extended coefficient space, or extend the no-go" — fingerprint, dependencies, controls and acceptance criteria in `deepseek_push/astra_spawn_ideas/branches/AS075/AS075.C01.md`.

## 11. Limitations

Does not derive κ = 1/2 (adopted; the work order shows what a derivation must still supply). Does not establish E* exists or not beyond the audited class (A_τ + boundary family + relabelled relations; the MONO kernel's primitive sign is not computed). No dynamics, no causality criterion-B statement, no transfer to the operative filtered-MONO target (Requirement 1) or any other gate beyond Requirement 13's derive-arm diagnosis (gate A03 cell, ORCHESTRATOR map: gate 13 stays OPEN; "preserved as input" is the honest label). The alternative footing's κ_eff = 0.602388404 is a relabel diagnostic, not a fit. Numerics at 1e-55…1e-61 relative are finite evidence; exactness rests on the symbolic identities and the Lean certificates (13 theorems, zero sorry, axioms ⊆ {propext, Classical.choice, Quot.sound}).

## 12. Lean certificate

`AS075_work_order_certificates.lean` (run dir), compiled with `lake env lean` on the compile host (no files written into fable_independent_2026/lean_2026): 13 theorems — removal_deriv_identity, boundary_family_kappa_free, obligB_alone_not_half, obligA_alone_j_free, relabel_strict_mono, relabel_injective, relabel_surjective, relabel_selects_nothing, relabel_diagnostics_distinct, slope_family_diagnostics, boundary_j_neg, diag_vacua_distinct, full_system_lands_half. Compile exit 0, zero `sorry`; unfiltered `#print axioms` for each = `[propext, Classical.choice, Quot.sound]` (lean_axioms.out).