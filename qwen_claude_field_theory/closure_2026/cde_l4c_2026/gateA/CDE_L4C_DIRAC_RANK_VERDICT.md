# CDE-L4C truncated Dirac-rank result — full-action count OPEN (corrected 2026-09-03)

The executable `cde_l4c_covariant_dirac_rank.py` computes a useful algebraic
result for its declared four-pair scalar phase space. It is not a covariant
Dirac closure or a certificate that the proposed full action has
\(N_{\rm grav}=2\).

## What the program actually defines

The canonical coordinates are
\[
Q=(\Phi,\Psi,B,\lambda),\qquad
P=(p_\Phi,p_\Psi,p_B,p_\lambda).
\]
There is no \((\chi,p_\chi)\) pair. Moreover, no single nonlinear CDE-L4C
action is frozen in this directory. The program assigns the principal
surrogate
\[
C_{\rm MOND}=\lambda_\parallel a_0^2 k^2\Phi
+B_pk^2(\Phi+\Psi)+p_\Psi+\rho_b
\]
rather than deriving it anew by preserving the primaries of such an action.

For the declared ordered set
\(\{p_N,C_{\rm MOND},C_K,C_{\rm slip}\}\), it derives
\[
\Delta=
\begin{pmatrix}
0&-(B_p+\lambda_\parallel a_0^2)k^2&0&-c_sk^2\\
(B_p+\lambda_\parallel a_0^2)k^2&0&B_pk^2&c_sk^2\\
0&-B_pk^2&0&c_sk^2\\
c_sk^2&-c_sk^2&-c_sk^2&0
\end{pmatrix}
\]
and
\[
\det\Delta=c_s^2 k^8
\left(2B_p+\lambda_\parallel a_0^2\right)^2.
\]
Thus the submatrix has rank four for generic nonzero \(k\) and generic
coefficients, but rank two on
\[
B_p=-{1\over2}\lambda_\parallel a_0^2.
\]
The older prose incorrectly stated a nonzero condition using only
\(\lambda_\parallel>0\); that positivity does not exclude this cancellation.

Solving the two assigned weak-field constraints gives \(\Psi=\Phi\) and a
nonzero source-dependent potential within the toy subsystem. This is not an
independent variation of one full action, and it cannot establish the
physical metric response or PPN parameters.

The displayed momentum-constraint brackets vanish with \(p_N\) but not with
all other members of the set. They have not been reduced to combinations of
constraints, so first-class spatial-diffeomorphism closure is also open.

## Correct status

- **Established:** an exact symbolic PB matrix, its generic rank-four branch,
  its rank-two cancellation surface, and a sourced no-slip solution inside
  the declared truncated model.
- **Not established:** all primaries and secondaries of one action,
  preservation to genuine closure, first/second-class classification of the
  full system, or \(N_{\rm grav}=2\).
- **Next:** include \((\chi,p_\chi)\), lapse, shift, the full ADM metric phase
  space, and every auxiliary pair in a Hamiltonian obtained from one explicit
  nonlinear action; then run the functional Dirac algorithm separately at
  \(k=0\) and \(k\ne0\).

**Verdict: the old full-action certificate is WITHDRAWN. CDE-L4C remains
OPEN / NOT CERTIFIED.**
