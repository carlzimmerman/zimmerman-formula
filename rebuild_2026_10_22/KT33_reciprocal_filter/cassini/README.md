# KT33 Cassini: fixed reciprocal Gaussian, no refit

The corrected fixed-width map fails the inherited Cassini ceiling on both
frozen KT25 footings. At epsilon = 0.5 its absolute quadrupole is **1.09159063
ceiling on canonical** and **1.61965966 ceiling on alt**. This is a finite
Solar external-field diagnostic, conditional on numerical convergence and the
inherited physical conventions. It is not a full ephemeris calculation or a
universal width prescription. No dwarf or SPARC calculation was run.

The archived source-only integral is reproduced separately. An additional
analytic finding matters for interpreting that comparison: after smoothing
the solar source, the integration by parts used in KT16/KT25 has a nonzero
origin surface term. The archived integral omits it. The physical source-only
Hessian and the archived flux integral must therefore not be identified.
The reciprocal result is unaffected by this issue because its smoothed Green
kernel removes the inner surface term.

## Frozen inputs and conventions

- Map: `Phi[rho] = N rho + S Phi_ph[S rho]`; only the phantom potential receives
  the outer filter. `S` is a normalized isotropic Gaussian with standard
  deviation `xi`, held fixed when varying the source.
- Point Sun: `GM = 6.6743e-11 * 1.98892e30` in SI units. The physical Newtonian
  point-source term remains unsmoothed.
- `r_M = sqrt(GM/a0)` and `xi/r_M = epsilon = 0.5` on each footing. Canonical
  `a0 = 9.3603e-11 m/s²`; alt `a0 = 1.1312e-10 m/s²`.
- Uniform external Newtonian gradient along z: `gext = 2.32e-10 m/s²`, with
  `eta = gext/a0`. The external linear potential survives convolution unchanged.
- Simple `nu(h) = 1/2 + sqrt(1/4 + 1/h)`. The phantom source is
  `D = div[(nu-1) u]` in dimensionless coordinates, `u = g(r) rhat + eta zhat`.
- The signed `q_hessian_signed` is the trace-free zz Hessian of the phantom
  potential, in units `a0/r_M`. Preserve the KT16 normalization
  `Q2_signed = (3/2) (a0/r_M) q_hessian_signed`. The observed criterion uses
  `abs(Q2) <= 5.2e-27 s^-2`; the sign is not discarded in the JSON.
- The Gaussian width is sigma, not FWHM or a heat-kernel width with a different
  factor of two. Its density is `(2*pi*xi²)^(-3/2) exp(-r²/(2*xi²))`.

The old source-only scalar integral used the same final factor `3/2`, but its
signed output is named `q_flux_signed` here, since it omits a boundary term for
a smooth source. No archived input/output or owner/seal file was changed.

## Outer-filter derivation

All radii and widths below are dimensionless in units of `r_M`. Put
`A = nu(|u|)-1`, `mu = rhat dot zhat`, and `P(mu) = 3 mu²-1`. A prime
on `nu` differentiates with respect to its dimensionless argument. For a source
Gaussian of width `s`,

```
g(r) = [erf(x/sqrt(2)) - sqrt(2/pi) x exp(-x²/2)] / r²,  x = r/s,
div(g rhat) = sqrt(2/pi) exp(-x²/2) / s³,
g'(r) = div(g rhat) - 2 g/r.
```

For zero source width, `g = 1/r²`. Its point-source delta does not create a
phantom quadrupole because `nu-1` tends to zero in the divergent central field.

Convolution commutes with the whole-space Poisson Green operator. Therefore
outer smoothing replaces the Newton kernel `1/r` by

```
f(r) = erf(r/(sqrt(2)*sigma_outer))/r.
T(r) = r³ [f''(r)-f'(r)/r] / 3
     = erf(x/sqrt(2)) - sqrt(2/pi) exp(-x²/2) (x + x³/3)
     = P_regularized_gamma(5/2, x²/2),   x = r/sigma_outer.
T'(r) = sqrt(2/pi) exp(-x²/2) x⁴ / (3 sigma_outer).
```

At zero outer width, `T=1` and `T'=0`. At positive width, `T=O(r^5)`
near the origin. The gamma representation avoids cancellation at small r.
The STF Hessian of `f` has zz component `[f''-f'/r](mu²-1/3)`.
With `Phi_ph = -(1/(4*pi)) integral D(y)/|x-y| d³y`, integration over azimuth
gives the independent density formula, with `v=log(r)`,

```
q_density = -1/2 integral dv T(r) integral dmu D(r,mu) P(mu).
```

The analytic divergence used in that route is

```
h = sqrt(g² + eta² + 2 eta g mu),
D = A (g' + 2g/r)
    + [nu'(h)/h] [g' (g+eta mu)² + eta² g (1-mu²)/r].
```

Integrating by parts on a finite spherical annulus gives a second calculation:

```
q_flux = (3/2) integral dv (T/r)
           integral dmu A [eta (3mu-5mu³) + g (1-3mu²)]
         + (1/2) integral dv T'
           integral dmu A (g+eta mu) P(mu),
B = (1/2) [ (T/r) integral dmu A (g+eta mu) P(mu) ]_(rmin)^(rmax),
q_hessian = q_flux - B = q_density.
```

Both the extra `T'` term and the surface term are retained. Multiplying the
historical integrand by a source enclosed-mass fraction would be wrong.
In fact the new `T'` contribution dominates here: canonical
`weighted_old_term = -0.00218616784925` and
`gaussian_derivative_term = -0.0459585614317`.
Radial reference terms whose angular polynomial integrals are exactly zero
are subtracted before quadrature to suppress numerical cancellation; this
changes neither the continuum equations nor the normalizations.

## Inherited source-only origin term

For a positive source width and positive `eta`, write
`c = sqrt(2/pi)/(3*sigma_source³)`. Near the origin, `g = c r + O(r³)` and

```
A u_r = (nu(eta)-1) eta mu
        + c r [(nu(eta)-1) + eta nu'(eta) mu²] + O(r²).
```

Thus for zero outer width the lower surface limit is

```
b_inner = (4/15) c eta nu'(eta)
        = -2c / [15 eta sqrt(1/4+1/eta)],
q_hessian = q_flux + b_inner       (infinite outer domain).
```

The lower term is `-0.14159222566552934` on canonical and
`-0.16106180007580947` on alt. It is **not zero**, however small the excluded
inner sphere. The upper term vanishes as the domain expands. The numerical
annulus surface and independent density route confirm this derivation.
For the reciprocal outer Gaussian, `T=O(r^5)` instead makes the lower surface
zero. For an unsmoothed point source, the old lower surface also vanishes.

This explains why the apparently passing old canonical source-only number
cannot be treated as a correctly computed source-only Hessian. The actual
physical source-only quadrupole is already above the inherited ceiling;
outer smoothing reduces that physical value but leaves both reciprocal
footings above the ceiling.

## Results

These use the finest run, `nr=40000`, `nmu=800`, and
`r/r_M in [1e-8,1e6]`. Units of signed Q2 are s^-2.

| Footing | Prescription | Signed Q2 | abs(Q2)/ceiling | Criterion |
|---|---|---:|---:|---|
| canonical | Legacy KT25 source-only **flux control** | -2.49908921058e-27 | 0.480594078958 | archived integral below ceiling |
| canonical | Physical source-only Hessian | -1.91928351621e-26 | 3.69092983887 | fails |
| canonical | Reciprocal fixed Gaussian | -5.67627125419e-27 | 1.09159062581 | fails |
| canonical | Plain QUMOND | -4.09821787692e-26 | 7.88118822485 | fails |
| alt | Legacy KT25 source-only **flux control** | -5.49507641164e-27 | 1.05674546378 | archived integral above ceiling |
| alt | Physical source-only Hessian | -3.07229926605e-26 | 5.90826781933 | fails |
| alt | Reciprocal fixed Gaussian | -8.42223022124e-27 | 1.61965965793 | fails |
| alt | Plain QUMOND | -4.70941145459e-26 | 9.05656048960 | fails |

The unrounded values, separate flux/density estimates, signed components,
boundaries and convergence rows are in `run_002/results.json`. The physical
source-only by-parts result differs from its independent density estimate by
`1.38e-10` canonical and `9.24e-10` alt in dimensionless q, caused by evaluating
a finite origin surface with floating arithmetic. This is negligible for its
grade. The reciprocal difference is at most `1.75e-15` in the finest run.

## Checks, provenance and limits

`test_cassini_v2.py` contains seven tests. Tests were written first, failed
because the implementation was absent, and then passed; the red logs are
`test_red.txt` and `test_v2_red.txt`. The v2 tests separately verify a centered
finite-difference Hessian of `erf(r/(sqrt(2)*sigma))/r`, normalized Gaussian
mass and field, literal archive reproduction, flux versus analytic density,
the nonzero source-only origin term, spherical symmetry, and nu=1/xi=0 limits.
The bounded `tests_001` run records all seven passing tests.

The physical run covers exactly two footings, three physical prescriptions and
four numerical settings each: 24 quadrature rows, no parameter search.
Settings are `(nr,nmu,rmin,rmax)` = `(20000,200,1e-7,1e5)`,
`(40000,400,1e-7,1e5)`, `(40000,400,1e-8,1e6)`, and
`(40000,800,1e-8,1e6)`. Separate literal archival controls and exact nu=1 controls
are also saved. Reciprocal results move less than `7.4e-14` relatively over
these settings. The plain-QUMOND density route converges more slowly near its
zero-field saddle; its finest discrepancy with the flux route is `1.11e-7`
canonical and `9.14e-8` alt in q. The archived KT16 plain value differs by about
`3e-4` relatively from the stable evaluation; KT16's own doubled-resolution
check and its `v<=400` independent integral already show this small variation.
This has no effect on either plain-QUMOND grade.

All 22 structured checks in `run_002/results.json` pass. Nu=1 gives exactly
zero phantom quadrupoles. The spherical density route leaves only
`-2.30e-32` roundoff; its criterion is absolute `1e-14`. This residual was the
sole reason `run_001` exited unsuccessfully: v1 incorrectly required exact
floating equality for that symmetry check. Its source files, contract and
manifest remain frozen and validate as a **failed** evidence record. V2 uses
new filenames, labels the legacy flux and physical Hessian separately, and
uses the stated spherical tolerance. It does not change the physical inputs.

`run_002/manifest.json` has status `completed` (runtime 7.07 seconds) and
validates against unchanged pinned inputs. `tests_001/manifest.json` also
validates as completed. The runner records Python/NumPy/SciPy versions, Git
revision and dirty state, argv, time, input hashes before/after and output
hashes. The physical run caps are 300 seconds wall time, 180 seconds CPU,
1 MiB combined logs and numerical-library threads set to one. CPU affinity
is unavailable on this macOS platform; no affinity or memory cap was claimed.
Arrays are evaluated in 256-radius chunks. No randomness is used.

Independent review by the sibling `filter_review` agent checked the STF
normalization, `T` and `T'`, surface sign, density divergence, radial-reference
subtraction and analytic origin correction. This review is additional
provenance, not an error bound or proof of physical applicability.

The outcome is **conditional on numerical tolerance: the fixed reciprocal
candidate fails the inherited Cassini cut on both frozen footings**. Convergence
is empirical, not interval-certified. The uniform external field, point Sun,
constant object-level width, simple nu and quadrupole-only observational
criterion are inherited premises. Neither source composition nor a common
state-dependent filter law is tested. An outer Gaussian also generally produces
an isotropic Hessian component; this diagnostic grades only the inherited
trace-free quadrupole and makes no claim of passing other Solar System tests.

## Reproduction commands

Run from the repository root. The original run argv is recorded verbatim in
the manifest. This equivalent explicit Python command constructs the same
bounded launch with a **fresh** output directory. It executes only the named
local calculation; input paths are read from its pinned contract.

```bash
PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'
import json
from pathlib import Path
import subprocess
import sys
root = Path.cwd()
base = Path('rebuild_2026_10_22/KT33_reciprocal_filter/cassini')
runner = Path('/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/run_experiment.py')
contract = base / 'contract_v2.json'
run = base / 'run_003'  # Must not exist; choose another unused name if needed.
argv = [sys.executable, str(runner), '--root', str(root), '--contract', str(contract)]
for path in json.loads(contract.read_text())['execution_artifacts']:
    argv += ['--input', path]
argv += ['--output', str(run), '--result', str(run/'results.json'),
         '--timeout', '300', '--max-cpu-seconds', '180', '--max-threads', '1',
         '--max-output-bytes', '1048576', '--', sys.executable,
         str(base/'cassini_v2.py'), '--output', str(run/'results.json')]
subprocess.run(argv, check=True)
PY
```

Bounded unit-test command (choose a fresh test directory on repetition):

```bash
PYTHONDONTWRITEBYTECODE=1 python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/run_experiment.py \
  --root "$PWD" \
  --contract rebuild_2026_10_22/KT33_reciprocal_filter/cassini/contract_tests.json \
  --input rebuild_2026_10_22/KT33_reciprocal_filter/cassini/cassini_v2.py \
  --input rebuild_2026_10_22/KT33_reciprocal_filter/cassini/test_cassini_v2.py \
  --output rebuild_2026_10_22/KT33_reciprocal_filter/cassini/tests_002 \
  --timeout 30 --max-cpu-seconds 20 --max-threads 1 --max-output-bytes 1048576 \
  -- python3 rebuild_2026_10_22/KT33_reciprocal_filter/cassini/test_cassini_v2.py
```

Validate any recorded run (replace the manifest path for a reproduction):

```bash
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py \
  rebuild_2026_10_22/KT33_reciprocal_filter/cassini/run_002/manifest.json --root "$PWD"
```
