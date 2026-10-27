# A finite geometric upper bound for the saved host endpoint

This read-only postprocessing checks `run_base_host/final.npz`. It changes no
simulation state, imported evolution code, centring routine, or physical input.
The assertion concerns the **stored coordinate set**, at this one endpoint.

## Reduction covering all centres

Let a radius-R sphere contain a nonempty set A of cold particles, and pick any
member p. Every member of A is at distance at most2R from p, so A is a subset of
the particle-centred2R neighbourhood S_p. Every pair of members of A is also at
distance at most2R from one another. Now take any disjoint matching of pairs in
S_p whose separations exceed2R. At least one endpoint from each such pair must
be absent from A. Disjointness prevents counting an omitted endpoint twice.
Consequently

    |A| <= |S_p| - number_of_disjoint_far_pairs.

The maximum of these upper bounds over **every** cold particle p bounds every
nonempty radius-R aperture, regardless of its centre. Empty apertures satisfy
the bound immediately. A matching need not be maximum, and no density or
potential-centre search is required. During computation, a matching may be
skipped only when the neighbourhood cardinality itself is no larger than the
current certified upper bound; this preserves complete coverage.

## Arithmetic, tolerance and independent checks

The executed code uses R=300pc and an inflated comparison length
`float(600.0 + 1e-8)`pc. It converts that represented number and every stored
binary64 coordinate to a common exact power-of-two integer grid. All squared
distance comparisons and matching certificates then use Python integers.
Using the inflated length both to include neighbours and to classify far pairs
weakens the bound conservatively. It cannot exclude a pair whose saved-coordinate
separation is at most600pc. This avoids cKDTree, optimization and floating norm
roundoff in the load-bearing geometric comparisons.

The result includes one coverage certificate per cold particle and records
all unordered pair checks. An orthogonal `fractions.Fraction` implementation
checks every distinct matching witness and a deterministic set of grid-distance
comparisons. Three handcrafted checks cover a cluster with no far pair, two
distant triples plus a bridge (bound4, independently checked by exhaustive
subsets), and a just-beyond600pc pair intentionally retained by the tolerance.

Input parsing retains the saved finite binary64 values exactly. The output
mass conversion remains floating point; the primary assertion is the integer
particle-count bound. This does not bound unrecorded continuum-coordinate error,
time integration error, or the physical evolution. Exact geometric bookkeeping
does not make the underlying finite-particle simulation a continuum solution.

## Reproduction and provenance

Run from the repository root. The output directory must be new.

The first runner attempt, preserved at `geometric_run_001/manifest.json`, failed
before launching because macOS rejected `RLIMIT_AS`. Its logs contain no
scientific result. The retry below enforces wall time, CPU time and numerical
library thread limits. It reports observed peak RSS instead of claiming an
unsupported hard address-space limit. The script caps input size at4096 and
stores neighbourhoods and per-aperture matching matrices, not a simulation.

```bash
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/run_experiment.py \
  --root /Users/carlzimmerman/new_physics/zimmerman-formula \
  --contract sol61_push/isolated_host_dwarf_2026_10_19/geometric_contract.json \
  --input sol61_push/isolated_host_dwarf_2026_10_19/geometric_bound.py \
  --input sol61_push/isolated_host_dwarf_2026_10_19/GEOMETRIC_BOUND.md \
  --input sol61_push/isolated_host_dwarf_2026_10_19/run_base_host/final.npz \
  --output sol61_push/isolated_host_dwarf_2026_10_19/geometric_run_001/retry_cpu_bounded \
  --result sol61_push/isolated_host_dwarf_2026_10_19/geometric_run_001/retry_cpu_bounded/result.json \
  --timeout 30 --max-output-bytes 1048576 \
  --max-cpu-seconds 25 --max-threads 1 \
  -- python3 sol61_push/isolated_host_dwarf_2026_10_19/geometric_bound.py \
  --snapshot sol61_push/isolated_host_dwarf_2026_10_19/run_base_host/final.npz \
  --output sol61_push/isolated_host_dwarf_2026_10_19/geometric_run_001/retry_cpu_bounded/result.json

python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py \
  sol61_push/isolated_host_dwarf_2026_10_19/geometric_run_001/retry_cpu_bounded/manifest.json \
  --root /Users/carlzimmerman/new_physics/zimmerman-formula
```

The manifest pins the executed source, this local proof, and the snapshot before
and after execution, with the exact command, revision, versions, limits and
output hashes. Read `run.status` and the actual integer bound in `result.json`;
a completed command alone does not establish a physical claim. The output
reports whether the bound is below205particles, the count needed for at least
one tenth of the2048-particle original cold inventory. The2.44million-solar-mass
remnant found by the independent centring diagnostic is compatible with a
centre-independent bound that excludes that larger threshold.
