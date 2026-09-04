# Vanishing spatial projector: Dirac chain and zero-field response audit — 2026-09-03

Script: `vanishing_projector_dirac_chain_2026.py` (13/13). The SymPy
calculation derives the Poisson brackets and response limits; its controls
reproduce the Lorentz-branch ghost and fixed-projector determinant, reject an
unscaled source at zero field, and remove the finite path memory when the
source is changed from linear to quadratic switch-off.

## Candidate and scope

The tested auxiliary reduction is

\[
 S_{\rm aux}=\int\sqrt{-g}\,\lambda
 \left(H^{\mu\nu}\nabla_\mu\nabla_\nu\chi-J\right),\qquad
 H^{\mu\nu}=X(g^{\mu\nu}+u^\mu u^\nu),
\]

on the $u$-frame background, one Fourier mode $k\ne0$, and with $X$
treated as a background parameter. There $H^{00}=0$, $H^{ij}=X\delta^{ij}$,
and

\[
 L=-Xk^2\lambda\chi-J\lambda .
\]

This is a candidate-specific auxiliary principal reduction. It is not the
full covariant metric/clock Dirac chain and is not a classification of every
metric-only projector.

## Dirac chain

- **$X\ne0$:** the primaries $p_\lambda,p_\chi$ generate the
  secondaries $-Xk^2\chi-J,-Xk^2\lambda$. Their actual Poisson matrix has
  determinant $X^4k^8\ne0$, so all four are second class. Preservation fixes
  both multipliers and produces no tertiary. The auxiliary count is zero.
- **$X=0$:** for a generic source the secondary becomes the external
  consistency condition $J=0$. With $J=X\widetilde J$, both secondary
  expressions vanish at $X=0$; the two primaries commute and are first
  class. The auxiliary count is again zero.

Thus the constraint **class** changes while the auxiliary count remains zero.
That branchwise count does not establish a regular response through the
rank-changing point.

## What is actually adverse

For $X>0$, substituting $J=X\widetilde J$ gives

\[
 \chi=-\frac{\widetilde J}{k^2},\qquad
 \frac{\partial\chi}{\partial\widetilde J}=-\frac1{k^2},
\]

with no frequency dependence. If $\chi$ is the physical MOND mediator, this
specified mechanism fails the strict no-instantaneous-channel requirement
(gate 7).

The exact zero-field equation must be evaluated before cancelling $X$:

\[
 -X(k^2\chi+\widetilde J)=0
 \quad\xrightarrow{X=0}\quad 0=0.
\]

It selects no $\chi$. Two paths whose rescaled sources differ by
$\Delta\widetilde J$ have physical source difference
$X\Delta\widetilde J\to0$, yet their $X\to0^+$ solutions retain

\[
 \Delta\chi=-\frac{\Delta\widetilde J}{k^2}.
\]

The same endpoint $(X,J)=(0,0)$ therefore has a nonunique/path-dependent
finite limiting solution. The $J=X^2\widetilde J$ mutation instead gives
$\chi=-X\widetilde J/k^2\to0$, demonstrating that the check is sensitive to
the linear source scaling. The tested $J=X\widetilde J$ ansatz fails the
controlled-zero-field requirement (gate 9) unless a further action-derived
prescription resolves this discontinuity.

## PPN correction

The calculation contains a static $u$-frame auxiliary response. It does not
contain the boosted $g_{00}$, $g_{0i}$, and $g_{ij}$ solutions through the
required post-Newtonian orders, all constraint and multiplier backreaction, a
moving-matter solution, the standard-PPN gauge map, or PPN coefficient
matching. Consequently:

\[
 \alpha_1=\text{UNCOMPUTED},\qquad
 \alpha_2=\text{UNCOMPUTED},\qquad
 \alpha_3=\text{UNCOMPUTED}.
\]

An instantaneous denominator is not itself a PPN parameter; general
relativity also has elliptic lapse and shift constraints. The previous
inherited-$\alpha_3$ claim is withdrawn.

## Corrected verdict

The specified $H=X(g+uu)$, $J=X\widetilde J$ auxiliary reduction preserves
the valid zero-auxiliary-DOF Dirac facts, but is adverse on gates 7 and 9.
Gate 4 remains uncomputed. This does **not** close every metric-only projector
and does not close the broader nonlocal door.
