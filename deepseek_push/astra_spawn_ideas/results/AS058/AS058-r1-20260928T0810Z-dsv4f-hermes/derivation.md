# AS058 — Field redefinition and the channel slope — derivation

**Run:** `AS058-r1-20260928T0810Z-dsv4f-hermes` — worker `deepseek-v4-flash-0731 (openrouter) / Hermes subagent`
**Group A03 (coefficient mechanisms and their missing premises) · Branch: CORE coefficient; conditional MU_n statistical response (MU2).**
**Outcome: supports_scoped_claim** (dimensionless; both footings stated separately).

---

## 0. Task verification

- Seed `deepseek_push/astra_spawn_ideas/AS058_field_redefinition_and_the_channel_slope.md`, sha256 =
  `1d5455bde1c9a6843a40845cf27525fb40fc9f768bb479af85845c54acbed1f0` — **verified before execution** (matches task instruction).
- Pinned sources vs `SOURCE_MANIFEST.json` (all **match**, re-checked at packaging time):
  - `deepseek_push/PD01_polarization_count.py` = `37e39d1abb8dfe74763e59282b6137ed6a6b570215da415d197de72c33e2c74d`
  - `deepseek_push/PD08_particle_free_derivation.py` = `83f6054cdfb1b45834af1ce702b1a040f00ad1625ffc34799ae367bd367f0cfb`
  - `kappa_closure/k01_zero_mode_theorem_and_lambda_free_vacuum.py` = `8df5a3ab5a38d189e0152ab0e54c0fb497056e58373cc0e80db49fca3f35b25c`
- Contracts read before computing: `FRAMEWORK_CONTRACT.md` = `ca696c7f...`, `RESULT_CONTRACT.json` = `621fdad0...`,
  `ORCHESTRATOR.md`, `FIRST_PRINCIPLES_AND_BRANCHING.md`.
- Branch distinctness: AS054 (`run_20260928T0803`, channel-composition nonuniqueness) is a different result;
  AS058 tests redefinition invariance of the slope claim — related but distinct; cited, not re-treaded.

---

## 1. Precise claim, symbol dictionary, boundary conditions, assumptions (seed step 1)

**Claim under test.** *The deep-MOND slope of the response `mu(Y)` at `Y = 0` is the channel count `n`; the
derived deep coefficient is `a0 = s/n`, i.e. `kappa = a0/s = 1/n`; and this survives the same-theory field
redefinition `Phi' = lambda*Phi` (with the matter coupling `rho*Phi = rho*Phi'/lambda`), so `kappa = 1/2`
(at the adopted `n = 2`) is a property of the physical identification — not of the bare field variable.*

| symbol | meaning | status |
|---|---|---|
| `s = c*sqrt(G*rho_L)` | vacuum's own rate (fixed independently of a0; a0 an *output* on the one-scale reading) | framework input |
| `rho_L` | vacuum mass density | framework input |
| `kappa` | `a0/s` | **adopted = 1/2** (contract); derived as `1/n` within this lane for the physical normalization |
| `Y = |grad Phi|/s` | dimensionless drive (physical) | definition |
| `g = |grad Phi|` | acceleration | definition |
| `g_N = G*M/r^2` | Newtonian field of the source | definition (static spherical sector) |
| `mu_n(Y) = 1 - (1+Y)^(-n)` | MU_n response family; slope at origin = n | corpus member (PD01 count n; MU2 = n=2) |
| `p(Y)` | per-channel engagement, `p(0)=0`, `p'(0)=1`, completion unknown | premise (PD08 step 3; k01: no second coefficient derivable from the action) |
| `lambda > 0` | field rescale `Phi' = lambda*Phi` | diagnostic parameter |
| `n >= 1` | channel count, symbolic | parameter |

**Assumptions / boundary conditions:** static, spherical sector (Gauss-law source, point or spherically
symmetric); `Y in (0, oo)`; `G, M, r, s, g, g_N > 0`, `r > 0`; field equation in the PD08 convention
`div(mu(Y) grad Phi) = 4 pi G rho`.

**Framework inputs (not derived here, listed as such):** `kappa = 1/2` adopted; the OR-identification premise
(PD01 D1); the fraction identity `p'(0) = 1` (PD08 step 3, backed by k01's zero-mode theorem).

---

## 2. Kinetic and source coefficients under `Phi' = lambda*Phi` (seed step 2)

Action form (PD08):

```
S = (s^2/8piG) ∫ K(|grad Phi|/s) − ∫ rho·Phi
```

Relabel `Phi = Phi'/lambda`:

```
S = (s^2/8piG) ∫ K(|grad Phi'|/(lambda·s)) − ∫ (rho/lambda)·Phi'
```

- kinetic scale: `s → lambda·s` (pattern match inside K);
- source coefficient in the action: `rho → rho/lambda`;
- field equation by direct substitution of `Phi = Phi'/lambda` into `div(mu(Y) grad Phi) = 4 pi G rho`:
  `div( mu(|grad Phi'|/(lambda·s)) · grad Phi' ) = 4 pi G (lambda·rho)` — i.e. the field-equation source
  density rescales as `4πGρ → 4πGλρ`.
- **invariant argument:** `Y' = |grad Phi'|/(lambda·s) = |grad Phi|/s = Y`. The response's argument is the
  ratio of the *physical* gradient to the *fixed* vacuum rate — invariant under the same-theory redefinition.
  The measured acceleration `g = |grad Phi| = g'/lambda` is invariant (pure relabelling).

**Slope under a normalization change (S3).** Slope measured against the physical ratio `Y = g/s`: `d/dY = n`,
invariant. Slope measured against the primed field's gradient in *fixed*-s units `Z' = |gradPhi'|/s = lambda·Y`:
`d mu_n/dZ'|_0 = n/lambda` — at `lambda in {1/2, 1, 2}`: `{2n, n, n/2}`. **A slope claim survives a
normalization change iff the slope is measured against the physical acceleration in fixed vacuum units.**

## 3. Deep-MOND matching under the compensated redefinition (seed step 3)

Deep regime `Y << 1`: `mu_n(Y) = n·Y + O(Y^2)`. Static sector: `g·mu_n(g/s) = g_N`:

```
g·(n·g/s + O((g/s)^2)) = g_N   ⇒   g^2 = (s/n)·g_N   (yN := g_N/s^2 -> 0)
```

so `a0 = s/n`, `kappa = a0/s = 1/n`. Compensated redefinition: the primed-variable matching
`g'·mu_n(g'/(lambda·s)) = lambda·g_N` gives `g'^2 = (lambda^2 s/n)·g_N`; with `g = g'/lambda` (**S4**):

```
g^2 = g'^2/lambda^2 = (s/n)·g_N        (residual = 0, exact symbolic identity)
```

`g, g_N, a0, kappa` are all invariant under the same-theory redefinition; only the representation changes
(kinetic scale `lambda·s`; field-equation source `lambda·rho`).

**Leading neglected terms (S6).** Deep regime:

```
g·mu_n(g/s) = (n/s)·g^2 · [ 1 − ((n+1)/2)·(g/s) + O((g/s)^2) ],   mu_n series coefficient of Y^2 = −n(n+1)/2
```

correction `−(n+1)/2·(g/s)`; e.g. n=2: 4.5% at u=g/s=0.03, 1.5% at u=0.01; domain of the linear
deep law `u < 0.1` for better-than-15% accuracy. Newtonian regime:

```
mu_n = 1 − (1+Y)^(−n) = 1 − Y^(−n) + O(Y^(−n−1)),   neglected term Y^(−n)  (1% at Y = 10, n = 2).
```

Both limits are shared by **every** lambda-copy of the same theory (S4) and differ in the *changed* theory only
in the deep coefficient (S5).

## 4. Negative control — rescale the field, keep the matter coupling (controls that can fail)

**S5 (capable of failing — passed, flag raised).** With the source coupling **unchanged** (`rho' = rho`), the
rescaled-field theory's deep matching `g_c·mu_n(g_c/(lambda·s)) = g_N` gives

```
g_c^2 = (lambda·s/n)·g_N   ⇒   a0_c = lambda·s/n,   kappa_c = lambda/n.
```

Diagnostics at n=2, lambda in {1/2,1,2}: `kappa_c = {1/4, 1/2, 1}` — the derived coefficient is
normalization-dependent when the coupling is not rescaled. The flag: `kappa = 1/2` survives **only** the
compensated redefinition; the uncompensated rescale moves the coefficient across the whole measured band
(`kappa_meas ~ 0.465 ± 0.076, 0.551 ± 0.043`). The physical identification (metric-potential normalization
`h_00 = −2Phi` and the matter coupling) fixes the freedom.

**Newtonian/deep limits (N2).** Root ratio `u_c/u_ref` for the uncompensated rescale: deep regime → `sqrt(lambda)`
(1.414 at lambda=2); Newtonian regime → 1. Measured against analytic expectations including the finite-grid
tail corrections (S6): all 12 grid cells within 2e-3 tolerance (set before evaluation; exact numbers in
`raw_outputs/run_log.txt`). The uncompensated rescale is **physically visible**: `sqrt(lambda)` deep, unity
Newtonian.

## 5. Independent check in a different representation (seed step 4)

Bounded high-precision numeric roots over the grid `n in {2,3}`, `lambda in {1/2,1,2}`, `yN in [1e-4, 30]`
(deep subgrid `yN <= 3e-2` for N4):

- **N1** — compensated redefinition: physical root `u_phys = u'/lambda` of `u'·mu_n(u'/lambda) = lambda·yN`
  satisfies `u_phys·mu_n(u_phys) = yN`. Max relative deviation across the grid `= 0.000e+00`;
  max absolute equation residual `|u·mu(u) − target| = 4.441e-16` (bisection convergence noise; the identity
  is exact — S4 symbolic residual 0). **Actual residuals saved, not booleans.**
- **N3** — deep-law recovery at `yN = 1e-4`: `max |u^2·n/yN − (1 + (n+1)u/2)| = 2.242e-05`, consistent with
  `O(u^2) = (n^2−1)u^2/12` (= 1.3e-5, n=2). The a0-line is recovered exactly only at `yN = 0`.
- **N4** — leading deep correction: measured relative deviation matches `−(n+1)/2·(g/s)` to 10% relative
  accuracy; observed max 3.499e-02.

## 6. Both footings (dimensional examples kept separate)

Canonical `a0 = 9.3619e-11 m/s^2` → `s = 2·a0 = 1.87238e-10 m/s^2`, `kappa = 1/2` enforced;
`rho_L = 5.8444e-27 kg/m^3`. Alternative `a0 = 1.1279e-10 m/s^2`:
(i) `rho_L` fixed → effective `kappa = a0_alt/s = 0.6024`; (ii) `kappa = 1/2` fixed → `s_alt = 2.255800e-10 m/s^2`
with `rho_L` scaled by `(a0_alt/a0_can)^2` (`8.4831e-27 kg/m^3`, factor 1.4515). The two footings **never share
both** fixed density and fixed kappa. The derived statement is dimensionless (`kappa = a0/s = 1/n`); it applies
to the alternative footing with that footing's own `s`, and normalizations act inside one footing (S4), never
between footings.

## 7. Lean 4 certificate (algebraic core, n = 2, kappa = 1/2)

`AS058_field_redefinition_invariance.lean` (170 lines; compile host `fable_independent_2026/lean_2026`,
`lake env lean`; **zero errors, zero sorry**). Theorems:

- **T1** `or_identity_corpus`: `1 − (1 − Y/(1+Y))^2 = 1 − ((1+Y)^2)^(−1)` for `Y ≠ −1` (the OR-composition identity).
- **T2** `or_slope_generic`: for **any** completion `p` with `p(0)=0`, `p'(0)=1`: slope of `1−(1−p)^2` at 0 is **exactly 2** (completion-independent).
- **T3** `corpus_slope_two`: `d/dY[1−((1+Y)^2)^(−1)]|_0 = 2`.
- **T4** `slope_renormalized`: w.r.t. `Z' = lambda·Y` the slope is `2/lambda` — "normalization-free ONLY in the physical variable Y = g/s".
- **T5** `deep_law_invariance`: compensated redefinition: `g'^2 = lambda^2·(s/2)·(G M/r^2)` and `g = g'/lambda` ⇒ `g^2 = (s/2)(G M/r^2)`.
- **T6** `changed_theory_deep_law` (negative control): unchanged coupling `g·(2g/(lambda·s)) = G M/r^2` ⇒ `g^2 = (lambda·s/2)(G M/r^2)` — `a0_c = lambda·s/2`.
- **T7** `changed_coefficient_differs`: `lambda·s/2 ≠ s/2` for `lambda ≠ 1`, `s ≠ 0`.

Axiom audit (`#print axioms`, all seven): `[propext, Classical.choice, Quot.sound]` — no `sorryAx`,
no extra axioms. House traps handled: `mul_left_cancel₀` on `a*b = a*c` form; no trailing tactic after
`field_simp`; `congr_deriv` used instead of `convert` (this build's instance elaboration); `Pi.mul_apply`
bridging for pointwise products; `hasDerivAt_id (x := ...)` explicit argument.

## 8. Strongest surviving statement and the transfer implication

**Strongest statement (scoped, dimensionless, both footings):** under the framework premises (static
spherical sector; `mu_n = 1−(1+Y)^(−n)`, `n ≥ 1`; per-channel `p(0)=0`, `p'(0)=1`; `kappa = 1/2` adopted),
the deep coefficient of the physical acceleration in the compensated normalization is `a0 = s/n`, i.e.
`kappa = 1/n`; at the adopted `n = 2`: `kappa = 1/2`, invariant under `Phi' = lambda·Phi` with
`rho·Phi = rho·Phi'/lambda`. Domain: `0 < yN < oo` numerically (deep limit exact at `yN = 0`); diagnostics
at `lambda in {1/2, 1, 2}`; `n in {2, 3}` numerically, symbolic `n ≥ 1` analytically. The uncompensated
rescale is rejected by control S5/N2 (`a0_c = lambda s/n`; root ratio `sqrt(lambda)` deep, 1 Newtonian).

**First additional implication needed to transfer to the full theory:** the physical identification itself —
a separate argument that the *observational* normalization of the potential (`h_00 = −2·Phi`, matter coupling
`rho·Phi`) is the one in which `n = 2` channels saturate. The slope claim survives redefinitions *within* that
normalization class (S4) and fails *outside* it (S5); nothing in this lane derives which class is realized.
Next gate: the amended thirteen-item target (filtered MONO, causality criterion B) — needs a branch bridge from
MU2 deep behavior to the operative MONO interpolation before transfer (per branch protocol, no import without proof).