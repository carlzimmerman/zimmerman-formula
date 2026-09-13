# Screened versus hyperbolic compensator

At the operator level, replacing the pure Laplacian by

\[
P(k,\omega)=k^2+m^2-\omega^2/c^2
\]

gives

\[
\Lambda=-R/P.
\]

For (m>0) and a purely spatial operator ((c=0) understood as no time
derivative), the static response is finite at (k=0):
\(Lambda(0)=-R/m^2\).  This is the only promising IR escape, but it introduces
a new screening length and has not been derived from the covariant action.

If the operator is promoted to a wave operator, its poles are

\[
\omega^2=c^2(k^2+m^2),
\]

so the auxiliary sector contains a propagating mode.  Setting (c=0) avoids
that pole but returns an instantaneous elliptic channel.  The executable gate
checks these identities without hard-coded ranks, PPN values, or DOF counts.

This is a fork, not a closure: the next construction must show whether a
covariant, single-metric action can realize the (m>0), purely spatial operator
while retaining exact exponential MOND and (Phi=\Psi) without a forbidden
instantaneous physical channel.
