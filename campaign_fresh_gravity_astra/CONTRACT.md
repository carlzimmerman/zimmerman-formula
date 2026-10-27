# Fresh gravity campaign — checkpoint AFG-001

Owner: this Astra chat. Start: 2026-09-27. Base Git revision:
`6b7ab82438dfd55c91d3a1efd1745857c4f3dd45` (shared checkout already dirty).
Write scope: `campaign_fresh_gravity_astra/` only. The concurrently populated
`campaign_fresh_gravity/` belongs to a separate lane and is not modified here.

## User objective and evidence standard

Derive new chains directly from Zimmerman's core assumptions, with scaling MOND
in every acceleration, discrepancy and prediction. Work from equations and
cached measurements, not imported theoretical mechanisms. Find a common physical
account of the evidence, or an explicit, independently testable measurement
explanation. Agreement manufactured by an independent correction for every
object does not meet this target. A complete answer needs common dynamics,
lensing, cosmology, conservation, stability and instrument likelihoods; none is
assumed solved by a successful local relation.

No new literature search or theoretical synthesis is used. Existing observations
are allowed as evidence. Cached reductions retain their original modelling
assumptions; they are not raw photons. Independent derivation here does not
establish historical novelty. Existing framework equations are credited to the
repository and are not claimed as new discoveries.

## Frozen framework and branch distinctions

Use the latest `STANDING.md` rather than superseded June claims:
`a0 = kappa c sqrt(G rho_Lambda)`, with kappa adopted, not derived. At low
redshift use both registered normalizations 9.3619e-11 and 1.1279e-10 m/s².
The pressure-law reading is `a0² = kappa² G (-p)` with pressure in energy/volume;
for vacuum p = -rho_Lambda c² these agree. A non-vacuum density law is not
automatically the pressure law. The primary numerical branch holds a0 constant
for vacuum. Separately test `a0(z)/a0(0) = E(z)` with illustrative
E² = 0.315(1+z)³ + 0.685, not a newly fitted cosmology.

Keep three static relations separate, B = g_bar > 0:

* Q: F(B) = sqrt(B² + a0 B), the core algebraic a0-line.
* R: F(B) = B/[1-exp(-sqrt(B/a0))], the repository RAR relation.
* M: F(B) = B + a0 h_mono(B/a0), the latest monotone-phantom static branch
  defined in L340. Its interpolation definition is inherited explicitly.

All share the isolated deep limit F(B) ~ sqrt(a0 B). They are not equivalent.
M here is the unfiltered radial law, not the complete filtered field theory.
Spherical mass conversions are used only for spherical cluster reductions.
Disk points are acceleration comparisons, not enclosed-mass estimates.

## Initial executable routes

1. **Moment closure from the algebraic core.** Derive how averaging affects the
   equation, then derive a line-moment estimator under an explicit beam and
   line-spread model. First uncertainty: whether the moments identify a0 when
   intrinsic broadening is unknown. Check exact mixtures, then deliberately
   miscalibrated broadening. Success is a conditional invariant and a measurable
   failure condition, not a claim that current data already measure it.
2. **Inverse source budget.** Invert Q/R/M on cached SPARC accelerations and
   X-COP hydrostatic profiles. Never reuse a Newtonian missing mass as a MOND
   requirement. First uncertainty: whether the residual can be eliminated by
   changing only the registered normalization or cosmic scaling. Record required
   baryonic-source and force factors, and compare matched accelerations.
3. **Coarse structure versus cosmic evolution.** Derive the deep-limit response
   of a positive unresolved acceleration distribution. Compute the heterogeneity
   needed to disguise H(z) scaling as constant a0, and the associated spectral
   prediction. Distinguish a beam average from physical homogenization.

## Computational contract

Binary64 numerics plus symbolic differentiation; deterministic inputs, no random
sampling. SPARC selection: Q <= 2, inclination >= 30 degrees, positive radius,
observed velocity, velocity error and net baryonic acceleration. Stellar
mass-to-light factors 0.5 disk, 0.7 bulge are fixed conventions, not fitted.
Signed gas contributions are preserved. Report point-weighted and
galaxy-weighted summaries without a chi-square/significance claim.

X-COP: only clusters with their own stellar profile; all three radial supports
must include the evaluation radius, and no extrapolation. Convert each radius
with its own FITS units/header. Read central M_FORW and MGAS/MSTAR columns directly.
Mass units and radius alignment must be inspected before the run. No imputed
stars, cosmic baryon-fraction prior or new dark-halo fit.

Checks: inverse/forward recovery, limiting laws, exact moment identities,
independent quadrature of broadened profiles, deliberately wrong broadening,
FITS radius alignment against the shared NFW column solely as a unit check,
finite-difference curvature against symbolic expressions. Cache input hashes,
software versions, executed command, output hashes, ranges and exclusions.

No finite grid proves a universal theorem. No cached-profile RMS is a likelihood.
No synthetic line is observational evidence. Failed checks block the associated
claim; a nonzero empirical residual is retained, not renamed a detection.
