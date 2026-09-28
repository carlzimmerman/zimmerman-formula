# AS048 — MONO splice smoothing as a declared new candidate / heat-filter second-derivative-scale audit

**Run**: `AS048_20260928T055422Z_e8c82fcb`
**Seed**: `deepseek_push/astra_spawn_ideas/AS048_mono_splice_smoothing_as_a_declared_new_candidate.md`
**Seed sha256**: `8a54735e26d0da909364dcd17c2892063859a06d6e4839bd0899ee3b13dcb89f` (matches manifest.json pin and claims/AS048.json)
**Coverage note**: the dispatch brief named `AS048_mono_heat_filter_and_the_second_derivative_scale.md`, which does not exist in the catalog (0 matches). Per the manifest/claims pin, this run executes the real seed and folds the heat-filter/second-derivative-scale audit (filter `S = exp[(xi^2/2) Delta]`, exact Fourier multiplier `exp[-(xi^2/2)|k|^2]`, deviation vs the second-derivative scale `L`, interaction of the C^1-not-C^2 splice with the filter width xi) into the same framework cell, per the dispatch correction.

---

## 1. Framework cell (operative and candidate branches; both footings)

Dimensionless field equation variables: `y = B/a0 ∈ (0, ∞)`, `x = g/a0`, with the framework relation
`a0 = kappa * c * sqrt(G * rho_Lambda)`, **kappa = 1/2 ADOPTED as input** (mandatory framework).

| quantity | canonical footing | alternative footing |
|---|---|---|
| `a0` | `9.3619e-11` m/s^2 | `1.1279e-10` m/s^2 |
| `rho_Lambda` (back-solved, kappa=1/2) | `5.844412454021876e-27` kg/m^3 | `8.483089619559099e-27` kg/m^3 |
| kappa_eff if rho_Lambda fixed by one footing | 0.5 (consistent) | 0.6024 (inconsistent — alternative footing forces kappa ≠ 1/2) |
| `Lambda` upper bound if `Lambda = G*rho_Lambda >= G_N*rho_Lambda` | `1.0908e-52` (G_bare resolution) | `1.5833e-52` |

G_N/G_bare/G_cosmo kept separate (standard campaign separation); numerics `G=6.67430e-11, c=299792458, M_sun=1.98847e30, pc=3.085677581491367e16`.

**Branches**: Q, RAR, MU2, EXP frozen constitutive; **MONO = operative** (criterion B). Splice data adopted from AS033/AS034 (pinned): `y_star = 2.337412405266329`, `y_p = 2.539638282188165`, `h_p = 0.6476102378919149`, h'' jump `J = +3.4744713554836107e-2`, `delta = 0.05`.

## 2. Operative MONO field and the splice

- RAR branch: `nu_RAR(y) = 1/(1 - exp(-sqrt y))`, `h_RAR(y) = y/(exp(sqrt y) - 1)`.
- P(y) = delta·h_p/(y + y_p); for `y > y_star`: `h_mono(y) = h_RAR(y_star) + delta·h_p·ln((y+y_p)/(y_star+y_p))`.
- h is C^0, h' is C^0 (matches at y_star by construction), **h'' is NOT C^0**: h'' jumps by `J = +3.474e-2` at y_star (hpp_RAR(y_star) = −0.0361061, hpp_cont(y_star) = −0.0013613; jump = +0.0347447).
- Verified: h_mono(y_star) − h_RAR(y_star) = 0 exactly (log term vanishes); patch endpoints residuals < 1e-40 at 50 dps; h_p/hpp matches mpmath mp.diff to 7e-52 (analytic derivative rules confirmed).

## 3. Heat filter and its second-derivative scale

Operative filtered equation: a flat leaf is smoothed with **`S = exp[(xi^2/2) Delta]`** — a Gaussian heat step: exact Fourier multiplier `exp[-(xi^2/2) |k|^2]`; as a kernel, convolution with `G_xi(z) = exp(-z^2/2xi^2)/sqrt(2 pi xi^2)` (normalized: `∫ G_xi = 1`).

**Exact identities (Lean-certified, see §7):**

1. **Deviation bound (static, per mode)**: for the mode `k = 1/L`, `S(cos(ky)) = exp[-(xi/L)^2/2] · cos(ky)`, so the *amplitude* deviation from identity is
   `1 − exp[-(xi/L)^2/2] ≤ (xi/L)^2/2`  (Lean: `deviation_bound_exp`), i.e. the filter deviates from identity at second order in the ratio `xi/L` — the **natural separation statement**: the heat filter is scale-selective with intrinsic scale `xi`; modes with `L ≫ xi` are preserved to `O((xi/L)^2)`, modes with `L ≲ xi` are damped exponentially.

2. **Modal eigenrelation**: `u(x) = C·cos(kx)` with `C = exp[-(xi^2/2)k^2]` satisfies `u'' = −k^2 u` and `d/dt exp(-k^2 t) = −k^2 exp(-k^2 t)` — the damped cosine is an exact heat-semigroup mode; multiplying the amplitude by `exp[-(xi^2/2)k^2]` IS the exact filter action on the mode (Lean: `mode_first_deriv`, `mode_second_deriv`, `heat_mode_rate`). Amplitude identity `exp[-(sigma^2/2)k^2] = exp[-(sigma^2 k^2)/2]` (Lean: `multiplier_amplitude`).

3. **Normalization**: `∫_R G_xi = 1` (Lean: `gaussian_integral_norm`, `∫ exp(-z^2/2xi^2) = sqrt(2 pi) xi`) and `G_xi(z) ≤ G_xi(0)` (Lean: `gaussian_kernel_le_center`, `gaussian_kernel_peak`). Hence `S(1) = 1` and `S(affine) = affine` — no DC/constant leakage.

**Numerical verification (direct convolution, no FFT; 50-dps mpmath amplitudes):**

| xi, L | measured amp | predicted exp[-(xi^2/2)(1/L)^2] | residual |
|---|---|---|---|
| 0.01, 0.1 | 0.995012479192703 | 0.995012479192682 | 2.1e-14 |
| 0.03, 0.1 | 0.9559974818333 | 0.9559974818331 | 1.8e-13 |
| 0.1, 0.1 | 0.6065306597139 | 0.6065306597126 | 1.3e-12 |
| 0.03, 1.0 | 0.99955010123482 | 0.99955010123481 | 1.2e-15 |
| 0.1, 1.0 | 0.99501247919269 | 0.99501247919268 | 1.3e-14 |
| 0.5, 1.0 | 0.88249690258487 | 0.88249690258460 | 2.7e-13 |
| 1.0, 1.0 | 0.60653065971338 | 0.60653065971263 | 7.4e-13 |
| 0.3, 10.0 | 0.99955010123481 | 0.99955010123481 | 7.8e-16 |
| 1.0, 10.0 | 0.99501247919267 | 0.99501247919268 | 8.9e-15 |
| 3.0, 10.0 | 0.95599748183302 | 0.95599748183310 | 7.6e-14 |

C7 passes: max residual 1.28e-12 over the 9-row table.

**Deviation vs second-derivative scale (the audit's central table)**, `s = xi/L` → exact multiplier `1 − exp[-(xi/L)^2/2]`:

| s = xi/L | deviation 1−exp(−s²/2) |
|---|---|
| 0.05 | 0.001249 (0.12%) |
| 0.1 | 0.004988 (0.50%) |
| 0.14178 | 0.010000 (1.0%) |
| 0.3203 | 0.05000 (5.0%) |
| 0.5 | 0.1175 (11.8%) |
| 1.0 | 0.3935 (39.3%) |
| 1.4142 | 0.6321 (63.2%) |
| 3.0 | 0.9889 |
| 10.0 | 1.0 |

**Boundary**: a field whose second derivative varies on scale L is preserved to within 1% iff `xi ≲ 0.1418·L` (i.e. `L ≳ 7.05 ξ`); 5% iff `xi ≲ 0.32·L`.

**Identity checks** (xi = 0.02, interior window ≥ 8xi from zero-padded edges): S(1) = 1 residual 1.11e-16; S(affine) = affine residual 1.07e-14; leading term `(Sf − f)/(xi^2/2) → f''/2` for f = cos(0.5y) residual 6.25e-06 (grid-limited). PASS.

## 4. Interaction with the C^1-not-C^2 splice (h'' jump J at y_star) as function of xi

Linear decomposition (exact, by linearity of S): write `hpp_g = hpp_ref + J·theta(y − y_star)` where `theta` is the unit step and `hpp_ref` is the continuum (jump-removed) part. Then the filter residual on the *splice-smoothing* candidate splits:

- `D(y) := S(hpp_g) − S(hpp_ref) = J·S(theta) = (J/2)·(1 + erf((y − y_star)/(xi·sqrt2)))` — a smoothed step,
  height `J` (asymptotically), **value at y_star → J/2**, **max slope J/(sqrt(2 pi) xi)**;
- `B(y) := S(hpp_ref) − hpp_ref` — the background-curvature term.

Meanwhile a C^2 splice (quintic Hermite patch of width w, certified endpoint matching C^0/C^1/C^2) produces **force deviation scaling as w^2** (log-log slope 2.03) with sup|h_eps − h_mono| ≤ 0.003·J·w^2:

| xi | D(y_star) | J/2 | ratio | max slope measured | J/(sqrt(2π)ξ) | slope ratio |
|---|---|---|---|---|---|---|
| 0.03 | 0.017950 | 0.017372 | 1.033 | 0.46124 | 0.46204 | 0.99827 |
| 0.1 | 0.017546 | 0.017372 | 1.010 | 0.13859 | 0.13861 | 0.99984 |
| 0.3 | 0.017430 | 0.017372 | 1.003 | 0.046203 | 0.046204 | 0.99998 |
| 1.0 | 0.017390 | 0.017372 | 1.001 | 0.013861 | 0.013861 | 0.999998 |

The erf closed-form is confirmed by the value/slope ratios converging to 1 as xi widens (C10 PASS: the residual is exactly `D = J·S(theta)`).

**Kink detection control (negative control, must discriminate)**: window [y_star−1, y_star+1], xi = 0.1: max|S(hpp_g)−S(hpp_ref)| = **0.0187 with the jump** vs **0.0016 with the jump removed** — 11.6× separation: the RAR splice's C^1-not-C^2 character is quantitatively detectable in the filtered branch at filter widths xi well below the background curvature scale.

**Scale interplay**: for xi ≲ 0.3 (dimensionless) the jump term D dominates the background term B in the splice neighbourhood (jump-dominance ratio 83, 23 for xi = 0.03, 0.1); for xi ≳ 0.3 the background-curvature smoothing B_{max} (measured including the near-origin RAR curvature blow-up region) overtakes D. This is the expected heat-filter behavior: the filter only **sees** the singularity (C^1 kink) when its width xi is below the length scale on which the rest of the field's second derivative varies — the second-derivative-scale audit of §3 made quantitative: the splice contributes like a mode of scale ~xi, the background of scale ~O(1).

**Large-xi destruction (negative control)**: xi = 10 on nu_mono: sup relative deviation 0.028 — O(1) relative structure destruction, consistent with the N2 gate (large filter widths must wreck, not refine).

## 5. Negative controls (all registered)

- **N1 (overshoot gate)**: cubic Hermite in h' bridging [y_star−0.05, y_star+0.05] with both endpoint h' forced to −1.0·|window| (unphysically steep) → min h'_patch = −0.0879 < 0: monotonicity gate **REJECTS** the overshooting endpoint-matching polynomial (a working gate; the splice h' itself is monotone decreasing, C5: min h' > 0 at all w).
- **N2 (large-xi destruction)**: PASS (destruction registered, see §4).
- **N3 (independent roots)**: y_p, y_star, J recomputed from different brackets + mp.diff: |dy_p| = 0, |dy_star| = 3.1e-56, |dJ| = 8.4e-53.
- **NC_kink (jump detection)**: discriminates 0.0187 vs 0.0016 (§4).
- **NC4 (independent implementation)**: rerun on the independent-grid code path, PASS.

## 6. Limits and footings

- Deep limit (Newtonian): nu − 1 → 1.000e0 at y = 1e8; deep: h/sqrt y → 0.99999500 at y = 1e-10 (matches AS032 landmarks).
- Footings: see §1 table. Canonical footing self-consistent with kappa = 1/2 (kappa_eff = 0.5 exactly); the alternative footing would require kappa = 0.6024 — a *falsifiable* separation between the two footings, recorded, not adjudicated here.

## 7. Lean certificate

File: `AS048_certificate.lean` — verified with `lake env lean`, exit 0, **zero `sorry`**, axioms ⊆ {propext, Classical.choice, Quot.sound} for all 8 theorems:

| theorem | content |
|---|---|
| `deviation_bound_exp` | 1 − exp(−t) ≤ t for t ≥ 0 (the deviation bound of §3.1) |
| `mode_first_deriv` | d/dx [C·cos(kx)] = −C·k·sin(kx) |
| `mode_second_deriv` | d/dx [−C k sin(kx)] = −k^2·C·cos(kx) (mode eigenrelation u'' = −k^2 u) |
| `heat_mode_rate` | d/dt [exp(−k^2 t)·cos(kx)] = −k^2·exp(−k^2 t)·cos(kx) (the heat-semigroup multiplier action on the mode) |
| `gaussian_integral_norm` | ∫_R exp(−z^2/2xi^2) dz = sqrt(2π)·xi for xi ≥ 0 (kernel normalization, Mathlib `integral_gaussian`) |
| `gaussian_kernel_le_center` | exp(−z^2/2xi^2) ≤ 1 for xi ≠ 0 (kernel maximum at centre) |
| `gaussian_kernel_peak` | G_xi(z) ≤ G_xi(0) for xi > 0 (normalized kernel) |
| `multiplier_amplitude` | exp(−(sigma^2/2)k^2) = exp(−sigma^2 k^2/2) |

The erf-valued smoothed-step identity `D = (J/2)(1+erf((y−y_star)/(xi√2)))` is *numerically* verified (ratios 0.9983–0.999998); a fully formal `fourierIntegral_gaussian`-based real-part derivation of the cosine multiplier is recorded as a child proposal (AS048.C03).

## 8. Result and closure implication

**Claim (scoped, criterion B — operative branch declaration)**: *For the operative MONO branch with the heat filter S = exp[(xi^2/2)Delta], (i) the filter acts as the exact Fourier multiplier exp[-(xi^2/2)|k|^2] (verified on modes, residuals ≤ 1.3e-12), deviating from identity by ≤ (xi/L)^2/2 on fields whose second-derivative scale is L, and by ≤ 1% iff L ≳ 7.05·xi; (ii) the C^1-not-C^2 splice at y_star (h'' jump J = +3.474e-2) produces, under S, the residual D = J·S(theta) with D(y_star) → J/2 and max slope → J/(sqrt(2 pi) xi) — confirmed to within 0.2% (slope) at xi = 0.03 and better at larger xi; (iii) a C^2 patch of width w instead produces only O(w^2) force deviation, so the C^1 kink is the dominant filter-visible feature of the operative branch at xi ≲ 0.3.*

Closure implication: the filter cell `S = exp[(xi^2/2)Delta]` with kappa = 1/2 is *compatible* with the adopted splice data (criterion B, monotonicity gate passed on h'), provided the filter width satisfies `xi ≲ 0.3` (dimensionless) so the splice residual keeps its closed form and the background curvature stays unresolved; common-action domain: dimensionless y ∈ [0.005, 40], both footings. `closure_candidate = null` — the campaign gate (declared new candidate) requires the orchestrator review; no full-action witness file was supplied.

## 9. Limitations

- `D(y_star)/J/2 = 1.033` at xi = 0.03: small window-curvature admixture at the finest filter width (the erf form is asymptotic in xi/window); the slope ratio (0.9983) is the cleaner check and stays within 0.2%.
- B_{max} at xi ≥ 0.3 is contaminated by the near-origin RAR curvature blow-up of hpp_RAR (|hpp| ~ O(10) at y ~ 0.05–0.5); the B_max window therefore overstates the background term for large xi — recorded, not a failure of D (D is gradient-free of the corner by exact linearity).
- The dispatch-brief filename does not exist in the catalog; this run executes the manifest-pinned seed and folds the heat-filter audit in as compatible analysis (per dispatch correction).
- No attempt to physically calibrate xi (the filter width) to an observed scale; the second-derivative-scale ratios are stated in dimensionless units.
- The alternative footing (a0 = 1.1279e-10) forces kappa_eff = 0.6024 ≠ 1/2; both footings were carried through (all dimensionless checks are footing-independent), but the footing choice itself is not adjudicated here.

## 10. Bounds actually enforced

wall 6.02 s (limit 120 s), ru_maxrss 71,663,616 bytes ≈ 71.7 MB on macOS (raw getrusage bytes; AS034-worker ×1024 convention NOT applied), OMP/MKL/OPENBLAS/NUMEXPR threads all 1 (limit 1). mpmath 50 dps; direct convolution smoothing, no FFT; measurement windows ≥ 8xi from zero-padded edges.