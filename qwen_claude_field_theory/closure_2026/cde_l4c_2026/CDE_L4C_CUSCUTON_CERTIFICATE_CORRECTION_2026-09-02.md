# CDE-L4C cuscuton certificate correction — updated 2026-09-03

## Corrected result

The existing CDE-L4C scripts do not establish \(N_{\rm grav}=2\) for the
advertised cuscuton-plus-four-constraint architecture.

The structural gate inferred a primary constraint from the finite
large-velocity asymptote of the cuscuton momentum. That inference is invalid:
an asymptote is not a degenerate Legendre map, and the momentum is not even
globally bounded on the timelike domain. The later \(4\times4\) PB program
omits \((\chi,p_\chi)\), contains a previously unreported rank-drop surface,
and assigns rather than action-derives its principal MOND constraint.

## Full ADM Legendre calculation

Define
\[
A=\dot\chi-N^iD_i\chi,\qquad
S=\gamma^{ij}D_i\chi D_j\chi,
\]
and take the timelike branch of
\[
L_{\rm cusc}=\sqrt\gamma M^2\sqrt{A^2-N^2S}
-N\sqrt\gamma V(\chi).
\]
Direct differentiation gives
\[
p_\chi={\sqrt\gamma M^2A\over\sqrt{A^2-N^2S}},
\qquad
{\partial p_\chi\over\partial\dot\chi}
=-{\sqrt\gamma M^2N^2S\over(A^2-N^2S)^{3/2}}.
\]

For \(S>0\), parameterize the physical domain by
\(A=N\sqrt{S+u^2}\), \(u>0\). Then
\[
{\partial p_\chi\over\partial\dot\chi}
=-{\sqrt\gamma M^2S\over Nu^3}<0.
\]
The positive-branch inverse and Hamiltonian are
\[
\dot\chi=N^iD_i\chi
+{Np_\chi\sqrt S\over\sqrt{p_\chi^2-\gamma M^4}},
\]
\[
H_{\rm cusc}=N^ip_\chi D_i\chi
+N\sqrt S\sqrt{p_\chi^2-\gamma M^4}
+N\sqrt\gamma V(\chi).
\]
Hence the one-variable inhomogeneous Legendre map is invertible. Although
\(p_\chi\to\sqrt\gamma M^2\) as \(A\to+\infty\), it diverges as
\(A\to N\sqrt S\) from inside the timelike domain. It is not globally
bounded.

At \(S=0\), instead,
\[
p_\chi=\sqrt\gamma M^2\operatorname{sgn}A,
\qquad
{\partial p_\chi\over\partial\dot\chi}=0.
\]
The positive branch has
\(p_\chi-\sqrt\gamma M^2\approx0\). The displayed Legendre rank therefore
changes between \(k=0\) and \(k\ne0\). An algebraic \(a_0(\chi)F(y)\) term
adds zero to both Hessians and does not create the missing inhomogeneous
primary.

This calculation does **not** assert that standard cuscuton gravity contains
a local propagating scalar. Its absence, when it holds, follows only after
the complete coupled gravity constraint analysis. It cannot be imported from
the invalid one-variable argument used by this certificate.

## Audit of the four-constraint subsystem

The source of `gateA/cde_l4c_covariant_dirac_rank.py` declares
\[
Q=(\Phi,\Psi,B,\lambda),\qquad
P=(p_\Phi,p_\Psi,p_B,p_\lambda),
\]
so the cuscuton pair is absent. The program's exact determinant is
\[
\det\Delta=c_s^2 k^8
\left(2B_p+\lambda_\parallel a_0^2\right)^2.
\]
The generic rank is four, but it drops to two at
\[
B_p=-{1\over2}\lambda_\parallel a_0^2.
\]
Thus \(\lambda_\parallel>0\) does not by itself guarantee nonsingularity.

The displayed momentum-constraint brackets are not all zero and have not
been shown to be combinations of the constraints. Its first-class closure is
therefore unproved. Finally, the program's \(C_{\rm MOND}\) is an assigned
principal surrogate: no one frozen nonlinear action in this directory is
varied to generate the whole chain.

## Consequence and next calculation

The old certificate is refuted; the architecture itself is not yet
falsified. CDE-L4C is **OPEN / NOT CERTIFIED**. The unavoidable calculation
is to freeze the nonlinear action and perform the full gravity + lapse +
shift + cuscuton + auxiliary Dirac algorithm, including all primaries,
preservation through closure, functional PBs, and separate \(k=0\) and
\(k\ne0\) sectors. Only a successful full count permits a meaningful PPN,
FLRW, Ward-identity, or stability certification.

## Reproducibility

- `cde_l4c_cuscuton_legendre_audit_2026.py`: 8 derived checks.
- `test_cde_l4c_cuscuton_legendre_audit_2026.py`: 7 regression tests.
- `cde_l4c_cuscuton_legendre_audit_2026.out`: observed output.

The script differentiates the full ADM density with shift, spatial volume
factor, and potential; verifies the inverse Legendre map on an explicitly
parameterized physical domain; takes both velocity-boundary limits; parses
the certificate phase-space lists; rebuilds its PB matrix; and derives its
generic and cancellation ranks. No rank, determinant, or DOF count is
hard-coded as a reported result.
