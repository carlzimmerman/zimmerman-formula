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

## Covariant branch now under test

The direct route around the time-diffeomorphism residual is to replace the
raw ADM gradient by a clock/Stueckelberg acceleration in the same action:

\[
S_{\rm cov}=\int d^4x\sqrt{-g}\left[
 \frac{c^3}{16\pi G_b}(R-2\Lambda)
 -\frac{c^3a_0^2}{8\pi G_b}
 G\!\left(\frac{c^2\sqrt{a_\mu a^\mu}}{a_0}\right)
 +M^4K(X)\right]+S_m[g,\psi],
\]

\[
X=g^{\mu\nu}\nabla_\mu T\nabla_\nu T<0,\qquad
n_\mu=-\frac{\nabla_\mu T}{\sqrt{-X}},\qquad
a_\mu=n^\nu\nabla_\nu n_\mu.
\]

In unitary gauge (T=t), (a_i=D_i\ln N); the static variation therefore
reduces to the exponential constitutive flux already derived above.  The
clock equation is obtained by varying (T), and the metric equation by
varying (g^{\mu\nu}); neither is imposed phenomenologically.  The principal
symbol gates show that the acceleration term alone has zero clock sound speed,
while adding (K(X)=-A\sqrt{1-X^2/L^2}) repairs the clock symbol on a finite
scan at the price of one explicitly propagating clock scalar.  A full
variation including metric/clock mixing, nonlinear constraint algebra, PPN,
FLRW and the Ward identity is still required before this branch can be called
a complete theory.  In particular, the `flrw_clock_background_gate.py` check
shows that a shift-symmetric (K(X)) with (T=t) obeys
(\partial_t(a^3K_X)=0); on an expanding background this forces
(K_X(-1)=0), which removes the gradient repair.  A potential or explicit
clock dependence must therefore be treated as part of the same action rather
than appended after the fact.

The (T=t) specialization is avoidable: on FLRW the conserved shift current
can instead be carried by an evolving \,\(\dot T(a)\).  For the DBI choice and
\(z=\dot T^2/L\), the current equation is

\[
\frac{z^3}{1-z^2}=L\left(\frac{C}{A a^3}\right)^2,
\]

which has one root in (0<z<1) for every positive (a).  The executable
`flrw_clock_evolving_gate.py` verifies this branch and its positive,
subluminal clock symbol.  The resulting homogeneous stress tensor and its
back-reaction on (H(t)) still have to be derived from the same metric
variation; that is the next cosmological closure gate.

The homogeneous lapse variation is now evaluated in
`flrw_clock_friedmann_gate.py`.  With (chi=\dot T^2) and
(z=\chi/L), it gives

\[
\rho=2\chi K_\chi-K=A(1+z^2)/\sqrt{1-z^2},\qquad
p=K=-A\sqrt{1-z^2},qquad
w=-(1-z^2)/(1+z^2).
\]

The conserved current makes the continuity equation exact; the branch is
dust-like as (a\to0) and vacuum-like as (a\to\infty), with a positive-(H)
Friedmann witness.  This advances the FLRW gate, but the full covariant
stress (T^a_{\mu\nu}), metric-clock mixing, and nonlinear constraint algebra
remain to be calculated.

The homogeneous canonical reduction is now explicit: the lapse momentum is
(p_N=0), its preservation gives the Hamiltonian constraint (C=0), and the
two-constraint bracket vanishes on the constraint surface.  With six
homogeneous phase variables this leaves one physical clock scalar.  The
calculation is in `flrw_minisuperspace_dirac_gate.py`; it does not replace the
full spatial Dirac analysis needed to establish (N_{\rm grav}=2).

For a fixed metric, the clock variation can already be written explicitly.
Let (s=\sqrt{-X}), (P_\mu{}^\nu=\delta_\mu{}^\nu+n_\mu n^\nu),
(F(a^2)=-(c^3a_0^2/8\pi G_b)G(c^2\sqrt{a^2}/a_0)), and
(A^\mu=2F_{a^2}a^\mu).  Since

\[
\delta n_\mu=-s^{-1}P_\mu{}^\rho\nabla_\rho\delta T,
\qquad
\delta a_\mu=\delta n^\nu\nabla_\nu n_\mu+n^\nu\nabla_\nu\delta n_\mu,
\]

integration by parts gives the actual (T)-Euler equation

\[
\nabla_\rho\!\left(\frac{P_\mu{}^\rho}{s}
 [A^\alpha\nabla^\mu n_\alpha-\nabla_\nu(A^\mu n^\nu)]\right)
 -2M^4\nabla_\mu(K_X\nabla^\mu T)=0.
\]

The last term is the explicit k-essence clock equation.  The metric equation
has the exact variational form

\[
G_{\mu\nu}+\Lambda g_{\mu\nu}
 =\frac{8\pi G_b}{c^4}\bigl(T^{m}_{\mu\nu}+T^{K}_{\mu\nu}+T^{a}_{\mu\nu}\bigr),
\quad
T^{a}_{\mu\nu}=-\frac{2}{\sqrt{-g}}\frac{\delta S_a}{\delta g^{\mu\nu}},
\]

where the unresolved calculation is to expand (T^a_{\mu\nu}) and its
constraint algebra.  The static weak-field variation is already fully
expanded in `rmmg_constitutive_action.py`; the covariant metric variation,
boosted PPN and FLRW reduction are deliberately not claimed closed.
