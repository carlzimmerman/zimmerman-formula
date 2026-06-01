# The Zimmerman Formula — a post-mortem, and the one piece that survived

**Status (2026-06-01): most of this program is invalidated.** What began as a single
real observation — the MOND acceleration scale a₀ ≈ cH₀ — sprawled, largely under
autonomous AI agents, into ~1,650 commits of numerology and cross-domain overclaims.
A full audit against real open data found that **essentially all of the headline
claims fail.** This README documents that honestly, the way a lab notebook should
record a hypothesis that didn't survive contact with the data. One falsifiable
prediction is left standing; it is not yet confirmed, and it might be wrong too — but
it is real science, and it is testable.

> *"The first principle is that you must not fool yourself — and you are the easiest
> person to fool."* — R. Feynman. We fooled ourselves for a while. This is the correction.

**Update (2026-06-01, deepened review):** the one surviving prediction has now been **tested
against real 2026 data and is favored over the constant-a₀ null at 5σ** (p = 0.80 ± 0.17,
consistent with E(z)). It is *not* a unique confirmation — ΛCDM predicts a similar trend — but
for the first time in this program the data leans *toward* a claim rather than killing it. The
same deepened review also hardened the negatives: a **random number** reproduces α⁻¹=4Z²+3 and
the mass ratios as well as 32π/3 does, and the coefficient Z is not uniquely selected by the
data. See `real_research/EQUATIONS.md` and `real_research/WEB_SYNTHESIS.md`.

---

## Timeline

| date | what happened |
|---|---|
| **2026-03-17** | First commit: *"The Zimmerman Formula: a novel MOND–cosmology relationship."* The legitimate core — a₀ ≈ cH₀/Z fit to real SPARC rotation curves, with high-z predictions. |
| **2026-03 → 05** | Rapid sprawl (1,600+ commits, autonomous agents): α⁻¹=4Z²+3 and ~100 "constant derivations"; a 20.6 Gpc cubic-topology universe; galaxy chirality / parity "detections"; topological quasar ghosts; protein/abiogenesis "Z-resonance"; a Z² hurricane model; an E₆-orbifold "Theory of Everything." |
| **2026-05** | The project's *own* honesty files begin flagging problems (`MATHEMATICAL_HONESTY_ASSESSMENT`, `Z2_STATISTICAL_VERDICT`, `Z2_HURRICANE_FINAL_VERDICT`, `EARTH_ABIOGENESIS_HONESTY_ASSESSMENT`, …). |
| **2026-06-01** | Systematic external audit of every calculation run on real data. **Verdict: the data is real; the positive results are not.** Repo reorganized: failed work quarantined, the surviving prediction isolated and sharpened. |
| **2026-06-01** *(cont.)* | Deepened review. The surviving prediction tested on real 2026 high-z data (MUSE-DARK III, Vărăşteanu 2025, de Graaff 2024): **constant a₀ rejected at 5σ**, exponent p=0.80±0.17. The over-constrained web (+4 independent measurements) and a tiered equation sheet consolidated; the relativistic frontier and a first CMB calculation scoped; the constants shown reproducible by *any* base (a random number beats 4Z²+3); the published Zenodo papers mapped claim-by-claim. Full suite: 80/80 scripts pass. |

## What was invalidated, and why

Full evidence: **`real_research/reviews/DATA_AUDIT.md`** (six forensic audits across ~45
data scripts) and **`real_research/reviews/OPUS_PHYSICS_REVIEW.md`**. In short — the
data was genuinely downloaded (Planck, DESI, SDSS, Gaia, SPARC, RCSB, NOAA, LIGO…), but
**every defensible real-data measurement returned a null or a falsification**, and every
"detection" traced to one of: synthetic data dressed as real, circular self-injection
(generate data from the model, then "recover" it), a hardcoded/cited number, a units
bug, or unpenalized look-elsewhere.

| claim | verdict |
|---|---|
| α⁻¹ = 4Z²+3 and the ~100 constant "derivations" | **numerology** — 81% never contain Z (`is_Z_special.py`); a *random* number reproduces α and the mass ratios to the same precision (`can_another_number_do_it.py`); a 34k-formula search hits arbitrary O(100) targets to 0.004% ~20% of the time (`false_discovery_rate.py`) |
| Z² = η(T³/Z₂) = 8×(4π/3) "derivation" | **category error** — the eta density is 0 everywhere; a scale-free invariant can't equal a c³-scaling ball volume (`eta_local_bruning_seeley.py`) |
| 20.6 Gpc T³/Z₂ cosmic topology | **excluded** by Planck matched circles (`matched_circle_*`) |
| galaxy chirality / 7σ parity | the "7σ" is a *pasted citation*; real DESI runs are null (z=−0.08) |
| topological quasar ghosts | **none** — candidates ruled out by real BOSS spectra |
| wide-binary "16σ MOND" | a velocity **units bug** (ratios ~1000×) |
| protein / abiogenesis "Z-resonance" | 5.8 Å is trivial backbone geometry; PDB test gives z=−0.59σ; the sim is admittedly circular |
| Z² hurricane prediction | **falsified** on NOAA data (3.4× off, p≈0) |
| E₆-orbifold "Theory of Everything" | inherited model-building bolted on; derives nothing |

## What survived

One real anchor, one novel reading, one falsifiable prediction — written up in
**`real_research/FRAMEWORK.md`**:

1. **Real:** a₀ = (1.13 ± 0.06)×10⁻¹⁰ m/s² from the genuine 175-galaxy SPARC RAR
   (`real_research/reviews/sparc_rar_honest.py`). This is mainstream MOND, reproduced
   cleanly — but it is the 40-year-old Milgrom result, *not* evidence for the value Z.
2. **Novel (from the audit, not the original):** the coefficient's ½ is a **Schwarzschild
   surface-gravity** form a₀ = c²/2R of the cosmic free-fall scale — not de Sitter
   (`schwarzschild_factor_and_density_fork.py`). This is a genuine, if heuristic, new reading.
3. **Falsifiable — and now data-favored.** a₀(z)/a₀(0) = **E(z)**, H₀- and Z-independent.
   Two updates since the first audit: (a) the evolution is **derived** — horizon thermodynamics
   forces a₀ ∝ H(z) route-independently, and needs no Z (`reviews/horizon_a0_derivation.py`);
   (b) it has now been **tested on real 2026 data** — SPARC (z≈0), Vărăşteanu 2025 (z≈0.05),
   MUSE-DARK III 2026 (z≈0.9): fitting a₀(z)=A·E(z)^p gives **p = 0.80 ± 0.17**, with the
   **constant-a₀ null rejected at 5σ** and the matter-only (1+z)^1.5 branch *also* excluded at 5σ
   (`a0_powerlaw_confrontation.py`, `rar_evolution_test.py`). **Honest caveats:** the dominant
   uncertainty is a ~40% local-anchor systematic (SPARC 1.20 vs Vărăşteanu 1.69), and an evolving
   RAR is *also* expected in ΛCDM from halo evolution — so this is "favored over constant,"
   **not** a unique confirmation. The decisive test remains a clean deep-MOND a₀ at z>2.

The full structure these sit in — one premise, ~13 forced edges, a +4 over-constrained web, and
the honest boundary (no Standard-Model constants, no CMB without a relativistic completion) — is
written up in **`real_research/WEB_SYNTHESIS.md`**, with the tiered equation list in
**`real_research/EQUATIONS.md`**.

## Repository structure

```
real_research/        # the honest core
  FRAMEWORK.md             # the surviving scaling-MOND framework
  WEB_SYNTHESIS.md         # the whole over-constrained web, physicist-ready
  EQUATIONS.md             # full equation sheet, tiered by novelty
  SALVAGE_LEDGER.md        # systematic re-check of ai_slop (nothing salvageable beyond MOND)
  ZENODO_PUBLICATION_MAP.md  # the published papers mapped claim-by-claim (keep vs retract)
  REAL_WEB.py              # the over-constrained web (+4) + the generator
  a0_powerlaw_confrontation.py  # the 5σ data test of the evolving prediction
  can_another_number_do_it.py   # proof a random number reproduces the "constants"
  coefficient_uniqueness_test.py # the coefficient Z is not uniquely selected
  a0_evolution_pipeline.py # the falsifiable test, real-data-ready (no monotonicity trick)
  reviews/               # the full audit + every honest analysis script (80/80 pass)
    DATA_AUDIT.md           # forensic ledger of what failed and why
    OPUS_PHYSICS_REVIEW.md  # referee-style review
    false_discovery_rate.py # the look-elsewhere baseline for the constants
    sparc_rar_honest.py     # the real a0 anchor
    ...
  data/                  # real data on disk (SPARC, KMOS3D)
  papers/                # the v12 synthesis attempts (superseded by FRAMEWORK.md)

ai_slop/              # everything that failed/was invalid, PRESERVED not deleted
                      #   numerology, topology, chirality, ghosts, biotech,
                      #   meteorology, the E6 TOE, and the autonomous-agent swarm
                      #   (HermesFlow/TruthFlow/…) that generated most of it.
```

Nothing was deleted. Failed work is quarantined in `ai_slop/` as the historical record —
because documenting a dead end *is* part of the science.

## Reproduce

```bash
python real_research/reviews/sparc_rar_honest.py      # the real a0 = 1.13e-10 anchor
python real_research/a0_powerlaw_confrontation.py     # the evolving a0: constant rejected 5σ
python real_research/REAL_WEB.py                       # the over-constrained web (+4)
python real_research/reviews/is_Z_special.py          # why the constant numerology is empty
python real_research/can_another_number_do_it.py      # a random number "derives" the constants too
python real_research/reviews/false_discovery_rate.py  # the 34k-formula look-elsewhere baseline
```

## Preserved as open research

This repository is kept intact — warts and all — as a documented record of a research
program that mostly did not survive contact with data, because a *labeled* dead end is
more useful than a quiet deletion.

- **Nothing is deleted.** Every failed line of work is preserved under `ai_slop/`,
  including the autonomous-agent swarm that generated it and the multi-GB raw datasets
  (Planck/Gaia/LIGO/DESI), which are kept on disk (gitignored, not committed).
- **The audit is reviewable as a diff.** The session that audited the program and rebuilt
  the honest core is captured on two frozen branches — `baseline-pre-audit` (before) →
  `honest-core-rebuild` (after):
  <https://github.com/carlzimmerman/zimmerman-formula/compare/baseline-pre-audit...honest-core-rebuild>
- **Forward work continues** in `real_research/`, held to the bar the audit set: one real
  anchor (SPARC a₀), one posited number (the coefficient Z — *not* uniquely selected, and *not*
  derived: horizon thermodynamics derives the **evolution** a₀∝H but not the O(1) coefficient),
  one falsifiable prediction (a₀(z), now favored over constant at 5σ), and the honest open
  frontier (the CMB needs a relativistic completion — `toe_cmb_calculation.py` shows a₀ itself
  cannot be the clustering dark matter, so the work is a sharp, bounded question, not a TOE).

## The point

This is what science actually is: you have an idea, you push it hard, you test it
against reality, and when reality says no, **you say so, you keep the wreckage labeled,
and you carry forward only the one piece that still stands.** The surviving prediction
a₀(z) ∝ E(z) is worth testing precisely because the same honesty that demolished the
rest can also kill it cleanly — or, for the first time in this program, confirm something.
