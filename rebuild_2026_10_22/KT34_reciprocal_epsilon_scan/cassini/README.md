# KT34 Cassini scan of the common Gaussian width

Varying only the common source and outer Gaussian standard deviation gives
one numerically resolved Cassini threshold on each frozen footing:

| Footing | Refined epsilon at equality | Signed Q2 at equality | Sampled passing side |
|---|---:|---:|---|
| canonical | 0.515606478108 | -5.2e-27 s^-2 | larger epsilon |
| alt | 0.592818409720 | -5.2e-27 s^-2 | larger epsilon |

No sign reversal or cancellation island was found in 407 widths per footing.
This is a finite numerical statement, not a proof that an arbitrarily narrow
island cannot occur between samples. Separately, the analytic bound below
proves that **every epsilon >= 4 passes this Cassini quadrupole cut** on both
footings. Cassini therefore does not exclude the whole fixed-Gaussian family.
Whether the family also passes the Milky Way constraints is a separate task.

## Contract and unchanged inputs

The map is `N rho + S Phi_ph[S rho]`, with normalized isotropic Gaussian `S`.
The sole varied physical parameter is
`sigma_source = sigma_outer = epsilon`, in units `rM = sqrt(GM/a0)`.
The physical Newtonian point-source term remains unsmoothed; only the phantom
potential receives the outer filter. Each object-level sigma is held fixed
when varying its source. No width law, source-dependent width, or refit is used.

The import-safe corrected implementation
`KT33_reciprocal_filter/cassini/cassini_v2.py` is imported unchanged. Its
constants remain `GM = 6.6743e-11 * 1.98892e30`, `gext = 2.32e-10`,
canonical `a0 = 9.3603e-11`, alt `a0 = 1.1312e-10`, simple
`nu(h) = 1/2 + sqrt(1/4 + 1/h)`, and ceiling `5.2e-27 s^-2`.
The conventions are `q = STF zz Hessian / (a0/rM)` and
`Q2_signed = (3/2)(a0/rM) q`. The cut grades `abs(Q2)`.

For every positive common width the outer kernel is O(r^5) at the origin,
so its exact inner surface is zero. Epsilon zero uses the plain point-source
control, whose inner surface also vanishes. The source-only origin defect
identified in KT33 is never reintroduced. The numerical finite-domain outer
surface is retained, and the independent analytic-density integral is also
evaluated. No frozen or archived files were edited.

## Scan, crossings, and controls

The sweep is the deduplicated union of zero, `1e-6`, `1e-5`, 301 logarithmic
points from `1e-4` to `10`, 101 linear points from `.35` to `.85`, `.5`,
`100`, and `1000`. It contains exactly 407 widths per footing, 814 physical
rows total, with `nr=6000`, `nmu=120`, and `r in [1e-8,1e6]`.
The signed q is retained, and **every** sampled sign and ceiling crossing is
searched rather than assuming monotonicity.

The only ceiling brackets are `[.515,.520]` canonical and `[.590,.595]` alt.
There are no sign brackets. The only sampled extremum brackets are at
epsilon below `1e-4`; higher-resolution evaluation shows variations of order
`1e-9` in the ceiling ratio on the plain-limit plateau, consistent with
roundoff. There are no resolved finite-width extrema.

Each crossing is solved at `16000 x 240`, checked at `40000 x 800`, then
checked at `60000 x 1000` with expanded domain `[1e-10,1e7]`.
At the saved canonical root, the three ceiling ratios are
`1.000000000000010`, `1.000000000000016`, and `1.000000000000399`.
At the saved alt root they are `0.999999999999585`,
`0.999999999999590`, and `0.999999999999973`.
The independent density/flux discrepancies at the expanded checks are
`4.40e-14` and `3.29e-14` in q. Root neighbors at epsilon +/- `1e-6` bracket
the cut by about `5.55e-6` canonical and `4.86e-6` alt in ceiling ratio.
Equality is allowed by the criterion; floating-point classification of the
root itself is consequently not used as a separate physical conclusion.

Representative high-resolution ratios `abs(Q2)/ceiling` are:

| epsilon | canonical | alt |
|---:|---:|---:|
| 0, plain QUMOND | 7.88118822485 | 9.05656048960 |
| 0.000001 | 7.88118822649 | 9.05656048970 |
| 0.01 | 7.88058527592 | 9.05601201416 |
| 0.1 | 7.36779074791 | 8.58564884947 |
| 0.2 | 5.50147220779 | 6.68781201769 |
| 0.3 | 3.77311651244 | 4.85507052305 |
| 0.5 | 1.091590625806 | 1.619659657931 |
| 1 | 0.141537168901 | 0.213656381266 |
| 10 | 0.000141878103 | 0.000214408948 |
| 100 | 0.000000141878 | 0.000000214409 |

Epsilon `.5` reproduces KT33 within `2e-14` relative. The tiny-width controls
numerically approach the plain result; this experiment does not establish a
uniform error bound for the singular epsilon-to-zero limit.
At small widths the Newtonian external-field saddle makes density quadrature
converge more slowly. The largest coarse sweep discrepancy is `5.78e-5` q
near epsilon `.292864` canonical and `2.50e-5` near `.316228` alt. The high
resolution small-width controls have discrepancies about `1e-7` q, far below
their failure margins. These errors do not occur near either ceiling crossing.

The scan numerically indicates the passing branches
`epsilon >= 0.515606478108` canonical and
`epsilon >= 0.592818409720` alt. The portion below 4 is empirical coverage
with refined crossings; it is not an interval-certified continuum claim.

## Independent large-width asymptotic

Set `eta=gext/a0`, `r=epsilon*x`, and `g=epsilon^-2 f(x)`.
As epsilon grows, the field is uniformly external-field dominated. Linearize
the phantom response in the source field. The two equal Gaussian factors
combine into a Gaussian of width `sqrt(2)*epsilon`. The angular average
`<mu^4 - mu^2/3> = 4/45` then gives

```
q = [2/(45 sqrt(pi))] eta nu'(eta) epsilon^-3 + O(epsilon^-7)
  = -epsilon^-3 / [45 sqrt(pi) eta sqrt(1/4+1/eta)] + O(epsilon^-7).
```

The quadratic term vanishes by parity. The leading coefficients are
`-0.006257551433211981` canonical and `-0.007117993188982303` alt.
At epsilon 10, the relative deviations of `q*epsilon^3` from these limits
are `-2.404e-7` and `-3.512e-7`. At 100 they are below `4.7e-11`.
At 1000 the subtraction of almost equal nonlinear responses costs precision:
the relative deviations are about `1.06e-8`, while the absolute ceiling
ratios are only `1.42e-10` and `2.14e-10`. That last point is a tail control,
not an accuracy claim at the `1e-11` relative level.

## Analytic uniform passing tail

The following bound covers every epsilon >= 4, including unsampled widths.
It does not assume monotonicity. Put `c=sqrt(2/pi)` and write

```
f(x) = M(x)/x^2,
0 <= f(x) <= min(c*x/3, x^-2),
0 <= T(x) <= min(1, c*x^5/15),
div g = epsilon^-3 c exp(-x^2/2).
```

The Gaussian enclosed-mass and kernel inequalities follow by bounding their
positive integral representations. Thus
`gmax <= (c/3)^(2/3) epsilon^-2 < 1/2` when epsilon >= 1.
Both frozen eta values exceed 2, so `eta/2 <= h <= 3eta/2`.
Write `A(h)=nu(h)-1` and `L=abs(nu'(eta/2))`. Both A and abs(nu') decrease.
For the radial source Jacobian J, its eigenvalues are `g'`, `g/r`, `g/r`;
since `g'=div g-2g/r`, `||J|| <= div g+2g/r`. The phantom density obeys

```
D = A(h) div g + [nu'(h)/h] u^T J u,
abs(D) <= A(eta/2) div g + (3eta/2)L [div g+2g/r].
```

The density Hessian has weight `-T(3mu^2-1)/2`, whose absolute angular
integral is `4/(3sqrt(3))`. Splitting the positive radial integrals at x=1
gives the elementary bounds

```
I1 = integral T(x)c exp(-x^2/2) d(log x)
   <= c^2/75 + c exp(-1/2),
I2 = integral T(x) f(x)/x d(log x)
   <= c^2/225 + 1/3,
abs(q) <= K epsilon^-3,
K = 4/(3sqrt(3)) [A(eta/2) I1 + (3eta/2)L (I1+2 I2)].
```

The displayed footing-specific ratio bounds are `28.4732/epsilon^3` and
`42.6218/epsilon^3`. A conservative common bound can be certified with
rational slack: `c<.8`, `exp(-.5)<.607`, `4/(3sqrt(3))<.77`,
`A(eta/2)<=A(1)<.62`, `(3eta/2)L<=3/sqrt(5)<1.35`, and the physical
prefactor divided by the ceiling is less than 31 on both footings.
These imply

```
K < 54317417/37500000,
abs(Q2)/ceiling < 45/epsilon^3  (epsilon >= 1).
```

Consequently `epsilon >= 4` implies a ratio below `45/64 = .703125`.
The `tail_bounds.py` run checks the rational slack and both physical
prefactor inequalities exactly; sharper decimal constants are supplementary.
The elementary exponential inequality is checked using the positive Taylor
sum through order four. The analytic proof and constants were independently
reviewed by the sibling `epsilon_review` agent. This guarantee applies only
to the inherited trace-free quadrupole diagnostic.

## Evidence and reproducibility

All runs use prewritten contracts, finite wall/CPU/log caps, and numerical
threads fixed to one. No memory or CPU-affinity cap is claimed on this macOS
host. No randomness is used. Software: Python 3.9.6, NumPy 1.26.2,
SciPy 1.11.4. Each manifest pins before/after input hashes and output hashes.

| Contract | Result | Status | Runtime |
|---|---|---|---:|
| contract_sweep.json | sweep_001/results.json | completed; manifest validated | 10.72 s |
| contract_refine.json | refine_001/results.json | completed; manifest validated | 15.41 s |
| contract_tail.json | tail_001/results.json | completed; manifest validated | under 1 s |

The scan and crossing outcome is **conditional on numerical tolerance**.
The analytic tail is a separate bound, with exact rational arithmetic checking
its safe constants. Neither evidence source validates a full Solar ephemeris,
an isotropic Hessian component, the Milky Way, dwarfs, SPARC, or a universal
state-dependent filter law.

To reproduce a sweep from the repository root, choose a fresh output directory:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'
import json, subprocess, sys
from pathlib import Path
base=Path('rebuild_2026_10_22/KT34_reciprocal_epsilon_scan/cassini')
contract=base/'contract_sweep.json'
run=base/'sweep_002'  # Must be new.
runner=Path('/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/run_experiment.py')
argv=[sys.executable,str(runner),'--root',str(Path.cwd()),'--contract',str(contract)]
for path in json.loads(contract.read_text())['execution_artifacts']:
    argv+=['--input',path]
argv+=['--output',str(run),'--result',str(run/'results.json'),
       '--timeout','300','--max-cpu-seconds','240','--max-threads','1',
       '--max-output-bytes','1048576','--',sys.executable,
       str(base/'epsilon_scan.py'),'--mode','sweep','--output',str(run/'results.json')]
subprocess.run(argv,check=True)
PY
```

For refinement, use `contract_refine.json`, a fresh `refine_002` directory,
`--mode refine`, and `--scan .../sweep_001/results.json`. For the tail arithmetic,
use `contract_tail.json`, `tail_bounds.py`, a fresh `tail_002` directory, and
30-second wall/20-second CPU caps. Exact original argv arrays are stored in
each manifest. Validate using the installed computation-audit
`scripts/validate_manifest.py MANIFEST --root "$PWD"`.
