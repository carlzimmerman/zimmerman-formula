# PN28-HALO: finite halos of the dispersion-coupled reduced equation of state

Coordinator continuation of PN28-DISP, opened after its explicit EOS passed
an initial algebra check. Owner `/root`; base checkpoint as in ../TARGET.md.
This is a conditional Newtonian equilibrium calculation, not a claim about
formation, kinetic stability, vacuum normalization, or the full scalar PDE.

## Inputs and first discriminator

The frozen ../dispersion_coupling/EOS.md has SHA256
`05f919345cb73c8b96e3f07d5fdb421ae8ee1d24a01e177abc9551aab4092274`.
For B,rho_*>0 its local reduced pressure and density are

    P_ex=P_total+V=B ln y,
    rho/rho_*=y^(2/5)(y-1)^(3/5),       1<=y<infinity.          (1)

P_ex is the total matter-plus-adjusted-scalar excess pressure. It is NOT the
MC27 bare kinetic pressure. Treat rho as the dominant Newtonian gravitational
mass density and neglect the cosmological force on the halo scale. Apply
dp/dr=-rho GM/r^2, dM/dr=4pi r^2 rho. Constant V drops out of the gradient but
its gravity has not been exactly solved here. Finite scalar gradients are
also omitted in the local auxiliary approximation. Both omissions require
scale checks before applying this to an actual parent solution.

The first discriminator is whether (1) itself has finite hydrostatic halos
and tends to the logotropic core-column relation, without installing a
separate exterior profile by hand.

## 1. Exact enthalpy transformation

Set t=1-1/y, so 0<=t<1. Then

    rho/rho_*=t^(3/5)/(1-t),
    P_ex=-B ln(1-t).

The specific enthalpy, zero at the vacuum edge, is exactly

    h=integral_0^rho dP_ex/rho
     =(B/rho_*) integral_0^t tau^(-3/5) d tau
     =(5B/(2rho_*)) t^(2/5).                                 (2)

Define psi=t^(2/5). The complete reduced EOS is therefore

    h=(5B/(2rho_*)) psi,
    rho=rho_* psi^(3/2)/(1-psi^(5/2)),
    P_ex=-B ln(1-psi^(5/2)),           0<=psi<1.               (3)

In particular it has one low-density edge and a bounded specific enthalpy.
With length ell=sqrt(5B/(8piG rho_*^2)), the hydrostatic equation becomes

    psi''+(2/r)psi'=-f(psi),
    f(psi)=psi^(3/2)/(1-psi^(5/2)),
    psi(0)=psi_c in (0,1),       psi'(0)=0.                    (4)

Here r is measured in ell; primes in (4) refer to that dimensionless radius.
Regular initial expansion: psi=psi_c-f(psi_c)r^2/6+O(r^4).

## 2. Every regular reduced halo has finite radius and mass

For each fixed psi_c<1, f is positive and locally Lipschitz on [0,psi_c].
The integral form of (4) gives the regular solution until it reaches zero.
Put m(r)=integral_0^r f(psi(s))s^2 ds. Then psi'=-m/r^2<0 for r>0.
No finite-radius singularity can arise while 0<=psi<=psi_c because f is
bounded on that interval. Suppose, for contradiction, the solution stays
positive for every radius.

Its decreasing limit must be zero. A positive limit would bound f below by
a positive constant, forcing m to grow at least as r^3 and psi to cross zero.
Consequently

    psi(r)=integral_r^infinity m(s)/s^2 ds >= m(r)/r.           (5)

Since psi decreases, and f(psi)>=psi^(3/2),

    m(r)>=r^3 psi(r)^(3/2)/3.

Combining this with (5) gives psi(r)<=9/r^4. But for any fixed r0>0,
equation (5) also gives psi(r)>=m(r0)/r for r>=r0, a contradiction at large
r. Thus the first zero R is finite. The density is bounded, so m(R) is finite
and positive; psi'(R)=-m(R)/R^2<0. The density vanishes as (R-r)^(3/2) and the
excess pressure as (R-r)^(5/2). The constant vacuum pressure outside matches
P_total(R)=-V. This proves finite radius and mass for the reduced model only.

## 3. The logotropic quarter-density column is an asymptotic theorem

Let n_c=rho_c/rho_*=f(psi_c), and define a central length
L_c=sqrt(B/(4piG rho_c^2)). Write zeta=r_phys/L_c and

    v=(rho_c/B)(h_c-h)=(5/2)n_c(psi_c-psi).

Equation (4) is equivalently

    v''+(2/zeta)v'=d_n(v),
    d_n(v)=f(psi_c-2v/(5n_c))/n_c,
    v(0)=v'(0)=0.                                            (6)

As psi_c approaches 1, n_c tends to infinity, and

    psi_c=1-2/(5n_c)+O(n_c^-2),
    d_n(v)=1/(1+v)+O(n_c^-1).                                (7)

The error is uniform for v in any fixed compact nonnegative interval. It
follows by expanding (3):
`1-psi^(5/2)=(1+v)/n_c+O(n_c^-2)` while `psi^(3/2)=1+O(n_c^-1)`.
The regular integral form of (6), with its bounded uniformly Lipschitz right
hand side on such intervals, gives continuous dependence through the
quarter-density crossing. For example,
`v(zeta)=integral_0^zeta (s-s^2/zeta)d_n(v(s)) ds`, so the usual integral
estimate has no singular coefficient at the center.

The limiting equation for Theta=1+v is

    Theta''+(2/zeta)Theta'=1/Theta,
    Theta(0)=1, Theta'(0)=0.                                  (8)

Its quarter-density point has Theta=4 and zeta=xi_q=5.84477267596...
The crossing is transverse because v'>0 at every positive finite radius.
It occurs at finite radius: if v<=3 for all zeta, its source is at least 1/4,
so v>=zeta^2/24, a contradiction. The finite-family quarter crossing likewise
converges to this point by (7) and transversality. Therefore

    rho_c r_(1/4) -> xi_q sqrt(B/(4piG))        as n_c->infinity. (9)

At finite n_c the coefficient is state dependent; it is computed from (4),
not set to xi_q. The two free parent/state quantities B and rho_* have not
been eliminated by this theorem.

The limit n_c->infinity is mathematical. To use it physically one must also
keep the NR rest-energy, negligible scalar-gradient and negligible vacuum-
force approximations valid. In particular the underlying conjugate kinetic
pressure grows roughly as B rho/rho_* at high density, so its characteristic
specific energy is of order B/rho_*. This ratio must be small compared with
c^2. No fixed-parameter arbitrarily concentrated halo is certified as a
solution of the full finite-gradient parent by (9).

## 4. A candidate acceleration relation, with its exact qualifications

The parent EOS supplies B=m_phi^2/(9g^2), with canonical scalar normalization
and the kinetic/potential conventions in EOS.md. If both the high-density
reduced-halo limit and the adopted identification Sigma=a0/(2piG) are used,

    a0^2 = pi xi_q^2 G m_phi^2/(9g^2).                       (10)

Here m_phi^2 denotes the curvature of the canonically normalized potential;
converting a particle mass in SI units requires the usual hbar,c conventions.
Equation (10) ties the candidate acceleration scale to a scalar stiffness and
coupling. It does not derive either parameter or their ratio to V. The factor
1/2 in a0=(1/2)c sqrt(G rho_Lambda) would require, additionally,

    m_phi^2/(g^2 V)=9/(4pi xi_q^2).                          (11)

The action admits independent B and V changes. Thus (11) is an outstanding
physical selection condition, not a result of this construction.

## Evidence and continuation

The mathematical finite-radius and asymptotic statements above are analytic.
check_halo.py independently integrates (4), checks density/potential mass
identities, derives the reference xi_q directly from (8), and tests a finite
range of central states at two numerical tolerances. Results, versions,
source hashes and caps are recorded by the computation runner. Numerical
agreement is not the proof of the all-central-state statement.

Next physical discriminator: retain the scalar gradient term from the same
parent and derive its static halo boundary problem and the validity range of
the local reduction. A finite core with a selected B/V, phase-space state,
and formation mechanism is still required. No old MC27 kinetic closure or
empirical fit has been silently transferred to this changed total-pressure
model.
