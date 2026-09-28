# FGF-015: numerical slab checkpoint accepted within its boundary class

Coordinator read the raw derivation and verified all required fields, actual
source/artifact hashes and numeric_001 manifest. Result SHA256:
`d6d44466be4552b9332a093934868a0a2c87a9ad40af4cec818328fd4d6c6440`.

The variational forms use the actual varying hydrostatic density and
constitutive coefficient. Their assembled squares preserve the previously
audited sign theorem; comparison to the original density-potential form and
independently integrated Rayleigh quotients checks that the implementation
has not substituted a different operator. Accept the finite result: 120
returned eigenvalues in 12 Q/R, grid and inertia cells are positive, with
finest-grid changes <=0.29992%. Dimensionless frequencies and dimensional
restoration retain their declared toy parameters.

The nonzero wall-flux samples correctly distinguish fixed potential from
fixed flux. The wrong-background control prevents applying the hydrostatic
factorization to the separately supported/subtracted periodic model. No
additional sign-grid sweep is needed for these same premises.

No metric, filtered-MONO, free-boundary, three-dimensional, nonlinear or
observational stability result is accepted here. A physical background and
boundary selection or the operative action's own quadratic form are the
remaining implications. Actual runner HEAD and scientific ancestry are
separate because other work changed the shared checkout; input hashes stayed
fixed. This review does not claim a new coordinator reproduction of the
eigensolver beyond the recorded independent controls and algebra inspection.
