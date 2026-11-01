# Complete component vertices for finite two-loop vacuum graphs

The raw action is the unchanged canonical-K SU(5) singlet/two-adjoint
model. This route constructs every scalar and scalar-Weyl coupling needed
by SSS, SS, FFS and barFFS. The coordinator supplies the six vector graph
classes, and the master-integral worker independently supplies finite I,J.
Together these evaluate all ten Landau DR-bar-prime vacuum classes, rather
than another RG-only approximation.

## Real fields and mass bases

There are n=49 chiral coordinates and 24 gauginos. Write

    z=z0+E r, E=(I,iI)/sqrt(2), r=(q[49],p[49]).

Let Y_ijk=W_ijk, F_i=W_i, M_ij=W_ij. The chiral part of the scalar Hessian
uses A=M^dagger M and B_ij=conjugate(F_k)Y_kij. Its real blocks are
Re(A+B),-Im(A+B),Im(A-B),Re(A-B). Gauge D terms are included before
diagonalizing. The full symmetric fermion mass matrix contains both
W_ij and sqrt(2)g z^dagger R_a gauge/gaugino mixing. The scalar orthogonal
matrix O and vector matrix Ov have eigenvectors as columns.

The retained CP slice admits a particularly stable Takagi factorization.
The fixed diagonal phase P has entries -i for X and B, and 1 for A and
gauginos. Then P^T MF P is real symmetric. If V diagonalizes it to signed
real d, take U=P V diag(1 for d>=0, i for d<0). Consequently

    U^T MF U=diag(|d|), U^dagger U=I.

This avoids an arbitrary SVD phase choice inside degenerate singular
spaces. The chirality-flip graphs require these phases. A generic complex
background outside this realifiable slice is rejected explicitly; no
general Takagi claim is made.

All 98 Landau-gauge scalar coordinates, including massless Goldstones,
remain in the graph calculation. They are not quotiented from internal
propagators. Massless ghosts are already included in the coordinator's
pure-gauge kernel. The heavy-normal relaxation separately quotients gauge
directions when minimizing the reduced potential.

## Cubic and quartic scalar vertices

Use mass-basis Em=E O and define

    K_ia=M_ij Em_ja,
    B_iab=Y_ijk Em_ja Em_kb.

Expand each real D auxiliary as D_p=D0_p+L_pa r_a+S_pab r_a r_b/2.
Before the scalar rotation,

    L_pa=2g Re(E^dagger R_p z0)_a,
    S_pab=2g Re(E^dagger R_p E)_ab.

Rotate L,S with O, retaining their factors of g. Direct differentiation
of sum|F|^2+sum D^2/2 yields

    lambda_abc=2 Re sum_i[conj(K_ia)B_ibc+conj(K_ib)B_iac
                                            +conj(K_ic)B_iab]
                 +sum_p[L_pa S_pbc+L_pb S_pac+L_pc S_pab].

The SS class needs only lambda_iijj. It is computed without allocating
the 98^4 tensor:

    lambda_iijj=2 Re sum_k conj(B_kii)B_kjj
                 +4sum_k |B_kij|^2
                 +sum_p[S_pii S_pjj+2 S_pij^2].

These formulas include the scalar D interactions; omitting them would
not define the gauged microscopic theory. Independent original-polynomial
directional derivatives test the cubic, quartic and mixed-pair quartic
coefficients, including a direction that mixes the full real field space.

## All scalar-Weyl vertices

Differentiate the complete 73x73 symmetric fermion matrix with respect to
each real scalar, then transform both fermion indices with the Takagi U.
The chiral block is Y_ijk Em_ka. The mixed block is

    partial_a J_pi=sqrt(2)g conj(Em_ka)(R_p)_ki.

It is antiholomorphic in the background scalar, unlike the superpotential
block. The implementation retains this complex conjugation and the two
symmetric mixed blocks. Thus FFS/barFFS include gauginos as well as the
49 chiral fermions.

With positive diagonal Takagi masses mI, the ordered-index graph weights
are

    SSS: lambda_ijk^2/12,
    SS: lambda_iijj/8,
    FFS: |y_IJk|^2/2,
    barFFS: Re(y_IJk^2) mI mJ/2.

The last expression includes the source's complex-conjugate graph. It is
not |y|^2 and can carry either sign. All indices remain ordered; no second
symmetry-factor division is made after grouping degenerate masses.

The source kernels are fSSS=-I, fSS=J(x)J(y),
fFFS=J(x)J(y)-J(x)J(z)-J(y)J(z)+(x+y-z)I and fbarFFS=2I.
Only after summing loop-stripped graphs is the result divided by
(16pi^2)^2. SOURCE_RECORD.json pins exact source/version and locators.

## Grouping, controls and scaling

Massless eigenvalues are clipped only relative to the spectrum, not to a
fixed unit mass. The positive run uses zero threshold2e-11 times the
largest mass square and rejects negative values below -2e-10 times that
scale. Distinct positive masses are grouped with relative tolerance2e-8
per mass and a tiny spectrum-relative floor. At the weak reference point
there are 13 scalar groups and 9 fermion groups. This preserves the
distinct light chiral thresholds.

The verified builder passes ten controls. The one-field supersymmetric
Wess-Zumino origin independently fixes scalar/fermion graph weights:
SSS weight m^2y^2/2, SS weight y^2/2, FFS weight y^2/2 and zero total
barFFS weight. Together with the exact kernels these cancel.

A separate deterministic Givens rotation within all scalar, Takagi and
vector mass-degenerate spaces leaves each grouped nonvector weight and
all ten finite graph values invariant. The quartic diagonal contraction
is regenerated from the rotated underlying B,S tensors, rather than
rotating an insufficient old diagonal. This exercises the degeneracy
and mass-insertion bookkeeping directly.

At h=lambda=e,g=sqrt(29/200)e,f=1, X proportional to e^(-1/2) and Q^2
proportional to e, every mass square scales as e. Cubics scale as e^(3/2),
quartics and squared Yukawas as e^2, and every two-loop graph scales as
e^4. Direct e=.03 versus .01 tests check this for all ten graph classes.
Actual ungauged full-SU5 f=0,g=0 graph sums vanish independently of the
coordinator's gauged SUSY controls.

## Limits and interpretation

The common builder covers the stated CP valley and the declared finite
trial range. Numerical grouping and cancellation controls are not interval
certificates. The full finite potential remains gauge/scheme dependent
away from physical stationary observables. The graph coefficient is a
two-loop result for this specified rigid action, not an all-order theorem,
gravity matching, selected coupling or cosmological state.

The former missing finite vacuum-diagram function is now actually
calculated jointly with the coordinator's gauge classes. Kinetic/current
matching remains a separate obligation and cannot be supplied by this
potential alone. The pressure driver must use the complete graph sum and
count heavy-normal relaxation exactly once, without adding RG logarithms
already present in the explicit finite diagrams.
