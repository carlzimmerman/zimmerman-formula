# IC6: actual secondary drift and a full-metric homogeneous preservation test

Base `0b75e72bf5797e451beb258847ade528cd9c4551`, 2026-09-08.
**Bounded preservation result; full inhomogeneous theory OPEN.**

The same IC6 Hamiltonian yields a nonzero secondary–secondary bracket on a
genuinely shearing, numerically constrained Bianchi I state. Its computed
multiplier cancels the actual canonical drift. An unprojected integration of
all six metric components, their six momenta, both auxiliaries and their
primary momenta preserves the constraints to the measured integration error.
This is a finite homogeneous reduction. Spatial derivatives, spatial momentum
constraints, shift variables and matter are not part of its numerical phase
space. In particular, its count is not the field theory's polarization count.

## 1. Continuum density and its full canonical metric derivatives

Here \(g_{ij}\) denotes the **barred canonical leaf metric**, not the physical
metric. All \(D,R,R^{ij}\) in this note use this barred metric. Work on the
expanding activation plateau, with \(J_T>0\), and on a periodic leaf (or with
boundary conditions justifying the displayed integrations by parts). Set

\[
V=\sqrt{\det g},\quad p^{ij}=\frac{\bar\pi^{ij}}V,\quad
\rho=g_{ij}p^{ij},\quad
\tau=g_{ik}g_{j\ell}p^{ij}p^{k\ell}-\rho^2/3,\quad
q=(\xi,u),\quad z_i=D_i(\xi+bu),\quad Z=g^{ij}z_i z_j.
\]

The symbol \(p^{ij}\) here is a normalized metric momentum; the auxiliary
primary momenta are separately denoted \(p_A\). With all action constants
unchanged from [IC5_ACTION.md](IC5_ACTION.md) and
[TENSOR_BALANCE.md](TENSOR_BALANCE.md), define

\[
\begin{aligned}
E&=e^{(4-3u)\xi},&G&=e^{u\xi},&w&=(u-1)\xi,\\
J&=1+\frac{e^{-6w}\rho^2F}{m^2a_0^2},&
\chi&=-\frac m2G-\frac{e^{(6-5u)\xi}\rho^2F}{2ma_0^2},&
B&=m\alpha G,\\
h_{\mathrm{ng}}&=\frac{2E}{m}\left(\frac\tau J-\frac{\rho^2}6\right)
 +m e^{(3u-2)\xi}C-\frac\kappa2e^{(3u-4)\xi}+\chi R,
&C&=\Lambda+a_0^2U(u^2),\\
H&=\int d^3x\,Vh,&h&=h_{\mathrm{ng}}-BZ.
\end{aligned}
\]

The integrand \(h_{\mathrm{ng}}\) is distinct from the action's expansion
constant \(h_0=\sqrt{\kappa/(6m)}\).

In particular, the curvature coefficient is the one in IC5, and IC6 changes
the shear coefficient to \(1/J\). Their dependence on \(\rho\) contributes
to metric velocity; holding that momentum dependence fixed would give the
wrong drift.

For any scalar density integrand \(\psi(\rho,\tau,R,q,Dq,Df)\), define

\[
\begin{aligned}
\mathcal U^{ij}&=p^{ij}-\tfrac12\rho g^{ij},\\
\mathcal W^{ij}&=2p^{ik}g_{k\ell}p^{\ell j}
 -\tfrac23\rho p^{ij}-\tau g^{ij},\\
\mathcal E^{ij}[\psi,L]&=\tfrac12g^{ij}\psi
 +\psi_\rho\mathcal U^{ij}+\psi_\tau\mathcal W^{ij}+L^{ij}
 -\psi_R R^{ij}+(D^iD^j-g^{ij}\Delta)\psi_R,\\
\mathcal B_{ij}[\psi]&=\psi_\rho g_{ij}
 +2\psi_\tau(g_{ik}p^{k\ell}g_{\ell j}-\rho g_{ij}/3).
\end{aligned}
\]

Here \(L^{ij}\) is the *explicit* derivative of \(\psi\) with respect to
\(g_{ij}\), holding \(\rho,\tau,R\), auxiliary fields and gradient covectors
fixed. For \(H\), it is \(L_H^{ij}=Bz^iz^j\). Thus the actual canonical
metric equations at fixed auxiliaries are

\[
v_{ij}:=\{g_{ij},H\}=\mathcal B_{ij}[h],\qquad
\{\bar\pi^{ij},H\}=-V e^{ij},\qquad
e^{ij}:=\mathcal E^{ij}[h,L_H].
\]

The \(\mathcal U,\mathcal W\) terms include the volume dependence of the
normalized momenta, and the last two curvature terms are the full adjoint of
the scalar-curvature variation. Neither the metric nor its determinant is
held fixed in these canonical brackets.

For an explicit evaluation of the auxiliary derivatives, let

\[
a_A=(4-3u,-3\xi),\quad g_A=(u,\xi),\quad
w_A=(u-1,\xi),\quad c_A^{\rm pot}=(3u-2,3\xi),
\quad d_A=(3u-4,3\xi).
\]

These are derivatives of the relevant exponents, not new coefficients in
the action. With \(F_A=(A_R,B_R)\),

\[
\begin{aligned}
J_A&=\frac{\rho^2e^{-6w}}{m^2a_0^2}(F_A-6Fw_A),\\
\chi_A&=-\frac m2Gg_A
-\frac{\rho^2e^{(6-5u)\xi}}{2ma_0^2}
 [F_A+F(6-5u,-5\xi)_A],\\
(h_{\mathrm{ng}})_A&=\frac{2E}{m}
 \left[a_A\left(\frac\tau J-\frac{\rho^2}6\right)
 -\frac{\tau J_A}{J^2}\right]
 +m e^{(3u-2)\xi}(c_A^{\rm pot}C+C_A)
 -\frac\kappa2e^{(3u-4)\xi}d_A+\chi_A R,\\
C_A&=(0,-2a_0^2u\log^2(1-u^2)),\qquad B_A=Bg_A.
\end{aligned}
\]

Higher derivatives in the formulas below mean ordinary partial derivatives
of these displayed functions, with \((\rho,\tau,R)\) held independent.

## 2. Expanded IC6 drift and the actual secondary–secondary bracket

Use the coordinate-density secondary constraints

\[
S_A=\frac{\delta H}{\delta q_A}
=V[(h_{\mathrm{ng}})_A-B_AZ]+2c_A\partial_i(VBz^i),\qquad c_A=(1,b).
\]

Their sign differs from a convention using \(\delta(-H)/\delta q_A\);
the following matrix and multiplier signs consistently use \(S=\delta H/\delta q\).
Because \(H\) contains no \(p_A\), the auxiliary fields and their covariant
gradient components are fixed along its unmultiplied canonical flow. Define

\[
\begin{aligned}
\theta&=\tfrac12g^{ij}v_{ij},& \dot V&=V\theta,\\
\dot\rho&=p^{ij}v_{ij}-g_{ij}e^{ij}-\rho\theta,\\
\dot\tau&=(2p^{ik}g_{k\ell}p^{\ell j}-2\rho p^{ij}/3)v_{ij}
 -2(g_{ik}p^{k\ell}g_{\ell j}-\rho g_{ij}/3)e^{ij}
 -2\tau\theta,\\
\dot R&=-R^{ij}v_{ij}+D^iD^jv_{ij}-\Delta(g^{ij}v_{ij}).
\end{aligned}
\]

Raising \(v^{ij}=g^{ik}g^{j\ell}v_{k\ell}\), direct differentiation of
the actual secondary gives the coordinate-density drift

\[
\boxed{\begin{aligned}
D_A:=\{S_A,H\}
={}&V\left\{\theta[(h_{\mathrm{ng}})_A-B_AZ]
 +(h_{\mathrm{ng}})_{A\rho}\dot\rho+(h_{\mathrm{ng}})_{A\tau}\dot\tau
 +\chi_A\dot R+B_Av^{ij}z_i z_j\right\}\\
&+2c_A\partial_i\left[VB(\theta z^i-v^{ij}z_j)\right].
\end{aligned}}
\]

No metric equation was suppressed in obtaining this expression. In
particular, the \(\dot R\) term differentiates a metric velocity that itself
depends on curvature, so this expression does not assert a low derivative
order or a regularity theorem for the coupled evolution.

For smearing functions \(f_A\), write

\[
S[f]=\int d^3x\,V\psi_f,\qquad
\psi_f=f_A[(h_{\mathrm{ng}})_A-B_AZ]-2Bc_A(D_i f_A)z^i.
\]

Its explicit fixed-invariant metric derivative is

\[
L_f^{ij}=f_AB_Az^iz^j+2Bc_A(D^{(i}f_A)z^{j)}.
\]

Thus all canonical dependence of the two required brackets is specified by

\[
\boxed{\begin{aligned}
D[f]&=\int d^3x\,V\{
 \mathcal E^{ij}[\psi_f,L_f]\mathcal B_{ij}[h]
 -\mathcal B_{ij}[\psi_f]\mathcal E^{ij}[h,L_H]\},\\
\Omega[f,g]&=\int d^3x\,V\{
 \mathcal E^{ij}[\psi_f,L_f]\mathcal B_{ij}[\psi_g]
 -\mathcal B_{ij}[\psi_f]\mathcal E^{ij}[\psi_g,L_g]\}.
\end{aligned}}
\]

Equivalently, replacing \(v,e\) in the boxed pointwise drift by
\(\mathcal B[\psi_f],\mathcal E[\psi_f,L_f]\) gives
\(\{S_A,S[f]\}\). Auxiliaries contribute no extra canonical term to
\(\Omega\), since \(S_A\) is independent of \(p_A\). A specified ordinary
matter Hamiltonian would contribute additional terms to every relevant
variation; none is assumed here.

These are analytic continuum identities. The new numerical program checks
their homogeneous restriction with independent derivative controls; it does
not test their spatial terms by assigning them a finite matrix.

## 3. Independent exact reduction and computed finite Poisson matrix

For a unit coordinate cell in Bianchi I, \(Dq=R=0\). This is an exact
restriction of the Hamiltonian; all off-diagonal directions in its symmetric
metric and momenta remain present. Let

\[
P=\operatorname{tr}(g\bar\pi),\quad
A=\operatorname{tr}(g\bar\pi g\bar\pi)-P^2/3,
\quad H_{\rm BI}=Vh_{\mathrm{ng}}(P/V,A/V^2,0,q).
\]

The canonical coordinate order is

\[
(g_{11},g_{22},g_{33},g_{12},g_{13},g_{23};
 \bar\pi^{11},\bar\pi^{22},\bar\pi^{33},
 2\bar\pi^{12},2\bar\pi^{13},2\bar\pi^{23};\xi,u;p_\xi,p_u).
\]

The factors of two follow from the actual symplectic contraction
\(\bar\pi^{ij}dg_{ij}\). Exact symbolic differentiation of the generic
six-component metric and momentum polynomials verifies

\[
\{\det g,P\}=3\det g,\qquad
\{\det g,A\}=0,\qquad\{P,A\}=0.
\]

Consequently \(\{V,P\}=3V/2\), and for invariant functions the independent
bracket reduction gives

\[
D_A=\frac{3V}{2}(H_{AV}H_P-H_{AP}H_V),\qquad
\Omega_{AB}=\frac{3V}{2}(H_{AV}H_{BP}-H_{AP}H_{BV}),\qquad
K_{AB}=H_{AB}.
\]

Here \(A,B\) as *subscripts* label auxiliary components, whereas the scalar
\(A\) in \(H(V,P,A,q)\) is the shear invariant. On \(S_A=V(h_{\mathrm{ng}})_A=0\),
one especially useful specialization is

\[
\Omega_{AB}=3V\tau\left[(h_{\mathrm{ng}})_{A\rho}(h_{\mathrm{ng}})_{B\tau}
 -(h_{\mathrm{ng}})_{A\tau}(h_{\mathrm{ng}})_{B\rho}\right].
\]

This explains why isotropic constrained data suppress this bracket without
making it identically zero on the shearing constraint surface.

The main computation does not use that reduction to insert a desired matrix.
It differentiates \(H\) in all fourteen nontrivial variables, constructs the
four constraint gradients in the full sixteen-dimensional canonical space,
and computes \(\mathbb O=(\partial\Phi)J_{16}(\partial\Phi)^T\), where
\(\Phi=(p_\xi,p_u,S_\xi,S_u)\). It then compares against the independently
reduced formulas. The actual matrix has the block form

\[
\mathbb O=\begin{pmatrix}0&-K\\K&\Omega\end{pmatrix},\qquad
\lambda=-K^{-1}D,\qquad \dot S=D+K\lambda.
\]

The initial metric is

\[
g=\begin{pmatrix}1.03&.012&-.008\\.012&.98&.009\\-.008&.009&1.01\end{pmatrix}.
\]

With \(m=h_0=1\), the initial normalized trace is
\(-3e^{-1/2}(1.007)\). A traceless symmetric orthonormal-frame shear is

\[
\Sigma=\begin{pmatrix}.04&.012&-.009\\.012&-.025&.007\\-.009&.007&-.015\end{pmatrix},
\qquad
\bar\pi=Vg^{-1/2}(\rho I/3+\Sigma)g^{-1/2}.
\]

All action constants retain the original witness values. A bounded Newton
solve initializes only \((\xi,u)\), yielding approximately
\((.24275274634454308,.6635898184777362)\); its maximum residual is
\(1.80\times10^{-14}\). This is the only auxiliary projection in the run.
The actual shearing-state values are

\[
K\simeq\begin{pmatrix}-14.9712400052&16.3722704813\\
16.3722704813&-29.7446446103\end{pmatrix},\qquad
\Omega\simeq\begin{pmatrix}0&.06402066864\\-.06402066864&0\end{pmatrix},
\]

\[
D\simeq(.24704222301,-.12154392780),\qquad
\lambda\simeq(.03022759343,.01255185304).
\]

The matrix singular values are approximately
\((40.31947,40.31947,4.396461,4.396461)\). Both its numerical rank and the
constraint-Jacobian rank are four at tolerance \(10^{-9}\). Thus all four
constraints in this finite reduction are second class; its constrained
phase-space dimension is \(16-4=12\), or six configuration variables.
If the matrix were rank deficient, the program would leave that count
unassigned: matrix nullity alone would not settle further consistency.
The absent spatial constraint sector cannot be restored by subtracting a
field-theory gauge count from this homogeneous fixture.

Deleting the canonical metric contribution to \(D\) gives a tangency defect
\(7.5392\), and setting the multipliers to zero gives a defect \(0.2470\).
The actual multipliers leave a defect below \(5\times10^{-17}\) initially.
The explicit block inverse is checked on both sides against this actual
matrix, with residual below \(7\times10^{-16}\).

## 4. Unprojected finite evolution and controls

The program integrates

\[
\dot g=H_{p_g},\quad\dot p_g=-H_g,\quad
\dot q=\lambda(g,p_g,q),\quad\dot p_A=-S_A
\]

to coordinate time \(0.08\). As in Dirac preservation, multipliers are
treated as prescribed values at each integration stage; they are not
differentiated inside the Hamiltonian bracket. No \(S_A=0\) solve or resetting
of \(p_A\) is performed after initialization. A fourth-order Runge–Kutta
stepper gives these maximum errors on completed time steps:

| Steps | Secondary residual | Primary residual | Energy error |
|---:|---:|---:|---:|
| 16 | \(5.99\times10^{-11}\) | \(2.71\times10^{-11}\) | \(3.15\times10^{-11}\) |
| 32 | \(3.76\times10^{-12}\) | \(1.69\times10^{-12}\) | \(1.98\times10^{-12}\) |
| 64 | \(2.37\times10^{-13}\) | \(1.05\times10^{-13}\) | \(1.24\times10^{-13}\) |

Internal predictor stages are not completed fourth-order steps. Their maximum
secondary residuals are separately reported as \(3.19\times10^{-5}\),
\(8.00\times10^{-6}\), and \(2.00\times10^{-6}\). The code reports their
energy and primary errors too. The algebraic tangency residual stays below
\(1.1\times10^{-16}\) even at these off-surface predictor states.

Across every stage in these runs, the actual Poisson rank is four, the
smallest singular value exceeds \(4.3964\), the metric's smallest eigenvalue
exceeds \(0.9741\), \(J_T\ge .98610\), and
\(|r^2-1|\le .010501<1/4\). Nonzero shear persists. The metric/momentum state
moves by Euclidean norm \(0.31639\), and the auxiliary fields move by norm
\(0.0021940\). These are measurements along an evolving nonlinear trajectory,
not repeated static constraint solves.

The first- and second-derivative engine is forward automatic differentiation
of the full barred Hamiltonian. Its independent controls reconstruct the
physical metric and physical momentum and evaluate the covariant phase
Hamiltonian. At the non-diagonal test point, complex-step first derivatives
of that independent expression agree in all fourteen directions within
\(2.7\times10^{-15}\); centered differences of those first derivatives agree
with the full Hessian within \(2.2\times10^{-9}\), using step \(2\times10^{-6}\).
The wrong off-diagonal canonical normalization changes the Hamiltonian by
\(0.01254\), so it cannot pass this control. The separately derived exact
isotropic witness velocities and auxiliary mass matrix also pass. This
derivative comparison is numerical, not interval certification.

## 5. Reproduction, provenance and remaining gap

The new implementation and tests are
[ic6_dirac_flow.py](ic6_dirac_flow.py) and
[test_ic6_dirac_flow.py](test_ic6_dirac_flow.py). Only these two files and this
note belong to this addition; existing dirty workspace files were preserved.
The program pins the five authoritative input documents, checks them before
and after each full run, records its implementation hash, actual software
versions and cooperative numerical-thread environment, and emits JSON-safe
results. The parent task's bounded run manifest can capture that stdout
without modifying an old scientific result.

The initial six-test run failed because the implementation was absent.
Additional exact-invariant and accepted-step controls were then added before
their implementation. Final verification uses seven tests. An early test
incorrectly applied fourth-order completed-step accuracy to internal RK
predictor stages; the correction separates both measured errors explicitly.
The initial NumPy determinant path emitted spurious tiny-complex-perturbation
warnings on this LAPACK build, so the independent covariant path uses a
cross-product determinant. It then runs without warnings.

From the repository root, apply the following cooperative thread prefix to
each command (it does not enforce CPU affinity):

```text
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
```

```text
python3 -B qwen_claude_field_theory/closure_2026/integrable_clock_construction_2026/test_ic6_dirac_flow.py
python3 -B qwen_claude_field_theory/closure_2026/integrable_clock_construction_2026/ic6_dirac_flow.py
python3 -B qwen_claude_field_theory/closure_2026/integrable_clock_construction_2026/ic6_dirac_flow.py --require-field-closure
```

The required-field-closure command deliberately exits 2 after the finite
checks pass. Normal completion exits 0; a failed finite check exits 1.
The tested environment is Python 3.9.6, NumPy 1.26.2 and SymPy 1.14.0. Runs
take less than two seconds on this host and stay within the requested
180-second bound. Hard wall-time enforcement belongs to the external runner;
the script's own guards bound integration to at most 256 steps and \(t\le .1\).
There is no random input or numerical parallel worker.

**Result interpretation:** the finite assertion and its independent controls
are verified subject to float64 tolerances. Exact polynomial Poisson identities
are also checked. The source hashes prevent action-version drift. The
structural result is the shear-dependent bracket and the metric contribution
to the true preservation source. Numerical ranks on this trajectory do not
prove any continuum operator inverse or global persistence theorem.

The companion [IC6_STRONG_AUXILIARY.md](IC6_STRONG_AUXILIARY.md) supplies a
local spatial auxiliary solve, regularity and a common smooth domain under its
stated hypotheses. This finite numerical reduction does not supply that
continuum result. The remaining evolution implication is a coupled
finite-Sobolev existence and persistence theorem keeping the data in that
regular branch. The curvature and gradient sectors must enter that argument;
they vanish identically in the present numerical reduction. A physical reduced
characteristic analysis and specified matter equations remain separate
obligations. No finite matrix here is presented as an inhomogeneous closure
certificate.
