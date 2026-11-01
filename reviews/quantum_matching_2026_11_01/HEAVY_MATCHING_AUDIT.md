# TP02 coordinator reconstruction of finite heavy-state matching

This derives a calculable part of the next-order effective action. It does
not replace genuine finite two-loop graphs or direct finite kinetic graphs.
The background preserves the unbroken SU(3) x SU(2) subgroup and the stated
real/imaginary symmetry slice. Retain the original real X; vary A=i aD and
B=bD, D=diag(2,2,2,-3,-3), with real a,b. All derivatives below use these
unnormalized matrix-amplitude coordinates consistently.

## Heavy classical Hessian

Direct evaluation of the raw F potential gives

    V0=(f-15h a²)²+(15/2)lambda²a⁴+30a²(hX-lambda b)².

At a0²=2fh/(30h²+lambda²), b0=hX/lambda, the two heavy derivatives vanish
and their Hessian is diagonal:

    Haa=120fh, Hbb=60lambda²a0², Hab=0.

The Coleman–Weinberg gradient must be taken from the full mass matrices at
this stationary background, not by differentiating the already minimized
one-dimensional potential. Spectral Fréchet derivatives of the one-loop
sum give these gradients without evaluating a tachyonic off-shell trial.

At zero occupancy the leading heavy displacement is
delta a=-V1_a/Haa, delta b=-V1_b/Hbb. Its finite potential correction is

    Delta U_relax=-1/2[V1_a²/Haa+V1_b²/Hbb].

Because the displacement is one-loop, this is a two-loop-order contribution
to the reduced potential even though it requires no two-loop vacuum graph.

## The same displacement changes the phase interaction

The microscopic R phase rotates X and B together; A is uncharged. Thus
the tree angular coefficient before heavy elimination is

    Ftheta=X²+30b².

The vacuum heavy displacement induces
Delta Ftheta=60b0 delta b at first order. The corresponding radial pullback
change is 60X²(h/lambda) partial_X(delta b); they need not be equal.
These are finite geometric matching pieces, not the complete one-loop
component kinetic action.

At angular frequency omega, work with the grand-potential density
Omega=V-omega²Ftheta. The heavy source is

    Ja=V1_a,
    Jb=V1_b-omega²60b0.

Eliminating the two heavy amplitudes to leading order therefore gives

    Delta Omega_relax=-1/2[Ja²/Haa+Jb²/Hbb].

The square includes the vacuum correction, its induced angular metric and
an omega⁴ operator. On the charge-supported branch omega² is one-loop in
the weak-coupling power count, so all three terms matter at the same order
being tested. Adding only the vacuum shift and metric while omitting the
quartic term does not compute the full leading heavy response of that state.
Conversely adding the full square plus those terms separately double-counts
them.

At fixed phase density n, the equivalent leading correction uses
E0=n²/(4Ftheta0) and replaces omega²60b0 by E0*60b0/Ftheta0. The
Legendre-transform consistency can be checked before numerical use.

## State thermodynamics and limits

On a stable stationary branch Omega_X=0,

    n=-partial_omega Omega,
    P=-Omega, epsilon=Omega+omega n,
    c_s²=n/[omega (dn/domega)_branch].

The branch derivative includes X(omega). With a nonzero density and
regular radial/phase coefficients, the zero sound-speed boundary can be
found from Omega_XX=0 while preserving Omega_X=0. This is a local
homogeneous-state statement; additional modes and phase-charge violation
are separate obligations.

The full gradient source, heavy Hessian and matching scale must be pinned
before these formulas supply numerical evidence. Direct finite two-loop
graphs, component derivative thresholds, occupied light sectors and the
anomalous current remain named missing inputs after this calculable subset.
