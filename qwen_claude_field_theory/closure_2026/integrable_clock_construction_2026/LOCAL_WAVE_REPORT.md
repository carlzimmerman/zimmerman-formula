# IC-4: constructing a healthy local scalar wave from the action

2026-09-08; starting checkpoint `0a9f9fa33`. **Full theory OPEN.**

The new result is a joint construction, not another failed-model list:
the explicit [IC-4 action](IC4_ACTION.md) has a positive, wave-number-independent
scalar kinetic coefficient and a local, positive-frequency scalar wave on
the same exact expanding branch. Its physical clock norm also obeys a local
wave equation. Both come from varying and reducing that action.

The construction preserves the prior static equations and the expanding
background without setting $H=0$, and preserves luminal positive tensor
propagation on that background. It does not close the whole gravity target.

## 1. The missing adjustable term

IC-2 had positive quadratic kinetic energy but a negative-frequency band.
The retuned $J$ calculation in [clock_locality_completion.py](clock_locality_completion.py)
found a constant-kinetic family; changing $J$ alone still left a physical
clock-response denominator. Those calculations are intermediate construction
evidence, not results for IC-4.

The new ingredient is $Q^2\widehat R F/a_0^2$, where $F$ vanishes on the
chosen expanding background but its field derivatives do not. Thus it can
alter the scalar constraint sources without changing that background, the
stationary $Q=0$ equations or the pure tensor quadratic action.

The full density is differentiated, including the physical volume, lapse,
shift, and $Q$ perturbations. With

\[
\bar h_{ij}=B^2e^{2\epsilon z\cos(kx^1)}\delta_{ij},\quad
\ln N=1/4+\epsilon n\cos(kx^1),\quad
u=2/3+\epsilon v\cos(kx^1),\quad
N^1=\epsilon b_{\rm shift}\sin(kx^1),
\]

the added quadratic action is

\[
\frac{\Delta L_2}{m e^{-1/2} B^3 h^2}
=xz\frac{16\ell^2}{3}(A_R n+B_Rv)=xz(p_Rn+q_Rv),
\qquad x=\frac{k^2N_0^2}{A^2h^2}.
\]

Here $L_2$ is twice the spatial average of the $\epsilon^2$ coefficient,
as in the pinned source. $x=(k_{\rm phys}/H_{\rm phys})^2$, not a coordinate
speed normalization. Write $\tau=h(t-t_0)$, $y=z'=\dot z/h$; then
$x'=-2x$. The symbol $y$ in this report is a velocity amplitude, **not**
the static MOND variable $|\nabla\Phi|/a_0$.

## 2. Joint source and kinetic matching

After varying the shift, $n=y/2+3v/8$. In the rank-one $J$ family of
IC4_ACTION.md the remaining action is

\[
\mathcal L=
\left(3+\frac{\alpha x}{4}\right)y^2
-\frac{9(\mathcal T+ex)}{\mathcal T}yv
+(\mathcal T+ex)v^2
+\left(\frac23+\frac{p_R}{2}\right)xzy
+\left(1+\frac{3p_R}{8}+q_R\right)xzv+xz^2.
\]

Solving for the vanishing position source fixes
$q_R=-1-3p_R/8$. The actual auxiliary equation then gives

\[
v=\frac{9}{2\mathcal T}y,\qquad
n=\frac{8\mathcal T+27}{16\mathcal T}y.
\]

The three-by-three matrix of the actual $n,v,b_{\rm shift}$ equations,
using $S=k b_{\rm shift}/h$ as the shift variable, has determinant
$-32(\mathcal T+ex)$, which is nonzero for $x\ge0$ and $e>0$.
This is an auxiliary-equation matrix, **not** a Poisson-bracket matrix.

After elimination, $\mathcal L=a_*y^2+b(x)zy+xz^2$, with

\[
a_*=3-\frac{81}{4\mathcal T}>0,\quad
b(x)=\left(\frac23+\frac{p_R}{2}\right)x.
\]

Positivity follows from $\ell=\ln(9/5)<4/5$, hence
$\mathcal T>27/4$. The logarithm bound follows directly from
$[t-\ln(1+t)]'=t/(1+t)>0$ and its zero value at $t=0$.

The time-dependent measure must be retained when integrating $bzy$:

\[
g(x)=x-\frac32 b+x b_x=\left(\frac23-\frac{p_R}{4}\right)x.
\]

Solving $g=-a_*\sigma x$ fixes $p_R=8/3+4a_*\sigma$. The reduced action
is therefore, up to the explicitly checked local time boundary,

\[
L_{2,\rm red}=m e^{-1/2}B^3 a_*
\left[\dot z^2-\sigma\frac{N_0^2 k^2}{A^2}z^2\right].
\]

Consequently, for every nonzero wave number on this background,

\[
\boxed{z''+3z'+\sigma xz=0,\qquad
n''+5n'+(6+\sigma x)n=0.}
\]

The second equation follows by differentiating the reconstructed lapse,
not by assuming a separate clock oscillator. The physical scalar is
$\delta X=-e^{-1/2}n$; the background clock norm is constant, so this
linear perturbation is gauge invariant. Proper-time conversion gives
$c_s^2=\sigma c^2$, with the explicit choice $\sigma=1/3$.
There is no negative-frequency band in these equations and no scalar pole
introduced by their auxiliary reduction. This statement is background- and
sector-specific, not a claim about all field configurations.

The positive mode energy satisfies the exact identity

\[
E=\tfrac12(y^2+\sigma xz^2),\qquad
E'=-3y^2-\sigma xz^2\le0.
\]

## 3. Actual quadratic Dirac closure

[quadratic_dirac.py](quadratic_dirac.py) restores the longitudinal spatial
gauge variable $E$, independently checks the ADM spatial pullback, and uses
$b_{\rm shift}\mapsto b_{\rm shift}-\dot E/k$ in the action. Write
$\mathcal F=m e^{-1/2}B^3$, so $\dot{\mathcal F}=3h\mathcal F$.
The coordinates are $(z,E,n,v,b_{\rm shift})$; the active $(\dot z,\dot E)$
Hessian has determinant $-4\mathcal F^2$. This indefinite unreduced matrix
contains a gauge variable and is not the physical kinetic-energy test.

The generated primary constraints are $p_n,p_v,p_b$. The Hamiltonian can be
written using $\mathbf q=(n,v)^T$ and $C=1+a_*\sigma$ as

\[
H=\frac{3p_E^2}{4\mathcal F}-\frac{p_Ep_z}{2\mathcal F}
+k b_{\rm shift}p_E+\tfrac12\mathbf q^TM\mathbf q
+h(2n-3v/4)p_z
+\mathcal Fh^2Cxz(-4n+3v/2)-\mathcal Fh^2xz^2,
\]
\[
\frac{M}{\mathcal Fh^2}=
\begin{pmatrix}
-24-\dfrac{81x}{4\mathcal T^2}
&27+\dfrac{9x}{4\mathcal T}+\dfrac{243x}{32\mathcal T^2}\\
27+\dfrac{9x}{4\mathcal T}+\dfrac{243x}{32\mathcal T^2}
&-2\mathcal T-\dfrac{135}{8}-\dfrac{x}{4}
 -\dfrac{27x}{16\mathcal T}-\dfrac{729x}{256\mathcal T^2}
\end{pmatrix}.
\]

Preservation produces $C_n=-H_n$, $C_v=-H_v$, $C_b=-kp_E$. Explicitly,

\[
\binom{C_n}{C_v}=
\binom{-2hp_z+4\mathcal Fh^2Cxz}
      {3hp_z/4-3\mathcal Fh^2Cxz/2}-M\binom n v.
\]

The actual Poisson matrix, in the order $(p_n,p_v,p_b,C_n,C_v,C_b)$, is

\[
\Omega=\begin{pmatrix}
0&0&0&M_{11}&M_{12}&0\\
0&0&0&M_{12}&M_{22}&0\\
0&0&0&0&0&0\\
-M_{11}&-M_{12}&0&0&0&0\\
-M_{12}&-M_{22}&0&0&0&0\\
0&0&0&0&0&0
\end{pmatrix},\qquad
\det M=\frac{3\mathcal F^2h^4(4\mathcal T-27)(8\mathcal T+x)}{2\mathcal T}>0.
\]

In particular $\{C_n,C_v\}=0$ is computed here; IC-2's corresponding
bracket was nonzero and is not transferred. The independence minor of all
six constraints is $-k\det M\ne0$. The matrix therefore has rank four,
with four second-class constraints and two first-class constraints forming
one spatial-gauge chain. Direct preservation includes both
$3h\mathcal F\partial_{\mathcal F}C$ and $-2hx\partial_xC$;
it fixes the two auxiliary multipliers and leaves only the shift multiplier
free. All three remaining preservation residuals vanish. No extra constraint
or auxiliary momentum pair is omitted at this quadratic level.

The five-coordinate scalar sector consequently has
$(10-2\times2-4)/2=1$ physical pair. Its reduced Hamiltonian agrees with
the independently reduced action, including the time-dependent boundary
canonical map. The separately varied uniform sector has three coordinates,
four second-class constraints and one pair, with the different coefficient
given below. These are finite-mode quadratic calculations, not the full
nonlinear functional count or an automatic matter/gravity classification.

## 4. Canonical readout and physical compact packets

Let $P=\partial\mathcal L_{\rm red}/\partial y=2a_*y+bz$ before
removing the $bzy$ boundary. Then $n,v$ and
$\zeta_{\rm phys}=z-n/3+v/4$ are finite spatial differential expressions
in $(z,P)$. The earlier background boundary shifts the original normalized
trace momentum by $-18z$; that local shift does not change spatial support.

The shift itself still has $b_{\rm shift}=hS/k$, where

\[
S=a_*y+(1+a_*\sigma)xz=P/2.
\]

Thus polynomial lapse readouts alone do not certify full metric causality.
For a constructive physical packet, introduce a wave potential $\mathscr U$
on flat $\mathbb R^3$, with smooth compactly supported initial
$\mathscr U,\mathscr U'$. Its equations and local reconstruction are

\[
\mathscr U''+\mathscr U'+\sigma\mathcal X\mathscr U=0,\qquad
\mathcal X=-\frac{N_0^2}{h^2A^2}\Delta,
\]
\[
z=-\frac{\mathscr U'+\mathscr U}{\sigma},\quad
y=\mathcal X\mathscr U,\quad
n=\frac{8\mathcal T+27}{16\mathcal T}\mathcal X\mathscr U,\quad
v=\frac9{2\mathcal T}\mathcal X\mathscr U,
\]
\[
N^i=-\frac{N_0^2}{hA^2}\partial_i
 [a_*\mathscr U+(1+a_*\sigma)z].
\]

No spatial inverse is used to **construct** these data or evolve them.
Fourier comparison with the reduced equation gives $\mathscr U=y/x$
for $k\ne0$; this inverse relation is not used at $k=0$.
Every displayed field, including the shift and the physical spatial metric,
is obtained by local differentiation. The boundary-shifted normalized momentum $P$ is
$2\mathcal X[a_*\mathscr U+(1+a_*\sigma)z]$; its longitudinal
trace-free reconstruction also has no inverse-Laplacian tail for these data.

For completeness, put $v_c(\tau)=\sqrt\sigma N_0/(hA)$ and
$e_{\mathscr U}=(\mathscr U'^2+v_c^2|\nabla\mathscr U|^2)/2$.
Direct differentiation yields

\[
\partial_\tau e_{\mathscr U}
-\nabla\cdot(v_c^2\mathscr U'\nabla\mathscr U)
=-\mathscr U'^2-v_c^2|\nabla\mathscr U|^2.
\]

The normal flux is bounded by $v_c e_{\mathscr U}$. Integrating this
identity outside an outward-moving front of speed $v_c$ proves zero
exterior energy for initially zero exterior data. The wave and its local
metric readouts therefore remain supported inside that cone. Physical
front speed is $\sqrt\sigma c$. Existence can also be read from the
change $\eta=-\sqrt\sigma N_0/(hA)$, which reduces the equation to
$\partial_\eta^2\mathscr U-\Delta\mathscr U=0$.

This constructs linear physical scalar packets on the specified background.
Compact $\mathscr U$ imposes a compact Poisson primitive for the initial
$y$ and $P$: their harmonic moments vanish. This is a substantive restriction,
not a claim about arbitrary compact $(z,P)$. The positive wave energy is an
estimate for $\mathscr U$, not a norm uniformly equivalent to the original
canonical energy as $k\to0$; metric estimates require enough additional
Sobolev derivatives for the displayed reconstruction.
It does **not** prove an admissible nonlinear lift, a complete parametrization
of every global constrained datum, or all-channel causal support on other
backgrounds. Tensor/vector coupling and ordinary-matter perturbations are
not part of this packet construction.

## 5. Exactly homogeneous is not the zero-wave-number shortcut

The independently varied uniform action gives

\[
a_0^{\rm hom}=\frac{4\mathcal T-27}{9},\quad
n_0=\frac{8\mathcal T+27}{108}y_0,\quad v_0=\frac23 y_0,
\quad z_0''+3z_0'=0.
\]

Here $a_0^{\rm hom}$ is a kinetic coefficient, not the acceleration $a_0$.
It differs from $a_*$; no momentum constraint divided by $k$ is used at
zero wave number. After using each sector's own momentum
$P_0=2a_0^{\rm hom}y_0$, its $n_0(P_0),v_0(P_0)$ equal the $x\to0$
canonical readouts. This comparison is checked symbolically, but does not
identify the global data spaces. Compact packets above have zero integrated
boundary-shifted momentum $P$ and zero integrated $y$, so they do not excite
an independent homogeneous expansion mode. The original normalized trace
momentum is $P-18z$; its integral need not vanish.

## 6. Numerical and independent checks

For $\sigma=1/3$, four deterministic fundamental-matrix problems use
$x_0\in\{10^{-4},1,100,10^4\}$ and $0\le\tau\le6$.
The exact basis is $\cos r+r\sin r$, $\sin r-r\cos r$, with
$r=\sqrt{\sigma x}$; both functions are substituted back into the equation.
Their transfer matrix is independently evaluated at 60 decimal digits and
compared with two DOP853 runs. The retained tolerances are
$(10^{-9},10^{-11},0.1)$ and $(10^{-12},10^{-14},0.05)$ for
(relative tolerance, absolute tolerance, maximum step).

The local run found maximum scaled analytic discrepancy $1.67\times10^{-11}$,
maximum scaled refinement discrepancy $1.84\times10^{-8}$, and no sampled
energy increase. These are finite numerical controls, not the proof of
all-wave-number positivity or of the cone bound.

Independent [operator variation](curvature_operator_bridge.py) reconstructs
the physical metric before calculating $Q$, retains both lapse and auxiliary
velocities before cancellation, and checks a spatial integration-by-parts
identity. Its source-to-action mapping agrees with the separate main program.
Both share the pinned IC-1 background/scalar input; this is not independent
validation of every upstream field equation.

The earlier [IR bound](IR_GROWTH.md) is retained with its own action ID and
provenance. It belongs to IC-2, not IC-4, and is not combined with this action's
passes. Exact commands, statuses and files are in [REPRODUCE.md](REPRODUCE.md).

## 7. Unavoidable next calculation

Derive the full nonlinear secondary functional constraint operator of
**IC-4**, continue preservation and establish the admissible initial-data
correspondence. The primary point-map cancellation and a quadratic wave
cannot replace that calculation. Then test the same action on the actual
galactic branch, including the clock stress and its embedding in FLRW,
before claiming independent no-slip and PPN predictions. The static $u=0$/$|a|=0$
stratum, strong coupling, realistic matter perturbations and empirical tests
remain required. No proof here completes or weakens the thirteen requirements.
