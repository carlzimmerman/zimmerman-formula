# Native lensing constraints: usable operator, unrestricted fitting ruled out

2026-10-11. Advances priority 1 (cluster core mass). Theory still open; no
carrier, action, settling rate, physical cluster mass or kappa derivation here.
Both physical footings remain untested by this operator-only computation.

## Result

The catalogue yields 135 gold images of 49 source features in 27 galaxies.
Eliminating their unknown source-feature positions leaves 172 scalar linear
constraints on deflections evaluated at the measured positions. The operator is
saved in `run_v2/operator.npz`, with image order, groups and zsys in
`run_v2/results.json`. It does not contain a fitted physical mass map.

The proposed unrestricted positive-mass feasibility search is NOT a decisive
test: its continuum relaxation can match any finite prescribed point deflections
with arbitrarily little positive mass concentrated near the evaluation points.
This remains true for smooth positive mass patches if their density has no
uniform bound. A grid introduces an implicit resolution/concentration prior.
Thus a grid's success cannot establish our cold-energy mechanism, and its
failure need not survive refinement. This corrects the scope of the previous
handoff, rather than claiming a new viable theory.

## Source audit and retained failure

Frozen criteria `de0769647` expected the counts in the paper's prose. The first
run stopped at a quality-count check: prose says S=22/B=42, but CDS contains
S=21/B=43. Its parser slices agree with the byte definitions. The independent
HTML-table reader in `source_audit.py` matches the quality of every CDS row.
Gold count and selection are unchanged. `V2_CRITERIA.md`, committed alone in
`d858f7c7a`, declares the correction before rerunning. The original criteria,
script, contract and failed run are retained, not relabelled as passing.

Source: [Rihtarsic et al., arXiv:2601.22245v2](https://arxiv.org/html/2601.22245v2),
section 3 and Appendix A; [CDS J/A+A/710/A207](https://cdsarc.cds.unistra.fr/viz-bin/ReadMe/J/A%2BA/710/A207?format=html).
The lowercase ID suffix labels a distinct source feature; the final dot suffix
labels its images. zsys is the shared spectroscopic system value. Individual
NIRSpec values need not equal it. Rows of silver/bronze quality are excluded.
Original catalogue, metadata, versioned HTML and their hashes are preserved.
The full paper HTML is retained locally and excluded from Git; its exact URL
and hash are in `sources/provenance.json`. Reproduction on another checkout
requires fetching that version to the recorded path. The CC-BY CDS catalogue
is already committed in the preceding lane.

## Operator and conventions

Coordinates are east/north gnomonic tangent-plane angles in arcseconds, centred
on the mean gold RA/Dec. Minimum image separation is 0.2235276825 arcsec.
For n images of a feature, use the (n-1)-by-n Helmert matrix H:

    H[k-1,0:k] = 1/sqrt(k(k+1)); H[k-1,k] = -k/sqrt(k(k+1)).

Then H1=0, HH^T=I and H^TH=I-11^T/n. With source efficiency w_s=D_ls/D_s,

    beta_s = theta_i - w_s a_hat(theta_i)
    => H_s theta = w_s H_s a_hat(theta).

This is the thin-lens weak-field mass-deflection relation, not an adoption of
another theory's phantom gravity. A physical prediction must compute a_hat
from actual baryon plus cold mass and must declare its relativistic lensing
relation. Distances must come from the framework's background; none are inferred
in this run. No external halo template, QUMOND calculation, or EFE is imported.

172 is an algebraic dimension, not a calibrated number of independent noisy
observations. Multiple features in a galaxy share redshift and systematics.
Orthonormal contrasts do not magically whiten measurement or modelling errors.
Mapping image-position errors into source-plane errors involves the model's
Jacobian. A source-plane residual threshold cannot be borrowed from an external
image-plane fit. Future scoring must propagate this relation or solve directly
for image positions, including associations and extra-image completeness.

## Why unrestricted positive mass can fake this test

Normalize the positive deflection coefficient to one, so a unit point mass at
y contributes k(x-y)=(x-y)/|x-y|^2. Let x_i be any finite collection of distinct
image positions and let d_i be any finite target deflections. A fixed background
can be included by subtracting its deflection from d_i. For any strictly positive
source efficiencies, take d_i=(theta_i-beta_s)/w_s-a_background(theta_i).

Choose B>max_i,component |d_i|. At each x_i put masses at x_i-epsilon e_x,
x_i+epsilon e_x, x_i-epsilon e_y and x_i+epsilon e_y, respectively:

    epsilon(B+v_ix)/2, epsilon(B-v_ix)/2,
    epsilon(B+v_iy)/2, epsilon(B-v_iy)/2.

Their SELF contribution at x_i is exactly v_i. All other image points have a
strictly positive minimum separation delta. For epsilon<delta/4, their cross
contributions are smooth. Write the complete finite linear system as

    (I+E_epsilon) v + b_epsilon = d.

The baseline symmetric pairs give b_epsilon=O(epsilon B). The v-dependent cross
terms are proportional to epsilon times the difference of k evaluated at two
points separated by 2epsilon. Since derivatives of k are bounded away from its
origin, E_epsilon=O(epsilon^2). Constants may depend on this finite point set.

For small enough epsilon, ||E_epsilon||<1; the inverse exists by the Neumann
series. Thus v=d+O(epsilon B), and |v_component|<B eventually. Every mass is
strictly positive, the desired deflections are matched EXACTLY, and

    M_total = 2 N epsilon B -> 0.

This proves the continuum construction for each fixed finite target set; the
numerical run alone would not. Replacing each point by a circular smooth
positive projected mass patch of radius <epsilon/4 leaves its exterior
deflection unchanged, so all evaluated deflections persist. The peak surface
density grows without bound as epsilon shrinks. Smoothness of each individual
map alone therefore does not cure the loophole; uniform concentration control
or the physical profile does. No claim of novelty for this inverse-problem
observation is made.

An exact total budget alone also cannot fix this unrestricted relaxation:
surplus mass can be placed in a circular projected annulus enclosing all image
positions, with zero deflection inside its hole. Such freely selected clumps
and annuli are NOT claimed to obey candidate B, its round settled profiles,
its catchments, phase-space restrictions, equilibrium or its unknown action.
Additional images, distortions and time delays generally change. Therefore
matching sampled deflections is not matching the full lensing observations.

## Executed adversarial check

For all 135 gold positions, divide coordinates by their minimum separation,
choose each feature's source position as its image mean, set w=1 and background
zero, and fix B=2*maxabs(target)+1. These are dimensionless mathematical controls,
not cosmology assumptions or an astrophysical fit. Four clumps per image give
540 positive masses and a 270-by-270 linear solve.

| epsilon / minimum separation | Total dimensionless mass | Max relative residual |
|---:|---:|---:|
| 1e-3 | 61.99506824 | 2.49e-15 |
| 1e-4 | 6.19950682 | 2.36e-15 |
| 1e-5 | 0.61995068 | 2.86e-15 |
| 1e-6 | 0.06199507 | 2.61e-15 |

All weights positive; condition numbers <=1.000003. Source selection, gnomonic
inverse, Helmert identities, point-lens normalization, symmetric Jacobian and
single-source mass-sheet control pass. MUTATE controls reject wrong deflection
sign/efficiency, merged source features, duplicate IDs, inconsistent/missing
redshifts, and bad quality. V2 passes 74/74 checks. Original run remains FAILED
on the prose/table count discrepancy. Both manifests retain their actual status.
No large simulation or multi-agent work was launched. Review is analytic
self-review plus numerical controls, not independent external review.

## Consequence for the remaining theory work

The fixed repaired-kernel settled profile must be imposed before assessing
lensing; it cannot be replaced by an arbitrary positive fitted map. Any extra
unsettled core mass must come from a derived phase-space distribution and host
ownership rule. The previously proved exterior-shell bound remains relevant
to that supply, but does not specify it.

Next physical obligation: provide measured baryonic substructure and a uniquely
declared host assignment to construct the framework's current merger mass
field, then apply this operator on BOTH footings. The smooth F26 decomposition
and isolated CFG625 progenitors are not a complete current-epoch map. In
particular, galaxy member contributions cannot be replaced with external
fitted dark halos or ignored and called a theory exclusion.

An action-derived prediction is still required. A full settled-profile miss
could falsify that declared equilibrium reading; it would not exclude all
non-equilibrium histories unless the dynamics bound their allowed departures.
No concentration parameter will be introduced to make a lens fit. The
unrestricted-placement route is closed as a standalone discriminator; the
native fixed-profile/action route remains open. Kernel, kappa, cosmic ratio,
other lanes and sealed predictions are unchanged.
