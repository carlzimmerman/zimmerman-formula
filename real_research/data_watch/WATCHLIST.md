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
| **6** | **ELT/HARMONI commissioning + JWST/ALMA high-z rotation-curve papers** (z≳3 kinematics) | C3-preparation: stage the high-z BTFR-offset-sign and EFE-vs-z tests; the declining-a₀(z) prediction (×0.96/0.86/0.65–0.74 at z=1/2/3, per the paper §2.3) becomes testable. **C3 fence: stage only — no a₀(z) claim from z=0 data.** | `reviews/public_data/OBSERVATIONAL_PROGRAM.md` (C3 folder) |

## Discipline notes
- **Keep it dumb and reliable:** the harvester only fetches + dedupes; all judgment is human/Claude-in-session per `ROUTINE.md`.
- **Both-ways, every time:** entries 1 and 3 can each kill OR confirm the framework; record the kill condition with equal weight.
- **Prior-sensitivity rider (from WB-3b):** any future WB significance — ours or a published one — is orbital-prior-limited until
  3D velocities pin the (a,e) library; carry that caveat into every DR4-triggered assessment.

**7 (added 2026-06-10, Door IVb):** BepiColombo/MORE Mercury-ranging releases → re-run the solar-reflex test
(`reviews/toe_law/agentE_solar_reflex.py`) on the real arc: the framework-normalization signal brackets 0.4 cm–1.2 m
post-absorption vs MORE's ~1 cm verified accuracy — window-limited (2.5 yr vs the 11.86-yr carrier), decisive in the
upper bracket. Owner: `TOE_STATUS_AND_DOORS.md` §Door-IVb. (The constituent-acceleration reading — the sole surviving
per-body-F4 reading — is untouched by this channel; its coherence cost is on record.)

**8 (added 2026-06-11, agentM):** the DR4 wide-binary fork is RESHAPED by the named matter-sector template
(Milgrom-2022 + exponential tail, θ(0)-enhanced EFE): soft-shape boost cut to 4–10%; a clean ~3% null kills
soft-M22 only if θ(0)≲2; **+4–8% POSITIVELY SELECTS M22**; +10–15% kills the enhanced EFE for all shapes.
Supersedes the bare F4-vs-soft fork of entry 1 as the primary reading. Owner: `reviews/toe_law/agentM_milgrom2022_gauntlet.md`.

**9 (added 2026-06-11, agentP):** the coefficient contest's external adjudicators: (a) any third-party
adjudication of Dai–Stojkovic (1710.00946) vs Yoon (2003.03198) on Verlinde's derivation; (b) reproduction of
the 2601.01715 dSph 5.2σ claim — if reproduced, it is evidence FOR a ~9.0×10⁻¹¹ scale on the ρ_DE footing
(framework-relevant, advocacy-flagged). Owner: `reviews/toe_law/agentP_verlinde_coefficient.md`.

**10 (added 2026-06-11, agentS):** any published DSSYK contrastive calculation of the edge placement's late-time
observables (the field running our agentS discriminator): edge-fails confirms EDGE-WOUNDED → contest collapses
further; an edge-QNM rescue would re-symmetrize the gate. Owner: `reviews/toe_law/agentS_edge_qnm.md`.

**11 (added 2026-06-11, agentCC):** the deep-MOND flattening (a★) discriminators: (a) the AGC 114905 inclination
fight (2404.06537 deep-downturn vs 2408.05269/Lelli-2024 i≈15° reconciliation) — the one floor-shaped isolated
object; (b) BIG-SPARC release → re-run the agentCC two-branch fit on the enlarged deep sample; (c) any kinematics
of ISOLATED ultra-deep rotators (e_N ≲ 0.005, g_obs = 0.01–0.05 a₀, pinned inclinations) — the named decisive
test: a floor ⇒ universal downturn at one g_obs everywhere; EFE ⇒ none in isolation. Current bound: a★ ≤ 0.107 a₀
(95%, SPARC deep decade); the binding constraint stays agentBB's band line (a★ < 0.05 a₀), untested below.
Owner: `reviews/toe_law/agentCC_astar_hunt.md`.

**12 (added 2026-06-11, agentGG):** the high-z branch fork is RADIUS+MASS-blocked, not error-blocked:
any deep ALMA [CII] rotation curve of a REBELS-class z ≳ 4 disc reaching ~3–4 R_e (past r_MOND ≈ 6–10 kpc)
splits declining/constant/rising by ×2.3–2.4 in asymptotic velocity at fixed M_bar (declining 86–143 /
constant 106–175 / rising 204–335 km/s for REBELS-25, canon footing) — decisive IF M_bar is independently
pinned to ×2 (JWST IMF/SED + non-dynamical gas tracer; current bracket ×7). Triggers: any REBELS/CRISTAL
extended-[CII] follow-up; any independent α_[CII] or dust-based gas mass for REBELS-25; DLA0817g1 outer-disc
kinematics. C3 fence applies. Owner: `reviews/public_data/agentGG_jwst_highz.md`.
