# Coefficient Footing Audit — cH₀ vs cH_Λ across the a₀/Z corpus

**C. Zimmerman, 2026-06-05.** Seeded by a real bug in [`THE_FACTOR_OF_FOUR.md`](../THE_FACTOR_OF_FOUR.md)
(the "thermal 2π" row used the measured `cH₀` where the pure-Λ `cH_Λ` was meant), a 24-agent reconciliation
workflow swept the ~40-file coefficient corpus for siblings. **Every number below was reproduced by running the
script or recomputing by hand.** Result, stated up front:

> The corpus's **canonical surface is clean** and the **"route-forced by GR, not uniquely forced" verdict is
> unchanged.** But the `THE_FACTOR_OF_FOUR` fix had **five un-fixed siblings** (now corrected), one self-labeled
> "PAPER-READY", and the consistency lesson **cuts against** one of the framework's softer marketing claims.

---

## 1. The bug class

The framework defines `a₀ = κ·c·√(Gρ_Λ)`, with `ρ_Λ = Λc²/(8πG)` the **dark-energy** density, and
`Z ≡ cH_Λ/a₀` where `H_Λ = c√(Λ/3)` is the **pure-Λ de Sitter rate**. The bug: computing a route's `a₀`/`Z`
from the **measured `H₀` / total critical density `ρ_c`** instead of the pure-Λ `ρ_Λ`/`cH_Λ`, while labeling the
result as the framework's value.

Since `ρ_c = ρ_Λ/Ω_Λ` and `cH₀ = cH_Λ/√Ω_Λ`, this inflates the "framework a₀" by exactly

```
cH₀/cH_Λ = 1/√Ω_Λ = 1.2082     (Ω_Λ = 0.685)
```

— turning the honest **9.36×10⁻¹¹** (which sits at the **low edge** of the data band) into **1.13×10⁻¹⁰** (which
sits dead-centre on the observed ~1.2×10⁻¹⁰). The match *looks* better; it is bought by silently abandoning the
a₀↔Λ thesis and reading a₀ off the **total** density (the rising-a₀ branch).

**Why the trap is subtle.** `Z = cH/a₀ = 2√(8π/3) = 5.789` is an **algebraic identity** of the `a₀=(c/2)√(Gρ)`
form for *any* `ρ,H` with `H²=8πGρ/3` — the `H` cancels. So "Z = 5.789 ✓, automatically via Friedmann" is a
**tautology** that confirms the *functional form*, never the data. The only genuine data content is (a) the
**magnitude** of a₀ (9.36e-11 = low edge of [9.0, 13]×10⁻¹¹), and (b) **which density** — ρ_Λ (dark energy,
declining branch) vs ρ_total (rising branch).

**Carve-out (NOT bugs):** files that *label* their basis (`ρ_c`/observed `cH₀` vs `ρ_Λ`) are transparent seams,
not errors; the genuinely-observed `cH₀/a₀ = 5.46–5.91` is a real, separate data statement; Verlinde `cH/6`,
McCulloch `2cH₀`, and the Wald a₀-blind Z-list are correct literature attributions.

## 2. Verified inconsistencies — all now FIXED

| file | what it printed as "the framework a₀" | corrected to | sev |
|---|---|---|---|
| `reviews/derive_Z_cleanest.py` | **1.13e-10**, "Z=5.789 MATCH", tagged **PAPER-READY** (ρ from `3H₀²/8πG`) | ρ→ρ_Λ; a₀=**9.36e-11**, Z=cH_Λ/a₀; Z labeled an identity | **high** |
| `reviews/entropy_coefficient_rigorous_endgame.py` | "FRAMEWORK geometric" row = 1.20e-10 directly above "observed = 1.20e-10" (manufactured match) | all readings on `cH_Λ`; framework=**9.93e-11** (@H₀=71.5); all below observed | med |
| `reviews/the_one_quarter_target.py` | a₀=1.20e-10 = observed; "Z²=32π/3 automatically" | shows ρ_Λ (9.93e-11, low edge) **and** ρ_c (1.20e-10, off-thesis); "can't have both" | med |
| `reviews/derive_Z_firstprinciples.py` | Step-2 a₀=1.13e-10 "MATCHES", no-prefactor 2.3e-10 | ρ_Λ values **9.36e-11** / **1.87e-10**; low-edge framing | med |
| `reviews/holographic_entropy_chase.py` | framework row = 1.13e-10 (cH₀/Z); Q1 called cH₀ "the de Sitter acceleration" | column relabeled `a₀=cH₀/Z`; note: native = cH_Λ/Z=9.36e-11; Q1 fixed | low |
| `reviews/OPEN_PROBLEM_yphi32_KQ.md` | **stale** cleanup pointer flagging a `THE_FACTOR_OF_FOUR` bug that was already fixed | repointed at the 5 siblings; marked APPLIED | low |

The dimensionless physics in each script (e.g. the 3.6% Verlinde-vs-geometric fork) was **correct and is
unchanged** — only the misleading absolute a₀ magnitudes and labels were corrected.

## 3. The canonical route ledger (single source of truth)

`Z` is defined by `Z = cH_Λ/a₀` with the **pure-Λ** rate `cH_Λ = 5.420×10⁻¹⁰` (`= c²√(Λ/3)`), **not** the
measured `cH₀ = 6.548×10⁻¹⁰`. All four motivated readings satisfy `κ·Z = √(8π/3) = 2.8944`.

| route | κ | Z = cH_Λ/a₀ | a₀ [m/s²] | a₀ = c²√(Λ/N) | π-power | branch | status |
|---|---|---|---|---|---|---|---|
| de Sitter raw (a₀=cH_Λ) | 2.894 | 1.00 | 5.42e-10 | N=3 | 0 | Λ | excluded (~6× too big) |
| **framework free-fall ½ (CANONICAL)** | **0.500** | **5.789 (=√(32π/3))** | **9.36e-11** | **N=32π=100.5** | **1** | **Λ / declining** | **in band, LOW EDGE — the prediction** |
| Jeans 1/√π | 0.564 | 5.13 | 1.06e-10 | N=8π²=79.0 | 2 | — | in band (central) |
| thermal 2π (cH_Λ/2π) | 0.461 (=√6/3√π) | 6.28 (=2π) | 8.63e-11 | N=12π²=118.4 | 2 | Λ / declining | just outside band (low) |
| no prefactor κ=1 | 1.000 | 2.89 | 1.87e-10 | N=8π | 1 | Λ | excluded (~2× too big) |
| Verlinde dS entropy (cH/6) | — | 6.000 (rational) | ~1.1e-10 (cH₀/6) | — (π-free) | — | Hubble | literature attribution, **not** a framework a₀ |
| **DATA-ALLOWED BAND** | **0.48–0.69** | **4.2–6.0** | **9.0–13e-11** | — | — | — | reference (data central ≈ κ 0.56–0.64) |

*The "π-power" column is just a restatement of the dimension/route diagnostic already in
[`FORCING_THE_COEFFICIENT.md`](../FORCING_THE_COEFFICIENT.md) (the `Z_d = 8√(π/d(d−1))` 3-D fingerprint): N∝π⁰
is pure de Sitter geometry, N∝π¹ adds the Einstein 8π (framework), N∝π² adds a second, statistical 2π (thermal /
Jeans). It is a clean reframing, not a new result.*

## 4. Two findings that cut honestly

**(a) The "data leans to Z=5.79" claim does not survive consistent footing.**
[`FORCING_THE_COEFFICIENT.md`](../FORCING_THE_COEFFICIENT.md) notes "observed cH₀/a₀ = 5.46–5.91, leaning slightly
to Z=5.79." That uses `cH₀` in the observed ratio while `Z` is defined with `cH_Λ` — the *same* cross-footing as
the bug. On consistent `cH_Λ` footing the observed ratio is `cH_Λ/a₀ ≈ 4.5–4.9`, i.e. **κ ≈ 0.56–0.64** — leaning
toward Jeans / higher-κ, *not* toward ½. Stated footing-free: the data give **κ ≈ 0.49–0.64** (central ~0.56–0.64
from McGaugh RAR); the framework's **½ is viable but at the low edge.** Enforcing consistent footing *removes* the
framework's strongest data-based claim to ½ — it does not strengthen it.

**(b) This conflation is the static shadow of the framework's *decisive* open test.**
The coefficient is empirically **moot**: every falsifiable prediction is Z-free because the evolution bridge
`a₀(z)/a₀(0) = √(ρ_DE(z)/ρ_DE,0)` cancels the coefficient exactly, and the ~28% interpolation-function (μ)
systematic on absolute a₀ is ~10× too coarse to ever select a reading (pairwise gaps: framework–thermal 8.2%,
framework–Jeans 12.1%, thermal–Jeans 20.2%; to split the tightest pair at 3σ needs σ(a₀) < 2.7%). The decisive
question is the **evolution branch**: does a₀ **decline** as √ρ_DE, or **rise** as ~E(z)? And
[`THE_DARK_ENERGY_TRACKING_READING.md`](../THE_DARK_ENERGY_TRACKING_READING.md) diagnoses the rising reading as a
**"ρ_total/ρ_DE conflation"** — which is the *exact same 1/Ω_Λ error* as the cH₀/cH_Λ bug, in the time domain.
(The corpus is internally inconsistent here: that file argues declining, while
[`A0Z_STATUS_CORRECTED.md`](../A0Z_STATUS_CORRECTED.md) flip-flopped and lands on rising.) **Enforcing ρ_Λ
everywhere simultaneously sharpens the coefficient story and settles the evolution branch toward the declining
√ρ_DE reading.** That is the real payoff of the consistency fix — and the live frontier.

## 5. New vs already-known

**New from this pass:** the 5 un-fixed siblings (one "PAPER-READY"); the stale pointer; the explicit
discrimination-precision table; and the observation that the "data-leans-to-Z" claim is itself a cross-footing
artifact, *and* that the static bug and the rising-vs-declining evolution fork are the same ρ_total/ρ_Λ error.

**Already in the repo (not re-credited here):** the "route-forced not uniquely forced" verdict
([`FORCING_THE_COEFFICIENT.md`](../FORCING_THE_COEFFICIENT.md), `COEFFICIENT_DEFINITIVE_VERDICT.md`); the three
clean readings and their triples ([`factor_of_four.py`](../predictions/factor_of_four.py),
[`coefficient_landscape.py`](../predictions/coefficient_landscape.py)); the already-fixed
[`THE_FACTOR_OF_FOUR.md`](../THE_FACTOR_OF_FOUR.md) and its "fan-out across ½" framing; the μ-systematic band; and
the labeled ρ_c-vs-ρ_Λ / H₀=67.4-vs-71.5 seams (transparent, not bugs).

## 6. Bottom line

The framework's **canonical documents are clean** and the verdict is unchanged. The cleanup that fixed
`THE_FACTOR_OF_FOUR.md` had simply **stopped at the headline file**; five derivation/"endgame" scripts — one
"PAPER-READY" — still read a₀ off the total density and so over-stated the framework's observational success by
1.208×. They are now consistent with the framework's own `a₀ = (c/2)√(Gρ_Λ)`. The honest picture they now show:
**a₀ = 9.36×10⁻¹¹ at the low edge of the data, Z = 5.789 a Friedmann *identity* not a measurement, and the real
open question is the redshift evolution of a₀ — not its prefactor.**

---

## 7. Addendum (2026-06-05, canonical-Z-convention pass)

After [`THE_FACTOR_OF_FOUR.md`](../THE_FACTOR_OF_FOUR.md) gained an explicit **"one canonical Z convention"** section
(with the guard reproduced in [`factor_of_four.py`](../predictions/factor_of_four.py) §5), a follow-up swept the
**prose** corpus and closed the items §4(a) had *diagnosed but not edited*, plus one new sibling class:

- **Type-(ii) prose now fixed** (the cross-footing this audit flagged): `FORCING_THE_COEFFICIENT.md` ("leaning
  slightly to Z") and `DOORS_LEDGER.md` ("lands *on Z* … data softly favor the framework's coefficient") now put the
  observed ratio on `cH_Λ` footing (`cH_Λ/a₀ ≈ 4.5–4.9`, κ≈0.56–0.64) **before** comparing, and state ½ is
  viable-but-low-edge. (§2's table had corrected only the `.py` siblings; the prose claims were left live.)
- **New sibling — a κ mislabeled as a Z** inside a Z-axis list, in two files: `COEFFICIENT_DEFINITIVE_VERDICT.md`'s
  "(every route's Z)" ladder led with "Milgrom `½`", and `OPEN_PROBLEM_yphi32_KQ.md` item D wrote "Z = 0.5 / 2π / 6 /
  5.79". In both, `0.5` is the framework **κ**, whose Z is the 5.79 already in the list (`κ·Z = √(8π/3)`); both are
  corrected, and the ladder is now labeled as a single `Z = cH_Λ/a₀` axis.

Canonical surface and verdict unchanged. A repo-wide rescan finds no remaining `softly favor` / `leans-to-Z` /
`Z = 0.5` cross-footing claims.
