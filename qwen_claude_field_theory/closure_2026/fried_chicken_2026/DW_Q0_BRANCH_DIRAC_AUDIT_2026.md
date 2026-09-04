# DW Localized Action: Restarted \(Q=0\) Branch Audit

Date: 2026-09-04
Repository state: `edff7fddedb24f76af60a1133e49f1110ab38dce` plus uncommitted work

## Result

The \(Q=0\) rank drop does **not** rescue the unrestricted localized action.
On both \(\lambda\neq0\) and \(\lambda=0\), the \((X,\xi)\) kinetic block remains
nondegenerate with determinant \(-1\).  On a constant-background Fourier mode,

\[
\det \mathcal O_{X\xi}(\omega,k)=-(\omega^2-k^2)^2,
\]

so the independent-auxiliary local theory still has two scalar light-cone
channels with opposite kinetic signs.  Its unrestricted \(Q=0\) reading is
therefore **DEAD** at the scalar stability/extra-mode gate.

The restarted branch analysis also reveals why a naive first-/second-class
count at \(Q=0\) is unsafe.  The stratum conditions restrict the tangent bundle
without each supplying an independent Hessian-null velocity.  Their Hamiltonian
multipliers are tied to the genuine null velocities by the undivided Legendre
map.  If \(Q=0\) or \(\lambda=0\) is substituted before variation, the transverse
Euler–Lagrange equations are lost and spurious gauge freedom appears.

The homogeneous embedded branch equations are closed below.  The full spatial
ADM constraint algebra remains **NOT COMPUTED**; no \(N_{\rm grav}=2\) claim is
made from this finite-dimensional count.

## 1. Undivided action and order of operations

The fixed-lapse homogeneous density is

\[
L=\frac{\dot X\dot\xi}{N}
+\lambda N\left(1-\frac{\dot\phi^2}{N^2}\right)
+Q\frac{\dot\phi\dot\nu}{N}-cMN,
\quad
Q=M+f(Z),
\quad
Z=-\frac{4\dot X^2}{N^2a_0^2}.
\]

Here \(c=a_0^2/\kappa\).

The script uses an arbitrary symbolic two-jet
\(f(Z)=f_0+f_1Z+f_2Z^2/2\).  This is sufficient for the exact Hessian because
only \(f'\) and \(f''\) can occur.  It first calculates

\[
\begin{aligned}
p_X&=\frac{\dot\xi}{N}
-\frac{8f'(Z)\dot X\dot\phi\dot\nu}{N^3a_0^2},\\
p_\xi&=\frac{\dot X}{N},\\
p_\phi&=-\frac{2\lambda\dot\phi}{N}+\frac{Q\dot\nu}{N},\\
p_\nu&=\frac{Q\dot\phi}{N},
\end{aligned}
\]

and only then evaluates \(Q=0\).  Exact maximal minors give

\[
\operatorname{rank}H\big|_{Q=0,\lambda\neq0}=3,
\qquad
\det H_{3\times3}=\frac{2\lambda}{N^3},
\]

and

\[
\operatorname{rank}H\big|_{Q=0,\lambda=0}=2,
\qquad
\det H_{2\times2}=-\frac1{N^2}.
\]

With \(F_1=f'(Z)\), exact null vectors in velocity order
\((\dot X,\dot\xi,\dot\phi,\dot\nu)\) are

\[
n_{\lambda\neq0}=
\left(0,\frac{8F_1\dot X\dot\phi}{N^2a_0^2},0,1\right),
\]

and

\[
n_{\lambda=0}^{(\phi)}=
\left(0,\frac{8F_1\dot X\dot\nu}{N^2a_0^2},1,0\right),
\qquad
n_{\lambda=0}^{(\nu)}=
\left(0,\frac{8F_1\dot X\dot\phi}{N^2a_0^2},0,1\right).
\]

The script multiplies the evaluated Hessians by these vectors and obtains zero.
As a mutation control, substituting \(Q=0\) in the action before differentiation
instead produces a pure-\(\nu\) null direction and erases the multiplier tie.

## 2. Embedded branch with \(Q=0,\lambda\neq0\)

Let

\[
Z_p=-\frac{4p_\xi^2}{a_0^2},
\qquad \mathcal Q=M+f(Z_p).
\]

The branch Legendre energy, derived directly from \(p\dot q-L\), admits the
extension

\[
H_c=N\left(p_Xp_\xi-\frac{p_\phi^2}{4\lambda}-\lambda+cM\right).
\]

The branch image and preservation chain contain

\[
p_\lambda=0,\quad p_M=0,\quad p_\nu=0,\quad \mathcal Q=0,
\]

followed by the clock secondary

\[
D=p_\phi^2-4\lambda^2=0.
\]

In the order \((p_\lambda,p_M,p_\nu,\mathcal Q,D)\), the calculated Poisson
matrix is

\[
\begin{pmatrix}
0&0&0&0&8\lambda\\
0&0&0&-1&0\\
0&0&0&0&0\\
0&1&0&0&0\\
-8\lambda&0&0&0&0
\end{pmatrix}.
\]

Its exact rank is four, witnessed by the nonzero maximal minor
\(64\lambda^2\).  Intrinsically, four directions form second-class pairs and
one relation is Poisson-null.

That null relation is not enough to declare a gauge mode of the original
Euler–Lagrange system.  Matching Hamilton's \(\dot\xi\) to the undivided
Legendre map forces

\[
u_{\mathcal Q}=\frac{p_\phi}{2\lambda}\dot\nu.
\]

Preservation of \(p_M\) gives \(u_{\mathcal Q}=-Nc\), hence

\[
\dot\nu=-\frac{2Nc\lambda}{p_\phi}.
\]

Together with \(D=0\) and
\(\dot\phi=-Np_\phi/(2\lambda)\), this derives

\[
\dot\phi^2=N^2,
\qquad
\dot\phi\dot\nu=cN^2.
\]

Further preservation gives

\[
\dot{\mathcal Q}=v_M=0,
\qquad
\dot D=-8\lambda v_\lambda=0,
\qquad
\dot p_\nu=0.
\]

Thus the homogeneous embedded chain closes by fixing multipliers, but it is an
irregular stratum rather than a standard constant-rank Dirac system.

## 3. Embedded branch with \(Q=0,\lambda=0\)

The exact branch relations are

\[
(p_\lambda,p_M,p_\phi,p_\nu,\lambda,\mathcal Q)=0.
\]

Their calculated Poisson matrix is

\[
\begin{pmatrix}
0&0&0&0&-1&0\\
0&0&0&0&0&-1\\
0&0&0&0&0&0\\
0&0&0&0&0&0\\
1&0&0&0&0&0\\
0&1&0&0&0&0
\end{pmatrix},
\]

with exact rank four and unit maximal-minor witness.  It has two intrinsic
Poisson-null relations.

To retain the equations transverse to this stratum, the audit derives the
Hamilton–Pontryagin energy before setting \(\lambda=\mathcal Q=0\):

\[
\begin{aligned}
H_{HP}={}&N(cM+p_Xp_\xi)
+v_\phi p_\phi+v_\nu p_\nu
+v_\lambda p_\lambda+v_Mp_M\\
&+\lambda\left(\frac{v_\phi^2}{N}-N\right)
-\mathcal Q\frac{v_\phi v_\nu}{N}.
\end{aligned}
\]

Velocity stationarity gives \(p_\phi=p_\nu=0\).  The transverse
\(p_\lambda\) and \(p_M\) preservation equations give

\[
v_\phi^2=N^2,
\qquad
v_\phi v_\nu=cN^2,
\]

with exactly two sign-related solutions

\[
(v_\phi,v_\nu)=(N,Nc),\qquad(-N,-Nc).
\]

Homogeneous tangency fixes \(v_\lambda=v_M=0\).  Therefore the two PB-null
directions do not carry arbitrary multipliers in the embedded original problem.
Applying the ordinary formula
\((\dim\Gamma-2F-S)/2\) to this intrinsic matrix would manufacture a false
gauge interpretation, so the script explicitly refuses that count.

## 4. Spatial Fourier obstruction

On the original \(M\) equation,

\[
W\equiv\dot\phi\dot\nu-\nabla\phi\cdot\nabla\nu=c.
\]

At a constant-\(X\) background, expanding the original combination
\(QW-cM\) rather than an asserted effective density gives

\[
\mathcal L^{(2)}_{X\xi}
=\dot X\dot\xi-\nabla X\cdot\nabla\xi
-\frac{4cf'(0)}{a_0^2}
 \left(\dot X^2-|\nabla X|^2\right).
\]

Consequently

\[
K_{X\xi}=
\begin{pmatrix}
-8cf'(0)/a_0^2&1\\
1&0
\end{pmatrix},
\qquad
\det K_{X\xi}=-1.
\]

The exact inertia is one positive and one negative direction.  For \(k\neq0\),

\[
\det\mathcal O=-(\omega^2-k^2)^2,
\]

while the separate homogeneous sector is

\[
\det\mathcal O(\omega,0)=-\omega^4.
\]

Thus neither \(Q=0\) rank stratum removes the independent local \((X,\xi)\)
channels.  Retarded initial histories can select a smaller solution set, but
they are not constraints of this local Hamiltonian.

For a second spatial check, linearize \(\mathcal Q=0\) tangency around
\(\nabla\bar X=0\), \(\bar p_\xi=v\neq0\).  A Fourier mode gives

\[
\delta\dot{\mathcal Q}(k)
=u_M+\frac{8f'(\bar Z)v}{a_0^2}k^2\delta X.
\]

At finite \(k\), this fixes

\[
u_M=-\frac{8f'(\bar Z)v}{a_0^2}k^2\delta X,
\]

whereas \(u_M=0\) at \(k=0\).  It fixes a multiplier rather than producing a
new local constraint; the two sectors are not conflated.

## 5. Status and exact non-claims

| Object | Status | Reason |
|---|---|---|
| Unrestricted independent-auxiliary local action on \(Q=0\) | **DEAD** | The action-derived \((X,\xi)\) block has determinant \(-1\) and opposite-residue finite-\(k\) scalar poles. |
| Homogeneous embedded \(Q=0\) preservation | **EXACT BUT IRREGULAR** | Both \(\lambda\) strata close after tied multipliers are fixed; intrinsic PB nullity is not a valid gauge count for the embedded problem. |
| Full spatial plus ADM Dirac chain | **NOT COMPUTED** | Lapse, shift, spatial metric, curvature-response mixing, and distributional PBs are absent from this audit. |
| Retarded fixed-history theory | **OPEN / noncanonical** | Retarded data restrict solutions externally and are not generated by the local constraints. |

This audit does not derive a full ADM value of \(N_{\rm grav}\), PPN parameters,
FLRW perturbations, or equivalence to a causal metric-only nonlocal action.  Its
DEAD verdict applies to the unrestricted local representative because the
extra indefinite scalar block already survives in its fixed-background scalar
sector.  The result is not presented as a completed no-go theorem for every
possible causal nonlocal variational formalism.

## 6. Next unresolved equation

The next ADM calculation must evaluate the distributional operator

\[
\dot{\mathcal Q}(x)=
\left\{\mathcal Q(x),
H_{\rm ADM}+\int d^3y\,
\big[N\mathcal H_\perp+N^i\mathcal H_i+u^A C_A\big](y)
\right\}\approx0,
\]

together with
\(\{\mathcal Q(x),\mathcal H_\perp(y)\}\),
\(\{\mathcal Q(x),\mathcal H_i(y)\}\), and preservation of every new
branch relation.  The curvature coupling
\(-\xi R_{ab}u^a u^b\) must be retained when deriving the ADM momenta; it cannot
be appended after the scalar count.  This must be done separately at finite
\(k\) and \(k=0\).

For the retarded reading, the alternative unavoidable calculation is a doubled
in-in/closed-time-path variational construction whose reduced equations and
Ward identity are shown to reproduce the desired retarded metric equations.

## 7. Reproduction

Run from `qwen_claude_field_theory/closure_2026/fried_chicken_2026`:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 test_dw_q0_branch_dirac_2026.py
PYTHONDONTWRITEBYTECODE=1 python3 dw_q0_branch_dirac_2026.py
```

Observed exits: 0 and 0.  The test suite passed 6/6 cases and the executable
audit passed 29/29 internal controls.  The pre-implementation failing run is
preserved in `dw_q0_branch_tdd_red_2026.out`.
