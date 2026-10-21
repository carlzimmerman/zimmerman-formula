# Flux geometry: a fixed radion charge and an exact scale obstruction

2026-10-20. Base431f22bd6; criteria-only commit89bf113b0.
**The healthy microscopic xi=1/4 and complete formal-bridge goal remains
open.** This is a concrete common-action test, not a new quantum UV
completion, flux scan or universal compactification no-go. No measured
scale, flux integer or target selects a coefficient. Sources and exact
version/normalization qualifications are in SOURCES_FLUX.md.
Use c=hbar=1, signature -+++++ in six dimensions and -+++ in four.
The compact sphere radius is R; it is not the amplitude invariant R_amp.

## 1. One higher-dimensional action, flux and canonical radion

Consider the six-dimensional Einstein--Maxwell action

    S6=int sqrt(-G)[M6^4 R6/2-Lambda6-F_AB F^AB/(4g_e6^2)],
    M6>0, Lambda6>0, g_e6^2>0.

Here the gauge connection has mass dimension one and [g_e6]=-1.
Choose its electric charge unit so that the fixed magnetic flux is

    F=Q sin(theta)dtheta wedge dvarphi,
    int_S2 F=4pi Q=2pi N, N integer, Q=N/2.

No integer is chosen to reproduce a target. This is a two-form magnetic
flux on the internal sphere, not the old four-dimensional top-form or
electric BI construction. Introduce the Einstein-frame ansatz

    ds6^2=e^(-psi)g_mu nu dx^mu dx^nu+R0^2 e^psi dOmega2^2,
    M4^2=4pi R0^2 M6^4,       chi=M4 psi.

Keeping the sphere-symmetric zero modes and fixed flux, integration of
the internal curvature and Maxwell energy, with the metric boundary term
removed, gives

    S4=int sqrt(-g)[M4^2 R4/2-(partial chi)^2/2-V(psi)],
    V=A e^(-psi)-B e^(-2psi)+C e^(-3psi),
    A=4pi R0^2 Lambda6,
    B=4pi M6^4=M4^2/R0^2,
    C=2pi Q^2/(g_e6^2 R0^2)>0.

All of A,B,C have mass dimension four, while psi is dimensionless.
For example sqrt(-G)=R0^2 e^(-psi)sqrt(-g)sqrt(g_Omega), and
F_AB F^AB=2Q^2 R0^-4 e^(-2psi), which fixes C. The radion is an
ordinary canonical propagating field; it is not an auxiliary modulus.
Other gauge/KK modes are accounted for below rather than discarded as
a health argument. This unwarped scalar sector and its linear response
are the declared reduction, not a proof of an arbitrary nonlinear
localized-source truncation.

## 2. Actual positive vacuum and its exact retained mass

Let x=e^(-psi)>0 and Delta=sqrt(B^2-3AC). The extrema satisfy

    V_x=A-2Bx+3Cx^2=0,
    x_+/-=(B+/-Delta)/(3C).

For Delta>0, x_+ is a local minimum and x_- a local maximum, since
V_chi chi=+/-2Delta x^2/M4^2 there. At the minimum,

    V0=x_+^2(B-2C x_+),
    m_rad^2=2Delta x_+^2/M4^2,
    H_E^2=V0/(3M4^2).

A positive locally stabilized de Sitter branch therefore has
0<Delta<B/2, equivalently 1/4<AC/B^2<1/3. At Delta=B/2 the minimum
is Minkowski; at Delta=0 the two extrema merge. V0 is the varied
same-state vacuum energy: T_mu nu=-V0 g_mu nu at the constant minimum.
The positive height here uses an explicit positive higher-dimensional
Lambda6; it is not a quantum calculation fixing its absolute value.

One can choose the fiducial R0 and external constant-frame normalization
at the actual vacuum, so psi0=0 and R0=R, M4^2=4pi R^2M6^4. This is a
coordinate/reference convention, not a change of flux or physical state.
Then the exact background and mass equations become

    A=2B-3C, V0=B-2C,
    M4^2 m_rad^2=-2B+6C, 3M4^2 H^2=B-2C.

Consequently

    m_rad^2+9H^2=B/M4^2=R^-2=m_KK,spin2,l=1^2/2.       (*)

The last equality uses the physical first massive spin-two KK mass,
not merely a conventionally named KK scale. This common-action identity
is an exact discriminator; it is not an amplitude selector.

## 3. The full bosonic linear vacuum spectrum and a source-root caveat

The following specializes and diagonalizes Brown--Dahlen's harmonic,
constraint-reduced blocks for one S2, p=4,q=2. This is not claimed as a
fresh derivation of every six-dimensional Euler component. Let c_F be
the flux-density variable of that source's action convention, and put

    c_F^2=2Q^2/(g_e6^2 M6^4 R^4)=4 C/M4^2,
    c_F^2=2/R^2-6H^2,
    mu=m_rad^2=-2/R^2+3c_F^2/2,
    k_l^2=l(l+1)/R^2.

The strictly stable positive-vacuum range is
4/3<c_F^2 R^2<2, hence mu>0 and 0<H^2R^2<1/9.
The retained l=0 fields are the massless graviton, Maxwell photon and
canonical radion of mass squared mu. The sphere's Killing sector gives
the massless SU(2) vectors; together with the photon these are not
additional universally charged gravitational scalars.

For l>=2 the physical coupled scalar block has trace and determinant

    tr_S=2k_l^2+mu,
    det_S=k_l^2(k_l^2-2/R^2).

Direct diagonalization gives

    m_S,+/-^2=k_l^2+mu/2
                  +/-sqrt(mu^2/4+(3/2)c_F^2 k_l^2).

Both roots are positive: trace and determinant are positive, and the
displayed discriminant is real. At l=1 one of the two formal modes is
gauge/non-dynamical; the physical scalar has
m_S,l1^2=2/R^2+3c_F^2/2=5/R^2-9H^2>0. At l=0 the flux perturbation
does not add a second scalar at fixed conserved flux.

For transverse vector harmonics the source's displayed matrix is

    M_V=k_l^2 1+matrix[-6H^2, k_l^2; c_F^2, 0].

Its literal eigenvalues, obtained here from that matrix, are

    m_V,+/-^2=k_l^2-3H^2+/-sqrt(9H^4+c_F^2 k_l^2),
    tr_V=2k_l^2-6H^2,
    det_V=k_l^2(k_l^2-2/R^2).

Thus both roots are positive for l>=2. For l=1 they are zero and
4/R^2-6H^2>0, with the zero modes precisely the Killing vectors.
This trace contains -3H^2 in each root. The source's printed vector
root formula instead has +3H^2, inconsistent with its preceding matrix
and its following Killing-zero-mode statement. The same discrepancy
appears in the checked PDF, not just converted HTML. We use the displayed
block and its explicit determinant/zero-mode checks, not that root formula.
No other source correction is inferred.

The spin-two tower has physical m_T,l^2=k_l^2; its l>=1 modes satisfy
the de Sitter Higuchi bound m_T,l^2>=2H^2. The apparent curvature term
in its wave equation is not an additional tachyonic mass. S2 has no
additional scalar or harmonic-one-form zero modes. These scalar, vector
and tensor blocks exhaust the bosonic linear Einstein--Maxwell harmonic
sectors in the specified unwarped vacuum, with the inherited ordinary
Einstein/Maxwell signs and gauge constraints. The q=2 spectrum is therefore
classically perturbatively stable on the volume-minimum branch.
This is not a nonlinear, quantum, cutoff or all-matter stability theorem,
nor a microscopic completion of six-dimensional Einstein gravity.

## 4. A geometric attractive matter charge, with its actual force

Specify matter as neutral massive six-dimensional particles with no
internal momentum. Equivalently, a minimally coupled massive scalar's
constant internal harmonic has a four-dimensional mass squared
m0^2 e^(-psi), after its kinetic term is canonically normalized.
The particle action fixes, rather than assigns, its radion dependence:

    S_particle=-m0 int e^(-psi/2)ds_g,
    A_m(chi)=e^(-chi/(2M4)), alpha=d log A_m/dchi=-1/(2M4).

This is universal for this specified sector. Wrapped objects, KK momentum
states or matter with internal stress need a different mass/charge map;
it is not universality over an unspecified complete microscopic spectrum.
Massless gauge modes are unsourced by the neutral zero-internal-charge
sector. A localized internal source also excites massive KK harmonics;
its distant zero-mode force requires r>>R.

Around the vacuum A_m(0)=1, the source-dependent, weak, subcurvature
equations are

    Delta Phi_E=rho/(2M4^2),
    (Delta-m_rad^2)chi=alpha rho,
    Phi_phys=Phi_E+alpha chi, Psi_phys=Psi_E-alpha chi,
    G_T=1/(8pi M4^2), G_S=alpha^2/(4pi)=G_T/2.

The Einstein-frame potentials agree in this linear zero-mode sector.
For a positive point mass m_src,

    Phi_phys=-[G_T+G_S e^(-m_rad r)]m_src/r,
    g_source=m_src[G_T+G_S(1+m_rad r)e^(-m_rad r)]/r^2.

The scalar force is attractive and its canonical charge is geometric.
But it is Yukawa, not the square-root-in-source MOND law. The potential
ratio tends formally to 1/3 and the force coefficient to 3G_T/2 only
if r<<m_rad^-1 as well as r>>R,r<<H^-1. They are not automatically
an actually calibrated ultraviolet Newton/PPN regime.
At linear order a valid static elimination gives instead the nonlocal
source energy

    E_on-shell,radion=-(alpha^2/2) int rho (-Delta+m_rad^2)^(-1)rho.

It does not give a local positive |grad Phi|^3 functional. In formal
n>=2 spatial dimensions the scalar equation integrates as

    Omega_(n-1) r^(n-1)chi'(r)
       =alpha M_enclosed(r)+m_rad^2 int_|x|<r chi d^n x.

There is no conserved exterior scalar flux at nonzero mass. When the
mass term is negligible the field scales as r^(-(n-1)), not the cubic
Gauss exponent r^(-(n-1)/2). This n-dimensional statement is a flux
diagnostic, not a claim to have changed the compactification dimension.

## 5. A quantitative obstruction to the required force window

Identity (*) implies the exact bound

    min(m_rad^-1,H^-1)<=sqrt(10) R.

Indeed m_rad^2+9H^2<=10 max(m_rad,H)^2. Thus a light unscreened
radion and a low-curvature background cannot both be parametrically
separated from the KK scale. A few-radius interval is not excluded by
this inequality, but does not give the required parametric four-dimensional
quasistatic reduction.

There is a useful directly sourced version. Suppose r/R>=L and Hr<=eps,
where L>3eps>0. Then

    m_rad r>=sqrt(L^2-9eps^2),
    (g_radion/g_tensor)<=
       [1+sqrt(L^2-9eps^2)]exp[-sqrt(L^2-9eps^2)]/2.

The second line uses that (1+x)e^-x decreases for positive x. On a
parametrically four-dimensional subcurvature domain L>>1,eps<<1, the
radion correction is exponentially small; the other massive KK modes
also require their usual low-energy suppression. The controlled weak
Newton response is tensor dominated, with G_T. Near Minkowski, m_rad
is of order R^-1. Making the radion mass small instead approaches
H=1/(3R), where there is no broad subcurvature four-dimensional window.

## 6. The critical endpoint is not a MOND auxiliary branch

At Delta=0, V_psi=V_psi psi=0 but

    V_psi psi psi=-6V0, V_chi chi chi=-6V0/M4^3 !=0.

It is a homogeneous stationary inflection, not a potential minimum.
The radion still has its ordinary canonical gradient/time kinetic term;
one cannot integrate out this massless propagating field algebraically.
Its physical source is the matter trace above, not an installed h^2
spurion. Identifying a spinodal square root with a local gravitational
cubic would discard both its source equation and its retained gradients.
The critical point also has H=1/(3R), independently of that failure.

The common action genuinely ties Newton normalization, a geometric scalar
charge, flux stabilization and positive vacuum. The executed test fails
before a numerical ratio: there is no operational C3 or MOND regime,
so R_amp=epsilon C3^2/C2^3 is not defined here as the requested invariant.
No acceleration is identified with H,R^-1 or a membrane tension by fiat.
An additional higher-curvature, warped or microscopic sector could change
the response and scale identity, but must then derive its sourced branch,
retained spectrum and same-state stress anew. The present classical toy
model does not force128pi/9 and does not close those wider routes.
