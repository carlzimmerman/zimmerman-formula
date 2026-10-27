# FD status: actual forces expose an inadequate pump on the tested branch

The full formation problem remains open. This phase replaces a chosen
conversion potential with the actual prior free-domain energy and derives the
transport/front forcing. It does not claim a successful galaxy formation run.

## New statements and tests

* Derived the spatial connection curvature and both reciprocal forces. A
  spatially varying scalar couples front and infall; the antisymmetric force
  does no net work.
* Derived positive scalar added inertia from its radial Poisson kernel.
* Proved a passive-outlet bound for a linear front with positive, varying
  inertia and stiffness, including parameter-work accounting. The theorem is
  stated with its exclusions in MECHANISM.md.
* Identified the exact zero-source condition in nonconverting bulk. This
  conversion-current operator has no direct coupling to redistribution where
  the T current is conserved.

FD-02, finest sampled branch:

| Quantity | Result |
|---|---:|
| lambda interval | 0.0625 to 0.9999 |
| actual energy release on this interval | 3.13607981553522 Eunit |
| conservative branch traversal, starting at rest | 13,531.3689 Myr |
| leading slow monopole radiation | 1.48021e-12 Eunit |
| radiation / release | 4.71994e-13 |
| first sampled law error <=1% | lambda=0.9854451 |
| law error at last sample | 0.6032962% |
| last sampled potential-minimum radius | about 56.3477 kpc |
| minimum sampled static front curvature | 0.0888028 Eunit/rM² |
| maximum front force residual at its conditional minimum | 1.91e-11 |

The traversal is a conditional history on an endpoint-interpolation manifold,
starting after a nucleus exists. It is not a cosmological formation age. At the
last sample the released energy remains mostly kinetic: a small instantaneous
law residual is not relaxation into the final galaxy.

FD-05 includes the full computed kinetic correction to front stiffness. With
the finer metric difference step and 0.05 Myr time step:

* peak forced linear-front energy: 7.77900e-10 Eunit;
* maximum front departure from its moving minimum: 0.000489019 kpc;
* passive-outlet bound for this finite coefficient model: 1.73862e-8 Eunit,
  or 5.54392e-9 of the branch release;
* energy ledger closure: 1.05e-23 Eunit.

That bound covers a passive outlet at the single linear front port. It does
not bound the complete nonlinear two-port scalar system. In particular the
prescribed infall port and a changing source shape cannot be silently included
as passive terms.

## Numerical qualifications

FD-01's uniform integration undersampled the final-density approach. FD-02
corrects it using positive log-metric interpolation and nonuniform panel
integration; its 161/321/641 grids give traversal times agreeing to 0.017 Myr
and slow radiation agreeing to about 4.8e-5 relative across the range.

The original fixed-cell quadrature crosses translated PCHIP knots. FD-04's
independent knot-split quadrature checks the continuous source identity to
8.41e-15 relative. The unsplit FD-02 source audit has 7.32e-6 relative error;
the static cell-midpoint energy and continuous source remain distinct
discretizations. No continuum convergence of that inherited spatial model is
claimed. The inherited endpoints are reproduced in energy to 1.12e-16.

FD-04 finds the kinetic stiffness correction below 0.20% of static curvature
on its tested differences, with positive effective curvature. Its maximum is
not converged under the two difference steps. FD-05 checks that including
either correction does not materially change the tiny peak mode energy.

The passive bound converges under time subdivision for each interpolated
model, but grows from 4.75e-9 to 9.41e-9 to 1.69e-8 Eunit as more branch
coefficient variation is resolved. This is NOT a converged uniform continuum
bound. The corresponding peak energies remain near 7.7e-10 Eunit. The theorem
is exact; its numerical application remains scoped to each finite model.

Density positivity, absence of a hollow shell, and the unconverted outer
profile are inherited restrictions of the manifold, not dynamical successes.
The original normal-F entropy and galaxy-population obligations remain open.

## Decision

Do not treat a fast internal frequency, a zero sampled energy barrier, or an
efficient externally energized outlet as a formation mechanism. On the tested
smooth infall branch, neither the slow conversion source nor the mechanically
forced linear front carries the required energy. Raising a passive damping
coefficient cannot supply missing input energy within the proved model.

The remaining live target is actual energy transfer from freely evolving
material into escaping modes, including nonlinear feedback and the second
current port. A mechanism must compute that transfer and obey the existing
static and outer-reservoir constraints. No arbitrary full-release oscillator,
optimizer-energy radiation ledger, or static density gate is warranted.
