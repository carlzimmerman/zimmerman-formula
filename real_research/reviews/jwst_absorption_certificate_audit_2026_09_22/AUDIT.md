# Absorption prerequisite review

Original candidate2f5e9e972d3c4102b198721f015426a8 is a useful finite calibration.
Its unchanged source was independently replayed in main, positive and negative
modes using the prescribed inputs and seeds. All12 audit checks pass and the
manifest validates. Main mean z=.2316,-.3726 and escape z=.9865,.7928;
positive mean z=-.0843,.6622 and escape z=.3700,-1.8112; half-alpha negative
escape z=31.4674,54.4180. The constituent transport functions had already passed
an independent-seed audit; this replay verifies the new Qwen certificate.

Scope: tau0=1,alpha=.1,.5, central unit scalar Thomson cloud, selected escaping
D=T-Z. This is not a universal solver proof, physical observation or novelty.
The candidate's phrase 'significance level alpha=.1' is incorrect: alpha here
is absorption rate, not the significance level of a5SE diagnostic. The
referee's claim that all positive z-scores are below1 is also inaccurate.

0ddaf5165c6f4ebea1f05584df5c83cf does not implement ray tracing: its reference
is arbitrary2.5R, its simulated sample is Gaussian noise centered on that
reference, and its source is changed from central to distributed. Reject.
9772a088 uses a changed negative alpha10 with zero escaping photons, then
fills the undefined conditional mean with0. 8c6ef90 changes the prescribed
negative toalpha/100 after earlier checks fail. Preserve the valid original
half-alpha conjunctive certificate; neither modification is needed.

Referee80573661 calls comparing independent estimators circular and a fixed
5SE diagnostic tautological. Those criticisms are wrong at the claimed finite
calibration scope. Agreement can fail (and did fail in earlier broken codes).
It still does not validate an astronomical interpretation. A one-SE criterion
would also reject sound noisy simulations frequently; it is not proof of flaw.

Path attemptf3d79ead has actual transport bugs: radial1-r exit distance,
local-rate flights in a varying medium, isotropic rather than Thomson mu,
nonorthogonal transverse rotation, incorrect occupation integrals, overwritten
profile checks and an inverted negative predicate. cc604699 replaces the
process by Brownian motion. Neither challenges the cap theorem. The v10
supplement supplies segment formulas whose derivatives and zero-length
values were checked exactly in SymPy (segment_check.json). This kinematic
check does not replace the pending path simulation.

Next work is an explicitly unproved extension: whether conditional escaped
mean and variance still satisfy the conservative cap inequality underalpha=.5,2,4.
Qwen must report the cap margin and its correlated-moment uncertainty, using
independent killed and weighted conservative transport. The original theorem
assumes no absorption. Any selected-sample violation would concern the extension,
not refute that theorem. No new novelty claim survived this review.
