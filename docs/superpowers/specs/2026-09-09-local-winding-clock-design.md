# Local Winding Clock MOND Design

## Purpose and status

This specification defines a new constructive candidate inspired by the
L75 cumulative-winding opening.  It is not a declaration that the target
theory exists.  The candidate is accepted only gate-by-gate from one explicit
action; a failed gate falsifies this branch but does not silently transfer a
PASS from another model.

The architectural idea is to retain the integrable-clock exponential MOND
sector and add a local first-order memory clock \(Q\).  \(Q\) gates a primordial
cold sector through a positive transmission function.  The cold sector is
metric-minimally coupled, so ordinary baryons remain minimally coupled to the
same physical metric and their Ward identity is tested separately.

## Candidate action

Use signature \((-+++)\), \(X_T=-g^{\mu\nu}T_\mu T_\nu/2>0\),

\[
 n_\mu=-T_\mu/\sqrt{2X_T},\quad
 h_{\mu\nu}=g_{\mu\nu}+n_\mu n_\nu,\quad
 a_\mu=n^\nu\nabla_\nu n_\mu,
\]

and the IC1 variables

\[
 u\in(0,1),\quad w=(u-1)\ln N,\quad
 W=n^\mu\nabla_\mu w,\quad Q_{\mu\nu}=K_{\mu\nu}-h_{\mu\nu}W.
\]

The proposed action is

\[
\begin{aligned}
 S={}&S_{\rm IC1}[g,T,u]
 +\int d^4x\sqrt{-g}\,\lambda
   \left(n^\mu\nabla_\mu Q-\mathcal W(\Theta)\right)\\
 &+S_{\rm cold}[g,\chi_c;Q]+S_m[g,\psi_b],
\end{aligned}
\]

where \(\Theta=\nabla_\mu n^\mu/3\),

\[
 \mathcal W(\Theta)=\sqrt{\Theta^2+\varepsilon_w^2}-\varepsilon_w,
 \qquad
 S_{\rm cold}=\int d^4x\sqrt{-g}\,e^{-\beta Q}\mathcal L_c(g,\chi_c).
\]

The smooth regulator \(\varepsilon_w>0\) is retained during variation and
the \(\varepsilon_w\to0^+\) limit is a separate gate.  On an expanding
homogeneous branch, \(\dot Q\simeq H\), so \(Q\) measures local integrated
e-folding.  The exact exponential MOND primitive remains the IC1 primitive;
the new terms are tested first on the baryon-only branch \(\chi_c=0\).

The cold Lagrangian is fixed at the first gate to the explicit canonical
massive scalar

\[
 X_c=-\tfrac12 g^{\mu\nu}\nabla_\mu\chi_c\nabla_\nu\chi_c,
 \qquad \mathcal L_c=X_c-\tfrac12m_c^2\chi_c^2.
\]

Coherent nonrelativistic oscillations of this field provide the cold,
dust-like limit, while its fundamental kinetic sign is directly testable.
No phenomenological density term may replace this action.  The exponential
factor is dimensionless and positive for finite Q.

## Intended mechanism

The memory equation is action-derived:

\[
 n^\mu\nabla_\mu Q=\mathcal W(\Theta).
\]

The cold stress is multiplied by \(e^{-\beta Q}\), but no direct
nonmetric force is applied to baryons.  Diffeomorphism invariance implies

\[
\nabla_\mu T_b^{\mu\nu}=0
\]

on the baryon equations, while the cold-plus-memory sector has an exchange
identity that must be derived rather than assumed.  The proposed ordering is

\[
 Q_{\rm rec}\approx0,
 \qquad Q_{\rm gal}>Q_{\rm cl},
 \qquad
 \eta(Q)=e^{-\beta Q},
\]

using the L75 representative assembly values
\(Q_{\rm gal}\simeq\ln3\) and
\(Q_{\rm cl}\simeq\ln1.7\).  These values are calibration inputs for a
diagnostic, not a derivation from cosmological structure formation.

## Gate sequence

### Gate 1 — exact variation

Derive the Euler–Lagrange equations for (g,T,u,Q,\lambda,\chi_c) from the
displayed action.  Keep the regulator, boundary terms, and cold-sector
variation explicit.  Confirm that the IC1 static primitive remains
\(\mu(y)=1-e^{-y}\) when \(\chi_c=0\).

### Gate 2 — canonical/Dirac closure

In a fixed clock foliation with shift retained, compute the velocity Hessian
and all primary constraints.  For the memory block the expected candidates
are derived, not inserted:

\[
 p_\lambda=0,
 \qquad C_Q=p_Q-\sqrt h\lambda=0.
\]

Compute the full Poisson matrix, preserve every constraint, and separate
nonzero spatial modes from \(k=0\).  The result must explicitly report the
remaining \(Q\) phase-space pair as a genuine clock degree of freedom if the
bracket calculation gives that result.  No expected rank or DOF count may be
hard-coded.

### Gate 3 — weak field and Ward identities

Vary lapse and spatial metric independently.  Derive \(\Phi\) and \(\Psi\)
separately on the baryon-only branch, extract measured \(G_N\), and compute
the cold-source correction.  Derive the baryon Ward identity and the
cold-plus-memory exchange identity from the same action.

### Gate 4 — FLRW and local winding

Derive the homogeneous equations without imposing \(H=0\), solve for an
expanding branch, and integrate the actual \(Q\) equation.  Then compare the
derived local histories with the L75 ordering; representative values may be
used only as a falsifiable calibration, not as proof.

### Gate 5 — perturbations and stability

Compute scalar, vector, and tensor principal matrices on the expanding branch.
The memory mode must be explicitly counted and have no ghost or gradient
instability.  The tensor cone must satisfy \(c_T^2=1\).  Any instantaneous
physical channel or extra hidden pole is a failure.

### Gate 6 — PPN and empirical predictions

Derive \(\gamma,\beta,\alpha_1,\alpha_2,\alpha_3\) from the same action,
then test the exponential MOND law, galaxy/cluster transmission, and the
orbital/supernova ledgers.  No static weak-field result is promoted to a full
PPN result without the moving-source calculation.

## Lean boundary

The workspace currently has no Lean executable or lake project.  The first
implementation will export exact SymPy identities (primitive derivative,
memory constraint bracket, and Ward residuals) to a deterministic JSON file
with a Lean-shaped statement file.  That output is explicitly labelled
Lean-ready, not Lean-compiled, until a compiler and mathlib environment are
available.

## Success and failure semantics

The candidate is **OPEN** until every gate is derived from this action.  A
successful local winding calibration is not a theory PASS.  A failed causal,
PPN, FLRW, or stability gate kills this candidate branch and records the exact
obstruction.  The global research goal remains active unless a complete
theory or a clearly scoped universal theorem is actually proved.
