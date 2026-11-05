# Full-variation Solar STF quadrupole

This implements the candidate specified in KT37 PLAN, following the generalized
action of [Milgrom (2023), equations 6 and 16](https://arxiv.org/html/2305.01589v2).
The paper supplies the action framework; the calculations and boundary analysis
below are this lane's work. No observational result or novel-law claim is
imported from the paper.

Use rM=sqrt(GM_sun/a0), with dimensionless acceleration in a0 units, and the
unchanged external gradient eta e_z. The length lambda=ell_physical/rM is
universal in physical units; its Solar dimensionless value is not a fitted
object parameter. Let

```
g = g0(r)n+eta e_z,
H = gp nn+gt(I-nn),  gp=g0', gt=g0/r,
x=g.g, z=x+lambda^2(gp^2+2gt^2),
R(z)=Q(z)/z, Q'=nu_simple(sqrt(z)), Q(0)=0,
C=R-1+xR', D=lambda^2 xR', A=Cg, B=DH.
```

The complete anomalous source is S=div A-double_div B. Both terms are
required by the variation. In particular, replacing the law by a modified
nu in div A alone is not this calculation. Q=z gives A=B=0 exactly; lambda=0
gives the unchanged simple-QUMOND source.

## Angular Green reduction

Put p(mu)=3mu^2-1 and F=p/r^3, the STF zz derivative of 1/r off the origin.
Since the Poisson Green function is -1/(4pi r), integration by parts gives

```
q_A=(1/(4pi)) integral grad F.A d^3x,
q_B=(1/(4pi)) integral Hess F:B d^3x,
```

plus the boundary/contact terms below. Define angular integrals

```
a(r)=integral_-1^1 p C(g0+eta mu) dmu,
b(r)=integral_-1^1 C[eta(3mu-5mu^3)+g0(1-3mu^2)] dmu,
d(r)=integral_-1^1 p D dmu.
```

Direct contraction gives

```
q_A,flux=(3/2) integral b/r d(log r),
q_B,flux=6 integral (gp-gt)d/r^2 d(log r).
```

For the exterior point-Sun field g0=r^-2, gp=-2r^-3, gt=r^-3, this becomes

```
q_B,flux=-18 integral d/r^5 d(log r).
```

Indeed, Hess F:H=(gp-gt) d^2F/dr^2=12(gp-gt)p/r^5, since Delta F=0.
The 1/(4pi) azimuthal integral contributes 1/2. This fixes the sign and
factor of the Hessian contribution. The parent independently reconstructed
this contraction.

## Smooth-core contact and outer surfaces

A literal delta-source Hessian contains a distribution, whose square in z
is not defined. The point formula is interpreted only through regular
spherical source limits, not by substituting distributions into P.

For a smooth spherical core g0=kr+O(r^3), the origin has H=kI. With
z0=eta^2+3lambda^2 k^2 and derivatives with respect to x at fixed H:H,

```
C_x=2R'+xR'',
D_xx=lambda^2(2R''+xR'''),
q_A,contact=8 k eta^2 C_x/15,
q_B,contact=-(8/3) k^3 eta^2 D_xx.
```

The first is the known source-only QUMOND contact at lambda=0. The second
can be checked locally without distribution conventions: for H=kI,
B=kD(x)I and -double_div B=-Delta[kD(x)], so its local potential is -kD.
Since x=eta^2+2k eta z_coord+k^2r^2, the STF zz Hessian of -kD is precisely
the second contact above. Higher radial corrections to H have isotropic
second derivatives at the origin; their first derivatives vanish, and they
add no STF contact. The parent independently checked both terms.

For a finite radial endpoint, define T=gp+2gt=div(g0 n). The surfaces are

```
S_A=a/(2r),
S_B=(1/2)[gp d'/r+T' d/r+3gp d/r^2].
```

The whole-space approximation over a finite integration interval uses
q=q_A,flux+q_B,flux-S_A(rmax)+S_B(rmax)+q_A,contact+q_B,contact.
The omitted inner density integral must be negligible and is tested by domain
changes. Replacing the origin contacts by S_A(rmin)-S_B(rmin) instead gives
the exact finite-annulus integration-by-parts identity.

## Shrinking Gaussian source limit

A Gaussian core of width sigma has k=sqrt(2/pi)/(3sigma^3). For fixed
lambda>0, z0 grows as lambda^2 sigma^-6. The simple-Q primitive obeys
R-1=2z^-1/2+O(log(z)/z), R'=-z^-3/2+O(log(z)/z^2), with the corresponding
derivative asymptotics. Consequently both STF contacts tend to zero as
O(eta^2 sigma^6/lambda^3).

For the exterior point field, subtract its eta=0 part and average eta with
-eta before considering the origin. This leaves only the part relevant to
the even STF quadrupole. The resulting A is O(eta^2 r^7/lambda^3) and B is
O(eta^2 r^6/lambda); hence all STF origin surfaces vanish. The integrated
point kernels are convergent at zero. The pointwise exterior convergence
of shrinking Gaussian fields and the vanishing core contacts are analytical;
the numerical runs additionally check decreasing finite core widths. A
complete uniform dominated-convergence proof for every possible regulator
is not claimed. The model is defined here with the stated Gaussian limit.

## Differential-source check

An independent differential evaluation of the same angular moments uses

```
integral p div A dmu = a'-a/r-3b/r,
integral p double_div B dmu
 = gp d''+(gp'+T'+2gp/r)d'
   +(T''+2T'/r-6gt/r^2)d.
```

These follow by integrating the angular divergence by parts. Radial
derivatives of C and D are evaluated analytically from x,z and their
derivatives, not by differentiating sampled q values. The direct density
quadrupole is -1/2 times the first expression plus 1/2 times the second,
integrated against d(log r). Agreement with the Green expression checks
the full variation, surfaces, and normalization. It is not a second full
three-dimensional Poisson solver.

Physical normalization remains Q2_signed=(3/2)(a0/rM)q, graded by its absolute
value against 5.2e-27 s^-2. The ordinary Newtonian Solar Hessian is excluded.
The diagnostic retains the prescribed constant Galactic field; actual
Galactic gradients and an ephemeris fit are separate tasks.
