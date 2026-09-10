# Radial-pressure freedom: constructive checkpoint

Full theory: **OPEN**. Base de9cc54aba17177ae88c123d56fc0c744a906822;
concurrent Claude changes are retained, not automatically endorsed.

The preceding same-action joint point continues numerically to 12 of 14
prescribed acceleration points. All 12 retain angular scalar instability;
the other two hit the declared clock-gradient bound. This is one seed family,
not a universal exclusion. No more initial-only parameter scans are warranted
on that family without a genuinely different input.

The constructive change is to remove exact zero radial pressure, an extra
restriction not demanded by leading-order no-slip. `general_inverse/` varies
the SAME previous action, includes geometric p_r and its radial derivative,
and solves for the actual action jets. The inverse matrix determinant is
computed, not supplied; this is NOT the Dirac constraint matrix. Independent
physical and Einstein-frame equations and the previous zero-pressure limit
are checked. See its report for assumptions and exact equations.

An especially useful corrected target follows directly from the coordinate
transformation to isotropic radius R:

\[
\frac{d\log R}{dr}=\frac{\sqrt B}{r},\quad
\Phi_{\log}'=g,\quad\Psi_{\log}'=\frac{\sqrt B-1}{r}.
\]

Thus equal **logarithmic** potentials, after matching their constants at one
finite radius, require

\[
\boxed{B=(1+rg)^2,\qquad G^r{}_r=-g^2/B.}
\]

With the retained target g=yB and h=ry=r times y, the regular branch is

\[
B=\frac4{(1+\sqrt{1-4h})^2}=1+2h+5h^2+O(h^3),\quad 0<h<1/4.
\]

The old B=1/(1-2h) instead has coefficient 4 at second order and enforces
G^r_r=0. Both agree at leading weak-field order. This is a geometric target
identity, NOT a new observed law or an action-derived PPN result. Logarithmic
potentials agree with the user's physical weak-field potentials only to
leading order. No global asymptotic normalization or cosmological matching
has been assumed.

`log_slip_geometry.py` checks these identities exactly and inserts the new
target into the actual general-pressure inverse at one regular point. Its
physical Einstein/current residuals are below 1e-40 at 60 digits. This shows
that the added pressure is admitted by the varied equations locally; it does
not prove a healthy universal action. Global a0 remains fixed, and no particle
dark matter or per-galaxy acceleration scale is introduced.

Next unavoidable calculation: derive the action curvatures and their shared
preservation on this logarithmic-no-slip geometry, then solve joint matching
and health together. A single inverse point is not a common action across
masses. Physical DOF/PPN/causality, sourced lensing, FLRW/CMB and zero modes
remain open. Prior Lean algebra certificates cannot fill those gaps.

Reproduction: `run_suite.py --result-file PATH` records all actual commands,
outputs and exits. The pinned evidence is `run_001/manifest.json` and
`run_001/results.json`. No long background search is started by this package.
