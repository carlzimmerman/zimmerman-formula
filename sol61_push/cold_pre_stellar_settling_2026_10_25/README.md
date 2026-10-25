# CCT020 — pre-stellar cold-field settling

**No demonstrated four-dwarf formation solution.** The later coarse Draco and Sextans collapses keep changing and hit the phase-resolution gate without qualifying for stellar insertion. A common higher-infall-energy experiment also produces excessive profile velocity support in Fornax and Leo I at the fixed common comparison time. These finite results do not rule out eventual relaxation after the resolved interval or every other assembly history.

Start with [RESULTS.md](RESULTS.md), then [MECHANISM.md](MECHANISM.md), [ENERGY_SCOPE_CORRECTION.md](ENERGY_SCOPE_CORRECTION.md), and [NEXT.md](NEXT.md). Exact numerical records are the per-run `result.json`, `field.npz`, `stars.npz` and `manifest.json`; the final analysis and audit are identified in RESULTS. A completed runner means execution was saved, not that the physical test passed.

This is the CCT spherical wave proxy with fixed supported baryonic gas before later passive stars. It is **not** a Khronon/AeST/v3 action result, SCT-M, or a collisionless-particle/clump result. Cold Newtonian gravity is counted once. No real spin transport occurs in spherical symmetry; no escape-to-infinity measurement or gas-to-stars dynamics is supplied. The assumed half-catchment mass supply is a hypothesis tied to earlier metadata, not a directly measured cold reservoir.

The original producer contract and all failed implications remain unchanged. Separate posthoc hypotheses and implementation changes are named in their own contracts. In particular, the frozen energy screen's overly broad time-average interpretation is corrected in a separate file; fluctuating binding is not silently discarded. See [REVIEW.md](REVIEW.md).

All runs here are explicit bounded invocations. No schedule or background monitor was created. At most two galaxy jobs ran concurrently, each with one numerical thread and a 480-second segment. Measured resource limits, true coverage, restarts and inactive stellar tests are reported, rather than inferred from requested horizons.

The two `preflight_*` runs and `audit_preflight_001` are setup/debug checks, excluded from canonical producer counts and final evidence claims. `PADE8_FAILED_CONTROL.log` preserves an actual failed stiff-order control. `prolong_001` preserves an execution failure caused by NumPy Boolean serialization; `prolong_002` fixes that serialization only and records a failed physical-transfer screen. None is relabeled a formation success.
