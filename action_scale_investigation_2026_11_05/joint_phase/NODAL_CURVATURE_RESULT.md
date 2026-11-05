# Joint microscopic matching on Dirac leaves

Frozen contract: f0547408f5. This computes the cubic energy, curvature
threshold and amplitude kinetic term from one specified determinant. It
does not supply the desired positive four-dimensional gravitational
coefficient. Two independent issues prevent importing its coefficients
into LINEAR_INDUCED_RESULT.md: the finite curvature threshold has the
opposite sign, and the induced operator is intrinsic leaf curvature.

## Definition and source scope

Consider the parity-even determinant of minimally coupled Dirac fermions
on 2+1-dimensional leaves, with total spinor trace d_s and positive fixed
transverse density nu. Pair parity-odd contributions away. In Euclidean
signature the squared operator is -nabla_3^2+R_3/4+m^2, with m>0.
This is a definite curved extension of a cone, not a deduction of the
unique curved-space action from a flat nodal-ring dispersion.

[D. V. Vassilevich, Heat kernel expansion: user's manual,
hep-th/0306138v3](https://arxiv.org/html/hep-th/0306138v3), equations
(1.18), (3.27), (4.26)-(4.27), supplies the proper-time representation,
Dirac endomorphism E=-R/4 and coefficient E+R/6. These give -R_3/12 for
this operator. The fermion determinant reverses the bosonic sign.
The source assumes a suitable elliptic operator and a controlled local
expansion; it does not establish a nodal medium's four-dimensional
gravitational action. Version and equations were checked on 5 November
2026. The application below is our calculation, not a result attributed
to that review. No full source text is retained.

## Finite threshold and the Wick-rotation sign

The parity-even Euclidean effective density through first curvature order is

    L_E = nu d_s/[2(4pi)^(3/2)]
          integral_0^infinity ds s^(-5/2) exp(-m^2 s)
          [1-s R_3/12+...].

Analytically continuing the mass-dependent integrals yields

    L_E,finite = nu d_s m^3/(12pi)+nu d_s m R_3/(96pi).

The Lorentzian convention is L_L=F_leaf R_3/2-U; its Euclidean counterpart
is U-F_leaf R_3/2. Consequently

    U_finite=nu d_s m^3/(12pi),
    F_leaf,finite=-nu d_s m/(48pi).

The positive coefficient of Euclidean R_3 is NOT a positive Lorentzian
Planck coefficient. Reversing this dictionary gives a false apparent
success and is the negative control in the executable.

For m=h sigma define U_finite=C_A sigma^3/3 and F_leaf,finite=D sigma.
Then

    C_A=nu d_s h^3/(4pi)>0,
    D=-nu d_s h/(48pi)<0,
    D=-C_A/(12h^2).

Thus the powers match the previous candidate, but its required D>0 does
not. This is a finite threshold statement for the declared minimally
coupled fermions, not a claim that every induced gravitational coupling
must be negative.

## Cutoff terms are distinct matching data

With proper-time lower limit Lambda^(-2), define

    I1=2Lambda exp(-m^2/Lambda^2)-2sqrt(pi)m erfc(m/Lambda),
    I0=(2/3)Lambda^3 exp(-m^2/Lambda^2)-(2/3)m^2 I1.

These are the integrals of s^(-3/2) and s^(-5/2), respectively. With
P=nu d_s/[2(4pi)^(3/2)], U_cut=P I0 and F_leaf,cut=P I1/6. Expansion gives

    U_cut=nu d_s[Lambda^3/(24pi^(3/2))
                 -m^2 Lambda/(8pi^(3/2))+m^3/(12pi)+O(m^4/Lambda)],
    F_leaf,cut=nu d_s[Lambda/(48pi^(3/2))-m/(48pi)
                      +O(m^2/Lambda)].

F_leaf,cut is positive because its defining integral is positive. The
positive leading term depends on the cutoff; it is not the proposed
positive linear condensate term. Moreover,

    d F_leaf,cut/dm=-nu d_s erfc(m/Lambda)/(48pi)<0.

Vacuum and quadratic counterterms are needed to specify the critical
potential, and a gravitational matching term specifies the total Planck
coefficient. We have not fixed any of these by demanding the desired
ratio. The finite |m| and |m|^3 thresholds refer to the displayed operator
and an analytic-in-m^2 subtraction near zero; adding a new nonanalytic
operator is a changed microscopic matching assumption.

## Amplitude kinetic coefficient from the same fermions

In a flat leaf, expanding -Tr log(gamma.partial+m+delta m) gives a quadratic
kernel with numerator d_s[m^2-k.(k+q)]. Feynman parametrization and the
shift l=k+xq give M^2=m^2+x(1-x)q^2 and numerator M^2-l^2. In three
Euclidean dimensions,

    integral d^3l/(2pi)^3 1/(l^2+M^2)=-M/(4pi),
    integral d^3l/(2pi)^3 1/(l^2+M^2)^2=1/(8pi M),
    Pi(q)=nu d_s/(2pi) integral_0^1 dx sqrt[m^2+x(1-x)q^2].

The first integral is dimensionally continued; it is not a convergent
positive integral assigned a negative physical value. The derivative
coefficient is finite. Expanding at |q|<<m gives

    Pi(q)=nu d_s m/(2pi)+nu d_s q^2/(24pi m)+O(q^4/m^3),
    Z_m=nu d_s/(24pi m),
    Z_sigma=nu d_s h/(24pi sigma)=-2D/sigma.

The zero-momentum value equals U_finite''(m), a separate consistency check
on signs and normalization. The anticipated inverse-amplitude kinetic
scaling does occur, but accompanies negative D. It is a kinetic term
within the leaves, not a verified four-dimensional scalar kinetic term.

## The operator is not the Einstein term

On a warped spacetime ds^2=dy^2+a(y)^2 eta_ab dx^a dx^b, every fixed-y
leaf is intrinsically flat. Its determinant's R_3 term is zero. Direct
calculation of the four-dimensional connection instead gives

    R_4=-6a''/a-6(a'/a)^2,
    a^3 R_4=-6(a^2 a')'+6a(a')^2.

Take periodic y in [0,2pi] and a(y)=1+epsilon cos(y), 0<epsilon<1.
Then integral dy a^3 R_4=6pi epsilon^2, while the intrinsic curvature
integral vanishes. This distinguishes the bulk actions without a boundary
ambiguity. The same scalar-curvature expression follows using Euclidean
flat leaves, as in the executable connection calculation.

Extrinsic-curvature couplings, an orientation ensemble or inter-leaf
dynamics might change the operator. They are not determined by the flat
cone spectrum or by its density of states. The independent intrinsic-leaf
model therefore fails the required tensor matching, irrespective of sign.

## Conditional constant-bare-gravity repair

Even if one temporarily grants an Einstein interpretation of the threshold,
adding only a positive constant bare term gives F=F_b-d sigma with d>0.
On the explicit critical surface U=U0+C_A sigma^3/3, U_sigma>0 and
F_sigma<0. A homogeneous solution with F>0 obeys

    U_sigma=2 F_sigma U/F.

Its two sides cannot agree for U>0. Thus this minimal constant-bare-term
repair has no positive-vacuum stationary point at sigma>0. This assertion
uses the subtracted critical potential, not the unrenormalized cutoff
potential. A nonzero quadratic detuning or additional curvature dependence
changes the equations and is outside this restricted statement.

## Analytic continuation: allowing propagation between leaves

After the frozen determinant test, consider its immediate rank-restoring
repair: a nonzero normal velocity v and |k_y|<=Lambda_y. This is a separate
flat-spectrum calculation, not part of the executable leaf determinant.
Write L=v Lambda_y. Integrating the three-dimensional cone determinant
over the normal momentum gives, for m>0,

    U_v(m)=d_s/(12pi^2 v) integral_0^L dk (k^2+m^2)^(3/2)
          =d_s/(96pi^2 v)
            [L(2L^2+5m^2)sqrt(L^2+m^2)+3m^4 asinh(L/m)].

The antiderivative differentiates to the displayed integrand. For fixed
L>0, subtraction of its constant and quadratic parts leaves

    U_v,sub=d_s/(96pi^2 v)
             [3m^4 log(2L/m)+(9/4)m^4+O(m^6/L^2)].

Thus for any nonzero v the deep infrared response is quartic-logarithmic,
rather than cubic. At m>>L the leading term is instead
d_s L m^3/(12pi^2 v), reproducing the leaf cubic with
nu=Lambda_y/pi. The v->0 and m->0 limits do not commute. A cubic regime
can survive at intermediate scales if another ultraviolet limit permits
that window, but its crossover L is additional data. This is not a proof
against phenomenological MOND over a finite range; it does show that
restoring normal propagation does not automatically preserve the desired
asymptotic response. No curved determinant for this repaired theory was
calculated, and no Lorentz-invariance assumption is needed for this power
change.

## Evidence and next research boundary

Fifteen exact checks pass in evidence/nodal_curvature. Reversing the
curvature Wick sign fails four checks in evidence/nodal_curvature_mutate.
Both manifests validate with current input/output hashes. The bubble's
zero-momentum/vacuum-Hessian identity and direct metric-connection
calculation are the cross-checks beyond evaluating Gamma functions.
The constant-bare-gravity sign argument and normal-propagation integral
are analytic derivations, not included in those fifteen checks.

The derivative expansion is only justified for curvature and momentum
scales below m. It cannot be applied to the gapless polarization sector
as p->0 at fixed curvature. We did not infer a |p|R cusp or a gap from an
expansion invalid in that limit. The existing K230 sphere-gap attempt
was located in the register; no duplicate sphere computation was run.

Self-review verdict: the displayed minimal microscopic bridge fails.
This is not a general no-go for induced gravity or for the Zimmerman
relation. The broader coefficient goal remains unresolved. A productive
continuation must change the curved microscopic operator, its matter
content/interactions or its physical finite-range matching and then
calculate the resulting vacuum and operational response together. Simply
inserting a positive D into the previous action bypasses the demonstrated
missing step. Interacting/orientation completions remain uncomputed;
there is no justified coefficient to adopt from this calculation.
