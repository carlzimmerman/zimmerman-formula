# IC11: matter-coupled auxiliary response and a balanced local repair

Base `347950889570a839af41f6bef0c8bcba7531d02a`. Full theory **OPEN**.
This extends the pressure proposal, not the separately tested transition
completion. All numerical values use m=h0=1 and the unchanged IC10 constants.

## Same action, ordinary physical-metric matter

Let P0(X,w) be the explicit IC10 pressure and f(X)=5(2X)^16/64 from
[IC11_CLOCK_PRESSURE](IC11_CLOCK_PRESSURE.md). On eta=1 the proposed action is

    integral sqrt(-gtilde)[mstar Rtilde/2 + P0+f-b(P0_w)^2/2]
       + Sm[exp(2w)gtilde,psi],       mstar=exp(-1/6).

For the diagnostic Sm=-integral sqrt(-g) g^(mu nu)psi_mu psi_nu/2,
put Y=-gtilde^(mu nu)psi_mu psi_nu/2. Its contribution is exactly exp(2w)Y.
The total pressure L, not the vacuum pressure, must satisfy L_w=0.
X=exp(-2S)/2, and the stated chart is S>0, -S/2<w<0.

The phase-action lift of the correction is

    H_new-H10 = -eta exp(-4w)[f(exp(2w)Xphysical)-b(S,w)(P0_w)^2/2].

It is an explicitly specified local function on the regular active chart
below. At p=0, eta=0 on a neighborhood and the correction is defined to be
zero there, preserving all first static variations where the original chart
is regular. A globally regular extension through denominator zeros and the
activation transition is NOT provided by this construction.

No ordinary matter coupling is changed in physical variables. A diffeomorphism
variation of Sm gives, after integration by parts,
`nabla_mu T_m^(mu nu)=E_psi grad^nu psi`; the ordinary matter equation E_psi=0
therefore gives separate physical-metric conservation. This identity is not
a derivation of the PPN parameters, the measured G or lensing.

## Actual two-scalar principal matrices

For aligned homogeneous timelike currents, v=(sqrt(2X),sqrt(2Y)), define

    M=L_vv, q=L_vw, B=L_ww,
    K=M-q q^T/B,          D=diag(L_X,L_Y).

The script differentiates L, solves L_w=0, and computes eigenvalues of K
and the generalized pair (D,K). It independently checks K against numerical
velocity-coordinate derivatives. Positive K and D exclude a ghost/negative
gradient in this restricted principal problem; K-D positive semidefinite
puts both cones on or inside the physical null cone. These are not all-matter,
arbitrary-gradient or strong-coupling theorems.

For pressure alone (b=0), B=P0_ww>0 at the tested roots, while
`K_22=D_22-8Y exp(4w)/B<D_22` for Y>0. Consequently a positive K has a
superluminal generalized Rayleigh quotient in the matter direction.
Simply flipping B with a constant b=.01 does not fix the mixed cone: the
off-diagonal response must also be controlled. Both trials are retained as
negative controls, not reported as successful completions.

## Balanced curvature lemma: a constructive local improvement

At a vacuum stationary root P0_w=0, set

    A=(P0+f)_XX at fixed w, B=P0_ww, C=P0_Xw,
    R=A-C²/B=P_eff,XX,
    b(S,w)=1/(2B)+A/(2C²).

This is an explicit coefficient on B C != 0. Derivatives are taken before
substituting the root. The action is well-defined locally at the sampled
roots, not claimed globally regular. First derivatives of the added square
vanish at P0_w=0. Its second derivatives give exactly

    A_new=A-b C²=R/2,
    B_new=B-b B²=-B² R/(2C²),
    C_new=C(1-bB),
    A_new-C_new²/B_new=R.

Thus the vacuum pressure and eliminated clock kinetic coefficient remain
unchanged, while R>0 gives raw A_new>0 and B_new<0. For L=P(X,w)+exp(2w)Y,
the eliminated (X,Y) Hessian has determinant

    det(L_eff,IJ)=-4 exp(4w) P_XX/L_ww.

With P_XX>0 and L_ww<0 both its eigenvalues are positive. Together with
positive first gradients, continuity gives a small regular matter
neighborhood with subluminal coupled cones. The coefficient's derivatives
away from P0_w=0 are retained in the code, not frozen at vacuum values.

The four S=.03,.05,.1,.2 samples at Y=.0001 satisfy the actual eta=1
predicate and pass this coupled cone test. For example S=.1 gives squared
speeds approximately .226489685 and .999987672. These are finite checks
of the local improvement, not a certification at arbitrary matter density.

## The next matter limit: a fold, not automatically Dirac-rank loss

Larger Y cannot simply be declared healthy. Solving L_w=L_ww=0 at S=.1 gives

    w=-.0335823191256655382612570973820,
    Y=.000875852783922271225125849653.

The velocity-space auxiliary elimination folds there. Independent 70-digit
evaluation reproduced both equations. Crucially, canonical preservation
uses a different derivative:

    Acan=L_ww-q^T M^-1 q,
    {p_w,C_w}=Acan,       C_w=H_w=-L_w,
    H_reduced,pp=M^-1+M^-1 q q^T M^-1/Acan.

At the fold, `Acan=-.00656273355945958894`, so the actual 2x2 auxiliary
Poisson block has computed rank two, not zero. H_reduced,pp remains finite
but has one zero eigenvalue. A velocity-root fold is therefore NOT itself
a new propagating auxiliary or a lost canonical constraint. It leaves a
zero-speed/degenerate characteristic limit requiring analysis. On a nearby
side with L_ww>0 and Acan<0, `det K=det(M) Acan/L_ww<0`; not every local
continuation is healthy. Root-solver failures in the report mean unresolved
roots, not proof that every real branch is absent.

## Evidence, attribution and next work

[ic11_matter_gate.py](ic11_matter_gate.py) and its eight tests implement the
equations above. Tests progressed through missing-feature failures, then
actual derivative/root/rank checks. The initially attempted Y=.01 was not
silently declared passing: failure investigation located the fold above;
the successful cone claim is explicitly limited to weak matter samples.

Independent reviewer `matter_fold_audit` rederived the principal matrices,
balanced-curvature identity, fixed-momentum bracket, and fold. This is
independent algebra/code evaluation, not a formal proof assistant certificate.
No literature-wide novelty claim is made. Carl's separate motivating
paddle/wake suggestion is credited in
[CARL_CLOCK_MEMORY_INSIGHT](CARL_CLOCK_MEMORY_INSIGHT.md).

Next: continue in canonical variables through the fold, locate genuine
rank/characteristic degeneracies, and construct a pressure/auxiliary geometry
regular over the matter range required by the empirical source profiles.
The pressure-modified activation transition must also be varied independently;
the older IC10 transition numbers cannot certify this action.
