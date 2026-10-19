# Independent center-holonomy local bulk/collar match

This hand derivation was saved before asking the root for a candidate or
reading any new root synthesis. The prior boundary lane is unchanged.
Notation and scope are fixed by CONTRACT.md. The comparison is between
h=v-a/r, B=n_mag rhat/r^2 and constant h=v=pi/L, B=0 on the same wall.
Only outer-radius dependence of the stated local functionals is included.

## 1. The Duhamel collar does not by itself use the local-diagonal bulk

For one scalar trace with U=m^2>0, the local diagonal heat expansion through
two derivatives is

    K(x,x;t)=(4pi t)^(-3/2) exp(-tU)
             [1-t^2 Delta U/6+t^3 (partial U)^2/12+...].

The coefficients can be reconstructed directly from the free Gaussian
bridge: its covariance is 2[min(s,s')-ss'/t], the integrated quadratic
Taylor term gives t^2 Delta U/6, and half the integrated covariance of the
linear Taylor term gives t^3 (partial U)^2/12. Thus the unintegrated
two-derivative Gamma density for one scalar is

    D_diag = Delta U/(48pi m)-(partial U)^2/(192pi m^3).

Integrating by parts gives the bubble/IBP representative

    D_IBP = +(partial U)^2/(192pi m^3),
    D_diag-D_IBP = Delta m/(24pi).

There are two orbital scalar traces in the charged gauge/ghost combination,
so the difference is Delta m/(12pi) for each regulated frequency. The spin
terms have no such two-derivative scalar-potential ambiguity.

Now perturb a constant U by f. Exact Duhamel gives

    delta Gamma = integral_0^infinity dt exp(-m^2t) Tr(f exp(t Delta)).

The mixed smeared a2 coefficient of f_;in is proportional to the combined
tr chi=0. Hence the Duhamel *total trace* has no flat first-normal-jet
boundary response at this order. But the local diagonal bulk density has
linear variation Delta f/(24pi m) for the two orbital traces. Consequently
a collar accompanying the local diagonal bulk MUST contain

    C_diag-C_IBP = - integral_boundary partial_out m/(12pi)
                 = + integral_boundary partial_in m/(12pi).

The frozen Duhamel collar, whose flat first jet is zero, therefore matches
the all-IBP bulk representative. Combining it directly with the local
diagonal bulk would double count the displayed divergence. The curved
K*partial_in m/m jet in the frozen derivation is a separate higher-order
collar term and does not remove this flat-jet compensator.

At finite PV masses define

    q_n(h)=2pi n/L+h,
    mu_nj(h)=sqrt(q_n(h)^2+M_j^2),
    F0(h)=sum_n,j c_j mu_nj(h).

The exact representative conversion at this derivative order is

    Gamma_bulk,diag-Gamma_bulk,IBP
       = integral Delta F0(h)/(12pi),
    Gamma_collar,diag-Gamma_collar,IBP
       = - integral_outer partial_out F0(h)/(12pi),

with the corresponding inner surface term if an annular domain is used.
The inner term is fixed as R varies and changes no outer inverse-R
coefficient. Both representatives therefore give the same matched result.

## 2. Common-PV limits needed at center

The mode reflection n -> -n-1 sends q_n(v) -> -q_n(v). It kills all odd
sums in q exactly at every finite PV mass. Within the gapped holonomy
chamber, physical |q_n| has second derivative zero. A heavy regulator has

    d^2 mu/dh^2 = M_j^2/(q_n^2+M_j^2)^(3/2).

The frequency sum tends to L/pi: rescale q/M_j and integrate
(1+t^2)^(-3/2), whose primitive is t/sqrt(1+t^2). Since the heavy c_j sum
to -1,

    F0'(v)=0,  F0''(h) -> -L/pi,
    F0'(v-a/R) -> La/(pi R).

The matched local diagonal collar compensator is consequently

    -[4pi R^2/(12pi)] * [La/(pi R)] * [a/R^2]
      = -La^2/(3pi R).

This is missed by taking a modewise physical first-jet cancellation as a
statement about the local-diagonal collar after the regulated tower sum.

## 3. Bulk derivative terms

At a fixed PV mode, two orbital traces contribute

    K_B,orb=1/(24pi mu),
    K_E,orb=q_n^2/(24pi mu^3),

while the spin trace contributes -1/(2pi mu) to both E^2 and B^2.
Thus, after a common regulator sum and fixed magnetic harmonic subtraction,

    K_E,IBP=K_B+c,  c=L/(24pi^2).

The conversion above gives

    D_bulk,diag = K_B B^2+(K_B-c) E^2
                  +(1-Lh/pi) Delta h/(12pi).

Here Delta h=0 in the outer region. The EOM term is retained as part of
the representative definition; harmonicity does not erase the preceding
surface conversion.

At center and scale mu_ren=2pi/L, the declared magnetic harmonic scheme is

    K_B(v)=-11L log(2)/(12pi^2).

For example the finite centered harmonic difference is 4 log(2), obtained
by summing the two positive half-integer tails relative to integer tails;
each tail difference is 2 log(2). A common finite change delta_kappa to
the E^2 and B^2 coefficients remains a free coupling matching datum.

With E^2=a^2/r^4, B^2=n_mag^2/r^4, integration to R gives

    C_bulk,der,IBP = 11L log(2)(a^2+n_mag^2)/(3pi)-La^2/(6pi),
    C_bulk,der,diag = 11L log(2)(a^2+n_mag^2)/(3pi)+La^2/(6pi),

where Gamma|inverse=C/R. Terms from K_B(h)-K_B(v) first enter at
R^(-2), or later at center. A common finite delta_kappa shifts either C
by -4pi delta_kappa(a^2+n_mag^2).

## 4. Quartic local potential

For each mode the two-orbital zero-derivative density is -mu^3/(3pi).
The fourth h derivative of mu^3 is 9M_j^4/mu^5. For a heavy mass,

    sum_n M_j^4/(q_n^2+M_j^2)^(5/2) -> 2L/(3pi),

because integral_R (1+t^2)^(-5/2)dt=4/3. The physical fourth derivative
vanishes inside the chamber, while sum heavy c_j=-1. Hence

    V_eff''''(h)=2L/pi^2,
    V_eff(v-a/r)|quartic = La^4/(12pi^2 r^4),
    C_bulk,potential = -La^4/(3pi).

Lower Taylor powers give larger R powers and are excluded from the
inverse-R coefficient only after the comparison path has been fixed.
This derivation keeps the same common PV convention as the derivative
sector; it does not discard regulator fields before summing frequencies.

## 5. Outer collar and reference cancellation

The constant-mass actual relative-wall determinant per charged pair has

    Gamma_collar = -(8/3)R mu_b
                   +(5/8)log(mu_b^2)
                   +16/(315 mu_b R)+mass-jet terms+... .

The cubic-geometry term has the same inverse-R coefficient on the profile
and on the constant-v reference: their local masses differ by O(1/R),
which changes that term first at R^(-2). The holonomy-independent cubic
surface counterterm therefore cancels in this comparison.

For the all-IBP/Duhamel collar, expand

    mu_b=mu_nj-a*q_n/(mu_nj R)
           +a^2*M_j^2/(2mu_nj^3 R^2)+... .

The lower term -(8/3)R mu_b gives, after the common PV limit,

    C_collar,IBP = -4a^2/3 * sum_n,j c_j M_j^2/mu_nj^3
                 -> +4La^2/(3pi).

The first expansion of the logarithm and the curved first-jet term are
odd in q at center, hence vanish exactly at finite PV mass. Boundary
quadratic F terms and remaining higher jets are below inverse-R order
under the local gapped derivative counting. This is an inventory within
the specified derivative expansion, not a uniform global remainder proof.

For the local diagonal collar, Section 2 supplies the compensator:

    C_collar,diag = 4La^2/(3pi)-La^2/(3pi) = La^2/pi.

The apparently plausible combination of the diagonal bulk with the raw
IBP/Duhamel collar would instead exceed the matched answer by
La^2/(3pi). That is a precise convention mismatch, not a new observable.

## 6. Matched local result and sign

Adding either matched pair of bulk and collar representatives gives

    C_Gamma,local = (L/pi) [ (11 log(2)/3)(a^2+n_mag^2)
                            +7a^2/6-a^4/3 ],
    C_logweight,local = -C_Gamma,local.

The coefficient is in the declared magnetic harmonic scheme at 2pi/L
with no additional finite wall matching functional. It is a local charged
bulk-plus-outer-collar benchmark, conditional on the derivative expansion
and the stated boundary inventory. It is not the full monopole action.

In particular, for a=n_mag=1,

    C_Gamma,local = (L/pi)[22 log(2)/3+5/6].

The classical bulk contribution, if explicitly added in the same magnetic
matching scheme, is -2pi L(a^2+n_mag^2)/g_H^2 to C_Gamma, with the opposite
sign in the logweight. It is not part of the one-loop coefficient above.

## 7. Remaining finite boundary matching and comparison paths

Same geometry cancels holonomy-independent pure geometric wall terms, but
does not specify a physical wall action. A finite wall functional depending
on the allowed boundary background can shift the benchmark. With the
framed domain, background gauge transformations at the wall are restricted;
one must say whether arbitrary Wilson-line wall functions are permitted
matching data or whether the microscopic relative wall alone defines them.
For example a finite functional integral_boundary K w(h) has inverse-R
profile/reference difference 4pi a^2 w''(v)/R at center when w is even
there. A finite derivative wall term z(h) partial_out h can similarly
produce a term proportional to a^2 z'(v)/R. Such data are not fixed by the
cancellation of the pure cubic wall counterterm. The displayed coefficient
sets these additional finite matching functions to zero by definition.

The comparison uses asymptotic v fixed. Transporting h so that the wall
value stays fixed instead uses h(r;R)=v+a/R-a/r, changing the entire bulk
background by a/R. This shifts lower bulk potential powers (including the
R^3 and R terms), which can feed inverse-R coefficients on expansion. It
also changes the wall mass-function expansion. A fixed-wall-value path is
therefore a different subtraction problem; it cannot be substituted while
keeping the present coefficient.

Unknown pieces include the smooth core, full angular/global determinant,
neutral sector, lifted modes and collective-coordinate measure, deformation
and screening, the actual stable saddle, and regulator-uniform remainder
control. The metric stress and electromagnetic normalization are additional
missing maps. No physical alpha follows from this local benchmark.
