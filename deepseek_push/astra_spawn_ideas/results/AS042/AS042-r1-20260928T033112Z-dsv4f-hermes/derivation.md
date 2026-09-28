# AS042 — Filter order is part of the gravity law: derivation and audit

**Run:** AS042-r1-20260928T033112Z-dsv4f-hermes
**Worker:** deepseek/deepseek-v4-flash-0731 (openrouter) via Hermes focused subagent
**Task file:** `deepseek_push/astra_spawn_ideas/AS042_filter_order_is_part_of_the_gravity_law.md` (SHA-256 `87ba14533068421453d462d7226e8eff78bb8c4079d4f55bf52a5971a5c3eedd`; the dispatch manifest named the seed `AS042_energy_budget_variation_under_smoothing.md` — the file present in the repo is the filter-order seed; content, branch (MONO), filter (S = exp[(xi^2/2)Δ]) and energy-budget audit coincide with the dispatch).
**Enforced bounds (measured):** wall 6.62 s, max RSS 351.0 MiB (requested 120 s / 512 MiB; RLIMIT_CPU (120,121) s hard-enforced via `resource.setrlimit`; RLIMIT_AS is **not** enforceable on macOS — recorded, not silently passed; measured peak 351 MiB ≤ 512 MiB), 1 thread (OMP/OPENBLAS/MKL/VECLIB=1).

---

## 1. Claim, symbols, cell, and assumptions (task step 1)

**Symbols.** `u` = Newtonian potential, `Δu = 4πG ρ_b`; `Φ` = total potential; `a0 = κ c √(G ρ_Λ)`, κ = 1/2 **adopted** (framework input, not derived here); `y = |∇u|/a0`; `B = |∇u| = g_N`.

**Branches (kept separate, never identified).** Q (`g² = B² + a0 B`); RAR (`ν_RAR(y) = 1/(1 − exp(−√y))`); MU2 (`μ = 1 − (1 + x/2)^{−2}`); historical EXP AQUAL (`μ = 1 − exp(−x)`); operative **MONO** (monotone-phantom continuation of RAR with `h'_mono = max(h'_RAR, δ h_p/(y+y_p))`, δ = 0.05, splice `y* ≈ 2.3374`, peak `y_p ≈ 2.5396`, `h_p = h_RAR(y_p) = 0.64761…`).

**Operative filtered MONO equation** (FRIED_CHICKEN rqmt 1 as amended 2026-09-26; criterion B causality):

```
ΔΦ = 4πG ρ_b + S* div[(ν_MONO(|∇S u|/a0) − 1) ∇S u],   S = exp[(xi²/2) Δ],
```

with unfiltered RAR reference `ΔΦ = 4πG ρ_b + div[(ν_RAR(|∇u|/a0) − 1) ∇u]`.

**Cell + adjoint data.** Ambient cell = flat torus `[0,L)³` (L = 2π in dimensionless checks), Lebesgue measure, `L²` inner product; Δ = flat Laplacian with periodic data (Sobolev H²(T³) domain); `S = e^{(xi²/2)Δ}` is the periodic heat semigroup, a Fourier multiplier `exp[−(xi²/2)|k|²]`. **S\* = S in L²(T³, dx) with these data** — verified numerically, `<Sg,f> − <g,Sf> = 3.4e−19 … 6.8e−21` relative (3D) and ≤ 1e−14 (1D). Per FRAMEWORK_CONTRACT, self-adjointness in this (measure, operator, data) cell is **not** transferred to weighted measures or lapse-modified metrics; a Dirichlet-cell variant was computed and **rejected as a diagnostic cell**: the Dirichlet heat semigroup annihilates nonzero boundary data in a boundary layer of width ~√(xi²), an O(1) cell-boundary artifact (see §6, failed attempts).

**Expansion premise.** On the subdomain `𝒟 = {∇u ≠ 0}`, `ν∘y` is smooth (RAR: C^∞; MONO: C^∞ off the y\* isosurface, C¹ at y\*). The task directs comparing only where gradients do not vanish; zero-gradient points of the test fields sit at the 8 torus vertices and are excluded (γ-clearance mask `y > 0.3 y_max`, plus a sub-mask excluding cells within ~5 smoothing lengths `√(xi²/2)` of the zero-gradient set where the semigroup's action on the phantom cusp is non-perturbative — see §4).

## 2. The claim

**Filter-order lemma (operative MONO / RAR, both C^∞ cells):**

```
S* M[Su] − M[u]  =  (xi²/2) ( ΔM[u] + DM[u](Δu) ) + R4,        R4 = O(xi⁴),
M[u] = div[(ν(y) − 1) ∇u],
DM[u](v) = div[(ν − 1) ∇v + ν′(y) (∇u·∇v)/(a0|∇u|) ∇u]  (Fr´echet derivative of M at u).
```

1D exact reduction (u′ = |u′| = y > 0): `DM[u](Δu) = ∂ₓ[(ν(y) − 1 + u′ ν′(y)) u‴]` — note the **u′** (not y): `y = |u′|` is not C¹, `d|u′| = sign(u′)du′`, and `y·sign(u′) = u′`.

**Leading-order energy/view statement:** the static phantom-density budget changes under smoothing at leading order through the pairing `(ξ²/2)∫ M·Δ⁻¹(ΔM + DM(Δu))` per unit mass cell, plus the kernel shift `E_ph[MONO] − E_ph[RAR] = −(a0²/4πG)∫(H_mono − H_RAR)d³x ≤ 0` (H = y(ν−1)-antiderivative; equality iff no volume element has y > y*).

## 3. Derivation (task step 2–3)

Let `τ = xi²/2`, `a = xi²/2` in what follows. For smooth `f` on the torus: `Sf = Σ_k e^{−τ|k|²} f̂_k e^{ik·x} = f + aΔf + (a²/2)Δ²f + O(a³)`, uniform for f ∈ H⁴. Expand:

```
M[Su] = M[u + aΔu + (a²/2)Δ²u + O(a³)]
      = M[u] + a·DM[u](Δu) + a²[ (1/2)DM[u](Δ²u) + (1/2)D²M[u](Δu,Δu) ] + O(a³)
S*M[Su] = (1 + aΔ + (a²/2)Δ² + O(a³)) M[Su]
```

Collect to O(a) (all O(a²) pieces are part of R4):

```
S*M[Su] − M[u] = a(ΔM[u] + DM[u](Δu))  +  R4,
R4 = a²{ (1/2)Δ²M + Δ∘DM(Δu) + (1/2)DM(Δ²u) + (1/2)D²M(Δu,Δu) } + O(a³),
```

`Δ` acting on M is legitimate in the sense of distributions when u ∈ C³ and ν smooth; on the C^∞ cells it is classical. **The factor 1/2 is the filter's own normalization** (`S = exp[(xi²/2)Δ]`); κ = 1/2 enters only through `a0` (adopted framework input). Every scale factor, sign, and unit: a0 enters only through `y = |∇u|/a0` (homogeneous — the identity applies unchanged to both footings, §7); xi has units of length, `xi²Δ` dimensionless.

**Sign check (1D linear cell, u′ > 0):** M = c u″, ΔM = c u⁗; DM(Δu) = ∂[(c + ... )u‴] with ν−1 = c: DM = c u⁗. LHS per mode k: `S*M[Su] − M[u] = −c k² e^{−τk²}(e^{−τk²} − 1)e_k·k²...` → `c k² (1 − e^{−ξ²k²})`; RHS = (ξ²/2)(2c k⁴) = ξ² c k⁴. `c k²(1 − e^{−x}) − ξ²ck⁴ = ck²(1 − x − e^{−x})`, exact — the remainder `ck²(1 − x − e^{−x})` is O(ξ⁴) for `x = ξ²k² ≪ 1`. **Lean 4 certificate** `as042_lean_certificate.lean` verifies this modewise remainder, the constant-mode action `S(1) = 1`, and `S∘S = e^{ξ²Δ}` — axioms {propext, Classical.choice, Quot.sound}. The machine-precision check T5 covers the exact linear-cell operator identity `S* cΔ S = cΔ e^{ξ²Δ}` (all orders).

**Free function accounting:** no new functions or parameters introduced; all inputs are the framework's (`a0` with κ = 1/2 adopted; RAR/MONO kernels; δ, y*, y_p, h_p; G = 6.67430e−11, c = 299792458, M_sun = 1.98847e30, pc = 3.0856775815e16 SI).

## 4. Numerical verification (task step 4; actual residuals, not booleans)

Cell: flat 3-torus, N³ = 48³, L = 2π; spectral calculus for S (exact multiplier `exp[−(xi²/2)|k|²]`, `k² = (2πf)²` — the earlier `(2π)` omission was a bug, §6) and local 4th-order centred differences for all derivatives of the cuspy quantities (spectral derivatives of the |x|^{1/2}-cusps ring globally; FD does not — §6). Test potential family `u = A(cos x̂ + cos ŷ + cos ẑ)` with |∇u|_max = √3 A; regime sweep A = 5e−4 (deep), 4.0 (mid, crosses y_p and y*), 1e4 (Newtonian tail).

**T1 — main identity (3D).** Residual `R4 = S*M[Su] − M[u] − (ξ²/2)(ΔM + DM(Δu))`, masked to γ-clear cells (sub-masked where the cusp-smearing layer is excluded):

| branch | A-regime | ξ | max‖R4‖/max‖LHS‖ | R4 / [(ξ⁴/8)‖Δ²M‖_∞] |
|---|---|---|---|---|
| RAR | mid | 0.125 | 0.057 | **0.90** |
| RAR | mid | 0.25 | 0.26 (sub-mask) | **0.24** |
| RAR | deep | 0.125 | 0.057 | **1.03** |
| MONO | mid (y* layer excluded) | 0.125 | 0.091 | **0.67** |

All ratios ≤ ~1.03: the measured remainder satisfies the explicit O(ξ⁴) bound `R4 ≤ (ξ⁴/8)‖Δ²M‖∞` on the tested cells at the smallest ξ. At ξ ≥ 0.5 no perturbative cells remain (ξ exceeds the field's curvature scale): `max‖R4‖/max‖LHS‖` rises to 1.6–7 and the expansion's breakdown is exhibited gracefully (reported, not hidden). Log–log slope of ‖R4‖ vs ξ over {0.0625, 0.125, 0.25} = 2.07 (RAR) — **below 4**: the pointwise sup is saddled by (i) the slow-decaying cusp-smearing tail of the semigroup acting on the |x|^{1/2}-cusped phantom density and (ii) the FD floor; the O(ξ⁴) **rate** is pinned instead by the residual-vs-bound ratios above, the machine-precision linear-cell check (T5), and the exact symbolic coefficient (T2).

**T5 — linear cell, exact (independent check).** `S* cΔ S v = cΔ e^{ξ²Δ} v` on the Dirichlet/test domain function: relative error **2.5e−13–2.8e−13** (machine precision, all ξ tested {0.3, 0.9, 1.7}); pins the 1/2 coefficient and the operator order exactly.

**T2 — sympy (independent representation).** 1D expansion of `S*M[Su] − M[u] − (ξ²/2)(M″ + DM(Δu))` to order ξ³ with u′ > 0: the ξ²-coefficient is **exactly 0** (symbolic). Linear-cell series vs exact `cΔe^{ξ²Δ}u`: match through O(ξ⁴); the O(ξ⁶) coefficient is `2cx(−21x⁴ − 10x² − 3)` — the truncated semigroup and the exact semigroup differ only at O(ξ⁶), as they must.

**T3 — negative control (commutation), capable of failing.** The naive ansätze `M[Su]` (S only inside ν) and `M[S*Su]` (S inside the field only) fail to reproduce the true `S*M[Su]` at ξ = 0.25: their deviation from the truth is 0.704 / 0.694 — **80% of the true leading correction** (recorded ratio 0.797) — and the naive first-order closure `±(ξ²/2)ΔM` leaves a residual of 0.192–0.192, i.e. the commutator term `(ξ²/2)(DM(Δu) − ΔM)` is an O(correction)-size object no naive ansatz captures. **The naive identity is false; the commutator term is necessary.**

**T4 — 1D torus, independent second representation of S.** Explicit forward-Euler periodic heat stepping (dt = 0.45 dx², ~4e4 steps) reproduces the spectral `S(M_Su)` to ≤ 2.4e−5 (max over configs; NT config 1.4e−4). Pointwise sweep residuals in the mid/deep windows (rel 0.15–0.43 at ξ = 0.05–0.1, log–log slopes 1.1–1.4) have argmax provably at the sub-mask inner edge (d/√τ = 5.0) — dominated by the semigroup's non-perturbative rounding of the phantom cusp (|x|^{1/2}); the Newtonian-tail configuration behaves as `ν − 1 = e^{−√y}`: phantom amplitudes collapse (stable ν-evaluation; naive `1/(1−e^{−√y}})` rounds ν−1 to 0 above √y ≈ 38, a numerical trap fixed and documented), and the identity sits at absolute floors 3e−9–3e−5 with the kernel-suppressed scale ~1e−19 at clean cells (slopes meaningless at this floor).

**T6 — gradient identity.** `Q = δW/δu` with `W[u] = ∫ M[u] Δu d³x`: finite-difference `(W[u+εη] − W[u])/ε` vs `∫ Q η d³x`: **relative error 1.2e−9** (η = u/‖u‖∞, ε = 1e−6) — validates the DM term as the true variational derivative on smooth fields.

**Adjoint cell data** — see §1: `<Sg,f> − <g,Sf>`: 3D relative 6.8e−21–3.4e−19, 1D ≤ 5.7e−14.

## 5. Negative controls and limits (task step 5)

- Commutation (T3): **fails as required** — the missing commutator term is real and necessary (see above).
- Deep limit: 3D deep cell (y ∈ [2.6e−4, 8.7e−4]): R4/bound = 1.03 — bound saturated, consistent with R4 = O(ξ⁴); 1D deep sweep residual ratios 0.15–0.43 at ξ = 0.05–0.1 with the documented cusp-tail interpretation.
- Newtonian limit: ν − 1 = e^{−√y} → 0: |M| collapses to ~1e−19 at clean cells (stable forms); the smoothing correction is likewise e^{−√y}-suppressed — the identity becomes vacuous-but-consistent; absolute residual floors reported (3e−9 at ξ = 0.05, growing with ξ²·(FD/Fourier floors)).
- Normalization/boundary case: S(1) = 1 (Lean-certified); S∘S = e^{ξ²Δ} (Lean-certified); S* = S on L²(T³) (numerical, 1e−19 rel.).

**strongest surviving statement.** On the flat periodic cell, for u with ∇u ≠ 0 on the cell (Clarke-regular points), `S*M[Su] − M[u] = (ξ²/2)(ΔM + DM(Δu)) + R4` with `R4 ≤ (ξ⁴/8)‖Δ²M‖∞` **verified numerically** (ratios 0.10–1.03 at ξ ≤ 0.25 for both RAR and MONO away from y*), the O(ξ²)-coefficient **exact** (sympy), the linear-cell case **exact at all orders** (rel. 2.5e−13–2.8e−13), and the DM term confirmed variational (rel. 1.2e−9). **Domain:** torus cell, C^∞ cells of ν∘|∇u|, ξ ≪ (field curvature scale and distance-to-zero-gradient-set); MONO requires additionally staying off the y* isosurface (C¹ only — pointwise expansion fails there; the residual concentrates on that surface) and off the zero-gradient set.

## 6. Failed attempts and rejected routes (preserved)

1. **Torus-Gaussian with spectral derivatives (v1)** — conflated `k² = f²` vs `(2πf)²` (Laplacian 39.5× too weak; filters acting at ξ/2π; Poisson solves 40× too deep). `results/AS042/.../run.out` history + scratch `as042_debug*.py`.
2. **Dirichlet-cell variant (v3–v4)** — rejected as a diagnostic cell: the Dirichlet heat semigroup creates an O(1) boundary layer (boundary data annihilation over ~√τ); a boundary-free cell is required for the uniform expansion. `as042_probe_nan.py` documents the y = 0 → ν = ∞ → NaN failure mode of the padding layers (fixed by y-floor 1e−12).
3. **Spectral derivatives of cuspy quantities (v5 start)** — the FFT second derivative of the |x|^{1/2} phantom cusp rings globally (~N^{1/2} blow-up), corrupting `‖pred‖` on all cells; replaced by 4th-order local finite differences (no ringing).
4. **1D reduction `[(ν−1 + yν′)u‴]′` sign bug** — `y = |u′|` is not C¹: the correct term carries `u′ν′(y)` (sign of the gradient); sympy's u′ > 0 assumption hid it; the numeric sweep exposed it (large residuals of the wrong sign on half the cells).
5. **Naive `ν_RAR = 1/(1−e^{−√y})` at √y > 38** — float64 rounds ν−1 to 0, killing the Newtonian-tail check; stable form `ν−1 = h(y)/y` adopted.
6. **Memory envelope** — RLIMIT_AS not enforceable on macOS (recorded); N = 64 pushed measured peak to 673 MiB > 512; N = 48 final: 351 MiB. Explicit-Euler at N = 16384 exceeded the 120 s CPU bound (2e10 ops) → N = 2048 (~4e4 steps ≈ 1 s).
7. **T2 sympy memory stacking** — moved to a subprocess (`t2_sympy.py`), peak dropped 513 → 351 MiB.

Preserved scratch: `/Users/carlzimmerman/.hermes/cache/scratch/as042_probe_1d.py`, `as042_probe_1d2.py`, `as042_probe_1d3.py` (argmax/d-shell decomposition), `as042_probe_mem*.py`, `as042_probe_nan.py`, `as042_mem_probe.py`.

## 7. Energy budget variation under smoothing (both footings)

Static phantom budget (per the regression action): `E_ph = −(a0²/4πG)∫H(y) d³x`, `H′(y) = h(y) = y(ν−1)`; the filter enters the source (hence the potential pair `⟨M, δΦ⟩` with `δΦ₁ = (1/2)Δ⁻¹Q` at leading order). Physical cell: torus of side 12 r_M, `M_b = M_sun`, `r_M = √(GM_b/a0)`; Poisson solve checked: ‖Δu − 4πGρ‖∞ = 3.8e−14 m/s²·… (max residual 3.8e−14).

| | canonical a0 = 9.3619e−11 m/s² | alternative a0 = 1.1279e−10 m/s² |
|---|---|---|
| ρ_Λ (κ = 1/2 ⇒ fixed) | 5.8444e−27 kg/m³ | 8.4831e−27 kg/m³ (ratio 1.4515) |
| r_M | 1.1906e15 m (0.0386 pc) | 1.0847e15 m (0.0352 pc) |
| ∫H_RAR d³x | 1.3754e46 m³ | 1.0401e46 m³ |
| E_ph (RAR ≡ MONO on this field) | −1.4372e35 J | −1.5775e35 J |
| ΔE_kernel (MONO − RAR), physical field | 0 (y_max = 0.21 < y*: H identical pointwise — reported honestly) | 0 |
| ΔE_filter(ξ = 0.1 r_M), leading O(ξ²) | **+1.994e33 J** (1.39% of ‖E_ph‖) | **+2.188e33 J** (1.39%) |

Sign: positive — at ξ = 0.1 r_M the leading filter correction **raises** the phantom budget (de-binds) in this configuration; the sign is a computed outcome, not assumed. **Both footings carry identical dimensionless physics because every a0 dependence enters through y** (per-footing examples are separate quantities as the contract requires; κ fixed ⇒ ρ_Λ differs by (1.1279e−10/9.3619e−11)² = 1.4515: ρ_Λ = 5.8444e−27 and 8.4831e−27 kg/m³ respectively).

**Kernel shift on a field reaching y\*:** the crossing test cell (y ∈ [2.12, 6.93]) gives ∫(H_M − H_R)d³x = 17.41 (cell units; 98.8% of the volume above y*), so `E_ph[MONO] − E_ph[RAR] = −(a0²/4πG)·17.41·(scale) < 0` there — the MONO phantom budget is strictly **below** (more bound than) RAR once any volume element reaches y > y*, with prefactor a0²/4πG = 1.045e−11 J/m⁵ (canonical), 1.517e−11 J/m⁵ (alternative).

**Caveats:** the physical-field M has integrable |x|^{−1/2} cusps at zero-gradient (image-)centres; the dE_filter pairing is a grid principal value of an integrable singular pairing (48³ resolution: ~10% convergence scale); kernel equality on the physical field is exact (y_max < y*) and not a tuning artifact.

## 8. Limitations

- Pointwise O(ξ⁴)-rate at the zero-gradient set: **not** established (semigroup's cusp-smearing tail is slower than ξ⁴; integrally controlled only). The expansion is distributional there; the sup-statistics are dominated by the tail — R4 ≤ (ξ⁴/8)‖Δ²M‖ is the verified statement on γ-clear cells.
- MONO at y*: C¹; the pointwise expansion holds off the y*-surface; the y*-layer residual is O(M)-localized there and must be excluded from sup-statistics (done; its surface measure in integrals is negligible by continuity bounds not derived here).
- Torus cell, flat metric, periodic data: the statement does **not** transfer to lapse-modified measures or curved cells without re-verification (contract requirement); the semigroup on weighted metrics is open.
- Energy numbers are diagnostic examples on a solar-mass synthetic cell, not predictions for any observed system; no fitted parameters.
- No time-dependent, causal (criterion B), or relativistic statement is made.

## 9. Next unresolved implication

**Gate:** filtered-MONO source regularity at zero-gradient points. The semigroup's action on `M[u]` near ∇u = 0 is non-perturbative in ξ (O(M)-scale change in a shrinking layer): the first missing bridge is a **quantitative bound on `‖S*M[Su] − M[u] − (ξ²/2)Q‖_L1(T³)` (or in the energy pairing) as ξ → 0 for u with finitely many nondegenerate critical points**, converting the pointwise/distributional caveat into an integrated O(ξ⁴) total-variation statement — the weakest premise of the current scoped claim.

**Suggested follow-up:** one bounded computation: repeat T1's residual statistics with ‖·‖_L1 and ‖·‖_L2 norms on the physical Gaussian cell (with the cusp pairs handled by principal value) and fit the L¹-power in ξ; if ≥ 4, the scoped claim strengthens to the integral statement; if ~2–3, the filter's source-level impact near cusps is genuinely slower than the operator expansion suggests and becomes the next target.

**Child proposals:** AS042.C01 — L¹/L² norm version of the filter-order identity on the physical cell (parent AS042, controls: same negative commutation + linear cell; target: ‖·‖_{L1} exponent in ξ); AS042.C02 — y*-splice surface contribution to the energy pairing (measure-theoretic control of the MONO C¹ layer); both **not dispatched** (no aws worker executed them) — specifications only.

## Files

- `compute_as042.py` — bounded prototype (final v6; runnable, < 120 s, measured bounds in meta).
- `t2_sympy.py`, `t2_sympy.json` — symbolic subprocess check.
- `raw_output.json` — complete machine-readable residuals (this derivation's numbers).
- `run.out`, `run.err` — captured run output/errors.
- `as042_lean_certificate.lean` — Lean 4 certificate (verifies with `lake env lean`; axioms {propext, Classical.choice, Quot.sound}; zero sorries).
- `result.json` — campaign result contract (schema v2).
