# AS002 — Lambda conversion without a hidden Einstein factor

**Run:** `AS002-r1-20260927T200245-8f9004`
**Worker:** deepseek/deepseek-v4-flash-0731 (OpenRouter, Hermes subagent) — see `result.json`
**Task:** `deepseek_push/astra_spawn_ideas/AS002_lambda_conversion_without_a_hidden_einstein_factor.md`
(sha256 `92a2e2da0c4bc5062ae4dda7d30e08110e556fedcd18fee281ee99cfdf2902e3`)
**Branch:** CORE scale identities (Group A01 — scale, units and independent inputs). No branch
transfer is used; Q / RAR / MU2 / EXP / MONO are untouched by this derivation. The operative
filtered-MONO target is affected only through the scale dictionary this task pins.

---

## 0. Symbol dictionary and units

| symbol | meaning | SI unit |
|---|---|---|
| `G_E` | Einstein coupling: the coupling that multiplies matter stress in the Einstein field equations, `(8πG_E/c⁴)T_μν`; enters the vacuum-stress ↔ Λ relation | m³ kg⁻¹ s⁻² (same physical type as G_N; kept as a *separate symbol* — their equality is not assumed) |
| `G_N` | Newtonian scale coupling appearing in `a0 = (c/2)√(G_N ρ_Λ)` and in `r_M`, `v_flat⁴ = G_N M_b a0` (framework default `6.67430e-11`) | m³ kg⁻¹ s⁻² |
| `ρ_Λ` | vacuum mass density (`rho_Lambda`) | kg m⁻³ |
| `ε_Λ = ρ_Λ c²` | vacuum energy density | J m⁻³ |
| `Λ_eff` | effective cosmological constant (curvature scale, `Lambda`) | m⁻² |
| `a0` | galactic acceleration scale, `κ c √(G_N ρ_Λ)` with **κ = ½ adopted as an input** | m s⁻² |
| `κ` | the one-half normalization (adopted; NOT derived here — this task supplies no independent argument removing its freedom) | 1 |
| `c` | speed of light, `299792458` | m s⁻¹ |
| `l0 = c²/a0` | framework length scale | m |
| `M_b` | baryonic mass | kg |

Domain: all quantities real and **strictly positive** (`G_E, G_N, ρ_Λ, Λ_eff, a0, c > 0`; `κ > 0`
when the general-κ form is discussed). No boundary conditions, no dynamics, no limiting regime
are needed: the object of this task is an exact algebraic dictionary between two parametrizations
of the vacuum scale.

## 1. Claim (precise statement)

**Theorem (AS002-T).** Let `G_E, G_N, c, ρ_Λ, Λ_eff, a0 > 0` satisfy

- **P1 (Einstein vacuum stress, framework premise):**
  `ρ_Λ = Λ_eff c² / (8π G_E)`, equivalently `Λ_eff = 8π G_E ρ_Λ / c²`;
- **P2 (framework scale relation, κ = ½ adopted):**
  `a0² = G_N c² ρ_Λ / 4`.

Then, identically,

```
Λ_eff = 32π (G_E / G_N) a0² / c⁴        [m⁻²],          (T1)
```

and in the **same-G specialization** `G_E = G_N`,

```
Λ = 32π a0² / c⁴.                        [m⁻²]           (T2)
```

Conversely, given positive `(Λ_eff, G_E)` and `(G_N, κ=½)`, P1 and P2 determine `ρ_Λ` and `a0`
uniquely: the parametrizations `(ρ_Λ, G_N) → a0` and `(Λ_eff, G_E, G_N) → a0` give the *same*
prediction for every derived quantity, on both registered footings. T1 is exact; it is not a
numerical coincidence, and it contains no fitted input. General-κ form (cited for bookkeeping,
κ still adopted at ½):

```
Λ_eff(κ) = 8π (G_E/G_N) a0² / (κ² c⁴);   κ = ½  ⟹  T1.   (T3)
```

Framework inputs versus conclusions: **inputs** — P1 (the 8π Einstein convention, from the field
equations `R_μν − ½R g_μν + Λ g_μν = (8πG_E/c⁴)T_μν` with vacuum stress `T^vac_μν = −ρ_Λ c² g_μν`),
P2 with κ = ½ adopted, both couplings, both footings. **Conclusion** — T1/T2/T3 and the
equivalence-of-variables statement. The one-half normalization is *not* derived; the task's own
wording is respected: "The adopted one-half normalization is not a derived result unless an
independent argument removes its freedom."

## 2. Derivation of both directions

**Forward (density → Λ).** Start from P1 (vacuum stress in the Einstein convention):

```
ρ_Λ = Λ_eff c² / (8π G_E).            (P1)
```

Invert P2:

```
ρ_Λ = 4 a0² / (G_N c²).               (P2′)
```

Equate the two expressions of `ρ_Λ`:

```
Λ_eff c² / (8π G_E) = 4 a0² / (G_N c²)
Λ_eff = (8π G_E) · 4 a0² / (G_N c⁴) = 32π (G_E/G_N) a0² / c⁴.   ∎  (T1)
```

Every factor is carried: the `8π` is the Einstein coefficient of P1 **and is explicitly
retained**; the `4` is the κ = ½ (i.e. `4 = 1/κ²` at κ = ½) normalization of P2; the ratio
`G_E/G_N` is **not silently set to 1** — T1 is the asymmetric-coupling form, and T2 is its
specialization `G_E = G_N` (framework contract: "Lambda = 32 pi a0^2/c^4 [m^-2, when the
Einstein and scale G coincide]").

**Converse (Λ → density → scale).** Given `Λ_eff, G_E > 0`:

```
ρ_Λ = Λ_eff c² / (8π G_E);            (P1)
a0² = G_N c² ρ_Λ / 4
    = G_N Λ_eff c⁴ / (32π G_E),
a0 = c² √( Λ_eff / (32π (G_E/G_N)) ).               (T1′)
```

At `G_E = G_N`: `a0 = c² √(Λ/(32π))` — the form quoted in README.md (`a0 = c^2 sqrt(Lambda/(32 pi)) = 9.3619e-11`). Substituting T1 (or T1′) into any framework derived quantity is an exact rewrite: for example the deep-MOND law and MOND radius at same-G,

```
v_flat⁴ = G_N M_b a0,        r_M² = G_N M_b / a0,
v_flat⁴ = G_N M_b c² √(Λ/(32π)),   r_M² = M_b c² √(32π/Λ),
```

give the same numbers regardless of whether one first converts `a0 ↔ ρ_Λ` or `a0 ↔ Λ`
(verified numerically for `M_b ∈ {M_sun, 10¹⁰ M_sun, 10¹¹ M_sun}` on both footings — residuals
exactly 0 at 60-digit precision; see §5).

**General κ (T3).** If P2 is written `a0² = κ² G_N c² ρ_Λ`, the same two-line algebra gives
`Λ_eff = 8π (G_E/G_N) a0² / (κ² c⁴)`. T1 is the κ = ½ specialization (`1/κ² = 4`, so
`8π·4 = 32π`). This makes explicit exactly where the adopted normalization sits: the "32" in
T2 *contains* the κ = ½ input (`32 = 8π/κ²`) and the 8π from the Einstein convention — i.e. the
task's "no hidden Einstein factor" requirement is that the 8π arises **once, from P1**, and is
not double-counted or dropped when converting.

## 3. Boundary conditions and limiting regimes — status

The object is a pair of algebraic premises; there **are no** deep/Newtonian dynamical limiting
regimes *inside* the conversion (no field equation is solved, no radius/acceleration limit is
taken). In place of regime checks the controls exercise the permitted substitutes:

- **Boundary case** `G_E → G_N`: T1 → T2, which is the contract/README identity — checked
  symbolically (sympy) and numerically (κ_eff re-derived as exactly ½, both footings).
- **Normalization:** the adopted κ = ½ is witness-checked as `a0/(c√(G_N ρ_Λ)) = 0.5` exactly
  on both footings (consistent-by-construction — it is an input, not a test of physics).
- **Dimensionless witness:** `Λ·l0² = 32π` with `l0 = c²/a0` on both footings (README's
  `Lambda l0^2 = 32 pi`), residual 0 at 60 digits.
- **Degenerate/zero cases** (`a0 = 0`, `ρ_Λ = 0`, `G = 0`, `Λ = 0`) are excluded from the
  domain by P1/P2 positivity; the map is a bijection `(Λ_eff, G_E) ↔ (ρ_Λ ↔ (a0, G_N), κ=½)`
  on the positive orthant. No approximation error exists in the identity itself; the only
  "error" in the numerical work is floating-point representation (rel. ~10⁻¹⁶ in float64,
  exactly 0 at 60-digit mpmath and in sympy).

## 4. Approximation-error statement

Exact identity: relative error of T1 under its premises is **0 in exact arithmetic**. Finite
numerical evidence: float64 cross-representation residuals of order 10⁻¹⁶ (recorded — e.g.
`1.7e-16` for Λ on the canonical footing), mpmath-60-digit round-trip residuals exactly `0.0`.
This is a distinction the task demands ("Distinguish an exact identity from a finite numerical
consistency check"): the identity is **proved by algebra** (two-line substitution, §2),
**machine-certified** in Lean 4 (see the certificate file in this directory), and the numbers
here are finite witnesses of it, not evidence for a conjecture.

## 5. Numerical footings (both carried separately)

Constants: `G_N = 6.67430e-11`, `c = 299792458`, `M_sun = 1.98847e30`, `pc = 3.085677581491367e16`
(framework defaults). `G_E = G_N` in every number below (the same-G specialization is where both
footings live).

### Canonical footing — `a0 = 9.3619e-11 m/s²` (κ = ½)

```
ρ_Λ        = 4 a0²/(G_N c²) = 5.84441245402187536367003e-27 kg/m³
ε_Λ = ρ_Λ c²               = 5.25269595972611359992808e-10 J/m³
Λ  = 32π a0²/c⁴            = 1.09079976328073499027074e-52 m⁻²
l0 = c²/a0                 = 9.60013649725822365118192e+26 m
Λ l0²                       = 100.5309649148733836308... = 32π   (witness, residual 0)
round trip Λ → a0           = 9.3619e-11 m/s²  (rel. residual 0.0 at 60 digits)
```

### Alternative footing — `a0 = 1.1279e-10 m/s²` (κ = ½)

```
ρ_Λ = 8.48308961955909742997038e-27 kg/m³   ( = 1.45149 × canonical ρ_Λ )
ε_Λ = 7.62422072726727896558441e-10 J/m³
Λ   = 1.58328184769652276439212e-52 m⁻²     ( = 1.45149 × canonical Λ )
l0  = 7.96839417268213174926855e+26 m
Λ l0² = 32π  (witness, residual 0) · round trip exact 0.0
```

### Footing compatibility (contract requirement)

The two footings **cannot** share both a fixed `ρ_Λ` and a fixed `κ`:
at fixed κ = ½, `ρ_Λ(alt)/ρ_Λ(can) = (a0_alt/a0_can)² = 1.4514871573996111432795`.
Equivalently, holding the canonical density fixed and raising the scale to the alternative value
would require `κ_eff = (1/2)·(a0_alt/a0_can) = 0.6023884040632777534475`. Both readings are
recorded in the raw output; every dimensional number above is quoted on both footings
separately as the contract demands.

## 6. The negative control (task-mandated, must be capable of failing)

**Control K1 — remove the `8π` from the density definition.** Keep P2 and Λ_eff fixed; replace
P1 by `ρ' = Λ_eff c² / G_E` (the 8π dropped — this is exactly the "hidden Einstein factor" an
inconsistent convention would introduce). Reconstructing the scale with κ = ½:

```
a0′² = G_N c² ρ′/4 = G_N Λ_eff c⁴/(4 G_E)   (same-G: = Λ c⁴/4)
a0²  = G_N Λ_eff c⁴/(32π G_E)               (correct)
⇒  a0′/a0 = √(8π) = 5.01325654926200100483153...          (exactly, not ~)
```

Numerically (canonical footing): `a0′ = 4.69336064885359272071323e-10 m/s²` vs
`a0 = 9.3619e-11 m/s²` — ratio `5.0132565... = √(8π)` to all printed digits (residual 0.0).
Equivalently, on the Λ side, the density-derived constant without the 8π would read
`Λ′ = 4 a0²/c⁴ = Λ/(8π) = 4.34015435623995702194869e-54 m⁻²` — a factor-8π miss.

**Verdict: the control is live.** The reconstruction *changes* by the full √(8π) ≈ 5.013 factor
in `a0` (8π ≈ 25.13 in Λ). If the 8π were a null factor of the convention, the ratio would be 1
and the control would fail flat — it does not. This is a *symbolically* checked identity
(sympy difference ≡ 0; Lean-certified `a0sq_wrong_einstein_factor`), and the float64/mpmath
numbers are saved in `result_checks_raw.json`.

**Control K2 — coupling ratio must be carried (second task control).** At fixed `Λ_eff`, a
candidate action with `G_E ≠ G_N` shifts the inferred scale:

```
a0(G_E/G_N) = a0_sameG · √(G_N/G_E).
```

Witnessed for `G_E/G_N = 1.05` and `0.95` (canonical Λ): `a0 = 9.1362789e-11` and
`9.6051067e-11 m/s²` respectively, each matching `a0_sameG·(G_N/G_E)^½` to exactly 0.0
residual. `G_E = G_N` is therefore a **specialization to be declared**, never a silent
identification — this is precisely the contract's directive ("Enforcing the framework identity
is a matching condition on the candidate, not permission to set distinct couplings equal").

## 7. Independent check in a different representation (task step 4)

1. **Symbolic:** sympy derives `a0² = G_N Λ c⁴/(32π G_E)` from P1+P2 by substitution; the
   difference between T1's RHS evaluated on that `a0²` and `Λ` simplifies to `0`; the K1 and T3
   differences simplify to `0`. Full transcript in `result_checks_raw.json` → `symbolic_sympy`.
2. **High-precision:** all round trips and witnesses repeated at mpmath 60 digits — residuals
   exactly `0.0`; float64 cross-representation residuals recorded (~10⁻¹⁶, e.g. `1.7e-16`).
3. **Lean 4:** the identity, its converse-direction specialization, and the negative-control
   ratio are machine-certified (zero `sorry`, axioms ⊆ {propext, Classical.choice, Quot.sound});
   see `AS002_lambda_conversion.lean` and its `#print axioms` output in this directory.
4. **Equivalent variables:** `v_flat⁴` and `r_M` computed via `ρ_Λ` and via `Λ` agree with
   residual exactly 0 for `M_b = M_sun, 10¹⁰ M_sun, 10¹¹ M_sun` (canonical; same-G).

## 8. Strongest surviving statement and the first implication needed to transfer it

**Surviving statement (scoped).** For every positive `G_E, G_N, ρ_Λ, Λ_eff, a0, c`, the two
framework premises P1 (`ρ_Λ = Λ_eff c²/(8πG_E)`) and P2 (`a0² = G_N c² ρ_Λ/4`, κ = ½ adopted)
entail, exactly and dimensionally, `Λ_eff = 32π(G_E/G_N) a0²/c⁴`; the same-G specialization is
`Λ = 32π a0²/c⁴` = README/framework identity; the 8π lives once in P1 and was not hidden —
removing it changes the reconstructed scale by exactly √(8π) (a0) / 8π (Λ); and both registered
footings render the identity with zero residual. Domain: positive reals; no dynamics assumed;
no data fitted.

**First implication needed to transfer to the full theory (operative MONO target).** The
identity is a *dictionary*, not a mechanism. Before any MONO-branch prediction can use
`a0 = c²√(Λ/32π)` as a *derived* vacuum input, two premises must be supplied independently:
(i) **κ = ½** — adopted here, known underivable in the action class (zero-mode no-go,
`kappa_closure/k01`, README rev. 8–9): this task neither derives it nor claims to; and
(ii) **G_E = G_N** — the ratio of the Einstein coupling of the vacuum-stress term to the Newton
coupling entering `a0` must be derived or bounded, not assumed. The measured-value comparison
below shows the numerics are close, but matching `Λ` to the observed value is *not* evidence
that `G_E = G_N`; T1 predicts `Λ ∝ a0²` at any fixed ratio, so the ratio is a genuine free
degree of the framework cell. The transfer statement is therefore a **conditional theorem**:
filtered-MONO, criterion B, with the scale dictionary T1-T3, all other framework cell
components as declared, and `G_E/G_N = 1` + `κ = ½` as explicit listed conditions.

**Observational comparison (explicitly NOT a fit, NOT part of the claim).** Planck 2018
(arXiv:1807.06209, A&A 641 A6; TT,TE,EE+lowE+lensing row, `H0 = 67.39 ± 0.54 km/s/Mpc`,
`Ω_Λ = 0.6858 ± 0.0074`): `Λ_obs = 3H0²Ω_Λ/c²`:
`Λ_can/Λ_obs = 0.99903`, `Λ_alt/Λ_obs = 1.45008`. The canonical footing's implied Λ sits 0.1%
from the Planck value (the known near-coincidence); the alternative lies 45% above. This
category-level agreement is a cross-check of the *adopted* κ, not an output of this derivation
and not evidence about `G_E/G_N`.

## 9. Branch discipline and closure implication

No historical branch (Q, RAR, MU2, EXP, MONO) is used, translated, or identified with another.
The result lives in the CORE scale-identity lane:

- **Gate:** A01 common scale/units/independent-inputs gate (the vacuum-scale dictionary).
- **Closure implication:** for the operative filtered-MONO target, specifying the vacuum scale
  as `(ρ_Λ, G_N, κ=½)` or as `(Λ_eff, G_E, G_N, κ=½)` are exactly equivalent under T1;
  equivalently, any MONO-branch observable quoted in `a0` units is quoted in `Λ` units by T1′
  with no added independent input, at both footings, with the two explicit listed conditions. A
  conversion pass in either direction **cannot** be the source of an 8π discrepancy in any
  future lane — that freedom is closed by K1.
- **Not closed by this result:** κ = ½ (adopted; underivable in this task's premises), the
  physical origin of `ρ_Λ`, the value of `G_E/G_N`, and everything dynamic (criterion-B
  well-posedness, filters, the MONO kernel itself).

## 10. Files in this run directory

- `derivation.md` (this document)
- `result.json` (RESULT_CONTRACT.json schema_version 2)
- `checks_AS002.py` (the bounded verification script, rerunnable)
- `result_checks_raw.json` (full numeric output, residuals, bounds, symbolic transcript)
- `stderr_time.txt` (wall-time record from `/usr/bin/time -p`)
- `AS002_lambda_conversion.lean` (Lean 4 certificate) + `lean_compile_and_axioms.txt`
  (compile log with unfiltered `#print axioms` output)