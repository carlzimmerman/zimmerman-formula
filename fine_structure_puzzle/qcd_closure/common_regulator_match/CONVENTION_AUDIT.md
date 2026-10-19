# Exact source check of the flat mass jet and comparison-path qualifications

This is an additional derivation after INDEPENDENT_RAW.md was saved. No new
root synthesis has been read. All prior boundary files remain unchanged.

## Unweighted a4 checks the missing diagonal-collar term directly

Use the authenticated BGKV hep-th/9906144v1, Theorem 2.1(5), printed p. 5,
and the inward normal convention in its Section 2. The exact source hashes
are in INPUTS_SOURCES.json. Set the scalar-potential endomorphism E=-U I,
U=m^2; factor a constant reference mass from the proper-time exponential.
At first order in a variable U perturbation, the canonical heat formula has

    bulk: 60 tr_comb(E_;ii)/360 = -(1/3) Delta U,
    wall: tr_comb[(240P_+-120P_-) E_;in]/360
            = -(1/3) partial_in U.

For the wall contraction, the vector gives (240-3*120)(-partial_in U)
=+120 partial_in U; subtracting two Dirichlet ghosts gives
-240 partial_in U, for total -120 partial_in U. The bulk fiber trace is
4-2=2. These are actual mixed-domain coefficients; no replacement by
all-Dirichlet boundary conditions has been made.

Because partial_in=-partial_out, their integrated first-order heat trace
contribution is zero by the divergence theorem. This agrees with exact
Duhamel: its first-order response has zero combined flat f_;in coefficient.
It does NOT mean the canonical diagonal collar itself has zero first jet.

The canonical boundary term contributes to Gamma

    +(partial_in U)/(24pi m) = +(partial_in m)/(12pi),

while the canonical bulk has the linear Laplacian term. These cancel in
the total response. Thus there are two consistent descriptions:

* all-IBP bulk and zero flat first-jet collar;
* local diagonal bulk and the collar +(partial_in m)/(12pi).

The common PV sum of their difference is exactly the surface conversion
computed in the independent raw file. At center it changes the collar's
inverse-R coefficient by -La^2/(3pi). The local-diagonal bulk coefficient
changes by +La^2/(3pi), preserving the matched answer.

The source check establishes this specific convention conversion. It does
not independently prove completeness of every higher boundary invariant
or a regulator-uniform remainder for the full monopole operator.

## Explicit finite matching data

Let delta_kappa be a finite common shift of the bulk E^2/B^2 coefficient,
and delta_C_wall denote any additional finite background-dependent wall
matching contribution to the inverse-R coefficient. The most explicit
scoped result is therefore

    C_Gamma = (L/pi)[11 log(2)(a^2+n_mag^2)/3+7a^2/6-a^4/3]
              -4pi delta_kappa(a^2+n_mag^2)+delta_C_wall.

The benchmark fixes delta_kappa=0 in the stated harmonic scheme and
delta_C_wall=0 for the microscopic relative determinant alone. Pure
geometric cubic wall counterterms cancel against the same-domain
constant-v reference at inverse-R order. That cancellation does not fix
finite wall functions of boundary holonomy or of boundary field jets.

For instance, using reduced three-dimensional boundary functions with all
L factors absorbed into their definitions,

    S_wall = integral_S2 [K w(h)+z(h) partial_out h]

shifts the inverse-R difference at center by

    delta_C_wall = 4pi a^2 w''(v)-4pi a^2 z'(v).

If wall matching respects the center reflection h-v -> -(h-v), w is even;
z can be odd when paired with the odd field derivative. These examples
are therefore not removed solely by center symmetry. More general allowed
boundary source actions require their own symmetry and locality contract;
the examples are not advertised as an exhaustive wall EFT basis.

An area potential u(h) would contribute -2pi a^3 u'''(v)/3 at inverse-R
order if the chosen wall theory permits a nonzero u'''(v); center symmetry
would set it to zero. This illustrates why the permitted matching class
must be specified rather than inferred from cancellation of K^3 alone.

## Fixed wall value is a different path

Our path fixes the asymptotic v as R varies. Fixing the value at the wall
instead would give h(r;R)=v+a/R-a/r throughout the exterior. Even a bulk
quadratic potential beta_2(h-v)^2 then gives

    integral_rc^R 4pi r^2 beta_2 a^2(1/R-1/r)^2 dr
      =4pi beta_2 a^2 [R/3-rc+rc^2/R-rc^3/(3R^2)].

It contains an inverse-R term depending on the arbitrarily chosen inner
cutoff, whereas the fixed-asymptotic-v quadratic term has none. That
dependence signals the missing transported core contribution, not a local
outer-wall prediction.

The quartic term also changes character:

    integral_rc^R r^2(1/R-1/r)^4 dr
      =1/rc+[10/3-4log(R/rc)]/R
        -6rc/R^2+2rc^2/R^3-rc^3/(3R^4).

Thus a log(R)/R term appears under this transport. One cannot identify
the two subtraction paths by changing only the wall value in a lower-order
boundary formula. Neither path alone fixes global/core/neutral physics.
