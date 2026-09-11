# Exact spherical action and conserved scalar current

Base `776cc413d13ced7996fc06d544b68cacbebc5615`, 2026-09-10.
The working tree had unrelated existing changes; this subtask owns only
`spherical_baryon_bridge/action/`. No fit, parameter choice, physical mode
count, or phenomenological success is asserted.

**Audit verdict: computationally verified only in the stated range.** The
range is exact formal spherical jets through differential order three,
arbitrary constitutive derivatives, and nonzero lapse and spatial metric
factors. These are symbolic identities, not a sampling of halo profiles.
The reduction and current argument below explain their mathematical scope.
An additional independent audit checked cancellation of every third-order jet
from all five Euler equations; the executable now checks this too. Second-order
spherical equations do not by themselves prove a full constraint count or health.

## Action and conventions

Use signature \((-+++)\), \(K_{ij}=\tfrac12\mathcal L_n h_{ij}\), constant
\(M^2,\Lambda,\gamma\), and the stated covariant action

\[
S=\int\sqrt{-g}\,[\tfrac{M^2}{2}(\mathcal R-2\Lambda)
 +P(X,\tau)+\sqrt{X_\tau}W(Y,\tau)-V(\tau)
 +\gamma X\Box\chi]+S_m[g].
\]

Here \(X=-\nabla\chi\cdot\nabla\chi\),
\(X_\tau=-\nabla\tau\cdot\nabla\tau>0\), and \(Y\) is the squared
spatial gradient of \(\chi\) projected orthogonally to the clock normal.
Take an oriented clock patch \(\tau=t\), \(N,A,R>0\), with

\[
ds^2=-N^2dt^2+A^2(dr+vdt)^2+R^2d\Omega^2,
\quad u=\chi',\quad Q=(\dot\chi-vu)/N,\quad Y=u^2/A^2,\quad X=Q^2-Y,
\]
\[
k=K_r=(\dot A/A-vA'/A-v')/N,\qquad
h=K_\Omega=(\dot R/R-vR'/R)/N,\qquad K=k+2h,
\]
\[
D=D^2\chi=\frac{u'+(2R'/R-A'/A)u}{A^2},\qquad
Y'=2uu'/A^2-2A'u^2/A^3.
\]

All five functions \(N,v,A,R,\chi\) are independently varied. In particular,
\(R=r\), \(v=0\), \(A=1\), and \(N=1\) are not imposed in deriving
equations. Boundary terms are removable for compactly supported variations
or an appropriate boundary action. The origin \(R=0\) requires regular
limits and is not an invertible coordinate patch of this formula.

After integrating the angles, \(S=4\pi\int dt\,dr\,L+S_m\), where

\[
\boxed{L=M^2\left(NA+\frac{NR'^2}{A}+\frac{2N'RR'}A\right)
       +NAR^2\mathcal H+AR^2W,}
\]
\[
\mathcal H=-M^2(2kh+h^2+\Lambda)+P-V+\gamma B,
\quad B=-\tfrac23Q^3(k+2h)+2QkY+2Q^2D+\frac{uY'}{A^2}.
\]

The unintegrated spatial curvature is
\({}^{(3)}\mathcal R=2R^{-2}[1-R'^2/A^2-2RR''/A^2+2RR'A'/A^3]\).
The \(W\) term loses its lapse prefactor because \(\sqrt{X_\tau}=1/N\).
It still affects spatial metric equations and the scalar flux.

For additional independent checks, the script computes two-dimensional
Christoffel symbols and \(\mathcal R_2\), then uses
\(\mathcal R_4=\mathcal R_2+2/R^2-4\Box_2R/R-2(\nabla_2R)^2/R^2\).
The covariant Einstein density minus the displayed Einstein density is
\(\partial_t E_t+\partial_r E_r\), with

\[
E_t=M^2AR^2K,\qquad
E_r=-vE_t-M^2R^2N'/A-2M^2NRR'/A.
\]

The corresponding cubic boundary flux is

\[
B_t=\gamma AR^2(-Q^3/3+QY),\qquad
B_r=-vB_t-\gamma NR^2(Q^2+Y)u/A,
\]

so \(\gamma NAR^2X\Box\chi-\gamma NAR^2B
=\partial_tB_t+\partial_rB_r\). Both boundary identities are checked exactly.

## All independent spherical equations

Let \(\mathcal E_f=\partial L/\partial f-\partial_t(L_{\dot f})
-\partial_r(L_{f'})+\partial_r^2(L_{f''})\), with the last term needed
only for \(\chi\). Equations with matter are
\(\mathcal E_f+(4\pi)^{-1}\delta S_m/\delta f=0\).
The following are explicit compact forms, independently compared with direct
jet differentiation of \(L\):

\[
H_k=-2M^2h+\gamma(-2Q^3/3+2QY),\quad
H_h=-2M^2(k+h)-4\gamma Q^3/3,
\]
\[
H_Q=2QP_X+\gamma[-2Q^2(k+2h)+2kY+4QD],\qquad
\Pi_A=R^2H_k,\quad\Pi_R=ARH_h,\quad p=AR^2H_Q.
\]

Subscripts on \(\mathcal H\) below mean explicit derivatives holding
\(k,h,Q,u,u',A',R'\) fixed except for the indicated variable. Thus

\[
H_A=\frac{2YP_X}A+\gamma\left[-\frac{4QkY}A-\frac{4Q^2D}A
 +\frac{2Q^2A'u}{A^4}-\frac{8u^2u'}{A^5}+\frac{10A'u^3}{A^6}\right],
\]
\[
H_{A'}=-2\gamma u(Q^2+Y)/A^3,\quad
H_R=-4\gamma Q^2R'u/(A^2R^2),\quad H_{R'}=4\gamma Q^2u/(A^2R).
\]

With all coefficients evaluated at the physical fields,

\[
\boxed{\mathcal E_N=M^2[A+R'^2/A-(2RR'/A)']
 +AR^2[\mathcal H-kH_k-hH_h-QH_Q],}
\]
\[
\boxed{\mathcal E_v=A\Pi_A'-R'\Pi_R-u p,}
\]
\[
\begin{aligned}
\mathcal E_A={}&M^2(N-NR'^2/A^2-2N'RR'/A^2)+NR^2\mathcal H
 +NAR^2H_A-(Nk+v')\Pi_A+R^2(W-2YW_Y)\\
 &-\dot\Pi_A-\partial_r[-v\Pi_A+NAR^2H_{A'}],\\
\mathcal E_R={}&2M^2N'R'/A+2NAR\mathcal H+NAR^2H_R-Nh\Pi_R+2ARW\\
 &-\dot\Pi_R-\partial_r[2M^2(NR'+N'R)/A-v\Pi_R+NAR^2H_{R'}].
\end{aligned}
\]

In particular the scalar contribution to the lapse equation is
\(-AR^2\rho_{\rm clock}\), where

\[
\boxed{\rho_{\rm clock}=2Q^2P_X-P+V
 -\gamma[2Q^3K-2QkY-2Q^2D+uY'/A^2].}
\]

The minimally coupled matter lapse derivative is \(-AR^2\rho_m\), where
\(\rho_m=T_{\mu\nu}n^\mu n^\nu\). Replacing \(P(X,t)\) by a frozen
spatial function would discard part of this source.

## Full scalar conservation and omitted clock equation

The action has exact \(\chi\)-shift symmetry even when \(P,W,V\) depend
explicitly on \(t=\tau\). Its equation, including the time current, is

\[
\mathcal E_\chi=-(\dot p+j')=0,
\]
\[
\boxed{j=-vp+\frac{2NR^2}A\left\{u[-P_X+W_Y/N]
 +\gamma[2Qku-2QQ'-\tfrac{N'}N(Q^2+Y)-2\tfrac{R'}RY]\right\}.}
\]

The direct covariant current is
\(J^\mu=-2(P_X+\gamma\Box\chi)\nabla^\mu\chi
-\gamma\nabla^\mu X+2\sqrt{X_\tau}W_Yh^{\mu\nu}\nabla_\nu\chi\).
If \(p_c=NAR^2J^t\), \(j_c=NAR^2J^r\), and
\(F=2\gamma R^2Qu/A\), then

\[
p=p_c+F',\qquad j=j_c-\dot F.
\]

The boundary improvement changes the local charge density but not the
conservation equation. The script derives \(\Box\chi\) directly from
the metric divergence and verifies both improvement identities. At a regular
center, integrating the actual equation gives
\(j(t,r)=-\partial_t\int_0^r p(t,s)\,ds\) when the center flux vanishes.
Zero radial scalar flux therefore needs a time-independent enclosed charge;
it does not follow merely from regularity.

Clock gauge does not supply permission to drop the \(\tau\) equation.
Define \(\mathfrak E^{\mu\nu}=2(\sqrt{-g})^{-1}\delta S/\delta g_{\mu\nu}\)
and \(E_a=(\sqrt{-g})^{-1}\delta S/\delta a\). Diffeomorphism invariance,
after imposing matter equations, gives

\[
\nabla_\mu\mathfrak E^\mu{}_{\nu}
 =E_\chi\partial_\nu\chi+E_\tau\partial_\nu\tau.
\]

Since \(\partial_t\tau=1\), all metric equations and \(E_\chi=0\)
imply \(E_\tau=0\). This argument needs the original covariant action,
an invertible timelike clock patch, and all four spherical metric variations.
It is not a physical degree-of-freedom count or a boundary existence theorem.

## Benchmarks, dependency audit, and reproducibility

For \(N=n(t),A=a(t),R=a(t)r,v=0,\chi=f(t)\), substituted **after**
variation, let \(H=\dot a/(na)\), \(Q=\dot f/n\). The exact identities give

\[
\rho_\chi=2Q^2P_X-P+V-6\gamma HQ^3,\qquad
p_\chi=P-V+W/n+2\gamma Q^2\dot Q/n,
\]
\[
\mathcal E_N=a^3r^2[3M^2H^2-M^2\Lambda-\rho_\chi],\qquad
\mathcal E_v=0,
\]
\[
\frac{\mathcal E_A}{na^2r^2}
=\frac{\mathcal E_R}{2na^2r}
=M^2(2\dot H/n+3H^2-\Lambda)+p_\chi,
\]
\[
j=0,\qquad p=a^3r^2(2QP_X-6\gamma HQ^2),\qquad \dot p=0.
\]

The FLRW current can be nonzero; its conservation is not its vanishing.
These formulas are equations to solve, not evidence the previously chosen
background remains a solution after adding \(\gamma\).

Minkowski substitution \(N=A=1,R=r,v=0,\chi=qt\) gives
\(p=2qr^2P_X\), \(j=0\), \(\mathcal E_\chi=-2qr^2P_{X\tau}\),
\(\mathcal E_N=r^2(P-V-2q^2P_X-M^2\Lambda)\),
\(\mathcal E_A=r^2(P-V+W-M^2\Lambda)\), and
\(\mathcal E_R=2r(P-V+W-M^2\Lambda)\). Minkowski is an off-shell
benchmark unless these sources vanish or balance matter. Gamma-zero checks
compare every Euler derivative to a separately constructed first-derivative
\(P/W\) action, retaining both time and radial scalar gradients.

Dependency chain: stated covariant action and sign conventions → direct
spherical geometric identities and boundary reduction → unrestricted local
Euler derivatives → current conservation and conditional benchmark limits.
All these algebraic obligations passed. The Ward argument is an internal
variational identity; boundary regularity is an explicitly stated condition.
Solutions, admissible cosmological matching, characteristic cones, complete
Dirac analysis, lensing, MOND, and PPN are outside this derivation.

Run from repository root:

```sh
python3 qwen_claude_field_theory/closure_2026/clock_response_repair_2026/spherical_baryon_bridge/action/derive.py
```

The command prints JSON; Python 3.9.6 and SymPy 1.14.0 were used. Arithmetic
is exact, with no seed, floating tolerance, finite profile bounds, or fit.
Constitutive jets obey the full chain rule for arbitrary smooth \(P,W,V\);
they are not polynomial ansatzes. Aggregate run provenance and input/output
hashes are maintained by the parent task's runner. A first audit caught an
incorrect sign in a manually transcribed \(H_A\); the direct Euler operator
detected it and the corrected formula above passed re-execution.

Mathbox computation-audit and proof-audit guided the identity checks and
scope labels. Proofread-math self-review covered this report's equations and
definitions; no unresolved notation issue or later mathematical-token
correction remained. Agreement of symbolic expressions is evidence for
these fixed-dimensional identities, not closure of the proposed theory.
