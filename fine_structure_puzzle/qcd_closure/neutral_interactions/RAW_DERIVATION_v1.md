# First interacting closed neutral vacuum diagram

FSP-005, coordinator raw derivation. Saved before executing a new finite
check or looking for a published two-loop result. The parent closed scalar
action/determinant was read. Its old microscopic coupling dictionary has
already been qualified by FSP-004; this calculation uses independently
matched effective parameters, not that old dictionary or measured alpha.

## Action, regime and the complete diagram at this order

Use a stable branch of the compact dual photon on S3_R at fixed small
circle L. With canonical field varphi=sqrt(kappa) phi,

    S=integral [ (grad varphi)^2/2-u cos(varphi/sqrt(kappa)) ],
    m^2=u/kappa>0,
    U=-u+m^2 varphi^2/2+lambda varphi^4/24+...,
    lambda=-m^2/kappa.

Assume mR>1 and m/kappa small. Hold L, local curvature couplings and the
declared matched parameters fixed when varying R. Choose the parent's
minimal scalar operator, with no added xi R3 varphi^2 term, and its common
zeta/finite-part tadpole subtraction. Unspecified hard metric terms remain
outside the computed soft contribution. These choices define a conditional
EFT benchmark; they do not fix physical curved Yang--Mills matching.

W=-log Z. There is no cubic vertex at the minimum. A single quartic vertex
with its three Wick contractions is the only interaction vacuum diagram
at two-loop order. The sextic one-vertex diagram and two-quartic-vertex
connected diagrams begin at three loops. Therefore

    W_2=(lambda/8) V G_R^2,
    V=2pi^2 R^3,

plus the matching counterterm insertions required by the chosen parameter
path. All modes, including the compact field's constant Gaussian mode,
are included in G_R. The finite compact-cell multiplicity has zero stress.

## Exact coincident propagator in the declared scheme

Let a=sqrt(m^2 R^2-1) and q=a/R. The parent's exact mode sum gives

    G_R=R^2/V FP sum_(n>=1) n^2/(n^2+a^2)
       =-a coth(pi a)/(4pi R)=-q coth(pi a)/(4pi),
    G_infinity=-m/(4pi).

Its negative finite part is not a negative bare covariance: the positive
short-distance divergence was subtracted by the common local prescription.
The parent determinant obeys partial_(m^2) W_1=V G_R/2, which independently
fixes this tadpole normalization. Reusing a different subtraction for the
quartic contraction without its compensating matched mass is not allowed.

The isolated constant-mode contraction is

    G_const=1/(V m^2),
    W_2,const= -1/(8uV).

This matches the first interaction term in -log I0(uV) with the canonical
constant-mode measure. It is only one term of G_R^2, not an extra term to
append to the full diagram. The mixed constant/nonconstant contractions
and the nonconstant square are required at the same order.

## Path A: fixed Lagrangian m,kappa in the chosen finite-part scheme

Subtract the flat extensive density at the same m and lambda:

    Delta f_2^A=(lambda/(128pi^2))
                   [(m^2-R^-2)coth^2(pi a)-m^2].

Here f_2=W_2/V is a three-dimensional effective-action density. It is not
the spatial stress. For large mR, coth(pi a)=1+exponentially small terms,
so this expression has exactly one algebraic curvature power at this order:

    Delta f_2^A=-lambda/(128pi^2 R^2)+exponentially small,
    Delta tau_s,2^A=-lambda/(384pi^2 L R^2)+exponentially small
                   =m^2/(384pi^2 kappa L R^2)+exponentially small.

The stress convention is tau_s=(1/L)partial_V W, or
tau_s=(1/L)[f+(R/3)partial_R f]. At fixed Lagrangian coefficients the
exact expression is

    Delta tau_s,2^A=lambda/(128pi^2 L) *
      [(m^2-1/(3R^2))coth^2(pi a)-m^2
       -(2pi/3)a m^2 coth(pi a)csch^2(pi a)].

No 1/R term occurs in this complete two-loop soft contribution. This
statement is about the explicit diagram, not an assumption from a mass gap.

## Path B: fixed flat-space pole mass M and kappa

At the relevant order the flat scalar self energy is momentum independent:
Sigma_flat=(lambda/2)G_infinity. Retune the Lagrangian mass as

    m_lag^2=M^2+delta m^2,
    delta m^2=-(lambda/2)G_infinity(M).

The Gaussian determinant then adds the counterterm
(delta m^2/2)V G_R. Tree-vacuum shifts are extensive and cancel under the
same flat subtraction. Replacing lambda by -M^2/kappa is sufficient to
this order; changes in lambda from retuning are higher order. No independent
curved mass counterterm is imposed by this flat-pole condition.

The flat-subtracted complete two-loop soft density, expressed at fixed M,
is consequently

    Delta f_2^B=(lambda/8)(G_R(M)-G_infinity(M))^2
              =lambda/(128pi^2)[q coth(pi a)-M]^2,
    a=sqrt(M^2 R^2-1), q=a/R.

Thus the R^-2 term in Path A is removed by the mass matching, rather than
silently transported to a different comparison path. The leading terms are

    Delta f_2^B=lambda/(512pi^2 M^2 R^4)+O(R^-6)+exponential,
    Delta tau_s,2^B=-lambda/(1536pi^2 M^2 L R^4)+O(R^-6)+exponential
                   =1/(1536pi^2 kappa L R^4)+O(R^-6)+exponential.

For an exact stress define X=q coth(pi a)-M. Then

    D_R[q coth(pi a)]=coth(pi a)/(qR^2)-pi M^2 R csch^2(pi a),
    Delta tau_s,2^B=lambda/(128pi^2 L)
           [X^2+(2/3)X D_R(q coth(pi a))].

This is the flat tadpole mass subtraction, equivalent at this order to
normal ordering the quartic vertex at the flat massive covariance. It is
not a prescription to normalize away the complete metric functional.
Adding allowed independently matched curvature operators or hard gravity
terms changes the even-curvature coefficients; neither path predicts those
unknown coefficients. Both paths give zero inverse-radius coefficient for
this explicitly computed soft diagram.

## Quantified remaining gap

The calculation closes the first interacting diagram omitted by the parent
Gaussian result and includes its constant mode exactly once. It does not
control all loops, compact domain walls, hard monopole-core matching,
global microscopic gauge-to-dual normalization, physical QCD matter or
electromagnetic alpha. A genuine H or 1/R term would have to arise outside
the even-power and exponentially small structures calculated here. The
different geometry/state and fixed small L still require a physical bridge.

Planned finite checks: exact Wick and parameter-retuning algebra; propagator
versus independently differentiated determinant; both metric derivatives;
large-radius coefficients; numerical finite-radius spectral subtraction and
positive heat-kernel representation. A script passing those checks will
support only the declared finite identities; the loop-counting and matching
derivations above remain separate analytic evidence.
