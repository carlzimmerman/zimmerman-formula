# Fixed KT39 law: screening scales and Solar coefficient

This derivation concerns the already tested p=9/8, ell=3 kpc response. The
general formulas below assume p>1, ell>0 and, for Solar asymptotics, a fixed
positive uniform external field eta. No baryon, a0 or cut is changed. It
explains the mathematical action mechanism; it does not derive p or ell
from microscopic physics.

## 1. Full equations and exact scalar primitive

Let g=grad psi, H=Hess psi, Delta psi=4piG rho, and

    x=g.g/a0², s=ell²(H:H)/a0², z=x+s^p,
    E=a0²P=g.g R(z), R=Q/z.

The full anomalous response is

    A=[R-1+xR']g, B=p ell² s^(p-1)xR'H,
    Delta Phi_ph=div A-partial_i partial_j B_ij.

For the original simple nu, put y=sqrt(z). The primitive fixed by Q(0)=0 is

    Q(z)=z/2 +(y+2)sqrt[y(y+4)]/2
         -2 log[(y+2+sqrt[y(y+4)])/2].

Direct differentiation gives Q'(z)=1/2+sqrt(1/4+1/sqrt(z)). The stable
implementation uses a small-z series and rationalized high-z expressions;
the displayed closed form is for interpretation, not a replacement algorithm.
At small z, R~(4/3)z^(-1/4); at large z, R-1~2z^(-1/2).
Since Q' is strictly decreasing, R=integral_0^1 Q'(tz)dt>Q'(z), so
zR'=Q'-R<0 for every z>0.

## 2. The actual discriminator is acceleration variation as well as magnitude

At a point with g!=0 and H!=0, define L=|g|/||H||_F and y=|g|/a0. Then

    chi=s^p/x=(ell/L)^(2p) y^(2p-2),
    chi=1  iff  L=Lcrit=ell y^((p-1)/p).

At p=9/8 this is Lcrit=ell y^(1/9). Thus the response remains sensitive
to small spatial scales even at low acceleration: lowering y by a factor
100 only lowers Lcrit by a factor100^(1/9), about1.668. For example at
y=.01 and ell3kpc, Lcrit=1.79845kpc. Compact sub-kpc dwarf fields can have
chi much greater than one despite being deeply below a0.

chi is an action-input ratio, not an exact force-suppression factor. Even
the A-only response need not decrease monotonically with chi. In the joint
deep regime z<<1 its total first-gradient part satisfies

    (g+A)/(g nu_simple(y))
       ~ (4/3)(1+chi)^(-1/4) -(1/3)(1+chi)^(-5/4).

Its derivative at chi=0 is +1/12; only at large chi does the leading
chi^(-1/4) suppression dominate. More importantly, -double_div B is mandatory
and can enhance or reduce a particular force/virial observable.

The fixed-profile weak-amplitude limit (g,H)->epsilon(g,H) has
chi~epsilon^(2p-2). At p9/8 this is only epsilon^(1/4). Ordinary leading
deep-MOND recovery as epsilon->0 is therefore mathematically true away from
persistent zero-gradient saddles but very slow in the actual dwarf regime.

## 3. Point-mass and external-field crossover lengths

For an isolated point mass m=GM, rM=sqrt(m/a0),

    |g|=m/r², ||H||=sqrt(6)m/r³, L=r/sqrt(6),
    chi=6^p ell^(2p) rM^(4p-4)/r^(6p-4).

The exact isolated chi=1 radius is

    rc=6^[p/(6p-4)] ell^[2p/(6p-4)] rM^[(4p-4)/(6p-4)].

For p9/8,

    rc=6^(9/22) ell^(9/11) rM^(2/11)
       proportional to ell^(9/11) M^(1/11) a0^(-1/11).

This isolated expression is not the Solar crossover in its Galactic field.
For a uniform external gext=eta a0 and radii where the Solar g is much
smaller than gext, x~eta² while the Solar Hessian remains proportional to
r^(-3). Hence

    rstar=6^(1/6) ell^(1/3) rM^(2/3) eta^[-1/(3p)].

For p9/8, its eta exponent is -8/27. The two frozen footings give rstar
1.696720pc and1.684860pc. By comparison, Solar g equals the original external
field at0.0245142pc on either footing. Thus the curvature-controlled response
is displaced well outside the ordinary external-field transition. Exact
chi=1 roots using x=eta²+2eta(rM/r)²mu+(rM/r)^4 differ from rstar by less
than6.3e-5 relative at mu=-1,0,+1; see crossovers_001. The formal isolated
Solar rc~0.8kpc should not be interpreted as the physical Solar screening
radius in the Galactic environment.

## 4. A leading Solar quadrupole theorem for the point-source diagnostic

Use the repository's Solar dimensionless radius r/rM, lambda=ell/rM,
g=r^(-2)n+eta e_z, and s=6lambda²r^(-6). Set u=r^(-2),
x=eta²+2eta u mu+u², D=beta xR'(x+s^p), beta=p lambda²s^(p-1).
The reviewed Green expression is

    q_B=-18 integral_0^infty r^(-5)
             integral_-1^1 (3mu²-1) D dmu d(log r).

For any twice differentiable F(x(mu)), two integrations by parts give the
exact cancellation identity

    integral_-1^1 (3mu²-1)F(x(mu))dmu
      =eta²u² integral_-1^1 (1-mu²)² F_xx(x(mu))dmu.

The boundary terms vanish because both (1-mu²)² and its first derivative
vanish at mu=+-1. With F=D,

    D_xx=beta[2R''+xR'''].

Rescale r=lambda^(1/3)v. Then s=6v^(-6), u=lambda^(-2/3)v^(-2), and
x tends to eta² for each fixed v>0. Multiplying q_B by lambda leaves a
finite integrand. Near v=0, its absolute value against d(log v) is bounded
by a constant times v^(9p-3), using z>=s^p and
|2R''+xR'''|<=C z^(-5/2). At sufficiently large v, x is uniformly bounded
below by eta²/4 and the bound is C v^(-6p-3). Both bounds are integrable
for p>1. On the remaining compact annulus the derivatives are uniformly
bounded. Dominated convergence therefore applies.

Writing t=s^p and alpha=1/(2p) yields the leading coefficient

    q_B = c(eta,p)/lambda + o(lambda^(-1)),
    c(eta,p)=-(96/5) eta² 6^(-5/2)
       integral_0^infty t^alpha
         [2R''(eta²+t)+eta² R'''(eta²+t)] dt.

For completeness the A angular kernel is
b=integral C[eta(3mu-5mu³)+u(1-3mu²)]dmu, C=R-1+xR'. Its exact
Legendre cancellations give

    b=-eta²u³ integral (1-mu²)² C_xx dmu
      -(eta^4 u³/3) integral (1-mu²)³ C_xxx dmu.

Thus q_A=(3/2)integral b/r d(log r)=O(lambda^(-7/3)). The same rescaling
has integrable inner powers v^(15p-7),v^(21p-7) and outer v^(-7), so the
stated order is uniform for fixed eta>0,p>1. It is smaller than q_B.

The frozen dimensional convention is Q2=(3/2)q a0/rM, not q a0/rM.
Consequently

    Q2 = (3/2)c(eta,p) a0/ell + o(a0/ell)

in this large-lambda point-source limit. At p9/8 the coefficients are
-0.158273168685 canonical and -0.152400971727 alternate. Their dimensional
Q2 values reproduce the accepted full calculation within2.4e-8 relative.
The A/B magnitude ratio in that calculation is only about1.8e-8. The Solar
success is thus principally a curvature-stress effect with scale a0/ell;
dropping B would remove the dominant predicted quadrupole.

This is an ordered, fixed-eta point-source asymptotic. The coefficient's
leading independence of Solar mass is not a uniform decoupling theorem as
M->0: the response region itself shrinks as rstar proportional to M^(1/3),
and derivatives at the source need not converge uniformly. The statement
also assumes a constant external field, not an explicitly solved Galactic
tidal background or a specified microscopic regularization.

## 5. Exact Plummer scaling and the dwarf deficit

Let a be the Plummer radius, u=r/a, and alpha=GM/(a²a0). Then

    x=alpha² u²/(1+u²)^3,
    s=(ell/a)² alpha² 3(1+2u^4)/(1+u²)^5,
    L=a u(1+u²)/sqrt[3(1+2u^4)].

At r=a this becomes

    L=2a/3,
    chi(a)=8(9/32)^p (ell/a)^(2p) alpha^(2p-2).

At p9/8, chi(a) is proportional to ell^(9/4) M^(1/4) a^(-11/4)
at fixed a0. Size is a much stronger discriminator than mass. At the
actual Upsilon3 sources, chi(a) is about237 for Sculptor,32 for Fornax,
and401 for LeoI on the canonical footing. Their small acceleration alone
therefore does not restore ordinary QUMOND.

The force is not inferred from chi. The exact spherical equation used is

    g_ph=Cg-(Dg')'-2D(g'-g/r)/r,
    D=p ell² s^(p-1)xR'.

For unit-normalized Plummer tracer density, split the line-of-sight virial
variance into Newton, A and B pieces using

    sigma²=(4pi/3) integral rho_unit(r) r³ g_total(r) dr.

The frozen numerical response reconstructs all selected KT39 dispersions
to7.2e-15km/s. At Upsilon3, canonical (Newton,A,B) contributions in
(km/s)² are Sculptor (10.9782,25.7391,-11.7252), Fornax
(35.0836,114.1594,-44.5208), and LeoI (27.2284,29.7950,-15.0366).
The B contribution removes roughly40–50percent of the A variance in these
examples. This is an observed property of these fixed profiles, not a sign
theorem for arbitrary sources. The mechanism combines a curvature-modified
A response with a negative virial contribution from its mandatory B stress.
Neither contribution may be dropped to obtain a more favorable fit.

These exact scalings and finite decompositions explain the existing dwarf
deficit. They do not establish a satellite external-field prediction,
equilibrium distribution or viable microscopic completion. The Milky Way
requires its nonspherical full-response decomposition; an isolated spherical
scale argument alone cannot establish its four observational passes.
