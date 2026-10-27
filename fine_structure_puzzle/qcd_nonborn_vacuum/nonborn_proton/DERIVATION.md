# Full non-Born soft response and a no-alpha pion-loop calculation

FSP-009 proton worker; parent FSP-008, base revision
`3ac0427149a2108afa8f102df4d82da33b9060c4`. Original target remains open.
This derivation precedes its bounded run. Prior Born and sea-moment results are
read-only inputs. The result below is an actual new controlled non-Born
low-energy coefficient, not a total electromagnetic proton mass.

## 1. Definitions and normalization

Let `u=e^2=4 pi alpha`. The canonical QCD current contains rational quark
charges and no e. All quantities are expanded at u=0 in massive infinite-volume
QCD with fixed renormalized MSbar quark masses and strong coupling at a common
reference scale. Use the standard on-shell Born convention, including the
non-pole Dirac term. The WLCM scalar amplitudes `t_i` are dimensionless; with
`Q=|Q_E|`, `x=Q_4/Q`, `z=Q/(2M)`, the inherited all-component formula is

    K(P)=D_u(P)/M
      =1/(32 pi^3 M^2) integral dQ^2 P(Q^2)
         integral_-1^1 dx sqrt(1-x^2)
         [-3 t_1(iQx,Q^2)+(1-x^2)t_2(iQx,Q^2)].              (1)

Here the counterterms of the full integral are not assigned to a photon shell.
The finite shell functional is defined directly from the renormalized QCD
current tensor before the local mass/strong-parameter matching insertions.

Alarcon--Hagelstein--Lensky--Pascalutsa (AHLP),
[2005.09518v2](https://arxiv.org/abs/2005.09518v2), equations (1),(6),(7), use the
same tensor basis, but amplitudes `A_i` of mass dimension -1 including u.
Their Born term is `A_1^B=(u/M)[z^2 GM^2/(z^2+x^2)-F1^2]`, whereas the
inherited `t_1^B=2[z^2 GM^2/(z^2+x^2)-F1^2]`. Thus for both amplitudes

    t_i=(2M/u) A_i.                                         (2)

This factor is checked against both Born tensors, not inferred from a plotted
polarizability. Set `a=lim_(u->0) alpha_E/u`, `b=lim_(u->0) beta_M/u`, with
the polarizabilities in natural units. AHLP equation (7) gives the full
Born-subtracted two-current low-energy response:

    t_1^NB=8 pi M [b Q^2+(a+b) nu^2]+O(q^4),
    t_2^NB=8 pi M (a+b)Q^2+O(q^4).                          (3)

These are the full-QCD polarizabilities when no EFT truncation is made.
They include all quark contraction classes. Their values are independent
physical QCD information; no Ward identity fixes them from charge or elastic
form factors. The non-Born amplitudes are analytic near zero for fixed positive
pion mass. The order `O(q^4)` is uniform in Euclidean angle on a sufficiently
small ball below the first inelastic threshold.

## 2. Inelastic and subtraction together

At imaginary energy the integrand of (1) becomes

    8 pi M Q^2 [-3b+(a+b)(1+2x^2)]+O(Q^4).

Since `integral sqrt(1-x^2)dx=pi/2` and
`integral x^2 sqrt(1-x^2)dx=pi/8`, the sharp SO(4) soft ball `0<Q<Lambda`
has

    K_NB(Lambda)=3 Lambda^4/(32 pi M) (a-b)+O(Lambda^6),
    C_NB:=lim_(Lambda->0) K_NB(Lambda)/Lambda^4
         =3(a-b)/(32 pi M).                                (4)

In the standard subtraction at nu=0 this separates into

    K_sub,NB = -3 b Lambda^4/(16 pi M)+O(Lambda^6),
    K_disp,NB=  3(a+b)Lambda^4/(32 pi M)+O(Lambda^6).          (5)

Their sum is (4). This is not another evaluation of only `t_1(0,Q^2)`, the
Fu imaginary-energy line, an elastic disconnected vertex, or the previously
imported same-loop temporal moment. Both independent responses enter.
The inelastic response supplies `a+b`; the subtraction supplies `b`.

An independent local-operator check uses the rest-frame polarizability
interaction in Euclidean signature:

    Delta M = 2 pi [alpha_E <E_E^2>-beta_M <B_E^2>].

For a free Feynman-gauge photon restricted to the same four-ball,
`<E_E^2>=<B_E^2>=(3/2) integral d^4Q/(2pi)^4`, and the latter integral is
`Lambda^4/(32pi^2)`. Dividing by uM gives (4). The relative magnetic sign
comes from Wick rotation of the electric field; replacing it by a plus sign
would give the wrong Cottingham contraction.

## 3. A genuinely computed QCD low-energy sector

The authenticated AHLP source archive contains the ancillary notebook
`anc/SupplementaryFile_UnpolarizedVVCS.nb`. It provides exact covariant
pi-N-loop static polarizabilities, not only sampled/fitted Q^2 curves. We
import exactly the assignments `AlphaE1plusBetaM1protonLO` and
`BetaM1protonLO`, with their Mathematica Greek-character names preserved in
the input file. A small non-evaluating box parser extracts only these RHSs.
It never executes the notebook, its `constants` assignment, or its saved
outputs. The numerical measured alpha in that constants cell is excluded.

For a transparent independent implementation, put `mu=m_pi/M`,
`s=sqrt(4-mu^2)`, `theta=acos(mu/2)` for `0<mu<2`, and write

    (a+b)_piN = g_A^2/(pi^3 f_pi^2 m_pi) F_S(mu),
    b_piN     = g_A^2/(pi^3 f_pi^2 m_pi) F_B(mu),
    F_S=[-2 A theta+mu s B]/(96 s^5),
    F_B=[P theta-mu s R]/(192 s^3),                         (6)

where

    A=-44+788mu^2-1500mu^4+899mu^6-215mu^8+18mu^10,
    B=406-737mu^2+304mu^4-36mu^6
      +2(mu^2-4)^2(9-35mu^2+18mu^4)log(mu),
    P=4-492mu^2+942mu^4-424mu^6+54mu^8,
    R=-127+235mu^2-54mu^4
      +(-72+418mu^2-316mu^4+54mu^6)log(mu).

The source's magnetic expression contains principal `ArcTanh` and square
roots of `mu^2-4`. Its real form in (6) follows from
`atan(mu/s)-atan((mu^2-2)/(mu s))=acos(mu/2)` on this interval.
The bounded computation compares (6) against the directly parsed source
expression at every declared mu, including the source physical ratio.
No source numerical electromagnetic coupling is used.

The small-mu expansions, also checked against AHLP Appendix B and its
ancillary HB assignments, are

    F_S=11pi/768+mu(3log(mu)/16+1/4)-507pi mu^2/2048+...,
    F_B= pi/768+mu(3log(mu)/32+21/128)-327pi mu^2/2048+...,
    F_C:=F_S-2F_B
       =3pi/256-5mu/64+147pi mu^2/2048+O(mu^3 log(mu)).     (7)

In this pi-N-loop difference the order-mu logarithm cancels. The leading
chiral singularity of the full QCD polarizability difference is protected
against analytic short-distance polarizability counterterms:

    a-b = 3g_A^2/(256pi^2 f_pi^2 m_pi)
          + less singular terms,
    C_NB^LNA=9g_A^2/(8192pi^3 M f_pi^2 m_pi).               (8)

The statement is the usual leading SU(2) chiral asymptotic at fixed nonzero
Delta-nucleon gap. It is not exact at the physical pion mass. The soft limit
in (4) is taken first; a fixed Lambda cannot be held below threshold while
m_pi goes to zero. For `Lambda=epsilon m_pi`, the corresponding leading
term is proportional to `epsilon^4 m_pi^3`, not a divergence of the full mass.

The finite source-parameter evaluation uses `M=0.93827`, `m_pi=0.13957`,
`f_pi=0.09221` GeV and `g_A=1.27` from AHLP Table I, as printed decimals.
These are imported, physically calibrated strong-sector inputs and extraction
fits, not QCD predictions in this package. They are held fixed in the local u
derivative. The calculation has no continuum lattice covariance or parameter
uncertainty model. Its digits describe a deterministic source-formula
evaluation, not physical precision.

## 4. Sea and counterterms stay explicit

The pi-N loop is a controlled low-energy contribution to the full-QCD
two-current amplitude. It is not an identification of a pion loop with one
particular microscopic sea Wick contraction, and it is not an electroquenched
observable. QCD sea effects enter the EFT coefficients and long-distance
response; a source-free numerical flavor-disconnected decomposition does not
follow from (6). The independent polarizability operators at higher chiral
order shift the full `a` and `b`; their unknown coefficients remain in (4).
AHLP's fitted `delta beta`, its empirical Baldin normalization, and Delta
transition couplings/form factors are **not imported into our loop result**.
The source explicitly fits delta beta in Section III A, so importing its final
blue curve as a no-fit prediction would be invalid.

Renormalized polarizabilities in (3) are sufficient to define the soft finite
functional. They do not fix the full ultraviolet current convolution. That
still requires the scalar and gluon matching insertions for fixed MSbar
parameters, including their finite parts, as in the inherited physical-matching
derivation. Neither the independent local polarizability contacts nor the
full electromagnetic mass contacts are set to zero by charge conservation.

## 5. Concrete remaining leaf

The new exact reduction isolates the next low-energy leaf as the full-QCD
`(alpha_E-beta_M)/u` on the common calibration path. The bounded calculation
evaluates its pi-N-loop sector and leading chiral singularity. To determine
the entire non-Born mass response one needs, in addition, the full renormalized
Born-subtracted `t_1(iQx,Q^2),t_2(iQx,Q^2)` over all Q and x (or equivalent
inelastic structure functions together with an independently determined
subtraction function), full sea contraction coverage and the ultraviolet
matching insertions. The inspected lattice sources do not jointly supply
those data. This package leaves that data route open with this precise input
condition. It does not determine `D_u/M`, `A_rho`, `R(alpha)`, or alpha.
