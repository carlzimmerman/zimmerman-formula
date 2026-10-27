# Source and revision reconciliation

The raw delegated proofs were copied byte-for-byte from their temporary paths:

| Temporary raw artifact | Durable copy |
| --- | --- |
| `/private/tmp/boundary_pairing_20261019.md` | `BOUNDARY_PAIRING.md` |
| `/private/tmp/threshold_bootstrap_20261019.md` | `THRESHOLD_MODES.md` |
| `/private/tmp/cold_inverse_20261019.md` | `REGULAR_INVERSE.md` |
| `/private/tmp/cold_force_trace_route_20261019.md` | `GENERIC_FORCE_CANCELLATION.md` |
| `/private/tmp/conditional_cold_work_20261019.md` | `CONDITIONAL_WORK.md` |

The audit files retain their own exact raw proof hashes. Author statements
about pending independent audit inside the raw proofs are historical; the
separate reports and CHECKPOINT.json record the later review results without
rewriting that evidence.

During independent review, `REDUCED_INVERSE.md` was corrected to impose its
force condition at `|nu_0|=kappa`, explicitly including harmonics `+1,-1`.
The reviewer rechecked the corrected proof. Its final hash is
`ebc588cbd3fef36295dc355542f5b5344327c6ed1d76af12e777ee36786e93d1`.
The original formulation passed for positive frequencies and needed this
restriction/correction for negative ones. `REDUCED_INVERSE_AUDIT.md` records
the issue and the final scope.

The raw generic-force proof's source list pins the immediately preceding
reduced-inverse version `b7250d27338131815ad2ddf87187152efb35eb332606c7f037a591420970770e`.
Its scalar transversality and genericity argument does not depend on that
reduced-inverse conclusion; only its consequences section mentions it.
The combined theorem uses the corrected, separately reviewed final version.
The raw pin is preserved as provenance rather than silently refreshed.

The concrete cold-family bootstrap has quantitative source bounds from its
cap and endpoint proofs. The abstract bounded-source item in the raw bootstrap
alone supplies qualitative regularity; the uniform norm estimate additionally
needs quantitative control. `GEOMETRY_MODES_AUDIT.md` records this distinction.
The combined theorem uses the concrete family and its quantitative bounds.

No prior proof, manuscript, ledger, sealed criterion, scientific job or other
researcher's file was edited. The shared Git HEAD changed independently while
this checkpoint was written; source content hashes, the starting revision in
TARGET.md, and the assessment revision in CHECKPOINT.json carry the provenance.
