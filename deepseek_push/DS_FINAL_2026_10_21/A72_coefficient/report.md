# A72 — THE COEFFICIENT a0/(cH): IS IT 1/7 OR 1/(2π)?

**Lane:** A72_coefficient · **Date:** 2026-10-22 · **Base:** `deepseek_push/DS_FINAL_2026_10_21`
**Script:** `a72_checks.py` — **22/22 PASS, exit 0, 1.2 s** · `a72.out` · `a72_results.json`
**Mutations:** 12, each changes one input, each exit **1**, **22/22 checks killed** (`MUTATE.md`).
**Read first:** A62 (1/Z; 1/7 ⟺ Ω_Λ = 32π/147; the 223-hit look-elsewhere), A71 (κ_P3 = 0.3777 ± 0.1207,
the κ_DE/κ_P3 trap, the wide-binary forecast), A65 (`L*`), A69 (P-sector). Constants: BRIEF §4 + CODATA
ħ, measured numbers from A71. **Nothing fitted in this lane.**

## Claim

**Neither 1/7 nor 1/(2π) is a coefficient of the theory; only one of them is a coefficient at all.**
`a0 = κc√(Gρ_Λ)` gives `a0/(cH_Λ) = 2κ/Z = 1/Z = 0.172747` at κ = ½ — a pure number in the *de Sitter*
frame. `a0/(cH0) = √Ω_Λ/Z = 0.142848`, which equals **1/7 = 0.142857 to 6.12e-5** *only because*
Ω_Λ = 0.683800 sits 0.11σ from 32π/147 = 0.683884: "1/7" is a **measurement of Ω_Λ wearing a
coefficient's clothes**, and exact 1/7 ⟺ Ω_Λ = (8π/3)(2/7)², an irrational number no cell count can
produce (closest p/q with q ≤ 1000: 331/484, |Δ| = 1.825e-7). The thermal value **1/(2π) = 0.159155**
is, by contrast, **derived with zero free parameters** from a quantum carrier at the Gibbons–Hawking
temperature: `a_sat = k_B T_dS/(mℓ)` with `ℓ = ħ/mc` is *exactly* `cH_Λ/2π`, mass-independent (C5,
symbolic residual 0) — but its response is analytic (slope 1, A62 K15), so it derives the *scale*, not
the *law*. The record's companion **1.0422e-10 = cH0/2π is the same coefficient attached to
the wrong H**: it is `cH_Λ/2π × 1/√Ω_Λ = 8.618166e-11 × 1.2093`, a 20.9% error of the same kind as A71's
κ_DE/κ_P3 trap, and it lands at κ_DE = 0.557076 — **outside the falsifier band [0.3415, 0.5265]**.
Correctly attached, the thermal value is a0 = 8.618166e-11, **0.027σ** from the joint fit against
**0.297σ** for 1/7: the data prefer it by a likelihood ratio of **1.045** — i.e. not at all. The
look-elsewhere settles that matching cannot decide: in **9,217,780** closed forms (582,481 distinct
values) there are **540** within 1% and **5** within 0.01% of 1/7, **564 / 4** of 1/(2π), and
P(≥1 hit at 0.01%) = **0.9963** for a random coefficient — while **0 of the 540** near 1/7 and **1 of
the 564** near 1/(2π) is the output of any stated premise. Only the derivation discriminates.

## 0. The frame trap — the candidates are not coefficients of the same H

Symbols: Λ > 0; `H_Λ = c√(Λ/3)`; `ρ_Λ = Λc²/8πG`; `Z := 2√(8π/3) = 5.788810`; `a0 = κc√(Gρ_Λ)`;
`T_dS = ħH_Λ/2πk_B`; `Ω_Λ = (H_Λ/H0)² = 0.683800`; κ_P3, κ_DE are A71's two conventions.

```
(0.1) a0/(cH_Λ) = κ√(3/8π) = 2κ/Z  → κ=½: 1/Z = 0.172747 [C1]   (0.2) a0/(cH0) = κ√(3Ω_Λ/8π) = 0.142848 [C2]
(0.3) a0/(cH0) = 1/7 ⟺ Ω_Λ = 32π/147 = (8π/3)(2/7)² = 0.683884 [C3]  (0.4) 1/(2π)×cH_Λ ⟹ a0/(cH0) = 0.131609 [C15]
```

`a0/(cH0)` is **not** a pure number: it carries `√Ω_Λ`, i.e. it is a statement about cosmological
parameters. `a0/(cH_Λ)` is one. The candidates therefore live in different frames: the task's "11%" is
the ratio `7/(2π) = 1.11408`, while the a0 values are **8.55%** apart when each is attached to its own
horizon and **10.24%** apart when 1/(2π) is attached to cH0 as the record does.

| reading | a0 (m/s²) | coefficient | κ_P3 | κ_DE |
|---|---|---|---|---|
| 1/7 × cH0 (= κ = ½ closure) | 9.354746e-11 | 1/7 = 0.142857 (cH0) | 0.413461 | 0.500000 |
| 1/(2π) × cH_Λ (thermal, dS horizon) | 8.618166e-11 | 1/(2π) = 0.159155 (cH_Λ) | 0.380929 | 0.460659 |
| 1/(2π) × cH0 (thermal, apparent horizon) | 1.042198e-10 | 1/(2π) = 0.159155 (cH0) | 0.460659 | 0.557076 |

**The third row is the record's 1.0422e-10, and it is the only one outside the falsifier band.** The
coincidence that hides the trap: κ_DE of row 2 equals κ_P3 of row 3, both `Z/4π = √(2/3π) = 0.460659`
(exact: `Z_over_4pi_minus_sqrt` = 0) — 0.461 in the record is *one number in two conventions*, standing
for two a0's 20.9% apart.

## 1. Task 1 — every structural derivation of a coefficient of order 0.1

`DERIVATION` = a symmetry, conservation law or exact identity forces the number with no free parameter;
`MATCH` = a number that happens to agree.

| # | route (premise) | coefficient | a0 (m/s²) | κ_DE | label |
|---|---|---|---|---|---|
| **a** | thermal wavelength of the dS horizon, `λ_T = 2πc/H_Λ` (one wavelength = one circumference) | **1/(2π) = 0.159155** (cH_Λ) | 8.618166e-11 | 0.460659 | **DERIVATION(premise)**; the same number follows from a quantum carrier with *no* geometric premise (C5) |
| a′ | the same words with the de Broglie wavelength `λ_T = 2π/T_dS = 4π²c/H_Λ` | 1/(4π²) = 0.025330 | 1.371624e-11 | 0.073316 | the coefficient is convention-fixed only at the 2π level |
| **b** | Unruh matching `T_U(a) = T_dS` ⟹ `a = 2πck_BT_dS/ħ` | **1.000000** (cH_Λ) | 5.414953e-10 | 2.894405 | **DERIVATION**, dead: 16.7σ (cH_Λ) / 20.9σ (cH0) |
| **c** | Friedmann coefficient with the observed vacuum, `a0 = c²√(Λ/32π)` | 1/Z = 0.172747 (cH_Λ); 0.142848 (cH0); **= 1/7 to 6.12e-5** | 9.354173e-11 | 0.500000 | Λ-relation **DERIVED given κ=½**; the *1/7* is a **MATCH** (it is Ω_Λ = 32π/147) |
| **d** | horizon equipartition `N_surf = N_bulk` (Padmanabhan) | **1.000000** (cH_Λ) — it is Friedmann identically (C7) | 5.414953e-10 | 2.894405 | **DERIVATION of Friedmann only**; no independent acceleration |
| d′ | the same with the measured deficit `ΔN/N_sur` at Ω_m = 0.3162 | 0.474300 (cH0) | 3.105869e-10 | 1.660152 | a *choice* of normalisation, not a derivation |
| **e** | surface gravity of the dS horizon divided by 2π, `cH_Λ/2π` | 0.159155 (cH_Λ) | 8.618166e-11 | 0.460659 | **NOT A DERIVATION** — the 2π is inserted; identical to (a) (C8, residual 0) |
| **f** | acceleration at which `T_U = T_dS/2π` | 0.159155 (cH_Λ) | 8.618166e-11 | 0.460659 | **RESTATEMENT** — the 2π that defines the answer is the unknown (C8 proves e ≡ f) |
| **g** | any cell-count or mode-count derivation of 7 or 2π | 1/7 needs Ω_Λ = 32π/147 ∉ ℚ; 2π needs a geometric premise | — | — | **NO-GO**: a pure count gives Ω_Λ ∈ ℚ (C10), so no count can give 1/7 |
| — | Verlinde volume law `cH0/6` (completeness) | 0.166667 (cH0) | 1.091387e-10 | 0.583369 | quoted, not re-derived (A62 K13); 4.07σ stat off |

**Reading of the census.** Four entries land at a coefficient of order 0.1: 1/Z (the theory's), 1/(2π)
(thermal), 1/(2π) again (surface gravity over 2π — the same number), and 1/7, which is not a route at
all but 1/Z in the cH0 frame; two routes give exactly 1 and are dead. **Exactly one produces a
coefficient of order 0.1 with no free parameter and no frame dependence: the thermal one.**
It also answers "is κ = ½?": no — κ = Z/4π = 0.460659, so κ = ½ is an **8.54%** approximation
(0.5/0.460659 = 1.08540). The caveat, in the same breath: that mechanism's response is **analytic**
(`d lnA/d ln x = 1`, A62 K15) — Newton with a renormalised G, not √(a0g_N): it derives the *scale* and
fails the *shape*, and the theory's gate (Langmuir, A63) has its scale at a0 itself, an input.
**1/(2π) is derived as a scale, not as the MOND scale of this theory; 1/7 is not derived.**

## 2. Task 2 — the look-elsewhere, done honestly

Pool (independent of A62's): all closed forms with ≤ 3 binary operations from `{+,-,*,/ ,^}` over
`{1,2,3,4,5,7,8,π,e,√2,√3}`, all five tree shapes: **9,217,780 forms → 582,481 distinct values** in the
coefficient band [1e-3, 1e3] (deduplicated at 1e-11). Counts, with A62's 156,210-value pool:

| window | 1/7 | 1/(2π) | 1/Z | A62's 2Z pool |
|---|---|---|---|---|
| 1 % | **540** | **564** | 611 | 223 |
| 0.1 % | 42 | 49 | 64 | 37 |
| 0.01 % | **5** | **4** | 11 | 18 |
| 0.001 % | 1 | 3 | 0 | — |

**Probability that at least one hit occurs** (3,000 random targets log-uniform in [0.10, 0.25], C22):
P(≥1) = **1.0000** at 1%, **1.0000** at 0.1%, **0.9963** at 0.01%, **0.4323** at 0.001%; mean counts
582.3 / 58.28 / 5.87 / 0.578 — a 0.01% match is the *expected* event. The calibration agrees: the
density near each candidate is typical (z = **−0.53** for 1/7, **−0.22** for 1/(2π), against 581.8 ± 79.5
hits for random targets, C12), and **2178** closed forms lie strictly *between* the candidates (C19).

**The decisive test.** Of the 540 pool values within 1% of 1/7, **0** coincide (to 1e-9) with the output
of any stated premise; of the 564 within 1% of 1/(2π), **1** does — the thermal value itself (C21). Of
the seven distinct route outputs, **0 produce 1/7 exactly** and **3 produce 1/(2π) exactly** (C13), and
only one of the three is a derivation rather than a restatement. Description length cuts the other way
on simplicity: 1/7 is the *simpler* number (3 symbols) than 1/(2π) (5), and no ≤ 2-operation rival lies
within 0.01% of either — the closest are `(π−2)/8 = 0.142699` (0.11% from 1/7) and `(√3/4)/e = 0.159296` (0.089%).

## 3. Task 3 — the deciding observable

Current: a0 = 8.544e-11 ± 2.73e-11 (31.9%); the candidates differ by Δa0 = **7.365804e-12** (8.55%),
so the present separation is **0.270σ**; Δχ² = **0.0875**, likelihood ratio **0.957** (the thermal value
favoured by 1.045, C17). On the statistical error alone (σ_a0 = 5.835e-12) the odds are still only
**2.6 : 1** (χ² = 1.931 vs 0.0162, `a72_results.json`). Nothing is decided.

| forecast (A71 §8) | σ(κ_P3) | σ(a0)/a0 | separation |
|---|---|---|---|
| current joint | 0.12069 | 32.0 % | **0.270σ** |
| wide binary, full DR4 catalogue (~30,000 pairs) | 0.040 | 10.6 % | **0.814σ** |
| wide binary + joint | 0.0605 | 16.0 % | **0.538σ** |
| SPARC at N = 1000 | 0.118 | 31.2 % | **0.276σ** |
| **required for 3σ** | **0.01085** | **2.874 %** | 3σ |
| required for 5σ | 0.00651 | 1.724 % | 5σ |

**No measurement in the record's forecast set decides the coefficient** — A71's "single most valuable
next measurement", the wide-binary γ_v at 18–22 kAU, reaches **0.814σ**, not 3σ; SPARC at N = 1000 is
worth 0.276σ and should not be bought. What decides it is a **wide-binary γ_v at 18–22 kAU to
σ(γ_v) = 0.00553 (0.47% of 1.1811), needing ≈ 4.08 × 10⁵ pairs** (13.6× A71's 30,000-pair catalogue,
N ∝ σ⁻²), i.e. σ(a0)/a0 = **2.874%** or σ(κ_P3) = **0.01085**. On the record's own pairing (1/7 against
cH0/2π, Δκ_P3 = 0.047172) the requirement relaxes to σ(a0)/a0 = **4.164%**, σ(κ_P3) = **0.01572**,
≈ **1.94 × 10⁵ pairs** — still a **factor 3.7 beyond the best forecast on the table**. It is a *local*
measurement: Ω_Λ would need 0.00027 (26.8× Planck's 0.0073) to test Ω_Λ = 32π/147 at 3σ.

## 4. Task 4 — verdict

- **1/7 or 1/(2π)?** The theory's own coefficient is **1/Z = 0.172747 × cH_Λ** (κ = ½); the only
  order-0.1 coefficient with a derivation is **1/(2π) = 0.159155 × cH_Λ**. They differ by **8.54%**.
  "1/7" is neither: it is 0.142848 × cH0, and it is 1/7 only because Ω_Λ = 0.683800 ≈ 32π/147.
- **Derived or matched?** **1/(2π): derived, as a scale** (quantum carrier at T_dS, zero free
  parameters, mass-independent, exact — C5), from a premise whose response is analytic and therefore the
  wrong shape for MOND. **1/7: matched.** It requires Ω_Λ = 32π/147 = (8π/3)(2/7)², irrational and
  unreachable by any cell count (C10); the only "route" within 6.12e-5 of it is the closure itself.
- **What decides it:** a 2.874% measurement of a0, σ(κ_P3) = 0.01085 — a wide-binary γ_v at 18–22 kAU
  with ≈ 4.08 × 10⁵ pairs (σ(γ_v) = 0.00553). Nothing current or forecast does.
- **What κ follows:** if 1/7 — κ = ½ identically and Ω_Λ = 32π/147 = 0.683884 is a *prediction*
  (0.11σ from Planck). If 1/(2π) — **κ_DE = Z/4π = 0.460659**, **κ_P3 = 0.380929**, and κ = ½ is an
  8.54% approximation (the task's "8–11%" is right; 8.54% is frame-correct). Both cannot hold: for
  a0 = cH_Λ/2π to *also* give a0/(cH0) = 1/7, Ω_Λ would be (2π/7)² = 0.805682 — **16.6σ** from Planck.

**The evidence points, weakly, at 1/(2π) attached to cH_Λ**: 0.027σ from the joint fit against 0.297σ
for 1/7 (likelihood ratio 1.045 — no evidence), the only candidate with a derivation, and
κ_P3 = 0.380929 sits 0.13σ from the fit's 0.37765 while the 1/7 reading (0.413461) sits 1.39σ away.
What falsifies it: a 3% a0 measurement landing on 9.355e-11 rather than 8.618e-11.

## 5. Where this contradicts A62 or A71 — explicitly

1. **A62 §4.1/K14 is right; its number is frame-ambiguous.** A62 derives `a_sat = cH/2π` with H the
   vacuum expansion rate, i.e. H_Λ; the record's `a0 = cH/2π = 1.0422e-10` attaches it to H0 — **20.9%
   high, κ_DE = 0.557076, outside the falsifier band** (C15). Computed: cH_Λ/2π = 8.618166e-11 vs
   cH0/2π = 1.042198e-10, ratio 1.2093 = 1/√Ω_Λ — A71's trap, in a second place.
2. **A62's "1/7 holds to 5.6e-4" is the 3-s.f. rounding of a0_can.** With the exact closure value
   a0 = c²√(Λ/32π) = 9.354173e-11 the agreement is **6.12e-5** (C2). The conclusion is unchanged.
3. **A62's look-elsewhere understates the case**, and **A71's forecast does not decide this question**:
   223 hits at 1% in 156,210 values becomes **540** at 1% in 582,481 distinct values (P = 0.9963 at
   0.01% for a random coefficient), while σ(κ) = 0.040 separates the candidates at only **0.814σ** (C16)
   — a factor-3.7 better measurement is needed, so DR4 wide binaries cannot decide the coefficient.
4. **No contradiction with A71's fit.** κ_P3 = 0.377651 and κ_DE = 0.456695 are reproduced from
   a0 = 8.544e-11 (C20, ratio 1.209304 = 1/√Ω_Λ to 1e-12); both candidates are consistent with it.

## Status

**1/7: NO-GO(match)** — no structural origin; the exact statement is Ω_Λ = 32π/147, irrational and so
inaccessible to any counting argument. **1/(2π): CONDITIONAL(derivation of the scale; premise = a quantum
carrier at T_dS; shape wrong).** **Decidable at σ(a0)/a0 = 2.9%, 3.7× beyond the best forecast here.**

## Checks (a72_checks.py, 22/22 PASS, exit 0, 1.2 s)

| id | what it proves | measured |
|---|---|---|
| C1 | a0/(cH_Λ) = 1/Z at κ=½, SI vs algebra | 0.172747075, residual 0 |
| C2 | a0/(cH0) = κ√(3Ω_Λ/8π); 1/7 to 6.12e-5 | 0.142848395 |
| C3 | 1/7 ⟺ Ω_Λ = 32π/147, exact solve vs brentq | 0.683884115 |
| C4 | 1/Z and 1/(2π) are not the same number | 0.085402 rel |
| C5 | quantum carrier ⟹ exactly cH/2π, mass-independent | 8.618166e-11, residual 0 |
| C6 | Unruh matching ⟹ coefficient 1 | 1.000000000 |
| C7 | equipartition ⟺ Friedmann (N_b/N_s = 1) | 1.000000000000 |
| C8 | surface gravity/2π ≡ Unruh at T_dS/2π ≠ cH0/2π | both 8.618166e-11 |
| C9 | Ω_Λ vs 32π/147 vs Planck | 0.68380036 / 0.112σ |
| C10 | no rational count gives 32π/147 | 331/484 at 1.825e-7; irrational |
| C11 | pool ≥ 200,000 and hits at every window | 582,481; 540/42/5 |
| C12 | the density near each candidate is typical | z = −0.53, −0.22 |
| C13 | routes producing 1/7 exactly: 0; 1/(2π): 3 | 0 / 3, closest 6.12e-5 |
| C14 | present separation < 1σ and Δa0/a0 > 5% | 0.2698σ, 8.62% |
| C15 | the record's 1.0422e-10 = cH0/2π, not cH_Λ/2π | ratio 0.826922 = √Ω_Λ |
| C16 | every forecast < 1σ; 3σ needs N ≈ 4.08e5 | 0.814σ max; 407556 pairs |
| C17 | Δχ² and the likelihood ratio | 0.0875, 0.957 |
| C18 | both readings need Ω_Λ = 0.6839 vs 0.8057 | 16.6σ |
| C19 | forms interpolating the candidates | 2178 |
| C20 | κ_DE/κ_P3 = 1/√Ω_Λ (A71's trap) | 1.209304 |
| C21 | derivable hits: 0/540 (1/7), 1/564 (1/(2π)) | 0 / 1 |
| C22 | Monte-Carlo P(≥1 hit) | 0.9963 at 0.01% |

12 single-input mutations, all exit **1**, **all 22 checks killed** (`MUTATE.md`); none deleted.

## What this does not do

1. **It does not derive MOND's shape from the thermal premise.** A62 K15 showed the analytic response
   gives slope 1; this lane adds no mechanism that would fix it.
2. **The derivability count is over *named* routes**, not all conceivable premises: it says 1/7 is the
   output of none of the seven routes in the record, not that no premise could produce it.
3. **Pool-dependence.** Hit counts depend on the atom and operation sets; the ordering by description
   length and the derivability count do not. 0.01% is where the pool stops being informative
   (P = 0.9963); at 0.001% (P = 0.4323) it is marginal, so no claim is made there.
4. **The wide-binary forecast is a rescaling of A71's**, N ∝ σ⁻²; the 4.08e5-pair requirement inherits
   A71's 0.0726 per-bin scatter. **No new data**: every number is a BRIEF constant, an A62/A71 result,
   or computed here.

## Next

1. **Measure a0 to 3%** — the only thing that decides this: wide binaries at 18–22 kAU, ≈ 4.08e5 pairs.
2. **Stop quoting "1.0422e-10 = cH/2π" without its H**; the frame-correct thermal value is
   **8.618166e-11 = cH_Λ/2π**, and it is the one the data marginally prefer.
3. **If κ = ½ is retained, register it as a *match* to Ω_Λ = 32π/147** (0.11σ), not a derivation — the
   thermal alternative predicts κ_DE = 0.460659, inside the falsifier band and 0.13σ from the fit.

---

## VERDICT

**(1) The coefficient is neither 1/7 nor 1/(2π) as stated, because they are coefficients of different
horizons: the theory's own is 1/Z = 0.172747 × cH_Λ (κ = ½), and 1/7 = 0.142857 × cH0 is that same a0
seen through Ω_Λ = 32π/147. The one order-0.1 coefficient in the census that is a pure number with a
derivation is 1/(2π) = 0.159155 × cH_Λ, i.e. a0 = 8.618166e-11; the record's 1.0422e-10 = cH0/2π is the
same coefficient mis-attached to H0 (20.9% high, κ_DE = 0.557076, outside the falsifier band). (2) Only
1/(2π) is derived — exactly, with no free parameter, from a quantum carrier at the Gibbons–Hawking
temperature, mass-independent to 1e-12 — but the mechanism is analytic in the drive and so derives the
scale, not MOND's shape; 1/7 is a match, its exact content being Ω_Λ = 32π/147 = (8π/3)(2/7)², an
irrational number no cell count can produce (closest p/q with q ≤ 1000: 331/484 at 1.825e-7). The
look-elsewhere settles that matching cannot decide it: 540 closed forms lie within 1% and 5 within 0.01%
of 1/7 (564 / 4 for 1/(2π)), P(≥1 hit at 0.01%) = 0.9963, and 0 of those 540 is the output of any stated
premise. (3) The deciding measurement is a 2.874% measurement of a0 — σ(κ_P3) = 0.01085, a wide-binary
γ_v at 18–22 kAU with ≈ 4.08 × 10⁵ pairs and σ(γ_v) = 0.00553 — 3.7× beyond A71's best forecast; the
DR4 wide binary (σ(κ) = 0.040) separates the candidates at only 0.814σ and SPARC at N = 1000 at 0.276σ,
so neither decides. (4) If 1/7: κ = ½ identically and Ω_Λ = 32π/147 is a prediction (0.11σ from Planck).
If 1/(2π): κ_DE = Z/4π = 0.460659, κ_P3 = 0.380929, and κ = ½ is an 8.54% approximation. **The evidence
marginally supports 1/(2π) attached to cH_Λ — 0.027σ versus 0.297σ, a likelihood ratio of only 1.045,
with the statistical errors alone giving 2.6 : 1 — and the falsifier is a 3% a0 measurement landing on
9.355e-11 rather than 8.618e-11.**
