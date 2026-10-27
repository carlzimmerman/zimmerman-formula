# Thermal normalization: a new backreaction obstruction

The original theory is **open**. Kappa=1/2 is fitted under CFG908/CFG911.
This packet resolves a narrower uncertainty: in the macroscopic continuum/
mean-field regime, the latest exact rational compression construction cannot
acquire the required normalization by increasing inventory while preserving
its negligible-self-gravity tracer assumptions.

At the existing conditioned finite-core window x=10, with the physical
core volume and source length L=R, unit `4 pi G chi/V` requires
`Md/Mb=4.49053248`. Its central smooth/mean scalar/baryon density ratio is
`106.84037`; treating that mean density as a macroscopic gravitating source,
the omitted scalar gravity dominates there. Even with L
equal to the reference rms radius the ratio is `16.00874`. A separate
self-energy bound agrees. These follow exactly from the actual conditioned
Gamma moments plus the stated continuum-gravity hypothesis; the displayed
decimals are numerical evaluations. An independent review identified the
need for that scope restriction. For discrete independent particles,
expected pair energy and tagged-particle mean gravity carry `(1-1/N)`;
N=1 has no self-pair and is not excluded. The continuum stationary controls
below do not address that single-particle case. This is a restricted
obstruction, not an all-phase or unrestricted-finite-N no-go.

New self-consistent contact/gravity stationary controls retain that
inventory but give normalized susceptibilities `1.108e-5`, `.003558`,
`.13683` at the three declared contact parameters. Their nonlinear
compression also changes substantially. They are conditional thermal-EOS
controls, not certified physical/stable states or a selected abundance.

- Proof, hypotheses and continuation: `DERIVATION.md`.
- Code and executable contract: `check_backreaction.py`, `contract_v3.json`.
- Current evidence: `run_004/manifest.json`, status **completed**, 41/41
  numerical controls. Manifest validation with project root passes.
- Exact base/input/output hashes: `PROVENANCE.json` and the manifest.
  Requested base f659e6d8e1ee4cf2b756f091aff56b018da1fb1e; observed concurrent
  run HEAD a229bb78c078e809016a4c76c5b68f458423c664 descends from it.
- ~12.7 s, one serial stdlib process, ~11.7 MB maximum RSS, 45 CPU-second
  and 60 wall-second limits. Host cannot enforce the requested AS/affinity
  limits; no worker or numerical-library thread was used. All requested
  work stayed far below 1 GB. Earlier launch/mesh failures remain preserved.

Recompute the finite checks from repository root with a fresh output file:

```
python3 reviews/final_closure_push_2026_10_20/normalization_origin/check_backreaction.py /private/tmp/thermal_normalization_recheck.json
```

The exact recorded bounded command is in `run_004/manifest.json`; its output
directory must not be reused. Validate the current record with:

```
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py reviews/final_closure_push_2026_10_20/normalization_origin/run_004/manifest.json --root /Users/carlzimmerman/new_physics/zimmerman-formula
```

Next: select a physically supported live host/EOS, derive its complete
gravitational source and interacting response, and test a formation rule
for inventory and susceptibility together. The curvature-to-acceleration
operator bridge, thermal receiver, microscopic abundance and dark-energy
normalization are still missing. This packet edits only its assigned
review directory; no shared status, old output, action, frozen campaign
criterion, manuscript, publication or external message was changed.
