# Finite heavy-photon matching through the first mixed QCD order

FSP-010, base FSP-009. This derivation and the source input were written
before the bounded algebra run. Use u=e^2, k=1/(16 pi^2), canonical
L_g=-G^2/4, and L=log(s/mu^2), where s is the heavy photon's squared mass.
All parameters on the full-theory side are MSbar parameters held fixed at
mu. The photon couples to the conserved vector current sum Q_f qbar gamma q.
Retained quark masses and external invariants are small relative to s.

## 1. Source result and the correct intermediate theory

The exact primary inputs are the PDF of Martin, arXiv:1812.04100v3,
equations (1.15), (2.2), (2.15)-(2.16), (2.20), (2.26), (3.2), (3.7).
The PDF equations, rather than current HTML equation numbers, are used.
Bednyakov arXiv:1410.7603v4 independently describes the complete graph set,
bare-to-renormalized matching, electroweak gauge-parameter cancellation,
and its original result. Martin reports an independent recalculation.
Neither paper states our vector-current limit verbatim.

Introduce a hierarchy sqrt(t) << sqrt(W),sqrt(Z),sqrt(h), all still above
external momenta. Set y_t^2=g^2 t/(2W), r=W/Z, and keep 0<r<1 fixed.
There are SIX quarks in the intermediate QCD+QED theory obtained by first
decoupling W,Z,h. Only after this step is the small top mass decoupled.
Taking t to zero in a five-flavor formula without restoring this intermediate
mass parameter gives a wrong answer.

From Martin (1.15), F(t,Y)=O(Y^2 log(t/Y)/t) at fixed Y>0. Every
g_s^2 y_t^2 term of (2.16) therefore vanishes as O(t log t), or faster.
The term t log(t/W)/(t-W) vanishes too. The remaining coefficient of
k^2 g_s^2 g^2 in the simultaneous matching is

    T=8(r-1)L_t/9 +3 L_W
       +(25/(18r)-13/9+14r/9)L_Z
       -49/27-r/18-163/(216r).                         (1)

This expression retains the top as a light mass in the hard electroweak
matching, but the source's final EFT has already removed it. The subsequent
top threshold from (3.7), expressed in full-theory couplings, contributes

    P=(1-r)[-8 L_t/9-26/27]                            (2)

at this mixed order. It uses Q_t=2/3, T_F=1/2. The intermediate top mass
must also be matched. The Yukawa-free limit of (2.20) gives

    delta m_t/m_t =k g^2 m1,
    m1=(6+3/r)/16 +K(3L_Z-5/2),
    K=(1-r)(4r-1)/(9r).                               (3)

The use of (2.20) for a now-light top follows from its identical up-type
gauge representation once all Yukawa couplings vanish. No massive-top
Yukawa or Higgs threshold is retained. Its squared EFT mass is
t_EFT=t[1+2k g^2 m1]. Inserting this into the one-loop top threshold
(2/3)k g_s^2 log(t_EFT/mu^2) adds (4/3)k^2 g_s^2 g^2 m1.

Consequently the electroweak hard threshold with all six quarks retained is

    V=T-P-4m1/3
     =3(L_W-3/4)+A_Z(r)(L_Z-3/4),
    A_Z(r)=10r/3-11/3+11/(6r).                        (4)

The L_t terms cancel exactly. Omitting (3) changes BOTH the neutral-current
charge polynomial and the finite constant. This is sequential matching,
not a retuning of the original physical path: the EFT parameters are
derived functions of the fixed full-theory parameters.

## 2. Admission of the vector-current limit, including gauge and IR issues

At this order a heavy colorless vector appears only as one internal line
joining two vertices of a single massless quark loop with two external
gluons. Include every ordering, hence both vertex and quark-self-energy
topologies. Gluon/ghost vertices have no direct electroweak coupling; no
additional heavy-vector ghost graph contributes at this order. The source
matches the complete renormalized amplitude and not an OPE logarithm.

For massless quarks, chirality is conserved on the quark lines. Two neutral
vertices therefore produce c_L^2+c_R^2; left and right give identical parity
even two-gluon tensors. No cross-chirality term survives. This is also why
the axial-axial and vector-vector pieces of THIS one-loop fermion trace
agree. No singlet axial triangle or two-quark-loop anomaly graph enters
this two-loop two-gluon amplitude. This does not assert an all-orders
equality between singlet axial and vector currents.

For the six SM quarks the neutral couplings, divided by g, are

    up_L=(4r-1)/(6 sqrt(r)), up_R=2(r-1)/(3 sqrt(r)),
    down_L=-(1+2r)/(6 sqrt(r)), down_R=(1-r)/(3 sqrt(r)).

Three copies of their squared sum equal A_Z(r). The six charged-current
orientations give 6*(1/sqrt(2))^2=3. Both vector masses enter the same
massless one-scale fermion tensor: the only group dependence is the sum
of these squared couplings. Equation (4) thus determines the complete
universal single-vector finite function, not merely its RG slope.

In the six-flavor intermediate theory, the relevant hard region has loop
momenta of the vector mass. Purely soft regions are reproduced by the EFT.
The first current-current operator left by vector exchange is dimension
six, suppressed by 1/s. With small masses retained until the matching
difference is formed, its insertions do not alter the leading dimension-four
threshold. The surviving small-top dependence in the simultaneous formula
is exactly (2) and (3); equation (4) verifies cancellation of this regulator
dependence. Setting all light masses/external momenta to zero only after
this subtraction leaves the source's finite MSbar hard coefficient.

Goldstone/Higgs exchange is proportional to Yukawa couplings and drops out
of this limit. The scalar tadpole/VEV convention is accounted for in the
source parameter definitions and in (3); its uncharged pieces cannot be
silently deleted before sequential matching. Bednyakov's arbitrary
electroweak gauge calculation and Martin's separate Landau-gauge calculation
agree on the renormalized coupling threshold. We do not independently
recompute their d-dimensional tensor integrals or pole cancellations.

For a conserved VECTOR current, the longitudinal difference between a
massive Landau vector and canonical Feynman photon covariance gives zero
after current Ward identities and their contacts are included. The vector
limit therefore applies to the canonical massive photon. Its vector mass
may be called a running or fixed mass at this order: the relevant difference
first shifts the displayed threshold at a higher coupling order.

## 3. Finite gluon and mixed quark thresholds

For c_L=c_R=e Q_f, equation (4) gives S_Q=sum_f Q_f^2 and

    alpha_s,EFT/alpha_s,full
      =1+k^2 u g_s^2 S_Q(2L-3/2)+higher orders,
    g_s,EFT/g_s,full
      =1+k^2 u g_s^2 S_Q(L-3/4)+higher orders.           (5)

Thus the actual EFT coupling increment is

    (g_s,EFT-g_s,full)/u
      =g_s^3 S_Q/(256 pi^4) [L-3/4].                  (6)

The finite number 3/4 was extracted from the complete source threshold,
including mass matching; it was NOT inferred from a beta function.

The mixed quark partner follows independently from the Q_f^2 neutral-current
part of PDF (2.26). A Z-quark vertex has a common vector part proportional
to Q_f in both chiralities. The coefficient of Q_f^2 isolates two such
vector vertices; W, isospin-only and VEV terms are independent of Q_f^2.
Massless photon contributions agree between the two theories and cancel
in matching. Since g'^2(r-1)=-g^2(1-r)^2/r, replacing the squared common
vector coupling by u Q_f^2 gives

    (m_f,EFT-m_f)/m_f
       =k u Q_f^2[-3L+5/2]
        +k^2 u g_s^2 C_F Q_f^2[-3L+17/4]
        +O(u g_s^4,u^2,m_f^2/s), C_F=4/3.             (7)

The 5/2 one-loop result agrees with the independent FSP-010 Dirac threshold.
The 17/4 is a new finite mixed quark coefficient in this package. It is
not obtained by multiplying 5/2 by a beta-function coefficient.

## 4. Proton insertion, pure-QCD trace and signs

Let sigma_f=<p|m_f qbar_f q_f|p>/(2M)=m_f partial M/partial m_f,
H_g=<p|[G^2]|p>/(2M), and gamma_m=-d log(m_f)/d log(mu) in pure QCD.
The bracketed gluon operator is the pure-QCD renormalized coupling-derivative
operator, with its usual scalar mixing. Vacuum subtraction is implicit.

    M=sum_f(1+gamma_m) sigma_f +beta_s H_g/(2g_s),
    partial M/partial g_s=-H_g/(2g_s).                  (8)

The second identity follows equivalently by differentiating the rescaled
kinetic term or by combining dimensional analysis with the QCD RG equation.
This is a derivative at fixed renormalized masses; replacing it by a total
derivative along a different mass path is incorrect. Equations (6)-(8) give
the leading-power large-s proton endpoint f(s)=M_u(s)/M:

    f(s)=sum_f Q_f^2 sigma_f/M {
             k[-3L+5/2]+k^2 g_s^2 C_F[-3L+17/4]}
          -k^2 g_s^2 S_Q <[G^2]>/(4M^2) [L-3/4]
          +higher orders and power corrections.                    (9)

In particular define B_g=k^2 g_s^2 S_Q <[G^2]>/(4M^2).
The gluonic endpoint is -B_g L+(3/4)B_g. At leading pure-QCD order,
beta_s=-beta_0 g_s^3 k, and

    B_g=-S_Q/(16 pi^2 beta_0)
             [1-sum_f(1+gamma_m)sigma_f/M]+O(alpha_s). (10)

This reproduces the signed full-tensor OPE slope of FSP-007. Equation (8)
fixes the matrix element GIVEN the sigma terms and coupling; it supplies
neither the finite 3/4 in (6) nor numerical sigma terms. Source Gasser
1506.06747v3 uses a counterterm symbol delta g_s with the opposite sign to
the actual positive bare/threshold coupling increment. Its logarithm is
delta g_s/u=-g_s^3 S_Q k^2 log(Lambda^2/mu^2), in agreement with (9).

## 5. Heavy-photon threshold versus sharp O(4) photon conversion

Equation (9) is first a HEAVY-PHOTON threshold at fixed MSbar parameters.
Its relation to a sharp photon cutoff needs a separate argument. For the
finite vector-current convolution write g(t) for its renormalized scalar
density, f(0)-f(s)=int g(t) s/(t+s) dt (common local terms cancel).
A sharp photon cutoff at Lambda^2=s instead inserts theta(s-t).

For a dimension-four term with g(t)=B/t at this order,

    int_0^infinity dt/t [s/(t+s)-theta(s-t)] =0.        (11)

The integral is absolutely convergent across both endpoints and the matching
point. If the asymptotic remainder is o(1/t), with sufficient integrable
power/log control, its contribution tends to zero as s becomes hard.
The one-scale massless coefficients at the displayed orders have no
additional log(t) multiplying B/t; the leading gluon c_1g of the inherited
full-tensor OPE is explicitly constant. Consequently the finite gluon
conversion between this SHARP PHOTON prescription (other lines uncut) and
MSbar is also the endpoint (9), with L=log(Lambda^2/mu^2), through the
displayed order. At higher orders log(t) terms generate nonzero filter
moments and this equality must not be assumed. A non-rotational regulator
or different current contacts also requires its own conversion.

Thus the finite gluon mass counterterm contribution is

    D_ct^g/M = B_g[-log(Lambda^2/mu^2)+3/4].           (12)

Equivalently the Gasser-sign counterterm parameter is
delta g_s/u=-g_s^3 S_Q k^2[log(Lambda^2/mu^2)-3/4].
This is not an independent adjustable parameter. At mu=Lambda the finite
term remains. Equation (11), not an identification of regulators by name,
is the additional admission needed for (12).

## 6. What remains physical

This fixes actual local finite coefficients, conditional on the explicitly
checked source-to-vector translation above. It does not supply the full
nonlocal proton Compton convolution, numerical pure-QCD scalar matrix
elements, higher strong orders, threshold running for physical flavors,
or a controlled finite-s power remainder. It does not identify proton and
vacuum ensembles or evaluate curved unconditioned QCD A, R, or alpha.

The finite algebra run checks (1)-(12), all six chiral charge factors, the
mass-threshold composition, vector projection, and regulator moment. It
does not constitute a new evaluation of a two-loop Feynman integral or
independent verification of the primary source's UV/IR subtraction.
