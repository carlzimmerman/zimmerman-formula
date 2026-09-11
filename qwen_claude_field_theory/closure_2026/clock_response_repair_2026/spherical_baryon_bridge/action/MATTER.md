# Explicit baryonic dust action and nonzero radial evolution

Base `776cc413d13ced7996fc06d544b68cacbebc5615`, 2026-09-10. This adds a
specified matter model to the spherical action in `REPORT.md`. It is a local,
single-stream irrotational dust description before caustics. Radial velocity
dispersion, pressure, vorticity, and multistreaming need additional matter
physics; they are not implicitly supplied by this action.

**Audit verdict: computationally verified only in the stated range.** All
identities concern exact smooth spherical fields with \(N,A,R>0\), future
clock orientation, and nonnegative rest density. The moving benchmark is
tested on \(t>r>0\), a shell patch. It does not solve the Einstein equations.

Take the explicitly minimally coupled action

\[
S_d=-\frac12\int d^4x\sqrt{-g}\,\rho
 [g^{\mu\nu}\partial_\mu\theta\partial_\nu\theta+1]
 =4\pi\int dt\,dr\,L_d,
\]
\[
L_d=\frac12NAR^2\rho(U^2-Z^2-1),\qquad
U=(\dot\theta-vq)/N,\quad q=\theta',\quad Z=q/A.
\]

The multiplier \(\rho\) is the proper rest density on solutions. Choose
\(u_\mu=-\partial_\mu\theta\), so \(u^t=U/N>0\) selects the future
branch. Its other nonzero component is
\(u^r=-vU/N-q/A^2\). This dust potential is independent of both gravity
scalars \(\chi,\tau\).

## Variations and source normalization

Using the same per-solid-angle Euler derivative as `REPORT.md`, all source
terms follow before imposing normalization:

\[
\begin{aligned}
E_N^d&=-\tfrac12 AR^2\rho(U^2+Z^2+1),&
E_v^d&=-AR^2\rho Uq,\\
E_A^d&=\tfrac12 NR^2\rho(U^2+Z^2-1),&
E_R^d&=NAR\rho(U^2-Z^2-1),\\
E_\rho^d&=\tfrac12NAR^2(U^2-Z^2-1),&
E_\theta^d&=-\dot p_d-j_d'.
\end{aligned}
\]
\[
p_d=AR^2\rho U,\qquad
j_d=-vp_d-NR^2\rho q/A=p_dc_d,\qquad
c_d=-v-\frac{Nq}{A^2U}=u^r/u^t.
\]

The multiplier equation enforces \(U^2=1+Z^2\), hence \(u^\mu u_\mu=-1\).
The potential equation is exactly \(\nabla_\mu(\rho u^\mu)=0\). Since the
unit velocity is a gradient, normalization also implies
\(u^\mu\nabla_\mu u_\nu=\tfrac12\nabla_\nu(u^2)=0\); dust follows
geodesics. The stress tensor before imposing normalization contains the
term \(\mathcal L_d g_{\mu\nu}\), where
\(\mathcal L_d=\rho(U^2-Z^2-1)/2\). On shell it becomes
\(T_{\mu\nu}=\rho u_\mu u_\nu\). In particular,

\[
\epsilon_d=T_{\mu\nu}n^\mu n^\nu=\rho U^2,\qquad
J_r=-\rho Uq,\qquad S^r{}_r=\rho Z^2,\qquad S^\theta{}_\theta=0,
\]
\[
E_N^d=-AR^2\epsilon_d,\qquad E_v^d=AR^2J_r=-qp_d,\qquad
E_A^d=NR^2\rho Z^2,\qquad E_R^d=0.
\]

These terms enter the equations as \(\mathcal E_f+E_f^d=0\).
The momentum convention is \(J_r=-T_{r\mu}n^\mu\), with
\(n^\mu=(1/N,-v/N,0,0)\).
Rest density and the lapse source coincide only when \(q=0\).
The script independently contracts the stress tensor with each metric
variation and compares these signs and factors with action differentiation.

## Conservative evolution for the nonlinear solver

The positive branch can be reduced canonically with

\[
U=\sqrt{1+q^2/A^2},\quad
\rho=\frac{p_d}{AR^2U},\quad
\mathcal H_d=p_d(vq+NU),\quad L_{d,\mathrm{can}}=p_d\dot\theta-\mathcal H_d.
\]

This comes from the momentum definition and multiplier constraint; directly
substituting \(U^2-Z^2=1\) into the original Lagrangian would incorrectly
erase its equations. The canonical metric variations reproduce every
on-shell source above. An evolution system retaining radial motion is

\[
\boxed{\dot\theta=vq+NU,\qquad
\dot p_d+\partial_r(p_dc_d)=0,\qquad q=\theta'.}
\]

Equivalently evolve \(q\) alongside \(p_d\), preserving its initial gradient
origin:

\[
\dot q=\partial_r(vq+NU),\qquad
\dot q+c_dq'=qv'+UN'-\frac{Nq^2A'}{A^3U}.
\]

The normal-frame physical velocity is \(w=-Z/U\), so \(|w|<1\).
The conserved rest mass in a fixed coordinate interval is
\(M_d=4\pi\int p_d\,dr\); its change is the boundary flux
\(-4\pi[j_d]_{r_1}^{r_2}\). In a regular central patch \(q=O(r)\),
\(R=O(r)\), and finite \(\rho,A,U\) give \(p_d=O(r^2)\) and vanishing
central flux. Exterior boundary data still have to be specified.

Initially setting \(q=0\) is allowed. Preserving \(q=0\) at rest in a
zero-shift chart would require \(N'=0\), because the actual equation gives
\(\dot q=N'\) at that instant. Thus a static, prescribed finite-mass dust
profile cannot be treated as exact equilibrium in an inhomogeneous lapse.
This is why the solver must evolve its matter state. In a static zero-shift
metric the initial physical acceleration is \(\dot w/N=-N'/(NA)\).

## Benchmarks and deliberately wrong controls

On an FLRW background \(N=n(t), A=a(t),R=a(t)r,v=0,q=0,U=1\),
\(p_d=a^3r^2\rho\). Its continuity equation gives
\(\dot\rho+3\dot a\rho/a=0\), or \(\dot\rho/n+3H\rho=0\).
An independent stress divergence calculation gives the same equation:
\(n^2\nabla_\mu T^{\mu t}=\dot\rho+3\dot a\rho/a\).
These are matter equations on the stated background, not a claim that
arbitrary inhomogeneous dust is compatible with an exactly FLRW metric.

An exact moving dust check in prescribed Minkowski geometry uses
\(\theta=\sqrt{t^2-r^2}\),
\(\rho=C(t^2-r^2)^{-3/2}\), \(C>0\), \(t>r>0\).
It has \(c_d=r/t\). The script independently checks normalization, mass
continuity, and both energy and radial momentum conservation. The profile
is not a finite-mass regular Einstein solution; it tests moving matter signs.

Three negative controls are rejected with explicit nonzero residuals:
frozen radial momentum in \(N'\ne0\), using rest density as the normal
energy density for \(Z\ne0\), and holding rest density constant in an
expanding FLRW background. No negative control is presented as a physical
solution. Remaining tasks are to solve these matter equations together with
the full gravitational equations and to specify admissible initial and
boundary data; solving the dust subsystem alone does not establish that.

Run `python3 qwen_claude_field_theory/closure_2026/clock_response_repair_2026/spherical_baryon_bridge/action/matter.py`
from the repository root. It prints JSON for the parent runner and uses exact
SymPy arithmetic, without floating tolerances or parameter fitting. Mathbox
computation-audit, proof-audit, and proofread-math guide this derivation and
self-review. No full gravitational degree-of-freedom or PPN claim is made.
