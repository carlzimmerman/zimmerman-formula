# KT34 Milky Way: epsilon scan of the corrected Gaussian

The corrected reciprocal model has Milky Way passes at smaller epsilon, but
none in either numerically identified Cassini-admissible branch. This lane
keeps all original baryons, priors, acceleration footings, interpolation,
simple-nu law and observational cuts fixed. Only epsilon changes. KT33's
implementation is imported unchanged.

The production finite grid gives upper passing width-bin edges
**0.3135487841 canonical** and **0.4652841728 alternative**. These are exact
edges of the retained width quantization on that numerical grid, not physical
precision claims. Selected higher spatial resolutions move the canonical
edge to **0.3119849530** and the alternative edge to **0.4606545179**.
Use approximately **0.31 canonical** and **0.46 alternative** for the
resolved numerical scale of the upper MW boundary; see endpoint refinements.
Both are well below the Cassini onsets, **0.5156064781** and **0.5928184097**.

## What was held fixed

For each original cell and footing,

```
RM = sqrt(4.30091e-6 (Mstar + Mgas)/(a0 * 3.0857e19/1e6)),
xi = exp(round(log(epsilon * RM)/0.005) * 0.005),
Phi = N rho + S* Phi_ph[S rho].
```

At epsilon zero, S is exactly the identity. `Mgas` is
11910967635.394314 solar masses. The rounding convention, full baryonic mass,
gas density and original physical conversion are unchanged. The normalized
Gaussian is `S=H diag(1/H1)` and its weighted adjoint is
`S*=diag(1/H1) H`. Width is held fixed during source variations. Both source
and outer kernels use that same width. There is no baryon fitting, change of
thick-disc share, altered cut, or source-only substitution.

Each full population contains exactly **1,375 original in-prior cells**.
The cell identity/order is retained in the result files. The code expands
each source into 11 fixed gas/bulge/disc components, filters the components
once per shared quantized width, and recombines them with the original
nonnegative coefficients. Nonlinearity is applied separately to each cell.
Literal density comparisons and all-cell epsilon=0.5 reproduction verify the
cache. The maximum epsilon=0.5 discrepancy from KT33 is below `1e-10 km/s`
in circular speed and `5e-9` in Ou chi-square.

## Coarse and refined scans

`high_run` evaluates every original cell at epsilon
0.5, 0.55, 0.6, 0.75, 1 and 2, using twice the original spatial resolution
(393 radial by 96 angular cells) and even harmonics through degree 48.
All 16,500 evaluated cells fail the all-four-cut test. The epsilon=0.5 control
reproduces KT33's minimum Ou chi-squares 183.076924 and 76.848184.

`low_run` explores 0, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4 and 0.45 at
the original spatial resolution and degree 94. Most narrow-width cases
violate the inherited `1e-5` negative-source-mass tolerance. Their apparent
pass counts are **diagnostic only**, and do not become validated population
counts merely because execution completed.

`boundary_run` then evaluates the full populations at twice spatial resolution
and degree 96. All source-tail gates pass. The all-four-cut counts are:

| epsilon | Canonical | Alternative |
|---:|---:|---:|
| 0.30 | 4 | 42 |
| 0.31 | 2 | 44 |
| 0.32 | 0 | 43 |
| 0.33 | 0 | 43 |
| 0.45 | 0 | 6 |
| 0.46 | 0 | 2 |
| 0.47 | 0 | 0 |
| 0.48 | 0 | 0 |

Selected narrow-width witnesses were independently recalculated at three
times spatial resolution and degree 192. The canonical witnesses at epsilon
0.15, 0.25 and 0.30 pass, as do alternative witnesses at 0.15, 0.20, 0.30,
0.40 and 0.45. Their negative-mass fractions remain below `1e-5`. This
establishes these individual passing examples, not complete lower-epsilon
pass intervals. The disconnected structure of lower MW windows has not been
exhaustively mapped.

## Exhaustive coverage of the upper bands

No monotonicity assumption or interpolation between epsilon samples is used.
For each fixed cell, the code enumerates every integer k whose width plateau
intersects the declared interval:

```
exp(0.005*(k-1/2))/RM <= epsilon <= exp(0.005*(k+1/2))/RM.
```

Including both neighboring states at a rounding tie gives a conservative
closed cover; endpoint membership itself follows the original round-to-even
rule. Reported upper values are suprema of passing plateau interiors.

| Exhaustive run | Canonical | Alternative |
|---|---:|---:|
| Transition epsilon band | [0.30, 0.5156064781] | [0.44, 0.5928184097] |
| Transition cell/width states | 150,398 | 83,407 |
| States passing necessary L1 | 2,507 | 770 |
| States passing all four cuts | 25 | 57 |
| Passing union within transition band | [0.30, 0.3135487841] | [0.44, 0.4652841728] |
| High epsilon band | [0.5156064781, 2.5] | [0.5928184097, 2.5] |
| High-band cell/width states | 435,481 | 397,062 |
| High-band states passing L1 | 0 | 0 |
| High-band maximum vc(R0), km/s | 216.989125 | 218.178474 |

L1 requires at least 219.9 km/s. Hence every high-band width state fails a
necessary MW cut, with margins 2.910875 and 1.721526 km/s. The transition
run excludes all higher disconnected MW islands within its entire band.
The independent reviewer rebuilt all per-cell/per-width counts from the
KT33 archived masses using a different ceil/floor enumeration; see
`../review/coverage_001` and `../REVIEW.md`.

The cheap L1 calculation is the exact weighted discrete dual identity. If l
forms the inherited radial gradient at R0, W is cell volume, L the Poisson
matrix, G the cell gradient and A=(nu-1)G N(S rho), then

```
l S* [-L^-1 W^-1 G^T W A]
    = -[G L^-1 S(W^-1 l^T)]^T W A.
```

One dual solve per width replaces a phantom solve per cell. Every L1 survivor
in `transition_run` receives all original four cuts. Full solves agree with
the dual circular speed within `5.4e-9 km/s`. A separate full re-evaluation
of all 233,805 transition states finds the closest rejected L1 margins are
`8.62e-5` canonical and `0.001762` alternative km/s, safely larger than the
measured dual reproduction error and the declared `1e-7` audit separation.

The exhaustive high run uses degree 48 and a 300-kpc filter radius. The
transition run uses degree 96 and a 120-kpc radius. All mass errors are below
`2.5e-15`; conservative bounds on negative source mass are below `9.8e-7`.
Those bounds follow by summing each component's negative mass with its
nonnegative source coefficient. The code separately asserts the coefficient
signs and the numerical gates.

## Endpoint and filter refinement

The production maximum is at original cell index 1362, width index k=246,
in the canonical footing, and index 1359, k=306, in the alternative footing.
Indices are zero-based and retain the exact original iterator order.

The canonical terminal Ou chi-square rises from 59.71567 at twice spatial
resolution to 59.88618 at three times, 59.93648 at four times and 59.96045
at five times. The ceiling is 59.89250. Thus the terminal plateau eventually
fails; the next lower plateau, k=245, passes at both four and five times.
Its upper edge is 0.3119849530. This is why the ten-digit production edge is
not advertised as a continuum-accurate endpoint.

The alternative terminal case is similarly marginal: at four/five times
resolution its K(R0)=70.80114/70.80057 exceeds 70.8. Its Ou chi-square is
59.86802/59.88809. The neighboring k=305 case at index 1368 also fails at
four/five times. `endpoint_extended_run` finds the next lower upper edge
0.4606545179 at four, five and six times spatial resolution. At six times,
the original terminal k=306 passes K(R0), but fails Ou chi-square with
59.89454. The k=304 witness at index 1368 passes with Ou chi-square 58.91280.
These are selected checks, not an exhaustive finer-grid scan or rigorous
continuum error bounds. The alternative terminal case remains numerically
close to a cut; the conservative production upper edge remains 0.4652841728.

At the Cassini onsets, three-times resolution moves the worst high-band
circular speeds to 217.004300 and 218.192876 km/s. Doubling the filter radius
from 300 to 600 kpc leaves those values unchanged at displayed precision.
The same filter-radius check at epsilon 2.5 changes circular speed by less
than `3e-13 km/s`. These numerical changes are far smaller than the L1
failure margins. The separate review derives a continuum MW tail bound for
every epsilon >=2.5; this lane does not claim that its finite Gaussian alone
proves an infinite-epsilon statement.

## Provenance and reproduction

Every scientific run has a v2 computation-audit manifest with observed
input hashes before/after, output hashes, interpreter/library versions,
repository revision/dirty state, actual command, timing and limits. All
completed manifests validate against the current project. `checks_run`
reports `passed: true`; negative-tail failures in the preliminary `low_run`
remain explicitly recorded and are not waived.

Each runner invocation uses 1,800 wall seconds, 1,750 CPU seconds, one
numerical thread and 1 MiB of logs. No address-space cap is claimed. The
scripts are import-safe. To reproduce a run, choose a **new** output folder:

```bash
python3 rebuild_2026_10_22/KT34_reciprocal_epsilon_scan/mw/run_scan.py \
  --contract transition_contract.json --run transition_rerun \
  --script exact_all.py --refine 2 --lmax 96 --cut 120

python3 rebuild_2026_10_22/KT34_reciprocal_epsilon_scan/mw/run_scan.py \
  --contract exact_contract.json --run exact_rerun \
  --script exact_l1.py --upper 2.5 --refine 2 --lmax 48 --cut 300
```

The wrapper passes the contract's declared input closure to the bounded
runner. It never executes a command read from an evidence manifest.
Original KT33 and prior-lane files were not edited. No commits were made.

The conclusion is conditional on the stated finite spatial/harmonic
approximations, with selected refinement evidence. It does not transfer an
empirical pass to SPARC, dwarfs or clusters, derive epsilon, prove a universal
system-mass rule, or establish relativistic completion. The Cassini worker
and independent review retain their own sampled-branch qualifications.
