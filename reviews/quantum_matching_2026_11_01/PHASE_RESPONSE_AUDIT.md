# TP02 coordinator reconstruction: the phase response

This derivation starts from the complex canonical flat-field action, rather
than the stipulated waterbag pressure law. It is a fixed-background,
homogeneous local-state calculation, not a selected cosmological state or
an independent full quantum matching. A constant vacuum subtraction changes
absolute pressure but not the stability derivatives below.

## Canonical complex field

Take L=|partial T|²-U(|T|), with Minkowski contraction time minus space,
T=r exp(i theta), r>0. The phase current has homogeneous density
n_theta=2r² theta_dot. The R charge is twice this if R(T)=2. The exact
homogeneous fixed-charge energy is

    epsilon(n_theta,r)=n_theta²/(4r²)+U(r).

Writing s=ln(r/v), E=n_theta²/(4r²), stationarity gives U_s=2E>0.
This derives an inverse-square radial coupling, but its density exponent
is two, not the former waterbag exponent 5/3. At radial equilibrium,

    epsilon=U_s/2+U,
    P=n_theta partial_n epsilon-epsilon=U_s/2-U,
    D=partial_s² epsilon=U_ss+2U_s,
    dP/dln n_theta=U_s(U_ss-2U_s)/D.

The local fixed-charge radial branch requires D>0. Its long-wavelength
compressibility is positive only when U_ss>2U_s on that branch. This is a
different condition from the old waterbag's U_ss>3U_s.

## Direct amplitude/phase fluctuation check

At a circular state r=r0, theta=omega t, stationarity gives
2r0² omega²=U_s. Define sigma=sqrt(2) delta r and
pi=sqrt(2)r0 delta theta. The quadratic Lagrangian is

    L2=1/2[(partial sigma)²+(partial pi)²]
         +2omega sigma pi_dot -m_sigma² sigma²/2,
    m_sigma²=(U_ss-2U_s)/(2r0²).

For frequency Omega and wavenumber k, the determinant is

    (Omega²-k²-m_sigma²)(Omega²-k²)-4omega² Omega²=0.

The nonzero k=0 gap is D/(2r0²), whereas the low-k phase branch has

    c_s²=(U_ss-2U_s)/(U_ss+2U_s).

Thus positive fixed-charge radial curvature alone does not establish
gradient stability. If D>0 and the numerator is negative, an interval
0<k²<-m_sigma² has a negative Omega² branch in this local constant-state
system. This is not a gravity-driven Jeans inference or a finite-halo
formation claim. The result agrees with the thermodynamic calculation by
an independent fluctuation route.

## General matched angular kinetic coefficient

Let L=F(s)[(partial s)²+(partial theta)²]-U(s), F>0, and
a=dln F/ds. The tree canonical case is F=v² exp(2s), a=2.
At fixed n_theta, E=n_theta²/(4F), so aE=U_s. Work on a branch with
a nonzero, U_s/a>0, and

    D=U_ss+(a-a_s/a)U_s>0.

Then

    P=U_s/a-U,
    dln n_theta/ds=D/(2U_s),
    c_s²=[U_ss-(a+a_s/a)U_s]/[U_ss+(a-a_s/a)U_s].

This follows from epsilon_n=n_theta/(2F), P=n_theta epsilon_n-epsilon,
and the fixed-charge stationarity relation. The canonical radial gap is
D/(2F) at stationary occupancy. A field redefinition or running metric must
transform F, U and their derivatives together. Holding a=2 in a reference
coordinate after introducing wavefunction matching is not automatic.

More generally the two-derivative component action can have independent
positive coefficients A(s) for (partial s)² and B(s) for (partial theta)².
The fixed-charge energy and sound speed above use F=B, whereas the
nonzero amplitude/phase gap is D/(2A). In canonical local perturbations
the radial mass parameter is N/(2A), where N=U_ss-(a+a_s/a)U_s, and the
mixing coefficient squared is aU_s/A. Their sum is D/(2A), so the same
IR sound ratio N/D follows. Thus this sound-sign test does not need A=B,
but it does need the matched angular B, positive radial A and the stated
low-derivative restriction. Running field normalizations alone do not
calculate all finite component kinetic thresholds.

## A conditional coldness bound

Consider a connected branch starting at the broken-symmetry vacuum s=0,
with F0=F(0), F'>0, U_s>0, positive radial response, and nonnegative
sound numerator N throughout [0,s]. Put mu²=U_s/(aF). Then

    (mu²)'=N/(aF)>=0,
    U(s)-U(0)=integral_0^s mu²(t) F'(t) dt
                 <=mu²(s)[F(s)-F0].

The phase kinetic energy is E=mu²F. For the excess above the same vacuum,
epsilon_ex=E+Delta U and P_ex=E-Delta U. Hence

    w_ex=P_ex/epsilon_ex >= (F0/F)/(2-F0/F).

For the canonical angular metric this becomes

    w_ex >= 1/[2(r/r_vac)²-1].

It is therefore insufficient for the sound speed merely to approach zero
near a pressure boundary: if the entire stable branch spans only a modest
field-amplitude range, its vacuum-subtracted component still has a large
pressure-to-energy ratio. This is a conditional inequality, not an
exhaustive theorem for other charge states, disconnected branches or an
action with omega⁴/higher-derivative operators. It does not subtract the
vacuum from the gravitational action; it compares the additional occupied
component against the same vacuum.

## Remaining physical obligations

The rigid action supplies the phase degree and these classical couplings.
It does not choose a phase-charge density or prove its cosmological lifetime.
The R symmetry has a mixed SU(5) anomaly, so exact quantum charge
conservation cannot be assumed. Slow/background and derivative-expansion
conditions, light sectors and the matched metric must be checked before
using this local response as a halo model. The adjacent rotating-field
construction is already in the literature (SOURCE_CHECKS.md).
