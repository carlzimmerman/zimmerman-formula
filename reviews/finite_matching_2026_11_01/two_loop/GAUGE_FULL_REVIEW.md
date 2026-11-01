# Independent review of coordinator gauge/full graph calculation

Reviewer: spectrum/vertex researcher, separate from the gauge author.
This is not a blind review: the shared action, complete-spectrum work and
reported SUSY/CS results were known. This reviewer read the actual source
formulas and raw implementation and ran a distinct basis/scaling control.

**Verdict: the complete finite two-loop vacuum implementation is supported
in the stated canonical rigid SU5, CP-background, Landau DR-bar-prime and
finite numerical scopes.** Pressure/current/physical completion claims
require their own matched action and numerical checks.

## Source and contraction checks

Checked Martin hep-ph/0111209v2, source conventions2.10–2.16 and all
prefactors/functions6.11–6.30, including DR-prime finite constants and
massless limits, against the primary version. `functions.py` agrees.
The ordinary MS vector functions cannot be substituted for these values.

The real scalar generator is independently reconstructed from delta z=iRz:
J=[[-ImR,-ReR],[ReR,-ImR]]. Its antisymmetry gives the scalar-vector
couplings. Differentiating the vector mass matrix gives
gVVS=-g^2(JaJb+JbJa)r; the VS quartic contraction is
2g^2 sum_k(Ja)_ki^2. These agree with `vertices.py`, including source
prefactors1/4. The sign of SSV/VVS is immaterial after squaring, but their
normalization is not.

Fermion currents transform as G= g U^dagger R_F U. The gaugino block is
the adjoint in the same normalization as A,B. In a positive diagonal
Takagi basis the source chirality-flip FFV contraction is
Re(G_IJ^2)mI mJ/2, not |G_IJ|^2. The implementation uses that expression.
The adjoint relation R_adj=-if produces sum f_abc^2=120 for SU5, matching
the implementation's group control. The pure-gauge function already
contains the vector/ghost classes; they are not added twice.

`full.py` divides the loop-stripped ten-class coefficient by(16pi^2)^2
and adds the already-loop-normalized heavy-relaxation term once. It adds
no separate RG-resummed logarithm. The one-loop normalization is consistent
with the same source convention.

## Numerical and CS evidence checked

The coordinator's three fully gauged f=0 supersymmetric points have
residuals3.3e-17..2.6e-16 relative to the absolute graph scale. All gauge
and model construction controls pass. The reduced two-loop CS checks
have relative errors3.0e-9..2.3e-8 at the three stated weak points.

The CS comparison correctly includes the heavy-normal relaxation scale
derivative. The diagrams alone do not satisfy the *reduced* CS equation.
The retained original X is a gauge singlet, so its scalar Landau anomalous
dimension agrees with its chiral anomalous dimension through the used
orders. Applying the chiral anomalous dimensions indiscriminately to the
unreduced charged-background potential would be wrong; Martin7.5–7.9
distinguishes those objects.

This reviewer additionally executed run_basis: all ten finite graphs are
unchanged under independent deterministic rotations within degenerate
scalar, Takagi and vector spaces, with maximum normalized change1.9e-16.
The all-graph e^4 scaling check is within2.8e-16, and an additional actual
ungauged full-SU5 supersymmetric calculation cancels to1.03e-16.

These orthogonal controls support mass-insertion phases, degeneracy
bookkeeping, field factors and graph normalization. They are not a proof
of uniform numerical error, all-parameter coverage, higher-loop convergence
or a physical halo verdict. The kinetic/current matching is not certified
by this vacuum-potential review. Exact reviewed input hashes and actual
manifest statuses are recorded separately in GAUGE_REVIEW_INPUTS.json.
