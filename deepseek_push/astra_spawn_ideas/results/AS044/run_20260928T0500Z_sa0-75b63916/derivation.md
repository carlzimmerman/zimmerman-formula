# AS044 — Deep point-source potential and boundary matching

**Run:** `run_20260928T0500Z_sa0-75b63916`
**Worker:** subagent seed `sa0-75b63916` (deepseek/deepseek-v4-flash-0731 via openrouter, Hermes subagent)
**Finished UTC:** 2026-09-28T05:43:00Z
**Governing task file:** `deepseek_push/astra_spawn_ideas/AS044_deep_point_source_potential_and_boundary_matching.md`
(sha256 `101062f86bea2fceb66e3caf9d409eed4294aedc5986d6596f7b0be9bbfd4051` — matches the pin in `claims/AS044.json`)
Dispatch-title reconciliation: the campaign dispatch named this seed "phantom secularity and turnover", but no such task file exists on disk; the registered, hash-pinned AS044 is *Deep point-source potential and boundary matching*. The pinned hash governs; the mismatch is recorded here and in `result.json`.

Companion artifacts in this directory:
`derive_as044.py` (bounded prototype, sha256 `f90a5f63…680a9dc`), `out/residuals.json` (`b87df310…e971220`), `out/run1.log`, `out/run2.log`, `out/run3.log` (`94dc77d1…c87e8d5`), `AS044_matching_cert.lean` (`66daf0a5…bc8ed`), `AS044_axioms.lean` (`1655557c…cf8569`), `axioms_check.out`, `probe_t6.lean`.

---

## 0. Reading the sources (step 1: claim, symbol dictionary, boundary conditions)

Sources inspected and hash-verified against `SOURCE_MANIFEST.json`:
- `README.md` — sha256 `91a5fac44ffe30db5f8e95247e5f04e913eccd149f2ff8b683c1f05510a6b6ed` ✓ (RAR landmarks §1.1: `s = 2.540`, `Δ = 0.6476`),
- `qwen_claude_field_theory/closure_2026/FRIED_CHICKEN_SPEC.md` — sha256 `98d9149fcebb3a15a1d01b0142587b7d346b3471b007b52457b17a3bcb5d8e3f` ✓ (criterion B amendment),
- `real_research/peer_review_2026_09_26/README.md` — sha256 `521d9ac36a93a27dcd6c995f78743ae9b1de4304095911871d81e6a70f9ecaac` ✓.

**Precise claim to be established (scoped):**
> Let the deep point-source force be `g(r) = C / r` with `C = v_flat^2 = sqrt(G·M_b·a0)` and MOND radius `r_M = sqrt(G·M_b / a0)` (`C = r_M·a0`). For `r > 0`, the potential
> `Φ_D(r) = C·ln(r / r_ref)`,  with `r_ref = e·r_M`,
> is (i) the exact integral of the deep force (`-dΦ_D/dr = g(r)`), (ii) uniquely fixed by **double continuity** (potential *and* force) at the finite transition radius `r_t` to a Newtonian interior `g_N = G·M_b / r²`, which forces `r_t = r_M` and the integration constant `Φ_D(r_M) = -C = Φ_N(r_M)`; (iii) numerically compatible with the operative filtered-MONO splice to a quantified leading neglected term.

**Symbol dictionary.**

| symbol | meaning |
|---|---|
| `a0` | Zimmerman acceleration scale, `a0 = κ·c·√(G·ρ_Λ)`, `κ = 1/2` **adopted as input** (not derived) |
| `ρ_Λ` | mass density fixed by the footing: `ρ_Λ = a0²·4/(G·c²)` under κ=1/2 |
| `G, c` | Newton constant, speed of light (SI, sect. 5) |
| `M_b` | baryonic mass |
| `B` | Newtonian acceleration `g_N = G·M_b / r²` |
| `y` | `B / a0 = (r_M / r)² > 0` |
| `x` | `g / a0` |
| `C` | `√(G·M_b·a0)` — square of the asymptotic circular speed |
| `r_M` | `√(G·M_b / a0)` — transition/MOND radius |
| `r_t` | finite radius where interior Newtonian and deep branches are matched |
| `r_ref` | reference radius of the log potential; **result:** `r_ref = e·r_M` |
| `h(y)` | excess `h = x·(ν(x)-1)`, `x = ν(x)` the acceleration interpolant |
| `ν_RAR` | `1/(1 - exp(-√y))` (RAR) |
| `μ2` | `1 - (1 + x/2)^-2` (MU2 interpolant for `x·μ2(x) = y`) |
| `ζ` | EXP AQUAL interpolant solving `x·(1-exp(-x)) = y` |
| `δ, y_p, y_star, h_p` | MONO splice parameters `0.05, 2.53963828218817, 2.33741240526633, 0.647610237891915` |

**Framework inputs (distinct from conclusions):** `a0 = κ c √(G ρ_Λ)`, `r_M = √(G M_b/a0)`, `v_flat⁴ = G M_b a0`, κ=1/2 adopted, `G_N/G_bare/G_cosmo` kept separate, branches Q/RAR/MU2/EXP/MONO distinct, filtered MONO operative (criterion B). Boundary conditions *to be established*, not assumed: `r_t`, `r_ref`, `Φ_D(r_M)`.

## 1. Integration of the deep force (steps 2–3: algebra, signs, units)

Deep acceleration is outward-positive magnitude `g = C/r`; potential from `Φ' = -g`:

```
Φ_D(r) = -∫ (C/r') dr' = -C·ln r + K
```

**Force continuity at r_t** (identity, no approximation):

```
G·M_b / r_t² = C / r_t  ⟹  G·M_b = C·r_t                     (multiply by r_t² ≠ 0)
C² = G·M_b·a0  ⟹  r_t² = (G·M_b)² / (G·M_b·a0) = G·M_b / a0 = r_M²
r_t, r_M > 0  ⟹  r_t = r_M
```

**Potential continuity at r_t = r_M:** Newtonian interior potential `Φ_N(r) = G·M_b / r + k_N` (sign: −∫g_N dr with the boost convention of the framework, so interior values are positive at finite r; only differences and the boundary value matter). Setting `Φ_D(r_M) = Φ_N(r_M)` fixes the free constant. Evaluate the deep side at `r = r_M` with `r_ref` still free:

```
Φ_D(r_M) = C·ln(r_M / r_ref)  =  G·M_b / r_M + k_N  =  C + k_N          (G·M_b = C·r_M)
```

Choosing the natural zero of the Newtonian interior at the matching point is not needed: **equivalently, the deep potential is written with the reference radius that makes the potential continuous,** i.e. `r_ref = e·r_M`, because

```
Φ_D(r_M) = C·ln(r_M / (e·r_M)) = C·ln(1/e) = -C
Φ_D(r)   = C·ln(r / (e·r_M)) = C·(ln r - ln(e·r_M))
```

so that the deep branch attaches at `(r_M, -C)` to the interior, and the deep force at `r_M` equals `a0`:

```
g_D(r_M) = C / r_M = a0          g_N(r_M) = G·M_b / r_M² = a0      (both footings, sect. 5)
```

The reference radius `e·r_M` is forced by double continuity; any other `r_ref` leaves a potential jump at the transition (control C3 detects this — sect. 4).

**Leading neglected term (step 3, limiting regime domain).** The *operative* RAR-branch potential is not the pure log: `Φ_RAR(r) = ∫_r^∞ g_RAR(s) ds` with `g_RAR(s) = (G M_b/s²)·ν_RAR(G M_b/(a0 s²))`. For `r, r0 ≫ r_M` (`y ≪ 1`, `ν_RAR = 1/(1-e^(-√y)) = 1/√y + 1/2 + √y/12 + …`):

```
g_RAR(s) = (G M_b / s²)·(r_M/s + 1/2 + …)   with  √(G M_b/a0) = C  ⟹  G M_b/r_M = C
         = C / s · (1 + (s/r_M)/2 + …)
Φ_RAR(r) - Φ_RAR(r0) = C·ln(r/r0) + (G·M_b/2)·(1/r0 - 1/r) + O((r0⁻¹ - r⁻¹)·(r_M²/r0))
```

so the **leading neglected correction to the pure log is `-(G·M_b/2)·(1/r0 - 1/r)`** (ratio of correction to log term → 0 as `r → ∞`). The control measures exactly this (sect. 4, `branch_leading_term_*_ratio`).

## 2. Independent checks (step 4) — actual residuals, high precision

Independent representations: direct differentiation of `Φ_D`; direct integration of `g_RAR`; a 5-branch diagnostic grid; a spliced MONO re-derivation; a Lean 4 certificate of the algebra (sect. 6). `mp.dps = 50`.

**(a) Derivative identity** — `d/dr [C ln(r/(e r_M))] = C/r` pointwise for `r > 0`:
- `ddr_PhiD_at_{2,5,10,100}rM` residuals ≤ `3.2e-50` (exact zero at 50-digit working precision; the residual is the working-precision floor). ✓
- Integration identity: `∫_r0^r g_RAR - C·ln(r/r0)` = `0.0` at 2, 5, 50 r_M and `≤ 1.9e-40` at 10 r_M. ✓ (These are not Booleans; raw values are in `out/residuals.json`.)

**(b) Diagnostic grid** `y = 10^k`, `k ∈ [-10, 8]`, step 0.1 (181 points); all roots bracketed by sign-change scanning + bisection (tol 1e-48), never trusted to grid proximity. Deep band `k ≤ -4`, log–log slope/coefficient of `h(y) = y(ν-1)`:

| branch | deep slope | coefficient |
|---|---|---|
| Q (`x² = 1 + y`) | 1.5 | 0.5 |
| RAR | 1.00001 | 0.500118 |
| MU2 | 1.00002 | 0.375143 |
| EXP AQUAL | 1.00002 | 0.250103 |
| **MONO (operative)** | 1.00001 | 0.500118 |

RAR and MONO share the deep `2·√(r/r_M)`-scaled asymptote `h ≈ (1/2)√y`; Q, MU2, EXP are discriminated (slope/coefficient differ). Max deep-relative deviation from pure power law over the band: 0.5% (RAR/MONO), 0.5e-4 (Q); at `k=-10` all branches sit within 5e-6 of their pure asymptote. Finite-`y` anchor at `y=1`: `x-1 = 0.5819767` (RAR/MONO), `0.4142` (Q), `0.48929` (MU2), `0.34998` (EXP).

**(c) Matching residuals, both footings** (`1e11 M_sun`):

| quantity (residual) | canonical a0 = 9.3619e-11 | alternative a0 = 1.1279e-10 |
|---|---|---|
| `g_N(r_M) - a0` | 1.56e-61 | 0.0 |
| `g_D(r_M) - a0` | 1.56e-61 | 0.0 |
| `Φ_N(r_M) + C` | 0.0 | 0.0 |
| `Φ_D(r_M) + C` | 0.0 | 0.0 |
| `r_t - r_M` | 1.32e-31 | 4.95e-31 |
| `r_ref / r_M` | 2.71828182846 = e ✓ | same |

**(d) Splice landmarks reproduced** (operative MONO): `y_p = 2.53963828218817` (declared 2.539638282), `h_p = 0.647610237891915` (declared 0.647610238), `y_star = 2.33741240526633` (declared 2.337412405); continuity residual at `y_star` = 0.0, derivative-crossing residual `h'_RAR(y_star) - δ h_p/(y_star + y_p)` = `2.8e-50`. MONO coincides with RAR exactly on the whole grid (`y ≤ 1 < y_star`), as the splice requires (`deep_regime_mono_vs_rar`: diffs = 0.0 or 1e-53).

## 3. Negative controls, each capable of failing (step 5)

- **C1 — log to infinity, finite zero at ∞ (must fail):** demanding a finite `Φ_D(∞)=0` from `C·ln(r/(e r_M))` is unsatisfiable: `Φ_D(10^k r_M)` grows as `C·k` (values 3.5e10 → 1.6e12 at 1e20 r_M). **Control triggered as expected** — the log band must terminate at a finite outer radius; that termination mechanism is the open implication (sect. 7).
- **C2 — force jump at arbitrary match radius:** `|g_N - g_D|/a0` at `r/r_M ∈ {0.25, 0.5, 0.9, 1.0, 1.1, 2, 4}` is {9.96, 1.66, 0.102, **0.0**, 0.069, 0.208, 0.156} — zero **only** at `r_t = r_M`. Discriminates.
- **C3 — reference-radius mutation:** residual `|Φ_D(r_M) + C|` is `3.52e10` for `r_ref = r_M`, `1.08e10` for `r_ref = 2 r_M`, and **0.0 for `r_ref = e·r_M`**. Mutation detected.
- **Deep/normalization boundary check (exact-vs-numerical distinguished):** the exact identities `C/r_M = a0`, `G M_b/r_M² = a0`, `r_t² = r_M²`, `ln(r_M/(e r_M)) = -1`, `C·ln(r_M/(e r_M)) = -C`, and `d/dr[C(ln r - ln(e r_M))] = C/r` are **proved** in Lean 4 (sect. 6), independent of the numerical checks.

## 4. Dimensional application — both footings separately

Framework `a0 = (c/2)√(G ρ_Λ)` (κ = 1/2 **adopted**): `ρ_Λ = 4 a0²/(G c²)`.

| quantity | canonical a0 | alternative a0 |
|---|---|---|
| `ρ_Λ` [kg/m³] | 5.844412454e-27 | 8.48308962e-27 |
| `v_flat` (1e11 M_sun) [km/s] | 187.7466 | 196.6975 |
| `v_flat` (6e10 M_sun) [km/s] | 165.2380 | 173.1158 |
| `r_M` (1e11 M_sun) [kpc] | 12.202 | 11.117 |
| `r_M` (1 M_sun) [pc] | 0.038586 | 0.035154 |
| `g_deep(10 r_M)` [m/s²] | 9.3619e-12 = a0/10 | 1.1279e-11 = a0/10 |

Consistent with the standing solar MOND radius ~0.045 pc (order class). **Note:** the two footings imply different vacuum densities — they cannot share both fixed `ρ_Λ` and fixed κ; this is a free premise of the framework, flagged for the κ-identification child (sect. 8).

## 5. Lean 4 certificate (algebra, zero sorry)

`AS044_matching_cert.lean` proves, in real analysis (mathlib, Lean 4.34.0-rc2 via `lake env lean`):

- `deep_force_at_rM` — `C/r_M = a0` from `C² = G M_b a0`, `r_M² = G M_b/a0`, positives;
- `newton_force_at_rM` — `G M_b/r_M² = a0`;
- `double_continuity_forces_rM` — `G M_b/r_t² = C/r_t` forces `r_t² = r_M²` (hence `r_t = r_M`);
- `log_rM_over_exp_rM` — `ln(r_M/(e r_M)) = -1`;
- `potential_continuity` — `C·ln(r_M/(e r_M)) = -C`;
- `log_div_pointwise` — log law: `ln(t/(e r_M)) = ln t - ln(e r_M)`;
- `deep_potential_deriv` — `HasDerivAt (t ↦ C(ln t - ln(e r_M))) (C/r) r` for `r > 0` (difference form, which is pointwise equal to the division form by the log law — the certified "cleared algebra").

Verification (full outputs in `axioms_check.out`):
```
lake env lean <abs>/AS044_matching_cert.lean        → exit 0 (no errors, no sorry)
LEAN_PATH=<run>… lean --root=<run> <run>/AS044_axioms.lean → exit 0
#print axioms ‹all 7 theorems› → [propext, Classical.choice, Quot.sound]   (⊆ allowed set)
```
The `-o`-artifact `.olean` and the axioms transcript live in this run dir only; nothing was written into `fable_independent_2026/lean_2026`.

## 6. Bounds actually enforced

- **Time:** internal deadline 100 s + shell timeout; run3 `elapsed_s = 0.561` (≪ 120 s) — enforced.
- **Memory:** RLIMIT_AS 512 MB requested; the macOS session refused raising the soft limit (`current limit exceeds maximum limit`, recorded in `out/run3.log`); OS-reported max RSS ≈ 1.9251e7 bytes ≈ 18.4 MB — the effective memory was the session default, far under 512 MB.
- **Threads:** 1 (single-process Python; `mp.mp.dps = 50`).
- **Samples:** grid 181 pts; bisection tol 1e-48, ≤ 250 iterations; integration on `[r0, r]` upward with r0 = 1000 r_M, sweep radii {10, 100, 500}·r_M.

## 7. Strongest surviving statement and next implication

**Strongest statement (scoped, both footings):** for a point-source deep force `g = C/r`, double (potential + force) continuity at a finite transition radius **forces** `r_t = r_M`, the reference radius `r_ref = e·r_M`, and `Φ_D(r) = C ln(r/(e r_M))` with `Φ_D(r_M) = -C` — exactly the deep potential used by the framework; the operative MONO branch inherits the RAR deep asymptote `h ≈ (1/2)√y` and is identical to RAR across the entire tested domain `y ≤ 1 < y_star`; the correction to the pure-log potential from the RAR branch is `(G M_b/2)(1/r0 - 1/r)` (ratio-to-log → 1 measured: 1.0084, 1.00092, 1.00025 at 10, 100, 500 r_M). Domain: `y ∈ [10⁻¹⁰, 10⁸]` grid, deep band `y ≤ 10⁻⁴`, point-source, non-relativistic.

**Next unresolved implication:** the global log potential has no finite `Φ(∞) = 0` limit (control C1); transferring the matched potential into the full filtered theory requires the **outer termination scale** — "identify the finite radius `r_out(M_b, a0)` at which `Φ_D(r_out) = Φ_ext(r_out)` for a matter-normalized exterior (`Φ_ext(∞) = 0`), or prove no such matching exists under criterion B." Until `r_out` is identified, everything stated here is the deep/interior band only.

## 8. Suggested follow-up (child)

- **C01 κ-identification (weakest premise):** κ = 1/2 is adopted, and the two footings force two different `ρ_Λ`. Child claim: "determine κ (or equivalently fix `ρ_Λ` from an independent vacuum-density measurement) so that canonical and alternative footings reduce to one; deliverable: `κ` posterior interval from `{a0, ρ_Λ}` cross-footing with controls on the 187.7 vs 196.7 km/s split."
- (Second, documented downstream: certified C¹ analyticity of the spliced `h_MONO` at `y_star` — held at 2.8e-50 numerically, unproved analytically.)