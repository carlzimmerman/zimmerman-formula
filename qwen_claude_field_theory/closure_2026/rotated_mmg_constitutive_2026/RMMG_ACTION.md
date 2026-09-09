# Rotated-MMG constitutive candidate (2026)

This directory records a new, explicitly varied candidate rather than a
phenomenological assertion.  It is inspired by the two-degree-of-freedom
Hamiltonian constructions of Bojowald--Duque and Yao et al.; the Navier--Stokes
formalization workflow is used here only as a reproducibility model (small
kernel, executable gates, and a separate formal arithmetic witness).

## Candidate action

Use ADM variables and the rotated scalar combinations

\[
 u=\log N-\frac16\log h,\qquad
 r=\log N+\frac16\log h,\qquad h=\det h_{ij},
\]

so that \(u=2\Phi/c^2\) and \(r=(\Phi-\Psi)/c^2\) on the linear static
branch.  A first-order action for the candidate is

\[
 S=\int dt\,d^3x\,[\pi^{ij}\dot h_{ij}+p_u\dot u+p_r\dot r
 +P_T\dot T-N\mathcal C_\perp
 -N^i(\mathcal H_i+\mathcal H_i^m)-\lambda_R\mathcal C_R].
\]

The matter Hamiltonian \(\mathcal H_m\) is the minimally coupled matter
Hamiltonian of the *same* metric \(g(N,N^i,h)\).  The proposed geometric
constraints are

\[
 \mathcal C_\perp=\frac{\sqrt h}{8\pi G_b}
 D_i\!\left[\mu(Y)D^iu\right]+\mathcal H_m+\mathcal H_{TT}+\mathcal H_{\rm clock},
 \quad
 \mathcal C_R=\sqrt h\,D^2r,
\]

with \(Y=c^2|Du|/(2a_0(T))\) and \(\mu(Y)=1-e^{-Y}\).  Matter therefore
enters the same lapse constraint as the constitutive geometry, not an
explicitly nonmetric force in \(S_{\rm aux}\).  Whether the full nonlinear
constraint algebra makes this an honest four-dimensional generally covariant
theory is an open gate.

## Independent weak-field variation

The static scalar part obtained by expanding the same constitutive term is

\[
 \mathcal L_{\rm stat}=
 2|\nabla\Psi|^2-4\nabla\Phi\!\cdot\!\nabla\Psi
 -2a_0^2G(|\nabla\Phi|/a_0)+2|\nabla\Phi|^2
 -16\pi G_b\rho_b\Phi,
\]

where

\[
G(y)=y^2+2(1+y)e^{-y}-2,
\qquad \frac{G'(y)}{2y}=1-e^{-y}.
\]

Varying \(\Psi\) and \(\Phi\) independently gives

\[
 \Delta(\Psi-\Phi)=0,
\]

and, after using that independently derived slip equation,

\[
 \nabla\!\cdot\![\mu(|\nabla\Phi|/a_0)\nabla\Phi]
 =4\pi G_b\rho_b.
\]

Thus this finite gate derives \(\Phi=\Psi\), \(\gamma_{\rm PPN}=1\), and the
exact exponential law.  The executable variation is in
`rmmg_constitutive_action.py`; no coefficient is inserted into the result.

## Dirac sector

### Auxiliary-relay refinement

The local (p^2) Hamiltonian used for the first witness is not the preferred
completion.  The cleaner relay keeps (u,r) genuinely auxiliary:

\[
 S_{\rm relay}=\int[ p_u\dot u+p_r\dot r-N(\mathcal V_M+\mathcal V_R
 +\mathcal H_m+\mathcal H_{TT}+\mathcal H_{\rm clock})
 -\lambda_u p_u-\lambda_r p_r+\cdots],
\]

with \(\mathcal V_M=2a_0^2G(c^2|Du|/(2a_0))\) and
\(\mathcal V_R=\tfrac12|Dr|^2\).  The primary constraints are
\(p_u=p_r=0\); their preservation generates the constitutive and slip
equations.  Thus the elliptic equations are secondary constraints of the
same action, not phenomenological multiplier equations.  The script
`auxiliary_relay_dirac.py` computes the resulting Hessian/Poisson matrix and
continues preservation.  At the local witness it has full computed rank and
zero scalar phase dimension; at \(k=0\) the rank drops to zero.

For one Fourier mode the scalar constraints are

\[
 C_M=k^2[1-e^{-ku/(2a_0)}]u-\rho_k,\qquad C_R=k^2r.
\]

Preservation under \(H_0=(p_u^2+p_r^2+k^2u^2+k^2r^2)/2\) gives
\(P_M=\{C_M,H_0\}\) and \(P_R=\{C_R,H_0\}\).  The script constructs
\(M_{ab}=\{\chi_a,\chi_b\}\), \(\chi=(C_M,C_R,P_M,P_R)\), then computes
its numerical rank.  At \((k,u,a_0)=(1,2,1)\), the matrix is the canonical
four-by-four antisymmetric block matrix with determinant \(1\), rank 4, and
zero remaining scalar phase dimension.  At \(k=0\), every spatial operator
vanishes and the computed matrix is zero (rank 0): the homogeneous sector is
not silently identified with the local sector.

## What this does and does not establish

The finite gates establish an action-level static constitutive law and an
actual local scalar constraint closure witness.  They do **not** yet establish
the nonlinear hypersurface-deformation algebra, the ordinary-matter Ward
identity, boosted PPN \(\beta,\alpha_1,\alpha_2,\alpha_3\), full FLRW perturbation
stability, or a controlled \(y\to0\) completion.  The candidate is therefore
`OPEN`, not closed; these are the next unavoidable calculations.
