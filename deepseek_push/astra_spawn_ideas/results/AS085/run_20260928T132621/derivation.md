# AS085 — External Newtonian baryon virial term: derivation

**Run:** `run_20260928T132621` · **Seed:** `AS085_external_newtonian_baryon_virial_term.md`
(sha256 `3d50da7fc2ff74c47b6de56ce53b6f2a8d6317d4e69eaaaa7c0d9d964d558e33`, verified) ·
**Worker:** `deepseek/deepseek-v4-flash-0731 (OpenRouter)`, Hermes Agent subagent ·
**Branch (declared, per seed):** Conditional deep-equilibrium sector; no automatic
particle ontology. Q, RAR, MU2, EXP, MONO are distinct (framework contract); this
result uses **no interpolation branch** — the object is the virial bookkeeping of the
*external Newtonian well* on the equilibrium profile, a fixture that G091 already
quotes and that the seed asks to derive. No transfer to filtered MONO is claimed.

---

## 1. Claim, symbol dictionary, boundary conditions, assumptions

**Principal test (verbatim from the seed):**

```text
W_bar = -∫ rho · r · dPhi_b/dr dV ,   Phi_b(r) = -G_N M_b / r   (r > r_b)
```

**Symbols (SI):**

| Symbol | Meaning | Units |
|---|---|---|
| `G_N` | Newton's constant, `6.67430e-11` (separate from `G_bare`, `G_cosmo`; only `G_N` enters — the well is the measured Newtonian baryon well) | m³ kg⁻¹ s⁻² |
| `M_b` | baryon (point) mass at the origin | kg |
| `rho(r)` | phantom mass density (equilibrium profile) | kg m⁻³ |
| `Phi_b` | external Newtonian baryon potential, `-G_N M_b/r` for `r > r_b` | m² s⁻² |
| `C` | `sqrt(G_N M_b a0) = v_flat²` (framework input combo) | m² s⁻² |
| `r_M` | `sqrt(G_N M_b/a0)` | m |
| `A` | phantom density coefficient, `rho = A/r²` | kg m⁻¹ |
| `r_b` | baryonic inner edge (core radius) | m |
| `R` | shell outer edge | m |
| `r_break` | `λ r_M`, EFE-cap fixture, λ = 0.62 (G03B registered) | m |
| `W_bar` | baryon-coupling virial term | J = kg m² s⁻² |

**Boundary/domain conditions:** `0 < r_b ≤ r ≤ R < ∞`; the integral is
spherical over the shell `[r_in, R]`; the well is the *point-mass* Newtonian
well for all `r > 0` (no core below `r_b`: see NC1); `R ≤ r_M` fixtures test
the historical imposed-log-well ansatz only (seed instruction), and the deep
exterior is treated by separate shells (below).

**Assumptions (framework inputs, adopted, not derived here):**
1. `a0 = κ c sqrt(G_N rho_Lambda)` with `κ = 1/2` **adopted** (framework
   contract; the seed does not supply an independent derivation of κ — this
   result does not claim one). Footings carried **separately**:
   canonical `a0 = 9.3619e-11 m/s²` and alternative `a0 = 1.1279e-10 m/s²`;
   fixing κ = 1/2 per footing gives **different** vacuum densities
   `rho_Lambda = 4a0²/(G_N c²)` (5.8444e-27 vs 8.4831e-27 kg/m³) and
   `Lambda = 32πa0²/c⁴` (1.0908e-52 vs 1.5833e-52 m⁻²) — the two footings do
   not share a fixed density and fixed κ (contract).
2. Equilibrium phantom `rho(r) = A/r²`, `A = C/(4πG_N)` (equipartition
   normalization `M_ph(<r_M) = M_b`; G03E/A2 conditional deep-equilibrium
   input, inspected in G084/G091).
3. Isothermal fluid closure `P = σ²·rho` with surface term `3P_sV = σ² M_T`
   (G091 V1d) — cited as the G091 chain's closure when the virial consequence
   (Section 6) is drawn; the bare reading (no boundary term) is kept as the
   control NC3.
4. G091's quoted logarithmic expression is the comparison target, verbatim:
   `W_bar = -M_b C ln(r_break/r_b)`.

**Conclusions established (not inputs):** the closed form of `W_bar` and its
domain, the derivative identity, the divergence controls, the virial-chain
consequence. The κ = 1/2 normalization and `sigma² = C/2` remain framework
inputs/conditional targets; nothing here derives κ.

---

## 2. The integral over the allowed shell compared with G091

**Step 1 — general shell (any spherical ρ).** With `Phi_b = -G_N M_b/r`:

```text
dPhi_b/dr = +G_N M_b / r²   ⇒   r·dPhi_b/dr = G_N M_b / r = -Phi_b   (r ≠ 0).
```

Work form:  `W_work = -∫ rho r Phi_b' dV = -4π G_N M_b ∫_{r_in}^R rho(r) r dr`
Potential form: `W_pot = ∫ rho Phi_b dV = -4π G_N M_b ∫_{r_in}^R rho(r) r dr`.

The two representations are the **same integrand** (exact consequence of
`r·Phi_b' = -Phi_b`, the 1/r power-law identity — certified as `vthm_phi_deriv`
and `vthm_r_phi'_eq_neg_phi` in the Lean certificate).

**Step 2 — equilibrium profile `rho = A/r²`:**

```text
W_bar(r_in, R) = -4π G_N M_b A ∫_{r_in}^R dr/r = -4π G_N M_b A ln(R/r_in).
```

**Step 3 — coefficient bookkeeping** (`A = C/(4πG_N)` ⇒ `4πG_N A = C`):

```text
W_bar(r_in, R) = -M_b C ln(R/r_in) = -M_b sqrt(G_N M_b a0) ln(R/r_in).
```

**Comparison with G091** (quoted symbol-for-symbol): with `r_in = r_b`,
`R = r_break`,

```text
W_bar = -M_b C ln(r_break/r_b)     [G091 V1c verbatim]   ✓ exact match
```

**Domain stated explicitly:** the identity holds on **every finite shell
`0 < r_in < R < ∞`**; at the G091 boundary `r_b ≤ r ≤ r_break` with
`0 < r_b < r_break`. The integral is improper at `r ≤ r_b` (no baryonic
inside edge) and, on the deep exterior, at `R → ∞` — both limits diverge
(Section 5, NC1/NC2).

**Units/signs:** `4π` (solid angle), `G_N M_b` (source), `A` (density
coefficient): `(m³kg⁻¹s⁻²)·kg·kg·m⁻¹·(dimensionless log) = kg m² s⁻² = J`.
Sign negative: the phantom–baryon coupling is binding. The log is the 1/r
well's bookkeeping; every scale factor and sign verified symbolically
(residual 0, checks 1b–1d) and in Lean (`vthm_wbar_shell_integral`,
`vthm_wbar_coefficient`).

---

## 3. Intermediate algebra: limits and leading neglected term

No limiting regime is needed: the closed form is exact on every finite shell.
For thin shells `Δ = R - r_in`, `ε = Δ/r_in → 0` the expansion is

```text
W_bar = -M_b C ln(1+ε) = -M_b C [ε - ε²/2 + O(ε³)],
leading neglected term = -(1/3) M_b C ε³    (verified exactly, check 1f).
```

Derivative identity (independent representation, exact):

```text
dW_bar/dR = -M_b C / R = 4π R² ρ(R) Phi_b(R)
```

(the rate of change of the virial term when the outer edge moves is the
surface integrand at the edge — the shell-theorem derivative; symbolic
residual 0, check 1e; numeric 4th-order central difference residual
≤ 1.3e-71 relative, check 2c).

---

## 4. Independent high-precision check (actual residuals)

50-digit (mpmath) quadrature of the **defining work-form integral** vs the
closed form, `M_b = 6.5e10 M_sun` (G031 MW proxy), both footings — interior
diagnostics `(r_in/R, R/r_M) ∈ {0.01, 0.1, 0.5} × {0.62, 1.0}` and deep
exterior `r_in/r_M ∈ {10, 100} × R/r_in ∈ {2, 10}`:

| check | measured max |rel residual| | threshold (pre-set) | result |
|---|---|---|---|
| interior shells, 12 runs | 2.4e-51 | 1e-40 | PASS |
| deep-exterior shells, 8 runs | 1.7e-51 | 1e-40 | PASS |
| 4th-order FD of dW/dR, 6 runs | 1.3e-71 | 1e-50 | PASS |
| uniform-density case (boundary) | symbolic 0 | 0 | PASS |

The closed form **is** the integral evaluated; residuals are computed values,
not booleans. (Input constants are decimal conventions, carried as exact
decimal strings in mpmath so the residual isolates the integration.)

---

## 5. Negative controls (capable of failing)

**NC1 — no baryonic core, `r_in → 0`.** The point-source integral with
`rho = A/r²` becomes `-4πG_NA M_b ∫₀^R dr/r`: **logarithmically divergent**.
sympy returns `oo` for the limit; measured per-decade growth of `|W_bar|` as
`r_in` decreases by a decade is constant and equal to `M_b C ln 10` to 50
digits (check NC1). There is no finite virial term without a positive inside
edge `r_b > 0`.

**NC2 — no outer edge, `R → ∞` (deep exterior).** Same rate: per decade of
`R`, `|W_bar|` grows by exactly `M_b C ln 10` (measured 50 digits). The
full-kernel error of any finite-`R` truncation is `-M_b C ln(R_max/R) → -∞`:
the `rho = A/r²` phantom has unbounded mass at infinity (`M_ph(<r) = 4πAr`),
so the deep-exterior virial bookkeeping **requires a physical outer edge**
(the registered EFE cap sits at `0.62 r_M ≤ r_M`; none is registered beyond
`r_M`). This is an explicit open dependency (child spec AS085.C01), not a pass.

**NC3 — bare vs fluid-closure reading.** Without the boundary term
`3P_sV = σ²M_T` (collisionless reading `2T + W = 0`):
`sigma² = (C/3)[1 + (1/λ)ln(r_break/r_b)]`; with it (G091 reading B):
`sigma² = (C/2)[1 + (1/λ)ln(r_break/r_b)]`. Ratio `= 2/3` **exactly** at every
(footing, λ, r_b/r_break) (symbolic: residual 0; numeric: diff to 2/3 = 0).
The check's assert fails the moment the boundary term is dropped: **the C/2
triad is not a bare-virial answer.**

**NC4 — well-consistent boundary `r_b = r_break`.** The log vanishes:
`sigma² = C/2` exactly for any λ, any M_b, both footings (symbolic residual 0);
registered anchors reproduced: σ = 119.203 km/s (canonical) and 124.9 km/s
(alt) (checks 3a–3c).

---

## 6. Virial-chain consequence (bridging to G091, fluid closure)

Inserting the derived term into the G091 closed chain
`2T + W_self + W_bar = 3P_sV` with `T = (3/2)λM_b σ²`,
`W_self = -G_N M_T²/r_break = -λM_b C`, `3P_sV = λM_b σ²`, `W_bar = -M_b C L`,
`L = ln(r_break/r_b)`:

```text
σ² = (C/2)[1 + L/λ]      →   r_b → r_break : σ² = C/2  (deep bookkeeping)
```

This **re-solves** G091's reading-B equation with the W_bar term derived here
(symbolic residual 0, check 3a); the honest limits: `L = 0 ⇒ σ² = C/2` (NC4);
`r_b → 0 ⇒ σ² → ∞` (no finite equilibrium, NC1's virial face). All identities
of this section certified in Lean (`vthm_virial_fluid`, `vthm_virial_bare`,
`vthm_virial_triad`, `vthm_ratio_bare_over_fluid`, `vthm_wself_bookkeeping`).

---

## 7. Dimensional examples (both footings, M_b = 6.5e10 Msun)

| footing | a0 [m/s²] | rho_Lambda [kg/m³] | C [m²/s²] | r_M [pc] | W_bar(r_b=0.3·r_break) [J] | W_bar/M_b c² |
|---|---|---|---|---|---|---|
| canonical | 9.3619e-11 | 5.8444e-27 | 2.8418e10 | 9837.5 | -4.4223e51 | -3.807e-7 |
| alt | 1.1279e-10 | 8.4831e-27 | 3.1193e10 | 8962.6 | -4.8540e51 | -4.179e-7 |

κ = 1/2 adopted per footing (density differs); G_N separate from G_bare/G_cosmo
(unused, never set equal).

---

## 8. Strongest surviving statement

> On `0 < r_b ≤ r ≤ R < ∞` the external-Newtonian baryon virial term of the
> equilibrium phantom is exactly `W_bar = -M_b C ln(R/r_b)`,
> `C = sqrt(G_N M_b a0)`: the virial (work) form and the potential form are
> the same integral, `dW_bar/dR = 4πR²ρ(R)Φ_b(R)`, and the G091 verbatim
> expression `-M_b C ln(r_break/r_b)` is reproduced on `[r_b, r_break]`. The
> term diverges logarithmically (rate `M_b C ln 10` per decade) as `r_b → 0`
> (no core) and as `R → ∞` (no edge); with the isothermal fluid closure it
> yields `σ² = (C/2)[1 + (1/λ)L] → C/2` at `r_b = r_break`; the bare reading
> gives `C/3`-scaled — the `C/2` triad is not a bare-virial consequence.

**First implication needed to transfer to the full theory (open):** a
physical outer edge `R_max` for the deep exterior (beyond the registered
`0.62 r_M` cap) that makes the virial bookkeeping finite, and the branch
bridge carrying the interior fixture to filtered MONO (S/S* filter metric,
measure, domain, BCs not supplied here). Without either, the deep-exterior
virial term is divergent — an open dependency, not a pass.

---

## 9. Lean certificate

`as085_lean_cert.lean` (in this run dir), compiled with
`cd fable_independent_2026/lean_2026 && lake env lean <abs path>` — **exit 0**,
zero `sorry`, and `#print axioms` for all 11 theorems ⊆
{propext, Classical.choice, Quot.sound} (see `lean_check.out`). Certified:
(1/2) 1/r-well derivative and the representation equivalence
`r·Phi_b' = -Phi_b`; (3/4) FTC log-shell integral `∫_{rb}^R dx/x = ln R - ln rb`
and its assembly into `W_bar = -(M_b C) L` with the `4πGA = C` bookkeeping;
(5) the coefficient substitution; (6) the per-decade log growth
`ln(R/(r/10)) - ln(R/r) = ln 10` (NC1/NC2 rate); (7–9) the virial solves
(fluid, bare, triad); (10) the 2/3 ratio; (11) `W_self` bookkeeping.
Scope: Lean certifies the mathematics, not the physical law (header states
which physical premises enter as hypotheses).

## 10. Iteration log (harness, not science)

- RLIMIT_AS lowering raises EINVAL on this macOS build; memory bound enforced
  by monitor-and-abort on ru_maxrss (512 MB ceiling), CPU/wall by RLIMIT_CPU
  + SIGALRM (120 s) — actual enforced mechanisms recorded in result.json.
- Precision failures in the first lane pass were float64 contamination of the
  high-precision checks and a 2nd-order FD truncation misestimate; fixed with
  exact-decimal mpmath constants and a 4th-order central difference
  (thresholds still set before evaluation). Anchor check 3c fixed an index
  bug. No science claim changed between passes; the same closed forms and
  controls survived all passes.

## 11. Limitations

- Fixture-only: `rho = A/r²`, the Newtonian well and the G091 chain are the
  conditional deep-equilibrium sector's bookkeeping; no dynamics, no
  attainment, no kernel, no filtered-MONO evaluation (transfer requires the
  branch bridge).
- `κ = 1/2` adopted, not derived; `σ² = C/2` remains the conditional target.
- The deep-exterior divergence (NC2) is open: no registered outer edge beyond
  `r_M`.
- Dimensional values use the G031 MW proxy `M_b = 6.5e10 M_sun`; both a0
  footings carried separately with separate rho_Lambda (no shared
  density+κ).
- Finite numerical residuals (≤ 2.4e-51; FD ≤ 1.3e-71) are consistency checks
  of identities proven symbolically; symbolic residuals are 0.
