# Collision-to-cooling test packet

Start with [RESULT.md](RESULT.md). The field runs establish finite in-phase concentration and signed outward energy/charge transport. The nonlinear remnant does not yet pass the weak stationary-mode interpretation. No four-dwarf or full-theory closure is claimed.

The action is an explicit alternative Psi/X/chi matter model. Do not merge its normalization or carrier content into the canonical polarization framework without deriving that bridge.

## Evidence map

| Evidence | Entry point |
|---|---|
| Eight actual pair/isolated evolutions and conservation controls | `pair_*_run_001/manifest.json`, `isolated_*_run_001/manifest.json` |
| Original and positive-face-energy preflights | `preflight_run_001/`, `preflight_v2_run_001/` |
| Canonical mode-coordinate derivation and synthetic controls | `PROJECTION_DERIVATION.md`, `projection_synthetic_run_001/` |
| Depleted-Q discrete references; preserved failed attempts | `MATCHED_REFERENCE_RESULT.md`, `matched_refs_run_001` through `004` |
| Conditional actual-pair mode extraction and new reference outgoing solves | `analysis_run_001/`, `REVIEW_PAIR_ANALYSIS.md` |
| Consistent carrier phase and core-only mismatch | `FIXED_CARRIER_RESULT.md`, `fixed_carrier_run_001/` |
| Independently verified actual FV energy/charge currents | `FACE_FLUX.md`, `face_flux_run_001/` |
| Initial-state loading: failed unsupported interface, exact replay | `seed_loader_red_run_001/`, `seed_loader_green_run_001/` |
| Undressed linear-coordinate seeds and their failed energy interpretation | `clean_mode_initial_run_001/` |
| Explicit quasistatic-chi initial preparation, not cooling dynamics | `chi_dressed_initial_run_001/` |
| Conservative prepared-state comparisons | `dressed_K0_run_001/`, `dressed_K1_run_001/`, `dressed_K50_run_001/`, `dressed_K500_run_001/` |
| Prepared-state coordinate fits and resolved limitations | `DRESSED_ANALYSIS_RESULT.md`, `dressed_analysis_run_001/` |
| Prepared-state signed currents and early quadrature obstruction | `DRESSED_FACE_FLUX_RESULT.md`, `face_flux_dressed_run_001/` |
| Explicit restricted binding mechanism and its limits | `EFFECTIVE_BINDING_MECHANISM.md`, `effective_binding_run_001/` |
| Four-dwarf stock, aperture and heating gates | `FOUR_DWARF_GATES.md` |
| Exact new Claude result reconciliations | `CLAUDE_ARRIVAL.md`, `CLAUDE_937_ARRIVAL.md`, `CLAUDE_940_ARRIVAL.md` |
| Independent reviews | `REVIEW_PROJECTION_AND_SOLVER.md`, `REVIEW_PAIR_ANALYSIS.md`, `REVIEW_SEED_EVOLUTION.md` |
| Handoff and next decisive test | `HANDOFF_TO_CLAUDE.md`, `NEXT_TEST.md` |

Every bounded run has a frozen contract and v2 manifest with exact source/data hashes, argv, software declarations, resource caps, status and declared result hashes. A valid manifest can document a failed run; read `run.status` and the scientific scope before interpreting it. Passing execution checks do not count as mode acceptance or a galaxy fit. Source receipts accompany the focused reviews.

## Reproduction

For an existing run, inspect its manifest's exact command, execution artifacts, input hashes, scope and caps. Validate without rerunning:

    python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py RUN/manifest.json --root /Users/carlzimmerman/new_physics/zimmerman-formula

Use a new output directory for a new execution; do not overwrite or relabel any existing run. The runner rejects existing output directories. Existing case launchers freeze a named case/contract and target run001, so they are intentionally guarded against accidental repeats. Exact field binaries and compilation receipts are retained alongside C sources; full ten-array snapshots retain fields and velocities, not just plots or fit coefficients.

All experiments here are finite, deterministic and below1GB measured process RSS. Threads, runtime, CPU time and log sizes are capped. No hard address-space cap is claimed on macOS. Snapshots are stored on disk; that storage is separate from the process-memory bound. The shared heavy job was not duplicated. No frozen publication, physical criterion, or prior source file was edited.
