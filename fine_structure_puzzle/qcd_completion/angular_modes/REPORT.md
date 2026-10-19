# Exact next angular ghost sector and finite-wall gauge pairing

FSP-004, based on the frozen FSP-003 checkpoint. This calculation keeps the small circle fixed and the pure SU(2) BPS saddle exact. It evaluates the complete static **J=1 adjoint ghost** determinant, derives the general static ghost angular matrix and establishes the finite-wall longitudinal vector pairing. The ten-channel J=1 vector determinant remains open.

The comparison is the explicit unbroken saddle K=1,h=0, with the same smooth origin and framed Dirichlet ghost wall data. Its holonomy differs from the BPS saddle: it is an auxiliary determinant comparison, not physical broken-vacuum QCD subtraction. No measured alpha, cosmological datum or fitted coefficient enters.

## Action, angular decomposition and actual origin channels

Set t=m_W r, x=m_W R and

\[
K(t)=t/\sinh t,\quad h(t)=\coth t-1/t,\quad
D_i c=\partial_i c+A_i\times c,\quad
A_i=(1-K)(e_i\times n)/t,\quad\Phi=hn.
\]

The actual static ghost quadratic form, obtained by differentiating background divergence along the gauge orbit, is

\[
\langle c,Mc\rangle=\int_{B_x}(|D_i c|^2+|\Phi\times c|^2),\qquad
M=-D_iD_i-(\operatorname{ad}\Phi)^2.
\tag{A1}
\]

An adjoint scalar is a three-component isospin vector. For grand spin J=L+T, T=1, define C=J(J+1) and, for J>=1,

\[
R=nY_{JM},\qquad E=\nabla_S Y_{JM}/\sqrt C,\qquad
M_{\rm harm}=n\times\nabla_S Y_{JM}/\sqrt C.
\]

The harmonics are angular-orthonormal; c=(u_R R+u_E E+u_M M_harm)/t has reduced norm integral |u|²dt. The subscript on M_harm distinguishes a harmonic from the ghost operator M. In particular, these harmonics do not carry a spatial fluctuation-vector index.

The original Cartesian derivative gives

\[
D_i c=\partial_i c+\frac{1-K}{t}[n c_i-e_i(n\cdot c)].
\]

The angular derivative of R has tangent component K P_iY and normal component n grad_iY. The derivative of E or M_harm has the ordinary intrinsic tangent derivative and normal component -K n E_i or -K n(M_harm)_i. Integration uses div E=-sqrt(C)Y, div M_harm=0 and the unit-sphere identity integral |nabla^S E|²=integral |nabla^S M_harm|²=C-1. The resulting actual reduced operator is -d²/dt²+U with

\[
\boxed{U_{RE}=
\begin{pmatrix}
(C+2K^2)/t^2&-2\sqrt C K/t^2\\
-2\sqrt C K/t^2&h^2+(C-1+K^2)/t^2
\end{pmatrix},\qquad
U_M=h^2+(C-1+K^2)/t^2.}
\tag{A2}
\]

There is no R-M_harm or E-M_harm mixing. At J=0 only R exists and U=2K²/t², reproducing the frozen spherical ghost. The independent code applies the original Cartesian covariant Laplacian to all three J=1 harmonics, without assuming (A2), and verifies (A2) exactly on n·n=1.

Since K=1+O(t²),h=O(t), the RE centrifugal matrix has eigenvalues J(J-1),(J+1)(J+2), with eigenvectors

\[
e_-=(\sqrt J,\sqrt{J+1})/\sqrt{2J+1},\qquad
e_+=(-\sqrt{J+1},\sqrt J)/\sqrt{2J+1}.
\]

Thus the smooth branches are t^J e_-, t^(J+2)e_+, t^(J+1)M_harm, respectively l=J-1,J+1,J. For J=1 these are l=0,2,1. The l=0 reduced irregular constant is square-integrable but gives a Cartesian 1/t singularity; smooth origin data select the reduced Dirichlet/Friedrichs branch u~t. The irregular branches of the other channels are likewise excluded. Framing requires every u(x)=0. These conditions define the self-adjoint ghost domain. Its kernel is empty: zero quadratic form in (A1) gives D_i c=0, whose norm is constant, and c=0 on the wall then gives c=0 everywhere.

## Exact complete J=1 ghost determinant

For C=2 the magnetic expression is L_A=-d²/dt²+h²+(1+K²)/t². Its regular zero-energy solution is

\[
u_M=3(\sinh t/t-t/\sinh t),\qquad u_M/t^2\longrightarrow1.
\]

The same differential expression previously appeared with **Robin** wall data in the spherical phase pairing. Here its actual ghost wall data are Dirichlet. Its determinant to the unbroken reference u_ref=t² is therefore

\[
\boxed{D_M(x)=\frac3{x^2}(\sinh x/x-x/\sinh x).}
\tag{A3}
\]

For the coupled RE block, use the order (E,R) and write

\[
Q=\frac d{dt}+W,\quad W=
\begin{pmatrix}h&\sqrt2K/t\\\sqrt2K/t&-1/t\end{pmatrix}.
\]

Direct substitution of K'=-Kh,h'=(1-K²)/t² gives U_ER=W²+W'. Thus the J=1 ghost expression is QQ^dagger, while Q^dagger Q is the frozen real spherical gauge/A4 differential expression. This identity is used to construct solutions, not to identify finite-wall spectra.

Let

\[
y_0=(tK',t(h+th')/\sqrt2)^T,\quad
e_0=(\sqrt2,1)^T/\sqrt3,\quad e_2=(-1,\sqrt2)^T/\sqrt3.
\]

Then Qy0=0 and y0~t²e2/sqrt3. With J_mat=((0,-1),(1,0)) and f=sinh(t)/t²,

\[
z_0=-\sqrt3 f J_{\rm mat}y_0\sim te_0,\qquad Q^\dagger z_0=0.
\]

If z2~t³e2 is the other regular second-order solution, Q^dagger z2=-5sqrt3 y0. Indeed its leading coefficient is (-3-2)t²e2, and the first-order Q kernel has only one regular branch. A regular t³e2 admixture in z0 is immaterial to its determinant with z2. For d=det[z0,z2],

\[
(d/f)'=15|y_0|^2,\qquad
\det Z(x)=\frac{15\sinh x}{x^2}\int_0^x|y_0(t)|^2dt.
\]

The integral is elementary:

\[
|y_0|^2=\frac{t^2}{2}+\frac12\frac d{dt}
[t^3\operatorname{csch}^2t(1-t\coth t)],
\]
\[
\int_0^x|y_0|^2dt=\frac{x^3}{6}
[1+3\operatorname{csch}^2x(1-x\coth x)].
\]

The unbroken regular reference matrix [te0,t³e2] has determinant x^4. Consequently

\[
\boxed{D_{RE}(x)=\frac{5\sinh x}{2x^3}
[1+3\operatorname{csch}^2x(1-x\coth x)].}
\tag{A4}
\]

Both (A3) and (A4) approach one as x tends to zero and are strictly positive. Positivity of (A4)'s apparently cancelling bracket follows from the positive integral, so no sign or zero-mode convention is hidden in it.

The regular-interval determinant relation is checked against [Kirsten–McKane, math-ph/0403050v1, Section 4, equations (40)–(42) and the following determinant ratio, pages 12–13](https://arxiv.org/abs/math-ph/0403050v1). It requires Hermitian potentials, equal leading coefficient and matched self-adjoint boundary matrices. Apply it first on [epsilon,x]. The common l=0/l=2 centrifugal matrix gives cutoff fundamental normalization factors 1 and (5epsilon²)^(-1) in its two eigenchannels, to leading order. Their product cancels against the reference before epsilon tends to zero, yielding detZ/x^4. The magnetic common l=1 factor cancels similarly. This explicit endpoint limit, rather than the regular theorem by itself, supplies the singular-origin extension.

The full complex ghost contribution at J=1 has multiplicity 2J+1=3:

\[
\boxed{\frac{\det M_{J=1}}{\det M^{(0)}_{J=1}}
=[D_{RE}(x)D_M(x)]^3,}
\tag{A5}
\]
\[
D_{RE}D_M=\frac{15\sinh^2x}{2x^6}
[1+3\operatorname{csch}^2x(1-x\coth x)]
[1-x^2\operatorname{csch}^2x].
\]

Therefore

\[
\boxed{\log\frac{\det M_{J=1}}{\det M^{(0)}_{J=1}}
=6x-18\log x+3\log(15/8)+O(x^2e^{-2x}).}
\tag{A6}
\]

There is no algebraic inverse-radius term at any order in this exact static J=1 ghost comparison. A complex ghost contributes plus this logarithm to logZ. It does not determine the residual of the full J=1 gauge Gaussian, and cannot by itself confirm or cancel the spherical full-sector result.

## Finite-wall longitudinal pairing and precisely open vector sector

The static gauge fluctuation is a_mu=(a_i,phi), with D4=adPhi. The Yang–Mills action plus background Feynman gauge gives

\[
H_{\mu\nu}=-D_\lambda D_\lambda\delta_{\mu\nu}-2\operatorname{ad}F_{\mu\nu},\quad
Pc=(D_i c,[\Phi,c]),\quad P^\dagger a=-G(a),
\]
\[
G(a)=D_i a_i+[\Phi,\phi],\qquad
P^\dagger P=M,\qquad HP=PM.
\tag{A7}
\]

The last identity follows by commuting the covariant derivatives; the remaining term is the background Yang–Mills equation DnuF_mu_nu=0. It is not a guessed copy of the scalar Hessian.

The actual relative mixed vector quadratic-form domain fixes the tangential connection a_tan=0 and phi=0 at the wall; a_r is free. The natural operator-domain condition is G(a)=0 at the wall. Since the tangential traces and their tangential derivatives vanish there, and Ar=0 in the background, this becomes

\[
a_{\rm tan}(x)=0,\quad\phi(x)=0,\quad
(\partial_t+2/x)a_r(x)=0.
\tag{A8}
\]

For canonical reduced normal amplitudes zeta=t a_r the last equation is zeta'+zeta/x=0. This is a self-adjoint relative mixed condition, not all-component Dirichlet.

For every Dirichlet ghost eigenfunction Mc=lambda c, the field Pc has zero tangential and phi traces. Moreover G(Pc)=-lambda c=0 at the wall, so Pc is an actual vector eigenfunction in (A8). Integration by parts with c=0 gives ||Pc||²=lambda||c||². The isometry c -> Pc/sqrt(lambda) pairs the positive ghost spectrum exactly with the closed longitudinal range of P. It retains every positive small eigenvalue; no infinite-volume collective-coordinate rule is used. The orthogonal complementary vector subspace is exactly kerP^dagger=kerG in (A8). On smooth domain fields its L² projection is a_T=a-P M_D^(-1)P^dagger a, extended by closure. Thus the total Gaussian has an explicit longitudinal factor (detM_D)^(-1/2); with the complex ghost, the net factor is (detM_D)^(1/2) times the still uncomputed transverse-vector determinant to power -1/2.

At J=1, coupling the spatial-vector spin S=1 and adjoint T=1 to k=0,1,2 gives seven spatial channels:

- k=0: l=1;
- k=1: l=0,1,2;
- k=2: l=1,2,3.

The A4 scalar has l=0,1,2, giving ten radial vector channels per magnetic quantum number. Smooth reduced origin powers are t^(l+1) in these tensor harmonics; smooth Cartesian fields supply the full regular expansions. The normal spatial trace has the three R/E/M ghost angular channels. Its orthogonal spatial tangent complement has four channels. Consequently (A8) imposes **seven Dirichlet plus three Robin radial conditions**: four spatial tangent plus three A4 Dirichlet, and three normal Robin. Longitudinal images of the three ghost channels are paired. The precisely remaining physical calculation is the restriction of H to the **seven radial transverse combinations satisfying G=0**, with these mixed data and the stated smooth origin. These are constrained combinations of the ten tensor amplitudes, not seven separately invariant scalar channels.

There is an additional explicit obstruction to borrowing the spherical factorization as a ghost cancellation. Q maps the frozen real block's Dirichlet wall data y(x)=0 to **matrix Robin** ghost-expression data

\[
Q^\dagger z(x)=0\quad\Longleftrightarrow\quad z'(x)=W(x)z(x).
\tag{A9}
\]

Its inverse at positive eigenvalue is y=Q^dagger z/lambda and respects the regular origins. This Robin realization of QQ^dagger also has the exact regular kernel z0 above, at every finite x. The actual framed Dirichlet RE ghost has no kernel. Thus the two domains have different spectra even though the bulk differential expressions coincide. The formal Q relation alone cannot cancel the exact determinants (A3)–(A5) against the real spherical vector block.

## Computation and provenance

The independent raw action/matrix/determinant derivation was saved before reading any coordinator angular notes. No such notes were needed. The current code is check_angular_v2.py, contract COMPUTATION_CONTRACT_v2.json, run runs/angular-003/manifest.json. It checks all three original Cartesian J=1 actions, the symbolic general-J centrifugal eigenvectors, the BPS matrix factorization, the regular kernel, the integral identity and the magnetic solution. Independently it builds origin Frobenius data from the original second-order matrix and integrates that matrix with DOP853 at x=2,5,10,20 with epsilon=10^(-3),5*10^(-4). Four separate 70-digit quadratures check the positive integral without fitting any coefficient. The declared relative ODE tolerance is 2*10^(-7); floating results are not certified intervals.

Run angular-001 could not launch because the platform rejected its requested POSIX pre-execution resource setup. It is preserved as launch-failed, not mathematical evidence. Run angular-002 completed; subsequent audit found that its unused highest Frobenius coefficient omitted the potential's t^8 term. The code and contract were superseded immutably; angular-003 restores that term for both matrix and magnetic starts. The effect at the stated starts is far below double precision, but only angular-003 is current. Run angular-003 completed in 4.10 seconds of child runtime; the largest relative ODE discrepancy is 5.24*10^(-10), below the declared tolerance. Its v2 manifest validates against the current input bytes. Wall time, software, finite results and all input/output hashes are in the manifest; INPUTS.json and ARTIFACTS.sha256 provide the local receipt.

The first remaining physical gap in this lane is the seven-combination transverse J=1 vector determinant under (A8), followed by the higher-J/Fourier sum and common UV subtraction. Even their completion would still require a physical same-holonomy vacuum matching and a justified bridge from fixed-small-circle pure SU2 to the QCD metric stress and matched proton response. Physical A_rho, R(alpha), and an alpha root remain uncalculated.

Final mathematical proofreading self-review covered this new report only: notation, determinant exponents, angular degeneracy, origin powers, mixed wall conditions and finite versus infinite-radius limits were checked. Routine notation clarifications only; no unresolved typographical issue or mathematical-token correction remained. This self-review is not an independent proof audit.
