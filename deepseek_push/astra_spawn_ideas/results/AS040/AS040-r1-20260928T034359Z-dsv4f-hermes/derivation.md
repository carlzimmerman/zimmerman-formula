# AS040 — AQUAL and QUMOND spherical correspondence

**Run:** `AS040-r1-20260928T034359Z-dsv4f-hermes`
**Worker:** deepseek/deepseek-v4-flash-0731 (provider: openrouter); Hermes Agent focused subagent; identity from the executing agent's own system context.
**Branches:** separate Q, RAR, MU2, historical EXP, operative MONO — each cell labelled; conclusions on the declared branch only; the operative target (filtered MONO, causality criterion B) is NOT concluded on (quantified bridge delivered instead).
**Task hash:** `99fa799f08e1c2862ef88b3587e861080bb58733cee60fa692b8d1273fab4317` (matches the SOURCE_MANIFEST pin).
**Sources:** README.md (`91a5fac4…`), FRIED_CHICKEN_SPEC.md (`98d9149f…`), peer_review_2026_09_26/README.md (`521d9ac3…`) — all hash-verified against SOURCE_MANIFEST.json pins; STANDING.md and the September-26 amendment block read (operative target = filtered `nu_mono`, criterion B); ORCHESTRATOR.md + FIRST_PRINCIPLES_AND_BRANCHING.md consulted.

---

## 1. Precise claim, symbol dictionary, premises

**Claim (dimensionless, exact).** Let `x = g/a0 ≥ 0`, `y = B/a0 > 0` with `B = g_bar = g_N`. The AQUAL relation

```
mu(x) * x = y                       (AQUAL:  div[mu(|grad Phi|/a0) grad Phi] = 4 pi G rho_b,  spherical)
```

and the QUMOND relation

```
x = nu(y) * y                       (QUMOND:  Delta Phi = 4 pi G rho_b + div[(nu(B/a0)-1) grad Phi_N])
```

state, on their declared spherical branch, that each side is the *algebraic inverse* of the other:

**Correspondence condition (Theorem A, Lean-certified):** if `y = x·mu(x)` and `x = y·nu(y)` with `x, y ≠ 0`, then `mu(x) · nu(y) = 1` — at matched arguments only. The same-argument product `mu(y)·nu(y)` is **not** 1 in general (negative control NC1: mismatch ≈ 1 deep).

**Exact domain of the correspondence:** `y ∈ (0, ∞)`, `x ∈ (0, ∞)`, *spherical statics*, and `w(x) := x·mu(x)` **strictly monotone increasing** so that the matched `nu(y) := x(y)/y` is single-valued (existence of one `x > 0` solving `x·mu(x) = y` for every `y > 0` requires monotonicity; see §6b for the failure mode).

**Breakage (three disjoint locations):**
- **(a) non-spherical sources** — at linear order in an ℓ=2 perturbation the two PDEs give different responses: `max |R_A − R_Q|/peak(R_Q) = 0.52…0.60` (Q/EXP/MU2/MONO cells; §6a);
- **(b) non-monotone `mu`** — if `x·mu(x)` is not strictly increasing, `y = x·mu(x)` is multi-valued and the correspondence is not a function (counterexample `mu_bad`, Lean-certified double-root; §6b);
- **(c) the operative heat filter** — `S = exp((xi²/2)Δ)` makes the field nonlocal; the point-mass force deviates from the algebraic core `nu(gN)gN` by **≤ 6.0% (ξ/r0 = 0.3), 0.75% (0.1), 0.08% (0.03)**, confined to `r ≈ (1–8)ξ` (§6c).

**Symbols / premises.** Framework inputs adopted (not derived): `a0 = kappa·c·sqrt(G·rho_Lambda)`, `kappa = 1/2`; `r_M = sqrt(G·M_b/a0)`; `v_flat⁴ = G·M_b·a0`; `G = 6.67430e-11`, `c = 299792458`, `M_sun = 1.98847e30`, `pc = 3.085677581491367e16` (SI). `G_N`, `G_bare`, `G_cosmo` kept separate symbols (not equated here). Both footings `a0_can = 9.3619e-11` and `a0_alt = 1.1279e-10 m/s²` carried separately (they never share both fixed ρ_Lambda and fixed kappa: ratio `a0_alt/a0_can = 1.2047768081`; fixed-ρ effective kappa `1.2047768081`; fixed-κ density ratio `1.4514871574`). The theorem is dimensionless — both footings apply unchanged; SI examples are quoted separately for each.

## 2. Dictionary and the lookup routine (work-order steps 2–3)

Each cell declares one member of the pair; the other is derived by inversion, and **both implicit equations are checked by a lookup routine** (`impl1: x·mu(x) − y`, `impl2: y·nu(y) − x` at the matched point), 50-digit mpmath arithmetic:

| cell | declared | derived (matched) | x(y) = y·ν(y) |
|---|---|---|---|
| Q | `mu_Q(x) = (sqrt(1+4x²)−1)/(2x)` | `nu_Q(y) = sqrt(1+1/y)` | `sqrt(y²+y)` (implicit-free) |
| RAR | `nu_RAR(y) = 1/(1−exp(−sqrt(y)))` (parametric pair `u = sqrt(y)`, `mu = 1−exp(−u)`) | both | `y·nu_RAR(y)` |
| MU2 | `mu2(x) = 1−(1+x/2)^(−2)` | `nu2` via bisection of `x·mu2(x) = y` | bisection |
| EXP | `mu_EXP(x) = 1−exp(−x)` | via bisection | bisection |
| MONO | `nu_mono(y) = 1 + h_mono(y)/y`, `h'_mono = max(h'_RAR, delta·h_p/(y+y_p))`, splice at `y* = 2.337412…`, `y_p = 2.539638…`, `h_p = 0.647610…`, `delta = 0.05` | `mu_mono(x)` via bisection of `y·nu_mono(y) = x` | `y·nu_mono(y)` |

Lookup result (181-pt grid `y = 10^k`, `k = −10..8 step 0.1`, mpmath 50 dps): **matched identity `mu(x(y))·nu(y) = 1` to `≤ 9.4e-51`** (Q 3.5e-42, RAR 1.8e-44, MU2 1.8e-45, EXP 3.4e-45, MONO 9.4e-51); both implicit equations hold to the same level. Inverters use **bracketed bisection** (explicit brackets, not grid proof): `x·mu(x) = y` bracketed in `[y, y + y√y + √y]` with expanding fallback; `y·nu(y) = x` bracketed in `[min(x²/2, x/2), x]` (deep `y ≈ x²` vs Newtonian `y ≈ x − h` hybrid) with expanding fallback.

**Geometry restriction:** the reduction `div[mu g] = 4πGρ → d[r²·mu(g)·g]/dr = 4πGρ·r²` is a *spherical-statics identity*: the unweighted 1D divergence `d[mu·g]/dr = 4πGρ` is **wrong** by the `(2/r)·mu·g` term (control NC3: residual 2.2e8 — the check can fail and does).

## 3. Intermediate algebra (scale factors, signs, units; work-order step 3)

**(i) The matched identity collapses to cancellation.** With `y = x·mu(x)`, `x = y·nu(y)`: substituting the second into the first gives `y = y·nu(y)·mu(x)`, and (y ≠ 0) `mu(x)·nu(y) = 1` exactly — *zero scale factors, zero signs*: the correspondence is a pure algebraic duality; the force equality `g = x·a0` then holds identically on both sides (a0 cancels: dimensionless).

**(ii) Q-cell instantiation** (exact, Lean-certified): `x_Q(y) = y·nu_Q(y) = sqrt(y²+y)`, then `mu_Q(x_Q(y)) = (sqrt(1+4(y²+y))−1)/(2 sqrt(y²+y)) = (2y+1−1)/(2 sqrt(y²+y)) = y/sqrt(y²+y)`, and `nu_Q(y)·mu_Q(x_Q(y)) = sqrt(1+1/y)·y/sqrt(y²+y) = y·sqrt((y+1)/y)/sqrt(y(y+1)) = 1` for all `y > 0` (sign: all factors positive; unit: dimensionless).

**(iii) Spherical PDE reduction (independent representation).** For a Plummer sphere (`G=M=b=1`, `a0=1` code units; dimensionless — the a0 footings enter only through the SI conversion): AQUAL spherical form `d[r²·mu(g)g]/dr = 4πρr²` with `mu(g)g = g_N` telescopes to `psi(r) := r²·g_N = M(<r)` and `dpsi/dr = 4πρr²` is an **analytic identity**; the QUMOND phantom cumulant `M_ph(<r) = [s²(nu−1)g_N]_0^r = r²(nu−1)g_N` (endpoint term 0 because deep-MOND `r²·h(y) ~ r^(5/2) → 0`) makes `g_Q = g_N + M_ph/r² = nu·g_N` **identically** — both PDE representations reduce to the same algebraic core (measured 1.9e-11, §4). Leading neglected terms: deep `nu−1 ~ 1/sqrt(y)`, so `r²(nu−1)g_N ~ r^(5/2)→0` (endpoint exact); Newtonian `nu−1 = h(y)/y ≤ h_p/y` (h_p = 0.647610… the RAR phantom peak; MONO log-continuation `h_mono = h_RAR(y*) + delta·h_p·ln[(y+y_p)/(y*+y_p)]` stays `≪ y`).

**(iv) Q-cell phantom mass diverges.** `r²(nu_Q−1)g_N → (a0/2)·r` (measured `r²(nu−1)g_N/r → 0.999` at r_max): the Q cell's phantom mass is not enclosed at any finite radius (log-divergence class) — a *cell-specific* property, distinct from the correspondence identity itself.

**(v) ℓ=2 breakage (non-spherical).** Linearize both PDEs on the Plummer background: AQUAL `L_A[R] := (1/r²)d[r²·C(r)R']/dr − 6D(r)R/r² = 4πρ₂`, with `C = d[x·mu(x)]/dx|_bg`, `D = mu(x_bg)`; QUMOND `L_1[R] = (1/r²)d[r²R']/dr − 6R/r² = 4πρ₂ + (S-term)`, where the phantom term `s_Q = 4πρ₂ + (1/r²)d[r²(nu−1)·δu_N']/dr − 6(nu−1)δu_N/r² + (nup·g_N·δu_N'/a0)`-type pieces (all signs explicit in code). Solved as a finite-volume BVP on `r ∈ [1e-3, 1e3]`, N = 512/256, for a compact ℓ=2 source bump `ρ₂ = ε·(8/(π r_c³))(1−(r/r_c)²)²`, `ε = 1e-3`, `r_c = 2` (compact support ⇒ finite multipole moments; a `r²·ρ₀` weighting would have a divergent quadrupole moment — rejected in a failed attempt). Result: `max|R_A−R_Q|/peak = 0.52–0.60`, mesh-stable at the 3% level (N512 vs N256), peak at `r ≈ 1.29b`.

**(vi) Filter breakage (operative MONO).** Filtered QUMOND: `g = g_N − (Sψ)'` where `∇²ψ = div[(nu(g̃_N/a0)−1)∇ũ]`, `g̃_N = Sg_N`, `S = exp((ξ²/2)Δ)` on the declared measure (heat kernel on ℝ³; the radial kernel `K̃(r,r') = (1/sqrt(2π))(1/(ξ·r·r'))(e^{−(r−r')²/2ξ²} − e^{−(r+r')²/2ξ²})`, quadrature with `r'²dr'` weight and `dr` normalization). For a unit point mass: `g̃_N = (1/r²)[erf(w) − (2/sqrt(π))·w·e^{−w²}]`, `w = r/(sqrt(2)ξ)`, evaluated stably at small r (the naive form cancels catastrophically; the mpmath branch is used for `w < 0.25`). The cumulative phantom theorem `ψ'(r) = h(ỹ(r))` holds; the deviation `|g_filt − nu(g_N)g_N|/(nu g_N)` is measured and confined (Table in §6c).

**(vii) Non-monotone counterexample.** `mu_bad(x) = x + x² − x³/2` ⇒ `w(x) := x·mu_bad(x) = x² + x³ − x⁴/2`, factorized derivative `w'(x) = x(2−x)(2x+1)` (exact; w'(1) = 3, w'(5/2) = −15/2), so `w` is strictly increasing on (0,2) and strictly decreasing on (2,∞): for every `y0 ∈ (0, 4)` there are **two** positive roots of `w(x) = y0` — e.g. y0 = 3/2: x ∈ {1.0, 2.5987…} (Lean-certified IVT double-root; algebraic landmarks `w(1) = 3/2 < w(2) = 4 > w(25/10) = 75/32` certified).

## 4. Independent checks (work-order step 4; actual residuals)

| check | representation | observed residual |
|---|---|---|
| matched identity (all 5 cells) | algebraic inversion, different arguments | ≤ 9.35e-51 (50 dps roundoff) |
| spherical AQUAL↔QUMOND | telescoped phantom cumulant vs algebraic core | **1.92e-11** (rel) |
| same, FD-path (discretization envelope) | gradient-based phantom density vs telescoped | 1.11e-4 |
| 3D reduction identity `d[r²g_N]/dr = 4πρr²` | analytic identity via FD | 1.46e-3 (N512), 5.88e-3 (N256): ratio ≈ 4.0 ⇒ 2nd-order FD |
| Q cell forward law `x·mu(x) = y` | closed form | 3.49e-42 |
| ℓ=2 Newtonian control (mu = nu = 1) | both PDEs must coincide | 0.0 (identical solves; solver consistency) |
| ξ = 0 filter control (S = I ⇒ g = nu·gN) | exact telescoped identity | **3.15e-16** |

## 5. Negative controls that can fail (work-order step 5)

- **NC1 same-argument product:** `mu(y)·nu(y) − 1` at the *same* numerical argument ≠ 0 — measured `max |…| = 0.99999` over the grid for all five cells (deep: `mu(y)·nu(y) ≈ sqrt(y) → 0`): the correspondence holds at matched arguments **only**. RAR is degenerate by construction (parametric pair with the same u); its discriminating variant `mu_RAR(x)·nu_RAR(x)` at one *AQUAL* argument gives `−0.1923` (≠ 0).
- **NC1b–NC6 monotonicity:** `d[x·mu(x)]/dx` on the grid: min = 6.32e-5 > 0 for all five cells (deep slope 1 ⇒ min at the smallest grid x, equal across cells — correct shared deep limit).
- **NC3 wrong reduction:** 1D `d[mu·g]/dr = 4πρ` residual **2.2e8** — the check fails as designed (the 2/r term is not optional).
- **NC3c must-cancel:** both PDE representations agree (1.9e-11), so a naive "AQUAL vs QUMOND differ" claim is *rejected* in spherical statics.
- **NC4 non-spherical control:** with `mu = nu = 1` the ℓ=2 solves are identical (0.0); with kernels ≠ 1 the difference is 0.52–0.60 (≫ 0) — the breakage is kernel-driven, not a solver artifact.
- **NC5 filter ξ→0:** `S = I` returns the algebraic core to 3.15e-16.

## 6. Strongest surviving statements

**S1 (spherical correspondence — exact).** On the declared spherical-static domain `y ∈ (0,∞)`, for any cell whose `w(x) = x·mu(x)` is strictly increasing, the QUMOND interpolant `nu(y) = x(y)/y` and the AQUAL response `mu(x)` satisfy `mu(y·nu(y))·nu(y) = 1` exactly, `x(y) = y·nu(y)` is the unique solution of `x·mu(x) = y`, and both field equations produce the same force (measured 1.9e-11). Multivariate/multi-argument use of μ or ν without the matched argument is forbidden by NC1.

**S2 (monotonicity is the domain).** For each of Q (closed form), RAR, MU2, EXP, MONO: `d[x·mu(x)]/dx > 0` on the tested grid (181 points, y ∈ [1e-10, 1e8], x matched) — the correspondence domain is the strict-monotonicity domain. For a NON-monotone μ (explicit counterexample, Lean-certified), the correspondence fails as a function: two distinct forces-produce-the-same-y.

**S3 (non-spherical breakage, quantified).** At linear order about spherical equilibrium, AQUAL and QUMOND responses to the same ℓ=2 density differ by **52–60% of the peak response** (Q 0.581, EXP 0.583, MU2 0.549, MONO 0.525 at N512), so the spherical correspondence does **not** extend to aspherical sources by any pointwise algebraic rule — the PDE structure (one Poisson solve vs the phantom-source solve) is the carrier of the difference. This is the quantitative input for AS041.

**S4 (operative-filter deviation band).** For the operative MONO branch through the heat filter (point mass, r0 = sqrt(GM/a0) = 1):

| ξ/r0 | max \|g_filt − nu(gN)gN\|/(nu gN) | location | μ_impl vs μ_mono (max abs) |
|---|---|---|---|
| 0.3 | **0.0602** | r = 2.46ξ | 0.0619 |
| 0.1 | **0.0075** | r = 7.35ξ | 0.0075 |
| 0.03 | **0.0008** | r = 2.46ξ | 0.0008 |

Profile (ξ/r0 = 0.3): 3.3e-5 (0.2ξ) → 1.3% (0.5ξ) → 3.3% (1ξ) → 5.8% (3ξ) → 1.0% (10ξ) → 0.17% (30ξ): the deviation is *confined* to r ≈ (1–8)ξ and vanishes both into the core (r ≪ ξ: g̃_N → 0, the phantom force → h(ỹ) → 0 relative to g_N) and far outside (filter inert). The correspondence itself (the algebraic pair identity) is untouched; what the filter breaks is the *pointwise* character of the operative force law, at the ≤ 6% level for ξ/r0 ≤ 0.3.

**S5 (knee / footings).** r_M(1e9 M_sun) = 1.2202 kpc (canonical) / 1.1117 kpc (alt); r_M(1e11) = 12.202 / 11.117 kpc; v_flat = 59.37 / 62.20 km/s (1e9) and 187.75 / 196.70 km/s (1e11). Knee (y = 1, x = sqrt(2)) as in AS026.

## 7. Lean 4 certificate

`AS040_aqual_qumond_correspondence.lean` (in the run dir), verified with `cd fable_independent_2026/lean_2026 && lake env lean <abs path>` (exit 0). Six theorems, axiom audit via the `_axioms.lean` twin: **all depend only on [propext, Classical.choice, Quot.sound], zero `sorry`**:
- `generic_correspondence` — the correspondence condition (A);
- `xQ_eq_sqrt`, `q_pair_forward`, `q_correspondence` — Q-cell pair law and identity for all y > 0 (C, B);
- `wBad_nonmonotone` — w(1) < w(2) > w(5/2) (D, algebraic);
- `two_roots` — for every y0 ∈ (0,4) two distinct positive roots of w(x) = y0 via IVT (E).

(An earlier attempt to certify the derivative factorization `w' = x(2−x)(2x+1)` through the HasDerivAt API was abandoned after API friction; the derivative values w'(1) = 3 and w'(5/2) = −15/2 are instead carried numerically with the exact factorization stated in derivation §3(vii) — the algebraic non-monotonicity statements are fully certified.)

## 8. Framework cell and transfer

- **Action:** none varied (static algebraic/elliptic analysis only; no Lagrangian or coupling manipulation).
- **Kernel:** the five declared cells, separate; the correspondence is proved for the pair (mu, nu) generically and instantiated on Q exactly; RAR/MU2/EXP/MONO matched by bracketed bisection (50 dps).
- **Filter:** heat `S = exp((ξ²/2)Δ)` on ℝ³ (radial kernel as stated), exercised on the operative MONO branch (S4); self-adjointness per measure is the declared contract's domain question — here the Euclidean measure is used, as specified for the point-mass probe.
- **Gate:** A02 constitutive kernels and branch fidelity. Criterion B (causality) **not exercised** (statics only); the operative target (filtered MONO, criterion B) receives the quantified deviation band S4, not a pass.
- **Coupling:** single Newtonian G for the Plummer/point-mass probes; `G_N/G_bare/G_cosmo` separate symbols — no identity in this task requires their ratio.
- **Parameters:** kappa = 1/2 adopted; both a0 footings carried (all quoted dimensionless statements footing-independent).
- **Boundaries/initial conditions:** static, no initial data; y ∈ (0,∞), x ∈ (0,∞), ℓ=2 solution space with regularity at 0 and decay at ∞ (BVP), filter probe r ∈ [0.02ξ, 500ξ].
- **Units:** SI (m/s², kg, m, kg/m³) for the dimensional examples; the theorems are dimensionless.

## 9. Limitations

1. **No operative-target pass:** criterion B (causality) and the full filtered-MONO field theory are not concluded on; S4 is a bounded point-mass deviation band (the correspondence between μ and ν as algebraic objects remains exact).
2. **Singular is not generic:** the filter probe is a point mass; extended sources and the S-term's action on smoother profiles may show different (smaller) bands — stated as the open implication.
3. The ℓ=2 BVP is a linearization about the Plummer background with a compact quadrupole source; it quantifies the *response* difference, not a closed-form mapping (that is the child spec).
4. Grid evidence is finite: the monotonicity/identity claims are proven in Lean (Q cell, generic duality, counterexample); the other cells' monotonicity is grid-verified on 181 points (bracketed bisection, not grid proof, for the inversions).
5. `mu_bad` is a demonstrator kernel, not a physical branch of the framework; it establishes the *structural* failure mode only.
6. The heat filter's measure/domain (Euclidean ℝ³ here) is declared, not derived from the amended action.

## 10. First additional implication to transfer (and child)

**Next bridge:** the exact ℓ=2 *transfer kernel* of the operative MONO branch — the closed-form (or precisely bounded) linearized response ratio `R_A/R_Q(y)` as a function of the local background argument y, converting S3's single-profile measurement into a transferable operator statement, plus the filter-band formula `|g_filt − nu(gN)gN|/(nu gN) = F(ξ/r0, r/ξ)` for extended sources. The Q-cell exact inverse and the correspondence identity make the spherical static content exact; the *aspherical* content is currently a measurement, not a theorem.

**Child spec** `AS040.C01` (written to `deepseek_push/astra_spawn_ideas/branches/AS040/AS040.C01.md`, NOT dispatched — no subagent spawn available to this worker; ready for the orchestrator).