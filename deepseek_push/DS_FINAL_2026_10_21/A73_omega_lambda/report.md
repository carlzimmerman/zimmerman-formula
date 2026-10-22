# A73 — Ω_Λ = 32π/147: A KEPLER-GRADE PREDICTION, OR NUMEROLOGY?

**Lane:** A73_omega_lambda · **Date:** 2026-10-22 · **Base:** `deepseek_push/DS_FINAL_2026_10_21`
**Script:** `a73_checks.py` — **26/26 PASS, exit 0, 0.1 s**, deterministic, no network, stdlib + numpy + sympy.
**Output:** `a73.out` (stdout) · **Data:** `a73_results.json` · **Mutations:** 12, all exit 1, **26/26 checks killed** (`MUTATE.md`, `a73_MUTATE_*.out`).
**Read:** `A62_twelfth/report.md` (the 32π/147 identity and the first look-elsewhere), `A71_global_fit/report.md` (the joint fit and the convention trap), `A33_master_action/MASTER_ACTION.md` (§3.5, the background equation).

**Claim under audit.** `Ω_Λ = 32π/147 = 0.6838841151` exactly, which is the exact equivalent of
`a0/(cH0) = 1/7` and of `κ = ½` in the ρ_DE convention. `THEORY.md` §6.1 calls the 5.6×10⁻⁴ hit
"**a prediction, not a fit**".

**The test applied.** Kepler-grade means three things, and they are scored separately below:

| leg | requirement | this claim |
|---|---|---|
| **number** | exact, stated to more digits than the data | **PASS** — 0.6838841151, two engines agree to 0 |
| **recipe** | an integer 147 produced by the theory's structure *without* using the measured `a0/H0` | **FAIL** — 147 = 3(cH0/a0)², i.e. the measured ratio squared (§2) |
| **falsifier** | a named measurement that excludes it at 3σ, with the required precision stated | **FAIL on the Ω_Λ side** (needs 0.04 %, 27× Planck); **PASS on the a0 side** (needs 2.91 %, reachable) (§4) |

**One clean leg, one partial, one missing. That is the verdict; the rest of this report is the computation behind it.**

---

## 0. Bottom line

1. **The number is exact and 0.112σ from Planck** — but 0.112σ is the distance from a *number* to a
   *measurement*. The theory's own uncertainty on Ω_Λ, propagated from the `a0` that fixes it, is
   **±0.078 (13.7 %, joint fit) to ±0.128 (18.8 %, canonical footing)**: compared at its own precision the
   prediction is **1.47σ** from Planck, not 0.11σ (K8); the fractional error on Ω_Λ is 13.7 %, twice
   that on `a0`. The Ω_Λ agreement is bought by setting the
   theory's error bar to zero.
2. **147 is not structural.** `147 = 3(cH0/a0)²` and `32 = 8/κ²`: the integer is *defined* by the two
   measured ratios the claim is supposed to explain. Every exact route to 147 is either that identity
   or a chosen integer (`3(D−3)²` with D = 10; `7·C(7,2)`); no physical count (g_*, N_eff, e-folds,
   1/α) lands on it (K20, K26). The record itself already says so: A1 K13 concludes "hence no derivation", A37 calls it "numerology", A62's status is **NO-GO(obstruction)**.
3. **Look-elsewhere: 65 closed forms lie within 0.11σ of 0.6847 in a 260,129-value pool, and a random
   value in [0.5, 0.9] has 75.3 such forms on average — P(≥1) = 1.000000, 2000/2000 random targets
   have at least one.** A two-operation rival, **√3 − π/3 = 0.684853256**, is **5.32× closer** to
   Planck than 32π/147 (K11–K15).
4. **It is a coincidence, not a prediction.** The only falsifiable content is the relation
   **H0 = 7a0/c** (equivalently `a0 = cH0/7`), which is a real cross-dataset regularity but is measured
   to 6.8–9.4 %, not 0.1 %; it passes at **1.39σ** (K8). On the Ω_Λ side the claim is already **3.8σ**
   from the repo's own DESI DR2 + Pantheon+ + Planck-prior fit (K23), **1.0σ** from Pantheon+, and
   **0.11σ** from Planck — the "agreement" is a choice of dataset.

---

## 1. Task 1 — the number and its distance from every determination

**The value** (K1, two arithmetic engines plus the published string):

```
32π/147 = 0.6838841151        (10 decimal places)
        = 0.6838841150671658  (float; mpmath 50-digit and sympy 40-digit agree to 0.0e+00)
```

| determination | Ω_Λ | σ | pull of 32π/147 | source / status |
|---|---|---|---|---|
| **Planck 2018 TT,TE,EE+lowE+lensing** | **0.6847** | **0.0073** | **−0.112σ** | the brief; also rebuilt as 1−Ω_m from Ω_m = 0.3153 (K5) |
| theory's own H0 footing | 0.683800 | 0.01015 | +0.008σ | Λc²/(3H₀²), H₀ = 67.4 ± 0.5 — **circular**, see below (K6) |
| Pantheon+ (flat ΛCDM; SNe alone) | 0.666 | 0.018 | **+0.994σ** | Brout+2022, Ω_m = 0.334 ± 0.018 (K24); SH0ES calibrates the absolute scale, not the shape, so Ω_m is the same number in the Pantheon+/SH0ES fit |
| repo DESI DR2 BAO + Pantheon+ + Planck 3pt priors | 0.69797 | 0.00368 | **−3.82σ** | A46's flat-ΛCDM fit, σ from the Δχ² = 1 profile (K23) |
| the same fit, 2pt CMB compression | 0.68999 | 0.00589 | −1.04σ | K23; the less physical variant — it lets Ω_b h² float to 0.01955 against the BBN/Planck 0.02236, and only this variant brings the prediction inside 1σ |

**Agreement is dataset-dependent.** Planck and the theory's own footing sit on the prediction;
Pantheon+ is 1σ low; the repo's own BAO+SNe+CMB fit is 3.8σ high. The spread between the
determinations is **0.032** — 39× the 8.2×10⁻⁴ offset the claim is about (K25). The two extremes differ by 0.032 (1.7σ given their own errors); the prediction is
1σ from one and 3.8σ from the other. It is bracketed, not confirmed: no single Ω_Λ is within 1σ of both. **A number whose offset is 39× smaller than the
dataset spread is not being tested at 0.11σ.**

### 1.1 The error bar that the 0.11σ comparison drops

`Ω_Λ = (32π/3)(a0/cH0)²` is exact at κ = ½ (K2, K3). The `a0` that fixes it is measured:

| footing | a0 | σ(a0)/a0 | implied Ω_Λ | pull from 1/7 | pull from Planck |
|---|---|---|---|---|---|
| canonical (BRIEF) | 9.36e-11 | 9.389 % (SPARC bootstrap) | 0.68388 | +0.01σ | — (zero error by construction) |
| joint fit (A71) | 8.544e-11 | 6.83 % (stat) | **0.5705 ± 0.0779** | **−1.39σ** | **−1.47σ** |

(K7, K8.) The joint fit's `a0` is **1.39σ below** the value that gives 32π/147, and it implies
Ω_Λ = 0.571 ± 0.078 — 1.47σ from Planck. That is the honest comparison: the error on Ω_Λ propagates
as **twice** the fractional error on `a0`. **The 0.11σ figure is the distance from an exact number to
a measurement; it is not the theory's error bar.** With SPARC's 9.4 % the canonical footing's Ω_Λ is
±0.128 (18.8 %).

This is the logical fork, and both branches fail the "prediction" claim:

| reading | what is predicted | what is tested | result |
|---|---|---|---|
| `a0` is an input (measured) | **nothing** — Ω_Λ is a function of two measured numbers | 32π/147 vs Planck is number-vs-measurement | 0.11σ, no evidence value |
| 147 is structural | `a0 = cH0/7` | the `a0` measurement, at 6.8–9.4 % | 1.39σ, passes weakly |

**You cannot have it both ways.** If `a0` is measured, Ω_Λ is not predicted. If 147 is structural,
then the prediction is `a0 = cH0/7` and the Planck comparison is a tautology — and the test is the
9 % `a0` measurement, not 0.1 %.

### 1.2 Dependence on the H0 footing (K19)

At fixed Λ, `Ω_Λ ∝ H0⁻²` exactly: `dlnΩ/dlnH0 = −2.000000`. A **0.5 km/s/Mpc** shift in H0
(0.74 %) moves Ω_Λ by **1.00×10⁻² = 12.3× the 8.2×10⁻⁴ offset**. The claimed agreement is therefore
12× finer than the H0 footing on which it is computed. The theory's own Λ is not independent
evidence: `Λ = 3Ω_pred H0²/c² = 1.08913×10⁻⁵²` against the quoted `1.0890×10⁻⁵²` (1.2×10⁻⁴ relative,
i.e. the 4-significant-figure rounding); `a0` from that Λ is 9.35417×10⁻¹¹ against 9.36×10⁻¹¹. **The
pair (Λ, a0) satisfies the closure because Λ was written as 32πa0²/c⁴; κ = ½ is defined by the pair,
not predicted by it** (K4, K6).

### 1.3 Dependence on curvature (K18)

`Ω_Λ = 1 − Ω_m − Ω_k`, so `dΩ_Λ/dΩ_k = −1`. Planck's 1σ curvature, `Ω_k = 0.0007 ± 0.0019`
(TT,TE,EE+lowE+lensing+BAO), shifts Ω_Λ by **2.33× the offset**; the Planck-only closed-universe
preference `Ω_k = −0.044` shifts it by **53.9×**. **The claim is only defined in flat ΛCDM**, and the
curvature error is larger than the effect it is claiming.

---

## 2. Task 2 — is 147 structural?

**Criterion.** A structural origin must produce `7 = cH0/a0` (or 147 directly) from the theory's own
field content — a mode count, a lattice coordination number, a topological invariant — *without using
`a0`, `H0` or `Λ`*. Anything that uses those is a restatement. This is the criterion A62 applied to
κ = ½ and A1 to 1/12.

| # | construction | arithmetic | exact? | forced? | status |
|---|---|---|---|---|---|
| 1 | Friedmann 8π/3 | `Ω = (8π/3)(2/7)²`, residual 0 | **exact** | no — `(2/7)² = 4(a0/cH0)²` is the measured ratio | identity (K20) |
| 2 | 147 = 3(cH0/a0)² | at a0/cH0 = 1/7 → 147 exactly | **exact** | no — it *defines* 147 from the measured ratio | tautology (K20) |
| 3 | 32 = 8/κ² | at κ = ½ → 32 exactly | **exact** | no — κ = ½ is the thing A62 could not derive | restatement (K20) |
| 4 | g_*(recombination) = 3.91 | 147/3.91 = 37.5959 (miss 0.40) | no | — | fails (K26) |
| 5 | g_*(electroweak) = 106.75 | 147/106.75 = 1.3770 (miss 0.38) | no | — | fails (K26) |
| 6 | N_eff = 3.046 | 147/3.046 = 48.2600 (miss 0.26) | no | — | fails (K26) |
| 7 | e-folds N_e = 60 | 147/60 = 2.4500 (miss 0.45) | no | — | fails (K26) |
| 8 | 1/α = 137.036 | 147/137.036 = 1.0727 (miss 0.07) | no | — | fails (K26) |
| 9 | 2⁷ = 128 | 147/128 = 1.1484 (miss 0.15) | no | — | fails (K26) |
| 10 | e-folds, ln(10⁶⁴) | 147.365 (0.25 % high) | no | — | approximate only (K26) |
| 11 | 3 spatial × 7², 7 = D−3, D = 10 | 3(10−3)² = 147 | **exact** | **no — D = 10 is chosen, no link to Ω_Λ** | numerology (K26) |
| 12 | 32π = 8·4π solid angle | `Ω = (4π/3)(2√2/7)²`, exact restatement | **exact** | no — 2√2/7 is chosen | numerology (K20) |
| 13 | horizon area ratio | `A_dS/A_a0 = 4(a0/cH0)² = 1/49`, exact | **exact** | no — 49 is the measured input | tautology (K20) |
| 14 | cell count | `(R/ℓ₀)² = 3Ω/8π = 4/49`; 147 would need 1/147 | no | — | fails (A27's cell, K20) |
| 15 | Gauss–Bonnet | α_GB is a total derivative in 4D; no dimensionless 147 | no | — | no mechanism |
| 16 | 147 = 7·C(7,2) | 7·21 = 147 | **exact** | no — both factors chosen | numerology |
| 17 | A33's background bound | `147/(32π) = 1.462236` vs the quoted 1.462 | to 1.6×10⁻⁴ | no — `1/Ω_Λ = ρ_crit/ρ_DE` is a flat-budget identity (A46 §2) | tautology (K21) |

**Every exact row is either an identity in the measured ratio `a0/cH0` and in κ, or a chosen integer
(D = 10, or 7·C(7,2)); zero are forced derivations.** The counting constructions (rows 4–10) all miss by
0.07–0.45 in the integer, i.e. by 7–45 %, not by a rounding.

**The record already agrees.** A1 K13 (labelled in `a1_checks.py` as the "numerology control"): "`a0/(cH0)
= 1/7` to 5.62e-4 — a tighter integer hit than 1/12, **hence no derivation**". A31 C13 records the same
arithmetic as **BACKED**, which in that ledger means "same value and same meaning", not "derived". A37: "The
record's `a0/(cH0) = 1/7` **numerology** is exactly `L_MOND = 7.00 c/H0` … which is why the coincidence
exists at all and why it carries no information about κ." A62's status for the whole 2Z/κ = ½ cluster is
**NO-GO(obstruction)**.

**What changed in `THEORY.md` §6.1 is the label, not the evidence.** That sentence upgrades the same
5.6×10⁻⁴ coincidence to "a prediction, not a fit" with no new derivation; it also misprints the value as
`0.683827` (exact: **0.6838841151**, 5.7×10⁻⁵ higher) and the pull as `0.13σ` (exact: **0.112σ**).
Both errors are small and neither changes the verdict, but they sit in the one sentence that carries it.

---

## 3. Task 3 — the look-elsewhere

**Pool (K10).** Atoms `{1, 2, 3, 4, 5, 7, 8, π, e, √2, √3}` (11), operations `+ − × ÷` and unary `√`,
**at most three operations**, both operand orders, deduplicated by value at 10⁻¹⁰ and restricted to
`[10⁻³, 10³]`:

```
260,129 distinct closed forms          (A62's pool: 156,210)
 18,452 of them in the band [0.5, 0.9]
```

**Counts (K11).**

| window | hits near 0.6847 |
|---|---|
| ±8.0×10⁻⁴ (the task's 0.11σ) | **65** |
| ±8.16×10⁻⁴ (the target's own distance = 0.112σ) | **66** |

The target itself sits at 8.16×10⁻⁴ = **0.112σ**, *just outside* the round 0.11σ window — a first sign
that "0.11σ" is a rounded-up claim.

**Base rate (K12).** 2000 random targets uniform in [0.5, 0.9], seed 73:

```
mean 75.3 hits, median 75, range 37–117
P(≥1 hit) = 1 − exp(−75.3) = 1.000000
fraction of targets with at least one hit = 1.000 (2000/2000)
```

**The base rate is 100 %.** Every value in the band has dozens of closed forms within 0.11 % of it; the
question is not whether such a form exists but which one you write down.

**Comparison with 11.5776 (K13).** Density in hits per unit *relative* window per 1000 pool members:

| target | pool | density |
|---|---|---|
| 32π/147, ε = 0.112σ | this pool (260,129) | **106.5** |
| 11.5776, ε = 1 % | this pool | **187.0** |
| 11.5776, ε = 1 % | A62's pool (223/156,210) | **71.4** |

All three are O(10²), all have P(≥1) = 1. **32π/147 is neither more nor less remarkable than the
11.5776 hit A62 already rejected**; the factor is 1.5–1.8, and it points in opposite directions
depending on which pool is used. In A62's own terms: 223 hits at 1 % was "no evidence"; 65 hits at the
target's own window is the same density to within a factor 1.5.

**The target's own family (K14).** Inside the functional family that 32π/147 belongs to — `kπ/n` with
k ≤ 64, n ≤ 400 — **15 values** land within the target's window, **14 of them other than 32π/147**.
Even a numerologist who restricts to the prediction's own shape has fourteen rivals.

**The two-operation rival (K15).**

```
√3 − π/3 = 0.684853256      dev = 1.53×10⁻⁴     2 operations
32π/147  = 0.683884115      dev = 8.16×10⁻⁴
```

**The rival is 5.32× closer to Planck, with two operations.** This is the direct
analogue of A62's `√134`, which matched 11.5776 to 1.5×10⁻⁴ with two symbols.

**Verdict of Task 3: the hit is generic.** 65 hits, P(≥1) = 1, fourteen same-shape rivals, and a
two-operation form five times closer. The look-elsewhere control does not merely weaken the claim; it
removes the only evidence the number had.

---

## 4. Task 4 — the falsifier, the alternatives, and the verdict

### 4.1 The pre-registered kill conditions

**(a) Ω_Λ at 3σ (K17).** To exclude 32π/147 at 3σ one needs

```
σ(Ω_Λ) ≤ |0.6847 − 0.683884|/3 = 2.72×10⁻⁴  (0.0398 %)
```

Planck has 7.30×10⁻³ — **26.8× too coarse**. The repo's own DESI DR2 + Pantheon+ fit has 3.68×10⁻³ —
13.5× too coarse — and already sits 3.8σ away. **No quoted measurement or forecast in this repo reaches
0.04 %.** On the Ω_Λ side the claim is unfalsifiable with foreseeable cosmology.

**(b) a0 at 3σ — the reachable test.** The equivalent statement is `a0 = cH0/7`. The joint fit's `a0`
is 8.72 % below it with 6.83 % errors (**1.39σ**). A 3σ exclusion needs

```
σ(a0)/a0 ≤ 8.72 %/3 = 2.91 %
```

A71's Gaia DR4 wide-binary forecast gives σ(κ) = 0.040, i.e. **4.0 % → 2.2σ**; one more independent
channel reaches 3σ. **This is the only falsifier that is both reachable and decisive** — and it tests
`a0 = cH0/7`, i.e. the *integer 7*, not the Ω_Λ packaging.

**(c) Model dependence.** The claim is defined only for flat ΛCDM with w = −1. DESI DR2 prefers
w₀w_a over ΛCDM at 2.8–4.2σ depending on the SNe sample, and free curvature at Planck-only precision
moves Ω_Λ by 53.9× the offset (K18). Any w ≠ −1 or Ω_k ≠ 0 makes "Ω_Λ" a different number; the
prediction has no meaning outside the model in which it was computed.

### 4.2 The nearest simple alternatives (K16)

| value | Ω_Λ | pull from Planck |
|---|---|---|
| 3/8 | 0.375 | +42.42σ |
| 2/3 | 0.6667 | +2.47σ |
| 0.7 | 0.700 | −2.10σ |
| 0.69 | 0.690 | −0.73σ |
| 0.68 | 0.680 | +0.64σ |
| **11/16** | **0.6875** | **−0.38σ** |
| **32π/147** | **0.683884** | **−0.11σ** |

Planck's 1.07 % precision **cannot separate 32π/147 from 11/16 (0.38σ), 0.68 (0.64σ) or 0.69 (0.73σ)** —
all are inside 1σ. `11/16` is a two-integer rational with no theory behind it and it fits as well as the
"prediction". A prediction that is 0.38σ from a rival is not sharp at the precision of the data.

### 4.3 What would make it a prediction

One thing, and only one: a derivation of the integer **7** from the P-sector's own structure — a
coordination number, a mode count, a topological invariant, a lattice sum — that does **not** use `a0`,
`H0` or `Λ`, plus a stated measurement that can separate it from 11/16 at 3σ. The derivation does not
exist in the record (A1, A37, A62 all say so), and the measurement does not exist either. The
register should require both before the word "prediction" is used.

---

## 5. Checks (26/26 PASS, exit 0, 0.1 s)

| id | what it proves | measured |
|---|---|---|
| K1 | value to ten digits, two engines + published string | 0.6838841151; engine dev 0.0; string dev 1.1e-11 |
| K2 | Ω = 32π/147 ⟺ a0/(cH0) = 1/7 | symbolic residual exactly 0 |
| K3 | the closure at that point is κ = ½ | residual exactly 0 |
| K4 | a0 from Λ by two routes; vs a0_can | 9.35417e-11 both; 6.3e-4 from 9.36e-11 |
| K5 | Planck pull, Ω rebuilt from Ω_m | 1−0.3153 = 0.6847; z = −0.1118 |
| K6 | the theory's H0 footing and its circularity | 0.683800 (1.2e-4); Λ_needed 1.08913e-52 (1.2e-4) |
| K7 | canonical a0 vs 1/7 at its own precision | 5.62e-4; 4 simple fractions inside 1σ |
| K8 | joint-fit a0: r, pull, implied Ω_Λ | r = 0.130476 ± 0.008910; −1.39σ; Ω = 0.5705 ± 0.0779 |
| K9 | κ_DE/κ_P3 = 1/√Ω_Λ; footing separation | 1.20923 / 1.20851; 3.34σ |
| K10 | pool ≥ 200,000 | 260,129; band 18,452 |
| K11 | hits at 0.11σ, two counting routes | 65 (66 at the target's own window); routes agree |
| K12 | random-target base rate | 75.3 mean; P(≥1) = 1.0; 2000/2000 |
| K13 | density vs both 11.5776 baselines | 106.5 vs 187.0 vs 71.4 per unit window |
| K14 | the target's own kπ/n family | 15 inside, 14 rivals |
| K15 | the two-operation rival | √3−π/3, dev 1.53e-4, 5.32× closer |
| K16 | nearest simple alternatives | 3/8 42.4σ … 11/16 0.38σ |
| K17 | 3σ precision requirement | 2.72e-4 (0.0398 %); 26.8× Planck |
| K18 | curvature dependence | 1σ = 2.33× gap; closed = 53.9× |
| K19 | H0-footing sensitivity | slope −2.000000; 0.5 km/s/Mpc = 12.3× gap |
| K20 | 147 = 3(cH0/a0)², 32 = 8/κ², area ratio, Friedmann and solid-angle forms | five exact identities, residuals 0 |
| K21 | 1/Ω = 147/32π vs A33's 1.462 | 1.462236; 1.6e-4; 1/Planck 1.460494 |
| K22 | 1/7 and 1/(2Z) are different numbers | Z 5.788810, 2Z 11.577620; ratio 1.653946 |
| K23 | repo DESI DR2 + Pantheon+ pull | 3pt 0.69797 ± 0.00368, z = −3.82; 2pt −1.04 |
| K24 | Pantheon+ pull | 0.666 ± 0.018, z = +0.99 |
| K25 | dataset spread | pulls −3.82 … +0.99, width 4.82 |
| K26 | no standard count gives 147 | g_*, N_eff, N_e, 1/α, 2⁷ all miss; 3(10−3)² exact but chosen |

**Mutations:** 12 (`planck_sigma`, `h0_70`, `denom_148`, `omega_0688`, `kappa_051`, `pool_1op`,
`a0_alt`, `curvature`, `pantheon_om`, `desi_om`, `kappa_p3`, `family_small`), each changing one input,
each exit **1**, each breaking a named check; **26/26 checks killed** by at least one (`MUTATE.md`).
No check had to be deleted.

---

## 6. What this does not do

1. **It does not prove that no derivation of 7 exists.** It proves the record has none, and that every
   exact route currently written down is an identity in the measured ratio. A future derivation from the
   P-sector's mode structure would reopen the case — that is exactly the missing leg.
2. **It does not re-analyse DESI DR2 or Pantheon+.** The DESI numbers are A46's own flat-ΛCDM fit to
   the 13 BAO + 1580 SNe + 3 CMB points on disk, with σ from the Δχ² = 1 profile computed here; the
   Pantheon+ number is Brout+2022's SNe-only Ω_m. The DESI 3pt and 2pt variants differ because of the
   known 2.3σ DESI/CMB Ω_m tension, and that split is reported, not resolved.
3. **It does not claim 32π/147 is false.** It is 0.112σ from Planck; it may yet be true. The audit is
   about whether the *evidence* supports calling it a prediction, and it does not.
4. **The pool is one choice of atoms and operations.** The base rate is a property of that pool; the
   ordering by description length (a 2-operation rival 5× closer) is not. A different pool changes 65
   by a factor of order unity, not by the orders of magnitude needed to rescue the claim.

---

## VERDICT

**Ω_Λ = 32π/147 = 0.6838841151 is 0.112σ from Planck (0.6847 ± 0.0073), +0.99σ from Pantheon+
(0.666 ± 0.018), −3.82σ from the repo's own DESI DR2 + Pantheon+ + Planck-prior fit (0.69797 ± 0.00368)
and −1.04σ from its 2pt variant (0.68999 ± 0.00589) — an offset that is a choice of dataset and is
39× narrower than the spread between them; 147 is not structural, because 147 = 3(cH0/a0)² and
32 = 8/κ², i.e. the integer is defined by the measured ratios the claim is meant to explain, every exact
route to it is that identity or a chosen integer (3(D−3)² with D = 10), and no physical count (g_*, N_eff,
e-fold number, 1/α) lands on it; the look-elsewhere base rate is 100 % (65 closed forms within 0.11σ in a
260,129-value pool, 75.3 hits on average for any value in [0.5,0.9], P(≥1) = 1.000000, and a two-operation
rival √3 − π/3 is 5.32× closer than the prediction); the kill condition on the Ω_Λ side is σ(Ω_Λ) ≤
2.72×10⁻⁴ (0.0398 %), 27× beyond Planck and unreachable, while the reachable test is the equivalent
a0 = cH0/7 at σ(a0)/a0 ≤ 2.91 % (currently 1.39σ with 6.8 % errors, 2.2σ at A71's wide-binary forecast).
**Therefore this is not a parameter-free prediction. It is a numerical coincidence — the measured ratio
a0/(cH0) = 1/7 restated in Ω_Λ units, with the integer 147 manufactured from the same two numbers it
claims to predict — and it should be labelled as such in the register: NUMEROLOGY (a coincidence, with a
falsifiable corollary H0 = 7a0/c that is a real 9 %-precision regularity, not a 0.1 % prediction).
