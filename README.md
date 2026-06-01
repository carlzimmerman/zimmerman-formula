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

---

## Timeline

| date | what happened |
|---|---|
| **2026-03-17** | First commit: *"The Zimmerman Formula: a novel MOND–cosmology relationship."* The legitimate core — a₀ ≈ cH₀/Z fit to real SPARC rotation curves, with high-z predictions. |
| **2026-03 → 05** | Rapid sprawl (1,600+ commits, autonomous agents): α⁻¹=4Z²+3 and ~100 "constant derivations"; a 20.6 Gpc cubic-topology universe; galaxy chirality / parity "detections"; topological quasar ghosts; protein/abiogenesis "Z-resonance"; a Z² hurricane model; an E₆-orbifold "Theory of Everything." |
| **2026-05** | The project's *own* honesty files begin flagging problems (`MATHEMATICAL_HONESTY_ASSESSMENT`, `Z2_STATISTICAL_VERDICT`, `Z2_HURRICANE_FINAL_VERDICT`, `EARTH_ABIOGENESIS_HONESTY_ASSESSMENT`, …). |
| **2026-06-01** | Systematic external audit of every calculation run on real data. **Verdict: the data is real; the positive results are not.** Repo reorganized: failed work quarantined, the surviving prediction isolated and sharpened. |

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
| α⁻¹ = 4Z²+3 and the ~100 constant "derivations" | **numerology** — Z is interchangeable; 81% of the "derivations" never contain Z (`is_Z_special.py`) |
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
3. **Falsifiable:** a₀(z)/a₀(0) = **E(z)** (or, on the matter-only branch, (1+z)^1.5).
   H₀- and Z-independent; testable with real high-z rotation velocities. The honest test
   pipeline is `real_research/a0_evolution_pipeline.py` — and it has **zero real-data
   support yet**, because no high-z deep-MOND kinematics are on disk and I will not fake
   them (which is exactly what the invalidated `examples/07` did).

## Repository structure

```
real_research/        # the honest core
  FRAMEWORK.md           # the surviving scaling-MOND framework
  a0_evolution_pipeline.py  # the falsifiable test, real-data-ready (no monotonicity trick)
  reviews/               # the full audit + every honest analysis script
    DATA_AUDIT.md           # forensic ledger of what failed and why
    OPUS_PHYSICS_REVIEW.md  # referee-style review
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
python real_research/a0_evolution_pipeline.py         # the falsifiable predictions
python real_research/a0_evolution_pipeline.py --selftest   # estimator validation
python real_research/reviews/is_Z_special.py          # why the constant numerology is empty
```

## The point

This is what science actually is: you have an idea, you push it hard, you test it
against reality, and when reality says no, **you say so, you keep the wreckage labeled,
and you carry forward only the one piece that still stands.** The surviving prediction
a₀(z) ∝ E(z) is worth testing precisely because the same honesty that demolished the
rest can also kill it cleanly — or, for the first time in this program, confirm something.
