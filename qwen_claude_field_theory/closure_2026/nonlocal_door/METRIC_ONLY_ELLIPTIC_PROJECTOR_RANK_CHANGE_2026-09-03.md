# Metric-only elliptic projector: corrected rank-changing result — 2026-09-03

## Verdict

The broad claim that every regular metric-only elliptic projector is excluded
is **withdrawn**. The executable result is the narrower Minkowski stabilizer
lemma:

> A continuous Poincare-equivariant symmetric tensor evaluated at exact
> Minkowski cannot be a **nonzero** rank-three spatial projector. Its value is
> (H^{\mu\nu}=B\eta^{\mu\nu}), with rank four for (B\ne0) and rank zero
> for (B=0).

The loophole is a tensor that is rank three away from zero field and vanishes
smoothly at zero. The new scripts construct that loophole, derive its
rank-changing constraint matrix, and kill one explicit Ricci-polynomial
realization. They do not close every spectral or nonlocal metric projector.

## 1. Exact stabilizer result and varied multiplier action

For

\[
S_{\rm aux}=\int d^4x\sqrt{-g}\,\lambda
\left(H^{\mu\nu}\nabla_\mu\nabla_\nu\chi-J\right),
\]

rotations and one exact Lorentz boost give

\[
H^{\mu\nu}=B\eta^{\mu\nu}\quad\hbox{or}\quad0.
\]

The nonzero Fourier-mode Lagrangian is

\[
L=-A\dot\lambda\dot\chi-Bk^2\lambda\chi-J\lambda,
\]

and independent variation gives

\[
E_\lambda=A\ddot\chi-Bk^2\chi-J,
\qquad
E_\chi=A\ddot\lambda-Bk^2\lambda.
\]

On the Lorentz branch (A=-B), the derived velocity Hessian has determinant
(-B^2), empty null space, and eigenvalues ((-B,+B)). Its Legendre map is
regular, so the ordinary localized action has two auxiliary modes and one
negative kinetic direction.

For a fixed genuinely spatial coefficient (B>0) and (k\ne0), the two
primary and two secondary constraints have

\[
C_{AB}=
\begin{pmatrix}
0&0&0&-Bk^2\\
0&0&-Bk^2&0\\
0&Bk^2&0&0\\
Bk^2&0&0&0
\end{pmatrix},
\qquad \det C=B^4k^8.
\]

Preservation solves both multipliers and leaves no tertiary constraint. Thus
the fixed-background (k\ne0) auxiliary pair has four second-class
constraints and zero modes.

## 2. Smooth vanishing-projector counterexample

Let (V^\mu) be timelike and (X=-V^2>0). Then

\[
H^{\mu\nu}=Xg^{\mu\nu}+V^\mu V^\nu
=X(g^{\mu\nu}+u^\mu u^\nu)
\]

is polynomial in (V), has mixed eigenvalues ((0,X,X,X)), and is positive
on the spatial cotangent subspace. As (V\to0), (H\to0) independently of
the direction from which (V) approaches zero. Multiplying by the vanishing
amplitude removes the path dependence of the normalized frame. This is an
explicit counterexample to the broad regular-projector claim.

For (X=\epsilon_V^2), the fixed-mode Poisson determinant becomes

\[
\det C=\epsilon_V^8 k^8,
\]

and its rank changes from four to zero at (epsilon_V=0). If
(J=\epsilon_V J_1), the solution scales as

\[
\chi=-{J_1\over\epsilon_V k^2},
\]

so the linear response is unbounded. This establishes a rank bifurcation and
a necessary strong-coupling test, not a universal no-go: nonlinear degenerate
ellipticity may still control a zero-field solution.

The momentum-space tensor

\[
\Theta^{\mu\nu}=g^{\mu\nu}-{k^\mu k^\nu\over k^2}
\]

does not repair the construction. When used on the same Fourier mode,
(\Theta^{\mu\nu}k_\mu k_\nu=0); it supplies no second-order operator. It is
also undefined at (k^2=0).

## 3. The fixed-flat zero mode is not FLRW

The statement (J_0=0) applies to the exact-Minkowski fixed-background toy
or to the intrinsic spatial Laplacian. For the covariant contraction on flat
FLRW, the script derives the Christoffel symbols and obtains

\[
h^{\mu\nu}\nabla_\mu\nabla_\nu\chi
=D^2\chi-3H\dot\chi.
\]

A homogeneous field therefore obeys

\[
-3BH\dot\chi=J,
\qquad
\dot\chi=-{J\over3BH},
\]

so expanding FLRW can carry a nonzero homogeneous source. Its first-order
term mixes the metric, (lambda), and (chi) momenta; the complete
minisuperspace Dirac chain remains open.

## 4. A pure-metric polynomial construction and its failure

Define the traceless mixed Ricci tensor and polynomial

\[
S^\mu{}_\nu=R^\mu{}_\nu-{R\over4}\delta^\mu{}_\nu,
\qquad
P^\mu{}_\nu={3\over4}\operatorname{tr}(S^2)\delta^\mu{}_\nu
-(S^2)^\mu{}_\nu.
\]

On Ricci Segre type ({1,(111)}), where
(\operatorname{spec}S=(-3d,d,d,d)), the script derives

\[
\operatorname{spec}P=(0,8d^2,8d^2,8d^2).
\]

Thus (P) is a smooth rank-three scaled spatial projector for (d\ne0) and
vanishes at flat space. But generic anisotropy kills this particular choice.
For spatial eigenvalues (s_i),

\[
P^0{}_0={
(s_1-s_2)^2+(s_1-s_3)^2+(s_2-s_3)^2
\over4}.
\]

Any unequal (s_i) gives (P^{00}<0). Freezing the local principal symbol,
the ((\dot\lambda,\dot\chi)) Hessian then has eigenvalues
(\pm|P^{00}|): a ghost-signed auxiliary pair. The block vanishes
quadratically at exact isotropy, so a linear FLRW calculation would miss the
rank change.

The Bianchi-I highest-derivative calculation independently finds, for
(A_i=\dot H_i),

\[
\sum_i P^i{}_i={5\over4}\sum_i A_i^2
+{1\over4}\left(\sum_iA_i\right)^2.
\]

Its acceleration Hessian has eigenvalues proportional to
((4,5/2,5/2)); both traceless shear accelerations are nondegenerate. A
reduced Ostrogradsky Hamiltonian retaining the multiplier has one primary and
one secondary constraint. Their computed (2\times2) Poisson matrix is full
rank, preservation fixes the multiplier, and no tertiary remains. The phase
count is four shear-sector modes rather than the two second-order shears, and
the Hamiltonian is linear in both Ostrogradsky momenta. This explicit
Ricci-polynomial candidate is therefore **DEAD**.

This is candidate-specific. A nonanalytic exact spectral projector selecting
the unique timelike Ricci eigenvalue is outside this polynomial calculation.

## 5. Multiplier, effective stress, and ordinary-matter Ward identity

The bare multiplier does not manufacture phantom stress. For an invertible
fixed elliptic mode, variation of (chi) gives

\[
-fk^2\lambda=0\quad\Longrightarrow\quad\lambda=0.
\]

Every metric variation of the displayed auxiliary sector is then
proportional to (lambda) or its derivatives, so it vanishes on shell under
standard homogeneous boundary data. Adding (U(\chi)) gives instead

\[
\lambda={U'(\chi)\over fk^2},
\]

which can source the metric but activates the stability and rank problems.

There is a second exact fork. If (J=J[g,T(g,\psi)]), the auxiliary action
depends directly on ordinary matter. Its full matter equation is

\[
E_\psi^m+E_\psi^{\rm aux}=0,
\]

while the separate matter-action Ward identity is

\[
\nabla_\mu T_m^{\mu\nu}=E_\psi^m\nabla^\nu\psi
=-E_\psi^{\rm aux}\nabla^\nu\psi.
\]

It is generically nonzero. Only the total stress is conserved. Requiring the
ordinary (S_m) tensor to be separately conserved forces
(\delta J/\delta\psi=0), so the source must be reconstructed from metric
data or enter indirectly through the metric equations. That broader
metric-source architecture remains open.

## 6. Reproducibility and research status

- `metric_only_elliptic_projector_gate_2026.py`: 12 derived diagnostics.
- `test_metric_only_elliptic_projector_gate_2026.py`: 13 tests.
- `ricci_polynomial_projector_gate_2026.py`: 5 derived diagnostics.
- `test_ricci_polynomial_projector_gate_2026.py`: 6 tests.

All algebra is exact SymPy algebra with no randomness. A zero exit status
means the scripts reproduced these scoped statements, not that a theory
passed the fried-chicken requirements.

**Status:** the simple Ricci-polynomial projector is **DEAD**. The general
rank-changing metric-spectral/metric-source branch is **OPEN**. The next
unavoidable calculation is an explicit spectral-projector action with its
full metric variation, lapse-retaining Bianchi-I/FLRW Dirac analysis, and a
derived map from the curvature invariant to physical
(y=|\nabla\Phi|/a_0).
