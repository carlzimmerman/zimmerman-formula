# project_atomos

**Goal.** Replicate the *process* that produced the one genuinely novel result of the zimmerman-formula program —
a₀ = c²√(Λ/32π), found by brute-force symbolic regression (`hali_flow`/`bruteflow`) and then *validated* by a forced
kernel — and aim that same process at the open structural questions of particle physics (the fermion mass spectrum,
the CKM and **PMNS** mixing matrices, the gauge couplings, θ_QCD — the Standard Model's free parameters).

This is **not** a numerology generator. The entire value of the project lives in the gate that tells a *real* relation
from a *fitted coincidence*. Read the next section before touching anything.

---

## The one lesson that makes this science, not numerology

Brute-force symbolic regression over physical constants will **always** find formulas that match a target number. With
enough operators and constants, π's and integers, a search of 10⁵–10⁶ expressions hits any 4-digit target by chance.
The zimmerman-formula corpus proved this the hard way: **164 FDR-dead re-labelings** of the SM masses (4Z²+3, 64π+Z,
Z+11, λ⁶…, 6π⁵, 3/13) all "matched" and all died under a false-discovery-rate test. A match is worthless on its own.

**What made a₀ real was not the fit. It was the *forced kernel* and the *interlock*:**

- a₀ = c²√(Λ/32π) carries the kernel **√(8π/3)**, which decomposes *uniquely* as
  **√(8π)** [Einstein's field-equation normalization, ρ_Λ = Λc²/8πG] × **√(1/3)** [Friedmann's coefficient,
  H² = 8πGρ/3]. Both factors are **forced by General Relativity *before any fitting*.**
- The **same** √(8π/3) therefore appears in **two independent forced places** (Einstein *and* Friedmann), and the
  **form** a₀ ∝ √Λ is forced *a third* way (the dS–Unruh quadrature, Deser–Levin). That is an **overdetermined,
  interlocking** system — the structure is pinned from several directions at once, not fitted once.
- Only **one** number in the whole relation is free: the outer factor κ = ½ (Z = √(32π/3) = 2·√(8π/3); the "2" = 1/κ
  is the lone unforced O(1)). A one-parameter relation, not a tuned one.

So the discovery had two halves, and **both** are required:
1. **SEARCH** (hali_flow/bruteflow): brute-force symbolic regression over *anonymized* variables → candidate relations.
2. **VALIDATE** (the gate): a candidate is real only if it (a) survives an FDR test against the search-space size, **and**
   (b) has a **forced kernel** (a coefficient pinned by symmetry/geometry before fitting), **and** (c) **interlocks** —
   the same structure forces ≥2 independent observables, or ties ≥3 constants with one parameter (Koide-class).

A candidate that fits but doesn't interlock is a coincidence. **That is the filter Carl asked for** ("a way to check
for the interlocking mechanisms"), and it is the heart of this project.

---

## The honest prior (both ways — do not flinch from it, do not be defeated by it)

The zimmerman-formula corpus already ran this question once for the SM **mass** sector and found a structural reason it
is hard: **an asymmetry of forced kernels.** Gravity forces √(8π/3) before fitting; the SM Yukawa sector hands the
masses **no analogous forced kernel** — charged-lepton masses are eigenvalues of a *free* Yukawa matrix. That is why
the cosmology trick worked for a₀ and every transferred mass formula died (`project_particle_numerology_standing`).

**But** — and this is why the project is worth doing:
- **Koide Q = (Σmₗ)/(Σ√mₗ)² = 2/3 is a real, FDR-surviving, parameter-free interlock** (~1-in-44,000), a 45-year
  unsolved puzzle. It ties three masses with one geometric constraint (√-mass vector at 45° to (1,1,1)). The framework
  only *re-labels* it (r=√2 left free), but the **interlock itself is real** — exactly the signature this machine hunts.
- **Mixing matrices (PMNS especially) are structured**, not random — near-tri-bimaximal, small θ₁₃ — and the standard
  explanation is a **discrete flavor symmetry** (A₄, S₄, Δ(27)). Symmetry-forced structure is precisely the
  forced-kernel/interlock class this machine is built to detect. Carl's instinct that "it's probably geometric" lands
  in the right neighborhood (S₃/triality is where Koide already lives).
- The only way to *know* is to build the disciplined machine and run it. If the SM sector is genuinely kernel-free, this
  machine will report **FDR-dead, honestly**. If a geometric interlock is hiding (Koide-class, or in PMNS), this machine
  is the thing that can find it **and certify it instead of fooling us**.

We will not manufacture a win, and we will not high-priest a real signal away. Same bar both directions.

---

## Non-negotiable design principle: CALIBRATE before you trust

Before this machine is pointed at PMNS, it must prove itself on **known answers**:
- **Known positives it must re-find and certify:** a₀'s forced kernel √(8π/3); the Koide Q=2/3 interlock.
- **Known negatives it must reject:** the 164 FDR-dead SM re-labelings (4Z²+3, 64π+Z, 6π⁵, …).

If the machine cannot reproduce the *one* real discovery and reject the *known* coincidences, it is not trustworthy on
anything new. The calibration set lives in `calibration/` and is the first acceptance test. This is also the literal
answer to "find out what exactly we did to get this discovery": a machine that can re-derive it on demand.

---

## Architecture

```
engine/        symbolic-regression / autoresearch search   (adapted from hali_flow/bruteflow)
gate/          the validator: FDR test + forced-kernel detector + interlocking-mechanism check
calibration/   known positives (a0 kernel, Koide) + known negatives (164 FDR-dead) — the acceptance test
targets/       the SM free-parameter target list + which sectors have known mechanism hooks
results/       certified survivors + the honest FDR-dead ledger
notes/         design notes, verdicts, the running both-ways record
```

**Pipeline:** `engine` proposes candidate relations over anonymized SM constants → `gate` subjects each to the
three-part validation (FDR survival · forced kernel · interlock) → only candidates passing **all three** are reported as
leads; everything else is logged FDR-dead with its tell. Geometric/symmetry frameworks (discrete flavor groups, polytope
/ root-system constructions, Clifford/division-algebra angles) are first-class hypotheses, tried systematically.

## Provenance
- Search engine lineage: `~/new_physics/hali_flow/` (`bruteflow/engine.py`, `exhaustive_engine.py`, `symbolic_search.py`).
- Validation lineage: `~/new_physics/zimmerman-formula/real_research/reviews/false_discovery_rate.py`, `.../mass_fdr/`,
  `.../opus_48_extended_research/reviews/koide_dsunruh/` (Koide + cube-sphere FDR).
- Discipline lineage: the project's #1 working rule (test on its own terms; verify a "fails" claim as hard as a "works"
  claim; never manufacture a hit nor reflexively dismiss one).

*Local git, no remote. Independent of zimmerman-formula (no shared state; reads its artifacts read-only for calibration).*
