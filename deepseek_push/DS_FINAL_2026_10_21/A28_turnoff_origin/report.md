# A28 — the turn-off is κ in disguise: y_t = 66.30 has no independent origin

Lane A28 of `DS_FINAL_2026_10_21`; `a28_checks.py` (16/16 PASS, 0.6 s), `a28.out`, `a28_results.json`,
`MUTATE.md`. Footing: `a0 = 9.36e-11 m/s²`, `Λ = 1.0890e-52 m⁻²`; alt `1.13e-10` (BRIEF §4). Targets,
all external: `66.2999` (A4 §D5), `66.3803` (A25, at `32π`), `46.0148` (A4 eq. 18, alt).

## Claim

The closure is exact and reproduces **y_t = 66.299937**, but it also *is* the answer to the lane's
question: with `a0 = κc√(Gρ_Λ)` the closure reads **`F(y_t) = 8π/κ²` exactly**, so `y_t` is a strictly
decreasing function of `κ` and of nothing else. `y_t = 66.30` is therefore not an independent number
to derive — it is `κ = 1/2` (→ `32π` → 66.3803) shifted by 0.121 % by the difference between the
framework's `a0` and the quoted `9.36e-11` — and the four principles the task asks for are all κ
principles in disguise, so A1's two no-gos transfer verbatim. To numbers: **saturation 8.1815**
(×8.10 low), **response-time 5.7852** (×11.46 low; 36.3495 with the Unruh `2π`), **information
3.2287e33** (×4.87e31 high), **self-consistency `y_t = 1`** (which predicts 105.16× too little Λ, i.e.
`a0 = 9.5986e-10`). **None is within 1 %.** The obstruction is scale-theoretic: every local energy /
rate / mode balance in the vacuum sector solves to `a_t = ξ·cH_Λ` with `ξ` a pure number, i.e.
`y_t = O(Z)` with `Z = cH_Λ/a0 = 5.785207`, while the closure demands
`y_t = (6/π)Z² + O(ln Z) = 63.920 + 2.380`. The only expression in the exercise that lands within 1 %
on *both* footings is `2Z² = 66.9372` (+0.961 %) / `45.9264` (−0.192 %) — the *square* of candidate
(i), a two-parameter power law whose coefficient 2 is inserted, whose implied `κ = 0.497858` is a
0.428 % variant of the underivable 1/2, and whose turn-off strain is `2Z = 11.5704`: a coincidence,
not a derivation. **Status: NO-GO(obstruction).**

## Derivation

### 1. The closure equation, and 66.30 reproduced three ways (K1–K4)

    (1)  ν_fix(y) = 1 + (ν_L(y) − 1)/(1 + (y/y_t)²),   ν_L(y) = (1 + √(1+4/y))/2,   y ≡ g_N/a0
    (2)  h(y) ≡ y(ν_L−1) = ½(√(y²+4y) − y) → 1   (y → ∞)
    (3)  F(Y) ≡ ∫₀^∞ h(y)/(1+(y/Y)²) dy = Λc⁴/a0²        [A4 eq. 8; A25 eq. 1]

    (4)  F(Y) = Y ∫₀^{π/2} h(Y tanθ) dθ                       (y = Y tanθ; adaptive quadrature)
    (5)  F(Y) = Y² ∫₀² v²(4−v)/[4Y²(2−v)² + v⁴] dv,  v = √(y²+4y) − y   [A4 eq. 11, exact]
    (6)  F(Y) = (π/2)Y − ln(Y/4) + C_can,  C_can = −0.8862943611         [A4 eq. 13]

`N_Λ ≡ Λc⁴/a0² = 100.405845`. Root of (3): **y_t = 66.299937** (K2). At the root (4) and (5) agree to
1.415e-16 and (6) to 4.35e-4; inverting (6) gives 66.272140, 4.19e-4 low. `dF/dy|_root = 1.555713 > 0`
and `F` is monotone (min `dF/dy = 0.807063`), so the root is unique and `d ln y_t/d ln N_Λ = 0.973456`.

### 2. The closure is the κ identity — so y_t is not an independent unknown (K1, K12)

`ρ_Λ = Λc²/(8πG)` and `a0 = κc√(Gρ_Λ)` give `a0² = κ²Λc⁴/(8π)`, i.e.

    (7)  Λc⁴/a0² = 8π/κ²     (sympy residual 0; equivalently 3Z² = 8π/κ²)

so (3) reads **`F(y_t) = 8π/κ²`**, and since `F` is strictly increasing,

    (8)  y_t = F⁻¹(8π/κ²),      d ln y_t/d ln κ = −1.946912

`κ = 1/2` → `8π/κ² = 32π = 100.530965` → **y_t = 66.380331**; the quoted `(Λ, a0)` gives
`κ = 0.500311` → 100.405845 → **66.299937**. The 0.121 % gap in `y_t` is the 0.0623 % gap in `κ`; two
consequences organise the lane:

- **(a) Equivalence.** Deriving `y_t` *is* deriving `κ`. A1 proved `κ` is not fixed by any function of
  `{c,G,ħ,Λ,H}` (only invariant `ħGΛ/c³ = 2.8448e-122`, so an analytic `F` is constant to 122 digits)
  and that no horizon cell count of 2's and π's reaches 1/2 (`κ² ∈ ℚ·π^odd` for every member). By (8)
  both hold for `y_t`: **the dimensional data admit every `y_t ∈ (0,∞)`**.
- **(b) Diagnosis.** Every candidate that fixes `y_t` predicts a `κ` (the "κ implied" column of §8 is
  `√(8π/F(y_cand))`); a derivation must produce `(cH_Λ/a0)²`, not `cH_Λ/a0`.

### 3. Candidate (i) SATURATION — 8.1815, ×8.10 low (K7, K8, K16)

A1 §6's machinery, unchanged: elastic medium with the only available modulus `μ = ρ_Λc²`, strain
`ε = a/(cH_Λ)`, `u = ½με²`, `V_cell = (4/3)Għ/(c²H_Λ) = 5.781030e-44 m³` (`ℓ_cell = 3.866652e-15 m`),
`E_cell = ħH_Λ/2π = 3.031589e-53 J`. Then `u·V_cell = a²ħ/(4πc²H_Λ)`, and `uV_cell = E_cell` gives

    (9)  a_sat = √2 cH_Λ = 7.657900e-10 m/s²   ⇒   y_t = a_sat/a0 = √2 Z = 8.181518

Error −87.66 %; residual `66.2999/8.1815 = 8.103623 = 1.400749 Z` — which to 0.96 % is `√2 Z =
8.181518`, the candidate's own number. **So the residual is not a missing 2 or π: the target is the
square of the saturation scale.** This is A1's P1 in another coordinate: the same principle gives
`κ_P1 = 4√(π/3) = 4.093307`, i.e. `a0 = 8.181518 a0_can`, the same factor, because both are
`a_sat/a0`. The strain normalization is a free constitutive choice: `ε = a/A` with
`A ∈ {a0, √(a0cH_Λ), cH_Λ, (cH_Λ)²/a0}` gives `y_t = √2A/a0 = {1.414214, 3.401531, 8.181518,
47.331769}` (K8); the closest member is still 28.61 % away, so **no strain reference reaches 66.3** —
§9's landing value is exactly √2 times the largest member above (the first hint of §7).

### 4. Candidate (ii) RESPONSE TIME — 5.7852, ×11.46 low; the rate is not defined (K9)

A2's lattice fixes only the *ratio* of its rate constants: mass action `k_a g(1−θ) = k_d θ` with
`k_d/k_a = a0`, so the total exchange rate is

    (10) Γ = k_a g + k_d = k_d(1 + y)

and `k_d` is a free rate — the theory supplies no second condition. `Γ = H_Λ` is one equation in two
unknowns: **no prediction.** If `k_d` is identified with the only cosmological rate, `k_d = H_Λ`, then
`Γ ≥ H_Λ` with equality only at `y = 0`: no turn-off at all. The only rate the theory can build from
the acceleration alone is the Rindler/Unruh frequency `ω = ξ_r a/c`:

    (11) ω = H_Λ  ⇒  y_t = ξ_r Z = 5.785207 (ξ_r = 1)  or  36.349525 (ξ_r = 2π)

— errors −91.27 % and −45.17 %. Read as a time, the requirement is
`τ = 1/(y_t H_Λ) = 8.350507e15 s = 264.6 Myr`, **66.3× shorter than the Hubble time**
(`1/H_Λ = 5.536381e17 s`). "Causal cutoff at one Hubble time" is quantitatively wrong by the factor
`y_t` itself, and the obstruction is structural, not numerical: the action has no dissipative term, so
a relaxation rate is not a property of the medium at all.

### 5. Candidate (iii) INFORMATION — 3.23e33, ×4.87e31 high (K10)

Modes per cell with acceleration above `a`, counting `k > a/c` in the cell volume:

    (12) N(>a) = V_cell (a/c)³/(6π²) = 1  ⇒  a = c(6π²/V_cell)^{1/3} = 3.022057e23 m/s²
         ⇒  y_t = 3.228693e33   (alt: 2.674387e33)

At the actual target the count is `N = 8.658811e-96` modes per cell: the literal principle is a
Planckian statement about a 3.87e-15 m cell and misses by 33 orders of magnitude, since a cell that
large has no modes at `6.2e-9 m/s²`. The only reading returning an O(1) number is "one mode per cell at
the cell's own frequency `H_Λ`", i.e. `a = cH_Λ`, `y_t = Z` again (K9's number).

### 6. Candidate (iv) SELF-CONSISTENCY — y_t = 1, and Λ comes out 105× small (K11)

`W'(u) = (u/K)/(1 − u/a0)` has its pole at `u = a0`, i.e. `y = 1`; that is where the medium's own
description breaks. Cutting (3) there:

    (13) F(1) = 0.954759   vs   N_Λ = 100.405845   (short by 105.163593×)
         ⇒  a0 = c²√(Λ/F(1)) = 9.598615e-10 = 10.254930 a0

The candidate does not predict `y_t` at all — it defines it — and its testable content is the `Λ` it
predicts: 105× too small, requiring `a0` 10.25× too large. The observed `Λ` needs the integral to run
66.3× past the breakdown to `y_t = 66.3`, where `1/(1−u/a0) = −1/65.3`: the "description" is used 66×
outside its domain — the no-go, and no normalization repairs it.

### 7. Why the class fails — the scaling obstruction

**Class theorem.** Let a principle fix an acceleration by balancing two *local* quantities — an energy
density against a cell energy, a rate against `H_Λ`, a mode count against one — with constitutive data
`{ρ_Λ, c, ħ, H_Λ}` and at most one power of `a0` entering through a normalization (strain reference or
capacity). Each such balance is a dimensionless equation in `a/(cH_Λ)` with pure-number coefficients:

    (14) a_t = ξ cH_Λ,  ξ a pure number  ⇒  y_t = ξ Z  (or ξ, if a0 is the reference)

i.e. **`y_t = O(Z⁰)` or `O(Z¹)`, never `O(Z²)`.** The closure, however, needs

    (15) y_t = (6/π)Z² + (2/π)(ln(y_t/4) − C_can) = 63.920 + 2.380 = 66.300,  y_t/Z² = 1.980958

(`6/π = 1.909859`). Why `Z²` is unreachable locally: `ρ_Λc² = 3(cH_Λ)²/(8πG)` contains no `a0` and
`E_cell` contains no `a0`, so a local density carries at most `a0^0` or `a0^-1`; a balance yielding
`a_t ∝ 1/a0` needs a density `∝ a0^-2`, and **the only such object in the theory is `Λc⁴/a0² = 8π/κ²`
itself** — the target. A "principle" that produces `Z²` is therefore already a statement about the
vacuum integral: the closure, not an origin for it. Hence the misses are powers of `Z` (8.103623 =
1.400749 Z, 11.460254 = 1.980958 Z, 3.228693e33, 66.3), not O(1) factors.

### 8. The alt footing: what it does and does not test (K6, K13)

| object | y_t canonical | err | y_t alt | err | κ implied by (8) | residual drift `r_can/r_alt` |
|---|---|---|---|---|---|---|
| **target** | 66.2999 | — | 46.0148 | — | 0.500311 | 1 |
| (i) saturation | 8.1815 | −87.66 % | 6.7769 | −85.27 % | 1.513176 | 1.193473 |
| (ii) response | 5.7852 | −91.27 % | 4.7920 | −89.59 % | 1.833651 | 1.193473 |
| (iii) information | 3.2287e33 | — | 2.6744e33 | — | ≈0 | 1.193473 |
| (iv) self-consistency | 1.0000 | −98.49 % | 1.0000 | −97.83 % | 5.130659 | 1.440838 |
| `2Z²` (numerology) | 66.9372 | +0.961 % | 45.9264 | −0.192 % | 0.497858 | 0.988576 |

A candidate "one constant factor away" needs `r_can = r_alt`, drift 1. None has it: the `Z`-linear
three drift by 19.35 %, the footing-independent one by 44.08 %, so **no candidate is a normalization
slip away.** Nor is the alt footing independent data — it is the same closure at a different `a0`, so
it tests only the *exponent*, `p = d ln y_t/d ln Z = 1.946912`; two footings and two parameters mean
any `y = A Z^p` fits both exactly. It kills every `q ≤ 1` candidate; it cannot separate 2 from 1.947.

### 9. The only sub-1 % expression, and why it is not a derivation (K15)

`2Z² = 66.937230` (+0.961 %) and `45.926415` (−0.192 %): it lands because the closure's effective
coefficient is `y_t/Z² = 1.980958` (2 is 0.96 % above it) and the required exponent is 1.946912 (2 is
2.73 % above it) — two few-percent errors a one-parameter power law absorbs. Not a derivation:

1. **The 2 is inserted.** No balance in the theory gives coefficient 2 with exponent 2; saturation
   gives `√2 Z`. Squaring an acceleration ratio is dimensionally free — any pure function of `Z` is
   allowed — so the data select the exponent, not a principle.
2. **Its second prediction has no support.** `y_t = 2Z²` means `a_t·a0 = 2(cH_Λ)²`, so
   `√(a_t a0) = 7.657900e-10`: turn-off and `a0` would have the saturation acceleration as geometric
   mean. The same strain logic with `A = a0, √(a0cH), cH` gives 1.41, 3.40, 8.18 (§3).
3. **Through (8) it is `κ = 0.497858`**, a 0.428 % variant of the `κ = 1/2` A1 proved lies outside
   every cell-count class — a κ coincidence, re-expressed — and `2Z² = (2/3)N_Λ` is a statement about
   the target itself, carrying no information independent of the closure.

The strain reading fails for target and `2Z²` alike: at `y_t = 66.3` the strain is
`a_t/cH_Λ = 11.460254` and the strain energy per cell is `65.668711 E_cell`. Any "saturation at one
quantum per cell" story is 66× short at the turn-off — §3's failure from the other side.

### 10. Numerology control — how much precision is being claimed (K14)

| change to the closure | y_t | shift |
|---|---|---|
| coefficient `π/2 → π/4` / `→ π` (factor 2 each way) | 133.434814 / 32.913152 | +101.3 % / −50.4 % |
| drop `ln(y/4)` | 64.484578 | −2.74 % |
| drop `C_can` | 65.702141 | −0.90 % |
| `Λ` +1 % / −1 % | 66.945053 / 65.654764 | ±0.973 % |
| `N_Λ = 32π` instead of observed (A25) | 66.380331 | +0.121 % |
| `N_Λ = 73.19` (H0-tied; A25 §8, external) | 48.787740 | −26.4 % |

A factor-2 error in the closure moves `y_t` by a factor 2; the *definition* of the target moves it by
0.121 %; a 1 % `Λ` by 0.973 %. The four-digit 66.2999 is meaningful only relative to a specified
`(Λ, a0, C_can)` — the third digit sits at the 32π-vs-observed choice, the fourth is not physics —
and a "1 % hit" on `y_t` is a ~1 % statement about `Λ`.

## Status

**NO-GO(obstruction).** §1 **DERIVED** (quadrature agreement 1.415e-16, root 66.299937); §2
**DERIVED** (sympy identity (7), residual 0 — the load-bearing structural result); §3–§6
**NUMERICAL** (each candidate to a number, §8); §7 **NO-GO** (class theorem (14) + `Z²` argument);
§9 **NUMERICAL/numerology**; §10 **NUMERICAL** (precision audit). The missing premise, named
exactly: **a principle that produces `(cH_Λ/a0)²` — equivalently, a derivation of `κ`.** The
medium's cell structure cannot supply it (no local density carries `a0^-2`) and the dimensional data
cannot either (A1 no-go A, transported by (8)); any future claim to derive `y_t` is a claim to derive
`κ` and must survive A1's no-go B.

## Checks (`a28_checks.py`, 16/16 PASS, exit 0, 0.6 s)

| id | what it proves | measured |
|---|---|---|
| K1, K2 | exact `8π/κ² = 3Z²` identity; canonical root | residual 0.0e+00; 66.299937 (tol 5e-4) |
| K3, K4 | quadrature vs exact vs asymptotic; uniqueness | 1.415e-16, 4.35e-4; 66.272140 (4.19e-4), min dF/dy 0.807063 |
| K5, K6 | `32π` target; alt root and scaling | 66.380331; 46.014839, ratio 1.440838 vs 1.457489, p = 1.946912 |
| K7, K8 | saturation; its normalization family | 8.181518 (−87.66 %, residual 8.103623, κ = 1.513176); 1.41/3.40/8.18/47.33, min err 28.61 % |
| K9, K10 | response time; information | 5.785207 (−91.27 %), 2πZ = 36.349525, κ = 1.833651; y = 3.228693e33, N = 8.66e-96 |
| K11, K12 | self-consistency; equivalence κ(y_t) | F(1) = 0.954759, short 105.163593×, a0 = 9.598615e-10; 0.500311 both, elasticity −1.946912 |
| K13, K14 | alt-footing drift; numerology control | 1.193473 (×3), 1.440838; 133.434814 / 32.913152 / 64.484578 / 65.702141 / 66.945053 / 48.787740 |
| K15, K16 | `2Z²` on both footings; saturation's second prediction | +0.961 %, −0.192 %, κ = 0.497858, strain 11.570413; RAR(y=10) 0.400972 vs 0.977756 |

`--mutate=kernel` (Langmuir → quadrature) breaks **8/16** (K2–K6, K12, K14, K15), exit 1.
`--mutate=sat` (strain reference `a0 → (cH)²/a0`) breaks **2/16** (K7, K16), exit 1. Both in `MUTATE.md`.

## What this does not do

- **Does not prove no principle can produce `Z²`.** It proves no *local cell balance of the stated
  class* can, and that any principle which does produce `Z²` is already a statement about `Λc⁴/a0²`,
  hence about `κ`. A non-local or topological route evades §7 but is still a κ derivation (A1 no-go B).
- **Does not re-derive the closure normalization** (3), inherited from Zenodo 23171085 via A4 eq. 8
  and A25 eq. 1 and cross-checked at 0.19 % by the quadrature band; a factor-2 error in it moves `y_t`
  to 133.43 (§10).
- **No data fits, no EFE, no Cassini Q₂.** K16's RAR numbers are the leading `1/(1+(y/y_t)²)`, not a
  χ²; A25's cost of the `y_t = 48.79` turn-off (`Δχ² = +0.060`) is an external input.
- **Does not test candidates outside the four named**, except the strain family (§3) and both closed
  forms of the response-time reading (ξ_r = 1, 2π).
- **The alt footing is not independent data** (§8): it constrains the exponent, not the coefficient.

## Next

1. **Close the ledger entry.** `y_t` is a function of κ — `F(y_t) = 8π/κ²`, `y_t(1/2) = 66.380331` —
   and should be removed from the list of independent open problems. There is no separate "turn-off
   origin" question; there is the κ question, already NO-GO in A1.
2. **If the κ hunt is revived**, the three routes A1 named (χ(S²) = 2, two graviton polarizations, a
   two-sided causal diamond) each land `y_t` automatically via (8), and each must predict something
   else; `y_t` adds no independent falsifier to them.
3. **The measurement that would count** is the astrophysical shadow: the turn-off at 66.3 costs 2.22 %
   of the anomaly at `y = 10` (`0.977756`), saturation's 8.18 would cost 59.9 % (`0.400972`). A RAR
   determination at the few-percent level separates "no turn-off" from the Λ-required one; nothing in
   the Solar System can, the tightest planetary cap being `y_t ≤ 605.96` (A4), 9.14× above 66.3.
