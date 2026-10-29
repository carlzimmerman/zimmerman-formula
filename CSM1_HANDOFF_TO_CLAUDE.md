# Claude handoff: corrected core/switch results

Start with `rebuild_2026_10_22/CSM1_consistent_core_switch/README.md`, then
`MODEL.md`, `REVIEW.md`, `HANDOFF.json` and
`reconciliation_001/results.json` in that directory. This checkpoint supersedes
earlier claims of a joint calibration pass that used different concentration
coefficients for the switch and the actual core.

The correction adds no fitted parameter: each parent selector compares the
same mass-dependent unfloored column used by its local core with its own
floor. No independent T is adjusted. Own and basin masses retain the recorded
pipeline-specific meanings, and dwarfs retain their separate cooling profile.

Results on the unchanged cuts:

- L=3.75, 3.9 and 4.0: SPARC, 63 groups and all cluster keys pass on both
  footings. Lensing fails. Canonical delta-chi2 versus law is +415.281,
  +420.306 and +423.234, against an allowed +9.
- The predeclared existing-L refit is L=2.5090648745652686, defined by actual
  canonical/background-A X43 equality at logM=12.3. Lensing passes, but
  canonical groups fail at Z=+2.621919809. No joint pass was found.
- The alternate-footing fixed MW ultra-faint construction has exactly two
  possible L-independent profile states, both failing. Changing L alone
  cannot rescue that class. This is conditional on that fixed construction.
- Four tested levels do not exclude every canonical L. Do not infer likelihood
  or group-Z monotonicity from monotonic activation columns.

Old baselines reproduce; actual-flag mutation controls fail as intended.
The coordinator passes 141/141 reconciliation checks. Independent reviews
check numerical columns, actual branch decisions, raw class summaries and
primitive MW line cuts. Commands, hashes, manifests and retained unsuccessful
development runs are included. Scientific failure must not be confused with
implementation-control failure. The 2.12-ppm displayed-a0 challenge error was
corrected by rerunning the same frozen target; both records are retained.

The preceding audit and observational recovery are in
`rebuild_2026_10_22/INDEPENDENT_PUSH_2026-10-28/`. Its current-theory statements
are dated history; use CSM1 for the corrected-model empirical verdict.

Native progress update: seeds 3, 7 and 8 of nine have completed. Their verified
final snapshots, completion markers, final logs and hash inventory are in
`rebuild_2026_10_22/NATIVE_PARTIAL_2026-10-28/`. This is a partial ensemble,
not a new ensemble L estimate or NL1 grade; the other six remain pending. Use its
`completed_results.json` for the exact observation timestamp and seed set.

Preliminary measurements of seeds 3, 7 and 8 are in that package's
`measurement_002_three/results.json`: unchanged primary
c_f=3.138159/2.441598/4.010123 and NL1-normalized per-seed
L proxies=1.972446/1.534632/2.520507 (seeds 3/7/8). All have estimator flag
`ok`. Five implementation controls pass, including exact reproduction of the
previous seed-3/7 results. The initial two-seed evidence remains unchanged in
`measurement_001/`. Seed 8 is higher than the first two, but all three proxies
are below L near 4. Its c_f near 4 is not L near 4 under NL1's normalization.
These do not estimate the full ensemble or establish convergence. Completion
order is not a representative sample, and the NL1 mass/resolution-transfer
normalization remains conditional. No full NL1 grade has been produced here.

New robustness audit: `rebuild_2026_10_22/CSM2_single_L_search/README.md`.
Changing radial edges from 25 to 29 exposes an earlier -2 crossing: c_f moves
from 3.138 to 16.804 (seed 3), and 2.442 to 11.798 (seed 7). Seed 8 stays near
4.01--4.04. All tested binnings pass the synthetic control. Independent profile
reconstruction confirms multiple crossings and the first-crossing selection
mechanism. Original primary results remain unchanged, but their `ok` flags
alone do not establish a robust L. No alternative crossing was selected to
match a desired value. CSM2's bounded necessary group/lens grid is now complete:
none of15 predeclared levels survives. Groups fail through the sampled L=3.5;
six tested values3.625--5.0 pass groups but fail lensing by delta-chi2+411--437.
The finite result is not an all-L theorem. A validated linear-projection
preflight and `INTERVAL_ROUTE.md` record the next route to interval bounds.

The native ng64/NL1 aggregate work is still pending at this observation.
`rebuild_2026_10_22/NL1_native_level_L/` contains its scorer. Verify actual
complete outputs, seed coverage and uncertainty when they arrive. Its old
fixed-T primary grade alone cannot establish a corrected linked-T pass;
L near 4 alone would not restore CSM1 lensing. Preserve running jobs/follower.

Kappa=1/2 remains fitted, basin selection remains a posit, and there is no
new condensation field equation or covariant completion. No new temperatures,
inclination correction or hot-gas repair was folded into CSM1.

The user has authorized pushing completed results as they arrive so Claude
can retrieve them. Publish verified result packages and a clear handoff;
keep unrelated dirty work and incomplete simulation dumps out of such commits.


Native matrix checkpoint: `native_matrix_001/` completes the next structural
preflight (32/32 controls). Actual native radii, full covariance, four two-halo
templates and catalogue interpolation weights reproduce saved CSM1 at
L=3.75,3.9,4.0 on both footings. All181431 lenses reduce to127 positive-weight
nodes. The native projection identity passes24 cases (max error5.15e-15).
Free-amplitude projection matches independent least squares; a separate normal-
equation review agrees to1.26e-12. At alternate L=3.75 the unrestricted first
amplitude is negative: its lower score547.638 differs from the constrained
547.679, confirming why the interval route needs an inequality. A1% covariance
corruption breaks score reproduction. No new model pass or continuous-L
exclusion is claimed. `INTERVAL_001_CRITERIA.md` now freezes the first local
interval [3.75,3.751]; implementation and enclosure validation are next.
