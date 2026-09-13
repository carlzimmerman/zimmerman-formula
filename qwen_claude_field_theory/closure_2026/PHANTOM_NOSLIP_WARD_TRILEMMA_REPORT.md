# No-slip/Ward phantom trilemma (2026-09-13)

This gate tests the remaining local elliptic “phantom density” architecture,
starting from an action-derived Einstein curvature equation rather than an
asserted MOND Poisson law.  The scope is explicit: one physical metric;
linearized static Einstein curvature; pressureless minimally coupled baryons;
an isotropic auxiliary effective stress `U_{mu nu}`; and a separately
conserved auxiliary sector.  It is not a universal theorem against arbitrary
nonlocal, multimetric, or explicitly anisotropic actions.

For the weak-field metric used in the repository,

```text
G_00 = 2 Delta Psi,
delta^{ij} G_ij = 2 Delta(Phi-Psi).
```

On the no-slip branch `Phi=Psi`, the spatial trace equation is

```text
0 = 8 pi G (3 p_aux),
```

so positive `G` forces `p_aux=0`.  Static conservation of an isotropic source
is the weak-field Ward identity

```text
grad p_aux + (rho_aux+p_aux) grad Phi = 0.
```

With `p_aux=0`, static pressure (`grad p_aux=0`), and a nonzero gravitational
gradient, this forces `rho_aux=0`.

But rewriting the exact exponential MOND equation as an Einstein Poisson
equation requires

```text
rho_aux = (4 pi G)^(-1) div[(1-mu) grad Phi],
mu = 1-exp(-|grad Phi|/a0).
```

This is nonzero for generic fields.  A one-dimensional witness `Phi'=x`,
`a0=1` at `x=2` gives `rho_aux=-exp(-2)/(4 pi G)`, which is nonzero for
`G>0`.  Therefore this architecture cannot simultaneously retain exact MOND,
`Phi=Psi`, and a separately conserved isotropic auxiliary stress while keeping
the ordinary Einstein curvature equations.

The gate also checks the spherical vacuum version without relying on a point
witness.  Vanishing auxiliary density integrates to
`r^2 (1-mu) g=C`; the baryonic MOND equation is
`r^2 mu g=G M`.  Hence `r^2 g=G M+C` and `mu=G M/(G M+C)` would have to be
constant.  But the same flux sum gives `g=(G M+C)/r^2` and
`d mu/d r=-2(G M+C) exp[-(G M+C)/(a0 r^2)]/(a0 r^3)`, nonzero for a positive
total flux.  Thus no non-Newtonian spherical branch exists in this class.

The Python symbolic gate and its regression test evaluate the displayed
identities (six checks).  `PhantomNoSlipWardFormal.lean` independently certifies
the algebraic implications and the nonzero witness.  These are falsification
certificates: a zero exit status means the obstruction was reproduced, not
that the candidate passed.
