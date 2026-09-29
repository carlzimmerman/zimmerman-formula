# The REPORTED-ONLY sweep: clean re-runs of the lanes behind the adopted STANDING's never-re-run lines (2026-09-29)

- **Why.** Six lines in the adopted `STANDING_2026-09-29.md` body carried [REPORTED-ONLY] because no verification pass had re-run their lanes. LEDGER_VERIFICATION Parts 1–7 cover CFG43–50, CFG58–59, CFG61–106 and CFG110–115, but not CFG1, CFG4_clusters, CFG4_switch, CFG8, CFG16, CFG23, CFG25, CFG27 or CFG31. This sweep is separate from those parts, and its file lives here.
- **Method:** `verify_reported_only_2026-09-29.py`, log `.out`.
  - A clean `git archive` export of HEAD (23dc871c4). The git-ignored data under real_research/data were symlinked in: data only, never code.
  - Each lane ran in its main mode and with MUTATE=1. Each lane's outputs were deleted before its run, so a crash cannot leave the archived file in place. GIT_DIR pointed at the repository, read-only, because CFG1 reads commit messages.
  - Compared with the committed files: the exit code, the "N/M checks pass" tally and the full .out text, with timing stripped.

## Result: 20 runs, no tracebacks, every tally and exit code as committed

| lane | main: tally, rc | MUTATE: tally, rc | .out vs committed |
|---|---|---|---|
| CFG1_evidence_audit | 9/9, 0 | 8/9, 1 | 4 lines differ in both modes; all are live repository status (below) |
| CFG4_clusters | 7/7, 0 | 6/7, 1 | identical |
| CFG4_switch | 13/13, 0 | 12/13, 1 | identical |
| CFG8_chae_kernel | 6/8, 1 | 6/8, 1 | identical |
| CFG16_selfconsistent_floor | 3/4, 1 | 3/4, 1 | identical |
| CFG23_diagnostics | 4/4, 0 | 3/4, 1 | identical |
| CFG23_lcdm_control | 4/9, 1 | 6/9, 1 | identical |
| CFG25_fg016_lcdm_control | 3/5, 1 | 3/5, 1 | identical |
| CFG27_edge_thread_closure | 3/3, 0 | 1/3, 1 | identical |
| CFG31_coma_udgs_under_b | 11/11, 0 | 8/11, 1 | identical |

- **Main runs that exit 1:** CFG8, CFG16, CFG23_lcdm_control and CFG25. They do so because of checks their committed outputs show failing as they fell. These are not re-run discrepancies.
- **CFG1's four differing lines** are its live status report: FP24, XR34, XR35 and XR24 read "in flight" in the committed output and "committed" now. They reflect the repository's state when CFG1 last ran, not a result.
- **CFG1 cannot run from a plain git-archive export.** It reads commit messages with `git log` (for example fa341733d), and without repository access its regex sees empty text and raises. That is a portability limit, not a defect in its numbers.

## Spot-checks of the numbers STANDING quotes (all found in the outputs)

- **Coma UDGs 1.33 / 1.11σ (CFG31):** canonical +0.234 dex, alt +0.195, each ± 0.176.
- **X-COP identity 0.946 ± 0.080, and the Bullet's 4.6× / 4.9× the aperture baryons (CFG4_clusters).**
- **The KiDS–LG tension (CFG23):** T = 24.5 (x_t = 1 only) to 72.5 (c × 0.7) for standard halos, against the framework's 26.2 (P2) and 27.8 (ν_mono).
- **The cold budget against KiDS (CFG27):** cost/S = 0.59 (canonical, P2) to 0.98 (alt, ν_mono).
- **Chae's external-field signal (CFG8):** +1.7σ (P2, canonical) to +3.0σ (ν_mono, alt).

## Tags these runs upgrade in STANDING_2026-09-29 (appended there as a verification update)

- §1 "The law's other checks" (CFG4_galaxy_law, already re-run clean, and CFG1) and §1 "carried from GATES.md" (CFG31, CFG4_clusters, CFG4_switch, CFG16): now RE-RUN-CLEAN.
- §3 "Local Group R₀ and the KiDS + LG edge" (CFG23, CFG25), "Cold budget against KiDS" (CFG27) and "Chae's external-field signal" (CFG8): now RE-RUN-CLEAN.
- **Not covered:**
  - the κ like-for-like note (97f30b36c), a commit rather than a lane;
  - CFG99's C1c line (git-ignored cubes);
  - the lanes appended after adoption. Those have their own independent re-derivations: CFG100, CFG104–108 and LEDGER_VERIFICATION Part 7.

A re-run checks that the committed scripts reproduce their committed outputs. It does not check the models or their hypotheses. κ = ½ stays fitted. Nothing here says the theory is closed.
