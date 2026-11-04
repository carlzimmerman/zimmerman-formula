# KT36: new response laws with the original baryons and cuts

**A common physical Gaussian length can pass the original Milky Way and
Cassini checks, but the same corrected law fails the isolated dwarf
discriminator.** The tested constitutive changes and positive mixtures did
not produce a joint MW/Cassini survivor. No general response-law exclusion
or broadly successful gravity model follows.

This phase executes the user's authorization to change the response law
while retaining the baryon prescriptions and observational cuts. It leaves
KT33/KT34 and the original sources untouched. The fixed-length result changes
the object-mass width rule; it does not reopen the excluded common-epsilon
simple-nu model under its original assumptions.

## One common 3 kpc length: a real but limited two-check witness

Use the same state-independent physical Gaussian S_ell for every density,
with ell=3 kpc, and the original simple nu. The reduced energy and its
derivative are

    U = U_N + U_ph[S_ell rho],
    Phi = N rho + S_ell* Phi_ph[S_ell rho].

This is a single unsplit nonlocal law: no Sun/Galaxy mass partition or
object-specific width is needed. It replaces dimensionless epsilon by a
phenomenological physical length; the length is not derived. A
nonrelativistic action does not establish relativistic or dynamical health.
See [the derivation](universal_length/README.md).

The full original 1,375-cell baryon grid per footing gives:

| Universal length | Canonical four-cut passes | Alternate four-cut passes |
|---|---:|---:|
| 2.5 kpc | 3 | 45 |
| 3.0 kpc | 5 | 39 |
| 3.5 kpc | 0 | 31 |

These are 8,250 production cell-length evaluations. No cell passed the
separate strict vertical scale-length diagnostic. The two frozen 3 kpc
witnesses survive all six selected spatial/angular/domain checks each.
At refinement 5:

| Observable | Canonical, cell 1374 | Alternate, cell 1227 | Frozen criterion |
|---|---:|---:|---|
| Local circular speed (km/s) | 226.38354 | 225.93338 | Both original L1 bands |
| Local vertical force equivalent (Msun/pc^2) | 69.80799 | 69.22720 | 62.0 to 70.8 |
| 43-point vertical chi-squared | 42.81148 | 45.31890 | <=67.45935 |
| 37-point rotation chi-squared | 49.05954 | 36.91775 | <=59.89250 |
| Vertical scale length (kpc) | 3.25983 | 3.26736 | Separate strict band: 2.42 to 3.02; both fail |

Both witnesses use BV2 structure, thick fraction .35, bulge mass 2.12e10
Msun, thin radial length 2.6 kpc and thick radial length 2.0 kpc. The
canonical witness has sb=53.9, ht=.35, hk=1.08; the alternate has sb=50.5,
ht=.30, hk=.90. These are existing grid cells, including a canonical prior
corner, not a new baryon fit or a mid-box success.

[Full grid](mw/universal_grid_001/results.json) ·
[Refinements](mw/universal_refine_001/results.json) ·
[Independent score/action review](alternative/UNIVERSAL_REVIEW.md) ·
[Figure](mw_witnesses.png) · [PDF figure](mw_witnesses.pdf)

## Two analytic Solar bounds

For the same whole-space fixed Gaussian and simple response, the Sun-induced
increment in any fixed background obeys

    |delta Q2| < 6 sqrt(G M_sun a0)/ell^2.

At 3 kpc its ceiling ratios are below 1.501e-8 canonical and 1.651e-8
alternate. More generally the **total phantom tidal field**, including the
background contribution, obeys

    |Q2_ph,total| < (92/15) a0/ell.

At 3 kpc this is below 0.001193 and 0.001442 of the frozen Cassini ceiling.
This avoids relying on numerically unresolved enormous-epsilon quadratures
or a uniform Galactic field across kiloparsecs. The proof uses |A|<=a0 and
an integrable third derivative of the Gaussian-smoothed Newton kernel.

[Incremental proof and exact arithmetic](universal_length/README.md) ·
[Total phantom bound and exact arithmetic](alternative/TOTAL_PHANTOM_BOUND.md)

These bounds address the inherited quadrupole-amplitude diagnostic with the
standard Green boundary condition. They do not replace an ephemeris fit or
bound the ordinary Newtonian background tide. Independent proof review
reconstructed the normalization and trace-free factors.

## The same law fails the next dwarf discriminator

The fresh source-plus-outer calculation gives **4/24 canonical and 5/24
alternate isolated dwarf passes**, versus **19/24** for plain isolated
QUMOND, retaining the old sample, Plummer baryons, mass-to-light interval
[1,3], and dispersion cuts. The outer operation is the correct vector
Gaussian convolution, not smoothing the radial force as a scalar.

Even at Upsilon=3, alternate predictions for Fornax, Sculptor and Leo I are
7.4014, 3.5629 and 5.4144 km/s, below respective frozen lower limits 9.9,
6.4 and 6.4. Prediction monotonicity in Upsilon extends these failures over
the full continuous interval. Selected numerical shifts are <=.001127 km/s.
An independent Gaussian-mixture implementation and kernel/grade audit agree.

This is the exact spherical **isolated** discriminator, not a new full
satellite external-field grade. No theorem that the external field always
lowers dispersion in this nonlocal model is assumed. The deficit is a
substantial liability; it prevents treating the two-check witness as broad
success. [Results](dwarfs/README.md) · [Independent review](dwarfs/REVIEW.md)

## Constitutive changes: no survivor among the tested models

The response search retains the common-epsilon mass-width convention and
varies nu in the same reciprocal energy. It screens 36 response instances
(including a duplicate simple-law control) in power, exponential-cutoff and
rational families. The cutoff has two added shape choices, t and p, in
addition to epsilon:

    nu(y)=1+[nu_simple(y)-1] exp[-(y/t)^p].

Fourteen selected, solar-screened model choices receive the full original
1,375-cell MW search: **19,250 cell-model states, zero four-cut passes**.
One small-width case needed a second full-population run at refinement 3,
lmax=192 to satisfy the unchanged source-tail gate: its conservative negative
mass bound fell from 1.478e-5 to 1.198e-6 (limit 1e-5). That adds 1,375
resolution evaluations, not a fifteenth physical model. Its maximum speed
is 217.52262 km/s and it still fails the necessary local-speed cut.
The last four each pass canonical Cassini at 0.98947--0.98996 of the ceiling.
All four fail alternate Cassini. Their MW failure is not inferred from the
solar result; it is calculated independently.

The closest production choice is t=1.587, p=6.3, epsilon=.24, cell 1359.
At refinement 4 it has K0=71.03264>70.8 and rotation chi-squared
63.17887>59.89250. It still fails after spatial/angular and filter-domain
refinement. Its local speed is 220.43788 km/s. This is a resolved finite
miss, not a theorem excluding every interpolation function or parameter.

The exact constitutive condition d[y nu]/dy>0 is independently proved for
p=6,t>=1.5 and p=6.3,t>=1.5815, using analytic tails and rational interval
certificates. Those proofs establish neither a fit nor full action health.

[Response formulas, solar runs and certificates](response/README.md) ·
[MW first portfolio](mw/constitutive_grid_001/results.json) ·
[Continuation](mw/constitutive_continuation_001/results.json) ·
[Shape boundaries](mw/constitutive_edges_001/results.json) ·
[Closest-case refinement](mw/edge_refine_001/results.json)

## Positive mixtures of reciprocal energies

For nonnegative weights summing to one, a sum of filtered phantom energies
is itself variational and preserves the asymptotic normalization. The
finite-support optimization over 15 widths and all baryon cells tests
141,625 simplex/Cassini vertices. Refined selected maximal speeds are
216.94979 canonical and 218.20963 alternate, below the necessary 219.9.

The complete stored-array optimization remains exploratory because it
combines historical resolutions and some unresolved narrow-width components.
Both selected maximizing pairs use clean broad components and were replayed
with the literal full potential. This is not an all-width mixture theorem.
[Derivation, supporting-line check and runs](alternative/README.md)

## Evidence status and continuation

The result is a completed phase of the broader research task, not a viable
final theory. Original data and accepted cuts remain unchanged. Manifest
validation checks execution and input freshness; it is not proof validation.
One failed coarse solar refinement and two contract-wording/count mistakes
are retained with explicit corrected replays, not silently rewritten:

- response/refine_001 fails its original accuracy gate; refine_002 passes at
  increased angular resolution with the same physical law and tolerance.
- The original fractional monotonicity contract retained p=6 in one
  conventions field. The independently reviewed corrected-contract replay is
  universal_length/fractional_review_001; see
  [clarification](response/PROVENANCE_CLARIFICATION.md).
- mw/constitutive_checks_001 retained a bounds count of 6 despite its
  assertion/code checking 10 models. constitutive_checks_002 reruns the
  unchanged literal controls under the correctly stated contract.
- The epsilon=.20, t=1.52, p=6 row of the original continuation is a numerical
  diagnostic, because its harmonic source-tail bound exceeded the declared
  limit. [The full higher-resolution recheck](mw/constitutive_low_recheck_001/results.json)
  passes that same gate and is the accepted evidence for this model.

KT35 preserves the separate Gaussian sign theorem and unsuccessful magnitude
closure attempt. No lower-epsilon interval exclusion is claimed there.

The next live route is **KT37 generalized action**, using Newton-field
curvature inside a scalar action and retaining its complete Hessian
variation. This addresses a different mechanism from either a common
Gaussian blur or changing only nu(g). A known construction is available in
[Milgrom 2023, equations 6, 14 and 16](https://arxiv.org/html/2305.01589v2).
Its applicability here is a new experiment, not a consequence of that paper
and not a novelty claim. The route has its own contract and disjoint runs.
