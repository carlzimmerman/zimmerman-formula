# WF2 derivative-bimetric gate — bounded result

Date: 2026-09-09

This door tests the local two-metric connection-difference architecture, not
all bimetric theories.  The representative action is

\[
 S=\frac{M^2}{2}\int(\sqrt{-g}R+\sqrt{-\hat g}\hat R)
   +\lambda\int (|g||\hat g|)^{1/4}\,M(T_1,\ldots,T_5)
   +S_m[g,\psi],
\]

where \(C^a{}_{mn}=\Gamma^a{}_{mn}(g)-\Gamma^a{}_{mn}(\hat g)\), and the
quadratic local basis is \(T_1,\ldots,T_5\).  Matter couples only to \(g\).
The tests use the background-independent lapse-velocity-free subspace already
derived in `bimond_5invariant_ghostfree_subspace.py`:

\[
 (c_1,c_2,c_3,c_4,c_5)=(-u_0,-u_1/2,-u_1/2,u_0,u_1).
\]

This is a bounded action-level result.  It is not a universal no-go theorem
for nonlocal, derivative-bimetric, or other theories outside this ansatz.

## Exact obstruction: MOND-alive implies a higher-derivative vector

The independent Stückelberg calculation uses the relative perturbation

\[
 h_{mn}=k_m A_n+k_n A_m+k_mk_n\pi
\]

with \(k_m=(\omega,0,0,\kappa)\).  On the tuned two-dimensional subspace,
the pure \(\pi\) row and column vanish identically, including for explicit
MOND-alive points.  This removes the leading pure-helicity-0 term, but it does
not remove the transverse vector.  For \(A_1\), both independent reruns obtain

\[
 L_{A_1}=-\frac{\lambda}{2}(2u_0+u_1)
       (\kappa-\omega)^2(\kappa+\omega)^2 A_1^2.
\]

The static weak-field acceleration coefficient is independently

\[
 a(u_0,u_1)=-2(2u_0+u_1).
\]

Therefore, within this basis,

\[
 a\ne0\quad\Longrightarrow\quad
 2u_0+u_1\ne0\quad\Longrightarrow\quad
 \deg_{(\omega,\kappa)}L_{A_1}=4.
\]

This is a fourth-order local vector equation (a squared wave operator), not a
two-derivative auxiliary constraint.  The Einstein-Hilbert term vanishes on
the pure relative-diffeomorphism/Stückelberg direction, so it cannot cancel
this term.  The result is an extra propagating higher-derivative mode; in an
ordinary local unconstrained Hamiltonian formulation it carries the
Ostrogradsky ghost.  This is the decisive failure of the two-tensor/healthy
DOF target for the tested architecture.

For the concrete MOND-alive direction \((u_0,u_1)=(1,0)\), the direct
helicity-1 time-kinetic matrix is

\[
 W=\begin{pmatrix}-2&0\\0&9/2\end{pmatrix},
 \qquad \det W=-9,
\]

so one negative direction is visible without the Stückelberg degree-counting
interpretation.  The pure Einstein-Hilbert and Einstein-Hilbert plus
Fierz–Pauli controls give \(W=\operatorname{diag}(0,1/2)\), as expected for
an auxiliary vector component and a healthy control.  The determinant formula
for arbitrary \((u_0,u_1)\) is retained in the raw output; the robust family
statement is the fourth-order operator implication above, not a claim that a
particular two-component kinetic determinant has one sign everywhere.

## Independent lensing calculation

The static quadratic coefficients on the same subspace are

\[
 a=-4u_0-2u_1,\qquad b=-8(u_0+u_1),\qquad x=8u_1.
\]

In the interaction-dominated spherical branch, the unsourced spatial
relative-potential equation gives

\[
 \frac{Q'}{P'}=-\frac{x}{2b}
   =\frac{u_1}{2(u_0+u_1)}.
\]

Setting this ratio to one requires \(u_1=-2u_0\), which simultaneously gives
\(a=0\): the MOND acceleration scalar is dead.  At the concrete
\(T_4-T_1\) point, \(Q'/P'=0\), i.e. maximal scalar-sector under-lensing in
that branch.  When the Einstein-Hilbert term dominates at small relative
gradient, the ratio tends to one, but the radial force scales as \(P'\sim
r^{-2}\), so that limit is Newtonian rather than MOND.  Thus this branch does
not supply MOND enhancement and \(\Phi=\Psi\) in the same regime.

The linear coupled solve does verify that the sum metric obeys the GR scalar
relation (equal summed potentials), while the relative sector carries the
modified response.  That is not sufficient for the physical metric seen by
matter: the nonlinear MOND-dominated relative branch has the slip above.

## Tensor and preferred-frame checks

For \(T_4-T_1\), the two TT polarizations have

\[
 f_{\rm total}=(1/4+2\lambda)(\omega^2-\kappa^2),
 \qquad c_T^2=1,
\]

with positive tensor kinetic coefficient for the tested \(\lambda>0\).  This
is a genuine pass for that bounded tensor-speed test, not a pass for the full
theory.  The coupled-lensing script identifies the two-metric response as
hyperbolic/retarded, so it does not inherit the instantaneous-MMG
\(\alpha_3=O(1)\) mechanism.  A complete covariant PPN derivation was not
needed after the vector obstruction and is not claimed here.

## Reproduction and statuses

The orchestration script records raw stdout/stderr, source hashes, exact
commands, runtimes, and child return codes without encoding expected physical
values:

```text
PYTHONDONTWRITEBYTECODE=1 python3 -B \
  qwen_claude_field_theory/closure_2026/bimetric_secondfield/run_wf2_suite.py \
  --output qwen_claude_field_theory/closure_2026/bimetric_secondfield/wf2_suite_results.json
```

The suite exited 0 as an execution result; each child returned 0.  The
scientific gate is nevertheless **FAIL** because the child calculations find
the higher-derivative vector obstruction and the MOND/slip incompatibility.
The recorded runtimes were approximately 0.93 s (BD/Stückelberg), 3.08 s
(vector), 1.48 s (coupled lensing), 0.36 s (tensor), and 2.07 s (independent
vector adjudicator).

Raw evidence is in `wf2_suite_results.json`.  The direct scripts are
`wf2_indep_bdghost_reverify.py`, `wf2_vecghost_hel1.py`,
`wf2_adjudicator_vecghost_indep.py`, `wf2_coupledlens_alpha3.py`, and
`wf2_tensor_cT_gate.py`.

Conclusion for this door: **DEAD for the requested healthy MOND theory**;
the statement is bounded to the displayed local derivative-bimetric action
and its tuned five-invariant subspace.  A new action would have to remove the
relative vector's \(\Box^2\) term while retaining a nonzero static acceleration
coefficient, and then redo the full Hamiltonian, lensing, cosmology, and
stability analysis from scratch.

## Nonlinear-background strengthening

The Minkowski calculation assumes a nonzero quadratic coefficient.  To test
whether an exact MOND function could evade it by becoming nonlinear, the
additional `wf2_nonlinear_vector_background.py` freezes a static background
with \(p=\partial_z\Phi\), \(q=\partial_z\Psi\), and expands the same
\(T_4-T_1\) interaction around it.  It obtains, exactly,

\[
 \bar T=-4(p^2+2q^2),\qquad \delta T=0,
\]

and, writing \(M_1=M'(\bar T)\),

\[
 W=\begin{pmatrix}-2M_1&0\\0&4M_1\end{pmatrix},
 \qquad \det W=-8M_1^2,
\]

with

\[
 \det H=-8M_1^2(\kappa^2-\omega^2)^2.
\]

Thus every nonzero background with \(M'(\bar T)\neq0\) has an indefinite
vector principal kinetic matrix in this local orientation.  The deep-MOND
representative \(M(T)=(-T)^{3/2}\) gives

\[
 W=\operatorname{diag}\bigl(3\sqrt{p^2+2q^2},
              -6\sqrt{p^2+2q^2}\bigr).
\]

An exact constitutive law can avoid this local conclusion only at a point where
\(M'(\bar T)=0\), which makes the MOND principal symbol degenerate and invokes
the separate strong-coupling/zero-field gate.  This strengthens the bounded
obstruction from a Minkowski quadratic test to a nonzero-background principal
symbol, while remaining limited to \(T_4-T_1\), the displayed local action,
and the chosen static alignment.

Reproduction:

```text
PYTHONDONTWRITEBYTECODE=1 python3 -B \
  qwen_claude_field_theory/closure_2026/bimetric_secondfield/wf2_nonlinear_vector_background.py
```

This command exited 0 and printed the symbolic matrices and determinants
above.  No expected rank or determinant is hard-coded in the script.
