# P0 raw action: quantum matrix gravity

Author root. Base431f22bd6; criteria89bf113b0. Natural units; signature
(-+++). Symbols in this packet are local: G_{mu nu} is the emergent
metric, not Newton's constant; ell is the observation radius; r_* the
matrix noncommutativity parameter. Nothing is calibrated to the target.

## 1. A genuinely common microscopic proposal

Use the IKKT action, in the normalization of2601.08031v1 Eq1.1,

    S=Tr([T_a,T_b][T^a,T^b]+psi_bar Gamma^a[T_a,psi]), a=0,...,9.

T_a are Hermitian matrices and psi a Majorana-Weyl matrix spinor.
The proposed sector has a covariant quantum spacetime background with
compact fuzzy transverse K and an internal higher-spin bundle. Maximal
supersymmetry cancels the first three propagator orders of the one-loop
expansion. This really is one matrix functional generating gravitational
and vacuum terms. It is not three unrelated coefficients renamed as one.
The sector, quantum integration contour and dominant background are
additional physical obligations; they are not uniquely fixed here.

The exact one-loop coefficient quoted in2303.08012v1 Eqs6.30-32 and
7.22-24 is

    c_K^2=(pi^2/8)sum_(Lambda,s)
               (2s+1) C_Lambda^2/(mu_Lambda^2+m_s^2/m_K^2),
    G_N^-1=(2c_K^2/pi^3)rho^-2 m_K^2.

The basic brane formula omits s. The fuzzy spectrum makes the sum finite.
The same functional has a vacuum term proportional to the separate sum
sum V4,Lambda/mu_Lambda^4 (Eq6.17) and classical internal-field energy.
The K-radius stationarity equation also contains background torsion
(Eqs7.48-53). It is not a Ward equation fixing those spectral sums to
one universal invariant. This is a substantive common-scale mechanism,
but neither a spectrum nor the local MOND C3 is selected by this formula.

The constant-rho, omitted-axion two-derivative truncation in2601.08031v1
Eq3.1 includes the Einstein-Hilbert action and thus a short-distance
GR coefficient. Calling that operational C2 still requires the actual
matter response and the retained dilaton/extra modes. In a true ordinary
Einstein limit with no extra sourced mode, C2=1/(8pi G_N). The published
linear source solution tests that limit, with the qualifications below.

## 2. Vacuum density must be varied through the frame

Equations2.40 and3.12 of2601.08031v1 specify

    rho^2=sqrt|G|/rho_M=rho_M det(e^{a mu}),
    S_v=-int d4x rho_M rho^-2 V0(r_*,m_K).

Here rho_M is the fixed symplectic density. It is incorrect either to
set this term to an ordinary constant cosmological action or to declare
it non-gravitating merely because rho_M is fixed. The dilaton depends
on the dynamical frame. At fixed V0 and rho_M,

    delta ln(rho^2)=e_(a mu) delta e^{a mu},
    delta S_v=+int rho_M rho^-2 V0 e_(a mu) delta e^{a mu}.

This reproduces the displayed Eq3.13. There is a sign issue in the next
displayed equation which must be preserved, not silently repaired.
With the source's Eq3.9 convention

    delta S_m=-(1/2)int sqrt|G| T_(mu nu) delta G^{mu nu},

the same term can be written S_v=-int rho_M^2 V0/sqrt|G|. Direct variation
then gives

    T_v,(mu nu)=+rho^-4 V0 G_(mu nu),
    epsilon_v=-rho^-4 V0, p_v=+rho^-4 V0.

The printed Eq3.14 instead adds -rho^-4 V0 G_(mu nu) to the Einstein
equation. In the simplified frame equation the same mismatch follows:
Eq3.13 adds +L G to the trace-reversed variation, so solving and reversing
the trace gives +L G on the Einstein right-hand side, L=rho^-4 V0.
Both signs occur in the versioned PDF, not only the HTML conversion.

This is an audit of the isolated displayed functional at fixed V0 and
symplectic measure. Divergence-free frame constraints, the definition of
the anharmonicity tensor, derivatives of rho, and K/background variations
must be restored for the full solution. They cannot justify changing
the sign of this isolated variation without an additional term or
convention. No claim that the entire matrix theory has a negative
vacuum follows. Positive physical epsilon cannot simply be identified
with positive V0 from these displays. Moreover the source's cosmic
equation contains background T[C], not just this term.

## 3. Derive the point-mass force, rather than read off a halo label

Take the approximate static scalar Green sector in2601.08031v1
Eqs3.34-37. Work in locally normalized spatial coordinates, hold the
background fixed, omit the displayed higher-spin corrections and set
k=sqrt(3)m. The density entering its Poisson equation has the shape

    rho_eff=M delta3(x)+M k^2 cos(k ell)/(4pi ell).

The actual metric convention and trace-reversed potential can affect
the overall Newtonian prefactor; normalize it by the short-distance
point-source force and call that coefficient G_force. The radial
profile is fixed independently of that prefactor. Indeed,

    M_eff(ell)/M=1+k^2 int_0^ell s cos(ks) ds
                 =cos(k ell)+k ell sin(k ell),
    Phi(ell)=-G_force M cos(k ell)/ell,
    g_r(ell)=G_force M[cos(k ell)+k ell sin(k ell)]/ell^2.

The distributional identity is
Delta[cos(k ell)/ell]=-k^2 cos(k ell)/ell-4pi delta3(x).
Choose no independently excited homogeneous halo mode. The regular
solution retains Phi=-G_force M/ell+O(ell) near the source. At small
k ell the signed radial force is

    g_r=G_force M/ell^2+(G_force M k^2)/2+O(M k^4 ell^2).

On any attractive part of this fixed-background linear branch it is
proportional to M. More generally linearity enforces g[lambda rho]=
lambda g[rho] for the same boundary sector. A local positive cubic
MOND action instead has g[lambda rho]~sqrt(lambda)g[rho] in its deep
regime and g~sqrt(G M a0)/ell outside a spherical source. Thus this
published halo is not an operational deep-MOND C3, even in a radius
interval with a visually flat rotation curve. Fitting m separately for
each source would abandon the fixed common background and is not done.

The argument is restricted to the displayed linear regime. Dilaton,
higher-spin or genuinely nonlinear solutions may change the mass law.
They require a new calculation, not exclusion by linearization.

## 4. A real IR repair exists algebraically, but is not a health proof

The source's Eq4.46 has a single commuting-mode frequency polynomial

    p(t,x)=(x-t)(t-x/5+u)+v00+v01 t,
    t=omega^2, x=k_phys^2>=0, u=m^2>0.

The simplification to one scalar coefficient is explicit: the actual
V coefficients can mix higher-spin components. Rewrite

    p=-t^2+A t+B,
    A=6x/5+v01-u,
    B=ux-x^2/5+v00.

For two strictly positive distinct real roots for every x>=0, sufficient
conditions (and necessary within this sign-restricted scalar model) are

    v00<-5u^2/4,  v01>u+2sqrt(-v00).

Proof: the root product is x^2/5-ux-v00, minimized at x=5u/2 with
value -5u^2/4-v00. Their sum is A. The discriminant is

    A^2+4B=16x^2/25+(12v01+8u)x/5+(v01-u)^2+4v00.

Once the sum is positive at x=0, its discriminant is minimized there;
the stated second inequality gives a strictly positive minimum. This
checks that a frequency repair is possible; it does not calculate v00
or v01 from a selected background, establish positive residues of all
physical modes, control other components or prove nonlinear stability.
No illustrative parameters from the source are used as physical inputs.
The uncured polynomial alone has an infrared tachyon. It is equally
incorrect to call that a universal matrix-model no-go or to declare
complete health merely because a repair polynomial can be written.

## 5. First unsolved implication

A retained, quantum-controlled background must simultaneously determine
the fuzzy spectrum, rho and V0, and yield a nonlinear attractive force
with the correct source-mass dependence and Newtonian calibration.
Only then can one compute epsilon C3^2/C2^3. Section5 of2601.08031v1
itself leaves cosmic prediction and the complete dilaton/vacuum problem
unresolved. This model is a credible example of a common microscopic
functional, not a derivation of128pi/9. It remains a deferred nonlinear
route, with a precise mass-scaling and stress test for any claimed bridge.
