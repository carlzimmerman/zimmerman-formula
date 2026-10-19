# Independent raw derivation: charged static bulk coefficient

Saved 2026-10-19 UTC before reading target project reports or source formulas.
Only analytic hand derivation has been performed at this point.

Let `m=h>0`, `K=-(partial_i-i A_i)^2+m^2`. A pair of charged real adjoint
colors has twice the q=+1 spectrum. Thus the vector factor 1/2 leaves
`Tr_4 log(K delta+V)`, while a complex adjoint ghost leaves
`-2 Tr log K`. At V=0 the net coefficient is `2 Tr log K`.
`tr_4 V^2=8(E^2+B^2)` for `V=2i F`, with `E_i=partial_i h`.

## Orbital scalar potential gradient

For a single `Tr log(-partial^2+U)`, U=m^2, the quadratic variation is
`-1/2 integral dp deltaU(p)deltaU(-p) I(p)`, where

`I(p)=integral d^3k/(2pi)^3 [(k^2+m^2)((k+p)^2+m^2)]^-1`
`=atan(|p|/(2m))/(4pi |p|)`
`=1/(8pi m)-p^2/(96pi m^3)+O(p^4)`.

The integrated local term is `+(partial U)^2/(192pi m^3)`
`=+(partial m)^2/(48pi m)`. The net orbital coefficient 2 therefore gives
`+E^2/(24pi m)`.

## Orbital magnetic field

For a single scalar trace in constant B,
`Tr exp(-s K)/Vol=(4pi s)^(-3/2) exp(-s m^2) (Bs)/sinh(Bs)`.
Since `log K=-integral_0^infty ds exp(-sK)/s`, the B^2 density is

`+(B^2/6)(4pi)^(-3/2) integral_0^infty ds s^(-1/2)exp(-sm^2)`
`=+B^2/(48pi m)`.

Multiplication by the net orbital factor 2 gives `+B^2/(24pi m)`.

## Spin operator

The second term of `Tr_4 log(K delta+V)` is
`-1/2 tr(V^2) integral d^3k/(2pi)^3 (k^2+m^2)^-2`
`=-1/2 * 8(E^2+B^2)/(8pi m)`
`=-(E^2+B^2)/(2pi m)`.
Derivatives of V first enter at higher spatial derivative order. A cross
term with a scalar potential insertion has zero Lorentz trace at this order.

## Static result and shell integral

`Gamma_static,2 = -11/(24pi) integral d^3x (E^2+B^2)/h`.

On `h=v-1/r`, `E^2=1/r^4`, `B^2=n_mag^2/r^4`,

`Gamma_static,2(r_c,R) = -11(1+n_mag^2)/6 log[h(R)/h(r_c)]`.

Its large-R 1/R coefficient is `+11(1+n_mag^2)/(6v)`.
The logweight `-Gamma` has the opposite coefficient.

The zero-derivative density in 3D dimensional regularization is
`2 integral d^3k/(2pi)^3 log(k^2+h^2)=-h^3/(3pi)`.
For the exact static Coulomb profile its radial integral has R^3, R^2, R,
and log R terms, but no 1/R term. This property need not persist after the
complete circle tower is summed: the four-dimensional holonomy potential
can be quartic in h.

This coefficient concerns a local bulk functional on a fixed background.
It does not supply the core, boundary determinant, screened saddle, neutral
sector, complete finite-radius determinant, or a physical vacuum-stress law.
