# Charge exchange, the vacuum trace, and a non-Born threshold discriminator

FSP-009, route C1. This is a raw candidate derivation for fresh review.
No empirical alpha, proton mass, magnetic moment, polarizability or fitted
QCD spectrum is inserted. The full A_rho(u), full M_u and R remain open.

## 1. Exact comparison on the same QCD measure

Let m_u=m_d=m_l>0 at u=0. Fix all other renormalized masses and strong
parameters in a declared scheme. Let S be the nonanomalous vector flavor
rotation that interchanges u and d. For a diagonal rational charge matrix Q,
write Q^S=SQS^-1. In particular the two currents with

    Q=(2/3,-1/3,-1/3,...) and Q^S=(-1/3,2/3,-1/3,...)

are conserved currents of exactly the same pure-QCD theory. No hadron
spectrum or residue is changed independently. The charged QED extensions
differ, as they must for a charge-spurion test of a claimed universal Ward
identity. Their parameter and counterterm prescriptions are relabeled by S.

Use a common, flavor-covariant regulated action on an arbitrary fixed metric
and define W=-log Z, I_Q=partial_u S_eff|_0 after photon integration. All
current seagulls, determinant contractions and matching terms belong to I_Q.
Flavor relabeling is a change of integration variables, so exactly

    W[g,u;Q]=W[g,u;Q^S],
    <I_Q>_g=<I_Q^S>_g.                                      (1)

The first equality holds along an exchange-covariant matched family, not
merely to leading u. With t=log(radius), T=partial_t S_0 and V=Omega exp(4t),

    rho_u[Q]=[<partial_t I_Q>-Cov(I_Q,T)]/(4V).               (2)

Since T and the metric are isoscalars, the two terms in (2) each transform
under the same change of variables. Thus the charge-odd vacuum response is

    Delta_S rho_u(g)=rho_u[Q]-rho_u[Q^S]=0                    (3)

at every regulated radius, before any H limit. I_t includes the photon
Green-function variation, weights, vertices, action/measure derivatives,
and finite source/gravity contacts. This proof neither deletes them nor
identifies a disconnected vacuum expectation with a proton covariance.
If the continuum and A_rho limits exist in that common prescription,
Delta_S A_u=0. No flat-gap or smooth-curvature expansion is needed for (3).

Equivalently write j_Q=j_0+j_3, where j_0 includes the light isosinglet
and all other fixed-flavor currents and j_3 is the third isovector current.
The only charge-odd quadratic term is j_0 D j_3+j_3 D j_0. Its unconditioned
vacuum expectation and every metric derivative vanish by vector isospin.
This is a representation selection rule for the actual regulated QCD
functional, not an arbitrary multiplicative vacuum normalization.

## 2. The proton maps to a different state

For X define H_p[X]=lim_(Tsep->infinity)
([<N_p Nbar_p X>/<N_p Nbar_p>]-<X>)/Tsep with the prescribed charged-state
regulator/dressing and endpoint terms. At u=0 this gives M_u^p=H_p[I_Q].
The rotation S maps N_p to N_n. Therefore

    M_u^p[Q^S]=M_u^n[Q],
    Delta_S M_u^p=M_u^p[Q]-M_u^n[Q].                         (4)

The vacuum terms in this difference cancel using (1). All quark-line
disconnected loops correlated with the baryon remain. The same identity
holds for the complete two-current tensor and for its non-Born part, PROVIDED
the full on-shell Born graphs, including their regular non-pole term and
matched form factors, are subtracted covariantly. No elastic contribution
is silently reclassified as a polarizability.

Equations (3),(4) are the actual comparison map. In Wigner--Eckart terms the
vacuum is a singlet; an isovector two-current interference matrix element
between I=1/2 baryons is allowed. Vector/trace Ward identities preserve
this flavor representation. A zero-momentum trace form factor fixes
<p|Theta|p>=2M^2 in relativistic normalization, but its charge derivative
contains the charge derivative of the state, operator and normalization.
It supplies the trace Ward identity inside (4), not a map to (3).

An integrated soft scalar/trace insertion is also diagonal in this flavor
classification. In particular differentiating (3) with respect to m_l or
the strong scale leaves zero; differentiating the right side of (4)
need not vanish. The following actual QCD low-energy coefficients make
that distinction quantitative after removing analytic polarizability
contacts with a quark-mass derivative.

## 3. Source-checked non-Born logarithm, not the old mass LNA

Bernard--Kaiser--Schmidt--Meissner, hep-ph/9309211v1, (6)--(10), gives the
complete SU(2) HBChPT polarizabilities through order q^4. Their companion
hep-ph/9311354v1, (8) and the paragraph immediately following, explicitly
excludes nucleon pole graphs from the polarizabilities. Denote the physical
electric/magnetic polarizabilities by a_E,b_M and strip their overall u:

    a_i=a_E^i/u, b_i=b_M^i/u, C/u=1/(96 pi^2 F^2).

At the displayed order let L=log(M_pi/mu_chi), m=M_N, and keep chiral-limit
F,g_A,m,kappa_s as the fixed matching quantities. kappa_s=kappa_p+kappa_n
is the anomalous isoscalar moment, not the neutron moment. The individual
1/M_pi terms and c_2,c_+ terms cancel in p-n. Directly subtracting the
source coefficients x_p=9,x_n=3,y_p=71,y_n=39 and
x'_p=3+kappa_s,x'_n=1-kappa_s,y'_p=37/2+6kappa_s,
y'_n=13/2-6kappa_s yields

    Delta a = g_A^2/(96 pi^3 F^2 m) [6L+4]+d_a(mu_chi)+higher,
    Delta b = g_A^2/(96 pi^3 F^2 m)
              [6(1+kappa_s)L+3(1+kappa_s)]+d_b(mu_chi)+higher. (5)

d_a,d_b are independent renormalized non-Born contacts; none is assigned
a number. Their scale dependence cancels the scale dependence of L. They
are analytic in m_l at this order and cannot remove the logarithmic
mass coefficient. In the sequential chiral expansion, differentiating
with respect to log M_pi removes those leading constant contacts:

    partial_logMpi Delta a -> g_A^2/(16 pi^3 F^2 m),
    partial_logMpi Delta b -> (1+kappa_s)g_A^2/(16 pi^3 F^2 m). (6)

The limits use the chiral-limit constants and require the usual controlled
HBChPT remainder. m_l partial_m_l is one half of partial_logMpi to this
order since M_pi^2=2B m_l. A scalar Feynman--Hellmann current insertion
therefore sees a nonzero charge-odd electric coefficient if g_A is nonzero,
while its unconditioned vacuum counterpart remains exactly zero.

This is a non-Born Compton threshold response; it is NOT the inherited
M_u proportional to M_pi result, a numerical polarizability prediction,
or a full mass integral. The source's resonance estimates and empirical
numbers after (10) are deliberately unused.

## 4. Complete SO(4) soft-photon contraction

It is insufficient to insert only b_M into the subtraction function. The
electric dispersive partner must be included in the same angular integral.
For photon momenta small compared with the pion threshold, the spin-averaged
Born-subtracted rest-frame effective action is

    S_pol,E = 2 pi u integral d tau [a E_E^2-b B_E^2].        (7)

The relative sign follows by Wick rotating the Minkowski polarizability
interaction 2pi[a_E E_M^2+b_M B_M^2]; it also reproduces the negative
static energy -2pi b_M B^2. Gaussian photon contraction gives

    <E_E^2>_Q=(3Q_4^2+q^2)/Q^2,
    <B_E^2>_Q=2q^2/Q^2.                                    (8)

The SO(4) mean of Q_4^2/Q^2 is 1/4, so both means are 3/2. Thus the leading
soft-band mass functional, before adding full-theory mass counterterms, is

    M_u^NB(0<Q<K)=3 K^4/(32 pi) (a-b)+o(K^4),              (9)
    C_soft=lim_(K->0) M_u^NB(0<Q<K)/K^4=3(a-b)/(32 pi).

This is also independently obtained in the parent's WLCM normalization:

    T1^NB=8 pi m Q^2 [b-(a+b)x^2]+O(Q^4),
    T2^NB=8 pi m Q^2 (a+b)+O(Q^4), x=Q_4/Q.

Then -3T1+(1-x^2)T2=8pi m Q^2[a-2b+2(a+b)x^2], and integration with
sqrt(1-x^2) gives (3pi/4)(a-b). The subtraction limit T1(0,Q^2)=
(2m/alpha_em)b_M Q^2 agrees with WLCM 1203.0254v2 (16),(17), after
its full Born term is removed. This is an orthogonal normalization check.
Possible off-shell operators involving partial_mu F^mu nu begin at higher
photon momenta; EOM/source redefinitions must nevertheless be matched in
a full all-momentum calculation.

Combining (5),(9) produces the new fully angular-contracted shape:

    Delta C_soft = g_A^2/(1024 pi^4 F^2 m)
                   [1-3kappa_s-6kappa_s L]
                   +3(d_a-d_b)/(32pi)+higher.             (10)

Consequently

    lim_(Mpi->0) partial_logMpi Delta C_soft
       = -3 kappa_s g_A^2/(512 pi^4 F^2 m).                (11)

The K->0 limit is taken FIRST at each positive M_pi; fixed K followed by
M_pi->0 would leave the low-momentum domain and is not used. A partial_m_l
insertion introduces the factor 1/2 described above. Equation (11) can
vanish on the exceptional kappa_s=0 branch; the tensor-level electric
coefficient (6) is still nonzero. The kappa_s-independent logarithms in
a and b cancel in the SO(4) mass convolution. Claiming their electric-only
coefficient as a full-mass coefficient would be wrong.

## 5. What this excludes, and what remains

The exact selection rule plus (5),(6) excludes a flavor-covariant Ward
identity that reconstructs the complete proton non-Born two-current tensor
from only the vacuum mixed metric/current functional. Its charge-odd channel
would equate an exactly zero vacuum quantity to the nonzero electric chiral
logarithm. This is a genuine allowed-current comparison within the same
QCD theory. It neither introduces a nonlocal gravitational counterterm nor
changes a QCD spectrum by hand. A local R term cannot imitate A_rho H and
plays no role in the argument.

The full soft mass channel has the additional cancellation (11). On a
branch with kappa_s nonzero it supplies a nonanalytic mass-functional
coefficient absent from the charge-odd vacuum. It does NOT prove that the
full all-momentum charge-odd M_u is nonzero: hard/inelastic/subtraction and
finite mass matching still enter its integral. A numerical cancellation in
that full scalar quantity is a dynamical question, not disproved here.

For fixed unretuned renormalized QCD parameters, if A exists and M_p=M_n=M
at u=0, the exact ratio comparison is

    Delta_S R_u^p = -3 A Delta_S M_u^p/M^4.                (12)

For the parent's fixed-proton calibration along ell, the projector instead
gives Delta_S (dA/du)|_M=-(A_ell/M_ell) Delta_S M_u^p when the held
mass-coordinate prescription is exchange covariant. More calibration
coordinates require its full Jacobian. This uses the inherited projector;
it is recorded only to prevent conflating the exact fixed-theory null
response (3) with independently retuned proton paths.

The surviving physical leaf is the isospin-even vacuum/current functional
and the full individual-proton non-Born convolution on one common path.
At physical isospin breaking the derivative of (3) is an additional
isovector scalar insertion, not an error bar supplied by this symmetric
calculation. A relation only at the physical charge matrix could still
hold accidentally or through extra dynamics; the present result rules
out obtaining it from the stated flavor-covariant Ward identities alone.
