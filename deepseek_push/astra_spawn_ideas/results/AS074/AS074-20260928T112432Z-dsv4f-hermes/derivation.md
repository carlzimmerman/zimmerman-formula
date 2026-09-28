# AS074 — Robustness of kappa under small kernel deformations: derivation

**Run:** `AS074-20260928T112432Z-dsv4f-hermes`
**Worker:** `deepseek/deepseek-v4-flash-0731` (OpenRouter), Hermes-agent subagent session
**Task SHA-256:** `bdd98da0002f21e418cbf719fc234ade0e40bc5ed879cc8b036ed4f04183ff00` (verified against the dispatched file on disk)
**Started / finished (UTC):** 2026-09-28T11:57:29.670 / 2026-09-28T11:57:29.756 (bounded prototype); Lean verification 2026-09-28T11:58 (see lean_compile_log.txt)
**Result contract:** schema v2. **Branch used:** CORE coefficient (`kappa`), MU2-family response; no Q/RAR/MONO/EXP import anywhere in the derivation (branch dictionary respected; all four are distinct and untouched).

---

## 1. Precise claim (conditional theorem)

Let `s = c*sqrt(G*rho_Lambda)` (an acceleration, m/s²), `Y = g/s`, and the response family

```
mu_eps(Y) = mu_base(Y) + eps*f(Y),        mu_base(Y) = 1 - (1+Y)^(-2),
f in C^1([0,infty)),  f(0) = f(infty) = 0,   eps in R small,  f'(0) = delta,
```

with the MU2-family response law `mu_eps(Y)*g = B` (B = Newtonian baryonic field `G*M_b/r^2`, radial, algebraic). Then, in the deep limit `Y -> 0`:

```
g^2 = B*s/(2 + eps*delta) * (1+O(Y)),
v_flat^4 = G*M_b * s/(2 + eps*delta)  (leading order),      kappa_eff := a0_eff/s = 1/(2 + eps*delta).
```

**Robustness statement (the seed's headline):** with the framework relation `a0 = kappa*s`, `kappa = 1/2` adopted on the undeformed footing,

```
kappa_eff = 1/2  for all small eps  <=>  f'(0) = 0.
```

A small kernel deformation preserves the deep coefficient exactly when it is first-order tangent at the origin (zero slope at `Y=0`). **Endpoint preservation `f(0)=f(inf)=0` is NOT sufficient** — the negative control exhibits a counterexample (`fB`, delta = 1, eps = 1/5: `kappa_eff = 5/11 != 1/2`).

First-order drift: `kappa_eff = 1/2 - (eps*delta)/4 + O(eps^2)`.
Domain of the leading-order statement: `B/s << 1` (i.e. `r >> r_M`, `r_M = sqrt(G*M_b/a0)`), `|eps|` such that `2 + eps*delta != 0` and the series coefficients of f are bounded.

This is a **conditional theorem**: every condition is listed in §3. Nothing here derives `kappa = 1/2` from a physical mechanism — the adopted half remains an input (consistent with k01's audit that within the local-action class it is an empirical boundary condition); the seed's named claim "robustness of kappa under small kernel deformations" is answered in the precise sense above: the coefficient is robust **iff** `f'(0)=0`, and its response to a general small deformation is exactly `1/(2+eps*f'(0))`.

## 2. Symbol dictionary

| symbol | meaning | units |
|---|---|---|
| `G` | Newton constant `6.67430e-11` | m³ kg⁻¹ s⁻² |
| `c` | `299792458` | m s⁻¹ |
| `rho_L` = `rho_Lambda` | vacuum mass density | kg m⁻³ |
| `s = c*sqrt(G*rho_L)` | dark-energy acceleration unit | m s⁻² |
| `a0` | framework scale `= kappa*s`, `kappa=1/2` adopted | m s⁻² |
| `Y = g/s` | dimensionless argument | — |
| `mu_base`, `mu_eps` | response functions (dimensionless) | — |
| `f`, `eps`, `delta=f'(0)` | deformation, amplitude, zero-slope | —, —, — |
| `g` | total radial acceleration | m s⁻² |
| `B = g_N` | Newtonian baryonic field | m s⁻² |
| `M_b`, `r` | baryonic mass, radius | kg, m |
| `v_flat` | deep circular speed | m s⁻¹ |
| `kappa_eff` | deformed coefficient in `a0_eff = kappa_eff*s` | — |
| `rho_M` = `r_M` | MOND radius `sqrt(G*M_b/a0)` | m |

Check: `s`: `[c]=m/s`, `[sqrt(G rho)] = sqrt(m³ kg⁻¹ s⁻² · kg m⁻³) = s⁻¹`, so `[s] = m s⁻²` ✓. `rho_Lambda = 4 a0²/(G c²)`: `m² s⁻⁴ / (m³ kg⁻¹ s⁻² · m² s⁻²) = kg m⁻³` ✓.

## 3. Assumptions — framework inputs vs derived conclusions

*Framework inputs (adopted, not derived here):*
- `a0 = kappa*c*sqrt(G*rho_Lambda)` with `kappa = 1/2` (framework contract; PD01/PD08 treat the half as the channel-count-2 slope, k01 confirms it is an empirical boundary condition for the local action class).
- `s = c*sqrt(G*rho_Lambda)` (so `s = a0/kappa = 2*a0` on the adopted footing).
- `v_flat^4 = G*M_b*a0` (deep equilibrium; framework base), `r_M = sqrt(G*M_b/a0)`.
- Response composition class: MU2-family algebraic response `mu(Y)*g = B`, `mu(0)=0`, `mu(inf)=1`.
- Numerical constants §2 (G, c, M_sun, pc).

*Premises of the conditional theorem:*
1. `f in C^1([0,inf))` (the seed's stated regularity) with endpoint preservation `f(0)=f(inf)=0`.
2. `mu_eps` response law, radial and algebraic; deep limit `Y -> 0`; circular equilibrium `v^2 = g*r` used only to convert `g^2` to `v_flat^4`.
3. `2 + eps*delta != 0`, `s != 0`, `G != 0`, `M_b != 0`, `r != 0` (nondimensionality of the coefficient formula).
4. `|eps|` small enough that f's quadratic-and-higher terms are subordinate (leading-order statement; exact formula for the linearized kernel).

*Derived (established here):* the slope `mu_base'(0) = 2`; the deformed slope `mu_eps'(0) = 2 + eps*delta`; the identification `g^2 = B*s/(2+eps*delta)` (leading order); `kappa_eff = 1/(2+eps*delta)`; the iff-robustness criterion; the counterexample family; all numerics.

## 4. Derivation (all scale factors, signs, units)

**4.1 Undeformed kernel.** From the seed identity (verified symbolically and in Lean):

```
mu_base(Y) = 1 - (1+Y)^(-2) = MU2(2Y),   MU2(x) = 1 - (1+x/2)^(-2),    (exact)
mu_base(Y) = 2Y - 3Y^2 + 4Y^3 - 5Y^4 + ...   near Y=0   =>   mu_base'(0) = 2.   (sign: all coefficients alternate; leading +2)
```

So `mu_base` is MU2 evaluated at `x = 2Y`, not at `Y` (MU2(Y) = 1 − (1+Y/2)⁻² ≠ mu_base(Y); e.g. at Y=1: 3/4 vs 5/9).

**4.2 Deformed kernel, slope.** With `f'(0)=delta`, Taylor: `f(Y) = delta*Y + O(Y^2)`, so

```
mu_eps(Y) = (2 + eps*delta)*Y + O(Y^2),      mu_eps'(0) = 2 + eps*delta.     (2: base slope; sign of eps*delta as in f)
```

**4.3 Deep limit of the response law.** `mu_eps(Y)*g = B`, `Y = g/s`:

```
(2 + eps*delta)*(g/s)*g + O((g/s)^2) = B
=>  g^2 = B*s/(2 + eps*delta) * (1 + O(Y)),        Y = g/s.
```

Leading neglected term: the `O(Y^2)` piece of the response contributes relatively `O(Y) = O(sqrt(B/s)/sqrt(2+eps*delta))` to `g^2`; the deep statement is exact for the *linearized* kernel `mu_lin(Y) = (2+eps*delta)Y` and asymptotic otherwise. Units: both sides m² s⁻⁴ ✓.

**4.4 Deep coefficient.** Circular equilibrium `v^2 = g*r`; `B = G*M_b/r^2`:

```
v_flat^4 = g^2*r^2 = [B*s/(2+eps*delta)]*r^2 = G*M_b*s/(2+eps*delta).
```

Framework matching: the base relation is `v_flat^4 = G*M_b*a0` with `a0 = kappa*s`. Identification of the deformed theory's scale `a0_eff = kappa_eff*s`:

```
kappa_eff = 1/(2 + eps*delta).        (exactly the seed's formula)
```

ε = 0: `kappa_eff = 1/2` — the adopted half reproduced. First-order: `1/(2+x) = 1/2 − x/4 + x²/8 − …`, i.e. `kappa_eff = 1/2 − eps*delta/4 + O(eps²)`.

**4.5 Robustness criterion.** For `eps != 0`:

```
kappa_eff = 1/2  <=>  1/(2+eps*delta) = 1/2  <=>  2 = 2 + eps*delta  <=>  delta = 0.   (Lean-certified)
```

So: zero derivative at zero ⇔ coefficient preserved. The physical reading: the deep MOND coefficient is a *leading-order* (linear-in-Y) property of the response; deformations that are tangent to first order at the origin are exactly the ones invisible to it. This also matches PD08's mechanism: in the OR completion class `mu = 1−(1−p)^n`, the slope is `n` *for every completion p* — precisely because every completion has `p'(0)=1` and the slope picks only the linear term; deformations with `f'(0)=0` are exactly the completion-perturbations PD08 already proved irrelevant.

## 5. Step 2 of the seed — the two deformations

Both preserve endpoints (`f(0)=f(inf)=0`) and are C^∞:

```
fA(Y) = Y^2/(1+Y)^4                fA'(0) = 0   -> kappa_eff = 1/2   EXACTLY (deep coefficient s/2 unchanged)
fB(Y) = Y/(1+Y)^2                  fB'(0) = 1   -> kappa_eff = 1/(2+eps)
```

Diagnostic scale family `f_L(Y) = lam*Y/(1+lam*Y)^2`, `f_L'(0)=lam`, evaluated at `lam = 1/2, 1, 2` (eps = 0.2):

```
lam = 1/2 : kappa_eff = 1/2.1  = 0.4761905
lam = 1   : kappa_eff = 1/2.2  = 0.4545455
lam = 2   : kappa_eff = 1/2.4  = 0.4166667
```

Three distinct coefficients from one functional form, rescaled: the coefficient genuinely moves with the deformation scale — a mathematical statement, not an observational preference (per the seed: "do not use observational preference as a mathematical proof"; none is used).

## 6. Independent checks — actual residuals (seed step 4)

All mpmath (dps 50, refined to 100), single-threaded; script `AS074_prototype.py`; raw output `raw_output.txt`.

**(A) Slope estimator at fixed Y:** `kappa_est(Y) = 1/(mu_eps(Y)/Y)`. For `fB` (eps=0.2, target 1/2.2 = 0.4545454545…):

| Y | kappa_est | |residual| | rate (per decade of Y) |
|---|---|---|---|
| 1e-2 | 0.4615837104072398 | 7.038e-3 | — |
| 1e-4 | 0.454615703831644 | 7.025e-5 | 100× (≈ O(Y)²) |
| 1e-6 | 0.4545461570249286 | 7.025e-7 | 100× |
| 1e-8 | 0.4545454615702479 | 7.025e-9 | 100× |

i.e. residual decays as the first power of Y (expected: subleading O(Y) term). For `fA` the estimator converges to exactly 0.5 (residuals 7.018e-3 → 7.000e-9). Refinement at dps=100: fB residual at Y=1e-8 = 7.0e-9 (unchanged) — digits stable.

**(B) Exact implicit response:** root-solve `mu_eps(Y)*Y*s = B` (bisection, 300 iterations; residual of the law itself ≤ 3e-49 at all B). Deep estimator at B/s = 1e-8: fB → 0.4545928188 (residual 4.74e-5 vs 1/(2.2)), fA → 0.5000495008 (residual 4.95e-5 vs 1/2); both extrapolate to their targets as B/s → 0 (deep coefficient read off the *solved* response, not the series).

**(C) Newtonian recovery (Y → ∞):** g/B for `fB` at B/s = 1, 10, 100, 1e4: 1.1891, 0.99182, 0.99814, 0.99998; |g/B−1| = 1.9e-1, 8.2e-3, 1.9e-3, 2.0e-5 — converges to the exact identity g=B (mu_eps(inf)=1 since f(inf)=0).

**(D) Boundaries (exact identities):** mu_eps(0) = 0 identically (f(0)=0); mu_eps(1e6) = 0.9999999999992 (fA) / 1.0000002 (fB) — finite checks of the exact limits; A–C are finite numerical consistency checks, D's zero/one limits are exact identities, distinguished explicitly.

## 7. Negative control (seed step 5; controls that must be capable of failing)

**Control — "endpoint preservation is sufficient for coefficient preservation," applied to the second deformation fB:**

```
premise prediction:  kappa = 1/2            (fB(0)=fB(inf)=0)
actual (control run): kappa_eff = 1/(2+eps) = 0.4545454545  at eps = 0.2
delta kappa = 0.5 - 0.4545454545 = 0.0454545455  != 0
=> the premise FAILS.  The control is capable of failing and DID fail (as the
   mathematics requires); the discriminator is verified: the same control PASSES
   for fA (f'(0)=0 -> 0.5 exactly), so the operative condition is the zero
   derivative at zero, not the endpoints.
```

Machine-checked instance: `control_fB_instance` in the Lean certificate — `1/(2+1/5) = 5/11 ≠ 1/2` (norm_num), from `slope_fB` and `kappa_eff_formula`. Deep and Newtonian limiting regimes checked in §6 (B, C); normalization and boundary cases in §6 (D).

## 8. Both scale footings (per framework contract — kept separate)

Constants: `G=6.67430e-11`, `c=299792458`, `M_sun=1.98847e30`, `pc=3.085677581491367e16`.

| quantity | canonical | alternative |
|---|---|---|
| a0 [m s⁻²] | 9.3619e-11 | 1.1279e-10 |
| s = 2·a0 [m s⁻²] | 1.87238e-10 | 2.25580e-10 |
| rho_L = 4a0²/(Gc²) [kg m⁻³] | 5.84441e-27 | 8.48309e-27 |
| r_M(M_sun) [m] ([pc]) | 1.19064e15 (0.038586) | 1.08474e15 (0.035154) |
| v_flat(M_sun) [m s⁻¹] | 333.866 | 349.783 |

Both are κ = 1/2 footings with *different* vacuum densities (ratio rho_alt/rho_can = 1.45149 = (a0_alt/a0_can)²) — they do not share fixed density and fixed κ. Held instead at the canonical fixed density, the alternative a0 corresponds to `kappa_eff = 1.1279e-10/(2*9.3619e-11) = 0.6023884...` (matches k01's 0.602 reading), i.e. density fixed ⇒ κ must move; κ rigid at 1/2 ⇒ density must move by (a0_alt/a0_can)².

**Deformation applied (fB, eps = 0.2, delta = 1), per footing (s fixed, ρ fixed):** κ_eff = 0.4545454..., a0_eff = κ_eff·s = 8.5108e-11 m s⁻² (canonical), 1.02536e-10 (alternative); v_flat,eff = 326.06 / 341.62 m s⁻¹; if instead κ is held rigid at 1/2, the required density change is (2·0.4545454)² = 0.82645×ρ_L on each footing. The dimensionless theorem (§1) covers both footings identically; the dimensional consequences are quoted per footing.

## 9. Source inspection and branch discipline

- `deepseek_push/PD01_polarization_count.py` (hash ✓ manifest): kappa = 1/n from the channel-count; n=2 is the framework's empirical premise ("n=2 EMPIRICAL, all derivation routes closed"). Consistent with §4.5: the slope-2 kernel is where the half lives.
- `deepseek_push/PD08_particle_free_derivation.py` (hash ✓): completion-independent slope 2 of `1−(1−p)²`; deformations with f'(0)=0 are exactly the completion perturbations invisible to that slope — this run's robustness criterion is PD08's lemma at the level of small deformations.
- `kappa_closure/k01_zero_mode_theorem_and_lambda_free_vacuum.py` (hash ✓): kappa=1/2 is an empirical boundary condition not derivable from the local action class; alternative-footing kappa 0.602 quoted there agrees with §8. This seed does not overturn that: the conditional theorem *assumes* the half on the base footing and characterizes its robustness.
- Branches: only MU2-family (CORE coefficient) conclusions are drawn. Q, RAR, EXP, MONO are distinct and were not imported (no branch translation attempted).

## 10. Lean 4 certificate

File `AS074_kappa_deformation_certificate.lean` (self-contained, imports Mathlib only; compiled with `cd fable_independent_2026/lean_2026 && lake env lean <abs path>`; toolchain `leanprover/lean4:v4.34.0-rc2`, mathlib v4.34.0-rc2). Thirteen theorems:

- `slope_mu_base` : HasDerivAt mu_base 2 0 — μ_base'(0)=2.
- `slope_deformed` : HasDerivAt (mu_eps eps f) (2+eps*δ) 0 given HasDerivAt f δ 0.
- `slope_fA` (0), `slope_fB` (1), `slope_fL` (λ) — the seed's two deformations plus the λ-family slopes.
- `linearized_deep_g_sq` : (2+εδ)·g·(g/s)=B ⇒ g² = B·s/(2+εδ) (exact for the linearized response).
- `deep_flat_coefficient` : ⇒ (g·g)(r·r) = G·M_b·s/(2+εδ) (i.e. v_flat⁴ = G·M_b·s/(2+εδ)) under B = G·M_b/r².
- `kappa_eff_formula` : with a0 = κ·s and v_flat⁴ matching, κ = 1/(2+εδ).
- `kappa_preserved_iff` : ε≠0 ⇒ (1/(2+εδ) = 1/2 ⟺ δ = 0) — the robustness criterion.
- `control_fB_instance` : 5/11 ≠ 1/2 — the negative-control instance, machine-checked.
- `mu2_doubling`, `mu2_not_same_at_one` : mu_base = MU2(2·), and mu_base(1)=3/4 ≠ MU2(1)=5/9.
- `robustness_of_kappa` : bundled statement.

Verified: exit 0; zero `sorry`/`sorryAx`; `#print axioms` for **all** theorems = `{propext, Classical.choice, Quot.sound}` — the hard bar. Log: `lean_compile_log.txt`.

## 11. First-principles accounting

```
axiom/input (named): G, c, rho_Lambda (per footing), kappa=1/2 (adopted), MU2 response law,
                     deep equilibrium v_flat^4 = G M_b a0, circular v^2 = gr, C^1 deformations f(0)=f(inf)=0.
derived:            mu_base'(0)=2; mu_eps'(0)=2+eps*f'(0); g^2 = B s/(2+eps f'(0)) (+O(Y));
                     kappa_eff = 1/(2+eps f'(0)); robustness iff f'(0)=0; counterexample family;
                     residuals (A)-(D); Newtonian limit; both footings' dimensional bookkeeping.
not derived:         the value 1/2 itself (remains an adopted input, as k01 requires);
                     dynamics of how a kernel deformation arises from the action (no candidate action here);
                     finite-Y behavior of generic f beyond leading order.
```

## 12. Strongest surviving statement and next unresolved implication

**Strongest surviving statement (scope: CORE-coefficient MU2 branch, algebraic radial response):** for C¹ endpoint-preserving small kernel deformations, the deep coefficient obeys `kappa_eff = 1/(2 + eps*f'(0))` exactly at leading order; `kappa_eff = 1/2` for all small ε iff `f'(0) = 0`; endpoint preservation alone is refuted as a sufficient condition (control, λ-family). Domain: Y→0 (deep), |εδ|<2, per-footing constants as in §8.

**Next unresolved implication:** the *second-order* sensitivity — the O(ε² f'(0)², ε) corrections to κ_eff induced by the quadratic term `f''(0)`, and the exact statement that the deep coefficient is *first-order-tangent-invariant* but not invariant under second-order perturbations (the response's Y² coefficient does NOT appear in v_flat⁴ — confirmed here by the series — so the open question is which observable in the theory probes f''(0), i.e. which gate breaks the leading-order degeneracy of the kernel class). Transfer to the full theory additionally requires: (i) a demonstration that a kernel deformation of the action (operated branch, e.g. AQUAL-style primitive or filtered MONO) induces an f with the stated endpoint/regularity properties; (ii) the response law μ(Y)g=B derived from the action rather than adopted.

**Affected operative gate:** gate 13 (framework a0–vacuum relation preserved as input or derived) is unaffected (the input stays an input); the conditional robustness result is evidence for the coefficient layer of the CORE group (A03) — it does not by itself close gate 1 (filtered MONO from the same action) or any propagation gate.

## 13. Follow-up and child specification

Suggested immediate continuation: **AS074.C01** — a quantitative drift bound `|kappa_eff − 1/2| <= eps*|f'(0)| / [2*(2 − eps*|f'(0)|)]` together with an extension of the premise class from C¹ to locally-Lipschitz f (slope read off the essential supremum of the a.e. derivative), plus the identification of the observable that first detects f''(0). Full ready-to-dispatch spec: `branches/AS074/AS074.C01.md` (created; **not dispatched** — no spawner available in this session; orchestrator may dispatch). Duplicate check against manifest/CATALOG_REGISTRY: closest neighbors AS075 ("constructive missing premise work order for kappa") and AS672 ("kappa rigidity as a functional equation") are distinct (AS075 constructs the missing premise for κ itself; AS672 is a functional-equation rigidity class; C01 is a quantitative Lipschitz drift bound + f''(0) observable probe). No claim file was created.

## 14. Limitations

- The identification is leading-order in Y (exact only for the linearized kernel); finite-B corrections are O(sqrt(B/s)) measured, not bounded.
- Nothing derives κ=1/2 from an action; the robustness theorem presupposes the adopted footing.
- The deformation is a *response-kernel* deformation; the mapping from an action-level kernel change (e.g. within the AQUAL/MONO action class) to f(Y) is not derived here.
- Residuals are finite-precision consistency checks (some at 1e-49 arithmetic-level); the exact identities (slopes, coefficient formula, iff) are proven symbolically and Lean-certified, not by the numerics.
- One thread, 120 s CPU, 60 MiB RSS — bounds enforced and recorded (see result.json).
