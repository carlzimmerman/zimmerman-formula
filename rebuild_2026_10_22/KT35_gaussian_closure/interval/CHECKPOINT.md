# Cassini interval route checkpoint

This route was redirected to the newly authorized action-response search before
any numerical certification experiment was executed. It establishes no new
continuum exclusion and does not upgrade KT34's sampled Cassini statement.

The corrected KT33 flux and density formulae and KT34 scans were inspected.
Direct natural-interval density quadrature has a locally integrable singularity
at the Newtonian external-field saddle. The flux representation is better:
although `nu-1` diverges there, `(nu-1)u` tends to zero. Changing angular variable
from `mu` to `h` removes the singularity and permits elementary antiderivatives,
but their straightforward interval evaluation can suffer severe dependency
inflation and cancellation. Ordinary adaptive SciPy quadrature would not be an
interval certificate.

The installed Python 3.9.6 environment has mpmath 1.3.0. Its interval `erf` raised
`NoConvergence` for the simple input `[1,2]`; interval elementary functions plus
an explicitly bounded Gaussian series/integral would be needed instead. This
was an environment probe, not a mathematical experiment.

The sibling sign route found a more promising reduction. With
`L=r T'/T in [0,5]`, the combined angular flux is `3b+L c`, a convex combination
of `3b` and `3b+5c`. Although `c` alone changes sign, a positive softened-Coulomb
mixture representation of `nu-1` may prove both endpoints nonpositive. If proved,
one can certify a strictly negative integral on a favorable finite radial
patch and discard the rest by sign. This would avoid separate saddle and
infinite-tail error budgets. That proof was still in progress when this
checkpoint was written; consult the sign route for its final status.

No KT33/KT34 files, old evidence, model parameters, or observational cuts were
changed. No interval computation or bounded-run manifest was produced here.
