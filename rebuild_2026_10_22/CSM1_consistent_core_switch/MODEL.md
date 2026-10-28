# CSM1: one concentration level controls both core and switch

This is the corrected finite model tested in CSM1, conditional on the existing
backgrounds, halo-mass assignments, collapse recipe and native S9 shape.
Kappa=1/2 remains fitted. Basin selection remains phenomenological.

Let q(M) be S9's concentration divided by its value at 10^14 solar masses,
linearly interpolated in log mass and clamped outside the existing table.
With C=4/[3(3 ln2-pi/2)], define the unfloored collapse contribution

\[
U_{f,b}(M;L)=C[Lq(M)]^{5/4}\Sigma_{{\rm coll},b}(M),\qquad
\Sigma_{0,f}=\frac{a_{0,f}}{2\pi G}.
\]

The candidate parent halo has

\[
\Sigma_{{\rm core},f,b}(M)=\max\{\Sigma_{0,f},U_{f,b}(M;L)\},
\qquad H_{f,b}(M;L)=\mathbf1\{U_{f,b}(M;L)>\Sigma_{0,f}\}.
\]

The same concentration, collapse-column function, background, units and
numerical representation supply the amplitude and the selector. Equality is
on the law branch. Diagnostic crossover masses solve U=Sigma0; no independent
T is used to change a branch. The deleted mismatch was using L itself in the
switch coefficient while using Lq(M) in the core coefficient.

The comparison mass is the inherited BS1 basin mass for SPARC, the Milky Way
and Local Group dwarf flags, with the existing own-mass fallback. It remains
the system's own inferred mass for groups, clusters and isolated lenses.
A basin flag does not replace a galaxy's own mass in its halo profile.
Dwarfs retain X51's separate cooling-floor mass distribution; this correction
does not assert that their internal cores obey a universal Burkert formula.
Clusters retain GS1's measured-gas budget; other pipelines retain their prior
mass relations. No mass budget, radius, background or survey prior was refit.

X43 computes its collapse column from its existing background-specific EPS
implementation. X53 and the Milky Way use their existing tabulated versions.
Each compares its actual column with its actual floor, rather than importing
another pipeline's approximate T. Small differences between numerical roots
are disclosed and are not fitted offsets.

For fixed positive inputs, activation can also be written exactly as

\[
L>L_{{\rm crit},f,b}(M),\qquad
L_{{\rm crit},f,b}(M)=\frac1{q(M)}
 \left[\frac{\Sigma_{0,f}}{C\Sigma_{{\rm coll},b}(M)}\right]^{4/5}.
\]

This identity does not imply that the observational likelihood is monotone
or continuous in L. Changing a flag can replace an entire force profile.

The primary levels are the existing 3.75, 3.9 and 4.0. The single predeclared
challenge, if needed, sets L=Lcrit at the old canonical/background-A crossover
mass 10^12.3 solar masses. It gives L=2.5090648745652686 using X43's actual
floor convention. The initial numerical implementation used the displayed,
rounded a0 and gave 2.5090595510216196, lower by 2.12 parts per million;
that run is retained, and the same defined challenge is repeated with the
actual imported FP0 value. This is a refit of the existing L with old empirical
information, not a prediction or another independent fitted T. All other
cores and both footings must use that same L. No width, second normalization,
shape change, branch-dependent level or gas correction is introduced.

See the frozen contract and per-package source transformations for the exact
finite domain, controls and exclusions. This closure fixes the equation/code
mismatch; its empirical outcome must come from the rerun. It supplies no new
condensation field equation or covariant completion.
