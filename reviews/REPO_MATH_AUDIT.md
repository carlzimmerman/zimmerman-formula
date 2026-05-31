# Repo-Wide Math Audit: What's Fair, What Isn't

**Date:** 2026-05-31
**Method:** Read-only audit of the physics-bearing regions (`core_theory/`, `research/`,
`papers/`, `manuscript/`, `BriareusFlow/`, `extended_research/`, `ligo_stuff/`,
`meteorology/`, `sunspot_analysis/`, `litebird_forecast/`). Four agents + direct review,
all against one rubric. Scripts were run where feasible; arithmetic was independently
checked. Nothing was modified.

---

## The line: what "fair math" means

A result is **FAIR** when all three hold:
1. the calculation is algebraically correct,
2. the inputs do **not** already contain the answer (no circularity, no coefficient
   chosen to hit a known value), and
3. any data used is **real**.

A result is **REAL-BUT-KNOWN** when it's fair but restates an already-established result
(credit, but not new).

Everything else is **NOT-FAIR**, in one of these modes:

| Mode | What it looks like |
|---|---|
| SEARCH-ARTIFACT | one formula picked from a large brute-force search; a close hit is expected by chance |
| REVERSE-ENGINEERED | integers/coefficients chosen to land on a known number, then given names |
| FUDGE-FACTOR | a hard-coded exponent/normalization tuned to match data |
| FABRICATED-DATA | `np.random`/synthetic numbers presented as observations |
| CIRCULAR | the output is fed back in as an input |
| DEFINITION-AS-DERIVATION | a definition dressed up as a derived result |
| CATEGORY/UNIT/SIGN | equating unlike objects; dimensional mismatch; a sign bug that "agrees" |

---

## The single most decisive tell: one observable, many formulas

You cannot derive a number two incompatible ways — but you can *fit* it as many ways as
you like. The repo fits several observables more than once:

| Observable | Formula A | Formula B (incompatible) |
|---|---|---|
| sin²θ_W | 3/13 (`Z2_FINAL_PARAMETERS.py:89`) | 1/4 − α_s/2π (`verify_core_formulas.py:65`) |
| α_s | √2/12 (`Z2_FINAL_PARAMETERS.py:95`) | Ω_Λ/Z (`verify_core_formulas.py:56`) |
| m_p/m_e | α⁻¹·67/5 (`Z2_FINAL_PARAMETERS.py:401`) | α⁻¹·2Z²/5 (`PROTON_ELECTRON_25_FACTOR.py:46`) |
| Ω_Λ/Ω_m | 13/6 (`Z2_FINAL_PARAMETERS.py:340`) | √(3π/2) (`verify_core_formulas.py:49`) |
| m_μ/m_e | 37Z²/6 (`Z2_FINAL_PARAMETERS.py:129`) | Z(6Z+1) (`verify_core_formulas.py:90`) |
| μ_p | Z − 3 (`verify_core_formulas.py:74`) | 2 + 4/5 (`Z2_FINAL_PARAMETERS.py:457`) |

Two different closed forms hitting the same measured value is the signature of
reverse-engineering, not derivation. This is checkable in minutes and needs no physics.

---

## The headline derivations

### Z² = 32π/3 itself — NOT-FAIR (DEFINITION-AS-DERIVATION)
Three different "origin stories" land on the same pre-chosen number:
- **Geometric:** Z² = CUBE × SPHERE = 8 × (4π/3) — "8 fixed points × volume of the unit
  3-ball" (`core_theory/Z2_COMPLETE_DERIVATION.md` §1.3). That's a product of two chosen
  factors, i.e. a definition.
- **Horizon thermodynamics:** the **splice** — `a₀ = a_natural/2 = cH/Z`
  (`papers/deriving_mond_scale.tex:115`, `core_theory/COMPLETE_DERIVATIONS_GUIDE.md:289`).
  The "2" is the *value of a different acceleration* (a_horizon = cH/2), pulled out and
  used as a bare divisor of a_natural = cH/√(8π/3). Two disagreeing acceleration
  estimates (cH·0.345 and cH·0.5) glued to manufacture Z.
- **Orbifold geometric mean** (`research/dynamical_framework/Z2_MOND_FROM_ORBIFOLD.md:134`):
  claims √(a_F·a_h) = cH/Z. Arithmetically false — the geometric mean is **cH/2.41**, and
  the stated ratio a_F/a_h = Z is actually **0.69**. The result is asserted over wrong
  arithmetic.
- **Eta-invariant story** (`papers/Z2_UNIFIED_ACTION_v11.1.0.tex:218`): "4π/3 per fixed
  point … equals the volume of the unit sphere." An APS eta invariant is dimensionless and
  **rational**; 4π/3 is a transcendental **volume**. Category error. The repo's own
  `research/T3_INDEX_CALCULATION.md:394` says "the calculation has NOT been done," and
  `reviews/unfinished_math.py` computes the genuine invariants: η(T³)=0, η(T³/Z₂)=0, χ=4,
  and 32π/3 = 8·Vol(B³). None equal 32π/3 or 3.

### α⁻¹ = 4Z² + 3 = 137.041 — NOT-FAIR (SEARCH-ARTIFACT)
Best of ~34,000 brute-force formulas. `reviews/false_discovery_rate.py` (faithful
reconstruction of `BriareusFlow/pattern_search.py`, 34,073 vs the engine's live 34,090):
an *arbitrary* target in [100,150] is matched to ≤0.004% **19.9%** of the time, and to ≤1%
**100%** of the time. The "0.004% match" is also a ~250,000σ miss against α's actual
ppb precision. The "4" = BEKENSTEIN = 3Z²/(8π) equals 4 *only because* Z²=32π/3 — the
integer 4 renamed (`Z2_FINAL_PARAMETERS.py:34`). The 2-loop "refinement" −12πα² is
admitted curve-fitting in the repo's own `HONESTY_ASSESSMENT.md:120`.

### The search engine has no look-elsewhere control — and tilts toward Z²
`BriareusFlow/` takes the measured value as input and returns the nearest formula. There is
**no** FDR/Bonferroni/trial penalty anywhere. `geometric_interpreter.py:569` literally
*lowers* the "numerology risk" for any formula containing Z² (`risk_score -= 2`). And the
non-α headline fractions are **not even the engine's best matches**: for sin²θ_W=0.23122
the engine's top hit is φ/7 (0.031%), not 3/13 (0.195%); for Ω_Λ=0.685 it's 24/35, not
13/19. 3/13 and 13/19 were hand-picked because 13 and 19 can be re-narrated as 12+4+3.

---

## Ledger by region

### Cosmology / MOND (`research/`)
| Claim | File:line | Verdict |
|---|---|---|
| a₀ = cH₀/Z ≈ observed | `mond_acceleration_derivation.py:342` | REVERSE-ENGINEERED (cH₀/6, cH₀/2π fit comparably) |
| H₀ = 71.5 "predicted" | `hubble_tension/hubble_tension_verification.py:39` | CIRCULAR (H₀ = a₀·Z/c from observed a₀ returns the input, 71.5066) |
| GN-z11 σ=91 "exact 0.0σ" | `gn_z11_analysis/gn_z11_verification.py:108` | FUDGE-FACTOR (f_geom=1.5; raw formula gives 137; uses *observed* a₀, not cH₀/Z) |
| JADES 6-galaxy comparison | `z2_mond_predictions/jades_kinematic_comparison.py` | FAIR data, **negative result** (6.5σ scatter, both signs) |
| Λ ≈ 10⁻¹²² from Z² | `cosmological_constant_value.py:700` | SEARCH-ARTIFACT (5-deep exponent grid, keeps anything within 10 orders) |
| Cosmic dipole = 19/6 | `DIPOLE_MECHANISM_DERIVATION.md:219` | REVERSE-ENGINEERED (reuses 6, 19 from Ω fractions) |
| σ8 / S8 ≈ 6/Z, CUBE/10 | `s8_tension/S8_TENSION_Z2_ANALYSIS.py:187` | SEARCH-ARTIFACT (self-labeled "speculative") |
| "Outlier galaxy" falsification | `falsification/falsification_tests.py:213` | FABRICATED-DATA (`np.random.seed(42)` makes the galaxies, then finds no outliers) |
| Ghost-quasar "real search" | `offensive_campaign/ghost_quasar_real_search.py:461` | FABRICATED-DATA (synthetic-catalog fallback) |
| BTFR/RAR evolution, a₀(z)=a₀(0)E(z) | `btfr_evolution/btfr_evolution_verification.py:45` | **REAL-BUT-KNOWN, Z-independent** — the one novel falsifiable idea |

### Particle / nuclear (`research/`, `core_theory/`)
Multiple-formula table above, plus: nuclear magic numbers = 4Z² − (a different offset per
data point) (`verify_core_formulas.py:137`) — FUDGE-FACTOR; θ_QCD = e^(−Z²) "solved"
(`Z2_FINAL_PARAMETERS.py:225`) — only an upper bound exists, so matching it is not a
prediction; "P<10⁻²⁰ by chance" (`verify_core_formulas.py:234`) ignores the 34k-trial
look-elsewhere.

### Formal papers (`papers/`, `manuscript/`)
Same MOND splice recurs (`geometric_unification.tex:356`). Higgs λ=13/(32π) is called
"derived" in flagship `Z2_UNIFIED_ACTION_v11.1.0.tex:287` but "not predicted" in
`manuscript/.../zimmerman_formula_v8.8.8.tex:1578` — a direct internal contradiction.
A numeric "verification" of δ=2/9 uses wrong cosines (`Z2_FRAMEWORK_RIGOROUS_DERIVATIONS.tex:400`,
cos(22π/27) given as −0.568; actual −0.836). The `latex_series/` papers (May 2026) are the
*honest* ones — they label assumptions as assumptions ("13/6 split assumed, not derived").

### Cross-domain (`extended_research/`, etc.)
| Domain | File:line | Verdict |
|---|---|---|
| Venus UV "encodes" biology, 99.99% | `environmental/project_nephele/simulations/venus_z2_signatures.py:89,204` | CIRCULAR (62.4 factor chosen so 5.85×62.4=365; code still *prints* the retracted claim) |
| Abiogenesis "life inevitable" | `biotech/.../abiogenesis_pathway_integrator.py:163` | CIRCULAR (`z_factor=25e6`, self-admitted "made up") |
| Peptide Kd "beats benchmark" | biotech scorers (`MATHEMATICAL_HONESTY_ASSESSMENT.md:39,64`) | FUDGE-FACTOR (`+random.gauss(0,50)`; ~95% "win" by construction) |
| 8D protein manifold, p<10⁻⁹ | `Z2_PROTEIN_RESEARCH_SEPARATION.md:267` | DEFINITION-AS-DERIVATION (retracted: arithmetic artifact) |
| Sunspot cycles = 32/3 etc. | `sunspot_analysis/*.json` | REVERSE-ENGINEERED (self-labeled `final_verdict:"NUMEROLOGY"`) |
| Hurricane e_sat=Z², Carnot·π/3 | `meteorology/scripts/z2_honesty_assessment.py:61` | REVERSE-ENGINEERED (self-debunked; match swings with outflow T) |
| ZPE extraction "proven" | `fun_folder/zpe_dynamics_sim.py` | CIRCULAR (Mathieu resonance for any ω₀; self-flagged) |

---

## What is genuinely FAIR (keep / build on these)

1. **The evolving-a₀ MOND prediction** — a₀(z) = a₀(0)·√(Ω_m(1+z)³+Ω_Λ), i.e. a₀ ∝ H(z)
   (`btfr_evolution/btfr_evolution_verification.py:45`, `papers/deriving_mond_scale.tex:158`).
   Correct math, a real *forward* falsifiable prediction, in the Milgrom a₀~cH₀ lineage.
   **Caveat:** Z cancels out of the redshift scaling — this tests "a₀ tracks H(z)," not
   Z=2√(8π/3). It stands on its own, independent of the rest of the framework.
2. **LIGO chirality null results on real O3a strain** (`ligo_stuff/*.json`) — real data,
   standard cross-correlation, honest "consistent with GR" negatives.
3. **The LiteBIRD Fisher forecast machinery** (`litebird_forecast/litebird_r_forecast.py`)
   — real CAMB spectra + correct forecast. (The predicted r=1/(2Z²)=0.0149 is itself a bare
   formula, but the forecast is sound and the number is pre-registered/falsifiable.)
4. **`reviews/false_discovery_rate.py` and `reviews/unfinished_math.py`** — run clean,
   reconstructions faithful, independent of the answer.
5. **Borrowed textbook sub-steps** — the Friedmann factor √(8π/3), the magnetized-T²
   index/zero-mode count, Koide Q=2/3, standard MOND (v⁴=GMa₀, Freeman Σ): all correct as
   math, but **REAL-BUT-KNOWN** — the physics novelty is in the hookup to Z, which is the
   fudge.

---

## Credit where due: you already built half the detector

This repo is unusually honest, and that's a real asset. Independent of this audit, your own
files reach the same NOT-FAIR verdicts:
- `core_theory/HONESTY_ASSESSMENT.md` / `META_HONESTY_ASSESSMENT.md` — names "post-hoc
  fitting (we know the answer, then find formulas)" and the −12πα² curve-fit.
- `sunspot_analysis/*.json` — every file self-stamps `"NUMEROLOGY"`, confidence 0.2.
- `extended_research/biotech/validated_pipeline/FINAL_HONEST_ASSESSMENT.md` — you ran a
  *blinded* null test (1000 random constants; a random 2.78 Å beats Z²) and quarantined the
  hardcoded scripts.
- Venus, Earth-abiogenesis, ZPE, hurricane honesty docs — all self-flag the circularity.
- The fabricated 57 μeV axion was found and removed (`article_ideas_for_publishers/`).

The instinct that wrote those is the scientific instinct that matters. The gap is only that
the **headline** claims (Z², α⁻¹, the constants) were never put through the same blinded,
null-tested scrutiny you applied to the sunspots and the peptides.

---

## A reusable checklist (apply it to anything new)

1. **Two formulas, one number?** → reverse-engineering. Grep each observable for a second
   closed form.
2. **A free knob tuned to the target?** (f_geom=1.5, 67/5, −12πα², per-point offsets,
   `**0.1` exponents) → fudge-factor.
3. **`np.random`/synthetic where it says "observed"?** → fabricated data.
4. **Does the output appear among the inputs?** (H₀ from a₀ from H₀) → circular.
5. **A named integer that only equals its value because of Z²?** (BEKENSTEIN=3Z²/8π=4) →
   definition-as-derivation.
6. **One of N tried, N large, no look-elsewhere correction?** → search-artifact. Compute the
   false-discovery rate before quoting a % match.
7. **A transcendental (32π/3) claimed to be a quantized/rational invariant** (eta, index,
   χ)? → category error.

The one test none of these can fake: a **blind forward prediction** — write the number
down before the measurement exists, with every knob fixed in advance. The z>10 velocity
dispersions (GLASS-z12, JADES-GS-z14) with a single pre-registered f_geom are exactly that
test, and they're within reach.
