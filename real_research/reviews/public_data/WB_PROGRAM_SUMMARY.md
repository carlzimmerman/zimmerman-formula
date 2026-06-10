# Wide-binary program — synthesis & final state (for Fable)

*C. Zimmerman, 2026-06-10. Single entry point to the Gaia wide-binary thread: what was tested, what was found, what
remains. Real data throughout (El-Badry+2021 eDR3, Zenodo 4435257). Framework footing a₀=9.36×10⁻¹¹. C1/C2 only — the
program says NOTHING about a₀(z) (C3 fence). Inline execution, no swarms, fully pre-registered.*

## The question
Chae 2023 reports a ~5σ low-acceleration velocity **boost** in Gaia wide binaries (MOND-like); Banik 2024 reports a
~16σ **Newtonian null** on the same kind of data. Same catalog, opposite verdicts. Which methodological fork flips it,
and what does the framework's a₀ say?

## The arc (5 commits, each pre-registered before results)
| Stage | What | Result | Commit |
|---|---|---|---|
| WB-1/2 | first pass + stop-trigger diagnostics | both triggers fired on a *loose hybrid* sample → HALT | (earlier) |
| **WB-R1** | faithful Chae/Banik **selection** replication + per-paper mass pipelines | **Outcome A**: D1≈0.12–0.15, D2≈0.10, D4≈1.3–1.4× — all below triggers | `3681dd17` |
| WB-R2/3 pre-reg | deprojection-MC forward model + decision rule | committed before running | `09fbec76` |
| **WB-3** | matched deprojection Monte-Carlo | **degeneracy-limited**: data ~3σ over flat-Newton, absorbed by separation-dependent contamination | `284462b8` |
| WB-3b | real modified-gravity **orbit integration** | framework's own WB prediction is **orbital-prior-sensitive** → reinforces degeneracy | `258e625c` |

## Three findings that are FIRM (gate- and method-robust)
1. **D4 robust (1.3–1.4×):** the deep-bin super-escape is **not** a mass-estimator artifact — Fable's single biggest worry, resolved.
2. **A real mass-pipeline bug, caught and fixed:** inverting the Banik cubic outside its valid M_G window inflated velocities;
   it had produced a spurious ~0.48 (and the WB-2 0.27) super-escape. Faithful value ≈ **0.10**. Both earlier numbers retracted.
3. **Faithful super-escape ≈ 0.10 for BOTH teams' cuts**, stable across the RUWE 1.2–1.4 bracket — the clean sample is usable.

## The verdict: **AMBIGUOUS / degeneracy-limited — the framework is NOT excluded**
- The deep-MOND median ṽ rises modestly (0.56→0.65→0.82). Calibrated on the high-acceleration anchor, the data sit **~3σ above
  the flat-contamination Newtonian baseline** and **far below** the naive boost.
- That 3σ excess is **fully absorbed** by a separation-dependent triple fraction (~0.16 in the deep bins) that *independently*
  matches the measured super-escape → **the data do not require a boost.**
- But it is **not a Newtonian win either**: the deepest bin (N=104) keeps a residual; a *correctly-scaled* mild framework boost
  (~0.63–0.66) sits right on the reliable-bin data (0.647); and the framework's own integrated prediction is prior-sensitive.
- **Boost ↔ contamination is intrinsically degenerate in the sky-projected DR3 observable.** Neither confirmed nor excluded.

## What would decide it
**Gaia DR4 (late 2026): line-of-sight radial velocities → full 3D deprojection**, which (a) breaks the boost↔contamination
degeneracy and (b) constrains the orbital (a, e) prior that WB-3b showed the framework prediction depends on. This is the
pre-registered decider. (Three Banik cuts — astrometric χ²/ν eq.4, faint-companion search to mG<20, DR3-RV triple screen —
are also un-implementable from the eDR3 catalog and would tighten the sample further; logged as catalog/data-availability gaps.)

## Discipline applied (the methodological treacherous-item record)
Pre-registration before every run; hard ±10% sample-size gate; stop-and-report triggers honored (WB-2 HALT); hostile
verification reserved for any framework-favorable result; a real bug owned and scrubbed mid-stream; the retraction guard kept the
crude-MOND −22σ from being mis-stated as a falsification; both-directions reporting throughout (no manufactured boost, no
reflexive Newton). **Bottom line for the falsification matrix: wide binaries are currently a NULL-INFORMATIVE / degeneracy-limited
test at the framework a₀ — they neither validate nor invalidate; status = "awaiting Gaia DR4."**
