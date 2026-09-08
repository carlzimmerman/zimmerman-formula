# A spatial-kernel repair passes two screens, then fails a causal-response test

2026-09-08; reference checkpoint `92ff5f9703bfa9fccc1097fcbbc081e004b548ec`.

**Full theory: OPEN, not closed.** A specific action-defined nonlocal repair
has positive matter kinetic/gradient coefficients and a derived coefficient
that removes the displayed late-time curvature growth. Its retarded metric
response nevertheless extends outside the metric light cone for a smooth,
compact-in-space, conserved **signed external probe** on its Lambda=0 stiff
member. That qualification is
essential: a healthy physical-matter realization is not yet established.
This is not a universal no-go for MOND or an empirical rejection of a model.

`research_gate.py` compares the scalar actions used by the independent
calculations, then records every result, including failures and missing gates.
Default exit 0 means reproducible algebra, not successful gravity.
Quadratic action matching does not identify different fixed clock functions
or cosmological-constant parameters; the domain distinction below is retained.

## 1. One explicit candidate and its domain

Use c=1, m=M^2>0, physical ADM metric with
K_ij=(dot h_ij-Lie_shift h_ij)/(2N), and pi=h_ij pi^ij. Start with

\[
S_0=\int dT\,d^3x\,[\pi^{ij}\dot h_{ij}+p_\sigma\dot\sigma
-N(\mathcal H_{EH}+\mathcal H_m-m\sqrt h f(s))
-N^i\mathcal H_i-\lambda(\pi-\sqrt h\tau(T))],
\]
\[
\mathcal H_{EH}={2\over m\sqrt h}(\pi^{ij}\pi_{ij}-\pi^2/2)
-{m\sqrt h\over2}R+m\Lambda\sqrt h,\qquad
f(s)=2a_0^2[1-(1+y)e^{-y}],\quad y=\sqrt s/a_0,
\quad s=a_i a^i,\quad a_i=D_i\log N.
\]

Matter is minimally coupled to this metric, initially a shift-symmetric
P(X), X=-(partial sigma)^2/2. The source-response test specializes to P=X.
For that case H_m=p_sigma^2/(2sqrt(h))+sqrt(h)h^ij partial_i(sigma)
partial_j(sigma)/2, and H_i=-2h_ij D_k pi^jk+p_sigma partial_i(sigma).
Tau(T) is a prescribed trace-clock function in this ADM formulation;
covariant clock restoration and its complete constraint count are NOT proved.
The displayed cosmological family can be specified as
tau_Lambda(T)=-3m H_d coth(3H_d T), Lambda=3H_d^2, with continuous Lambda=0
limit tau_0=-m/T. The endpoint test uses Lambda>0; the exact causal witness
uses Lambda=0. They are different parameter members of one stated family,
NOT interchangeable solutions of one fixed positive-Lambda action.

Define the spatial operator L=-Delta_h and
I=R[h]-4D_i a^i-2a_i a^i. With the h-volume inner product, add

\[
\boxed{\Delta S_b=-{m\over16}\int dT\,
\langle\sqrt N I,L^{-1}\sqrt N I\rangle_h
-{b\tau_T\over24}\int dT\,
\langle L^{-1}I,L^{-1}I\rangle_h},\qquad b>0.
\]

This is a specified action, not a stress tensor assigned after variation.
Inverse operators are spatial, local in T, and self-adjoint. On a compact
slice use the zero-mean spectral inverse, annihilating its constant kernel;
on R^3 use spatial decay for the displayed dipole source. Those boundary
problems are not interchangeable. Nonlinear domains/continuity remain open.
No time derivatives of a new auxiliary field have been introduced, but this
fact ALONE does not count nonlinear gravitational degrees of freedom.

The action's full metric variation is not completed. The executed evidence
is the finite Legendre map, homogeneous equations, actual quadratic
variations and curvature, and the retarded linear response described below.

## 2. Why merely adding the trace constraint was not a new cure

`trace_hamiltonian.py` varies all six independent metric momenta, correctly
including off-diagonal factors. With ell=lambda/N and phi=tau/m it obtains

\[
L_g=mN\sqrt h[(R+K_{ij}K^{ij}-K^2)/2-\Lambda+f
+\ell K-3\ell^2/4+\phi\ell].
\]

Eliminating ell gives the same local VCDM trace-degenerate action as before:
R/2+K_T^2/2+2phi K/3+phi^2/3-Lambda+f. The Hamiltonians differ by
(pi-m sqrt(h)phi)(pi+m sqrt(h)phi)/(3m sqrt(h)), a constraint multiple.
Global equivalence additionally requires nonzero tau_T and vanishing surface
terms; constant-tau vacuum is separately exceptional. That equivalence is
an analytic conditional argument, not a full functional Poisson audit.

The homogeneous action is unchanged by Delta S_b since I=0 there. For
volume v=a^3 and canonical matter, actual preservation of

\[
C=-3vp_v^2/(4m)+m\Lambda v+p_\sigma^2/(2v),\qquad
F=p_v-2\tau/3
\]

gives Cdot=-3 lambda v rho and Fdot=2N rho-2tau_T/3 on the weak surface.
Thus lambda=0, N=tau_T/(3rho), K=-tau/m on the charged branch. The exact
stiff solution N=1, tau=-m/T, a=T^(1/3), q=sqrt(2m/3)/T expands.
Neither H=0 nor p_q=0 has been imposed to manufacture that solution.

## 3. General spatial-kernel obstruction and the actual repair

On flat FLRW let q=dot(sigma), Z=P_X>0, D=P_X+q^2P_XX>0,
kappa=k/a, and use physical proper time. Write N=1+n and
h_ij=a^2 exp(2z)delta_ij, so the leading physical potentials are Phi=n,
Psi=-z. Independent static variations of
Q z^2+2B nz+C n^2 give no slip only if B=Q. Retaining the seed static
coefficient then fixes C=Q+m kappa^2(alpha-1), alpha=f_s.
This is a **leading static quadratic-channel** statement, not full PPN.

The actual spatial curvature yields I_1=4kappa^2(z+n). Varying the new
action before eliminating its auxiliaries gives at alpha=f_s(0)=1

\[
n={D+3Z\over Dq}\dot u,\quad
z+n=-{3Zq\over2Q}\dot u,\quad
v_{shift}=-{3Zq\over2mk}u,
\]
\[
L_{red}={a^3\over2}(\mathcal K\dot u^2-\mathcal B u^2),\quad
\boxed{\mathcal K=-6Z-{9Z^2\over D}-{9Z^2q^2\over2Q}},\quad
\mathcal B=Z\kappa^2+{3Z^2q^2\over2m}>0.
\]

Hence all positive Q fail. Any unbounded |Q| has negative limiting kinetic
coefficient. In this fixed kinetic architecture finite polynomial
higher-spatial-derivative repairs cannot cure the ultraviolet problem.
A negative bounded kernel CAN pass:

\[
-{3q^2ZD\over2(2D+3Z)}<Q<0.
\]

The first fixed-clock choice Q=-m/(6T^2) passes a stiff background but fails
on an exactly solved, healthy canonical P=X-V0 background: m=3,T=1,V0=1/2
gives N=2 and K_matter=-6. This counterexample is on shell, not an arbitrary
choice of background coefficients.

Delta S_b instead derives Q=-2b tau_T/(3N). The homogeneous equations give
tau_T/N=(3/2)q^2Z, so Q=-bq^2Z and

\[
\mathcal K=Z\left({9\over2b}-6-9c_m^2\right),\qquad
c_{UV}^2={1\over9/(2b)-6-9c_m^2},\quad c_m^2=Z/D.
\]

For b=1/4 and 0<c_m^2<=1 the displayed coefficients are positive and
subluminal. This repairs the fixed-clock counterexample in a DIFFERENT,
explicitly defined action; the scripts do not merge these variants.
The surviving perturbation has delta rho=-3qZ dot(u): it is matter, not a
certification that an extra gravitational scalar is absent everywhere.

## 4. Next gate: the expanding late-time endpoint selects b=3/16

For canonical matter write K_s=9/(2b)-15 (not the spatial operator L).
On the exact stiff-plus-Lambda background

\[
a^3=\sinh(3H_dt),\quad H=H_d\coth(3H_dt),\quad
q=\sqrt{6m}H_d\operatorname{csch}(3H_dt),\quad\tau=-3mH,
\]

the independently varied matter equation is
u_ddot+3H u_dot+[kappa^2+3q^2/(2m)]u/K_s=0.
`adaptive_endpoint.py` differentiates the 4D metric to get Ricci and Weyl,
and verifies the pure-time-coordinate-change identity directly. With
R_com=delta R-Rbar_dot u/q, q=q0/a^3, u->U0, it obtains

\[
\boxed{\lim_{a\to\infty}{R_{com}\over a}
=-{10H_d(K_s-9)k^2U_0\over K_s q_0}}.
\]

Thus b=1/4 (K_s=3) has real gauge-invariant curvature growth. Solving the
growth equation, not guessing its answer, selects **b=3/16, K_s=9**. Then

\[
R_{com}\to288H_d^3U_3/q_0,\qquad
E_{\hat x\hat x}={q\over2m}(2Hu-\dot u)\to0.
\]

The other displayed Ricci curvature observables remain bounded or decay.
DOP853 transfers on t in [1,8], m=H_d=k=1, at two tolerances corroborate
the analytic calculation. They integrate p=a^3 u_dot to control numerical
error in the decaying mode. Finite numerical agreement is not the proof of
the all-time asymptotic statement, nor is this a nonlinear stability result.

## 5. Next gate: a retarded physical-curvature counterexample

`causal_response.py` couples delta g_mn Sigma^mn/2 to the SAME quadratic
action. On a=t^(1/3), q=sqrt(2m/3)/t, let eta be smooth, radial, supported
in r<1, with integral one; set g=partial_x eta (zero mean). Take

\[
\Sigma^{00}=R(t)g+C(t)\Delta g,\quad
\Sigma^{0i}=a^{-2}j(t)\partial_i g,\quad
\Sigma^{ij}=a^{-2}P(t)g\delta^{ij},
\]
\[
P=-\dot j-j/t,\quad
R={j\over t}+{1\over t}\int_1^t{j(s)\over s}ds,\quad
C=-{1\over t}\int_1^t s^{1/3}j(s)ds.
\]

All FOUR background-covariant stress divergences vanish by direct
Christoffel calculation. Set j=0 before t=1 and
j=exp[-1/(t-1)^2] through t=3/2, with an optional smooth later cutoff.
Scalar auxiliaries vanish initially; longitudinal momentum/isotropic stress
do not source transverse vectors or TT tensors, whose incoming solutions
are set to zero. There is no preexisting constraint tail in this witness.

The compact retarded matter packet can be written u=partial_x u0, with u0
radial. Integrating u0 is not activating a homogeneous physical mode.
For the required radial moment, the exact retarded Green kernel is
G_K(t,s)=Theta(t-s)s sqrt(K_s) sin[log(t/s)/sqrt(K_s)].
Its differential equation, initial value and unit derivative jump are checked.

The exterior orthonormal electric Weyl curvature follows from the metric:

\[
E_{\hat i\hat j}={D_{ij}\over2a^2}
[n-z+a^2(\dot\beta_{shift}+H\beta_{shift})],\quad
\beta_{shift}=-{3\over2m}\Delta^{-1}(qu-J),
\quad D_{ij}=\partial_i\partial_j-\delta_{ij}\Delta/3.
\]

All nine Weyl components and slicing invariance are checked. The exterior
time amplitude is derived to be

\[
F(t)={3\over K_s}\dot j+{j\over K_s t}
+{\dot W\over t}-{2W\over3t^2},\quad
(\partial_t^2+t^{-1}\partial_t+(K_st^2)^{-1})W
={4\over K_s}\dot j+{4K_s-3\over K_s^2t}j+{4R\over K_s}.
\]

The coefficient 3/K_s is nonzero, including at the curvature-selected K_s=9.
The exact dipole inverse Laplacian gives E_hat_xx=-9F/(8pi m r^4) on axis.
At t=3/2,r=3,m=1, the positive retarded-kernel bound yields

\[
\boxed{|E_{\hat x\hat x}|>{2e^{-4}\over27\pi}>0
\quad(K_s=9),}
\]

outside the metric light cone from the source support. An arbitrarily small
overall amplitude keeps this finite-time response perturbative. The result
is physical curvature, not an inference from an elliptic potential alone.
A separate flat alpha=0 control retains vectors/tensors and reproduces
causal GR in all nine tidal components, checking that distinction.

The positivity argument also excludes coefficient tuning within the entire
finite, canonical, subluminal family K_s>=1. On 1<=s<=t<=3/2 the kernel
bracket is bounded below by 2/3-1/(8K_s)>0; all three remainder-source
weights are positive. Therefore the SAME event obeys

\[
\boxed{|E_{\hat x\hat x}|>{2e^{-4}\over3\pi m K_s}>0
\qquad(1\le K_s<\infty).}
\]

The script proves these signs after K_s=1+w, w>=0, and derives the matter
speed squared 1/K_s from its actual equation. The singular infinite-K_s limit is
not included. This is a scoped obstruction for the displayed adaptive
spatial-kernel family, not every nonlocal action or every physical source.

**Exact scope:** the causal support of the linear response to an arbitrary
conserved signed external stress on the Lambda=0 stiff member. Extension
of this exact bound to the fixed positive-Lambda member is not proved here.
This source has not been derived from a
positive-energy dynamical matter sector. A theorem about signals realizable
by ordinary matter needs that extra implication. Neither a finite-dimensional
bracket test nor a Green-function calculation silently supplies it.

## 6. Exceptional sectors and the remaining requirements

At Q=0 but q!=0 the quadratic action is re-Legendre-transformed, not
substituted into 1/Q solutions: primary p_n,p_z,p_v and their three secondary
constraints have a computed rank-six Poisson matrix. Preservation, including
arbitrary explicit time derivatives, fixes multipliers and leaves one
matter pair with u_dot=0. This is a scalar-sector count, not full gravity.

At exactly q=Q=0 the canonical quadratic matter action is rebuilt first;
n,z disappear, and the matter speed is 1. The finite-q branch agrees in
that speed only at b=9/32, which differs from the curvature selection 3/16.
This is a nonuniform-limit diagnostic, not a universal theorem forbidding
all controlled limiting prescriptions. The mean-zero inverse also demands
a separate nonlinear k=0 analysis; no inverse k^2 is assigned at k=0.

Minimal P(X) matter has the off-shell identity
nabla_mu T_m^{mu nu}=E_sigma nabla^nu sigma,
E_sigma=nabla_mu(P_X nabla^mu sigma). Thus its ordinary conservation follows
on shell, not merely conservation of matter plus an assigned phantom source.

The exact exponential f is retained, and its seed relation is mu=1-f_s.
But a full nonlinear static solution of the NEW nonlocal action, independently
derived Phi/Psi at the required order, measured Newton constant, all PPN
parameters, full tensor/vector/clock analysis, strong-coupling control, and
observationally viable cosmology are still uncertified. No PPN value, full
gravitational count, empirical fit, or a0-Lambda derivation is reported.

## 7. Why the previous closure certificates cannot be inherited

The read-only legacy audit reproduces two exact errors without judging intent:

* In `sf58_full_nonlinear_adm_four_constraint_closure.py`, the displayed
  constraint K p_q=0 imposes p_q=0 for K!=0. Solving multipliers does not
  make p_q unconstrained. At K=L=0, its source constraint is -rho=0, not
  an automatically absent equation allowing arbitrary homogeneous matter.
* In `elliptic_corner/constrained_hamiltonian.py`, symmetrically dressing
  G_0mu by constant mu while keeping G_ij gives actual raised-index divergence
  (0,2(1-mu)partial_x Psi_tt,2(1-mu)partial_y Psi_tt,
  2(1-mu)partial_z Psi_tt). A compact smooth no-slip witness gives
  (0,1,0,0) at the origin for mu=1/2. Proportionality to the old plus-sign
  expression was not a full Bianchi identity.

These are mathematical overclaims in specific implementations, not evidence
that a named model deliberately lied. Their useful algebra is retained.

## 8. The next unavoidable calculation

Do not keep tuning b to pass more tests: every finite subluminal b in the
Lambda=0 branch already fails the stated conserved-probe support test.
First repeat the retarded calculation with the fixed positive-Lambda
tau_Lambda(T), keeping the full background coefficients rather than silently
using the stiff limit. Decide the physical implication by
deriving a compact perturbation from an explicitly healthy minimally coupled
matter action and computing its retarded Weyl response with full initial
constraints. If the tail survives, discard this spatially instantaneous
repair class under the causal requirement. If realizability forbids the
probe, prove precisely that restriction before advancing the full nonlinear
Dirac and zero-mode calculation. No new model parameter should hide this gap.

The user-linked NavierStokesAndEuler repository is relevant to **checking the
statement being proved**, not a supplied gravity mechanism; see
`FORMAL_VERIFICATION_PATH.md`. No global novelty claim is made here.
