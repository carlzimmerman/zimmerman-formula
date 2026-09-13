# Conditional no-go for the local derivative-multiplier class

Assume the trace-free multiplier enters a local action linearly, and that the
same formally self-adjoint spatial operator (P(k^2)) therefore appears in
the two linear Euler equations:

\[
R+P(k^2)\Lambda=0,\qquad P(k^2)d+F(k^2)\Lambda=0,
\]

where (d=\Phi-\Psi), (R\) is a generic nonzero trace-free MOND residual,
and (F) is any finite local quadratic regulator.

For derivative-only couplings (P(0)=0), the zero-mode metric equation reduces
to (R=0), contradicting a generic source.  At (k\ne0), elimination gives

\[
\Lambda=-R/P,\qquad d=F R/P^2.
\]

Thus exact no-slip forces (F=0), while the unregularized multiplier has an
infrared pole whenever (P) has a zero at the origin.  The Python gate tests
orders one through three symbolically; the Lean file proves the zero-mode
contradiction, the finite-mode solution, and the no-slip regulator implication
without hard-coded ranks, PPN values, or DOF counts.

This is a **conditional no-go theorem**, not a universal no-go for arbitrary
nonlocal theories or actions with a different algebraic metric coupling.  It
does, however, close the entire local self-adjoint derivative-multiplier route
represented by the current tensor-compensated branch.
