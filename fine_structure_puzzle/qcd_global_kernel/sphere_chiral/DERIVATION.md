# Global pion determinant on the round four-sphere

FSP-008, 2026-10-19. This is a new one-point/global calculation in the
declared one-loop low-energy pion sector. It is not a determination of
the full QCD sphere functional, proton mass, or fine-structure constant.

## 1. Action, state, and one common subtraction

On the smooth Euclidean round S4 of radius 1/H, let R=12H² and
V=8π²/(3H⁴). The regular Euclidean scalar functional includes every
harmonic, including l=0. A real pion of mass M>0 has quadratic operator

    L=-∇²+M²+ξR,     W=(1/2) log det L,
    λ_l/H²=l(l+3)+z+12ξ,     z=M²/H²,
    d_l=(l+1)(l+2)(2l+3)/6,     l=0,1,... .                 (1)

The spectrum and volume are authenticated in Kluth--Litim,
arXiv:1910.00543v2, Table 4 and (10),(24),(83). The minimal LO chiral
action fixes ξ=0, rather than the conformal value 1/6. The pion action,
charge convention and higher curvature matching constants are inherited
from the independently reviewed FSP-007 source packet. There are one
neutral and TWO real charged degrees of freedom. We do not add a
second complex-scalar multiplicity.

For x=H²t define

    Kξ(x)=exp(-12ξx) Σ_l d_l exp[-x l(l+3)],
    k0=1/6,  k1(ξ)=1/3-2ξ,
    k2(ξ)=29/90-4ξ+12ξ²,
    Bξ(x)=Kξ(x)-k0/x²-k1(ξ)/x-k2(ξ).                       (2)

The following fixed, mass-dependent decoupling prescription is used for
every radius and every charge. It subtracts the complete proper-time
contributions of the first three local heat coefficients with the SAME
mass in their exponential:

    Wdec(z,ξ)=-(1/2) ∫_0^∞ dx exp(-zx) Bξ(x)/x.             (3)

At x→0, Bξ=O(x); at infinity the integral converges when z>0 and
z+12ξ>0. No H-dependent fit or linear-H counterterm is introduced.
Equation (3) fixes finite local terms through curvature squared; it is
not an assertion that QCD's independently matched gravitational local
terms vanish. Their general form is ∫√g[c0(u)+c1(u)R+c2(u)R²], with
u=e². The prescription is a declared matter contribution to which those
terms can be added in another common matching scheme. On round S4 they
give a constant, H², and zero one-point contribution respectively at
fixed parameters. They cannot shift the linear-H projection. Independent
dimension-six gravity matching can shift an H⁶ coefficient. No total
gravitational-EFT coefficient is inferred from a pion determinant.

## 2. Direct metric differentiation and an exact spectral answer

All M, ξ and matched parameters are FIXED in the metric derivative:

    ρdec=-H∂_H Wdec/(4V)=z∂_z Wdec/(2V)
         =3H⁴ Ψ(z,ξ)/(32π²),
    Iξ(z)=∫_0^∞ dx exp(-zx) Bξ(x),     Ψ=z Iξ(z).           (4)

This differentiates the global functional itself. It does not substitute
q=H in a flat-space two-point form factor. Metric contacts and the
Gaussian measure are included by defining W as the determinant of the
covariant operator in (1), with the fixed subtraction (3).

Here is an absolutely convergent representation of (4). Set w=z+12ξ,
ν=sqrt(9/4-w), and use the real continuation through imaginary ν:

    S(w)=Σ_(l=0)^∞ (2l+3)/[6(l+1)(l+2)(l(l+3)+w)],
    Iξ(z)=(w-2)(1-2γ-log z)/6+(w-2)² S(w)
                       +2/9-2ξ-k2(ξ)/z                    (5)

or equivalently

    Iξ(z)=(w-2)/6 [ψ(3/2+ν)+ψ(3/2-ν)-log z]
                       +2/9-2ξ-k2(ξ)/z.                  (6)

The summand in (5) is positive for w>0 and O(l^-3), so this is also a
convergent finite-radius spectral answer, not a formal divergent sum.
For w=2 the multiplied S term vanishes; the formula is continuous.

One derivation starts from n=l+3/2 and d_l=(n³-n/4)/3. The fictitious
n=1/2 term is identically zero. Resolvent subtraction at w=2 gives the
exact identity

    d/(λ+w)=d/(λ+2)-(w-2)d/(λ+2)²
               +(w-2)²d/[(λ+2)²(λ+w)],                   (7)

where λ=l(l+3). The final sum is S(w). Partial fractions and the
convergent digamma difference give

    (w-2) S(w)=[ψ(3/2+ν)+ψ(3/2-ν)-(1-2γ)]/6.

Keeping the local heat subtractions fixes the remaining terms in (5).
For example, analytic proper-time regularization of the local pieces
uses Γ(ε-1)z^(1-ε), Γ(ε)z^-ε, and 1/z. Their finite parts give log z,
the constant 2/9-2ξ, and -k2(ξ)/z. Independent heat integration checks
these normalization and finite-part constants, rather than assuming a
zeta subtraction agrees automatically. Another exact representation is

    Wdec(z,ξ)=-(1/2)∫_z^∞ Iξ(v) dv,                         (8)

whose convergence follows from Iξ(v)=O(v^-2). Thus the same spectral
answer determines the full finite-radius W and its metric derivative.

## 3. Low-curvature result and the linear-H projection

Deriving the scalar heat coefficients directly by half-integer
Euler--Maclaurin/Hurwitz-zeta expansion gives

    K0(x)=1/(6x²)+1/(3x)+29/90
              +37x/189+149x²/1890+179x³/10395+...,
    k3(ξ)=37/189-58ξ/15+24ξ²-48ξ³.                         (9)

The first coefficients also agree with Kluth--Litim (88). Its expansion
is asymptotic, not a convergent Taylor series; the executable uses only
a short early-time segment and reports its numerical rather than
interval-certified status. For fixed positive M, bounded ξ and H→0,

    Wdec=-k3(ξ)H²/(2M²)+O(H⁴/M⁴),
    ρdec=3k3(ξ)H⁶/(32π²M²)+O(H⁸/M⁴).                    (10)

For ONE minimal real pion this is the concrete new homogeneous response

    ρdec=37H⁶/(2016π²M²)+O(H⁸/M⁴).                       (11)

The asymptotic result is analytic heat-kernel reasoning at fixed mass,
not an extrapolation of a few computed radii. It proves A_pi=lim ρdec/H=0
for this specified determinant contribution. A nonzero finite proton
normalizer does not change that result. It neither proves that full QCD
has A_rho=0 nor evaluates the full ratio A_rho/m_p³. The unknown global
QCD functional is not exhausted by a free pion determinant.

## 4. Calculated charge dependence, with independent matching retained

Write u=e²=4πα, M0²=M², Mc²=M²+2uC/F², holding M,F,C fixed. No observed
pion splitting, alpha, proton mass or cosmic scale is used to set these
constants. At leading chiral order ξ0=ξc=0 and the exact global
mass-shift component is

    ρ_pi,mass(H,u)=3H⁴/(32π²)
          [Ψ(M²/H²,0)+2Ψ((M²+2uC/F²)/H²,0)].             (12)

Its low-curvature expansion is

    ρ_pi,mass=37H⁶/(2016π²)[1/M²+2/(M²+2uC/F²)]+O(H⁸).

At y=2uC/(F²M²), the ratio of this leading H⁶ coefficient to its
zero-charge value is [1+2/(1+y)]/3. The executable also evaluates the
FULL finite-radius ratio from (12); at finite H it need not equal this
asymptotic expression. These are dimensionless conditional functions,
not fitted predictions of C or alpha.

The independently matched electromagnetic curvature operator k15 gives
the isolated higher-order quadratic insertion ξc=-2u k15^r. It can be
kept in (4)--(6), provided the spectrum remains positive. At u=0 its
additional and mass derivatives are

    ∂_u ρ_pi |_(selected pieces)
       =3H⁴/(16π²)[(2C/(F²H²)) Ψ_z(z,0)-2k15^r Ψ_ξ(z,0)],
    ∂_u[ρ_pi/H⁶] -> 3/(16π²)
            [116 k15^r/(15M²)-74C/(189F²M⁴)],             (13)
    ∂_α=4π ∂_u.

The factor TWO for charged real species is already in (13). The k15
part is scale dependent until the corresponding photon/chiral loops
are included. Strong curvature operators l11,l12,l13, interacting pion
loops, inclusive photons and nonpionic QCD matching also remain. Keeping
ξc exactly in a quadratic determinant resums a selected operator; it
does not claim an all-orders chiral/QED prediction. At physical masses
even the full H⁶ coefficient needs higher-order and heavy-sector terms.

## 5. Uniformity and the zero mode

All positive-mass runs include the constant harmonic, whose eigenvalue
is M²+12ξH². The Gaussian p-regime also needs H/(4πF) small and
M²F²V≫1. The finite-radius numbers are dimensionless determinant
benchmarks; they are not claims that arbitrary physical M/F lies in
this chiral regime.

For the SELECTED positive-mass action, choose a fixed charge interval
or a small complex neighborhood in which Re Mc²≥M_*²>0 and |ξc|≤ξ_*.
For sufficiently small H the complete quadratic spectrum then stays
uniformly away from zero. The small-x heat remainder and the
exponentially suppressed large-x tail yield (10) uniformly on that
parameter set, including fixed-order charge derivatives. In particular
∂_u ρ_pi/H=O(H⁵), so the zero-charge derivative and H→0 commute for
this sector at fixed positive strong pion mass. This statement does not
cover the massless photon sector or the full QCD+QED theory.

More explicitly, on such a compact parameter set the smooth heat kernel
has Bξ(x)=k3(ξ)x+O(x²), with the remainder and its fixed-order ξ
derivatives bounded by a common constant for 0<x<x0. Rescaling x=y/z
in (4) makes the remainder O(z^-3) in I, uniformly. The x≥x0 segment
is exponentially bounded using Re(Mc²)>0 for sufficiently small H.
Mass differentiation of exp(-Mc²t) inserts factors t, which gives the
same remainder order in H with additional bounded powers of 1/M_*².
Thus, writing the explicit leading term from (10), both the remainder
and its first fixed-input charge derivative are O(H⁸), rather than
merely an undifferentiated pointwise o(H⁶). No large-charge or chiral
uniformity is claimed.

M→0 at fixed H is different. For a minimal Gaussian scalar the formula
has zI0(z)→61/90 and Wdec has a logarithmic singularity. There is an
actual zero eigenvalue at M=0; deleting it is a different functional.
The compact chiral group zero mode needs non-Gaussian integration once
the p-regime fails. Neither the finite Gaussian chiral limit nor an
interchange of chiral, charge and radius limits is used for (10)--(13).

## 6. Finite computation and scope

compute_sphere.py checks exact heat coefficients and the charge factors;
compares (6) against independent, directly summed heat integrals for W
and rho; brackets it with finite positive spectral sums and an explicit
tail bound; verifies direct fixed-parameter metric differentiation; and
evaluates dimensionless radius/charge grids. Independent heat quadrature
uses a short asymptotic small-x segment, with order/split stability
checks. mpmath/SymPy results are conditional on numerical libraries and
reported tolerances, not certified intervals. The spectral tail bound
is an analytic positive-sum bound evaluated numerically.

The actual executable, fixed domain, caps and exclusions are in
contract.json. The frozen v2 run is run_001/manifest.json. No load-bearing
number comes from an alpha or cosmic target, and no kernel has been
replaced by a fitted loop formula. This route calculates a missing
global LOW-ENERGY contribution. It leaves the full proton-current
kernel, QCD global remainder and full matched charge response to the
other FSP-008 routes.
