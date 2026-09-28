# AS006 — The MOND radius as a dimensionless reduction

**Run:** `run_20260927T201133_AS006` · **Worker:** deepseek/deepseek-v4-flash-0731 (OpenRouter), Hermes subagent · **Branch:** CORE scale identities (task's declared branch; Q/RAR/MU2/EXP/MONO kept distinct) · **Sources hashed:** README.md `91a5fac4…a6b6ed`, FRIED_CHICKEN_SPEC.md `98d9149f…8e3f`, campaign_fresh_gravity_astra/DERIVATIONS.md `8da8176e…b889` — all match SOURCE_MANIFEST.json and the task's pin hashes. Task file SHA-256 `4a600837e652d713cfbad387064ab3af3ec23ae87a6bbfbc6855b564c4cd1916`.

---

## 1. Precise claim, symbols, boundary conditions, assumptions (task step 1)

**Claim under test.** With framework inputs
`a0 = kappa*c*sqrt(G*rho_Lambda), kappa = 1/2` (adopted, fitted **not** derived — zero-mode theorem, README rev. 8/README line 7; nothing in this task removes kappa's freedom), and `r_M = sqrt(G*M_b/a0)`, the dimensionless pair `(x, g/a0)` with `x = r/r_M` is a **genuine dimensionless reduction** of the spherical point-baryon acceleration problem: every acceleration ratio built from the variables `{G, M_b, a0, r}` reduces to a fixed function of `x` alone, with **no independent fitted input**; deep-limit quantities reduce to the constant functions implied by `v_flat^4 = G*M_b*a0`. "Genuine" means: (i) the identity `B/a0 = x^-2` is exact (not an approximation), (ii) the scaling exponent 1/2 in `r_M ∝ (G M_b/a0)^{1/2}` is forced by dimensions, (iii) the surviving hidden assumptions are enumerated, conditional, and do not hide a second fitted scale.

**Symbol dictionary (all SI unless noted).**

| symbol | meaning | units | status |
|---|---|---|---|
| `a0` | vacuum acceleration scale, `kappa*c*sqrt(G*rho_Lambda)` | m s⁻² | framework input (footing-valued) |
| `kappa` | coefficient of the a0–Λ relation | — | = 1/2 **adopted** (fitted, not derived) |
| `rho_Lambda` | mass density of the vacuum sector | kg m⁻³ | input (two footings, see §6) |
| `G` | Newtonian coupling of the point baryon (single symbol here; `G_N, G_bare, G_cosmo` stay separate globally — this task uses only the point-source Newtonian `G`) | m³ kg⁻¹ s⁻² | input, 6.67430e-11 |
| `c` | speed of light | m s⁻¹ | input, 299792458 |
| `M_b` | baryonic mass (spherical point baryon) | kg | input (translated: 1e6/1e9/1e12 M_sun) |
| `r` | radial distance, `r > 0` | m | independent variable |
| `B` | Newtonian baryonic acceleration `G*M_b/r^2` | m s⁻² | definition |
| `r_M` | MOND radius `sqrt(G*M_b/a0)` | m | derived (the object studied) |
| `x` | `r/r_M` | — | derived, dimensionless |
| `y` | `B/a0 = x^-2` | — | derived, dimensionless |
| `g` | total radial acceleration | m s⁻² | derived (kernels below) |
| `C` | `sqrt(G*M_b*a0) = a0*r_M` | m² s⁻¹ | derived (flat-speed moment) |
| `v_flat` | `(G*M_b*a0)^{1/4}` | m s⁻¹ | derived |
| `xi` | coherence length of the heat filter `S = exp[(xi^2/2) Δ]` | m | operative-MONO parameter (Cassini floor, §8) |

**Framework cell.** Kernel: task-level profiles evaluated for Q, RAR, MU2, EXP (historical AQUAL), MONO (operative spliced phantom) as **distinct labelled branches**; no identification. Filter: `S = exp[(xi^2/2)Δ]` enters only in §8 (operative transfer), where it is an explicit assumption, not silently dropped. Gate: A01 scale identities; operative closure target: amended thirteen-item requirement 1 (filtered ν_mono) and requirement 13 (a0–Λ relation, κ adopted) under causality criterion B. Initial/boundary data: point baryon at origin, spherical symmetry, no external field, Euclidean exterior with standard fall-off. Units: SI (m, kg, s) throughout; dimensionful examples on **both** footings.

**Boundary conditions / domain of the identity.** `B = G*M_b/r^2` for all `r > 0`; `x > 0`; kernels evaluated on `y = x^-2 ∈ (0, ∞)`. No observational fit anywhere in this task.

## 2. Reduction to x; which dependences disappear; translations (task step 2)

**Identity (exact, all positive reals).**

```
B/a0  =  G*M_b / (a0 r^2)  =  (G*M_b/a0) / r^2  =  (sqrt(G*M_b/a0)/r)^2  =  (r_M/r)^2  =  x^-2 .
```

This is one line of real algebra: `G M_b/(a0 r²) = (√(G M_b/a0)/r)²`. Certified in Lean (`b_over_a0_eq_x_neg_two`), and verified numerically to `≤ 6.6e-16` relative on a 2001-point log grid × {1e6, 1e9, 1e12 M_sun} × both footings (C1), and to `≤ 3.3e-51` relative at 50 decimal digits (C8).

**Which dependences disappear.** In the reduced pair `(x, g/a0)`:
- `M_b` disappears from the *shape*: `g/a0 = x^-2 · ψ(x^-2) =: F_ψ(x)` for any kernel `ψ` (see table). The two-parameter family `{M_b, a0}` collapses to one parameter `x`; curves for masses differing by 10¹² coincide to `5.8e-11` in absolute `g/a0` units over the whole grid (C2).
- `a0` enters only through the length `r_M` (exponent −1/2) and the acceleration unit; the identity is even invariant under the simultaneous rescaling `(M_b, a0) → (λM_b, λa0)` — "the same prediction in equivalent variables" (Lean: `rM_rescaling_invariant`, `b_over_a0_rescaling_invariant`, `collapse_same_x`).
- What does **not** disappear: dimensioned deep quantities of course retain their scalings, `v_flat ∝ M_b^{1/4} a0^{1/4}`, `r_M ∝ M_b^{1/2} a0^{-1/2}`, `C = √(G M_b a0)`; the reduction is a statement about *dimensionless profiles*, not about dimensioned values.

**Translations. `M_sun = 1.98847e30 kg`, `pc = 3.0856776e16 m`.**

| M_b [M_sun] | r_M [pc] (can) / [pc] (alt) | v_flat [km/s] (can / alt) | C [m²/s] (can / alt) |
|---|---:|---:|---|
| 1e6 | 38.586 / 35.154 | 10.558 / 11.061 | 1.1147e8 / 1.2235e8 |
| 1e9 | 1.2202 kpc / 1.1117 kpc | 59.371 / 62.201 | 3.5249e9 / 3.8690e9 |
| 1e12 | 38.586 kpc / 35.154 kpc | 333.87 / 349.78 | 1.1147e11 / 1.2235e11 |

Consistency: `v_flat^4 = G*M_b*a0` checked to `2.7e-16` relative; `v_flat^2 = a0*r_M` to `1.3e-16`; `C = a0*r_M` by construction. At `r = r_M` exactly, `B(r_M)/a0 = x^-2|x=1 = 1` (definition — no approximation), and `g(r_M)/a0 = F(1)` is a kernel number (see C5).

## 3. Intermediate algebra, signs, units; leading neglected terms and domains (task step 3)

**Branch table (spherical point-baryon algebraic level; branches distinct).**

| branch | definition | deep form `F(x)·x → 1` | leading deep correction (x ≫ 1) | Newtonian recovery (x → 0) |
|---|---|---|---|---|
| Q | `F_Q = sqrt(x^-4 + x^-2)` | 1 + x^-2/2 − x^-4/8 + … | `2 x² (F x − 1) → 1` | `F/x^-2 − 1 = x²/2 + … ` |
| RAR | `F_R = x^-2/(1 − exp(−1/x))` | 1 + 1/(2x) + 1/(12x²) + … | `2 x (F x − 1) → 1` | `F/x^-2 − 1 = e^-1/x + …` |
| MU2 | implicit `(1−(1+ξ/2)^-2) ξ = x^-2`, `F = ξ` | 1 + 3/(8x) + … | `(8x/3)(F x − 1) → 1` | `F/x^-2 − 1 = 4/y² + …` |
| EXP | implicit `(1−e^-ξ) ξ = x^-2`, `F = ξ` | 1 + 1/(4x) + … | `4 x (F x − 1) → 1` | `F/x^-2 − 1 = e^-y·(…)` |
| MONO | `ν_mono(y) = 1 + h_mono(y)/y`, RAR below splice, continuation above (§C6) | = RAR (deep is y→0, on the RAR segment) | same as RAR | `F/x^-2 − 1 = δ h_p ln y/y → 0` (slow, logarithmic) |

Leading neglected terms derived by Taylor expansion of each kernel:
- Q: `F·x = √(1 + x^-2) = 1 + x^-2/2 − x^-4/8 + …,` domain `x ≫ 1`, leading term `x^-2/2`.
- RAR: `ν(y) = y^-1/2(1 + y^1/2/2 + y/12 + …)`, so `F·x = 1 + 1/(2x) + 1/(12x²) + …`, domain `x ≫ 1`, leading `1/(2x)`.
- MU2: `μ(ξ) = ξ − 3ξ²/4 + ξ³/2 − …,` `μξ = x^-2 ⇒ ξ = x^-1(1 + 3/(8x) + …)`, leading `3/(8x)`.
- EXP: `(1−e^-ξ)ξ = ξ² − ξ³/2 + … ⇒ ξ = x^-1(1 + 1/(4x) + …)`, leading `1/(4x)`.
- MONO: below `y* = 2.3374` identical to RAR; above (interior `x < x* = 0.6541`) `ν_mono(y) = 1 + [h* + δ h_p ln((y+y_p)/(y*+y_p))]/y`.

**Distinctness audit (C6, computed):** `y_p = 2.53964` (spec landmark 2.5396; |Δ| = 4e-5), `h_p = 0.647610` (README bounded-boost Δ_max = 0.6476), `y* = 2.33741` from the derivative-equality root `h'_RAR(y*) = δ h_p/(y*+y_p)` (spec landmark 2.3374; |Δ| = 1.2e-5; residual ×(y*) = 4e-18), splice `x* = 0.6541`; `ν_mono = ν_RAR` to `1.4e-16` on `y < 0.99 y*`; continuity `|h_mono(y*+ε) − h_RAR(y*+ε)| = 1.7e-10`; the max-rule transitions at `y*±10⁻³` change sign as required (±3.5e-5). Landmark `y* = 2.3374` is confirmed to be the derivative-equality root (my first bracketing attempt with reversed bisection logic was the only failure; corrected to the analytic root with the sign-correct derivative `h'_RAR = (ν−1) − y e^-√y/(2√y(1−e^-√y)²)`, `ν' < 0`).

**Exact vs finite consistency:** `B/a0 = x^-2` is an **exact identity** in real arithmetic (Lean-certified; mpmath residuals at 50 digits are floating noise ≤ 3.3e-51). The branch profiles `F_ψ(x)` at fixed `x = 1` are finite kernel numbers, not limits: `F_Q(1) = √2 = 1.41421356…` (exact), `F_RAR(1) = 1/(1−e⁻¹) = 1.58197671…` (exact), `F_MU2(1) = 1.48929`, `F_EXP(1) = 1.34998` (implicit roots), `F_MONO(1) = F_RAR(1)` since `y = 1 < y*`.

## 4. Independent checks (task step 4)

All actual residuals (script `compute_AS006_mond_radius_reduction.py`, output `AS006_outputs.json`; bounds: wall 0.005 s measured ≪ 120 s; RSS 45 MB ≪ 512 MB; 1 thread enforced via OMP/OPENBLAS/MKL/NUMEXPR = 1; grid 2001 points, no refinement loop):

| check | content | tolerance (set before) | observed | pass |
|---|---|---|---|---|
| C1 | seed identity `B/a0 = x^-2` in physical variables, 6 (footing,mass) combos, 2001 log-points `x ∈ [3.16e-3, 316]` | rel ≤ 1e-9 | 6.6e-16 | PASS |
| C2 | collapse: max pairwise `|g/a0(M1,x) − g/a0(M2,x)|` for M_b = 1e6/1e9/1e12, Q branch | ≤ 1e-9 | 5.8e-11 | PASS |
| C3 | deep limits `F·x − 1` at x = 1e2/1e3 and leading-term ratios → 1 (Q: 0.9999998, RAR: 1.00017, MU2: 1.00027, EXP: 1.00029, MONO = RAR) | within 1e-3 | see values | PASS |
| C4 | Newtonian recovery `F/x^-2 − 1` at x = 3.16e-3 (Q 5.0e-6; RAR, EXP ≤ 1e-30; MU2 4.0e-10; MONO 9.7e-6 → 0) | behavior check | see values | PASS |
| C5 | normalization at x = 1: `B(r_M)/a0 = 1` exactly; `F(1)` branch values (Q = √2 exact, RAR = 1.58197671 exact) | exact & numerical | tabulated | PASS |
| C6 | MONO splice audit (above) | | | PASS |
| C7 | negative control (below) | | | ACTIVE |
| C8 | mpmath 50-digit spot identity at x ∈ {0.01, 0.1, 1, 10, 100} | ≤ 1e-38 | ≤ 3.3e-51 | PASS |
| C9 | translations; `v_flat^4 = G M_b a0`, `v_flat² = a0 r_M` identities | rel ≤ 1e-12 | ≤ 2.7e-16 | PASS |
| C10 | free parameters in `F(x)` = 0 (built only from declared constants; the only carried freedom is the adopted footing κ = 1/2) | 0 | 0 | PASS |

## 5. Negative control (task step 5) — must be capable of failing

Specified control: use `r_M' = G*M_b/a0` (linear candidate) and require **units and forward substitution to fail**. Verified (both footings):
- **(a) units** — `[G M_b/a0] = L³M⁻¹T⁻²·M·(L T⁻²)⁻¹ = L² (exponents [2,0,0])`, not a length; so `x' = r/r_M'` is not dimensionless and cannot define a dimensionless reduction.
- **(b) forward substitution** — claiming `B/a0 = (r/r_M')^-2` fails at the level of the missing length: the identity would require `(G M_b/a0)²/r² = (G M_b/a0)/r²`, off by the factor `(G M_b/a0)` (L²); numerically the dimensionless matching factor is off by ~10³⁶ (mismatch log10 ≈ 36.2 canonical, 1e6 M_sun).
- **(c) collapse** — the same physical radius `r = r_M(M1)` maps to `x'` values 10⁶ apart for M_b = 1e6 vs 1e12 M_sun, i.e. the profile does not collapse in `x'`-space.

The control is **capable of failing** in the required sense: it is a genuine falsifiable test (had the linear candidate been right, (b) and (c) would have passed; tolerances 1e-6 set beforehand), and it **rejects** the wrong radius. The `sqrt` in `r_M` is thereby forced by dimensional analysis: the unique length monomial constructible from `{G, M_b, a0}` is `(G M_b/a0)^{1/2}`.

## 6. Both footings (framework requirement)

The theorem is dimensionless and therefore **footing-independent by construction**: it uses only `B/a0` with positive real variables. Applicability statement: canonical footing `a0 = 9.3619e-11 m/s²` (κ = 1/2 on ρ_Λ = ρ_DE, ρ_Λ = 5.8444e-27 kg/m³) and alternative footing `a0 = 1.1279e-10 m/s²` (κ = 1/2 on ρ_total, ρ_Λ = 8.4831e-27 kg/m³) give the **same** reduced function `F(x)`; the two footings change only the dimensioned maps: `r_M ∝ a0^{-1/2}` (alt/can = 0.91106), `v_flat ∝ a0^{1/4}` (alt/can = 1.04768). Read consistently: holding ρ fixed at the canonical value and adopting a0 = 1.1279e-10 corresponds to effective κ = 0.60239 (not 1/2); the two footings cannot share both fixed ρ and fixed κ (stated, not conflated).

## 7. Strongest surviving statement

> **Theorem (scoped).** Fix `G > 0`, a baryon mass `M_b > 0`, a single adopted acceleration scale `a0 > 0` (either footing), and a spherical point baryon with Newtonian field `B = G M_b/r²`. Then, for **every** kernel of the form `g = B·ψ(B/a0)` (in particular Q, RAR, MU2, historical EXP, and the unfiltered operative MONO on its RAR segment), the identity `B/a0 = x^-2`, `x = r/r_M`, `r_M = √(G M_b/a0)`, is exact; the reduced acceleration profile `g/a0 = x^-2 ψ(x^-2)` is a fixed function of `x` alone with zero free parameters beyond the adopted footing; the deep limit is `g/a0 → x^-1` (`v_flat⁴ = G M_b a0`, `v² = C = √(G M_b a0)`), the Newtonian limit `g → B`, and every deep-limit *dimensionless* quantity (e.g. `v_flat²/C`, `g/g_deep`) reduces to a constant function of `x` — the constants being 1 (exact identity), while finite normalizations `F(1)` are branch numbers. Conditions: no external field; no second scale (see §8); spherical point source; kernel argument `B/a0` only. Without these the reduction is not claimed (each is a named assumption, none is a fitted input).

**Outcome:** supports-scoped-claim. The reduction is **genuine as an identity and as a dimensional structure**, with an enumerated set of composition assumptions; it is not a hidden-parameter fit. κ = 1/2 remains adopted (the task supplies no independent derivation of it).

## 8. Operative-gate transfer (filtered MONO) and the next unresolved implication

The operative target (amended requirement 1) uses `∇²Φ = 4πGρ_b + S*∇·[(ν_mono(|∇Su|/a0) − 1)∇Su]` with the heat filter `S = exp[(ξ²/2)Δ]`, coherence length `ξ ≥ 0.10 pc (canonical) / 0.15 pc (alt)` (Cassini floor). The filter introduces a **second scale**, so the exact x-only reduction is a property of the *unfiltered* point-source law. At the argument level: `Su_N` for a point mass is the Gaussian-smoothed monopole, `Su_N = −(GM_b/r)·erf(r/(√2ξ))`, so the filtered MOND argument is

```
|∇Su_N|/a0 = x^-2 · [erf(z) − (2z/√π)e^{-z²}],   z = r/(√2ξ) = x·r_M/(√2ξ),
```

with relative deviation from `x^-2` of `ε = −(2/√π) z e^{-z²} (1 + O(z⁻²))` — **exponentially small in (r/ξ)²** (asymptotic form cross-checked against the exact erf expression at z = 3: 5.0% relative, coincident with the 1/(2z²) next order). Evaluated at `r = r_M` for the tabulated masses: `log₁₀|ε| ≈ −3.2e4` (canonical, 1e6 M_sun) down to `−1e10` (1e12), i.e. `< 10⁻³²⁰⁰⁰` on both footings for all `M_b ≥ 1e6 M_sun`; `r_M/ξ` ranges 234–3.9e5. Hence for galactic baryons the operative filtered MONO branch inherits the x-only reduction to far beyond any observable precision; the exact statement `x^-2` requires the additional limit `ξ/r_M → 0`.

**Next unresolved implication:** the transfer is established here only at the *argument* level (`|∇Su|/a0`). What remains open: solving the operative **filtered two-field system** itself (the adjoint `S*`, boundary conditions and the phantom density `(ν_mono−1)∇Su` in the r ≫ ξ exterior) to show the deep branch closes to the same `v_flat⁴ = G M_b a0` with the same exponentially suppressed ξ-corrections; and the extended-disk case, where the shape scale breaks x-purity. These are the first bridges to a full-theory transfer, and exactly the content of the child spec below.

## 9. Limitations (what this result does not establish)

- κ = 1/2, the footing densities, G, c, M_sun, pc are framework inputs; nothing here derives κ (zero-mode theorem stands).
- The reduction is dimensionless; dimensioned observables retain `M_b^{1/2}/a0^{1/2}` (lengths) and `M_b^{1/4}a0^{1/4}` (speeds) scalings.
- No field-equation solution, no EFE treatment, no extended/disk sources, no r ≲ ξ interior analysis for the filtered branch, no stability/causality (criterion B), PPN, matter conservation or lensing content. The equilibrium relations of the contract (σ² = C/2 etc.) are **not** used or claimed here.
- Numerical agreement (C1, C8) is finite evidence for an exact identity whose proof is the Lean certificate; a finite grid is not a universal theorem.