# Promoted response coefficient: local continuation

Frozen route 3 treats the response coefficient as rigid. A local coefficient with positive gradient energy evades its global no-stationary-halo equation by exporting flux through a boundary. This is a hand-derived continuation, not an independently frozen numerical candidate or microscopic completion.

Let the static energy contain Z |grad b|^2/2 + b O3, Z>0, with O3>=0 independent of b when varying the other fields at fixed configuration. A consistent on-shell relaxation of those other fields preserves this first-variation formula by the envelope theorem, subject to differentiability and stationary boundary data. Then

    Z laplacian b = O3.

For a localized integrable spherical source of total Q=int O3 d^3x>0, outside the source

    b(r)=b_infinity-Q/(4pi Z r).

Its boundary flux 4pi Z r^2 b'=Q is the exact integral equation. The asymptotic coefficient b_infinity is not fixed by this dynamics. In n>2 spatial dimensions, replace Q/(4pi Z r) by Q/[(n-2)Omega_(n-1) Z r^(n-2)]. A finite periodic domain or zero normal-flux boundary requires int O3=0 and excludes the assumed nonzero stationary source; an infinite-domain nonzero flux evades that exclusion. Extended halos need a controlled infrared regulator and need not have finite Q.

The b-shift is not a symmetry with O3 present. Adding a potential W(b) can set b_infinity through W'(b_infinity)=0, but its extremum is new microscopic input until W is derived. No bare coefficient was selected merely by promoting it. If b must stay positive, the interior solution must satisfy that extra condition; no global healthy branch is claimed. Kinetic mixing, screening or a common microscopic potential may change this conclusion and require their own equations.

This is a constructive boundary-value diagnosis, not a no-go for all local adjusting fields. The explicit local equation and radial flux are derived analytically; no simulation or independent review is claimed.
