# Curved nodal band: the spatial curvature term comes from the endpoint

Contract frozen at 2cd6d1124f. The earlier leaf determinants did not specify
the curved extension of the original band Hamiltonian. This calculation
does: it retains the quadratic tangential dispersion on a curved surface.
The nodal modes still generate a flat cubic term, but the surface-curvature
coefficient comes from the lower band endpoint and is analytic in the gap
squared near zero. It is not the assumed linear-in-gap curvature threshold.

## Specified microscopic operator

On R_tau x R_z x S^2_r use the Hamiltonian and conventions of
CURVED_BAND_CONTRACT.md. The internal Gamma matrices are pseudospin,
with matrix trace d. They are scalar components under surface coordinate
changes; this is not a relativistic spinor Laplacian with an R/4 term.
The positive squared operator has eigenvalues

    omega^2+v^2 k_z^2+[(lambda_l-k0^2)/(2M)]^2+Delta^2,
    lambda_l=l(l+1)/r^2, multiplicity 2l+1.

The parity-even fermion effective action is minus one half the trace log
of this operator, hence plus one half its proper-time integral. M,k0,v,
Delta are positive. Define E0=k0^2/(2M), the gap at the band endpoint when
Delta=0, and R_Sigma=2/r^2. Curvature counterterms and the zero of vacuum
energy have not been selected by matching a target coefficient.

The flat band is the form in equation (1) of
[Jose and Uchoa, 1912.12504v2](https://arxiv.org/html/1912.12504v2),
6 January 2020. That source does not specify this curved operator or prove
its gravitational interpretation. The scalar surface heat coefficient is
consistent with equations (4.26)-(4.27) of
[Vassilevich, hep-th/0306138v3](https://arxiv.org/html/hep-th/0306138v3).
The spectral derivation below directly checks it without treating the
fourth-order band operator as a relativistic Dirac operator. Both source
versions and locators were checked on 5 November 2026. No novelty claim or
full source caching is made.

## Curvature expansion from the discrete spectrum

At fixed proper time s>0 put

    f_s(lambda)=exp[-s(lambda-k0^2)^2/(4M^2)],
    S_r(s)=sum_(l>=0)(2l+1) f_s(l(l+1)/r^2).

The integral part of Euler-Maclaurin is exactly

    integral_0^infinity dl (2l+1)f_s(l(l+1)/r^2)
      =r^2 integral_0^infinity d lambda f_s(lambda).

For g(l)=(2l+1)f_s(l(l+1)/r^2), the endpoint terms give
g(0)/2-g'(0)/12=f_s(0)/3+O(r^(-2)). Higher endpoint derivatives start
at O(r^(-2)). Thus the smooth local expansion per surface area is

    S_r/(4pi r^2)
      =(1/(4pi)) integral_0^infinity d lambda f_s(lambda)
        +R_Sigma f_s(0)/(24pi)+O(R_Sigma^2),
    f_s(0)=exp(-s E0^2).

The integral samples the nodal neighborhood lambda=k0^2. The term linear
in curvature instead samples lambda=0. Dropping that endpoint or replacing
its heat weight with the nodal value changes the curvature term.

This is an expansion at large r for fixed smooth heat weight. It is not
a uniform statement at fixed finite r as Delta tends to zero; discrete
level crossings and nonlocal finite-size terms require separate treatment.

## Flat cubic and spatial curvature from the same heat trace

The tau and z Gaussian integrals give 1/(4pi v s). Therefore

    K(s)/V4 = d exp(-s Delta^2)/(4pi v s)
              [(1/(4pi)) integral_0^infinity d lambda f_s(lambda)
                 +R_Sigma exp(-s E0^2)/(24pi)+...].

The radial integral is

    integral_0^infinity d lambda f_s(lambda)
      =M sqrt(pi/s)[1+erf(E0 sqrt(s))].

For s E0^2>>1 this approaches 2M sqrt(pi/s). Its nodal part has the
effective three-dimensional heat behavior, yielding the finite nonanalytic
vacuum contribution

    U_nodal=d M |Delta|^3/(12pi v).

Terms associated with the distant endpoint are analytic in Delta^2 near
zero after the requisite ultraviolet subtractions. This calculation does
not fix the total constant vacuum term or protect a zero quadratic term.

The local surface-curvature term in the Euclidean action is instead

    L_E,curv=e_Sigma(Delta) R_Sigma,
    e_Sigma(Delta)=d/(192pi^2 v)
                     integral_(Lambda^-2)^infinity ds s^(-2)
                       exp[-s(E0^2+Delta^2)].

Let B0=E0^2>0 and z=Delta^2. The integral equals

    I(B0+z)=Lambda^2 exp[-(B0+z)/Lambda^2]
              -(B0+z) E1[(B0+z)/Lambda^2].

Its large-cutoff expansion is Lambda^2+(B0+z)
[log((B0+z)/Lambda^2)+gamma_E-1]+O((B0+z)^2/Lambda^2).
Subtracting the value and first derivative in z at zero leaves the finite
mass-dependent remainder

    e_Sigma,sub=d/(192pi^2 v) J(z),
    J(z)=(B0+z)log(1+z/B0)-z,
    J(z)=z^2/(2B0)-z^3/(6B0^2)+O(z^4/B0^3).

Thus this curvature coefficient is analytic in Delta^2 for |Delta^2|<E0^2.
It has no |Delta| term. The un-subtracted constant and Delta^2 terms are
independent matching data; the subtraction exposes the nonanalyticity
question without choosing their physical values. The Lorentzian curvature
coefficient carries the usual opposite sign relative to Euclidean e_Sigma,
but that does not change its analytic dependence.

This product geometry probes only one combination of possible gravitational
operators. It does not identify a four-dimensional Einstein coefficient
or compute tensor-wave propagation. A standalone F proportional to
|Delta| multiplying R_4 would produce a |Delta| R_Sigma term here and is
not the result of this minimal determinant. Additional preferred-frame
curvature operators could cancel such a term; their separate coefficients
have not been calculated. No theorem against all curved nodal theories
follows from this restriction.

## Flat-preserving curvature freedom

The curved operator was explicitly minimal. A further allowed alternative
is L_Sigma -> L_Sigma+xi R_Sigma in its band argument, with constant xi.
It has precisely the same flat spectrum. At first order in the constant
surface curvature, its leading integral changes by

    (xi R_Sigma/(4pi)) integral_0^infinity d lambda f_s'(lambda)
       =-xi R_Sigma f_s(0)/(4pi).

Consequently the curvature heat coefficient is multiplied by 1-6xi while
the flat nodal cubic is unchanged. This is a direct operator-level reason
that the flat spectrum alone does not select curvature matching. No xi
has been set to obtain a desired value; the executed calculation uses
xi=0. The alternative's complete health and field equations are untested.

## Numerical discriminator and audit

The exact sphere sum was evaluated at 80-digit precision for the frozen
proper times 1/4,1,4 and radii 20,40,80. M=v=k0=1 are diagnostic units, not
measured or fitted values. At radius 80 the relative errors in the constant
curvature term were, respectively,

    3.9064e-6, 1.5626e-5, 6.2498e-5.

All successive error-reduction ratios lie in the frozen 3.5-to-4.5 interval,
consistent with the next O(r^(-2)) term in S_r. The largest omitted positive
tail bound was 6.85e-88. The tail estimate uses the exact decreasing-function
integral after verifying monotonicity at the truncation point. Arithmetic
is high-precision floating point, not interval-certified rounding.

Fifteen checks pass in evidence/curved_band. Replacing f_s(0) by the nodal
value 1 fails exactly the three curvature matches in
evidence/curved_band_mutate. Both v2 manifests validate against the current
input and output hashes. The error ladder, tail bound and mutation directly
test the endpoint distinction; they do not certify a complete gravity
theory. The exact identities include the Euler-Maclaurin constant, the
subtracted curvature mass dependence and the flat cubic normalization.

Self-review: determinant sign, scalar versus spinor surface operator,
area normalization, Gaussian frequency/longitudinal measure, band endpoint,
subtraction order, domains of analyticity and noncommuting limits were
checked. Verdict: conditional curved-operator matching result, with the
discrete coefficient computationally checked in the stated finite range.
No independent audit or global metric-source calculation is claimed.

## Next research boundary

This calculation replaces the unjustified inference from a flat nodal
density of states to a linear Einstein coefficient with an actual curved
band determinant. It retains the cubic but does not produce the assumed
spatial curvature dependence. It therefore cannot supply the missing joint
normalization identity for the Zimmerman coefficient.

The remaining route is a full specified curved microscopic action, including
its geometric couplings and whatever interaction fixes them, followed by
joint vacuum and operational-force matching. Computing more radii for this
same operator cannot supply that input. Metric components involving the
preferred time and axis, nonminimal geometric couplings, and interacting
completions remain uncomputed, rather than excluded. A positive continuation
must establish their selection and compatibility with the source response;
it cannot import coefficients from the incompatible leaf and curved-band
actions. The original goal remains active and unresolved.
