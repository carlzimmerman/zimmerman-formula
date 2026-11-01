# Leading soft/light completion of the photino loss budget

This addendum supplies channels not covered by the separate heavy-loop
dimension-seven majorant. It preserves the earlier frozen report, which
correctly called the Goldstino width partial before these and the hard
matching bound existed. The result below is a leading perturbative rigid
EFT statement, not an all-order total rate or a cosmological production
claim. The residual photon is not identified with observed EM; see
SCOPE_ADDENDUM.md.

## Actual phase law and canonical normalization

X and B have R charge2, A charge0; their Weyl fermions have charges1,1,-1,
and all gauginos have charge1. The massless Goldstino projection is in
X/B and has charge1. Write theta=argT, theta=pi/a with a=sqrt(2)v at
leading weak coupling. Under R rotation theta shifts by2alpha.
Consequently both the finite photino mass coefficient and its Ward dipole
carry exp(-i theta). This is fixed by the actual current, not a postulated
matter portal. In a linear fermion basis the leading terms are

    -m exp(-i theta) chi chi/2 + h.c.,
    -m exp(-i theta) G sigma^{mu nu}chi F_mu nu/(sqrt(2)Ftot) + h.c.

The mass expansion supplies a pseudoscalar chi-chi-pi vertex of magnitude
y=m/a and a two-phase contact. The dipole expansion supplies a
pi-G-chi-photon contact of magnitude1/a times the original dipole.
A phase-dependent fermion redefinition moves these terms into derivative
current vertices; it cannot remove their on-shell sum. The canonical
Goldstino has no tree phase Yukawa. Finite metric/current corrections are
higher-order perturbative matching corrections to this leading result;
we have not computed a new finite-momentum triangle here.

## Direct phase radiation: no soft pole

Use four-component dipole amplitude coefficient
kappa=m/(2sqrt(2)Ftot), so M2=kappa ubar_G [kslash,epsslash]u_chi,
and the authenticated two-body width is
Gamma2=kappa² m³/(2pi)=m⁵/(16pi Ftot²).
In the initial rest frame, for emitted massless phase momentum q,

    (pslash-qslash+m) gamma5 u(p)=-qslash gamma5 u(p).

The internal-chi denominator is -2p.q=-2m q0. Thus the norm of the
external-leg insertion is at most y/m=1/a: qslash has operator norm2q0.
There is no soft1/q0 divergence. The contact and this leg amplitude
each have magnitude at most4 kappa m²/a for any external spin/polarization:
use ||u||=sqrt(2E), E_G<=m/2, E_gamma<=m/2, and
||[kslash,epsslash]||<=4E_gamma<=2m. Summing the four final
spin/polarization choices and averaging the initial spin bounds the
squared sum by256 kappa² m⁴/a². The massless integrated three-body
phase space is m²/(256pi³). Therefore

    Gamma_direct(G gamma pi)/Gamma2 <= m²/(pi² a²).

This is a deliberately loose norm bound, not an assertion of vanishing
bremsstrahlung. At the conditional1MeV,e=.003 benchmark it is8.48109e-27.
On-shell radial emission is closed: mrad/mchi is about499.

## Anomaly photon splitting and interference

The independently authenticated microscopic anomaly convention is

    L = -5 g1² theta F1 Ftilde1/(32pi²)
      = ga pi F1 Ftilde1/4,
    |ga|=5g1²/(8pi² a).

The coefficient5 follows the adjoint gaugino and the two adjoint Weyl
charges1,-1,+1. Its sign is immaterial for a bound. This allows
chi -> G gamma* -> G gamma pi and must not be omitted. The apparent
massless photon pole is removed by the derivative vertex and its
transverse current, as can be seen without a collinear approximation:

* For invariant virtual mass squared s, a transverse vector has
  Gamma(gamma_s -> gamma pi)=ga² s^(3/2)/(96pi).
  Equivalently Im Sigma_T(s)=ga² s²/(96pi), so the propagator-squared
  s^(-2) is canceled.
* The dipole trace gives
  Gamma(chi -> G gamma_s)/Gamma2=(1-r)²(1+r/2), r=s/m².
  It follows from the spin sum4(m²-s)(2m²+s), normalized to8m⁴
  at s=0, and the two-body momentum factor1-r.
* Spectral factorization gives
  dGamma_anom/ds=Gamma(chi -> G gamma_s) ga²/(96pi²).
  The integral of(1-r)²(1+r/2) from0to1 is3/8.

Hence the anomaly-only contribution is exactly, at this EFT order,

    Gamma_anom/Gamma2=ga² m²/(256pi²).

It is2.26252e-43 at the benchmark. The same final state's interference
is retained conservatively by Cauchy--Schwarz:

    Gamma(G gamma pi)/Gamma2
       <= [sqrt(m²/(pi²a²))+sqrt(ga²m²/(256pi²))]²
       =8.48109110e-27.

This uses leading g1=g at the matching point; finite threshold corrections
and finite canonical-metric normalization change its tiny value within
the declared perturbative order. Further phase radiation has additional
1/a vertices and phase-space suppression, with the same soft cancellation;
it is higher order in m²/a². No all-order resummation is claimed.

## Allowed light-Goldstino-exchange transition

The C-allowed channel

    chi1 -> gamma1 + G* -> gamma1 + lambda_a + gauge_a

exists for a=SU3,SU2. It is a light nonlocal exchange and is **not**
included by a hard heavy-loop dimension-seven coefficient. Both vertices
are the actual Ward dipoles, kappa1=m/(2sqrt2Ftot),
kappa_a=ma/(2sqrt2Ftot). The virtual Goldstino has q²>=ma²,
so it never reaches its massless pole in this channel.

A conservative bound is obtained from two dipole-commutator norms<=2m,
the propagator norm<=2m/ma², external spinor product<=2m, and an
additional factor2 for the Majorana conjugate routing. The amplitude is
at most32 kappa1 kappa_a m⁴/ma². There are eight final spin/polarization
choices after the initial spin average and da color states. Using the
massless phase-space upper bound (which overestimates a massive ma)
gives

    Gamma_a/Gamma2 <= [4 da/(pi² ra²)] (m²/Ftot)²,
    ra=ma/m, d3=8, d2=3.

The finite-F pole masses give r3=.41494878686,r2=.60081557937.
The summed bound is6.31257e-39. The U1 final gaugino has the initial
mass and no available phase space. Subsequent nonabelian-gaugino decays
do not increase the primary photino loss rate already counted here.

## Other low-order channels and a cold-gas collision check

The exact perturbative C selection forbids chi->G+phase/radial and
chi->3G, and forbids the one-nonabelian-field-strength transition.
Three nonabelian gauginos are kinematically closed by3m3/m=1.24484636.
The singlet radial cannot be emitted on shell. A color-adjoint particle
alone is not a gauge-invariant final state. The first hard two-gauge-boson
transition is treated by the separate heavy-loop majorant. Additional
photons or Goldstino pairs require more Ward vertices or higher-dimension
operators. The expansion parameter m²/Ftot=1.68632e-20 is tiny; these
are higher perturbative orders, not an uncomputed order-one light decay.

For the collisionless-state question, the same actual mass phase law
fixes chi chi -> pi pi. At zero initial velocity, each t/u fermion
exchange amplitude is bounded by2m²/a² and the contact by2m²/a².
Off-shell radial exchange adds at most
8|kappa_s|m⁴/[a²(mrad²-4m²)], kappa_s=dlnm/ds. The spin average and
identical-final-phase factor therefore give

    sigma v_rel <= [6+8|kappa_s|m²/(mrad²-4m²)]² m²/(64pi a⁴).

The benchmark bound is1.25453e-45GeV^(-2). At the explicitly specified
local rho=.3GeV/cm³ it gives n sigma v<=2.89175e-84GeV, only
5.11154e-40 of the Ward decay rate. This is a leading threshold vacuum
bound, not a finite-temperature average. Tiny velocity .001 gives small
NR corrections, far below the hierarchy. Direct annihilation through
additional Ward vertices is more suppressed; an independently bounded
heavy multipole can separately bound its crossed annihilation channel.
No ambient thermal scattering history or production mechanism is inferred.

## Numerical evidence and resulting scope

`run_soft` evaluates these analytic formulas and current finite-F mass
ratios. Four checks pass; measured RSS11.3MB, one numerical thread,
30s wall/25s CPU caps. Its v2 manifest hashes exact inputs/results.
The dominant soft correction is at most8.5e-27 of Gamma2; the leading
light-Goldstino-exchange correction is below6.4e-39. They cannot change
the benchmark retained leading lifetime when combined with the separate
approximately1.07%-of-Gamma2 hard-transition upper bound. This closes
the named leading soft/light omission; it does not promote the result to
an all-order total lifetime, UV/gravitational completion, photon-line
phenomenology, abundance or production calculation.
