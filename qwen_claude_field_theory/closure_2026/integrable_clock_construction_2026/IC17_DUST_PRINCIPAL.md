# IC17 same-action dust principal symbol: aligned success, relative-flow failure

**Full theory OPEN. Matter cone fails at a tested relative-flow principal
point admitting a regular local ADM constraint patch.** The constructive
aligned result below must not be promoted to a complete matter-cone
certificate. No global initial-data or time-evolution solution is claimed.

## Exact covariant elimination, after variation

Use the actual IC17 plateau pressure P17(X,w), with its fixed positive pole
coefficient epsilon=10^-5, and minimally couple physical irrotational dust:

    S_dust = integral sqrt(−g) lambda_g (Y_g − 1/2),
    Y_g = −g^{mu nu} theta_mu theta_nu/2.

For g=z g_tilde, z=exp(2w), set lambda=z lambda_g and
Y=−g_tilde^{mu nu} theta_mu theta_nu/2. The barred matter Lagrangian is

    L = P17(X,w) + lambda (Y − z/2).

First varying lambda and w gives z=2Y and lambda=P_w/z. Only *after* these
equations are imposed may the dust term be set to zero. Exact local algebraic
elimination on Y>0 gives

    L_eff(X,Y) = P17(X, (1/2) log(2Y)).

This is the same action, not an added dust sound-speed ansatz. Its two coupled
scalar modes include the irrotational dust perturbation. The dust source is
positive when lambda>0, equivalently lambda_g>0. Their interaction-induced
characteristic speeds need not equal a separately imposed dust sound speed.

## Actual new backgrounds and aligned two-field characteristics

All numerical points use `ic17_baryon_background.state(S,k=.2)`, whose actual
auxiliary root satisfies P_w=b exp(w), with conserved dust-to-clock charge
ratio k. They are not vacuum roots reused with a spectator density. Put
S=−(1/2)log(2X), Y=exp(2w)/2, B=P_ww, C=P_Sw.

On a comoving homogeneous state the exact velocity Hessian and spatial matrix are

    K = [[(P_SS+P_S)/(2X), −C/(2 sqrt(XY))],
         [−C/(2 sqrt(XY)), (B−P_w)/(2Y)]],
    D = diag(−P_S/(2X), P_w/(2Y)).

The code differentiates an arbitrary second-order Taylor jet of P with
respect to the two *raw velocities*, substituting S=−log(T_dot), w=log(theta_dot),
and compares every entry with this K. First and second derivatives of the
covariant reduced pressure are checked independently. A direct numerical
velocity-Hessian check also uses the complete IC17 constitutive evaluator.

K>0 and K−D>0 are tested by their actual leading principal minors. Signed
generalized eigenvalues of D against K give both squared sound speeds; no
absolute value is taken. At S=.1 they are approximately
.00015738275 and .22114548031. Across 51 logarithmically spaced S values from
10^-8 to .1 at 70 digits, all aligned points pass. The smallest c² is
4.1508414966e−10 and largest .22114548030578. The minimum determinants of K
and K−D are respectively 20347.3913573 and 15845.1635747. These are finite
samples, not an interval theorem. The physical and barred null cones coincide
under the positive conformal factor z.

## Actual auxiliary canonical Schur matrix

For q=(w,lambda), the fixed-velocity matrices of the uneliminated L are

    L_vv = diag((P_SS+P_S)/(2X), lambda),
    L_qq = [[B−2lambda z, −z], [−z, 0]],
    L_qv = [[−C/sqrt(2X), 0], [0, sqrt(2Y)]].

Their explicit Schur complement A=L_qq−L_qv L_vv^−1 L_vq, evaluated on
2Y=z and lambda z=P_w, is

    A = [[B−2P_w−C²/(P_SS+P_S), −z], [−z, −z/lambda]],
    det(A) = −(z/lambda) [B−P_w−C²/(P_SS+P_S)].

Both the matrix and determinant are derived from the raw Hessians in SymPy,
not assigned as expected ranks. The primary constraints p_w=p_lambda=0
and the two auxiliary secondary constraints have homogeneous bracket matrix
[[0,−A],[A,0]] with a consistent secondary-sign convention. The secondary–
secondary bracket vanishes in this homogeneous shift-symmetric sector.
Singular values are computed at each point with rank threshold 10^-45;
all 51 computed ranks are four. Invertibility closes the auxiliary multiplier
equations locally in this sector. It does not establish the full spatial
Dirac algebra, the transition constraint rank, or a global degree-of-freedom
count on arbitrary backgrounds. An indefinite auxiliary A is not itself a
physical kinetic ghost; the physical velocity matrix is K above.

## Decisive negative control: dust moving relative to the clock

Hold X,Y and the constitutive point S=.1,k=.2 fixed. In the local clock-rest
frame, give the dust relative speed v=.1 along the wave direction while
preserving its invariant Y. Define

    P_X = −P_S/(2X),       P_Y = P_w/(2Y),
    P_XX = (P_SS+2P_S)/(4X²),
    P_XY = −C/(4XY),       P_YY = (B−2P_w)/(4Y²),
    d = (sqrt(2X)c, sqrt(2Y/(1−v²))(c−v)),
    Q_ij(c) = diag(P_X,P_Y)_ij (1−c²) − P_ij d_i d_j.

There is no summation on i,j in the final product. The characteristic equation
is det Q(c)=0. At v=0 it reduces to det(D−c²K)=0 and all four roots are real.
At v=.1, a 70-digit polynomial solve, checked against the *direct matrix
determinant*, gives

    −0.46920915267099280925914156616316930353179339822365875488039515,
     0.47215683732114278116227455102815263070333742884463015433785095,
     0.098127449943615761809490035584461036245011105245890713128960566
       ± 0.0046680484025079462116466851927116381662087932123137488646466845 i.

The largest normalized direct determinant residual is 6.29e−71. The boosted
time-kinetic matrix still has positive leading minors 225.0922422424 and
20552.0928581. Positive time kinetic therefore does **not** imply hyperbolicity:
the mixed relative-flow principal polynomial has a genuine complex pair.

This rules out promoting the aligned calculation to universal local matter
hyperbolicity on the tested constitutive domain. The algebraic auxiliary
constraints remain satisfied because X,Y are unchanged. The following local
construction also prevents dismissing this witness merely as an
off-gravitational-constraint constitutive point.

## Local initial-data constraint patch containing the bad principal point

On an initial spatial patch choose barred h_ij=delta_ij and K_ij=H(x)delta_ij,
using K_ij=+(1/2)L_n h_ij. Take T initially constant, its normal derivative
sqrt(2X(x)), and theta initially linear in x with constant spatial derivative
sqrt(2Y) gamma v and constant normal derivative sqrt(2Y) gamma. Thus Y, w,
and the relative velocity v remain fixed on the initial patch, while X varies.
Set lambda=P_w(X,w)/z. All scalar data are smooth and the two algebraic
auxiliary equations hold identically. At the witness,

    rho(X) = 2X P_X + 2Y gamma² P_Y − P = 3.0147594526108043,
    j(X) = T_ni = 2Y gamma² v P_Y = .03438770670818418,
    rho_X = P_X + 2X P_XX + 2Y gamma² P_XY = −531.5105429344.

With mstar=exp(−1/6), the actual ADM constraints reduce to

    6H² = 2rho(X)/mstar,
    −2H′ = j(X)/mstar.

The momentum sign follows directly from D_j K^j_i−D_i K=−2 partial_i H,
equal to T_ni/mstar in the stated positive-K convention; j here is **not**
the alternatively defined negative normal momentum density. Both geometric
reductions are checked symbolically from K_ij=H delta_ij.

Because rho_X is nonzero, the inverse-function theorem gives a smooth local
X=X(H). The smooth ODE H′=−j(X(H))/(2mstar) then supplies a local initial-data
patch satisfying both constraints, with H at the witness fixed by the positive
Hamiltonian root. Numerically H≈1.08957445, H′≈−.02031213769714 and
X′=6mstar H H′/rho_X. The code checks the point constraints and their
differentiated Hamiltonian identity directly at 70 digits.

The corrected activation value is r²≈1.1880410386>.75, and lambda>0 with an
interior field chart. These strict inequalities persist on a sufficiently
small patch by continuity, so the eta=1 reduced action remains the same full
IC17 action there. The complex pair is non-real by an open margin as well.
This is a local constraint-data existence argument, not a global boundary
construction or a finite-time solution. In particular, no well-posed evolution
is assumed to prove initial-data admissibility when the principal test fails.

## Reproduction and remaining scope

Run from this directory:

    python3 -m unittest test_ic17_dust_principal.py -v
    python3 ic17_dust_principal.py
    python3 ic17_dust_principal.py --require-full-closure

The seven tests include a negative control expecting the complex pair, not a
health assertion for that state. Audit exit 0 means the computations and the
explicit falsification reproduced; it does not mean the matter cone passes.
Failed verification checks exit 1. Strict full-closure requests exit 2 after
successful computation. The report retains `matter_cone_status=FAIL` and
`full_theory=OPEN`. Tests were run before implementation, observed failing,
then rerun against the actual implementation.

No radiation, vorticity, caustic evolution, strong-coupling cutoff,
full spatial constraint algebra, transition certificate, sourced MOND limit,
or complete cosmological history is established here. Next work must face
the relative-flow failure in this same action, not merely its aligned limit.
