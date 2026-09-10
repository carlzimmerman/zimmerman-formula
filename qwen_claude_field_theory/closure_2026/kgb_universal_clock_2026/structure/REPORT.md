# Common-mass structure: exact reductions and a bounded next-preservation check

Base: `1e8f58095a44e27b9cff0a467737e30eef414601`. This independent package concerns the same action

\[
\sqrt{-g}\{F(X)R+3F_X^2(\nabla X)^2/(2F)+P(X)-G(X)\Box\phi\},
\qquad X=-\nabla\phi\cdot\nabla\phi/2,
\]

with signature \((-+++)\), one explicit clock, the stationary spherical ansatz, zero **total** radial current, and the imposed target \(B=1+2rg\). No particle dark matter is introduced. The finite calculations below neither construct a universal action on an interval nor prove a universal obstruction.

## 1. Closed static inverse

Write \(f=F_X\), \(j=F_{XX}\), \(z=X'\), \(w=fz=F'\), \(U=p^2/B\), \(p=+\sqrt{BU}\), \(Q=2X+U\), \(a=g+2/r\), and \(b=B'/(2B)\). The regular chart assumes finite coefficients, \(F,X,U,B,r>0\), \(f,w\ne0\), and \(r_y\ne0\). The Einstein-frame interpretation additionally needs \(2(F-Xf)\ne0\); this is not a factor of the static matrix determinant.

With the target geometric density \(\rho\) and angular pressure \(p_t\), define

\[
\begin{aligned}
P&=(2wa+3w^2/(2F))/B,\\
L&=2F\rho+2w(g+b)/B+3w^2/(FB),\\
S&=2Fa\rho+4w(rg-1)/(r^2B),\\
\gamma&=G_X/f=prS/(2Qw),\\
W&=dw/dr=\tfrac B2(L-XrS/Q),\\
H&=\{(2/r+w/F)U-(2g+w/F)X\}/p,\\
\kappa&=P_X/f=2P/F+H\gamma.
\end{aligned}
\]

These expressions are independent of \(f,j\) at fixed \((X,F,y,U,w)\). Recover \(P_X=f\kappa\), \(G_X=f\gamma\), \(z=w/f\), and \(z'=W/f-jz^2/f\). Here \(W\) means \(dw/dr\), not the differently named quantity in the older unextended inverse.

For an exact check against the original three equations, let

\[
R_w=\partial_rP+g'\partial_gP+w\partial_FP,\quad
A_w=\rho-2p_t+\frac{3w^2}{2F^2B}-\frac{3(a-b)w}{FB},\quad
C_J=\frac{2(U-Xrg)}{pr}.
\]

The system and computed determinant are

\[
\begin{pmatrix}P_w&-w&0\\-3/(FB)&1&-C_J\\2/B&0&2Xw/p\end{pmatrix}
\begin{pmatrix}W\\\kappa\\\gamma\end{pmatrix}
=\begin{pmatrix}-R_w\\-A_w\\L\end{pmatrix},
\qquad \det M=\frac{4wQ}{Bpr}.
\]

SymPy substitutes the closed solution into all three original rows and checks \(S=A_ww+R_w+aL\), including the cancellation of every quadratic or mixed \((F,w)\) term in \(S\). Three fixed real cases also compare this helper and its complex-step action curvatures against the committed inverse; these are bounded cross-checks, not a stability test.

## 2. Shared lower jets and actual X-flow

At common \((X,F,f)\), the lower action requirements are \(\Delta P=\Delta\kappa=\Delta\gamma=0\). If the common \(\gamma\ne0\), these are equivalent to common \((P,H,\gamma)\). Pressure determines a quadratic in \(w\), independent of \(f\). For \(s_i=\sqrt{U_i}>0\), common signed \(H\) requires

\[
(2/r_i+w_i/F)s_i^2-H\sqrt{B_i}s_i-(2g_i+w_i/F)X=0.
\]

Both pressure branches and all admissible positive roots matter; squaring the signed equation can introduce false matches. Useful chart derivatives are

\[
H_U=\frac{(2/r+w/F)U+(2g+w/F)X}{2pU},\qquad
\gamma_U=\frac{\gamma(2X-U)}{2UQ}.
\]

A fold of this parametrization is not itself a proof of incompatible masses.

For any finite collection of mass parameters \(\epsilon_i\), use common \(F,f\) and individual \(y_i,U_i,w_i\). The actual flow, without projecting constraints, is

\[
F_X=f,\quad f_X=j,\quad
(y_i)_X=\frac f{r_{y,i}w_i},\quad
(U_i)_X=-2-\frac{2fg_iQ_i}{w_i},\quad
(w_i)_X=\frac{fW_i}{w_i}.
\]

Define operators on the \(f,j\)-independent state functions:

\[
L_0=\partial_X-2\sum_i\partial_{U_i},\qquad
L_1=\partial_F+\sum_i\left(\frac{\partial_{y_i}}{r_{y,i}w_i}
-\frac{2g_iQ_i}{w_i}\partial_{U_i}+\frac{W_i}{w_i}\partial_{w_i}\right).
\]

The full derivative is \(D_X=L_0+fL_1+j\partial_f+\ell\partial_j\), where \(\ell=F_{XXX}\). **Do not commute \(L_0,L_1\).** Exact identities are

\[
L_0P=0,\quad L_1P=\kappa,\quad
L_0\gamma=-\gamma/U,\quad
L_0\kappa=-2\gamma(g+2/r+3w/(2F))/p.
\]

Hence \(D_X\Delta P=f\Delta\kappa\): pressure preservation is automatic only after imposing common \(P_X\).

## 3. First preservation, next tangency, and the one shared control

For either \(q=\kappa\) or \(q=\gamma\), set

\[
A_q=L_0\Delta q,\quad B_q=L_1\Delta q,\quad E_q=A_q+fB_q.
\]

Then \(\Delta P_{XX}=j\Delta\kappa+fE_\kappa\) and \(\Delta G_{XX}=j\Delta\gamma+fE_\gamma\). On the lower matching surface, common second action jets require \(E_\kappa=E_\gamma=0\), independently of \(j\). Thus an arbitrary nonaffine \(F_{XX}\) cannot repair failed first preservation.

If one \(B\) is nonzero, first preservation determines a unique shared \(f=-A/B\) and requires the remaining minors to vanish. The resulting \(f\) must still obey the physical chart assumptions. If both \(B\)'s vanish, both \(A\)'s must vanish; otherwise there is no solution.

Define, retaining both operator orders,

\[
N_q=L_0A_q+f(L_1A_q+L_0B_q)+f^2L_1B_q.
\]

Then \(D_XE_q=N_q+jB_q\), and the unreduced third action-jet difference is

\[
\Delta P_{XXX}=\ell\Delta\kappa+2jE_\kappa+f(N_\kappa+jB_\kappa)
\]

(and analogously for \(G\)). Only on lower matching and first preservation do the \(\ell\) terms cancel. The next equations are therefore

\[
N_\kappa+jB_\kappa=0,\qquad N_\gamma+jB_\gamma=0.
\]

With a nonzero \(B\) pivot, a shared \(j\) exists iff

\[
N_\kappa B_\gamma-N_\gamma B_\kappa=0;
\]

it is then unique. If both \(B\)'s vanish, both \(N\)'s must vanish. Any resulting shared \(j\) must separately lie in every mass's admissible health interval.

This is also the tangency condition for \(T=A_\kappa B_\gamma-A_\gamma B_\kappa\):

\[
D_XT=N_\kappa B_\gamma-N_\gamma B_\kappa
+E_\kappa(L_0+fL_1)B_\gamma-E_\gamma(L_0+fL_1)B_\kappa.
\]

In particular \(D_XT\) is independent of \(j\). At the following order \(\ell\) generally reappears; no all-orders cancellation is claimed. For more masses, stack both differences against one reference mass and apply the same indexed scalar-control/minor criterion. No numerical rank is assigned, and this is not a Dirac degree-of-freedom count. Pointwise finite jets, even through this order, do not establish an invariant constraint manifold or common functions on an interval.

## 4. Lower matching does not generically force equal mass labels

There is an exact local non-rigidity route, not merely a numerical fit. For the exponential target let

\[
\mu=1-e^{-y},\quad \lambda=\mu+ye^{-y},\quad
\mathcal A=\sqrt{y\mu},\quad r=\epsilon/\mathcal A,\quad
\mathcal D=4Fy^2e^{-y}/\lambda,
\]

and put \(U=\epsilon u\). The symbols \(\mathcal A,\mathcal D\) here are not the metric lapse or conformal determinant. The scaled lower map has the smooth extension

\[
(\epsilon P,\sqrt\epsilon H,\sqrt\epsilon\gamma)
\longrightarrow
\left(4\mathcal A w,
\frac{2\mathcal A u-X(2y+w/F)}{\sqrt u},
\frac{\mathcal A\sqrt u}{X}(\mathcal D/w-1)\right)
\quad(\epsilon\downarrow0).
\]

At \(y=1,w=-F,u=X/\mathcal A\), put \(e=e^{-1}\). The exact Jacobian determinant of this limiting map with respect to \((y,w,u)\) is

\[
-\frac{2\mathcal A}{X}(12e^3-32e^2+28e+3)<0,
\]

because the polynomial equals \(3+4e\{2+2(1-e)+3(1-e)^2\}>0\). SymPy checks the smooth extension and determinant; Lean proves the conditional real-algebra sign. Continuity gives a nonzero finite-\(\epsilon\) determinant for sufficiently small positive \(\epsilon\). At each such \(\epsilon\), the row scalings and \(U=\epsilon u\) change are invertible, so the original lower map also has invertible partial derivative.

The parameter implicit-function theorem then gives nearby distinct positive mass labels with the same lower \((P,H,\gamma)\), holding \(X,F,f\) fixed. One regular witness choice is \(f=F/(2X)\): \(2(F-Xf)=F>0\), \(z=-2X\), and \(1+rw/(2F)>0\) for sufficiently small \(\epsilon\). Also \(\gamma\ne0\) near this limiting point. There is no physical \(\epsilon=0\) solution claim, quantitative mass-ratio bound, second-jet preservation, health certificate, or global common action in this argument. It excludes a *generic lower-jet mass-label rigidity* argument, not every branch-specific obstruction.

The IFT application is a prose argument using the authenticated local Mathlib theorem `HasStrictFDerivAt.eventually_apply_implicitFunctionOfProdDomain` in `Mathlib/Analysis/Calculus/ImplicitFunction/ProdDomain.lean`, at commit `85e3a25e006c35636f0e53b0e9296caca2685bc0`. Its hypotheses are strict differentiability and an invertible partial derivative in the three dependent variables. The finite-positive-\(\epsilon\) map is analytic on the stated chart. The full analytic-to-IFT application is **not** formalized by the conditional Lean algebra file; no novelty search is claimed.

## 5. Independent bounded next-preservation failure

`check_next_preservation.py` refines exactly one supplied seed, without importing the parent's matching solver. It differentiates the actual closed X-flow with nested `mpmath.diff`, recomputing the inner vector field at perturbed states. At \((\epsilon_1,\epsilon_2,X,F,y_1,U_1)=(10^{-6},2\cdot10^{-6},0.5,0.525,0.1,3\cdot10^{-8})\), the refined values begin

\[
(w_1,w_2,y_2,U_2/\epsilon_2,f)
=(-20.8245196960961,-27.4430902101842,0.153793693461797,
0.0260058245999448,259.685368559567).
\]

The five raw lower/first-preservation residuals are below \(4.4\cdot10^{-48}\) at 60 digits and \(1.8\cdot10^{-67}\) at 80 digits. Both precision runs give

\[
\frac{N_\kappa B_\gamma-N_\gamma B_\kappa}{\|N\|\|B\|}
\simeq-0.000538829413840944,
\]

with independently demanded controls \(j_\kappa\simeq-1.45833181066535\cdot10^9\) and \(j_\gamma\simeq-1.51150519937726\cdot10^9\). The unnormalized determinant is approximately \(-1.22420304825222\cdot10^{22}\). Thus this refined seed has a robust numerical next-preservation mismatch. This is finite arbitrary-precision evidence, not an interval-arithmetic proof, exhaustive branch scan, or universal no-go. No scalar health claim is made for this seed.

## 6. Evidence and remaining gates

The package contains eleven exact/bounded Python tests, eight conditional Lean theorems, and the two precision evaluations of one seed. `RUN.md` identifies the frozen run, versions and commands; the run manifest pins the source inputs. The Lean statements certify generic scalar-control algebra, determinant tangency on stated hypotheses, a conditional cancellation, signed lower matching, and a polynomial sign. They do not certify the covariant variation, physical correspondence, full IFT application, or numerical output.

The action still needs an invariant common-mass trajectory and common \(F(X),P(X),G(X)\) on overlapping intervals, healthy perturbations there, regular interior/source matching and measured gravitational normalization, and galaxy/lensing/time/cosmological tests. The imposed \(\epsilon\) labels are not independently calibrated physical masses. A target global acceleration constant is not inferred from these vacuum jets. No CMB certificate, measured Newton coupling, PPN values, or full Hamiltonian/Dirac result follows here.
