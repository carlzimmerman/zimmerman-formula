# A75 — IS THE THERMAL PREMISE DERIVED FROM THE ACTION, OR IS IT POSTULATED?

**Lane:** A75_thermal_premise · **Date:** 2026-10-22 · **Base:** `deepseek_push/DS_FINAL_2026_10_21`
**Script:** `a75_checks.py` — **24/24 PASS, exit 0** · `a75.out` · `a75_results.json`
**Mutations:** 16, each one input, each exit **1**, **24/24 checks killed** (`MUTATE.md`)
**Read first:** A72 (the derivation), A63 (the Langmuir gate), A33 `MASTER_ACTION.md`, A68 (the P
coefficients and the gapless `k⁴` mode), A65 (`L*`), A19 (`R`), A50 (horizon thermodynamics).
**Nothing fitted here. Every number quoted below is printed in `a75.out`.**

## Claim

**The thermal premise is a new postulate, not a consequence of the action.** It fixes the action's one free
acceleration `a0` by an external identification, and it competes with the theory's own selection of that
same parameter. Four obstructions, each computed:

1. **The action is classical** — it contains `G, Λ, a0, η, γ, β` and no `ħ`, no `k_B`. The premise needs
   both: `T_dS = ħH_Λ/2πk_B` and `λ_C = ħ/(mc)`. No functional of the action's own variables can produce a
   statement containing two constants it does not have.
2. **The gate is athermal at fixed drive.** `θ = g/(g+a0)` exactly, `dθ/dT|_g = 0`, heat capacity
   **`C_g = 0`** (K3, K6). A system with zero heat capacity cannot generate a thermal-wavelength
   condition. The only temperature-sensitive gate — linear (energetic) coupling — has `A(0) = a0/2 ≠ 0`
   and is excluded by A63 K16 (K7). **T-blind ⟹ no thermal condition; T-sensitive ⟹ wrong law.**
3. **The action's own carrier fails the literal condition by ×1.989424e+09** — `λ_C = L*/√2 = 16.988249 pc`
   against `λ_T = 2πc/H_Λ = 33.796833 Gpc`, and equality would require `L* = 47.795940 Gpc` (K8–K10).
4. **A72's formula never uses the carrier.** `a_sat = k_BT/(mλ_C) = k_BTc/ħ`: the mass cancels identically
   (spread 0 over four masses, K11), so no `η`, `γ`, `K` enters. It is the Gibbons–Hawking temperature
   rewritten as an acceleration, `a_Unruh(T_dS) = cH_Λ = 5.414953e-10`, divided by `2π` (K12) — which A72's
   own census labels **RESTATEMENT** (its route f). Mass-independence is not a virtue here: it is the
   proof that the carrier drops out.

**Forced by the action:** the isotherm, the law `g_N = g²/(g+a0)`, `λ_C = √(η/K)`, `m_T² = K/η`,
`L* = √(2γ/K)`, the gapless `k⁴` fifth mode. **Not forced:** any relation between `λ_C` and `1/T_dS`,
because `a0` is one of the action's free parameters (A33 §2 row 13, status **M**; A15
`DIFFERENT-QUANTITY`). The premise supplies that relation — a second selection rule, giving
`κ = 0.460658866` against the theory's `κ = ½` (a0 **7.87%** lower, `0.078682`) and `R = 3π/2` against
`R = 4` (K20, K21).

## 1. Task 1 — the gate's thermodynamics

`N_s` sites, at most one occupant, energy `−ε` when occupied, drive `g`, temperature `T`:

```
(1.1)  Z₁ = 1 + z,  z = e^{(μ+ε)/k_BT},  Ω = −k_B T ln(1+z),  θ = −∂Ω/∂μ = z/(1+z)               [K1]
(1.2)  μ(g,T) = k_B T ln(g/a0) − ε   ⟹   θ = g/(g+a0)   exactly, for every T                   [K2]
(1.3)  F = Ω + μθ = k_B T[θ lnθ + (1−θ)ln(1−θ)] − εθ = U − T S,   U = −εθ                      [K5]
(1.4)  S = −k_B[θ lnθ + (1−θ)ln(1−θ)],  C_g = T ∂S/∂T|_g = 0,  C_μ = εθ(1−θ)(μ+ε)/(k_BT²)    [K6]
(1.5)  ∂θ/∂T|_g = 0;   ∂θ/∂T|_μ = −θ(1−θ)(μ+ε)/(k_BT²) = −0.0550 at the sample point         [K3,K4]
(1.6)  ∂θ/∂T|_g = −g a0′(T)/(g+a0)²       (a0 temperature-dependent)                           [K3b]
```

`F = −TS + U` and `Ω = U − TS − μN` are checked as identities (K5); `C_g = 0` (`0.0e+00`) and `C_μ ≠ 0`
are two independent finite differences (K6). **The canonical gate has no temperature dependence at fixed
drive — identically**, because its drive is an *activity* `z = g/a0`, not an energy: its entropy and heat
capacity depend on `g` alone. Two exact consequences:

- **The gate cannot produce a thermal-wavelength condition.** Such a condition needs a temperature; the
  gate has none. The only place `T` can enter is through the affinity, `a0 = a0(T)` (1.6) — and the
  action's `a0` is a constant of the Lagrangian, not a function of a state variable. Making the gate
  thermal means *postulating* `a0 = a0(T_dS)`; that is the premise, not its consequence.
- **The one T-sensitive gate is excluded.** A linear-coupling gate `θ_F = 1/(1+e^{−λg/k_BT})` has
  `∂θ/∂T = −0.1966` at the sample point, but `θ_F(0) = 0.5`, i.e. `A(0) = a0/2 ≠ 0` (K7) — the failure
  A63 K16 already excludes. No gate in this class is both thermal and admissible.

A third premise sits in (1.2): the chemical potential must be **logarithmic** in the drive — a heat bath
does not supply that, a rate-driven activity does (A63's (P1)). The gate is not a thermal-equilibrium system.

## 2. Task 2 — the carrier inside the action

A68: `m_T² = K/η`, so `λ_C = √(η/K)`. A65: `L* = √(2γ/K)`. Under `η = γ` (which A68 D10/D13 shows the
action does **not** force) `λ_C = L*/√2`:

```
(2.1)  λ_C = √(η/K) = L*/√2 = 16.988249 pc   (η = γ),   L* = 24.025012 pc                       [K8]
(2.2)  λ_T = 2πc/H_Λ = 33.796833 Gpc                                                               [K23]
(2.3)  λ_T/λ_C = 1.989424e+09 = m_Pc²/k_BT_dS;  m_Pc² = 6.031116e-44 J = 3.764327e-25 eV,
       k_BT_dS = 3.031589e-53 J                                                                    [K9]
(2.4)  λ_C = λ_T  ⟹  L* = 47.795940 Gpc = 1.989424e+09 L*,   η → 3.957809e+18 η                    [K10]
(2.5)  a_sat = k_BT_dS/(m_P λ_C) = k_BT_dS c/ħ = cH_Λ/2π = 8.618165899975e-11 m/s²,
       independent of m_P (spread 0 over m/10 … 10³m)                                              [K11]
(2.6)  a_Unruh(T_dS) = 2πk_BT_dS c/ħ = cH_Λ = 5.414953e-10 m/s² = 2π a0                             [K12]
(2.7)  ħ a0/c = k_BT_dS  ⟺  a0 = cH_Λ/2π;  ratio 1.000000000000, canonical a0: 1.085402             [K13]
```

**Erratum to the task's wording.** A68's mass is `m_P = √(K/η)`, not `√(γ/K)`; `√(γ/K) = L*/√2` is the
Compton *length* `λ_C` under `η = γ` — the two expressions in the prompt are the same number read as a mass
and as a length. This matters because `λ_C = L*/√2` holds only at `η = γ` (K8 fails at `η = 3γ`:
`29.4245 pc`, MUTATE `eta_three`).

**What the action forces and what it does not.** *Forced:* `λ_C = √(η/K)`, `m_T² = K/η`, `L* = √(2γ/K)` —
a definite carrier mass once `η` is chosen, and a definite Compton length. *Not forced:* that this length
equals `2πc/H_Λ`. That is (2.4), a statement about `η` and `Λ` jointly, false for the action's own `L*` by
`1.989424e+09` in length and `3.957809e+18` in stiffness. *Not used at all by A72:* the mass. (2.5) is
exact for any `m`, which is why it cannot test the P sector; the content is (2.7), one line, with `a0` on
one side and the Gibbons–Hawking temperature on the other: a definition of `a0` in thermal units. If the
carrier is not the P field at all, it is a field the action does not contain, and the premise is external
*a fortiori*.

The literal reading of the task — the acceleration at which the carrier's Compton wavelength equals its
thermal wavelength — has **no solution with the action's carrier**: the equality needs a stiffness
`3.957809e+18` times the measured one, i.e. `L* = 47.795940 Gpc`, the horizon, not 24 pc. A72's formula
survives only because it never imposes the equality; it divides the thermal energy by the Compton length,
and the mass cancels.

## 3. Task 3 — the alternative routes

**(a) The P sector's own stress at `T_dS`.** The gapless `k⁴` mode has `ω_p = A p²`,
`A = L*/√(2(2+3β))` (from `α = γ = KL*²/2`, `Q = K(2+3β)/β`). Its thermal energy density is

```
(3.1)  ρ_k4 = Γ(5/2)ζ(5/2)/(4π²) · T_dS^{5/2} A^{−3/2} = 3.582385e-121 J/m³                  [K14]
(3.2)  a0²/(8πG) = 4.427760e-12 J/m³;   log₁₀(ρ_k4/target) = −109.0920
```

— **109 orders of magnitude short**, quadrature and closed form agreeing to `4.4e-17`. The massive
transverse modes are worse: `m_Pc²/k_BT_dS = 1.989424e+09`, so their occupation is
`log₁₀ n = −8.639959e+08` (K15). **The P sector is in its vacuum at `T_dS`; the action has no thermal bath
to saturate anything.** This is the quantitative form of obstruction 3: the carrier the premise needs is
not populated, and cannot be, at the de Sitter temperature.

**(b) Horizon entropy per cell.** With `S = A/(4l_P²)` and cells of size `L*`, `S_cell = L*²/(4l_P²) =
5.259550e+104` (= `S_dS/N_cells` with `S_dS = 3.313016e+122`, two routes, K16), while `a0/a_Planck =
1.549827e-62` and `log₁₀(S_cell/(a0/a_P)) = 166.5307` (K16). They differ by **166.53 decades**; no
dimensionless combination equates them. Worse, the route is circular: since `S_dS = 3π/(Λl_P²)`,
`a0 = c²/(2 l_P √(π S_dS))` **exactly, for every `Λ`** (K17) — the entropy *is* `Λ` inverted, so it returns
`cH_Λ/2π` identically and tests nothing. (A50 K11 reaches the same conclusion from the first law: κ is not
in its domain.)

**(c) The gate's chemical potential at `T_dS`.** Half occupancy is `z = 1`, i.e. `μ = −ε` — a zero of the
shifted chemical potential, independent of `T`. Setting `μ = k_BT_dS` gives
`θ = 1/(1+e^{−1}) = 0.731059 ≠ 1/2` and the drive `g = e·a0 = 2.342660e-10 m/s²` (K18): the gate would be
73% occupied, half-occupancy at `g = e a0`, not `a0`. The route "works" only if `ε = −k_BT_dS`, a tuned
binding energy — the postulate rewritten as a site energy (MUTATE `mu_eps`: then `g = a0` and `θ = 0.5` by
construction, which is the point).

**(d) The per-site capacity.** A63's bookkeeping is `q = a0/N_s` with affinity `a0`. With one gate per
horizon cell of size `L*`, `N_cells = 6.299048e+17` and `q = a0/N_cells = 1.368170e-28 m/s²`,
`q/a0 = 1.5875e-18` (K19). If the carrier saturates the *per-site* capacity rather than the affinity,
`a0 = N_s × a_sat` with `N_s` unpredicted (`cell_one`: `q/a0 = 1`). The thermal route fixes one
acceleration per carrier; the gate's `a0` is a total capacity. Matching them assumes `N_s = 1`.

## 4. Task 4 — verdict

**(ii) Consistent with the action, but independent: a new postulate — and a rival of the theory's own
closure.** Name it:

> **P-therm.** The gate's affinity equals the acceleration whose Unruh temperature is `T_dS/2π`:
> `ħ a0/c = k_BT_dS`, equivalently `a0 = cH_Λ/2π`, equivalently `λ_T = 2πc/H_Λ` with `a0 = c²/λ_T`.

Not (i) forced: the four obstructions are independent, and the strongest is that A72's formula is
mass-independent, so no action coefficient can enter it. Not (iii) inconsistent with the *Lagrangian*:
any `a0` gives a consistent member of the family. But it **is inconsistent with the theory's selected
closure**, and that is what matters:

```
(4.1)  R ≡ Λc⁴/(8πa0²) = 1/κ²;  κ_th = 0.460658866  ⟹  R = 4.712388980 = 3π/2 ∉ {1,2,4}        [K20]
(4.2)  Λ_pred/Λ_obs = 32πa0²/(Λc⁴) = 0.848826363 = 8/(3π);  deviation 0.151174 (15.1%)           [K21]
(4.3)  a0_thermal/a0_closure = 0.921318;   κ = ½ is 0.085402 above κ_th
```

A19's saturation cap admits only `R ∈ {1,2,4}` and the data exclude `R = 1` and `R = 2`; the thermal value
`3π/2 = 4.712388980` is **not in that set**. Adopting P-therm is therefore not conservative: it *replaces*
`R = 4` with `R = 3π/2`, moves `a0` down by 7.87%, and predicts a `Λ` 15.1% below `32πa0²/c⁴`.

> **ERRATUM (2026-10-22, doors push D5):** "the data select 4 among the natural caps" is wrong. A19's own natural grid (`a19_checks.py` K6: β ∈ {1, 2}, χ ∈ {1…4}) is R ∈ {1, 2, 3, 4, 8, 12, 16}, not {1, 2, 4}. The data **exclude R = 1** (6.14σ) and, **on CFG493 only**, R = 2 (3.05σ; on the A81 joint band R = 2 is only +1.71σ). On CFG493 (κ = 0.417 ± 0.095) R = 3 (+1.69σ), 4 (+0.87σ), 8 (−0.67σ), 12 (−1.35σ), 16 (−1.76σ) and A19's 4π (−1.42σ) all lie within 2σ, and **R = 8 is closer to the data than R = 4**. The data do not select 4; κ = ½ stays FITTED. See `doors_push_2026_10_22/D5_kappa_four/README.md`.

**What would have to be added to make it forced.** Nothing local. The natural local route to a thermal
response — an Unruh–DeWitt detector coupling of the P sector to the horizon vacuum — gives saturation at
`T_U(a) = T_dS`, i.e. `a0 = a_Unruh = cH_Λ = 5.414953e-10`, **2π larger** and excluded at 16.7σ (A72's
route b). The `1/2π` that makes the thermal value correct is the statement that *one thermal wavelength
fits the horizon circumference once*, `λ_T = 2πc/H_Λ` — a global condition, not a Lagrangian term. To
force P-therm one must add (i) quantization (`ħ`), (ii) a `T_dS` bath, and (iii) the global `2π`
identification. With (i)+(ii) only, the prediction is `a0 = cH_Λ`, which is dead; with (iii) added, the
theory's `R = 4` closure is gone.

**The no-go, stated precisely.** The action has one dimensionful vacuum scale `Λ` and one free acceleration
`a0`; their ratio is the free dimensionless parameter `R^{-1/2}`, and no term in the action contains it.
So *no* functional of the action's classical variables can produce `a0/(cH_Λ) = 1/2π`: producing it is
choosing `R = 3π/2`, a selection on the same footing as `R = 4`. A72's derivation is a *rule for selecting*
`a0`, not a computation of it, and both of its inputs — `T_dS` and `λ_C = ħ/(mc)` — are outside the action.

## Status

**NO-GO(obstruction).** The premise is **not implied** by the action: the gate is athermal at fixed drive
(`C_g = 0`), the one thermal gate is excluded (`A(0) = a0/2`), the action's carrier misses the thermal
wavelength by `1.989424e+09`, the `k⁴` bath at `T_dS` is 109 orders short of `a0²/(8πG)`, and A72's formula
is mass-independent by construction. It is **consistent with the Lagrangian but independent** — and it
**conflicts with the theory's `R = 4` closure** at 15.1% in `Λ` (`0.151174`) / 7.87% in `a0`
(`0.078682`). `a0` remains a free parameter selected from outside (A33 §2 row 13; A15; A50 K11).

## Checks (`a75_checks.py`, 24/24 PASS, exit 0)

| id | proves | measured | id | proves | measured |
|---|---|---|---|---|---|
| K1 | `θ=−∂Ω/∂μ` = `z/(1+z)` | rel `8.65e-18` | K13 | `ħ a0/c = k_BT_dS` only thermal | `1.000000000000` |
| K2 | activity map gives `g/(g+a0)` | rel 0 | K14 | `k⁴` density vs `a0²/8πG` | `−109.0920` dex |
| K3 | `∂θ/∂T|_g = 0` | `0.0` | K15 | massive quanta suppressed | `log₁₀ n = −8.639959e+08` |
| K3b | `∂θ/∂T|_g = −g a0′/(g+a0)²` | rel `5.08e-18` | K16 | entropy/cell ≠ `a0/a_P` | `166.5307` dex |
| K4 | `∂θ/∂T|_μ ≠ 0` | `−0.0550` | K17 | entropy route circular | rel 0 |
| K5 | `F = Ω+μθ = U−TS` | sym 0 | K18 | `μ=k_BT` ≠ half occupancy | `0.731059` |
| K6 | `C_μ≠0`, `C_g=0` | `C_g = 0.0e+00` | K19 | `q = a0/N_s` | `1.5875e-18` |
| K7 | thermal gate `A(0)=a0/2` | `θ_F(0)=0.500000` | K20 | `R = 3π/2 ∉ {1,2,4}` | `4.712388980` |
| K8 | `λ_C = L*/√2` at `η=γ` | `16.988249` pc | K21 | closure violated | `0.848826363` |
| K9 | `λ_T/λ_C = m_Pc²/k_BT` | `1.989424e+09` | K22 | law homogeneous | rel `2.8e-16` |
| K10 | stiffness needed for equality | `47.795940` Gpc | K23 | `2π` convention | `6.283185307180` |

## What this does not do

1. **It does not show the premise is false** — only that it is not in the action and costs the `R = 4`
   closure; a universe with `R = 3π/2` is a consistent member of the family.
2. **It does not redo A72's statistics.** A72's data comparison stands; this lane tests the premise's
   origin only.
3. **`L* = 24.025012 pc` is an external input** (A65, fitted in normalisation); every `λ_C` inherits it.
   Moving `L*` across A65's footing range does not touch the `1.989424e+09` that decides the question.
4. **The `k⁴` density uses the quadratic dispersion at the peak momentum printed in `a75.out`**
   (`p_peak`), far inside A68's IR regime; an `O(H)` gap would move it by factors, not 109 decades. **The
   one-loop P-sector stress at `H ≠ 0` is not computed here** — the calculation that would turn P-therm
   into a derivation or a no-go.

## Next

1. **Compute the one-loop P-sector stress at `H ≠ 0`.** If the transverse modes acquire an `O(H²)` mass,
   the carrier's `λ_C` could track `1/H` — the only route by which the action could supply the relation.
2. **Decide `R`.** The thermal premise and `R = 4` cannot both hold; a measurement at A72's forecast
   precision separates them, and until then C5 should be relabelled `POSTULATE(P-therm)` — it derives the
   identity `a_sat = k_BTc/ħ`, i.e. `a0 = a_Unruh(T_dS)/2π`, with `κ = 0.460659` and `R = 3π/2`.

---

## VERDICT

**(1) The thermal premise is neither forced by the action nor inconsistent with its Lagrangian: it is an
independent new postulate — P-therm, `ħ a0/c = k_BT_dS`, equivalently `a0 = cH_Λ/2π` — and a rival of the
theory's own selection of the same free parameter.** The obstruction is structural and computed: the
Langmuir gate is athermal at fixed drive (`C_g = 0`, `∂θ/∂T|_g = 0` identically, K3/K6), so it cannot
generate a thermal condition; the only temperature-sensitive gate has `A(0) = a0/2` and is excluded (K7);
the action's own carrier has `λ_C = 16.988249 pc` against `λ_T = 33.796833 Gpc`, a ratio `1.989424e+09`
equal to `m_Pc²/k_BT_dS`, so the literal condition fails for it by nine orders (K8–K10); the gapless `k⁴`
bath at `T_dS` carries `3.582385e-121 J/m³` against `a0²/(8πG) = 4.427760e-12`, 109 decades short, and the
massive P quanta are suppressed by `e^{−1.989424e+09}` (K14, K15); and A72's `a_sat = k_BT/(mλ_C)` is
mass-independent by construction, so it uses no action coefficient — it is the Gibbons–Hawking temperature
rewritten as `a_Unruh(T_dS)/2π`, which A72's own census labels RESTATEMENT. **(2) What the action does
force** is the shape: the Langmuir isotherm, `g_N = g²/(g+a0)`, `λ_C = √(η/K)`, `m_T² = K/η`,
`L* = √(2γ/K)`, and the gapless fifth mode — but `a0` itself is a free parameter (A33 §2 row 13, status M;
A15 `DIFFERENT-QUANTITY`; A50 K11), and `a0/(cH_Λ) = R^{-1/2}` is exactly that parameter. **(3) The
obstruction** is that the premise fixes a free parameter from outside, to a value that is not the theory's:
`κ = 0.460658866`, `R = 3π/2 = 4.712388980`, `Λ_pred/Λ = 8/(3π) = 0.848826363` — 15.1% below the `R = 4`
closure, `a0` 7.87% lower, and `3π/2` outside A19's admissible `{1,2,4}`. **(4) What addition would force
it:** nothing local — the natural Unruh–DeWitt coupling gives `a0 = cH_Λ`, 2π too large and excluded at
16.7σ; forcing `1/2π` requires a global condition (one thermal wavelength per horizon circumference) plus
quantization and a `T_dS` bath, and that addition predicts the `R = 3π/2` closure above. **A72 derives the
identity `a_sat = k_BTc/ħ`, not a coefficient of the action; the honest label is POSTULATE(P-therm), and
the honest consequence is that `κ = ½` and `a0 = cH/2π` are two different theories 8.54% apart.**
