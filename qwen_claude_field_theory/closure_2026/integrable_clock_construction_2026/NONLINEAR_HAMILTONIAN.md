# IC4 nonlinear Hamiltonian and the remaining functional closure problem

Base: `6708f1e3e695a99f3fc3f121e14528f68ace641c` (2026-09-08).
Input: [IC4_ACTION.md](IC4_ACTION.md), SHA256
`cb37292e21e0b1fbeef59a20f7800cb3d32c0cd20a46d36fd286cc3dd0f467a8`.

Verdict: the gravity plus canonical-clock Hamiltonian and its local
auxiliary variational operator are explicitly derived below. Functional
closure is **conditional on an unproved operator inverse**, not established
by this computation. Ordinary matter is retained as its unspecified
Hamiltonian functional, not silently set to zero in a full-theory count.

## 1. Domain and canonical conventions

Use unitary clock coordinates on a timelike-clock patch, $T=t$, and write
$\xi=\ln N$, $w=(u-1)\xi$, $g_{ij}=\bar h_{ij}$ in this note. Thus the
physical spatial metric is $h_{ij}=e^{2w}g_{ij}$; matter still uses the
physical spacetime metric. Assume $g$ positive definite, finite $\xi$,
$0<u<1$, $m,a_0,\kappa>0$, and sufficient smoothness for the derivatives
below. The metric Legendre inverse is restricted to $t_K\ne0$, defined
below. This is not an assumption that the auxiliary differential operator
is invertible.

The Einstein–Hilbert term uses its usual ADM temporal/spatial boundary
choice. The separate spatial integration by parts below requires either a
closed leaf or boundary/decay data making its flux and the subsequent
variation boundary terms vanish. Boundary charges are not computed.

The canonical one-form is $\int\pi^{ij}\delta g_{ij}$, with both ordered
indices summed. For independent components ordered as
$(11,22,33,12,13,23)$, canonical momenta are
$(\pi^{11},\pi^{22},\pi^{33},2\pi^{12},2\pi^{13},2\pi^{23})$.
The code differentiates all six independent velocities with these weights;
it does not infer the Legendre map from a diagonal ansatz.

The point transformation itself gives

\[
\bar\pi^{ij}=e^{2w}\pi_{\rm phys}^{ij},\qquad
p_{\xi,\rm bar}=p_{\xi,\rm phys}+2(u-1)\pi_{\rm trace},\qquad
p_{u,\rm bar}=p_{u,\rm phys}+2\xi\pi_{\rm trace}.
\]

These signs are checked by the actual symplectic one-form. In barred
variables the last two momenta vanish, rather than being discarded by a
time integration by parts.

## 2. Spatial identity and six-component Legendre transform

Put

\[
V_{ij}=\tfrac12(\dot g_{ij}-\mathcal L_{\boldsymbol N}g_{ij}),\quad
V=g^{ij}V_{ij},\quad
C=\frac m2\sqrt g\,e^{(3u-4)\xi}.
\]

Directly differentiating $h=e^{2w}g$, with
$\dot w=(u-1)\dot\xi+\xi\dot u$, gives
$Q_{ij}=e^{2w}V_{ij}/N$. Both independent auxiliary velocities cancel.
Let $\mathfrak F=A_R(\xi-1/4)+B_R(u-2/3)$ and

\[
\bar J=\frac{3}{4\ell^2}
 [\alpha |D\xi|^2+\beta D\xi\cdot Du+\gamma|Du|^2],\qquad
t_K=-\frac23+\frac{e^{-2w}}{a_0^2}(\bar J+\mathfrak F R[g]).
\]

All constants are those in the pinned IC4 action, including its selected
$\sigma=1/3$. The code carries them symbolically during the identities and
also supplies their exact action dictionary.

The kinetic density is therefore

\[
L_K=C(V_{\rm TF}^{ij}V_{{\rm TF},ij}+t_KV^2),\qquad
\pi^{ij}=C(V_{\rm TF}^{ij}+t_K Vg^{ij}).
\]

Consequently $\pi=3Ct_KV$ and

\[
V_{ij}=\frac1C\left(\pi_{{\rm TF},ij}
                  +\frac{\pi}{9t_K}g_{ij}\right),\qquad
\boxed{H_K=\frac1C\left(\pi_{\rm TF}^{ij}\pi_{{\rm TF},ij}
                          +\frac{\pi^2}{9t_K}\right).}
\]

The actual six-component velocity Hessian has orthonormal determinant
$3C^6t_K/8$. General congruence on symmetric tensors multiplies this by
$(\det g)^{-4}$. At $t_K=0$ its rank is five, so the displayed inverse is
not used there. No assertion about positivity of the unconstrained
gravitational trace kinetic term follows from invertibility.

For the spatial terms, the conformal Ricci identity gives

\[
R[h]=e^{-2w}(R[g]-4\Delta w-2|Dw|^2),\quad
A=\frac m2 e^{u\xi}.
\]

Since $Dw=(u-1)D\xi+\xi Du$ and $D\ln A=uD\xi+\xi Du$,

\[
\begin{split}
&\sqrt g A[-4\Delta w-2|Dw|^2+2(1-u^2)|D\xi|^2]\\
&\quad=\sqrt g A[4u\xi D\xi\cdot Du+2\xi^2|Du|^2]
             -4\sqrt g D_i(A D^i w).
\end{split}
\]

The pure $|D\xi|^2$ coefficient cancels exactly; omitting $\xi Du$ in
$Dw$ fails the check. Together with the canonical-clock contribution,
the rest of the Hamiltonian density is

\[
\boxed{\begin{split}
H_{\rm sp}={}&-\frac m2\sqrt g e^{u\xi}
 [R[g]+4u\xi D\xi\cdot Du+2\xi^2|Du|^2]\\
&+m\sqrt g e^{(3u-2)\xi}[\Lambda+a_0^2U(u^2)]
-\frac\kappa2\sqrt g e^{(3u-4)\xi}.
\end{split}}
\]

The negative last term is the Hamiltonian of $\kappa X$ after unitary
clock gauge fixing. Its auxiliary derivatives are nonzero and retained.

## 3. Explicit local auxiliary equations

Write $H_0=\int\sqrt g\,\mathcal H$, with $P^{ij}=\pi^{ij}/\sqrt g$,
$P=g_{ij}P^{ij}$, $A_P=P_{\rm TF}^{ij}P_{{\rm TF},ij}$, $B_P=P^2$.
Define $a_i=D_i\xi$, $b_i=D_i u$, and

\[
G=\frac2m e^{(4-3u)\xi},\quad E=e^{u\xi},\quad
V_0=\Lambda+a_0^2U(u^2),\quad
\mathcal K=G(A_P+B_P/(9t_K)),\quad
L_R=R+4u\xi a\cdot b+2\xi^2 b^2.
\]

At fixed metric, momenta and first auxiliary jets, the needed derivatives
of $t=t_K$, with $r=e^{-2w}/a_0^2$ and $j_0=3/(4\ell^2)$, are

\[
\begin{array}{ll}
t_\xi=-2(u-1)(t+2/3)+r A_RR,&
t_u=-2\xi(t+2/3)+r B_RR,\\
t_{a_i}=rj_0(2\alpha a^i+\beta b^i),&
t_{b_i}=rj_0(\beta a^i+2\gamma b^i).
\end{array}
\]

The actual local partials are

\[
\begin{split}
\mathcal H_\xi={}&(4-3u)\mathcal K-\frac{GB_Pt_\xi}{9t^2}
-\frac m2 E[u L_R+4u a\cdot b+4\xi b^2]\\
&+m(3u-2)e^{(3u-2)\xi}V_0
-\frac\kappa2(3u-4)e^{(3u-4)\xi},\\
\mathcal H_u={}&-3\xi\mathcal K-\frac{GB_Pt_u}{9t^2}
-\frac m2 E[\xi L_R+4\xi a\cdot b]\\
&+m e^{(3u-2)\xi}[3\xi V_0-2a_0^2u\ln^2(1-u^2)]
-\frac{3\kappa\xi}{2}e^{(3u-4)\xi},\\
\mathcal H_{a_i}={}&-\frac{GB_Pt_{a_i}}{9t^2}-2mEu\xi b^i,\\
\mathcal H_{b_i}={}&-\frac{GB_Pt_{b_i}}{9t^2}
-2mE(u\xi a^i+\xi^2b^i).
\end{split}
\]

Thus the two secondary constraint densities, with this sign convention,
are explicitly

\[
\boxed{S_A=\frac{\delta H_0}{\delta q_A}
=\sqrt g(\mathcal H_{q_A}-D_i\mathcal H_{q_{Ai}})=0,
\qquad(q_1,q_2)=(\xi,u).}
\]

The displayed divergences act on **all** coefficient fields, including
metric, curvature and momentum dependence. They are not homogeneous
algebraic partial derivatives. The program retains a local jet generator
for these expressions instead of suppressing those derivatives.

Let $H^{00}_{AB}=\mathcal H_{q_Aq_B}$,
$H^{01}_{A,Bj}=\mathcal H_{q_Aq_{Bj}}$,
$H^{10}_{Ai,B}=\mathcal H_{q_{Ai}q_B}$ and
$H^{11}_{Ai,Bj}=\mathcal H_{q_{Ai}q_{Bj}}$. All four arrays are computed by
differentiating the nonlinear density, including derivatives of $t$.
The scalar auxiliary operator is

\[
\boxed{\mathcal M_{AB}\eta_B=
H^{00}_{AB}\eta_B+H^{01}_{A,Bj}D_j\eta_B
-D_i[H^{10}_{Ai,B}\eta_B+H^{11}_{Ai,Bj}D_j\eta_B].}
\]

In particular its actual gradient Hessian is

\[
H^{11}_{Ai,Bj}=\frac{GB_P}{9}
 \left(\frac{2t_{Ai}t_{Bj}}{t^3}-\frac{t_{AiBj}}{t^2}\right)
 -mE\begin{pmatrix}0&2u\xi\\2u\xi&2\xi^2\end{pmatrix}_{AB}g^{ij},
\]

where
$t_{AiBj}=rj_0\left(\begin{smallmatrix}2\alpha&\beta\\\beta&2\gamma\end{smallmatrix}\right)_{AB}g^{ij}$.
The principal symbol is $H^{11}_{Ai,Bj}k_i k_j$. This note does not infer
its invertibility from its order, from a frozen mode, or from formal
self-adjointness. It does not identify the exact zero mode with a
nonzero-mode limit.

## 4. Correct secondary–secondary bracket

For compactly supported or boundary-compatible scalar test functions $f_A$,

\[
S[f]=\int\sqrt g\,\widehat f,\qquad
\widehat f=f_A\mathcal H_{q_A}+(D_i f_A)\mathcal H_{q_{Ai}}.
\]

This first-jet expression is useful because its metric and momentum
variations need no distributions left implicit. Hold covectors
$Dq,Df$ fixed in the algebraic metric derivative and keep the dependence
$P^{ij}=\pi^{ij}/\sqrt g$. With symmetric tensor derivatives,

\[
\begin{split}
E_f^{ij}:=\frac{\delta S[f]}{\delta g_{ij}}
=\sqrt g\bigg[\frac12g^{ij}\widehat f
 +\left(\frac{\partial\widehat f}{\partial g_{ij}}\right)_{\pi,R,q,Dq,Df}
-\widehat f_RR^{ij}
+(D^iD^j-g^{ij}\Delta)\widehat f_R\bigg],\\
B_{f,ij}:=\frac{\delta S[f]}{\delta\pi^{ij}}
=\sqrt g\left(\frac{\partial\widehat f}{\partial\pi^{ij}}\right)_{\rm sym},\\
\boxed{\Omega[f,g]:=\{S[f],S[g]\}
=\int (E_f^{ij}B_{g,ij}-B_{f,ij}E_g^{ij}).}
\end{split}
\]

The last two metric terms follow by varying scalar curvature,
$\delta R=-R^{ij}\delta g_{ij}+D^iD^j\delta g_{ij}
-\Delta(g^{ij}\delta g_{ij})$, and integrating twice. They cannot be
omitted because $t$ depends on curvature. The program checks the flat-point
curvature adjoint and the actual six-component normalized-momentum metric
variations. For example,

\[
\partial_g A_P=2P^{ik}g_{k\ell}P^{\ell j}
-\frac{2P}{3}P^{ij}-A_Pg^{ij},\quad
\partial_g B_P=2PP^{ij}-B_Pg^{ij}.
\]

The auxiliary canonical pair does not contribute to $\Omega$ because
$S_A$ contains no $p_A$. The metric pair generally does. As an actual
nonlinear diagnostic, take a unit coordinate-volume homogeneous restriction with isotropic metric
$g=a^2\delta$ with conjugate $p_a$, so

\[
H_{\rm hom}=-\frac{e^{(4-3u)\xi}p_a^2}{12ma}
+a^3\left[m e^{(3u-2)\xi}V_0-\frac\kappa2e^{(3u-4)\xi}\right].
\]

At $a=p_a=1$, $\xi=0$, $u=1/2$, leaving all action parameters unchanged,
direct differentiation gives
$\{\partial_\xi H_{\rm hom},\partial_u H_{\rm hom}\}
=-5a_0^2\ln^2(3/4)/4\ne0$. This point does **not** satisfy both auxiliary
constraints: it rules out an identically zero bracket, not a nonzero
bracket on the constraint surface. Nor is it an expanding physical solution.
No IC4 quadratic bracket or count has been imported into this result.

## 5. Preservation and the precise unproved implication

The primary constraints are $p_\xi=p_u=P_i^{\rm shift}=0$. The raw shift
coefficient is $-2g_{ik}D_j\pi^{jk}$; adding terms proportional to primaries
gives the spatial-diffeomorphism generator

\[
\mathcal H_i=-2g_{ik}D_j\pi^{jk}
+p_\xi D_i\xi+p_uD_i u\quad(+\mathcal H_{m i}).
\]

Its spatial-covariance identities hold with compatible boundary terms;
they are not a new lapse Hamiltonian-constraint algebra. The total
Hamiltonian may be written $H_T=H_0+\int N^i\mathcal H_i+\int\lambda_Ap_A$
plus the shift-primary multipliers. Primary preservation gives $S_A=0$.

Define the coordinate-density Hessian $\mathbb K=\sqrt g\,\mathcal M$,
so $\delta S=\mathbb K\delta q$. Then

\[
\{p[f],S[g]\}=-\int\sqrt g\,g_A\mathcal M_{AB}f_B,
\qquad
\mathbb O_{(p,S)}=
\begin{pmatrix}0&-\mathbb K\\\mathbb K&\Omega\end{pmatrix}.
\]

Here formal self-adjointness of $\mathbb K$ uses coordinate measure;
$\mathcal M$ uses $\sqrt g$ measure. Confusing these density conventions
would change the block identification. If, and only if justified on a
specified branch/domain, $\mathbb K$ has a two-sided compatible inverse,
the block algebra gives

\[
\mathbb O^{-1}=
\begin{pmatrix}
\mathbb K^{-1}\Omega\mathbb K^{-1}&\mathbb K^{-1}\\
-\mathbb K^{-1}&0
\end{pmatrix},\qquad
\mathbb K\lambda=-\{S,H_0\}\quad\text{modulo spatial transport}.
\]

No commutation of $\mathbb K$ with $\Omega$ is needed. A noncommuting finite
block check verifies this algebra but is not a discretization or proof of
the spatial inverse. Under that inverse hypothesis secondary preservation
fixes the two auxiliary multipliers rather than imposing a tertiary
constraint. A kernel instead requires compatibility/rank analysis that is
not done here.

For the gravity–clock system without additional matter, those hypotheses
would yield four second-class auxiliary constraints and the usual six
first-class spatial/shift constraints: conditionally three configuration
degrees of freedom (two tensor and one scalar). This is a conditional
arithmetic consequence, not a certified full nonlinear count or a
positivity/causality result.

The named remaining gap is to specify the nonlinear constraint surface and
boundary/function spaces, solve $S_A=0$ with regularity, establish a
two-sided inverse or classify the kernel of $\mathbb K$, and prove that
the selected rank branch persists under evolution. The surface $t_K=0$
also requires a separate analysis. No zero-mode or boundary kernel is
removed by decree.

For an ordinary matter action admitting its regular standard ADM Legendre
transform without metric velocities, append
$H_m[N=e^\xi,h=e^{2w}g,\psi,p_\psi]$ and its shift generator. The actual
$\delta H_m/\delta q_A$ and Hessian must then be included above, together
with the matter canonical contribution to $\Omega$. A statement that
matter is minimally coupled does not specify these derivatives for every
possible $S_m$. This computation cannot certify the unspecified matter
sector. Fixing the timelike clock also presupposes the usual diffeomorphism
Ward relation when reconstructing the clock equation; it is not permission
to omit a metric constraint.

## 6. Reproduction and evidence boundary

The Python uses exact SymPy algebra and a generic six-component symmetric
metric. It also has independently derived mutation controls for
off-diagonal factors, omitted auxiliary velocity, missing divergence,
curvature variation and incorrectly discarded $\Omega$. The polynomial
jet benchmark verifies the Euler/Frechet assembly; the full nonlinear
IC4 density independently supplies its coefficient arrays. No random scan,
floating-point rank, numerical PDE solver or external theorem is used.

Commands from this directory:

```text
python3 -B test_nonlinear_hamiltonian.py
python3 -B nonlinear_hamiltonian.py
python3 -B nonlinear_hamiltonian.py --require-functional-closure
```

The ordinary script reports exact-identity computation success; the last
flag deliberately returns 2 while the functional-closure hypothesis remains
unproved. Source-pin mismatch returns 1. The JSON-safe `run()` records the
base, source and implementation hashes, exact checks, software versions and
the unproved implication. Test-first red/green history and final run results
are recorded in the task handoff. No commit or prior-file edits are made.

Verification on Python 3.9.6 / SymPy 1.14.0: 11 tests passed; ordinary
script exit 0 with 28 exact checks and matching source hash; the
closure-required invocation exited 2. The embedded version-1 computation
manifest passed the Mathbox validator, including its project-relative
artifact hash check. Its legacy limitations remain explicit: no enforced
resource caps and no separate immutable result artifact. Those provenance
checks do not promote conditional functional closure to a theorem.
