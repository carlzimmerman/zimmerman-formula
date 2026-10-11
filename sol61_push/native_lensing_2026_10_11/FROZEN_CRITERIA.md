# Native lensing operator and concentration-loophole audit

2026-10-11. Base 812794f3f; current shared HEAD d5a227f0a. Commit this file
alone before code execution. No edits to Claude lanes or their frozen criteria.

This advances cluster closure by validating the proposed raw-image feasibility
test, not by declaring an observed pass/fail. Inputs already seen: CDS ReadMe,
first/full catalogue textual inspection, Rihtarsic+2026 v2 section 3 defining
G/S/B and feature IDs. Expected counts are published: 199 total, G=135, S=22,
B=42; gold has 49 source features in 27 galaxies. No numerical fit has run.

Parse fixed columns, retain G only for native constraints; system redshift is
zsys, not individual NIRSpec z. IDs before the final dot identify a source
feature. Removing its lowercase suffix identifies a galaxy, never a source
point. Require unique image IDs, legal classes, finite sky coordinates, known
positive redshifts >.296 for gold, identical zsys within every gold feature
and parent galaxy, >=2 gold images per feature, and the published counts.
Report discrepancies rather than silently modifying selection.

Coordinates: gnomonic sky tangent plane centred on the mean gold RA/Dec,
east/north in arcseconds. Verify inverse round-trip <1e-8 degrees.
For each feature form orthonormal Helmert contrasts H so H*1=0 and H*H^T=I.
Build both observed position contrasts and source-eliminated deflection
constraints. Expected scalar count 2*(135-49)=172, an algebraic dimension,
not a count of statistically independent data with known covariance.

Analytic question: without a density/regularity bound, can positive compact
lens mass approach zero while meeting any finite set of point deflections?
For N distinct image positions and finite target vectors d, place four positive
point masses at cardinal offsets epsilon around each image. Parameterize their
weights as epsilon*(B+v_x)/2, epsilon*(B-v_x)/2, and analogously y, in units
where the deflection coefficient is one. Choose B=2*max(abs(d))+1 once;
solve the exact linear cross-talk system for v. Total mass is 2*N*epsilon*B.
This is an adversarial mathematical relaxation, not an allowed cold-energy
model, action, species, or tuning prescription.

Synthetic controls: two-image point lens; symmetric Jacobian of the mass
deflection; Helmert projection equals subtracting per-feature means; mass
sheet degeneracy on a single source distance; wrong-deflection sign, wrong
source efficiency, and merging distinct features must be detected (MUTATE).
Controls compare errors to 1e-10 for dimensionless exact identities, except
finite-difference Jacobian tolerance 1e-6. Parser mutations: duplicate ID,
inconsistent zsys, missing gold zsys, or wrong quality must be rejected.

For the adversarial finite check use all 135 gold positions, scaled by the
minimum pair separation. Set each source-feature position to its image mean;
target d=theta-mean (unit source efficiency, no physical cosmology inference).
Use epsilon/minimum separation = 1e-3,1e-4,1e-5,1e-6. Report conditioning,
minimum weight and max relative residual. A cell is successful only if all
weights positive and residual <=1e-6 relative to max(1,maxabs(d)). No dropping
failed cells. Analytic proof, not finite points alone, must justify any
arbitrarily-small-mass assertion. Failure means investigate conditioning or
construction; it is not a candidate-B verdict. No astrophysical mass inferred.

Use numpy, one numerical thread; matrices <1000 by 1000; <200 MB expected
working storage, wall cap 90 seconds, CPU cap 60 seconds. No PM simulation.
Save code/input hashes, controls and results with a validated manifest.
Do not edit kernel, kappa, supply constants, sealed predictions or other lanes.
