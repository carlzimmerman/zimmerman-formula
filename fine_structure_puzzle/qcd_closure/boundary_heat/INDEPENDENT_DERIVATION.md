# FSP-005: relative-wall boundary heat benchmark, independent derivation

This hand derivation was saved before inspecting any scientific file in
`qcd_completion/far_field/`. It uses the closure contract and the exact sources
in `SOURCE_RECORDS.json`. It is a benchmark for a specified wall determinant;
it is not a monopole determinant, a metric stress, or a physical-alpha result.

## Operator, multiplicity, and convention

Take the product Euclidean metric on B_R^3 x S_L^1, a constant Cartan A_4=v,
v>0, and vanishing field strength. For each charged Matsubara conjugate pair
put q=2 pi n/L+v, m=|q|>0. The convention in the contract gives

    Gamma_n = Tr_C4 log(-Delta+m^2)_relative
              - 2 Tr_C log(-Delta+m^2)_Dirichlet.

The factor two on the scalar ghost is essential. In spatial terms this is
the relative three-vector heat trace minus one Dirichlet scalar heat trace:
the fourth vector component is another Dirichlet scalar.

Use the inward unit normal e_n=-rhat and the convention
L_ab=<nabla_a e_b,e_n>. Thus L_ab=delta_ab/R for the two sphere directions,
K=L_aa=2/R. The circle tangent has L_44=0. The mixed-wall data are

    P_+=rhat rhat^T,  rank P_+=1;
    P_-=I_4-P_+,     rank P_-=3;
    S=-(2/R)P_+;     chi=P_+-P_-.

They reproduce (partial_r+2/R)A_r=0 and tangential A=0, including A_4.
The inward Robin sign follows directly from the source relative-domain
formula. The origin is smooth and creates no boundary. For the constant
benchmark there are no gauge-connection curvature or endomorphism terms.

Write

    K_n(t)=Tr_vec exp(t Delta)-2 Tr_D exp(t Delta)
          ~ (4 pi t)^(-3/2) sum_{k>=0} A_k t^(k/2).

## Moving projection: exact fourth heat coefficient

At a boundary point choose orthonormal sphere tangents t_1,t_2. With R=1
temporarily,

    chi_:a=2(t_a rhat^T+rhat t_a^T),
    sum_a tr(chi_:a chi_:a)=16,
    sum_a chi_:a chi_:a=4(P_sphere+2P_+),
    tr(sum_a chi_:a chi_:a S)=-16.

The circle component of chi is constant. Hence the three projector-derivative
terms in the mixed a4 formula contribute, in units R^(-3),

    -12 tr(chi_:a chi_:a) K = -384,
    -24 tr(chi_:a chi_:b) L_ab = -384,
    -120 tr(chi_:a chi_:a S) = +1920,
    sum = +1152.

The cubic L terms give

    [(280+3*40)*8+(168-3*264)*4+(224+3*320)*2]/21
      = 1024/7.

The four S terms give

    144*(-2)*4+48*(-2)*2+480*4*2+480*(-8)=-1344.

The tangential total derivative integrates to zero: the trace of S is
constant on the closed sphere. Consequently the vector's boundary a4
polynomial is 1024/7-1344+1152=-320/7. Dividing by 360 and integrating
over 4 pi R^2 yields

    A_4(vector relative) = -32 pi/(63 R).

A scalar Dirichlet field has polynomial

    (40*8-264*4+320*2)/21=-32/7,
    A_4(D)=-16 pi/(315 R).

The requested charged gauge/ghost combination therefore has

    A_4 = -128 pi/(315 R).

The finite large-mass term in Gamma_n=-integral_0^infinity dt K_n(t)
exp(-m^2t)/t is

    Gamma_n|_{1/(mR)} = -A_4 Gamma(1/2)/[(4 pi)^(3/2)m]
                      = +16/(315 m R).

This is a nonzero spectral boundary coefficient with the actual moving
normal/tangent splitting. Freezing that splitting is not a valid substitute.

## Orthogonal TE/TM check

On a smooth three-ball the exact-gradient relative sector is isospectral
to the positive Dirichlet scalar spectrum. It cancels the remaining scalar.
The transverse sector is the union, for l>=1 with multiplicity 2l+1, of

    TE: j_l(x)=0,
    TM: (x j_l(x))'=0,       lambda=x^2/R^2.

These conditions follow by using j_l(kr) X_lm for a toroidal vector and its
curl/k for a poloidal vector, imposing zero tangential vector at R. A
divergence-free vector automatically obeys the normal relative Robin
condition there. The l=0 transverse vectors do not exist. Thus this heat
trace equals a scalar Dirichlet trace plus a scalar Robin trace with outward
Robin constant 1/R, after subtracting the two l=0 scalar sequences. The
l=0 roots are n pi (n>=1) and (n+1/2)pi (n>=0). Their sum is the interval
Dirichlet heat trace with interval length 2R; it has no t^(1/2) term.

For the scalar Robin trace S=-1/R in the source convention, the a4
polynomial is 160-192=-32. Its integrated coefficient is
-16 pi/(45 R). Adding the Dirichlet coefficient gives

    -16 pi/(45 R)-16 pi/(315 R)=-128 pi/(315 R),

independently reproducing the mixed-projector result. This is an analytic
spectral decomposition, not a numerical fit to truncated roots.

## Lower boundary orders and subtraction

The same mixed coefficients give

    A_0=2 Vol(B_R^3),  A_1=0,
    A_2=-32 pi R/3,   A_3=5 pi^(3/2),
    A_4=-128 pi/(315 R).

Thus the heat-trace constant is A_3/(4 pi)^(3/2)=5/8. With zeta/analytic
continuation for this fixed three-dimensional mode, the local terms are

    Gamma_n = -Vol*m^3/(3 pi) - (8/3)mR
              +(5/8)log(m^2/mu^2) +16/(315mR)+O((mR)^(-2)),

up to the corresponding local counterterms and the normalization convention
for the logarithm. The table, rather than an arbitrary finite subtraction,
is the invariant heat input. This is an asymptotic expansion for mR large;
the coefficient is not the full determinant at finite mR.

## What a Coulomb profile changes at the same inverse-radius order

For h(r)=v-1/r, keep one fixed nonzero q and put s=sign(q), m=|q|.
Near a large wall the local positive mass is m_b=m-s/R. A smooth extension
through the core is required before applying smooth heat theorems globally;
the local wall calculation depends only on the displayed boundary jets.

Merely replacing m by m_b in 16/(315mR) changes it first at R^(-2).
However lower-order boundary functions and derivative terms must also be
expanded. The logarithmic term already gives

    (5/8)log(m_b^2)=(5/8)log(m^2)-5s/(4mR)+O(R^(-2)).

The K*m_b term has no inverse-R term when expressed in terms of the actual
mass m_b; expanding V=m_b^2 only to first order would incorrectly create
one. A first normal derivative of mass coupled to K also contributes at
inverse R. This can be derived without importing a bulk IBP convention:
for a scalar-potential perturbation f=delta V times I_4, Duhamel gives

    delta Gamma = integral_0^infinity dt exp(-m^2t) K(f,t).

In the exact smeared a3 formula the coefficient of f_;n for the vector is
(6+3*30)K+96*(-K)=0, while the two ghosts give -60K. The f_;nn coefficient
is proportional to the combined tr chi=0. Therefore the boundary first-jet
term, to the order needed here, is

    -5/(128 pi) integral_boundary K*(partial_in V)/m^2
      = -5/(64 pi) integral_boundary K*(partial_in m_b)/m_b.

For partial_in m_b=-s/R^2 this contributes +5s/(8mR). At this order the
geometric cubic term, the mass expansion of the logarithm, and this first
jet give a candidate scalar-mass wall coefficient

    [16/315 - 5s/8]/(mR).

The fixed-mass +16/315 benchmark is the principal verified result. The
last formula is an additional local scalar-potential response derivation,
to be independently reviewed before it is promoted as a full profile wall
coefficient. It includes only the scalar part (omega+h)^2 of the operator.

A term involving partial_in^2 m_b could have this same dimensional size,
but its flat-wall coefficient vanishes in this gauge/ghost combination
at the linear order that could contribute: the smeared a3 f_;nn term has
combined tr chi=0. Terms quadratic in the mass gradient begin at R^(-2)
on the wall. Linear spin-curvature insertions have zero Lorentz trace
against the symmetric geometric coefficient matrices. The gauge-connection
curvature is Lorentz-scalar; tr_Lorentz(chi chi_:a)=0. Consequently these
local boundary formulas contain no linear magnetic F~R^(-2) contribution;
quadratic F terms integrated over the wall start at R^(-2), not inverse R.

This does NOT remove the monopole's bulk derivative contribution. Bulk
terms F^2/m and (partial m)^2/m decay as r^(-4) and their exterior integral
is proportional to 1/(mR). They are as large as the boundary benchmark.
They include electric spin terms from F_i4=partial_i h, magnetic terms,
and scalar-potential gradients; their coefficients and common regulator
must be retained. Shifting a bulk Laplacian term by IBP shifts a displayed
surface density, so it cannot substitute for the boundary spectrum.
Core matching, neutral/charged coupling, topology, and the complete
four-dimensional regulated sum are further obligations.

## Common four-dimensional regulator and surface matching

No frequency sum has been executed. If it is performed, a common PV
definition is

    Gamma_PV = -integral dt/t sum_j c_j exp(-M_j^2 t)
                         sum_n exp(-q_n^2t) K_n(t),
    c_0=1, M_0=0,

with the same regulator fields and relative/Dirichlet domains for every n.
One may require sum_j c_j M_j^(2k)=0, k=0,1,2, sufficient to suppress the
small-t four-dimensional divergences. This is a definition of the regulated
sum, not permission to renormalize frequencies separately. The cubic-wall
piece is

    (16/(315R)) sum_n sum_j c_j/sqrt(q_n^2+M_j^2).

Before PV removal it is finite. The unregulated sum has a logarithmic UV
divergence since its two tails behave as L/(pi |n|). A local cubic
extrinsic-curvature boundary counterterm on S_R^2 x S_L^1 is therefore
required. Its finite part changes the holonomy-independent inverse-R wall
term. Fixing that finite part, or comparing two gapped holonomies in the
same surface scheme, is necessary before calling an absolute summed
inverse-R coefficient physical. A same-scheme holonomy difference converges:

    (16/(315R)) sum_n [1/|2pi n/L+v|-1/|2pi n/L+v_0|].

This does not perform the Coulomb-profile sum. In particular sums and
large-R/mass expansions must be justified with the common regulator;
profile-dependent lower-order local functions may have nonuniform
frequency sums. No physical electromagnetic charge has been extracted.

## Scope and continuation

Verdict: the constant-gapped-holonomy local boundary benchmark is proved
from the authenticated mixed heat formula and checked by exact TE/TM
decomposition. The complete monopole inverse-R determinant/stress remains
open. The smallest next checks are an independent audit of the smeared
mass-jet derivation and a common-PV matching of bulk derivative, surface,
and core contributions. Numerical experiments below verify only the
finite exact arithmetic encoded from these formulae; they do not prove
a uniform asymptotic remainder or a full gauge-theory observable.
