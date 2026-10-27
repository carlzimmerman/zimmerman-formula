# Rational completion: verification and handoff

Mathematical parent: CE-PARTICLE-2026-10-18 / CE-FM-085. Initial requested
HEAD: `9516ee01c79f35c04b7556050669ba77b0c98b99`; actual interpretation
sources and concurrent observed HEAD are in `source_pins.json`.

## Claim cards and verdicts

**Conditional exact construction.** For the explicitly added independent
zero-temperature two-state dipole model and its nonnegative continuum
weight, the response and material Legendre energy equal the target when
the independent calibration `p_sat=a/K` is imposed. The locally integrable
finite-total-weight density is unique for that particular two-state kernel.
The random-axis inverse spectrum is positive and gives the same radial
law. **Author self-audit verdict: proved as written within those hypotheses.**
This is a static thermodynamic/disorder-averaged model, not a finite-Q
microscopic cell. The independent narrow review confirmed the integral,
Legendre pair and isotropic construction, and required a cutoff-window
restriction that has been incorporated.

**Original particle derivation.** The required physical local gravitational
dipole source, its saturating internal dynamics, its occupied reduced-gap
distribution, and the normalization against G have not been derived from
the original canonical Phi/X action. **Verdict: incomplete, with those named
missing implications.** No improvement of the original theory's closure
status is claimed from the conditional construction.

## Dependency and obligation audit

| Obligation | Evidence and status |
|---|---|
| Source and energy sign | H=H0−E D, F=e(0)−e(E), p=F_E; passed by direct diagonalization |
| Constant-lapse/fixed-Q source | Complete Hamiltonian redshift and m Phi Q identity; passed within the stated regulated NR/lapse scope |
| Finite-Q conversion response | Exact Q=2 matrix plus four complete finite sectors; passed within finite-mode scope |
| Finite-state endpoint obstruction | Variational upper/lower bounds; no zero-field-gap assumption |
| Continuum integral | Elementary primitive, E=a removable case, independent quadrature; passed |
| Inverse uniqueness | Abel inversion and beta-integral order reversal, a.e. density class; passed analytically |
| Isotropic law | Nonnegative double-integral change of variables and positive inverse density; passed |
| Finite cutoffs | Exact primitive, susceptibility, saturation and moment; passed |
| Cusp feature accuracy | Requires max(ell,a³/L²)<<E<<a without recalibration; independent finding incorporated |
| Strong endpoint vs full inventory | Requires a<<E<<L and ell²E/a³<<1; author self-review |
| Thermal occupancy interpretation | Direct partition functions and gamma density integral; author self-review only |
| Polynomial finite-tree obstruction | Finite algebraic branches versus logarithmic monodromy; author self-review only |
| Original dipole/source and G normalization | Open; added model assumptions must not be transferred |
| Dynamical local action | Not established; soft-gap distribution prevents uniform zero-field adiabatic elimination |

The actual phonon comparison preserves the linear IR weight of the nonlocal
longitudinal displacement; it does not use raw DOS counting as a no-go.
The Bogoliubov Jacobian was reconstructed from the stated dispersion and
matrix element and checked against the sibling collective note. A physical
local source/occupation map remains absent.

## Computation record

`run_003/manifest.json`: runner-v2, status **completed**, 88 passing
exact/finite controls. Current input and output hashes validated with:

```text
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py sol61_push/gravity_restoring_2026_10_19/rational_completion/run_003/manifest.json --root /Users/carlzimmerman/new_physics/zimmerman-formula
```

The exact command, actual versions, CPU/wall/log/thread limits, source hashes,
and output hashes are in that manifest. The standalone program accepts the
results path as its only positional argument. It was run only through the
bounded runner. The declared inputs cover the script, parent source pins,
and five interpretation sources. No random sampling was used.

Coverage: exact symbolic identities; eight direct 50-decimal continuum
quadratures; three isotropic quadratures using a separately integrated
angular kernel; fifteen finite-cutoff quadratures/bounds; complete two-mode
sectors Q=2,4,8,16 (dimensions 2,3,5,9); five Q=2 differential-source points.
The actual total is 88 individual assertions. Full universal mathematical
claims are supported by the explicit proofs, not by those finite points.

Run 001 remains a launch-failure record (preexec exception, detailed OS cause
not available). Run 002 remains a failed implementation check: a symbolic
positive-angle assumption did not restrict theta below pi/2; the final
positive tangent-coordinate identity fixes the chart. Run 003 succeeds
without the memory cap requested in run 001. These records distinguish
environment/implementation failures from mathematical counterexamples.

## Review provenance

The independent in-session analytic review lives in the sibling
`internal_polarization/RATIONAL_REVIEW.md`. It identifies its exact input
hash and scope; it predates final source edits. It covers Sections 1, 3–5
and Section 2's source restrictions, but not Sections 6–8 or numerical code.
Its reported UV-slope issue has a concrete correction in the final note.
The later per-site zero-energy identity shift avoids an infinite sum of
negative zero-field energies; it changes no response. The later explicit
thermodynamic and finite-frequency qualifications narrow the physical claim.
Those edits were self-reviewed rather than silently attributed to the old
independent pin. Cross-lane bytes used for reconciliation are separately
pinned without modifying the earlier runner inputs.

Math proofreading self-review covered the whole new note: consistent E,
p, u and K variables; pmax versus isotropic inventory factor 2; source
signs; W/F differentiation; E=a removable point; IR/UV cutoff conditions;
and the distinction between raw energy gaps and reduced gaps. No unrelated
manuscript or pre-existing source was edited. No external theorem or
novelty claim is used as a load-bearing unverified leaf.

## Continuation contract

The route remains open at the original physical dictionary. Next decisive
check: identify a local operator built from the actual particles whose
gravity source is a uniform acceleration, not merely a total COM force or
a tidal curvature source. Only after that map exists does it become useful
to compare its occupied dipole-weighted reduced-gap spectrum with the exact
positive density and cutoff tests. A new supported double-well model is an
explicit alternate model; it does not close that missing implication.

All output is confined to the assigned rational-completion directory. No
queue, current contract, manuscript, publication file or Git state was
mutated by this lane. `artifact_hashes.json` provides the final artifact
inventory; the initial HEAD pin is ancestry context, while actual input
hashes authenticate the computation amid concurrent repository changes.
