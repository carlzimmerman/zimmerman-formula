# D4/D6: global vacuum-regulated activation and its actual ADM quadratic cost

2026-09-26; starting commit `03524d209b7ca0c3900f47ccf5dfe42f9187d7c3`, shared dirty checkout. This route modifies only its new `environment_gate/` artifacts. It is a constructive continuation of the prior restricted gate lemma, with an explicit changed route after the first scalar-gradient obstruction.

**Result.** A globally smooth activation with exact zero/one plateaus exists using only the already available positive vacuum curvature scale. Its shear-completed ADM variation preserves the tensor speed on isotropic backgrounds but changes tensor normalization and scalar constraints. The uncorrected activation has a wrong-sign scalar \(k^4\) term on part of its transition. An explicit concave curvature addition supplies a nonempty uniform coefficient window that fixes that sign in the declared isotropic principal sector. Its positive \(k^4\) dispersion then fails an all-frequency metric-cone requirement. This is a concrete finite-band construction and an exact remaining causal-completion obligation, not a full action/observational closure.

The reproducible run verifies 48 exact identity/control/bound checks. Its symbolic/inequality evidence is in `check_gate_adm.py`, `contract.json`, and `run_verified/{results.json,manifest.json}`. The manuscript below supplies the analytic reduction from the global functions to the finite rational inequalities. Informational midpoint values use 35-digit evaluation; none of the uniform sign bounds depends on those floating values. An initial syntax-only failed run remains in `run/`; it produced no scientific result and was corrected before `run_verified`.

## 1. A global gate with explicit regulator and exact plateaus

Use \(c=1\), \(\Lambda>0\), \(K\in\mathbb R\) the trace of extrinsic curvature, and \(R=R^{(3)}+\sigma_{ij}\sigma^{ij}\in\mathbb R\). \(\Lambda\) and \(R\) have dimension length\(^{-2}\); \(K\) has dimension length\(^{-1}\). Declare **dimensionless** \(\epsilon>0\) and \(x_c>0\), without claiming either is derived. Put

\[
D=K^4+\epsilon\Lambda^2>0,\qquad
t=\frac{27\Lambda R}{8x_cD},\qquad f=W(t),
\]

where

\[
g(t)=\begin{cases}e^{-1/t}&t>0,\\0&t\le0,\end{cases}
\quad W(t)=\frac{g(t)}{g(t)+g(1-t)}.
\]

The denominator of \(W\) is positive at every real \(t\). The standard direct differentiation argument gives \(g^{(n)}(t)=e^{-1/t}\) times a polynomial in \(1/t\) for \(t>0\); every such derivative tends to zero at the origin. Thus \(W\), and hence \(f(R,K)\), is \(C^\infty\) on the entire real \((R,K)\) plane for fixed positive \(\Lambda,\epsilon,x_c\). It obeys \(0\le f\le1\), is exactly zero for \(R\le0\), and exactly one when \(27\Lambda R/4\ge2x_cD\). Consequently \(m^2(1-f)\ge0\): the negative-curvature pole and negative screening mass of the previous rational gate are absent. At the joint zero, \(f(0,0)=0\) with all derivatives zero. There is no discontinuous clipping.

At half activation \(t=1/2\), \(W=1/2,W'=2,W''=0\). Writing \(a=27\Lambda/4\),

\[
R_{1/2}=\frac{x_c(K^4+\epsilon\Lambda^2)}a,
\quad f_R=\frac a{x_cD},\quad
f_K=-\frac{4K^3}D,\quad
f_{KK}=\frac{4K^2(5K^4-3\epsilon\Lambda^2)}{D^2},
\quad f_{RK}=-\frac{4aK^3}{x_cD^2},\quad f_{RR}=0.
\]

**Exact cost.** Relative to the unregularized half-threshold, the curvature threshold increases by \(1+\epsilon\Lambda^2/K^4\). Requiring fractional shift at most \(\delta\) at a specified nonzero \(K\) requires \(\epsilon\le\delta K^4/\Lambda^2\). At \(K=0\), a finite curvature threshold \(R_{1/2}=4x_c\epsilon\Lambda/27\) replaces the former always-on positive-curvature limit. Taking \(\epsilon\to0\) removes this protection; no uniform joint-zero limit is claimed. The off-to-on transition occupies a finite interval, here \(0<t<1\), rather than a hard step. Both plateaus are exact. No nonconstant analytic gate can have an open exact plateau and remain analytic across the transition, so smooth nonanalytic endpoints are deliberate. Narrowing the transition rescales first and second derivatives inversely with its width and its width squared; the variational cost does not disappear with a hard-switch approximation.

This is the unnormalized \(p=1\) variable \(\widetilde x\Omega_\Lambda\). Matching L359's normalized threshold requires \(x_c=\Omega_{\Lambda0}x_{c0}\); the numerical witness \(x_c=1\) below is a declared test choice, not the previously fitted empirical cell.

## 2. Concrete ADM sector, including shear, lapse and shift

To make the calculation fully specified, use the explicit preferred-foliation action sector

\[
S=\int dt\,d^3x\,N\sqrt\gamma\left\{
\frac{M^2}{2}\left[R^{(3)}+\sigma^2-(\tfrac23+c_2)K^2+
\alpha a_i a^i-2\Lambda\right]+Bf(R,K)+C(R)\right\},
\quad a_i=D_i\ln N.
\]

Here \(M^2=(8\pi G)^{-1}>0\), and for the explicit test action \(B=bM^2\Lambda\) is a constant with declared dimensionless \(b\ge0\). Initially set \(C=0\). This realizes exactly the geometric \(B\delta f+B\delta^2f\) sector of the promoted L361 action at a frozen auxiliary background. **It is not an assertion that L361 dynamically makes its own \(B\) constant.** For actual L361, the quadratic terms also include \(\delta B(f_R\delta R+f_K\delta K)\), the original \(f\delta^2B\), and measure/contraction terms. The lapse expansion in the new check explicitly verifies the \(\delta B f_K\delta K+n\delta Bf\) contributions; they cannot be dropped in a full L361 constraint analysis.

The calculations below use an isotropic, frozen-coefficient background, retain the local quadratic principal operators, and keep the lapse and scalar shift until their algebraic Fourier constraints are reduced. Curvature-scale and time-varying-background lower-order terms, anisotropic background shear, and other field fluctuations are not included. A source capable of supporting the chosen background and its own perturbations is not constructed here. Neither the algebraic reductions nor their nonsingular Hessian is a nonlinear degree-of-freedom count.

### Tensor sector: the shear term matters at quadratic order

For one tensor polarization take \(\gamma_{ij}=a^2\operatorname{diag}(e^h,e^{-h},1)\), unit lapse and zero shift. Its trace is \(K=3H\) exactly, while

\[
\sigma^2=\tfrac12\dot h^2,\qquad
R^{(3)}_{\rm principal}=-\tfrac1{2a^2}(\partial_z h)^2.
\]

The spatial Ricci scalar was independently computed from the Christoffel symbols in the script, rather than inserted as a desired result. For an isotropic background the first-order TT variations of \(R,K\) vanish, but these second-order terms do not. For arbitrary TT polarization,

\[
\mathcal L^{(2)}_{TT}=\frac{a^3Z}{8}
\left[\dot h_{ij}\dot h_{ij}-a^{-2}\partial_lh_{ij}\partial_lh_{ij}\right],
\qquad Z=M^2+2(Bf_R+C_R).
\]

Thus the local principal tensor speed is exactly one **if \(Z>0\)**. Its normalization changes. Omitting the shear square from the gate while retaining it in \(C\) instead gives
\(c_T^2=[M^2+2(Bf_R+C_R)]/[M^2+2C_R]\); a negative-control witness gives 3 rather than 1. This calculation includes \(B\delta^2f\); checking only \(\delta K_{TT}=0\) would miss it. It does not establish tensor propagation on general anisotropic/inhomogeneous backgrounds or after unspecified auxiliary mixing.

### Scalar sector: actual trace Hessian and constraints

Use lapse perturbation \(n\), conformal perturbation \(\zeta\), and scalar shift divergence \(s\). With local scale factor absorbed into physical wavenumber, define

\[
\kappa=3\dot\zeta-s-K_0n,\qquad r=4k^2\zeta,
\]

the principal first-order trace and intrinsic-curvature variations. The trace-lapse calculation comes directly from \(K=(K_0+3\dot\zeta)/(1+n)\): the \(f_K\) second-order terms cancel against the lapse measure, leaving \(Bf_{KK}(3\dot\zeta-K_0n)^2/2\), before the shift is restored. Define

\[
\mathcal C=-M^2(\tfrac23+c_2)+Bf_{KK},\quad
\mathcal D=Bf_{RK},\quad \mathcal E=Bf_{RR}+C_{RR}.
\]

The declared principal quadratic density is

\[
\mathcal L^{(2)}_s=
\frac Z3s^2+\frac{\mathcal C}2\kappa^2+\mathcal D r\kappa+
\frac{\mathcal E}2r^2+Zk^2\zeta^2+2Zk^2n\zeta+
\frac{\alpha M^2}2k^2n^2.
\]

The \(Z\) spatial terms follow by expanding \(N\sqrt\gamma R^{(3)}\) for \(\gamma=e^{2\zeta}\delta\) and integrating spatial derivatives by parts. The term \(\mathcal D r\kappa\), the \(\mathcal E r^2/2\), and the changes to both \(Z\) and \(\mathcal C\) are induced by the varied gate; a prescribed mask omits them.

Put

\[
\Delta=\mathcal C+2Z/3,\quad
F=\frac{(2Z/3)\mathcal C}{\Delta},\quad
J=\frac{(2Z/3)\mathcal D}{\Delta},\quad
E_* =\mathcal E-\frac{\mathcal D^2}{\Delta}.
\]

For \(\Delta\ne0\), eliminating the shift gives \(F(3\dot\zeta-K_0n)^2/2+Jr(3\dot\zeta-K_0n)+E_*r^2/2\), in addition to the last three spatial/lapse terms. Eliminating the lapse, whose denominator is \(N_*=FK_0^2+\alpha M^2k^2\), gives

\[
\mathcal L^{(2)}_{\rm red}=\tfrac12 A_\zeta\dot\zeta^2+V_k\zeta^2
+(\hbox{constant-coefficient total time derivative}),
\]
\[
A_\zeta=\frac{9F\alpha M^2k^2}{N_*},\qquad
V_k=Zk^2+8E_*k^4-
\frac{(4JK_0-2Z)^2k^4}{2N_*}.
\]

These reductions are checked by solving the two algebraic Euler equations and substituting the solutions into the quadratic density. The branch \(Z>0,\Delta<0,\alpha>0\) has \(\mathcal C=\Delta-2Z/3<0\), hence \(F>0\) and \(A_\zeta>0\) for \(k\ne0\). This is the physical scalar kinetic sign in this declared reduced principal sector; it is stronger than an unreduced trace-Hessian sign but narrower than a full theory health proof.

## 3. First obstruction and an explicit changed route

With \(C=0\), \(B>0\), and \(W''>0\) on a lower-transition patch,
\(\mathcal E=B W'' t_R^2>0\). On the kinetic-positive branch \(\Delta<0\), one therefore has \(E_*>0\). The large-\(k\) potential has the wrong sign: \(V_k\sim8E_*k^4>0\), giving \(\omega^2<0\). Even at the midpoint, \(W''=0\), \(K_0\ne0\) generally gives \(\mathcal D\ne0\) and \(E_*=-\mathcal D^2/\Delta>0\). The script supplies an exact positive rational midpoint witness. **This refutes the uncorrected constant-B geometric sector, not every L361 completion:** its remaining auxiliaries can alter the reduced operator.

Continue with a new explicit shear-completed curvature operator,

\[
C(R)=-\eta M^2\left[R\arctan(R/\Lambda)
-\frac\Lambda2\ln(1+R^2/\Lambda^2)\right],\qquad\eta>0.
\]
\[
C_R=-\eta M^2\arctan(R/\Lambda),\qquad
C_{RR}=-\frac{\eta M^2\Lambda}{R^2+\Lambda^2}<0.
\]

It has bounded slope, is smooth on all real \(R\), uses no new dimensional scale, vanishes with its first derivative at \(R=0\), and retains the tensor kinetic/gradient equality because its argument is the same shear-completed \(R\). The dimensionless coefficient \(\eta\) is a new declared choice. It changes the gravitational action and is not an observationally free adjustment.

### Analytic global coefficient bounds, not an extrapolated parameter scan

On the transition, \(0<t<1\), the elementary bounds \(|W'|\le8\), \(|W''|\le160\) suffice. To check them, use symmetry about \(t=1/2\); for \(t\le1/2\), set \(y=1/t\ge2\). With logit \(\ell=-1/t+1/(1-t)\), one has \(e^\ell\le e^{2-y}\), \(\ell'\le y^2+4\), and \(|\ell''|\le2y^3+16\). Maximizing \(y^ne^{-y}\) gives the first bound 8 and the second bound at most \(256/e^2+54/e+64<160\). Outside the transition all derivatives vanish.

Writing \(C_0=1+729/(64x_c^2\epsilon^2)\), these imply

\[
\Lambda|f_R|\le\frac{27}{x_c\epsilon},\qquad
\Lambda|f_{KK}|\le\frac{528\sqrt3}{\sqrt\epsilon},
\]
\[
\Lambda(R^2+\Lambda^2)f_{RK}^2
\le\frac{84672\sqrt3 C_0}{\sqrt\epsilon},\quad
(R^2+\Lambda^2)|f_{RR}|\le160C_0,\quad
\Lambda|Kf_{RK}|\le\frac{567}{x_c\epsilon}.
\]

For example, the first mixed bound follows from
\(f_{RK}=-4K^3t_R[tW''+W']/D\),
\((R^2+\Lambda^2)t_R^2\le C_0\), and
\(\Lambda K^6/D^2\le3\sqrt3/(16\sqrt\epsilon)\).

If \(|\Delta|\ge\delta M^2\), the following sufficient inequalities give \(Z>0,\Delta\le-\delta M^2,E_*<0\):

\[
\eta\pi<1,\qquad
b\left(\frac{528\sqrt3}{\sqrt\epsilon}+\frac{36}{x_c\epsilon}\right)
+\frac{2\pi\eta}{3}<c_2-\delta,
\]
\[
160C_0b+\frac{84672\sqrt3 C_0b^2}{\delta\sqrt\epsilon}<\eta.
\]

The circular appearance of the assumed gap is removed by imposing the second inequality first; it proves that gap uniformly. A strict exact witness is

\[
\epsilon=x_c=1,\quad b=10^{-10},\quad\eta=10^{-6},\quad
c_2=1/50,\quad\delta=1/100.
\]

The script verifies the inequalities with conservative rational replacements \(\pi<4,\sqrt3<2\). They hold for **all finite real \(R,K\)** in this isotropic frozen-coefficient family. They are deliberately loose sufficient bounds, not an optimized parameter limit. They exhibit existence at weak coupling and do not say that L361's MOND-normalized \(B\) lies in the window.

Moreover \(|JK_0|/Z\le378b/(x_c\epsilon\delta)<1/4\). When \(Z>2\alpha M^2\), the scalar potential is negative for

\[
k^2>\frac{2ZFK_0^2}{(4JK_0-2Z)^2-2Z\alpha M^2},
\]

since its additional \(8E_*k^4\) term is negative. At \(K_0/\sqrt\Lambda=1,R/\Lambda=8/27\), \(\alpha=10^{-6}\), the sufficient right side is approximately \(11.4443\Lambda\); the frozen-principal interpretation separately requires wavelengths short relative to actual background variation scales.

## 4. Causal cost: the repair does not pass an all-frequency metric-cone gate

The exact dispersion of the displayed reduced principal block is the following. It is exact for that declared truncation, not the full curved-background action: for example, the omitted \(-2R_0\zeta\) piece of \(\delta R^{(3)}\) induces further curvature-dependent lower-derivative coefficients when \(f_{RR}\ne0\). This distinction limits quantitative use of the finite-band numbers, but not the nonzero \(k^4\) asymptote.

\[
\omega^2=-\frac{2ZK_0^2}{9\alpha M^2}
+c_s^2 k^2+d_4k^4,
\quad d_4=-\frac{16E_*}{9F}>0,
\]
\[
c_s^2=\frac{(4JK_0-2Z)^2-2Z\alpha M^2-16E_*FK_0^2}
{9F\alpha M^2}.
\]

The negative constant in this frozen expression is not a full cosmological Jeans/instability verdict, because background-evolution and curvature lower-order terms were not retained. The high-frequency conclusion needs no such interpretation: \(v_g\sim2\sqrt{d_4}\,k\) is unbounded. A fourth-order spatial principal equation with this dispersion has no all-frequency finite metric propagation cone. This explicit continuation therefore fails the stated no-hidden-cutoff causal closure if promoted unchanged to a fundamental all-frequency theory.

On a \(K_0=0\) positive-curvature midpoint, that constant is absent. If \(s=c_s^2\in(0,1)\), the exact massless group-speed condition is

\[
v_g^2=\frac{(s+2y)^2}{s+y}\le1,
\qquad 0\le y=d_4k^2\le
\frac{1-4s+\sqrt{1+8s}}8.
\]

Using the same weak-gate/concave parameters but explicitly choosing \(\alpha=1/10\), at \(R/\Lambda=4/27,K_0=0\), gives
\(c_s^2=0.184467763\), \(d_4\Lambda=7.60025885\times10^{-8}\), and
\(k\le1737.5097\sqrt\Lambda\). This is a **finite group-speed band of the local model**, not a finite front-speed theorem or a PPN-compatible parameter claim. The earlier \(\alpha=10^{-6}\) positive-coefficient witness instead gives \(c_s^2\simeq19417.65\) on this patch and already fails metric-cone causality before its dispersive term becomes important. Positivity and causality have been tested separately.

The next changed route must replace the scalar high-frequency response with a causal dynamical completion (and count its fields/constraints), or show that the complete L361 auxiliaries cancel the dangerous curvature coefficient. Merely declaring the displayed cutoff, or replacing the higher spatial operator by an untested rational transfer function, would not close the requested fundamental theory.

## 5. Vacuum scale and coefficient: what the regulator does not derive

The regulator \(\epsilon\Lambda^2\) is dimensionally available once a positive vacuum curvature \(\Lambda\) is present. It introduces a dimensionless crossover choice \(\epsilon\); dimensional consistency does not select it. On flat FRW \(R=0\), both this gate and \(C(R)\) vanish with the derivatives relevant to the background value, so the explicit sector does not generate its own vacuum density. The \(c_2K^2\) term still modifies the Einstein background equations and must be included in a full cosmology.

For a four-form amplitude \(q\), an explicit allowed example is

\[
P(q)=(Z_q/2+b_p\beta^2)q^2+C_v,\qquad
\varepsilon=qP_q-P=(Z_q/2+b_p\beta^2)q^2-C_v,
\quad a_0^2/G=\beta^2q^2.
\]

Adding the constant \(C_v\) leaves \(P_q\) and the charge equation unchanged but changes the gravitating energy. Restrict to positive vacuum energy \(C_v<(Z_q/2+b_p\beta^2)q^2\), so the following denominator is positive. Then

\[
\kappa^2=\frac{\beta^2q^2}{(Z_q/2+b_p\beta^2)q^2-C_v};
\quad C_v=0\Longrightarrow\kappa^2=\frac{2\beta^2}{Z_q+2b_p\beta^2}.
\]

Even in the restricted zero-counterterm case the coupling ratio is free. This is a scoped exact obstruction to deriving \(\kappa\) from the displayed action class, not a theorem excluding additional principles. Taking \(\Lambda\) in the gate to depend on \(q\) generates additional four-form feedback in the gate-active region; the fixed-\(\Lambda\) calculation above has not eliminated that feedback. A vacuum source supplies an available scale, not the gate function, its regulator, the MOND coefficient, or independently clustering initial data.

## 6. Decision and reproducibility

The original negative-curvature/joint-zero defect is resolved by a concrete global smooth gate. The tensor-shear calculation survives and the prescribed-mask omission is exposed by exact negative controls. The scalar curvature term creates a new specific instability, and the concave addition demonstrates a rigorously bounded way to repair its sign. That continuation reaches a finite-band causal boundary; it is neither a full no-go for same-clock gravity nor a passed fundamental all-frequency candidate.

Reproduce the checks through the computation-audit runner with `contract.json`, declaring `check_gate_adm.py` as input and a fresh output directory, then validate its manifest. The recorded successful command is in `run_verified/manifest.json`. Python 3.9.6 and SymPy 1.14.0; deterministic exact arithmetic; 120-second wall cap, 110-second CPU cap and one cooperative numerical-library thread. No old simulations were rerun and no fit parameter was silently selected. No Lean theorem or global DOF certification is claimed for this route.
