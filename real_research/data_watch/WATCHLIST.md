# Data-watch — trigger → pre-registered response → owner file (Prompt DW)

*C. Zimmerman, 2026-06-10. The registry that turns a new result into a pre-committed action. Pair with `ROUTINE.md`
(the daily-scan runbook) and `arxiv_watch.py` (the stdlib arXiv harvester; weekly cron-able, dedup via `seen.json`,
dated digests → `digests/`). Footing rule applies to every assessment: judge on the framework's OWN terms
(a₀=9.36×10⁻¹¹, ρ_DE footing, declining √ρ_DE branch, Υ≈0.70); verify a "kills it" as hard as a "confirms it";
mark **WATCH** when uncertain; never manufacture a hit nor reflexively dismiss one. Zero `ai_slop/` dependency.*

## How to run
```
python real_research/data_watch/arxiv_watch.py --days 7        # weekly; prints new candidates, marks seen
python real_research/data_watch/arxiv_watch.py --json --no-mark   # machine-readable dry run
```
Then for each candidate, match against the table below; if it fires a trigger, execute the response pipeline and
write a dated digest to `digests/YYYY-MM-DD.md` (committed; `seen.json` + `log/` stay gitignored).

## The registry
| # | Trigger (what to watch for) | Pre-registered response pipeline | Owner file(s) |
|---|---|---|---|
| **1** | **Gaia DR4 release** (~late 2026) — line-of-sight RVs / 3D wide-binary velocities | **The pre-registered decider.** Re-run D1/D2/D4 (`wb_exact_replication.py`) + the deprojection MC (`wb_deprojection_mc.py`) with **3D** velocities; the 3D data break the boost↔contamination degeneracy and constrain the (a,e) orbital prior (WB-3b). Report verdict against the locked outcomes. **F4 fork (added 2026-06-10, pre-DR4):** under vector-MI at the framework a₀ the deep-bin velocity boost is **F4 ≈ +4%** vs soft-shape MOND ≈ +13–16% (flat plateau, no separation trend) → a clean DR4 null at ~3% kills soft shapes but **F4 survives**; a +10–15% detection **kills F4**; only ~2%-level sensitivity tests F4 itself (`reviews/toe_law/mi_f4_widebinary_efe.py`). | `reviews/public_data/WB_PROGRAM_SUMMARY.md`, `WB_DEPROJECTION_MC_RESULTS.md` |
| **2** | **MUSE-DARK IV / any new kinematic a₀(z) point** (Ciocan-class) | Feed the new (z, a₀, σ) into the **a₀(z) compilation fit within days**, hierarchical systematic included; test declining √ρ_DE vs constant vs rising ∝√ρ_total. Footing: framework's declining branch, NOT the ΛCDM-apparent rise. | `reviews/.../A0Z_MUSE_DARK_III_CONFRONTATION.md`, `project_a0z_muse_confrontation` |
| **3** | **DESI DR3** (~2027) — updated w₀,wₐ | Re-run the w(z)-dependent numbers (a₀(z) lag band, ρ_DE ratios). **Meta-falsifier (record explicitly):** if w reverts to −1, the framework's distinctive evolving content **collapses to constant-a₀** (degenerates to ordinary MOND) — that is the hostage, log it as such either way. | `FALSIFICATION_MATRIX.md` (a₀(z) row), `project_zimmerman_coefficient_footing` |
| **4** | **Chae or Banik response / catalog update** (new cuts, DR4 reruns, rebuttals) | Transcribe the cut/pipeline deltas into `wb_published_cuts.md`; re-gate the replication (±10%); re-run the affected diagnostics. Replication-fidelity rule applies. | `reviews/public_data/wb_published_cuts.md` |
| **5** | **AeST / Skordis-Zlosnik & Verwayen-class papers** (relativistic-MOND theory, ghost spectra, K(Q) construction) | Check against the **V(Q) construction assumptions** and the AeST = LEANING-PINNED label; does it pin or unpin δQ/Q₀, the tilt term, or the ghost spectrum? Update the door-3/AeST disposition. | `reviews/door3_bimond_*.py`, `dQ_bounds.py`, the AeST label |
| **6** | **ELT/HARMONI commissioning + JWST/ALMA high-z rotation-curve papers** (z≳3 kinematics) | C3-preparation: stage the high-z BTFR-offset-sign and EFE-vs-z tests; the declining-a₀(z) prediction (×0.96/0.81/0.70 at z=1/2/3) becomes testable. **C3 fence: stage only — no a₀(z) claim from z=0 data.** | `reviews/public_data/OBSERVATIONAL_PROGRAM.md` (C3 folder) |

## Discipline notes
- **Keep it dumb and reliable:** the harvester only fetches + dedupes; all judgment is human/Claude-in-session per `ROUTINE.md`.
- **Both-ways, every time:** entries 1 and 3 can each kill OR confirm the framework; record the kill condition with equal weight.
- **Prior-sensitivity rider (from WB-3b):** any future WB significance — ours or a published one — is orbital-prior-limited until
  3D velocities pin the (a,e) library; carry that caveat into every DR4-triggered assessment.
