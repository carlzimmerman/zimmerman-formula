# Expansion-sensitive repair: a sharper same-action obstruction

Checkpoint 2026-09-08; base `b7bb6bb3cb0c8241f8470f0ac312daf8d1f15d87`.
The complete-theory goal remains **OPEN**. This is a new action test, not an
amendment of the original action or a universal MOND no-go. No novelty claim.

## 1. What was actually tried

Use the conventions and explicit multiplier action of
[the preceding FLRW calculation](../vcdm_flrw_gate_2026/FLRW_OBSTRUCTION.md),
with minimal matter and a **new** term:

\[
\begin{split}
S={}&M^2\int dt\,d^3x\,N\sqrt h\left[
\frac{R+K_{ij}K^{ij}-K^2}{2}-V(\varphi)-\frac34\lambda^2
-\lambda(K+\varphi)-\frac{\lambda_{\rm gf}^iD_i\varphi}{N}
+f(s)+sB(K)\right]+S_m[g,\psi],\\
s={}&a_i a^i,\quad a_i=D_i\log N,\quad
f(s)=2a_0^2[1-(1+\sqrt{s}/a_0)e^{-\sqrt{s}/a_0}],\\
B(K)={}&-\frac{K^2}{K^2+K_0^2},\qquad M^2=(8\pi G)^{-1}>0,\quad K_0>0.
\end{split}
\]

Here c=1; K0 has inverse-length units. Varying lambda and lambda_gf gives
lambda=-2(K+varphi)/3 and D_i varphi=0. After eliminating lambda, the kinetic
block is K_T^2/2 + 2 varphi K/3; the new term adds sB(K).
For k!=0 the varphi equation fixes the longitudinal gauge-fixing multiplier,
not another metric scalar constraint. Its homogeneous mode is retained below.

The proposed mechanism is specific: B(0)=B'(0)=0 leaves a static K=0 branch
unchanged at **first variation**, whereas B(3H) changes the FLRW lapse response.
It is not enough that the value of an added term vanish on a background.

The static weak-field density remains

\[
L_{\rm stat}=M^2[(\nabla\Psi)^2-2\nabla\Phi\cdot\nabla\Psi
+f((\nabla\Phi)^2)]-\rho\Phi.
\]

Its independent variations give Delta(Phi-Psi)=0 and
Delta Psi - div(f_s grad Phi)=rho/(2M^2). With regularity and matched boundary
data removing harmonic slip, both potentials therefore obey

\[
\Phi=\Psi,\qquad
\nabla\cdot[(1-e^{-|\nabla\Phi|/a_0})\nabla\Phi]=4\pi G\rho.
\]

These are leading quasistatic equations, not a moving-source PPN certificate.
The high-acceleration coefficient measures G on this branch. Full beta and
preferred-frame parameters have not been computed for the new action.

## 2. The intended cosmological change really occurs

On homogeneous FLRW, s=0 identically, so the new term does not change the
background equations or the genuine homogeneous canonical action. At quadratic
order it changes the coefficient of (grad n)^2 to

\[
\alpha_{\rm FLRW}=f_s(0)+B(3H)=\frac{K_0^2}{9H^2+K_0^2}<1\quad(H\ne0).
\]

Terms s B'(3H) delta K start at cubic order. Substitution into the preceding
**action-derived general-alpha** FLRW calculation gives, for timelike P(X)
matter, q=dot sigma>0, Z=P_X>0, D=P_X+q^2 P_XX>0,

\[
\mathcal K_{u,\rm UV}\to D,\qquad c_{u,\rm UV}^2\to Z/D.
\]

This removes the previous wrong-sign UV coefficient on exactly FLRW. It is
**not** full stability: auxiliary elimination is singular at

\[
\kappa_*^2=\frac{Dq^2(9H^2+K_0^2)}{18M^2H^2}>0.
\]

This singular reduction is not by itself proof of a physical pole. Its
regular-variable evolution would require another calculation if the candidate
survived the next gate. At k=0 the added action vanishes before variation;
the prior homogeneous canonical calculation is reused with its inputs pinned.
It derives rank 2, two first-class and two second-class constraints, one
homogeneous matter/background pair, and an explicit H=1/(3t) expanding solution.
This is not obtained by taking k->0 in the local static formulas.
The expansion and UV limits do not commute: taking H->0 first recovers
K_u,UV=-6Z-9Z^2/D<0, not D. The script checks both orders.

## 3. Actual static principal Dirac calculation

Take a regular local static patch, finite y0=|a_bar|/a0>0, and a nonzero wave
vector perpendicular to a_bar. Set m=M^2, alpha=e^(-y0), r=s_bar/K0^2, b=-r.
After scalar spatial gauge fixing, h_ij=exp(2z cos kx) delta_ij, lapse
perturbation n cos kx, shift N^x=v sin kx. The script constructs the ADM
tensors and keeps quadratic terms with two perturbation derivatives. Twice
the mode average is

\[
L_2=m\left[b(3\dot z-kv)^2+\frac{k^2v^2}{3}
+k^2(z^2+2nz+\alpha n^2)\right].
\]

For b!=0 the only primaries in this reduced sector are p_n,p_v. The momentum
p=6mb(3 dot z-kv) and the canonical Hamiltonian give two secondaries:

\[
H_c=\frac{p^2}{36mb}+\frac{kvp}{3}-\frac{mk^2v^2}{3}
-mk^2(z^2+2nz+\alpha n^2),\quad
C_n=2mk^2(z+\alpha n),\quad C_v=-kp/3+2mk^2v/3.
\]

In order (p_n,p_v,C_n,C_v), direct canonical differentiation yields

\[
\Omega=\begin{pmatrix}
0&0&-2m\alpha k^2&0\\
0&0&0&-2mk^2/3\\
2m\alpha k^2&0&0&-2mk^3/3\\
0&2mk^2/3&2mk^3/3&0
\end{pmatrix},\qquad
\det\Omega=\frac{16m^4\alpha^2k^8}{9}.
\]

Preservation fixes u_n=-kv/(3 alpha)-p/(18m alpha b), u_v=k(n+z).
All preservation residuals vanish; no tertiary condition remains in this
constant-coefficient principal system. The computed rank is four: four
second-class constraints, no first-class constraints, (6-4)/2=**one scalar
canonical pair**. It comes from the gravitational variables, not added matter.

Solving n=-z/alpha and v=p/(2mk) gives

\[
H_{\rm red}=\frac{1+3b}{36mb}p^2+mk^2\frac{1-\alpha}{\alpha}z^2,
\quad \mathcal K_z=-\frac{18mr}{1-3r},\quad
c_z^2=-\frac{(e^{y_0}-1)(1-3r)}{9r}.
\]

For 0<r<1/3 the kinetic sign is negative relative to the positive tensor
normalization and c_z^2<0. For r>1/3 this transverse scalar has positive signs
but still exists. At r=1/3 the same Poisson matrix retains rank four; H_red
loses its p^2 term and dot z=0, dot p=-2mk^2(e^y0-1)z. This is degenerate
evolution of one pair, not a new constraint. The exact fixture m=k=1,
alpha=1/2, b=-1/12 gives K_z=-2, c_z^2=-1.

At b=0 the Legendre transform is rebuilt: all three momenta become primary.
For alpha!=1 there are three independent secondaries, rank six, zero scalar
pairs. At the physical y0=0 point (b=0, alpha=1) there are only two independent
secondaries, rank four and one linear first-class direction p_z-p_n. No scalar
pair occurs at that quadratic point. This rank change is **not** evidence of
a nonlinear gauge symmetry or controlled strong coupling. The nonstatic loci
K=+/-K0/sqrt(3), where B''=0, are not covered by the static calculation.

## 4. A structural restriction, not another coefficient scan

Within the class of additions sB(K), maintaining the original zero trace
velocity Hessian at every s>0 and K requires sB''(K)=0. Hence B=c0+c1 K.
Keeping the static constitutive equation unchanged gives c0=0. But a c1 sK
term changes the static shift variation by

\[
\delta_{N^i}S_{\rm new}=m c_1\int\sqrt h\,D_i s\,\delta N^i.
\]

On the unchanged static branch Kij=0 and D_i varphi=0, with arbitrary spatially
varying acceleration, this cannot vanish unless c1=0. Thus the **only** member
of this restricted additive family preserving both properties is B=0.
Compensating new operators, a changed primary relation involving lapse
velocities, or different branches are outside this restriction.
Strictly preserving the *literal original trace primary* is an even stronger
requirement: before setting B''=0, its momentum relation changes to
pi-M^2 sqrt(h) varphi=(3/2)M^2 sqrt(h) sB'(K). The B'' argument above preserves
trace degeneracy, not necessarily that original relation.

The same argument covers **any C^2 local addition F(s,K)** (not just sB(K)),
on a connected product domain I x J with 0 in J, with no other changed
operators or multipliers. For the FLRW conclusion require a regular
first-derivative extension to s=0; s>0 may be treated first.
F_KK=0 integrates to F=A(s)K+C(s). Preserving the fixed exact static
constitutive coefficient requires C'(s)=0. Preserving the arbitrary static
momentum equation requires D_i A(s)=A'(s)D_i s=0, hence A'(s)=0. Therefore

\[
F(s,K)=c_1K+c_0,\qquad F_s(s,3H)=0.
\]

The constant-K term is a boundary term and c0 shifts only the potential;
neither changes the FLRW lapse-gradient coefficient. This is a uniform
restriction by elementary integration and independent variations, not an
exhaustive numerical scan. It preserves trace **degeneracy**, not necessarily
the identical original momentum relation. Explicit time-dependent constants
would additionally create a homogeneous volume term after integration by parts;
they still cannot produce the missing spatial lapse-gradient correction.
`general_local_deformation()` checks the variational reduction symbolically.

## 5. Different constraint architecture: independent second screen

The luminal extended-cuscuton seed is a distinct test; it is not used to lend
properties to the expansion-switch action. We checked the primary source
[Iyonaga, Takahashi and Kobayashi, arXiv:1809.10935v2](https://arxiv.org/html/1809.10935v2),
Eqs. 14, 42, 78 and 84, on 2026-09-08. The source's A5=0 Hamiltonian is affine
in lapse; its trace metric Hessian is nonzero, unlike the VCDM seed.

`cuscuton_screen.py` independently derives that Legendre cancellation using
all six symmetric metric velocities. Adding the unchanged MOND term gives
H_f=-m integral N sqrt(h) f(s), whose functional lapse Hessian on homogeneous
lapse has nonzero-mode symbol

\[
\frac{\delta^2H_f}{\delta N^2}(k)
=-\frac{2m\sqrt h\,f_s(0)}{\bar N}\kappa^2
=-\frac{2m\sqrt h}{\bar N}\kappa^2.
\]

The lapse-primary/secondary bracket therefore becomes invertible for k!=0;
preservation fixes the lapse multiplier instead of continuing the seed's
scalar-removing constraint chain. This directly added potential fails the
seed's mechanism. The script does not assign a full nonlinear gravitational
count from a two-by-two bracket, and k=0 is explicitly separate. The source
alone does not cover lapse-gradient operators; the displayed functional
variation is the new calculation needed for this application. No global
literature/novelty search or source-cache claim is made.

## 6. Path forward, and what this checkpoint does not claim

**Decision:** reject the expansion switch for the required regular galactic
branch. Reject bare extended-cuscuton + f as a two-tensor completion. Do not
repeat these two additive repairs by tuning V, K0 or time-dependent coefficients.

The next live route is a **correlated kinetic/clock completion**, not another
potential appended to a two-tensor seed. First calculate its actual functional
degeneracy and constraint preservation while retaining exact static MOND. For
an affine-lapse completion, a concrete sufficient structural target is

\[
\mathbb D=\mathcal L_{NN}
-\mathcal L_{N\dot h}\mathcal L_{\dot h\dot h}^{-1}
\mathcal L_{\dot h N}=0,
\]

where L denotes the **gravitational** Lagrangian, derivatives are functional
operators and compositions retain spatial derivatives. Ordinary matter must
already have been Legendre-transformed and be held at fixed canonical matter
variables; minimal matter then adds a lapse-affine Hamiltonian. The displayed
metric-only complement must not be applied to the total Lagrangian while
holding matter velocities fixed. For this complement H_NN=-D. Its strong
vanishing is a chosen sufficient structural target, not a universal necessity:
a more general construction could satisfy a weak condition modulo constraints.
This form applies to an invertible metric-velocity block without lapse
velocities. A lapse-velocity construction requires the enlarged Hessian
and an additional independent scalar-elimination condition. A null Hessian
alone does not close either theory: continue preservation, including ordinary
matter, before advancing to cosmology, PPN or data fitting. The initial test
must include a nonzero-acceleration patch as well as FLRW; testing only FLRW
would miss the scalar just found here.

No theorem here excludes every such correlated construction. No full nonlinear
Dirac analysis, global static solution, complete PPN calculation or empirical
prediction has been completed for a surviving candidate. Lean is not on the
current PATH; this evidence is exact SymPy computation with an analytic
reduction and independent review, not a Lean certificate. Large observational
fits would not settle the demonstrated constraint obstruction.

Original theory and empirical artifacts are untouched. This checkpoint builds
on the previous same-action audit; it does not infer intent or dishonesty from
disagreement between assistants. The current original action document itself
says it is a candidate rather than a closure.
