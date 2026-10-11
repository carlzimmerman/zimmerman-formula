# Cluster closure: an exterior-mass bound and a direct lensing route

2026-10-11. Criteria frozen alone in commit `7779a6213` before computation.
The theory remains open. Kappa is fitted; the two footings remain separate.
This is a conditional mathematical diagnostic, not a new observational verdict.

## What changed

The updated owner brief prioritizes the cluster core deficit. Consequently the
proposed spherical assembly simulation is deferred: its phenomenological support,
damping and softening parameters cannot meet the new no-additional-constants
closure criterion. Its reciprocal mechanics remain useful, but another toy
capture experiment would not resolve the current first obligation.

Instead, we checked whether exterior cold mass can supply a projected core
deficit without changing the spherical gravitational force inside the core.
The calculation gives a necessary budget/placement condition valid independently
of the settling rate. We also acquired the public spectroscopic image catalogue
needed to replace provisional aperture anchors with direct lensing constraints.

## Exact projection bound

For a spherical shell of mass dM at radius r and a cylindrical aperture R,
the shell contributes p(R,r)dM, with

    p(R,r) = 1                               (r <= R)
             1 - sqrt(1 - R^2/r^2)           (r > R).

Proof: the aperture selects two polar caps with sin(theta)<=R/r. Their combined
solid angle is 4*pi*(1-cos(theta)). Divide by 4*pi. For fixed R the fraction
decreases with r. Thus any nonnegative spherical mass B supported at r>=r0>=R
satisfies

    Delta M_projected(<R) <= B * p(R,r0).

This bound is sharp as a geometric statement: mass concentrated in a shell at
r0 saturates it. No equilibrium or formation mechanism for such a shell follows.
The shell exerts zero Newtonian force at r<r0; its lensing contribution is not
zero. Therefore a projected aperture deficit alone is not a proof that the
interior force law must change.

For a positive deficit Delta and budget B, write q=Delta/B. If q>1 there is no
solution of this exterior-only problem. Otherwise a necessary condition is

    r0 <= R / sqrt(q*(2-q)).

At r0=2R the maximum aperture fraction is 0.1339745962; at 4R it is
0.03175416345. Distant mass is an inefficient spherical repair.

## Conditional application, preserving the existing profile

Use CFG625's static profiles without rerunning or modifying them. For each
declared retained-baryon fraction f=1,.90,.86, the illustrative remaining budget is

    B = 5.364 * M_b / f - M_cold,total.

Subtracting only the already projected cold mass would double-count supply.
These are contextual allocations of original baryons, not a derived host
catchment. The global cosmic ratio alone does not fix an individual host's mass.
Negative B is flagged as inconsistent bookkeeping for that scenario.

For B3 (measured gas/stars approximation), f=.86, R=250 kpc:

| Footing / host | Remaining B (solar masses) | Recorded central deficit | Largest possible r0 |
|---|---:|---:|---:|
| canonical main | 7.2151e14 | 1.6806e14 | 389.68 kpc |
| alt main | 6.8319e14 | 1.6197e14 | 386.70 kpc |
| canonical sub | 2.8642e13 | 1.6030e14 | impossible with this budget |
| alt sub | 1.6935e13 | 1.5700e14 | impossible with this budget |

At the recorded lower two-sigma anchors, main limits become 411.95/409.65 kpc;
the sub remains budget-infeasible. These bounds apply to extra positive mass
while retaining the existing full profile. Redistributing that profile, borrowing
from a shared catchment, changing the original baryon allocation, nonspherical
structure, and merger evolution lie outside the bound. Merger apertures also
include contributions from other components. This is NOT a Bullet exclusion.

An exterior addition preserves the local law only inside its inner radius. If
the framework requires the exact baryon-only law at every radius occupied by
the addition too, that addition violates the law there. A reservoir explanation
must therefore declare its unsettled domain and derive its evolution.

## Evidence and controls

`run/results.json`: 74/74 checks, 96 conditional rows. Independent angular
counting uses 200000 directions per shell. Positive mixture bounds, analytic
endpoints, inverse recovery and three kinds of MUTATE control pass. The manifest
validates with current input/output hashes. Standard-library calculation only;
no PM jobs or large arrays. Analytic self-review checks both polar caps,
monotonicity, force-versus-projection distinction and total-mass accounting.
No independent agent review was performed. Conservation checks do not establish
physical realizability, nor does this bound determine a cold carrier or action.

## Source audit changes the next test

[Cha et al. 2025, published ApJL 987 L15, section 3.1](https://inspirehep.net/files/6e0881d4d2520b1febd14709f20f9343)
reports 250-kpc masses of (1.59,1.67,.87)e14 solar masses for its two main BCG
centres and subcluster centre. These are reconstruction outputs, not raw data.
They cannot simply replace CFG625's anchors: centre definitions, epoch, geometry,
photometric-redshift uncertainties and overlapping main apertures matter.
No ratios to these smaller masses were scored.

[Rihtarsic et al. 2026, arXiv:2601.22245v2, sections 5.3 and 7](https://arxiv.org/html/2601.22245v2)
compares reconstructions and finds closest aperture agreement near 60 kpc.
It supplies 135 secure images from 27 spectroscopic systems and publishes the
catalogue and model products. Use observed positions/redshifts as constraints;
its fitted halos and maps remain context, not our theory's prediction.

The older P16 target remains a provisional transcription here. Publisher fetch
failed; the web PDF extractor rejected the large arXiv file. We have not verified
its subcluster value from full text. No new data result rests on that attribution.
Neither JWST paper is newly released this week. The useful new step in this lane
is acquiring the raw catalogue and changing the test from mass-anchor selection
to a framework-native observable calculation.

## Next theoretical door: eliminate unknown source positions

Assume the declared weak-field, thin-lens relation for ordinary gravitating
cold mass, with distances computed from the framework's specified background.
For image i of source feature s,

    beta_s = theta_i - w_s * a_hat(theta_i),  w_s = D_ls/D_s.

Subtract two images of the SAME feature:

    theta_i - theta_j = w_s * [a_hat(theta_i)-a_hat(theta_j)].

The unknown source position cancels exactly. Spectroscopic redshifts fix which
distance ratio applies. For a fixed mass basis, deflection is linear in mass.
Thus nonnegative cold-mass coefficients, conservation bounds, fixed-law density
constraints, and bounded image residuals define a finite convex feasibility
problem. This can test whether ANY allowed placement works before inventing
another relaxation rate. This linear formulation holds at fixed observed image
locations; matching it is necessary, not sufficient for the full image topology.

For exact equalities Ax=b and x>=0, a dual vector y with A^T y>=0 but b^T y<0
would certify infeasibility of that finite model. A robust observational use
must include uncertainties and nuisance geometry, discretization/refinement
checks, and the proper inequality dual. A finite basis exclusion is not a
continuum exclusion without interpolation bounds. A feasible x supplies neither
a formation history nor a derived action. No such feasibility run is claimed here.

Executable next handoff: freeze a catalogue parser and its controls; retain secure
systems and separate resolved source features correctly; verify redshift/group
consistency. Then freeze the native deflection operator and positional-error
treatment, with point-lens, mass-sheet and wrong-redshift MUTATE checks. Use both
footings separately and the same measured baryons; include the complete merger
geometry rather than isolated static progenitors. Do not adopt external halo
templates. The repaired kernel, baryon-only switch, kappa and sealed predictions stay
unchanged. No theory-level failure or success follows until this comparison and
the remaining action/growth obligations are actually resolved.

Git provenance: while these outputs were staged, another writer committed the
shared index in `2f6846261` (labelled CFG628). That commit consequently contains
this lane's outputs too. Our own criteria-only commit `7779a6213` still precedes
our run. No other lane's files or criteria were edited here; history is preserved.
