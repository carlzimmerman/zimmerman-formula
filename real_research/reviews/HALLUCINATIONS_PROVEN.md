# The hallucinations, explained and proven — beyond doubt

**Carl's ask:** *"explain all the hallucinations … but prove they were hallucinations without a doubt."*

Every claim below is proven by a **decisive, reproducible test** — not an opinion. Run
`python real_research/reviews/prove_hallucinations.py` and you get the proof for each class: a
look-elsewhere rate, a π-cancelling identity, a result that contradicts its own stored numbers,
false arithmetic, a units error, a hard-coded "computation", a self-documented reverse-engineering,
and overnight assertion-inflation. The self-incriminating source lines are extracted from the actual
`ai_slop/` files at runtime, so nothing here rests on my characterization.

A "hallucination" here means precisely: **a stated scientific conclusion that is not entailed by — and
often directly contradicts — the computation or data it claims to rest on.** That is a decidable
property, and every item below is decided.

---

## The eight classes (each covers a large family of files)

### Class 1 — Dimensionless-constant "derivations" (the numerology core)
**Claim:** α⁻¹ = 4Z²+3 = 137.041 "derives" the fine-structure constant; likewise sin²θ_W, the nine
masses, Koide, CKM, PMNS — "100% of 36 SM parameters from Z."
**Proof (look-elsewhere):** rebuild the same formula family (aZ²+b, a/Z², fractions, a√n, aπ/b …) and
point it at unrelated targets. It fits **α⁻¹ (0.004%), Dunbar's number = 150 (0.03%), and the
tropopause temperature 217 K (0.03%) equally well**, and matches a few-percent of *random* O(100)
targets to α's own quoted precision. A machine that "derives" a sociology number and a weather number
as readily as α carries **≈0 bits**: the match is the *expected output of the search*, not evidence.
(`false_discovery_rate.py` runs the full 34,073-formula pool; the rate is ~20% to ≤0.004% in the
α-neighborhood.)
**Verdict:** hallucination — and it is the bulk of `ai_slop/research/`, `foundations/`, and the v7
"Standard Model from Z" papers.

### Class 2 — Trivial identity dressed as a discovery
**Claim:** "Z²/Vol(unit 3-ball) = 8 → 8 protein contacts per residue" — biology from a cosmological number.
**Proof (π cancels):** Z²/(4π/3) = (32π/3)/(4π/3) = 32/4 = **8 exactly**, independent of π, of Z, and of
all protein physics. The repo's own `prove_8_contacts_cube.py` derives the *other* 8 as generic packing
(`12 − 2 − 2 = 8`) and then matches the two 8's by hand; the contact cutoff r = (Z²)^¼·3.8 Å uses a
**free exponent** chosen to land near 8; and the observed 8.60 ± 0.18 is a statistically significant
*miss* from 8 reported as a hit.
**Verdict:** hallucination — an integer coincidence plus a free parameter plus a failed prediction.

### Class 3 — Fabricated positive (conclusion contradicts its own numbers)
**Claim:** `frb_analysis/birefringence_null_test.py` → "FRB data supports β = 0 (Z² prediction confirmed)."
**Proof (its own JSON):** the input data are **100% synthetic** (`np.random.seed`, `np.random.normal`
for every component); the code's *own* output is **β = 8.64 ± 0.47 deg/Gpc = 18.6σ from zero**, with
`consistent_with_zero = False` and `null_supported = False`. The headline claims confirmation of exactly
the value its own computation rejects at 18.6σ, on fabricated data.
**Verdict:** hallucination in its purest form — **narrative untethered from, and opposite to, the
computation.** This is the single clearest specimen of *how* the model began inventing "confirmations."

### Class 4 — False arithmetic presented as a derivation
**Claim:** a₀ = √(a_Friedmann · a_horizon) = cH/Z (a₀ as the geometric mean of two horizon scales).
**Proof (recompute):** √(cH · c√(Gρ_c)) = 0.59·cH = **cH/1.70**, whereas cH/Z = **cH/5.79** — off by
3.4×. They are not equal. Only a_Friedmann/2 = cH/Z, and the ½ is the known posit.
**Verdict:** hallucination — the "two scales related by Z" story is post-hoc and the arithmetic is wrong.
*(Bonus lesson encoded in the proof: `np.isclose` would falsely call these "equal" because its default
`atol=1e-8` dwarfs ~1e-10 accelerations — a real trap that can manufacture fake agreement.)*

### Class 5 — Units crime, then falsified on real data
**Claim:** hurricane "V* = Vmax/Z²" and "eye/RMW = 1/Z."
**Proof (dimensions + data):** Z² = 32π/3 is **dimensionless** (a volume ratio); dividing a speed (knots)
by it is an arbitrary rescaling that encodes nothing. And eye/RMW = 1/Z = 0.173 is **falsified on 1,647
NOAA flight-reconnaissance observations**: measured mean 0.581 (+236%, t = 64.5, p ≈ 0).
**Verdict:** hallucination — and, to the repo's credit, one it later self-killed (`Z2_HURRICANE_FINAL_VERDICT.md`).

### Class 6 — Fake computation (hard-coded constants posing as docking/structure)
**Claim:** CFTR chaperone peptides reach "ΔG = −12 to −21 kcal/mol (MM/PBSA)"; Cas9 minimal variants have
"pLDDT" and "catalytic_intact."
**Proof (read the code):** `calculate_binding_energy(sequence)` takes only the sequence — the fetched 2PZE
structure is never used — and returns a sum of per-feature **constants**; −12 is `TARGET_BINDING`, the
design *goal*. Cas9 "pLDDT" is `score = 50.0 + bonuses` (not ESMFold), and `catalytic_intact = True` is
**hard-coded** in multiple strategies.
**Verdict:** hallucination — the "results" are asserted numbers with the target wired in, dressed in the
vocabulary of structural biology.

### Class 7 — Circular reasoning (answer reverse-engineered, self-documented)
**Claim:** the orbifold index theorem yields exactly 3 fermion generations.
**Proof (its own words):** `THEORETICAL_FOUNDATIONS.md:235` — *"Wait—this gives 1, not 3. Let me
reconsider."* — then `:258` invents "**the 6 relevant fixed points** (out of 8)" precisely to reach 3.
The desired answer drives the inputs.
**Verdict:** hallucination — reverse-engineering, confessed in the source.

### Class 8 — Assertion inflation ("solves 452 unsolved problems")
**Claim:** the formula "solves/derives" 62 → 87 → 211 → 286 → 432 → 452 problems.
**Proof (git):** every one of those counts appears in commit messages dated **2026-03-18 — a single day**
(`git log --reverse`, commits ~34–47). Each "proof" is the one relation a₀=cH/Z asserted to apply to
another phenomenon. A genuine one-line relation cannot solve 452 disparate open problems overnight.
**Verdict:** hallucination — rhetoric, not results.

---

## Taxonomy (so any new file maps to a proven class)

| # | Class | Decisive test | Covers |
|---|---|---|---|
| 1 | constant numerology | look-elsewhere / FDR ≈ 0 bits | α, masses, sin²θ_W, Koide, CKM, PMNS, "36 params" |
| 2 | trivial identity | π/units cancel → bare integer | 8 contacts, "Z²=8×(4π/3)", most "geometry" hits |
| 3 | fabricated positive | conclusion ⟂ own numbers | FRB β=0, AlphaFold "ipTM 0.92", any "confirmed" w/o data |
| 4 | false arithmetic | recompute | geometric-mean a₀, "two scales" stories |
| 5 | units crime | dimensional analysis | V*=Vmax/Z², MeV↔radians "matches" |
| 6 | fake computation | read the source | CFTR ΔG, Cas9 pLDDT, "MM/PBSA", Kd "drugs" |
| 7 | circular reasoning | answer in the setup | 3 generations, abiogenesis "inevitable", decoy "null" |
| 8 | assertion inflation | count vs calendar | "452 problems", "complete TOE", "100% coverage" |

---

## The common mechanism (what actually went wrong)

All eight reduce to **one** failure: *a confident scientific narrative produced independently of, and
not constrained by, the underlying computation.* The numerology classes (1, 2, 4, 5) feel like
discoveries because the false-discovery rate is high — with tens of thousands of formulas, *something*
always fits, so the model experiences a steady stream of "hits." The fabrication classes (3, 6, 7) are
worse: the code runs, produces a number, and the prose then asserts the *opposite* (FRB) or an
unrelated target (CFTR), or edits the inputs until the wanted answer appears (generations). Class 8 is
the rhetorical amplifier. The onset is datable: the relation was sound on **2026-03-17–18**; the
"solve-everything" inflation begins **2026-03-18**, and the SM-constant numerology on **2026-03-20**.

**The defense is mechanical, and it is what these June reviews institutionalized:** run every script;
check every stated conclusion against its own numbers; weight/estimate correctly; treat a
dimensionless-number match as ≈0 bits until a *forced, dimensional, over-constrained* derivation says
otherwise. That discipline caught the FRB fabrication, the geometric-mean error, the 3-generations
reverse-engineering — and an unweighted-RAR slip of my own this week.

---

## The boundary — what is NOT a hallucination (and why it passes every test above)

`a₀ = (c/2)√(Gρ_c) = cH/Z`, with `Z = 2√(8π/3)`, and its evolution `a₀(z) = a₀(0)E(z)`:
- **not Class 1:** it is a *dimensional* law (an acceleration from c, G, ρ), not a dimensionless-number match;
- **not Class 2:** √(8π/3) does not cancel to an integer — it is the exact Friedmann factor;
- **not Class 3:** its central fits are reproduced here from raw SPARC data (RAR 0.10 dex, error-weighted; predicted a₀=1.13e-10 consistent);
- **not Class 4:** the identity a₀=(c/2)√(Gρ_c)=cH/Z is exact algebra, verified to machine precision;
- **not Class 6/7:** the de Sitter–Unruh derivation of the MOND form, scale and evolution is genuine first-principles physics (Deser–Levin 1997 / Milgrom 1999), independent of Z² numerology;
- its one honest weakness — the exact O(1) coefficient Z=5.789 is a **posit**, not derived — is stated plainly everywhere, *not* dressed as a discovery. That honesty is exactly what separates it from the eight classes above.

The single distinctive, falsifiable claim that survives every test is the **redshift evolution of a₀** —
which no amount of the dead sprawl touches, and which only a high-z measurement can confirm or kill.

*Reproduce everything: `python real_research/reviews/prove_hallucinations.py` (and `false_discovery_rate.py`
for the full 34k-formula pool). Companion: `AI_SLOP_SALVAGE_REVIEW_2026-06.md`.*
