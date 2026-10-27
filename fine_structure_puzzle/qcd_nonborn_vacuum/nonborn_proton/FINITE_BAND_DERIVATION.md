# Full finite-momentum HB pi-N non-Born photon band

Continuation of the frozen soft-coefficient run_001. No extrapolation of its
soft polynomial is used here. The distinct primary source is Nevado--Pineda,
[0712.1294v2](https://arxiv.org/abs/0712.1294v2), equations (2.9)--(2.11),
(3.16), (3.18), (3.19), (4.26), (4.27). Its exact PDF and TeX archive are
cached. The source PDF title page dates v2 to 8 March 2008; the HTML version
header agrees. This derivation and its numerical contract precede execution.

The AHLP ancillary was checked exhaustively: its assignments comprise static
polarizabilities and their Q^2 slopes for pi-N, pi-Delta and Delta exchange,
including HB expansions. It has no nu-dependent amplitude assignment. The
present source supplies the missing functions in the strict leading HB pi-N
sector, including the contact required by current conservation.

## Dictionary and exact finite integrand

The source S1/S2 Born terms include `-2 F1^2` and exactly match the inherited
WLCM dimensionless amplitudes. Hence `t_i=S_i` directly. The two-current
amplitudes (3.16),(3.19) contain no e. This is also checked by recovering the
charge-stripped polarizabilities from their soft limits. The source's
photoproduction expression (3.15) uses a charge convention with an explicit
e in its prefactor; it is not a numerical input here. Only the explicitly
normalized S_i and their Born/soft benchmarks are imported.

Write `r=Q/m_pi`, `x=Q4/Q`, `h=1-x^2`, `t=r^2`, `w=-t x^2`, `v=t h`,
`k=-t`, `H=sqrt(1-w)` and `D=4v+k^2`. Thus the source variables are
`q0=i m_pi r x`, `q^2=m_pi^2 k`, `|q|^2=m_pi^2 v`. Define

    I=atan(r/(2sqrt(h)))
      +atan(r(1-2x^2)/(2sqrt(h) H)),
    J=I/sqrt(v)
      =integral_0^1 dy [1+t y-t h y^2]^(-1/2).              (1)

The integral form in (1) independently verifies the arctangent branches in
the Euclidean region. It follows directly from the Feynman-parameter integral
in source (3.18); its typeset first denominator has a minor `bold q {2}` typo
in the TeX, resolved by the PDF and the second equality.

Set `C0=g_A^2 M m_pi/(4pi f_pi^2)`. Then the full non-Born source functions are

    S1=C0 B1,
    B1=3/2+1/v-(1+1/v)H-(1/2)(2+k/v)J,

    S2=C0 (k/v) B2,
    B2= -[3/2+(1/2+1/k+1/w)k/v]
        -(w k/D)(1/v-k/(2v))
        +(1/v)[2-(v/w)(1-w)+k w/D]H
        +(1/2)(2+3k/v+k)J.                                (2)

All factors in (2) are dimensionless. Apparent singularities at x=0 or
|x|=1 cancel in the tensor. Quadrature nodes avoid those points; arithmetic
uses 60 decimal digits to handle cancellation near them. In particular the
contact `3/2` in B1 is retained. Source (4.26),(4.27) explains that the purely
dispersive spatial tensor misses a seagull; dropping it violates the soft
limit. There is no extra phenomenological subtraction interpolation.

Define the actual finite functional of the full source amplitudes

    J_band(a,b)=integral_a^b 2r dr integral_-1^1 dx sqrt(1-x^2)
                    [-3B1+h(k/v)B2]
               =integral_a^b 2r dr integral_-1^1 dx sqrt(1-x^2)
                    [-3B1-B2],
    K_HBpiN(a,b)=g_A^2 m_pi^3/(128pi^4 M f_pi^2) J_band(a,b).  (3)

This is the complete non-Born tensor contribution at the declared strict
leading HB pi-N chiral order for that photon band. It combines subtraction,
inelastic and the required source contact. It is not the covariant loop of
run_001: the two approximations agree at their common leading chiral soft
limit but need not agree at the physical pion-to-nucleon ratio.

## Checks and finite scope

The exact soft expansions of (2) are

    B1=r^2(1-11x^2)/24+O(r^4),
    (k/v)B2=11r^2/24+O(r^4),
    J_band(0,L)=9pi L^4/64+O(L^6).                         (4)

These reproduce the independently derived non-Born coefficient in run_001.
The bounded run checks both scalar limits at three Euclidean angles, the
parameter-integral versus arctangent implementation, the seagull-sensitive
zero limit, and nested quadrature convergence. With `x=sin(theta)`, the
angular measure is `cos(theta)^2 dtheta`; evenness permits twice the interval
`0<theta<pi/2`, avoiding endpoint square-root convergence problems.

The declared balls end at `L=0.1,0.25,0.5`; one additional shell is
`0.25<r<0.5`. Tensor-product Gauss-Legendre rules of orders 12,24,48 are
compared. The convergence tolerance is a numerical diagnostic, not a rigorous
analytic quadrature bound. Strong parameters for units are the same printed
AHLP inputs as in run_001; no alpha or fit is supplied. Because the source
provides all momentum dependence at this order, the finite-band calculation
is not a fitted Q^2 curve or a Taylor-polynomial substitution.

The source is unquenched SU(2) low-energy EFT. It does not provide an
independent microscopic Wick-contraction decomposition. Strange/heavy effects,
short-distance polarizability operators, Delta contributions, recoil and
higher chiral orders are outside this sector and are not set to zero in the
physical answer. The strict HB chiral order is controlled as a low-momentum
expansion; no numerical error bound for its physical higher orders is claimed.
Full electromagnetic mass counterterms and common-path UV matching remain
separate. The balls and shell in (3) do not supply the full proton mass or R.
