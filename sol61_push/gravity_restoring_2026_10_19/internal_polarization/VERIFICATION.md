# Verification and review record

The universal Newtonian separation and common-frequency Q-ball exclusion
are analytic arguments in `INTERNAL_POLARIZATION.md`. This bounded exact
run checks coefficient bookkeeping on the contract's finite domain.

Actual execution command, from the project root:

```bash
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/run_experiment.py --root /Users/carlzimmerman/new_physics/zimmerman-formula --contract sol61_push/gravity_restoring_2026_10_19/internal_polarization/contract.json --input sol61_push/gravity_restoring_2026_10_19/internal_polarization/check_internal.py --output sol61_push/gravity_restoring_2026_10_19/internal_polarization/run_001 --result sol61_push/gravity_restoring_2026_10_19/internal_polarization/run_001/results.json --timeout 20 --max-output-bytes 65536 --max-cpu-seconds 10 --max-threads 1 -- python3 sol61_push/gravity_restoring_2026_10_19/internal_polarization/check_internal.py --output sol61_push/gravity_restoring_2026_10_19/internal_polarization/run_001/results.json
```

The runner output directory must be fresh. To regenerate, replace both
occurrences of `run_001` with one fresh run identifier. Do not overwrite
the preserved result or use a manifest as executable instructions.

Validation command executed:

```bash
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py sol61_push/gravity_restoring_2026_10_19/internal_polarization/run_001/manifest.json --root /Users/carlzimmerman/new_physics/zimmerman-formula
```

Result: valid evidence record, `run.status=completed`, child exit 0.
Python 3.9.6, exact Fraction arithmetic, no random seed or floating-point
tolerance. Counts: 3456 reference-center cases with five exact assertions
per case; 384 positive-square cases; 144 nonuniversal-ratio cases; 12 target
residual cases. Every original source hash in `source_pins.json` was
rechecked unchanged after the run and final note edit.

Implementation review: the Cartesian-product loops cover the declared
finite grids without filters, early exit or random sampling. The reference
center is checked by inversion of the coupled mass matrix and independently
by subtracting the two constituent accelerations. Its determinant is also
checked. The positive-square test uses rational complex-pair arithmetic
rather than floats. The finite assertions agree with the raw analytic
identities; they do not prove existence or absence of unspecified phases.

Proof self-review: reconstructed (3) by direct COM substitution, (6)-(7)
by the determinant/Schur complement, (9a)-(9b) by a canonical Legendre
transform, (14) by admissible profile scaling, and (15)-(19) by multipole
expansion. The exact assumptions and exclusions in the claim card remain
necessary. This is self-review with shared project context, not an externally
independent audit. Independent cross-review is pending the coordinator.

Proofreading self-review: the complete new note was reviewed for display
integration, definitions, equation numbering and cited version consistency.
Routine corrections: none. Mathematical-token corrections made as
proofreading: none. The new canonical lapse derivation (9a)-(9b) was an
explicit research addition after the initial draft, not a silent repair.
No mathematical LaTeX compilation was requested or needed for Markdown.

Authoritative local source bytes reviewed (paths relative to project root):

| Source | Bytes | SHA-256 |
|---|---:|---|
| `sol61_push/cold_production_2026_10_11/MASTER_COLD_ENERGY_EQUATIONS.md` | 41494 | `c81b4a3136d433a2b7a0bf06ec87f61389b8e5a73da6c7603a6b264dda0bbe43` |
| `sol61_push/particle_derivation_2026_10_18/density_duality/DENSITY_DUALITY.md` | 20561 | `bb45b6bddef696c689f9e60ca3f4bb608a8ce8914cab694e6027383d675f2fff` |
| `sol61_push/particle_derivation_2026_10_18/micro_exchange/MICRO_EXCHANGE.md` | 17864 | `8d122d78573b686b098f0c8d7847723d8063e80c8b9462adf7b1f50d072efb73` |
| `sol61_push/particle_derivation_2026_10_18/micro_response/DERIVATION.md` | 24173 | `2ba9a12c97fc2c3d237bbb963b22486ff0ad066fafd3404b6d35063d290423c8` |
| `sol61_push/particle_derivation_2026_10_18/density_duality/COHERENT_CURRENT_REVIEW.md` | 5900 | `54c84286eb7b55894f51305e1fe50325f5263a09436dda7e401da464302e5247` |

External primary-source checks are recorded in the note; those PDF/text bytes were not retained, and no external retained-source hash is asserted.
