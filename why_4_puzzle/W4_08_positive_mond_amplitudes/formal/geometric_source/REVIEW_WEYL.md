# Independent phase and curved-clock review

2026-10-20. Reviewer: gap_selection_physics, author of the separate Weyl
packet. Base f4d7d0e7a; criteria-only commit 1a46afd06.
The original healthy microscopic xi=1/4 goal remains open.
This is an independent analytic cross-review of P1 and P3. The P2 Weyl
remarks below are author self-review, not independent evidence.
No script, build, scan, download, Lean edit or source modification was used
for this review. Equations were reconstructed from the displayed actions.

## 1. Frozen evidence reviewed

All paths are relative to this directory. SHA256 pins:

| File | SHA256 |
| --- | --- |
| GRAVITY_PHASE.md | 3fb2a93890c8d81b953a43eb20cb85ef4d62ff0a44a34fa56c5f98200821950a |
| SOURCES_PHASE.md | f14b99fce4b22e29c87041c77494ee80d850338861d6e85b9d52f5a778a13aa2 |
| CURVED_CLOCK.md | cc734eccbcda67b27d39fbc36de75f0dfc33927325805afb24ac597e5336453a |
| SOURCES_CLOCK.md | 4a0f5d95a3c6c8cc8ed742789047c3c967b20d1eafae67a156b5339e955d36b3 |
| WEYL_SOURCE.md, author self-review only | c22d9b33f73e02f9498ace95334f954969c7c182779bc5a46837baa5870d3f8d |
| SOURCES_WEYL.md, author self-review only | e01333ba0a97b0c72a78e46fa2a78b4009dd71e52d11b72b8d7c18c1f6dd5149 |

I authenticated the Khoury primary exact-version HTML header
[1602.05961v2, 20 April 2016](https://arxiv.org/html/1602.05961v2),
and checked its displayed Eqs.18 and 73 against the static and covariant
operators used in P1. The source's supplied wider extraction pins were
read; this review does not claim a new authentication of every citation.
P3 is a new reduction of a fixed local action. Its inherited source cards
are distinguished from that calculation and are not reauthenticated here.

## 2. P1: exact static response and retained-field limitation

The action varies the gravitational potential itself and couples the
same potential to baryonic and superfluid mass. The force dictionary has
no independent phonon/test charge. Its n-dimensional surface-flux equation
Omega_(n-1)r^(n-1)E_h=M_enclosed and three-dimensional Newton coefficient
G=1/(8pi M^2) have the correct factors and attractive sign.

Writing x=h/(3a0), y=1+chi^2, the identity
1/y+x^2 y-2x=(xy-1)^2/y proves the stated global minimum at y=1/x for
0<x<1. The excess at y>=1 for x>=1 is (y-1)(x^2-1/y)>=0.
Consequently E_min=M^2[2h^3/(3a0)-h^4/(9a0^2)] and
mu=h/a0-2h^2/(9a0^2), with the reported positive interior radial
susceptibility. Retaining the quartic correction is essential.

Direct differentiation at the minimum gives
m_chi^2=8M^2h^4[1-h/(3a0)]/(9Z^2a0^2). Differentiating chi_*(h) gives
the stated gradient cost. On h=sqrt(Gm a0)/r its ratio to the leading
cubic is asymptotically 9Z^2r^2/[16M^2(Gm)^2]. Thus finite Z prevents
a uniform algebraic large-radius limit. This is a conditional diagnostic
of the profile used, not a proof excluding every retained-field halo.

The relativistic P(Y) variation gives epsilon=2Y P_Y-P. The reported
finite-density expansion and small positive equation of state check;
that state cannot be relabeled as a positive invariant vacuum merely
because P(mu) is constant in a local static expansion.

Both explicit potential tests check. The regular positive mass repair
has a broken interval iff h^2/(9a0^2)+b/h^2<1, with the reported roots;
it restores a quadratic response at sufficiently small h. For the
bounded positive deformation U_A=epsilon+A chi^6/(1+chi^2)^6, first and
second variations at chi=0 vanish while the ultraviolet minimum remains
chi=0. The low-h reduction has

    C3(A)=min_(s>0){M^2[1/s+s/(9a0^2)]+A/s^3},
    dC3/dA=1/s_A^3>0.

The positive root and second derivative establish the unique minimum.
This is an explicit static normalization counterfamily preserving the
specified vacuum/linearized/ultraviolet data, rather than parameter
counting. It does not claim unchanged curved halos or a healthy UV theory.

## 3. P1: normal-fluid variation and curvature scope

Twice integrating the normal-fluid operator gives
S_n=-(2M^2/3)int sqrt(-g)n_f Box F. Its Euler current is indeed
nabla_mu[n_f(Box F)(B^-1)_IJ partial^mu phi^J]=0. At chi=0, F=1,
so no bulk quadratic normal-fluid action follows from that displayed
operator; the first delta n_f times nonconstant F mixing is cubic.
This identifies a missing quadratic sector in the truncation, not a
demonstrated propagating ghost in every completed fluid theory.

The corrected rest-fluid example includes the quartic Gauss correction
to h itself. With z^2-(2/3)z^3=b_r^2/r^2,
z=b_r/r+b_r^2/(3r^2)+..., hence F=2z-z^2 gives
F=2b_r/r-b_r^2/(3r^2)+... and Delta F=-2b_r^2/(3r^4)+... .
The nonconstant Laplacian therefore survives the self-consistent force
correction. It is an additional equation to solve jointly, not a global
halo exclusion. The finite-Z asymptotic limitation remains separate.

For the stated fixed de Sitter diagnostic, Box n_f=Box Y=0 gives
Q_curv=6H^2 and canonical chi mass 12M^2H^2/Z^2. Constant nonzero-density
Y does not generally solve a^3P_Y Thetadot=constant. The report correctly
does not present that diagnostic as a full finite-density solution or
add a flat-space algebraic window to curvature by assumption.

## 4. P3: exact curved vacuum constraints

For B=M_Pl^2, 0<M<B, A=B-M and S_c=2B+M, I reconstructed the transverse
shift equation s=-MV/A. Its reduced speed
c_V^2=(2B-M)/(2A) and positive time coefficient agree. With U=aV,
the de Sitter 2H^2 term cancels after the stated temporal boundary,
leaving the positive conformal oscillator at finite nonzero k.

The longitudinal raw ADM bracket, lapse and shift solutions also check.
After their substitution C=2AS_c/M and D0=CH^2+MX are positive.
Using Xdot=-2HX in the final cross term gives precisely

    K_z=CMX/D0>0,
    V_z=2BX^2[M(2B-M)X+C S_cH^2]/D0^2>0.

Freezing X during integration would change this result. The reported
friction is positive; Omega_z^2 is increasing in X and therefore
decreases along expansion. Its Lyapunov derivative is nonpositive.
Boundedness of zeta requires the additional argument supplied: the
limiting first-order system has eigenvalues 0,-H and bounded evolution,
with integrable O(X) errors. This proves future boundedness at each
fixed finite initial k, not a uniform nonlinear or strong-coupling bound.

At strict k=0 the finite-k shift inverse is unavailable. The direct
v=I1a^-1+I2a^-2 solutions check. The given Killing vector has zero Lie
metric variation and generates the acceleration-free a^-1 clock tilt;
delta a_hat=vdot+Hv distinguishes the a^-2 mode. The large-isometry
boundary-condition caveat is required and retained. Positive clock
blocks do not repair the separate rational scalar's zero vacuum spatial
stiffness or singular real-auxiliary Hessian.

## 5. P3: actual homogeneous Bianchi control and its boundary

The exact relative-rapidity aether invariant and odd scalar/clock block
check directly. Homogeneous shift variation gives h(Kd-jh theta)=0;
the zero scalar momentum is thus a constraint for h>0. Eliminating it
produces mu_theta^2=2H_perp^2-h^2 j a_slope/(KM). No linear auxiliary
source supplies a missing quadratic elimination term in this block.
The finite-h perturbation of u.partial phi is nonzero, so it is not the
acceleration-free vacuum isometry.

I independently checked the background lapse, shear and h equations,
including Hdot=-3Av^2/B_cos-F_s/(6B_cos). For initially zero shear on
the expanding root, H>=H0 and v<=0 imply h<=h_i exp(-H0t) before a
positive H_perp is assumed. The integral bound on v and the explicit
smallness condition then prove H_perp>3H0/4 and mu_theta^2>H0^2.
The integrable approach to the limiting roots -H0,-2H0 supports the
reported decay. This is a genuine noncircular homogeneous basin at
fixed coupling, nonuniform at M=0 or A=0.

The rational-point threshold M/B>1210/27129 is only an instantaneous
initial sign. Neither it nor the basin is a coupled finite-k finite-h
Bianchi theorem. The earlier subcurvature weak-gravity packet has a
different ordered limit and its own regular-constraint/cutoff conditions.
P3 preserves these limits, does not recount earlier lambda>1 ADM work
as this new model, and does not infer a matter charge or selected xi.

## 6. Author self-review and decision

For my own P2 report I checked the external-vector versus normalized
variational closure, multiplier stress cancellation, matter trace chain
rule, finite-gradient scalar symbol and conditional operational ratios.
These checks are not independent review of my work. The final restored
units use inverse-length a_geom and reproduce the same dimensionless
32pi/(lambda beta^2); no measured scale or target fixes that invariant.

No required algebra correction remains in the independently reviewed
P1/P3 texts at the pinned revisions. Their scoped constructive results
stand: universal attractive metric response in an algebraic EFT window,
and controlled curved clock sectors in the specified vacuum/homogeneous
basin. They do not establish a regular microscopic completion, a global
sourced curved MOND halo, an invariant selecting equation or xi=1/4.
