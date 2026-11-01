# TP01 spectrum and pressure contract

Frozen before any numerical spectrum execution, 2026-11-01.

Target: the rigid, canonical-K collective SU(5) model specified in
`microscopic_vacuum_2026_10_28/INVERTED_HIERARCHY.md`, with
W=fX+(h/2)X Tr A^2+(lambda/2)Tr A^2 B and its actual stated classical valley.
Construct all 49 chiral, 24 gauge and 73 total Weyl-field mass matrices,
including D Hessian and gaugino mixing. Test the valley before trusting it.
Adjoint component basis has Tr(Ta Tb)=delta_ab; gauge generators are Ta/sqrt(2).
Use the supersymmetric DR-bar one-loop supertrace, with all spin constants
3/2 and physical spin multiplicities 1,-2,3; massless gauge modes contribute
zero to the potential, not an extra massive-vector degree of freedom.

Initial diagnostic: f=1, h=lambda=0.6, g=sqrt(29/200)*lambda,
X in {0,0.1,1,3,10}. Compare F/D stationarity and Vtree to the printed valley,
Goldstone Hessian null directions, massless Goldstino, vector multiplicities,
and STr M^2. Derive independent vector masses and explicit-generator group
contractions. If the stated valley is not stationary, or has a physical
tachyon, that is an adverse mathematical result; do not alter the action or
silently substitute another branch. Pursue exact subsector diagnosis.

If this succeeds, enumerate all h,lambda in {0.3,0.6,1} at the same critical
g/lambda and scan X/sqrt(f) over a fixed logarithmic grid 10^-2..10^2 (81
points). Report physical negative scalar eigenvalues as instabilities, not
absolute-valued stable masses. CW with a negative mass is not a real stable
potential. Retain complete clustered spectra at X={0.1,1,10}; tolerance
scale-aware 1e-9 for null/eigenvalue sign diagnostics, and 1e-8 for algebraic
matrix controls. Finite log derivatives use h_s=0.005 and an independent
half-step; no pressure sign certified if derivative convergence fails.

Matter check is conditional on the old trial portal Z=exp(2s), s=ln(X/v).
For any accepted real potential calculate total P=U_s/3-U and the necessary
positive-source, stable-branch condition U_ss>3U_s. No microscopic portal,
Kahler corrections, gravity matching, UV boundary data or state are invented.
Inspect supertrace cancellations to distinguish a full renormalizable
microscopic threshold calculation from an isolated scalar-loop exp(6s)
counterterm. No universal all-field quantum protection is inferred from a
finite field scan.

Limits: one numerical thread, 1 GB address-space target, at most 180 seconds
per bounded run, fresh version-2 runner manifest. Preserve failed runs. All
writes stay in this directory. No git mutations, installs or downloads.
