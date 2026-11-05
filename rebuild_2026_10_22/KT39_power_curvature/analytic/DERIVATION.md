# KT39 power-curvature action and its limits

The general nonrelativistic action framework is from Milgrom,
arXiv:2305.01589v2, equation6: https://arxiv.org/html/2305.01589v2.
KT37/SOURCE_CHECK.md records the authenticated source/version. The function
chosen here is phenomenological, not literally that paper's equation16 or
a claimed fundamental derivation. Both p and common physical ell are now
searched parameters. The predeclared powers are1.25,1.5,1.75; lengths are
1.5,2,2.5,3,3.5,4 kpc. All baryons, a0 values and cuts remain fixed.

With g=grad psi and H=Hess psi, use the full Frobenius contraction and

    x=g.g/a0², s=ell² H:H/a0², z=x+s^p,
    E=a0²P=g.g R(z), R=Q/z, Q(0)=0,
    Q'(z)=nu_simple(sqrt(z)).

The stable scalar primitive and its derivatives are imported read-only
from KT37. The Newtonian auxiliary field still solves Delta psi=4piG rho.
Complete variation of the action gives

    Delta Phi_ph=div A-partial_i partial_j B_ij,
    A=.5E_g-g=[R-1+xR']g,
    B=.5E_H=p ell² s^(p-1)xR'H.

Indeed z_H=2p ell²s^(p-1)H/a0². A has acceleration units and B
acceleration-times-length units. Its weak source is
-integral grad(v).A-integral Hess(v):B, with the same explicit boundary
terms as the general KT37/38 action. Both adjoints are retained.
For stable coefficients, use d=zR'=Q'-R,f=x/z: A=[R-1+fd]g,
B=p ell²s^(p-1)fd H. At the joint zero jet the continuous E,A,B values
are zero; no physical floor is introduced. Naked R and invariant partials
remain singular there.

Q=z gives the exact Newtonian control A=B=0; ell=0 gives ordinary simple
QUMOND. p=1 reproduces KT37 and p=2 reproduces KT38. Six numerical test
functions check these controls, full tensor energy variation, weak scaling,
uniform-field variation, and exact spherical limits across all three powers.

## Weak scaling, origin regularity, and static response

At a fixed point with g!=0, scaling (g,H)->lambda(g,H) gives
z=lambda²x+lambda^(2p)s^p. For p>1 this restores the ordinary deep-MOND
leading A+g=lambda^(1/2)sqrt(a0/|g|)g. The Hessian term is
B=O(lambda^(2p-3/2)), subleading to A for all tested powers. Recovery
becomes slower as p approaches1 and is not uniform near persistent g=0
saddles.

At fixed g!=0,H=0, the energy correction starts at order|H|^(2p), so
E is C² for p>1 and its pure H-H quadratic variation vanishes. Thus the
uniform external-field linear susceptibility is ordinary QUMOND:

    delta Phi_hat/delta psi_hat=nu+eta nu' cos²(alpha), eta>0.

However B is proportional at leading order to |H|^(2p-2)H. It is C¹
but not generally C² for p<=1.5. For p=1.25 its second derivative can
diverge at a zero of H; for p=1.5 it can have direction-dependent limits.
The double-divergence source may therefore need its weak interpretation
even when the Newtonian field is smooth. For the tested smooth isolated
Plummer fields, H:H remains positive at every finite r>0, so their radial
integrals avoid this particular degeneracy without adding a floor. This
does not settle arbitrary source geometries or joint g/H zeros.

Nor does the H=0 improvement remove every short-wave tidal effect.
At a nonzero fixed background H, the rank-one Hessian variation K=nn has

    N(n)=.5E_HH[nn,nn]
      =p ell²s^(p-1)xR'
       +(2p ell^4 x/a0²)[(p-1)s^(p-2)R'
                         +p s^(2p-2)R''](n.H.n)².

If n.H.n=0, N(n)=p ell²s^(p-1)xR'<0. Such directions exist for a
nonzero indefinite vacuum tidal tensor, for example diag(k,-k,0) with
n=e_z and a nonzero background gradient. In a local high-frequency
expansion this contributes +N(n)|k_wave|² to the potential transfer.
The statement is about the highest spatial derivative, not a global
constant-H galaxy, and supplies no dynamical no-go or new observational
cut. Matter dynamics, a relativistic kinetic sector and general microscopic
source/coarse-graining prescriptions remain unspecified.

## Exact spherical force and limits

For g=psi'(r), b=g/r, x=g²/a0² and
s=ell²[(g')²+2b²]/a0², define

    C=R-1+xR', D=p ell²s^(p-1)xR',
    g_ph=Cg-(Dg')'-2D(g'-g/r)/r.

Analytic coefficient derivatives are

    x'=2gg'/a0²,
    s'=2ell²[g'g''+2(g/r)(g'/r-g/r²)]/a0²,
    z'=x'+p s^(p-1)s',
    D'=p ell²[(p-1)s^(p-2)s'xR'
              +s^(p-1)(x'R'+xR''z')].

The ell=0 branch is evaluated directly as ordinary QUMOND rather than
forming zero times a divergent fractional power. The full derivative of
D is retained in every nonzero-ell radial calculation.

For a smooth core g=kappa r+O(r³), s0=3ell²kappa²/a0²,z0=s0^p,

    g_total=kappa r[R(z0)-(2p/3)z0R'(z0)]+O(r³).

As positive kappa tends to zero at fixed ell, its central slope is
asymptotic to [(12+2p)/9](3ell²/a0²)^(-p/4) kappa^(1-p/2).
It tends to zero for the three tested powers, but its scaling differs
from the fixed-radius weak-field limit. At a quadratic saddle g=0,H=K,
the source is [R-1]trK-(2p ell²s0^(p-1)/a0²)R' tr(K³); it need not
vanish in vacuum. One cannot infer differentiated source values from A=B=0
at a single point.

For an exterior point field g=m/r², m=GM, put c=6ell²m²/a0². At fixed
ell>0, all tested powers satisfy curvature dominance as r tends to zero,

    g_ph ~ [2-p(2+3p)/3] m c^(-p/2) r^(3p-2).

The coefficient is negative for p>(sqrt(19)-1)/3, including all three
declared powers. This tiny anomaly is subleading to positive m/r²; it is
not a statement about the sign of every total-force profile. At large r,
s^p/x scales as r^(4-6p) and ordinary deep-MOND normalization is recovered.

For a Gaussian source shrinking at fixed eta>0 and ell>0, the same
angular-cancellation argument as KT37/38 gives origin contacts and B-core
flux O(eta² sigma^(9p-3)/ell^(3p)); uniform A-core bounds have powers
delta^(15p-7)/ell^(5p) and delta^(21p-7)/ell^(7p). These powers are
positive for every tested p. The B exterior tail scales as r^(-6p-3)
against d(log r), and A as r^-7. These statements concern the specified
regularized STF observable, not products of point-source distributions or
regulator independence. The Solar lane supplies the complete limit proof.

The isolated dwarf screen uses the full radial force, its integration-by-
parts virial, and direct variation of the actual new energy under Plummer
homology. It reports all18choices and retains signed local force diagnostics.
Counts are finite-grid observational screens, not equilibrium existence,
actual satellite EFE predictions, or global health claims.
