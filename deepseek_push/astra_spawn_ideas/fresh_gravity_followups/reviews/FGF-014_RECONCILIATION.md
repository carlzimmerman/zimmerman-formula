# FGF-014 independent root reconciliation

2026-09-30. Reviewed result SHA256
`ed32191c7e0a3169c3218ef69ad3b43464f40306c802a1abd6176491d444ffff`.
All ten declared input and ten artifact hashes match. Root derived the
Schur complement independently before reading the worker's final derivation.
The 288 cells / 2592 spectra are finite implementation controls, not the proof.

Let nu=4piG rho0>0, d=q² cos²theta, y=k²>0. Reorder the printed stiffness
as fluid, potential, scale. Eliminating the positive scale diagonal gives
potential stiffness y[Lambda-d/(Jy+m)]. Eliminating this positive diagonal
then gives fluid stiffness cs² y -nu/[Lambda-d/(Jy+m)]. Thus its sign,
and only its sign, determines whether there is one negative eigenvalue.
Positive diagonal kinetic mass preserves this inertia and real squared
frequencies by symmetric congruence. The directional condition follows from
m>q²/lambda since Lambda>=lambda cos²theta. The threshold function
h(y)=cs² y[Lambda-d/(Jy+m)] satisfies
h'(y)=cs²[Lambda-d*m/(Jy+m)²]>0; it runs from zero to infinity.
This independently proves a unique threshold, one negative branch below,
none above, and a marginal zero branch at equality. It also confirms the
quadratic cs² Lambda J y²+[cs²(Lambda m-d)-nu J]y-nu m=0.

Direct determinant expansion yields
det(H-xM)=-[(Dphi Dchi-q² k_parallel²)(x-cs²k²)+nu k² Dchi].
Equivalently the worker's
Eq. (1) vanishes. Setting q=0 or nu=0 gives its stated factors. Eliminating
the potential before taking tau=0 yields its 2x2 constrained matrix, including
the positive off-diagonal q cos(theta) sqrt(nu)/Lambda. H/k² tends to a
positive diagonal matrix, which establishes short-wave positivity at fixed
strictly positive coefficients. No rate bound uniform in singular limits follows.

A phase-sign typo was noticed in an intermediate read: xi=-i u would require
a negative potential/fluid entry. The final xi=+i u matches the printed positive
entry. The worker corrected this BEFORE execution; the corrected derivation
SHA256 de002f57e6ae4b20ef9a0a0879991b4657ccbe487537ee56b8d02f6bbab85a25
is pinned by the valid run manifest. No post-run history was rewritten.

Accepted only as a conditional theorem on the supported/subtracted local
Q/R diagnostic extension with responsive scale. Positive kinetics is a
premise, not a derived physical theory. The conserved quadratic energy does
not authenticate the external reservoirs. Constant-vacuum reference versus
dynamic effective scale remains an explicit unresolved interpretation.
Both a0 normalizations and frozen H comparison snapshots are restored;
no evolving cosmology, registered M action, filtered-MONO transfer, physical
metric, photon coupling or empirical closure is proved.

Next: derive the full quadratic form and boundary terms on a genuinely
balanced finite scale-plus-fluid slab; a frozen scale theorem cannot transfer
without the new field and density-gradient terms.
