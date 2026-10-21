# Extended supersymmetry: moment maps, positive vacuum and the response operator

2026-10-20. Base b37b50b1c; criteria-only commit 1d58a0851.
**The healthy microscopic xi=1/4 goal remains open.** This is a bounded
analytic continuation, not a new ultraviolet completion or a universal
no-go for extended supersymmetry. No measured scale, target, coefficient
scan, script, build, download or Lean calculation enters.
Exact primary versions and extraction limits are in SOURCES_EXTENDED.md.
Use c=hbar=1, signature -+++, and distinguish FI xi_FI from physical xi.

## 1. The strongest explicit FI candidate and its actual action

The four-dimensional Antoniadis--Partouche--Taylor (APT) model has an
Abelian N2 vector multiplet: a complex scalar a, photon, two fermions and
an auxiliary triplet. In N1 superspace its two-derivative terms are

    K=(i/2)(a Fbar_a-abar F_a), f_gauge=-i F_aa,
    L=int d4theta K + [int d2theta(f_gauge Walpha^2/4+W)+c.c.]
          +sqrt(2) xi_FI D,
    W=e a+m F_a, tau=F_aa=s+i t, t>0.

This is a genuine N2 electric/magnetic FI action, distinct from the
inherited five-dimensional CS prepotential and ordinary electric FI test.
APT explicitly treats it as a general low-energy action, not a derived
renormalizable microscopic completion for arbitrary F. In the N1 component
description the algebraic sector is

    Laux=t F_aux Fbar_aux+t D^2/2
           +[F_aux(e+m tau)+c.c.]+sqrt(2)xi_FI D,
    t F_aux+overline(e+m tau)=0, t D+sqrt(2)xi_FI=0.

The N2 dual formulation also fixes the imaginary auxiliary triplet
Im Y=2 M_FI; its field-independent contribution is retained below.
Eliminating these auxiliaries gives, in the source's convention,

    V=[(e+m s)^2+xi_FI^2]/t+m^2 t+2mp.

Here e,m,xi_FI,p have mass dimension two. The real p=Im E_2 is part of
the full N2 FI action and enters only through its field-independent term.
It must not be omitted when claiming an absolute gravitating vacuum.
The scalar/photon bosonic kinetic terms in our signature are

    L_bos=-t partial a.partial abar-t Fmunu^2/4
                 +(s/4)Fmunu Ftilde^munu-V.

Topological sign conventions do not enter the scalar calculation below.
For m,xi_FI>0 and a point where tau_a is nonzero, stationary minimization
in the regular tau chart gives s0=-e/m, t0=xi_FI/m and

    V0=2m(xi_FI+p).

The source's preserved-N1 vacuum and central/FI algebra therefore do not
alone fix a positive cosmological constant: p is still an independent
action datum. In particular the source discusses p=-xi_FI. A rigid value
of V0 is not automatically the potential of a local N2 supergravity
completion. Minimal nonsupersymmetric Einstein coupling would give
Tmunu=-V0 gmunu on a constant state; that operation does not prove a
supersymmetric gravitational completion.

## 2. Retained canonical modes and the absence of an actual MOND branch

Choose e=0, xi_FI=m t0 and a local holomorphic prepotential with
tau=i t0+c a, c real nonzero of mass dimension -1. This is a test of
the admissible action, with no coefficient chosen from the target.
Write a=u+i v, so s=c u and t=t0+c v. Around a=0,

    V=V0+(m^2 c^2/t0)(u^2+v^2)+O(a^3),
    Lkin=-t0[(partial u)^2+(partial v)^2]+O(a (partial a)^2).

Thus u_c=sqrt(2t0)u, v_c=sqrt(2t0)v are canonical real fields and, in
this displayed bosonic normalization,

    m_can^2=m^2 c^2/t0^2>0.

The photon has positive coefficient t0 and remains massless. The regular
positive FI state supplies massive scalar response, not a shift-symmetric
long-range MOND mediator. For a stipulated scalar source -J u,
(Delta-m_can^2)u=J/(2t0) at linear order. Its attractive scalar exchange
is Yukawa, with the source/test coupling still to be specified. Integrating
regular gapped modes locally yields an analytic small-derivative expansion;
it cannot be identified with a leading |grad Phi|^3 constitutive action.

There is an exact auxiliary-looking relaxation diagnostic, but it does
not repair that source problem. At fixed real u in this linear-tau model,
minimizing over v is equivalent to minimizing over t>0:

    V(u,t)=m^2[t+(t0^2+c^2u^2)/t]+2mp,
    t_*(u)=sqrt(t0^2+c^2u^2),
    V_min(u)=2m^2 sqrt(t0^2+c^2u^2)+2mp.

It is analytic at u=0 and starts with u^2. This is a scalar *potential*,
not energy as a function of a gravitational gradient. Neither t nor a
is an auxiliary field of the retained theory. Replacing u by |grad Phi|
would introduce a new operator and is not an N2 derivation.

For ordinary N2 charged matter a superpotential sqrt(2)(a+m_f)Q Qtilde
gives mass M_f=sqrt(2)|a+m_f| in that conventional normalization.
At real positive m_f, its canonical u charge is 1/sqrt(t0), while its
charge per inertial mass depends on m_f. Gauge charge also remains.
This observation does not assert that naively adding this matter to a
magnetic-FI action supplies a consistent local completion. It shows why
a universal attractive metric source cannot be inferred just from the
vector-multiplet central-charge formula. A completed matter action and
its full vector/scalar force are missing.

The singular limits are different theories or EFT limits: xi_FI=0 drives
t0 to the kinetic boundary, m=0 has no regular isolated FI minimum, and
tau_a=0 removes the above mass argument. At such points charged light
states or other critical modes must be retained. No assertion here rules
out an interacting N2 critical theory; this regular branch is insufficient.

## 3. An exact allowed N2 higher-jet deformation at fixed vacuum data

Extended supersymmetry does restrict a chosen prepotential's operators,
but it does not fix that holomorphic function merely by naming N2.
Take the explicit local two-derivative family

    F_d(a)=i t0 a^2/2+c a^3/6+d a^7/42,
    tau_d=i t0+c a+d a^5,           c,d real.

d has mass dimension -5. For every sufficiently small neighborhood of
a=0, t=Im tau_d remains positive. The same a=0 state, FI auxiliaries,
V0, photon/scalar kinetic coefficients and canonical scalar masses are
unchanged. Differences of the kinetic metric begin at fifth order in
the physical scalars, and differences of the potential at sixth order.
On the retained component slice v=0 the exact expression is

    V_d(u,0)=V0+(m^2/t0)[c^2u^2+2cd u^6+d^2u^10].

This slice is not stationary for u nonzero: writing s=c u+d u^5,
V_v=-m^2 s^2 s'(u)/t0^2 there. It is not legitimate to discard v and
call this an exact one-real-field completion of U_eta.
Nevertheless its gapped stationary v branch exists locally by the
implicit-function theorem. At d=0 it has v_*(u)=c u^2/(2t0)+O(u^4).
On that branch the leading d-dependent potential correction is still
2m^2 c d u^6/t0: the first-order envelope variation is V_s delta s,
because V_t=0 on the undeformed stationary branch. It provides a concrete
N2-allowed higher potential jet with unchanged vacuum quadratic data.

This is a local special-Kahler EFT family, not a UV-complete microscopic
counterfamily with the Khoury portal or a globally healthy MOND solution.
It does not establish an N2 completion of the entire rational tail.
Its narrower implication is exact: N2 and its FI algebra by themselves
do not forbid all sextic potential deformations near this broken vacuum.
Extra global, microscopic or duality input would have to exclude this F.

## 4. What the Higgs-branch theorem does and does not protect

The APS Higgs-branch argument concerns the two-derivative metric of
massless neutral hypermultiplets on rigid unbroken-N2 vacuum branches.
Local vector/hyper factorization and promotion of the gauge coupling
or strong scale to a background vector imply the protected metric.
It is not a theorem fixing every higher-derivative D-term or the absolute
energy of a supersymmetry-breaking gravitational state. At singular
strata the massless field content changes and the regular chart must be
replaced. Gravity is outside the rigid theorem's stated application.

A concrete renormalizable gauge parent for the quotient construction is
N2 SQED with two charge-one hypermultiplets. With one real electric FI
level zeta>0, one conventional component potential is

    V=2 sum_i |a+m_i|^2(|q_i|^2+|qtilde_i|^2)
       +(g^2/2)[sum_i(|q_i|^2-|qtilde_i|^2)-zeta]^2
       +2g^2|sum_i qtilde_i q_i|^2.

For equal zero masses the moment-map quotient is the smooth resolved
four-real-dimensional Higgs geometry. For example a=0, q1=sqrt(zeta),
all other q,qtilde zero gives exactly V=0. The FI level fixes a geometric
scale but remains an allowed level of the moment map. The supersymmetric
quotient metric therefore supplies neither a positive same-state vacuum
nor a cubic gravitational response. Its regular two-derivative scalar
kinetic action starts quadratically in spatial gradients.

For unequal masses one instead may choose a=-m1 at that vacuum; its
energy is still zero. At q=qtilde=0 the displayed tree potential is
g^2 zeta^2/2, but this is a broken-supersymmetry Coulomb configuration,
not the protected massless-hyper Higgs branch. Its hypermultiplet mass
conditions, quantum Coulomb metric and full stabilization must be checked
separately. This prevents transferring the theorem between those states.
SQED is used as a renormalizable gauge parent, not an all-scale UV claim.

The primary four-derivative classification explicitly allows independent
nonholomorphic full-superspace functions on Higgs, Coulomb and mixed
branches. It separately identifies a protected holomorphic Higgs term.
That classification assumes its stated no-FI massless-branch derivative
expansion and a restriction concerning superspace CS-like terms; it is
not imported as a complete classification of broken-FI higher derivatives.
It suffices to prevent identifying protection of one two-derivative
metric with absence of every N2 higher-gradient gravitational operator.

## 5. The missing attractive operator and a legitimate continuation

The inherited gravitational mechanism needs field-dependent coefficients
of both h^2 and h^4 and relaxation of their real order parameter. A
protected Higgs metric alone is a two-derivative scalar sigma model;
no authenticated theorem here identifies its moment-map level with the
coefficients of that gravitational action. Even after adding an attractive
conformal source by hand, a regular finite metric gives a quadratic local
force response. An exact shift along the real order parameter, commuting
with the physical metric and source, would force its scalar coefficient
functions to be constant; that would remove this relaxation mechanism
as well as a nonconstant U. A phase shift does not forbid a potential for
an invariant radial amplitude. The separate P1 packet treats those Ward
identities more generally.

No operational C3 or ultraviolet/infrared force pair was derived from
these N2 models, so there is no physical R to evaluate or set equal to
128pi/9. A central-charge or FI numerical equality is not that bridge.
The strongest remaining constructive task is to specify a microscopic
N2 matter/gravity or critical-sector action whose exact protected
invariant actually reduces to the attractive gravitational h^2/h^4
operator, while retaining all light fields, and then derive its positive
local-supergravity vacuum stress. Only after that action-level bridge
could global duality/charge data plausibly eliminate the allowed response
and FI/prepotential deformations. No such selecting equation was found.
