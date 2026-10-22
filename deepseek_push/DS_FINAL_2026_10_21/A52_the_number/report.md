# A52 — WHAT PHYSICAL QUANTITY EQUALS 2√(32π/3) = 11.5776 ?

Lane A52. `a52_checks.py` — 17 checks, **17/17 PASS**, exit 0, 2.3 s, deterministic, no network,
stdlib + sympy. `a52.out` is the captured stdout; `a52_results.json` holds every number quoted
below (each value here is that file's entry, rounded to the digits shown); `MUTATE.md` records four
mutations, each breaking exactly one check. Constants: BRIEF §4 (c, G, H0, Λ, a₀_can, Mpc, pc), plus
ħ = 1.054571817e-34 J s (CODATA 2018, declared, only for S_dS) and κ = 0.417 ± 0.095 (CFG493 via A15,
external). No fitted constant introduced.

## Claim

11.5776 = 2√(32π/3) has exactly one physical identity, and it is a tautology: it is the de Sitter
horizon acceleration in units of a₀/2, **2cH_Λ/a₀ = L_MOND/(r_H/2)**, evaluated at κ = 1/2. Of the
26 closed forms tabulated here (25 of order 10, plus one sixth root), the only 6-digit hits are four
algebraic spellings of that one number (residual 0 across all four); every genuinely distinct
**physical** candidate misses by ≥ 3.65 % (12) — 4π by 8.54 %, the sphere-volume family by ≥ 14.75 %,
the Jeans coefficient by 82 %, the Hubble/Planck sixth root by 29 orders — and the static-patch
degrees of freedom are 3.31×10¹²² (or the integers 10, 20, 2, 4). The two closest expressions of any
kind, e^√6 (0.042 %) and 4π−1 (0.097 %), carry no physical statement and are exactly what the
look-elsewhere pool predicts (§8). The number is irrational (K9), so **no integer count can equal
it**; and any count that hits it fixes only the product β√χ = 2, which *is* κ by definition (K8,
A27). A pool of 119,108 distinct closed forms with ≤ 3 operations contains 401 values within 1 % of
the target and 9 within 0.01 % — against 401.1 ± 16.6 for a random target in the same window; the
target sits at the 54th percentile. **Verdict: numerology as a derivation, but a genuine measurable
ratio as a quantity** — the one-line identification and its falsifier are in §5.

## Derivation

### 1. The exact object (K1, K6, K7)

    (1.1)  ρ_Λ = Λc²/(8πG),  H_Λ² = Λc²/3,  a₀ = κc√(Gρ_Λ) = κc²√(Λ/8π),
           Z := √(32π/3) = 2√(8π/3) = 5.7888100365
    (1.2)  a₀/(cH_Λ) = 2κ/Z   ⟹   2cH_Λ/a₀ = Z/κ
    (1.3)  κ = 1/2  ⟹  2cH_Λ/a₀ = 2Z = √(128π/3) = 4√(8π/3) = 8√(2π/3) = 11.5776200729
    (1.4)  L_MOND := c²/a₀ = 31.14 Gpc,  r_H := c/H_Λ = 5.38 Gpc
           L_MOND/(r_H/2) = 11.5776200729,   L_MOND/r_H = 5.7888100365

All three residuals are exactly 0 symbolically. The factor 2 between Z and the target is the
radius/diameter bookkeeping that A1 §3 catalogued as free: 5.7888 is the radius reading
(a₀/(cH_Λ) = 0.17275), 11.5776 the half-horizon reading with H_half := c/(r_H/2) = 2H_Λ
(a₀/(cH_half) = 0.08637). So even "11.5776 rather than 5.7888" is a convention, not a measurement.

### 2. The candidate table — task (1), to 10 digits (K2–K5)

| expression | value | dev. from 11.5776 | what it is | verdict |
|---|---|---|---|---|
| 2√(32π/3) | 11.5776200729 | 0 | the target (definition) | **hit** |
| 4√(8π/3) | 11.5776200729 | 0 | 4 × inverse Friedmann coefficient | **hit, rewrite** |
| √(128π/3) | 11.5776200729 | 0 | same, factored | **hit, rewrite** |
| 8√(2π/3) | 11.5776200729 | 0 | same, factored | **hit, rewrite** |
| e^√6 | 11.5824351900 | +0.042 % | chance near-hit | miss (numerology) |
| 4π − 1 | 11.5663706144 | −0.097 % | chance near-hit | miss (numerology) |
| 3π + 2 | 11.4247779608 | −1.32 % | chance near-hit | miss |
| 2^(7/2) | 11.3137084990 | −2.28 % | chance near-hit | miss |
| π² + 2 | 11.8696044011 | +2.52 % | chance near-hit | miss |
| **12** | 12.0000000000 | **+3.65 %** | cH_Λ/6 (Verlinde-form); SM gauge generators | miss |
| 11 | 11.0000000000 | −4.99 % | M-theory dimensions | miss |
| 4π | 12.5663706144 | +8.54 % | solid angle of S² | miss |
| 2π√(8/3) | 10.2603986413 | −11.4 % | 2π × √Friedmann | miss |
| 10 | 10.0000000000 | −13.6 % | dS₄ Killing vectors; Weyl components | miss |
| 8π/3 | 8.3775804096 | −27.6 % | Friedmann coefficient | miss |
| 16π/3 | 16.7551608191 | +44.7 % | 4 × Friedmann | miss |
| √(32π/3) | 5.7888100365 | −50 % | half the target: cH/a₀ | miss |
| Vol S⁵/Vol B⁵ | 5.8904862255 | −49.1 % | surface/volume, n = 5 | miss |
| Vol S⁴/Vol B⁴ | 5.3333333333 | −53.9 % | surface/volume, n = 4 | miss |
| Vol S³/Vol B³ | 4.7123889804 | −59.3 % | surface/volume, n = 3 | miss |
| 4π/3 | 4.1887902048 | −63.8 % | ball-volume factor | miss |
| Vol S²/Vol B² | 4.0000000000 | −65.5 % | surface/volume, n = 2 | miss |
| Vol S⁴/Vol S² | 2.0943951024 | −81.9 % | sphere-volume ratio | miss |
| (4π/3)^(1/2) | 2.0466534159 | −82.3 % | Jeans mass coefficient | miss |
| Vol B⁴/Vol B² | 1.1780972451 | −89.8 % | ball-volume ratio | miss |
| (V_H/V_P)^(1/6) | 2.9141×10³⁰ | (not of order 10) | Hubble/Planck volume, sixth root | miss |

**Hits: 4 rows, 1 distinct value, 0 independent formulas** (K2: `n_hits6 = 4`,
`n_distinct_hit_values = 1`, `n_nonrewrite_hits = 0`). Every sphere-volume ratio is below
0.9 × target — the family's largest member is S⁵/B² = π² = 9.869604, 14.75 % low (K3). The whole
solid-angle family misses by ≥ 8.54 % (K4). Thermodynamic/gravitational candidates (K5): Jeans
√(4π/3) = 2.0467; S_dS = A/4ℓ_P² = 3.3130×10¹²², A/ℓ_P² = 1.3252×10¹²³, √S_dS = 1.820×10⁶¹,
log₂S_dS = 407.0; dS₄ Killing vectors = 10; Weyl components = 10; Riemann components = 20;
graviton polarisations = 2; dimensions = 4; N_eff = 3.046; g_* = 106.75 — none is 11.58, and the
closest order-10 item is the integer 12 at 3.65 %. The static patch never gives 11.58: either a count of 10 (isometries) or 10¹²² (entropy), nothing in between.

### 3. The exact hit: physical statement, prediction, and what it fixes — task (2)

There is **one distinct hit**, in four spellings. Its physical statement is (1.3)–(1.4):

> *the de Sitter horizon's surface gravity cH_Λ is 5.788810 a₀; the MOND length is 11.577620
> half-horizon radii.* Equivalently a₀ = cH_Λ/Z = c²√(Λ/32π).

**What it predicts.** a₀ = 9.3541734858×10⁻¹¹ m/s² from Λ alone — hence the RAR knee at g = a₀
(the no-free-parameter Δχ²(Q−L) = +157.96 test of A25), L_MOND = 31.14 Gpc = 2ℓ₁, and the THEORY §5
entries that depend on a₀ (γ_v = 1.18 at 20 kAU, R_core = 53.31 pc; THEORY §5, external). It is
falsifiable: σ(a₀)/a₀ ≲ 2.8 % separates κ = 1/2 from Z/4π (8.54 % away, A1 §4) and ≲ 1.0 % separates
11.5776 from 12.

**But it has zero surplus.** The quantity identified *is* Z/κ. The identification "N = 2cH_Λ/a₀"
with N = 11.5776 is the equation Z/κ = 2Z, i.e. κ = 1/2 — no more and no less. In A27's D-criteria
it fails D1 (independence: the premise, with the abbreviations eliminated, *is* a₀ = c²√(Λ/32π)),
D2 (discriminating image: the map has the single value 2) and D4 (surplus: nothing checkable beyond
the postulate). So the hit is an **identity, not a derivation**: it predicts a₀ because P3 does.

### 4. The product test: a hit on a product is not a derivation (K8)

Write the same number in the theory's own dimensionless variables, with β := L/ℓ₁ and χ the cell
topology (A27):

    (4.1)  κ = 1/(β√χ)   ⟹   N := 2cH/a₀ = 2√(8π/3)·β√χ
    (4.2)  N = 11.577620  ⟺  β√χ = 2   (exactly; residual 0)

One equation, two unknowns: the level set is a **curve** (dimension 1), and both named geometries
sit on it — (β,χ) = (2,1) ("the MOND length is the diameter of the 4-ball") and (1,4) ("the radius
of S²×S²") give κ = 1/2 exactly. So the identification fixes the **product** β√χ, not the geometry;
κ follows only because κ is *defined* as the reciprocal of that product. This is A27's result
reproduced for this number: a hit on a product is not a derivation, and here the product is κ.

The four cases exhaust the possibilities, and each closes:

| identification type | what it fixes | status |
|---|---|---|
| N = 2cH_Λ/a₀ (a ratio of the theory's own scales) | κ, bijectively | **tautology** (κ is defined by it) |
| N = a count (integer/rational from π-powers) | — | **impossible**: N is irrational (K9) |
| N = F(κ, β, χ, u) with any medium parameter | a curve in (κ, β) | **κ free along it** (K8) |
| N = a numerical near-hit (4π−1, e^√6, …) | nothing | **numerology** (no prediction) |

### 5. The one-line identification, and its prediction

**11.5776 is the de Sitter horizon acceleration in units of a₀/2: 2cH_Λ/a₀ = L_MOND/(r_H/2) = 11.577620, at κ = 1/2.**

Its prediction is a₀ = c²√(Λ/32π) = 9.3542×10⁻¹¹ m/s², with the falsifier σ(a₀)/a₀ ≲ 1 % (which
separates it from 12 at 3σ). It is a *measurable* number: both factors are observables (§7). It is
not an independent constant and not a count.

### 6. Why 12 is not the answer — and the control that kills the method (K9, K10)

    (6.1)  12/2Z = 1.0364824484 = √(27/(8π));  κ(12) = Z/12 = 0.4824008 (3.52 % below 1/2);
           R(12) = 1/κ² = 108/(8π) = 4.29718  (vs the exact 4)
    (6.2)  2Z = 11.577620 lies between the integers 11 (−4.99 %) and 12 (+3.65 %); no integer is
           within 1 % (K9). 4√(8π/3) is irrational: if it were p/q then π = 3p²/(128q²) ∈ ℚ,
           contradicting π transcendental.
    (6.3)  12 = 2 × 6 and 6 = round(2√(8π/3)) = round(5.788810). "The twelfth" is **twice the
           nearest integer to the Einstein–Friedmann normalisation** — rounding, not counting.

The control: on the H0 footing with a₀_can, 2cH0/a₀ = 13.992236, which is the integer **14** to
**0.0555 %** — **66× tighter** than 12's 3.65 %. If a 3.5 % integer hit were a derivation, 14 would
be 66 times more of one (and A1's K13 found the same with 1/7, sixty times tighter than 1/12).
An integer-matching method that returns 12, 14 and 7 with comparable looseness has no discriminating
power. (Both folklore divisors, 6 and 2π, exceed Z = 5.7888, so both give a₀ below the exact value.)

### 7. Measurement status (K11)

2cH_Λ/a₀ is an observable: a₀ from the RAR, H_Λ from cosmology. With κ_meas = 0.417 ± 0.095:

    (7.1)  N = Z/κ = 13.882 ± 3.163 ;  z(11.5776) = 0.73σ ;  z(12) = 0.60σ

Both values are within 1σ; the data cannot tell them apart. A 3σ separation needs
σ(κ) ≤ 0.00423 (1.01 %), i.e. **22.5× better than the current 0.095**. So the number is observed
today only at ±23 % (σ_κ/κ = 0.095/0.417): consistent with 11.5776, equally consistent with 12, 14 or 10.

### 8. Look-elsewhere — task (3) (K12–K15)

Declared grammar: atoms {2,3,4,5,8,π,√2,√3,e}; operations + − × ÷ and √, each costing one;
≤ 3 operations; intermediate values pruned to [0.05, 5000]; values deduplicated at 10 s.f.

    generated expressions        430,461      distinct values      119,108
    sub-pool with <= 2 operations  12,556      distinct values        4,099
    distinct values in [10.42,12.735] (order-10 window)            4,008
    within 1 % of 11.5776          401   (10.0 % of the window; 0.34 % of the whole pool)
    within 0.1 % / 0.01 %          49 / 9
    closest pool value   11.5775512456 = π(π + e/5),  dev 5.94×10⁻⁶  (0.00059 %)

Matched controls: 200 random targets in [10.5, 12.7] give **401.1 ± 16.6** hits within 1 %
(range 358–441); the actual target gives 401, **z = −0.00, 54th percentile**. Integer targets are
hit *exactly* (3–4 exact expressions each for 4, 10, 11, 12, 13); the irrational target is hit
exactly **zero** times. The best chance hit (π(π+e/5), 5.94×10⁻⁶) is **6137× tighter** than the best
physical near-miss (12, 3.65×10⁻²).

A 200-expression pool of this complexity contains ≈ 20 hits within 1 %; P(≥1) ≈ 1 (1 − 0.9²⁰⁰ =
7.6×10⁻¹⁰). Look-elsewhere probability: p = 0.100 per candidate, so P(≥1 hit | m = 12) = **0.718**,
with 1.20 expected hits; **56 candidates** are enough to guarantee a 3σ "discovery" by chance and
136 for 5σ. The task's own list of twelve produced **one distinct hit** — exactly the chance
expectation. (A34's independent pool found 11/90 = 12.2 % for a different target; the two base
rates agree.)

### 9. No independent O(10) number exists in the vacuum data (K16)

The exponent matrix of {c, G, ħ, Λ, H} has nullspace dimension 2; imposing H = H_Λ (the theory's own
Friedmann identity) leaves exactly one invariant,

    (9.1)  x = ħGΛ/c³ = 2.8448×10⁻¹²²  (log₁₀ = −121.5)

Any analytic F(x) is constant to 122 digits. So no O(10) dimensionless number can be built from the
vacuum data without a₀; the target can only enter through a₀, which is what makes it κ in disguise.
That is A1's no-go A, restated: the search for "another formula" is closed in principle.

## Status

**`NO-GO(obstruction)`** for the derivation; **`NUMEROLOGY`** for the "12". Sub-results: §1–§2
**DERIVED** (exact identities, K1–K7); §3–§5 **IDENTITY, zero surplus** (K6, K8); §6 **NO-GO** (K9,
K10); §7 **NUMERICAL** (K11); §8 **NUMERICAL** (K12–K15); §9 **NO-GO** (K16). The obstruction, stated so it can be attacked:
*any quantity equal to 11.5776 is either 2cH_Λ/a₀ itself (κ restated), or a count (impossible —
irrational), or a function of the medium's free parameters (fixes a curve, not κ), or a numerical
coincidence (no prediction).* What is missing for a derivation is a UV/topological principle that
outputs the dimensionless number **2√(8π/3) without inserting the Einstein 8π/3 and without a₀** —
i.e. a count that carries a √π normalisation, which A1's lattice theorem excludes.

## Checks (a52_checks.py, 17/17 PASS, exit 0, 2.3 s)

| id | what it proves | value |
|---|---|---|
| K1 | 2√(32π/3) = 4√(8π/3) = √(128π/3) = 8√(2π/3), residuals exactly 0 | 11.5776200729 |
| K2 | 26 candidates to 10 digits: 4 hits, 1 distinct value, 0 non-rewrite | hits 4, distinct 1 |
| K3 | S^n, B^n (n = 2..5) and every ratio: 0 hits | max ratio π² = 9.869604 |
| K4 | solid angle 4π and fractions: 0 hits | 4π dev +8.54 % |
| K5 | Jeans, (V_H/V_P)^(1/6), static-patch dof: 0 hits | closest O(10) 12 at 3.65 % |
| K6 | 2cH_Λ/a₀ = 2√(8π/3)/κ; κ = 1/2 ⟺ target; a₀ = c²√(Λ/32π) | 9.354173e-11 |
| K7 | L_MOND/(r_H/2) = 2cH/a₀ exactly | 11.5776200729 |
| K8 | κ = 1/(β√χ), N = 2√(8π/3)β√χ; hit ⟺ β√χ = 2; level set dim 1 | dim 1 |
| K9 | irrationality: π = 3p²/(128q²); no integer within 1 % | 11, 12 miss |
| K10 | 12/2Z = √(27/(8π)); κ(12) = 0.4824008; 14-hit 66× tighter | dev14 0.0555 % |
| K11 | N(κ_meas) = 13.882 ± 3.163; z(2Z) = 0.73, z(12) = 0.60 | σ_κ(3σ) = 0.00423 |
| K12 | pool 430,461 gen / 119,108 distinct; 401 hits @1 %, 9 @0.01 % | base rate 10.0 % |
| K13 | random targets 401.1 ± 16.6; target z = 0.0, 54th pct; exact hits at integers 3–4, target 0 | z −0.00 |
| K14 | p = 0.100; P(≥1|m=12) = 0.718; 56 trials for 3σ | 1.20 expected |
| K15 | best chance hit π(π+e/5) at 5.94e-6, 6137× tighter than 12 | 5.94e-06 |
| K16 | nullspace dim 2; unique invariant x = 2.8448e-122 | log₁₀ = −121.5 |
| K17 | a₀: cH/2π < cH/6 < exact; H0 footing 20.9 % higher | 8.618/9.025/9.354 e-11 |

Mutations: `--mutate=M1..M4` each break exactly one check (K2, K6, K12, K11) and print `MUTATION CONFIRMED`; see `MUTATE.md`.

## What this does not do

- It does not search the literature exhaustively for an *obscure* formula that happens to equal
  4√(8π/3). It enumerates the closed forms a gravitational/thermodynamic physicist writes down
  (a declared class, K2–K5), and proves the class of *independent* constructions is empty (K9, K16).
- It does not prove κ ≠ 1/2 in nature, nor that no UV completion produces κ = 1/2. That is the open
  problem (BRIEF §6); this lane shows the number 11.5776 cannot be its output *unless* the
  completion inserts the Friedmann normalisation.
- The pool is a declared grammar, not "all of mathematics" (level breakdown in §8). It does not
  re-derive κ_meas, and does not adjudicate the canonical/alt footing (9.36e-11 vs 1.13e-10); §17
  shows the footing moves a₀ by 20.9 %, itself an argument against reading 11.5776 as a constant.

## Next

1. The only live route: a UV/topological principle that outputs 2√(8π/3) *as a ratio* with the
   8π/3 normalisation already present, without a₀. A1's lattice theorem says no π-power count does;
   a ratio of two independently computable areas/rates is the remaining shape. If a count is ever
   offered, check first that it is not 2×6 with 6 = round(2√(8π/3)): that is the observed arithmetic
   of the "twelfth", and it is rounding.
2. Pre-registered discriminator: σ(a₀)/a₀ ≤ 1.0 % separates 11.5776 (κ = 1/2) from 12 (κ = 0.4824)
   at 3σ; ≤ 2.8 % separates it from Z/4π. Both are within reach of a future RAR/wide-binary program.
