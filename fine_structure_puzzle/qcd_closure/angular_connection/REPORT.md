# Quantitative angular connection in boundary coordinates

The large-J logarithmic-derivative and neutral-Schur obligation is resolved
for the actual static charge-one SU(2) BPS gauge Hessian and its relative
mixed wall. The full regulated angular determinant and physical QCD bridge
remain open. This result does not use a physical alpha or a coefficient fit.

For every integer J>=6 and every r>0, the exact reduced operator satisfies

\[
\frac{(J-1)(J-2)}{r^2}I+h(r)^2Q
\ \le V_J(r)\le\
\frac{(J+2)(J+3)+2}{r^2}I+Q,
\]

where Q projects onto the eight charged angular components. This follows
from an exact angular expression obtained from H=-D^2 delta-2adF, and the
profile inequality 0<=Kh/r<=h'<=r^(-2). It supplies quantitative coercivity;
the prior whole-space no-kernel/index result is not an assumption of this
large-J proof.

Let P_J(R)=Y'_J(R)Y_J(R)^(-1) for the smooth-origin regular solution matrix.
Its definition does not depend on the normalization of its columns. Put

\[
Z_J(R)=\frac JR I+Q,\qquad c_* =\frac14\tanh 1.
\]

For J>=6 and R>=4,

\[
\boxed{c_*Z_J(R)\le P_J(R)\le\frac53 Z_J(R).}
\]

This retains the neutral scale J/R and charged scale 1+J/R. In particular
a radius-independent positive lower bound on an unscaled neutral DN block
is false: its upper bound is beta_J/R at fixed J, where
beta_J=(1+sqrt(4J^2+20J+33))/2.

Use input coordinate Z^(1/2)u(R), Dirichlet output Z^(1/2)P_Du(R), and
Robin output Z^(-1/2)P_N(u'(R)+u(R)/R). The resulting actual 9D+3R map
has inverse norm at most 8/(3c_*). Its normal block lies between c_*I
and (11/6)I. Eliminating its two charged normal directions leaves a
neutral Robin Schur coefficient in [c_*,11/6]. The Dirichlet part retains
its identity block. This is a bound for the actual relative wall, without
replacing it by twelve scalar walls.

There is also a quantitative regular-to-exterior comparison. Let P_0,J
be the DN map of the exact diagonal Coulomb operator with the regular
Friedrichs branch at its origin. Its charged channels have potential
1-2/r+l(l+1)/r^2 and its neutral channels l(l+1)/r^2, with
l=J-1,J,J,J+1. Then

\[
\|P_J(R)-P_{0,J}(R)\|\le \epsilon_J(R),
\]

\[
\epsilon_J(R)=\frac{J+6}{2}\left(\frac2R\right)^{2J-2}
+\int_2^R\left(\frac sR\right)^{2J-2}
\left[\frac{6(J+5)}s+16\right]e^{-s}\,ds.
\]

The bound includes all off-diagonal BPS profile corrections. It follows
from Riccati contraction and does not discard charged-induced neutral
tails. R epsilon_J(R)/J tends uniformly to zero for J>=kappa sqrt(R),
for any fixed kappa>0; the raw derivation gives explicit elementary
bounds, including the J/R regime.

Normalize both regular matrices to I at the fixed core radius r=2, and
let F_J,F_0,J be their complete relative-wall determinants. In this
declared normalization a constant c_J exists with

\[
|c_J|<38,\qquad
\left|\log\frac{F_J(R)}{F_{0,J}(R)}-c_J\right|
\le 12T_J(R)+6\frac R J\epsilon_J(R),
\]

provided R epsilon_J/J<=1/2, where

\[
T_J(R)=\frac{R\epsilon_J(R)
+[6(J+5)+16(R+1)]e^{-R}}{2J-3}.
\]

Thus the core-dependent radius correction is smaller than every power of
1/R throughout the J~sqrt(R) band, with an explicit normalized determinant
connection bound. The separate origin-to-r=2 Frobenius factors must be
restored for the original canonical determinant. A bound on every singular
value of a Frobenius growing-connection matrix is not claimed.

The exact symbolic crosscheck reproduces all 120 Cartesian components of
the frozen ten-channel J1 Hessian from the new universal angular expression.
It also checks the active curvature characteristic polynomial and generic
polynomial decompositions. Run `runs/exact-001/manifest.json` is completed,
has 146 exact checks passed, and validates against its pinned inputs. It
used Python 3.9.6 and SymPy 1.14.0 under a 45-second wall cap and 1-MiB
log cap. No ODE, floating fit, stochastic sample, or larger finite-J scan
was performed. The universal inequalities are hand proofs, with the run
serving as an operator/sign/algebra check. Review status is self-audited;
fresh-agent review remains a separate provenance event.

The next unresolved mathematical step is the ultraviolet large-J symbol
subtraction for the complete gauge/ghost complex in a common regulator,
including relative-wall local terms and origin normalization. The estimates
above do not justify the unregulated infinite angular sum: their high-J
tail is not summable with every degeneracy. No fixed-J coefficient was
assigned a physical finite part. Nonzero Fourier modes, same-holonomy
physical vacuum matching, and the electromagnetic QCD stress insertion
remain additional obligations; no physical alpha prediction follows.

The proof is in `RAW_DERIVATION_v1.md`, the normalized claim and self-review
are in `SELF_AUDIT_v1.md`, and route continuation is in `ROUTE_v1.md`.
`INPUTS_v1.json` and `ARTIFACTS_v1.sha256` supply file-hash provenance.
