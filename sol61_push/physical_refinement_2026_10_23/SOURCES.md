# Sources and regeneration

This phase derives and computes consequences of the local model. No new external theorem, observational number or literature claim is relied on.

- `../expanding_polarization_2026_10_23/DERIVATION.md`: inherited preferred-frame action, coefficients, work identity, and cosmological limitations.
- `../expanding_polarization_2026_10_23/RESULT.md`: inherited large-scale growth comparison, not rerun here.
- `../spatial_expansion_2026_10_23/RESULT.md`: previous 3D resolution limitation and unresolved initial histories.
- `CONTRACT.md`, `radial_v2.py`, `history.py`: this phase's conventions and evolved model.
- Per-run manifests: exact argv, hashed inputs/results, versions, observed repository revision, resource limits and execution status.
- `analysis/result.json`: deposited aperture and limited Newtonian energy diagnostics. `analysis/manifest.json` pins its input dependency list.
- `plot.py`: generates profiles.png from already pinned evolution outputs; illustrative postprocessing, not independent evidence. Run `python3 sol61_push/physical_refinement_2026_10_23/plot.py` from the repository root.

Bounded runner and manifest validator came from the installed mathbox computation-audit skill at `/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/`. Regenerate into new output directories; never overwrite historical run outputs. Validator results are saved in VALIDATION.txt. CHECKPOINT.sha256 pins the final local artifact set excluding itself and Python caches.
